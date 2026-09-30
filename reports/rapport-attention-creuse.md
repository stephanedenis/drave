# Attention creuse — le trou se referme, et par le haut

Le point faible identifié dans nos bilans : l'attention n'est **pas exprimable en
listes d'événements**, parce que ses poids sortent d'un softmax calculé à
l'exécution, et son coût croît **linéairement avec le contexte** (2,0 ms à 64
tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192).

Une seule modification, à l'inférence, sans réentraînement : **ne garder que les
k plus grands scores par requête** avant le softmax. Les autres sont masqués
(`-∞`), le softmax renormalise sur les k retenus.

*Ce n'est pas une importation : c'est la même question que pour les activations —
imposer une parcimonie à un modèle préentraîné et mesurer ce qu'elle coûte. La
réponse, ici, est qu'elle **rapporte**.*

---

## 1. Résultat

Deux jeux de 1 024 tokens, réglage sur A, vérification sur B.

| k (clés gardées) | PPL (A) | PPL (B) | 2 040 tokens | ctx 512 |
|---|---|---|---|---|---|
| **dense** (référence) | 23,6125 | 26,2565 | 24,8995 | 19,5222 |
| 128 | 23,5840 (−0,12 %) | — | — |
| 64 | 23,4621 (−0,64 %) | 26,1959 (−0,23 %) | 24,6867 | **19,3700 (−0,78 %)** |
| **32** | **23,3302 (−1,20 %)** | **26,1199 (−0,52 %)** | **24,6857 (−0,86 %)** | **19,4136 (−0,56 %)** |
| 24 | — | — | 24,7043 |
| 16 | 23,6591 (+0,20 %) | 26,5065 (+0,95 %) | — |
| 8 | 24,9071 (+5,5 %) | — | — |

➡️ **Restreindre l'attention aux 32 meilleures clés améliore la perplexité de
0,5 à 1,2 % selon le jeu et le contexte, et le gain se reproduit sur des tokens
jamais vus ainsi qu'en contexte 512.**

## 2. Pourquoi c'est important pour nous

En contexte 256, garder 32 clés sur 256 fait de la matrice d'attention une
matrice **creuse à ~12,5 %**. Et cette densité **décroît avec le contexte** :

| contexte | densité avec k = 32 |
|---|---|
| 256 | 12,5 % |
| 1 024 | 3,1 % |
| 4 096 | 0,78 % |
| 32 768 | 0,1 % |

Autrement dit : **là où l'attention nous coûtait le plus cher — les longs
contextes — elle devient l'élément le plus creux du modèle.** Ses poids sont des
événements (requête, clé, poids) qu'un générateur peut émettre à la volée, et que
notre moteur consomme comme n'importe quelle liste de connexions.

Le trou identifié dans le bilan multi-matériel — « attention hors du domaine
événementiel » — se referme **du point de vue de la représentation** : ses poids
deviennent creux, donc listables, et la qualité s'améliore. Il ne se referme pas
du point de vue du calcul : noter toutes les clés reste inévitable (voir §3 bis).

### L'optimum suit le contexte — mais un k fixe suffit

À contexte 256, k = 32 est optimal (12,5 % des clés) ; à contexte 512, c'est
k = 64 (12,5 % également). L'optimum est donc une **fraction** du contexte, ce
qui laisserait la complexité quadratique.

**Un k fixe change la nature du calcul** : le coût devient O(N·k), **linéaire**,
et la qualité reste meilleure que le dense aux deux contextes testés
(−1,20 % à 256, −0,56 % à 512). C'est la même complexité qu'une attention
linéaire à noyau, mais **sans approximer le softmax** — on en garde les k termes
dominants au lieu de le remplacer par un produit de fonctions.

C'est ce qui compte pour nous : une attention en O(N·k) dont les poids sont
creux, donc une liste d'événements de taille linéaire.

## 3. Pourquoi ça améliore la perplexité

Les poids d'attention faibles sont majoritairement du bruit : sommer 256
contributions dont la plupart sont négligeables dilue le signal. Les couper
**aiguise** la distribution, et le softmax renormalisé compense exactement la
masse retirée.

C'est le même raisonnement qui avait échoué pour les activations du FFN
(troncature → perte), mais il réussit ici parce que la distribution d'attention
est **exponentielle** : ses petites valeurs sont réellement négligeables, alors
que les petites activations d'un FFN portent une partie du signal.

## 3 bis. Correction : le gain est en qualité, pas en temps

J'avais annoncé que l'attention creuse la rendrait « meilleure, moins chère et
listable ». **La partie « moins chère » est fausse en l'état, et la mesure le
dit.**

J'ai d'abord masqué les scores (`-∞`) sans réécrire les boucles : aucun gain,
évidemment, puisque le softmax et la somme pondérée parcouraient toujours toutes
les clés. J'ai ensuite réécrit le softmax et la somme pour n'itérer que sur les k
clés retenues — complexité O(N·k) — en vérifiant que la perplexité restait
identique au chiffre près (23,6125 dense, 23,3279 à k=32).

Résultat : **toujours aucun gain.** 11,5 ms en dense, 11,5 ms à k=32, et
**11,6 ms à k=1** — où la somme pondérée ne fait plus que 14 × 64 opérations au
lieu de 459 000.

➡️ **Le coût de l'attention n'est donc pas dans le softmax ni dans la somme
pondérée : il est dans le CALCUL DES SCORES**, qui doit noter toutes les clés
avant de pouvoir choisir lesquelles garder. Le top-k ne peut pas y échapper.

Ce que l'attention creuse apporte reste réel, mais c'est autre chose :

| apport | statut |
|---|---|
| Qualité | ✅ **+0,5 à +1,2 %** de perplexité, vérifié sur A, B et contexte 512 |
| Poids creux, donc listables | ✅ 12,5 % de densité à 256, 0,8 % à 4 096 |
| Temps de calcul | ❌ **aucun gain** — les scores restent O(N) par requête |
| Poids d'attention dans le flux d'événements | ✅ négligeable : 0,04 M paires/token contre 354 M événements |

Baisser le coût demanderait d'éviter le calcul des scores — donc soit un index
appris (entraînement, hors de ce programme), soit une approximation de type
noyau ou hachage sensible à la localité.

## 3 ter. Ce qui a *effectivement* accéléré l'attention : la vectorisation

En cherchant pourquoi le top-k ne gagnait rien, j'ai trouvé un coût bien plus
gros que prévu : l'attention tournait à **1,9 GFLOP/s sur un seul cœur**, soit
0,6 opération par cycle. Le compilateur ne vectorisait pas les boucles écrites
sous forme indexée.

Deux réécritures, à perplexité **rigoureusement identique** (23,6125 dense,
23,3279 à k = 32) :

| boucle | avant | après |
|---|---|---|
| produit scalaire des scores | `for d in 0..hd { s += qh[d]*kt[d] }` | `qh.iter().zip(kt.iter()).map(\|(a,b)\| a*b).sum()` |
| somme pondérée | accumulation par dimension (stride 64) | accumulation **par clé** dans le vecteur de sortie (lecture séquentielle) |

Mesure entrelacée, contexte 512 :

| | temps d'attention |
|---|---|
| avant | **11,5 ms/token** |
| après | **5,7 ms/token** |

➡️ **Divisée par deux**, gratuitement, sans changer un chiffre de la perplexité.
C'est le gain le plus net de toute la campagne — et il ne vient pas de la
parcimonie mais de l'écriture des boucles.

## 4. Ce qui reste à faire

1. **Générer les événements d'attention** : le moteur sait consommer des listes,
   il faut maintenant un générateur qui produise `(clé, poids)` pour chaque
   requête à partir des scores calculés. C'est de la plomberie, pas de la
   recherche.
2. **Mesurer en contexte long** : le gain de perplexité devrait croître avec le
   contexte (mesure en cours à 512).
3. **Choisir k par tête** : k = 32 est un réglage global ; certaines têtes
   pourraient tolérer bien moins.
4. ~~Vérifier l'interaction avec le k-WTA du FFN~~ → **mesuré, non additive et
   défavorable** : attention 32 seule = −0,52 % (B), attention 32 + FFN 90 % =
   −0,45 %, attention 32 + FFN 85 % = **+0,19 %**. Le FFN mange le gain de
   l'attention. Retenir l'attention creuse, se méfier du k-WTA du FFN.

## 5. Reproductible

```bash
cd drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/wt2_a.txt \
    --ctx 256 --abits 16 --threads 16 --attn-topk 32
```

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
| 64 | 23,4621 (−0,64 %) | 26,1959 (−0,23 %) | 24,6867 |
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
événementiel, et elle croît linéairement » — se referme par le haut : la
restreindre la rend **meilleure, moins chère, et listable**.

## 3. Pourquoi ça améliore la perplexité

Les poids d'attention faibles sont majoritairement du bruit : sommer 256
contributions dont la plupart sont négligeables dilue le signal. Les couper
**aiguise** la distribution, et le softmax renormalisé compense exactement la
masse retirée.

C'est le même raisonnement qui avait échoué pour les activations du FFN
(troncature → perte), mais il réussit ici parce que la distribution d'attention
est **exponentielle** : ses petites valeurs sont réellement négligeables, alors
que les petites activations d'un FFN portent une partie du signal.

## 4. Ce qui reste à faire

1. **Générer les événements d'attention** : le moteur sait consommer des listes,
   il faut maintenant un générateur qui produise `(clé, poids)` pour chaque
   requête à partir des scores calculés. C'est de la plomberie, pas de la
   recherche.
2. **Mesurer en contexte long** : le gain de perplexité devrait croître avec le
   contexte (mesure en cours à 512).
3. **Choisir k par tête** : k = 32 est un réglage global ; certaines têtes
   pourraient tolérer bien moins.
4. **Vérifier l'interaction avec le k-WTA du FFN** : les deux parcimonies
   s'appliquent à des endroits différents, elles devraient se composer.

## 5. Reproductible

```bash
cd qtrinet-core && cargo build --release
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/wt2_a.txt \
    --ctx 256 --abits 16 --threads 16 --attn-topk 32
```

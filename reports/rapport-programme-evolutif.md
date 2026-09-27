# Programme « journaliser, faire évoluer » — ce que la mesure autorise

Évaluation du programme : *journaliser les flux d'activation, construire et
entraîner des versions concurrentes en parallèle sur les ressources inutilisées,
avec moins de couches, des grappes par expertise, des portions récursives, et un
apprentissage de nouveaux nœuds par rétroaction sur la couche antérieure.*

Tout ce qui suit est mesuré sur ce dépôt, ou explicitement marqué comme
raisonnement.

---

## 1. Journaliser : c'est fait, et c'est presque gratuit

| | Mesure |
|---|---|
| Capteur de co-activation branché sur une projection | **+3,0 %** (96,75 s → 99,64 s sur 1 025 tokens) |
| Journal complet des entrées d'une couche | 2048 × 896 × 4 o = **7 Mo pour 2 048 tokens** |
| Journal des activations de toutes les couches (24) | ~1,2 Mo/token, soit 19 Mo/s à 15,8 tok/s |

**La traçabilité totale ne demande pas de journaliser les événements.** Les poids
sont statiques et les événements en sont une fonction déterministe : journaliser
les *listes d'activations* suffit à rejouer intégralement le calcul. 1,2 Mo/token
au lieu de 706 Mo. C'est le point (1) du programme, et il est acquis.

Sur les ressources libres : l'inférence occupe 16 threads sur 40, une carte GPU
sur deux, et 125 Go de RAM dont l'inférence n'utilise que 1,3 Go.

## 2. Grappes corrélées : deux usages, un seul tient

**Usage A — prédire la difficulté : faible.** Journal de la couche 12 sur 2 040
tokens de WikiText-2, k-moyennes sur les vecteurs d'entrée du FFN :

| Mesure | Valeur |
|---|---|
| η² (variance de perte expliquée par la grappe), apprentissage | 6,2 % |
| Écart grappe la plus dure / la plus facile | **7,1×** (perte 5,51 contre 0,77) |
| Taille des grappes les plus dures | 0,4 à 1,6 % des tokens |
| **R² hors échantillon (K=32)** | **+0,007** |
| **Corrélation des pertes par grappe, apprise → testée (K=32)** | **r = +0,573** |
| Même corrélation à K=128 | r = +0,232 |
| Lecture **linéaire** de la perte depuis les activations | **R² < 0** à toute régularisation (−7,5 à −0,21) |

➡️ **Les motifs difficiles existent et se reproduisent** (r = 0,57 d'une moitié à
l'autre), mais **ils expliquent moins de 1 % de la variance de perte** : la
difficulté est à 99 % propre au token, pas au motif. Et plus on affine les
grappes, plus ça se dégrade (0,57 → 0,23) — signature classique du bruit que l'on
prend pour de la structure.

**Usage B — réorganiser pour la localité : fort, et déjà mesuré.** Des grappes
d'activation *corrélées* veulent dire des neurones qui tirent ensemble. Réorganiser
les listes pour que ces neurones soient **contigus** a déjà été mesuré sur ce
projet : **+30 % de débit à taux d'événements égal** (élagage contigu 17,91 tok/s
contre dispersé 13,77), et c'est la même conclusion que l'effondrement du mode
épars — le coût d'un événement dépend de la ligne de cache qu'il touche.

➡️ **L'optimisation d'architecture par les grappes est réelle, mais elle porte sur
la disposition mémoire, pas sur la structure de difficulté.**

## 3. Nouveaux nœuds par rétroaction : où ça peut marcher

Mesuré au tour précédent :

- **69,2 % des poids** sont dans des projections **saturées** (rang des lignes =
  dimension d'entrée) : `ffn_gate`, `ffn_up`, `attn_q`, `attn_output`. Là, **tout
  nouveau nœud linéaire est une combinaison des existants** — vérifié : 100,00 %
  des directions de la trace hebbienne, y compris son résidu non linéaire, sont
  dans l'espace des poids.
- **30,8 %** sont dans des projections **ouvertes** : `attn_k` (127/896),
  `attn_v` (128/896), `ffn_down` (896/4864). Là, un nouveau nœud apporte de la
  dimension.
- Et **401 856 monômes quadratiques** `x_i·x_j` sont hors du span linéaire : c'est
  là qu'est l'espace réellement neuf.

➡️ La rétroaction négative doit viser **les projections ouvertes et les
caractéristiques non linéaires**, pas les projections saturées.

## 4. Versions concurrentes : la capacité est mesurable

Perplexité sur 2 040 tokens, selon les threads alloués :

| Threads par variante | Durée | Variantes en parallèle | Débit |
|---|---|---|---|
| 4 | 366,8 s | 10 | **98 évaluations/h** |
| 8 | 215,5 s | 5 | 83 évaluations/h |
| 1 (extrapolé) | ~1 284 s | 40 | ~112 évaluations/h |

➡️ **~100 évaluations de modèle par heure**, en continu, sans gêner l'inférence.
Soit 2 400 par jour : une boucle évolutive a un vrai budget expérimental. À noter :
allouer *moins* de threads par variante donne un meilleur débit global — le moteur
monte mal en charge au-delà de 8 threads.

## 5. Deux idées du programme que l'architecture événementielle sert particulièrement

**Les experts (grappes par expertise) sont un ajustement naturel.** Un expert qui
ne tire pas coûte **zéro octet** : ses listes ne sont pas lues. Une implémentation
dense doit tenir tous les experts en mémoire et payer le routeur. Un modèle à
100 experts dont 2 tirent par token coûte donc, chez nous, le prix de 2 experts —
et non celui de 100.

**La récursion est adaptée à notre goulot.** Le moteur lit 706 Mo/token à
10,4 Go/s alors que la machine en offre 28,7 : il est **borné par le calcul de
dispersion, pas par la mémoire** (2,8× de marge). Réutiliser K fois les mêmes
listes ne coûte **aucune mémoire supplémentaire** et consomme la marge
disponible : ~2,8 passes supplémentaires tiennent dans la bande passante
actuelle. Un transformeur bouclé est donc, sur ce moteur précis, le bon côté du
compromis.

## 6. Ce qui manque, et c'est un seul point

**Aucune capacité d'entraînement.** La pile sait *mesurer* (perplexité, 100/h) et
sait *ajuster une lecture* (moindres carrés, algèbre linéaire, OpenBLAS à
759 GFLOP/s), mais elle ne sait pas rétropropager : pas d'autogradage, pas
d'optimiseur, aucun cadre d'apprentissage installé.

La boucle constructible **aujourd'hui**, sans entraînement :

1. **Journaliser** pendant l'inférence (+3,0 %).
2. **Proposer** des candidats : grappes contiguës (localité), nœuds sur les
   projections ouvertes, caractéristiques quadratiques, experts par motif.
3. **Ajuster la lecture** des nouveaux nœuds par moindres carrés sur le journal —
   pas de rétropropagation.
4. **Évaluer** la perplexité sur texte retenu (~100/h sur les threads libres).
5. **Sélectionner** et garder les variantes gagnantes — versions concurrentes.

L'étape 3 est la clé qui rend le programme réalisable sans cadre
d'apprentissage ; l'étape 4 lui donne un débit connu. Ce qui manque pour la
boucle complète est donc du **plomberie** : charger un modèle patché (nœuds
supplémentaires) depuis un fichier, ce que le moteur ne sait pas encore faire.

## 7. Reproductible

```bash
# journal d'activations + pertes par token
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/wt2_ids.txt \
    --ctx 256 --abits 16 --threads 16 --hebbian 12
# -> /tmp/act_log.bin (2048 x 896 f32), /tmp/loss_log.bin (pertes par token)
```

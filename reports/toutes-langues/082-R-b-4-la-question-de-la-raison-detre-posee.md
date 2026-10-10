> Campagne : **toutes-langues** · expérience **R**
> Titre : B.4 La question de la raison d'être, posée franchement
> Date réelle : **2026-10-07 07:19 HAE** (source : commit `597f577`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## B.4 La question de la raison d'être, posée franchement

Drave veut **notre propre** pont linguistico-sémantique : émuler les premières couches
d'un gros modèle, en boîte noire, sans rétropropagation, pour obtenir un modèle récurrent
capable de répondre au premier niveau abstrait.

**Les mesures de cette session disent quelque chose d'inconfortable sur cette
hypothèse.** Le §70 a mesuré, sur trois jeux de caractéristiques emboîtés :

| caractéristiques | fidélité | rapport contenu/langue |
|---|---:|---:|
| **l'entrée seule du professeur, 0 neurone** | **0,5161** | **1,698** |
| les états de notre réservoir | 0,4751 | **1,354** |
| entrée + réservoir | **0,5309** | 1,598 |
| *le professeur à sa couche 8* | — | *10,912* |

**Notre calcul propre — le réservoir récurrent — fait MOINS BIEN que l'entrée du
professeur lue linéairement, sur les deux axes à la fois.** Quatre mesures indépendantes
le confirment (§29, §34, §70, §71).

**Conséquence sur la raison d'être** : en l'état, Drave n'est pas un pont — c'est une
**dégradation** de la représentation du professeur. Le « pont » qui fonctionne le mieux
mesuré est une régression linéaire-quadratique sur la couche 0 du professeur, c'est-à-dire
le professeur lui-même, à peine projeté.

**Et la transformation qui compte — celle qui crée la séparation contenu/langue entre la
couche 0 et la couche 8 — n'est produite par AUCUN des mécanismes que le projet
s'autorise** : ni le réservoir aléatoire gelé (§70), ni la lecture en forme fermée
(§69, bornée à 64 %), ni le renforcement/atrophie (§72, +1,7 % du chemin nécessaire).

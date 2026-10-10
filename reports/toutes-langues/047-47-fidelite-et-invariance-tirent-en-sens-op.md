> Campagne : **toutes-langues** · expérience **47**
> Titre : 47. Fidélité et invariance TIRENT EN SENS OPPOSÉ quand le réseau grandit
> Date réelle : **2026-10-06 15:50 HAE** (source : commit `f6d40c8`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 47. Fidélité et invariance TIRENT EN SENS OPPOSÉ quand le réseau grandit

Le journal de la croissance (§44, couche 10, ride 0,03, lecture quadratique,
multi-échelle, 300 langues d'ajustement et 51 de validation) donne, à chaque
naissance, la fidélité **et** l'invariance. Les deux courbes vont dans des directions
opposées, et de façon monotone :

| neurones | fidélité TEST | invariance inter-langue | pire paire |
|---:|---:|---:|---:|
| 8 | 0,6151 | **0,9437** | **0,7399** |
| 24 | 0,6261 | 0,9206 | 0,6551 |
| 40 | 0,6294 | 0,9084 | 0,6559 |
| 64 | 0,6287 | 0,8971 | 0,6625 |
| 96 | 0,6311 | 0,8819 | 0,6419 |
| 128 | 0,6302 | 0,8760 | 0,5935 |
| 160 | 0,6327 | 0,8662 | 0,5737 |
| 179 | **0,6336** | **0,8661** | **0,5594** |

| | 8 → 179 neurones |
|---|---:|
| fidélité TEST | **+0,0185** |
| invariance | **−0,0776** |
| pire paire | **−0,1805** |

**Le coût est quatre fois le gain, et il porte exactement sur ce que la mission
cherche.** Ajouter des neurones rend le pont plus fidèle *et moins interlingue*.

### 47.1 Pourquoi, et ce n'est pas un accident

La lecture est ajustée pour reproduire la représentation du professeur. Or **le
professeur garde lui-même beaucoup de structure propre aux langues** : son invariance
est de 0,6836 à la couche 8 et 0,6529 à la couche 10 (§44, §41). Un réseau plus
grand reproduit davantage de cette structure **et donc davantage de marque
linguistique**.

Autrement dit : **le pont devient plus fidèle et moins « pont » à mesure qu'il
grandit.** Ce n'est pas un défaut de réglage, c'est l'objectif qui est ambigu — on
demande au même ajustement de copier la cible *et* d'effacer ce que la cible contient.

### 47.2 Le résultat contre-intuitif : le PETIT réseau est presque aussi bon

À **8 neurones**, la fidélité vaut déjà 0,6151 contre 0,6336 au mieux — **2 % de
moins** — et l'invariance est de 0,9437 contre 0,8661. Si l'objectif est un pont
interlingue, **un réseau huit fois plus petit est meilleur sur l'axe qui compte**.

### 47.3 La suite que cela désigne : une lecture ajustée SOUS CONTRAINTE d'invariance

L'ajustement actuel minimise `‖XW − Y‖²` seul. Il ignore complètement l'invariance.
Or la pénalité manquante **reste en forme fermée** :

> pénaliser la variance **inter-langue** de la sortie `XW` — c'est-à-dire
> `Σ_i ‖m_i − m̄‖²`, où `m_i` est la moyenne par langue de la sortie — ajoute un terme
> **quadratique en `W`**. L'objectif total reste quadratique, donc résoluble d'un seul
> coup, sans rétropropagation.

C'est un changement d'objectif, pas d'algorithme : on demande à la lecture de copier
la cible **tout en rapprochant les langues**, avec un curseur pour doser. C'est
exactement ce que la mission demande, et cela n'a jamais été essayé.

**Prédiction, écrite avant la mesure** : pénaliser l'invariance doit faire monter
l'invariance et baisser la fidélité ; le point intéressant est **le taux d'échange**.
Si l'invariance monte beaucoup pour peu de fidélité, le curseur est un vrai levier.


---

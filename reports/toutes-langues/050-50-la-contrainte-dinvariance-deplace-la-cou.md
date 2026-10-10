> Campagne : **toutes-langues** · expérience **50**
> Titre : 50. La contrainte d'invariance déplace la courbe, elle ne supprime pas la tension
> Date réelle : **2026-10-06 16:46 HAE** (source : commit `d355fec`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 50. La contrainte d'invariance déplace la courbe, elle ne supprime pas la tension

Le §48 avait balayé μ sur **40 neurones**. Reste à savoir si la contrainte **annule**
le compromis du §47 ou si elle le **déplace**. Mesuré à **179 neurones**, couche 8,
mêmes 300/51/41 langues, mêmes 896 canaux :

| μ | fid VAL | **fid TEST** | **invariance** | **pire paire** |
|---:|---:|---:|---:|---:|
| 0 | 0,7251 | **0,6922** | 0,7492 | 0,3719 |
| 0,03 | 0,7246 | 0,6908 | 0,7701 | 0,4089 |
| 0,1 | 0,7218 | **0,6852** | **0,8019** | **0,4255** |
| 0,3 | 0,7131 | 0,6695 | 0,8405 | 0,4575 |

### 50.1 Les deux tailles, côte à côte

| | 40 neurones | 179 neurones |
|---|---:|---:|
| **μ = 0** : fid TEST | 0,6646 | **0,6922** |
| **μ = 0** : invariance | **0,8740** | 0,7492 |
| **μ = 0,1** : fid TEST | 0,6564 | **0,6852** |
| **μ = 0,1** : invariance | **0,9157** | 0,8019 |
| **μ = 0,1** : pire paire | **0,6224** | 0,4255 |
| gain d'invariance à μ=0,1 | +0,0417 | **+0,0528** |
| coût de fidélité à μ=0,1 | −0,0082 | **−0,0070** |

**La contrainte est encore plus rentable sur le grand réseau** : +0,0528 d'invariance
pour 0,0070 de fidélité, soit **7,5 pour 1** (contre 5 pour 1 à 40 neurones). Le
levier fonctionne, et il fonctionne mieux là où le besoin est le plus grand.

### 50.2 Mais la tension demeure

À μ = 0,1, passer de 40 à 179 neurones donne **+0,0288 de fidélité pour −0,1138
d'invariance**. Le rapport est de **1 pour 4** — le même sens qu'au §47, et le même
ordre de grandeur.

**La contrainte ne supprime donc pas le compromis : elle translate toute la courbe
vers plus d'invariance.** C'est un déplacement utile — à μ=0,1 et 179 neurones on a
0,8019 d'invariance, ce que le réseau nu n'atteint nulle part — mais grandir coûte
toujours ce que la mission cherche.

### 50.3 Ce que cela dit du choix d'architecture

Puisque la tension est réelle et monotone, **le choix de taille est un choix
d'objectif, pas de qualité** :

- si l'on veut **la fidélité** — reproduire le plus exactement possible la couche du
  professeur — il faut grandir, et accepter de perdre l'invariance ;
- si l'on veut **le pont** — que les langues se ressemblent au niveau abstrait — un
  réseau **petit** et une contrainte modérée donnent le meilleur point mesuré :
  **40 neurones, μ = 0,1 → fidélité 0,6564 · invariance 0,9157 · pire paire 0,6224.**

C'est le premier endroit de ce rapport où un choix d'architecture se déduit
proprement des mesures au lieu d'être postulé.


---

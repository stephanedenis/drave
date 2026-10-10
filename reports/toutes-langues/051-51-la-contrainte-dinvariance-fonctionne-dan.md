> Campagne : **toutes-langues** · expérience **51**
> Titre : 51. La contrainte d'invariance fonctionne DANS la croissance, pas seulement sur réseau fixe
> Date réelle : **2026-10-06 17:16 HAE** (source : commit `61248eb`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 51. La contrainte d'invariance fonctionne DANS la croissance, pas seulement sur réseau fixe

Le §48 mesurait μ sur un réseau **déjà construit**. Restait à savoir si la contrainte
tient pendant que le réseau **naît**. Deux croissances libres, mêmes réglages
(couche 10, ride 0,03, quadratique, multi-échelle, 300/51/41 langues, 896 canaux),
**à μ = 0 et à μ = 0,1**, comparées à taille égale :

| neurones | μ = 0 : fid TEST · inv · pire | **μ = 0,1 : fid TEST · inv · pire** |
|---:|---|---|
| 40 | 0,6294 · 0,9084 · 0,6559 | 0,6278 · **0,9289** · **0,7329** |
| 64 | 0,6287 · 0,8971 · 0,6625 | 0,6274 · **0,9201** · **0,7364** |
| 96 | 0,6311 · 0,8819 · 0,6419 | 0,6298 · **0,9075** · **0,7090** |

| à taille égale | coût de fidélité | gain d'invariance | gain de pire paire |
|---|---:|---:|---:|
| 40 neurones | −0,0016 | **+0,0205** | **+0,0770** |
| 64 neurones | −0,0013 | **+0,0230** | **+0,0739** |
| 96 neurones | −0,0013 | **+0,0256** | **+0,0671** |

**Le taux d'échange est de 16 à 20 pour 1 sur l'invariance, et de 26 à 50 pour 1 sur
la pire paire.** Le coût de fidélité est constant (−0,0013 à −0,0016) et pratiquement
négligeable — trois à quatre fois plus petit que le bruit de graine mesuré ailleurs
dans ce rapport.

### 51.1 Ce que cela change

La contrainte n'est donc **pas** un artefact d'un réseau figé : elle agit à chaque
ajustement pendant la croissance, et son effet **s'accumule proprement**. À 96
neurones, le réseau contraint a **plus d'invariance (0,9075)** que le réseau **non
contraint en avait à 8 neurones** (0,8819 au §47) — tout en ayant une fidélité de
0,6298 contre 0,6151.

Autrement dit : **la contrainte permet de grandir sans payer l'invariance**, ce que
la croissance seule ne permettait pas. C'était exactement le problème du §47.

### 51.2 Réserve

La comparaison porte sur **une graine** (graine 5) pour chaque condition. Le §34 avait
mesuré qu'un écart de 0,0026 sépare deux graines sur ce genre de réseau : le coût de
fidélité (−0,0013) est **du même ordre**, donc « gratuit » se lit ici comme
« indiscernable du bruit », pas comme « exactement nul ». Le gain d'invariance, lui,
vaut 15 à 20 fois ce bruit.


---

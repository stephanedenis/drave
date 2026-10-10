> Campagne : **toutes-langues** · expérience **16**
> Titre : 16. Restriction ou pas : la comparaison complète, et une correction de mon invariant
> Date réelle : **2026-10-06 04:01 HAE** (source : commit `644cf5c`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 16. Restriction ou pas : la comparaison complète, et une correction de mon invariant

Les deux runs de la phase 2, même professeur, mêmes 301 langues d'apprentissage,
même panel de test (41 langues, 22 écritures) :

| | **896 canaux** (sans restriction) | **157 canaux** (50 % de l'énergie) |
|---|---:|---:|
| réseau | 45 neurones · 1 couche | 40 neurones · 1 couche |
| fidélité apprentissage | 0,6199 | 0,7459 |
| fidélité VALIDATION | 0,6231 | 0,7505 |
| **fidélité TEST** | 0,6088 | **0,7430** |
| constante témoin | 0,5766 | 0,7207 |
| **écart à la constante** | **+0,0322** | **+0,0223** |
| **invariance TEST** | 0,9682 | **0,9827** |
| **pire paire** | 0,8494 | **0,9165** |
| écart oracle TEST | +0,0327 | +0,0223 |
| écart oracle VALIDATION | +0,0111 | +0,0058 |
| rapport des écarts | 2,95 | 3,85 |

### Ce qui se confirme

**La restriction améliore tout ce qui compte pour l'usage** : +13,4 points de
fidélité, +1,5 point d'invariance, +6,7 points sur la pire paire — **avec 5 fois
moins de canaux de sortie** (157 sur 896). Le pont restreint est meilleur sur les
trois axes mesurés.

### Ce que je dois CORRIGER

**L'écart à la constante est plus GRAND sans restriction (+0,0322) qu'avec
(+0,0223).** Or j'ai présenté cet écart comme « l'invariant des +0,020 » à travers
sept périmètres et deux architectures. La mesure d'aujourd'hui dit autre chose :
c'est une **plage de +0,020 à +0,032**, pas une constante.

**Ce qui tient** : la contribution propre du pont est **petite** (2 à 3 points de
cosinus) et **ne croît pas avec la restriction** — ici elle décroît même. La
conclusion qualitative est intacte.

**Ce qui ne tient pas** : le chiffre exact. J'ai lu une coïncidence numérique
(+0,0197 ± 0,0009 sur sept périmètres) comme une loi, alors que ces sept
périmètres partageaient le même panel de 46 langues. **Changer de panel change
l'écart** — je ne l'avais pas testé, et c'est une leçon de plus sur les conclusions
tirées d'un seul jeu de données.


---

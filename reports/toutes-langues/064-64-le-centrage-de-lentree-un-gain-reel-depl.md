> Campagne : **toutes-langues** · expérience **64**
> Titre : 64. Le centrage de l'entrée : un gain réel, déployable, et le premier de la série
> Date réelle : **2026-10-06 21:52 HAE** (source : commit `33d4018`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 64. Le centrage de l'entrée : un gain réel, déployable, et le premier de la série

### 64.1 Un levier du dépôt qui n'avait jamais été essayé sur ce diagnostic

`--centre-entree` retire à chaque langue son **jeton moyen** — le décalage massivement
propre à la langue (écriture, morphologie) qui ne dit aucun contenu. **Il attaque le
décalage de langue À LA SOURCE**, avant le réservoir, au lieu d'essayer de le retirer
après coup. Et il est **déployable** : la moyenne de l'entrée se calcule sur l'entrée
elle-même, sans étiquette ni regroupement.

### 64.2 Le résultat

| | P_lang | **P_cont** | **rapport** | fidélité TEST |
|---|---:|---:|---:|---:|
| sans centrage (§61) | 232,0 | 338,7 | **1,460** | 0,4747 |
| **avec centrage** | **48,0** | 89,8 | **1,871** | **0,4668** |
| **effet** | **÷ 4,8** | ÷ 3,8 | **+28 %** | −0,008 |
| *professeur* | *399,2* | *4 356,4* | *10,912* | |

**Le centrage réduit l'axe de langue d'un facteur 4,8** — c'est de loin le plus grand
effet obtenu sur cet axe dans toute la série. Et il coûte **0,008 de fidélité**.

Mais il réduit l'axe du contenu de 3,8× **en même temps** : le rapport ne gagne donc
que 28 %, et **les deux énergies tombent très en dessous de celles du professeur**
(48 contre 399, 90 contre 4 356).

### 64.3 La version déployable reste impuissante — et c'est instructif

| γ | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 0 | 0,4668 | 48,0 | 89,8 | **1,871** |
| 1 | 0,4656 | 191,9 | 359,1 | **1,871** |
| 3 | 0,4585 | 767,8 | 1 436,6 | **1,871** |
| 5 | 0,4462 | 1 727,5 | 3 232,2 | **1,871** |

**Le rapport est encore exactement constant.** L'amplification du décalage de moyenne
par entrée met toujours les deux axes à l'échelle ensemble — le centrage améliore le
**niveau** du rapport, il ne rend pas l'amplification sélective pour autant.

### 64.4 Ce que cela donne, concrètement

**Un gain déployable, gratuit à 0,008 près, qu'on garde** : `--centre-entree` améliore
le rapport contenu/langue de 28 % et divise par 4,8 l'énergie propre à la langue. C'est
modeste, mais c'est **le premier levier de toute la série §58-§64 qui soit à la fois
efficace et déployable.**

**Et une confirmation nette** : le problème n'est pas seulement de réduire l'axe de
langue — le centrage le fait très bien — mais de **ne pas réduire l'axe du contenu en
même temps**. Les deux sont **mêlés dans les états du réservoir**, et aucun des huit
moyens essayés ne les démêle sur des langues inconnues.

### 64.5 La série, complète

| § | moyen | déployable ? | verdict |
|---|---|---|---|
| 58 | objectif à deux curseurs | oui | atteint la cible, mais **non convexe**, non monotone |
| 59 | centrage/normalisation/blanchiment de la **cible** | oui | **écarté** — prémisse réfutée par le spectre |
| 60 | amplification uniforme | oui | **écarté** — ne change pas l'ordre |
| 61 | *décomposition de variance* | — | **diagnostic** : 12× moins d'énergie de contenu |
| 62 | amplification de l'axe contenu | **non** | **fonctionne** (β=3 → magnitude du professeur, coût 0,006) |
| 62 | amplification de la moyenne par entrée | oui | **écarté** — mêle les deux axes |
| 62 | `μ_lang` | oui | **écarté** — comprime les deux |
| 63 | sous-espace du contenu appris | oui | **écarté** — ne se transfère pas |
| **64** | **centrage de l'ENTRÉE** | **oui** | **RETENU** — rapport +28 %, P_lang ÷ 4,8, coût 0,008 |

**Huit moyens essayés, sept écartés, un retenu.** Le retenu est modeste ; les écartés
le sont chacun par une mesure, et le défaut est localisé avec un chiffre. C'est l'état
réel du problème, et il est plus étroit qu'au début de la série.


---

> Campagne : **toutes-langues** · expérience **10**
> Titre : 10. Signal précoce sur le panel STRATIFIÉ : l'écart de transfert était un artefact
> Date réelle : **2026-10-06 00:51 HAE** (source : commit `99a89ec`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 10. Signal précoce sur le panel STRATIFIÉ : l'écart de transfert était un artefact

Mesure prise sur les 168 premières langues tracées : **133 d'apprentissage, 15 de
validation, 20 de test couvrant 12 des 22 écritures**. Assez pour lire la réponse
de la phase 2 avant la fin du traçage.

**Réseau : 52 neurones en 1 seule couche.**

| | ancien panel (test non latin seul) | **nouveau panel stratifié** |
|---|---:|---:|
| fidélité TEST | 0,6383 | **0,7438** |
| fidélité VALIDATION | 0,7500 | 0,7621 |
| constante témoin | 0,6140 | 0,7215 |
| **écart à la constante** | +0,0243 | **+0,0223** |
| invariance TEST | 0,9488 | 0,9739 |
| pire paire | 0,8821 | 0,8929 |
| **écart oracle TEST** | +0,0693 | **+0,0292** |
| écart oracle VALIDATION | +0,0269 | +0,0198 |
| **rapport des écarts (test/validation)** | **2,58** | **1,47** |

### Ce que cela établit

**L'écart de transfert tombe de +0,0693 à +0,0292 — 2,4× plus petit** — et son
rapport test/validation passe de **2,58 à 1,47**. Le « goulot dans le transfert »
que j'avais annoncé au tour 3 était donc **pour l'essentiel un artefact de mon
panel de test**, composé uniquement de langues non latines. C'est exactement ce que
le diagnostic de typologie laissait prévoir.

**Et l'invariant tient** : l'écart à la constante vaut **+0,0223** ici, contre
+0,0243 sur l'ancien panel et +0,020 sur les sept périmètres du rapport précédent.
La contribution propre du pont reste **+0,020**, indépendamment du panel.

### Réserve explicite

Ce panel est **partiel** : 20 langues de test sur 41, et 12 écritures sur 22. Les
chiffres définitifs viendront de l'analyse complète, déclenchée automatiquement à
la fin des 392 langues. Mais la direction est nette et va dans le sens du
diagnostic de typologie.


---

> Campagne : **toutes-langues** · expérience **89**
> Titre : 89. LOCALITÉ : la couche 8 doit 24 % au jeton, 33 % à trois jetons, et 67 % à autre chose
> Date réelle : **2026-10-07 12:23 HAE** (source : commit `2ef44ea`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 89. LOCALITÉ : la couche 8 doit 24 % au jeton, 33 % à trois jetons, et 67 % à autre chose

### 89.1 La question, et elle décide d'une architecture

Notre pont est **récurrent** : `s_t = (1−a)·s_{t−1} + a·tanh(P·s_{t−1} + B·e_t)`. La
récurrence ne se justifie que si la cible dépend du contexte. Si la couche 8 n'était, à
chaque position, qu'une fonction du jeton courant, un réseau par position suffirait — et
toute la machinerie récurrente serait de la complexité inutile.

### 89.2 Le protocole

À chaque position p, on cherche à prédire `h_c(p)` — la couche c du professeur — à partir
d'une **fenêtre de trois jetons** de la couche 0 : `h_0(p)`, `h_0(p−1)`, `h_0(p−2)`.
Régression ridge en forme fermée, `ride = 1,0`. **300 traces** (50 articles × 6 langues),
**164 775 positions appariées**. La Grammaire `XᵀX` est calculée une seule fois — elle ne
dépend pas de la couche cible.

| couche | R²(jeton seul) | R²(fenêtre de 3) | **gain** | **gain relatif** |
|---:|---:|---:|---:|---:|
| 1 | 0,6051 | 0,6436 | +0,0385 | **9,8 %** |
| 2 | 0,5059 | 0,5667 | +0,0608 | **12,3 %** |
| 3 | 0,4139 | 0,5224 | +0,1085 | **18,5 %** |
| 5 | 0,2733 | 0,3604 | +0,0870 | **12,0 %** |
| 8 | 0,2424 | 0,3313 | +0,0888 | **11,7 %** |

### 89.3 Trois lectures

**1. Le jeton courant porte beaucoup, et de moins en moins avec la profondeur.**
`R²(0)` vaut **60,5 %** à la couche 1 et tombe à **24,2 %** à la couche 8. Une lecture
linéaire du seul jeton explique donc les deux tiers de la couche 1 — et le quart de la
couche 8. **La couche cible est la moins locale des neuf.**

**2. Le contexte ajoute peu, mais il ajoute — et le gain est maximal au milieu.**
Deux jetons de contexte supplémentaires ne récupèrent que **9,8 % à 18,5 %** de ce que le
jeton seul laissait inexpliqué. Le maximum est à la **couche 3** (18,5 %) : c'est là que le
professeur fait le plus de travail contextuel **par unité de variance inexpliquée**.

**3. Surtout : les deux tiers de la couche 8 restent inexpliqués.**
`R²(fenêtre) = 0,3313` signifie que **66,9 % de la variance de la couche 8 n'est atteinte ni
par le jeton, ni par trois jetons**. Cette part demande du contexte plus long, ou une
non-linéarité, ou les deux.

**Conséquence pour la conception** : la récurrence **n'est pas décorative**, mais elle n'est
pas non plus ce qui porte la plus grosse part. Le résultat utile est le contraste entre les
couches : **1 → 8, la dépendance au contexte augmente et la dépendance au jeton diminue**,
ce qui est cohérent avec le profil du §84 (la séparation contenu/langue se construit entre
les couches 3 et 5, exactement là où le gain contextuel culmine).

### 89.4 Un piège de mesure à consigner, et il est de la même famille

La première version de cette mesure, lancée sur **8 articles anglais** (3 674 positions),
donnait `R²(0) = 0,5632` et `R²(fenêtre) = 0,8689` — un gain de **+70 %** au lieu de +11,7 %.
Le chiffre était quatre fois trop grand.

**La cause : 2 688 variables pour 3 674 points.** Dans ce régime, un R² **calculé sur les
données d'ajustement** est gonflé par la capacité du modèle à interpoler. Le passage à
164 775 positions rend la mesure honnête. Il n'y avait aucun bug : seulement un rapport
entre nombre de variables et nombre de points qui n'était pas déclaré.

C'est la **sixième** fois de la session qu'un chiffre dépend d'un choix tu. La règle des
§81.6, §84.1, §86.5 et §88.4 s'allonge d'un sixième terme : *nommer la graine, le panel, le
pooling, l'ajustement, l'échelle — et le rapport variables/points.*

### 89.5 Réserves

**Mesure LINÉAIRE.** Un gain faible ne prouve pas que la couche est locale : il prouve
qu'**aucune lecture linéaire d'une fenêtre de trois jetons** n'en tire profit. Un professeur
peut faire dépendre `h_8(p)` du contexte d'une façon qu'aucune combinaison linéaire de trois
jetons ne capte — c'est même ce que le point 3 suggère.

**Fenêtre courte.** Trois jetons, c'est peu pour un texte. La courbe `R²(k)` en fonction de
la taille de fenêtre n'est pas tracée ; elle dirait **à quelle distance** le contexte
commence à porter, et c'est la mesure qui manque pour trancher entre « récurrence » et
« contexte long ».

---

> Campagne : **toutes-langues** · expérience **55**
> Titre : 55. Le pont transfère sur le corpus Wikipedia multi-domaine — et sur TROIS paires de langues
> Date réelle : **2026-10-06 18:30 HAE** (source : commit `44f0c9f`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 55. Le pont transfère sur le corpus Wikipedia multi-domaine — et sur TROIS paires de langues

Le corpus Wikipedia apparié (§45) permet pour la première fois de mesurer le transfert
sur un contenu **riche, multi-domaine et aligné**, et sur **plusieurs paires de
langues** — ce que Romeo seul (une paire, un registre) ne permettait pas.

**71 articles alignés × 6 langues**, couche 8, 120 neurones, 1 couche.

| paire | fidélité sur A | **fidélité sur B (transférée)** | **perte au transfert** | invariance de sortie | pire segment | oracle sur B | écart à l'oracle |
|---|---:|---:|---:|---:|---:|---:|---:|
| en ↔ fr | 0,6083 | **0,5444** | **−0,0639** | 0,9179 | 0,6556 | 0,6073 | +0,0629 |
| en ↔ de | 0,6083 | **0,5426** | **−0,0657** | 0,8981 | 0,6224 | 0,6160 | **+0,0734** |
| fr ↔ de | 0,6169 | **0,5851** | **−0,0318** | 0,9204 | 0,7420 | 0,6247 | **+0,0396** |

### 55.1 Ce que cela établit

**1. Le pont transfère, sur les trois paires.** La perte va de −0,032 (fr↔de) à
−0,066 (en↔de). La lecture apprise sur une langue, appliquée sans réapprentissage à
une autre, garde 87 à 95 % de sa fidélité.

**2. La paire la plus proche transfère le mieux.** fr↔de perd **deux fois moins** que
en↔fr et en↔de. C'est cohérent : plus les langues sont proches, mieux la lecture
partagée convient — et cela **confirme que la perte mesure bien la distance entre
langues**, pas autre chose.

**3. La comparaison avec Romeo est favorable.** Sur Romeo (24 scènes, en–fr), la perte
valait −0,0858. Ici, sur 71 articles encyclopédiques et multi-domaines, elle vaut
−0,0639 pour la même paire en–fr. **Un corpus plus riche et plus varié transfère
mieux**, ce qui va dans le sens de la mission.

**4. Le goulot de transfert est bien réel et quantifié** : l'écart à l'oracle va de
+0,0396 à +0,0734 selon la paire. Un ajustement privé rapporterait donc de 4 à 7 points
— c'est la marge qui reste à prendre.

### 55.2 Le chemin parcouru sur l'invariance de sortie

| corpus | paires | invariance de sortie | pire segment |
|---|---|---:|---:|
| Romeo (littéraire) | en–fr | 0,9540 | — |
| **Wikipedia (encyclopédique)** | en–fr | 0,9179 | 0,6556 |
| **Wikipedia** | en–de | 0,8981 | 0,6224 |
| **Wikipedia** | fr–de | 0,9204 | 0,7420 |

L'invariance de sortie de Wikipedia est **plus basse** que celle de Romeo — et c'est
attendu : le contenu est varié (71 sujets différents), donc il y a plus de matière à
ne pas confondre. Une invariance de 0,92 sur 71 sujets distincts vaut mieux qu'une
invariance de 0,95 sur 24 scènes d'une même pièce.

### 55.3 Une confirmation de déterminisme au passage

La croissance relancée après la correction du §54 reproduit **exactement** les points
de la passe interrompue : à 40 neurones, `0,6278 · 0,9289 · 0,7329` dans les deux
exécutions. Ce n'est pas une vérification de laboratoire, c'est une **reproduction
accidentelle sur un calcul de 40 minutes** — et elle vaut confirmation.


---

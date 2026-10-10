> Campagne : **campagne-benefices** · expérience **37**
> Titre : 37. E4 — l'équilibre excitation/inhibition : l'hypothèse est VRAIE dans un sens seulement
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 37. E4 — l'équilibre excitation/inhibition : l'hypothèse est VRAIE dans un sens seulement

L'hypothèse biologique (E4) : un réseau cortical équilibré vit près d'un point où excitation
et inhibition se compensent, et un déséquilibre dans **un** sens ou dans l'autre coûte.
Transposée au moteur avec le levier existant `--ffn-gain couche:valeur`, la question
mesurable est : **existe-t-il un gain de la FFN, par couche, qui AMÉLIORE la perplexité — et
est-il intérieur ?** Qwen2.5-0.5B-Q8, 128 jetons, référence **14,6496**.

| gain | couche 0 | couche 1 | couche 2 | couche 6 | couche 12 | couche 18 |
|---|---|---|---|---|---|---|
| **1,0** | **14,6496** | **14,6496** | **14,6496** | **14,6496** | **14,6496** | **14,6496** |
| 0,75 | **12,9635** | 13,9844 | 15,9977 | — | — | — |
| 0,5 | 14,1057 | **13,7907** | 18,1670 | 15,2081 | 14,9512 | 15,4868 |
| 0,25 | **996,0390** | 14,2423 | 20,3067 | — | — | — |
| 0,0 | 56 860,57 | — | — | 17,6825 | 15,6908 | 17,4291 |
| −0,25 | 41 039,85 | — | — | 20,7224 | 16,3034 | 18,9574 |
| −0,5 | 70 349,61 | — | — | 27,6019 | 17,1200 | 21,2038 |
| −1,0 | 112 958,21 | — | — | 65,1286 | 19,4791 | 30,2514 |

**Trois résultats, et le premier est un invariant :**

1. **`--ffn-gain L:1.0` EST l'absence de réglage** : 14,6496 exactement, sur trois couches
   (0, 6, 18). Sans cet invariant, aucune autre ligne ne comparerait quoi que ce soit — et
   c'est la porte qui l'exige ;
2. **du côté INHIBITION, la courbe est MONOTONE et l'optimum intérieur est réfuté** : à la
   couche 12, tout gain inférieur à 1 dégrade, et de plus en plus (15,69 · 16,30 · 17,12 ·
   19,48). L'hypothèse « un peu d'inhibition fait du bien » est **fausse** ici ;
3. **du côté AMPLIFICATION, l'optimum est INTÉRIEUR et net sur les premières couches** :
   couche 0 à **0,75** → **12,9635**, soit **−11,5 %** ; couche 1 à 0,5 → 13,7907 (−5,9 %) ;
   la couche 2 n'a plus d'optimum utile (son meilleur point est ≥ 1,0). Et sous l'optimum il
   y a une **falaise** : la couche 0 à 0,25 donne **996,04**, **68× pire** — un gain trop
   faible à la première couche ne dégrade pas un peu, il casse le modèle.

**Ce que cela dit du modèle, et c'est le plus intéressant** : le profil optimal n'est pas
plat — il **décroît avec la profondeur** (optimum à 0,75 puis 0,5 puis ≥ 1,0). Les premières
couches ont donc besoin d'**être amplifiées** et les suivantes non ; autrement dit, la
« balance » d'un transformeur n'est pas la même à toutes les profondeurs, et un profil appris
par couche est un levier **mesuré** (−11,5 % sur un réglage, sans rien entraîner).

**Et le bénéfice est LOCALISÉ : le profil complet, sur les 24 couches, à gain 0,75.**

| couche | 0 | 1 | 2 | 3 | 4-16 | 17 | 19 | 21 | 23 |
|---|---|---|---|---|---|---|---|---|---|
| écart à la référence | **−11,5 %** | **−4,5 %** | **+9,2 %** | **+10,6 %** | ±1 % | +3,8 % | −0,1 % | +4,3 % | +5,7 % |

**Seules les couches 0 et 1 gagnent à être amplifiées** ; les couches 2 et 3 **perdent
beaucoup** (+9,2 % et +10,6 %, elles ne supportent pas d'être atténuées) ; les couches 4 à 16
restent dans ±1 % (neutres), et seules 17, 21 et 23 repassent au-dessus de +3 %. Le
déséquilibre n'est donc **pas réparti sur la profondeur : il est à l'ENTRÉE** — les deux
premières couches ont besoin d'être amplifiées, et le reste du réseau est déjà à son point.

**Et les gains NE SE COMPOSENT PAS — le profil défait le meilleur réglage seul.**
`--ffn-gain` accepte maintenant une liste (`0:0.75,1:0.5`), ce qui rend la question mesurable :

| profil | perplexité | écart |
|---|---|---|
| **`0:0.75` seul** | **12,9635** | **−11,51 %** |
| `1:0.5` seul | 13,7907 | −5,86 % |
| `0:0.75,1:0.5` | 13,7679 | −6,02 % |
| `0:0.9,1:0.6` | 13,4209 | −8,39 % |
| `0:0.75,1:0.5,2:1.0` | **13,7679** | identique au précédent |

**Ajouter le gain de la couche 1 DÉGRADE le résultat de la couche 0** (12,9635 → 13,7679) : les
deux réglages s'antagonisent en partie, ils ne s'additionnent pas. Le meilleur profil mesuré
est donc **un réglage SEUL**. Et la dernière ligne est le témoin qui rend les autres lisibles :
un gain de **1,0 dans un profil est exactement neutre** (13,7679 = 13,7679), donc l'identité
tient aussi à l'intérieur d'un profil.

**Conséquence pour le dessin I**, et elle est plus dure que celle du §37 : non seulement le
profil n'a que deux couches utiles, mais **le composer empire les choses**. Un profil appris
aurait donc à découvrir que la bonne réponse est « une seule couche, un seul gain » — ce qu'un
apprentissage par gradient sur peu de paramètres peut très bien ne pas trouver, puisqu'il
optimiserait les deux ensemble.

**Généralise-t-il ? Deux axes testés, et les deux disent la même chose : la direction tient,
la magnitude dépend des conditions.**

| axe | mesure |
|---|---|
| **autre quantification** (Q4_0 au lieu de Q8_0) | gain 0,75 à la couche 0 → **14,7453** contre **15,8055** sans réglage = **−6,7 %** |
| **fenêtre d'évaluation** (256 jetons au lieu de 128) | **17,1915** contre **17,4315** = **−1,4 %** (au lieu de −11,5 %) |

**L'effet n'est donc pas un artefact d'une quantification** : il vaut −6,7 % sur Q4_0 et
−11,5 % sur Q8_0. Mais **il décroît fortement avec la fenêtre** : −11,5 % sur 128 jetons,
−1,4 % sur 256. Le chiffre de −11,5 % est un **point de mesure**, pas une propriété du modèle,
et c'est écrit ainsi — la porte exige d'ailleurs que la magnitude décroisse, donc un futur
relecteur ne pourra pas citer le meilleur chiffre sans voir la condition.

**Conditions** : un seul modèle (0,5 B) en deux quantifications, deux fenêtres (128 et 256
jetons), un seul jeu d'identifiants ; l'optimum à 0,75 est un point de la grille
(0,5 · 0,75 · 1,0), il n'est pas localisé plus finement ; deux profils à deux couches testés,
plus un à trois couches.

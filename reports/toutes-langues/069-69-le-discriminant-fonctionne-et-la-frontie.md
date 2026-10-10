> Campagne : **toutes-langues** · expérience **69**
> Titre : 69. Le discriminant fonctionne — et la frontière est maintenant tracée
> Date réelle : **2026-10-06 23:38 HAE** (source : commit `3b50b1a`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 69. Le discriminant fonctionne — et la frontière est maintenant tracée

### 69.1 L'outil qui vise le rapport par les directions

Le §67 avait établi qu'aucune amplitude ne peut corriger le rapport ; le §68, que la
covariance totale ne le détermine pas. Restait l'outil qui vise **exactement** la bonne
quantité : les directions qui **maximisent le rapport** entre l'énergie de contenu et
l'énergie de langue, calculées sur les **moyennes par entrée** de l'apprentissage —
l'analyse discriminante linéaire :

```
C_cont · v = λ · C_lang · v
```

On garde les `r` directions de plus grand λ et on y projette la sortie. **Linéaire,
forme fermée, sans rétropropagation, déployable** — le projecteur est une matrice fixe.

Valeurs propres obtenues : **6286,5 · 1651,2 · 931,8 · 804,5 · 674,6 · 575,6 · 545,6 ·
480,9** — la structure est fortement hiérarchisée, ce qui est bon signe.

### 69.2 Le rapport, et c'est le meilleur de toute la série

| rang | fid TEST | P_lang | P_cont | **RAPPORT** |
|---:|---:|---:|---:|---:|
| 0 | 0,4703 | 42,4 | 82,1 | 1,934 |
| **2** | 0,4341 | 4,3 | 30,2 | **6,961** |
| 5 | 0,4433 | 9,9 | 41,6 | 4,216 |
| 20 | 0,4575 | 17,4 | 57,9 | 3,326 |
| 40 | 0,4620 | 23,0 | 64,4 | 2,800 |
| | | | **professeur 4 356** | **professeur 10,912** |

**Le rapport atteint 6,961 — plus du double du meilleur précédent (3,064), et 64 % de
la cible.** Les directions apprises **se transfèrent** aux langues inconnues.

### 69.3 Mais les énergies sont écrasées — et c'est le critère qui compte

Projeter sur 2 directions de 896 laisse peu d'énergie : `P_cont` = 30,2 contre 4 356
pour le professeur. Le rapport est élevé, mais **par les deux côtés à la fois**. Or le
§62.3 a établi le bon critère : **`P_cont` proche du professeur ET `P_lang` qui ne le
dépasse pas.**

Comme le rapport est invariant d'échelle (§67), on peut **amplifier** sans le changer.
Question : à quel coût en fidélité ?

| rang | α | fid TEST | P_lang | P_cont | critère |
|---:|---:|---:|---:|---:|---|
| 20 | 1,0 | 0,4575 | 17,4 | 57,9 | — |
| **20** | **4,2** | **0,3536** | **300,7** | **1 000** | **✓ P_lang ≤ 399** |
| 2 | 5,8 | 0,3321 | 143,6 | 1 000 | ✓ |
| 2 | **12,0** | **0,2385** | **625,8** | **4 356** | **✗ P_lang > 399** |

**Pour amener `P_cont` à la magnitude du professeur (4 356), la fidélité tombe à
0,24-0,27** — de 0,47. Et `P_lang` dépasse alors 399 dans les trois cas.

**Le meilleur compromis** : rang 20, α = 4,2 → `P_lang` **300,7** (sous le professeur),
`P_cont` **1 000** (4,4× sous le professeur), fidélité **0,3536** — soit un coût de
**0,117**.

### 69.4 La réponse à la question ouverte au §57

| question | réponse |
|---|---|
| La structure contenu/langue du professeur est-elle **accessible** ? | **oui, en partie** — rapport 6,96 sur 10,91, soit 64 % |
| Par une transformation **linéaire, fermée, sans rétropropagation** ? | **oui** — analyse discriminante, matrice fixe, déployable |
| **Sans payer** ? | **non** — 0,117 de fidélité pour `P_cont` = 1 000, 0,23 pour la magnitude complète |
| Le **ratio** du professeur est-il atteignable ? | **non par cette voie** — 6,96 est le maximum obtenu |

**La frontière est donc tracée** : fidélité contre structure contenu/langue. Le pont ne
peut pas avoir les deux, et il ne peut pas atteindre la structure complète du
professeur par une lecture linéaire — du moins pas avec les caractéristiques actuelles.

### 69.5 Ce que cela dit de la suite, et ce n'est plus une conjecture

Puisque **toutes** les transformations linéaires essayées butent sur la même frontière —
neuf moyens, sept écartés, deux retenus qui donnent 3,06, et le discriminant qui monte à
6,96 en payant 0,12 à 0,23 de fidélité — **le facteur limitant n'est plus l'objectif ni
la lecture : ce sont les CARACTÉRISTIQUES.**

Le §58 avait montré qu'une lecture linéaire *atteint* la cible, mais par un objectif non
convexe et instable. Le §69 montre que la voie convexe et déployable y arrive à 64 % et
coûte cher. **Les deux résultats ensemble désignent la même conclusion** : les états du
réservoir contiennent la structure, mais ils la contiennent **mêlée** à la langue d'une
façon qu'aucune transformation linéaire ne démêle sans perdre le contenu.

**La prochaine étape n'est donc pas un dixième objectif, c'est une caractéristique
différente** — un état dont la structure de langue soit séparable par construction, et
non par post-traitement.


---

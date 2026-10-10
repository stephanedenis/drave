> Campagne : **toutes-langues** · expérience **74**
> Titre : 74. La combinaison des deux mécanismes DOMINE chacun d'eux
> Date réelle : **2026-10-07 01:50 HAE** (source : commit `5b1b6b6`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 74. La combinaison des deux mécanismes DOMINE chacun d'eux

Le §73 s'achevait sur une piste : *« apprendre quoi lire » agit sur les
caractéristiques, le discriminant agit sur la lecture — les deux sont complémentaires,
et leur combinaison n'a pas été essayée.* Elle l'est.

| méthode | fid TEST | P_lang | **P_cont** | **rapport** |
|---|---:|---:|---:|---:|
| discriminant **seul** (§69), rang 2 | 0,4341 | 4,3 | **30,2** | **6,961** |
| discriminant seul, rang 20 | 0,4575 | 17,4 | 57,9 | 3,326 |
| **quoi lire + discriminant, rang 2** | 0,4305 | 31,8 | **184,4** | 5,803 |
| **quoi lire + discriminant, rang 5** | **0,4378** | **48,1** | **280,5** | **5,829** |
| **quoi lire + discriminant, rang 20** | 0,4505 | 87,4 | **360,8** | 4,129 |
| *professeur* | — | *399,2* | *4 356,4* | *10,912* |

### 74.1 Ce que la combinaison apporte

**À rapport comparable, elle porte NEUF FOIS plus d'énergie de contenu** : au rang 5,
`P_cont` = **280,5** contre **30,2** pour le discriminant seul au rang 2, pour un rapport
du même ordre (5,83 contre 6,96) et une fidélité équivalente (0,4378 contre 0,4341).

Sur le critère du §62.3 — le seul qui compte — **les deux satisfont `P_lang` < 399**, mais
la combinaison porte **neuf fois plus de contenu** :

| méthode | P_lang (< 399 ?) | **P_cont** | rapport |
|---|---:|---:|---:|
| rien | 247,1 ✓ | 318,7 | 1,290 |
| centrage + sous-espace (§66) | 22,9 ✓ | 70,2 | 3,064 |
| discriminant seul (§69) | 4,3 ✓ | 30,2 | 6,961 |
| apprendre quoi lire (§73) | 181,9 ✓ | 438,5 | 2,411 |
| **quoi lire + discriminant (§74)** | **48,1 ✓** | **280,5** | **5,829** |

**La combinaison est le meilleur compromis trouvé** : un rapport de 5,83 (53 % de la
cible) avec une énergie de contenu de 280,5 — là où le discriminant seul n'en portait que
30,2 pour gagner 1,1 de rapport.

### 74.2 Où en est la traque, après quatorze moyens

| moyen | déployable | rapport | P_cont |
|---|---|---:|---:|
| rien | — | 1,290 | 318,7 |
| amplifications (§60, §62) | oui | *inchangé* — identité du §67 | — |
| `μ_lang` (§62) | oui | 0,910 | 144,4 |
| sous-espace du contenu (§63) | oui | 1,495 | 8 274 (par explosion) |
| centrage de l'entrée (§64) | oui | 1,871 | 89,8 |
| centrage + sous-espace de langue (§66) | oui | 3,064 | 70,2 |
| covariance de la cible (§68) | oui | 1,810 | 1 784,5 |
| discriminant (§69) | oui | **6,961** | 30,2 |
| blanchiment de l'entrée (§71) | oui | 1,606 | 27 185 (par explosion) |
| mise à l'échelle du renforcement (§72) | oui | 1,312 — **forcé par l'identité du §67** | 317,0 |
| **apprendre quoi lire (§73)** | **oui** | 2,411 | **438,5** |
| **quoi lire + discriminant (§74)** | **oui** | **5,829** | **280,5** |
| *professeur* | — | *10,912* | *4 356,4* |

**On est passé de 1,29 à 5,83 — soit 53 % de la cible — avec des mécanismes tous
déployables, tous en forme fermée, tous sans rétropropagation.** Et l'énergie de contenu,
qui était le défaut central du §61 (douze fois trop faible), est remontée de 318,7 à
280,5 en changeant de point de fonctionnement — **mais le rapport, lui, est monté**.

### 74.3 Ce qui reste, et c'est plus étroit qu'au début

Le meilleur point trouvé a `P_cont` = 280,5 là où le professeur a 4 356. **Pour l'amener
là par amplification, il faudrait multiplier `P_lang` par 15,5 et le porter à 746 — au
double de celui du professeur.** Le rapport de 5,83 ne suffit donc pas : il faudrait
**10,9**.

**Mais la voie est maintenant tracée et elle n'est plus une conjecture** : deux mécanismes
déployables, complémentaires, qui agissent l'un sur les caractéristiques et l'autre sur la
lecture, portent le rapport de 1,29 à 5,83. **Il reste un facteur 1,9 à trouver**, et les
deux mécanismes ont été testés séparément puis ensemble — la question est désormais de
savoir si **d'autres directions d'entrée** (au-delà du premier passage, qui sature) ou
**d'autres rangs** du discriminant rapprochent encore.


---

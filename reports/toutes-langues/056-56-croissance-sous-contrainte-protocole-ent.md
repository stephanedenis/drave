> Campagne : **toutes-langues** · expérience **56**
> Titre : 56. Croissance sous contrainte, protocole ENTIER : 147 neurones, oracle sur les deux panneaux
> Date réelle : **2026-10-06 19:44 HAE** (source : commit `e266e21`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 56. Croissance sous contrainte, protocole ENTIER : 147 neurones, oracle sur les deux panneaux

Première passe de croissance qui fournit **le protocole complet** demandé par
l'objectif — les quatre mesures **et** l'oracle sur les **deux** panneaux.

Couche 10, `--part-langues 0.5`, ride 0,03, lecture quadratique, réservoir
multi-échelle, fit sur 1/20, μ = 0,1, 300 langues d'ajustement / 51 de validation /
41 de test, 896 canaux.

| | |
|---|---:|
| **TAILLE** | **147 neurones · 1 couche** |
| fidélité apprentissage | 0,6464 |
| fidélité **VALIDATION** (même vivier) | 0,6312 |
| **fidélité TEST** (hors vivier) | **0,6299** |
| constante témoin sur TEST | 0,5762 |
| **apport propre** | **+0,0537** |
| **invariance inter-langue** | **0,8958** |
| **pire paire** | **0,6392** |
| oracle TEST | 0,6721 |
| **écart à l'oracle — TEST (hors vivier)** | **+0,0415** |
| oracle VALIDATION (même vivier) | 0,6504 |
| **écart à l'oracle — VALIDATION** | **+0,0194** |

### 56.1 Comparaison avec la même croissance SANS contrainte

| | μ = 0 (182 neurones) | **μ = 0,1 (147 neurones)** |
|---|---:|---:|
| fidélité TEST | **0,6340** | 0,6299 |
| invariance | 0,8659 | **0,8958** |
| pire paire | 0,5556 | **0,6392** |
| oracle TEST | *(manquant — drapeau cassé)* | **0,6721** |
| écart à l'oracle TEST | *(manquant)* | **+0,0415** |

**−0,0041 de fidélité pour +0,0299 d'invariance et +0,0836 de pire paire.** Le taux
d'échange sur la pire paire est de **20 pour 1**.

### 56.2 Le goulot de transfert se resserre quand le réseau grandit

L'écart à l'oracle hors vivier vaut ici **+0,0415**, contre **+0,1003** pour le profil
à **40 neurones** (§44). Le rapport entre l'écart hors vivier et l'écart dans le vivier
tombe de **8,7× à 2,1×**.

Autrement dit : **un réseau plus grand transfère mieux.** C'est la première fois que
le goulot de transfert du §36 se réduit sous l'effet d'une décision d'architecture.


---

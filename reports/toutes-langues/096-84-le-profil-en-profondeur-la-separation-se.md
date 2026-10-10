> Campagne : **toutes-langues** · expérience **84**
> Titre : 84. LE PROFIL EN PROFONDEUR : la séparation se fait entre les couches 3 et 5
> Date réelle : **2026-10-07 11:08 HAE** (source : commit `207ef67`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 84. LE PROFIL EN PROFONDEUR : la séparation se fait entre les couches 3 et 5

50 articles × 6 langues, couches 0 à 8, moyenne sur les positions. Mêmes entrées pour toutes
les couches ; seule la couche lue change.

| couche | P_lang | P_cont | **RAPPORT** | vs couche 0 | dim. eff. |
|---:|---:|---:|---:|---:|---:|
| 0 | 4 401,9 | 1 120,0 | **0,254** | 1,00× | 14,2 |
| 1 | 10 220,7 | 2 079,1 | **0,203** | 0,80× | 16,1 |
| 2 | 10 760,1 | 2 509,7 | **0,233** | 0,92× | 18,3 |
| 3 | 2 000,7 | 853,8 | **0,427** | 1,68× | 22,3 |
| 4 | 5 644,1 | 3 941,6 | **0,698** | 2,74× | 32,5 |
| 5 | 3 312,2 | 5 464,3 | **1,650** | 6,48× | 37,5 |
| 6 | 7 386,3 | 12 821,4 | **1,736** | 6,82× | 37,5 |
| 7 | 3 475,6 | 5 817,8 | **1,674** | 6,58× | 34,6 |
| 8 | 2 515,7 | 4 449,6 | **1,769** | 6,95× | 35,5 |

**Deux lectures, et la seconde corrige la première.**

**1. Le saut est entre 3 et 5.** Le rapport passe de 0,233 (couche 2) à 1,650 (couche 5) :
×7 en trois couches. Les couches 0 à 2 sont *contre-productives* — le rapport y **baisse**
(0,254 → 0,203), la langue se renforce plus vite que le contenu.

**2. Mais le plateau de 5 à 8 est un artefact d'agrégat.** Sur l'agrégat 6 langues, 5→8
n'ajoute que +0,119. Or, paire par paire, sur les mêmes 50 articles :

| paire | couche 5 | couche 8 | gain |
|---|---:|---:|---:|
| de–en (pire) | 1,588 | 1,559 | −0,029 |
| es–it | 7,514 | 14,064 | **+6,55** |
| it–pt | 7,635 | 13,614 | **+5,98** |
| es–pt (meilleure) | 23,098 | 48,269 | **+25,17** |

**Les paires proches continuent de se séparer jusqu'à la couche 8 — elles doublent.** Ce que
le plateau agrégé cache, c'est que la paire difficile (de–en) est déjà saturée à la couche 5
et que l'agrégat, dominé par elle, ne bouge plus. **La dimension effective, elle, sature
vraiment à la couche 5** (37,5 puis 37,5 · 34,6 · 35,5) : au-delà, le professeur réorganise
sans ajouter de directions.

**Conséquence pour notre conception** : la séparation contenu/langue que nous cherchons à
émuler est **acquise dès la couche 5**, et la couche 8 n'apporte un gain que sur les paires
faciles. Émuler la couche 5 au lieu de la couche 8 ne coûterait donc rien sur l'axe
difficile — c'est une piste de conception, pas une cible à reproduire.

### 84.1 Le pooling : deux sondes, deux mondes

Mêmes traces, même corpus, même couche. Seule change la façon de réduire les positions d'une
entrée à un vecteur :

| pooling | couche 0 | couche 8 |
|---|---:|---:|
| **moyenne sur les positions** (le pooling du §70) | 0,254 | 1,769 |
| **dernière position** | 8,044 | 6,275 |

**À la dernière position, le rapport est de 8,0 en couche 0 et 6,3 en couche 8** : la
dernière position d'un article est un résumé stéréotypé où la langue domine moins, et le
profil est *plat*. À la moyenne, il est de 0,25 et 1,77, et le profil *monte*. **Les deux
sondes ne racontent pas la même histoire, et c'est la moyenne qui est comparable au §70 et à
notre pont** — parce que notre lecture, elle aussi, voit l'entrée entière.

C'est la deuxième fois dans cette session qu'un chiffre se révèle être un artefact de
réduction (le §81 avait trouvé l'artefact de graine). La règle s'étend : **avant d'écrire un
chiffre, nommer la graine, le panel, et le pooling.**

---

> Campagne : **toutes-langues** · expérience **30**
> Titre : 30. Couche 8 contre couche 10, au niveau des DIX unités alignées
> Date réelle : **2026-10-06 09:20 HAE** (source : commit `b2e5631`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 30. Couche 8 contre couche 10, au niveau des DIX unités alignées

Le traçage par unité écrit les couches 0, 8 et 10. On peut donc comparer les deux
cibles sur **le même découpage et les mêmes langues** — 17 langues d'apprentissage,
230 unités de test, dix points de mesure alignés par langue au lieu d'un.

### 30.1 Les chiffres

| | couche 10 | couche 8 | écart |
|---|---:|---:|---:|
| canaux retenus | 151/896 | 121/896 | — |
| neurones (naissance libre + attrition) | 49 | 120 | — |
| **invariance du PROFESSEUR** | 0,6471 | **0,6998** | **+0,0527** |
| fidélité VALIDATION | 0,7649 | **0,8138** | +0,0489 |
| **fidélité TEST** | 0,7087 | **0,7582** | **+0,0495** |
| **oracle TEST** | 0,7439 | **0,8012** | **+0,0573** |
| notre invariance | **0,9701** | 0,9401 | −0,0300 |
| notre pire paire | **0,8702** | 0,7778 | −0,0924 |

**La couche 8 gagne sur tout ce qui mesure la cible** : le professeur y est plus
interlingue (+0,0527), et notre fidélité y est meilleure (+0,0495), y compris
mesurée contre l'oracle (+0,0573 — donc ce n'est pas un effet de lecture).

### 30.2 Deux réserves, et elles comptent

**Les réseaux n'ont pas la même taille** (49 neurones contre 120). La naissance
libre et l'attrition ont divergé, donc une partie de l'écart peut être de la
capacité et non de la couche. Ce n'est pas corrigé ici.

**Notre invariance BAISSE à la couche 8** (0,9401 contre 0,9701), alors que celle du
professeur MONTE. Nous sommes donc **plus invariants que le professeur**, et l'écart
se creuse à la couche 10 : 0,9701 pour nous contre 0,6471 pour lui. Un modèle qui
lisse plus que sa cible peut être en train de perdre du contenu, pas d'acquérir de
l'invariance. La fidélité (0,7582) dit que ce n'est pas un effondrement — mais le
point mérite d'être surveillé, et il n'est pas résolu.

### 30.3 Le décrochage d'une seule langue

À la couche 10, la pire paire mélangeait `csw`, `amh`, `acu`, `bum`. **À la couche 8,
`amh` apparaît dans 8 des 10 unités.** Ce n'est plus un bruit réparti mais une
langue qui décroche, et c'est un point d'enquête précis — pas encore instruit.

### 30.4 Une régression que j'ai introduite, et corrigée

En ajoutant la constante de temps par neurone (§28), j'ai étendu `nait`, `recalcule`
et `compacte` — mais **pas la recopie de généalogie de `tools/pont_parallele.py`**,
qui copiait `poids` sans copier `a_neur`. Résultat : le pont a planté sur **Romeo**
et sur **Wikipedia**, les deux sections entières, avec un `IndexError` obscur.

C'est exactement le risque que mon propre commentaire du §28 annonçait — « une
constante de temps qui ne suivrait pas le neurone changerait silencieusement la
dynamique » — et je ne l'ai pas vérifié ailleurs. Corrigé à deux endroits :

1. `pont_parallele.py` recopie désormais `a_neur`, avec un `assert` de cohérence ;
2. `recalcule` **refuse bruyamment** toute généalogie désynchronisée, au lieu de
   produire un calcul silencieux avec la mauvaise dynamique.

Les deux sections ont été relancées.


---

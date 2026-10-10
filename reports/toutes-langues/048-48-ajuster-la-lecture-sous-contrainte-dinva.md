> Campagne : **toutes-langues** · expérience **48**
> Titre : 48. Ajuster la lecture SOUS CONTRAINTE d'invariance : le levier existe, et il est bon marché
> Date réelle : **2026-10-06 16:11 HAE** (source : commit `5ad2f09`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 48. Ajuster la lecture SOUS CONTRAINTE d'invariance : le levier existe, et il est bon marché

### 48.1 Le principe, et pourquoi il reste en forme fermée

L'ajustement ordinaire minimise `‖XW − Y‖²` **seul**. Il ignore l'invariance
inter-langue — d'où la tension mesurée au §47. On ajoute donc à l'objectif la
**variance inter-langue de la sortie** :

```
P(W) = Σ_i n_i ‖m_i − m̄‖²        m_i = moyenne par langue de X_i·W
```

`P` est **quadratique en `W`** : `P(W) = tr(Wᵀ C W)` avec
`C = Σ_i n_i (M_i − M̄)ᵀ(M_i − M̄)`. L'objectif total reste quadratique et la solution
reste **en forme fermée** :

```
(XᵀX + μ·C_échelle + ride·I) W = Xᵀ(Y − mt)
```

**On ne change pas d'algorithme, on change d'objectif** — et la contrainte « aucune
rétropropagation » est respectée à la lettre.

### 48.2 Une première tentative FAUSSE, et ce qu'elle a appris

J'avais d'abord écrit la pénalité `μ·len(X)·C`. Mesuré :

| μ | fid TEST | invariance | pire paire |
|---:|---:|---:|---:|
| 0 | 0,6646 | 0,8740 | 0,4463 |
| 0,003 | 0,5982 | **0,9998** | **0,9986** |
| ≥ 0,01 | 0,5988 | **1,0000** | **1,0000** |

**Une falaise, pas un curseur.** L'invariance passe de 0,874 à 0,9998 dès le plus
petit μ non nul, et la fidélité tombe à 0,5988 — **sous le témoin constant** (0,6049
à la couche 8). Autrement dit : la sortie devenait la MÊME pour toutes les langues,
donc ne dépendait plus de l'entrée.

La cause est arithmétique : `len(X)·trace(C)` vaut **~80× `trace(XᵀX)`**, donc même
μ=0,003 écrasait le terme de données. Corrigé en normalisant `C` pour que **μ=1
signifie « pénalité de même échelle que l'ajustement »**.

### 48.3 Le vrai curseur

Couche 8, 40 neurones, 1 couche, lecture quadratique, multi-échelle, 300 langues
d'ajustement / 51 de validation / 41 de test, 896 canaux :

| μ | fid VAL | **fid TEST** | **invariance** | **pire paire** |
|---:|---:|---:|---:|---:|
| **0** | 0,6942 | **0,6646** | 0,8740 | 0,4463 |
| 0,001 | 0,6942 | 0,6646 | 0,8747 | 0,4489 |
| 0,003 | 0,6941 | 0,6644 | 0,8760 | 0,4540 |
| 0,01 | 0,6939 | 0,6639 | 0,8803 | 0,4713 |
| 0,03 | 0,6930 | 0,6624 | 0,8909 | 0,5152 |
| **0,1** | 0,6895 | **0,6564** | **0,9157** | **0,6224** |
| 0,3 | 0,6812 | 0,6429 | 0,9448 | 0,7543 |
| 1,0 | 0,6689 | **0,6242** | **0,9677** | **0,8600** |

**La prédiction est confirmée** : l'invariance monte, la fidélité baisse, et la
courbe est régulière sur trois ordres de grandeur de μ.

### 48.4 Le taux d'échange, et il est favorable

| de μ=0 à | gain d'invariance | gain de pire paire | coût de fidélité TEST |
|---|---:|---:|---:|
| μ=0,03 | +0,0169 | +0,0689 | **−0,0022** |
| **μ=0,1** | **+0,0417** | **+0,1761** | **−0,0082** |
| μ=0,3 | +0,0707 | +0,3080 | −0,0217 |
| μ=1,0 | +0,0937 | +0,4137 | −0,0404 |

**À μ = 0,1, on achète +0,042 d'invariance et +0,176 de pire paire pour 0,008 de
fidélité.** Le rapport est de **5 pour 1**, et sur la pire paire de **21 pour 1**.

C'est le premier levier de toute la session qui améliore **l'axe que la mission
cherche** sans coûter cher, et il ne demande ni neurone, ni couche, ni apprentissage
supplémentaire — seulement un terme de plus dans une équation qu'on résolvait déjà.

### 48.5 Ce que cela ne règle pas

À μ=0,1 notre invariance vaut 0,9157, contre **0,6836 pour le professeur**. Nous
restons **beaucoup plus invariants que notre propre cible**, et notre pire paire
(0,6224) reste très au-dessus de la sienne (0,0104). Le §41 n'est donc pas résolu : la
question « est-ce de l'invariance ou de l'appauvrissement ? » tient toujours, et elle
se tranchera sur un corpus où **le contenu diffère d'une langue à l'autre** — ce que
l'UDHR ne permet pas et que le corpus Wikipedia apparié (§45) permettra.

**μ = 0,1 est retenu comme point de fonctionnement par défaut** : c'est le point où le
gain d'invariance reste cinq fois son coût.


---

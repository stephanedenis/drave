# Qtrinet — éliminer la valeur par répétition d'adresse ?

Modèle mesuré : **qwen2** quantifié **Q4_0** (166 matrices 2-D).
Les niveaux sont lus *tels que stockés* (−8..+7), avant mise à l'échelle.

## 1. Distribution réelle des niveaux

- zéros : **12.9 %** des poids (densité 87.1 %)
- `E[|v|]` sur les non-nuls : **3.02**
- `E[popcount(|v|)]` : **1.39**

| \|v\| | Part des poids | Part des non-nuls |
|---|---|---|
| 1 | 23.72 % | 27.2 % |
| 2 | 19.54 % | 22.4 % |
| 3 | 14.84 % | 17.0 % |
| 4 | 10.53 % | 12.1 % |
| 5 | 7.06 % | 8.1 % |
| 6 | 4.54 % | 5.2 % |
| 7 | 3.84 % | 4.4 % |
| 8 | 3.05 % | 3.5 % |

## 2. Coût par poids non nul

| Stratégie | Bits stockés | Opérations |
|---|---|---|
| positionnel (4 bits) | 4,00 | 1,00 |
| **unaire (répétition d'adresse)** | **2.02** | **3.02** |
| plans binaires (popcount) | 1.39 | 1.39 |
| **hybride (unaire pour \|v\|=1, puis plans)** | **1.12** | **1.12** |

## 3. Seuil de bascule

L'unaire gagne si `E[|v|] − 1 < k`, c'est-à-dire `E[|v|] < k + 1` :

| Bits k | E[\|v\|] uniforme | Coût unaire | Coût positionnel | Gagnant |
|---|---|---|---|---|
| 1 | 0.5 | -0.5 | 1 | **unaire** |
| 2 | 1.5 | 0.5 | 2 | **unaire** |
| 3 | 3.5 | 2.5 | 3 | **unaire** |
| 4 | 7.5 | 6.5 | 4 | positionnel |
| 6 | 31.5 | 30.5 | 6 | positionnel |
| 8 | 127.5 | 126.5 | 8 | positionnel |

Sur ce modèle 4 bits réel : `E[|v|] = 3.02` → coût unaire 2.02 contre 4 bits → **unaire gagnant**.

## Verdict

**Sur un vrai modèle 4 bits, `E[|v|]` ne vaut que 3.02** — pas 7,5 comme
le suppose une distribution uniforme. La raison : l'échelle Q4_0 est fixée par
le maximum du bloc, donc la plupart des poids tombent sur les petits niveaux
(27 % des non-nuls valent ±1). **Le code 4 bits gaspille donc ses bits.**

Conséquence : l'idée de répétition **gagne** (2.63 b/poids contre 4,00 en dense), et sa forme hybride gagne encore plus (**1.85 b/poids, soit ×2.17**), sans aucune perte.

1. **L'idée est exacte** : répéter l'adresse v fois reproduit exactement la
   valeur, sans perte au-delà de la quantification d'origine. Le raisonnement
   est juste.
2. **Mais c'est de l'encodage unaire**, et l'unaire est exponentiellement plus
   coûteux que le positionnel : le coût est proportionnel à `v` au lieu de
   `log2(v)`. C'est la différence entre « ajouter v fois » et « multiplier par v ».
3. **Le seuil est net** : l'unaire gagne pour k ≤ 3 bits, perd à partir de 4.
   Sur ce modèle 4 bits réel (`E[|v|]=3.02`), il perd.
4. **Là où l'idée est optimale — et c'est important** : en **binaire** (k=1) et
   en **ternaire** (BitNet). Tous les non-nuls valent ±1, donc l'adresse *seule*
   porte la valeur : zéro bit de valeur, zéro répétition. C'est exactement ce
   que fait l'encodage « listes signées » déjà mesuré (0,39 b/poids).
5. **La variante qui gagne à 4 bits** : les **plans binaires**, où le nombre
   d'opérations vaut `popcount(v)` et non `v` — soit le passage de l'unaire au
   positionnel, appliqué aux *opérations* au lieu du stockage.

> ⚠️ Mesures sur les niveaux quantifiés d'un Q4_0 réel ; le raisonnement sur les
> seuils est analytique et indépendant du modèle.


---
*Généré par `run_value_encoding.py` — Qtrinet.*

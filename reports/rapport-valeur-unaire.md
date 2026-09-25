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

Sur ce modèle Q4_0 réel : `E[|v|] = 3.02` → coût de la répétition 2.63 b/poids contre 4,00 en dense.

## Verdict

1. **L'idée est exacte** : répéter l'adresse v fois reproduit exactement la valeur
   quantifiée, sans aucune perte au-delà de la quantification d'origine. Le
   raisonnement est juste — et il élimine bien la valeur du stockage.

2. **C'est de l'encodage unaire** : le coût est proportionnel à `v`, là où le
   positionnel coûte `log2(v)`. Sur une distribution *uniforme*, l'unaire perd à
   partir de 4 bits (E[|v|] ≈ 7,5 > k+1).

3. **Mais les distributions réelles ne sont pas uniformes** : sur ce Q4_0,
   `E[|v|] = 3.02` seulement — l'échelle du bloc est fixée par son maximum,
   donc 27 % des non-nuls valent ±1 et le code dense gaspille ses bits.
   La répétition gagne alors **même à 4 bits** : 2.63 contre 4,00 b/poids.

4. **Sa forme hybride est la meilleure** : unaire pour |v|=1 (gratuit — l'adresse
   porte le signe), puis plans binaires au-delà (`popcount` au lieu de `v`) →
   **1.85 b/poids, soit ×2.17**, pour 0.98 opération
   par poids contre 0.87 en dense : quasi gratuit en calcul aussi.

5. **Là où l'idée est optimale** : en **binaire** (k=1) et en **ternaire** (BitNet
   b1.58). Tous les non-nuls valent ±1, donc l'adresse *seule* porte la valeur :
   zéro bit de valeur, zéro répétition. C'est exactement l'encodage « listes
   signées » déjà mesuré à 0,39 b/poids.

6. **Conséquence matérielle** : le décodeur doit gérer trois cas — ajouter une fois
   (|v|=1), ajouter v fois (unaire), ou ajouter par plans décalés (`popcount`).
   Les trois se réduisent à des additions et des décalages : **aucun DSP**, la
   contrainte du cahier des charges tient.


> ⚠️ Mesures sur les niveaux quantifiés d'un Q4_0 réel (Qwen2.5-0.5B). `E[|v|]`
> dépend de la recette de quantification : Q4_K_M, avec ses échelles de blocs
> plus fines, donnerait une distribution différente — à mesurer avant de figer
> le format.


---
*Généré par `run_value_encoding.py` — Qtrinet.*

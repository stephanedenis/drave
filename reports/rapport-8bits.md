# Qtrinet — 8 bits : la perfection est-elle atteignable ?

Modèle : **qwen2** en Q8_0, 494.0 M poids analysés.

## 1. Distribution des niveaux

- densité : **99.2 %**
- niveaux distincts : **256** (sur 256 possibles)
- `E[|v|]` : **42.79**
- `E[popcount(|v|)]` : **3.13**
- niveaux les plus fréquents : `127` (1.6 %), `-127` (1.6 %), `2` (0.8 %), `-1` (0.8 %), `1` (0.8 %), `3` (0.8 %), `0` (0.8 %), `-2` (0.8 %)

## 2. Bits réellement nécessaires (sans perte)

| Codage | bits/poids | Gain |
|---|---|---|
| positionnel fixe | 8,000 | ×1,000 |
| **entropie de la source** | **7.648** | **×1.046** |
| **code de Huffman réel** | **7.671** | **×1.043** |

## 3. Encodages structurels

| Stratégie | bits/poids | opérations/poids |
|---|---|---|
| positionnel (8 bits) | 8,00 | 0.99 |
| plans denses (7 plans + signe) | 8,00 | 3.10 |
| unaire (répétition) | 42.45 | 42.45 |
| **Huffman (sans perte)** | **7.67** | 0.99 |

## 4. Sur le modèle entier

| | Taille des niveaux | Gain |
|---|---|---|
| 8 bits brut | 494.0 Mo | — |
| Huffman | 473.6 Mo | ×1.043 |
| borne entropique | 472.3 Mo | ×1.046 |

## Verdict

1. **La qualité à 8 bits est déjà la perfection pratique** : c'est la référence
   quasi sans perte de l'écosystème. La question qui reste n'est pas la qualité
   mais le **stockage exact**.
2. **Le gain sans perte existe mais il est modeste** : l'entropie de la source
   vaut 7.65 b/poids et un vrai code de Huffman atteint 7.67 b/poids, soit **×1.04**.
3. **L'uniformité des niveaux est la raison** : un quantificateur Q8_0 bien réglé
   répartit les poids sur beaucoup de niveaux, ce qui rapproche la distribution
   de l'uniforme et l'entropie de 8 bits. Il n'y a presque rien à récupérer :
   **c'est le signe d'une quantification déjà efficace**.
4. **Les encodages structurels ne servent à rien à 8 bits** : les plans denses
   coûtent exactement 8 bits/poids (7 magnitude + 1 signe = le code positionnel),
   et l'unaire explose (42 b/poids). La répétition d'adresse, si
   élégante soit-elle, n'a de sens que sur les petites valeurs.
5. **Conclusion** : la perfection sans perte se paie au prix de l'entropie, et
   à 8 bits l'entropie est déjà presque atteinte. Le vrai levier reste la
   **quantification à 4 bits et moins**, où la structure a de la place pour
   s'exprimer — c'est là que les gains mesurés (×2,17) se trouvent.


---
*Généré par `run_8bit_perfection.py` — Qtrinet.*

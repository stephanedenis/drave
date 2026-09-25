# Qtrinet — élagage et approche par événement

Modèle minimal (MLP 32→64→10), accuracy float **76.07 %**, ternaire (non élagué) **49.71 %**.

## 1. Densité naturelle du ternaire

- poids non nuls : **26.3 %** (densité d = 0.263)
- activations non nulles après ReLU : **52.8 %**
- événements réels (poids ∧ activation) : **13.9 %**

## 2. Coût des encodages (bits par poids)

| Encodage | Coût | À d = 50 % | À d = 25 % |
|---|---|---|---|
| dense 2 bits | 2,00 | 2,00 | 2,00 |
| **bitmap + signe** | **1 + d** | **1,50** | **1,25** |
| CSR bloc 16 b | 17·d | 8,50 | 4,25 |
| CSR plat 32 b | 33·d | 16,50 | 8,25 |
| N:M structuré (2:4) | (m+n)/m | 1,50 | — |

> Un poids ternaire non nul ne porte **qu'un signe**. Le bitmap dit *où* sont
> les non-nuls, le signe dit *lequel*. C'est pourquoi « bitmap + signe » est
> toujours ≤ au code dense 2 bits, et strictement meilleur dès qu'il y a un zéro.

## 3. Frontière précision ↔ bits/poids (mesurée)

| Gardés | Densité | Accuracy | dense | bitmap | CSR16 | CSR32 | gain bitmap |
|---|---|---|---|---|---|---|---|
| 100.0 % | 26.3 % | 49.71 % | 2.00 | 1.26 | 4.48 | 8.69 | ×1.58 |
| 75.0 % | 19.8 % | 49.41 % | 2.00 | 1.20 | 3.36 | 6.52 | ×1.67 |
| 50.0 % | 13.2 % | 45.31 % | 2.00 | 1.13 | 2.24 | 4.35 | ×1.77 |
| 25.0 % | 6.6 % | 52.93 % | 2.00 | 1.07 | 1.12 | 2.17 | ×1.88 |
| 12.5 % | 3.3 % | 50.00 % | 2.00 | 1.03 | 0.56 | 1.08 | ×1.94 |
| 6.2 % | 1.6 % | 50.49 % | 2.00 | 1.02 | 0.28 | 0.54 | ×1.97 |
| 3.1 % | 0.9 % | 47.66 % | 2.00 | 1.01 | 0.15 | 0.28 | ×1.98 |
| 2:4 struct. | 24.0 % | 48.73 % | 2,00 | 1.24 | — | — | ×1.61 |

## 4. Seuils de rentabilité

| Comparaison | Égalité à | Gagnant en dessous |
|---|---|---|
| bitmap vs dense2 | 100.0 % | bitmap |
| csr32 vs dense2 | 6.1 % | csr32 |
| csr16 vs dense2 | 11.8 % | csr16 |
| csr32 vs bitmap | 3.1 % | csr32 |
| csr16 vs bitmap | 6.2 % | csr16 |

## 5. Projection 7B sur une carte (tok/s)

| Densité | dense | bitmap | CSR16 | CSR32 | 2:4 |
|---|---|---|---|---|---|
| 100.0 % | 5.5 | 5.5 | 0.6 | 0.3 | 7.4 |
| 26.3 % | 5.5 | 8.7 | 2.5 | 1.3 | 7.4 |
| 50.0 % | 5.5 | 7.4 | 1.3 | 0.7 | 7.4 |
| 25.0 % | 5.5 | 8.8 | 2.6 | 1.3 | 7.4 |
| 12.5 % | 5.5 | 9.8 | 5.2 | 2.7 | 7.4 |
| 6.2 % | 5.5 | 10.4 | 10.4 | 5.4 | 7.4 |

## 6. Verdict

1. **Oui, un modèle ternaire est déjà creux** — ici 26.3 % de non-nuls, sans aucun élagage. C'est le point de départ, pas une contrainte ajoutée.
2. **L'encodage événementiel « bitmap + signe » domine le dense** : 1 + d bits/poids contre 2, soit jusqu'à 2× moins de trafic. Il ne coûte jamais plus cher.
3. **Le CSR, lui, est disqualifié** : rentable seulement sous 6 % (indice 32 b) ou 12 % (indice 16 b) de densité — un régime que les LLM n'atteignent pas sans s'effondrer.
4. **Le vrai obstacle n'est pas le poids, c'est l'activation** : un événement n'existe que si le poids *et* l'activation sont non nuls (ici 13.9 % d'événements réels). Récupérer l'activation à un index arbitraire impose une fenêtre de lecture et un multiplexeur par voie : ~21 LUT pour un 64:1, soit ≈ 3 400 ALM pour 312 voies (**2 % du FPGA**) — c'est payable.
5. **Recommandation** : garder le dense 2 bits comme chemin nominal (simple, déterministe, déjà validé) et ajouter un **encodage bitmap + signe** là où la densité est faible. Le saut de blocs entièrement nuls (1 bit par bloc de 64) est le premier pas, à 1,6 % de surcoût.

### Réserves à lever avant de s'engager

- La courbe précision ↔ élagage est **bruitée** : le modèle ne pèse que 2688 poids et son accuracy ternaire (49.7 %) laisse peu de marge de mesure. Les variations observées (±4 pt) sont dans le bruit d'un jeu de test de 1 024 exemples — **on ne peut pas conclure sur la dégradation due à l'élagage**.
- La densité naturelle (26.3 %) est propre à ce modèle. Un modèle **entraîné** en ternaire (BitNet b1.58) tourne plutôt autour de 50-70 % de non-nuls : le gain du bitmap y serait de ×1,2 à ×1,4, pas ×1,6.
- La littérature (SparseGPT, Wanda) situe l'élagage non structuré *one-shot* des LLM à 50-60 % sans réentraînement, et le 2:4 structuré (50 %) est la forme matériellement supportée. **Au-delà de ~90 % de zéros, un LLM généraliste s'effondre** — le régime où le CSR deviendrait rentable est donc hors d'atteinte.


---
*Généré par `run_sparsity.py` — Qtrinet.*

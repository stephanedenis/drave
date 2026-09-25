# Qtrinet — encodage de structure : éliminer la valeur

Idée testée : remplacer `(position, valeur)` par **deux listes triées de
destinations** (les « + » et les « − »). Le signe est porté par l'appartenance
à la liste : **plus aucun bit de valeur n'est stocké**, il ne reste que de la
position. Coûts mesurés sur les matrices réelles, pas estimés.

Modèle : MLP 32→64→10 (2688 poids), référence float 76.07 %.

## Coûts réels (bits/poids)

| Motif | k | Densité | Accuracy | bitmap+signe | **listes signées** | CSR | dense | entropie | écart moyen |
|---|---|---|---|---|---|---|---|---|---|
| non structuré | 1 | 26.9 % | 45.02 % | 1.27 | **3.52** | 10.03 | 2.00 | 0.90 | 3.6 |
| non structuré | 2 | 49.6 % | 72.46 % | 1.50 | **5.02** | 18.02 | 2.00 | 1.22 | 2.0 |
| non structuré | 1 | 18.0 % | 64.55 % | 1.18 | **3.24** | 7.08 | 2.00 | 0.71 | 5.5 |
| non structuré | 2 | 24.6 % | 65.53 % | 1.25 | **3.95** | 9.52 | 2.00 | 0.85 | 4.1 |
| non structuré | 1 | 9.0 % | 59.18 % | 1.09 | **2.88** | 4.13 | 2.00 | 0.44 | 11.0 |
| non structuré | 2 | 12.1 % | 65.33 % | 1.12 | **3.24** | 5.24 | 2.00 | 0.54 | 8.3 |
| non structuré | 1 | 5.1 % | 58.59 % | 1.05 | **2.65** | 2.82 | 2.00 | 0.29 | 19.8 |
| non structuré | 2 | 6.0 % | 61.82 % | 1.06 | **2.82** | 3.18 | 2.00 | 0.33 | 16.8 |
| groupé (blocs de 8) | 1 | 17.9 % | 59.86 % | 1.18 | **3.13** | 7.05 | 2.00 | 0.70 | 5.2 |
| groupé (blocs de 8) | 2 | 39.0 % | 69.43 % | 1.39 | **4.30** | 14.40 | 2.00 | 1.09 | 2.5 |
| groupé (blocs de 8) | 1 | 11.5 % | 54.79 % | 1.11 | **2.81** | 4.94 | 2.00 | 0.52 | 7.8 |
| groupé (blocs de 8) | 2 | 20.4 % | 65.92 % | 1.20 | **3.41** | 8.09 | 2.00 | 0.76 | 4.5 |
| groupé (blocs de 8) | 1 | 6.9 % | 53.42 % | 1.07 | **2.60** | 3.41 | 2.00 | 0.36 | 12.2 |
| groupé (blocs de 8) | 2 | 11.0 % | 57.62 % | 1.11 | **2.89** | 4.90 | 2.00 | 0.51 | 8.0 |
| groupé (blocs de 8) | 1 | 4.3 % | 42.87 % | 1.04 | **2.47** | 2.55 | 2.00 | 0.26 | 20.3 |
| groupé (blocs de 8) | 2 | 5.8 % | 52.83 % | 1.06 | **2.61** | 3.13 | 2.00 | 0.32 | 15.3 |

## Frontière de Pareto (coûts réels)

| b/poids | Accuracy | tok/s (7B, 1 carte) | Encodage |
|---|---|---|---|
| 1.04 | 42.87 % | 10.6 | groupé (blocs de 8), k=1, d=4.3%, bitmap |
| 1.05 | 58.59 % | 10.5 | non structuré, k=1, d=5.1%, bitmap |
| 1.06 | 61.82 % | 10.4 | non structuré, k=2, d=6.0%, bitmap |
| 1.12 | 65.33 % | 9.9 | non structuré, k=2, d=12.1%, bitmap |
| 1.20 | 65.92 % | 9.2 | groupé (blocs de 8), k=2, d=20.4%, bitmap |
| 1.39 | 69.43 % | 7.9 | groupé (blocs de 8), k=2, d=39.0%, bitmap |
| 1.50 | 72.46 % | 7.4 | non structuré, k=2, d=49.6%, bitmap |
| 2.00 | 4971.00 % | 5.5 | dense ternaire (référence CDC) |

## Coût EXACT à largeur réaliste (N = 4096)

Le tableau précédent est dominé par les en-têtes de liste (lignes de 64 poids).
Sur une largeur réaliste, le classement s'inverse :

| Densité | bitmap + signe | **listes signées** | gain | tok/s 7B | vs dense 2 b |
|---|---|---|---|---|---|
| 100.0 % | 2.000 | **2.282** | 0.88× | 4.8 | ×0.88 |
| 50.0 % | 1.500 | **1.838** | 0.82× | 6.0 | ×1.09 |
| 25.0 % | 1.250 | **1.306** | 0.96× | 8.5 | ×1.53 |
| 12.5 % | 1.125 | **0.871** | ×1.29 | 12.7 | ×2.30 |
| 5.0 % | 1.050 | **0.476** | ×2.21 | 23.2 | ×4.20 |
| 2.0 % | 1.020 | **0.251** | ×4.06 | 44.0 | ×7.96 |
| 1.0 % | 1.010 | **0.151** | ×6.71 | 73.3 | ×13.28 |

**Bascule vers 20 % de densité** : au-dessus, le bitmap + signe gagne (les
écarts sont trop courts pour amortir) ; en dessous, les listes signées gagnent,
et l'écart se creuse vite (×4,2 à 5 %, ×13 face au dense 2 bits à 1 %).


## Verdict

1. **L'idée est juste : la valeur disparaît complètement.** Avec des poids ±1,
   l'appartenance à la liste porte le signe, et il ne reste que des **positions**.
   La matrice devient un graphe biparti signé.
2. **Le gain dépend entièrement de la densité** : ~×1,3 à 12,5 %, ×2,2 à 5 %,
   ×13 face au dense ternaire à 1 %. La bascule avec le bitmap se situe vers 20 %.
3. **Ce qui rend l'idée payante, c'est l'encodage par écarts** (listes triées).
   Sans lui, un indice complet coûte plus cher que le bitmap qu'il remplace.
4. **Le décodeur reste LUT-only** : c'est un accumulateur d'écarts (addition + FIFO),
   plus un compteur de liste. Aucun DSP — la contrainte du cahier des charges tient.
5. **Le coût se déplace vers la collecte d'activation**, qui devient totalement
   irrégulière : chaque événement vise un indice arbitraire. C'est LE point dur de
   cette voie (croisement ou réplication de bancs M20K), pas le décodage.
6. **Marge restante** : à 5 %, l'entropie des positions vaut 0,288 b/poids contre
   0,476 pour les listes — il reste un facteur 1,65 dans un codage plus fin
   (arithmétique, ou exploitation du groupement).

> ⚠️ Les coûts ci-dessus sont mesurés exactement (positions aléatoires). Les
> *densités atteignables* viennent du MLP jouet : sur un LLM réel, 5-12 % de
> densité demande un réentraînement lourd, à valider sur un vrai modèle.


---
*Généré par `run_encoding.py` — Qtrinet.*

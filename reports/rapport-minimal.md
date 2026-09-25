# Qtrinet — test de principe : modèle minimal en ternaire / multi-bits

Modèle : MLP 32→64→10, entraîné sur 4096 exemples synthétiques, évalué sur 1024.

## 1. Fidélité de la quantification

| Format des poids | b/poids | Accuracy | Δ vs float |
|---|---|---|---|
| float32 (référence) | 32.00 | 76.07 % | +0.00 pt |
| int8 (signe-magnitude) | 8.00 | 76.27 % | +0.20 pt |
| int4 (signe-magnitude) | 4.00 | 74.12 % | -1.95 pt |
| ternaire 1,58 b (dense 2 b) | 2.00 | 49.71 % | -26.37 pt |
| multi 2 plans ternaires | 4.00 | 73.44 % | -2.64 pt |
| multi 3 plans ternaires | 6.00 | 74.12 % | -1.95 pt |
| multi 4 plans ternaires | 8.00 | 75.98 % | -0.10 pt |

### Chemin entier (ce que fera le FPGA : add/sub, aucun DSP)

| Mesure | Valeur |
|---|---|
| Exactitude arithmétique — couche 1 (entier vs flottant, mêmes entrées) | 4.233e-07 |
| Exactitude arithmétique — couche 2 | 1.861e-06 |
| Erreur de quantification des activations — couche 1 | 1.089e-01 |
| Erreur de quantification des activations — couche 2 | 6.322e-01 |
| Accuracy chemin entier (poids ternaires + activations int8) | 49.22 % |
| Accuracy chemin flottant (mêmes poids quantifiés) | 49.71 % |
| Accumulateur max (doit tenir en int32) | 488 |

## 2. Coût des encodages

| Encodage | bits/poids | Taille totale |
|---|---|---|
| float32 | 32.00 | 10.5 Kio |
| int8 | 8.00 | 2.6 Kio |
| int4 | 4.00 | 1.3 Kio |
| ternaire dense (2 b) | 2.00 | 0.7 Kio |
| borne entropique ternaire | 1.58 | 0.5 Kio |
| multi 2 bits — dense 1 b/plan | 2.00 | 0.7 Kio |
| multi 2 bits — bitmap+signe | 4.00 | 1.3 Kio |
| multi 2 bits — CSR/plan (CDC) | 28.44 | 9.3 Kio |
| multi 3 bits — dense 1 b/plan | 3.00 | 1.0 Kio |
| multi 3 bits — bitmap+signe | 6.00 | 2.0 Kio |
| multi 3 bits — CSR/plan (CDC) | 44.66 | 14.7 Kio |
| multi 4 bits — dense 1 b/plan | 4.00 | 1.3 Kio |
| multi 4 bits — bitmap+signe | 8.00 | 2.6 Kio |
| multi 4 bits — CSR/plan (CDC) | 61.77 | 20.3 Kio |
| ternaire en CSR (CDC) | 10.10 | 3.3 Kio |

### Densité par plan (justifie — ou non — le CSR)

| Magnitude | plan 0 | plan 1 |
|---|---|---|
| 2 bits | 50.9 % | 27.5 % |
| 3 bits | 51.3 % | 44.1 % | 27.5 % |
| 4 bits | 51.5 % | 48.1 % | 42.8 % | 27.5 % |

## 3. Débit projeté sur la carte (Stratix V GS D5)

Débits **mesurés** : DDR3 9,66 Go/s · PCIe x8 6,5 Go/s · fmax actuel 124 MHz.

| Modèle / encodage | Taille | ms/token | tok/s | Voies MAC | ALM |
|---|---|---|---|---|---|
| modèle minimal — ternaire dense 2 b | 0.0 Mo | 0.000 | 13989862.4 | 312 | 9360 |
| modèle minimal — multi 4 bits (1 b/plan) | 0.0 Mo | 0.000 | 6994931.2 | 156 | 4680 |
| modèle minimal — multi 4 bits (bitmap+signe) | 0.0 Mo | 0.000 | 3497465.6 | 78 | 2340 |
| modèle minimal — int8 | 0.0 Mo | 0.000 | 3497465.6 | 78 | 2340 |
| modèle minimal — ternaire CSR (CDC) | 0.0 Mo | 0.001 | 1645866.2 | 37 | 1110 |
| 7B — ternaire 2 b | 1750.0 Mo | 181.159 | 5.5 | 312 | 9360 |
| 7B — 4 bits | 3500.0 Mo | 362.319 | 2.8 | 156 | 4680 |
| 7B — ternaire CSR | 14875.0 Mo | 1539.855 | 0.6 | 37 | 1110 |
| 70B — ternaire 2 b | 17500.0 Mo | 1811.594 | 0.6 | 312 | 9360 |
| 70B — 4 bits | 35000.0 Mo | 3623.188 | 0.3 | 156 | 4680 |
| 70B — ternaire CSR | 148750.0 Mo | 15398.551 | 0.1 | 37 | 1110 |

## 4. Conclusions

1. **Le chemin entier est exact** : 4.23e-07 / 1.86e-06 d'écart avec le calcul flottant — c'est de l'arrondi flottant, rien d'autre. Le principe « pas de DSP, que des additions/soustractions » est donc validé.
2. **La quantification ternaire *post-entraînement* coûte cher** : 76.1 % → 49.7 % (-26.4 pt). Ce n'est PAS un verdict contre BitNet : les modèles ternaires (b1.58) sont *entraînés* avec la contrainte. Un modèle float quantifié après coup perd sa fonction.
3. **Le découpage en plans (multi-bits) dégrade progressivement** : 4 plans → 76.0 % (-0.1 pt). C'est la voie naturelle pour réutiliser un modèle 4 bits existant sans réentraînement.
4. **Le CSR est un piège chiffré** : 10.1 b/poids pour le ternaire et 61.8 b/poids pour 4 plans, contre 2.0 et 4,0 b/poids en dense — soit 5 à 15× plus de trafic mémoire, qui se traduit directement en division du débit (cf. §3).
5. **Tout le projet est borné par la DDR3**, pas par le calcul : à 124 MHz il ne faut que ~312 voies de MAC (≈ 9 400 ALM, 5 % du FPGA) pour saturer les 9,66 Go/s. 96 % du device reste disponible pour la mémoire, le décodeur et le réseau.

> ⚠️ **Réserve** : le modèle minimal (10 Kio) n'est pas borné par la mémoire mais par la latence. Ses chiffres de débit (§3, premières lignes) ne veulent rien dire — seules les projections 7B/70B sont significatives.

> ⚠️ Le ternaire testé ici est de la quantification *a posteriori*. La question « le ternaire suffit-il ? » se tranche sur un modèle **entraîné en ternaire** (BitNet b1.58) — ce sera l'étape suivante.


---
*Généré par `run_quantify.py` — Qtrinet.*

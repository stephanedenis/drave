# Qtrinet — la sparsité peut-elle acheter de la précision ?

Modèle minimal (MLP 32→64→10, 2688 poids), référence float **76.07 %**.

Protocole : **prune → retrain (masque fixe) → quantize → refit d'échelle**.

## Modèle de coût

Un poids ternaire non nul ne porte qu'un signe, donc un encodage creux coûte :

```
bitmap (1 bit/poids) + k bits par non-nul   =   1 + k·d   bits/poids
```

À densité donnée, **on peut dépenser les bits économisés en précision** au lieu
de les dépenser en zéros. C'est la forme utile de l'intuition « plus de nœuds ».

## Résultats (triés par coût)

| Encodage | k | Densité | b/poids | Accuracy | tok/s 7B (1 carte) |
|---|---|---|---|---|---|
| creux 1 bits d=0.125 | 1 | 8.4 % | 1.08 | 60.06 % | 10.2 **◀** |
| creux 1 bits d=0.250 | 1 | 16.8 % | 1.17 | 64.84 % | 9.5 **◀** |
| creux 2 bits d=0.125 | 2 | 11.8 % | 1.24 | 65.04 % | 8.9 **◀** |
| creux 1 bits d=0.500 | 1 | 26.6 % | 1.27 | 48.63 % | 8.7 |
| creux 3 bits d=0.125 | 3 | 12.3 % | 1.37 | 67.29 % | 8.1 **◀** |
| creux 2 bits d=0.250 | 2 | 24.0 % | 1.48 | 70.41 % | 7.5 **◀** |
| creux 4 bits d=0.125 | 4 | 12.4 % | 1.50 | 67.48 % | 7.4 |
| creux 3 bits d=0.250 | 3 | 24.8 % | 1.74 | 71.09 % | 6.3 **◀** |
| creux 2 bits d=0.500 | 2 | 49.3 % | 1.99 | 72.17 % | 5.6 **◀** |
| creux 4 bits d=0.250 | 4 | 24.9 % | 2.00 | 71.09 % | 5.5 |
| creux 8 bits d=0.125 | 8 | 12.5 % | 2.00 | 67.87 % | 5.5 |
| dense 1 bits (ternaire) | 1 | 100.0 % | 2.00 | 49.71 % | 5.5 |
| dense 2 bits | 2 | 100.0 % | 2.00 | 73.44 % | 5.5 **◀** |
| creux 3 bits d=0.500 | 3 | 50.0 % | 2.50 | 74.22 % | 4.4 **◀** |
| creux 4 bits d=0.500 | 4 | 50.0 % | 3.00 | 76.07 % | 3.7 **◀** |
| dense 3 bits | 3 | 100.0 % | 3.00 | 74.12 % | 3.7 |
| creux 8 bits d=0.250 | 8 | 25.0 % | 3.00 | 71.68 % | 3.7 |
| dense 4 bits | 4 | 100.0 % | 4.00 | 75.98 % | 2.8 |
| creux 8 bits d=0.500 | 8 | 50.0 % | 5.00 | 76.27 % | 2.2 **◀** |
| dense 8 bits | 8 | 100.0 % | 8.00 | 76.37 % | 1.4 **◀** |

## Frontière de Pareto (accuracy maximale à coût donné)

| b/poids | Encodage | Accuracy | tok/s 7B |
|---|---|---|---|
| 1.08 | creux 1 bits d=0.125 | 60.06 % | 10.2 |
| 1.17 | creux 1 bits d=0.250 | 64.84 % | 9.5 |
| 1.24 | creux 2 bits d=0.125 | 65.04 % | 8.9 |
| 1.37 | creux 3 bits d=0.125 | 67.29 % | 8.1 |
| 1.48 | creux 2 bits d=0.250 | 70.41 % | 7.5 |
| 1.74 | creux 3 bits d=0.250 | 71.09 % | 6.3 |
| 1.99 | creux 2 bits d=0.500 | 72.17 % | 5.6 |
| 2.00 | dense 2 bits | 73.44 % | 5.5 |
| 2.50 | creux 3 bits d=0.500 | 74.22 % | 4.4 |
| 3.00 | creux 4 bits d=0.500 | 76.07 % | 3.7 |
| 5.00 | creux 8 bits d=0.500 | 76.27 % | 2.2 |
| 8.00 | dense 8 bits | 76.37 % | 1.4 |

## Verdict

1. **« Plus de nœuds » ne marche pas** : ajouter des PE n'ajoute pas de bande
   passante. Le débit est fixé par la DDR3 (9,66 Go/s) ; 312 voies suffisent à la
   saturer. Les nœuds supplémentaires resteraient affamés.
2. **Mais « dépenser la sparsité en précision » marche** — et c'est la même
   intuition, correctement orientée. Voir la frontière de Pareto ci-dessus :
   à budget de bits égal, un encodage creux à valeurs multi-bits bat le ternaire
   dense, parce qu'il ne gaspille aucun bit sur les zéros.
3. **Conséquence matérielle** : un MAC int4×int8 en LUT (4 additions
   conditionnelles décalées) coûte ~30-35 ALM contre ~20 pour le PE ternaire
   (mux + add/sub). Pour 312 voies : ~11 000 ALM, soit **6 % du FPGA** au lieu
   de 4 %. Le surcoût est négligeable — et **aucun DSP n'est requis**, la
   contrainte du cahier des charges est respectée.
4. **Réserve** : ces mesures sont faites sur un MLP de 2 688 poids, avec un
   réentraînement court. Les valeurs absolues ne se transposent pas à un LLM ;
   c'est la **forme de la frontière** qui est transposable.


---
*Généré par `run_precision.py` — Qtrinet.*

# qtrinet-core

Moteur d'exécution par **listes d'événements** pour modèles quantifiés.
Rust, **std seul** (aucune dépendance externe, aucun accès réseau au build).

## Ce que ça fait

```
cargo build --release
./target/release/qtrinet-core <modele.gguf> [--matrix blk.0.ffn_gate.weight] [--threads 16]
```

1. **Lecteur GGUF** complet (métadonnées, tenseurs, Q4_0/Q8_0/F16/F32 → f32 ou niveaux bruts).
2. **Encodages de listes**, avec taille **mesurée** sur les données réelles :
   - `dense k` — référence
   - `bitmap + signe` — ternaire (1 b/poids + 1 b/non-nul)
   - `creux k` — bitmap + k bits par non-nul (sans perte pour k = largeur du modèle)
   - `listes signées + écarts` — deux listes triées (+, −) par ligne, écarts en varint ;
     **zéro bit de valeur**, le signe est porté par l'appartenance à la liste
3. **Moteur d'événements** : pour chaque source active, on pousse sa valeur vers les
   destinations de sa liste. Accumulateur par thread, puis réduction.
4. **Exécution sans multiplieur** : `w·x = Σ_b bit_b(|w|) · (x << b)` —
   `popcount(|w|)` additions par poids, **aucun DSP**.

## Résultats mesurés (Qwen2.5-0.5B Q8_0, 16 threads)

### Tailles d'encodage (bits/poids, densité 99,2 %)

| Encodage | b/poids | Perte ? |
|---|---|---|
| dense 8 bits | 8,000 | non (référence) |
| **bitmap + signe** | **1,992** | oui (ternarise) |
| creux k=4 | 4,970 | oui |
| creux k=8 | 8,939 | **non** |
| listes signées + écarts | 7,975 | non |

➡️ Sur une matrice **dense**, aucun encodage ne bat le dense 8 bits — sauf le ternaire,
qui perd la magnitude. Les listes ne gagnent que sous ~20 % de densité : c'est la
confirmation, en Rust et sur le vrai modèle, de l'analyse faite en Python.

### Débit du moteur d'événements (variable par construction)

| Densité activations | Événements | G év/s | ms/appel |
|---|---|---|---|
| 0 % | 0 | — | 0,484 |
| 5 % | 217 851 | 0,59 | 0,370 |
| 25 % | 1 082 120 | 2,16 | 0,501 |
| 100 % | 4 325 087 | **4,66** | 0,928 |

- Le **nombre d'événements varie avec les activations** — c'est le débit variable cherché.
- **Contrôle : listes vs dense → IDENTIQUE** (le moteur est exact).
- Plancher de 0,48 ms à densité nulle : coût fixe du lancement des threads et de la
  réduction. **Première optimisation à faire** (pool de threads persistant).

### Exécution sans multiplieur

| | Temps | Rapport |
|---|---|---|
| multiplication i8×i8 | 2,5 ms | — |
| décalages + additions | 110,7 ms | ×44 |

Résultat **identique**, mais **44× plus lent sur CPU** — parce que la multiplication
entière est vectorisée (SIMD) alors que la boucle de décalages est scalaire et
imprévisible. Conclusion honnête : **le CPU n'est pas la cible du shift-and-add** ;
c'est le FPGA, où le multiplieur coûte des DSP et où l'additionneur décalé coûte
quelques ALM.

## Suite

1. **Pool de threads persistant** — supprimer le plancher de 0,48 ms/appel.
2. **Décodage SIMD** des varints et des bitmaps (objectif : 10 G év/s).
3. **Vecteur d'activation creux explicite** — aujourd'hui on balaie les sources actives ;
   la vraie cascade construira cette liste en amont.
4. **Fusion des listes** (le « réseau de combinaison par destination ») : sortir du
   varint quand le motif le permet.

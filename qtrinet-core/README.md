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

| Densité | Événements | scoped (avant) | **pool (après)** | ms/appel | gain |
|---|---|---|---|---|---|
| 0 % | 0 | — | — | **0,049** | **×10** |
| 1 % | 43 560 | 0,11 G év/s | **0,84** | 0,052 | ×7,5 |
| 5 % | 217 851 | 0,54 | **2,95** | 0,074 | ×5,5 |
| 10 % | 433 035 | 1,07 | **4,02** | 0,108 | ×3,8 |
| 25 % | 1 082 120 | 2,31 | **4,91** | 0,220 | ×2,1 |
| 50 % | 2 163 317 | 3,76 | **5,51** | 0,392 | ×1,5 |
| 100 % | 4 325 087 | 5,77 | **5,80** | 0,746 | ×1,0 |

- **Coût fixe : 0,484 ms → 0,049 ms** grâce au pool persistant (threads et
  accumulateurs conservés entre les appels). Le gain est maximal là où il fallait :
  **×8,5 en régime creux**, précisément le régime qui nous intéresse.
- **Le débit varie de ×15** entre densité nulle (0,049 ms) et pleine (0,746 ms) —
  c'est le débit variable cherché, mesuré.
- **Pic : 5,80 G événements/s** (contre 4,66 avant), soit 75 % du banc C de
  référence (7,79 G) qui utilisait des écarts à largeur fixe, pas des varints.
- **Contrôle : pool OK | scoped OK | bitmap OK** — les trois chemins donnent le
  même résultat.

### Bitmap vs varint

À 100 % de densité : bitmap 4,07 G év/s contre **5,80** pour les varints. Le chemin
rapide « varint d'un octet » est très efficace quand la matrice est dense ; le
bitmap garde l'avantage de la **taille** (1,99 b/poids contre 7,97).

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

1. ~~Pool de threads persistant~~ ✅ fait (×10 sur le coût fixe).
2. **Réduction incrémentale** : ne réduire que les sorties réellement touchées
   (le plancher de 0,049 ms reste dominé par la réduction des 896 sorties × 16 threads).
3. **Traitement par blocs de destination** : la dispersion scalaire plafonne vers
   5,8 G év/s ; regrouper les événements d'une même plage de destinations
   permettrait de vectoriser (AVX2 n'a ni gather ni scatter entiers).
4. **Vecteur d'activation creux explicite** — la vraie cascade le construira en amont.
5. **Fusion de listes** par compartiments de destination.

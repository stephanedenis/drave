# Croisement push / pull — quand l'architecture événementielle est-elle justifiée ?

Deux façons d'exécuter le même modèle quantifié :

- **push** (notre architecture) : pour chaque source active, on *disperse* ses
  poids dans un accumulateur (`acc[dest] += x·w`). Le flux est indexé par
  source, un événement = écart + valeur, 2 octets.
- **pull** (le noyau dense ordinaire) : pour chaque sortie, on *lit* sa ligne de
  poids et on fait un produit scalaire. 1 octet par poids, aucune dispersion.

Elles donnent **exactement le même résultat** — vérifié : perplexité 19,2647 au
chiffre près sur 510 jetons, tokens identiques, en écrivant les deux chemins avec
le même ordre d'opérations (les sommes entières sont exactes des deux côtés).

> ⚠️ **Corrigé le 27/09** : le tableau de croisement de la section 1 mesurait
> « push » contre « dense » alors que le drapeau `--dense`, placé en dernier
> argument, n'était jamais lu (`while i + 1 < args.len()`), et le mode dense
> sommait des tranches périmées. Les chiffres ci-dessous sont ceux du banc
> instrumenté, à arithmétique identique. Voir
> `rapport-mur-memoire-4bits.md`.

---

## 1. Le croisement

Temps CPU pour 24 tokens, meilleur de 2, mesures entrelacées. La densité est
celle des activations, imposée par k-WTA.

Mesure refaite sur `blk.0.ffn_gate.weight` (4 864 × 896, 4,36 M poids), 16 threads,
en comparant cette fois **la même arithmétique** (`PushMat` et `DenseQ8` ont la
même quantification int8, une échelle par sortie) :

| densité | push (ms) | pull (ms) | push/pull |
|---|---|---|---|
| 0 % | 0,004 | 0,167 | 0,03 |
| 1 % | 0,019 | 0,162 | 0,12 |
| 5 % | 0,047 | 0,168 | 0,28 |
| **10 %** | 0,078 | 0,163 | **0,48** |
| **25 %** | 0,180 | 0,163 | **1,11** |
| 50 % | 0,355 | 0,165 | 2,15 |
| **100 %** | 0,801 | 0,171 | **4,69** |

➡️ **Les deux architectures se croisent à ~22 % de densité d'activation**, pas à
10 %. Le chiffre se lit dans le rapport à pleine densité : le pull traite 4,7 fois
plus de poids par seconde que le push ne traite d'événements, donc l'égalité tombe
vers 1/4,7. À 10 % le push est ×2,1 plus rapide, à 1 % ×8,3.

Le seuil de bascule `seuil_push` est passé de 0,15 à **0,22**.

## 2. Pourquoi ce chiffre ordonne tout le projet

| fait mesuré | densité d'activation | côté du croisement |
|---|---|---|
| LLM dense entraîné (notre Qwen2.5-0.5B) | **100 %** (0,00 % de zéros) | ❌ pull gagne ×4,7 |
| meilleure parcimonie imposée sans entraînement | ~85 % | ❌ pull gagne |
| réseau à décharge entraîné (SpikeGPT) | **R̂ = 0,15** | ✅ **push gagne** |
| réseau vraiment creux (ReLU, MoE, top-k) | < 10 % | ✅ push gagne |

**Toute la thèse du projet tient donc à une seule question : la densité
d'activation.** Un LLM dense se place exactement du mauvais côté du croisement,
et c'est pourquoi le mode événementiel n'a jamais rendu le débit promis. Un
réseau entraîné à décharger se place du bon côté, avec une marge confortable.

## 3. Correction d'une affirmation antérieure

Le rapport d'inférence annonçait : « le mode liste est maintenant 8 % plus
rapide que le noyau dense (15,8 contre 14,7 tok/s) ». **C'est faux, et je l'ai
mesuré deux fois.** Le produit scalaire du noyau dense accumulait en **i64 sur
toute la ligne**, ce qui empêchait toute vectorisation ; réécrit avec une
accumulation i32 par tranches de 256 (reportée en i64), il passe de 14,7 à
**36,4 tok/s** :

| | tok/s | PPL |
|---|---|---|
| push (événements) | 15,59 | 24,8995 |
| pull (dense i8), avant | 14,66 | 24,8995 |
| **pull (dense i8), après** | **36,43** | 24,8995 |

➡️ **C'est la troisième fois dans cette session qu'un simple réglage de code
renverse une conclusion d'architecture** — après l'attention non vectorisée
(÷2) et la liste des destinations touchées (+35 %). La règle de méthode ajoutée
au programme vaut donc aussi pour les comparaisons entre architectures : *avant
de conclure qu'une approche est meilleure, vérifier que les deux sont écrites
correctement.*

## 3 bis. Le dispatch par mesure, vérifié en conditions réelles

`--auto` charge les deux formes et bascule à chaque projection selon la densité
d'activation mesurée. Vérification sur le modèle entier, 255 jetons, 16 threads ;
les **événements** disent quel chemin a servi (0 = tout dense) :

| `--act-topk` | densité | pull | auto |
|---|---|---|---|
| 1000 | 111 % | 0 év — 9,1 s | 0 év — 9,3 s (dense) |
| 400 | 44 % | 0 év — 10,1 s | 0 év — 9,4 s (dense) |
| 200 | 22 % | 0 év — 9,6 s | 18,1 G év — 8,7 s (bascule) |
| 100 | 11 % | 0 év — 9,1 s | 9,1 G év — **7,1 s** |
| 50 | 5 % | 0 év — 9,1 s | 4,5 G év — **6,2 s** |

➡️ La bascule tombe exactement au seuil mesuré (22 %), et le gain croît à mesure
que la densité baisse — ×1,47 à 5 % de densité. Le choix n'est plus une
préférence d'architecture, c'est une **mesure**.

## 4. Ce que ça change concrètement

1. **Sur CPU, le mode pull est le bon choix** au-dessus de 22 % de densité. Le
   moteur gagne ×2,27 de bout en bout (13,6 → 30,7 tok/s, 510 jetons) à basculer
   sur ce chemin pour un modèle dense — et le résultat est identique au bit près.
2. **Le FPGA garde le push** : c'est sa forme naturelle — pas de multiplieur,
   accumulateur en BRAM, dispersion dans un banc privé. Le croisement y est
   différent (la DDR3 de la carte fait 9,66 Go/s contre 380 pour le GPU), mais
   la question de densité reste la même.
3. **Le choix d'architecture devient une fonction de la densité mesurée**, pas
   une préférence. Le moteur sait faire les deux ; il devrait choisir par
   mesure, matrice par matrice.

## 5. Reproductible

```bash
cd qtrinet-core && cargo build --release
# les deux modes, résultats identiques
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --infer --ids 9707,0 --n 32 --threads 16 --abits 8
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --infer --ids 9707,0 --n 32 --threads 16 --abits 8 --dense
# le croisement
for k in 1000 500 250 100 50; do
  ./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --infer --ids 9707,0 --n 24 --threads 16 --abits 8 --act-topk $k
  ./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --infer --ids 9707,0 --n 24 --threads 16 --abits 8 --act-topk $k --dense
done
```

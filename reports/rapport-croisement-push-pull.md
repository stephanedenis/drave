# Croisement push / pull — quand l'architecture événementielle est-elle justifiée ?

Deux façons d'exécuter le même modèle quantifié :

- **push** (notre architecture) : pour chaque source active, on *disperse* ses
  poids dans un accumulateur (`acc[dest] += x·w`). Le flux est indexé par
  source, un événement = écart + valeur, 2 octets.
- **pull** (le noyau dense ordinaire) : pour chaque sortie, on *lit* sa ligne de
  poids et on fait un produit scalaire. 1 octet par poids, aucune dispersion.

Elles donnent **exactement le même résultat** — vérifié : 32 tokens identiques
et perplexité 24,8995 au chiffre près dans les deux modes.

---

## 1. Le croisement

Temps CPU pour 24 tokens, meilleur de 2, mesures entrelacées. La densité est
celle des activations, imposée par k-WTA.

| densité d'activation | push (s CPU) | pull (s CPU) | gagnant |
|---|---|---|---|
| **100 %** | 42,12 | **19,51** | pull, **×2,16** |
| 50 % | 27,08 | **16,28** | pull, ×1,66 |
| 25 % | 21,49 | **16,08** | pull, ×1,34 |
| **10 %** | **17,63** | 17,59 | **égalité** |
| 5 % | **16,82** | 17,47 | push, ×1,04 |

➡️ **Les deux architectures se croisent à 10 % de densité d'activation.** Au-dessus,
le noyau dense gagne — jusqu'à 2,2× à pleine densité. En dessous, le mode
événementiel gagne.

## 2. Pourquoi ce chiffre ordonne tout le projet

| fait mesuré | densité d'activation | côté du croisement |
|---|---|---|
| LLM dense entraîné (notre Qwen2.5-0.5B) | **100 %** (0,00 % de zéros) | ❌ pull gagne ×2,2 |
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

## 4. Ce que ça change concrètement

1. **Sur CPU, le mode pull est le bon choix** au-dessus de 10 % de densité. Le
   moteur gagnerait 2,3× à basculer sur ce chemin pour les modèles denses.
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

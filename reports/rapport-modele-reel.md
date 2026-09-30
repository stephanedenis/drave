# Drave — le modèle réel expose-t-il ses grappes ?

Modèle analysé : **qwen2**, 24 couches, hidden 896, intermédiaire 4864, 14 têtes / 2 KV (GQA).

## 1. Parcimonie intrinsèque

| Tenseur (couche 0) | \|w\|<5 % max | <10 % | <20 % |
|---|---|---|---|
| blk.0.attn_norm.weight | 19.0 % | 77.9 % | 92.2 % |
| blk.0.ffn_down.weight | 62.5 % | 91.1 % | 99.7 % |
| blk.0.ffn_gate.weight | 73.8 % | 96.3 % | 99.9 % |
| blk.0.ffn_up.weight | 56.5 % | 87.5 % | 99.7 % |
| blk.0.ffn_norm.weight | 0.0 % | 0.0 % | 0.0 % |
| blk.0.attn_k.weight | 68.5 % | 87.7 % | 96.8 % |
| blk.0.attn_output.weight | 95.9 % | 99.7 % | 100.0 % |
| blk.0.attn_q.weight | 79.3 % | 94.3 % | 99.1 % |
| blk.0.attn_v.weight | 45.2 % | 74.6 % | 95.7 % |

## 2. Spécialisation afférente de la dimension cachée

Part de la masse d'entrée d'un neurone venant de sa grappe dominante.
**1/G = pas de structure, 1 = blocs disjoints.**

| Grappes G | Couche 0 (apprise) | Couches 1+ (test) | Grappes aléatoires | Test/aléatoire |
|---|---|---|---|---|
| 4 | 27.4 % | 27.5 % | 27.5 % | **1.00×** |
| 8 | 15.3 % | 15.2 % | 15.1 % | **1.00×** |

## 3. Dividende d'encodage (réordonnancement par grappe)

| Tenseur | Seuil | Densité | Écart naturel | Écart groupé | Gain |
|---|---|---|---|---|---|
| blk.0.ffn_gate.weight | 5 % | 5.0 % | 42.01 | 44.97 | 0.93× |
| blk.0.ffn_gate.weight | 10 % | 10.0 % | 15.68 | 16.11 | 0.97× |
| blk.0.ffn_gate.weight | 20 % | 20.0 % | 6.27 | 6.28 | 1.00× |
| blk.0.ffn_down.weight | 5 % | 5.0 % | 24.91 | 24.91 | 1.00× |
| blk.0.ffn_down.weight | 10 % | 10.0 % | 11.54 | 11.54 | 1.00× |
| blk.0.ffn_down.weight | 20 % | 20.0 % | 5.42 | 5.42 | 1.00× |

## 4. Structure explicite : GQA

- `attn_q` : (896, 896), 14 têtes de 64 dimensions
- énergie par tête : 1.4 % à 28.5 % (uniforme = 7.1 %)
- similarité entre têtes : 0.020 en moyenne


## Verdict

**Non : un LLM dense n'expose pas de grappes naturelles le long de la dimension
cachée.** Le test est sans ambiguïté — grappes apprises sur la couche 0, testées
sur les couches 1-3 : **27,5 % contre 27,5 % pour une partition aléatoire (1,00×)**.
Aucune information ne passe d'une couche à l'autre. Le gain d'encodage par
réordonnancement est de **1,00×**, ce qui confirme qu'il n'y a rien à réordonner.

⚠️ Mon premier test était **circulaire** (grappes apprises sur les matrices
ensuite mesurées) et laissait croire à un effet de 1,56× : c'était l'effet
mécanique du « max sur G parts », reproduit à l'identique par une partition
aléatoire.

### Ce que le modèle réel expose quand même

1. **Hétérogénéité de magnitude massive** : dans `attn_output`, **95,9 %** des
   poids sont sous 5 % du maximum ; 73,8 % dans `ffn_gate`. C'est le phénomène
   des poids aberrants — le levier de l'élagage *avec calibration* (SparseGPT),
   pas de la clustérisation.
2. **Structure explicite par têtes (GQA)** : 14 têtes de requête pour 2 têtes KV
   (groupement 7:1), et l'énergie par tête va de **1,4 % à 28,5 %** (uniforme :
   7,1 %) — soit un facteur 20 de spécialisation. Les têtes sont par ailleurs
   quasi orthogonales (similarité moyenne 0,020).

### Conséquence

Le découpage en sous-modèles **ne peut pas révéler** une structure qui n'existe
pas : **il doit l'imposer à l'entraînement**. C'est une bonne nouvelle — l'essai
précédent a montré que l'imposer ne coûte rien (74,12 % contre 74,12 % pour le
meilleur dense à budget égal), et qu'elle divise le coût des positions par deux
(0,39 contre 0,79 b/poids).

Seule structure réellement préexistante et exploitable : **les têtes GQA**, déjà
groupées 7:1 par construction.

---
*Généré par `run_real_clusters.py` — Drave.*

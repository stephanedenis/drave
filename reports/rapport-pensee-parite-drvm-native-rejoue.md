# B13 — la parité DRVM/native **rejouée** : checkpoint régénéré en CPU, 5/5 prompts, écart 0,00005

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ✅ **la parité est
> reproductible de bout en bout** — le checkpoint et le DRVM ont été régénérés à neuf en **CPU**
> (44,9 s, `--device cpu`, `CUDA_VISIBLE_DEVICES=""`), puis la parité Rust natif ↔ Python donne
> **5/5 top-1, 5/5 top-5, écart max 0,00005**. N2 n'a pas été touché.

## 1. Ce qui a été fait

1. **Régénération** : `entrainer_native.py --device cpu --pas 200 --sortie /tmp/drave-n0-pont.pt
   --drvm /tmp/drave-n0-pont.drvm` → **44,9 s**, `sha256` du DRVM noté.
2. **Parité** : `verifier_parite_native.py` compare les 5 logits du Rust
   (`drave-core/target/release/drave --drvm-forward`) à la référence PyTorch.
3. **Le piège mesuré** : le script compare à `/tmp/n0-native.drvm` **codé en dur** ; sans ce
   fichier, la première passe donne **0/5 et écart 999** (mesuré). Après copie du DRVM frais
   (même `sha256`), **5/5**.

## 2. Les résultats

| prompt | top-1 | top-5 | écart max |
|---|---|---|---|
| `La France est un pays` | ✅ | ✅ | 0,00005 |
| `Le chat dort sur` | ✅ | ✅ | 0,00005 |
| `Demain, nous irons` | ✅ | ✅ | 0,00003 |
| `def addition(a, b):` | ✅ | ✅ | 0,00004 |
| `Once upon a time` | ✅ | ✅ | 0,00005 |
| **total** | **5/5** | **5/5** | **0,00005** |

## 3. Le contrôle négatif

- **Avant** la copie du DRVM : **0/5**, écart **999** — le banc échoue proprement quand le fichier
  comparé manque, il ne « passe » pas par hasard.
- **Après** : 5/5, écart 0,00005 — la parité tient sur un checkpoint **régénéré**, pas seulement sur
  celui de la veille.
- **Sans GPU** : `CUDA_VISIBLE_DEVICES=""` ; aucune mesure GPU ; N2 intact.

## 4. Ce qui pourrait rendre ce résultat faux

- Le checkpoint et le DRVM vivent dans `/tmp` : à régénérer avant tout rejeu (44,9 s CPU).
- 5 prompts fixes : parité de **logits**, pas de perplexité.
- ~~Le script code en dur `/tmp/n0-native.drvm`~~ : **corrigé** — `--checkpoint`, `--drvm`,
  `--binaire`, `--sortie` (défaut `/tmp/drave-n0-pont.drvm`).
- La régénération repart de la graine 1 et de 200 pas : ce n'est pas le checkpoint exact de la
  veille, c'est un checkpoint **équivalent par construction** (même recette).

## 5. La suite

1. **Corriger** `verifier_parite_native.py` : prendre le DRVM en argument (fin du chemin codé en dur).
2. **Rejouer** les deux parités dans une porte (`tools/toutes-les-portes.sh`).
3. Le lien (plafond 5/10) reste le chantier suivant.

## 6. Fichiers

- [`pensee-parite-drvm-native-rejoue.json`](pensee-parite-drvm-native-rejoue.json) — la mesure et
  le sha256.
- [`native-parite.json`](native-parite.json) — la sortie brute du banc.
- [`tools/verifier_parite_native.py`](../tools/verifier_parite_native.py) — le banc.

# N0.8 — parité native automatisée : 5/5 prompts, écart < 0,0001

> **Objet.** Le N0.7 ne vérifiait qu’un prompt. Ici, cinq prompts fixes sont comparés
> automatiquement entre Python et le Rust natif.

## Résultat

| prompt | top-1 | top-5 | écart max |
|---|---|---|---|
| `La France est un pays` | ✅ | ✅ | 0,00006 |
| `Le chat dort sur` | ✅ | ✅ | 0,00004 |
| `Demain, nous irons` | ✅ | ✅ | 0,00005 |
| `def addition(a, b):` | ✅ | ✅ | 0,00005 |
| `Once upon a time` | ✅ | ✅ | 0,00004 |
| **total** | **5/5** | **5/5** | **< 0,0001** |

- Code : [`tools/verifier_parite_native.py`](../tools/verifier_parite_native.py).
- DRVM : `/tmp/n0-native.drvm` (11 469 192 paramètres).
- Aucun tirage aléatoire : liste de prompts fixe.

## Lecture

- La parité **tient sur cinq prompts**, pas seulement sur celui de N0.7.
- L’écart maximal est **0,00006**, compatible avec l’ordre des additions f32.
- Le test est **reproductible** : même binaire, même DRVM, mêmes prompts.

## Verdict

**N0.8 est atteint** : la parité native DRVM est **automatisée** et **multi-prompt**.

## Limites

- **Cinq prompts courts** ; pas de contexte long.
- **Pas de PPL native** ; seulement les logits de la dernière position.
- **Pas de test unitaire Rust** : le test est un script Python qui appelle le binaire.
- **Un seul modèle**.

## Fichiers

- Code : [`tools/verifier_parite_native.py`](../tools/verifier_parite_native.py).
- JSON : [`native-parite.json`](native-parite.json).

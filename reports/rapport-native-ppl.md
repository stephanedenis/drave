# N0.12 — PPL native de bout en bout : 4,6585, identique à Python

> **Objet.** Calculer une perplexité **native** avec le cache KV, sur un texte octet, et la comparer
> au même calcul PyTorch.

## Dispositif

- DRVM : `/tmp/n0-native.drvm`, **11 469 192** paramètres.
- Texte : `La France est un pays de la couche huit et le reste du monde`, **59 octets notés**.
- CLI : `drave --drvm-native-ppl FILE "texte"`.
- Cache KV par bloc et par tête ; chaque position est notée une seule fois.

## Résultat

| mesure | Rust natif | Python |
|---|---:|---:|
| PPL | **4,6585** | **4,658519** |
| octets notés | 59 | 59 |
| écart | — | **< 0,0001** |

## Lecture

- La PPL native est **identique** à la référence Python.
- Ce n'est pas la PPL de validation (3,58) : c'est un **texte court et choisi** ; les valeurs ne sont
  pas comparables.
- Le calcul passe par le cache : **59 passes** de un jeton, pas 59 passes complètes.

## Verdict

**N0.12 est atteint** : PPL native de bout en bout, parité Python.

## Limites

- **59 octets**, un seul texte.
- **Pas** de PPL sur un corpus complet ; le coût reste linéaire mais le texte est court.
- **Un seul modèle**.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- JSON : [`native-ppl.json`](native-ppl.json).

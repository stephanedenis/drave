# N0.14 — PPL native sur 1 996 octets : 54,0379, Python 54,0343

> **Objet.** Passer de 1 076 à près de 2 000 octets, limite de `max_pos=2048`, et vérifier la
> parité native sur un texte plus long.

## Dispositif

- DRVM : `/tmp/n0-best.drvm`, **11 469 192** paramètres, **PPL validation 2,708**.
- `data/corpus_fr_val.txt`, **1 900 caractères** = **1 996 octets** notés.
- CLI : `drave --drvm-native-ppl FILE "@fichier" 1900`.
- **2 098 octets** échouent : `max_pos=2048` (IndexError Python, troncature Rust).

## Résultat

| mesure | Rust natif | Python |
|---|---:|---:|
| PPL | **54,0379** | **54,0343** |
| octets notés | 1 996 | 1 997 |
| écart | — | **0,0036** |

## Lecture

- La parité **tient** sur 1 996 octets, avec un écart de **0,0036** dû à l'accumulation f32.
- La PPL **54** n'est **pas** la validation **2,708** : c'est un texte **sans contexte**, et le
  modèle est **hors de sa fenêtre d'entraînement** (128 octets).
- La limite **2 048** est atteinte : au-delà, Python échoue et Rust tronque la position.

## Verdict

**N0.14 est atteint** : PPL native sur 1 996 octets, parité à **0,0036**.

## Limites

- **1 996 octets**, pas le corpus.
- **Hors fenêtre** d'entraînement (128) : la valeur n'est pas une qualité de modèle.
- **Un seul modèle**.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- JSON : [`native-ppl-2k.json`](native-ppl-2k.json).

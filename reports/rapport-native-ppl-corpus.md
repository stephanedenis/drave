# N0.13 — PPL native sur 1 076 octets : 18,6394, identique à Python

> **Objet.** passer d'un texte de 59 octets à un vrai début de corpus et vérifier que la PPL native
> tient sur 1 024 caractères.

## Dispositif

- DRVM : `/tmp/n0-native.drvm`, 11 469 192 paramètres.
- Fichier : `data/corpus_fr_val.txt`, **1 024 premiers caractères** = **1 076 octets** notés.
- CLI : `drave --drvm-native-ppl FILE "@data/corpus_fr_val.txt"`.
- **12,5 s** CPU.

## Résultat

| mesure | Rust natif | Python |
|---|---:|---:|
| PPL | **18,6394** | **18,6395** |
| octets notés | 1 076 | 1 077 |
| écart | — | **0,0001** |

## Lecture

- La PPL native **tient** sur 1 076 octets, pas seulement sur 59.
- La valeur **18,6** est élevée parce que le texte commence **au milieu** du corpus, sans contexte
  d'entraînement ; elle n'est **pas comparable** à la PPL de validation (3,58).
- Les deux comptes diffèrent d'un octet (1 076 / 1 077) : découpage caractère/octet, sans effet
  mesurable sur la PPL.

## Verdict

**N0.13 est atteint** : PPL native de corpus court, parité Python à 0,0001.

## Limites

- **1 024 caractères** ; pas le corpus complet.
- **12,5 s** CPU pour 1 076 octets : le moteur natif est scalaire.
- **Un seul modèle**.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- JSON : [`native-ppl-corpus.json`](native-ppl-corpus.json).

# R13.1 — le BPE natif gagne 11,9 % de bits/octet à budget d’octets égal

> **Ligne de roadmap** : R13.1 · **Date** : 2026-10-29 · **Verdict** : ✅ **le BPE natif bat
> l’octet** — à budget d’**octets** égal (~405–410 k octets vus), le modèle BPE 512 fait
> **3,249 bits/octet** contre **3,689** pour le modèle octets, soit **−11,9 %**. Le tokenizer
> est **réversible** (1,977 octet/jeton). La condition R13.1 « pas de modèle BPE natif » est levée.
>
> **Dispositif** : `tools/tokenizer_bpe.py` + `tools/entrainer_native_tokens.py`, corpus
> `data/corpus_fr.txt`, mêmes architecture/graine/seed ; porte `tools/porte-r13-bpe.sh` ;
> données [`r13.1-bpe.json`](r13.1-bpe.json).

## Ce qui est mesuré

| modèle | vocab | paramètres | PPL/jeton | bits/octet | octets vus |
|---|---:|---:|---:|---:|---:|
| octets, 200 pas | 256 | 11 814 792 | 14,11 | 3,818 | 204 800 |
| octets, 400 pas | 256 | 11 814 792 | 12,90 | **3,689** | 409 600 |
| **BPE, 200 pas** | **512** | 12 448 136 | 85,83 | **3,249** | 404 864 |

- **Budget d’octets** : 409 600 (octets 400 pas) contre 404 864 (BPE 200 pas × 1,977), écart
  **−1,2 %**.
- **Gain BPE** : `(3,689 − 3,249) / 3,689 = 11,9 %`.
- **Contrôle des données** : passer de 200 à 400 pas octets améliore de **3,3 %**
  (3,818 → 3,689) ; le BPE garde **11,9 %** à octets comparables.
- **Tokenisation** : 4 633 889 octets → 2 344 050 jetons ; **réversible** exactement.

## Le contrôle négatif

- **Mêmes graine, architecture, corpus, évaluation** ; seul le tokenizer et le vocabulaire changent.
- **Budget d’octets** aligné à 1,2 % ; la porte refuse un écart > 3 %.
- **Le gain de données est mesuré** (octets 200 → 400) et ne suffit pas à expliquer le BPE.
- **Réversibilité** : le décodage redonne le texte exact ; un tokenizer qui perd des octets serait
  disqualifié avant la comparaison.

## Ce qui pourrait le rendre faux

- **Français seulement** ; 512 jetons ; 200/400 pas ; une graine.
- **Le modèle BPE a 5,4 % de paramètres en plus** (embedding/tête 512 contre 256) ; le gain
  n’est pas « à paramètres égaux ».
- **La PPL par jeton du BPE est élevée** (85,8) : c’est le bits/octet qui compte ici.
- **Pas de contexte long** ; la comparaison porte sur des fenêtres de 128 jetons.

## Ce que ça décide

**R13.1 est mesuré** : le BPE natif l’emporte sur ce corpus et ce budget. La condition
« aucun checkpoint BPE natif » est levée. Le prochain pas est **vocab 1024**, l’**anglais/
multilingue** et plus de pas — pas un retour à la condition.

## Fichiers

- `tools/tokenizer_bpe.py` — tokenizer BPE 512 réversible.
- `tools/entrainer_native_tokens.py` — trainer à vocabulaire variable.
- `tools/porte-r13-bpe.sh` — la porte.
- `reports/r13.1-bpe.json` — les mesures.
- `reports/rapport-r13.1-bpe.md` — cette fiche.

# 2026-11-15 — Documentation, état, conventions

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (3)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 02:00 | `5891ef8a` | ÉTAT — T0 TENU : LA LIGNE FAIT RACCOURCIE | `en-cours.md`, `README.md`, `mesures.md` (+6) |
| 03:51 | `01b6db6e` | JOURNAL — 2026-11-15 : B2, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX (NÉGATIF CONTRÔLÉ ; LE STYLE EST ABSORBÉ PAR LA DATE) | `README.md`, `mesures.md`, `README.md` (+4) |
| 04:30 | `c24253ee` | DOC PRODUIT — LA PASSE D'HONNÊTETÉ : LES TROIS BASES (612, 602, RÉEL 452), L'ATTACHEMENT 238/239, LE TAGGER 95,75, LES CHIFFRES DATÉS ANNOTÉS | `en-cours.md`, `README.md`, `README.md` (+5) |

## Sessions actives ce jour

- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 348.0 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)

<!-- notes -->
### D1 — les exemples du tagger et de la base réelle

`docs/produit/exemples.md` passe à **dix** blocs. **Trois** exécutions `--tagger` avec la clé et un
cache neuf affichent le **coût réel** : `g001` neutre (130 tokens), `g011` répare `lu` NOUN → VERB
(157 tokens), `r241` répare `when` CONJ → PRON (154 tokens) — **14/17 → 16/17** sur 17 tokens,
**441 tokens** et **3,7 s** pour les trois. **Deux** exécutions `--reel` donnent la base honnête :
**452 phrases**, POS **0,8891**, F1 **0,7906**, attachement **183/184 = 0,9946**. Les cinq blocs
sont rejoués **5/5** ; la doc mutée (`lu/VERB` → `lu/NOUN`) est détectée **4/5** ; les trois
annotations `--tagger` passent le schéma **v2**. Le code courant ne bouge pas : F1 **0,7902**,
**238/239** cibles. [`fiche`](../../reports/rapport-exemples-tagger.md).
<!-- /notes -->

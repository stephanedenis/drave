# 2026-11-15 — Documentation, état, conventions

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (13)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 02:00 | `5891ef8a` | ÉTAT — T0 TENU : LA LIGNE FAIT RACCOURCIE | `en-cours.md`, `README.md`, `mesures.md` (+6) |
| 03:51 | `01b6db6e` | JOURNAL — 2026-11-15 : B2, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX (NÉGATIF CONTRÔLÉ ; LE STYLE EST ABSORBÉ PAR LA DATE) | `README.md`, `mesures.md`, `README.md` (+4) |
| 04:30 | `c24253ee` | DOC PRODUIT — LA PASSE D'HONNÊTETÉ : LES TROIS BASES (612, 602, RÉEL 452), L'ATTACHEMENT 238/239, LE TAGGER 95,75, LES CHIFFRES DATÉS ANNOTÉS | `en-cours.md`, `README.md`, `README.md` (+5) |
| 04:48 | `e42bac4f` | JOURNAL — 2026-11-15 : D1, LES EXEMPLES --tagger (441 TOKENS, 3,7 S) ET --reel (452 PHRASES) SONT DANS LA DOC ; 5/5 REJOUÉS, MUTATION 4/5 | `README.md`, `distribue.md`, `docs.md` (+8) |
| 07:32 | `2b7e520b` | ÉTAT — T0 VERT | `en-cours.md`, `README.md`, `distribue.md` (+9) |
| 07:35 | `49011807` | ÉTAT — T0 VERT (LA LIGNE FAIT NETTOYÉE, COQUILLE CORRIGÉE) | `en-cours.md`, `README.md`, `docs.md` (+4) |
| 07:47 | `8cb0a926` | PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE CONTRÔLÉE, RESTITUTION V3, TAGGER PAR DÉFAUT ? | `en-cours.md`, `semaine-2.md`, `README.md` (+12) |
| 08:08 | `6b2208ee` | PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE, RESTITUTION v3, LE TAGGER PAR DÉFAUT ? ; LA FILE DU CHANTIER À 41 TÂCHES | `en-cours.md`, `README.md`, `distribue.md` (+12) |
| 12:35 | `2b5bd1cd` | JOURNAL — RÉGÉNÉRÉ APRÈS LA CLÔTURE DE LA SEMAINE 2 (W1-W6) ; LE TAG semaine-2-2026-11-20 REPOSÉ SUR LE COMMIT W5 | `en-cours.md`, `README.md`, `distribue.md` (+15) |
| 14:01 | `158dee4d` | ÉTAT — LA SEMAINE 2 INSCRITE : GOLD 452, TAGGER 402/H50, MATRICE DU DÉFAUT, PANINI 26 SIGNATURES, RESTITUTION v3, PAGE /, TAGGER EN LOT | `en-cours.md`, `README.md`, `distribue.md` (+13) |
| 14:43 | `a1c45477` | ÉTAT — T0 TENU (LES LIGNES R ET N RACCOURCIES) | `en-cours.md`, `README.md`, `memoire.md` (+4) |
| 14:49 | `75dc9259` | ÉTAT — T0 VERT | `en-cours.md`, `README.md`, `distribue.md` (+10) |
| 14:52 | `b8248b2d` | ÉTAT — T0 VERT (LA LIGNE W5 RACCOURCIE) | `en-cours.md`, `README.md`, `distribue.md` (+10) |

## Sessions actives ce jour

- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 365.4 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)

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

### E1 — la FAQ entre au sommaire, ses liens sont vérifiés

La FAQ de `docs/produit/README.md` (§ 8) n'était listée ni dans un sommaire du document, ni
dans le « Où aller ensuite » du § 9, ni dans la table **Produit** de `docs/README.md`. Le
document gagne un **sommaire de neuf entrées** (la huitième est la FAQ), le § 9 une ligne
FAQ, et `docs/README.md` sa ligne (ancre `#8-faq--dix-questions`, **995/1000** mots). Les
**cinq liens** de § 8 et les **neuf ancres** du sommaire résolvent : **0 mort**. Le contenu
des **dix réponses** ne bouge pas — sha256 `8855b475…` avant et après. Dispositif
[`tools/verifier_liens_faq.py`](../../tools/verifier_liens_faq.py), contrôle négatif **2/2**
(fichier absent, ancre absente) ; fiche
[`reports/rapport-faq-sommaire.md`](../../reports/rapport-faq-sommaire.md) et
[`reports/faq-sommaire.json`](../../reports/faq-sommaire.json).

### W5 — l'état et la roadmap après la restitution v3

`docs/pilotage/en-cours.md` passe à **753** fichiers / **846** JSON, la session Pensée reçoit
W5 (gold v2 **20/46**, F1 **0,5406** ; gold S **144/144**, cinq rôles **18/18**), et la prochaine
action devient **J4 — l'or de rôles**. `docs/pilotage/roadmap.md` marque W5 dans la ligne **R**
et dans l'état B13 ; `reports/README.md` et `reports/INDEX.md` reçoivent la fiche.
<!-- /notes -->

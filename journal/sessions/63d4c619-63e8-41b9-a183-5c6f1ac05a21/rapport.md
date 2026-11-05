# Session 63d4c619 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `63d4c619-63e8-41b9-a183-5c6f1ac05a21` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 13:11 |
| Durée | 0.6 h |
| Tours | 1 |
| Messages | 53 |
| Appels d'outils | 70 |
| Fichiers touchés | 1 |
| Commandes | 53 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, dépôt Python). Mission : **audit de reproductibilité** de la mesure d'attachement du bloc linguistique.  Contexte : `tools/tests/linguistique/evaluer_gold.py` expose `charger()` (gold de 612 phrases) et `evaluer_bloc(nom, bloc, phrases)` ; `tools/bloc_linguistique.py` expose `Heuristique`. Les valeurs publié … [1967 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, dépôt Python). Mission : **au … [2247 caractères tronqués]

*70 appels d'outils.* Actions notables :

- bash — Check git status, branch, and reports dir
- bash — List linguistique tests and count lines
- read
- bash — List pensee reports and sizes
- bash — Display the five JSON reports
- bash — Locate key symbols in bloc_linguistique
- bash — Find generators/references of the reports
- bash — Count phrases per gold file
- bash — Read the five markdown sheets
- bash — Run evaluer_bloc on 612 gold phrases
- bash — Check code state and submodule status
- bash — Compute lost attachment spans by type
- bash — Find span category protocol and GP fix
- bash — Search scripts for span categories
- … et 53 autres

**Synthèse produite :**

⏵ Closing the audit and reporting figures

\## Audit de reproductibilité — attachement (B13)

**Verdict : ✅ les 14 valeurs publiées reproduisent exactement, écart 0.** Mesure rejouée sur `s/v7` au commit `e1171032`, `bloc_linguistique.py` sha256 `d9c9d559…`, `evaluer_gold.py` sha256 `dbbcfe90…`, gold 612 phrases (20 `hand` + 432 `reel` + 160 synthétiques), `Heuristique()` aux défauts, durée ~0,5 s.

| mesure | mesuré | publié | écart |
|---|---:|---:|---:|
| cibles | 239 | 239 | 0 |
| labels | 145 | 145 | 0 |
| top1 | 126 | 126 | 0 |
| top-k (sous-chaîne) | 134 | 134 | 0 |
| exact | 123 | 123 | 0 |
| top-k strict | 88 | 88 | 0 |
| couverture | 0,6067 | 0,6067 | 0 |
| cibles verbes / justes | 63 / 60 | 63 / 60 | 0 |
| cibles noms / justes | 82 / 63 | 82 / 63 | 0 |
| spans perdus REL / SUB / GP | 48 / 33 / 13 | 48 / 33 / 13 | 0 |

Taux dérivés : top1 0,8690 des labels ; top-k 0,9241 ; exact 0,8483 ; strict 0,6069 ; verbes 0,9524 ; noms 0,7683 ; F1 syntagmes 0,2862 (P 0,3154, R 0,2619). Catégories de spans courantes : 65 aucun / 24 plus large / 4 plus étroit / 1 coupe.

**Contrôle négatif** (graine 20261105, 1 000 tirages) : permutation des cibles gold **1,12 %** (1,62/145, max 7) ; candidat aléatoire **27,42 %** (39,75/145) ; contrôle du harnais **0,42 %** (1/239). Observé **84,83 %** (123/145), soit 76× la permutation et 3,1× le candidat aléatoire. Nuance : exact et top-k strict ne mesurent pas le même objet (82 labels exacts et stricts, 41 exacts hors liste stricte, 6 cibles présentes mal choisies).

\### Écarts constatés — dans les JSON, pas dans les valeurs auditées

- `pensee-topk-strict.json` (`e223a98d`) et `pensee-echecs-cible.json` (`a048cb83`) : **reproduisent à l'identique**.
- `pensee-conventions.json` (`f70a1b2a`) et `pensee-attachement-cible.json` (`23853cb7`) : **instantanés antérieurs**. Ils publient 146 labels, exact 118 (0,8082), top1 122 (0,8356), 48/51 verbes, 70/95 noms ; rejoués à leur commit, ils sont exacts — mais l'état courant est 145 / 123 / 126 / 60-63 / 63-82.
- `pensee-spans.json` : sa version committée publie **12 GP / 93 spans** (bloc `spans`, état « après » `13e8bb2d`), alors que le chiffre audité est **13 GP / 94** (état courant, = bloc « avant » `d400e188`). Les deux blocs reproduisent à leurs commits ; aucun n'est l'état courant. Le lexique élargi `a408a909` (10:39) a ramené 146→145 labels, GP 12→13, F1 0,2869→0,2862 et exact 118→123 ; stable depuis `a048cb83`.

Un autre agent a ajouté pendant l'audit un bloc `courant` à `pe
… [542 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-attachement.md` | 1 | 11 |

### Commandes exécutées (échantillon)

- **T1** Check git status, branch, and reports dir
- **T1** List linguistique tests and count lines
- **T1** List pensee reports and sizes
- **T1** Display the five JSON reports
- **T1** Locate key symbols in bloc_linguistique
- **T1** Find generators/references of the reports
- **T1** Count phrases per gold file
- **T1** Read the five markdown sheets
- **T1** Run evaluer_bloc on 612 gold phrases
- **T1** Check code state and submodule status
- **T1** Compute lost attachment spans by type
- **T1** Find span category protocol and GP fix
- **T1** Search scripts for span categories
- **T1** Read T165-T168 autotests
- **T1** Read syntagme generation and GP handling
- **T1** Compute target failure breakdown
- **T1** Check commit history of code and reports
- **T1** Compute negative controls and F1
- **T1** Diff code since spans report and submodule state
- **T1** Inspect S-generator import and source
- **T1** Check submodule data dependency and S output
- **T1** Show code changes since spans report
- **T1** Inspect imports and pin file hashes
- **T1** Extract historic bloc versions to /tmp
- **T1** Replay historic commits' measurements
- **T1** Replay historic commits with registered modules
- **T1** Replay parent commit before spans report
- **T1** List spanning predictions for lost gold spans
- **T1** Recompute categories with split rule
- **T1** Replay failure breakdown across commits
- **T1** Replay lexicon-expansion commit
- **T1** Run consolidated audit measurement script
- **T1** Show pinned device metadata and current HEAD
- **T1** Re-run measurement and compare determinism
- **T1** Diff measurements excluding duration
- **T1** Cross-tabulate exact vs candidate presence
- **T1** Verify the two target files do not exist
- **T1** Verify pinned commit hashes match working tree
- **T1** Generate and validate the audit JSON
- **T1** Inspect final JSON key values
- … et 13 autres

## 4. Mesures et résultats marquants

- **T1** `- **La mesure globale cachait l'écart** : 0,6438 = moyenne pondérée (51 × 0,73 + 95 × 0,60).`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : ===== 13e8bb2d ===== f70a1b2a ===== 23853cb7 ===== a048cb83 ===== e223a98d [stderr] Traceback (most recent call last):   File "<stdin>", line 7, in <module>   File "<frozen importlib._bootstrap_extern


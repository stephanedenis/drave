# Session 29ad180d — Session structures CPU analyseur rôles

> **Journaux :** [le jour](../../2026-11-02/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `29ad180d-38a5-4481-a9a7-ec6ab31c895f` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-02 16:14 |
| Durée | 0.7 h |
| Tours | 2 |
| Messages | 140 |
| Appels d'outils | 154 |
| Fichiers touchés | 9 |
| Commandes | 98 |
| Sous-agents | 0 |
| Commits | 5 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es la session S (les structures, CPU). Lis AGENTS.md, docs/pilotage/en-cours.md,  docs/theorie/jeux-symboliques.md et tools/structures/ (sous-module heads/fusion). Ton id est  dans `printenv DSH_SESSION_ID` ; crée journal/sessions/<id>/plan.md avec  `python3 tools/sessions.py --modele` (État : actif, heartbeat maintenant), réserve  `tools/structures/`, ses exports et sa banque. Prochaine action … [285 caractères tronqués]

**Tour 2** — mets le dossier copilotage à jour

## 2. Déroulé, étape par étape

### Tour 1 — Tu es la session S (les structures, CPU). Lis AGENTS.md, docs/pilotage/en-cours.md,  docs/theorie/jeux-symboliques.md et … [565 caractères tronqués]

*129 appels d'outils.* Actions notables :

- bash — Get session id and git status
- read
- bash — Inspect repo root and tools/structures
- bash — Inspect sessions tool usage and status
- bash — Inspect structures submodule and reports
- bash — Inspect submodule branches and fusion tree
- bash — Locate analyseur report, corpus, and plan template
- bash — Compare fusion and analyse branches
- bash — Check branch graph, generateur diff, run tests
- bash — Read sessions.py first half
- bash — Inspect pre-commit hook and state checker
- bash — Search hub coordination mechanism
- bash — Read sessions.py second half
- bash — Read date and plan-travail territory rules
- … et 92 autres

**Synthèse produite :**

⏵ Cycle S clos côté code ; la fiche attend le hub pour la ligne d'état.

**Fait — analyseur rôles/subordonnées + export**

- **Gold** : 39 phrases (`dev` 7, `test` 16, `holdout` 16), dans `tools/structures/donnees/gold-analyseur.json`.
- **Mesure** (`mesure_analyseur.py`) : types **38/39** (97,4 %), rôles **99/100** (99 %), compléments **45/45**, couverture **1 156/1 161** (99,6 %).
- **Contrôles** : baseline à rôle constant **64/100** ; règles coupées **66/100** ; rôles mélangés **0,099** [0,00–0,22] sur 200 permutations ; `verifier_corpus.py --autotest` refuse un span corrompu.
- **Échec nommé** : `h033` — « La femme parle » est lu comme un GN, le verbe sans auxiliaire est avalé. Non corrigé par une liste apprise sur le holdout.
- **Export** : `data/structures/banque.jsonl`, **39 lignes**, SHA-256 `973c70a4…cd7db71` ; modes `banque` (0 ligne, aucun verdict humain — nommé) et `reference` (7 lignes). Manifeste copié dans `reports/s-banque-structures.json`.
- **Tests** : **40/40** verts, dont les 19 d'origine.

**Commits**

- Sous-module : **`647205a`** (committé dans son dépôt avant le pointeur).
- Pointeur principal : **`13f4e131`**, avec le journal du jour.
- Plan de session + bloc d'état proposé : dans **`e420267a`** (le hub l'a intégré au journal), section « Ligne d'état proposée au hub ».

**Reste un geste du hub** — je n'ai pas touché à `en-cours` :

- committer [`reports/rapport-s-analyseur-roles.md`](reports/rapport-s-analyseur-roles.md) et [`reports/s-banque-structures.json`](reports/s-banque-structures.json) avec la section S du plan ;
- compteurs **551 fiches / 637 JSON** (au lieu de 550/636), `reports/INDEX.md`, ligne roadmap **S**.

`revue_documentation.py` signale exactement ces deux compteurs : c'est l'écart attendu tant que la fiche n'est pas intégrée. `verifie_en_cours`, `verifie_journal`, `porte-tableaux`, `verifier_schemas` et `sessions.py --check --strict` passent.

**Prochaine action S** : validation humaine de la banque (le mode `banque` est à zéro), puis frontière du GN sans auxiliaire (`h033`) et gold plus large (voix, causatives).

Reproduction : `cd tools/structures && python3 -m unittest discover -s tests && python3 mesure_analyseur.py && python3 exporter_corpus.py && python3 verifier_corpus.py ../../data/structures/banque.jsonl`.

### Tour 2 — mets le dossier copilotage à jour

*25 appels d'outils.* Actions notables :

- read
- bash — Get current report/JSON counts before editing state
- bash — Get real time for state timestamps
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md`
- bash — Run documentation and state checks after edits
- bash — Run tables and size checks, inspect diff
- … et 9 autres

**Synthèse produite :**

⏵ Mise à jour de `docs/pilotage/` : état S, compteurs et roadmap, puis commit avec la fiche.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md` | 3 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/gold-analyseur.json` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py` | 0 | 7 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/mesure_analyseur.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_corpus.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/verifier_corpus.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 7 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 5 |

### Commandes exécutées (échantillon)

- **T1** Get session id and git status
- **T1** Inspect repo root and tools/structures
- **T1** Inspect sessions tool usage and status
- **T1** Inspect structures submodule and reports
- **T1** Inspect submodule branches and fusion tree
- **T1** Locate analyseur report, corpus, and plan template
- **T1** Compare fusion and analyse branches
- **T1** Check branch graph, generateur diff, run tests
- **T1** Read sessions.py first half
- **T1** Inspect pre-commit hook and state checker
- **T1** Search hub coordination mechanism
- **T1** Read sessions.py second half
- **T1** Read date and plan-travail territory rules
- **T1** Inspect work/n2w and data layout
- **T1** Inspect unmerged analyse branch bank and exporter
- **T1** Check gitignore, bank files, hub plan
- **T1** Dump phrases and reference candidates
- **T1** Run analyzer measurement and sample output
- **T1** Trace bank and export history
- **T1** Main repo status and export references
- **T1** Check gitignore and other session plans
- **T1** Check tracked data precedent
- **T1** Read results method
- **T1** Print official session plan template
- **T1** Validate session plan and check overlaps
- **T1** Read real current time
- **T1** Fix heartbeat and reserved files line
- **T1** Inspect parsed plan fields
- **T1** Clean reserved list and recheck
- **T1** Move reservation note to separate section
- **T1** Baseline analyzer output on candidate gold phrases
- **T1** Validate gold spans
- **T1** Run existing tests after analyzer changes
- **T1** Compare analyzer output to gold
- **T1** Compare analyzer output to gold (fixed)
- **T1** Add 8 holdout phrases after rules
- **T1** Patch coverage weighting and run measurement
- **T1** Inspect holdout type failure
- **T1** Add copula predicate rule and remeasure
- **T1** Add second holdout and run once
- … et 58 autres

## 4. Mesures et résultats marquants

- **T1** `n2-analyse            c7232b3 ANALYSEUR — L'ADVERBE DE TEMPS ET LE « QU'ELLE » : 7/7 SÉQUENCES, 94 % DE COUVERTURE`
- **T1** `| | * c7232b3 (n2-analyse) ANALYSEUR — L'ADVERBE DE TEMPS ET LE « QU'ELLE » : 7/7 SÉQUENCES, 94 % DE COUVERTURE`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `129:- **S — le banc de structures** : outil web (`tools/structures`), générateur, pragmatique (niveaux 0–4), export ; analyseur **7/7** séquences, **93,9 %** de couverture, **19 tests** ; [`analyseur``
- **T1** `[still running after 60000ms; moved to background job bash-67]`
- **T2** `34:| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v2** : rôles **contextuels** et subordonnées typées, gold **39** phrases ; analyseur **38/39** types`

## 5. Erreurs rencontrées

6 sorties en erreur ou divergentes. Les premières :

- **T1** : __pycache__/ *.pyc reports/*.tmp models/ data/ qtrinet-core/target/  # Traces de session : la copie brute reste sur disque (volumineuse, binaire), # le digest markdown est versionné. journal/sessions/
- **T1** : === data suivis === count: 0 === reports json exemples === reports/b102bis-corpus-jw.json reports/campagne-benefices/051-R-annexe-manifeste-des-journaux.md reports/corpus-genres.json reports/corpus-li
- **T1** : ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)   ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/w
- **T1** : p001 dev [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module>   File "<stdin>", line 6, in <genexpr> TypeError: list indices must be integers or slices, not str [exit code
- **T1** : 57048   57032       02:18 00:00:00  0.0 S    /bin/sh .git/hooks/pre-commit   59838   57048       01:05 00:00:47 73.3 R    python3 tools/session_report.py --quiet === io === PID 59838     ELAPSED     T
- **T1** : #!/usr/bin/env python3 """Produit, pour chaque session DSH, un rapport qui reconstitue son essence et démontre le travail accompli, étape par étape.  Sortie, à côté du digest brut :    journal/session

## 6. Commits

- S — L'ANALYSEUR NOMME LES RÔLES : 99/100, 38/39 TYPES ; LE CORPUS DE 39 STRUCTURES SORT" -m "Le générateur gagne des rôles contextuels (possession/thème, instru
- S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES" -m "Le sous-module tools/structures est committé dan
- ps -eo pid,etime,cmd | grep -E "git commit|archive_sessions|journal_auto|session_report|python3" | grep -v grep | head -20; echo "=== index lock ==="; ls -la /h
- ps -eo pid,ppid,etime,pcpu,stat,cmd | grep -E "57032|57052|57681|job|git commit" | grep -v grep; echo "=== enfants ==="; ps --ppid 57032 -o pid,etime,pcpu,stat,
- S — L'ÉTAT INTÈGRE L'ANALYSEUR RÔLES : 38/39 TYPES, 99/100 RÔLES, 39 STRUCTURES" -m "La fiche reports/rapport-s-analyseur-roles.md, le manifeste reports/s-banqu


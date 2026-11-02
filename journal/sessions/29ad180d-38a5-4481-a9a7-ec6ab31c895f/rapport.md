# Session 29ad180d — Session structures CPU analyseur rôles

> **Journaux :** [le jour](../../2026-11-02/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `29ad180d-38a5-4481-a9a7-ec6ab31c895f` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-02 16:14 |
| Durée | 1.1 h |
| Tours | 3 |
| Messages | 160 |
| Appels d'outils | 176 |
| Fichiers touchés | 9 |
| Commandes | 118 |
| Sous-agents | 0 |
| Commits | 7 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es la session S (les structures, CPU). Lis AGENTS.md, docs/pilotage/en-cours.md,  docs/theorie/jeux-symboliques.md et tools/structures/ (sous-module heads/fusion). Ton id est  dans `printenv DSH_SESSION_ID` ; crée journal/sessions/<id>/plan.md avec  `python3 tools/sessions.py --modele` (État : actif, heartbeat maintenant), réserve  `tools/structures/`, ses exports et sa banque. Prochaine action … [285 caractères tronqués]

**Tour 2** — mets le dossier copilotage à jour

**Tour 3** — commit l'ensemble

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

*35 appels d'outils.* Actions notables :

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
- … et 19 autres

**Synthèse produite :**

⏵ Pilotage S committé : fiche, manifeste, `en-cours` et roadmap à jour.

**Fait**

- **`63927a03`** — `reports/rapport-s-analyseur-roles.md`, `reports/s-banque-structures.json`, la section S d'`en-cours`, la ligne S de la roadmap et le plan de session.
- **`dca7e7a2`** — compteurs au disque : **552 fiches / 639 JSON**.
- La section S porte le fait (38/39 types, 99/100 rôles, 45/45 compléments, contrôles 64/100 · 66/100 · 0,099, échec h033, corpus 39 lignes SHA `973c70a4…`, 40 tests), le pointeur `13f4e131`, le sous-module `647205a` et la prochaine action.
- La roadmap porte S en ✅ v2, la phrase d'état, la file « jamais en attente » et la banque validée à 0 comme ligne bloquée nommée.

**Contrôles au commit** : `revue_documentation.py` ✅, T0 ✅, `en-cours` 1 626 mots ✅, `verifie_en_cours.py` ✅, `sessions.py --check` ✅, `verifie_etat_a_jour.py` ✅.

**À noter** : depuis le commit, la session **Pensée** écrit son gold neuronal dans `en-cours`/`roadmap` (fichiers modifiés, non committés ; mtime 17:01). Ces lignes — une 6e question, T0 à 4 105, `reports/README.md` à 2 809 — sont **son** intégration, pas celle de S : je ne les ai ni committées ni modifiées. Le hub/Pensée doit les finir en ramenant les questions à 5 et en coupant ~105 mots. Dis-moi si tu veux que je fasse cette coupe et que je commite l'ensemble.

Prochaine action S inchangée : **validation humaine de la banque**, puis frontière du GN sans auxiliaire (`h033`).

### Tour 3 — commit l'ensemble

*12 appels d'outils.* Actions notables :

- bash — Full worktree status before integration
- bash — Inspect other sessions' diffs
- bash — Inspect staged integration diff
- bash — Inspect untracked N2/OCR files and indices
- bash — Current gate state with staged integration
- read
- bash — Inspect en-cours D/R/A and header before editing
- bash — Add D/R/A detection, trim to budget, recheck
- bash — Stage D/R/A detection and state, inspect index
- bash — Check whether Pensée set was committed concurrently
- bash — Review staged en-cours delta and run checks
- bash — Commit D/R/A detection integration

**Synthèse produite :**

⏵ Intégration de l'ensemble : je vérifie les changements en cours, je remets les compteurs et les budgets au vert, puis je commite tout.

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
- … et 78 autres

## 4. Mesures et résultats marquants

- **T1** `n2-analyse            c7232b3 ANALYSEUR — L'ADVERBE DE TEMPS ET LE « QU'ELLE » : 7/7 SÉQUENCES, 94 % DE COUVERTURE`
- **T1** `| | * c7232b3 (n2-analyse) ANALYSEUR — L'ADVERBE DE TEMPS ET LE « QU'ELLE » : 7/7 SÉQUENCES, 94 % DE COUVERTURE`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `129:- **S — le banc de structures** : outil web (`tools/structures`), générateur, pragmatique (niveaux 0–4), export ; analyseur **7/7** séquences, **93,9 %** de couverture, **19 tests** ; [`analyseur``
- **T1** `[still running after 60000ms; moved to background job bash-67]`
- **T2** `34:| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v2** : rôles **contextuels** et subordonnées typées, gold **39** phrases ; analyseur **38/39** types`
- **T2** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4, A6.2 bloqués** ; A2.6 partiel ; A3.2/A3.3 mesurée`
- **T2** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T2** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v2** : rôles **contextuels** et subordonnées typées, gold **39** phrases ; analyseur **38/39** types (9`
- **T2** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T2** `| **B11** | la base d'universaux typés : schéma, [parseur](../theorie/glossaire/entrees/parseur.md), codec, contexte | ✅ | **B11.10 close** (cartes, ambiguïtés refusées) ; le codec lit **100 %** |`
- **T2** `| **C3.2** | les modules par famille de langues | ✅ | aucune — **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤ 0,5 %** |`
- **T2** `**Ce qui compte pour R** : le **codec classique** lit **100 %** des surfaces ; c'est la preuve qu'un bloc`
- **T2** `| **R0.2** | **[contrôleur de lecture](../theorie/glossaire/entrees/controleur-de-lecture.md)** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, tit`
- **T2** `| **R0.3** | **[banc de lecture rapide](../theorie/glossaire/entrees/banc-de-lecture-rapide.md)** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles`
- **T2** `-| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 langues`
- **T2** `+| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 langues`
- **T3** `**20 000 pas** × 8 × 128, lr 3e-4, graine 1, canal de structure — exactement la recette de`
- **T3** `- **Corpus** : `data/wiki_fr/propre/train.txt` (186 Mo) et son canal ; validation appariée`
- **T3** `8 lots × 16 fenêtres. Le **témoin** est le point N2.z (`base-34m-canal.pt`), repassé dans le`
- **T3** `| [rapport-pensee-hasard.md](rapport-pensee-hasard.md) | B13 — le hasard variable : 20–60 %, 20/20 à chaque taux |`
- **T3** `| [rapport-s-analyseur.md](rapport-s-analyseur.md) | S — L'analyseur contre les structures écrites à la main : 7/7 séquences, 93,9 % de couverture |`

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
- ÉTAT — COMPTEURS AU DISQUE (552 FICHES / 639 JSON) ; LA FICHE S EST INTÉGRÉE" -m "Le compteur passe à 552 fiches / 639 JSON après l'intégration de la fiche S et
- D/R/A — LA DÉTECTION CEGEP SÉPARE 147 SCANS DE 2 681 PDF ; L'OCR PASSE À LA LISTE EXPLICITE" -m "La détection sur le texte intégral (pdftotext + pdfinfo, seuil 


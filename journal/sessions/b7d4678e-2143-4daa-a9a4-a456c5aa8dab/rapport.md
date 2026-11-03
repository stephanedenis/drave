# Session b7d4678e — Reprise session L/B13 et vérification stricte

> **Journaux :** [le jour](../../2026-11-02/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `b7d4678e-2143-4daa-a9a4-a456c5aa8dab` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-02 16:16 |
| Durée | 3.5 h |
| Tours | 4 |
| Messages | 325 |
| Appels d'outils | 349 |
| Fichiers touchés | 18 |
| Commandes | 206 |
| Sous-agents | 0 |
| Commits | 6 |
| Compactages de contexte | 0 |

## Objectifs déclarés

- **create** — Session D/R/A (fe3c05f0) : OCR du fonds CEGEP restant (~127 scans) en sortie séparée, fusion et contrôle du corpus (10 notes + suite), fiche + JSON, en-cours + commit explicite, puis clôture de la session.
- **complete** — Session D/R/A (fe3c05f0) : OCR du fonds CEGEP restant (~127 scans) en sortie séparée, fusion et contrôle du corpus (10 notes + suite), fiche + JSON, en-cours + commit explicite, puis clôture de la session.

## 1. Ce qui a été demandé

**Tour 1** — Tu reprends la session L/B13 `e181ce02-cd50-488a-a6be-e84b79d40dcc`. Lis son plan, AGENTS.md  et docs/pilotage/en-cours.md. Remets `- **État** : actif` et `- **Heartbeat** : <maintenant>`  dans son plan, puis vérifie `python3 tools/sessions.py --check --strict`. Le cycle 140/140  (gold 432, 116 liens) est committé. Prochaine action : gold neuronal (qualifier un modèle  local) ; DRVM/native est blo … [114 caractères tronqués]

**Tour 2** — Tu reprends la session D/R/A `fe3c05f0-834b-44f2-8739-501865d652c1`. Lis son plan, AGENTS.md  et en-cours. Remets `État : actif` et heartbeat maintenant, puis  `sessions.py --check --strict`. Le texte intégral, le PDF, les 20 livres, les 10 notes CEGEP,  le glossaire (355 entrées) et docwatch sont committés. Prochaine action : OCR ~127 scans CEGEP  (`tools/ocr_pdf.py --racine CEGEP --deja <N>`), p … [87 caractères tronqués]

**Tour 3** — as-tu terminé? les gpu et cpu sont tranquilles

**Tour 4** — c'est le temps de s'assurer que le pilotage est bien a jour et concis afin que tout soit optimal avec les sessions en cours dans les autres terminaux

## 2. Déroulé, étape par étape

### Tour 1 — Tu reprends la session L/B13 `e181ce02-cd50-488a-a6be-e84b79d40dcc`. Lis son plan, AGENTS.md  et docs/pilotage/en-cours. … [394 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Show working directory and top-level files
- bash — Inspect sessions tool usage
- bash — List session directories
- bash — Show session status
- read
- bash — Show current date and time
- bash — Check git status and recent commits
- bash — Show current diff of the session plan
- bash — Peek AGENTS.md and count doc lines

**Synthèse produite :**

⏵ Reprise de la session L/B13 : lecture du plan, AGENTS.md et en-cours

### Tour 2 — Tu reprends la session D/R/A `fe3c05f0-834b-44f2-8739-501865d652c1`. Lis son plan, AGENTS.md  et en-cours. Remets `État  … [367 caractères tronqués]

*271 appels d'outils.* Actions notables :

- read
- get_goal
- bash — Inspect session check logic
- bash — Show OCR tool usage
- bash — Current time
- bash — Read OCR tool part 1
- bash — Read OCR tool part 2
- bash — Find the 127 scans figure and OCR artifacts
- bash — History of OCR tool and pending OCR files
- bash — Read CEGEP OCR manifest
- bash — Inspect OCR corpora and CEGEP PDF count
- bash — Locate scan census sources
- bash — Search 127 mentions across docs
- bash — Read session report around next steps
- … et 196 autres

**Synthèse produite :**

⏵ Session D/R/A terminée : OCR du fonds CEGEP mesuré, fiché et committé

**Session `fe3c05f0` (D/R/A) reprise puis close.** Le plan est passé `État : actif` avec heartbeat, puis `État : terminé` après livraison ; `cloture.md` est écrit, la session est sortie d'`en-cours`.

**Le chiffre, et la correction qu'il impose.** Le « ~127 scans » venait d'une détection sur les **deux premières pages**, qui sur-classe **5,5×** : **807 candidats** (179 426 p) côté outil, **147 vrais scans** (2 701 p) au texte **intégral**, **91 uniques** (2 053 p) après 56 doublons exacts (dont un second *Tesla* de 499 p). Les **10 « notes » du pilote** étaient en réalité **9 livres natifs** (463 à 1 706 car/p) et un seul scan (*AQPC*, 2 p) — erratum dans la fiche, corpus du pilote archivé.

**OCR du fonds, mesuré.** 91 scans traités (`--liste` explicite, `--ouvriers 8`), **60 documents retenus**, **1 982 pages**, **4 408 811 caractères**, splits **53 / 4 / 3**, 8 Ko **0 duplication** (542/2/2 fenêtres), éval `fr-xnli 0/40`, `fr-udhr 0/24`, `en-xnli 0/40`. Le PDF *MicroPython* (359 p) dépassait le timeout de rendu à 300 dpi : repris à **150 dpi** et ajouté au corpus.

**Livré et committé (`83f78803`) :** fiche [`rapport-ocr-cegep.md`](reports/rapport-ocr-cegep.md), manifeste [`ocr-pdf-cegep.json`](reports/ocr-pdf-cegep.json), détection [`ocr-pdf-cegep-detection.json`](reports/ocr-pdf-cegep-detection.json), contrôle [`contamination`](reports/ocr-pdf-cegep-contamination.json), outils `tools/detecte_scans_pdf.py` et `tools/ocr_pdf.py` (`--liste`, `--ouvriers`), état (`en-cours`, roadmap, chantiers, plan-travail), [clôture](journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/cloture.md), journal du jour.

**Contrôles passés :** revue de documentation ✅ (556 fiches / 643 JSON), `verifie_en_cours` ✅ (1 566 mots), `verifie_journal` ✅, hook d'état ✅. **`sessions.py --check --strict` reste rouge, mais hors D/R/A** : `29ad180d` (S, heartbeat de 108 min) et `536cd5d6` (hub, 123 min) sont périmés — ces deux sessions doivent rafraîchir leur plan. D/R/A est `terminé` et n'est plus exigé.

**Limites nommées :** 8 scans en `.PDF` (58 p) échappent à `rglob("*.pdf")` ; 31 documents courts (71 p) écartés par `--min-chars 300` ; WER non mesurée (pas de vérité terrain). Restent **R1.1/R1.2** (N2) et **A2.6** (A).

La session **L/B13** (`e181ce02`) est bien restée `actif` (heartbeat 18 h 22) et poursuit le gold neuronal.

### Tour 3 — as-tu terminé? les gpu et cpu sont tranquilles

*5 appels d'outils.* Actions notables :

- job_list
- bash — Check remaining processes, load and GPU
- bash — Verify my closure files are committed
- bash — Confirm commit ancestry and strict state
- bash — Check whether another session is still committing

**Synthèse produite :**

⏵ État vérifié : D/R/A close, aucun job à moi ; la machine n’est pas tout à fait vide

**Oui, ma part est terminée.** La session D/R/A (`fe3c05f0`) est close et committée — `83f78803` est bien dans l’historique ; plan `État : terminé`, `cloture.md`, fiche, manifeste et état à jour. **Aucun job de moi ne tourne** : les 9 jobs listés sont `completed` ou `killed` (le seul tué était la passe MicroPython à 200 dpi, remplacée par celle à 150 dpi qui a réussi).

**Mais la machine n’est pas complètement tranquille** : une autre session (Pensée/B13) a encore `llama-server` actif (818 % CPU), la porte `porte-audit-drapeaux` tourne depuis ~2 min (timeout 30 min), et des fichiers d’état (`en-cours`, `roadmap`, `chantiers`, `plan-travail`) sont **stagés** par une autre session. Mieux vaut ne pas couper tant que cette porte/ce commit n’a pas fini.

**`sessions.py --check --strict` reste rouge, hors D/R/A** : `29ad180d` (S, heartbeat de 163 min) et `536cd5d6` (hub, 178 min). D/R/A est `terminé` et n’est plus exigé. Si ces deux sessions sont réellement arrêtées, il faut les passer `en pause` (ou rafraîchir leur heartbeat) ; je n’ai pas touché à leurs plans. Je peux le faire si tu veux rendre la porte stricte verte.

### Tour 4 — c'est le temps de s'assurer que le pilotage est bien a jour et concis afin que tout soit optimal avec les sessions en co … [29 caractères tronqués]

*62 appels d'outils.* Actions notables :

- bash — Current time, recent commits and working tree
- bash — Session status, strict check and state checks
- bash — Inspect active session plans and heartbeats
- bash — Check active processes and GPU state
- read
- bash — Check N2 200k evaluation progress
- bash — Read roadmap and plan-travail lines
- edit `docs/pilotage/en-cours.md`
- edit `docs/pilotage/en-cours.md`
- edit `docs/pilotage/en-cours.md`
- edit `docs/pilotage/en-cours.md`
- edit `docs/pilotage/en-cours.md`
- edit `docs/pilotage/roadmap.md`
- bash — Verify roadmap N line
- … et 36 autres

**Synthèse produite :**

⏵ Passe de pilotage : je relève l’état réel des quatre sessions et des compteurs avant d’écrire

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md` | 0 | 4 |
| `work/ocr/census_cegep.py` | 1 | 0 |
| `work/ocr/detecte_cegep.py` | 1 | 0 |
| `tools/ocr_pdf.py` | 0 | 6 |
| `tools/detecte_scans_pdf.py` | 1 | 0 |
| `work/ocr/fiche-cegep.md` | 1 | 4 |
| `work/ocr/fait_fiche.py` | 1 | 1 |
| `work/ocr/ajoute_micro.py` | 1 | 0 |
| `reports/rapport-ocr-cegep.md` | 0 | 2 |
| `docs/pilotage/en-cours.md` | 0 | 19 |
| `docs/pilotage/roadmap.md` | 0 | 8 |
| `docs/pilotage/chantiers.md` | 0 | 4 |
| `docs/pilotage/plan-travail.md` | 0 | 4 |
| `journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/cloture.md` | 1 | 0 |
| `journal/2026-11-02/README.md` | 0 | 3 |
| `journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md` | 0 | 2 |
| `journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md` | 0 | 1 |
| `journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Show working directory and top-level files
- **T1** Inspect sessions tool usage
- **T1** List session directories
- **T1** Show session status
- **T1** Show current date and time
- **T1** Check git status and recent commits
- **T1** Show current diff of the session plan
- **T1** Peek AGENTS.md and count doc lines
- **T2** Inspect session check logic
- **T2** Show OCR tool usage
- **T2** Current time
- **T2** Read OCR tool part 1
- **T2** Read OCR tool part 2
- **T2** Find the 127 scans figure and OCR artifacts
- **T2** History of OCR tool and pending OCR files
- **T2** Read CEGEP OCR manifest
- **T2** Inspect OCR corpora and CEGEP PDF count
- **T2** Locate scan census sources
- **T2** Search 127 mentions across docs
- **T2** Read session report around next steps
- **T2** Inspect inventory JSONs for scan counts
- **T2** Show PDF corpus scan counts per root
- **T2** Show CEGEP inventory source
- **T2** Find scan count derivation in report
- **T2** Find scan-count code and day journal mentions
- **T2** Run strict session check
- **T2** Inspect the two offending plans
- **T2** Debug heartbeat parsing
- **T2** Re-run strict check and show file mtimes
- **T2** Check running OCR jobs and resources
- **T2** Check working tree before OCR work
- **T2** Inspect concurrent hub commits
- **T2** Check work dir and gitignore
- **T2** Census CEGEP PDFs and scans
- **T2** Find OCR gates and contamination tool
- **T2** Find prior journal entries for OCR
- **T2** Check contamination tool and OCR scan gate
- **T2** Detect true scanned PDFs via full text
- **T2** Inspect OCR scan gate and threading settings
- **T2** Check whether the 10 OCR notes are in the full-text scan list
- … et 166 autres

## 4. Mesures et résultats marquants

- **T2** `"split": f"hash salé du chemin : {args.val:.0%} val, {args.test:.0%} test",`
- **T2** `docs/pilotage/roadmap.md:36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte `
- **T2** `"split": "hash salé du chemin : 5% val, 5% test",`
- **T2** `**Le corpus OCR du CEGEP est passé de 7 à 10 notes** : *Algorithms Illuminated (Part 4)* 274 p, *Part 1* 217 p et *Data Structures and Algorithms in C* 366 p se sont ajoutés. Total mesuré : **10 notes`
- **T2** `2476:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours.`
- **T2** `2494:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours.`
- **T2** `2512:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre depuis plusieurs rounds.`
- **T2** `2530:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.`
- **T2** `2549:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.`
- **T2** `2568:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.`
- **T2** `2589:**L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours ; c'est le poste le plus lent.`
- **T2** `2609:**L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours ; c'est le poste le plus lent.`
- **T2** `2628:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.`
- **T2** `2647:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours.`
- **T2** `2666:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.`
- **T2** `2685:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.`
- **T2** `2704:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.`
- **T2** `2723:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.`
- **T2** `2943:| ocr (scannés) | 32,1 | 4,8 % |`
- **T2** `2967:Le manifeste est écrit et le corpus fermé : **7 459 PDF**, **803 817 pages**, **3 384 documents gardés**, **1 017 scannés**, **1 316 courts**, **1 742 doublons**, **871 972 648 caractères**, **10`
- **T2** `8885:- **Le processus** (PID 2644645) : **50 s**, **65,7 Mo lus**, **19,8 Mo écrits** — la détection des scannés (`pdfinfo` + `pdftotext` des 2 premières pages) parcourt le fonds CEGEP ; l'OCR des **5`
- **T2** `/dev/mapper/system-root   11T  9,0T  2,0T  83% /home/stephane/Data13TB`
- **T2** `75:| 01:28 | `6eff8d8d` | DONNÉES — L'OCR DES 8 LIVRES EST FICÉ : 2 815 PAGES, 7,69 M CARACTÈRES, 8 KO 0 (VAL/TEST VIDES, LE CSS SUIT) |`
- **T2** `78:| 01:34 | `868399c8` | DONNÉES — LA ROADMAP ET LE RÉCIT PORTENT L'OCR DES 8 LIVRES : 2 815 PAGES, 7,69 M CARACTÈRES, 951 FENÊTRES 8 KO |`
- **T2** `91:| 02:20 | `07e87a6f` | DONNÉES — L'OCR PASSE 10 M CARACTÈRES : 11 LIVRES, 4 042 PAGES, 1 244 FENÊTRES 8 KO, ÉVAL 0/40 |`
- **T2** `117:| 05:10 | `15f2c8f6` | DONNÉES — L'OCR DES 20 LIVRES EST CLOS : 7 381 PAGES, 15,36 M CARACTÈRES, 8 KO 0 (VAL 115, ÉVAL 0/40) |`
- **T2** `122:| 05:25 | `166896b4` | GENRES — L'OCR DES 20 LIVRES PASSE À 38,5 CAR/LIGNE (6,8 % DE DOUBLONS, 14,4 M) |`
- **T2** `128:| 05:48 | `bfe57da7` | CHANTIERS — LA LIGNE D PORTE L'OCR DES 20 LIVRES (15,36 M CARACTÈRES, 8 Ko 0) |`
- **T2** `132:| 06:30 | `ccf8bac5` | DONNÉES — LE CEGEP ENTRE DANS L'OCR : 5 NOTES, 292 PAGES, 506 801 CARACTÈRES, 8 KO 0 |`
- **T2** `210:- **Le corpus OCR** : 20 livres, 7 381 pages, 15,36 M caractères, 8 Ko 0 (val 115 fenêtres, éval 0/40) ; le pilote `--max-doc 20` est clos (le 20e, *Life Histories of Etnos Theory*, 450 p).`
- **T2** `211:- **Le corpus OCR du CEGEP** : 10 notes scannées, 1 596 pages, 2 519 507 caractères, 8 Ko 0 (val 11 fenêtres) — le pilote `--racine CEGEP` ferme la boucle « livres, CEGEP, collections » (4 *Algori`
- **T2** `30:| 01:28 | `6eff8d8d` | DONNÉES — L'OCR DES 8 LIVRES EST FICÉ : 2 815 PAGES, 7,69 M CARACTÈRES, 8 KO 0 (VAL/TEST VIDES, LE CSS SUIT) | `en-cours.md`, `README.md`, `apprentissage.md` (+16) |`
- **T2** `48:| 05:10 | `15f2c8f6` | DONNÉES — L'OCR DES 20 LIVRES EST CLOS : 7 381 PAGES, 15,36 M CARACTÈRES, 8 KO 0 (VAL 115, ÉVAL 0/40) | `en-cours.md`, `plan-travail.md`, `roadmap.md` (+22) |`
- **T2** `50:| 05:25 | `166896b4` | GENRES — L'OCR DES 20 LIVRES PASSE À 38,5 CAR/LIGNE (6,8 % DE DOUBLONS, 14,4 M) | `en-cours.md`, `README.md`, `distribue.md` (+11) |`
- **T2** `57:| 06:30 | `ccf8bac5` | DONNÉES — LE CEGEP ENTRE DANS L'OCR : 5 NOTES, 292 PAGES, 506 801 CARACTÈRES, 8 KO 0 | `en-cours.md`, `plan-travail.md`, `roadmap.md` (+20) |`
- **T2** `fichiers (tronçon de 8 Ko écrit par `corpus_wikipedia.py`) est hachée ; un`
- **T2** `(`corpus_wikipedia_texte.py`), l'unité est la **fenêtre** de 8 Ko coupée au`
- **T2** `[still running after 60000ms; moved to background job bash-37]`
- **T2** `echo "  corpus de scans absent : fabrication (10 pages dev + 10 test × 5 familles)"`
- **T2** `default run1: 2.04 s (141% CPU)`
- **T2** `default run2: 1.46 s (192% CPU)`
- **T2** `omp1 run1: 1.56 s (99% CPU)`
- **T2** `omp1 run2: 1.51 s (100% CPU)`
- **T2** `{'ocr': 'tesseract 5.5.3 sans root (work/ocr/root)', 'langues': 'fra+eng', 'dpi': 300, 'psm': 3, 'pretraitement': 'aucun (le R4.4 le fera)', 'detection': 'liste explicite de scans qualifiés sur le tex`
- **T2** `- **Objectif final** : un **mètre honnête** pour N2 — corpus dédupliqué (0 % de fenêtres de`
- **T2** `- **Résultat** : corpus 4,63 → 3,61 Mo (−22,2 %), **0 / 2 814** fenêtres de validation dans`
- **T2** `l'entraînement (contre 32,8 %) ; chaîne propre **3,09** en domaine, **16,70** sur la littérature`
- **T2** `**−5,9 % à +19,5 %**. Fiche [`rapport-a83-defaut.md`](../../../reports/rapport-a83-defaut.md),`
- **T2** `budget 10 %. Fiche [`rapport-a83b-regimes.md`](../../../reports/rapport-a83b-regimes.md).`
- **T2** `**11,1** (plancher **38,5**), 3 bras × 3 graines ; à **1800 pas** la traduction reste entre`
- **T2** `0 = lignes ; 8192 = fenêtres de 8 Ko (texte intégral)`
- **T2** `reports/rapport-ocr-cegep.md:36:`verifie_contamination.py --taille-troncon 8192` : **54 fenêtres de 8 Ko** en train, **11** en val, **0 duplication** entre splits. Recouvrement avec les évaluations **`
- **T2** `reports/rapport-ocr-pdf.md:36:`verifie_contamination.py --taille-troncon 8192` : **1784 fenêtres de 8 Ko** en train, **115** en val, **0 duplication** entre splits (le val porte un livre, le test aucu`
- **T2** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4, A6.2 bloqués** ; A2.6 partiel ; A3.2/A3.3 mesurée`
- **T2** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T2** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | 🔬 **v0** : 7 phrases + **générateur** + **pragmatique** (statuts, double sens conservé, **niveaux 0–4**, ni`
- **T2** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T2** `- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 intérieur, ×62,7 tout ; [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../reports/rapport-typogly`
- **T2** `- **S — le banc de structures** : outil web (`tools/structures`), générateur, pragmatique (niveaux 0–4), export ; analyseur **7/7** séquences, **93,9 %** de couverture, **19 tests** ; [`analyseur`](..`
- **T2** `[still running after 60000ms; moved to background job bash-83]`
- **T2** `docs/pilotage/chantiers.md:89:| **D — les données** (nouveau) | avec quoi entraîne-t-on, et à quel prix ? | ✅ inventaire local ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 `
- **T2** `220:- **Le corpus OCR du CEGEP** : 10 notes scannées, 1 596 pages, 2 519 507 caractères, 8 Ko 0 (val 11 fenêtres) — le pilote `--racine CEGEP` ferme la boucle « livres, CEGEP, collections » (4 *Algori`
- **T2** `- **Les dix corpus Wikipédia en texte intégral** : 20,53 M articles, 67,73 G caractères, 81,2 Go, 8 Ko 0 partout ; l'anglais clos à 99,2 % (l'écriture bloquée à 125/125 Go, le manifeste reconstruit de`
- **T2** `- **Le corpus PDF** : 2 785 PDF, 1 927 documents, 322 Mo, 8 Ko 0, licences nommées.`
- **T2** `- **Le corpus Documents** : 7 459 PDF, 3 384 documents, 872 M caractères, 8 Ko 2,07 % (les 372 tronçons dupliqués).`
- **T2** `- **Le corpus OCR** : 20 livres, 7 381 pages, 15,36 M caractères, 8 Ko 0 (val 115 fenêtres, éval 0/40) ; le pilote `--max-doc 20` est clos (le 20e, *Life Histories of Etnos Theory*, 450 p).`
- **T2** `- **Le corpus OCR du CEGEP** : 10 notes scannées, 1 596 pages, 2 519 507 caractères, 8 Ko 0 (val 11 fenêtres) — le pilote `--racine CEGEP` ferme la boucle « livres, CEGEP, collections » (4 *Algorithms`
- **T2** `- **Les genres** : l'encyclopédie 103–147 car/ligne, les livres et documents 32–37, les lignes dupliquées 8,7–24 % (l'OCR 4,8 %).`
- **T2** `- **A2.6/A8.3** : le lot ne divise pas les lectures denses (+27 % de calcul, PPL −0,006 %).`
- **T2** `- **15 h 06 — reboot.** Les deux GPU étaient bloqués (`GPU requires reset`, `nvidia_drm refcnt -1`) ; le reset logiciel a échoué et le reboot a rendu les cartes (1 Mio, 0 %). Les deux sessions de trav`
- **T2** `tmpfs            63G     0   63G   0% /dev/shm`
- **T2** `tmpfs            63G   59M   63G   1% /tmp`
- **T2** `dispositif {'ocr': 'tesseract 5.5.3 sans root (work/ocr/root)', 'langues': 'fra+eng', 'dpi': 300, 'psm': 3, 'pretraitement': 'aucun (le R4.4 le fera)', 'detection': 'liste explicite de scans qualifiés`
- **T2** `24:| tronçons 8 Ko | **{{troncons}}** |`
- **T2** `32:3. **Splits** : hash salé du chemin (`graine=1`) — 5 % val, 5 % test ; les mêmes règles que les autres corpus.`
- **T2** `38:- **8 Ko** : `verifie_contamination.py --taille-troncon 8192` — **{{w_train}}** fenêtres en train, **{{w_val}}** en val, **{{w_dup}}** duplication entre splits.`
- **T2** `59:- `reports/ocr-pdf-cegep-contamination.json` — le contrôle 8 Ko et évaluations.`
- **T2** `éval : `fr-xnli.txt` **0/40** · `fr-udhr.txt` **0/24** · `en-xnli.txt` **0/40** · 8 Ko : 542 / 2 / 0`
- **T2** `| **D — les données** (nouveau) | avec quoi entraîne-t-on, et à quel prix ? | ✅ inventaire local ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**), **PDF** (322 Mo), **d`
- **T2** `1 982 p, 4 408 811 caractères**, 8 Ko 0, éval **0/40 · 0/24 · 0/40** ; le PDF de 359 p`
- **T2** `| [rapport-native-tetes.md](rapport-native-tetes.md) | N1.4 — les têtes précoces de `drave-n0` : 55,2 / 60,9 / 62,1 % |`
- **T2** `-- **Le corpus OCR du CEGEP** : 10 notes scannées, 1 596 pages, 2 519 507 caractères, 8 Ko 0 (val 11 fenêtres) — le pilote `--racine CEGEP` ferme la boucle « livres, CEGEP, collections » (4 *Algorithm`
- **T2** `+1 982 p, 4 408 811 caractères**, 8 Ko 0, éval **0/40 · 0/24 · 0/40** ; le PDF de 359 p`
- **T2** `+> **60 documents, 1 982 p, 4 408 811 car.**, 8 Ko 0 ; les 10 notes du pilote étaient`
- **T2** `2 053 p), **60 documents, 1 982 p, 4 408 811 car.**, 8 Ko 0 ; la détection à deux pages`
- **T3** `0, 0 %, 1862 MiB`
- **T3** `1, 45 %, 1014 MiB`
- **T4** `→ la **passe de portes** complète, **reportée** — mesuré à 16 h 32 : GPU 0 à **92 %** (N2, 1 650 MiB) et GPU 1 à **84 %** (`entrainer_rope.py`, 1 300 MiB), charge **24** ; le doc `portes.md` interdit `
- **T4** `0, 0 %, 928 MiB`
- **T4** `1, 0 %, 122 MiB`
- **T4** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T4** `36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art.,`
- **T4** `111:[N2] lasts 4 days and is 30% complete and is colored in #b26a00`
- **T4** `N2.aa avait montré qu'à 40 Mo vus, un corpus 5,6× plus grand ne fait pas apprendre plus — il fait`
- **T4** `de `data/wiki_fr/propre` (186 Mo) et `data/wiki_big/propre` (831 Mo) ; canal concaténé ; le`
- **T4** `découpage interne réserve les 5 % finaux à la validation d'entraînement.`
- **T4** `lieu de 60 000 (×3,33). GPU 0, **11 410 s** (3 h 10), ~57 ms/pas.`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T2** : 19:48 /tmp/ocr-pdf-19jav9ag: 453 page(s) 0 [exit code: 1]

## 6. Commits

- ps -eo pid,etime,args | grep -E "git commit|git add|pre-commit|archive_sessions|session_report" | grep -v grep | head -8; echo "--- staged now ---"; git diff --
- DONNÉES — L'OCR CEGEP EST CLOS : 147 SCANS DÉTECTÉS (91 UNIQUES, 2 053 P), 60 DOCUMENTS, 1 982 P, 4,41 M CAR. ; LE PILOTE DES 10 NOTES ÉTAIT 9 FAUX POSITIFS" -m
- ps -eo pid,etime,pcpu,comm,args --sort=-pcpu | grep -E "ocr_pdf|detecte_scans|tesseract|pdftoppm|entrainer|llama-server|porte-|git commit" | grep -v grep | head
- ps -eo pid,etime,pcpu,args | grep -E "git commit|porte-audit|entrainer_moteur|llama-server" | grep -v grep | head -5; echo "--- dernier commit ---"; git log -1 
- ps -eo pid,etime,pcpu,args --sort=-pcpu | grep -E "entrainer|llama-server|porte-|git commit|n2ac" | grep -v grep | head -6; echo "--- gpu ---"; nvidia-smi --que
- date "+%H:%M:%S"; ls -l --time-style=+%H:%M:%S docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/chantiers.md docs/pilotage/plan-travail.md; ps -


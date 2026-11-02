# Session b7d4678e — Reprise session L/B13 et vérification stricte

> **Journaux :** [le jour](../../2026-11-02/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `b7d4678e-2143-4daa-a9a4-a456c5aa8dab` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-02 16:16 |
| Durée | 2.1 h |
| Tours | 2 |
| Messages | 201 |
| Appels d'outils | 218 |
| Fichiers touchés | 8 |
| Commandes | 153 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## Objectifs déclarés

- **create** — Session D/R/A (fe3c05f0) : OCR du fonds CEGEP restant (~127 scans) en sortie séparée, fusion et contrôle du corpus (10 notes + suite), fiche + JSON, en-cours + commit explicite, puis clôture de la session.

## 1. Ce qui a été demandé

**Tour 1** — Tu reprends la session L/B13 `e181ce02-cd50-488a-a6be-e84b79d40dcc`. Lis son plan, AGENTS.md  et docs/pilotage/en-cours.md. Remets `- **État** : actif` et `- **Heartbeat** : <maintenant>`  dans son plan, puis vérifie `python3 tools/sessions.py --check --strict`. Le cycle 140/140  (gold 432, 116 liens) est committé. Prochaine action : gold neuronal (qualifier un modèle  local) ; DRVM/native est blo … [114 caractères tronqués]

**Tour 2** — Tu reprends la session D/R/A `fe3c05f0-834b-44f2-8739-501865d652c1`. Lis son plan, AGENTS.md  et en-cours. Remets `État : actif` et heartbeat maintenant, puis  `sessions.py --check --strict`. Le texte intégral, le PDF, les 20 livres, les 10 notes CEGEP,  le glossaire (355 entrées) et docwatch sont committés. Prochaine action : OCR ~127 scans CEGEP  (`tools/ocr_pdf.py --racine CEGEP --deja <N>`), p … [87 caractères tronqués]

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

*207 appels d'outils.* Actions notables :

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
- … et 145 autres

**Synthèse produite :**

⏵ Correction mesurée : 807 candidats à 2 pages, mais 147 vrais scans (91 uniques, 2 053 p) — j'adapte l'outil

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md` | 0 | 3 |
| `work/ocr/census_cegep.py` | 1 | 0 |
| `work/ocr/detecte_cegep.py` | 1 | 0 |
| `tools/ocr_pdf.py` | 0 | 6 |
| `tools/detecte_scans_pdf.py` | 1 | 0 |
| `work/ocr/fiche-cegep.md` | 1 | 0 |
| `work/ocr/fait_fiche.py` | 1 | 1 |
| `work/ocr/ajoute_micro.py` | 1 | 0 |

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
- … et 113 autres

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

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T2** : 19:48 /tmp/ocr-pdf-19jav9ag: 453 page(s) 0 [exit code: 1]

## 6. Commits

- ps -eo pid,etime,args | grep -E "git commit|git add|pre-commit|archive_sessions|session_report" | grep -v grep | head -8; echo "--- staged now ---"; git diff --


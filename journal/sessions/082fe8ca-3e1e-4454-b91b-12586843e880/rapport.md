# Session 082fe8ca — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `082fe8ca-3e1e-4454-b91b-12586843e880` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 11:17 |
| Durée | 0.6 h |
| Tours | 1 |
| Messages | 36 |
| Appels d'outils | 49 |
| Fichiers touchés | 2 |
| Commandes | 40 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer la fiabilité du produit hors gold** — le test « utilisateur » qui manque.  Contexte : `tools/drave.py` (CLI : `analyser`, `evaluer`, `rejouer`, `--version`), `tools/bloc_linguistique.py` (`Heuristique.analyser` → `Annotation`), la doc `docs/produit/README.md`. État mesuré : gold  … [1665 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [1945 caractères tronqués]

*49 appels d'outils.* Actions notables :

- bash — Check working directory and git status
- bash — List repo root and reports directory
- bash — Count lines of key files
- bash — Check recent commits and reports status
- read
- bash — List classes and methods in bloc_linguistique.py
- bash — Read product test and gate
- bash — List linguistic tests and check CLI version
- bash — List product reports and inspect JSON format
- bash — Inspect recent report markdown styles
- bash — Check file timestamps and existing report summary
- bash — Inspect existing JSON structure
- bash — Probe CLI edge cases and exit codes
- bash — Probe URL tokenization and phrase spans
- … et 29 autres

**Synthèse produite :**

⏵ Classification fine des chevauchements, cibles et POS manquantes

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/audit_cli.py` | 1 | 0 |
| `/tmp/audit_cli_detail.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check working directory and git status
- **T1** List repo root and reports directory
- **T1** Count lines of key files
- **T1** Check recent commits and reports status
- **T1** List classes and methods in bloc_linguistique.py
- **T1** Read product test and gate
- **T1** List linguistic tests and check CLI version
- **T1** List product reports and inspect JSON format
- **T1** Inspect recent report markdown styles
- **T1** Check file timestamps and existing report summary
- **T1** Inspect existing JSON structure
- **T1** Probe CLI edge cases and exit codes
- **T1** Probe URL tokenization and phrase spans
- **T1** Probe option-like and invalid-UTF-8 inputs
- **T1** Measure 10k-character input
- **T1** Test locale and stdout encoding failures
- **T1** Test broken pipe and phrase span whitespace
- **T1** Read existing report contract and fixes sections
- **T1** Check date, environment, commit, roadmap
- **T1** Read roadmap header
- **T1** Probe phrase overlaps from abbreviations
- **T1** Patch harness duplicate examples
- **T1** Run full CLI audit harness
- **T1** Read benchmark per-sentence output
- **T1** Aggregate benchmark results
- **T1** Inspect surface errors, languages, targets
- **T1** Debug invalid UTF-8 argv injection
- **T1** Debug surrogate handling in argv and API
- **T1** Test API with lone surrogate
- **T1** Instrument CLI argv for invalid byte
- **T1** Test Python surrogate encoding behavior
- **T1** Check module modification and refusal code
- **T1** Inspect loaded analyser source
- **T1** Inspect concurrent module changes and hashes
- **T1** Show new commits and module diff since audit start
- **T1** Check last commit touching module
- **T1** Compare harness and module timestamps
- **T1** Retest surrogate CLI and non-str API after fix
- **T1** Run detailed overlap/target analysis
- **T1** Fix refusal handling and rerun detail analysis

## 4. Mesures et résultats marquants

- **T1** `6ef2a3f5 JOURNAL ET ROADMAP — LA VAGUE PRODUIT : DRAVE V0 DOCUMENTÉ, PORTE PRODUIT VERTE, AUTOTEST ×2,4, MASTER POUSSÉ (7f73c17f)`
- **T1** `| graphème, mot | ✅ | 0 crash, 0 span hors texte, `valeur = texte[debut:fin]` à **100 %**, couverture **49/50 à 100 %** (x46 : 95,14 %, newlines) |`
- **T1** `dash-- rc=0 out=langue=und script=Latn source=heuristique · 12 étiquettes · unités sémantiques=1 (66.7% du texte)`
- **T1** `**graphème** : 49/50 textes à 100 %, x46 à **95,14 %** (7 newlines, catégorie `Cc`, non couvertes).`
- **T1** `| **heuristique** | **1,08 ms** | **4,60 ms** | **19,43 ms** | 0,097 |`
- **T1** `| mock neuronal | 0,30 ms | 1,08 ms | 4,44 ms | 0,022 |`
- **T1** `| parallèle | 1,51 ms | 6,18 ms | 27,22 ms | 0,136 |`
- **T1** `| cascade | 1,51 ms | 6,25 ms | 29,64 ms | 0,148 |`
- **T1** `- **Coût des compositions** : +37 % (parallèle) et +45 % (cascade) à 200 mots **avec le mock** ;`
- **T1** `**99–113 ms** (import + première analyse), **27,4 Mio**.`
- **T1** `- **Passage à l'échelle** : 200 mots 19 ms (0,096 ms/mot), 500 mots 70 ms (0,139), 1 000 mots`
- **T1** `166 ms (0,166), 2 000 mots 482 ms (0,241), 4 000 mots **1 574 ms** (0,394). Le coût par mot`
- **T1** `| `valeur` | **surface** pour graphème/mot/pos/syntagme (100 %) ; **normalisée** pour morphème (126/134) ; **tronquée à 60** pour document (42/53) ; **catégorielle** pour phrase/pragmatique/discours ;`
- **T1** `| **P1-15** | **Réduire le coût superlinéaire au-delà de 200 mots** | 0,096 ms/mot à 200, **0,394** à 4 000 (4,1×), 1,57 s à 4 000 ; `_cible_proche` : **199 302** appels à `_est_adverbe_seul` | 800-85`
- **T1** `| **P2-16** | Couvrir les caractères de contrôle dans graphème | x46 : **7 newlines** non couverts, 95,14 % ; 49/50 à 100 % | 1020-1031 | **15 min** |`
- **T1** `38:**État au 06/11 11 h 15.** B13 est à **183/183** ; **attachement 222/222 (1,0000)** (fr 136/136, en 86/86), **couverture 0,9289** ; dev 153/153, test 69/69 ; **le premier produit est debout et docu`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4, A6.2 bloqués** ; A2.6 partiel ; A3.2/A3.3 mesurée`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête `
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 06/11 11 h 15.** B13 est à **183/183** ; **attachement 222/222 (1,0000)** (fr 136/136, en 86/86), **couverture 0,9289** ; dev 153/153, test 69/69 ; **le premier produit est debout et documen`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `**préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `fax **56,7 %**, la limite d'information) ; les **colonnes** tombent de **89,4 %** à **0,5 %**,`
- **T1** `les **tableaux** donnent **92,6 %** de cellules exactes, et **trois vrais scans** s'accordent à`
- **T1** `**7,10 %** et **88,4 %** de mots, l'**ordre des colonnes** prouvé (**15,3 %** contre **98,0 %**`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `f50 rc=0 wall=  226.6ms json=True labels=1990 ovl={'discours': {'paires': 7, 'etiquettes': 11, 'exemples': [['connecteur', 0, 182, 'paragraphe', 0, 716], ['paragraphe', 0, 716, 'connecteur', 182, 268]`
- **T1** `rob 10k_phrases: rc=0 590ms labels=10362 json=2763666o`
- **T1** `rob 10k_sans_espace: rc=0 194ms labels=7 json=42482o`
- **T1** `rob 10k_ponctuation: rc=1 152ms`
- **T1** `rob 10k_lisible: rc=0 155ms ligne_max=10010`
- **T1** `f01 rc=0 wall=  150.8ms json=True labels=19 ovl={}`
- **T1** `f02 rc=0 wall=  193.9ms json=True labels=59 ovl={'syntagme': {'paires': 2, 'etiquettes': 5, 'exemples': [['REL', 22, 42, 'REL', 22, 54], ['REL', 22, 54, 'GV', 43, 54]]}}`
- **T1** `f03 rc=0 wall=  149.9ms json=True labels=37 ovl={}`
- **T1** `f04 rc=0 wall=  157.2ms json=True labels=38 ovl={}`
- **T1** `f05 rc=0 wall=  181.6ms json=True labels=30 ovl={'phrase': {'paires': 1, 'etiquettes': 2, 'exemples': [['type', 0, 20, 'négation', 0, 20]]}, 'syntagme': {'paires': 1, 'etiquettes': 3, 'exemples': [['G`
- **T1** `f06 rc=0 wall=  154.1ms json=True labels=62 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 61, 'paragraphe', 0, 61]]}, 'phrase': {'paires': 1, 'etiquettes': 2, 'exemple`
- **T1** `f07 rc=0 wall=  149.3ms json=True labels=32 ovl={}`
- **T1** `f08 rc=0 wall=  149.7ms json=True labels=37 ovl={}`
- **T1** `f09 rc=0 wall=  145.2ms json=True labels=33 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 36, 'paragraphe', 0, 36]]}}`
- **T1** `f10 rc=0 wall=  141.8ms json=True labels=51 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 42, 'paragraphe', 0, 42]]}, 'syntagme': {'paires': 1, 'etiquettes': 5, 'exemp`
- **T1** `f11 rc=0 wall=  161.5ms json=True labels=41 ovl={'syntagme': {'paires': 1, 'etiquettes': 4, 'exemples': [['GP', 26, 27, 'GP', 26, 31]]}}`
- **T1** `f12 rc=0 wall=  153.0ms json=True labels=63 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['paragraphe', 0, 62, 'connecteur', 33, 62]]}}`
- **T1** `f13 rc=0 wall=  148.6ms json=True labels=26 ovl={}`
- **T1** `f14 rc=1 wall=  156.8ms json=None labels=- ovl=-`
- **T1** `f15 rc=1 wall=  150.2ms json=None labels=- ovl=-`
- **T1** `f16 rc=1 wall=  136.8ms json=None labels=- ovl=-`
- **T1** `f17 rc=1 wall=  159.6ms json=None labels=- ovl=-`
- **T1** `f18 rc=0 wall=  143.3ms json=True labels=6 ovl={}`
- **T1** `f19 rc=0 wall=  147.5ms json=True labels=44 ovl={}`
- **T1** `f20 rc=0 wall=  175.9ms json=True labels=69 ovl={'phrase': {'paires': 1, 'etiquettes': 2, 'exemples': [['type', 0, 59, 'type', 2, 59]]}, 'pragmatique': {'paires': 1, 'etiquettes': 2, 'exemples': [['ac`
- **T1** `f21 rc=0 wall=  152.4ms json=True labels=59 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 56, 'paragraphe', 0, 56]]}, 'phrase': {'paires': 1, 'etiquettes': 2, 'exemple`
- **T1** `f22 rc=0 wall=  153.1ms json=True labels=56 ovl={'syntagme': {'paires': 2, 'etiquettes': 8, 'exemples': [['GN', 6, 8, 'GN', 6, 11], ['GN', 6, 11, 'GV', 8, 11]]}}`
- **T1** `f23 rc=0 wall=  147.6ms json=True labels=55 ovl={'phrase': {'paires': 1, 'etiquettes': 2, 'exemples': [['type', 0, 61, 'modalité', 0, 61]]}, 'syntagme': {'paires': 2, 'etiquettes': 6, 'exemples': [['G`
- **T1** `f24 rc=0 wall=  165.8ms json=True labels=71 ovl={'syntagme': {'paires': 5, 'etiquettes': 7, 'exemples': [['GV', 0, 8, 'GV', 0, 34], ['GV', 0, 34, 'GN', 9, 34], ['REL', 35, 45, 'REL', 35, 65]]}}`
- **T1** `f25 rc=0 wall=  163.8ms json=True labels=25 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['paragraphe', 0, 21, 'connecteur', 10, 21]]}}`
- **T1** `f26 rc=0 wall=  155.4ms json=True labels=50 ovl={'syntagme': {'paires': 1, 'etiquettes': 4, 'exemples': [['GV', 24, 34, 'GV', 27, 34]]}}`
- **T1** `f27 rc=0 wall=  168.6ms json=True labels=13 ovl={}`
- **T1** `f28 rc=0 wall=  154.5ms json=True labels=45 ovl={}`
- **T1** `f29 rc=0 wall=  150.5ms json=True labels=47 ovl={'pragmatique': {'paires': 1, 'etiquettes': 3, 'exemples': [['acte', 0, 33, 'double_sens', 0, 33]]}, 'syntagme': {'paires': 2, 'etiquettes': 5, 'exemple`
- **T1** `f30 rc=0 wall=  172.1ms json=True labels=40 ovl={}`
- **T1** `f31 rc=0 wall=  149.8ms json=True labels=27 ovl={'phrase': {'paires': 1, 'etiquettes': 2, 'exemples': [['type', 0, 20, 'négation', 0, 20]]}, 'syntagme': {'paires': 1, 'etiquettes': 2, 'exemples': [['G`
- **T1** `f32 rc=0 wall=  147.9ms json=True labels=62 ovl={'syntagme': {'paires': 1, 'etiquettes': 6, 'exemples': [['GN', 0, 17, 'GN', 7, 17]]}}`
- **T1** `f33 rc=0 wall=  145.9ms json=True labels=34 ovl={}`
- **T1** `f34 rc=0 wall=  139.0ms json=True labels=54 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 58, 'paragraphe', 0, 58]]}, 'syntagme': {'paires': 3, 'etiquettes': 6, 'exemp`
- **T1** `f35 rc=0 wall=  180.3ms json=True labels=43 ovl={}`
- **T1** `f36 rc=0 wall=  160.1ms json=True labels=46 ovl={'phrase': {'paires': 1, 'etiquettes': 2, 'exemples': [['type', 0, 47, 'modalité', 0, 47]]}}`
- **T1** `f37 rc=0 wall=  148.7ms json=True labels=55 ovl={}`
- **T1** `f38 rc=0 wall=  175.0ms json=True labels=103 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 24, 'paragraphe', 0, 69]]}, 'syntagme': {'paires': 1, 'etiquettes': 9, 'exem`
- **T1** `f39 rc=0 wall=  150.2ms json=True labels=73 ovl={'pragmatique': {'paires': 1, 'etiquettes': 3, 'exemples': [['acte', 0, 28, 'double_sens', 0, 28]]}, 'syntagme': {'paires': 2, 'etiquettes': 7, 'exemple`
- **T1** `f40 rc=0 wall=  149.5ms json=True labels=76 ovl={}`
- **T1** `f41 rc=0 wall=  150.6ms json=True labels=83 ovl={'syntagme': {'paires': 3, 'etiquettes': 5, 'exemples': [['GP', 18, 31, 'GP', 18, 66], ['GP', 18, 66, 'GP', 32, 43], ['GP', 18, 66, 'GP', 49, 66]]}}`
- **T1** `f42 rc=0 wall=  148.2ms json=True labels=32 ovl={}`
- **T1** `f43 rc=0 wall=  153.9ms json=True labels=342 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 390, 'paragraphe', 0, 390]]}, 'pragmatique': {'paires': 1, 'etiquettes': 2, `
- **T1** `f44 rc=0 wall=  179.1ms json=True labels=60 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 74, 'paragraphe', 0, 74]]}, 'phrase': {'paires': 1, 'etiquettes': 2, 'exemple`
- **T1** `f45 rc=0 wall=  147.4ms json=True labels=64 ovl={'phrase': {'paires': 1, 'etiquettes': 2, 'exemples': [['type', 0, 72, 'négation', 0, 72]]}, 'syntagme': {'paires': 4, 'etiquettes': 7, 'exemples': [['G`
- **T1** `f46 rc=0 wall=  154.1ms json=True labels=56 ovl={'syntagme': {'paires': 4, 'etiquettes': 6, 'exemples': [['GV', 0, 8, 'GV', 3, 6], ['GV', 0, 8, 'GV', 7, 24], ['GV', 7, 24, 'GV', 12, 16]]}}`
- **T1** `f47 rc=0 wall=  147.1ms json=True labels=45 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 43, 'paragraphe', 0, 43]]}}`
- **T1** `f48 rc=0 wall=  168.8ms json=True labels=89 ovl={}`
- **T1** `f49 rc=0 wall=  154.3ms json=True labels=59 ovl={}`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : argv bytes: b'["\'-c\'", "\'analyser\'", "\'\\\\udcff\'"]\n' b'' cli bytes: 1 b'' b"drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)\n" [stderr] Traceback (most


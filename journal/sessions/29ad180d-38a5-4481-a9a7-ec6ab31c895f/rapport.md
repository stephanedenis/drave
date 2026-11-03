# Session 29ad180d — Session structures CPU analyseur rôles

> **Journaux :** [le jour](../../2026-11-02/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `29ad180d-38a5-4481-a9a7-ec6ab31c895f` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-02 16:14 |
| Durée | 25.6 h |
| Tours | 13 |
| Messages | 376 |
| Appels d'outils | 368 |
| Fichiers touchés | 16 |
| Commandes | 282 |
| Sous-agents | 0 |
| Commits | 26 |
| Compactages de contexte | 1 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es la session S (les structures, CPU). Lis AGENTS.md, docs/pilotage/en-cours.md,  docs/theorie/jeux-symboliques.md et tools/structures/ (sous-module heads/fusion). Ton id est  dans `printenv DSH_SESSION_ID` ; crée journal/sessions/<id>/plan.md avec  `python3 tools/sessions.py --modele` (État : actif, heartbeat maintenant), réserve  `tools/structures/`, ses exports et sa banque. Prochaine action … [285 caractères tronqués]

**Tour 2** — mets le dossier copilotage à jour

**Tour 3** — commit l'ensemble

**Tour 4** — push

**Tour 5** — tu feras un commit push quand ce sera stable. pour l'instant, la machine est tranquille. tu peur entreprendre des choses

**Tour 6** — attends-tu aprèes quelque-chose? on a des ressources qui peuvent en prendre un peu plus

**Tour 7** — tiens ta liste de tâches dsh à jour et continue

**Tour 8** — prochaine étape?

**Tour 9** — pour ce qui est de la validation de la banque, après moins de 20%, j'arrête car j'ai trop de doutes sur l'arvre syntaxique car il manque trop souvent de profondeur et les référents ne semblent pas résolus avant que je tranche

**Tour 10** — vas-y avec des paragraphes complets et un arbre svg avec liaisons référents-référés

**Tour 11** — quel page web utiliser pour la suite?

**Tour 12** — les svg sortent du cadre, prévoir scrollbar et largeur de page adapté à la largeur d'écran ou fenêtre

**Tour 13** — tu peux aussi valider le sens (et indirectement les référents de syntaxe) en utilisant des traductions.

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

*13 appels d'outils.* Actions notables :

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
- bash — Final integration status and checks

**Synthèse produite :**

⏵ Intégration committée : Pensée (`7ef0199c`), D/R/A (`d2fc26c6`), S (`63927a03`/`dca7e7a2`). Seul le brouillon N2 reste hors commit.

**Committé**

- **`7ef0199c`** — Pensée/B13 : gold neuronal, tagger 7B local, POS **0,8483**, cascade **0,9440** ; fiche + JSON + doc + outils ; état, README et INDEX.
- **`d2fc26c6`** — D/R/A : détection CEGEP **2 681 PDF → 147 scans** (91 uniques, 2 053 p) ; `ocr_pdf.py --liste --ouvriers`, `detecte_scans_pdf.py`, `reports/ocr-pdf-cegep-detection.json` ; ligne D/R/A d'`en-cours`.
- **`dca7e7a2`** et **`63927a03`** — S : fiche, manifeste, section S, roadmap, compteurs **553 fiches / 639 JSON**.

**Contrôles** : `revue_documentation.py` ✅ · budgets T0/T1 ✅ · `en-cours` **1 612 mots**, 5 questions ✅ · `verifie_en_cours.py` ✅ · `verifie_etat_a_jour.py` ✅.

**Reste hors commit** : `reports/rapport-n2-r11.md` — la fiche R1.1 de N2 contient encore `{{G2}}`, `{{ABS1152}}` et `{{R12}}` : c'est un **brouillon en cours d'écriture**, pas un fait publiable. La session N2 le terminera ; je le committerai ensuite si tu veux. Tout le reste de l'arbre est propre.

### Tour 4 — push

*8 appels d'outils.* Actions notables :

- bash — Inspect remotes and ahead/behind
- bash — Inspect uncommitted code and submodule remote state
- bash — Push structures submodule
- bash — Inspect submodule remote repo and gitmodules
- bash — Allow updateInstead and push submodule
- bash — Test GitHub SSH connectivity
- bash — Push main repository to GitHub
- bash — Verify pushed refs and remaining local changes

**Synthèse produite :**

⏵ Push terminé : principal `d2fc26c6`, sous-module `647205a`.

- **Dépôt principal** — `origin/master` : `a31a2e4d..d2fc26c6` (**263 commits** poussés). `master...origin/master` à jour.
- **Sous-module `tools/structures`** — `origin/master` : `3b68143..647205a`. Le remote local `drave-structures` refusait le push (branche `master` checkoutée, dépôt non bare) ; réglé par `receive.denyCurrentBranch=updateInstead`, puis poussé.
- Le pointeur commité dans le principal (`647205a`) existe donc bien sur le remote du sous-module.

**Reste local, non poussé** — travail en cours d'autres sessions :

- `tools/bloc_linguistique.py`, `tools/tests/linguistique/test_bloc_linguistique.py`, `tools/tests/linguistique/qualifier_syntagmes.py` : le tagger de **syntagmes** (BIO/GBNF) de Pensée, encore en écriture ;
- `reports/rapport-n2-r11.md` : brouillon N2 R1.1 avec `{{G2}}`, `{{ABS1152}}`, `{{R12}}`.

Dis-moi quand ils sont prêts : je les commite avec leurs lignes d'état et je pousse.

### Tour 5 — tu feras un commit push quand ce sera stable. pour l'instant, la machine est tranquille. tu peur entreprendre des choses

*31 appels d'outils.* Actions notables :

- bash — Check machine load, GPUs, and running work
- bash — Check WIP freshness and session/gate state
- todo_write
- bash — Reproduce GN boundary failures
- bash — Locate constants and GN loop
- bash — Add finite-verb GN boundary and test examples
- bash — Add GV time-adverb break and measure
- bash — Add holdout3 and measure
- bash — Add GN boundary tests and rerun suite/measure
- bash — Update submodule README for v3
- bash — Export 47-phrase gold corpus and verify
- bash — Commit submodule v3
- bash — Exact v3 measure values and boundary lines
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md`
- … et 16 autres

**Synthèse produite :**

⏵ S v3 poussé : analyseur 47/47 types, 117/117 rôles, corpus 47 ; sous-module et principal à jour.

**Le cycle entrepris**

- **Frontière GN-devant-verbe** : `h033` (« La femme parle ») est corrigé par un lexique de verbes finis ; le GV s'arrête aussi devant un adverbe de temps (« part demain » → GV + GP temps).
- **Gold porté à 47 phrases** (7 dev, 16 test, 24 holdout en trois vagues ; `h040–h047` écrites après la règle, mesurées une fois).
- **Mesure** : types **47/47**, rôles **117/117**, compléments **47/47**, couverture **1 309/1 320** (99,2 % ; holdout 605/616, 98,2 %) ; contrôles **80/117**, **82/117**, rôles mélangés **0,109**.
- **Limite nommée** : les homographes nominaux `h046` (« ferme ») et `h047` (« fait ») sont coupés comme des verbes — le type et le rôle ne le voient pas, la **couverture** oui (0,75 et 0,77).
- **Corpus** : 47 lignes, SHA `f2a0d2fb3a9b0a9aebd562b170503f4d1a98251efdc4a3645a2523b5197227a2` ; `verifier_corpus.py` le rejoue.
- **43 tests** verts.

**Commits et push**

- Sous-module : **`90e507b`**, poussé sur `drave-structures` (`647205a..90e507b`).
- Principal : **`e2227509`** (la clôture N2 a intégré la fiche S v3, le manifeste, le pointeur `90e507b`, la roadmap et l'INDEX), poussé : `origin/master` = `e2227509`.
- `docs/pilotage/en-cours.md` porte la ligne S v3 (47/47, 117/117, corpus 47, 43 tests) ; T0 repassé sous 4 000.

**En cours, pas à moi** : la **passe complète des portes** du hub (`work/portes/passe-1102-19h32`, `porte-épisodique` en cours) ; ses mises à jour de `docs/pilotage/` sont encore dans l'arbre, et `reports/pensee-porte-minute.json` est en écriture. Je les laisse au hub. Prochaine action S : homographes/lexique, puis validation humaine de la banque.

### Tour 6 — attends-tu aprèes quelque-chose? on a des ressources qui peuvent en prendre un peu plus

*33 appels d'outils.* Actions notables :

- bash — Inspect CEGEP OCR corpus for real-text measurement
- bash — Assess OCR text quality and plausible sentence count
- bash — Locate clean French corpus for contrast
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/mesure_corpus.py`
- bash — Measure analyzer on 20k CEGEP and clean lines
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/mesure_corpus.py`
- bash — Measure on lines and sentences, 20k each
- bash — Measure on 50k units for stability
- bash — Fix output path, canonicalize 50k JSON
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_mesure_corpus.py`
- bash — Add corpus section to README and run tests
- bash — Commit and push corpus measurement submodule
- bash — Check main state, gate pass, and fiche status
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-corpus-reel.md`
- … et 19 autres

**Synthèse produite :**

⏵ Non : le CPU a servi au corpus réel et à la banque ; tout est committé et poussé.

**Ce qui a été entrepris**

- **Mesure sur corpus réel** (`mesure_corpus.py`, 60 s CPU) : **50 000 lignes** et **20 799 phrases** CEGEP OCR + **50 000** lignes/phrases de littérature propre, avec le **mélange des mots** en contrôle.
  - littérature propre : **65,5 %** de GN+GV (phrases) / **51,0 %** (lignes) contre **9,1 %** / **3,8 %** pour le mélange ;
  - CEGEP OCR : **8,5 %** / **3,6 %** contre **9,1 %** / **3,8 %** — **au plancher du mélange** : corpus multilingue/technique, analyseur français ; ce n'est pas une mesure du français OCR ;
  - couverture **0,94** / **0,89** ; homographes **25**/20 799 et **1 064**/50 000.
- **Banque de candidats réels** (`candidats_corpus.py`) : **200 phrases, 355 candidats**, manifeste SHA-256 `43957a3b…` — de la matière à valider, pas des vérités.
- **46 tests** verts ; fiches [`corpus réel`](reports/rapport-s-corpus-reel.md) et [`analyseur`](reports/rapport-s-analyseur-roles.md).

**Committé et poussé**

- Sous-module : **`97641d5`** (mesure + banque) → `drave-structures` ; le pointeur est dans le principal.
- Principal : **`3f74fe83`** → `origin/master` (la fiche, le manifeste, l'état S, le pointeur, l'INDEX) ; le registre des ressources **`a67dbf00`** du hub est poussé avec.
- État : **562 fiches / 648 JSON**, T0 vert, `en-cours` 1 623 mots.

**Ce qui tourne / ce qui reste**

- Le **GPU** est à N2 (mandat de nuit R1.2 à 1 024 octets, jusqu'à 08 h) et à la passe de portes ; le **CPU** était à S, d'où le registre `tools/ressources.py` du hub (`a67dbf00`) — on peut maintenant réserver explicitement.
- Prochaine action S : **validation humaine des 200 phrases** de la banque (le serveur les charge), puis **homographes/lexique** (`ferme`, `fait`, `lit`) et filtre langue/genre.

### Tour 7 — tiens ta liste de tâches dsh à jour et continue

*28 appels d'outils.* Actions notables :

- todo_write
- bash — Add homograph context rule and test examples
- bash — Add surprend to lexicon and retest homographs
- bash — Add holdout4 and measure context rule
- bash — Update tests for context rule and run
- bash — Re-run corpus measure and bank with context rule
- bash — Update submodule README for v4 context rule
- bash — Export 55-line gold and read exact measures
- bash — Commit and push v4 context rule
- bash — Commit bank manifest timestamp
- bash — Copy 55-line manifest and check main state
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md`
- read
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md`
- … et 12 autres

**Synthèse produite :**

⏵ Liste DSH à jour ; cycle v4 poursuivi et poussé : 54/55 types, 131/131 rôles, 55 structures.

**Ce qui a été fait**

- **Règle de contexte v4** : un mot du lexique de verbes est un **nom** si le suivant est un auxiliaire ou un verbe — `h046` (« la petite ferme est ») et `h047` (« le simple fait surprend ») sont corrigés.
- **Holdout4 écrit après la règle** (`h048–h055`, mesuré une fois) : **54/55 types** (98,2 %), **131/131 rôles**, **47/47 compléments**, couverture **1 466/1 475** (99,4 % ; holdout 762/771, 98,8 %).
- **Limites nommées** : `h050` (« fait » suivi d'un verbe **hors lexique**) et `h053` (« lit » après un adjectif, en fin de phrase).
- **Contrôles** : baseline **94/131** (0,718), règles coupées **96/131** (0,733), rôles mélangés **0,109** [0,00 ; 0,23].
- **Corpus réel** re-mesuré : 65,5 % de GN+GV sur la littérature propre contre 9,1 % pour le mélange ; 8,5 % sur le CEGEP OCR (plancher, multilingue/technique) ; homographes **1 134/28** (suspects, pas erreurs).
- **Banque** : 200 phrases / 355 candidats (SHA `43957a3b…` inchangé) ; **corpus de référence** : 55 lignes, SHA `76accf9d…` ; **47 tests**.

**Committé et poussé**

- Sous-module : **`1445e1d`** (v4) et **`00d2a01`** (manifeste) → `drave-structures`.
- Principal : **`69bfddba`** → `origin/master` ; pointeur `tools/structures` = `00d2a01`.
- Fiches : [`analyseur v4`](reports/rapport-s-analyseur-roles.md) et [`corpus réel`](reports/rapport-s-corpus-reel.md) ; état **564 fiches / 650 JSON**, 82 portes, T0 vert.

**Liste DSH** : les 7 tâches du cycle sont terminées ; restent **`h050`/`h053`** (lexique élargi ou règle de fin de phrase) et la **validation humaine des 200 phrases** de la banque. L'arbre porte encore les mises à jour du hub en cours (portes/état) ; je n'y ai pas touché.

### Tour 8 — prochaine étape?

*1 appels d'outils.* Actions notables :

- bash — Start the structures bank server and verify load

**Synthèse produite :**

⏵ Le banc est lancé : 207 phrases, 369 candidats. La prochaine étape est la **validation humaine**, puis l'export de la banque validée.

**Tout de suite : valider la banque**

- Le serveur tourne sur **http://127.0.0.1:8765** (`pid 1737843`, log `/tmp/structures-serveur.log`).
- Il charge les **7 phrases du banc** (avec leur référence écrite à la main) + les **200 phrases réelles** de la littérature (355 candidats) ; **0 validation** pour l'instant.
- Conseil : valider d'abord les **7 phrases du banc** (elles ont une référence, on peut comparer), puis un **premier lot de 20 phrases réelles** — les verdicts s'écrivent dans `donnees/validations.jsonl` (append-only).
- Ensuite, je fais l'export `python3 exporter_corpus.py --mode banque` → `data/structures/banque-validee.jsonl` + manifeste, avec la fiche : combien de `resolu`/`compatible`/`double_sens`/`exclu`, l'accord avec la référence, les spans vérifiés, et les limites (200 phrases, un seul valideur).

**En parallèle, côté S (CPU)**

- **Filtre langue/genre + segmentation en phrases** : c'est la leçon de la mesure corpus — le CEGEP OCR est au plancher du mélange (8,5 % contre 9,1 %) parce qu'il est multilingue/technique et coupé en lignes. Filtrer le français, reconstruire les phrases, puis refaire le taux de GN+GV : c'est le préalable à une banque issue de l'OCR.
- **`h050`/`h053`** (verbe suivant hors lexique, nom après adjectif en fin de phrase) : petit raffinement, à mesurer sur une nouvelle vague sans retoucher le gold.

**Règle 11 (AGENTS mis à jour)** : le chemin LLM de S (`llm.py`) passe bien par l'**API DeepSeek** ; S n'utilise **aucun serveur local**. Le `llama-server` 7B qui tourne encore (port 18082) est celui de **Pensée** : la règle le déclasse pour les professeurs — le hub/Pensée doit le couper et passer par `tools/llm/enseignant.py`. Les GPU restent à Drave (`porte-ressources`, `hauru-gpu-guard`).

La liste DSH est à jour : banque (humain) et filtre langue/genre en tête, `h050`/`h053` ensuite.

### Tour 9 — pour ce qui est de la validation de la banque, après moins de 20%, j'arrête car j'ai trop de doutes sur l'arvre syntaxiq … [105 caractères tronqués]

*20 appels d'outils.* Actions notables :

- bash — Inspect partial human validations and notes
- bash — Stop bank server and export partial validated bank
- bash — Check server and export partial bank
- bash — Measure current tree depth and unresolved referents
- bash — Commit partial human bank and tree/referent measure
- bash — Copy partial bank manifest and check counts
- bash — Read current S state/roadmap/INDEX
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-banque-partielle.md`
- read
- bash — Get date, counts, and en-cours list
- bash — Update plan/state/roadmap/INDEX for partial bank and recheck
- bash — Trim S state to T0 budget
- bash — Final trim and check S files for commit
- bash — Stage partial bank fact in alternate index
- … et 6 autres

**Synthèse produite :**

⏵ C'est un résultat, pas un échec : la banque s'arrête, et le pourquoi est mesuré et nommé. Je passe à l'arbre réel puis aux référents avant de te redemander quoi que ce soit.

**Le fait, tel qu'il est**

- **142 verdicts sur 71 phrases** ; **81 lectures acceptées sur 65 phrases** (71 `resolu`, 10 `compatible`, 1 `double sens`), **60 `exclu`** ; export partiel **81 lignes**, SHA `2d27b712…`, spans et restitution vérifiés.
- Ton retour est cité verbatim dans la fiche : « il manque trop souvent de profondeur » et « les référents ne semblent pas résolus avant que je tranche ».
- Ce que l'outil montrait : **277/369 candidats** de profondeur maximale **1** (82 de 2, 10 de 0) et **170/207 phrases** avec un pronom/possessif — **371 formes, 0 antécédent proposé**. La note p002 (« l'homme au télescope ») est conservée.
- La banque est **partielle**, pas fausse ; `donnees/validations.jsonl` garde tout. Le serveur est arrêté.

**Committé et poussé**

- Sous-module **`51b6aaf`** : validations, `mesure_arbre.py`, `mesure-arbre.json`, README.
- Principal **`727c4860`** : fiche [`banque partielle`](reports/rapport-s-banque-partielle.md), manifeste, état, roadmap, plan actif ; `origin/master` à jour.
- **47 tests** restent verts ; la règle 11 est respectée côté S (aucun serveur local, `llm.py` → API DeepSeek).

**La prochaine étape, dans cet ordre**

1. **Arbre réel** : `parent`/`enfants`/`profondeur` explicites dans le générateur, rendu indenté — et mesure de la profondeur sur les 200 phrases (le chiffre actuel est 75 % à 1).
2. **Référents** : proposer les antécédents des pronoms/possessifs (GN, sujet, tête de GP), les faire **résoudre avant** le verdict de structure, et les enregistrer avec le verdict.
3. Ensuite seulement, **reprise de la validation** des 200 phrases sur l'outil corrigé, puis export de la banque complète ; `h050`/`h053` restent les limites de l'analyseur, après.

### Tour 10 — vas-y avec des paragraphes complets et un arbre svg avec liaisons référents-référés

*28 appels d'outils.* Actions notables :

- bash — Find a real paragraph with referents
- bash — Locate generator tree insertion points
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py`
- bash — Add tree construction and inspect depths
- bash — Add referent proposal and test on Alice paragraph
- bash — Filter verb-like proper nouns and inspect target tree
- bash — Skip lone prepositions, run tests/measure
- bash — Generate SVG tree with referent links
- bash — Find an SVG renderer for visual check
- bash — Render SVG to PNG for visual check
- bash — Render SVG with inkscape
- read_image
- bash — Measure new tree depth and referent proposal coverage
- … et 12 autres

**Synthèse produite :**

⏵ L'arbre SVG est prêt, avec ses liens référents-référés, et la fiche est écrite en paragraphes complets.

L'arbre demandé est dans [`docs/schemas/arbre-referents.svg`](docs/schemas/arbre-referents.svg) : il part d'un vrai paragraphe d'Alice, place les segments par profondeur réelle (le GV « Elle avait » en racine, puis le GP, le GV « se donner », le GP, la SUB et le GV « quelquefois elle se grondait »), et relie en pointillés les pronoms « Elle », « elle » et « lui » à leur antécédent « Alice », qui vit dans la phrase de contexte. Le fichier a un `viewBox`, un `<title>`, un `<desc>`, des liens relatifs, et il est inscrit dans l'index des schémas ; la vérification `verifier_schemas.py` passe sur les 67 SVG. La fiche [`reports/rapport-s-arbre-referents.md`](reports/rapport-s-arbre-referents.md) raconte le problème, l'arbre, les référents, le SVG, les contrôles et les limites en paragraphes complets, et `donnees/paragraphes.json` porte trois paragraphes réels (cible + contexte + antécédent) comme unité de la banque suivante.

Les chiffres avant/après sont nets. Avant l'arbre, 277 candidats sur 369 s'arrêtaient à une profondeur de 1 ; maintenant, sur 359 candidats, 37 seulement restent à 1, 221 sont à 2 et 99 atteignent 3 ou plus. Pour les référents, l'outil ne proposait aucun antécédent sur 371 formes ; il en propose maintenant pour 294 (79,2 %), et les 77 qui restent sans candidat sont précisément ceux qui demandent le contexte d'un paragraphe — « Elle avait pour habitude… » ne trouve Alice que dans la phrase précédente. Le paragraphe d'Alice sert de contrôle positif : sans contexte, « Elle » n'a aucun candidat ; avec le contexte, il propose Alice, et « elle » et « lui » la retrouvent.

Les limites sont nommées dans la fiche : l'arbre est une heuristique d'attachement, les référents sont des candidats et non une résolution (« habitude » et « conseils » sont proposés à tort, le pronom objet « les » est classé DET et manqué), les trois paragraphes sont peu nombreux, et la banque partielle reste une trace. Cinquante tests couvrent l'arbre, les référents et le SVG ; la revue de documentation, le budget T0 et l'état passent. Le sous-module est poussé en `b18dbac` et le principal en `2b3595c1`, avec le pointeur à jour.

La suite est l'UI du serveur : afficher le contexte, l'arbre et les référents dans la page de validation, et faire résoudre les référents avant le verdict de structure, puis étendre la banque de paragraphes complets et reprendre la validation. Les
… [39 caractères tronqués]

### Tour 11 — quel page web utiliser pour la suite?

*15 appels d'outils.* Actions notables :

- bash — Inspect bank server routes and UI
- bash — Read server data model and routes
- bash — Read analyser output and UI rendering
- bash — Read server tests to extend
- bash — Add paragraph routes and data to server
- bash — Read bank page header for style reuse
- bash — Create paragraph page, export, test
- bash — Commit paragraph page and push submodule
- bash — Relaunch server and verify paragraph page
- bash — Update state for paragraph page and check
- bash — Inspect divergent main state and fiche history
- bash — Inspect L commit deletion of S fiche
- bash — Restore SVG, index, schema reference after L deletion
- bash — Commit page and restore S files
- … et 1 autres

**Synthèse produite :**

⏵ La page est en ligne : `http://127.0.0.1:8765/paragraphes`, avec les trois paragraphes, l'arbre SVG et les référents à trancher.

Pour la suite, la page à utiliser est **http://127.0.0.1:8765/paragraphes**. Le serveur tourne (pid 2414252) et répond 200 sur la page comme sur `/api/paragraphes`. Elle affiche les trois paragraphes complets d'Alice : le contexte en encadré, la cible colorée par segment, l'arbre SVG avec la profondeur réelle et les flèches pointillées des référents, puis les référents sous forme de listes déroulantes — « Elle → Alice » est présélectionné quand Alice est un candidat — et enfin les lectures candidates avec les quatre verdicts. La bonne séquence est de trancher d'abord les référents, puis la structure : le verdict enregistre les deux dans `donnees/paragraphes-validations.jsonl`, et le lien « exporter les verdicts » télécharge ce journal en NDJSON. Le banc de phrases d'origine reste sur `/`, avec son propre journal.

Le serveur a été relancé après l'ajout de la page et les 51 tests passent. Le sous-module est poussé en `0422a8c` et le principal en `08418b55`. Au passage, le commit L avait supprimé la fiche S et le SVG de l'arbre ; je les ai rétablis dans ce commit, avec la ligne de l'index des schémas et celle de l'INDEX des fiches.

Il reste à valider les trois paragraphes sur cette page ; ensuite j'étendrai l'échantillon de paragraphes complets, puis nous reprendrons l'export complet de la banque. Les limites `h050`/`h053` restent après. Si le serveur s'arrête, il se relance avec `cd tools/structures && python3 serveur.py` puis la même adresse.

### Tour 12 — les svg sortent du cadre, prévoir scrollbar et largeur de page adapté à la largeur d'écran ou fenêtre

*12 appels d'outils.* Actions notables :

- bash — Measure SVG content bounds and CSS widths
- bash — Read CSS layout and SVG layout code
- bash — Read SVG layout block to rewrite
- bash — Dynamic SVG viewBox and check all three fit
- bash — Responsive CSS, natural SVG with scroll, frame test
- bash — Restart server, verify SVGs and responsive page
- bash — Locate README/fiche/state lines to update
- bash — Commit responsive SVG fix and push submodule
- bash — Update fiche/state for responsive frame fix
- bash — Inspect L deletions, counters, pointer
- bash — Commit responsive frame fix and restore S files
- bash — Push frame fix and verify live page

**Synthèse produite :**

⏵ Les SVG restent dans leur cadre, la page s'adapte à la fenêtre et l'arbre défile dans son cadre.

Le débordement venait du `viewBox` fixe de 1 020 px : l'arbre du troisième paragraphe allait jusqu'à 1 097,5 px, et les jetons des référents poussaient encore plus loin. Le `viewBox` est maintenant **calculé** à partir du niveau le plus large, des jetons et du contexte : 1 020 × 550 pour l'exemple, 1 398 × 550 pour a002 et 1 613 × 550 pour a003. Un test vérifie sur les trois paragraphes que chaque rectangle — nœuds, jetons, contexte — reste dans le cadre.

La page est **responsive**. Le header, la légende et le main sont bornés à 1 180 px, centrés, et le corps ne déborde plus horizontalement ; les longues phrases passent à la ligne. L'arbre garde sa largeur naturelle et **défile horizontalement** dans son propre cadre, avec une barre de défilement fine, quand la fenêtre est plus étroite : le SVG ne sort plus de la carte, il se parcourt. Le banc de phrases d'origine profite des mêmes règles.

Le serveur a été relancé (pid 2430607) et la page répond 200 ; recharge `http://127.0.0.1:8765/paragraphes` (un Ctrl+F5 si le CSS est resté en cache). Les 52 tests passent, le sous-module est poussé en `4d3a3ca` et le principal en `ef530713`. La fiche et le SVG, de nouveau retirés par un commit L, ont été rétablis au passage. Il reste à valider les trois paragraphes sur cette page.

### Tour 13 — tu peux aussi valider le sens (et indirectement les référents de syntaxe) en utilisant des traductions.

*15 appels d'outils.* Actions notables :

- bash — Inspect S LLM client and API key
- web_fetch
- bash — Add English sources to paragraphs, page, test
- bash — Expose English source in API and rerun tests
- bash — Restart server and verify English source in API/page
- bash — Print referent forms for translation table
- bash — Fix a003 context to name Alice and verify referents
- bash — Default personal referents to Alice, test a003
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-traductions.md`
- bash — Commit translation validation and push submodule
- bash — Check main state before translation commit
- bash — Inspect L deletions and S files to restore
- bash — Read S state and HEAD index lines
- bash — Update state for translation and run checks
- … et 1 autres

**Synthèse produite :**

⏵ La traduction comme contrôle du sens et des référents : je récupère la source anglaise d'Alice et je la confronte aux trois paragraphes.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md` | 3 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/gold-analyseur.json` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py` | 0 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/mesure_analyseur.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_corpus.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/verifier_corpus.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md` | 5 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 7 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/mesure_corpus.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_mesure_corpus.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-corpus-reel.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/candidats_corpus.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-banque-partielle.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-arbre-referents.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-traductions.md` | 1 | 0 |

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
- … et 242 autres

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
- **T5** `0, Quadro RTX 5000, 0 %, 688 MiB, 16384 MiB`
- **T5** `1, Quadro RTX 5000, 43 %, 966 MiB, 16384 MiB`
- **T5** `- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 intérieur, ×62,7 tout ; [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../reports/rapport-typogly`
- **T6** `cegep           1.97   3.6%    0.4%    0.94       10              8`
- **T6** `propre          4.32  50.8%   10.8%    0.89      217            215`
- **T6** `melange         2.07   3.9%    0.5%    0.94       11             11`
- **T6** `cegep           1.97   3.6%    0.4%    0.94       10               8`
- **T6** `propre          4.32  50.8%   10.8%    0.89      217             215`
- **T6** `melange         2.07   3.9%    0.5%    0.94       11              11`
- **T6** `cegep           3.24   8.4%    0.8%    0.94       24              24`
- **T6** `propre          6.89  65.5%    8.0%    0.89      388             381`
- **T6** `melange         4.11   9.3%    0.4%    0.93       23              23`
- **T6** `cegep           1.96   3.6%    0.5%    0.94       18              15`
- **T6** `propre          4.33  51.0%   10.2%    0.89      553             550`
- **T6** `melange         2.07   3.8%    0.5%    0.94       18              18`
- **T6** `cegep           3.25   8.5%    0.8%    0.94       25              25`
- **T6** `propre          6.93  65.5%    8.0%    0.89     1064            1035`
- **T6** `melange         4.11   9.1%    0.4%    0.93       22              22`
- **T6** `162:| phrase | CEGEP | 8,5 % | 0,8 % | 0,94 | 25 |`
- **T6** `168:OCR**, il est au **plancher du mélange** (8,5 % contre 9,1 %) : ce corpus est **multilingue et`
- **T6** `262:  propre contre 9,1 % pour les mots mélangés, 8,5 % contre 9,1 % sur le CEGEP OCR (multilingue et`
- **T6** `[master 140feb6] S — L'ANALYSEUR LIT LE FRANÇAIS PROPRE (65,5 %), PAS LE CEGEP OCR (8,5 %, PLANCHER DU MÉLANGE)`
- **T6** `140feb6 S — L'ANALYSEUR LIT LE FRANÇAIS PROPRE (65,5 %), PAS LE CEGEP OCR (8,5 %, PLANCHER DU MÉLANGE)`
- **T6** `[master 3f74fe83] S — LE CORPUS RÉEL (65,5 % PROPRE / 8,5 % CEGEP, PLANCHER DU MÉLANGE) ET LA BANQUE 200 PHRASES / 355 CANDIDATS`
- **T7** `cegep           1.96   3.6%    0.5%    0.94       21              18`
- **T7** `propre          4.33  51.0%   10.2%    0.89      578             575`
- **T7** `melange         2.07   3.8%    0.5%    0.94       19              19`
- **T7** `cegep           3.25   8.5%    0.8%    0.94       28              28`
- **T7** `propre          6.93  65.5%    8.0%    0.89     1134            1104`
- **T7** `melange         4.11   9.1%    0.4%    0.93       23              23`
- **T7** `166:| phrase | propre | 65,5 % | 8,0 % | 0,89 | 1 134 |`
- **T7** `31:| ligne | CEGEP | 3,6 % | 0,5 % | 0,94 | 18 | 15 |`
- **T7** `32:| ligne | propre | **51,0 %** | 10,2 % | 0,89 | 553 | 550 |`
- **T7** `33:| ligne | mélange | 3,8 % | 0,5 % | 0,94 | 18 | 18 |`
- **T7** `35:| phrase | propre | **65,5 %** | 8,0 % | 0,89 | 1 064 | 1 035 |`
- **T7** `| ligne | CEGEP | 3,6 % | 0,5 % | 0,94 | 18 | 15 |`
- **T7** `| ligne | propre | **51,0 %** | 10,2 % | 0,89 | 553 | 550 |`
- **T7** `| ligne | mélange | 3,8 % | 0,5 % | 0,94 | 18 | 18 |`
- **T7** `| phrase | CEGEP | 8,5 % | 0,8 % | 0,94 | 25 | 25 |`
- **T7** `| phrase | propre | **65,5 %** | 8,0 % | 0,89 | 1 064 | 1 035 |`
- **T7** `| phrase | mélange | 9,1 % | 0,4 % | 0,93 | 22 | 22 |`
- **T7** `- **Le filtre** sélectionne les lignes plausibles (20–300 car., ≥ 4 mots, ≥ 80 % de lettres) : les`
- **T7** `35:| phrase | propre | **65,5 %** | 8,0 % | 0,89 | 1 134 | 1 104 |`
- **T7** `- **Fait** : types **47/47**, rôles **117/117** ; contrôles **80/117**, **82/117**, **0,109** ; h033 corrigé, **h046/h047** nommés ; **corpus réel** : GN+GV **8,5 %** CEGEP (mélange 9,1 %), **65,5 %**`
- **T7** `98:- **S — le banc de structures** : **analyseur 47/47 types, 117/117 rôles, 47/47 compléments**, **corpus réel 8,5 % CEGEP / 65,5 % propre** (mélange 9,1 %), gold **47**, **46 tests** ; corpus **47**`
- **T7** `34:| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v3** : frontière GN-devant-verbe, gold **47** phrases ; analyseur **47/47** types, **117/117** rôles`
- **T7** `- **S — le banc de structures** : **analyseur 47/47 types, 117/117 rôles, 47/47 compléments**, **corpus réel 8,5 % CEGEP / 65,5 % propre** (mélange 9,1 %), gold **47**, **46 tests** ; corpus **47** st`
- **T9** `- **Fait** : types **54/55**, rôles **131/131** ; contrôles **94/131**, **96/131**, **0,109** ; h033/h046/h047 corrigés, **h050/h053** limites nommées ; **corpus réel** : GN+GV **8,5 %** CEGEP (mélang`
- **T9** `34:| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v4** : règle de contexte des homographes, gold **55** phrases ; analyseur **54/55** types, **131/131`
- **T9** `563:| [rapport-s-analyseur.md](rapport-s-analyseur.md) | S — L'analyseur contre les structures écrites à la main : 7/7 séquences, 93,9 % de couverture |`
- **T9** `564:| [rapport-s-corpus-reel.md](rapport-s-corpus-reel.md) | S — L'analyseur lit le français propre (65,5 % de GN+GV), pas le CEGEP OCR (8,5 %, plancher du mélange) |`
- **T10** `- **Fait** : types **54/55**, rôles **131/131** ; h050/h053 nommées ; **corpus réel** 8,5 %/65,5 % (mélange 9,1 %) ; **banque partielle** : **142** verdicts/71 phrases, **81** lectures/65, arrêt humai`
- **T12** `67:.ctx { width: 100%; background: #0d1117; color: var(--texte); border: 1px dashed var(--bord);`
- **T12** `72:        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1020 %d" width="1020" height="%d" '`
- **T12** `'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1020 %d" width="1020" height="%d" '`
- **T12** `55:pointillées** à Alice. Le SVG a un `viewBox` (1020 × 550), un `<title>`, un `<desc>`, des liens`
- **T12** `50:- **Fait** : types **54/55**, rôles **131/131** ; **corpus réel** 8,5 %/65,5 % ; **banque partielle** 142/71, 81/65 ; **arbre** 99 candidats à ≥3, **référents** 294/371 ; **page `/paragraphes`** ; `
- **T13** `50:- **Fait** : types **54/55**, rôles **131/131** ; **corpus réel** 8,5 %/65,5 % ; **banque partielle** 142/71, 81/65 ; **arbre** 99 candidats à ≥3, **référents** 294/371 ; **page `/paragraphes`** (r`
- **T13** `- **Fait** : types **54/55**, rôles **131/131** ; **corpus réel** 8,5 %/65,5 % ; **banque partielle** 142/71, 81/65 ; **arbre** 99 candidats à ≥3, **référents** 294/371 ; **page `/paragraphes`** (resp`

## 5. Erreurs rencontrées

11 sorties en erreur ou divergentes. Les premières :

- **T1** : __pycache__/ *.pyc reports/*.tmp models/ data/ qtrinet-core/target/  # Traces de session : la copie brute reste sur disque (volumineuse, binaire), # le digest markdown est versionné. journal/sessions/
- **T1** : === data suivis === count: 0 === reports json exemples === reports/b102bis-corpus-jw.json reports/campagne-benefices/051-R-annexe-manifeste-des-journaux.md reports/corpus-genres.json reports/corpus-li
- **T1** : ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)   ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/w
- **T1** : p001 dev [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module>   File "<stdin>", line 6, in <genexpr> TypeError: list indices must be integers or slices, not str [exit code
- **T1** : 57048   57032       02:18 00:00:00  0.0 S    /bin/sh .git/hooks/pre-commit   59838   57048       01:05 00:00:47 73.3 R    python3 tools/session_report.py --quiet === io === PID 59838     ELAPSED     T
- **T1** : #!/usr/bin/env python3 """Produit, pour chaque session DSH, un rapport qui reconstitue son essence et démontre le travail accompli, étape par étape.  Sortie, à côté du digest brut :    journal/session
- **T5** : === WIP mtimes === -rw-------. 1 stephane stephane 14355 18:49:42 reports/rapport-n2-r11.md -rw-------. 1 stephane stephane 82670 18:52:50 tools/bloc_linguistique.py -rw-------. 1 stephane stephane 11
- **T5** : {     "version": 2,     "mode": "gold",     "date": "2026-11-02T19:40:35",     "source": "tools/structures/donnees/gold-analyseur.json",     "sortie": "data/structures/banque.jsonl",     "phrases": 47
- **T6** : [stderr]   ✅ index : aucun fait stagé sans état fatal: Unable to create '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.git/index.lock': File exists.  Another git process seems to be running in this
- **T9** : [stderr]   ✅ index : aucun fait stagé sans état fatal: cannot lock ref 'HEAD': is at 229c5bf16e5e5bf09c0c93d7c274e614c73899b0 but expected d255588d2e4ee2d98482dd9aed6e6b4e64f5950d [exit code: 128]
- **T10** : convert: attempt to perform an operation not authorized by the security policy `SVG' @ error/module.c/OpenModule/1273. convert: no decode delegate for this image format `SVG' @ error/constitute.c/Read

## 6. Commits

- S — L'ANALYSEUR NOMME LES RÔLES : 99/100, 38/39 TYPES ; LE CORPUS DE 39 STRUCTURES SORT" -m "Le générateur gagne des rôles contextuels (possession/thème, instru
- S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES" -m "Le sous-module tools/structures est committé dan
- ps -eo pid,etime,cmd | grep -E "git commit|archive_sessions|journal_auto|session_report|python3" | grep -v grep | head -20; echo "=== index lock ==="; ls -la /h
- ps -eo pid,ppid,etime,pcpu,stat,cmd | grep -E "57032|57052|57681|job|git commit" | grep -v grep; echo "=== enfants ==="; ps --ppid 57032 -o pid,etime,pcpu,stat,
- S — L'ÉTAT INTÈGRE L'ANALYSEUR RÔLES : 38/39 TYPES, 99/100 RÔLES, 39 STRUCTURES" -m "La fiche reports/rapport-s-analyseur-roles.md, le manifeste reports/s-banqu
- ÉTAT — COMPTEURS AU DISQUE (552 FICHES / 639 JSON) ; LA FICHE S EST INTÉGRÉE" -m "Le compteur passe à 552 fiches / 639 JSON après l'intégration de la fiche S et
- D/R/A — LA DÉTECTION CEGEP SÉPARE 147 SCANS DE 2 681 PDF ; L'OCR PASSE À LA LISTE EXPLICITE" -m "La détection sur le texte intégral (pdftotext + pdfinfo, seuil 
- S — LA FRONTIÈRE DU GN S'ARRÊTE DEVANT LE VERBE : 47/47 TYPES, 117/117 RÔLES ; GOLD 47" -m "Le générateur gagne un lexique de verbes finis (frontière GN) et le 
- S — L'ANALYSEUR LIT LE FRANÇAIS PROPRE (65,5 %), PAS LE CEGEP OCR (8,5 %, PLANCHER DU MÉLANGE)" -m "mesure_corpus.py : 50 000 lignes et 20 799 phrases CEGEP, 50
- S — LA BANQUE DE CANDIDATS RÉELS : 200 PHRASES, 355 CANDIDATS, MANIFESTE SHA-256" -m "candidats_corpus.py : 200 phrases de la littérature propre (filtre 40-200 
- S — LE CORPUS RÉEL (65,5 % PROPRE / 8,5 % CEGEP) ET LA BANQUE 200/355 ; N2 — LE MANDAT DE NUIT ET L'OUTIL RESSOURCES" -m "S — mesure_corpus.py sur 50 000 lignes
- S — LE CORPUS RÉEL (65,5 % PROPRE / 8,5 % CEGEP, PLANCHER DU MÉLANGE) ET LA BANQUE 200 PHRASES / 355 CANDIDATS" -m "mesure_corpus.py : 50 000 lignes et 20 799 p
- S — LE CONTEXTE TRANCHE LES HOMOGRAPHES : 54/55 TYPES, 131/131 RÔLES ; GOLD 55" -m "Le GN ne s'arrête plus devant « ferme »/« fait » quand le suivant est un aux
- S — BANQUE : LE MANIFESTE REPREND LA DATE DU RESCAN (SHA 43957a3b INCHANGÉ)" -m "La banque de 200 phrases / 355 candidats est identique (sha256 43957a3b…) ; seu
- S — LE CONTEXTE TRANCHE LES HOMOGRAPHES : 54/55 TYPES, 131/131 RÔLES ; GOLD 55 (SHA 76accf9d)" -m "Le GN ne s'arrête plus devant « ferme »/« fait » quand le sui
- S — LA BANQUE PARTIELLE : 142 VERDICTS, 81 LECTURES / 65 PHRASES ; L'ARRÊT HUMAIN EST MESURÉ (ARBRE 1, RÉFÉRENTS 0)" -m "La validation humaine s'arrête : arbre 
- S — LA BANQUE PARTIELLE : 142 VERDICTS, 81 LECTURES/65 PHRASES ; L'ARRÊT HUMAIN (ARBRE 1, RÉFÉRENTS 0) EST MESURÉ" -m "La validation humaine s'arrête après 142 
- S — LA BANQUE PARTIELLE : 142 VERDICTS, 81 LECTURES/65 PHRASES ; L'ARRÊT HUMAIN (ARBRE 1, RÉFÉRENTS 0) EST MESURÉ" -m "La validation humaine s'arrête après 142 
- S — L'ARBRE A UNE PROFONDEUR ET LES RÉFÉRENTS SONT PROPOSÉS : 99 CANDIDATS À ≥3, 294/371 FORMES ; SVG ALICE" -m "construire_arbre() donne un père et une profond
- S — ARBRE ET RÉFÉRENTS : 99 CANDIDATS À ≥3, 294/371 FORMES, SVG ALICE" -m "construire_arbre() donne un père et une profondeur réelle : 359 candidats, 37 de prof
- S — LA PAGE /PARAGRAPHES : ARBRE, RÉFÉRENTS ET VERDICT ; 51 TESTS" -m "Le serveur sert /paragraphes : les trois paragraphes complets (contexte, cible, antécéden
- S — LA PAGE /PARAGRAPHES : ARBRE, RÉFÉRENTS, VERDICT ; LE BANC PEUT REPRENDRE" -m "Le serveur sert /paragraphes : les trois paragraphes complets (contexte, cibl
- S — LES SVG RESTENT DANS LEUR CADRE : VIEWBOX CALCULÉ, PAGE RESPONSIVE, DÉFILEMENT ; 52 TESTS" -m "Le viewBox est calculé depuis le niveau le plus large, les je
- S — LES SVG RESTENT DANS LEUR CADRE : VIEWBOX CALCULÉ, PAGE RESPONSIVE, DÉFILEMENT ; 52 TESTS" -m "Le viewBox est calculé depuis le niveau le plus large, les je
- S — LA TRADUCTION CONTRÔLE LE SENS : 14/14 RÉFÉRENTS ANAPHORIQUES CONFIRMÉS PAR L'ANGLAIS, « LES » → « IT » RETROUVÉ" -m "Les trois paragraphes français sont co
- S — LA TRADUCTION CONTRÔLE LE SENS : 14/14 RÉFÉRENTS ANAPHORIQUES CONFIRMÉS, « LES » → « IT » RETROUVÉ ; SOURCE ANGLAISE DANS LA PAGE" -m "Les trois paragraphes


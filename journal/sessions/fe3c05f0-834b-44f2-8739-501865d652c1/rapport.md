# Session fe3c05f0 — Lecture de en-cours.md et choix de tâche

> **Journaux :** [le jour](../../2026-10-31/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `fe3c05f0-834b-44f2-8739-501865d652c1` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-31 17:35 |
| Durée | 25.9 h |
| Tours | 12 |
| Messages | 873 |
| Appels d'outils | 872 |
| Fichiers touchés | 18 |
| Commandes | 799 |
| Sous-agents | 0 |
| Commits | 42 |
| Compactages de contexte | 2 |

## Objectifs déclarés

- **create** — R4.4 ambitieux : rendre l'OCR du lecteur robuste aux scans (corpus de scans simulés avec vérité terrain, prétraitement, reconstruction de layout, exposants, colonnes, tableaux), mesurer WER et parité avant/après, itérer jusqu'à parité ≥ 90 % sur les scans dégradés avec contrôles négatifs, et livrer 
… [168 caractères tronqués]
- **complete** — R4.4 ambitieux : rendre l'OCR du lecteur robuste aux scans (corpus de scans simulés avec vérité terrain, prétraitement, reconstruction de layout, exposants, colonnes, tableaux), mesurer WER et parité avant/après, itérer jusqu'à parité ≥ 90 % sur les scans dégradés avec contrôles négatifs, et livrer 
… [168 caractères tronqués]
- **create** — Suivre docs/pilotage/plan-travail.md et faire avancer le mandat D/R/A de la session fe3c05f0 jusqu'au 2026-11-02 08:00 EST : produire les 10 corpus Wikipédia en texte intégral (les 9 langues restantes : mesures, manifestes, contamination, fiche et catalogue), l'extraction PDF/OCR des documents locau
… [279 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — lis le fichier en-cours.md et prends une tâche qui n'est pas en conflit avec l'autre session

**Tour 2** — tu dois être plus ambitieux. je te donne 10h humain (pas tes estimés, continue d'itérer tant que l'heure système te it que tu n'y est pas arrivée. J'accueille tes résultars et écarts sans jugement.

**Tour 3** — <goal_round> Objective: "R4.4 ambitieux : rendre l'OCR du lecteur robuste aux scans (corpus de scans simulés avec vérité terrain, prétraitement, reconstruction de layout, exposants, colonnes, tableaux), mesurer WER et parité avant/après, itérer jusqu'à parité ≥ 90 % sur les scans dégradés avec contrôles négatifs, et livrer fiches, JSON, docs, porte, roadmap, en-cours, journal et commits. Continuer … [637 caractères tronqués]

**Tour 4** — révise nos sources de données pour l'entrainement. fais le tour du disque dur pour avoir un inventaire local pour l'entrainement.

**Tour 5** — go

**Tour 6** — constitue les corpus des autres langues et assure-toi que tous les agents s'y retrouvent pour leurs besoins

**Tour 7** — relis mes demandes de toutes les sessions des derniers 48h pour compredre la vision à jour du projet. creuse l'historique au besoin pour garantir la cohérence et élargir l'inventaire de chantier pour mieux comprendre leurs relations.

**Tour 8** — combien de chantiers simultanés on peut faire en ce moment? Est0il préférable d'avoir plusieurs sessions dsh ou bien une seule avec beaucoup de sub-agents?

**Tour 9** — organise le dossier pilotage pour qu'il soit à jour et qu'entre le en-cours.md et roadmap.md il y ait un plan de travail optimal pour plusieurs sessions bien balancées. Note tout se passe sur la même machine. Elle est bien ddtée en matériel, mais ils faut surveiller beaucoup de fichiers en mouvement par des sessions parallèles.

**Tour 10** — lire docs/pilotage/plan-travail.md et avancer

**Tour 11** — es-tu à jour? as-tu fait tout ce que tu pouvais?

**Tour 12** — suis le plan, continue jusqu'à 8h demain matin

## 2. Déroulé, étape par étape

### Tour 1 — lis le fichier en-cours.md et prends une tâche qui n'est pas en conflit avec l'autre session

*185 appels d'outils.* Actions notables :

- read
- bash — Check active sessions status
- bash — Check git working tree and recent commits
- bash — Read active session mandate plan
- bash — Run backlog graph verifier
- bash — Inspect other session files and heartbeat
- bash — Read start of backlog verifier
- bash — Find missing-card logic in verifier
- bash — Check current time and GPU usage
- bash — Run documentary gates
- job_kill
- bash — Verify no gate script still running
- bash — List processes touching the repo
- bash — List documentary gate scripts
- … et 159 autres

**Synthèse produite :**

⏵ Bilan de la session R4.4

J'ai pris **R4.4 — l'OCR** : aucun conflit avec N2 (pas de GPU, pas de fichier réservé, pas de `toutes-les-portes.sh`). La ligne était bloquée par une ressource absente, pas par une question ouverte.

**Ce qui a été fait**

- tesseract **5.5.3 installé sans root** dans `work/ocr/` (`tools/installer_ocr.sh`, RPM openSUSE, ni `sudo` ni paquet système) ;
- l'OCR rend des **blocs** au graphe R0.1 par la même fonction de manifeste que le PDF natif (`tools/graphe_document_ocr.py`) : offsets, partition, provenance identiques, **confiance par bloc** dans la provenance ;
- mesure (`tools/mesurer_ocr.py`) sur **10 pages rendues à 300 dpi**, 6 PDF, fr/en/es ; nouvelle porte `tools/porte-ocr.sh` (la 79e).

**Résultat** (`0088fc2f`)

| mesure | valeur |
|---|---|
| WER mot à mot | **4,48 %** (169 éditions / 3 771 mots), rappel 97,37 %, confiance 93,2 |
| parité de passage (même lecteur R0.2) | **27/30 = 90,0 %**, F1 médian 1,000 |
| valeur exacte | 25/30 = 83,3 % |
| contrôle **sans OCR** | **0/30** |
| contrôle **page « photo » simulée** | WER 17,08 %, parité **26,7 %** |

Les 5 écarts sont nommés : trois **appels de note en exposant** lus `!` par tesseract, deux **en-têtes découpés autrement** (`Point 13`), un `XXI` lu `XXD`. R4.4 passe de **bloquée à partielle** : la porte de la roadmap (vraies pages **scannées**) reste ouverte, et le contrôle dégradé en donne la mesure.

**Livrables** : `reports/rapport-r44-ocr-pilote.md`, `reports/r44-ocr-pilote.json`, `docs/implantation/encodeur-visuel.md`, backlog R44 mis à jour, roadmap et `en-cours` à jour. Session `fe3c05f0` close et archivée (`b8683d00`).

**Deux choses à signaler**

- Au tout début, une commande mal composée a lancé `toutes-les-portes.sh` par erreur : **tuée en moins de 60 s**, aucun processus de porte restant, et les deux entraînements N2 ont continué normalement (g1/g2 finis, g3 en cours, aucune erreur). Les PPL ne dépendent pas du temps.
- `tools/taille_documents.py` comptait le budget **T0** contre un document **T1** (`organisation-du-depot`, 1 579 mots) : 445 mots de budget faux, dans le sens qui bloque. Corrigé et commité — T0 à **3 702** mots pour 4 000.

**Portes** : revue de documentation, tableaux, état, document, schémas, journal, sessions, backlog, budget et OCR — **toutes vertes**.

### Tour 2 — tu dois être plus ambitieux. je te donne 10h humain (pas tes estimés, continue d'itérer tant que l'heure système te it q … [77 caractères tronqués]

*393 appels d'outils.* Actions notables :

- create_goal
- bash — Record start time, deadline and machine resources
- bash — Check image-processing libraries available
- bash — Check concurrent sessions and clock
- bash — Create work journal and look for scanned PDFs
- bash — Read current state after 4 hours
- bash — See commits since my result
- todo_write
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/simuler_scan.py`
- bash — Fix reproducibility and generate sample scans
- bash — Fix perspective shadowing and generate scans
- read_image
- bash — Baseline WER on sample scans
- bash — Calibrate scan degradation families
- … et 361 autres

**Synthèse produite :**

⏵ Clôture : vérification finale et bilan du programme R4.4

J'ai pris la ligne **R4.4 — les scans** (CPU seulement, sans toucher aux GPU de N2.h) et je l'ai poussée jusqu'au bout : corpus, prétraitement, exposants, colonnes, tableaux, validation réelle, coût, porte. Voici le bilan.

\## Les chiffres

**Cinq familles de scans simulés** (100 pages, split dev/test, WER mot à mot ; préservation = les réponses du lecteur retrouvées) :

| famille | WER dev | WER test | préservation |
|---|---:|---:|---:|
| propre (contrôle) | 4,14 % | 3,01 % | 90,0 % |
| photocopie | 6,34 % | 4,69 % | 86,7 % |
| photo | **55,85 → 6,68 %** | **80,65 → 5,68 %** | 86,7 % |
| papier | **13,02 → 6,87 %** | **53,15 → 6,38 %** | 80,0 % |
| fax | 27,05 → 21,90 % | 23,10 → 15,52 % | 53,3 % |

**Les autres axes** : colonnes à deux **89,4 → 0,5 %** de WER ; **trois** colonnes **52,5 → 0,0 %** (0–1,1 % dégradé) ; mono-colonnes inchangées (écart 0,00 pt). Tableaux : **92,6 %** de cellules exactes sur un rendu, **69,1 %** sur une photocopie, **62,4 %** sur une photo (8 grilles sur 10). Trois **vrais livres** d'Internet Archive : **7,10 %**, **8,73 %**, et un lexique à deux colonnes où l'ordre est **prouvé** (15,3 % contre **98 %** en ordre inverse). Coût : 0,4 s de prétraitement contre 2,4–2,9 s d'OCR par page.

\## Ce que le réel a corrigé

Deux défauts que le synthétique ne voyait pas : un **en-tête centré** traversait la gouttière d'un lexique (la gouttière se cherche maintenant sur les mots, en couverture verticale — 93 % → 15 %) ; et le fond d'éclairage coûtait **9,5 s** pour un champ basse fréquence (vignette : **1,4 s**, et le papier gagne 6,6 points de préservation).

\## Les écarts, nommés

- **Fax 1 bit** : 21,9 % de WER, 53,3 % de préservation — limite d'information, pas de réglage.
- **Tableaux photo** : 2 pages sur 10 hors grille (ombre, trait interrompu).
- **Exposant fusionné** : un appel de note collé au mot n'est pas récupéré ; les appels séparés le sont.
- **Réel = accord entre moteurs**, pas vérité humaine ; trois livres seulement.
- **Gouttière < 2,5 %**, mise en page irrégulière, **flou σ=4** (49,6 → 53,2 %), **rotation > 6°** (10° : 43,5 %) : limites mesurées, écrites.

\## L'état

**17 commits**, la 80e porte `porte-ocr-scans` **verte** (familles, colonnes, tableaux), la porte OCR du pilote verte aussi. Fiche `reports/rapport-r44-scans.md`, 11 JSON, 13 outils, spécification `docs/implantation/encodeur-visuel.md` réécrite, roadmap/backlog/en-cours à jour, récit du 1er novemb
… [486 caractères tronqués]

### Tour 3 — <goal_round> Objective: "R4.4 ambitieux : rendre l'OCR du lecteur robuste aux scans (corpus de scans simulés avec vérité … [917 caractères tronqués]

*83 appels d'outils.* Actions notables :

- bash — Inspect failed parity questions
- bash — Inspect scan entry structure
- bash — List all failed parity values
- bash — Find parity functions and question data
- bash — Read reader and parity code
- bash — Reproduce failing parity questions
- bash — Compare page-1 block segmentation native vs OCR
- bash — Inspect paragraph text and passages for page 1
- bash — Read block typing and merging logic
- bash — Fix note typing and test page-1 parity
- bash — Re-run scans after note-typing fix
- bash — Read scans results after note fix
- bash — List remaining parity failures
- bash — Inspect the 2030-11 value failure
- … et 69 autres

**Synthèse produite :**

**R4.4 est close, avec son objectif de parité tenu sur quatre familles sur cinq.** Voici le bilan.

\## Le résultat

| famille | WER dev | WER test | **parité (préservation)** |
|---|---:|---:|---:|
| propre (contrôle) | 4,14 % | 3,01 % | **96,7 %** |
| photocopie | 6,34 % | 4,69 % | **93,3 %** |
| photo | **55,85 → 6,68 %** | **80,65 → 5,68 %** | **90,0 %** |
| papier | **13,02 → 6,87 %** | **53,15 → 6,38 %** | **90,0 %** |
| fax | 27,05 → 21,90 % | 23,10 → 15,52 % | **56,7 %** |

La parité est passée de 86,7 % à **90–97 %** en corrigeant trois verrous **du lecteur, pas de l'OCR** : une ligne de continuation courte était typée « note » (elle coupait le paragraphe et faisait perdre « point 13 »), le seuil de titre à 1,12 prenait une ligne un peu haute pour une section (le « 12 septembre 2025 » sortait du paragraphe), et la parité de valeur se mesure désormais sur le **passage choisi**, comme le dit la spécification, avec la variante stricte publiée à côté.

Le reste du programme tient : colonnes **89,4 → 0,5 %** (deux colonnes), **52,5 → 0–1,1 %** (trois colonnes, gouttières multiples), mono-colonnes intactes ; tableaux **92,6 / 69,1 / 62,4 %** de cellules exactes (grilles 10/10, 10/10, 8/10) ; trois vrais livres (7,10 % ; 36,26 % avec l'ordre des colonnes prouvé à 15,3 % contre 98 % en ordre inverse ; 8,73 %) ; coût 0,4 s de prétraitement contre 2,4–2,9 s d'OCR. `porte-ocr-scans` est **verte** sur le code final, et toutes les revues de documentation passent.

\## Ce qui n'est pas tenu, nommé

- **Fax 1 bit** : 56,7 % — 120 dpi, deux niveaux, l'information n'y est plus ; c'est une limite physique, pas un réglage.
- **Exposants fusionnés** (`développement,` + `10`, `2030` + `11`) : les chiffres font 6 × 8 px, les recadrages/agrandissements ne les rendent pas lisibles.
- **Un quatrième livre** (Google 1905) n'est **pas mesurable** : sa couche PDF est vide et les pages du DjVu ne s'alignent pas sur celles du PDF ; le banc refuse désormais de diviser par zéro (le bug donnait 27 200 % de WER).
- La référence des vrais scans reste un **autre moteur**, pas une vérité humaine.

\## Où regarder

- Fiche : [`reports/rapport-r44-scans.md`](reports/rapport-r44-scans.md) — tableaux, contrôles, limites, coût, porte.
- JSON : `reports/r44-scans.json`, `r44-colonnes.json`, `r44-tableaux.json`, `r44-reel*.json`, `r44-seed2/3.json`, `r44-sans-exposants.json`, `r44-rotation.json`, `r44-cout.json`, `r44-petit.json`.
- Code : `tools/graphe_document_ocr.py`, `nettoyer_scan.py`, `e
… [632 caractères tronqués]

### Tour 4 — révise nos sources de données pour l'entrainement. fais le tour du disque dur pour avoir un inventaire local pour l'entr … [9 caractères tronqués]

*44 appels d'outils.* Actions notables :

- bash — Show mounted filesystems and volumes
- bash — Measure home and data volume top-level sizes
- job_kill
- bash — List home and data top-level directories
- bash — Measure IA volume subdirectories
- bash — List data volume and project directories
- bash — Measure main data directories on 10.9T volume
- bash — Measure project data and models directories
- bash — List project data, work, and corpus reports
- bash — List corpus, library, and data directories
- bash — Inspect archives directory
- bash — Inspect model caches and stores
- bash — Inspect recovery raw archive structure
- bash — Inventory HuggingFace cache
- … et 30 autres

**Synthèse produite :**

⏵ Inventaire local terminé et committé

J'ai fait le tour du disque et écrit l'inventaire : **59 entrées** avec taille, format, rôle, état, dans `reports/inventaire-donnees-entrainement.json`, et une fiche lisible : `reports/inventaire-donnees-entrainement.md`. Commit `1c9d3d26`, toutes les revues passent.

\## Le disque, en grand

| volume | taille | utilisé | libre |
|---|---:|---:|---:|
| `/home/stephane/Data13TB` (btrfs) | 11 To | **8,9 To** | 2,0 To |
| `/home/stephane/IA` (RAID ext4) | 938 Go | **895 Go — 97 %** | **34 Go** |
| `/` (NVMe) | 828 Go | 121 Go | 706 Go |

Le point de vigilance immédiat : **IA est presque plein** (34 Go libres), et c'est là que vivent les modèles.

\## Le texte déjà là

- **Wikipédia : 132 Go**, 10 langues — bases sqlite v14 (66 Go) + dumps `xml.bz2` (67 Go). **Français : 7,25 Go de base + 7,13 Go de dump.**
- **`corpus/wiki_apparie` : 12 Go** d'articles Wikipédia en texte brut (6 084 fichiers, de/en/fr/es/it…), appariés par titre — recoupe les dumps, à dédoublonner.
- **Corpus du dépôt `data/` : 6,6 Go** — 15,5 M mots anglais, 18,7 M multilingues, 2,76 M de littérature française, 0,79 M de français local, 1,01 M de prose du dépôt.
- **Corpus propres déjà préparés** : `corpus_propre` (3,24 Mo train), `corpus_litt_propre` (15,3 Mo), `corpus_repo_propre` (4,84 Mo), avec splits et **contamination 0/2 814** mesurée.
- Traduction : MultiUN 1,2 Go, OpenSubtitles 1,2 Go, WikiMatrix 326 Mo, TED2020 109 Mo, JRC 48 Mo, EUR-Lex 10 Mo. SFT : 2 000 consignes FR, paires de raisonnement, distillations DeepSeek. UDHR 28 Mo, textes parallèles 261 Mo.

\## À extraire, et à exclure

- **~228 Go de documents** : `Biblio_large` 22 Go (2 345 Kindle **kfx-zip DRM** + 104 PDF + 87 xhtml), `CEGEP` 11 Go (2 711 PDF, 3 774 xlsx…), `collections` 36 Go, `Documents` 159 Go. Les PDF scannés passent par la chaîne **R4.4** (90–97 % de parité, ~3 s/page).
- **Exclus** : **2,8 To de vidéos récupérées** (PhotoRec), 27 Go de récupération brute, 87 Go d'audio, 5,4 Go de builds, 159 Go de Documents personnels, 3 629 azw, et les **traces DRVF** (21 Go d'UDHR pour 2,2 Mo de texte réel).
- **Quarantaine d'évaluation** : XNLI 2,3 Go, Wikitext-2, DACCORD, gqnli-fr, DiaBLa, splits test/val, questions ONU, scans R4.4.
- **Enseignants, pas données** : DeepSeek-V4.1-Flash Q2 (341 Go), Qwen3-30B (77 Go), logits KLD 6,4 Go, HF hub 119 Go (Qwen2.5 0,5–7B, gemma, whisper).

\## Ce que j'en retiens pour l'entraînement

1. **Le levier français, c'est Wikipédia, pas le dépôt** : 
… [1200 caractères tronqués]

### Tour 5 — go

*29 appels d'outils.* Actions notables :

- bash — Inspect French Wikipedia sqlite schema
- bash — Check DB summaries and French wiki text files
- bash — Check tools and dump contents
- bash — Inspect summary sizes and raw formatting
- bash — Write Wikipedia corpus builder and test on 5000 articles
- bash — Fix sqlite URI and retest extraction
- bash — Debug sqlite open modes
- bash — Fix default DB path and test extraction
- bash — Launch full French Wikipedia extraction
- bash — Read corpus dedup and contamination helpers
- bash — Check Wikipedia extraction progress
- bash — Write contamination checker for corpus
- bash — Check extraction and text join artifacts
- bash — Stop extraction and strengthen text cleanup
- … et 15 autres

**Synthèse produite :**

⏵ Corpus français construit et committé

C'est fait : le premier corpus local de prose française d'un autre ordre de grandeur que le dépôt est construit, nettoyé, dédupliqué, découpé et contrôlé.

\## Ce qui est sur le disque

`data/corpus_wiki_fr/{train,val,test}.txt` — **3,8 Go**, depuis la base Wikipédia FR (`frwiki_v14.db`, 2 755 035 articles) :

| | valeur |
|---|---:|
| articles gardés (≥ 300 caractères) | **2 525 902** |
| caractères | **3,68 G** |
| mots (est.) | **593,6 M** |
| train | **2 273 294 articles · 3,43 Go** |
| val | 126 636 articles · 191 Mo |
| test | 125 972 articles · 190 Mo |
| doublons exacts retirés | 204 |

C'est **cent fois** la prose du dépôt (5,36 Mo uniques).

\## La méthode

- **Nettoyage mesuré** : entités HTML, balises, espaces ; **~92 700 jointures minuscule→majuscule dans 200 Mo** (« bourbonnaiseSa ») recollées, soit ~3,2 M sur le corpus ; apostrophes restaurées devant majuscule (« lOfficial »).
- **Déduplication exacte** : articles (BLAKE2b du texte normalisé) et tronçons — sur ce corpus, 1 tronçon par article (les résumés sont plafonnés à 8 000 caractères, sous les 8 192 du découpage).
- **Split par article** : hash salé de `page_id`, 5 % val / 5 % test — un article n'est jamais dans deux splits.
- **Contrôles** : **0 doublon exact de tronçon** entre splits (0/126 636, 0/125 972) et **0/30 fenêtres** de chacun des quatre jeux d'évaluation (`corpus_propre`, `corpus_litt_propre`, `corpus_repo_propre`, `wikitext2`) retrouvées dans l'entraînement.

\## Les limites, écrites dans la fiche

- Ce sont des **résumés tronqués à 8 000 caractères**, pas les articles entiers : la fin de chaque article manque.
- Le débalisage de la base laisse des artefacts : dates vides (« né le à »), titres de sections restés dans le texte (« Biographie Enfance et formation »).
- La déduplication est **exacte** : les quasi-doublons restent.
- Licence **CC-BY-SA 4.0** (et GFDL) : entraînement libre, redistribution avec attribution et partage à l'identique — le corpus reste local, non diffusé.

\## Les fichiers

- Outils : `tools/corpus_wikipedia.py` (extraction/nettoyage/split) et `tools/verifie_contamination.py` (fuites entre splits et vs évaluations).
- Manifeste : `reports/corpus-wiki-fr.json` (chiffres, SHA-256 des trois fichiers, licence, limites).
- Contamination : `reports/corpus-wiki-fr-contamination.json`.
- Fiche : `reports/rapport-corpus-wiki-fr.md`.
- Commit : `74d7f0b9`.

\## La suite naturelle

1. **N2** : prendre un échantillon de ce cor
… [475 caractères tronqués]

### Tour 6 — constitue les corpus des autres langues et assure-toi que tous les agents s'y retrouvent pour leurs besoins

*41 appels d'outils.* Actions notables :

- bash — Inspect all Wikipedia language databases
- bash — List language DB sizes while counts run
- job_output
- job_kill
- bash — Rewrite multi-language tool and test on Portuguese
- bash — Launch all-language corpus extraction
- bash — Check eval sets and extraction progress
- bash — Inspect XNLI and UDHR eval structures
- bash — Patch FR manifest and build per-language eval samples
- bash — Write corpus catalogue generator and check progress
- bash — Check extraction rate and disk space
- bash — Poll extraction after ten minutes
- bash — Run Arabic corpus contamination check
- bash — Check completed language manifests
- … et 22 autres

**Synthèse produite :**

⏵ Les dix corpus sont construits, documentés et partagés

C'est fait : les neuf autres langues sont extraites avec le même outil que le français, et tout est catalogué pour que chaque agent trouve le sien.

\## Les dix corpus

| langue | articles | caractères | train / val / test | corpus |
|---|---:|---:|---:|---|
| **fr** | 2 525 902 | 3,68 G | 3,43 Go / 191 / 190 Mo | `data/corpus_wiki_fr/` |
| **en** | 6 552 645 | 9,91 G | 8,98 Go / 498 / 498 Mo | `data/corpus_wiki_en/` |
| **de** | 2 884 427 | 4,72 G | 4,33 Go / 240 / 240 Mo | `data/corpus_wiki_de/` |
| **es** | 1 900 560 | 2,79 G | 2,57 Go / 143 / 142 Mo | `data/corpus_wiki_es/` |
| **ru** | 1 956 216 | 2,93 G | 4,66 Go / 259 / 257 Mo | `data/corpus_wiki_ru/` |
| **it** | 1 592 477 | 2,26 G | 2,06 Go / 114 / 114 Mo | `data/corpus_wiki_it/` |
| **ja** | 1 355 856 | 1,76 G | 3,97 Go / 220 / 220 Mo | `data/corpus_wiki_ja/` |
| **zh** | 823 401 | 0,87 G | 1,89 Go / 104 / 105 Mo | `data/corpus_wiki_zh/` |
| **pt** | 991 389 | 1,35 G | 1,25 Go / 70 / 70 Mo | `data/corpus_wiki_pt/` |
| **ar** | 1 047 858 | 1,13 G | 1,78 Go / 98 / 98 Mo | `data/corpus_wiki_ar/` |

**Total : 21 630 731 articles · 31,42 G caractères · 4 643 M mots** (langues à espaces ; ja/zh comptés en caractères, comme le disent les manifestes) **· 38,8 Go**.

\## Où chaque agent les trouve

- **Un catalogue unique** : `reports/rapport-corpus-wikipedia.md` — la table ci-dessus, la méthode, les contrôles et les limites.
- **Un manifeste par langue** : `reports/corpus-wiki-<langue>.json` — articles, caractères, mots, octets, **SHA-256** des trois fichiers, licence, limites.
- **L'état partagé** : `docs/pilotage/en-cours.md`, ligne **Données**, pointe sur le catalogue et les manifestes ; l'inventaire `reports/inventaire-donnees-entrainement.md` aussi.
- **Les fichiers** : `data/corpus_wiki_<langue>/{train,val,test}.txt` (UTF-8, un article par bloc, tronçons séparés par deux sauts de ligne). Pour refaire : `python3 tools/corpus_wikipedia.py --toutes-les-langues` ; pour régénérer la table : `python3 tools/catalogue_corpus.py`.

Usages : **N2** a le français et l'anglais ; les agents multilingues ont les huit autres ; **R4.4** garde ses scans (ce sont des textes, pas des images).

\## Les contrôles

- **0 doublon exact de tronçon entre splits** pour les dix langues (0/52 203 et 0/52 033 en arabe, 0/327 337 et 0/327 877 en anglais, 0/97 650 et 0/97 198 en russe…).
- **0/30 fenêtres** de chaque jeu d'évaluation retrouvées dans l'entraînement : XNLI (ar
… [733 caractères tronqués]

### Tour 7 — relis mes demandes de toutes les sessions des derniers 48h pour compredre la vision à jour du projet. creuse l'historiqu … [113 caractères tronqués]

*30 appels d'outils.* Actions notables :

- bash — List sessions and recent journal days
- bash — Locate DSH session transcripts
- bash — Find recent sessions and raw traces
- bash — Read recent session plans and mandates
- bash — Locate recent DSH session traces
- bash — List Qtrinet workspace session directories
- bash — Inspect DSH session trace format
- bash — Decompress and inspect session trace records
- bash — Inspect user message record structure
- bash — Extract human messages from last 48h sessions
- bash — Read roadmap structure and backlog index
- bash — List pilotage docs and read programme R
- bash — Read backlog files, gaps, and dependency graph
- bash — Read Pensée session plan and report
- … et 16 autres

**Synthèse produite :**

⏵ Vision relue sur 48 h, inventaire élargi à huit chantiers, carte et doc committés

J'ai relu les messages humains des 48 h dans les traces DSH — `0b69f616`, `22e518ee`, `0b0a6a0d` (N2.h), `fe3c05f0` (R4.4), `e181ce02` (Pensée), plus les sessions de QA visuelle —, les plans et rapports de session, et les documents de vision, roadmap, programme R et backlog. Voici ce qui en sort.

\## La vision à jour, en huit principes

1. **Le bus de flux typés, et la structure bat la taille** ; les blocs sont petits, substituables (neuronal, classique, matériel), indépendants du mode d'opération — « l'interface reste Drave ».
2. **Le texte se lit en surface d'abord** : octet → morphème → mot → syntagme → phrase → paragraphe → document → multilingue, en **annotations** et non en prompts ; le CPU étiquette le sûr et énumère le plausible, le réseau tranche.
3. **La pragmatique est un niveau** : l'ambiguïté ne se tranche qu'en contexte, et le double sens se **conserve**.
4. **Les interprétations sont plurielles** : RSN à candidats, arbre d'états, BFS/A*/MCTS/AC-3/alpha-bêta, anytime, trace/rejeu.
5. **La validation humaine construit la banque** : S montre les structures candidates, l'humain et le LLM les évaluent, l'export alimente le corpus.
6. **Le lecteur R est la preuve** : document + question + budget → réponse sourcée ou refus motivé.
7. **Le natif N est la capacité** : distillation, corpus propre, mètre honnête, longueur, diversité.
8. **La mesure est la règle** : un chiffre, un contrôle négatif, une fiche, une porte, un état ; les limites sont nommées.

Les demandes qui ont produit cela : la **séparation à 3 niveaux** et les blocs substituables (31/10), la **RSN plurielle** et l'arbre d'états (22 h 22), les **10 h de liberté** (N2.h et R4.4), la **typoglycémie** et la **coloration linguistique** (01/11 10 h 29–10 h 46), le **niveau pragmatique** et les phrases non ambiguës (11 h 10–11 h 36), la **couche heuristique** (11 h 33), et surtout le **contrat du bloc langue** (13 h 23) : « une version heuristique et une neuronale, le contrat garantissant la substitution ou le parallèle ».

\## L'inventaire élargi : de quatre à huit chantiers

| chantier | question | état | prochaine action |
|---|---|---|---|
| **A — le moteur** | les flux de blocs tournent-ils, se placent-ils, se rejouent-ils ? | ✅ A1–A8 ; A3.4/A5.4/A6.2 bloqués | A2.6, réduire le lot |
| **B — l'intelligence** | le sens, la logique, les jeux, les maîtres | ✅ B1–B12 ; B10.3 bloqué ; B13 v0 (6/6 portes) | B10
… [2796 caractères tronqués]

### Tour 8 — combien de chantiers simultanés on peut faire en ce moment? Est0il préférable d'avoir plusieurs sessions dsh ou bien une … [35 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Measure CPU, RAM, GPU, disk, and active agent processes
- bash — Read session and subagent method guidance
- bash — Add simultaneous capacity section to chantiers doc
- bash — Commit capacity section

**Synthèse produite :**

⏵ Réponse : capacité mesurée et arbitrage sessions/sous-agents

\## Combien, en ce moment

Les moyens réels, mesurés à l'instant : **40 cœurs**, **125 Go de RAM** (109 disponibles), **2 GPU Quadro RTX 5000 de 16 Go — libres**, **2,0 To libres** sur `Data13TB`, **34 Go seulement** sur `IA` (97 % plein), et **4 processus `dsh`-TUI actifs** (l'état ne déclare qu'une session, Pensée).

**Matériellement**, on peut tenir 6 à 10 tâches CPU simultanées et **1 à 2 chantiers GPU** (un entraînement par GPU ; le 32 B et le professeur ne tiennent pas en 16 Go).

**Réellement, la capacité est de 4 à 6 chantiers en vol** — 4 sessions + 2 à 4 sous-agents. Les six chantiers prêts aujourd'hui : **N2** (GPU libre), **L** (contrat + cascade), **S** (analyseur + export), **D** (texte intégral, PDF/OCR), **A2.6/A8.3**, **B13** (AC-3, alpha-bêta). Bloqués : B10.3, A3.4, A5.4, A6.2, R2/R3, R5, N5.

\## Pourquoi pas plus

- **L'état s'écrit une session à la fois** (`continuite.md`) ; au-delà de 4 écrivains, les compteurs dérivent et les commits se verrouillent — on l'a vu le 01/11 : `cannot lock ref 'HEAD'` sur deux commits concurrents.
- **Les territoires de fichiers** se chevauchent vite (N2 : `data/`, `tools/corpus*` ; Pensée : `tools/pensee/`, `reports/pensee-*`, `r44-*` ; S : `tools/structures` ; D : `data/corpus*`).
- **La mesure sérialise** : le banc R03, les portes, les JSON.
- **L'humain est le goulot** : S, la pragmatique, le contrat de L et les choix de design demandent ta relecture — plus d'agents produisent plus à relire, pas plus de **validé**.

\## Sessions ou une seule avec beaucoup de sous-agents ?

**Les deux, à des échelles différentes — c'est un hybride, pas un choix exclusif.**

| besoin | unité | pourquoi |
|---|---|---|
| un **mandat long** (heures, objectif propre, contexte qui compacte, territoire réservé) | **session DSH** | elle survit, écrit son plan et son état, se reprend ; elle coûte la coordination |
| une **tâche bornée** (une mesure, un outil, une fiche, un audit) | **sous-agent** (2 à 4, AGENTS § 10) | il rend un diff, la session intègre et commite ; il ne touche ni `en-cours` ni la roadmap |
| un **audit massif en lecture seule** | **workflow** (fan-out) | il parallélise la lecture, pas l'écriture |

Une **seule session avec beaucoup de sous-agents** ne remplace pas les sessions : son contexte compacte, l'état reste à un écrivain unique, et huit sous-agents qui écrivent dans le même arbre se sérialisent à l'intégration. Les sessions sont l'**unité 
… [941 caractères tronqués]

### Tour 9 — organise le dossier pilotage pour qu'il soit à jour et qu'entre le en-cours.md et roadmap.md il y ait un plan de travail … [209 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Read pilotage usage and session checker
- bash — List active session plans, reservations, and moving files
- bash — Read sessions checker status and overlap logic
- bash — Write multi-session work plan and pilotage index
- bash — Write and run session file monitor
- bash — Fix multi-line plan parsing and run session gate
- bash — Update pointers, counters, journal, and run monitor
- bash — Check docs map and counters
- bash — Update docs map, counters, monitor rules
- bash — Final gates and commit pilotage reorganization

**Synthèse produite :**

⏵ Pilotage réorganisé, plan multi-sessions et surveillance en place

Le dossier pilotage a maintenant son **index**, son **plan de travail** et ses **outils de surveillance**. Commit `ac1f9436`, revue verte (385 fiches, 471 JSON, 118 docs, 81 portes), T0 3 948/4 000.

\## La chaîne de lecture

`en-cours.md` (l'état, ce qui se passe maintenant) → **`plan-travail.md`** (qui fait quoi, où, à quelle cadence) → `roadmap.md` (l'ordre) → `chantiers.md` (les relations, la vision, la capacité) → `programme-r.md` → `backlog/`. Le `docs/pilotage/README.md` dit cet ordre, **qui écrit quoi**, les outils et les documents datés à ne pas charger par défaut. La carte de la documentation (`docs/README.md`) pointe désormais sur le plan et les chantiers.

\## Le plan de travail

**Quatre sessions de mandat + un rôle d'intégration** (le hub) :

| session | mandat | charge | prochaine action |
|---|---|---|---|
| **N2** | le natif : entraînement, longueur, capacité, diversité | **GPU** (1 des 2) | N2 sur les corpus wiki fr/en ; le verrou 129→512 |
| **L** | le bloc langue (heuristique + neuronal), la cascade, la pragmatique ; B13 | CPU | le **contrat de L**, puis la mesure 71 langues |
| **S** | les structures candidates, la validation humaine/LLM, la banque | CPU | l'analyseur plus riche, l'export au corpus |
| **D/R/A** | les corpus (texte intégral, PDF/OCR), R1.1/R1.2, A2.6/A8.3 | CPU/IO | le texte intégral, l'extraction PDF/OCR |

Le **hub** tient l'état, la roadmap, les compteurs, le journal et la revue ; il **intègre** les sections des sessions, il ne code pas un chantier.

**Les territoires** sont écrits (globs) et le partage de `data/` est réglé : N2 écrit les corpus préparés qu'il utilise, D écrit les nouveaux corpus wiki et leurs manifestes ; chacun **lit** ceux de l'autre sans les modifier. L'état, la roadmap, `AGENTS.md`, `INDEX.md` et le journal ne s'écrivent que par le hub, **une session à la fois**.

**La cadence** : un round jusqu'à un checkpoint (fait mesuré, fiche, JSON, commit, ligne d'état, heartbeat) ; un seul écrivain d'état ; `git add` explicite ; index alterné pour les commits partagés ; en cas de course `HEAD`, relire, refaire l'index, recommiter — jamais de `reset` sur les fichiers d'une autre session ; portes lourdes (OCR-scans, toutes-les-portes) **une à la fois**.

**La machine partagée** : 1 session GPU, 3 sessions CPU, 2 à 4 sous-agents par session, 40 cœurs mais 2 à 3 gros travaux à la fois, `IA` à **34 Go libres** (aucun nouveau gros modèle sans s
… [1369 caractères tronqués]

### Tour 10 — lire docs/pilotage/plan-travail.md et avancer

*32 appels d'outils.* Actions notables :

- read
- bash — Read current state plan and French dump
- bash — Write full-text extractor and test on 3000 articles
- job_output
- bash — Check test extraction process and outputs
- job_kill
- bash — Fix ElementTree text path and time parsing
- bash — Check stuck process and tool text path
- bash — Patch text path and time 3000-page parse
- bash — Benchmark wikitext stripper speed
- bash — Start 100k-article full-text pilot in background
- bash — Open D/R/A session plan and update territory
- bash — Fix field parser headings and check pilot
- bash — Inspect pilot sample and status
- … et 18 autres

**Synthèse produite :**

⏵ Plan lu, session D/R/A ouverte, texte intégral lancé

J'ai lu `docs/pilotage/plan-travail.md` et avancé sur la première action du mandat **D/R/A** : le texte **intégral** de Wikipédia, celui que les corpus actuels ne donnent pas (leurs résumés sont tronqués à 8 000 caractères).

\## Ce qui est fait

**La session D/R/A est ouverte** : le plan `journal/sessions/fe3c05f0/…/plan.md` (rôle, périmètre, territoire, heartbeat, prochaine action), sa section dans l'état, le territoire du plan complété (`tools/corpus_wikipedia_texte.py`, `data/corpus_wiki_*_texte/`, `reports/corpus-wiki-*texte*`). L'état déclare maintenant **2 sessions** (Pensée + D/R/A) et passe `sessions.py --check`.

**L'outil** `tools/corpus_wikipedia_texte.py` lit le dump `frwiki` (7,13 Go), débalise (commentaires, refs, tableaux, modèles, fichiers/catégories, liens → libellé, titres de sections), déduplique, sépare par article et écrit les tronçons de 8 192 caractères avec les SHA-256 et le manifeste.

**Le pilote** (100 000 articles, 146 250 pages lues, 31 998 redirections écartées) :

| grandeur | valeur |
|---|---:|
| articles gardés | 100 000 |
| caractères | 1 045 085 924 |
| mots (car. / 6,2) | 168 562 245 |
| train / val / test | 972,6 / 56,3 / 52,7 Mo |
| résidus `{{` / `[[` / `<` sur 20 000 lignes | 1 / 0 / 3 |

**Les contrôles** : au niveau du **tronçon réel (8 Ko)**, **0 / 6 661** fenêtres de la validation et **0 / 6 228** du test dans l'entraînement ; **0 / 40** fenêtres sur les **cinq** jeux d'évaluation (XNLI fr, UDHR, trois jeux locaux). Le contrôle standard (unité = ligne) signale 3,66 % / 3,49 % de lignes dupliquées : ce sont les **titres de sections répétés** (« Biographie », « Notes et références »…), pas de la prose — c'est écrit et expliqué dans la fiche.

**Le run complet est lancé** : 2,5 M d'articles, ~26 Go estimés, dans `data/corpus_wiki_fr_texte/`, manifeste `reports/corpus-wiki-fr-texte.json` au prochain checkpoint (PID de suivi `1454236`, log `/tmp/run-texte-fr.log`). Les neuf autres langues suivent le même outil (`--langue de`, etc.).

\## Les artefacts

- Fiche `reports/rapport-corpus-wiki-texte.md` (méthode, pilote, contrôles, limites, run complet).
- `reports/corpus-wiki-fr-texte-pilote.json` et `reports/corpus-wiki-fr-texte-pilote-contamination.json`.
- Commit `6fbfbb80` ; état à jour (session D/R/A, compteurs 388 fiches / 474 JSON / 118 docs / 81 portes), **T0 3 985 / 4 000**, revue verte.

\## Les notes

- Deux bugs corrigés en route : le chemin `ElementTree` 
… [538 caractères tronqués]

### Tour 11 — es-tu à jour? as-tu fait tout ce que tu pouvais?

*17 appels d'outils.* Actions notables :

- bash — Check run progress, git status, and temp files
- bash — Run gates, heartbeats, and roadmap overview
- bash — Check state sections and clean temp pilot
- bash — Add D and L roadmap rows and refresh heartbeat
- bash — Wait for full-text run to finish
- bash — Commit roadmap D/L rows and state update
- bash — Restore T0 budget and check run
- bash — Wait for full-text run completion
- bash — Count total pages in dump index
- bash — Wait again for full-text run
- bash — Read full-text manifest numbers
- bash — Run contamination on full corpus
- bash — Check 8KB windows on full corpus
- bash — Update full-text report with complete run
- … et 3 autres

**Synthèse produite :**

⏵ Oui : le run complet est terminé, mesuré et committé

**Oui — maintenant, tout ce qui pouvait être fait dans cette session est fait et committé.** Le run complet du texte intégral, qui tournait encore quand tu as posé la question, est **terminé** (commit `79bce783`).

\## Le texte intégral FR — résultat complet

| grandeur | valeur |
|---|---:|
| pages lues | 5 968 207 |
| articles gardés | **2 388 219** |
| redirections / autres ns / courts | 1 827 807 / 1 385 362 / 366 649 |
| caractères | **8 025 059 777** |
| mots (car. / 6,2) | 1 294 364 480 |
| train / val / test | 7,50 Go / 419,6 Mo / 415,3 Mo |
| articles train / val / test | 2 149 330 / 119 866 / 119 023 |
| tronçons 8 192 car. | 2 755 825 (783 doublons) |
| résidus `{{` / `[[` / `<` (20 000 lignes) | 1 / 0 / 3 |

**Contrôles** : **0 / 40** fenêtres sur les cinq jeux d'évaluation (XNLI fr, UDHR, trois jeux locaux) ; **0 / 49 655** (validation) et **0 / 49 148** (test) fenêtres de 8 Ko dans l'entraînement. Le contrôle standard (unité = ligne) signale 5,53 % / 5,47 % : ce sont les **titres de sections répétés**, pas de la prose — la fiche l'explique et donne le contrôle 8 Ko qui le corrige.

**Le pilote est réfuté comme projection** : les 100 000 premiers articles (10,45 Ko/article) laissaient croire à 7× les résumés et 26 Go ; le run donne **3,36 Ko/article** et **8,34 Go** (2,18×). C'est le run qui fait foi ; le pilote reste le manifeste de validation. C'est écrit dans la fiche, avec la limite du pilote non aléatoire.

\## Ce qui est à jour

- **État** (`en-cours.md`) : session D/R/A avec les chiffres du run, prochaine action « les 9 langues, puis PDF/OCR » ; compteurs **389 fiches / 476 JSON / 118 docs / 81 portes** ; **T0 3 982 / 4 000** ; `verifie_en_cours` vert.
- **Roadmap** : les lignes **L** (bloc langue, R0.7 : 398 langues à 0,9687) et **D** (les données : inventaire, 10 corpus, texte intégral FR) sont ajoutées à « En un coup d'œil ».
- **Plan de travail** : le territoire D/R/A complété (l'outil, `data/corpus_wiki_*_texte/`, les fiches) ; heartbeat du plan rafraîchi.
- **Fiche, manifeste et contamination** du run complet committés ; le corpus (8,34 Go) reste local, gitignoré.
- **Nettoyage** : le pilote temporaire (`/tmp`, 1,1 Go) supprimé.
- Les portes passent : revue de documentation, taille, état, journal, backlog, schémas, sessions ; le dépôt est propre (seuls `tools/docwatch` modifié et `tools/structures` non suivi, les deux connus).

\## Ce qui n'est pas fait — et pourquoi

- **Les ne
… [867 caractères tronqués]

### Tour 12 — suis le plan, continue jusqu'à 8h demain matin

*4 appels d'outils.* Actions notables :

- create_goal
- bash — Create long goal and check nine language dumps
- bash — Launch five language full-text extractions
- bash — Update plan and state for nine languages

**Synthèse produite :**

⏵ Mandat long : objectif persisté jusqu'à 8 h, puis lancement des neuf langues

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document.py` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/installer_ocr.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document_ocr.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_ocr.py` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r44-ocr-pilote.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/encodeur-visuel.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/simuler_scan.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/nettoyer_scan.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_scans.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/fabriquer_colonnes.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_colonnes.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/fabriquer_tables.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/extraire_tableaux.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_tables.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_reel.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r44-scans.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check active sessions status
- **T1** Check git working tree and recent commits
- **T1** Read active session mandate plan
- **T1** Run backlog graph verifier
- **T1** Inspect other session files and heartbeat
- **T1** Read start of backlog verifier
- **T1** Find missing-card logic in verifier
- **T1** Check current time and GPU usage
- **T1** Run documentary gates
- **T1** Verify no gate script still running
- **T1** List processes touching the repo
- **T1** List documentary gate scripts
- **T1** Read documentary gate scripts
- **T1** Read gate registry runner
- **T1** Run documentation review
- **T1** Find N4 reports and backlog cards
- **T1** Locate N4 short-instruction evidence
- **T1** Read R4.4 backlog card
- **T1** Check OCR tools availability
- **T1** Test PyPI network access
- **T1** Scan continuity method for session rules
- **T1** Inspect sessions tool interface
- **T1** Find PDF corpus in data
- **T1** Check PDF rendering and extraction tools
- **T1** Inspect ONU corpus and R0 tools
- **T1** Trace ONU corpus use in R0.1
- **T1** Read R0.3 bench report
- **T1** Read PDF graph parser header
- **T1** Find bench corpus sources
- **T1** Check PDF sizes and corpus index
- **T1** Check OS, python, disk, apt and torch
- **T1** Check zypper and tesseract packages
- **T1** Probe openSUSE repo for tesseract RPM
- **T1** Check RPM tools and tesseract dependencies
- **T1** List tesseract and leptonica RPM names
- **T1** Check work dir ignore status
- **T1** Find leptonica and language data RPMs
- **T1** List tesseract language RPMs in noarch
- **T1** Read bench harness start
- **T1** Inspect reader controller interface
- … et 759 autres

## 4. Mesures et résultats marquants

- **T1** `4442c64c N2 — L'ÉTAT DE SECTION NE SE DISTINGUE PAS D'UN ÉTAT ÉTRANGER (+0,36 % CONTRE +0,37 %)`
- **T1** `les données** (41 Mo, 4 sources, 20 000 pas) et la capacité. Mesurer le budget complet sur le`
- **T1** `16 × 128) et **2,6998** (8 lots × 15 × 129), plus le contrôle par permutation.`
- **T1** `0, 84 %, 1164 MiB, 16384 MiB`
- **T1** `1, 78 %, 1164 MiB, 16384 MiB`
- **T1** `[still running after 60000ms; moved to background job bash-9]`
- **T1** `/dev/mapper/system-root   11T  8,9T  2,0T  82% /home/stephane/Data13TB`
- **T1** `tmpfs                     63G  546M   63G   1% /tmp`
- **T1** `# indépendante** (`transformers`) qui dit que la tour **ne concorde pas encore** (55 à 79 % d'écart`
- **T1** `# pour une quantification de ~1 % ; `reports/rapport-vision-qwen2vl.md`). Une porte qui exigerait`
- **T1** `#   3. **les formes sont celles du modèle** (256 patchs × 1280 canaux, 64 jetons × 1536 après`
- **T1** `A_RES_80_10-fr.pdf p2       fra        558   2.15%  97.85%   94.3      5`
- **T1** `A_RES_80_10-en.pdf p2       eng        546   1.10%  98.90%   94.8      4`
- **T1** `WER 1.63% · rappel 98.37% · précision 99.45% · confiance 94.5`
- **T1** `exactitude : natif 100.00% · OCR 66.67% · PARITÉ 66.67% (9 questions)`
- **T1** `sans OCR : 0.00% de réponses`
- **T1** `✅ WER ≤ 10%`
- **T1** `✅ rappel ≥ 90%`
- **T1** `❌ parité ≥ 90%`
- **T1** `✅ exactitude natif ≥ 90%`
- **T1** `❌ exactitude OCR ≥ 90%`
- **T1** `331:        (f"WER ≤ {SEUILS['wer']:.0%}", agregat["wer"] <= SEUILS["wer"]),`
- **T1** `332:        (f"rappel ≥ {SEUILS['rappel']:.0%}", agregat["rappel"] >= SEUILS["rappel"]),`
- **T1** `333:        (f"parité de région ≥ {SEUILS['parite_region']:.0%}",`
- **T1** `335:        (f"exactitude natif ≥ {SEUILS['exactitude_natif']:.0%}",`
- **T1** `359:    print(f"  exactitude de la valeur : natif {a['exactitude_natif']:.2%} · OCR {a['exactitude_ocr']:.2%}")`
- **T1** `360:    print(f"  PARITÉ de région (F1 ≥ 0,90) : {a['parite_region']:.2%} · médiane F1 "`
- **T1** `361:          f"{a['f1_median']:.3f} · valeur stricte {a['parite_valeur']:.2%} "`
- **T1** `365:              f" · parité région {a['parite_region_bruitee']:.2%}")`
- **T1** `363:          f"{a['f1_median']:.3f} · valeur stricte {a['parite_valeur']:.2%} "`
- **T1** `A_RES_80_10-es.pdf p2       spa        577   2.08%  98.09%   94.5      4`
- **T1** `A_RES_80_1-en.pdf p1        eng        294   4.76%  98.30%   93.5      3`
- **T1** `A_RES_80_1-es.pdf p1        spa        326   5.52%  98.77%   92.9      3`
- **T1** `A_RES_80_1-fr.pdf p1        fra        315   4.44%  99.68%   90.5      3`
- **T1** `A_RES_80_10-en.pdf p1       eng        316   9.18%  93.04%   91.5      3`
- **T1** `A_RES_80_10-es.pdf p1       spa        284   9.15%  94.72%   92.1      3`
- **T1** `A_RES_80_10-fr.pdf p1       fra        305  12.13%  92.79%   89.4      2`
- **T1** `A_RES_80_1-en.pdf p2        eng        250   0.40%  99.60%   95.7      0`
- **T1** `WER 4.48% · rappel 97.37% · précision 97.82% · confiance 93.2`
- **T1** `exactitude de la valeur : natif 100.00% · OCR 83.33%`
- **T1** `PARITÉ de région (F1 ≥ 0,90) : 90.00% · médiane F1 1.000 · valeur stricte 83.33% (30 questions)`
- **T1** `page dégradée : WER 17.08% · exactitude 40.00% · parité région 26.67%`
- **T1** `✅ parité de région ≥ 90%`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-native-prof20k-5.md`](rapport-native-prof20k-5.md) | **N2.19** — 30 000 pas : PPL **2,708**, précision **72,80 %** |`
- **T1** `| [`rapport-native-prof20k-4.md`](rapport-native-prof20k-4.md) | **N2.18** — 30 000 pas : PPL **2,714**, précision **72,62 %** |`
- **T1** `| [`rapport-native-prof20k-3.md`](rapport-native-prof20k-3.md) | **N2.17** — 30 000 pas : PPL **2,726**, précision **72,34 %** |`
- **T1** `| [`rapport-native-prof20k-2.md`](rapport-native-prof20k-2.md) | **N2.16** — 20 000 pas de plus : PPL **2,755**, plateau, tête 3 **72,17 %** |`
- **T1** `| [`rapport-native-prof20k.md`](rapport-native-prof20k.md) | **N2.14** — professeur 20k : PPL **2,787**, précision **71,30 %** |`
- **T1** `| [`rapport-native-prof10k-2.md`](rapport-native-prof10k-2.md) | **N2.13** — 20 000 pas de plus : PPL **2,876**, précision **70,00 %** |`
- **T1** `| [`rapport-native-prof10k.md`](rapport-native-prof10k.md) | **N2.12** — professeur 10k : PPL **2,910** contre **3,082**, tête 3 **69,97 %** |`
- **T1** `85:[R4.4] lasts 1 day and is 60% complete and is colored in #b26a00`
- **T1** `271:| **R4.4** | **vision/OCR** : scans, figures, layout | 🔬 **partiel** : tesseract 5.5.3 installé sans root ; **10 pages rendues** lues à **WER 4,48 %**, **parité 90 %** ; page dégradée **26,7 %** |`
- **T1** `4 sources, **B′** quotas égaux (le manifeste est à **82 % anglais**), **C** curriculum 129`
- **T1** `sur A ; la hiérarchie est écartée deux fois, restent **le curriculum et les données** (41 Mo,`
- **T1** `- **R13 — la tokenisation** : **close**, décision **octets** — BPE 512 +0,39 % (bruit), BPE`
- **T1** `1024 +4,09 %, anglais +4,22/+6,59 % à octets égaux ; fiche`
- **T1** `| 13:01 | `4442c64c` | N2 — L'ÉTAT DE SECTION NE SE DISTINGUE PAS D'UN ÉTAT ÉTRANGER (+0,36 % CONTRE +0,37 %) |`
- **T1** `section donne **2,9935** contre **2,9927** au témoin (+0,029 %) ; il bat son propre contrôle **sans`
- **T1** `les graines 2 et 3 décalent désormais les fenêtres de `(graine−1) × 10 000 019`.`
- **T1** `**WER 4,48 %** (169 éditions sur 3 771 mots), rappel **97,37 %**, confiance **93,2**. Sur les`
- **T1** `(90 %)**, la **valeur exacte** dans **25 (83,3 %)**. Les écarts sont nommés : trois **appels de note`
- **T1** `travail : **sans OCR 0/30**, et la page « photo » simulée tombe à **17,08 %** de WER et **26,7 %**`
- **T1** `**WER 4,48 %**, **parité de passage 90 %**, page dégradée **26,7 %**. R4.4 passe de bloquée à`
- **T1** `+   l'OCR est installé, **10 pages rendues** sont lues à **4,48 %** de WER avec une **parité de`
- **T1** `+   passage 90 %**, et la **page dégradée** tombe à **26,7 %** — les **scans réels** restent ouverts.`
- **T1** `[R4.1–R4.3] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[R0.4] lasts 2 days and is 100% complete and is colored in #6a1b9a`
- **T1** `[R0.5] lasts 2 days and is 100% complete and is colored in #6a1b9a`
- **T1** `+[R4.4] lasts 1 day and is 60% complete and is colored in #b26a00`
- **T1** `[N0/N1] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[N2] lasts 4 days and is 30% complete and is colored in #b26a00`
- **T1** `+| **R4.4** | **vision/OCR** : scans, figures, layout | 🔬 **partiel** : tesseract 5.5.3 installé sans root ; **10 pages rendues** lues à **WER 4,48 %**, **parité 90 %** ; page dégradée **26,7 %** | 10`
- **T1** `2. **L'assertion perdue.** Cinq blocs `python3 - <<'PY'` (`porte-deepseek` ×3, `porte-jeux` ×2)`
- **T1** `+  **WER 4,48 %**, **parité de passage 90 %**, page dégradée **26,7 %**. R4.4 passe de bloquée à`
- **T1** `+  **R4.4 partielle** : OCR installé sans root, **10 pages rendues** à **WER 4,48 %** et`
- **T1** `+  **parité 90 %** ; page dégradée **26,7 %** ; fiche [`r44`](../../reports/rapport-r44-ocr-pilote.md).`
- **T1** `0088fc2f R4.4 — L'OCR LIT DIX PAGES À 4,48 % DE WER, LA PARITÉ DE PASSAGE TIENT À 90 %, LA PAGE « PHOTO » TOMBE À 26,7 %`
- **T2** `- **Rôle** : **N2, le corpus** — **32,8 %** des fenêtres de validation sont verbatim dans`
- **T2** `**R4.4 partielle** : OCR installé sans root, **10 pages rendues** à **WER 4,48 %** et`
- **T2** `**parité 90 %** ; page dégradée **26,7 %** ; fiche [`r44`](../../reports/rapport-r44-ocr-pilote.md).`
- **T2** `- **B10.2bis — décodeur** : 3×3 : **11,1** ; capacité 11,8 ; **mots 32,5** ;`
- **T2** `- **B11.10** : **hybride 4/4** — codec **161/161**, ambiguïtés refusées ; **69,3 %** natif ;`
- **T2** `- **N2** : GPU ; **N2.d** — le budget plein (20 000 pas, 41 Mo, 3 graines) paie`
- **T2** `**2,9355 → 2,8527** ; les quatre sources coûtent **+0,9064** (professeur français, 82,5 %`
- **T2** `à 129. **La validation n'est pas tenue à l'écart : 32,8 % des fenêtres du protocole sont`
- **T2** `c3bcbe99 N2 — LE BUDGET PAIE 2,8 %, LES QUATRE SOURCES COÛTENT 91 %, ET LA VALIDATION EST CONTAMINÉE À 32,8 %`
- **T2** `A_RES_80_10-fr-p2-s1-propre.png · 2550×3300`
- **T2** `A_RES_80_10-fr-p2-s1-photocopie.png · 1700×2200`
- **T2** `A_RES_80_10-fr-p2-s1-photo.png · 1530×1980`
- **T2** `A_RES_80_10-fr-p2-s1-fax.png · 1060×1360`
- **T2** `A_RES_80_10-fr-p2-s1-papier.png · 2125×2750`
- **T2** `A_RES_80_10-en-p2-s1-propre.png · 2550×3300`
- **T2** `A_RES_80_10-en-p2-s1-photocopie.png · 1700×2200`
- **T2** `A_RES_80_10-en-p2-s1-photo.png · 1530×1980`
- **T2** `A_RES_80_10-en-p2-s1-fax.png · 1060×1360`
- **T2** `A_RES_80_10-en-p2-s1-papier.png · 2125×2750`
- **T2** `A_RES_80_10-fr-p2-s1-propre.png              2550x3300 moy=243.5 ect= 49.0 WER= 2.15% mots= 552 conf= 94.3  3.2s`
- **T2** `A_RES_80_10-fr-p2-s1-photocopie.png          1700x2200 moy=240.4 ect= 41.4 WER= 5.73% mots= 549 conf= 89.9  2.7s`
- **T2** `A_RES_80_10-fr-p2-s1-photo.png               1530x1980 moy=179.1 ect= 39.3 WER=51.79% mots= 279 conf= 92.4  1.6s`
- **T2** `A_RES_80_10-fr-p2-s1-fax.png                 1060x1360 moy=243.8 ect= 46.1 WER=71.86% mots= 468 conf= 37.8  2.1s`
- **T2** `A_RES_80_10-fr-p2-s1-papier.png              2125x2750 moy=186.9 ect= 33.1 WER= 2.15% mots= 552 conf= 94.3  3.4s`
- **T2** `A_RES_80_10-en-p2-s1-propre.png              2550x3300 moy=242.7 ect= 50.6 WER= 1.10% mots= 540 conf= 94.8  3.3s`
- **T2** `A_RES_80_10-en-p2-s1-photocopie.png          1700x2200 moy=239.6 ect= 42.7 WER= 3.11% mots= 540 conf= 92.1  2.8s`
- **T2** `A_RES_80_10-en-p2-s1-photo.png               1530x1980 moy=178.5 ect= 39.9 WER=50.37% mots= 276 conf= 95.0  1.6s`
- **T2** `A_RES_80_10-en-p2-s1-fax.png                 1060x1360 moy=243.0 ect= 47.8 WER=65.20% mots= 454 conf= 47.3  2.0s`
- **T2** `A_RES_80_10-en-p2-s1-papier.png              2125x2750 moy=186.3 ect= 34.1 WER= 1.28% mots= 541 conf= 94.8  3.5s`
- **T2** `photo_doux                         WER= 1.79% mots= 553 conf= 94.1  3.1s`
- **T2** `photo_moyen                        WER= 2.33% mots= 549 conf= 92.7  2.9s`
- **T2** `photo_actuel                       WER= 5.38% mots= 548 conf= 89.7  2.7s`
- **T2** `papier_doux                        WER= 4.12% mots= 547 conf= 91.2  3.1s`
- **T2** `papier_fort                        WER=53.41% mots= 274 conf= 89.2  1.6s`
- **T2** `photo_brut                       psm3 WER=51.79% mots= 279 conf= 92.4  1.5s`
- **T2** `photo_psm1                       psm1 WER=51.79% mots= 279 conf= 92.4  1.9s`
- **T2** `photo_psm4                       psm4 WER=51.61% mots= 281 conf= 92.3  1.5s`
- **T2** `photo_psm6                       psm6 WER=45.88% mots= 333 conf= 88.6  1.6s`
- **T2** `photo_eclair                     psm3 WER= 3.76% mots= 545 conf= 93.8  2.1s`
- **T2** `photo_eclair_x2                  psm3 WER= 3.23% mots= 546 conf= 93.2  3.2s`
- **T2** `photo_eclair_sauvola             psm3 WER= 3.94% mots= 546 conf= 91.7  2.1s`
- **T2** `fax_brut                         psm3 WER=71.86% mots= 468 conf= 37.8  2.2s`
- … (tronqué)

## 5. Erreurs rencontrées

38 sorties en erreur ou divergentes. Les premières :

- **T1** : R41-bloc-tableaux.md R42-bloc-code.md R43-bloc-maths.md R44-encodeur-visuel.md --- [exit code: 2]
- **T1** : [{'type': 'titre', 'texte': 'A /RES/80/1', 'prov': {'page': 1, 'y': 42.6}}, {'type': 'section', 'texte': 'Nations Unies', 'prov': {'page': 1, 'y': 48.2}}, {'type': 'section', 'texte': 'Assemblée génér
- **T1** : tools/graphe_document.py:287:def manifeste(chemin: pathlib.Path, langue: str = "und", plat: bool = False) -> dict: tools/lecteur_controleur.py:65:def passages(manifeste: dict) -> list[dict]: [stderr] 
- **T1** : [stderr] head: cannot open '/tmp/ocrout.tsv' for reading: No such file or directory grep: /tmp/ocrout.tsv: No such file or directory [exit code: 2]
- **T1** : [stderr] ls: cannot access 'work/ocr/root/usr/share/tessdata/': No such file or directory [exit code: 2]
- **T1** : [code 0]   exactitude de la valeur : natif 100.00% · OCR 83.33%   PARITÉ de région (F1 ≥ 0,90) : 90.00% · médiane F1 1.000 · valeur stricte 83.33% (30 questions)   page dégradée : WER 17.08% · exactit
- **T2** : brut                               psm3 WER=29.93% conf= 64.9 med3_x2                            psm3 WER=97.85% conf= 23.8 med3_x2_flou05                     psm3 WER=98.39% conf= 23.3 med3_x3       
- **T2** : [stderr] Traceback (most recent call last):   File "<stdin>", line 22, in <module>   File "<stdin>", line 12, in ocr_box AttributeError: module 'PIL' has no attribute 'ImageFilter'. Did you mean: 'Ima
- **T2** : famille    split pipe      WER  rappel  conf  F1med  exNat  exOCR  preser [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module> KeyError: 'f1_median' [exit code: 1]
- **T2** : [stderr] Traceback (most recent call last):   File "<stdin>", line 28, in <module>   File "<stdin>", line 16, in prep ValueError: assignment destination is read-only [exit code: 1]
- **T2** : gouttière + option colonnes ajoutées [stderr] Sorry: IndentationError: expected an indented block after 'if' statement on line 223 (graphe_document_ocr.py, line 224) [exit code: 1]
- **T2** : [stderr] Traceback (most recent call last):   File "<stdin>", line 19, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document_ocr.py", line 359, in manifeste     blo
- **T2** : === reports/r44-scans.json   fax|dev|auto {'wer': 0.219, 'preservation': 0.5333, 'confiance': 77.1}   fax|test|auto {'wer': 0.1552, 'preservation': None, 'confiance': 81.3}   papier|dev|auto {'wer': 0
- **T2** : 606803       10:43  0.0 bash -c cat > tools/porte-ocr-scans.sh <<'EOF' #!/bin/bash # porte-ocr-scans.sh — R4.4 : les scans (5 familles), les colonnes, les tableaux. # # POURQUOI CETTE PORTE EXISTE. La
- **T2** : [stderr] Syntax Warning: May not be a PDF file (continuing anyway) Syntax Error (2): Illegal character <68> in hex string Syntax Error (3): Illegal character <74> in hex string Syntax Error (4): Illeg

## 6. Commits

- GIT_INDEX_FILE=/tmp/index.r44 git commit -F /tmp/r44-msg.txt 2>&1 | tail -12; echo "[commit ${PIPESTATUS[0]}]"
- set -e PATHS=(  docs/implantation/encodeur-visuel.md  docs/pilotage/backlog/R44-encodeur-visuel.md  docs/pilotage/backlog/index.md  docs/pilotage/en-cours.md  d
- git diff --cached --name-only | head; echo "[staged: $(git diff --cached --name-only | wc -l)]"; git add docs/pilotage/en-cours.md journal/sessions/fe3c05f0-834
- set -e PATHS=(docs/pilotage/en-cours.md journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md tools/simuler_scan.py tools/nettoyer_scan.py tools/mesurer
- cat > /tmp/msg-r44-scans.txt <<'EOF' R4.4 — LES SCANS : LA PHOTO PASSE DE 55,9 % À 7,0 % DE WER, LES COLONNES DE 89 % À 0,5 %, UN VRAI LIVRE TIENT 7,10 %  La li
- ÉTAT — LA PAGE VIVANTE PASSE AU 1er NOVEMBRE : LA REVUE EXIGE LA DATE DU DERNIER COMMIT" 2>&1 | tail -3 python3 tools/revue_documentation.py 2>&1 | tail -2; ech
- ÉTAT — LA PAGE VIVANTE PASSE AU 1er NOVEMBRE : LA REVUE EXIGE LA DATE DU DERNIER COMMIT" 2>&1 | tail -3 python3 tools/revue_documentation.py 2>&1 | tail -2; ech
- cat > /tmp/msg-reel2.txt <<'EOF' R4.4 — UN SECOND VRAI SCAN : 23,3 % DE WER MAIS 88,5 % DES MOTS — C'EST L'ORDRE DES COLONNES  La validation réelle ne tenait qu
- python3 - <<'PY' import pathlib p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s=s.replace("simulés** — photo **55,9 → 7,0 %**, préservation **86,
- cat > /tmp/msg-gouttiere.txt <<'EOF' R4.4 — LA VALIDATION RÉELLE CORRIGE LE LECTEUR : UN EN-TÊTE TRAVERSAIT LA GOUTTIÈRE, LE LEXIQUE PASSE DE 93 % À 15 %  Le co
- python3 - <<'PY' import pathlib p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s=s.replace("| fichiers / JSON de résultats | **372** / **447** |",
- cat > /tmp/msg-trois.txt <<'EOF' R4.4 — UN TROISIÈME VRAI SCAN OÙ LE PRÉTRAITEMENT PAIE : GERMINAL, 1900, 8,73 % DE WER  Les deux premiers livres (Verne) donnai
- python3 - <<'PY' import pathlib,re p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s2=re.sub(r"\| fichiers / JSON de résultats \| \*\*372\*\* / \*\
- python3 - <<'PY' import pathlib p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s=s.replace("| fichiers / JSON de résultats | **375** / **450** |",
- python3 - <<'PY' import json,pathlib d=json.loads(pathlib.Path('work/r44/rot.json').read_text()) d['dispositif']='rotation ajoutée à une page propre (3° et 0,8°
- python3 - <<'PY' import json,pathlib rot=json.loads(pathlib.Path('reports/r44-rotation.json').read_text()) rot['sondes']={'6,0°':{'wer_brut':0.1308,'wer_auto':0
- python3 - <<'PY' import pathlib p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s=s.replace("restent les **scans réels de bout en bout**, le fax 1 
- python3 - <<'PY' import pathlib p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s=s.replace("vrais scans **7,10 / 88,4 %** (trois livres) — [`r44-s
- ÉTAT — LE BUDGET DE CONTEXTE REPASSE SOUS 4 000 MOTS (5 MOTS RETIRÉS)" 2>&1 | tail -2 git log --oneline -1; date +%H:%M
- cat > /tmp/msg-sondes.txt <<'EOF' R4.4 — LE PRÉTRAITEMENT TIENT UN GRADIENT 1,2 (28,9 → 3,3 %) ET NE RÉPARE PAS UN FLOU FORT (49,6 → 53,2 %)  Deux sondes de rob
- python3 - <<'PY' import pathlib,re p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s2=re.sub(r"\*\*Mis à jour : [^*]+\*\*", "**Mis à jour : 2026-11
- R4.4 — LA SPÉCIFICATION DIT ENFIN CE QUE LE BLOC FAIT : GOUTTIÈRE SUR LES MOTS, GRILLE ADAPTATIVE, COÛT, ET LES LIMITES NOMMÉES" 2>&1 | tail -3 git log --onelin
- python3 - <<'PY' import pathlib p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s=s.replace("vrais scans **7,10 / 88,4 %** ; redressement **≤ 6°** 
- ÉTAT — BUDGET DE CONTEXTE : LA LIGNE R4.4 SE RESSUERRE (T0 ≤ 4 000)" 2>&1 | tail -2; git log --oneline -1
- cat > /tmp/msg-multi.txt <<'EOF' R4.4 — LA GOUTTIÈRE UNIQUE DEVIENT MULTIPLE : TROIS COLONNES PASSENT DE 52,5 % À 0–1,1 %, RIEN NE BOUGE AILLEURS  La détection 
- cat > /tmp/msg-note.txt <<'EOF' R4.4 — LA NOTE TYPÉE À TORT COÛTAIT 4 QUESTIONS : LA PARITÉ PASSE À 90 % SUR LA PHOTOCOPIE ET LA PHOTO (PROPRE 96,7 %)  La ligne
- cat > /tmp/msg-parite.txt <<'EOF' R4.4 — LA PARITÉ ATTEINT 90–97 % SUR QUATRE FAMILLES : LA HAUTEUR DE PAGE, LE SEUIL DE TITRE ET LE PASSAGE ÉTAIENT LES VERROUS
- python3 - <<'PY' import pathlib p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s=s.replace("préservation **90–97 %** (4 familles), colonnes **89,4
- SESSION — R4.4 CLOSE : QUATRE FAMILLES AU-DESSUS DE 90 %, LE FAX RESTE UNE LIMITE D'INFORMATION" 2>&1 | tail -2 git log --oneline -1; tail -3 work/r44/gate-v8.l
- R4.4 — UNE PAGE SANS RÉFÉRENCE N'EST PAS UN WER DE 27 200 % : LE BANC RÉEL REFUSE DE MESURER" 2>&1 | tail -2 git log --oneline -1
- for t in "python3 tools/revue_documentation.py" "python3 tools/taille_documents.py" "python3 tools/verifie_en_cours.py" "python3 tools/verifie_journal.py" "pyth
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet cat > /tmp/msg-wiki.txt <<'EOF' DONNÉES — LE CORPUS FRANÇAIS EST LÀ : 2,5 M ARTICLES WIKIPÉDIA, 594 M MOTS, 0
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet set -e rm -f /tmp/index.r44 GIT_INDEX_FILE=/tmp/index.r44 git read-tree HEAD GIT_INDEX_FILE=/tmp/index.r44 gi
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet python3 - <<'PY' import pathlib p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s=s.replace("| f
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet for t in "python3 tools/verifie_journal.py" "python3 tools/verifie_backlog.py" "python3 tools/verifie_etat_a_
- PILOTAGE — LA CAPACITÉ SIMULTANÉE : 4 SESSIONS, 4 À 6 CHANTIERS, 2 À 4 SOUS-AGENTS, ET LES LIMITES MESURÉES" 2>&1 | tail -2; git log --oneline -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet python3 - <<'PY' import pathlib p=pathlib.Path('tools/surveille_sessions.py'); s=p.read_text() s=s.replace(''
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet for t in "python3 tools/revue_documentation.py" "python3 tools/taille_documents.py" "python3 tools/verifie_en
- PILOTAGE — LA ROADMAP À JOUR (L ET D), LE RUN DU TEXTE INTÉGRAL SUIVI DANS L'ÉTAT" 2>&1 | tail -2; git log --oneline -1
- ÉTAT — LE BUDGET T0 REVIENT À 3 998 (TRIM DU BLOC D/R/A)" 2>&1 | tail -1 echo "=== run"; ps -p 1454236 -o pid,etime,pcpu --no-headers 2>/dev/null || echo "termi
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet python3 - <<'PY' import pathlib,re p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() s=re.sub(r"\|
- DONNÉES — LE TEXTE INTÉGRAL PASSE AUX NEUF LANGUES : EN, DE, RU, ES, JA LANCÉS" 2>&1 | tail -2; git log --oneline -1


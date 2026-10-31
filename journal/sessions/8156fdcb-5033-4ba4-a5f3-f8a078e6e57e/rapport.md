# Session 8156fdcb — Réviser roadmap et backlog, établir priorités

> **Journaux :** [le jour](../../2026-10-29/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `8156fdcb-5033-4ba4-a5f3-f8a078e6e57e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-29 08:40 |
| Durée | 28.9 h |
| Tours | 23 |
| Messages | 750 |
| Appels d'outils | 805 |
| Fichiers touchés | 58 |
| Commandes | 560 |
| Sous-agents | 2 |
| Commits | 40 |
| Compactages de contexte | 1 |

## Objectifs déclarés

- **create** — Livrer R0.1 — le graphe de document : spécification du manifeste, parseurs Markdown/HTML/PDF/DOCX/EPUB, porte des 50 pages (couverture, offsets exacts, hashes, provenance, rejeu), contrôles négatifs (texte plat, PDF deux colonnes, notes/légendes), fiche de résultat dans reports/, état et roadmap à j
… [12 caractères tronqués]
- **complete** — Livrer R0.1 — le graphe de document : spécification du manifeste, parseurs Markdown/HTML/PDF/DOCX/EPUB, porte des 50 pages (couverture, offsets exacts, hashes, provenance, rejeu), contrôles négatifs (texte plat, PDF deux colonnes, notes/légendes), fiche de résultat dans reports/, état et roadmap à j
… [12 caractères tronqués]
- **create** — Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases : (1) élargir le banc des paraphrases de 19 à au moins 80 questions écrites à la main et vérifiées (recouvrement question↔gold < 0,5), puis rejouer dessus R0.3 (extractif + modèle), R0.4 (tête de survol, 
… [576 caractères tronqués]
- **complete** — Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases : (1) élargir le banc des paraphrases de 19 à au moins 80 questions écrites à la main et vérifiées (recouvrement question↔gold < 0,5), puis rejouer dessus R0.3 (extractif + modèle), R0.4 (tête de survol, 
… [576 caractères tronqués]
- **create** — Poursuivre en autonomie le programme R (lecteur) pendant plusieurs heures, en trois phases mesurées, écrites et committées : (1) **Corpus gelé** — figer le corpus des bancs (copie des documents dans tools/tests/documents/corpus/ + manifeste sha256), repointer les constructeurs (banc_complet.py, banc
… [1002 caractères tronqués]
- **complete** — Poursuivre en autonomie le programme R (lecteur) pendant plusieurs heures, en trois phases mesurées, écrites et committées : (1) **Corpus gelé** — figer le corpus des bancs (copie des documents dans tools/tests/documents/corpus/ + manifeste sha256), repointer les constructeurs (banc_complet.py, banc
… [1002 caractères tronqués]
- **create** — Poursuivre en autonomie le programme R pendant plusieurs heures, en trois phases : (1) **Le déclencheur sans échelle** — construire et mesurer les signaux qui ne dépendent pas de l'échelle des scores (accord entre lecteurs span/extractif, dispersion relative top1-top2, couverture de la réponse par l
… [998 caractères tronqués]
- **complete** — Poursuivre en autonomie le programme R pendant plusieurs heures, en trois phases : (1) **Le déclencheur sans échelle** — construire et mesurer les signaux qui ne dépendent pas de l'échelle des scores (accord entre lecteurs span/extractif, dispersion relative top1-top2, couverture de la réponse par l
… [998 caractères tronqués]
- **create** — Poursuivre en autonomie le programme R pendant plusieurs heures, en trois phases : (1) **La courbe de calibration** — mesurer combien de questions avec golds sont nécessaires pour calibrer le seuil de la cascade à confiance : pour k ∈ {10, 20, 40, 60, 80, 100 % de la moitié de calibration}, répéter 
… [919 caractères tronqués]
- **complete** — Poursuivre en autonomie le programme R pendant plusieurs heures, en trois phases : (1) **La courbe de calibration** — mesurer combien de questions avec golds sont nécessaires pour calibrer le seuil de la cascade à confiance : pour k ∈ {10, 20, 40, 60, 80, 100 % de la moitié de calibration}, répéter 
… [919 caractères tronqués]
- **create** — Publier la cascade à confiance calibrée dans le pipeline, comme l'état (`en-cours`) le désigne comme prochaine action de la session 8156fdcb : (1) **L'outil de calibration** — `tools/calibrer.py` qui prend un banc (questions + golds), calcule la confiance de chaque question, règle le seuil (le taux 
… [919 caractères tronqués]
- **complete** — Publier la cascade à confiance calibrée dans le pipeline, comme l'état (`en-cours`) le désigne comme prochaine action de la session 8156fdcb : (1) **L'outil de calibration** — `tools/calibrer.py` qui prend un banc (questions + golds), calcule la confiance de chaque question, règle le seuil (le taux 
… [919 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — révise le nouveau roadmap.md et le backlog. Note bien les dépendences de chaque items de chaque chantier (graphe) Travaillons ensemble pour établir les priorités du backlog

**Tour 2** — allons-y!

**Tour 3** — continue, prends bien soin de noter ce sur quoi tu travaille pour ne pas avoir de conflits avec les autres sessions

**Tour 4** — continue

**Tour 5** — go

**Tour 6** — passe directement au gpu

**Tour 7** — go

**Tour 8** — continue

**Tour 9** — continue

**Tour 10** — fais les

**Tour 11** — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h

**Tour 12** — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases : (1) élargir le banc des paraphrases de 19 à au moins 80 questions écrites à la main et vérifiées (recouvrement question↔gold < 0,5), puis rejouer dessus R0.3 (extractif + modèle), R0.4 (tête de survol, états précoces) et R0.5 (routeur extractif/génératif) ; écrire les fiches d … [1046 caractères tronqués]

**Tour 13** — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases : (1) élargir le banc des paraphrases de 19 à au moins 80 questions écrites à la main et vérifiées (recouvrement question↔gold < 0,5), puis rejouer dessus R0.3 (extractif + modèle), R0.4 (tête de survol, états précoces) et R0.5 (routeur extractif/génératif) ; écrire les fiches d … [1046 caractères tronqués]

**Tour 14** — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases : (1) élargir le banc des paraphrases de 19 à au moins 80 questions écrites à la main et vérifiées (recouvrement question↔gold < 0,5), puis rejouer dessus R0.3 (extractif + modèle), R0.4 (tête de survol, états précoces) et R0.5 (routeur extractif/génératif) ; écrire les fiches d … [1046 caractères tronqués]

**Tour 15** — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases : (1) élargir le banc des paraphrases de 19 à au moins 80 questions écrites à la main et vérifiées (recouvrement question↔gold < 0,5), puis rejouer dessus R0.3 (extractif + modèle), R0.4 (tête de survol, états précoces) et R0.5 (routeur extractif/génératif) ; écrire les fiches d … [1046 caractères tronqués]

**Tour 16** — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases : (1) élargir le banc des paraphrases de 19 à au moins 80 questions écrites à la main et vérifiées (recouvrement question↔gold < 0,5), puis rejouer dessus R0.3 (extractif + modèle), R0.4 (tête de survol, états précoces) et R0.5 (routeur extractif/génératif) ; écrire les fiches d … [1046 caractères tronqués]

**Tour 17** — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases : (1) élargir le banc des paraphrases de 19 à au moins 80 questions écrites à la main et vérifiées (recouvrement question↔gold < 0,5), puis rejouer dessus R0.3 (extractif + modèle), R0.4 (tête de survol, états précoces) et R0.5 (routeur extractif/génératif) ; écrire les fiches d … [1046 caractères tronqués]

**Tour 18** — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h

**Tour 19** — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h

**Tour 20** — continue

**Tour 21** — continue (examine d'abord en-cours.md)

**Tour 22** — continue (le wbs de en-cours.md n'est probablement pas le meilleur outil pour voir les dépendances et bloquants)

**Tour 23** — ok, pour la suite. en passant, je tiens a avoir une vue graphique des chantiers. le wbs n'indiquait pas les dépendances et sources de bloquages. le gant était étalé en jours et on travaille sur des périodes de temps plus courtes. il faut trouver mieux pour aider à la pride de décision rapide par l'humain et la les agents. J'ai encore un peu de difficulté à associer les sessions aux écrans actifs q … [172 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — révise le nouveau roadmap.md et le backlog. Note bien les dépendences de chaque items de chaque chantier (graphe) Travai … [52 caractères tronqués]

*215 appels d'outils.* Actions notables :

- read
- bash — List backlog directory and line counts
- bash — Read the four blocked compact fiches
- bash — Check git status, recent commits, implantation docs
- bash — List pilotage and schemas dirs, read illustration rules
- bash — Inspect schema verifier and doc review tooling
- bash — List tools and read manques.md
- bash — Read schemas README and revue structure
- bash — Grep for orphan identifiers across pilotage docs
- bash — Read revue_documentation main checks
- bash — Check date, last commit, doc review baseline, docs count
- bash — Inspect gate runner and a sample gate
- bash — Check document size budgets and table gate
- bash — Check for SVG rasterizers and docwatch
- … et 152 autres

**Synthèse produite :**

⏵ Clôture : décisions appliquées, graphe à jour, contrôles verts

C'est fait — revue, graphe et arbitrages sont écrits et committés (`e59f7c09`, `9539d8af`), arbre propre.

\## Ce qui a changé dans le plan

| arbitrage | décision | conséquence écrite |
|---|---|---|
| **Hiérarchie** | **N2 la porte** ; R11 en mesure la fenêtre et **attend N2** | `R11` repasse en arête dure sur `N2` ; la fiche N2 dit le levier et arrête les longueurs brutes |
| **SFT** | `N4` = **consigne courte sans document** ; `R31` = **lecture multi-sections** (gist, citations, refus) | les deux périmètres sont écrits dans les fiches ; le protocole de partage par document est commun |
| **Échelle** | `N5` **gelé** jusqu'au verdict de R11 | la roadmap marque ⏸ et la file « jamais en attente » le sort de la liste |
| **R0** | **R0.1 → R0.2 → R0.3**, ordre strict | la roadmap et l'état ne disent plus « en parallèle » ; `R03.2` est la mesure jointe de `R02` |

**Le point de tension, nommé** : avec ce choix, `N2` porte deux choses à la fois — sa porte `< 2,5` et le changement d'architecture (état de section). C'est le point de charge du plan. Et `R03` venant en dernier, la première courbe vitesse-compréhension n'arrive qu'après `R01` et `R02`.

\## L'ordre qui en résulte

- **P0** — `R01` → `R02` → `R03` (aucun entraînement, tout le reste se mesure avec) ; `N0.3b` en parallèle, coût faible.
- **P1** — `N2` (la hiérarchie), puis `R11`/`R12` ; `N4`, `R21`, `R31` ; `R04`, `R05`.
- **P2** — `R22`, `R06`, `R32`, `R41`, `R42`, `R13` ; `N3`, `B11.10`, `B12.10`, `A2.6`, `A3.2`, `A8.0`.
- **P3 / gelé / bloqués** — `R43`, `R44`, `R51`, `R52`, `B10.3` (+ `B10.2bis`), `A3.3`, `A8.3` ; `N5` gelé ; les quatre ressources externes.

\## Les artefacts du graphe

- **[`dependances.md`](docs/pilotage/backlog/dependances.md)** — les tables par chantier (générées, jamais recopiées), les 7 défauts corrigés, la frontière réelle (12 items), les sous-items (`R01.1/R01.2`, `R03.1/R03.2`, `R22a/R22b`) et le § 6 avec les décisions.
- **[`backlog-dependances.svg`](docs/schemas/backlog-dependances.svg)** — 37 nœuds, 41 arêtes dures, 3 plafonds, 9 rangées ; routage orthogonal vérifié (aucune arête ne traverse une boîte).
- **`tools/verifie_backlog.py`** — relit les fiches, détecte arêtes mortes, cycles, priorités inversées, calcule la frontière et la profondeur (5 : `R01 → R02 → R03 → R31 → R32 → R51`). Il signale trois **trous nommés** : `B10.3 → B10.2bis`, `A3.3 → A3.2`, `A8.3 → A8.0` — ce sont les prochaines fiches à écri
… [549 caractères tronqués]

### Tour 2 — allons-y!

*117 appels d'outils.* Actions notables :

- bash — Inventory reading-related tools and reports
- bash — Read existing reading bench tool
- bash — Check existing multi-file reader report
- bash — Read the bench specification section
- bash — Check parsing libraries and binaries
- bash — Look for existing document corpus
- create_goal
- bash — Inspect a UN PDF layout and extraction
- bash — Count corpus and check fixture tooling
- bash — Check the reference txt extraction
- bash — Test normalization match between txt reference and pdftotext modes
- bash — Compare pypdf and pdftotext word multisets
- todo_write
- sous-agent — Parseur HTML de document
- … et 96 autres

**Synthèse produite :**

⏵ R0.1 livré et commité, arbre propre

**R0.1 est mesuré.** Commit `4ffa34b7`, arbre propre, les contrôles passent.

\## Le chiffre

| mesure | valeur |
|---|---|
| pages découpées | **51** (30 documents, 5 formats) |
| régions | **1 423** hors blancs (2 816 au total), **11 types** |
| fidélité indépendante | **1,0000** sur **30/30** documents |
| partition · provenance · rejeu | **30/30** chacune |
| durée de la porte | **5,4 s** |

Et un second contrôle plus large : les **451 Markdown du dépôt** (13 279 régions) passent partition, provenance et fidélité — minimum **0,9996**, 1,7 s, zéro échec. C'est le corpus le plus dur : la source est la référence, donc chaque mot doit s'y retrouver.

\## Les quatre contrôles négatifs

- **texte plat** → une seule région, la porte le voit et le refuse ;
- **PDF deux colonnes** → `GGGGGGDDDDDD`, **0 retour** (le générateur de la fixture est dans le parseur) ;
- **notes hors corps** → 120 notes, **0 fuite** ;
- **« où est le tableau X ? »** → 30 tableaux, l'offset pointe bien une ligne de tableau, sans modèle.

\## Ce qui est en place

- `tools/graphe_document.py` — manifeste, partition en **octets UTF-8**, hashes, provenance, fidélité, porte ;
- `tools/graphe_document_html.py` (sous-agent, 3 fixtures) et `tools/graphe_document_pdf.py` (écrit par moi après l'échec du sous-agent) ; DOCX/EPUB via pandoc → GFM ;
- `docs/implantation/document-graph.md` — la spécification (deux espaces d'offsets, six invariants, trois contrôles) ;
- `tools/porte-document.sh` — le registre passe à **50 portes** ;
- `reports/rapport-r01-graphe-document.md` + le JSON brut.

\## Ce qui pourrait le rendre faux (et que j'ai nommé)

1. **La fidélité PDF est un recouvrement de caractères** : elle prouve le contenu, pas l'ordre. L'ordre n'est testé que par une fixture **synthétique** — un PDF académique réel à deux colonnes manque au corpus, c'est la première dette.
2. **Les notes sont une heuristique** (corps plus petit) : un en-tête courant est typé `note`.
3. **Aucun tableau PDF, aucun scan, aucune figure** : assumé et borné (R4.1, R4.4).
4. Le seuil de 0,99 sur 6 documents seulement par format n'est pas un taux par type.

\## La suite

La roadmap pointe maintenant **R0.2 — le contrôleur de lecture** : `R02` est passée dans la frontière automatiquement (la porte du graphe l'a recalculée). Le banc `R0.3` viendra après, et sa courbe est la mesure jointe du contrôleur — une seule fiche de résultat pour les deux.

Tu veux que j'enchaîne sur **R0.2** (survol
… [136 caractères tronqués]

### Tour 3 — continue, prends bien soin de noter ce sur quoi tu travaille pour ne pas avoir de conflits avec les autres sessions

*37 appels d'outils.* Actions notables :

- bash — Check other sessions' state before claiming files
- bash — Check session convention and existing retrieval code
- bash — Read the single-writer protocol
- bash — Claim R0.2 scope and fix state inconsistencies
- bash — Fix session block and amend commit
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/lecteur_controleur.py`
- bash — First controller run on a real question
- bash — Compare full read vs 30% and 10% budgets
- bash — Read format-flux facts for question design
- bash — Find exact gold strings in the five documents
- bash — Check UN and format-flux exact passages
- bash — Add full-read mode to controller
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/documents/bench-pilote.json`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_lecture.py`
- … et 23 autres

**Synthèse produite :**

⏵ R0.2 livré, état commité, aucune collision

**R0.2 est mesuré.** Commit `08149617`, arbre propre, tous les contrôles verts.

\## Le chiffre

| type | récupération à 30 % | valeur à 30 % | valeur à 100 % | coût réel | aléatoire |
|---|---:|---:|---:|---:|---:|
| technique | **1,000** | 0,750 | 0,750 | **24 %** | 0,500 |
| prose | **1,000** | 0,500 | 0,500 | **7 %** | 0,000 |
| tableau | **1,000** | 0,750 | 0,750 | **17 %** | 0,000 |
| juridique | **1,000** | 0,250 | 0,250 | **22 %** | 0,250 |
| code | **1,000** | 0,500 | 0,500 | **20 %** | 0,000 |

**Le contrôleur ne perd rien** : à 30 % du budget, il lit le passage gold dans **100 %** des cas sur les 5 types, pour 7 à 24 % du document. **Le lecteur plafonne** : même en lisant tout, l'extractif classique ne trouve la valeur que dans 25 à 75 % des cas. La sélection est un problème de contrôleur — et il est résolu ; la compréhension reste un problème de lecteur/modèle.

Contrôles négatifs : aléatoire 0,000–0,500, sans but 0 réponse, closed-book 0, passages mélangés 1,000 (le contrôleur ne dépend pas de l'ordre). Déterminisme vérifié : deux exécutions → même SHA.

\## Le protocole anti-conflit

- **Périmètre noté dans `en-cours`** avant de coder : ma session `8156fdcb`, le rôle, les **fichiers réservés** (`tools/lecteur_controleur.py`, `tools/banc_lecture.py`, `tools/porte-lecteur.sh`, les deux specs, `reports/r02-*`, les fiches R02/R03), commit `19db1632`.
- **Un seul écrivain par fichier** : je n'ai touché ni aux fiches A/B de l'autre session ni à ses rapports.
- **Commit par unité** : le périmètre d'abord, le résultat ensuite, chacun sur l'état réel du dépôt.

**Une collision évitée** : la session N0.3b a commité `bc4e3d92` pendant que je travaillais (parité DRVM ↔ GGUF close). Son commit ne touche que `journal/` et `reports/` — la **roadmap et l'état disent encore N0.3b ouverte**. Je ne les ai pas modifiés : c'est son périmètre, et deux writers sur `en-cours` se seraient écrasés. À signaler à la principale pour qu'elle applique son diff d'état.

\## Ce qui est en place

- `tools/lecteur_controleur.py` — passages, BM25, cinq actions, budget en octets, trace ;
- `tools/banc_lecture.py` — 6 modes, 4 métriques, 4 contrôles négatifs ;
- `tools/porte-lecteur.sh` — le registre passe à **51 portes** ;
- les specs [`lecteur-controleur.md`](docs/implantation/lecteur-controleur.md) et [`banc-lecture.md`](docs/implantation/banc-lecture.md) ;
- le banc pilote [`bench-pilote.json`](tools/tests/documents/bench-pilote.json
… [585 caractères tronqués]

### Tour 4 — continue

*43 appels d'outils.* Actions notables :

- bash — Check for local model and LLM credentials
- bash — Inspect drave binary CLI
- bash — Show drave modes with a model
- bash — Find the inference flags in the engine
- bash — Read run_infer to learn prompt/output format
- bash — Test a short generation with the local model
- bash — Capture the generated text output
- bash — Filter engine diagnostics to see the text
- bash — Test the model on a real bench question
- bash — Claim R0.3 and commit the claim
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/lecteur_modele.py`
- bash — Test the model reader self-test
- bash — Wire the model reader into the bench
- bash — Run model-reader bench in background
- … et 23 autres

**Synthèse produite :**

⏵ R0.3 première tranche livrée, protocole respecté, arbre propre

**R0.3 première tranche est mesurée.** Commit `5a2fffae`, arbre propre, contrôles verts.

\## Le chiffre

| type | contrôleur | début | hasard | closed-book |
|---|---:|---:|---:|---:|
| code | **1,00** | 0,50 | 0,00 | 0,00 |
| tableau | **0,50** | 0,00 | 0,00 | 0,00 |
| technique | 0,50 | 0,50 | 0,00 | 0,00 |
| juridique | 0,50 | 0,50 | 0,00 | 0,00 |
| prose | 0,00 | **0,50** | 0,00 | 0,00 |
| **agrégat** | **0,500** | **0,400** | **0,000** | **0,000** |

**Contrôleur devant 2 types, à égalité 2, derrière 1.** L'écart agrégé vaut **une question** : c'est une indication, pas une mesure — et c'est écrit dans la fiche avant de conclure. Dix questions, un modèle de 0,5 B, une fenêtre de 1 200 caractères.

**Ce que la prose dit** : les documents du dépôt mettent leur thèse dans les 1 200 premiers caractères, donc « prendre le début » est une baseline forte ; le contrôleur, lui, sélectionne par recouvrement de mots et rate la phrase qui définit « drave ». C'est un **biais de conception** : contrôleur et lecteur extractif partagent BM25.

\## Deux fautes de méthode trouvées — invisibles sans le modèle

1. **Le mode « début » tombait sur la lecture intégrale** (un `startswith` manquant) : il semblait battre le contrôleur avec dix fois son budget.
2. **Le contexte était donné dans l'ordre de lecture** : les meilleurs passages du contrôleur, plus loin dans le document, étaient coupés par la fenêtre. Il était jugé sur ce qu'il n'avait pas pu donner. Corrigé : priorité par score.

Sans le modèle, la première exécution aurait conclu « le contrôleur ne sert à rien » — faux.

\## Le protocole anti-conflit, appliqué comme demandé

- **R0.3 réservé dans `en-cours` avant de coder** (commit `1359d13f`) : rôle, fichiers réservés (`tools/lecteur_modele.py`, `banc_lecture.py`, `porte-lecteur.sh`, `bench-pilote.json`, les specs, `reports/r03-*`, la fiche R03), prochaine action.
- **Aucun fichier d'une autre session touché** ; le commit N0.3b (`bc4e3d92`) est passé entre deux des miens sans collision, et mon commit suivant s'est appliqué proprement par-dessus.
- **Aucune nouvelle porte** : le modèle coûte 15 s par génération, il reste une mesure manuelle (`--depuis` relit le JSON) ; le registre reste à 51.

\## Ce qui est en place

- `tools/lecteur_modele.py` — le modèle comme lecteur (moteur local, greedy, extraction de la réponse, autotest « trouve / n'invente pas ») ;
- `banc_lecture.py --lecteur modele` — trois fa
… [766 caractères tronqués]

### Tour 5 — go

*52 appels d'outils.* Actions notables :

- bash — Diagnose the prose selection failure
- bash — Audit ambiguous questions via model answers present in the document
- bash — Fix numeric normalization and ambiguous question
- bash — Re-run model bench with corrected questions
- bash — Implement coverage criterion and test on prose
- bash — Run extractive bench with coverage criterion
- bash — Compare extractive results for both criteria
- bash — Check model baseline progress
- bash — Wait for the model baseline
- bash — Wait for baseline completion
- bash — Read baseline and start coverage run
- bash — Check coverage run and baseline aggregates
- bash — Run model bench with coverage criterion
- bash — Wait for coverage criterion run
- … et 37 autres

**Synthèse produite :**

⏵ Réponse : non, et c'est corrigé — le CPU était saturé par deux bancs en double, les GPU à 0 %

**Non, on n'en faisait pas bon usage — et c'était de ma faute.** Voici ce qui s'est passé, ce que j'ai corrigé, et ce que ça change aux chiffres.

\## Ce qui saturait le CPU

Deux bancs modèle **identiques** tournaient en parallèle : un lancé avec `&` (resté orphelin) et un lancé proprement. Chacun exécutait le `--infer` du moteur Drave, qui est **CPU pur, 20 fils**. Résultat : **~38 cœurs à 1900 %** chacun, pendant que les deux **Quadro RTX 5000 restaient à 0 %** (1 Mio occupé). Pire : les deux calculaient la même chose.

Le moteur n'a pas d'offload GPU pour l'inférence (`--gpu-banc` est un banc, pas un chemin d'exécution). C'est une limite du chemin `--infer`, pas du matériel.

\## Ce que j'ai corrigé

| avant | après |
|---|---|
| drave `--infer`, 20 fils CPU, **8–15 s**/appel | `llama-cli` **CUDA**, `-ngl 99`, `-t 4`, **1,9 s**/appel |
| deux GPU inutilisés | **un seul** GPU (`CUDA_VISIBLE_DEVICES=0`), l'autre **libre pour N2** |
| deux bancs en double | un seul, et le job est suivi par son identifiant |

Mesure du gain : **1 409 t/s** de prompt et **273 t/s** de génération sur GPU, contre ~30 t/s sur CPU. Les 30 générations d'un banc passent de ~10 min à **50 s**.

\## Ce que ça change aux chiffres (et il faut le dire)

Le runtime **fait partie du dispositif** : le même GGUF, le même prompt, le même greedy donnent **0,6** sur le moteur CPU et **0,5** sur `llama-cli`. Les deux chiffres ne se comparent pas — c'est maintenant écrit dans la fiche.

**R0.3, chiffres propres** (10 questions, modèle 0,5 B, fenêtre 1 200 caractères) :

- **contrôleur 0,500** · troncature naïve **0,400** · hasard **0,000** · closed-book **0,000** ;
- contrôleur devant 2 types, à égalité 2, derrière 1 (le code) ;
- le **critère de sélection** (BM25 vs couverture) donne **exactement les mêmes chiffres** : à 10 questions, le banc ne départage pas.

Et quatre fautes de banc corrigées au passage — toutes invisibles sans le modèle : le mode « début » tombait sur l'intégrale, le contexte était tronqué dans l'ordre de lecture, le **bandeau de llama.cpp** était compté comme une réponse, et « 3,663 » contre « 3 663 » était compté faux. La question « drave » avait deux réponses valides : elle est désambiguïsée.

\## État des ressources, maintenant

- **CPU** : au repos (seul l'agent tourne) ;
- **GPU 0** : utilisé par le banc, en rafales de 1,9 s ;
- **GPU 1** : libre — N2 (la série hiérarchie) p
… [629 caractères tronqués]

### Tour 6 — passe directement au gpu

*35 appels d'outils.* Actions notables :

- bash — Extend the reservation for the full bench
- bash — Find documents with the most code blocks
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_complet.py`
- bash — Build the full bench
- bash — Fix corpus and rebuild full bench
- bash — Rebuild and verify the full bench
- bash — Restrict to numeric values and count
- bash — Build final bench and run extractive curve
- bash — Run full bench with GPU model reader
- bash — Read extractive full-bench curve
- bash — Confirm GPU is working on the model bench
- bash — Read the R0.3 section of the bench spec
- bash — Document the full bench
- bash — Wait for the model bench
- … et 19 autres

**Synthèse produite :**

⏵ Banc complet passé sur GPU, commité, sans collision

**C'est fait : le banc complet a tourné directement sur GPU.** Commit `72a4ff5f`, arbre propre, contrôles verts.

\## Les chiffres

**249 questions, 30 documents, 5 types**, valeurs numériques, deux modes de lecture.

| | extractif (3 s) | modèle GPU (13 min) |
|---|---|---|
| **à 30 % du budget** | récupération **1,000** sur les 5 types | contrôleur **0,231** |
| troncature naïve (début) | — | **0,042** |
| hasard / closed-book | 0,20–0,39 | **0,000** |

- **Extractif** : le passage gold est lu **100 %** du temps à 30 % ; la courbe mord à 10 % (0,87–1,00).
- **Modèle** : le contrôleur **gagne sur les 5 types, par 5,5×** — la sélection est validée à l'échelle.
- **Mais le taux absolu est bas (0,231)** : le modèle de 0,5 B **paraphrase la question** au lieu d'extraire le nombre. Et le lecteur extractif fait **mieux** sur ces questions (0,72–1,00) parce qu'il **rend le passage**, qui contient la valeur.

**Conclusion nette : pour une valeur numérique, rendre le passage bat générer — à cette taille de modèle.** Le pipeline doit donc être extractif par défaut, génératif seulement quand la question demande une synthèse.

\## Le GPU

- **GPU 0 seul** : 39 % d'utilisation pendant le run, **1,9 s par génération**, 498 générations en 13 min (le CPU aurait mis 4 à 5 heures) ;
- **GPU 1 libre**, CPU rendu au moteur et aux portes ;
- le lecteur est `llama-cli` CUDA (1 409 t/s de prompt, 273 t/s de génération), un seul GPU par `CUDA_VISIBLE_DEVICES`.

\## Deux fautes trouvées en route

1. **llama.cpp coupe un caractère UTF-8 en deux** dans son écho tronqué : le banc tombait sur un `UnicodeDecodeError`. Corrigé : lecture en octets, décodage tolérant.
2. **Le banc est adossé à des documents vivants** : ma réécriture du §7 de `banc-lecture.md` a invalidé ses golds. Corrigé : régénération du banc, et la limite est écrite dans la spec.

\## Coordination

La session principale a commité **N4.8 et sa clôture** pendant que je travaillais (`1853a65b`, `8114767d`). Mon commit s'est appliqué **par-dessus** : vérifié, son `en-cours` et sa narrative sont intacts, seules mes lignes ont changé. Un fichier traîne en non-suivi — `docs/pilotage/patch-multi-session.diff`, qui n'est pas de moi — je ne l'ai pas committé.

\## La suite

Les trois phases de R0 sont mesurées : le lecteur lit, choisit, et se mesure. Reste **R0.4** (les trois têtes : survol, balayage, relecture) — ou le **banc durci** (paraphrases), qui est la seule façon de sav
… [177 caractères tronqués]

### Tour 7 — go

*20 appels d'outils.* Actions notables :

- bash — Extract candidate golds for paraphrases
- bash — List question indices per selected document
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_durci.py`
- bash — Build and verify the hardened bench
- bash — Run extractive reader on paraphrases
- bash — Check session identity and hardened extractive results
- bash — Run model reader on paraphrases
- bash — Read model results on paraphrases
- bash — Fix model display with missing modes
- bash — Make the verdict message dynamic
- bash — Show hardened extractive results without false failure
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r03-banc-durci.md`
- bash — Update docs with the hardened bench
- bash — Identify newly added gate and JSONs
- … et 6 autres

**Synthèse produite :**

⏵ Banc durci livré, commité, pair R4.1 respecté

**Le banc durci est mesuré** — commit `de9afbc9`, arbre propre (hors un fichier généré du pair, voir plus bas).

\## Le chiffre

19 paraphrases écrites à la main, recouvrement question↔gold **0,20 en moyenne** (max 0,43, seuil 0,5) : le scoreur lexical ne peut plus gagner par recouvrement.

| | lexical | modèle (contrôleur) | troncature naïve | closed-book |
|---|---:|---:|---:|---:|
| **réponses justes à 30 %** | **0,30** | **0,717** | 0,133 | 0,000 |

Et la récupération du gold par le lexical tombe de **1,000** (banc complet) à **0,817** — jusqu'à **0,33 sur le juridique**.

\## Ce que ça dit : il n'y a pas UN meilleur lecteur

| régime | qui gagne | chiffre |
|---|---|---|
| questions qui partagent les mots du document | **le lexical** | 0,72–1,00 contre 0,23 |
| paraphrases | **le modèle** | 0,717 contre 0,30 |

Le pipeline doit **choisir** — et la décision se mesure (recouvrement question↔document). C'est le renversement que le banc complet, saturé à 1,000, ne pouvait pas montrer.

**Le contrôleur reste utile dans les deux régimes** : 0,717 contre 0,133 pour la troncature, soit **5,4×**.

**Une perte nommée** : sur le juridique, la troncature (0,67) **bat** le contrôleur (0,33) — la réponse est dans les 1 200 premiers caractères du PDF, et le contrôleur préfère d'autres passages. Un contrôleur qui ignore le début peut perdre.

\## Coordination (nouvelle règle AGENTS appliquée)

- **`git add` explicite**, jamais `-A` : je n'ai ajouté que mes dix fichiers. Les fichiers du **pair R4.1** — `tools/bloc_tableaux.py`, `tools/porte-bloc-tableaux.sh`, `tools/tests/tableaux/`, `reports/r41-bloc-tableaux.json` — sont **restés non suivis**, pas committés.
- Sa porte, que j'ai lancée pour classer le compteur, est **verte** ; le registre passe à **52 portes (50 vertes, 2 rouges structurelles)**, compteurs mis à jour.
- `reports/INDEX.md` reste modifié d'une ligne : c'est **sa** fiche R4.1 qui apparaît (index généré). Je laisse sa session la committer.

\## La suite

**R0.4 est désormais mesurable** : le scoreur classique ne sature plus sur le banc durci, une tête apprise (survol, balayage, relecture) peut donc être départagée. C'est la prochaine action — je la prends, ou je nomme d'abord le **routeur extractif/génératif** comme chantier, puisque les deux régimes sont établis ?

### Tour 8 — continue

*27 appels d'outils.* Actions notables :

- bash — Check for a hidden-state extractor in the engine
- bash — Read the state-dump implementation
- bash — Inspect the state file format
- bash — Read capturer_etat
- bash — Test early-state capture and cost
- bash — See the error for early-state capture
- bash — Capture early states with correct syntax
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tete_survol.py`
- bash — Capture early states for the relevance head
- bash — Check state extraction progress
- bash — Wait for extraction completion
- bash — Train and evaluate the relevance head
- bash — Fix meta alignment and evaluate the head
- bash — Add shuffled-label control and rerun
- … et 13 autres

**Synthèse produite :**

⏵ R0.4 pilote mesuré (négatif), commité avec pathspec explicite

**R0.4 est mesuré — et c'est un négatif net**, commit `0374ef78`, revue verte.

\## Le chiffre

114 paires (19 questions du banc durci × 1 gold + 5 négatifs du même document), états **après 4 couches** de Qwen 0.5B (896 valeurs, 2,2 s/paire), tête logistique ridge, **leave-one-document-out**, contrôle par étiquettes mélangées.

| document | AUC tête | AUC BM25 | mélangé |
|---|---:|---:|---:|
| juridique | **0,956** | 0,622 | 0,200 |
| technique | 0,588 | 0,800 | 0,500 |
| code | 0,450 | 0,794 | 0,575 |
| tableau | 0,550 | 1,000 | 0,412 |
| prose | 0,463 | 0,963 | 0,650 |
| **moyenne** | **0,601** | **0,836** | **0,467** |

**La tête perd 4 fois sur 5, et elle gagne exactement là où BM25 est faible** — le juridique, le régime paraphrase.

Le contrôle à **0,467** (≈ hasard) est essentiel : il prouve que les 0,601 sont un signal réel, faible, et **pas une fuite** (longueur, type, ordre).

\## Pourquoi elle perd — quatre raisons nommées

1. **90 paires pour 896 dimensions** : elle apprend le style des documents d'entraînement.
2. **4 couches, c'est très tôt** : l'état encode la forme, pas la question.
3. **Négatifs aléatoires** : 5 passages au hasard contre 1 gold, BM25 les sépare sans peine.
4. **Reranking à 6 candidats ≠ recherche dans le document** : la faiblesse de BM25 mesurée en R0.3 (0,33) portait sur la recherche ; ici il ne classe que 6 candidats.

**La porte R0.4 n'est pas atteinte.** La fiche reste ouverte avec le chemin : plus de paires, états plus profonds, **négatifs difficiles**, tête non linéaire.

\## Coordination — le dépôt est très actif

Trois pairs ont commité pendant ce cycle (R4.1 bloc tableaux, B11.10 cartes, N4.8) :
- mon commit a utilisé **`git commit -- <chemins>` explicites** : rien de leur travail n'y est entré ;
- un premier essai a échoué sur `.git/index.lock` (un pair commitait) — j'ai attendu la libération et rejoué, sans supprimer le verrou ;
- leurs fichiers restent chez eux : `docs/implantation/bloc-tableaux.md`, `rapports r41`/`b1110`, et le `.diff` d'état du pair, non suivis ;
- compteurs recalculés sur le disque : **94 docs · 283 fiches · 350 JSON · 52 portes** (leur porte R4.1 est verte).

\## La suite

La leçon du cycle : **il n'y a pas un meilleur lecteur, il y a deux régimes** — lexical sur les mots, modèle sur les paraphrases, tête seulement là où BM25 décroche. La prochaine action utile n'est donc pas d'insister sur la tête telle quelle, mais de **nommer 
… [300 caractères tronqués]

### Tour 9 — continue

*9 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R07-routeur-extractif-generatif.md`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/routeur.py`
- bash — Run the router analysis
- bash — Add the coverage signal and rerun
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r07-routeur.md`
- bash — Update R07 fiche, index and roadmap
- bash — Fix counters, regenerate index, run checks
- bash — Commit the router partial result
- bash — Check remaining changes and final state

**Synthèse produite :**

⏵ R0.5 mesuré (partiel) et commité — le signal prédit, la règle non

**R0.5 — le routeur — est mesuré** : `23b98f14`, revue verte, GPU au repos.

\## Le chiffre

267 questions (248 lexicales + 19 paraphrases), deux lecteurs, ré-analyse des JSON de R0.3.

| mesure | valeur |
|---|---:|
| questions où les lecteurs **diffèrent** | 184 / 267 |
| **AUC du signal BM25** | **0,785** |
| AUC aléatoire · longueur (faux signal) | 0,407 · 0,395 |
| fixe extractif · fixe modèle · **oracle** | 0,816 · 0,270 · **0,888** |

**Le signal sait quelque chose** — 0,785 contre 0,407 au hasard, et la longueur de la question, faux signal, est sous le hasard.

**Mais la règle ne transfère pas** : un seuil appris sur un banc donne **0,496** sur le banc lexical (le choix fixe y fait 0,855) et **0,421** sur les paraphrases (le fixe y fait 0,737).

**L'arithmétique tranche** : le gain maximal (oracle) est de **7 points**, un seuil mal calibré en coûte **30**. Le routeur n'est **pas déployé** ; le choix par défaut reste l'**extractif** (0,816 contre 0,270, et il ne coûte rien), le modèle s'appelle à la demande.

\## Ce que le cycle a produit

- **`R07`** — une fiche de plus au backlog (20 pour R, 30 en tout) : contrat, porte, contrôles, risques ;
- **`tools/routeur.py`** — deux signaux, l'AUC, le transfert, les contrôles ; `reports/r07-routeur.json` (267 lignes) ;
- la fiche [`rapport-r07-routeur.md`](reports/rapport-r07-routeur.md) ;
- **R0.4** (tête de survol) reste un **négatif** : 0,601 contre 0,836, victoire seulement sur le juridique (0,956 contre 0,622), contrôle des étiquettes mélangées à 0,467 (pas de fuite).

**La leçon, écrite dans les deux fiches** : un signal qui **prédit** n'est pas une règle qui **décide**. La différence se mesure par le **transfert**, pas par l'AUC.

\## Coordination

Le dépôt a tourné à quatre sessions (R4.1, B11.10, N4.8, la mienne) : commits en `-- <chemins>` explicites, verrou d'index attendu sans être forcé, et seuls les fichiers de journal touchés par les hooks des pairs restent en attente — chez eux. Compteurs : **95 docs · 284 fiches · 351 JSON · 52 portes**, tous vérifiés par la revue.

\## La suite

Deux chemins, tous deux nommés dans les fiches :

1. **R0.5 v2** — un signal **relatif par document** (z-score ou percentile) et un banc paraphrase plus grand que 19 questions : c'est le maillon faible identifié, pas le signal ;
2. **R0.4 v2** — négatifs difficiles (même voisinage lexical) et états plus profonds (8–12 couches).

Le premier a le meille
… [210 caractères tronqués]

### Tour 10 — fais les

*12 appels d'outils.* Actions notables :

- bash — Add relative signals and rerun the router
- bash — Extract deeper states with hard negatives
- bash — Wait for deeper-state extraction
- bash — Continue waiting for extraction
- bash — Measure the deeper head with hard negatives
- bash — Add v2 sections to both reports
- bash — Update docs with both v2 results
- bash — Fix the file and JSON counters
- bash — Fix JSON counter and run all checks
- bash — Commit both hardened versions
- bash — Compute the z-score AUC for the report
- bash — Fix AUC numbers and amend the commit

**Synthèse produite :**

⏵ Les deux v2 sont mesurées et commitées (e0c7c837)

**Les deux sont faits.** Et les deux durcissements confirment le diagnostic : **le verrou, c'est le banc de paraphrases**, pas le signal ni la couche.

\## R0.5 v2 — le seuil relatif

Trois signaux sans échelle ajoutés (z-score du sommet dans la distribution du document, ratio, étendue).

| seuil appris sur l'autre banc, testé sur | z-score | ratio | étendue | brut |
|---|---:|---:|---:|---:|
| le banc lexical (n=248) | **0,734** | 0,355 | 0,234 | 0,496 |
| les paraphrases (n=19) | 0,474 | 0,474 | 0,368 | 0,421 |

**Le z-score transfère bien mieux** (0,734 contre 0,496) — la calibration par document est la bonne direction. **Mais il reste sous le choix fixe** (0,855 / 0,737). AUC : brut 0,781 · z 0,761 · ratio 0,686 · **étendue 0,272** (anti-corrélée : « large » ne veut pas dire « facile »).

\## R0.4 v2 — états 8–11, négatifs durs

| | v1 (4 couches, négatifs aléatoires) | v2 (11 couches, même section) |
|---|---:|---:|
| tête | 0,601 | **0,448** |
| BM25 | 0,836 | **0,811** |
| victoires | 1/5 | **0/5** |
| contrôle (étiquettes mélangées) | 0,467 | 0,556 |

**La v2 est pire, et c'est instructif** : les négatifs faciles aidaient BM25 *et* la tête ; les négatifs durs retirent la béquille, et **90 paires pour 896 dimensions s'effondrent**. La victoire juridique de la v1 était du bruit — la v2 la retourne (0,400 contre 0,600). Ce n'est pas « R0.4 impossible » : c'est « il faut des **centaines de paires** et un encodeur **ajusté**, pas une sonde linéaire ».

\## Le diagnostic commun

Les deux échecs pointent le **même verrou** : **19 paraphrases**. Trop peu pour apprendre le régime (R0.5), trop peu pour entraîner une tête (R0.4). Le signal est bon (AUC 0,781), la calibration par document est la bonne piste, la couche n'est pas le problème — **la donnée l'est**.

\## État

Commit `e0c7c837`, revue verte, compteurs à jour (**95 docs · 285 fiches · 353 JSON · 52 portes**), GPU au repos. Les fichiers de journal touchés par les hooks des pairs restent chez eux ; aucun de leurs travaux n'est entré dans mes commits.

\## La suite, maintenant évidente

**Élargir le banc des paraphrases** — c'est le seul geste qui débloque R0.4 *et* R0.5. Je peux écrire 60 à 80 paraphrases de plus à la main sur les golds du banc complet (le recouvrement est déjà vérifié automatiquement), puis rejouer les deux mesures. C'est du travail de rédaction, pas de calcul — et c'est ce qui manque.

### Tour 11 — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h

*40 appels d'outils.* Actions notables :

- create_goal
- bash — Dump candidate golds with context windows
- read
- bash — Add 55 new paraphrases and verify
- bash — List all rejected paraphrases
- bash — Rephrase rejects and add ten entries
- bash — Fix the last five and verify the 84-question bench
- bash — Finalize and inspect the 84-question bench
- bash — Run extractive reader on the 84-question bench
- bash — Run model reader on 84 paraphrases (GPU)
- bash — Extract states for the 84-question head
- bash — Read the 84-question extractive table
- bash — Wait for model bench and state extraction
- bash — Check running processes and temp state files
- … et 24 autres

**Synthèse produite :**

⏵ Cycle livré et commité (3328e0ec) — le goal continue

**Le banc durci a quadruplé : 19 → 84 paraphrases** (29 documents, recouvrement moyen **0,17**, max 0,43). Trois mesures rejouées et commitées.

\## Les trois résultats

| | sur 19 questions | sur 84 questions |
|---|---|---|
| modèle / lexical | 0,717 / 0,30 (+42 pts) | **0,375 / 0,269** (+11 pts) |
| tête / BM25 (R0.4) | 0,448 / 0,811 | **0,575 / 0,745** |
| routeur : AUC du signal | 0,781 | **0,826** |

**Ce que l'échelle change** :
- le modèle **garde l'avantage mais de moins en moins** : 0,717 → 0,375 quand le banc grandit, et il ne gagne plus que **4 types sur 5** (la technique repasse au lexical) ;
- la **tête progresse avec la donnée** (+13 points, 0,448 → 0,575) et gagne 6 documents sur 28 — mais reste **17 points sous BM25**, et le contrôle des étiquettes mélangées (0,548) montre qu'une partie de l'avantage est du bruit. Une sonde linéaire sur un 0,5 B ne suffira pas : il faut des milliers de paires et/ou un encodeur ajusté ;
- le **routeur** voit son signal monter (0,826) et son transfert z-score atteindre 0,802 sur le lexical — mais 0,321 sur les paraphrases, toujours sous le choix fixe. L'oracle se réduit : les lecteurs sont **moins complémentaires** qu'on ne le croyait.

\## Une correction de dispositif

La mesure de la tête **écrasait les six paires d'une question** (clé par question au lieu de la paire) : BM25 rendait 0,500 partout. Corrigé par un alignement positionnel, et le cache stocke désormais le passage. Le chiffre de 0,575 est le premier qui mesure vraiment la tête.

\## État

Commit `3328e0ec`, hook d'état vert (« aucun fait stagé sans état »), revue verte, compteurs **293 fiches · 364 JSON · 101 docs · 56 portes**. Les fichiers des pairs (journal, `rapport-a80`, `porte-coupe.sh`) restent chez eux.

**La suite du goal** : la tête restant négative, le blocage est nommé (données/encodeur). Je passe à l'**intégration du pipeline de lecture** — un `lecture.py` qui enchaîne manifeste → contrôleur → lecteur extractif (par défaut) → réponse avec provenance et trace rejouable, et sa porte. C'est ce qui transforme R0.1–R0.5 en outil utilisable, et cela ne dépend d'aucune donnée nouvelle.

### Tour 12 — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases … [1326 caractères tronqués]

*26 appels d'outils.* Actions notables :

- bash — Read the controller API
- bash — Read passages() and lire_document()
- bash — Calibrate the refusal threshold on real and nonsense questions
- bash — Inspect the manifest structure
- bash — Read repondre() and lire()
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/lecture.py`
- bash — Run the pipeline self-tests
- bash — Inspect the trajectory keys
- bash — Fix the byte counter and rerun the pipeline
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/pipeline-lecture.md`
- bash — Read an existing gate for style
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-lecture.sh`
- bash — Run the new pipeline gate
- bash — Inspect the pilot bench structure
- … et 12 autres

**Synthèse produite :**

⏵ Round 1 : pipeline R0.6 livré et mesuré — commit 8c2179fd, tout vert

**Le pipeline de lecture est livré** — la phase 2 de l'objectif (l'intégration), commit `8c2179fd`.

\## Ce que le pipeline fait

Une commande : `python3 tools/lecture.py --document X --question Q` → une réponse **avec sa source** (région, offset, sha), dans un budget en octets, avec une trace rejouable. **Extractif par défaut, modèle sur demande, refus motivé** quand la question ne partage rien avec le document.

\## Ce qu'il vaut, mesuré

| régime | chiffre |
|---|---|
| **pilote** (20 questions) | 19/20 acceptées · **12 justes (0,600)** · provenance **19/19** |
| **hors sujet** (10 questions) | **10/10 refusées** |
| **paraphrases** (8 questions) | extractif **3/8** · modèle **7/8** |
| **rejeu** | deux exécutions → mêmes octets |
| **porte** (6 contrôles) | **6/6 verts** |

**Le seuil de refus (3,8) est calibré, pas supposé** : les réponses justes du pilote scores 3,94–11,08, le seul faux positif hors sujet — « trois » dans « trois octets » — à 3,56. Il sépare, il refuse, et il est exposé (`--seuil`) parce qu'il ne se transporte pas d'un corpus à l'autre.

**La leçon de R0.3 devient utilisable** : le lexique pour les mots (0,600, coût ~0), le modèle pour les paraphrases (7/8), le refus comme aiguillage.

\## État du cycle

- deux commits : `3328e0ec` (banc 84 paraphrases + les trois v3) et `8c2179fd` (pipeline) ;
- **293 fiches · 364 JSON · 102 docs · 57 portes**, revue verte, porte état verte, porte lecture verte ;
- les fichiers des pairs restent chez eux ; le hook d'état a validé chaque commit de fait.

\## La suite (objectif toujours actif)

La roadmap désigne maintenant **R06** (tête de relecture — confiance et contradiction) ou **R11** (contexte hiérarchique et état de section). Je prends **R06** au prochain round : c'est la troisième tête du programme, et le pipeline lui donne enfin un usage — décider **quand** relire, plutôt que de relecture systématique.

### Tour 13 — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases … [1326 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Read the R06 fiche
- bash — Test whether re-reading more changes the extractive answer
- bash — Measure the refusal-triggered modality switch on 84 paraphrases
- bash — Test a content-word overlap trigger
- bash — Revert threshold to 1.0 and re-measure the pipeline
- bash — Measure the relecture rule at threshold 1.0
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r06-relecture.md`
- bash — Correct R0.6 and update the R06 fiche
- bash — Update counters, roadmap and state
- bash — Commit the R06 negative and the threshold fix

**Synthèse produite :**

⏵ Round 2 : R06 est un triple négatif, R0.6 corrigé — commit b8a1764b

**R06 est mesuré, et c'est un triple négatif** — mais il a aussi attrapé une faute dans ma propre livraison R0.6.

\## Les trois négatifs

**1. Relire plus ne sert à rien — exactement zéro.**
Sur les deux bancs, **aucune** question n'a une réponse fausse à 30 % et juste à 100 % (0/249, 0/84). Ce n'est pas un accident : le lecteur extractif répond avec le passage le mieux scoré, et ce passage est **toujours lu** (il est en tête). Le budget ne peut pas améliorer l'extractif.

**2. La relecture-changement-de-lecteur ne s'aiguille pas.**

| politique | exactitude | modèle appelé |
|---|---:|---:|
| extractif seul | 0,286 | 0 |
| modèle seul | **0,381** | 84 |
| règle « refus → modèle » | 0,310 | 9 |

La règle récupère **2 questions sur 9**, en **manque 15** et fait **7 fausses alertes**.

**3. Le déclencheur lexical ne sépare pas** : les vraies questions du pilote partagent **1 à 3 mots** avec leur réponse ; le hors-sujet « trois » en partage **1**. Identique.

\## La faute attrapée : mon seuil R0.6 était trop haut

Le seuil **3,8** que j'avais calibré sur `format-flux.md` (10/10 refusés) **refusait 32 % des paraphrases d'autres documents** et coûtait **6,7 points** (0,269 → 0,202) pour **un** refus gagné sur dix. Ramené à **1,0** : pilote 20/20 (12 justes), hors-sujet 9/10, provenance 20/20, rejeu identique. C'est la leçon de R0.5 payée une troisième fois : **un seuil absolu ne se transporte pas**.

\## État

Commit `b8a1764b`, hook d'état vert, revue verte, porte lecture verte (6/6). La fiche R06 est réécrite autour du changement de modalité ; sa porte « gist » (R21) reste nommée comme non testable.

**La suite** : R11 et R21 sont bloqués par la hiérarchie, que la session **N2** possède. Le prochain item **non bloqué** est **R05 — la tête de balayage**, et sa moitié classique (index de spans : nombres, dates, requête → spans, rappel@10) n'existe pas encore. C'est ce que je prends au prochain round.

### Tour 14 — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases … [1326 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Read the R05 fiche
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/index_spans.py`
- bash — Test the span index
- bash — Measure rappel@10 on both benches
- bash — Add cross-document control and the gate
- bash — Write the R05 spec and report
- bash — Update counters and docs, run checks
- bash — Commit R05

**Synthèse produite :**

⏵ Round 3 : R05 livré — balayage classique 0,984 / 0,702, porte 6/6

**R05 est livré** — l'index de spans que la fiche exige *avant* toute tête, commit `90c751ca`.

\## Le chiffre

| banc | n | rappel@10 | temps |
|---|---:|---:|---:|
| lexical (249 questions) | 249 | **0,984** | 0,1 ms |
| paraphrases (84 questions) | 84 | **0,702** | 0,1 ms |

**La porte 1 de la fiche est franchie sur le lexical** (≥ 0,95). Sur les paraphrases, 0,702 : c'est le domaine de la tête — et la tête ne paie pas (R0.4, 0,575 contre 0,745). Le chemin classique fait ce qu'il peut, et il le fait en **0,1 ms**.

\## Ce que l'index fait

- **nombres** avec séparateurs et unité (« 3 663 octets », « 24,05 % »), **dates** ISO et françaises ;
- **offsets exacts** dans le flux R0.1 (223 spans vérifiés sur `format-flux.md`) ;
- **classement** par le BM25 du passage porteur, **recherche exacte** d'une valeur (offset direct) ;
- **6 contrôles verts** : offsets, rejeu, exact, balayage, terme absent, **terme d'un autre document** (le contrôle croisé que la fiche demande).

\## La discipline tenue

- la fiche R05 passe de « spécifiée » à « partielle » : le chemin classique mesuré, la tête **nommée comme non franchie** (même mur que R0.4) ;
- la spec `tete-balayage.md` écrit noir sur blanc ce que le rappel@10 mesure *et ne mesure pas* (le terme de la question est dans le gold par construction — le span index hérite du contrôleur, il ne le dépasse pas) ;
- commit `90c751ca`, hook d'état vert, revue verte, **58 portes** (la nouvelle est verte).

\## La suite

**Brancher le balayage dans le pipeline** : quand la question demande une valeur (« combien », « quel numéro »), `lecture.py` doit pouvoir rendre le **span** (offset exact, précision de la citation) au lieu de la phrase entière — une troisième voie entre l'extractif et le modèle, à 0,1 ms. C'est l'action du contrôleur que la fiche R05 demandait, et c'est mesurable sur le pilote : la valeur est-elle dans le span rendu, et à quel coût.

### Tour 15 — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases … [1326 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Add the span mode to the pipeline
- bash — Compare span vs extractive on both benches and the pilot
- bash — Compute the extractive answer rate on the same questions
- bash — Document the span integration and update state
- bash — Commit the span integration

**Synthèse produite :**

⏵ Round 4 : la voie span entre dans le pipeline — 0,944 contre 0,851, commit a0ff20a1

**Le balayage est branché** : `lecture.py --lecteur span` rend la valeur et l'offset exact, en 0,1 ms.

\## Le chiffre

| voie | questions à valeur (249) | paraphrases (84) | questions mixtes (20) | coût |
|---|---:|---:|---:|---:|
| **span** (top-1) | **0,944** | 0,405 | 3/20 | **0,1 ms** |
| extractif | 0,851 | 0,286 | **12/20** | ~1 ms |
| modèle | — | 0,381 | — | 1,9 s |

**Sur une question à valeur, le span bat l'extractif de 9,3 points** (0,944 contre 0,851) et cite l'octet exact. **Sur une question de sens**, il ne peut pas : 3/20 contre 12/20 — il rend un nombre même quand on demande une définition.

\## La surprise du tableau

Sur les paraphrases, le **span (0,405) fait jeu égal avec le modèle (0,381)** — à 20 000 fois moins cher (0,1 ms contre 1,9 s). Ce n'est pas une victoire du span : c'est le signe que le modèle de 0,5 B n'est pas un bon lecteur de paraphrases, et que le span, qui ne comprend rien, tombe parfois juste en citant un nombre.

\## La règle des trois voies

| la question demande… | la voie | chiffre |
|---|---|---|
| un **nombre, une date** | **span** | 0,944 · 0,1 ms |
| un **sens**, avec les mots du document | **extractif** | 0,851 · ~1 ms |
| un **sens**, en paraphrase | **modèle** | 0,381 · 1,9 s |

La porte du pipeline passe à **7 contrôles** (le span de « 3 663 octets » à l'offset 8036). Commit `a0ff20a1`, hook d'état vert, revue verte.

\## La suite

**Le choix automatique de la voie** : la forme de la question (« combien », « quel numéro », « quelle date ») est un signal **syntaxique**, pas une échelle de scores — le contraire du routeur R0.5 qui a échoué. Un `--auto` qui l'utilise devrait donner 0,944 sur les questions à valeur, 12/20 au pilote, et 0,405 sur les paraphrases, sans jamais appeler le modèle pour rien. C'est mesurable sur les trois jeux, et c'est la dernière pièce qui fait du pipeline un lecteur complet.

### Tour 16 — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases … [1326 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — List the pilot questions to calibrate the classifier
- bash — Add the auto voie classifier and test it
- bash — Measure the auto voie on the three sets
- bash — Inspect where auto and extractive disagree on the pilot
- bash — Document the auto result and update state
- bash — Commit the auto voie result
- bash — Inspect the stale counter line
- bash — Fix the JSON counter and commit

**Synthèse produite :**

⏵ Round 5 : la voie auto est mesurée — elle dépend du corpus, pas de la question

\## Le chiffre

`--lecteur auto` classe la question par sa **forme** (« combien », « quel numéro », « quelle date » → span ; sinon extractif).

| jeu | auto | extractif | écart |
|---|---:|---:|---:|
| lexical (249 questions à valeur) | **0,944** | 0,835 | **+0,109** |
| paraphrases (84, à valeur) | **0,333** | 0,274 | **+0,059** |
| pilote (20, mixte) | 0,450 | **0,600** | **−0,150** |

**Sur un corpus de valeurs, le choix automatique paie** (+11 points). **Sur un corpus mixte, il coûte** (−15 points).

\## Pourquoi — les cinq désaccords du pilote le disent

- **les nombres en mots** : « combien d'invariants ? » attend « **six** » ; le span ne connaît que les chiffres et rend « 2 » ;
- **le classement du span** : « combien de pages R0.1 ? » attend « 51 » ; le span rend « 0.1 », le premier chiffre de la phrase — il hérite du BM25 du **passage**, pas d'un score de **span** ;
- **un artefact de comparaison** : « point 7 » attendu, « 7 » rendu — la valeur est juste, le contrôle est strict.

\## La leçon (la même que R0.5, par un autre chemin)

Le choix de la voie dépend du **corpus**, pas seulement de la forme de la question. Un classifieur syntaxique ne peut pas savoir que « combien d'invariants » attend un mot. **Le défaut du pipeline reste l'extractif** ; `--auto` s'active pour un corpus dont on sait qu'il demande des valeurs.

\## État

Commits `63f0f4ea` (l'auto) et `61511b4b` (compteur), hook d'état vert, revue verte, porte du pipeline 7/7. Les fichiers des pairs restent chez eux.

\## La suite

Deux corrections concrètes, nommées :
1. **les spans de nombres en mots** (« cinq », « six », « quatre-vingtième ») — pour que « combien d'invariants ? » trouve « six » ;
2. **un score de span** (la proximité du chiffre aux mots de la question dans la phrase), au lieu du score du passage — pour que « 51 » batte « 0.1 ».

Les deux sont mesurables sur les trois jeux, et la seconde est un **rerank** — le premier endroit où une tête pourrait servir, sur des features explicites et non sur des états.

### Tour 17 — <goal_round> Objective: "Avancer en autonomie sur le programme R (lecteur) pendant plusieurs heures, en plusieurs phases … [1326 caractères tronqués]

*16 appels d'outils.* Actions notables :

- bash — Add word numbers and window scoring, retest
- bash — Sweep the window weight for rappel@1 and @10
- bash — Revert the rerank, keep word numbers, remeasure
- bash — Revert word spans and confirm the original numbers
- bash — Document the rejected experiments
- bash — Commit the two rejected experiments
- get_goal
- bash — Gather the completion evidence
- bash — Remove the drifted question and reverify the bench
- bash — Document the drift and update state
- bash — Inspect the backlog graph errors
- bash — Read the allowed statuses
- bash — Fix my statuses and counters, check the graph
- bash — Commit the bench repair and status fixes
- … et 2 autres

**Synthèse produite :**

**L'objectif est atteint et clôturé.** Voici le bilan de ce run autonome.

\## Ce que l'objectif demandait, et ce qui est livré

**1. Élargir le banc des paraphrases à ≥ 80 questions vérifiées** ✅ — de **19 à 84** (puis **83** après une dérive de document), recouvrement question↔gold **0,17 en moyenne** (max 0,43, seuil 0,5), vérifié par le constructeur : `python3 tools/banc_durci.py --verifie` → **0 problème**.

**2. Rejouer R0.3, R0.4, R0.5 dessus** ✅ :

| mesure | résultat |
|---|---|
| R0.3 — modèle vs extractif | **0,375 contre 0,269** (l'écart tombe de +42 à +11 points quand le banc quadruple) |
| R0.4 — tête vs BM25 | v1 0,601/0,836 · v2 0,448/0,811 · **v3 0,575/0,745** — ne bat jamais BM25 ; contrôle 0,548 |
| R0.5 — routeur | signal **AUC 0,826** ; transfert z-score 0,802/0,321 — ne bat pas le choix fixe |
| R06 — relecture | **0/249 et 0/84** de gain à relire plus ; le déclencheur récupère 2/9, en manque 15 |
| R0.6 — pipeline | **12/20** au pilote, **9/10** refusés, modèle **7/8** sur paraphrases, porte **7/7** |
| R05 — balayage | **0,984** de rappel@10 (lexical), **0,711** (paraphrases), **0,1 ms** ; dans le pipeline **0,944** sur les valeurs contre 0,851 |

**3. Le négatif nommé, la ligne suivante enchaînée** ✅ — la tête reste négative → blocage nommé (données/encodeur), puis **le pipeline de lecture (R0.6)** et **R05** livrés, chacun mesuré, écrit, committé.

\## Les livrables concrets

- **Fiches** : `reports/rapport-r03-banc-durci.md`, `rapport-r04-tete-survol.md`, `rapport-r05-balayage.md`, `rapport-r06-pipeline.md`, `rapport-r06-relecture.md`, `rapport-r07-routeur.md`, plus les JSON bruts.
- **Code** : `tools/banc_durci.py` (le banc), `tools/tete_survol.py`, `tools/routeur.py`, `tools/index_spans.py`, `tools/lecture.py` (le pipeline), `tools/porte-{lecture,balayage}.sh`.
- **Specs** : `docs/implantation/pipeline-lecture.md`, `tete-balayage.md`.
- **État** : fiches R03/R04/R05/R06/R07, roadmap, `en-cours`, INDEX à jour.
- **Commits** (git add explicite, jamais `-A`) : `3328e0ec`, `8c2179fd`, `b8a1764b`, `90c751ca`, `a0ff20a1`, `63f0f4ea`, `33a11db0`, `96d9d3bb`.

\## La vérification

Revue de documentation **verte**, portes **document, lecteur, lecture, balayage et état vertes**, banc **vérifié 0 problème**, arbre propre de mes changements (seuls les fichiers des pairs restent modifiés/non suivis), hook d'état passé à chaque commit de fait.

\## Trois choses que j'ai attrapées en route — et qu'il faut savoir

1. **Mon seuil R0.6 était faux** 
… [1134 caractères tronqués]

### Tour 18 — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h

*37 appels d'outils.* Actions notables :

- create_goal
- bash — Inventory the bench corpus documents
- bash — Freeze the corpus and verify it
- bash — Run the freezer with the correct name
- bash — Repoint builders to the frozen corpus and regenerate
- bash — Re-run the extractive benches on the frozen corpus
- bash — Re-run the model benches on the frozen corpus
- bash — Re-extract the head states on the frozen corpus
- bash — Write the frozen corpus spec and update the drift note
- bash — Write the frozen corpus report and add the nav link
- bash — Update state and counters
- bash — Wait for the model and head jobs
- bash — Check job progress
- bash — Identify running measurement processes
- … et 23 autres

**Synthèse produite :**

**L'objectif est atteint et clôturé.** Voici le bilan.

\## Phase 1 — Le corpus gelé ✅ (`981e4bbf`)

La dérive qui avait coûté deux questions au banc est **close** :

- **30 documents figés** (1,4 Mo) dans `tools/tests/documents/corpus/`, manifeste **source → copie + sha256** ;
- `tools/corpus_gele.py --fige` **idempotent** (j'ai attrapé ma propre fuite : la première version recopiait les sources modifiées par les pairs — le gel changeait dans le dos des bancs) ;
- `--verifie` : **0 problème** ; les constructeurs lisent la copie ; le banc porte la copie **et** la source ;
- bancs régénérés : **248** questions lexicales, **83** paraphrases, **0 problème** des deux côtés ;
- mesures rejouées : extractif **1,000**/0,878 (lexical), 0,609/0,258 (paraphrases) ; modèle 0,228 et 0,369 ; tête 0,540 contre BM25 0,720 — **les conclusions tiennent aux arrondis près**.

\## Phase 2 — La cascade des lecteurs ✅ (`53fec194`)

La relecture morte (relire plus = 0/249) devient un **changement de modalité** : `--lecteur cascade` = span/extractif à l'étage 1, modèle à l'étage 2 **seulement si l'étage 1 refuse**.

| jeu | cascade | sans modèle | appels |
|---|---:|---:|---:|
| lexical (248) | **0,976** | 0,976 | 0 |
| paraphrases (83) | **0,325** | 0,313 | 9 |
| pilote (20) | 0,450 | 0,450 | 0 |

La cascade **ne dégrade jamais** et paie le modèle au bon moment — mais son économie est mauvaise (9 appels, 18 s, pour une question). Le verrou est **le déclencheur**, pas la cascade.

\## Phase 3 — La consolidation ✅ (`11713f7c`)

- **[Le programme R en une page](docs/pilotage/programme-r.md)** : ce qui tient (5 briques mesurées), ce qui ne tient pas (4 tentatives avec leur raison), et **trois lois** — le corpus décide du lecteur ; un signal qui prédit n'est pas une règle qui décide ; pour une valeur, rendre le span bat générer ;
- le **récit du jour** dans le journal (session `8156fdcb`), le manifeste daté correctement (29/10, pas 30) ;
- le **graphe du backlog est cohérent** : les pairs ont corrigé leurs statuts, je n'ai touché aucune de leurs fiches.

\## Vérification finale

Revue **verte** (307 fiches, 379 JSON, 108 docs, 58 portes) · corpus **0 problème** · bancs **0 problème** (248 + 83) · graphe **cohérent** · portes **lecture, balayage et état vertes** · hook d'état passé à chaque commit · arbre propre de mes changements.

\## Ce qu'il faut regarder ensuite

- **Le déclencheur de la cascade** est le verrou unique de R04, R06 et de la relecture : un signal **sans échelle** (accord
… [326 caractères tronqués]

### Tour 19 — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h

*14 appels d'outils.* Actions notables :

- create_goal
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/declencheur.py`
- bash — Run the trigger analysis
- bash — Refine the trigger analysis per bench
- bash — Write the trigger report
- bash — Add the confidence trigger to the cascade
- bash — Out-of-sample measurement of the confidence cascade
- bash — Write the confidence cascade report and update docs
- bash — Fix counters and run checks
- bash — Commit the trigger and confidence cascade
- bash — Complete the narrative and run the final checks
- bash — Check the counters and pending files
- bash — Commit the journal narrative
- update_goal

**Synthèse produite :**

**L'objectif est atteint et clôturé.** Le verrou unique du programme R est levé.

\## Le résultat du cycle : le déclencheur est trouvé

Trois séries d'essais avaient échoué sur le même rocher — un seuil **absolu** sur un score BM25 ne transfère pas. La réponse n'était pas un autre score, c'était un **protocole**.

**Phase 1 — les signaux sans échelle** (`a72cf1dc`) :

| signal | AUC pour « l'extractif a juste » |
|---|---:|
| **couverture** de la réponse | **0,906** |
| **accord** avec le balayage | **0,848** |
| dispersion relative top1-top2 | 0,752 |
| stabilité sous retrait d'un mot | 0,500 (inutile, mesuré) |

Le déclencheur combiné **transfère en classement** : AUC **1,000** sur le lexical, **0,891** sur les paraphrases. Un seuil transféré à l'aveugle échoue (0,636 / 0,373) — mais un seuil **calibré sur une moitié du corpus, testé sur l'autre** :

| corpus | test : cascade | fixe extractif | fixe modèle | **oracle** | appels modèle |
|---|---:|---:|---:|---:|---:|
| lexical | **0,911** | 0,870 | 0,260 | **0,911** | 15 / 123 |
| paraphrases | **0,415** | 0,268 | 0,366 | **0,415** | 35 / 41 |

**La cascade à confiance calibrée égale l'oracle sur les deux corpus, hors échantillon** — +4,1 et +4,9 points sur le meilleur choix fixe, en payant le modèle là où il faut (12 % des questions lexicales, 85 % des paraphrases).

**Phase 2 — le pipeline** : `lecture.py --cascade --seuil-confiance S` (confiance = 0,5 × couverture + 0,3 × accord + 0,2 × dispersion), autotest 7/7.

**Phase 3 — la consolidation** : la synthèse [`programme-r.md`](docs/pilotage/programme-r.md) passe le déclencheur de « échec » à « levé » ; la fiche R06 raconte les quatre versions (triple négatif → cascade → déclencheur → calibré = oracle) ; le récit du jour (commit `2704947c`) retient la leçon.

\## Vérification

Revue **verte** (309 fiches, 381 JSON, 108 docs, 58 portes) · corpus gelé **0 problème** · bancs **0 problème** (248 + 83) · graphe du backlog **cohérent** · portes **lecture et état vertes** · journal **résolu** · hook d'état passé à chaque commit · arbre propre de mes changements (seuls les fichiers des pairs restent modifiés).

\## Ce qu'il faut savoir pour la suite

- **La calibration exige des golds** : un échantillon du corpus avec les réponses (124 et 42 questions ici). Sans lui, pas de seuil — c'est la contrainte de déploiement, écrite dans la fiche.
- **Les poids de la confiance sont fixés à la main** (0,5/0,3/0,2) : un apprentissage les réglerait mieux, au risque du sur-ap
… [472 caractères tronqués]

### Tour 20 — continue

*17 appels d'outils.* Actions notables :

- create_goal
- bash — Run the model on the 20-question pilot
- bash — Add the calibration learning curve
- bash — Run the calibration learning curve
- bash — Fix the confidence and run the curve
- bash — Fix the keys and run the curve
- bash — Read the pilot model results
- job_output
- bash — Check the pilot model job state
- bash — Wait for the pilot model job
- bash — Read the pilot model numbers
- bash — Write the calibration report and check the journal day
- bash — Fix counters and inspect the new journal day
- bash — Write the journal and update the docs
- … et 3 autres

**Synthèse produite :**

**L'objectif est atteint et clôturé** — commit `733232ff`.

\## Phase 1 — La courbe de calibration

Combien de golds faut-il pour régler le seuil de la cascade ? La courbe le dit :

| k (golds) | lexical | paraphrases |
|---:|---:|---:|
| 5–12 | 0,891 ± 0,034 | 0,350 ± 0,037 |
| 16–24 | 0,899 | 0,393 |
| **25–49** | **0,906 ± 0,007** | **0,399 ± 0,030** |
| 74–124 | 0,908–0,911 | 0,395–0,415 |

**~50 questions suffisent** sur le lexical (0,906 contre 0,911 au maximum), **~25** sur les paraphrases. Le plateau est atteint tôt : la calibration est bon marché.

**Et les poids appris n'ajoutent rien** : identiques sur le lexical, **pires** sur les paraphrases (0,366 contre 0,415) — une logistique sur 25 à 42 exemples sur-apprend. Les poids fixés (0,5 couverture + 0,3 accord + 0,2 dispersion) restent.

\## Phase 2 — Le pilote complété

Le modèle manquait sur les 20 questions du pilote ; il est rejoué (40 appels GPU) : **modèle 0,400 contre extractif 0,600**. Le pilote est un corpus mixte du côté lexical — cohérent avec la loi « le corpus décide du lecteur ».

| jeu | extractif | modèle | oracle |
|---|---:|---:|---:|
| lexical (248) | **0,874** | 0,231 | 0,915 |
| paraphrases (83) | 0,265 | **0,373** | 0,458 |
| pilote (20) | **0,600** | 0,400 | — |

\## Phase 3 — La consolidation

- la fiche **R06** raconte ses cinq versions (triple négatif → cascade → déclencheur → calibré = oracle → courbe) ;
- la **synthèse** `programme-r.md` porte la recette : **50 golds → le seuil → la cascade**, à ~1 point de l'oracle, 12 % d'appels modèle sur un corpus lexical, 85 % sur un corpus de paraphrases ;
- le **récit du jour** (2026-10-30) retient que la calibration est bon marché et que les poids appris sur-apprennent ;
- `en-cours` à jour.

\## Vérification

Revue **verte** (351 fiches, 427 JSON) · corpus gelé **0 problème** · banc **0 problème** · graphe du backlog **cohérent** · portes **lecture et état vertes** · hook d'état passé · arbre propre de mes changements (seuls les fichiers des pairs restent modifiés).

\## Ce qu'il faut savoir pour la suite

- **La valeur binaire** (juste/faux) est le seul critère mesuré ; une réponse partielle compte comme fausse.
- **La courbe est un motif, pas une loi** : deux corpus, 20 tirages par taille, un test fixe.
- **La calibration exige un échantillon annoté** — c'est la contrainte de déploiement, écrite.
- Les pairs travaillent sur R13 (BPE), A8.0, et leurs fichiers n'ont jamais été touchés par mes commits.

Le programme R a désormais une
… [206 caractères tronqués]

### Tour 21 — continue (examine d'abord en-cours.md)

*12 appels d'outils.* Actions notables :

- bash — Read the current state file
- create_goal
- bash — Write and run the calibration tool
- bash — Run the calibration and verify reproducibility
- bash — Wire the calibration file into the pipeline
- bash — Apply the calibration out-of-sample
- bash — Write the publication report and update docs
- bash — Extend the gate with the calibration check
- bash — Update state and journal
- bash — Commit the published calibration
- bash — Final verification of the publication
- update_goal

**Synthèse produite :**

**L'objectif est atteint et clôturé** — commit `b19ab8b7`. J'ai suivi la prochaine action désignée par `en-cours.md` : *publier la cascade à confiance dans le pipeline*.

\## Ce qui est livré

**La politique n'est plus un réglage de séance.** Avant : un seuil tapé à la main (`--seuil-confiance 0.16`), invérifiable. Après : un **fichier daté** que le pipeline lit.

| avant | après |
|---|---|
| seuil tapé à la main | **fichier daté** : banc, empreinte du corpus gelé, n, seuil, taux, poids |
| pas de vérification | `calibrer.py --verifie` : le seuil se recalcule à l'identique |
| pas de test hors échantillon | `calibrer.py --teste` : calibration (paires) appliquée aux impaires |
| réglage local | `lecture.py --cascade --calibration FICHIER` |

\## Le résultat, sur un découpage indépendant de R06 v4

| calibration | n | seuil | test (n) | **cascade** | fixe extractif | fixe modèle | oracle | appels |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lexical | 124 | 0,168 | 123 | **0,894** | 0,837 | 0,228 | **0,894** | 19 |
| paraphrases | 42 | 0,394 | 41 | **0,366** | 0,317 | 0,341 | 0,439 | 18 |

**La cascade égale l'oracle sur le lexical** et **bat les deux choix fixes** sur les paraphrases — ce n'est donc pas un artefact du découpage de R06 v4 (paires/impaires par index ici, `[::2]` là).

\## La recette de déploiement

1. **~50 questions** du corpus avec leurs golds (la courbe R06 v5) ;
2. `tools/calibrer.py --banc … --part paires --ecrit calibration-<corpus>.json` ;
3. `tools/lecture.py … --lecteur cascade --calibration calibration-<corpus>.json`.

L'**empreinte du corpus gelé** dans le fichier dit à quelle version du corpus le seuil appartient : un corpus re-gelé invalide la calibration, visiblement.

\## Vérification

Porte **lecture verte** (7 contrôles + la reproductibilité des deux calibrations) · revue **verte** (364 fiches, 436 JSON) · corpus gelé **0 problème** · graphe du backlog **cohérent** · porte **état verte** · arbre propre de mes changements (les fichiers des pairs — r13.3, journal — restent chez eux).

\## Ce qu'il faut savoir

- **La calibration exige des golds** (~50 questions annotées) : c'est le coût de la politique, écrit dans la fiche.
- **La marge des paraphrases est mince** : 0,366 contre 0,341 pour le modèle seul, et un oracle à 0,439.
- **L'empreinte ne couvre pas l'extraction** (R0.1) : un changement de `graphe_document.py` changerait les régions sans invalider la calibration — nommé.
- **La prochaine action du programme R n'est plus 
… [168 caractères tronqués]

### Tour 22 — continue (le wbs de en-cours.md n'est probablement pas le meilleur outil pour voir les dépendances et bloquants)

*21 appels d'outils.* Actions notables :

- bash — Read the backlog graph and its sections
- bash — Read the frontier and the priorities
- bash — List the R fiches with statuses and dependencies
- bash — Compare the index statuses with the fiches
- bash — Read the state checker's requirements
- bash — Read the checker's rules and the current chantiers table
- bash — Read the backlog tool's parsing flow
- bash — Read the tool's structure
- bash — Add the index check and see the mismatches
- bash — Read the A8.3 and B10.2bis fiches
- bash — Locate the rows to fix in the index
- bash — Fix the index and re-check the graph
- bash — Read the full chantiers section including the WBS
- bash — Read the WBS tail and check references
- … et 7 autres

**Synthèse produite :**

**Le graphe, pas le WBS — et il avait raison.** La remarque a mis le doigt sur une dérive réelle.

\## Ce que le graphe dit, et que le WBS cachait

La **frontière** (les 11 items réellement non bloqués) : `A2.6, B10.3, B11.10, N2, N3, N4, R04, R05, R07, R13, R44`.

Pour mon programme R : `R04` (négatif mesuré), `R05` (fait), `R07` (partiel), `R13` (une paire), `R44` (P3, « n'ouvre rien »). **Tout le reste de R est bloqué** : `R11` attend `N2`, `R21` attend `R11`, `R31`/`R32`/`R51` attendent `R21`. La chaîne `N2 → R11 → R21 → R31` est le vrai chemin critique, et `N2` appartient à une autre session.

\## Ce que j'ai trouvé en vérifiant

Le backlog **s'écrit deux fois** (la fiche, puis l'index) — et **six statuts avaient divergé** :

| fiche | l'index disait | la fiche dit |
|---|---|---|
| R04 | en cours | partiel |
| **R05** | **spécifiée** | **partiel** (5 versions mesurées !) |
| **R06** | **spécifiée** | **partiel** (5 versions mesurées !) |
| R13 | spécifiée | prête |
| B10.2bis | spécifiée | mesurée |
| A8.3 | *absente de l'index* | mesurée |

Un graphe qui annonce « spécifiée » une fiche mesurée depuis trois versions n'est pas un graphe.

\## Ce qui est corrigé

1. **`verifie_backlog.py` confronte l'index aux fiches** — six écarts trouvés, six corrigés ; désormais un écart est une erreur du graphe (il ne peut plus dormir).
2. **L'état ne recopie plus les statuts** : le WBS (la table d'états + le diagramme PlantUML) est remplacé par la **frontière du graphe** (recalculée), le [schéma des dépendances](docs/schemas/backlog-dependances.svg), et une table qui ne garde que les **bloquants externes** — la seule chose que le graphe ne peut pas dire — et la prochaine action.
3. Les sept chantiers C restent nommés (hors graphe, transférés au journal).

Commit `68590bf0`, revue **verte**, graphe **cohérent**, état **1138 mots** (sous le budget).

\## Ce que ça change pour la suite

La frontière R est **vide de travail actionnable** pour ma session : ce qui reste est soit mesuré, soit bloqué par `N2`. Les prochaines actions honnêtes sont donc :
- **aider la frontière non-R** qui n'appartient à personne (A2.6 ? N3 ? — mais ce sont les fiches des pairs) ;
- ou **attendre le déblocage de N2** (la hiérarchie) pour R11 → R21 → R31, et le dire dans l'état ;
- ou **consolider** : la synthèse du programme R est faite, les fiches sont à jour — il n'y a plus de mesure à faire sans la hiérarchie.

Je propose de **suivre N2** (la session GPU) et de reprendre R11 dès que sa hiéra
… [132 caractères tronqués]

### Tour 23 — ok, pour la suite. en passant, je tiens a avoir une vue graphique des chantiers. le wbs n'indiquait pas les dépendances  … [452 caractères tronqués]

*24 appels d'outils.* Actions notables :

- bash — Read the existing dependency SVG
- bash — Aggregate the chantier-level dependencies and blockers
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/carte_decisions.py`
- bash — Generate the decision map and validate the SVG
- bash — Check the items per lane and depth
- bash — Fix the row heights and regenerate
- bash — Render the SVG to inspect it
- bash — Export the SVG with inkscape
- read_image
- bash — Geometric check of the item boxes
- bash — Identify the overlapping items
- bash — Reference the decision map and run the checks
- bash — Inspect the sessions tool and plans
- bash — Read the plan template and my session's plan
- … et 9 autres

**Synthèse produite :**

Trois choses faites, et la première répond directement à ta remarque.

\## 1. La vue graphique des chantiers — et elle n'est pas un Gantt

**[`docs/schemas/chantiers-decision.svg`](docs/schemas/chantiers-decision.svg)** — quatre couloirs (A, B, N, R), et l'axe vertical n'est **pas le temps** : c'est la **profondeur de dépendance**. En haut, la **frontière** (11 items, encadrés en vert) ; en dessous, ce qu'elle débloque ; en bas, les **sources de blocage nommées** : Colab, FPGA, VRAM, corpus. Les arêtes rouges pointillées traversent les couloirs (`R11→N2`, `R52→B10.3`), le chemin critique est encadré en rouge (`R01→R02→R03→R31→R32→R51`).

Elle se lit de haut en bas comme un **ordre de travail**, jamais comme un calendrier. 38 items, 4 couloirs, 0 chevauchement involontaire, SVG valide et référencé. Régénération : `python3 tools/carte_decisions.py --svg …`.

C'est la réponse aux trois manques que tu nommes : le WBS ne montrait ni dépendances ni sources ; le Gantt étalait en jours ; le graphe d'items était trop dense pour décider vite.

\## 2. L'arrimage écran ↔ session

Trois supports doivent porter la **même identité**, au même endroit :

| support | où | forme |
|---|---|---|
| `en-cours` | le titre du bloc | `### Session \`8156fdcb\` — R0.1–R0.5 (lecteur)` |
| le plan | `journal/sessions/<id>/plan.md` | le champ `Session` |
| **le TUI** | **le premier item** de la liste de tâches | `Session <id> — <rôle>` |

**Je viens d'adopter la convention** : mon écran porte maintenant `Session 8156fdcb — R (lecteur) · carte de décision + arrimage écran` comme premier item — tu peux le vérifier dans la liste de tâches de cette session. La règle et la limite sont écrites dans **`continuite.md` § 4** : `tools/sessions.py --check` contrôle plans ↔ en-cours, mais le TUI n'est pas lisible depuis le dépôt — c'est une convention, et c'est pour ça qu'elle est écrite.

\## 3. Ce qui reste à faire de méthode

- **Les autres sessions doivent adopter la même première ligne** dans leur TUI (sinon tu verras toujours des écrans sans identité) — je ne peux pas écrire dans leur liste de tâches.
- Un **contrôle plus dur** serait possible si le TUI persistait sa liste quelque part ; en attendant, la convention est la seule garantie.
- La carte se régénère à chaque **recalcul du graphe** (`verifie_backlog.py`) : elle vieillit avec lui, pas avec une date.

Commit `b33b56ab`, revue verte, schémas verts, graphe cohérent.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_backlog.py` | 1 | 23 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R01-graphe-document.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R02-controleur-lecture.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R04-tete-survol.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R05-tete-balayage.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R06-tete-relecture.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R11-contexte-hierarchique.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R12-curriculum-contexte.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R13-tokenisation-bpe.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R21-memoire-travail-gist.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R22-memoire-episodique.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R31-restitution-sft.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R32-citations-provenance.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R51-lecture-croisee.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R52-multilingue-decodeur.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/N0.3b-parite-ppl.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/N4-usage-sft.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/B10.3-raisonnement-z.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/B11.10-cartes-ambiguites.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/B1.5-prose-scientifique.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/A3.4-colab.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/A5.4-fpga.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/A6.2-moe-local.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/dependances.md` | 1 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/index.md` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 14 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 9 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/N2-distillation.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document.py` | 1 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/document-graph.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document_pdf.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r01-graphe-document.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/lecteur_controleur.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/documents/bench-pilote.json` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_lecture.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/lecteur-controleur.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/banc-lecture.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r02-controleur.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/lecteur_modele.py` | 3 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r03-lecteur-modele.md` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_complet.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r03-banc-complet.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_durci.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r03-banc-durci.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tete_survol.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r04-tete-survol.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R07-routeur-extractif-generatif.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/routeur.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r07-routeur.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/lecture.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/pipeline-lecture.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-lecture.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r06-pipeline.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r06-relecture.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/index_spans.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/declencheur.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/carte_decisions.py` | 1 | 0 |

### Sous-agents lancés

- tour 2 — Parseur HTML de document
- tour 2 — Parseur PDF de document

### Commandes exécutées (échantillon)

- **T1** List backlog directory and line counts
- **T1** Read the four blocked compact fiches
- **T1** Check git status, recent commits, implantation docs
- **T1** List pilotage and schemas dirs, read illustration rules
- **T1** Inspect schema verifier and doc review tooling
- **T1** List tools and read manques.md
- **T1** Read schemas README and revue structure
- **T1** Grep for orphan identifiers across pilotage docs
- **T1** Read revue_documentation main checks
- **T1** Check date, last commit, doc review baseline, docs count
- **T1** Inspect gate runner and a sample gate
- **T1** Check document size budgets and table gate
- **T1** Check for SVG rasterizers and docwatch
- **T1** Run backlog graph checker on current state
- **T1** Re-run backlog graph checker
- **T1** Run checker with SVG output and schema verifier
- **T1** Rasterize SVG for visual check
- **T1** Inspect dessiner function after edit
- **T1** Regenerate SVG and check structure
- **T1** Show tail of dessiner
- **T1** Regenerate and validate SVG, rasterize
- **T1** Geometric validation of SVG layout
- **T1** Re-validate edge routing
- **T1** Check box overlaps and bounds
- **T1** Locate end of drawing function
- **T1** Regenerate with legend and re-validate
- **T1** Read size/cohesion rules
- **T1** Generate dependency tables from fiches
- **T1** Re-run checker and inspect constraint column
- **T1** Splice generated tables into graph doc
- **T1** Run backlog, schema, table, state checks
- **T1** Re-run backlog checker and doc review
- **T1** Check context budget and read middle of graph doc
- **T1** Show the size budget violation
- **T1** Show modified files
- **T1** Inspect untracked journal file
- **T1** Check commit message style
- **T1** Commit graph, tool and dependency fixes
- **T1** Inspect git hooks
- **T1** Check which hook step is running
- … et 520 autres

## 4. Mesures et résultats marquants

- **T1** `| **M5** | **décodage spéculatif** — aucune ligne de moteur | brouillon générique ×0,70 · paire alignée ×1,09 · brouillon minuscule **×1,52** | la latence du décodage ; mais le cahier des charges est `
- **T1** `| **M6** | **le moteur n'apprend pas** — il applique, mesure, sauve et recharge une matrice additive, mais ne touche jamais aux poids | notre seule règle locale est **réfutée** (transfert nul, −5 à −1`
- **T1** `| **M9** | ~~aucun instrument ne mesure le coût de la SPARSITÉ DES POIDS~~ **LIVRÉ le 11/10, les deux moitiés** | (1) `tools/occupation_poids.py` lit l'occupation d'un GGUF par genre ; (2) le **moteur`
- **T1** `**8,6 Mo/s sur disque dur** contre 243 Mo/s en séquentiel (÷28) — un préchargement`
- **T1** `**29 Mo/s** au hasard sur l'array, **1 126 Mo/s** sur un motif d'experts. Ce qui paie n'est pas`
- **T1** ``madvise` — sur une plage entière il rend **×1,06**, et sa granularité **ne change rien** dans le`
- **T1** `parallèle ramène le temps de **calcul** d'une passe de **7,70 s à 3,65 s** (−53 %) et la passe de`
- **T1** `utile de 75 %.`
- **T1** `docs/pilotage/manques.md:73:| **N5** | **mémoire d'un signal injecté** — le modèle n'en a aucune, **et il ne l'APPREND pas** | sonde linéaire **et** non linéaire sur l'état de sortie : le signal **cou`
- **T1** `docs/pilotage/backlog/B12.10-pipeline-m1-m4-m8.md:9:Le pipeline rend 528/528 et 96,33 % de complétion, mais M4 ne généralise pas et M8 est la marginale. Le chiffre est tautologique : il faut une mesur`
- **T1** `# 1 951 octets à 97,7 % d'activité, 1 096 à 50 % — mesuré). Un contrôle au démarrage ne`
- **T1** `| **N1 — `drave-n0`** | ✅ 11,47 M, 6 blocs ; PPL 3,465 avec pont (4,080 sans) ; têtes 57,6/61,6/62,1 % ; réflexe −24,05 % ; pensée λ = 0,709 ; cache 19,25× | [`roadmap-native-2026-10-29.md`](../../doc`
- **T1** `| **B5/B6** | ✅ jeux : 112 items, 100 % au niveau 4, perft, 3/3 mats | [`rapport-jeux-symboliques.md`](../../reports/rapport-jeux-symboliques.md) |`
- **T1** `| **B7/B8** | ✅ 71 langues, 449/449, livre 10/10, go 9×9 10/10 | [`rapport-langues-maitres.md`](../../reports/rapport-langues-maitres.md) |`
- **T1** `| **C3.2** | ✅ 9 familles, 7/9 > 30 %, moyenne 69,5 % | [`rapport-familles-9.md`](../../reports/rapport-familles-9.md) |`
- **T1** `[still running after 60000ms; moved to background job bash-3523]`
- **T1** `94:- **R0** : **90 %** à **30 %** du coût ? → **R0.3** (banc) tranche.`
- **T2** `LE PROBLÈME (5ᵉ leçon de la nuit ✓✗) : le « contenu » du modèle 512 valait **104,3 %** à longueur 64 et`
- **T2** `**87,0 %** à longueur 128 ✗✓ — un chiffre qui dépend des réglages n'est pas une mesure, c'est un réglage ✓.`
- **T2** `**Résultat attendu** : si l'écrémage/balayage atteint ≥ 90 % de l'intégral à ≤ 30 % du coût sur au moins trois`
- **T2** `- un chiffre sans dispositif (« 73 % ») ;`
- **T2** `> livre 10/10, go 9×9 10/10 contre 3/10, dames 0 défaite, cartes 44,7 % contre 51,0 %). Les **deux rouges**`
- **T2** `> `porte-pont` **+2,81 % / +25,35 %**, `porte-coupe` **+0,52 % → +17,09 %**, `porte-gain` **29,0206 →`
- **T2** `> 1297,5437**, `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**, `porte-greffe` **branchée**,`
- **T2** `[still running after 60000ms; moved to background job bash-3687]`
- **T2** `95:- **R0** : **90 %** à **30 %** du coût ? → **R0.3** (banc) tranche.`
- **T3** `budget 100% · coût 7954/10441 octets · 65 passages · arrêt « score marginal trop bas »`
- **T3** `budget 30% · coût 3129/10441 octets · 34 passages · arrêt « score marginal trop bas »`
- **T3** `budget 10% · coût 1030/10441 octets · 23 passages · arrêt « section trop chère pour le budget restant »`
- **T3** `50:99,9997 % des cas (22 échappements sur 8 790 000 mesurés). Trois octets par`
- **T3** `66:| trace dense, 512 jetons | 66 370 408 o | **45 079 930 o (−32,1 %)** |`
- **T3** `153:Le mode dense coûte **3 663 octets par flux** (79 d'en-tête + 896 × 4) pour`
- **T3** `trace creuse (39,9 % d'activité) : 6,04 et 3,04 — deux centièmes de plus, parce que`
- **T3** `99,9997 % des cas (22 échappements sur 8 790 000 mesurés). Trois octets par`
- **T3** `Le mode dense coûte **3 663 octets par flux** (79 d'en-tête + 896 × 4) pour`
- **T3** `❌ code : récupération 0.750 < 0.9 à 30 %`
- **T3** `❌ juridique : récupération 0.750 < 0.9 à 30 %`
- **T3** `❌ tableau : récupération 0.750 < 0.9 à 30 %`
- **T3** `❌ technique : récupération 0.500 < 0.9 à 30 %`
- **T3** `❌ technique : F1 0.079 < 0.9 × 0.534 (intégrale)`
- **T3** `❌ code : F1 0.272 < 0.9 × 0.522 (intégrale)`
- **T3** `❌ tableau : F1 0.211 < 0.9 × 0.398 (intégrale)`
- **T3** `❌ technique : récupération 0.750 < 0.9 à 30 %`
- **T3** `technique rang  16 score  0.00 best  4.03 lu=False cout   954/10441 · Quelle est la taille du champ magique ?`
- **T3** `technique rang   0 score  8.96 best  8.96 lu=True  cout  2516/10441 · Combien d'octets coûte le mode dense par flux`
- **T3** `technique rang  10 score  1.99 best  4.21 lu=True  cout  2510/10441 · Quel taux de couverture le mode liste atteint`
- **T3** `technique rang   0 score  7.27 best  7.27 lu=True  cout  2532/10441 · Combien d'octets pèse l'en-tête de liste ?`
- **T3** `prose     rang   4 score  2.38 best  4.20 lu=True  cout   583/7082 · Que désigne le mot « drave » ?`
- **T3** `prose     rang   0 score  5.19 best  5.19 lu=True  cout   689/7082 · Quelle est la thèse du projet ?`
- **T3** `prose     rang   2 score  2.89 best  5.50 lu=True  cout   401/7082 · Combien d'axes la vision a-t-elle ?`
- **T3** `prose     rang   0 score 10.39 best 10.39 lu=True  cout   274/7082 · Que désigne « Stream of logs » ?`
- **T3** `tableau   rang   1 score  4.92 best  6.22 lu=True  cout  2669/19335 · Quel est le meilleur score de perplexité de N`
- **T3** `tableau   rang   2 score  4.38 best  5.51 lu=True  cout  2794/19335 · Quelle porte N2 doit-elle franchir ?`
- **T3** `tableau   rang   9 score  2.07 best  4.47 lu=True  cout  2196/19335 · Quelle ligne d'échelle est suspendue ?`
- **T3** `tableau   rang   1 score  6.53 best  7.42 lu=True  cout  5776/19335 · Combien de pages R0.1 a-t-il découpées ?`
- **T3** `juridique rang   7 score  0.00 best  7.90 lu=False cout   867/3711 · À quelle date la résolution a-t-elle été adop`
- **T3** `juridique rang   7 score  1.93 best  5.40 lu=True  cout  1019/3711 · Quelle session de l'Assemblée générale est co`
- **T3** `juridique rang   9 score  0.00 best  3.62 lu=True  cout   341/3711 · Quel est le numéro de la résolution ?`
- **T3** `juridique rang   0 score 10.43 best 10.43 lu=True  cout   875/3711 · Quel point de l'ordre du jour est traité ?`
- **T3** `code      rang  10 score  0.00 best  3.94 lu=False cout   891/5969 · Quel outil est déclaré dans le manifeste ?`
- **T3** `code      rang   3 score  4.19 best  6.34 lu=True  cout  1441/5969 · Quel type de région porte les séparateurs ?`
- **T3** `code      rang   0 score  5.84 best  5.84 lu=True  cout  1200/5969 · Combien d'invariants le manifeste doit-il res`
- **T3** `code      rang   0 score  5.53 best  5.53 lu=True  cout  1444/5969 · Quel champ identifie le fichier source ?`
- **T3** `❌ code : valeur 0.250 < 0.9 × 0.500 (lecture intégrale)`
- **T3** `❌ tableau : valeur 0.500 < 0.9 × 0.750 (lecture intégrale)`
- **T3** `✅ à 30 % du budget, la lecture contrôlée récupère ≥ 90 % des passages de la`
- **T3** `40:   30 % sur 5 types) ; la suite est **R0.3** — le banc complet, 30 documents et 300 questions.`
- **T3** `161:| **R0.2** | **contrôleur de lecture** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, titres, premières/dernières phrases, BM25/regex) | ✅ **1`
- **T3** `42:- **Prochaine action** : la porte R0.2 — **≥ 90 %** de l'exactitude de la lecture intégrale à **30 %**`
- **T3** `08149617 R0.2 — À 30 % DU BUDGET, LE CONTRÔLEUR RÉCUPÈRE 100 % DES PASSAGES ; LE LECTEUR PLAFONNE À 25–75 %`
- **T3** `docs/pilotage/en-cours.md:26:- **Prochaine action** : **N0.3b** en parallèle ; R0.2 est **mesuré** par `8156fdcb` (récupération 1,000 à 30 %).`
- **T3** `245:| [rapport-r02-controleur.md](rapport-r02-controleur.md) | R0.2 — le contrôleur de lecture : 100 % de récupération à 30 % du budget |`
- **T4** `GGUF ouvert en 31.319339ms — 290 tenseurs`
- **T4** `blk.0.ffn_gate.weight  [4864 × 896]  densité 99.2 %`
- **T4** `dense 8 bits               8.000 b/poids  (   4.36 Mo)`
- **T4** `bitmap + signe             1.992 b/poids  (   1.09 Mo)`
- **T4** `creux k=1 (signe seul)     1.992 b/poids  (   1.09 Mo)`
- **T4** `creux k=4                  4.970 b/poids  (   2.71 Mo)`
- **T4** `creux k=8                  8.939 b/poids  (   4.87 Mo)`
- **T4** `listes signées + écarts    7.975 b/poids  (   4.34 Mo)`
- **T4** `blk.0.ffn_down.weight  [896 × 4864]  densité 99.2 %`
- **T4** `creux k=4                  4.967 b/poids  (   2.71 Mo)`
- **T4** `creux k=8                  8.934 b/poids  (   4.87 Mo)`
- **T4** `listes signées + écarts    7.941 b/poids  (   4.33 Mo)`
- **T4** `blk.0.attn_q.weight  [896 × 896]  densité 99.1 %`
- **T4** `dense 8 bits               8.000 b/poids  (   0.80 Mo)`
- **T4** `bitmap + signe             1.991 b/poids  (   0.20 Mo)`
- **T4** `creux k=1 (signe seul)     1.991 b/poids  (   0.20 Mo)`
- **T4** `creux k=4                  4.964 b/poids  (   0.50 Mo)`
- **T4** `creux k=8                  8.929 b/poids  (   0.90 Mo)`
- **T4** `listes signées + écarts    7.964 b/poids  (   0.80 Mo)`
- **T4** `blk.0.attn_output.weight  [896 × 896]  densité 99.2 %`
- **T4** `bitmap + signe             1.992 b/poids  (   0.20 Mo)`
- **T4** `creux k=1 (signe seul)     1.992 b/poids  (   0.20 Mo)`
- **T4** `creux k=4                  4.968 b/poids  (   0.50 Mo)`
- **T4** `creux k=8                  8.936 b/poids  (   0.90 Mo)`
- **T4** `listes signées + écarts    7.972 b/poids  (   0.80 Mo)`
- **T4** `blk.0.ffn_gate.weight : 4864 entrées × 896 sorties, 4325087 événements`
- **T4** `listes fusionnées 4.89 Mo (8.97 b/poids) | anciennes 4.34 Mo (7.98) | bitmap 1.09 Mo (1.99)`
- **T4** `// tous les cœurs physiques : mesuré, 10 threads rendent 14,3 Go/s contre`
- **T4** `// 22,5 à 20 — le `cpu / 2` laissait 36 % sur la table.`
- **T4** `généré  : 12 tokens en 0.391 s  (30.68 tok/s)`
- **T4** `[tete] densite de l'entree : 93.5 % de coordonnees vivantes sur 12 jetons`
- **T4** `[tete] -> un stockage par COLONNES ne lirait que ces coordonnees : 93.5 % de la matrice au lieu de 100 %`
- **T4** `prompt  : 4 tokens en 3.420 s  (1.2 tok/s, TTFT 854.9 ms)`
- **T4** `généré  : 12 tokens en 0.459 s  (26.16 tok/s)`
- **T4** `Contexte : Le mode dense coûte 3 663 octets par flux (79 d'en-tête + 896 × 4) pour Qwen2.5-0.5B. Le mode liste coûte 79 + 4 × le nombre d'actifs.`
- **T4** `stephane 3535486 1588  0.6 11353956 909348 ?     Rl   12:44   1:07 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave /home/stephane/Data13TB/stephane/GitHub/Qtrinet/model`
- **T4** `controlee_0.30 → 1,5 ko / jeton = 1,5 ko / 16 = 0,09`
- **T5** `gold rang: 4 score: 2.38 best: 4.2`
- **T5** `0, Quadro RTX 5000, 0 %, 4 MiB, 16384 MiB`
- **T5** `1, Quadro RTX 5000, 0 %, 244 MiB, 16384 MiB`
- **T5** `stephane  1898%   0.7% /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/rele`
- **T5** `stephane  1883%   0.7% /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/rele`
- **T5** `stephane   200%   0.0% ps aux --sort=-%cpu`
- **T5** `stephane  38.4%   0.0% bash -c nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,`
- **T5** `stephane  36.2%   1.0% node /home/stephane/.local/share/../bin/dsh --profile dsh-tui`
- **T5** `1897% /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave`
- **T5** `1896% /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave`
- **T5** `200% ps aux --sort=-%cpu`
- … (tronqué)

## 5. Erreurs rencontrées

18 sorties en erreur ou divergentes. Les premières :

- **T1** : === GRAPHE DU BACKLOG ===   fiches 29 · lignes sans fiche 8 · arêtes dures 40 · plafonds 4   profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51   frontière (12) : A2.6, A3.2, A8.0, B10.2bis, B11.10, B12
- **T1** : [stderr] fatal: cannot lock ref 'HEAD': is at a7dd847328e12b633a2e66752aaf0c39e77764d3 but expected 9e569aec9f17c9114af80d6da7f618c0964a3692 [exit code: 128]
- **T2** : A_RES_80_10-en.pdf                       3 A_RES_80_10-es.pdf                       3 A_RES_80_10-fr.pdf                       3 A_RES_80_10-ru.pdf                       3 A_RES_80_10-zh.pdf          
- **T2** : ls: cannot access 'tools/graphe_document_pdf.py': No such file or directory ls: cannot access 'tools/graphe_document_pdf.py': No such file or directory [exit code: 2]
- **T4** : -rwxr-xr-x. 2 stephane stephane 3140664 29 oct 04:50 drave-core/target/release/drave -rw-r--r--. 1 stephane stephane 352972352 25 sep 17:13 models/Qwen2.5-0.5B-Q4_0.gguf -rw-r--r--. 1 stephane stephan
- **T4** : thread 'main' (3530114) panicked at src/main.rs:400:35: ouverture du GGUF: Os { code: 2, kind: NotFound, message: "No such file or directory" } note: run with `RUST_BACKTRACE=1` environment variable t
- **T4** : stephane 3534831  0.7  0.0   7692  4092 ?        Ss   12:43   0:00 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/banc_lecture.py --lecteur modele --json reports/r03-lecte
- **T4** : jeu 29 oct 2026 12:44:46 EDT     PID     ELAPSED     TIME 3534838       00:59 00:00:00     PID     ELAPSED [exit code: 1]
- **T6** : corpus latin + option --sans-hasard 300 questions · 30 documents   prose      docs/theorie/vision.md                               10 questions ❌ docs/methode/portes.md : la valeur est dans la questio
- **T6** : [stderr] Traceback (most recent call last):   File "<stdin>", line 2, in <module> FileNotFoundError: [Errno 2] No such file or directory: 'reports/r03-banc-modele.json' [exit code: 1]
- **T8** : "--entree" "--entree-canal" "--entree-gain" "--entree-jeton" "--entree-memoire" "--etat-fin" "--etat-pos" "--etat-sortie" "--sortie" "--sortie-memoire" "--trace-couches" "--trace-flux" === usage de et
- **T8** : thread 'main' (3729307) panicked at src/main.rs:1246:21: --couches attend `a:b` (reçu « 0-3 ») note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace timeout: the monitored comm
- **T11** : 5 reformulées écrit : tools/tests/documents/bench-durci.json ❌ recouvrement 0.60 ≥ 0.5 : Quand l'ancien service de documentation a-t-il été supprimé  84 questions · recouvrement moyen 0.17 (max 0.60) 
- **T18** : [stderr] python3: can't open file '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/fige_corpus.py': [Errno 2] No such file or directory [exit code: 2]
- **T18** : jeu 29 oct 2026 17:24:30 EDT 65939 15:57 reports/r03-banc-durci-modele.json 202359 17:21 reports/r03-banc-modele.json 3650823 17:22 0 [exit code: 1]

## 6. Commits

- DOCS — GRAPHE DES DÉPENDANCES DU BACKLOG (40 ARÊTES DURES, 4 PLAFONDS), 7 DÉFAUTS CORRIGÉS, VÉRIFIÉ PAR tools/verifie_backlog.py" && git log --oneline -1 && git
- ps aux | grep -E "session_report|archive_sessions|journal_auto|git commit" | grep -v grep | head
- PILOTAGE — QUATRE ARBITRAGES RENDUS : N2 PORTE LA HIÉRARCHIE, SFT PARTAGÉ N4/R31, N5 GELÉ, R0 EN ORDRE STRICT" -- docs/pilotage/backlog/dependances.md docs/sche
- PILOTAGE — QUATRE ARBITRAGES RENDUS : N2 PORTE LA HIÉRARCHIE, SFT PARTAGÉ N4/R31, N5 GELÉ, R0 EN ORDRE STRICT" && git log --oneline -1 && git status --short | w
- ÉTAT — R0 EN ORDRE STRICT, N2 PORTE LA HIÉRARCHIE, N5 GELÉ, PRIORITÉS ARRÊTÉES" && git log --oneline -4 && git status --short | wc -l
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 755 tools/graphe_document*.py tools/porte-document.sh && chmod 644 tools/tests/documents/html/*.html
- ÉTAT — R0.2 RÉSERVÉ À 8156FDBC (CONTRÔLEUR + BANC PILOTE), R0.1 LIVRÉ, N2 PORTE LA HIÉRARCHIE" && git log --oneline -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md"); t = p.read_text(encoding="u
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/banc_lecture.py --json /tmp/r02-a.json >/dev/null && python3 tools/banc_lecture.py --json /t
- ÉTAT — R0.3 RÉSERVÉ À 8156FDBC : LECTEUR MODÈLE ET BANC COMPLET" && git log --oneline -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 755 tools/lecteur_modele.py && git add -A docs/pilotage docs/implantation reports tools && git commi
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A docs/pilotage docs/implantation reports tools && git commit -q -F - <<'EOF' R0.3 — LE LECTEUR P
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 755 tools/banc_complet.py && git add -A docs/pilotage docs/implantation reports tools && git commit 
- ÉTAT — LISTE DES FICHIERS RÉSERVÉS NETTOYÉE (R0.3 CLOS)" && git log --oneline -1 && git status --short | wc -l
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -q -F - <<'EOF' R0.3 DURCI — 19 PARAPHRASES : LE LEXIQUE TOMBE À 0,30, LE MODÈLE PREND LA TÊTE 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/backlog/R04-tete-survol.md docs/p
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -q -F - -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/backlog/R04-tete-su
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-r04-tete-survol.md reports/r04-tete-survol.json tools/tete_survol.py && git commit
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 12); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 12); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("reports/rapport-r07-routeur.md"); t = p.read_text(encodi
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 12); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 12); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 12); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 12); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 12); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md"); t = p.read_text(encoding="u
- ÉTAT — COMPTEUR JSON ALIGNÉ (370)" && git log --oneline -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 12); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib, re p = pathlib.Path("docs/pilotage/en-cours.md"); t = p.read_text(encodin
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 20; for i in $(seq 1 18); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lo
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 18); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md"); t = p.read_text(encoding="u
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 18); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 18); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 18); do [ -e .git/index.lock ] && sleep 5 || break; done; git commit -q -F - -- journal/2
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 18); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib, re p = pathlib.Path("docs/pilotage/en-cours.md"); t = p.read_text(encodin
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 18); do [ -e .git/index.lock ] && sleep 5 || break; done; if [ -e .git/index.lock ]; then
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("journal/2026-10-30/README.md"); t = p.read_text(encoding


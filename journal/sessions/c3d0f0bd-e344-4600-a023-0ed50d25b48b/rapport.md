# Session c3d0f0bd — Chantier inactif à examiner

> **Journaux :** [le jour](../../2026-10-29/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `c3d0f0bd-e344-4600-a023-0ed50d25b48b` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-29 14:37 |
| Durée | 18.7 h |
| Tours | 5 |
| Messages | 561 |
| Appels d'outils | 551 |
| Fichiers touchés | 26 |
| Commandes | 485 |
| Sous-agents | 0 |
| Commits | 32 |
| Compactages de contexte | 1 |

## Objectifs déclarés

- **create** — Faire avancer la roadmap Drave en autonomie pendant plus de 3 h, par cycles mesurés : à chaque round, prendre la ligne la plus utile non bloquée (R4.2 bloc code, puis R0.4/R0.5 durcis, R2.1 gist, N3, A2.6…), produire un résultat avec contrôle négatif, écrire la fiche dans reports/, la spec dans docs
… [148 caractères tronqués]
- **complete** — Faire avancer la roadmap Drave en autonomie pendant plus de 3 h, par cycles mesurés : à chaque round, prendre la ligne la plus utile non bloquée (R4.2 bloc code, puis R0.4/R0.5 durcis, R2.1 gist, N3, A2.6…), produire un résultat avec contrôle négatif, écrire la fiche dans reports/, la spec dans docs
… [148 caractères tronqués]
- **create** — Programme B — débloquer la restitution : après B10.2bis (attention croisée négative), tester les leviers nommés un à un (corpus plus grand, capacité, objectif de décodage) sur le protocole sémantique, avec 3 graines et le même contrôle de plancher chrF, puis B10.3 si le plancher tombe. Chaque round 
… [30 caractères tronqués]
- **complete** — Programme B — débloquer la restitution : après B10.2bis (attention croisée négative), tester les leviers nommés un à un (corpus plus grand, capacité, objectif de décodage) sur le protocole sémantique, avec 3 graines et le même contrôle de plancher chrF, puis B10.3 si le plancher tombe. Chaque round 
… [30 caractères tronqués]
- **create** — Programme A — le transport et l'ordonnanceur : expliquer le défaut mesuré (le lot change la PPL : 61,9920 à lot 1 contre 60,8135 à lot ≥ 2, en f32), le corriger si c'est un défaut de calcul, puis avancer A2.6 (experts et tête dans la règle choisir) et épingler le régime 1 % si l'effet est expliqué. 
… [43 caractères tronqués]
- **complete** — Programme A — le transport et l'ordonnanceur : expliquer le défaut mesuré (le lot change la PPL : 61,9920 à lot 1 contre 60,8135 à lot ≥ 2, en f32), le corriger si c'est un défaut de calcul, puis avancer A2.6 (experts et tête dans la règle choisir) et épingler le régime 1 % si l'effet est expliqué. 
… [43 caractères tronqués]
- **create** — Programme portes — la passe complète du 2026-10-29 : lancer les 58 portes, lire le registre par `awk '$2 != 0'` (jamais les marqueurs), comparer aux rouges tolérées de references-non-regression.md, corriger toute rouge non tolérée, puis mettre à jour references-non-regression.md (durée, compte, verd
… [105 caractères tronqués]
- **complete** — Programme portes — la passe complète du 2026-10-29 : lancer les 58 portes, lire le registre par `awk '$2 != 0'` (jamais les marqueurs), comparer aux rouges tolérées de references-non-regression.md, corriger toute rouge non tolérée, puis mettre à jour references-non-regression.md (durée, compte, verd
… [105 caractères tronqués]
- **create** — Programme B — l'objectif de décodage : après quatre leviers négatifs (attention, pas, corpus, capacité), construire un décodeur au niveau du MOT conditionné sur le même z gelé (UDHR, 24/6, 3 graines) et le comparer au décodeur byte-level (chrF 11,1 contre un plancher de 38,5). Si le chrF monte, l'ob
… [85 caractères tronqués]
- **complete** — Programme B — l'objectif de décodage : après quatre leviers négatifs (attention, pas, corpus, capacité), construire un décodeur au niveau du MOT conditionné sur le même z gelé (UDHR, 24/6, 3 graines) et le comparer au décodeur byte-level (chrF 11,1 contre un plancher de 38,5). Si le chrF monte, l'ob
… [85 caractères tronqués]
- **create** — Programme B — le verrou `z` : le décodeur mot a levé le décodeur (32,5) mais le `z` ne porte que 2,6 points sur l'UDHR formulaire. Tester le même décodeur mot sur le corpus JW (encodeur JW gelé, corpus non formulaire, 11 langues avec espaces) avec le contrôle `z` dur, pour mesurer ce que `z` porte q
… [57 caractères tronqués]
- **complete** — Programme B — le verrou `z` : le décodeur mot a levé le décodeur (32,5) mais le `z` ne porte que 2,6 points sur l'UDHR formulaire. Tester le même décodeur mot sur le corpus JW (encodeur JW gelé, corpus non formulaire, 11 langues avec espaces) avec le contrôle `z` dur, pour mesurer ce que `z` porte q
… [57 caractères tronqués]
- **create** — Programme B — forcer le décodeur à lire `z` : ajouter un terme contrastif (z correct contre z d'une autre unité, marge) à l'entraînement du décodeur mot sur UDHR, 3 graines ; mesurer le chrF ET l'écart au contrôle `z` mélangé (référence : 32,5 avec un écart de 2,6). Si le décodeur lit `z`, B10.3 se 
… [57 caractères tronqués]
- **complete** — Programme B — forcer le décodeur à lire `z` : ajouter un terme contrastif (z correct contre z d'une autre unité, marge) à l'entraînement du décodeur mot sur UDHR, 3 graines ; mesurer le chrF ET l'écart au contrôle `z` mélangé (référence : 32,5 avec un écart de 2,6). Si le décodeur lit `z`, B10.3 se 
… [57 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — trouve un chantier qui mérite mon attention (qui n'est pas actif)

**Tour 2** — as-tu mis ton état de session à jour dans en-cours.md (incluant le svg)?

**Tour 3** — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h

**Tour 4** — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h

**Tour 5** — continue

## 2. Déroulé, étape par étape

### Tour 1 — trouve un chantier qui mérite mon attention (qui n'est pas actif)

*163 appels d'outils.* Actions notables :

- bash — Check sizes of key state docs
- bash — Review recent commits and working tree
- read
- bash — List backlog fiches and R4 references
- bash — Search table handling mentions
- bash — Inspect document graph table handling
- bash — Inspect bench documents and R0.3 results
- bash — Look for existing table parsing code
- bash — Show per-type bench results
- bash — Show aggregates and details shapes
- bash — Show table-type results across benches
- bash — Compare per-type question counts and values
- bash — Find C4 date control references
- bash — Check A8.3 and B11.10 status
- … et 140 autres

**Synthèse produite :**

⏵ R4.1 mesuré, écrit et committé ; état à jour et toutes les vérifications vertes

**R4.1 — le bloc tableaux est fait.** Le chantier dormant est devenu une mesure avec sa porte.

| ce qui est mesuré | résultat |
|---|---|
| corpus | 9 fichiers, **35 tableaux**, 3 formats, **996 cellules** |
| provenance | **802/802** cellules Markdown exactement à leur tranche de source (en-têtes compris) |
| opérations | **8/8** justes (somme, moyenne, min/max, filtre texte/numérique, jointure, en-tête à 2 niveaux) |
| contrôle négatif | le **texte plat échoue 3/3** : somme 120 contre 146 ; cellule `3` contre la rangée entière ; filtre 2 contre 3 |
| refus nommés | rangée irrégulière, en-tête fusionnée, tableau imbriqué, colonne de texte non sommable |
| coût | **25,0 ms / 1 000 cellules**, linéaire (×3,8 pour ×4) — CPU seul |

**Le point qui méritait ton attention est confirmé** : le type « tableau » du banc R0.3 ne mesure pas un tableau. Sur ses 59 questions, 27 ont une rangée aplatie pour gold, et 20 de ces 27 attendent le **numéro de l'étiquette de ligne** (`B11` → « 11 », `R0.4` → « 0.4 »). R4.1 ne relève donc pas le 0,932 — il ajoute la mesure qui manquait : la cellule, l'en-tête, l'opération.

**Fichiers** : `tools/bloc_tableaux.py` · `tools/porte-bloc-tableaux.sh` · `tools/tests/tableaux/` (7 fixtures) · `docs/implantation/bloc-tableaux.md` · [`reports/rapport-r41-bloc-tableaux.md`](reports/rapport-r41-bloc-tableaux.md) · `reports/r41-bloc-tableaux.json`.

**Commits** : `7fb1c8a6` (résultat), `65ab24cf` (état), `52075592` (journal). L'état est passé de 4 004 à **3 993 mots** (lignes périmées N0.3b/B12.10 retirées, blocs compressés) ; `verifie_en_cours`, `revue_documentation`, `verifie_backlog`, `verifie_journal`, `verifier_schemas` et `porte-tableaux` sont verts, ainsi que la nouvelle porte. La passe complète des 52 portes n'a pas été relancée (1 h 40, GPU partagé avec N2) : les 4 portes concernées le sont.

**Suite** : R4.2 — le bloc code (AST, exécution exacte, contrôle « lecture du texte seul »), puis R4.3 (maths) ; la ligne lecteur reprend à R0.4.

### Tour 2 — as-tu mis ton état de session à jour dans en-cours.md (incluant le svg)?

*19 appels d'outils.* Actions notables :

- bash — List schemas and references to the chantiers SVG
- bash — Check which sessions and lines the SVG shows
- read
- bash — Read schema verifier requirements
- bash — Check available SVG rasterisers
- bash — Update the SVG states and sessions
- bash — Render the SVG to PNG for visual check
- read_image
- bash — Query SVG object bounding boxes
- bash — Check text overflow and overlaps
- bash — Check column overflow and modified text boxes
- bash — Check tree, schema and docs before commit
- bash — Wait for the peer commit before committing the SVG
- bash — Commit the updated schema
- … et 5 autres

**Synthèse produite :**

⏵ Vérification terminée : en-cours et le schéma portent bien la session `c3d0f0bd`

**Oui pour `en-cours.md`** (commit `65ab24cf`) : bloc de session `c3d0f0bd` avec les 7 champs, ligne **R4.1** dans « Ce qui est en cours », ligne **R** (R0.1–R0.3 mesurés, R4.1 mesurée, suite R4.2), « Ce qui reste » et question R0 tranchée.

**Non pour le SVG — je viens de le corriger** (commit `1ded6b7f`). Il datait de 14 h 10 et montrait encore `f0969e87` sur B11.10, `8156fdcb` sur R0.3 et R4 « à faire ». Désormais :

| boîte | avant | maintenant |
|---|---|---|
| **R0.3** | en cours, `8156fdcb` | **mesuré** (1,000 à 30 %, 249 questions ; durci 0,30 / 0,717) |
| **R0.4** | à faire, après R0.3 | **négatif / signal** — tête 0,601 contre BM25 0,836 · routeur R0.5 AUC 0,785 · `8156fdcb` |
| **R4** | à faire | **partiel** — **R4.1 ✅ 996 cellules · 802 exactes**, suite R4.2 · lien fiche R41 · **`c3d0f0bd`** |
| **B11.10** | à faire, `f0969e87` | **mesuré** (161/161) |

L'en-tête « Sessions actives », les sous-titres des colonnes et le `<desc>` suivent : `8156fdcb → R0.4/R0.5 · c3d0f0bd → R4.1 · N2-GPU → N2`.

**Vérifié** : `verifier_schemas` ✅ (viewBox, `<title>`, `<desc>`, liens relatifs), XML valide, aucun débordement ni chevauchement de texte (contrôle par les boîtes Inkscape), `revue_documentation` ✅, T0 **3 993** ≤ 4 000. J'ai aussi remis les compteurs à **285 / 352** (commit `6480f6d8`) : le commit A8.0 venait d'ajouter une fiche et un JSON sans mettre l'état à jour.

À noter : l'arbre porte encore les modifications en cours d'un pair (`reports/r07-routeur.json`, `tools/routeur.py`, `tools/tete_survol.py`) — je n'y ai pas touché.

### Tour 3 — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h

*235 appels d'outils.* Actions notables :

- create_goal
- bash — Read the R4.2 backlog fiche
- bash — Inventory Python tools and AST usage
- bash — Measure AST parse coverage on the repo tools
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_code.py`
- bash — Fix interpreter edge cases
- bash — Create code fixtures and snippets
- bash — Run the code block gate
- bash — Add the missing environment and rerun
- bash — Fix the comparator attribute and rerun
- bash — Fix the membership snippet and rerun
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-bloc-code.sh`
- bash — Create the shell gate and write the JSON
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r42-bloc-code.md`
- … et 220 autres

**Synthèse produite :**

⏵ Cycle autonome clos : 3 h 28, 7 rounds mesurés, état et portes au vert

**Bilan de la session autonome** (15 h 37 → 19 h 05, objectif > 3 h tenu). Sept rounds, chacun mesuré, écrit, committé, avec son contrôle négatif.

| round | résultat | chiffre |
|---|---|---|
| **R4.2 — bloc code** | 294/294 fichiers `tools/`, 24/24 extraits, 7/7 refus nommés | texte seul **0/3** · commit `4ccf641f` |
| **R4.3 — bloc maths** | 32/32 formules, 10/10 dérivées, 6/6 équations, oracle sympy 32/32 | surface **0/3** · commit `6415d58b` |
| **Le miroir** (règle 6) | 34/34 tableaux, 296/296 modules, 42/42 formules rendus puis relus | 3 contrôles perdus · commit `d2457e46` |
| **A8.3 — le défaut** | les portes épinglées bougent de −5,9 % à +19,5 % | **opt-in conservé** · commit `a489d9ff` |
| **A8.3b — 3 régimes KV** | f32 / mélange / int8 partout ; mélange meilleur 3/6, int8 pire partout ; topologie au régime 1 % | commits `0c074374`, `8c3ba915` |
| **B10.2bis — le décodeur** | 3 bras × 3 graines : **11,1 / 11,2 / 11,0** contre un plancher de **38,5** ; à 1800 pas : 10,2–11,4 | **négatif net** : ni l'attention ni la durée |
| **Le graphe** | 7 fiches créées (A3.2, A3.3, A8.0, B10.2bis, A8.3, A2.6, N3) | **37 fiches**, 42 arêtes, **1 sans fiche** (N5), 0 cycle |

**Portes** : 4 sous-passes (CPU, GPU, moyenne, divers), **52 passages, 51 vertes, 1 rouge tolérée** (`porte-melange`, structurelle connue). La passe complète (58 portes, ~1 h 40) n'a pas été relancée — c'est écrit dans [`references-non-regression.md`](docs/pilotage/references-non-regression.md).

**État final** : `en-cours` à jour (T0 **4 000** = budget), roadmap, backlog, schéma et fiche de session ([`journal/sessions/c3d0f0bd…`](journal/sessions/c3d0f0bd-e344-4600-a023-0ed50d25b48b.md)) ; revue, budget, en-cours, backlog, journal, schémas et fraîcheur de l'état **verts**. Arbre propre pour ma part (seuls les journaux d'un pair restent en cours).

**Ce que la session laisse comme prochaines actions** : B10.2bis → tester la **capacité**, le **corpus** ou l'**objectif** (un à la fois, même protocole) ; A8.3b → isoler le **mode de lot** ; R4.4 reste **bloqué** (aucun OCR) ; R0.4/R0.5 portés par `8156fdcb`.

### Tour 4 — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h

*87 appels d'outils.* Actions notables :

- create_goal
- bash — Inspect the multilingual data and synthetic corpus
- bash — Read the JW manifest structure
- bash — Inspect the parallel units of the JW corpus
- bash — Read the corpus sampling and metrics code
- bash — Write and smoke-test the JW parallel corpus loader
- bash — Count units per JW article
- bash — Patch the trainer for the JW corpus and smoke-test
- bash — List native checkpoints and check the chrF floor
- bash — Launch the JW corpus experiment (9 runs)
- bash — Prepare the JW report generator
- bash — Check the first JW results
- bash — Chain the capacity experiment after JW
- bash — Run the JW reconstruction control on GPU 1
- … et 64 autres

**Synthèse produite :**

⏵ Cycle clos : 3 h 06, trois goals enchaînés, passe complète verte (60/62, 2 tolérées)

**Trois goals successifs, tous mesurés et committés** (19 h 06 → 22 h 12).

\### Goal 1 — Programme B : les leviers du décodeur

| levier | dispositif | résultat |
|---|---|---|
| **corpus** | corpus parallèle **JW** : 5 articles, **12 langues**, **139 unités** alignées ; 3 bras × 3 graines | traduction **7,6 / 6,3 / 8,0** contre un plancher de **17,1** ; reconstruction **9,4** (plancher 37,8) → **négatif** |
| **capacité** | base **31,77 M** (3,4×), même protocole, 3 bras | **11,8 / 11,6 / 11,7** contre 11,1 / 11,2 / 11,0 (plancher 38,5) : **+0,5 à +0,7 point** → **négatif** |

**B10.2bis est close** : quatre leviers testés — attention croisée, durée, corpus, capacité — quatre négatifs. Le prochain n'est plus un réglage : c'est l'**objectif de décodage** (non byte-level) ou l'échelle N5 (gelée). Ajouts : [`corpus_jw.py`](tools/semantique/corpus_jw.py), `--corpus {udhr,jw}` dans le trainer.

\### Goal 2 — Programme A : le transport

**A8.3c — le lot n'est pas neutre.** En f32, lot 1 → **61,9920**, lot ≥ 2 → **60,8135** (−1,90 %) ; le mélange KV est **cohérent par chemin** (−5,9 % jeton par jeton, +3,2 % par lots). La « non-monotonie » d'A8.3b était donc un **effet de chemin**, pas la règle — et le moteur le documente déjà (`main.rs` : préremplissage par lots non bit-à-bit identique). A8.3 reste opt-in, pour la bonne raison. Ajout : `LOT` dans `porte-flux` (défaut inchangé).

\### Goal 3 — Programme portes : la passe complète

**62 portes, 60 vertes, 2 rouges, 1 h 46** — les deux rouges sont les **structurelles connues** (`porte-indice` 895 s, `porte-melange` 110 s), mêmes diagnostics : **aucune régression**. Six portes ont été ajoutées par un pair pendant la journée (68 au disque) et prendront leur tour à la prochaine passe. `references-non-regression.md` et `en-cours` à jour.

**État final** : T0 **3 997**, revue, en-cours, backlog, journal, schémas et fraîcheur de l'état **verts**. Commits de la session : `0eff33e1` (capacité), `a1aae534` (A8.3c), `ebd8a960` (état), `dc0587a0` (passe), plus le corpus JW. Les pairs ont avancé en parallèle (N3, A8.0, R0.5) sans conflit.

**Prochaines actions nommées** : B10 → objectif de décodage ou N5 ; A2.6 bloqué par A6.2 (pas de MoE local) ; R4.4 bloqué (aucun OCR) ; les 6 portes récentes dans la prochaine passe.

### Tour 5 — continue

*47 appels d'outils.* Actions notables :

- create_goal
- bash — Check existing decoders and GPU availability
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/semantique/decodeur_mots.py`
- bash — Check whether the trainer saves the trained encoder
- bash — Load the trained encoder and smoke-test the word decoder
- bash — Fix the token slice and retry
- bash — Run the word decoder experiment (3 seeds)
- bash — Add the trained-model controls and rerun
- bash — Check the patch state and processes
- bash — Apply the controls patch
- bash — Run the word decoder experiment with controls
- bash — Check the word decoder training
- bash — See the error after the first seed
- bash — Wait for the 3-seed measurement
- … et 29 autres

**Synthèse produite :**

⏵ Trois rounds sur le décodeur — l'objectif lève la surface, `z` reste le verrou

**B10 — l'objectif de décodage, trois expériences** (toutes mesurées, écrites, committées).

| round | dispositif | résultat | contrôle | commit |
|---|---|---|---|---|
| **décodeur mot (UDHR)** | même `z` **gelé** (9,29 M), 3 000 pas, 3 graines ; décodeur de mots (2 couches d'attention croisée) | **32,5** de chrF (plancher **33,7**) contre **11,1** pour l'octet — **96 % du plancher** | `z` d'un autre article : **29,9** (−2,6) | `2640e017` |
| **décodeur mot (JW)** | encodeur JW gelé, 139 unités, 11 langues, corpus **non formulaire** | **26,7** contre un plancher de **17,1** (**+9,5**) — il **bat le plancher** ; l'octet restait à 7,6 | `z` d'une autre unité : **24,8** (−1,9) | `e3747c3f` |
| **contrastif** | terme `λ·relu(marge − (CE_z_mélangé − CE_z_correct))`, marge 1,0 | **32,6** (inchangé) ; écart `z` **1,45** (contre 2,57) | le décodeur devient plus **robuste** au mauvais `z`, pas plus lecteur | `ecb67fe9` |

**Ce que ça dit.** Le levier **objectif** est réel et positif : le décodeur octet était un goulot, le décodeur mot atteint le plancher sur l'UDHR et le **dépasse** sur JW. Mais sur les **deux** corpus, le `z` ne porte que **1,5 à 2,6 points** de chrF — et le terme contrastif ne corrige rien, parce que le décodeur satisfait la contrainte **sans consulter `z`** (le prior de langue et de registre suffit). **B10.3 reste bloqué** : on ne peut pas raisonner sur un sens que le décodeur ne lit qu'à ~7 %. Le verrou est l'**encodeur / le conditionnement**, et le prochain test doit **retirer le prior** : une **langue tenue à l'écart** (le décodeur ne l'a jamais vue) ou une tâche de **contenu** (retrouver un fait précis, pas le style).

**État** : T0 **3 999**, revue, en-cours, backlog et fraîcheur de l'état **verts** ; compteurs **361 fiches / 434 JSON**. Le code du décodeur ([`decodeur_mots.py`](tools/semantique/decodeur_mots.py)) porte `--corpus {udhr,jw}` et `--contraste`.

**Nommé pour la suite** : langue tenue à l'écart (B10), contenu plutôt que style ; les pairs continuent A8.0 (19/33 portes épinglées) et N3.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_tableaux.py` | 2 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/tableaux/mesures.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/tableaux/notes.csv` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/tableaux/eleves.csv` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/tableaux/sans-entete.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/tableaux/irregulier.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/tableaux/fusions.html` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/tableaux/multi-niveaux.html` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/tableaux/entete-fusionnee.html` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-bloc-tableaux.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/tableaux/imbrique.html` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r41-bloc-tableaux.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/bloc-tableaux.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_code.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-bloc-code.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r42-bloc-code.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/bloc-code.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_maths.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-bloc-maths.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r43-bloc-maths.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/bloc-maths.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-miroir-blocs.sh` | 2 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-miroir-blocs.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83-defaut.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83b-regimes.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/semantique/decodeur_mots.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check sizes of key state docs
- **T1** Review recent commits and working tree
- **T1** List backlog fiches and R4 references
- **T1** Search table handling mentions
- **T1** Inspect document graph table handling
- **T1** Inspect bench documents and R0.3 results
- **T1** Look for existing table parsing code
- **T1** Show per-type bench results
- **T1** Show aggregates and details shapes
- **T1** Show table-type results across benches
- **T1** Compare per-type question counts and values
- **T1** Find C4 date control references
- **T1** Check A8.3 and B11.10 status
- **T1** Check R4 mentions in docs and implantation files
- **T1** Inspect table region code and bench table questions
- **T1** Count distinct documents per bench type
- **T1** Read the manques page
- **T1** Inspect bench question generation for tables
- **T1** Check gates and any table-related commits
- **T1** Read deferred table note and backlog priorities
- **T1** Inspect the existing table gate
- **T1** Search B10.2bis definition
- **T1** Read dependency notes on A8.3 condition
- **T1** Find pending human decisions
- **T1** Verify table gold passages are flattened table regions
- **T1** Trace gold passage types for table documents
- **T1** Count table-gold questions and show examples
- **T1** Check whether expected values are row labels
- **T1** Read the gates method doc header
- **T1** Read document gate structure
- **T1** Check how value score is computed
- **T1** Check running jobs and working tree state
- **T1** Inventory HTML and CSV corpus
- **T1** Recheck git state after session activity
- **T1** Read the result contract
- **T1** Re-read current state after R0.3 close
- **T1** Check DSH environment and journals dir
- **T1** Inspect the R0.3 closing commit
- **T1** List session journals
- **T1** Check whether the R0.3 session closed
- … et 445 autres

## 4. Mesures et résultats marquants

- **T1** `c8acf22e N0.15/N4.7 — MEILLEUR 2,6998 SERVI : PARITÉ NATIVE, 650,1 MS`
- **T1** `08149617 R0.2 — À 30 % DU BUDGET, LE CONTRÔLEUR RÉCUPÈRE 100 % DES PASSAGES ; LE LECTEUR PLAFONNE À 25–75 %`
- **T1** `journal/2026-10-24/README.md:107:| 15:32 | `976d55e4` | A7.2 + A8.2 — LE RELAIS A CHIFFRE EGAL, ET LA PERTE ENTRE DANS LA REGLE. A7.2 etabli : porte-topologie (92 s, 42.5477) — une couche executee ail`
- **T1** `journal/2026-10-24/README.md:117:| 16:31 | `b22b7097` | A8.3 — LA REGLE PLACE ET PERTE EST BRANCHEE : placement::kv_precision choisit la precision du KV par couche selon le budget DRAVE_PERTE_MAX (def`
- **T1** `journal/2026-10-24/README.md:122:| 16:57 | `5c69a33f` | A8.3 — LA REGLE DEVIENT OPT-IN : le passage du defaut a la regle place+perte a DECALE les portes (porte-coupe est passee de +0,52-17,09 % a 5,9-`
- **T1** `journal/2026-10-24/distribue.md:21:| 15:32 | `976d55e4` | A7.2 + A8.2 — LE RELAIS A CHIFFRE EGAL, ET LA PERTE ENTRE DANS LA REGLE. A7.2 etabli : porte-topologie (92 s, 42.5477) — une couche executee a`
- **T1** `journal/2026-10-24/distribue.md:26:| 16:31 | `b22b7097` | A8.3 — LA REGLE PLACE ET PERTE EST BRANCHEE : placement::kv_precision choisit la precision du KV par couche selon le budget DRAVE_PERTE_MAX (d`
- **T1** `journal/2026-10-24/modele.md:57:`choisir_avec_perte` (3 nouveaux tests) refuse la tête 4 bits (+10 %) à un budget de 5 %, accepte l'int8 tardif`
- **T1** `Le codec lit 100 % du corpus, mais les cartes restent à 69,3 % et certaines surfaces sont ambiguës (`A1`, `E4`, `d4`, `b6-c5`).`
- **T1** `B11.1–B11.9 mesurés ; B11.10 suivant ; le codec reste à 100 % sur son domaine.`
- **T1** `| **M5** | **décodage spéculatif** — aucune ligne de moteur | brouillon générique ×0,70 · paire alignée ×1,09 · brouillon minuscule **×1,52** | la latence du décodage ; mais le cahier des charges est `
- **T1** `| **M6** | **le moteur n'apprend pas** — il applique, mesure, sauve et recharge une matrice additive, mais ne touche jamais aux poids | notre seule règle locale est **réfutée** (transfert nul, −5 à −1`
- **T1** `| **M9** | ~~aucun instrument ne mesure le coût de la SPARSITÉ DES POIDS~~ **LIVRÉ le 11/10, les deux moitiés** | (1) `tools/occupation_poids.py` lit l'occupation d'un GGUF par genre ; (2) le **moteur`
- **T1** `**8,6 Mo/s sur disque dur** contre 243 Mo/s en séquentiel (÷28) — un préchargement`
- **T1** `**29 Mo/s** au hasard sur l'array, **1 126 Mo/s** sur un motif d'experts. Ce qui paie n'est pas`
- **T1** ``madvise` — sur une plage entière il rend **×1,06**, et sa granularité **ne change rien** dans le`
- **T1** `parallèle ramène le temps de **calcul** d'une passe de **7,70 s à 3,65 s** (−53 %) et la passe de`
- **T1** `utile de 75 %.`
- **T1** `**l'allocation** est 37 à 91 % du coût d'un montage d'expert (`reports/rapport-vram-transfert.md`).`
- **T1** `| **N1** | **structure innée à l'échelle** — gratuite à 25 % à dim 384 (+1,0 %), coûteuse à 12,5 % (+13,7 %) **et à dim 512 (+6,7 %)** | E1 et m16, mesurés | un connectome inné viable demande un masqu`
- **T1** `| **N4** | **profondeur routée** (mixture-of-depths), **budget d'événements appris**, **quantification adaptée aux listes** | dessins évalués ; le **chemin court entraîné** (dessin B) est mesuré depui`
- **T1** `| **N5** | **mémoire d'un signal injecté** — le modèle n'en a aucune, **et il ne l'APPREND pas** | sonde linéaire **et** non linéaire sur l'état de sortie : le signal **courant** est lisible (**R² 0,9`
- **T1** `d28ad551 B12 — PIPELINE M1→M4→M8 : 528/528, COMPLÉTION 96,3 %, 7 PROTOTYPES (DOCS)`
- **T1** `journal/2026-10-22/moteur.md:70:(64 % au 1,5 B, 28 % au 32 B) : la décroissance n'est pas attribuable à la taille, et le « 1,5 B bat les gros » de`
- **T1** `journal/2026-10-22/moteur.md:76:suffit pas à rendre les modèles comparables : chaque modèle a sa meilleure couche. Le 32 B à la couche 32 (50 %)`
- **T1** `journal/2026-10-22/moteur.md:98:**Le 24 octobre — B2.7 tranché : à profondeur fixe, l'échelle AIDE.** Le 32 B à la couche 32 (50 %) donne 0,600`
- **T1** `journal/2026-10-22/moteur.md:284:loin du 32 B (0,600/0,772). La taille ne garantit rien, même au même endroit : le 14 B est meilleur à 67 % (0,63) et`
- **T1** `72a4ff5f R0.3 — 249 QUESTIONS, 30 DOCUMENTS SUR GPU : SÉLECTION 1,000 À 30 %, LE CONTRÔLEUR BAT LA TRONCATURE 5,5×`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `1,000 à 30 %, 5 types, commit `08149617`) ; **R0.3** en cours depuis le 29/10.`
- **T1** `**1,000** à 30 % ; modèle **0,231** contre troncature **0,042** ; hasard et closed-book **0,000**.`
- **T1** `- **R0 — lecteur v0** : R0.1 **mesuré** (51 pages) et R0.2 **mesuré** (récupération 1,000 à 30 %, 5 types) ;`
- **T1** `- **N2 — distillation** : GPU ; meilleur **2,6998** (contexte 129) ; porte **< 2,5** non atteinte. **N0.15/N4.7** : exporté, parité native, servi **650,1 ms**. **N4.8** : consignes courtes **0/40** su`
- **T1** `- **R0** : **90 %** à **30 %** du coût ? → **R0.3** (banc) tranche.`
- **T1** `docs/archive/colab-reparti.md:58:  | 0 ms (localhost) | 16,8 ms | 1,01× |`
- **T1** `docs/archive/colab-reparti.md:59:  | 5 ms | 33,0 ms | 1,99× |`
- **T1** `docs/archive/colab-reparti.md:60:  | 20 ms | 81,8 ms | 4,89× |`
- **T1** `4. coût        : ×3.92 de temps pour ×4 lectures (0.55 ms / lecture)`
- **T1** `4. coût        : ×4.06 de temps pour ×4 lectures (0.54 ms / lecture)`
- **T1** `4. coût        : ×3.97 de temps pour ×4 cellules (2.42 ms / 150 cellules)`
- **T1** `4. coût        : ×3.85 de temps pour ×4 cellules (2.53 ms / 150 cellules)`
- **T1** `4. coût        : ×4.08 de temps pour ×4 cellules (2.27 ms / 150 cellules)`
- **T1** `> 1,9 s/appel) ; budgets 10/30/50 % ; JSON bruts`
- **T1** `plafond de 25–75 % du lecteur extractif était-il celui du lecteur ou du document ?`
- **T1** `**30 documents** (5 types × 6) : prose (théorie), technique (implantation), tableau (pilotage),`
- **T1** `| type | récup. 10 % | récup. 30 % | récup. 50 % | valeur 30 % | valeur 100 % | aléatoire 30 % |`
- **T1** `À **30 %** du budget, le passage gold est lu dans **100 %** des cas sur les cinq types — la`
- **T1** `courbe est plate entre 30 et 50 %, et commence à mordre à 10 % (0,87–1,00). Le **hasard** reste`
- **T1** `| type | contrôleur 30 % | début 30 % | closed-book |`
- **T1** `4. coût        : ×3.82 de temps pour ×4 cellules (2.49 ms / 150 cellules)`
- **T1** `Le budget est une **fraction du document** (10 %, 30 %, 50 %) : c'est ce qui rend les`
- **T1** `| [rapport-speculatif-reflexe.md](rapport-speculatif-reflexe.md) | Le réflexe propose, le cerveau vérifie — acceptation 2 à 30 % (le cerveau non entraîné : 0 %) |`
- **T1** `| [rapport-vitesse-v41.md](rapport-vitesse-v41.md) | Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé |`
- **T1** `247:| [rapport-r02-controleur.md](rapport-r02-controleur.md) | R0.2 — le contrôleur de lecture : 100 % de récupération à 30 % du budget |`
- **T1** `R0.3 — 249 QUESTIONS, 30 DOCUMENTS SUR GPU : SÉLECTION 1,000 À 30 %, LE CONTRÔLEUR BAT LA TRONCATURE 5,5×`
- **T1** `Dispositif : 30 documents (5 types × 6), 249 questions générées à valeur numérique (deux mots`
- **T1** `Résultat extractif : à 30 % du budget, le passage gold est lu dans 100 % des cas sur les cinq`
- **T1** `types (0,87–1,00 à 10 %) ; hasard 0,20–0,39 ; le taux de réponse est exactement celui de la`
- **T1** `tableau imbriqué, colonne de texte non sommable). Coût **≈ 25 ms / 1 000 cellules**, linéaire`
- **T1** `(×3,8 pour ×4). Fiche : [`rapport-r41-bloc-tableaux.md`](../../../reports/rapport-r41-bloc-tableaux.md) ;`
- **T1** `98:- **Le coût** est celui du **parsing** (25,0 ms pour 1 000 cellules, entrées-sorties`
- **T1** `99:  comprises ; ×3,80 pour ×4 cellules, donc linéaire) ; le coût des opérations n'est pas`
- **T1** `[still running after 60000ms; moved to background job bash-100]`
- **T1** `Résultat : réponses justes à 30 % — lexical 0,30, modèle 0,717, troncature naïve 0,133,`
- **T1** `4. coût        : ×3.96 de temps pour ×4 cellules (2.41 ms / 150 cellules)`
- **T1** `[still running after 60000ms; moved to background job bash-108]`
- **T1** `3724480 3659624      67 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - <<'MSG' R4.1 — LE BLOC TABLEAUX : 996 CELLULES, 802 EXACTES, LE TEXTE PLAT RATE 3/3  Dispositif : `
- **T1** `| 14:18 | `c8acf22e` | N0.15/N4.7 — MEILLEUR 2,6998 SERVI : PARITÉ NATIVE, 650,1 MS | `en-cours.md`, `README.md`, `docs.md` (+3) |`
- **T1** `[still running after 60000ms; moved to background job bash-117]`
- **T1** `40:   30 % sur 5 types et **249 questions**) ; la suite est **R0.4** — les trois têtes — ou le banc durci.`
- **T1** `162:| **R0.3** | **banc de lecture rapide** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles closed-book, régions aléatoires, sections mélangées |`
- **T1** `30 % sur 5 types et **249 questions**) ; la suite est **R0.4** — les trois têtes — ou le banc durci.`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `| **R0.2** | **contrôleur de lecture** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, titres, premières/dernières phrases, BM25/regex) | ✅ **1,000`
- **T1** `| **R0.3** | **banc de lecture rapide** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles closed-book, régions aléatoires, sections mélangées | ✅ *`
- **T1** `989102e1 B11.10 — CARTES 161/161, AMBIGUÏTÉS REFUSÉES : LE 69,3 % EST NATIF`
- **T1** `docs/pilotage/en-cours.md:60:- **R0 — lecteur v0** : R0.1 **mesuré** (51 pages) et R0.2 **mesuré** (récupération 1,000 à 30 %, 5 types) ;`
- **T1** `docs/pilotage/en-cours.md:112:- **R0** : **90 %** à **30 %** du coût ? → **R0.3** (banc) tranche.`
- **T1** `-  1,000 à 30 %, 5 types, commit `08149617`) ; **R0.3** en cours depuis le 29/10.`
- **T1** `-- **R0 — lecteur v0** : R0.1 **mesuré** (51 pages) et R0.2 **mesuré** (récupération 1,000 à 30 %, 5 types) ;`
- **T1** `-- **N2 — distillation** : GPU ; meilleur **2,6998** (contexte 129) ; porte **< 2,5** non atteinte. **N0.15/N4.7** : exporté, parité native, servi **650,1 ms**. **N4.8** : consignes courtes **0/40** s`
- **T1** `-- **R0** : **90 %** à **30 %** du coût ? → **R0.3** (banc) tranche.`
- **T1** `+- **R0** : **90 %** à **30 %** du coût ? → R0.3 a tranché la **sélection** (1,000 ; paraphrase 0,30 contre 0,717) ;`
- **T1** `-   30 % sur 5 types et **249 questions**) ; la suite est **R0.4** — les trois têtes — ou le banc durci.`
- **T1** `+   30 % sur 5 types et **249 questions**) ; **R0.4** (tête de survol) est un **pilote négatif**`
- **T3** `ok 293 ko 0 noeuds 445216 fonctions 1681 classes 67`
- **T3** `6. coût        : ×4.29 de temps pour ×4 nœuds (0.30 ms / 50 additions)`
- **T3** `6. coût        : ×4.37 de temps pour ×4 nœuds (0.29 ms / 50 additions)`
- **T3** `6. coût        : ×4.20 de temps pour ×4 termes (0.36 ms / 50 additions)`
- **T3** `· d7a4d1bf A8.0 — PORTE-PONT ÉPINGLÉE : PPL 113,0068 / 111,9225, FALAISE +2,81 % / +25,35 %`
- **T3** `d7a4d1bf A8.0 — PORTE-PONT ÉPINGLÉE : PPL 113,0068 / 111,9225, FALAISE +2,81 % / +25,35 %`
- **T3** `**113,0068 / 111,9225** (falaise **+2,81 % / +25,35 %**) ; fiches`
- **T3** `- **R0** : **90 %** à **30 %** du coût ? → R0.3 a tranché la **sélection** (1,000 ; paraphrase 0,30 contre 0,717) ;`
- **T3** `drave-core/src/model.rs:4709:        // premières couches, +0,03 % sur les dernières (A5.3) — le budget `DRAVE_PERTE_MAX``
- **T3** `ok 40 ko 0 []`
- **T3** `ok 296 ko 0`
- **T3** `6. coût        : ×4.07 de temps pour ×4 termes (0.43 ms / 50 additions)`
- **T3** `6. coût        : ×4.28 de temps pour ×4 nœuds (0.30 ms / 50 additions)`
- **T3** `4. coût        : ×3.85 de temps pour ×4 cellules (2.49 ms / 150 cellules)`
- **T3** `(falaise **+2,81 % / +25,35 %**) ; fiches [`a80-flux`](../../reports/rapport-a80-porte-flux.md),`
- **T3** `- **B11.10** : **mesurée** — codec **161/161**, ambiguïtés refusées ; **69,3 %** = natif ;`
- **T3** `// précision par couche quand rien n'est forcé : l'int8 coûte +2,28 % sur les`
- **T3** `// premières couches, +0,03 % sur les dernières (A5.3) — le budget `DRAVE_PERTE_MAX``
- **T3** `// décale les chiffres des portes (mesuré le 24/10 : porte-coupe passe de +0,5-17 % à`
- **T3** `// 5,9-11,6 % et échoue) — on ne change pas un défaut sans épingler les portes d'abord.`
- **T3** `(l'int8 coûte +2,28 % sur les premières, +0,03 % sur les dernières)");`
- **T3** `34:> `porte-pont` **+2,81 % / +25,35 %**, `porte-coupe` **+0,52 % → +17,09 %**, `porte-gain` **29,0206 →`
- **T3** `132:| `porte-pont.sh` | 75 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |`
- **T3** `#      de 108,87 à 118,53 de perplexité — soit 9 % d'écart — parce que l'erreur de`
- **T3** `#      d'un pont de 448 fibres va de +0,52 % (coupe 18/6) à +17,09 % (coupe 15/9).`
- **T3** `=== flux, règle ON (budget 1 %) ===`
- **T3** `deux nœuds        : perplexité 111.8003  (2.4 s)`
- **T3** `=== budget 0,001 % (aucune couche int8) ===`
- **T3** `=== budget 10 % (toutes les couches int8 ?) ===`
- **T3** `a489d9ff A8.3 — LE DÉFAUT PLACE+PERDE DÉPLACE LES PORTES DE −5,9 % À +19,5 % : OPT-IN CONSERVÉ`
- **T3** `71:| A3.2 | **Granularité** : par couche, par bloc, par expert | ✅ | listes i16, échelles par bloc, indices par écarts : **1 608 octets par flux** à 256 jetons ; le mode « lot en listes » : 1,5 ko/jet`
- **T3** `72:| A3.3 | **Seuil de rentabilité** : à quel débit/latence le découpage gagne | 🔬 | attente ≈ calcul distant + **3,2 × latence** : 1,01× à 0 ms, 1,99× à 5 ms, 4,89× à 20 ms ; le débit ne compte pas (`
- **T3** `reports/rapport-compacite-trace.md:201:   flux pèse 1,5 ko et c'est la latence qui coûte (`attente ≈ calcul + 3,2 ×`
- **T3** `0, 1 MiB, 16384 MiB, 0 %`
- **T3** `1, 1 MiB, 16384 MiB, 0 %`
- … (tronqué)

## 5. Erreurs rencontrées

7 sorties en erreur ou divergentes. Les premières :

- **T3** : code=128 [stderr] fatal: Unable to create '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.git/index.lock': File exists.  Another git process seems to be running in this repository, or the lock file 
- **T3** : [stderr]   File "<stdin>", line 11     s = s.replace('''    python3 - "$bloc" "/tmp/miroir-${bloc}.json" <<'PY'''',                                                                               ^ Synt
- **T3** : jeu 29 oct 2026 17:06:41 EDT === 1800 pas, bras a === [exit code: 2]
- **T4** : jeu 29 oct 2026 19:47:25 EDT 6   pas   600 · perte 10.2454 · align 0.945 · rappel 0.198 (mélangé 0.020) · sonde 0.147 · chrF rec 0.0 / trad 7.1 / plancher 17.1 · 278 s # écrit /tmp/jw-b-s2 et /tmp/jw-
- **T5** : ven 30 oct 2026 08:39:03 EDT Loading weights:   0%|          | 0/68 [00:00<?, ?it/s]Loading weights: 100%|██████████| 68/68 [00:00<00:00, 1176.91it/s]   pas   500 · perte 0.107 · chrF rec 26.5 / tra
- **T5** : ven 30 oct 2026 08:54:39 EDT Loading weights:   0%|          | 0/68 [00:00<?, ?it/s]Loading weights: 100%|██████████| 68/68 [00:00<00:00, 1224.66it/s]   pas   500 · perte 1.689 · chrF rec 24.8 / tra
- **T5** : ven 30 oct 2026 09:15:22 EDT Loading weights:   0%|          | 0/68 [00:00<?, ?it/s]Loading weights: 100%|██████████| 68/68 [00:00<00:00, 1090.39it/s]   pas   500 · perte 0.097 · chrF rec 25.2 / tra

## 6. Commits

- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - <<'MSG' R4.1 — LE BLOC TABLEAUX : 996 CELLULES, 802 EXACTES, LE TEXTE PLAT RATE 3/3  Dispo
- JOURNAL — R4.1 ENTRE AU RÉCIT DU JOUR (55 COMMITS)" >/tmp/journal-commit.log 2>&1; echo "code=$?"; tail -3 /tmp/journal-commit.log
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date; ls -l --time-style=+%H:%M:%S docs/pilotage/en-cours.md docs/pilotage/roadmap.md tools/routeur.py rep
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/backlog/index.md <<'MS
- JOURNAL — R4.1 ET L'ÉTAT DANS LE RÉCIT DU JOUR (59 COMMITS)" >/tmp/j2.log 2>&1; echo "code=$?"; tail -2 /tmp/j2.log; git status --short
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short; echo "--- checks ---"; python3 tools/verifier_schemas.py 2>&1 | tail -1; bash tools/po
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/schemas/chantiers-etats.svg && git commit -- docs/schemas/chantiers-etats.svg -F - <<'MSG' >/
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - -- docs/schemas/chantiers-etats.svg <<'MSG' >/tmp/svg-commit.log 2>&1 SCHÉMA — R4.1 MESURÉ
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - -- docs/pilotage/en-cours.md <<'MSG' >/tmp/compteurs.log 2>&1 ÉTAT — COMPTEURS 285 / 352 (
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/bloc_code.py tools/porte-bloc-code.sh tools/tests/code docs/implantation/bloc-code.md docs/p
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/bloc_code.py tools/porte-bloc-code.sh tools/tests/code docs/implantation/bloc-code.md docs/p
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/index.lock 2>/dev/null || echo "pas de verrou"; git add docs/pilotage/en-cours.md && git commit -F
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/index.lock 2>/dev/null || echo "verrou libre"; git add tools/bloc_maths.py tools/porte-bloc-maths.
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/index.lock 2>/dev/null || true; git add tools/bloc_tableaux.py tools/bloc_code.py tools/bloc_maths
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/index.lock 2>/dev/null || true; git add reports/rapport-a83-defaut.md reports/a83-defaut.json repo
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit --amend -F - <<'MSG' >/tmp/am83.log 2>&1 A8.3 — LE DÉFAUT PLACE+PERDE DÉPLACE LES PORTES DE −5,
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/index.lock 2>/dev/null || true; git add docs/pilotage/backlog/A3.2-granularite.md docs/pilotage/ba
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py 2>&1 | tail -1; git add reports/rapport-b102bis-decodeur.md reports/b102bis
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") s = p.read_text() vieux = "|
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -6 /tmp/portes-gpu.log; git add docs/pilotage/backlog/A2.6-ordonnanceur.md docs/pilotage/backlog/N3-o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") s = p.read_text() vieux = "-
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/references-non-regression.md && git commit -F - -- docs/pilotage/references-non-regr
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add journal/sessions/c3d0f0bd-e344-4600-a023-0ed50d25b48b.md && git commit -F - -- journal/sessions/c3
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/references-non-regression.md") s = p.read_
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/semantique/corpus_jw.py tools/semantique/corpus.py tools/semantique/entrainer.py reports/rap
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") s = p.read_text() vieux = "|
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") s = p.read_text() vieux = "-
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") s = p.read_text() vieux = "*
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") s = p.read_text() paires = [
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") s = p.read_text() vieux = "d
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py 2>&1 | tail -1; git add reports/rapport-b10-mots-jw.md reports/b10-mots-jw.
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py 2>&1 | tail -1; git add reports/rapport-b10-contraste.md reports/b10-mots-c


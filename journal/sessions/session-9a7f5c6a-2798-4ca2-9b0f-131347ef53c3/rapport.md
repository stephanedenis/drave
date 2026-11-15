# Session session- — Rapport gold 452 et split H50

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-9a7f5c6a-2798-4ca2-9b0f-131347ef53c3` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 08:57 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 67 |
| Appels d'outils | 129 |
| Fichiers touchés | 9 |
| Commandes | 76 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche W1 (semaine 2, J1 matin, la part du pilote) : le gold réel 452 — **ne modifie pas le gold** (S/D). Écris `reports/rapport-gold-452.md` + JSON : (1) la composition exacte des 452 (20 hand + 432 corpus, par langue, par source) ; (2) le **split 402 / H50** proposé (50 phrases mises à l'écart, la règle déterministe du tirage, la graine) ; (3) le **sha256 avant** du gold ; (4) la **liste des 10 G … [196 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche W1 (semaine 2, J1 matin, la part du pilote) : le gold réel 452 — **ne modifie pas le gold** (S/D). Écris `reports/ … [476 caractères tronqués]

*129 appels d'outils.* Actions notables :

- bash — Inspect repo root and git state
- bash — List gold dir and reports dir
- bash — Search plan for 452 references
- bash — Inspect gold_reel_50 and gold_split
- bash — Find existing gold reports and W1 task
- bash — Read semaine-2 plan
- bash — Read existing C3 report part 1
- bash — Search docs for gold 200+ mentions
- bash — Search H50 references
- bash — Search seed mentions in gold 50
- bash — Read C3 report part 2
- bash — Inspect C3 JSON top-level structure
- bash — Locate selection function in gold_reel_50.py
- bash — Read gold_reel_50 selection logic
- … et 99 autres

**Synthèse produite :**

\## Livrables

- Fiche : [`reports/rapport-gold-452.md`](reports/rapport-gold-452.md)
- JSON : [`reports/rapport-gold-452.json`](reports/rapport-gold-452.json)

\## Ce que la fiche établit

**1. Composition exacte des 452**
- **20 hand** (`gold.json`) : 14 fr + 6 en.
- **432 corpus** (`gold_reel.json`, source brute `reel`) : 228 fr + 204 en.
- Total : **242 fr + 210 en**, **2 480 tokens**, **1 501 segments**, **184 cibles** (GP 72, REL 58, SUB 54).
- Il reste **10 GP/SUB sans cible** : 9 GP + 1 SUB.

**2. Split 402 / H50**
- H50 = les **50 phrases dures de C3** : **2 hand + 48 corpus**, **25 fr + 25 en**, **323 tokens**, **190 segments**, **22 cibles**.
- 402 = **18 hand + 384 corpus**, **217 fr + 185 en**, **2 157 tokens**, **1 311 segments**, **162 cibles**.
- Règle déterministe : score `3×att + 2×POS + 1×segment absent`, tri `(-score, id)`, au plus 2 phrases par signature d'erreur, quota 25/25. **Aucun aléa.**
- **Graine `20261116`** : elle ne sert **pas** à tirer H50 (lot dur C3) ; elle fixe le **contrôle négatif** et le **manifeste** (`1615c17a…`). Le tirage aléatoire de cette graine est fourni dans le JSON, non retenu.
- Manifeste : `1615c17a97bb998451de66585dadcea0643ba1d7f8d962ccbdf28a13b575d970`.

**3. sha256 avant du gold** — identique après :
- `gold.json` : `3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a`
- `gold_reel.json` : `05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11`
- Concaténation ordonnée : `cff6b6d703546ad5992c5ada4fc99e1bdaa8e76e9cd089bd3e3b88bd71e90ac5`

**4. 10 GP/SUB candidats pour S** (cible proposée = verbe gouverneur) :

| id | span | cible |
|---|---|---|
| `r267` | `à moi` | `est` (30–33) |
| `r324` | `sur la table` | `est` (9–12) |
| `r328` | `on the table` | `is` (9–11) |
| `r336` | `to her` | `speaks` (20–26) |
| `r342` | `to her` | `speaks` (20–26) |
| `r349` | `sur la table` | `est` (9–12) |
| `r358` | `to her` | `speaks` (20–26) |
| `r363` | `on the table` | `is` (9–11) |
| `r367` | `to him` | `listen` (33–39) |
| `r429` | `que c'est vrai` (SUB) | `dit` (3–6) |

**4 dans H50** (`r324`, `r328`, `r349`, `r363`) ; double codage proposé sur ces 4. Si S accepte les 10 : **184 → 194** cibles (GP 72→81, SUB 54→55 ; H50 22→26, 402 162→168).

**5. « gold 200+ » retiré des docs**
- **18 occurrences** exactes supprimées, **0 ligne `200+`** restante dans `docs/**/*.md`.
- Les occurrences **B13** deviennent **« gold de pensée (B13) »** (noté `gold B13` dans la roadmap) ; les occurrences **linguisti
… [726 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 11 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Inspect repo root and git state
- **T1** List gold dir and reports dir
- **T1** Search plan for 452 references
- **T1** Inspect gold_reel_50 and gold_split
- **T1** Find existing gold reports and W1 task
- **T1** Read semaine-2 plan
- **T1** Read existing C3 report part 1
- **T1** Search docs for gold 200+ mentions
- **T1** Search H50 references
- **T1** Search seed mentions in gold 50
- **T1** Read C3 report part 2
- **T1** Inspect C3 JSON top-level structure
- **T1** Locate selection function in gold_reel_50.py
- **T1** Read gold_reel_50 selection logic
- **T1** Dump C3 JSON key structures
- **T1** Inspect gold file structures and composition
- **T1** Summarize C3 JSON fields
- **T1** Print 10 candidate spans
- **T1** Check tracking/commit status of C3 artifacts
- **T1** Read main setup of gold_reel_50
- **T1** Show selected IDs by language
- **T1** Recompute selection and test seeded tie-breaks
- **T1** Check IDs, duplicates, and sha256
- **T1** List all docs lines containing 200+
- **T1** Check current date and HEAD
- **T1** Read result/report conventions
- **T1** Show context windows around 200+ mentions
- **T1** Read contexts for roadmap/product/chantiers
- **T1** Read en-cours contexts
- **T1** Inspect candidates' tokens and segments
- **T1** Compute exact composition stats
- **T1** Compute split stats and seed control
- **T1** Count label occurrences before edits
- **T1** Check gitignore for report JSON
- **T1** Verify no 200+ remains in docs
- **T1** Review doc diff
- **T1** Generate W1 JSON
- **T1** Fix source keys and regenerate JSON
- **T1** Inspect generated JSON key data
- **T1** Check error parts and control text
- … et 36 autres

## 4. Mesures et résultats marquants

- **T1** `tools/chantier/plan.json:581:   "mandat": "Tâche F1 : le plan de la **semaine 2** (16 → 22/11) — lis le bilan de la semaine (`reports/rapport-bilan-semaine.md`), `docs/pilotage/en-cours.md` et les fic`
- **T1** `"mandat": "Tâche F1 : le plan de la **semaine 2** (16 → 22/11) — lis le bilan de la semaine (`reports/rapport-bilan-semaine.md`), `docs/pilotage/en-cours.md` et les fiches des tâches C/B/D/E, puis écr`
- **T1** `> diversité plafonnée) portent **37,1 %** des erreurs POS et **25,1 %** des segments absents pour`
- **T1** `> **11,1 %** des phrases ; l'heuristique y fait **68,42 %** de POS (étiquettes seules **75,68 %**)`
- **T1** `> contre **91,98 %** sur le reste. L'attachement, lui, est **saturé** : **183/184** (une seule`
- **T1** `d'erreur** : 102/275 erreurs POS (37,1 %), 87/346 segments absents (25,1 %), 1/1 erreur`
- **T1** `d'attachement. (3) Mesure : lot dur **68,42 %** POS, **58,36 %** F1, **21/22** attachement ; reste`
- **T1** `402 **91,98 %**, **81,90 %**, **162/162** ; 50 aléatoires stratifiées **87,24–90,77 %** POS,`
- **T1** `**73,68–83,63 %** F1, **95,0–100 %** attachement. Le lot dur est **hors** des contrôles pour le POS`
- **T1** `| POS heuristique | **88,91 %** (2 205/2 480 ; fermé 92,94 %, ouvert 84,66 %) | cette fiche |`
- **T1** `| POS hors tokenisation | **91,34 %** (2 205/2 414) | cette fiche |`
- **T1** `| F1 syntagmes | **79,06 %** (P 81,28 / R 76,95) | cette fiche |`
- **T1** `| attachement | **183/184 = 99,46 %** | cette fiche |`
- **T1** `| POS exact | 88,91 % | **68,42 %** | 91,98 % |`
- **T1** `| POS hors tokenisation | 91,34 % | **75,68 %** | 93,50 % |`
- **T1** `tokenisation** non tranchée. Les 66 erreurs globales (24 % du total) et les 31 du lot (30 %)`
- **T1** `Les **trois familles** qui restent : le **verbe lexical** (VERB→NOUN, 45,5 % des erreurs globales),`
- **T1** `la **tokenisation** des élisions/traits d'union (24 %), et les **classes ouvertes** (NOUN↔ADJ,`
- **T1** `PRON→DET, CONJ→PRON). Le lot dur **sur-représente** la tokenisation (30 % contre 24 %) : c'est un`
- **T1** `| précision | 81,28 % | **63,19 %** | 83,62 % |`
- **T1** `| rappel | 76,95 % | **54,21 %** | 80,24 % |`
- **T1** `| F1 | **79,06 %** | **58,36 %** | 81,90 % |`
- **T1** `| GN | 124 | **28** | 101 | **22** | 83,20 % | 67,11 % |`
- **T1** `| GV | 147 | **38** | 125 | **28** | 74,86 % | **45,00 %** |`
- **T1** `| GP | 0 | 0 | 25 | 4 | 86,63 % | 75,00 % |`
- **T1** `| REL | 0 | 0 | 11 | 5 | 91,34 % | 81,48 % |`
- **T1** `| SUB | 1 | 1 | 4 | 1 | 95,58 % | 88,89 % |`
- **T1** `| ADJ | 35 | 11 | 0 | 0 | 0 % | 0 % |`
- **T1** `| ADV | 30 | 9 | 0 | 0 | 0 % | 0 % |`
- **T1** `| PONCT | 9 | 0 | 0 | 0 | 0 % | 0 % |`
- **T1** `2. **ADJ/ADV/PONCT ne sont jamais produits** (rappel 0) : **74 des 346** segments absents (21,4 %)`
- **T1** `sont **structurels**, pas des erreurs de frontière. Le F1 79,06 % est donc **plombé par une`
- **T1** `Le lot dur **amplifie** les deux : GV F1 **45,00 %** (le pire des types **produits**), GN`
- **T1** `**67,11 %**, et 20 des 87 segments absents sont ADJ/ADV (structurels). Il reste **67 segments`
- **T1** `lot dur **ne le teste pas** (22 cibles, 21 justes ; les 50 aléatoires stratifiées font 95,0–100 %).`
- **T1** `| POS exact | 88,91 % | **68,42 %** | 91,98 % | **87,24–90,77 %** (moy. 89,18) |`
- **T1** `| POS hors tokenisation | 91,34 % | **75,68 %** | 93,50 % | **89,40–93,31 %** (moy. 91,37) |`
- **T1** `| F1 syntagmes | 79,06 % | **58,36 %** | 81,90 % | **73,68–83,63 %** (moy. 78,61) |`
- **T1** `| attachement | 99,46 % | **95,45 %** | **100 %** | **95,0–100 %** (moy. 99,38) |`
- **T1** `docs/pilotage/plan-travail.md:39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**`
- **T1** `docs/pilotage/plan-travail.md:195:   **0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **`
- **T1** `docs/pilotage/chantiers.md:88:| **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter que le résidu ? | ✅ **contrat + bloc v0** : 9 niveaux, **398 langues à 0,`
- **T1** `docs/pilotage/chantiers.md:90:| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime**`
- **T1** `docs/pilotage/roadmap.md:288:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `QlaErYTMvvpsFuJWrjlKAsu7/Xs3Qy93zHJ9w3e+Ml4qOCI76UxmHmy+e8dMf2rC+ptejYyv4XfhSvnfPvajGbn/rY+IR85dXePWyu4f/lh2Uv7v1gdx0LOGMucXtqO01VVZ1GT61b4vPUdZqrkusSOAeHSrC1tWTLtFSXS4R3vnK5Y8m0VAUlkt8yQI7Az82HVgXULR`
- **T1** `work/chantier/etat.json:491:   "sortie_agent": "ative : les **144 GN/GV** du lot (79 GN + 65 GV), soit 338 cibles au total.\n- **Sélection déterministe** : score `3×att + 2×POS + 1×segment absent`, 25`
- **T1** `work/chantier/etat.json:630:   "sortie_agent": "J’ai écrit [docs/pilotage/semaine-2.md](docs/pilotage/semaine-2.md) — **113 lignes** (limite 120).\n\nLe plan contient :\n\n- **5 jours × 2 vagues** : J`
- **T1** `work/chantier/boucle5.log:41: "sortie_agent": "ative : les **144 GN/GV** du lot (79 GN + 65 GV), soit 338 cibles au total.\n- **Sélection déterministe** : score `3×att + 2×POS + 1×segment absent`, 25 `
- **T1** `work/chantier/boucle8.log:12: "sortie_agent": "J’ai écrit [docs/pilotage/semaine-2.md](docs/pilotage/semaine-2.md) — **113 lignes** (limite 120).\n\nLe plan contient :\n\n- **5 jours × 2 vagues** : J1`
- **T1** `reports/rapport-gold-reel-50.md:236:| uniforme (12 classes, graine 0) | **8,36 %** (lot) · 9,56 % (global) | — | — |`
- **T1** `reports/rapport-gold-reel-50.md:237:| 50 au hasard, 8 graines | 85,00–91,01 % | 76,22–83,85 % | 100 % |`
- **T1** `reports/rapport-gold-reel-50.md:238:| 50 stratifiées, 8 graines | 87,24–90,77 % | 73,68–83,63 % | 95,0–100 % |`
- **T1** `tools/tests/linguistique/gold_reel_50.py:563:            "tirage_simple": "50 phrases au hasard, 8 graines : le POS reste ≥ 85 %.",`
- **T1** `**Part des erreurs** : le lot fait **11,1 %** des phrases et **13,0 %** des tokens, mais il porte`
- **T1** `**37,1 %** des erreurs POS (102/275), **25,1 %** des segments absents (87/346) et **100 %** de`
- **T1** `| majoritaire (classe la plus fréquente) | **21,98 %** (PRON, lot) · 23,47 % (global) | — | — |`
- **T1** `| uniforme (12 classes, graine 0) | **8,36 %** (lot) · 9,56 % (global) | — | — |`
- **T1** `| 50 au hasard, 8 graines | 85,00–91,01 % | 76,22–83,85 % | 100 % |`
- **T1** `| 50 stratifiées, 8 graines | 87,24–90,77 % | 73,68–83,63 % | 95,0–100 % |`
- **T1** `| **lot dur 50** | **68,42 %** | **58,36 %** | **95,45 %** |`
- **T1** `(le gold passerait à 502), les chiffres agrégés deviendraient : POS **86,55 %** (−2,36 pts),`
- **T1** `F1 **76,82 %** (−2,24 pts), attachement **204/206 = 99,03 %** (−0,43 pt). C'est une **projection**`
- **T1** `**split** 402/50 (91,98 % contre 68,42 %), pas 452/502.`
- **T1** `**Effet** : le dénominateur d'attachement passe de **184 à 194** (+5,4 %). Les 4 du lot dur sont`
- **T1** `(91,34 % global, 75,68 % lot) est le chiffre d'étiquetage.`
- **T1** `- **L'attachement.** 184 cibles, **une** erreur : le taux 99,46 % a une barre de confiance énorme`
- **T1** `de la plage (l'attachement stratifié va de 95,0 à 100 % à cause de `g017`).`
- **T1** `doivent plus être **toutes** in-sample. Le split 402/50 donne 91,98 % contre 68,42 % : c'est la`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `L88: ...**sans `par` : chunker 3/3, S ignore** ; **cible par proximité : exact ×13** ; **candidats verbes : top-k 0,4686** ; **échecs : 94 spans (48 REL/33 SUB/13 GP), 8 cibles** | **gold 200+** ; **p`
- **T1** `L90: ...ité : exact ×13** ; **candidats verbes : top-k 0,4686** ; **échecs : 94 spans (48 REL/33 SUB/13 GP), 8 cibles** (négation/modalité sous l'heuristique, la fusion la garde) ; **gold 200+** ; **p`
- **T1** `L288: ...le par proximité : exact 0,0042 → 0,0544 (×13)** ; **candidats verbes : top-k 0,4686 → 0,9724 avec les têtes** ; **échecs v2 : 94 spans (48 REL/33 SUB/13 GP) + 8 cibles** ; **gold 200+** ; **`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46) ; **J11.1–J11.4** ([exemples](../../reports/`
- **T1** `| **R — le lecteur** | un document, une question, un budget : réponse sourcée ou refus motivé ? | ✅ R0.1–R0.3 ; R0.4/R0.5 négatifs ; R4.1–R4.4 mesurés (R4.4 : 4/5 familles ≥ 90 %) | **R1.1/R1.2** (con`
- **T1** `-| **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter que le résidu ? | ✅ **contrat + bloc v0** : 9 niveaux, **398 langues à 0,9687**, **gold 432 réels + 16`
- **T1** `+| **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter que le résidu ? | ✅ **contrat + bloc v0** : 9 niveaux, **398 langues à 0,9687**, **gold 432 réels + 16`
- **T1** `| **D — les données** (nouveau) | avec quoi entraîne-t-on, et à quel prix ? | ✅ inventaire local ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**), **PDF** (322 Mo), **d`
- **T1** `-| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes**`
- **T1** `+| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes**`
- **T1** `| **N2 — le natif (session `0733c5bb`)** | entraîner et évaluer le modèle natif sur les corpus D, mesurer longueur, capacité, diversité | N2, N4, le mètre honnête | **GPU** (1 des 2), 8–16 cœurs | **N`
- **T1** `-| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **166/166** (6 S f`
- **T1** `+| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **166/166** (6 S f`
- **T1** `-   **0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusi`
- **T1** `+   **0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusi`
- **T1** `**147 scans détectés** (91 uniques, 2 053 p), **60 documents, 1 982 p, 4,41 M car.**, 8 Ko 0 ;`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **B11** | la base d'universaux typés : schéma, [parseur](../theorie/glossaire/entrees/parseur.md), codec, contexte | ✅ | **B11.10 close** (cartes, ambiguïtés refusées) ; le codec lit **100 %** |`
- **T1** `-| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** `
- **T1** `+| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** `
- **T1** `| **C3.2** | les modules par famille de langues | ✅ | aucune — **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤ 0,5 %** |`
- **T1** `**Ce qui compte pour R** : le **codec classique** lit **100 %** des surfaces ; c'est la preuve qu'un bloc`
- **T1** `"tirage_aleatoire": "graine 20261116 : POS 88,13 %, F1 78,69 %, attachement 100 % ; H50 : 68,42 %, 58,36 %, 95,45 %.",`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **5`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/gen_w1.py", line 67, in <module>     rows = [g.analyser(h, p) for p in phrases]             ~~~~~~~~~~^^^^^^   File "/home/stephane/Data13TB/st


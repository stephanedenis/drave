# Session 7263ca42 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `7263ca42-cd56-4c36-a6dd-8ff2d1024a43` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:22 |
| Durée | 0.7 h |
| Tours | 1 |
| Messages | 55 |
| Appels d'outils | 58 |
| Fichiers touchés | 1 |
| Commandes | 41 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **qualifier et chiffrer les 8 échecs restants** de l'attachement (état v2 du 2026-11-05).  Contexte : `tools/bloc_linguistique.py` (`Heuristique`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`). Sur les 145 segments gold dont le span est prédit, l'exact (égalité st … [1744 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **qualifie … [2024 caractères tronqués]

*58 appels d'outils.* Actions notables :

- bash — Check git state and reports listing
- bash — Check key files exist
- read
- bash — Inspect gold JSON structure
- bash — Reproduce the 8 attachment failures
- bash — Rerun reproduction script
- bash — Locate attachment logic lines
- bash — Trace S segmentation for the 8 cases
- bash — Dump predicted segments and gold segments
- bash — Find lexicon constants and _est_verbe
- bash — Read lexicons
- bash — Grep for r230/r309 references
- bash — Dump 145 label records and base counts
- bash — Inspect SUB cases with self/non-lexicon cibles
- … et 37 autres

**Synthèse produite :**

⏵ Bilan final : les 8 échecs qualifiés, 5 règles chiffrées, deux fiches écrites

\## Mission remplie

Deux fichiers neufs, **aucun fichier existant modifié, aucun commit** :
- [`reports/rapport-echecs-v2.md`](reports/rapport-echecs-v2.md) — la fiche
- [`reports/pensee-echecs-v2.json`](reports/pensee-echecs-v2.json) — les 8 fiches, règles, contrôles

Base reproduite par `evaluer_gold.py` : 239 cibles, **145 spans prédits**, **exact 137 (0,9448)**, top1 140, top-k 142, top-k strict 141. Les 8 échecs = 5,52 % des 145.

\### Convention (point de désaccord avec la fiche v2)
La ventilation v2 « **3 hors candidats / 5 mal classés** » est la lecture **sous-chaîne** ; en **égalité stricte** c'est **4 / 4** (`appelle` ⊂ `appelle-moi`). Le 141/145 du top-k strict correspond au 4/4.

\### Les 8 qualifications
| id | source/type | segment → gold / choisi | qualification |
|---|---|---|---|
| g002 | hand GP | `de la voisine` → `chat` / *(vide)* | cible vide + absente |
| g012 | hand GP | `à manger` → `prêt` / `manger` | mal choisie + auto-attachement |
| r018 | reel GP | `à manger` → `prête` / `manger` | idem g012 |
| r230 | reel SUB | `Quand tu arrives` → `appelle` / `appelle-moi` | **tokenisation** (enclitique) |
| r309 | reel SUB | `qu'il viendra` → `viendra` / `Peut-être` | absente + pseudo-GV du S |
| s041 | synth GP | `devant elles` → `marche` / *(vide)* | cible vide + verbe hors lexique |
| s108 | synth GP | `sous le nuage` → `rêve` / `papier` | mal choisie + POS (papier tagué VERB) |
| s122 | synth GP | `vers les montagne` → `saute` / `papier` | idem s108 |

GP 6 / SUB 2 / REL 0 ; hand 2 / reel 3 / synthétique 3 ; cibles VERB 5 / ADJ 2 / NOUN 1. **0 « autre »**.

\### Règles candidates chiffrées (simulées en mémoire, cumulées)
| règle | répare | portée | gain | exact cumulé |
|---|---|---:|---:|---:|
| R1 lexique `rêver/sauter/marcher` | s108, s122 | 2 | +2 | 139 |
| R2 un GP n'est pas gouverné par un mot de son span | g012, r018 | 2 | +2 | 141 |
| R3 cible vide : génitif → GN gauche ; sinon verbe proche | g002, s041 | 2 | +2 | 143 |
| R4 enclitique `appelle-moi` → `appelle` | r230 | 1 | +1 | 144 |
| R5 ignorer un « GV » mono-token ADV | r309 | 1 | +1 | **145/145** |

**8/8, portée 8, 0 régression** — mais **borne haute sur le même gold** : R3a n'est juste que **2/4** sur ses 4 déclencheurs (s081/s120 attendent le verbe), R4 et R5 ont n=1, R1 est lexicale (formes prises dans le gold). Top-k strict 145/145 seulement si la cible réparée est aussi ajoutée aux candidats
… [805 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-echecs-v2.md` | 1 | 7 |

### Commandes exécutées (échantillon)

- **T1** Check git state and reports listing
- **T1** Check key files exist
- **T1** Inspect gold JSON structure
- **T1** Reproduce the 8 attachment failures
- **T1** Rerun reproduction script
- **T1** Locate attachment logic lines
- **T1** Trace S segmentation for the 8 cases
- **T1** Dump predicted segments and gold segments
- **T1** Find lexicon constants and _est_verbe
- **T1** Read lexicons
- **T1** Grep for r230/r309 references
- **T1** Dump 145 label records and base counts
- **T1** Inspect SUB cases with self/non-lexicon cibles
- **T1** Draft simulation (will rewrite)
- **T1** Simulate lexicon and GV completion variants
- **T1** Simulate the four fallback rules sequentially
- **T1** Simulate refined rules sequentially
- **T1** Check _tete_texte behavior on governing GVs
- **T1** Run final rule sequence with R-E head fix
- **T1** Count rule triggers over all 239 gold targets
- **T1** Inspect other de-GP segments
- **T1** Inspect S attachments for GP de/du cases
- **T1** Run official evaluator to confirm base numbers
- **T1** Run negative controls for the rules
- **T1** Inspect N4 self-attachment types and N6 precision
- **T1** Compare gold POS and heuristic POS on the 8 cases
- **T1** Check date, recent reports and JSON keys
- **T1** Inspect topk diagnostic JSON schema
- **T1** Read random baseline control
- **T1** Final cumulative simulation with lexicon retained
- **T1** Check doc review constraints on reports
- **T1** Show heuristic tokenization for r230/r309
- **T1** Generate reports/pensee-echecs-v2.json
- **T1** Verify counts and lexical facts
- **T1** Check R2 scope on s022
- **T1** Measure R2 applied to all types
- **T1** Locate typos and claims to fix
- **T1** Fix JSON typo, counts and 4/4 claim
- **T1** Validate JSON, links, and git status
- **T1** Final JSON consistency edits
- … et 1 autres

## 4. Mesures et résultats marquants

- **T1** `reports/rapport-annotation-independante.md:31:   (`r293`, `s052`, `r230`). Au span exact, il est juste **10/12 = 83,3 %**, cohérent avec le gold entier`
- **T1** `22:**145/239 = 0,6067**. Les 8 échecs = **5,52 %** des 145, **3,35 %** des 239.`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : [  {   "regle": "R-A lexique verbal",   "portee": 2,   "gagne": 2,   "perd": 0,   "exact": 139,   "touches": [    [     "s108",     "papier",     "rêve"    ],    [     "s122",     "papier",     "saute
- **T1** : base exact: 137 N3 split any hyphen: portee 2 gagne 1 perd 0 touches [('r230', 'appelle-moi', 'appelle'), ('r309', 'Peut-être', 'Peut')] [stderr] Traceback (most recent call last):   File "/tmp/ech/co


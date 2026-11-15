# Session session- — Protocole d'annotation or de rôles S

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-c6d0e659-7d2e-4d23-a2b4-d50387bb6f61` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 12:40 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 97 |
| Appels d'outils | 102 |
| Fichiers touchés | 3 |
| Commandes | 99 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche X2 (J4 matin, la part du pilote) : le protocole d'annotation de l'**or de rôles** pour S — les champs (phrase, cadre, rôles : agent/prédicat/lieu/temps/destinataire/possession/complément), la **double annotation** (deux codeurs, le kappa), les 144 rôles existants du gold S (61 phrases / 144 rôles), le **gold v2 (46)** comme base de départ, et le contrôle négatif (l'or permuté doit s'effondre … [144 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche X2 (J4 matin, la part du pilote) : le protocole d'annotation de l'**or de rôles** pour S — les champs (phrase, cad … [424 caractères tronqués]

*102 appels d'outils.* Actions notables :

- bash — List repository root, reports, data
- bash — Read current state document
- bash — Find role/gold reports
- bash — Find gold files
- bash — Read S role analyzer report
- bash — Read restitution v3 and gold v2 JSON
- bash — Search for task references
- bash — Inspect gold S JSON structure
- bash — Read week 2 plan
- bash — Read rest of v3 report and JSON
- bash — List schema/protocol JSONs and read restitution v3
- bash — Inspect gold S and role counts
- bash — Compute gold S role stats
- bash — Search kappa and inspect protocol/schema style
- … et 88 autres

**Synthèse produite :**

Livré.

**Fichiers**
- [`reports/rapport-or-roles-protocole.md`](reports/rapport-or-roles-protocole.md) — le protocole, l'inventaire, le kappa, l'or permuté.
- [`reports/rapport-or-roles-protocole.json`](reports/rapport-or-roles-protocole.json) — les mêmes chiffres, SHA-256, simulations et contrôles.
- [`reports/schema-or-roles.json`](reports/schema-or-roles.json) — schéma Draft 2020-12 des records `phrase / cadres / 7 rôles`.
- [`reports/or-roles-base-v1.json`](reports/or-roles-base-v1.json) — la graine des 46 textes v2 (provisoire, **pas un gold**).
- [`tools/protocole_or_roles.py`](tools/protocole_or_roles.py) — script reproductible, lecture seule du gold S.

**Les chiffres**
- Gold S : **61 phrases / 144 rôles / 17 étiquettes** ; **117** se projettent dans les 7 champs, **27** restent `hors_champ` (`patient`, `qualite`, subordonnées).
- Gold v2 : **46 textes / 65 variantes** ; **78 rôles** non vides dans la première variante ; **3/7** champs.
- Base commune : **222 mentions** dont **195** dans les 7 champs ; rôles rares : `temps` 9, `destinataire` 5, `possession` 1, `complement` 7.
- Supplément prévu : **60 phrases / 90 mentions** → **312 mentions** (285 dans les 7 champs + 27 `hors_champ`) ; chaque rôle à **20–29**.
- Kappa simulé à 90 % d'accord : **0,857** [0,802 ; 0,915] sur la base, **0,878** [0,836 ; 0,914] après supplément. À 85 % : **0,786** / **0,818**.
- Contrôles négatifs : gold S cinq rôles **0/18** ; tous rôles **0,4028** (borne haute, à cause de l’alias `predicat`/`prédicat`) ; rôle constant **3/18, F1 0,037** ; gold v2 cinq rôles **0/6** `lieu`, **37/77**, F1 0,5139.
- Schéma : **46 items validés, 0 erreur** ; **4/4** mutations refusées (sans agent, deux principaux, span faux, sans prédicat).

**Gold S intact**
SHA-256 `4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879` avant et après ; sous-module `tools/structures` propre.

**Validation**
`python3 tools/protocole_or_roles.py` et `--verifier` passent ; `porte-tableaux.sh` passe ; la revue de documentation ne signale que les **2 compteurs** de `en-cours.md` (755 → 756 fiches, 848 → 851 JSON), à mettre à jour par le principal. Les fichiers sont écrits mais non commités.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/schema-or-roles.json` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/protocole_or_roles.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-or-roles-protocole.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repository root, reports, data
- **T1** Read current state document
- **T1** Find role/gold reports
- **T1** Find gold files
- **T1** Read S role analyzer report
- **T1** Read restitution v3 and gold v2 JSON
- **T1** Search for task references
- **T1** Inspect gold S JSON structure
- **T1** Read week 2 plan
- **T1** Read rest of v3 report and JSON
- **T1** List schema/protocol JSONs and read restitution v3
- **T1** Inspect gold S and role counts
- **T1** Compute gold S role stats
- **T1** Search kappa and inspect protocol/schema style
- **T1** Inspect task plan JSON around X2
- **T1** Check git status and submodules
- **T1** Check Python libs and schema validators
- **T1** Read rest of restitution v3 and driver
- **T1** Compute gold v2 stats
- **T1** List gold v2 place mentions and empties
- **T1** Inspect restitution v2 comparison logic
- **T1** Inspect reports index and doc review
- **T1** Read result and filing method docs
- **T1** Check current date
- **T1** Inspect doc review navigation checks
- **T1** Inspect orphan check
- **T1** Run v3 gold S controls read-only
- **T1** Run v3 bank controls
- **T1** Inspect control structure
- **T1** Inspect base controls exact numbers
- **T1** Inspect permutation mapping
- **T1** Check v2 role spans are substrings
- **T1** Prototype kappa simulation
- **T1** Recalibrate kappa simulation
- **T1** Simulate kappa for post-supplement distribution
- **T1** Inspect roles_gp definitions
- **T1** Simulate kappa with coarse mapping
- **T1** Patch base key and write order
- **T1** Inspect main
- **T1** Run schema/base verifier
- … et 59 autres

## 4. Mesures et résultats marquants

- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/r`
- **T1** `> de types 54/55** (98,2 %), les **rôles 131/131** (100 %), les **compléments 47/47**, et couvre`
- **T1** `> **1 466/1 475 octets** (99,4 % ; holdout **762/771**, 98,8 %). La **règle de contexte** corrige`
- **T1** `| `dev` | 7 | **7/7** | 229/229 (100 %) | **22/22** | **10/10** |`
- **T1** `| `test` | 16 | **16/16** | 475/475 (100 %) | **40/40** | **19/19** |`
- **T1** `| `holdout` | 32 | **31/32** | 762/771 (98,8 %) | **69/69** | **18/18** |`
- **T1** `| **global** | **55** | **54/55** (98,2 %) | **1 466/1 475** (99,4 %) | **131/131** (100 %) | **47/47** |`
- **T1** `3bvBWgjiDImkfRLBTEXaoyCg9Hh78MoEzgsevfk3qF89VZre9R+1UFG77VTh/dXxgf+4jcizGexaJCPyAppGX44L1hm9O52m6dfvHR3LEkzgR+1e3lDsM/9EZ/NxwzqDYPoSrXOjRH+AbxkOZDkXD1+3wcxR2pNyDf36YZQtHhTf2O8njXc8poP9wX/Mro/q3jt725dP`
- **T1** `-dasharray: 1, 0;"/></marker><g class="root"><g class="clusters"/><g class="edges edgePaths"><path d="M164,97.5L200,97.5" id="my-svg-L_A_B_0" class="edge-thickness-normal edge-pattern-solid edge-thick`
- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `docs/theorie/glossaire/README.md:31:[ALM (Adaptive Logic Module)](entrees/alm.md) · [AVX2 · AVX-512 · SIMD](entrees/avx2-avx-512-simd.md) · [Bande passante (bandwidth)](entrees/bande-passante.md) · [C`
- **T1** `docs/theorie/glossaire/entrees/xeon-e5-2687w-v3-cpu.md:4:> **Fiche glossaire — Xeon E5-2687W v3 · CPU.** Le processeur du banc : 2 sockets × 10 cœurs (40 fils logiques), 125 Go de RAM, jeu d'instructi`
- **T1** `docs/theorie/glossaire/index.json:1466:      "resume": "Le processeur du banc : 2 sockets × 10 cœurs (40 fils logiques), 125 Go de RAM, jeu d'instructions AVX2. Toutes les mesures « CPU » du dépôt son`
- **T1** `docs/implantation/contexte-long.md:14:> NVMe à ~3,5 Go/s, 20 cœurs Haswell AVX2).`
- **T1** `docs/implantation/contexte-long.md:370:est **déjà vectorisé AVX2** et le coût par expert (4,4 Mo) est faible : le`
- **T1** `reports/rapport-mur-memoire-4bits.md:187:restait que le SIMD. En AVX2 + FMA, 32 éléments par tour : **×3,3**.`
- **T1** `reports/rapport-materiel-disque-ou-cpu.md:56:  AVX2+FMA du produit scalaire (`DRAVE_SIMD_DOT=1`, ×2,06 sur la passe) — un gain`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `| [rapport-a83d-lot-threads.md](rapport-a83d-lot-threads.md) | A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread |`
- **T1** `| [rapport-autotest-parallele.md](rapport-autotest-parallele.md) | B13 — la vérification parallèle : 183/183 en 1 min 54 (×2,4) |`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `kappa  : base 90% -> 0.8572, après supplément -> 0.8778`
- **T1** `verdict Protocole livré : 61 phrases / 144 rôles S se projettent en 117 mentions des sept champs et 27 hors_champ ; avec les 46 textes v2, la base donne 222 mentions, dont 195 dans les sept champs ; l`
- **T1** `1047:    print(f"   kappa  : base 90% -> {simulations['base']['cibles'][2]['kappa_moyen']}, "`
- **T1** `"couverture": "100 % des 167 items, deux codeurs, soit 334 annotations.",`
- **T1** `> le kappa simulé à 90 % d'accord passe de **0,857** à **0,878**, et l'or permuté existant`
- **T1** `reports/rapport-or-roles-protocole.json:8: "verdict": "Protocole livré : 61 phrases / 144 rôles S se projettent en 117 mentions des sept champs et 27 hors_champ ; avec les 46 textes v2, la base donne `
- **T1** `Protocole livré : 61 phrases / 144 rôles S se projettent en 117 mentions des sept champs et 27 hors_champ ; avec les 46 textes v2, la base donne 222 mentions, dont 195 dans les sept champs ; le protoc`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : patched [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/protocole_or_roles.py", line 1014, in <module>     raise SystemExit(main())           


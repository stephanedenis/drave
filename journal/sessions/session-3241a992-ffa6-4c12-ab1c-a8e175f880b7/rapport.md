# Session session- — Preuves CIC : vérification et rapport

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-3241a992-ffa6-4c12-ab1c-a8e175f880b7` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 03:55 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 105 |
| Appels d'outils | 129 |
| Fichiers touchés | 8 |
| Commandes | 83 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche B3 : le corpus d'or CIC (42 verdicts, 42/42 reproduits en J12.2) — étends le vérificateur : les 36 preuves altérées sont rejetées ; ajoute la vérification du **type de Bruijn** et le sha256 indépendant rejoué par une seconde implémentation ; fiche `reports/rapport-cic-v2.md` + JSON.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche B3 : le corpus d'or CIC (42 verdicts, 42/42 reproduits en J12.2) — étends le vérificateur : les 36 preuves altérée … [169 caractères tronqués]

*129 appels d'outils.* Actions notables :

- bash — Inspect repo root and git state
- bash — List key directories
- bash — Find CIC references
- bash — Find de Bruijn references
- bash — Find J12 references
- read
- bash — Inspect existing CIC result JSON
- bash — Inspect gate, manifest, corpus entries
- bash — Find B3 task references
- bash — Find CIC in planning docs
- bash — Read B3 task definition from plan
- bash — Read roadmap and current state around CIC
- bash — Locate Panini source implementation
- bash — Inspect entry schema
- … et 98 autres

**Synthèse produite :**

**B3 terminée et committée** — `2067a6f0`.

\## Ce qui a été ajouté au vérificateur

**1. Vérification du type de de Bruijn** (`tools/verificateur_cic.py`)
- portée purement structurelle : aucun `var i` hors des lieurs ouverts ;
- bien-formedness : `[] ⊢ type : sort n` ;
- une preuve n'est acceptée que si son type est clos et bien formé.

**Résultat** : **42/42** types clos et bien formés (**38** en `sort 0`, **4** en `sort 1`), **42/42** preuves closes.

**2. Seconde implémentation de SHA-256**
- FIPS 180-4 réécrite dans le module, **sans `hashlib`** ;
- **16** vecteurs (FIPS + longueurs de rembourrage) ;
- rejeu du sha256 du fichier, des **42** couples `preuve || type` et des **24** termes de l'environnement ;
- **0 écart** avec `hashlib` et avec les empreintes déclarées.

**3. Contrôles négatifs étendus**
- **36/36** preuves altérées rejetées ;
- **42/42** types altérés rejetés — dont **36** types devenus invalides et **6** rejets par la preuve ;
- **1 020/1 020** mutations de `eq(2,2)` rejetées ;
- corpus corrompu (preuve **ou** type) refusé en code **1**.

\## Porte et tests
`bash tools/porte-cic.sh` : ✅ verte
- **21** tests J12.2 + **17** tests B3 = **38** cas.

\## Livrables
- Fiche : [`reports/rapport-cic-v2.md`](reports/rapport-cic-v2.md)
- JSON : [`reports/cic-verificateur-v2.json`](reports/cic-verificateur-v2.json)
- Code : [`tools/verificateur_cic.py`](tools/verificateur_cic.py), [`tools/porte-cic.sh`](tools/porte-cic.sh), [`tools/tests/test_verificateur_cic_v2.py`](tools/tests/test_verificateur_cic_v2.py)
- État et roadmap mis à jour (`docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`), récit dans `journal/2026-11-15/README.md`.

Les modifications préexistantes hors B3 (autres rapports, `tools/chantier/plan.json`) n'ont pas été touchées.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py` | 0 | 9 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_verificateur_cic_v2.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-cic.sh` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cic-v2.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/cic/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 7 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Inspect repo root and git state
- **T1** List key directories
- **T1** Find CIC references
- **T1** Find de Bruijn references
- **T1** Find J12 references
- **T1** Inspect existing CIC result JSON
- **T1** Inspect gate, manifest, corpus entries
- **T1** Find B3 task references
- **T1** Find CIC in planning docs
- **T1** Read B3 task definition from plan
- **T1** Read roadmap and current state around CIC
- **T1** Locate Panini source implementation
- **T1** Inspect entry schema
- **T1** Find CIC files in Panini
- **T1** Find CIC files in Panini-Research
- **T1** Find CIC generation/type docs in Panini
- **T1** Find Panini CIC kernel API
- **T1** Inspect hash/type functions in Panini kernel
- **T1** Read Panini serialization/hash
- **T1** Inspect Panini golden corpus generator
- **T1** Search for v2/hardening hints
- **T1** Inspect report naming and index
- **T1** Compute proof byte totals
- **T1** Test inferring types of all declared types
- **T1** Check closedness of all terms
- **T1** Check inferability of accepted proofs
- **T1** Check defs/consts well-formedness
- **T1** Inspect documentation review tools
- **T1** Test whether mutated types still accepted
- **T1** Inspect roadmap B section
- **T1** Read en-cours structure
- **T1** Inspect journal date folder and current date
- **T1** Read journal conventions
- **T1** Locate functions after insertion
- **T1** Compile and run verifier without controls
- **T1** Test pure SHA-256 self-test
- **T1** Run verifier with all controls
- **T1** Run new B3 tests
- **T1** Run existing J12.2 tests
- **T1** Run CIC gate with new checks
- … et 43 autres

## 4. Mesures et résultats marquants

- **T1** `6560a0a5 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612)`
- **T1** `2d7a7f2b 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5)`
- **T1** `ce7241d5 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:11929:TOKENIZER RUST LIVRÉ — /home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/tokenizer.rs (371 lignes, 14 Ko, sha256 b7`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:11956:**Fichier livré** : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/tokenizer.rs` — **371 lignes**, 14 Ko, `sha2`
- **T1** `journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/rapport.md:50:**Fichier livré** : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/tokenizer.rs` — **371 lignes**, 14 Ko, `sha256`
- **T1** `journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/digest.md:1083:- **send_message** `{"agent_id": "22bcae27-254b-47b2-acda-87467dab060c", "message": "TOKENIZER RUST LIVRÉ — /home/stephane/Data13TB`
- **T1** `journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/digest.md:1093:**Fichier livré** : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/tokenizer.rs` — **371 lignes**, 14 Ko, `sha25`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:10982:- **T1** : 511 tokens notés — perplexité cumulée 247.031  (4.9 tok/s) === perplexité 247.0308 sur 511 tokens (0 événements, 104.5`
- **T1** `sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur`
- **T1** `contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même`
- **T1** `tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à`
- **T1** `**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction`
- **T1** `d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:2283:| **0.3 codec de référence** | `tools/flux_codec.py` — la **seconde implémentation** du format DRVF | aller-retour **IDENTIQUE** s`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:22039:| **0.3 codec de référence** | `tools/flux_codec.py` — la **seconde implémentation** du format DRVF | aller-retour **IDENTIQUE** s`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `| [rapport-a83d-lot-threads.md](rapport-a83d-lot-threads.md) | A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread |`
- **T1** `| [rapport-autotest-parallele.md](rapport-autotest-parallele.md) | B13 — la vérification parallèle : 183/183 en 1 min 54 (×2,4) |`
- **T1** `| **A2** | placer sur une machine : [KV](../theorie/glossaire/entrees/kv.md) paginé, [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md), [top-k](../theorie/glossaire/entrees`
- **T1** `| **A5** | formats, matériels, énergie : SIMD, PTX, FPGA, KV | ✅ / 🧱 | **A5.4 bloqué** (FPGA) ; le 8 bits tardif est gratuit (+0,03 %) |`
- **T1** `| **A8** | l'ordonnanceur place **et** perte : `choisir_avec_perte` | ✅ **opt-in** ; 6 portes épinglées, A8.3 **échoue** (−5,9 % … +19,5 %) | **A8.3c/d** : le lot change la PPL, pas les threads ; rédu`
- **T1** `| **B5** | la sémantique des jeux : contrat [RSN-jeu](../theorie/glossaire/entrees/rsn-jeu.md), cinq niveaux, bruit | ✅ | aucune — 112 items, **100 %** au niveau 4 |`
- **T1** `| **B6** | la logique dans la pensée : règles, recherche, cartes, invariance | ✅ | aucune — perft, **3/3** mats, dames **20/20**, cartes **79,7 %** |`
- **T1** `| **B8** | les maîtres : 17 principes, 9 sources, livre, parties | ✅ | aucune — livre **10/10**, go 9×9 **10/10** contre 3/10, cartes **44,7 %** |`
- **T1** `| **B11** | la base d'universaux typés : schéma, [parseur](../theorie/glossaire/entrees/parseur.md), codec, contexte | ✅ | **B11.10 close** (cartes, ambiguïtés refusées) ; le codec lit **100 %** |`
- **T1** `| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** +`
- **T1** `| **C3.2** | les modules par famille de langues | ✅ | aucune — **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤ 0,5 %** |`
- **T1** `**Ce qui compte pour R** : le **codec classique** lit **100 %** des surfaces ; c'est la preuve qu'un bloc`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet`
- **T1** `48:**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (has`
- **T1** `189:   suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du pla`
- **T1** `207:[B1–B12] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `208:[B10.2bis] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `209:[B10.3] lasts 2 days and is 15% complete and is colored in #b03a2e`
- **T1** `210:[B11.10] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `282:| **B11** | la base d'universaux typés : schéma, [parseur](../theorie/glossaire/entrees/parseur.md), codec, contexte | ✅ | **B11.10 close** (cartes, ambiguïtés refusées) ; le codec lit **100 %** |`
- **T1** `284:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `359:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **5`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canoniq`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `64 39 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 c`
- **T1** `93 33 - **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœ`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : ❌ 1 tableau(x) ne rendront pas (mistune refuse le tableau ENTIER) :      reports/rapport-cic-v2.md:174 — 4 cellules ≠ 2 attendues [stderr]   1813 fichier(s) examiné(s) [exit code: 1]
- **T1** : en-cours · 1698 mots · 7 sections · 4 session(s) · 11 puces · 5 questions   ❌ 1 anomalie(s) :      · 11 puces dans « Ce qui est en cours » > 10 [exit code: 1]
- **T1** : budget de contexte · documents chargeables     mots lignes  cat budget  document     9133    500   T1   9000  docs/pilotage/roadmap.md     5999    597 DATÉ      0  docs/implantation/contexte-long.md  
- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r

## 6. Commits

- B3 — LE CORPUS D'OR CIC V2 : 42/42 TYPES DE BRUJIN BIEN FORMÉS, 42/42 SHA256 PAR DEUX IMPLÉMENTATIONS, 36/36 PREUVES ET 42/42 TYPES ALTÉRÉS REJETÉS" -m "Le corp


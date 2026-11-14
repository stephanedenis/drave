# Session session- — Rapport de semaine et suivi J5.1

> **Journaux :** [le jour](../../2026-11-13/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-e8c327f2-a7ec-464a-8e40-0615e5befecb` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-13 22:59 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 98 |
| Appels d'outils | 115 |
| Fichiers touchés | 5 |
| Commandes | 73 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J5.1 : le rapport de semaine — relis les fiches des jours 1 à 4, écris `reports/rapport-semaine.md` + JSON : les chiffres avant/après (POS, F1, attachement, le produit, l'intégration), les décisions, les rejets, ce qui reste. Mets à jour `docs/pilotage/semaine-autonome.md` (l'état de chaque jour).

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J5.1 : le rapport de semaine — relis les fiches des jours 1 à 4, écris `reports/rapport-semaine.md` + JSON : les c … [184 caractères tronqués]

*115 appels d'outils.* Actions notables :

- bash — Explore workspace root and reports
- bash — Read semaine-autonome state file
- bash — List recent report markdown files
- bash — List most recent reports directory entries
- read
- bash — Search for existing weekly report references
- bash — Inspect reports README and INDEX head
- bash — Read results method doc
- bash — Read filing method doc
- bash — Inspect JSON top-level keys
- bash — Inspect integration JSON top-level keys
- bash — Check git status and HEAD
- bash — Find counters and week mentions in en-cours
- bash — Read en-cours top sections
- … et 84 autres

**Synthèse produite :**

\## J5.1 — fait

**Livrables**
- [`reports/rapport-semaine.md`](reports/rapport-semaine.md) — le rapport consolidé J1→J4.
- [`reports/rapport-semaine.json`](reports/rapport-semaine.json) — la version machine (13 décisions, 21 rejets, 12 restes, chronologie, limites).
- [`docs/pilotage/semaine-autonome.md`](docs/pilotage/semaine-autonome.md) — l'état de chaque jour (§ 8) + le § 3 bis mis à jour.
- [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) — compteurs **718 / 812**, lignes J5.1 et coordination J4.
- [`reports/README.md`](reports/README.md) et [`reports/INDEX.md`](reports/INDEX.md) — fiches courantes et index régénéré.
- Les fiches J4 N2/S/A non committées ont été emportées avec le rapport.

**Commit** : `34e3e4ab` — *J5.1 — LE RAPPORT DE SEMAINE : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 237, TAGGER 0,9475 (+8,49, INTÉGRER), INTÉGRATION BORNÉE (TABLE 14/14, CORPUS 418/438), 13 DÉCISIONS, 21 REJETS*.

**Les chiffres avant/après**
- **POS** : **0,8625 → 0,8625** (heuristique de production, 0 jeton changé) ; le **tagger API** mesure **0,9475** (**+8,49 pts**, IC95 [+7,23 ; +9,74]), décision **intégrer**, mais **non branché** ; réserve : réel 432 seul **+4,67 pts**.
- **F1** : **0,7533 → 0,7902** (**+0,0369**) ; dev **0,7875**, test **0,7962** ; vue linéaire **0,8120 → 0,8144**.
- **Attachement** : exact **236/237 → 237/238** ; couverture **0,9916 → 0,9958** ; 0 cible perdue.
- **Le produit** : schéma **v2** (26 cas / 0 échec, v1 lue, 1 836 annotations / 0 échec) ; restitution **46/46** surfaces, miroir strict **0,1087**, contrôle négatif 46/46.
- **L'intégration** : table **14/14** (hypothèse, pas mesure) ; corpus **21 textes / 418 sur 438** (95,4 %, 8/8 contrôles) ; retrieval **script +0,609**, famille +0,181, **date −0,034/siècle (p = 0,19)**, 0,710 vs 0,710 à script contrôlé ; généalogie **154/154 hors script au hasard**, couverture **5/21 / 15/21 / 21/21**, R² **0,256 / 0,230**.
- **Coordination J4** : N2 **8,0225 → 2,9726/2,7856** (`--rope --canal-dir`) ; S **11 verdicts** (7 acceptés / 4 exclus ; clone 8/4/11) ; R **0,9475** ; A6.2 **libre** (MoE 18,56 Go, PPL 37,2013, porte 54,5202), A8.3b2 hors graphe.

**Vérifications** : JSON valide ; `revue_documentation.py` ✅ ; `porte-tableaux` + liens ✅ ; `verifie_en_cours.py` ✅ ; `taille_documents` **3 999 / 4 000** ; `verifie_journal.py` ✅.

**Ce qui reste** : **J5.2** (passe complète, revue, tag annoté, release) ; `g017` et l'objet du GV ; le split réel du tagger ; la signature V14 des 21 langues ; la
… [294 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.json` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 15 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Explore workspace root and reports
- **T1** Read semaine-autonome state file
- **T1** List recent report markdown files
- **T1** List most recent reports directory entries
- **T1** Search for existing weekly report references
- **T1** Inspect reports README and INDEX head
- **T1** Read results method doc
- **T1** Read filing method doc
- **T1** Inspect JSON top-level keys
- **T1** Inspect integration JSON top-level keys
- **T1** Check git status and HEAD
- **T1** Find counters and week mentions in en-cours
- **T1** Read en-cours top sections
- **T1** Count reports md and json files
- **T1** Compare committed counters and committed file counts
- **T1** Run documentation review tool
- **T1** Count committed top-level report files
- **T1** Count committed reports directory entries
- **T1** List commits during the week
- **T1** Show current date and time
- **T1** Extract r035 JSON figures
- **T1** Extract convention GV JSON figures
- **T1** Extract schema v2 validation figures
- **T1** Extract restitution v0 synthesis
- **T1** Extract atoms table status and calibration
- **T1** Extract common corpus statistics
- **T1** Extract retrieval JSON key figures
- **T1** Extract genealogy JSON verdict sections
- **T1** Extract J4 coordination JSON verdicts
- **T1** Show semaine-autonome structure
- **T1** Read an existing multi-day report for style
- **T1** Inspect state freshness checker and pre-commit hook
- **T1** Inspect table gate rules
- **T1** Inspect report index generator
- **T1** Check README for coordination entries
- **T1** Validate weekly report JSON
- **T1** Run table gate on reports
- **T1** Check en-cours word budget and current state
- **T1** Check which coordination files are tracked
- **T1** Regenerate and verify reports index
- … et 33 autres

## 4. Mesures et résultats marquants

- **T1** `(R² 0,30) — la surface capte l'époque ; tout test de style contrôle la date, tout test de famille`
- **T1** `| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 niveaux |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir 0,2276 |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | **B13** — POS **83,83 %** (R2a/R3/R2b), F1 **0,6181** |`
- **T1** `| [`rapport-autotest-parallele.md`](rapport-autotest-parallele.md) | **B13** — l'autotest parallèle : **183/183 en 1 min 54** (×2,4), mêmes verdicts |`
- **T1** `| [`rapport-cache-chunker.md`](rapport-cache-chunker.md) | **B13** — la validation A11 du cache : ×11,0 à 160 tokens, égalité 612/612, cache falsifié détecté |`
- **T1** `| [`rapport-cache-chunker-applique.md`](rapport-cache-chunker-applique.md) | **B13** — le cache appliqué : **×139** en chunker, ×1 en défaut (S domine), sortie identique, **181/181** |`
- **T1** `| [`rapport-cout-chunker.md`](rapport-cout-chunker.md) | **B13** — le coût du chunker : O(n²) confirmé, cache ×11,6 à 160 tokens |`
- **T1** `| [`rapport-pensee-cible-proximite.md`](rapport-pensee-cible-proximite.md) | **B13** — la cible par proximité : exact 0,0042 → **0,0544** (×13), top1 0,3975, **164/164** |`
- **T1** `| [`rapport-pensee-oubli.md`](rapport-pensee-oubli.md) | **B13** — la mémoire courte : Q × 0,9/10, 20/20, 10,0 pas, **71/71** |`
- **T1** `| [`rapport-pensee-ultra-rare.md`](rapport-pensee-ultra-rare.md) | **B13** — l'information ultra-rare : utile 0,1 %, 4 looks, v final 0,44, 20/20, **68/68** |`
- **T1** `| [`rapport-pensee-tres-rare.md`](rapport-pensee-tres-rare.md) | **B13** — l'information très rare : utile 1 %, v final 0,54, 20/20, 8,0 pas, **67/67** |`
- **T1** `| [`rapport-pensee-rare.md`](rapport-pensee-rare.md) | **B13** — l'information rare : utile 10 %, v final 0,8, 20/20, 8,0 pas, **66/66** |`
- **T1** `| [`rapport-pensee-rupture.md`](rapport-pensee-rupture.md) | **B13** — la rupture : 90 % d'erreur, v final 0,12, 20/20, 8,0 pas, **57/57** |`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `| [rapport-a83d-lot-threads.md](rapport-a83d-lot-threads.md) | A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread |`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `48:- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV +`
- **T1** `| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **1 024 octets entraînés** ; **2 048** fini (2×10 000 pas) ; la restitution |`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `9c7f71dc 2026-11-07 PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`
- **T1** `26c7b7ab 2026-11-07 ROADMAP ET JOURNAL — LA NUIT FINIT À F1 0,7535, POS 86,25 %, 236/237, COUVERTURE 0,9916 ; LA CONVENTION DU SUJET`
- **T1** `5a067ba5 2026-11-06 ROADMAP ET JOURNAL — LA NUIT FINIT À 236/237, COUVERTURE 0,9916, POS 86,25 %, 2 SPANS ; r264 RÉGLÉ`
- **T1** `ba42d4cc 2026-11-06 FICHE — LES TROIS RÈGLES REJETÉES (PARTICIPES, R4-FR GÉNÉRIQUE, PARTICIPE APRÈS AVOIR) ; POS RESTE À 86,25 %`
- **T1** `c43dd5cc 2026-11-06 B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `6432bdb9 2026-11-06 JOURNAL ET ROADMAP — LA NUIT DES ÉTATS : N2/S/R/A INVENTORIÉS, FRONTIÈRE CORRIGÉE (A6.2 LIBRE), POS 85,84 %, PONCT, R4-FR ; ÉTAT HORODATÉ`
- **T1** `6b976cb1 2026-11-06 B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `=== convergence : [{"constat": "La surface passe avant la filiation, des deux côtés.", "preuve": "Panini §150 : β époque 0,1378 > β filiation 0,0489 (R² 0,30). Drave : le script est une porte (154/154`
- **T1** `chiffres : {"propre512_8k": {"protocole": "validation data/corpus_propre/val.txt, fenêtres Van der Corput dans les chunks de 8192, 8 lots × 16 fenêtres", "courbes": {"absolu_sans_canal": {"128": 8.022`
- **T1** `> **hétérogène** (`corpus_en`, dispersion ×2,9 — `rapport-consolidation-structure-partagee.md`) —`
- **T1** `> tenu à l'écart.** Jour 1 : m30 **−0,92 %** ✓. Jours **2 et 3** : **aucune époque n'améliore la`
- **T1** `> validation**, donc le protocole **rend le modèle inchangé** (0,00 %, au chiffre près) — un`
- **T1** `> l'écart **monte** (m30 **+0,36 %**, m0 **+0,61 %**).`
- **T1** `> et elle est étiquetée comme telle) · LoRA rang 8 sur les 8 premières couches.`
- **T1** `| **jour 1** | m0..m4 | 1 | **22,9422** | **−0,92 %** | 23,0310 | −6,89 % *(mémorisation)* |`
- **T1** `| **jour 2** | m5..m9 | **0 — REFUSÉ** | 22,9422 | **0,00 %** | 23,0310 | 0,00 % |`
- **T1** `| **jour 3** | m10..m14 | **0 — REFUSÉ** | 22,9422 | **0,00 %** | 23,0310 | 0,00 % |`
- **T1** `| **jour 4** | m15..m19 | 1 | **23,0236** | **+0,36 %** | 23,1724 | +0,61 % |`
- **T1** `* **et la journée acceptée DÉGRADE le texte tenu à l'écart** (+0,36 % sur m30, +0,61 % sur m0) :`
- **T1** `« structure partagée », où la colonne « validation » gagnait −3,6 % sans que le test gagne rien) ;`
- **T1** `* **le contraste avec wikitext2 est total** : là, une nuit donne −7,9 % et une deuxième +0 % ; ici,`
- **T1** `**une journée sur quatre sert**, pour −0,9 %. Ce n'est pas le mécanisme qui change, c'est le`
- **T1** `(dispersion ×2,9) ;`
- **T1** `-| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **1 024 octets entraînés** ; **2 048** fini (2×10 000 pas) ; la restitution |`
- **T1** `+| **J2** | après-midi : corpus commun | ✅ fait | **21 textes**, 5 familles, 10 écritures, **418/438** paires exactes (95,4 %), 8/8 contrôles | `c3467170` (avec J3.1) | corpus multi-époques / multi-ge`
- **T1** `30:| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; `
- **T1** `38:**État au 07/11 18 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) rég`
- **T1** `148:| **A2** | placer sur une machine : [KV](../theorie/glossaire/entrees/kv.md) paginé, [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md), [top-k](../theorie/glossaire/ent`
- **T1** `180:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `255:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du plancher 1`
- **T1** `| **A2** | placer sur une machine : [KV](../theorie/glossaire/entrees/kv.md) paginé, [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md), [top-k](../theorie/glossaire/entrees`
- **T1** `| **A5** | formats, matériels, énergie : SIMD, PTX, FPGA, KV | ✅ / 🧱 | **A5.4 bloqué** (FPGA) ; le 8 bits tardif est gratuit (+0,03 %) |`
- **T1** `| **A8** | l'ordonnanceur place **et** perte : `choisir_avec_perte` | ✅ **opt-in** ; 6 portes épinglées, A8.3 **échoue** (−5,9 % … +19,5 %) | **A8.3c/d** : le lot change la PPL, pas les threads ; rédu`
- **T1** `| S — la banque validée | **`/paragraphes` fini** : 9/9 paragraphes, 19/19 candidats, 11 acceptés, 8 exclus, **11 verdicts non committés** ; **banque 150 verdicts / 74 des 207 phrases** (35,7 %), mais`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : dc78f223 2026-11-13 ÉTAT — T0 DANS LE BUDGET (3 991 MOTS) : LA LIGNE R0.7 PORTE LE TAGGER 612 (0,9475, +8,49, INTÉGRER) a934d779 2026-11-13 R0.7 — LE TAGGER POS SUR LE GOLD 612 : 0,9475 (3012/3179), +

## 6. Commits

- J5.1 — LE RAPPORT DE SEMAINE : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 237, TAGGER 0,9475 (+8,49, INTÉGRER), INTÉGRATION BORNÉE (TABLE 14/14, CORPUS 418/438), 13 


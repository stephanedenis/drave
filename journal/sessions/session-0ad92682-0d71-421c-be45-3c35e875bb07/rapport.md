# Session session- — Clôture T6 : rapport bilan et mise à jour roadmap

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-0ad92682-0d71-421c-be45-3c35e875bb07` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 23:33 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 99 |
| Appels d'outils | 146 |
| Fichiers touchés | 6 |
| Commandes | 95 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche T6 (clôture) : le bilan — relis les fiches T1-T5, écris `reports/rapport-bilan-exploitable.md` + JSON : ce qui est désormais installable, le quickstart, l'API du JSON, la performance, les codes de sortie ; les négatifs ; ce qui reste (le gold de S, les signatures de Panini, la décision du tagger `auto`) ; mets à jour `docs/pilotage/en-cours.md` et la roadmap. **Ne relance pas la passe complè … [26 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche T6 (clôture) : le bilan — relis les fiches T1-T5, écris `reports/rapport-bilan-exploitable.md` + JSON : ce qui est … [306 caractères tronqués]

*146 appels d'outils.* Actions notables :

- bash — List workspace and work/portes
- bash — List reports and pilotage docs
- bash — Find T1-T5 fiches
- bash — Inspect work/portes contents
- bash — Find docs mentioning T1-T5
- bash — List newest report md and chantier
- bash — Search T-task references in pilotage
- bash — Read en-cours beginning
- bash — Preview T1-T5 headers and JSONs
- bash — Git log and status
- read
- bash — Inspect T1-T5 JSON structure
- bash — Find latest gate run directories
- bash — Find registre files and recent work
- … et 119 autres

**Synthèse produite :**

**T6 est clos.** Commit `83adaa2b` — *T6 — LE BILAN EXPLOITABLE*.

\## Livrables

- **[`reports/rapport-bilan-exploitable.md`](reports/rapport-bilan-exploitable.md)** — la fiche de clôture : installable, quickstart, API JSON, performance, codes de sortie, négatifs, reste.
- **[`reports/rapport-bilan-exploitable.json`](reports/rapport-bilan-exploitable.json)** — schéma `drave.bilan-exploitable`, toutes les mesures et les trois lignes restantes.
- **[`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md)** — T6 clos, 765 fiches / 860 JSON, passe et 86e porte, reste réorganisé.
- **[`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md)** — T6 inscrit, lignes B et R mises à jour, **U1** désignée comme prochaine action.
- **[`journal/2026-11-15/README.md`](journal/2026-11-15/README.md)** — récit T4/T5/T6 ; index [`reports/INDEX.md`](reports/INDEX.md) et [`reports/README.md`](reports/README.md) à jour.

\## Ce que le bilan retient

- **Installable** : `pip install -e .`, `drave 0.1.0`, 8 tests ; sans installation, code **127** propre. Limite : pas de wheel autonome.
- **Quickstart** : **3/3** commandes, JSON v2 **5 899** octets, erreurs **3/4/1**. Le clone public reste dégradé par l’absence de `tools/structures`.
- **API JSON** : **2 139** objets `{span, cible, source}`, **8** rôles normalisés, **0** span faux, v1 toujours lue.
- **Performance** : 10 000 mots en **4,01 s**, **2 493 mots/s**, **126 Mio**, **14,8 Mo** de JSON ; 100 phrases à **1,10 ms**. Le contrôle de linéarité **échoue** : **α = 1,55**, quadratique **R² 0,99995**, coupables `_groupes_partition` / `_cible_proche`.
- **CLI** : **20/20** cas, codes **0/3/4/5/1**, aide **8/8**, `--duree` sans casser le défaut.

\## Portes

Aucune passe complète relancée. Lecture de `work/portes-1115-09h53/registre.txt` : **85 portes, 81 vertes, 4 rouges** ; `sessions` réparée, `indice`, `melange`, `prechargement` tolérées et nommées. Ciblage `work/portes/w6-final/` : **9/9**. Seule la **86e porte** `porte-banc-performance` a été rejouée à part : **verte**, 12 tests.

\## Ce qui reste

- **Le gold de S** : 61 phrases / 144 rôles écrits par les mêmes règles — **144/144** n’est pas un or humain indépendant ; **J4** n’est pas ouvert.
- **Panini** : **26 signatures** V14 manquantes, calibration **42/44**, rejeu **27/60** ; le manifeste et la commande sont prêts, le test attend.
- **`--tagger auto`** : prototype opt-in mesuré (30/30 tests, code 0 dans tous les cas) ; la **décision reste humaine**, le défaut hors ligne est in
… [299 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable.json` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 24 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** List workspace and work/portes
- **T1** List reports and pilotage docs
- **T1** Find T1-T5 fiches
- **T1** Inspect work/portes contents
- **T1** Find docs mentioning T1-T5
- **T1** List newest report md and chantier
- **T1** Search T-task references in pilotage
- **T1** Read en-cours beginning
- **T1** Preview T1-T5 headers and JSONs
- **T1** Git log and status
- **T1** Inspect T1-T5 JSON structure
- **T1** Find latest gate run directories
- **T1** Find registre files and recent work
- **T1** Read latest gate registres and failures
- **T1** Preview registre format
- **T1** Inspect the four red gates
- **T1** Locate T1-T5 references in indexes and roadmap
- **T1** Read roadmap beginning
- **T1** Search gold S and J4
- **T1** Search Panini signatures and tagger auto decisions
- **T1** Read S page measurement report relevant parts
- **T1** Search exact gold S phrasing
- **T1** Read J4 plan and restitution v3 gold S facts
- **T1** Read openings and blocking sections
- **T1** Inspect bilan JSON conventions
- **T1** Check product README codes and quickstart
- **T1** Inspect report JSON schemas
- **T1** Read roadmap T4 section and B13 table row
- **T1** Find T6 task in plan
- **T1** Search T6 in plan JSON
- **T1** Show T6 and following task details
- **T1** Inspect revue_documentation counters
- **T1** Find report index tooling
- **T1** Inspect report nav and counters checks
- **T1** Inspect navigation and counters functions
- **T1** Inspect reports README index format
- **T1** Check T-series entries in reports README
- **T1** Check index_reports tool
- **T1** Check T reports in INDEX
- **T1** Compute current counters and date
- … et 55 autres

## 4. Mesures et résultats marquants

- **T1** `docs/pilotage/roadmap.md:38:**État au 15/11.** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25`
- **T1** `docs/pilotage/roadmap.md:315:| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/r`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `# T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)`
- **T1** `9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** `7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `"langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)",`
- **T1** `"stdout": "drave 0.1.0 — analyse heuristique (CPU, hors ligne)\nlangue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VERB ./PONC`
- **T1** `"stdout": "drave 0.1.0 — évaluation de l'heuristique sur le gold\ngold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement\n\nPOS         exactitude 86.25 %  (fer`
- **T1** `docs/pilotage/roadmap.md:296:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 15/11.** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 23`
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`
- **T1** `canonique**, le strict **5/46** ; temps CLI médian **159,2 ms**, API **2,7 ms**. Comparaison`
- **T1** `sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur`
- **T1** `contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même`
- **T1** `tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à`
- **T1** `**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction`
- **T1** `d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150`
- **T1** `reports/rapport-n2-multilingue-distille.md:11:N2.k avait mesuré la dilution (fr +57 %, en −1,7 PPL face au monolingue) ; N2.n et N2.j4 ont montré`
- **T1** `reports/pensee-gold-anglais.json:1133:  "est_verbe": "83,5 % d'accord avec le POS gold sur les cibles ; 15 FN, 1 FP (flower) ; garder le POS gold comme référence",`
- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `> pour `evaluer` F1 **79,02 %** / attachement **99,58 %** (voir [`README.md`](README.md) § 3.1`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `"controle": "tirage 20261116 : POS 88,13 % contre H50 68,42 % ; H50 ∩ 402 = 0 ; union = 452 ; sha256 avant = après",`
- **T1** `**14,8 Mo** JSON ; 100 phrases **1,10 ms** ; `--tagger` **1,17 s/phrase**.`
- **T1** `**Contrôle de linéarité négatif** : **α = 1,55**, **R² 0,99995** ;`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `| **B5** | la sémantique des jeux : contrat [RSN-jeu](../theorie/glossaire/entrees/rsn-jeu.md), cinq niveaux, bruit | ✅ | aucune — 112 items, **100 %** au niveau 4 |`
- **T1** `| **B6** | la logique dans la pensée : règles, recherche, cartes, invariance | ✅ | aucune — perft, **3/3** mats, dames **20/20**, cartes **79,7 %** |`
- **T1** `| **B8** | les maîtres : 17 principes, 9 sources, livre, parties | ✅ | aucune — livre **10/10**, go 9×9 **10/10** contre 3/10, cartes **44,7 %** |`
- **T1** `| **B11** | la base d'universaux typés : schéma, [parseur](../theorie/glossaire/entrees/parseur.md), codec, contexte | ✅ | **B11.10 close** (cartes, ambiguïtés refusées) ; le codec lit **100 %** |`
- **T1** `| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** +`
- **T1** `| **C3.2** | les modules par famille de langues | ✅ | aucune — **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤ 0,5 %** |`
- **T1** `**Ce qui compte pour R** : le **codec classique** lit **100 %** des surfaces ; c'est la preuve qu'un bloc`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (677 textes), **672 appels réseau**, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `# un passage COURT du banc (1 000 mots, 20 phrases, 3 tailles, bloc ×1/×2/×4) hors ligne.`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `163-**14,8 Mo** JSON ; 100 phrases **1,10 ms** ; `--tagger` **1,17 s/phrase**.`
- **T1** `164-**Contrôle de linéarité négatif** : **α = 1,55**, **R² 0,99995** ;`
- **T1** ``analyser` rend `objet` / `—` au lieu de `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %**`
- **T1** `au lieu de **79,02 %** / **99,58 %**. Le document affiche la sortie réelle du clone et nomme`
- **T1** `63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../report`
- **T1** `132:- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `133:- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `--- W5 — restitution v3 555 nguistique** (398 langues, 0,9687) ; **W2 — tagger 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), fermé 402 −1,55** ([fiche](../../reports/rapport-tagger-h50.md)) ; **W`
- **T1** `--- J4 — l'or de rôles 883 roles-v3` opt-in** ([fiche](../../reports/rapport-restitution-v3.md)) | **R4.4 close** ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; **1 02`
- **T1** `--- T132/T133 -1 | **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (néga`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `**État au 15/11 (nuit).** **T1–T6 — le produit exploitable** : installable, quickstart rejoué, JSON v2, performance mesurée, CLI robuste ; [bilan](../../reports/rapport-bilan-exploitable.md). Semaine `
- **T1** `-| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ;`
- **T1** `+| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ;`
- **T1** `-**État au 15/11.** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 2`
- **T1** `+**État au 15/11 (nuit).** **T1–T6 — le produit exploitable** : installable, quickstart rejoué, JSON v2, performance mesurée, CLI robuste ; [bilan](../../reports/rapport-bilan-exploitable.md). Semaine`
- **T1** `+mots **4,01 s**, **2 493 mots/s**, **126 Mio**, **14,8 Mo**), **CLI** (**20/20**, codes`
- **T1** `+restent : le **clone public** perd `tools/structures` (attachement **88,70 %** au lieu de`
- **T1** `+**99,58 %**), la croissance est **O(k²)** (α = **1,55**), et le **gold de S** n'est pas un or`
- **T1** `**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (238/238 ; [fiche](../../reports/`
- **T1** `171-mots **4,01 s**, **2 493 mots/s**, **126 Mio**, **14,8 Mo**), **CLI** (**20/20**, codes`
- **T1** `174-restent : le **clone public** perd `tools/structures` (attachement **88,70 %** au lieu de`
- **T1** `175-**99,58 %**), la croissance est **O(k²)** (α = **1,55**), et le **gold de S** n'est pas un or`
- **T1** `perplexité 113.0068 · code 0`
- **T1** `| [rapport-consolidation-balayage.md](rapport-consolidation-balayage.md) | Le balayage de la consolidation — un optimum INTÉRIEUR de capacité (rang 4) et de pas (3e-4), qui ne composent PAS |`
- **T1** `| [rapport-consolidation-c7.md](rapport-consolidation-c7.md) | C7 — la consolidation : le rejeu met bien l'expérience dans les poids (−16,4 % en domaine, **+1,3 % hors domaine**) |`
- **T1** `| [rapport-consolidation-structure-partagee.md](rapport-consolidation-structure-partagee.md) | Ce qui se consolide, c'est la STRUCTURE PARTAGÉE — même mémorisation (−22,5 %), transfert −7,4 % ou +1,2 `
- **T1** `| [rapport-elagage-logs.md](rapport-elagage-logs.md) | A6.3 — l'élagage guidé par les logs : aucun neurone ne s'allume jamais, mais 63 % s'allument à peine |`
- **T1** `+| [rapport-performance.md](rapport-performance.md) | T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55) |`
- **T1** `| [rapport-r02-controleur.md](rapport-r02-controleur.md) | R0.2 — le contrôleur de lecture : 100 % de récupération à 30 % du budget |`
- **T1** `| [rapport-s-corpus-reel.md](rapport-s-corpus-reel.md) | S — L'analyseur lit le français propre (65,5 % de GN+GV), pas le CEGEP OCR (8,5 %, plancher du mélange) |`
- **T1** `+**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902**,`
- **T1** `+public** à **88,70 %** d'attachement au lieu de **99,58 %**, croissance **O(k²)** (α = **1,55**),`
- **T1** `[still running after 60000ms; moved to background job bash-92]`
- **T1** `83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module> AssertionError: 2 [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module> ImportError: cannot import name 'poids' from 'taille_documents' (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools

## 6. Commits

- T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC


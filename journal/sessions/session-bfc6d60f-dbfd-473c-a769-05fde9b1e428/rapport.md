# Session session- — Restitution v3 et rôles _role_gp

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-bfc6d60f-dbfd-473c-a769-05fde9b1e428` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 11:05 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 186 |
| Appels d'outils | 230 |
| Fichiers touchés | 10 |
| Commandes | 156 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche W5 (J3 après-midi) : la restitution v3 — `_role_gp` distingue **lieu / temps / destinataire / possession / complément** (des prépositions : `à` + lieu/temps/destinataire, `de` + possession, `avec` + moyen...) ; mesure la **précision et le rappel par rôle** sur le gold v2 (46) et le gold S (61/144 existants), avec le **contrôle négatif** (permuter les rôles doit tuer la mesure). Fiche `report … [94 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche W5 (J3 après-midi) : la restitution v3 — `_role_gp` distingue **lieu / temps / destinataire / possession / complém … [374 caractères tronqués]

*230 appels d'outils.* Actions notables :

- bash — Show repo status and recent commits
- bash — List root and reports directory
- grep
- bash — Read _role_gp implementations
- bash — Find gold and restitution files
- bash — Find restitution references in pilotage docs
- bash — Read restitution v2 report and JSON structure
- bash — Find week plan and gold references
- bash — Inspect working tree changes
- bash — Read week 2 plan
- bash — Inspect gold S structure
- bash — Inspect gold v2 structure
- bash — Count gold S roles and labels
- bash — Read restitution v2 module
- … et 183 autres

**Synthèse produite :**

Les mesures sont stables. J'écris la fiche v3 avec le positif de séparation et le négatif produit.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py` | 1 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py` | 1 | 10 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_restitution_v3.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution_v3.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v3.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 7 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Show repo status and recent commits
- **T1** List root and reports directory
- **T1** Read _role_gp implementations
- **T1** Find gold and restitution files
- **T1** Find restitution references in pilotage docs
- **T1** Read restitution v2 report and JSON structure
- **T1** Find week plan and gold references
- **T1** Inspect working tree changes
- **T1** Read week 2 plan
- **T1** Inspect gold S structure
- **T1** Inspect gold v2 structure
- **T1** Count gold S roles and labels
- **T1** Read restitution v2 module
- **T1** Read rest of generator _role_gp
- **T1** Read rest of restitution_v2.py
- **T1** Read v2 measurement script
- **T1** Inspect GP role call site in bloc_linguistique
- **T1** Read v2 metrics and gold S matcher
- **T1** Read v2 tests
- **T1** Find gold S usage
- **T1** Read gold S matcher implementation
- **T1** History of v2 and role code
- **T1** Check for existing v3 work
- **T1** Look for prior work artifacts
- **T1** Read heuristic analyzer token loop
- **T1** Inspect uncommitted drave.py change
- **T1** Find restituter CLI code
- **T1** Read product README on v2 limitation
- **T1** Show GP/SUB role predictions vs gold S
- **T1** Show v2 lieu predictions on 46 gold
- **T1** Find role assignment in bloc_linguistique
- **T1** Inspect annotations for gold S examples
- **T1** Find role post-processing
- **T1** Find GP role refinement
- **T1** Read analyzer post-processing
- **T1** Read S data builder and attachment role refinement
- **T1** Find S call methods
- **T1** Compute per-role gold S current accuracy
- **T1** Find place/time lexicons
- **T1** Probe current role assignments for prepositions
- … et 116 autres

## 4. Mesures et résultats marquants

- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `docs/pilotage/roadmap.md:38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL `
- **T1** `docs/pilotage/roadmap.md:188:   611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `docs/pilotage/roadmap.md:307:| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne`
- **T1** `docs/pilotage/en-cours.md:49:- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/`
- **T1** `docs/pilotage/roadmap.md:34:| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `-| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ;`
- **T1** `+| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ;`
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `c43dd5cc B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `6b976cb1 B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `7a45325f B13 — LA PONCTUATION A UNE POS (PONCT) : POS 85,00 → 85,75 %, MIROIR 0,196 → 0,2276, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `015d7c56 B13 — LA PARTITION DES SYNTAGMES (P0-3) : meta.alternative PAR DÉFAUT (MESURES INCHANGÉES), filtrer EN OPTION (F1 +0,047) ; outside/feel CORRIGÉS, POS 85,00 %`
- **T1** `5c5d3b52 B13 — LE PAQUET POS SÛR (CLASSES FERMÉES + R4-EN) : POS 83,83 → 84,96 %, 37 CORRIGÉS / 0 CASSÉ, ATTACHEMENT INCHANGÉ ; 183/183`
- **T1** `2ba393b0 B13 — LA POS À 83,83 % (R2a/R3/R2b) : F1 0,5849 → 0,6181, ANGLAIS 0,6341 → 0,7273, ATTACHEMENT INCHANGÉ (222/222) ; 183/183`
- **T1** `POS         exactitude 97.14 % (fermé 94.74 %, ouvert 100.00 %) · Δ +8.57 pts vs heuristique`
- **T1** `SYNTAGMES   F1 90.16 % (tête 97.39 %) — conservés à l'heuristique`
- **T1** `reports/INDEX.md:267:| [rapport-modules-famille.md](rapport-modules-famille.md) | C3.2b — un module de restitution par famille : l'indo-européen recopie à 100 % |`
- **T1** `reports/INDEX.md:536:| [rapport-pensee-miroir-resume.md](rapport-pensee-miroir-resume.md) | B13 — la restitution sémantique : le résumé rappelle 78 % |`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **5`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; **D1–D3**, **E1–E2** livrés ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [er`
- **T1** `- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues (Glottolog **21/21**), **154/154** hors script au hasard, **V14 3/21** ; B2 **négatif** (niveaux non prédits) ; J7.1 famille **6`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet`
- **T1** `288:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `363:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du`
- **T1** `canonique**, le strict **5/46** ; temps CLI médian **159,2 ms**, API **2,7 ms**. Comparaison`
- **T1** `-- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **`
- **T1** `-- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues (Glottolog **21/21**), **154/154** hors script au hasard, **V14 3/21** ; B2 **négatif** (niveaux non prédits) ; J7.1 famille **`
- **T1** `+- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues (Glottolog **21/21**), **154/154** hors script au hasard, **V14 3/21** ; B2 **négatif** (niveaux non prédits) ; J7.1 famille **`
- **T1** `-**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet d`
- **T1** `+**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (238/238 ; [fiche](../../reports`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : 5b2d07fc D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270) b6e474dc J6.2 — s065 : LA REL SUIVIE D'UN G
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/proto_v3.py", line 22, in <module>     pré vallon colline berge lac etang étang fleuve ocean océan terre air espace""" ).split()               
- **T1** : [stderr] ls: cannot access 'tools/__init__.py': No such file or directory [exit code: 2]
- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r


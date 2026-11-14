# Session session- — Clôture du chantier et tag annoté

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-a68c9aaf-bd76-458b-8501-5a29431b2e10` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 06:53 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 118 |
| Appels d'outils | 129 |
| Fichiers touchés | 4 |
| Commandes | 105 |
| Sous-agents | 0 |
| Commits | 2 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J14.1 : la clôture — **sans relancer la passe complète** (elle a été faite le 14/11 00 h : `work/portes/passe-1311-23h15.log`, 84 portes, 81 vertes, 3 rouges nommées). Vérifie « porte-indice », « porte-melange », « porte-sessions » ; mets à jour `docs/pilotage/references-non-regression.md` si nécessaire ; crée le **tag annoté** `chantier-2026-11-14` sur le dernier commit vert ; écris le rapp … [69 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J14.1 : la clôture — **sans relancer la passe complète** (elle a été faite le 14/11 00 h : `work/portes/passe-1311 … [349 caractères tronqués]

*129 appels d'outils.* Actions notables :

- bash — Check git status and recent history
- bash — List workspace and gate/report dirs
- bash — Read the gate pass log
- bash — Read tolerated red gates doc
- bash — Show date, HEAD, tags
- bash — Look for closure reports, journal, plan
- bash — Extract J13/J14 tasks from plan
- bash — Inspect last commit contents
- bash — Inspect the three gate scripts
- bash — Full status and modified file timestamps
- bash — Read plan diff and today's journal index
- bash — Read current state
- bash — Read sessions tool
- bash — Read session plans/heartbeats
- … et 94 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/mesures.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cloture-chantier.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check git status and recent history
- **T1** List workspace and gate/report dirs
- **T1** Read the gate pass log
- **T1** Read tolerated red gates doc
- **T1** Show date, HEAD, tags
- **T1** Look for closure reports, journal, plan
- **T1** Extract J13/J14 tasks from plan
- **T1** Inspect last commit contents
- **T1** Inspect the three gate scripts
- **T1** Full status and modified file timestamps
- **T1** Read plan diff and today's journal index
- **T1** Read current state
- **T1** Read sessions tool
- **T1** Read session plans/heartbeats
- **T1** Check model, binary, running work, resources
- **T1** Gate sessions and pre-commit hook
- **T1** Run porte-indice in background
- **T1** Run porte-melange in background
- **T1** Run porte-sessions
- **T1** Read gates and closure method
- **T1** Read state and doc review tools
- **T1** Read measurements table summary
- **T1** Read chantier and week reports
- **T1** Check gate progress
- **T1** Locate heartbeat and state lines
- **T1** Check claims and session status
- **T1** Refresh active heartbeat, pause stale hub
- **T1** Re-run porte-sessions after heartbeat fix
- **T1** Check gate progress again
- **T1** Inspect report indexes
- **T1** Find tag conventions
- **T1** Check gate logs
- **T1** Inspect J5.2 tag task
- **T1** Inspect measurements JSON structure
- **T1** Inspect JSON tail conventions
- **T1** Check gate process and progress
- **T1** Inspect journal theme and generators
- **T1** Check gate progress
- **T1** Check git identity and HEAD
- **T1** Wait and check gates
- … et 65 autres

## 4. Mesures et résultats marquants

- **T1** `bb68b820 J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0089 APRÈS TOPO`
- **T1** `porte-c4-retard        ✅                          31 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne`
- **T1** `porte-coupe            ✅                         136 s    ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit`
- **T1** `porte-delais           ✅                          21 s    ✅ le temps, lui, augmente : 7.00 s → 10.42 s (+3.4 s ≈ 50 ms × 64 pas)`
- **T1** `porte-homeostasie      ✅                         529 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)`
- **T1** `porte-jeux             ✅                         111 s    ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision,`
- **T1** `porte-mistral          ✅                          10 s      ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= p`
- **T1** `porte-pont             ✅                          83 s    ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux`
- **T1** `porte-reflexe          ✅                         154 s    ✅ 3. l'accord est mesuré AVANT (0.4 %) et APRÈS — la mesure est branchée`
- **T1** `porte-reparti-moteur   ✅                           3 s  PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %)`
- **T1** `| `porte-c4-retard.sh` | 29 s | PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne |`
- **T1** `| `porte-coupe.sh` | 131 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit pour  |`
- **T1** `| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.77 s → 9.67 s (+2.9 s ≈ 50 ms × 64 pas) |`
- **T1** `| `porte-homeostasie.sh` | 495 s | ✅ porte tenue (×0 exact · activité monotone · dominance reproduite) |`
- **T1** `| `porte-jeux.sh` | 104 s | ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision, |`
- **T1** `| `porte-mistral.sh` | 8 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= plancher  |`
- **T1** `| `porte-pont.sh` | 79 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |`
- **T1** `| `porte-reflexe.sh` | 141 s | ✅ 3. l'accord est mesuré AVANT (0.4 %) et APRÈS — la mesure est branchée |`
- **T1** `| `porte-reparti-moteur.sh` | 3 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `# pèse ×10 ailleurs). Le contrôle apparié annule le texte : MÊME invite, MÊME longueur, une`
- **T1** `| 05:37 | `bb68b820` | J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0`
- **T1** `**521/532** étiquetées Glottolog), le top-1 de voisinage est de la même famille **66,1 %** (hasard`
- **T1** `10,3 %) et de la même branche **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout est au hasard**`
- **T1** `(famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %) ; dans la même écriture, la famille monte à`
- **T1** `**69,8 %** et la sœur à **27,8 %**. Le retrieval parallèle 30 articles le chiffre : sur les **25`
- **T1** `autre segment ; couverture **65,84 % des jetons**, **75,19 % des caractères**. La limite est la`
- **T1** `Temps CLI médian **159,2 ms**, API **2,7 ms**. Fiche`
- **T1** `La loi H0 se reproduit (**R² = 0,909139** sur 655 lignes, **0,906307** sur 488 paires uniques non auto) ;`
- **T1** `le retrieval brut donne **61,4 %** de même tradition et **56,8 %** de voisins à ≤50 ans ; les contrôles`
- **T1** `croisés ramènent la filiation à **50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373).`
- **T1** `Seule une petite prédiction d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../re`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `- **Note** : l'attachement est à **236/237 (0,9916)**, la couverture 0,9916, POS **86,25 %**, F1 **0,7535**, 2 spans ; la seule rouge est`
- **T1** `CPU + neuronal de contrat, parallèle/cascade, activation 51–76 %) ; **398 langues à 0,9687**,`
- **T1** `**tête 0,560**, pragmatique **1,0/1,0/0,994/0,889** ; cascade (mock) **67,1 %** ;`
- **T1** `contrôle négatif est le même sur les deux : une cible exacte tirée au hasard vaut **1,67 %**`
- **T1** `| P04 | F1 syntagmes (vue alternative) | 602 · 239 cibles | — (non publié sur 602) | **0,7882** (P 0,7818 / R 0,7946 ; 1 455/406/376) | −0,0020 vs 612 | 234 labels au lieu de 238 ; même span exact 1,0`
- **T1** `| T01 | POS API (tagger neuronal seul) | 612 · 3 179 jetons | 0,8625 (2 742/3 179) | **0,9475** (3 012/3 179) | **+8,49 pts** [7,23 ; 9,74] | majoritaire 0,2145 ; classe fréquente 0,2491 ; permutation`
- **T1** `| Q05 | Mesure par langue | 612 · fr 402 phrases / 2 031 tokens / 151 cibles ; en 210 / 1 148 / 88 | global seul : POS 0,8625 ; F1 0,7902 ; att. 238/239 | fr POS **0,8159** / F1 **0,7475** / att. **15`
- **T1** `| Q06 | Robustesse — 50 textes libres | 50 textes A26 · 46 annotations · 4 refus | A26 (06/11) : 4 refus code 1 sans JSON ; 0/46 champs 8 ; 107 chevauchements alternative ; 0 filtrer | **0 plantage** `
- **T1** `McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. Contrôles négatifs : majoritaire **0,2145**, classe`
- **T1** `| table atomes ↔ niveaux | 0 ligne mesurée | **14/14 lignes, 8 niveaux** | hypothèse, pas corrélation ; 33 paires à ∣r∣ ≥ 0,5 ; 4 composantes > 1 ; 80,7 % de variance sur 3 | [atomes](rapport-atomes-n`
- **T1** `| corpus commun | 0 texte commun | **21 textes, 418/438 paires exactes (95,4 %)** | 8/8 (6 rejets + 2 témoins) ; 20 écarts exclus, pas corrigés | [corpus](rapport-corpus-commun.md) |`
- **T1** `| retrieval par famille (J7.1) | 0 mesure | **532 textes (445 langues)** ; famille **66,1 %** (hasard 10,3 %), sœur **26,1 %** (2,5 %) | permutations 1 000/500 ; requêtes permutées ; leave-one-languag`
- **T1** `**4 composantes > 1**, les trois premières à **80,7 %** de la variance (6,967 · 2,845 · 1,491).`
- **T1** `**418 exactes (95,4 %)** ; **20 écarts de surface exclus, pas corrigés** (apostrophes,`
- **T1** `0,427** est un **effet de composition** : 60 % des couples décalés sont de même écriture,`
- **T1** `contre 33 % des contemporains.`
- **T1** `| corpus commun | 0 texte commun | **21 textes, 418/438 paires exactes (95,4 %)** | 8/8 (6 rejets + 2 témoins) | [corpus](rapport-corpus-commun.md) |`
- **T1** `un **effet de composition** : 60 % des couples décalés sont de même écriture, contre 33 % des`
- **T1** `reports/INDEX.md:119:| [rapport-consolidation-structure-partagee.md](rapport-consolidation-structure-partagee.md) | Ce qui se consolide, c'est la STRUCTURE PARTAGÉE — même mémorisation (−22,5 %), tran`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `| [rapport-a83d-lot-threads.md](rapport-a83d-lot-threads.md) | A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread |`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 niveaux |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir 0,2276 |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | **B13** — POS **83,83 %** (R2a/R3/R2b), F1 **0,6181** |`
- **T1** `| [`rapport-autotest-parallele.md`](rapport-autotest-parallele.md) | **B13** — l'autotest parallèle : **183/183 en 1 min 54** (×2,4), mêmes verdicts |`
- **T1** `[still running after 60000ms; moved to background job bash-31]`
- **T1** `{"schema": "drave.tableau-mesures", "version": 1, "titre": "J13.1 — la table des mesures du chantier", "sous_titre": "POS, F1, attachement, couverture, spans, le produit, Panini — avant/après, base 61`
- **T1** `"objet": "table 14 atomes × 8 niveaux : 14/14 lignes, 33 paires colinéaires",`
- **T1** `"resultat": "0,2145 / 0,2491 / 0,1667 / 0,0833 ; McNemar 344/74, p = 1,1 × 10⁻⁴²",`
- **T1** `"resultat": "1,99 % fr / 2,27 % en / 1,67 % global",`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête `
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 14/11 03 h 30.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du`
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`
- **T1** `canonique**, le strict **5/46** ; temps CLI médian **159,2 ms**, API **2,7 ms**. Comparaison`
- **T1** `sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur`
- **T1** `contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même`
- **T1** `tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à`
- **T1** `**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction`
- **T1** `d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `**préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `fax **56,7 %**, la limite d'information) ; les **colonnes** tombent de **89,4 %** à **0,5 %**,`
- **T1** `les **tableaux** donnent **92,6 %** de cellules exactes, et **trois vrais scans** s'accordent à`
- **T1** `**7,10 %** et **88,4 %** de mots, l'**ordre des colonnes** prouvé (**15,3 %** contre **98,0 %**`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `38:**État au 14/11 03 h 30.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet`
- **T1** `**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du`
- **T1** `-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../r`
- **T1** `+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../r`

## 5. Erreurs rencontrées

6 sorties en erreur ou divergentes. Les premières :

- **T1** : M reports/pensee-coherence-fiches-v7.json  M reports/pensee-dev-test-v10.json  M reports/pensee-quatre-modes.json  M reports/rapport-audit-v7.md  M reports/rapport-coherence-fiches-v7.md  M reports/ra
- **T1** : sam 14 nov 2026 11:53:18 UTC --- 0e75f101734145489cc45389feb6489591d324fd 2026-11-14 06:32:00 -0500 J13.1 — LA TABLE DES MESURES : F1 0,7533 → 0,7902, ATTACHEMENT 236/237 → 238/238, BASE 612/602, 26 T
- **T1** : commit 0e75f101734145489cc45389feb6489591d324fd Author: Stéphane <stephane@localhost> Date:   Sat Nov 14 06:32:00 2026 -0500      J13.1 — LA TABLE DES MESURES : F1 0,7533 → 0,7902, ATTACHEMENT 236/237
- **T1** : diff --git a/tools/chantier/plan.json b/tools/chantier/plan.json index 21ea0cf4..7d2004b5 100644 --- a/tools/chantier/plan.json +++ b/tools/chantier/plan.json @@ -306,6 +306,118 @@       "attendu": "F
- **T1** : # 2026-11-14 — Campagnes et mesures  > **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`). > Seul le bloc « notes » en fin de fichier est écrit à la main et préservé. > Heure
- **T1** : cb6ccab4 J14.1 — LA CLÔTURE : 84 PORTES, 81 VERTES, 3 ROUGES NOMMÉES (SESSIONS RÉPARÉE, INDICE ET MELANGE STRUCTURELLES) ; TAGS chantier-2026-11-14 ET semaine-2026-11-14 SUR 0e75f101 ; 28/28 ACCEPTATI

## 6. Commits

- J14.1 — LA CLÔTURE : 84 PORTES, 81 VERTES, 3 ROUGES NOMMÉES (SESSIONS RÉPARÉE, INDICE ET MELANGE STRUCTURELLES) ; TAGS chantier-2026-11-14 ET semaine-2026-11-14
- J14.1 — LE RAPPORT DE CLÔTURE EST CORRIGÉ : sessions À 20 s (vérification) ET LE TABLEAU DES MESURES EST MIS À JOUR, PAS SEULEMENT LU" -m "Deux corrections de f


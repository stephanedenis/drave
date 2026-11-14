# Session session- — Table des mesures du chantier J13.1

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-4271ad32-61f1-46a0-8494-7c94c3f8050f` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 06:23 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 96 |
| Appels d'outils | 120 |
| Fichiers touchés | 5 |
| Commandes | 102 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J13.1 : la table des mesures du chantier — POS, F1, attachement, couverture, spans, le produit, Panini — avant/après, avec la base (612/602), les commits et les contrôles négatifs ; fiche `reports/rapport-tableau-mesures.md` + JSON.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J13.1 : la table des mesures du chantier — POS, F1, attachement, couverture, spans, le produit, Panini — avant/apr … [118 caractères tronqués]

*120 appels d'outils.* Actions notables :

- bash — List working directory and recent commits
- bash — Search for task J13.1 references
- bash — Show plan entries for late tasks
- bash — Read current state document
- bash — Read previous bilan report
- bash — Read previous bilan JSON head
- bash — Read rest of previous bilan
- bash — Read results method doc
- bash — List recent commits with tasks
- bash — List report names
- bash — Inspect J11/J12 report JSON structures
- bash — Find related JSON names
- bash — Show files changed in J11/J12 commits
- bash — Summarize JSON structures of recent reports
- … et 103 autres

**Synthèse produite :**

I'll assemble the consolidated measurement table, JSON, and verify the base numbers at HEAD. Let me first build the data file.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/build_tableau.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 10 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/mesures.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** List working directory and recent commits
- **T1** Search for task J13.1 references
- **T1** Show plan entries for late tasks
- **T1** Read current state document
- **T1** Read previous bilan report
- **T1** Read previous bilan JSON head
- **T1** Read rest of previous bilan
- **T1** Read results method doc
- **T1** List recent commits with tasks
- **T1** List report names
- **T1** Inspect J11/J12 report JSON structures
- **T1** Find related JSON names
- **T1** Show files changed in J11/J12 commits
- **T1** Summarize JSON structures of recent reports
- **T1** Read J11.2 report
- **T1** Read J11.3 report
- **T1** Read J11.1/J11.4 report heads
- **T1** Read J12.1 report head
- **T1** Read J12.1 results sections
- **T1** Read J12.2 report
- **T1** Find frozen gold 602 values
- **T1** Find frozen gold metrics
- **T1** Read base table in honesty pass report
- **T1** Read week report overview
- **T1** Summarize Panini JSON structures
- **T1** Extract exact Panini aggregate values
- **T1** Check atoms calibration values
- **T1** List all plan tasks
- **T1** Get commit dates and subjects
- **T1** Re-measure living gold 612
- **T1** Re-measure frozen gold 602
- **T1** Find historical frozen 602 metrics
- **T1** Inspect journal entries for the day
- **T1** Read roadmap
- **T1** Inspect table gate and doc review
- **T1** Inspect gold loader paths
- **T1** Check tracked gold files and working tree status
- **T1** Identify parent commit of first chantier task
- **T1** Measure pre-chantier gold 612/602 in worktree
- **T1** Compare pre/post metrics on both golds
- … et 62 autres

## 4. Mesures et résultats marquants

- **T1** `bb68b820 J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0089 APRÈS TOPO`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../re`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. Contrôles négatifs : majoritaire **0,2145**, classe`
- **T1** `| table atomes ↔ niveaux | 0 ligne mesurée | **14/14 lignes, 8 niveaux** | hypothèse, pas corrélation ; 33 paires à ∣r∣ ≥ 0,5 ; 4 composantes > 1 ; 80,7 % de variance sur 3 | [atomes](rapport-atomes-n`
- **T1** `| corpus commun | 0 texte commun | **21 textes, 418/438 paires exactes (95,4 %)** | 8/8 (6 rejets + 2 témoins) ; 20 écarts exclus, pas corrigés | [corpus](rapport-corpus-commun.md) |`
- **T1** `| retrieval par famille (J7.1) | 0 mesure | **532 textes (445 langues)** ; famille **66,1 %** (hasard 10,3 %), sœur **26,1 %** (2,5 %) | permutations 1 000/500 ; requêtes permutées ; leave-one-languag`
- **T1** `**4 composantes > 1**, les trois premières à **80,7 %** de la variance (6,967 · 2,845 · 1,491).`
- **T1** `**418 exactes (95,4 %)** ; **20 écarts de surface exclus, pas corrigés** (apostrophes,`
- **T1** `0,427** est un **effet de composition** : 60 % des couples décalés sont de même écriture,`
- **T1** `contre 33 % des contemporains.`
- **T1** `| **D8** | Comparer les deux généalogies sur les **paires couvertes** ; « inconnu = 1,0 » n'est **pas** une distance | R² 0,256 contre 0,230 ; 154/154 hors script | ✅ ; V14, 9 dhātus, distance continu`
- **T1** `| **D16** | Lire le retrieval **par écriture d'abord**, puis séparer **sœur** et **famille lointaine** ; la « famille » est un mélange | sœur +0,448 (p = 0,002) contre famille +0,155 ; R² 0,474 → 0,63`
- **T1** `| **R25** | « La **famille** est une variable unique » | famille **+0,1548** contre sœur **+0,4479** ; R² 0,474 → 0,631 | la famille est un **mélange** de sœurs et de familles lointaines ; il faut la `
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `bb68b820 (origin/s/v7, origin/master, origin/HEAD, master) J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0`
- **T1** `9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`
- **T1** `26c7b7ab ROADMAP ET JOURNAL — LA NUIT FINIT À F1 0,7535, POS 86,25 %, 236/237, COUVERTURE 0,9916 ; LA CONVENTION DU SUJET`
- **T1** `5a067ba5 ROADMAP ET JOURNAL — LA NUIT FINIT À 236/237, COUVERTURE 0,9916, POS 86,25 %, 2 SPANS ; r264 RÉGLÉ`
- **T1** `ba42d4cc FICHE — LES TROIS RÈGLES REJETÉES (PARTICIPES, R4-FR GÉNÉRIQUE, PARTICIPE APRÈS AVOIR) ; POS RESTE À 86,25 %`
- **T1** `c43dd5cc B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `6432bdb9 JOURNAL ET ROADMAP — LA NUIT DES ÉTATS : N2/S/R/A INVENTORIÉS, FRONTIÈRE CORRIGÉE (A6.2 LIBRE), POS 85,84 %, PONCT, R4-FR ; ÉTAT HORODATÉ`
- **T1** `6b976cb1 B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `7a45325f B13 — LA PONCTUATION A UNE POS (PONCT) : POS 85,00 → 85,75 %, MIROIR 0,196 → 0,2276, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `bfd98892 DOC PRODUIT — RESYNCHRONISÉE : POS 85,00 %, F1 0,6482, ATTACHEMENT 235/236, GELÉ 85,32 / 0,6511 ; SORTIE D'EVALUER REJOUÉE`
- **T1** `['mesure in-sample : les règles ont été dessinées sur ce gold', 'l’anglais est 100 % réel (6 hand + 204 reel) ; le français ajoute 160 synthétiques', '88 cibles anglaises (dont 1 sans span, g017) : pe`
- **T1** `> même composition** : l'anglais est **100 % réel**, le français ajoute **160 synthétiques**.`
- **T1** `| **fr** | 151 | 151 | **151/151 (1,0000)** | **1,0000** | 149/151 (0,9868) | 1,99 % |`
- **T1** `| **en** | 88 | 87 | **87/88 (0,9886)** | **1,0000** | 87/88 (0,9886) | 2,27 % |`
- **T1** `| tout | 239 | 238 | 238/239 (0,9958) | 1,0000 | 236/239 (0,9874) | 1,67 % |`
- **T1** `**1,67 %** (239 cibles), **1,99 %** (151, fr) et **2,27 %** (88, en), graine 0. Le modèle est`
- **T1** `- **composition des golds** : l'anglais est 100 % réel, le français a 160 synthétiques ; même`
- **T1** `> **159,2 ms**, API **2,7 ms**.`
- **T1** `| codes de sortie | **46 × 0**, **4 × 3** |`
- **T1** `| couverture des jetons / caractères | 65,84 % / 75,19 % | **65,84 % / 75,19 %** |`
- **T1** `médiane est dominée par le **démarrage de Python** (~150 ms), pas par l'analyse.`
- **T1** `- L'API est à **quelques ms** ; le maximum est `f50` (74,0 ms), le texte long de 2 144`
- **T1** `sont inchangés ; les **2 unités** et **61,5 %** du texte aussi.`
- **T1** `segments du groupe 0 portent `meta.partition` (`membres: 3` ; rang 1 = REL longue, rang 2 = GV,`
- **T1** `rang 3 = REL courte) et `meta.alternative` avec les deux autres. La doc le dit maintenant au § 2.`
- **T1** `**Lecture.** Le porteur est le **rang 2** d'un groupe de **3** ; l'alternative de rang 1 (la REL`
- **T1** `> de séparer les deux.** La loi H0 de Panini se reproduit (**R² = 0,909139** sur les **655 lignes** de`
- **T1** `> Sur les **44 signatures** (14 parts flottantes), le retrieval brut donne **61,4 %** de même tradition`
- **T1** `> (hasard 22,4 %) et **56,8 %** de voisins à ≤ 50 ans (hasard 22,8 %) ; les contrôles croisés ramènent`
- **T1** `> la filiation à **50,0 %** (p = 0,0492, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,373). Seule une`
- **T1** `> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0086, **Holm 0,034**).`
- **T1** `> `analytic_sigs_v1.json` (**44 œuvres × 14 atomes**), `sources_coverage.json` / `sources_manifest.json``
- **T1** ``d_lex ~ 1 + même_tradition_large` donne **R² = 0,369** et **β = −0,189** : les paires de même`
- **T1** `| **même tradition large** | **61,4 %** | 22,4 % | **2,74×** | **27** |`
- **T1** `| **même auteur canonique** | **36,4 %** | 10,0 % | **3,64×** | **16** |`
- **T1** `| **à ≤ 50 ans** | **56,8 %** | 22,8 % | **2,49×** | **25** |`
- **T1** `| **filiation** (top-1 même tradition, étiquettes permutées dans les tranches de 250 ans) | **61,4 %** | **50,0 %** | **0,0492** | **0,128** |`
- **T1** `| **époque** (top-1 ≤ 50 ans, années permutées dans chaque tradition) | **56,8 %** | **53,8 %** | **0,373** | 0,373 |`
- **T1** `| **filiation, exactitude équilibrée** (même null) | **30,6 %** | **22,0 %** | **0,092** | — |`
- **T1** `significative (0,373). Le top-1 d'époque **brut** (56,8 %) est donc presque entièrement expliqué par`
- **T1** `| **année, résidu intra-tradition** | MAE **55,7** ; R² **0,042** | **82,2** ; p = **0,033** | 4,2 % de la variance intra-tradition |`
- **T1** `| **tradition, kNN k=1** | exactitude **61,4 %** ; équilibrée **30,6 %** | majorité **43,2 %** ; null date **50,0 %** (p = 0,043) | l'exactitude est portée par GRECO (19/44) |`
- **T1** `| **tradition, équilibrée** | **30,6 %** | null date **22,0 %** (p = 0,092) | pas significatif après date |`
- **T1** `La lecture est nette : **l'année brute est très prédite** (R² 0,614), mais **presque toute** cette`
- **T1** `global). Il reste **4,2 %** de variance intra-tradition (p = 0,033), et c'est le **seul** test qui`
- **T1** `équilibrée** (30,6 %) et le null de date (22,0 %, p = 0,092) montrent que le modèle retrouve surtout`
- **T1** `donne **R² = 0,016** : la tradition n'explique presque rien de la similarité des signatures, et la date`
- **T1** `encore moins (β ≈ 8,7 × 10⁻⁶). Le top-1 reste à **50 %** de même tradition (hasard 15,2 %) et **37,5 %**`
- **T1** `à ≤ 50 ans (hasard 9,1 %) — mais avec **24 requêtes**, ces taux sont fragiles et ne sont pas le même`
- **T1** `cos = 1) sont retirés des candidats : le top-1 tradition reste **61,4 %**, le top-1 ≤ 50 ans monte à`
- **T1** `**59,1 %**. Ils ne portent donc pas la conclusion ; ils la rendent seulement plus propre.`
- **T1** ``d_sig ≈ 0,159 + 0,049·d_graph + 0,138·(Δyear/1000) + 0,002·même_tradition`, **R² = 0,3004**.`
- **T1** `1. **La loi H0 du §334 est une loi de filiation/topologie**, pas d'époque : R² = 0,909139 sur les 655`
- **T1** `formulation qui publierait `0,85` sans « POS » ni `85 %`. Une fiche peut donc rester périmée`
- **T1** `| POS (gold vivant 612) | **84,96 – 85,75 %** | **86,25 %** | **+0,50 à +1,29 pt** |`
- **T1** `« l'état courant est … (POS 86,25 %, F1 0,7535, 236/237, 2 spans) » : en recopiant l'état, il`
- **T1** `| corpus commun | 0 texte commun | **21 textes, 418/438 paires exactes (95,4 %)** | 8/8 (6 rejets + 2 témoins) | [corpus](rapport-corpus-commun.md) |`
- **T1** `un **effet de composition** : 60 % des couples décalés sont de même écriture, contre 33 % des`
- **T1** `principe: 20 langues stratifiées (5 familles glottolog × 4) + le français, pivot de Drave ; toutes les paires sont exactes après n`
- **T1** `lecture "Les 44 oeuvres sont majoritairement philosophiques et religieuses ; les correlations refletent le genre, l'epoque et le lexique, pas la structure linguistique. Les parts sont compositionnelle`
- **T1** `9c7f71dc 2026-11-07 14:55 PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`
- **T1** `| 05:37 | `bb68b820` | J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0`
- **T1** `**521/532** étiquetées Glottolog), le top-1 de voisinage est de la même famille **66,1 %** (hasard`
- **T1** `10,3 %) et de la même branche **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout est au hasard**`
- **T1** `(famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %) ; dans la même écriture, la famille monte à`
- **T1** `**69,8 %** et la sœur à **27,8 %**. Le retrieval parallèle 30 articles le chiffre : sur les **25`
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
- **T1** `suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du plancher 1`
- **T1** `> change pas : **144 FP de sujet (45 %)** dominent, puis 73 d'objet, 39 de troncature. Deux règles`
- **T1** `| **sujet** | **144** | 45 % | 4 | 144 | **5** | le GV commence avant le verbe, sur le sujet (« Il a couru ») |`
- **T1** `| objet | 73 | 23 % | 75 | 73 | **75** | le GV avale un nom nu objet (« love music ») |`
- **T1** `| tronque | 39 | 12 % | 42 | 40 | **42** | le GV est plus court que le gold (« venir » pour « Peux-tu venir ») |`
- **T1** `| deux_cotes | 27 | 8 % | 18 | 25 | **15** | le GV déborde des deux côtés |`
- **T1** `| adverbe | 16 | 5 % | 16 | 10 | **10** | le GV avale un adverbe final (« viens demain ») |`
- **T1** `| parasite | 16 | 5 % | 16 | 16 | **16** | GV sans recouvrement (une préposition prise pour un verbe) |`
- **T1** `| gauche_autre | 5 | 2 % | 3 | 6 | **4** | débordement à gauche hors GN sujet |`
- **T1** `| **total** | **320** | 100 % | **174** | **315** | **167** | |`
- **T1** `| chev_droite | 75 | 42 % | 80 | 72 | **77** | le gold est plus long à droite (« souffle » vs « souffle fort ») |`
- **T1** `| avale_GN | 51 | 28 % | 51 | 51 | **51** | le GV du gold est avalé par un GN/GP prédit |`
- **T1** `| chev_deux | 28 | 16 % | 17 | 23 | **15** | recouvrement des deux côtés |`
- **T1** `| tronque | 19 | 11 % | 19 | 19 | **20** | le GV prédit est à l'intérieur du gold |`
- **T1** `| chev_gauche | 6 | 3 % | 3 | 9 | **5** | le GV prédit déborde à gauche |`
- … (tronqué)

## 5. Erreurs rencontrées

7 sorties en erreur ou divergentes. Les premières :

- **T1** : /home/stephane/Data13TB/stephane/GitHub/Qtrinet total 208 drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 . drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 .. -rw-r--r--. 1 stephane stephane  99
- **T1** : b20a4c31 (HEAD -> s/v7) J12.2 — LE CORPUS D'OR CIC EST REJOUÉ HORS DE PANINI : 42/42 VERDICTS, 42/42 EMPREINTES, 36/36 PREUVES ALTÉRÉES REJETÉES (1 020/1 020 MUTATIONS DE eq(2,2)) ; NOYAU DRAVE INDÉPE
- **T1** : 171 reports/rapport-exemples-rejoues.md   108 reports/rapport-evaluer-langue.md   238 reports/rapport-robustesse-semaine.md   190 reports/rapport-schema-v2-doc.md   384 reports/rapport-panini-334.md  
- **T1** : 84e393bb J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238  docs/pilotage/en-cours.md                          |   15 +-  docs/pilotage/ro
- **T1** : 25a6c0ff 2026-11-07 12:40 B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183 92652984 2026-11-07 13:44 B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,75
- **T1** : # 2026-11-14 — Campagnes et mesures  > **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`). > Seul le bloc « notes » en fin de fichier est écrit à la main et préservé. > Heure
- **T1** : AGENTS.md 1196 docs/pilotage/en-cours.md 1643 [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module> AttributeError: module 'taille_documents' has no attribute 'specifiques'

## 6. Commits

- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - <<'EOF' J13.1 — LA TABLE DES MESURES : F1 0,7533 → 0,7902, ATTACHEMENT 236/237 → 238/238, 


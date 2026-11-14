# Session session- — Analyse vague Panini §334

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-6a9e96a0-20f8-4721-8b73-82eba29bd2b6` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 05:08 |
| Durée | 0.5 h |
| Tours | 1 |
| Messages | 133 |
| Appels d'outils | 146 |
| Fichiers touchés | 1 |
| Commandes | 141 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J12.1 : la deuxième vague Panini — le corpus §334 (114 textes, 655 paires, 102 sources) et les signatures des 44 œuvres (14 flottants) : mesurer le retrieval et la prédiction de l'époque vs la filiation, avec le contrôle de date. Fiche `reports/rapport-panini-334.md` + JSON.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J12.1 : la deuxième vague Panini — le corpus §334 (114 textes, 655 paires, 102 sources) et les signatures des 44 œ … [161 caractères tronqués]

*146 appels d'outils.* Actions notables :

- bash — List repo root, reports, journal
- read
- bash — Find Panini-related files
- bash — Recent git history and status
- bash — Search state and plan for J12.1
- bash — Inspect Panini repos and inventory report
- bash — Print J12 and Panini tasks from plan
- bash — Locate retrieval scripts and 655 references
- job_kill
- bash — Inspect Panini research repo for §334
- grep
- bash — Find catalogue and recent docs
- bash — Inspect falsification artifacts
- bash — Search for 44 works signatures
- … et 132 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_334.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repo root, reports, journal
- **T1** Find Panini-related files
- **T1** Recent git history and status
- **T1** Search state and plan for J12.1
- **T1** Inspect Panini repos and inventory report
- **T1** Print J12 and Panini tasks from plan
- **T1** Locate retrieval scripts and 655 references
- **T1** Inspect Panini research repo for §334
- **T1** Find catalogue and recent docs
- **T1** Inspect falsification artifacts
- **T1** Search for 44 works signatures
- **T1** Inspect signature files
- **T1** Search docs for 44 works and floating
- **T1** Count signature entries and inspect floating refs
- **T1** List prior Panini reports and scripts
- **T1** Read prior epoch retrieval report
- **T1** Inspect 655 pair metadata
- **T1** Inspect corpus catalogs and official validation JSON
- **T1** Inspect sources manifest and signed corpus
- **T1** Inspect graph v35 nodes
- **T1** Inspect graph node structure
- **T1** Inspect a catalog entry structure
- **T1** Audit 114 texts metadata coverage
- **T1** Check 44 signature works coverage and source counts
- **T1** Cross-check 48 vs 114 vs 44 and source counts
- **T1** Find artifact listing 114 active texts
- **T1** Inspect graph top-level metadata
- **T1** Inspect GPS graph artifact
- **T1** Dump metadata for all 48 pair texts
- **T1** Check duplicate signatures and same-author groups
- **T1** Identify relation between pair metrics and signatures
- **T1** Read genealogy theory doc
- **T1** Read rest of prior report and JSON schema
- **T1** Read result and gate conventions
- **T1** Read retrieve families report and latest journal
- **T1** Check Python scientific stack
- **T1** Read prior tool conventions
- **T1** Inspect blank tradition pairs and language pairs
- **T1** List 44 labels for harmonization
- **T1** Read genealogy two faces report for beta context
- … et 101 autres

## 4. Mesures et résultats marquants

- **T1** `9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`
- **T1** `63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../..`
- **T1** `92:- **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×`
- **T1** `[still running after 60000ms; moved to background job bash-7]`
- **T1** `> dans ce retrieval de **surface**, **l'écriture domine** (+0,609 ; IC 95 % [0,529 ; 0,702]), la **famille**`
- **T1** `> **effet de composition** : les couples décalés contiennent **60 %** de paires de même écriture, les`
- **T1** `> contemporains **33 %**. **L'époque ne domine pas ici ; le confondant de composition, lui, n'est pas nul : sans`
- **T1** `langue B ?* Le hasard est **1/30 = 3,33 %**. Toutes les entrées portent **1948** : la date est contrôlée par`
- **T1** `toutes les traductions, versets non répétés, graine 0). Le hasard est **1/1 000 = 0,1 %**.`
- **T1** `A, on classe les candidats de B ; le **top-1** est la proportion de requêtes dont le bon candidat est rang 1.`
- **T1** `intervalles **inter-paires** (2,5–97,5 %).`
- **T1** `la mesure appariée. Les 2×2 :`
- **T1** `| variable | coefficient | IC 95 % |`
- **T1** `**R² = 0,400.** L'écriture pèse **près de trois fois** la famille. Les coefficients ne se comparent pas`
- **T1** `[0,014 ; 0,111], R² = 0,140. **Contrôle négatif** : cibles permutées **0,0323** contre 0,0333 de hasard —`
- **T1** `(0,238) : c'est l'inverse de l'avertissement. Mais les couples décalés contiennent **60 %** de paires de`
- **T1** `même écriture (18/30), contre **33 %** chez les contemporains (14/42). **À écriture contrôlée, les deux`
- **T1** `"Sciences hellénistiques (Euclide, Archimède ×2, Apollonius, Aratos, Aristarque)",`
- **T1** `- **langues** : 448 langues UDHR ; la surface est **lue à 80-100 %** ; le **sens** se retrouve à **96 %**`
- **T1** `sur les paires bien couvertes, **16 %** sur 100 langues stratifiées, **3,5×** le hasard dans un vivier`
- **T1** `- **dialectes** : 100 % lisibles ; contenu retrouvé **30 à 100 %** selon la couverture de la langue ;`
- **T1** `- **styles / traducteurs** : 87-100 % lisibles ; contenu **6-24 %** — *et ce chiffre est encore confondu`
- **T1** `Δ moyen **+0,52 point**, IC 95 % **[−2,9 ; +4,3]**. Les effets par cible ne sont pas monotones :`
- **T1** `Δ moyen **+0,52 point**, IC 95 % **[−1,2 ; +1,9]**. Positifs : **LUT +2,6**, **KJV +2,1**,`
- **T1** `**Le 2×2 anglais × français.** Quatre cellules, même paire de langues, dates croisées :`
- **T1** `**R² = 0,763.** Le coefficient de dates n'est **pas significatif** ; le contrôle par **permutation des`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `> le top-1 de voisinage est de la même famille dans **66,1 %** des cas (hasard 10,3 %) et de la même`
- **T1** `> branche (sœur) dans **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout retombe au hasard** :`
- **T1** `> famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %. Dans la même écriture, la famille monte à`
- **T1** `> **69,8 %** (hasard 16,2 %) et la sœur à **27,8 %** (hasard 5,7 %). Le retrieval parallèle 30 articles`
- **T1** `| étiquetés Glottolog | **521** | 97,9 % ; 11 restent non étiquetés |`
- **T1** `valeurs du même ordre (top-1 famille 66,4 %, sœur 25,9 %) : la déduplication ne change pas la conclusion,`
- **T1** `| **échantillon 20** | les 20 strates du corpus commun (5 familles × 4, sans `fra`) | **20** | **380** |`
- **T1** `**521/532** étiquetées Glottolog), le top-1 de voisinage est de la même famille **66,1 %** (hasard`
- **T1** `10,3 %) et de la même branche **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout est au hasard**`
- **T1** `(famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %) ; dans la même écriture, la famille monte à`
- **T1** `**69,8 %** et la sœur à **27,8 %**. Le retrieval parallèle 30 articles le chiffre : sur les **25`
- **T1** `top-1 0,049, écriture +0,062, famille +0,056, R² 0,14. J3.2 a montré que, sur ces 21 langues,`
- **T1** `| **famille, brut** | **13/15** (86,7 %) | `kin`, `ibo` : Panini dit « Niger-Congo », Glottolog « Atlantic-Congo » — nomenclature, pas désaccord substantiel |`
- **T1** `| **famille, apparié** | **15/15** (100 %) | en traitant Niger-Congo comme la famille large d'Atlantic-Congo |`
- **T1** `| **branche, nœud exact** | **14/15** (93,3 %) | `mya` : « Tibeto-Burman » n'a pas de nœud exact dans le chemin Glottolog (`tibe1272` absent) ; `burm1265` est le descendant le plus proche |`
- **T1** `| **branche, nœud proche** | **15/15** (100 %) | avec l'allowance ci-dessus |`
- **T1** `(p = 2,8 × 10⁻¹⁴), **Pearson r = 0,918** (p = 3,3 × 10⁻⁴³). Sur les **10 paires** des 5 langues de`
- **T1** ``LANG_TREE`, P1 et P2 donnent des **valeurs identiques** (6 × 0,40, 4 × 0,75). L'accord est donc excellent`
- **T1** `| même famille + même script | **8** | **0,3853** | 0,2004 | **7/8** (87,5 %) | 0,4216 |`
- **T1** `| 1 | 6,967 | 49,76 % | 49,76 % |`
- **T1** `| 2 | 2,845 | 20,32 % | 70,08 % |`
- **T1** `| 3 | 1,491 | 10,65 % | **80,73 %** |`
- **T1** `| 4 | 1,260 | 9,00 % | 89,73 % |`
- **T1** `| 5 | 0,528 | 3,77 % | 93,51 % |`
- **T1** `| 6 | 0,381 | 2,72 % | 96,23 % |`
- **T1** `**4 composantes > 1** ; **3 composantes pour 80 %** ; **5 pour 90 %** ; **6 pour 95 %**. Sur la`
- **T1** `**covariance** des parts CLR (sans standardiser), il n'y a plus qu'**une** composante > 1 (52,63 % de la`
- **T1** `de « filiation » (`d_graph`) vaut **+0,0489** contre **+0,1378** pour l'époque (R² = 0,3004), et leurs`
- **T1** `5. **Les deux généalogies prédisent le retrieval de façon comparable.** R² 0,256 (P2) contre 0,230 (G)`
- **T1** `"interpretation_dsig": "d_sig ≈ +0.159 +0.049·d_graph +0.138·(Δyear/1000) +0.002·same_trad  (R²=0.300)",`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../re`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `38:**État au 14/11 03 h 30.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet`
- **T1** `54:**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (has`
- **T1** `235:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `310:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête `
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 14/11 03 h 30.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du`
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`
- **T1** `canonique**, le strict **5/46** ; temps CLI médian **159,2 ms**, API **2,7 ms**. Comparaison`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `15:> la filiation à **50,0 %** (p = 0,0496, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,352). Seule une`
- **T1** `16:> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0088, **Holm 0,035**).`
- **T1** `210:| **filiation** (top-1 même tradition, étiquettes permutées dans les tranches de 250 ans) | **61,4 %** | **50,0 %** | **0,0496** | **0,128** |`
- **T1** `211:| **époque** (top-1 ≤ 50 ans, années permutées dans chaque tradition) | **56,8 %** | **53,8 %** | **0,352** | 0,352 |`
- **T1** `216:significative (0,352). Le top-1 d'époque **brut** (56,8 %) est donc presque entièrement expliqué par`
- **T1** `229:| **année, résidu intra-tradition** | MAE **55,7** ; R² **0,042** | **82,1** ; p = **0,032** | 4,2 % de la variance intra-tradition |`
- **T1** `235:global). Il reste **4,2 %** de variance intra-tradition (p = 0,032), et c'est le **seul** test qui`
- **T1** `292:   (56,8 % vs 22,8 %), mais les contrôles croisés ramènent la filiation à 50,0 % (p = 0,0496, Holm`
- **T1** `293:   0,128) et l'époque à 53,8 % (p = 0,352). **Aucun des deux n'est fort**.`
- **T1** `295:   (R² = 0,042, p = 0,0088, Holm 0,035) : il reste une trace d'époque, mais 96 % de la variance`
- **T1** `374:  **petite** prédiction d'année intra-tradition (R² = 0,042, Holm 0,035) ; la filiation est **marginale**`
- **T1** `15:> la filiation à **50,0 %** (p = 0,0498, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,3565). Seule une`
- **T1** `16:> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0106, **Holm 0,042**).`
- **T1** `210:| **filiation** (top-1 même tradition, étiquettes permutées dans les tranches de 250 ans) | **61,4 %** | **50,0 %** | **0,0498** | **0,128** |`
- **T1** `211:| **époque** (top-1 ≤ 50 ans, années permutées dans chaque tradition) | **56,8 %** | **53,8 %** | **0,3565** | 0,3565 |`
- **T1** `216:significative (0,3565). Le top-1 d'époque **brut** (56,8 %) est donc presque entièrement expliqué par`
- **T1** `229:| **année, résidu intra-tradition** | MAE **55,7** ; R² **0,042** | **82,1** ; p = **0,031** | 4,2 % de la variance intra-tradition |`
- **T1** `235:global). Il reste **4,2 %** de variance intra-tradition (p = 0,031), et c'est le **seul** test qui`
- **T1** `293:   (56,8 % vs 22,8 %), mais les contrôles croisés ramènent la filiation à 50,0 % (p = 0,0498, Holm`
- **T1** `294:   0,128) et l'époque à 53,8 % (p = 0,3565). **Aucun des deux n'est fort**.`
- **T1** `296:   (R² = 0,042, p = 0,0106, Holm 0,042) : il reste une trace d'époque, mais 96 % de la variance`
- **T1** `375:  **petite** prédiction d'année intra-tradition (R² = 0,042, Holm 0,042) ; la filiation est **marginale**`
- **T1** `1. **La loi H0 du §334 est une loi de filiation/topologie**, pas d'époque : R² = 0,909139 sur les 655`
- **T1** `4. **Sur les 44 signatures**, le brut penche pour la filiation (61,4 % vs 22,4 %) et pour l'époque`
- **T1** `(56,8 % vs 22,8 %), mais les contrôles croisés ramènent la filiation à 50,0 % (p = 0,0498, Holm`
- **T1** `0,128) et l'époque à 53,8 % (p = 0,3565). **Aucun des deux n'est fort**.`
- **T1** `(R² = 0,042, p = 0,0106, Holm 0,042) : il reste une trace d'époque, mais 96 % de la variance`
- **T1** `**petite** prédiction d'année intra-tradition (R² = 0,042, Holm 0,042) ; la filiation est **marginale**`
- **T1** `326:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `autre segment ; couverture **65,84 % des jetons**, **75,19 % des caractères**. La limite est la`
- **T1** `Temps CLI médian **159,2 ms**, API **2,7 ms**. Fiche`
- **T1** `....                                                                     [100%]`
- **T1** `15:> la filiation à **50,0 %** (p = 0,0492, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,373). Seule une`
- **T1** `16:> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0086, **Holm 0,034**).`
- **T1** `210:| **filiation** (top-1 même tradition, étiquettes permutées dans les tranches de 250 ans) | **61,4 %** | **50,0 %** | **0,0492** | **0,128** |`
- **T1** `211:| **époque** (top-1 ≤ 50 ans, années permutées dans chaque tradition) | **56,8 %** | **53,8 %** | **0,373** | 0,373 |`
- **T1** `216:significative (0,373). Le top-1 d'époque **brut** (56,8 %) est donc presque entièrement expliqué par`
- **T1** `229:| **année, résidu intra-tradition** | MAE **55,7** ; R² **0,042** | **82,2** ; p = **0,033** | 4,2 % de la variance intra-tradition |`
- **T1** `235:global). Il reste **4,2 %** de variance intra-tradition (p = 0,033), et c'est le **seul** test qui`
- **T1** `293:   (56,8 % vs 22,8 %), mais les contrôles croisés ramènent la filiation à 50,0 % (p = 0,0492, Holm`
- **T1** `294:   0,128) et l'époque à 53,8 % (p = 0,373). **Aucun des deux n'est fort**.`
- **T1** `296:   (R² = 0,042, p = 0,0086, Holm 0,034) : il reste une trace d'époque, mais 96 % de la variance`
- … (tronqué)

## 5. Erreurs rencontrées

7 sorties en erreur ou divergentes. Les premières :

- **T1** : febfdfff J11.4 — SCHÉMA v2 DOCUMENTÉ : 4 CHAMPS PARTITION + 10 CHAMPS ALTERNATIVE, 6 CAS / 0 ÉCHEC, LES DEUX VERSIONS LUES (612 v2 + 612 v1) 55bde5c5 J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 S
- **T1** : nipada/corpus/INDEX_catalogs_v206z.json nipada/corpus/INDEX_catalogs_v207a.json nipada/corpus/catalog_african_colonial_v206x.json nipada/corpus/catalog_buddhist_axial_v205.json nipada/corpus/catalog_b
- **T1** : # J7.1 — Le retrieval approfondi par famille Glottolog  > **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, J7.1 · **Date** : 2026-11-14 > **Verdict** : ✅ **le retrieval retrou
- **T1** : 2026-11-14T05:15:33-05:00 2026-11-14 05:05:58 -0500 febfdfff J11.4 — SCHÉMA v2 DOCUMENTÉ : 4 CHAMPS PARTITION + 10 CHAMPS ALTERNATIVE, 6 CAS / 0 ÉCHEC, LES DEUX VERSIONS LUES (612 v2 + 612 v1)
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 17, in <module> KeyError: <function b at 0x7fe31bc8d260> [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 17, in <module> NameError: name 'b' is not defined [exit code: 1]
- **T1** : -rwxr-xr-x. 1 stephane stephane 1470 31 oct 12:55 .git/hooks/pre-commit #!/bin/sh # pre-commit — l'état accompagne le fait, le journal accompagne le code. # # Versionné dans tools/hooks/ et installé p

## 6. Commits

- cat > /tmp/commit-j121.txt <<'EOF' J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44


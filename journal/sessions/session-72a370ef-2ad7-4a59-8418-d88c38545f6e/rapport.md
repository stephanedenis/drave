# Session session- — Rapport protocole Panini à date contrôlée

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-72a370ef-2ad7-4a59-8418-d88c38545f6e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 02:46 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 113 |
| Appels d'outils | 134 |
| Fichiers touchés | 0 |
| Commandes | 131 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche B1 : le protocole Panini à date contrôlée (la suite de la note 4A) — construis `reports/rapport-protocole-date.md` + JSON : 60 paires en trois groupes (20 contemporaines de traditions différentes ±10 ans, 20 de même tradition à ±200 ans, 20 de même langue source à dates décalées), tirées des artefacts §334 en lecture seule ; le protocole (H0, les contrôles, les 14 atomes), le pré-enregistrem … [77 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche B1 : le protocole Panini à date contrôlée (la suite de la note 4A) — construis `reports/rapport-protocole-date.md` … [357 caractères tronqués]

*134 appels d'outils.* Actions notables :

- bash — List repo root and reports
- bash — Show recent commits and status
- bash — Find Panini/4A related files
- bash — Read Panini-Nipada method doc
- read
- bash — Inspect 334 artifacts sizes
- bash — Inspect panini-334.json structure
- bash — Locate Panini repo
- bash — Search Panini repo for 334 artifacts
- bash — Inspect sources and pair records
- job_kill
- bash — List Panini falsification artifacts
- bash — Inspect pairs334_axes artifact
- bash — Inspect sigs, revalidation, graph
- … et 120 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo root and reports
- **T1** Show recent commits and status
- **T1** Find Panini/4A related files
- **T1** Read Panini-Nipada method doc
- **T1** Inspect 334 artifacts sizes
- **T1** Inspect panini-334.json structure
- **T1** Locate Panini repo
- **T1** Search Panini repo for 334 artifacts
- **T1** Inspect sources and pair records
- **T1** List Panini falsification artifacts
- **T1** Inspect pairs334_axes artifact
- **T1** Inspect sigs, revalidation, graph
- **T1** List signed nodes with metadata
- **T1** Inspect sections and metadata in pairs
- **T1** List nipada dirs and corpus cache
- **T1** Map signatures to graph metadata
- **T1** List signature keys
- **T1** Find §334 write-up
- **T1** Recompute signature intersection
- **T1** Inspect pair node metadata
- **T1** Inspect node schema
- **T1** Count candidate contemporaneous pairs
- **T1** Inspect Drave 488-pair artifact
- **T1** Inspect v150 validation artifact
- **T1** Compute pair feasibility over 57 signed nodes
- **T1** Recompute pair feasibility with counter
- **T1** List exact G1 candidate pairs
- **T1** Search for B1 task description
- **T1** Read Panini 334 technical report part 1
- **T1** Read rest of Panini 334 report
- **T1** Read panini_334 tool
- **T1** List 44 works metadata
- **T1** Compute candidate counts for 44 works
- **T1** G1 feasibility with 57 signed nodes and large traditions
- **T1** Inspect all dated graph nodes
- **T1** Raw-label G1 candidates among 44
- **T1** Check other graph versions for signatures
- **T1** Search signature artifacts
- **T1** Inspect other signature artifacts
- **T1** Inspect aggregated and propagated signatures
- … et 91 autres

## 4. Mesures et résultats marquants

- **T1** `6560a0a5 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612)`
- **T1** `2d7a7f2b 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5)`
- **T1** `ce7241d5 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS`
- **T1** `> **Ce qui se reproduit** : votre loi H0 tient (**R² = 0,909139** sur les 655 lignes ;`
- **T1** `> **0,906307** sur les 488 paires uniques non auto). Le retrieval brut donne **61,4 %** de même`
- **T1** `> tradition (hasard 22,4 %).`
- **T1** `| retrieval même tradition | — | **61,4 %** (hasard 22,4 %) |`
- **T1** `| même tradition à ≤ 50 ans | — | **56,8 %** (hasard 22,8 %) |`
- **T1** `| filiation après contrôles croisés | — | **50,0 %** (p = 0,0492 ; Holm 0,128) |`
- **T1** `| époque après contrôles croisés | — | **53,8 %** (p = 0,373) |`
- **T1** `[still running after 60000ms; moved to background job bash-8]`
- **T1** `{"features": ["intercept", "d_graph", "dyear_per_1000y", "same_tradition"], "ols_dsig": {"beta": [0.1594, 0.0489, 0.1378, 0.0022], "r2": 0.3004}, "ols_drefl": {"beta": [0.7014, -0.0279, -0.0365, -0.11`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:335:| B11.2 | **Le parseur natif typé** : `route` 31,63 M, pooling moyen, 15 têtes | ⚠️ **partiel** | réel seul : **48,3 % train / 0 % validation** (surappren`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:336:| B11.3 | **Le codec classique** : lecture surface → RSN | ✅ **mesuré** | **79/79** et **449/449** RSN exactes (100 %) ; **surface originale 33/79** |`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:337:| B11.4 | **Données synthétiques / distillation du codec** | ✅ **mesuré** | 10 556 surfaces synthétiques, 71 langues, **aucune surface réelle** à l'entraî`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:338:| B11.5 | **Cohérence inter-langues du natif** | ⚠️ **partiel** | normalisation lexicale : **55,7 %** de code exact et **37,0 %** d'invariance (contre 45,`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:339:| B11.6 | **Codec + contexte, mémoire** | ✅ **mesuré** | codec **528/528** avec contexte (100 %) ; sans contexte **374/528** (70,8 %) ; mémoire 470 cibles`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:340:| B11.7 | **Natif contextuel** | ⚠️ **partiel** | contexte **suffixé** : **59,8 %** de code exact et **40,7 %** d'invariance ; contexte **préfixé** : 0,4 `
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:341:| B11.8 | **Contexte séparé** | ❌ **sans gain** | vecteur de contexte 512 + MLP : **59,1 %** / **40,7 %**, contre **59,8 %** / **40,7 %** pour le suffixe `
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:342:| B11.9 | **Restitution du code** | ✅ **mesuré** | **79/79** et **449/449** rendus, **aller-retour RSN 100 %** ; **surface originale 33/79** ; sans décode`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:343:| B11.10 | **Cartes et ambiguïtés** | ⏳ **suivant** | `carte` **69,3 %** ; symbole du morpion, chemin des dames ; le codec lit 100 % |`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:355:| B12.1 | **Bus + hub M1** | ✅ **mesuré** | **528/528** exact avec contexte ; sans contexte **70,8 %** ; canonique **100 %** ; invariance **100 %** ; 1 58`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:356:| B12.2 | **M2 voies ventrales/dorsales** | ⚠️ **vu + règles** | `aug-formes` : `de` **95,2 %, inédit 13/20**, `chemin_0` **88,1 %, 6/14** ; `aug-pos` : ``
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:359:| B12.5 | **M5 prédictif** | ⚠️ **contexte** | sans contexte : action 97,5 % = majoritaire ; avec plateau : source **3,224→2,598 nat** (+5,9 pts), cible *`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:360:| B12.6 | **M6 gating** | ⚠️ **sélecteur** | tâche sens/langue 94,95 % (base 50 %) mais conflit **0**, commutation **0** ; langue seule 88,6 % ; pas un co`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:361:| B12.7 | **M7 neuromodulation** | ❌ **nul** | 3,64 % = plafond 16/439 ; LFU +23,1 pts sur les répétés, nouveauté −19,6, incertitude −38,7, récompense −53`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:362:| B12.8 | **M8 sommeil** | ❌ **marginal** | 96,48 % de champs mais exact **65,1 %**, baseline par jeu **96,10 %** ; leave-one-code-out exact **0 % par con`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:363:| B12.9 | **M9 lésion** | ✅ **table** | contexte **29,2 %** ; M2 ventrale **24,7 %** ; M2 dorsale **2,1 %** ; M7 **13,7 %** ; M3 **0** ; M4 **0** ; M5 **1`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:364:| B12.10 | **Pipeline M1 → M4 → M8** | ⚠️ **intégration** | **528/528**, 7 prototypes, 96,33 % de complétion — tautologique : M4 ne généralise pas, M8 est`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:372:| B19.1 | **M2 secours hors codec** | ⚠️ **typos seulement** | M1 original **100 %**, casse **98,7 %**, phrase **86,6 %** ; M1 espaces **34,8 %**, typo **`
- **T1** `> de séparer les deux.** La loi H0 de Panini se reproduit (**R² = 0,909139** sur les **655 lignes** de`
- **T1** `> Sur les **44 signatures** (14 parts flottantes), le retrieval brut donne **61,4 %** de même tradition`
- **T1** `> (hasard 22,4 %) et **56,8 %** de voisins à ≤ 50 ans (hasard 22,8 %) ; les contrôles croisés ramènent`
- **T1** `> la filiation à **50,0 %** (p = 0,0492, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,373). Seule une`
- **T1** `> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0086, **Holm 0,034**).`
- **T1** `> `analytic_sigs_v1.json` (**44 œuvres × 14 atomes**), `sources_coverage.json` / `sources_manifest.json``
- **T1** `| **H0 officielle** (655 lignes) | 655 | **0,909139** | reproduction bit-exacte de Panini (écart 3 × 10⁻⁷) |`
- **T1** `| **époque seule** | 488 | **0,257876** | la date seule explique 25,8 % |`
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
- **T1** `4. **Sur les 44 signatures**, le brut penche pour la filiation (61,4 % vs 22,4 %) et pour l'époque`
- **T1** `(56,8 % vs 22,8 %), mais les contrôles croisés ramènent la filiation à 50,0 % (p = 0,0492, Holm`
- **T1** `0,128) et l'époque à 53,8 % (p = 0,373). **Aucun des deux n'est fort**.`
- **T1** `(R² = 0,042, p = 0,0086, Holm 0,034) : il reste une trace d'époque, mais 96 % de la variance`
- **T1** `**petite** prédiction d'année intra-tradition (R² = 0,042, Holm 0,034) ; la filiation est **marginale**`
- **T1** ``d_lex ~ d_topo^0,67` (R² = 0,909139 officiel) est reproduite, puis opposée`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
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
- **T1** `64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 cano`
- **T1** `93:- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](..`
- **T1** `**Mis à jour : 2026-11-15, 02 h 32 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **5`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet`
- **T1** `48:**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (has`
- **T1** `184:   suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du pla`
- **T1** `202:[B1–B12] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `203:[B10.2bis] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `204:[B10.3] lasts 2 days and is 15% complete and is colored in #b03a2e`
- **T1** `205:[B11.10] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `277:| **B11** | la base d'universaux typés : schéma, [parseur](../theorie/glossaire/entrees/parseur.md), codec, contexte | ✅ | **B11.10 close** (cartes, ambiguïtés refusées) ; le codec lit **100 %** |`
- **T1** `279:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `354:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `49:- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; `
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `[still running after 60000ms; moved to background job bash-131]`

## 5. Erreurs rencontrées

7 sorties en erreur ou divergentes. Les premières :

- **T1** : dated signed 49 ('tao_te_ching_legge_en', -600, 'lzh', 'DAOISM', None, 'Laozi (Legge)') ('mozi_selections', -400, 'lzh', 'CHINESE_RATIONALIST', None, 'mozi') ('great_learning_legge_en', -400, 'lzh', '
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 1, in <module>   File "<string>", line 71          ^ IndentationError: expected an indented block after 'while' statement on line 70 
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/diag.py", line 1, in <module>     exec(open('/tmp/select_proto2.py').read().split("best=None")[0])     ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module> AssertionError [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 38, in <module>   File "<stdin>", line 31, in pool   File "<stdin>", line 24, in base_ok KeyError: 'work' [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 10, in <module> AssertionError [exit code: 1]
- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r

## 6. Commits

- B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE" -m "Le manifeste reports/proto


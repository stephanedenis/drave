# Session session- — Prédiction Drave par atomes

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-10414d5d-1d81-4840-b524-e77375127547` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 03:06 |
| Durée | 0.7 h |
| Tours | 1 |
| Messages | 198 |
| Appels d'outils | 203 |
| Fichiers touchés | 0 |
| Commandes | 189 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche B2 : les 14 atomes comme prédicteurs des 8 niveaux Drave — sur les 44 œuvres × 14 flottants (JSON plat, lecture seule chez Panini), mesure la prédiction d'un niveau (POS, syntagmes, attachement) par les atomes, avec le contrôle de permutation des colonnes et le contrôle de date ; fiche `reports/rapport-atomes-prediction.md` + JSON.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche B2 : les 14 atomes comme prédicteurs des 8 niveaux Drave — sur les 44 œuvres × 14 flottants (JSON plat, lecture se … [219 caractères tronqués]

*203 appels d'outils.* Actions notables :

- bash — List repo root and recent commits
- bash — List reports and journal directories
- bash — Inspect existing atomes-niveaux.json
- bash — Find B2 in roadmap
- bash — Search for 14 floats references
- bash — Inspect Panini repo
- bash — Read B2 task description and inventory excerpt
- bash — Read existing atomes-niveaux report
- bash — Search B2 references everywhere
- bash — Read REPRISE.md
- bash — Search state for atomes/B2
- bash — Read current state header
- bash — Inspect Panini falsification dir and signatures
- bash — List Panini corpus files
- … et 177 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo root and recent commits
- **T1** List reports and journal directories
- **T1** Inspect existing atomes-niveaux.json
- **T1** Find B2 in roadmap
- **T1** Search for 14 floats references
- **T1** Inspect Panini repo
- **T1** Read B2 task description and inventory excerpt
- **T1** Read existing atomes-niveaux report
- **T1** Search B2 references everywhere
- **T1** Read REPRISE.md
- **T1** Search state for atomes/B2
- **T1** Read current state header
- **T1** Inspect Panini falsification dir and signatures
- **T1** List Panini corpus files
- **T1** Find 334 metadata files
- **T1** Find date sources in 334 report
- **T1** Find linguistic tools
- **T1** Find POS scripts and reports
- **T1** Inspect panini_334 tool
- **T1** Inspect bloc_linguistique tool
- **T1** Read Analyzer API
- **T1** Read loader for works and dates
- **T1** Read paths and constants
- **T1** Load 44 works metadata via panini_334
- **T1** Inspect sources manifest
- **T1** Print manifest and coverage entries
- **T1** Inspect coverage and manifest lists
- **T1** Check text availability and sizes
- **T1** Find attachment output fields
- **T1** Read language block report header
- **T1** Run heuristic analyzer on a sample
- **T1** Find text cleaning code
- **T1** Read Gutenberg cleaner
- **T1** Check Gutenberg markers and starts
- **T1** Find largest texts and check pdftotext
- **T1** Time full analysis of largest text
- **T1** Inspect POS/syntagme tag names
- **T1** Check running analysis process
- **T1** Word counts of 44 works
- **T1** Find signature computation code
- … et 149 autres

## 4. Mesures et résultats marquants

- **T1** `6560a0a5 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612)`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `docs/pilotage/semaine-autonome.md:70:| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexica`
- **T1** `docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 lan`
- **T1** `docs/pilotage/roadmap.md:354:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
- **T1** `reports/rapport-inventaire-panini.md:369:| **§334 (philosophie/religion)** | 114 textes actifs ; 102 fichiers `sources/` (9,5 Mo) ; signatures de 44 œuvres | `.txt` un fichier par œuvre + signatures J`
- **T1** `reports/rapport-inventaire-panini.md:407:2. **Signatures 14 atomes** : **44 œuvres** × 14 flottants (somme 1), en JSON pur. Livrable : table`
- **T1** `reports/rapport-atomes-niveaux.md:7:> 44 œuvres de Panini montre **33 paires d'atomes à |r| ≥ 0,5** (brut), **4 composantes > 1** et **80,7 %** de`
- **T1** `reports/rapport-atomes-niveaux.md:53:- `../../Panini/research/nipada/falsification/analytic_sigs_v1.json` : 44 œuvres × 14 parts, somme 1.`
- **T1** `reports/rapport-panini-334.md:24:> `analytic_sigs_v1.json` (**44 œuvres × 14 atomes**), `sources_coverage.json` / `sources_manifest.json``
- **T1** `(R² 0,30) — la surface capte l'époque ; tout test de style contrôle la date, tout test de famille`
- **T1** `| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |`
- **T1** `| API REST | `src/nipada/api/api.py`, `server.py` | FastAPI : `/decompose`, `/reconstruct`, `/roundtrip`, `/compare`, `/atoms`, `/dhatus`, `/benchmark`, `/search`, `/hypotheses`, `/api/v1/*` | fastapi`
- **T1** `2. **Signatures 14 atomes** : **44 œuvres** × 14 flottants (somme 1), en JSON pur. Livrable : table`
- **T1** `cassés, backlog P0 entièrement « À faire ». **Ne pas promettre du 0 % WER.**`
- **T1** `> 44 œuvres de Panini montre **33 paires d'atomes à |r| ≥ 0,5** (brut), **4 composantes > 1** et **80,7 %** de`
- **T1** `- `../../Panini/research/nipada/falsification/analytic_sigs_v1.json` : 44 œuvres × 14 parts, somme 1.`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:166:| B2.1 | **La RSN** : une représentation partagée, mais non alignée | ✅ | pont 28-69 %, cos 0,78-0,92, insensible à la taille |`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:172:| B2.7 | **Le 32 B** : la profondeur et l'alignement à une échelle de plus | ✅ mesuré — **le confondant tranché** | à profondeur relative fixe (50 %), le `
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:173:| B2.8 | **Le raisonnement naturel à l'échelle** : XNLI au 14 B/32 B, et un corpus naturel plus dur | ✅ mesuré | **DACCORD +26,9, GQNLI +56,7, XNLI +35,9*`
- **T1** `reports/rapport-c9-echange-experts.md:74:| un **troisième** texte (B2) | 34,6692 (×0,93) | — | — |`
- **T1** `reports/rapport-consolidation-structure-partagee.md:27:| **B2** (rejeu des 20 premiers) | corpus_en | **19,4392 (−22,5 %)** | 4,6391 (−3,6 %) | **17,3258 (+1,2 %)** |`
- **T1** `reports/pensee-partition-syntagmes.json:9: "verdict": "Les 239 paires des deux bancs sont **toutes** des paires S × chunker : 53,1 % de S qui contient le chunker, 33,5 % l'inverse, 2,5 % de mêmes born`
- **T1** `reports/rapport-partition-syntagmes.md:28:| Option B2 (partition stricte) | F1 **0,6172**, exact **205/239**, **0 paire** ; **+2,0 %** de JSON |`
- **T1** `reports/rapport-partition-syntagmes.md:215:| B2 | 0 | 0 | 545 | 397 | 1 967 190 | **+2,0 %** | 466 |`
- **T1** `- **sérialiser les gros lecteurs de disque** (deux lecteurs de 63 Go en parallèle : 8,6 Mo/s) ;`
- **T1** `l'Instruct et diffèrent de **1,5 à 2,5 %** de celles du base ; une différence f32 ne peut pas`
- **T1** ``--test m20` n'était pas un test — la fuite valait **×8** sur la perplexité, et trois énoncés`
- **T1** `93:- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](..`
- **T1** `**Mis à jour : 2026-11-15, 02 h 32 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **5`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canoniq`
- **T1** `24:> `analytic_sigs_v1.json` (**44 œuvres × 14 atomes**), `sources_coverage.json` / `sources_manifest.json``
- **T1** `145:| **époque seule** | 488 | **0,257876** | la date seule explique 25,8 % |`
- **T1** `230:| **tradition, kNN k=1** | exactitude **61,4 %** ; équilibrée **30,6 %** | majorité **43,2 %** ; null date **50,0 %** (p = 0,043) | l'exactitude est portée par GRECO (19/44) |`
- **T1** `231:| **tradition, équilibrée** | **30,6 %** | null date **22,0 %** (p = 0,092) | pas significatif après date |`
- **T1** `237:équilibrée** (30,6 %) et le null de date (22,0 %, p = 0,092) montrent que le modèle retrouve surtout`
- **T1** `244:donne **R² = 0,016** : la tradition n'explique presque rien de la similarité des signatures, et la date`
- **T1** `257:`d_sig ≈ 0,159 + 0,049·d_graph + 0,138·(Δyear/1000) + 0,002·même_tradition`, **R² = 0,3004**.`
- **T1** `> substituables, un parallèle et une cascade, une activation sémantique à **51–76 %** ; la`
- **T1** `bengio_2003 63198 False '%PDF-1.1 % 2 0 obj < < /Length 5589 /Filter /LZWDecode >> stream \x10y\x18l \x18 `P\\9\x1b\x06\x11!\x04: A eR_BT'`
- **T1** `[still running after 60000ms; moved to background job bash-36]`
- **T1** `==== bengio_2003 66060 b'%PDF-1.1 % 2 0 obj < < /Length 5589 /Filter /LZWDecode >> st'`
- **T1** `ne-height:1.75;--reader-max-width:760px;--reader-font-family:"Source Serif 4 Variable", "Iowan Old Style", Charter, Georgia, "Times New Roman", serif;--reader-background:var(--background);--reader-for`
- **T1** `[still running after 60000ms; moved to background job bash-85]`
- **T1** `[still running after 60000ms; moved to background job bash-103]`
- **T1** `[still running after 60000ms; moved to background job bash-105]`
- **T1** `reports/rapport-base-reelle.md:7:> 86,25 %) et la **F1 est la même** (79,06 % contre 79,02 %) — le synthétique n'aidait donc **pas**`
- **T1** `reports/rapport-base-reelle.md:18:| POS | 86,25 % | **88,91 %** (fermé 92,94 / ouvert 84,66) |`
- **T1** `> de séparer les deux.** La loi H0 de Panini se reproduit (**R² = 0,909139** sur les **655 lignes** de`
- **T1** `> Sur les **44 signatures** (14 parts flottantes), le retrieval brut donne **61,4 %** de même tradition`
- **T1** `> (hasard 22,4 %) et **56,8 %** de voisins à ≤ 50 ans (hasard 22,8 %) ; les contrôles croisés ramènent`
- **T1** `> la filiation à **50,0 %** (p = 0,0492, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,373). Seule une`
- **T1** `> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0086, **Holm 0,034**).`
- **T1** `> `analytic_sigs_v1.json` (**44 œuvres × 14 atomes**), `sources_coverage.json` / `sources_manifest.json``
- **T1** `| 05:37 | `bb68b820` | J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0`
- **T1** ``61,4 %` · `50,0 %` · `56,8 %` · `53,8 %` · `0,0089` · `0,128` · `0,373` · `0,042` · `0,034` · `0,006` · `0,138``
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `ACP {'valeurs_propres': [4.5645, 2.8967, 1.7096, 1.4529, 1.2282, 0.6867, 0.4765, 0.2197, 0.1377, 0.0799, 0.0176, 0.0059, 0.0058], 'variance_expliquee': [0.3386, 0.2149, 0.1268, 0.1078, 0.0911, 0.0509,`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `354:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `| **R0.2** | **[contrôleur de lecture](../theorie/glossaire/entrees/controleur-de-lecture.md)** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, tit`
- **T1** `| **R0.3** | **[banc de lecture rapide](../theorie/glossaire/entrees/banc-de-lecture-rapide.md)** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles`
- **T1** `| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 langues*`
- **T1** `48:**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (has`
- **T1** `contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même`
- **T1** `tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à`
- **T1** `**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction`
- **T1** `d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150`
- **T1** `363:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `36:| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `-| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 langues`
- **T1** `+| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 langues`
- **T1** `-**Mis à jour : 2026-11-15, 02 h 32 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`

## 5. Erreurs rencontrées

9 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 8, in <module> TypeError: list indices must be integers or slices, not dict [exit code: 1]
- **T1** : (no output) [exit code: 2]
- **T1** : ==== 2_esdras 103170 b'// Apply the local archive-bar preference before shared HTML' *** START -1 ***START -1 Project Gutenberg -1 <script -1 <body -1 Chapter 52125 CHAPTER -1 ==== bengio_2003 66060 b
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 23, in <module>   File "<stdin>", line 18, in cv_ridge ValueError: operands could not be broadcast together with shapes (1,43) (20,) 
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 16, in <module> ValueError: operands could not be broadcast together with shapes (580,29) (20,29)  [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 9, in <module> TypeError: _design_date() takes 1 positional argument but 2 were given [exit code: 1]
- **T1** : keys ['fiche', 'version', 'date', 'titre', 'statut', 'source', 'atomes', 'cohorte_primaire', 'n', 'familles', 'metriques', 'metriques_ecartees', 'permutations', 'null_col', 'null_resid', 'null_date_in
- **T1** : distribue.md docs.md mesures.md portes.md README.md === distribue.md docs.md memoire.md mesures.md moteur.md portes.md README.md === # 2026-11-14 — Régions, flux, protocoles, budgets, pannes  > **Géné
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 16, in <module> AssertionError [exit code: 1]

## 6. Commits

- B2 — LES ATOMES NE PRÉDISENT PAS POS, SYNTAGMES NI ATTACHEMENT : SUR 28 ŒUVRES PROPRES, R² −0,092 / −0,160 / −0,092 (p 0,56 / 0,85 / 0,67) ; LE STYLE EST PRÉDIT


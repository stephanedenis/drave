# Session session- — Généalogie à deux faces : Panini vs Glottolog

> **Journaux :** [le jour](../../2026-11-07/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-07 17:59 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 109 |
| Appels d'outils | 137 |
| Fichiers touchés | 0 |
| Commandes | 127 |
| Sous-agents | 0 |
| Commits | 4 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J3.2 : la généalogie à deux faces — confronter la théorie de Panini (14 atomes, 9 dhātus) à nos mesures d'alignement (Glottolog) sur le corpus commun. Fiche `reports/rapport-genealogie-deux-faces.md` + JSON : ce qui converge, ce qui diverge, ce qui reste à mesurer. La théorie va dans `docs/theorie/genealogie-des-langues.md` (mise à jour), les chiffres restent dans reports/.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J3.2 : la généalogie à deux faces — confronter la théorie de Panini (14 atomes, 9 dhātus) à nos mesures d'aligneme … [262 caractères tronqués]

*137 appels d'outils.* Actions notables :

- bash — Inspect workspace root and recent history
- bash — List theory, method and reports directories
- read
- bash — Find Panini/genealogy related reports
- bash — Search for J3.2 mentions
- bash — List language/corpus reports
- bash — Find J3.2 task definition
- bash — Locate tools and inspect genealogy data
- bash — Inspect corpus-commun JSON structure
- bash — Read J3.1/J3.2 task definitions
- bash — Inspect genealogy tool head
- bash — Inspect Panini repository
- bash — Find signature computation scripts in Panini
- bash — Find dhātu documentation
- … et 115 autres

**Synthèse produite :**

**J3.2 livré et committé.** La confrontation est faite sur les 21 langues du corpus commun, avec trois sections explicites : ce qui converge, ce qui diverge, ce qui reste à mesurer.

\## Fichiers

- **Fiche** : [`reports/rapport-genealogie-deux-faces.md`](reports/rapport-genealogie-deux-faces.md)
- **JSON** : [`reports/genealogie-deux-faces.json`](reports/genealogie-deux-faces.json) (210 paires, groupes, régressions, permutations, LOO, ACP, §150)
- **Outil reproductible** : [`tools/genealogie_deux_faces.py`](tools/genealogie_deux_faces.py)
- **Théorie mise à jour** : [`docs/theorie/genealogie-des-langues.md`](docs/theorie/genealogie-des-langues.md) — les chiffres J3.2 restent dans `reports/`.
- État, roadmap, journal et index mis à jour.

**Commits** : `c2e629b3` (J3.2) et `c3467170` (les prérequis J2.2/J3.1, qui étaient restés stagés).

\## Ce qui converge

- **La surface passe avant la filiation des deux côtés.** Panini : β époque 0,1378 > β filiation 0,0489. Drave : toutes les paires hors script sont au hasard.
- **Rapport filiation/surface du même ordre** : 0,0489/0,1378 = **0,355** chez Panini ; 0,181/0,609 = **0,297** en J3.1.
- **Même arbre là où les deux généalogies existent** : 15/15 familles appariées, 14/15 branches au nœud exact, Spearman 0,657 / Pearson 0,918 sur les 105 paires couvertes.
- **Prédiction comparable** : R² 0,256 (Panini UDHR) contre 0,230 (Glottolog) ; l’écart est petit mais stable (positif dans les 21 retraits).

\## Ce qui diverge

- **L’objet de la « filiation »** : le §150 de Panini est une distance de **tradition** — **3/655** paires ont deux langues connues différentes, 173 sont `eng–eng`, 479 ont une langue vide. Ce n’est pas une distance de famille de langues.
- **La couverture** : `lang_distance` (LANG_TREE) couvre **5/21** langues (**200/210** paires « inconnues ») ; les métadonnées UDHR **15/21** (**105/210**) ; Glottolog **21/21**. Les 6 langues non labellisées par Panini sont toutes non indo-européennes, et les 4 paires de même branche sont précisément codées « inconnu » par LANG_TREE.
- **La granularité** : l’échelle à 4 niveaux n’utilise jamais 0,15 sur ces 21 langues ; son niveau 0,40 mélange `eng–fra` (MRR 0,952) et cinq paires au plancher ; « inconnu = 1,0 » est une valeur manquante, pas une distance.
- **La porte du script** : **154/154 paires hors script sont au hasard exact** (MRR 0,1332 = H₃₀/30 ; top-1 0,0333 = 1/30). Le signal de famille ne vit que dans **56 paires de même script**, et il est porté par **2-3
… [1226 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Inspect workspace root and recent history
- **T1** List theory, method and reports directories
- **T1** Find Panini/genealogy related reports
- **T1** Search for J3.2 mentions
- **T1** List language/corpus reports
- **T1** Find J3.2 task definition
- **T1** Locate tools and inspect genealogy data
- **T1** Inspect corpus-commun JSON structure
- **T1** Read J3.1/J3.2 task definitions
- **T1** Inspect genealogy tool head
- **T1** Inspect Panini repository
- **T1** Find signature computation scripts in Panini
- **T1** Find dhātu documentation
- **T1** Find reports mentioning Glottolog
- **T1** Read Panini README theory sections
- **T1** Search dhatu mentions in docs
- **T1** Find beta coefficients source
- **T1** Read V14 and dhatu sections
- **T1** Find Panini genealogy docs
- **T1** Inspect analytic signatures file
- **T1** Find generator of analytic signatures
- **T1** List falsification and nipada dirs
- **T1** Inspect Panini linguistic distance outputs
- **T1** Read signature generator script
- **T1** Inspect Panini corpus metadata structures
- **T1** Read measure 49 of common layer
- **T1** Read family reports
- **T1** Read inter-language report
- **T1** Find branch alignment numbers
- **T1** List JSON top-level keys
- **T1** Inspect genealogy and metadata records
- **T1** Read inventory section on language distance
- **T1** Locate lang_distance implementation
- **T1** Find distance convention context
- **T1** Find Panini UDHR decomposition files
- **T1** Inspect Panini UDHR V14 files
- **T1** Inspect Panini UDHR corpus metadata
- **T1** Inspect Panini UDHR corpus structure fully
- **T1** Inspect selection structure
- **T1** List 21 texts with both genealogies
- … et 87 autres

## 4. Mesures et résultats marquants

- **T1** `9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`
- **T1** `docs/pilotage/roadmap.md-33-| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `docs/pilotage/roadmap.md-34-| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tr`
- **T1** `docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 lan`
- **T1** `docs/pilotage/roadmap.md-36-| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte `
- **T1** `docs/pilotage/roadmap.md-38-**État au 07/11 14 h 40.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r0`
- **T1** `docs/pilotage/roadmap.md-251-| **R0.3** | **[banc de lecture rapide](../theorie/glossaire/entrees/banc-de-lecture-rapide.md)** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage`
- **T1** `docs/pilotage/roadmap.md:253:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
- **T1** `../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md:588:- NIPADA : 14 atomes vs ~250 FL → trop grossier. Solution : 9 dhātus → ~250 FL (96% de réduction)`
- **T1** `../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md:1181:Fondation algébrique (14 atomes + 9 dhātus) ≠ statistique (100B+ paramètres). SAT déterministe ≠ stochastique. 0% hallucination ≠ `
- **T1** `**Résultat** : couverture NSM de 89% (58/65) → **100% (65/65)**. Confiance de 0.780 → 0.891 (+0.111). Total : 14 + 6 = 20 primitives.`
- **T1** `Les 9 Dhātus remplacés par 49 Fonctions Lexicales (Mel'čuk) dans le pipeline de décomposition. Granularité LF : ×5.4 vs Dhātus. Mapping vers ~250 fonctions RLF avec 80% de réduction (§566).`
- **T1** `- NIPADA : 14 atomes vs ~250 FL → trop grossier. Solution : 9 dhātus → ~250 FL (96% de réduction)`
- **T1** `D8["D8: 0% WER = templates (20 textes)"]`
- **T1** `D1["D1: R²=0.32 vs 0.91"]`
- **T1** `{"date": "2026-04-23", "system": "nipada", "version": "0.3.0", "model": "paraphrase-multilingual-MiniLM-L12-v2", "n_languages": 21, "n_molecules": 15, "H1_causer_11": {"r2": 0.5750081539154053, "cosin`
- **T1** `# C3.2c — les 9 familles : 7 sur 9 au-dessus de 30 %`
- **T1** `## Résultats (8 textes, contrôle 0 %)`
- **T1** `| indo-européen | 98 | 0,0 % | **14,7 %** | 0,0 % |`
- **T1** `| atlantic-congo | 74 | — | **94,0 %** | 0,0 % |`
- **T1** `| **quechuan** | 11 | 33,3 % | **88,2 %** | 0,0 % |`
- **T1** `| **mayan** | 9 | 8,9 % | **64,4 %** | 0,0 % |`
- **T1** `| **afro-asiatic** | 12 | 0,0 % | **60,2 %** | 0,5 % |`
- **T1** `| austronesian | 35 | — | **61,0 %** | 0,0 % |`
- **T1** `| **uralic** | 9 | 31,0 % | **46,7 %** | 0,0 % |`
- **T1** `| turkic | 14 | — | **96,1 %** | 0,0 % |`
- **T1** `| sino-tibetan | 17 | 40,5 % | **100,0 %** | 0,0 % |`
- **T1** `- **Moyenne des 9** : **69,5 %** ; **médiane** : **64,4 %**.`
- **T1** `- **7 familles sur 9** dépassent **30 %** ; **1 seule** (indo-européen) est sous **30 %**.`
- **T1** `- Le **contrôle** reste **≤ 0,5 %** partout.`
- **T1** `- La **taille** n'explique pas tout : l'**indo-européen** (98 langues) est **dernier** à **14,7 %**,`
- **T1** `tandis que le **quechuan** (11 langues) est à **88,2 %**.`
- **T1** `différentes ; l'uralic (9 langues) reste à **46,7 %** malgré sa petite taille.`
- **T1** `- **4 nouvelles familles** : **3 sur 4** au-dessus de **60 %** ; l'**uralic** est le négatif.`
- **T1** `- Le **contrôle** à 0 % montre que le module **recopie** sa famille, sans perroquet.`
- **T1** `- **200 pas**, rang 8, 8 textes ; un seul run par famille.`
- **T1** `- Le **sino-tibetan** partait de **40,5 %** avant entraînement (connaissance préalable).`
- **T1** `**C3.2c est close sur les 9 familles** : **7/9 > 30 %**, moyenne **69,5 %**, contrôle **0 %**. Le`
- **T1** `module par famille **casse la chute** pour la majorité, mais l'**indo-européen** (14,7 %) et`
- **T1** `l'**uralic** (46,7 %) montrent que l'**hétérogénéité interne** est le vrai facteur.`
- **T1** `# C3.2d — l'indo-européen à 14,7 % est un effet de composition`
- **T1** `> **Objet.** L'indo-européen (98 langues) était la seule famille sous **30 %** en C3.2c (14,7 %).`
- **T1** `| **indo-iranien** | 26 | 0,0 % | **100,0 %** |`
- **T1** `| **baltique** | 15 | 12,5 % | **95,3 %** |`
- **T1** `| **italique** | 29 | 11,4 % | **87,6 %** |`
- **T1** `| **celtique** | 5 | 0,0 % | **79,9 %** |`
- **T1** `| **germanique** | 20 | 0,0 % | **54,6 %** |`
- **T1** `| *indo-européen entier* | *98* | *0,0 %* | ***14,7 %*** |`
- **T1** `- **Toutes** les sous-familles dépassent **54 %** ; l'IE entier reste à **14,7 %**.`
- **T1** `- Le **contrôle** est à **0 %** partout.`
- **T1** `- Le **14,7 %** de l'IE n'est pas une incapacité du module : c'est un **effet de composition**.`
- **T1** `Les sous-familles apprennent **54,6 à 100 %**, mais un module **unique** entraîné sur 98 langues`
- **T1** `- La **germanique** est la plus basse (**54,6 %**) : c'est la sous-famille la plus **hétérogène**`
- **T1** `- L'**indo-iranien** atteint **100 %** : sous-famille nombreuse mais **plus homogène**.`
- **T1** `- La **taille** n'explique pas tout : le celtique (5 langues) est à **79,9 %**, la germanique`
- **T1** `(20 langues) à **54,6 %**.`
- **T1** `**C3.2d explique C3.2c** : l'IE à 14,7 % est un **effet de composition**, pas une difficulté`
- **T1** `- **200 pas**, rang 8, un seul run par sous-famille.`
- **T1** `adaptateur **linéaire** (896×896) suivi d'une tête **gelée** ne peut pas battre un modèle de`
- **T1** `domaine ×2,6) parce que les deux corpus sont du **français** ;`
- **T1** `reports/rapport-cache-chunker.md:153:| 160 | 48 | 16 | 27,88 | 27,27 | 13,55 | 30,76 | ×1,02 | ×2,06 | ×0,91 |`
- **T1** `reports/rapport-croisement-push-pull.md:107:   moteur gagne ×2,27 de bout en bout (13,6 → 30,7 tok/s, 510 jetons) à basculer`
- **T1** `reports/rapport-design-H-profondeur-routee.md:71:| 0,70 | 30,7 % | 42,78 % | 47,23 % | 63,36 % | 40,09 % |`
- **T1** `reports/rapport-e9-homeostasie.md:11:> **−15,24 %** (contre −16,11 %, légèrement moins bien) et hors domaine **−0,58 %** — c'est-à-dire`
- **T1** `reports/rapport-e9-homeostasie.md:28:| **×0,6** | **6,7751** | **−8,75 %** | 16,2096 | −15,24 % | **17,1671** | **−0,58 %** |`
- **T1** `reports/rapport-e9-homeostasie.md:32:| **×1,25** | 7,0243 | −5,39 % | 16,2203 | −15,20 % | 17,5506 | **+1,64 %** |`
- **T1** `reports/rapport-e9-homeostasie.md:87:| 0 | **×0,6** | 6,7751 | −8,75 % | 16,2096 | −15,24 % | 17,1671 | **−0,58 %** |`
- **T1** `reports/rapport-e9-homeostasie.md:118:| **uniforme ×0,6** | **6,7751** | **−8,75 %** | **16,2096** | **−15,24 %** | 17,1671 | −0,58 % |`
- **T1** `reports/rapport-etat-a.md:49:| **A7** grappe déportée | ✅ fait | A3, A4 | greffe **648 s** ; **1 608 octets/flux** ; **0,25 Mbit/s** ; top-1024 rend **30,7286** ; format v2 **4,22×** moins cher ; tran`
- **T1** `reports/rapport-grappe-intra-couche.md:10:| 0 (tout) | 100 % | 30,7286 |`
- **T1** `reports/rapport-grappe-intra-couche.md:13:| **1 024** | **21,1 %** | **30,7286 — la même** |`
- **T1** `reports/rapport-grappe-intra-couche.md:17:- **La grappe exacte existe à 21 %** : le top-1024 rend **exactement** la perplexité du réseau complet (30,7286 à`
- **T1** `33-58 Mo à charger : **à tester avant de s'y engager**.`
- **T1** `**époque +0,1378**, **filiation +0,0489**, tradition +0,0022, R² = 0,3004. H1 (stratification) et H2`
- **T1** `| **UDHR, article 1** | 229 Ko, 532 langues | JSON `udhr-v2.0-xml` : `{name, iso, script, dir, text, family, branch, tradition}` | **532** | `research/data/udhr_corpus.json` (+ `udhr_decomposed_v14.js`
- **T1** `| **UDHR, 30 articles** | 28 Mo | XML `udhr_XXX.xml` + `langues.jsonl`, `genealogie.json`, `familles/*.jsonl` | 456 | `Qtrinet/data/udhr/` | déjà intégré côté Drave |`
- **T1** `| **§334 (philosophie/religion)** | 114 textes actifs ; 102 fichiers `sources/` (9,5 Mo) ; signatures de 44 œuvres | `.txt` un fichier par œuvre + signatures JSON | surtout **anglais** (408 paires), 2`
- **T1** `| **Gutenberg** | 1 999 métadonnées ; **1 943 téléchargés** ; 332 fichiers (271 Mo) ; 5 curatés | SQLite `books(id,title,lang,authors,subjects,downloads,url,fetched)` + `.txt` | en, fr, de, es | `rese`
- **T1** `| **Textes sacrés / suttacentral / MIT Classics** | 21 Mo + 13 Mo + 2 Mo | `.txt` par section | pi, en, gr | `_cache/sacred_texts/`, `_cache/suttacentral/`, `_cache/mit_aristotle_*` | oui |`
- **T1** `| **Protoathéisme (hôte)** | 36 Mo, 42 œuvres | dossiers + `STATUS_PENDING.txt` | en, fr, la… | `Panini/corpus/protoatheism/` | **non : acquisition inachevée** |`
- **T1** `| **Tokens protoathéisme** | 120 Ko | JSONL | — | `Panini/corpus/protoatheism_tokens/` | oui |`
- **T1** `"interpretation_dsig": "d_sig ≈ +0.159 +0.049·d_graph +0.138·(Δyear/1000) +0.002·same_trad  (R²=0.300)",`
- **T1** `| 00:16 | `26c7b7ab` | ROADMAP ET JOURNAL — LA NUIT FINIT À F1 0,7535, POS 86,25 %, 236/237, COUVERTURE 0,9916 ; LA CONVENTION DU SUJET |`
- **T1** `**La nuit du 07/11 (00 h 00 → 01 h 10).** Le bloc finit la nuit à **POS 86,25 %**, **F1 0,7535**`
- **T1** `l'**article 1 de la DUDH** : **21 textes** (20 langues stratifiées, 5 familles × 4, plus le`
- **T1** `**453** fichiers communs, **438** appariables article 1, **418 paires exactes (95,4 %)** ; les`
- **T1** `décalés contiennent 60 % de paires de même écriture, les contemporains 33 %. **Contrôles négatifs** :`
- **T1** ``r035`, 322/180 avant) donnait **144 FP de sujet (45 %)** et 73 d'objet. La règle **sujet hors du`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête `
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 07/11 14 h 40.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé `
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `253:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `0.40 n=  6 above=  1 (17%) mean_above=0.9515`
- **T1** `0.75 n=  4 above=  0 (0%) mean_above=nan`
- **T1** `1.00 n=200 above= 43 (22%) mean_above=0.2037`
- **T1** `0.15 n=  4 above=  3 (75%) mean_above=0.4342`
- **T1** `0.40 n= 14 above=  1 (7%) mean_above=0.9515`
- **T1** `0.75 n= 87 above= 18 (21%) mean_above=0.2071`
- **T1** `1.00 n=105 above= 22 (21%) mean_above=0.1694`
- **T1** `atomes : 4 valeurs propres > 1 (corrélation), 1 (covariance) ; 90 % à 5 composantes`
- **T1** `124:**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035`, convention des GV, schéma v2 et restitution v0 faits**, reste `g017` ; *`
- **T1** `255:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `(R² 0,256 contre 0,230 sur 105 paires). **Ce qui diverge** : l'objet de la « filiation » (tradition chez`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir 0,2276 |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `-- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre `
- **T1** `-- **Panini J2.1** : table **14 atomes × 8 niveaux** ; [fiche](../../reports/rapport-atomes-niveaux.md).`
- **T1** `-**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035`, convention des GV, schéma v2 et restitution v0 faits**, reste `g017` ; **S*`
- **T1** `+**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035`, convention des GV, schéma v2 et restitution v0 faits**, reste `g017` ; **J3`
- **T1** `+| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0`
- **T1** `-**État au 07/11 14 h 40.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé`
- **T1** `+**État au 07/11 18 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé`
- **T1** `| **R0.2** | **[contrôleur de lecture](../theorie/glossaire/entrees/controleur-de-lecture.md)** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, tit`
- … (tronqué)

## 5. Erreurs rencontrées

6 sorties en erreur ou divergentes. Les premières :

- **T1** : /home/stephane/Data13TB/stephane/GitHub/Qtrinet total 208 drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 . drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 .. -rw-r--r--. 1 stephane stephane  99
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 1, in <module> ModuleNotFoundError: No module named 'sklearn' [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/j32/explore2.py", line 39, in <module>     labeled=np.array([a['famille_panini']!='Other' and b
- **T1** : # 2026-11-07  > **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier > [`journal/2026-11-07/`](README.md). Le récit écrit à la main est conservé plus bas, dans > le bloc « not
- **T1** : [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/j32/explore7.py", line 11, in <module>     Y=np.array([mrr[(ids[i],ids[j])] for i,j in pairs]);
- **T1** : [stderr] /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/genealogie_deux_faces.py:173: RuntimeWarning: invalid value encountered in divide   t = b / se Traceback (most recent call last):   File 

## 6. Commits

- PANINI — J2.2 ET J3.1 : LE CORPUS COMMUN (418/438 PAIRES EXACTES, 8/8 CONTRÔLES) ET LE RETRIEVAL À ÉPOQUE CONTRÔLÉE (SCRIPT +0,609, ÉPOQUE −0,034/SIÈCLE, p=0,19
- J3.2 — DEUX FACES : 154/154 PAIRES HORS SCRIPT AU HASARD, PANINI 3/655 PAIRES INTER-LANGUES ET 5/21 LANGUES, LA FAMILLE VIT DANS 2-3 PAIRES" 2>&1 | tail -30
- git commit --amend --no-edit 2>&1 | tail -20
- git commit --amend --no-edit 2>&1 | tail -20


# Session session- — Retrieval Panini par familles Glottolog

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-02ebc573-ec84-46cf-945c-cfd7d563a9fc` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 01:21 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 196 |
| Appels d'outils | 208 |
| Fichiers touchés | 1 |
| Commandes | 183 |
| Sous-agents | 0 |
| Commits | 3 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J7.1 : approfondir le retrieval Panini — sur les 532 langues UDHR (même source XML), mesurer le retrieval par famille Glottolog (les 29 langues de `language_genealogy.py` + l'échantillon 20) avec le contrôle d'époque, et comparer à la mesure de J3.1. Fiche `reports/rapport-retrieval-familles.md` + JSON, contrôle négatif (familles différentes vs sœurs).

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J7.1 : approfondir le retrieval Panini — sur les 532 langues UDHR (même source XML), mesurer le retrieval par fami … [240 caractères tronqués]

*208 appels d'outils.* Actions notables :

- bash — Inspect workspace root and git state
- bash — List reports and journal entries
- bash — Locate J3.1 references and genealogy files
- bash — Locate UDHR and 532-language references
- bash — Read J3.1 retrieval-epoch report and JSON
- bash — Read current state document
- bash — Inspect UDHR data directory and genealogy schema
- bash — Read genealogy UDHR tool
- bash — Find language_genealogy.py and references
- bash — Inspect UDHR metadata and family counts
- bash — Read autonomous week plan and Panini inventory relevant sections
- bash — Locate Panini UDHR source and J3.2 work
- bash — Inspect Panini 532-language UDHR corpus schema
- bash — Read J3.2 genealogy two-faces report
- … et 179 autres

**Synthèse produite :**

**J7.1 terminé — commit `d31e8788`.**

\## Ce qui a été mesuré

**Corpus** : 532 textes UDHR de Panini (article 1, même source XML, 1948), **521 étiquetés Glottolog** (97,9 %), **447 groupes ISO**, **445 textes distincts** après retrait de 74 variantes ISO et 2 doublons de texte exact.

\### 1. Global 532 — la porte d'écriture

| pool | top-1 famille | hasard | top-1 sœur | hasard |
|---|---:|---:|---:|---:|
| toutes (445) | **66,1 %** | 10,3 % | **26,1 %** | 2,5 % |
| même écriture (417) | **69,8 %** | 16,2 % | **27,8 %** | 5,7 % |
| écriture différente (445) | 9,9 % | 8,1 % | 0,7 % | 0,8 % |

**Hors écriture, tout est au hasard** ; dans la même écriture, la famille est enrichie 4,3× et la sœur 4,8×. Permutations d’étiquettes (1 000) : p = 0,001 pour famille et sœur ; requêtes permutées : 11,1 % contre 10,3 % de baseline.

\### 2. LANG_TREE 25 — les sœurs dominent

- **sœurs** : **0,619** (60 paires)
- **même famille, autre branche** : 0,170 (216)
- **familles différentes** : **0,0445** (324)
- **13,89×**, Δ **+0,574** [0,490 ; 0,655]
- régression de décomposition : **sœur +0,448** (p = 0,002), **écriture +0,213**, famille-autre +0,092, R² 0,631
- contraste apparié : **11/11 langues positives**, p = 0,00098 ; leave-one-language-out : sœur **+0,404 → +0,518**
- candidats mélangés : 0,0303 contre 0,0333 de hasard

\### 3. Échantillon 20 — le contraste s’éteint

- sœurs **0,0583** (12 paires), familles différentes **0,0389** (320), famille-autre **0,0757** (48)
- coefficient de sœur **+0,0154**, p = **0,078** (non significatif) ; famille-autre +0,0384, p = 0,016
- **8 des 12 paires de sœurs sont hors écriture** ; les paires qui portent le signal sont `jav–ind` (0,900) et `ind–jav` (0,833), deux non-sœurs.

C’est le résultat de J3.2 confirmé : l’échantillon 20 ne peut pas résoudre les sœurs.

\### 4. Comparaison à J3.1

**J3.1 est reproduit à l’identique** (écart maximal **0** : top-1 0,04944, écriture +0,06186, famille +0,05562, R² 0,13957). Son coefficient de famille (+0,0556) n’était pas faux : c’était un **minorant dilué**, mélange de 12 paires de sœurs et 56 paires de famille-autre. Sur LANG_TREE, le coefficient de sœur est **+0,448**, soit **8×** celui de J3.1.

\### 5. Contrôle d’époque

UDHR **mono-époque** (1948) : placebo de dates **−0,0013** [−0,065 ; +0,041]. Le seul bras daté de J3.1 (Bible) donne **−0,034/siècle** [−0,075 ; +0,009], p = 0,19, contre **+0,609** pour l’écriture. L’époque ne peut pas expliquer l’effet de famille ici.

\## Fichiers

- Fich
… [697 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `tools/retrieval_familles.py` | 0 | 8 |

### Commandes exécutées (échantillon)

- **T1** Inspect workspace root and git state
- **T1** List reports and journal entries
- **T1** Locate J3.1 references and genealogy files
- **T1** Locate UDHR and 532-language references
- **T1** Read J3.1 retrieval-epoch report and JSON
- **T1** Read current state document
- **T1** Inspect UDHR data directory and genealogy schema
- **T1** Read genealogy UDHR tool
- **T1** Find language_genealogy.py and references
- **T1** Inspect UDHR metadata and family counts
- **T1** Read autonomous week plan and Panini inventory relevant sections
- **T1** Locate Panini UDHR source and J3.2 work
- **T1** Inspect Panini 532-language UDHR corpus schema
- **T1** Read J3.2 genealogy two-faces report
- **T1** Inspect full Panini UDHR corpus structure
- **T1** Read J3.2 tool head
- **T1** Search J7.1 references and roadmap
- **T1** Search 532 mentions and J3.2 JSON keys
- **T1** Read common corpus report
- **T1** Inspect common corpus JSON
- **T1** Inspect Panini language entries
- **T1** Count metadata distributions in Panini corpus
- **T1** Check Panini/Drave key alignment and family agreement
- **T1** Join Panini keys to Drave files and Glottolog
- **T1** List Panini languages not in Drave and check Glottolog cache
- **T1** Read J3.1 retrieval tool head
- **T1** Read J3.1 retrieval tool core
- **T1** Read remaining J3.1 tool
- **T1** Extract 29 LANG_TREE languages
- **T1** Inspect J7.1 context in digest
- **T1** Search task file for J7 details
- **T1** Find J7.1 task text in plan
- **T1** Search chantier work dir for J7.1
- **T1** Read chantier state for task descriptions
- **T1** Extract J7 task definition
- **T1** Read J7 plan entry with acceptance
- **T1** Extract full J7 plan entries
- **T1** Inspect Drave languages metadata
- **T1** Check Glottolog coverage of missing Panini codes
- **T1** Locate missing UDHR XML files
- … et 143 autres

## 4. Mesures et résultats marquants

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
- **T1** `Δ moyen **+0,52 point**, IC 95 % **[−2,9 ; +4,3]**. Les effets par cible ne sont pas monotones :`
- **T1** `Δ moyen **+0,52 point**, IC 95 % **[−1,2 ; +1,9]**. Positifs : **LUT +2,6**, **KJV +2,1**,`
- **T1** `**Le 2×2 anglais × français.** Quatre cellules, même paire de langues, dates croisées :`
- **T1** `**R² = 0,763.** Le coefficient de dates n'est **pas significatif** ; le contrôle par **permutation des`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../re`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:60032:GÉNÉALOGIE : `src/nipada/signing/language_genealogy.py` (LANG_TREE, 29 langues, epoch/morphologie/distance normalisée) ; UDHR 53`
- **T1** `(R² 0,30) — la surface capte l'époque ; tout test de style contrôle la date, tout test de famille`
- **T1** `| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |`
- **T1** `33-58 Mo à charger : **à tester avant de s'y engager**.`
- **T1** `**époque +0,1378**, **filiation +0,0489**, tradition +0,0022, R² = 0,3004. H1 (stratification) et H2`
- **T1** `| **UDHR, article 1** | 229 Ko, 532 langues | JSON `udhr-v2.0-xml` : `{name, iso, script, dir, text, family, branch, tradition}` | **532** | `research/data/udhr_corpus.json` (+ `udhr_decomposed_v14.js`
- **T1** `| **UDHR, 30 articles** | 28 Mo | XML `udhr_XXX.xml` + `langues.jsonl`, `genealogie.json`, `familles/*.jsonl` | 456 | `Qtrinet/data/udhr/` | déjà intégré côté Drave |`
- **T1** `| **§334 (philosophie/religion)** | 114 textes actifs ; 102 fichiers `sources/` (9,5 Mo) ; signatures de 44 œuvres | `.txt` un fichier par œuvre + signatures JSON | surtout **anglais** (408 paires), 2`
- **T1** `| **Gutenberg** | 1 999 métadonnées ; **1 943 téléchargés** ; 332 fichiers (271 Mo) ; 5 curatés | SQLite `books(id,title,lang,authors,subjects,downloads,url,fetched)` + `.txt` | en, fr, de, es | `rese`
- **T1** `| **Textes sacrés / suttacentral / MIT Classics** | 21 Mo + 13 Mo + 2 Mo | `.txt` par section | pi, en, gr | `_cache/sacred_texts/`, `_cache/suttacentral/`, `_cache/mit_aristotle_*` | oui |`
- **T1** `| **Protoathéisme (hôte)** | 36 Mo, 42 œuvres | dossiers + `STATUS_PENDING.txt` | en, fr, la… | `Panini/corpus/protoatheism/` | **non : acquisition inachevée** |`
- **T1** `| **Tokens protoathéisme** | 120 Ko | JSONL | — | `Panini/corpus/protoatheism_tokens/` | oui |`
- **T1** `- Le plus « prêt à prouver » : **corpus d'or CIC** (`corpus_dor_cic_v1.json`, 46 Ko + TSV) : 3 defs,`
- **T1** `| Lexiques V14 | `data/v14_lexicon_enriched.json` (3,9 Mo) | `{lang: {ATOME: [mots]}}` | aucune | haute (qualité à vérifier) |`
- **T1** `| API REST | `src/nipada/api/api.py`, `server.py` | FastAPI : `/decompose`, `/reconstruct`, `/roundtrip`, `/compare`, `/atoms`, `/dhatus`, `/benchmark`, `/search`, `/hypotheses`, `/api/v1/*` | fastapi`
- **T1** `2. **Signatures 14 atomes** : **44 œuvres** × 14 flottants (somme 1), en JSON pur. Livrable : table`
- **T1** `cassés, backlog P0 entièrement « À faire ». **Ne pas promettre du 0 % WER.**`
- **T1** `| **famille, brut** | **13/15** (86,7 %) | `kin`, `ibo` : Panini dit « Niger-Congo », Glottolog « Atlantic-Congo » — nomenclature, pas désaccord substantiel |`
- **T1** `| **famille, apparié** | **15/15** (100 %) | en traitant Niger-Congo comme la famille large d'Atlantic-Congo |`
- **T1** `| **branche, nœud exact** | **14/15** (93,3 %) | `mya` : « Tibeto-Burman » n'a pas de nœud exact dans le chemin Glottolog (`tibe1272` absent) ; `burm1265` est le descendant le plus proche |`
- **T1** `| **branche, nœud proche** | **15/15** (100 %) | avec l'allowance ci-dessus |`
- **T1** `(p = 2,8 × 10⁻¹⁴), **Pearson r = 0,918** (p = 3,3 × 10⁻⁴³). Sur les **10 paires** des 5 langues de`
- **T1** ``LANG_TREE`, P1 et P2 donnent des **valeurs identiques** (6 × 0,40, 4 × 0,75). L'accord est donc excellent`
- **T1** `| même famille + même script | **8** | **0,3853** | 0,2004 | **7/8** (87,5 %) | 0,4216 |`
- **T1** `| famille différente + même script | **48** | **0,1691** | 0,1483 | 37/48 (77,1 %) | 0,1827 |`
- **T1** `(77,1 %) pour les paires de familles différentes ; la moyenne au-dessus du hasard est 0,422 contre 0,183.`
- **T1** `| script + P1 | 210 | 0,1821 | +0,0698 | −0,1961 | 1,4 × 10⁻⁴ |`
- **T1** `| script + P2 | 210 | 0,1980 | +0,0652 | −0,1184 | 1,7 × 10⁻⁵ |`
- **T1** `| script + G | 210 | 0,1638 | +0,0651 | −0,1161 | 1,7 × 10⁻³ |`
- **T1** `| script + P1 | 105 | 0,2310 | +0,1137 | −0,1948 | 5,9 × 10⁻³ |`
- **T1** `| **script + P2** | 105 | **0,2564** | +0,1020 | **−0,2120** | **9,2 × 10⁻⁴** |`
- **T1** `| **script + G** | 105 | **0,2297** | +0,1005 | **−0,2259** | **6,5 × 10⁻³** |`
- **T1** `R² 0,256 (P2) contre 0,230 (G), et les intervalles du leave-one-language-out se recouvrent (P2 : R²`
- **T1** `distribution nulle (p = 0,006 ; nul moyen −0,003 ; IC 2,5–97,5 % [−0,147 ; +0,087]).`
- **T1** `| 1 | 6,967 | 49,76 % | 49,76 % |`
- **T1** `| 2 | 2,845 | 20,32 % | 70,08 % |`
- **T1** `| 3 | 1,491 | 10,65 % | **80,73 %** |`
- **T1** `| 4 | 1,260 | 9,00 % | 89,73 % |`
- **T1** `| 5 | 0,528 | 3,77 % | 93,51 % |`
- **T1** `| 6 | 0,381 | 2,72 % | 96,23 % |`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `68:   **préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `181:| **C3.2** | les modules par famille de langues | ✅ | aucune — **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤ 0,5 %** |`
- **T1** `255:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `306:| **R4.4** | **vision/OCR** : scans, figures, layout | 🔬 **mesuré sur scans simulés ; ouvert sur les scans réels** : 5 familles (photo **55,9 → 6,7 %** de WER, test **5,7 %**), **préservation 90–9`
- **T1** `reports/rapport-deepseek.md:132:| dim 320, 7 couches | **16,02 M** | **2,7210** | 2,7742 | +0,0532 | **aligné 3/3** (1,92 %) |`
- **T1** `reports/rapport-n2-multilingue.md:42:| **ja** | 53,8382 | 43,5327 | 5,7423 | −87 % |`
- **T1** `reports/rapport-inventaire-panini.md:367:| **UDHR, article 1** | 229 Ko, 532 langues | JSON `udhr-v2.0-xml` : `{name, iso, script, dir, text, family, branch, tradition}` | **532** | `research/data/udh`
- **T1** `reports/rapport-coordination-r.md:82:| `7a45325f` — la ponctuation a une POS (`PONCT`) | 85,00 → 85,75 % | **+25** |`
- **T1** `> appariables (**95,4 %**). **20 écarts de surface** sont **exclus, pas corrigés**. Les **8 contrôles**`
- **T1** `| fichiers communs | **453** | **99,3 %** de Drave ; **85,2 %** de Panini | l'intersection des identifiants de fichier |`
- **T1** `| article 1 côté Drave | 440 | 96,5 % de Drave | 16 fichiers Drave n'ont pas d'article 1 |`
- **T1** `| appariables article 1 | **438** | 96,7 % de l'intersection | 15 communs sans article 1, 2 Drave hors Panini |`
- **T1** `| **paires exactes** | **418** | **95,4 %** des appariables ; **78,6 %** de Panini | le corpus disponible |`
- **T1** `| écarts de surface | 20 | 4,6 % des appariables | exclus, pas corrigés |`
- **T1** `| Indo-European | 120 | 28,7 % | 5 |`
- **T1** `| Atlantic-Congo | 81 | 19,4 % | 4 |`
- **T1** `| Austronesian | 37 | 8,9 % | 4 |`
- **T1** `| Sino-Tibetan | 17 | 4,1 % | 4 |`
- **T1** `| Turkic | 17 | 4,1 % | 0 (écarté : écritures déjà couvertes) |`
- **T1** `| Afro-Asiatic | 12 | 2,9 % | 4 |`
- **T1** `| 45 autres étiquettes | 134 | 32,1 % | 0 |`
- **T1** `| **total** | **418** | **100 %** | **21** |`
- **T1** `Les cinq familles retenues couvrent **267/418 = 63,9 %** du pool exact ; le turcique (**17**,`
- **T1** `4,1 %) et les **45 autres** étiquettes (**134**, 32,1 %, dont les 10 `(inconnue)`) ne sont pas`
- **T1** `retenues sont **sur-représentées** (19,0 % chacune contre 8,9 % pour l'austronésien, 4,1 % pour le`
- **T1** `sino-tibétain et 2,9 % pour l'afro-asiatique), l'**atlantic-congo** est à parité (19,0 % contre`
- **T1** `19,4 %) et l'**indo-européen** est **sous-représenté** (23,8 % contre 28,7 %). C'est un choix`
- **T1** `**Répartition** : 20 strates (5 × 4) + 1 pivot ; **10 écritures** — latin 11 textes, arabe 2,`
- **T1** `bon (même concept, même article, même verset) est rang 1. Le hasard est 1/k (k candidats).`
- **T1** `"""IC 95 % par bootstrap sur les requêtes (hits ∈ {0,1})."""`
- **T1** `# 2×2 anglais × français`
- **T1** `- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/chantiers.md'); t=p.read_text()\nt=t.replace(\"**bloc lin`
- **T1** `| **B — l'intelligence** | le sens, la logique, les jeux, les maîtres : que sait faire le système ? | ✅ B1–B12 ; B10.3 bloqué (encodeur) ; **B13** state store v0 + DRVF + **bloc linguistique** (POS **`
- **T1** `[still running after 600000ms; moved to background job bash-4822]`
- **T1** `./data/presse/api/IP_26_1934-FR.json:1:{"ky": 212771, "docuLanguageResource": {"ky": 703531, "title": "Selon le nouvel Eurobaromètre, les Européens font plus d'activité physique", "subtitle": "Selon l`
- **T1** `[still running after 60000ms; moved to background job bash-33]`
- **T1** `"sortie_agent": "esure sur les 50 textes libres**\n\n| mesure | valeur |\n|---|---:|\n| annotations / refus | **46 / 4** |\n| surface exacte | **46/46 = 1,0000** |\n| surface avant le correctif `C` | `
- **T1** `[still running after 60000ms; moved to background job bash-40]`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-speculatif-reflexe.md](rapport-speculatif-reflexe.md) | Le réflexe propose, le cerveau vérifie — acceptation 2 à 30 % (le cerveau non entraîné : 0 %) |`
- **T1** `| [rapport-vitesse-v41.md](rapport-vitesse-v41.md) | Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé |`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête `
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 14/11 01 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `**préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `fax **56,7 %**, la limite d'information) ; les **colonnes** tombent de **89,4 %** à **0,5 %**,`
- **T1** `les **tableaux** donnent **92,6 %** de cellules exactes, et **trois vrais scans** s'accordent à`
- **T1** `**7,10 %** et **88,4 %** de mots, l'**ordre des colonnes** prouvé (**15,3 %** contre **98,0 %**`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `| **R0.2** | **[contrôleur de lecture](../theorie/glossaire/entrees/controleur-de-lecture.md)** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, tit`
- **T1** `| **R0.3** | **[banc de lecture rapide](../theorie/glossaire/entrees/banc-de-lecture-rapide.md)** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles`
- … (tronqué)

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : cjy Sino-Tibetan sino1245/sini1245/clas1255/midd1354/nort3155 [stderr] Traceback (most recent call last):   File "<stdin>", line 4, in <module> TypeError: 'NoneType' object is not subscriptable [exit 
- **T1** : (no output) [exit code: 1]

## 6. Commits

- J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE" 2>&1 | tail -30
- J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE" 2
- J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE" 2


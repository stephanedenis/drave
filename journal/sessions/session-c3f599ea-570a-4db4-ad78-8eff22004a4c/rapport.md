# Session session- — Vérificateur indépendant du corpus CIC

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-c3f599ea-570a-4db4-ad78-8eff22004a4c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 05:43 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 107 |
| Appels d'outils | 126 |
| Fichiers touchés | 5 |
| Commandes | 115 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J12.2 : le corpus d'or CIC (42 verdicts, preuve de Bruijn + sha256, portable) — écrire un **vérificateur indépendant** côté Drave qui rejoue les 42 verdicts et compare ; fiche `reports/rapport-cic-verificateur.md` + JSON, 42/42 attendu, contrôle négatif (altérer un octet).

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J12.2 : le corpus d'or CIC (42 verdicts, preuve de Bruijn + sha256, portable) — écrire un **vérificateur indépenda … [159 caractères tronqués]

*126 appels d'outils.* Actions notables :

- bash — Inspect repo root and git state
- bash — Find J12 references in pilotage
- bash — Read roadmap J12 section
- bash — Find CIC references
- bash — List data and reports for CIC
- bash — Find CIC in docs and reports
- bash — Search CIC in work/sprints/tools
- bash — Search de Bruijn and sha256 references
- job_output
- bash — Read semaine-autonome J12 plan
- bash — Inspect submodules and sibling repos
- bash — Find CIC context in reports
- bash — Read CIC inventory sections
- bash — List CIC corpus directory
- … et 109 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_verificateur_cic.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-cic.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/cic/README.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cic-verificateur.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Inspect repo root and git state
- **T1** Find J12 references in pilotage
- **T1** Read roadmap J12 section
- **T1** Find CIC references
- **T1** List data and reports for CIC
- **T1** Find CIC in docs and reports
- **T1** Search CIC in work/sprints/tools
- **T1** Search de Bruijn and sha256 references
- **T1** Read semaine-autonome J12 plan
- **T1** Inspect submodules and sibling repos
- **T1** Find CIC context in reports
- **T1** Read CIC inventory sections
- **T1** List CIC corpus directory
- **T1** Inspect corpus JSON structure
- **T1** Find CIC checker source files
- **T1** Locate CIC python checkers
- **T1** Find scripts using corpus
- **T1** Read CIC checker head
- **T1** Inspect corpus entries
- **T1** Map functions in cic.py
- **T1** Read serialization and env
- **T1** Read Kernel part 1
- **T1** Read Kernel part 2
- **T1** List tools structure
- **T1** Run Panini checker on all verdicts
- **T1** Determine fingerprint formula and tags used
- **T1** Test single-byte mutation strategies
- **T1** Exhaustive single-byte mutations of eq(2,2)
- **T1** Read J12.1 report style
- **T1** Read J11.4 report style
- **T1** Read gate launcher
- **T1** List gate scripts and registry
- **T1** Check tracked data and gitignore
- **T1** Read example gate scripts
- **T1** Check tracked test fixtures
- **T1** Check plan.json for J12.2
- **T1** Read J12.2 plan acceptance
- **T1** Read shift/subst
- **T1** Read substN/apply_multi
- **T1** Hash and provenance of corpus
- … et 75 autres

## 4. Mesures et résultats marquants

- **T1** `bb68b820 J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0089 APRÈS TOPO`
- **T1** `docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 lan`
- **T1** `docs/pilotage/roadmap.md:326:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
- **T1** `docs/pilotage/en-cours.md:93:- **Panini J12.1 — §334** : **655 lignes = 495 paires uniques (160 doublons, 7 auto-paires), 48 textes, 44 signatures** ; H0 **0,909139** / **0,906307** (488) ; date **0,2`
- **T1** `sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur`
- **T1** `contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même`
- **T1** `tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à`
- **T1** `**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction`
- **T1** `d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `**préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `fax **56,7 %**, la limite d'information) ; les **colonnes** tombent de **89,4 %** à **0,5 %**,`
- **T1** `[still running after 60000ms; moved to background job bash-4]`
- **T1** `work/ocr/rpm/tesseract-ocr-traineddata-osd-4.1.0%2Bgit.20240801.8741641-3.1.noarch.rpm`
- **T1** `reports/rapport-corpus-gele.md:4:> des bancs est gelé et vérifié** — 30 documents, 1,4 Mo, manifeste sha256, **0 problème** ;`
- **T1** `(R² 0,30) — la surface capte l'époque ; tout test de style contrôle la date, tout test de famille`
- **T1** `| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |`
- **T1** `reports/rapport-inventaire-panini.md:383:- Le plus « prêt à prouver » : **corpus d'or CIC** (`corpus_dor_cic_v1.json`, 46 Ko + TSV) : 3 defs,`
- **T1** `reports/rapport-inventaire-panini.md:465:croisée (deux checkers indépendants dans leur dépôt : `cic` et `cic_named`). 46 Ko.`
- **T1** `par DTP (0 % WER annoncé) et le stocke dans un graphe encyclopédique flou. Le dépôt porte aussi les`
- **T1** `- Le plus « prêt à prouver » : **corpus d'or CIC** (`corpus_dor_cic_v1.json`, 46 Ko + TSV) : 3 defs,`
- **T1** `| Lexiques V14 | `data/v14_lexicon_enriched.json` (3,9 Mo) | `{lang: {ATOME: [mots]}}` | aucune | haute (qualité à vérifier) |`
- **T1** `| API REST | `src/nipada/api/api.py`, `server.py` | FastAPI : `/decompose`, `/reconstruct`, `/roundtrip`, `/compare`, `/atoms`, `/dhatus`, `/benchmark`, `/search`, `/hypotheses`, `/api/v1/*` | fastapi`
- **T1** `2. **Signatures 14 atomes** : **44 œuvres** × 14 flottants (somme 1), en JSON pur. Livrable : table`
- **T1** `cassés, backlog P0 entièrement « À faire ». **Ne pas promettre du 0 % WER.**`
- **T1** `croisée (deux checkers indépendants dans leur dépôt : `cic` et `cic_named`). 46 Ko.`
- **T1** `> de séparer les deux.** La loi H0 de Panini se reproduit (**R² = 0,909139** sur les **655 lignes** de`
- **T1** `> Sur les **44 signatures** (14 parts flottantes), le retrieval brut donne **61,4 %** de même tradition`
- **T1** `> (hasard 22,4 %) et **56,8 %** de voisins à ≤ 50 ans (hasard 22,8 %) ; les contrôles croisés ramènent`
- **T1** `> la filiation à **50,0 %** (p = 0,0492, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,373). Seule une`
- **T1** `> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0086, **Holm 0,034**).`
- **T1** `> `analytic_sigs_v1.json` (**44 œuvres × 14 atomes**), `sources_coverage.json` / `sources_manifest.json``
- **T1** `**Lecture.** Le porteur est le **rang 2** d'un groupe de **3** ; l'alternative de rang 1 (la REL`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
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
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p`
- **T1** `- **Panini J12.1 — §334** : **655 lignes = 495 paires uniques (160 doublons, 7 auto-paires), 48 textes, 44 signatures** ; H0 **0,909139** / **0,906307** (488) ; date **0,258** seule, **0,0089** après `
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 niveaux |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir 0,2276 |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | **B13** — POS **83,83 %** (R2a/R3/R2b), F1 **0,6181** |`
- **T1** `| **R0.2** | **[contrôleur de lecture](../theorie/glossaire/entrees/controleur-de-lecture.md)** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, tit`
- **T1** `| **R0.3** | **[banc de lecture rapide](../theorie/glossaire/entrees/banc-de-lecture-rapide.md)** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles`
- **T1** `| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 langues*`
- **T1** `| **R1.3** | **tokenisation** : octets ou BPE ; la décision est **mesurée**, pas doctrinale | ✅ **décidée : octets** (R13 close) | à octets égaux, français 2 graines BPE512 **+0,39 %** (bruit), BPE102`
- **T1** `41 - **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **`

## 5. Erreurs rencontrées

7 sorties en erreur ou divergentes. Les premières :

- **T1** : /home/stephane/Data13TB/stephane/GitHub/Qtrinet total 208 drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 . drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 .. -rw-r--r--. 1 stephane stephane  99
- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r
- **T1** : #!/bin/bash # porte-etat.sh — l'état est COURT, STRUCTURÉ, et À JOUR (le fait et sa ligne). # # POURQUOI CETTE PORTE EXISTE. `verifie_en_cours.py` vérifie la forme ; il ne peut pas # savoir qu'un fait
- **T1** : 3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec  nipada/falsification/corpus_dor_cic_v1.json 9aa1a5f4faa1552e0f34732bdde48629dc048a51ce2997395e25367ce1197424  nipada/falsification/cor
- **T1** : ✅ eq(2,2)                  attendu=accepte  obtenu=accepte  empreinte=ok   ✅ eq(4,4)                  attendu=accepte  obtenu=accepte  empreinte=ok   ✅ eq(11,11)                attendu=accepte  obtenu
- **T1** : # 2026-11-14  > **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier > [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé plus bas, dans > le bloc « not
- **T1** : ok [exit code: 1]

## 6. Commits

- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/commit-j122.txt <<'EOF' J12.2 — LE CORPUS D'OR CIC EST REJOUÉ HORS DE PANINI : 42/42 VERDICTS, 


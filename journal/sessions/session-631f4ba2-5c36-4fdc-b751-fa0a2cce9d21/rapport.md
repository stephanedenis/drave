# Session session- — Documenter schéma v2 produit

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 04:58 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 69 |
| Appels d'outils | 99 |
| Fichiers touchés | 6 |
| Commandes | 76 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J11.4 : documenter le schéma v2 dans `docs/produit/README.md` (les champs de `meta.partition`/`meta.alternative`, la rétro-compatibilité v1) et vérifier que `tools/verifier_schema_produit.py` valide les deux versions ; fiche `reports/rapport-schema-v2-doc.md` + JSON, commit.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J11.4 : documenter le schéma v2 dans `docs/produit/README.md` (les champs de `meta.partition`/`meta.alternative`,  … [161 caractères tronqués]

*99 appels d'outils.* Actions notables :

- bash — Inspect repository root and git state
- bash — List product docs and verifier script
- read
- bash — Search references to J11.4 and schema v2
- bash — Read v2 schema part 1
- bash — Read v1 schema
- bash — Read schema tests
- bash — Read plan J11.4 and recent J11.3 report
- bash — Read schema v1 report and JSON sidecar
- bash — Locate J11.4 state and INDEX conventions
- bash — Inspect journal entries for J11 tasks
- bash — Read roadmap and en-cours context
- bash — Run schema verifier on both versions
- bash — Check JSON sidecar naming conventions
- … et 79 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2-doc.md` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_schema_v2_doc.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Inspect repository root and git state
- **T1** List product docs and verifier script
- **T1** Search references to J11.4 and schema v2
- **T1** Read v2 schema part 1
- **T1** Read v1 schema
- **T1** Read schema tests
- **T1** Read plan J11.4 and recent J11.3 report
- **T1** Read schema v1 report and JSON sidecar
- **T1** Locate J11.4 state and INDEX conventions
- **T1** Inspect journal entries for J11 tasks
- **T1** Read roadmap and en-cours context
- **T1** Run schema verifier on both versions
- **T1** Check JSON sidecar naming conventions
- **T1** Check other schema v2 mentions
- **T1** Inspect schema v2 commit history
- **T1** Read filing and gate method docs
- **T1** Inspect today's journal notes
- **T1** Check document size budget
- **T1** Run documentation review baseline
- **T1** Check README budget category
- **T1** Read J11.3 journal note and docs theme
- **T1** Understand doc review checks
- **T1** Inspect pre-commit hook state
- **T1** Read freshness and counter checks
- **T1** Count reports and JSON files
- **T1** Find counters in en-cours
- **T1** Inspect original schema v2 README diff
- **T1** Extract a real meta.partition example
- **T1** Print full partition/alternative schemas
- **T1** Locate partition construction in bloc
- **T1** Find partition helpers
- **T1** Read partition semantics implementation
- **T1** Run verifier with gold 20 and schema tests
- **T1** List gates and read product gate
- **T1** Measure schema validation across both versions
- **T1** Recompute distinct groups count
- **T1** Fix distinct group count and rerun
- **T1** Check references to section 3.3 bis
- **T1** Read en-cours top and B13 paragraphs
- **T1** Read roadmap B13 paragraphs
- … et 36 autres

## 4. Mesures et résultats marquants

- **T1** `> **159,2 ms**, API **2,7 ms**.`
- **T1** `| codes de sortie | **46 × 0**, **4 × 3** |`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`
- **T1** `canonique**, le strict **5/46** ; temps CLI médian **159,2 ms**, API **2,7 ms**. Comparaison`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `**préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `**521/532** étiquetées Glottolog), le top-1 de voisinage est de la même famille **66,1 %** (hasard`
- **T1** `10,3 %) et de la même branche **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout est au hasard**`
- **T1** `(famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %) ; dans la même écriture, la famille monte à`
- **T1** `**69,8 %** et la sœur à **27,8 %**. Le retrieval parallèle 30 articles le chiffre : sur les **25`
- **T1** `autre segment ; couverture **65,84 % des jetons**, **75,19 % des caractères**. La limite est la`
- **T1** `Temps CLI médian **159,2 ms**, API **2,7 ms**. Fiche`
- **T1** `-langue=fr script=Latn source=heuristique · 19 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `+langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../re`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p`
- **T1** `| [rapport-familles-9.md](rapport-familles-9.md) | C3.2c — les 9 familles : 7 sur 9 au-dessus de 30 % |`
- **T1** `| [rapport-s-corpus-reel.md](rapport-s-corpus-reel.md) | S — L'analyseur lit le français propre (65,5 % de GN+GV), pas le CEGEP OCR (8,5 %, plancher du mélange) |`
- **T1** `-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../r`
- **T1** `+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../r`
- **T1** `+**Lecture.** Le porteur `REL [22:42]` est le **rang 2** d'un groupe de **3** segments ; ses deux`
- **T1** `+alternatives sont au rang 1 (la REL longue `[22:54]`, qui le **contient** : `inclus`) et au rang 3`

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : /home/stephane/Data13TB/stephane/GitHub/Qtrinet total 208 drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 . drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 .. -rw-r--r--. 1 stephane stephane  99
- **T1** : ecef7250 J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT 1f61caaa FICHES — DIX FICHES ANNOTÉES « INSTANTANÉ HISTORIQUE » (L'É
- **T1** : total 28 drwxr-xr-x. 1 stephane stephane   90 14 nov 04:52 . drwxr-xr-x. 1 stephane stephane  972 14 nov 00:51 .. -rw-r--r--. 1 stephane stephane 3205 14 nov 04:57 docs.md -rw-r--r--. 1 stephane steph
- **T1** : --- [exit code: 1]
- **T1** : commit 9a259953dff03514c40fe3eb0403a3d3bc95703c Author: Stéphane <stephane@localhost> Date:   Sat Nov 7 14:23:24 2026 -0500      B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 

## 6. Commits

- git commit -F - <<'MSG' J11.4 — SCHÉMA v2 DOCUMENTÉ : 4 CHAMPS PARTITION + 10 CHAMPS ALTERNATIVE, 6 CAS / 0 ÉCHEC, LES DEUX VERSIONS LUES (612 v2 + 612 v1)  La 


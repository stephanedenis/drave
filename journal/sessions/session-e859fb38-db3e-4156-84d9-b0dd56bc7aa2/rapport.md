# Session session- — Plan semaine 2 du projet

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-e859fb38-db3e-4156-84d9-b0dd56bc7aa2` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 07:43 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 44 |
| Appels d'outils | 57 |
| Fichiers touchés | 2 |
| Commandes | 42 |
| Sous-agents | 0 |
| Commits | 2 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche F1 : le plan de la **semaine 2** (16 → 22/11) — lis le bilan de la semaine (`reports/rapport-bilan-semaine.md`), `docs/pilotage/en-cours.md` et les fiches des tâches C/B/D/E, puis écris `docs/pilotage/semaine-2.md` (120 lignes max) : les 5 jours × 2 vagues, les tâches par jour (le gold réel 452 à annoter, la page `/` de S, le corpus à date contrôlée de Panini, la restitution v3, le tagger pa … [146 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche F1 : le plan de la **semaine 2** (16 → 22/11) — lis le bilan de la semaine (`reports/rapport-bilan-semaine.md`), ` … [426 caractères tronqués]

*57 appels d'outils.* Actions notables :

- bash — Inspect repository root and git state
- bash — List pilotage and reports directories
- bash — Locate week report and task sheets
- bash — Check sizes of core files
- read
- bash — Search for task C/B/D/E references
- bash — Search for week 2 references
- bash — List journal and session plan references
- bash — Inspect journal entries for task letters
- bash — List candidate task reports
- bash — Search plan-travail for relevant lines
- bash — Read headers of C/B/D/E reports
- bash — Read conclusions of C2 and C3
- bash — Read conclusions of B1 and D2
- … et 38 autres

**Synthèse produite :**

J’ai écrit [docs/pilotage/semaine-2.md](docs/pilotage/semaine-2.md) — **113 lignes** (limite 120).

Le plan contient :

- **5 jours × 2 vagues** : J1 16/11 → J5 20/11, avec 21–22/11 en réserve.
- **Le gold réel 452** : split 402 / H50, annotation des **10 GP/SUB** (184 → 194 cibles), sans ajouter 50 phrases.
- **La page `/` de S** : décision garder/régénérer, **106 conservés**, **41 en quarantaine**, recette avec les 56 tests.
- **Panini à date contrôlée** : 26 signatures V14, calibration sur 44, rejeu des 60 paires ; si incomplet → `statut incomplet`, aucune p-value.
- **La restitution v3** : qualité des rôles (`agent`, `prédicat`, `lieu`), `_role_gp`, or de rôles plus large.
- **Le tagger par défaut ?** : mesure coût/erreurs, recommandation **défaut hors ligne + `--tagger` opt-in + `auto` si clé**, décision en J5.
- Les **dépendances**, les **risques** et les **livrables** sont tabulés, avec la règle « jamais en attente ».

`semaine-autonome.md` n’a **pas été modifié**. Contrôles passés : revue de documentation, porte-tableaux, `verifie_en_cours`, journal et budget. Commit : `8cb0a926`.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 4 |

### Commandes exécutées (échantillon)

- **T1** Inspect repository root and git state
- **T1** List pilotage and reports directories
- **T1** Locate week report and task sheets
- **T1** Check sizes of core files
- **T1** Search for task C/B/D/E references
- **T1** Search for week 2 references
- **T1** List journal and session plan references
- **T1** Inspect journal entries for task letters
- **T1** List candidate task reports
- **T1** Search plan-travail for relevant lines
- **T1** Read headers of C/B/D/E reports
- **T1** Read conclusions of C2 and C3
- **T1** Read conclusions of B1 and D2
- **T1** Search tagger-default decision context
- **T1** Read roadmap top
- **T1** Inspect chantier plan JSON
- **T1** Search exact task-sheet phrasing
- **T1** List all plan task ids and titles
- **T1** Print F1 task definition
- **T1** Inspect phase 4 plan commit
- **T1** Check history of week 2 plan and plan.json changes
- **T1** Inspect documentation review rules
- **T1** Read rest of documentation review
- **T1** Run documentation review baseline
- **T1** Check current date and last commit date
- **T1** Inspect state and document budget checks
- **T1** Check line count and run documentation review
- **T1** Run doc review and state checks
- **T1** Check context budget and line count
- **T1** Inspect pre-commit hook and working tree
- **T1** Re-run checks after edits
- **T1** Check final line count and review
- **T1** Run table formatting gate
- **T1** See supervisor commit behavior
- **T1** Review state diff before commit
- **T1** Check current time
- **T1** Commit week 2 plan and updated state
- **T1** Check post-commit status and review
- **T1** Verify committed plan and line count
- **T1** Confirm week 1 archive untouched
- … et 2 autres

## 4. Mesures et résultats marquants

- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:9993:    100.0%       4303745            2.98        1.4452       186.1`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:10034:     25.0%       1076785  fusion   2.38 G (0.4521 ms) | 2-listes   5.82 G (0.1850 ms)`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:10898:threads=40      100.0%       4303745  fusion   1.51 G (2.8452 ms) | 2-listes   1.36 G (3.1726 ms)`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:17510:  k-WTA garde  95.0 % :    18.1 M évts/token   perplexité 87122.9916   (4522.42x)`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:18156:⏵ Composition **non additive** : l'attention seule gagne 1,20 %, les deux ensemble seulement 0,24 %. Je vérifie sur B en tâche de `
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:21201:k=50 (densité 5%)  | pull (0 événements, 9.1 s) | auto (4526494712 événements, 6.2 s)`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:25881:généré  : 30 tokens en 5.452 s  (5.50 tok/s)`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:10908:- **T1** `452 tokens notés — perplexité cumulée 3476.367  (4.6 tok/s)  [fenêtre 2 : 226 notés, PPL 3067.009]``
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:4256:     452 tokens notés — perplexité cumulée 3476.367  (4.6 tok/s)  [fenêtre 2 : 226 notés, PPL 3067.009]`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:4372:     452 tokens notés — perplexité cumulée 3476.367  (4.6 tok/s)  [fenêtre 2 : 226 notés, PPL 3067.009]`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:6313:=== perplexité 121.7486 sur 2047 tokens (0 événements, 452.5 s) ===`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:6335:=== perplexité 121.7486 sur 2047 tokens (0 événements, 452.5 s) ===`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:15257:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\np='REPRISE.md'; s=open(p).read()\`
- **T1** `reports/pensee-multicibles.json:1673:  "split": "si (b) est adopté, classer verbe/nom par la cible appariée : 114 cibles verbe / 112 justes (98,25 %), 31 noms / 31 justes (100 %) au lieu de 116/112 et`
- **T1** `39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **166/166** (6 S`
- **T1** `195:   **0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **f`
- **T1** `356:encore** (`kd2-mix512-30k`, les deux GPU à 100 %, fin vers 22 h 40). **S** a repris à 13 h 55 sur`
- **T1** `> IC95 bootstrap par phrase **[+7,23 ; +9,74]**, McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. La règle`
- **T1** `> diversité plafonnée) portent **37,1 %** des erreurs POS et **25,1 %** des segments absents pour`
- **T1** `> **11,1 %** des phrases ; l'heuristique y fait **68,42 %** de POS (étiquettes seules **75,68 %**)`
- **T1** `> contre **91,98 %** sur le reste. L'attachement, lui, est **saturé** : **183/184** (une seule`
- **T1** `d'erreur** : 102/275 erreurs POS (37,1 %), 87/346 segments absents (25,1 %), 1/1 erreur`
- **T1** `d'attachement. (3) Mesure : lot dur **68,42 %** POS, **58,36 %** F1, **21/22** attachement ; reste`
- **T1** `402 **91,98 %**, **81,90 %**, **162/162** ; 50 aléatoires stratifiées **87,24–90,77 %** POS,`
- **T1** `**73,68–83,63 %** F1, **95,0–100 %** attachement. Le lot dur est **hors** des contrôles pour le POS`
- **T1** `| 4 | **Couverture de la banque** | **74/207** phrases complètes (35,7 %), **133** sans verdict, **147/369** candidats, **1 note**, **1 annotateur** | reprendre après la migration (point 1) ; second l`
- **T1** `(91,34 % global, 75,68 % lot) est le chiffre d'étiquetage.`
- **T1** `- **L'attachement.** 184 cibles, **une** erreur : le taux 99,46 % a une barre de confiance énorme`
- **T1** `de la plage (l'attachement stratifié va de 95,0 à 100 % à cause de `g017`).`
- **T1** `doivent plus être **toutes** in-sample. Le split 402/50 donne 91,98 % contre 68,42 % : c'est la`
- **T1** `docs/produit/README.md:556:| **cache, chemin par défaut** | ×5,8 à 20 répétitions, puis **×1,0** à 80 et 160 | S domine le coût |`
- **T1** `docs/produit/README.md:562:réel, le gain est **×1,2** ; sur le chemin par défaut, **×1,0** à 80 et 160 répétitions. Annoncer`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du`
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`
- **T1** `canonique**, le strict **5/46** ; temps CLI médian **159,2 ms**, API **2,7 ms**. Comparaison`
- **T1** `sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur`
- **T1** `contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même`
- **T1** `tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à`
- **T1** `**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction`
- **T1** `d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150`
- **T1** `"mandat": "Tâche F1 : le plan de la **semaine 2** (16 → 22/11) — lis le bilan de la semaine (`reports/rapport-bilan-semaine.md`), `docs/pilotage/en-cours.md` et les fiches des tâches C/B/D/E, puis écr`
- **T1** `+   "mandat": "Tâche B2 : les 14 atomes comme prédicteurs des 8 niveaux Drave — sur les 44 œuvres × 14 flottants (JSON plat, lecture seule chez Panini), mesure la prédiction d'un niveau (POS, syntagme`
- **T1** `+   "mandat": "Tâche F1 : le plan de la **semaine 2** (16 → 22/11) — lis le bilan de la semaine (`reports/rapport-bilan-semaine.md`), `docs/pilotage/en-cours.md` et les fiches des tâches C/B/D/E, puis`
- **T1** `[still running after 60000ms; moved to background job bash-37]`

## 6. Commits

- grep -n -E "git commit|commit|git add|acceptation|accep" tools/chantier/superviseur.py | head -60
- PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE CONTRÔLÉE, RESTITUTION V3, TAGGER PAR DÉFAUT ?" 2>&1 | tail -40; echo "COMMIT_EXIT=${PIP


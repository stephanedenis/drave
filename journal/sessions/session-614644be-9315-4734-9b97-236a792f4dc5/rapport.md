# Session session- — Schéma annotation v2 et validation

> **Journaux :** [le jour](../../2026-11-07/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-614644be-9315-4734-9b97-236a792f4dc5` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-07 14:11 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 146 |
| Appels d'outils | 171 |
| Fichiers touchés | 12 |
| Commandes | 95 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J1.3 : le schéma v2 de l'annotation — publier `tools/schemas/drave-annotation-v2.json` (ajout de `meta.alternative` et `meta.partition`), version 2, valider avec `tools/verifier_schema_produit.py --gold 20`, mettre à jour la doc produit, commit. Rétro-compatible : version 1 reste lue.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J1.3 : le schéma v2 de l'annotation — publier `tools/schemas/drave-annotation-v2.json` (ajout de `meta.alternative … [171 caractères tronqués]

*171 appels d'outils.* Actions notables :

- bash — Inspect repo root and git state
- bash — List schemas and tools
- read
- bash — Locate schema verifier and references
- job_kill
- bash — Find product docs and schema docs
- bash — Targeted grep for annotation schema references
- bash — List product docs and tests
- bash — Find meta alternative/partition in bloc_linguistique
- bash — Search product docs for schema/meta mentions
- bash — Find J1.3 task references
- bash — Inspect chantier plan for J1 tasks
- bash — Print J1.3 task object
- bash — Read first part of product README
- … et 139 autres

**Synthèse produite :**

**J1.3 terminée et committée** (`9a259953`).

\### Livré
- **`tools/schemas/drave-annotation-v2.json`** : schéma Draft 2020-12, `version: 2`, avec `meta.partition` (`groupe`, `rang`, `membres`, `vue`) et `meta.alternative` (type, span, source, union, relation, rang, `retire`, rôle, attachement).
- **`tools/bloc_linguistique.py`** : `VERSION_ANNOTATION = 2` ; le JSON produit porte désormais `version: 2`.
- **`tools/verifier_schema_produit.py`** : choix du schéma d’après `version` ; **v1 reste lue** avec le schéma v1. Contrôle négatif intégré : le schéma v2 refuse bien une annotation v1.
- **Tests / porte** : `test_schema_produit.py` passé à 8 tests (v2 + rétro-compatibilité), labels de `porte-produit.sh` mis à jour.
- **Doc produit** : `docs/produit/README.md`, `docs/produit/exemples.md` (schéma v2, `meta.partition`/`meta.alternative`, refus code 3, options réelles).
- **Fiche** : `reports/rapport-schema-v2.md` + `reports/pensee-schema-v2.json`.
- **État / roadmap** : `en-cours`, `roadmap`, `semaine-autonome`, index des reports mis à jour.

\### Validation
```text
python3 tools/verifier_schema_produit.py --gold 20
→ 26 cas, 0 échec
→ 5 cas v2 + 1 cas v1 + 20 phrases du gold
→ ✅ v1 lue par le schéma v1
→ ✅ contrôle négatif : v2 refuse v1
```

Contrôles complémentaires : `porte-produit` **verte** (16 tests produit, 8 tests schéma, 4 tests libres, autotest **183/183**), revue doc ✅, journal ✅, budget ✅, état ✅. Les modifications préexistantes hors périmètre (`reports/pensee-*`, `tools/chantier/superviseur.py`, `tools/structures`, etc.) sont restées non committées.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v2.json` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_schema_produit.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 25 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-schema-v2.json` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Inspect repo root and git state
- **T1** List schemas and tools
- **T1** Locate schema verifier and references
- **T1** Find product docs and schema docs
- **T1** Targeted grep for annotation schema references
- **T1** List product docs and tests
- **T1** Find meta alternative/partition in bloc_linguistique
- **T1** Search product docs for schema/meta mentions
- **T1** Find J1.3 task references
- **T1** Inspect chantier plan for J1 tasks
- **T1** Print J1.3 task object
- **T1** Read first part of product README
- **T1** Read rest of product README
- **T1** Find version and JSON loading functions
- **T1** Find version references in CLI/tests
- **T1** Read product test/version and gate
- **T1** See example docs on meta fields
- **T1** Inspect branch and dirty files
- **T1** Run current schema verifier
- **T1** Find all schema v1 references
- **T1** Read partition reports for schema rationale
- **T1** Find meta field descriptions
- **T1** Read schema sketch for meta fields
- **T1** Find partition tests
- **T1** Find other references to schema
- **T1** Read partition tests
- **T1** Inspect generated meta keys and types
- **T1** Enumerate all syntagme types and relations on gold
- **T1** Find hash/version expectations in tests
- **T1** Find code reading annotation version
- **T1** Inspect CLI for schema/version
- **T1** Read exemples ending
- **T1** Find v1 mentions in main module
- **T1** Validate v2 schema on gold and modes
- **T1** Run new schema verifier
- **T1** Locate v1 labels in gate
- **T1** Update gate labels to v2
- **T1** Run schema product tests
- **T1** Run product smoke tests
- **T1** Rename test class for v2
- … et 55 autres

## 4. Mesures et résultats marquants

- **T1** `[still running after 60000ms; moved to background job bash-3]`
- **T1** `124:  vue linéaire (partition filtrer) F1 81.04 %  · attachement 93.31 % de couverture`
- **T1** `docs/pilotage/en-cours.md:126:**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035` et convention des GV faits**, reste `g017` (J1.`
- **T1** `| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |`
- **T1** `1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat`
- **T1** `aléatoire** dans les listes donne **42,14 %** de top-1 — et la **permutation des cibles**`
- **T1** `**1,997/220 = 0,908 %** ; les deux donnent p = 0. Un chiffre sans sa contre-épreuve n'est pas un`
- **T1** `langue=fr script=Latn source=heuristique · 19 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)`
- **T1** `SYNTAGMES   F1 75.33 %  (P 72.39 % / R 78.53 %)`
- **T1** `tête      F1 86.40 %  (P 85.19 % / R 87.65 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.04 %  · attachement 93.31 % de couverture`
- **T1** `ATTACHEMENT exact 98.74 % · couverture 99.16 % · exact sur span 99.58 % · top-k 98.33 %`
- **T1** `tête      couverture 100.00 % · top-k 99.16 %`
- **T1** `PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %`
- **T1** `FRACTION SÉMANTIQUE 54.76 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)`
- **T1** `**Lecture.** `exact 98.33 %` est le **rendement** (235/239 cibles) ; `exact sur span 99.58 %` est`
- **T1** `le gold gelé 602 (F1 65,11 %, POS 85,32 %). La commande sort **0** : elle ne teste pas la cascade`
- **T1** `| **cache du chunker** | **×138,7** à 160 répétitions (9 817,7 → 70,8 ms) | banc de texte **répété**, chemin chunker |`
- **T1** `| **cache, chemin par défaut** | ×5,8 à 20 répétitions, puis **×1,0** à 80 et 160 | S domine le coût |`
- **T1** `| **cache, corpus réel** | **×1,2** | phrases réelles, 6,1 tokens/phrase |`
- **T1** `**Ce que le ×139 veut dire — et ne veut pas dire.** C'est la suppression du **O(n²)** du chunker`
- **T1** `réel, le gain est **×1,2** ; sur le chemin par défaut, **×1,0** à 80 et 160 répétitions. Annoncer`
- **T1** `« ×139 plus rapide » sans la condition serait faux. Ce que le cache garantit, c'est que les`
- **T1** `SYNTAGMES   F1 58.93 %  (P 63.19 % / R 55.22 %)`
- **T1** `tête      F1 73.92 %  (P 81.36 % / R 67.72 %)`
- **T1** `| **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |`
- **T1** `> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,`
- **T1** `> **toutes** des paires S × chunker (53,1 % de S qui contient le chunker, 33,5 % l'inverse,`
- **T1** `> 2,5 % de mêmes bornes, 10,9 % de croisements). Le mode **`alternative`** (défaut) garde les deux`
- **T1** `> exact 235/236, POS 85,00 %** — les mesures de la base, **sans déduplication silencieuse**. Le mode`
- **T1** `| **`alternative`** (défaut) | 239 | **0,6482** | **235/236** | +10,4 % |`
- **T1** `| `filtrer_union` | 91 | 0,6163 | 217/239 → 217/218 | +7,2 % |`
- **T1** `| `filtrer` (partition stricte) | **0** | **0,6954** | 217/218 | +2,0 % |`
- **T1** `"retire": <bool>}`. Le rang 1 reste le **chunker le plus large** (179/207 groupes avec un span du`
- **T1** `gold, 86,5 %).`
- **T1** `- **Le coût JSON** (+10,4 %) n'est pas mesuré côté client.`
- **T1** `- **le rang 1** est une heuristique (le chunker le plus large).`
- **T1** `- **le rang 1 est la vue préférée, pas la partition** : en B2, tous les union sont conservés et`
- **T1** `Exemple A (porteur `GP 29-60`, groupe de 4, rang 1, trois alternatives) :`
- **T1** `- **Le rang 1** est une préférence de groupe (179/207 avec gold), pas une vérité sémantique ; le`
- **T1** `large) ; le gold le dit minoritaire (12,1 % des groupes), pas impossible.`
- **T1** `docs/pilotage/plan-travail.md:449:| 1 (P0) | frontières, partition, POS R4 | 32/40 → 0 frontières fausses ; `meta.alternative` ; **POS 85,00 %** |`
- **T1** `reports/rapport-partition-syntagmes.md:289:   **+2,0 %** de JSON. Les S retirés restent dans `meta.alternative` (`retire: true`) : la vue est`
- **T1** `comme « 100 % du langage » : c'est 100 % des spans prédits, sur **92,89 %** des cibles.`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV +`
- **T1** `- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (`
- **T1** `| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **1 024 octets entraînés** ; **2 048** fini (2×10 000 pas) ; la restitution |`
- **T1** `**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035` et convention des GV faits**, reste `g017` (J1.3/J1.4) ; **S** — poursuivre l`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `docs/pilotage/roadmap.md:38:**État au 07/11 13 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r0`
- **T1** `docs/pilotage/roadmap.md:178:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `docs/pilotage/roadmap.md:253:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
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
- **T1** `| **total** | **179** | 100 % | **170** | **174** | **168** | |`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.14 %)`
- **T1** `SYNTAGMES   F1 78.82 %  (P 78.18 % / R 79.46 %)`
- **T1** `tête      F1 90.25 %  (P 92.34 % / R 88.26 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.27 %  · attachement 92.05 % de couverture`
- **T1** `ATTACHEMENT exact 97.49 % · couverture 97.91 % · exact sur span 99.57 % · top-k 97.07 %`
- **T1** `tête      couverture 100.00 % · top-k 99.15 %`
- **T1** `PRAGMATIQUE acte 99.67 % · négation 97.67 % · modalité 98.84 % · double sens 94.35 %`
- **T1** `FRACTION SÉMANTIQUE 54.96 %`
- **T1** `SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)`
- **T1** `tête      F1 90.29 %  (P 92.61 % / R 88.08 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture`
- **T1** `ATTACHEMENT exact 99.16 % · couverture 99.58 % · exact sur span 99.58 % · top-k 98.74 %`
- **T1** `docs/pilotage/en-cours.md:66:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV`
- **T1** `-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV `
- **T1** `+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV `
- **T1** `-**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035` et convention des GV faits**, reste `g017` (J1.3/J1.4) ; **S** — poursuivre `
- **T1** `+**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035`, convention des GV et schéma v2 faits**, reste **J1.4 restitution** puis `g0`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `-**État au 07/11 13 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé`
- **T1** `+**État au 07/11 14 h 20.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé`
- **T1** `-langue=fr script=Latn source=heuristique · 19 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `+langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : ✅ fr   ✅ en   ✅ vide   ✅ ponctuation   ✅ long   ✅ gold:g001   ✅ gold:g002   ✅ gold:g003   ✅ gold:g004   ✅ gold:g005   ✅ gold:g006   ✅ gold:g007   ✅ gold:g008   ✅ gold:g009   ✅ gold:g010   ✅ gold:g011 
- **T1** : ✅ index : aucun fait stagé sans état [s/v7 9a259953] B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE  30 files changed, 3978 insertions(+), 134 deletions
- **T1** : 9a259953 B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE  docs/pilotage/en-cours.md                          |   19 +-  docs/pilotage/roadmap.md         

## 6. Commits

- B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE" 2>&1 | tail -40; echo "exit=${PIPESTATUS[0]}"


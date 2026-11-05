# Session ff7e786c — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `ff7e786c-3ece-4eae-864e-19dddfead93c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 13:11 |
| Durée | 1.5 h |
| Tours | 1 |
| Messages | 165 |
| Appels d'outils | 194 |
| Fichiers touchés | 2 |
| Commandes | 114 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **vérifier la cohérence** des fiches B13 du 2026-11-05 avec leurs JSON et avec les valeurs attendues par les portes.  À faire : 1. Dans `reports/`, prends les fiches `rapport-pensee-*.md` datées du 05/11 : verbe-gv, lexique-verbal, spans, denominateur, classement, conventions, attachement- … [1601 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **vérifier … [1881 caractères tronqués]

*194 appels d'outils.* Actions notables :

- bash — Check branch and list reports
- glob
- bash — Inspect headers of named fiches
- bash — Find fiches mentioning 2026-11-05
- bash — Line counts for fiches, JSON, autotest
- bash — Locate gate references in autotest
- bash — Find gate function definitions
- bash — Read gate registration block
- read
- bash — Dump first six JSONs
- bash — Dump last five JSONs
- bash — Read gates T153-T169 bodies
- bash — Read gates T172-T174 bodies
- bash — Locate metrics in evaluer_gold.py
- … et 163 autres

**Synthèse produite :**

⏵ Livraison du résumé final à l'utilisateur

Les deux fichiers sont écrits et validés (JSON valide, `porte-tableaux.sh` vert, 3 225 liens résolus) :

- `reports/rapport-coherence-fiches.md`
- `reports/pensee-coherence-fiches.json`

\## Bilan

- **11 fiches vérifiées** (les 11 `rapport-pensee-*.md` B13 datées du 2026-11-05, avec leurs 11 JSON).
- **8 fiches cohérentes** avec leur JSON et leur porte d'époque : 5 purement historiques (verbe-gv, lexique-verbal, classement, conventions, attachement-cible) et 3 qui étaient l'état pré-v2 (echecs-cible, topk-strict, convention-doc).
- **3 fiches présentaient une divergence réelle au blob d'origine, soit 7 écarts** :
  - `lexique-elargi` : 62 au lieu de 63 ; 83/0,7590 au lieu de 82/0,7683 ; 23 au lieu de 22 ; 145 (avant) au lieu de 146 — 4 écarts.
  - `spans` : titre « 94 spans » avec une ventilation 48+33+12=93 ; table des catégories 65/25/3/1=94 sous un total de 93 (l'après-correctif est 65/24/3/1) ; 65+25=90 attribués aux subordonnées alors qu'il n'y a que 81 REL/SUB — 2 écarts.
  - `denominateur` : « 93 chez S (REL/SUB) » alors que 93 = 81 REL/SUB + 12 GP — 1 écart.
- **7 paliers historiques reconnus** (verbe-gv 08:58 → attachement-cible 10:18), plus les colonnes « avant » de `lexique-elargi`. Les portes T153/T161/T162/T163/T166/T167/T168/T169 ont été réécrites à chaque commit : les écarts des fiches antérieures avec les valeurs d'aujourd'hui sont **historiques, pas des erreurs**.

\## Corrections et résidus

Je n'ai corrigé aucune fiche. Le parent a corrigé les 3 fiches dans `9d5337ce` (v2, spans) et `2e08cbc7` (lexique-elargi, denominateur), mais les corrections sont partielles ; **3 résidus subsistent** :

1. `spans` : le chapô dit encore **12 GP** (titre/table : 13) et la narrative **25** (table : 24), avec 65+25 attribués aux 81 REL/SUB.
2. `denominateur` : le corps dit **94** cibles sans segment, alors que le tableau/JSON gardent **146 labels** et une couverture de **0,6109** (239−146 = 93) ; l'attribution « (REL/SUB de S) » reste fausse (94 = 81 REL/SUB + 13 GP). La correction 93→94 a introduit cette incohérence.
3. `lexique-elargi` : le chapô et le titre de §1 disent encore « Sur les **145** segments » (l'avant est 146 ; le tableau, lui, dit « avant (146) ») ; le « +4 » reste ambigu.

\## Contexte v2

Le commit `9d5337ce` a intégré la **v2** (180/180) : convention SUB au POS gold, split **116/29**, exact **137/145**, top-k strict **0,9724**. Les 11 fiches sont **pré-v2** ; je n'ai pas exécuté les 180 porte
… [349 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-fiches.md` | 1 | 40 |
| `/tmp/gen_coherence_json.py` | 0 | 20 |

### Commandes exécutées (échantillon)

- **T1** Check branch and list reports
- **T1** Inspect headers of named fiches
- **T1** Find fiches mentioning 2026-11-05
- **T1** Line counts for fiches, JSON, autotest
- **T1** Locate gate references in autotest
- **T1** Find gate function definitions
- **T1** Read gate registration block
- **T1** Dump first six JSONs
- **T1** Dump last five JSONs
- **T1** Read gates T153-T169 bodies
- **T1** Read gates T172-T174 bodies
- **T1** Locate metrics in evaluer_gold.py
- **T1** Check file size and commit history
- **T1** Run selected gates and print actual values
- **T1** Count and list B13 fiches dated 2026-11-05
- **T1** Find generation references and JSON history
- **T1** Log around spans fiche
- **T1** Count gate entries
- **T1** Count gates precisely via AST
- **T1** Extract each gate at its fiche commit
- **T1** Find span category logic
- **T1** Compare GP bounding code at spans commit vs current
- **T1** Compare claimed gate counts to actual at each commit
- **T1** Trace gate assertions across commits
- **T1** Print T161-T163 bodies at key commits
- **T1** Read reports README B13 index
- **T1** Check headers/dates of adjacent B13 fiches
- **T1** Extract assertions at intermediate commits
- **T1** Extract T163 expected span/cible per commit
- **T1** Find duplicated figures elsewhere
- **T1** Check docs for lexique-elargi figures
- **T1** Get commit timestamps
- **T1** Inspect session log for lexique-elargi edits
- **T1** Extract T153/T167-T169/T172/T173 per commit
- **T1** Check T166 GP expected at key commits
- **T1** Check date, output files, clean status
- **T1** Dump current attachement metrics
- **T1** Find tete values in session log
- **T1** Verify gold size and target count
- **T1** Run full autotest suite
- … et 74 autres

## 4. Mesures et résultats marquants

- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-pensee-cible-proximite.md`](rapport-pensee-cible-proximite.md) | **B13** — la cible par proximité : exact 0,0042 → **0,0544** (×13), top1 0,3975, **164/164** |`
- **T1** `| [`rapport-s-corpus-reel.md`](rapport-s-corpus-reel.md) | **S** — le corpus réel : GN+GV 8,5 % CEGEP (mélange 9,1 %), 65,5 % propre (9,1 %) ; plancher du mélange ; banque 200 phrases / 355 candidats `
- **T1** `# B13 — la cible par proximité : l'exact passe de 0,0042 à 0,0544 (×13)`
- **T1** `| conventions | « 0,6438 = 51 × 0,73 + 95 × 0,60 » | 0,6438 | — | exact avec 0,7255 ; 0,6454 avec 0,73 | ⚠️ arrondi non bloquant (cf. § 5.3) |`
- **T1** `- **`conventions` « 0,6438 = 51 × 0,73 + 95 × 0,60 »** : avec 0,73 (arrondi), on obtient 0,6454 ;`
- **T1** `l'égalité n'est exacte qu'avec 0,7255 (37/51) : (51 × 0,7255 + 95 × 0,60) / 146 = 0,6438.`
- **T1** `- **La mesure globale cachait l'écart** : 0,6438 = moyenne pondérée (51 × 0,73 + 95 × 0,60).`
- **T1** `(rang 0, ordre gauche→droite→dedans) donne **139/145** (+2). Conclusion : **ne pas intégrer**`
- **T1** `{"fiche": "conventions", "champ": "« 0,6438 = 51 × 0,73 + 95 × 0,60 »", "explication": "0,6454 avec 0,73 ; l'égalité exacte utilise 0,7255."},`
- **T1** `- **Sur les segments qu'on sait segmenter, l'attachement tient** : top-k **90,4 %**, top1`
- **T1** `**78,8 %**, exact **22,6 %** — la bonne cible est presque toujours proposée.`
- **T1** `- **L'exact reste faible** (22,6 %) : le classement des candidats n'est pas appris, la règle de`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : 172 [exit code: 1]


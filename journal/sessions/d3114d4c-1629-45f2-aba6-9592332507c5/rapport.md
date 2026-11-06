# Session d3114d4c — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `d3114d4c-1629-45f2-aba6-9592332507c5` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 21:12 |
| Durée | 1.7 h |
| Tours | 1 |
| Messages | 102 |
| Appels d'outils | 124 |
| Fichiers touchés | 1 |
| Commandes | 102 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : vérifier la **cohérence des huit fiches de la journée** (v2 → v8) avec leurs JSON et avec l'état committé `f908d7b0`.  Fiches (chacune avec son JSON) : - `rapport-pensee-attachement-v2.md`, `-v3.md`, `-segmentation-v4.md`, `-couverture-v5.md`, `-attachement-parfait.md` (v6), `-couverture-v … [1566 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : vérifier l … [1846 caractères tronqués]

*124 appels d'outils.* Actions notables :

- bash — Check git status, branch, and commits
- bash — List reports directory
- bash — Locate the eight reports
- bash — List pensee-related files in reports
- read
- bash — Print all eight JSON files
- bash — Check claimed snapshot commits and ancestry
- bash — List coherence reports and README size
- bash — Diff stat since v7 commit
- bash — History of fiches and README
- bash — Read evaluer_gold.py head
- bash — Find functions and constants in evaluer_gold
- bash — Read evaluer_bloc tail and main
- bash — Evaluate current code on 612 and 602 gold
- … et 99 autres

**Synthèse produite :**

⏵ Livraison du bilan de cohérence des huit fiches

Les deux fichiers neufs sont écrits et validés :
- `reports/rapport-coherence-fiches-v8.md`
- `reports/pensee-coherence-fiches-v8.json`

**Aucun fichier existant modifié, aucun commit.** L'audit est ancré sur `f908d7b0` (les fichiers d'or sont identiques de `9d5337ce` à `f908d7b0` ; mesures rejouées avec le `bloc_linguistique.py` historique sur 612 et 602).

\## Nombre de fiches et écarts

**8 fiches** (1 courante : v8 ; 7 historiques : v2→v7), **42 écarts** : **7 critiques**, **23 majeurs**, **12 mineurs**.

| fiche | écarts | dont critiques |
|---|---:|---:|
| v2 `9d5337ce` | 4 | 0 |
| v3 `dcf7bc91` | 3 | 0 |
| v4 `392f03aa` | 4 | 1 |
| v5 `b975011b` | 5 | 1 |
| v6 `0ec6c27d` | 3 | 0 |
| gold-split `85e4082b` | 4 | 0 |
| v7 `69bd865e` | 7 | 3 |
| v8 `f908d7b0` | 8 | 2 |
| systémique | 4 | 0 |

\## Corrections prioritaires

**P1 — chiffres de tête et statut**
1. **v8** : le tableau des règles annonce `+15 dev, +5 test, 0 perte, +3, +2, +2` (somme **+27**) ; la mesure réelle v7→v8 est **+23 labels gagnés / −7 perdus = +16 labels, +17 exacts** (24 gains/7 pertes ; test net **+2**, pas +5). Les 7 pertes : `s032, s037, s069, s072, s115, s135, r273`.
2. **v8** : « 17 inatteignables » a le bon compte mais la mauvaise composition. Les 27 = **17 inatteignables** (6 REL + 3 SUB + 4 GP + `r255` + `r035` + `r264` + `r288`) **+ 7 régressions + 3 gains A17 non intégrés** (`g017`, `r280`, `r153`). Le texte compte 20 cas, omet 3 SUB synthétiques et classe 6 régressions dans les « 12 synthétiques ».
3. **v8** : à `f908d7b0`, pas de date, pas de commit exact, pas de contrôle négatif ; le lien `rapport-spans-v7.md` est cassé (fichier non committé).
4. **v4** : F1/tête compare la v3 **612** (`0,2862/0,4989`) à la v4 **602** (`0,4539/0,6432`) ; base non nommée, § 3 dit 612.
5. **v5** : `dev 126/126 (0,9921)` doit être **1,0000** ; F1 `0,5156`/tête `0,6826` sont les constantes de porte, pas la mesure 602 (`0,5164/0,6834`).
6. **v7** : se dit « État courant `69bd865e` » (faux) ; en-tête/JSON POS `0,7475` contre table `0,7482` ; JSON `avant` mélange v6 612 (`0,5130`), v5 (tête `0,6826`) et v4 (POS `0,7475`) ; « qui 12 » au lieu de 6 ; § 3/§ 5 contredisent § 2 sur dev/test.
7. **v2** : split lexical pré-v2 `60/63` et `63/82` étiqueté « POS gold » ; `46` vs `45` ; colonne « gain » incomplète (`88+45=133` vs 141).

**P2 — contrôles négatifs**
8. **v4, v5, v6** : remplacer le contrôle copié de la v7 (`1,67/196` vs `195/196`) par un c
… [1740 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-fiches-v8.md` | 1 | 7 |

### Commandes exécutées (échantillon)

- **T1** Check git status, branch, and commits
- **T1** List reports directory
- **T1** Locate the eight reports
- **T1** List pensee-related files in reports
- **T1** Print all eight JSON files
- **T1** Check claimed snapshot commits and ancestry
- **T1** List coherence reports and README size
- **T1** Diff stat since v7 commit
- **T1** History of fiches and README
- **T1** Read evaluer_gold.py head
- **T1** Find functions and constants in evaluer_gold
- **T1** Read evaluer_bloc tail and main
- **T1** Evaluate current code on 612 and 602 gold
- **T1** Show diffs of fiches since v7
- **T1** Inspect bloc_linguistique imports
- **T1** Check historical module imports and diff
- **T1** Check RACINE use and Heuristique init
- **T1** Measure historical POS exact values
- **T1** Measure POS at v6, v7, HEAD
- **T1** Search for POS delta values in audit
- **T1** Search repo for POS values
- **T1** List classes in bloc_linguistique
- **T1** Measure S and chunker F1 on 602
- **T1** Find how S/chunker F1 are measured
- **T1** Find segmentation methods
- **T1** Read S and union segmentation code
- **T1** Search for S/chunker values v8
- **T1** Find audit v7 measurement of S/chunker
- **T1** List unpredicted gold spans by type
- **T1** List unpredicted target spans
- **T1** Search audit v7 for span classification
- **T1** Find inevitables mentions
- **T1** Classify missing spans by lexicon
- **T1** Search for v8 rule gains
- **T1** Inspect v8 rule implementation
- **T1** Search dev/test v7 for v8 rule gains
- **T1** Read v8 clause boundary code
- **T1** Find A17 references
- **T1** Search all reports for v8 fr/en counts
- **T1** Check spans-v7 report and v8 commit files
- … et 62 autres

## 4. Mesures et résultats marquants

- **T1** `b1b1292f B13 — LE CACHE COMPLET : UN SEUL CHUNKING DANS LES DEUX CHEMINS (T178), VALIDÉ PAR A11 (×11,0, ÉGALITÉ 612/612) ; 181/181`
- **T1** `e0592c59 B13 — LE CACHE DU CHUNKER APPLIQUÉ : ×139 À 160 RÉPÉTITIONS, SORTIE IDENTIQUE (0/612) ; ×1 EN DÉFAUT, S DOMINE ; 181/181`
- **T1** `| [`rapport-native-distillation-tetes.md`](rapport-native-distillation-tetes.md) | **N2.4** — têtes dans la distillation : PPL **3,295**, pas de gain ; tête 3 **62,98 %** > principale **62,35 %** |`
- **T1** `reports/rapport-pensee-phase-devine.md:4:> **83/83 portes** : l'agent reçoit un **signal bruité à 90 %** sur le but. La`
- **T1** `32	| [`rapport-cache-chunker.md`](rapport-cache-chunker.md) | **B13** — la validation A11 du cache : ×11,0 à 160 tokens, égalité 612/612, cache falsifié détecté |`
- **T1** `35	| [`rapport-cache-chunker-applique.md`](rapport-cache-chunker-applique.md) | **B13** — le cache appliqué : **×139** en chunker, ×1 en défaut (S domine), sortie identique, **181/181** |`
- **T1** `37	| [`rapport-cout-chunker.md`](rapport-cout-chunker.md) | **B13** — le coût du chunker : O(n²) confirmé, cache ×11,6 à 160 tokens |`
- **T1** `+> donnerait **143/145 (98,62 %)** et 143/239 (59,83 %), avec « +2 cas, dont 2 synthétiques »`
- **T1** `**Permutation globale des cibles** (2000 tirages) : **2,04/212** en moyenne (0,96 %) contre`
- **T1** `**212/212** observé, p = 0. **Candidat aléatoire** : 35,9 % de top-1 (observé 100 %).`
- **T1** `**Permutation des listes de candidats** : top-k 0,85 % (observé 83,5 %).`
- **T1** `| [`rapport-native-capacite-egal.md`](rapport-native-capacite-egal.md) | **N2.5b** — capacité à budget égal : 21,63 M **4,294** vs 11,47 M **4,476** (−4,1 %) |`
- **T1** `-| [`rapport-native-distillation-tetes.md`](rapport-native-distillation-tetes.md) | **N2.4** — têtes dans la distillation : PPL **3,295**, pas de gain ; tête 3 **62,98 %** > principale **62,35 %** |`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 26, in <module>   File "<stdin>", line 10, in load_hist   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistiq
- **T1** : [stderr]   File "<stdin>", line 24     print('lexical split v2: verb',v_ok,'/',v_n, v_ok/v_n; 'nom',n_ok,'/',n_n,n_ok/n_n)                                                          ^ SyntaxError: inval
- **T1** : rows 42 {'majeure': 23, 'mineure': 12, 'critique': 7} [stderr] Traceback (most recent call last):   File "<stdin>", line 261, in <module> AssertionError [exit code: 1]


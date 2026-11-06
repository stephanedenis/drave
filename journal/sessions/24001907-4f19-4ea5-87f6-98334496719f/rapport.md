# Session 24001907 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `24001907-4f19-4ea5-87f6-98334496719f` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 19:25 |
| Durée | 1.4 h |
| Tours | 1 |
| Messages | 106 |
| Appels d'outils | 141 |
| Fichiers touchés | 1 |
| Commandes | 97 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer l'état v7 de l'attachement** (commit `69bd865e`) et vérifier que ses chiffres et ses portes sont justes.  Contexte : `tools/bloc_linguistique.py` (classe `Heuristique`, `_syntagmes_simple`, `_cible_precedent`, `_cible_hors_span`), `tools/tests/linguistique/evaluer_gold.py` (`char … [2193 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2473 caractères tronqués]

*141 appels d'outils.* Actions notables :

- bash — Inspect git HEAD and status
- bash — List reports and relevant tool dirs
- read
- bash — Count lines of key files
- bash — Run gold evaluator and save JSON
- bash — Inspect gold sizes and dev/test split
- bash — Extract measured metrics per source
- bash — Compare living gold vs frozen gold
- bash — Locate cited gate definitions
- bash — Inspect autotest structure and gates count
- bash — Find gate function definitions
- bash — Run autotest gates
- bash — Read bloc_linguistique header and classes
- job_output
- … et 104 autres

**Synthèse produite :**

⏵ Clôture de l'audit et récapitulatif des livrables

Audit terminé. Les deux fichiers demandés sont écrits :

- [`reports/rapport-audit-v7.md`](reports/rapport-audit-v7.md)
- [`reports/pensee-audit-v7.json`](reports/pensee-audit-v7.json)

**État git** : le parent les a déjà committés dans `4ebeb683`. Le JSON du working tree est identique au commit ; le `.md` ne diffère que par 4 lignes ajoutées / 2 modifiées (liste des 26 docstrings + nuance sur la fiche v5), non committées. Je n'ai fait aucun commit et n'ai modifié aucun fichier existant.

**Résultat principal**
- **Invariants justes** sur le vivant 612 et le gelé 602 : 196 labels, 195 exacts (0,9949), couverture 0,8201, top-k 166/239, fr 135/135, en 60/61, 43 spans (21/17/5).
- **Cinq valeurs sont gelées, pas vivantes** : POS 0,7603 vs **0,7581**, F1 0,5595 vs **0,5555**, S 0,4741 vs **0,4688**, chunker 0,5858 vs **0,5822**, tête 0,7205 vs **0,7152**.
- **L'« avant » n'est pas la v6** : POS 0,7475 = v4, tête 0,6826 = v5a, F1 0,5130 = v6 vivant. V6 mesurée : POS 0,7461/0,7482, F1 0,5130/0,5164, tête 0,6785/0,6834.
- **POS contextuel** : +8 labels (pas 9), +0,0118 gelé / +0,0116 vivant (pas +0,0132) ; les 8 labels et r102 sont dans dev, test inchangé.
- **Règle du précédent** : 195→**160/196** sans elle ; 28 exacts en dev, 7 en test. La moitié « candidats du précédent » est **redondante** (0 effet).
- **Exemple faux** : `SUB « that she would come »` n'est pas produit (prédit `SUB « that she »`, span gold toujours perdu). « qui » 12 = en fait **6** ; 12 = 8 REL + 4 SUB françaises.
- **Portes** : **183/183**, zéro échec, mais **26 docstrings périmées** et **6 messages `/145` faux** ; aucune porte dev/test.
- **dev/test** : dev **133/134 (0,9925)**, F1 **0,5512**, couverture **0,8221** ; test **62/62 (1,0)**, F1 **0,5651**, couverture **0,8158**.
- **Contrôles négatifs** : permutation globale 1,81/196 (0,92 %) ; par type+langue 9,40/196 (4,79 %), max 20 ; observé 195/196, p<0,001. Candidat aléatoire dans la liste 70,24/196 (35,84 %) ; candidats permutés en top-k 2,46/196 (1,26 %).

Le message détaillé a été envoyé au parent.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `reports/rapport-audit-v7.md` | 1 | 16 |

### Commandes exécutées (échantillon)

- **T1** Inspect git HEAD and status
- **T1** List reports and relevant tool dirs
- **T1** Count lines of key files
- **T1** Run gold evaluator and save JSON
- **T1** Inspect gold sizes and dev/test split
- **T1** Extract measured metrics per source
- **T1** Compare living gold vs frozen gold
- **T1** Locate cited gate definitions
- **T1** Inspect autotest structure and gates count
- **T1** Find gate function definitions
- **T1** Run autotest gates
- **T1** Read bloc_linguistique header and classes
- **T1** Run autotest as module
- **T1** Locate key heuristic functions
- **T1** Locate Heuristique class
- **T1** Extract cited gate outputs
- **T1** Check gate totals
- **T1** List coverage reports and history
- **T1** Inspect v7 and upstream commits
- **T1** Read v6 sheet and JSON
- **T1** Compare v5 sheet versions
- **T1** Compare v4 sheet versions
- **T1** Read upstream JSONs
- **T1** Measure all metrics across golds and splits
- **T1** Measure S and chunker on living/frozen gold
- **T1** Create local copy of bloc_linguistique for ablations
- **T1** Run POS and previous-segment ablations
- **T1** Run ablations with proper module registration
- **T1** Find dev/test and v7 value gates
- **T1** Inspect v7 code changes
- **T1** Measure v6 code on living and frozen gold
- **T1** Remeasure v6 with correct root
- **T1** Search where before-values appear
- **T1** Check v6 JSON for POS/head
- **T1** Run target permutation and random candidate controls
- **T1** Check whether gold changed since v4/v5
- **T1** Extract v4 and v5 heuristic code
- **T1** Inspect gold split commit changes
- **T1** Replay v4/v5/v6/v7 code on golds
- **T1** Measure v4/v5 component F1 values
- … et 57 autres

## 4. Mesures et résultats marquants

- **T1** `- **Le mélange des types varie** : le test canonique est **REL-pauvre** (17 cibles, 22,4 %, contre`
- **T1** `35,0 % en dev) et **GP-riche** (35, 46,1 %, contre 37,4 %) ; l'attendu serait 23,5 REL et 30,5 GP.`
- **T1** `Ce n'est pas significatif (p=0,26), mais les décalés ne donnent pas le même mélange : test REL 34,8 %`
- **T1** `(décalé 1) et 35,1 % (décalé 2). C'est le principal levier des variations agrégées ci-dessous.`
- **T1** `Toutes les étendues observées sont dans la bande 95 % du tirage aléatoire. **Conclusion : le split est`
- **T1** `sous dev, ~2,7 cas pour 76), mais cette estimation n'est pas significative : les IC Wilson 95 % se`
- **T1** `- **F1** : test **+1,39 point**, mais l'agrégat est dominé par GN/GV (81 % des segments) : GV test`
- **T1** `aucun résidu 0.7919`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : sans_pos : bloc retiré 807 caractères sans_precedent : 3 sites retirés [stderr] Traceback (most recent call last):   File "<stdin>", line 15, in <module>   File "<stdin>", line 10, in charger_module  


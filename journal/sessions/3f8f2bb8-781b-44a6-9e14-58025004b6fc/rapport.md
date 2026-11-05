# Session 3f8f2bb8 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `3f8f2bb8-781b-44a6-9e14-58025004b6fc` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:22 |
| Durée | 1.3 h |
| Tours | 1 |
| Messages | 98 |
| Appels d'outils | 108 |
| Fichiers touchés | 1 |
| Commandes | 94 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer l'attachement v2** (l'intégration du 2026-11-05 14 h) et vérifier que ses chiffres et ses portes sont justes.  Contexte : `tools/bloc_linguistique.py` (classe `Heuristique`), `tools/tests/linguistique/evaluer_gold.py` (`charger()`, `evaluer_bloc`), `tools/tests/linguistique/gold_ … [2167 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2447 caractères tronqués]

*108 appels d'outils.* Actions notables :

- bash — Check repo state and locate attachment reports
- read
- bash — Line counts of key files
- bash — Find cited gate definitions
- bash — Find attachment references in autotest
- bash — Read CONVENTION_CIBLE definition
- bash — Replay full attachment evaluation
- bash — Find candidate head logic
- bash — Read audit attachment report
- bash — Inspect recent commits and file history
- bash — List recent commits all branches
- bash — Show v2 commit stat and bloc diff
- bash — Inspect lexicon variable and imports
- bash — Show evaluer_gold and autotest v2 diff
- … et 83 autres

**Synthèse produite :**

⏵ Delivering the audit summary.

\## Livrables

Deux fichiers neufs, aucun fichier existant modifié, aucun commit :

- `reports/rapport-audit-v2.md`
- `reports/pensee-audit-v2.json` (JSON valide, 43 comparaisons)

L'audit porte sur le **commit v2 `9d5337ce`**, avec le blob exact `git show 9d5337ce:tools/bloc_linguistique.py` (sha256 `6e843018…`) chargé depuis `/tmp` et `RACINE` forcé à la racine.

\## Verdict

**Toutes les valeurs v2 reproduisent** : labels 145, top1 140, top-k 142, exact 137, top-k strict 141 ; taux 0,9655 / 0,9793 / 0,9448 / 0,9724 ; rendement 0,5858 / 0,5941 / 0,5732 ; split 116/111 (0,9569) et 29/26 (0,8966) ; 8 échecs (3/5) ; spans 94 = 48/33/13 ; avant 126/134/123/88 ; gold 612. Le modèle appris a été rejoué : 142/145, +5, McNemar 7/2, p = 0,1797, IC [-0,69 ; +7,59] → rejeté, conforme.

**Deux arrondis seulement** : `p = 0,18` pour `0,179688` ; IC `[-0,7 ; +7,6]` pour `[-0,69 ; +7,59]`.

\## Écarts documentaires

1. **« 46 des 57 échecs » → 45.** A2 dit 45 ; le comptage indépendant donne 45 têtes candidates égales à la cible. Le 46 est `134 − 88` (sous-chaîne vs strict), une autre quantité. Le gain « +45 » est correct.
2. **Colonne avant du split** : elle est étiquetée « (POS gold) » mais **63/82 est l'ancien split lexical** (`_est_verbe`, lexique pré-v2). Le POS gold sur l'ancien bloc donne **116/97 (0,8362)** et **29/26 (0,8966)**. Le « **+48 cibles** » est `111 − 63`, un mélange de justes et de cibles ; ce n'est pas un gain. Le JSON nomme correctement les valeurs avant `verbe_est` / `nom_est`.
3. **Attributions incomplètes** : le segment précédent fait **+6 exact et +6 top1** ; le lexique fait **+8 exact/+8 top1/+8 top-k/+8 strict** ; les têtes font **+45 strict (26 REL + 19 GP), 0 exact**. Les totaux 137/140/142/141 sont justes, mais le tableau des corrections omet +6 top1 et +8 top-k/strict. Le helper `_cible_s_par_genre`, ajouté au v2, a **0 effet mesuré** et n'est pas documenté.

\## Portes

- **Au commit v2, les 15 portes citées passent** (T153, T161–T164, T166–T170, T172, T173, T175–T177). Registre v2 : **180** portes. Run complet au moment de l'audit (avant v3) : **181/181**.
- **8 docstrings périmées** : T153, T162, T163, T166, T167, T168, T172, T173. T168 imprime encore `/146` au lieu de `/145` ; T163 dit « 33 avant les correctifs » alors que 33 était un compte d'exacts à `d400e188` (A1 compte 22 échecs).
- **Chiffres non couverts** : `topk_taux` 0,5941 ; les taux avant et le split nom 82/63 ; le 69/69 SUB = VERB ; le compte 
… [1247 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v2.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check repo state and locate attachment reports
- **T1** Line counts of key files
- **T1** Find cited gate definitions
- **T1** Find attachment references in autotest
- **T1** Read CONVENTION_CIBLE definition
- **T1** Replay full attachment evaluation
- **T1** Find candidate head logic
- **T1** Read audit attachment report
- **T1** Inspect recent commits and file history
- **T1** List recent commits all branches
- **T1** Show v2 commit stat and bloc diff
- **T1** Inspect lexicon variable and imports
- **T1** Show evaluer_gold and autotest v2 diff
- **T1** Locate ablation anchors and old segment block
- **T1** Ablate heads, lexicon, segment rule and pre-v2 bloc
- **T1** Rerun ablations with sys.modules registration
- **T1** Run cited gates and count total
- **T1** Run full autotest gate registry
- **T1** Independent count of failures, spans, POS split
- **T1** Check full autotest result
- **T1** Verify SUB convention and split definitions
- **T1** Run full autotest as module
- **T1** Compute old and new splits
- **T1** Compare lexical split across bloc versions
- **T1** Check old CONVENTION_CIBLE text
- **T1** Debug old bloc labels and old convention
- **T1** Compare and re-evaluate old bloc copies
- **T1** Test cache warm-up effect on old bloc
- **T1** Locate generateur and its caches
- **T1** Check submodule commits across versions
- **T1** Inspect sys.path and generateur import setup
- **T1** Read _syntagmes_s path setup
- **T1** Read full autotest results
- **T1** Trace cold old-bloc S call
- **T1** Read A2 top-k and A3 learned-model reports
- **T1** Verify 46/57 head-reduction diagnostic
- **T1** Count head-fixable failures on pre-v2 state
- **T1** Count head-fixable top-k strict failures pre-v2
- **T1** Measure F1 and F1+F2 on pre-v2 base
- **T1** Count gates per commit and show post-v2 diff
- … et 54 autres

## 4. Mesures et résultats marquants

- **T1** `[still running after 60000ms; moved to background job bash-1077]`
- **T1** `> **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ❌ **ne pas intégrer le classement appris en l'état** ; le signal utile est le **vivier ordonné*`
- **T1** `> **142/145 (0,9793)** hors-pli contre **137/145 (0,9448)** pour la règle live (empreinte `6e843018`, 13:51) : **+5**, McNemar 7/2, **p = 0,18**, IC 95 % bootstrap **[-0,7 ; +7,6] pts** → **non signif`
- **T1** `| **rang 0 seul** (premier de la liste, sans apprentissage) | **139/145** | **0,9586** |`
- **T1** `- **Modèle contre rang 0** : 3 justes / 0 fausse (g003, g014, g016), **p = 0,25**. Le « appris » ajoute +3 au prior, pas davantage.`
- **T1** `1. **Le levier est le vivier, pas les poids** : le simple « premier candidat plein de la liste gauche → droite → dedans » fait **139/145** (95,9 %), déjà au-dessus de la règle live (137). Les 25 poids`
- **T1** `repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586, 'rang0_par_type': {'GP': {'n': 83, 'justes': 78, 'taux': 0.9398}, 'REL': {'n': 26, 'justes': 26, 'taux': 1.0}, '`
- **T1** `e0592c59 B13 — LE CACHE DU CHUNKER APPLIQUÉ : ×139 À 160 RÉPÉTITIONS, SORTIE IDENTIQUE (0/612) ; ×1 EN DÉFAUT, S DOMINE ; 181/181`
- **T1** `"rang0_justes": 139,`
- **T1** `"rang0_taux": 0.9586,`
- **T1** `"rang0_par_type": {`
- **T1** `b1b1292f B13 — LE CACHE COMPLET : UN SEUL CHUNKING DANS LES DEUX CHEMINS (T178), VALIDÉ PAR A11 (×11,0, ÉGALITÉ 612/612) ; 181/181`

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : exit=1 Traceback (most recent call last):   File "/tmp/audit_v2/ablate.py", line 37, in <module>     res['sans_tetes'] = measure(variant('sans_tetes', SRC.replace(head_block, '')))                    
- **T1** : File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", line 32, in <module>     from .coeur import Candidat, Etat ImportError: attempted relative import with no known parent 
- **T1** : cibles par type {'GP': 96, 'SUB': 69, 'REL': 74} SUB POS (tous, 69) : {'VERB': 69} total 69 SUB non-VERB: [] [stderr] Traceback (most recent call last):   File "<stdin>", line 36, in <module>   File "
- **T1** : old bloc cold RACINE fix: labels 145 fail 22 strict 123 [stderr] Traceback (most recent call last):   File "<stdin>", line 31, in <module>   File "<stdin>", line 28, in tete AttributeError: type objec
- **T1** : current                  top1=140 topk=142 exact=137 strict=141 | exact GP/SUB/REL=77/34/26 | strict GP/SUB/REL=81/34/26 | labels=83/36/26 [stderr] Traceback (most recent call last):   File "<stdin>",


# Session 3f8f2bb8 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `3f8f2bb8-781b-44a6-9e14-58025004b6fc` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:22 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 43 |
| Appels d'outils | 53 |
| Fichiers touchés | 0 |
| Commandes | 43 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer l'attachement v2** (l'intégration du 2026-11-05 14 h) et vérifier que ses chiffres et ses portes sont justes.  Contexte : `tools/bloc_linguistique.py` (classe `Heuristique`), `tools/tests/linguistique/evaluer_gold.py` (`charger()`, `evaluer_bloc`), `tools/tests/linguistique/gold_ … [2167 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2447 caractères tronqués]

*53 appels d'outils.* Actions notables :

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
- … et 30 autres

**Synthèse produite :**

⏵ Resolving the 180 vs 181 discrepancy in the registry count.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

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
- … et 3 autres

## 4. Mesures et résultats marquants

- **T1** `[still running after 60000ms; moved to background job bash-1077]`
- **T1** `> **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ❌ **ne pas intégrer le classement appris en l'état** ; le signal utile est le **vivier ordonné*`
- **T1** `> **142/145 (0,9793)** hors-pli contre **137/145 (0,9448)** pour la règle live (empreinte `6e843018`, 13:51) : **+5**, McNemar 7/2, **p = 0,18**, IC 95 % bootstrap **[-0,7 ; +7,6] pts** → **non signif`
- **T1** `| **rang 0 seul** (premier de la liste, sans apprentissage) | **139/145** | **0,9586** |`
- **T1** `- **Modèle contre rang 0** : 3 justes / 0 fausse (g003, g014, g016), **p = 0,25**. Le « appris » ajoute +3 au prior, pas davantage.`
- **T1** `1. **Le levier est le vivier, pas les poids** : le simple « premier candidat plein de la liste gauche → droite → dedans » fait **139/145** (95,9 %), déjà au-dessus de la règle live (137). Les 25 poids`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : exit=1 Traceback (most recent call last):   File "/tmp/audit_v2/ablate.py", line 37, in <module>     res['sans_tetes'] = measure(variant('sans_tetes', SRC.replace(head_block, '')))                    
- **T1** : File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", line 32, in <module>     from .coeur import Candidat, Etat ImportError: attempted relative import with no known parent 
- **T1** : cibles par type {'GP': 96, 'SUB': 69, 'REL': 74} SUB POS (tous, 69) : {'VERB': 69} total 69 SUB non-VERB: [] [stderr] Traceback (most recent call last):   File "<stdin>", line 36, in <module>   File "
- **T1** : old bloc cold RACINE fix: labels 145 fail 22 strict 123 [stderr] Traceback (most recent call last):   File "<stdin>", line 31, in <module>   File "<stdin>", line 28, in tete AttributeError: type objec


# Session 24529ced — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `24529ced-6556-4491-9633-9401c2dffb0c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 19:25 |
| Durée | 1.5 h |
| Tours | 1 |
| Messages | 99 |
| Appels d'outils | 97 |
| Fichiers touchés | 0 |
| Commandes | 85 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnostiquer les 43 spans non prédits** de l'attachement (état v7, commit `69bd865e`) et proposer des règles chiffrées, sans modifier le code.  Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_syntagmes_simple`, `_cible_precedent`), `tools/tests/linguistique/evaluer_gold.py` (` … [1761 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnost … [2041 caractères tronqués]

*97 appels d'outils.* Actions notables :

- bash — Inspect git state and recent commits
- bash — List linguistics tests and reports directories
- read
- bash — Locate key functions in bloc_linguistique
- bash — Find where Heuristique is configured
- bash — Inspect gold JSON structure
- bash — Run baseline analysis and dump missing spans
- bash — List the 43 missing spans with details
- bash — Show predicted segmentation around each missing span
- bash — Print closed-class lexicons relevant to rules
- bash — Compare simple chunker and S generator segments
- bash — Check verb recognition and _est_verbe definition
- bash — Gold stats, ADV sets, split membership, wrong attachment
- bash — Distribution of REL/SUB head markers by type and language
- … et 74 autres

**Synthèse produite :**

Mission terminée. **Deux fichiers neufs**, aucun fichier existant modifié, aucun commit.

- [`reports/rapport-spans-v7.md`](reports/rapport-spans-v7.md) — diagnostic complet, 43 cas détaillés, règles, rejets, limites.
- [`reports/pensee-spans-v7.json`](reports/pensee-spans-v7.json) — données structurées (43 cas, causes, règles, variantes, contrôles).

\## État

**239 cibles, 196 labels au bon span, 195 exacts** ; **43 non prédits = 21 REL / 17 SUB / 5 GP** (27 anglais, 16 français, 13 synthétiques). Baseline identique à `evaluer_bloc` ; F1 gold **vivant 612 = 0,5555** (le 0,5595 du commit est le **gelé 602**).

\## Effectifs par cause

| cause | n | dont REL/SUB/GP | sort |
|---|---:|---|---|
| Frontière de clause (15 arrêt précoce + 5 2e prédicat avalé) | **20** | 12/8/0 | 20 exacts (R1) |
| Type attendu différent (`When` → SUB ; r245) | **4** | 0/4/0 | 4 exacts (R2, +R3c pour r245) |
| GN qui avale (3 verbes synthétiques + collision `car`) | **4** | 1/3/0 | 1 exact, 3 absents |
| Lexique disjoint synthétique — REL sur-longues | **6** | 6/0/0 | 6 absents |
| Gold synthétique sans préposition (bug ligne 98) | **4** | 0/0/4 | 4 absents |
| Marqueur absent / élidé (`r035`, `r264`) | **2** | 1/1/0 | 2 absents |
| Lexique verbal réel (`achetée`/`roule`) | **1** | 1/0/0 | 1 absent |
| GP tronqué par `bus` | **1** | 0/0/1 | 1 exact (R3b) |
| Adverbe final (`tomorrow`, arbitrage `g017`) | **1** | 0/1/0 | 1 absent |

\## Règles (exacts gagnés / perdus vs baseline)

| règle | dev | test | tous |
|---|---:|---:|---:|
| **R1** frontière de clause (pronom, modaux, 2e prédicat) | **+15 / −0** | **+5 / −0** | **+20 / −0** |
| **R2** type REL/SUB par antécédent | **+3 / −0** (+1 label faux r245) | 0 / −0 | **+3 / −0** |
| **R3** (a `car`, b GP/déterminant, c `fall`/`call`) | +1 / −0 seule ; **+3 en marge** de R1+R2 | +1 / −0 | +2 seule ; **+4 en marge** |
| **R1+R2+R3** | **154/154** | **68/68** | **222/222** |

**Meilleure combinaison** : **222 labels, 222 exacts / 222** (exact/span **1,0000**), **222/239 cibles = 0,9289**, F1 vivant **0,5851** ; dev **154/154**, test **68/68**.

\## Restent 17 absents, 0 faux

4 GP gold (bug générateur, corrigeable par un commit gold : +4 exacts contrefactuels), 9 synthétiques (lexique disjoint ; les ajouter donne +8 mais **mesure invalide**), `r035` relative zéro, `r255` couverture verbale réelle, `r264` tokenisation `qu'`, `r288` adverbe final (retirer la règle perd `g017` en dev).

\## Rejetées

R3 globale DET (**dev +11/−4, test +4/−1**
… [584 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Inspect git state and recent commits
- **T1** List linguistics tests and reports directories
- **T1** Locate key functions in bloc_linguistique
- **T1** Find where Heuristique is configured
- **T1** Inspect gold JSON structure
- **T1** Run baseline analysis and dump missing spans
- **T1** List the 43 missing spans with details
- **T1** Show predicted segmentation around each missing span
- **T1** Print closed-class lexicons relevant to rules
- **T1** Compare simple chunker and S generator segments
- **T1** Check verb recognition and _est_verbe definition
- **T1** Gold stats, ADV sets, split membership, wrong attachment
- **T1** Distribution of REL/SUB head markers by type and language
- **T1** Find gold verbs unrecognized by the lexicon
- **T1** See how verb lexicon constants are built
- **T1** Read VERBES and SUJETS definitions
- **T1** Check synthetic GP convention and r102 attachment
- **T1** Inspect synthetic gold generator GP convention
- **T1** Read synthetic generator vocabulary
- **T1** Read generator verb list
- **T1** Simulate clause-boundary and type rules on dev
- **T1** Refined simulation with sentence-level clause scan
- **T1** Debug over-extension regressions
- **T1** Measure rule variants on dev with copied chunker
- **T1** Re-measure with S generator enabled (real baseline)
- **T1** Debug remaining dev misses and r228 gain
- **T1** Inspect r228 baseline status precisely
- **T1** Re-list dev gains cleanly
- **T1** Add modals to the R1 auxiliary test and re-measure dev
- **T1** Verify modal patch applied
- **T1** Use modal set for previous-token check and re-measure
- **T1** Evaluate rules on held-out test set
- **T1** Identify new wrong-cible label and remaining absences
- **T1** Retry detailed diff
- **T1** Debug r255 and r280 segmentation
- **T1** Trace simple chunker output on r255
- **T1** Verify override is called inside analyser
- **T1** Patch R3 ordering and R4, measure dev and test
- **T1** Restore exact baseline order and verify counts
- **T1** Inspect R3 losses and the GP case
- … et 45 autres

## 4. Mesures et résultats marquants

- **T1** `| les contrôles négatifs ? | permutation 1,81/196 (0,92 %) ; par type+langue 9,40/196 (4,79 %) ; observé 195/196 |`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : base 196 195 | best 220 218 [stderr] Traceback (most recent call last):   File "<stdin>", line 8, in <module> ValueError: too many values to unpack (expected 2) [exit code: 1]
- **T1** : [stderr]   File "/tmp/spans/rediger.py", line 245     w("`i = v + [t[0] for t in gv].index(prep) + 1` puis `("GP", i, i + len(g))` : le GP commence")       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **T1** : fixed ['r280'] écrit 617 lignes [stderr] Traceback (most recent call last):   File "/tmp/spans/rediger_json.py", line 49, in <module>     assert sum(c["effectif"] for c in causes) == 43            ^^^


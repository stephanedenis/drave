# Session session- — Rejouer et corriger exemples de la doc

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-b0a87524-43a4-4935-a248-72c1d42c8471` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 04:16 |
| Durée | 0.0 h |
| Tours | 1 |
| Messages | 40 |
| Appels d'outils | 53 |
| Fichiers touchés | 1 |
| Commandes | 49 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J11.1 : les exemples de la doc produit — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (F1 0,7902, 237/238, le schéma v2) et corrige les sorties qui ont bougé ; fiche `reports/rapport-exemples-rejoues.md` + JSON, commit.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J11.1 : les exemples de la doc produit — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (F1 … [130 caractères tronqués]

*53 appels d'outils.* Actions notables :

- bash — Show git status and recent commits
- read
- bash — Find J11 task references
- bash — Run first example current code
- bash — Read J11 task definitions
- bash — Read J11 section of bilan report
- bash — Check jq and CLI version/schema
- bash — Read CLI header
- bash — Replay example 1
- bash — Replay example 2
- bash — Replay example 3
- bash — Replay example 4 refusal
- bash — Replay example 5
- bash — Inspect example 1 JSON and current eval
- … et 39 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `docs/produit/exemples.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Show git status and recent commits
- **T1** Find J11 task references
- **T1** Run first example current code
- **T1** Read J11 task definitions
- **T1** Read J11 section of bilan report
- **T1** Check jq and CLI version/schema
- **T1** Read CLI header
- **T1** Replay example 1
- **T1** Replay example 2
- **T1** Replay example 3
- **T1** Replay example 4 refusal
- **T1** Replay example 5
- **T1** Inspect example 1 JSON and current eval
- **T1** Read r035 report
- **T1** Extract current evaluation summary
- **T1** Find evaluer options
- **T1** Run evaluer on live gold
- **T1** Inspect v2 partition in example 2
- **T1** Inspect v2 partition in example 5
- **T1** Check current date and HEAD
- **T1** Read r035 caveats and g011 refs
- **T1** Find unreachable spans references
- **T1** Inspect per-language attachment and ex2 readable
- **T1** Inspect gold evaluator functions
- **T1** Compute missed gold spans current
- **T1** Read v12 report context
- **T1** Read gold GP corrected report
- **T1** Read s065 report
- **T1** Check README refusal contract and CLI code
- **T1** Inspect refusal implementation and README
- **T1** Test refusal with --json
- **T1** Find references to examples doc
- **T1** Check reports index and existing example reports
- **T1** Read result-report method
- **T1** Look for doc replay tooling
- **T1** Search replay helpers
- **T1** Find the 13-span list
- **T1** Check status of known failure cases
- **T1** Find missing gold attachment targets
- **T1** Show full example 1 JSON
- … et 9 autres

## 4. Mesures et résultats marquants

- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `| **J2** | après-midi : corpus commun | ✅ fait | **21 textes**, 5 familles, 10 écritures, **418/438** paires exactes (95,4 %), 8/8 contrôles | `c3467170` (avec J3.1) | corpus multi-époques / multi-gen`
- **T1** `f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"`
- **T1** `reports/rapport-dev-test-v10.md:216:- **Le mélange des types varie** : test **REL-pauvre** (17 cibles, 22,4 %, contre 35,0 % en`
- **T1** `langue=fr script=Latn source=heuristique · 43 étiquettes · unités sémantiques=3 (48.6% du texte)`
- **T1** `cibles** (2000 tirages) → **1,997/220** (0,908 %) contre l'observé, p = 0 ; candidat aléatoire`
- **T1** `→ 42,14 % de top-1. Ici **222/222** : la marge est du même ordre.`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `tools/distiller_budget.py:8:rejoue le **budget complet** — 20 000 pas × 16 × 128 = **41 Mo** — et permet de`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../re`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : M journal/README.md  M journal/sessions/MANIFEST.md  M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md  M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md  M journal/se


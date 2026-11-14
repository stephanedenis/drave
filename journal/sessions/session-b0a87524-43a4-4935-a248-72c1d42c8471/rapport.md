# Session session- — Rejouer et corriger exemples de la doc

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-b0a87524-43a4-4935-a248-72c1d42c8471` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 04:16 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 141 |
| Appels d'outils | 157 |
| Fichiers touchés | 4 |
| Commandes | 113 |
| Sous-agents | 0 |
| Commits | 3 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J11.1 : les exemples de la doc produit — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (F1 0,7902, 237/238, le schéma v2) et corrige les sorties qui ont bougé ; fiche `reports/rapport-exemples-rejoues.md` + JSON, commit.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J11.1 : les exemples de la doc produit — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (F1 … [130 caractères tronqués]

*157 appels d'outils.* Actions notables :

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
- … et 134 autres

**Synthèse produite :**

**J11.1 terminé et committé** (`84e393bb`).

\### Ce que le rejeu a montré

| bloc | verdict | changement |
|---|---|---|
| §1 `g001` | corrigé | **19 → 20 étiquettes**, `./PONCT`, couverture POS `0,92 → 0,95` |
| §2 `g011` | identique | v2 publie `meta.partition`/`meta.alternative` sur le groupe 0 |
| §3 `r241` | corrigé | `left` : `NOUN 0,3 → VERB 0,85`, `./PONCT` ajouté |
| §4 refus | corrigé | code de sortie **1 → 3** ; `--json` rend l'annotation de refus |
| §5 `r035` | corrigé | **l'ancien échec est désormais prédit** : `REL [9:24] « she talks about » → film` |

Le point important : **`r035` n'est plus un échec**. Il ne reste que `g017` comme cible sans span prédit.

\### Chiffres courants

- F1 syntagmes **0,7902**
- POS **0,8625** (ouvert **0,7918**)
- attachement **238/238 labels** — **238/239 cibles**, couverture **0,9958**
- gold vivant : **612 phrases**, **3 179 tokens**, **239 cibles**

Le mandat disait `237/238` : c'est l'état d'avant `s065` (J6.2), qui a ajouté un label sans toucher un span.

\### Contrôle négatif

Mutation d'un token dans une copie de la doc (`left/VERB → NOUN`) : le comparateur signale **4/5** et l'écart exact `.pos[4].type: 'NOUN' != 'VERB'`. Sur la doc réelle : **5/5**.

\### Livrables

- [`docs/produit/exemples.md`](docs/produit/exemples.md) — 5 blocs corrigés, en-tête daté, §5 réécrit
- [`reports/rapport-exemples-rejoues.md`](reports/rapport-exemples-rejoues.md)
- [`reports/rapport-exemples-rejoues.json`](reports/rapport-exemples-rejoues.json)
- état [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) et roadmap mis à jour

\### Portes

- `porte-produit` : **verte**, autotest **183/183**
- revue de documentation : **verte** (725 fiches / 819 JSON)
- liens, tableaux, schémas : **verts**
- `en-cours` : 1 630 mots, T0 dans le budget
- `verifie_etat_a_jour --head` : **aucun fait après le dernier état**

Note : `reports/INDEX.md` reste modifié dans l'arbre par le cycle concurrent (ligne `s-paragraphes` non committée) ; la ligne de cette fiche y figure déjà.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `docs/produit/exemples.md` | 0 | 15 |
| `reports/rapport-exemples-rejoues.md` | 1 | 1 |
| `docs/pilotage/en-cours.md` | 0 | 13 |
| `docs/pilotage/roadmap.md` | 0 | 2 |

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
- … et 73 autres

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
- **T1** `comme « 100 % du langage » : c'est 100 % des spans prédits, sur **92,89 %** des cibles.`
- **T1** `| [rapport-s-corpus-reel.md](rapport-s-corpus-reel.md) | S — L'analyseur lit le français propre (65,5 % de GN+GV), pas le CEGEP OCR (8,5 %, plancher du mélange) |`
- **T1** `| [rapport-familles-9.md](rapport-familles-9.md) | C3.2c — les 9 familles : 7 sur 9 au-dessus de 30 % |`
- **T1** `38:**État au 14/11 03 h 30.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet`
- **T1** `192:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `267:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../..`
- **T1** `37 48 - **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥`
- **T1** `68 63 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibl`
- **T1** `26 134 - **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité st`
- **T1** `27 135 - **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,89`
- **T1** `-langue=fr script=Latn source=heuristique · 19 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `+langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `+  (`membres: 3` ; rang 1 = REL longue, rang 2 = GV, rang 3 = REL courte) et `meta.alternative``
- **T1** `-comme « 100 % du langage » : c'est 100 % des spans prédits, sur **92,89 %** des cibles.`
- **T1** `+comme « 100 % du langage » : c'est 100 % des spans prédits, sur **99,58 %** des cibles. Le cas`
- **T1** `@@ -617,8 +655,9 @@ comme « 100 % du langage » : c'est 100 % des spans prédits, sur **92,89 %** d`

## 5. Erreurs rencontrées

7 sorties en erreur ou divergentes. Les premières :

- **T1** : M journal/README.md  M journal/sessions/MANIFEST.md  M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md  M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md  M journal/se
- **T1** : a6808c5e CHANTIER — LE PLAN EST RELU À CHAQUE TOUR (LA BOUCLE VOYAIT UNE FILE VIDE APRÈS UN AJOUT DE TÂCHES) ; ÉTAT HORODATÉ 03ecee41 J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236
- **T1** : 2240069       01:24 python3 -m tools.pensee.autotest 2240070       01:24 python3 -m tools.pensee.autotest [exit code: 1]
- **T1** : [stderr] wc: /tmp/j111/porte-produit-autotest.log: No such file or directory tail: cannot open '/tmp/j111/porte-produit-autotest.log' for reading: No such file or directory [exit code: 1]
- **T1** : a6808c5e CHANTIER — LE PLAN EST RELU À CHAQUE TOUR (LA BOUCLE VOYAIT UNE FILE VIDE APRÈS UN AJOUT DE TÂCHES) ; ÉTAT HORODATÉ 03ecee41 J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236
- **T1** : [stderr]   ✅ index : aucun fait stagé sans état error: Terminal is dumb, but EDITOR unset Please supply the message using either -m or -F option. [exit code: 1]
- **T1** : MM journal/2026-11-14/README.md MM journal/2026-11-14/docs.md MM journal/2026-11-14/memoire.md MM journal/2026-11-14/mesures.md MM journal/2026-11-14/portes.md MM journal/README.md MM journal/THEMES.m

## 6. Commits

- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet git commit --dry-run -- docs/produit/exemples.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/r
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet git commit -- docs/produit/exemples.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-exe
- cat > /tmp/j111/commit-msg.txt <<'MSG' J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238  Les 5 bl


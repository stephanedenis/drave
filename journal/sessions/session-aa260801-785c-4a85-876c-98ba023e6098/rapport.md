# Session session- — Vérification roue Python et gold CLI

> **Journaux :** [le jour](../../2026-11-16/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-aa260801-785c-4a85-876c-98ba023e6098` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-16 00:31 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 142 |
| Appels d'outils | 158 |
| Fichiers touchés | 9 |
| Commandes | 102 |
| Sous-agents | 0 |
| Commits | 2 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche U2 (suite de T1) : **la roue** — `python3 -m build` (ou `pip wheel .`) produit `drave-0.1.0-py3-none-any.whl`, installée dans un venv **propre** depuis la roue (pas le dépôt) : `drave --version` et `drave analyser` depuis `/tmp` ; le **contrôle négatif** : la roue sans les gold doit-elle échouer (le CLI lit `tools/tests/linguistique/gold_*.json` — si les gold ne sont pas dans la roue, `evalu … [139 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche U2 (suite de T1) : **la roue** — `python3 -m build` (ou `pip wheel .`) produit `drave-0.1.0-py3-none-any.whl`, ins … [419 caractères tronqués]

*158 appels d'outils.* Actions notables :

- bash — Inspect repo root and git state
- bash — Read current state doc
- bash — Read pyproject and src layout
- bash — Find task references
- bash — Find section 8.10 and T1 report
- bash — Read CLI entrypoint start
- bash — Inspect tools tree and gold files
- bash — Find evaluer and gold option handling
- bash — Extract U2 mandate from plan
- bash — Read evaluer implementation
- bash — Read rest of evaluer and main
- bash — Read evaluer_gold loading logic
- bash — Check package init files and imports
- bash — Check build tooling availability
- … et 124 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 10 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Inspect repo root and git state
- **T1** Read current state doc
- **T1** Read pyproject and src layout
- **T1** Find task references
- **T1** Find section 8.10 and T1 report
- **T1** Read CLI entrypoint start
- **T1** Inspect tools tree and gold files
- **T1** Find evaluer and gold option handling
- **T1** Extract U2 mandate from plan
- **T1** Read evaluer implementation
- **T1** Read rest of evaluer and main
- **T1** Read evaluer_gold loading logic
- **T1** Check package init files and imports
- **T1** Check build tooling availability
- **T1** Check U2 status and neighbors in plan
- **T1** Check packaging config and cross imports
- **T1** List imports of modules needed
- **T1** Inspect restitution and miroir headers
- **T1** Check tagger construction imports
- **T1** Check remaining imports and packaging test
- **T1** Read tagger import and transport
- **T1** Measure package candidates
- **T1** Locate gold file constants
- **T1** Find uses of --gold
- **T1** Check CLI tests for evaluer
- **T1** Find gates touching wheel/packaging
- **T1** Read product test sections
- **T1** Inspect uncommitted changes
- **T1** Check ignore and branch
- **T1** List JSON data under tests
- **T1** Check if packaging test is gated
- **T1** Find which gate runs tests
- **T1** Build wheel with current config
- **T1** Inspect wheel contents
- **T1** Inspect tools/tests contents
- **T1** Check llm data dependencies
- **T1** Inspect deepseek RACINE use
- **T1** Read T1 JSON structure
- **T1** Search session plan for U2
- **T1** Inspect journal structure
- … et 62 autres

## 4. Mesures et résultats marquants

- **T1** `d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO`
- **T1** `83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE`
- **T1** `9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** `7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `docs/pilotage/chantiers.md:90:| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime**`
- **T1** `docs/pilotage/plan-travail.md:39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**`
- **T1** `docs/pilotage/plan-travail.md:195:   **0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **`
- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `docs/pilotage/roadmap.md:307:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `base réelle 452, **183/184 (99,46 %)**. Détail : [`rapport-g017.md`](../../reports/rapport-g017.md).`
- **T1** `| **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |`
- **T1** `work/ocr/cegep64/controle/train.txt:113012:U9P2MS ‘W[OU203S poor`
- **T1** `"langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)",`
- **T1** `- **Note** : l'attachement est à **236/237 (0,9916)**, la couverture 0,9916, POS **86,25 %**, F1 **0,7535**, 2 spans ; la seule rouge est`
- **T1** `CPU + neuronal de contrat, parallèle/cascade, activation 51–76 %) ; **398 langues à 0,9687**,`
- **T1** `**tête 0,560**, pragmatique **1,0/1,0/0,994/0,889** ; cascade (mock) **67,1 %** ;`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `| 23:30 | `9a291c8b` | T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS | `en-cours.md`, `roadmap.md`, `README.m`
- **T1** `fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%`
- **T1** `mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `166:**U1 — les deux O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),`
- **T1** `| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO |`
- **T1** `| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO | `en`
- **T1** `[still running after 120000ms; moved to background job bash-95]`
- **T1** `| `ddf8d740` | 2026-10-22 08:28 | 0.1 Mo | 22 Ko | 1 | 17 | 14 | 0 | 0 |`
- **T1** `| `df1b1098` | 2026-10-31 17:52 | 0.0 Mo | 13 Ko | 1 | 4 | 0 | 0 | 0 |`
- **T1** `| `e14c26ae` | 2026-10-02 21:15 | 0.7 Mo | 109 Ko | 1 | 49 | 76 | 0 | 0 |`
- **T1** `-| `e181ce02` | 2026-10-31 17:40 | 21.1 Mo | 4043 Ko | 202 | 4058 | 3625 | 8 | 18 |`
- **T1** `+| `e181ce02` | 2026-10-31 17:40 | 21.1 Mo | 4045 Ko | 202 | 4061 | 3628 | 8 | 18 |`
- **T1** `| `e7dfe34f` | 2026-09-28 14:56 | 0.2 Mo | 28 Ko | 1 | 20 | 21 | 0 | 0 |`
- **T1** `| `ea169cb1` | 2026-11-05 23:24 | 0.9 Mo | 159 Ko | 1 | 120 | 136 | 2 | 0 |`
- **T1** `| `ebd3d5a2` | 2026-10-22 08:14 | 0.1 Mo | 26 Ko | 1 | 19 | 14 | 0 | 0 |`
- **T1** `| `session-` | 2026-11-07 12:18 | 0.6 Mo | 149 Ko | 1 | 112 | 138 | 2 | 0 |`
- **T1** `| `session-` | 2026-11-14 06:53 | 0.6 Mo | 153 Ko | 1 | 123 | 134 | 2 | 0 |`
- **T1** `| `session-` | 2026-11-07 14:46 | 0.6 Mo | 128 Ko | 1 | 74 | 106 | 3 | 0 |`
- **T1** `+| `session-` | 2026-11-16 00:31 | 0.6 Mo | 166 Ko | 1 | 131 | 147 | 2 | 0 |`
- **T1** `| `session-` | 2026-11-14 04:16 | 0.6 Mo | 155 Ko | 1 | 141 | 157 | 3 | 0 |`
- **T1** `| `session-` | 2026-11-07 10:46 | 0.0 Mo | 12 Ko | 1 | 4 | 0 | 0 | 0 |`
- **T1** `| `session-` | 2026-11-15 09:44 | 0.7 Mo | 140 Ko | 1 | 141 | 156 | 1 | 0 |`
- **T1** `| `session-` | 2026-11-14 05:43 | 0.7 Mo | 147 Ko | 1 | 121 | 138 | 1 | 0 |`
- **T1** `| `session-` | 2026-11-15 12:40 | 0.7 Mo | 113 Ko | 1 | 97 | 102 | 0 | 0 |`
- **T1** `| `session-` | 2026-11-15 22:35 | 1.0 Mo | 179 Ko | 1 | 148 | 177 | 1 | 0 |`
- **T1** `-| `session-` | 2026-11-15 23:43 | 1.0 Mo | 241 Ko | 1 | 252 | 281 | 2 | 0 |`
- **T1** `+| `session-` | 2026-11-15 23:43 | 1.0 Mo | 248 Ko | 1 | 257 | 287 | 2 | 0 |`
- **T1** `| `session-` | 2026-11-14 03:46 | 0.7 Mo | 134 Ko | 1 | 81 | 114 | 1 | 0 |`
- **T1** `| `session-` | 2026-11-14 03:18 | 0.7 Mo | 162 Ko | 1 | 131 | 155 | 2 | 0 |`
- **T1** `| `session-` | 2026-11-15 02:15 | 0.7 Mo | 160 Ko | 1 | 92 | 156 | 3 | 0 |`
- **T1** `| `session-` | 2026-11-15 12:05 | 0.7 Mo | 153 Ko | 1 | 115 | 136 | 1 | 0 |`
- **T1** `| `session-` | 2026-11-15 23:16 | 0.5 Mo | 129 Ko | 1 | 103 | 121 | 0 | 0 |`
- **T1** `-Total : 376.0 Mo de traces brutes.`
- **T1** `+Total : 376.7 Mo de traces brutes.`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : work/ocr/census-cegep.json:14452:   "chemin": "/home/stephane/Data13TB/stephane/archives/CEGEP/import-export-2026-06-20/Documents/Enseignement__02/Cours/SW Engineering/Les 100 schémas du management  L
- **T1** : tools/verifier_faq.py:353:        "empaquetage": {"livre": "pip install -e . + commande drave", tools/verifier_faq.py:401:        "empaquetage": { --- count gates 86     DRAVE_DUMP_COUCHES=/tmp/porte_
- **T1** : # Les portes : lancer, lire le verdict, ne pas se tromper de rouge  > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.  ## La commande

## 6. Commits

- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet git add pyproject.toml tools/drave.py tools/tests/test_empaquetage.py docs/produit/README.md docs/pilotage/en
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet git add journal/2026-11-16/README.md journal/2026-11-16/mesures.md git commit -F - <<'MSG' JOURNAL — 2026-11-


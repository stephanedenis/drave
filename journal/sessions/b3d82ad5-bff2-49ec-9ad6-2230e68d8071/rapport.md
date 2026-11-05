# Session b3d82ad5 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `b3d82ad5-bff2-49ec-9ad6-2230e68d8071` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:47 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 25 |
| Appels d'outils | 33 |
| Fichiers touchés | 0 |
| Commandes | 32 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer l'effet des **cibles multiples** du gold sur la mesure d'attachement, sans modifier le code.  Contexte : `tools/tests/linguistique/evaluer_gold.py::evaluer_bloc` compare la cible choisie à `cibles[0]` pour l'exact, mais le gold autorise parfois **plusieurs cibles** (`cibles` = list … [1681 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer l' … [1961 caractères tronqués]

*33 appels d'outils.* Actions notables :

- bash — Show repo status and branch
- bash — List linguistique tools and reports
- read
- bash — Read head of gold_reel.py
- bash — Find reports with 239 targets
- bash — Read more of gold_reel.py
- bash — Inspect attachement reports
- bash — Inspect gold_reel.json structure
- bash — Read A7 section of audit report
- bash — Count targets per gold source
- bash — List all multi-target segments
- bash — Find multiword target values
- bash — Check gold_gele counts
- bash — Run heuristic and inspect predicted targets
- … et 19 autres

**Synthèse produite :**

⏵ Calcul détaillé des taux (a), (b), (c) et des sous-populations

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Show repo status and branch
- **T1** List linguistique tools and reports
- **T1** Read head of gold_reel.py
- **T1** Find reports with 239 targets
- **T1** Read more of gold_reel.py
- **T1** Inspect attachement reports
- **T1** Inspect gold_reel.json structure
- **T1** Read A7 section of audit report
- **T1** Count targets per gold source
- **T1** List all multi-target segments
- **T1** Find multiword target values
- **T1** Check gold_gele counts
- **T1** Run heuristic and inspect predicted targets
- **T1** Find attachement production in block
- **T1** Find head-reduction helpers
- **T1** Read head-reduction helpers and attachment code
- **T1** Read annotation audit report
- **T1** Read rest of audit report
- **T1** List unusual target strings
- **T1** Search existing multi-target work
- **T1** Check target files and prior multi-target analysis
- **T1** Check sibling session digest tail
- **T1** Check code state and hashes
- **T1** Inspect recent attachment measurements
- **T1** Run evaluer_bloc for current rates
- **T1** Inspect git history for multi-target work
- **T1** Search roadmap for A13
- **T1** Inspect attachement v2 commit
- **T1** Read attachment v2 report
- **T1** Search multi-target mentions in recent reports
- **T1** Compute detailed per-segment rates
- **T1** Verify head-reduction helper

## 4. Mesures et résultats marquants

- **T1** `| **moi ↔ gold**, cible top-1 | **20/20 = 100 %** | 83,9–100 % |`
- **T1** `| moi ↔ gold, sans `r057` (cas non aveugle) | 19/19 = 100 % | 83,2–100 % |`
- **T1** `| **moi ↔ bloc HEAD**, strict (même type + span) | **10/20 = 50 %** | 29,9–70,1 % |`
- **T1** `| moi ↔ bloc HEAD, cible d'attachement seule | **17/20 = 85 %** | 64,0–94,8 % |`
- **T1** `| moi ↔ bloc post-correctif, strict | 11/20 = 55 % | 34,2–74,2 % |`
- **T1** `| moi ↔ bloc post-correctif, attachement seul | 18/20 = 90 % | 69,9–97,2 % |`
- **T1** `hasard (0,77 %).`
- **T1** `(`r293`, `s052`, `r230`). Au span exact, il est juste **10/12 = 83,3 %**, cohérent avec le gold entier`
- **T1** `(**123/145 = 84,8 %**).`
- **T1** `**11/20**, attachement **18/20** ; sur tout le gold **137/145 = 94,5 %** (contre 123/145) et les échecs`
- **T1** `Le span exact (12/20 = 60 %) et la justesse au span exact (10/12 = 83,3 %) sont dans la même zone que le`
- **T1** `gold entier : **145/239 = 60,7 %** de spans exacts et **123/145 = 84,8 %** de cibles justes au span exact.`
- **T1** `| HEAD `e1171032` (aveugle) | `d9c9d559` | 10/20 | 13/20 | 17/20 | 3 | 123/145 = 84,8 % | 69/83 | 28/36 | 26/26 |`
- **T1** `| snapshot 13:51:26 | `6e843018` | **11/20** | 14/20 | **18/20** | **2** | **137/145 = 94,5 %** | 77/83 | 34/36 | 26/26 |`
- **T1** `que **26/74** REL (35,1 %), mais quand il le fait, la cible est juste **26/26**. Dans l'échantillon,`
- **T1** `| accord moyen avec le gold | **0,77 %** |`
- **T1** `| IC95 des simulations | 0–5 % |`
- **T1** `Le contrôle interne d'`evaluer_gold` (`c in rng.choice(cibles)`) donne 1/239 = 0,42 %, du même ordre. Le`
- **T1** `1. **n = 20** : IC larges (20/20 → 83,9–100 % ; 10/20 → 29,9–70,1 %). On ne conclut pas sur les 239 ; on`
- **T1** `e0592c59 B13 — LE CACHE DU CHUNKER APPLIQUÉ : ×139 À 160 RÉPÉTITIONS, SORTIE IDENTIQUE (0/612) ; ×1 EN DÉFAUT, S DOMINE ; 181/181`
- **T1** `(rang 0, ordre gauche→droite→dedans) donne **139/145** (+2). Conclusion : **ne pas intégrer**`


# Session b3d82ad5 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `b3d82ad5-bff2-49ec-9ad6-2230e68d8071` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:47 |
| Durée | 1.1 h |
| Tours | 1 |
| Messages | 68 |
| Appels d'outils | 95 |
| Fichiers touchés | 1 |
| Commandes | 78 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer l'effet des **cibles multiples** du gold sur la mesure d'attachement, sans modifier le code.  Contexte : `tools/tests/linguistique/evaluer_gold.py::evaluer_bloc` compare la cible choisie à `cibles[0]` pour l'exact, mais le gold autorise parfois **plusieurs cibles** (`cibles` = list … [1681 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer l' … [1961 caractères tronqués]

*95 appels d'outils.* Actions notables :

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
- … et 79 autres

**Synthèse produite :**

Mesure faite, sans modifier le code ni committer. Fiche : `reports/rapport-multicibles.md` · JSON : `reports/pensee-multicibles.json`.

**Pin** : HEAD `b1b1292f` (V3, bloc `9da6dee7…`). Le worktree `9544f…`, encore modifié par un autre agent, n'est pas inclus. Le pin V2 `15ee10d3` (`5640809e…`, contexte A7) sert de comparaison.

**Les trois taux — 145 segments au bon span**
| définition | taux |
|---|---:|
| (a) `cible == cibles[0]` | **141/145 = 97,24 %** |
| (b) `cible in cibles` | **143/145 = 98,62 %** |
| (c) `cible == tête d'une cible` | **143/145 = 98,62 %** |

Écart (b−a) : **+2 cas, +1,38 pt** ; GP 80/83 → 82/83 (+2,41 pt), SUB 35/36 et REL 26/26 inchangés. **(c) = (b)** : la réduction à la tête est un no-op sur ce gold.

**Sur 239 cibles** : (a) 141/239 = 59,00 % ; (b) 143/239 = 59,83 % ; (c) 143/239 ; +2 (+0,84 pt). **Contexte V2** : 137/145 = 94,48 % → 139/145 = 95,86 %, même +2 et mêmes cas.

**Les 2 gains** sont `s108` et `s122`, deux GP **synthétiques** où le bloc choisit `papier`, la 2e cible. Sur hand+reel : 114/115 = 99,13 %, **écart 0**. Contrôle négatif (1 000 tirages) : P1 p=0,001 ; P2 p=0,001 (exact 1/903) ; mais McNemar p=0,5 et bootstrap [0 ; +3,45] pt : correction réelle de 2 cas, pas gain de population.

**Recommandation** : adopter **(b)** pour `exact` et `topk_exact` — annoncer **143/145 = 98,62 %** et **143/239 = 59,83 %**, avec la mention « +2 cas, dont 2 synthétiques ». **Ne pas ajouter (c)** (no-op). Documenter `CONVENTION_CIBLE` (GP multi = `[gouverneur, tête nominale]`) et décider si l'attachement nominal compte ; sinon nettoyer le gold. Corriger à part `s041` (cible vide) et `r309` (SUB). Si (b) est adopté, reclasser le split verbe/nom par la cible appariée : **114/112 verbe, 31/31 nom**.

Aucun fichier existant modifié ; aucun commit. Les deux fichiers sont neufs (index : `A`, sans commit de ma part).

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-multicibles.md` | 2 | 11 |

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
- **T1** Run full analysis with null controls
- **T1** Inspect g003 tokenization
- **T1** Locate roadmap line for multi-target
- **T1** Compute paired uncertainty and inspect key cases
- **T1** Compute rates by source and POS
- **T1** Debug per-source discrepancy
- **T1** Check for nondeterminism in block
- **T1** Repeat measurement three times
- … et 38 autres

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
- **T1** `docs/pilotage/roadmap.md:178:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `docs/pilotage/roadmap.md:253:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
- **T1** `docs/pilotage/chantiers.md:88:| **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter que le résidu ? | ✅ **contrat + bloc v0** : 9 niveaux, **398 langues à 0,`
- **T1** `docs/pilotage/chantiers.md:90:| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime**`
- **T1** `docs/pilotage/plan-travail.md:39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**`
- **T1** `delta bootstrap 95% 0.0 0.034482758620689655 mean 0.01381448275862069`
- **T1** `"definition": "adopter (b) cible in cibles pour exact et topk_exact ; conserver les deux dénominateurs (239 rendement, 145 span) et annoncer 139/145 = 95,86 % et 139/239 = 58,16 %, avec la mention « +`
- **T1** `"split": "si (b) est adopté, classer verbe/nom par la cible appariée : 114/111 verbe (97,37 %), 31/28 nom (90,32 %) au lieu de 116/111 et 29/26",`
- **T1** `142:| **Total** | **145** | **36** | **137 (94,48 %)** | **139 (95,86 %)** | **+2 (+1,38 pt)** |`
- **T1** `15:> nominale (`papier`) que le gold autorise ; sur hand+reel, `(a) = (b) = 110/115 = 95,65 %`.`
- **T1** `147:**Le +2 est entièrement synthétique.** Sur hand+reel (115 labels), `(a) = (b) = 110/115 = 95,65 %`,`
- **T1** `43/239 cibles (17,99 %) 1`
- **T1** `36/145 labels (24,83 %) 1`
- **T1** `43/96 (44,79 %) 1`
- **T1** `36/83 (43,37 %) 1`
- **T1** `137 (94,48 %) 3`
- **T1** `139 (95,86 %) 4`
- **T1** `33/36 (91,67 %) 1`
- **T1** `31,086/36 (86,35 %) 1`
- **T1** `1,23/145 (0,85 %) 1`
- **T1** `b1b1292f7983a5f7349bc81dc92404be5cd99a36 2026-11-05 15:29:19 -0500 B13 — LE CACHE COMPLET : UN SEUL CHUNKING DANS LES DEUX CHEMINS (T178), VALIDÉ PAR A11 (×11,0, ÉGALITÉ 612/612) ; 181/181`
- **T1** `b1b1292f B13 — LE CACHE COMPLET : UN SEUL CHUNKING DANS LES DEUX CHEMINS (T178), VALIDÉ PAR A11 (×11,0, ÉGALITÉ 612/612) ; 181/181`
- **T1** `"head_sujet": "B13 — LE CACHE COMPLET : UN SEUL CHUNKING DANS LES DEUX CHEMINS (T178), VALIDÉ PAR A11 (×11,0, ÉGALITÉ 612/612) ; 181/181",`
- **T1** `141 (97,24 %) 4`
- **T1** `143 (98,62 %) 5`
- **T1** `35/36 (97,22 %) 1`
- **T1** `33,086/36 (91,91 %) 1`
- **T1** `1,251/145 (0,86 %) 1`
- **T1** `137 (94,48 %) 1`
- **T1** `139 (95,86 %) 1`
- **T1** `2026-11-05 15:29:19 -0500 B13 — LE CACHE COMPLET : UN SEUL CHUNKING DANS LES DEUX CHEMINS (T178), VALIDÉ PAR A11 (×11,0, ÉGALITÉ 612/612) ; 181/181`
- **T1** `b1b1292f7983a5f7349bc81dc92404be5cd99a36 B13 — LE CACHE COMPLET : UN SEUL CHUNKING DANS LES DEUX CHEMINS (T178), VALIDÉ PAR A11 (×11,0, ÉGALITÉ 612/612) ; 181/181`


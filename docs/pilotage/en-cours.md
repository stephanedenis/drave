# En ce moment

**Mis à jour : 2026-11-20, 10 h 00 HNE (le README racine réécrit : la vision, l'état du 20/11, la vulgarisation)**

> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 11** : serveurs locaux arrêtés ; professeurs par l'**API DeepSeek** ; GPU à Drave.

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures *(actif)*

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : validation.
- **Ambition** : rôles.
- **Stratégie** : contrôles.
- **Objectif final** : gold 60.
- **Fait** : types **61/61**, rôles **144/144** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
- **Ce qu'elle fait** : **session close** ; **`/paragraphes`** v7, **`/`** 369 + **profondeur** (324 appariés, **95** à ≥3) ; **`s/v7`** à fusionner.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**.
- **Prochaine action** : **rétro-traduction** — script + 9/9, l'alignement à raffiner ; les **71 langues** ; la migration `/` est faite (324/369).
- **Bloquants** : aucun ; 8765 pris (lancer 9000) ; migration = choix.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(en pause)*

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13 · **Stratégie** : v0 · **Ambition** : tracé · **Objectif final** : moteur v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.
- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**) ; **U1** 4,0 → 0,82 s ; **U2** roue 1 727 201 o ; **U3** profils 20/20 ; **V1** 0,8625/0,8891 ; **V2** **27/27** ; **V3** la clôture — **86/82/4** → **84/2**, tag `exploitable-2026-11-16` ([bilan 2](../../reports/rapport-bilan-exploitable-2.md)).
- **Ce que font les autres** : N2.
- **Prochaine action** : **J4** (fenêtre remisée 11 h 30-19 h 30) ; T132/T133 ; la décision `auto`. L'entraînement long qu'elle attendait est **fait** (150 M, 19-20/11).
- **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles ; **19/19 verdicts `389b99f`** ; [v2](../../reports/rapport-coordination-s-v2.md).
- **N2 — 100 M mesuré · corpus épinglé** : banc apparié — greedy **0,882** vs **0,884** (34 M), répétition **6** vs **9** ; [fiche](../../reports/rapport-banc-generation-100m.md) ; **corpus épinglé** (manifeste `fae5bb73…`, `--verifie` 6,5 s) ; **val épinglé 4,6792** contre **4,0139** sur la fin du train (**+16,57 %**, mêmes poids) — [pin](../../reports/rapport-corpus-epingle.md), [val](../../reports/rapport-natif-val-deux-decoupages.md).
- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → 4) ; **U3** profils 20/20 ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [roue](../../reports/rapport-roue.md), [profils](../../reports/rapport-profils.md).
- **L — le bloc langue** : contrat ; frontière script 1,0 / langue 0,137/0,9687 ; fusion réparée **0,9309/0,8226/0,8784/0,9954**.
- **R0.7 / W2–W3 — le tagger** : 402 **0,9198 → 0,9643**, H50 **0,6842 → 0,8607** ; défaut hors ligne **0 socket**, `--tagger` **code 4** sans clé ; **lot 612 exécuté** (11:30, **608 appels**, 87 550 tokens, **0,01869 $**) : POS **0,9572** contre **0,8625** (**+9,47**), ouvert **0,978** contre 0,7918, fermé à parité, **0 refus** — [W2](../../reports/rapport-tagger-h50.md), [lot](../../reports/rapport-tagger-612.md).
- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues, **V14 3/21** ; B2 **négatif** ; B1 **60 paires**, **27/60**, calibration **42/44** ; CIC **42/42**, B3 **42/42** types de Bruijn ; [atomes](../../reports/rapport-atomes-niveaux.md), [B1](../../reports/rapport-protocole-date.md), [CIC](../../reports/rapport-cic-verificateur.md), [v2](../../reports/rapport-cic-v2.md).
- **N4 — grammaticalité et données** (18/11) : GV **6,90 → 1,45** (34 → 73 M) ; **135,5 Go**, **7,5 Go** exploitable ; dédup **par ligne** **8,042 %** — corpus v2 **6,90 Go** épinglé (`9861fb39…`) ; [grammaticalité](../../reports/rapport-grammaticalite-100m.md), [données](../../reports/rapport-donnees-inventaire.md), [blocs](../../reports/rapport-dedup-blocs.md), [lignes](../../reports/rapport-dedup-lignes.md).
- **N — l'entraînement, les corpus et le décodage** (18-20/11) : 73 M **4,6792 → 3,0098** ; **150 M** : v1 **2,844** / v2 **3,038** (110k) ; **nuit** : `wiki_big` seul **6,8349** (v1 6,867, v2 7,093 ; **±1,8 %** de run-à-run), long-forme **7,7479** — la **sélection du contenu** est confirmée, la forme écartée ; **top-40/T=0,5** bat le greedy (**0,907**) ; [courbe](../../reports/rapport-courbe-r1-r3.md), [150 M](../../reports/rapport-150m-nuit.md), [nuit](../../reports/rapport-nuit-wikibig.md), [sélection](../../reports/rapport-selection-contenu.md), [décodage](../../reports/rapport-decodage-r1.md).
- **A2.6 — la règle des experts** (18-19/11) : bande **7,0 Go/s** (16 : aucun gain), chemins optimisés lents, PPL **37,2013** ; **branchée** en trace sous opt-in sur le vrai 30B (**1,10 Go/jeton · 156,9 ms → VRAM**), **15/15** tests, **porte** dédiée ; la **décision**, les **bandes** et le garde des clusters ; **lire** les clusters reste ; [recon](../../reports/rapport-a2.6-reconnaissance.md), [bande](../../reports/rapport-a2.6-bande-experts.md), [branchement](../../reports/rapport-a2.6-branchement.md).
- **N3.7–N3.10** (17/11) : variantes, routes, moteurs Rust ↔ numpy **3,576e-07**, le profil « court » bit-exact.

## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **91** (dont `porte-a2.6-experts` le 18/11) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **817** / **1049** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **128** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **20/11 05 h 58 → 07 h 58** : **91** portes, **89/2** ; seules `indice` (836 s) et `melange` (105 s) **structurelles** ; `sessions` **verte** ; machine au repos (les runs de la nuit finis) | `work/portes/roue-1120-0558/registre.txt` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 rig+ring ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
| **B — l'intelligence** | **B13** | **B13 : 183/183, F1 0,7902, 238/239** ; le produit installable (roue, quickstart) ; le tagger 95,75 % ; D1–E2 ; le natif (le banc, la numpy) | **le palier 1** (le corpus épinglé) ; B10.3 bloqué |
| **N — le natif** | **N2, N4** | N2 : **1 024 — 2,3911 / 2,3522** ; porte 2,7856 ; **[v2](../../reports/rapport-coordination-n2-v2.md)** ; **N4 tranché** — le banc (0,87, répétition 15), l'échelle (le vocabulaire seul), **la numpy (4/4)**, **le 2,40 non reproductible** ([alerte](../../reports/rapport-native-reproductibilite.md)) ; N5 gelé | **épingler le corpus** ([le plan](../../docs/pilotage/natif-plan.md)) ; la porte propre |
| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 0,9575 ; réel 452 0,9500 ; W2 402 0,9643, H50 0,8607 ; W3 défaut hors ligne ; X3 1 000 items 0,022 $ ; Y1 `auto` | **J4 — l'or de rôles** ; Panini (les 26 signatures) |
| **C1** **C2** **C3** **C4** **C5** **C6** **C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 3 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |


## Ce qui reste

**N** : le corpus du palier 1 (résumés, **3,69 Go**, épinglé) — le run à époques égales ; la porte propre (0,29) ; N4.
**A** : les clusters et les bandes d'A2.6 ; A3.4 (Colab), A5.4 (FPGA : P2 + RTL), A6.2. **R** : la
décision de routage du tagger (+9,47 mesuré) ; J4. **S** : migrer `/` vers la v7 (41 à re-juger).
**B** : B13 (gold neuronal) ; B10.3. **Panini** : 26 signatures V14, calibration 42/44. **L** : la
pragmatique, r353. **D** : la diversité — bloquée (Gutenberg 503, Wikisource).

## Les questions ouvertes

- **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
- **N2** : **< 2,5** ? → **oui par la fenêtre** : 2,4759 / 2,4373 au grand corpus (1 024, 30 k pas) ; la porte **propre** reste à 2,7856.
- **A5.4** : 4 cartes + ring 40G (17/11) ; **P1 tranché** : la dispersion GPU **29,37 G év/s** bat la projection FPGA (19,3) → le kernel GPU.
- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche ; la
  restitution v1 **ne monte pas** (0,1087) ; la v3 sépare les cinq rôles (**18/18**) mais le
  gold v2 reste à **20/46** ; J4 (or de rôles) suit.

## La carte

- Méthode : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · plan : [roadmap](roadmap.md) ·
  [semaine 2](semaine-2.md) · [backlog](backlog/index.md) · preuves : [reports/](../../reports/) ·
  [journal/](../../journal/).

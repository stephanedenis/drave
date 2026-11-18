# En ce moment

**Mis à jour : 2026-11-17, 20 h 20 HNE (les plans par fenêtre tarifaire)**

> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
- **Prochaine action** : **suivi docs**, puis la **passe**.
- **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 11** : serveurs locaux arrêtés ; professeurs par l'**API DeepSeek** ; GPU à Drave.

### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise *(en pause)*

- **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
- **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
- **Plan** : état.
- **Ambition** : reprise.
- **Stratégie** : flux.
- **Objectif final** : zéro.
- **Ce qu'elle fait** : intégration ; passe **82, 80/2**.
- **Ce que font les autres** : **N2**, **S**, **Pensée**.
- **Prochaine action** : reprise par le hub `1e7ef596` ; l'état du 04/11 est la source.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/).

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures *(en pause)*

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : validation.
- **Ambition** : rôles.
- **Stratégie** : contrôles.
- **Objectif final** : gold 60.
- **Fait** : types **61/61**, rôles **144/144** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
- **Ce qu'elle fait** : **session close** ; **`/paragraphes`** v7, **`/`** ancien arbre (369) ; **`s/v7`** à fusionner.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**.
- **Prochaine action** : **migration `/` v7** (106/41) ; référents ; rétro-traduction.
- **Bloquants** : aucun ; 8765 pris (lancer 9000) ; migration = choix.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)*

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13 · **Stratégie** : v0 · **Ambition** : tracé · **Objectif final** : moteur v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.
- **Ce que font les autres** : N2.
- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**, v2 **20/46**) ; **U1** 4,0 → 0,82 s (α 1,08) ; **U2** roue 1 727 201 o, sans gold → 4 ; **U3** profils 20/20, `und` ; **V1** `--strict` 0,8625/0,8891 ; **V2** exemples **27/27** ; **V3** la clôture — **86/82/4** → **84/2**, tag `exploitable-2026-11-16` ([bilan 2](../../reports/rapport-bilan-exploitable-2.md)).
- **Prochaine action** : **J4** ; T132/T133 ; la décision `auto`.
- **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*

- **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
- **Rôle** : **N2** — la production et la capacité.
- **Plan** : fenêtre.
- **Ambition** : la longueur et la capacité.
- **Stratégie** : budgets contrôlés, mêmes bancs.
- **Objectif final** : la production qui tient.
- **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte ; `kd2` et `rope2048` **arrêtés** ; **paire propre** : **3,1500** → **3,1119**
- **Ce que font les autres** : **hub**, **S**, **Pensée**.
- **Prochaine action** : la **porte propre (0,29)** ; le **2 048** est fini.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles ; **19/19 verdicts `389b99f`** ; [v2](../../reports/rapport-coordination-s-v2.md).
- **N2 — en pause** : commande **`eval_longueurs.py --rope --val <dir>`** (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → 4) ; **U3** profils 20/20 ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [roue](../../reports/rapport-roue.md), [profils](../../reports/rapport-profils.md).
- **L — le bloc langue** : contrat ; frontière script 1,0 / langue 0,137/0,9687 ; fusion réparée **0,9309/0,8226/0,8784/0,9954**.
- **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ; [W2](../../reports/rapport-tagger-h50.md), [W3](../../reports/rapport-tagger-defaut.md).
- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues, **V14 3/21** ; B2 **négatif** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [B2](../../reports/rapport-atomes-prediction.md), [familles](../../reports/rapport-retrieval-familles.md).
- **Panini B1** : **60 paires** ; **27/60**, calibration **42/44** ; [W4](../../reports/rapport-panini-manifeste.md), [B1](../../reports/rapport-protocole-date.md).
- **Panini J12.1–J12.2 + B3** : CIC **42/42** ; B3 **42/42** types de Bruijn ; [§334](../../reports/rapport-panini-334.md), [CIC](../../reports/rapport-cic-verificateur.md), [v2](../../reports/rapport-cic-v2.md).
- **Bilans** : F1 **0,7902**, chantier **20/21** ; [semaine](../../reports/rapport-semaine.md), [bilan](../../reports/rapport-bilan-chantier.md), [clôture](../../reports/rapport-cloture-chantier.md).
- **N3.7–N3.10 — variantes, routes, moteurs, coût** (17/11) : `impl`+`contrat` (substitution **4,768e-07**) ; routes exécutées (0 = `flou` **bit-exact**, 10⁹ = `defaut` **bit-exact**) ; Rust ↔ numpy **2,980e-07** (defaut, bloque, court) ; `court` **0,694×** le temps ; sur 5 modèles : bloque **±0,04 %**, flou **+1,1…+7,0 %**, court **−12…+4,6 %** de PPL ; numpy refuse flou et les routes ; [variantes](../../reports/rapport-n3-variante.md), [routes](../../reports/rapport-n3-route.md), [moteurs](../../reports/rapport-n3-moteurs.md), [court](../../reports/rapport-n3-court.md), [profils](../../reports/rapport-profils-modele.md).

## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **90** (dont `porte-n3-variante`, `-route`, `-moteurs`, `-court` le 17/11) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **789** / **880** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **128** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **17/11 20 h 42 → 22 h 39** : **90** portes, **87/3** ; rouges `indice` (862 s) et `melange` (106 s) **structurelles**, `sessions` **circonstance** (heartbeat `e181ce02` à 1 896 min) → **aucune rouge nouvelle** ; cumul **6 981 s** | `work/portes/roue-1117-2042/registre.txt` |

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

**V3 — la clôture** : **T1–T6**, **U1–U3**, **V1–V2** ; **86/82/4** → **84/2** après vérification ciblée ; tag `exploitable-2026-11-16` sur `ae3c24f2` ; [bilan 2](../../reports/rapport-bilan-exploitable-2.md), [U1](../../reports/rapport-performance-fix.md), [U2](../../reports/rapport-roue.md), [U3](../../reports/rapport-profils.md), [V1](../../reports/rapport-evaluer-strict.md), [V2](../../reports/rapport-exemples-v2.md), [Z1](../../reports/rapport-ci.md).

**Pensée** — `g017`, T132/T133, gold de pensée ; **J4 — l'or de rôles** (seconds cadres). **Le gold de S** (61 phrases/144 rôles) n'est pas un or humain indépendant ; **S** — page `/` : décision et recette (106/41), **12/28** référents faux.

**Panini** — **26 signatures V14** manquantes, calibration **42/44**, rejeu **27/60** : le test attend ; **R0.7** — `--tagger auto` prototype livré (**opt-in**, défaut hors ligne inchangé), **décision humaine** ; **N2** — porte (0,2856/0,3566) ; **A** — A6.2, A8.3b2.

## Les questions ouvertes

- **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
- **N2** : **< 2,5** ? → **oui par la fenêtre** : 2,4759 / 2,4373 au grand corpus (1 024, 30 k pas) ; la porte **propre** reste à 2,7856.
- **A5.4** : 4 cartes + ring 40G disponibles (17/11) ; **P1 tranché** : la dispersion GPU fait **29,37 G év/s** > **19,3 G** projetés → le débit ne justifie pas le ring ; restent l'**énergie**, le **déterminisme**, la **démo** et **P2** (ring 4,8 Go/s) ; la grille de la banque : **6×** à 512 sorties, neutre à 4 096, **nuisible** à 65 536 ; [fiche](backlog/A5.4-fpga.md), [P1](../../reports/rapport-gpu-scatter.md), [grille](../../reports/rapport-gpu-scatter-grille.md).
- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche ; la
  **restitution v1** : le miroir strict **ne monte pas** (0,1087), la forme canonique vaut
  **46/46** ; la **v3** sépare les cinq rôles (**18/18** au gold S) mais le gold v2
  reste à **20/46** ; J4 (or de rôles) suit.

## La carte

- Méthode : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · plan : [roadmap](roadmap.md) ·
  [semaine 2](semaine-2.md) · [backlog](backlog/index.md) · preuves : [reports/](../../reports/) ·
  [journal/](../../journal/).

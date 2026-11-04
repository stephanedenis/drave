# En ce moment

**Mis à jour : 2026-11-04, 12 h 05 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).
>
> **Reboot du 03/11 19 h 33** : la nuit a été coupée net — `kd2` à **8 250/30 000** pas et
> `rope2048` à **3 350/20 000**, **sans checkpoint** ; les quatre sessions sont **en pause**.
> Reprise par le hub le **04/11 08 h** : analyse des sessions, tâches courtes, état, intégration ;
> runbook [`plan-travail.md`](plan-travail.md) § 9, plan de la nuit § 11.

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — analyse des quatre sessions interrompues, tâches courtes, état.
- **Fait** : index réparé (`git read-tree HEAD`) ; N2/S/Pensée triés ; **8 verdicts S** committés ; banque **84/67** ; **fix FIFO** (+3 tests) ; état au 04/11.
- **Prochaine action** : commit d'intégration, puis **passe de portes** ; les runs longs N2 ensuite.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 11** : serveurs locaux arrêtés ; professeurs par l'**API DeepSeek** ; GPU à Drave.
>
> **Bilan de 08 h du 04/11** : nuit **coupée à 19 h 33** ; quatre sessions en pause, WIP triés ;
> **runs N2 relancés à 09 h 30** (`kd2` gpu0, `rope2048` gpu1) ; **passe complète après** (§ 11). [journal du 03/11](../../journal/2026-11-03/README.md).

### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise *(en pause)*

- **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
- **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
- **Plan** : audit, état, runbook ; nuit.
- **Ambition** : un état reprenable.
- **Stratégie** : committer par flux.
- **Objectif final** : sédimentation à zéro.
- **Ce qu'elle fait** : intégration ; **passe 11 h 30 — 82, 80/2** ; plan de nuit.
- **Ce que font les autres** : **N2**, **S**, **Pensée**.
- **Prochaine action** : **rouvrir le hub** (session `1e7ef596`) ; il tient l'état, la passe et
  l'intégration ; les runs longs N2 repartent ensuite.
- **Bloquants** : aucun ; GPU à N2 (les deux), claims dans le registre.
- **Journal** : [la session](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/).

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export *(en pause)*

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : analyseur, export, arbre, validation.
- **Ambition** : nommer le rôle et la frontière GN.
- **Stratégie** : une règle = trois contrôles.
- **Objectif final** : gold 60, corpus 60.
- **Fait** : types **60/60**, rôles **142/142** ; **corpus réel** 8,5 %/65,5 % ; **arbre** 99 à ≥3, **référents** 294/371, **traduction** 14/14 ; **page `/paragraphes`**, **banque 9 paragraphes** ; **55 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md).
- **Ce qu'elle fait** : page **`/paragraphes`**, corpus **60**, banque **84/67**.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**.
- **Prochaine action** : **poursuivre la validation sur `/paragraphes`** (a001–a003 faits, 8
  verdicts committés), puis la rétro-traduction API ; le nom après un adjectif hors lexique.
- **Bloquants** : aucun ; la page **`/paragraphes`** porte l'arbre/les référents ; la banque
  partielle reste archivée.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(en pause)*

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN plurielle, arbre d'états, moteur N3 ; R4.4 ; heuristique ; bloc linguistique.
- **Plan** : B13, R4.4, bloc linguistique.
- **Ambition** : un runtime cognitif tracé.
- **Stratégie** : v0 petit et mesuré.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **140/140** (T132/T133 2/5), gold **432** (réel **0,9065/0,4598/0,5633/0,9954** → true) ;
  **DRVM/native 114/114 + 5/5** ; **sto 5/5** ; **fenêtre non discriminante** (oracle 228, aveugle 215) ;
  **pragmatique 0,6375** ; fiches [B13](../../reports/rapport-b13-porte-140.md), [fenêtre](../../reports/rapport-pensee-porte-fenetre.md).
- **Ce qu'elle fait** : gold neuronal rejoué sur l'**API** (mêmes verdicts, latence 5,5 / 2,9 s au lieu de 6,4 / 101,6 s) ; [fiche](../../reports/rapport-pensee-gold-api.md).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Prochaine action** : **gold 432 réel (0,9954)** ; **DRVM/native 114/114+5/5** ; la suite :
  **T132/T133**, gold 200+ ; **porte B13** attend S ; le **fix FIFO** est testé, le qualifier
  fenêtre BFS 500 attend une version API (le serveur local est interdit).
- **Bloquants** : aucun pour POS/syntagmes/cascade/DRVM/minute/mobile ; la **pragmatique neuronale** ne qualifie pas ; la **porte B13** attend S ; reste **gold 200+** ; les expériences **7B locales** sont **interdites** (règle 11) — la professeure passe par l'**API DeepSeek** ou le **DRVM natif**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*

- **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
- **Rôle** : **N2** — le run long de production et la capacité sur le corpus propre.
- **Plan** : 1 024, capacité.
- **Ambition** : la longueur et la capacité.
- **Stratégie** : budgets contrôlés, mêmes bancs.
- **Objectif final** : la production qui tient au long.
- **Ce qu'elle fait** : **60 000 pas à 1 024** ; capacité propre ; distillation native **+0,10** ; **runs relancés à 09 h 30** ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [production](../../reports/rapport-n2-production-fenetre.md), [porte](../../reports/rapport-n2-porte-propre.md).
- **Ce que font les autres** : **hub**, **S**, **Pensée**.
- **Prochaine action** : **surveiller les runs relancés à 09 h 30** — `kd2` (gpu0) et `rope2048`
  (gpu1) ; puis mesurer et committer ; ensuite la **porte propre (0,29)**.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).


## Ce qui est en cours

- **S — les structures** : analyseur **60/60**, **142/142** rôles ; corpus **60** ; banque **84/67**, **8 verdicts de référents**, **55/55 tests** ; référents **294/371**, page **`/paragraphes`**.
- **N2 — en pause** : **1 024** = recette de production (2,48–2,91 ; sous 2,5 au grand corpus) ; **runs relancés à 09 h 30** (la nuit était coupée : `kd2` 8 250/30 000, `rope2048` 3 350/20 000) ; **distillé : −0,10** ; copie 0,0078.
- **Pensée — B13 (en pause)** : **140/140**, gold **432 réel true** (0,9954), **DRVM/native 114/114 + 5/5**, T132/T133 2/5 ; **fix FIFO du store** (+3 tests) ; qualifier fenêtre BFS 500 écarté.
- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (= le max)**.

## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **82** (passe du **03/11 11 h 30** : **82, 80/2**) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **602** / **687** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **120** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **03/11 11 h 30** (82, **80/2**, les 2 connues) ; **04/11 08 h 40 arrêtée** ; complète après les runs | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 140/140, gold 432, 116 liens** | **B13 : gold réel 432 (0,9065/0,4598/0,5633/0,9954) ; porte 140/140 ; sto 5/5** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N3, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856, **capacité saturée** (2,8662 à 34,3 M) ; N4 0/4 ; N5 gelé | **la fenêtre** (N2.ac + RoPE 512 : 2,9096 à 512, 2,7607 à 2 000) |
| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **loi de la fenêtre mesurée** (256 → 1 024) ; **2 048** en cours, puis un professeur long à distiller |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

**C1** · **C2** · **C3** · **C4** · **C5** · **C6** · **C7** — hors graphe.

## Ce qui reste

**N2** — relancer `kd2`/`rope2048` ; **R1** — R1.2-1024 ; **Pensée** — gold 200+ ; **S** —
poursuivre la validation ; **N4** — consigne ; **B10.3** — `z` ; **B13** — 140/140 ; **R0.7** —
tagger ; **D** — OCR clos (8 `.PDF`).



## Les questions ouvertes

- **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
- **N2** : **< 2,5** ? → **oui par la fenêtre** : 2,4759 / 2,4373 au grand corpus (1 024, 30 k pas) ; la porte **propre** reste à 2,7856.
- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non mesuré** (run interrompu).
- **R1 (nuit)** : 2 048 à 20 000 pas ? → **non mesuré** (run interrompu).
- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche.

## La carte

- Méthode : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · plan : [roadmap](roadmap.md) ·
  [backlog](backlog/index.md) · preuves : [reports/](../../reports/) · [journal/](../../journal/).

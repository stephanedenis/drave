# En ce moment

**Mis à jour : 2026-11-04, 19 h 42 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).
>
> **Reboot du 03/11 19 h 33** : la nuit a été coupée (`kd2` **8 250/30 000**, `rope2048`
> **3 350/20 000**, sans checkpoint) ; les quatre sessions ont été mises en pause. **Reprise du
> 04/11** : hub `1e7ef596` (08 h 50), N2 09 h 41, S 09 h 46, L/B13 10 h 14 ; **N3** clos en
> session courte (11 h 30–11 h 38). Runbook [`plan-travail.md`](plan-travail.md) § 9 et § 12.

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
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
> **Bilan de 15 h** : reprises à 09 h ; **runs N2 arrêtés** (`kd2`, `rope2048` à 6 400/20 000) ; **perte α=0,9 0,8385 (−0,176), PPL 3,1119 (−0,06)** ;
> **N3 clos** ; la **passe complète attend la fin des runs** (§ 11). [journal du 04/11](../../journal/2026-11-04/README.md).

### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise *(en pause)*

- **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
- **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
- **Plan** : audit, état, runbook ; nuit.
- **Ambition** : un état reprenable.
- **Stratégie** : committer par flux.
- **Objectif final** : sédimentation à zéro.
- **Ce qu'elle fait** : intégration ; passe **11 h 30 — 82, 80/2** ; plan de nuit.
- **Ce que font les autres** : **N2**, **S**, **Pensée**.
- **Prochaine action** : reprise par le hub `1e7ef596` ; l'état du 04/11 est la source.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/).

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures *(en pause)*

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : analyseur, export, arbre, validation.
- **Ambition** : nommer le rôle et la frontière GN.
- **Stratégie** : une règle = trois contrôles.
- **Objectif final** : gold 60, corpus 60.
- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
- **Ce qu'elle fait** : **session close** ; page **`/paragraphes`** (validation 3/9), branche **`s/v7`** à fusionner.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**.
- **Prochaine action** : **reprise** : poursuivre la validation sur `/paragraphes` (a001–a003 faits, 8 restants), puis la rétro-traduction API et les 71 langues.
- **Bloquants** : aucun ; la page **`/paragraphes`** porte l'arbre/les référents.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)*

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13, bloc linguistique.
- **Ambition** : un runtime cognitif tracé.
- **Stratégie** : v0 mesuré.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **165/165** ; **candidats verbes : top-k 0,4686, tête 0,7655** ; attachement par proximité (exact 0,0544) ; rôles 301/322 ; passifs hors du chemin S ; fiches [passifs](../../reports/rapport-pensee-passifs.md), [cible par proximité](../../reports/rapport-pensee-cible-proximite.md), [candidats verbes](../../reports/rapport-pensee-candidats-verbes.md).
- **Ce qu'elle fait** : l'API rejoue le gold (mêmes verdicts).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Prochaine action** : les **candidats verbes**, puis le **générateur S**.
- **Bloquants** : 7B locales interdites (règle 11) ; reste **gold 200+**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(actif)*

- **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
- **Rôle** : **N2** — la production et la capacité.
- **Plan** : 1 024, capacité.
- **Ambition** : la longueur et la capacité.
- **Stratégie** : budgets contrôlés, mêmes bancs.
- **Objectif final** : la production qui tient.
- **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondération) ; `kd2` et `rope2048` **arrêtés** (code biaisé, trop lents) ; **paire propre de production** finie : α = 0 → **3,1500**, α = 0,9 → **3,1119** (−0,06 ; −0,19 anglais) ; **repondération 4× : −0,05** ; **2 048 relancé** (2×10 000 pas) ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [production](../../reports/rapport-n2-production-fenetre.md), [erratum](../../reports/rapport-n2-distillation-native.md), [porte](../../reports/rapport-n2-porte-propre.md).
- **Ce que font les autres** : **hub**, **S**, **Pensée**.
- **Prochaine action** : le **2 048** (fin ~21 h) ; ensuite la **porte propre (0,29)**.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
- **N2 — actif** : **1 024** = recette de production (2,48–2,91 ; sous 2,5 au grand corpus) ; **kd2** arrêté, **2 048 : 1re moitié finie** (10 000 pas, 10 224 s, drvm `c50beff6`), 2e en cours ; **perte d'entraînement** : α = 0 **1,014**, α = 0,9 **0,8385** (−0,176) ; **PPL de validation** : α = 0 **3,1500**, α = 0,9 **3,1119** (−0,06 ; −0,19 anglais) ; la distillation **paie** sur le PPL ; **repondération 4× : −0,05**.
- **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
- **Pensée — B13 (actif)** : **165/165**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; la fusion garde l'heuristique.
- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.

## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **83** (82 à la passe du **03/11 11 h 30** ; **+1** le 04/11 : `porte-n3-inventaire`) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **627** / **720** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **120** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **03/11 11 h 30** (82, **80/2**, les 2 connues) ; **04/11 08 h 40 arrêtée** ; N3 **17/17** à 11 h 32 ; complète après les runs | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 165/165, gold 432, 116 liens** | **B13 : T132/T133, gold 200+** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre (0,29)** ; **N4** |
| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **1 024 octets entraînés** ; **2 048** arrêté à 6 400/20 000 ; la restitution |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 3 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

**C1** · **C2** · **C3** · **C4** · **C5** · **C6** · **C7** — hors graphe.

## Ce qui reste

**N2** — finir `kd2`/`rope2048`, puis la **porte propre (0,29)** ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+ ; **S** — poursuivre la validation ; **N4** — consigne ; **B10.3** — `z` ; **B13** — 165/165 ; **R0.7** — tagger ; **D** — **restauré** : le corpus à **62 documents** (Choquette + Assurance ; DOC1/DOC2, quasi-doublons, écartés) est en place (`data/corpus_ocr_cegep` : train 4 440 987, val 12 536, test 10 524 ; 8 Ko 0, 500 o 0) ; [fiche](../../reports/rapport-ocr-cegep-64.md).

## Les questions ouvertes

- **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
- **N2** : **< 2,5** ? → **oui par la fenêtre** : 2,4759 / 2,4373 au grand corpus (1 024, 30 k pas) ; la porte **propre** reste à 2,7856.
- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.
- **R1 (nuit)** : 2 048 à 20 000 pas ? → `rope2048` en cours, réponse attendue.
- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche.

## La carte

- Méthode : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · plan : [roadmap](roadmap.md) ·
  [backlog](backlog/index.md) · preuves : [reports/](../../reports/) · [journal/](../../journal/).

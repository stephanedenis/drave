# En ce moment

**Mis à jour : 2026-11-04, 12 h 37 HNE (heure locale, EST).**

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
> **Bilan de 11 h** : reprises à 09 h ; **runs N2 actifs** (`kd2` gpu0, `rope2048` gpu1) ;
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

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures *(actif)*

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : analyseur, export, arbre, validation.
- **Ambition** : nommer le rôle et la frontière GN.
- **Stratégie** : une règle = trois contrôles.
- **Objectif final** : gold 60, corpus 60.
- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
- **Ce qu'elle fait** : page **`/paragraphes`**, corpus **60**, banque **84/67**.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**.
- **Prochaine action** : **poursuivre la validation sur `/paragraphes`** (a001–a003 faits), puis la rétro-traduction API ; le nom après un adjectif hors lexique.
- **Bloquants** : aucun ; la page **`/paragraphes`** porte l'arbre/les référents.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)*

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN plurielle, arbre d'états, moteur N3 ; R4.4 ; heuristique ; bloc linguistique.
- **Plan** : B13, R4.4, bloc linguistique.
- **Ambition** : un runtime cognitif tracé.
- **Stratégie** : v0 petit et mesuré.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **148/148** (troisième passe : variance **nulle**, run 3 = run 2 — POS **0,9389**, syntagmes **0,8241**, tête **0,8797**, refus **0** ; le `parallele` passe de **0,9326** à **0,9389** avec la clé ; seuil du parallèle ; défaut conditionnel ; run2 ; élision POS **0,7455**) ; **quatre modes 0,9309/0,8226/0,8784** ; **fusion : la confiance (0,7424) bat le niveau (0,3432)** ; gold **432** (réel **0,9065/0,4598/0,5633/0,9954** → true) ; **DRVM/native 114/114 + 5/5** ; **sto 5/5** ; fenêtre **non discriminante** ; pragmatique **0,6375** ; fiches [élision](../../reports/rapport-pensee-elision.md), [quatre modes](../../reports/rapport-pensee-quatre-modes-432.md), [défaut](../../reports/rapport-pensee-defaut-niveau.md), [run2](../../reports/rapport-pensee-quatre-modes-run2.md), [défaut conditionnel](../../reports/rapport-pensee-defaut-conditionnel.md), [seuil parallèle](../../reports/rapport-pensee-seuil-parallele.md), [troisième passe](../../reports/rapport-pensee-troisieme-passe.md), [B13](../../reports/rapport-b13-porte-140.md).
- **Ce qu'elle fait** : gold neuronal rejoué sur l'**API** (mêmes verdicts, latence /35).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Prochaine action** : **T132/T133**, **gold 200+** ; le qualifier fenêtre attend une version API (serveur local interdit).
- **Bloquants** : la **pragmatique neuronale** ne qualifie pas ; les **7B locales** sont **interdites** (règle 11) ; reste **gold 200+**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(actif)*

- **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
- **Rôle** : **N2** — le run long de production et la capacité sur le corpus propre.
- **Plan** : 1 024, capacité.
- **Ambition** : la longueur et la capacité.
- **Stratégie** : budgets contrôlés, mêmes bancs.
- **Objectif final** : la production qui tient au long.
- **Ce qu'elle fait** : **60 000 pas à 1 024** ; capacité propre ; **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,030/−0,009/−0,004 ; le +0,14–0,18 était une repondération) ; **runs relancés à 09 h 30** : `kd2` **~19 400/30 000** (gpu0), `rope2048` **4 650/20 000** (gpu1) ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [production](../../reports/rapport-n2-production-fenetre.md), [erratum](../../reports/rapport-n2-distillation-native.md), [porte](../../reports/rapport-n2-porte-propre.md).
- **Ce que font les autres** : **hub**, **S**, **Pensée**.
- **Prochaine action** : **surveiller les runs** (fin estimée **~13 h 30** / **~19–20 h**), puis mesurer et committer ; la **paire propre de la distillation** (production, α = 0 / 0,9) est en cours ; ensuite la **porte propre (0,29)**.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
- **N2 — actif** : **1 024** = recette de production (2,48–2,91 ; sous 2,5 au grand corpus) ; **runs actifs** : `kd2` **~19 400** (gpu0), `rope2048` **4 650/20 000** (gpu1).
- **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
- **Pensée — B13 (actif)** : **148/148**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; fusion : la confiance bat le niveau.
- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.

## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **83** (82 à la passe du **03/11 11 h 30** ; **+1** le 04/11 : `porte-n3-inventaire`) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **611** / **698** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **120** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **03/11 11 h 30** (82, **80/2**, les 2 connues) ; **04/11 08 h 40 arrêtée** ; N3 **17/17** à 11 h 32 ; complète après les runs | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 148/148, gold 432, 116 liens** | **B13 : T132/T133, gold 200+** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre (0,29)** ; **N4** |
| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **1 024 octets entraînés** ; **2 048** (`rope2048`) ; la restitution |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 3 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

**C1** · **C2** · **C3** · **C4** · **C5** · **C6** · **C7** — hors graphe.

## Ce qui reste

**N2** — finir `kd2`/`rope2048`, puis la **porte propre (0,29)** ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+ ; **S** — poursuivre la validation ; **N4** — consigne ; **B10.3** — `z` ; **B13** — 148/148 ; **R0.7** — tagger ; **D** — OCR clos (8 `.PDF`).

## Les questions ouvertes

- **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
- **N2** : **< 2,5** ? → **oui par la fenêtre** : 2,4759 / 2,4373 au grand corpus (1 024, 30 k pas) ; la porte **propre** reste à 2,7856.
- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → runs relancés, réponse attendue.
- **R1 (nuit)** : 2 048 à 20 000 pas ? → `rope2048` en cours, réponse attendue.
- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche.

## La carte

- Méthode : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · plan : [roadmap](roadmap.md) ·
  [backlog](backlog/index.md) · preuves : [reports/](../../reports/) · [journal/](../../journal/).

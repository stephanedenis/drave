# En ce moment

**Mis à jour : 2026-11-14, 01 h 10 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

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

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif ; heartbeat à rafraîchir)*

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13, bloc linguistique.
- **Stratégie** : v0 mesuré.
- **Ambition** : un runtime cognitif tracé.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** ([fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v0** (46/46, miroir 0,1087) ; **contrat v1**, **`drave` v0**.
- **Ce qu'elle fait** : l'API rejoue le gold (mêmes verdicts).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Prochaine action** : **trancher la convention d'adverbe (`g017`)** ; puis T132/T133, gold 200+.
- **Sous-agents** : 4 mandats, [plan-travail](plan-travail.md) § 9.
- **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*

- **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
- **Rôle** : **N2** — la production et la capacité.
- **Plan** : fenêtre.
- **Ambition** : la longueur et la capacité.
- **Stratégie** : budgets contrôlés, mêmes bancs.
- **Objectif final** : la production qui tient.
- **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondération) ; `kd2` et `rope2048` **arrêtés** ; **paire propre** : **3,1500** → **3,1119** (−0,06 ; −0,19 anglais) ; **repondération : −0,05** ; **2 048** ne bat pas 1 024 ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [production](../../reports/rapport-n2-production-fenetre.md), [erratum](../../reports/rapport-n2-distillation-native.md), [porte](../../reports/rapport-n2-porte-propre.md).
- **Ce que font les autres** : **hub**, **S**, **Pensée**.
- **Prochaine action** : la **porte propre (0,29)** ; le **2 048** est fini.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
- **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
- **Pensée — B13 (actif)** : **183/183**, gold 432, pragmatique 130/432 ; **`r035`** (238/238) ; **convention des GV** (0,7902, 0 perte) ; **`s065` réglé** (238/238, 0 span ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée** (adverbe final hors SUB, test −0,0028 ; g017 : convention à trancher) ; **schéma v2** (26 cas, 0 échec ; v1 lue) ; **restitution v0** (46/46, miroir 0,1087) ; [restitution](../../reports/rapport-restitution-v0.md), [g017](../../reports/rapport-g017.md).
- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
- **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significative ; **J3.2** : les deux faces diffèrent — `lang_distance` couvre **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, la famille vit dans **2-3 paires**, **V14 : 3/21** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-faces.md).
- **J5.1** : rapport de semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets**) ; [rapport](../../reports/rapport-semaine.md) + JSON.
- **Coordination J4** : N2 **2,9726/2,7856** ; S **7 acceptés / 4 exclus** ; R **0,9475 (+8,49)** ; A6.2 **libre** (PPL 37,2013), A8.3b2 hors graphe ; [N2](../../reports/rapport-coordination-n2.md), [S](../../reports/rapport-coordination-s.md), [R](../../reports/rapport-coordination-r.md), [A](../../reports/rapport-coordination-a.md).

## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **84** (dont `porte-produit` le 07/11) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **720** / **814** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **03/11 11 h 30** (82, **80/2**) ; N3 **17/17** à 11 h 32 | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 et convention des GV (0,7902, 238/238), s065 réglé (238/239), J6.1 rejeté (convention d'adverbe à trancher), schéma v2 (v1 lue), restitution v0 (46/46, 0,1087)** | **trancher la convention d'adverbe (`g017`)** ; puis T132/T133, gold 200+ ; **B10.3 bloquée** |
| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 (manque **0,2856** val / **0,3566** test) ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |
| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9475 (+8,49), intégrer** ; R2/R3 attendent N5/N4 | **route API derrière drapeau** ; **split réel tenu à l'écart** |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 3 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

**C1** · **C2** · **C3** · **C4** · **C5** · **C6** · **C7** — hors graphe.

## Ce qui reste

**N2** — porte (0,2856 val / 0,3566 test) ; **Pensée** — convention d'adverbe `g017`, T132/T133, gold 200+ ; **J3.2** — **V14 des 21 langues** ; **S** — 11 verdicts + pointeur ; **R0.7** — **0,9475**, intégrer, split réel ; **A** — A6.2, A8.3b2 ; **J5.2** — passe, revue, tag.

## Les questions ouvertes

- **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
- **N2** : **< 2,5** ? → **oui par la fenêtre** : 2,4759 / 2,4373 au grand corpus (1 024, 30 k pas) ; la porte **propre** reste à 2,7856.
- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.
- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).
- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche ; la
  **restitution** v0 est un codec (miroir **0,1087**) ; la v0.1 replace la ponctuation, le gold
  reste à faire.

## La carte

- Méthode : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · plan : [roadmap](roadmap.md) ·
  [backlog](backlog/index.md) · preuves : [reports/](../../reports/) · [journal/](../../journal/).

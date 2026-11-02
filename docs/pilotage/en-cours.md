# En ce moment

**Mis à jour : 2026-11-02, 16 h 49 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active**. Méthode :
> [`methode/`](../methode/) ; résultats : [`reports/`](../../reports/) ; histoire :
> [`journal/`](../../journal/) ; plan : [`roadmap.md`](roadmap.md).
>
> **Reprise après le reboot du 02/11 15 h 06** : les **quatre** sessions ont rouvert entre 16 h 14
> et 16 h 21 — N2 `0733c5bb`, S `29ad180d`, Pensée `e181ce02`, D/R/A `fe3c05f0` ; les GPU sont
> sains ; reprise par `dsh --profile dsh-tui --resume <id>` ; runbook dans
> [`plan-travail.md`](plan-travail.md) § 9.

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.

### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise

- **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
- **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
- **Plan** : 1–7) ~~audit, commits, état, mandats, porte, INDEX, runbook~~ ; 8) **intégration** ;
  9) **passe de portes** (GPU 1).
- **Ambition** : un état reprenable, des mandats qui disent la vérité.
- **Stratégie** : committer par flux (`git add` explicite), nommer ce qui reste.
- **Objectif final** : sédimentation à zéro, quatre mandats explicites, runbook.
- **Ce qu'elle fait** : intégration ; **porte stricte réparée** (imbrication = avertissement) ;
  sous-passe documentaire **7/8** (bloc-maths : bruit de charge).
- **Ce que font les autres** : **N2**, **S**, **Pensée**, **D/R/A** (sessions ouvertes).
- **Prochaine action** : **passe complète reportée** — les **deux GPU** sont à N2, charge **24** ;
  la tenir machine libre.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2, le natif : 200 000 pas et la fenêtre

- **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
- **Rôle** : **N2 — le natif, GPU** : le compute sur le mélange 1 Go, puis la fenêtre native
  (R1.1/R1.2).
- **Plan** : 1) ~~plan et réservations~~ ; 2) **200 000 pas** (en cours) ; 3) **banc R1.1/R1.2** ;
  4) **mesure** (cinq PPL, courbe) ; 5) **fiche, JSON, état, commit**.
- **Ambition** : que N réponde « plus de pas, quelle position, quelle fenêtre ».
- **Stratégie** : recette constante (34,3 M, canal, positions aléatoires, graine 1) ; banc sur le GPU 1.
- **Objectif final** : trancher **< 2,5 sans perdre le français**, puis **R1.1/R1.2**.
- **Ce qu'elle fait** : mandat ouvert à **16 h 17** ; **200 k pas** sur `data/wiki_mix/propre`, GPU 0.
- **Ce que font les autres** : **hub**, **S**, **Pensée**, **D/R/A**.
- **Prochaine action** : la fin des 200 k pas, puis les **cinq PPL** et la **courbe**.
- **Bloquants** : aucun ; **GPU 0** à N2, **GPU 1** aux portes.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : 1–4) ~~plan, analyseur (gold 39), export, tests 40~~ ; 5–6) ~~fiche, pointeur, état~~.
- **Ambition** : nommer le rôle, couper la subordonnée ; un corpus qui se rejoue.
- **Stratégie** : une règle = une phrase du gold, trois contrôles.
- **Objectif final** : gold **39**, corpus **39**, manifeste SHA-256.
- **Fait** : types **38/39**, rôles **99/100**, compléments **45/45** ; contrôles **64/100**,
  **66/100**, **0,099** ; échec nommé **h033** ; **40 tests** ;
  [`fiche`](../../reports/rapport-s-analyseur-roles.md).
- **Ce qu'elle fait** : sous-module **`647205a`** et pointeur **`13f4e131`** committés ; corpus
  **39** lignes (SHA `973c70a4…`) ; mode `banque` à **0** verdict humain.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**, **D/R/A**.
- **Prochaine action** : validation humaine de la banque, puis frontière du GN (h033).
- **Bloquants** : aucun pour l'analyseur et l'export ; **banque validée à 0** verdict.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN plurielle, arbre d'états, moteur N3 ; R4.4 ; heuristique ; bloc linguistique.
- **Plan** : 1–6) ~~moteur B13~~ ; 7) ~~R4.4~~ ; 8) ~~heuristique~~ ; 9) ~~bloc~~ ; 10) ~~coréférence~~.
- **Ambition** : un **runtime cognitif** où penser est une recherche tracée sur des états pluriels.
- **Stratégie** : v0 petit et mesuré, GPU de N2 intacts.
- **Objectif final** : un **moteur de pensée v0** exécutable, documenté, mesuré, committé.
- **Fait** : B13 **140/140**, gold **432**, coréférence **116 liens** ; **R0.7** — 9 niveaux,
  **398 langues à 0,9687** ; **R4.4** — trois limites nommées.
- **Ce qu'elle fait** : le cycle **140/140** est committé ; reprise à **16 h 16**.
- **Ce que font les autres** : **N2**, **S**, **D/R/A**, **hub**.
- **Prochaine action** : **gold neuronal** (modèle local) ; **DRVM/native** bloqué.
- **Bloquants** : **neuronal réel bloqué** (`llama-cli`, taggers, poids) ; le mock reste un contrat.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `fe3c05f0-834b-44f2-8739-501865d652c1` — D/R/A : les données, le lecteur, le moteur

- **Id** : `fe3c05f0-834b-44f2-8739-501865d652c1` — [`plan.md`](../../journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md).
- **Rôle** : **D/R/A** — texte intégral, PDF/OCR, prépa R1.1/R1.2, A2.6/A8.3.
- **Plan** : texte intégral, PDF, OCR, glossaire.
- **Ambition** : le français réel.
- **Stratégie** : dump, débaliseur, OCR page à page, glossaire au rendu.
- **Objectif final** : 10 corpus, ficés.
- **Ce qu'elle fait** : 10 corpus (**20,53 M**) ; PDF 1 927 ; OCR 20 livres + 10 notes
  CEGEP ; glossaire 355 ; [`ocr-cegep`](../../reports/rapport-ocr-cegep.md).
- **Ce que font les autres** : **N2**, **S**, **Pensée**, **hub**.
- **Prochaine action** : **OCR ~127 scans CEGEP** (cens en cours) ; clôture.
- **Bloquants** : aucun ; reprise à **16 h 21**.
- **Journal** : [le 02/11](../../journal/2026-11-02/README.md).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; **R0.4/R0.5 closes (négatifs)** ; R0.6 **12/20** au pilote, **7/7** à la porte.
- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 intérieur, ×62,7 tout ; [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../reports/rapport-typoglycemie.md).
- **Données** : **10 corpus** (**21,6 M art.**, **31,4 G car.**, **38,8 Go**, **0 fuite**) ; **OCR CEGEP** 10 notes, 1 596 p ; **glossaire** 355 entrées — [`inventaire`](../../reports/inventaire-donnees-entrainement.md), [`corpus-wikipedia`](../../reports/rapport-corpus-wikipedia.md).
- **S — le banc de structures** : **analyseur rôles/subordonnées 38/39 types, 99/100 rôles, 45/45 compléments**, gold **39**, **40 tests** ; corpus **39** structures (SHA `973c70a4…`) ; [`fiche`](../../reports/rapport-s-analyseur-roles.md) ; **banque validée à 0**.
- **N2** : **N2.ac** (mélange **1,02 Go**, 60 k pas) : **3,49** domaine, **6,03** littérature,
  **8,34** anglais, **9,05** wikitext2 — **le modèle de production** ; N4 **0/40** ; **session
  `0733c5bb`** ouverte le 02/11 16 h 17 — **200 k pas en cours** ; [`n2-canaux`](../../reports/rapport-n2-canal-34m.md),
  [`n2-1go`](../../reports/rapport-n2-corpus-1go.md).
- **Pensée — B13** : state store v0, AC-3/alpha-bêta, DRVF, banc, opérateurs, **140/140** ; gold
  **432 réels**, coréférence **116 liens** ; [`pensee-vrais-absents`](../../reports/rapport-pensee-vrais-absents.md),
  [`pensee-anaphore-bilan`](../../reports/rapport-pensee-anaphore-bilan.md).

## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **81** (76 vertes, 5 rouges au 02/11 06 h — 4 connues + greffe à 700 s, verte à 1200 s) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **551** / **639** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **119** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **02/11 06 h** (81 portes, 76/5) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 140/140, gold 432, 116 liens** | **B13 : DRVM/native (bloqué)** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N3, N4** | N2 : **N2.ac 1 Go — 3,49 domaine / 6,03 littérature** ; < 2,5 non atteinte ; N4 0/4 ; N5 gelé | **N2** : 200 k pas **en cours** (session `0733c5bb`), puis **R1.1/R1.2** ; **N4** |
| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** (398 langues) ; R1/R2/R3 attendent N5/N4 | **R1.1/R1.2** (contexte natif) |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

**C1** corpus · **C2** traduction · **C3** restitution · **C4** styles · **C5** domaines ·
**C6** documentation · **C7** pensée — hors graphe.

## Ce qui reste

**N2** — **200 k pas**, puis **R1.1/R1.2** ; **Pensée** — **DRVM/L** ; **S** — la **validation
humaine** de la banque et la frontière du GN (h033) ; **N4** — la consigne ; **B10.3** — le `z` ;
**R0.7** — gold/neuronal.

- **Vue d'ensemble** : huit chantiers et relations [`chantiers`](chantiers.md) ; plan multi-sessions [`plan-travail`](plan-travail.md) ; carte [`chantiers-vision.svg`](../schemas/chantiers-vision.svg).

## Les questions ouvertes

- **R1** : **1 000 octets** sans refaire 130–256 ? → **R1.1/R1.2** tranchent.
- **N2** : les **200 k pas** font-ils passer **< 2,5** sans perdre le français ? → N2 tranche.
- **N4** : une **consigne courte** tient-elle hors du vu ? → **N4** tranche (0/4 tenus).
- **B10.3** : chrF **> 39,6** ? → l'attention croisée tranche.
- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche.

## La carte

- **Méthode** : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · **plan** :
  [roadmap](roadmap.md) · [backlog](backlog/index.md) · [graphe](backlog/dependances.md) ·
  [carte](../theorie/carte.md) · **preuves** : [reports/](../../reports/) ·
  [journal/](../../journal/).

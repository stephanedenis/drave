# En ce moment

**Mis à jour : 2026-11-02, 19 h 43 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active**. Méthode :
> [`methode/`](../methode/) ; résultats : [`reports/`](../../reports/) ; histoire :
> [`journal/`](../../journal/) ; plan : [`roadmap.md`](roadmap.md).
>
> **Reprise après le reboot du 02/11 15 h 06** : les **quatre** sessions ont rouvert entre 16 h 14
> et 16 h 21 — N2 `0733c5bb`, S `29ad180d`, Pensée `e181ce02`, D/R/A `fe3c05f0` ; **D/R/A est
> close à 18 h 45** (OCR du fonds CEGEP) ; les GPU sont sains ; reprise par
> `dsh --profile dsh-tui --resume <id>` ; runbook dans
> [`plan-travail.md`](plan-travail.md) § 9.

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.

### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise

- **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
- **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
- **Plan** : 1–7) ~~audit, commits, état, mandats, porte, INDEX, runbook~~ ; 8–9) **intégration,
  portes** (GPU 1).
- **Ambition** : un état reprenable, des mandats qui disent la vérité.
- **Stratégie** : committer par flux (`git add` explicite), nommer ce qui reste.
- **Objectif final** : sédimentation à zéro, quatre mandats explicites, runbook.
- **Ce qu'elle fait** : intégration ; **porte stricte** ; sous-passe doc. **7/8** ; **passe de
  portes en cours** (`porte-bus`, 19 h 37).
- **Ce que font les autres** : **N2**, **S**, **Pensée** ; **D/R/A close**.
- **Prochaine action** : finir la **passe complète**, puis intégrer les lignes B13/N2/S.
- **Bloquants** : aucun ; la passe tient la machine (GPU libres).
- **Journal** : [la session](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2, le natif : 200 000 pas et la fenêtre

- **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
- **Rôle** : **N2 — le natif, GPU** : le compute sur le mélange 1 Go, puis la fenêtre native
  (R1.1/R1.2).
- **Plan** : 1) ~~plan~~ ; 2) ~~200 k pas~~ ; 3) ~~banc R1.1/R1.2~~ ; 4) **cinq PPL**, courbe,
  fiche + clôture.
- **Ambition** : N répond « plus de pas, quelle position, quelle fenêtre ».
- **Stratégie** : 34,3 M, canal, graine 1 ; banc GPU 1.
- **Objectif final** : **< 2,5 sans perdre le français**, puis **R1.1/R1.2**.
- **Ce qu'elle fait** : **200 k pas terminés** ; cinq PPL mesurées — val_fr **3,16**,
  littérature **5,61**, anglais **7,28**, wikitext2 **8,00** (< 2,5 non atteinte) ;
  **R1.1/R1.2 mesurées** ; [`n2-r11`](../../reports/rapport-n2-r11.md),
  [`n2-200k`](../../reports/rapport-n2-200k.md).
- **Ce que font les autres** : **hub**, **S**, **Pensée** ; **D/R/A close**.
- **Prochaine action** : la **courbe**, la **fiche + état + commit** du run de 200 k, puis la
  **clôture**.
- **Bloquants** : aucun ; **GPU libres**.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : 1–4) ~~plan, analyseur (gold 47), export, tests 43~~ ; 5–6) ~~fiche, pointeur, état~~.
- **Ambition** : nommer le rôle et la frontière GN.
- **Stratégie** : une règle = une phrase, trois contrôles.
- **Objectif final** : gold **47**, corpus **47**, manifeste SHA-256.
- **Fait** : types **47/47**, rôles **117/117** ; contrôles **80/117**, **82/117**, **0,109** ; h033 corrigé, **h046/h047** nommés ; **43 tests** ; [`fiche`](../../reports/rapport-s-analyseur-roles.md).
- **Ce qu'elle fait** : **`90e507b`** ; corpus **47** (SHA `f2a0d2fb…`) ; banque **0**.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**, **D/R/A**.
- **Prochaine action** : homographes/lexique, puis validation humaine de la banque.
- **Bloquants** : aucun ; **banque à 0** verdict.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN plurielle, arbre d'états, moteur N3 ; R4.4 ; heuristique ; bloc linguistique.
- **Plan** : 1–6) ~~moteur B13~~ ; 7) ~~R4.4~~ ; 8) ~~heuristique~~ ; 9) ~~bloc~~ ; 10) ~~coréférence~~.
- **Ambition** : un **runtime cognitif** où penser est une recherche tracée sur des états pluriels.
- **Stratégie** : v0 petit et mesuré.
- **Objectif final** : un **moteur de pensée v0** exécutable, documenté, mesuré, committé.
- **Fait** : B13 **134/140** (4 S `647205a` + 2 test périmé T132/T133 ; le 140/140 de 702b368c
  ne se rejoue pas), gold **432** ; **gold neuronal** POS/syntagmes, cascade
  **0,9415/0,7539/1,0** ; **DRVM/native** cadenas 3, porte 27 (règle), labyrinthe 2 sonde ;
  **pragmatique** dev 1,0, test 0,6375 (majoritaire 0,7556) ; l'heuristique garde ;
  [B13](../../reports/rapport-b13-porte-134.md), [pragmatique](../../reports/rapport-pensee-pragmatique-neuronale.md).
- **Ce qu'elle fait** : **gold neuronal, DRVM, pragmatique et porte B13** mesurés ; reprise **16 h 16**.
- **Ce que font les autres** : **N2**, **S**, **D/R/A**, **hub**.
- **Prochaine action** : **gold 200+ phrases** ; **porte B13** ; **porte qui bouge**.
- **Bloquants** : aucun pour POS/syntagmes/cascade/DRVM ; la **pragmatique neuronale** ne qualifie pas ; restent **gold 200+** et **porte B13**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

> **Session close** : `fe3c05f0` — **91 scans uniques**, 60 documents, 1 982 p, 4,41 M car. ;
> [clôture](../../journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/cloture.md),
> fiche [`ocr-cegep`](../../reports/rapport-ocr-cegep.md).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; **R0.4/R0.5 closes (négatifs)** ; R0.6 **12/20** au pilote, **7/7** à la porte.
- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 intérieur, ×62,7 tout ; [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../reports/rapport-typoglycemie.md).
- **Données** : **10 corpus** (**21,6 M art.**, **31,4 G car.**, **38,8 Go**, **0 fuite**) ; **OCR CEGEP** **91 scans uniques** (60 documents, 1 982 p, 4,41 M car.) ; **glossaire** 355 entrées — [`inventaire`](../../reports/inventaire-donnees-entrainement.md), [`corpus-wikipedia`](../../reports/rapport-corpus-wikipedia.md), [`ocr-cegep`](../../reports/rapport-ocr-cegep.md).
- **R1 — la fenêtre native** : **R1.1** RoPE **3,2545** à 1 000 octets (table absolue **8,2024**),
  invariant au décalage ; **R1.2** à octets constants **3,0107** (−0,244), le contexte est utilisé ;
  depuis zéro, RoPE ne suffit pas — [`n2-r11`](../../reports/rapport-n2-r11.md).
- **S — le banc de structures** : **analyseur 47/47 types, 117/117 rôles, 47/47 compléments**, gold **47**, **43 tests** ; corpus **47** structures (SHA `f2a0d2fb…`) ; [`fiche`](../../reports/rapport-s-analyseur-roles.md) ; **banque validée à 0**.
- **N2** : **N2.ac** 1 Go — **3,49** domaine, **6,03** littérature ; **200 k pas** — val_fr
  **3,1591** (−0,33), grand corpus **3,0035**, littérature **5,6056**, anglais **7,2770**, wikitext2
  **8,0018** : **< 2,5 non atteinte** (la loi place 2,5 à **1,3–2,7 M pas**), et le gain
  **s'inverse à 512 octets** (+0,14) — le compute ne remplace pas une fenêtre entraînée ; N4
  **0/40** ; [`n2-200k`](../../reports/rapport-n2-200k.md),
  [`n2-canaux`](../../reports/rapport-n2-canal-34m.md),
  [`n2-1go`](../../reports/rapport-n2-corpus-1go.md).
- **Pensée — B13** : state store v0, AC-3/alpha-bêta, DRVF, banc, opérateurs, **134/140** (4 S + 2 test périmé) ; gold
  **432 réels**, coréférence **116 liens** ; [`pensee-vrais-absents`](../../reports/rapport-pensee-vrais-absents.md),
  [`pensee-anaphore-bilan`](../../reports/rapport-pensee-anaphore-bilan.md).

## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **81** (76 vertes, 5 rouges au 02/11 06 h — 4 connues + greffe à 700 s, verte à 1200 s) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **560** / **647** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **119** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **02/11 06 h** (81 portes, 76/5) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 134/140, gold 432, 116 liens** | **B13 : gold 200+ ; porte 134/140** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N3, N4** | N2 : **N2.ac 1 Go — 3,49 domaine / 6,03 littérature** ; < 2,5 non atteinte ; N4 0/4 ; N5 gelé | **N2** : 200 k pas **en cours** (session `0733c5bb`), puis **R1.1/R1.2** ; **N4** |
| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** (398 langues) ; R2/R3 attendent N5/N4 | **R1.1/R1.2 mesurées** ; la suite est **1 024 octets entraînés** (fenêtre), pas un autre schéma |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

**C1** corpus · **C2** traduction · **C3** restitution · **C4** styles · **C5** domaines ·
**C6** documentation · **C7** pensée — hors graphe.

## Ce qui reste

**N2** — **fiche et clôture du run de 200 k** ; **R1** — 1 024 octets entraînés ; **Pensée** — gold 200+,
porte B13 ; **S** — validation humaine, h033 ; **N4** — la consigne ; **B10.3** — le `z` ;
**B13** — porte 134/140 (4 S + 2 test périmé) ; **R0.7** — le tagger complet ; **D** — OCR clos (8 scans `.PDF`).

- **Vue d'ensemble** : huit chantiers et relations [`chantiers`](chantiers.md) ; plan multi-sessions [`plan-travail`](plan-travail.md) ; carte [`chantiers-vision.svg`](../schemas/chantiers-vision.svg).

## Les questions ouvertes

- **R1** : **1 000 octets** sans refaire 130–256 ? → **R1.2** tranche (3,0107 à octets constants) ;
  reste **1 024 octets**.
- **N2** : les **200 k pas** font-ils passer **< 2,5** sans perdre le français ? → **non** :
  3,1591 ; le français tient et la largeur progresse ; 2,5 est à **1,3–2,7 M pas**.
- **N4** : une **consigne courte** tient-elle hors du vu ? → **N4** tranche (0/4 tenus).
- **B10.3** : chrF **> 39,6** ? → l'attention croisée tranche.
- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche.

## La carte

- **Méthode** : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · **plan** :
  [roadmap](roadmap.md) · [backlog](backlog/index.md) · [graphe](backlog/dependances.md) ·
  [carte](../theorie/carte.md) · **preuves** : [reports/](../../reports/) ·
  [journal/](../../journal/).

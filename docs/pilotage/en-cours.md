# En ce moment

**Mis à jour : 2026-11-02, 21 h 17 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).
>
> **Reprise après le reboot du 02/11 15 h 06** : quatre sessions rouvertes ; **D/R/A close**
> (18 h 45), **N2** close à 19 h 46 puis **rouverte** pour la **nuit** ; runbook :
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

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : 1–4) ~~plan, analyseur (gold 55), export, tests 47~~ ; 5–6) ~~fiche, pointeur, état~~.
- **Ambition** : nommer le rôle et la frontière GN.
- **Stratégie** : une règle = une phrase, trois contrôles.
- **Objectif final** : gold **55**, corpus **55**, manifeste SHA-256.
- **Fait** : types **54/55**, rôles **131/131** ; contrôles **94/131**, **96/131**, **0,109** ; h033/h046/h047 corrigés, **h050/h053** limites nommées ; **corpus réel** : GN+GV **8,5 %** CEGEP (mélange 9,1 %), **65,5 %** propre (9,1 %) ; banque **200** phrases / **355** candidats ; **47 tests** ; [`analyseur`](../../reports/rapport-s-analyseur-roles.md), [`réel`](../../reports/rapport-s-corpus-reel.md).
- **Ce qu'elle fait** : **`00d2a01`** ; corpus **55** (SHA `76accf9d…`) ; banque **200** phrases / **355** candidats, **0** validée.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**, **D/R/A**.
- **Prochaine action** : **h050/h053**, puis validation humaine de la banque.
- **Bloquants** : aucun ; **banque à 0** verdict.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN plurielle, arbre d'états, moteur N3 ; R4.4 ; heuristique ; bloc linguistique.
- **Plan** : 1–6) ~~moteur B13~~ ; 7) ~~R4.4~~ ; 8) ~~heuristique~~ ; 9) ~~bloc~~ ; 10) ~~coréférence~~.
- **Ambition** : un **runtime cognitif** où penser est une recherche tracée sur des états pluriels.
- **Stratégie** : v0 petit et mesuré.
- **Objectif final** : un **moteur de pensée v0** exécutable, documenté, mesuré, committé.
- **Fait** : B13 **140/140** (6 S fixés ; T132/T133 2/5), gold **432** ; **gold
  neuronal** POS/syntagmes, cascade **0,9415/0,7539/1,0** ; **DRVM/native** cadenas 3, porte 27,
  labyrinthe 2 ; **porte minute** — **26 nœuds** ; **porte mobile** — (3,3) **échoue**, (1,3)
  passe (28/4) ; **porte bouge** — 25/2 mais l'aveugle (25/2) et le labyrinthe (28/5) aussi :
  test faible ; **pragmatique** 0,6375 ; l'heuristique garde ;
  [B13](../../reports/rapport-b13-porte-138.md), [minute](../../reports/rapport-pensee-porte-minute.md),
  [mobile](../../reports/rapport-pensee-porte-mobile.md), [bouge](../../reports/rapport-pensee-porte-bouge.md),
  [pragmatique](../../reports/rapport-pensee-pragmatique-neuronale.md).
- **Ce qu'elle fait** : **gold neuronal, DRVM, pragmatique, portes** mesurés ; reprise **16 h 16**.
- **Ce que font les autres** : **N2**, **S**, **D/R/A**, **hub**.
- **Prochaine action** : **gold 200+** ; **porte stochastique/fenêtre** ; **porte B13** attend S.
- **Bloquants** : aucun pour POS/syntagmes/cascade/DRVM/minute/mobile ; la **pragmatique neuronale** ne qualifie pas ; la **porte B13** attend S ; reste **gold 200+**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2, la nuit : la fenêtre à 1 024

- **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
- **Rôle** : **N2** — R1.2 à **1 024 octets** et la fenêtre sur le **mélange de production**.
- **Plan** : R1.2-1024 (2 500 → 20 000 pas) ; mélange affiné à 512 ; fiche + commit par fait.
- **Ambition** : que la longueur cesse de reculer.
- **Stratégie** : RoPE, budgets contrôlés, mêmes bancs, contrôles joints.
- **Objectif final** : une fenêtre 1 024 mesurée, une production qui tient à 1 000 octets.
- **Ce qu'elle fait** : R1.2-1024 lancée à 19 h 57 (GPU 0) ; les portes gardent le GPU 1.
- **Ce que font les autres** : **hub** (portes), **S** (analyseur), **Pensée** (B13).
- **Prochaine action** : les contrôles de R1.2-1024, puis la fiche.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

> **Session close** : `fe3c05f0` (D/R/A) — OCR CEGEP (91 scans, 60 documents, 1 982 p,
> 4,41 M car.) ; [clôture](../../journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/cloture.md),
> fiche [`ocr-cegep`](../../reports/rapport-ocr-cegep.md).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; **R0.4/R0.5 closes (négatifs)** ; R0.6 **12/20** au pilote, **7/7** à la porte.
- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 intérieur, ×62,7 tout ; [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../reports/rapport-typoglycemie.md).
- **Données** : **10 corpus** (**21,6 M art.**, **31,4 G car.**, **38,8 Go**, **0 fuite**) ; **OCR CEGEP** **91 scans uniques** (60 documents, 1 982 p, 4,41 M car.) ; **glossaire** 355 entrées — [`inventaire`](../../reports/inventaire-donnees-entrainement.md), [`corpus-wikipedia`](../../reports/rapport-corpus-wikipedia.md), [`ocr-cegep`](../../reports/rapport-ocr-cegep.md).
- **R1 — la fenêtre native** : **R1.1** RoPE **3,2545** à 1 000 octets (table absolue **8,2024**),
  invariant au décalage ; **R1.2** à octets constants **3,0107** (−0,244), le contexte est utilisé ;
  depuis zéro, RoPE ne suffit pas — [`n2-r11`](../../reports/rapport-n2-r11.md).
- **S — le banc de structures** : **analyseur 54/55 types, 131/131 rôles, 47/47 compléments**, **corpus réel 8,5 % CEGEP / 65,5 % propre** (mélange 9,1 %), gold **55**, **47 tests** ; corpus **55** structures (SHA `76accf9d…`) ; banque **200** phrases / **355** candidats ; fiches [`analyseur`](../../reports/rapport-s-analyseur-roles.md), [`réel`](../../reports/rapport-s-corpus-reel.md) ; **banque validée à 0**.
- **N2** : **200 k pas** — **3,16 / 5,61 / 7,28 / 8,00** (**< 2,5 non atteinte** ; 2,5 à
  1,3–2,7 M pas) ; **R1.2 à 1 024** lancée pour la nuit (GPU 0) ; N4 **0/40** ;
  [`n2-200k`](../../reports/rapport-n2-200k.md), [`n2-canaux`](../../reports/rapport-n2-canal-34m.md).
- **Pensée — B13** : **140/140**, gold **432**, **116 liens** ; minute 26, mobile/bouge **faibles** ; [`vrais-absents`](../../reports/rapport-pensee-vrais-absents.md),
  [`anaphore-bilan`](../../reports/rapport-pensee-anaphore-bilan.md).

## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **82** (81 à la passe du 02/11 06 h : 76/5 ; **82e `porte-ressources`**, à valider) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **567** / **652** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **119** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **02/11 06 h** (81 portes, 76/5) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 140/140, gold 432, 116 liens** | **B13 : gold 200+ ; porte 140/140 ; minute 26, mobile/bouge faibles** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N3, N4** | N2 : **200 k pas — 3,16 / 5,61 / 7,28 / 8,00** ; **< 2,5 non atteinte** (2,5 à 1,3–2,7 M pas) ; **R1.2-1024 en cours** (GPU 0) ; N4 0/4 ; N5 gelé | **N2** : R1.2-1024, fiche ; **N4** |
| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** (398 langues) ; R2/R3 attendent N5/N4 | **R1.1/R1.2 mesurées** ; la suite est **1 024 octets entraînés** (fenêtre), pas un autre schéma |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

**C1** corpus · **C2** traduction · **C3** restitution · **C4** styles · **C5** domaines ·
**C6** documentation · **C7** pensée — hors graphe.

## Ce qui reste

**R1** — R1.2-1024 (nuit) ; **Pensée** — gold 200+, porte mobile ; **S** — homographes, validation ;
**N4** — la consigne ; **B10.3** — le `z` ; **B13** — 138/140 ; **R0.7** — le tagger ; **D** — OCR clos (8 `.PDF`).

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

- Méthode : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · plan : [roadmap](roadmap.md) ·
  [backlog](backlog/index.md) · preuves : [reports/](../../reports/) · [journal/](../../journal/).

# En ce moment

**Mis à jour : 2026-11-03, 00 h 52 HNE (heure locale, EST).**

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
>
> **Nuit du 02/11 → 03/11 (08 h)** : les quatre sessions restent productives ; claims dans `work/ressources.json` ; à la fin d'un job, `--release` puis `--claim` du suivant ; si une action attend l'humain, prendre la ligne suivante. Le hub suit la passe et fera le bilan à 08 h.

### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise

- **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
- **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
- **Plan** : 1–7) ~~audit, commits, état, mandats, porte, INDEX, runbook~~ ; 8–9) **intégration,
  portes** (GPU 1).
- **Ambition** : un état reprenable, des mandats qui disent la vérité.
- **Stratégie** : committer par flux (`git add` explicite), nommer ce qui reste.
- **Objectif final** : sédimentation à zéro, quatre mandats explicites, runbook.
- **Ce qu'elle fait** : intégration ; **passe close — 81 portes, 76 vertes, 5 rouges, 1 h 52** ;
  INDEX/README ; **bilan de 8 h**.
- **Ce que font les autres** : **N2**, **S**, **Pensée**.
- **Prochaine action** : intégrer les lignes B13/N2/S ; tenir le **bilan de 8 h**.
- **Bloquants** : aucun ; GPU à N2 (les deux), claims dans le registre.
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
- **Fait** : B13 **140/140** (6 S fixés ; T132/T133 2/5), gold **432** ; **gold neuronal** —
  cascade **0,9415 / 0,6130 / 0,7575 / 1,0** (180) ; **réel 432 : 0,9065/0,4598/0,5633/0,9954 (0,90/0,45/0,55/0,50 → true) ; cache ; voisin 2/5 ;
  **DRVM/native** 3/27/2 ; **porte sto** — **5/5** (28–34 nœuds, 5–7 sonde) ; **fenêtre** — **non discriminante** (oracle 228, aveugle 215) ; mobile/bouge **faibles** ; **pragmatique** 0,6375 ;
  [B13](../../reports/rapport-b13-porte-140.md), [sto](../../reports/rapport-pensee-porte-sto.md),
  [sto 5/5](../../reports/rapport-pensee-porte-sto-graines.md),
  [fenêtre](../../reports/rapport-pensee-porte-fenetre.md),
  [pragmatique](../../reports/rapport-pensee-pragmatique-neuronale.md).
- **Ce qu'elle fait** : **gold neuronal, DRVM, pragmatique, portes** mesurés ; reprise **16 h 16**.
- **Ce que font les autres** : **N2**, **S**, **D/R/A**, **hub**.
- **Prochaine action** : **gold 200+** ; **porte stochastique/fenêtre** ; **porte B13** attend S.
- **Bloquants** : aucun pour POS/syntagmes/cascade/DRVM/minute/mobile ; la **pragmatique neuronale** ne qualifie pas ; la **porte B13** attend S ; reste **gold 200+**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2, la nuit : la fenêtre à 1 024

- **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
- **Rôle** : **N2** — la fenêtre à **1 024** et la fenêtre sur la **production**.
- **Plan** : loi, production, 2 048 ; fiche par fait.
- **Ambition** : la longueur d'abord.
- **Stratégie** : budgets contrôlés, mêmes bancs.
- **Objectif final** : une production qui tient au long.
- **Ce qu'elle fait** : la **loi de la fenêtre** jusqu'à 2 048 et la **production** (N2.ac +
  RoPE 512/1 024) ; le compute à fenêtre 1 024 en cours.
- **Ce que font les autres** : **hub**, **S**, **Pensée**.
- **Prochaine action** : **2 048**, puis un point de compute.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

> **Session close** : `fe3c05f0` (D/R/A) — OCR CEGEP (91 scans, 60 documents, 1 982 p,
> 4,41 M car.) ; [clôture](../../journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/cloture.md),
> fiche [`ocr-cegep`](../../reports/rapport-ocr-cegep.md).

## Ce qui est en cours

- **Données** : **10 corpus** (**21,6 M art.**, **31,4 G car.**, **38,8 Go**, **0 fuite**) ; **OCR CEGEP** **91 scans uniques** (60 documents, 1 982 p, 4,41 M car.) ; **glossaire** 355 — [`inventaire`](../../reports/inventaire-donnees-entrainement.md), [`corpus-wikipedia`](../../reports/rapport-corpus-wikipedia.md), [`ocr-cegep`](../../reports/rapport-ocr-cegep.md).
- **R1 — la fenêtre native** : loi mesurée jusqu'à **2 048** (**2,9950** à 1 024) ;
  **1 024 est le point d'équilibre** ; à 20 000 pas : **2,6256** à 1 000 —
  [`2048`](../../reports/rapport-n2-r12-2048.md), [`fenêtre`](../../reports/rapport-n2-fenetre.md).
- **S — le banc de structures** : **analyseur 54/55 types, 131/131 rôles, 47/47 compléments**, **corpus réel 8,5 % CEGEP / 65,5 % propre** (mélange 9,1 %), gold **55**, **47 tests** ; corpus **55** structures (SHA `76accf9d…`) ; banque **200** phrases / **355** candidats ; fiches [`analyseur`](../../reports/rapport-s-analyseur-roles.md), [`réel`](../../reports/rapport-s-corpus-reel.md).
- **N2** : **200 k pas** — **3,16 / 5,61 / 7,28 / 8,00** (< 2,5 non atteinte) ;
  **la fenêtre bat le compute** : N2.ac + RoPE 512 (1 h) donne **3,1588 / 2,7607** à
  128/512/2 000 — [`fenêtre`](../../reports/rapport-n2-fenetre.md),
  [`n2-200k`](../../reports/rapport-n2-200k.md).
- **Pensée — B13** : **140/140**, gold **432**, **116 liens** ; minute 26, mobile/bouge **faibles** ; [`vrais-absents`](../../reports/rapport-pensee-vrais-absents.md),
  [`anaphore-bilan`](../../reports/rapport-pensee-anaphore-bilan.md).

## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **82** (passe 19 h 32 : **81, 76/5** ; **82e `porte-ressources`** verte, comptée à la suivante) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **577** / **662** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **119** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **02/11 19 h 32** (81, 76/5 ; 4 connues + `porte-tableaux` verte) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 140/140, gold 432, 116 liens** | **B13 : gold réel 432 (0,9065/0,4598/0,5633/0,9954) ; porte 140/140 ; sto 5/5** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N3, N4** | N2 : **200 k pas — 3,16 / 5,61 / 7,28 / 8,00** ; < 2,5 non atteinte (1,3–2,7 M pas) ; N4 0/4 ; N5 gelé | **la fenêtre bat le compute** (N2.ac + RoPE 512 : 2,9096 à 512, 2,7607 à 2 000) ; **2 048** en cours |
| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **loi de la fenêtre mesurée** (256 → 1 024) ; **2 048** en cours, puis un professeur long à distiller |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

**C1** corpus · **C2** traduction · **C3** restitution · **C4** styles · **C5** domaines ·
**C6** documentation · **C7** pensée — hors graphe.

## Ce qui reste

**R1** — R1.2-1024 ; **Pensée** — gold 200+ ; **S** — homographes, validation ;
**N4** — consigne ; **B10.3** — `z` ; **B13** — 140/140 ; **R0.7** — tagger ; **D** — OCR clos (8 `.PDF`).

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

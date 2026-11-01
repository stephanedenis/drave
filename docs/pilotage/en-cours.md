# En ce moment

**Mis à jour : 2026-11-01, 17 h 50 HNE (heure locale, EST).**

> **État courant, pas histoire.** Une sous-section par **session active**, une ligne par **chantier**
> avec son **bloquant**. Méthode : [`methode/`](../methode/) (contexte, continuité). Résultats :
> [`reports/`](../../reports/). Histoire : [`journal/`](../../journal/). Plan : [`roadmap.md`](roadmap.md).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session qui trouve l'état en retard
> le corrige.

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN plurielle, arbre d'états, moteur N3 ; reprise R4.4 ; **analyse de la couche heuristique** ; **bloc linguistique**.
- **Plan** : 1) ~~RSN plurielle, arbre, cycle~~ ; 2) ~~portefeuille, contrat, anytime~~ ; 3) ~~state store v0 (6/6 portes)~~ ; 4) ~~moteur v0 (BFS, greedy, A*, MCTS-lite)~~ ; 5) ~~AC-3, alpha-bêta~~ (**8/8**) ; ~~DRVF~~ (**9/9**) ; 6) **banc anytime** (AUC, regret, justification, rejeu) et intégration ; 7) ~~reprise R4.4~~ ; 8) ~~couche heuristique~~ (analyse, 5 schémas) ; 9) **bloc linguistique** (R0.7).
- **Ambition** : un **runtime cognitif** où penser est une recherche tracée sur des états pluriels, avec des opérateurs hétérogènes.
- **Stratégie** : théorie d'abord, puis un **v0 petit et mesuré** ; réserver les fichiers ; ne pas toucher aux GPU de N2.
- **Objectif final** : un **moteur de pensée v0 exécutable** — state store, arbre, A*/MCTS/AC-3, trace/rejeu, banc avec contrôles — documenté, mesuré, committé.
- **Reprise** : **R4.4** — note de clôture des trois limites (fax 1 bit, exposant fusionné,
  parité réelle sans questions) ; **S** est actif dans une autre TUI (export pragmatique, 11 tests).
- **Coloration** : analyse [`pre-traitement-linguistique`](../theorie/pre-traitement-linguistique.md)
  (5 schémas) — le CPU étiquette la surface et énumère le plausible, le réseau tranche l'ambiguïté ;
  la cascade se juge sur la couverture × la précision par unité de calcul, pas sur le débit.
- **Bloc linguistique** : **R0.7** — le contrat [`bloc-linguistique`](../implantation/bloc-linguistique.md)
  (9 niveaux, heuristique CPU + neuronal de contrat, parallèle/cascade, activation 51–76 %) ;
  **398 langues à 0,9687**, script **1,0000**, permuté **0,0022** ; fiche et porte ; le modèle
  réel local n'est pas qualifié.
- **Moteur B13** : **AC-3, alpha-bêta (8/8)** et **DRVF `thought` (9/9)** — la trace se relit,
  se rejoue à l'identique et refuse un score modifié ; **23 597 octets, 93 événements** ;
  fiches [`pensee-ac3-alphabeta`](../../reports/rapport-pensee-ac3-alphabeta.md) et
  [`pensee-drvf`](../../reports/rapport-pensee-drvf.md) ; prochain : **banc anytime**.
- **Ce qu'elle fait** : **state store v0** écrit et testé — **6/6 portes** (T0 canonique, T1 rejeu,
  T2 stratégies, T3 anytime, T4 justification) sur le jouet des cruches ; BFS, greedy, A* et
  MCTS-lite ; puis **AC-3 et alpha-bêta** (8/8 ; 1 495/296 contre 18 730) ; fiches
  [`pensee-v0`](../../reports/rapport-pensee-v0.md) et
  [`pensee-ac3-alphabeta`](../../reports/rapport-pensee-ac3-alphabeta.md).
- **Ce que font les autres** : **N2.h** et **R4.4** sont **closes** ; **S** (le banc de structures)
  avance ; **N4** en file ; **A/B** gardent les leurs.
- **Interfaces** : `State`, `Proposal`, `Score`, `Decision`, `Trace` ; un opérateur est un bloc `state → state`.
- **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`, `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`, `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`, `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`, `tools/porte-bloc-linguistique.sh`, `tools/tests/linguistique/`, `docs/implantation/bloc-linguistique.md`, `docs/schemas/bloc-linguistique-*.svg`, `reports/bloc-*`, `journal/sessions/e181ce02-…/`.
- **Prochaine action** : **bloc linguistique v0** livré (398 langues) ; gold + modèle neuronal ; **moteur B13** : **banc anytime** (DRVF fait).
- **Bloquants** : aucun ; corpus de test à choisir ; pas de GPU.
- **Journal** : [le 31/10](../../journal/2026-10-31/README.md) · [le 01/11](../../journal/2026-11-01/README.md) · [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

> **Sessions archivées** : `8156fdcb`, `c3d0f0bd`, `N2-GPU`, `71d57f53`, `0b69f616`, `22e518ee`,
> `0b0a6a0d` (N2.h/N2.i, close) et `fe3c05f0` (R4.4, close ; restes nommés : fax 1 bit,
> exposant fusionné, parité réelle sans questions) — rapports dans [`journal/sessions/`](../../journal/sessions/).

### Session `fe3c05f0-834b-44f2-8739-501865d652c1` — D/R/A : les données, le lecteur, le moteur

- **Id** : `fe3c05f0-834b-44f2-8739-501865d652c1` — [`plan.md`](../../journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md).
- **Rôle** : **D/R/A** — le texte intégral, l'extraction PDF/OCR, la prépa R1.1/R1.2, A2.6/A8.3.
- **Plan** : le texte intégral (pilote FR), puis PDF/OCR, puis R1.1/R1.2.
- **Ambition** : le français réel pour N2 ; D, carburant.
- **Stratégie** : le dump, débaliseur mesuré, dédup, splits.
- **Objectif final** : 10 corpus en texte intégral, mesurés et ficés.
- **Ce qu'elle fait** : le **texte intégral FR** (**2,39 M articles**, **8,3 Go**, **0 fuite 8 Ko**, **0/40** éval) ; les **9 langues** en cours (en, de, ru, es, ja) ; [`fiche`](../../reports/rapport-corpus-wiki-texte.md).
- **Ce que font les autres** : Pensée, S, N2 ; le hub tient l'état.
- **Prochaine action** : les 9 langues, la contamination et les fiches, puis PDF/OCR.
- **Bloquants** : aucun.
- **Journal** : [le 01/11](../../journal/2026-11-01/README.md).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; **R0.4/R0.5 closes (négatifs)** ; R0.6 **12/20** au pilote, **7/7** à la porte ; fiches [`r04`](../../reports/rapport-r04-tete-survol.md), [`r07`](../../reports/rapport-r07-routeur.md), [`r06`](../../reports/rapport-r06-publication.md).
- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 au mélange intérieur, ×62,7 tout ; fiches [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../reports/rapport-typoglycemie.md).
- **Données** : inventaire local (Wikipédia **132 Go**, documents **~228 Go**, DRM et vidéos exclus) ; **corpus par langue** (10) : **21,6 M articles**, **31,4 G caractères**, **38,8 Go**, **0 fuite** — fiches [`inventaire-donnees`](../../reports/inventaire-donnees-entrainement.md), [`corpus-wikipedia`](../../reports/rapport-corpus-wikipedia.md).
- **S — le banc de structures** : outil web (`tools/structures`), générateur, pragmatique (double sens, niveaux 0–4), export JSONL (12 tests) ; 7 phrases, 14 candidats ; [`README`](../../tools/structures/README.md).
- **R13 — la tokenisation** : **close**, décision **octets** — BPE 512 +0,39 %, 1024 +4,09 % ; fiche [`r13`](../../reports/rapport-r13-decision.md).
- **B10.2bis — décodeur** : 3×3 **11,1** ; capacité 11,8 ; **mots 32,5** ; **JW 26,7** ; `z` 1,5–2,6 ; fiches [`b102bis`](../../reports/rapport-b102bis-decodeur.md), [`mots`](../../reports/rapport-b10-decodeur-mots.md), [`mots-jw`](../../reports/rapport-b10-mots-jw.md).
- **A8** : **A8.0 : 19** ; **A8.3b refusé** (lot) ; **A8.3c/d** : lot 1≠≥2, threads innocents ; fiches [`a83`](../../reports/rapport-a83-defaut.md), [`a83b`](../../reports/rapport-a83b-regimes.md), [`a83c`](../../reports/rapport-a83c-lot.md), [`a83d`](../../reports/rapport-a83d-lot-threads.md).
- **B11.10** : **hybride 4/4** — codec **161/161**, ambiguïtés refusées ; **69,3 %** natif ;
  [`b1110`](../../reports/rapport-b1110-cartes.md).
- **N2.h/N2.i — closes** : corpus dédupliqué, **3,09** en domaine, **12,93** littérature, **33,83** anglais ; **N2.j** (186 Mo) **7,42/12,41** ; **N2.k** (10 langues) fr **5,68**, anglais **6,30** ; **N2.j2** : 256 **9,28 → 4,49**, 512 **13,37 → 5,67** ; **N2.j3** : 21,65 M **4,20** (11,47 M 4,39) ; N4 **0/40**. Fiches [`n2-propre`](../../reports/rapport-n2-propre.md), [`n2-corpus-reel`](../../reports/rapport-n2-corpus-reel.md), [`n2-capacite-reelle`](../../reports/rapport-n2-capacite-reelle.md).
- **Pensée — state store v0** : 6/6 portes (BFS, greedy, A*, MCTS-lite), jouet des cruches ; fiche [`pensee-v0`](../../reports/rapport-pensee-v0.md) ; prochaine AC-3, alpha-bêta, DRVF.


## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **81** (75 vertes, 4 rouges à la passe du 31/10 19 h 42 ; 2 ajoutées depuis) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **390** / **477** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **118** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 46** (01/11 00 h 56) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Les dépendances vivent dans le graphe** ([`dependances.md`](backlog/dependances.md) §5, schéma
[`backlog-dependances.svg`](../schemas/backlog-dependances.svg)), recalculé par
`tools/verifie_backlog.py`. Cette table ne garde que les **bloquants externes** et la **prochaine
action** — pas les statuts, qui dérivent. Vue d'ensemble :
[**la carte de décision**](../schemas/chantiers-decision.svg).

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : AC-3/alpha-bêta 8/8, DRVF 9/9** | **B11.10 close** ; **B13 : banc anytime** ; B10.3 bloquée |
| **N — le natif** | **N3, N4** | N2.h close ; N2 < 2,5 non atteinte ; N4 0/4 ; N5 gelé | **N2 close** ; **N4** (consigne) |
| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** (398 langues) ; R1/R2/R3 attendent N5/N4 | **R1.1/R1.2** (contexte natif) |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

> **P — la pensée** (session `e181ce02`) : RSN plurielle, arbre, moteur N3 ; fichiers réservés ;
> ni GPU ni `toutes-les-portes.sh`.

**Les sept chantiers C** — **C1** corpus · **C2** traduction · **C3** restitution · **C4**
styles · **C5** domaines · **C6** documentation · **C7** pensée — hors graphe, mesurés, du récit.

## Ce qui reste

**N2.h** — **close** (N2.i : 12,93 littérature, 33,83 anglais ; porte < 2,5 non atteinte) ;
**Pensée** — **banc anytime** (AC-3/alpha-bêta/DRVF faits ; session `e181ce02`) ; **N4** — la consigne
courte ; **B10.3** — le `z` et l'encodeur ; **R4.4** — close, limites nommées ; **R0.7** — gold/neuronal ; **R1.1/R1.2** — le contexte natif ; **S** — l'export au corpus.

- **Vue d'ensemble** : huit chantiers et relations [`chantiers`](chantiers.md) ; plan multi-sessions [`plan-travail`](plan-travail.md) ; carte [`chantiers-vision.svg`](../schemas/chantiers-vision.svg).

## Les questions ouvertes

- **R1** : **1 000 octets** sans refaire 130–256 ? → **R1.1** (état de section) puis **R1.2**
  (curriculum) tranchent ; la hiérarchie de N2 est écartée.
- **N2** : la porte **< 2,5** est-elle la bonne, après N2.h (**3,09** en domaine, **12,93** en littérature) ? →
  la **roadmap N** tranche.
- **N4** : une **consigne courte** tient-elle hors du vu ? → **N4** tranche (0/4 tenus).
- **B10.3** : chrF **> 39,6** ? → **B10.3** (attention croisée) tranche.
- **Pensée** : le **banc anytime** bat-il le greedy, et à quel coût ? →
  le **v0 suivant** tranche.

## La carte

- **Méthode** : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md).
- **Plan** : [roadmap.md](roadmap.md) · [backlog](backlog/index.md) · [graphe](backlog/dependances.md) ·
  [carte](../theorie/carte.md) · [inventaire](../README.md).
- **Preuves** : [reports/](../../reports/) · [journal/](../../journal/) ·
  [état transféré](../../journal/2026-10-29/etat-transfere.md).

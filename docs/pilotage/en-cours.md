# En ce moment

**Mis à jour : 2026-11-01, 16 h 30 HNE (heure locale, EST).**

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
- **Plan** : 1) ~~RSN plurielle, arbre, cycle~~ ; 2) ~~portefeuille, contrat, anytime~~ ; 3) ~~state store v0 (6/6 portes)~~ ; 4) ~~moteur v0 (BFS, greedy, A*, MCTS-lite)~~ ; 5) ~~AC-3, alpha-bêta~~ (**8/8**), **DRVF** ; 6) **banc anytime** (AUC, regret, justification, rejeu) et intégration ; 7) ~~reprise R4.4~~ ; 8) ~~couche heuristique~~ (analyse, 5 schémas) ; 9) **bloc linguistique** (R0.7).
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
- **Moteur B13** : **AC-3 et alpha-bêta** — **8/8 portes** ; chaîne A/B/C, carte arc-consistante,
  contradiction ; alpha-bêta **1 495 nœuds / 296 coupes** contre **18 730** au minimax ; fiche
  [`pensee-ac3-alphabeta`](../../reports/rapport-pensee-ac3-alphabeta.md) ; prochain : **DRVF**,
  banc anytime.
- **Ce qu'elle fait** : **state store v0** écrit et testé — **6/6 portes** (T0 canonique, T1 rejeu,
  T2 stratégies, T3 anytime, T4 justification) sur le jouet des cruches ; BFS, greedy, A* et
  MCTS-lite ; puis **AC-3 et alpha-bêta** (8/8 ; 1 495/296 contre 18 730) ; fiches
  [`pensee-v0`](../../reports/rapport-pensee-v0.md) et
  [`pensee-ac3-alphabeta`](../../reports/rapport-pensee-ac3-alphabeta.md).
- **Ce que font les autres** : **N2.h** et **R4.4** sont **closes** ; **S** (le banc de structures)
  avance ; **N4** en file ; **A/B** gardent les leurs.
- **Interfaces** : `State`, `Proposal`, `Score`, `Decision`, `Trace` ; un opérateur est un bloc `state → state`.
- **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`, `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`, `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`, `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`, `tools/porte-bloc-linguistique.sh`, `tools/tests/linguistique/`, `docs/implantation/bloc-linguistique.md`, `docs/schemas/bloc-linguistique-*.svg`, `reports/bloc-*`, `journal/sessions/e181ce02-…/`.
- **Prochaine action** : **bloc linguistique v0** livré (398 langues) ; gold + modèle neuronal ; **moteur B13** : **DRVF**, banc anytime.
- **Bloquants** : aucun ; corpus de test à choisir ; pas de GPU.
- **Journal** : [le 31/10](../../journal/2026-10-31/README.md) · [le 01/11](../../journal/2026-11-01/README.md) · [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

> **Sessions archivées** : `8156fdcb`, `c3d0f0bd`, `N2-GPU`, `71d57f53`, `0b69f616`, `22e518ee`,
> `0b0a6a0d` (N2.h/N2.i, close) et `fe3c05f0` (R4.4, close ; restes nommés : fax 1 bit,
> exposant fusionné, parité réelle sans questions) — rapports dans [`journal/sessions/`](../../journal/sessions/).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; **R0.4 close (négatif)** ; **R0.5 close
  (négatif)** ; R0.6 **12/20** au pilote, **7/7** à la porte. Fiches
  [`r04`](../../reports/rapport-r04-tete-survol.md), [`r07`](../../reports/rapport-r07-routeur.md),
  [`r06`](../../reports/rapport-r06-publication.md) (cascade à confiance **publiée**).
- **R4.1–R4.4 — les blocs** : **mesurés** — 996/802 cellules, 294/24 fichiers,
  32/10 formules ; **R4.4** scans simulés (4/5 ≥ **90 %**) ; **typoglycémie** : le modèle lit les
  lettres (×17,8 au mélange intérieur, ×62,7 tout) ; fiches
  [`r44-scans`](../../reports/rapport-r44-scans.md) · [`typoglycemie`](../../reports/rapport-typoglycemie.md).
- **Données** : inventaire local (Wikipédia **132 Go**, documents **~228 Go**, DRM et vidéos exclus) ;
  **corpus par langue** (10) : **21,6 M articles**, **31,4 G caractères**, **38,8 Go**, splits par
  article, **0 fuite** — fiches [`inventaire-donnees`](../../reports/inventaire-donnees-entrainement.md),
  [`corpus-wikipedia`](../../reports/rapport-corpus-wikipedia.md) (catalogue et manifestes).
- **S — le banc de structures** : outil web (`tools/structures`, submodule) ; **générateur**
  heuristique, **pragmatique** (statuts, **double sens conservé**, **niveaux de contexte 0–4**,
  **niveau minimal** mesuré) et **export corpus** JSONL (12 tests) ; 7 phrases, 14 candidats ;
  la banque reçoit déjà des validations réelles ; [`README`](../../tools/structures/README.md).
- **R13 — la tokenisation** : **close**, décision **octets** — BPE 512 +0,39 % (bruit), BPE
  1024 +4,09 %, anglais +4,22/+6,59 % à octets égaux ; fiche
  [`r13`](../../reports/rapport-r13-decision.md), spécification
  [`tokenisation`](../implantation/tokenisation.md).
- **B10.2bis — décodeur** : 3×3 : **11,1** ; capacité 11,8 ; **mots 32,5** ;
  **JW 26,7** (plancher 17,1) ; `z` 1,5–2,6 points ; **contrastif négatif** ; fiches
  [`b102bis`](../../reports/rapport-b102bis-decodeur.md), [`mots`](../../reports/rapport-b10-decodeur-mots.md), [`mots-jw`](../../reports/rapport-b10-mots-jw.md).
- **A8.0 : 19** ; **A8.3b refusé** (lot) ; **A8.3c/d** : lot 1≠≥2, ctx stable, threads
  innocents — fiches [`a83`](../../reports/rapport-a83-defaut.md), [`a83b`](../../reports/rapport-a83b-regimes.md), [`a83c`](../../reports/rapport-a83c-lot.md), [`a83d`](../../reports/rapport-a83d-lot-threads.md).
- **B11.10** : **hybride 4/4** — codec **161/161**, ambiguïtés refusées ; **69,3 %** natif ;
  [`b1110`](../../reports/rapport-b1110-cartes.md).
- **N2.h — close** : corpus dédupliqué (**0 %** de fuite), chaîne propre **3,09** en domaine,
  diversité (÷ 4,3 hors dépôt), longueur (14,11 → 3,25 à 256), combinaison et capacité ; **N2.i**
  (4,84 Mo) : **12,93** littérature, **33,83** anglais — généralise sans relever le domaine ; **N2.j**
  (**186 Mo** de Wikipédia) : **7,42** / **12,41**, filtre non ambigu sans effet ; **N2.k**
  (**10 langues**, 237 Mo) : fr **5,68** (à données égales **3,62**), anglais **6,30**, chinois
  **9,65**. Fiches
  [`n2-propre`](../../reports/rapport-n2-propre.md) · [`n2-corpus-elargi`](../../reports/rapport-n2-corpus-elargi.md) ·
  [`n2-corpus-reel`](../../reports/rapport-n2-corpus-reel.md) ·
  [`n2-multilingue`](../../reports/rapport-n2-multilingue.md). N4 **0/40**.
- **Pensée — state store v0** : théorie (10 tours, 9 schémas) et **state store v0** (6/6 portes
  T0–T4 ; BFS, greedy, A*, MCTS-lite ; jouet des cruches) ; fiche
  [`pensee-v0`](../../reports/rapport-pensee-v0.md) ; prochaine : AC-3, alpha-bêta, DRVF, banc anytime.


## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **81** (75 vertes, 4 rouges à la passe du 31/10 19 h 42 ; 2 ajoutées depuis) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **386** / **472** | `reports/*.md` / `reports/*.json` |
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
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : AC-3/alpha-bêta 8/8** | **B11.10 close** ; **B13 : DRVF, banc** ; B10.3 bloquée |
| **N — le natif** | **N3, N4** | N2.h close ; N2 < 2,5 non atteinte ; N4 0/4 ; N5 gelé | **N2 close** ; **N4** (consigne) |
| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** (398 langues) ; R1/R2/R3 attendent N5/N4 | **R1.1/R1.2** (contexte natif) |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

> **P — la pensée** (session `e181ce02`) : RSN plurielle, arbre, moteur N3 ; fichiers réservés ;
> ni GPU ni `toutes-les-portes.sh`.

**Les sept chantiers C** — **C1** corpus · **C2** traduction · **C3** restitution · **C4**
styles · **C5** domaines · **C6** documentation · **C7** pensée — hors graphe, mesurés, du récit.

## Ce qui reste
- **Chantiers — la vue d'ensemble** : huit chantiers (A/B/N/R/**S**/**L**/**D**/B13) et leurs relations ; doc [`chantiers`](chantiers.md), carte [`chantiers-vision.svg`](../schemas/chantiers-vision.svg).

**N2.h** — **close** (N2.i : 12,93 littérature, 33,83 anglais ; porte < 2,5 non atteinte) ;
**Pensée** — **DRVF, banc anytime** (AC-3/alpha-bêta faits ; session `e181ce02`) ; **N4** — la consigne
courte ; **B10.3** — le `z` et l'encodeur ; **R4.4** — close, limites nommées ; **R0.7** — gold/neuronal ; **R1.1/R1.2** — le contexte natif ; **S** — l'export au corpus.

- **Le plan de travail multi-sessions** : [`plan-travail`](plan-travail.md) — quatre sessions (N2, L, S, D/R/A) + le hub, les territoires, la cadence, la surveillance ; le pont entre cet état et la roadmap.

## Les questions ouvertes

- **R1** : **1 000 octets** sans refaire 130–256 ? → **R1.1** (état de section) puis **R1.2**
  (curriculum) tranchent ; la hiérarchie de N2 est écartée.
- **N2** : la porte **< 2,5** est-elle la bonne, après N2.h (**3,09** en domaine, **12,93** en littérature) ? →
  la **roadmap N** tranche.
- **N4** : une **consigne courte** tient-elle hors du vu ? → **N4** tranche (0/4 tenus).
- **B10.3** : chrF **> 39,6** ? → **B10.3** (attention croisée) tranche.
- **Pensée** : le **DRVF** rejoue-t-il le moteur, et le banc anytime bat-il le greedy ? →
  le **v0 suivant** tranche.

## La carte

- **Méthode** : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md).
- **Plan** : [roadmap.md](roadmap.md) · [backlog](backlog/index.md) · [graphe](backlog/dependances.md) ·
  [carte](../theorie/carte.md) · [inventaire](../README.md).
- **Preuves** : [reports/](../../reports/) · [journal/](../../journal/) ·
  [état transféré](../../journal/2026-10-29/etat-transfere.md).

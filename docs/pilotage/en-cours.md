# En ce moment

**Mis à jour : 2026-11-02, 07 h 05 HNE (heure locale, EST).**

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
- **Plan** : 1) ~~RSN plurielle, arbre, cycle~~ ; 2) ~~portefeuille, contrat, anytime~~ ; 3) ~~state store v0 (6/6 portes)~~ ; 4) ~~moteur v0 (BFS, greedy, A*, MCTS-lite)~~ ; 5) ~~AC-3, alpha-bêta~~ (**8/8**) ; ~~DRVF~~ (**9/9**) ; 6) ~~banc anytime~~ (**10/10**) ; 6 bis) ~~opérateurs~~ (**15/15**) ; 7) ~~reprise R4.4~~ ; 8) ~~couche heuristique~~ ; 9) **bloc linguistique** (R0.7).
- **Ambition** : un **runtime cognitif** où penser est une recherche tracée sur des états pluriels, avec des opérateurs hétérogènes.
- **Stratégie** : théorie d'abord, puis un **v0 petit et mesuré** ; réserver les fichiers ; ne pas toucher aux GPU de N2.
- **Objectif final** : un **moteur de pensée v0 exécutable** — state store, arbre, A*/MCTS/AC-3, trace/rejeu, banc avec contrôles — documenté, mesuré, committé.
- **Reprise** : **R4.4** — note de clôture des trois limites (fax 1 bit, exposant fusionné,
  parité réelle sans questions) ; **S** est actif dans une autre TUI (export pragmatique, 11 tests).
- **Coloration** : analyse [`pre-traitement-linguistique`](../theorie/pre-traitement-linguistique.md)
  (5 schémas) — CPU étiquette
  cascade
- **Bloc** : **R0.7** — contrat [`bloc-linguistique`](../implantation/bloc-linguistique.md)
  (9 niveaux) ; **398 langues à 0,9687** ; fiche et porte.
- **Moteur B13** : **AC-3/alpha-bêta**, **DRVF**, **banc**, **opérateurs 98** ; fiches
  [`pensee-croyance`](../../reports/rapport-pensee-croyance.md), [`pensee-observatrice`](../../reports/rapport-pensee-observatrice.md),
  [`pensee-bayes`](../../reports/rapport-pensee-bayes.md), [`pensee-derive`](../../reports/rapport-pensee-derive.md),
  [`pensee-rupture`](../../reports/rapport-pensee-rupture.md), [`pensee-alternance`](../../reports/rapport-pensee-alternance.md),
  [`pensee-correction`](../../reports/rapport-pensee-correction.md), [`pensee-audit`](../../reports/rapport-pensee-audit.md).
- **Gold 360** : **200 + 160 synthétiques** ; POS **0,772** (fermé 0,939/ouvert 0,621),
  syntagmes exacts **0,194**/**tête 0,560**, pragmatique **0,994–1,0** ; cascade (mock) ; **attachement tête 1,0/0,966/0,932** (59 ambiguës), hasard 0,015 ; neuronal
  **refusé** ; fiche [`pensee-gold`](../../reports/rapport-pensee-gold-linguistique.md) ; prochain :
  **lecture du gold + modèle qualifié**.
- **Ce qu'elle fait** : **state store v0** écrit et testé — **6/6 portes**  sur le jouet des cruches ; BFS, greedy, A* et
  MCTS-lite ; puis **AC-3 et alpha-bêta** (8/8 ; 1 495/296 contre 18 730) ; fiches
  [`pensee-v0`](../../reports/rapport-pensee-v0.md) et
  [`pensee-ac3-alphabeta`](../../reports/rapport-pensee-ac3-alphabeta.md).
- **Ce que font les autres** : **N2.h** et **R4.4** sont **closes** ; **S** (le banc de structures)
  avance ; **N4** en file ; **A/B** gardent les leurs.
- **Interfaces** : `State`, `Proposal`, `Score`, `Decision`, `Trace` ; un opérateur est un bloc `state → state`.
- **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`, `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`, `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`, `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`, `tools/porte-bloc-linguistique.sh`, `tools/tests/linguistique/`, `docs/implantation/bloc-linguistique.md`, `docs/schemas/bloc-linguistique-*.svg`, `reports/bloc-*`, `journal/sessions/e181ce02-…/`.
- **Prochaine action** : **L** — 200+ ; **B13** — DRVM.
- **Bloquants** : aucun ; corpus de test à choisir ; pas de GPU.
- **Journal** : [le 31/10](../../journal/2026-10-31/README.md) · [le 01/11](../../journal/2026-11-01/README.md) · [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

> **Sessions archivées** : `8156fdcb`, `c3d0f0bd`, `N2-GPU`, `71d57f53`, `0b69f616`, `22e518ee`,
> `0b0a6a0d` (N2.h/N2.i, close) et `fe3c05f0` (R4.4, close ; restes nommés : fax 1 bit,
> exposant fusionné, parité réelle sans questions) — rapports dans [`journal/sessions/`](../../journal/sessions/).

### Session `fe3c05f0-834b-44f2-8739-501865d652c1` — D/R/A : les données, le lecteur, le moteur

- **Id** : `fe3c05f0-834b-44f2-8739-501865d652c1` — [`plan.md`](../../journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md).
- **Rôle** : **D/R/A** — le texte intégral, l'extraction PDF/OCR, la prépa R1.1/R1.2, A2.6/A8.3.
- **Plan** : le texte intégral, le PDF, l'OCR.
- **Ambition** : le français réel.
- **Stratégie** : le dump, débaliseur.
- **Objectif final** : 10 corpus, ficés.
- **Ce qu'elle fait** : le **texte intégral** : les **10** (**20,53 M** ; 8 Ko 0) ; **PDF** (1 927 doc., 322 Mo) ; **Documents** (3 384 doc., 872 M car. ; 8 Ko 2,07 %) ; **OCR** 20 livres (7 381 p, 15,36 M car. ; 1 784 fenêtres 8 Ko train + 115 val, 8 Ko 0 ; éval 0/40, 0/24, 0/40) ; **genres** mesurés (OCR **38,5** car/ligne) ; fiche [`wiki`](../../reports/rapport-corpus-wiki-texte.md).
- **Ce que font les autres** : Pensée, S, N2.
- **Prochaine action** : l'**OCR complet** (les 159 scans ; le pilote des 20 livres est clos) ; la clôture de la session à 8 h ; les collections.
- **Bloquants** : aucun.
- **Journal** : [le 01/11](../../journal/2026-11-01/README.md).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; **R0.4/R0.5 closes (négatifs)** ; R0.6 **12/20** au pilote, **7/7** à la porte ; fiches [`r04`](../../reports/rapport-r04-tete-survol.md), [`r07`](../../reports/rapport-r07-routeur.md), [`r06`](../../reports/rapport-r06-publication.md).
- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 au mélange intérieur, ×62,7 tout ; fiches [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../reports/rapport-typoglycemie.md).
- **Données** : inventaire local (Wikipédia **132 Go**, documents **~228 Go**, DRM et vidéos exclus) ; **corpus par langue** (10) : **21,6 M articles**, **31,4 G caractères**, **38,8 Go**, **0 fuite** — fiches [`inventaire-donnees`](../../reports/inventaire-donnees-entrainement.md), [`corpus-wikipedia`](../../reports/rapport-corpus-wikipedia.md).
- **S — le banc de structures** : outil web (`tools/structures`), générateur (**subordonnées**, **coordination**), pragmatique (double sens, niveaux 0–4), **export corpus** (15 tests) ; 7 phrases ; [`README`](../../tools/structures/README.md).
- **R13 — la tokenisation** : **close**, décision **octets** — BPE 512 +0,39 %, 1024 +4,09 % ; fiche [`r13`](../../reports/rapport-r13-decision.md).
- **B10.2bis — décodeur** : 3×3 **11,1** ; capacité 11,8 ; **mots 32,5** ; **JW 26,7** ; `z` 1,5–2,6 ; fiches [`b102bis`](../../reports/rapport-b102bis-decodeur.md), [`mots`](../../reports/rapport-b10-decodeur-mots.md), [`mots-jw`](../../reports/rapport-b10-mots-jw.md).
- **A8** : **A8.0 : 19** ; **A8.3b refusé** (lot) ; **A8.3c/d** : lot 1≠≥2, threads innocents ; fiches [`a83`](../../reports/rapport-a83-defaut.md), [`a83b`](../../reports/rapport-a83b-regimes.md), [`a83c`](../../reports/rapport-a83c-lot.md), [`a83d`](../../reports/rapport-a83d-lot-threads.md).
- **B11.10** : **hybride 4/4** — codec **161/161**, ambiguïtés refusées ; **69,3 %** natif ;
  [`b1110`](../../reports/rapport-b1110-cartes.md).
- **N2** : **N2.h** 3,09 ; **N2.j** 7,42 ; **N2.n** 3,94 ; **N2.o** 5,41 ; **N2.p** 4,00 ; **N2.q** 5,89 ; **N2.t** 5,58 ; **N2.r** 3,69 ; **N2.v** multi 34 M distillé **4,79** ; **S** : 7/7 séquences, 94 % ; **N2.w** : **3,77** ; **N2.z** : canal 34,3 M **3,53** (2 graines) ; **N2.y** : canal + KD 3,53 ; N4 **0/40** ; fiches
  [`n2-propre`](../../reports/rapport-n2-propre.md), [`n2-anglais`](../../reports/rapport-n2-anglais.md), [`n2-canal`](../../reports/rapport-n2-canal.md).
- **Pensée — state store v0** : 6/6 portes (BFS, greedy, A*, MCTS-lite), jouet des cruches ; fiche [`pensee-v0`](../../reports/rapport-pensee-v0.md) ; prochaine AC-3, alpha-bêta, DRVF.


## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **81** (77 vertes, 4 rouges — les connues — à la passe du 02/11 00 h 03) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **504** / **591** | `reports/*.md` / `reports/*.json` |
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
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : AC-3/alpha-bêta 8/8, DRVF 9/9, banc 10/10, opérateurs 98** | **B11.10 close** ; **B13 : DRVM/native** ; B10.3 bloquée |
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
**Pensée** — **DRVM/L** (AC-3/alpha-bêta/DRVF/banc/opérateurs/gold 180/attachement faits ; session `e181ce02`) ; **N4** — la consigne
courte ; **B10.3** — le `z` et l'encodeur ; **R4.4** — close, limites nommées ; **R0.7** — gold/neuronal ; **R1.1/R1.2** — le contexte natif ; **S** — l'export au corpus.

- **Vue d'ensemble** : huit chantiers et relations [`chantiers`](chantiers.md) ; plan multi-sessions [`plan-travail`](plan-travail.md) ; carte [`chantiers-vision.svg`](../schemas/chantiers-vision.svg).

## Les questions ouvertes

- **R1** : **1 000 octets** sans refaire 130–256 ? → **R1.1** (état de section) puis **R1.2**
  (curriculum) tranchent ; la hiérarchie de N2 est écartée.
- **N2** : la porte **< 2,5** est-elle la bonne, après N2.h (**3,09** en domaine, **12,93** en littérature) ? →
  la **roadmap N** tranche.
- **N4** : une **consigne courte** tient-elle hors du vu ? → **N4** tranche (0/4 tenus).
- **B10.3** : chrF **> 39,6** ? → **B10.3** (attention croisée) tranche.
- **Pensée** : l'A* = greedy sur ces scores ; un score 0/1 et un opérateur hétérogène les séparent-ils ? →
  le **v0 suivant** tranche.

## La carte

- **Méthode** : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md).
- **Plan** : [roadmap.md](roadmap.md) · [backlog](backlog/index.md) · [graphe](backlog/dependances.md) ·
  [carte](../theorie/carte.md) · [inventaire](../README.md).
- **Preuves** : [reports/](../../reports/) · [journal/](../../journal/) ·
  [état transféré](../../journal/2026-10-29/etat-transfere.md).

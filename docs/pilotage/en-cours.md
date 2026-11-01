# En ce moment

**Mis à jour : 2026-11-01, 00 h 25 HAE (heure locale, EST).**

> **État courant, pas histoire.** Une sous-section par **session active**, une ligne par **chantier**
> avec son **bloquant**. Méthode : [`methode/`](../methode/) (contexte, continuité). Résultats :
> [`reports/`](../../reports/). Histoire : [`journal/`](../../journal/). Plan : [`roadmap.md`](roadmap.md).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session qui trouve l'état en retard
> le corrige.

### Session `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — N2.h, le mètre propre

- **Id** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — [`plan.md`](../../journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md).
- **Rôle** : **N2.h — le mètre propre** : corpus, distillation, évaluation.
- **Plan** : 1) `tools/corpus_propre.py` (dédup, split par chunks) ; 2) chaîne propre (professeur 23,5 M, base 20k, distillation 20k × 3, curriculum 129 × 3) ; 3) porte honnête + hors domaine + décomposition ; 4) diversité FR 50/50 ; 5) verrou de longueur 129→512 × 3 ; 6) fiches, portes, commit.
- **Ambition** : sortir N2 du chiffre contaminé (**2,85** sur **32,8 %**) et donner à R un modèle qui lit du français général ; trancher le verrou de longueur.
- **Stratégie** : un seul changement à la fois, trois graines, contrôle par permutation, le corpus d'abord.
- **Objectif final** : un **mètre honnête** — corpus dédupliqué (0 % de validation dans l'entraînement), chaîne refaite, porte < 2,5 redéfinie, généralité et verrou tranchés.
- **Ce qu'elle fait** : corpus propre, chaîne refaite, diversité et longueur mesurées (3 fiches).
- **Résultat** (3 graines) : la chaîne propre vaut **3,09** en domaine (3,20 au test) — pas 2,85
  — et **16,70** sur la littérature jamais vue ; la **diversité** la ramène à **3,86** (÷ 4,3) et
  l'anglais de **57,6** à **25,7** pour **+0,17** ; les **positions aléatoires** font passer 256
  octets de **14,11** à **3,25** et 512 de **32,41** à **5,93** ; la base supervisée vaut **12,29**
  hors domaine : **la distillation spécialise**. Fiches `n2-propre`, `n2-diversite`, `n2-longueur`.
- **Ce que font les autres** : **Pensée** et **R4.4** sans GPU ; **N4** en file ; **A/B** gardent leurs fichiers.
- **Fichiers réservés** : `data/`, `tools/corpus*`, `tools/eval_n2_propre.py`, `tools/distiller_budget.py`, `reports/n2-*`, `work/n2h/`, `journal/sessions/0b0a6a0d-…/`.
- **Prochaine action** : clôture — journal, roadmap, portes, commit.
- **Bloquants** : aucun — GPU rendus.
- **Journal** : [le 31/10](../../journal/2026-10-31/README.md) · [le 01/11](../../journal/2026-11-01/README.md) · [la session](../../journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/).

### Session `fe3c05f0-834b-44f2-8739-501865d652c1` — R4.4, les scans

- **Id** : `fe3c05f0-…` — [`plan.md`](../../journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md).
- **Rôle** : **R4.4 — les scans** (CPU).
- **Plan** : corpus ✅, prétraitement ✅, exposants ✅, colonnes/tables ✅, porte `porte-ocr-scans` ✅, fiche ✅.
- **Ambition** : l'OCR comme **bloc classique robuste**, jugé par la **parité**.
- **Stratégie** : brut d'abord, n'ajouter que ce qui paie, dev pour régler, test pour trancher.
- **Objectif final** : **R4.4 mesurée** ; restent **scans réels de bout en bout**, **fax**, **exposant fusionné**.
- **Ce qu'elle fait** : photo **55,9 → 6,7 %**, préservation **70–87 %**, colonnes **89,4 → 0,5 %**, tableaux **92,6 %**, vrais scans **7,10 / 88,4 %** (trois livres) ; redressement utile **≤ 6°** (10° : **43 %**) — [`r44-scans`](../../reports/rapport-r44-scans.md).
- **Ce que font les autres** : N2.h a les GPU ; ne pas toucher `work/r44/`, `work/ocr/`, `reports/r44-*`.
- **Prochaine action** : **fax** 1 bit et **exposant fusionné**.
- **Bloquants** : aucun — pas de scanner réel ; scans **simulés**, écrit.
- **Journal** : [le 31/10](../../journal/2026-10-31/README.md).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN plurielle, arbre d'états, moteur N3.
- **Plan** : 1) ~~RSN plurielle, arbre, cycle~~ ; 2) ~~portefeuille, contrat, anytime~~ ; 3) **state store** typé ; 4) **moteur v0** (frontière, A*/MCTS/AC-3, trace) ; 5) **banc anytime** (AUC, regret, justification, rejeu) ; 6) intégration DRVM/DRVF.
- **Ambition** : un **runtime cognitif** où penser est une recherche tracée sur des états pluriels, avec des opérateurs hétérogènes.
- **Stratégie** : théorie d'abord, puis un **v0 petit et mesuré** ; réserver les fichiers ; ne pas toucher aux GPU de N2.
- **Objectif final** : un **moteur de pensée v0 exécutable** — state store, arbre, A*/MCTS/AC-3, trace/rejeu, banc avec contrôles — documenté, mesuré, committé.
- **Ce qu'elle fait** : doc `pensee-iterative.md` (10 tours, 9 schémas), pointeurs ; prochaine étape : state store.
- **Ce que font les autres** : **N2.h** et **R4.4** gardent leurs fichiers ; **N4** en file ; **A/B** gardent les leurs.
- **Interfaces** : `State`, `Proposal`, `Score`, `Decision`, `Trace` ; un opérateur est un bloc `state → state`.
- **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`, `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`, `journal/sessions/e181ce02-…/`.
- **Prochaine action** : le state store v0 (candidats, hash Merkle, arbre, trace) ; le contrat est écrit.
- **Bloquants** : aucun ; corpus de test à choisir ; pas de GPU.
- **Journal** : [le 31/10](../../journal/2026-10-31/README.md) · [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

> **Sessions archivées** : `8156fdcb`, `c3d0f0bd`, `N2-GPU`, `71d57f53`, `0b69f616`, `22e518ee`,
> `0b0a6a0d` (N2.d) — rapports dans [`journal/sessions/`](../../journal/sessions/).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; **R0.4 close (négatif)** ; **R0.5 close
  (négatif)** ; R0.6 **12/20** au pilote, **7/7** à la porte. Fiches
  [`r04`](../../reports/rapport-r04-tete-survol.md), [`r07`](../../reports/rapport-r07-routeur.md),
  [`r06`](../../reports/rapport-r06-publication.md) (cascade à confiance **publiée**).
- **R4.1–R4.3 — les blocs structurels** : **mesurées** — 996 cellules/802, 294 fichiers/24,
  32 formules/10 dérivées, **miroir 34/34, 296/296, 42/42** ; **R4.4** est **mesurée sur scans
  simulés** — photo **55,9 → 6,7 %**, préservation **70–87 %**, colonnes **89,4 → 0,5 %**,
  tableaux **92,6 %**, vrais scans **7,10 / 88,4 %** (trois livres) ; fiche [`r44-scans`](../../reports/rapport-r44-scans.md).
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
- **N2.h — le mètre propre** : corpus dédupliqué (**0 %** de fuite), chaîne propre **3,09** en
  domaine, diversité (÷ 4,3 hors dépôt) et longueur (14,11 → 3,25 à 256) mesurées ; fiches
  [`n2-propre`](../../reports/rapport-n2-propre.md) · [`n2-diversite`](../../reports/rapport-n2-diversite.md) · [`n2-longueur`](../../reports/rapport-n2-longueur.md). N4 **0/40**.
- **Pensée — RSN plurielle** : doc `pensee-iterative.md` (10 tours, 9 schémas) ; le **state store
  v0** est la prochaine action ; fichiers réservés dans la session `e181ce02`.


## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **80** (75 vertes, 4 rouges à la passe du 31/10 19 h 42 ; 1 ajoutée depuis) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **375** / **453** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **114** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 39** (31/10 19 h 42) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Les dépendances vivent dans le graphe** ([`dependances.md`](backlog/dependances.md) §5, schéma
[`backlog-dependances.svg`](../schemas/backlog-dependances.svg)), recalculé par
`tools/verifie_backlog.py`. Cette table ne garde que les **bloquants externes** et la **prochaine
action** — pas les statuts, qui dérivent. Vue d'ensemble :
[**la carte de décision**](../schemas/chantiers-decision.svg).

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | aucune | B1.5 corpus ; B10.3 attend un encodeur | **B11.10 close** ; B10.3 bloquée |
| **N — le natif** | **N2, N3, N4** | N2 < 2,5 ; validation **contaminée (32,8 %)** ; N4 0/4 ; N5 gelé | **N2** (le corpus décontaminé) ; **N4** (consigne) |
| **R — le lecteur** | aucune | R4.4 : scans réels de bout en bout, fax | **R4.4 mesurée sur scans simulés** ; R1/R2/R3 attendent N2 |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

> **P — la pensée** (session `e181ce02`) : RSN plurielle, arbre, moteur N3 ; fichiers réservés ;
> ni GPU ni `toutes-les-portes.sh`.

**Les sept chantiers C** — **C1** corpus · **C2** traduction · **C3** restitution · **C4**
styles · **C5** domaines · **C6** documentation · **C7** pensée — hors graphe, mesurés, du récit.

## Ce qui reste

**N2.h** — le **corpus propre** et la porte honnête (en cours) ; **Pensée** — le **state store v0**
et le moteur N3 (session `e181ce02`) ; **N4** — la consigne courte ; **B10.3** — le `z` et
l'encodeur ; **R4.4** — les scans réels.

## Les questions ouvertes

- **R1** : **1 000 octets** sans refaire 130–256 ? → **R1.1** (état de section) puis **R1.2**
  (curriculum) tranchent ; la hiérarchie de N2 est écartée.
- **N2** : **< 2,5** — et **sur quel jeu** ? La validation se recopie (32,8 % verbatim) →
  le **split par document** tranche.
- **N4** : une **consigne courte** tient-elle hors du vu ? → **N4** tranche (0/4 tenus).
- **B10.3** : chrF **> 39,6** ? → **B10.3** (attention croisée) tranche.
- **Pensée** : un état pluriel se rejoue-t-il à l'identique, et une stratégie se substitue-t-elle ? →
  le **state store v0** et le banc anytime tranchent.

## La carte

- **Méthode** : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md).
- **Plan** : [roadmap.md](roadmap.md) · [backlog](backlog/index.md) · [graphe](backlog/dependances.md) ·
  [carte](../theorie/carte.md) · [inventaire](../README.md).
- **Preuves** : [reports/](../../reports/) · [journal/](../../journal/) ·
  [état transféré](../../journal/2026-10-29/etat-transfere.md).

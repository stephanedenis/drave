# En ce moment

**Mis à jour : 2026-11-02, 16 h 50 HNE (heure locale, EST).**

> **État courant, pas histoire.** Une sous-section par **session active**, une ligne par **chantier**
> avec son **bloquant**. Méthode : [`methode/`](../methode/) (contexte, continuité). Résultats :
> [`reports/`](../../reports/). Histoire : [`journal/`](../../journal/). Plan : [`roadmap.md`](roadmap.md).
>
> **Reprise après le reboot du 02/11 15 h 06** : les deux sessions sont **en pause**, leurs cycles
> sont committés, les GPU sont sains ; reprise par `dsh --profile dsh-tui --resume <id>` ; runbook
> dans [`plan-travail.md`](plan-travail.md) § 9.

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.

### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise

- **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
- **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
- **Plan** : 1) ~~audit~~ ; 2) ~~commits B13/D/N2~~ ; 3) ~~état~~ ; 4) **mandats** ; 5) **porte stricte** ; 6) **INDEX** ; 7) **runbook**.
- **Ambition** : un état reprenable, des mandats qui disent la vérité.
- **Stratégie** : committer par flux avec `git add` explicite, nommer ce qui reste.
- **Objectif final** : sédimentation à zéro, mandats explicites (N2, S, L/B13, D/R/A), runbook.
- **Ce qu'elle fait** : audit des 111 sessions ; commits B13 **140/140**, D (OCR/glossaire), N2.ac ; sessions en pause ; porte stricte ; INDEX.
- **Ce que font les autres** : `e181ce02` et `fe3c05f0` en pause ; N2 et S sans session.
- **Prochaine action** : la **passe de portes** (1 h 46) quand la machine est libre ; suivre les sessions ouvertes.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN plurielle, arbre d'états, moteur N3 ; R4.4 ; heuristique ; bloc linguistique.
- **Plan** : 1–6) ~~moteur B13~~ (state store, AC-3/alpha-bêta, DRVF, banc, opérateurs) ; 7) ~~R4.4~~ ; 8) ~~heuristique~~ ; 9) ~~bloc linguistique~~ ; 10) ~~coréférence/absences~~ (**140/140**).
- **Ambition** : un **runtime cognitif** où penser est une recherche tracée sur des états pluriels.
- **Stratégie** : v0 petit et mesuré, fichiers réservés, GPU de N2 intacts.
- **Objectif final** : un **moteur de pensée v0 exécutable**, documenté, mesuré, committé.
- **Reprise** : **R4.4** — trois limites nommées (fax 1 bit, exposant fusionné, parité sans questions).
- **Bloc** : **R0.7** — [`bloc-linguistique`](../implantation/bloc-linguistique.md), 9 niveaux ; **398 langues à 0,9687**.
- **Moteur B13** : AC-3/alpha-bêta, DRVF, banc, opérateurs 109 ; **140/140** (T137 : 5 sans antécédent, 0 lien ; 116 liens = 51 intra + 65 inter) ; [`pensee-vrais-absents`](../../reports/rapport-pensee-vrais-absents.md).
- **Gold** : **432 réels + 160 synthétiques + 20** ; POS **0,765** ; coréférence **116 liens**, bilan **27/30**, CV **0,847 ± 0,051**, κ **1,0** ; neuronal **refusé** ; [`pensee-gold`](../../reports/rapport-pensee-gold-linguistique.md).
- **Ce qu'elle fait** : B13 (DRVF, banc, opérateurs, coréférence **140/140**), gold **432** ; le cycle est committé.
- **Ce que font les autres** : **N2.ac** production ; **D** OCR/glossaire ; **S** hors DSH ; **A/B**.
- **Fichiers réservés** : `pensee-iterative`, `moteur-de-pensee`, `tools/pensee/`, `reports/pensee-*`, `tools/tests/linguistique/`.
- **Prochaine action** : **gold neuronal** (modèle local) ; **DRVM/native** bloqué.
- **Bloquants** : **neuronal réel bloqué** (`llama-cli`, taggers, poids) ; le mock reste un contrat.
- **Arrêt** : 02/11 15 h 06, trace 14 h 40 ; **en pause** ; `dsh --profile dsh-tui --resume e181ce02-cd50-488a-a6be-e84b79d40dcc`.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `fe3c05f0-834b-44f2-8739-501865d652c1` — D/R/A : les données, le lecteur, le moteur

- **Id** : `fe3c05f0-834b-44f2-8739-501865d652c1` — [`plan.md`](../../journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md).
- **Rôle** : **D/R/A** — texte intégral, PDF/OCR, prépa R1.1/R1.2, A2.6/A8.3.
- **Plan** : texte intégral, PDF, OCR, glossaire, docwatch.
- **Ambition** : le français réel.
- **Stratégie** : dump, débaliseur, OCR page à page, glossaire au rendu.
- **Objectif final** : 10 corpus, ficés.
- **Ce qu'elle fait** : texte intégral 10 (**20,53 M** ; 8 Ko 0) ; PDF 1 927/322 Mo ; Documents 3 384/872 M ; OCR 20 livres (7 381 p, 15,36 M) ; **OCR CEGEP** 10 notes (1 596 p, 2,52 M) ; genres **38,5** ; glossaire 335 + 20 ; docwatch **1,5 px** ; [`ocr-cegep`](../../reports/rapport-ocr-cegep.md).
- **Ce que font les autres** : Pensée (140/140), N2 (N2.ac), S (hors DSH).
- **Prochaine action** : **OCR ~127 scans CEGEP** ; clôture ; R1.1/R1.2 après N2, A2.6 après A6.2.
- **Bloquants** : aucun.
- **Arrêt** : 02/11 15 h 06, trace 13 h 25 ; **en pause** ; `dsh --profile dsh-tui --resume fe3c05f0-834b-44f2-8739-501865d652c1`.
- **Journal** : [le 02/11](../../journal/2026-11-02/README.md).

> **Sessions archivées** : `8156fdcb`, `c3d0f0bd`, `N2-GPU`, `71d57f53`, `0b69f616`, `22e518ee`,
> `0b0a6a0d` (N2.h close), `b6a672ec` (GPU/reboot, close) — [`journal/sessions/`](../../journal/sessions/).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; **R0.4/R0.5 closes (négatifs)** ; R0.6 **12/20** au pilote, **7/7** à la porte ; fiches [`r04`](../../reports/rapport-r04-tete-survol.md), [`r07`](../../reports/rapport-r07-routeur.md), [`r06`](../../reports/rapport-r06-publication.md).
- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 au mélange intérieur, ×62,7 tout ; fiches [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../reports/rapport-typoglycemie.md).
- **Données** : inventaire local (Wikipédia **132 Go**, documents **~228 Go**) ; **10 corpus** (**21,6 M art.**, **31,4 G car.**, **38,8 Go**, **0 fuite**) ; **OCR CEGEP** 10 notes, 1 596 p ; **glossaire** 355 entrées — fiches [`inventaire`](../../reports/inventaire-donnees-entrainement.md), [`corpus-wikipedia`](../../reports/rapport-corpus-wikipedia.md).
- **S — le banc de structures** : outil web (`tools/structures`), générateur, pragmatique (niveaux 0–4), export ; analyseur **7/7** séquences, **93,9 %** de couverture, **19 tests** ; [`analyseur`](../../reports/rapport-s-analyseur.md). **Aucune session DSH**.
- **N2** : **N2.ac** (mélange **1,02 Go**, 60 k pas) : **3,49** domaine, **6,03** littérature,
  **8,34** anglais, **9,05** wikitext2 — **le modèle de production** ; **N2.z** 3,53 ; **N2.w**
  3,77 ; N4 **0/40** ; fiches [`n2-canaux`](../../reports/rapport-n2-canal-34m.md),
  [`n2-1go`](../../reports/rapport-n2-corpus-1go.md).
- **Pensée — B13** : state store v0, AC-3/alpha-bêta, DRVF, banc, opérateurs, **140/140** ; gold
  **432 réels**, coréférence **116 liens** (51 intra, 65 inter), **0 absent**, 5 phrases sans
  antécédent ; fiches [`pensee-vrais-absents`](../../reports/rapport-pensee-vrais-absents.md),
  [`pensee-anaphore-bilan`](../../reports/rapport-pensee-anaphore-bilan.md).

## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **81** (76 vertes, 5 rouges à la passe du 02/11 06 h : les 4 connues + greffe à la borne 700 s, rejouée verte à 1200 s) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **550** / **636** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **119** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **02/11 06 h** (81 portes, 76/5 ; 5e rejouée verte à 1200 s) · durée mesurée **1 h 46** (01/11) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Les dépendances vivent dans le graphe** ([`dependances.md`](backlog/dependances.md) §5, schéma
[`backlog-dependances.svg`](../schemas/backlog-dependances.svg)), recalculé par
`tools/verifie_backlog.py`. Cette table ne garde que les **bloquants externes** et la **prochaine
action** — pas les statuts, qui dérivent. Vue d'ensemble :
[**la carte de décision**](../schemas/chantiers-decision.svg).

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 140/140, gold 432, 116 liens** | **B13 : DRVM/native (bloqué)** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N3, N4** | N2 : **N2.ac 1 Go — 3,49 domaine / 6,03 littérature** ; < 2,5 non atteinte ; N4 0/4 ; N5 gelé | **N2** : 200 k pas sur le mélange, puis **R1.1/R1.2** ; **N4** |
| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** (398 langues) ; R1/R2/R3 attendent N5/N4 | **R1.1/R1.2** (contexte natif) |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

> **N2 et S n'ont pas de session active** : N2.ac vient de `0b0a6a0d` (plan terminé) ; S vit dans
> `tools/structures`. **P** (`e181ce02`) est **en pause**.

**Les sept chantiers C** — **C1** corpus · **C2** traduction · **C3** restitution · **C4**
styles · **C5** domaines · **C6** documentation · **C7** pensée — hors graphe, mesurés, du récit.

## Ce qui reste

**N2** — N2.ac (1 Go) est le modèle de production ; reste **200 k pas** et la fenêtre **R1.1/R1.2** ;
**Pensée** — **DRVM/L** (140/140, gold 432, 116 liens ; neuronal bloqué ; session `e181ce02` en pause) ;
**N4** — la consigne courte ; **B10.3** — le `z` et l'encodeur ; **R4.4** — close, limites nommées ;
**R0.7** — gold/neuronal ; **R1.1/R1.2** — le contexte natif ; **S** — l'export au corpus, sans session.

- **Vue d'ensemble** : huit chantiers et relations [`chantiers`](chantiers.md) ; plan multi-sessions [`plan-travail`](plan-travail.md) ; carte [`chantiers-vision.svg`](../schemas/chantiers-vision.svg).

## Les questions ouvertes

- **R1** : **1 000 octets** sans refaire 130–256 ? → **R1.1** (état de section) puis **R1.2** (curriculum) tranchent ; la hiérarchie de N2 est écartée.
- **N2** : les **200 k pas** sur le mélange 1 Go font-ils passer **< 2,5** sans perdre le français ? → N2 tranche (N2.ac : 3,49 domaine, 6,03 littérature).
- **N4** : une **consigne courte** tient-elle hors du vu ? → **N4** tranche (0/4 tenus).
- **B10.3** : chrF **> 39,6** ? → **B10.3** (attention croisée) tranche.
- **Pensée** : l'**absence** est-elle annotable (5 phrases, 0 lien) ou faut-il la laisser au gold ? → le **v0 suivant** tranche.

## La carte

- **Méthode** : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md).
- **Plan** : [roadmap.md](roadmap.md) · [backlog](backlog/index.md) · [graphe](backlog/dependances.md) ·
  [carte](../theorie/carte.md) · [inventaire](../README.md).
- **Preuves** : [reports/](../../reports/) · [journal/](../../journal/) ·
  [état transféré](../../journal/2026-10-29/etat-transfere.md).

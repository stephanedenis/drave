# En ce moment

**Mis à jour : 2026-10-31, 18 h 15 HAE (heure locale, EDT).**

> **État courant, pas histoire.** Une sous-section par **session active** ; une ligne par **chantier** avec son
> **bloquant**. Les détails de méthode sont dans [`methode/`](../methode/) — chargement et budget dans
> [`contexte.md`](../methode/contexte.md), contrat des sessions dans [`continuite.md`](../methode/continuite.md).
> Les résultats sont dans [`reports/`](../../reports/) ; l'histoire dans
> [`journal/`](../../journal/) ; le plan dans [`roadmap.md`](roadmap.md).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session qui trouve l'état en retard
> le corrige.

### Session `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — N2.h, le mètre propre

- **Id** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — plan et journal dans
  [`journal/sessions/0b0a6a0d-…/`](../../journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md).
- **Rôle** : **N2.h — le mètre propre**, mandat libre de 10 h (nuit du 31/10 au 1/11).
- **Objectif final** : donner à la ligne N2 un **mètre honnête** — corpus dédupliqué et split
  sans fuite, chaîne refaite dessus, porte < 2,5 **redéfinie** sur ce jeu — puis trancher ce
  qu'aucun chiffre contaminé ne pouvait trancher : la **généralité** et le **verrou de longueur**.
- **Plan** : 1) `tools/corpus_propre.py` : dédup par shingles, split par chunks, **0 %** de
  contamination vérifiée ; 2) chaîne propre — professeur 23,5 M, base 20 000 pas, distillation
  20 000 pas × 3 graines, curriculum 129 × 3 ; 3) **porte honnête** + profil hors domaine
  (littérature, anglais, wikitext2) et décomposition (têtes précoces, pensée) ; 4) **diversité
  française** — moitié dépôt, moitié littérature, × 3 graines : ce que la généralité coûte ;
  5) **verrou de longueur** — courbe 129→512 et positions aléatoires × 3 ; 6) fiches, portes, commit.
- **Stratégie** : un seul changement à la fois, trois graines, contrôle par permutation, et **le
  corpus d'abord** — un levier mesuré sur un mètre faux ne vaut rien.
- **Ambition** : sortir N2 du chiffre qui flattait (**2,85** sur un jeu contaminé à **32,8 %**),
  donner à R un modèle qui lit du **français général**, et trancher le verrou de longueur par une
  expérience, pas par un vœu.
- **Ce qu'elle fait** : campagne GPU (2 cartes) ; points de contrôle dans `work/n2h/`, archivés
  ensuite sur deux disques.
- **Ce que font les autres** : **R4.4** (scans réels) et les docs continuent en parallèle ; ne
  pas lancer `tools/toutes-les-portes.sh` tant que les GPU tournent, ni toucher `data/`,
  `tools/corpus*`, `reports/n2-*` ; cette page : une session à la fois.
- **Fichiers réservés** : `data/`, `tools/corpus*`, `tools/eval_n2_propre.py`, `reports/n2-*`,
  `work/n2h/`, `journal/sessions/0b0a6a0d-…/`.
- **Prochaine action** : attendre la distillation A (3 graines) puis évaluer la porte honnête.
- **Bloquants** : aucun — GPU occupés jusqu'à ~1 h 40.
- **Journal** : [le 31/10](../../journal/2026-10-31/README.md).

> **Sessions archivées** : `8156fdcb`, `c3d0f0bd`, `N2-GPU`, `71d57f53`, `0b69f616`, `22e518ee`,
> `fe3c05f0`, `0b0a6a0d` (N2.d) — rapports dans [`journal/sessions/`](../../journal/sessions/).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; **R0.4 close (négatif)** ; **R0.5 close
  (négatif)** ; R0.6 **12/20** au pilote, **7/7** à la porte. Fiches
  [`r04`](../../reports/rapport-r04-tete-survol.md), [`r07`](../../reports/rapport-r07-routeur.md),
  [`r06`](../../reports/rapport-r06-publication.md) (cascade à confiance **publiée**).
- **R4.1–R4.3 — les blocs structurels** : **mesurées** — 996 cellules/802, 294 fichiers/24,
  32 formules/10 dérivées, **miroir 34/34, 296/296, 42/42** ; fiches
  [`r41`](../../reports/rapport-r41-bloc-tableaux.md), [`r42`](../../reports/rapport-r42-bloc-code.md),
  [`r43`](../../reports/rapport-r43-bloc-maths.md), [`miroir`](../../reports/rapport-miroir-blocs.md).
  **R4.4 partielle** : OCR installé sans root, **10 pages rendues** à **WER 4,48 %** et
  **parité 90 %** ; page dégradée **26,7 %** ; fiche [`r44`](../../reports/rapport-r44-ocr-pilote.md).
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
- **Backlog — graphe** : 37 fiches, 43 arêtes, **4 à la frontière** ; `tools/verifie_backlog.py`.
- **N2** : GPU ; **N2.d** — le budget plein (20 000 pas, 41 Mo, 3 graines) paie
  **2,9355 → 2,8527** ; les quatre sources coûtent **+0,9064** (professeur français, 82,5 %
  anglais, quotas égaux **3,4350**) ; le curriculum 129 gagne **0,0416**
  à 129. **La validation n'est pas tenue à l'écart : 32,8 % des fenêtres du protocole sont
  verbatim dans l'entraînement** — sur fenêtres propres, A est à **2,9795** et le témoin de
  5 000 pas à **3,0534** ; **2,6998 est mesuré sur le même jeu contaminé**. Fiche
  [`n2-budget`](../../reports/rapport-n2-budget.md). Suite : **corpus dédupliqué et split par
  document**, puis la porte ; la capacité attend. N4 **0/40**.

## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **79** (75 vertes, 4 rouges à la passe du 31/10 19 h 42) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **371** / **441** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **113** (hors archive et README) | `docs/**/*.md` |
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
| **R — le lecteur** | aucune | R4.4 : scans réels, layout, exposants | **R4.4 partielle** (scans réels) ; R1/R2/R3 attendent N2 |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 43 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

**Les sept chantiers C** (hors graphe, transférés au journal) : **C1** corpus · **C2**
traduction · **C3** restitution · **C4** styles (date à contrôler) · **C5** domaines · **C6**
documentation · **C7** pensée — mesurés, et désormais du récit, pas du plan.

## Ce qui reste

**N2** — le **corpus propre** et la porte honnête (N2.h, en cours) ; **N4** — la consigne
courte ; **B10.3** — le `z` et l'encodeur ; **R4.4** — les scans réels.
**Bloqués** : A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE local), B1.5 (corpus).

## Les questions ouvertes

- **R1** : **1 000 octets** sans refaire 130–256 ? → **R1.1** (état de section) puis **R1.2**
  (curriculum) tranchent ; la hiérarchie de N2 est écartée.
- **N2** : **< 2,5** — et **sur quel jeu** ? La validation se recopie (32,8 % verbatim) →
  le **split par document** tranche.
- **N4** : une **consigne courte** tient-elle hors du vu ? → **N4** tranche (0/4 tenus).
- **B10.3** : chrF **> 39,6** ? → **B10.3** (attention croisée) tranche.
- **Backlog** : graphe sans cycle ni arête morte ? → `tools/verifie_backlog.py` tranche.

## La carte

- **Méthode** : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md).
- **Plan** : [roadmap.md](roadmap.md) · [backlog](backlog/index.md) · [graphe](backlog/dependances.md) ·
  [carte](../theorie/carte.md) · [inventaire](../README.md).
- **Preuves** : [reports/](../../reports/) · [journal/](../../journal/) ·
  [état transféré](../../journal/2026-10-29/etat-transfere.md).

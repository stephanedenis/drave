# En ce moment

**Mis à jour : 2026-10-29, 09 h 20 HAE (heure locale, EDT).**

> **État courant, pas histoire.** Une sous-section par **session active** ; une ligne par **chantier** avec son
> **bloquant**. Les détails de méthode sont dans [`methode/`](../methode/) — chargement et budget dans
> [`contexte.md`](../methode/contexte.md), contrat des sessions dans [`continuite.md`](../methode/continuite.md).
> Les résultats sont dans [`reports/`](../../reports/) ; l'histoire et les sessions terminées dans
> [`journal/`](../../journal/). Le plan est [`roadmap.md`](roadmap.md) ; les fiches dans
> [`backlog/index.md`](backlog/index.md).

## Sessions en cours

> Contrat et budget : [`continuite.md`](../methode/continuite.md) ; sessions terminées :
> [`journal/sessions/`](../../journal/sessions/).

### Session `f0969e87` — principale : état, docs, R0

- **Id** : `f0969e87-af0c-43b1-93cf-f278d9c90846`.
- **Rôle** : tenir l'état, la roadmap et l'analyse ; préparer R0 (lecteur v0) sur CPU.
- **Ce qu'elle fait** : R0.1 (graphe de document) est **mesuré** — 51 pages, fidélité **1,000** ;
  la suite est R0.3 (banc complet) ;
  l'ordre est **strict**.
- **Ce que font les autres** : `8156fdcb` tient le **graphe du backlog** et ses fiches ; `N2-GPU` distille ;
  elles rendent un **diff d'état**, la principale applique.
- **Prochaine action** : **N0.3b** en parallèle ; R0.2 est **mesuré** par `8156fdcb` (récupération 1,000 à 30 %).
- **Bloquants** : aucun pour R0 ; N0.3b dépend de la parité DRVM ↔ GGUF ; N2 dépend du GPU.
- **Journal** : [index des sessions](../../journal/README.md#sessions) · [jour](../../journal/2026-10-29/README.md).

### Session `8156fdcb` — backlog livré, puis R0.2 (contrôleur de lecture)

- **Id** : `8156fdcb-5033-4ba4-a5f3-f8a078e6e57e`.
- **Rôle** : graphe du backlog (livré : 41 arêtes, 3 plafonds, 8 lignes sans fiche) ; **R0.1** livré
  (51 pages, fidélité 1,000) ; **R0.2** mesuré le 29/10.
- **Ce qu'elle fait** : R0.2 — contrôleur classique (survol, balayage, lecture, relecture, arrêt),
  budget en **octets**, trace rejouable ; banc **pilote** de 5 types. Récupération **1,000** à 30 %.
- **Ce que font les autres** : `f0969e87` tient l'état et prend N0.3b ; `N2-GPU` distille la hiérarchie ;
  elles rendent un **diff d'état**.
- **Fichiers réservés** : `tools/lecteur_controleur.py`, `tools/banc_lecture.py`, `tools/porte-lecteur.sh`,
  `docs/implantation/lecteur-controleur.md`, `docs/implantation/banc-lecture.md`, `reports/r02-*`,
  `docs/pilotage/backlog/R02-controleur-lecture.md`, `R03-banc-lecture-rapide.md`.
- **Prochaine action** : **R0.3** — le banc complet (30 documents, 300 questions), et un **modèle**
  pour savoir si le plafond de 25–75 % est celui du lecteur extractif ou du document.
- **Bloquants** : aucun ; le pilote est extractif classique, sans modèle externe.
- **Journal** : commit `4ffa34b7` (R0.1) · [docs du jour](../../journal/2026-10-29/docs.md) · [sessions](../../journal/README.md#sessions).

### Session `N2-GPU` — calcul : distillation

- **Id** : aucun Id DSH (job GPU lancé par la session principale).
- **Rôle** : N2 — professeur et distillation ; ne touche ni aux docs ni aux fiches.
- **Ce qu'elle fait** : 49 999 fenêtres, 4 sources ; professeur 30k ; student 20k–30k ; mesure de PPL.
- **Ce que font les autres** : `f0969e87` prépare R0 et tient l'état ; `8156fdcb` tient le graphe du backlog.
- **Prochaine action** : N2 — la **hiérarchie** (état de section), porte **< 2,5** (meilleur **2,6998**, plateau **2,708**) ; **N5 gelé**.
- **Bloquants** : GPU occupé ; les contextes 130/136/160/256 sont négatifs ; le corpus est à 4 sources.
- **Journal** : [mesures du jour](../../journal/2026-10-29/mesures.md).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1 **mesurée** (51 pages) et R0.2 **mesuré** (récupération 1,000 à 30 %, 5 types) ;
  R0.3 en **pilote** (20 questions) ; aucun bloquant.
- **Backlog — graphe** : 41 arêtes dures, 3 plafonds, 8 lignes sans fiche ; vérifié par `tools/verifie_backlog.py`.
- **N2 — distillation** : GPU ; plateau **2,708** ; porte **< 2,5** non atteinte.
- **Documentation** : roadmap unique A/B/N/R ; **90 documents** ; glossaire **famille 12** (27 termes) ;
  éléments terminés transférés au journal.

## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **51** (49 vertes, 2 rouges structurelles) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **275** / **339** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **93** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 40** (28/10 00 h 12) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

| chantier | état | bloquant | prochaine action |
|---|---|---|---|
| **A — le moteur** | ✅ A1–A8 ; A2.6/A3.2/A3.3 ouverts | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | A2.6, A3.2/A3.3 ; A8.3 en opt-in |
| **B — l'intelligence** | ✅ B1–B12 ; B10.3/B12.10 ouverts | B10.3 décodeur sous le plancher ; B1.5 corpus | B12.10, puis B10.3 |
| **N — le natif** | N0/N1 mesurés ; N2 plateau ; N4 partiel | N2 **< 2,5** non atteint ; N4 **0/4** tenus ; N5 gelé | N0.3b ; N2 (hiérarchie) ; N4 (consigne) |
| **R — le lecteur** | 🔬 R0.1 mesuré (51 pages) ; R01 prête | aucun pour R0 ; R1 dépend de R01 et N2 | R0.2 → R0.3 |
| **C1–C7** | ✅ corpus, traduction, restitution, styles, domaines, documentation, pensée | C4 date à contrôler ; le reste est hors plan | transférés au journal |
| **Backlog — graphe** | 29 fiches ; 41 arêtes dures | 8 lignes sans fiche ; priorités arrêtées | vérifier le graphe (`8156fdcb`) |

**C1** corpus · **C2** traduction · **C3** restitution · **C4** styles · **C5** domaines ·
**C6** documentation · **C7** pensée : ✅ mesurés ; détail dans
[`etat-transfere.md`](../../journal/2026-10-29/etat-transfere.md).

## Ce qui reste

**R0** — **R0.1 mesuré** ; R0.2 → R0.3 (non bloqué). **N0.3b** — parité DRVM ↔ GGUF. **N2** — la **hiérarchie** ; **N5 gelé**.
**N4** — SFT tenu à l'écart. **B10.3** — décodeur (bloqué). **B12.10** — intégration.
**Backlog** — graphe et fiches (`8156fdcb`).
**Bloqués** : A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE local), B1.5 (corpus).

## Les questions ouvertes

- **R0** : **90 %** à **30 %** du coût ? → **R0.3** (banc) tranche.
- **R1** : **1 000 octets** sans refaire 130–256 ? → **N2** (hiérarchie), puis **R1.1**, tranchent.
- **N2** : **< 2,5** ? → **N2** (la hiérarchie) tranche.
- **B10.3** : chrF **> 39,6** ? → **B10.3** (attention croisée) tranche.
- **Backlog** : graphe sans cycle ni arête morte ? → `tools/verifie_backlog.py` tranche.

## La carte

- **Méthode** : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
  [résultats](../methode/resultats.md) · [portes](../methode/portes.md).
- **Plan** : [roadmap.md](roadmap.md) · [backlog](backlog/index.md) · [graphe](backlog/dependances.md) ·
  [carte](../theorie/carte.md) · [inventaire](../README.md).
- **Preuves** : [reports/](../../reports/) · [journal/](../../journal/) ·
  [état transféré](../../journal/2026-10-29/etat-transfere.md).

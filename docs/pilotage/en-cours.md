# En ce moment

**Mis à jour : 2026-10-30, 13 h 00 HAE (heure locale, EDT).**

> **État courant, pas histoire.** Une sous-section par **session active** ; une ligne par **chantier** avec son
> **bloquant**. Les détails de méthode sont dans [`methode/`](../methode/) — chargement et budget dans
> [`contexte.md`](../methode/contexte.md), contrat des sessions dans [`continuite.md`](../methode/continuite.md).
> Les résultats sont dans [`reports/`](../../reports/) ; l'histoire dans
> [`journal/`](../../journal/) ; le plan dans [`roadmap.md`](roadmap.md).

## Sessions en cours

> Contrat et budget : [`continuite.md`](../methode/continuite.md) ; sessions terminées :
> [`journal/sessions/`](../../journal/sessions/).

> **Plan d'abord.** Chaque session active expose son mandat dans
> [`journal/sessions/`](../../journal/sessions/) (`<id>/plan.md`) ; `python3 tools/sessions.py --status`
> avant d'écrire ici.

> **Écriture.** Toute session écrit l'état, **une à la fois** : un commit est atomique, et
> aucun fait (`reports/`, roadmap, backlog) ne se commite sans sa ligne. La garantie est au
> commit, pas dans un rôle : `tools/verifie_etat_a_jour.py` refuse le commit (hook
> `pre-commit`) et la porte `porte-etat.sh` compare les commits. Une session qui trouve
> l'état en retard le corrige — elle n'attend pas qu'on désigne une « principale ».

### Session `8156fdcb` — R0.1–R0.5 (lecteur)

- **Id** : `8156fdcb-5033-4ba4-a5f3-f8a078e6e57e`.
- **Rôle** : graphe du backlog (livré), **R0.1–R0.3 mesurés** ; **R0.4** (pilote négatif) et
  **R0.5** (routeur) ouverts.
- **Ce qu'elle fait** : cascade à confiance **publiée** (`tools/calibrer.py`, fichiers datés,
  `--calibration`) : out-of-sample 0,894 (oracle) / 0,366 (au-dessus des deux fixes).
- **Ce que font les autres** : `71d57f53` A8.0/B11.10 ; `N2-GPU` N2 ; `c3d0f0bd` R4.2.
- **Fichiers réservés** : `tools/lecteur_modele.py`, `tools/routeur.py`, `reports/r03-*`, `reports/r07-*`.
- **Prochaine action** : la boucle de lecture (R11, dépend de N2) ou la restitution (R31, dépend
  de R21) — toutes deux hors R0 ; sinon consolidation.
- **Bloquants** : aucun ; le GPU 0 lit à 1 409 t/s de prompt, le GPU 1 reste à N2.
- **Journal** : commits `4ffa34b7` (R0.1), `08149617` (R0.2) · [docs du jour](../../journal/2026-10-29/docs.md).

### Session `c3d0f0bd` — R4, B10.2bis, A8.3b

- **Id** : `c3d0f0bd-e344-4600-a023-0ed50d25b48b`.
- **Rôle** : **R4.1–R4.3**, **B10.2bis** et **A8.3b** mesurées (`7fb1c8a6`, `4ccf641f`, ce cycle).
- **Ce qu'elle fait** : blocs R4.1–R4.3, miroir ; B10.2bis ; **décodeur mot** ; A8.3b.
- **Ce que font les autres** : `8156fdcb` R0.5 ; `N2-GPU` N2 ; `71d57f53` A8.0/B11.10.
- **Fichiers réservés** : `tools/bloc_*.py`, `tools/porte-bloc-*.sh`, `tools/tests/tableaux/`,
  `tools/tests/code/`, `tools/tests/maths/`, `reports/r4*`, `docs/implantation/bloc-*.md`.
- **Prochaine action** : **B10.2bis** suite (encodeur) ; **A8.3b** ; **R4.4 bloqué**.
- **Bloquants** : aucun.
- **Journal** : [mesures du jour](../../journal/2026-10-29/mesures.md).

### Session `N2-GPU` — calcul : distillation

- **Id** : aucun Id DSH (job GPU, hors session).
- **Rôle** : N2 — professeur et distillation ; ne touche ni aux docs ni aux fiches.
- **Ce qu'elle fait** : 49 999 fenêtres, 4 sources ; professeur 30k ; student 20k–30k.
- **Ce que font les autres** : `71d57f53` A8.0/B11.10 ; `8156fdcb` R0.5 ; `c3d0f0bd` R4.2.
- **Prochaine action** : N2 — la **hiérarchie** (état de section), porte **< 2,5** (meilleur **2,6998**, plateau **2,708**) ; **N5 gelé**.
- **Bloquants** : GPU occupé ; les contextes 130/136/160/256 sont négatifs ; le corpus est à 4 sources.
- **Journal** : [mesures du jour](../../journal/2026-10-29/mesures.md).

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; R0.4 **négatif**, R0.5 **signal** (AUC 0,785) ; suite **R0.4**.
- **R4.1–R4.3 — les blocs structurels** : **mesurées** — 996 cellules/802, 294 fichiers/24,
  32 formules/10 dérivées, **miroir 34/34, 296/296, 42/42** ; fiches
  [`r41`](../../reports/rapport-r41-bloc-tableaux.md), [`r42`](../../reports/rapport-r42-bloc-code.md),
  [`r43`](../../reports/rapport-r43-bloc-maths.md), [`miroir`](../../reports/rapport-miroir-blocs.md).
- **B10.2bis — décodeur** : 3×3 : **11,1** ; capacité 11,8 ; **mots 32,5** ;
  **JW 26,7** (plancher 17,1) ; `z` 1,5–2,6 points ; **contrastif négatif** ; fiches [`b102bis`](../../reports/rapport-b102bis-decodeur.md), [`mots`](../../reports/rapport-b10-decodeur-mots.md), [`mots-jw`](../../reports/rapport-b10-mots-jw.md).
- **A8.0 : 19** ; **A8.3b refusé** (lot) ; **A8.3c** : lot 1≠≥2, ctx stable — fiches [`a83`](../../reports/rapport-a83-defaut.md), [`a83b`](../../reports/rapport-a83b-regimes.md), [`a83c`](../../reports/rapport-a83c-lot.md).
- **B11.10** : **hybride 4/4** — codec **161/161**, ambiguïtés refusées ; **69,3 %** natif ;
  [`b1110`](../../reports/rapport-b1110-cartes.md).
- **Backlog — graphe** : 42 arêtes, 1 sans fiche ; `tools/verifie_backlog.py`.
- **N2** : GPU ; meilleur **2,6998** ; porte **< 2,5** non atteinte ; N4 **0/40**.
  Suite : [journal/sessions/f0969e87…](../../journal/sessions/f0969e87-af0c-43b1-93cf-f278d9c90846.md).

## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **78** (61 vertes, 2 rouges, 15 hors passe) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **364** / **436** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **108** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 46** (29/10 22 h 09) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

| chantier | état | bloquant | prochaine action |
|---|---|---|---|
| **A — le moteur** | ✅ A1–A8 ; **A8.0/A8.3a : 19 portes** ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3 refusé, A8.3c expliqué** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (A6.2 bloqué) ; lot |
| **B — l'intelligence** | ✅ B1–B12 ; B10.3 ouvert ; **B12.10, B10.2bis closes** ; décodeur (32,5) | `z` ~2 points ; B1.5 corpus | **B11.10 hybride 4/4** ; B10.3 attend un **encodeur** |
| **N — le natif** | N0/N1 mesurés ; N0.3b **close** ; N2 plateau ; **N3.1/N3.2a/N3.2b0/N3.2b1/N3.2b2/N3.3a/N3.3b/N3.3c/N3.4a/N3.4b/N3.4c/N3.4d/N3.5a/N3.5b/N3.5c/N3.5d/N3.5e/N3.5f/N3.6** ; N4 partiel | N2 **< 2,5** non atteint ; N4 **0/4** tenus ; N5 gelé | N2 (hiérarchie) ; N4 (consigne) |
| **R — le lecteur** | 🔬 R0.1–R0.3 **mesurés** ; R0.4/R0.5 ouverts ; **R4.1–R4.3 mesurées** ; **R13 condition** | **R4.4 bloqué** (aucun OCR) ; R1 dépend de N1/N2 | **R0.4** (négatifs difficiles), **R0.5** (routeur) ; **R13.4** (2e graine) ; **R4.4 bloqué** |
| **C1–C7** | ✅ corpus, traduction, restitution, styles, domaines, documentation, pensée | C4 date à contrôler ; le reste est hors plan | transférés au journal |
| **Backlog — graphe** | **37 fiches ; 42 arêtes** | 1 sans fiche | vérifier le graphe (`8156fdcb`) |

```plantuml
@startwbs
scale 1.8
title Les chantiers — état au 30/10 13 h 00
* Drave
**[#c8e6c9] A — le moteur
***[#c8e6c9] A1–A8
***[#c8e6c9] A8.0/A8.3a — 19 portes
***[#c8e6c9] A8.3b/c
***[#ffe0b2] A2.6 — partiel
***[#ffcdd2] A3.4/A5.4/A6.2 — bloqués
**[#ffe0b2] B — l'intelligence
***[#c8e6c9] B1–B12
***[#c8e6c9] B10.2bis — close
***[#ffcdd2] B10.3 — attend un encodeur
***[#c8e6c9] B11.10 — 4/4
***[#e1bee7] B12.10 — négatif
**[#ffe0b2] N — le natif
***[#c8e6c9] N0/N1
***[#ffe0b2] N2 — 30 %
***[#c8e6c9] N3.6 — service ✅
***[#bbdefb] N4 — à faire
***[#e0e0e0] N5 — gelé
**[#ffe0b2] R — le lecteur
***[#c8e6c9] R0.1–R0.3
***[#c8e6c9] R4.1–R4.3
***[#ffe0b2] R0.5 — en cours
***[#ffcdd2] R4.4 — bloqué
** Sessions actives
*** 8156fdcb — R0.5 (cascade)
*** c3d0f0bd — B10.2bis/A8.3b
*** N2-GPU — N2
@endwbs
```

*Lecture : structure et états, sans axe de temps (en-cours se pilote à l'heure) ; vert = mesuré, rouge = bloqué.
Gantt (jours) dans la [roadmap](roadmap.md#le-gantt-indicatif), dépendances dans le [graphe](backlog/dependances.md).*

**C1** corpus · **C2** traduction · **C3** restitution · **C4** styles · **C5** domaines ·
**C6** documentation · **C7** pensée : ✅ mesurés ; détail dans
[`etat-transfere.md`](../../journal/2026-10-29/etat-transfere.md).

## Ce qui reste

**R0** — R0.1–R0.3 **mesurés**, R0.4/R0.5 ouverts ; **R4.1–R4.3** — **mesurées** ; **R4.4 bloqué** (aucun OCR). **N2** — la **hiérarchie**.
**N4** — SFT tenu à l'écart. **B10.3** — décodeur (bloqué).
**Bloqués** : A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE local), B1.5 (corpus).

## Les questions ouvertes

- **R0** : **90 %** à **30 %** du coût ? → R0.3 a tranché la **sélection** (1,000 ; paraphrase 0,30 contre 0,717) ;
  R0.4 (tête) et R0.5 (routeur) tranchent la **compréhension**.
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

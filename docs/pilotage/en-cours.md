# En ce moment

**Mis à jour : 2026-10-31, 18 h 15 HAE (heure locale, EDT).**

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

### Session à ouvrir — N2, le corpus décontaminé

- **Id** : aucune session active — `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` est **close** (la
  campagne N2.d est committée).
- **Rôle** : **N2, le corpus** — **32,8 %** des fenêtres de validation sont verbatim dans
  l'entraînement ; il faut dédupliquer et séparer train/validation **par document** avant que la
  porte < 2,5 ait un sens.
- **Ce qu'elle fait** : reconstruire `data/corpus_fr.txt` sans répétitions, un split par document,
  puis remesurer la base et le meilleur élève ; la porte sera **redéfinie** sur ce jeu-là.
- **Ce que font les autres** : **R4.4** (les scans réels) est ouverte et non bloquante ; **N4**
  (consigne courte) prend la file si N2 bloque.
- **Fichiers réservés** : `data/`, `tools/corpus*`, `reports/n2-*`, `journal/sessions/<id>/`.
- **Prochaine action** : le script de déduplication et le split par document.
- **Bloquants** : aucun côté N2 ; **R4.4** attend des scans, pas un blocage.
- **Journal** : [le 30/10](../../journal/2026-10-30/README.md) · [le 31/10](../../journal/2026-10-31/README.md).

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
| fichiers / JSON de résultats | **371** / **439** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **112** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 39** (31/10 19 h 42) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Les dépendances ne sont pas dans cette page.** Elles vivent dans le **graphe** du backlog —
[`backlog/dependances.md`](backlog/dependances.md) §5 pour la frontière, et le schéma
[`backlog-dependances.svg`](../schemas/backlog-dependances.svg) — recalculé par
`python3 tools/verifie_backlog.py`, qui confronte aussi les statuts des fiches et de l'index.
Cette table ne garde que les **bloquants externes** (ce que le graphe ne peut pas dire : une
ressource qui manque) et la **prochaine action** ; elle ne recopie pas les statuts, qui dérivent.
La vue d'ensemble est la **[carte de décision](../schemas/chantiers-decision.svg)** : quatre
couloirs, la profondeur de dépendance comme axe (jamais le temps), la frontière en vert et les
sources de blocage nommées.

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

**R0** — R0.1–R0.6 **mesurés** ; **R0.4/R0.5 closes en négatif** ; **R4.4 partielle** (OCR, scans réels à faire).
**N2** — la **hiérarchie** et les **données** sont écartées ; le **budget** paie **−0,08** ; la
**validation est contaminée à 32,8 %** — le prochain pas est le **corpus**, pas l'entraînement. **N4** — la **consigne
courte**. **B10.3** — le `z` et l'encodeur.
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

# En ce moment

**Mis à jour : 2026-10-31, 11 h 21 HAE (heure locale, EDT).**

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

### Session `22e518ee-81b8-4081-ae1b-f0d7a777a1d7` — clôture des sessions inachevées

- **Id** : `22e518ee-81b8-4081-ae1b-f0d7a777a1d7`.
- **Rôle** : **session unique** — terminer proprement les sessions inachevées avant toute ligne
  du backlog : résultats committés, archives, plans, journal, état.
- **Ce qu'elle fait** : `0b69f616` (R0.4, R0.5, R13) est **close et committée** ; les mandats
  `8156fdcb`, `c3d0f0bd`, `N2-GPU` et la coordination `71d57f53` sont **archivés** dans
  `journal/sessions/<id>/` (rapport + digest) ; l'outillage lit désormais les traces
  `session.v4.jsonl.zstd` (le glob ne couvrait que l'ancien nom — d'où les archives manquantes).
- **Ce que font les autres** : personne — **session unique**.
- **Fichiers réservés** : `tools/archive_sessions.py`, `tools/session_report.py`,
  `tools/journal_auto.py`, `journal/sessions/`, `journal/2026-10-30/README.md`,
  `journal/2026-10-31/`, `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`,
  `reports/INDEX.md`, `docs/pilotage/backlog/`.
- **Prochaine action** : commit de clôture (portes, revue, journal) ; ensuite **N2** (la
  hiérarchie) ou **N4** (consigne courte) — les GPU sont libres.
- **Bloquants** : aucun ; **R4.4** reste bloqué (aucun OCR installé).
- **Journal** : [le 30/10](../../journal/2026-10-30/README.md) · [le 31/10](../../journal/2026-10-31/README.md).

> **Sessions archivées** : `8156fdcb` (R0.1–R0.5), `c3d0f0bd` (R4, B10.2bis, A8.3b),
> `N2-GPU` (distillation native), `71d57f53` (coordination), `0b69f616` (R0.4, R0.5, R13) —
> rapports dans [`journal/sessions/`](../../journal/sessions/) et récit dans le journal du jour.

## Ce qui est en cours

- **R0 — lecteur v0** : R0.1–R0.3 **mesurés** ; **R0.4 close (négatif)** ; **R0.5 close
  (négatif)** ; R0.6 **12/20** au pilote, **7/7** à la porte. Fiches
  [`r04`](../../reports/rapport-r04-tete-survol.md), [`r07`](../../reports/rapport-r07-routeur.md),
  [`r06`](../../reports/rapport-r06-publication.md) (cascade à confiance **publiée**).
- **R4.1–R4.3 — les blocs structurels** : **mesurées** — 996 cellules/802, 294 fichiers/24,
  32 formules/10 dérivées, **miroir 34/34, 296/296, 42/42** ; fiches
  [`r41`](../../reports/rapport-r41-bloc-tableaux.md), [`r42`](../../reports/rapport-r42-bloc-code.md),
  [`r43`](../../reports/rapport-r43-bloc-maths.md), [`miroir`](../../reports/rapport-miroir-blocs.md).
  **R4.4 bloqué** (aucun OCR).
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
- **Backlog — graphe** : 37 fiches, 42 arêtes, **4 à la frontière** ; `tools/verifie_backlog.py`.
- **N2** : GPU ; meilleur **2,6998** ; porte **< 2,5** non atteinte ; N4 **0/40**.
  Suite : [la clôture de la session `f0969e87`](../../journal/sessions/f0969e87-af0c-43b1-93cf-f278d9c90846/cloture.md).

## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **78** (61 vertes, 2 rouges, 15 hors passe) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **367** / **435** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **109** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 46** (29/10 22 h 09) | `docs/pilotage/references-non-regression.md` |

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
| **N — le natif** | **N2, N3, N4** | N2 < 2,5 ; N4 0/4 ; N5 gelé | **N2** (hiérarchie) ; **N4** (consigne) |
| **R — le lecteur** | aucune | R4.4 (aucun OCR) | **R4.4 bloqué** ; R1/R2/R3 attendent N2 |
| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |
| **Backlog — graphe** | **37 fiches, 42 arêtes, 4 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |

**Les sept chantiers C** (hors graphe, transférés au journal) : **C1** corpus · **C2**
traduction · **C3** restitution · **C4** styles (date à contrôler) · **C5** domaines · **C6**
documentation · **C7** pensée — mesurés, et désormais du récit, pas du plan.

## Ce qui reste

**R0** — R0.1–R0.6 **mesurés** ; **R0.4/R0.5 closes en négatif** ; **R4.4 bloqué** (aucun OCR).
**N2** — la **hiérarchie** ; **N4** — la **consigne courte**. **B10.3** — le `z` et l'encodeur.
**Bloqués** : A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE local), B1.5 (corpus).

## Les questions ouvertes

- **R1** : **1 000 octets** sans refaire 130–256 ? → **N2** (hiérarchie), puis **R1.1**, tranchent.
- **N2** : **< 2,5** ? → **N2** (la hiérarchie) tranche.
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

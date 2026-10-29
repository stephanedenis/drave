# 2026-10-29 — Documentation, état, conventions

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (14)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:52 | `7afd909a` | DOCS — EN-COURS DATÉ DU 2026-10-29, 01 H 52 | `en-cours.md`, `README.md`, `mesures.md` (+1) |
| 04:01 | `8ec49f6a` | DOCS — N2.24 : COMPTEURS ET LIGNE ROADMAP | `en-cours.md`, `README.md`, `mesures.md` (+1) |
| 04:03 | `e8ea9852` | DOCS — ROADMAP N2.7–N2.24 ET ENTRÉES README | `roadmap-native.md`, `README.md`, `docs.md` (+1) |
| 04:06 | `53577daa` | DOCS — COMPTEURS 259/324 | `en-cours.md`, `README.md`, `mesures.md` (+1) |
| 04:23 | `87dfd1fc` | DOCS — COMPTEURS 260/325 | `en-cours.md`, `README.md`, `mesures.md` |
| 08:18 | `3b9162d1` | DOCS — UNE ROADMAP UNIQUE (A/B/N/R), ANALYSE LECTURE RAPIDE, BACKLOG 29 FICHES | `AGENTS.md`, `README.md`, `README.md` (+47) |
| 08:54 | `8bca0318` | DOCS — GRAPHE DES DÉPENDANCES DU BACKLOG (40 ARÊTES DURES, 4 PLAFONDS), 7 DÉFAUTS CORRIGÉS, VÉRIFIÉ PAR tools/verifie_backlog.py | `A3.4-colab.md`, `A5.4-fpga.md`, `A6.2-moe-local.md` (+30) |
| 09:02 | `9e569aec` | DOCS — EN-COURS MULTI-SESSIONS (3 SESSIONS), BLOQUANTS PAR CHANTIER, TRANSFERT AU JOURNAL | `contexte.md`, `continuite.md`, `en-cours.md` (+3) |
| 10:02 | `a7dd8473` | DOCS — GLOSSAIRE 12 (27 TERMES DE LECTURE), BACKLOG LIÉ AU GLOSSAIRE | `README.md`, `A3.4-colab.md`, `A5.4-fpga.md` (+75) |
| 14:11 | `076d15ef` | ÉTAT — LE GRAPHE DES CHANTIERS, ACTIVITÉS ET ÉTATS DANS EN-COURS | `en-cours.md`, `README.md`, `chantiers-etats.svg` (+3) |
| 14:41 | `7d47b3c7` | ÉTAT — LISTE DES FICHIERS RÉSERVÉS NETTOYÉE (R0.3 CLOS) | `en-cours.md`, `README.md`, `moteur.md` (+1) |
| 14:46 | `6e995187` | MÉTHODE — IDENTITÉ DSH, PAIRS ET DISCIPLINE GIT ; 71d57f53 INSCRIT | `AGENTS.md`, `continuite.md`, `en-cours.md` (+2) |
| 14:53 | `4767036b` | JOURNAL — R4.1 ENTRE AU RÉCIT DU JOUR (55 COMMITS) | `README.md`, `mesures.md` |
| 15:22 | `65ab24cf` | ÉTAT — R4.1 MESURÉE : 996 CELLULES, 802 EXACTES ; T0 À 3 993 | `index.md`, `en-cours.md`, `roadmap.md` (+3) |

## Mesures et rapports touchés

- [reports/README.md](../../reports/README.md)

<!-- notes -->
- **08 h 30 — une seule roadmap, et le lecteur entre au plan.** L'analyse `docs/theorie/lecture-rapide.md` ouvre le
  **programme R** ; `docs/pilotage/roadmap.md` devient le plan unique A/B/N/R, les anciens plans A/B et N sont
  archivés et liés ; `docs/pilotage/backlog/` reçoit **29 fiches** (19 R, 10 lignes ouvertes A/B/N). Aucun chiffre
  nouveau : les mesures citées sont celles des fiches existantes ; les compteurs passent à **88 documents**.
- **Ce qui reste ouvert** : R0.1/R0.2/R0.3 (lecteur v0), N0.3b (parité), N2 (porte < 2,5), N4 (SFT tenu à l'écart).
- **09 h 20 — l'état passe au pluriel et reste léger.** `en-cours` a désormais une section **Sessions en cours** avec
  une sous-section par session active (`f0969e87`, `8156fdcb`, `N2-GPU`), une table **chantiers × bloquants** et un
  transfert des éléments finis vers [`etat-transfere.md`](etat-transfere.md). Le contrôleur `verifie_en_cours.py`
  vérifie les sept champs de chaque session et refuse un bloquant vide.
- **09 h 40 — le backlog entre au glossaire.** Nouvelle **famille 12** (27 entrées) : lecture rapide, contrôleur,
  graphe de document, gist, span, closed-book, SFT, distillation, chrF, WER, F1, AUC, parseur, AST, CAS, OCR,
  layout, DRVM, contrôle négatif, graphe de dépendances, contrat, tableau, tenu à l'écart, banc de lecture. Chaque
  fiche du backlog porte une ligne **Glossaire** ; l'index du backlog renvoie à la famille 12. Le glossaire passe à
  **316 entrées** et `docs/` à **90 documents**.
<!-- /notes -->

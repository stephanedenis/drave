# 2026-10-24 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-24.md](2026-10-24.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (3)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 08:13 | `3c9665f1` | A1.5 — LA DECISION PAR COUCHE : la table (densites 20,1 a 56,3 %, croisement 22 %) et la verification — PPL identique (28,4015) entre le push et le dense, le dense 2 % plus rapide (9,2 contre 9,4 s a 255 jetons) ; la table predit le dense pour 23 couches sur 24, la mesure suit. Correction du « ~10 % » perime dans l'analyse du flux | `en-cours.md`, `roadmap.md`, `2026-10-22_moteur.md` (+5) |
| 08:43 | `7a956534` | B1.6 — LE CORPUS DIALOGUE TROUVE : DiaBLa (Bawden et al. 2021), 144 dialogues spontanes FR/EN, 4 910 paires avec les post-editions humaines ; extraction tools/corpus_diabla.py ; la mesure au 7 B est en file (GPU occupe par le 32 B). B1.5 (la prose scientifique) : la recherche ne trouve que des comparables, la ligne reste bloquee et nommee | `roadmap.md`, `2026-10-22_moteur.md`, `2026-10-24.md` (+4) |
| 08:46 | `fcabe8e9` | B2.8 — LE CORPUS NATUREL PLUS DUR TROUVE : DACCORD (1 034 paires FR de contradictions), RTE3-FR (2 x 800) et GQNLI-FR (300), plus durs que XNLI (Skandalis et al., LREC-COLING 2024) ; la mesure est en file, le GPU etant occupe par le 32 B | `roadmap.md`, `2026-10-22_moteur.md`, `2026-10-24.md` (+2) |

## Chiffres du jour

`1034 paires` · `4910 paires` · `56,3 %` · `22 %` · `2 %` · `10 %` · `9,4 s` · `255 jetons` · `23 couches` · `28,4015`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Mesures et rapports touchés

- [reports/README.md](../reports/README.md)
- [reports/rapport-analyse-flux.md](../reports/rapport-analyse-flux.md)
- [reports/rapport-decision-par-couche.md](../reports/rapport-decision-par-couche.md)

<!-- notes -->

<!-- /notes -->

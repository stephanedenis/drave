# 2026-10-15 — Attention, fenêtre, puits

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-15.md](2026-10-15.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (4)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:41 | `4123006b` | Le budget d'attention a-t-il une bonne taille par texte ? Le cout de la moitie varie de x180, un budget uniforme CASSE la tolerance sur 5 textes sur 8, et la politique par texte la tient pour -14,1 % de cles | `cerveau-facultes.md`, `references-non-regression.md`, `2026-10-15.md` (+5) |
| 01:42 | `db89e8be` | Le budget d'une DECISION : la profondeur est le seul levier lineaire (357,8 -> 119,3 -> 59,6 M paires pour 24/8/4 couches), et la fenetre d'attention ne deplace PAS cette metrique — deux monnaies, le plan n'en comptait qu'une | `cerveau-facultes.md`, `2026-10-15.md`, `2026-10-15_attention.md` (+3) |
| 02:10 | `e3fb38c4` | Aucun signal BON MARCHE ne predit la sensibilite au budget d'attention (correlations -0,019 et +0,096 sur huit textes) : la politique par texte exige DEUX passes, donc 2x le calcul pour -14,1 % de cles | `2026-10-15.md`, `2026-10-15_memoire.md`, `THEMES.md` (+1) |
| 14:02 | `000ec103` | POURQUOI les couches profondes ne se comparent pas : l'attention S'EFFONDRE (entropie 3,36 -> 0,16) et BASCULE d'un patch a l'autre — l'ecart est discret, pas un arrondi amplifie | `en-cours.md`, `main.rs`, `2026-10-15.md` (+2) |

## Chiffres du jour

`-14,1 %` · `0,019` · `0,096` · `4 couches`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Mesures et rapports touchés

- [reports/rapport-budget-decision.md](../reports/rapport-budget-decision.md)
- [reports/rapport-politique-budget-attention.md](../reports/rapport-politique-budget-attention.md)
- [reports/rapport-vision-qwen2vl.md](../reports/rapport-vision-qwen2vl.md)

<!-- notes -->

<!-- /notes -->

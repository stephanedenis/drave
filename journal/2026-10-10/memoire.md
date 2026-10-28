# 2026-10-10 — Mémoire épisodique, consolidation, greffe

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (18)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:03 | `d9d532f7` | C7 suite : le rejeu RÉPÉTÉ est un point fixe, pas une usure (erreur exactement 0,00e0) | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+4) |
| 01:32 | `b852b093` | C2/C6 : la greffe d'état — branchée, et elle ne transfère PAS le contexte | `sprint-cerveau.md`, `main.rs`, `model.rs` (+6) |
| 02:02 | `7a8cfb70` | C6 : un indice ÉTRANGER retrouve le bon passage — 136 jetons contre 448 de hasard | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+3) |
| 02:28 | `f537818f` | C6 : la porte de l'indice étranger CORRIGE la mesure — l'effet est réel, non robuste | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+3) |
| 04:08 | `52d49ec3` | Porte greffe : cas 5 réécrit — la greffe porte le CONTENU, pas seulement le 1er jeton | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 04:20 | `089c52a3` | C6/C2 : la mémoire QUI SERT, de bout en bout — et le goulot est le RAPPEL | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+3) |
| 04:56 | `b21f7158` | C6 : le rappel par le contenu dépend de l'INDICE, pas de la mémoire (8 indices mesurés) | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+3) |
| 05:12 | `7a688a7c` | C6 : le rappel n'est PAS continu — deux jetons voisins donnent 50 et 1 006 jetons | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 07:28 | `7869a126` | Etat reprenable consolide : trois chantiers avec leur premiere commande, et cinq corrections a ne pas reintroduire | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 14:19 | `e1a0e33c` | C8 peripherie : la tache fermee mesuree — le signal COURANT est dans la sortie (R2 0,913), sa MEMOIRE n'y est pas | `etat-cerveau.md`, `note-peripherie-c8.md`, `main.rs` (+11) |
| 14:42 | `eed13e81` | C8 peripherie : la memoire du signal n'est PAS dans l'etat — meme une lecture non lineaire ne la trouve pas | `etat-cerveau.md`, `2026-10-10.md`, `2026-10-10_apprentissage.md` (+16) |
| 17:32 | `7d72564e` | Note de peripherie C8 : la STRUCTURE de memoire, concue AVANT le code, avec ses quatre portes | `note-peripherie-c8.md`, `2026-10-10.md`, `2026-10-10_apprentissage.md` (+13) |
| 17:34 | `0302cf9b` | Etat : le renvoi vers la conception de la memoire de C8 (le patch precedent avait echoue sur un motif perime) | `etat-cerveau.md`, `2026-10-10.md`, `2026-10-10_docs.md` (+5) |
| 19:25 | `4d7a41e7` | C8 : la STRUCTURE de memoire est livree — la poursuite donne R2 1,000 et une erreur NULLE, pour zero paire de plus | `etat-cerveau.md`, `note-peripherie-c8.md`, `main.rs` (+12) |
| 20:07 | `e1028f94` | C2 : la recurrence est implementee, bornee, gratuite en paires — et elle NUIT (echo, pas memoire) | `etat-cerveau.md`, `plan-cerveau-complet.md`, `main.rs` (+11) |
| 20:09 | `b0703814` | C2 : la conception du CYCLE a deux regions, ecrite AVANT le code, avec ses cinq portes | `etat-cerveau.md`, `note-cycle-c2.md`, `2026-10-10.md` (+14) |
| 20:28 | `5f748214` | Passe du 20 h 28 : 26 vertes sur 26 (dont porte-memoire) — comptes mis a jour | `etat-cerveau.md`, `manques.md`, `2026-10-10.md` (+15) |
| 22:29 | `4ef58643` | Dessin H (profondeur routee) : la borne de l'oracle vaut 31 % des jetons, et le routeur n'est pas le facteur limitant | `etat-cerveau.md`, `manques.md`, `modele-pour-drave.md` (+21) |

## Chiffres du jour

`31 %` · `1,000` · `0,913` · `1006 jetons` · `136 jetons`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `d31b3d9b-58e4-4d34-85fa-381b6f6a6a76` — Où en est-on (début 2026-10-08 09:11, 71.0 h) → [rapport](../sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/rapport.md) · [digest](../sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md)

## Mesures et rapports touchés

- [reports/rapport-c2-recurrence.md](../../reports/rapport-c2-recurrence.md)
- [reports/rapport-c8-peripherie.md](../../reports/rapport-c8-peripherie.md)
- [reports/rapport-campagne-benefices.md](../../reports/rapport-campagne-benefices.md)
- [reports/rapport-design-H-profondeur-routee.md](../../reports/rapport-design-H-profondeur-routee.md)

<!-- notes -->
` … `
<!-- /notes -->

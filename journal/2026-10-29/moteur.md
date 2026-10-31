# 2026-10-29 — Moteur : chargement, calcul, listes, quantification

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (6)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 04:45 | `702e4dae` | FIX — VARS_LUES : DRAVE_TOKEN | `main.rs`, `README.md`, `mesures.md` (+1) |
| 04:53 | `0bf0297e` | N0.14 — PPL NATIVE 1 996 OCTETS : 54,0379, PYTHON 54,0343 | `en-cours.md`, `roadmap-native.md`, `main.rs` (+5) |
| 12:03 | `bc4e3d92` | N0.3b — PARITÉ PPL DRVM ↔ GGUF CLOSE : 68,1917 / 92,1875 (CONVERSION), 4,6585 / 18,6394 (NATIF) | `README.md`, `mesures.md`, `INDEX.md` (+3) |
| 13:56 | `acdfa987` | R0.3 — LE LECTEUR PASSE SUR GPU (1,9 S/APPEL) : CONTRÔLEUR 0,500, DÉBUT 0,400, HASARD 0,000 | `banc-lecture.md`, `R03-banc-lecture-rapide.md`, `en-cours.md` (+13) |
| 14:39 | `72a4ff5f` | R0.3 — 249 QUESTIONS, 30 DOCUMENTS SUR GPU : SÉLECTION 1,000 À 30 %, LE CONTRÔLEUR BAT LA TRONCATURE 5,5× | `banc-lecture.md`, `R03-banc-lecture-rapide.md`, `index.md` (+12) |
| 20:25 | `04357861` | N3.3c — LE MOTEUR COMPTE LES EXPERTS/CANAUX : 6/6/3 · 48/24/24 ; PORTE 63 | `N3-operations-natives.md`, `en-cours.md`, `roadmap.md` (+7) |

## Chiffres du jour

`30 %` · `1,000` · `0,500` · `0,400` · `0,000` · `68,1917` · `92,1875` · `4,6585` · `18,6394` · `54,0379` · `54,0343`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `1f9394fb-6435-4928-9a03-2b258e5a28c5` — — (début 2026-10-29 14:10, 0.0 h) → [rapport](../sessions/1f9394fb-6435-4928-9a03-2b258e5a28c5/rapport.md) · [digest](../sessions/1f9394fb-6435-4928-9a03-2b258e5a28c5/digest.md)
- `3de141c0-089b-4ceb-8a2e-bd6d83044a5f` — Tu travailles dans le dépôt (début 2026-10-29 11:32, 0.3 h) → [rapport](../sessions/3de141c0-089b-4ceb-8a2e-bd6d83044a5f/rapport.md) · [digest](../sessions/3de141c0-089b-4ceb-8a2e-bd6d83044a5f/digest.md)
- `4a342d0f-bf6c-433f-bac9-c5a960b89a7f` — Tu travailles dans le dépôt (début 2026-10-29 11:32, 0.2 h) → [rapport](../sessions/4a342d0f-bf6c-433f-bac9-c5a960b89a7f/rapport.md) · [digest](../sessions/4a342d0f-bf6c-433f-bac9-c5a960b89a7f/digest.md)
- `71d57f53-8b41-4220-84dd-7bb9eedc88d9` — Évaluation des techniques de lecture rapide pour Drave (début 2026-10-29 07:42, 29.9 h) → [rapport](../sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/rapport.md) · [digest](../sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/digest.md)
- `8156fdcb-5033-4ba4-a5f3-f8a078e6e57e` — Réviser roadmap et backlog, établir priorités (début 2026-10-29 08:40, 28.9 h) → [rapport](../sessions/8156fdcb-5033-4ba4-a5f3-f8a078e6e57e/rapport.md) · [digest](../sessions/8156fdcb-5033-4ba4-a5f3-f8a078e6e57e/digest.md)
- `c3d0f0bd-e344-4600-a023-0ed50d25b48b` — Chantier inactif à examiner (début 2026-10-29 14:37, 18.7 h) → [rapport](../sessions/c3d0f0bd-e344-4600-a023-0ed50d25b48b/rapport.md) · [digest](../sessions/c3d0f0bd-e344-4600-a023-0ed50d25b48b/digest.md)
- `cf0456ab-e3f0-4f81-a4f5-bec4b3455f9f` — Mécanisme de mise à jour pair douteux (début 2026-10-29 15:51, 21.6 h) → [rapport](../sessions/cf0456ab-e3f0-4f81-a4f5-bec4b3455f9f/rapport.md) · [digest](../sessions/cf0456ab-e3f0-4f81-a4f5-bec4b3455f9f/digest.md)
- `d58fb6be-cedc-4236-a298-aa953dfb21b7` — Tu es dans /home/stephane/Data13TB/steph (début 2026-10-29 22:25, 0.5 h) → [rapport](../sessions/d58fb6be-cedc-4236-a298-aa953dfb21b7/rapport.md) · [digest](../sessions/d58fb6be-cedc-4236-a298-aa953dfb21b7/digest.md)
- `d622230d-649c-43cf-9202-da1eeb230259` — Tu es dans /home/stephane/Data13TB/steph (début 2026-10-29 22:25, 0.3 h) → [rapport](../sessions/d622230d-649c-43cf-9202-da1eeb230259/rapport.md) · [digest](../sessions/d622230d-649c-43cf-9202-da1eeb230259/digest.md)
- `f0969e87-af0c-43b1-93cf-f278d9c90846` — Optimiser couches linguistiques jeux symboliques (début 2026-10-25 21:28, 89.0 h) → [rapport](../sessions/f0969e87-af0c-43b1-93cf-f278d9c90846/rapport.md) · [digest](../sessions/f0969e87-af0c-43b1-93cf-f278d9c90846/digest.md)

## Mesures et rapports touchés

- [reports/INDEX.md](../../reports/INDEX.md)
- [reports/README.md](../../reports/README.md)
- [reports/rapport-drvm-ppl.md](../../reports/rapport-drvm-ppl.md)
- [reports/rapport-n3.3c-sparsite-compte.md](../../reports/rapport-n3.3c-sparsite-compte.md)
- [reports/rapport-native-ppl-2k.md](../../reports/rapport-native-ppl-2k.md)
- [reports/rapport-r03-banc-complet.md](../../reports/rapport-r03-banc-complet.md)
- [reports/rapport-r03-lecteur-modele.md](../../reports/rapport-r03-lecteur-modele.md)

<!-- notes -->

<!-- /notes -->

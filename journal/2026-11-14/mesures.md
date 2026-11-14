# 2026-11-14 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (7)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:06 | `b6e474dc` | J6.2 — s065 : LA REL SUIVIE D'UN GV PREND LE SUJET DU GV (238/238 LABELS, 238/239 CIBLES, F1 0,7902 INCHANGÉ, 0 SPAN, 0 POS) | `chantiers.md`, `en-cours.md`, `roadmap.md` (+14) |
| 01:08 | `6ecc9763` | JOURNAL — 2026-11-14 : J6.2 AU RÉCIT (2 COMMITS, LE THÈME MESURES), s065 238/238 | `README.md`, `mesures.md`, `README.md` (+4) |
| 03:23 | `229098ec` | J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS) | `en-cours.md`, `roadmap.md`, `README.md` (+24) |
| 03:53 | `03ecee41` | J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ | `en-cours.md`, `roadmap.md`, `semaine-autonome.md` (+16) |
| 04:28 | `84e393bb` | J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238 | `en-cours.md`, `roadmap.md`, `exemples.md` (+13) |
| 04:40 | `09e54143` | J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ | `en-cours.md`, `roadmap.md`, `README.md` (+18) |
| 04:55 | `55bde5c5` | J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 SCHÉMA V2, 115 CHEVAUCHEMENTS ALTERNATIVE / 0 FILTRER ; RESTITUTION 46/46, STRICT 0,1087 (F1 0,7902) | `en-cours.md`, `roadmap.md`, `README.md` (+16) |

## Chiffres du jour

`0,1087` · `0,7902` · `0,8159` · `0,7475` · `0,9451` · `0,8656` · `0,7533`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 325.9 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)

## Mesures et rapports touchés

- [reports/README.md](../../reports/README.md)
- [reports/rapport-bilan-chantier.md](../../reports/rapport-bilan-chantier.md)
- [reports/rapport-evaluer-langue.md](../../reports/rapport-evaluer-langue.md)
- [reports/rapport-exemples-rejoues.md](../../reports/rapport-exemples-rejoues.md)
- [reports/rapport-restitution-v1.md](../../reports/rapport-restitution-v1.md)
- [reports/rapport-robustesse-semaine.md](../../reports/rapport-robustesse-semaine.md)
- [reports/rapport-s065.md](../../reports/rapport-s065.md)

<!-- notes -->
**J13.1 — la table des mesures.** Le chantier est consolidé en une table unique, de J1.1 à
J12.2 : **26 tâches**, **25 acceptations vertes**, **1 échec** (J5.2, le tag), **5 timeouts**
dont **4 récupérés**. Chaque ligne porte sa **base** (612/602), son **avant**, son **après**, son
**Δ**, un **contrôle négatif**, son **commit** et sa **fiche**. Le produit tient (**F1 0,7533 →
0,7902**, attachement **236/237 → 238/238 labels**, couverture **0,9916 → 0,9958**, spans
**2 → 1**, schéma v2, restitution v1, 50 textes, 5 exemples, fr/en) ; le tagger vaut **0,9475
(+8,49)** ; Panini est **borné** (table 14/14, corpus 418/438, généalogie 154/154, familles
0,619 vs 0,0445, §334, CIC 42/42). La **base 612/602** est re-mesurée au HEAD `b20a4c31` :
**0,7902 / 0,7882** (F1), **238/239 / 234/239** (attachement). La clôture reste **J14.1** (passe
+ tag). Fiche [`reports/rapport-tableau-mesures.md`](../../reports/rapport-tableau-mesures.md) +
[`JSON`](../../reports/tableau-mesures.json).
<!-- /notes -->

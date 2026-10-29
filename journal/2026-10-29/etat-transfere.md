# État transféré — 2026-10-29

> **Pourquoi ce fichier.** `docs/pilotage/en-cours.md` ne garde que les **sessions actives** et les **bloquants**.
> Les éléments terminés sont transférés ici, avec leur fiche. **Ne pas charger par défaut** : c'est de l'histoire.
> Le plan est [`docs/pilotage/roadmap.md`](../../docs/pilotage/roadmap.md) ; l'état courant
> [`docs/pilotage/en-cours.md`](../../docs/pilotage/en-cours.md).

## Terminés, retirés de l'état

| chantier | état | où lire |
|---|---|---|
| **N0 — DRVM** | ✅ format, lecteur Python/Rust, GGUF ↔ DRVM (SHA identique), trace/rejeu (6 144 listes), exécution native ; **N0.3b (parité PPL) reste ouvert** | [`roadmap-native-2026-10-29.md`](../../docs/archive/roadmap-native-2026-10-29.md) |
| **N1 — `drave-n0`** | ✅ 11,47 M, 6 blocs ; PPL 3,465 avec pont (4,080 sans) ; têtes 57,6/61,6/62,1 % ; réflexe −24,05 % ; pensée λ = 0,709 ; cache 19,25× | [`roadmap-native-2026-10-29.md`](../../docs/archive/roadmap-native-2026-10-29.md) |
| **C1–C7** | ✅ corpus, traduction, restitution, styles, domaines, documentation, pensée | [`etat-ancien.md`](../2026-10-28/etat-ancien.md) |
| **B3/B4** | ✅ plan (0,43), opérateurs (négatifs nommés) | [`rapport-operateur-negation.md`](../../reports/rapport-operateur-negation.md) |
| **B5/B6** | ✅ jeux : 112 items, 100 % au niveau 4, perft, 3/3 mats | [`rapport-jeux-symboliques.md`](../../reports/rapport-jeux-symboliques.md) |
| **B7/B8** | ✅ 71 langues, 449/449, livre 10/10, go 9×9 10/10 | [`rapport-langues-maitres.md`](../../reports/rapport-langues-maitres.md) |
| **C3.2** | ✅ 9 familles, 7/9 > 30 %, moyenne 69,5 % | [`rapport-familles-9.md`](../../reports/rapport-familles-9.md) |
| **A1–A8** | ✅ moteur ; restent A2.6, A3.2/A3.3, et les bloqués A3.4/A5.4/A6.2 | [`roadmap-detail-2026-10-29.md`](../../docs/archive/roadmap-detail-2026-10-29.md) |

## Ce qui n'est pas transféré

Les **sessions actives** restent dans `en-cours` ; les **bloquants** aussi. Les **résultats** restent dans
`reports/` ; ce fichier n'est qu'un **index de transfert**, pas une fiche de mesure.

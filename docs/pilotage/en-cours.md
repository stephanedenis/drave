# En ce moment

**Mis à jour : 2026-10-28, 12 h 59 HAE (heure locale, EDT).**

> Cette page dit **où l'on va, ce qui est en cours, où l'on en est, et ce qu'il reste**. Les chiffres, les séries et
> les contrôles vivent dans [`reports/`](../../reports/) ; le plan dans [`roadmap.md`](roadmap.md) et
> [`roadmap-native.md`](roadmap-native.md). **Ici, l'actualité seulement** — le détail se charge à la demande.

## Session en cours

- **Id DSH** : `f0969e87-af0c-43b1-93cf-f278d9c90846`.
- **Cycle DSH** : goal unique par programme, **max_goal_rounds 1 000** ; 2 à 4 sous-agents en
  parallèle ; reprise par `update_goal resume` (voir [`continuite.md`](../methode/continuite.md)).
- **Journaux** : [l'index des sessions](../../journal/README.md#sessions) · [le journal du jour](../../journal/2026-10-28/README.md).
- **Agent principal** : **N4.2 terminé** — service local HTTP, 69 octets, CPU. **Prochain : N0.7**, test automatisé de la parité native et PPL native.
- **Sous-agents actifs** : **aucun pour l'instant**. Au prochain cycle, lancer **2 à 4** sous-agents sur les
  actions indépendantes (N0.3b, N1.6, N2). Les anciens A18/A19/A20 sont **inactifs** ; aucun travail n'attend.
- **Reprise** : lire cette page, puis [`roadmap-native.md`](roadmap-native.md) (N0/N1) ; l'historique est dans
  [`journal/2026-10-28/etat-ancien.md`](../../journal/2026-10-28/etat-ancien.md).

## Ce qui est en cours

- **N0 — DRVM** : format natif (manifeste, graphe, payload aligné 64 o, SHA-256, `mmap`), lecteur Python et
  Rust (`drvm.rs`, CLI `--drvm-inspect`). **Fait** : N0.1, N0.2, N0.3 (parseur), **poids 114/114**, N0.4
  (GGUF ↔ DRVM, **SHA identique**), **PPL 28,7355**, N0.5 (trace **6 144 listes**, logits **SHA identique**), N0.6.
- **N1 — `drave-n0`** : 11,47 M, octets, 6 blocs, attention locale 256, FFN creux top-2 + k-WTA 25 %,
  3 têtes précoces, cellule de pensée contractante, **pont** après le bloc 3. **PPL 3,465** ; têtes
  **57,6 / 61,6 / 62,1 %** contre **62,7 %** pour la principale ; pensée **λ = 0,709**.
- **N1.5 — la pensée contractante** : **λ = 0,709**, PPL **3,58**, sans pensée **721 726** ; **fait**. Le contenu est porté par la pensée, pas seulement par la sortie.
- **N1.6 — le pont** : **fait** — PPL **3,465**, neutralisé **4,080** ; effet **−9,3 %** ; coût vs modèle sans pont **−3,2 %**.
- **N1.7 — le réflexe** : **fait** — 4 blocs **5,978 ms** contre 6 blocs **7,871 ms**, **−24,05 %** de temps pour **−1,61 point** de précision.
- **N2 — la distillation** : **corpus** 49 999 fenêtres, **4 sources**, **ordre VDC** ; **professeur fr** 23,76 M (PPL **2,355**) ; **distillation fr** PPL **3,295** ; **multi** student **9,517** vs professeur **9,571** ; **capacité à budget égal, 3 graines** : 21,63 M **4,142** vs 11,47 M **4,507** (−8,1 %) ; checkpoint 11,47 M **3,295**. Porte **< 2,5** non atteinte.
- **N4 — génération** : **technique** — greedy 160 octets, cohérent 12 octets puis dérive ; **pas un assistant**.
- **N4.2 — service local** : HTTP `/sante` + `/generer`, **69 octets**, CPU, greedy ; pas d'auth, pas de cache KV.
- **N0.7 — exécution native** : `--drvm-forward` calcule **sans GGUF** ; logits **10,8232** identiques, top-5 identique. Cause de l'écart initial : le routeur n'était pas appliqué à `h` dans le modèle Python.

## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **49** (46 vertes, 3 rouges) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **235** / **301** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **57** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 40** (28/10 00 h 12) | `docs/pilotage/references-non-regression.md` |

## Où l'on en est

| | |
|---|---:|
| **N0 — DRVM** | format + lecteur Python/Rust + CLI ; **parité PPL à faire** |
| **N1 — PPL** | **3,465** (avec pont et pensée) ; sans pont **4,080** |
| **N1.4 — têtes précoces** | **57,57 / 61,60 / 62,06 %** ; principale **62,70 %** ; témoin **0,39 %** |
| **N1.5 — pensée** | **λ = 0,709** ; PPL sans pensée **721 726**, avec **3,53** |
| tests cerveau | **180 OK**, 31 skips |
| portes | **46 vertes, 3 rouges** (28/10 00 h 12) |

## Les sept chantiers, en une ligne

| chantier | état |
|---|---|
| **C1** corpus et généalogie | ✅ fait (UDHR, Glottolog) |
| **C2** traduction | ✅ mesuré (juge, plancher, marge) |
| **C3** restitution | ✅ mesuré — **9 familles**, **7/9 > 30 %** ; sous-familles IE **54,6–100 %** |
| **C4** dialectes et styles | ✅ mesuré ; la date reste à contrôler |
| **C5** qualité par domaine | ✅ six registres + dialogue spontané |
| **C6** documentation | ✅ fait — quatre familles, revue verte |
| **C7** pensée abstraite | ✅ mesuré — la carte, **B4** close, **B5/B6** faits, **B10–B12** premier passage ; **N1.5** en cours |

## Ce qui reste

**N0.3b** — parité PPL DRVM ↔ GGUF. **N0.4** — `gguf2drvm`. **N0.5** — trace/rejeu DRVM. **N1.6** — pont de
région. **N2** — 50 000 séquences et distillation. **N4** — SFT chat, service, sûreté.

**Migré** : les résultats A7.5–A7.26, B10–B27, C3.2c/d/e et les anciens tableaux de bord sont dans
[`journal/2026-10-28/etat-ancien.md`](../../journal/2026-10-28/etat-ancien.md) ; ils ne sont plus dans cette page.

## Les questions ouvertes

- **N0.3b** : le moteur peut-il exécuter une passe avant DRVM et rendre la même PPL que l'entraîneur ?
- **N1.6** : le pont de région coûte-t-il moins de **5 %** de PPL ?
- **N2** : 50 000 séquences sont-elles accessibles et licites ?
- **N4** : le BPE est-il nécessaire, ou les octets suffisent-ils à 12 M ?

## La carte

[`carte.md`](../theorie/carte.md) — les sujets, bloc par bloc ; [`README.md`](../README.md) — l'inventaire ;
[`roadmap.md`](roadmap.md) — le plan ; [`roadmap-native.md`](roadmap-native.md) — le programme N ;
[`synthese/index.md`](../theorie/synthese/index.md) — la théorie ; [`reports/`](../../reports/) et
[`journal/`](../../journal/) — les preuves et le récit.

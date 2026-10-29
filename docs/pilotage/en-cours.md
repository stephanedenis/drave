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
- **Agent principal** : **sprint 08:00** — professeur 10 000 pas (GPU 1) et distillation 30 000 pas (GPU 0) en parallèle ; PPL native de corpus en attente.**
- **Sous-agents actifs** : **aucun pour l'instant**. Au prochain cycle, lancer **2 à 4** sous-agents sur les
  actions indépendantes (N0.3b, N1.6, N2). Les anciens A18/A19/A20 sont **inactifs** ; aucun travail n'attend.
- **Reprise** : lire cette page, puis [`roadmap-native.md`](roadmap-native.md) (N0/N1) ; l'historique est dans
  [`journal/2026-10-28/etat-ancien.md`](../../journal/2026-10-28/etat-ancien.md).

## Ce qui est en cours

- **N0 — DRVM** : format natif, lecteur Python/Rust, GGUF ↔ DRVM (**SHA identique**), trace/rejeu (**6 144 listes**, logits **SHA identique**), **exécution native** (`--drvm-forward`, logits **10,8232**), **parité automatisée 5/5 prompts** (écart **0,00006**) et **cache KV 19,25×** (592,6 ms contre 11 406,9 ms).
- **N1 — `drave-n0`** : 11,47 M, 6 blocs, attention locale, FFN creux, 3 têtes précoces, pensée contractante **λ = 0,709**, pont **−9,3 %**, réflexe **−24,05 %**.
- **N2 — distillation** : 49 999 fenêtres / 4 sources, VDC ; professeur fr **2,355** ; student **3,123** après 20 000 pas ; multi **9,517** vs **9,571** ; capacité à budget égal 21,63 M **4,142** vs 11,47 M **4,507** (−8,1 %). Porte **< 2,5 non atteinte**.
- **N0.11 — test Rust** : fixture **36 Ko**, **7 754** paramètres, forward et génération testés dans le crate.
- **N0.12 — PPL native** : **4,6585**, identique à Python sur 59 octets.
- **N0.13 — PPL native de corpus** : **18,6394** sur **1 076 octets**, Python **18,6395**.
- **N4 — usage** : génération greedy, service Python (69 octets), **service Rust cache** (53 octets, 611 ms), **jeton 401/200** ; **pas d'alignement SFT**, pas un assistant.

## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **49** (46 vertes, 3 rouges) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **246** / **311** | `reports/*.md` / `reports/*.json` |
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

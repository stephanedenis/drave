# En ce moment

**Mis à jour : 2026-10-29, 08 h 30 HAE (heure locale, EDT).**

> Cette page dit **où l'on va, ce qui est en cours, où l'on en est, et ce qu'il reste**. Les chiffres, les séries et
> les contrôles vivent dans [`reports/`](../../reports/) ; le plan est **unique** : [`roadmap.md`](roadmap.md)
> (programmes A, B, N, R) ; les fiches de fonctionnalité dans [`backlog/index.md`](backlog/index.md). **Ici,
> l'actualité seulement** — le détail se charge à la demande.

## Session en cours

- **Id DSH** : `f0969e87-af0c-43b1-93cf-f278d9c90846`.
- **Cycle DSH** : goal unique par programme, **max_goal_rounds 1 000** ; 2 à 4 sous-agents en parallèle ; reprise
  par `update_goal resume` (voir [`continuite.md`](../methode/continuite.md)).
- **Journaux** : [l'index des sessions](../../journal/README.md#sessions) · [le journal du jour](../../journal/2026-10-29/README.md).
- **Agent principal** : **sprint 08:00** — N2 (professeur 10 000 pas, distillation 30 000 pas) sur GPU ;
  **R0 — lecteur v0** (graphe de document, contrôleur, banc) sur CPU, sans entraînement.
- **Sous-agents actifs** : **aucun pour l'instant**. Au prochain cycle, lancer **2 à 4** sous-agents sur les
  actions indépendantes : **R0.1** (graphe), **R0.2** (contrôleur), **R0.3** (banc), **N0.3b** (parité).
- **Reprise** : lire cette page, puis [`roadmap.md`](roadmap.md) § **Programme R** et § **L'ordre du jour** ;
  l'historique est dans [`journal/2026-10-28/etat-ancien.md`](../../journal/2026-10-28/etat-ancien.md).

## Ce qui est en cours

- **N0 — DRVM** : format, lecteur Python/Rust, GGUF ↔ DRVM (**SHA identique**), trace/rejeu (**6 144 listes**,
  logits **SHA identique**), exécution native ; seule la **parité PPL** (N0.3b) reste ouverte.
- **N1 — `drave-n0`** : 11,47 M, 6 blocs, attention locale, FFN creux, 3 têtes précoces ; PPL **3,465** avec pont
  (**4,080** sans), pensée **λ = 0,709**, réflexe **−24,05 %**, cache **19,25×**.
- **N2 — distillation** : 49 999 fenêtres / 4 sources ; professeur 30k **1,734** ; student **3,123** à 20 000 pas ;
  meilleur **2,6998**, plateau **2,708** ; porte **< 2,5 non atteinte**.
- **N4 — usage** : génération greedy, service Python (69 octets), service Rust (53 octets, 611 ms), jeton
  **401/200** ; **SFT 24/24 vus, 0/4 tenus** — pas d'alignement.
- **R0 — lecteur v0** : **nouveau et non bloqué** — graphe de document (R0.1), contrôleur de lecture (R0.2), banc
  de lecture rapide (R0.3) ; se mesure avec un modèle externe, sans entraîner le natif.
- **B10/B12 — sémantique et cerveau** : encodeur `z` **0,426** contre **0,167** de hasard ; décodeur **sous le
  plancher** (chrF **12,7 / 5,3** contre **39,6**) ; B12.10 (pipeline M1→M4→M8) partiel.
- **A — moteur** : A1–A8 mesurés, sauf **A3.4** (Colab), **A5.4** (FPGA), **A6.2** (MoE local) ; restent
  A2.6 (ordonnanceur), A3.2/A3.3 (granularité, seuil) ; A8.3 en opt-in.
- **Backlog** : **29 fiches** — 19 pour R, 10 pour les lignes ouvertes A/B/N ; une fiche par contrat, porte et
  contrôle négatif.
- **Documentation** : une **seule roadmap** (A/B/N/R) ; l'ancien détail A/B et N est archivé et lié depuis la
  roadmap ; l'analyse de la lecture rapide est dans [`lecture-rapide.md`](../theorie/lecture-rapide.md).

## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **49** (47 vertes, 2 rouges structurelles) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **273** / **337** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **88** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 40** (28/10 00 h 12) | `docs/pilotage/references-non-regression.md` |

## Où l'on en est

| | |
|---|---:|
| **N0 — DRVM** | format + lecteur + rejeu ; **parité PPL à faire** |
| **N1 — PPL** | **3,465** (avec pont et pensée) ; sans pont **4,080** |
| **N2 — distillation** | meilleur **2,6998**, plateau **2,708** ; porte **< 2,5** non atteinte |
| **N4 — usage** | service **611 ms** ; SFT **24/24 vus, 0/4 tenus** |
| **R0 — lecteur** | **à faire** : graphe, contrôleur, banc ; c'est la priorité non bloquée |
| **B10/B12** | `z` **0,426** ; décodeur négatif ; B12.10 partiel |
| tests cerveau | **180 OK**, 31 skips |
| portes | **47 vertes, 2 rouges** (28/10 23 h 55) |

## Les sept chantiers, en une ligne

| chantier | état |
|---|---|
| **C1** corpus et généalogie | ✅ fait (UDHR, Glottolog) |
| **C2** traduction | ✅ mesuré (juge, plancher, marge) |
| **C3** restitution | ✅ mesuré — **9 familles**, **7/9 > 30 %** ; sous-familles IE **54,6–100 %** |
| **C4** dialectes et styles | ✅ mesuré ; la date reste à contrôler |
| **C5** qualité par domaine | ✅ six registres + dialogue spontané |
| **C6** documentation | ✅ fait — quatre familles, revue verte |
| **C7** pensée abstraite | ✅ mesuré — **B4** close, **B5/B6** faits, **B10–B12** premier passage |

## Ce qui reste

**R0** — le lecteur v0 : **R0.1** graphe de document, **R0.2** contrôleur, **R0.3** banc (priorité non bloquée).
**N0.3b** — parité PPL DRVM ↔ GGUF. **N2** — données/capacité, porte < 2,5. **N4** — SFT tenu à l'écart.
**B10.3** — raisonnement sur `z` (bloqué par le décodeur). **B12.10** — pipeline M1→M4→M8.
**Bloqués** : B1.5 (corpus), A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE local).

## Les questions ouvertes

- **R0** : un contrôleur classique + un modèle externe atteint-il **90 %** de la compréhension à **30 %** du coût
  sur trois types de documents ?
- **R1** : le natif peut-il lire **1 000 octets** sans refaire les négatifs 130–256 — et la hiérarchie suffit-elle ?
- **N2** : le student peut-il descendre sous **2,5** de PPL, ou le plateau **2,708** est-il la capacité du corpus ?
- **N4** : le BPE est-il nécessaire, ou les octets suffisent-ils à 12 M ?
- **B10.3** : un décodeur à attention croisée dépasse-t-il le plancher **39,6** de chrF ?

## La carte

[`carte.md`](../theorie/carte.md) — les sujets, bloc par bloc ; [`README.md`](../README.md) — l'inventaire ;
[`roadmap.md`](roadmap.md) — **le plan unique (A/B/N/R)** ; [`backlog/index.md`](backlog/index.md) — les fiches de
fonctionnalité ; [`synthese/index.md`](../theorie/synthese/index.md) — la théorie ; [`reports/`](../../reports/) et
[`journal/`](../../journal/) — les preuves et le récit.

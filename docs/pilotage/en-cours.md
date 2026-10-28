# En ce moment

**Mis à jour : 2026-10-28, 08 h 35 HAE (heure locale, EDT).**

> Cette page dit **où l'on va, ce qui est en cours, où l'on en est, et ce qu'il reste**. Les chiffres, les séries et
> les contrôles vivent dans [`reports/`](../../reports/) ; le plan dans [`roadmap.md`](roadmap.md). **Ici, l'actualité
> seulement** — le détail se charge à la demande.

## Où l'on va

**Démontrer que la structure bat la taille, et construire le [bus d'événements](../theorie/glossaire/entrees/evenement.md) qui rend
les blocs [observables](../theorie/glossaire/entrees/trace.md), [décomposables](../theorie/glossaire/entrees/couche-etage.md),
[répartissables](../theorie/glossaire/entrees/grappe.md) et [rejouables](../theorie/glossaire/entrees/rejeu.md).** Le bus accepte des blocs **neuronaux** (l'intuition, la langue) et
**classiques** (une règle, un solveur, une opération exacte) ; il les rend substituables, comparables et mesurables.
La vision complète est dans [`vision.md`](../theorie/vision.md).

## Ce qui est en cours

**La phase B12 est mesurée** ; les suites sont dans [`roadmap.md`](roadmap.md).

- **A7 la [grappe](../theorie/glossaire/entrees/grappe.md) [déportée](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md)** — **faite jusqu'à A7.26** : relais exact, grappe 21 %, transport sparse **4,44×**,
  seuil réseau, [couche](../theorie/glossaire/entrees/couche.md) distante **bit-à-bit**, [cache KV](../theorie/glossaire/entrees/kv.md) [int8](../theorie/glossaire/entrees/int4-int8.md),
  **[cache mixte](../theorie/glossaire/entrees/quantification-du-kv.md) 92,6 % à 256 [jetons](../theorie/glossaire/entrees/jeton-2.md)**. Reste **A7.27**,
  le recalage f32 des tokens incertains.
- **B12 les modules cerveau-langage** — **corrigé** : M1 **528/528** solide ; M2 vu seulement ; M3 **tautologique** ;
  M4 **lookup** ; M5 contexte ; M6 langue, commutation 0 ; M7 plafond **3,64 %** ; M8 **96,48 % marginal**. Détail :
  [`rapport-cerveau-corrections.md`](../../reports/rapport-cerveau-corrections.md).
- **B10 le protocole sémantique** — **premier passage** : encodeur **0,426** contre 0,167 ; décodeur **négatif**
  (chrF **14,0 / 5,4** contre un plancher **38,8**) ; `z` est un **code d'identité** plus qu'un code de contenu.
  Fiche : [`rapport-semantique.md`](../../reports/rapport-semantique.md).
- **B11 la base d'universaux typés** — le **codec classique** lit **528/528** et restitue le code à **100 %** ; le
  **natif** est à **59,8 % / 40,7 %** avec contexte ; la **surface originale** reste à **33/79**. Fiche :
  [`rapport-universaux.md`](../../reports/rapport-universaux.md).
- **B13–B23** — chaînes sémantiques, mémoire, restitution, secours, typo, [routeur](../theorie/glossaire/entrees/routeur.md) : intégration mesurée, pas preuve
  d'[étage](../theorie/glossaire/entrees/couche-etage.md). Les négatifs sont nommés dans [`roadmap.md`](roadmap.md).
- **B24–B27** — [routeur](../theorie/glossaire/entrees/routeur.md) confiance (**typo +7,5, espaces −7,5**), M8 [rejeu](../theorie/glossaire/entrees/rejeu.md) (**0**), M6 conflit/moteur (**0**, sélecteur
  sans compétition). Détail : [`rapport-routeur-confiance.md`](../../reports/rapport-routeur-confiance.md),
  [`rapport-m8-rejeu.md`](../../reports/rapport-m8-rejeu.md), [`rapport-m6-conflit2.md`](../../reports/rapport-m6-conflit2.md).
- **C3.2c/d/e** — **9 [familles](../theorie/glossaire/entrees/genealogie.md)** : **7/9 > 30 %**, moyenne **69,5 %** ; l'indo-européen à **14,7 %** est un **effet de
  composition** (sous-familles **54,6–100 %**) ; l'uralic côtier **100 %** explique l'uralic à **46,7 %**.
- **[Portes](../theorie/glossaire/entrees/porte-drave.md)** — dernière passe : **46 vertes, 3 rouges** (`porte-indice`, `porte-melange` structurelles ;
  `porte-occupation-moteur` **verte seule**, rouge de contention).

## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py` ; les autres pages y renvoient.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **49** (46 vertes, 3 rouges) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **215** / **282** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **53** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 40** (28/10 00 h 12) | `docs/pilotage/references-non-regression.md` |

## Où l'on en est

| | |
|---|---:|
| portes (dernière passe) | **46 vertes, 3 rouges** (28/10 00 h 12) |
| porte-deepseek | **verte** (20 tests) |
| fichiers / JSON de résultats | **215** / **282** |
| la sonde, au pic du 1,5 B | **0,7256** (XNLI) |
| le pont, au pic du 14 B | **0,8715** — il plafonne à 0,87 |
| la sémantique des jeux (B5/B6) | **112 items, 100 % au niveau 4, 33/33 paires** |
| les langues (B7) | **71 langues, 35 concepts, 449/449, 11/11** |
| les maîtres (B8) | **d4, livre 10/10, go 9×9 10/10, dames 0 défaite, cartes 44,7 % (négatif)** |
| le banc externe (B9) | **DeepSeek 310/310, chrF 82,82 contre 15,64 ; 31,63 M/610 : 4,40 %** |
| le protocole sémantique (B10) | **encodeur 0,426 contre 0,167 ; décodeur négatif 14,0/5,4 contre 38,8** |
| la base typée (B11) | **codec 100 %** (79/79, 449/449) ; natif **59,8 % / 40,7 %** ; surface **33/79** |
| B22/B23 — M2 et le routeur | **M2 typos 62–80 % vs M1 24–45 %** ; routeur espaces **41,8 % vs 11,6 %**, typo **56,2 % < M2 68,3 %** |
| A7.26 — cache mixte | **92,6 %** à 256 jetons, seuil **64**, mémoire **62,5 %** |

## Les sept chantiers, en une ligne

| chantier | état |
|---|---|
| **C1** corpus et généalogie | ✅ fait (UDHR, Glottolog) |
| **C2** traduction | ✅ mesuré (juge, plancher, marge) |
| **C3** restitution | ✅ mesuré — **9 familles**, **7/9 > 30 %** ; sous-familles IE **54,6–100 %** |
| **C4** dialectes et styles | ✅ mesuré ; la date reste à contrôler |
| **C5** qualité par domaine | ✅ six registres + dialogue spontané |
| **C6** documentation | ✅ fait — revue du 28/10 : compteurs et chemins corrigés ; docwatch épinglé en sous-module |
| **C7** pensée abstraite | ✅ mesuré — la carte, **B4** close, **B5/B6** faits, **B10–B12** premier passage |

## Ce qui reste

**Court terme** — **A7.27** : recalage f32 des tokens incertains ; **B10.3** : un décodeur au-dessus du plancher ;
**B12.10** : M3 répétitions, M7 capacité ; **B9** : 31,63 M / 610 à 750/1 000 pas ; **C3.2f** : afro-asiatic
**est** vs **ouest**.

**Moyen terme** — les suites des jeux hors plan (corpus externe, MCTS budgété, portage Rust), la **prose
scientifique** (bloquée par le corpus), le **FPGA**, la **démonstration distante** (compte Colab), le **MoE** local.

**Objectif final** — une entrée-sortie **fiable** (étage 1), puis une **pensée abstraite** jugée sur des
**opérations** (étage 2) ; un moteur **décomposable, répartissable, observable et rejouable**, tenu par ses mesures.

## Les questions ouvertes

- **Bloquées par une ressource** : B1.5 (corpus scientifique humain), A3.4 (compte Colab), A5.4 (carte Stratix V),
  A6.2 (MoE local).
- **Ouvertes sans blocage** : **B10.3** (décodeur au-dessus du plancher), **B12.10** (M3/M7), **A7.27** (recalage
  f32), le **pic du 32 B** (nommé, non forcé), les limites des jeux (détection sur cases seules, ko simple, MCTS à
  60 playouts), le **portage Rust** du contrat RSN.
- **Tranchée** : les styles à époque contrôlée — la surface capte l'époque (+0,138) plus que la filiation (+0,049) ;
  c'est une règle de méthode.

## Le vocabulaire

Les termes de cette page ont leur fiche : [bus d'événements](../theorie/glossaire/entrees/evenement.md) ·
[couche / étage](../theorie/glossaire/entrees/couche-etage.md) · [RSN](../theorie/glossaire/entrees/representation-semantique-neutre.md) ·
[grappe](../theorie/glossaire/entrees/grappe.md) · [KV](../theorie/glossaire/entrees/kv.md) · [quantification du KV](../theorie/glossaire/entrees/quantification-du-kv.md) ·
[porte Drave](../theorie/glossaire/entrees/porte-drave.md) · [rejeu](../theorie/glossaire/entrees/rejeu.md) · [routeur](../theorie/glossaire/entrees/routeur.md) ·
[généalogie](../theorie/glossaire/entrees/genealogie.md) · [fidélité](../theorie/glossaire/entrees/fidelite.md) · [perplexité](../theorie/glossaire/entrees/perplexite.md).

## La carte

[`carte.md`](../theorie/carte.md) — les sujets, bloc par bloc ; [`README.md`](../README.md) — l'inventaire ; [`roadmap.md`](roadmap.md)
— le plan ; [`synthese/index.md`](../theorie/synthese/index.md) — la théorie ; [`reports/`](../../reports/) et
[`journal/`](../../journal/) — les preuves et le récit.

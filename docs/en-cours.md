2026-10-26

# En ce moment

**Mis à jour : 2026-10-26, 16 h 20 HAE (heure locale, EDT).**

> Cette page dit **où l'on va, ce qui est en cours, où l'on en est, et ce qu'il reste**. Les chiffres, les séries et
> les contrôles vivent dans [`reports/`](../reports/) ; le plan dans [`roadmap.md`](roadmap.md). **Ici, l'actualité
> seulement** — le détail se charge à la demande.

## Où l'on va

**Démontrer que la structure bat la taille, et construire le bus d'événements qui rend les blocs observables,
décomposables, répartissables et rejouables.** Le bus accepte des blocs **neuronaux** (l'intuition, la langue) et
**classiques** (une règle, un solveur, une opération exacte) ; il les rend substituables, comparables et mesurables.
La vision complète est dans [`vision.md`](vision.md).

## Ce qui est en cours

**La phase B9 est mesurée** ; les suites sont dans [`roadmap.md`](roadmap.md).

- **A7 la grappe déportée** — **faite** : le relais rend le même chiffre, la grappe exacte à 21 %, le transport à
  4,22×.
- **B4 les opérateurs abstraits** — **close** : six mesures, dont le LoRA qui **inverse**.
- **A8 l'ordonnanceur place et perte** — **fait, opt-in**.
- **B5/B6 les jeux symboliques** — **faits** : surface → RSN-jeu → pensée, cinq jeux, 112 items.
- **B7/B8 les langues et les maîtres** — **faits** : 71 langues, 449 surfaces, 17 principes, les négatifs nommés.
- **B9 le banc externe** — **mesuré** : DeepSeek sert le langage, `route` reste sur GPU. Le **meilleur écart** de
  distillation est **4,40 % à 31,63 M / 610 exemples** ; la **fenêtre** (3,71 % à 500 pas, 1,29 % à 750, −0,49 % à
  1 000) et le **négatif 30 langues** sont nommés. Détail : [`rapport-deepseek.md`](../reports/rapport-deepseek.md).

## Où l'on en est

| | |
|---|---:|
| portes (passe complète) | **49** — **47 vertes, 2 structurelles** (26/10 14 h 30) |
| porte-deepseek | **verte** (20 tests), incluse dans la passe |
| fiches / JSON de résultats | **164** / **236** |
| la sonde, au pic du 1,5 B | **0,7256** (XNLI) |
| le pont, au pic du 14 B | **0,8715** — il plafonne à 0,87 |
| la sémantique des jeux (B5/B6) | **112 items, 100 % au niveau 4, 33/33 paires** |
| les langues (B7) | **71 langues, 35 concepts, 449/449, 11/11** |
| les maîtres (B8) | **d4, livre 10/10, go 9×9 10/10, dames 0 défaite, cartes 44,7 % (négatif)** |
| le banc externe (B9) | **DeepSeek 310/310, chrF 82,82 contre 15,64 ; 31,63 M/610 : 4,40 %** |

## Les sept chantiers, en une ligne

| chantier | état |
|---|---|
| **C1** corpus et généalogie | ✅ fait (UDHR, Glottolog) |
| **C2** traduction | ✅ mesuré (juge, plancher, marge) |
| **C3** restitution | ✅ mesuré ; **C3.2** : un module par famille, **4/5** au-dessus de la référence |
| **C4** dialectes et styles | ✅ mesuré ; la date reste à contrôler |
| **C5** qualité par domaine | ✅ six registres + dialogue spontané |
| **C6** documentation | ✅ fait (revue, portes, archive) |
| **C7** pensée abstraite | ✅ mesuré — la carte, **B4** close, **B5/B6** faits |

## Ce qui reste

**Court terme** — aucune ligne non bloquée du plan n'est ouverte ; les suites sont nommées : **31,63 M / 610 à
750/1 000 pas** (la fenêtre tient-elle avec la capacité ?), **plus de données avec la capacité** (pas plus de langues
seules), le **masque dans le trainer**, l'**export du 31,63 M** vers le moteur.

**Moyen terme** — les suites des jeux hors plan (corpus externe, MCTS budgété, portage Rust), les **9 familles** de
C3, la **prose scientifique** (bloquée par le corpus), le **FPGA**, la **démonstration distante** (compte Colab), le
**MoE** local.

**Objectif final** — une entrée-sortie **fiable** (étage 1), puis une **pensée abstraite** jugée sur des
**opérations** (étage 2) ; un moteur **décomposable, répartissable, observable et rejouable**, tenu par ses mesures.

## Les questions ouvertes

- **Bloquées par une ressource** : B1.5 (corpus scientifique humain), A3.4 (compte Colab), A5.4 (carte Stratix V),
  A6.2 (MoE local).
- **Ouvertes sans blocage** : le **pic du 32 B** (nommé, non forcé), les limites des jeux (détection sur cases
  seules, ko simple, MCTS à 60 playouts), le **portage Rust** du contrat RSN.
- **Tranchée** : les styles à époque contrôlée — la surface capte l'époque (+0,138) plus que la filiation (+0,049) ;
  c'est une règle de méthode.

## La carte

[`carte.md`](carte.md) — les sujets, bloc par bloc ; [`README.md`](README.md) — l'inventaire ; [`roadmap.md`](roadmap.md)
— le plan ; [`synthese/index.md`](synthese/index.md) — la théorie ; [`reports/`](../reports/) et
[`journal/`](../journal/) — les preuves et le récit.

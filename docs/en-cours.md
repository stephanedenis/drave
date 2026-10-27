# En ce moment

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 174 fichiers / 242 JSON, 52 documents**), chemins archivés
> corrigés (`docs/archive/`), B10–B12 réintégrés dans les cartes. **Les règles d'`AGENTS.md`
> ne changent pas.** *Spécifique : la date, les compteurs et les lignes ouvertes sont mis à
> jour ci-dessous ; les chiffres B12 restent pilotés par le chantier en cours.*

**Mis à jour : 2026-10-27, 10 h 52 HAE (heure locale, EDT).**

> Cette page dit **où l'on va, ce qui est en cours, où l'on en est, et ce qu'il reste**. Les chiffres, les séries et
> les contrôles vivent dans [`reports/`](../reports/) ; le plan dans [`roadmap.md`](roadmap.md). **Ici, l'actualité
> seulement** — le détail se charge à la demande.

## Où l'on va

**Démontrer que la structure bat la taille, et construire le bus d'événements qui rend les blocs observables,
décomposables, répartissables et rejouables.** Le bus accepte des blocs **neuronaux** (l'intuition, la langue) et
**classiques** (une règle, un solveur, une opération exacte) ; il les rend substituables, comparables et mesurables.
La vision complète est dans [`vision.md`](vision.md).

## Ce qui est en cours

**La phase B12 est mesurée** ; les suites sont dans [`roadmap.md`](roadmap.md).

- **A7 la grappe déportée** — **faite** : le relais rend le même chiffre, la grappe exacte à 21 %, le transport à
  4,22×.
- **B4 les opérateurs abstraits** — **close** : six mesures, dont le LoRA qui **inverse**.
- **A8 l'ordonnanceur place et perte** — **fait, opt-in**.
- **B5/B6 les jeux symboliques** — **faits** : surface → RSN-jeu → pensée, cinq jeux, 112 items.
- **B7/B8 les langues et les maîtres** — **faits** : 71 langues, 449 surfaces, 17 principes, les négatifs nommés.
- **B9 le banc externe** — **mesuré** : DeepSeek sert le langage, `route` reste sur GPU. Le **meilleur écart** de
  distillation est **4,40 % à 31,63 M / 610 exemples** ; la **fenêtre** (3,71 % à 500 pas, 1,29 % à 750, −0,49 % à
  1 000) et le **négatif 30 langues** sont nommés. Détail : [`rapport-deepseek.md`](../reports/rapport-deepseek.md).
- **B10 le protocole sémantique** — **premier passage** : l'**encodeur converge** sur 10 langues (rappel
  **0,426** contre 0,167 ; sonde de langue **0,100**) ; le **décodeur est négatif** (chrF **14,0 / 5,4** contre un plancher **38,8** (référence tronquée)) ; les ablations montrent que `z` 512, le préfixe 64 et 8 unités linéaires n'aident pas, et que `z` est un
  **code d'identité** plus qu'un code de contenu ; le prochain levier est une **attention de requêtes**. Le diagnostic multilingue est sous le plancher. Le raisonnement sur `z` n'est pas
  branché. Protocole : [`protocole-semantique.md`](protocole-semantique.md) ; fiche :
  [`rapport-semantique.md`](../reports/rapport-semantique.md).

- **B11 la base d'universaux typés** — **premier passage** : schéma fixe de **15 champs / 502 classes**,
  sortie déterministe ; le **codec classique** lit **100 %** des coups B5/B7 (79/79, 449/449) et restitue
  la **surface originale** dans **33/79** cas ; le **parseur natif typé** surapprend en réel seul (**48,3 % train / 0 % validation**) mais la
  **distillation synthétique** le débloque : **45,1 %** de code exact sur les **528 surfaces réelles** jamais
  vues, `jeu` **83,1 %**, `de`/`vers` **90,0 / 89,4 %** ; l'**invariance par paire** reste **7,4 %**. La **normalisation lexicale** (concepts canoniques) porte le natif à **55,7 %** de code exact et
  **37,0 %** d'invariance, contre **45,1 % / 7,4 %** ; la **consistance softmax** (38,3 %, invariance 0) et
  l'**adversaire de langue** (39,6 %, invariance 0) restent deux **négatifs**. Le codec reste à **100 %**. Avec le **contexte**, le codec lit **528/528** (100 %) ; sans contexte, **374/528**
  (70,8 %) : le contexte est décisif, et le natif ne le reçoit pas encore. En **suffixe**, le contexte porte le natif à **59,8 %** de code exact et
  **40,7 %** d'invariance ; en **préfixe**, il collapse (0,4 % / 88,9 %) ; en **vecteur séparé**, **59,1 % / 40,7 %**,
  aucun gain. Le verrou restant est `carte` (**69,3 %**) et les ambiguïtés de surface. La **restitution du code
  (aller-retour RSN)** est **100 %** : **79/79** et **449/449** rendus, **aller-retour RSN exact** ; la **surface
  originale** n'est reproduite qu'à **33/79**. Note : [`semantique-universaux.md`](semantique-universaux.md) ; fiche :
  [`rapport-universaux.md`](../reports/rapport-universaux.md).

- **B12 les modules cerveau-langage** — **corrigé** : M1 **528/528** solide ; M2 `de` **93,6 % = 126/126 vus + 10,7/20 inédits**, `point`/`chemin` sous la majorité ; M3 span **tautologique** ; M4 **lookup** (29 codes, 0/6 non stockés) ; M5 action constante ; M6 détection de langue, commutation 0 ; M7 plafond 3,64 %, LFU ; M8 **96,48 % marginal**, exact 65,1 %, baseline par jeu 96,10 %. Détail : [`rapport-cerveau-corrections.md`](../reports/rapport-cerveau-corrections.md).
- **B12 pipeline** — **M1 → M4 → M8** : **528/528** surfaces, **7** prototypes, **96,33 %** de complétion
  sur 120 codes partiels ; test d'intégration, pas de généralisation M4.
- **Bilan B11** : le codec lit **528/528** et la **restitution du code** fait **100 %** d'aller-retour ; la **surface
originale** reste à **33/79** ; le natif normalisé + contexte reste à **59,8 %** de code exact et **40,7 %**
d'invariance ; le raisonnement n'est **pas branché**. Bilan : [`bilan-b11.md`](../reports/bilan-b11.md).

## Les chiffres de l'état

> **Source unique.** Ces cinq valeurs sont vérifiées par `tools/revue_documentation.py` ; les
> autres pages y renvoient au lieu de les recopier.

| invariant | valeur | contrôle |
|---|---:|---|
| portes | **49** (47 vertes, 2 structurelles) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/synthese/0*.md` |
| fichiers / JSON de résultats | **174** / **242** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **52** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 34** (26/10 14 h 30) | `docs/references-non-regression.md` |

## Où l'on en est

| | |
|---|---:|
| portes (passe complète) | **49** — **47 vertes, 2 structurelles** (26/10 14 h 30) |
| porte-deepseek | **verte** (20 tests), incluse dans la passe |
| fichiers / JSON de résultats | **174** / **242** |
| la sonde, au pic du 1,5 B | **0,7256** (XNLI) |
| le pont, au pic du 14 B | **0,8715** — il plafonne à 0,87 |
| la sémantique des jeux (B5/B6) | **112 items, 100 % au niveau 4, 33/33 paires** |
| les langues (B7) | **71 langues, 35 concepts, 449/449, 11/11** |
| les maîtres (B8) | **d4, livre 10/10, go 9×9 10/10, dames 0 défaite, cartes 44,7 % (négatif)** |
| le banc externe (B9) | **DeepSeek 310/310, chrF 82,82 contre 15,64 ; 31,63 M/610 : 4,40 %** |
| le protocole sémantique (B10) | **encodeur 0,426 contre 0,167 ; décodeur négatif 14,0/5,4 contre 38,8** (référence tronquée) |
| la base typée (B11) | **codec 100 %** (79/79, 449/449) ; natif **59,8 % / 40,7 %** ; surface **33/79** |
| les modules cerveau-langage (B12) | **M1 528/528 ; M2 98,6/93,2 ; M8 96,48 %** ; M5/M6/M7 négatifs |

## Les sept chantiers, en une ligne

| chantier | état |
|---|---|
| **C1** corpus et généalogie | ✅ fait (UDHR, Glottolog) |
| **C2** traduction | ✅ mesuré (juge, plancher, marge) |
| **C3** restitution | ✅ mesuré ; **C3.2** : un module par famille, **4/5** au-dessus de la référence |
| **C4** dialectes et styles | ✅ mesuré ; la date reste à contrôler |
| **C5** qualité par domaine | ✅ six registres + dialogue spontané |
| **C6** documentation | ✅ fait — revue du 27/10 : compteurs et chemins corrigés (passe 2) |
| **C7** pensée abstraite | ✅ mesuré — la carte, **B4** close, **B5/B6** faits, **B10–B12** premier passage |

## Ce qui reste

**Court terme** — les lignes ouvertes, non bloquées : **B10.3** (un décodeur au-dessus du plancher, puis le
raisonnement sur `z`), **B12.10** (M2 équilibré + contexte, M3 répétitions, M5 ordre 2, M6 conflit, M7 capacité,
M8 rejeu), et les suites de **B9** (**31,63 M / 610 à 750/1 000 pas**, **plus de données avec la capacité**, le
**masque dans le trainer**, l'**export du 31,63 M** vers le moteur).

**Moyen terme** — les suites des jeux hors plan (corpus externe, MCTS budgété, portage Rust), les **9 familles** de
C3, la **prose scientifique** (bloquée par le corpus), le **FPGA**, la **démonstration distante** (compte Colab), le
**MoE** local.

**Objectif final** — une entrée-sortie **fiable** (étage 1), puis une **pensée abstraite** jugée sur des
**opérations** (étage 2) ; un moteur **décomposable, répartissable, observable et rejouable**, tenu par ses mesures.

## Les questions ouvertes

- **Bloquées par une ressource** : B1.5 (corpus scientifique humain), A3.4 (compte Colab), A5.4 (carte Stratix V),
  A6.2 (MoE local).
- **Ouvertes sans blocage** : **B10.3** (décodeur au-dessus du plancher), **B12.10** (les six suites des modules),
  le **pic du 32 B** (nommé, non forcé), les limites des jeux (détection sur cases seules, ko simple, MCTS à
  60 playouts), le **portage Rust** du contrat RSN.
- **Tranchée** : les styles à époque contrôlée — la surface capte l'époque (+0,138) plus que la filiation (+0,049) ;
  c'est une règle de méthode.

## La carte

[`carte.md`](carte.md) — les sujets, bloc par bloc ; [`README.md`](README.md) — l'inventaire ; [`roadmap.md`](roadmap.md)
— le plan ; [`synthese/index.md`](synthese/index.md) — la théorie ; [`reports/`](../reports/) et
[`journal/`](../journal/) — les preuves et le récit.

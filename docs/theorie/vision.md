# Drave — la vision

> *« Stream of logs »* : le flux des listes. Et, en français d'ici, **la drave** — ces billots qu'on confiait à la
> rivière au printemps, qu'on guidait de l'estacade jusqu'à la scierie. Le nom dit ce que fait ce moteur : il ne lit
> pas des matrices, il conduit un flux.

Ce document dit **ce que le projet cherche**, et ce qu'il refuse. Les chiffres, les protocoles et les comptes rendus
vivent dans [`reports/`](../../reports/) ; l'état courant dans [`en-cours.md`](../pilotage/en-cours.md) ; le plan dans
[`roadmap.md`](../pilotage/roadmap.md). Ici : ce qui reste vrai quand les chiffres changent.

## La raison d'être

**Drave est un bus d'événements pour l'IA.** Les activations d'un réseau sont des **faits** — « le neurone 2 539 de
la couche 23 a valu 27,8 » —, regroupés en **listes valuées poussées** vers leurs lecteurs. Le coût du calcul devient
proportionnel à l'**activité**, pas à la taille du modèle ; le modèle devient **observable**, **décomposable**,
**répartissable** et **rejouable**.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de les
**combiner**, de les **décomposer en blocs** exécutables par du matériel divers, voire **distribué en réseau**, de les
**diagnostiquer** et de **rejouer** des événements.

**La thèse : la structure bat la taille.** Un pont linéaire, une grille de conversion, un routage de blocs valent
mieux que des paramètres ajoutés. La mesure a déjà tranché plusieurs fois dans ce sens : la sonde est **plate dès
1,5 B**, le pont **plafonne à 0,87** ; à profondeur fixe, le 14 B est **dernier** (0,4833). Le détail est dans
[`reports/README.md`](../../reports/README.md).

## Le bus, en cinq propriétés

1. **Un bloc est une unité de conception.** Il a des entrées et des sorties **typées**, un coût mesurable, et une
   trace. Un bloc peut être **neuronal** (l'intuition, la langue, la perception) ou **classique** (une règle, un
   solveur, un index, un compilateur) — le bus ne fait pas la différence.
2. **Il est substituable.** Deux implémentations du même contrat — un réseau et un algorithme, deux architectures,
   deux quantifications — se remplacent **sans toucher au bus**. C'est ce qui rend la comparaison honnête : même
   entrée, même sortie attendue, même trace.
3. **Il est observable.** Un flux est un **journal de faits** : on peut compter, tracer, différencier deux versions,
   et savoir *où* le calcul diverge, pas seulement *qu'il* diverge.
4. **Il est répartissable.** Un bloc va là où son entrée est déjà, ou là où elle coûte le moins à amener. Le
   découpage suit les **poids** (2,669 Go par jeton pour V4-Flash contre 65 536 octets d'activation), pas une
   intuition.
5. **Il est rejouable.** Une trace stable, un format de rejeu, des portes de non-régression : le même événement
   redonne le même résultat, et une modification se juge sur pièce.

**L'hybridation est le point, pas un détail.** Là où l'informatique classique est plus fiable et plus performante —
une opération arithmétique, une recherche exhaustive, une règle de jeu, un tri —, elle doit être un **bloc
classique** à part entière, branché sur le même bus. Là où l'intuition est un avantage — reconnaître, traduire,
résumer, proposer —, un **bloc neuronal**. Le bus fournit le contrat, la trace et la mesure ; il ne force ni l'un ni
l'autre.

## Deux programmes, un seul projet

### Le moteur

Le bus, les blocs, l'ordonnanceur, le transport, les formats, le rejeu, les portes. Il avance par ses propres
mesures et ne dépend pas de l'avancement de l'intelligence. Ses cinq axes restent les questions du bus : observer et
régler, placer sur une machine, répartir en réseau, rejouer et comparer, choisir formats/matériels/énergie.

### L'intelligence

L'application, branchée sur les mêmes blocs. **Deux étages, dans cet ordre** :

1. **L'entrée-sortie linguistique** — lire et produire toutes les langues, dialectes et styles, jugée en **qualité
   de traducteur**. C'est un **bloc de langue** (surface → représentation sémantique neutre, RSN) que l'on peut
   comparer à d'autres architectures.
2. **La pensée abstraite, indépendante de la langue** — représenter, composer, inférer, planifier. Elle se juge sur
   des **opérations**. C'est là que l'hybridation est la plus utile : un bloc neuronal pour la représentation, un
   bloc classique pour l'opération exacte.

**Dans l'intelligence, l'ordre est strict** : l'étage 2 ne se bâtit pas sur une entrée-sortie qui n'est pas fiable.
Mais le **moteur** est indépendant : il avance en parallèle, et c'est lui qui rend l'intelligence **observable**.

## Ce que la mesure a déjà tranché

- **La sparsité ne gagne pas toujours** : le croisement push/pull est mesuré à ~22 % de densité ; en dessous, les
  listes gagnent, au-dessus, le dense. Le moteur garde **les deux chemins** et choisit par la mesure.
- **Les jeux et les langues se représentent** : B5/B6 (surface → RSN-jeu → pensée) et B7/B8 (71 langues,
  maîtres) sont mesurés ; les négatifs sont nommés, notamment les cartes.
- **Le natif a un seuil, une fenêtre et une limite** : la distillation native passe par un seuil de capacité
  (9,23–9,96 M), un meilleur écart **4,40 % à 31,63 M / 610 exemples**, une **fenêtre** (3,71 % à 500 pas, 1,29 %
  à 750, −0,49 % à 1 000) et un **négatif à 30 langues**. La capacité ne paie **qu'avec les données**.
- **Le langage peut sortir des GPU** : DeepSeek sert le professeur et le juge ; les GPU restent au natif. Le banc
  est mesuré, les contrôles sont dans la fiche.

Les détails, les séries et les contrôles : [`reports/rapport-deepseek.md`](../../reports/rapport-deepseek.md),
[`reports/rapport-langues-maitres.md`](../../reports/rapport-langues-maitres.md),
[`reports/rapport-jeux-symboliques.md`](../../reports/rapport-jeux-symboliques.md).

## Ce que la vision n'est pas

- **Ce n'est pas « le sparse gagne toujours »** : le dense est un chemin de première classe, mesuré.
- **Ce n'est pas « un seul modèle »** : le bus accepte des blocs d'architectures différentes, neuronaux ou
  classiques, à condition qu'ils tiennent le contrat.
- **Ce n'est pas « distribuer est gratuit »** : le transport est fidèle, mais l'ordonnanceur complet et la
  démonstration distante restent des chantiers nommés.
- **Ce n'est pas « plus gros = mieux »** : la sonde sature dès 1,5 B ; la taille sans données ni structure ne paie
  pas.
- **Ce n'est pas un modèle de langue** : la langue est **une famille de blocs**, pas le projet.

## Comment on saura que c'est tenu

1. Un bloc **neuf** se branche sur le bus, avec son contrat et sa trace, **sans modifier le bus**.
2. Un bloc **classique** et un bloc **neuronal** coopèrent sur la même tâche, et l'A/B les départage.
3. Une **substitution** (architecture, quantification, algorithme) se mesure sur la même trace, avec le même jeu de
   portes.
4. Un **rejeu** redonne le même résultat, et le diff dit **où** il diverge.
5. Le coût d'un bloc suit son **activité**, pas seulement sa taille.

## Le nom

**Drave** : le flux qu'on conduit, du bassin de flottage jusqu'à la scierie. Le mot porte les trois propriétés du
document — il **coule**, il se **répartit**, il se **surveille**. Le renommage est fait (2026-09-30) ; l'histoire des
trois âges est dans [`histoire.md`](histoire.md).

## Où lire la suite

- **Comprendre** : [`agent/mission.md`](../methode/mission.md) · [`protocole-semantique.md`](protocole-semantique.md) ·
  [`glossaire.md`](glossaire.md) · [`synthese/index.md`](synthese/index.md).
- **Faire** : [`agent/`](../methode/) · [`organisation-du-depot.md`](../methode/organisation-du-depot.md) ·
  [`utilisation.md`](../pilotage/utilisation.md).
- **L'état et les preuves** : [`en-cours.md`](../pilotage/en-cours.md) · [`roadmap.md`](../pilotage/roadmap.md) ·
  [`reports/README.md`](../../reports/README.md) · [`journal/`](../../journal/).
- **L'histoire et les plans archivés** : [`archive/README.md`](../archive/README.md) — **facultatif**.

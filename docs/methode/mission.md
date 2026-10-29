# La mission, la stratégie et l'ordre des priorités

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). Il développe **la mission** ; les règles
> opérationnelles restent dans `AGENTS.md`, les résultats dans [`reports/`](../../reports/), l'état dans
> [`en-cours.md`](../pilotage/en-cours.md), le plan dans [`roadmap.md`](../pilotage/roadmap.md).
>
> **Vocabulaire** : *couche* = **couche de neurones** ; *étage* = **niveau d'architecture** (étage 1 entrée-sortie,
> étage 2 pensée) ; *jeton* = unité du **tokeniseur**, jamais la **représentation sémantique neutre (RSN)**, faite
> d'**unités de sens**. Voir le [glossaire](../theorie/glossaire.md).

## La vision, en une page

**Drave est un bus d'événements pour l'IA.** Les activations sont des **faits** — « le neurone 2 539 de la couche 23
a valu 27,8 » — regroupés en **listes valuées poussées** vers leurs lecteurs : le coût suit l'**activité**, pas la
taille du modèle. Le modèle devient **observable**, **décomposable**, **répartissable** et **rejouable**.

Le bus traite les **blocs** de la même façon, qu'ils soient **neuronaux** (l'intuition, la langue, la perception) ou
**classiques** (une règle, un solveur, un index, une opération exacte). Un bloc a un **contrat**, une **trace**, un
**coût** ; il est **substituable** et **comparable** sans toucher au bus. C'est l'hybridation qui donne au projet sa
portée : le neuronal là où l'intuition paie, le classique là où la fiabilité et la performance sont meilleures.

**La thèse : la structure bat la taille.** Un pont linéaire, une grille de conversion, un routage de blocs valent
mieux que des paramètres ajoutés. La mesure a déjà tranché : la sonde est **plate dès 1,5 B**, le pont **plafonne à
0,87**, et à profondeur fixe le 14 B est **dernier**. Le détail est dans [`reports/`](../../reports/).

## Les deux programmes

> La **roadmap** découpe ces deux programmes en **quatre chantiers** : **A** (moteur), **B** (intelligence),
> **N** (natif) et **R** (lecteur). Les deux programmes de la vision restent l'ordre : le moteur et l'intelligence
> ne se bloquent pas l'un l'autre ; N et R sont les lignes qui les rendent mesurables.

### Le moteur

Le bus, les blocs, l'ordonnanceur, le transport, les formats, le rejeu, les portes. Il avance par ses propres mesures
et ne dépend pas de l'avancement de l'intelligence. Ses cinq questions restent celles du bus : observer et régler,
placer sur une machine, répartir en réseau, rejouer et comparer, choisir formats/matériels/énergie.

### L'intelligence

L'application, branchée sur les mêmes blocs. **Deux étages, dans cet ordre** :

1. **L'entrée-sortie linguistique** — lire et produire toutes les langues, dialectes et styles, jugée en **qualité
   de traducteur**. C'est le **bloc de langue** (surface → RSN), comparable à d'autres architectures.
2. **La pensée abstraite, indépendante de la langue** — représenter, composer, inférer, planifier, jugée sur des
   **opérations**. C'est là que l'hybridation est la plus utile : un bloc neuronal pour la représentation, un bloc
   classique pour l'opération exacte.

**Dans l'intelligence, l'ordre est strict** : l'étage 2 ne se bâtit pas sur une entrée-sortie qui n'est pas fiable.
Mais le **moteur** est indépendant : il avance en parallèle, et c'est lui qui rend l'intelligence **observable**.

## L'ordre des priorités

L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date — la feuille de route vivante est
[`roadmap.md`](../pilotage/roadmap.md) :

- **les deux programmes en parallèle** : le moteur et l'intelligence ne se bloquent pas l'un l'autre ;
- **dans l'intelligence, l'étage 1 d'abord** ; chaque mesure de l'étage 2 qui touche à la langue se double d'une
  mesure de l'étage 1 ;
- **la file « jamais en attente »** : si une ligne est bloquée (corpus, compte, matériel), on prend la suivante.

## Le temps est un plancher, pas un plafond

*Carpe diem* ([`relations-humaines.md`](relations-humaines.md) § Addendum) : on ne s'arrête pas parce qu'une
échéance est passée ; on s'arrête quand c'est **fait, mesuré et écrit**. Une journée sans mesure ni commit est une
journée perdue — et une mesure sans fiche sera refaite.

## Ce que « perfectible » veut dire

Un **étage** est perfectible tant qu'un **chiffre reproductible** montre qu'il peut mieux faire — sur une langue, un
domaine, un style, un bruit d'entrée, une taille. Un **bloc du moteur** est perfectible tant qu'un chiffre montre un
coût évitable : un repli CPU, un seuil codé en dur, une allocation qui ne paie pas. « Perfectible » n'est pas une
impression : c'est un **écart mesuré** entre ce qu'on sait faire et ce que la vision demande.

## Où est l'état

[`en-cours.md`](../pilotage/en-cours.md) — la page qu'on lit si on ne lit qu'une page ; le plan est
[`roadmap.md`](../pilotage/roadmap.md).

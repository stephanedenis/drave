# 1. Le cerveau Drave — l'idée, en cinq minutes

> **Périmètre** : ce chapitre relève du programme **moteur** ; la vision est dans [`docs/vision.md`](../vision.md), la roadmap dans [`docs/roadmap.md`](../roadmap.md).

## Le problème de départ

Un grand modèle de langue est **un seul bloc** : 24, 32, 80 couches, l'une après l'autre, sur une seule
machine, dans un seul ordre. On ne peut pas le répartir, on ne peut pas lui demander de répondre vite en
sautant des couches, on ne peut pas l'endormir, on ne peut pas le priver de mémoire en temps de crise.

**Drave répond à une question simple** : *et si on le traitait comme un cerveau — avec des régions, des
liaisons, des horloges, des budgets et de la mémoire — sans le réentraîner ?*

## L'image

![Drave en une image](schemas/vue-ensemble.svg)

Trois idées y sont dessinées :

* **on coupe** le modèle en **régions** (des groupes de couches) ;
* **on les relie** par un **bus** (des messages de taille fixe) ;
* **et un « cerveau »** — une couche logicielle, pas des poids — les **organise** : horloges, budgets,
  mémoire, sommeil, pannes.

Le calcul, lui, ne change pas : ce sont les **mêmes poids**, dans le **même ordre** si on veut. Drave ne
remplace pas le modèle ; il le **met en scène**.

## La mesure qui rend tout possible

Si couper un modèle change sa perplexité, tout s'écroule. C'est donc la **première** chose qui a été
mesurée : **huit coupes, une seule perplexité** — le modèle coupé en régions qui se parlent donne le même
résultat que le modèle entier (113,0068 dans les deux cas).

![L'anatomie d'une coupe](schemas/anatomie-coupe.svg)

Et le schéma dit la nuance qui compte : **couper tôt coûte cher** (+17 %), **couper tard ne coûte
presque rien** (+0,5 %). La raison est simple à voir : les premières couches transforment des mots en
nombres ; les dernières transforment des nombres en mots. Un état qui sort d'une couche 3 est encore
« du mot » ; un état qui sort d'une couche 16 est déjà « du sens ». Couper tard, c'est couper là où
l'information est **dense** — et une information dense se transporte.

## Ce que ça permet, et qui ne marchait pas avant

| sans Drave | avec Drave |
|---|---|
| un modèle par machine | le même modèle **réparti**, avec un état à transporter |
| on attend la fin | on peut **court-circuiter** (le réflexe) et répondre plus vite |
| pas de mémoire | une **mémoire** de travail et épisodique, mesurée |
| pas de consolidation | un **sommeil** qui consolide ce qui a servi |
| pas de budget | des **budgets** par région, et des compteurs qui disent où passe le temps |

## Comment on sait que c'est vrai

Chaque affirmation ci-dessus a **une fiche** dans `reports/` et **une porte** dans `tools/`. Par exemple :
`porte-coupe.sh` vérifie que huit découpages donnent la même perplexité ; `porte-flux.sh` que le bus
transporte bien l'état ; `porte-reflexe.sh` que le moteur **refuse** un adaptateur sans tête, plutôt que de
l'ignorer silencieusement.

Et la règle de lecture du dépôt : **une porte qui ne peut pas échouer ne vaut rien** — elle a été appliquée
à la lettre, et deux portes qui ne pouvaient pas échouer ont été trouvées et corrigées.

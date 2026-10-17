# 2. L'anatomie interne — ce qui circule, et où

## Les quatre pièces

| pièce | ce que c'est | en une phrase |
|---|---|---|
| **région** | un groupe de couches consécutives | elle lit un état, calcule, écrit un état |
| **lien** | un canal entre deux régions | il transporte un état, pas des mots |
| **bus** | le canal partagé | des messages de taille fixe, avec des priorités |
| **horloge** | un compteur par région | chaque région peut battre à son rythme |

## L'état, la seule monnaie d'échange

Ce qui circule entre régions n'est pas du texte : c'est un **vecteur de 896 nombres** (pour le modèle de
0,5 milliard de paramètres). On l'appelle l'**état** ou le **résidu**. C'est la même chose que ce que le
modèle calcule en interne à chaque position.

* Un état peut être **écrit** (`--etat-sortie`), **relu** (`--etat-entree`) et **injecté** dans un autre
  moteur, à une position choisie.
* Un état **contient du sens** : on sait lire, dans un état, non seulement le mot suivant, mais la
  **trajectoire** des 16 jetons à venir (mesuré : 80,3 % de reconstitution, contre 118,4 % pour le mot que
  le modèle aurait dit).

## Les trois découpages qui marchent

![L'anatomie d'une coupe](schemas/anatomie-coupe.svg)

| découpage | coût du pont | usage |
|---|---|---|
| **0-3 / 4-23** | +17,09 % | à éviter : la région haute a besoin de plus de contexte |
| **0-15 / 16-23** | +0,52 % | le découpage de référence |
| **0-19 / 20-23** | +0,52 % | le réflexe : une région courte et rapide |

Le **pont** est ce qui raccorde deux régions. Le dépôt a mesuré qu'avec **448 fibres** le pont coûte
**+2,81 %** de perplexité et **divise par 1,8** les octets échangés — c'est-à-dire que le pont peut être
**étroit** sans être **mauvais**.

## Les horloges, et pourquoi elles ne changent pas le résultat

Chaque région peut battre à son rythme (deux régions sur trois, une sur deux…). Ce qui est mesuré : le
résultat **ne change pas**, mais le **coût** change. Une horloge n'est donc pas une approximation : c'est
une **politique de dépense**.

## Ce qui se passe quand ça casse

| panne | ce que le cerveau fait | ce qui est mesuré |
|---|---|---|
| une région muette | on continue avec les autres | la perplexité se dégrade **progressivement**, jamais d'un coup |
| un lien lent | on baisse la priorité | le résultat est identique, le temps non |
| un budget dépassé | on coupe la région la plus chère | on sait **où** passe le temps, par région |

*Le principe est le même partout : une panne doit **dégrader**, pas **casser**.*

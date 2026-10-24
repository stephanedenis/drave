# La vision, la mission et l'ordre des priorités

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). Il développe **la vision et la mission** ; les
> règles opérationnelles restent dans `AGENTS.md`, les résultats dans [`reports/`](../../reports/), la feuille de
> route dans [`roadmap.md`](../roadmap.md).
>
> **Vocabulaire** : *couche* = **couche de neurones** ; *étage* = **niveau d'architecture** (étage 1 entrée-sortie,
> étage 2 pensée) ; *jeton* = unité du **tokeniseur**, jamais la **représentation sémantique neutre (RSN)**, faite
> d'**unités de sens**. Voir le [glossaire](../glossaire.md).

## La vision

**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Un moteur qui traite les
activations d'un réseau comme des **faits** — « le neurone 2 539 de la couche 23 a valu 27,8 » —, regroupés en
**listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, pas à la
taille du modèle ; le modèle devient **décomposable**, **répartissable** et **observable** — on peut le tracer, le
rejouer, le comparer.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de
les **combiner**, de les **décomposer en couches et grappes de neurones** exécutables par du matériel divers, voire
**distribué en réseau**, de les **diagnostiquer et faire évoluer** en étudiant leurs **flux**, et de **rejouer à
volonté** des événements. L'ambition : des modèles **plus légers, plus flexibles, plus puissants**, **très flexibles
sur le matériel** qui les supporte.

**La thèse, en une phrase** : la **structure** bat la taille — un pont linéaire, une grille de conversion, une carte
des flux valent mieux que des paramètres ajoutés. **Elle est désormais mesurée** : la sonde est plate dès le 1,5 B
(0,7256 / 0,7269 / 0,7189 / 0,7376), le pont plafonne à 0,87, et à profondeur fixe le 14 B est **dernier** (0,4833) —
dix fois la taille pour +0,001. Ce qui reste à éprouver, c'est **où** elle tient : par tâche, par opération, par
registre.

## Deux programmes, un seul projet

### Le programme du moteur (les flux)

L'origine et le cœur. Cinq **axes**, chacun mesuré par ses propres chiffres :

1. **Observer et régler**, neurone par neurone (le flux comme objet de première classe, le diff par couche) ;
2. **Répartir sur la machine** (KV paginé, attention GPU, tête, experts) ;
3. **Répartir en réseau** (le transport fidèle, les listes comme unités de travail, le placement) ;
4. **Rejouer et comparer** (les portes, les références indépendantes, le diff) ;
5. **Formats, matériels, énergie** (les trois matériels, la quantification choisie par la mesure).

Il avance **par ses propres mesures** et ne dépend pas de l'avancement de l'intelligence.

### Le programme de l'intelligence (les deux étages)

L'application, par-dessus les flux. **Deux étages, dans cet ordre** :

1. **L'entrée-sortie linguistique** — lire et produire **toutes** les langues, dialectes et styles, dans les
   registres **techniques, littéraires, juridiques, quotidiens**. On la juge en **qualité de traducteur**
   (*restitution* à l'identique, *traduction* du sens). On ne « déclare complet » que sur des **chiffres** qui
   couvrent langues, dialectes, styles et domaines.
2. **La pensée abstraite, indépendante de la langue** — **seulement après** une entrée-sortie fiable. On la juge
   sur des **opérations** : représenter, composer, inférer, planifier. C'est le sens de « penser sans verbaliser » :
   lire la réponse dans l'**état**, avant et sans la génération.

**Dans l'intelligence, l'ordre est strict** : l'étage 2 ne se bâtit pas sur une entrée-sortie qui n'est pas fiable.
Mais le **moteur** est indépendant : il avance en parallèle, et c'est lui qui rend l'intelligence **observable**.

## La stratégie révisée (24/10)

Les 173 mesures ont déplacé le centre de gravité du projet. **Trois constats, trois décisions :**

1. **L'échelle a rendu son verdict** : la sonde sature dès le 1,5 B, le pont plafonne à 0,87, et le pic du 32 B
   coûte 10-20 h pour un point que trois courbes ont déjà tranché. → **On arrête de courir après l'échelle** : le pic
   du 32 B reste **nommé**, pas planifié.
2. **L'étage 1 est tenu** (six registres, 24 langues, le dialogue spontané) ; l'étage 2 a sa **carte** (l'état porte
   le raisonnement, le pont l'aligne, le plan résiste). Ce qui manque à l'étage 2, ce sont les **opérateurs** : les
   opérations abstraites (composer, inférer, ordonner) que la carte ne mesure pas encore. → **B4, les opérateurs
   abstraits.**
3. **Le moteur a sa règle de placement et sa porte de greffe** (l'injection d'état est branchée) — mais il n'exécute
   encore **aucune couche ailleurs**. C'est pourtant le cœur de la vision : la **grappe déportée**, et l'ordonnanceur
   qui porte la place **et** la perte. → **A7 et A8.**

**L'ordre de la nouvelle phase** : **A7** (la grappe, la plus proche de la vision), **B4** (les opérateurs, le plus
neuf scientifiquement), **A8** (l'ordonnanceur, le plus ingénieur). Tout le reste est **nommé** ou bloqué.

## L'ordre des priorités

L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date — la feuille de route vivante est
[`docs/roadmap.md`](../roadmap.md) :

- **les deux programmes en parallèle** : le moteur et l'intelligence ne se bloquent pas l'un l'autre ;
- **dans l'intelligence, l'étage 1 d'abord** (tant qu'il a des trous mesurés, l'étage 2 attend) ; chaque mesure de
  l'étage 2 qui touche à la langue se double d'une mesure de l'étage 1 ;
- **la file « jamais en attente »** : si une ligne est bloquée (corpus, compte, matériel), on prend la suivante.

## Le temps est un plancher, pas un plafond

*Carpe diem* ([`relations-humaines.md`](../relations-humaines.md) § Addendum) : on ne s'arrête pas parce qu'une
échéance est passée ; on s'arrête quand c'est **fait, mesuré et écrit**. Une journée sans mesure ni commit est une
journée perdue — et une mesure sans fiche est une mesure qui sera refaite.

## Ce que « perfectible » veut dire

Un **étage** est perfectible tant qu'un **chiffre reproductible** montre qu'il peut mieux faire — sur une langue, un
domaine, un style, un bruit d'entrée, une taille de modèle. Un **axe du moteur** est perfectible tant qu'un chiffre
montre un coût évitable : un repli CPU, un seuil codé en dur, une allocation qui ne paie pas. « Perfectible » n'est
pas une impression : c'est un **écart mesuré** entre ce qu'on sait faire et ce que la vision demande.

## Où est l'état courant

[`docs/en-cours.md`](../en-cours.md) — la synthèse en tête, puis le tableau de bord ; la feuille de route vivante
est [`docs/roadmap.md`](../roadmap.md). C'est la page qu'on lit si on ne lit qu'une page.

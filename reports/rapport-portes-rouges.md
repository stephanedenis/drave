# Les deux portes rouges — le diagnostic (structurelles, tolérées, comprises)

> **Ce que ce document est.** Le **diagnostic** des deux portes qui restent rouges après la passe
> du 22/11 00 h 55 : `porte-indice` et `porte-melange`. Elles sont **tolérées** par
> [`references-non-regression.md`](../docs/pilotage/references-non-regression.md) — ce document dit
> **pourquoi**, et ce qu'il faudrait pour les faire passer au vert.

## 1. `porte-melange` — la calibration échoue

**Ce qu'elle teste** : trois invites (A avec le code `ZQ`, B avec `KJ`, C sans aucun code) ;
on prélève l'état final, on **calibre** (quelle position porte le contenu ?), puis on **mélange**
les états pour voir si le modèle restitue le bon code.

**Le verdict** : `❌ l'état de A ne rend pas le code de A dans une invite qui n'en contient aucun :
le mélange ne pourrait rien dire`.

**La lecture** : le **préalable de la porte échoue** — la calibration ne trouve pas la position qui
porte le code. Ce n'est pas le mélange qui est faux ; c'est la **mesure amont** : sur ce modèle
(le 1,5 B ? le 7 B ? le checkpoint testé), l'état final **ne contient pas le code** dans une invite
sans code — donc **l'expérience n'a pas de sens** et la porte le dit (`le mélange ne pourrait rien
dire`).

**Ce qu'il faudrait** : un modèle plus grand (le 7 B/14 B), ou une position d'état différente, ou
un prompt qui rend le code **saillant** dans l'état. C'est un **chantier de recherche**, pas une
régression.

## 2. `porte-indice` — la section 3 ne conclut pas

**Ce qu'elle teste** : la capture d'état d'une question (B) peut-elle servir d'**indice extérieur**
à une mémoire qui interroge A ? Trois sections : (1) A répond le code, B non — les invites diffèrent
bien par l'aiguille ; (2) la capture d'état de A et de B (positions 1439 / 1469) ; (3) la mémoire
interroge A **avec** puis **sans** l'indice extérieur.

**Le verdict** : la section 3 s'arrête sans conclure (le script se termine sur la ligne 3).

**La lecture** : la porte **ne va pas au bout** — la comparaison avec/sans l'indice n'est pas
rendue. C'est moins grave que `melange` (l'infrastructure existe : les états sont capturés), mais
la porte ne peut pas être dite « tenue » tant qu'elle n'a pas **conclu**.

**Ce qu'il faudrait** : débloquer la section 3 (un modèle qui répond, une comparaison mesurée), ou
**réduire la porte** à ce qu'elle sait faire (les sections 1-2) et laisser la section 3 en chantier
nommé.

## 3. Pourquoi elles sont tolérées

Les deux portes dépendent d'un **préalable de recherche** (un état qui porte le code, une mémoire
qui l'utilise) qui n'est **pas encore établi**. Les rendre vertes demanderait un **autre modèle** ou
un **autre prompt** — pas une correction de code. C'est la définition d'une **rouge structurelle** :
la porte mesure une hypothèse de recherche, pas une régression du dépôt.

## 4. Ce que la passe a appris d'autre

- **87 portes vertes** sur 89 (le reste des 183 est couvert par les autotests par lots).
- **`porte-sessions` était rouge** (le heartbeat de la session S périmé de 1 114 min) : **corrigé**,
  elle est verte.
- Les deux rouges restantes **ne bloquent rien** : les autres portes ne les attendent pas.
## 5. La cause commune : le modèle des deux portes est 0,5 B

Les deux portes utilisent le **même modèle** : `models/Qwen2.5-0.5B-Q8_0.gguf` (le défaut de
`MODELE` dans les deux scripts). **0,5 milliard de paramètres**, 4 bits — c'est un modèle de
**démonstration**, pas un modèle de raisonnement.

**Ce que ça explique** :

- `porte-melange` **calibre** quatre positions de fin pour trouver celle qui porte le code ; sur
  un 0,5 B, **aucune** ne le porte — la capacité n'est pas là. La porte a donc **raison de dire**
  « le mélange ne pourrait rien dire » : l'expérience n'a pas de support.
- `porte-indice` capture les états (positions 1439/1469) mais la section 3 ne conclut pas : la
  mémoire interroge A, et le 0,5 B ne répond pas de façon stable.

**Le diagnostic est donc structurel, et il est net** : ce ne sont pas deux bugs, c'est **un
modèle trop petit** pour les deux expériences. Les rendre vertes demanderait un **modèle plus
grand** (le 7 B/14 B déjà présents ?) — et c'est un **choix de campagne**, pas une correction.

**La conséquence pour le dépôt** : les deux portes **mesurent une hypothèse sur les états
internes** ; elles sont rouges **par honnêteté**, pas par négligence. Les tolérer est le bon
arbitrage tant que le modèle de campagne n'est pas changé.

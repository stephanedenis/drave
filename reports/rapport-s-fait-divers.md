# S — Le fait divers est tranché : 61/61 types, 144/144 rôles ; la tête du GN arrête le verbe

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : « Le fait divers surprend »
> ne coupe plus le verbe dans le GN. La règle v7 suit la **tête du GN** — dès qu'un nom est vu,
> un homographe qui suit un adjectif n'est plus le nom — et accepte un adjectif après
> l'homographe quand le verbe vient après. Le gold gagne `h061` (sixième vague) : **61/61
> types**, **144/144 rôles**, **50/50 compléments**, couverture **1,00** ; les contrôles restent
> à **104/144**, **106/144** et **0,10**. Les **56 tests** passent.

## La règle

L'analyseur butait sur « Le fait divers surprend » : « fait » est un homographe nom/verbe,
« divers » est un adjectif, et « surprend » un verbe. La v6 traitait « surprend » comme le nom
final (règle « adjectif + fin de phrase »), avalant tout le groupe. La v7 introduit la **tête du
GN** : dès que le GN a un nom (« fait », ou « lit » après « grand »), l'homographe suivant qui
vient après un adjectif n'est plus un nom — c'est le verbe, et le GV s'ouvre. La règle accepte
aussi l'adjectif **après** l'homographe (« fait **divers** ») quand le verbe suit. « divers »
entre dans le lexique d'adjectifs.

## Le gold et la mesure

`h061` rejoint le holdout (sixième vague, écrite après la règle et mesurée une fois) :
« Le fait divers surprend » → `GN « Le fait divers »` + `GV « surprend »`. La mesure donne
**61/61 types**, **144/144 rôles**, **50/50 compléments**, couverture **1,00** ; la holdout
seule : 38/38, 82/82, 21/21. Les contrôles : baseline **104/144** (0,722), règles coupées
**106/144** (0,736), rôles mélangés **0,10** [0,00 ; 0,24].

## Ce qui pourrait le rendre faux

La règle dépend d'un **lexique d'adjectifs** : un adjectif absent (« Le fait étrange surprend »)
retomberait sur l'ancien découpage ; la tête du GN est une heuristique, pas une analyse
morphologique. Le gold est de la même main que la règle, et la vague 6 a été écrite après elle.
Les 61 phrases restent un instrument de cohérence, pas de généralité. Les autres limites de la
traduction demeurent : « de très-bons conseils » (GP français, objet direct anglais) et
« Lequel est-ce ? » (*Which way?*).

## La suite

La validation des neuf paragraphes sur `/paragraphes` (référents puis structure) reste le geste
humain ; la rétro-traduction API quand la clé sera là ; les 71 langues de l'UDHR ; et la
prochaine limite de l'analyseur — le nom après un adjectif hors lexique, précisément.

## Fichiers

- Sous-module : `generateur.py` (tête du GN, adjectif après l'homographe), `donnees/gold-analyseur.json`
  (h061, 61 phrases), `donnees/mesure-analyseur.json`, `tests/test_generateur.py`, README ; **56 tests**.
- Fiche : celle-ci ; état, roadmap et plan mis à jour.

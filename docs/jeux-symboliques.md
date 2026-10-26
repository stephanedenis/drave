# Les jeux symboliques — de la surface au sens, puis à la pensée

> **Ce que ce document est.** Le **bloc de langue et de jeux** du bus : comment une surface (une notation, une
> phrase, un diagramme) devient une **représentation sémantique neutre (RSN-jeu)**, et comment la **pensée**
> raisonne ensuite sur cette RSN sans relire la surface. Le bloc est **hybride** : la surface et la RSN sont des
> opérations classiques, la pensée peut appeler un solveur exact ou un modèle selon le jeu. Les **chiffres** et les
> contrôles sont dans [`rapport-jeux-symboliques.md`](../reports/rapport-jeux-symboliques.md) ;
> la **théorie** dans [`synthese/07`](synthese/07-modeles-alternatifs-entree-sortie.md) et
> [`synthese/08`](synthese/08-les-operations.md).

## Le problème

Un même état de jeu a **beaucoup de surfaces** :

- aux échecs, la position de départ est une **FEN**, un **diagramme**, une suite de coups **SAN**
  (`1. e4 e5`), **UCI** (`e2e4`), française (`Cf3`, « le cavalier de g1 va en f3 ») ou anglaise
  (« knight from g1 to f3 ») ;
- aux dames, une prise est `11x18x27`, `b6xd4xf2` ou « le pion b6 prend en d4 puis f2 » ;
- au go, un point est `D4`, `B[dd]`, une ligne/colonne, ou « pierre noire en D4 » ;
- aux cartes, une carte est `A♥`, `AH`, « as de cœur » ou « ace of hearts » ;
- au morpion, une case est `B1`, `(1,2)`, « ligne 1 colonne 2 » ou « haut milieu ».

Si l'étage 2 lit la surface, il dépend de la langue et de la notation : deux écritures du même état peuvent
produire deux décisions différentes. La règle de l'architecture est donc **ordonnée** :

```
surface ──(couches linguistiques)──► RSN-jeu ──(pensée)──► décision
         étage 1                              étage 2
```

**L'étage 2 ne voit jamais la surface.** Il reçoit une RSN, la convertit en état interne, cherche, et rend
une RSN d'action. C'est ce contrat qui rend l'**invariance** mesurable : la même position écrite de cinq
façons doit donner la même empreinte, donc la même décision.

## Le contrat : la RSN-jeu

Une RSN-jeu est un triplet **jeu + nature + corps**, plus une **annotation** :

```json
{
  "jeu": "echecs",
  "nature": "coup",
  "corps": {"de": 52, "vers": 36, "promotion": null, "roque": null}
}
```

L'annotation porte la langue, le format, la confiance, les ambiguïtés, la surface d'origine et le niveau de
lecture. Elle est **hors de l'empreinte** : le bruit est transporté, pas confondu avec le sens.

Cinq propriétés, et chacune est mesurée :

1. **canonique** — deux surfaces qui disent la même chose donnent le même corps, donc la même empreinte ;
2. **séparable** — l'annotation ne change pas l'empreinte ;
3. **compacte** — un encodage binaire (`RSNB`) est disponible à côté du JSON canonique ;
4. **réversible** — tout corps encodé se décode à l'identique, et tout état se rend en surface ;
5. **typée** — le corps est un arbre de `null`, `bool`, `int`, `str`, listes et dictionnaires. **Aucun
   flottant** : le komi du go est en dixièmes (`65` pour 6,5), pour que l'empreinte ne dépende pas d'un
   arrondi de machine.

Les **natures** sont `etat`, `coup`, `partie`, `main` et `resultat`. Une **unité de sens** est une case, un
trait, une carte, un point, un pli — jamais un « jeton » : le jeton est l'unité technique du tokeniseur.

## Les cinq niveaux (0 → 4), quatre couches ajoutées

Les niveaux sont **cumulatifs** ; l'ablation de la fiche vérifie que la couverture ne baisse pas en montant.

| niveau | couche | ce qu'elle ajoute | exemple |
|---:|---|---|---|
| **0** | surface | la forme canonique exacte d'un jeu | `e2e4`, `XOX/.../...`, `9-13`, `D4`, `A♥` |
| **1** | normalisation | casse, accents, espaces, ponctuation | `E2-E4`, `e2 e4`, `b6-c5`, `d4` |
| **2** | lexique | synonymes et langues (FR/EN, puis **71 langues** pour les mots-clés) | `Cf3`, « cavalier de g1 vers f3 », « as de cœur », `конь g1 f3`, `馬 g1 f3` |
| **3** | grammaire | phrases, ordre libre, articles, verbes | « le cavalier g1 va en f3 », « je passe » |
| **4** | sémantique | légalité, désambiguïsation, canonicalisation | une FEN avec un `ep` inutile devient la même position ; `R` est le roi français **ou** la tour anglaise, tranché par la légalité |

La séparation est **volontaire** : le niveau 3 produit un **arbre** avec ce que la surface dit et des `None`
là où elle ne dit rien ; le niveau 4 tranche avec les règles. C'est ce qui permet de dire, dans la fiche, ce
que chaque couche apporte — au lieu de créditer le parseur entier.

## Les cinq jeux

| jeu | état (corps) | action (corps) | ce que la sémantique ajoute |
|---|---|---|---|
| **morpion** | 9 cases, trait | case (+ symbole) | le trait est **dérivé** des comptes ; une grille impossible est refusée |
| **échecs** | plateau FEN, trait, roques, ep, compteurs | de, vers, promotion, roque | droits impossibles retirés, `ep` sans prise supprimé, SAN désambiguïsé par la légalité |
| **dames** | 32 cases, trait, demi-coups | **chemin** (liste de cases) | la prise est obligatoire, une prise multiple est un chemin, la promotion arrête le pion |
| **go** | taille, plateau, trait, ko, passes, komi | point (+ taille) ou passe | suicide interdit, ko simple, score Tromp-Taylor |
| **cartes** | 4 mains, atout, pli, tour, plis | carte | il faut fournir la couleur demandée ; le pli se résout par l'atout |

Deux points de conception valent d'être nommés :

- **le morpion n'a pas de trait indépendant** : il se déduit des comptes. Une grille `XOX/.../...` implique
  que c'est à O de jouer ; un état « X au trait » avec ces comptes est **incohérent**, et la couche
  sémantique le refuse. C'est pour cela que le contrôle de perturbation y change une case, pas le trait.
- **le go indexe un point par sa taille de plateau** : `{"taille": 9, "point": 48}` et non `{"point": 48}`.
  Sans la taille, le même indice désigne deux intersections différentes ; l'action serait ambiguë.

## La pensée

L'étage 2 est **la logique du jeu**, pas un modèle de langue. Il reçoit la RSN et applique :

| jeu | logique | pourquoi |
|---|---|---|
| **morpion** | minimax **exact**, mémoïsé | le jeu est résolu : la valeur de la position vide est 0, et une partie parfaite est nulle |
| **échecs** | négamax alpha-bêta, approfondissement itératif, table de transposition, ordre des coups | la largeur interdit l'exhaustif ; le perft vérifie les règles **avant** la force |
| **dames** | négamax alpha-bêta, prises d'abord | les prises obligatoires réduisent la largeur ; le chemin est l'action |
| **go** | MCTS (UCT), playouts aléatoires | la recherche exhaustive est hors de portée ; le budget est explicite |
| **cartes** | politique (fournir, ne pas surjouer le partenaire, gagner au plus bas) | l'information est imparfaite : une recherche parfaite n'aurait pas de sens |

**La règle d'or** : la décision est **déterministe** à graine et budget fixés. Deux surfaces du même état
donnent la même RSN, donc la même décision — et c'est cette égalité qui est la mesure d'invariance de la
pensée.

## Ce que la mesure vérifie

La fiche [`rapport-jeux-symboliques.md`](../reports/rapport-jeux-symboliques.md) porte les chiffres. Les
contrôles, eux, sont stables :

- **couverture** par niveau : la couche 4 doit lire **tout** le corpus ;
- **invariance** : deux surfaces équivalentes doivent avoir la **même empreinte** ;
- **collisions négatives** : deux surfaces différentes ne doivent **pas** avoir la même empreinte ;
- **restitution** : rendre l'état puis le relire doit redonner la même empreinte ;
- **perturbation** : changer un champ sémantique doit changer l'empreinte après rendu/relu ;
- **permutation du lexique** : permuter les concepts doit faire **chuter** la couverture des phrases — sinon
  le lexique n'était pas utilisé ;
- **étiquettes mélangées** : mélanger les attendus doit faire tomber la couverture au hasard ;
- **règles** : perft des échecs (six positions), perft des dames (1→6), captures, suicide, ko, score ;
- **pensée** : le morpion exact ne perd pas contre le hasard, les mats en un sont trouvés, la recherche des
  dames gagne contre le joueur sans recherche, la politique des cartes bat le hasard, et les cinq jeux
  donnent la **même décision** sur des surfaces différentes.

## Les langues et les maîtres (B7/B8)

Le **lexique multilingue** (35 concepts, 71 langues, construit depuis Wikidata CC0) et le **corpus de 449
surfaces** sont mesurés : lecture au niveau 4, paires inter-langues invariantes, notation indépendante de la
langue, noms de jeux détectés. Les **maîtres** (17 principes, 9 sources du domaine public, 3 parties) changent
l'ouverture des échecs, tiennent le livre, gagnent au go 9×9 et ne perdent pas aux dames ; l'accord avec le coup
du maître ne bouge pas et la politique du whist **perd** contre la base.

Les chiffres, les listes de langues et les négatifs nommés sont dans
[`rapport-langues-maitres.md`](../reports/rapport-langues-maitres.md). Le concept reste : la **langue est un
bloc** (surface → RSN), les **maîtres sont une entrée** de la pensée, pas sa force.

## Ce qui reste ouvert

- **la détection automatique du jeu** n'est fiable que sur les surfaces **distinctives** (une FEN, un SGF,
  une grille 3×3, un compact 32 caractères). Une case seule (`D4`, `A1`) est ambiguë : la détection choisit le plus probable, et
  peut se tromper ; pour une garantie, il faut le jeu explicite, ou un contexte. La fiche donne le taux et
  nomme les cas ambigus.
- **les langues** : le lexique multilingue est fait de **lemmes** Wikidata, pas de formes fléchies ; les
  71 langues couvrent les **mots-clés**, pas la grammaire. Cinq langues n'ont aucun item naturel ; la notation
  les couvre. `e4`/`E4` restent ambiguës entre échecs et go.
- **les maîtres** : trois parties, une profondeur 3, un jeu de cartes simplifié. Les principes changent
  l'ouverture et le livre, mais l'accord avec le coup du maître ne bouge pas (+1/101) et la politique du whist
  **perd** contre la base (44,7 % contre 51,0 %). Ce sont des **négatifs nommés**, pas des preuves de force.
- **le go** implémente le **ko simple**, pas le ko positionnel complet ; le score est Tromp-Taylor, sans
  retirer les pierres mortes. C'est le score des playouts, pas un arbitre de fin de partie réelle.
- **les cartes** sont un whist à information imparfaite : la politique est lisible, mais elle n'est pas
  optimale ; la RSN porte les quatre mains pour la mesure et la simulation, pas pour tricher.
- **la force** n'est pas le sujet de ce chantier : le perft prouve les règles, pas la qualité de jeu. Le
  MCTS du go est mesuré à petit budget et **ne prétend pas** être fort ; c'est écrit dans la fiche.
- **le portage moteur** : cette implémentation est en Python, dans `tools/jeux/` ; le moteur Rust n'est pas
  modifié. Le contrat RSN est assez petit pour être porté, mais ce n'est pas fait.

## Où vit le code

| module | rôle |
|---|---|
| [`tools/jeux/rsn.py`](../tools/jeux/rsn.py) | le contrat : canonique, empreinte, binaire, différences |
| [`tools/jeux/lexique.py`](../tools/jeux/lexique.py) | les tables FR/EN et la normalisation |
| [`tools/jeux/lexique_multilingue.py`](../tools/jeux/lexique_multilingue.py) | le lexique 71 langues (Wikidata) et sa recherche |
| [`tools/jeux/corpus_multilingue.py`](../tools/jeux/corpus_multilingue.py) | le corpus multilingue dérivé du lexique |
| [`tools/jeux/grammaire.py`](../tools/jeux/grammaire.py) | les unités, les phrases, les motifs |
| [`tools/jeux/codecs/`](../tools/jeux/codecs/) | un codec par jeu (surface → RSN, RSN → surface) |
| [`tools/jeux/regles/`](../tools/jeux/regles/) | les règles internes et le perft |
| [`tools/jeux/pensee.py`](../tools/jeux/pensee.py) | minimax, alpha-bêta, MCTS, politique |
| [`tools/jeux/corpus.py`](../tools/jeux/corpus.py) | le corpus construit par le code, avec ses attendus |
| [`tools/jeux/maitres.py`](../tools/jeux/maitres.py) | les principes, évaluations, livre, parties, politiques, priors |
| [`tools/jeux/mesure.py`](../tools/jeux/mesure.py) | les séries et les contrôles |
| [`tools/jeux/mesure_langues.py`](../tools/jeux/mesure_langues.py) | la couverture et les contrôles des 71 langues |
| [`tools/jeux/mesure_maitres.py`](../tools/jeux/mesure_maitres.py) | les mesures des principes et leurs contrôles |
| [`tools/porte-jeux.sh`](../tools/porte-jeux.sh) | la porte de non-régression |

**Vocabulaire** : une RSN-jeu est faite d'**unités de sens** ; le **jeton** reste l'unité technique du
tokeniseur. Voir le [glossaire](glossaire/01-le-projet-ses-noms-sa-methode.md).

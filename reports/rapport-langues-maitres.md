# B7/B8 — 71 langues pour les jeux, et les livres des maîtres mesurés

> Mesure du **26/10/2026**, sur `Hauru` (Python 3.13, sans GPU), `tools/jeux/` et
> `tools/porte-jeux.sh`. Deux extensions de B5/B6 : un **lexique multilingue** de 35 concepts dans
> **71 langues** (Wikidata, CC0) et une **base de 17 principes** tirés de neuf sources (sept ouvrages du
> domaine public, les proverbes traditionnels du go, le morpion résolu), avec leurs évaluations, leur livre,
> leurs parties et leurs politiques. JSON bruts :
> [`jeux-langues-mesures.json`](jeux-langues-mesures.json) et
> [`jeux-maitres-mesures.json`](jeux-maitres-mesures.json). Concept :
> [`docs/theorie/jeux-symboliques.md`](../docs/theorie/jeux-symboliques.md). Durées : **3,1 s** (langues), **468,8 s**
> (maîtres), **188,7 s** (jeux, régénéré avec le lexique Unicode).

## Ce qui est mesuré

1. **Les langues** — le même sens (pièce + cases, rang + enseigne, nom du jeu + coordonnée) dans 71 langues ;
   couverture du corpus au niveau 4, invariance inter-langues, contrôle par permutation des libellés,
   notation indépendante de la langue, détection des noms de jeux.
2. **Les maîtres** — 17 principes encodés dans la pensée, et ce qu'ils déplacent : premier coup des échecs,
   livre d'ouvertures, mats en un, accord avec le coup du maître sur trois parties, dames, go, cartes.

Le corpus multilingue est **dérivé du lexique** : pour chaque langue, on prend les libellés disponibles et on
construit les surfaces. Ce n'est pas de la grammaire : c'est la **couche lexicale**, celle qui doit porter le
sens avant qu'une phrase soit possible. Les libellés Wikidata sont des **lemmes** ; les formes fléchies ne sont
pas couvertes (voir « Ce qui pourrait rendre ce résultat faux »).

## 1. Les langues : la couverture

| mesure | valeur |
|---|---:|
| langues | **71** |
| concepts | **35** |
| couples concept-langue | **1 433** |
| moyenne de concepts par langue | **20,13** |
| langues « fortes » (pièces N/P + un rang + une enseigne) | **32** |
| langues avec au moins un item du corpus | **66** |
| langues avec au moins un item fort (échecs ou cartes) | **62** |

Les concepts couvrent les noms des cinq jeux (et du whist), les six pièces des échecs, le roque, le mat, la
promotion, la nulle, les quatre rangs A/K/Q/J, les quatre enseignes, l'atout, le pli, le ko, le proverbe du go,
les couleurs blanc/noir et cinq notions de maîtres (colonne ouverte, poste, tempo, structure de pions).

| concept | langues | concept | langues |
|---|---:|---|---:|
| pièce K | 62 | rang A | 36 |
| pièce Q | 63 | rang K | 33 |
| pièce R | 61 | rang Q | 32 |
| pièce B | 60 | rang J | 32 |
| pièce N | 61 | enseigne C | 35 |
| pièce P | 61 | enseigne D | 34 |
| nom « échecs » | 69 | enseigne H | 36 |
| nom « go » | 62 | enseigne S | 35 |
| nom « dames » | 60 | nom « cartes » | 59 |
| nom « morpion » | 42 | nom « whist » | 27 |

## 2. Le corpus multilingue : 449 surfaces

| mesure | valeur |
|---|---:|
| items | **449** |
| bons au niveau 4 | **449 / 449** (**100 %**) |
| paires inter-langues | **11** |
| paires invariantes | **11 / 11** (**100 %**) |
| langues sans item | **5** (`ky`, `lo`, `mt`, `si`, `yo`) |

Les 11 paires sont : Nf3, e4, A♥, K♠, Q♦, J♣, 10♥, go D4, go passe, dames b6-c5, morpion A1. Chaque paire
contient une variante par langue disponible : la même empreinte RSN, donc le même sens.

**Détection des noms de jeux** : **315/315** libellés de jeu reconnus (morpion 42, échecs 69, dames 56, go 62,
cartes 86 — le whist compte avec les cartes). **Détection exacte sur le corpus de 112 items** : **110/112**
(**98,2 %**) ; les deux échecs sont `e4` et `E4`, des cases **réellement ambiguës** entre échecs et go, nommées
et non maquillées. **Langue détectée** : **343/449** (**76,4 %**) ; les confusions viennent des libellés
partagés (roumain/ukrainien `король`, plusieurs langues `шах`).

## 3. Les contrôles des langues

| contrôle | résultat |
|---|---:|
| permutation des libellés entre concepts, items forts | **12 / 275** restants (**4,4 %**) |
| permutation, tous les items | **186 / 449** (les items « nom du jeu + coordonnée » survivent : la coordonnée est neutre) |
| notation : 72 items × 71 langues | **5 112 / 5 112** (**100 %**) |
| notation, mode rapide : 12 langues | **864 / 864** |

La permutation garde les **mêmes formes** et les associe au **mauvais concept** : la couverture des items forts
s'effondre de 275/275 à 12/275. Les 12 survivants sont des hasards de rotation (un libellé de pièce qui retombe
sur une pièce au coup légal, une carte dont le rang et l'enseigne restent cohérents) ; c'est le bruit attendu
d'un contrôle, pas une lecture du sens.

La notation est le **recours indépendant de la langue** : FEN, SAN, UCI, GTP, SGF, grille, donne compacte,
binaire. Les 72 items de notation du corpus sont lus avec chacune des 71 langues comme annotation : 5 112
lectures, 5 112 bons. La langue ne change pas la notation ; elle ne change que l'étiquette.

## 4. Les maîtres : la base

| mesure | valeur |
|---|---:|
| principes | **17** |
| sources | **9** |
| parties du domaine public | **3** (Opéra 1858, Immortelle 1851, Toujours verte 1852) |
| positions de livre | **28** |
| lignes d'ouverture | **5** (Ruy Lopez, Italienne, Gambit dame, Sicilienne, Indienne du roi) |

Les sources : Lasker, *Lasker's Manual of Chess* (1925) ; Capablanca, *Chess Fundamentals* (1921) ;
Nimzowitsch, *My System* (1925) ; Tarrasch, *The Game of Chess* (1931) ; Payne, *The Game of Draughts* (1756) ;
Smith, *The Game of Go* (1908) ; Cavendish, *The Laws and Principles of Whist* (1884) ; les proverbes
traditionnels du go ; le morpion résolu. Les trois parties sont des **faits** (les coups), citées par leurs
joueurs, leur lieu et leur année ; elles sont validées par le moteur jusqu'au mat.

## 5. Les maîtres : ce que les principes déplacent

### Échecs

| mesure | sans les principes | avec les principes |
|---|---:|---:|
| premier coup depuis la position initiale | **Nc3** (`b1c3`) | **d4** (`d2d4`) |
| premier coup parmi e4/d4/Nf3/c4 | non | **oui** |
| livre : plies suivis | — | **10 / 10** |
| mats en un | **3 / 3** | **3 / 3** |
| accord avec le coup du maître (101 positions) | **41 / 101** (40,6 %) | **42 / 101** (41,6 %) |

L'évaluation augmentée (centre, développement, roi roqué, colonnes ouvertes, postes avancés) change le premier
coup et **ne coûte pas** les mats. Le livre tient 10 plies. Mais l'accord avec le coup du maître ne bouge pas :
**+1 position sur 101** — c'est un **négatif** : la connaissance des principes ne remplace pas la profondeur de
recherche. Le moteur reste un moteur de profondeur 3.

### Dames

| mesure | valeur |
|---|---:|
| parties, même profondeur 4 | **20** |
| victoires des maîtres | **10** |
| nulles | **10** |
| défaites | **0** |
| victoires des Blancs avec la base seule | **0 / 20** |

Les maîtres ne perdent jamais ; les 10 victoires sont avec les Noirs, les 10 nulles avec les Blancs. La base
seule ne gagne **aucune** des 20 parties avec les Blancs (**0/20**). Le **biais de couleur** de ce jeu est nommé :
il ne permet pas de dire « les maîtres sont meilleurs » sans réserve ; il permet de dire qu'ils **ne perdent pas**
et qu'ils **améliorent le côté défavorisé**.

### Go

| mesure | sans prior | avec prior |
|---|---:|---:|
| 9×9 : coups de 3e/4e ligne (10 graines) | **3 / 10** | **10 / 10** |
| 5×5 : premier coup au bord (10 graines) | **10 / 10** | **10 / 10** |
| capture évidente sur 5×5 (10 graines) | **10 / 10** | **10 / 10** |

Le prior des proverbes (« les coins avant les côtés, les côtés avant le centre ») est **net sur 9×9** :
10/10 contre 3/10. Sur 5×5, le plateau est trop petit : le bord est déjà le choix de la base, et la capture
évidente est trouvée par les deux. Ce sont des **effets nuls nommés**, pas des preuves de force.

### Cartes

| mesure | maîtres | base | hasard |
|---|---:|---:|---:|
| donnes (1 000) | **447 / 1 000** (44,7 %) | **510 / 1 000** (51,0 %) | — |
| contre le hasard | **785 / 1 000** (78,5 %) | **824 / 1 000** (82,4 %) | 486 / 1 000 (48,6 %) |
| ablation : sans couvrir l'honneur | **435** | — | — |
| ablation : sans seconde main basse | **457** | — | — |
| ablation : sans troisième main haute | **465** | — | — |

La politique du whist classique, encodée naïvement, est **moins bonne** que la politique du dépôt : 44,7 %
contre 51,0 %. L'ablation montre que la **seconde main basse** est la règle qui coûte le plus (447 → 457 quand
on la retire), mais aucune variante ne rattrape la base (457 < 510). C'est un **négatif nommé** : le jeu de
cartes du dépôt est simplifié (pas d'enchères, pas de signalisation), et la base y est déjà un optimum local.

## 6. Les contrôles des maîtres

- **Échecs** : la même recherche sans les principes (41/101), le livre sans le livre (le premier coup est Nc3),
  et les mats en un comme non-régression (3/3).
- **Dames** : la base contre elle-même (0 victoire blanche sur 20) et les maîtres contre la base (0 défaite).
- **Go** : le même MCTS sans prior (3/10 sur 9×9, 10/10 sur 5×5, capture 10/10) ; le prior ne fait que
  déplacer les choix là où le plateau est assez grand.
- **Cartes** : la base contre elle-même (51,0 %), les maîtres contre le hasard (78,5 %), la base contre le
  hasard (82,4 %) et l'ablation des trois règles.
- **Langues** : la permutation des libellés (12/275), la notation dans les 71 langues (5 112/5 112) et la
  détection des noms de jeux (315/315).

## 7. Ce qui pourrait rendre ce résultat faux

- **Les libellés Wikidata sont des lemmes.** « ملك » (roi) et « قلوب » (cœurs) ne se rencontrent pas sous la
  forme du pluriel ; les formes fléchies, les articles et les synonymes ne sont pas couverts. Le corpus
  multilingue utilise les libellés tels quels : il mesure la couche lexicale, pas une compréhension générale.
- **Les 5 langues sans item** (`ky`, `lo`, `mt`, `si`, `yo`) n'ont pas de libellé pour les concepts testés ;
  ce n'est pas une faute de lecture, c'est un trou de la source.
- **La détection exacte est à 110/112**, pas 112 : `e4` et `E4` sont des cases d'échecs **et** des points de go.
  Aucune surface seule ne permet de trancher ; il faut le contexte du jeu.
- **Trois parties de maîtres** ne font pas un corpus ; l'accord de 42/101 vaut pour ces trois parties, à
  profondeur 3, pas pour « les maîtres » en général.
- **Le jeu de cartes est simplifié** : sans enchères ni signalisation, les règles du whist ne sont pas dans
  leur domaine de validité. Le négatif des cartes est donc un négatif **de ce jeu**, pas des livres.
- **Le biais de couleur aux dames** : la base ne gagne aucune des 20 parties avec les Blancs (0/20) ; le résultat
  des maîtres (0 défaite) est solide, mais l'effet propre des principes est confondu avec l'avantage des Noirs.
- **La vitesse a baissé** : 1 297 parses/s au niveau 4 contre 3 083 avant le multilingue (tokenisation Unicode
  et détection de langue). La couche reste sous la milliseconde par surface ; c'est le prix des 71 langues,
  pas une régression cachée.

## 8. Ce que ça n'autorise pas à dire

- que le modèle **comprend** les 71 langues : il lit des **libellés** et des **notations**, pas des phrases
  fléchies ;
- que les principes des maîtres **rendent le moteur fort** : ils changent l'ouverture, tiennent le livre,
  gagnent au go 9×9, mais ne rapprochent pas du coup du maître aux échecs et **perdent** aux cartes ;
- que la détection est résolue : deux surfaces restent ambiguës sans contexte ;
- que les 5 langues sans item sont « non couvertes » par la notation : elles le sont par la notation, pas par
  le lexique naturel.

## 9. Les fichiers

- lexique : [`tools/jeux/lexique_multilingue.json`](../tools/jeux/lexique_multilingue.json), construit par
  [`construire_lexique_multilingue.py`](../tools/jeux/construire_lexique_multilingue.py), chargé par
  [`lexique_multilingue.py`](../tools/jeux/lexique_multilingue.py) ;
- corpus : [`corpus_multilingue.py`](../tools/jeux/corpus_multilingue.py) ;
- mesures : [`mesure_langues.py`](../tools/jeux/mesure_langues.py),
  [`mesure_maitres.py`](../tools/jeux/mesure_maitres.py) ; pilotes :
  [`tools/mesure_langues.py`](../tools/mesure_langues.py),
  [`tools/mesure_maitres.py`](../tools/mesure_maitres.py) ;
- maîtres : [`tools/jeux/maitres.py`](../tools/jeux/maitres.py) ;
- tests : [`tools/jeux/tests/`](../tools/jeux/tests/) (**65 tests**, dont 11 nouveaux) ;
- porte : [`tools/porte-jeux.sh`](../tools/porte-jeux.sh) (étendue aux langues et aux maîtres) ;
- JSON : [`jeux-langues-mesures.json`](jeux-langues-mesures.json),
  [`jeux-maitres-mesures.json`](jeux-maitres-mesures.json), [`jeux-mesures.json`](jeux-mesures.json).

## 10. La ligne de roadmap

**B7** (les langues) et **B8** (les maîtres), mesurées ; voir [`docs/pilotage/roadmap.md`](../docs/pilotage/roadmap.md).

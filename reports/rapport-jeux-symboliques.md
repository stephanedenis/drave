# B5/B6 — les jeux symboliques : 112 surfaces, 100 % au niveau 4, 33/33 paires invariantes

> Mesure du **25/10/2026**, sur `Hauru` (Python 3.13, sans GPU), `tools/jeux/` et
> `tools/porte-jeux.sh`. Corpus **construit par le code** (`tools/jeux/corpus.py`), cinq jeux, deux langues,
> plusieurs notations ; dix contrôles. JSON brut : [`jeux-mesures.json`](jeux-mesures.json). Concept :
> [`docs/jeux-symboliques.md`](../docs/jeux-symboliques.md). Durée de la mesure complète : **180 s**.

## Ce qui est mesuré

Deux étages, dans l'ordre du contrat :

1. **les couches linguistiques** — une surface (notation, phrase, diagramme) devient une **RSN-jeu**
   canonique ; on mesure la couverture par niveau (0→4), l'invariance entre surfaces équivalentes, la
   non-collision des surfaces différentes, la restitution, le compactage et la vitesse ;
2. **la pensée** — les règles et la recherche de chaque jeu (perft, mats, capture, ko), la force (morpion
   exact, alpha-bêta des dames, MCTS du go, politique des cartes) et l'**invariance de la décision** :
   la même position écrite de plusieurs façons doit donner le même coup.

**Le corpus** : 112 items — morpion 32, échecs 34, dames 16, go 14, cartes 16. Les attendus sont calculés
par les **règles**, jamais recopiés à la main : si le codec et les règles se contredisent, le corpus le dit.

## 1. La couverture par couche

| niveau | ce qu'il ajoute | bons / 112 | taux |
|---:|---|---:|---:|
| 0 | surface (forme canonique exacte) | 50 | 44,6 % |
| 1 | normalisation (casse, accents, espaces, ponctuation) | 77 | 68,8 % |
| 2 | lexique (synonymes, FR/EN) | 105 | 93,8 % |
| 3 | grammaire (phrases, ordre libre) | 110 | 98,2 % |
| **4** | **sémantique (légalité, désambiguïsation, canonicalisation)** | **112** | **100 %** |

Par jeu, aux deux extrêmes :

| jeu | n0 | n4 |
|---|---:|---:|
| morpion | 18 / 32 | **32 / 32** |
| échecs | 13 / 34 | **34 / 34** |
| dames | 7 / 16 | **16 / 16** |
| go | 8 / 14 | **14 / 14** |
| cartes | 4 / 16 | **16 / 16** |

**Ce que ça dit** : chaque couche ajoute, et le niveau 4 est nécessaire pour les deux FEN sémantiquement
égales (l'en passant inutile et les droits de roque impossibles) — les seules qui échouent encore au
niveau 3 (110/112). Leur attendu est construit **sans** le canonicaliseur du codec (la FEN sans en passant,
la FEN sans droits) : le test ne compare pas le codec à lui-même.

## 2. L'invariance entre surfaces

33 paires d'expressions **équivalentes** (même RSN attendue) : une FEN et son diagramme, `e2e4` et
« le pion de e2 vers e4 », `9x18` et `b6xd4`, `D4` et `B[dd]`, `A♥` et « as de cœur », etc.

| niveau | paires invariantes | taux |
|---:|---:|---:|
| 0 | 9 / 33 | 27,3 % |
| 1 | 19 / 33 | 57,6 % |
| 2 | 29 / 33 | 87,9 % |
| 3 | 31 / 33 | 93,9 % |
| **4** | **33 / 33** | **100 %** |

**Ce que ça dit** : sans les couches, deux écritures du même état ne sont **pas** le même sens ; au
niveau 4, elles le sont. C'est la mesure qui autorise à dire que l'étage 2 ne dépend pas de la surface.

## 3. Les contrôles négatifs

| contrôle | mesure | verdict |
|---|---|---|
| **collisions** : 8 groupes de surfaces **différentes** | 0 collision | les surfaces différentes ne se confondent pas |
| **permutation du lexique** : concepts permutés (cases, pièces, rangs, couleurs…) | 112 → **92** items corrects (**20 perdus**) | le lexique est **porteur** ; les formes canoniques, non lexicales, résistent — c'est attendu |
| **étiquettes mélangées** : attendus permutés | **7 / 112** (6,25 %) | le comparateur ne valide pas au hasard |
| **restitution** : rendre l'état puis le relire | **112 / 112** | le sens survit au miroir sortie → entrée |
| **perturbation** : changer un champ sémantique puis rendre/relire | **112 / 112** détectées | le rendu ne mange pas un changement de sens |

Les 20 items perdus par la permutation sont ceux qui passent par le lexique : les phrases, les noms de
cases, et les grilles dont les symboles sont des mots ou des tokens séparés. Les formes canoniques compactes
(FEN, `e2e4`, `9x18`, `D4`, `A♥`) résistent — c'est attendu. Une permutation qui ne ferait rien serait le
signe d'un lexique décoratif.

## 4. Compactage et vitesse

| mesure | valeur |
|---|---:|
| objets sémantiques distincts | 41 |
| JSON canonique moyen | 128,93 octets |
| binaire `RSNB` moyen | 71,10 octets |
| **ratio binaire / JSON** | **0,5515** (45 % de moins) |
| vitesse de lecture, niveau 4 | **3 083 parses/s** (0,0363 s pour 112) |
| vitesse de lecture, niveau 0 | **4 470 parses/s** (0,0251 s pour 112) |

Le binaire ne remplace pas le JSON : il mesure le **coût du contrat**. Il est plus petit et il se décode à
l'identique (test de round-trip) ; il ne porte pas les annotations par défaut.

## 5. La pensée : les règles d'abord

### Morpion — le jeu résolu

| mesure | valeur |
|---|---:|
| valeur minimax de la position vide | **0** (nulle) |
| partie parfaite contre parfaite | **N** (nulle) |
| exact contre hasard | **200 / 200** sans défaite |
| gourmand (sans recherche) contre exact | **0 / 200** défaite |

Le gourmand ne perd pas : son heuristique est déjà bonne au morpion. La contribution du minimax exact
n'est pas le gain contre un gourmand, c'est la **valeur** (0) et la **preuve** que la partie parfaite est
nulle. C'est écrit ici pour ne pas surinterpréter le 0/200.

### Échecs — le perft avant la force

Six positions de référence, profondeur 4 ; les nombres de feuilles sont **connus** et indépendants de ce
code.

| position | profondeur 4 | temps |
|---|---:|---:|
| départ | 197 281 | 1,26 s |
| Kiwipete | 4 085 603 | 25,88 s |
| p3 | 43 238 | 0,31 s |
| p4 | 422 333 | 2,84 s |
| p5 | 2 103 487 | 13,16 s |
| p6 | 3 894 594 | 22,05 s |

**Les six sont exacts.** C'est le contrôle de règles le plus fort du lot : roque, en passant, promotion,
échec et clouage sont dans le compte. La recherche alpha-bêta trouve les **3 mats en un** de la suite
(20, 26 et 42 nœuds) ; le joueur statique n'en trouve qu'**1** — la recherche ajoute 2 mats sur 3. Une
auto-partie de 30 plis (7 456 nœuds) reste légale et termine sur une FEN valide.

### Dames — le perft et la recherche

| mesure | valeur |
|---|---|
| perft 1→6 depuis le départ | **7 · 49 · 302 · 1 469 · 7 361 · 36 768** (exacts) |
| prise simple, prise multiple, promotion | les trois générées et appliquées |
| recherche (profondeur 4) contre sans-recherche | **20 / 20** parties gagnées (adjudication au matériel) |

### Go — les règles, puis un MCTS honnête

| mesure | valeur |
|---|---|
| plateau vide 5×5 | **25** coups légaux |
| capture d'une pierre | ✅ |
| suicide | refusé ✅ |
| ko simple | le recapturé immédiat est refusé ✅ |
| score Tromp-Taylor connu (croix 3×3) | **90 / 0** en dixièmes, soit 9 points à 0 ✅ |
| MCTS, 60 playouts, 3 parties contre le hasard | **1 / 3** |

Le MCTS est **légal** et déterministe à graine fixée, mais à 60 playouts il ne bat pas le hasard de façon
crédible. C'est un **négatif nommé** : le budget est le facteur limitant, pas la règle. Un essai isolé à
200 playouts a gagné de 80 points, mais un essai n'est pas une mesure ; il n'entre pas dans le tableau.

### Cartes — la politique du whist

| mesure | 1 000 donnes |
|---|---:|
| politique contre hasard | **79,7 %** |
| hasard contre hasard | 48,6 % |
| politique sans partenaire | 75,6 % |
| politique sans atout | 73,5 % |
| coups illégaux de la politique | **0 / 52 000** |

**Ce que ça dit** : la politique bat nettement le hasard, et les coups sont légaux. Les deux ablations
(partenaire, atout) coûtent **4 à 6 points** : la politique doit l'essentiel à la **fourniture de couleur**
et au choix de la carte, pas à une lecture fine du partenaire. C'est une politique lisible, pas un solveur.

## 6. L'invariance de la pensée

Pour chaque jeu, deux surfaces du **même état** sont lues puis données à `decide` avec le même budget :

| jeu | surfaces | décision identique |
|---|---|---:|
| morpion | deux grilles vides | ✅ |
| échecs | FEN et diagramme du départ | ✅ |
| dames | compact et diagramme du départ | ✅ |
| go | deux diagrammes vides (5×5) | ✅ |
| cartes | donne et donne avec les cartes en toutes lettres | ✅ |

**5 / 5.** Le contrôle négatif change le **trait** (ou le joueur au trait) : les cinq empreintes d'état
diffèrent, **5 / 5**. Une invariance qui ne serait qu'un cache de surface ne passerait pas ce contrôle.

## 7. La détection automatique du jeu

**100 / 112** surfaces sont attribuées au bon jeu sans indication (89,3 %). Les 12 échecs sont des
surfaces **ambiguës par nature** : `A1`, `B1`, `E4`, `d4`, `b6-c5`, `c3-d4` sont des cases valides dans
plusieurs jeux, et « le pion b6 prend en d4 » ne dit pas s'il s'agit de dames ou d'échecs. Sans indice de
jeu, la détection choisit le plus probable — et sur ces 12 surfaces, ce choix est faux. Pour une garantie,
il faut passer le jeu explicitement, ou un contexte.

## Ce qui pourrait rendre ce résultat faux

- **La circularité du corpus.** Le corpus est construit par le même code que celui qu'il teste. Ce qui
  protège : le perft est **externe** (nombres connus), les règles sont indépendantes des codecs, la
  restitution est un aller-retour (et non une table), la permutation du lexique et le mélange des étiquettes
  cassent la correspondance. Un corpus **externe** resterait nécessaire pour une prétention de couverture
  générale.
- **La taille et le choix du corpus.** 112 items, deux langues, cinq jeux. Le corpus est **construit pour
  couvrir les couches**, pas échantillonné au hasard : une autre collection de phrases pourrait baisser la
  couverture. Le 100 % est un 100 % **sur ce corpus**, pas sur « tous les jeux ».
- **Le français et l'anglais seulement.** L'allemand, l'espagnol, le japonais ne sont pas testés ; le
  lexique est une table extensible, pas une preuve de couverture.
- **Le perft prouve les règles, pas la force.** Les 3 mats en un sont une suite courte ; les 20/20 des
  dames sont contre un joueur **sans recherche** ; le MCTS du go est faible à 60 playouts.
- **La RSN-jeu n'est pas la RSN finale.** C'est un contrat **par jeu**, avec des champs spécifiques
  (roques, chemin, ko, pli). Il ne prétend pas être la représentation multi-niveaux générale de la
  synthèse 07 ; il en est l'application à un domaine fermé.
- **Le binaire est mesuré sur les 41 objets attendus**, pas sur tous les états possibles ; il n'inclut pas
  les annotations par défaut.
- **Le trait du morpion est dérivé** : une grille `XOX/.../...` implique O au trait. Le contrôle de
  perturbation y change donc une case (un successeur valide), pas un trait impossible — c'est une
  propriété du jeu, pas une faiblesse du contrôle.

## Ce que ça n'autorise pas à dire

- que les couches **comprennent** toutes les langues et tous les jeux : elles couvrent ce corpus ;
- que la pensée est **forte** : elle est **correcte** (perft, règles), **invariante** (5/5) et **mesurée**
  (morpion exact, mats, dames, cartes) ; la force du go n'est pas établie ;
- que l'étage 2 de la synthèse 07 est terminé : le corpus est symbolique et fermé, la langue naturelle
  générale reste l'étage 1 du projet.

## La ligne de roadmap

**B5.1** contrat RSN-jeu — ✅ · **B5.2** cinq niveaux (0→4) et cinq codecs — ✅ · **B5.3** restitution et bruit
— ✅ · **B5.4** contrôles négatifs — ✅ · **B6.1** règles et perft — ✅ · **B6.2** recherche — ✅ ·
**B6.3** politique des cartes — ✅ · **B6.4** invariance de la pensée — ✅.

**Prochaine action** : aucune sur B5/B6. Les suites sont **hors du plan** : un corpus externe, la
détection avec contexte, le ko positionnel complet, un MCTS assez budgété pour être jugé, et le portage du
contrat dans le moteur Rust.

## Les fichiers

- code : [`tools/jeux/`](../tools/jeux/) (`rsn.py`, `lexique.py`, `grammaire.py`, `codecs/`, `regles/`,
  `pensee.py`, `corpus.py`, `mesure.py`) ;
- tests : [`tools/jeux/tests/`](../tools/jeux/tests/) (54 tests) ;
- porte : [`tools/porte-jeux.sh`](../tools/porte-jeux.sh) ;
- JSON : [`jeux-mesures.json`](jeux-mesures.json).

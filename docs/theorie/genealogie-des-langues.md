# La généalogie des langues, des dialectes et des styles

> **Ce que cette page est.** La **théorie** de la structure généalogique qui doit organiser l'**étage
> entrée-sortie** (nom historique : « couche commune ») de Drave, et ce que les projets complémentaires
> **Panini** et **Nipada** ont établi sur elle. Les **mesures** sont dans
> [`reports/07-mesures-couche-commune.md`](../../reports/07-mesures-couche-commune.md), dans
> [`reports/rapport-corpus-commun.md`](../../reports/rapport-corpus-commun.md),
> [`reports/rapport-retrieval-epoque.md`](../../reports/rapport-retrieval-epoque.md) et, pour la
> confrontation des deux faces, dans
> [`reports/rapport-genealogie-deux-faces.md`](../../reports/rapport-genealogie-deux-faces.md).
> *À relire et à mettre à jour à chaque cycle : Panini et Nipada sont des sources vivantes.*

## 1. Pourquoi une généalogie

Une couche entrée-sortie ne peut pas être « riche en langues » au sens d'une **liste**. Les langues forment
une **structure** : des familles, des branches, des dialectes, des styles, et des **traductions** qui
traversent tout cela. Si la structure est réelle, elle doit se voir dans les états du modèle — et si elle
ne s'y voit pas, c'est le modèle qui est incomplet.

La hiérarchie à couvrir, du plus large au plus fin :

| niveau | exemple | ce qui varie |
|---|---|---|
| **famille** | indo-européen, nigéro-congolais, austronésien | le système, la morphologie |
| **branche** | roman, slave, germanique | le lexique, la syntaxe |
| **langue** | français, russe, chinois | l'orthographe, la grammaire |
| **dialecte** | occitan languedocien, romanche surmiran | la phonologie, le lexique local |
| **style / époque** | baroque, classique, technique, traduit | le registre, la syntaxe, le vocabulaire |
| **traducteur** | Butler, Pope, Walter | le rythme, le vers ou la prose, les choix |

## 2. Ce que Panini et Nipada ont établi — et leur avertissement

Les deux projets attaquent le même objectif par l'**autre bout** : **Panini** décompose le texte en
**14 atomes sémantiques** (∃ ∆ ∼ ↗ ⊙ ⧖ ◇ № ⊕ ⊗ λ ⊞ ≍ ≡) et **9 dhātus**, et **Nipada** fait tourner ce
graphe comme un tissu computationnel (SAT-solver trinaire, programmes de dhātus) — *une approche
**algébrique** là où Drave est **statistique***. Ils se rejoignent sur un point : il faut une **structure**
entre les langues, pas une liste.

**Leur résultat le plus utile pour nous est un avertissement** ✗✓. En cherchant si leur signature
lexicale (14 atomes de fréquence) reproduit la **généalogie** d'un corpus de textes philosophiques (grec,
latin, arabe, sanskrit, chinois, français, allemand), ils ont trouvé (rapport §150) :

| variable | coefficient | lecture |
|---|---:|---|
| **époque** (années) | **+0,138** | **dominant** |
| **généalogie** (distance dans l'arbre) | **+0,049** | faible |
| tradition (même école) | +0,002 | nul |

*Leur conclusion : **la signature de surface capte l'époque, pas la filiation*** ✗✓ — « l'héritage transmet
les **concepts**, pas les **signifiants** ». Et leur remède proposé : des **embeddings denses multilingues**
projetés sur les atomes, pour supprimer le confondant langue/époque.

**Ce que J3.2 ajoute à la lecture de cet avertissement.** Leur « filiation » (`d_graph`) est une distance
de **tradition** — la position d'une œuvre dans un graphe d'héritage —, **pas** une distance de **famille
de langues**. Leur corpus est massivement anglais : presque aucune paire ne met deux langues différentes
en regard. L'avertissement est donc un constat sur la **signature de texte** et sur la **tradition**, pas
une mesure de la généalogie des langues. Il faut le lire comme une **borne de validité de l'atome**, pas
comme une théorie de l'arbre. Les chiffres et les contrôles sont dans la fiche J3.2.

**Ce que J12.1 ajoute : l'avertissement est indexé à son corpus.** Sur la deuxième vague — le corpus
§334 et les signatures de 44 œuvres —, la loi que Panini ajuste est une loi de **filiation/topologie**,
pas d'époque : quand la date et la topologie sont mises côte à côte, la topologie porte la variance et la
date n'ajoute presque rien. Mais le corpus est **colinéaire** : les couples de même tradition sont
presque tous contemporains, et les couples longs sont presque tous inter-traditions. Il ne permet donc
pas d'identifier un effet d'époque indépendant. Les 44 signatures ne reproduisent pas le β époque de la
validation v150 et, à surface contrôlée, le signal de tradition s'affaiblit fortement : la signature V14
est une signature de **texte, de source et de traduction** avant d'être une signature de tradition. La
conséquence théorique n'est pas « Panini a tort » : c'est que **l'avertissement vaut pour le corpus et
l'instrument qui l'ont produit**, et qu'il faut, pour le transporter, contrôler **la date, la tradition
et la source** — les trois à la fois. Les chiffres et les contrôles sont dans
[`reports/rapport-panini-334.md`](../../reports/rapport-panini-334.md).

## 3. Ce que cela impose à nos tests

1. **contrôler l'époque** ✗✓ : un « style » mesuré sur deux traductions d'âges différents peut être de
   l'**époque**, pas du traducteur. Tout test de style doit apparier les dates, ou les déclarer.
2. **tester par niveau** ✓✓ : famille, branche, langue, dialecte, style — chacun avec son propre jeu de
   paires et son propre hasard (une paire de langues sœurs n'est pas une paire de familles différentes).
3. **ne pas confondre lisibilité et structure** ✗✓ : que la langue soit **lisible** dans l'état ne dit
   **rien** de la **généalogie** — une signature de surface peut être dominée par l'époque.
4. **ne pas confondre les deux faces** ✗✓ : la **face atome** est une signature de **texte** (ce qu'un
   texte dit) ; la **face langue** est une **généalogie** (ce qui apparente deux langues). Une distance
   entre signatures d'atomes n'est pas une distance entre langues, et un arbre de langues ne valide pas
   une théorie sémantique. Les deux faces se confrontent **sur le même corpus**, avec des unités
   différentes — et seulement si les deux y sont présentes.
5. **contrôler l'écriture avant la famille** ✗✓ : sur le corpus commun, le retrieval de surface ne
   traverse **aucune** frontière d'écriture ; le signal de famille n'apparaît que dans les paires de même
   écriture, et il y est porté par quelques paires. Un test de famille qui ne stratifie pas par écriture
   mesure surtout l'**écriture**.

## 4. La preuve que la structure compte — et ce qu'elle ne prouve pas

La grille de 60 langues, regroupée par niveau Glottolog, donne un ordre **monotone** : **même branche** >
**même famille** > **familles différentes** (hasard très bas) — *l'alignement du modèle suit la
généalogie*. ⚠️ Le confondant de l'**écriture** reste ✗✓ : les paires « même branche » sont surtout CJK.

**Ce que J3.2 change dans cette lecture.** Cet ordre ne doit **pas** être lu comme un effet de famille
tant que l'écriture n'est pas contrôlée. Sur le corpus commun, **toutes** les paires d'écritures
différentes sont au hasard exact ; le signal de famille ne vit que dans les paires de **même écriture**,
et il y est porté par **quelques paires** (quelques paires de même famille et de même écriture portent la
moyenne ; les autres sont à peine au-dessus du hasard). La preuve correcte est donc **conditionnelle** :
*la structure compte **à l'intérieur d'une écriture***, pas « la famille explique tout ». Et les deux
généalogies — celle de Panini et celle de Glottolog — sont **le même arbre là où elles se rencontrent** ;
ce qui diverge n'est pas la forme, c'est la **couverture** (la fonction de distance de Panini ne couvre
qu'une minorité des langues du corpus) et la **granularité** (quatre niveaux, dont un « inconnu » qui est
une valeur manquante, pas une distance).

## 5. Les deux faces de la généalogie (J3.2)

| face | ce qu'elle mesure | unité | ce qu'elle ne peut pas dire |
|---|---|---|---|
| **atomes** (14) | une signature lexicale de texte | le texte / l'œuvre | la proximité historique de deux langues |
| **dhātus** (9) | des **macros** de V14, des motifs de contraintes | le token / le graphe | un axe indépendant : ils ne sont pas un second jeu d'atomes |
| **langue** (Glottolog + retrieval) | une classification + une surface partagée | la langue / la paire de textes | le sens profond : le retrieval est de surface |

Trois conséquences pour la théorie :

1. **Les 14 atomes ne sont pas 14 dimensions.** Sur les signatures de Panini, l'ACP donne **un petit nombre**
   de dimensions effectives — quelques-unes sur la corrélation des parts, une seule sur la covariance ;
   les atomes sont plus colinéaires que des colonnes indépendantes. Le nombre **9** des dhātus est **architectural**, pas
   mesuré : sans matrice publiée dhātu → V14, il n'est pas identifiable. La théorie doit dire **ce que
   les dhātus ajoutent** (des contraintes, des dépendances non adjacentes), pas les compter comme des
   primitives.
2. **La face atomes n'est pas disponible sur le corpus commun.** Panini n'a décomposé qu'une minorité
   des 21 langues. Tant que la signature V14 n'est pas multilingue, la confrontation atomes ↔ généalogie
   **sur le même corpus** reste à faire : c'est la mesure qui manque, pas un résultat négatif.
3. **La face langue est script-gated.** Le retrieval de surface ne traverse pas les écritures ; la famille
   est un résidu **intra-écriture**, faible et fragile. Une généalogie de langues doit donc être mesurée
   avec l'écriture contrôlée, sur un corpus **équilibré** (plusieurs familles par écriture, plusieurs
   branches par famille), et non sur un échantillon stratifié par famille.

## 6. Où en est Drave (état au 07/11)

- **langues** : 448 langues UDHR ; la surface est **lue à 80-100 %** ; le **sens** se retrouve à **96 %**
  sur les paires bien couvertes, **16 %** sur 100 langues stratifiées, **3,5×** le hasard dans un vivier
  ouvert ;
- **dialectes** : 100 % lisibles ; contenu retrouvé **30 à 100 %** selon la couverture de la langue ;
- **styles / traducteurs** : 87-100 % lisibles ; contenu **6-24 %** — *et ce chiffre est encore confondu
  avec l'alignement et l'époque* ✗✓ ;
- **corpus commun** (J2.2) : 21 textes, 5 familles, 10 écritures, article 1 de la DUDH, 1948 ;
- **retrieval à époque contrôlée** (J3.1) : l'écriture domine, l'époque ne pèse pas à écriture contrôlée,
  le brut est un effet de composition ;
- **généalogie à deux faces** (J3.2) : les deux généalogies sont le même arbre là où elles se rencontrent ;
  la fonction de distance de Panini couvre une minorité des langues et code les paires les plus proches
  comme inconnues ; le retrieval est script-gated ; la face atomes n'est pas disponible sur les 21
  langues.

**Le chantier** : construire la **généalogie** (familles, branches) pour les 448 langues — Glottolog est
la source de référence — et **organiser les tests par niveau**, en contrôlant l'époque **et** l'écriture.
C'est ce qui manque pour dire que la couche entrée-sortie est **riche** au sens fort, et pas seulement
large.

## 7. Ce qui reste à mesurer

1. **Une signature V14 multilingue** sur les 21 langues du corpus commun : c'est la seule manière de
   confronter les atomes à la généalogie **sur le même corpus**. Le test : les parts d'atomes sont-elles
   invariantes entre traductions (universalité) ou clusterisent-elles par famille (filiation) ?
2. **Une matrice 9 dhātus → 14 atomes** publiée, et la réconciliation des deux nomenclatures (sanskrit et
   computationnelle).
3. **Une distance Panini continue** (ou l'extension de `LANG_TREE` aux 21 langues) : l'échelle à quatre
   niveaux sature et son « inconnu » n'est pas une distance.
4. **Un corpus équilibré** même écriture / familles différentes, avec plusieurs branches par famille :
   le corpus actuel ne donne que quelques paires de même famille et de même écriture.
5. **Un retrieval neuronal** : la porte du script peut être une propriété des n-grammes, pas du sens.
6. **Un corpus multi-époques** avec les mêmes langues : l'avertissement de Panini sur l'époque ne peut pas
   être testé sur un corpus mono-époque. Sur le §334, il faudrait en plus les **dates de traduction** et
   un **support commun** même-tradition × longue époque : sans eux, la date et la filiation restent
   confondues.
7. **Des poids d'arêtes Glottolog** : la distance de chemin traite toutes les arêtes comme égales.

*La théorie est là ; les mesures sont dans `reports/`. Ce qui manque n'est pas une opinion, c'est une
signature V14 multilingue et un corpus équilibré.*

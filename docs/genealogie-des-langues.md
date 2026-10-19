# La généalogie des langues, des dialectes et des styles

> **Ce que cette page est.** La **théorie** de la structure généalogique qui doit organiser l'**étage entrée-sortie** (nom historique : « couche commune »)
> entrée-sortie de Drave, et ce que les projets complémentaires **Panini** et **Nipada** ont établi sur elle. Les
> mesures de Drave sont dans [`reports/07-mesures-couche-commune.md`](../reports/07-mesures-couche-commune.md).
> *À relire et à mettre à jour à chaque cycle : Panini et Nipada sont des sources vivantes.*

## 1. Pourquoi une généalogie

Une couche entrée-sortie ne peut pas être « riche en langues » au sens d'une **liste**. Les langues forment une
**structure** : des familles, des branches, des dialectes, des styles, et des **traductions** qui traversent tout
cela. Si la structure est réelle, elle doit se voir dans les états du modèle — et si elle ne s'y voit pas, c'est le
modèle qui est incomplet.

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

Les deux projets attaquent le même objectif par l'**autre bout** : **Panini** décompose le texte en **14 atomes
sémantiques** (∃ ∆ ∼ ↗ ⊙ ⧖ ◇ № ⊕ ⊗ λ ⊞ ≍ ≡) et **9 dhātus**, et **Nipada** fait tourner ce graphe comme un tissu
computationnel (SAT-solver trinaire, programmes de dhātus) — *une approche **algébrique** là où Drave est
**statistique***. Ils se rejoignent sur un point : il faut une **structure** entre les langues, pas une liste.

**Leur résultat le plus utile pour nous est un avertissement** ✗✓. En cherchant si leur signature lexicale (14
atomes de fréquence) reproduit la **généalogie** d'un corpus de textes philosophiques (grec, latin, arabe,
sanskrit, chinois, français, allemand), ils ont trouvé (rapport §150) :

| variable | coefficient | lecture |
|---|---:|---|
| **époque** (années) | **+0,138** | **dominant** |
| **généalogie** (distance dans l'arbre) | **+0,049** | faible |
| tradition (même école) | +0,002 | nul |

*Leur conclusion : **la signature de surface capte l'époque, pas la filiation*** ✗✓ — « l'héritage transmet les
**concepts**, pas les **signifiants** ». Et leur remède proposé : des **embeddings denses multilingues** projetés sur
les atomes, pour supprimer le confondant langue/époque.

## 3. Ce que cela impose à nos tests

1. **contrôler l'époque** ✗✓ : un « style » mesuré sur deux traductions d'âges différents peut être de l'**époque**,
   pas du traducteur. Tout test de style doit apparier les dates, ou les déclarer.
2. **tester par niveau** ✓✓ : famille, branche, langue, dialecte, style — chacun avec son propre jeu de paires et son
   propre hasard (une paire de langues sœurs n'est pas une paire de familles différentes).
3. **ne pas confondre lisibilité et structure** ✗✓ : que la langue soit **lisible** dans l'état (80-100 %, mesure
   Drave) ne dit **rien** de la **généalogie** — Panini a montré qu'une signature de surface peut être dominée par
   l'époque.

## 4. La preuve que la structure compte (18/10)

La grille de 60 langues, regroupée par niveau Glottolog, donne un ordre **monotone** : **même branche 30,7 %** >
**même famille 22,0 %** > **familles différentes 15,2 %** (hasard 3,3 %) — *l'alignement du modèle suit la
généalogie* (fiche : `reports/07-mesures-couche-commune.md`, mesure 49). ⚠️ Le confondant de l'**écriture** reste ✗✓
(les paires « même branche » sont surtout CJK) : la réplication doit contrôler l'écriture.

## 5. Où en est Drave (état au 18/10)

- **langues** : 448 langues UDHR ; la surface est **lue à 80-100 %** ; le **sens** se retrouve à **96 %** sur les
  paires bien couvertes, **16 %** sur 100 langues stratifiées, **3,5×** le hasard dans un vivier ouvert ;
- **dialectes** : 100 % lisibles ; contenu retrouvé **30 à 100 %** selon la couverture de la langue ;
- **styles / traducteurs** : 87-100 % lisibles ; contenu **6-24 %** — *et ce chiffre est encore confondu avec
  l'alignement et l'époque* ✗✓.

**Le chantier** : construire la **généalogie** (familles, branches) pour les 448 langues — Glottolog est la source
de référence — et **organiser les tests par niveau**, en contrôlant l'époque. C'est ce qui manque pour dire que la
couche entrée-sortie est **riche** au sens fort, et pas seulement large.

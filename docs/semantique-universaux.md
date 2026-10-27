# Universaux sémantiques : ce que les écoles disent, ce que Drave en garde

> **Rôle.** Cette note fonde la **base fixe** de la couche sémantique. Elle ne remplace pas les mesures :
> elle fixe le vocabulaire, les invariants et les limites. Le protocole est dans
> [`protocole-semantique.md`](protocole-semantique.md) ; le premier résultat typé dans
> [`rapport-universaux.md`](../reports/rapport-universaux.md).

## 1. Pourquoi une base, et pas un vecteur libre

Un `z` contrastif retrouve un article, mais ne dit pas **ce qu'il contient**. Pour une couche **opérable**,
il faut un code **typé**, **fini**, **déterministe** : un tuple de champs fixes, chacun avec un vocabulaire
fixe. Le sens devient une **structure** que le raisonnement classique peut lire, et la restitution peut être
un **codec** exact plutôt qu'un décodeur neuronal approximatif.

## 2. Les écoles

### 2.1 Natural Semantic Metalanguage (NSM)

Wierzbicka et Goddard proposent une **réduction** du sens à des **primes sémantiques** universelles
(« I », « YOU », « SOMEONE », « THINK », « WANT », « GOOD », « BIG », « BECAUSE », « IF »…), combinées par
une grammaire minimale, et paraphrasables dans toutes les langues. La force : un **métalangage** contrôlé,
culturellement transparent. La limite : les primes et leur universalité sont **débattues**, et la liste ne
suffit pas à elle seule à typers un domaine technique.

Source : [NSM](https://nsm-approach.net/) ; [SEP, *Word Meaning*](https://plato.stanford.edu/entries/word-meaning/).

### 2.2 Sémantique conceptuelle (Jackendoff)

Jackendoff décrit la **structure conceptuelle** comme un niveau autonome, avec des catégories
(THING, EVENT, STATE, ACTION, PLACE, PATH, PROPERTY, AMOUNT) et des primitives de décomposition
(GO, STAY, CAUSE, LET…). La force : les **rôles** et l'**espace/trajectoire** sont explicites ; la limite :
toutes les primitives ne sont pas fixées, et le lien au lexique reste un programme de recherche.

Source : [Jackendoff, *Conceptual Semantics*](https://www.degruyterbrill.com/document/doi/10.1515/9783110226614.688/html).

### 2.3 Théorie Sens-Texte (Meaning-Text Theory)

Mel'čuk organise la langue en **strates** : représentation sémantique, syntaxe profonde, syntaxe de surface,
morphologie profonde, morphologie de surface. Les **actants** (I, II, III…) et les **fonctions lexicales**
(Syn, Anti, Conv, Oper, Func, Magn, Bon, Ver…) décrivent les relations de sens et les **paraphrases**. La
force : un pont explicite **sens ↔ texte** ; la limite : c'est un modèle **descriptif**, pas une base de
primitives universelles.

Source : Mel'čuk, *Dependency in Language* (2014), [PDF](http://olst.ling.umontreal.ca/pdf/Mel'%C4%8Duk_2014_Dependency%20in%20Language.pdf).

### 2.4 Les pionniers empiriques et formels

- **Frege** : sens/référence, compositionnalité.
- **Tarski** : vérité et modèle.
- **Montague** : types, lambda, quantification généralisée, sémantique modèle-théorique.
- **Davidson** : événements et quantification sur les événements.
- **Kamp** : représentation du discours et anaphores.
- **Barwise & Perry** : situations et canaux d'information.
- **Fillmore** : cadres sémantiques ; **Rosch** : prototypes ; **Berlin & Kay** : termes de couleur ;
  **Levinson** : cadres spatiaux ; **Talmy/Langacker/Lakoff** : cognition, espace, métaphore.

La force : la **composition** et les **types** sont explicites. La limite : ces théories ne donnent pas
toutes une **liste fermée** de primitives ; elles donnent des **contraintes** et des **opérations**.

Sources : [SEP, *Montague Semantics*](https://plato.stanford.edu/entries/montague-semantics/) ;
[SEP, *Word Meaning*](https://plato.stanford.edu/entries/word-meaning/) ;
[Levinson & Meira, espace](https://hal.science/hal-00939058/document).

### 2.5 Logique et mathématiques

La logique fournit des **ingrédients exacts** : types, lambda, connecteurs, quantificateurs, modalités,
théorie des modèles, théorie de la démonstration. Les mathématiques fournissent les **structures** :
ensembles, relations, ordres et treillis, catégories, **méréologie** (partie/tout), topologie, mesure,
probabilité, théorie de l'information. Ces ingrédients ne sont pas des « significations » : ce sont des
**opérations** et des **invariants** que la couche sémantique peut appliquer sans approximation.

Sources : [SEP, *Mereology*](https://plato.stanford.edu/entries/mereology/) ;
[SEP, *Church* (types)](https://plato.stanford.edu/archives/fall2026/entries/church/supplementD.html) ;
[SEP, *Category Theory*](https://plato.stanford.edu/entries/category-theory/).

### 2.6 La physique comme source d'ingrédients

La physique n'est pas une sémantique. Mais elle donne des **invariants de structure** utiles :

- **symétrie** = invariance sous un groupe de transformations ; une **classe d'équivalence** de descriptions
  (SEP, *Symmetry and Symmetry Breaking*) ;
- **théorème de Noether** : une symétrie continue ↔ une quantité conservée ;
- **état / observable / évolution** : un sens peut être un état, une observation, une transition ;
- **entropie / information** : l'ambiguïté et la nouveauté se mesurent ;
- **échelle / renormalisation** : le même sens à plusieurs granularités ;
- **unités et dimensions** : un nombre de coups n'est pas un nombre de points.

Ces notions servent de **contraintes de conception** : équivariance inter-langues, conservation du sens
dans la traduction, mesure d'ambiguïté, granularité explicite.

Sources : [SEP, *Symmetry*](https://plato.stanford.edu/entries/symmetry-breaking/) ;
[SEP, *Semantic Conceptions of Information*](https://plato.stanford.edu/entries/information-semantic/).

## 3. Les invariants qui reviennent

| invariant | écoles | usage Drave |
|---|---|---|
| **prédication typée** (entité, événement, état) | NSM, Jackendoff, Montague | type + identité |
| **rôles actanciels** (agent, patient, source, but) | Sens-Texte, cadres | champs de rôle |
| **espace et trajectoire** | Jackendoff, NSM, Levinson | `de`, `vers`, `chemin`, `point` |
| **temps et aspect** | NSM, Montague | avant/après/maintenant |
| **quantité et degré** | NSM, Montague | nombre, mesure, comparaison |
| **partie/tout** | méréologie, NSM | plateau, pièces, cartes |
| **modalité et polarité** | logique, Montague | opérateurs |
| **évaluation** | NSM | bon/mauvais |
| **information et ambiguïté** | Shannon, Barwise/Perry | confiance, canaux |
| **symétrie et conservation** | physique | équivariance, fidélité |
| **échelle** | physique, information | granularité du sens |

## 4. La base fixe proposée

Cinq niveaux, tous **finis** et **versionnés** :

1. **Atomes** : les primes NSM (liste fixe, identifiants stables), avec leurs équivalents multilingues.
2. **Types** : entité, événement, état, action, propriété, quantité, lieu, chemin, proposition.
3. **Rôles** : agent, patient, expérienceur, instrument, source, but, lieu, possesseur, partie.
4. **Paramètres** : les champs du domaine (jeu, action, `de`, `vers`, `case`, `carte`, `point`, `chemin`…),
   chacun avec un **vocabulaire fixe**.
5. **Opérateurs et invariants** : négation, conjonction, quantificateurs, modalité, temps/aspect,
   comparaison, causalité ; symétrie/équivariance, conservation, entropie, échelle.

**Sortie** : un **one-hot concaténé** sur les champs, lu par `argmax` — donc **déterministe**. Pas de `z`
libre. Le **décodeur** est un **codec classique** (RSN → surface), et le **raisonnement** lit le code typé.

## 5. Ce qu'on ne peut pas conclure

- Les primes NSM ne sont pas une ontologie formelle complète ; leur universalité est discutée.
- La sémantique conceptuelle est un programme, pas une liste close de primitives.
- Sens-Texte est un modèle linguistique descriptif, pas une théorie cognitive.
- La sémantique formelle est modèle-théorique ; elle ne donne pas un espace vectoriel.
- La physique fournit des **analogies et des contraintes**, pas des significations.
- Un code typé **exact** sur un corpus ne prouve pas la **généralisation** à des surfaces inconnues : c'est
  pourquoi le parseur natif est mesuré à part, avec contrôle négatif.

## 6. Conséquence pour le protocole

Le protocole « embedding libre puis décodeur » a échoué sur la restitution (chrF 14,0 contre un plancher
38,8). La base typée change le contrat : le **code** est la sémantique, le **codec** est la restitution,
le **raisonnement** est classique. Le modèle natif doit être jugé sur sa **fidélité au code**, pas sur un
vecteur latent. Résultat du premier passage : le codec lit **100 %** des coups B5/B7, le parseur natif typé
**surapprend** (48,3 % train, 0 % validation). Détail :
[`rapport-universaux.md`](../reports/rapport-universaux.md).

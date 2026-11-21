# La RSN à trois niveaux — les travaux comparables

> **Ce que ce document est.** La **recherche bibliographique** qui situe la RSN à trois niveaux
> (le noyau, les faits, les affirmations) dans les travaux existants : ce qui a été fait, par qui,
> avec quel résultat, et **ce que Drave en reprend ou en écarte**. La théorie :
> [`rsn-3-niveaux.md`](../docs/theorie/rsn-3-niveaux.md) ; le code : [`tools/rsn.py`](../tools/rsn.py).
>
> **Une réserve.** Les sources ont été trouvées et lues **au 21/11** ; les liens sont donnés, les
> affirmations sont celles des résumés, pas des relectures complètes. Aucun chiffre de ces travaux
> n'est repris comme un résultat de Drave.

## 1. La structure en trois niveaux — qui a déjà essayé

### 1.1 Le découplage savoir / raisonnement (Wang, 2026)

**La référence** : *Decoupling Knowledge and Reasoning: A Brain-Inspired Architecture for Traceable,
Hallucination-Free AI with Quantified Uncertainty*, Yi-Chuan Wang, Zenodo, juin 2026
([le dépôt](https://zenodo.org/records/20709229)).

**Ce qu'il propose** : une architecture à **trois modules** — le **stockage du savoir**, l'**analyse
du contexte**, le **raisonnement** — séparés **au niveau de l'entraînement** pour éliminer
l'hallucination et fournir une **incertitude quantifiée**. La v2 ajoute un prototype complet, des
validations E1–E5, et une couche de **savoir causal** extraite d'une base de **496 555 faits**
Wikipédia.

**Ce qui est proche** : la séparation en trois étages, l'incertitude quantifiée, la traçabilité.
**Ce qui diffère** : Wang sépare des **modules d'entraînement** ; la RSN sépare des **niveaux de
qualification** (le noyau prouve, les faits degrés, les affirmations contexte). Le premier est une
**architecture de réseau** ; la seconde une **architecture de données**.

### 1.2 La stratification formelle (Nipada / Panini)

**La référence** : [`../Panini/research/philosophy-theory/DOCUMENT_DE_CONTEXTE_v3.0.md`](../../Panini/research/philosophy-theory/DOCUMENT_DE_CONTEXTE_v3.0.md)
(le projet parent) — le noyau formel (Ł3, unification, résolution), la couche descriptive (les
degrés, les hypothèses), la promotion par dérivation.

**Ce qui est proche** : c'est la **source** de la structure des trois niveaux.
**Ce qui diffère** : Nipada vise un **système formel complet** ; la RSN en reprend la **séparation**,
avec un noyau **minimal**.

## 2. Les approches comparables, par niveau

### 2.1 Le niveau 1 — le noyau formel

| approche | référence | ce qu'elle fait | ce que la RSN en reprend | ce qu'elle écarte |
|---|---|---|---|---|
| **les assistants de preuve** | Lean 4, Coq, Isabelle | un **kernel** qui vérifie les dérivations ; le reste est non fiable | l'idée d'un **vérificateur auditable** et la séparation « automatismes / noyau » | la lourdeur (la RSN n'a pas besoin d'un kernel complet) |
| **la programmation logique** | Prolog, Datalog | l'unification et la résolution avec retour arrière | l'unification et la **résolution** comme inférence de base | le moteur complet |
| **la logique trinaire** | Łukasiewicz (Ł3) | trois valeurs : vrai, faux, inconnu | le **tri-état** du noyau | — |

**Le constat** : le noyau à trois valeurs est **bien établi** (les assistants de preuve, la logique
trinaire). Ce qui manque à Drave n'est pas l'idée, c'est **l'implémentation** (le kernel).

### 2.2 Le niveau 2 — les faits et le flou

| approche | référence | ce qu'elle fait | ce que la RSN en reprend | ce qu'elle écarte |
|---|---|---|---|---|
| **Probabilistic Soft Logic** (PSL) | Bach et al., *Hinge-Loss Markov Random Fields and Probabilistic Soft Logic*, JMLR 2017 ([le papier](http://xxx.itp.ac.cn/abs/1505.04406v1)) | des **règles logiques pondérées** sur des variables **continues** [0,1] ; l'inférence est une optimisation convexe | les **degrés [0,1]** sur les faits, les règles de composition floues | le cadre probabiliste complet (la RSN n'a pas besoin d'un champ de Markov) |
| **la logique floue** (Zadeh) | Zadeh, *Fuzzy Sets*, 1965 | les degrés d'appartenance [0,1] | le **degré de confiance** d'un fait | la théorie de l'ensemble flou complète |
| **Markov Logic Networks** | Richardson & Domingos, 2006 | des formules logiques pondérées | l'idée de **règles pondérées** | le coût (l'inférence est exponentielle) |
| **aProbLog / ProbLog** | Kimmig et al. ([le papier](https://ar5iv.labs.arxiv.org/html/1312.4328)) | la **programmation logique probabiliste** : les faits ont une probabilité | la séparation faits / règles | la sémantique probabiliste (la RSN est **fuzzy**, pas probabiliste) |

**Le constat** : la RSN a choisi **le flou (Zadeh) et non le probabiliste** — c'est un choix
assumé. Le flou compose les degrés par des **règles** (le min/max), le probabiliste par des
**produits** ; le premier est plus simple et plus lisible, le second plus rigoureux. **La RSN ne
fait pas d'inférence probabiliste** — elle fait de la **qualification**.

### 2.3 Le niveau 3 — les affirmations et leur contexte source

| approche | référence | ce qu'elle fait | ce que la RSN en reprend | ce qu'elle écarte |
|---|---|---|---|---|
| **RDF-star / les identifiants d'énoncé** | le W3C ([la spécification](https://www.w3.org/2021/rdf-star/)) | les **assertions sur les assertions** : on peut attacher une provenance à un triple | le **contexte source** attaché à chaque affirmation | le modèle RDF complet |
| **PROV-O** | le W3C ([la spécification](https://www.w3.org/TR/prov-o/)) | la **provenance** (entité, activité, agent) | la **traçabilité** de la provenance | le vocabulaire OWL complet |
| **les truth maintenance systems** | Doyle (1979), de Kleer (1986) | les **justifications** des faits ; quand un fait tombe, ses dépendants tombent | le **statut** (hypothèse/retenu/réfuté) et la **justification** | le mécanisme complet de propagation |
| **les argumentations frameworks** | Dung (1995), *On the acceptability of arguments* | les **arguments** attaqués/défendus, l'acceptabilité | le **statut** et la **réfutation** (la négation explicite) | le calcul des extensions |

**Le constat** : la **provenance** et le **statut** sont des problèmes **résolus** dans la littérature
(RDF-star, PROV-O, TMS, Dung). La RSN en reprend les **idées**, pas les formats : son `contexte`
(texte, span, version) et son `statut` (hypothèse, retenu, réfuté, ouvert) sont les **briques
minimales** qui suffisent à la falsifiabilité.

### 2.4 Le neuro-symbolique — le pont

| approche | référence | ce qu'elle fait | ce que la RSN en reprend |
|---|---|---|---|
| **DeepProbLog** | Manhaeve et al., NeurIPS 2018 ([le papier](https://neurips.cc/virtual/2018/spotlight/12755)) | un réseau neuronal **dans** une programme logique : les probabilités des réseaux deviennent les faits du raisonnement | l'idée du **pont** entre le neuronal (la surface) et le symbolique (le noyau) |
| **les agents neuro-symboliques** | *Autonomous Skill Development: Neuro-Symbolic Agents that Self-Generate Verifiable Tools* ([le papier](https://publications.hevs.ch/index.php/attachments/single/2000)) | des agents qui **génèrent** des outils vérifiables | l'idée de **vérification** des sorties |

**Le constat** : le neuro-symbolique est **le cadre** de la RSN (la surface neuronale, le noyau
symbolique). Drave a déjà la surface (le bloc linguistique) ; le pont est la **promotion** — qui
reste à implémenter.

## 3. Ce que la RSN a d'original

1. **Le contexte source comme citoyen de première classe** : la littérature (RDF-star, PROV-O)
   traite la provenance comme une **annotation** ; la RSN en fait un **champ du candidat**, et la
   falsifiabilité en dépend.
2. **Le flou assumé, le probabiliste écarté** : le choix de Zadeh contre les réseaux bayésiens est
   explicite — la RSN **qualifie**, elle ne **calcule pas de probabilité**. C'est plus faible, mais
   plus lisible, et surtout **composable** avec le tri-état du noyau.
3. **La structure en couches, pas en modules** : Wang sépare des **modules d'entraînement** ; la RSN
   sépare des **niveaux de qualification**. On peut ajouter un concept (une affirmation) sans
   toucher le noyau — c'est l'**extensibilité** que les architectures modulaires n'ont pas.

## 4. Ce que la RSN n'a pas (les limites, dites)

- **Pas de kernel de vérification** : les assistants de preuve en ont un ; la RSN n'a que le
  tri-état, pas la preuve.
- **Pas de sémantique probabiliste** : PSL, ProbLog et les MLN font mieux sur l'incertitude
  quantifiée ; la RSN est plus simple, et plus faible.
- **Pas de calcul d'extensions** : Dung fournit le cadre de l'acceptabilité ; la RSN n'a que le
  statut local, pas la propagation globale.
- **Pas de format standard** : RDF-star et PROV-O sont des standards ; la RSN a son schéma
  `drave.rsn` v1, qui n'est **pas** encore publié.

## 5. La conclusion (ce que la recherche dit)

**La structure en trois niveaux n'est pas une invention** : elle est **convergente** avec les
travaux de 2026 (Wang), avec les standards du web sémantique (RDF-star, PROV-O), avec la logique
floue et la programmation logique probabiliste. Ce qui est **propre** à la RSN, c'est la
**combinaison** : le noyau minimal (Ł3), les faits flous (Zadeh), les affirmations à contexte source,
**sans** les coûts des cadres complets.

**La leçon** : ne pas réinventer le noyau (les assistants de preuve l'ont), ne pas réinventer la
provenance (RDF-star l'a), **mais** garder le **contrat minimal** qui rend la RSN utilisable par un
moteur de pensée — c'est la position de Drave, et elle est **défendable**.

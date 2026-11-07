# Table de correspondance — 14 atomes de Panini et 8 niveaux de Drave

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.1 · **Date** : 2026-11-07
> **Verdict** : ✅ **la table est complète** — 14 atomes, 8 niveaux, 14 lignes, un ancrage et un porteur par
> atome, une mesure possible et son contrôle négatif. ⚠️ **aucune correspondance atome ↔ niveau n'est mesurée à
> ce stade** : c'est une **hypothèse de lecture** et un **protocole**, pas une corrélation. La calibration des
> 44 œuvres de Panini montre **33 paires d'atomes à |r| ≥ 0,5** (brut), **4 composantes > 1** et **80,7 %** de
> la variance sur les trois premières (ACP sur CLR) : la colinéarité est le premier confondant, avant même
> l'époque.
> **Dispositif** : lecture seule de `../../Panini/research` (HEAD `e10d695`, 2026-10-25) ; signatures
> `../../Panini/research/nipada/falsification/analytic_sigs_v1.json` (44 œuvres, 2026-10-18) ; contrat des
> niveaux `../docs/theorie/contrat-bloc-langue.md` ; JSON [`atomes-niveaux.json`](atomes-niveaux.json).
> **Aucune écriture dans Panini** : les seuls fichiers produits sont cette fiche et son JSON.

## 1. La question, et ce que la table n'est pas

Un **atome V14** est une **primitive sémantique** (Panini : ∃ ÊTRE, ∆ DIFFÉRENCE, ∼ RAPPORT, …). Un **niveau**
est une **taille d'unité d'annotation** (Drave : graphème, mot, pos, syntagme, phrase, pragmatique, discours,
document). Rien ne garantit une bijection entre les deux : un atome peut traverser plusieurs niveaux, et un
niveau peut porter plusieurs atomes.

La table répond, pour chaque atome, à trois questions :

- **ce qu'il capte** : la glose de V14, dans les termes de Panini ;
- **où il a une marque observable** : le niveau d'**ancrage**, la plus petite unité où l'atome a un marqueur
  dédié (un diacritique pour ∆, une copule pour ∃, un numéral pour №) ;
- **où il devient mesurable** : le niveau **porteur**, celui où l'atome est une contribution sémantique que
  Drave peut annoter et compter (la négation dans la phrase pour ∆, l'assertion d'existence pour ∃).

Trois portées sont distinguées :

| portée | sens | exemple |
|---|---|---|
| **direct** | un seul niveau suffit à porter l'atome | № → mot ; ⊗ → pos |
| **distribué** | l'atome est mesurable à plusieurs niveaux, avec des signaux différents | ∆ : graphème (paire minimale) et phrase (négation) |
| **émergent** | l'atome n'est lisible qu'au niveau supérieur ; l'ancrage n'est qu'un précurseur | ⊞ : le syntagme précède, le document porte |

**Ce que la table n'est pas.** Elle n'est pas une preuve que V14 est minimal — Panini écrit lui-même que
l'irréductibilité de V14 n'est **pas démontrée** (dette D2, `../../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md`
§ 1.6) ; elle n'est pas une mesure de similarité ; elle ne dit rien de la généalogie des langues. C'est une
**grille de lecture** et un **plan de mesure**.

## 2. Sources et méthode

### 2.1 Les atomes (Panini, V14 de Research)

- `../../Panini/README.md` § 5–6 : les 14 atomes, les 9 dhātus, l'avertissement β (époque **+0,138**,
  filiation **+0,049**).
- `../../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md` § 1.1 (liste, primes), § 1.4
  (classification périodique), § 1.5 (régime logique), § 1.6 (V14 = hypothèse de travail).
- `../../Panini/research/philosophy-theory/GRILLE_ABLATION_V14_v0.1.md` § 2 (rôle de chaque atome et
  prédiction d'ablation).
- `../../Panini/research/nipada/falsification/analytic_sigs_v1.json` : 44 œuvres × 14 parts, somme 1.

**Vocabulaire retenu** : V14 de **Research** uniquement. Les 34 atomes de Panini-FS et les 9 dhātus de l'ancien
`docs/` de l'hôte sont des lignes divergentes ; ils ne sont pas utilisés ici (voir
`rapport-inventaire-panini.md` § 0.5).

### 2.2 Les niveaux (Drave)

- `../docs/theorie/contrat-bloc-langue.md` § 2 : `NIVEAUX = ("graphème", "morphème", "mot", "pos",
  "syntagme", "phrase", "discours", "pragmatique", "document")`.
- `../docs/theorie/pre-traitement-linguistique.md` § 2 : ce que chaque niveau étiquette, et ce qui reste au
  réseau.
- `rapport-bloc-linguistique.md` § 4 : les neuf niveaux et leurs couvertures mesurées.

**Le choix des huit niveaux.** Le contrat en compte **neuf** avec `morphème` ; le mandat J2.1 en liste **huit**,
sans `morphème`. La table suit le mandat. Le morphème reste un **ancrage possible** pour ∆ (affixes, diacritiques)
et λ (dérivation), mais il n'est pas retenu comme porteur : il ne change pas la lecture d'ensemble. Si on
l'ajoutait, ∆ et λ seraient les deux lignes à réexaminer.

### 2.3 La méthode

Pour chaque atome, quatre décisions explicites, toutes **argumentées, pas mesurées** :

1. la **glose** : ce que Panini met dans l'atome, avec ses mots ;
2. l'**ancrage** : la plus petite unité où l'atome a une marque observable et non ambiguë ;
3. le **porteur** : le niveau où l'atome est une contribution sémantique mesurable, et non un simple effet de
   surface ;
4. la **mesure possible** : un signal, une métrique, un contrôle négatif, et ce qui la rendrait fausse.

Le choix du porteur est un **choix de mesure**, pas une essence. Un même atome peut avoir un autre porteur dans
une autre tâche : ∆ est graphémique pour l'orthographe et phrastique pour la négation ; ⊕ est syntagmatique pour
le sens spatial et documentaire pour la mise en page. Le JSON conserve le choix et les alternatives.

## 3. La table — 14 atomes, 14 lignes

> **Lecture.** `Ancrage → porteur` : le niveau minimal où l'atome a une marque, puis le niveau où il est mesuré.
> `Portée` : `direct`, `distribué` ou `émergent` (voir § 1). Les mesures sont des **propositions** : elles
> décrivent le dispositif à construire en J2.2, pas un résultat.

| # | Atome | Ce qu'il capte (V14) | Ancrage → porteur | Portée | Mesure possible | Contrôle négatif |
|---:|---|---|---|---|---|---|
| 1 | **∃ ÊTRE** (2) | présence, substrat, existence ; copule, « il y a », subsomption | mot → phrase | distribué | copules et existentiels par phrase → taux de prédications existentielles ; ρ avec la part de ∃ | paraphrase en verbes lexicaux ; permutation de la colonne ∃ |
| 2 | **∆ DIFFÉRENCE** (3) | distinction, négation, privatif, écart, seuil | graphème → phrase | distribué | paires minimales (diacritique, casse, lettre) → taux de discrimination ; négations par phrase → taux ; ρ avec la part de ∆ | neutraliser diacritiques et casse ; retirer les négations ; permutation |
| 3 | **∼ RAPPORT** (5) | mise en relation, préposition/cas, lien orienté | pos → syntagme | distribué | dépendances et attachements → F1 d'attachement, densité d'arêtes, distance moyenne ; ρ avec la part de ∼ | mélanger les têtes ; arbre aléatoire ; permutation |
| 4 | **↗ ORIENTATION** (7) | direction du flux, visée, transmission | syntagme → discours | distribué | sens des attachements, ordre temporel/causal, connecteurs → accuracy d'ordre, ratio avant/arrière ; ρ avec la part de ↗ | inverser l'ordre ; mélanger les phrases ; permutation |
| 5 | **⊙ SUJET** (11) | agent, expérienceur, point de vue situé | pos → syntagme | distribué | rôle sujet/agent, personne, accord → F1 du rôle sujet, taux de sujets agentifs ; ρ avec la part de ⊙ | passiver ou impersonnaliser ; permutation |
| 6 | **⧖ TEMPS** (13) | durée, séquence, ancrage temporel | pos → phrase | distribué | temps/aspect, adverbes temporels, ordre → F1 temps/aspect, densité temporelle ; ρ avec la part de ⧖ | retirer la morphologie temporelle ; texte sans temps ; permutation |
| 7 | **◇ MODALITÉ** (17) | possible, nécessaire, obligation, engagement | pos → pragmatique | distribué | auxiliaires modaux, hedges, actes → F1 modalité/acte, taux de modaux, κ inter-annotateurs ; ρ avec la part de ◇ | retirer modaux et hedges ; permutation |
| 8 | **№ NOMBRE** (19) | quantité, cardinalité, comptage | mot → mot | direct | numéraux, quantifieurs, dates → exact match, taux de numéraux ; ρ avec la part de № | remplacer les chiffres par des mots ; obfusquer ; permutation |
| 9 | **⊕ ESPACE** (23) | localisation, topologie, étendue, métaphore spatiale | pos → syntagme | distribué | PP locatifs, deixis here/there, rôles lieu → F1 rôle lieu, taux de PP locatifs ; ρ avec la part de ⊕ | retirer les prépositions spatiales ; permutation |
| 10 | **⊗ OPÉRATION** (29) | action, acte, application d'un opérateur | mot → pos | direct | VERB/AUX, prédicats, aktionsart → accuracy VERB/AUX, taux de verbes, F1 prédicat ; ρ avec la part de ⊗ | nominaliser les verbes ; permutation |
| 11 | **λ FONCTION** (31) | finalité, usage, téléologie, morphisme typé | pos → syntagme | distribué | but, moyen, fonction d'un constituant → F1 rôle but/fonction, taux de constructions finales ; ρ avec la part de λ | retirer les marqueurs de but ; permutation |
| 12 | **⊞ STRUCTURE** (37) | organisation, agencement, ensemble + axiomes | syntagme → document | émergent | régions, TOC, hiérarchie, structure argumentale → F1 frontières de régions, profondeur de l'arbre, couverture TOC ; ρ avec la part de ⊞ | aplatir ou mélanger les sections ; permutation |
| 13 | **≍ SYMÉTRIE** (41) | équilibre, invariance, harmonie, répétition équilibrée | graphème → discours | émergent | parallélisme, coordination, sections équilibrées, palindromes → score de parallélisme, variance des longueurs ; ρ avec la part de ≍ | casser le parallélisme ; permutation |
| 14 | **≡ ÉQUATION** (43) | égalité, équivalence, identité, définition | syntagme → phrase | émergent | copule équative, définitions, « = », renvois → F1 définition/équation, taux de copules équatives ; ρ avec la part de ≡ | remplacer les définitions par des descriptions ; permutation |

## 4. Ce que la table dit

### 4.1 La répartition des porteurs

| porteur | atomes | nombre |
|---|---|---:|
| **phrase** | ∃, ∆, ⧖, ≡ | 4 |
| **syntagme** | ∼, ⊙, ⊕, λ | 4 |
| **discours** | ↗, ≍ | 2 |
| **mot** | № | 1 |
| **pos** | ⊗ | 1 |
| **pragmatique** | ◇ | 1 |
| **document** | ⊞ | 1 |
| **graphème** | — (ancrage de ∆ et ≍) | 0 |

**Le graphème n'est pas un porteur sémantique.** Il est l'**ancrage minimal** de ∆ (une différence de trait) et
de ≍ (une symétrie visuelle), mais aucun atome ne s'y mesure seul : un diacritique distingué ne dit pas encore
ce que le texte **dit**. C'est un résultat de la table, pas un oubli.

**La phrase et le syntagme portent huit atomes sur quatorze.** C'est cohérent avec la nature compositionnelle
du sens : l'existence, la différence, le temps et l'équation se jugent dans la phrase ; la relation, l'agent,
l'espace et la finalité se lient dans le syntagme. Les niveaux « profonds » (pragmatique, discours, document)
portent les atomes les plus **émergents** : modalité, orientation, symétrie, structure.

### 4.2 Trois atomes à portée directe, et pourquoi ils sont les premiers candidats

- **№ NOMBRE → mot** : un numéral est un token, sa cardinalité est vérifiable, l'exact match est une mesure
  dure.
- **⊗ OPÉRATION → pos** : un verbe est une classe, son étiquette est un gold, l'accuracy est directe.
- **⊞ STRUCTURE → document** : une région est un span, la frontière est un gold, le F1 est standard.

Ces trois lignes sont les seules où l'atome et le niveau se ressemblent assez pour qu'une corrélation soit
interprétable **sans** composition. Elles serviront de **témoins** : si elles ne corrèlent pas, le problème est
la signature lexicale de Panini, pas la table.

### 4.3 Une projection, pas une bijection

Le même atome peut avoir un autre porteur selon la tâche. La table choisit le porteur **le plus informatif pour
une mesure de texte**, pas le porteur « vrai ». C'est pourquoi le JSON porte, pour chaque atome, `ancrage`,
`porteur`, `niveaux_secondaires` et `portee`. Une table à une seule colonne aurait été plus lisible et moins
honnête.

## 5. Calibration des 44 œuvres — ce que les signatures disent déjà

La calibration est **descriptive** : elle ne teste pas la table, elle décrit le corpus qui servira à la tester.
Source : `../../Panini/research/nipada/falsification/analytic_sigs_v1.json`, 44 œuvres, parts normalisées
(somme 1). Les œuvres sont majoritairement philosophiques et religieuses ; ce n'est pas un corpus équilibré.

### 5.1 Parts moyennes

| atome | moyenne | écart-type | min | max | CV |
|---|---:|---:|---:|---:|---:|
| ∃ ÊTRE | 0,1074 | 0,0326 | 0,0506 | 0,1657 | 0,30 |
| ∆ DIFFÉRENCE | 0,0232 | 0,0106 | 0,0040 | 0,0435 | 0,46 |
| ∼ RAPPORT | 0,0882 | 0,0347 | 0,0332 | 0,1751 | 0,39 |
| ↗ ORIENTATION | 0,0062 | 0,0031 | 0,0009 | 0,0146 | 0,50 |
| ⊙ SUJET | 0,1890 | 0,0282 | 0,0873 | 0,2331 | 0,15 |
| ⧖ TEMPS | 0,0801 | 0,0233 | 0,0188 | 0,1273 | 0,29 |
| ◇ MODALITÉ | 0,0365 | 0,0195 | 0,0025 | 0,0981 | 0,53 |
| № NOMBRE | 0,0960 | 0,0336 | 0,0569 | 0,2246 | 0,35 |
| ⊕ ESPACE | 0,0482 | 0,0192 | 0,0069 | 0,0903 | 0,40 |
| ⊗ OPÉRATION | 0,0831 | 0,0220 | 0,0173 | 0,1360 | 0,27 |
| λ FONCTION | 0,0962 | 0,0237 | 0,0383 | 0,1400 | 0,25 |
| ⊞ STRUCTURE | 0,1170 | 0,0204 | 0,0873 | 0,1608 | 0,17 |
| ≍ SYMÉTRIE | 0,0029 | 0,0016 | 0,0003 | 0,0090 | 0,56 |
| ≡ ÉQUATION | 0,0260 | 0,0170 | 0,0044 | 0,1004 | 0,66 |

**Deux atomes sont au plancher** : ≍ SYMÉTRIE (moyenne **0,0029**) et ↗ ORIENTATION (**0,0062**). Ce sont
précisément les deux atomes dont le porteur est `discours` : leur mesure sera la plus bruitée. Il faudra soit
un corpus plus riche en parallélisme et en orientation, soit une mesure dédiée (répétition, ordre) plutôt qu'une
corrélation avec une part globale.

### 5.2 Les atomes ne sont pas indépendants

Sur les 44 œuvres, **33 paires** d'atomes ont |r| ≥ 0,5 en brut. Les plus fortes :

| paire | r brut | r CLR |
|---|---:|---:|
| № NOMBRE ↔ ≡ ÉQUATION | **+0,923** | +0,577 |
| ∃ ÊTRE ↔ ∆ DIFFÉRENCE | **+0,857** | +0,581 |
| ∃ ÊTRE ↔ ∼ RAPPORT | **−0,846** | −0,420 |
| ∼ RAPPORT ↔ ⊕ ESPACE | **−0,829** | −0,751 |
| ∃ ÊTRE ↔ ⊕ ESPACE | +0,796 | — |
| ∼ RAPPORT ↔ ◇ MODALITÉ | −0,760 | — |

Les parts sont des **données compositionnelles** (somme 1) : une corrélation brute est mécaniquement contrainte.
Le passage au **CLR** (log-ratio centré, remplacement des zéros par 1e−6) change la structure : par exemple
№ ↔ ≡ passe de **+0,923** à **+0,577**, et ∃ ↔ ∼ de **−0,846** à **−0,420**. Certaines restent fortes
(∼ ↔ ⊕ : −0,829 → **−0,751**), d'autres apparaissent (∼ ↔ ⊞ : **+0,925** en CLR). **Conclusion : toute
corrélation atome ↔ niveau doit être calculée sur les parts transformées, pas sur les parts brutes.**

Une ACP sur les parts CLR donne **4 composantes de valeur propre > 1** ; les trois premières expliquent
**80,7 %** de la variance (6,967 · 2,845 · 1,491 · 1,260 · …). Autrement dit, dans ce corpus, les 14 atomes
n'occupent que **quatre dimensions effectives**. Une table qui traiterait les 14 atomes comme 14 mesures
indépendantes surestimerait massivement l'information disponible.

**Ce que cette calibration n'est pas** : un test de la table. Elle ne contrôle ni la date, ni la langue, ni le
genre ; elle ne dit pas si un atome « porte » un niveau. Elle dit que le corpus de départ est **petit, colinéaire
et déséquilibré**, et que le protocole doit en tenir compte.

## 6. Protocole de mesure — ce qu'il faudra faire en J2.2

### 6.1 Le corpus commun

- **20 textes** au minimum, avec le même identifiant des deux côtés, le même découpage (premiers 10 000 mots,
  comme `analytic_sigs_v1.json`), et les mêmes métadonnées : date, langue, famille, genre.
- **Au moins 5 genres** et **3 familles** ; sinon, l'époque et le genre expliqueront tout.
- Les signatures Panini (14 parts) et les annotations Drave (9 niveaux, dont 8 retenus) sont produites sur le
  **même texte**, pas sur deux traductions différentes.

### 6.2 Les variables

- **X** : les 14 parts d'atomes, transformées en **CLR** (ou ALR) ; jamais les parts brutes.
- **Y** : pour chaque atome, **une** variable principale pré-enregistrée (§ 3), plus ses variables secondaires
  et un **placebo** (longueur du texte, colonne aléatoire).
- **Covariables** : log(longueur), date, langue/famille, genre.

### 6.3 La statistique

- **Spearman ρ** entre la part CLR de l'atome et la variable de niveau, avec **10 000 permutations** des
  colonnes d'atomes pour la distribution nulle.
- **Corrélation partielle** contrôlant log(longueur), date, langue/famille, genre **et les 13 autres atomes**
  (pour éviter que № ne soit qu'un proxy de ≡, ou ∃ de ⊙).
- **Correction de Benjamini-Hochberg** sur les 14 tests.
- **Split-half** : découverte sur 10 textes, confirmation sur 10 ; le signe et l'ordre des ρ doivent tenir.

### 6.4 Les contrôles négatifs

1. **Permutation des colonnes** : les 14 parts sont mélangées entre textes ; les ρ doivent tomber à ~0. Si une
   corrélation survit, elle est portée par la longueur ou par le genre, pas par l'atome.
2. **Placebo** : une variable de niveau aléatoire, ou la longueur du texte ; le ρ de l'atome avec le placebo
   doit être plus faible qu'avec sa variable principale.
3. **Corpus négatif** : on retire la marque du niveau sans toucher au texte — négations supprimées pour ∆,
   chiffres remplacés par des mots pour №, sections aplaties pour ⊞, parallélisme cassé pour ≍. Si le ρ ne
   baisse pas, la mesure ne mesure pas le niveau.
4. **Texte sans la langue** : pour les atomes lexicaux (№, ⊗), une version traduite ou un texte de genre
   différent ; le ρ doit rester stable si l'atome est structurel, chuter s'il est lexical.

### 6.5 La règle de décision

Un atome est **ancré** au niveau proposé si, et seulement si :

- ρ principal **≥ 0,30** et **p_perm < 0,05** après BH ;
- ρ principal **>** ρ de chacune des variables secondaires **et** **>** ρ du placebo ;
- le corpus négatif fait **chuter |ρ| de ≥ 50 %** ou le rend non significatif ;
- la corrélation partielle (contrôles + autres atomes) reste **du même signe** et **≥ 0,20**.

Sinon, l'atome est déclaré **non ancré** à ce niveau. Ce n'est pas un échec de la table : c'est le résultat qui
dit que la glose était trop généreuse, ou que la signature lexicale de Panini ne capte pas l'atome. Dans les deux
cas, on révise la table, pas les données.

### 6.6 Ce qui rendrait la table fausse

- Un atome dont le ρ principal est **plus faible** que celui d'un niveau secondaire ou du placebo.
- Un effet que le **corpus négatif** ne supprime pas.
- Un effet qui **disparaît** quand on contrôle la date, la langue ou la longueur.
- Un atome **colinéaire** avec un autre (№ ↔ ≡, ∃ ↔ ∆) dont la corrélation partielle s'effondre : la table
  aurait attribué à un niveau ce qui appartient à un autre atome.

### 6.7 L'avertissement de Panini, à ne pas oublier

La signature lexicale capte **l'époque** (β **+0,138**) bien plus que la **filiation** (β **+0,049**) — voir
`../docs/theorie/genealogie-des-langues.md` § 2. Toute corrélation atome ↔ niveau doit donc **contrôler la
date** ; toute similarité de surface doit être lue comme une **hypothèse**, pas comme une preuve de structure.
La table J2.1 est en amont de cette question : elle dit **où** mesurer, pas **ce que** la mesure prouvera.

## 7. Limites, nommées

1. **La table est une grille de lecture**, pas une preuve que V14 est le bon ensemble de primitives. Panini
   lui-même réserve V14 (ablation en attente, dette D2).
2. **Les niveaux sont ceux de Drave**, pas des universaux linguistiques. Le POS et le syntagme sont
   FR/EN-centrés ; les mesures sur d'autres langues doivent être stratifiées.
3. **Le morphème est omis** (8 niveaux au lieu de 9). Si on l'ajoute, ∆ et λ sont les lignes à réexaminer.
4. **La calibration est déséquilibrée** : 44 œuvres philosophiques et religieuses, pas 44 genres. Les
   corrélations y sont un mélange de genre, d'époque et de lexique.
5. **Aucune mesure atome ↔ niveau n'est encore faite.** La fiche livre la table, le protocole et la calibration,
   pas la preuve.
6. **La signature de Panini est lexicale** : elle peut ne pas capter l'atome du tout. Le contrôle négatif est
   précisément là pour le détecter ; un résultat nul est un résultat.

## 8. La suite — J2.2

1. **Construire le corpus commun** : 20 textes, mêmes identifiants, mêmes métadonnées, signatures Panini et
   annotations Drave sur le même texte.
2. **Pré-enregistrer** les 14 paires atome → variable principale de § 3, avant de regarder les corrélations.
3. **Exécuter** le protocole § 6 : CLR, permutations, partielles, BH, split-half, corpus négatif.
4. **Publier** la table mesurée : `rapport-atomes-niveaux-v2.md` + JSON, avec les atomes **ancrés**,
   **non ancrés** et **ambigus**.
5. **Réviser** la table si un atome échoue ; ne pas réviser les données pour sauver la table.

Le lien avec le reste de la semaine : cette table est le préalable de J2.2 (corpus commun), J3.1 (retrieval à
époque contrôlée) et J3.2 (généalogie à deux faces). Elle ne remplace ni le corpus ni la mesure.

## 9. Fichiers

- cette fiche : `reports/rapport-atomes-niveaux.md` ;
- les données : [`atomes-niveaux.json`](atomes-niveaux.json) — 14 atomes, 8 niveaux, la calibration des 44
  œuvres, le protocole et les contrôles ;
- les sources Panini (lecture seule) : `../../Panini/README.md`,
  `../../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md`,
  `../../Panini/research/philosophy-theory/GRILLE_ABLATION_V14_v0.1.md`,
  `../../Panini/research/nipada/falsification/analytic_sigs_v1.json` ;
- les sources Drave : `../docs/theorie/contrat-bloc-langue.md`,
  `../docs/theorie/pre-traitement-linguistique.md`, `rapport-bloc-linguistique.md` ;
- l'inventaire qui a préparé la table : [`rapport-inventaire-panini.md`](rapport-inventaire-panini.md) § 4.2 ;
- le plan de la semaine : `../docs/pilotage/semaine-autonome.md` (J2.1).

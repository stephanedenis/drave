> Campagne : **toutes-langues** · expérience **70**
> Titre : 70. OÙ ENTRE LA LANGUE : dans l'entrée du professeur, pas dans le réservoir
> Date réelle : **2026-10-06 23:50 HAE** (source : commit `97fc5ea`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 70. OÙ ENTRE LA LANGUE : dans l'entrée du professeur, pas dans le réservoir

### 70.1 La question, et pourquoi il fallait la poser avant de concevoir autre chose

Le §69 a conclu qu'il faut **une caractéristique différente**, séparable par
construction. Mais concevoir une caractéristique sans savoir **où entre la langue**
serait construire à l'aveugle. Trois candidats, et ils se départagent par une mesure :

- **l'ENTRÉE** — les plongements de couche 0, qui portent l'écriture et la morphologie ;
- **le RÉSERVOIR** — la dynamique récurrente, qui pourrait amplifier ou mêler ;
- **la LECTURE** — l'ajustement, qui choisit quelles directions servent.

On mesure `P_cont/P_lang` sur la sortie obtenue à partir de trois jeux de
caractéristiques **emboîtés**.

### 70.2 Le résultat

| caractéristiques | fid TEST | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| **A · l'ENTRÉE seule (ZÉRO neurone)** | **0,5161** | 199,5 | **338,8** | **1,698** |
| **B · les ÉTATS du réservoir** | 0,4751 | **238,8** | 323,3 | **1,354** |
| C · ENTRÉE + ÉTATS | **0,5309** | 312,4 | 499,2 | 1,598 |
| *professeur* | — | *399,2* | *4 356,4* | ***10,912*** |

### 70.3 Trois constats, et ils sont nets

**1. L'axe de langue vient de l'ENTRÉE.** L'entrée seule a un rapport de **1,698**, le
meilleur des trois. Le réservoir ne fait pas mieux : il fait **pire** (1,354). La
prédiction qui prévoyait « si A est proche de B et C, l'axe vient de l'entrée » est
confirmée, et même au-delà : **B est plus BAS que A**.

**2. Le réservoir AMPLIFIE l'axe de langue.** `P_lang` passe de **199,5** (entrée seule)
à **238,8** (réservoir) — soit **+20 %** — pendant que `P_cont` **baisse** (338,8 →
323,3). La dynamique aléatoire ne démêle pas : elle **ajoute** de la langue et
**retire** du contenu.

**3. Le réservoir COÛTE aussi en fidélité.** L'entrée seule atteint **0,5161**, le
réservoir seul **0,4751** — soit **−0,041**. C'est une troisième confirmation
indépendante du §29 (« une lecture sans aucun neurone bat le réservoir »), cette fois
avec l'explication structurelle.

**Et C (entrée + états) est le meilleur en fidélité (0,5309) mais a un rapport de 1,598,
inférieur à l'entrée seule (1,698).** Ajouter le réservoir achète donc de la fidélité en
vendant de la structure contenu/langue.

### 70.4 Le constat qui commande tout le reste

**Le professeur a un rapport de 10,912 à sa couche 8. Sa propre couche 0, lue le mieux
possible, en a 1,698.** Autrement dit :

> **La séparation contenu/langue que le professeur atteint à la couche 8 n'existe PAS
> dans sa couche 0. Elle est CRÉÉE par la transformation couche 0 → couche 8.**

Et cette transformation, le pont ne la reproduit pas. Un réservoir à poids aléatoires
gelés, aussi large soit-il, **n'est pas** cette transformation : mesuré, il fait passer
le rapport de 1,698 à 1,354 — il l'**abaisse**.

### 70.5 Ce que cela dit de l'architecture, et c'est la conclusion de la traque

La chaîne est maintenant établie de bout en bout :

| étape | ce qu'elle apporte |
|---|---|
| **l'entrée** (couche 0 du professeur) | un rapport de **1,698** — la langue y est déjà, mêlée |
| **le réservoir** (poids aléatoires gelés) | **−0,041** de fidélité, **−0,344** de rapport |
| **la lecture** (linéaire, forme fermée) | reproduit ce qu'on lui donne |
| **les post-traitements** (§58-§69) | montent le rapport à **6,96** en payant **0,12 à 0,23** de fidélité |
| **le professeur, couche 8** | rapport **10,912** |

**Le maillon manquant n'est ni la lecture ni l'objectif : c'est la TRANSFORMATION entre
l'entrée et la cible.** Le pont la remplace par une dynamique aléatoire, qui ne la
produit pas.

**Ce que la mission appelle « émuler les premières couches » est donc exactement cela** —
et c'est précisément ce que l'architecture actuelle ne fait pas. Le réservoir n'émule
pas les couches du professeur : il projette l'entrée dans un espace où la lecture doit
tout refaire, et où elle n'y arrive qu'à 64 % en sacrifiant la fidélité.

**C'est la conclusion la plus utile de toute la série**, et elle est mesurée : elle ne
dit pas « il faut un dixième objectif », elle dit **quelle transformation manque**.


---

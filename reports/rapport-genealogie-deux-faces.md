# J3.2 — La généalogie à deux faces : Panini et Glottolog sur le corpus commun

> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : semaine Panini, J3.2 · **Date** : 2026-11-07
> **Verdict** : ✅ **la confrontation est faite, et elle déplace la question.** Les deux faces ne mesurent
> **pas le même objet** : la « filiation » de Panini est une distance de **tradition** (3 paires seulement,
> sur 655, ont deux langues connues différentes), tandis que la nôtre est une distance de **famille de
> langues** (5 familles, 210 paires). Ce qui converge est réel mais **conditionnel** : la surface passe
> avant la filiation des deux côtés, et le rapport filiation/surface est du même ordre (≈ un tiers). Ce qui
> diverge est décisif : **la théorie couvre 5/21 langues** avec sa fonction `lang_distance` (200/210 paires
> codées « inconnu »), **15/21** avec ses métadonnées UDHR, **21/21** avec Glottolog ; et sur nos 21 langues,
> **les 154 paires hors script sont exactement au hasard** (MRR 0,1332 = H₃₀/30 ; top-1 0,0333 = 1/30).
> Le signal de famille ne vit que dans **56 paires de même script**, et il est porté par **2-3 paires**.
> **Dispositif** : 21 textes du corpus commun (5 familles, 10 écritures, 1948), retrieval UDHR de J3.1
> (210 paires non ordonnées), `LANG_TREE` et métadonnées UDHR de Panini (lecture seule), Glottolog
> (`data/udhr/genealogie.json`), signatures V14 de 44 œuvres, validation §150 de Panini. **Contrôles
> négatifs** : permutations de labels Panini et de chemins Glottolog (1 000), leave-one-language-out,
> décomposition de l'effet « inconnu », ACP avec permutation des colonnes et split-half.
> **JSON** : [`genealogie-deux-faces.json`](genealogie-deux-faces.json) · **Outil** :
> [`../tools/genealogie_deux_faces.py`](../tools/genealogie_deux_faces.py).
> **Ce qui pourrait le rendre faux** : le retrieval est **de surface** ; le corpus est **mono-époque** et
> **mono-genre** ; les paires ne sont pas indépendantes ; la distance Glottolog est une distance de chemin
> à arêtes uniformes ; l'ACP des atomes porte sur 44 œuvres, pas sur les 21 langues. Voir § 7.

## 1. La question, et ce que « deux faces » veut dire

J3.2 demande de confronter la **théorie de Panini** (14 atomes, 9 dhātus, une échelle de distance) à nos
**mesures d'alignement** (Glottolog + retrieval) sur le **corpus commun** — les 21 textes de l'article 1
de la DUDH construits en J2.2.

Les deux faces ne sont pas deux instruments du même objet :

| face | ce qu'elle est | ce qu'elle mesure | unité |
|---|---|---|---|
| **Panini — atomes** | 14 primitives sémantiques (∃ ∆ ∼ …) projetées sur un texte | une **signature lexicale** de 14 parts | le texte / l'œuvre |
| **Panini — dhātus** | 9 opérateurs cognitifs, déclarés **macros** de V14 | des motifs de contraintes, pas des axes indépendants | le token / le graphe |
| **Panini — généalogie** | `LANG_TREE` (29 langues) + une échelle à 4 niveaux | une **distance de tradition** codée à la main | la langue / la tradition |
| **Drave — Glottolog** | un arbre de 441 langues, chemins de glottocodes | une **classification** hiérarchique | la langue |
| **Drave — retrieval** | n-grammes de caractères, TF-IDF, cosinus | la **surface partagée** entre deux textes | la paire de textes |

La question de J3.2 n'est donc pas « qui a raison ? » mais : **qu'est-ce qui est commensurable, sur quel
corpus, et à quel prix ?** La réponse courte est que le corpus commun permet la confrontation **langue ↔
langue** (Panini UDHR vs Glottolog), mais **pas** la confrontation **atome ↔ langue** : Panini n'a pas
projeté ses 14 atomes sur les 21 langues.

## 2. Le matériau — trois généalogies, trois couvertures

### 2.1 Les trois représentations et leur couverture

| représentation | source | langues | couverture des 21 | paires à « inconnu » |
|---|---|---:|---:|---:|
| **P1 — `lang_distance` (LANG_TREE)** | `language_genealogy.py`, 29 langues | 29 | **5/21** (eng, fra, ell, hin, heb) | **200/210** |
| **P2 — métadonnées UDHR** | `udhr_corpus.json`, 532 langues | 111 avec famille connue (421 `Other`) | **15/21** | **105/210** |
| **G — Glottolog** | `data/udhr/genealogie.json`, 441 langues | 441 | **21/21** | 0 |

Les **6 langues sans label Panini** sont `ewe`, `fuf`, `mly`, `cnh`, `ctd`, `arb` : **toutes non
indo-européennes**. Les **16 langues sans `LANG_TREE`** incluent les 4 paires de même branche que Panini
lui-même reconnaît dans ses métadonnées UDHR (`ind`/`tgl`/`jav` : Malayo-Polynesian ; `amh`/`heb` :
Semitic). Autrement dit, **la fonction de distance de Panini ne voit pas ses propres paires les plus
proches** : elle les code `1,0` (« inconnu »).

### 2.2 L'accord des deux faces, là où elles se rencontrent

Sur les **15 langues** que Panini labelise dans ses métadonnées UDHR :

| comparaison | accord | détail |
|---|---:|---|
| **famille, brut** | **13/15** (86,7 %) | `kin`, `ibo` : Panini dit « Niger-Congo », Glottolog « Atlantic-Congo » — nomenclature, pas désaccord substantiel |
| **famille, apparié** | **15/15** (100 %) | en traitant Niger-Congo comme la famille large d'Atlantic-Congo |
| **branche, nœud exact** | **14/15** (93,3 %) | `mya` : « Tibeto-Burman » n'a pas de nœud exact dans le chemin Glottolog (`tibe1272` absent) ; `burm1265` est le descendant le plus proche |
| **branche, nœud proche** | **15/15** (100 %) | avec l'allowance ci-dessus |

Sur les **105 paires** de ces 15 langues, les deux distances sont fortement liées : **Spearman ρ = 0,657**
(p = 2,8 × 10⁻¹⁴), **Pearson r = 0,918** (p = 3,3 × 10⁻⁴³). Sur les **10 paires** des 5 langues de
`LANG_TREE`, P1 et P2 donnent des **valeurs identiques** (6 × 0,40, 4 × 0,75). L'accord est donc excellent
**là où les deux faces existent** — le problème n'est pas la forme de l'arbre, c'est sa **couverture** et sa
**granularité**.

### 2.3 L'échelle à quatre niveaux n'est pas une distance

L'échelle de Panini a cinq valeurs (0 ; 0,15 ; 0,40 ; 0,75 ; 1,0). Sur les 21 langues :

| niveau | P1 (LANG_TREE) | P2 (UDHR) | ce que le niveau contient |
|---:|---:|---:|---|
| 0,15 | **0 paire** | 4 paires | P2 : 3 paires austronésiennes + 1 paire sémitique |
| 0,40 | 6 paires | 14 paires | P2 : **une seule** paire au-dessus du hasard sur 14 (`eng–fra`, MRR 0,952) ; 5 paires P1 à 0,133 sauf `eng–fra` |
| 0,75 | 4 paires | 87 paires | P1 : `heb` contre les 4 IE, **toutes au plancher** (0,133) |
| 1,0 | 200 paires | 105 paires | « inconnu » : ce n'est pas une distance, c'est une valeur manquante |

Deux conséquences :

1. **Le niveau 0,40 n'est pas homogène** : il mélange `eng–fra` (MRR 0,952) et cinq paires au plancher
   (0,133). Une même valeur de distance recouvre des réalités opposées ; la régression linéaire sur cette
   échelle est un **résumé**, pas une mesure.
2. **Le niveau 1,0 n'est pas un niveau** : c'est le code de l'absence. Il n'est pas *missing at random* :
   les 6 langues non labellisées sont toutes non-IE, et les paires inconnues ont un MRR plus bas
   (0,140 contre 0,162). Le coder comme « distance maximale » fabrique un effet de couverture.

## 3. L'alignement — le script est une porte, la famille vit dans les paires de même script

### 3.1 La porte du script : 154/154 paires hors script au hasard exact

Le retrieval de J3.1 sur l'UDHR (21 langues, 30 articles) donne 210 paires non ordonnées (moyenne des deux
sens). Le hasard est **MRR 0,13317** (H₃₀/30) et **top-1 1/30 = 0,03333**.

| groupe | n | MRR moyen | top-1 moyen | lecture |
|---|---:|---:|---:|---|
| **toutes** | 210 | **0,1510** | 0,0494 | — |
| **même script** | 56 | **0,1999** | 0,0938 | le seul endroit où il y a un signal |
| **script différent** | **154** | **0,1332** | **0,0333** | **exactement le hasard** |

Les **154 paires hors script** ont **toutes** la même valeur : MRR 0,13316624, top-1 0,033333. Ce n'est pas
« en moyenne au hasard » : c'est **le hasard exact, sans variance**. Le retrieval de surface ne traverse
**aucune** frontière d'écriture. C'est le résultat le plus net de J3.2, et il est un **contrôle négatif
intégré** : la partie du corpus où l'on ne peut rien apprendre est exactement celle où le score est nul.

### 3.2 Ce qui reste dans le même script : 56 paires, 8 de même famille

| cellule | n | MRR moyen | médiane | au-dessus du hasard | moyenne au-dessus |
|---|---:|---:|---:|---:|---:|
| même famille + même script | **8** | **0,3853** | 0,2004 | **7/8** (87,5 %) | 0,4216 |
| même famille + script différent | 26 | 0,1332 | 0,1332 | 0/26 | — |
| famille différente + même script | **48** | **0,1691** | 0,1483 | 37/48 (77,1 %) | 0,1827 |
| famille différente + script différent | 128 | 0,1332 | 0,1332 | 0/128 | — |

Les **8 paires même famille + même script** :

| paire | MRR | top-1 | distance P2 | branche Panini |
|---|---:|---:|---:|---|
| `eng–fra` | **0,9515** | 0,9333 | 0,40 | Germanic / Romance |
| `kin–ewe` | 0,1585 | 0,0500 | 1,00 (inconnu) | Bantu / Unknown |
| `kin–ibo` | 0,1311 | 0,0167 | 0,40 | Bantu / Volta-Niger |
| `ewe–ibo` | 0,1932 | 0,1000 | 1,00 (inconnu) | Unknown / Volta-Niger |
| `ind–tgl` | 0,2077 | 0,1167 | 0,15 | Malayo-Polynesian |
| `ind–jav` | **0,9178** | 0,8667 | 0,15 | Malayo-Polynesian |
| `tgl–jav` | 0,1771 | 0,0500 | 0,15 | Malayo-Polynesian |
| `cnh–ctd` | 0,3456 | 0,2000 | 1,00 (inconnu) | Unknown / Unknown |

Deux lectures, et il faut les tenir ensemble :

- **le signal est réel** : 7/8 paires de même famille + même script sont au-dessus du hasard, contre 37/48
  (77,1 %) pour les paires de familles différentes ; la moyenne au-dessus du hasard est 0,422 contre 0,183.
- **le signal est fragile** : deux paires (`eng–fra` 0,952, `ind–jav` 0,918) portent la moyenne ; les six
  autres vont de 0,131 à 0,346. Le **leave-one-language-out** du coefficient de distance va de **−0,296 à
  −0,103** (médiane −0,212) : retirer `ind` le rend plus négatif, retirer `tgl` le rend moins négatif
  (tableau § 3.3). Ce n'est pas une pente de famille, c'est **un effet de quelques paires**.

### 3.3 Les régressions : le script d'abord, la distance ensuite

`MRR ~ script_match + distance`, sur 210 paires (toutes) et 105 paires (labelisées P2) :

| modèle | n | R² | coef. script | coef. distance | p distance (OLS) |
|---|---:|---:|---:|---:|---:|
| script seul | 210 | 0,1228 | +0,0668 | — | — |
| script + P1 | 210 | 0,1821 | +0,0698 | −0,1961 | 1,4 × 10⁻⁴ |
| script + P2 | 210 | 0,1980 | +0,0652 | −0,1184 | 1,7 × 10⁻⁵ |
| script + G | 210 | 0,1638 | +0,0651 | −0,1161 | 1,7 × 10⁻³ |
| script seul | 105 | 0,1713 | +0,1077 | — | — |
| script + P1 | 105 | 0,2310 | +0,1137 | −0,1948 | 5,9 × 10⁻³ |
| **script + P2** | 105 | **0,2564** | +0,1020 | **−0,2120** | **9,2 × 10⁻⁴** |
| **script + G** | 105 | **0,2297** | +0,1005 | **−0,2259** | **6,5 × 10⁻³** |

Les tests d'inférence sont les **permutations de labels** (1 000) :

| représentation | p (210 paires) | p (105 paires) |
|---|---:|---:|
| P1 — LANG_TREE | 0,020 | 0,045 |
| **P2 — UDHR** | **0,003** | **0,006** |
| **G — Glottolog** | 0,017 | 0,019 |

Sur les 105 paires couvertes, **les deux faces prédisent le retrieval aussi bien l'une que l'autre** :
R² 0,256 (P2) contre 0,230 (G), et les intervalles du leave-one-language-out se recouvrent (P2 : R²
0,165–0,317 ; G : 0,154–0,301). La différence de 0,027 est **petite mais stable** : l'écart de R² reste positif dans les 21 retraits
(0,007–0,055). **Ce n'est pas Glottolog qui gagne, ni Panini : c'est la même information, à deux
granularités.**

### 3.4 Le piège de la couverture : « inconnu = 1,0 » n'est pas une distance

Sur les 210 paires, P2 a un R² de 0,198 et G de 0,164. P2 « gagne » — mais une partie de ce gain est le
codage des 105 paires inconnues à 1,0. Si on sépare la distance (estimée sur les paires couvertes) d'un
**indicateur d'inconnu** :

| modèle | coef. distance | coef. inconnu | R² |
|---|---:|---:|---:|
| script + P2 (distance sur couvertes) + inconnu | **−0,2200** | **−0,1716** | 0,2253 |
| script + G (distance sur couvertes) + inconnu | **−0,2413** | **−0,2899** | 0,2021 |

Le coefficient de distance reste **stable** (−0,22 / −0,24) et l'indicateur d'inconnu porte un effet
négatif fort. Le R² « toutes » de 0,198 n'est donc **pas** une supériorité généalogique de Panini : c'est
un **effet de couverture**. C'est la raison pour laquelle la comparaison honnête est celle des 105 paires
couvertes, où les deux faces sont à égalité.

### 3.5 Contrôles négatifs de l'alignement

1. **Hors script** : 154/154 paires au hasard exact (MRR 0,1332, top-1 0,0333) — le contrôle est **déjà
   dans les données**, et il passe.
2. **Permutation des labels Panini** : le coefficient observé (−0,212 sur 105 paires) sort de la
   distribution nulle (p = 0,006 ; nul moyen −0,003 ; IC 2,5–97,5 % [−0,147 ; +0,087]).
3. **Permutation des chemins Glottolog** : coefficient observé −0,226, p = 0,019 (nul moyen −0,003 ;
   IC [−0,209 ; +0,107]).
4. **Leave-one-language-out** : le coefficient reste négatif dans les 21 retraits, mais varie de −0,296 à
   −0,103 (P2) et de −0,294 à −0,100 (G) : la **direction** est robuste, la **taille** ne l'est pas.
5. **Décomposition de l'inconnu** : voir § 3.4 — le gain apparent de P2 sur toutes les paires disparaît
   quand on sépare la couverture de la distance.

## 4. La face « atomes » — 14 atomes, 9 dhātus, et pourquoi ce n'est pas une généalogie

### 4.1 Ce que les signatures V14 disent d'elles-mêmes

Sur les **44 œuvres** de `analytic_sigs_v1.json` (14 parts normalisées, somme 1), l'ACP sur la **matrice
de corrélation des parts CLR** (la convention de J2.1) donne :

| composante | valeur propre | variance | cumul |
|---:|---:|---:|---:|
| 1 | 6,967 | 49,76 % | 49,76 % |
| 2 | 2,845 | 20,32 % | 70,08 % |
| 3 | 1,491 | 10,65 % | **80,73 %** |
| 4 | 1,260 | 9,00 % | 89,73 % |
| 5 | 0,528 | 3,77 % | 93,51 % |
| 6 | 0,381 | 2,72 % | 96,23 % |

**4 composantes > 1** ; **3 composantes pour 80 %** ; **5 pour 90 %** ; **6 pour 95 %**. Sur la
**covariance** des parts CLR (sans standardiser), il n'y a plus qu'**une** composante > 1 (52,63 % de la
variance). Le « 4 dimensions effectives » dépend donc d'un choix : **standardiser donne le même poids aux
atomes rares** (≍, ↗), ce qui augmente artificiellement le rang. Les deux lectures sont dans le JSON.

**Contrôle par permutation des colonnes** (1 000) : le nombre observé de valeurs propres > 1 est **4**,
la nullité en donne **6,25 en moyenne** (p = 0,001). Autrement dit, les 14 atomes sont **plus colinéaires
que des colonnes indépendantes** — c'est le sens du résultat : ils ne portent pas 14 dimensions.
La variance des 3 premières est **0,807** contre **0,393** sous permutation (p = 0,001).

**Stabilité split-half** (1 000 coupures 22/22) : le premier axe est stable **en moyenne** (cos **0,930**),
mais son IC descend à **0,298** — il existe des coupures où il ne l'est pas. Le sous-espace à 3 dimensions
ne l'est que partiellement (recouvrement moyen **0,612**, IC [0,484 ; 0,716]). Le premier axe est un fait
robuste en moyenne ; les axes 2–4 sont des directions **instables**.

### 4.2 Les 9 dhātus ne sont pas mesurables en l'état

Panini donne **deux listes** de 9 dhātus :

- **sanskrit** : BHŪ, KR, STHĀ, DĀ, JÑĀ, BUDH, MAN, VAC, DṚŚ ;
- **computationnels** : EXIST, TRANS, EVAL, LOCATE, FEEL, ACT, QUAL, REL, KNOW.

La théorie dit qu'ils sont des **macros** (des motifs nommés dans l'espace V14), **pas un second jeu
d'atomes**. Il n'existe **aucune matrice publiée** dhātu → V14 dans les sources lues. Sans elle :

- on ne peut pas projeter les signatures de 44 œuvres sur les 9 dhātus ;
- on ne peut pas tester si 9 dhātus expliquent mieux que 14 atomes ;
- le **nombre 9** est **architectural**, pas mesuré. Les données donnent 4 dimensions effectives
  (corrélation) ou 1 (covariance) ; 9 est **sur-complet** par rapport à ce que les signatures portent, mais
  ce n'est pas une réfutation : des macros peuvent se recouvrir.

C'est un **point de mesure manquant**, pas un échec de la théorie.

### 4.3 Pourquoi la face atomes n'est pas la face langue

Les 14 atomes sont une **signature de texte** : ils décrivent ce qu'un texte dit, pas la proximité
historique de deux langues. Panini l'a mesuré lui-même : dans `nipada_v150_validation.json`, le coefficient
de « filiation » (`d_graph`) vaut **+0,0489** contre **+0,1378** pour l'époque (R² = 0,3004), et leurs
hypothèses H1 (stratification) et H2 (LOOCV tradition) sont **KO** ; le go/no-go de la phase religieuse est
**NO-GO**. Leur conclusion — « la signature de surface capte l'époque, pas la filiation » — est un constat
sur **la signature de texte**, pas sur la généalogie des langues.

Et leur corpus ne permet pas de tester la filiation des langues : sur les **655 paires** de
`paires334_axes_v1.json`, **173** sont `eng–eng`, **479** ont au moins une langue vide, et **3 seulement**
ont deux langues connues différentes. Le `d_graph` est une distance de **tradition** (brahmanisme,
grecque, chinoise…), pas une distance de famille. **Le mot « filiation » ne désigne pas le même objet des
deux côtés.**

Enfin, sur le corpus commun, la face atomes est **quasi absente** :

| source Panini | langues | dont les 21 | couverture |
|---|---:|---:|---:|
| `udhr_decomposed_v14.json` | 11 | eng, fra, ind | **3/21** |
| `udhr_convergence_v14.json` | 4 | eng | **1/21** |

On ne peut donc pas, avec les données présentes, confronter les 14 atomes aux 21 langues. C'est **la**
mesure qui manque.

## 5. Ce qui converge

1. **La surface passe avant la filiation, des deux côtés.** Panini : β époque 0,1378 > β filiation 0,0489.
   Drave : le script est une porte (154/154 paires hors script au hasard), la famille ne vit que dans les
   paires de même script.
2. **Le rapport filiation/surface est du même ordre : environ un tiers.** Panini : 0,0489/0,1378 = **0,355**.
   J3.1 (Bible) : famille 0,181 / script 0,609 = **0,297**. Ce n'est pas une preuve, mais c'est une
   **convergence de forme** entre deux instruments et deux corpus différents.
3. **Un signal de filiation résiduel est détectable quand la surface est contrôlée.** Panini : β filiation
   0,0489 (H3 OK). Drave : coefficient de distance −0,212 sur les 105 paires couvertes, p = 0,006 par
   permutation des labels. Les deux faces disent : *il reste quelque chose, mais ce n'est pas le premier
   terme.*
4. **Les deux généalogies sont le même arbre là où elles se rencontrent.** 15/15 familles (appariées),
   14/15 branches au nœud exact (15/15 avec l'allowance Tibeto-Burman), Spearman 0,657 et Pearson 0,918
   sur les 105 paires.
5. **Les deux généalogies prédisent le retrieval de façon comparable.** R² 0,256 (P2) contre 0,230 (G)
   sur les 105 paires ; l'écart est petit mais stable (positif dans les 21 retraits). La différence de
   granularité ne se paie pas sur ce corpus.

## 6. Ce qui diverge

1. **L'objet de la « filiation ».** Panini mesure une distance de **tradition** (3/655 paires
   inter-langues, 479 avec une langue vide) ; Drave mesure une distance de **famille de langues** (5
   familles, 210 paires). La convergence du § 5 est une convergence de **forme**, pas d'unité.
2. **La couverture.** P1 : 5/21 langues, 200/210 paires à 1,0. P2 : 15/21, 105/210 à 1,0. G : 21/21, 0.
   Les 6 langues non labellisées par Panini sont **toutes non-IE** ; **3 des 4 paires de même branche** sont
   entièrement hors de `LANG_TREE`, et la quatrième (`amh–heb`) a `amh` hors arbre. La théorie est aveugle
   à ses propres meilleures paires.
3. **La granularité.** L'échelle à 4 niveaux n'utilise jamais 0,15 dans `LANG_TREE` sur les 21 langues ;
   son niveau 0,40 mélange `eng–fra` (0,952) et cinq paires au plancher ; son niveau 1,0 est une valeur
   manquante. Ce n'est pas une distance métrique : c'est une **échelle ordinale grossière**.
4. **Le confondant dominant.** Panini dit **époque** ; Drave dit **écriture**. Le corpus commun est
   mono-époque (1948) : il ne peut pas tester l'époque. J3.1, à écriture contrôlée, trouve −0,034/siècle
   (p = 0,19). Le script, lui, est une **porte exacte**. Les deux faces sont d'accord sur « la surface
   d'abord », pas sur **quelle** surface.
5. **La fragilité du signal de famille.** 7/8 paires même famille + même script au-dessus du hasard, mais
   deux paires portent la moyenne ; le coefficient de distance varie de −0,296 à −0,103 au leave-one-out.
   Le corpus ne permet pas d'estimer une **pente** de famille : il permet de dire que **quelques paires**
   de même famille se ressemblent plus que le hasard.
6. **La face atomes n'est pas une généalogie.** 4 dimensions effectives (corrélation) ou 1 (covariance) ;
   9 dhātus macros sans matrice V14 ; V14 couvre 3/21 langues. La théorie des atomes est une théorie du
   **texte**, pas un arbre de langues.
7. **Le code « inconnu = 1,0 ».** Ce n'est pas une valeur manquante neutre : les paires inconnues sont
   plus basses (0,140 contre 0,162), et le gain apparent de P2 sur toutes les paires disparaît quand on
   sépare l'indicateur d'inconnu. Une valeur manquante codée comme distance maximale **fabrique** un effet.

## 7. Ce qui reste à mesurer

| # | mesure | pourquoi elle manque | dispositif | contrôle |
|---:|---|---|---|---|
| 1 | **Signature V14 des 21 langues** | la face atomes n'existe que pour 3/21 langues | projection multilingue (wordnets/embeddings alignés) des 14 atomes sur les 21 textes, puis test : invariance entre traductions (universalité) ou cluster par famille (filiation) | même texte, deux langues de même famille vs deux familles ; l'invariance doit être plus forte dans le premier cas |
| 2 | **Matrice 9 dhātus → 14 atomes** | les 9 dhātus sont des macros, aucune matrice publiée ; deux nomenclatures | publier la décomposition de chaque dhātu en V14, projeter les 44 œuvres, comparer la variance expliquée | permutation des colonnes de la matrice |
| 3 | **Distance Panini continue, étendue aux 21** | LANG_TREE couvre 5/21 ; 200/210 paires « inconnues » | étendre LANG_TREE ou apprendre une distance continue sur Glottolog, refaire la régression sur 210 paires | comparer à la distance discrète : si le R² ne bouge pas, le gain est nul |
| 4 | **Corpus équilibré même script / familles différentes** | 56 paires de même script, 8 de même famille + même script, 2-3 paires porteuses | 6 familles × 6 langues de même écriture, plusieurs branches par famille | leave-one-out : le coefficient doit rester stable quand on retire une langue et les 2 paires extrêmes |
| 5 | **Retrieval neuronal** | le retrieval est de surface ; la porte du script peut être un artefact de n-grammes | refaire l'UDHR avec les états cachés d'un modèle multilingue, script contrôlé | mêmes paires, même découpage ; si le modèle traverse le script, la conclusion change |
| 6 | **Corpus multi-époques** | le corpus commun est mono-époque (1948) | Bible ou corpus daté dans un sous-ensemble des 21 langues, plusieurs traductions par langue | permutation des années |
| 7 | **Poids des arêtes Glottolog** | la distance de chemin traite toutes les arêtes comme égales ; l'arbre est très déséquilibré | calibrer les longueurs de branches (temps de séparation, distance lexicale) | comparer aux arêtes uniformes |

## 8. Limites, et ce qui pourrait rendre le résultat faux

1. **Retrieval de surface.** Les n-grammes de caractères capturent l'orthographe et les cognates, pas le
   sens. La porte du script peut être une propriété de l'instrument ; un retrieval neuronal pourrait la
   franchir. **C'est la limite principale.**
2. **Corpus mono-époque, mono-genre.** 21 langues, 5 familles, 10 écritures, 1948, déclaration. Il ne
   permet ni le contrôle de l'époque ni une estimation de famille stable.
3. **Paires non indépendantes.** Chaque langue apparaît dans 20 paires ; les p-values OLS sont
   descriptives. Les tests d'inférence sont les permutations de labels et le leave-one-out, pas les
   p-values OLS.
4. **Distance Glottolog conventionnelle.** Chemin à arêtes uniformes, normalisé par |a|+|b|−2. Un autre
   choix (hauteur du LCA, longueurs de branches) changerait les valeurs.
5. **Deux Panini.** Les métadonnées UDHR (111/532 langues) et `LANG_TREE` (29 langues) sont deux
   représentations différentes ; leur accord n'est vérifié que sur 5 langues.
6. **ACP sur 44 œuvres.** Les 4 dimensions effectives sont une propriété de la **signature de Panini** sur
   un corpus philosophique et religieux, pas du corpus commun. Le résultat ne dit rien des 21 langues.
7. **Effet de famille moyen sur des paires hétérogènes.** Le coefficient ne dit pas quelles langues sont
   proches ; il est porté par 2-3 paires. Une conclusion « la famille explique X % » serait abusive.
8. **Le corpus commun n'est pas un échantillon.** 21 textes sur 418 paires exactes, 5 familles sur 51,
   10 écritures. Toute généralisation à « les langues » est hors de portée.

## 9. Fichiers et reproduction

| fichier | rôle |
|---|---|
| [`../tools/genealogie_deux_faces.py`](../tools/genealogie_deux_faces.py) | le dispositif complet (couverture, accord, alignement, atomes, contrôles) |
| [`genealogie-deux-faces.json`](genealogie-deux-faces.json) | tous les chiffres : 210 paires, groupes, régressions, permutations, LOO, ACP, §150 |
| [`rapport-corpus-commun.md`](rapport-corpus-commun.md) | les 21 textes et leur construction (J2.2) |
| [`rapport-retrieval-epoque.md`](rapport-retrieval-epoque.md) | le retrieval UDHR/B7/Bible (J3.1) |
| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | la table 14 atomes × 8 niveaux (J2.1) |
| [`../docs/theorie/genealogie-des-langues.md`](../docs/theorie/genealogie-des-langues.md) | la théorie mise à jour (sans les chiffres) |

Reproduction :

```bash
python3 tools/genealogie_deux_faces.py
```

Le script lit `reports/corpus-commun.json`, `reports/retrieval-epoque.json`, `../Panini/research/` (lecture
seule) et `data/udhr/genealogie.json`. Il écrit `reports/genealogie-deux-faces.json`. Les 1 000
permutations et les 1 000 split-half sont fixés par `--graine 0` ; `--permutations` permet de les
augmenter.

## 10. Verdict

- **J3.2 est mesuré, écrit, contrôlé.** La confrontation est **possible** sur la généalogie
  langue ↔ langue (P2 vs Glottolog) et **impossible** sur les atomes (V14 couvre 3/21 langues).
- **Ce qui converge** : la surface d'abord, la filiation ensuite, un rapport d'environ un tiers, et deux
  généalogies qui sont le même arbre là où elles se rencontrent.
- **Ce qui diverge** : l'objet (tradition vs famille), la couverture (5/21, 15/21, 21/21), la granularité
  (4 niveaux, pas une distance), le confondant dominant (époque vs script), et la fragilité (2-3 paires).
- **Ce qui reste** : une signature V14 multilingue sur les 21 langues, une matrice 9 dhātus → V14, une
  distance continue, un corpus équilibré, un retrieval neuronal, un corpus multi-époques. **La prochaine
  mesure est la signature V14 des 21 langues** : c'est elle qui rendrait la face atomes commensurable avec
  la face langue.

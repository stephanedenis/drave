# B2 — Les 14 atomes prédisent-ils les niveaux de Drave ? Le style de surface, oui ; POS, syntagmes et attachement, non

> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, B2 · **Date** : 2026-11-15
> **Verdict** : ❌ **non, pas de façon robuste** — sur les **28 œuvres propres** (parmi 44 signatures), les
> 14 atomes ne prédisent pas les trois niveaux du mandat : POS **R²_CV = −0,092** (p_col = 0,56),
> syntagmes **−0,160** (p = 0,85), attachement **−0,092** (p = 0,67). Le seul signal nominal (POS,
> **ρ = +0,176**, p = 0,029, **Holm 0,088**) ne survit pas au contrôle de date (**p_resid = 1,0**).
> Sur les **36 mesurables**, le POS brut est prédit (**R² = +0,102**, p = 0,004 ; ρ = +0,280) et les
> syntagmes (**+0,060**, p = 0,006), mais le signal tombe à **+0,010 / +0,014** sur les **34 sources
> propres**, à **−0,080 / −0,204** sur les **26 œuvres ≥ 2 000 mots**, et le contrôle de date le retire
> (**p_resid = 0,77 / 0,14**). Le dispositif n'est pas muet : il prédit l'**entropie des graphèmes**
> (**+0,811**, p = 0,0005), la **longueur des mots** (**+0,657**), la **négation** (**+0,440**) et la
> **part de verbes** (**+0,429**) ; mais la date explique **0,16–0,54** de ces métriques et **aucune** ne
> survit au contrôle de date (**p_resid = 0,76–1,0**). Les atomes captent un **gradient de style/époque**,
> pas la syntaxe de surface des niveaux.
>
> **Dispositif** : 44 signatures V14 de Panini (`analytic_sigs_v1.json`, 14 parts, somme 1, calculées sur
> les **10 000 premiers jetons**), lues en **lecture seule** ; dates, traditions et langues du graphe
> `nipada_v334_graph_v35.json` ; niveaux mesurés par le **bloc linguistique heuristique** de Drave
> (`tools/bloc_linguistique.py`) sur des échantillons de prose (6 × 10 000 caractères, ou le texte entier
> s'il est plus court) ; régression **ridge multi-sorties** en **LOOCV groupée** (les doublons de texte
> restent dans le même pli) ; **permutation indépendante des 14 colonnes** (2 000 tirages) ; **contrôle de
> date** (année de composition, régression in-sample, 1 000 permutations, résidus). **Contrôle négatif** :
> colonnes permutées → la prédiction doit tomber au hasard ; **contrôle de date** : les atomes doivent
> prédire ce que la date ne dit pas.
>
> **JSON** : [`atomes-prediction.json`](atomes-prediction.json) · **Mesures** :
> [`atomes-prediction-mesures.json`](atomes-prediction-mesures.json) · **Outil** :
> [`../tools/atomes_prediction.py`](../tools/atomes_prediction.py).
>
> **Ce qui pourrait le rendre faux** : les niveaux sont des **annotations heuristiques de surface**, pas
> un gold ; la signature V14 est calculée sur les **10 000 premiers jetons bruts**, parfois une page de
> navigation ou une table des matières ; la date est celle de la **composition**, pas de la traduction
> anglaise ; **26 textes uniques** seulement (17 GRECO, deux paires de doublons), et la CV ne groupe que
> les doublons exacts, pas l'auteur ni la tradition ; la moyenne de famille est un **indice**, pas un R²
> multivarié ; le niveau **document** n'est pas mesurable (sources sur une ligne). Voir § 6.

## 1. La question

La table `rapport-atomes-niveaux.md` (J2.1) a proposé, pour chacun des **14 atomes V14** de Panini, un
**ancrage** et un **porteur** parmi les **8 niveaux** de Drave. C'était une **hypothèse de lecture** et un
**protocole**, pas une mesure : aucune correspondance atome ↔ niveau n'avait été testée. B2 pose la
question inverse, et la seule qui compte pour un moteur : **les 14 parts d'atomes d'une œuvre
prédisent-elles les statistiques de ses niveaux ?**

Trois niveaux sont au mandat : **POS**, **syntagmes**, **attachement**. Les cinq autres — graphème, mot,
phrase, pragmatique, discours — sont mesurés en secondaire ; le niveau **document** ne l'est pas (les 44
sources sont sur **une seule ligne**, sans paragraphes). La question se double de deux contrôles :

1. **permutation des colonnes** — si l'on permute indépendamment chaque colonne d'atomes entre les
   œuvres, la prédiction doit tomber au hasard. C'est le contrôle négatif du mandat ;
2. **contrôle de date** — Panini avertit que la surface capte **l'époque** (β +0,138) bien plus que la
   filiation (β +0,049). Si les atomes ne prédisent les niveaux que parce qu'ils datent les œuvres, la
   prédiction n'a pas de valeur syntaxique.

La réponse courte : **le dispositif est sensible au style de surface, mais il ne trouve rien de robuste
pour POS, syntagmes et attachement ; ce qu'il trouve est absorbé par la date.**

## 2. Les données et leur qualité

### 2.1 Les 44 signatures

`../../Panini/research/nipada/falsification/analytic_sigs_v1.json` contient **44 œuvres × 14 parts**
(somme 1). Le script `../../Panini/research/scripts/loi_analytique.py` montre que chaque signature est
calculée sur les **10 000 premiers jetons** du fichier source, **avant** nettoyage. C'est un point
important : les fichiers sont des acquisitions web, pas des éditions normalisées. Nous les lisons en
**lecture seule** et nous auditons la fenêtre de signature (part de mots vides, de balises, de lettres)
avant de décider ce qui est mesurable.

### 2.2 La cascade de qualité

| cohorte | n | définition | usage |
|---|---:|---|---|
| **signatures** | 44 | toutes les œuvres du JSON de Panini | source |
| **mesurables** | 36 | ≥ 200 mots de prose après nettoyage | mandat |
| **propres** | 34 | fenêtre de signature de prose (mots vides ≥ 0,15, balises ≤ 0,05, lettres ≥ 0,75) | contrôle |
| **utilisables** | 28 | propres **et** ≥ 1 000 jetons de signature | **primaire** |
| **strictes** | 26 | utilisables **et** ≥ 2 000 mots mesurés | contrôle |

**8 œuvres ne sont pas mesurables** : `bengio_2003` (PDF illisible par `pdftotext`, 0 mot),
`aristotle_prior_analytics` (57 mots de prose), `mn35_culasaccaka` (37), `hosea_book` (106),
`zechariah_book` (106), `daniel_book` (105), `ezekiel_book` (174), `jeremiah_book` (182). Ce sont des
pages de navigation, des tables des matières ou un PDF corrompu : il n'y a pas assez de prose pour
mesurer un niveau.

**2 œuvres sont mesurables mais leur signature n'est pas de la prose** : `2_esdras` (769 mots de prose,
mais la fenêtre de signature est à **35,6 %** de balises/JS) et `isaiah_book` (210 mots, signature à
**1,2 %** de mots vides : une table des matières). Elles restent dans la cohorte « mesurable » (36),
mais pas dans « propre » (34).

**6 œuvres propres sont trop courtes** pour une signature stable (< 1 000 jetons) :
`aristotle_posterior_analytics` (941), `book_of_enoch` (827), `lukasiewicz_1920` (451), `mengzi` (304),
`mikolov_2013` (600), `qiwulun` (788). Elles passent de 34 à 28.

La **cohorte primaire** est donc **28 œuvres**, dont **26 textes uniques** (deux paires de doublons
exacts : `plato_gorgias` / `plato_gorgias_jowett`, `plato_meno` / `plato_meno_jowett`). Les doublons
restent dans le **même pli** de validation croisée. Les dates vont de **−440** à **1972**, médiane
**−355** ; **17/28** sont GRECO, **20/28** antérieures à 1000. Ce n'est pas un échantillon de 28
observations indépendantes : c'est un corpus de philosophie et de religion, très majoritairement grec.

### 2.3 Les dates et les atomes

Le graphe v35 fournit l'année de **composition** (ou son estimation). Sur les 28 œuvres propres, cinq
atomes sont corrélés à la date (tableau complet au § 4.4) : `STRUCTURE` **+0,760**, `ÊTRE` **−0,596**,
`RAPPORT` **+0,541**, `DIFFÉRENCE` **−0,536**, `FONCTION` **+0,448**. La signature V14 est donc aussi une
**signature d'époque** : c'est le confondant que le contrôle de date doit retirer.

## 3. Le dispositif

### 3.1 Les métriques de niveau

Le bloc linguistique heuristique de Drave (`Heuristique.analyser`) étiquette les neuf niveaux. Nous
agrégeons ses sorties en familles :

| famille | métriques | ce que la famille mesure |
|---|---|---|
| **POS** | `pos_entropie`, parts NOUN, VERB+AUX, ADJ, ADV, PRON, DET, PREP, CONJ, NUM, PONCT | la composition des classes de mots |
| **SYNTAGMES** | `syn_par_phrase`, `syn_longueur`, parts GN, GV, GP, REL, SUB, `syn_profondeur` | la segmentation en groupes |
| **ATTACHEMENT** | `att_taux`, `att_distance`, `att_distance_mediane`, `att_part_gp` | la relation segment → cible |
| graphème | `graph_lettres`, `graph_ponctuation`, `graph_entropie` | la surface des caractères |
| mot | `mot_longueur`, `mot_ttr`, `mot_hapax` | le lexique de surface |
| phrase | `phrase_longueur`, `phrase_negation`, `phrase_modalite`, `phrase_interrogative` | la phrase |
| pragmatique | `pragma_assertion`, `pragma_entropie` | les actes de parole |
| discours | `disc_connecteurs_1000` | les connecteurs |
| document | — | **non mesurable** (sources sur une ligne) |

Les trois familles du mandat sont les **primaires**. Les autres sont **exploratoires** et corrigées par
Benjamini-Hochberg. La moyenne de famille est la **moyenne des R²_CV des métriques** : c'est un indice de
famille, pas un R² multivarié. Un R² de famille négatif signifie que le modèle fait moins bien que la
moyenne des œuvres, même si la permutation des colonnes est significative.

### 3.2 L'échantillonnage

Pour chaque œuvre, on nettoie la source (Gutenberg, HTML, modèles wiki, URL), on filtre les phrases non
prose (moins de 5 mots, moins de 12 % de mots vides, moins de 55 % de lettres) et on prélève :

- **6 fenêtres non chevauchantes de 10 000 caractères** (60 000 caractères) réparties sur toute l'œuvre,
  si l'œuvre est plus longue ;
- **le texte entier** sinon.

On analyse chaque fenêtre séparément, puis on agrège les compteurs. Les métriques sont des rapports de
compteurs, pas des moyennes de fenêtres. Le nombre de mots mesurés va de **797** à **11 517** (médiane
**10 468**) sur la cohorte primaire.

### 3.3 Le modèle

1. **CLR** (centered log-ratio) des 14 parts ; la 14e colonne est retirée car le CLR est de rang 13
   (somme des logs nulle). La base 13 colonnes a une condition de **27,95**.
2. **Ridge multi-sorties**, avec une **pénalité choisie dans chaque pli** (30 valeurs de λ de 10⁻² à
   10³, validation croisée interne).
3. **LOOCV groupée** : on tient à l'écart une œuvre (ou la paire de doublons), on entraîne sur les
   autres, on prédit. Le R² est calculé sur les prédictions hors-pli.
4. **Statistiques** : R² brut, **ρ de Spearman hors-pli** (robuste aux valeurs extrêmes), et leur
   distribution sous permutation.

### 3.4 Les contrôles

- **Permutation des colonnes** (2 000 tirages) : chaque colonne d'atomes est permutée indépendamment
  entre les œuvres. Le null détruit à la fois l'alignement et la contrainte de composition ; il est donc
  **strict**. On compare le R² observé et le ρ observé à leur null.
- **Contrôle de date** (1 000 permutations) : on ajuste d'abord la métrique sur l'année de composition
  (régression in-sample, année linéaire), puis on demande aux atomes de prédire le **résidu**. Le null
  permute les années avant le même ajustement. On rapporte le R² de la date, son p, le R² résiduel et
  le p résiduel. Une variante quadratique (degré 2) est donnée en sensibilité.
- **Correction multiple** : Holm sur les **3 familles primaires** ; Benjamini-Hochberg sur les métriques
  exploratoires.
- **Cohortes** : la primaire (28), puis 36, 34 et 26 pour voir ce que chaque filtre retire.

### 3.5 Ce qui était pré-déclaré

Avant lecture : la cohorte primaire est **28** (signature propre + ≥ 1 000 jetons) ; les trois familles
sont **POS**, **SYNTAGMES**, **ATTACHEMENT** ; le seuil est **0,05** après Holm ; les métriques
individuelles sont **exploratoires** ; le contrôle principal est la **permutation des colonnes**, le
contrôle de date est **secondaire mais décisif** pour l'interprétation. Le choix de la cohorte 28 est
justifié par l'audit de qualité du § 2, pas par le résultat.

## 4. Résultats

### 4.1 Les trois niveaux du mandat

| famille | R² atomes | p_col | Holm | ρ CV | p_ρ | R² date | p_date | R² résidu | p_resid |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **POS** | **−0,092** | 0,5552 | 1,0000 | **+0,176** | 0,0290 | +0,163 | 0,0140 | −0,567 | **1,0000** |
| **SYNTAGMES** | **−0,160** | 0,8506 | 1,0000 | −0,013 | 0,2579 | +0,058 | 0,1928 | −0,400 | **0,9830** |
| **ATTACHEMENT** | **−0,092** | 0,6652 | 1,0000 | −0,047 | 0,3513 | +0,049 | 0,2328 | −0,219 | **0,9500** |

**Lecture.** Aucune des trois familles n'a de R² positif : le modèle ridge fait **moins bien** que la
moyenne des œuvres. La permutation des colonnes ne sauve que le ρ de POS (**+0,176**, p = 0,029), mais
ce p devient **0,088** après Holm sur les trois familles, et le contrôle de date le retire
(**p_resid = 1,0**). Les syntagmes et l'attachement sont au hasard, et le restent après date.

Le ρ de POS est un artefact de la LOOCV : le null de ρ n'est pas centré sur 0 (la CV avec 13 prédicteurs
sur 28 observations produit des prédictions très resserrées et une légère anticorrélation résiduelle ; la
moyenne du null est **≈ −0,092**) ; c'est pourquoi le p de ρ est plus petit que le p de R². L'excès de ρ
(observé − null) est de **+0,269**, mais il ne correspond qu'à un classement faible, et il disparaît après
date.

### 4.2 Les huit niveaux

| niveau | métrique | R² atomes | p_col | BH | ρ CV | R² date | p_date | p_resid | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| graphème | `graph_entropie` | **+0,811** | 0,0005 | 0,0092 | +0,825 | +0,216 | 0,0130 | 0,9271 | brut, absorbé date |
| mot | `mot_longueur` | **+0,657** | 0,0005 | 0,0092 | +0,744 | +0,393 | 0,0030 | 1,0000 | brut, absorbé date |
| pos | `pos_part_verbe` | **+0,429** | 0,0025 | 0,0277 | +0,593 | +0,369 | 0,0020 | 0,9990 | brut, absorbé date |
| syntagme | `syn_par_phrase` | −0,056 | 0,4538 | 0,8395 | −0,211 | +0,115 | 0,0859 | 0,0120 | non |
| phrase | `phrase_negation` | **+0,440** | 0,0040 | 0,0277 | +0,789 | +0,538 | 0,0010 | 0,7592 | brut, absorbé date |
| pragmatique | `pragma_entropie` | **+0,381** | 0,0045 | 0,0277 | +0,564 | +0,159 | 0,0360 | 0,9520 | brut, absorbé date |
| discours | `disc_connecteurs_1000` | −0,012 | 0,2024 | 0,5547 | −0,122 | +0,004 | 0,7243 | 0,9680 | non |
| attachement | `att_distance` | −0,065 | 0,6887 | 0,9560 | +0,205 | +0,175 | 0,0190 | 0,9301 | non |

**Lecture.** Le dispositif **voit** le style : l'entropie des graphèmes, la longueur des mots, la
négation, la part de verbes et l'entropie pragmatique sont prédites bien au-delà du null de colonnes
(BH < 0,05). Mais **aucune** ne survit au contrôle de date : la date explique à elle seule **0,16 à
0,54** de ces métriques, et les résidus ne sont plus prédits (p_resid = 0,76–1,0). La prédiction des
atomes est donc une **prédiction d'époque et de genre**, pas une prédiction syntaxique.

Le `p_resid = 0,0120` de `syn_par_phrase` est **trompeur** : le R² résiduel est **négatif** ; le p
signale seulement que le modèle est moins mauvais que le null, pas qu'il prédit. C'est pourquoi le
verdict de la ligne est « non ».

### 4.3 Le contrôle de permutation des colonnes

| famille | R² obs | null R² moy | null R² p95 | p_col | ρ obs | p_ρ |
|---|---:|---:|---:|---:|---:|---:|
| POS | −0,092 | −0,096 | +0,051 | 0,5552 | +0,176 | 0,0290 |
| SYNTAGMES | −0,160 | −0,097 | +0,036 | 0,8506 | −0,013 | 0,2579 |
| ATTACHEMENT | −0,092 | −0,079 | +0,020 | 0,6652 | −0,047 | 0,3513 |

Le null de R² est **légèrement négatif** (≈ −0,08 à −0,10) : c'est le coût de la CV avec 13 prédicteurs
sur 28 observations. Les R² observés sont dans ce null, ou en dessous. **La permutation des colonnes tue
la prédiction**, comme demandé.

Pour les métriques de style, le null est très différent : `graph_entropie` observé **+0,811** contre un
null moyen de **−0,10** (p = 0,0005), `mot_longueur` **+0,657** (p = 0,0005), `phrase_negation`
**+0,440** (p = 0,0040), `pos_part_verbe` **+0,429** (p = 0,0025). Le dispositif n'est donc pas un
instrument mort : il détecte des effets réels, mais ces effets sont **datés**.

### 4.4 Le contrôle de date

**Corrélations atome × année (cohorte primaire, 28 œuvres) :**

| atome | ρ(date) | p |
|---|---:|---:|
| `STRUCTURE` | **+0,760** | 0,0000 |
| `ÊTRE` | **−0,596** | 0,0008 |
| `RAPPORT` | **+0,541** | 0,0030 |
| `DIFFÉRENCE` | **−0,536** | 0,0033 |
| `FONCTION` | **+0,448** | 0,0168 |
| `OPÉRATION` | +0,362 | 0,0585 |
| `MODALITÉ` | −0,317 | 0,1002 |
| `SYMÉTRIE` | −0,299 | 0,1223 |
| les six autres | \|ρ\| ≤ 0,18 | ≥ 0,36 |

Cinq atomes sur quatorze sont **datés** au seuil 0,05, et `STRUCTURE` l'est à **+0,760**. La date
explique **0,163** du POS, **0,058** des syntagmes et **0,049** de l'attachement (p_date = 0,014 /
0,193 / 0,233). Après ajustement de la date, les atomes ne prédisent plus les résidus (p_resid =
1,000 / 0,983 / 0,950). La variante de date **quadratique** ne change pas la conclusion : le R² de date
monte à **0,329 / 0,280 / 0,216**, et les p_resid restent **0,997 / 0,967 / 0,867**.

### 4.5 La sensibilité aux cohortes

| cohorte | n | famille | R² | p_col | ρ | p_ρ | R² date | p_resid |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| **utilisable** | **28** | POS | **−0,092** | 0,5552 | +0,176 | 0,0290 | +0,163 | 1,0000 |
| utilisable | 28 | SYNTAGMES | **−0,160** | 0,8506 | −0,013 | 0,2579 | +0,058 | 0,9830 |
| utilisable | 28 | ATTACHEMENT | **−0,092** | 0,6652 | −0,047 | 0,3513 | +0,049 | 0,9500 |
| mesurable | 36 | POS | +0,102 | **0,0040** | +0,280 | 0,0060 | +0,065 | 0,7674 |
| mesurable | 36 | SYNTAGMES | +0,060 | **0,0060** | +0,335 | 0,0020 | +0,035 | 0,1362 |
| mesurable | 36 | ATTACHEMENT | −0,152 | 0,9780 | +0,247 | 0,0100 | +0,026 | 0,9967 |
| propre | 34 | POS | +0,010 | **0,0359** | +0,234 | 0,0040 | +0,103 | 1,0000 |
| propre | 34 | SYNTAGMES | +0,014 | **0,0220** | +0,227 | 0,0060 | +0,053 | 0,7508 |
| propre | 34 | ATTACHEMENT | −0,045 | 0,4870 | +0,186 | 0,0220 | +0,030 | 0,9635 |
| stricte | 26 | POS | −0,080 | 0,3373 | +0,178 | 0,0519 | +0,161 | 1,0000 |
| stricte | 26 | SYNTAGMES | −0,204 | 0,8703 | −0,029 | 0,2874 | +0,073 | 0,9834 |
| stricte | 26 | ATTACHEMENT | −0,278 | 0,9541 | −0,055 | 0,3772 | +0,042 | 0,9402 |

**Ce que la sensibilité dit.** Le signal POS/syntagmes n'apparaît que sur les cohortes **36** et **34**.
Il **tombe** quand on retire les 6 œuvres courtes (34 → 28) puis les 2 signatures non-propres (36 → 34) :
- 36 → 34 : POS **+0,102 → +0,010**, syntagmes **+0,060 → +0,014** ;
- 34 → 28 : POS **+0,010 → −0,092**, syntagmes **+0,014 → −0,160** ;
- 28 → 26 : POS **−0,092 → −0,080**, syntagmes **−0,160 → −0,204**.

Le peu de signal est donc porté par les **sources courtes** (269–941 jetons) et par les **deux signatures
non-propres** (`2_esdras`, `isaiah_book`), pas par les œuvres qui permettent une mesure stable. C'est
exactement ce que le contrôle de qualité devait révéler.

## 5. Ce que le résultat dit

1. **Pour les trois niveaux du mandat, la réponse est non.** Sur la cohorte primaire, le R²_CV est
   négatif pour POS, syntagmes et attachement ; les p de permutation ne sont pas significatifs après
   Holm ; le contrôle de date ne laisse rien.
2. **Le dispositif n'est pas muet.** Il prédit l'entropie des graphèmes (+0,811), la longueur des mots
   (+0,657), la négation (+0,440), la part de verbes (+0,429) et l'entropie pragmatique (+0,381). Ces
   effets sont robustes à la permutation des colonnes (BH < 0,05). Ils constituent le **contrôle positif**
   du dispositif : si le modèle ne trouvait rien nulle part, le null des niveaux serait ininterprétable.
3. **La date absorbe le style.** Les cinq effets ci-dessus ont un R² de date de **0,16 à 0,54** et un
   p_resid de **0,76 à 1,0**. Les atomes sont une signature **chronologique et générique** ; leur
   pouvoir prédictif sur les niveaux est un effet de **composition** (époque, tradition, source,
   traduction).
4. **La table J2.1 reste une hypothèse de lecture.** Le porteur proposé pour chaque atome (∃ → phrase,
   ∼ → syntagme, etc.) n'est pas validé par cette mesure. Il faudrait, pour le tester, un corpus avec
   **gold** POS/syntagmes/attachement et des signatures calculées sur le **même texte nettoyé**.
5. **Le seul signal POS est la part de verbes** (`pos_part_verbe`, R² = +0,429, p = 0,0025), et il est
   **daté** (R² date = +0,369, p_resid = 0,999). Ce n'est pas une prédiction syntaxique : c'est le
   contraste ancien (verbes nombreux) / moderne (style nominal), que la signature V14 capte parce que
   `ÊTRE`, `DIFFÉRENCE`, `RAPPORT` et `STRUCTURE` sont eux-mêmes datés (§ 4.4).

## 6. Ce qui pourrait le rendre faux

1. **Les niveaux sont heuristiques, pas un gold.** Le bloc linguistique de Drave n'a **pas** de gold
   pour les niveaux profonds ; ses confiances sont déclarées (0,32–0,78). Le POS et l'attachement ont
   été évalués sur le gold B13 (POS **86–89 %**, F1 syntagmes **0,79**, attachement **238/239**), mais
   ce gold est **français et synthétique**, alors que le corpus B2 est **anglais, traduit, hétérogène**.
   Un bruit d'annotation **atténue** les corrélations : un effet modéré sur POS/syntagmes pourrait être
   manqué avec n = 28. Le contrôle positif (style) montre que le dispositif n'est pas au plancher, mais
   il ne prouve pas qu'il aurait vu un effet de 0,1.
2. **La signature V14 est calculée sur les 10 000 premiers jetons bruts.** Pour 2 œuvres, c'est une page
   de navigation ou une table des matières ; pour 6 autres, moins de 1 000 jetons. Nous les avons
   retirées de la cohorte primaire, mais les 28 restantes peuvent encore avoir une fenêtre de signature
   atypique (préface, titre, copyright). Si la signature ne résume pas l'œuvre, la prédiction est
   atténuée ou décalée.
3. **La date est celle de la composition, pas de la traduction.** 24/44 sources sont anglaises, 1
   française, 19 de langue inconnue ; les traductions sont majoritairement du XIXe–XXe siècle. Le
   contrôle de date peut donc **sur-corriger** (attribuer à l'époque ce qui est un effet de traduction)
   ou **sous-corriger** (la date de composition n'est pas celle du texte mesuré). C'est le même défaut
   que J12.1.
4. **Le corpus est petit et compositionnel.** 28 œuvres, **26 textes uniques**, **17 GRECO**, deux paires
   de doublons. La CV ne groupe que les doublons exacts : elle ne teste pas la généralisation à un
   **auteur** ou à une **tradition** nouvelle. Un modèle qui apprend « Platon vs Aristote » peut sembler
   prédictif sans l'être pour une œuvre hors corpus.
5. **La moyenne de famille est un indice.** Un R² de famille négatif peut cacher une métrique prédite
   (c'est le cas de `pos_part_verbe`) et noyer une métrique bruitée. Nous donnons les deux lectures :
   la famille (pré-déclarée) et les métriques (exploratoires, BH). Le verdict « non » porte sur la
   famille, pas sur chaque métrique.
6. **Le niveau document n'est pas mesuré.** Les 44 sources sont sur **une seule ligne** : il n'y a ni
   paragraphe, ni section, ni frontière de document exploitables. Le contrat à 9 niveaux n'est donc
   couvert qu'à **7 niveaux + l'attachement** ; le document reste une case vide, pas un résultat nul.
7. **La colinéarité.** Les 14 parts sont fortement corrélées : l'ACP standardisée donne **5 composantes
   > 1** et **68,0 %** de la variance sur les trois premières (33,9 + 21,5 + 12,6) ; la base CLR de rang
   13 a une condition de **27,95**. Le modèle ridge est stable, mais les **coefficients par atome** ne
   le sont pas : nous ne concluons jamais sur un atome isolé, seulement sur l'ensemble.
8. **Le test de date est in-sample pour l'ajustement.** Le résidu est calculé avec un ajustement de date
   sur les 28 œuvres, puis la CV est faite sur les résidus. Le null permute les années et refait le même
   ajustement, donc le **p** est valide ; le **R² résiduel** est optimiste. C'est pourquoi nous nous
   appuyons sur le p_resid et sur le R² brut, pas sur la valeur absolue du R² résiduel.

## 7. Protocole pour rejouer

```bash
# 1. Mesures de niveau (44 œuvres, ~1 min)
python3 tools/atomes_prediction.py --mesurer --forcer

# 2. Analyse (cohorte primaire 28, 2 000 permutations de colonnes, 1 000 de date, ~7 min)
python3 tools/atomes_prediction.py --analyser
```

Le script lit `../../Panini/research` en **lecture seule** et écrit uniquement
`reports/atomes-prediction-mesures.json` et `reports/atomes-prediction.json`. Graine **20261115**.
Les champs utiles du JSON :

- `cohorte_primaire`, `n`, `familles`, `metriques`, `metriques_ecartees` ;
- `cohortes` : les cinq exécutions (28, 36, 34, 26, 28 avec date quadratique) ;
- `atomes_dates`, `acp`, `condition`, `base_clr` (dans chaque cohorte) ;
- `null_col`, `null_resid`, `null_date_in` : les distributions de permutation ;
- `oeuvres` : les 44 lignes, avec signature, qualité de source, dates, métriques et diagnostics.

## 8. Références

- Panini, signatures : `../../Panini/research/nipada/falsification/analytic_sigs_v1.json` (44 × 14).
- Panini, dates et traditions : `../../Panini/research/nipada/falsification/nipada_v334_graph_v35.json`.
- Panini, calcul des signatures : `../../Panini/research/scripts/loi_analytique.py` (10 000 premiers
  jetons, avant nettoyage).
- Table J2.1 (hypothèse de lecture) : [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) et
  [`atomes-niveaux.json`](atomes-niveaux.json).
- Bloc linguistique : [`rapport-bloc-linguistique.md`](rapport-bloc-linguistique.md),
  [`../tools/bloc_linguistique.py`](../tools/bloc_linguistique.py), contrat
  [`../docs/theorie/contrat-bloc-langue.md`](../docs/theorie/contrat-bloc-langue.md).
- Gold B13 (POS, syntagmes, attachement) : [`rapport-bilan-chantier.md`](rapport-bilan-chantier.md) § 3.
- Avertissement β époque/filiation : [`../docs/methode/panini-nipada.md`](../docs/methode/panini-nipada.md).
- J12.1 (date et filiation sur le §334) : [`rapport-panini-334.md`](rapport-panini-334.md).

## 9. Ce que B2 laisse à la suite

- **Un gold de niveaux** sur 100–200 phrases anglaises (POS, syntagmes, attachement) pour remplacer
  l'heuristique par une mesure validée.
- **Une signature recalculée sur le texte nettoyé** (mêmes 10 000 jetons, mais après retrait de
  l'appareil Gutenberg/HTML/TOC) : si le signal POS revient, le résultat actuel est un artefact de
  source ; s'il ne revient pas, le négatif est confirmé.
- **Un contrôle par tradition** (leave-one-tradition-out) : la CV actuelle ne teste pas la
  généralisation hors GRECO.
- **Le niveau document** : il faudra des sources avec paragraphes ou un découpage externe ; les 44
  fichiers actuels ne le permettent pas.

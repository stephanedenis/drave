# 10. Le pont linguistico-sémantique — le vocabulaire de l'émulation

> **Famille 10 du glossaire** (11 familles). Index : [le glossaire](../glossaire.md).

---

## 10. Le pont linguistico-sémantique — le vocabulaire de l'émulation

Cette section couvre le vocabulaire du **pont** (rapports
`reports/rapport-toutes-langues.md`, `reports/rapport-pont-generatif.md`). Elle
manquait entièrement : avant ce rafraîchissement, le glossaire ne contenait
**aucune** occurrence de *professeur*, *réservoir*, *oracle*, *invariance*,
*attrition*, *fragmentation* ni *boîte noire* — c'est-à-dire aucun des mots qui
décrivent le travail en cours. Comme partout ailleurs, chaque entrée définit sur
place les termes qu'elle emploie.

### 10.1 Les acteurs

> **Professeur** *(teacher ; modèle professeur)* — le grand modèle dont on cherche à
> imiter **une** couche. Ici : `qwen2.5-0.5b-instruct-q4_k_m.gguf`. On ne l'entraîne
> jamais et on ne le modifie jamais : on l'interroge et on enregistre. Le mot vient de
> la *distillation* : un petit modèle (l'**élève**) apprend d'un grand. La différence
> est qu'ici l'élève n'apprend pas les sorties du professeur mais une de ses **couches
> internes**.
> Réf. Hinton, Vinyals & Dean, *Distilling the Knowledge in a Neural Network*.

> **Boîte noire** *(black box)* — règle du projet : on ne lit du professeur **que la
> couche à émuler**. Jamais sa **tête**, jamais les jetons qu'il génère. Conséquence
> pratique : on ne peut pas mesurer une perte de langue (perplexité), seulement des
> représentations internes. C'est ce qui rend la comparaison possible entre langues :
> la couche est un vecteur de nombres, la tête serait un vocabulaire.

> **Tête** *(head ; tête de sortie)* — la dernière projection du professeur, qui
> transforme sa représentation interne en probabilités sur son vocabulaire. On ne la
> lit pas. À ne pas confondre avec la « tête » d'un disque dur (§6).

> **Élève** *(student)* — voir **pont**.

> **Pont** *(bridge ; pont linguistico-sémantique)* — notre modèle. Un réseau
> **récurrent** de petite taille, dont la sortie doit ressembler à la couche du
> professeur, et ce **pour toutes les langues à la fois**. Le nom dit l'objectif :
> relier les langues entre elles par un niveau de représentation commun, sans passer
> par les mots.

> **Jeton** *(token)* — l'unité de découpage du texte qu'utilise un modèle. Un mot
> courant vaut souvent un jeton ; un mot rare ou une écriture mal couverte en vaut
> plusieurs. Tout le pont compte en jetons, jamais en caractères — c'est une source
> d'erreur constante (§10.5, *fragmentation*).
> Réf. Sennrich, Haddow & Birch, *Neural Machine Translation of Rare Words with
> Subword Units*.

> **Tokeniseur** *(tokenizer)* — le programme qui découpe le texte en **jetons**. Il
> est propre à chaque modèle et n'est pas neutre entre langues : un tokeniseur
> entraîné surtout sur de l'anglais découpe l'allemand en gros morceaux et le pular
> en miettes.
> Réf. Kudo & Richardson, *SentencePiece*.

### 10.2 Le réservoir

> **Réservoir** *(reservoir)* — un réseau **récurrent** dont les poids internes sont
> tirés **au hasard** puis **gelés** : ils ne changent jamais. Seule la **lecture**
> qui le suit est ajustée. L'idée, venue de l'étude des systèmes dynamiques, est
> qu'un réseau aléatoire assez riche projette déjà l'entrée dans un espace où la
> bonne réponse est accessible par une simple combinaison linéaire.
> Réf. Jaeger, *The "echo state" approach to analysing and training recurrent neural
> networks* (2001) ; Maass, Natschläger & Markram, *Real-time computing without
> stable states* (2002).

> **Calcul par réservoir** *(reservoir computing)* — le paradigme correspondant :
> dynamique fixe et aléatoire + lecture ajustée. Son intérêt ici est double : il
> n'exige **aucune rétropropagation**, et il est très peu coûteux à entraîner.

> **Récurrence** *(recurrence)* — le fait qu'un neurone relise son propre état au pas
> précédent. C'est ce qui donne au réseau une **mémoire** : son état présent dépend de
> tout ce qu'il a lu avant, avec un oubli progressif.

> **État** *(state)* — le vecteur `s_t` des activations du réservoir au pas `t`. C'est
> la seule chose que la **lecture** voit.

> **Constante de temps** *(time constant ; taux de fuite, leak rate)* — le nombre `a`
> qui règle la vitesse d'oubli : `s_t = (1-a)·s_{t-1} + a·tanh(...)`. Un `a` petit
> garde longtemps la trace du passé, un `a` grand l'oublie vite. Le pont utilise
> `a = 0,2`, soit une mémoire d'environ cinq pas. Voir aussi *multi-échelle*.

> **Multi-échelle** *(multi-scale)* — donner à chaque neurone sa **propre** constante
> de temps, étalées logarithmiquement (ici de 0,02 à 0,80), au lieu d'une seule pour
> tous. Motif classique en dynamique : un système qui doit représenter des phénomènes
> lents et rapides a besoin de plusieurs échelles de temps.

> **Gain d'entrée** *(input gain)* — le facteur multiplicatif appliqué à la projection
> de l'entrée. Mesuré : le porter de 1 à 16 ne change **rien** (le `tanh` est déjà
> saturé), et le **baisser** dégrade.

> **tanh** *(tangente hyperbolique)* — fonction qui écrase tout nombre réel dans
> l'intervalle `[-1, +1]`. C'est la non-linéarité du réservoir. Deux régimes
> opposés : petit argument, `tanh(x) ≈ x` (linéaire, l'information passe graduée) ;
> grand argument, `tanh(x) ≈ ±1` (**saturé**, le neurone ne transmet plus qu'un
> signe).

> **Saturation** *(saturation)* — état d'un neurone dont la sortie est collée à
> `±1`. Le pont vit **en saturation quasi permanente** : l'argument du `tanh` vaut
> 16,9 en moyenne. Ce n'est pas un défaut, c'est le mécanisme : la saturation
> transforme l'entrée en signes, et la récurrence en fait une **moyenne glissante de
> signes**, qui est ce que la lecture exploite.
> Réf. Goodfellow, Bengio & Courville, *Deep Learning*, ch. 6 (déjà cité §2).

> **Rayon spectral** *(spectral radius)* — le plus grand module des valeurs propres
> d'une matrice. Pour une récurrence, il décide de la **stabilité** : au-dessus de 1,
> l'état peut diverger ou osciller indéfiniment. Voir *jacobien*.
> Réf. Strogatz, *Nonlinear Dynamics and Chaos* (cité par titre).

> **Jacobien** *(Jacobian)* — la matrice des dérivées partielles d'une transformation.
> Pour la récurrence du pont, `J = (1-a)·I + a·D·P` où `D` est la pente locale du
> `tanh` et `P` la matrice des poids internes. Calculer son **rayon spectral** est la
> façon rigoureuse de vérifier qu'un réseau récurrent ne part pas en oscillation.

> **Oscillation** ; **épilepsie** *(oscillation ; « epilepsy »)* — comportement d'un
> réseau récurrent dont l'état se met à battre indéfiniment au lieu de se stabiliser.
> Nom familier donné au phénomène en neurologie computationnelle. Mesuré : **absente**
> du pont jusqu'à `a = 0,95`.

### 10.3 Structure du réseau

> **Couche** *(layer)* — ici, un ensemble de neurones soumis à une règle de
> connectivité stricte : **un neurone de la couche `c` ne lit que la couche `c-1`
> entière, et les siens nés avant lui**. Il ne lit jamais une couche plus basse
> directement. Sans cette règle, « ouvrir une couche » et « ajouter un neurone »
> produisent exactement le même calcul — c'était le cas dans une version antérieure
> du pont, où les 24 « couches » n'étaient qu'une numérotation.

> **Neurone** — une unité qui calcule une moyenne pondérée de ses entrées, la passe
> au `tanh`, et la mélange à son propre passé. Le mot est employé au sens de
> *unité de calcul*, sans prétendre imiter un neurone biologique.

> **Naissance** *(birth)* — l'ajout d'un neurone au réseau. Ici, **un neurone à la
> fois** : aucun calendrier (1, 2, 4, 8… 256) ni plafond imposé, parce qu'un compte
> rond est le signe qu'on a **choisi** la taille au lieu de la **mesurer**.

> **Naissance libre** *(free birth)* — le mode correspondant. Une **couche** neuve ne
> s'ouvre que sur deux signes mesurés : (1) la couche courante est épuisée, et
> (2) des **concepts communs** ont émergé. Sinon on ajoute des neurones à la couche
> existante.

> **Concept commun** *(common concept)* — un neurone dont la trajectoire suit le même
> contenu d'une langue à l'autre, au lieu de suivre un trait propre à une langue.
> C'est le signal qui autorise une couche supplémentaire.

> **Attrition** *(attrition ; élagage, pruning)* — le retrait des neurones
> redondants. Point capital : on **recalcule** la trajectoire des survivants sans les
> retirés ; on ne se contente pas de masquer des colonnes. Sinon, on ne mesure pas une
> réduction mais un masquage.

> **Redondance** *(redundancy)* — à quel point l'activation d'un neurone est déjà
> prédite par celle des autres. Le pont la calcule par un complément de Schur, donc
> une seule inversion de matrice. Voir *contribution*.

> **Contribution** *(contribution)* — l'énergie qu'un neurone apporte à la sortie,
> produit de la norme de son poids de lecture et de la norme de son activation.

> **Généalogie** *(genealogy)* — l'ensemble `(poids_parents, poids_couche, biais,
> couche, constante de temps)` conservé pour **chaque** neurone. C'est elle qui permet
> de recalculer un sous-ensemble de survivants sans les retirés. Toute recopie de la
> généalogie doit être complète : une constante de temps oubliée fait calculer
> **silencieusement** la mauvaise dynamique.

### 10.4 La lecture, et l'absence de rétropropagation

> **Lecture** *(readout)* — la transformation, ajustée, qui convertit l'**état** du
> réservoir en la sortie visée. Ici elle est **linéaire** (ou quadratique), et c'est
> la **seule** partie du pont qui est apprise.

> **Rétropropagation** *(backpropagation)* — l'algorithme standard qui ajuste les
> poids d'un réseau en propageant l'erreur de la sortie vers l'entrée. **Le pont ne
> l'utilise pas.** C'est une contrainte du projet, pour deux raisons : elle exige de
> connaître la sortie désirée partout, et elle rend l'apprentissage dépendant d'un
> calcul global, donc peu compatible avec une croissance locale par corrélation.
> Réf. Rumelhart, Hinton & Williams (1986) ; LeCun et al. (1988) ; Lillicrap,
> Santoro, Marris, Akerman & Hinton, *Backpropagation and the brain* (2020).

> **Forme fermée** *(closed form)* — une solution calculée d'un seul coup par une
> formule, par opposition à une méthode qui s'approche par étapes successives. La
> régression **ridge** est en forme fermée ; **NLMS** ne l'est pas.

> **Régression** *(regression)* — ajuster les coefficients d'une combinaison pour
> qu'elle approche au mieux une cible. Voir *moindres carrés*.

> **Moindres carrés** *(least squares)* — le critère classique : minimiser la somme
> des **carrés** des écarts entre la prédiction et la cible. « Carrés » a une
> conséquence qu'on oublie : une ligne dont la cible a une norme double pèse **quatre
> fois** plus dans l'objectif.

> **Régression ridge** *(ridge regression ; régression de Tikhonov)* — des moindres
> carrés auxquels on ajoute une pénalité proportionnelle au carré des coefficients.
> Elle sert à stabiliser le calcul quand les colonnes sont corrélées, ce qui est
> toujours le cas ici. Elle est en **forme fermée**, donc sans rétropropagation.
> Réf. Hoerl & Kennard, *Ridge Regression: Biased Estimation for Nonorthogonal
> Problems* (1970) ; Tikhonov (1943).

> **Ride** *(ridge coefficient ; λ)* — le nombre qui règle la force de cette
> pénalité. **Mesuré : le pont utilisait 0,3, soit dix à trente fois trop.** La
> fidélité de TEST est maximale à **0,03**.

> **Matrice de Gram** *(Gram matrix)* — la matrice `AᵀA` des produits scalaires deux à
> deux des colonnes d'une matrice `A`. C'est elle qu'on accumule pour résoudre une
> régression. Son coût est `O(lignes × caractéristiques²)` — **c'est le goulot du
> pont** : 22 minutes pour 1 296 colonnes.

> **Caractéristiques** *(features)* — les colonnes de la matrice sur laquelle porte la
> régression. Ici : les états du réservoir, et éventuellement l'entrée du professeur.

> **Lecture quadratique** *(quadratic readout)* — une lecture qui voit
> `[états, états²]` au lieu de `[états]`. Elle reste en forme fermée et n'ajoute
> qu'une inversion.

> **NLMS** *(normalized least mean squares ; moindres carrés moyens normalisés)* —
> une règle **locale** et itérative : `W ← W + η·(y − W·x)·xᵀ/‖x‖²`. Elle ne
> construit aucune Gram et n'inverse aucune matrice — elle conviendrait donc à une
> implémentation par **événements**. **Mesuré, et le pas décide de tout** :
>
> | η | après 1 passe | après 6 passes |
> |---:|---:|---:|
> | 0,003 | **0,6158** (−0,0075 sous la ridge) | 0,6058 (−0,0175) |
> | 0,1 | 0,4971 (−0,1261) | 0,4971 (gelé) |
>
> À pas fin, NLMS arrive à **0,0075** de la ridge en **une** passe, puis se dégrade :
> elle sur-apprend le vivier (la validation reste à 0,624, le test baisse). Il faut
> donc l'arrêter tôt, sur la validation.
>
> **Coût comparé** : la Gram coûte `O(lignes × caractéristiques²)`, NLMS
> `O(lignes × caractéristiques × sorties)`. Avec 896 sorties, la ridge est ~11× moins
> chère à 80 caractéristiques, mais **NLMS devient moins chère au-delà d'environ 900
> caractéristiques** — c'est-à-dire exactement là où le pont se trouve quand il
> grossit. Le mode matriciel n'est donc pas à jeter : il est à **réserver aux petits
> réseaux**.
> Réf. Haykin, *Adaptive Filter Theory* (cité par titre).

> **Règle delta** *(delta rule ; règle de Widrow-Hoff)* — l'ancêtre de NLMS :
> `ΔW = η·(cible − prédiction)·entrée`. Locale, sans rétropropagation.
> Réf. Widrow & Hoff, *Adaptive Switching Circuits* (1960), cité par titre.

### 10.5 La mesure — ce que chaque chiffre veut dire

> **Fidélité** *(fidelity)* — la **similarité de cosinus** entre la sortie du pont et
> la couche du professeur, moyennée sur les positions puis sur les langues. Elle vaut
> entre −1 et 1. On dit « fidélité » et non « précision » : on ne prédit pas une
> classe, on ressemble plus ou moins à un vecteur.

> **Similarité de cosinus** *(cosine similarity)* — le cosinus de l'angle entre deux
> vecteurs. Elle **ignore les longueurs** : multiplier un vecteur par 10 ne la change
> pas. C'est capital ici — une langue dont les représentations sont « fortes » n'est
> ni avantagée ni pénalisée. Deux vecteurs opposés donnent −1.

> **Norme** *(norm)* — la longueur d'un vecteur. Mesuré : la norme de la couche 10 du
> professeur varie de 362 à 574 selon la langue — c'est une propriété **réelle** de la
> langue, pas un artefact de longueur de texte.

> **Témoin constant** *(constant baseline)* — la réponse la plus bête possible :
> prédire partout le même vecteur, la moyenne des cibles d'apprentissage. Tout modèle
> doit la battre, sinon il n'apporte rien. **Attention** : c'est un témoin **faible**,
> et la fidélité du pont s'y réduit à 97,7 % près. Voir *apport propre*.

> **Apport propre** *(own contribution)* — la fidélité **moins** le témoin constant.
> C'est la seule quantité qui dise quelque chose du pont, et non du corpus.

> **Invariance inter-langue** *(cross-lingual invariance)* — à quel point deux langues
> qui disent la même chose ont des représentations qui se ressemblent. Mesurée par la
> similarité de cosinus entre les représentations de langues différentes pour un même
> contenu aligné, moyennée sur toutes les paires.

> **Pire paire** *(worst pair)* — la plus mauvaise similarité parmi toutes les paires
> de langues. Une moyenne peut cacher une langue qui décroche ; la pire paire ne le
> peut pas.

> **Oracle** *(oracle)* — une lecture **ajustée sur le jeu qu'on évalue**, donc
> avantagée. Ce n'est **pas un modèle**, c'est un **diagnostic** : il borne ce que les
> caractéristiques permettent. Si l'oracle plafonne comme nous, le problème est dans
> les caractéristiques ; s'il monte haut, il est dans le transfert.

> **Vivier** *(pool)* — l'ensemble des langues disponibles pour l'apprentissage.

> **Hors vivier** / **même vivier** *(out-of-pool / in-pool)* — une langue **hors
> vivier** n'a jamais été vue à l'apprentissage ; une langue **du même vivier** a
> servi, mais la lecture n'a pas été ajustée sur elle.

> **Panneau** *(panel)* — un jeu d'évaluation. Le protocole en exige **deux** : le
> **TEST**, hors vivier, et la **VALIDATION**, du même vivier. L'écart entre les deux
> sépare ce qui vient du transfert de ce qui vient des caractéristiques.

> **Écart à l'oracle** *(oracle gap)* — oracle moins notre fidélité. Mesuré :
> **+0,0975 hors vivier contre +0,0112 dans le vivier**. C'est le résultat qui a
> identifié le **transfert** comme goulot.

> **Fragmentation** *(fragmentation ; jetons par caractère)* — combien de jetons le
> tokeniseur produit pour un caractère. Mesuré : **1,578** en pular (le tokeniseur
> hache) contre **0,271** en allemand (il est efficace), soit un rapport de 6. Corrélé
> à la norme de la cible (−0,55) et à l'apport propre du pont (+0,82).

> **Corrélation de Pearson** *(Pearson correlation)* — mesure de liaison **linéaire**
> entre deux séries, entre −1 et 1. Sensible aux valeurs extrêmes.

> **Corrélation de Spearman** *(Spearman correlation)* — la même chose calculée sur
> les **rangs** plutôt que sur les valeurs. Insensible aux extrêmes et aux
> transformations croissantes. **Toujours donner les deux** : un écart entre elles
> signale que la liaison tient à quelques points.

> **Corrélation partielle** *(partial correlation)* — la liaison entre deux séries
> **après avoir retiré** l'effet d'une troisième. Sert à ne pas attribuer à une
> variable ce qui appartient à une autre — par exemple la norme plutôt que la
> longueur.

> **Coefficient de détermination** *(R²)* — la fraction de la variance expliquée,
> entre 0 et 1. Un R² de 0,67 signifie « les deux tiers ».

> **Sur-apprentissage** *(overfitting)* — apprendre les particularités du jeu
> d'apprentissage au lieu de la régularité sous-jacente. Se voit à l'écart entre
> l'apprentissage et le test.

### 10.6 Le professeur, concrètement

> **Couche 0** *(layer 0 ; couche d'entrée)* — la sortie de la couche d'embedding du
> professeur : le premier vecteur associé à chaque jeton. C'est ce que le pont reçoit
> en entrée. Sa norme vaut environ 720.

> **Couche cible** *(target layer)* — la couche du professeur que le pont cherche à
> reproduire. Le projet a d'abord visé la **couche 10**, puis mesuré que la **couche
> 8** est le plateau sémantique (invariance 0,6998 contre 0,6471).

> **Trace DRVF** *(DRVF trace)* — le fichier binaire produit par le moteur, qui
> contient les activations du professeur position par position. Format décrit au §3.

> **Encodage positionnel rotationnel** *(rotary position embedding ; RoPE)* — la
> façon dont un modèle transformer inscrit la **position** d'un jeton dans son
> vecteur. Elle a une conséquence méthodologique : la position est lisible dans la
> couche 0, donc une lecture pourrait prédire le contenu par la seule position **si le
> corpus est aligné**. Mesuré : cet effet vaut +0,0145, il n'explique pas les
> résultats.
> Réf. Su et al., *RoFormer*.

> **Qwen2.5-0.5B-Instruct** — le professeur employé. Un modèle « transformer » de
> 24 couches et environ 500 millions de paramètres, quantifié en Q4_K_M (§3).
> Réf. Qwen Team, *Qwen2.5 Technical Report*.

### 10.7 Les corpus

> **UDHR** *(Universal Declaration of Human Rights ; Déclaration universelle des
> droits de l'homme)* — un texte **unique** traduit en plusieurs centaines de langues.
> C'est le corpus principal du pont (392 langues), parce qu'il est **aligné** :
> chaque langue dit exactement la même chose, ce qui rend l'invariance mesurable.
> Réf. Assemblée générale des Nations unies, résolution 217 A (III), 1948.

> **Corpus aligné** *(aligned corpus)* — un ensemble de textes où le segment `i` d'une
> langue correspond au segment `i` d'une autre. Condition **nécessaire** pour mesurer
> l'invariance inter-langue. L'UDHR et *Roméo et Juliette* sont alignés ; Wikipedia ne
> l'est pas.

> **Corpus non aligné** — les segments ne se correspondent pas. On peut y mesurer la
> fidélité et le transfert, **pas** l'invariance. Un chiffre d'invariance calculé sur
> un corpus non aligné ne veut rien dire, et le logiciel le dit lui-même.

> **Unité** *(unit)* — une des dix sections alignées dans lesquelles l'UDHR a été
> découpée. Traiter par unité donne dix points de mesure alignés par langue au lieu
> d'un seul, donc une invariance dix fois mieux étayée.

### 10.8 Ce que la mesure a établi, en une page

Les entrées ci-dessus renvoient à des résultats datés. Ceux qui structurent tout le
reste, avec leur chiffre :

- **La fidélité du pont EST le témoin constant** (corrélation +0,9768). Son classement
  par langue ne dit presque rien du pont. D'où l'**apport propre**.
- **L'écart à l'oracle est 8,7 fois plus grand hors vivier que dans le vivier**
  (+0,0975 contre +0,0112). Le goulot est le **transfert**, pas la taille ni la
  lecture.
- **Le réservoir paie, et de plus en plus** : 0,0329 à 200 neurones, 0,0399 à 400,
  **0,0457 à 800** — sans coude.
- **La profondeur n'achète rien** : 2 couches de 20 valent 1 couche de 40 (0,5979
  contre 0,5972). Le pont tient dans une couche face aux 24 du professeur.
- **Le ride était 10 à 30 fois trop fort** : 0,03 au lieu de 0,3, soit +0,0074 gratuit.
- **La dynamique n'est pas creuse** : 99,8 % des couples (neurone, pas) changent à
  chaque pas, à tout gain. Une implémentation par **événements** de cette dynamique ne
  paierait rien — le passage aux **impulsions** est un changement de dynamique, pas un
  réglage.
- **Aucune oscillation** : rayon spectral < 1 pour `a` de 0,05 à 0,95.

### 10.9 Termes employés DANS les définitions du §10, et qui n'avaient pas d'entrée

Le glossaire se lit seul : tout mot employé pour définir un autre doit avoir sa
propre entrée. Ceux-ci apparaissaient au §10 sans en avoir.

> **Valeur propre** ; **vecteur propre** *(eigenvalue ; eigenvector)* — pour une
> matrice `M`, un vecteur `v` tel que `M·v = λ·v` : la matrice ne fait que
> l'étirer, sans changer sa direction. Le nombre `λ` est la valeur propre associée.
> Ce sont elles qui composent le **rayon spectral**, donc qui décident de la
> stabilité d'une récurrence.

> **Complément de Schur** *(Schur complement)* — pour une matrice `G` découpée en
> blocs `[[A, B], [C, D]]`, la quantité `D − C·A⁻¹·B`. Ici il sert à mesurer la
> **redondance** : la part de l'activation d'un neurone que les autres expliquent
> déjà se lit sur la diagonale de l'inverse de la matrice de Gram, ce qui évite
> `K` inversions séparées pour `K` neurones.

> **Inversion de matrice** ; **résolution de système linéaire** *(matrix inversion ;
> linear solve)* — trouver `x` tel que `M·x = b`. C'est l'opération centrale de la
> **forme fermée** : une régression ridge se résout par une seule résolution. Son
> coût croît comme le **cube** du nombre d'inconnues, ce qui explique pourquoi
> passer de 80 à 2 496 colonnes change un calcul de quelques secondes en plus d'une
> heure.

> **Moyenne glissante** *(moving average ; moyenne mobile exponentielle)* — une
> moyenne qui donne plus de poids au présent et oublie progressivement le passé. La
> récurrence `s_t = (1-a)·s_{t-1} + a·x_t` en est une exactement. C'est ce que
> calcule le réservoir du pont : une moyenne glissante de valeurs saturées, donc de
> **signes**.

> **Algorithme itératif** ; **convergence** ; **point fixe** *(iterative algorithm ;
> convergence ; fixed point)* — une méthode qui s'approche du résultat par étapes
> successives, par opposition à la **forme fermée**. Elle **converge** quand les
> étapes rapprochent de la solution, et atteint un **point fixe** quand elles ne
> changent plus rien. Attention : un point fixe n'est pas forcément la bonne
> réponse — **NLMS** en atteint un à 0,4971 là où la ridge donne 0,6233.

> **Parcimonie** *(sparsity)* — le fait qu'une représentation ait **peu** d'éléments
> non nuls. Une représentation parcimonieuse se calcule et se stocke beaucoup moins
> cher. Mesuré : la couche 10 du professeur est **dense en support** (862 canaux sur
> 896 sont écrits) mais **creuse en énergie** (40 canaux portent la moitié). Les deux
> questions sont différentes et ne se contredisent pas.

> **Impulsion** *(spike)* — dans un réseau de neurones à impulsions, un signal bref
> émis quand le potentiel d'un neurone franchit un **seuil**, suivi d'une **remise à
> zéro**. C'est un événement, pas une valeur continue : c'est ce qui rend un tel
> réseau **parcimonieux par construction**. Le pont actuel n'en émet pas — sa
> dynamique est continue et saturée. Voir §10.8 et `reports/rapport-toutes-langues.md`.

> **Frame temporelle** *(time frame)* — dans un simulateur à impulsions, la tranche
> de temps pendant laquelle on regroupe les événements avant de les traiter. Le
> projet `neuronspikes` annonce des frames jusqu'à 15 360 Hz, soit une résolution de
> 65 microsecondes.

> **Plongement** *(embedding)* — la traduction d'un objet discret (un jeton, une
> image) en un **vecteur** de nombres réels, de façon que des objets proches aient
> des vecteurs proches. La **couche 0** du professeur est exactement cela.

> **Élagage** *(pruning)* — synonyme d'**attrition** au §10.3 : le retrait des
> unités inutiles. Le mot est plus courant en apprentissage automatique ; le dépôt
> emploie les deux.

> **Contexte** ; **fenêtre de contexte** *(context ; context window)* — le nombre de
> jetons qu'un modèle peut lire avant de répondre. Sans rapport avec le « contexte »
> d'un processus (§4).

### 10.10 Le vocabulaire de la mesure contenu / langue

Ces termes sont nés de la traque des §57 à §70 et sont devenus **la mesure centrale** du
pont. Ils manquaient au glossaire.

> **`P_lang`** *(énergie de langue)* — la variance des **moyennes par langue** de la
> sortie, autour de la moyenne globale. Ce que la représentation porte **parce que la
> langue change**, à contenu égal. On veut qu'elle soit **basse**.

> **`P_cont`** *(énergie de contenu)* — la variance des **moyennes par contenu** de la
> sortie, autour de la moyenne globale. Ce que la représentation porte **parce que le
> sujet change**, à langue égale. On veut qu'elle soit **haute** — et proche de celle du
> professeur.

> **Rapport contenu/langue** *(content-to-language ratio)* — `P_cont / P_lang`. Il vaut
> **10,912** pour le professeur à sa couche 8, et **1,698** pour une lecture optimale de
> sa propre couche 0. C'est le premier chiffre qui dise qu'une représentation **sépare**
> le sujet de la langue au lieu de tout confondre.

> **Invariance d'échelle** *(scale invariance)* — le fait qu'une quantité ne change pas
> quand on multiplie son objet par un facteur. **Le rapport contenu/langue est invariant
> d'échelle** : `P_cont` et `P_lang` sont tous deux quadratiques, donc multiplier la
> sortie par `α` les multiplie tous deux par `α²`. **Aucune amplification ne peut donc
> corriger le rapport** — seulement un changement de directions. C'est une identité, pas
> une observation, et elle explique cinq échecs consécutifs (§67).

> **Décomposition de variance** *(variance decomposition)* — écrire la variance totale
> d'un jeu de représentations comme la somme d'une part **entre langues**, d'une part
> **entre contenus** et d'un résidu. Exacte et additive. C'est elle qui a **localisé** le
> défaut du pont : douze fois moins d'énergie de contenu que le professeur, à énergie de
> langue comparable (§61).

> **Analyse discriminante linéaire** *(linear discriminant analysis ; LDA)* — trouver les
> directions d'un espace qui **maximisent le rapport** entre la variance d'un groupe et
> celle d'un autre. C'est un **problème aux valeurs propres généralisé**,
> `C_cont·v = λ·C_lang·v`, donc **en forme fermée** et sans rétropropagation. Appliquée à
> la sortie du pont, elle porte le rapport de 1,93 à **6,96** — 64 % de celui du
> professeur — mais coûte 0,12 à 0,23 de fidélité (§69).
> Réf. Fisher, *The use of multiple measurements in taxonomic problems* (1936), cité par
> titre.

> **Rétrécissement** *(shrinkage)* — le fait qu'un ajustement par moindres carrés
> produise des prédictions **plus petites** que leurs cibles, ramenées vers la moyenne.
> Mesuré sur le pont : `‖écart à la moyenne‖/‖moyenne‖` vaut **0,623** chez nous contre
> **2,145** chez le professeur — un facteur **3,4**. C'est un défaut réel, mais
> l'amplifier ne rétablit pas l'ordre contenu/langue (§60).

> **Frontière** *(trade-off frontier)* — l'ensemble des compromis atteignables entre deux
> quantités qu'on ne peut pas maximiser ensemble. Ici : **fidélité contre rapport
> contenu/langue**. Mesurée : à rapport 6,96 la fidélité tombe à 0,43 ; pour amener
> `P_cont` à la magnitude du professeur elle tombe à **0,24** (§69.3).

> **Caractéristiques emboîtées** *(nested features)* — comparer des jeux de
> caractéristiques dont l'un contient l'autre, pour attribuer un effet à la partie
> ajoutée. C'est ainsi qu'on a montré que **l'axe de langue vient de l'entrée** et non du
> réservoir : l'entrée seule a un rapport de 1,698, le réservoir seul de 1,354 (§70).

> **Sous-espace de langue** *(language subspace)* — les directions d'un espace de
> représentations qui portent la différence **entre langues**. On l'estime par les
> vecteurs propres dominants de la covariance inter-langue, puis on projette sur son
> complément. **Déployable** : c'est une matrice fixe apprise une fois (§66).

---


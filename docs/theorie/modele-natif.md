# Le modèle Drave natif — un graphe, un flux, trois niveaux

> **Ce que ce document est.** La **théorie** du modèle natif : ce qu'il est (un **graphe de blocs** exécuté sur un
> **bus de faits**), ce qui le distingue d'un transformeur monolithique, et le **principe de séparation à trois
> niveaux** — surface, RSN, pensée — qui rend la neutralité **mesurable** au lieu de la promettre. Les **chiffres**
> de `drave-n0` et des campagnes N sont dans [`reports/`](../../reports/) ; le **format** dans
> [`architecture-native.md`](architecture-native.md) et [`format-flux.md`](../implantation/format-flux.md) ;
> l'**implémentation d'un bloc impulsionnel** dans [`diehl-cook.md`](../implantation/diehl-cook.md).

> **Fiche concept — le modèle natif.**
> Un modèle Drave n'est pas un fichier de tenseurs : c'est un **graphe de blocs** dont les arêtes portent des
> **contrats typés**, exécuté par un **bus de listes valuées**, et **rejouable** à l'octet. `drave-n0` en est la
> première instance : 6 blocs, des octets, une attention locale, un FFN creux routé, 3 têtes précoces, une cellule
> de pensée et un pont.
> **Glossaire :** [couche / étage](glossaire/entrees/couche-etage.md) · [RSN](glossaire/entrees/representation-semantique-neutre.md) ·
> [fait · mesuré · projeté · déduit](glossaire/entrees/fait-mesure-projete-deduit.md)
> **Illustration :** ![Trois niveaux de contrat, un centre neutre](../schemas/natif-niveaux.svg)

## 1. Ce qu'on appelle « natif »

**Natif** veut dire **conçu pour le régime Drave**, pas « adapté après coup ». Le régime tient en quatre
propriétés : le modèle est **décomposable** (un bloc se lit et s'exécute seul), **répartissable** (un bloc va là
où son entrée est déjà), **observable** (chaque activation est un fait daté) et **rejouable** (la même trace
redonne le même résultat). Un modèle qui n'a pas ces quatre propriétés n'est pas natif, même s'il est écrit dans
un fichier qui s'appelle DRVM.

**Trois choses, et il faut les distinguer** :

| le mot | ce qu'il désigne | où il vit |
|---|---|---|
| **DRVM** | le **conteneur** : manifeste, graphe, tenseurs, exécution | [`architecture-native.md`](architecture-native.md) |
| **`drave-n0`** | le **modèle** : l'instance de 6 blocs qui remplit ce conteneur | [`roadmap.md`](../pilotage/roadmap.md) § N |
| **le régime** | la **manière d'exécuter** : listes valuées, sorties précoces, routes, rejeu | [`format-flux.md`](../implantation/format-flux.md) |

**Ce que le natif n'est pas** : un consommateur de GGUF, un petit Qwen3-MoE, un transformeur dans une boîte
neuve. GGUF est un **conteneur de tenseurs** ; Qwen3-MoE est une **architecture générique** ; les deux supposent
un modèle **monolithique, dense, exécuté d'un bloc**. Drave est un **graphe de blocs événementiels**, avec des
sorties précoces, des routes, des contrats d'activation et du rejeu. La différence n'est pas cosmétique : elle
change ce qu'on peut mesurer.

**La thèse** : *la structure bat la taille*. Un pont linéaire, une grille de conversion, un routage de blocs
valent mieux que des paramètres ajoutés. Le natif est l'endroit où cette thèse devient un format.

## 2. Les trois niveaux — surface, RSN, pensée

### Le problème

Une même chose a **beaucoup de surfaces** : un chiffre est un tracé de pixels, un glyphe Unicode, un mot dans
trois langues ; une position d'échecs est une FEN, un diagramme, une suite SAN. Si le raisonnement lit la
surface, deux écritures de la même chose peuvent produire deux décisions différentes. L'invariance devient alors
invérifiable — et un modèle qui ne peut pas prouver son invariance n'a pas de centre, seulement des couches.

La séparation est **volontaire** et **ordonnée** :

![Trois niveaux de contrat, un centre neutre](../schemas/natif-niveaux.svg)

| niveau | ce qu'il porte | ce qu'il a le droit de lire | ce qu'il rend |
|---|---|---|---|
| **N1 — surface** | texte, image, notation, langue, style | la surface | une **RSN** |
| **N2 — RSN** | les **unités de sens**, le corps canonique, l'annotation | une RSN (ou `φ(RSN)`) | une RSN |
| **N3 — pensée** | les opérations : composer, inférer, planifier, décider | une RSN **seulement** | une RSN d'action |

**La règle** : *le niveau est un contrat de port, pas un algorithme*. Un même code — un réseau, un solveur, un
index — peut être N1, N2 ou N3 selon ce qu'il **reçoit** et ce qu'il **rend**. Un bloc qui reçoit la surface est
N1 ; un bloc qui rend une décision sans RSN n'est ni N2 ni N3 : il **fuit** la surface vers le raisonnement, et
c'est cette fuite que le format doit refuser.

**Pourquoi trois niveaux, et pas deux.** À deux niveaux, il n'y a que deux architectures possibles, et les deux
échouent :

- **surface → pensée** : la pensée dépend de la surface ; deux écritures du même sens peuvent donner deux
  décisions, et l'invariance n'est pas testable ;
- **surface → RSN** : c'est un encodeur sans opération ; il peut classer, pas raisonner, et il n'y a pas de
  contrat pour brancher un solveur.

Le troisième niveau insère le **contrat** qui manque : la RSN est ce qui rend la pensée **substituable** (un
solveur ou un réseau au même endroit) et **mesurable** (la même RSN, la même décision). Ce n'est pas un étage de
plus : c'est la **condition** des deux autres.


### Ce que la RSN est, et ce qu'elle n'est pas

La RSN est une **structure multi-niveaux** (graphémique/phonologique, morphologique, syntaxique, sémantique,
discursif/pragmatique), **indépendante de la langue de surface**, **annotée de son bruit** (confiance,
ambiguïtés, langues probables, format d'origine). Ses éléments sont des **unités de sens**, jamais des **jetons**
de tokeniseur : le jeton est le porteur technique du modèle, pas l'unité du contrat.

Trois propriétés la rendent vérifiable :

1. **canonique** — deux surfaces qui disent la même chose donnent le même **corps**, donc la même **empreinte** ;
2. **séparable** — l'**annotation** (le bruit, la langue, le format) est **hors de l'empreinte** ; elle est
   transportée, pas confondue avec le sens ;
3. **typée et réversible** — le corps est un arbre de `null`, `bool`, `int`, `str`, listes et dictionnaires,
   **sans flottant** ; tout corps encodé se décode à l'identique.

C'est le contrat déjà utilisé par les jeux symboliques : voir [`jeux-symboliques.md`](jeux-symboliques.md). Ce
qui est **original** ici n'est pas l'idée d'une interlingua — elle est ancienne — mais le fait que le contrat soit
**porté par le format** (ports typés, graphe, refus) et **mesuré** (sonde de format, invariance, restitution).

### La RSN comme quotient

Une RSN n'est pas un vecteur : c'est une **classe d'équivalence**. Soit `S` l'ensemble des surfaces et `~` la
relation « dire la même chose ». La RSN est le quotient `S/~`, représenté par deux fonctions :

- `c : S → C`, le **canoniseur**, qui rend le **corps** ; il doit vérifier `c(s) = c(s') ⇔ s ~ s'` ;
- `a : S → A`, l'**annotation**, qui rend le bruit : langue, format, confiance, ambiguïtés, source.

Le **corps** est l'invariant ; l'**annotation** est le chemin. L'empreinte est `h = H(c(s))` : elle ne dépend que
du corps. Deux surfaces du même sens ont le même `h`, même si l'une est un PNG et l'autre une phrase.

![La RSN est un quotient, pas un vecteur](../schemas/natif-quotient.svg)

**Le miroir est une rétraction.** Un décodeur `d : C × A → S` est un miroir si `c(d(c(s), a(s))) = c(s)` : il
peut changer la surface, pas le sens. La restitution exacte (`d(c(s), a(s)) = s`) est plus forte ; elle n'est pas
toujours possible — une image perdue ne se reconstruit pas — et c'est pourquoi le contrat demande la **fidélité du
corps**, pas la copie de l'octet.

**Trois conséquences opérationnelles** :

1. **l'annotation n'entre pas dans `c`** — sinon deux surfaces du même sens n'ont plus le même corps ;
2. **le corps ne contient pas de flottant** — sinon l'équivalence dépend de l'arrondi de la machine ;
3. **le hash n'est pas le sens** — c'est un représentant ; ce qui fait foi, c'est `c`, pas `h`.

**Ce que le quotient achète** : la neutralité devient une **propriété de l'image de `c`**, pas une intention. On
peut la tester : si `c` dépend encore du format, deux surfaces équivalentes n'ont pas le même corps, et le test
le dit. C'est pour cela que la RSN est un **contrat** et pas un espace latent de plus.

**Mais la RSN de travail est plurielle.** Le quotient décrit **un** candidat ; l'état de pensée est un **ensemble**
de candidats, avec un arbre, une frontière et des statuts. La RSN canonique unique est le **résultat** d'un cycle,
pas la représentation de travail. Voir [`pensee-iterative.md`](pensee-iterative.md).


### Niveau, étage, couche — ne pas confondre

> **Note de vocabulaire.** Un **niveau** est un **contrat de port** : N1 surface, N2 RSN, N3 pensée. Un **étage**
> est une **étape d'architecture** : l'étage 1 est l'entrée-sortie (N1 ↔ N2), l'étage 2 est la pensée (N3). Une
> **couche** est une **couche de neurones**. Les « niveaux 0–4 » de [`jeux-symboliques.md`](jeux-symboliques.md)
> sont autre chose : les couches de lecture d'une surface. Voir [couche / étage](glossaire/entrees/couche-etage.md).

**Deux étages, trois niveaux** : l'étage 1 contient N1 et N2 ; l'étage 2 est N3. C'est pour cela que la vision
parle de **deux étages** sans contredire la séparation à **trois niveaux** : le niveau du milieu est le contrat
qui sépare les deux étages.

### Le système de types et la légalité du graphe

Un bloc a une **signature** : `b : (τ_1, …, τ_n) → (σ_1, …, σ_m)`, où chaque type est `surface`, `rsn`, `code`
ou `trace`. Son **niveau** est **déclaré** dans le manifeste et **vérifié** contre sa signature : la signature
**borne** les niveaux possibles, elle ne les devine pas.

| signature | niveaux possibles | exemple |
|---|---|---|
| `surface → rsn` | N1 | encodeur |
| `rsn → surface` | N1 | décodeur |
| `rsn → rsn` | N2 **ou** N3, déclaré | mémoire / opération |

**Les règles** :

- `surface` n'entre jamais dans un bloc N2 ou N3 ;
- `code` — le code interne, spikes ou latent — **ne traverse jamais une arête** : il est privé au bloc ;
- `rsn` circule entre N1, N2 et N3 ;
- `trace` est un port de sortie, jamais une entrée de calcul.

![Le système de types](../schemas/natif-types.svg)

**Théorème (pas de fuite de surface).** Dans un graphe légal, tout chemin d'une entrée `surface` vers un bloc N3
traverse au moins une arête `rsn`. *Preuve.* Une arête `surface` ne peut entrer que dans un bloc **déclaré N1**
(le chargeur le vérifie). La sortie d'un bloc N1 est soit `surface` (décodeur), soit `rsn` (encodeur). Pour
atteindre N3, le chemin doit donc emprunter une arête `rsn`. ∎

**La composition ne change pas la règle.** Le niveau d'un bloc composé est **déclaré** ; sa signature externe le
contraint : un composite `surface → rsn` est N1, même s'il contient une mémoire N2 à l'intérieur. C'est ce qui
permet de **substituer** un encodeur par un autre sans toucher au reste du graphe.

**Le raffinement.** `b'` raffine `b` au niveau L si `b'` a la même signature et si, pour toute entrée,
`c(b'(x)) = c(b(x))` (même corps) et les annotations sont compatibles. La substituabilité est un **raffinement
+ une trace** : on remplace, on rejoue, on compare. C'est la définition opérationnelle du bus.

**Le type `rsn` se décline.** Un bloc N1 rend des **candidats** ; un bloc N2 transforme un **état** (un ensemble
de candidats) ; un moteur N3 a la signature `state → state` (ou `state → décision`). Le type `rsn` ne disparaît
pas : il devient le **contenu** d'un état, pas l'état lui-même. Voir [`pensee-iterative.md`](pensee-iterative.md).


### Neutralité et informativité

La neutralité seule est un piège : un code **constant** est parfaitement neutre et parfaitement inutile. La
propriété utile est un **couple** :

- **neutre** : le format (langue, notation, appareil) n'est pas prédictible depuis le corps ;
- **informatif** : la classe (le sens) est prédictible depuis le corps.

Deux sondes, deux attendus :

| sonde | entrée | attendu | si ça échoue |
|---|---|---|---|
| `P_f` format | `c(s)` | **échec** (chance) | la RSN fuit la surface |
| `P_y` classe | `c(s)` | **succès** | la RSN a détruit le sens |

![Neutre et informatif : les deux sondes](../schemas/natif-neutralite.svg)

Le **marginal sémantique** est `I − N` (informatif moins neutre) ; on veut les deux hauts. Le diagramme montre
les quatre quadrants et les deux pièges : le **collapse** (constant) et la **fuite** (code de surface).

**La neutralité est relative au corpus.** Si toutes les images françaises sont des 7 et toutes les anglaises des
1, la sonde de format apprend la classe : ce n'est pas une fuite de la RSN, c'est un corpus **confondu**. Le
contrôle est un corpus **équilibré** par format et une sonde **linéaire** — pas un réseau profond qui mémorise.


### Ce que la séparation coûte

La séparation n'est pas gratuite, et il faut l'écrire :

- **deux fois le travail** : un encodeur et un décodeur (le miroir), deux jeux de mesures ;
- **un canoniseur par modalité** : le corps n'est pas donné, il se construit et se maintient ;
- **des sondes** : la neutralité se mesure, donc elle se paie en corpus et en évaluations ;
- **une latence** : le passage par la RSN ajoute une étape, et parfois un goulot ;
- **une perte** : tout ce qui n'entre pas dans le corps est perdu pour le raisonnement — il reste dans
  l'annotation, mais l'annotation n'est pas le sens ;
- **un risque de collapse** : un corps trop pauvre est parfaitement neutre et parfaitement inutile.

Le bon critère n'est pas « la séparation est belle », c'est « la séparation **rapporte** plus qu'elle ne coûte »
sur une tâche mesurée. C'est pourquoi les sondes et le miroir sont dans le contrat, pas dans les bonnes intentions.


### Le miroir

Toute mesure d'entrée se double d'une mesure de **sortie**. Un encodeur sans décodeur n'est pas un bloc de
langue, c'est un classifieur : il peut être juste sans être **fidèle**. Le miroir impose trois choses :

1. **la sortie valide l'entrée** — ce que N1 a compris doit pouvoir être redit par le décodeur, à l'identique ou
   en boucle ;
2. **le sens se découple du bruit** — la sortie sert de référence ; on mesure l'écart entre ce que l'entrée a
   extrait et ce que la sortie sait reconstruire ;
3. **le bruit voyage avec le sens** — le module de pensée reçoit une RSN **annotée**, pas une RSN « propre » qui
   ferait croire à une vérité.

La formule du dépôt : **la fluidité n'est pas la fidélité**. Une sortie belle peut être fausse ; c'est la
restitution qui tranche. Voir [`miroir.md`](../methode/miroir.md).

## 3. Le bus — des faits, pas des matrices

Une activation n'est pas une case dans un tenseur : c'est un **fait** — « le neurone 2 539 de la couche 23 a valu
27,8 ». Les faits d'une même source sont regroupés en une **liste valuée** `(indices, valeurs, échelle)`, et la
liste est **poussée** vers ses lecteurs. Le coût du calcul devient proportionnel à l'**activité**, pas à la
taille du modèle.

![Le coût suit l'activité, pas la taille](../schemas/natif-cout-activite.svg)

**Deux régimes, et le moteur garde les deux.** Le croisement push/pull est mesuré à **~22 % de densité** : en
dessous, les listes gagnent ; au-dessus, le dense reste meilleur. Ce n'est pas un aveu de faiblesse, c'est la
condition d'une mesure honnête : le dense est un **chemin de première classe**, pas un pis-aller. La fiche est
dans [`rapport-croisement-push-pull.md`](../../reports/rapport-croisement-push-pull.md) ; le format et ses
mesures dans [`format-flux.md`](../implantation/format-flux.md).

**Le même format sert quatre choses** : la **trace** (`--trace-flux`), le **rejeu** (`--flux-forcer`), le
**transport** (`--flux-serveur`) et l'**analyse** (`profil_flux.py`, `analyse_flux.py`, `diff_flux.py`). Une liste
d'activation est une liste d'activation, qu'elle aille sur le disque ou sur le réseau. C'est ce qui rend le
modèle **observable** : le flux n'est pas un sous-produit du calcul, c'est l'instrument de réglage.

**Le rejeu est exact, et il a un piège nommé.** Le champ `jeton` de DRVF est un **compteur global**, pas la
position dans la fenêtre : avec `--depuis`, un même jeton traité dans deux fenêtres consomme **deux** clés. Une
trace ne se rejoue donc qu'avec la même configuration de fenêtres. Le format le dit, parce qu'une trace qui se
rejoue en silence avec une perplexité fausse est pire qu'une trace qui refuse.

## 4. Le graphe — blocs, régions, routes, têtes

L'unité de conception n'est pas la couche, c'est le **bloc**. Un bloc a des entrées et des sorties **typées**, un
**coût mesurable**, et une **trace**. Il peut être **neuronal** (l'intuition, la langue, la perception) ou
**classique** (une règle, un solveur, un index, un compilateur) : le bus ne fait pas la différence.

![drave-n0 : un graphe, pas une pile](../schemas/natif-graphe-n0.svg)

**`drave-n0` en une ligne** : 11,47 M de paramètres, **6 blocs**, un vocabulaire d'**octets** (256), une
attention locale (fenêtre 256), un **FFN creux routé** (8 experts, top-2, k-WTA 25 %), **3 têtes précoces**
(après les blocs 2, 4, 6), une **cellule de pensée** récurrente et un **pont** entre deux régions. Les chiffres
et l'état sont dans [`roadmap.md`](../pilotage/roadmap.md) § N ; la décision de conception dans
[`architecture-native.md`](architecture-native.md).

**Les huit types de blocs de DRVM v0** :

| kind | rôle | ce qu'il porte |
|---|---|---|
| `input` | l'entrée | octets + positions |
| `local_mixer` | le mélange local | attention fenêtrée |
| `sparse_ffn` | le FFN creux | routeur, experts, k-WTA |
| `state` | l'état | récurrence, mémoire de travail |
| `early_head` | la sortie précoce | une tête par profondeur |
| `thought` | la pensée | cellule contractante, λ < 1 |
| `bridge` | le pont | projection entre régions |
| `output` | la sortie | tête octet + tête RSN typée |

**Le manifeste porte le graphe**, pas seulement une liste de tenseurs. Un fragment réel, réduit :

```json
{
  "format": "DRVM",
  "version": 0,
  "model": {"name": "drave-n0", "tokenizer": {"kind": "bytes", "vocab": 256}},
  "graph": {
    "blocks": [
      {"id": "input", "kind": "input", "inputs": [], "outputs": ["h"]},
      {"id": "b0", "kind": "local_mixer", "inputs": ["h"], "outputs": ["h"]},
      {"id": "early0", "kind": "early_head", "inputs": ["h"], "outputs": ["y0"]}
    ],
    "regions": [{"id": "r0", "blocks": ["input", "b0", "early0"]}],
    "heads": ["early0"],
    "routes": [],
    "thought": {"steps": 1}
  }
}
```

**Un bloc inconnu est refusé**, pas ignoré : `BLOCS_CONNUS` est une liste fermée, et le lecteur rend une erreur
qui nomme le type. C'est une **fonctionnalité** : un modèle à moitié compris qui s'exécute quand même est un
modèle qui ment. Le même principe vaut pour la version et pour une section absente.

**Pourquoi un graphe plutôt qu'une pile** : parce que les mécanismes de Drave sont des **arêtes**, pas des
couches. Une **sortie précoce** est une arête qui court-circuite la fin ; un **pont** est une arête entre deux
régions ; une **route** est une arête conditionnelle ; la **pensée** est une arête qui boucle. Une pile ne sait
pas dire ces choses ; un graphe, si.

### Le mode d'opération est privé

**La RSN n'est pas un bloc.** C'est le **type** qui circule. Les blocs qui la produisent ou la consomment —
encodeur, mémoire, décodeur — sont, eux, **technologiquement libres**. Confondre les deux, c'est croire qu'un
format est une machine.

**Le principe** : un bloc est défini par sa **signature typée**, son **contrat** (ce que le corps doit être), sa
**trace** et son **coût** — pas par sa technologie. Le mode d'opération (dense, impulsionnel, classique, FPGA,
neuromorphe, distant) est **privé** : il ne regarde ni le bus, ni le consommateur. Le bus ne voit pas des
neurones ; il voit des types.

![Le contrat est l'invariant, la technologie est la variable](../schemas/natif-modes.svg)

**Le théorème d'indifférence.** Si deux blocs ont la même signature et satisfont le même contrat — même corps
pour les mêmes entrées, annotations compatibles, même trace — alors ils sont **substituables**, quelle que soit
leur technologie. Le consommateur ne peut les distinguer que par le **coût** et la **trace**. *Preuve.* Le
consommateur ne lit que le type et le corps ; par hypothèse, ils sont égaux. ∎

**Ce que l'indifférence exige** : un **test de contrat** (les sondes), une **trace** (le rejeu), un **coût**
(le placement). Sans les trois, l'hétérogénéité n'est pas une modularité, c'est un zoo.

**Le mode d'apprentissage est privé aussi.** Un bloc peut apprendre par STDP locale, par gradient hors ligne,
par une règle classique, ou ne pas apprendre. Le contrat ne voit que la sortie ; mais le bloc doit **déclarer**
son mode et son niveau de rejeu, sinon la trace n'est pas reproductible.

**Le corollaire pour la RSN** : un encodeur RSN peut être un transformeur, un réseau impulsionnel, un analyseur
à règles ou un service distant. Le consommateur ne le sait pas ; il voit une RSN, une empreinte et une trace.
C'est ce qui rend le centre **neutre vis-à-vis de la technologie**, pas seulement de la langue.

### La granularité : petit, mais pas trop

**Pourquoi petit** : un bloc petit a un contrat simple, un coût mesurable, une place possible sur un device, et
une chance d'être remplacé. Un monolithe n'a aucune de ces quatre propriétés.

**Pourquoi pas trop petit** : chaque arête paie une **liaison** (sérialisation, transport, synchronisation,
trace). Le coût total est :

`coût_total = coût_bloc + k · nombre_d_arêtes`

Si le bloc est trop petit, `k · arêtes` domine ; s'il est trop gros, la substitution meurt. L'optimum dépend de
la tâche et du matériel : il se **mesure**, il ne se décrète pas.

![La bonne granularité](../schemas/natif-granularite.svg)

**La règle de conception** : un bloc doit tenir sur **un** device (ou un nœud), avoir **un** contrat, et payer
une liaison **négligeable** devant son coût. Quand ce n'est pas le cas, on découpe ou on fusionne — et on
remesure.

### Le graphe dynamique

**Le graphe n'est pas figé.** Les routes changent (top-2, seuils), les sorties précoces court-circuitent la fin,
la pensée boucle, les blocs apprennent. Ce qui ne change pas, c'est le **type des ports** et la **trace** : le
graphe peut être reconfiguré sans casser les contrats.

| dynamicité | ce qui change | ce qui reste | où c'est tracé |
|---|---|---|---|
| **routage** | quelles arêtes sont actives | les ports | la route, par pas |
| **profondeur** | combien de blocs sont traversés | le contrat de sortie | la sortie précoce |
| **apprentissage** | les poids, les prototypes | la signature | les événements d'apprentissage |

**La règle** : une dynamicité qui change le **type** n'est pas une dynamicité, c'est un **autre graphe**. Un
graphe qui change de contrat en cours de route n'est pas dynamique ; il est inconsistant.


## 5. DRVM — le conteneur

**DRVM** (Drave Model) est un conteneur **versionné**, **mmap-able**, **par bloc**, avec quatre sections :

![DRVM : le conteneur du modèle](../schemas/natif-drvm.svg)

| section | ce qu'elle porte | ce que ça permet |
|---|---|---|
| **Manifeste** | version, hash, provenance, tokenizer, schéma RSN | refuser, dater, reproduire |
| **Graphe** | blocs, ports, régions, routes, têtes, pont | lire, router, placer |
| **Tenseurs** | offsets alignés, dtype, forme, quantification, masque de sparsité | mmap par bloc, quantifier |
| **Exécution** | placement, cache, graines, contrat d'activation, tolérances de rejeu | rejouer, répartir |

**Le critère de DRVM n'est pas « il contient tout », c'est « un bloc se lit seul »** : `mmap`, placement
indépendant, rejeu indépendant. Le hash du manifeste couvre le graphe et les poids ; un lecteur qui ne connaît
pas un bloc le **refuse**. C'est la différence avec un conteneur qui tolère l'inconnu : ici, l'inconnu est une
erreur, pas une extension.

**Trois formats, trois rôles, à ne pas confondre** :

| format | porte | rôle |
|---|---|---|
| **DRVM** | le **modèle** | poids + graphe + routes + contrats |
| **DRVF** | les **activations** | trace, rejeu, transport, analyse |
| **RSN** | le **sens** | champs typés, codec, universaux |

**GGUF reste un format d'import/export**, pas le format natif. Un GGUF Qwen se convertit en DRVM et doit rendre
la même perplexité ([`rapport-drvm-ppl.md`](../../reports/rapport-drvm-ppl.md)) ; l'inverse n'est pas vrai : un
DRVM n'a pas à être un GGUF qui s'ignore.

## 6. Le régime d'exécution

Le graphe ne sert à rien s'il n'est pas **exécuté autrement**. Cinq mécanismes font le régime :

| mécanisme | ce qu'il change | où il se mesure |
|---|---|---|
| **sortie précoce** | on répond avant la fin quand la confiance suffit | [`rapport-deepseek.md`](../../reports/rapport-deepseek.md) |
| **pensée contractante** | λ < 1, contenu conservé après k pas | [`rapport-deepseek.md`](../../reports/rapport-deepseek.md) |
| **pont tardif** | une projection entre régions, 30× moins chère que le pont précoce (cible) | [`architecture-native.md`](architecture-native.md) |
| **FFN creux routé** | 8 experts, top-2, k-WTA 25 % : la sparsité est un budget | [`roadmap.md`](../pilotage/roadmap.md) § N |
| **cache et placement** | le cache KV natif, le placement par bloc | [`rapport-native-cache.md`](../../reports/rapport-native-cache.md) |

### Rejouer : la pile de déterminisme

Le rejeu n'est pas une propriété du format : c'est une **pile** de décisions, et chaque étage peut la casser.

| étage | source de non-déterminisme | décision | test |
|---|---|---|---|
| graine | tirage implicite | graine déclarée dans le manifeste | deux runs, même graine |
| RNG | ordre d'appel | tirage **contré** `hash(seed, exemple, pas, neurone)` | permuter l'ordre des neurones |
| ordre | réduction flottante | ordre fixe, réduction séquentielle ou arbre déterministe | 1 thread contre 4 |
| arithmétique | fast-math, FMA | f64, pas de contraction, NaN canonique | même résultat sur deux machines |
| trace | ordre des clés | JSON canonique, clés triées | hash de la trace |
| hash | collision | SHA-256 | deux traces égales → même hash |

![Rejouer : la pile de déterminisme](../schemas/natif-rejeu.svg)

**Trois niveaux de rejeu**, et il faut dire lequel on revendique :

1. **bit-exact** : mêmes spikes, mêmes poids — c'est ce que D&C revendique ;
2. **tolérant** : mêmes logits à `ε` près — pour les blocs flottants non déterministes ;
3. **sémantique** : même corps de RSN — pour les blocs qui changent de surface.

Un bloc qui ne peut pas dire **lequel** il garantit ne garantit rien. Le diff n'est pas un supplément d'âme :
c'est ce qui transforme « ça a l'air de marcher » en « voici le premier pas qui diverge ».


**Ce que la mesure a déjà tranché** — et qui contraint la suite :

- **le contexte est le verrou** : 129 octets est le meilleur point, 130 est négatif, 2 000 octets font
  s'effondrer la perplexité. Allonger le contexte demande **un autre schéma**, pas un curriculum de plus ;
- **le saut de calcul existe, le saut de contenu n'existe pas** : la sortie précoce gagne du temps en perdant des
  points ; c'est une décision sur la **confiance du prochain octet**, pas sur la **pertinence** ;
- **la mémoire manque** : le signal courant est lisible, celui d'il y a 8 pas ne l'est pas ; le tampon gelé lit,
  mais le réseau ne s'en sert pas.

Les trois leçons sont écrites dans [`roadmap.md`](../pilotage/roadmap.md) § N, avec leurs fiches. Elles ne
condamnent pas le natif : elles disent **où** il faut changer de schéma, ce qui est plus utile qu'un score.

## 7. L'objectif d'entraînement

**Le prochain octet ne suffit pas** : il n'apprend ni à sortir tôt, ni à penser, ni à se décomposer. Le natif a
donc **sept pertes**, et chacune a une porte :

![Sept pertes, un seul objectif](../schemas/natif-pertes.svg)

| # | perte | ce qu'elle installe | contrôle |
|---:|---|---|---|
| 1 | **prochain octet** | le socle : prédire | perplexité, jeu tenu à l'écart |
| 2 | **distillation** | la distribution du professeur | écart au professeur, permutation |
| 3 | **pertes locales par bloc** | chaque région reste utile seule | ablation d'une région |
| 4 | **têtes précoces** | la bonne réponse à la profondeur *k* | tête précoce contre témoin sans tête |
| 5 | **contraction de la pensée** | λ < 1, contenu conservé | λ et contenu après *k* pas |
| 6 | **cohérence du pont** | la sortie d'une région reste lisible | pont contre sans pont |
| 7 | **budget de sparsité** | k-WTA 25 %, pas plus | qualité à budget égal |

**Les données sont le second verrou.** 610 exemples sont un **banc**, pas un corpus : la cible v0 est
**50 000 séquences**, avec un jeu **tenu à l'écart** et un **contrôle par permutation**. La capacité ne paie
qu'avec les données — c'est la leçon de B9, et elle n'a pas changé.

## 8. Ce qui est original

![Ce qui est original, en six gestes](../schemas/natif-original.svg)

**1. Le bloc, pas la couche.** L'unité de conception a des ports, un coût et une trace ; deux implémentations du
même contrat se remplacent **sans toucher au bus**. Le bloc est **aveugle à sa technologie** : le même contrat
accepte un transformeur, un réseau impulsionnel, un solveur ou un service distant. C'est ce qui rend la comparaison honnête : même entrée, même
sortie attendue, même trace.

**La leçon de L (04/11) : le service distant gagne l'analyse, pas le sens.** Sur le gold 432, un
service distant (l'API DeepSeek) mesuré comme un bloc du contrat donne **POS 0,9309**,
**syntagmes 0,8226**, **tête 0,8784** — contre 0,7394 / 0,2520 / 0,4511 pour l'heuristique — mais
**acte pragmatique 0,0000** : il ne rend pas la pragmatique. La **fusion par niveau**
(`PRIORITE_NIVEAU`) prend au neuronal ce qu'il fait mieux (POS, syntagmes) et laisse à
l'heuristique ce qu'elle fait mieux (pragmatique, 0,9954). Pour le natif, cela fixe trois
exigences :

1. **Le contrat doit porter le niveau**, pas seulement la sortie : un bloc qui ne rend pas un
   niveau doit le **déclarer** (refus), et la fusion doit choisir **par niveau** — c'est la
   version native de « le bloc, pas la couche ».
2. **La tokenisation est un contrat** : le service a rendu **7 POS pour 6 tokens** sur
   `l'écoutent` (élision) ; un bloc natif qui tokenise autrement que le centre casse la
   comparaison. Le centre doit imposer sa tokenisation, ou le bloc doit la déclarer.
3. **Le réel doit être joignable dans les portes** : le mock avait conclu l'inverse du réel
   (niveau 0,3432 contre 0,7424) ; un défaut choisi sur le mock est un défaut faux. Toute
   décision de fusion se mesure **avec le réel**, sinon elle reste une hypothèse.

**2. Le format porte le graphe.** DRVM ne stocke pas seulement des tenseurs : il stocke des **blocs**, des
**régions**, des **routes**, des **têtes** et un **contrat d'activation**. Un format qui ne sait pas dire ces
choses ne peut pas exécuter le régime.

**3. Le coût suit l'activité.** Les listes valuées, poussées, font que le calcul paie les **faits**, pas les
zéros. Le dense reste un chemin de première classe : le moteur choisit par la mesure, pas par doctrine.

**4. Le réflexe est entraîné.** Les têtes précoces ne sont pas un ajout après coup : elles ont leur perte, leur
porte et leur contrôle. Une sortie précoce qui n'est pas entraînée est une sortie fausse plus rapide.

**5. Le centre est un contrat.** La RSN n'est pas un espace latent de plus : c'est un **objet typé, canonique,
annoté**, avec une empreinte qui ne dépend pas de la surface. C'est ce qui rend la **neutralité mesurable** — et
c'est ce qui permet de brancher un réseau impulsionnel, un solveur ou un index au même endroit.

**6. Le rejeu est un citoyen.** La trace n'est pas un log de débogage : c'est le même format que le transport et
l'analyse, avec un **diff** qui dit *où* le calcul diverge. Un modèle qu'on ne peut pas rejouer n'est pas
observable ; il est seulement reproductible par chance.

**Ce qui n'est pas original** : le transformeur, le MoE, le spike, l'interlingua, la sparsité. Drave ne prétend
pas les inventer. Ce qui est original, c'est **l'assemblage contraint** : un format qui refuse, un bus qui pousse,
un centre qui type, un rejeu qui compare.

| critère | GGUF + transformeur | DRVM + `drave-n0` |
|---|---|---|
| unité de conception | la couche | le **bloc** |
| format | un sac de tenseurs | un **graphe** + des contrats |
| exécution | dense, d'un bloc | listes, **sorties précoces**, routes |
| coût | ∝ taille | ∝ **activité** |
| sortie | une tête finale | têtes précoces + **réflexe** |
| centre | pas de contrat de sens | **RSN** typée, neutre, annotée |
| rejeu | non | **DRVF** + diff |
| substitution | architecture figée | bloc **substituable** |
| inconnu | toléré | **refusé** |

## 9. Les portes N

![Les portes du natif : N0 → N4](../schemas/natif-portes.svg)

| porte | question | critère |
|---|---|---|
| **N0.1** | DRVM se lit-il ? | aller-retour octet-à-octet, `mmap`, hash, refus de version |
| **N0.2** | le moteur le charge-t-il ? | `drave-core` lit DRVM sans conversion |
| **N0.3** | GGUF reste-t-il importable ? | un GGUF Qwen se convertit et rend la même perplexité |
| **N1.1** | l'entraîneur et le moteur sont-ils d'accord ? | même perplexité à 1e-4 près |
| **N1.2** | le réflexe paie-t-il ? | accord de la tête précoce > témoin sans tête |
| **N1.3** | la pensée est-elle contractante ? | λ < 1 et contenu > baseline |
| **N2.1** | la distillation paie-t-elle ? | écart au professeur ≤ 4,40 % (B9) |
| **N2.2** | les langues tiennent-elles ? | pas de chute > 5 pts sur 30 langues |
| **N3.1** | la sparsité paie-t-elle ? | même qualité, moins d'octets |
| **N3.2** | le rejeu est-il exact ? | trace identique, mêmes logits |
| **N4.1** | le chat est-il utilisable ? | suivi d'instructions, arrêt, multi-tours |

**Une porte rouge n'est pas un échec** : c'est une information qui nomme ce qui manque. Le registre se lit par
le **code de sortie**, jamais par un marqueur. Voir [`portes.md`](../methode/portes.md).

## 10. Les anti-patrons

Six façons de casser la séparation, et le test qui les attrape :

![Six anti-patrons, et le test qui les attrape](../schemas/natif-anti-patrons.svg)

| anti-patron | symptôme | test |
|---|---|---|
| **le code promu** | le code de spikes s'appelle « RSN » | la sonde de format réussit sur le corps |
| **la surface au raisonneur** | N3 lit les pixels ou le texte | changer le format change la décision |
| **l'annotation dans le corps** | la langue ou le format est dans l'empreinte | deux surfaces du même sens → deux hashes |
| **le jeton déguisé** | la RSN est une suite de jetons | changer le tokeniseur change le sens |
| **le faux miroir** | le décodeur invente, l'encodeur ne restitue pas | `c(d(c(s))) ≠ c(s)` |
| **le niveau décoratif** | le manifeste dit N2, le bloc lit la surface | la sonde de format réussit sur un bloc N2 |

**Le plus fréquent est le premier** : un bloc impulsionnel produit un beau vecteur creux, on l'appelle
« représentation sémantique », et personne ne vérifie qu'il est neutre. Le test est la sonde, pas l'intuition.

## 11. Ce qui pourrait rendre ce document faux

- **Trop petit** : 12 M ne parle pas ; `drave-n0` est un **banc de mécanismes**, pas un assistant. Si on le juge
  comme un chat, il échoue — et ce n'est pas une information sur le régime.
- **DRVM devient un second GGUF** : si le graphe n'est qu'un décor et que les routes ne sont pas exécutées, le
  critère « un bloc se lit seul » est perdu. Le test est un bloc chargé et exécuté **sans** le reste.
- **La distillation plafonne** : si l'élève ne fait que copier le professeur, les pertes locales et les têtes
  précoces ne servent à rien. Le contrôle par permutation et le jeu tenu à l'écart sont obligatoires.
- **Les octets ne paient pas** : les séquences sont 3–4× plus longues ; le BPE a été mesuré et écarté à budget
  égal (R13), mais il reste une **condition de réouverture** à 50–100 M, pas un dogme.
- **Le centre n'est pas neutre** : si une sonde de format retrouve la langue ou la notation dans le **corps** de la
  RSN, la séparation est décorative. La sonde est le contrôle ; sans elle, « neutre » est un mot.
- **Le graphe n'est pas utilisé** : si retirer le pont, les routes ou les têtes précoces ne change rien, alors le
  modèle est une pile qui s'ignore. Chaque arête doit avoir une ablation.

## 12. Les questions ouvertes

Ce document dit ce qui est **défini** ; il ne dit pas que tout est **résolu**. Les questions qui restent, et ce
qui les trancherait :

| question | ce qui la trancherait |
|---|---|
| **canoniser à l'échelle** : combien de modalités, et comment composer des RSN de modalités différentes ? | un canoniseur multi-modal, mesuré sur des paires parallèles |
| **l'algèbre de l'annotation** : comment composer langue, format, confiance et ambiguïté sans fuite ? | un monoïde d'annotation implanté, avec une preuve de non-fuite |
| **la neutralité relative** : quel corpus, quelle puissance, quel adversaire ? | une sonde adversariale sur un corpus équilibré, avec un seuil |
| **le coût de la séparation** : deux fois le travail, une latence ; la RSN est-elle un goulot ? | une mesure de bout en bout, en temps réel |
| **le composite** : un `surface → rsn` contient une mémoire N2 ; fuit-il ? | un test de bout en bout + une preuve de composition |
| **le rejeu distribué** : la pile tient sur une machine ; deux nœuds ? | un rejeu à deux nœuds, diff à zéro |
| **la substitution** : que faire des annotations incompatibles ? | un protocole de raffinement avec tolérance déclarée |

**Ce qui ne changera pas** : la RSN est un **quotient**, pas un vecteur ; le niveau est un **contrat déclaré**,
pas une couche ; la neutralité est un **couple** avec l'informativité, pas une vertu. Ces trois phrases sont la
partie stable du document.

## 13. Où lire la suite

- **Le format** : [`architecture-native.md`](architecture-native.md) · [`format-flux.md`](../implantation/format-flux.md) ·
  [`format-clusters.md`](../implantation/format-clusters.md)
- **Le sens** : [`protocole-semantique.md`](protocole-semantique.md) · [`jeux-symboliques.md`](jeux-symboliques.md) ·
  [`semantique-universaux.md`](semantique-universaux.md)
- **Le plan et l'état** : [`roadmap.md`](../pilotage/roadmap.md) § N · [`en-cours.md`](../pilotage/en-cours.md) ·
  [`reports/README.md`](../../reports/README.md)
- **Un bloc impulsionnel concret** : [`diehl-cook.md`](../implantation/diehl-cook.md) — comment un réseau de type
  Diehl & Cook (2015) devient un bloc Drave sans franchir les niveaux.
- **La pensée itérative** : [`pensee-iterative.md`](pensee-iterative.md) — la RSN plurielle, l'arbre d'états et
  le portefeuille de stratégies.

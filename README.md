# Drave

> **Ce que ce document est.** La vitrine publique de Drave : la vision, les cinq axes, les deux
> étages, six résultats et l'état du dépôt. Les chiffres sont cités comme état ; les fiches sont
> dans [`reports/`](reports/). **Chargement :** T1 — ce résumé, puis la section utile.

**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Un moteur qui traite les
activations d'un réseau de neurones comme des **faits** — « le neurone 2 539 de la couche 23 a valu 27,8 » — et non
comme des cases dans une matrice. Le coût du calcul devient proportionnel à l'**activité**, pas à la taille du
modèle ; le modèle devient **décomposable**, **répartissable** sur du matériel divers, et **observable** — on peut le
tracer, le rejouer, le comparer.

*« Stream of logs » : le flux des listes. Et « la drave » — ces billots qu'on confiait à la rivière au printemps,
qu'on guidait de l'estacade jusqu'à la scierie. Le nom dit ce que fait le moteur : il ne lit pas des matrices, il
conduit un flux.*

## Essayez — le premier produit

Le bloc linguistique s'utilise **aujourd'hui**, hors ligne, sur un CPU, sans modèle ni réseau :

```bash
python3 tools/drave.py analyser "Le chat de la voisine qui dort sur le toit se réveille."
python3 tools/drave.py analyser "The cat that sleeps on the roof is black." --langue en --json
python3 tools/drave.py evaluer        # la mesure sur le gold (POS, F1, attachement)
python3 tools/drave.py rejouer "Le chat dort."   # vérifie le déterminisme (sha256)
```

Sortie : une **annotation** — langue, classes de mots, syntagmes avec rôle et **cible
d'attachement**, acte de parole — avec ses spans et sa confiance, de façon **déterministe**. Le
**format est versionné** (`schema: "drave.annotation"`, `version: 1`, schéma publié dans
[`tools/schemas/`](tools/schemas/), un refus est une réponse JSON avec le code 3). La notice
complète est [`docs/produit/README.md`](docs/produit/README.md), les exemples vérifiés
[`docs/produit/exemples.md`](docs/produit/exemples.md), et la porte produit
`bash tools/porte-produit.sh` (10 contrôles, ~2 min).

**Mesuré au 20/11** : POS **86,25 %** en français (**95,75 %** avec l'option `--tagger`),
syntagmes F1 **0,7902**, attachement **238/239** (couverture **99,58 %**), 183/183 portes.
Sur les **452 phrases réelles** (hors synthétique) : POS 88,91 %, F1 79,06 %, attachement
99,46 %. Les limites sont dites : **1 span inatteignable** (`g017`), la génération du modèle
natif ne produit que des collages, et la traduction n'est pas là.


## Ce que c'est, en clair

**Le problème.** Un modèle d'IA (un « réseau de neurones ») est aujourd'hui une grosse boîte de
calcul : pour lire une phrase, il refait des milliards de multiplications, même si la plupart des
neurones ne servent à rien sur cette phrase. Conséquence : il faut des machines énormes, on ne
sait pas ce qui se passe dedans, et on ne peut ni le découper ni le répartir.

**L'idée.** Au lieu de voir le modèle comme une **grille de nombres** qu'on multiplie en entier,
Drave le voit comme un **flux de faits** : « le neurone 2 539 de la couche 23 a valu 27,8 ». On ne
calcule que ce qui **s'active** — le coût suit l'**activité**, pas la taille du modèle. Une image :
au lieu d'allumer toutes les lampes d'un immeuble pour trouver la bonne pièce, on suit les
personnes qui s'y déplacent.

**Ce que ça change, concrètement** : un modèle qu'on peut **observer** (compter, tracer), **rejouer**
(la même entrée redonne la même sortie, au bit près), **découper** en morceaux et **répartir** sur
plusieurs machines ou plusieurs cartes — et, si la densité d'activité est assez faible (sous
~22 %), **plus rapide** que le calcul classique.

**Ce que ce n'est pas.** Drave ne promet pas un modèle plus intelligent ; il promet un modèle
**maîtrisable** : on sait ce qu'il fait, on peut le mesurer et le corriger, et il tient sur du
matériel modeste.

## L'origine

Drave est né d'un besoin concret : faire fonctionner des modèles neuronaux **de types différents** sur des machines
dont les **ressources sont limitées** ; **combiner** plusieurs modèles ; **décomposer** un modèle existant en
**couches et grappes de neurones** exécutables par des **combinaisons de matériel divers**, voire **distribuées en
réseau** ; **diagnostiquer** et **faire évoluer** les réseaux en étudiant leurs **flux de données**, avec le pouvoir
de **rejouer à volonté** des événements. Partant de là, on crée des modèles plus facilement et on combine des
architectures innovantes.

L'ambition : faire éclore des modèles **plus légers, plus flexibles et plus puissants**, tout en restant **très
flexibles sur le matériel** qui les supporte. Le cahier des charges d'origine (l'inférence ternaire sur un cluster de
cartes Stratix V, [`Qtrinet-bootstrap.md`](Qtrinet-bootstrap.md)) est l'acte de naissance ; le projet s'appelle
aujourd'hui Drave, et la vision complète est dans [`docs/theorie/vision.md`](docs/theorie/vision.md).

## Le cœur : des listes, pas des matrices

Un moteur classique multiplie une matrice par un vecteur : il lit tous les poids, pour tous les jetons, et jette ce
qui ne compte pas. Ici, la représentation est l'inverse :

- une activation est un **fait** — « le neurone 2 539 de la couche 23 a valu 27,8 » — et non une case dans un
  tableau ;
- les faits d'une même couche forment une **liste valuée**, groupée **par source** ;
- la liste est **poussée** vers ses destinations (chaque neurone actif connaît ses lecteurs), au lieu d'être tirée
  par chaque ligne de poids — c'est l'**AER** des architectures neuromorphiques (*Address Event Representation*).

Conséquence : **le coût du calcul devient proportionnel à l'activité, pas à la taille du modèle.** Un modèle plus
gros n'est plus mécaniquement plus lent à densité constante ; un modèle plus creux n'est plus lu en entier.

*Ce que la mesure impose de dire tout de suite* : la sparsité ne gagne pas toujours. En dessous d'environ **22 % de
densité**, le push (listes) bat le pull (matvec dense) ; au-dessus, le dense gagne. Le moteur garde **les deux
chemins** et choisit par la mesure — et le chemin par listes a ses propres portes : le rejeu d'une trace redonne la
même perplexité à **+0,074 %** près.

---

## Les cinq axes de la vision

### Axe 1 — Observer et régler le modèle, neurone par neurone

Un flux de listes est **observable par construction** : on peut compter, tracer, comparer, sans rien reconstruire.
Les mesures ont déjà appris des choses invisibles autrement : le **top 10 %** des neurones portent **33,1 %** de la
magnitude, et seuls **0,08 %** sont « chauds » plus de 90 % du temps — donc un préchargement statique ne paie pas,
alors qu'un cache dynamique, si. Un flux dit quels experts se réveillent, quels blocs une sélection garde, quelles
rangées d'une table sont touchées : **le journal n'est pas un sous-produit, c'est l'instrument de réglage**.

### Axe 2 — Répartir sur les composants d'une machine

C'est l'axe le plus avancé, et il est mesuré :

| ce qui est réparti | où | gain mesuré |
|---|---|---|
| cache KV d'une couche | VRAM (paginée, deux cartes) | attention à 1 M de clés : 968 → **13,2 ms** |
| attention complète | noyau GPU (décodage et préremplissage) | 22,16 → **3,29 ms/jeton** (÷6,7) |
| projections Q8_0 (> 8 Mo) | GPU, opt-in | tête : 15,6 → 6,2 ms/jeton |
| tête Q6_K | GPU | 7,58 → **3,60 ms/jeton** |
| cache KV (hôte) | pagination à la demande | contexte 1 M : **0,03 Go** au lieu de 25,77 Go |

La règle : **on place un opérateur là où son flux coûte le moins cher**, et on le vérifie.

### Axe 3 — Répartir sur plusieurs machines

**Le transport existe** : deux processus se passent des flux (protocole **v5**, modes dense / listes / blocs / lot
dense / lot en listes), le découpage est **fidèle au bit près** (`0,00e0`), et le préremplissage par lots tient en un
aller-retour par lot. **Une liste est une unité de travail autonome** — distribuer, c'est router des listes. Les
mesures faites : **1 608 octets** par flux à 256 jetons, 0,25 Mbit/s, latence ≤ 20 ms. Et le fait qui commande le
placement : **2,669 Go de poids par jeton** contre **65 536 octets** d'activation à une coupure — quatre ordres de
grandeur, donc **le placement suit les poids**, pas les flux.

Ce qui reste : l'ordonnanceur de placement, la granularité par bloc, et la démonstration distante.

### Axe 4 — Rejouer, comparer, ne pas régresser

Un flux est un **journal**, et un journal se rejoue. Les portes de non-régression (Qwen ctx 256 = **19,3885**,
gpt-oss = **15,6017**) exigent que deux chemins d'exécution rendent le même résultat ; les parties validées contre une
**référence indépendante** (MLA à 5,2e-7 contre numpy, 0,999024 contre llama.cpp) montrent la méthode. Ce que cela
ouvre : le **diff par couche** — après un changement de quantification ou de noyau, savoir *où* le calcul diverge, et
non seulement *qu'il* diverge.

### Axe 5 — Formats, matériels, énergie

La représentation par listes valuées impose ses formats, et ils sont là : listes par source avec échelle par bloc de
32 (Q8_0, Q4_K, Q6_K, MXFP4), KV quantifié int8/int4, et des noyaux pour **trois matériels** (SIMD x86, PTX sur
Quadro, logique FPGA). Deux chiffres qui comptent : l'int8 sur le cache KV coûte **+1,5 %** de perplexité à 512
jetons et **+3,0 %** à 8 192, là où l'int4 coûte **+364 %** — le débat n'est pas « combien de bits » mais **où sont
les échelles** ; et la densité d'activation (**17,9 %** sur Qwen2.5-0.5B) est l'argument énergétique : **on ne lit
que ce qui parle**.

---

## L'intelligence : deux étages, par-dessus les flux

La vision des flux ne dit pas seulement comment **exécuter** un modèle ; elle dit comment **l'observer** — et c'est
là que la recherche sur l'intelligence intervient. Deux étages :

1. **L'entrée-sortie linguistique** — lire et produire toutes les langues, dans tous les registres. On la juge en
   **qualité de traducteur** : la traduction est-elle fidèle, et le sens passe-t-il ?
2. **La pensée abstraite** — lire l'**état** interne du modèle (le vecteur qu'il calcule après avoir lu un texte) et
   voir ce qu'il porte : le sens, la composition, le raisonnement — et si c'est **indépendant de la langue**.

*Le pont entre les deux est la même idée que le moteur : une représentation faite de faits, qu'on peut lire. On ne
demande pas au modèle d'écrire sa réponse ; on la lit dans son état, avec une sonde — un classifieur linéaire aussi
simple que possible.*

## Ce qu'on a trouvé récemment (20/11)

**Le produit est utilisable.** `drave analyser` lit un texte, en français ou en anglais, et rend
la langue, les classes de mots, les groupes (sujet, verbe, complément) et **à quoi chaque groupe
se rattache** — le tout **hors ligne, sur CPU, en 0,8 s pour 10 000 mots**. Il s'installe
(`pip install -e .`), se mesure (`drave evaluer`) et se rejoue à l'identique (`drave rejouer`).
Sur le gold de 612 phrases : POS **86,25 %**, segmentation F1 **0,79**, attachement **99,58 %**.
Avec l'option `--tagger` (l'API DeepSeek), le POS monte à **95,75 %** pour ~0,02 $ les 612 phrases.

**Le modèle natif apprend, mais ne compose pas encore.** Le petit modèle maison (34 M) a une
perplexité de 2,40 sur son corpus ; il **écrit des mots réels** (87 %) mais **répète** (la
cohérence s'arrête à ~3 mots). Un modèle **100 M**, entraîné 10× moins longtemps, fait **mieux**
(88 % de mots, répétition ÷2,5) : **l'échelle paie**, et c'est le prochain chantier.

**Ce qu'on ne sait pas encore.** Le modèle natif ne tient pas une phrase ; la génération reste un
prototype. C'est mesuré, écrit, et le plan est dans [`natif-plan.md`](docs/pilotage/natif-plan.md).

## Ce qu'on a trouvé (expliqué sans jargon)

**1. Traduire : correct, jamais parfait.** Sur 532 langues de l'UDHR, 398 sont détectées à 96,87 % ;
l'allemand et l'arabe portent ; le chinois et le coréen restent faibles. La traduction marche
(34,0 % exacte sur 8 langues), mais c'est le **domaine** qui la fait progresser, pas le volume.

**2. Le raisonnement est déjà là.** Sur une énigme de positions, une simple lecture des nombres
internes retrouve la bonne réponse **100 fois sur 100** (2 personnes) et **51/100** (6) — le hasard
est à 5. L'information est dans l'état, avant l'écriture.

**3. Le français et l'anglais sont rangés différemment.** Un détecteur entraîné en français tombe
au hasard en anglais (5,8 %) ; un **pont** (une grille de conversion apprise) le remonte à 100 %
(2 personnes), 46 % (6). Il marche sur d'autres langues et d'autres relations — mais **doit rester
simple** : un réseau plus puissant fait moins bien.

**4. On peut apprendre au modèle à ranger ses deux langues ensemble.** Entraîné sur les deux, le
détecteur lit l'anglais à 65,6 % ; avec l'objectif contrastif, 74,2 % (plafond 75,3 %). Le prix :
le modèle devient un peu moins bon dans sa propre langue (98,7 → 77,6 %).

**5. Mais le fil d'une histoire ne se traduit pas.** Deviner la 5ᵉ phrase d'une histoire : 43 % en
français, et **aucune** méthode ne transfère à l'anglais. C'est le **contre-exemple** qui donne sa
valeur au pont.

**6. Sur de vraies phrases, le même schéma.** Sur XNLI (2 490 paires réelles), le détecteur lit la
réponse à 69 % (fr) / 78 % (en) contre 33 % au hasard ; le pont transfère à 83 %.

**En une phrase.** L'intelligence d'un modèle est **dans ses nombres internes**, pas seulement dans
ce qu'il écrit ; ces nombres sont **rangés différemment selon la langue**, mais une **grille simple**
relie les deux ; certaines capacités, comme le fil d'une histoire, restent **collées à la langue**.
La taille n'est pas le levier : la structure, si.

## Comment on le sait (et pourquoi on peut nous croire)

1. **Le juge doit être neuf.** Le banc initial (la Déclaration des droits de l'homme) était dans les données
   d'entraînement : le modèle **récitait** au lieu de traduire. Toutes les mesures ont été refaites sur un texte
   postérieur.
2. **Toujours un plancher et un contrôle.** La qualité se mesure en **marge** au-dessus de « recopier la source » ;
   chaque expérience a son **contrôle négatif** (paires mélangées, étiquettes mélangées) et son intervalle. Une
   référence **minée** (et non humaine) gonfle la marge : on l'a vu et corrigé.
3. **Ce qui pourrait le rendre faux est écrit à côté.** Six erratums ont retiré des mesures après coup — dont un bug
   de carte des lignes qui avait fait croire à une « falaise » du raisonnement. Les mesures retirées restent dans la
   fiche.

La méthode complète et ses sept leçons : [`docs/theorie/synthese/06-comment-savoir.md`](docs/theorie/synthese/06-comment-savoir.md).

---

## Ce que contient le dépôt

| vous cherchez… | allez à |
|---|---|
| **l'état courant** (ce qui est vrai aujourd'hui) | [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) |
| **la vision complète** (les cinq axes, ce qu'elle n'est pas) | [`docs/theorie/vision.md`](docs/theorie/vision.md) |
| **la roadmap** (les quatre chantiers A/B/N/R, l'ordre, la file « jamais en attente ») | [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) |
| **les résultats**, mesure par mesure, avec les contrôles | [`reports/README.md`](reports/README.md) · [`reports/`](reports/) |
| **la théorie** (8 chapitres) et la carte du raisonnement | [`docs/theorie/synthese/index.md`](docs/theorie/synthese/index.md) · [chap. 5](docs/theorie/synthese/05-la-pensee-sans-verbaliser.md) |
| **la méthode** et ses pièges | [`docs/theorie/synthese/06-comment-savoir.md`](docs/theorie/synthese/06-comment-savoir.md) |
| le **récit daté** de la recherche | [`journal/`](journal/) |
| les **instruments** (les expériences sont rejouables) | [`tools/`](tools/) |
| le **serveur de documentation** (sous-module) | [`tools/docwatch/`](tools/docwatch/) · [dépôt public](https://github.com/stephanedenis/docwatch) |
| les **corpus** | [`data/`](data/) (non versionné) |
| le **moteur d'inférence** (Rust) | [`drave-core/`](drave-core/) |
| l'**état des capacités du moteur** (archive) | [`docs/archive/etat-cerveau.md`](docs/archive/etat-cerveau.md) |
| les **règles de travail** du dépôt | [`AGENTS.md`](AGENTS.md) |

**Sous-module.** `tools/docwatch/` est un dépôt Git indépendant, épinglé comme sous-module. Après un clone :
`git submodule update --init --recursive`. Les évolutions de l'outil se font dans ce dépôt, puis le pointeur est
commité dans Drave.

**Le vocabulaire, en trois lignes** : une **couche** est une couche de neurones ; un **étage** est un niveau
d'architecture (étage 1 entrée-sortie, étage 2 pensée) ; une **unité de sens** est un élément de la représentation
neutre (la « RSN »), jamais un « jeton » de tokeniseur. Le glossaire : [`docs/theorie/glossaire.md`](docs/theorie/glossaire.md).

## Par où commencer

0. [`docs/theorie/carte.md`](docs/theorie/carte.md) — **la carte** : trouver un sujet (un concept, un chantier, une phase)
   directement, fichier par fichier ;
1. [`docs/theorie/vision.md`](docs/theorie/vision.md) — la vision complète (le cœur et les cinq axes) ;
2. [`AGENTS.md`](AGENTS.md) — la mission et les règles non négociables ;
3. [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) — l'état courant, daté ;
4. [`docs/theorie/synthese/05-la-pensee-sans-verbaliser.md`](docs/theorie/synthese/05-la-pensee-sans-verbaliser.md) — la carte du
   raisonnement, si c'est l'étage 2 qui vous intéresse.

Pour rejouer : les outils sont dans [`tools/`](tools/), et chaque résultat a son JSON dans `reports/`. Les portes de
qualité du dépôt :

```bash
python3 tools/revue_documentation.py   # classement, structure, fraîcheur, cohérence, vocabulaire
bash tools/porte-tableaux.sh           # liens, tableaux, date de la page vivante
bash tools/toutes-les-portes.sh        # toutes les portes (~1 h)
```

## Ce qui est fait, et ce qui reste ouvert

**Fait, mesuré** : le moteur (A7, B4, A8), la restitution par famille (C3.2), les jeux symboliques (B5/B6),
les 71 langues et les maîtres (B7/B8), le banc externe (B9), le protocole sémantique (B10), la base typée (B11)
et les modules cerveau-langage (B12). S'y ajoutent, mesurés les 17 et 18/11 : le **contrat d'implémentation**
du format DRVM (`impl` + `contrat`, routes conditionnelles, deux moteurs d'accord à 3e-7, le profil `court`
à 0,694×) ; le **tagger API à 0,9572** contre 0,8625 hors ligne (+9,47, pour deux centimes les 612 phrases) ;
le **corpus natif épinglé** (sha256, manifeste `fae5bb73…` ; la validation change le chiffre : 4,0139 ou
4,6792) ; la **courbe du 73 M** (3 000 → 33 000 pas : PPL 4,6792 → 3,1317, top-40 0,551 → 0,870, le greedy
qui boucle) ; **A2.6** (bande des experts 7,0 Go/s, tête Q8_0 dans la règle) ; **P1** (la dispersion GPU
29,37 G év/s bat la projection FPGA de 19,3 G). Les **chiffres, les contrôles et les négatifs**
— y compris le seuil de distillation 9,23–9,96 M, le meilleur écart 4,40 % (31,63 M / 610 ex.), la fenêtre 610/20 à 500 pas et le négatif 910/30 — sont dans
[`reports/README.md`](reports/README.md) ; l'**état** dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; le **plan**
dans [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md). Ces pages sont **facultatives** : on ne les charge que pour la tâche.

**Reste ouvert, bloqué par le dehors** :
- **La prose scientifique** : le corpus parallèle humain manque.
- **Le pic du 32 B** : nommé, non mesuré (10-20 h en 4 bits) — la tendance est établie par trois courbes.
- **Les langues peu dotées** hors périmètre ; la démonstration distante (le compte Colab).
- **Le FPGA** : le matériel existe (4 cartes + ring 40G, et P1 est clos — le débit ne le justifie pas) ; il
  reste **P2** (le ring tient-il 4,8 Go/s ?) et le programme RTL, quand le rig sera prêt.
- **La donnée du natif** : 7,5 Go de français disponible, mais ~98 % Wikipédia ; la déduplication par ligne
  (≈ 600 Mo) et la **diversité** (des livres) restent à faire.

---

*Un résultat qui n'a pas de contrôle négatif n'est pas un résultat.*

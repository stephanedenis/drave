# Drave

**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Un moteur qui traite les
activations d'un réseau de neurones comme des **faits** — « le neurone 2 539 de la couche 23 a valu 27,8 » — et non
comme des cases dans une matrice. Le coût du calcul devient proportionnel à l'**activité**, pas à la taille du
modèle ; le modèle devient **décomposable**, **répartissable** sur du matériel divers, et **observable** — on peut le
tracer, le rejouer, le comparer.

*« Stream of logs » : le flux des listes. Et « la drave » — ces billots qu'on confiait à la rivière au printemps,
qu'on guidait de l'estacade jusqu'à la scierie. Le nom dit ce que fait le moteur : il ne lit pas des matrices, il
conduit un flux.*

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
aujourd'hui Drave, et la vision complète est dans [`docs/vision.md`](docs/vision.md).

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

## Ce qu'on a trouvé (expliqué sans jargon)

Six résultats. Les mots techniques sont définis en passant ; les chiffres sont là pour être vérifiés, pas pour
impressionner.

### 1. Traduire : correct, jamais parfait

**Le test.** Un vrai règlement européen de 2025, que le modèle n'a jamais vu, avec sa traduction humaine officielle.
On lui fait traduire le texte, puis on compare sa sortie à la traduction humaine **caractère par caractère** — une
note de 0 à 100, comme une dictée corrigée lettre par lettre.

**Le repère qui compte.** Si on se contente de **recopier la phrase source sans traduire**, on obtient déjà **20 à 35
sur 100** (le français et l'anglais partagent des mots et des lettres). Le modèle obtient **55 à 76** : il traduit
donc vraiment, avec une avance de **30 à 40 points** sur la simple copie.

**Ce que ça dit.** Le modèle est meilleur sur la presse et les discours préparés, plus faible sur la **littérature**
(le style, les images) et la **prose technique** (longue et dense). Et **doubler la taille** (de 7 à 14 milliards de
paramètres) n'apporte qu'**un point de plus** : la taille n'est pas le levier principal.

### 2. Le raisonnement est déjà dans la tête du modèle

**La devinette.** « Alice est devant Bob. Bob est devant Carl. Qui est devant tout le monde ? » Les phrases sont
mélangées : il faut les remettre en ordre pour répondre.

**Le tour de passe-passe.** On ne demande **pas** au modèle d'écrire sa réponse. On lit directement **les nombres
internes** qu'il calcule après avoir lu (son « état »), avec un détecteur volontairement simple : une règle de calcul
linéaire, comme une balance à plusieurs plateaux.

**Pourquoi c'est étonnant.** Ce détecteur retrouve la bonne réponse **100 fois sur 100** pour deux personnes, **51
fois sur 100** pour six — alors que le hasard est à **5**. Autrement dit : **l'information est déjà là, avant
l'écriture**. Le modèle a « compris » la chaîne, même s'il ne l'a pas encore dite. C'est tout le sens de « penser
sans verbaliser ».

### 3. Le français et l'anglais sont rangés dans deux espaces différents

**L'expérience.** On entraîne le détecteur en français, puis on le fait lire **l'anglais** : il tombe à **5,8 %**,
c'est-à-dire le hasard. Ce n'est pas que l'anglais manque d'information : c'est que les nombres internes sont
**organisés autrement**. Image : deux bibliothèques qui possèdent les mêmes livres, mais les rangent selon deux
systèmes incompatibles — le catalogue de l'une ne sert pas dans l'autre.

**La solution.** Un **pont** : une **grille de conversion** (une simple règle linéaire, apprise sur des phrases dont
on possède la version française et anglaise). Cette grille transforme les nombres anglais en nombres « à la
française » ; le détecteur français lit alors l'anglais : **100 %** pour 2 personnes, **91 %** pour 3, **68 %** pour
4, **52 %** pour 5, **46 %** pour 6.

**Ce que le pont n'est pas.** Une baguette magique. Il **marche** pour d'autres relations (comparer des tailles),
pour d'autres langues (l'espagnol, l'allemand, et même l'**arabe** — autre famille, autre écriture), à d'autres
couches du réseau, jusqu'à **12 personnes**, et à toutes les échelles testées (3, 7 et 14 milliards de paramètres).
Il **doit rester simple** : un réseau de neurones plus puissant fait **moins bien** — la grille linéaire suffit, et
c'est ce qui rend l'idée élégante.

### 4. On peut apprendre au modèle à ranger ses deux langues ensemble

**L'expérience.** Le pont est une pièce rapportée. On a donc **entraîné le modèle lui-même** sur les deux langues à
la fois : le détecteur français lit alors l'anglais à **65,6 %**. Mieux : en montrant au modèle la phrase française
et son équivalent anglais **côte à côte**, en lui demandant de rapprocher leurs nombres internes (l'« objectif
contrastif »), on monte à **74,2 %**. Au-delà, plus de progrès : **75,3 %**, c'est le plafond de cette méthode.

**Le prix.** Le modèle devient un peu moins bon **dans sa propre langue** (le détecteur français passe de 98,7 % à
77,6 %). Comme un bilingue qui mélange un peu ses deux langues : l'alignement a un coût, et il est mesurable.

### 5. Mais le fil d'une histoire, lui, ne se traduit pas

**L'expérience.** On donne au modèle les **quatre premières phrases** d'une histoire et on lui demande de **deviner
la cinquième** parmi huit candidates (une sur huit au hasard). Pour réussir, il doit garder le **fil** du récit —
ce qu'on appelle le « plan ».

**Le résultat.** En français, le fil est là (43 % de réussite). Mais **aucune** des méthodes qui ont marché pour le
raisonnement ne le transfère à l'anglais : ni le pont, ni l'apprentissage bilingue, ni le contraste, ni une mémoire
récurrente. L'apparent transfert qu'on avait cru voir était un **artefact** : l'entraînement rendait simplement les
bonnes réponses françaises plus faciles à retrouver, sans aligner les langues.

**Pourquoi c'est important.** C'est le **contre-exemple** qui donne sa valeur au pont. Toutes les capacités ne se
rangent pas de la même façon ; le pont n'est pas une clé universelle, et le dire est plus utile que de le croire.

### 6. Sur de vraies phrases, le même schéma

**Le test.** Les énigmes précédentes sont fabriquées. On a donc refait le travail sur **XNLI**, un corpus de **vraies
phrases** (2 490 paires français/anglais) : on donne une affirmation et une conséquence possible, et il faut dire si
elle est **vraie, fausse ou indécidable**.

**Le résultat.** Le détecteur lit la réponse dans l'état : **69 % en français, 78 % en anglais** (le 1,5 B), contre
**33 %** au hasard ; le **pont** transfère à **83 %**. Et le 3 B, à sa meilleure couche, lit **87 %** (le 1,5 B 81 % à la sienne) : *la lecture dépend du point de mesure
autant que du modèle ; la sonde mesure l'accès à l'état, pas la qualité.*

**Ce que ça dit.** Le schéma du pont n'est pas un artefact des énigmes : il tient sur du langage réel. Et le même
enseignement que la traduction : **c'est le domaine qui compte, pas le volume** — 13 394 paires d'entraînement
prises ailleurs n'ont pas amélioré la lecture, alors que des données du bon domaine, si.

### En une phrase

L'intelligence d'un modèle est **dans ses nombres internes**, pas seulement dans ce qu'il écrit ; ces nombres sont
**rangés différemment selon la langue**, mais une **grille de conversion simple** — qu'on peut apprendre — relie les
deux ; et certaines capacités, comme le fil d'une histoire, restent **collées à la langue**. La taille n'est pas le
levier : la structure, si.

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

La méthode complète et ses sept leçons : [`docs/synthese/06-comment-savoir.md`](docs/synthese/06-comment-savoir.md).

---

## Ce que contient le dépôt

| vous cherchez… | allez à |
|---|---|
| **l'état courant** (ce qui est vrai aujourd'hui) | [`docs/en-cours.md`](docs/en-cours.md) |
| **la vision complète** (les cinq axes, ce qu'elle n'est pas) | [`docs/vision.md`](docs/vision.md) |
| **la roadmap** (les deux programmes, l'ordre, la file « jamais en attente ») | [`docs/roadmap.md`](docs/roadmap.md) |
| **les résultats**, mesure par mesure, avec les contrôles | [`reports/07-mesures-couche-commune.md`](reports/07-mesures-couche-commune.md) · [`reports/`](reports/) |
| **la théorie** (7 chapitres) et la carte du raisonnement | [`docs/synthese/index.md`](docs/synthese/index.md) · [chap. 5](docs/synthese/05-la-pensee-sans-verbaliser.md) |
| **la méthode** et ses pièges | [`docs/synthese/06-comment-savoir.md`](docs/synthese/06-comment-savoir.md) |
| le **récit daté** de la recherche | [`journal/`](journal/) |
| les **instruments** (les expériences sont rejouables) | [`tools/`](tools/) |
| les **corpus** | [`data/`](data/) (non versionné) |
| le **moteur d'inférence** (Rust) | [`drave-core/`](drave-core/) |
| l'**état des capacités du moteur** | [`docs/etat-cerveau.md`](docs/etat-cerveau.md) |
| les **règles de travail** du dépôt | [`AGENTS.md`](AGENTS.md) |

**Le vocabulaire, en trois lignes** : une **couche** est une couche de neurones ; un **étage** est un niveau
d'architecture (étage 1 entrée-sortie, étage 2 pensée) ; une **unité de sens** est un élément de la représentation
neutre (la « RSN »), jamais un « jeton » de tokeniseur. Le glossaire : [`docs/glossaire.md`](docs/glossaire.md).

## Par où commencer

0. [`docs/carte.md`](docs/carte.md) — **la carte** : trouver un sujet (un concept, un chantier, une phase)
   directement, fichier par fichier ;
1. [`docs/vision.md`](docs/vision.md) — la vision complète (le cœur et les cinq axes) ;
2. [`AGENTS.md`](AGENTS.md) — la mission et les règles non négociables ;
3. [`docs/en-cours.md`](docs/en-cours.md) — l'état courant, daté ;
4. [`docs/synthese/05-la-pensee-sans-verbaliser.md`](docs/synthese/05-la-pensee-sans-verbaliser.md) — la carte du
   raisonnement, si c'est l'étage 2 qui vous intéresse.

Pour rejouer : les outils sont dans [`tools/`](tools/), et chaque résultat a son JSON dans `reports/`. Les portes de
qualité du dépôt :

```bash
python3 tools/revue_documentation.py   # classement, structure, fraîcheur, cohérence, vocabulaire
bash tools/porte-tableaux.sh           # liens, tableaux, date de la page vivante
bash tools/toutes-les-portes.sh        # toutes les portes (~1 h)
```

## Ce qui est fait, et ce qui reste ouvert

**Fait, mesuré** : la **grappe déportée** (A7 : le relais **42,5477**, la grappe exacte à **21 %**, le transport à
**4,22×**), les **opérateurs abstraits** (B4 : les **six** mesures, jusqu'au LoRA qui **inverse**), l'**ordonnanceur
place et perte** (A8 : la règle branchée en **opt-in**), et la **restitution par famille** (C3.2 : 28 familles
découpées, le module par famille, la courbe sur 5 familles — **4 sur 5 au-dessus de la référence**, de 14,7 % à
100 %, le contrôle à 0 %).

**Reste ouvert, bloqué par le dehors** :
- **La prose scientifique** : le corpus parallèle humain manque.
- **Le pic du 32 B** : nommé, non mesuré (10-20 h en 4 bits) — la tendance est établie par trois courbes.
- **Les langues peu dotées** hors périmètre ; la démonstration distante (le compte Colab) et le FPGA (le matériel).

---

*Un résultat qui n'a pas de contrôle négatif n'est pas un résultat.*

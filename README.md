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

## Ce qu'on a trouvé

**Traduire : correct, jamais parfait.** Sur un texte neuf (un règlement européen de 2025, jamais vu à
l'entraînement), la qualité est de **55 à 76 sur 100**, soit une **marge de +30 à +40** au-dessus de « recopier la
source ». Les registres ne se valent pas : le littéraire est le plus dur (+25,9), la presse et le parlé préparé les
plus faciles (+38,6 / +39,8). La taille aide, mais de moins en moins (+0,9 entre 7 et 14 milliards). Le critère
démographique est tenu jusqu'au **français inclus** (20 langues), pidgin nigérian compris.

**Le raisonnement est déjà dans l'état.** « Alice est devant Bob. Bob est devant Carl. Qui est devant tout le
monde ? » — une sonde linéaire lit la réponse : **100 %** pour deux personnes, **51 %** pour six, contre 5 % de
hasard. **Le modèle compose sans écrire.**

**Mais les langues ne sont pas dans le même espace.** La sonde française ne lit pas l'état anglais (5,8 %). Un
**pont** — une simple carte linéaire apprise sur des phrases appariées — l'y ramène : **100 / 91 / 68 / 52 / 46 %**
pour 2 à 6 personnes. Ce pont marche pour d'autres relations, d'autres langues (dont l'**arabe**), à plusieurs
couches, jusqu'à **12 personnes**, et à **toutes les échelles** (0,81 à 0,975 de 3 à 14 milliards). Il doit rester
**linéaire** : un réseau plus puissant échoue.

**L'alignement peut s'apprendre.** Entraîné sur les deux langues, le modèle fait lire l'état anglais à **65,6 %** ;
avec un objectif contrastif, **74,2 %**, puis **saturation** (75,3 %). Le prix : l'in-langue baisse (98,7 % →
77,6 %). *La tête bien faite a un coût, et il est mesurable.*

**Le plan résiste.** Un état qui résume un contexte plus long (les 4 premières phrases d'une série) ne s'aligne pas :
ni les ponts, ni le bilinguisme, ni le contraste, ni la récurrence. Son transfert apparent venait d'un **effet côté
cible** — la tâche rend les cibles françaises plus faciles à retrouver, sans aligner les langues. *C'est le
contre-exemple qui donne sa valeur au pont.*

**Le naturel confirme.** Sur XNLI (2 490 paires traduites FR/EN), l'inférence est dans l'état (50 % / 58 % contre
33 %), le pont la transfère à **59 %**, et un fine-tuning à **75-77 %**.

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

## Ce qui reste ouvert

- **Le placement** : l'ordonnanceur qui décide où vit chaque grappe (aujourd'hui : des seuils réglés à la main).
- **La granularité par bloc** et la démonstration distante.
- **Le plan multi-tâches** : la seule variante non testée de l'étage 2.
- **La prose scientifique** : le corpus parallèle humain manque.
- **Le 32 B** et la profondeur au-delà de 12 personnes.
- **Les langues peu dotées** hors périmètre.

---

*Un résultat qui n'a pas de contrôle négatif n'est pas un résultat.*

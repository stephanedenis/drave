# Drave — la vision

> *« Stream of logs »* : le flux des listes. Et, en français d'ici, **la drave** —
> ces billots qu'on confiait à la rivière au printemps, qu'on guidait de
> l'estacade jusqu'à la scierie. Le nom dit exactement ce que fait ce moteur :
> il ne lit pas des matrices, il conduit un flux.

Ce document est la **vision** du projet : ce qu'il cherche, pourquoi la
représentation qu'il a choisie change la nature des problèmes, et ce que cela
ouvre sur chaque axe. Il ne remplace pas les rapports — chaque affirmation
mesurée renvoie à celui qui la porte — et il distingue partout ce qui est
**mesuré**, ce qui est **raisonné**, et ce qui est **à faire**.

Le projet s'appelait `Drave`, du nom de son origine : un cahier des charges
d'inférence ternaire sur un cluster de cartes Stratix V
(`Qtrinet-bootstrap.md`). Ce cahier des charges reste l'acte de naissance ; le
nom, lui, ne dit plus ce que le projet est devenu. **Drave** le dit.

---

## 1. Le cœur : des listes, pas des matrices

Un moteur d'inférence classique multiplie une matrice par un vecteur : il lit
tous les poids, pour tous les jetons, et jette ce qui ne compte pas. Ici, la
représentation est l'inverse :

* une activation est un **fait** — « le neurone 2 539 de la couche 23 a valu
  27,8 » — et non une case dans un tableau ;
* les faits d'une même couche forment une **liste valuée**, groupée **par source**
  (chaque source a sa table : les valeurs d'une même origine partagent leur
  échelle) ;
* la liste est **poussée** vers ses destinations (chaque neurone actif connaît
  ses lecteurs), au lieu d'être tirée par chaque ligne de poids — c'est
  l'**AER** des architectures neuromorphiques (*Address Event Representation*),
  d'où viennent les premières mesures du projet
  (`reports/rapport-cpu-aer.md`).

Conséquence directe, et c'est toute la vision : **le coût du calcul devient
proportionnel à l'activité, pas à la taille du modèle**. Un modèle plus gros
n'est plus mécaniquement plus lent à densité constante ; un modèle plus creux
n'est plus lu en entier.

### Ce que la mesure impose de dire tout de suite

Le projet ne prétend pas que la sparsité gagne toujours. Le croisement a été
**mesuré** : en dessous d'environ **10 % de densité**, le push (listes) bat le
pull (matvec dense) ; au-dessus, le dense gagne
(`reports/rapport-croisement-push-pull.md`). C'est pourquoi le moteur garde **les
deux chemins** et choisit par la mesure, pas par principe — `--dense` existe, et
les portes de non-régression tournent sur les deux.

La densité observée, elle, dépend du modèle et de la couche : **17,9 %** sur
Qwen2.5-0.5B à 512 jetons, mais les FFN denses de certaines familles ne sont pas
creux du tout (`reports/rapport-localite-activation.md`). Une vision honnête dit
où elle s'applique — et où elle ne s'applique pas.

---

## 2. Axe 1 — Voir et régler le modèle, neurone par neurone

Un flux de listes est **observable par construction** : on peut compter, tracer,
comparer, sans rien reconstruire.

Ce qui existe déjà, et qui a servi :

| outil | ce qu'il donne |
|---|---|
| `--profil-neurones`, `--neurones-sortie` | quels neurones s'allument, à quelle fréquence, avec quelle magnitude |
| `--profil-experts` | quels experts sont choisis (MoE), et à quel point le routage est concentré |
| `[config]` sur chaque exécution | quel chemin est **réellement** actif (rotation, cache KV, MLA, experts…) |
| `--ppl-profil` | le temps par poste (projections, rope, attention, FFN, tête) |
| journal de session | l'historique de tout ce qui a été mesuré, archivé à chaque commit |

Ce que ces mesures ont appris, et qui n'aurait pas été visible autrement :

* **top 10 % des neurones portent 33,1 % de la magnitude** ; seuls **0,08 %** sont
  « chauds » plus de 90 % du temps — donc un préchargement statique ne paie pas,
  alors qu'un cache dynamique, si ;
* `--attn-topk 256` **améliore** la perplexité (234,88 contre 298,56 à contexte
  2 048) : restreindre l'attention lointaine retire du bruit ;
* le capteur hebbien apprend des **journaux d'activation** eux-mêmes
  (`reports/rapport-capteur-hebbien.md`) — le flux n'est pas qu'un objet
  d'exécution, c'est une donnée d'apprentissage.

**Ce que la vision ajoute** : faire du flux un **objet de première classe** —
un format de trace stable, par couche et par neurone, qu'on puisse rejouer,
diffuser et comparer entre deux versions d'un modèle ou deux configurations du
moteur. Le débogage cesse d'être « la perplexité a bougé de 0,01 » pour devenir
« la couche 23 a changé de régime au jeton 4 096 ».

---

## 3. Axe 2 — Répartir sur les composants d'une machine

C'est l'axe le plus avancé, et il est **mesuré** :

| ce qui est réparti | où | gain mesuré |
|---|---|---|
| cache KV d'une couche | VRAM (paginée, sur **deux** cartes) | attention à 1 M de clés : 968 → **13,2 ms** par couche |
| attention complète | noyau GPU, décodage **et** préremplissage | 22,16 → **3,29 ms/jeton** (÷6,7) ; préremplissage **×2,8** |
| projections Q8_0 (> 8 Mo) | GPU, opt-in | tête : 15,6 → 6,2 ms/jeton |
| tête Q6_K | GPU | 7,58 → **3,60 ms/jeton** |
| experts MXFP4 | cache VRAM LRU | **+6 %** — mesuré, verdict : ne pas activer tel quel |
| cache KV (hôte) | pagination à la demande | contexte 1 M : **0,03 Go** au lieu de 25,77 Go |

La leçon de cet axe est une règle de placement : **on place un opérateur là où
son flux coûte le moins cher**, et on le vérifie. Le même raisonnement mène au
FPGA : le projecteur événementiel sur Stratix V existe et a été synthétisé
(`reports/rapport-pe-evenementiel.md`), et le bilan multi-matériel
(`reports/bilan-multi-materiel.md`) donne le cadre CPU / FPGA / GPU.

Ce qui reste ouvert : la **politique** de placement (aujourd'hui : des seuils
codés en dur, réglés à la main par la mesure) et le **déport du top-k** dans le
noyau d'attention — le dernier chemin qui retombe sur le CPU.

---

## 4. Axe 3 — Répartir sur plusieurs machines

**Rien n'existe ici, et c'est le chantier le plus prometteur du projet.** La
raison est dans la nature de la représentation : si le calcul est un flux de
listes adressées, alors **une liste est une unité de travail autonome**, avec ses
entrées (les activations), sa sortie (les activations produites) et sa
dépendance (les poids d'une couche). Distribuer, c'est router des listes.

Ce qu'il faut définir, dans l'ordre :

1. **le contrat d'échange** : une tranche de liste = un en-tête (couche, source,
   échelle, bits) + des paires (destination, valeur). Compact, vérifiable,
   versionné ;
2. **la granularité** : par couche ? par bloc de canaux ? par expert ? La mesure
   dira où le coût de sérialisation rattrape le gain de parallélisme — le
   croisement push/pull à 10 % donne déjà l'ordre de grandeur de ce qu'on
   transporte ;
3. **le placement** : la même règle qu'à l'axe 2, appliquée entre machines — un
   opérateur va là où son entrée est déjà, ou là où elle coûte le moins à
   amener ;
4. **ce qui ne se parallélise pas** : le décodage est **séquentiel** (un jeton
   dépend du précédent) ; c'est le **préremplissage** qui est parallèle par
   nature, et c'est donc là qu'il faut commencer ;
5. **les mesures à faire** : débit d'un flux sérialisé, latence aller-retour,
   taille moyenne d'une tranche par couche, et le point où le réseau coûte plus
   que le calcul économisé.

Cette section est une **hypothèse de travail**, pas un résultat. Elle est écrite
ici parce qu'aucun autre moteur ne peut l'aborder aussi directement : dans une
architecture par matrices, l'unité de travail est une matrice entière — dans une
architecture par listes, c'est une poignée de faits.

---

## 5. Axe 4 — Rejouer, comparer, ne pas régresser

Un flux est un **journal**, et un journal se rejoue.

* les **portes de non-régression** du dépôt (Qwen ctx 256 = **19,3885**,
  gpt-oss ctx 256 = **15,1757**) sont l'application minimale de cette idée :
  deux chemins d'exécution doivent rendre le même résultat ;
* les tranches du projet qui ont été validées contre une **référence
  indépendante** (MLA à **5,2e-7** contre numpy ; vision : patchs 5,4e-7,
  projecteur 1,7e-6) montrent la méthode : une seconde implémentation de la même
  formule, pas une seconde exécution de la même implémentation ;
* l'enregistrement du flux permettrait le **diff par couche** : après un
  changement de quantification ou de noyau, savoir *où* le calcul diverge, et
  non seulement *qu'il* diverge.

Ce que cela demande : un format de trace stable, un coût d'écriture acceptable
(échantillonner les couches plutôt que tout tracer), et une règle claire — **on
ne trace pas ce qu'on ne relit pas**.

---

## 6. Axe 5 — Formats, matériels, énergie

La représentation par listes valuées impose ses formats, et ils sont déjà là :
listes **par source** avec échelle par bloc de 32 (`Q8_0`, `Q4_K`, `Q6_K`,
`MXFP4`), KV quantifié int8/int4 avec échelles par bloc, et des noyaux écrits
pour **trois matériels** (SIMD x86, PTX sur Quadro, logique FPGA).

Les chiffres qui comptent, du point de vue de la vision :

* l'int8 sur le cache KV coûte **+1,5 %** de perplexité à 512 jetons et
  **+3,0 %** à 8 192, là où l'int4 coûte +364 % — le débat n'est pas « combien de
  bits » mais **où sont les échelles** ;
* le dépaquetage vectorisé du noyau d'attention a fait passer le f32 de 13,6 à
  **7,0 ms** par couche à 1 M (308 Go/s, 69 % de la bande VRAM) : quand le
  format est bien lu, la mémoire cesse d'être le mur ;
* la densité d'activation (17,9 %) est l'argument énergétique : **on ne lit que
  ce qui parle**. C'est la même idée que l'AER neuromorphique, et c'est ce qui
  rend le FPGA intéressant pour autre chose que le débit brut.

---

## 7. Ce que la vision n'est pas

Pour que le document serve à quelque chose, il doit aussi refuser des choses :

* **ce n'est pas « le sparse gagne toujours »** : le croisement à 10 % de densité
  est mesuré, et le moteur garde le chemin dense ;
* **ce n'est pas « un neurone = une décision »** : le profiler montre qu'un petit
  nombre de neurones portent l'essentiel, et qu'un préchargement statique ne paie
  pas — le dynamisme est la condition, pas l'ornement ;
* **ce n'est pas « distribuer, c'est gratuit »** : l'axe 3 est une hypothèse,
  avec ses mesures à faire, et le décodage restera séquentiel ;
* **ce n'est pas une réécriture** : le moteur Rust actuel *est* cette
  architecture — Drave est le nom de ce qu'il fait déjà, pas un projet parallèle.

---

## 8. Feuille de route par axes

| axe | état | prochain pas |
|---|---|---|
| **1. Observer/régler par neurone** | outils en place, mesures faites | format de trace stable + diff par couche |
| **2. Répartir sur composants** | mesuré (KV, attention, tête, experts) | top-k dans le noyau GPU ; politique de placement réglée par la mesure |
| **3. Répartir sur machines** | **rien** — hypothèse écrite | contrat d'échange, granularité, mesures de débit |
| **4. Rejouer/comparer** | portes de non-régression + références indépendantes | enregistrement du flux, diff |
| **5. Formats/matériels/énergie** | trois matériels, formats au point | politique de quantification par bloc *choisie* par la mesure, pas par défaut |

---

## 9. Le nom

**Drave** : le flux qu'on conduit, du bassin de flottage jusqu'à la scierie. Le
mot porte les trois propriétés que ce document essaie de décrire — il **coule**
(les listes avancent), il se **répartit** (les billots se séparent aux fourches),
et il **se surveille** (on compte, on trie, on redirige).

**Le renommage est fait** (2026-09-30), et partout : crate `drave-core`, binaire
`drave`, variables `DRAVE_*`, noyaux `drave_gpu.*`, et « Drave » dans les rapports
comme dans les documents.

Trois choses ont été **préservées**, délibérément : le **journal de sessions**
(un journal réécrit n'est plus un journal), le **cahier des charges d'origine**
`Qtrinet-bootstrap.md` (une pièce datée), et l'**historique Git**.

La table de conversion des anciens noms — variables `QT_*`, chemins — est dans
[`docs/histoire.md`](histoire.md), avec l'histoire des trois âges du projet : le
Qtrinet ternaire des cartes Stratix V, le virage événementiel, et Drave. Les
anciennes variables ne font plus rien, mais le moteur **le dit** au lieu de
laisser croire qu'une option est active.

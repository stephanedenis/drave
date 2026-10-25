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

Le projet s'appelait `Qtrinet`, du nom de son origine : un cahier des charges
d'inférence ternaire sur un cluster de cartes Stratix V
(`Qtrinet-bootstrap.md`). Ce cahier des charges reste l'acte de naissance ; le
nom, lui, ne dit plus ce que le projet est devenu. **Drave** le dit.

## La raison d'être — et ce que 173 mesures en ont fait

**Drave existe pour démontrer que la structure bat la taille, et pour construire le moteur qui rend cette structure
observable, décomposable, répartissable et rejouable.**

Ce n'est plus une hypothèse de travail : c'est un **résultat mesuré**. Sur le raisonnement naturel, **la sonde est
plate dès le 1,5 B** (0,7256 / 0,7269 / 0,7189 / 0,7376 à leurs pics : **dix fois la taille pour +0,001**) et **le
pont plafonne à 0,87** ; à profondeur fixe (50 %), le 32 B mène (0,5997) mais le 14 B est **dernier** (0,4833) — et
le même 14 B, à 67 %, devient le meilleur (0,6305). **La taille ne garantit pas la lisibilité ; la profondeur décide
autant que le modèle**, et ce qui reste est la **structure**.

Le projet s'est donné trois moyens, et il les a mesurés :

1. **la représentation** — des listes valuées, pas des matrices : le coût suit l'activité (le top-k fusionné, le
   diff par couche, la trace rejouable) ;
2. **l'alignement** — un pont linéaire transfère l'état d'une langue à l'autre (0,826 → 0,857 → 0,870) sans
   entraîner le modèle ;
3. **la répartition** — la règle `choisir` place le KV (4 tests), et la porte de la greffe montre que l'injection
   d'état est **branchée**.

**Ce que les mesures ont refusé** — et c'est aussi la raison d'être : apprendre des flux (les produits hebbiens
**+0,0045** de R², aucun neurone mort à élaguer), le 4 bits de la tête (**+10 %** de PPL), la course à l'échelle (le
pic du 32 B coûte 10-20 h et ne tranche plus rien). *Le projet n'est pas « plus de paramètres » : il est **plus de
structure, mesurée**.*

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
**mesuré** : en dessous d'environ **22 % de densité**, le push (listes) bat le
pull (matvec dense) ; au-dessus, le dense gagne
(`reports/rapport-croisement-push-pull.md`). C'est pourquoi le moteur garde **les
deux chemins** et choisit par la mesure, pas par principe — `--dense` existe, les
portes de non-régression tournent en dense (`tools/portes.sh`), et le chemin par
listes a les siennes : **le rejeu d'une trace redonne la même perplexité à
+0,074 % près** (19,4029 contre 19,3885) et l'écart d'activation entre le calcul
et la trace est de **1,5e-5** (`REPRISE.md` §6, `DRAVE_FLUX_VERIF=1`).

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
| `--profil-neurones` | quels neurones s'activent, couche par couche (le `--profil-experts` d'origine n'existe pas) |
| `[config]` sur chaque exécution | quel chemin est **réellement** actif (rotation, cache KV, MLA, experts…) |
| profil par poste | `--ppl` imprime le temps par poste (projets-attn, rope, attention, proj+mlp, tête) et, pour V4, ses cinq sous-postes. `--ppl-profil` imprime en plus la **perte par tranche de 256 positions** — le drapeau manquait (le champ était lu par le code, aucune branche CLI ne le remplissait : `reports/rapport-drapeaux-ignores.md`) ; il a été branché le 03/10 au bloc 19 |
| journal de session | l'historique de tout ce qui a été mesuré, archivé à chaque commit |

Ce que ces mesures ont appris, et qui n'aurait pas été visible autrement :

* **top 10 % des neurones portent 33,1 % de la magnitude** ; seuls **0,08 %** sont
  « chauds » plus de 90 % du temps — donc un préchargement statique ne paie pas,
  alors qu'un cache dynamique, si (`reports/rapport-localite-activation.md`) ;
* `--attn-topk 256` **améliore** la perplexité (**gpt-oss**, contexte 2 048, mêmes
  512 jetons notés : 234,88 contre 298,56 — `docs/contexte-long.md` §6) :
  restreindre l'attention lointaine retire du bruit ; l'écart A/B fait foi, la
  valeur absolue dépend des réglages et n'a pas été reproduite depuis
  (`docs/plan-gpu-topk.md`) ;
* le capteur hebbien apprend des **journaux d'activation** eux-mêmes
  (`reports/rapport-capteur-hebbien.md`) — le flux n'est pas qu'un objet
  d'exécution, c'est une donnée d'apprentissage.

**Ce que la vision ajoute** : faire du flux un **objet de première classe** —
un format de trace stable, par couche et par neurone, qu'on puisse rejouer,
diffuser et comparer entre deux versions d'un modèle ou deux configurations du
moteur. Le débogage cesse d'être « la perplexité a bougé de 0,01 » pour devenir
« la couche 23 a changé de régime au jeton 4 096 ».

Et, au-delà du débogage : **lire ces flux pour comprendre le modèle et adapter
l'architecture à la tâche**. Un flux dit quels experts se réveillent, quels blocs
une sélection garde, quelles rangées d'une table sont touchées — et une
architecture qui se règle sur ces mesures n'est plus choisie une fois pour
toutes. C'est la finalité d'un moteur qui conduit des listes : le journal n'est
pas un sous-produit, c'est l'instrument de réglage.

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

Sources de ce tableau : `docs/contexte-long.md` (KV paginé, attention GPU),
`reports/rapport-session-2026-09-30.md`, `REPRISE.md` §6.

La leçon de cet axe est une règle de placement : **on place un opérateur là où
son flux coûte le moins cher**, et on le vérifie. Le même raisonnement mène au
FPGA : le projecteur événementiel sur Stratix V existe et a été synthétisé
(../../FPGA-Stratix-V/docs/rapport-pe-evenementiel.md), et le bilan multi-matériel
(`reports/bilan-multi-materiel.md`) donne le cadre CPU / FPGA / GPU.

**Ce qui est fait, et ce qui reste ouvert.** Le **déport du top-k** dans le noyau
d'attention est **fait** : le noyau fusionné tient un lancement par ligne et le
seuil de bascule (131 072 clés) est mesuré — le dernier repli CPU est levé en
opt-in. La **politique de placement** a sa règle (`placement.rs`, `choisir`, 4
tests) ; reste l'**ordonnanceur complet**, qui doit porter **la place et la
perte** — la tête l'a montré, le 4 bits « qui tient » coûte +10 % de perplexité.

---

## 4. Axe 3 — Répartir sur plusieurs machines

**Le transport existe, et c'est l'axe où le projet a le plus avancé depuis.**
Deux processus se passent des flux (protocole **v5** : version, modes dense /
listes / blocs / **lot dense** / **lot en listes**, contrat d'activation complet),
le découpage est fidèle au bit près (`0,00e0`), le préremplissage par lots tient en un aller-retour par lot, et
`colab/` contient de quoi faire la démonstration sur un runtime distant. Ce qui
reste : l'ordonnanceur de placement, le flux de poids depuis le NVMe, et la
granularité par bloc. La
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
   croisement push/pull à ~22 % donne déjà l'ordre de grandeur de ce qu'on
   transporte. **Mesuré le 03/10 (`reports/rapport-granularite-flux.md`)** : à
   erreur ÉGALE, une seule liste par flux est **la plus compacte** (43,3 % du dense
   f32 à 10 % d'erreur, contre 58-68 % dès qu'on découpe en 4, 16, 64 ou 512
   listes) — l'en-tête (14 o par liste) et la perte de l'échelle globale coûtent
   plus que ce que la finesse rapporte en octets. **La granularité ne compresse
   pas, elle ROUTE** : une unité ne reçoit que ses listes, une tranche d'énergie
   négligeable coûte 0 octet, et à seuil égal une tranche fine a une erreur plus
   faible (0,244 à G = 1 contre 0,030 à G = 512). Et le fait qui commande le
   placement est ailleurs : **2,669 Go de poids par jeton** (V4-Flash) contre
   **65 536 octets** d'activation à une coupure — quatre ordres de grandeur, donc
   **le placement suit les poids**, pas les flux d'activation ;
3. **le placement** : la même règle qu'à l'axe 2, appliquée entre machines — un
   opérateur va là où son entrée est déjà, ou là où elle coûte le moins à
   amener ;
4. **ce qui ne se parallélise pas** : le décodage est **séquentiel** (un jeton
   dépend du précédent) ; c'est le **préremplissage** qui est parallèle par
   nature, et c'est donc là qu'il faut commencer ;
5. **les mesures faites** : **1 608 octets** par flux à 256 jetons, 0,25 Mbit/s,
   latence aller-retour jusqu'à 20 ms, attente ≈ calcul distant + 3,2 × latence
   (`docs/roadmap.md`) ; restent la granularité par bloc et le point où le réseau
   coûte plus que le calcul économisé ;
6. **ce que le flux coûte selon l'architecture** : un modèle à
   **hyper-connexions** (DeepSeek-V4) porte son état résiduel en `hc` copies —
   son flux de coupure fait donc **`hc` fois** la taille d'un état ordinaire
   (4 × 4 096 = 16 384 canaux pour V4-Flash, 64 Ko par flux en f32). Ce n'est
   pas une hypothèse : réduire les copies au point de coupure change le modèle
   (perplexité répartie 8 311 → 34 159, écart 3,11 alors que le transport est
   exact), donc **le découpage d'un tel modèle est refusé** tant que le
   protocole ne transporte pas les copies. Corollaire pour la suite : à flux
   égal, un modèle à hyper-connexions se découpe **plus près du calcul**.

Cette section mêle un **acquis** (le transport, fidèle à `0,00e0`) et une
**hypothèse de travail** (placement, granularité). Elle est écrite
ici parce qu'aucun autre moteur ne peut l'aborder aussi directement : dans une
architecture par matrices, l'unité de travail est une matrice entière — dans une
architecture par listes, c'est une poignée de faits.

---

## 5. Axe 4 — Rejouer, comparer, ne pas régresser

Un flux est un **journal**, et un journal se rejoue.

* les **portes de non-régression** du dépôt (Qwen ctx 256 = **19,3885**,
  gpt-oss ctx 256 = **15,6017**) sont l'application minimale de cette idée :
  deux chemins d'exécution doivent rendre le même résultat ;
* les tranches du projet qui ont été validées contre une **référence
  indépendante** (MLA à **5,2e-7** contre numpy et **0,999024** contre llama.cpp
  sur GLM-5.3 — `reports/rapport-mla-experts.md` ; vision : patchs 5,4e-7,
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

Deux cas méritent d'être nommés, parce qu'ils commandent la suite :

* le cas général est la **connexion pondérée** — `(source → destination, poids)` :
  c'est ce que le moteur transporte, et ce qu'un mélange appris entre plusieurs
  copies d'un état produit naturellement (les hyper-connexions d'un modèle
  récent en sont un exemple) ;
* le cas **trinaire** se passe de valeur : **deux listes**, celle des « + » et
  celle des « − », le signe étant porté par l'appartenance
  (`reports/rapport-encodage.md`). L'information est alors dans la structure, pas
  dans un octet — c'est le point extrême de la représentation choisie ici.

Les chiffres qui comptent, du point de vue de la vision :

* l'int8 sur le cache KV coûte **+1,5 %** de perplexité à 512 jetons et
  **+3,0 %** à 8 192, là où l'int4 coûte +364 % — le débat n'est pas « combien de
  bits » mais **où sont les échelles** (`reports/rapport-placement-bits-kv.md`) ;
* le dépaquetage vectorisé du noyau d'attention a fait passer le f32 de 13,6 à
  **7,0 ms** par couche à 1 M (308 Go/s, 69 % de la bande VRAM) : quand le
  format est bien lu, la mémoire cesse d'être le mur ;
* la densité d'activation (17,9 %) est l'argument énergétique : **on ne lit que
  ce qui parle**. C'est la même idée que l'AER neuromorphique, et c'est ce qui
  rend le FPGA intéressant pour autre chose que le débit brut.

---

## 7. Ce que la vision n'est pas

Pour que le document serve à quelque chose, il doit aussi refuser des choses :

* **ce n'est pas « le sparse gagne toujours »** : le croisement à ~22 % de densité
  est mesuré, et le moteur garde le chemin dense ;
* **ce n'est pas « un neurone = une décision »** : le profiler montre qu'un petit
  nombre de neurones portent l'essentiel, et qu'un préchargement statique ne paie
  pas — le dynamisme est la condition, pas l'ornement ;
* **ce n'est pas « distribuer, c'est gratuit »** : l'axe 3 est **engagé** (le
  transport est fidèle), avec ses mesures faites (latence, débit, taille des
  tranches) — mais l'ordonnanceur de placement n'existe pas, et le décodage
  restera séquentiel ;
* **ce n'est pas une réécriture** : le moteur Rust actuel *est* cette
  architecture — Drave est le nom de ce qu'il fait déjà, pas un projet parallèle.
* **ce n'est pas « apprendre des flux »** : le capteur hebbien n'ajoute que
  **+0,0045** de R² sur la couche 6 (la trace linéaire explique déjà 92 %), et
  **aucun** des 116 736 neurones ne reste muet — l'élagage par le zéro est vide.
  Les flux servent à **observer**, pas (encore) à apprendre ;
* **ce n'est pas « plus gros = mieux lire »** : la sonde est **plate dès le
  1,5 B** et le 14 B est **dernier** à profondeur fixe (0,4833) — la mesure a
  corrigé **quatre fois** dans la même journée la même erreur de point de mesure.

---

## 8. Feuille de route par axes

| axe | état | prochain pas |
|---|---|---|
| **1. Observer/régler par neurone** | ✅ le format de trace **v2**, le diff par couche **dans la porte** (18 s) | — |
| **2. Répartir sur composants** | mesuré (KV, attention, tête, experts) ; **la règle de placement est écrite** (`placement.rs`, `choisir`, 4 tests) et le KV l'applique | l'ordonnanceur **complet** : porter la place **et** la perte — la tête l'a montré, le 4 bits « qui tient » coûte +10 % de PPL → **A8, fait** (la règle place+perte, branchée en **opt-in**) |
| **3. Répartir sur machines** | **transport en place et fidèle** (`0,00e0`, protocole v5, cinq modes) ; mesuré : 1 608 octets/flux, 0,25 Mbit/s, latence ≤ 20 ms | la **grappe déportée** : exécuter une couche sur une autre ressource, pilotée par les flux — la greffe est **branchée** (648 s), le relais rend **42,5477**, la grappe exacte est à **21 %**, le transport à **4,22×** → **A7, fait** ; la démonstration distante reste bloquée par le compte Colab |
| **4. Rejouer/comparer** | ✅ portes, références indépendantes, **diff par couche**, rejeu | — |
| **5. Formats/matériels/énergie** | trois matériels, formats au point | ✅ la quantification par couche est un **curseur** (l'int8 tardif +0,03 %, le 4 bits +2,7 %) — mesuré, appliqué |

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

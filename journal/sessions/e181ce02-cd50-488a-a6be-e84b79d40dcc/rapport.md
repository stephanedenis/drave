# Session e181ce02 — Documentation Drave avec diagrammes et implémentation

> **Journaux :** [le jour](../../2026-10-31/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `e181ce02-cd50-488a-a6be-e84b79d40dcc` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-31 17:40 |
| Durée | 4.8 h |
| Tours | 4 |
| Messages | 159 |
| Appels d'outils | 183 |
| Fichiers touchés | 13 |
| Commandes | 131 |
| Sous-agents | 2 |
| Commits | 7 |
| Compactages de contexte | 0 |

## Objectifs déclarés

- **create** — Refondre la documentation de l'architecture Drave autour de la RSN plurielle (plusieurs candidats, pas un objet canonique unique) comme représentation interne permettant des cycles de pensée itératifs multi-niveaux : arbre d'états, opérateurs neuronaux/classiques, portefeuille de stratégies d'IA cla
… [256 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — fais une documentation détaillée du modèle Drave natif. utilise beaucoup de diagrammes pour expliquer ce qui est original à Drave. Comment implémenter un modèle de type Modèles de Diehl & Cook (2015) en respectant notre principe de séparation à 3 niveaux (sémentique neutre au centre)

**Tour 2** — continue tes réflexions et enrichit le document. Tu dois aller plus loin

**Tour 3** — Il est important que le RSN comme les autres blocs puissent accomplir leur tâches indépendamment du mode d'opération. C'est à dire que pour chaque bloc (et on veut que ces blocs soient petits) peut utiliser la technologie et les moyens les plus appropriés pour arriver à leur fins. Bref on a une modularité extréme où les neurones et le approches technoliques plus natives au matériel se coitoient na … [132 caractères tronqués]

**Tour 4** — tu commence à peine à comprendre la portée de ce quie je te demande. le RSN (le pluriel sera plus approprié ca tu dois avoir pleusieurs candidats) est une représentation de données interne qui te permen d'itérer indéfiniment dans de4s cicles de pensées à plunieurs niveauc. Il te faudra donc un arbre d'états et toutes les streatégies de l'ia traditionelle, pour pouvoir "penser". Prends au moins 10  … [102 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — fais une documentation détaillée du modèle Drave natif. utilise beaucoup de diagrammes pour expliquer ce qui est origina … [164 caractères tronqués]

*123 appels d'outils.* Actions notables :

- bash — Lister la structure du dépôt
- grep
- read
- bash — Chercher Diehl/Cook, LIF, STDP dans docs et code
- bash — Lire la vision
- bash — Lire contexte et sommaire docs
- bash — Chercher références Diehl & Cook
- bash — Lire la méthode illustrations et l'index des schémas
- bash — Inspecter le moteur drave-core
- bash — Lire la spec DRVF
- bash — Lire la synthèse chapitre 7
- bash — Lire l'archive sur les réseaux impulsionnels
- bash — Lire le bus et le chemin natif
- bash — Chercher le principe de séparation
- … et 101 autres

**Synthèse produite :**

⏵ Documentation livrée : deux pages, treize schémas, deux commits

J'ai écrit deux pages complémentaires, avec **13 schémas SVG** vérifiés :

- **[`docs/theorie/modele-natif.md`](docs/theorie/modele-natif.md)** — le modèle natif : le bus de faits, DRVM, le graphe `drave-n0`, les sept pertes, ce qui est réellement original, les portes N0–N4, et ce qui pourrait rendre le document faux.
- **[`docs/implantation/diehl-cook.md`](docs/implantation/diehl-cook.md)** — le cahier d'implémentation Diehl & Cook : équations, paramètres, manifeste DRVM, flux DRVF, tête RSN, contrôles négatifs et portes D0–D6.

\## L'idée centrale : le niveau est un contrat de port

La séparation à trois niveaux est posée explicitement :

| niveau | ce qu'il porte | ce qu'il rend |
|---|---|---|
| **N1 — surface** | texte, image, notation, langue | une **RSN** |
| **N2 — RSN** | les unités de sens, le corps canonique, l'annotation | une RSN |
| **N3 — pensée** | les opérations, les règles, les solveurs | une RSN d'action |

**N1 surface → N2 RSN → N3 pensée** : la RSN est au centre, et la surface ne traverse jamais le centre. Deux étages, trois niveaux : l'étage 1 est N1 ↔ N2, l'étage 2 est N3.

\## Où placer Diehl & Cook

C'est la réponse qui structure le second document :

1. **En N1 — encodeur** : `surface → RSN`. Il voit les pixels, mais il **rend** une RSN typée. C'est le seul placement où le résultat MNIST publié est reproductible tel quel. C'est le bootstrap.
2. **En N2 — mémoire** : `RSN → RSN`. Le même code reçoit `φ(RSN)` et jamais la surface ; il apprend des prototypes **de sens**. C'est la cible.
3. **En N3 — lecture associative** : `RSN → RSN`, légal si l'opération est vérifiable, mais la lecture de référence reste **classique et exacte** ; l'A/B tranche.
4. **Interdit** : `surface → décision` sans RSN. C'est le raccourci qui rend l'invariance invérifiable.

Le point non négociable : **le code de spikes n'est jamais la RSN**. C'est un code interne, surface-bound en N1. La RSN est un objet **canonique, typé, annoté**, avec une empreinte qui ne dépend pas de la surface. `φ` ne lit que le **corps** ; l'annotation (format, langue, confiance) est un port séparé. La neutralité se mesure par deux sondes : le **format** doit être prédictible depuis le code de spikes (N1), mais **pas** depuis `φ(corps)`.

Le document donne aussi le contrat DRVM concret : `kind: "spiking_map"`, `niveau`, `ports`, les tenseurs (`w_in`, `w_ei`, `w_ie`, `theta`, `assign`), les règles de refus du chargeur, l
… [1692 caractères tronqués]

### Tour 2 — continue tes réflexions et enrichit le document. Tu dois aller plus loin

*41 appels d'outils.* Actions notables :

- write `/tmp/gen_plus.py`
- bash — Générer les quatre nouveaux schémas formels
- bash — Corriger le branchement du canoniseur
- bash — Générer les cinq schémas d'analyse
- bash — Corriger la note WTA et centrer la pyramide
- bash — Repérer les textes longs des nouveaux schémas
- bash — Générer le schéma des six anti-patrons
- bash — Repérer les points d'insertion exacts
- write `/tmp/enrichir.py`
- bash — Insérer les sections enrichies et vérifier la structure
- bash — Lire le tableau des schémas à compléter
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md`
- … et 23 autres

**Synthèse produite :**

⏵ Enrichissement terminé : 23 schémas, deux documents approfondis, portes vertes

J'ai poussé les deux pages beaucoup plus loin, et le centre de gravité a changé : la séparation à trois niveaux n'y est plus un schéma, c'est un **système formel** ; et Diehl & Cook n'y est plus un modèle recopié, c'est un **bloc analysé, chiffré et pré-enregistré**.

\## 1. La séparation devient un système de types

- **La RSN est un quotient**, pas un vecteur : `c(s) = c(s') ⇔ s ~ s'`, le corps est l'invariant, l'annotation est le chemin, le miroir est une **rétraction** (`c(d(c(s), a(s))) = c(s)`). Le hash n'est qu'un représentant.
- **Le niveau est déclaré et vérifié**, pas deviné : une signature `surface → rsn` est N1, `rsn → rsn` peut être N2 ou N3 mais doit le déclarer ; le code interne (`code`) ne traverse **jamais** une arête.
- **Théorème de non-fuite** : dans un graphe légal, tout chemin du monde à N3 traverse une arête `rsn`. La preuve tient en trois lignes, et c'est le chargeur qui l'applique.
- **Le raffinement** définit la substituabilité : même signature, même corps, annotations compatibles, même trace. C'est la définition opérationnelle du bus.

\## 2. La neutralité devient mesurable — et piégeuse

Le nouveau schéma `natif-neutralite.svg` pose le couple :

- **neutre** : le format n'est pas prédictible depuis le corps (`P_f` doit échouer) ;
- **informatif** : la classe est prédictible depuis le corps (`P_y` doit réussir).

Un code constant est parfaitement neutre et parfaitement inutile. Un code de surface est informatif et non neutre. La cible est le quadrant haut-droit ; le **marginal sémantique** est `I − N`. Et la neutralité est **relative au corpus** : un corpus où le format prédit la classe fait réussir `P_f` sans que la RSN fuie.

J'ai ajouté les **six anti-patrons** (le code promu, la surface au raisonneur, l'annotation dans le corps, le jeton déguisé, le faux miroir, le niveau décoratif) avec, pour chacun, le test qui l'attrape.

\## 3. Le rejeu devient une pile de décisions

Six étages : graine → RNG contré → ordre des opérations → arithmétique (f64, pas de fast-math) → trace canonique → hash. Trois niveaux de rejeu : **bit-exact**, **tolérant**, **sémantique**. D&C revendique le bit-exact ; un bloc qui ne dit pas lequel il garantit ne garantit rien.

\## 4. Le résultat le plus utile : le coût caché de la STDP symétrique

C'est le point que je n'avais pas vu en écrivant la première version. La règle du code de démonstration met à jour les poids **à chaq
… [4153 caractères tronqués]

### Tour 3 — Il est important que le RSN comme les autres blocs puissent accomplir leur tâches indépendamment du mode d'opération. C' … [412 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Générer les schémas modes et granularité
- bash — Insérer le mode privé, la granularité et le graphe dynamique
- bash — Repérer les lignes du tableau des schémas
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md`
- bash — Passer les portes après l'ajout du mode privé
- bash — Committer le principe d'indépendance technologique
- job_output

**Synthèse produite :**

⏵ Principe intégré : le contrat est l'invariant, la technologie est la variable

Oui — et c'est un déplacement important, parce qu'il ne faut pas confondre **la RSN et les blocs RSN**. La RSN n'est pas un bloc : c'est le **type** qui circule. Les blocs qui la produisent ou la consomment — encodeur, mémoire, décodeur — sont, eux, technologiquement libres. Un format n'est pas une machine.

J'ai ajouté cette axe aux deux documents, avec deux schémas.

\## 1. Le théorème d'indifférence

Si deux blocs ont la même **signature typée**, le même **contrat** (même corps pour les mêmes entrées, annotations compatibles) et la même **trace**, alors ils sont **substituables**, quelle que soit leur technologie. Le consommateur ne peut les distinguer que par le **coût** et la **trace**.

C'est la version formelle de ce que tu décris : le bus ne voit pas des neurones, il voit des **types**. Un transformeur dense, un réseau impulsionnel, un solveur classique, un bloc FPGA ou un service distant peuvent occuper le même port.

Mais l'indifférence a un prix, et le document le dit : il faut **un test de contrat** (les sondes), **une trace** (le rejeu) et **un coût** (le placement). Sans les trois, l'hétérogénéité n'est pas une modularité, c'est un zoo.

\## 2. Le mode d'opération et le mode d'apprentissage sont privés

Un bloc peut être :

| réalisation | représentation | ce qu'elle apporte |
|---|---|---|
| transformeur dense | f32, attention | composition, langue |
| D&C impulsionnel | spikes, STDP | parcimonie, apprentissage local |
| règle classique | symboles, table | exactitude, auditabilité |
| FPGA | bits, shift-and-add | énergie, déterminisme |
| service distant | DRVF/TCP | placement, réutilisation |

**Ce qui change** : la latence, le coût, la précision, le niveau de rejeu.
**Ce qui ne change pas** : les ports, le corps de la RSN, l'empreinte, la trace.

Le mode d'apprentissage est privé aussi : STDP locale, gradient hors ligne, règle classique, ou aucun. Le contrat ne voit que la sortie ; mais le bloc doit **déclarer** son mode et son niveau de rejeu — `bit-exact`, `tolérant`, `sémantique` — sinon la trace n'est pas reproductible.

\## 3. La granularité : petit, mais pas trop

Tu demandes des blocs petits. Le document formalise le compromis :

`coût_total = coût_bloc + k · nombre_d_arêtes`

Un bloc trop gros n'est ni mesurable, ni plaçable, ni substituable. Un bloc trop petit paie la liaison — sérialisation, transport, synchronisation, trace. L'optimum dépend de la tâch
… [2300 caractères tronqués]

### Tour 4 — tu commence à peine à comprendre la portée de ce quie je te demande. le RSN (le pluriel sera plus approprié ca tu dois a … [382 caractères tronqués]

*11 appels d'outils.* Actions notables :

- create_goal
- write `/tmp/gen_pensee.py`
- bash — Générer les deux premiers schémas de la pensée
- bash — Corriger la hauteur des nœuds de l'arbre
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/pensee-iterative.md`
- bash — Relier la RSN plurielle aux documents existants et vérifier
- bash — Corriger le lien et aligner les compteurs
- bash — Lire les lignes de compteurs exactes
- bash — Aligner le compteur JSON et revérifier
- bash — Committer le premier tour de la refonte
- job_output

**Synthèse produite :**

⏵ Tour 1/10 — la RSN de travail est un ensemble de candidats, pas un quotient unique

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/svgkit.py` | 1 | 0 |
| `/tmp/gen_natif.py` | 1 | 0 |
| `/tmp/gen_diehl.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/modele-natif.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/diehl-cook.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md` | 0 | 5 |
| `/tmp/gen_plus.py` | 1 | 0 |
| `/tmp/enrichir.py` | 1 | 0 |
| `/tmp/gen_pensee.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/pensee-iterative.md` | 1 | 0 |

### Sous-agents lancés

- tour 1 — Revue visuelle des 7 schémas
- tour 1 — Test revue visuelle

### Commandes exécutées (échantillon)

- **T1** Lister la structure du dépôt
- **T1** Chercher Diehl/Cook, LIF, STDP dans docs et code
- **T1** Lire la vision
- **T1** Lire contexte et sommaire docs
- **T1** Chercher références Diehl & Cook
- **T1** Lire la méthode illustrations et l'index des schémas
- **T1** Inspecter le moteur drave-core
- **T1** Lire la spec DRVF
- **T1** Lire la synthèse chapitre 7
- **T1** Lire l'archive sur les réseaux impulsionnels
- **T1** Lire le bus et le chemin natif
- **T1** Chercher le principe de séparation
- **T1** Lire le protocole sémantique et la fiche couche/étage
- **T1** Lire fiches RSN et un SVG existant
- **T1** État git et état courant
- **T1** Repérer la ligne N de la roadmap
- **T1** Repérer les fiches natives dans reports
- **T1** Lire le lecteur DRVM
- **T1** Trouver les outils DRVM
- **T1** Inspecter le fixture DRVM
- **T1** Afficher le manifeste du modèle témoin
- **T1** Extraire les paramètres du texte de l'article
- **T1** Lister les fichiers du dépôt de référence
- **T1** Récupérer le code de référence et ses paramètres
- **T1** Lire les paramètres complets du code de référence
- **T1** Lire inhibition et normalisation
- **T1** Lire le générateur de connexions
- **T1** Lire la doctrine des trois niveaux (jeux symboliques)
- **T1** Lire le vérificateur de schémas
- **T1** Lire la revue de documentation et le budget
- **T1** Lire la suite de la revue (classement, navigation)
- **T1** Lire deux SVG existants pour le style
- **T1** Lire la porte des tableaux et le vérificateur d'état
- **T1** Lire le README du moteur et la liste valuée
- **T1** Repérer les mécanismes d'exécution
- **T1** Lire la section N de la roadmap
- **T1** Lire la carte des sujets
- **T1** Lire l'écrivain DRVM
- **T1** Vérifier la date et la règle d'état à jour
- **T1** Voir la modification en cours de l'état
- … et 91 autres

## 4. Mesures et résultats marquants

- **T1** `- **La sparsité ne gagne pas toujours** : le croisement push/pull est mesuré à ~22 % de densité ; en dessous, les`
- **T1** `(9,23–9,96 M), un meilleur écart **4,40 % à 31,63 M / 610 exemples**, une **fenêtre** (3,71 % à 500 pas, 1,29 %`
- **T1** `à 750, −0,49 % à 1 000) et un **négatif à 30 langues**. La capacité ne paie **qu'avec les données**.`
- **T1** `trace creuse (39,9 % d'activité) : 6,04 et 3,04 — deux centièmes de plus, parce que`
- **T1** `99,9997 % des cas (22 échappements sur 8 790 000 mesurés). Trois octets par`
- **T1** `| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |`
- **T1** `| trace dense, 512 jetons | 66 370 408 o | **45 079 930 o (−32,1 %)** |`
- **T1** `| rejeu `--flux-forcer` | 19,3885 | **19,4029 (+0,074 %)** |`
- **T1** `| neurones actifs | 22 008 776 | 21 630 645 (−1,7 % : les valeurs qui s'arrondissent à zéro ne sont pas écrites) |`
- **T1** `| erreur par valeur | nulle | RMS **0,085 %** du max de la liste (max 0,394 %) |`
- **T1** `jetons, 16 par lot, seuil 0,01 : **1,5 ko par jeton au lieu de 3,5** (÷2,3) pour`
- **T1** `f32 dense (3,5 ko par jeton) ; le lot en LISTES est le mode 4 (1,5 ko par jeton,`
- **T1** `- **la langue est lisible partout** dans l'état d'un modèle entraîné (80 à 100 % dès la couche 1, sur 5 modèles`
- **T1** `- **le sens est aligné malgré la langue** : le même article UDHR se retrouve d'une langue à l'autre à **96 %** sur`
- **T1** `les paires bien couvertes, **16 %** sur un échantillon stratifié de 100 langues, et **3,5×** le hasard dans un`
- **T1** `- **la restitution exacte** (même langue, à l'identique) est **parfaite pour un modèle spécialisé** (85 % de`
- **T1** `fragments exacts) et **s'effondre quand il partage 448 langues** (0,6 %) : la capacité ne se partage pas`
- **T1** `- **la hiérarchie des surfaces** : langues **96 %** > dialectes **52-97 %** > styles (traducteurs) **24 %** — et les`
- **T1** `trois sont **lues à 100 %**. *L'étage entrée-sortie n'efface aucune surface : il en aligne le sens.*`
- **T1** `- **le bruit d'entrée est signalable** (fautes et langues mêlées : détection 100 %, AUC 1,00) **mais pas`
- **T1** `- **La langue est un petit paramètre** : **1,33 %** des poids (32 768 au dernier étage), bascule **5 ms**,`
- **T1** `**530 Ko** (mesures 3 et 7). Un module de langue peut donc être **petit** et **chargé à la demande**.`
- **T1** `- **Le partage détruit la restitution** : **85 %** de fragments exacts pour un modèle spécialisé, **4 %** quand il`
- **T1** `- **Mais l'espace sémantique est partagé** : **96 %** de retrieval croisé sur les paires couvertes (mesure 39) ; le`
- **T1** `**Ce que cela autorise** : un **noyau partagé** (le sens, 96 %) + des **modules de surface par langue** (entrée et`
- **T1** `sortie : embeddings, tête, adaptateurs), **routés par segment** et **chargés à la demande** (5 ms / 530 Ko). C'est`
- **T1** `langue contre modèle partagé 448 langues, pour répliquer 85 % → 4 %.`
- **T1** `3. **le style** : il est lisible, mais le sens ne le traverse qu'à 24 % — comment l'augmenter sans perdre le style ?`
- **T1** `de 77-88 µJ à **0,594 µJ**. Résultat : 74,81 % sur ImageNet en 4 pas de temps.`
- **T1** `15 % de spikes non nuls en moyenne. 46 M et 216 M de paramètres, **32,2× moins`
- **T1** `redeviennent des accumulations. Gain : **+1,04 % de précision ET −57,34 %`
- **T1** `| Taux d'activation mesuré | **R̂ ≈ 0,15** (SpikeGPT) | **0,00 % de zéros** sur un LLM dense entraîné |`
- **T1** `| Arithmétique | ET logique + **AC** (accumulation) | MAC (mais décalages+additions validés, 0 DSP sur FPGA) |`
- **T1** `| Énergie par opération | E_AC = 0,9 pJ contre E_MAC = 4,5 pJ (Horowitz) | 8,3 nJ/événement (FPGA, **projeté** : 4,83 G évts/s, limite DDR3) contre 57 nJ (CPU, **mesuré**) — rapport 6,9× |`
- **T1** `qui s'active » reste théorique. À seuil 5 % du max, la densité mesurée tombe à`
- **T1** `**17,9 %** — sous le croisement push/pull de **22 %**`
- **T1** `(2,0 ms à 64 tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192) et ses poids`
- **T1** `| Débit mesuré (CPU, 16 threads) | 5,3 G évts/s | 5,3 G évts/s |`
- **T1** `| Temps par token | 63 ms | **~10 ms** |`
- **T1** `| Débit | 15,8 tok/s | **~100 tok/s** |`
- **T1** `- Les gains annoncés (32×, 57 %) sont **théoriques**, calculés avec`
- **T1** `écart relatif réel (4,40 %) mais **transitoire** : à 1 000 pas, le contrôle repasse, et à 30 langues l'effet se`
- **T1** `- **batch 16, seq 384** : le GPU est à ~95 %, la mémoire à ~15 Go par carte ; le CPU ne fait qu'un fil par`
- **T1** `<text x="450" y="350" text-anchor="middle" font-size="12.5" fill="#334155">B11 : codec 100 % (79/79, 449/449), surface 33/79, natif 59,8 / 40,7. B12 : modules M1–M9.</text>`
- **T1** `4442c64c N2 — L'ÉTAT DE SECTION NE SE DISTINGUE PAS D'UN ÉTAT ÉTRANGER (+0,36 % CONTRE +0,37 %)`
- **T1** `4 sources, **B′** quotas égaux (le manifeste est à **82 % anglais**), **C** curriculum 129`
- **T1** `sur A ; la hiérarchie est écartée deux fois, restent **le curriculum et les données** (41 Mo,`
- **T1** `- **R13 — la tokenisation** : **close**, décision **octets** — BPE 512 +0,39 % (bruit), BPE`
- **T1** `1024 +4,09 %, anglais +4,22/+6,59 % à octets égaux ; fiche`
- **T1** `- **B10.2bis — décodeur** : 3×3 : **11,1** ; capacité 11,8 ; **mots 32,5** ;`
- **T1** `- **B11.10** : **hybride 4/4** — codec **161/161**, ambiguïtés refusées ; **69,3 %** natif ;`
- **T1** `**N2.h2** (distillation, professeur refait, 3 graines) : **2,9935** contre **2,9927** (+0,029 %) ;`
- **T1** `84:[N0/N1] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `85:[N2] lasts 4 days and is 30% complete and is colored in #b26a00`
- **T1** `168:| **N1** | `drave-n0` : 11,47 M, 6 blocs, octets, attention locale, FFN creux, 3 têtes précoces | ✅ | aucune — PPL **3,465** avec pont (**4,080** sans) ; têtes **57,6 / 61,6 / 62,1 %** contre **62`
- **T1** `41:| [`rapport-native-distillation-50k.md`](rapport-native-distillation-50k.md) | **N2.11** — 50 000 pas : PPL **3,082**, plateau ; tête 3 **68,70 %** |`
- **T1** `51:| [`rapport-native-service-rust.md`](rapport-native-service-rust.md) | **N4.3** — service Rust natif avec cache : **611 ms**, 53 octets |`
- **T1** `54:| [`rapport-native-distillation-20k.md`](rapport-native-distillation-20k.md) | **N2.8** — 20 000 pas : PPL **3,123** contre **3,295**, précision **67,96 %**, gap **+0,768** |`
- **T1** `60:| [`rapport-native-cache.md`](rapport-native-cache.md) | **N0.9** — cache KV natif : sortie identique à Python, **592,6 ms**, 53 octets |`
- **T1** `67:| [`rapport-native-distillation-tetes.md`](rapport-native-distillation-tetes.md) | **N2.4** — têtes dans la distillation : PPL **3,295**, pas de gain ; tête 3 **62,98 %** > principale **62,35 %** |`
- **T1** `85:| [`rapport-deepseek.md`](rapport-deepseek.md) | **B9** : DeepSeek pour le langage, 310 prompts, chrF, le natif sur GPU, la transition 9,23–9,96 M, la fenêtre 610/20 (3,71 % à 500 pas) et le négati`
- **T1** `34:In order to understand how the mammalian neocortex is performing computations, two things are necessary; we need to have a good understanding of the available neuronal processing units and mechanis`
- **T1** `45:Here we present a spiking neural network which relies on a combination of biologically plausible mechanisms and which uses unsupervised learning, i.e., the weights of the network learn the structur`
- **T1** `56:We use biologically plausible ranges for almost all of the parameters in our simulations, including time constants of membranes, synapses and learning windows (Jug, 2012 ); the exception is the tim`
- **T1** `79:The input to the network is based on the MNIST dataset which contains 60,000 training examples and 10,000 test examples of 28 28 pixel images of the digits 0 9 (LeCun et al., 1998 ). The input is p`
- **T1** `81:To train the network, we present digits from the MNIST training set (60,000 examples) to the network. Before presenting a new image, there is a 150 ms phase without any input to allow all variables`
- **T1** `87:Additionally to the 100 neuron network, we trained and tested three other networks with 400, 1600, and 6400 excitatory neurons by presenting 3, 7, and 15 times the entire MNIST training set; the fo`
- **T1** `95:The presented network achieves good classification performance on the MNIST benchmark using SNNs with unsupervised learning made of biologically plausible components. A comparison of spiking neural`
- **T1** `170:A network architecture similar to ours is presented in Querlioz et al. ( 2011a , 2013 ) and Bichler et al. ( 2012 ), using the learning rule presented in Querlioz et al. ( 2011b ). The main differ`
- **T1** `178:Intuitively, the function of the network is similar to competitive learning procedures (McClelland et al., 1986 ) like self-organizing maps (Kohonen, 1990 ) or neural-gas (Fritzke, 1995 ), which s`
- **T1** `First run the main file "Diehl&Cook_spiking_MNIST.py" (which by default uses the pretrained weights) and wait until the simulation finished (on recent hardware this should take about 30min). After the`
- **T1** `At first you have to modify the main file "Diehl&Cook_spiking_MNIST.py" by changing line 210 to "test_mode = False" to train the network. The resulting weights will be stored in the subfolder "weights`
- **T1** `<text x="450" y="366" text-anchor="middle" font-size="13" fill="#0f172a">1 608 octets par flux à 256 jetons · 0,25 Mbit/s · latence ≤ 20 ms</text>`
- **T1** `### Tailles d'encodage (bits/poids, densité 99,2 %)`
- **T1** `qui perd la magnitude. Les listes ne gagnent que sous ~20 % de densité : c'est la`
- **T1** `| 0 % | 0 | — | — | **0,049** | **×10** |`
- **T1** `| 1 % | 43 560 | 0,11 G év/s | **0,84** | 0,052 | ×7,5 |`
- **T1** `| 5 % | 217 851 | 0,54 | **2,95** | 0,074 | ×5,5 |`
- **T1** `| 10 % | 433 035 | 1,07 | **4,02** | 0,108 | ×3,8 |`
- **T1** `| 25 % | 1 082 120 | 2,31 | **4,91** | 0,220 | ×2,1 |`
- **T1** `| 50 % | 2 163 317 | 3,76 | **5,51** | 0,392 | ×1,5 |`
- **T1** `| 100 % | 4 325 087 | 5,77 | **5,80** | 0,746 | ×1,0 |`
- **T1** `- **Coût fixe : 0,484 ms → 0,049 ms** grâce au pool persistant (threads et`
- **T1** `**×8,5 en régime creux**, précisément le régime qui nous intéresse.`
- **T1** `- **Le débit varie de ×15** entre densité nulle (0,049 ms) et pleine (0,746 ms) —`
- **T1** `- **Pic : 5,80 G événements/s** (contre 4,66 avant), soit 75 % du banc C de`
- **T1** `À 100 % de densité : bitmap 4,07 G év/s contre **5,80** pour les varints. Le chemin`
- **T1** `| multiplication i8×i8 | 2,5 ms | — |`
- **T1** `| décalages + additions | 110,7 ms | ×44 |`
- **T1** `1. ~~Pool de threads persistant~~ ✅ fait (×10 sur le coût fixe).`
- **T1** `(le plancher de 0,049 ms reste dominé par la réduction des 896 sorties × 16 threads).`
- **T1** `5,8 G év/s ; regrouper les événements d'une même plage de destinations`
- **T1** `| **N1** | `drave-n0` : 11,47 M, 6 blocs, octets, attention locale, FFN creux, 3 têtes précoces | ✅ | aucune — PPL **3,465** avec pont (**4,080** sans) ; têtes **57,6 / 61,6 / 62,1 %** contre **62,7 %`
- **T1** `2. **Le saut de calcul existe, le saut de contenu n'existe pas.** La sortie précoce gagne **24,05 %** de temps en`
- **T1** `| **A7** la grappe déportée | **fait** — relais 42,5477, grappe 21 %, transport 4,22× | [la roadmap](../pilotage/roadmap.md) |`
- **T1** `| **B5/B6** les jeux symboliques | **faits** — 112 items, 100 % au niveau 4, pensée 5/5 | [le concept](jeux-symboliques.md) · [la fiche](../../reports/rapport-jeux-symboliques.md) |`
- **T1** `| **B9** le banc externe | **mesuré** — seuil 9,23–9,96 M, 31,63 M/610 4,40 %, fenêtre, négatif 30 langues | [le concept](../implantation/llm-externe.md) · [la fiche](../../reports/rapport-deepseek.md`
- **T1** `| **B11** la base d'universaux typés | **premier passage** — codec 100 % (79/79, 449/449) ; natif synthétique normalisé 55,7 % (invariance 37,0 %) ; codec + contexte 528/528 (100 %) ; natif contexte s`
- **T1** `| **C3.2e** sous-familles autres | **mesuré** — uralic 46,7→100 %, benue 88 %, austro 60,3 %, afro ouest 53,5 % | [la fiche](../../reports/rapport-sous-familles-autres.md) |`
- **T1** `| **C3.2d** sous-familles IE | **mesuré** — 54,6–100 % ; l'IE à 14,7 % est un effet de composition | [la fiche](../../reports/rapport-ie-sous-familles.md) |`
- **T1** `| **C3.2c** 9 familles | **mesuré** — 7/9 > 30 %, moyenne 69,5 %, contrôle 0 ; indo-européen 14,7 %, uralic 46,7 % | [la fiche](../../reports/rapport-familles-9.md) |`
- **T1** `| **B23** routeur M1→M2 | **partiel** — espaces 41,8 % vs 11,6 % ; typo 56,2 % < M2 68,3 % ; collision de lexique | [la fiche](../../reports/rapport-routeur-m1-m2.md) |`
- **T1** `| **B22** M2 typos | **niche robuste** — M2 62–80 % contre M1 24–45 % sur 4 types de typos | [la fiche](../../reports/rapport-m2-typo.md) |`
- **T1** `| **B17** mémoire LFU | **filtre** — LFU 9,28 % suffixe vs FIFO 5,03 % ; M8 couverture 70,75 %, lookup 100 %, généralisation 0 | [la fiche](../../reports/rapport-pipeline-memoire.md) |`
- **T1** `| **B14** M2 dans la chaîne | **rameau** — M1 100 %, M2 93,4/93,6 %, aucun étage ne consomme M2 ; M5 plateau 18,70 % vs 12,60 % | [la fiche](../../reports/rapport-pipeline-m2.md) |`
- **T1** `| **B15** M1 multilingue | **66 langues** — 528/528 ; 26/26 variantes et 15/15 interlangues invariantes ; contrôle permuté 0/90 % | [la fiche](../../reports/rapport-multilingue.md) |`
- **T1** `| **B13** la chaîne sémantique | **intégration** — M1 528/528 ; M5 contexte 18,7 % vs 12,6 % ; M6 94,3 % ; M8 57,95 % (borne haute) | [la fiche](../../reports/rapport-pipeline-semantique.md) · [le cod`
- **T1** `| **B12** les modules cerveau-langage | **premier passage** — M1 528/528 ; M2 **98,6 / 93,2** (double dissociation) ; M8 **96,48 %** hors stock ; M5/M6/M7 négatifs ; M9 lésions | [les modules](modules`
- **T1** `touche **25 % des activations × 50 % des poids = 12,5 %** des poids par jeton`
- **T1** `(campagne, § 5 ter), alors qu'un pas d'entraînement par gradient en touche **100 %**.`
- **T1** `d'événement, décroissance, forme signée) : gains en échantillon −0,73 % au mieux,`
- **T1** `**transfert nul** sur un autre texte, et **dégradation de 5 à 10 % sur des langues`
- **T1** `**(b) Un signal global, lui, apprend.** La distillation (−13,8 % sur un modèle routé`
- **T1** `à dim 512 ; −0,3 % sur un dense creux) est notre seul mécanisme de crédit, et il`
- **T1** `**(c) Les contraintes dures apprises marchent.** k-WTA à 25 % : le modèle creux fait`
- **T1** `*mieux* que dense, là où le témoin s'effondre (+118 %). Élagage appris à 50 % :`
- **T1** `÷2 lectures, qualité inchangée (+0,3 %). **Le substrat accepte d'apprendre sous`
- **T1** `**(d) Un connectome inné aléatoire coûte 1 % — ATTENTION : sur l'attention seulement, rétracté le 11/10 (+9,4 % pour le modèle entier).** Masque de 25 % des connexions tiré à`
- **T1** `la naissance, jamais modifié : perplexité 5,0472 contre 4,9959, événements **÷4,1**,`
- **T1** `débit **×2,1** (§ 4 bis de `biologie-pour-drave.md`). **La structure peut être`
- … (tronqué)

## 6. Commits

- DOCS — LE MODÈLE NATIF ET DIEHL & COOK, 13 SCHÉMAS : LA SÉPARATION À TROIS NIVEAUX" 2>&1 | tail -30; echo "EXIT=${PIPESTATUS[0]}"
- DOCS — DIEHL & COOK : UNITÉS, DÉLAIS ET TRACE DES INHIBITEURS" 2>&1 | tail -12; echo "EXIT=${PIPESTATUS[0]}"
- DOCS — LE MODÈLE NATIF ET DIEHL & COOK ENRICHIS : QUOTIENT, TYPES, NEUTRALITÉ, DÉTERMINISME, BANC, CONFORMITÉ" 2>&1 | tail -12; echo "EXIT=${PIPESTATUS[0]}"
- DOCS — LE COÛT CACHÉ DE LA STDP SYMÉTRIQUE, LA LECTURE D'UN PAS ET LES QUESTIONS OUVERTES" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- DOCS — SEUILS PRÉ-ENREGISTRÉS ET COÛT DE LA STDP : LE RENVERSEMENT" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- DOCS — LE CONTRAT EST L'INVARIANT, LA TECHNOLOGIE EST LA VARIABLE : MODES, GRANULARITÉ, GRAPHE DYNAMIQUE" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- PENSÉE — TOUR 1-2 : LA RSN PLURIELLE ET L'ARBRE D'ÉTATS" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"


# Session e181ce02 — Documentation Drave avec diagrammes et implémentation

> **Journaux :** [le jour](../../2026-10-31/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `e181ce02-cd50-488a-a6be-e84b79d40dcc` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-31 17:40 |
| Durée | 0.5 h |
| Tours | 1 |
| Messages | 93 |
| Appels d'outils | 120 |
| Fichiers touchés | 9 |
| Commandes | 87 |
| Sous-agents | 2 |
| Commits | 2 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — fais une documentation détaillée du modèle Drave natif. utilise beaucoup de diagrammes pour expliquer ce qui est original à Drave. Comment implémenter un modèle de type Modèles de Diehl & Cook (2015) en respectant notre principe de séparation à 3 niveaux (sémentique neutre au centre)

## 2. Déroulé, étape par étape

### Tour 1 — fais une documentation détaillée du modèle Drave natif. utilise beaucoup de diagrammes pour expliquer ce qui est origina … [164 caractères tronqués]

*120 appels d'outils.* Actions notables :

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
- … et 98 autres

**Synthèse produite :**

⏵ Commit des deux documents et des treize schémas

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
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md` | 0 | 2 |

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
- … et 47 autres

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


# Ce que la biologie a à nous apprendre — avant d'écrire notre modèle

> 9 octobre 2026. Exploration demandée : les connectomes sont maintenant assez bien
> documentés pour inspirer un modèle où **l'énergie et les ressources sont
> limitées**, et où l'on fait **croître** à partir d'un connectome de base (inné)
> tout le savoir et le comportement. Ce document rassemble les faits mesurés, écarte
> les mythes, et traduit le tout en décisions de conception pour Drave — avec, à la
> fin, les expériences que nos outils permettent de faire **cette semaine**.

---

## 1. Ce qui est réellement mesuré

### 1.1 Trois connectomes complets, et un fragment de mammifère

| cerveau | neurones | connexions | état |
|---|---:|---:|---|
| *C. elegans* | **302** | ~7 000 | complet depuis 1986 |
| larve de drosophile | **3 016** | — | complet (2023) |
| **drosophile adulte** | **139 255** | **~50 millions** | **complet (2024)**, 8 000 types cellulaires annotés, synapses prédites excitatrices ou inhibitrices ([FlyWire/Nature](https://www.eurekalert.org/news-releases/1059473), [flywire.ai](https://flywire.ai/)) |
| souris (1 mm³ de cortex visuel) | ~2 × 10⁵ cellules | ~5 × 10⁸ synapses | [MICrONS](https://www.microns-explorer.org/cortical-mm3), [Nature 2025](https://www.nature.com/articles/s41586-025-08790-w) |

Le cerveau humain, lui, n'est pas reconstruit : **86 milliards de neurones** dont
~16 milliards dans le cortex, et de l'ordre de 10¹⁴-10¹⁵ synapses. On ne dispose que
de fragments (quelques milliers de neurones et ~10⁷ synapses par fragment).

**Trois faits de méthode, tirés du travail sur la drosophile, comptent pour nous :**

1. **« Les cerveaux ne sont pas des flocons de neige »** — la comparaison avec des
   reconstructions partielles antérieures montre une **forte similarité de câblage
   entre individus**. C'est la justification empirique de l'idée d'un *connectome de
   base* : il existe, et il est partagé.
2. **~0,5 % des neurones ont une variation développementale** qui peut mal câbler
   leurs connexions. Autrement dit : la variabilité individuelle est **une petite
   fraction** du plan, pas le plan lui-même.
3. Le coût de la reconstruction : 7 000 tranches de 40 nm, **100 To d'images**,
   33 personnes-années de relecture pour 50 M de connexions. **Un connectome est un
   objet coûteux** — la question « faut-il en apprendre un, ou partir d'un plan
   fixe ? » a donc un enjeu pratique, pas seulement théorique.

### 1.2 Le budget d'énergie : c'est la SIGNALISATION qui coûte

- Le cerveau humain pèse **2 %** du corps et consomme **20 %** de son métabolisme
  ([PNAS, « Brain power »](https://www.pnas.org/doi/full/10.1073/pnas.2107022118)).
- L'essentiel part dans les **potentiels d'action et la transmission synaptique**,
  pas dans l'entretien passif : c'est le résultat central du bilan d'Attwell &
  Laughlin ([J. Cereb. Blood Flow Metab. 2001](https://rcseng.ovidds.com/discover/result?logSearchID=163215621&pubid=solr_6306-sage%3A10.1097%2F00004647-200110000-00001&pubid=solr_7902-info%3Adoi%2F10.1097%252F00004647-200110000-00001&pubid=solr_6057-medline%3A11598490)).
- Un potentiel d'action coûte de l'ordre de **1,5 × 10⁹ molécules d'ATP**
  (ordre de grandeur relevé dans la littérature de bilan énergétique).

**Et c'est là que la biologie parle directement à Drave** : dans un cerveau, le coût
d'un calcul est **proportionnel au nombre d'événements** (spikes × synapses
postsynaptiques actives). Dans Drave, le coût d'une passe est **le nombre de paires
(poids × activation)**. **C'est la même forme fonctionnelle.** Le moteur a été conçu
autour de la bonne quantité — ce que la biologie appelle énergie, Drave l'appelle
« paires ».

### 1.3 La sparsité : deux ordres de grandeur, pas 10 %

- Taux de décharge moyen du cortex : **0,1 à 1 Hz**, avec des pointes brèves ; à un
  instant donné, **de l'ordre de 1 % des neurones** sont actifs.
- Codage épars dans le cortex visuel : **~10 % des neurones** répondent fortement à
  une scène naturelle ([Vinje & Gallant 2000](https://journals.physiology.org/doi/pdf/10.1152/jn.00594.2010)) —
  et la réponse est *distribuée* : l'information n'est pas dans un neurone mais dans
  un petit sous-ensemble.
- Il existe même un **sous-réseau de neurones très actifs** intégré dans le cortex
  ([Neuron 2010](https://embargoed.www.cell.com/neuron/fulltext/S0896-6273(10)00971-2)) :
  la sparsité n'est pas uniforme, elle est **structurée**.

**Comparaison avec la campagne** : nos modèles denses ont une densité d'activation
de **71 %**, identique sur quatre corpus. Le cerveau est deux ordres de grandeur
en dessous. Ce n'est pas un détail de réglage : c'est une **différence de régime**.

### 1.4 La connectivité : creuse, locale, et pas aléatoire

- Probabilité de connexion entre deux neurones corticaux : **~10 %** (souvent citée
  entre 1 et 20 % selon les couches et les types) ; **~7 000 synapses** par neurone
  en moyenne, pour 10¹⁰ neurones corticaux — donc une matrice **très creuse**.
- Le câblage minimise la longueur d'axone (principe de **wiring minimisation**,
  Chklovskii) et présente une structure **petit-monde** (forte clustering locale +
  quelques connexions longues).
- Balance **excitation / inhibition** maintenue autour de 80/20, avec des boucles de
  rétroaction qui la stabilisent.

### 1.5 L'inné et l'acquis : surproduction puis élagage

- La synaptogenèse **surproduit** : la densité synaptique culmine vers **1 an**,
  puis est **élaguée** jusqu'à l'adolescence
  ([thèse King's College](https://kclpure.kcl.ac.uk/ws/portalfiles/portal/103185189/2017_Pote_In_s_1270668_ethesis.pdf)).
- L'apprentissage synaptique est **local** (STDP), sans mécanisme connu de
  rétropropagation du gradient ; le crédit global passe par des **neuromodulateurs**
  (dopamine, acétylcholine) — des signaux diffus, pas un gradient par poids.
- Le cerveau **rejoue** : les séquences d'activité sont réactivées hors ligne
  (sommeil), ce qui consolide.

---

## 2. Les mythes à écarter tout de suite

| mythe | ce que la mesure dit |
|---|---|
| « le neurone est une unité de calcul simple » | les dendrites font des opérations non linéaires ; mais **pour notre sujet c'est secondaire** : c'est le *coût par événement* qui compte, pas la biophysique fine |
| « le cerveau apprend par descente de gradient » | aucun mécanisme connu ; l'apprentissage est **local**, le crédit passe par la neuromodulation |
| « 86 milliards de neurones = 86 milliards de paramètres » | le cerveau a ~10¹⁴-10¹⁵ **synapses**, et il en **élague** la moitié ; le nombre de neurones n'est pas la capacité |
| « il faut imiter les spikes pour être bio-inspiré » | ce qui compte est **où va l'énergie** : dans les événements, pas dans la forme du signal |
| « le cerveau est optimisé pour la précision » | il est optimisé pour **survivre avec 20 W**, ce qui inclut être *suffisamment* bon, pas optimal |
| « un génie a un cerveau plus gros / plus dense » | les différences structurelles rapportées sont **fines et contestées** (voir § 5) ; la taille explique peu |

---

## 3. La traduction : dix correspondances avec Drave

| biologie (mesuré) | Drave (mesuré) | ce que ça impose au modèle |
|---|---|---|
| énergie ∝ nombre de spikes × synapses actives | coût ∝ **paires (poids × activation)** | l'objectif d'entraînement doit être un **budget de paires**, pas une taille de modèle |
| taux de décharge **0,1-1 Hz**, ~1 % actif | densité mesurée **71 %** sur un modèle dense — et le croisement listes/dense est à **22-25 %** | un modèle dense ordinaire est **hors régime** : la sparsité doit être **apprise** (§ 5 ter de la campagne : à 25 % gardés, le témoin perd +118 %, le modèle entraîné s'améliore) |
| probabilité de connexion **~10 %**, ~7 000 synapses/neurone | le moteur compte les **non-nuls par ligne** (`row_ev`) ; `--keep` élagué à 50 % **ne coûte rien** en qualité (mesuré) | **la structure creuse est un paramètre de conception**, pas un artefact d'exécution |
| surproduction synaptique puis **élagage** développemental | `--elagage` : rampe cubique, même règle que `--keep` (implémenté le 9/10) | entraîner **dense puis élaguer** est la trajectoire biologique — et elle est déjà outillée |
| synapses **excitatrices / inhibitrices** (~80/20) | poids **signés** (`--poids-signes` dans le banc de décharge) | la contrainte de signe et la balance E/I sont un levier de stabilité à tester |
| câblage **local**, petit-monde, longueur minimisée | le moteur lit par défauts de page : **8,6 Mo/s** sur disque dur contre 243 Mo/s en séquentiel | un modèle **rangé par groupes d'événements** transformerait la lecture en séquentiel (×28 disponibles) |
| apprentissage **local**, pas de rétropropagation | la distillation est notre seul signal global (mesurée : elle rattrape le routage) | un modèle ad hoc devrait viser des **règles locales** + un signal diffus, pas un gradient par poids |
| **rejeu** hors ligne | le moteur écrit des **traces DRVF** et sait les **rejouer** (écart 0,00e0) | le rejeu est déjà un outil de première classe : consolidation, distillation de soi-même |
| **0,5 %** de variation développementale ; cerveaux similaires | nos modèles sont réentraînés de zéro à chaque fois | un **connectome de base partagé** est une hypothèse défendable — et vérifiable chez nous |
| cerveau : 20 W pour ~10¹⁵ synapses | notre niche : un modèle **plus gros que la RAM** qui ruisselle (365 Go sur 125 Go) | le streaming n'est pas une concession : c'est **le régime biologique** (le poids n'est jamais « chargé ») |

### 3 ter. Le fait biologique que nos modèles NE reproduisent PAS : des poids à queue lourde

C'est le fait le plus directement exploitable de tout ce document, et il se voit en
une commande.

**En biologie**, les efficacités synaptiques corticales ne sont pas distribuées
autour d'une moyenne : elles suivent une loi **log-normale**, sur plusieurs ordres de
grandeur — quelques synapses très fortes portent l'essentiel, la grande majorité est
faible ([Song, Sjöström, Reigl, Nelson & Chklovskii 2005](https://janeliafarm.org/publication/highly-nonrandom-features-synaptic-connectivity-local-cortical-circuits) ;
[implications computationnelles](https://ieeexplore.ieee.org/document/6767040) ;
[auto-organisation de la distribution](https://infoscience.epfl.ch/bitstreams/988897d4-089b-4c04-8ded-86e45b6fa304/download)).
C'est une distribution **multiplicative**, produite par des produits de variables
aléatoires (croissance, potentialisation, dépression).

**Chez nous**, mesuré sur les modèles entraînés de la campagne :

| modèle | \|w\| médian | p99,9 / médiane | poids sous **10 % du max de leur ligne** |
|---|---:|---:|---:|
| `m5_d384_dense` (témoin) | 0,1148 | **5,2** | **25,7 %** |
| `m7_d384_kwta025` (creux appris) | 0,1080 | **5,6** | **27,6 %** |

Une gaussienne donne un rapport p99,9/médiane de l'ordre de 4 ; **nos modèles sont
donc quasi gaussiens**, pas log-normaux. Conséquence directe, et elle explique une
mesure de la campagne : élaguer 50 % des poids **ne coûte rien** (les 50 % qui
restent portent presque toute l'énergie), mais élaguer à 25 % **effondre** le modèle
(+232 % de perplexité, § 6 de `modele-pour-drave.md`). Le cerveau, lui, est
élagable *par construction* : sa distribution est faite pour ça.

**Ce que cela donne comme dessin, et c'est inédit** : **paramétrer les poids en
log-magnitude** — apprendre `θ` et utiliser `w = signe(θ) · e^{|θ|}` — produit une
distribution **log-normale par construction** (c'est le générateur même de cette
loi). Le modèle apprendrait alors naturellement à concentrer le calcul sur peu de
connexions fortes, ce qui est exactement ce que le chemin par listes récompense, et
ce que l'élagage développemental exploite.

**Prédiction mesurable** : à budget d'événements égal, un modèle à poids
log-normaux doit **mieux supporter l'élagage** qu'un modèle gaussien.

**E6 A ÉTÉ TENTÉE, ET ELLE A ÉCHOUÉ — PAR UN DÉFAUT DE CODE, PAS PAR UN RÉSULTAT.**
La reparamétrisation `w = signe · e^{theta}` (signes figés à la naissance, magnitudes
apprises) a été écrite et entraînée (40 000 pas, dim 384) : la distribution obtenue
n'est d'ailleurs **toujours pas à queue lourde** (p99,9/médiane **5,5**, contre 5,2 au
témoin gaussien), et la qualité en validation est **nettement moins bonne** (2,2662
contre 1,9020 bits/octet). Mais surtout : **le modèle sauvegardé n'est pas le modèle
entraîné.**

| mesure | valeur |
|---|---|
| validation à l'entraînement | 2,2662 bits/octet (perplexité ≈ 4,8) |
| perplexité du modèle SAUVEGARDÉ, moteur | **8 668** |
| perplexité du modèle SAUVEGARDÉ, référence PyTorch (mêmes poids quantifiés) | **15 552** |
| échelle des poids linéaires sauvegardés | \|w\| max **0,453** — contre **1,89** pour le témoin |

La référence PyTorch sur les poids sauvegardés donne *pire* que le moteur : **ce n'est
pas le moteur, c'est le fichier.**

**Le premier soupçon a été testé et ÉLIMINÉ** : la matérialisation de la
reparamétrisation avant `save_pretrained` a été refaite en recalculant explicitement
`signes · clamp(theta, −12, 6).exp()` et en le **vérifiant** — écart mesuré avant
copie : **0,000e+00**, c'est-à-dire que la reparamétrisation était déjà cohérente. Le
défaut est donc **ailleurs**, et il reste ouvert : la piste la plus courte est
l'écart entre la validation d'entraînement (évaluée en fp32 sur le modèle vivant) et
le modèle *sauvegardé puis quantifié* — c'est-à-dire, une fois de plus, la
quantification et non l'entraînement.

**Et la mesure définitive, avec le protocole de l'entraînement lui-même** (même
corpus, mêmes fenêtres, même formule) : le fichier sauvé du témoin gaussien redonne
**exactement** sa validation (1,9020 bits/octet), celui du modèle log-normal donne
**13,0614** là où l'entraînement annonçait 2,2662. **Le fichier ne reproduit pas le
modèle entraîné**, et ce n'est ni le moteur (il exécute fidèlement ce qu'on lui
donne), ni la quantification (la référence PyTorch sur les mêmes poids donne 15 552),
ni la matérialisation (écart mesuré 0,000e+00). La cause reste **ouverte** ; le
variant est marqué inutilisable dans le harnais tant qu'elle ne l'est pas.

**E6 est donc INCONCLUSIVE : ni la prédiction, ni son contraire, ne sont établis** —
et c'est écrit comme tel plutôt que présenté comme un échec de la biologie. Deux
faits subsistent : la distribution obtenue n'est **pas** à queue lourde
(p99,9/médiane 5,5 contre 5,2 au témoin), et la validation d'entraînement est
nettement moins bonne (2,2662 contre 1,9020 bits/octet) — ce qui suggère que **figer
les signes coûte cher**, indépendamment du défaut de fichier.

---

## 3 bis. Le budget, chiffré : où nous en sommes

Deux calculs, faits avec les chiffres du § 1 et les mesures de la campagne. Ils sont
**d'ordre de grandeur** et comparent des substrats incomparables — c'est écrit à la
fin.

**Le cerveau.** ~16 × 10⁹ neurones corticaux, ~1 % actifs à un instant, ~0,5 Hz de
taux moyen, ~7 000 synapses par neurone :

    16×10⁹ × 0,5 Hz × 7 000 ≈ 5,6×10¹³ événements synaptiques par seconde

pour **20 W** (et le cortex n'en prend qu'une partie) :

    → ≈ 0,4 picojoule par événement synaptique

Ce chiffre recoupe la littérature : un événement synaptique coûte 10⁵ à 10⁷ molécules
d'ATP, soit **0,01 à 1 pJ** ([Attwell & Laughlin](https://rcseng.ovidds.com/discover/result?logSearchID=163215621&pubid=solr_6306-sage%3A10.1097%2F00004647-200110000-00001&pubid=solr_7902-info%3Adoi%2F10.1097%252F00004647-200110000-00001&pubid=solr_6057-medline%3A11598490)).

**Notre modèle le plus économe** (`m8_d512_kwta25` exécuté à 25 % d'activations et
50 % de poids, mesuré le 9/10) :

    201 308 279 événements pour 128 jetons ≈ 1,57 × 10⁶ événements par jeton
    à 213 jetons/s → 3,3 × 10⁸ événements par seconde

sur une machine qui consomme, en charge, de l'ordre de **300 W** (deux Xeon à
160 W de TDP, plus la mémoire et la carte) :

    → ≈ 0,9 microjoule par événement

**L'écart est de six ordres de grandeur (≈ 2 × 10⁶).** Et il ne dit *pas* que
l'algorithme est mauvais : dans les deux cas, le coût est **proportionnel au nombre
d'événements** — c'est la même loi. L'écart est dans le **substrat** : nos événements
sont exécutés par un processeur généraliste, un par un, avec du trafic mémoire ; ceux
du cerveau par du matériel analogique **colocalisé avec sa mémoire**.

**Ce que cela change dans la façon de concevoir** : la sparsité apprise fait gagner
×4 à ×8 sur les événements (§ 5 ter de la campagne, § 6 de `modele-pour-drave.md`) —
c'est réel, et c'est le levier que nous contrôlons. Mais **aucun gain algorithmique
ne comblera six ordres de grandeur** : ce que la biologie enseigne ici, c'est que
l'énergie se joue dans la **disposition** (mémoire proche du calcul), pas dans le
nombre d'opérations seul. Cela donne un argument de plus au dessin du § 4, et au
rangement des poids par groupes d'événements (§ 3, D de `modele-pour-drave.md`) :
moins de trafic, moins de joules.

**Les réserves, et elles sont lourdes** : un « événement synaptique » n'est pas une
multiplication-accumulation int8 ; le cerveau calcule en analogique, avec du bruit,
et sa « précision » n'est pas comparable ; les 300 W sont une estimation de TDP, pas
une mesure (aucun compteur RAPL exploité ici) ; et le cerveau fait mille autres
choses avec ses 20 W. **Ces deux nombres encadrent un ordre de grandeur, ils ne
comparent pas deux ordinateurs.**

---

## 4. Le dessin qui sort de là : **structure innée, poids appris**

C'est la question posée, et la biologie y répond assez précisément : le cerveau a un
**plan de câblage largement partagé** (§ 1.1), **très creux** (§ 1.4), dont les
poids se modifient localement, et dont une partie des connexions est **éliminée**
avec l'âge (§ 1.5).

Traduit en Drave, cela donne un objet qui **n'existe dans aucune bibliothèque**, mais
que notre moteur exécute *nativement* :

> Un modèle dont la **matrice de connexions est fixée à la naissance** (un masque
> creux, tiré une fois, partagé par toutes les instances), dont **seuls les poids des
> connexions existantes sont appris**, et dont le coût d'exécution est
> **structurellement borné** — sans aucun top-k à l'exécution, puisque les
> connexions absentes ne sont pas dans les listes d'événements.

**Pourquoi c'est le bon objet pour Drave, et pas seulement pour la biologie :**

1. **Le coût est connu à la compilation.** Le nombre de paires par jeton est borné
   par la densité du masque × les activations. On peut donc *concevoir* un modèle
   pour un budget d'énergie donné — ce que la biologie fait depuis toujours et que
   nos modèles font à l'envers (on entraîne, puis on mesure).
2. **Aucun top-k à l'exécution.** Le k-WTA appris (§ 5 ter) exige d'exécuter au taux
   appris, sinon le modèle se dégrade. Un masque inné supprime cette fragilité : le
   modèle *est* creux, il n'a pas à le devenir.
3. **Les listes d'événements du moteur sont exactement la structure du graphe.**
   `PushMat` stocke, pour chaque entrée, les sorties non nulles. Un graphe creux
   inné, c'est un `PushMat` **sans passe de quantification** — le format natif du
   moteur, appliqué au modèle entier.
4. **L'élagage développemental est le mécanisme de croissance.** On peut partir d'un
   masque **plus dense** (surproduction), entraîner, puis **élaguer** selon
   l'activité — la règle est celle du cerveau, et elle est implémentée
   (`--elagage`, rampe cubique, même sémantique que `--keep`).
5. **Le modèle peut être rejoué, tracé, découpé** : le moteur transporte des listes
   d'événements entre nœuds (écart 0,00e0) ; un graphe creux est *déjà* une
   répartition naturelle par unités.

**Ce qui n'est PAS résolu par ce dessin** : comment apprendre un masque *utile* sans
gradient global (le cerveau utilise des règles locales, nous avons la
rétropropagation — c'est une facilité qu'il ne faut pas confondre avec une
nécessité) ; et comment croître **sans réentraîner** (le cerveau ajoute des synapses
localement).

### 4 bis. E1 — le résultat : un connectome inné ALÉATOIRE coûte 1 %

Mesuré le 9 octobre à 12 h 06. Même modèle que le témoin dense (dim 384, 4 couches,
40 000 pas, mêmes données, même export Q8), **sauf** qu'un quart des connexions de
chaque ligne est tiré **au hasard à la naissance** et ne change plus jamais — seuls
les poids des connexions existantes sont appris.

| dim 384, 8 × 128 jetons | perplexité | **événements/fenêtre** | débit |
|---|---:|---:|---:|
| témoin dense (toutes les connexions) | **4,9959** | 336,7 M | 131,4 tok/s |
| **connectome inné à 25 %** (aléatoire, figé) | **5,0472** (+1,0 %) | **81,6 M (÷4,1)** | **276,2 tok/s (×2,1)** |

**Un pour cent de perplexité pour quatre fois moins de lectures et deux fois plus de
débit.** Et c'est un masque **aléatoire** : la structure n'a pas eu besoin d'être
apprise ni optimisée. La validation à l'entraînement suit (2,0413 contre 1,9020 pour
le témoin, soit +7 % en bits/octet là où le moteur ne mesure que +1 % de perplexité —
l'écart entre les deux unités est le même qu'au § 5 bis de la campagne).

**Ce que cela établit** : la thèse du § 4 — *structure innée, poids appris* — tient
pour un modèle de cette taille, sur cette tâche, avec un masque tiré au hasard. Le
coût d'exécution est **borné dès la conception** (81,6 M d'événements au lieu de
336,7 M), sans aucun top-k à l'exécution, donc sans la fragilité du « exécuter au
taux appris » (§ 5 ter de la campagne).

**Et la limite apparaît à 12,5 %** (mesuré à 13 h 18) : le même masque inné, mais
deux fois plus creux —

| dim 384, 8 × 128 | perplexité | événements/fenêtre | débit |
|---|---:|---:|---:|
| témoin dense | **4,9959** | 336,7 M | 131 tok/s |
| masque inné **25 %** | 5,0472 (+1,0 %) | 81,6 M | 276 tok/s |
| masque inné **12,5 %** | **5,6810 (+13,7 %)** | **40,6 M** | **341 tok/s** |

**La structure innée est presque gratuite jusqu'à 25 %, et coûte cher à 12,5 %.** Le
mur est entre les deux — et c'est une information de conception : un connectome inné
doit viser un quart des connexions, pas un huitième.

**Ce que cela n'établit pas** : qu'un masque *appris* ne ferait pas mieux (l'écart de
1 % à 25 % est peut-être récupérable), ni que le résultat tient à d'autres échelles.

---

## 5. L'axe « génie / idiot » : ce que la littérature dit vraiment

La question posée est brutale, et la littérature l'est moins. Ce qui est documenté :

- **La taille explique peu.** Le volume cérébral corrèle faiblement avec les
  performances cognitives à l'échelle des individus.
- **Ce qui corrèle mieux** : l'**efficacité de réseau** (chemins courts, forte
  modularité, connectivité globale intégrée mesurée en IRM de diffusion), l'épaisseur
  corticale régionale, et surtout **la trajectoire de développement** (myélinisation,
  élagage).
- **Les variations extrêmes** de développement cognitif sont associées à des
  **atypies de connectivité et d'élagage**, pas à un déficit de « matière grise »
  globale.
- Les études sur des cerveaux de génies (Einstein inclus) reposent sur des cas
  uniques, avec des critiques méthodologiques sérieuses — **elles ne fondent rien**.

**Traduction honnête pour nous** : « génie ou idiot » n'est pas un paramètre de
taille, c'est un paramètre de **structure et de trajectoire** — densité de
connexions, efficacité des chemins, et surtout **ce qui est élagué et quand**.
C'est exactement le dessin du § 4, et c'est **mesurable** chez nous : à budget de
paires égal, un masque inné bien choisi vaut-il un masque aléatoire ? Et l'élagage
appris vaut-il mieux qu'un masque fixé au départ ?

---

## 6. Les expériences que nos outils permettent de faire maintenant

Aucune ne demande de nouveau moteur : le harnais d'entraînement (`--kwta`,
`--elagage`), l'exporteur et le protocole 8 × 128 suffisent.

| # | expérience | ce qu'elle teste | coût |
|---|---|---|---|
| **E1** | **masque inné creux** : masque aléatoire fixe à **25 %** des connexions par ligne, seuls ces poids sont appris, mesuré au protocole 8 × 128 contre un dense iso-tout | la structure fixe suffit-elle, ou faut-il apprendre *où* sont les connexions ? | **FAIT — voir § 4 bis** |
| **E2** | **croissance** : partir de 10 % de connexions, en **ajouter** selon l'activité (règle locale : une connexion naît là où deux neurones s'activent ensemble), mesurer la trajectoire | l'inné + la croissance locale peuvent-ils remplacer l'apprentissage global des poids ? | ~2 h, règle locale à écrire |
| **E3** | **élagage développemental** : dense → élagage appris à 50 % puis 25 % (§ déjà outillé) | la trajectoire biologique (surproduire puis élaguer) bat-elle l'entraînement creux direct (`--kwta`) ? | **déjà en file** (`m11`, chaîne jour3) |
| **E4** | **balance excitation/inhibition** : contrainte de signe sur les poids (80 % excitateurs / 20 % inhibiteurs), mesurer stabilité et qualité | la séparation E/I est-elle un levier de stabilité à long entraînement ? | le banc `--poids-signes` existe ; à porter dans l'entraînement |
| **E5** | **rejeu** : tracer une passe (DRVF), la rejouer, et distiller le modèle *sur ses propres traces* | le rejeu améliore-t-il la consolidation (comme le sommeil) ? | le moteur trace et rejoue déjà ; l'outil de distillation existe |
| **E6** | **poids log-normaux** : apprendre `θ`, exécuter `w = signe(θ)·e^{\|θ\|}`, puis élaguer à 50 % et 25 % | une distribution multiplicative (celle du cerveau) rend-elle l'élagage gratuit, là où la nôtre est quasi gaussienne (p99,9/médiane 5,2) ? | ~1 h 30 ; une reparamétrisation + `--elagage` |

**La première à faire est E1** : c'est la moins chère, elle teste directement la
thèse « structure innée, poids appris », et elle se mesure avec le protocole de
record de la campagne.

---

## 7. Ce que ce document ne dit pas

- Aucune de ces expériences n'a été faite : **tout le § 4 est un dessin**, appuyé sur
  des mesures biologiques et sur les mesures de la campagne, pas sur un résultat.
- Les chiffres biologiques cités sont des **ordres de grandeur** publiés, avec leur
  source ; ceux du cerveau humain (86 G neurones, 10¹⁴-10¹⁵ synapses) sont des
  estimations, pas des comptages, et le connectome humain n'existe pas.
- Le passage « connectome → modèle entraînable » est **notre interprétation** : la
  biologie ne dit pas qu'un masque creux fixe est suffisant, elle dit qu'il est
  **très creux**, **partagé**, **local** et **élagué**.
- Et une limite qui compte : la biologie **n'utilise pas** la rétropropagation. Rien
  ne dit qu'un modèle qui l'utilise doive ressembler à un cerveau — seulement que le
  **budget énergétique** qu'elle respecte est une contrainte que nous pouvons, pour
  la première fois, exécuter fidèlement.

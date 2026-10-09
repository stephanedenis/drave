# Plan détaillé — les capacités manquantes à Drave pour simuler un cerveau

> 9 octobre 2026. Complète `docs/architecture-cerveau-et-drave.md` (qui établit *ce
> qui* manque et *pourquoi*) par un plan d'ingénierie : douze capacités, leur
> conception, leur interface, l'invariant qui les rend vérifiables, la mesure qui les
> valide, leur coût et leur risque — puis les phases, et le détail de la
> **distribution sur plusieurs instances de Drave, sur plusieurs machines**.

---

## 0. État des lieux : ce que Drave est aujourd'hui, exactement

| ce qui existe | ce que ça vaut, mesuré |
|---|---|
| **exécution par listes** (paires = poids × activation) | déterministe et **exacte** : logits identiques au bit près contre le chemin dense, à encodage de poids égal |
| **découpage à deux nœuds** (`--flux-serveur`, `--ppl-reparti`, modes 0-4) | écart **0,00e0** (modes 0, 1, 3), 3,65e-2 (mode 2), 4,45e-3 (mode 4) ; protocole TCP, exact à toute latence |
| **coût d'un lien** | **3,4 ms par jeton et par ms d'aller-retour** ; plancher localhost ×3,5 à ×5,3 |
| **experts** (clusters, nœud partiel) | 2,36 Go pour un huitième des experts ; mais **chemin par listes impossible** (le chargeur refuse Q8_0) |
| **mémoire adressable** (`engram.rs`) | 479 723 rangées distinctes, injection branchée |
| **traces et rejeu** (DRVF) | rejeu **exact** (0.00e0) |
| **plasticité locale** (`--hebb-diff`) | applique, mesure, sauve, recharge — et **réfutée** en l'état |
| **structure creuse** (`--kwta`, `--elagage`, `--masque`) | ÷8 lectures pour +3,8 % de perplexité (deux axes **appris**) |
| **GPU** (`gpu.rs`) | projections Q8 ≥ 8 Mio, KV, top-k, experts MXFP4/Q4_K — **dense uniquement**, et nos modèles sont trop petits |

**La forme générale** : le moteur est une **chaîne** de couches, exécutée de façon
**synchrone**, avec un transport exact vers **un** pair. Un cerveau est un **graphe**
de régions, **asynchrone**, avec des **délais**, **deux mémoires** et une
**périphérie**. Tout le plan consiste à passer de l'un à l'autre sans jamais perdre
les invariants d'exactitude qui font la valeur du dépôt.

---

## 1. Les douze capacités manquantes

Chaque fiche : **structure cérébrale** → **état du moteur** → **conception** →
**interface** → **invariant vérifiable** → **mesure de validation** → **coût** →
**risque**.

### C1 — Graphe de régions (topologie arbitraire)

- **Cerveau** : 180 aires corticales par hémisphère, connectées en graphe, pas en chaîne.
- **Moteur** : `--couches-locales N` découpe une **plage contiguë** ; le flux va d'un
  producteur à un consommateur, dans l'ordre des couches.
- **Conception** : un **descripteur de topologie** (JSON) déclarant des *régions*
  (`{id, couches:[i..j], instance, poids}`) et des *liens* (`{de, vers, type,
  délai_ms, budget}`). Le pilote exécute un **graphe acyclique ordonnancé par
  dépendances**, chaque région étant une instance existante du moteur.
- **Interface** : `--topologie cerveau.json` ; `--region <id>` pour lancer une
  instance qui *est* une région.
- **Invariant** : sur une topologie **linéaire**, les logits sont identiques au bit
  près à aujourd'hui (la chaîne est un cas particulier du graphe) — c'est la porte de
  non-régression.
- **Validation** : le graphe linéaire redonne 0,00e0 ; puis un graphe en « Y »
  (deux régions qui alimentent une troisième) est comparé à un modèle équivalent
  exécuté d'un seul tenant.
- **Coût** : 2-3 semaines. **Risque** : moyen — c'est de l'ordonnancement, pas du calcul.

### C2 — Liens multiples et récurrence

- **Cerveau** : chaque aire reçoit de plusieurs sources, et les boucles
  cortico-thalamo-corticales dominent.
- **Moteur** : une couche a **une** entrée (le résidu) ; aucune récurrence.
- **Conception** : une région peut déclarer **plusieurs entrées** ; l'agrégation est
  déclarée (somme, concaténation, porte apprise) — et la **récurrence** exige un
  ordonnancement par *pas de temps* : une région peut consommer sa propre sortie du
  pas précédent (état explicite par région).
- **Interface** : `entrees: [{de, mode: "somme"|"concat"|"porte", delai_ms}]` ;
  `recurrent: true` avec état persisté (`--etat <fichier>`).
- **Invariant** : sans délai et sans récurrence, C1 s'applique (0,00e0).
- **Validation** : un cycle à deux régions, comparé à une implémentation de référence
  en une seule passe sur 4 pas de temps.
- **Coût** : 2 semaines après C1. **Risque** : élevé — c'est là qu'on quitte la
  certitude « une passe = un résultat ».

### C3 — Délais par lien

- **Cerveau** : conduction de 1 à 100 ms ; le temps porte de l'information.
- **Moteur** : la latence existe (mesurée), mais elle **coûte** au lieu de *servir*.
- **Conception** : une **file temporisée** par lien (`delai_ms`), alimentée par les
  messages et vidée par l'horloge locale de la région consommatrice. Le coût est
  connu d'avance : 3,4 ms/jeton/ms de RTT.
- **Interface** : `delai_ms` dans le lien ; `--horloge-pas <ms>` pour un pas de temps
  simulé.
- **Invariant** : à `delai_ms = 0`, comportement identique à C1.
- **Validation** : mesurer la courbe débit ↔ délai (l'outil existe :
  `tools/carte_latence.sh`, relais TCP `tools/proxy_latence.py`) et vérifier que la
  perplexité **ne bouge pas** quand les délais changent (elle ne bougeait pas jusqu'à
  50 ms par message dans nos mesures).
- **Coût** : 1 semaine. **Risque** : faible techniquement, élevé scientifiquement
  (rien ne garantit que le temps *serve*).

### C4 — Horloges par région (asynchronisme)

- **Cerveau** : aucune horloge globale.
- **Moteur** : passe synchrone par jeton, barrières implicites.
- **Conception** : chaque région cadence ses pas ; les barrières ne subsistent que là
  où un calcul l'exige (agrégation de plusieurs entrées). Un **jeton** devient un
  *événement horodaté* circulant dans le graphe.
- **Interface** : `--asynchrone`, `--pas-max <n>` (garde-fou de terminaison).
- **Invariant** : terminaison bornée (pas de blocage) — test de vivacité, plus une
  comparaison exacte avec la version synchrone sur un graphe sans cycle.
- **Coût** : 3 semaines. **Risque** : élevé — c'est le cœur du changement de nature.

### C5 — Bus de modulation (scalaire diffusé)

- **Cerveau** : quelques dizaines de milliers de neurones modulent tout le reste.
- **Moteur** : **amorcé** — `DRAVE_HEBB_MODULE=valeur`, modulateur externe par
  fichier (`DRAVE_HEBB_MODULATEUR_FICHIER`), retard d'un jeton.
- **Conception** : un **bus multi-canaux** (`recompense`, `nouveaute`, `incertitude`,
  `erreur`), diffusé à toutes les régions, y compris **entre instances** (un message
  de contrôle, pas de données). Chaque région décide comment l'utiliser.
- **Interface** : `--bus <hôte:port>` ; CLI `moduler: canal=valeur`.
- **Invariant** : à canal nul, sortie inchangée (le bus n'entre pas dans le calcul,
  seulement dans les taux d'apprentissage).
- **Validation** : nos mesures sont déjà négatives et instructives — nouveauté
  +20,4 %, valeur propre +15,3 %, signal **externe** +9,1 %, règle nue +5,2 %,
  référence 0. **Aucun modulateur scalaire ne sauve la règle locale** : le bus est
  nécessaire mais pas suffisant, et le plan doit le dire.
- **Coût** : 1 semaine (mécanique) + l'inconnue du signal. **Risque** : élevé sur le
  fond, faible sur la forme.

### C6 — Mémoire épisodique adressable par contenu

- **Cerveau** : hippocampe, écriture en un coup, lecture par similarité.
- **Moteur** : `engram.rs` adresse par **hachage** (déterministe), le cache KV est
  indexé par **position**.
- **Conception** : un magasin clé/valeur où la clé est un **vecteur creux** (les
  activations d'un épisode), la lecture un **plus proche voisin approximatif**
  (LSH sur les mêmes hachages que l'engram), et l'écriture **une seule passe**.
- **Interface** : `--episodique <fichier>` ; `ecrire`/`lire` exposés au graphe comme
  une région.
- **Invariant** : une écriture suivie d'une lecture avec la **même** clé rend
  exactement la valeur écrite (test de round-trip, comme la porte de rejeu).
- **Validation** : retrouver un épisode parmi N (courbe de rappel), et mesurer le
  coût par lecture en paires.
- **Coût** : 2-3 semaines. **Risque** : moyen.

### C7 — Consolidation (rejeu → poids)

- **Cerveau** : le rejeu pendant le sommeil consolide l'épisodique dans le cortical.
- **Moteur** : le rejeu est **exact** (DRVF, 0.00e0) et la distillation marche
  (−13,8 % sur un modèle routé) — mais **hors moteur**.
- **Conception** : une boucle interne : rejouer une trace → calculer la perte → mettre
  à jour les poids (par gradient local sur la couche visée, ou par distillation d'un
  enseignant résident). Le point dur est **où** vivent les gradients : le moteur
  n'entraîne rien aujourd'hui.
- **Interface** : `--consolider <trace.drvf> --pas N --taux <lr>`.
- **Invariant** : après consolidation à taux nul, le modèle est **bit à bit** identique.
- **Validation** : la perplexité baisse-t-elle sur un jeu **non rejoué** ? C'est la
  seule question, et c'est un protocole qu'on sait déjà monter (`rapport-modele-moteur`).
- **Coût** : 4-6 semaines. **Risque** : élevé — c'est de l'apprentissage dans le moteur.

### C8 — Périphérie (capteurs, effecteurs, réflexes)

- **Cerveau** : rétine → nerf optique (1,2 × 10⁶ axones) ; moelle épinière qui décide seule.
- **Moteur** : un banc vision (embedding de patchs) ; rien ne sort.
- **Conception** : des **régions frontière** : entrée (flux continu, horloge propre) et
  sortie (effecteur, avec délai) ; les **réflexes** sont des liens qui court-circuitent
  le centre (une région répond à une entrée sans passer par le graphe profond).
- **Interface** : `--entree <type:chemin>`, `--sortie <type:fichier>`, `--reflexe
  <de:vers>`.
- **Invariant** : une entrée constante produit une sortie constante (déterminisme).
- **Validation** : une tâche fermée (contrôle d'un signal simple) où l'on mesure le
  **nombre d'événements par décision** — la métrique du projet.
- **Coût** : 3 semaines. **Risque** : moyen.

### C9 — Latéralité et corps calleux

- **Cerveau** : deux hémisphères, ~2 × 10⁸ axones, connexions homotopiques.
- **Moteur** : on sait découper une plage de couches entre deux nœuds ; pas de
  duplication miroir ni d'échange massif.
- **Conception** : deux **instances jumelles** du même modèle, un lien
  **homotopique** par couche (échange d'activations), avec bande passante déclarée.
  C'est un cas particulier de C1 (graphe symétrique).
- **Interface** : `--jumeau <hôte:port> --echange <couches|experts>`.
- **Invariant** : échange désactivé ⇒ chaque instance est identique au modèle seul.
- **Validation** : gain de perplexité **ou** de robustesse (entrée dégradée d'un côté)
  — et si le gain est nul, **le dire** (c'est le cas le plus probable : rien dans nos
  mesures ne suggère un gain).
- **Coût** : 1-2 semaines après C1. **Risque** : faible techniquement, gain incertain.

### C10 — Budgets par lien (bande passante, énergie)

- **Cerveau** : 20 W pour tout ; le câblage est minimisé.
- **Moteur** : il **mesure** octets, paires, temps par lien ; il n'impose rien.
- **Conception** : un **planificateur** qui refuse un graphe dont le coût dépasse un
  budget (`{paires/s, octets/s, watts}` par lien et global). Les mesures existantes
  (0,210 ns par événement valorisé, 8,6 Mo/s en mmap sur disque dur, 3,4 ms par
  jeton et par ms de RTT) donnent les constantes.
- **Interface** : `--budget budget.json` ; refus explicite au démarrage si dépassé.
- **Invariant** : le coût estimé est **comparable au coût mesuré** à ±20 % (sinon le
  modèle de coût est faux, et c'est consigné).
- **Validation** : sur les graphes déjà mesurés (2 nœuds, modes 0-4), l'estimation
  doit retrouver les mesures.
- **Coût** : 2 semaines. **Risque** : faible.

### C11 — Instances multiples concertées (le substrat distribué)

Voir § 3 : c'est la capacité qui porte toutes les autres, et elle mérite son propre
plan.

### C12 — Observabilité unifiée (traçage distribué)

- **Cerveau** : pas d'équivalent — mais sans elle on ne débogue pas un graphe.
- **Moteur** : traces DRVF **locales**, exactes, rejouables ; mesures par lien.
- **Conception** : une **trace globale** où chaque événement porte
  `(région, pas de temps, lien, horodatage)`, agrégée par un collecteur ; le rejeu
  global doit reproduire une exécution distribuée **au bit près** (on sait déjà le
  faire pour une chaîne).
- **Interface** : `--trace-globale <fichier>` ; `--rejouer-globale <fichier>`.
- **Invariant** : rejeu global = exécution originale, 0,00e0.
- **Coût** : 2 semaines. **Risque** : faible.

---

## 2. Les phases, avec leurs portes

Aucune phase ne commence avant que la précédente ait **sa porte verte**, et chaque
porte est une **égalité mesurée**, pas une impression.

| phase | contenu | porte | durée |
|---|---|---|---|
| **P0** | descripteur de topologie + graphe linéaire (C1) | graphe linéaire ⇒ **logits identiques au bit près** à aujourd'hui | 2-3 sem. |
| **P1** | entrées multiples + horloges + délais (C2, C3, C4) | délai 0 et pas unique ⇒ 0,00e0 ; terminaison bornée | 4-5 sem. |
| **P2** | instances multiples et trace globale (C11, C12) | une exécution sur 3 machines se **rejoue** à 0,00e0 | 4 sem. |
| **P3** | mémoire épisodique + consolidation (C6, C7) | round-trip exact ; puis perplexité hors rejeu | 6-8 sem. |
| **P4** | bus de modulation généralisé (C5) | canal nul ⇒ sortie inchangée ; et un signal qui **améliore** (aujourd'hui : aucun) | 1 sem. + recherche |
| **P5** | périphérie et réflexes (C8) | entrée constante ⇒ sortie constante ; tâche fermée mesurée | 3 sem. |
| **P6** | latéralité et budgets (C9, C10) | échange désactivé ⇒ identique ; estimation de coût à ±20 % | 3 sem. |

**Total réaliste : 5 à 7 mois** pour un moteur qui *peut* porter une architecture de
cerveau — et **aucune** de ces phases ne garantit qu'un tel modèle soit meilleur
qu'un transformeur sur une tâche donnée. C'est dit au § 5.

---

## 3. La distribution sur plusieurs instances, sur plusieurs machines

C'est la partie que la question demandait explicitement. Voici le plan.

### 3.1 Ce qui existe déjà, et qui est réutilisable tel quel

- **Un protocole de flux exact** : le nœud (`--flux-serveur`) applique une plage de
  couches ; le pilote (`--ppl-reparti`, `--couches-locales`) lui envoie les
  activations. Cinq modes (0 : f32 dense, 1 : listes quantifiées, 2 : listes par
  blocs, 3 : lot dense, 4 : lot en listes), écarts mesurés **0,00e0 / 0,00e0 /
  3,65e-2 / 0,00e0 / 4,45e-3**.
- **`TCP_NODELAY`**, échelles par bloc, bornes d'allocation (règle R4 : plafond de
  256 Mo pour toute allocation pilotée par le réseau).
- **Un instrument de latence** : `tools/proxy_latence.py` (relais TCP avec délai
  réglable) et `tools/carte_latence.sh` (balayage), qui ont donné la loi
  **3,4 ms par jeton et par ms de RTT**.
- **Le découpage par experts** (`clusters.rs`) : un fichier par grappe, un nœud peut
  ne charger qu'un huitième des experts (2,36 Go mesurés).

### 3.2 Ce qui manque, capacité par capacité

| manque | aujourd'hui | conception |
|---|---|---|
| **topologie** | 1 producteur → 1 consommateur, plage contiguë | descripteur JSON (C1), N régions, liens typés |
| **découverte** | adresse écrite à la main (`hôte:port`) | registre statique (fichier partagé) puis dynamique (`--registre hôte:port`, heartbeat 1 s) |
| **plusieurs pairs** | une connexion par nœud | une connexion **par lien**, avec identifiant de région ; les messages portent `(source, destination, pas)` |
| **ordonnancement** | ordre des couches | ordonnanceur par **dépendances** + pas de temps (C1, C4) |
| **état par région** | cache KV local au nœud | état déclaré et persisté par région (`--etat`), pour la récurrence |
| **pannes** | le pilote échoue | politique déclarée : `requis` (échec global), `best-effort` (la région est sautée, l'écart est **annoncé**, jamais silencieux) |
| **budgets** | aucun | `{paires/s, octets/s, ms}` par lien, vérifiés au démarrage (C10) |
| **observabilité** | mesures locales | trace globale horodatée + rejeu global à 0,00e0 (C12) |
| **hétérogénéité** | threads/GPU par instance | déclaration des ressources par instance (`materiel.rs` existe) et affectation région↔ressource |

### 3.3 Le protocole, en détail

1. **Trame** : `[magie u32][version u16][type u8][région u16][pas u32][longueur u32][charge]`,
   types : `ACTIVATIONS` (mode 0-4 existant), `HORLOGE` (avance de pas), `MODULATION`
   (un scalaire par canal), `EPISODE` (clé/valeur), `FIN`, `ERREUR`.
2. **Ordre et fiabilité** : TCP par lien ⇒ ordre garanti par lien ; **aucun ordre
   global** (c'est voulu : les régions sont asynchrones). Un numéro de pas permet de
   détecter les retards et de les **compter** (métrique : messages en retard par pas).
3. **Contre-pression** : une région qui ne peut pas suivre **refuse** (fenêtre de
   crédits par lien, comme la règle R4) ; elle ne perd jamais un message en silence.
4. **Délais** : un message `ACTIVATIONS` porte son horodatage d'émission ; la région
   consommatrice le place dans sa **file temporisée** et ne le lit qu'à `t + delai_ms`.
   Le relais TCP de test peut simuler le délai sans changer le moteur.
5. **Modulation** : un canal par connexion de contrôle (UDP suffirait, perte
   tolérée — on l'annonce), valeur normalisée dans `[0, 4]`, comme aujourd'hui.
6. **Panne** : heartbeat par région ; au-delà de 3 s, la région est déclarée morte ;
   la politique du lien décide, et **l'écart de perplexité est mesuré et publié**
   (comme pour le mode 2, toléré à 3,65e-2).
7. **Reprise** : une région peut redémarrer et **recharger son état** ; le rejeu
   global (C12) est le mécanisme de vérification.

### 3.4 Comment le développer et le valider sur UNE SEULE machine

C'est le point pratique : nous n'avons qu'une machine, et cela suffit pour tout le
développement — les mesures de latence le prouvent (un relais local ajoute des
millisecondes réglables, et nous avons déjà tracé la courbe jusqu'à 50 ms par message).

| étape | dispositif | ce qui est vérifié |
|---|---|---|
| **V1** | 2 instances, loopback, mode 1 | 0,00e0 (déjà acquis) |
| **V2** | 3 instances, topologie en Y, mode 1 | égalité avec le modèle d'un seul tenant |
| **V3** | idem **derrière le relais à délai** (0 / 1 / 5 / 20 ms) | perplexité **inchangée** ; débit conforme à 3,4 ms/jeton/ms |
| **V4** | une instance tuée en cours d'exécution | la politique annoncée est appliquée ; l'écart est mesuré |
| **V5** | rejeu global d'une exécution à 3 instances | **0,00e0** |
| **V6** | les mêmes, sur la carte 4×NVMe et les deux sockets NUMA | l'effet du tissu (bande passante, latence NUMA) sur le coût par événement |

**Le vrai passage à plusieurs machines** ne change qu'une constante : la latence. Or
nous avons déjà la loi qui la relie au coût (3,4 ms/jeton/ms), et l'instrument qui la
simule. **La distribution multi-machines est donc entièrement développable ici** — ce
qui manque n'est pas le matériel, c'est le code.

---

## 4. Le premier sprint recommandé (3 semaines)

Trois capacités seulement, choisies parce que **nos mesures les réclament** :

1. **C1 (graphe, graphe linéaire d'abord)** — sans topologie, rien d'autre n'est
   possible ; et sa porte (0,00e0 sur le cas linéaire) est immédiate.
2. **C5 (bus de modulation généralisé)** — la mécanique est déjà là ; il reste à en
   faire un bus multi-canaux inter-instances. Notre mesure dit que le signal scalaire
   ne suffit pas, mais **elle dit aussi quelle expérience monter** (un signal externe
   d'un autre modèle : +9,1 % contre +5,2 % pour la règle nue — le meilleur des
   modulateurs, et le seul qui mérite d'être poussé).
3. **C12 (trace globale + rejeu)** — parce que sans elle, un graphe distribué n'est
   pas débogable, et parce que la porte (rejeu à 0,00e0) est celle que le dépôt sait
   déjà tenir.

**Ce que ce sprint ne fait pas** : ni mémoire épisodique, ni consolidation, ni
périphérie, ni latéralité. Elles attendent qu'un **modèle** les réclame.

---

## 5. Ce que ce plan ne donne pas — et il faut le lire

- **Aucune garantie qu'une architecture de régions soit meilleure** qu'un empilement
  de couches sur une tâche donnée. Aucun modèle n'existe aujourd'hui qui demande un
  graphe, des délais ou une périphérie. Construire les six phases sans modèle, c'est
  construire une route sans véhicule.
- **La biologie ne fournit pas les hyperparamètres.** Elle fournit des ordres de
  grandeur (creux, local, deux mémoires, délais) et une contrainte (20 W), pas un
  plan de modèle.
- **Le moteur n'apprend pas.** C7 (consolidation) est le vrai saut, et c'est celui
  dont on sait déjà qu'il est difficile : notre seule règle locale a été réfutée, et
  aucun modulateur scalaire ne l'a sauvée.
- **Et une limite de méthode** : tout ce plan est un plan. Sur douze capacités,
  **zéro** est implémentée à ce jour, et les mesures qui le justifient sont celles de
  la campagne — pas celles d'un cerveau simulé.

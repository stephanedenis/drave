# Programme de recherche — vers une intelligence locale

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

**Objet.** Définir une feuille de route vérifiable vers un système capable
d'apprendre et d'évoluer *localement*, sur du matériel qu'une personne possède,
sans centre de données. Ce document ne promet pas l'AGI : il définit des paliers
**mesurables** et nomme ce qui, aujourd'hui, n'est pas démontré.

**Règle du programme.** Chaque affirmation est mesurée, chaque erreur est
consignée. Sept affirmations de ce projet ont déjà été retirées ou corrigées
(encodage ×2,17 retiré pour violation de Kraft, divergence fantôme, tokenizer
non conforme, roofline corrigée, coût du mode liste inversé, 4 bits sans gain).
C'est la méthode, pas un accident : **une trace de recherche qui ne contient pas
ses erreurs ne vaut rien.**

---

## 1. Thèse

Une intelligence locale doit être **traçable**, **incrémentale**, **bornée en
énergie** et **capable d'évoluer sans salle machine**. Les piles denses
généralistes optimisent une seule de ces dimensions — le débit par dollar de
calcul — et sacrifient les trois autres.

L'architecture événementielle défendue ici possède quatre propriétés
structurelles que ces piles n'ont pas :

1. **Traçabilité par construction.** Le calcul *est* une liste d'événements de
   cause à effet explicites : chaque sortie est la somme de contributions
   nommées. Journaliser les listes d'activations (1,2 Mo/token, **+3,0 %**)
   suffit à rejouer intégralement le raisonnement — les poids sont statiques et
   les événements en sont une fonction déterministe
   (`reports/rapport-programme-evolutif.md`).
2. **Le coût suit ce qui tire.** Un poids nul coûte zéro octet ; un expert qui ne
   se déclenche pas coûte zéro octet ; un motif non activé n'est jamais lu. Un
   modèle à cent experts dont deux tirent coûte le prix de deux.
3. **La récursion échange du calcul contre de la mémoire.** Le moteur mesuré est
   borné par la dispersion (10,4 Go/s utilisés sur 28,7) : **2,8× de marge
   mémoire** pour ~2,8 passes supplémentaires à paramètres constants.
4. **Le flux se route.** Une liste est une **unité de travail autonome** : elle a
   ses entrées, sa sortie et sa dépendance (les poids d'une couche), donc elle se
   place — sur un composant (CPU, GPU, FPGA) ou sur une autre machine — là où son
   coût est le plus faible. C'est ce que la vision appelle les **grappes de
   neurones** : le moteur ne répartit pas des matrices, il route des listes
   (`docs/vision.md` §3-§4), et le découpage en clusters d'experts le fait déjà
   sans changer un chiffre (Qwen3-30B : **origine 15,2789 · clusters 15,2789**,
   mêmes 63 jetons, même contexte — `docs/format-clusters.md`).

Ces quatre propriétés ne sont pas des opinions : elles sont mesurées, et elles
définissent ce que le programme peut tenter que d'autres ne peuvent pas.

## 2. Point de départ mesuré

| Acquisition | Valeur |
|---|---|
| Inférence 0,5 B quantifié, CPU seul, sans GPU ni BLAS | **15,8 tok/s**, perplexité 24,90 (référence float32 : 25,00) — et **5,3 G événements/s** : le coût suit l'activité (`reports/rapport-inference.md`) |
| Exactitude | 16/16 tokens identiques à la référence numpy, 14/14 au banc des décodeurs |
| Moteur d'événements | 5,3 G événements/s, 2 547 lignes de Rust sans dépendance |
| Carte FPGA | PE vérifié sur 309 020 événements réels, synthétisé (176 ALMs, 0 DSP), lecteur DDR3 vérifié de bout en bout |
| GPU | 380 Go/s, 18,1 G événements/s de dispersion, consomme les mêmes listes |
| Journalisation | +3,0 %, digest versionnable, archive automatique |
| Capacité d'évaluation | **~100 évaluations de modèle par heure** sur les threads libres, soit 2 400/jour |
| Ressources libres | 24 threads sur 40, une carte GPU sur deux, 123 Go de RAM sur 125 |

## 2 bis. Ce que la littérature neuromorphique change

Comparaison détaillée dans [`comparaison-spiking.md`](comparaison-spiking.md).
Trois enseignements qui modifient ce programme :

1. **Les réseaux à spikes résolvent par construction notre problème de débit
   constant.** Nous mesurons 0,00 % d'activations nulles sur un LLM dense ; un
   neurone LIF décharge à R̂ ≈ 0,15 (SpikeGPT) — soit **6,7× moins d'événements**
   dans notre moteur, donc ~100 tok/s sur CPU au lieu de 15,8.
2. **L'astuce décisive est l'alignement séquence = temps** (SpikeGPT). Chez
   Spikformer, la parcimonie est par pas de temps et le gain net est R̂×T, pas
   R̂ : sans cet alignement, les pas de temps mangent le gain.
3. **L'attention sans softmax et décomposable** (Spikformer) répond à notre trou
   le plus sérieux : `SN(Q·Kᵀ·V·s)` supprime le softmax, ramène la complexité à
   O(N·d²) et rend l'attention exprimable en événements.

➡️ **La cible devient « un modèle à décharge parcimonieuse exécuté en listes »**,
pas « un LLM quantifié exécuté en listes ». Seule la première donne le débit
variable que le cahier des charges promettait.

## 2 ter. Ce que la campagne de parcimonie a appris

Campagne complète : [`rapport-campagne-parcimonie.md`](../reports/rapport-campagne-parcimonie.md).
Quatre enseignements, dont un qui change la méthode.

1. **La parcimonie ne s'impose pas, elle s'entraîne.** Nous plafonnons à −4 à
   −15 % d'événements pour +0,5 % de perplexité, là où un réseau entraîné à
   décharger atteint R̂ = 0,15 (6,7×). L'écart est exactement le prix de
   l'entraînement : un réseau dense répartit son information partout, couper
   après coup détruit du signal.
2. **Ce qui est surabondant se coupe gratuitement.** Les poids d'attention :
   n'en garder que 32 par requête **améliore** la perplexité de 0,5 à 1,2 %
   (vérifié sur trois jeux). Ce qui est porteur — Q, K, les activations du FFN —
   ne se coupe pas.
3. **Une configuration gagne des deux côtés** : attention à 32 clés + `gate` à
   85 % → **−0,44 % de perplexité et −4,4 % d'événements**.
4. **Le plus gros gain ne venait pas de la parcimonie.** L'attention tournait à
   1,9 GFLOP/s sur un cœur parce que ses boucles n'étaient pas vectorisées :
   réécrites, elle a été **divisée par deux** à perplexité identique. Quatre
   micro-optimisations de la boucle d'événements ont été testées et **rejetées
   par la mesure** (décodage par paquets, accumulateurs i32, contrôles de
   bornes, renormalisation).

➡️ **Règle de méthode à ajouter** : avant d'imposer une approximation pour
gagner du temps, vérifier que le code de base est écrit correctement. Sur cette
campagne, une réécriture de boucle a rapporté plus que toutes les techniques
neuromorphiques importées.

## 3. Ce que la mesure interdit d'espérer

Trois résultats de ce projet ferment des portes. Les ignorer serait la faute
principale possible dans ce programme.

1. **Les motifs récurrents expliquent moins de 1 % de la difficulté.** Les grappes
   d'activation difficiles se reproduisent (r = 0,57 d'une moitié à l'autre) mais
   leur pouvoir prédictif hors échantillon est de R² = +0,007, et une lecture
   linéaire de la perte depuis les activations donne R² < 0. **La difficulté est
   à 99 % propre au token.** Un programme qui parierait sur la découverte de
   « motifs d'expertise » pour améliorer la qualité se tromperait.
2. **Un nœud linéaire ne peut rien ajouter à 69,2 % des poids.** Sur les
   projections saturées (`ffn_gate`, `ffn_up`, `attn_q`, `attn_output`), le rang
   des lignes égale la dimension d'entrée : 100,00 % des directions de la trace
   hebbienne, y compris son résidu non linéaire, sont déjà dans l'espace des
   poids. Zéro dimension disponible.
3. **Le FPGA ne bat pas le GPU, et de loin.** Mêmes listes lues, mémoire 39×
   plus lente. Sa seule justification est l'énergie par événement (7× le CPU) et
   l'absence de multiplieur — c'est-à-dire les scénarios sans GPU.

## 4. Feuille de route

Chaque étape a une **porte** : un chiffre, mesuré sur cette machine, qui décide
de continuer ou d'abandonner.

### Étape A — Boucle d'apprentissage sans rétropropagation (mois 0-3)

*Pourquoi c'est possible maintenant :* la pile sait mesurer (perplexité, 100/h) et
sait ajuster une lecture (moindres carrés, OpenBLAS à 759 GFLOP/s). Il manque la
plomberie de chargement d'un modèle patché.

- Charger un modèle augmenté de nœuds, sans réentraînement (`--patch`).
- Boucle : journaliser → proposer → ajuster la lecture → évaluer → sélectionner.
- Candidats autorisés par la mesure : **projections ouvertes** (`attn_k`, `attn_v`,
  `ffn_down`), **caractéristiques quadratiques** (401 856 monômes hors du span
  linéaire), **réorganisation contiguë** des listes (localité : +30 % de débit
  déjà mesuré à qualité constante).

> **Porte A** : une variante qui bat le modèle de base de ≥1 % de perplexité sur
> texte retenu, l'ajustement tenant en <1 h sur les threads libres. **Ou** une
> variante 1,3× plus rapide à perplexité égale par réorganisation des listes.

### Étape B — Architecture évolutive (mois 3-12)

Population de variantes concurrentes, évaluées en continu sur les ressources
libres ; opérateurs structurels : ajouter des nœuds, ajouter des experts,
récurer un bloc, lier des poids.

> **Porte B** : une variante **2× moins chère par token à perplexité égale**, ou
> **10 % de perplexité en moins à coût égal**. Les deux se mesurent avec
> l'instrumentation existante.

### Étape C — Spécialisation et mémoire (an 1-2)

- **Experts** : un expert qui ne tire pas coûte zéro — c'est notre avantage
  structurel le plus net sur les piles denses.
- **Mémoire externe** : le journal hebbien comme mémoire associative (kNN sur les
  activations passées), pour apprendre un fait à l'inférence.
- **Récursion** : profondeur sans paramètres, financée par la marge mémoire.

> **Porte C** : apprendre un fait nouveau à l'inférence et le retenir sur 10 000
> tokens **sans oubli catastrophique** — mesuré par la perplexité sur le fait
> contre un contrôle apparié.

### Étape D — Boucle autonome (an 2-5)

Fermer la boucle : percevoir → agir → journaliser → proposer → évaluer → adopter,
sans humain dans la boucle d'amélioration.

> **Porte D** : une courbe de capacité **monotone et mesurée** sur un banc
> retenu, produite par le système lui-même sur ≥100 cycles consécutifs.

## 5. Risques, et ce qui tuerait le programme

| Risque | Signal d'alarme | État actuel |
|---|---|---|
| Les motifs sont du bruit | R² hors échantillon ≈ 0 | **déjà observé** (0,007) |
| L'espace de caractéristiques est saturé | 100 % des directions dans le span | **déjà observé** (69 % des poids) |
| Le coût d'évaluation explose | moins de 10 évaluations/h | non observé (98/h) |
| L'absence de rétropropagation plafonne | pas de gain après 10⁴ candidats | à mesurer |
| La trace devient ingérable | >1 Go/session | non observé (10 Mo) |

**Critère d'arrêt honnête** : si l'étape A ne franchit pas sa porte après 10⁴
candidats évalués, la thèse « on apprend sans gradient sur ce substrat » est
falsifiée, et le programme doit se replier sur l'objectif de performance
(localité, experts, récursion) sans prétendre à la plasticité.

## 6. Méthode

1. **Tout mesurer sur la machine**, jamais estimer sans le dire. Et mesurer en
   **entrelaçant** les configurations comparées : la machine porte une charge de
   fond (bureau, autres projets) qui fait varier le temps mur de 30 %. Les
   mesures déterministes — perplexité, comptes d'événements — sont insensibles à
   cette charge et doivent être préférées.
2. **Consigner les erreurs** : le journal de session est archivé
   automatiquement (`tools/archive_sessions.py`, hook git + tâche horaire), et
   chaque rectification est datée dans les rapports.
3. **Séparer mesure, déduction et projection**, explicitement étiquetées.
4. **Une porte non franchie arrête la branche** — pas de poursuite par inertie.

## 7. Les trois prochaines actions

1. **Plomberie d'apprentissage** : charger un modèle patché, mesurer la
   perplexité avant/après (`--patch`). C'est ce qui rend l'étape A exécutable.
2. **Premier candidat non linéaire** : un nœud quadratique sur une projection
   ouverte, ajusté par moindres carrés sur le journal. C'est le seul candidat que
   la mesure n'a pas déjà exclu.
3. **Réorganisation contiguë** : grouper les neurones co-actifs dans les listes.
   Gain attendu +30 % de débit, mesuré à qualité constante — la porte la plus
   proche du programme.

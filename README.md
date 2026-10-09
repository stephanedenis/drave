# Drave

*Anciennement `Qtrinet`.* **La drave**, c'est le flux qu'on conduit : ici, celui
des **listes d'activation** (*stream of logs*) — le moteur ne lit pas des
matrices, il pousse des faits valués vers leurs destinations. La vision complète
est dans [`docs/vision.md`](docs/vision.md).

Origine du projet : inférence de LLM en **ternaire / multi-bits** sur un cluster
de cartes **Stratix V** (Microsoft Storey Peak) — 100 % logique, sans DSP.
Le cahier des charges d'origine est dans [`Qtrinet-bootstrap.md`](Qtrinet-bootstrap.md)
⚠️ **il a été audité et corrigé** : voir la section « Écarts avec le CDC » ci-dessous.
Le renommage est FAIT : le crate et le binaire s'appellent `drave-core` et
`drave`, les variables `DRAVE_*` (table de conversion dans `docs/histoire.md`) ;
le journal de sessions, archivé, n'est pas réécrit.

---

## La campagne du 8-9 octobre — 24 h de mesures, par famille de tâches

Ce que l'architecture événementielle vaut, **tâche par tâche**, avec pour chaque
chiffre ses conditions (corpus, tokenizer, charge) :
[`reports/rapport-campagne-benefices.md`](reports/rapport-campagne-benefices.md)
(verdict famille par famille au § 0 bis). La file de mesures est
[`tools/campagne-benefices.sh`](tools/campagne-benefices.sh), ses journaux bruts
sont dans `/tmp/campagne24/`, et **les 23 portes du dépôt sont vertes**.

**Cinq résultats, chacun avec sa mesure :**

| résultat | mesure |
|---|---|
| **Le chemin par listes n'approxime RIEN** | logits **identiques au bit près** contre le chemin dense, à encodage de poids égal (`cmp` sur 4 254 216 octets) |
| **La parcimonie doit être APPRISE** | à 25 % gardés : témoin **10,8758** de perplexité, modèle entraîné creux **5,1719** (−52 %) |
| **La courbe lecture ↔ qualité** | **÷4 pour +1 %** (structure innée aléatoire) · **÷8 pour +4 %** (deux axes appris) · ÷15 pour +22 % si un axe est imposé |
| **Le routage seul s'inverse à dim 512 ; la distillation le rattrape** | routé +10 % à 512, routé **distillé 4,3305 contre 4,5686** au dense (à 12,8 M paires/jeton des deux côtés) |
| **La mémoire tient, et les gros modèles tournent** | **18 aiguilles sur 18** jusqu'à **12 288 jetons** · V4-Flash **365,7 Go sur 125 Go de RAM, 37,6 Go résidents** · gpt-oss rend **15,6017**, la valeur attendue au chiffre près |

**Quatre documents de conception** en sortent, et ils disent aussi ce qui manque :

- [`docs/modele-pour-drave.md`](docs/modele-pour-drave.md) — **moteur contre
  modèle** : ce que l'architecture récompense, dix dessins évalués, dont trois
  inédits (profondeur routée, budget d'événements appris, quantification adaptée aux
  listes) ; et la réponse GPU : **nos modèles à décharges ne sont pas déportables**
  (projections trop petites, noyau GPU dense).
- [`docs/biologie-pour-drave.md`](docs/biologie-pour-drave.md) — ce que les
  connectomes imposent : structure innée (~gratuite à 25 %, chère à 12,5 %), poids
  synaptiques log-normaux (les nôtres sont gaussiens), et **six ordres de grandeur**
  entre l'énergie par événement du cerveau et la nôtre.
- [`docs/hebbien-differentiel-et-biologie.md`](docs/hebbien-differentiel-et-biologie.md)
  — notre règle locale est **réfutée**, et la biologie dit pourquoi : pas de crédit,
  pas de décorrélation, structures saturées.
- [`docs/architecture-cerveau-et-drave.md`](docs/architecture-cerveau-et-drave.md) +
  [`docs/plan-cerveau-complet.md`](docs/plan-cerveau-complet.md) — les **douze
  capacités manquantes** pour porter une architecture de cerveau (graphe de régions,
  délais, horloges, bus de modulation, mémoire épisodique, consolidation,
  périphérie, latéralité, budgets, instances concertées, traçage distribué), en six
  phases à portes mesurées, avec la distribution multi-instances développable **sur
  cette seule machine**.

**Deux manques restent des manques**, et sont écrits comme tels : les
**encodeurs/embeddings** (`bge-m3` inexécutable : ni attention bidirectionnelle ni
pooling) et le **noyau Q8 par expert** (sans lui, un modèle routé ne peut pas être
exécuté en listes).

---

## La journée du 30/09 — huit chantiers, mesurés

Le détail est dans [`reports/rapport-session-2026-09-30.md`](reports/rapport-session-2026-09-30.md).

| chantier | résultat |
|---|---|
| **calcul réparti fidèle** | écart local/réparti **0,00e0** à 40, 200 et 1 024 jetons |
| **préremplissage par lots** (mode 3) | 256 jetons en 4 lots, **0,00e0** ; **18×** plus rapide qu'un flux par jeton sur un lien à 20 ms |
| **lot en listes** (mode 4) | **1,5 ko par jeton** au lieu de 3,5 (÷2,3), écart 3,03e-2 |
| **transport en listes** | 3 663 → 1 608 octets par flux pour 2,7e-2 d'écart |
| **cache KV : où mettre les bits** | clés f16 + valeurs int8 = **+0,018 %** pour **39 %** de la taille du f32 → [`reports/rapport-placement-bits-kv.md`](reports/rapport-placement-bits-kv.md) |
| **format de trace v2 / v3** | 132 396 736 → **66 370 408** (sans perte) → **45 079 930** octets (+0,074 % de perplexité) |
| **protocole de flux v5** | version, cinq modes, contrat d'activation complet, refus immédiat d'un pair incompatible |
| **Colab prêt** | [`colab/`](colab/README.md) : notebook, bundle de 4,5 Mo, trois voies de tunnel, vérifié de bout en bout |

Deux relectures adversariales déléguées ont trouvé **22 défauts** — dont 17 par
lecture et non par un banc, y compris dans les correctifs de la première.

## État du projet

| Étape | État |
|-------|------|
| Audit du cahier des charges | ✅ (corrections ci-dessous) |
| **Test de principe : quantification d'un modèle minimal** | ✅ **fait** → [`reports/rapport-minimal.md`](reports/rapport-minimal.md) |
| **Élagage et approche par événement** | ✅ **fait** → [`reports/rapport-eparsite.md`](reports/rapport-eparsite.md) |
| **Sparsité → précision** | ✅ **fait** → [`reports/rapport-precision.md`](reports/rapport-precision.md) |
| **Encodage de structure (listes signées)** | ✅ **fait** → [`reports/rapport-encodage.md`](reports/rapport-encodage.md) |
| **Architecture push (AER) + faisabilité CPU** | ✅ **fait** → [`reports/rapport-cpu-aer.md`](reports/rapport-cpu-aer.md) |
| **Moteur d'événements Rust (4 optimisations)** | ✅ **fait** → [`reports/rapport-optimisations.md`](reports/rapport-optimisations.md) |
| **Inférence complète en Rust, sans GPU** | ✅ **fait** → [`reports/rapport-inference.md`](reports/rapport-inference.md) |
| **PE événementiel vérifié et synthétisé (Stratix V)** | ✅ **fait** → [`../FPGA-Stratix-V/docs/rapport-pe-evenementiel.md`](../FPGA-Stratix-V/docs/rapport-pe-evenementiel.md) |
| **Lecteur DDR3 vérifié de bout en bout** | ✅ **fait** → [`../FPGA-Stratix-V/docs/rapport-lecteur-ddr3.md`](../FPGA-Stratix-V/docs/rapport-lecteur-ddr3.md) |
| **Bilan multi-matériel (CPU / FPGA / GPU)** | ✅ → [`reports/bilan-multi-materiel.md`](reports/bilan-multi-materiel.md) |
| **Capteur hebbien (apprendre des logs d'activation)** | ✅ mesuré → [`reports/rapport-capteur-hebbien.md`](reports/rapport-capteur-hebbien.md) |
| **Programme évolutif (journaliser, faire évoluer)** | ✅ évalué → [`reports/rapport-programme-evolutif.md`](reports/rapport-programme-evolutif.md) |
| **Croisement push/pull à ~22 % de densité** | ✅ mesuré → [`reports/rapport-croisement-push-pull.md`](reports/rapport-croisement-push-pull.md) |
| **Greffon : plomberie d'apprentissage** | ✅ validé → [`reports/rapport-greffon.md`](reports/rapport-greffon.md) |
| **Journal de sessions automatisé** | ✅ `tools/archive_sessions.py` (hook git + cron) |
| **Comparaison Spiking (SpikeGPT / Spikformer / Spikingformer)** | ✅ → [`docs/comparaison-spiking.md`](docs/comparaison-spiking.md) |
| **Parcimonie imposée à l'inférence (k-WTA)** | ✅ mesuré → [`reports/rapport-parcimonie-imposee.md`](reports/rapport-parcimonie-imposee.md) |
| **Attention creuse (top-k par requête)** | ✅ mesuré → [`reports/rapport-attention-creuse.md`](reports/rapport-attention-creuse.md) |
| **Campagne parcimonie : synthèse** | ✅ → [`reports/rapport-campagne-parcimonie.md`](reports/rapport-campagne-parcimonie.md) |
| **Attention vectorisée (÷2 sur le temps)** | ✅ à perplexité identique |
| Modèle ternaire *entraîné* (BitNet b1.58) | ⬜ à faire |
| Extracteur GGUF → plans ternaires | ⬜ à faire |
| Format binaire + schéma partagé Python/RTL | ⬜ à faire |
| RTL : PE ternaire + décodeur | ⬜ à faire |

Le matériel est prêt de son côté : voir le dépôt
[`FPGA-Stratix-V`](../FPGA-Stratix-V) — carte détectée (Gen3 ×8), JTAG validé
(`0x029070dd`), Quartus Prime Standard 21.1 opérationnel, bitstream produit.

---

## Test de principe (`run_quantify.py`)

Un MLP minimal (32→64→10) est **entraîné** en numpy (aucune dépendance ML), puis
quantifié selon plusieurs formats. Trois questions, chiffres en main :

**1. Le chemin entier est-il exact ?** Oui — écart avec le calcul flottant :
**4,2e-07** (couche 1) et **1,9e-06** (couche 2), soit de l'arrondi flottant pur.
Le principe « que des additions/soustractions, aucun DSP » est validé. Le biais
s'ajoute à la remise à l'échelle, hors du réseau de MAC.

**2. Le ternaire préserve-t-il le modèle ?**

| Format | b/poids | Accuracy |
|--------|---------|----------|
| float32 | 32 | 76,07 % |
| int8 | 8 | 76,27 % |
| int4 | 4 | 74,12 % |
| **ternaire 1,58 b (dense 2 b)** | **2** | **49,71 %** |
| multi 2 plans | 4 | 73,44 % |
| multi 3 plans | 6 | 74,12 % |
| multi 4 plans | 8 | 75,98 % |

➡️ La quantification ternaire **a posteriori** détruit la fonction (−26 pt). Ce n'est
pas un verdict contre BitNet : les modèles b1.58 sont **entraînés** avec la contrainte.
Le découpage en plans (multi-bits) dégrade au contraire très progressivement.

**3. Combien coûte chaque encodage ?**

| Encodage | Ternaire | 4 plans |
|----------|----------|---------|
| dense (1 bit/plan) | **2,0 b/poids** | **4,0 b/poids** |
| bitmap + signe | — | 8,0 b/poids |
| **CSR par plan (le CDC)** | **10,1 b/poids** | **61,8 b/poids** |

➡️ Le CSR coûte **5 à 15× le dense** en trafic mémoire. Sur un système borné par la
DDR3, cela divise directement le débit.

**4. Débit projeté** (débits **mesurés** : DDR3 9,66 Go/s, fmax 124 MHz) :

| Modèle | Encodage | tok/s par carte |
|--------|----------|-----------------|
| 7B | ternaire dense 2 b | **5,5** |
| 7B | 4 bits | 2,8 |
| 7B | ternaire CSR | 0,6 |

➡️ **312 voies de MAC suffisent** (≈ 9 400 ALM, 5 % du FPGA) pour saturer la DDR3.
Le projet est un projet **système mémoire**, pas un projet de PE.

---

## Élagage et approche par événement (`run_sparsity.py`)

**Question** : un modèle quantifié peut-il être élagué assez pour qu'une exécution
« par événement » (ne traiter que les non-nuls) soit rentable ?

**Le point clé** : un poids ternaire non nul ne porte **qu'un signe**. Le meilleur
encodage événementiel est donc *bitmap + signe* = **1 + d bits/poids** (d = densité),
à comparer aux 2 bits du code dense. Il n'est **jamais pire**, et jusqu'à 2× meilleur.

| Encodage | Coût (b/poids) | À d = 50 % | À d = 25 % |
|---|---|---|---|
| dense 2 bits | 2,00 | 2,00 | 2,00 |
| **bitmap + signe** | **1 + d** | **1,50** | **1,25** |
| CSR bloc 16 b | 17·d | 8,50 | 4,25 |
| CSR plat 32 b | 33·d | 16,50 | 8,25 |

**Densités de rentabilité** (mesurées par le modèle de coût) :

| Comparaison | Égalité à | Gagnant en dessous |
|---|---|---|
| bitmap vs dense | 100 % | **bitmap (toujours)** |
| CSR 16 b vs dense | **11,8 %** | CSR |
| CSR 32 b vs dense | **6,1 %** | CSR |
| CSR 32 b vs bitmap | 3,1 % | CSR |

➡️ **Le CSR n'est rentable que sous ~6 % de densité** — un régime qu'un LLM
généraliste n'atteint pas (SparseGPT/Wanda : 50-60 % en *one-shot* ; le 2:4 structuré
= 50 % est la forme supportée par le matériel).

**Mesuré sur notre modèle** : densité naturelle du ternaire **26,3 %**, activations
non nulles après ReLU **52,8 %**, donc **13,9 % d'événements réels**. Le bitmap y
donne **×1,58** de débit : un 7B passe de **5,5 à 8,7 tok/s** par carte.

**Le vrai coût est ailleurs** : un événement n'existe que si le poids *et* l'activation
sont non nuls, et récupérer l'activation à un index arbitraire impose une fenêtre de
lecture + un multiplexeur par voie (~21 LUT pour un 64:1, soit ≈ 3 400 ALM pour
312 voies = **2 % du FPGA**). C'est payable.

**Recommandation** : garder le dense 2 bits comme chemin nominal (simple, déterministe,
déjà validé) et ajouter un encodage bitmap + signe là où la densité est faible. Le saut
de blocs entièrement nuls (1 bit par bloc de 64 = 1,6 % de surcoût) est le premier pas.

> ⚠️ La courbe précision ↔ élagage obtenue est **bruitée** (modèle de 2 688 poids) : elle
> ne permet pas de conclure sur la dégradation réelle due à l'élagage. Les densités
> atteignables sur un LLM sont à revérifier sur un vrai modèle.

---

## Encodage de structure : éliminer complètement la valeur (`run_encoding.py`)

**Idée** : avec des poids ±1, la valeur n'a plus besoin d'être stockée. On remplace la
matrice par **deux listes triées de destinations** par source (les « + » et les « − ») :
l'appartenance à la liste porte le signe. Il ne reste que des **positions** — la matrice
devient un **graphe biparti signé**. C'est le « adressage relationnel » du CDC, poussé
jusqu'au bout.

Ce qui rend l'idée payante : les listes étant triées, on encode des **écarts** (deltas),
comme les formats de graphes compressés (WebGraph/LLP).

**Coût exact mesuré, lignes de 4 096 poids :**

| Densité | bitmap + signe | **listes signées** | gain | tok/s 7B | vs dense 2 b |
|---|---|---|---|---|---|
| 50 % | 1,500 | 1,838 | 0,82× | 6,0 | ×1,09 |
| 25 % | 1,250 | 1,306 | 0,96× | 8,5 | ×1,53 |
| **12,5 %** | 1,125 | **0,871** | **×1,29** | 12,7 | **×2,30** |
| **5 %** | 1,050 | **0,476** | **×2,21** | **23,2** | **×4,20** |
| 2 % | 1,020 | 0,251 | ×4,06 | 44,0 | ×7,96 |
| 1 % | 1,010 | 0,151 | ×6,71 | 73,3 | ×13,28 |

➡️ **Bascule vers 20 % de densité.** Au-dessus, le bitmap + signe gagne ; en dessous, les
listes signées gagnent et l'écart se creuse très vite.

**Croisement avec la précision mesurée** (`run_precision.py`) : à 5 % de densité, le
ternaire élagué+réentraîné atteint **59,1 %** d'accuracy (contre **49,7 %** pour le
ternaire dense non élagué) pour **0,476 b/poids au lieu de 2,0** — soit **à la fois plus
précis et ×4,2 plus rapide**.

**Marge restante** : à 5 %, l'entropie des positions vaut 0,288 b/poids contre 0,476 pour
les listes — un facteur 1,65 encore disponible dans un codage plus fin.

**Le coût se déplace** vers la collecte d'activation (chaque événement vise un indice
arbitraire → croisement ou réplication de bancs M20K). Le décodeur, lui, reste LUT-only :
un accumulateur d'écarts + une FIFO, aucun DSP.

> ⚠️ Les coûts d'encodage sont mesurés exactement ; les *densités atteignables* viennent
> du MLP jouet. Sur un LLM réel, 5-12 % de densité exige un réentraînement lourd — c'est
> la question ouverte.

---

## Architecture « push » (AER) et exécution CPU (`run_cpu.py`, `bench/cpu_aer.c`)

**Le problème** : dans l'architecture « tirer » (gather), chaque poids non nul doit aller
chercher son activation à un indice arbitraire — accès irrégulier, coûteux.

**La solution** : **pousser**. Chaque source dont l'activation est non nulle émet un
événement ; sa liste de destinations se lit **séquentiellement** ; on disperse
`acc[dest] += signe · x[src]`. C'est l'**AER** (Address Event Representation) du
neuromorphique. L'accès aléatoire se déplace de l'entrée (activation, large) vers la
sortie (accumulateur 4096 × 24 bits = **12 Kio**, tient dans les M20K). Les poids se
lisent en flux : plus aucun gather.

**Mesures C/OpenMP sur ce bi-Xeon (`bench/cpu_aer.c`, 16 threads) :**

| Test | 1 th | 8 th | 16 th | 32 th |
|---|---|---|---|---|
| Lecture séquentielle | 4,1 Go/s | 23,4 | **28,7** | 28,2 |
| Dispersion pure | 0,96 G év/s | 3,46 | 3,20 | 3,22 |
| **Écarts + dispersion** | 0,87 | 4,55 | **7,79** | 6,79 |

➡️ La dispersion sature vers 8 threads (accès aléatoire à l'accumulateur). **Le décodage
par écarts est quasi gratuit** : le noyau complet est *plus rapide* que la dispersion pure.

**Projection 7B (densité 5 %, 0,476 b/poids, 416 Mo et 350 M événements par token) :**

| Cible | ms/token | tok/s |
|---|---|---|
| CPU borné bande passante | 14,5 | 68,9 |
| CPU borné noyau | 44,9 | 22,3 |
| **CPU réaliste** | **44,9** | **22,3** |
| 1 carte FPGA | 43,1 | 23,2 |
| **4 cartes FPGA** (modèle réparti) | **10,8** | **92,8** |

➡️ **Une carte FPGA ≈ ce CPU** (23 contre 22 tok/s) : le CPU a 3× la bande passante mais
est limité par sa cadence d'événements ; la carte est limitée par sa DDR3. L'avantage du
FPGA est le **passage à l'échelle** (4 mémoires et 4 jeux de voies indépendants), pas la
carte seule — c'est exactement l'argument du ring.

**Conséquence pratique** : écrire d'abord l'implémentation **CPU**. Elle est immédiate
(aucun bitstream, aucun DMA, aucun JTAG), elle valide le format et la sémantique des
événements, et elle fournit le **modèle d'or** que le RTL devra reproduire.

> ⚠️ Projection sur la partie GEMM seule : attention, KV cache, non-linéarités et
> échantillonnage ne sont pas comptés. À confronter à une vraie implémentation.

---

## Tri et dédoublonnage des contributions (`bench/cpu_merge.c`)

**Intuition** : trier et dédoublonner les contributions avant de les appliquer — une
seule écriture par destination au lieu d'une par événement.

**Mesure (50 M événements, 4 096 destinations, 16 threads) :**

| Variante | Cadence | Écritures |
|---|---|---|
| (a) Dispersion (1 écriture/événement) | 3,36 G év/s | 50 000 000 |
| **(b) Trié + replié** | **3,89 G év/s** (+16 %) | **4 111** |
| (c) Coût du tri (radix 2 passes) | 0,06 G év/s = **838 ms** | — |
| rappel : ordre naturel (écarts décodés) | **7,79 G év/s** | — |

➡️ **Le tri divise les écritures par 12 000 mais ne gagne que 16 %** : les écritures
n'étaient pas le goulot. Et il coûte 838 ms là où l'accumulation en coûte 15 — environ
**50× plus cher que ce qu'il rapporte**.

**Ce qu'il faut faire à la place :**

1. **Exploiter l'ordre naturel** (par source, listes de deltas) : 7,79 G év/s, le meilleur
   résultat mesuré. Pas de tri.
2. **Multi-plans : décaler l'activation**, pas fusionner les listes. La contribution du
   plan *b* vaut `x[src] << b` : l'accumulation les somme naturellement, sans aucun
   dédoublonnage. Un seul accumulateur suffit.
3. **Le dédoublonnage ne se justifie que pour la sémantique** : fusion de sommes
   partielles venant de plusieurs cartes (ring), ou déterminisme du résultat. Dans ce cas,
   utiliser un **réseau de combinaison à compartiments par destination** (ce que font les
   routeurs AER), jamais un tri global.

> ⚠️ Le tri mesuré est un radix naïf mono-thread ; un tri parallèle irait ~10× plus vite,
> mais resterait 5× plus cher que l'accumulation qu'il optimise.

---

## Moteur d'événements Rust (`drave-core`)

Le moteur d'exécution par listes est maintenant écrit en Rust — **std seul, zéro
dépendance** (crates.io est inaccessible depuis cette machine, et c'est très bien :
le moteur tenait en 386 lignes à ses débuts ; il en fait 15 300 aujourd'hui). Détail complet :
[`reports/rapport-optimisations.md`](reports/rapport-optimisations.md).

```bash
cd drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --threads 16
```

**Les 4 optimisations :**

1. **Réduction incrémentale** — chaque worker ne remet à zéro que les destinations
   qu'il a touchées. Coût d'un appel à vide : 0,484 ms → **0,011 ms** (×44).
2. **Décodage SWAR** — 8 écarts d'un octet décodés d'un coup dans un mot de 64 bits
   (un seul test `w & 0x8080…`), sans branche par élément.
3. **Vecteur creux explicite** (`SparseVec`) — indices triés + valeurs contiguës,
   plus de test de zéro ni d'indirection dans la boucle chaude.
4. **Listes fusionnées** (`FusedSign`) — une seule liste triée + plan de signe, au
   lieu de deux listes (+, −) : l'accès à l'accumulateur devient monotone.

**Résultats** (30 threads, `blk.0.ffn_gate.weight` 4864×896, 4 303 745 événements) :

| Densité | Événements | Fusion | 2 listes |
|---|---|---|---|
| 0 % | 0 | 0,011 ms | 0,011 ms |
| 10 % | 430 359 | 1,81 G év/s | 2,30 G év/s |
| 25 % | 1 076 785 | 3,18 G év/s | 3,86 G év/s |
| 100 % | 4 303 745 | 4,51 G év/s | 5,44 G év/s |

Les deux décodeurs donnent le résultat **exact** du produit matrice-vecteur dense
de référence : **14 vérifications sur 14** (7 densités × 2 décodeurs). Le débit
varie de **0,011 ms à 0,95 ms sur la même matrice** (rapport 86) : « on ne paie que
ce qui s'active » est vérifié à l'échelle du moteur.

**Montée en charge** (densité 100 %, meilleur de 3 passes) : 1 thread 0,41 G év/s →
8 threads 2,75 → 16 threads 4,45 → **32 threads 4,84** → 39 threads **2,04** ❌.
L'attente active ne tolère aucune sursouscription : le pool est borné à `CPU − 1`
et vaut `3/4 × CPU` par défaut.

**Sans multiplieur** : décalages + additions donnent le résultat exact en 112,3 ms
contre 2,5 ms pour i8×i8 (×44,9 sur CPU) — mais **sur FPGA le multiplieur n'existe
pas**, et la contrainte du CDC est satisfaite sans réentraînement ni élagage.

> ⚠️ Trois pièges ont coûté une campagne de mesures fausses chacun : un état
> partagé avec **deux contrats de nettoyage** (d'où une « divergence » fantôme et
> un débit surestimé à 7,53 G év/s), un `&mut` dans la boucle chaude (barrière
> d'aliasing : 3,09 → 0,97 G év/s), et la **sursouscription** de l'attente active
> (39+1 threads sur 40 CPU : effondrement ×2,4 — et le `yield_now()` censé le
> corriger a tout empiré). Détail dans le rapport.

---

## Formats et modèles réellement lisibles

Le moteur lit **Q4_K, Q6_K, Q4_0, Q5_0, Q5_1, Q8_0, Q2_K, Q3_K, Q5_K, MXFP4,
IQ1_S, IQ1_M, IQ2_XXS, IQ3_XXS, IQ4_XS, BF16, F16 et F32** — soit tout ce que
l'écosystème public distribue — **sans copie ni requantification** : les blocs
sont lus tels quels dans le fichier, et les experts d'un MoE sont des tranches
contiguës adressées par un pointeur et un pas. Les formats de super-bloc sans
noyau dédié (Q2_K, Q3_K, Q5_K, IQ*) sont lus par **déquantification puis produit
en f32** : plus lent qu'un noyau, juste par construction.

Chaque déquantificateur est comparé à **libggml** bloc par bloc, et les grilles
IQ embarquées sont extraites de `ggml-common.h` par programme :

```bash
tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggml
tools/extraire_tables_ggml.sh verifier    # les tables embarquées = celles de ggml
```

**19 formats lisibles, 17 vérifiés à la porte** : `Q4_1` et `Q5_1` sont lus par
les mêmes branches que leurs voisins `Q4_0`/`Q5_0` (`drave-core/src/gguf.rs`)
mais ne sont pas dans la batterie comparée bloc par bloc.

| modèle | format | perplexité | débit | mémoire |
|---|---|---|---|---|
| Qwen2.5-0.5B | Q4_0 | 21,01 | 39 tok/s | 0,41 Go |
| Qwen2.5-1.5B | Q4_K_M | 12,92 | 17 tok/s | 1,1 Go |
| Qwen2.5-VL-7B | Q4_K_M | 10,99 | 2,8 tok/s | 4,5 Go |
| **Qwen3-30B-A3B** (MoE 128 experts, top-8) | Q4_K_M | **7,61** | 5,4 tok/s | **17,7 Go** |
| **gpt-oss-120b** (MoE, MXFP4) | MXFP4 | **15,6017** (ctx 256) | blocs lus | 60 Go |
| **GLM-5.3** (79 couches MLA, 256 experts) | IQ1_S/IQ3_XXS/IQ4_XS | pos. 0 : corrélation **0,999024** · au-delà, l'écart croît (4 nats à la pos. 3) | 190 s/jeton | 90 Go |
| **Kimi-K2.7** (61 couches MLA, 384 experts) | IQ1_M/IQ2_XXS/IQ3_XXS | non validé | 73 s/jeton | 1 026 G mmap |

Les deux derniers sont les plus gros modèles que le moteur ait calculés. Leur
attention MLA à rang faible (cache latent) est **validée à la position 0**
(corrélation des logits 0,999024, top-1 3/3 sur les trois premiers jetons) mais
**pas au-delà** : sur 7 jetons, l'écart à llama.cpp passe de 0,33 à 4,07 nats et
la perplexité de 890,4559 à 4 807,76. Une erreur qui grandit avec la position
vient de l'état (cache, scores) et non des poids : c'est le chantier en cours,
et c'est écrit ici pour que personne ne s'appuie sur ces chiffres au-delà de
deux jetons.

Les lecteurs Q4_K et Q6_K sont vérifiés **tenseur par tenseur** contre une
référence F16 des mêmes poids produite par `llama-quantize`, et le routage MoE
sur `Qwen3-30B-A3B`. Détail : [`docs/convertisseur.md`](docs/convertisseur.md)
et [`reports/rapport-passage-a-l-echelle.md`](reports/rapport-passage-a-l-echelle.md).

### Les modèles éclatés se lisent comme un seul

Un modèle en **shards** (`…-00002-of-00003.gguf`) s'ouvre par n'importe lequel de
ses morceaux, et un dossier au **format clusters** (`commun.gguf` + `cluster-XX.gguf`
+ `mapping.tsv`) **est** un modèle : `drave <dossier> …`, sans option nouvelle.
Les tenseurs de chaque cluster sont exposés sous leur préfixe (`cl0/…`) et
`Moe::ou(expert_global)` rend `(fichier, ligne locale)` — un expert absent du nœud
est simplement sauté.

| mesure | résultat |
|---|---|
| DeepSeek-V4-Flash, 3 shards, en-têtes seuls | 86,90 Go annoncés = **86,90 Go sur disque** · 1 328 tenseurs · 54 ms |
| Qwen3-30B-A3B en clusters | 9 fichiers · **1 587 tenseurs · 18,55 Go** = l'original |
| **origine contre clusters** (mêmes 63 jetons) | **15,2789 = 15,2789** |
| chemin par lots sur le même modèle | 15,2736 (`--lot 64`) |

Un lecteur d'inventaire (`--tensors`) travaille sur les **seuls en-têtes** : il
faut cela pour inspecter un fichier de 366 Go. Détail :
[`docs/format-clusters.md`](docs/format-clusters.md) et
[`reports/rapport-lecteur-multifichiers.md`](reports/rapport-lecteur-multifichiers.md).

## Inférence complète en Rust (`--infer`)

Qwen2.5-0.5B-Instruct Q8_0 tourne **en mode listes d'événements**, sans GPU, sans
BLAS, sans aucune dépendance : **15 300 lignes de Rust, `std` seul** au 01/10 à midi (2 319 au premier prototype). Détail :
[`reports/rapport-inference.md`](reports/rapport-inference.md).

```bash
cd drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --chat --prompt "Explain in one sentence why the sky is blue."
```

> `<|im_start|>assistant`
> The sky is blue because it reflects sunlight, which contains colors such as
> red, orange, yellow, green, blue, and indigo, which are all visible in the
> spectrum.

Le moteur sait exécuter le même modèle de **trois façons**, et c'est un résultat
en soi : elles donnent des sorties **bit à bit identiques** (PPL 19,2647 au chiffre
près sur 510 jetons, mêmes tokens). Le mode est une décision de performance, pas de
sémantique.

| mode | quand | débit (510 jetons) |
|---|---|---|
| **auto** — *le défaut* | toujours : charge les deux formes et bascule projection par projection sur la densité mesurée | **le meilleur des deux** |
| **pull** (`--dense`) | densité d'activation > 22 % — le cas d'un LLM dense | 29,5 tok/s |
| **push** (`--push`) | densité < 22 % — réseau creux, k-WTA, ReLU | 13,6 tok/s à 100 %, 20,6 à 5 % |
| **4 bits** (`--q4`, `--q4-tout`) | modèle 4 bits existant (Q4_0) ou débit prioritaire | **41,6 – 44 tok/s** |

Le défaut est `auto` : sur un modèle dense il donne ×2,0 sans rien changer aux
sorties, et sur un réseau creux il bascule tout seul du bon côté.

| | |
|---|---|
| Événements par token | 352,8 M à **5,3 G év/s** en push |
| Mémoire | 1,27 Go (0,71 Go de listes), chargement 6,3 s |
| Justesse | **16 tokens sur 16 identiques** à la référence numpy float32 |
| Perplexité WikiText-2 | **24,90** sur 2 040 jetons contre **25,00** pour numpy + OpenBLAS |
| Croisement push/pull | **~22 %** de densité d'activation, mesuré — pas 10 % (voir [`reports/rapport-croisement-push-pull.md`](reports/rapport-croisement-push-pull.md)) |
| Mur mémoire | 19–22 Go/s mesurés sur cette machine ; le noyau dense lit ses poids à 14 Go/s : **il est au mur**, pas mal écrit |

**Les 4 bits paient — sur les grosses matrices.** Un noyau AVX2 (`vpmaddwd`) à 4,5
bits/poids, alimenté par un **import verbatim** des blocs Q4_0 (aucune
requantification), fait tourner un vrai Qwen2.5-0.5B **Q4_0** à **41,6 tok/s**
contre 28,3 pour le même fichier lu par le noyau int8 — et avec une perplexité
légèrement **meilleure**, parce qu'il ne rajoute pas une seconde couche d'erreur.
Le prix réel des 4 bits est celui du modèle : +9,1 % de perplexité contre Q8_0.
Détail complet : [`reports/rapport-mur-memoire-4bits.md`](reports/rapport-mur-memoire-4bits.md).

**Deux compromis assumés :** la tête de sortie (151 936 sorties) est calculée par
produits scalaires sur les lignes Q8_0 d'origine — en mode push il faudrait un
accumulateur de 36 Mo *par worker* et chaque sortie serait écrite 896 fois ; et les
activations sont quantifiées (int16 par défaut : 16/16 identiques ; int8 : 0,3 % plus
rapide mais les courses serrées basculent).

**Ce que ça ne démontre pas :** le débit variable. 352 M événements par token, à tous
les tokens, parce qu'un LLM dense n'a **jamais** d'activation nulle. Le mode
événementiel ne paiera que sur des activations creuses **par construction**.

**Le gain le moins cher du projet** a été trouvé en cherchant ce plafond : la
**liste des destinations touchées** (pour ne vider que ce qui a été écrit) coûtait
six micro-opérations par événement — soit **45 % du temps des produits
matriciels**. La remplacer par une borne haute cumulative par worker donne
**+35 % de débit** (10,96 → 14,8 tok/s), perplexité et tokens inchangés. Le détail
et les deux bugs que cette suppression a révélés sont dans
[`reports/rapport-inference.md`](reports/rapport-inference.md).

**En mode push, le 4 bits ne paie pas** : chaque événement coûte
`varint(écart) + i8(valeur)` ≈ 2 octets **quelle que soit la précision de la
source** — la vitesse suit le nombre d'événements, pas le nombre de bits. Le 4 bits
est un levier du chemin **dense**, celui dont le débit suit les octets lus.

**Et le coût d'un événement n'est pas constant.** 10× moins d'événements ne donnent
que 2× de vitesse, pour deux raisons mesurées : la **localité** (un élagage *contigu*
est 30 % plus rapide qu'un élagage dispersé à taux égal — c'est l'argument des grappes
efférentes), et la **taille de l'accumulateur** : sur des événements épars, ajouter des
threads *ralentit* (31 ms à 4 threads contre 53 ms à 32, les accumulateurs débordant le
L2). ➡️ Le tuilage de la dimension de sortie n'est pas un détail d'optimisation,
c'est le paramètre qui décide du débit en régime creux.

---

## Écarts avec le CDC d'origine

| Point du CDC | Réalité vérifiée |
|---|---|
| « transceivers 40 Gbps » | Aucun transceiver Stratix V GS ne dépasse 12,5 Gbps : le 40G = 4 × 10,3125 Gbps via QSFP+ |
| « NVLink entre les 2 RTX 5000 » | ✅ **exact** — mesuré à 25,78 Go/s par lien |
| « M20K en lecture combinatoire » | Le M20K est **synchrone** (1-2 cycles) ; l'asynchrone, c'est le MLAB |
| « CSR pour éliminer les zéros » | Coûte 5-15× le dense (cf. §3) et impose des accès aléatoires aux activations |
| « 1,58 bit » | Vrai pour un ternaire **entraîné** ; faux pour un Q4 bit-slicé |
| DMA « VFIO ou XDMA » | Ni l'un ni l'autre : l'IP DMA + driver existent déjà (6,5 Go/s mesurés) |

---

## Structure

```
Qtrinet-bootstrap.md    cahier des charges d'origine (à lire avec les écarts ci-dessus)
src/ternary.py          quantification ternaire/multi-bits, plans, encodages, MAC entier
src/tiny_model.py       MLP minimal + entraînement numpy (aucune dépendance ML)
src/roofline.py         projection matérielle (constantes mesurées de la carte)
run_quantify.py         orchestrateur : entraîne, quantifie, mesure, écrit le rapport
drave-core/           moteur d'événements en Rust (std seul, 0 dépendance)
  src/gguf.rs             lecture GGUF + déquantification Q4_0/Q8_0/F16/F32
  src/list.rs             encodages : deltas signés, bitmap+signe, creux k, fusion, push
  src/engine.rs           pool de threads, décodage SWAR, accumulation creuse
  src/tokenizer.rs        BPE byte-level Qwen2 (pré-tokenizer réécrit à la main)
  src/model.rs            forward Qwen2 complet + cache KV + génération
  src/main.rs             mesures du moteur, inférence, perplexité
reports/                rapports générés
```

## Lancer

```bash
python3 run_quantify.py --epochs 400      # ~10 s, numpy seul
cd drave-core && cargo build --release  # moteur d'événements
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --threads 16
```

Aucune dépendance hors `numpy`. (`torch`/`gguf`/`transformers` seront nécessaires
plus tard, pour les modèles réels — pas pour le test de principe.)

---

## L'empreinte mémoire : ce qu'il faut charger avant d'opérer

Question posée pour DeepSeek-V4.1-Flash (365,7 Go) sur une machine à 125 Go de
RAM. Réponse mesurée : **50 à 80 Go suffisent**, et ce n'est pas en découpant
les experts.

| famille de tenseurs | Go | % | à charger |
|---|---|---|---|
| **engram** (2 couches) | **203,4** | **55,6 %** | **0,4 Go** — mmappé |
| experts (40 couches) | 152,9 | 41,8 % | 21 à 71 Go selon l'objectif |
| attention, embeddings, tête | 10,0 | 2,7 % | 10 Go |

`blk.N.engram_embd.weight` fait 101,4 Go par couche, de forme `[384 006 168, 264]`
en I8 — mais **ce n'est pas un tenseur de poids, c'est une table de hachage de
n-grammes**. Une session de 10 000 jetons n'en touche que **17 276 entrées, soit
4,6 Mo** : un rapport de 1 pour 22 000. Le `mmap` la rend adressable sans jamais
la charger.

Ce qui a été mesuré et **écarté** : découper plus fin que l'expert (le seuil
d'activation détruit le modèle dès 5 % : perplexité ×287) · des grappes par
langue (les experts se recouvrent à 0,75–0,90 entre langues, contre 0,805 pour
deux moitiés d'une même langue) · un dictionnaire token → experts (le routage est
contextuel : Jaccard 0,06) · une allocation du cache par couche (+1,2 % au mieux).

Ce qui a été mesuré et **retenu** : le cache d'experts (25 % de l'empreinte sert
80 % des appels) · la tête restreinte à la langue d'entrée (−30 % de trafic ; le
top-1 y est dans 99,2 % des cas) · l'engram mmappé (−203 Go).

Deux structures trouvées en chemin : **un miroir** (les couches extrêmes sont
4,6× plus liées au token que les médianes) et **une périodicité de 12 couches**
(Jaccard 0,323 à écart 12 contre 0,035 ailleurs).

```bash
# Chiffrer l'empreinte d'un MoE depuis une trace de routage réelle
DRAVE_TRACE_EXPERTS=/tmp/routage.txt ./drave-core/target/release/drave \
    /home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2 \
    --ppl /tmp/ids_30b_wiki.txt --ctx 2048 --limit 2048 --dense --threads 10 --lot 1
python3 tools/analyse_empreinte.py /tmp/routage.txt --modele deepseek41
```

Détail : [`reports/rapport-empreinte-memoire.md`](reports/rapport-empreinte-memoire.md).

## Architecture mémoire : ce qui va en VRAM, en RAM, sur le disque

Débits **mesurés** : VRAM **84,9 Go/s** (noyau warp) · RAM **22 Go/s** (20 cœurs
physiques) · **NVMe 31 Go/s à 16 lecteurs parallèles** (5,4 à un seul) · PCIe 3.0
×16 ~12 Go/s · **NVLink GPU↔GPU 25,8 Go/s**. Le noyau GPU est **4× plus rapide
que le CPU**, et **le NVMe parallélisé dépasse la RAM**.

Trois mesures de topologie qui ferment des pistes : **l'hyperthreading n'apporte
rien** (40 threads = 22,8 Go/s, 20 cœurs = 22,6 — le moteur est corrigé pour
prendre les cœurs physiques, 30 → 20 fils) · **le NUMA ne paie pas** (4 % sur le
chemin NVMe, du bruit sur le calcul — l'UPI est rapide) · **pas de FPGA** dans
cette machine.

| niveau | capacité | contenu |
|---|---|---|
| **VRAM** | 30,2 Go | commun 8,0 Go (tête, attention, embeddings) + experts chauds 22,2 Go |
| **RAM** | 102 Go | jusqu'à 10 247 experts — 90 % des appels tiennent dans 71 Go |
| **NVMe** | 828 Go | le reste des experts + l'engram mmappé |

**Ce qui manque, par ordre de gain** : un noyau **attention MLA** (−194 ms/jeton,
c'est le premier poste et il n'est pas déportable) · un noyau **IQ2_XXS/Q2_K**
pour les experts de V4.1 (−86 ms) · **un chargeur parallèle d'experts** (les
2,39 Go par jeton passent de 435 ms à 77 ms sans aucun cache). Cumul :
**499 → ~150 ms par jeton**.

**Et une conclusion qui se retourne** : puisque le NVMe parallélisé (31 Go/s)
dépasse la RAM (22 Go/s), **ne rien cacher devient presque aussi rapide que tout
garder** — et ça libère les 71 Go de RAM du cache pour le **KV**, qui est le vrai
goulot à long contexte (96,6 Go en F16 à 1 M).

**Et le poste qu'on oublie** : le cache KV fait **96,6 Go en F16 à 1 M de
contexte** — plus que les 71 Go d'experts. Sa quantification n'est pas une
optimisation mais une condition : au-delà de 0,77 M de jetons en F16, il ne reste
plus de place pour les experts.

Détail : [`reports/rapport-architecture-memoire.md`](reports/rapport-architecture-memoire.md).

## Prochaines étapes

La feuille de route complète est dans [`docs/roadmap.md`](docs/roadmap.md). Ce qui
est ouvert aujourd'hui, par ordre de valeur mesurée :

1. **Le top-k déporté fonctionne — mais pas dans le préremplissage.** Les trois
   noyaux sont écrits, fusionnés en un seul (`attn_topk_tout` : descente radix,
   collecte et somme par ligne, 8 lancements → 2) et branchés dans le moteur
   (`DRAVE_GPU_TOPK=1`) : l'attention creuse déportée est **plate** (4,5–5,0
   ms/jeton de 255 à 4 095 clés) là où le CPU monte de 4,26 à 38,84, et le
   croisement tombe à ~300 clés. Détail : `reports/rapport-gpu-topk-selection.md`.
   **Ce qui manque** : le chemin par lots ignore `--attn-topk` (le moteur le dit),
   donc le préremplissage reste dense et coûte 246 s par sonde de 4 096 jetons au
   lieu de 75 — c'est le premier chantier de la prochaine session, avec la courbe
   du k nécessaire ([`reports/rapport-aiguille-topk.md`](reports/rapport-aiguille-topk.md)).
2. **La qualité de l'attention creuse** : à 4 096 clés, k = 256 (6 %) retrouve
   l'information 2 fois sur 3 (trois fenêtres distinctes) et k = 1 024 (25 %) 3 fois
   sur 3, l'attention complète 3 fois sur 3 — mais 8 fenêtres sur 9 seulement quand
   on en essaie neuf. Le **taux** est la bonne mesure, et il demande le top-k dans le
   préremplissage (point 1) pour être mesuré à moindre coût.
3. **Second GPU** : 16 Go dorment. Le cache d'experts MXFP4 et le KV paginé à 1 M
   les rempliraient utilement ; il faut un second contexte CUDA et une règle de
   répartition.
4. **Démonstration Colab** : tout est prêt côté code
   ([`colab/`](colab/README.md)), la manipulation demande un compte et un tunnel.
5. **Phase 2 locale** : ordonnanceur de flux (2 GPU, CPU, VRAM, RAM, NVMe),
   streaming des poids depuis le NVMe (3,5 Go/s) pour ce qui ne tient pas en RAM,
   cache d'experts rentable (+6 % aujourd'hui, l'objectif est ≥ +30 %).
6. **Phase 5, sur matériel** : le PE événementiel et le lecteur DDR3 existent et
   sont vérifiés ; il manque un accès à la carte pour la comparaison
   énergie/jeton. Le prototype C mesure 7,79 G événements/s et le croisement
   push/pull (~22 % de densité) — de quoi décider si le mode événementiel vaut le
   détour matériel.

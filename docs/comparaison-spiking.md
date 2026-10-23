# SpikeGPT, Spikformer, Spikingformer — ce qu'ils nous apprennent

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

Comparaison des trois architectures neuromorphiques de référence avec la nôtre,
et inventaire des astuces transposables.

Le cœur de Drave n'est pas remis en cause par cette comparaison : **router des
flux d'activation sur des grappes de neurones réparties entre composants et
machines** (`docs/vision.md`, axes 2-3) et **lire ces flux pour adapter
l'architecture à la tâche** (§2) restent les deux dimensions structurantes. Le
spike n'est examiné ici que comme **moyen d'obtenir la parcimonie** que nos
modèles quantifiés n'ont pas naturellement.

Mesures internes : `reports/rapport-inference.md`,
`reports/rapport-attention-creuse.md`, `reports/rapport-localite-activation.md`,
`reports/bilan-multi-materiel.md`.

Sources : [Spikformer](https://ar5iv.labs.arxiv.org/html/2209.15425) (Zhang et
al., ICLR 2023), [SpikeGPT](https://ar5iv.labs.arxiv.org/html/2302.13939) (Zhu
et al., 2023), [Spikingformer](https://ar5iv.labs.arxiv.org/html/2304.11954)
(Zhou et al., AAAI 2024).

---

## 1. Ce que fait chacun

**Spikformer** remplace la self-attention par une **Spiking Self Attention** :
Q, K, V sont des trains de spikes (0 ou 1), la carte d'attention est donc
naturellement non négative et **le softmax devient inutile**. L'opération
devient `SN(Q·Kᵀ·V·s)` — des ET logiques et des additions, **aucune
multiplication**. Deux conséquences : c'est décomposable (`Kᵀ·V` d'abord, en
O(N·d²) au lieu de O(N²·d)), et la consommation théorique de l'attention passe
de 77-88 µJ à **0,594 µJ**. Résultat : 74,81 % sur ImageNet en 4 pas de temps.

**SpikeGPT** abandonne l'attention : il porte **RWKV** dans le domaine
spiking — Spiking RWKV comme mélangeur de tokens, Spiking Receptance FFN comme
mélangeur de canaux. Trois idées : l'**alignement de la dimension séquence sur
la dimension temporelle** (pas de dimension T supplémentaire), l'entraînement
autorégressif, et des neurones à état. Le neurone LIF décharge à **R̂ = 0,15** :
15 % de spikes non nuls en moyenne. 46 M et 216 M de paramètres, **32,2× moins
d'opérations** et 33,2× moins d'énergie qu'un transformeur dense.

**Spikingformer** corrige un défaut structurel des deux autres : leur connexion
résiduelle `O_l = SN(ConvBN(O_{l-1})) + O_{l-1}` produit une valeur **non-spike**
(entiers 0,1,2,… jusqu'à 16 mesurés sur 8 blocs), qui alimente la couche suivante
en multiplications entier×flottant. Leur correction est un simple **échange
d'ordre** : `O_l = ConvBN(SN(O_{l-1})) + O_{l-1}`. Le flux résiduel reste
flottant — ce ne sont que des additions — mais **l'entrée de chaque couche
linéaire redevient purement discrète**, donc toutes les multiplications
redeviennent des accumulations. Gain : **+1,04 % de précision ET −57,34 %
d'énergie** sur ImageNet.

## 2. Comparaison avec notre architecture

| | Spikformer / SpikeGPT / Spikingformer | Drave |
|---|---|---|
| Origine de la parcimonie | **dynamique** : le seuil du LIF force des activations 0/1 | **structurelle** : les poids nuls ne coûtent rien |
| Taux d'activation mesuré | **R̂ ≈ 0,15** (SpikeGPT) | **0,00 % de zéros** sur un LLM dense entraîné |
| Valeur transmise | spike binaire (1 bit) | int8/int16 + poids int8 |
| Arithmétique | ET logique + **AC** (accumulation) | MAC (mais décalages+additions validés, 0 DSP sur FPGA) |
| Attention | SSA sans softmax, décomposable | **absente du domaine événementiel** |
| Résiduel | flottant, entrée des couches discrète (Spikingformer) | **idem** : `x = o + down` flottant, entrée quantifiée int8 |
| Entraînement | gradient de substitution, rétropropagation dans le temps | aucun (quantification après coup) |
| Énergie par opération | E_AC = 0,9 pJ contre E_MAC = 4,5 pJ (Horowitz) | 8,3 nJ/événement (FPGA, **projeté** : 4,83 G évts/s, limite DDR3) contre 57 nJ (CPU, **mesuré**) — rapport 6,9× |

**Deux observations qui nous concernent directement.**

**a) Ils ont résolu par construction le problème qui nous bloque.** Nous avons
mesuré que les activations d'un LLM dense ne sont **jamais** exactement nulles :
notre débit est donc constant **à seuil nul**, et l'argument « on ne paie que ce
qui s'active » reste théorique. À seuil 5 % du max, la densité mesurée tombe à
**17,9 %** — sous le croisement push/pull de **22 %**
(`reports/rapport-localite-activation.md`, `reports/rapport-croisement-push-pull.md`) —,
et c'est là que le coût redevient proportionnel à l'activité. Un réseau à spikes **impose** cette parcimonie : R̂ = 0,15, soit
**6,7× moins d'événements** dans notre moteur. Notre architecture événementielle
est mieux adaptée aux modèles à spikes qu'aux modèles quantifiés denses — c'est
un renversement de perspective.

**b) Nous appliquons déjà le principe de Spikingformer sans l'avoir cherché.**
Leur correction consiste à garder le flux résiduel en accumulation et à rendre
discrète l'entrée de chaque couche linéaire. C'est exactement ce que fait notre
`forward` : `x = o + down` reste flottant, et chaque produit matriciel reçoit un
vecteur d'activation **quantifié en int8** — jamais le résidu flottant. Le
principe « spike-driven » est donc déjà respecté ; la différence est que notre
discrétisation est à 8 bits plutôt qu'à 1.

## 3. Les astuces à reprendre, par ordre d'applicabilité

**1. L'alignement séquence = temps (SpikeGPT).** C'est l'astuce décisive, et
elle est contre-intuitive : chez Spikformer, la parcimonie est *par pas de
temps*, et il faut T pas de temps — le gain net est R̂×T, pas R̂. En alignant la
dimension séquence sur la dimension temporelle, SpikeGPT travaille à T = 1
effectif et **encaîne réellement les 6,7×**. Pour nous, cela veut dire : un
modèle récurrent à spikes, pas un transformeur à spikes.

**2. L'ordre dans le résiduel (Spikingformer).** Déjà acquis chez nous — mais à
vérifier formellement : aucun produit matriciel ne doit jamais recevoir autre
chose qu'un vecteur quantifié. C'est une contrainte de conception à inscrire,
pas un accident.

**3. L'attention sans softmax et décomposable (Spikformer).** C'est la réponse à
notre trou le plus sérieux : l'attention croît linéairement avec le contexte
(2,0 ms à 64 tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192) et ses poids
sortent d'un softmax, donc ne sont pas pré-stockables en listes. `SN(Q·Kᵀ·V·s)`
supprime le softmax et, en calculant `Kᵀ·V` d'abord (une matrice d×d), ramène la
complexité à O(N·d²) — **et rend l'attention exprimable en événements**, puisque
tout devient ET logique et accumulation.

**4. Le neurone LIF à état (SpikeGPT).** `U[t] = H[t] + β(Y[t] − (H[t−1] − U_reset))`,
seuil 1, reset 0, β = 0,5. Une mémoire à un scalaire par neurone, sans coût de
matrice — exactement le genre d'état que notre moteur peut porter dans le flux
d'événements plutôt que dans des tenseurs.

**5. BatchNorm au lieu de LayerNorm (Spikformer).** Ils rapportent que la
normalisation de couche « ne s'applique pas » aux SNN. Notre moteur utilise
RMSNorm flottant hors du domaine événementiel ; si nous passons aux spikes, BN
est à reprendre.

**6. L'embedding binaire (SpikeGPT).** Convertir l'embedding continu en spikes
par une fonction de Heaviside, avec gradient de substitution à la
rétropropagation — sinon le premier tenseur reste flottant et contamine tout.

## 4. Projection chiffrée pour notre moteur

Un modèle à spikes de type SpikeGPT alimentant notre moteur d'événements :

| | aujourd'hui (Qwen2.5-0.5B Q8) | avec R̂ = 0,15 |
|---|---|---|
| Événements par token | 352,8 M | **~53 M** |
| Débit mesuré (CPU, 16 threads) | 5,3 G évts/s | 5,3 G évts/s |
| Temps par token | 63 ms | **~10 ms** |
| Débit | 15,8 tok/s | **~100 tok/s** |

➡️ **Un facteur 6,7 sur le CPU, sans matériel supplémentaire** — à condition
d'avoir un modèle à spikes, donc de savoir l'entraîner.

## 5. Ce que ça change dans notre programme

1. **La cible du programme n'est plus « un LLM quantifié exécuté en listes »,
   mais « un modèle à décharge parcimonieuse exécuté en listes ».** Les deux sont
   compatibles avec notre moteur, mais seul le second donne le débit variable
   que le cahier des charges promettait.
2. **L'attention cesse d'être un trou béant** : la SSA décomposable est
   événement-compatible. C'est la brique à implémenter en priorité après la
   boucle d'apprentissage.
3. **La brique manquante reste la même** : l'entraînement. Les trois papiers
   entraînent par rétropropagation avec gradient de substitution — c'est
   précisément ce que notre pile ne sait pas faire, et cela confirme que c'est le
   verrou principal, pas un détail.

## 6. Réserves

- Les modèles à spikes restent **en retard de qualité** sur les transformeurs de
  même taille ; SpikeGPT parle de « compétitif sur les benchmarks testés », sur
  des corpus bien plus petits que ceux des LLM actuels.
- Les gains annoncés (32×, 57 %) sont **théoriques**, calculés avec
  E_AC = 0,9 pJ et E_MAC = 4,5 pJ sur du 45 nm — pas mesurés sur silicium.
  Notre chiffre, lui, donne 6,9× entre CPU et FPGA, du même ordre — mais la
  consommation FPGA est **projetée** (limite DDR3), seule la CPU est mesurée.
- Aucun de ces modèles n'est un modèle de langage à l'échelle des LLM actuels :
  SpikeGPT-216M est le plus gros SNN entraîné par rétropropagation à sa sortie.

# Capteur hebbien — apprendre des logs d'activation

*Réponse mesurée à : « peut-on avoir un flux de listes d'activations
post-traité sur une autre ressource pour apprendre de ces logs, et créer de
nouveaux nœuds par un principe hebbien ? »*

**Réponse courte : le capteur est presque gratuit et il fonctionne — mais la
création de nœuds par Hebb n'ajoute rien sur 69 % des poids du modèle, pour une
raison mathématique vérifiée sur les données.**

---

## 1. Le capteur, et ce qu'il coûte

`qtrinet-core --hebbian L --hebb-q Q --hebb-out F` branche un accumulateur sur
une projection : `H[o][i] += y[o] · x[i]`, **uniquement pour les sorties qui
« déchargent »** (|y| au-dessus du quantile Q). C'est le principe neuromorphique :
seuls les neurones qui tirent apprennent. Il ne modifie jamais le calcul.

Mesure sur 1 025 tokens de WikiText-2, couche 12, projection `ffn_gate`
(4 864 × 896), quantile 0,1 :

| | Temps |
|---|---|
| sans capteur | 96,75 s |
| avec capteur | 99,64 s |
| **surcoût** | **+3,0 %** |

499 175 activations capturées, soit 487 par token — exactement les 10 % demandés.
Trace produite : 17,4 Mo par couche.

➡️ **Sur un autre cœur, c'est gratuit** : la machine en a 24 inutilisés pendant
l'inférence. Le flux d'activations existe déjà (c'est lui qui pilote le moteur),
sa copie coûte 7 Ko par matrice, 1,2 Mo par token, soit 19 Mo/s à 15,8 tok/s.
Sur FPGA, le même point de mesure est une FIFO branchée sur le réseau de
réduction — quelques fils.

## 2. Que contient la trace ?

La trace est-elle une redite des poids, ou autre chose ?

| Mesure | Valeur |
|---|---|
| Énergie expliquée par `W · C` (prédiction linéaire) | **R² = 0,845** |
| Énergie **hors** de cette prédiction | **15,5 %** |
| 1ʳᵉ valeur singulière | **46,2 %** de l'énergie de la trace — contre 0,44 % pour `W` |
| 8 premières | 61,6 % — contre 2,3 % pour `W` |
| Rang effectif | 795 (trace) contre 894 (poids) |

➡️ La trace n'est **pas** une redite : 15,5 % de son énergie échappe à la
prédiction linéaire, et sa structure est radicalement différente de celle des
poids — **très concentrée** (la co-activation vit dans un sous-espace de faible
dimension) là où les poids sont presque isotropes. Le seuil de décharge introduit
une non-linéarité, et c'est là que se trouve le contenu.

## 3. La limite, et elle est dirimante

Une « nouvelle ligne » tirée de la trace est-elle une direction nouvelle ?

| Direction testée | Part dans l'espace des lignes de `W` |
|---|---|
| trace, direction n°0 | **100,00 %** |
| trace, direction n°1 | **100,00 %** |
| trace, direction n°2 | **100,00 %** |
| résidu non linéaire, directions n°0 à 4 | **100,00 %** |

Et le rang de `W` pour `ffn_gate` est de **896 sur 896 dimensions d'entrée** :
l'espace des lignes **est l'espace entier**.

➡️ **Tout nouveau nœud linéaire est une combinaison linéaire des nœuds
existants.** Sa pré-activation est une fonction linéaire des pré-activations
existantes ; avec la même non-linéarité, il n'ajoute rien. Ce n'est pas une
opinion : c'est un argument de rang, vérifié sur 1 025 tokens réels.

## 4. Où la création de nœuds a du sens, en revanche

Le critère est simple : **le rang des lignes est-il inférieur à la dimension
d'entrée ?**

| Projection | Forme | Rang | Nouveau nœud linéaire |
|---|---|---|---|
| `attn_q` | 896 × 896 | 853 | saturée |
| `attn_output` | 896 × 896 | 852 | saturée |
| `ffn_gate` | 4 864 × 896 | 896 | **saturée — zéro dimension disponible** |
| `ffn_up` | 4 864 × 896 | 896 | **saturée** |
| `attn_k` | 128 × 896 | 127 | **ouverte — 769 directions** |
| `attn_v` | 128 × 896 | 128 | **ouverte — 768 directions** |
| `ffn_down` | 896 × 4 864 | 893 | **ouverte — 3 971 directions** |

**69,2 % des poids** sont dans des projections saturées, **30,8 %** dans des
projections ouvertes. La création de nœuds hebbiens a donc un sens sur les
projections `k`, `v` et `down` — et aucun sur `gate`, `up`, `q` et `output`.

**Et surtout : ce qui échappe vraiment au span linéaire, c'est la
non-linéarité.** Il y a **401 856 monômes quadratiques** `x_i · x_j` dans un
espace d'entrée de 896 dimensions, dont aucun n'est une combinaison linéaire des
lignes existantes. Une trace hebbienne de *produits* — `H[o][(i,j)] += y[o] · x_i · x_j`
— capture un espace de caractéristiques réellement neuf. C'est la piste, pas la
trace linéaire.

## 5. Ce qui manque pour que ça apprenne vraiment

Le capteur mesure la **corrélation**. Or ce qui compte est l'**utilité**, et elle
n'est définie que par une perte. Un schéma qui tient debout :

1. **Hebb propose** — la trace désigne des candidats à moindre coût, sans
   gradient (c'est fait ici : +3,0 %).
2. **Un ajustement de lecture dispose** — les poids de sortie du nouveau nœud se
   calculent par moindres carrés sur le résidu, ce qui reste bon marché et sans
   rétropropagation complète.
3. **La perplexité tranche** — accepter ou rejeter le nœud.

Sans l'étape 2, une trace hebbienne ajoute des nœuds qui **corrèlent** sans
**servir** : c'est la limite de tout apprentissage non supervisé, et elle ne se
contourne pas par l'architecture.

## 6. Reproductible

```bash
cd qtrinet-core && cargo build --release
# trace hebbienne de la couche 12, 10 % des sorties, sur 1025 tokens réels
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --infer \
    --ids-file /tmp/wt2_1024.txt --n 1 --ctx 2048 --threads 16 --abits 16 \
    --hebbian 12 --hebb-q 0.1 --hebb-out /tmp/hebb12.bin
```

# Passer aux gros modèles : ce qui bloque, chiffré

> Question posée : que reste-t-il à améliorer sur le moteur événementiel pour
> faire tourner les plus gros modèles récents accessibles au public ?
> Réponse par les mesures, sur les modèles réellement présents sur cette machine.

## 0. Le parc disponible, et ce que le moteur sait en ouvrir

| modèle | taille | types de tenseurs | lisible ? |
|---|---|---|---|
| Qwen2.5-0.5B Q8_0 | 0,53 Go | Q8_0 | ✅ |
| Qwen2.5-0.5B Q4_0 | 0,35 Go | Q4_0 | ✅ |
| Qwen2.5-VL-7B Q4_K_M | 4,5 Go | **Q4_K** 6,09 G + **Q6_K** 1,52 G | ❌ |
| DeepSeek-R1-Distill-14B Q4_K_M | 8,6 Go | Q4_K + Q6_K | ❌ |
| Qwen3-30B-**A3B** Q4_K_M (MoE) | 17,7 Go | Q4_K 25,35 G + Q6_K 5,17 G | ❌ |
| Qwen2.5-Coder-32B Q4_K_M | 18,9 Go | Q4_K 27,29 G + Q6_K 5,48 G | ❌ |
| **gpt-oss-120b MXFP4** (MoE) | 60,5 Go | **MXFP4** 114,66 G + Q8_0 2,11 G | ❌ |

Le moteur ne lit que `F32`, `F16`, `Q8_0` et `Q4_0`. **Aucun modèle récent ne
s'ouvre aujourd'hui** : l'écosystème public est en `Q4_K_M` (toute la famille
Qwen/Llama/Mistral) et en `MXFP4` (gpt-oss-120b).

C'est le premier verrou, et de loin le moins intéressant scientifiquement — mais
tant qu'il tient, tout le reste est théorique.

## 1. Le vrai modèle de coût

Le moteur lit **une fois chaque poids actif, par jeton**. Le temps par jeton est
donc :

```
t = octets_actifs_par_jeton / bande_passante
```

Trois régimes mesurés sur ce moteur :

| représentation | octets par poids | quand elle gagne |
|---|---|---|
| listes d'événements (`PushMat`) | **1,98** | densité d'activation < 22 % |
| int8 dense (`DenseQ8`) | 1,00 | densité > 22 % |
| **4 bits** (`DenseQ4`) | **0,53** | grosses matrices, au-delà du cache |

Bande passante atteinte sur cette machine : **20–25 Go/s** (théorique ≈ 68 Go/s
par socket, 136 pour les deux — il y a là un facteur 3 non exploré, voir §4).

Ce modèle prédit correctement le débit mesuré : 0,49 G poids × 0,53 o = 0,26 Go
par jeton ÷ 20 Go/s = **13 ms/jeton = 41 tok/s**, contre **41,6 tok/s mesurés**.
Il est donc utilisable pour dimensionner.

## 2. Ce que ça donne sur les modèles visés

En 4 bits (0,53 o/poids), avec les paramètres **actifs** par jeton :

| modèle | actifs | octets/jeton | temps/jeton | tok/s |
|---|---|---|---|---|
| Qwen2.5-0.5B (dense) | 0,49 G | 0,26 Go | 13 ms | **41,6** (mesuré) |
| Qwen2.5-VL-7B (dense) | 7 G | 3,7 Go | 185 ms | 5,4 |
| DeepSeek-R1-Distill-14B | 14 G | 7,4 Go | 370 ms | 2,7 |
| Qwen2.5-Coder-32B (dense) | 32 G | 17 Go | 850 ms | 1,2 |
| **Qwen3-30B-A3B** (MoE) | 3,3 G | 1,7 Go | 87 ms | **11,5** |
| **gpt-oss-120b** (MoE) | 5,1 G | 2,7 Go | 135 ms | **7,4** |

➡️ **Sans MoE, cette machine plafonne vers 7 B en usage interactif et 32 B en
traitement de nuit.** Avec MoE, un modèle de 120 G paramètres passe devant un
dense de 32 G — parce que ce qui compte n'est pas la taille du modèle mais le
nombre de poids **réveillés par jeton**.

➡️ Et c'est exactement le régime où l'architecture événementielle cesse d'être
un coût : un routeur MoE qui allume 1 expert sur 8 est une **parcimonie
structurelle**, pas un k-WTA imposé après coup. Le croisement mesuré à 22 % de
densité tombe alors du bon côté.

## 3. Les quatre verrous, dans l'ordre

### 3.1 Formats de quantification — *le déblocage immédiat*

- **MXFP4** est le plus simple : bloc de 32 = 1 octet d'échelle E8M0
  (une **puissance de deux**) + 16 octets de valeurs E2M1. Les 8 magnitudes
  valent `{0,1,2,3,4,6,8,12}` — donc, multipliées par 2, des **entiers** qui
  tiennent sur 4 bits. Un noyau MXFP4 est notre noyau AVX2 actuel avec un
  `pshufb` (table de 16 entrées) à la place du `(nibble − 8)`, et l'échelle de
  bloc se replie en ajustement d'exposant. L'import serait **exact**, sans
  requantification.
- **Q4_K / Q6_K** : super-blocs de 256 poids, échelles et minima sur 6 bits.
  Plus de travail (dépaquetage des 12 octets d'échelles), mais incontournable :
  c'est le format de toute la famille Qwen/Llama. Q6_K accompagne toujours Q4_K
  dans le même fichier.

**MXFP4 : fait, et vérifié sur le vrai fichier.** Bloc de 17 octets (exposant
E8M0 + 16 octets de nibbles E2M1). Les huit magnitudes du format sont
`{0, ½, 1, 1½, 2, 3, 4, 6}` : **doublées**, ce sont les entiers
`{0,1,2,3,4,6,8,12}`, et l'échelle de bloc est une puissance de deux. L'import
est donc **exact** — il n'ajoute aucune erreur, contrairement au passage par les
f32 qui coûtait 12 % de perplexité sur Q4_0. Un test unitaire le vérifie contre
une référence f64, et le noyau AVX2 (table de 16 octets chargée par `pshufb`,
échelle repliée en exposant) reste bit à bit identique au scalaire.

Contrôle sur `gpt-oss-120b-MXFP4.gguf` (60,5 Go), sans charger le fichier :

```
tenseur témoin : blk.0.ffn_down_exps.weight   dims = (2880, 2880, 128)   type 39
exposants : min 119  max 121  médian 120                        → 2^-8 … 2^-6
|v|max / (6·2^(e−127)) : médian 1.000, min 0.667
```

Un ratio médian de **1,000** signifie que le plus grand poids de chaque bloc
atteint exactement la magnitude maximale du format : c'est la signature d'un
bloc correctement mis à l'échelle. Elle valide d'un coup la taille de bloc, la
table E2M1, l'ordre des nibbles et la sémantique de l'exposant.

Et elle révèle la structure qui manque au moteur : `dims = (2880, 2880, 128)` —
**128 experts empilés dans un tenseur 3D**. Nos `Proj` sont 2D.

### 3.2 Zéro copie — *sinon les gros modèles ne tiennent pas*

Aujourd'hui `Model::load` **matérialise une seconde copie** des poids (listes
d'événements, `DenseQ8` ou `DenseQ4`), et `Gguf::open` fait un `read_to_end` :
le fichier est lu intégralement en mémoire.

Pour gpt-oss-120b : 60 Go de fichier + 61 Go de copie 4 bits = 121 Go sur 125.
Ça ne passe pas. Or le moteur **sait déjà** lire en place — `q4_blocks()` et
`q8_view()` renvoient des tranches du tampon chargé, sans copie, et c'est ce que
fait la tête de sortie depuis le début. Il suffit de généraliser ce chemin à
toutes les projections : **60 Go résidents, zéro copie**, et le noyau AVX2 lit
les blocs du fichier directement.

### 3.3 MoE — *la fonctionnalité qui décide de tout*

Le moteur n'a aucune notion d'expert. Il faut :

1. le **routeur** (top-k sur la porte, normalisation des poids d'experts,
   expert partagé le cas échéant) ;
2. des **tranches de poids par expert** (les tenseurs `ffn_*_exps` sont
   empilés : un `Proj` par expert, ou une vue indexée) ;
3. la **lecture sélective** : ne charger que les experts retenus. C'est là que
   l'architecture événementielle redevient naturelle — et qu'un cache d'experts
   chauds (les experts sont réutilisés d'un jeton à l'autre) peut diviser le
   trafic réel par un facteur supplémentaire.

### 3.4 Contexte et KV — *le prochain mur, déjà visible*

Le cache KV est en f32, par couche, non paginé. À 128 k de contexte sur un
modèle à GQA, il dépasse la taille des poids d'une couche, et il est relu
**entièrement à chaque jeton** : l'attention mesurée croît exactement
linéairement avec le contexte (0,88 / 1,91 / 3,20 ms à 64 / 128 / 256).
Il faut : KV quantifié (int8/int4), paginé, et — pour les architectures récentes
— le support de **MLA** (DeepSeek), qui compresse le KV en latents et change
complètement la donne mémoire.

## 4. Le facteur 3 inexploré : la bande passante

Nous atteignons 20–25 Go/s là où deux sockets DDR4-2133 en offrent ~136. Les
pistes, par ordre de probabilité :

1. **NUMA** : les poids sont alloués par un seul thread (*first-touch* sur le
   socket 0) ; la moitié des accès traverse le QPI. Allocation *premier-touch
   parallèle*, ou épinglage.
2. **Mmap + grosses pages** : `read_to_end` alloue de la mémoire anonyme en
   4 Ko de page ; 60 Go de poids, c'est 15 M de pages et autant de défauts de
   TLB. Des pages de 2 Mo diviseraient ce coût par 512.
3. **Recouvrement** : aujourd'hui le moteur alterne lecture et calcul par
   projection. Un préchargement explicite (`_mm_prefetch` sur la projection
   suivante) pendant le calcul de la courante est gratuit à écrire.

Test NUMA préliminaire (8 threads, `numactl`) : repère 20,7 → **24,7 Go/s** en
liant tout à un socket. Le gain existe mais n'explique pas tout ; c'est un
chantier à part entière, et il multiplie **tout** le reste.

## 5. Et la thèse événementielle là-dedans ?

Le passage à l'échelle ne condamne pas l'architecture, il la **précise** :

| ce que la mesure dit | conséquence |
|---|---|
| un événement coûte 1,98 o, soit 3,7× un poids 4 bits | encoder les valeurs sur 4 bits, et les écarter quand elles sont nulles : ~1,5 o/événement |
| le croisement est à 22 % de densité | l'événementiel n'est rentable que sur une parcimonie **structurelle** |
| les plus gros modèles publics sont des MoE | la parcimonie structurelle est arrivée — mais elle s'appelle « experts », pas « k-WTA » |
| l'accumulateur décide du débit en régime creux (mesuré : ×1,7 entre 4 et 32 threads sur des événements épars) | le **tuilage de la dimension de sortie** est le paramètre d'architecture, pas un détail |
| QSFP+ 4,8 Go/s, NVLink 25,78 Go/s, PCIe x8 6,5 Go/s | le flux d'événements adressé par destination est un protocole réseau naturel : c'est la thèse du CDC, et elle devient mesurable dès qu'un modèle dépasse un nœud |

Le point qui compte : **un événement est adressable**. Contrairement à une ligne
de poids dense, il porte sa destination. C'est ce qui permet de découper un
modèle entre nœuds sans diffuser les activations, et c'est la seule chose que le
dense ne sait pas faire aussi bien.

## 6. Ordre de marche proposé

| # | chantier | effort | débloque |
|---|---|---|---|
| 1 | lecteur **MXFP4** — *fait, testé, vérifié sur gpt-oss-120b* | faible | ✅ |
| 2 | lecteur **Q4_K / Q6_K** | moyen | toute la famille Qwen/Llama 7–32 B |
| 3 | **zéro copie** (lecture en place généralisée) | faible | tout modèle > 32 Go |
| 4 | **routage MoE** + tranches par expert | moyen | Qwen3-30B-A3B, gpt-oss-120b à leur vrai débit |
| 5 | **KV quantifié + paginé**, puis MLA | moyen | contextes longs |
| 6 | bande passante : mmap, grosses pages, premier-touch parallèle | moyen | ×2–3 sur **tout** |
| 7 | transport d'événements multi-nœuds | élevé | dépasser un nœud |

Les points 1 à 3 sont la condition d'existence ; 4 et 6 sont les multiplicateurs ;
7 est la thèse.

## 7. Reproductible

```bash
# types de tenseurs d'un GGUF (script de recensement)
python3 - <<'PY'
import struct
f=open("model.gguf","rb"); assert f.read(4)==b"GGUF"
struct.unpack("<I",f.read(4)); nt,=struct.unpack("<Q",f.read(8)); nkv,=struct.unpack("<Q",f.read(8))
# ... (cf. journal de session pour le parseur complet)
PY

# modèle 4 bits natif, noyau 4 bits
cd drave-core
./target/release/drave ../models/Qwen2.5-0.5B-Q4_0.gguf --ppl /tmp/wt2_ids.txt \
    --ctx 256 --abits 16 --threads 16 --limit 512 --q4

# repère de bande passante (lu dans le même banc, mêmes conditions)
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --matrix blk.0.ffn_gate.weight --threads 16
```

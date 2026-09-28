# Convertisseur et chargement : ce que la mesure dit de faire

> Directive : « un convertisseur de modèle haute fidélité afin d'avoir un
> chargement optimal : abolition des zéros, identification des clusters et MoE,
> tuning CPU/hyperthread/core pour les calques sur CPU et similaires pour les
> calques sur GPU avec optimisation des calques en fonction des routes PCIe ».
>
> Ce document confronte chacun de ces quatre points à la mesure, puis propose le
> format et l'ordre de marche.

## 1. Ce que « chargement optimal » veut dire, mesuré

Le chargement d'un modèle passait par une **copie complète** : déquantifier les
f32, puis reconstruire les poids dans notre disposition. Mesuré sur le 0,5B
Q4_0 :

| | avant (copie) | après (emprunt) |
|---|---|---|
| chargement des 24 couches | 2,70 s | **0,845 s** |
| mémoire crête (fichier 353 Mo) | ~700 Mo | **413 Mo** |
| perplexité (510 jetons) | 21,0116 | **21,0110** |

Le gain de perplexité n'est pas un bruit : l'import réencodait l'échelle de bloc
sur 16 bits relatifs (erreur 1/32767), l'emprunt lit l'échelle d'origine. **La
lecture en place est plus fidèle que la conversion.**

➡️ **Conséquence de conception : dans le chemin dense, le convertisseur est
inutile.** Les blocs Q4_0 et MXFP4 du fichier se lisent tels quels : les nibbles
bas sont les poids 0–15 et les hauts les poids 16–31, donc les activations à
apparier sont **contiguës** — l'entrelacement de notre disposition était une
commodité, pas une nécessité. Un noyau AVX2 lit les blocs du fichier sans rien
réarranger, et les sommes entières restent **bit à bit identiques** (vérifié par
test unitaire).

Pour gpt-oss-120b, c'est la différence entre 121 Go (60 de fichier + 61 de copie)
et **60 Go** — c'est-à-dire entre ne pas tenir en mémoire et tenir.

## 2. Abolition des zéros : où elle paie, où elle coûte

Taux mesurés :

| source | zéros exacts |
|---|---|
| MXFP4 (gpt-oss-120b, 4 tenseurs) | **12,0 – 17,9 %** |
| Q8_0 (Qwen2.5-0.5B) | 0,76 % |

Un schéma à masque (32 bits de présence + 4 bits par poids non nul) coûte 1
bit/poids de masque :

| zéros | dense 4 bits | masque + valeurs | gain |
|---|---|---|---|
| 0 % | 16,0 o | 20,0 o | −25 % |
| 12 % | 16,0 o | 18,1 o | −13 % |
| 18 % | 16,0 o | 17,1 o | −7 % |
| **25 %** | 16,0 o | 16,0 o | **0 %** |
| 40 % | 16,0 o | 13,6 o | +15 % |
| 70 % | 16,0 o | 8,8 o | +45 % |

➡️ **Le seuil est à 25 %, et MXFP4 est à 12–18 % : en dense, abolir les zéros
coûte plus que ça ne rapporte.** En revanche :

- **en mode événements**, c'est déjà fait et c'est gratuit : un poids nul ne
  produit aucun événement. 15 % de zéros MXFP4 = 0,30 octet/poids économisé,
  soit 15 % du flux d'événements ;
- **en MoE**, c'est le vrai levier : un routeur top-4 sur 128 experts n'allume
  que **3 %** des poids du FFN. Ce n'est plus de l'abolition de zéros, c'est du
  non-chargement.

## 3. Identification des clusters

Deux usages distincts, à ne pas confondre :

1. **Grappes effectives** (destination) : réordonner la dimension de sortie pour
   que les destinations co-activées soient adjacentes. Mesuré précédemment :
   un élagage *contigu* est 30 % plus rapide qu'un élagage *dispersé* à taux
   égal — c'est l'effet de l'accumulateur. À retester sur les grosses couches
   (`ffn` 18 944 pour un 7B : accumulateur de 76 Ko, donc hors L1).
2. **MoE** : les experts sont **déjà** des clusters — un tenseur 3D
   `dims = (2880, 2880, 128)` empile 128 experts. Il n'y a pas de cluster à
   découvrir, il y a un tenseur à découper et un routeur à exécuter.

Le convertisseur doit donc produire : une **permutation** de la dimension de
sortie (avec sa table), et des **tranches d'experts** alignées sur des pages.

## 4. Placement CPU / GPU et routes PCIe

Ce que la machine a déjà mesuré :

| chemin | débit | usage |
|---|---|---|
| DDR3 de la carte FPGA | 9,66 Go/s | lecture de listes |
| CPU, 16 threads | 14–25 Go/s | tout ce qui précède |
| PCIe x8 (gen 3) | 6,5 Go/s | transfert CPU↔GPU |
| QSFP+ | 4,8 Go/s | inter-nœuds |
| NVLink (2× Quadro RTX 5000) | 25,78 Go/s | inter-GPU |
| GPU, lecture | 380 Go/s | poids denses |
| GPU, dispersion d'événements | 18,1 G év/s | mode push |

Deux enseignements pour le placement :

- **NUMA d'abord** : 20,7 → **24,7 Go/s** en liant un socket (mesuré au banc).
  Un plan de placement qui ignore les nœuds NUMA laisse 20 % sur la table, et
  probablement bien plus sur un modèle qui ne tient pas dans un socket.
- **La route PCIe est le goulot d'un montage hybride** : à 6,5 Go/s, envoyer un
  flux d'événements au GPU coûte plus cher que de le calculer sur CPU tant que
  le CPU tient 5,3 G év/s (≈ 10,6 Go/s d'événements). **Le seuil d'intérêt du
  GPU par PCIe est donc proche de 1** : il ne se justifie que si le GPU calcule
  *plus* que ce qu'on lui envoie — c'est-à-dire s'il garde les poids et ne reçoit
  que les activations.

## 5. Format proposé : `QTNT`

Un conteneur, un index, des sections alignées.

```
en-tête      magie, version, nb_calques, nb_tenseurs, alignement (2 Mo), graine
index        par tenseur :
               nom, rôle (Wq/Wk/Wv/Wo/gate/up/down/routeur/expert),
               calque, rang d'expert, dimensions,
               encodage (blocs_source | dense4 | listes),
               offset (aligné), taille, empreinte,
               statistiques (zéros, blocs vides, variances de grappe),
               placement (cpu|gpu, nœud NUMA, nb de threads conseillé,
                          route (pcie|nvlink|qsFP), priorité de préchargement)
permutation  table de réordonnancement de la dimension de sortie (clusters)
sections     blocs de poids, alignés 2 Mo (grosses pages, lecture directe)
```

Règles de conception, chacune adossée à une mesure :

1. **Les poids restent dans leur format d'origine** quand il est déjà en 4 bits
   (`blocs_source`) : c'est ce qui rend la conversion **fidèle par
   construction** — il n'y a rien à convertir.
2. **Les listes d'événements ne sont pas matérialisées** : 1,98 o/poids × 120 G
   = 237 Go, impossible. Elles se dérivent **par expert et à la demande**.
3. **Une tranche par expert**, alignée, pour que le chargement d'un expert soit
   une lecture contiguë — et pour que le cache d'experts chauds soit possible.
4. **L'index est en tête** : le plan de placement se lit avant les poids, donc on
   peut décider où charger chaque calque sans avoir lu le modèle.
5. **L'alignement 2 Mo** est ce qui permettra les grosses pages le jour où mmap
   sera disponible (`std` seul ne l'expose pas ; en attendant, `pread` par
   section donne déjà le chargement à la demande).

## 6. Fidélité : comment on la prouve

La fidélité n'est pas une intention, c'est un test. Trois niveaux, du plus fort
au plus faible :

| niveau | critère | état |
|---|---|---|
| **bit à bit** | même forme d'exécution, même résultat | ✅ obtenu (push/pull/auto : PPL 19,2641 identique ; AVX2 vs scalaire : identique) |
| **exact** | aucun réencodage : les octets du fichier sont ceux exécutés | ✅ obtenu pour Q4_0 et MXFP4 (emprunt) |
| **équivalent** | même perplexité à l'arrondi près | ✅ (import 21,0116 contre emprunt 21,0110) |

Un convertisseur qui réencode doit prouver le niveau « exact » ou renoncer à
l'appeler haute fidélité. C'est exactement ce que la double quantification avait
coûté : **12 % de perplexité** sur Q4_0 avant qu'on s'en aperçoive.

## 7. Ordre de marche

| # | chantier | état | gain mesuré ou attendu |
|---|---|---|---|
| 1 | emprunt des blocs en place (Q4_0, MXFP4) | ✅ **fait** | chargement ×3,2, mémoire ÷2, fidélité exacte |
| 2 | lecteur **Q4_K / Q6_K** | à faire | ouvre 7B → 32B |
| 3 | **routeur MoE** + tranches par expert | à faire | gpt-oss-120b : 61 Go/jeton → 2,7 Go/jeton |
| 4 | conteneur `QTNT` + index de placement | à faire | plan CPU/GPU/NUMA lisible avant les poids |
| 5 | placement : épinglage NUMA, threads par calque | à faire | 20,7 → 24,7 Go/s mesuré au banc |
| 6 | **Q8_0 en place** (le noyau `q8_dot_at` existe déjà pour la tête) | à faire | supprime la dernière copie du chemin int8 |
| 7 | mmap (appel système direct) | à faire | grosses pages, partage entre processus |

Les points 1 et 6 sont ce qui rend un modèle de 60 Go **chargeable** ; 2 et 3
sont ce qui le rend **exécutable** ; 4 et 5 sont ce qui le rend **efficace**.

---

# État après implémentation (mesuré)

## Ce qui est fait

| # | chantier | état | vérification |
|---|---|---|---|
| 1 | emprunt des blocs en place | ✅ | Q4_0, MXFP4, **Q4_K**, **Q6_K**, Q8_0 (tête) |
| 2 | lecteur **Q4_K / Q6_K** | ✅ | comparé à une référence **F16 des mêmes poids** produite par `llama-quantize`, tenseur par tenseur |
| 3 | **routeur MoE** + tranches par expert | ✅ | Qwen3-30B-A3B (128 experts, top-8) : PPL 7,61 |
| 4 | **index de placement** (`--plan`) | ✅ | poids par couche, octets actifs par jeton, débit prévu par support |
| 4 bis | **épinglage NUMA** (`--pin`) | ✅ mesuré, **négatif** | 23,2 → 25,5 s (cœurs physiques) et → 27,6 s (un socket) sur le 30B MoE |
| 5 | **Q8_0 en place** (projections) | ✅ | chargement 2,73 → 0,81 s, mémoire 921 → 566 Mo |

## Le parc de modèles, maintenant

| modèle | format | PPL (notre jeu) | tok/s | chargement | mémoire |
|---|---|---|---|---|---|
| Qwen2.5-0.5B | Q8_0 | 19,3885 | 32 | **0,81 s** | **0,57 Go** |
| Qwen2.5-0.5B | Q4_0 | 21,0110 | 39 | **0,87 s** | 0,41 Go |
| Qwen2.5-1.5B | Q4_K_M | 12,9228 | 17 | 4,2 s | 1,1 Go |
| Qwen2.5-VL-7B | Q4_K_M | 10,9947 | 2,8 | 24 s | 4,5 Go |
| **Qwen3-30B-A3B** | Q4_K_M | **7,6139** | 5,4 | 13,3 s | **17,7 Go** |
| gpt-oss-120b | MXFP4 | — | — | lit les blocs | 60 Go |

La chaîne est cohérente : 19,3 → 12,9 → 11,0 → 7,6 de perplexité pour
0,5 → 1,5 → 7 → 30 G paramètres. **Le 30B tient en 17,7 Go, soit exactement la
taille du fichier** : aucune copie, aucune requantification.

## La méthode qui a trouvé les bugs

`llama.cpp` est installé sur la machine (`llama-cli`, `llama-perplexity`,
`llama-quantize`). C'est la référence qui manquait :

1. **`llama-perplexity`** donne la vérité terrain sur un modèle :
   11,3954 pour le 1,5B Q4_K_M sur le fichier entier — contre 50 000 chez nous,
   ce qui a rendu le bug incontestable.
2. **`llama-quantize --allow-requantize … F16`** fabrique une référence des
   **mêmes poids** en demi-précision. Comparer notre déquantification bloc par
   bloc à ce fichier a montré : Q4_K exact à 1e-5 (bruit f16), Q6_K **faux** —
   ggml écrit les quatre quants en quarts successifs, je les entrelaçais.
3. **Le bug le plus coûteux n'était pas dans la quantification** : le
   Qwen2.5-1.5B a un tenseur `output.weight` **distinct** de `token_embd.weight`
   (poids non liés) ; notre tête était câblée sur la table d'embedding. Perplexité
   50 000 au lieu de 11,4 — et le 0,5B, qui a des poids liés, ne pouvait pas le
   révéler.

## Ce que le MoE change à la thèse

Un routeur top-8 sur 128 experts n'allume que **6 %** du FFN. C'est très en
dessous du croisement mesuré à 22 % de densité : le régime où l'architecture
événementielle cesse d'être un coût est **exactement celui des grands modèles
publics actuels**. Le 30B-A3B lit 1,8 G poids par jeton au lieu de 30 G.

## Deux résultats négatifs, mesurés

**L'épinglage NUMA ne paie pas.** Le banc de bande passante montrait 20,7 → 24,7
Go/s en liant les fils à un socket ; sur la charge réelle c'est une **perte** :
23,2 → 27,6 s sur le 30B MoE. Lier les seize fils à dix cœurs physiques met deux
fils par cœur, et la barrière tournante souffre doublement de la contention SMT.
Même en se limitant aux cœurs physiques des deux sockets : 25,5 s. L'ordonnanceur
fait mieux seul. Le drapeau `--pin` reste disponible, documenté comme perdant ici.

**Le plan surestime le débit des MoE d'un facteur 2.** Il annonçait 12 tok/s pour
le 30B-A3B à 20 Go/s ; nous en mesurons 5,4. Les tranches d'experts sont lues à
**8 Go/s**, pas 20 : dix-huit mille tranches de 900 Ko dispersées sur 18 Go
coûtent en TLB et en localité ce que la lecture séquentielle ne paie pas. Le plan
chiffre maintenant aussi ce régime — 4,81 tok/s prévus contre 5,4 mesurés.

## Reste à faire

1. **Q4_K sur FPGA** : le format des modèles réels, à porter dans `event_reader`.
2. **Épinglage NUMA** : 20 % mesurés, mais `sched_setaffinity` n'est pas dans
   `std` — il faut un appel système direct.
3. **Q8_0 en place** pour les projections (la tête le fait déjà).
4. **gpt-oss-120b** : le routeur MoE fonctionne (top-4 sur 128) mais le modèle
   pèse 60 Go et son encodage d'expert est en MXFP4 avec des tenseurs Q8_0 ;
   c'est l'étape suivante naturelle.

---

# gpt-oss-120b : la machine tient, le modèle n'est pas encore juste

## Ce qui marche

`gpt-oss-120b` **charge et tourne** : 62,2 Go résidents — la taille du fichier,
aucune copie — pour 62,2 Go de mémoire crête, à **~195 ms par jeton (5 tok/s)** :

| poste | ms/jeton | débit implicite |
|---|---|---|
| projections d'attention (Q8_0, 36 couches) | 42 | **21 Go/s — au mur** |
| experts MoE (4 sur 128, MXFP4) | 148 | 12,4 Go/s |
| tête de sortie (Q8_0, 579 M poids) | 23 | 27 Go/s |
| attention (fenêtre 128) | 1,1 | — |

Le **tokenizer o200k** est vérifié : identique à celui de llama.cpp sur 7 cas
pièges (CamelCase, nombres par groupes de trois, contractions, accents, tirets
cadratins, dates), via l'API `/tokenize` de `llama-server`.

## Ce qui a été ajouté pour lui (et sert aux autres)

- **biais du routeur** (`ffn_gate_inp.bias`) et **biais par expert** (gpt-oss en a
  trois par expert, Qwen3-MoE aucun) ;
- **puits d'attention appris** (`attn_sinks.weight`) : une clé virtuelle de
  valeur nulle qui ne compte que dans le dénominateur du softmax ;
- **`post_attention_norm`** — c'est le `ffn_norm` de gpt-oss sous un autre nom ;
- **fenêtre glissante lue des métadonnées** (`attention.sliding_window = 128`) ;
- **RoPE YaRN** : rampe entre extrapolation (basses dimensions) et interpolation
  (hautes), `mscale = 1 + 0,1·ln(facteur)`.

Un bug corrigé au passage : les valeurs par défaut de la ligne de commande
**écrasaient** les métadonnées du modèle (`attn_window ← 0`, `attn_sinks ← 4`),
ce qui désactivait silencieusement la fenêtre glissante. Désormais `0` signifie
« garder ce que dit le modèle ».

## Ce qui reste faux

La perplexité de gpt-oss est **42 127** : la sortie n'est pas encore correcte.
Trois candidats, non départagés faute de référence :

1. les **constantes YaRN** (le `mscale` et les dimensions de correction varient
   selon les implémentations) ;
2. la **convention du softmax de routage** : softmax sur les 128 experts puis
   top-k (ce que nous faisons, comme Qwen3), ou softmax sur les seuls top-k
   (certaines implémentations de gpt-oss) ;
3. la **fenêtre et les puits** : après correction de l'écrasement, le puits
   appris s'est révélé **inerte** sur la perplexité, ce qui reste inexpliqué.

La méthode qui a trouvé les bugs précédents s'applique : `llama-quantize` pour
une référence de poids, `llama-server /tokenize` pour le découpage. Il manque
l'équivalent pour les **logits** — un moyen de comparer la sortie couche par
couche à llama.cpp sur ce modèle.

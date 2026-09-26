# Inférence complète en Rust — Qwen2.5-0.5B sans GPU, sans BLAS, sans dépendance

**2 319 lignes de Rust, `std` seul, zéro dépendance.** Le modèle Qwen2.5-0.5B-Instruct
quantifié Q8_0 (507 Mo, 494 M de poids) tourne en **mode listes d'événements** sur le
CPU de cette machine (2 × Xeon E5-2687W v3), et génère du texte correct :

```
$ qtrinet-core qwen2.5-0.5b-q8_0.gguf --infer --chat \
      --prompt "Explain in one sentence why the sky is blue."

<|im_start|>user
Explain in one sentence why the sky is blue.<|im_end|>
<|im_start|>assistant
The sky is blue because it reflects sunlight, which contains colors such as
red, orange, yellow, green, blue, and indigo, which are all visible in the
spectrum.<|im_end|>

généré  : 38 tokens en 3.86 s  (9.85 tok/s)
```

Aucun GPU. Aucune bibliothèque de tenseurs, aucune BLAS, aucun crate : le lecteur
GGUF, le tokenizer BPE, le moteur d'événements et le forward Qwen2 sont écrits ici.

---

## 1. Ce qui a été construit

| Fichier | Rôle | Lignes |
|---|---|---|
| `src/gguf.rs` | lecteur GGUF, déquantification Q4_0/Q8_0/F16/F32, ligne Q8_0 | 332 |
| `src/list.rs` | 4 encodages de listes, dont `PushMat` (écart + valeur int8) | 321 |
| `src/engine.rs` | pool à barrière atomique, décodeurs SWAR, modes push/pull | 510 |
| `src/tokenizer.rs` | BPE byte-level Qwen2, pré-tokenizer réécrit à la main | 371 |
| `src/model.rs` | forward Qwen2 : RMSNorm, RoPE, GQA + cache KV, SwiGLU, tête | 403 |
| `src/main.rs` | mesures du moteur + inférence + perplexité | 382 |

**Le forward est complet** : embedding, 24 couches (attention groupée 14 têtes / 2 KV
avec biais QKV, RoPE base 1e6, MLP SwiGLU), norme finale, tête liée, échantillonnage
glouton ou température + top-40, arrêt sur `<|im_end|>`.

## 2. Validation : identique à la référence, token pour token

La référence est `src/transformer_np.py` (numpy/OpenBLAS, float32, poids Q8_0
déquantifiés). Même prompt (ids `9707,0`), décodage glouton, 16 pas :

| | tokens générés |
|---|---|
| numpy float32 | `358 2776 264 48948 304 13027 323 358 2776 4460 311 1855 264 2025 429 646` |
| **moteur d'événements** | `358 2776 264 48948 304 13027 323 358 2776 4460 311 1855 264 2025 429 646` |

**16/16 identiques.** Les logits suivent à 0,3–0,5 % près :

| pas | numpy | moteur |
|---|---|---|
| 0 | 358 (17,3063) | 358 (17,0202) |
| 2 | 264 (13,4068) | 264 (13,4408) |
| 4 | 304 (17,2215) | 304 (17,1400) |

L'écart résiduel est la **quantification des poids par ligne** (notre format) au lieu
des blocs de 32 de Q8_0 — un choix de format, pas une erreur de calcul.

### Perplexité WikiText-2 (2 040 tokens, fenêtres de 256)

| moteur | perplexité |
|---|---|
| numpy float32 (OpenBLAS) | 25,0004 |
| **moteur d'événements (int16)** | **24,8995** |

Écart : **−0,4 %** — la qualité est préservée. (La valeur absolue plus élevée que les
20,29 du harnais précédent vient de la fenêtre de 256 et de l'échantillon court.)

## 3. Performances mesurées

Machine : 2 × Xeon E5-2687W v3 (20 cœurs / 40 CPU logiques), bureau actif.

| | valeur |
|---|---|
| Chargement du modèle (quantification + transposition) | 6,3 s |
| Mémoire résidente | **1,27 Go** (dont 0,71 Go de listes) |
| Événements par token | **352,8 M** |
| **Débit de génération** | **10,5 tok/s** (int16) · 10,6 (int8) · **11,4 en dense** |
| Temps par token | 100 ms = 90 ms de forward + 10 ms de tête |
| TTFT | 74–95 ms |
| Débit pendant le forward | **3,9 G événements/s** |

Montée en charge de l'inférence (meilleur de 2, densité 100 %) :

| Threads | 1 | 8 | 16 | 24 | 32 |
|---|---|---|---|---|---|
| tok/s | 1,51 | 8,22 | **10,52** | 10,15 | 9,83 |

➡️ L'optimum est vers **16 threads** — la moitié des CPU — et non 32 : un token paie
**168 barrières** (7 matrices × 24 couches), donc le coût fixe compte plus que dans le
microbanc. Le défaut du mode `--infer` est réglé sur `CPU/2`.

Pour comparaison, la référence numpy + OpenBLAS (40 threads) faisait 132 ms par token,
soit 7,6 tok/s. **Le moteur d'événements est 38 % plus rapide que numpy+BLAS** — sans
BLAS, sans GPU, et en arithmétique entière exacte.

### Combien coûte l'architecture événementielle sur CPU ?

Question centrale du projet, et elle a maintenant une réponse mesurée. Le même modèle,
la même quantification (int8 par ligne), les mêmes activations (int16), les mêmes
tokens générés — seule change la façon de parcourir les poids :

| | mémoire des poids | tok/s (16 threads) |
|---|---|---|
| **Listes d'événements** (push, dispersion, réduction) | 0,71 Go — **1,44 o/poids** | **10,52** |
| Matrice dense int8 (produit scalaire par ligne) | 0,49 Go — **1,06 o/poids** | **11,42** |

➡️ **L'architecture événementielle coûte 8 % sur CPU** — alors qu'elle lit 36 % de
mémoire en plus, décode des écarts en varint et disperse dans 16 accumulateurs avant
réduction. Elle est déjà au niveau du dense.

*Pour être honnête sur le protocole : le dense a d'abord été 20 % plus **lent*
(8,5 tok/s) parce que sa boucle de produit scalaire était limitée par une chaîne
d'accumulation i64 unique. Déroulée 4× avec quatre accumulateurs, elle passe à
11,4 tok/s. La comparaison ci-dessus est celle de deux implémentations soignées.*

*Et sur ce CPU (AVX2 disponible), un noyau dense écrit à la main en intrinsèques
irait encore plus vite — ce que le moteur d'événements ne peut pas se permettre, sa
dispersion n'étant pas vectorisable (AVX2 n'a ni gather ni scatter entier). C'est
précisément le pari matériel : le FPGA ne paie pas ce coût, et n'a pas de
multiplieur du tout.*

## 4. Deux compromis assumés

### La tête de sortie n'est pas en mode push

Le plafond d'embedding fait 151 936 sorties. En mode push il faudrait un accumulateur
de 151 936 × 8 octets **par worker** (36 Mo) et chaque sortie serait écrite 896 fois :
le déséquilibre est structurel, pas une question de précision. La tête est donc
calculée par **produits scalaires entiers sur les lignes Q8_0 d'origine**, parallélisés
par tranches de vocabulaire — pas de dispersion, pas de réduction. Coût : 10 ms sur
100, soit 10 % du token.

*(Le reste du modèle — 99,7 % des poids — passe par les événements.)*

### Les activations sont quantifiées

Une échelle par vecteur, 32767 niveaux par défaut. C'est **ce qui décide de la
fidélité** :

| activation | événements/token | accord avec la référence | tok/s |
|---|---|---|---|
| int8 (127 niveaux) | 299 M | 3 tokens sur 6 — les courses serrées basculent | 10,3 |
| **int16 (32 767 niveaux)** | 353 M | **16 sur 16** | 10,0 |

Int8 coûte 0,3 % sur 4 % d'écart de logits, ce qui suffit à faire basculer un argmax
quand deux tokens sont à 0,26 de logit (cas observé). Int16 ne coûte que 4 % de débit
et reproduit la référence : **c'est le réglage par défaut**.

## 5. Le tokenizer : mon portage Python était faux

Le tokenizer Rust livré implémente le **vrai motif Qwen2**, vérifié contre un moteur
d'expression régulière Perl exécutant le motif exact : **737 cas sur 737**, plus
13 468 cas de fuzz sans divergence.

Mon portage Python précédent (`src/bpe_np.py`, utilisé par le harnais de perplexité)
s'en écarte sur **5 points** :

| Point | Cas | Exemple : `bpe_np.py` → Qwen2 |
|---|---|---|
| ` ?[^\W\d_]+` au lieu de `[^\r\n\p{L}\p{N}]?\p{L}+` | 17 | `Musicnotes.com` : `. com` → `.com` |
| ` ?[^\s\w]+` sans `[\r\n]*` | 10 | `end.\n` : `13 198` → `624` |
| `\s*[\r\n]+` absente | 5 | `a\n\nb` : `198 198` → `271` |
| `(?i:)` absent | 4 | `we'D` : `6 35` → `27705` |
| `findall` saute `_` | 2 | `_` : *(vide)* → `62` |

Conséquence : les identifiants produits diffèrent dans **5,2 % des cas** (38 sur 737).
Cela **n'invalide pas** la comparaison de perplexité ci-dessus — numpy et Rust ont
consommé exactement la même suite d'identifiants — mais la valeur absolue publiée
précédemment (20,29) a été calculée avec le tokenizer approximatif et devra être
reprise.

## 6. Ce que ça démontre, et ce que ça ne démontre pas

**Démontré :**
1. L'architecture « listes d'événements » **exécute un vrai LLM**, à qualité égale
   (perplexité à 0,4 %, 16 tokens identiques sur 16), en arithmétique entière.
2. Elle tient dans **2 300 lignes de Rust sans aucune dépendance** — pas de BLAS, pas
   de framework, pas de GPU.
3. Le débit est **entièrement déterminé par le nombre d'événements** : 3,9 G év/s,
   soit exactement la cadence mesurée du moteur au microbanc.
4. Elle est **30 % plus rapide que numpy + OpenBLAS** sur le même modèle, sur le même
   CPU, avec 20 threads au lieu de 40.

**Non démontré :**
1. **Le débit variable reste hors d'atteinte** : 352 M événements par token, tous les
   tokens, parce que les activations d'un LLM dense ne sont jamais nulles. Le mode
   événementiel ne paiera que sur des modèles à activations **creuses par
   construction** (seuil, top-k, ReLU, MoE, ou graphes).
2. **Aucun avantage de cadence brute** : 3,9 G événements/s sur 20 cœurs ≈ 1 événement
   par cycle et par cœur. Un banc FPGA à 124 MHz × 32 PEs vise la même cadence.
3. La **mémoire** est le prix du format : 0,71 Go de listes pour 494 M de poids, soit
   1,44 octet par poids — contre 1,06 pour Q8_0 dense. À 99 % de densité, les listes
   coûtent 36 % de mémoire en plus et n'économisent rien.

## 7. Le gain le moins cher : la liste des destinations touchées

Le moteur lisait 706 Mo par token en 95 ms, soit **7,4 Go/s sur les 28,7 Go/s
mesurés de la machine** : il n'était donc pas borné par la mémoire, mais par le
nombre de cycles par événement (13,7). Chercher ce qui restait a donné le gain le
plus rentable du projet.

**La cause** : pour ne vider que les destinations réellement écrites,
l'accumulateur tenait une **liste des destinations touchées**, alimentée à chaque
événement — soit une comparaison, une écriture et une mise à jour de longueur,
environ six micro-opérations **par événement**. Or vider l'accumulateur entier
par fenêtre coûte… 0,2 % du temps de token.

| Version | tok/s | matvec+MLP |
|---|---|---|
| liste des destinations touchées | 10,96 | 92,2 ms |
| + accumulateur i32 | 11,38 | 92,2 ms |
| **sans la liste (borne haute cumulative)** | **14,74** | **69,4 ms** |

➡️ **+35 %**, perplexité **identique au chiffre près** (24,8995) et tokens
identiques. Le débit par événement passe de 3,6 à **5,3 G év/s**.

**Deux bugs révélés par la suppression**, tous deux trouvés par les bancs :

1. Les chemins fusion et 2-listes écrivent dans un accumulateur i64 tandis que
   le mode push utilise un i32 ; la réduction lisait toujours le second. Le banc
   signalait « DIVERGENT au rang 0 : 0 vs 3513 » — la réduction d'un
   accumulateur jamais écrit.
2. Remettre à zéro la seule fenêtre du travail précédent ne suffit pas : **si
   elle rétrécit**, des valeurs plus anciennes survivent au-delà. D'où une
   **borne haute cumulative** par worker, remise à zéro seulement lors d'un
   changement de largeur. C'est ce que le banc signalait au rang 895.

**Ce qui reste sur la table** : 10,4 Go/s utilisés sur 28,7 → **2,8× avant
d'être borné par la mémoire**. Mais attention au sens de la comparaison : à
14,8 tok/s le moteur d'événements est maintenant **plus rapide que le noyau dense
int8** (11,4 tok/s) sur la même machine.

## 8. Le 4 bits ne paie pas — et pourquoi

*Réponse mesurée à la question « est-ce que ça permet de faire tourner des modèles
4 bits efficacement sur CPU ? »*

Le même moteur, le même code, deux modèles du même réseau :

| | Q8_0 | Q4_0/Q4_1 | écart |
|---|---|---|---|
| Fichier GGUF | 506 Mo | 337 Mo | **−33 %** |
| Listes en mémoire | 0,71 Go | 0,63 Go | **−11 %** |
| Événements par token | 352,7 M | 312,5 M | −12 % |
| RSS | 1,27 Go | 1,02 Go | −20 % |
| Débit | 10,33 tok/s | 11,78 tok/s | +14 % |
| **Perplexité WikiText-2** | **24,90** | **27,83** | **+12 %** |

➡️ **Non.** Le fichier perd un tiers de sa taille, mais notre représentation n'en
gagne que 11 % : chaque événement coûte `varint(écart) + i8(valeur)`, soit ~2 octets,
**quelle que soit la précision de la source**. Le 4 bits est élargi à 8 bits au
chargement. Et la vitesse suit le *nombre d'événements*, pas le nombre de bits :
−12 % d'événements, +14 % de débit. On échange 12 % de perplexité contre 11 % de
mémoire — un mauvais marché.

*(Même en empaquetant idéalement la valeur sur 4 bits, on serait à 1,5 octet par
événement contre 0,56 octet par poids en Q4 dense : le format liste reste 2,7× plus
gros, parce qu'à 99 % de densité chaque poids a besoin de son octet d'écart.)*

### Le vrai résultat : le coût d'un événement n'est pas constant

En élaguant par magnitude (le levier qui, lui, réduit réellement le nombre
d'événements) :

| poids gardés | événements/token | tok/s | débit par événement |
|---|---|---|---|
| 100 % | 352,7 M | 10,33 | 3,56 G év/s |
| 50 % | 178,6 M | 12,17 | 2,28 G év/s |
| 25 % | 89,5 M | 15,64 | 1,43 G év/s |
| 10 % | 35,6 M | 21,40 | 0,88 G év/s |

**10× moins d'événements ne donnent que 2× de vitesse.** Le débit par événement
s'effondre quand la matrice s'éclaircit. Deux causes identifiées :

**1. La localité du accumulateur.** À pleine densité, 8 événements consécutifs
tombent dans la même ligne de cache : une seule transaction mémoire pour huit. À
10 %, chaque événement touche une ligne différente. L'élagage par magnitude disperse
les poids ; un élagage **contigu** (fenêtre de destinations par source, la forme que
produiraient des grappes efférentes) est **30 % plus rapide à taux égal** :

| élagage à 25 % | événements | matvec | tok/s |
|---|---|---|---|
| dispersé (magnitude) | 89,5 M | 66,1 ms | 13,77 |
| **contigu (fenêtre)** | 85,8 M | **50,1 ms** | **17,91** |

**2. La taille de l'accumulateur — et c'est le résultat le plus important.** Chaque
worker tient un accumulateur de `n_out` entiers de 64 bits (39 Ko pour une matrice
4864 × 896). En densité pleine, l'accès est séquentiel et le préchargeur masque tout.
En densité faible, il est dispersé et chaque worker promène son propre accumulateur :

| threads | 4 | 8 | 16 | 32 |
|---|---|---|---|---|
| matvec, 100 % de poids | 186,6 ms | 120,6 ms | 99,1 ms | **90,4 ms** |
| matvec, 10 % de poids | **31,3 ms** | 35,7 ms | 40,6 ms | 52,9 ms ❌ |

➡️ **Sur des événements épars, ajouter des threads *ralentit*.** À 32 workers il faut
1,2 Mo d'accumulateurs, qui débordent le cache L2 de chaque cœur : chaque écriture
devient un accès L3. Le mode événementiel n'est parallélisable que si l'accumulateur
par worker tient dans son cache.

**Conséquence pour la carte :** le dimensionnement de l'accumulateur sur puce n'est
pas un détail d'implémentation, c'est le paramètre qui décide du débit en régime
creux. Il plaide pour un **tuilage de la dimension de sortie** (traiter 512–1024
destinations à la fois) plutôt qu'un accumulateur large par PE.

## 9. Reproductible

```bash
cd qtrinet-core && cargo build --release     # 0 avertissement

# génération de texte (gabarit de chat Qwen2.5)
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --chat --prompt "Explain in one sentence why the sky is blue." \
    --n 60 --threads 16 --abits 16

# perplexité sur une suite d'identifiants
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --ppl /tmp/wt2_ids.txt --ctx 256 --abits 16 --threads 16

# comparaison avec un noyau dense int8 (mêmes poids, mêmes activations)
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --ids 9707,0 --n 16 --threads 16 --abits 16 --dense

# modèle 4 bits (le fichier est mixte Q4_0/Q4_1) et élagage
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q4_0.gguf \
    --infer --ids 9707,0 --n 16 --threads 16 --abits 16
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --ids 9707,0 --n 16 --threads 16 --keep 0.25    # dispersé
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --ids 9707,0 --n 16 --threads 16 --keep -0.25   # contigu
```

Exemple de sortie (le modèle tourne réellement sur le CPU de cette machine) :

```
<|im_start|>user
Give the first five prime numbers, separated by commas.<|im_end|>
<|im_start|>assistant
3, 5, 7, 11, 13<|im_end|>
```

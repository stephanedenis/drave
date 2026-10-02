# Engram de DeepSeek-V4.1 : ce qui est établi, ce qui manque, et pourquoi on s'arrête là

**En une ligne** : les deux tables d'engram sont **entièrement décrites** (101,38
Go chacune, 264 octets par rangée), et **une référence existe** — un portage 1:1
de `vllm/models/deepseek_v4_1/common/engram.py` dans
[`mudler/vllm.cpp`](https://github.com/mudler/vllm.cpp/blob/main/src/vllm/model_executor/models/deepseek_v4_1_engram.cpp)
— ce qui **rouvre la phase** : la formule n'est plus à deviner, elle est à
retrouver.

> **Correction d'une conclusion antérieure.** Ce rapport concluait à l'issue (b)
> du plan (« pas de référence, ne pas implémenter »). La recherche de sources l'a
> démenti : la référence existe, et une première vérification a déjà été faite
> contre elle (voir §2). Le plan prévoyait exactement cette issue (a) : écrire une
> référence indépendante et la faire concorder.

## 1. Ce qui est établi (et vérifiable)

| fait | valeur | source |
|---|---|---|
| tenseurs | `blk.1.engram_embd` **I8 [384006168, 264]** et `blk.14.engram_embd` **I8 [384016682, 264]** | `--tensors` |
| taille | 384 006 168 × 264 = **101,378 Go** · 384 016 682 × 264 = **101,380 Go** | arithmétique, recoupée par l'inventaire |
| format de rangée | `engram.encoding = e4m3_e8m0_32_row264` → **8 blocs de 32 valeurs e4m3** (256) **+ 8 échelles e8m0** = **264 octets** | métadonnées + forme du tenseur |
| par couche | `engram_q_norm`, `engram_k_norm` **[4, 5120]** (4 = taille maximale du n-gramme) · `engram_kv` **[25600, 6144]** | `--tensors` |
| hachage | `engram.primes` : **48 nombres premiers** ≈ 16 000 057 · `engram.multipliers` : **8 entiers 64 bits** | métadonnées |
| vocabulaire | `engram.token_map` : **129 280 entrées** (une par jeton) · `compressed_vocab_size = 99 092` · `pad_id = 2` | métadonnées |
| couches | `engram.layer_ids = [1, 14]` · `engram_max_ngram_size = 4` · `engram_n_heads = 8` · `engram_head_dim = 256` | `deepseek41.config` |
| sonde | `--sonder-engram 10000` : **219 à 524 ms**, **2,6 Mo touchés** par table, **120 Mo de RSS** pour 365,7 Go | `reports/rapport-execution-v41.md` |

Les deux tables pèsent **202,8 Go** à elles seules : c'est 55 % du fichier de
365,7 Go, et de loin le plus gros poste du modèle.

## 1.bis Ce que la référence a déjà confirmé (vérifié, pas supposé)

Le portage de `engram.py` donne la recette **et** les invariants. Trois d'entre
eux se vérifient **sans charger le modèle**, à partir des seules métadonnées :

| invariant de la référence | vérification sur le fichier | résultat |
|---|---|---|
| les 48 premiers sont les suivants de `engram_vocab_size - 1`, pris dans l'ordre (couche × groupe × tête) et **jamais réutilisés** — via un Miller-Rabin (2, 7, 61) qui **reproduit le défaut d'origine** (`_is_prime(61) == False`) | recalcul complet de l'algorithme sur `vocab = 16 000 000`, `max_ngram = 4`, `n_heads = 8`, 2 couches | **48 premiers IDENTIQUES** à ceux du fichier |
| `build_compressed_token_map` émet des identifiants **denses** `[0, compressed_vocab_size)` | `max(token_map) + 1 = 99 092` et `set(token_map) == range(99 092)` | **dense et exact** (99 092 = `compressed_vocab_size`) |
| les multiplicateurs sont **impairs**, un par (couche, recul), sous la borne `max_int64 / compressed_vocab_size / 2` | 8 multiplicateurs, tous impairs, tous sous la borne | **conformes** |

La structure du fichier et la référence disent donc la même chose — ce qui est
déjà une porte : les métadonnées ne sont pas décoratives, elles **déterminent**
l'adressage.

## 2. Ce qui reste à faire : la formule, maintenant écrite

La formule, telle que la référence la donne (`NgramHashState::Forward`,
`engram.py:248-380`) :

```
pour chaque jeton, position p, couche l :
  rolling[l] = 0
  pour shift de 0 à max_ngram-1 :
      lookback = p - shift
      source = id compressé du jeton (ou pad / dead / fenêtre de recul)
      blocked = blocked || lookback < 0 || source == dead     # COLLANT
      valeur  = blocked ? pad_id : source
      rolling[l] ^= valeur * multiplier[l][shift]
      si shift > 0 :
          pour chaque tête h :
              col = (shift-1)*n_heads + h
              rangée = rolling[l] % prime[l][col] + offset[l][col]
```

Trois détails portent tout le comportement, et aucun n'est devinable :

1. **`^=` et non `+`** : le repli est un OU exclusif, pas une somme ;
2. **`blocked` est collant** : dès qu'un n-gramme est cassé (début de séquence,
   jeton mort), **tous les reculs plus profonds** sont remplacés par le pad — sans
   quoi un 4-gramme à cheval sur une image hacherait comme si l'image n'existait
   pas ;
3. le modulo se fait **par colonne** (prime et offset propres à chaque
   (couche, groupe, tête)), pas sur la table entière.

S'y ajoutent la lecture (e4m3 × échelle e8m0 par bloc de 32, sortie bf16) et
l'injection (une porte `sigmoid(±sqrt(max(|dot|, 1e-6)))` — le clamp est **dans**
la racine et c'est un **maximum**, donc un produit scalaire minuscule est
*amplifié* — multipliée par une valeur partagée entre les `hc` copies).

La suite de P8 est donc bornée : porter ces trois fonctions, les faire concorder
avec la référence sur les 10 000 entrées de la sonde, et **annoncer** le
changement de sortie.

## 2.bis Ce que le moteur sait faire maintenant (et ce qui le prouve)

| pièce | état | preuve |
|---|---|---|
| **adressage** (`^=` sur un repli collant, modulo par colonne) | **porté** | 10 000 jetons × 2 couches × 24 colonnes = **480 000 adresses, 0 écart** avec `tools/engram_reference.py`, sur les métadonnées **réelles** de V4.1 |
| invariants du fichier | **vérifiés** | les 48 premiers recalculés sont identiques ; table de correspondance dense (99 092) ; 8 multiplicateurs impairs sous la borne ; chaque adresse tombe dans le seau de sa colonne |
| **lecture d'une rangée** (e4m3 × e8m0 par bloc de 32) | **portée** | 2 000 rangées lues → **512 000 valeurs, identiques au bit près** au décodage Python des mêmes octets |
| **injection** (porte `sigmoid(±sqrt(max(|dot|, 1e-6)))`, valeur partagée entre les `hc` copies) | **portée** | deux tests : conformité à la transcription Python (valeurs générées) et masque qui éteint la porte en rendant l'entrée **exactement** |

Ce que la liste coûte et ce qu'elle dit, mesuré (`--engram-adresses`) : 10 000
jetons en **5,9 ms**, **99,9 % de rangées distinctes**, **0,06 %** des 768 022 850
rangées adressées, et **0 % de recouvrement entre jetons consécutifs** — le
hachage décorrèle, c'est sa raison d'être. Porte permanente ajoutée à
`tools/portes.sh`.

**Ce qui n'est PAS fait, et pourquoi** : l'injection n'est **branchée dans aucune
passe avant**, parce qu'aucun modèle exécutable ne la porte — V4.1 est le seul à
avoir un engram, et il reste refusé pour deux raisons indépendantes (compression
de ratio 2 sans référence, réduction des `hc` copies non spécifiée). Le jour où
il tournera, l'engram **changera la sortie** : c'est écrit ici, et ce sera écrit
à l'ouverture.

## 3. Ce qui n'est pas encore fait

- **Brancher** l'injection dans une passe avant (bloqué : aucun modèle exécutable
  ne porte d'engram).
- **Un outil d'analyse du flux d'adresses** : la liste est écrite (`--engram-adresses`),
  mais rien ne la relit encore — c'est pourtant le flux le plus intéressant du
  modèle après les candidats de l'indexeur : il dit quels n-grammes le modèle
  consulte, et sa stabilité d'un jeton à l'autre est une question ouverte.

Tant que ce n'est pas fait, la seule chose honnête que le moteur puisse faire de
l'engram est ce qu'il fait : **l'adresser** (`--sonder-engram`), le **compter**
(202,8 Go, 264 octets par rangée) et **le déclarer non calculé**.

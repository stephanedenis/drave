# Engram de DeepSeek-V4.1 : ce qui est établi, ce qui manque, et pourquoi on s'arrête là

**En une ligne** : les deux tables d'engram sont **entièrement décrites** par les
métadonnées et par la forme de leurs tenseurs — 101,38 Go chacune, 264 octets par
rangée — mais la **formule d'adressage n'est nulle part**, et **aucune référence
n'existe** : l'implémenter serait deviner, ce que la règle 6 du plan interdit.

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

## 2. Ce qui manque : la formule

Les métadonnées donnent les **ingrédients** (48 premiers, 8 multiplicateurs, une
table de correspondance de vocabulaire) mais **pas la recette**. Un hachage
modulaire sur les n-grammes est *plausible* — quelque chose comme
`rangée = (Σᵢ token_map[tᵢ] · multiplierᵢ) mod rows` — et c'est exactement le
problème : **plusieurs formules plausibles donnent des rangées différentes**, et
aucune ne se vérifie.

Or il n'existe **aucune référence** :

- `llama.cpp` **ignore l'engram** (il ne le charge ni ne le calcule) ;
- **V4-Flash ne l'a pas** : il n'y a donc pas de modèle plus petit où l'étudier ;
- le dépôt ne contient ni le code d'entraînement de DeepSeek, ni un
  convertisseur qui aurait écrit ces tables.

C'est le cas d'école de la règle 6 du plan : **livrer sans référence violerait la
règle**. Une formule inventée ne se contenterait pas d'être fausse — elle
produirait des injectassions *plausibles*, donc invisibles, dans deux couches sur
quarante.

## 3. La décision : issue (b), écrite

Le plan prévoyait deux issues. C'est la seconde :

> **ne pas le faire, et l'écrire** — ce document.

Ce qui a été fait à la place, et qui a de la valeur : l'engram est **inventorié**
(forme, taille, format de rangée), sa **sonde** est mesurée, et son **absence de
référence** est nommée. `--config` ne le compte pas comme un manque bloquant
(llama.cpp l'ignore : ce n'est pas un obstacle à une comparaison avec lui), mais
`manques_architecture` le dit à l'ouverture — sans quoi un modèle qui tourne
laisserait croire qu'il calcule tout.

## 4. Ce qui débloquerait P8

Par ordre de coût croissant :

1. **le script de conversion** qui a produit ce GGUF, ou son équivalent amont :
   il nomme la formule, même en une ligne ;
2. **une note de spécification** de l'engram (les tables sont adressées par
   n-grammes : la littérature sur les *n-gram embeddings* donne le schéma
   général, pas les 48 premiers de ce modèle) ;
3. **une implémentation amont** (llama.cpp ou un autre moteur) : elle servirait
   alors de porte de correction, et l'engram deviendrait une phase ordinaire —
   référence d'abord, flux ensuite.

Tant qu'aucune des trois n'existe, la seule chose honnête que le moteur puisse
faire de l'engram est ce qu'il fait : **l'adresser** (`--sonder-engram`), le
**compter** (202,8 Go, 264 octets par rangée) et **le déclarer non calculé**.

# Format — le modèle éclaté en clusters (un fichier par cluster)

**En une ligne** : un GGUF est converti en `commun.gguf` + `cluster-XX.gguf`, un
fichier **GGUF autonome par cluster d'experts**, avec un manifeste qui porte la
correspondance ; un nœud n'ouvre que ce qu'il sert — mesuré **3,20 Go au lieu de
18,56** et **625 ms au lieu de 3,9 s** sur Qwen3-30B-A3B.

Outil : [`tools/convertir_clusters.py`](../tools/convertir_clusters.py).

## Le problème

Un MoE publié en GGUF met **tous** les experts d'une couche dans un seul tenseur :

```
blk.0.ffn_gate_exps.weight   [128, 768, 2048]   Q4_K
blk.0.ffn_up_exps.weight     [128, 768, 2048]   Q4_K
blk.0.ffn_down_exps.weight   [128, 2048, 768]   Q6_K
```

Un nœud qui n'héberge que 16 experts sur 128 lit donc 18 Go pour en utiliser un
huitième — et notre mode d'opération lit les poids **en flux à chaque jeton** :
c'est le chemin le plus chaud du moteur.

## Ce que produit le convertisseur

```
modele/
  commun.gguf          embeddings, tête de sortie, attention, normes, ROUTEURS
  cluster-00.gguf      les tranches d'experts du cluster 0, toutes couches
  cluster-01.gguf      …
  cluster-XX.gguf      … (un par cluster, XX numéroté à partir de 00, sans trou)
  mapping.tsv          couche · ligne locale · expert global · cluster
  manifeste.json       rôle de chaque fichier, tenseurs, tailles, ordre des
                       experts (par fréquence), correspondance local ↔ global
```

**`mapping.tsv` est la pièce critique** et elle est en texte, délibérément : le
moteur est en Rust sans dépendance, et un JSON demanderait un parseur de plus à
éprouver. Trois colonnes se relisent à l'œil — ce qui n'est pas un luxe pour la
seule chose qui relie un expert global à sa ligne locale. Le convertisseur
vérifie en l'écrivant que chaque expert global est placé **exactement une fois** ;
le moteur, en le lisant, refuse un doublon.

Trois propriétés, et chacune est vérifiée :

1. **Aucune requantification.** Les octets des poids sont copiés tels quels. Les
   blocs de quantification sont alignés sur l'axe des experts (768 et 2048 sont
   des multiples de 256), donc la tranche d'un expert est une **plage d'octets
   exacte** — le convertisseur le vérifie (`par_expert * ne == octets`) et
   s'arrête si ce n'est pas le cas.
2. **Chaque fichier est un GGUF valide et cohérent.** Le champ
   `{arch}.expert_count` est **réécrit** dans chaque cluster (16 et non 128), donc
   un lecteur qui ouvre `cluster-00.gguf` voit un MoE de 16 experts, pas un fichier
   menteur. Le reste des métadonnées (tokenizer compris) voyage à l'identique.
3. **Vérification par empreintes.** `--verifier` relit chaque fichier produit et
   compare le SHA-256 de **chaque** tenseur — pour les clusters, la concaténation
   des tranches dans l'ordre du manifeste — à la tranche correspondante de la
   source. Sur Qwen3-30B-A3B : **1 587 tenseurs, tout concorde**.

## L'ordre des experts : mesuré, pas deviné

Les experts d'un cluster sont pris **par fréquence d'usage décroissante**, lue dans
une trace de routage (`--trace`, produite par `DRAVE_TRACE_EXPERTS`) — et non par
index. C'est ce qui fait que `cluster-00.gguf` est le cluster qu'un nœud veut
garder : sur Qwen3-30B-A3B, ses 16 experts sont `[28, 72, 91, 122, 64, 75, 100,
51, …]` au lieu de `[0, 1, 2, …]`.

Sans trace, l'ordre naturel est utilisé : le format reste correct, il est seulement
moins bien ordonné. Le rapport [`rapport-decoupage-moe.md`](../reports/rapport-decoupage-moe.md)
montre que cette seule mise en ordre divise la ventilation d'un jeton par ~1,8
(3,08 nœuds au lieu de 5,32 à 8 clusters).

## Mesures (Qwen3-30B-A3B-Instruct Q4_K_M, 18,56 Go, 48 couches, 128 experts)

| fichier | en-tête (mmap) | lecture totale | octets |
|---|---|---|---|
| `commun.gguf` | 1,4 ms | 201,6 ms | 1,00 Go |
| `cluster-00.gguf` | 1,8 ms | 423,3 ms | 2,20 Go |
| le modèle entier | 0,9 ms | **3 906,4 ms** | **18,56 Go** |

Un nœud qui sert le cluster 0 charge **3,20 Go au lieu de 18,56 (5,8× moins)** et
**625 ms au lieu de 3,9 s (6,2× plus vite)**. Avec huit nœuds, chacun ne lit que
son cluster ; le surcoût est la duplication des métadonnées (8 × ~4 Mo, soit
0,2 % du modèle).

## Conversion

```bash
# trace de routage (facultative mais recommandée : elle ordonne les experts)
DRAVE_TRACE_EXPERTS=/tmp/routage.txt ./drave-core/target/release/drave <modele.gguf> \
    --ppl <ids.txt> --ctx 2048 --limit 2048 --lot 64 --threads 16

# conversion : un cluster = 16 experts ; --mode couches pour un modèle dense
python3 tools/convertir_clusters.py <modele.gguf> <dossier> \
    --clusters 8 --trace /tmp/routage.txt --verifier
```

`--mode couches` découpe un modèle **dense** en groupes de couches (un fichier par
groupe), ce qui sert au même usage : un nœud ne charge que sa tranche. Mesuré sur
Qwen2.5-0.5B : `commun.gguf` (embeddings + tête) + 4 fichiers de 6 couches,
290 tenseurs vérifiés.

## Le lecteur (fait, sprint 08)

Un dossier qui contient `commun.gguf` **est** un modèle : `drave <dossier> …`,
sans option nouvelle. Le lecteur ouvre le commun puis les clusters, en préfixant
les tenseurs de chaque cluster (`cl0/blk.0.ffn_gate_exps.weight`) — sans quoi les
huit fichiers porteraient huit fois le même nom. `Moe::ou(expert_global)` rend
`(fichier, ligne locale)` et les neuf points de lecture d'experts passent par lui.

Vérifié : **origine 15,2789 · clusters 15,2789** (mêmes 63 jetons, même contexte),
et l'identité des deux lectures tient au chiffre près. L'inventaire annonce
1 587 tenseurs et 18,55 Go, exactement le modèle d'origine.

**La chaîne complète rejouée par les outils du dépôt** : `tools/convertir_clusters.py`
(351,7 s, 1 587 tenseurs vérifiés par SHA-256, *tout concorde*) écrit
`commun.gguf`, les huit clusters et `mapping.tsv` — puis `drave <dossier>` rend
**15,2789**, exactement le modèle d'origine. Aucune étape manuelle entre les deux.

## La table des types ggml

`octets_tensor` doit connaître la taille de chaque type : `nelem()` compte des
**poids**, et un type quantifié range 32 ou 256 poids par bloc. Cette table est
**relevée, pas devinée** — un petit programme lié à `libggml` imprime
`ggml_blck_size` et `ggml_type_size` :

```
 0 f32   1/4     8 q8_0  32/34   16 iq2_xxs 256/66   24 i8   1/1    39 mxfp4 32/17
 1 f16   1/2     9 q8_1  32/36   17 iq2_xs  256/74   29 iq1_m 256/56  40 nvfp4 64/36
 2 q4_0 32/18   10 q2_K 256/84   18 iq3_xxs 256/98   30 bf16  1/2
 3 q4_1 32/20   11 q3_K 256/110  19 iq1_s  256/50   34 tq1_0 256/54
 6 q5_0 32/22   12 q4_K 256/144  20 iq4_nl 32/18    35 tq2_0 256/66
 7 q5_1 32/24   13 q5_K 256/176  21 iq3_s  256/110
                14 q6_K 256/210  22 iq2_s  256/82
                15 q8_K 256/292  23 iq4_xs 256/136
```

Deux fois, un type absent de cette table a rendu un inventaire faux : 8,56 Go
annoncés pour 86,9 Go de fichiers (`iq1_m` manquant), puis 3,19 Go pour 18,55 Go
(préfixes non appliqués). Un type inconnu est donc désormais **signalé** au lieu
d'être compté zéro.

`tools/verifier_table_types.sh` **confronte la table à `libggml` elle-même** : il
compile un petit programme lié à la bibliothèque, imprime `ggml_blck_size` et
`ggml_type_size` pour chaque type, et compare au source Rust. Dernier passage :

```
types confondus : 41 · divergents : 0 · absents du moteur : 0
```

Il liste aussi les types que ggml connaît et que le moteur ignore — c'est ainsi
que les huit types ajoutés après NVFP4 (`Q1_0`, `Q2_0`, `Q6_0`, `Q6_1`, `Q3_0`,
`Q3_1`, `Q2_0S`, `Q2_1`) ont été relevés et ajoutés.

## Ce qui reste

* **Le nœud partiel** : `DRAVE_CLUSTERS=0,3` ne charge que ces clusters — et un
  cluster **demandé mais absent du disque est une erreur**, pas un silence : sans
  cela, un artefact amputé passait pour complet et les contributions manquantes
  disparaissaient sans un mot. Mesuré
  sur Qwen3-30B, mêmes 7 jetons :

  | clusters | perplexité | mémoire |
  |---|---|---|
  | 1 | 268 786,62 | **2,35 Go** |
  | 2 | 63 780,09 | 2,83 Go |
  | 4 | 3 378,91 | 4,60 Go |
  | 8 | **799,8557** | 6,28 Go |

  **Ce qui manque** : la somme des contributions entre nœuds. Le moteur saute
  déjà un expert absent, mais rien n'additionne encore ce que deux nœuds calculent
  chacun de leur côté. Avec elle, deux nœuds à quatre clusters rendraient
  799,8557 pour 4,60 Go chacun — moins que les 6,28 Go d'un nœud complet.
* **Les biais d'experts + clusters** : refusés explicitement. Les indexer par
  l'expert global lirait la mauvaise ligne.
* **Le mmap** : FAIT. `read_to_end` dupliquait le modèle (18,55 Go sur le tas en
  plus du cache de pages) ; les fichiers sont mappés, le noyau lit à la demande.
  Mesuré sur Qwen3-30B en clusters : **9,32 s et 6,35 Go** contre **30,68 s et
  19,20 Go**, perplexité identique. `DRAVE_MMAP=0` revient à la lecture.
* **Le format binaire du manifeste** : JSON convient à quelques kilo-octets ; si le
  nombre de fichiers grandit (un par expert), il faudra un index binaire.
* **Le rééquilibrage par charge** : les clusters sont équilibrés en nombre
  d'experts, pas en nombre d'activations — le nœud qui garde les experts chauds
  travaillera plus.

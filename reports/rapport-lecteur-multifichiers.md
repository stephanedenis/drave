# Rapport — un modèle éclaté se lit comme un seul

Sprint 08 · 11:13 → 13:13 · binaire `drave-core` (release), commit à venir.

## La question

Un modèle trop gros pour un nœud, ou un MoE dont un nœud ne sert qu'un huitième
des experts, doit pouvoir être lu **par morceaux** — sans requantification, sans
recopier les poids, et sans que le moteur ait à savoir que le modèle est découpé.
Le sprint précédent a produit le format (convertisseur, 1 587 tenseurs vérifiés
par SHA-256) ; celui-ci devait le rendre **lisible**, et le prouver.

## Ce qui a été mesuré

### L'épreuve décisive : origine contre clusters

Mêmes jetons, même contexte, même quantification, chemin par jeton. Le modèle
d'origine (18,56 Go, un fichier, sur le disque mécanique) contre le même modèle
éclaté en `commun.gguf` + 8 × `cluster-XX.gguf` (sur le NVMe) :

| | perplexité | temps |
|---|---|---|
| modèle d'origine | **15,2789** | 12,2 s |
| modèle en clusters | **15,2789** | 11,6 s |

**Identiques au chiffre près**, sur 63 jetons. C'est la preuve que la traduction
expert global → (fichier, ligne locale) est juste, et que rien n'est perdu ni
décalé dans l'assemblage.

### Les gros fichiers découpés en shards

DeepSeek-V4-Flash-UD-IQ1_M (86,9 Go, 3 shards), inventaire par les seuls
en-têtes :

| | |
|---|---|
| annoncé par les descripteurs | **86,90 Go** |
| somme des fichiers sur disque | **86,90 Go** |
| tenseurs | 1 328 (shard 1 : 0, shard 2 : 784, shard 3 : 544) |
| temps de lecture des en-têtes | 54 ms (disque au repos) |

La concordance au centième de gigaoctet est la vérification qui compte : elle
prouve à la fois que la table des tailles de types ggml est juste et que les
trois shards sont complets. Un shard manquant est refusé, pas ignoré.

Le shard 1 ne porte **aucun tenseur** — seulement les métadonnées (architecture,
tokenizer). Le lecteur prend les métadonnées du premier fichier qui en porte, ce
qui couvre ce cas sans le traiter à part.

### Le format en clusters, inventorié

| | |
|---|---|
| fichiers | 9 (commun + 8 clusters) |
| tenseurs | **1 587** = le compte de la conversion |
| poids | **18,55 Go** = le modèle d'origine |
| chargement complet du modèle | 48 couches en 27,8 s |
| mélanges d'experts chargés | **48/48 couches** |

### Portes de régression

| porte | attendu | obtenu |
|---|---|---|
| Qwen2.5-0.5B ctx 256 `--dense` | 19,3885 | **19,3885** |
| gpt-oss-120b ctx 256 (binaire final, mmap) | 15,1757 | **15,1757** |
| `cargo test --release` | vert | **32 verts** (20 au début du sprint) |
| modèle en clusters | 15,2789 | **15,2789** |
| nœud partiel (cluster 0 seul) | 268 786,6218 | **268 786,6218** |

## Les défauts trouvés

### 1. `q8_dot_at` lisait 34 octets trop tôt — perplexité NaN

Le refactor a changé la signification de `Q8View.base` : offset **global**
(`data_start + offset`) devenu offset **local au fichier**. Deux sites
(`q8_dot_at`, `q8_dot_avx2`) faisaient `&self.bufs[v.fichier]` au lieu de
`&self.bufs[v.fichier][self.starts[v.fichier]..]` : le tenseur était lu dans
l'en-tête du fichier.

La perplexité Qwen est passée à **NaN**, et **aucun test ne l'a vu**. Le test
`avx2_egale_scalaire` compare deux chemins qui partageaient l'erreur ; le test
multi-fichiers passe par `dequant()`, qui n'emprunte pas cette route.

Corrigé, puis le test manquant a été écrit :
`q8_dot_at_voit_les_bons_octets` fabrique un GGUF Q8_0 synthétique dont les
produits scalaires se calculent à la main. **Vérifié par sabotage** — offset
retiré, le test rougit (`ligne 0 : 2181034 au lieu de 271`) ; remis, il verdit.

### 2. L'inventaire sans poids ignorait les préfixes

`open_multi_meta` n'appliquait pas les préfixes : les huit clusters portaient les
mêmes noms, et sept disparaissaient par déduplication. Symptôme : **3,19 Go
annoncés pour 18,55**.

### 3. Le nom des tenseurs d'experts était préfixé deux fois

`vues()` applique déjà `blk.{l}.` ; les appels lui passaient `p("ffn_gate_exps.weight")`,
soit `blk.0.blk.0.ffn_gate_exps.weight`. Résultat : `charger_moe` rendait `None`
pour **les 48 couches**, sans un mot, et le moteur tombait dans le chemin FFN
dense — qui paniquait cent lignes plus loin sur « projection dense requise »,
un message qui ne dit pas pourquoi.

Ce défaut a été trouvé en **rendant le silence visible** : un message par refus
dans `charger_moe`, et un compteur `mélanges d'experts chargés : 0/48` au
chargement. Le message a nommé la faute immédiatement.

### 4. Deux défauts relevés par la revue adverse

- **Le tri des clusters était lexicographique.** `cluster-100.gguf` se range
  avant `cluster-20.gguf`, alors que les préfixes `cl{c}/` sont attribués par
  **position**. Au-delà de 99 clusters, chaque expert aurait été lu dans le
  mauvais fichier — mêmes formes, donc aucune erreur, juste un résultat faux. Le
  numéro est maintenant lu et la numérotation exigée continue à partir de 0.
- **Le mapping était publié avant l'ouverture.** Un dossier refusé laissait
  derrière lui le mapping d'un autre modèle. Il n'est plus publié qu'après une
  ouverture réussie. C'est un test qui l'a montré, pas une relecture.

### 5. Un type ggml inconnu comptait zéro octet, en silence

Même mécanisme que l'incident `iq1_m` (8,56 Go annoncés pour 86,9). Les types 41
et 42, ajoutés à ggml, y tombaient. Un type hors table est désormais signalé.

### 6. Le nœud partiel pouvait perdre des experts sans le dire (revue adverse)

Défaut **bloquant et silencieux**, trouvé par la revue déléguée : `DRAVE_CLUSTERS`
listant tous les clusters annoncés sur un dossier amputé chargeait ce qui
restait, et les contributions des experts absents disparaissaient — sans erreur,
sans renormalisation, sans un mot. Un cluster **demandé mais absent du disque**
est maintenant une erreur, et un dossier incomplet n'est accepté que s'il est
assumé.

Trois autres défauts de la même revue : `octets_de` ne bornait pas le *début* de
la tranche (un décalage aberrant paniquait au lieu de se dire) ; le contrôle de
continuité des numéros empêchait un nœud de ne **posséder** que ses fichiers
(seul le disque, pas la mémoire, était découpé) ; et rien ne vérifiait que le
mapping décrivait le même modèle que les métadonnées.

### 7. Le correctif du nœud partiel n'avait aucun test

Le plus instructif. Remplacer la traduction par numéro de cluster
(`numeros.position(...)`) par le bug d'origine (`Some((cluster, ligne))`)
laissait **les trente tests verts** : sur un nœud complet, le numéro et le rang
coïncident. Il fallait un nœud partiel dont le cluster chargé n'est pas le rang 0.

Le blocage était que `gguf_synth` ne fabriquait que du F32, type que `source_de`
refuse — donc **aucun `Moe` n'était constructible en test**. Un générateur Q4_0 a
levé l'obstacle, et deux tests couvrent désormais le chemin. **Vérifiés par
sabotage** : le bug d'origine les fait rougir.

*Leçon : quand un correctif ne peut pas être testé, la question n'est pas
« comment écrire le test ? » mais « qu'est-ce qui manque pour le rendre
testable ? ». Ici, c'était un générateur de fichiers.*

### Les modèles lourds, inventoriés par les en-têtes

`tools/inventaire_modeles_lourds.sh` confronte les poids annoncés par les
descripteurs GGUF aux tailles annoncées par HuggingFace. **La concordance porte
sur 984 Go** : DeepSeek-V4.1-Flash 365,70 = 365,7 · GLM-5.3 216,71 = 216,7 ·
Kimi-K2.7 303,90 = 303,9 · DeepSeek-V4-Flash 86,90 = 86,9. Une seule entrée
fausse dans la table des types ggml donnerait un écart visible sur des centaines
de gigaoctets — c'est ainsi que `iq1_m` manquant avait fait annoncer 8,56 Go pour
86,9 Go.

Les architectures sont lues (`deepseek41`, `deepseek2`, `deepseek4`, `glm-dsa`) ;
aucune n'a encore de `forward`. Kimi est en huit fichiers, GLM en six : le lecteur
les rassemble à partir d'un seul chemin.

### Le mmap : 3,3× plus rapide, 3× moins de mémoire

`read_to_end` lisait tout le fichier et en gardait une copie dans le tas, **en
plus** du cache de pages du noyau — deux fois la taille du modèle en mémoire
physique. Les fichiers sont maintenant **mappés** (le noyau lit les pages à la
demande). Sur Qwen3-30B-A3B en clusters, mêmes 7 jetons, perplexité identique
(799,8557 dans les deux cas) :

| | chargement + passe | mémoire maximale (RSS) |
|---|---|---|
| mappé (défaut) | **9,32 s** | **6,35 Go** |
| lu en entier (`DRAVE_MMAP=0`) | 30,68 s | 19,20 Go |

Les 19,20 Go sont exactement la taille du modèle : la copie complète. Le mappé
n'en touche que 6,35 Go — les pages réellement lues. Un modèle dont on
n'utiliserait qu'un huitième des experts ne lirait qu'un huitième des octets.

Portes revérifiées dans les deux modes : Qwen2.5-0.5B ctx 256 = **19,3885** avec
et sans mmap.

### Le nœud partiel : un huitième des experts pour un huitième de la mémoire

`DRAVE_CLUSTERS=0` ne fait charger que `commun.gguf` + `cluster-00.gguf`. Le
moteur saute les experts absents (`Moe::ou` rend `None`) : le résultat est
**volontairement dégradé**, puisqu'il manque les contributions des autres nœuds.
Ce que la mesure montre, c'est le coût d'un nœud et la décroissance de l'erreur
quand on ajoute des clusters :

| clusters chargés | perplexité (7 jetons) | mémoire maximale | chargement + passe |
|---|---|---|---|
| 1 | 268 786,62 | **2,35 Go** | 9,64 s |
| 2 | 63 780,09 | 2,83 Go | 9,33 s |
| 4 | 3 378,91 | 4,60 Go | 10,27 s |
| **8** | **799,8557** | 6,28 Go | 10,65 s |

La perplexité décroît de façon monotone et la mémoire suit — **2,7× moins pour un
nœud à un cluster que pour le modèle entier**. C'est le compromis que le format
achète, et c'est aussi ce qui manque : la somme des contributions entre nœuds.
Deux nœuds à quatre clusters rendraient 799,8557 pour 4,60 Go chacun, soit moins
que les 6,28 Go d'un nœud complet.

La mémoire d'un nœud à un cluster est **2,7× moindre** que celle du modèle
entier. C'est la mesure qui justifie le format — et elle montre aussi, par la
décroissance, que ce qui manque n'est pas un bug mais bien la somme des
contributions entre nœuds, qui reste à écrire.

Au passage, cette manipulation a **confirmé en vrai un défaut prédit par la revue
adverse** : l'identifiant de cluster du mapping servait d'index direct dans le
`Vec` des vues. Tant que les huit clusters étaient chargés, les deux coïncidaient
et rien ne se voyait ; avec un seul cluster, le moteur est sorti du tableau
(`index out of bounds: the len is 1 but the index is 6`). Les vues portent
maintenant leur numéro, et `Moe::ou` le cherche au lieu de le supposer.

## Méthode

Trois fois dans ce sprint, la correction est venue d'avoir **rendu visible** ce
qui était silencieux : un message par refus de `charger_moe`, un compteur au
chargement, un avertissement sur un type inconnu. Les trois défauts les plus
coûteux étaient des `return None` et des `continue` — du code qui a raison
localement et tort globalement.

Et une fois de plus : **le test qui compare deux chemins ne prouve rien s'ils
partagent leur origine**. Le NaN est passé sous 24 tests verts. Le seul test qui
pouvait l'attraper confronte le chemin à une valeur calculée à la main.

## Ce qui n'est pas fait

- Le **nœud partiel** : charger un seul cluster et sommer les experts entre
  nœuds. Le moteur sait déjà sauter un expert absent ; rien ne somme encore.
- Le **chemin par lots** sur les MoE : il fonctionne. `--lot 64` rend 15,2736
  contre 15,2789 par jeton — l'écart connu entre les deux ordres de sommation.
  La panique observée venait du double préfixe décrit plus haut, donc bien de ce
  sprint, et non d'un défaut antérieur.
- Le **mmap** : `read_to_end` charge tout le fichier. DeepSeek-V4.1-Flash fait
  366 Go, il restera hors de portée sans lui.
- Les **biais d'experts** en clusters : refusés explicitement.

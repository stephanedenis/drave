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
| `cargo test --release` | vert | **29 verts** (20 au début du sprint) |
| gpt-oss-120b ctx 256 | 15,1757 | en cours (binaire figé) |

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
- Le **chemin par lots** sur les MoE : `--lot 64` sur Qwen3-30B-A3B panique
  (`wdown.d` est vide pour un MoE et le code y arrive quand même). Défaut
  **préexistant**, sans rapport avec les clusters.
- Le **mmap** : `read_to_end` charge tout le fichier. DeepSeek-V4.1-Flash fait
  366 Go, il restera hors de portée sans lui.
- Les **biais d'experts** en clusters : refusés explicitement.

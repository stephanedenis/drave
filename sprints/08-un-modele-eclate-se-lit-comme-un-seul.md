# Sprint 08 — Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters

- **Début** : 11:13 · **Fin** : 13:13 (boxing de 120 min)
- **Objectif** : un modèle éclaté en plusieurs fichiers (shards d'un GGUF découpé,
  ou notre format en clusters) doit s'ouvrir avec **la même commande** qu'un
  modèle ordinaire, et rendre **le même résultat**.
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Ce qui a été fait

### 1. Le lecteur ne connaissait qu'un fichier

`Gguf` portait `buf: Vec<u8>` et `data_start: usize` : un seul tampon, un seul
début de données. Un tenseur était donc `data_start + offset`, et rien ne
permettait de dire « ce tenseur vit dans l'autre fichier ».

Refonte : `bufs: Vec<Vec<u8>>` et `starts: Vec<usize>`, plus un champ `fichier`
sur chaque `TensorInfo`. Tous les accès aux poids passent par **un seul point**,
`tbuf(&t)` — c'est ce qui a permis de changer la représentation sans dupliquer
les quinze routines de déquantification.

Trois constructeurs nouveaux :

| fonction | ce qu'elle ouvre |
|---|---|
| `open_multi` | N fichiers, métadonnées du premier qui en porte, doublons refusés s'ils divergent |
| `open_avec_prefixes` | idem, en préfixant les noms (`cl0/`, `cl1/`…) |
| `open_multi_meta` / `open_meta_avec_prefixes` | idem **sans lire les poids** |

Et une détection automatique : `shard_de("…-00002-of-00003.gguf")` reconnaît un
nom de shard, `chemins_du_modele` rassemble les morceaux, `open_auto` aiguille.
Un shard manquant est une **erreur**, pas un silence : sinon des tenseurs
seraient absents et le moteur paniquerait bien plus loin, sur un message qui ne
dirait pas pourquoi.

### 2. Un dossier est un modèle

`open_auto` accepte désormais un **répertoire** qui contient `commun.gguf` : il
l'ouvre au format clusters, publie le mapping, et tout le reste du moteur ne
sait même pas que le modèle est découpé.

### 3. Le mapping global ↔ local, et sa traduction

`clusters.rs` lit `mapping.tsv` (trois colonnes : couche, ligne locale, expert
global) et refuse un expert placé deux fois. `Moe` porte `Vec<Vue4>` — une vue
par fichier porteur — et une méthode `ou(e)` qui rend `(vue, ligne locale)` pour
l'expert **global** `e`. Les neuf points de lecture d'experts (trois par chemin :
GPU, jeton, lot) passent par elle. Un expert absent n'est pas une erreur, c'est
le principe du découpage : la boucle le saute.

Cas refusé **explicitement** : biais d'experts + clusters. Les indexer par
l'expert global lirait la mauvaise ligne ; un résultat faux et silencieux est
pire qu'un arrêt.

## Mesures

| mesure | résultat |
|---|---|
| DeepSeek-V4-Flash, 3 shards, inventaire par les en-têtes | **86,90 Go annoncés = 86,90 Go sur disque** · 1 328 tenseurs · 54 ms |
| répartition réelle | shard 1 : 0 tenseur (métadonnées seules), shard 2 : 784, shard 3 : 544 |
| Qwen3-30B-A3B en clusters, inventaire | 9 fichiers · **1 587 tenseurs · 18,55 Go** = le modèle d'origine |
| chargement du modèle en clusters | 48 couches en **27,8 s**, listes 0,91 Go |
| porte Qwen2.5-0.5B ctx 256 | **19,3885** (inchangée) |
| `cargo test --release` | **24 verts** (20 → 24) |

## Les deux défauts trouvés, et comment

### a) `q8_dot_at` lisait au début du fichier — perplexité NaN

Le refactor a transformé `Q8View.base` d'un offset **global** (`data_start +
offset`) en un offset **local au fichier**. Deux sites (`q8_dot_at` et
`q8_dot_avx2`) faisaient `&self.bufs[v.fichier]` au lieu de
`&self.bufs[v.fichier][self.starts[v.fichier]..]` : le tenseur était lu
34 octets trop tôt, dans l'en-tête.

**La perplexité Qwen est passée à NaN** — et aucun test ne l'a vu. Le test
`avx2_egale_scalaire` compare le chemin AVX2 au chemin scalaire : faux tous les
deux de la même façon, il ne pouvait pas les départager. Le test multi-fichiers
passe par `dequant()`, qui n'emprunte pas cette route.

Correction, puis ajout du test qui manquait : `q8_dot_at_voit_les_bons_octets`
fabrique un GGUF Q8_0 synthétique dont les produits scalaires se calculent à la
main, et compare ligne par ligne. **Vérifié par sabotage** : offset retiré →
`ligne 0 : 2181034 au lieu de 271`, test rouge ; offset remis → vert.

*Leçon, la huitième du même genre : un test qui compare deux chemins ne prouve
rien s'ils partagent leur origine. Il faut confronter le chemin à une vérité
extérieure — ici une valeur calculée à la main.*

### b) L'inventaire sans poids ignorait les préfixes

`open_multi_meta` n'appliquait pas les préfixes : les huit clusters portaient
les mêmes noms de tenseurs, et sept disparaissaient par déduplication. Symptôme
visible : **3,19 Go au lieu de 18,55**. Corrigé en factorisant
`open_meta_avec_prefixes`.

*Leçon : un total qui ne colle pas à la somme des fichiers est un signal, pas un
arrondi. C'est la deuxième fois ce soir que la table des tailles de types ggml
est en cause (la première : 8,56 Go au lieu de 86,9 Go, faute d'`iq1_m`).*

## Ce qui reste ouvert

- **L'épreuve d'exécution du modèle en clusters** (origine contre clusters, mêmes
  jetons) tournait encore à la clôture du boxing. Elle est lancée, son résultat
  sera lu au bloc suivant — **je ne le déclare donc pas acquis**.
- **Le chemin par lots achoppe sur les MoE** : `--lot 64` sur Qwen3-30B-A3B
  panique à `model.rs:2945`, `projection dense requise` (`wdown.d` est vide pour
  un MoE, et le code y arrive quand même). **Défaut préexistant**, sans rapport
  avec les clusters — il se déclenche sur le modèle d'origine aussi.
- `read_to_end` charge tout le fichier : DeepSeek-V4.1-Flash fait 366 Go, il
  faudra `mmap`.
- Le nœud partiel : charger UN cluster et sommer les experts entre nœuds.
- Biais d'experts + clusters (refusé pour l'instant).
- `mapping.tsv` n'est pas encore écrit par le convertisseur ; il a été produit
  depuis le manifeste existant, ce qui a servi de vérification croisée
  (`experts[couche]` du manifeste = concaténation des clusters, accord 1,000).

## Rétrospective (introspection)

Le boxing a été mal calibré : 2 h pour un refactor de représentation **plus** un
format de fichier **plus** une épreuve d'exécution, c'était trop. Le refactor a
mangé 70 % du temps, et c'est l'épreuve — la seule chose qui prouve quelque
chose — qui est restée en suspens. Le prochain boxing de cette taille se découpe :
(1) lecteur multi-fichiers seul, (2) clusters et preuve d'exécution.

Deuxième observation : j'ai lancé la porte gpt-oss **avant** d'avoir fini de
recompiler, puis reconstruit le binaire par-dessus. Le processus tournait sur
l'ancien binaire — pas de dégât ici, mais c'est une façon de mesurer autre chose
que ce qu'on croit mesurer. Les portes longues se lancent sur un binaire **figé
dans /tmp**, comme cela avait déjà été fait pour le banc KV.

Troisième observation, plus encourageante : le point d'accès unique (`tbuf`) a
rendu le refactor possible sans toucher aux routines de calcul. C'est la
deuxième fois cette nuit qu'un bon point d'étranglement paie — la première était
`Moe::ou`.

## Revue adverse (autonome)

Trois attaques retenues :

1. **« Le test multi-fichiers ne prouve pas la traduction d'experts. »** Exact :
   il vérifie la concaténation des tenseurs, pas le mapping. Le mapping n'a
   qu'un test unitaire de lecture. La preuve manquante est l'épreuve
   d'exécution — d'où son statut « en cours » et non « acquise ».
2. **« 27,8 s de chargement, est-ce mieux ? »** Non, c'est **plus lent** que le
   fichier unique annoncé à 3,9 s — mais ce n'était pas la même chose : 3,9 s
   mesurait la lecture des tenseurs d'un cluster (3,20 Go), 27,8 s charge le
   modèle complet (18,55 Go) avec les listes. Les deux chiffres ne se comparent
   pas ; les avoir posés côte à côte dans un rapport aurait été fautif.
3. **« Et si le dossier contenait neuf clusters au lieu de huit ? »** `ouvrir`
   refuse : `clusters.len() != mapping.n_clusters` est une erreur explicite.

## Planning

Bloc suivant, dans l'ordre de valeur :

1. Lire le résultat de l'épreuve origine/clusters et le consigner, quel qu'il soit.
2. Corriger le chemin par lots sur les MoE (le défaut bloque toute mesure de
   perplexité par lots sur les modèles qu'on veut faire tourner).
3. `mmap` : sans lui, DeepSeek-V4.1-Flash (366 Go) restera hors de portée.
4. Le nœud partiel : charger un cluster, sommer entre nœuds.

# Sprint 08 — Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters

- **Début** : 11:13 · **Fin** : 13:13 (boxing de 120 min) · **Close** : 11:50
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
| **épreuve appariée origine contre clusters** | **15,2789 = 15,2789** (mêmes 63 jetons) |
| porte Qwen2.5-0.5B ctx 256 | **19,3885** (inchangée) |
| `cargo test --release` | **32 verts** (20 → 32) |
| mapping produit par le convertisseur | **identique à l'octet près** à celui dérivé du manifeste |
| **mmap** contre lecture complète (7 jetons) | **9,32 s / 6,35 Go** contre 30,68 s / 19,20 Go — perplexité identique (799,8557) |
| **nœud partiel** à un cluster | **2,36 Go** de mémoire (contre 6,33 Go) · perplexité 268 786 → 17 929 → 800 en ajoutant des clusters |

## Les défauts trouvés, et comment

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

### b) Le nom des tenseurs d'experts était préfixé deux fois

`vues()` applique déjà `blk.{l}.` ; les appels lui passaient
`p("ffn_gate_exps.weight")`, soit `blk.0.blk.0.ffn_gate_exps.weight`. Résultat :
`charger_moe` rendait `None` pour **les 48 couches**, sans un mot, et le moteur
tombait dans le chemin FFN dense. Trouvé en **rendant le silence visible** : un
message par refus dans `charger_moe`, et un compteur
`mélanges d'experts chargés : 0/48` au chargement. Le message a nommé la faute
du premier coup (`blk.0.blk.0.…`).

### c) L'inventaire sans poids ignorait les préfixes

`open_multi_meta` n'appliquait pas les préfixes : les huit clusters portaient
les mêmes noms de tenseurs, et sept disparaissaient par déduplication. Symptôme
visible : **3,19 Go au lieu de 18,55**. Corrigé en factorisant
`open_meta_avec_prefixes`.

*Leçon : un total qui ne colle pas à la somme des fichiers est un signal, pas un
arrondi. C'est la deuxième fois ce soir que la table des tailles de types ggml
est en cause (la première : 8,56 Go au lieu de 86,9 Go, faute d'`iq1_m`).*

## Ce qui reste ouvert

- **L'épreuve d'exécution** : ACQUISE, 15,2789 des deux côtés. Le chemin par
  lots achoppait sur les MoE ; l'épreuve a donc été faite par jeton (`--lot 1`).
- **Le chemin par lots sur les MoE** : il FONCTIONNE, et il n'était pas
  préexistant — j'avais écrit le contraire dans une première version de ce
  sprint, avant de le mesurer. `--lot 64` sur le modèle en clusters rend
  **15,2736** contre **15,2789** par jeton (mêmes 63 jetons) : l'écart de
  0,035 % est celui, connu, entre les deux ordres de sommation. La panique
  « projection dense requise » venait entièrement du double préfixe, donc de ce
  sprint.

*Correction d'une affirmation non vérifiée : j'ai d'abord écrit « défaut
préexistant, sans rapport avec les clusters » parce que la panique se produisait
aussi sur le modèle d'origine — ce qui était une déduction, pas une mesure. La
mesure dit l'inverse. Une phrase de moins, un test de plus.*
- `read_to_end` charge tout le fichier : DeepSeek-V4.1-Flash fait 366 Go, il
  faudra `mmap`.
- Le nœud partiel : charger UN cluster et sommer les experts entre nœuds.
- Biais d'experts + clusters (refusé pour l'instant).
- `mapping.tsv` n'est pas encore écrit par le convertisseur ; il a été produit
  depuis le manifeste existant, ce qui a servi de vérification croisée
  (`experts[couche]` du manifeste = concaténation des clusters, accord 1,000).

## Deux chantiers de plus, dans le même boxing

Le sprint a débordé de son objectif initial — le lecteur multi-fichiers — parce
que la preuve d'exécution a ouvert deux questions immédiates.

**Le `mmap`.** `read_to_end` gardait une copie complète du modèle dans le tas,
*en plus* du cache de pages : 19,20 Go de RSS pour un modèle de 18,55 Go. Les
fichiers sont maintenant mappés (le noyau lit les pages à la demande) :
**6,35 Go** et un chargement **3,3× plus rapide**, perplexité identique. C'est ce
qui rendra DeepSeek-V4.1-Flash (366 Go) approchable.

**Le nœud partiel.** `DRAVE_CLUSTERS=0` ne charge que `commun.gguf` et un
cluster : **2,36 Go** contre 6,33 Go, et la perplexité décroît à mesure qu'on
ajoute des clusters (268 786 → 17 929 → 800). Le résultat est volontairement
dégradé — il manque la somme des contributions entre nœuds — mais le coût d'un
nœud est mesuré, et c'est ce qui justifie le format.

Ce chantier a **confirmé en vrai un défaut prédit par la revue adverse** :
l'identifiant de cluster du mapping servait d'index direct dans le `Vec` des
vues. Tant que les huit clusters étaient chargés, les deux coïncidaient et rien
ne se voyait ; avec un seul cluster, le moteur est sorti du tableau
(`index out of bounds: the len is 1 but the index is 6`). Les vues portent
maintenant leur numéro et `Moe::ou` le cherche au lieu de le supposer.

*Leçon : un défaut prédit par relecture et un défaut observé à l'exécution n'ont
pas la même valeur, mais le premier dit où regarder. La revue avait raison sur le
mécanisme et se trompait sur la gravité (« latent ») : il s'est déclenché dans
l'heure.*

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

Une revue déléguée à un sous-agent (lecture seule, ne modifie rien) a rendu huit
réponses avec preuves. Elle a confirmé ce qui est juste — les décalages, la table
des types, `n_expert_global`, les mesures annoncées — et trouvé quatre défauts
réels, tous corrigés dans ce boxing :

- **le tri des clusters était lexicographique** (`cluster-100` avant
  `cluster-20`) alors que les préfixes `cl{c}/` sont attribués par position :
  au-delà de 99 clusters, chaque expert lu dans le mauvais fichier, sans erreur ;
- **le mapping était publié avant l'ouverture** : un dossier refusé laissait le
  mapping d'un autre modèle ;
- **`chemins_du_modele` échouait sur un chemin sans dossier** (`read_dir("")`) ;
- **`meta.as_ref().unwrap()` paniquait** quand le premier fichier n'a pas de
  métadonnées, rendant inatteignable le message d'erreur prévu.

Elle a aussi montré que **le test multi-fichiers ne pouvait pas attraper le NaN**
(il ne fabrique que du F32 et ne passe que par `dequant`) et listé quatre angles
morts. Quatre tests ont été ajoutés en conséquence : préfixes, mode en-tête seul,
détection des shards, dossier de clusters de bout en bout, numérotation, type
inconnu. Le test du dossier de clusters a d'ailleurs **révélé un cinquième
défaut** (publication du mapping avant succès) que la relecture n'avait pas vu.

Ses trois attaques les plus utiles :

1. **« Le test multi-fichiers ne prouve pas la traduction d'experts. »** Exact,
   et c'est ce qui a justifié de ne pas clore le sprint avant d'avoir le chiffre :
   l'épreuve appariée rend 15,2789 des deux côtés. Le test a depuis été complété
   par un dossier de clusters ouvert de bout en bout.
2. **« 27,8 s de chargement, est-ce mieux ? »** Non, c'est **plus lent** que le
   fichier unique annoncé à 3,9 s — mais ce n'était pas la même chose : 3,9 s
   mesurait la lecture des tenseurs d'un cluster (3,20 Go), 27,8 s charge le
   modèle complet (18,55 Go) avec les listes. Les deux chiffres ne se comparent
   pas ; les avoir posés côte à côte dans un rapport aurait été fautif.
3. **« Et si le dossier contenait neuf clusters au lieu de huit ? »** `ouvrir`
   refuse : `clusters.len() != mapping.n_clusters` est une erreur explicite.

## Revue adverse n°2 (mmap, nœud partiel, numeros)

Une seconde revue déléguée a porté sur le mmap, le nœud partiel et la table des
numéros de cluster. Elle a répondu à huit questions et **confirmé l'absence de
fuite, de double `munmap` et de dépassement d'index** — puis trouvé cinq défauts,
tous corrigés dans le boxing :

- **bloquant silencieux** : `DRAVE_CLUSTERS` couvrant tous les clusters annoncés
  sur un dossier amputé chargeait ce qui restait ; les contributions des experts
  absents disparaissaient. Un cluster demandé et absent est désormais une erreur ;
- `octets_de` ne bornait pas le *début* de la tranche ;
- le contrôle de continuité empêchait un nœud de ne **posséder** que ses fichiers
  (seul le disque n'était pas découpé) ;
- aucune vérification que le mapping et les métadonnées décrivent le même modèle ;
- un doublon dans `DRAVE_CLUSTERS` passait sans un mot (cosmétique).

Et son constat le plus utile : **le correctif de `Moe::ou` n'avait aucun test** —
le remettre en cause laissait les trente tests verts. Le blocage était que
`gguf_synth` ne produisait que du F32, refusé par `source_de`, donc aucun `Moe`
n'était constructible en test. Un générateur Q4_0 a levé l'obstacle ; les deux
nouveaux tests sont **vérifiés par sabotage**.

*Ce qui a disparu au passage : deux états globaux du chemin de chargement (le
drapeau `PARTIEL` et la lecture de `ACTIF` par couche). L'exhaustivité se vérifie
à l'ouverture du dossier, où les fichiers sont sous la main ; les couches ne
vérifient que la cohérence entre les trois projections. C'est plus juste, et
c'est aussi ce qui rend le chemin testable.*

## Planning

Bloc suivant, dans l'ordre de valeur :

1. **Le chemin par lots sur les MoE** : établir d'abord s'il est cassé sur le
   modèle d'origine aussi (l'épreuve a dû se rabattre sur `--lot 1`). C'est ce
   défaut qui bloque toute mesure de perplexité rapide sur les modèles qu'on veut
   faire tourner.
2. **Le nœud partiel** : charger UN cluster et sommer les experts entre nœuds.
   `Moe::ou` rend déjà `None` pour un expert absent ; il manque la somme.
3. **`mmap`** : sans lui, DeepSeek-V4.1-Flash (366 Go) restera hors de portée.
4. **Les biais d'experts en clusters** : refusés pour l'instant. gpt-oss en a,
   donc le format ne couvre pas encore ce modèle-là.
5. **Le rééquilibrage par charge** : les clusters sont équilibrés en nombre
   d'experts, pas en nombre d'activations.

## Revue — ce qui est livré, mesuré

Quatre objectifs, dont deux qui n'étaient pas au programme et que la preuve
d'exécution a rendus nécessaires : le **mmap** (3,3× plus rapide, 3× moins de
mémoire) et le **nœud partiel** (2,36 Go pour un huitième des experts).

Livré et mesuré : le lecteur multi-fichiers (shards et clusters) · les clusters
exécutables, 15,2789 = 15,2789 contre l'original · le mmap · le nœud partiel ·
le convertisseur écrit `mapping.tsv` (identique à l'octet près à la référence) ·
les portes Qwen 19,3885 et gpt-oss 15,1757 · 30 tests verts (20 au début).

Durée : 51 min (boxing 120 min). Commits : 4.

  - `6a2dfcb` Journal du bloc : mmap, nœud partiel, et le défaut prédit par la revue confirmé en vrai
  - `b24a2e6` mmap (3,3x plus rapide, 3x moins de mémoire) et nœud partiel (2,36 Go pour un huitième des experts)
  - `8f55e4f` Clusters exécutables : origine 15,2789 = clusters 15,2789, et les défauts trouvés en chemin
  - `3eb0af7` Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters

## Rétrospective — garder / changer

- **Garder** : le **point d'étranglement unique** (`tbuf` pour les octets, `Moe::ou`
  pour les experts). Les deux refactors ont été possibles parce qu'il n'y avait
  qu'un endroit à changer — et `Moe::ou` a ensuite servi de point d'accroche au
  nœud partiel sans toucher aux neuf sites de lecture.
- **Garder** : **rendre le silence visible**. Le défaut le plus coûteux
  (`blk.0.blk.0.…`) a été trouvé en une minute après avoir ajouté un message par
  refus et un compteur au chargement. Avant, `charger_moe` rendait `None` 48 fois
  sans un mot.
- **Changer** : **figer le binaire dans /tmp avant toute mesure longue**. J'ai
  lancé la porte gpt-oss puis recompilé par-dessus ; le processus tournait sur
  l'ancien binaire. Pas de dégât cette fois, mais c'est mesurer autre chose que ce
  qu'on croit.
- **Changer** : **un seul job lourd à la fois**. Trois chargements de 18–63 Go en
  parallèle sur le disque mécanique ont saturé l'I/O et fait croire à des
  blocages. La règle existait ; je ne l'ai pas suivie.
- **Doute** : la table des tailles ggml. Elle est relevée depuis `libggml` et
  confrontée à deux modèles réels, mais rien ne garantit qu'un type ajouté demain
  n'y manquera pas. Le signalement d'un type inconnu est le filet ; il faudrait un
  test qui compare la table à `ggml_type_size` quand llama.cpp est présent.
- **Doute** : la publication du mapping par `OnceLock` est globale au processus.
  Un test qui ouvre deux modèles ne peut pas vérifier la seconde publication — je
  l'ai contourné en testant la valeur rendue plutôt que la valeur publiée. C'est
  honnête mais incomplet.

## Planning — le sprint suivant

| # | chantier | critère de succès |
|---|---|---|
| 1 | La **somme des contributions entre nœuds** : deux nœuds partiels, chacun ses clusters, et la sortie du modèle complet | la perplexité des deux nœuds sommés égale 15,2789 |
| 2 | Les **biais d'experts** en clusters | gpt-oss-120b convertible et exécutable en clusters |
| 3 | Le **rééquilibrage par charge** (activations, pas nombre d'experts) | le nœud le plus chargé porte moins d'activations que le plus léger d'aujourd'hui |
| 4 | Un test qui confronte `octets_tensor` à `ggml_type_size` | la table ne peut plus dériver en silence |

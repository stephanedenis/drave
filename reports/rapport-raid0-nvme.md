# Le raid0 de 4 NVMe en service — débits, QPI, et ce que le moteur n'en voit pas

> Campagne : **machine (stockage)** · expérience 01 — l'array NVMe monté le 12/10
> Question : `docs/configuration-nvme-raid-amd.md` a été écrit **avant** l'intervention (§ 8 :
> « aucune de ces optimisations n'est mesurée sur cette configuration : elle n'existe pas
> encore »). L'array existe depuis le 12/10. **Le pari du § 1 tient-il, et que faut-il en faire ?**
> Verdict : **le pari tient** — 4 NVMe bien sur le **nœud 1**, GPU en **x16**, array à **7,45 Go/s**
> en lecture (8 lecteurs) pour **6-7 Go/s attendus**, **2,86 Go/s** en écriture. Deux réserves du
> § 8 se confirment (**contrôleurs DRAM-less** : à QD1 l'array ne bat pas un NVMe seul) et une
> crainte tombe (**le QPI ne coûte rien** à pleine bande : 7,47 / 7,42 / 7,41 Go/s selon le
> placement). Un écart est trouvé côté moteur : `--materiel` **ne voit pas l'array**.
> Date réelle : 2026-10-12, 15:40-16:45 HAE (heure lue sur la machine)
> Protocole : `~/IA/outils/banc-io.py` (4 motifs × 3 supports, O_DIRECT, erreurs comptées) ·
> `~/IA/outils/banc-numa-raid.py` (3 placements × 3 répétitions entrelacées) ·
> `~/IA/outils/etat-raid.sh` · le moteur : `drave … --materiel`

## 1. Les débits (12/10 15:40, O_DIRECT, 0 erreur)

| support | séq. 1 flux | séq. 8 flux | aléa 4 Kio QD1 | aléa 4 Kio QD8 | aléa 512 o QD1 | écriture |
|---|---|---|---|---|---|---|
| **raid0 `md0`** (4 NVMe, nœud 1) | 1,95 Go/s | **7,45 Go/s** | 10 058 i/s (92 µs) | 57 623 i/s | 10 035 i/s (92 µs) | **2,86 Go/s** |
| nvme2n1p2 (1 NVMe, btrfs, nœud 0) | 1,15 Go/s | 3,47 Go/s | 9 065 i/s (108 µs) | 54 430 i/s | 12 124 i/s (103 µs) | 1,13 Go/s |
| sda2 (HDD 11 To) | 0,27 Go/s | 0,29 Go/s | 108 i/s (8 646 µs) | 207 i/s | 39 i/s (27 713 µs) | 0,35 Go/s |

Ce que ça dit, et qui n'est pas « l'array est plus rapide » :

* **le gain est en débit, pas en latence.** À QD1 l'array fait **1,1×** un NVMe seul : quatre
  contrôleurs **DRAM-less** (`MAXIO MAP1202`, lu dans `lspci`) derrière `md` ne réduisent pas la
  latence d'une lecture isolée. Le § 8 l'annonçait (« les contrôleurs DRAM-less peuvent être en
  dessous, surtout en écriture ») : c'est vrai en aléa QD1, et **2,86 Go/s** en écriture est
  effectivement en dessous des 4 × ~1,5 Go/s d'une extrapolation naïve ;
* **×3,8 entre 1 et 8 lecteurs** (1,95 → 7,45 Go/s) sur le **même** support. C'est le chiffre qui
  manquait au § 6.5.1 (« les lecteurs parallèles ne sont pas utilisés ») : sur cet array, le
  parallélisme du chemin de lecture n'est pas une optimisation, c'est **le** régime ;
* une entrée d'engram de 264 octets passe de **27 713 µs** (mécanique) à **92 µs** — ×300, ce qui
  confirme la mesure de `~/IA/modeles-lourds/README.md` (16 936 µs/entrée sur le mécanique).

## 2. Le pari du § 1 tient (et c'est vérifié, pas supposé)

| attendu (`configuration-nvme-raid-amd.md`) | mesuré le 12/10 |
|---|---|
| les 4 NVMe sur le **nœud 1** | `numa_node = 1` pour `nvme0n1`, `nvme1n1`, `nvme3n1`, `nvme4n1` ✅ (le système est sur `nvme2n1`, nœud 0) |
| les Quadro en **x16** — « si c'est x8, le pari est perdu » (§ 7.5) | `0000:03:00.0` et `0000:04:00.0` : **16x** ✅ (à 2,5 GT/s **au repos** — le § 7.5 le prévoit ; la montée sous charge reste à voir) |
| array à **6-7 Go/s** (§ 8, extrapolé) | **7,45 Go/s** en lecture à 8 flux ✅ |

## 3. Le QPI ne coûte rien à pleine bande (§ 6.3, § 7.4)

Le § 6.3 laissait la question ouverte — « avec 6-8 Go/s, c'est la moitié du QPI : à mesurer ». Mesure
du **côté lecture** (O_DIRECT, 2 Go par essai, 3 répétitions entrelacées, médiane) :

| placement | 1 flux | 8 flux |
|---|---|---|
| `cpu0+mem0` (moteur sur le nœud 0) | 1,80 Go/s | **7,47 Go/s** |
| `cpu1+mem1` (moteur sur le nœud 1) | 2,22 Go/s | **7,42 Go/s** |
| `cpu0+mem1` (mémoire nœud 1, calcul nœud 0) | 2,11 Go/s | **7,41 Go/s** |

* **à 8 flux, les trois placements sont identiques à 1 %** : les 7,4 Go/s traversent le QPI sans
  pénalité mesurable. La crainte du § 8 (« le QPI portera 6-8 Go/s : la moitié de ce qu'il
  écoule ») ne se matérialise pas sur cette charge ;
* **à 1 flux, l'écart (1,80 contre 2,22) n'est pas séparable du bruit** : les étendues se
  recouvrent (1,69-2,23 contre 1,81-2,25). Il faudrait plus de répétitions pour trancher, et la
  règle du dépôt (3 répétitions entrelacées) ne suffit pas ici ;
* **ce qui n'est pas mesuré** : la troisième ligne du § 6.3 côté **calcul** (des fils de lecture
  sur le nœud 1 qui envoient leurs tenseurs au nœud 0, ou aux GPU). Ce banc ne mesure que la
  lecture.

## 4. Ce que le moteur n'en voit pas encore (§ 7.2)

`--materiel` doit « montrer les GPU sur le nœud 0, et **l'array sur le nœud 1** » (§ 7.2). Il
montre :

```
GPU  0 · Quadro RTX 5000 · 15.6/16.0 Go libres · 1 lien(s) NVLink
GPU  1 · Quadro RTX 5000 · 15.6/16.0 Go libres · 1 lien(s) NVLink
DISQ /home/stephane/FastNVMe · 715 Go libres · nœud 0
DISQ /home/stephane/Data13TB · 2004 Go libres · nœud ?
```

**L'array n'y est pas.** La cause est nommée, elle est petite : `drave-core/src/materiel.rs:244`
porte une **liste de deux chemins en dur** (`/home/stephane/FastNVMe`, `/home/stephane/Data13TB`),
et le nœud est lu par `/sys/block/<bloc>/device/numa_node` — or `md0` n'a pas de `device/`, donc
même ajouté, il rendrait « nœud ? » comme le HDD (qui, lui, n'a réellement pas de nœud). Deux
lignes à changer, plus la résolution `md0 → ses disques` (`/sys/block/md0/md/dev-*/`) pour obtenir
le **nœud 1** attendu.

## 5. Ce que l'array porte depuis le 12/10

| source | destination | taille | vérification |
|---|---|---|---|
| `FastNVMe/{modeles-lourds,k3-nvme,artefacts}` (phase 1, 14:44) | `~/IA/…` | 685 Go | rsync (sans seconde passe — phase 1) |
| `~/.cache/huggingface` | `~/IA/cache/huggingface` | 6,0 Go | sommes de contrôle des deux côtés |
| `~/.cache/ccache` | `~/IA/cache/ccache` | 528 Mo | sommes de contrôle |
| `FastNVMe/qwen3-30b-a3b-Q4_K_M.gguf` | `~/IA/modeles/` | 18,5 Go | SHA-256 identique (`6c997b8a…74d0`) |
| `Data13TB/stephane/ollama-models` | `~/IA/modeles/ollama` | 59 Go | sommes de contrôle (37 fichiers) |
| `FastNVMe/kld` (4 vidages `.kld` de logits) | `Data13TB/stephane/archives/kld-logits-2026-09-24` | 6,4 Go | sommes de contrôle + `sha256` d'un fichier |

Les chemins configurés **n'ont pas changé** (liens) : `OLLAMA_MODELS`, `~/.cache/huggingface`,
le gguf du § `campagne-benefices.sh`. Vérifié côté outil : `ollama serve` + `ollama list` rend les
**7 modèles** depuis l'array, et le store appartient désormais à `stephane` (le `pull` fonctionne,
ce qu'interdisait le dossier `ollama:ollama` précédent).

**Ce qui n'existe QUE sur l'array** : `~/IA/artefacts` (116 Go de clusters réécrits), dont la copie
de sûreté sur le mécanique a été **vérifiée octet pour octet** le 12/10
(`Data13TB/stephane/sauvegardes/artefacts-2026-10-12`, manifeste SHA-256 de 45 fichiers, 2 liens
identiques). Un raid0 n'a **aucune redondance** : cette copie est la seule protection.

## 6. Ce qui ne gagne PAS (mesuré, donc pas fait)

* **la compilation de `drave-core`** : 48,03 s (cible sur le HDD) contre 48,79 s (cible sur
  l'array), 47 s de `user` pour 0,7 s de `sys`, **2,9 Mo** d'artefacts — la cible reste sur le HDD.
  Migrer n'aurait été qu'un déplacement ;
* **le cache `uv`** (3,3 Go) : `uv` **lie** son cache aux environnements virtuels ; sur deux
  systèmes de fichiers, il **copie**. Laissé en place.

## 7. Un piège trouvé par le banc : des `EIO` sur btrfs en lecture directe concurrente

Huit fils lisant le même fichier btrfs avec un **descripteur partagé** rendent `EIO` sur ~4-6 % des
lectures, toujours à des offsets 4 Kio alignés. Trois faits tranchent : les compteurs d'erreurs de
`md0` restent à **0** ; les mêmes lectures en mode normal — qui **vérifient les sommes de contrôle
btrfs** — passent toutes ; avec un descripteur **par fil**, **0 erreur sur 2 000**, sur les deux
supports. C'est une bizarrerie du chemin `O_DIRECT` concurrent sur btrfs, **pas** un disque et
**pas** une corruption. L'array (ext4) n'en rend aucune. Le banc porte donc un descripteur par fil.

## 8. Un effet de bord utile : la porte topologie survit au redémarrage

`REPRISE.md` § 2 nommait **une seule** porte incapable de tourner après un redémarrage :
`porte-topologie.sh`, qui réclamait `/tmp/m5_d384_dense.gguf` et `/tmp/campagne24/ids_m5_d384_dense.txt`
— deux fichiers que `/tmp` emporte. Vérifié le 12/10 : **elle tourne**, avec des prérequis
**persistants** sur l'array et un modèle de substitution à 24 couches :

```bash
IDS=~/IA/scratch/prerequis/ids_qwen05_wt2.txt      # tokenisé une fois, gardé sur le raid
./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
    --tokenize --fichier data/wikitext2_test.txt --sortie "$IDS"
MODELE=models/Qwen2.5-0.5B-Q8_0.gguf IDS=$IDS LIMITE=255 \
M3=models/Qwen2.5-0.5B-Q8_0.gguf     IDS3=$IDS tools/porte-topologie.sh
```

Résultat : référence **17,4702** ; découpage historique et découpage par topologie **30,4363**
(écart **0,00e0**, porte tenue) ; les deux refus sont nommés ; relais deux régions / trois
instances **42,5477 = 42,5477**, écart **0,00e0**. Le cas 5 était sauté faute d'`IDS3` — c'est le
seul prérequis qui manquait, et il tient en un fichier de 395 Ko qu'on garde.

## 9. Ce qui reste ouvert

* `read_ahead_kb` = **1 024** sur `md0` et les NVMe (§ 6.2 proposait 4 096-8 192) : **root requis**,
  rien n'est mesuré tant que la valeur n'est pas changeable ;
* la **montée en vitesse du lien GPU sous charge** (§ 7.5) : x16 vérifié **au repos** seulement ;
* la **troisième ligne du § 6.3** (fils de lecture nœud 1 × calcul nœud 0) : mesurée côté lecture,
  pas côté calcul ;
* `~/IA` est à **83 %** (162 Go libres) : premier candidat à sortir, `~/IA/k3-nvme` (228 Go, 5
  shards sur 32, la bibliothèque du mécanique les porte tous) ;
* `docs/numa-segregation.md` décrit l'état d'**avant** (« NVMe 931 Go, 97 % plein, 29 Go libres ») ;
* `tools/harmony_canonique.py:17` pointe `…/GitHub/Drave/…`, chemin **mort** (le dépôt est
  `Qtrinet`) — la porte qui s'en sert échouerait sans le dire.

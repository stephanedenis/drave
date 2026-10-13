# Les lecteurs parallèles — lire dans nos tampons au lieu du mapping

> **2026-10-12, 20 h 50 HAE** (heure lue sur la machine). Note de conception : ce qui est
> **mesuré**, ce qui existe déjà, ce qui reste à trancher, et les **portes à tenir** (§ 5) —
> écrite avant le code, comme `docs/note-cycle-c2.md` § 4 et `docs/note-peripherie-c8.md` § 6.
> Elle prolonge **S4** (`docs/strata-pour-drave.md` § S4) : la prélecture parallèle est entrée
> dans le moteur le 12/10 et a réglé la moitié du problème — le calcul n'attend plus les défauts
> de page — mais **les octets passent toujours par le mapping**.

## 1. Le chiffre qui ouvre le chantier

| mesure | valeur | où |
|---|---|---|
| l'array, huit lecteurs séquentiels | **7,45 Go/s** | `~/IA/README.md` (banc `banc-io.py`) |
| le même array, lecture **à la demande** d'un motif d'experts | **1 126 Mo/s** | `tools/banc-experts.py` |
| le même motif, **`pread` depuis huit fils** dans des tampons | **3 995 Mo/s** (×3,5) | `tools/banc-experts.py` |
| dans le moteur, la passe réelle (8 jetons de Qwen3-30B) | ~350 Mo/s utiles ; le **calcul** paie les défauts de page : 7,70 s → **3,65 s** après la prélecture parallèle | `tools/porte-prechargement.sh` |

Le § 6.5.1 de `docs/configuration-nvme-raid-amd.md` l'avait écrit le 08/10 : « **les lecteurs
parallèles ne sont pas utilisés** — le plan calcule `lecteurs = 16` et ne s'en sert jamais ; sur un
RAID0, c'est le chemin de lecture qu'il faut paralléliser explicitement (`pread` par bande, ou
`O_DIRECT`) ». La mesure du 12/10 lui donne son chiffre.

## 2. Ce qui existe déjà, et pourquoi ça ne suffit pas

| mécanisme | état | pourquoi il ne suffit pas |
|---|---|---|
| `mmap` paresseux | le défaut | un défaut de page par page, synchrone ; **957 170** défauts majeurs sur une passe de 8 jetons |
| `madvise(WILLNEED)` | en place, mesuré **inerte** | ×1,06 sur une plage entière ; la granularité ne change rien dans le moteur (31-36 s partout) |
| `prelecture_parallele` (S4, 12/10) | **actif, mesuré** | le calcul ne paie plus les défauts (÷2,1) — mais les octets entrent toujours par le mapping, un défaut par page, aidés seulement de la lecture en avance du noyau |
| `DRAVE_EXPERTS_RAM` | mesuré **perdant** (+4 % à 4 Go, +21 % à 32 Go) | c'est un **cache**, pas un **lecteur** : il copie au chargement, il ne lit pas en avance |
| `blocs_expert(e) -> &[u8]` | existe | le chemin « expert en RAM » sait déjà rendre des **octets** : c'est la porte par laquelle un tampon peut entrer dans le calcul |

## 2bis. État au 13/10 — les tampons sont dans le moteur, et ils gagnent sur les deux tableaux

`DRAVE_TAMPONS=1` lit les experts **retenus** par `pread`, **par offset croissant**, dans des
tampons réutilisables, et le calcul lit ces octets. Mesuré sur la même passe (8 jetons de
Qwen3-30B, array, cache évincé avant chaque bras, perplexité identique dans les quatre) :

| bras | octets lus | passe (mural − chargement) |
|---|---|---|
| à la demande (`DRAVE_PRELIRE=0`) | 9,52 Go | 5,97 s |
| `madvise` | 8,04 Go | 7,25 s |
| fils qui entrent les pages | 10,90 Go | 3,70 s |
| **tampons séquentiels** | **6,22 Go** | **3,40 s** |

C'est le seul bras qui gagne **et** sur les octets **et** sur le temps : la lecture en avance du
noyau dépasse la plage utile de 75 %. Ce qui reste de ce chantier est en § 4 (le pool et le
recouvrement), et le côté **VRAM** a été mesuré puis corrigé le même jour : **l'allocation** y est
37 à 91 % du coût d'un montage, et un pool l'a supprimée (`reports/rapport-vram-transfert.md`).

## 3. `MADV_POPULATE_READ` : TRANCHÉ le 13/10 — il ne remplace pas les tampons

La question était posée « avant tout » : le noyau entre une plage d'un seul appel (constante 22,
absente de Python mais présente dans `libc`), ce qui pourrait rendre les tampons inutiles.
Mesuré par `tools/banc-experts.py` (24 plages de 4 Mio, 101 Mo utiles par bras, array, médiane de
trois répétitions) :

| bras | débit utile (médiane) | |
|---|---:|---|
| à la demande | 1 021 Mo/s | |
| `madvise` par plage | 1 070 Mo/s | |
| `madvise` par tranches | 2 077 Mo/s | |
| **`MADV_POPULATE_READ`** | **2 121 Mo/s** | ≈ `madvise` par tranches |
| **`pread`, 8 fils** | **4 603 Mo/s** | **2,2× mieux** |

**Verdict : `MADV_POPULATE_READ` ne vaut pas mieux que le `madvise` par tranches déjà en place**
(2 121 contre 2 077, dans le bruit), et il reste **2,2× sous le `pread` parallèle**. Les tampons
ne sont donc pas un détour : c'est le seul chemin qui atteint le débit du disque. Le chantier
« lecteurs parallèles » garde son dessin — et la mesure est rejouable
(`python3 tools/banc-experts.py <modele>`).

*Et un défaut de banc corrigé au passage* : le bras `populate` passait l'**offset dans le fichier**
comme adresse à `madvise`, qui veut une **adresse virtuelle** — le noyau répondait `ENOMEM` et le
bras ne mesurait rien. Sondé par tailles avec un mapping monté à la main : `POPULATE_READ` marche
partout, donc le refus ne venait pas du noyau.

## 3bis. Le dessin tel qu'il a été construit

Le noyau 7.2 connaît **`MADV_POPULATE_READ` (22)** : entrer une plage d'un seul appel, sans passer
par un défaut par page. Si ce chemin rend ce que rendent huit fils qui touchent les pages
(3,5 à 4 Go/s sur le motif d'experts), alors **le chantier des tampons n'a pas lieu d'être** :
quelques lignes suffisent, et le calcul continue de lire le mapping.

**Première commande** (le banc porte déjà le bras) :

```bash
python3 tools/banc-experts.py ~/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf     # bras « populate »
```

C'est la première chose à faire, et elle peut clore la note.

## 4. Le dessin, si les tampons sont nécessaires

Deux variantes, dans cet ordre — la première est bornée et ne demande aucun routage :

* **(a) les poids denses d'abord.** Les `wq/wk/wv/wo` d'une couche sont **connus d'avance** : un
  pool de N tampons (double tampon par couche), R fils qui `pread` la couche `l+1` pendant que la
  couche `l` calcule, et le calcul lit dans le tampon. Borné : une couche dense de V4.1 se compte
  en dizaines de mégaoctets, pas en gigaoctets. C'est `Layer::plages_denses()` (ajouté le 12/10)
  qui donne les plages à lire ;
* **(b) les experts ensuite.** Les `k` experts retenus ne sont connus qu'après le routage de la
  couche : la lecture doit alors se faire dans le pool juste après le routage, et le calcul doit
  lire le tampon au lieu du mapping. `blocs_expert()` rend déjà les octets — reste à faire
  consommer ces octets par les noyaux (c'est là qu'est le vrai travail, et c'est ce que
  `DRAVE_EXPERTS_RAM` faisait de travers : il copiait **tout**, une fois, au lieu de lire **ce qui
  va servir**, juste à temps).

Ce que ça coûte, et les deux risques à surveiller : la **mémoire** (125 Go ; le modèle reste
mmappé — « la RAM ne peut pas en garder une copie », `docs/modele-pour-drave.md`) et le
**placement NUMA** des tampons (l'array est sur le **nœud 1** ; mesuré le 12/10 : le QPI ne coûte
rien à pleine bande — 7,41 / 7,42 / 7,47 Go/s aux trois placements — mais un tampon écrit par un
fil du nœud 1 et lu par le calcul du nœud 0 traverse, lui).

## 5. Les portes à tenir (écrites AVANT le code)

1. **la perplexité ne bouge pas** — un octet près : un lecteur qui se trompe de plage change le
   calcul, et le changement doit être vu (`tools/porte-prechargement.sh` a déjà ce contrôle, et
   c'est le seul non négociable) ;
2. **le temps de calcul baisse ET le temps mural baisse** : un lecteur qui déplace le temps sans
   le réduire n'a rien gagné — c'est ce que la prélecture dense de S4 a montré (30,47 s sans,
   32,05 s avec), et c'est pour ça qu'elle est éteinte ;
3. **les octets lus sont publiés**, pas érigés en critère : sur l'array la bande passante est
   abondante, sur un plateau elle ne l'est pas — la porte doit permettre de reprendre la décision
   sur l'autre support ;
4. **une vue ROUGE** : un lecteur volontairement décalé d'une plage (`DRAVE_LECTEUR_DECALE=1`) doit
   faire échouer la porte — sans quoi elle ne vérifie rien.

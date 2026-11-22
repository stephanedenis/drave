# Le banc de génération du natif — le modèle a appris les mots, pas la phrase

> **Ligne de roadmap** : **N4** (l'usage du natif) · **Date** : 2026-11-16 · **Modèle mesuré** :
> `work/n2ac/mix1024-60k.pt` (**34,3 M** paramètres, RoPE, seq 1 024, PPL **2,40**, corpus
> `wiki_mix/propre`) · **Verdict** : ❌ **le natif n'est pas un générateur de texte** — il a
> appris le **vocabulaire** (87 % de mots réels), pas la **composition** (un trigramme répété
> **15 fois** en greedy, des pseudo-mots en échantillonnage).
>
> **Le chiffre, en une ligne.** Sur **20 prompts** fixes et **128 octets** par prompt, trois
> réglages : **greedy** 0,870 de mots valides mais une **répétition de 15** ; **top-40/0,8**
> 0,490 de mots valides et une diversité de 1,000 ; **top-20/0,5** 0,735 et 0,981. Le
> **contrôle aléatoire** (même architecture, poids au hasard) : **0,336** de mots valides et
> **1** de répétition — le banc discrimine le modèle du bruit.

## 1. Le dispositif

[`tools/banc_generation.py`](../tools/banc_generation.py) : 20 prompts français
(« La France est un pays », « Dans les années 1950 », « Il était une fois »…), trois réglages
(greedy ; top-40 + 0,8 ; top-20 + 0,5), 128 octets par génération. Mesures par réglage : les
**mots valides** (la fraction des mots générés présents dans les 50 000 formes les plus fréquentes
du corpus), la **diversité** (distinct-2), la **répétition** (le plus grand nombre d'occurrences
d'un trigramme), l'**écho** (la fraction des mots générés recopiés du prompt), le **débit**.

**Contrôle négatif** : `--aleatoire` (la même architecture, les poids au hasard, la graine 1234).

## 2. Les résultats

| réglage | mots valides | distinct-2 | répétition | écho | octets/s |
|---|---:|---:|---:|---:|---:|
| **greedy** | **0,870** | 0,726 | **15** | 0,01 | 36,4 |
| top-40 / 0,8 | 0,490 | 1,000 | 1 | 0,01 | 36,4 |
| top-20 / 0,5 | 0,735 | 0,981 | 1 | 0,01 | 36,6 |
| **aléatoire (contrôle)** | **0,336** | 1,000 | 1 | 0,00 | 41,7 |

**Lecture.** (1) Le modèle **connaît les mots** : 0,870 contre 0,336 au hasard (+0,53). (2) Il
**ne compose pas** : en greedy, il tombe dans une boucle (un trigramme 15 fois) ; en
échantillonnage, il invente des pseudo-mots (0,49–0,74). (3) Le **débit** est de ~36 octets/s
(byte-level, 34 M sur CPU).

## 3. Les échantillons (la preuve, pas l'impression)

```
greedy  : « La France est un pays don d d da d 20 n dese de 1 20 20 aba dele 1 la 1 20 20 201 1 »
top-20  : « La France est un pays 2010 sene don d ousi le e 20 ste 2019 de 20 1 se confolemenatéce »
greedy  : « Dans les années 1950 le por le de la da la le e e de de e ena 20 1 esa la en ena da da »
```

La **cohérence s'arrête au prompt + ~3 mots** ; ensuite viennent les **nombres du corpus** (20,
201, 2019, 2020 — les dates) et les **formes inventées**. C'est le « 12 octets puis dérive » de
l'archive, mesuré.

## 3 bis. Le natif jugé par notre analyseur (le banc de grammaticalité)

[`tools/banc_grammaticalite.py`](../tools/banc_grammaticalite.py) passe les **136 générations**
(les 20 prompts × 3 réglages × le natif et le contrôle) dans **notre propre analyseur** :

| source | GV moyens | GN moyens | ciment (classes fermées) | attachements |
|---|---:|---:|---:|---:|
| **natif** (greedy) | **6,90** | 2,85 | 0,335 | 0,737 |
| natif (top-20) | 5,85 | 3,15 | 0,310 | 0,789 |
| **aléatoire** (greedy) | **2,30** | 1,80 | 0,791 | 0,747 |
| aléatoire (top-20) | 4,00 | 2,35 | 0,796 | 0,670 |

**Lecture.** Le natif a **trois fois plus de GV** que le hasard (6,9 contre 2,3) : il a appris
quelque chose de la **position des verbes**. Mais son **ciment** est **bas** (0,335 contre 0,791) :
ses textes sont des **mots de contenu** sans la glu grammaticale (les déterminants, les
prépositions) — la structure est un squelette, pas une phrase. Les **attachements** ne
discriminent pas (l'analyseur attache tout, même le bruit).

## 3 ter. L'échelle — trois checkpoints, la même mesure

Le même banc (20 prompts, 128 octets) sur trois tailles, tous byte-level :

| modèle | paramètres | PPL | greedy : mots valides | greedy : répétition | top-20 : mots valides |
|---|---:|---:|---:|---:|---:|
| `cap-1147m-512` | 11,8 M | 3,58 | 0,247 | 1 | 0,258 |
| `cap-2165m-512` | 21,6 M | 3,40 | **0,494** | 6 | 0,431 |
| `mix1024-60k` | **34,3 M** | **2,40** | **0,870** | **15** | **0,735** |

**Ce que ça dit.** (1) **L'échelle achète le vocabulaire** : +0,25 puis +0,38 de mots valides par
doublement — les 11 M/21 M produisent des **formes** (« cinistilité », « estinstas »), les 34 M
des **mots réels**. (2) **Elle n'achète pas la composition** : la **répétition monte** avec la
taille (1 → 6 → 15) — le grand modèle **reproduit les boucles** du corpus ; il mémorise, il ne
phrase pas. (3) Les échantillons le montrent : le 34 M bascule des mots aux **nombres** (20, 201,
2020) — la signature des dates de la Wikipédia.

**La syntaxe à l'échelle** (notre analyseur, le greedy) : les **GV** moyens passent de **1,90**
(11 M) à **2,65** (21 M) et **6,90** (34 M) ; le **ciment** (les classes fermées) de **0,137** à
**0,278** et **0,335**. L'échelle aide aussi la structure — mais le ciment reste **sous** le
niveau du hasard (0,79), et la **répétition** monte. Le détail :
[`banc-grammaticalite-echelle.json`](banc-grammaticalite-echelle.json).

**La conséquence pour le plan** : un 100–150 M aura **de meilleurs mots** et **autant de boucles**
si rien ne change ; le palier 1 doit donc traiter la **répétition** (le contrôle, la
régularisation, les données dédupliquées), pas seulement la taille.

## 4. Ce que le banc ne dit pas

- **La validité lexicale n'est pas la grammaticalité** : « 20 » est dans le vocabulaire du corpus.
- **20 prompts** et **128 octets** : un échantillon, pas une distribution.
- **Le byte-level** pénalise le débit ; un BPE changerait les chiffres, pas le diagnostic.

## 5. Ce qu'il faudrait (le chemin, chiffré)

1. **Le tokenizer BPE** (4 000–8 000) : ~8× moins de pas pour un même texte, et la qualité par
   paramètre remonte. **Le levier le plus rentable.**
2. **L'échelle** : 34 M est petit ; le corpus (1 Go) nourrirait un 150–300 M — mais l'entraînement
   passe de 3,7 h à des jours, et le GPU est réservé.
3. **L'alignement** (SFT) : le N4.6 mémorisait (24/24 vus, 0/4 tenus) ; un vrai SFT demande des
   données d'instruction, pas le corpus brut.
4. **L'évaluation** : ce banc est le début ; il faut une mesure de **grammaticalité** (un
   analyseur, le nôtre !) sur les générations.

## 6. La conclusion honnête

Le natif est un **prototype de recherche** : il sait **modéliser** (PPL 2,40, les mots appris) mais
pas **produire**. Ce n'est pas un défaut de plomberie (l'entraînement, la génération, le service,
le DRVM existent) : c'est un défaut de **qualité**, et il se paie en semaines de calcul, pas en
jours. Le produit `drave` exploitable reste le **bloc linguistique** (183/183, 0 dépendance) ; le
natif est le **chantier suivant**, pas une livraison.
## Le 100 M — le banc à 3 000 pas (et à 30 000, en cours)

Le **même protocole** (20 prompts, 3 réglages, le contrôle aléatoire), sur le checkpoint 100 M
(96,7 M de paramètres, d_model 640, 8 blocs, entraîné sur `data/wiki_mix/propre`).

| modèle | pas | mots valides (greedy) | distinct_2 | **répétition** | echo | octets/s |
|---|---:|---:|---:|---:|---:|---:|
| 11 M | 3 000 | 0,247 | — | 1 | — | — |
| 21 M | 3 000 | 0,494 | — | 6 | — | — |
| 34 M | 30 000 | 0,870 | — | **15** | 0,01 | 36 (CPU) |
| **100 M** | **3 000** | **0,882** | 0,753 | **6** | 0,03 | **78 (GPU)** |
| **100 M** | 30 000 | *en cours* | — | — | — | — |

**La lecture.** Le 100 M, avec **30× moins de données vues** que le 34 M, fait **mieux** sur les mots
(0,882 contre 0,870) et **réduit la répétition de 2,5×** (6 contre 15). Sur le même nombre de
jetons, il est donc **~10× plus efficace** : c'est la réponse à la question du 16/11 — **l'échelle
paie**, et elle paie surtout sur la dérive.

**Les réglages échantillonnés** : top-40 (0,583, distinct 1,000, répétition 1) et top-20 (0,708,
distinct 0,970, répétition 2) restent **sous le greedy** sur les mots — la même signature que le
34 M.

**Le débit** : 78 octets/s sur le GPU (le 100 M), contre 36 sur le CPU (le 34 M) — le GPU n'apporte
que ×2 ici, parce que la génération est **memory-bound** (le CPU lit 136 Mo de poids par jeton).


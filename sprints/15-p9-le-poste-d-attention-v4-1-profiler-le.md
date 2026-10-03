# Sprint 15 — P9 — le poste d'attention V4.1 : profiler les 12,4 s par jeton, puis accélérer SANS changer un chiffre (preuve d'égalité au bit près sur les vides)

- **Début** : 22:01 · **Fin** : 22:32 (31 min utiles — la boîte s'arrête quand les
  chantiers sont livrés, mesurés et commités ; les mesures ont été courtes parce
  que la passe V4.1 est passée de 66 s à 22 s dans ce bloc même)
- **Objectif** : P9 — le poste d'attention V4.1 : profiler les 12,4 s par jeton, puis accélérer SANS changer un chiffre (preuve d'égalité au bit près sur les vides)
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. La mesure : 12,4 s par jeton, et une étiquette qui trompait

Le profil de la passe V4.1 attribuait **12 369,91 ms par jeton** au poste
« attention », dont « scores 0,00 | softmax 0,00 » — parce que ces deux
sous-compteurs appartiennent à l'autre chemin d'attention (le MLA de V3) : sur
V4.1, **tout `attn_v4` tombait dans le poste**, projections comprises, sous une
étiquette (« somme pondérée + écriture KV ») qui ne décrit que sa dernière partie.

Deux mesures ont suffi à savoir où creuser :

| mesure | résultat |
|---|---|
| `--moe-topk 1` (MoE réduit ~6×, pour retirer la contention de cœurs) | attention **7 283,42 ms/token**, proj+mlp 1 039,64 — le poste ne bouge pas d'un ordre : il est bien dans `attn_v4` |
| lecture du code | `matvec_f32` — le produit matrice-vecteur f32 du chemin V4 — est une boucle **mono-fil scalaire**, appelée 11 fois par couche (q_a, q_b, kv, comp_kv, comp_gate, indexeur, sortie groupée) : ~41 M de produits par couche et par jeton, soit **1,65 G de produits par jeton** pour 20 cœurs inoccupés |

### 2. Le correctif : parallèle par LIGNES, donc identique AU BIT PRÈS

`matvec_f32_fils` découpe les **lignes de sortie** entre les fils (tranches
contiguës, comme le noyau d'experts ; `o - o0` pour indexer la tranche du fil,
car indexer par le numéro de ligne global lève « len is 256 but the index is
256 » dès le deuxième fil). Chaque ligne reste sommée par **un seul fil, dans le
même ordre** : aucune réassociation, donc aucune raison qu'un bit change — et
c'est la seule forme d'accélération qui n'a pas à être annoncée comme un
changement de calcul. Un seuil évite de payer un `spawn` (~30 µs) sous 65 536
produits.

Mesuré, passe complète V4.1, mêmes jetons, ctx 8, 8 bits :

| poste | avant | après | gain |
|---|---|---|---|
| **attention** | 12 369,91 ms/token | **1 324,48 ms/token** | **×9,34** |
| proj+mlp (MoE, lectures d'experts) | 9 383,19 | 5 945,70 | ×1,58 (contention en moins) |
| **total** | 21 753,10 ms/token | **7 270,18 ms/token** | **×2,99** |
| perplexité (3 jetons) | 1 743 713,6243 | **1 743 713,6243** | **identique** |
| vides (`DRAVE_DUMP_COUCHES`, 2 544 tenseurs) | — | **0 différent** | **identique au bit près** |
| durée de la passe | 66-68 s | **22,2 s** | ×3 |

La parallélisation couvre aussi le `wkv` de l'engram ([25 600, 6 144], 157 M de
produits par couche et par jeton) et les projections de `forward_mla` — d'où la
porte V4-Flash, qui doit rendre **exactement** 8430,4966.

### 3. Le gain à contexte plus long, et la troisième preuve d'égalité

Même commande que l'A/B de l'engram du bloc 14 (31 jetons, ctx 32, 8 bits), avec
le binaire d'avant puis d'après :

| mesure | avant | après |
|---|---|---|
| durée de la passe | 313,1 s | **152,9 s** (×2,05) |
| poste `attention` | (12,4 s/token à ctx 8) | **1 004,36 ms/token** |
| poste `proj+mlp` | (9,4 s/token à ctx 8) | 3 707,07 ms/token |
| perplexité (31 jetons) | 115 521,8693 | **115 521,8693** |

Le gain tombe de ×3 (ctx 8) à **×2,05** (ctx 32) : le débit mémoire reprend la
main quand le cache ne suffit plus, exactement ce que la rétrospective mettait en
doute. Et la perplexité identique **au dernier chiffre** est une troisième preuve
d'égalité — à un autre contexte, sur un autre nombre de jetons.

### 4. Le profil dit maintenant ce qu'il mesure

L'étiquette « somme pondérée + écriture KV » recouvrait tout `attn_v4` : cinq
sous-compteurs la remplacent (statiques `PROF_V4`, une ligne de plus au profil),
et la répartition est sans ambiguïté — mesuré, ctx 32, 31 jetons, 145,1 s :

```
attention 1002,74 ms/token
  dont attn_v4 : projets q/kv 372,34 | compresseur 6,73 | indexeur 11,66
                 scores + softmax + somme 45,02 | dé-rotation + sortie groupée 566,75
```

Le **calcul d'attention proprement dit** (scores, softmax, somme pondérée) vaut
**45,02 ms/token, soit 4,5 %** du poste ; le reste est de la projection — dont
**566,75 ms pour la dé-rotation et la sortie groupée** (`wo_a`/`wo_b`), le premier
poste d'`attn_v4` désormais. Et la perplexité est encore **115 521,8693**, la même
qu'avant l'optimisation : les compteurs ne changent rien.

### 5. Ce que la mesure laisse sur la table, et pourquoi on s'arrête là

Le poste d'attention lit ~6,6 Go de poids par jeton (41 M de poids f32 × 40
couches) en 1,32 s, soit **≈ 5 Go/s** — loin des ~40-60 Go/s que la DDR4 de cette
machine peut rendre. Le levier suivant est le **SIMD** (AVX2, comme `dot8_avx`),
et il n'est **pas** gratuit : huit accumulateurs partiels **changent l'ordre de la
sommation**, donc changent des bits, donc changent la référence de non-régression
(V4-Flash 8430,4966 et tous les chiffres publiés du chemin f32 seraient à
re-mesurer). Décision de ce bloc : **ne pas le faire** — le poste qui domine
maintenant est `proj+mlp` (5 946 ms/token, des lectures d'experts sur NVMe, déjà
mesuré comme I/O-bound par P9), et il se traite par une autre politique de
lecture, pas par des noyaux.

## Rétrospective — garder / changer / doute

**Garder.**

- **« Parallèle par lignes » comme premier réflexe** : quand un noyau scalaire
  mono-fil est chaud, découper les *sorties* donne le gain des cœurs **sans**
  toucher à l'arithmétique. Le seuil de 65 536 produits et la tranche `o - o0`
  viennent du noyau d'experts — les deux pièges déjà connus du dépôt (spawn
  inutile, index global dans une tranche).
- **La mesure d'isolement `--moe-topk 1`** : elle a séparé deux postes qui se
  disputaient les mêmes cœurs, sans instrumenter une ligne de code.

**Changer.**

- **Le profil doit dire ce qu'il ne mesure pas.** « somme pondérée + écriture KV »
  était le *reste* de `prof[2]` : sur V4.1 il contenait aussi les projections, le
  compresseur et l'indexeur, et « scores 0,00 | softmax 0,00 » faisait croire que
  l'attention ne coûtait rien. Action : nommer les postes par ce qu'ils couvrent
  (`attn_v4` en entier) ou instrumenter les sous-postes — c'est écrit ici, et
  c'est la prochaine fois qu'un profil V4.1 sera lu.

**Doute.**

- Le gain de ×9,34 est mesuré à ctx 8 sur quatre jetons avec 20 fils, et le gain
  de bout en bout tombe à **×2,05** à ctx 32 — le débit mémoire reprend la main.
  C'était le doute de cette rétro, et il est confirmé par la mesure : annoncer
  « ×9 » sans contexte aurait été une promesse fausse.
- La parallélisation ne dit rien de la **latence** : à un fil, un jeton coûte
  21,8 s ; à vingt, 7,3 s. Sur une machine déjà chargée, le poste redevient
  mono-fil et le gain disparaît.

## Portes

- `tools/portes.sh rapide` : voir le journal du bloc — **V4-Flash doit rendre
  8430,4966** (c'est la porte qui protège `forward_mla`, touché ici), 63 tests,
  Qwen 19,3885, clusters 799,8557, engram, et les cinq modes du découpage.
- V4.1 : perplexité et vides **inchangés** (mesuré ci-dessus).

## Planning du bloc 16 — le poste dominant : les experts sur NVMe

`proj+mlp` vaut maintenant **3 530 ms/token à ctx 32** (contre 1 003 pour
l'attention) et c'est de la lecture d'experts : ~6 experts par couche sur 384,
pris au hasard dans ~330 Go, 40 couches par jeton. P9 a déjà établi que le goulot
est la LECTURE (même calcul, mêmes chiffres : 86,9 Go en 3 tranches = 111,8 s
contre 8 grappes = 39,9 s).

Chantiers du bloc 16 :

1. **Mesurer la réutilisation** : `--trace-experts` (qui existe) sur 64 jetons de
   wiki réel, puis la distribution (quels experts, combien de fois) — c'est la
   seule façon de savoir si un cache en RAM peut mordre, et `--profil-experts`
   donne déjà le compte par couche.
2. **Garder en RAM ce qui se répète** (132 Go disponibles, 330 Go d'experts) : une
   politique de résidence explicite, **sans changer un chiffre** — un expert lu
   depuis la RAM rend les mêmes octets que depuis le NVMe, donc l'égalité au bit
   près est de nouveau la preuve attendue (vides avant/après).
3. **Publier** : secondes par jeton avant/après, à ctx 8 et ctx 32, plus le taux
   de réutilisation qui justifie (ou non) la politique.

## Ce qui reste, nommé

- **Le SIMD f32** : ~5 Go/s effectifs contre 40-60 Go/s possibles, mais au prix
  d'un changement de bits et d'une re-mesure de toutes les références f32.
  Décision reportée, avec ses conditions écrites ci-dessus.
- **`proj+mlp` (5 946 ms/token)** : lectures d'experts sur NVMe. C'est le poste
  dominant maintenant ; P9 avait déjà mesuré que le goulot est la LECTURE.
- **Le profil V4.1** reste agrégé : les sous-postes d'`attn_v4` (projections,
  compresseur, indexeur, scores, somme) ne sont pas séparés.

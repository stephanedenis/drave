# Sprint 18 — Vectoriser la DÉQUANTIFICATION des experts (grille Q2_K) sans changer un bit

- **Début** : 23:44 · **Fin** : 00:12 (28 min — le noyau, sa preuve et les portes)
- **Objectif** : la déquantification des experts de V4.1 (Q2_K) pèse 25 % de la
  passe et 45 % du poste d'experts (mesuré par ablation au bloc 17). La
  vectoriser — c'est une **conversion pure, valeur par valeur**, donc le seul
  endroit du chemin des experts où le SIMD est bit-exact par construction — puis
  le prouver : vides, perplexités, portes.
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. Le noyau, et pourquoi il ne peut pas changer un bit

`Gguf::dequant_q2k_avx2` traite **huit valeurs à la fois** : huit octets chargés,
élargis en huit entiers 32 bits, décalés et masqués (2 bits), convertis en f32,
puis `(d·sc)·quant − dmin·m` — **exactement les opérations de la version
scalaire, dans le même ordre**, sans réassociation et **sans FMA** (`fma(a, b, −c)`
n'a pas le même arrondi que `a·b − c`).

C'est la différence de fond avec le SIMD du produit scalaire, écarté aux blocs 15
et 17 : là, vectoriser **réassocie une somme** et ferait tomber la référence de
non-régression. Ici, chaque valeur de sortie ne dépend que d'elle-même.

Un premier pas, avant le noyau : la version scalaire recalculait `d·sc` et
`dmin·m` **par valeur** ; les calculer une fois par groupe de 16 (la granularité
de l'échelle dans le format) est identique au bit près et a déjà rendu ×1,13 sur
le poste.

### 2. Les mesures

| mesure | avant le bloc | après (16 fils) |
|---|---|---|
| poste `proj+mlp`, ctx 8 | 2 563,79 ms/token | **2 267,69** (×1,13) |
| passe, ctx 8 | 11,4 s | **10,7 s** |
| poste `proj+mlp`, ctx 32 | 2 431,58 ms/token | **1 833,91** (×1,33) |
| passe, ctx 32 (31 jetons) | 109,8 s | **88,5 s** (×1,24) |
| perplexités ctx 8 / ctx 32 | 1 743 713,6243 / 115 521,8693 | **identiques** |
| vides, 2 544 tenseurs | — | **0 différent** |

**Cumulé depuis le début de la nuit** (blocs 15, 17 et 18), la passe V4.1 à
ctx 32 passe de **313,1 s à 88,5 s (×3,54)**, et pas un chiffre n'a bougé :
perplexités identiques à ctx 8, 32 et 64, quatre comparaisons de vides à
0 différent, porte V4-Flash inchangée.

### 3. Ce qui reste dans le poste

La conversion ne coûtait que ~45 % du poste d'experts ; le reste est le **produit
scalaire** (dont le SIMD réassocierait la somme) et les **lectures compressées**
(84 octets par 256 poids, que le noyau AVX2 lit toujours). Le noyau a donc un
plafond bas : ×1,13 à ctx 8, ×1,33 à ctx 32.

### 3bis. Et l'autre modèle lourd ? (mesuré, et c'est une piste pour la suite)

V4-Flash (43 couches, experts **IQ1_M**, 3 fragments), ctx 32, 5 jetons, 16 fils :

```
=== perplexité 8430.4966 sur 4 tokens (0 événements, 12.8 s) ===
postes : attention 1132.53 | proj+mlp 2024.50 | somme 3157.03
passe complète (chargement compris) : 24,0 s
```

Sa perplexité est **exactement** celle de la porte (8430,4966) : les
optimisations de la nuit ne lui ont pas pris un chiffre, et la parallélisation du
matvec f32 a accéléré son attention comme celle de V4.1. Mais ses experts sont en
**IQ1_M**, un format à codebook qui **n'a pas de noyau vectorisé** : c'est le même
levier qui reste ouvert, sur l'autre modèle lourd du dépôt.

### 4. Le même noyau pour IQ1_M, et ce qu'il rapporte (peu, et c'est dit)

V4-Flash tire ses experts d'un format à **codebook** (`IQ1S_GRID`, 2048 lignes de
8 valeurs) : la ligne se lit en scalaire (un `gather` coûterait plus cher), mais
l'élargissement i8 → f32, l'ajout du décalage et la multiplication par l'échelle
sont vectoriels — huit valeurs d'un coup, sans réassociation.

| V4-Flash, ctx 32, 5 jetons, 16 fils | scalaire | AVX2 IQ1_M |
|---|---|---|
| poste `proj+mlp` | 2 054,97 ms/token | **1 916,57** (×1,07) |
| passe complète (chargement compris) | 23,9 s | 23,4 s |
| perplexité | 8430,4966 | **8430,4966** |
| vides, 3 126 tenseurs (43 couches) | — | **0 différent** |

**×1,07 seulement**, et la raison est instructive : le coût d'IQ1_M n'est pas
l'arithmétique que le noyau vectorise, c'est la **lecture du codebook** (une ligne
de 8 octets tirée au hasard dans une table de 16 Ko, donc des défauts de cache par
groupe de huit valeurs). Le noyau reste — il est exact, mesuré et gratuit — mais
il ne faut pas en attendre ce qu'il ne peut pas donner : la leçon du bloc, c'est
que **le plafond d'un noyau se mesure avant de l'écrire**, et qu'ici il était bas.

## Portes

- `tools/portes.sh rapide` : **toutes vertes** — et la porte **V4-Flash
  8430,4966** est celle qui compte ici (si ses experts sont en Q2_K, le noyau
  vectorisé les déquantifie aussi), avec 63 tests, Qwen 19,3885, clusters
  799,8557, engram et les cinq modes du découpage.
- V4.1 : perplexités et vides inchangés (mesuré ci-dessus).

## Rétrospective — garder / changer / doute

**Garder.**

- **Chercher le SIMD qui ne réassocie rien.** Avant d'écrire le noyau, la
  question posée a été « quelle opération puis-je vectoriser sans changer un
  bit ? » — la réponse (une conversion pure) a donné un noyau gratuit en
  exactitude, là où le SIMD du produit scalaire aurait fait tomber toutes les
  références du dépôt.
- **L'ablation d'abord** (bloc 17) : connaître la part exacte (25 % de la passe)
  a évité de chercher un noyau pour un poste qui ne pèse pas.
- **Le pas scalaire avant le noyau** : hoister `d·sc` et `dmin·m` a rendu ×1,13
  en dix minutes, sans intrinsics — et a réduit ce que le noyau avait à gagner.

**Changer.**

- **Mesurer ce que le noyau ne peut pas atteindre.** Le poste d'experts reste à
  1 834 ms/token à ctx 32 : le produit scalaire (réassociation interdite) et les
  lectures compressées y dominent. La prochaine fois, annoncer le plafond AVANT
  d'écrire le noyau, pas après.

**Doute.**

- Le gain du noyau est mesuré sur **un** format (Q2_K, celui des experts de
  V4.1) et une machine (AVX2). Les autres formats de grille (Q3_K, IQ2_XXS,
  IQ1_M…) n'ont pas de noyau : ils paieraient le même coût sans le gain.
- **Les lectures compressées** n'ont pas été mesurées séparément du produit : le
  plafond du noyau (×1,13 à ctx 8) dit qu'il reste beaucoup, mais pas quoi.

## Planning du bloc 19 — V4.1 à 1 024 jetons : la première passe LONGUE

Ce qui bloquait la vérification à contexte long n'existe plus : la passe de
31 jetons est passée de 313,1 s à 88,5 s cette nuit (×3,54). Une passe de
**1 024 jetons** coûte donc ~45-55 min — c'est enfin abordable, et elle exerce
trois mécanismes qui n'ont **jamais** tourné à cette échelle :

1. **La sélection de l'indexeur** (`indexer.top_k` = 512) : elle ne mord qu'au-delà
   de 512 blocs compressés, c'est-à-dire ~1 025 jetons en ratio 2. Une passe de
   1 024 jetons est exactement le régime où elle CHOISIT — et le seuil a été
   vérifié à la position 512 sur une seule couche, jamais en passe complète.
2. **Le YaRN des couches compressées aux positions longues** : la question
   ouverte du bloc 12 (`reports/rapport-v4-yarn-compresse.md`) est de savoir si le
   régime YaRN ×16 tient au-delà de ~1 024 positions — précisément là où les deux
   lectures divergent.
3. **Le compresseur et le cache partagé à l'échelle** : 512 blocs par couche au
   lieu de 16, et la mémoire que ça demande (à mesurer, pas à supposer).

Chantiers :

1. **Construire 1 024 jetons réels** (wikitext, tokenizer du modèle) et lancer la
   passe avec le profil.
2. **Vérifier qu'elle est saine** : perplexité par position (le profil existe :
   `--ppl-profil`), aucune position NaN, mémoire résidente, et le compteur de
   blocs gardés (« 513 → 512 ») sur les couches d'indexeur.
3. **Publier** : temps, perplexité, sélection observée, mémoire — et ce que le
   contexte long change (ou ne change pas) dans les couches compressées.

## Ce qui reste, nommé

- **Le SIMD du produit scalaire** reste écarté (il réassocie) : décision
  inchangée depuis le bloc 15, et elle a un prix (une partie du poste d'experts).
- **Les autres formats de grille** n'ont pas de noyau vectorisé.
- Le **cache RAM d'experts** (bloc 16) reste éteint et documenté.

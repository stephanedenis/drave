# Sprint 18 — Vectoriser la DÉQUANTIFICATION des experts (grille Q2_K) sans changer un bit

- **Début** : 23:44 · **Fin prévue** : 01:44 (boxing de 120 min)
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

## Portes

- `tools/portes.sh rapide` : voir le journal du bloc — la porte **V4-Flash
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

## Planning du bloc 19 — le même noyau pour IQ1_M (l'autre modèle lourd)

V4.1 est servi (Q2_K vectorisé, ×3,54 sur la nuit) ; **V4-Flash non** : ses
experts sont en IQ1_M, un format à codebook qui passe encore par
`formats::dequant_iq1m_dans` (mesuré : `proj+mlp` 2 024,50 ms/token, du même ordre
que V4.1 avant son noyau).

1. **Lire le décodage IQ1_M** et dire ce qui est vectorisable : la table de
   codebook se lit **par valeur** (un `gather` serait plus lent qu'un scalaire),
   mais l'application du **signe**, de l'**échelle** et le **produit** sont
   vectorisables sans réassocier — et le pas par groupe peut être hoisté comme
   pour Q2_K.
2. **Mesurer la part exacte** de la conversion dans IQ1_M (même ablation qu'au
   bloc 17) avant d'écrire quoi que ce soit : le plafond du noyau doit être connu
   d'avance, c'est la leçon du bloc 18.
3. **Prouver** : `cargo test`, porte V4-Flash **8430,4966** inchangée, vides
   identiques au bit près, puis publier le gain.

## Ce qui reste, nommé

- **Le SIMD du produit scalaire** reste écarté (il réassocie) : décision
  inchangée depuis le bloc 15, et elle a un prix (une partie du poste d'experts).
- **Les autres formats de grille** n'ont pas de noyau vectorisé.
- Le **cache RAM d'experts** (bloc 16) reste éteint et documenté.

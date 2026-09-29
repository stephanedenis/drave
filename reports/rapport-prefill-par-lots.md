# Préremplissage par lots : ce que le GEMM apporte vraiment

> Chantier 4 du plan de reprise. Le préremplissage est le mur n° 1 du contexte
> long (`docs/contexte-long.md` : 4,5 h à 32 k, 1 234 h à 1 M en séquentiel) : le
> moteur traitait **un jeton à la fois**, donc chaque matrice de poids était relue
> pour chaque jeton.

## 1. Ce qui a été fait

| pièce | rôle |
|---|---|
| `Pool::gemm_dense_i8` | produit matrice-matrice int8 : une tranche de lignes par fil, tout le lot servi par la même lecture de ligne |
| `Pool::gemm_dense_q4` | même chose pour les matrices 4 bits (experts MXFP4 de gpt-oss, Q4_K de Qwen) |
| `Model::forward_lot` | un avant complet pour `t` jetons : projections en lot, attention toujours par jeton (elle est causale), FFN dense en lot |
| **regroupement des experts** | les jetons qui ont choisi le même expert sont traités ensemble : la matrice de l'expert est lue une fois pour le groupe |
| `--lot N` | taille du lot (1 = chemin historique jeton par jeton) |

## 2. Justesse

Trois bogues ont été trouvés par la comparaison au chemin jeton par jeton, tous
invisibles à la compilation :

1. les sorties de q, k et v partageaient un tampon avec des pas différents
   (`n_q` contre `n_kv × dim`) : perplexité mesurée **1 614 183** ;
2. l'entrée de la projection de sortie était dimensionnée sur `hidden`
   (2 880) au lieu de `n_têtes × dim_tête` (4 096) : panique à l'index ;
3. les tampons du lot étaient alloués à chaque couche et à chaque lot.

Et un bogue **latent** du chemin historique, corrigé au passage : le biais de
`ffn_down_exps` était découpé par la largeur d'expert (`n_ff`) au lieu de la
largeur de sortie (`h`). Les deux valent 2 880 sur gpt-oss, donc rien ne se
voyait ; sur Qwen3-MoE (768 contre 2 048) le biais aurait été lu au mauvais
endroit. **Effet mesuré : nul** sur Qwen3-30B-A3B (7,6139 avant comme après — ce
modèle ne déclare pas de biais de descente).

Après correction, les lots donnent la même perplexité que le jeton par jeton :

| modèle | lot 1 | lot 16 |
|---|---|---|
| Qwen2.5-0.5B (dense) | 13,1368 | **13,1359** |
| gpt-oss-120b (MoE, regroupé) | 13,7149 | **13,7205** |

L'écart (6e-5 à 4e-4) est l'**ordre des accumulations flottantes**, pas une
erreur : le noyau somme par ligne entière, le chemin historique par tranches.

## 3. Le débit : mesurer, comprendre, corriger

Première mesure, machine au calme, Qwen2.5-0.5B, 511 jetons notés :

| lot | temps |
|---|---|
| 1 | **16,6 s** |
| 4 | 23,2 s |
| 16 | 20,0 s |
| 64 | 18,1 s |

Le lot était donc **plus lent** que le jeton par jeton, alors que le noyau est
2,4× plus rapide isolément (test unitaire). Diagnostic : dans le noyau, la boucle
des jetons était **à l'intérieur** de la boucle des lignes de sortie, donc chaque
ligne relisait *tout* le lot d'activations (64 × 896 × 4 = 229 Ko) — 4 864
relectures par projection.

Correction : **tuilage** — un groupe de 16 jetons (8 pour le 4 bits) est traité
avant de passer à la ligne suivante, donc les activations du groupe restent en
cache pendant qu'on parcourt les poids. C'est l'arbitrage classique : la ligne est
relue `t / TUILE` fois, mais chaque relecture sert 16 jetons au lieu d'un.

## 4. Le débit, attribué poste par poste

Le profil du chemin par lots (ajouté pour l'occasion : sans lui, aucun poste
n'était chronométré) donne, par jeton, Qwen2.5-0.5B, contexte 512, 16 fils :

| poste | lot 1 | lot 512 | verdict |
|---|---|---|---|
| projections d'attention | 3,05 ms | **1,49 ms** | le GEMM divise par 2 ✓ |
| attention | 4,05 ms | 8,90 ms | **×2,2** ✗ |
| FFN + projection de sortie | 25,31 ms | 20,92 ms | ÷1,2 seulement |
| **somme** | 33,14 ms | 31,31 ms | −5 % |
| tête + échantillonnage | 8,36 ms | 8,75 ms | inchangé (la tête est par jeton) |
| **total** | 41,5 ms | **40,1 ms** | **−3 %** |

Le mécanisme fonctionne — le produit matrice-matrice divise bien par deux le
temps des projections — mais **il ne porte que sur 8 % du coût par jeton**, et
deux postes l'annulent :

1. **l'attention par lots est deux fois plus lente** : elle emprunte le chemin
   par tête, alors que le chemin jeton par jeton utilise le chemin *groupé* qui
   relit les clés une fois par groupe de têtes KV (`rep` = 7 sur Qwen) ;
2. **la tête de sortie reste calculée jeton par jeton** (145 Mo lus par jeton
   pour Qwen 0.5B) : c'est le premier consommateur après le FFN, et il n'est
   même pas dans le lot.

Conclusion, mesurée : pour que le préremplissage par lots tienne ses promesses,
il faut **aussi** (a) passer l'attention par le chemin groupé dans le chemin par
lots, et (b) **traiter la tête comme un GEMM** — même noyau, sortie de
151 936 lignes, trente fois plus de travail que les projections d'attention.
Sans (b), le préremplissage restera dominé par la tête et le FFN.

### 4.bis Les deux suites annoncées, faites et mesurées (réponse à la §4)

Les deux manques de la §4 sont comblés :

* **(a) attention groupée dans le lot** : dans `forward_lot`, les clés et valeurs
  sont déquantifiées **une fois par groupe de têtes KV** (§ `rep` = 7 sur Qwen)
  et non une fois par couple (tête, jeton) ; les scores du groupe partagent un
  tampon `nh × ctx` ;
* **(b) tête de sortie en lot** (`Model::logits_lot`) : les `t` états cachés sont
  quantifiés une fois, puis parcourus **par tuiles de 16 jetons** — la ligne de
  poids reste en cache pendant qu'elle sert les 16 jetons.

Qwen2.5-0.5B Q8_0, contexte 512, 511 jetons notés, 16 fils, `--dense` :

| poste (ms/jeton) | lot 1 | lot 512 | verdict |
|---|---|---|---|
| projections d'attention (q, k, v) | 2,58 | **0,99** | ÷2,6 ✓ |
| rope | 0,46 | (compté dans l'attention) | — |
| attention | 2,78 | 5,59 | **×1,7** ✗ reste le point noir |
| projection de sortie + FFN | 20,75 | **14,54** | ÷1,43 |
| **somme** | 26,57 | **21,13** | ÷1,26 |
| tête de sortie seule | ~5,63 | **5,47** | ≈ inchangé — voir ci-dessous |
| notation log-sum-exp | 1,38 | 1,38 | inchangé (par jeton) |
| **total** | 34,5 | **28,2** | **−18 %** |

Bout en bout, sans profil (qui ajoute ses propres horloges) : **17,1 s → 13,6 s,
soit −20 %**, à perplexité identique (13,1368 → 13,1359). Sur gpt-oss (MoE
regroupé par expert, contexte 256, 255 jetons) : lot 1 ≈ 50 s, lots 64/128/256 =
**33,7 / 33,9 / 34,4 s**, perplexité 13,7205 dans tous les cas.

Trois enseignements, tous mesurés :

1. **La tête en lot ne gagne rien** (5,47 contre ~5,63 ms/jeton). L'argument de
   la §4 — « 145 Mo lus par jeton » — est un argument de *bande passante*, et il
   ne s'applique pas : le noyau Q8_0 de la tête (`gguf::q8_dot_at`) est **lié au
   calcul**, pas à la mémoire (151 936 lignes × 896 produits par jeton, en
   scalaire). Le tuilage supprime bien les relectures, mais elles n'étaient pas
   le coût dominant. Ce qu'il faut pour la tête, c'est un noyau vectorisé AVX2 ou
   le déport GPU (`QT_GPU_TETE=1`, déjà mesuré à 6,2 ms/jeton contre 15,6 pour
   tête + échantillonnage sur gpt-oss), pas un lot plus gros.
2. **L'attention par lots reste 1,7 fois plus lente** que le chemin par jeton
   (5,59 contre 2,78 + 0,46 ms). Le groupement des KV a divisé le coût, mais il
   reste un surcoût propre au lot.
3. Le gain réel vient des **grosses matrices mémoire-liées** : projections
   ÷2,6 et FFN/wo ÷1,43. C'est exactement ce que la §2 annonçait, et c'est
   pourquoi le lot paie sur un modèle à vocabulaire énorme mais FFN mince
   (Qwen 0.5B) comme sur un MoE de 120 B.

### 4.ter Un pointeur gras, un blocage muet

Le lot 128 faisait tomber le programme sur :

```
thread '<unnamed>' panicked at src/engine.rs:473:77:
index out of bounds: the len is 90 but the index is 90
```

`90` = nombre de blocs de 32 d'un jeton (2 880 / 32), pas le nombre de jetons du
lot. Cause : le tableau des sommes par bloc, `&[Vec<i32>]`, était publié dans un
`AtomicPtr<Vec<Vec<i32>>>` par un **pointeur de tranche (gras)** puis relu comme
un `Vec<Vec<i32>>`. La longueur relue était donc celle du **premier jeton**
(90 blocs) et le pointeur de données celui de ses sommes : tout allait bien tant
que le lot restait sous 90 jetons (les noyaux MXFP4 ignorent ces sommes, d'où
des résultats justes malgré la lecture fantôme), et au-delà, dépassement de
borne chez un worker.

Pire que la panique : **elle ne se voyait pas**. Le worker mourait sans rendre
son jeton et le fil principal tournait indéfiniment sur `done` — dix minutes
d'attente active au lieu d'une erreur (même classe de panne que le blocage de
27 minutes raconté dans `REPRISE.md`). Deux correctifs, dans cet ordre :

1. `Shared::gs32` est un pointeur **fin** vers `Vec<i32>` ; le worker
   reconstruit la tranche avec la longueur du lot (`from_raw_parts(ptr, t)`).
   Un test le verrouille : `tests_gemm_q4` fait tourner des lots de 1, 8, 9, 17
   et 40 jetons sur une matrice de 256 colonnes — soit des lots **plus grands
   que le nombre de blocs (8)** — et compare au chemin jeton par jeton.
2. Toute génération de travail est passée sous `catch_unwind` : un worker qui
   panique incrémente `Shared::morts`, et l'attente commune (`Pool::attendre`)
   **panique à son tour avec un message clair** au lieu de boucler. Vérifié en
   réintroduisant le bug : le test échoue en quelques secondes avec
   « un worker du pool est mort pendant le calcul (panique ci-dessus) » là où il
   tournait auparavant indéfiniment.

## 5. Ce que ça change pour le contexte long

Le préremplissage séquentiel coûtait un parcours complet des poids **par jeton**.
Un lot de `t` jetons ne le coûte plus qu'une fois par groupe de 16 (et une fois
par expert et par groupe pour un MoE) : le facteur à gagner est donc de l'ordre
de 16 sur la partie « projections », qui domine le préremplissage.

Mesuré, avec les deux suites de la §4 et le correctif de la §4.ter en place :

| machine / modèle | contexte | lot 1 | lot 512 | gain |
|---|---|---|---|---|
| Qwen2.5-0.5B Q8_0, `--dense`, 16 fils | 512 | 17,1 s | **13,6 s** | **−20 %** |
| gpt-oss-120b MXFP4, MoE groupé, 16 fils | 256 | ≈ 50 s | 34,4 s (lot 256) | **−31 %** |

Perplexité inchangée dans les deux cas (13,1368 → 13,1359 ; 13,7149 → 13,7205),
et la porte de non-régression Qwen contexte 256 reste à **19,3885**.

Ce qui reste sur la table, dans l'ordre de rentabilité : **le noyau de la tête**
(vectorisation AVX2 ou déport GPU — le lot n'y change rien, §4.bis), **l'attention
par lots** (1,7 × le chemin par jeton), puis le FFN dense (÷1,43 seulement, la
part `wo` étant déjà à son plancher mémoire).

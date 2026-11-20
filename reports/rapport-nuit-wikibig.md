# La nuit du 19-20/11 : `wiki_big` seul, 110 000 pas — le corpus de 1 Go qui bat le mélange

> **Ligne de roadmap** : N (le palier 1) · **Date** : 19-20/11 · **Verdict** : ✅ mesuré — deux
> chaînes de 11 tranches de 10 000 pas (lr 1e-4, AMP, `d=896`, graine 1) : **`wiki_big` seul**
> (831 Mo) et le **long-forme** (les lignes ≥ 200 o du plein texte, 4,79 Go, épinglé `a50f6045…`).
> À 110 000 pas : `wiki_big` **6,8349** sur wikitext2 (PPL val de v1 **2,9102**), le long-forme
> **7,7479** (3,1525). `wiki_big` seul fait donc **mieux que le mélange v1** (6,867) et **que le
> plein texte v2** (7,093), avec 1 Go et 1/7 de leur donnée.
>
> **Dispositif** : `bench/chaine_nuit.sh` (10 000 pas + banc + grammaticalité + **PPL wikitext2**
> après chaque tranche) · le corpus long-forme est extrait par `tools/extraire_lignes_longues.py`
> (4,79 Go, 464 o/ligne) et épinglé (`12e4620d…`) · le val tiers est `data/wikitext2_test.txt`
> (352 256 jetons).

## Les courbes

| pas | `wiki_big` wikitext2 / PPL v1 | long-forme wikitext2 / PPL v1 |
|---:|---|---|
| 10 000 | 8,8598 / 3,5277 | 9,9360 / 3,6727 |
| 20 000 | 7,8340 / 3,2334 | 8,4990 / 3,4124 |
| 30 000 | 7,3531 / 3,1196 | 8,1943 / 3,2969 |
| 40 000 | 7,1105 / 3,0419 | 7,9337 / 3,2371 |
| 50 000 | 6,9299 / 2,9942 | 7,8008 / 3,1691 |
| 60 000 | 6,8916 / 2,9547 | 7,6831 / 3,1607 |
| 70 000 | 6,8566 / 2,9426 | 7,6300 / 3,1393 |
| 80 000 | 6,8590 / 2,9327 | 7,6053 / 3,1428 |
| 90 000 | **6,8072 / 2,9203** | 7,6991 / 3,1454 |
| 100 000 | 6,8448 / 2,9167 | 7,7758 / 3,1476 |
| 110 000 | **6,8349 / 2,9102** | **7,7479 / 3,1525** |

## Les lectures (à confirmer sur les deux dernières tranches)

1. **`wiki_big` seul est au niveau du mélange et devant le plein texte** : **6,8349** à 110 000 pas,
   contre **6,867** pour le 150 M v1 de la nuit dernière et **7,093** pour v2. L'écart avec v1
   (−0,5 %) est **dans la variance** du run-à-run (±1,8 %, voir plus bas) ; l'écart avec v2
   (−3,6 %) en sort. Sa meilleure tranche est 90 000 pas (6,8072).
2. **Le long-forme ne suit pas** : filtrer les lignes longues du plein texte (4,79 Go) donne 7,60-7,70
   — la longueur des lignes n'est pas le critère ; la préparation de `wiki_big` (un corpus « propre »,
   filtré, à 407 o/ligne) fait autre chose.
3. **La variance du run-à-run** : le rejeu de `wiki_big` à 30 000 pas donne 7,3531 contre 7,2237
   l'après-midi (**±1,8 %**), alors que le pas 1 est bit-identique — la dispersion vient de
   l'entraînement (non-déterminisme GPU). Les écarts de moins de 2 % ne sont pas significatifs ;
   c'est pourquoi `wiki_big` vs v1 est un **match nul** plutôt qu'une victoire, et v2 (7,09) est le
   seul 150 M clairement derrière.

## Ce qui pourrait le rendre faux

- **Une graine, un val** : les écarts de 1-2 % sont dans la variance mesurée (±1,8 %) ; l'écart
  `wiki_big`/v1 (6,81 vs 6,87) est à la limite, et seul le long-forme (7,70) est clairement hors.
- **Le val tiers est du Wikipédia** : les trois corpus en viennent ; le val mesure un style
  d'extraction autant qu'un contenu.
- **`wiki_big` est petit** (831 Mo) : à 110 000 pas il a vu ~1,1 époque ; le comparer à un corpus de
  6,9 Go à pas égal n'est pas un test d'échelle, c'est un test de **sélection**.

## Voir aussi

- [la sélection du contenu](rapport-selection-contenu.md) · [le corpus v2](rapport-corpus-v2.md) ·
  [la courbe de la nuit dernière](rapport-150m-nuit.md) · [les données](courbe-150m.json)

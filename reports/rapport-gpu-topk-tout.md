# Le top-k GPU : le noyau fusionné gagne jusqu'à ~64 k clés, la chaîne séparée au-delà

> Banc `--banc-topk` (Qwen2.5-0.5B-Q8_0, **14 lignes** — 2 têtes KV × 7 têtes de requête —, `hd` 64, KV 8 bits,
> k = 256), le 24/10/2026. Le binaire est celui du dépôt (`target/release/drave`), non modifié pour la mesure.

## La question

Le plan `docs/plan-gpu-topk.md` pariait sur **une fusion** : réduire les **8 lancements et 17 transferts** par
couche et par jeton de la chaîne séparée (histogramme ×4, comptage, écriture, somme) à **un seul noyau** — la
descente radix, la collecte et la somme dans un bloc par ligne, les k scores vivant en partagé. Le noyau
(`attn_topk_tout`) existe, est branché dans `model.rs` en opt-in (`DRAVE_GPU_TOPK=1`), et conforme au contrat
d'exactitude. Restait **la mesure du gain** : la fusion est-elle le levier ?

## Les résultats

Temps par appel, en ms, sur les mêmes tampons (le GPU est un Quadro RTX 5000 ; la référence CPU est l'attention
complète, 14 fils) :

| n (clés) | **noyau fusionné** | chaîne séparée | CPU complet | vainqueur |
|---:|---:|---:|---:|---|
| 4 096 | **0,14** | 0,27 | 3,69 | fusionné (×1,9) |
| 8 192 | **0,16** | 0,26 | 9,15 | fusionné (×1,6) |
| 16 384 | **0,19** | 0,30 | 12,46 | fusionné (×1,6) |
| 32 768 | **0,29** | 0,35 | 30,97 | fusionné (×1,2) |
| 65 536 | **0,44** | 0,49 | 36,66 | fusionné (×1,1) |
| 131 072 | 0,87 | **0,79** | 71,10 | chaîne (×1,1) |
| 262 144 | 1,57 | **1,27** | 143,47 | chaîne (×1,24) |
| 1 048 576 | 5,86 | **4,10** | 483,68 | chaîne (×1,43) |

Les écarts d'exactitude restent sous le critère (1e-6) partout : 7,0e-7 à 262 k, 9,7e-7 à 1 M pour le fusionné
(il frôle le critère sans le franchir), 2,7-4,8e-7 pour la somme de la chaîne.

## Ce que ça dit

- **Le noyau fusionné gagne jusqu'à ~64 k clés** (×1,1 à ×1,9), et **la chaîne séparée gagne au-delà**
  (×1,1 à ×1,43). Le croisement est **mesuré**, entre 65 k et 131 k.
- **La fusion n'est pas le levier universel** que le plan espérait : elle paie là où le **coût fixe** des lancements
  et des transferts domine (petit n) ; au-delà, c'est le **parallélisme de la grille** qui commande — 1 792 blocs
  pour la chaîne contre **14 blocs** (un par ligne) pour le fusionné, qui n'occupent que 14 des 48 SM.
- **Le seuil du modèle est donc mesuré, pas choisi** : `SEUIL_NOYAU4 = 131_072` dans `model.rs` — le fusionné en
  dessous, la chaîne au-dessus. À la frontière (131 k), les deux mesures se croisent à ±10 % : le choix n'est pas
  critique.
- **Le critère de l'axe A2.5 est tenu** : le top-k déporté ne retombe plus sur le CPU (en opt-in), et le mode creux
  est utilisable à 1 M (5,86 ms par couche pour le fusionné, 4,10 pour la chaîne, contre **483,68 ms** au CPU —
  ×83 à ×118).

## Ce que ça change dans le plan

La section « la prochaine étape n'est pas un noyau de plus, c'est une fusion » est **faite et mesurée** — mais son
pronostic est **partiellement faux** : la fusion ne supprime pas le besoin de la chaîne séparée, elle la **complète**
en dessous de ~100 k. La vraie conclusion est une **politique par taille**, pas un noyau unique.

## Ce que ce résultat ne dit pas

- La forme du modèle compte : le 0,5 B a **2 têtes KV × 64** ; un 7 B (4 × 128) ou un 14 B déplacent le coût par
  ligne et peut-être le croisement — non mesuré ici.
- Le banc mesure le **noyau**, pas la perplexité de bout en bout au-delà de 2 048 clés : le chemin complet
  (`--ppl` à long contexte) n'a pas été refait.
- Les temps incluent les transferts du banc, pas ceux du moteur par couche et par jeton ; la comparaison CPU/GPU
  est l'attention complète, pas le top-k CPU seul.

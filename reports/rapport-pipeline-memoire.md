# B17 — M7-bis dans la chaîne : LFU aide la mémoire, pas M8

> **Objet.** Brancher `MemoireFrequence` (B16) entre M1 et M8, sur le flux 528 (préfixe 422,
> suffixe 106), et mesurer la couverture. Résultat : **LFU retient mieux** que FIFO/LRU, mais
> **M8 sur les codes retenus est un lookup** ; la généralisation reste **0**.

## Résultats (30 permutations, capacité 16)

| politique | suffixe surface | suffixe code | codes en mémoire |
|---|---:|---:|---:|
| FIFO | 5,03 % | 71,70 % | 16 |
| LRU | 5,94 % | 71,89 % | 16 |
| **LFU** | **9,28 %** | **74,69 %** | 16 |

**LFU** double presque le suffixe surface de FIFO (+4,25 pts) et gagne +3,0 pts de suffixe code.
C'est le même effet que B16, retrouvé dans la chaîne.

## M8 après la mémoire

| mesure | valeur |
|---|---:|
| prototypes | **6** |
| suffixe | 106 |
| codes couverts | **75** |
| couverture | **70,75 %** |
| exact sur couverts | **100 %** (lookup) |
| généralisation | **0 %** |

**Lecture** : M8 sur les codes que la mémoire a retenus est un **lookup exact** ; il ne peut rien
dire des 31 codes non couverts. La couverture (70,75 %) est la seule mesure utile ; le **100 %**
sur couverts est tautologique.

## Verdict

- **LFU est une bonne politique de mémoire bornée** : +4,25 pts de suffixe surface, +3,0 pts de
  suffixe code.
- **M8 n'ajoute rien** : sur les codes retenus, c'est un lookup ; sur les non couverts, 0 %.
- La mémoire ne remplace pas la consolidation ; elle **filtre** ce que M8 peut voir.

## Limites

- 30 permutations, un corpus, capacité 16 : le suffixe est petit (106).
- M8 est évalué sur les codes de la mémoire, pas sur des codes tenus à l'écart ; le 100 % est
  tautologique.
- LFU privilégie les répétés ; les one-shot sont perdus (B16 : −0,67 pt sur les nouveaux du suffixe).

## Fichiers

- Code : [`tools/cerveau/pipeline_memoire.py`](../tools/cerveau/pipeline_memoire.py).
- Test : [`tools/cerveau/tests/test_pipeline_memoire.py`](../tools/cerveau/tests/test_pipeline_memoire.py).
- JSON : [`pipeline-memoire.json`](pipeline-memoire.json).

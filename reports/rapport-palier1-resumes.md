# Le palier 1 : les résumés Wikipédia, 3,69 Go — à 20 000 pas, il mène `wiki_big`

> **Ligne de roadmap** : N · **Date** : 2026-11-20 · **Verdict** : *(tranche 30 000 en cours)* — le
> corpus du palier 1 (les **résumés** de `frwiki_v14`, `n_chars >= 300`, **3,69 Go**, épinglé
> `469a6d78…`) est entraîné à **deux graines** (GPU 0 et 1), 3 tranches de 10 000 pas, mêmes juges.
> À 20 000 pas, il rend **7,7017 / 7,9700** sur wikitext2, contre **7,8340 / 8,1700** pour
> `wiki_big` — il **mène légèrement**, mais l'écart (1-2 %) est dans la variance des graines.

## Les tranches

| pas | palier 1, graine 1 (p1) | palier 1, graine 2 (p2) | `wiki_big`, g1-g3 |
|---:|---|---|---|
| 10 000 | 9,0631 / 3,5299 | 8,7014 / 3,4922 | 8,78-9,50 / 3,51-3,57 |
| 20 000 | 7,9700 / 3,2572 | **7,7017 / 3,2196** | 7,83-8,17 / 3,23-3,29 |
| 30 000 | *(en cours, ≈ 16 h 30)* | *(en cours)* | 7,22-7,56 / 2,92-3,12 |

*(wikitext2 / PPL du val de v1)*

## Ce que ça dit déjà

1. **Le registre compte plus que le volume** : `wiki_big` (831 Mo) et le palier 1 (3,69 Go) sont
   **les mêmes résumés**, et leurs courbes sont dans la même bande — le second mène de 1-2 % à 20k,
   pas de quoi crier victoire.
2. **La variance domine** : avec un écart-type de 1,8 % et une étendue de 4,7 % à 30 000 pas, un
   écart de 1-2 % entre corpus **ne tranche pas** — c'est la leçon de la fiche de variance.
3. **Le 30 000 pas est le point utile** (il tombe vers 16 h 30) : c'est là que les deux graines du
   palier 1 se comparent aux quatre mesures de `wiki_big`.

## Ce qui pourrait le rendre faux

- La variance des graines (±1,8 % d'écart-type) dépasse l'écart mesuré.
- Un seul val tiers (wikitext2) ; le val de v1 est du même registre (les résumés).
- La 3e tranche n'est pas finie : tout peut encore bouger.

## Voir aussi

- [le corpus du palier 1](rapport-corpus-palier1.md) · [la variance](rapport-variance-graines.md) ·
  [la sélection](rapport-selection-contenu.md) · [la nuit](rapport-nuit-wikibig.md)

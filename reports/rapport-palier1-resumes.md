# Le palier 1 : les résumés Wikipédia, 3,69 Go — à 20 000 pas, il mène `wiki_big`

> **Ligne de roadmap** : N · **Date** : 2026-11-20 · **Verdict** : ✅ mesuré — à 30 000 pas, le
> palier 1 rend **7,2790 / 7,7044** contre **7,22-7,56** pour `wiki_big` : **le léger avantage de
> 20 000 pas ne tient pas**, les deux corpus du même registre se valent **dans la variance** (4,7 %).
>
> Le
> corpus du palier 1 (les **résumés** de `frwiki_v14`, `n_chars >= 300`, **3,69 Go**, épinglé
> `469a6d78…`) est entraîné à **deux graines** (GPU 0 et 1), 3 tranches de 10 000 pas, mêmes juges.
> À 20 000 pas, il rend **7,7017 / 7,9700** sur wikitext2, contre **7,8340 / 8,1700** pour
> `wiki_big` — il **mène légèrement**, mais l'écart (1-2 %) est dans la variance des graines.

## Les tranches

| pas | palier 1, graine 1 (p1) | palier 1, graine 2 (p2) | `wiki_big`, g1-g3 |
|---:|---|---|---|
| 10 000 | 9,0631 / 3,5299 | 8,7014 / 3,4922 | 8,78-9,50 / 3,51-3,57 |
| 20 000 | 7,9700 / 3,2572 | **7,7017 / 3,2196** | 7,83-8,17 / 3,23-3,29 |
| 30 000 | **7,7044 / 3,1486** | **7,2790 / 3,0874** | 7,22-7,56 / 2,92-3,12 |

*(wikitext2 / PPL du val de v1)*

## Ce que ça dit déjà

1. **Le registre compte plus que le volume** : `wiki_big` (831 Mo) et le palier 1 (3,69 Go) sont
   **les mêmes résumés**, et leurs courbes se confondent — 4,4× plus de données n'achète pas de
   généralisation mesurable à pas égal.
2. **La variance domine** : l'étendue des graines (4,7 % à 30 000 pas) recouvre l'écart entre les
   deux corpus (7,28-7,70 contre 7,22-7,56) — le palier 1 **ne se distingue pas** de `wiki_big`.
3. **Ce qui reste vrai** : ni le plein texte (7,09-7,75) ni `wiki_fr` (8,09) n'atteignent cette
   bande — la **sélection du registre** (les résumés préparés) est le fait solide de la semaine.

## Ce qui pourrait le rendre faux

- La variance des graines (±1,8 % d'écart-type) dépasse l'écart mesuré.
- Un seul val tiers (wikitext2) ; le val de v1 est du même registre (les résumés).
- La 3e tranche n'est pas finie : tout peut encore bouger.

## Voir aussi

- [le corpus du palier 1](rapport-corpus-palier1.md) · [la variance](rapport-variance-graines.md) ·
  [la sélection](rapport-selection-contenu.md) · [la nuit](rapport-nuit-wikibig.md)

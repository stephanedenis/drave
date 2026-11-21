# Le corpus du palier 1 : les résumés Wikipédia, 3,69 Go à 753 o/ligne

> **Ligne de roadmap** : N · **Date** : 2026-11-20 · **Verdict** : le corpus du palier 1 est
> construit — les **résumés** de la base `frwiki_v14` (2 755 035 articles), filtre `n_chars >= 300`,
> dédupliqués et découpés : **3,69 Go**, **4 899 962 lignes**, **753 o/ligne**. C'est le registre de
> `wiki_big` (qui gagne la sélection), **pas** le plein texte : la nuit du 19-20/11 a montré que les
> lignes longues du plein texte (7,75 sur wikitext2) ne valent pas les résumés préparés (6,83).
>
> **Dispositif** : `tools/corpus_wikipedia.py --db frwiki_v14.db --min-chars 300 --val 0.02
> --test 0.01` ; épinglé `469a6d78…` (manifeste `f0ff49d7…`), val 76,4 Mo, test 38,2 Mo ;
> manifeste du corpus [`corpus-wiki-fr-palier1.json`](corpus-wiki-fr-palier1.json).

## Le tableau

| quoi | valeur |
|---|---:|
| articles lus / gardés | 2 755 035 / ~2,75 M |
| octets train | **3 691 727 067** |
| lignes train | 4 899 962 |
| octets par ligne | **753** |
| val / test | 76,4 / 38,2 Mo |

## Ce qui pourrait le rendre faux

- Le filtre `n_chars >= 300` garde les articles longs (753 o/ligne contre 407 pour `wiki_big`) :
  le corpus n'est pas un tirage uniforme des résumés, c'est le **haut** du registre.
- La déduplication des tronçons retire les doublons de résumés — le volume « brut » est plus grand.
- Le registre reste les **résumés** : la même limite que `wiki_big` (une prose de lead, pas
  l'article entier).

## Voir aussi

- [la sélection du contenu](rapport-selection-contenu.md) · [la nuit `wiki_big`](rapport-nuit-wikibig.md) ·
  [le corpus v2](rapport-corpus-v2.md)

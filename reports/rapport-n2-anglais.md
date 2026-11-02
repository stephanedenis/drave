# N2.m — L'anglais seul : 4,42 sur 204 Mo, et ce que le multilingue coûte (1,6 PPL)

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : la base **anglaise
> monolingue** (204,6 Mo, 120 000 articles) vaut **4,4234** sur sa validation, **4,6739** sur la
> validation du multilingue (transfert de gamme) et **5,2967** sur le banc anglais ; la base à
> **10 langues** (21 Mo d'anglais) vaut **6,1152 / 6,3024 / 7,0461** sur les mêmes textes. Le
> monolingue est meilleur de **1,6 à 1,7 PPL** — le même coût de dilution que le français.

## La question

N2.k avait mesuré le coût du multilingue **vu du français** (+57 %, +0,65 bit/octet). La question
symétrique : que vaut l'**anglais seul**, et le multilingue est-il un bon compromis pour l'anglais ?
Le plan de travail demandait « N2 sur les corpus wiki fr/**en** » : voici l'anglais.

## Le dispositif

- **Corpus anglais** : 120 000 articles (`enwiki_v14`, page_ids 300 000+), 230,6 Mo bruts,
  dédupliqués à 1,44 % → **204,6 Mo** d'entraînement, 11,0 de validation, 0/100 contaminées.
- **Base** : 11,47 M, 20 000 pas × 8 × 128, lr 3e-4, graine 1, **positions aléatoires [0, 384]**.
- **Comparaisons** : la base à 10 langues (N2.k, 21 Mo d'anglais) et le banc anglais du protocole.

## Ce qui est mesuré

| modèle | val wiki_en (sa gamme) | val du multilingue | banc anglais | wikitext2 |
|---|---:|---:|---:|---:|
| **anglais seul** (204,6 Mo) | **4,4234** | **4,6739** | **5,2967** | **5,5607** |
| **10 langues** (21 Mo d'anglais) | 6,1152 | 6,3024 | 7,0461 | 7,3391 |
| écart | **−1,69** | **−1,63** | **−1,75** | **−1,78** |

Courbe de longueur (anglais seul) : **4,42 / 4,49 / 4,72 / 5,55 / 6,60** à 129/192/256/384/512.

## Lecture

Le monolingue **gagne partout** de 1,6 à 1,8 PPL — sur sa gamme, sur la gamme du multilingue (un
transfert), et sur le banc externe. C'est la même loi que pour le français : à 11,47 M, **dix
langues coûtent ~1,6 PPL par langue** (0,7 bit/octet environ).

La courbe de longueur de l'anglais (4,42 → 6,60 à 512) montre le même plafond que le français
(4,39 → 5,78) : la fenêtre locale de 256 octets, pas la position.

## Ce que ça change pour N2

- **Pour la ligne R** (lire des documents) : le multilingue est un **choix**, pas une évidence —
  un modèle par langue est meilleur, un modèle à 10 langues est plus petit en tout. La décision
  dépend du budget de paramètres : à 11,47 M, on paie 1,6 PPL par langue ; à 21,65 M (N2.j3, où la
  capacité paie sur le corpus réel), le coût serait probablement plus faible.
- **Pour la porte N2** (le français) : l'anglais seul ne la concerne pas, mais il donne un point de
  comparaison : le français seul (3,76 sur sa gamme) est plus facile que l'anglais seul (4,42).

## Ce qui pourrait le rendre faux

- **Gammes de pages différentes** : la validation du multilingue (page_ids 200k-212k) n'est pas
  dans la gamme d'entraînement de l'anglais seul (300k+) ; c'est un transfert, pas un test en
  domaine — mais l'écart est le même sur la validation en domaine.
- **Une seule graine, 20 000 pas** (10 % du corpus) : ni convergence ni intervalle.
- **Le texte est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Extraction : `work/n2k/extrait_en.py` ; corpus : `data/wiki_en/`, manifeste
  [`corpus-wiki-en-propre.json`](corpus-wiki-en-propre.json).
- Points de contrôle : `work/n2k/base-en.pt` ; mesures : `work/n2k/eval-en.json`,
  `eval-multi-en.json`, `eval-en-sur-multi.json`.

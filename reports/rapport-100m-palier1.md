# Le 100 M sur le palier 1 (3,44 Go) — le test de la donnée

> **Ce que ce document est.** Le run du **100 M sur le corpus `corpus_wiki_fr_palier1` (3,44 Go)**
> — le vrai test du palier 1, avec **27 tokens/paramètre** au lieu des 30 du run sur 1 Go.
> L'hypothèse, écrite d'avance : sur 3,44 Go, le 100 M **ne sur-apprend pas** et donne
> **mots > 0,85, répétition ≤ 5, non-UTF-8 ≈ 0, PPL < 2,5**. Le run est lancé le 22/11 à 02 h 15.

## 1. Le dispositif

| réglage | valeur |
|---|---|
| corpus | `data/corpus_wiki_fr_palier1/train.txt` (3,44 Go) |
| le canal | **absent** (le corpus n'a pas de `train.canal` — le run tournera sans la structure) |
| les pas | 30 000 |
| le lot | 8 × 1 024 |
| le modèle | 100 M (d_model 640, 8 blocs, expert 640) |
| l'optimisation | AMP, sans les 9 têtes précoces |
| le GPU | une RTX 5000, 5,5 Go de VRAM, 99 % |
| l'ETA | **~2 h 25** (04 h 40) |

## 2. Ce qui est mesuré (à la fin)

1. **la PPL de validation** (le val du corpus, 73 Mo) ;
2. **le banc 612** (le même que les trois autres checkpoints) ;
3. **le taux de non-UTF-8** (la mesure qui discrimine) ;
4. **le contrôle négatif** (déjà fait : poids aléatoires = 0,711 de mots et 60/60 non-UTF-8).

## 3. Ce qui pourrait rendre le test faux

- **Le canal absent** : le run sur `wiki_mix/propre` utilisait un canal de structure ; celui-ci
  n'en a pas. La comparaison avec les autres checkpoints est **partielle** (le canal change le
  signal d'entraînement).
- **Le corpus n'est pas nettoyé** : 3,44 Go de wiki brut — les doublons sont rares (1 pour
  100 000 lignes mesuré), mais le bruit (titres, liens, articles courts) reste.
- **Le val est le val du corpus** : la PPL n'est comparable qu'au **même découpage** (le val de
  73 Mo de `corpus_wiki_fr_palier1`).

## 4. L'état (le 22/11, 02 h 20)

Le run est à **900 / 30 000 pas**, la PPL de validation à **11,97**, le GPU à 99 %. Le résultat
sera dans ce document à la fin du run.

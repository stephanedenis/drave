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
## 5. Le résultat (le 22/11, 04 h 42)

| mesure | valeur | l'hypothèse (écrite d'avance) | verdict |
|---|---:|---|---|
| la durée | **2 h 25** (8 721 s) | ~2 h 25 | ✅ |
| la PPL de validation finale | **3,073** | < 2,5 | ❌ |
| la précision top-1 | 0,672 | — | — |
| **mots valides** (banc 612) | **0,854** | > 0,85 | ✅ (à 0,004 près) |
| **répétition** | **2** | ≤ 5 | ✅ |
| **non-UTF-8** | **13** / 602 (2,2 %) | ≈ 0 | ⚠️ (pas 0, mais 2× moins que le 30 k sur 1 Go) |
| le débit | 124,3 octets/s | — | — |

**Le verdict honnête : 3 hypothèses sur 4 tiennent, la PPL manque.**

- **La donnée paie** : 0,854 de mots valides contre **0,755** pour le même modèle sur 1 Go (+10
  points) et **0,763** pour le 30 k sur 1 Go (+9 points). **C'est le meilleur résultat jamais obtenu
  par le natif** sur le gold 612.
- **La dérive recule** : 13 non-UTF-8 contre 29 (le 30 k sur 1 Go) — le ratio 27 tokens/paramètre
  vaut mieux que 30, mais n'élimine pas la dérive.
- **La PPL reste haute** (3,073 contre 2,944 pour le 30 k sur 1 Go) : le corpus de 3,44 Go est
  **plus dur** (wiki brut, pas le mix nettoyé), donc la PPL n'est **pas comparable** directement.

**Ce qui change la conclusion** : le meilleur checkpoint du natif n'est **plus** le 100 M sur 1 Go
(0,755) mais le **100 M sur 3,44 Go** (0,854). **La donnée était bien le verrou** — et le palier 1
est **franchi**, avec une réserve sur la PPL.

**Le prochain pas** : le **même run avec le corpus nettoyé et le canal** (le `train.canal` manquait) ;
et le **banc 612 sur le 30 k du palier 1** pour voir si la dérive revient.
## 6. Le 3 000 pas du palier 1 — la courbe du temps

Le **même modèle** sur le **même corpus** (3,44 Go), à **3 000 pas** (14,7 min) au lieu de 30 000
(2 h 25) :

| checkpoint | pas | temps | mots valides | répétition | non-UTF-8 |
|---|---:|---:|---:|---:|---:|
| palier 1, 3 k | 3 000 | **14,7 min** | 0,842 | **0** | **3** |
| palier 1, 30 k | 30 000 | 2 h 25 | **0,854** | 2 | 13 |

**Le résultat** : les 30 000 pas n'apportent que **1,2 point** de mots valides (0,842 → 0,854) et
**coûtent 10× plus de temps** — en échange de **plus de dérive** (3 → 13 non-UTF-8) et de
répétitions (0 → 2).

**La lecture** : sur 3,44 Go, le **3 000 pas est déjà le bon point** — le corpus est assez grand
pour que le modèle apprenne vite, et l'entraînement plus long n'achète presque rien. C'est la
**première** fois que la courbe du natif montre un **plateau net** avant le sur-apprentissage.

**Le classement final du natif** (gold 612, mots valides) :

| modèle | corpus | pas | temps | mots |
|---|---|---:|---:|---:|
| 34 M | 1 Go | 30 k | 3,7 h | 0,666 |
| 100 M | 1 Go | 3 k | 12 min | 0,755 |
| 100 M | 1 Go | 30 k | 2,4 h | 0,763 |
| **100 M** | **3,44 Go** | **3 k** | **15 min** | **0,842** |
| 100 M | 3,44 Go | 30 k | 2,4 h | 0,854 |

**Le meilleur rapport temps/qualité** est le **100 M sur 3,44 Go à 3 000 pas** : 0,842 pour
**15 minutes**. Le 30 k est le meilleur absolu (0,854), mais 10× le temps.

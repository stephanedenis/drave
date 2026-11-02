# B13 — la méta-règle : 25/30, le vote ne bat pas le dernier nom

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **105/105 portes** : le **vote majoritaire** des quatre règles (égalité → dernier nom) fait
> **25/30**. C'est mieux que le rôle (23) et l'hybride (24), moins bien que le **dernier nom**
> seul (**27/30**). Le vote ne dépasse pas la meilleure règle : la **famille rôle** (3 voix)
> écrase la proximité (1 voix) sur les cas ambigus.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-meta.json`](pensee-anaphore-meta.json).

## 1. Les cinq règles

| règle | court (20) | long (10) | **tout (30)** |
|---|---:|---:|---:|
| **dernier nom** | **20** | 7 | **27** |
| rôle | 14 | 9 | 23 |
| hybride | 15 | 9 | 24 |
| sémantique | 15 | 8 | 23 |
| **méta (vote)** | 18 | 7 | **25** |

**Ce que ça dit** :

- **Le vote ne dépasse pas 27** : la famille `role`/`hybride`/`sémantique` vote ensemble
  (κ ≈ 0,9–1,0) et impose sa réponse aux cas ambigus (r321, r322, r323, r327).
- **Il gagne sur les cas courts** (18/20 contre 14–15) mais perd le long (7/10) : le vote est un
  **compromis**, pas un progrès.
- **La meilleure règle reste la plus simple** (27/30) : sur ce gold, la proximité est un
  **signal fort** que le vote dilue.
- **La négative est explicite** : 25/30 < 27/30.

## 2. Ce que ce banc ne dit pas

- **30 liens** ; 100 donneraient une courbe.
- **Un vote pondéré** (règles de poids différents) n'est pas testé.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (30 liens) ;
- **le vote** dépend de la famille de règles (3 vs 1) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Un vote pondéré** : poids appris sur 20 cas, testés sur 10.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre_meta`, `mesurer_meta`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T102, 105/105.
- [`pensee-anaphore-meta.json`](pensee-anaphore-meta.json) — le vote.

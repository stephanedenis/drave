# B13 — le vote pondéré : poids (1,0,0,0), test 7/10

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **106/106 portes** : les **poids** des quatre règles sont appris sur les 20 premiers liens et
> testés sur les 10 derniers. Le meilleur poids est **(1,0,0,0)** : le **dernier nom seul**. Il
> fait 20/20 en apprentissage et **7/10 en test** — le test est le **long**, où la proximité perd.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-pondere.json`](pensee-anaphore-pondere.json).

## 1. Le vote pondéré

| poids | train (20) | test (10) |
|---|---:|---:|
| **(1,0,0,0)** — dernier nom | **20/20** | **7/10** |
| (0,1,0,0) — rôle | ? | ? |
| (1,1,0,0) | ? | ? |

**Ce que ça dit** :

- **Le dernier nom gagne l'apprentissage** (20/20) : sur les cas courts, la proximité est parfaite.
- **Le test est le long** (7/10) : la pondération apprise ne généralise pas ; elle choisit la
  règle qui marche sur le train, pas celle qui marcherait sur le test.
- **Le partage 20/10 est un piège** : les 20 premiers liens sont les courts (r301–r320), les 10
  derniers les longs (r337–r342) ; le « test » n'est pas un échantillon aléatoire.
- **La négative est explicite** : 7/10 en test, malgré 20/20 en train.

## 2. Ce que ce banc ne dit pas

- **30 liens** ; 100 donneraient une courbe.
- **Le partage** n'est pas aléatoire ; c'est la limite de la mesure.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le partage** (20/10 non aléatoire) : c'est la limite principale ;
- **les poids** (grille 0/1/2, pas de réels poids continus) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Un partage aléatoire** : 5 plis croisés ; les poids généralisent-ils ?
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `mesurer_pondere`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T103, 106/106.
- [`pensee-anaphore-pondere.json`](pensee-anaphore-pondere.json) — les poids.

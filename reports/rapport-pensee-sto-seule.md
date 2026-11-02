# B13 — la politique seule sur le bruit : elle réessaie et atteint le but

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **19/19 portes** : la `PolitiqueApprise` entraînée sur la porte **déterministe** est exécutée
> **seule** (sans A*) sur la porte **stochastique** (80 %). Elle **réessaie** quand la porte
> résiste et atteint le but en **8–10 pas** (1–3 essais) sur **15/15 runs**.
>
> **Dispositif** : [`courbe.py`](../tools/pensee/courbe.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-courbe.json`](pensee-courbe.json).

## 1. La politique seule sur le bruit

À l'état `(3,2,False)`, la politique propose `bas` ; la porte s'ouvre avec **80 %** ; en cas
d'échec, l'état reste et la politique **réessaie**. Aucun A*, aucun budget de recherche.

| épisodes | graines | buts seuls | pas | essais | but seul (déterministe) |
|---:|---:|---:|---:|---:|---:|
| 50 | 0,1,2 | **3/3** | 8–10 | 1–3 | 3/3 (8) |
| 100 | 0,1,2 | **3/3** | 8–10 | 1–3 | 3/3 (8) |
| 200 | 0,1,2 | **3/3** | 8–10 | 1–3 | 3/3 (8) |
| 400 | 0,1,2 | **3/3** | 8–10 | 1–3 | 3/3 (8) |
| 800 | 0,1,2 | **3/3** | 8–10 | 1–3 | 3/3 (8) |

**Ce que ça dit** :

- **La politique seule persiste** : elle réessaie (1–3 essais) et atteint le but en 8–10 pas ;
  la Q-table **transfère** du déterministe au bruit.
- **Le coût du bruit est faible** : +1 à +2 pas, +1 à +3 essais ; le chemin reste optimal une
  fois la porte ouverte.
- **15/15 runs** ; les 3 graines ont des essais différents (1, 2, 3) mais toutes réussissent.
- **La Q-table reste petite** (52–83 états) : le bruit ne change pas sa taille, seulement le
  nombre d'essais.

## 2. Ce que ce banc ne dit pas

- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le bruit est indépendant** (80 % à chaque essai) ; une porte qui **apprend** serait plus dure.
- **Le labyrinthe 5×5** est un jouet ; 8–10 pas, 1–3 essais.
- **Le coût 5** de la sonde n'intervient pas ici (la politique seule ne paie pas le moteur).

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (3 graines, 15 runs, toutes réussissent) ;
- un **A* caché** dans `seule_sto` (non : la boucle n'appelle que la Q-table) ;
- une **politique** qui contournerait la porte (les murs l'en empêchent) ;
- un **budget** de 200 pas (le but est atteint en 8–10).

## 4. La suite

1. **Porte qui se referme** : après un pas, la porte se referme ; le moteur doit repasser.
2. **Porte apprise avec le bruit** : entraîner sur la porte stochastique.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`courbe.py`](../tools/pensee/courbe.py) — `seule_sto()`, la politique sans A* sur le bruit.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueApprise`, `LABYRINTHE_PORTE_STO`.
- [`autotest.py`](../tools/pensee/autotest.py) — T16, 19/19.
- [`pensee-courbe.json`](pensee-courbe.json) — les 15 runs avec `sto_but`/`sto_pas`/`sto_essais`.

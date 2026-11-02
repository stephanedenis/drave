# B13 — la porte à un tour : la sonde ouvre et passe dans le même pas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **21/21 portes** : la porte ne s'ouvre que **le temps d'un pas**. La bonne politique doit
> ouvrir **et** passer dans le **même tour** : la `sonde_pm` le fait, et l'A* atteint le but en
> **27 nœuds** (sonde 5, coût 57). Le `pas`/`saut` ne peuvent pas profiter de l'ouverture.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-minute.json`](pensee-minute.json).

## 1. La porte à un tour

Même labyrinthe que T11, mais l'ouverture de la porte ne dure **qu'un pas** : la `sonde` doit
ouvrir la porte **et** franchir la case dans le **même** appel. Un `pas`/`saut` séparé ne voit
jamais la porte ouverte.

| politique | nœuds | pas | saut | sonde | coût | but |
|---|---:|---:|---:|---:|---:|---|
| **manhattan** | **27** | 12 | 10 | **5** | **57** | **oui** |

**Ce que ça dit** :

- **L'ouverture d'un tour suffit** : la sonde ouvre et passe dans le même pas ; le but est
  atteint en 27 nœuds, comme sur la porte stable (T11 : 28) et la porte qui se referme (T11 : 27).
- **Le `pas`/`saut` ne peuvent pas tricher** : ils ne voient jamais la porte ouverte ; seule la
  sonde franchit.
- **Le coût est stable** (57) : 5 sondes, 7 appels ; la porte minute ne coûte pas plus cher.
- **Le vrai piège serait une porte qui se referme** avant le passage **et** un agent qui doit
  revenir ; ce banc laisse l'agent passer directement.

## 2. Ce que ce banc ne dit pas

- **Politique manhattan** (règle), pas la Q-table : la Q-table sur la porte minute n'est pas
  mesurée.
- **Le coût 5** de la sonde est déclaré.
- **Le labyrinthe 5×5** est un jouet.
- **La porte minute** est déterministe (une ouverture par pas) ; un vrai problème aurait une
  **fenêtre** temporelle.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **politique chanceuse** qui ouvrirait la porte sans la viser ;
- un **chemin** qui contournerait la porte (les murs l'en empêchent) ;
- une **confusion** ouverture / passage : la sonde fait les deux ;
- un **budget** trop grand.

## 4. La suite

1. **Q-table sur la porte minute** : la politique apprend l'ouverture-passage.
2. **Fenêtre temporelle** : la porte s'ouvre tous les 3 pas ; le moteur doit attendre.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `LABYRINTHE_PORTE_MINUTE`, `REGISTRE_PM`,
  `sonde_pm`.
- [`autotest.py`](../tools/pensee/autotest.py) — T18, 21/21.
- [`pensee-minute.json`](pensee-minute.json) — le bilan.

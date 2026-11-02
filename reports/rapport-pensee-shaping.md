# B13 — le reward shaping : il ne suffit pas, la politique seule échoue encore

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **25/25 portes** : la `PolitiqueAppriseShaping` (Q-learning + **reward shaping** : -0,01 par pas
> + 0,1 par case gagnée vers le but) est entraînée sur la porte minute (56 états-Q). Exécutée
> **seule**, elle **échoue encore** (8 pas). Le shaping ne suffit pas ; l'A* reste nécessaire.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-shaping.json`](pensee-shaping.json).

## 1. Le reward shaping

Même porte minute que T18-T21, mais la récompense est **dense** : chaque pas vers le but rapporte
+0,1, chaque pas coûte -0,01, l'ouverture de la porte +0,1. La Q-table est entraînée (200
épisodes, graine 0) puis exécutée **seule**, sans A*.

| politique | états-Q | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **apprise shaping** | **56** | **0** | **8** | 28 nœuds |
| apprise minute (T21) | 60 | 0 | 8 | 28 nœuds |

**Ce que ça dit** :

- **Le shaping ne suffit pas** : la politique seule échoue encore en 8 pas ; la Q-table apprend
  la **distance** mais pas la **séquence complète**.
- **L'A* reste nécessaire** : c'est lui qui explore et atteint le but (T19) ; la politique seule
  ne le fait pas, même avec une récompense dense.
- **La Q-table reste petite** (56 états) : le shaping ne change pas fondamentalement la table.
- **La négative est explicite** : 0 but, 8 pas, 56 états-Q.

## 2. Ce que ce banc ne dit pas

- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le shaping** est une somme linéaire ; un shaping **potentiel** (Ng et al.) serait plus
  principled.
- **La `seule_minute`** s'arrête au `None` : la politique est **incomplète**, pas seulement
  mal récompensée.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (200 épisodes, graine 0) ;
- un **A* caché** dans `seule_minute` (non : la boucle n'appelle que la Q-table) ;
- une **Q-table** initialisée (non : elle part de zéro) ;
- un **budget** de 200 pas (le `None` arrive en 8).

## 4. La suite

1. **Réseau** : une politique paramétrique au lieu de la table, capable de **généraliser**.
2. **Shaping potentiel** : un shaping qui préserve la politique optimale.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseShaping`.
- [`autotest.py`](../tools/pensee/autotest.py) — T22, 25/25.
- [`pensee-shaping.json`](pensee-shaping.json) — le bilan.

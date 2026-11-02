# B13 — la mémoire très courte : 20/20, 8,0 pas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **72/72 portes** : la Q-table est multipliée par **0,5** tous les 10 épisodes — un oubli deux
> fois plus fort que T68. La politique atteint le but **20/20** en **8,0 pas** : l'oubli fort
> **n'empêche rien**, et le chemin est même plus court que l'oubli léger (10,0).
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-oubli-fort.json`](pensee-oubli-fort.json).

## 1. La mémoire très courte

Même monde que T68 (look à l'épisode 3000), mais la Q-table est multipliée par **0,5** tous les
10 épisodes.

| oubli | buts | v final | états-Q | pas |
|---|---|---:|---:|---:|
| **× 0,5 (T69)** | **20/20** | **0,38** | 586 | 8,0 |
| × 0,9 (T68) | 20/20 | 0,56 | 463 | 10,0 |
| aucun (T67) | 20/20 | 0,54 | 530 | 8,0 |

**Ce que ça dit** :

- **L'oubli fort n'empêche rien** : 20/20, 8,0 pas ; le chemin est même plus court que l'oubli
  léger — la décroissance forte force la re-découverte, pas la perte.
- **v ≈ 0,38** : la fenêtre ne voit pas le look ; elle reste au hasard.
- **La Q-table grandit** (586 états) : l'oubli fort force l'exploration, donc plus d'états.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **L'oubli est uniforme** ; un oubli sélectif serait autre.
- **Le × 0,5** n'est pas la limite : × 0,1 ou × 0 testeraient la rupture.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,38** qui serait un artefact de la fenêtre (le look est sorti) ;
- un **A* caché** (non : `seule_bayes_oubli_fort` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Oubli total** (× 0) : la rupture de la mémoire.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubliFort`.
- [`autotest.py`](../tools/pensee/autotest.py) — T69, 72/72.
- [`pensee-oubli-fort.json`](pensee-oubli-fort.json) — le bilan.

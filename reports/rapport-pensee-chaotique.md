# B13 — l'alternance aléatoire : 20/20, v = 0,12

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **59/59 portes** : la fiabilité **bascule au hasard** (0,1 ↔ 0,9 avec p = 1/500 par épisode).
> La fenêtre adaptative suit chaque bascule ; v finit à **0,12** et la politique atteint le but
> **20/20** en **8,0 pas**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-chaotique.json`](pensee-chaotique.json).

## 1. L'alternance aléatoire

Même monde que T55, mais la bascule est **aléatoire** : à chaque épisode, p = 1/500 de changer
de régime (0,1 ↔ 0,9) ; le nombre de bascules varie.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| 4000 | 20/20 | 0,08 | 742 | 8,6 |
| **8000** | **20/20** | **0,12** | 820 | 8,0 |
| alternance régulière (T55) | 20/20 | 0,14 | 797 | 8,0 |

**Ce que ça dit** :

- **Le hasard ne casse rien** : 20/20 aux deux durées ; la fenêtre adaptative suit des bascules
  imprévisibles.
- **v suit le dernier régime** (0,12) ; il ne moyenne pas les deux.
- **Le coût est faible** (8,0 pas à 8000 ; 8,6 à 4000) : la politique s'adapte sans détour.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Deux régimes** (0,1 / 0,9) ; une fiabilité continue aléatoire serait autre.
- **La bascule est rare** (1/500) ; 1/50 serait plus dure.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v final 0,12** qui serait un artefact de la fin (le dernier régime est bien 0,1 ou 0,9) ;
- un **A* caché** (non : `seule_bayes_chaotique` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Bascule fréquente** : 1/50 ; mesurer la dégradation.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesChaotique`.
- [`autotest.py`](../tools/pensee/autotest.py) — T56, 59/59.
- [`pensee-chaotique.json`](pensee-chaotique.json) — le bilan.

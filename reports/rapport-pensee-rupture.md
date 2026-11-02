# B13 — la rupture : 90 % d'erreur, v = 0,12, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **57/57 portes** : la fiabilité de l'observation **s'effondre** — 10 % d'erreur sur la
> première moitié de l'entraînement, **90 %** sur la seconde. La fenêtre adaptative descend à
> **v = 0,12** ; le filtre **inverse** l'observation (elle dit le contraire) et la politique
> atteint le but **20/20** en **8,0 pas**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-rupture.json`](pensee-rupture.json).

## 1. La rupture

Même monde que T52/T53, mais l'erreur passe **brutalement** de 10 % à 90 % à mi-entraînement :
l'observation devient **antiprédictive**. `v` est estimé sur la fenêtre adaptative.

| dispositif | buts | v final | états-Q | pas |
|---|---:|---:|---:|---:|
| **rupture (8000 ép.)** | **20/20** | **0,12** | 780 | 8,0 |
| rupture (4000 ép.) | 20/20 | 0,04 | 723 | 8,0 |
| dérive continue (T53) | 20/20 | 0,5 | 738 | 8,6 |

**Ce que ça dit** :

- **La rupture est absorbée** : v descend à 0,12 ; le filtre bayésien **inverse** l'observation
  (quand elle dit « porte en 0 », il croit 1) et la politique réussit 20/20.
- **Le coût est nul** (8,0 pas) : l'observation antiprédictive est aussi informative qu'une
  observation fiable, une fois le signe connu.
- **La table reste petite** (780 états) : la rupture ne crée pas d'états, elle change le sens.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Une seule rupture** ; des ruptures répétées demanderaient une détection plus fine.
- **La vraisemblance est estimée** par le taux ; une rupture **de la vérité** (la porte change
  de loi) serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v inversé** qui serait un artefact (0,12 < 0,5 : le filtre inverse bien) ;
- un **A* caché** (non : `seule_bayes_rupture` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Ruptures répétées** : la fiabilité alterne ; la fenêtre doit suivre.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesRupture`.
- [`autotest.py`](../tools/pensee/autotest.py) — T54, 57/57.
- [`pensee-rupture.json`](pensee-rupture.json) — le bilan.

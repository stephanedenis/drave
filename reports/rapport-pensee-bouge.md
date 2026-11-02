# B13 — la porte qui bouge : l'horloge dans l'état

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **37/37 portes** : la porte change de position **toutes les 3 pas** (elle alterne `(3,3)` et
> `(1,3)`). L'**A*** la trouve (28 nœuds, sonde 5, coût 58) ; la `PolitiqueAppriseBouge`
> (236 états-Q, l'horloge `t % 6` dans l'état) **atteint le but seule en 10 pas**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-bouge.json`](pensee-bouge.json).

## 1. La porte qui bouge

Même labyrinthe à deux portes que T31/T32, mais la porte **change de position** toutes les 3
pas : `d(t) = (t // 3) % 2`. L'état porte l'horloge `t % 6` ; la politique doit **re-planifier**
quand la porte bouge.

| dispositif | résultat |
|---|---|
| **A* + sonde** | but, 28 nœuds, sonde 5, coût 58 |
| **politique seule** | **but/10 pas**, 236 états-Q |

**Ce que ça dit** :

- **La politique apprend le temps** : l'horloge `t % 6` dans l'état suffit à re-planifier quand
  la porte bouge ; le but est atteint en 10 pas (contre 8 pour la porte fixe).
- **Le coût de la mobilité est faible** : +2 pas, +1 sonde ; la porte qui bouge ne casse pas
  la politique.
- **L'A* reste un cadre** : il explore les états horodatés et trouve la séquence ; la politique
  seule la reproduit.
- **236 états-Q** : plus que la porte mobile (170) — l'horloge ajoute un facteur 6 aux états,
  mais la table reste petite.

## 2. Ce que ce banc ne dit pas

- **Une seule période** (3 pas) ; une porte qui bouge **aléatoirement** serait plus dure.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **La porte est déterministe** (elle alterne) ; une porte **stochastique** + mobile serait autre.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (1000 épisodes, graine 0 ; à vérifier sur plusieurs graines) ;
- une **période codée en dur** dans la politique (non : `t` vient de l'état) ;
- un **A* caché** dans `seule_bouge` (non : la boucle n'appelle que la Q-table) ;
- une **case de l'autre porte** qui bloquerait (le `_libre_pb` la libère).

## 4. La suite

1. **Plusieurs graines** : la porte qui bouge tient-elle hors graine 0 ?
2. **Période variable** : 2, 4, 5 pas ; mesurer la dégradation.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `LABYRINTHE_PORTE_BOUGE`, `REGISTRE_PB`,
  `PolitiqueAppriseBouge`, `seule_bouge`.
- [`autotest.py`](../tools/pensee/autotest.py) — T34, 37/37.
- [`pensee-bouge.json`](pensee-bouge.json) — le bilan.

# B13 — le neuronal nécessaire : le cadenas, la sonde seule, l'aveugle échoue

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **12/12 portes** : sur le **cadenas**, la **sonde est le seul opérateur** ; avec la politique
> « avant », le moteur atteint le but en **3 appels** ; avec la politique « arrière » (aveugle),
> il consomme **20 appels** et **n'atteint pas** le but. Le neuronal n'est plus seulement
> *utile* : il est **nécessaire**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-necessaire.json`](pensee-necessaire.json).

## 1. Le cadenas

État : une position `0..3`. **Un seul opérateur**, `sonde` (genre **neuronal**), qui demande à la
politique la direction (`avant` / `arrière`) et avance d'un cran. But : `3`.

| politique | nœuds | appels | coût | but |
|---|---:|---:|---:|---|
| **avant** (`cadenas_avant`) | **3** | **3** | **3** | **oui** |
| arrière (`cadenas_arriere`) | 20 | 20 | 20 | **non** |

**Ce que ça dit** :

- **Le seul chemin est la politique** : `pas` et `saut` n'existent pas dans ce registre ; le
  moteur ne peut avancer que par la sonde.
- **La bonne politique atteint le but en 3 coups** ; **l'aveugle tourne** (0→1→0→…) et échoue
  même avec 20 nœuds : le contrôle négatif n'est plus « inutile », il est **décisif**.
- **Le coût est le coût du modèle** : 3 appels contre 20 ; la politique est le **seul** levier.
- **Le `DRVM`** rend le bilan (`noeuds`, `par_operateur`, `genres`, `cout`, `appels`, `but`,
  `score`, `politique`), et il utilise désormais le **but du problème courant**, pas la grille.

## 2. Ce que ce banc ne dit pas

- **La politique est un double** (`cadenas_avant`/`arrière`), pas un modèle neuronal : le vrai
  `drave-n0` n'a pas de poids dans l'environnement, le `NeuronalLLM` reste refusé.
- **Le cadenas est un jouet** : un état linéaire, un seul opérateur ; il prouve la **nécessité
  structurelle**, pas la qualité d'un modèle.
- **Le coût 1 par appel** est déclaré ; une latence réelle changerait le bilan.
- **L'aveugle échoue par construction** (il revient en arrière) ; ce n'est pas une preuve que
  tout mauvais modèle échoue, seulement que **sans la bonne politique** le but n'est pas atteint.
- **Le `DRVM`** est le runtime du moteur, pas le format DRVM de N0.

## 3. Ce qui pourrait rendre cette fiche fausse

- une politique **chanceuse** qui atteindrait le but par hasard (le cadenas est linéaire : non) ;
- un opérateur **caché** qui contournerait la sonde (le registre n'en a qu'un) ;
- un budget **trop grand** qui laisserait l'aveugle atteindre le but (20 nœuds, but à 3 : non) ;
- une confusion **politique / opérateur** : c'est la politique qui est neuronale, l'opérateur
  n'est que le **point d'appel**.

## 4. La suite

1. **Politique DRVM/native** : brancher un vrai modèle quand ses poids seront là ; le cadenas
   mesurera alors la **qualité** de la politique, pas seulement sa nécessité.
2. **Coût mesuré** : remplacer le coût 1 par la latence réelle des appels.
3. **L** : 200+ phrases réelles et lecture double ; le neuronal réel reste bloqué.
4. **B13** : un cadenas **non linéaire** (plusieurs chemins, un piège) pour que la politique
   puisse être **bonne** ou **mauvaise** sans être trivialement l'une ou l'autre.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `CADENAS`, `REGISTRE_CADENAS`,
  `PolitiqueCadenas`, `PolitiqueCadenasAveugle`.
- [`autotest.py`](../tools/pensee/autotest.py) — T9, 12/12.
- [`pensee-necessaire.json`](pensee-necessaire.json) — les bilans.
- [`moteur-de-pensee.md`](../docs/implantation/moteur-de-pensee.md) — le contrat.

# B13 — le juge des réponses : sa couverture est 0/19

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **126/126 portes** : le **juge** est en place (comparaison à une référence, mesure de la
> couverture), mais sa **couverture est 0/19** : le gold porte l'**acte** des questions, pas leur
> **réponse**. Sans référence, aucun juge ne peut mesurer la correction. C'est la pièce
> manquante, nommée.
>
> **Dispositif** : [`juge.py`](../tools/tests/linguistique/juge.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-juge.json`](pensee-juge.json).

## 1. Le juge

| mesure | valeur |
|---|---:|
| questions du gold | 19 |
| questions avec **réponse de référence** | **0** |
| couverture | **0,0000** |
| réponse candidate (None) vs référence (None) | 0,0 |

**Ce que ça dit** :

- **Le juge est aveugle** : il compare à une référence qui n'existe pas ; 0/19 de couverture
  signifie que la mesure de correction est **impossible** en l'état.
- **Le gold mesure la forme, pas le fond** : l'`acte` (19/19) est annoté, la `reponse` ne l'est
  pas — c'est le **biais** de tout le gold actuel.
- **La pièce manquante est nommée** : il faut **écrire les 19 réponses de référence** (le oui/non,
  le contenu) avant de juger ; c'est le prochain round.
- **Le juge ne juge pas** : `juge(None, None) = 0` ; le 0 n'est pas une performance du bloc, c'est
  l'absence de référence.

## 2. Ce que ce banc ne dit pas

- **Ce qu'un juge humain dirait** : la correction sémantique n'est pas mesurée.
- **19 questions** ; le réel donne les mêmes ordres.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de la référence** (une chaîne exacte, pas le sens) ;
- **le 0/19** est un état du gold, pas du bloc ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Écrire les 19 réponses de référence** dans le gold (`pragma.reponse`), puis re-mesurer la
   couverture et le juge.
2. **Le neuronal réel** : toujours bloqué ; c'est lui qui répondrait.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`juge.py`](../tools/tests/linguistique/juge.py) — `juge`, `couverture`.
- [`autotest.py`](../tools/pensee/autotest.py) — T123, 126/126.
- [`pensee-juge.json`](pensee-juge.json) — la couverture.

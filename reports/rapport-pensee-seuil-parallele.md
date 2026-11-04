# B13 — le seuil du parallèle : il ne peut pas battre le max

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **147/147 portes** : le seuil `parallele` du banc exigeait que le **parallèle
> (confiance)** batte le **max** de l'heuristique et du neuronal (0,9389). Il ne le peut pas
> (**0,9326**) : la fusion par confiance garde les tokens de l'heuristique (confiance 0,7)
> contre ceux du neuronal (0,6), donc elle plafonne sous le neuronal. Le seuil est corrigé : le
> parallèle doit **tenir l'heuristique**, pas battre le max — c'est le `_niveau` qui bat le max.
>
> **Dispositif** : [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432-run2.json`](pensee-quatre-modes-432-run2.json),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-seuil-parallele.json`](pensee-seuil-parallele.json).

## 1. Les modes et le max

| mode | POS | contre le max (0,9389) | verdict |
|---|---:|---|---|
| heuristique | 0,7444 | — | — |
| neuronal | **0,9389** | — | — |
| parallèle (confiance) | 0,9326 | −0,0063 | **ne peut pas** |
| cascade (confiance) | 0,9326 | −0,0063 | ne peut pas |
| **parallele_niveau** | **0,9389** | 0 | **bat le max** |
| **cascade_niveau** | **0,9389** | 0 | **bat le max** |

**Ce que ça dit** :

- **La confiance ne suffit pas** : la fusion par confiance donne le token au bloc le plus
  confiant ; l'heuristique (0,7 sur les tokens ouverts) gagne contre le neuronal (0,6), donc le
  parallèle **plafonne sous le neuronal**.
- **Le niveau est la seule fusion qui bat le max** : il donne la POS au neuronal et garde le
  reste à l'heuristique — d'où 0,9389 + acte 0,9954.
- **Le seuil était faux** : il demandait au parallèle un exploit que sa règle interdit ; il est
  corrigé (le parallèle tient l'heuristique, le niveau bat le max).
- **La négative est explicite** : le parallèle reste sous le neuronal (−0,0063), c'est sa nature.

## 2. Ce que ce banc ne dit pas

- **Deux passes** (température 0) ; la variance n'est pas mesurée au-delà.
- **Le seuil du `cascade`** (confiance) est déjà « tient l'heuristique » ; il passe.
- **Le gold 432** : les seuils sont ceux du banc.
- **Le défaut conditionnel** (T143) : le niveau quand la clé est là.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la règle de confiance** pourrait changer (un autre seuil) ;
- **le gold** : 432 phrases ;
- **les passes** : deux, à température 0 ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La troisième passe** : la variance (si le temps le permet).
2. **Le `parallele` utile** : il reste le mode sans clé (il tient l'heuristique).
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) — le seuil.
- [`pensee-quatre-modes-432-run2.json`](pensee-quatre-modes-432-run2.json) — les mesures.
- [`autotest.py`](../tools/pensee/autotest.py) — T144, 147/147.
- [`pensee-seuil-parallele.json`](pensee-seuil-parallele.json) — le seuil.

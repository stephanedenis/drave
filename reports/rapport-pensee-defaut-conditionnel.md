# B13 — le défaut conditionnel : le niveau si le réel est là

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **146/146 portes** : le défaut de la fusion est **conditionné à la présence
> d'un neuronal réel**. Deux passes ont montré que le **niveau gagne** avec le réel (0,9389) et
> **perd** avec le mock (0,3454) ; le défaut suit donc la **présence de la clé**, pas une doctrine.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-defaut-conditionnel.json`](pensee-defaut-conditionnel.json).

## 1. La règle

| condition | `priorite_par_defaut()` | conséquence |
|---|---|---|
| `DEEPSEEK_KEY_FILE` présent | **`PRIORITE_NIVEAU`** | le niveau (POS 0,9389 avec le réel) |
| clé absente | **`None`** | la confiance (POS 0,7455 avec le mock) |

**Ce que ça dit** :

- **Le défaut n'est pas une constante** : il dépend de ce qui est **joignable**. Le réel gagne
  le niveau ; le mock perd. Un défaut fixe serait faux dans l'un des deux cas.
- **La mesure tranche** : deux passes (0,9309 puis 0,9389) contre le mock (0,3432 / 0,3454).
- **Le comportement explicite reste prioritaire** : un `priorite_par_niveau=` fourni par
  l'appelant n'est pas écrasé ; seul `None` (le défaut) est résolu.
- **La négative est explicite** : sans clé, le niveau ferait 0,3454 — il n'est pas choisi.

## 2. Ce que ce banc ne dit pas

- **La clé est un proxy** : un autre neuronal réel (un modèle local) aurait le même effet, mais
  le test ne le prouve pas.
- **Les seuils du banc** ne changent pas (le `parallele` échoue encore).
- **L'API** : deux passes, température 0.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la variable d'environnement** : elle peut être posée sans que l'API réponde ;
- **le mock** reste le défaut des portes (pas de clé en CI) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le seuil du `parallele`** : le réviser ou le documenter.
2. **La troisième passe** : la variance (une passe de plus, si le temps le permet).
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `priorite_par_defaut`, `Parallele`, `Cascade`.
- [`autotest.py`](../tools/pensee/autotest.py) — T143, 146/146.
- [`pensee-defaut-conditionnel.json`](pensee-defaut-conditionnel.json) — la règle.

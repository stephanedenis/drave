# B13 — l'anaphore : 4/4 liens justes

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **95/95 portes** : quatre phrases du discours portent une annotation `coref` à la main
> (r307 `il → chat`, r308 `elle → marie`, r317 `it → cat`, r318 `she → marie`). L'heuristique
> « dernier nom » (`anaphore.py`) résout **4/4** liens justes. C'est une **première** mesure de
> coréférence, pas une preuve : le gold est petit et les cas sont faciles.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore.json`](pensee-anaphore.json).

## 1. L'anaphore

| phrase | pronom | attendu | obtenu |
|---|---|---|---|
| r307 | `il` | `chat` | `chat` |
| r308 | `elle` | `marie` | `marie` |
| r317 | `it` | `cat` | `cat` |
| r318 | `she` | `marie` | `marie` |

**Ce que ça dit** :

- **4/4** : le « dernier nom » suffit sur ces quatre cas (le pronom suit immédiatement son
  antécédent).
- **La règle est naïve** : elle échouera sur `Le chat voit le chien ; il dort` (le dernier nom
  est `chien`), sur les pronoms sujets inversés (`Viens-tu ?`) et sur les chaînes longues.
- **Le gold est petit** (4 liens) : le taux 1,0 n'a pas d'intervalle utile.
- **La négative manque** : il faudrait des cas pièges pour mesurer la règle.

## 2. Ce que ce banc ne dit pas

- **4 liens** ; 50 liens donneraient un taux.
- **Les cas pièges** (deux noms, pronoms inversés) ne sont pas dans le gold.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 500** (320 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (4 liens) : c'est la limite principale ;
- **les ancres** (annotation à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Des cas pièges** : deux noms, pronoms inversés ; la règle naïve doit échouer.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre`, `mesurer`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 4 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T92, 95/95.
- [`pensee-anaphore.json`](pensee-anaphore.json) — le bilan.

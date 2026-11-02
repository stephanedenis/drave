# B13 — les chaînes anaphoriques longues : 7/10, le rôle manque

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **99/99 portes** : six phrases à **chaînes longues** (r337–r342 : trois noms, deux pronoms)
> entrent dans le gold (342 phrases). La règle « dernier nom » tombe à **7/10** (0,70) : elle
> prend l'**objet** pour l'antécédent du **sujet**. Les 20 liens courts restent à 20/20.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-chaines.json`](pensee-anaphore-chaines.json).

## 1. Les chaînes longues

| sous-ensemble | liens | justes | taux | échecs |
|---|---:|---:|---:|---|
| r301–r336 (court) | 20 | 20 | 1,00 | — |
| **r337–r342 (long)** | **10** | **7** | **0,70** | r337 `il→sophie`, r339 `elle→livre`, r341 `she→book` |

**Ce que ça dit** :

- **Le rôle manque** : dans `Paul voit Marie et Sophie ; il lui parle`, le dernier nom est
  `sophie` (l'objet), mais `il` reprend `paul` (le sujet). La règle du dernier nom ne peut pas
  distinguer le sujet de l'objet.
- **Trois échecs sur dix** : deux sur le sujet (`il`, `elle`, `she`), un sur la chaîne
  (`elle le ferme`).
- **La correction est claire** : utiliser le **rôle du segment** (`agent` pour le sujet,
  `patient` pour l'objet) — c'est la prochaine mesure.
- **La négative est explicite** : 7/10, et les 20 liens courts restent 20/20 (le gold est
  cohérent).

## 2. Ce que ce banc ne dit pas

- **10 liens** ; 30 donneraient une courbe.
- **Le rôle du segment** est annoté dans le gold (`agent`/`patient`) : la correction est
  possible, pas encore faite.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (10 liens) ;
- **les rôles** (annotation à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le rôle du segment** : `agent`/`patient` pour distinguer sujet et objet ; viser 10/10.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre`, `mesurer`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T96, 99/99.
- [`pensee-anaphore-chaines.json`](pensee-anaphore-chaines.json) — le bilan.

# B13 — la vérification parallèle : 183/183 en 1 min 54 (×2,4)

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;
> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,
> F1 0,7535, attachement 236/237, couverture 0,9916, 2 spans).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Ce que ça règle** : l'autotest était **mono-processus** — ~4 min 40 de CPU et ~4 min 40 de
> temps mural sur un poste à 40 cœurs, alors que **183 portes indépendantes** pouvaient tourner de
> front. Avec `AUTOTEST_JOBS=8`, il tient en **1 min 54** (temps mural), **183/183**, mêmes verdicts.
> **Ce que ça ne règle pas** : le reste du dépôt (évaluations gold, portes longues) reste séquentiel ;
> ce round ne fait que la vérification.
>
> **Dispositif** : [`autotest.py`](../tools/pensee/autotest.py) (`_portes` rend des **callables**,
> `_parallele` sur un pool `fork`, `AUTOTEST_JOBS`) ; JSON [`pensee-autotest-parallele.json`](pensee-autotest-parallele.json).

## 1. La mesure

| mode | temps mural | user (CPU) | verdict |
|---|---:|---:|---|
| séquentiel (`AUTOTEST_JOBS=1`) | ~4 min 40 | ~4 min 40 | 183/183 |
| **parallèle 8** | **1 min 54** | 4 min 39 | **183/183** |

**Facteur** : ×2,4 sur le temps mural (le CPU total ne change pas ; le parallélisme effectif est
limité par les portes longues — T154 320 s, T31/T32/T33, etc.).

**Ce que ça dit** :

- **Les portes sont indépendantes** (chacune construit son état) : le pool `fork` suffit, sans
  partage ni verrou.
- **Les verdicts sont identiques** (183/183, mêmes messages) : `fork` hérite du module importé.
- **Le CPU total est inchangé** (4 min 39) : on ne fait que mieux l'utiliser.

## 2. Ce que ce banc ne dit pas

- **Les portes longues** : une porte de 300 s borne le temps mural du lot.
- **Les autres évaluations** (`evaluer_gold.py`, les portes du dépôt) : non parallélisées.
- **La mémoire** : 8 processus × le module (~50 Mo) — négligeable ici.

## 3. Ce qui pourrait rendre cette fiche fausse

- **les portes à effet de bord** (T178 patche `_syntagmes_simple`) : elles s'exécutent dans leur
  propre processus, donc sans effet croisé — mais si une porte écrivait un fichier partagé, le
  parallèle changerait le résultat ;
- **le `fork`** n'existe pas sur toutes les plateformes (le repli est le mode séquentiel) ;
- un **audit** qui ne vérifie pas ces mesures.

## 4. La suite

1. **Paralléliser `evaluer_gold.py`** (par phrase) pour les mesures de masse.
2. **Une porte produit** qui lance le smoke test + l'autotest parallèle.

## 5. Fichiers

- [`autotest.py`](../tools/pensee/autotest.py) — `_portes` (callables), `_parallele`, `AUTOTEST_JOBS`.
- [`pensee-autotest-parallele.json`](pensee-autotest-parallele.json).

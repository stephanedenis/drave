# B13 — les 500 premiers segments : 294 GN et 206 GV sans cible

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **158/158 portes** : les **500 premiers segments sans cible** sont **294 GN** et **206 GV** —
> la structure élémentaire (sujet + verbe) des phrases du début du gold. Leur attachement n'est
> pas annoté, et la règle ne peut pas l'inventer : c'est la **couverture** qui manque, pas la
> mesure.
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-cibles-500.json`](pensee-cibles-500.json).

## 1. Les 500 premiers

| type | segments | part |
|---|---:|---:|
| **GN** | **294** | 58,8 % |
| **GV** | **206** | 41,2 % |
| autres | 0 | 0 % |

**Ce que ça dit** :

- **Le début du gold est du SVO nu** (`Le chat dort.`, `La femme a vu l'homme.`) : les GN et GV
  élémentaires n'ont pas de `cible` — l'attachement n'a de sens que pour les **compléments**
  (GP, REL, SUB) et les relations **GN → GV**.
- **La cible n'est pas définie pour un GN sujet** : un attachement `agent → GV` serait une
  relation, pas une cible de segment ; le gold ne l'annote pas, et c'est cohérent.
- **Le vrai déficit est ailleurs** : les 1624 sans cible incluent les relations **non
  annotées**, pas seulement les cibles manquantes.
- **La négative est explicite** : 0 cible sur ces 500, et ce n'est pas une erreur de mesure.

## 2. Ce que ce banc ne dit pas

- **Les 500 suivants** : la répartition peut changer (les phrases complexes ont des GP/REL).
- **Le gold 432** : 432 phrases.
- **L'attachement** : il se mesure sur les 239 cibles annotées (T153).
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de la cible** : un GN sujet n'a pas de cible, ce n'est pas un manque ;
- **le gold** : 432 phrases ;
- **les 500** : un échantillon du début ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les 500 suivants** : voir la part des GP/REL/SUB (les vrais candidats à une cible).
2. **La relation GN → GV** : un attachement `agent`/`patient` serait une autre mesure.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `attachement`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — les `cible`.
- [`autotest.py`](../tools/pensee/autotest.py) — T155, 158/158.
- [`pensee-cibles-500.json`](pensee-cibles-500.json) — les 500.

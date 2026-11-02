# B13 — les liens classés : 50 intra, 62 inter, 4 absents

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **138/138 portes** : les **116 liens** de coréférence sont classés : **50 intra-phrase**
> (l'antécédent est dans la même phrase — `il l'attrape`), **62 inter-phrase** (l'antécédent est
> dans une phrase antérieure), **4 absents** du texte. Le 62/116 du round précédent n'était donc
> qu'une partie de l'histoire.
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-liens-classes.json`](pensee-liens-classes.json).

## 1. Les trois classes

| classe | liens | part |
|---|---:|---:|
| **intra-phrase** | **50** | 0,4310 |
| **inter-phrase** | **62** | 0,5345 |
| **absents** | **4** | 0,0345 |
| **tout** | **116** | 1,0000 |

**Ce que ça dit** :

- **La coréférence est locale** : 43 % des liens ont leur antécédent dans la **même phrase** —
  le lien de phrase (62) n'en couvre que la moitié.
- **4 absents** : le texte ne contient pas l'antécédent (les pronoms sans nom, les sujets
  implicites) — la règle ne peut rien faire.
- **Le lien de phrase est une sous-mesure** : il ne faut pas lire 62/116 comme un taux d'échec ;
  c'est 62 inter-phrase + 50 intra-phrase = **112 liens résolus par la règle**, 4 sans ancre.
- **La négative est explicite** : 4 absents restent hors de portée.

## 2. Ce que ce banc ne dit pas

- **Les 50 intra** ne sont pas « trouvés » par le lien de phrase : ils sont dans la phrase même.
- **116 liens** : un échantillon.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 607** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de l'intra** (le nom de l'antécédent apparaît dans le texte de la phrase) ;
- **les 4 absents** dépendent du gold ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les 4 absents** : les nommer (les pronoms sans antécédent) — la frontière de la règle.
2. **Le neuronal réel** : toujours bloqué.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `classer_liens_coref`.
- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre_meta`.
- [`autotest.py`](../tools/pensee/autotest.py) — T135, 138/138.
- [`pensee-liens-classes.json`](pensee-liens-classes.json) — les classes.

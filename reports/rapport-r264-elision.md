# B13 — `r264` réglé : le GV s'arrête au marqueur élidé (`qu'il`), couverture 0,9916

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Le 13e span est retrouvé** : dans « Je sais **qu'il vient demain** », le GV « sais » avalait
> le marqueur élidé, donc la SUB n'était jamais produite au bon span. La condition d'arrêt du GV
> testait `endswith("qu")` sur le **token entier** (`qu'il`) au lieu de son **radical** (`qu`).
> Corrigé : l'attachement passe de **235/236 à 236/237**, la **couverture de 0,9874 à 0,9916**,
> la **F1 de 0,6482 à 0,6519** ; **183/183** ; **2 spans restants** (`r035`, `g017`).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (boucle GV),
> [`autotest.py`](../tools/pensee/autotest.py) (17 assertions) ; JSON
> [`pensee-r264-elision.json`](pensee-r264-elision.json).

## 1. Le bug

```python
# avant : la condition teste le token entier
and (_normaliser(mots[j][2]).split("'")[0] + "e"
     if _normaliser(mots[j][2]).endswith("qu") else ...)   # « qu'il ».endswith("qu") → False
# après : elle teste le radical
and (_normaliser(mots[j][2]).split("'")[0] + "e"
     if _normaliser(mots[j][2]).split("'")[0] == "qu" else ...)
```

Conséquence avant : le GV continuait sur « qu'il vient demain » (j jusqu'à la ponctuation), la
SUB n'était produite que par le générateur S, au span court **[8:19]** ; le gold attend **[8:26]**.

## 2. Avant / après

| mesure | avant | **après** |
|---|---:|---:|
| exact / labels | 235/236 | **236/237** |
| **couverture** | 0,9874 | **0,9916** |
| spans perdus | 3 | **2** (`r035`, `g017`) |
| F1 syntagmes | 0,6482 | **0,6519** |
| dev / test | 160/161, 74/74 | **160/161, 76/76** |

## 3. Contrôles

- **183/183** portes, **17 assertions** recalées.
- **Aucune régression** : POS 0,8625 inchangé ; l'attachement monte.
- **Le doublon** SUB [8:19] (générateur S) reste, marqué `meta.alternative` — c'est la partition
  étiquetée, pas une erreur.

## 4. Ce que ce banc ne dit pas

- **`r035`** (relative zéro : « The film she talks about ») et **`g017`** (arbitrage d'adverbe)
  restent hors d'atteinte : 2 spans.
- **Le doublon** S n'est pas filtré par défaut.

## 5. Ce qui pourrait rendre cette fiche fausse

- **la condition** dépend de l'apostrophe du token (`qu'il`) ;
- **le gold** attend [8:26], la SUB du chunker le donne maintenant.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — la boucle GV.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-r264-elision.json`](pensee-r264-elision.json).

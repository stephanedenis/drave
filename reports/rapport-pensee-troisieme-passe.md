# B13 — la troisième passe : variance nulle, tous les seuils verts

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **148/148 portes** : la **troisième passe** API donne **exactement** le run 2
> (POS 0,9389, syntagmes 0,8241, tête 0,8797, refus 0) — variance **nulle** à température 0.
> Et le **défaut conditionnel** (T143) est visible : le `parallele` passe de 0,9326 (run 2, sans
> la clé dans l'environnement) à **0,9389** (run 3, avec la clé) — parce que le défaut prend le
> `PRIORITE_NIVEAU` quand la clé est là.
>
> **Dispositif** : [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432-run3.json`](pensee-quatre-modes-432-run3.json),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-troisieme-passe.json`](pensee-troisieme-passe.json).

## 1. Trois passes

| passe | neuronal POS | `_niveau` POS | `parallele` POS | refus |
|---|---:|---:|---:|---:|
| run 1 | 0,9309 | 0,9309 | 0,9280 | 1 |
| run 2 | **0,9389** | **0,9389** | 0,9326 | **0** |
| **run 3** | **0,9389** | **0,9389** | **0,9389** | **0** |

**Ce que ça dit** :

- **Variance nulle** : run 2 et run 3 sont identiques au chiffre près (température 0) ; le
  résultat est **stable**.
- **Tous les seuils passent** (7/7) : le `parallele` atteint 0,9389 parce que le **défaut
  conditionnel** (T143) lui donne le `PRIORITE_NIVEAU` quand la clé est dans l'environnement.
- **Le run 2 avait la clé en argument mais pas en variable** : `DEEPSEEK_KEY_FILE` était passée
  au processus, pas exportée dans l'environnement au moment de la construction — le run 3 la
  voit, et le défaut s'applique.
- **La négative** : sans la clé, le `parallele` resterait la confiance (0,9326).

## 2. Ce que ce banc ne dit pas

- **La variance du modèle** au-delà de trois passes à température 0 : nulle par construction.
- **Le run 2** a servi de contrôle (la clé absente de l'environnement) : c'est un hasard
  **heureux** qui documente le défaut conditionnel.
- **Le gold 432** : les seuils sont ceux du banc.
- **Le coût** : 858 appels, 254 454 tokens, 807,6 s par passe.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la température 0** : elle cache la variance réelle du modèle ;
- **le cache** de l'API peut expliquer l'identité parfaite (858 appels, mêmes tokens) ;
- **le gold** : 432 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La variance réelle** : une passe à température 0,3 pour la mesurer.
2. **Le DRVM** : le conteneur natif (la prochaine ligne).
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) — les six modes.
- [`pensee-quatre-modes-432-run3.json`](pensee-quatre-modes-432-run3.json) — la passe 3 (brute).
- [`autotest.py`](../tools/pensee/autotest.py) — T145, 148/148.
- [`pensee-troisieme-passe.json`](pensee-troisieme-passe.json) — la variance.

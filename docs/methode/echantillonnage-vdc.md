# Échantillonnage déterministe : van der Corput

> **Règle.** Les fenêtres d'entraînement ne sont **pas** tirées par `randint` ni mélangées par
> `shuffle`. Elles suivent la suite de **van der Corput** (base 2, bit reversal), qui parcourt
> `[0, 1)` en **discrépance faible**. Même compteur = mêmes fenêtres, sans état de générateur.

## Pourquoi

Un tirage pseudo-aléatoire dépend d'un **état global** : deux exécutions peuvent différer après une
sauvegarde, un changement de bibliothèque ou un ordre d'appels différent. La suite de van der Corput
est une **fonction pure** de l'indice : elle est reproductible, vérifiable et couvrante.

## Définition

Pour `i ≥ 0`, on écrit `i` en base 2, on inverse les chiffres et on place le résultat après la
virgule :

| `i` | base 2 | bit reversal | `vdc(i)` |
|---:|---|---|---:|
| 0 | 0 | 0 | 0,000 |
| 1 | 1 | 0,1 | 0,500 |
| 2 | 10 | 0,01 | 0,250 |
| 3 | 11 | 0,11 | 0,750 |
| 4 | 100 | 0,001 | 0,125 |

## Usage

```python
from tools.vdc import departs_vdc
# n fenêtres à partir du compteur global ; borne = len(data) - seq - 1
debuts = departs_vdc(compteur, n, borne, seq)
```

- **Entraînement** : compteur `pas × lot`.
- **Validation** : compteur `10 000 000 + …`, séparé de l'entraînement.
- **Corpus** : l'ordre des fenêtres est `ordre_vdc(n)`, pas un `shuffle`.
- **Initialisation** : la graine ne sert qu'aux poids ; elle est **enregistrée** dans le JSON.

## Ce que cela ne fait pas

- Ce n'est **pas** un générateur cryptographique.
- Ce n'est **pas** un échantillonnage uniforme indépendant : c'est une suite **déterministe** à
  faible discrépance, ce qui est le but.
- Les **corpus multi-sources** gardent des quotas par source ; la suite ordonne, elle ne rééquilibre pas.

## Vérification

```bash
PYTHONPATH=tools:. python3 -m unittest tools.cerveau.tests.test_vdc
```

Le test vérifie les quatre premiers termes, la reproductibilité, la permutation et les bornes.

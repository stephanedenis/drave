# B13 — la phrase simple : r222 écarté, les paires restent 5/10

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ⚠️ **la contrainte
> « phrase simple » (pas de SUB) écarte bien r222, mais le taux reste 5/10** — r409, r410 et r411
> trouvent encore des phrases à **point-virgule** (r344 « Le chat mange ; il dort. », r390 « La
> cloche sonne ; elle appelle. », r354 « Marie et Paul dansent ; ils s'amusent. ») que l'heuristique
> ne marque pas comme subordonnées.

## 1. La contrainte ajoutée

`_simple(a)` : aucune étiquette **SUB** au niveau syntagme. Une question se lie à une phrase
simple. C'est ce qui écarte r222 « Si tu viens, nous partirons. » (SUB).

## 2. Les résultats

| lecture | justes | taux |
|---|---:|---:|
| 10 paires (phrase simple) | **5/10** | 0,50 |
| r418–r422 (non inversées) | 5/5 | 1,00 |
| r408–r412 (inversées) | 0/5 | 0,00 |

| question | trouvé | pourquoi |
|---|---|---|
| r408 | — | aucun candidat ne matche sujet+verbe+simple |
| r409 | **r344** « Le chat mange ; il dort. » | juxtaposition non marquée SUB |
| r410 | **r390** « La cloche sonne ; elle appelle. » | idem |
| r411 | **r354** « Marie et Paul dansent ; ils s'amusent. » | idem |
| r412 | — | aucun candidat |

## 3. Le contrôle négatif

- r418–r422 : 5/5 — la contrainte ne casse rien.
- r222 est bien écarté : la contrainte **fonctionne** sur les SUB marquées.
- Mais les **juxtapositions à point-virgule** passent : l'heuristique ne les étiquette pas SUB.

## 4. Ce qui pourrait rendre ce résultat faux

- L'heuristique ne marque pas les propositions juxtaposées comme subordonnées.
- 10 paires d'un même bloc.
- La contrainte « GV unique » n'est pas encore posée.

## 5. La suite

1. Exiger **un seul GV** (pas de point-virgule) dans l'antécédent.
2. Ou accepter que le lien ne résolve que les paires **simples** (r418–r422) et le documenter.
3. **Parité DRVM/native** (cadenas 3, porte 27, labyrinthe 2).

## 6. Fichiers

- [`pensee-lien-simple.json`](pensee-lien-simple.json) — la mesure et le constat.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `_simple`.

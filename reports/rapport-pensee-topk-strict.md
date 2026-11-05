# B13 — le top-k strict : 0,6069, pas 0,9241

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **176/176 portes** : le top-k publié jusqu'ici acceptait les **sous-chaînes** (`vu` ⊂ `aperçu`,
> `a` ⊂ `parle`) et affichait **0,9241** ; en **égalité exacte**, la bonne cible n'est dans les
> candidats que **88 fois sur 145** — **0,6069**. L'écart de 32 points est un artefact de mesure,
> pas un résultat.
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-topk-strict.json`](pensee-topk-strict.json).

## 1. Les deux top-k (145 segments au bon span)

| mesure | sous-chaîne | **égalité exacte** |
|---|---:|---:|
| top-k (count) | 134 | **88** |
| taux sur les spans | 0,9241 | **0,6069** |
| rendement (÷ 239) | 0,5607 | **0,3682** |

**Ce que ça dit** :

- **Le top-k lenient gonflait le rappel** : 46 « succès » étaient des sous-chaînes (un candidat
  `a` compte pour la cible `parle`, `vu` pour `aperçu`).
- **Le vrai rappel est 0,6069** : la cible exacte est dans la liste 6 fois sur 10 — c'est la
  marge réelle du classement.
- **L'exact (0,8483) dépasse le top-k strict (0,6069)** : normal, le `cible` choisi est souvent
  la bonne réponse même quand la liste ne la contient pas exactement (la règle du type fait
  mieux que les candidats).
- **La négative est explicite** : 0,6069, pas 0,9241.

## 2. Ce que ce banc ne dit pas

- **Les 57 échecs du top-k strict** : non qualifiés.
- **Les candidats** viennent de S (paires « segment → cible ») et du lexique : leur forme
  (texte entier vs tête) explique une partie de l'écart.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition du candidat** : un candidat textuel (`« dans le parc » → a vu`) n'est pas une
  cible réduite ; l'égalité exacte le pénalise ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Réduire les candidats à leur tête** (comme la cible) : le top-k strict remonterait.
2. **Le classement appris** (11 mal classés).
3. **Les subordonnées** : demander à S (81 spans).
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `topk_exact`.
- [`autotest.py`](../tools/pensee/autotest.py) — T173, 176/176.
- [`pensee-topk-strict.json`](pensee-topk-strict.json) — les deux top-k.

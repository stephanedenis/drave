# B15 — M1 sur 66 langues : invariance et exactitude

> **Objet.** Mesurer le codec M1 sur le corpus multilingue existant, par langue et par jeu, avec
> une baseline de surface et un contrôle de surface permutée. **Couche lexicale** : les surfaces
> B7 sont « libellé + coordonnée » ; la réussite mesure la reconnaissance lexicale, pas la
> compréhension d'une phrase libre.

## Corpus

| source | coups | langues | paires |
|---|---:|---:|---:|
| B5 | 79 | 2 (en, fr) + notation | 19 |
| B7 | 449 | 66 | 11 |
| total | **528** | **66** | **30** |

- **71 langues** au lexique, **66** présentes dans le corpus ; absentes : **ky, lo, mt, si, yo**.
- **26 paires multi-variantes**, **15 paires interlangues**.
- 5 langues à **n=1** (am, km, pa, so, zu) : un taux de 0 ou 100 % sur un seul item n'est pas une estimation.

## Résultats globaux

| mesure | valeur |
|---|---:|
| exact avec contexte | **528 / 528 = 100 %** |
| exact sans contexte | **374 / 528 = 70,8 %** |
| canonique | **528 / 528 = 100 %** |
| invariance toutes variantes (contexte) | **26 / 26 = 100 %** |
| invariance interlangues (contexte) | **15 / 15 = 100 %** |
| invariance toutes variantes (sans contexte) | **21 / 26 = 80,8 %** |
| invariance interlangues (sans contexte) | **14 / 15 = 93,3 %** |
| baseline de surface (sans contexte) | **71,8 %** |
| M1 sans contexte sur le même périmètre | 71,6 % |

**Lecture** : avec le contexte, **toutes les variantes d'une paire** produisent le **même code**,
y compris entre langues. Sans contexte, l'invariance tombe à 80,8 % (21/26) et 93,3 % (14/15) :
le contexte est ce qui lève l'ambiguïté.

## Contrôle de surface permutée

| contrôle | attendu | donneur |
|---|---:|---:|
| strict, contexte | **0,0 %** (369) | **90,0 %** |
| strict, sans contexte | **0,0 %** (369) | 84,8 % |
| large, contexte | **0,0 %** (518) | 81,7 % |
| large, sans contexte | **0,0 %** (518) | 74,9 % |

Le code **suit la surface** (donneur 90 %), et **pas l'attendu** d'une autre paire (0 %) :
la liaison surface → code n'est pas un hasard de position.

## Négatifs et limites

- **La baseline de surface ne perd que 0,19 pt** sans contexte : sur ce corpus, la paire suffit
  presque ; la valeur de M1 est le **contexte**, pas la surface seule.
- **Invariance ≠ exactitude** : sans contexte, go et morpion restent souvent invariants (même code
  pour toutes les langues) alors que le code est **faux** (go 0 %, morpion 7,8 % d'exact).
- **Couche lexicale** : 66 langues, pas 71 ; 5 langues à n=1 ; pas d'intervalle de confiance.
- Le corpus est construit par le code : les attendus viennent des mêmes règles que le codec ; le
  contrôle permuté est la seule vérification externe.

## Fichiers

- Code : [`tools/cerveau/multilingue.py`](../tools/cerveau/multilingue.py).
- JSON : [`multilingue.json`](multilingue.json).

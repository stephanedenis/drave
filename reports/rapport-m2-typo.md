# B22 — M2 et les typos : quatre types, un avantage net

> **Question.** B19 montrait que M2 sauve les **suppressions** de caractère. Ici on distingue
> **suppression**, **substitution**, **insertion** et **transposition**, à code constant, sur
> 528 surfaces, 300 pas, graine 1.

## Résultats (3 graines, 300 pas)

| typo | M1 | M2 `de` | M2 `vers` | écart M2−M1 (`de`) |
|---|---:|---:|---:|---:|
| original | **100 %** | 93,61 % | 93,61 % | — |
| suppression | 35,35 % | **72,83 %** | **77,63 %** | +37,5 pts |
| substitution | 27,79 % | **61,64 %** | **68,26 %** | +33,9 pts |
| insertion | 43,31 % | **72,83 %** | **77,40 %** | +29,5 pts |
| transposition | 24,72 % | **73,52 %** | **70,78 %** | +48,8 pts |

**Lecture** :

- M1 **s'effondre** sur les quatre typos (24–45 %).
- M2 **résiste** (62–80 % sur `de`, 66–80 % sur `vers`) : il lit une **forme bruitée de notation**,
  pas une correspondance exacte de surface.
- La **transposition** est la plus destructrice pour M1 (24,1 %) et la plus rentable pour M2
  (+46,5 pts) ; la **substitution** est la plus dure pour M2 (62,3 %).

## Verdict

La niche **typo** de B19 est **robuste aux quatre types**. M2 ne remplace pas M1 (original 100 %
contre 93 %), mais il est un **détecteur de notation bruitée** utilisable en secours.

## Limites

- **3 graines**, 300 pas ; les chiffres sont des moyennes.
- Typos **synthétiques** : une seule position, alphabet restreint.
- Le code attendu est inchangé ; on mesure la lecture de la forme, pas la compréhension.
- M2 reste un **rameau** (B14) ; B22 ne le promeut pas en étage.

## Fichiers

- Code : [`tools/cerveau/m2_typo.py`](../tools/cerveau/m2_typo.py).
- Test : [`tools/cerveau/tests/test_m2_typo.py`](../tools/cerveau/tests/test_m2_typo.py).
- JSON : [`m2-typo.json`](m2-typo.json).

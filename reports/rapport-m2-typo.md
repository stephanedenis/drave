# B22 — M2 et les typos : quatre types, un avantage net

> **Question.** B19 montrait que M2 sauve les **suppressions** de caractère. Ici on distingue
> **suppression**, **substitution**, **insertion** et **transposition**, à code constant, sur
> 528 surfaces, 300 pas, graine 1.

## Résultats

| typo | M1 | M2 `de` | M2 `vers` | écart M2−M1 (`de`) |
|---|---:|---:|---:|---:|
| original | **100 %** | 93,15 % | 93,15 % | — |
| suppression | 32,77 % | **72,60 %** | **80,14 %** | +39,8 pts |
| substitution | 27,08 % | **62,33 %** | **65,75 %** | +35,3 pts |
| insertion | 44,51 % | **66,44 %** | **70,55 %** | +21,9 pts |
| transposition | 24,05 % | **70,55 %** | **73,29 %** | +46,5 pts |

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

- Une graine, 300 pas, pas d'intervalle de confiance.
- Typos **synthétiques** : une seule position, alphabet restreint.
- Le code attendu est inchangé ; on mesure la lecture de la forme, pas la compréhension.
- M2 reste un **rameau** (B14) ; B22 ne le promeut pas en étage.

## Fichiers

- Code : [`tools/cerveau/m2_typo.py`](../tools/cerveau/m2_typo.py).
- Test : [`tools/cerveau/tests/test_m2_typo.py`](../tools/cerveau/tests/test_m2_typo.py).
- JSON : [`m2-typo.json`](m2-typo.json).

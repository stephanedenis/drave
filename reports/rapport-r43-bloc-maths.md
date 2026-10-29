# R4.3 — le bloc maths : 32 formules exactes, 10/10 dérivées, l'oracle sympy d'accord

> **Ligne de roadmap** : R4.3 · **Date** : 2026-10-29 · **Verdict** : ✅ **la formule est
> évaluée, pas lue** — **32/32** formules exactes (fractions), **32/32** recoupées par
> **sympy**, **10/10** dérivées justes sur 5 points, **6/6** équations (dont **1 refus
> attendu** d'une non linéaire), **8/8** refus nommés, et le contrôle « surface » **échoue
> 3/3** (`\frac{1}{3}+\frac{1}{6}` : surface « 1 », calcul `1/2`).
>
> **Dispositif** : CPU seul, aucun modèle ; sous-ensemble **LaTeX** ; arithmétique
> **`fractions.Fraction`** (exacte) et flottant pour les irrationnels ; **oracle
> indépendant = sympy** (évaluation, dérivée, solution) ; fixtures
> `tools/tests/maths/formules.json` ; JSON brut [`r43-bloc-maths.json`](r43-bloc-maths.json) ;
> spec [`bloc-maths.md`](../docs/implantation/bloc-maths.md) ; porte
> [`porte-bloc-maths.sh`](../tools/porte-bloc-maths.sh).

## La question

Une formule mathématique n'est pas du texte : `\frac{1}{3}+\frac{1}{6}` vaut `1/2`, et cette
valeur n'est écrite nulle part. R0.1 range les formules en région `maths` et le texte reste
du texte ; un lecteur de surface peut retrouver les chiffres, jamais le résultat. Peut-on
lire la formule par son **AST**, l'évaluer **exactement**, la **dériver** et la **résoudre**
— et prouver chaque résultat par une seconde implémentation ?

## Les formules — 32/32, et 32/32 confirmées

| famille | exemples | résultat |
|---|---|---|
| fractions | `1/3 + 1/6`, `1/2 + 1/3 + 1/6`, `7/2 − 3/2` | `1/2`, `1`, `2` |
| puissances | `2^{10}`, `2^{-3}`, `-3^{2}`, `(-3)^{2}` | `1024`, `1/8`, `-9`, `9` |
| racines | `\sqrt{144}`, `\sqrt{9}+2^{2}`, `\sqrt{16}+1/2` | `12`, `7`, `9/2` |
| décimales | `1.5+2.25` | `15/4` |
| variables | `1/2·x` (x=3), `2x+3` (x=4), `x^{2}` (x=5) | `3/2`, `11`, `25` |
| irrationnels | `\pi`, `\sin{\pi}`, `\sqrt{2}\cdot\sqrt{2}` | flottant, tolérance 1e-9 |

**Le contrôle indépendant est l'oracle** : chaque AST est traduit en **sympy**, qui évalue la
même formule. **32/32** sont d'accord — deux implémentations, un même nombre. Ce n'est pas
une preuve de justesse absolue (les deux passent par mon parseur), c'est une preuve que
l'**évaluation** et la **traduction** ne se trompent pas ensemble.

## Les dérivées — 10/10

`x^{2}`, `3x^{3}+2x`, `\sin x`, `\cos x`, `\exp x`, `\ln x`, `\sqrt{x}`, `1/x`,
`(x^{2}+1)^{3}`, `2x^{2}-3x+1` — chacune comparée à `sympy.diff` en **5 points rationnels**
(1/2, 1, 2, 3, 5), tolérance `1e-8`. La comparaison est **numérique**, pas symbolique : elle
ne dépend pas d'une simplification.

## Les équations — 6/6, dont un refus

| équation | solution | oracle sympy |
|---|---:|---:|
| `2x+3=7` | **2** | 2 |
| `3x-1=8` | **3** | 3 |
| `\frac{x}{2}+1=3` | **4** | 4 |
| `5(x-1)=10` | **3** | 3 |
| `-2x+4=0` | **2** | 2 |
| `x^{2}=4` | **refus** : non linéaire | — |

La linéarité se **vérifie** (dérivée seconde nulle) : une équation non linéaire est refusée,
pas approximée. C'est le choix du dépôt : un refus nommé vaut mieux qu'une solution fausse.

## Les contrôles négatifs

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **surface** (premier nombre de la formule) | donner une valeur fausse | ✅ **3/3 faux** : `1` au lieu de `1/2`, `2` au lieu de `1024`, `144` au lieu de `13` |
| **macro inconnue** (`\int`) | être refusée | ✅ `Refus: macro inconnue` |
| **accolade ouverte** | être refusée | ✅ `Refus: symbole attendu` |
| **caractère inconnu** (`@`) | être refusé | ✅ `Refus: caractère inconnu` |
| **syntaxe** (`x +`) | être refusée | ✅ `Refus: formule incomplète` |
| **division par zéro** | erreur nommée | ✅ `ErreurCalcul` |
| **racine négative** | erreur nommée | ✅ `ErreurCalcul` |
| **non linéaire** | être refusée | ✅ `Refus: équation non linéaire` |
| **variable absente** | erreur nommée | ✅ `ErreurCalcul` |

## Ce qui pourrait le rendre faux

- **Le corpus est une fixture.** Le dépôt **ne contient pas de corpus LaTeX** : les formules
  mesurées sont les 32 que j'ai choisies. La couverture du parseur est donc une couverture de
  fixtures, pas celle d'un vrai document mathématique — c'est la limite principale.
- **Le sous-ensemble est petit** : pas d'intégrale, de somme, de matrice, de dérivée
  partielle, de `\left`/`\right` complexes ; une macro inconnue est refusée.
- **L'oracle n'est pas indépendant du parseur** : sympy reçoit l'AST que j'ai construit. Il
  valide le **calcul**, pas la lecture du LaTeX.
- **La dérivée est comparée en 5 points** : deux fonctions différentes peuvent coïncider en
  5 points (peu probable ici, mais ce n'est pas une preuve d'égalité symbolique).
- **L'arithmétique exacte s'arrête aux rationnels** : dès qu'un irrationnel entre (π, sin, √2),
  le résultat est flottant et la comparaison devient tolérante.
- **Le coût est linéaire en jetons**, pas en « difficulté » : une expression très profonde peut
  déborder la pile du parseur récursif (non mesuré).

## Ce que ça change pour R4 et R0.3

R4.3 ferme le troisième bloc structurel : **R4.1** (tableaux), **R4.2** (code), **R4.3**
(maths) sont mesurés. **R4.4** (vision/OCR) est le dernier — et il est **bloqué** : aucun
`tesseract`, aucun `pytesseract` sur la machine (manque nommé, pas contourné).

Pour R0.3, le type « maths » n'existe pas dans le banc ; les formules du dépôt sont dans la
prose. Le bloc ajoute une mesure que le banc ne sait pas produire : la **valeur exacte**.

## Reproduire

```bash
bash tools/porte-bloc-maths.sh
python3 tools/bloc_maths.py --mesure reports/r43-bloc-maths.json
python3 tools/bloc_maths.py --calcule "\\frac{1}{3}+\\frac{1}{6}"
python3 tools/bloc_maths.py --derive "x^2+3x" --var x
```

## Ce qui vient

**R4.4 — vision/OCR** : bloqué par l'absence d'OCR (nommé). La suite utile est **R0.4**
(négatifs difficiles) et **R0.5** (routeur, `8156fdcb`), puis **R1** dès que N2 tranche.

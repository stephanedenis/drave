# Le bloc maths — un AST exact, un oracle indépendant

> **Ce que ce document est.** La spécification de **R4.3** : le sous-ensemble LaTeX lu, le
> type des valeurs, les règles de dérivation et de résolution, et ce qui est refusé. Le code
> est `tools/bloc_maths.py` ; la porte est
> [`porte-bloc-maths.sh`](../../tools/porte-bloc-maths.sh) ; les chiffres sont dans
> [`rapport-r43-bloc-maths.md`](../../reports/rapport-r43-bloc-maths.md).
>
> **Chargement** : lire § 2 et § 3 pour coder contre le bloc ; § 6 pour les limites.
>
> **Ce que ce bloc n'est pas** : un moteur de calcul formel général. Pas d'intégrale, pas de
> somme, pas de matrice, pas d'équation non linéaire — et un refus nommé plutôt qu'une
> approximation.

## 1. Le besoin

Une formule mathématique n'est pas du texte : `\frac{1}{3}+\frac{1}{6}` vaut `1/2`, et cette
valeur n'est écrite nulle part. R0.1 range les formules en région `maths` et le texte reste du
texte ; un lecteur de surface retrouve les chiffres, jamais le résultat. Un bloc classique
parse la formule, l'évalue **exactement**, la dérive et la résout — pour un coût constant.

## 2. Le contrat

| élément | contenu |
|---|---|
| **entrée** | une formule ou une équation LaTeX (sous-ensemble), et un environnement de variables |
| **sortie** | la valeur (Fraction ou float), la dérivée (AST), la solution (Fraction) ou un refus nommé |
| **coût** | linéaire en jetons — **×4,1** de temps pour ×4 termes |
| **oracle** | chaque résultat est recoupé par **sympy** (évaluation, dérivée, solution) |
| **rejeu** | l'empreinte de l'AST est stable (aucun horodatage) |

Le module expose `analyse_latex(texte)`, `evaluer(ast, env)`, `derive(ast, variable)`,
`resous(equation, variable)`, `vers_sympy(ast, symboles)` et `empreinte(ast)`.

## 3. Les jetons et la grammaire

**Lu** : nombres entiers et décimaux ; variables d'une lettre et lettres grecques (`\pi`,
`\alpha`, `\beta`, `\gamma`, `\delta`, `\theta`, `\lambda`, `\mu`) ; `+ - * / ^` ; `\frac`,
`\sqrt`, `\cdot`, `\times`, `\div` ; fonctions `\sin`, `\cos`, `\tan`, `\ln`, `\log`, `\exp` ;
parenthèses et accolades ; équations `a = b`.

**Grammaire** (récursive descendante) : `expr → terme (('+'|'-') terme)*` ;
`terme → facteur (('*'|'/') facteur | implicite)*` ; `facteur → ('+'|'-') facteur | atome '^' facteur` ;
`atome → nombre | variable | '(' expr ')' | '{' expr '}' | \frac{…}{…} | \sqrt{…} | fonction atome`.
La **multiplication implicite** (`2x`, `\frac{1}{2}x`, `\sqrt{2}\sqrt{3}`) est reconnue.

**Refusé en le nommant** : macro inconnue (`\int`), caractère inconnu, accolade non fermée,
formule incomplète, reste après la formule, `\pm` (ambigu).

## 4. Les valeurs et l'exactitude

`fractions.Fraction` dès que le résultat est rationnel : `1/3 + 1/6 = 1/2`, `2^{-3} = 1/8`,
`\frac{10}{4} = 5/2`. Les irrationnels (`\pi`, `\sin`, `\sqrt{2}`) passent en **flottant**, et
la comparaison devient tolérante (`1e-9`) — le contrat dit lequel des deux régimes s'applique.

`\sqrt` est **exact quand le radicande est un carré parfait** (`\sqrt{144} = 12`), flottant
sinon. Une racine négative est une `ErreurCalcul`, pas un complexe implicite.

## 5. Dérivation et résolution

**Dérivation** : somme, produit, quotient, puissance (exposant constant), chaîne pour `sin`,
`cos`, `tan`, `ln`, `log`, `exp`, `sqrt`. Une puissance à exposant variable (`x^y`) est
**refusée** (elle demanderait `ln` et une règle qui n'est pas dans le sous-ensemble).

**Résolution** : une équation est linéaire si la dérivée seconde de `gauche − droite` est
nulle ; la solution est `−f(0)/f'(0)`, exactement. Une équation **non linéaire** est refusée
(nommée), jamais approximée ; une équation sans solution unique (`a = 0`) aussi.

## 6. L'oracle et ses limites

L'AST est traduit en **sympy** : `\pi` → `sp.pi`, les rationnels → `sp.Rational`, les fonctions
→ `sp.sin`… L'oracle valide le **calcul** et la **traduction**, pas la lecture du LaTeX (il
reçoit l'AST). Les dérivées sont comparées **numériquement en 5 points**, pas symboliquement.

## 6 bis. La restitution (miroir)

La formule se **rend** en LaTeX parenthésé, puis se **relit** : 32 formules et 10 dérivées
retrouvent le même AST (les constantes sont repliées à la construction, donc `\frac{1}{2}` et
`1/2` sont le même nœud). Le contrôle négatif est la formule **sans parenthèses** : la
précédence change, l'AST change.

Porte : [`porte-miroir-blocs.sh`](../../tools/porte-miroir-blocs.sh).

## 7. Ce que le bloc ne fait pas

- **pas de LaTeX complet** : intégrales, sommes, matrices, dérivées partielles, `\left`/`\right`
  imbriqués complexes → refus nommé ;
- **pas de corpus dans le dépôt** : le dépôt ne contient pas de formules LaTeX hors fixtures ;
  la couverture mesurée est celle des 32 formules choisies ;
- **pas d'équation non linéaire** : refusée ;
- **pas d'arithmétique exacte des irrationnels** : flottant, tolérance ;
- **pas de preuve d'égalité symbolique** : 5 points, pas une identité.

## 8. Voir aussi

- [R4.3 — le bloc maths](../pilotage/backlog/R43-bloc-maths.md) — la fiche de fonctionnalité.
- [Le bloc tableaux](bloc-tableaux.md) et [le bloc code](bloc-code.md) — les deux autres blocs
  structurels, mesurés.
- [Le graphe de document](document-graph.md) — les régions `maths` de R0.1.
- [Le banc de lecture rapide](banc-lecture.md) — ce que le banc ne demande pas.

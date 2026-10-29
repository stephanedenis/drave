# Le miroir des trois blocs : 34/34 tableaux, 296/296 modules, 42/42 formules

> **Lignes de roadmap** : R4.1, R4.2, R4.3 (contrôle croisé) · **Date** : 2026-10-29 ·
> **Verdict** : ✅ **les trois blocs restituent ce qu'ils lisent** — 34/34 grilles rendues en
> Markdown/CSV puis relues à l'identique, 296/296 modules Python rendus par `ast.unparse`
> puis relus au MÊME AST, 42/42 formules et dérivées rendues en LaTeX puis relues au même
> AST. Et pour chacun, le **contrôle négatif échoue** : le texte plat perd la grille, la
> source aplatie perd l'AST, la formule sans parenthèses perd la précédence.
>
> **Dispositif** : CPU seul, aucun modèle ; la porte
> [`porte-miroir-blocs.sh`](../tools/porte-miroir-blocs.sh) appelle les trois blocs en mode
> `--miroir` ; JSON bruts [`r41`](r41-bloc-tableaux.json), [`r42`](r42-bloc-code.json),
> [`r43`](r43-bloc-maths.json) (clé `miroir`) ; specs
> [`bloc-tableaux`](../docs/implantation/bloc-tableaux.md),
> [`bloc-code`](../docs/implantation/bloc-code.md),
> [`bloc-maths`](../docs/implantation/bloc-maths.md).

## La question

La règle du dépôt (n° 6) est que **toute mesure d'entrée se double d'une mesure de sortie** :
un lecteur qui ne sait pas restituer ce qu'il a lu n'a pas lu, il a filtré. R4.1, R4.2 et
R4.3 mesuraient l'entrée — la grille, l'AST, la valeur. Restituent-ils ? La restitution
n'est pas la même chose que la fidélité : rendre un tableau, un module ou une formule et le
**relire** doit redonner le **même objet**, pas seulement le même nombre.

## Les trois miroirs

| bloc | rendu | relecture | exacts |
|---|---|---|---:|
| **R4.1 tableaux** | Markdown (ou CSV) | `markdown_texte` / `csv_texte` | **34/34** |
| **R4.2 code** | `ast.unparse` | `ast.parse` + clé d'AST | **296/296** |
| **R4.3 maths** | LaTeX (parenthésé) | `analyse_latex` | **42/42** |

**R4.1** — 32 tableaux Markdown, 1 CSV (Glottolog) et 1 HTML sans fusion : la grille rendue
puis relue garde les **en-têtes**, les **dimensions** et le **texte de chaque cellule**. Le
seul non représentable est `entites.html`, sans en-tête : nommé, pas inventé. Les fusions
(`rowspan`/`colspan`) ne sont **pas** représentables en Markdown/CSV et sont comptées à
part — le miroir ne prétend pas les restituer.

**R4.2** — les 296 modules de `tools/*.py` sont rendus par `ast.unparse`, relus, et la
**forme de l'AST** (type de chaque nœud + constante, nom, argument) est identique. Les
numéros de ligne changent, c'est attendu : la restitution compare le **sens**, pas la mise
en page.

**R4.3** — 32 formules et 10 dérivées rendues avec des **parenthèses partout**, puis relues :
l'AST est identique, au bit près (les constantes sont repliées à la construction, donc
`\frac{1}{2}` et `1/2` sont le même nœud). La restitution est LaTeX valide et sans ambiguïté.

## Les contrôles négatifs

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **texte plat** d'une grille (rangées tabulées) | perdre la grille | ✅ plus aucune barre, **0 tableau** relu |
| **source aplatie** (`if x: a = 1 b = 2`) | perdre l'AST | ✅ `Refus: syntaxe` |
| **formule sans parenthèses** (`1 + 2 \cdot 3` au lieu de `(1 + 2) \cdot 3`) | perdre la précédence | ✅ AST différent |

**Ce que ces contrôles prouvent** : la restitution n'est pas triviale — un rendu qui perd la
structure est détecté. Ils ne prouvent pas que toute perte serait détectée : le miroir
compare une forme canonique, pas une sémantique.

## Ce qui pourrait le rendre faux

- **Le miroir compare une forme, pas un sens.** Deux AST différents peuvent calculer la même
  chose ; deux grilles identiques peuvent avoir des provenances différentes (les offsets ne
  sont pas rendus). C'est un contrôle de **structure**, pas de fidélité au document.
- **La restitution est la mienne.** Markdown, `ast.unparse` et mon LaTeX parenthésé sont des
  rendus choisis ; un autre rendu (même correct) donnerait un autre texte.
- **Les fusions de tableau échappent au miroir** : Markdown/CSV ne les expriment pas ; elles
  sont comptées à part (1 tableau sans en-tête, les fixtures à fusion exclues du corpus).
- **Les numéros de ligne changent** dans le code : le miroir ne prouve pas la conservation de
  la mise en page, seulement de la structure.
- **42 formules** : le corpus maths est une fixture (le dépôt n'a pas de corpus LaTeX).

## Ce que ça change

Les trois blocs structurels sont désormais mesurés **en entrée et en sortie** : la règle 6
est satisfaite pour eux, et la porte
[`porte-miroir-blocs.sh`](../tools/porte-miroir-blocs.sh) le vérifie en quelques secondes.
C'est aussi ce qui rend une **boucle** possible : lire → restituer → relire est la base d'un
rejeu fidèle, et c'est ce que R2 (mémoire) et R3 (restitution) demanderont.

## Reproduire

```bash
bash tools/porte-miroir-blocs.sh
python3 tools/bloc_tableaux.py --miroir
python3 tools/bloc_code.py --miroir
python3 tools/bloc_maths.py --miroir
```

# R4.2 — le bloc code : 294 fichiers, 453 038 nœuds, 24/24 extraits exécutés

> **Ligne de roadmap** : R4.2 · **Date** : 2026-10-29 · **Verdict** : ✅ **le code se lit par
> son AST et son exécution** — **294/294** fichiers de `tools/` acceptés (**453 038** nœuds,
> **1 722** fonctions, **73** classes), **24/24** extraits exécutés à la valeur exacte,
> **7/7** refus nommés, et le contrôle « texte seul » **échoue 3/3** (2**10+24 : texte 2,
> exécution 1048).
>
> **Dispositif** : CPU seul, aucun modèle ; langage **Python 3** (`ast`), interpréteur **en
> sable** (liste blanche de nœuds, pas d'import, pas d'attribut, pas, itérations et
> profondeur bornés) ; fixtures `tools/tests/code/` ; JSON brut
> [`r42-bloc-code.json`](r42-bloc-code.json) ; spec
> [`bloc-code.md`](../docs/implantation/bloc-code.md) ; porte
> [`porte-bloc-code.sh`](../tools/porte-bloc-code.sh).

## La question

R0.1 range le code en **région** et le texte reste du texte. Le banc R0.3 pose des questions
de valeurs numériques par deux mots rares : sur du code, il mesure la recherche d'une ligne,
pas la compréhension. Peut-on lire du code par sa **structure** — portée, flux, exécution —
et répondre exactement, sans modèle ?

## Le parseur

| mesure | valeur |
|---|---:|
| fichiers de `tools/*.py` | **294** |
| acceptés par `ast.parse` | **294** (100 %) |
| nœuds | **453 038** |
| fonctions | **1 722** |
| classes | **73** |
| temps de parse | **3,27 s** (11 ms/fichier) |

Une syntaxe fausse est **refusée en la nommant** (`Refus: syntaxe (ligne 1) : invalid
syntax`) : c'est le contrôle `erreur.py`, et il ne passe pas en silence.

## La portée et le flux

| question | réponse |
|---|---|
| `x` ligne 2 de `portee.py` | **module** |
| `x` ligne 4 (dans `f`) | **fonction** |
| `y = f()` | **2** (la fonction a rendu son `x` local, pas le `x` du module) |
| noms lus et jamais liés dans `flux.py` | **`sous_total`**, ligne 1 |
| faux positifs sur `portee.py` | **0** |

La résolution remonte la chaîne des portées (module → fonction → classe → compréhension) et
s'arrête à la plus profonde qui contient la ligne. Un nom lu et jamais lié est signalé ; un
nom lié plus tard dans le module ne l'est pas (Python le résout à l'appel).

## L'exécution — 24 extraits, 24 valeurs exactes

| extrait | attendu | rendu |
|---|---:|---:|
| `2 ** 10 + 24` | 1048 | **1048** |
| `17 // 5` / `17 % 5` | 3 / 2 | **3 / 2** |
| `[i * i for i in range(5)]` | `[0, 1, 4, 9, 16]` | **identique** |
| `sum([i for i in range(6) if i % 2 == 0])` | 6 | **6** |
| `def carre(x): return x * x` · `carre(7)` | 49 | **49** |
| `def f(n): … for … return s` · `f(5)` | 10 | **10** |
| `def fact(n): … fact(n - 1)` · `fact(5)` | 120 | **120** |
| `a, b = 3, 4` · `a * b` | 12 | **12** |

L'interpréteur rend la **dernière expression** et les variables finales ; c'est un REPL
borné, pas un exécuteur de programme. Ce qu'il refuse, il le refuse **par son nom** (voir
plus bas), jamais en silence.

## Les contrôles négatifs

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **texte seul** (premier nombre de la source) | donner une valeur fausse | ✅ **3/3 faux** : 2 au lieu de 1048, 10 au lieu de 45, 3 au lieu de 14 |
| **syntaxe fausse** | être refusée | ✅ `Refus: syntaxe` |
| **import** | ne pas s'exécuter | ✅ `Refus: import interdit` |
| **attribut** | ne pas s'exécuter | ✅ `Refus: attribut interdit` |
| **division par zéro** | erreur nommée | ✅ `ErreurExecution` |
| **nom inconnu** | erreur nommée | ✅ `ErreurExecution` |
| **boucle infinie** | borne nommée | ✅ `ErreurExecution: boucle bornée dépassée (10000)` |
| **appel interdit** (`open`) | refusé | ✅ `ErreurExecution: nom inconnu : open` |

**Ce que le contrôle prouve, et ce qu'il ne prouve pas** : il prouve que la valeur d'une
expression est dans l'exécution, pas dans la ligne. Il ne prouve pas qu'un modèle ne peut pas
apprendre à calculer — il prouve qu'un **bloc classique** le fait exactement, pour un coût
constant.

## Ce qui pourrait le rendre faux

- **Un seul langage.** Python 3 par `ast` ; le JavaScript, le Rust ou le C du dépôt ne sont
  pas lus. La couverture de 294/294 est celle de `tools/*.py`, pas du dépôt entier.
- **Un sous-ensemble.** Pas d'import, pas d'attribut, pas de classe exécutée, pas de closure
  par référence, pas de générateur : un extrait qui en use est **refusé** (nommé), pas exécuté.
- **Les fixtures sont les miennes.** Les 24 extraits sont simples et choisis pour être justes ;
  ce n'est pas un tirage aléatoire sur un corpus de code réel.
- **La récursion est bornée à 50** et les boucles à 10 000 itérations : un programme correct
  mais plus long est refusé (nommé) — c'est le prix du sable.
- **Le texte seul est un gabarit naïf** (premier nombre de la source) : un lecteur plus malin
  trouverait parfois la valeur par chance. Le contrôle prouve la **nécessité** de calculer,
  pas l'impossibilité de deviner.

## Ce que ça change pour R0.3

Le banc R0.3 a un type **« code »** (54 questions sur 249). Comme pour les tableaux, ses
questions demandent la **valeur numérique** du passage : elles se répondent par recherche de
ligne. Le 0,722 du lexical y est la sélection du bon passage, pas une lecture de code. R4.2
ajoute une autre mesure : la **valeur calculée**, la **portée**, le **nom libre** — trois
choses que le texte ne contient pas.

## Reproduire

```bash
bash tools/porte-bloc-code.sh
python3 tools/bloc_code.py --mesure reports/r42-bloc-code.json
python3 tools/bloc_code.py --execute "2**10 + 24"
python3 tools/bloc_code.py --json tools/bloc_tableaux.py
```

## Ce qui vient

**R4.3 — le bloc maths** (LaTeX/MathML, CAS, contrôle « surface »), puis **R4.4 — vision/OCR**
après R4.1–R4.3. La ligne lecteur garde **R0.4** (négatifs difficiles) et **R0.5** (routeur).

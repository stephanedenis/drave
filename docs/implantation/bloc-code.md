# Le bloc code — un AST, des portées, une exécution en sable

> **Ce que ce document est.** La spécification de **R4.2** : ce que lire du code veut dire,
> ce que l'AST porte, quelles constructions sont permises, et ce qui est refusé. Le code est
> `tools/bloc_code.py` ; la porte est
> [`porte-bloc-code.sh`](../../tools/porte-bloc-code.sh) ; les chiffres sont dans
> [`rapport-r42-bloc-code.md`](../../reports/rapport-r42-bloc-code.md).
>
> **Chargement** : lire § 2 et § 4 pour coder contre le bloc ; § 6 pour les limites.
>
> **Ce que ce bloc n'est pas** : un exécuteur de programmes. Il répond à des questions
> **bornées** sur un extrait (valeur, portée, nom libre) ; il n'exécute ni import, ni réseau,
> ni fichier.

## 1. Le besoin

Un document de code n'est pas de la prose : la réponse à « que vaut cette expression ? » est
dans l'**exécution** ; la réponse à « quelle variable cette ligne lit-elle ? » est dans la
**portée**. R0.1 range le code en région et le texte reste du texte ; le banc R0.3 demande des
valeurs par deux mots rares — il mesure la recherche d'une ligne, pas la compréhension. Un
bloc classique lit la structure, et il la lit exactement.

## 2. Le contrat

| élément | contenu |
|---|---|
| **entrée** | un fichier Python (ou une chaîne) et une question |
| **sortie** | l'AST, les portées et leurs symboles, une valeur d'exécution, des noms libres |
| **coût** | linéaire en nœuds — **×4,4** de temps pour ×4 nœuds |
| **borne** | pas ≤ 200 000, itérations ≤ 10 000, profondeur ≤ 50, collections ≤ 100 000 |
| **trace** | nombre de pas, sortie de `print`, variables finales |
| **rejeu** | l'empreinte de l'AST est stable (aucun horodatage) |

Le module expose `analyse(source)`, `resous(module, nom, ligne)`, `noms_libres(module)`,
`empreinte(module)` et `execute(source)`.

## 3. L'AST et les portées

| élément | règle |
|---|---|
| **portée** | module → fonction → classe → compréhension ; `lambda` a la sienne |
| **paramètre** | lié dans la portée de la fonction (positionnels, `*args`, `**kwargs`, keyword-only) |
| **affectation** | `Name`, `Tuple`/`List` (dépaquetage), `Subscript` ; `global`/`nonlocal` remontent la déclaration |
| **import** | l'alias est un symbole de genre `import` (il n'est jamais exécuté) |
| **lecture** | chaque `Name` en `Load` est enregistré avec sa ligne et sa portée |
| **résolution** | la portée la plus profonde qui contient la ligne, puis la chaîne des parents |
| **nom libre** | lu et jamais lié dans la chaîne, hors `LISIBLES` — signalé avec sa ligne |
| **refus** | syntaxe fausse → `Refus: syntaxe (ligne, message)` |

Un nom lié **plus tard** dans le module n'est pas signalé : Python le résout à l'appel, et
le déclarer libre serait un faux positif. C'est une limite assumée (voir § 6).

## 4. L'exécution en sable

**Liste blanche de nœuds** — expressions : constante, nom, binaire, unaire, booléen,
comparaison chaînée, conditionnel, appel, indice, tranche, liste, tuple, ensemble,
dictionnaire, compréhension de liste. Instructions : affectation, affectation augmentée,
affectation annotée, `if`, `for`, `while`, `def`, `return`, `pass`, `break`, `continue`.

**Liste blanche d'appels** : `len`, `abs`, `min`, `max`, `sum`, `sorted`, `range`, `int`,
`float`, `str`, `bool`, `list`, `tuple`, `dict`, `set`, `round`, `enumerate`, `zip`, `any`,
`all`, `print`, `reversed`, `chr`, `ord` — et les fonctions définies dans l'extrait.

**Tout le reste est refusé en le nommant** : import, attribut, classe exécutée, `with`, `try`,
`raise`, `assert`, `delete`, f-string, lambda, générateur. Un nœud ignoré serait une exécution
qui n'a pas eu lieu — c'est précisément ce qu'on ne veut pas.

**Bornes** : le nombre de pas, les itérations, la profondeur d'appel et la taille des
collections sont plafonnés ; une boucle infinie rend `ErreurExecution: boucle bornée dépassée`
en un temps fini.

## 5. La porte

```
bash tools/porte-bloc-code.sh
```

Elle exige, ensemble : **tout le corpus** `tools/*.py` accepté ; **24/24** extraits à la
valeur exacte ; la portée de `x` (module/fonction) et `y = 2` ; `sous_total` signalé et zéro
faux positif ; le **texte seul qui échoue 3/3** ; **7 refus nommés** ; le coût linéaire ; le
rejeu identique. Une seule condition manquante rend la porte rouge.

## 6. Ce que le bloc ne fait pas

- **pas d'autre langage** : Python seulement ; le reste du dépôt (Rust, JS, C) n'est pas lu ;
- **pas d'import ni d'attribut** : `import os`, `obj.methode()` → refus nommé ;
- **pas de classe exécutée**, pas de générateur, pas de f-string ;
- **pas de closure par référence** : une fonction capture l'environnement de définition, mais
  la portée locale d'un appel est une copie ;
- **pas de faux positif évité** : un nom défini plus tard est considéré lié (comme Python) ;
- **pas de preuve de sécurité formelle** : la liste blanche est une garantie de construction,
  pas un bac à sable système (le processus n'est pas isolé).

## 7. Voir aussi

- [R4.2 — le bloc code](../pilotage/backlog/R42-bloc-code.md) — la fiche de fonctionnalité.
- [Le graphe de document](document-graph.md) — les régions et leur provenance (R0.1).
- [Le bloc tableaux](bloc-tableaux.md) — le même motif pour les tableaux (R4.1).
- [Le banc de lecture rapide](banc-lecture.md) — ce que le banc mesure, et son type « code ».

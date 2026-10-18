# Directives de l'agent — Drave Natif

> Ce fichier est la **première chose à lire** avant d'agir sur ce dépôt. Il dit la **mission**, l'**ordre des
> priorités**, et les **règles de rangement** — pas l'historique (il est dans `journal/`).

## 1. La mission, et l'ordre des priorités

Drave Natif se construit **couche par couche**, et on ne passe pas à la suivante tant que la précédente est
**perfectible** :

1. **Les modules d'ENTRÉE et de SORTIE linguistiques** — c'est la priorité absolue. Ils doivent être **parfaits** et
   **très riches en langues et en domaines** : lire et produire toutes les langues, dialectes et styles, dans les
   registres techniques, littéraires, juridiques, quotidiens.
   - On les **teste en qualité de traducteur** — c'est le juge de paix : *restitution* (même langue, à l'identique)
     et *traduction* (même sens, autre langue, autre style).
   - **On continue tant qu'ils sont perfectibles**, et on ne « déclare complet » que sur des chiffres qui couvrent
     les langues, les dialectes, les styles et les domaines.
2. **Le module de pensée abstraite, indépendant de la langue** — seulement après. Il ne peut pas être conçu sur une
   entrée-sortie qui n'est pas fiable.

**Le temps imparti est un plancher, pas un plafond** (*carpe diem*, `docs/relations-humaines.md` § Addendum) :
on ne s'arrête pas parce qu'une échéance est passée ; on s'arrête quand la couche est faite, mesurée et écrite.

## 2. Le rangement : `docs/` n'est pas `reports/`

C'est la règle la plus souvent violée, et elle est **stricte** :

| dossier | ce qu'il contient | ce qu'il ne contient **jamais** |
|---|---|---|
| **`docs/`** | l'**état actuel**, la **mission**, la **vision**, l'**architecture**, les **concepts** et les **modes d'emploi** — ce qui reste vrai quand les chiffres changent | des **résultats** de mesure, des tableaux de chiffres, des comptes rendus de round |
| **`reports/`** | les **résultats mesurés** : fiches, séries de mesures, tableaux, erratums, récits de round | la documentation de référence |
| **`journal/`** | le **récit daté** : ce qui a été fait, quand, et ce qu'on en a appris | les chiffres seuls (ils vont dans `reports/`) |
| **`data/`** | les corpus et leur généalogie (`data/udhr/`, `data/corpus_*.txt`) | du code |

Une page de `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/` ; il reste dans `docs/` un
**résumé de l'état** (ce qu'on sait, ce qu'on ne sait pas, et le lien vers la fiche).
À chaque cycle : `docs/en-cours.md` dit l'état **courant** en quelques lignes, pas l'historique.

## 3. Ce qu'un résultat doit porter, à chaque fois

- le **chiffre**, la **mesure** qui le produit, et le **dispositif** (quel corpus, quel modèle, quelle couche,
  quel découpage) ;
- le **contrôle négatif** quand il y en a un (hasard, étiquettes mélangées, corpus mélangé) — sans lui, le chiffre
  n'est pas un résultat ;
- **à côté du chiffre, ce qui pourrait le rendre faux** (les pièges d'instrument) ;
- un **commit** par résultat mesuré, et la **fiche** dans `reports/`, le **récit** dans `journal/`, l'**état** dans
  `docs/en-cours.md`.

## 4. Les portes

`bash tools/toutes-les-portes.sh` écrit `registre.txt` ; on lit le verdict par `awk '$2 != 0'` — **jamais** par les
marqueurs ni à travers un tube. Les deux rouges structurelles connues sont `porte-indice` et `porte-melange` ; toute
**autre** rouge est une régression et se corrige avant de continuer.

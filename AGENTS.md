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


## 5. Étudier Panini et Nipada, régulièrement

Les projets **`../Panini/`** et **`../Panini-Research/`** poursuivent le **même objectif par une approche
complémentaire** : Panini décompose le texte en **14 atomes sémantiques**, Nipada le fait tourner comme un tissu
computationnel — *algébrique, là où Drave est statistique*. Ils tiennent le **système linguistique** et généralisent
une **généalogie des langues, dialectes et styles**.

**Règle** : à chaque cycle, lire ce qui a bougé chez eux (docs, publications, journaux de bord) et confronter leurs
résultats aux nôtres. Ce qui en sort va dans [`docs/genealogie-des-langues.md`](docs/genealogie-des-langues.md)
(la théorie) — jamais les chiffres (ils vont dans `reports/`).

**Leur avertissement, à ne pas oublier** ✗✓ : leur signature lexicale capte **l'époque** (β +0,138) bien plus que la
**filiation** (β +0,049) — *la surface transmet les signifiants, pas la généalogie*. Tout test de style doit donc
**contrôler la date**, et tout test de famille doit **contrôler la surface**.

## 6. La documentation : `docs/` reflète **tous** les chantiers, et une synthèse toujours à jour

- **`docs/en-cours.md` est le tableau de bord** : il porte les **sept chantiers**, leurs **dépendances**, leurs
  **sous-chantiers indépendants** (ce qui peut tourner en parallèle) et leur **état**. Il porte aussi, en tête, une
  **synthèse** de l'état de la couche — celle qu'on lit si on ne lit qu'une page.
- **`reports/` reçoit les données intermédiaires et les références** de nos travaux : fiches de mesure, JSON de
  résultats, dumps d'expériences, brouillons de référence. *Tout ce qui n'est pas « ce qui reste vrai quand les
  chiffres changent » va dans `reports/`, jamais dans `docs/`.*
- **`docs/synthese/` porte la synthèse théorique** (7 chapitres, 7 schémas), et son `index.md` doit refléter les
  sept chantiers.

### 6.1 La revue de fin de sous-chantier (obligatoire)

**Quand** : à la **fin de chaque sous-chantier** (et au minimum une fois par cycle), avant le commit de clôture.
**Quoi** : `python3 tools/revue_documentation.py` vérifie, et **corrige** avant de continuer :

1. **classement** : un résultat qui traîne dans `docs/` est déplacé dans `reports/` ; une page de `docs/` qui n'a
   plus de « ce qui reste vrai » est supprimée ;
2. **structure** : chaque chantier de `en-cours.md` a son entrée, son état, sa fiche, et ses sous-chantiers ;
3. **annotation** : tous les **liens internes** résolvent (docs ↔ reports ↔ journal), et les **sources externes**
   (Glottolog, Gutenberg, Unicode UDHR, Panini/Nipada) sont citées avec leur URL ou leur chemin ;
4. **fraîcheur** : la date de `en-cours.md` est l'**heure locale** du dernier commit (jamais une estimation) ;
5. **cohérence** : la synthèse (`docs/synthese/index.md`) et le tableau de bord disent la même chose.

*Une documentation qui n'est pas revue à la fin d'un sous-chantier est une documentation qui mentira au cycle
suivant* ✗✓.

# Étudier Panini et Nipada, régulièrement

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **à chaque cycle**, avant de conclure sur
> la généalogie, les styles ou les familles de langues.

## Pourquoi

Les projets **`../Panini/`** et **`../Panini-Research/`** poursuivent le **même objectif par une approche
complémentaire** : Panini décompose le texte en **14 atomes sémantiques**, Nipada le fait tourner comme un tissu
computationnel — *algébrique, là où Drave est statistique*. Ils tiennent le **système linguistique** et généralisent
une **généalogie des langues, dialectes et styles**.

## La règle

À chaque cycle, **lire ce qui a bougé chez eux** (docs, publications, journaux de bord, `git log`) et **confronter
leurs résultats aux nôtres**. Ce qui en sort va dans [`docs/genealogie-des-langues.md`](../genealogie-des-langues.md)
(la théorie) — **jamais les chiffres** (ils vont dans `reports/`).

## Leur avertissement, à ne pas oublier ✗✓

Leur signature lexicale capte **l'époque** (β **+0,138**) bien plus que la **filiation** (β **+0,049**) — *la
surface transmet les signifiants, pas la généalogie*.

Conséquences pour nos tests :

- tout test de **style** doit **contrôler la date** (comparer des couples contemporains) ;
- tout test de **famille** doit **contrôler la surface** (écriture, époque, domaine) ;
- une similarité de surface entre deux langues n'est pas une preuve de parenté : c'est une **hypothèse** à
  contrôler.

## Ce que Drave apporte en retour

Nos mesures de **retrieval** (le même contenu se retrouve-t-il d'une langue à l'autre ?) et de **généalogie**
(l'alignement suit-il les familles Glottolog ?) sont la face **statistique** de leur face algébrique. La
confrontation se fait sur les **chiffres** (dans `reports/`), pas sur les intuitions.

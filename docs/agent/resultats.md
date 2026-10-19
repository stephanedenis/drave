# Ce qu'un résultat doit porter

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
> résultats, ou un message de commit.

## Les cinq pièces d'un résultat

1. **Le chiffre** — la valeur, avec son unité et son arrondi utile (jamais plus de chiffres que l'instrument n'en
   porte) ;
2. **La mesure qui le produit** — le calcul exact, la métrique (chrF, précision, rappel, AUC…), et ce qu'elle ne
   mesure pas ;
3. **Le dispositif** — quel corpus (et sa provenance), quel modèle (taille, quantification, date de coupure),
   quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
   grammaticale ; si c'est un jeton, le dire comme **technique**), quels réglages (prompt, gabarit, longueur de
   sortie, graine) ;
4. **Le contrôle négatif** — hasard, étiquettes mélangées, corpus mélangé, chapitres permutés, source changée. *Sans
   contrôle négatif, le chiffre n'est pas un résultat* ✗✓ ;
5. **Ce qui pourrait le rendre faux** — les pièges d'instrument, les biais du corpus, les artefacts de taille, les
   conditions qui ne sont pas celles du réel.

## Le commit, la fiche, le récit, l'état

Un **commit par résultat mesuré** (ou par paire de mesures liées), avec :

| où | quoi |
|---|---|
| `reports/` | la **fiche** : chiffres, dispositif, contrôles, pièges, limites ; les JSON de résultats bruts |
| `journal/` | le **récit daté** : ce qui a été fait, quand, et ce qu'on en a appris (généré par `tools/journal_auto.py`, notes à la main entre les marqueurs) |
| `docs/en-cours.md` | l'**état** : la synthèse, la ligne du chantier, les questions ouvertes |

Le message de commit suit la convention du dépôt : **une phrase-titre en majuscules** qui porte le chiffre et le
verdict, puis le corps qui donne le dispositif et les contrôles. Il est lu par le journal : il doit rester vrai sans
la fiche.

## Ce qui n'est pas un résultat

- un chiffre sans dispositif (« 73 % ») ;
- un chiffre sans contrôle (« le modèle préfère X ») ;
- un chiffre sur un texte que le modèle a pu **mémoriser** sans le dire (mesure 61 : l'UDHR récitée) ;
- une impression de lecture, même juste : elle se mesure ou elle reste une hypothèse.

## La règle de tri

*Tout ce qui n'est pas « ce qui reste vrai quand les chiffres changent » va dans `reports/`, jamais dans `docs/`.*
La théorie et les modes d'emploi restent dans `docs/` ; les tableaux, les séries et les erratums vont dans
`reports/`.

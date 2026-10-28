# La documentation de Drave — quatre familles

> **`docs/` dit ce qui reste vrai** : la méthode, l'état, la théorie, l'implantation. Les **chiffres** et les
> séries vivent dans [`reports/`](../reports/) ; le **récit daté** dans [`journal/`](../journal/). Une page de
> `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/`.

> **Chargement facultatif.** Aucun document de ce dossier n'est nécessaire pour commencer une tâche : lire
> [`AGENTS.md`](../AGENTS.md), puis le document de la tâche. Le reste se charge au besoin.

## En trois portes

| si vous voulez… | lisez |
|---|---|
| **comprendre le projet** | [la vision](theorie/vision.md) · [la mission](methode/mission.md) · [le protocole sémantique](theorie/protocole-semantique.md) · [le glossaire](theorie/glossaire.md) · [la synthèse](theorie/synthese/index.md) |
| **faire** (résultat, porte, rangement, Panini, miroir, ressources) | [`methode/`](methode/) · [l'organisation](methode/organisation-du-depot.md) · [l'utilisation](pilotage/utilisation.md) |
| **savoir où l'on en est** | [l'état](pilotage/en-cours.md) · [la roadmap](pilotage/roadmap.md) · [les résultats](../reports/README.md) · [les portes](pilotage/references-non-regression.md) · [le journal](../journal/README.md) |

## Méthode — comment on travaille

| document | pour quoi |
|---|---|
| [`methode/mission.md`](methode/mission.md) | la vision, les deux programmes, l'ordre des priorités |
| [`methode/echantillonnage-vdc.md`](methode/echantillonnage-vdc.md) | échantillonnage déterministe des fenêtres (van der Corput) |
| [`methode/resultats.md`](methode/resultats.md) | ce qu'un résultat doit porter : chiffre, contrôle, commit, fiche |
| [`methode/rangement.md`](methode/rangement.md) | les quatre familles de `docs/`, `reports/`, `journal/`, `data/`, la revue |
| [`methode/organisation-du-depot.md`](methode/organisation-du-depot.md) | où écrire quoi, comment nommer et horodater |
| [`methode/portes.md`](methode/portes.md) | lancer les portes, lire le registre, les rouges connues |
| [`methode/illustrations.md`](methode/illustrations.md) | les illustrations : SVG obligatoire, conversion, vérification |
| [`methode/panini-nipada.md`](methode/panini-nipada.md) | Panini/Nipada, l'avertissement époque/filiation |
| [`methode/miroir.md`](methode/miroir.md) | le miroir entrée/sortie et ses quatre règles |
| [`methode/ressources.md`](methode/ressources.md) | le matériel, les GPU, la composition mesurée |
| [`methode/contexte.md`](methode/contexte.md) | le budget de contexte : ce qu'on charge, ce qu'on ne charge pas |
| [`methode/continuite.md`](methode/continuite.md) | les cycles DSH, les sous-agents, la discipline de `en-cours` |
| [`methode/modularisation.md`](methode/modularisation.md) | diviser ou paralléliser : ce que la mesure dit |
| [`methode/relations-humaines.md`](methode/relations-humaines.md) | *carpe diem*, le temps et les échanges |

## Pilotage — planification, état, suivi

| document | pour quoi |
|---|---|
| [`pilotage/en-cours.md`](pilotage/en-cours.md) | l'**état courant** : synthèse, chantiers, questions |
| [`pilotage/roadmap.md`](pilotage/roadmap.md) | le **plan** : lignes A/B, prochaine action par ligne |
| [`pilotage/utilisation.md`](pilotage/utilisation.md) | ce qui marche aujourd'hui, avec la commande exacte |
| [`pilotage/manques.md`](pilotage/manques.md) | le registre des manques mesurés |
| [`pilotage/references-non-regression.md`](pilotage/references-non-regression.md) | les repères chiffrés des passes complètes |
| [`pilotage/roadmap-native.md`](pilotage/roadmap-native.md) | le programme N : DRVM, `drave-n0`, distillation |

## Théorie — ce qui reste vrai

| document | pour quoi |
|---|---|
| [`theorie/vision.md`](theorie/vision.md) | la vision : les flots, les cinq axes, ce qu'elle n'est pas |
| [`theorie/carte.md`](theorie/carte.md) | la carte des sujets, bloc par bloc |
| [`theorie/histoire.md`](theorie/histoire.md) | Qtrinet → Drave, les trois âges |
| [`theorie/protocole-semantique.md`](theorie/protocole-semantique.md) | rejouer, converger, sens → texte, raisonnement gelé |
| [`theorie/semantique-universaux.md`](theorie/semantique-universaux.md) | la base typée : 15 champs, 502 classes |
| [`theorie/modules-cerveau-langage.md`](theorie/modules-cerveau-langage.md) | les modules M1–M9, le bus et les négatifs |
| [`theorie/jeux-symboliques.md`](theorie/jeux-symboliques.md) | surface → RSN-jeu → pensée, 71 langues, maîtres |
| [`theorie/genealogie-des-langues.md`](theorie/genealogie-des-langues.md) | la généalogie et l'avertissement époque/filiation |
| [`theorie/synthese/index.md`](theorie/synthese/index.md) | la synthèse en 8 chapitres |
| [`theorie/glossaire.md`](theorie/glossaire.md) | le vocabulaire : couche vs étage, unité de sens, RSN |
| [`theorie/architecture-native.md`](theorie/architecture-native.md) | DRVM, `drave-n0` : le format et le modèle natifs |
| [`theorie/glossaire/README.md`](theorie/glossaire/README.md) | les 289 fiches du glossaire |

## Implantation — comment c'est construit

| document | pour quoi |
|---|---|
| [`implantation/format-flux.md`](implantation/format-flux.md) | la spécification DRVF : trace, rejeu, transport |
| [`implantation/format-clusters.md`](implantation/format-clusters.md) | le modèle éclaté en clusters |
| [`implantation/convertisseur.md`](implantation/convertisseur.md) | le convertisseur et le chargement |
| [`implantation/contexte-long.md`](implantation/contexte-long.md) | ce que 1 M de contexte veut dire, et par où ça casse |
| [`implantation/llm-externe.md`](implantation/llm-externe.md) | le banc externe, le professeur et l'élève |
| [`implantation/numa-segregation.md`](implantation/numa-segregation.md) | la ségrégation NUMA mesurée |
| [`implantation/configuration-nvme-raid-amd.md`](implantation/configuration-nvme-raid-amd.md) | l'array NVMe et le pari AMD |

## Transversal et archive

| document | pour quoi |
|---|---|
| [`schemas/README.md`](schemas/README.md) | l'index des schémas et la convention SVG |
| [`archive/README.md`](archive/README.md) | les plans, notes et études de 2026-09/10, hors chargement |

## La règle de rangement

`docs/` = **méthode, pilotage, théorie, implantation** ; `reports/` = **résultats** ; `journal/` = **récit daté** ;
`data/` = **corpus**. Une page de `docs/` qui se remplit de tableaux de mesures déménage dans `reports/`.
Les **plans et notes datés** vivent dans [`archive/`](archive/README.md), **facultatifs** ; la feuille de route est
[`pilotage/roadmap.md`](pilotage/roadmap.md).

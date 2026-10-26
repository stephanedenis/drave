# La documentation de Drave — la carte

> **`docs/` dit ce qui reste vrai** : la vision, les concepts, les contrats, l'état et les règles. Les **chiffres**,
> les séries et les comptes rendus vivent dans [`reports/`](../reports/) ; le **récit daté** dans [`journal/`](../journal/).
> Une page de `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/`.

> **Chargement facultatif.** Aucun document de ce dossier n'est nécessaire pour commencer une tâche : lire
> [`AGENTS.md`](../AGENTS.md), puis le document de la tâche dans [`agent/`](agent/). Le reste se charge au besoin.

## En trois portes

| si vous voulez… | lisez |
|---|---|
| **comprendre le projet** | [la vision](vision.md) · [la mission](agent/mission.md) · [le glossaire](glossaire.md) · [la synthèse](synthese/index.md) |
| **faire** (résultat, porte, rangement, Panini, miroir, ressources) | [`agent/`](agent/) · [l'organisation](organisation-du-depot.md) · [l'utilisation](utilisation.md) |
| **savoir où l'on en est** | [l'état](en-cours.md) · [la roadmap](roadmap.md) · [les résultats](../reports/README.md) · [les portes](references-non-regression.md) · [le journal](../journal/README.md) |

## La carte des blocs

La vision est un **bus d'événements** : chaque bloc a un contrat, une trace et un coût ; il peut être neuronal ou
classique, et se remplacer sans toucher au bus. Les documents qui portent chaque bloc :

| bloc | le concept | les preuves |
|---|---|---|
| **le bus et les flux** | [la vision](vision.md) · [le format de flux](format-flux.md) · [les clusters](format-clusters.md) | [les portes](references-non-regression.md) |
| **le bloc neuronal** | [la vision](vision.md) · [le format de flux](format-flux.md) · [la modularisation](modularisation.md) | [`reports/`](../reports/README.md) |
| **le bloc classique** | [la vision](vision.md) · [la modularisation](modularisation.md) | [les jeux](jeux-symboliques.md) · [les portes](references-non-regression.md) |
| **la langue (surface → RSN)** | [les jeux symboliques](jeux-symboliques.md) · [la généalogie](genealogie-des-langues.md) | [B7/B8](../reports/rapport-langues-maitres.md) |
| **la pensée (étage 2)** | [la synthèse 05](synthese/05-la-pensee-sans-verbaliser.md) · [la synthèse 08](synthese/08-les-operations.md) | [les opérations](../reports/rapport-operateur-negation.md) |
| **le professeur externe** | [le banc externe](llm-externe.md) | [B9](../reports/rapport-deepseek.md) |
| **la mesure** | [la synthèse 06](synthese/06-comment-savoir.md) · [l'organisation](organisation-du-depot.md) | [les portes](references-non-regression.md) |

## Les documents de tâche

`AGENTS.md` est court : il porte la vision, les règles et le routage. Le détail d'une tâche est **chargé à la
demande**, un document par tâche.

| document | pour quoi |
|---|---|
| [agent/mission.md](agent/mission.md) | la vision, les deux programmes, l'ordre des priorités |
| [agent/resultats.md](agent/resultats.md) | ce qu'un résultat doit porter : chiffre, contrôle, commit, fiche |
| [agent/rangement.md](agent/rangement.md) | `docs/` vs `reports/` vs `journal/` vs `data/`, la revue |
| [agent/portes.md](agent/portes.md) | lancer les portes, lire le registre, les rouges connues |
| [agent/panini-nipada.md](agent/panini-nipada.md) | Panini/Nipada, l'avertissement époque/filiation |
| [agent/miroir.md](agent/miroir.md) | le miroir entrée/sortie et ses quatre règles |
| [agent/ressources.md](agent/ressources.md) | le matériel, les GPU, la composition mesurée |

## Les références et les normes

| document | ce qu'il dit |
|---|---|
| [glossaire.md](glossaire.md) | le vocabulaire : couche vs étage, unité de sens, RSN |
| [organisation-du-depot.md](organisation-du-depot.md) | où écrire quoi, comment nommer et horodater |
| [utilisation.md](utilisation.md) | ce qui marche aujourd'hui, ce qui manque |
| [histoire.md](histoire.md) | Qtrinet → Drave, les trois âges |
| [references-non-regression.md](references-non-regression.md) | les repères des passes complètes |
| [manques.md](manques.md) | le registre des manques mesurés |

## La règle de rangement

`docs/` = **état, vision, concepts** ; `reports/` = **résultats** ; `journal/` = **récit daté**. Une page de `docs/`
qui se remplit de tableaux de mesures déménage dans `reports/` — il reste ici un résumé et le lien vers la fiche.
Les **plans et notes datés** ne sont pas la feuille de route : ils vivent dans [`archive/`](archive/README.md),
**facultatifs**, et la feuille de route est [`roadmap.md`](roadmap.md).

## L'archive

[`archive/README.md`](archive/README.md) — les plans, notes et études de 2026-09/10, conservés pour l'histoire, mais
**hors du chargement par défaut**. On y va pour retrouver une décision ou une mesure ancienne, pas pour comprendre
l'état courant.

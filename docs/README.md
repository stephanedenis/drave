# La documentation de Drave — l'inventaire

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 184 fichiers / 251 JSON, 54 documents**), chemins archivés
> corrigés (`docs/archive/`), B10–B12 réintégrés dans les cartes. **Les règles d'`AGENTS.md`
> ne changent pas.** Source de vérité : `docs/en-cours.md` (état) et
> `docs/roadmap.md` (plan). *Spécifique : cette page est l'**inventaire** ; `carte.md`
> est l'index des sujets, et le tableau des blocs y vit désormais.*

> **`docs/` dit ce qui reste vrai** : la vision, les concepts, les contrats, l'état et les règles. Les **chiffres**,
> les séries et les comptes rendus vivent dans [`reports/`](../reports/) ; le **récit daté** dans [`journal/`](../journal/).
> Une page de `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/`.

> **Chargement facultatif.** Aucun document de ce dossier n'est nécessaire pour commencer une tâche : lire
> [`AGENTS.md`](../AGENTS.md), puis le document de la tâche dans [`agent/`](agent/). Le reste se charge au besoin.

## En trois portes

| si vous voulez… | lisez |
|---|---|
| **comprendre le projet** | [la vision](vision.md) · [la mission](agent/mission.md) · [le protocole sémantique](protocole-semantique.md) · [le glossaire](glossaire.md) · [la synthèse](synthese/index.md) |
| **faire** (résultat, porte, rangement, Panini, miroir, ressources) | [`agent/`](agent/) · [l'organisation](organisation-du-depot.md) · [l'utilisation](utilisation.md) |
| **savoir où l'on en est** | [l'état](en-cours.md) · [la roadmap](roadmap.md) · [les résultats](../reports/README.md) · [les portes](references-non-regression.md) · [le journal](../journal/README.md) |

## La carte des blocs

La vision est un **bus d'événements** : chaque bloc a un contrat, une trace et un coût ; il peut être neuronal ou
classique, et se remplacer sans toucher au bus. La **cartographie détaillée** — bus, bloc neuronal, bloc classique,
langue, pensée, mesure, sémantique typée (B10/B11), cerveau-langage (B12) — vit dans
[`carte.md`](carte.md#les-blocs) : cette page ne la duplique plus, pour éviter les deux copies qui divergent.

## Les documents de tâche

`AGENTS.md` est court : il porte la vision, les règles et le routage. Le détail d'une tâche est **chargé à la
demande**, un document par tâche.

| document | pour quoi |
|---|---|
| [agent/mission.md](agent/mission.md) | la vision, les deux programmes, l'ordre des priorités |
| [agent/resultats.md](agent/resultats.md) | ce qu'un résultat doit porter : chiffre, contrôle, commit, fiche |
| [agent/rangement.md](agent/rangement.md) | `docs/` vs `reports/` vs `journal/` vs `data/`, la revue |
| [agent/illustrations.md](agent/illustrations.md) | les illustrations : SVG obligatoire, conversion, vérification |
| [agent/portes.md](agent/portes.md) | lancer les portes, lire le registre, les rouges connues |
| [agent/panini-nipada.md](agent/panini-nipada.md) | Panini/Nipada, l'avertissement époque/filiation |
| [agent/miroir.md](agent/miroir.md) | le miroir entrée/sortie et ses quatre règles |
| [agent/ressources.md](agent/ressources.md) | le matériel, les GPU, la composition mesurée |
| [agent/contexte.md](agent/contexte.md) | le budget de contexte : ce qu'on charge, ce qu'on ne charge pas |

## Les références et les normes

| document | ce qu'il dit |
|---|---|
| [glossaire.md](glossaire.md) | le vocabulaire : couche vs étage, unité de sens, RSN |
| [organisation-du-depot.md](organisation-du-depot.md) | où écrire quoi, comment nommer et horodater |
| [utilisation.md](utilisation.md) | ce qui marche aujourd'hui, ce qui manque |
| [histoire.md](histoire.md) | Qtrinet → Drave, les trois âges |
| [references-non-regression.md](references-non-regression.md) | les repères des passes complètes |
| [manques.md](manques.md) | le registre des manques mesurés |
| [schemas/README.md](schemas/README.md) | l'index des schémas, des sources docwatch et la convention SVG |
| [glossaire/README.md](glossaire/README.md) | l'index des 289 entrées et des fiches courtes |
| [glossaire/entrees/](glossaire/entrees/) | les fiches glossaire par entrée (format carte pour docwatch) |
| [semantique-universaux.md](semantique-universaux.md) | la base typée (B11) : 15 champs, 502 classes, les écoles |
| [modules-cerveau-langage.md](modules-cerveau-langage.md) | les modules M1–M9 (B12), le bus et les négatifs |
| [contexte-long.md](contexte-long.md) | ce que 1 M de jetons de contexte veut dire, et par où ça casse |
| [configuration-nvme-raid-amd.md](configuration-nvme-raid-amd.md) | l'array NVMe et le pari AMD (daté 12/10) |
| [numa-segregation.md](numa-segregation.md) | la ségrégation NUMA mesurée |
| [convertisseur.md](convertisseur.md) | le convertisseur et le chargement, ce que la mesure dit de faire |

## La règle de rangement

`docs/` = **état, vision, concepts** ; `reports/` = **résultats** ; `journal/` = **récit daté**. Une page de `docs/`
qui se remplit de tableaux de mesures déménage dans `reports/` — il reste ici un résumé et le lien vers la fiche.
Les **plans et notes datés** ne sont pas la feuille de route : ils vivent dans [`archive/`](archive/README.md),
**facultatifs**, et la feuille de route est [`roadmap.md`](roadmap.md).

## L'archive

[`archive/README.md`](archive/README.md) — les plans, notes et études de 2026-09/10, conservés pour l'histoire, mais
**hors du chargement par défaut**. On y va pour retrouver une décision ou une mesure ancienne, pas pour comprendre
l'état courant.

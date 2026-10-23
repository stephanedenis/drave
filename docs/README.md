# La documentation de Drave Natif — état, mission, vision

> **Ce dossier n'est pas un dépôt de résultats.** Les chiffres, les séries de mesures et les comptes rendus vivent
> dans [`reports/`](../reports/). Ici : ce qui **reste vrai** quand les chiffres changent — la mission, l'état
> actuel, l'architecture, les concepts, et les modes d'emploi.

## La mission, en un paragraphe

**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut** : les activations sont
des **faits** poussés vers leurs lecteurs, le coût suit l'**activité**, et le modèle devient **décomposable**,
**répartissable** et **observable** — né du besoin de faire tourner des modèles **de types différents** sur des
machines **limitées**, de les **combiner**, de les **décomposer** sur du matériel divers, voire **distribué en
réseau**, de les **diagnostiquer** et **rejouer**. Deux **programmes** avancent en parallèle : le **moteur** (les
flux, les cinq axes) et l'**intelligence** (les deux étages : l'entrée-sortie linguistique, jugée en qualité de
traducteur, puis la pensée abstraite indépendante de la langue). La thèse : **la structure bat la taille**.

## Par où commencer

| si vous voulez… | lisez |
|---|---|
| **l'état actuel**, en quelques lignes | [en-cours.md](en-cours.md) |
| la **vision** (les flots, les cinq axes, ce qu'elle n'est pas) | [vision.md](vision.md) |
| la **roadmap** (les deux programmes, l'ordre, la file « jamais en attente ») | [roadmap.md](roadmap.md) |
| les **directives de l'agent** (courtes), et le routage par tâche | [AGENTS.md](../AGENTS.md) (racine du dépôt) |
| le **détail d'une tâche** (résultat, portes, rangement, Panini, miroir…) | [`docs/agent/`](agent/) |
| la **synthèse théorique** (7 chapitres, 7 schémas) | [synthese/index.md](synthese/index.md) |
| **utiliser** le dépôt | [utilisation.md](utilisation.md) |
| les **chiffres mesurés** | [`reports/`](../reports/) |
| le **récit** des journées | [`journal/`](../journal/) |

## Les documents de tâche de l'agent

`AGENTS.md` est volontairement **court** : il porte la mission, les règles non négociables et le routage. Le détail
est chargé **à la demande**, un document par tâche :

| document | pour quoi |
|---|---|
| [agent/mission.md](agent/mission.md) | la vision, les deux programmes, l'ordre des priorités, ce que « perfectible » veut dire |
| [agent/resultats.md](agent/resultats.md) | ce qu'un résultat doit porter, le commit, la fiche, le récit, l'état |
| [agent/rangement.md](agent/rangement.md) | `docs/` vs `reports/` vs `journal/` vs `data/`, la revue de documentation |
| [agent/portes.md](agent/portes.md) | lancer les portes, lire le registre, les rouges connues |
| [agent/panini-nipada.md](agent/panini-nipada.md) | étudier Panini/Nipada, l'avertissement époque/filiation |
| [agent/miroir.md](agent/miroir.md) | le miroir entrée/sortie et ses quatre règles |
| [agent/ressources.md](agent/ressources.md) | le matériel, les GPU, la philosophie carpe diem |

## La règle de rangement

`docs/` dit l'**état**, la **mission**, la **vision** ; `reports/` porte les **résultats** ; `journal/` porte le
**récit daté**. Une page de `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/` — il reste ici
un résumé de l'état et le lien vers la fiche. *C'est la règle que ce dépôt a le plus souvent violée ; elle est
maintenant écrite.*

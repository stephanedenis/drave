# La documentation de Drave — la carte

> **Ce dossier n'est pas un dépôt de résultats.** Les chiffres, les séries de mesures et les comptes rendus vivent
> dans [`reports/`](../reports/). Ici : ce qui **reste vrai** quand les chiffres changent — la vision, l'état,
> l'architecture, les concepts, et les modes d'emploi.

## La vision, en un paragraphe

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

## L'inventaire, par famille

### Le cadre (la vision et son état)

| document | ce qu'il dit |
|---|---|
| [vision.md](vision.md) | **la vision** : des listes, pas des matrices ; les cinq axes ; ce qu'elle n'est pas |
| [roadmap.md](roadmap.md) | **les deux programmes**, l'ordre du jour sans dates, la file « jamais en attente », les blocages nommés |
| [en-cours.md](en-cours.md) | **l'état courant** : la synthèse, les chantiers, les questions |
| [agent/](agent/) | les **documents de tâche** : mission, résultats, rangement, portes, miroir, Panini/Nipada, ressources |

### La théorie (la synthèse en sept chapitres)

| # | chapitre | programme | ce qu'il explique |
|---|---|---|---|
| 1 | [le cerveau Drave](synthese/01-le-cerveau-drave.md) | moteur | l'idée fondatrice, et pourquoi couper un modèle ne le casse pas |
| 2 | [l'anatomie interne](synthese/02-anatomie-interne.md) | moteur | régions, liens, bus, horloges : ce qui circule et où |
| 3 | [les modes et les portes](synthese/03-les-modes-et-les-portes.md) | moteur | les six façons de faire tourner le modèle, et les vérifications |
| 4 | [les douze facultés](synthese/04-les-facultes-et-la-biologie.md) | moteur | C1-C12 : ce qu'on cherche à donner à un modèle |
| 5 | [la pensée sans verbaliser](synthese/05-la-pensee-sans-verbaliser.md) | intelligence | la carte du raisonnement : l'état, le pont, l'alignement, le plan |
| 6 | [comment savoir](synthese/06-comment-savoir.md) | méthode | les portes, le registre, les cinq pièges, les sept leçons |
| 7 | [les modèles d'entrée-sortie](synthese/07-modeles-alternatifs-entree-sortie.md) | intelligence | la théorie de l'étage entrée-sortie : cinq familles, ce qui reste ouvert |

### Le moteur (les flux, les cinq axes)

**Les spécifications et l'état :**

| document | ce qu'il spécifie |
|---|---|
| [format-flux.md](format-flux.md) | le format de flux **DRVF** : la trace, le rejeu, le transport, l'analyse — un seul format |
| [format-clusters.md](format-clusters.md) | le modèle **éclaté en clusters** : un fichier par grappe, le placement des neurones |
| [etat-cerveau.md](etat-cerveau.md) | l'**état des capacités** du moteur : ce qui est fait, le chiffre qui le prouve, la prochaine action |
| [etat.md](etat.md) | l'**index des modules** : pour chacun, sa roadmap et son état |
| [references-non-regression.md](references-non-regression.md) | les **repères qui ne doivent pas bouger** (les verdicts de perplexité) |
| [manques.md](manques.md) | le registre des **manques** mesurés |
| [contexte-long.md](contexte-long.md) | ce que **1 M de contexte** veut dire, et par où ça casse |
| [convertisseur.md](convertisseur.md) | le **convertisseur** et le chargement, ce que la mesure dit de faire |
| [modularisation.md](modularisation.md) | la **modularisation** et le parallélisme, par la mesure |
| [numa-segregation.md](numa-segregation.md) | la **ségrégation NUMA** : ce que la machine répond |
| [configuration-nvme-raid-amd.md](configuration-nvme-raid-amd.md) | la **machine** : l'array NVMe, l'AMD pour le bureau |
| [campagne-benefices.md](campagne-benefices.md) | la **campagne 24 h** du 8-9/10 : où le moteur est à son meilleur, tâche par tâche |

**Les plans de chantier (datés) :**

| document | le chantier |
|---|---|
| [plan-gpu-topk.md](plan-gpu-topk.md) | le **top-k de l'attention dans le noyau GPU** (phase 1.1) |
| [plan-mode4-lot-listes.md](plan-mode4-lot-listes.md) | le **lot en listes** (protocole v5) |
| [plan-prefill-reparti.md](plan-prefill-reparti.md) | le **préremplissage par lots sur le fil** (phase 3.4) |
| [plan-mla-vision.md](plan-mla-vision.md) | **MLA et vision** (chantier 5) |
| [plan-kimi-k3.md](plan-kimi-k3.md) | **Kimi-K3** : exécuter en local ce qui ne tient pas |
| [plan-modeles-lourds.md](plan-modeles-lourds.md) | les **modèles lourds** : les télécharger, découper leurs MoE |
| [plan-deepseek41-complet.md](plan-deepseek41-complet.md) | exécuter **DeepSeek-V4.1** dans Drave, les flux d'abord |
| [plan-deepseek-v4-flash.md](plan-deepseek-v4-flash.md) | adapter les tests de contexte à **DeepSeek-V4-Flash** |
| [architecture-kimi-k3.md](architecture-kimi-k3.md) · [verification-kimi-k3.md](verification-kimi-k3.md) | l'architecture de Kimi-K3 et son protocole de vérification |
| [colab-reparti.md](colab-reparti.md) | la **répétition Colab** de la phase 3.4 |
| [plan-cerveau-complet.md](plan-cerveau-complet.md) | le **plan d'origine** des capacités d'un « cerveau » (à lire comme un plan historique) |

**Les notes et les études (datées) :**

| document | l'étude |
|---|---|
| [note-lecteurs-paralleles.md](note-lecteurs-paralleles.md) | lire dans nos tampons plutôt que dans le mapping |
| [note-cancellation-evenementielle.md](note-cancellation-evenementielle.md) | prédire une couche pour ne transporter que l'imprévu |
| [note-regle-contrastive.md](note-regle-contrastive.md) | la règle contrastive : ce qu'il faut construire, et pourquoi |
| [note-un-pont-par-professeur.md](note-un-pont-par-professeur.md) | un pont par professeur : pas de couche sémantique universelle |
| [note-chemin-court-n4.md](note-chemin-court-n4.md) | entraîner le chemin court (N4) |
| [note-cycle-c2.md](note-cycle-c2.md) | C2, le cycle à deux régions |
| [note-lateralite-c9.md](note-lateralite-c9.md) | C9, la latéralité : deux instances jumelles |
| [note-peripherie-c8.md](note-peripherie-c8.md) | la périphérie de C8 : entrées, sorties, réflexes |
| [note-cout-professeur.md](note-cout-professeur.md) | le coût du professeur : ce qu'on calcule pour rien |
| [note-corpus-panini.md](note-corpus-panini.md) | les corpus de Panini-Research |
| [note-ingestion-corpus.md](note-ingestion-corpus.md) | l'ingestion des corpus, dans l'ordre demandé |
| [biologie-pour-drave.md](biologie-pour-drave.md) · [hebbien-differentiel-et-biologie.md](hebbien-differentiel-et-biologie.md) | la biologie, et le **hebbien différentiel** |
| [comparaison-spiking.md](comparaison-spiking.md) · [impulsion-pure-apprenant.md](impulsion-pure-apprenant.md) | les réseaux impulsionnels, et le mode impulsion |
| [architecture-cerveau-et-drave.md](architecture-cerveau-et-drave.md) · [cerveau-facultes.md](cerveau-facultes.md) | l'architecture du cerveau, faculté par faculté |
| [modele-pour-drave.md](modele-pour-drave.md) | quel modèle pour Drave : évaluer un modèle *ad hoc* |
| [programme-recherche.md](programme-recherche.md) | le programme de recherche vers une intelligence locale |
| [etat-emulation-professeur.md](etat-emulation-professeur.md) | l'état de l'émulation d'un professeur |
| [sprints.md](sprints.md) | la charte des sprints de 2 h |
| [roadmap-drave.md](roadmap-drave.md) | la **niche** de Drave (analyse du 05/10, la passe K3 liée au disque) |

### L'intelligence (les deux étages)

| document | ce qu'il dit |
|---|---|
| [synthese/05](synthese/05-la-pensee-sans-verbaliser.md) | **la carte du raisonnement** : l'état, le pont, l'alignement, le plan |
| [synthese/07](synthese/07-modeles-alternatifs-entree-sortie.md) | **la théorie de l'étage entrée-sortie** : cinq familles |
| [genealogie-des-langues.md](genealogie-des-langues.md) | la **généalogie** des langues : la surface capte l'époque, la filiation, non |
| [`reports/07`](../reports/07-mesures-couche-commune.md) | les **mesures** (167), une fiche par expérience |
| [`rapport-carte-raisonnement-naturel.md`](../reports/rapport-carte-raisonnement-naturel.md) | **la carte du raisonnement naturel** — la synthèse des mesures 160-168 : quatre mesures, trois courbes, deux axes, quatre limites |
| [relations-humaines.md](relations-humaines.md) | le **carpe diem**, des deux côtés |

### Les références

| document | ce qu'il dit |
|---|---|
| [glossaire.md](glossaire.md) | le **vocabulaire** du dépôt (couche vs étage, unité de sens…) |
| [organisation-du-depot.md](organisation-du-depot.md) | **où écrire quoi** : `docs/`, `reports/`, `journal/`, `data/` |
| [utilisation.md](utilisation.md) | **utiliser** Drave : ce qui marche aujourd'hui, ce qui manque |
| [histoire.md](histoire.md) | l'**histoire** du projet et le renommage Qtrinet → Drave |

## Les documents de tâche de l'agent

`AGENTS.md` est volontairement **court** : il porte la vision, les règles non négociables et le routage. Le détail
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

`docs/` dit l'**état**, la **vision**, les **concepts** ; `reports/` porte les **résultats** ; `journal/` porte le
**récit daté**. Une page de `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/` — il reste ici
un résumé de l'état et le lien vers la fiche. *C'est la règle que ce dépôt a le plus souvent violée ; elle est
maintenant écrite.*

**Les documents datés** (les plans, les notes, les analyses) portent leur date et leur état en tête ; ils ne sont
**pas** la feuille de route — celle-ci est [`roadmap.md`](roadmap.md), et l'état courant est
[`en-cours.md`](en-cours.md).

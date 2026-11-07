# La documentation de [Drave](theorie/glossaire/entrees/drave.md) — quatre familles

> **`docs/` dit ce qui reste vrai** : la méthode, l'[état](theorie/glossaire/entrees/etat.md), la théorie, l'implantation. Les **chiffres** et les
> séries vivent dans [`reports/`](../reports/) ; le **récit daté** dans [`journal/`](../journal/). Une page de
> `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/`.

> **Chargement facultatif.** Aucun document de ce dossier n'est nécessaire pour commencer une tâche : lire
> [`AGENTS.md`](../AGENTS.md), puis le document de la tâche. Le reste se [charge](theorie/glossaire/entrees/charge-flux-chargeflux.md) au besoin.

## En trois portes

| si vous voulez… | lisez |
|---|---|
| **comprendre le projet** | [la vision](theorie/vision.md) · [la mission](methode/mission.md) · [le protocole sémantique](theorie/protocole-semantique.md) · [le glossaire](theorie/glossaire.md) · [la synthèse](theorie/synthese/index.md) |
| **faire** (résultat, [porte](theorie/glossaire/entrees/porte.md), rangement, Panini, miroir, ressources) | [`methode/`](methode/) · [l'organisation](methode/organisation-du-depot.md) · [l'utilisation](pilotage/utilisation.md) |
| **savoir où l'on en est** | [l'état](pilotage/en-cours.md) · [le plan de travail](pilotage/plan-travail.md) · [la roadmap](pilotage/roadmap.md) · [les chantiers](pilotage/chantiers.md) · [le backlog](pilotage/backlog/index.md) · [les résultats](../reports/README.md) · [les portes](pilotage/references-non-regression.md) · [le journal](../journal/README.md) |

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
| [`methode/ressources.md`](methode/ressources.md) | le matériel, les [GPU](theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md), la composition mesurée |
| [`methode/contexte.md`](methode/contexte.md) | le budget de [contexte](theorie/glossaire/entrees/contexte.md) : ce qu'on charge, ce qu'on ne charge pas |
| [`methode/continuite.md`](methode/continuite.md) | les cycles DSH, les sous-agents, la discipline de `en-cours` |
| [`methode/modularisation.md`](methode/modularisation.md) | diviser ou paralléliser : ce que la mesure dit |
| [`methode/relations-humaines.md`](methode/relations-humaines.md) | *carpe diem*, le temps et les échanges |

## Pilotage — planification, état, suivi

| document | pour quoi |
|---|---|
| [`pilotage/README.md`](pilotage/README.md) | la **carte du pilotage** : ordre de [lecture](theorie/glossaire/entrees/lecture.md), qui écrit quoi, outils |
| [`pilotage/en-cours.md`](pilotage/en-cours.md) | l'**état courant** : synthèse, chantiers, sessions actives |
| [`pilotage/semaine-autonome.md`](pilotage/semaine-autonome.md) | le chantier d'une semaine + Panini |
| [`pilotage/plan-travail.md`](pilotage/plan-travail.md) | le **plan multi-sessions** : quatre sessions + le hub, territoires, cadence, surveillance |
| [`pilotage/roadmap.md`](pilotage/roadmap.md) | l'**ordre** : chantiers [A/B](theorie/glossaire/entrees/a-b.md)/N/R/S, état et prochaine action par ligne |
| [`pilotage/chantiers.md`](pilotage/chantiers.md) | les **relations** entre chantiers, la vision à jour, la capacité |
| [`pilotage/programme-r.md`](pilotage/programme-r.md) | la **charte du programme R** : six phases, lois, dépendances |
| [`pilotage/backlog/index.md`](pilotage/backlog/index.md) | le **backlog** : une fiche par fonctionnalité (R, et lignes ouvertes A/B/N) |
| [`pilotage/utilisation.md`](pilotage/utilisation.md) | ce qui marche aujourd'hui, avec la commande exacte |
| [`pilotage/manques.md`](pilotage/manques.md) | le registre des manques mesurés |
| [`pilotage/references-non-regression.md`](pilotage/references-non-regression.md) | les repères chiffrés des passes complètes |

## Théorie — ce qui reste vrai

| document | pour quoi |
|---|---|
| [`theorie/vision.md`](theorie/vision.md) | la vision : les flots, les cinq axes, ce qu'elle n'est pas |
| [`theorie/carte.md`](theorie/carte.md) | la carte des sujets, bloc par bloc |
| [`theorie/histoire.md`](theorie/histoire.md) | [Qtrinet](theorie/glossaire/entrees/qtrinet.md) → Drave, les trois âges |
| [`theorie/protocole-semantique.md`](theorie/protocole-semantique.md) | rejouer, converger, sens → texte, raisonnement gelé |
| [`theorie/semantique-universaux.md`](theorie/semantique-universaux.md) | la base typée : 15 champs, 502 classes |
| [`theorie/modules-cerveau-langage.md`](theorie/modules-cerveau-langage.md) | les modules M1–M9, le bus et les négatifs |
| [`theorie/jeux-symboliques.md`](theorie/jeux-symboliques.md) | surface → [RSN-jeu](theorie/glossaire/entrees/rsn-jeu.md) → pensée, 71 langues, maîtres |
| [`theorie/genealogie-des-langues.md`](theorie/genealogie-des-langues.md) | la [généalogie](theorie/glossaire/entrees/genealogie.md) et l'avertissement époque/filiation |
| [`theorie/synthese/index.md`](theorie/synthese/index.md) | la synthèse en 8 chapitres |
| [`theorie/glossaire.md`](theorie/glossaire.md) | le vocabulaire : [couche](theorie/glossaire/entrees/couche.md) vs étage, [unité](theorie/glossaire/entrees/unite.md) de sens, RSN |
| [`theorie/architecture-native.md`](theorie/architecture-native.md) | [DRVM](theorie/glossaire/entrees/drvm.md), `drave-n0` : le format et le modèle natifs |
| [`theorie/modele-natif.md`](theorie/modele-natif.md) | le modèle natif, le bus, les blocs et la séparation à trois niveaux |
| [`theorie/pensee-iterative.md`](theorie/pensee-iterative.md) | la RSN plurielle, l'arbre d'états et les stratégies de pensée |
| [`theorie/lecture-rapide.md`](theorie/lecture-rapide.md) | la [lecture rapide](theorie/glossaire/entrees/lecture-rapide.md) humaine, les 14 techniques et les cinq couches qui manquent |
| [`theorie/pre-traitement-linguistique.md`](theorie/pre-traitement-linguistique.md) | la couche heuristique : niveaux, cascade, coloration, coût et protocole |
| [`theorie/glossaire/README.md`](theorie/glossaire/README.md) | les 316 fiches du glossaire |

## Implantation — comment c'est construit

| document | pour quoi |
|---|---|
| [`implantation/format-flux.md`](implantation/format-flux.md) | la spécification [DRVF](theorie/glossaire/entrees/drvf.md) : [trace](theorie/glossaire/entrees/trace.md), [rejeu](theorie/glossaire/entrees/rejeu.md), transport |
| [`implantation/format-clusters.md`](implantation/format-clusters.md) | le modèle éclaté en clusters |
| [`implantation/convertisseur.md`](implantation/convertisseur.md) | le convertisseur et le chargement |
| [`implantation/contexte-long.md`](implantation/contexte-long.md) | ce que 1 M de contexte veut dire, et par où ça casse |
| [`implantation/tokenisation.md`](implantation/tokenisation.md) | la tokenisation native : octets, et la décision mesurée R13 |
| [`implantation/encodeur-visuel.md`](implantation/encodeur-visuel.md) | l'[OCR](theorie/glossaire/entrees/ocr.md) comme bloc classique : [contrat](theorie/glossaire/entrees/contrat.md), confiance, parité, porte |
| [`implantation/bloc-linguistique.md`](implantation/bloc-linguistique.md) | le bloc linguistique : neuf niveaux, heuristique/neural, substitution, activation sémantique |
| [`implantation/diehl-cook.md`](implantation/diehl-cook.md) | un bloc Diehl & Cook : équations, contrat DRVM, RSN, portes |
| [`implantation/moteur-de-pensee.md`](implantation/moteur-de-pensee.md) | le state store, l'arbre d'états, les stratégies et les portes du moteur |
| [`implantation/llm-externe.md`](implantation/llm-externe.md) | le [banc externe](theorie/glossaire/entrees/banc-externe.md), le [professeur](theorie/glossaire/entrees/professeur.md) et l'[élève](theorie/glossaire/entrees/eleve.md) |
| [`implantation/numa-segregation.md`](implantation/numa-segregation.md) | la ségrégation [NUMA](theorie/glossaire/entrees/numa.md) mesurée |
| [`implantation/configuration-nvme-raid-amd.md`](implantation/configuration-nvme-raid-amd.md) | l'array [NVMe](theorie/glossaire/entrees/nvme-ssd-odirect-pread.md) et le pari AMD |

## Produit — ce qui s'utilise aujourd'hui

| document | pour quoi |
|---|---|
| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte avec Drave — à qui, quoi, comment, limites |
| [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels (entrée → sortie), dont un cas d'échec connu |

## Transversal et archive

| document | pour quoi |
|---|---|
| [`schemas/README.md`](schemas/README.md) | l'index des schémas et la convention SVG |
| [`archive/README.md`](archive/README.md) | les plans, notes et études de 2026-09/10, hors chargement |

## La règle de rangement

`docs/` = **méthode, pilotage, théorie, implantation** ; `reports/` = **résultats** ; `journal/` = **récit daté** ;
`data/` = **[corpus](theorie/glossaire/entrees/corpus.md)**. Une page de `docs/` qui se remplit de tableaux de mesures déménage dans `reports/`.
Les **plans et notes datés** vivent dans [`archive/`](archive/README.md), **facultatifs** ; la feuille de route est
[`pilotage/roadmap.md`](pilotage/roadmap.md).

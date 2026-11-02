# Session e181ce02 — Documentation Drave avec diagrammes et implémentation

> **Journaux :** [le jour](../../2026-10-31/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `e181ce02-cd50-488a-a6be-e84b79d40dcc` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-31 17:40 |
| Durée | 30.1 h |
| Tours | 49 |
| Messages | 815 |
| Appels d'outils | 768 |
| Fichiers touchés | 25 |
| Commandes | 617 |
| Sous-agents | 2 |
| Commits | 65 |
| Compactages de contexte | 3 |

## Objectifs déclarés

- **create** — Refondre la documentation de l'architecture Drave autour de la RSN plurielle (plusieurs candidats, pas un objet canonique unique) comme représentation interne permettant des cycles de pensée itératifs multi-niveaux : arbre d'états, opérateurs neuronaux/classiques, portefeuille de stratégies d'IA cla
… [256 caractères tronqués]
- **complete** — Refondre la documentation de l'architecture Drave autour de la RSN plurielle (plusieurs candidats, pas un objet canonique unique) comme représentation interne permettant des cycles de pensée itératifs multi-niveaux : arbre d'états, opérateurs neuronaux/classiques, portefeuille de stratégies d'IA cla
… [256 caractères tronqués]
- **create** — Reprendre et compléter les sessions suspendues : R4.4 (exposant fusionné, fax 1 bit, scans réels de bout en bout) et S (candidats générés par un analyseur, export branché sur le corpus). Produire les mesures, fiches, tests et mises à jour d'en-cours/plans, documenter les limites qui ne se réparent p
… [114 caractères tronqués]
- **complete** — Reprendre et compléter les sessions suspendues : R4.4 (exposant fusionné, fax 1 bit, scans réels de bout en bout) et S (candidats générés par un analyseur, export branché sur le corpus). Produire les mesures, fiches, tests et mises à jour d'en-cours/plans, documenter les limites qui ne se réparent p
… [114 caractères tronqués]
- **create** — Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantier
… [253 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — fais une documentation détaillée du modèle Drave natif. utilise beaucoup de diagrammes pour expliquer ce qui est original à Drave. Comment implémenter un modèle de type Modèles de Diehl & Cook (2015) en respectant notre principe de séparation à 3 niveaux (sémentique neutre au centre)

**Tour 2** — continue tes réflexions et enrichit le document. Tu dois aller plus loin

**Tour 3** — Il est important que le RSN comme les autres blocs puissent accomplir leur tâches indépendamment du mode d'opération. C'est à dire que pour chaque bloc (et on veut que ces blocs soient petits) peut utiliser la technologie et les moyens les plus appropriés pour arriver à leur fins. Bref on a une modularité extréme où les neurones et le approches technoliques plus natives au matériel se coitoient na … [132 caractères tronqués]

**Tour 4** — tu commence à peine à comprendre la portée de ce quie je te demande. le RSN (le pluriel sera plus approprié ca tu dois avoir pleusieurs candidats) est une représentation de données interne qui te permen d'itérer indéfiniment dans de4s cicles de pensées à plunieurs niveauc. Il te faudra donc un arbre d'états et toutes les streatégies de l'ia traditionelle, pour pouvoir "penser". Prends au moins 10  … [102 caractères tronqués]

**Tour 5** — en-cours.md doit contenir pour chaque session tout ton plan, ambition et stratégie et objectif final. Continue ton bon travail en maintenant ce document à jour pour que les autres sessions locales puissent être en synergie avec tes travaux.

**Tour 6** — étudie les sessions dsh actives et assure-toi que notre doc est à jour

**Tour 7** — prends en charge ici les sessions en suspend pour les compléter

**Tour 8** — on une session active sur l'analyse linguistique par heuristique (coloration). J'aimerais de ce côté-ci (cette session parallèle) que tu analyse les bénéfices d'avoir une couche linguistique de prétraitement par heuristique pour l'étiquetage des différents niveaux du mot jusqu'au document en plusieurs langues. Je vise ici à alléger le traitement linguistique des réseaux de neurones en utilisant de … [60 caractères tronqués]

**Tour 9** — détaille ce qu'est le pprogramme R : docs/pilotage/programme-r.md

**Tour 10** — donc, on n'a pas encore de bloc d'étiquetage de structure linguistique?

**Tour 11** — fait les deux. Le bloc langue doit couvrir l'étiquetage tous les niveaux linguistiques jusqu'à la pragmatique. on doit avoir une version heuristique et une neuronale. Le contrat garantissant la possibilité de substituer ou faire fonctionner en parallèle (heuristique ultra rapide permettant l'activation de la couche sémantique à une fraction du coût.

**Tour 12** — lire docs/pilotage/plan-travail.md et avancer

**Tour 13** — suis le plan, continue jusqu'à 8h demain matin

**Tour 14** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [723 caractères tronqués]

**Tour 15** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [723 caractères tronqués]

**Tour 16** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [723 caractères tronqués]

**Tour 17** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [723 caractères tronqués]

**Tour 18** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [723 caractères tronqués]

**Tour 19** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [723 caractères tronqués]

**Tour 20** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [723 caractères tronqués]

**Tour 21** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [723 caractères tronqués]

**Tour 22** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [723 caractères tronqués]

**Tour 23** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 24** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 25** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 26** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 27** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 28** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 29** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 30** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 31** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 32** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 33** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 34** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 35** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 36** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 37** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 38** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 39** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 40** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 41** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 42** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 43** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 44** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 45** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 46** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 47** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 48** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

**Tour 49** — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le DRVF `thought` (encodage, rejeu, diff) et le banc anytime (AUC, regret) de B13 ; puis le gold POS/syntagme/pragmatique et la qualification neuronale de L (cascade mesurée) ; tenir en-cours/roadmap/chantiers/plan, les portes et les commits ; ne pas écrire dans les territoires S/D/ … [724 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — fais une documentation détaillée du modèle Drave natif. utilise beaucoup de diagrammes pour expliquer ce qui est origina … [164 caractères tronqués]

*123 appels d'outils.* Actions notables :

- bash — Lister la structure du dépôt
- grep
- read
- bash — Chercher Diehl/Cook, LIF, STDP dans docs et code
- bash — Lire la vision
- bash — Lire contexte et sommaire docs
- bash — Chercher références Diehl & Cook
- bash — Lire la méthode illustrations et l'index des schémas
- bash — Inspecter le moteur drave-core
- bash — Lire la spec DRVF
- bash — Lire la synthèse chapitre 7
- bash — Lire l'archive sur les réseaux impulsionnels
- bash — Lire le bus et le chemin natif
- bash — Chercher le principe de séparation
- … et 101 autres

**Synthèse produite :**

⏵ Documentation livrée : deux pages, treize schémas, deux commits

J'ai écrit deux pages complémentaires, avec **13 schémas SVG** vérifiés :

- **[`docs/theorie/modele-natif.md`](docs/theorie/modele-natif.md)** — le modèle natif : le bus de faits, DRVM, le graphe `drave-n0`, les sept pertes, ce qui est réellement original, les portes N0–N4, et ce qui pourrait rendre le document faux.
- **[`docs/implantation/diehl-cook.md`](docs/implantation/diehl-cook.md)** — le cahier d'implémentation Diehl & Cook : équations, paramètres, manifeste DRVM, flux DRVF, tête RSN, contrôles négatifs et portes D0–D6.

\## L'idée centrale : le niveau est un contrat de port

La séparation à trois niveaux est posée explicitement :

| niveau | ce qu'il porte | ce qu'il rend |
|---|---|---|
| **N1 — surface** | texte, image, notation, langue | une **RSN** |
| **N2 — RSN** | les unités de sens, le corps canonique, l'annotation | une RSN |
| **N3 — pensée** | les opérations, les règles, les solveurs | une RSN d'action |

**N1 surface → N2 RSN → N3 pensée** : la RSN est au centre, et la surface ne traverse jamais le centre. Deux étages, trois niveaux : l'étage 1 est N1 ↔ N2, l'étage 2 est N3.

\## Où placer Diehl & Cook

C'est la réponse qui structure le second document :

1. **En N1 — encodeur** : `surface → RSN`. Il voit les pixels, mais il **rend** une RSN typée. C'est le seul placement où le résultat MNIST publié est reproductible tel quel. C'est le bootstrap.
2. **En N2 — mémoire** : `RSN → RSN`. Le même code reçoit `φ(RSN)` et jamais la surface ; il apprend des prototypes **de sens**. C'est la cible.
3. **En N3 — lecture associative** : `RSN → RSN`, légal si l'opération est vérifiable, mais la lecture de référence reste **classique et exacte** ; l'A/B tranche.
4. **Interdit** : `surface → décision` sans RSN. C'est le raccourci qui rend l'invariance invérifiable.

Le point non négociable : **le code de spikes n'est jamais la RSN**. C'est un code interne, surface-bound en N1. La RSN est un objet **canonique, typé, annoté**, avec une empreinte qui ne dépend pas de la surface. `φ` ne lit que le **corps** ; l'annotation (format, langue, confiance) est un port séparé. La neutralité se mesure par deux sondes : le **format** doit être prédictible depuis le code de spikes (N1), mais **pas** depuis `φ(corps)`.

Le document donne aussi le contrat DRVM concret : `kind: "spiking_map"`, `niveau`, `ports`, les tenseurs (`w_in`, `w_ei`, `w_ie`, `theta`, `assign`), les règles de refus du chargeur, l
… [1692 caractères tronqués]

### Tour 2 — continue tes réflexions et enrichit le document. Tu dois aller plus loin

*41 appels d'outils.* Actions notables :

- write `/tmp/gen_plus.py`
- bash — Générer les quatre nouveaux schémas formels
- bash — Corriger le branchement du canoniseur
- bash — Générer les cinq schémas d'analyse
- bash — Corriger la note WTA et centrer la pyramide
- bash — Repérer les textes longs des nouveaux schémas
- bash — Générer le schéma des six anti-patrons
- bash — Repérer les points d'insertion exacts
- write `/tmp/enrichir.py`
- bash — Insérer les sections enrichies et vérifier la structure
- bash — Lire le tableau des schémas à compléter
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md`
- … et 23 autres

**Synthèse produite :**

⏵ Enrichissement terminé : 23 schémas, deux documents approfondis, portes vertes

J'ai poussé les deux pages beaucoup plus loin, et le centre de gravité a changé : la séparation à trois niveaux n'y est plus un schéma, c'est un **système formel** ; et Diehl & Cook n'y est plus un modèle recopié, c'est un **bloc analysé, chiffré et pré-enregistré**.

\## 1. La séparation devient un système de types

- **La RSN est un quotient**, pas un vecteur : `c(s) = c(s') ⇔ s ~ s'`, le corps est l'invariant, l'annotation est le chemin, le miroir est une **rétraction** (`c(d(c(s), a(s))) = c(s)`). Le hash n'est qu'un représentant.
- **Le niveau est déclaré et vérifié**, pas deviné : une signature `surface → rsn` est N1, `rsn → rsn` peut être N2 ou N3 mais doit le déclarer ; le code interne (`code`) ne traverse **jamais** une arête.
- **Théorème de non-fuite** : dans un graphe légal, tout chemin du monde à N3 traverse une arête `rsn`. La preuve tient en trois lignes, et c'est le chargeur qui l'applique.
- **Le raffinement** définit la substituabilité : même signature, même corps, annotations compatibles, même trace. C'est la définition opérationnelle du bus.

\## 2. La neutralité devient mesurable — et piégeuse

Le nouveau schéma `natif-neutralite.svg` pose le couple :

- **neutre** : le format n'est pas prédictible depuis le corps (`P_f` doit échouer) ;
- **informatif** : la classe est prédictible depuis le corps (`P_y` doit réussir).

Un code constant est parfaitement neutre et parfaitement inutile. Un code de surface est informatif et non neutre. La cible est le quadrant haut-droit ; le **marginal sémantique** est `I − N`. Et la neutralité est **relative au corpus** : un corpus où le format prédit la classe fait réussir `P_f` sans que la RSN fuie.

J'ai ajouté les **six anti-patrons** (le code promu, la surface au raisonneur, l'annotation dans le corps, le jeton déguisé, le faux miroir, le niveau décoratif) avec, pour chacun, le test qui l'attrape.

\## 3. Le rejeu devient une pile de décisions

Six étages : graine → RNG contré → ordre des opérations → arithmétique (f64, pas de fast-math) → trace canonique → hash. Trois niveaux de rejeu : **bit-exact**, **tolérant**, **sémantique**. D&C revendique le bit-exact ; un bloc qui ne dit pas lequel il garantit ne garantit rien.

\## 4. Le résultat le plus utile : le coût caché de la STDP symétrique

C'est le point que je n'avais pas vu en écrivant la première version. La règle du code de démonstration met à jour les poids **à chaq
… [4153 caractères tronqués]

### Tour 3 — Il est important que le RSN comme les autres blocs puissent accomplir leur tâches indépendamment du mode d'opération. C' … [412 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Générer les schémas modes et granularité
- bash — Insérer le mode privé, la granularité et le graphe dynamique
- bash — Repérer les lignes du tableau des schémas
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md`
- bash — Passer les portes après l'ajout du mode privé
- bash — Committer le principe d'indépendance technologique
- job_output

**Synthèse produite :**

⏵ Principe intégré : le contrat est l'invariant, la technologie est la variable

Oui — et c'est un déplacement important, parce qu'il ne faut pas confondre **la RSN et les blocs RSN**. La RSN n'est pas un bloc : c'est le **type** qui circule. Les blocs qui la produisent ou la consomment — encodeur, mémoire, décodeur — sont, eux, technologiquement libres. Un format n'est pas une machine.

J'ai ajouté cette axe aux deux documents, avec deux schémas.

\## 1. Le théorème d'indifférence

Si deux blocs ont la même **signature typée**, le même **contrat** (même corps pour les mêmes entrées, annotations compatibles) et la même **trace**, alors ils sont **substituables**, quelle que soit leur technologie. Le consommateur ne peut les distinguer que par le **coût** et la **trace**.

C'est la version formelle de ce que tu décris : le bus ne voit pas des neurones, il voit des **types**. Un transformeur dense, un réseau impulsionnel, un solveur classique, un bloc FPGA ou un service distant peuvent occuper le même port.

Mais l'indifférence a un prix, et le document le dit : il faut **un test de contrat** (les sondes), **une trace** (le rejeu) et **un coût** (le placement). Sans les trois, l'hétérogénéité n'est pas une modularité, c'est un zoo.

\## 2. Le mode d'opération et le mode d'apprentissage sont privés

Un bloc peut être :

| réalisation | représentation | ce qu'elle apporte |
|---|---|---|
| transformeur dense | f32, attention | composition, langue |
| D&C impulsionnel | spikes, STDP | parcimonie, apprentissage local |
| règle classique | symboles, table | exactitude, auditabilité |
| FPGA | bits, shift-and-add | énergie, déterminisme |
| service distant | DRVF/TCP | placement, réutilisation |

**Ce qui change** : la latence, le coût, la précision, le niveau de rejeu.
**Ce qui ne change pas** : les ports, le corps de la RSN, l'empreinte, la trace.

Le mode d'apprentissage est privé aussi : STDP locale, gradient hors ligne, règle classique, ou aucun. Le contrat ne voit que la sortie ; mais le bloc doit **déclarer** son mode et son niveau de rejeu — `bit-exact`, `tolérant`, `sémantique` — sinon la trace n'est pas reproductible.

\## 3. La granularité : petit, mais pas trop

Tu demandes des blocs petits. Le document formalise le compromis :

`coût_total = coût_bloc + k · nombre_d_arêtes`

Un bloc trop gros n'est ni mesurable, ni plaçable, ni substituable. Un bloc trop petit paie la liaison — sérialisation, transport, synchronisation, trace. L'optimum dépend de la tâch
… [2300 caractères tronqués]

### Tour 4 — tu commence à peine à comprendre la portée de ce quie je te demande. le RSN (le pluriel sera plus approprié ca tu dois a … [382 caractères tronqués]

*42 appels d'outils.* Actions notables :

- create_goal
- write `/tmp/gen_pensee.py`
- bash — Générer les deux premiers schémas de la pensée
- bash — Corriger la hauteur des nœuds de l'arbre
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/pensee-iterative.md`
- bash — Relier la RSN plurielle aux documents existants et vérifier
- bash — Corriger le lien et aligner les compteurs
- bash — Lire les lignes de compteurs exactes
- bash — Aligner le compteur JSON et revérifier
- bash — Committer le premier tour de la refonte
- job_output
- bash — Générer le cycle et le portefeuille de stratégies
- bash — Corriger la sortie settled du cycle
- bash — Déplacer le libellé settled au-dessus du nœud
- … et 23 autres

**Synthèse produite :**

⏵ Dix tours achevés : RSN plurielle, arbre d'états, moteur de pensée documenté

J'ai intégré la correction de fond : **la RSN canonique unique était le résultat d'un cycle, pas la représentation de travail**. La représentation de travail est **plurielle** — un ensemble de candidats — et la pensée est une **recherche** dans un **arbre d'états**, avec un **portefeuille de stratégies** d'IA classique. Le document [`docs/theorie/pensee-iterative.md`](docs/theorie/pensee-iterative.md) est la refonte ; il documente les dix tours.

\## Les dix tours

| tour | question | ce que ça a produit |
|---:|---|---|
| **1** | la RSN unique était-elle la bonne représentation ? | le diagnostic : ambiguïté, incomplétude, contradiction, plan, provenance, révision |
| **2** | comment ordonner les candidats ? | l'état = ensemble de candidats, statuts, provenance, empreinte Merkle, arbre |
| **3** | comment penser en boucle ? | le cycle observer → proposer → contraindre → évaluer → sélectionner → revenir → arrêter |
| **4** | avec quelles stratégies ? | le portefeuille : A*, beam, MCTS, alpha-bêta, AC-3, SAT/SMT, STRIPS/HTN, probabiliste, local, cas-based, méta |
| **5** | quel contrat ? | `state`, `proposal`, `score`, `constraint`, `decision`, `trace` ; moteur N3, opérateurs N1/N2, store |
| **6** | quand s'arrêter ? | anytime, best-so-far, budget, `settled`, contradiction, méta, interruption |
| **7** | comment choisir la stratégie ? | bandit, statistiques MCTS, politique hors ligne ; le regret comme signal |
| **8** | comment garder et rejouer ? | store, query, compact, replay, diff, share ; rejouer les **choix**, pas seulement les tenseurs |
| **9** | comment mesurer ? | anytime AUC, taux de solution, gap, nœuds, regret, justification, rejeu, invariance |
| **10** | que change-t-on aux documents ? | `modele-natif.md`, `diehl-cook.md`, index, 9 schémas, portes |

\## Les idées qui structurent la refonte

**La RSN est un type, pas un bloc.** Un **candidat** a un corps canonique, une annotation, un statut, une provenance, un coût, un score. Un **état** est un ensemble de candidats, avec un parent, une profondeur, une frontière, une empreinte. Le quotient reste **local** : il s'applique à un candidat, pas à l'état.

**La pensée est une recherche, pas un forward pass.** L'arbre d'états est la mémoire de travail : nœuds = états, arêtes = opérateurs, frontière = nœuds ouverts, transposition = même empreinte, justification = le chemin racine → nœud. Le retour arrière est une arête de p
… [3465 caractères tronqués]

### Tour 5 — en-cours.md doit contenir pour chaque session tout ton plan, ambition et stratégie et objectif final. Continue ton bon t … [120 caractères tronqués]

*32 appels d'outils.* Actions notables :

- bash — Lire l'état courant et les variables DSH
- bash — Lire le contrat des sessions
- bash — Lire le vérificateur de l'état
- bash — Vérifier la session et le format des plans
- bash — Lire la vérification des plans et de l'état
- bash — Lire l'heure et les budgets des documents
- bash — Lister les plans de session et leurs états
- bash — Lire les plans N2 et R4.4
- bash — Lire la fin de l'état courant
- bash — Lire le bloc de session à remplacer
- bash — Lire le début du bloc N2
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md`
- bash — Mettre à jour l'état avec la session Pensée
- bash — Compter les sessions et lire la question
- … et 18 autres

**Synthèse produite :**

⏵ État à jour : trois sessions, onze champs, contrat du moteur écrit

`en-cours.md` porte maintenant **trois sessions actives**, chacune avec son **plan**, son **ambition**, sa **stratégie** et son **objectif final** — les quatre champs que tu demandais, en plus des champs de coordination (rôle, action, autres sessions, interfaces, fichiers réservés, prochaine action, bloquants, journal).

\## Les trois sessions

| session | plan | ambition | objectif final |
|---|---|---|---|
| **N2.h** — le mètre propre | dédup + split par document, chaîne propre, porte honnête, diversité FR, verrou de longueur | sortir N2 du chiffre contaminé (2,85 sur 32,8 %) | un mètre honnête : corpus dédupliqué, chaîne refaite, porte < 2,5 redéfinie, généralité et verrou tranchés |
| **R4.4** — les scans | scans simulés, prétraitement mesuré, exposants, colonnes, second moteur, porte resserrée | faire de l'OCR un bloc classique robuste, jugé par la parité | WER ≤ 5 %, parité ≥ 90 % sur les scans de test, porte resserrée |
| **Pensée** — RSN plurielle et moteur N3 | state store, moteur v0, banc anytime, intégration DRVM/DRVF | un runtime cognitif où penser est une recherche tracée sur des états pluriels | un moteur de pensée v0 exécutable : state store, arbre, A*/MCTS/AC-3, trace/rejeu, banc avec contrôles |

Chaque session renvoie à son **plan complet** dans `journal/sessions/<id>/plan.md` ; `en-cours` garde la version compacte pour tenir les budgets (2 000 mots pour l'état, 4 000 pour le T0). Le détail — phases, fichiers, contrôles, échéances — est dans le plan lié.

\## Ce qui rend la synergie vérifiable

- **`tools/verifie_en_cours.py` exige désormais les quatre champs** (`Plan`, `Ambition`, `Stratégie`, `Objectif final`) pour **chaque** session : une session sans eux ne passe plus la porte.
- **`docs/methode/continuite.md`** documente le **contrat de synergie** : les quatre champs disent ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
- **`tools/sessions.py --check`** confronte les plans et l'état : trois plans actifs, trois sessions listées, périmètres et fichiers réservés sans recouvrement.
- **`Pensée`** expose ses **interfaces** : `State`, `Proposal`, `Score`, `Decision`, `Trace` ; un opérateur est un bloc `state → state` ou `state → proposal`. Une autre session peut brancher un opérateur sans toucher au moteur.
- J'ai ajouté les champs machine-readables manquants au plan **R4.4** (`Périmètre`, `Fichiers réservés`, `Prochaine action`) pour que 
… [1419 caractères tronqués]

### Tour 6 — étudie les sessions dsh actives et assure-toi que notre doc est à jour

*23 appels d'outils.* Actions notables :

- bash — Lire l'état des plans de session
- bash — Extraire les champs de tous les plans
- bash — Repérer l'activité récente des sessions
- bash — Lire la date, les derniers commits et l'état git
- bash — Chercher les artefacts Pensée v0 et N2.i
- bash — Relire l'état courant complet
- bash — Voir les modifications non committées de l'état
- bash — Lire les commits de clôture N2.i/Pensée v0
- bash — Lire la fin de l'état courant
- bash — Inspecter le dernier commit et l'arbre de travail
- bash — Lire les compteurs réels et les dernières fiches
- bash — Voir les modifications récentes de l'état
- bash — Identifier les sessions DSH des processus actifs
- read
- … et 9 autres

**Synthèse produite :**

⏵ Audit terminé : une seule session active, l'état suit les mandats

J'ai étudié les trois TUI DSH ouvertes et confronté leurs **plans** à `en-cours`. Verdict : **un seul mandat est actif**, les deux autres sont clos ; l'état était en retard d'un jour et listait encore deux sessions fermées.

\## Ce que disent les mandats

| session | plan | état réel |
|---|---|---|
| `e181ce02` — Pensée | heartbeat 2026-11-01 10 h 55 | **actif** ; state store v0 committé (`a20de579`), 6/6 portes T0–T4 |
| `0b0a6a0d` — N2.h/N2.i | heartbeat 08 h 35 | **terminé** ; N2.i committé (`17ececfc`) |
| `fe3c05f0` — R4.4 | heartbeat 02 h 55 | **terminé** ; R4.4 close (`7452a447`, `43a7b3fe`) |

Trois processus DSH tournent encore, mais **deux mandats sont clos** : le contrat de `continuite.md` dit qu'une session terminée sort d'`en-cours`. Les résultats restent dans les fiches et dans les puces de l'état.

\## Ce qui était faux dans `en-cours`

- date **03 h 15** alors que les commits vont jusqu'à **10 h 51** ;
- **N2.h et R4.4 encore en sessions actives**, alors que leurs plans sont `terminé` ;
- Pensée avec un **heartbeat du 31/10 22 h 45** et une prochaine action « écrire `moteur-de-pensee.md` » — déjà fait ;
- puce N2 encore sur **N2.h en cours** alors que **N2.i** est committé ;
- puce Pensée encore sur « le state store v0 est la prochaine action » alors qu'il est **mesuré 6/6** ;
- questions ouvertes et ligne **N** du chantier restées sur l'ancien état.

\## Ce que j'ai corrigé

- **Date** : 2026-11-01, 10 h 55 HNE.
- **Sessions en cours** : une seule, **Pensée** — `e181ce02` — avec plan, ambition, stratégie, objectif final, interfaces, fichiers réservés, heartbeat et prochaine action.
- **Sessions archivées** : `0b0a6a0d` (N2.h/N2.i) et `fe3c05f0` (R4.4) ajoutées, avec leurs fiches.
- **Pensée** : state store v0 **6/6 portes**, BFS/greedy/A*/MCTS-lite, fiche [`pensee-v0`](../../reports/rapport-pensee-v0.md) ; prochaine action **AC-3, alpha-bêta, DRVF, banc anytime**.
- **N2** : N2.h close, N2.i (4,84 Mo) **12,93** littérature / **33,83** anglais, fiche [`n2-corpus-elargi`](../../reports/rapport-n2-corpus-elargi.md).
- **R** : R4.4 close, **typoglycémie** ×17,8 (intérieur mélangé) / ×62,7 (tout mélangé), fiche [`typoglycemie`](../../reports/rapport-typoglycemie.md).
- **Chantier N** : N2 close, N2 < 2,5 non atteinte, N4 0/4, N5 gelé.
- **Questions** : N2 (la porte < 2,5 est-elle la bonne après 3,09 en domaine et 12,93 en littérature ?) et Pensée (AC-3/alpha-bêta et le banc anyt
… [971 caractères tronqués]

### Tour 7 — prends en charge ici les sessions en suspend pour les compléter

*57 appels d'outils.* Actions notables :

- bash — Lire le plan R4.4 et ce qui reste
- bash — Lire le plan N2 et son objectif final
- bash — Inspecter S, work/r44 et les GPU
- bash — Lire la fiche R4.4 et ses limites
- bash — Lire le README du banc de structures
- bash — Lister les artefacts R4.4 disponibles
- create_goal
- bash — Repérer les fonctions R4.4 à étendre
- bash — Lire le banc de mesure des scans
- bash — Lire la construction des données S et l'export
- bash — Lire la récupération des exposants
- bash — Lire la suite de l'OCR et le banc réel
- bash — Trouver les scans réels et le journal de bord
- bash — Trouver la page et la boîte de l'exposant fusionné
- … et 39 autres

**Synthèse produite :**

⏵ Reprise terminée : R4.4 close par ses limites, S laissé à sa TUI active

J'ai audité les sessions DSH actives avant de reprendre quoi que ce soit. Résultat : **deux sessions étaient closes, une était active, et une travaillait déjà** — la situation n'était pas « trois sessions suspendues ».

\## Ce que disent les mandats

| session | plan | état réel |
|---|---|---|
| `0b0a6a0d` — N2.h/N2.i | terminé, heartbeat 08 h 35 | **close** ; N2.i committé (`17ececfc`) |
| `fe3c05f0` — R4.4 | terminé, heartbeat 02 h 55 | **close** ; reste trois limites nommées |
| `e181ce02` — Pensée | actif | **active** ; state store v0, 6/6 portes |
| S — banc de structures | **aucun plan** | **active dans une autre TUI** ; commits `0ca545eb` et `5a5915a5` pendant mon travail |

La leçon de l'audit : S n'était **pas suspendue**, elle était en cours. J'ai donc arrêté de la reprendre pour ne pas écraser son travail.

\## Ce que j'ai complété

**R4.4 — close par ses limites, pas par une correction fictive.** J'ai ajouté à [`reports/rapport-r44-scans.md`](../../reports/rapport-r44-scans.md) la section « Ce qui reste — trois limites nommées » :

- **fax 1 bit** : 120 dpi, information détruite ; médian/ouverture/CC et `psm` 4/6/11 essayés, **56,7 %** de parité ;
- **exposant fusionné** : le `10` de « développement 10 » a une boîte de **confiance 0** ; il n'y a pas de boîte séparée à recadrer, un split textuel serait une devinette ;
- **scans réels de bout en bout** : Verne 1 à **7,10 %** de WER, ordre des colonnes prouvé ; la **parité** exige des questions humaines sur le scan.

Ce qui rouvrirait : un scanner réel, une vérité humaine, ou un OCR qui retrouve le 1 bit. Sans cela, R4.4 est close — et le banc tourne tel quel sur des scans réels.

**S — je n'ai pas dupliqué ; j'ai corrigé l'état.** La TUI S a committé pendant mon travail :

- `0ca545eb` — le générateur de candidats (phrase brute → structures) ;
- `5a5915a5` — le **statut pragmatique** (`resolu`, `compatible`, `exclu`, `double_sens`) avec contexte, et l'export **une ligne par lecture conservée** (statut, contexte, groupe), **11 tests**.

Mon premier jet d'export (`exporter_corpus.py`, 14 tests) a été **supplanté** par ce commit ; il n'est pas dans l'arbre. L'état dit maintenant la vérité : **S est actif dans une autre TUI**, pas repris par moi. La seule chose qui reste à S est de **brancher l'export sur `data/`** ; c'est son mandat, pas le mien.

**N2 — close, non rouverte.** La porte < 2,5 n'est pas atteinte (3,09 en domaine
… [1557 caractères tronqués]

### Tour 8 — on une session active sur l'analyse linguistique par heuristique (coloration). J'aimerais de ce côté-ci (cette session p … [340 caractères tronqués]

*22 appels d'outils.* Actions notables :

- bash — Lire les universaux et les niveaux de la RSN
- bash — Lire la lecture rapide et ses couches
- bash — Lire l'heuristique de coloration
- write `/tmp/gen_heuristique.py`
- bash — Générer les schémas heuristiques
- bash — Lire l'API du kit SVG
- bash — Voir l'erreur du générateur SVG
- bash — Générer les quatre schémas
- bash — Rendre les schémas en PNG pour inspection
- bash — Ajouter le schéma multilingue et corriger la cascade
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/pre-traitement-linguistique.md`
- bash — Repérer les index à mettre à jour
- bash — Lire l'index des schémas et l'usage des formules
- bash — Indexer la note et les cinq schémas
- … et 8 autres

**Synthèse produite :**

⏵ Analyse livrée : la couche heuristique retire la surface, le réseau garde l'ambiguïté

L'analyse est dans [`docs/theorie/pre-traitement-linguistique.md`](../../docs/theorie/pre-traitement-linguistique.md), avec **5 schémas** (`heuristique-niveaux`, `cascade`, `coloration`, `cout`, `multilingue`) et un commit : **`e331ef42`**. Voici la substance.

\## La thèse

Le réseau ne paie pas seulement le sens : il paie la **surface** — normalisation Unicode, script, langue, frontières de mots et de phrases, classes fermées, régions de document. Ces opérations sont **locales, déterministes et bon marché** : un CPU les fait en O(octets), à des ordres de grandeur d'un passage dans un transformer.

Mais l'heuristique ne doit pas **décider l'ambigu**. Elle doit :

1. **étiqueter le sûr** avec une source et une confiance ;
2. **énumérer le plausible** quand plusieurs analyses sont possibles ;
3. laisser le **résidu** au réseau (ou à l'humain).

C'est la différence entre un étiqueteur et un **générateur de candidats** — et c'est exactement le contrat de la coloration.

\## Les niveaux : ce qui s'enlève au réseau

| niveau | ce que le CPU fait bien | ce qui reste au réseau |
|---|---|---|
| **octet / Unicode** | script, NFC/NFKC, ponctuation, chiffres, dates, URLs | rien |
| **morphème** | affixes réguliers, diacritiques, lemmes productifs | irréguliers, allomorphes, agglutinants |
| **mot** | frontières sur scripts à espaces, nombres, emoji | CJK, thaï, khmer (segmentation) |
| **syntagme** | **candidats** GN/GV/GP/REL/SUB, rôles par préposition, attachements | choix de l'attachement, rôle final |
| **phrase** | frontières, type, négation | bruit OCR, ponctuation absente, portée |
| **paragraphe** | titres, listes, tableaux, régions, code | scans, layouts inédits |
| **document** | TOC, structure, provenance, renvois | compréhension, résumé |
| **multilingue** | langue sur texte long, script, famille | langues proches, codes mêlés, texte court |

Le point clé : **la couche heuristique ne remplace pas le réseau, elle lui retire la surface**. Le réseau garde le choix, le sens, l'inférence.

\## Le cas de la coloration

Le générateur S (`tools/structures/generateur.py`, que j'ai lu sans y toucher) est le bon modèle :

- il reconnaît les **classes fermées** (déterminants, prépositions, relatifs, pronoms, auxiliaires) ;
- il segmente en **GN, GV, GP, REL, SUB** ;
- il **varie l'attachement** du segment ambigu : sur « Le chat de la voisine qui dort sur le toit se réveille. », il 
… [5328 caractères tronqués]

### Tour 9 — détaille ce qu'est le pprogramme R : docs/pilotage/programme-r.md

*28 appels d'outils.* Actions notables :

- bash — Vérifier si la charte existe et lire la ligne R de la roadmap
- bash — Lire le programme R dans la lecture rapide
- bash — Lire le backlog R et les fiches
- bash — Lire la charte R existante
- bash — Lister les fiches R et lire R0.6/R13
- bash — Lire l'état R et les questions ouvertes
- bash — Trouver les portes du programme R
- bash — Lire les chiffres du banc et de la publication R0.6
- bash — Lire la porte de lecture et le pipeline
- bash — Lire les chiffres R4.4 et R4.1
- bash — Vérifier les documents et les fiches R4
- write `/tmp/gen_programme_r.py`
- bash — Générer les deux schémas du programme R
- bash — Corriger la branche de refus du pipeline
- … et 13 autres

**Synthèse produite :**

⏵ Charte R réécrite : six phases, trois lois, le verrou de l'encodeur

La page `docs/pilotage/programme-r.md` est passée d'une **synthèse de 600 mots datée du 29/10** à une **charte de 3 437 mots, 12 sections et 2 schémas**, à l'état du **2026-11-01**. Commit : **`73b00495`**, puis **`0a17760d`** pour le compteur JSON. Voici ce qu'elle dit.

\## 1. Ce qu'est R — et ce qu'il n'est pas

Drave a quatre lignes : **A** (le moteur), **B** (le sens), **N** (le natif) et **R** (le lecteur). Les trois premières construisent des **capacités** ; R construit la **preuve d'usage** :

> un document, une question, un budget → une réponse **avec sa source**, ou un **refus motivé**.

R n'est donc **ni un modèle, ni un benchmark** : c'est un **programme** avec des phases (R0–R5), des blocs (R01–R52), des mesures, des fiches, des portes et des états. Il **assemble** des blocs classiques (parseurs, BM25, AST, sympy, OCR) et des blocs neuronaux (le 0,5 B, plus tard le natif). Sans R, N2 est une course à la perplexité et B10 un `z` qui ne dit pas ce qu'il contient.

La distinction structurante :

- **R0** est le lecteur **système**, sans entraînement, avec l'existant et un modèle externe ;
- **R1–R5** sont le lecteur **natif** : fenêtre, mémoire, restitution, structure, croisé.

\## 2. La carte des six phases

| phase | question | état |
|---|---|---|
| **R0 — lecteur v0** | lire un document, choisir, citer, refuser | ✅ **close** : R0.1–R0.3, R0.6 ; R0.4/R0.5 négatifs |
| **R1 — fenêtre native** | 1 000 octets sans refaire 130–256 ? | 🟡 **R13 close (octets)** ; R1.1/R1.2 attendent le contexte |
| **R2 — mémoire** | gist, entités, relire | ⛔ attend R1 et N5 |
| **R3 — restitution** | répondre, résumer, extraire, citer | ⛔ attend N4 |
| **R4 — blocs structurels** | tables, code, maths, scans | ✅ R4.1–R4.3 ; **R4.4 close avec limites** |
| **R5 — lecture croisée** | comparer, recouper, traduire | ⛔ attend R3 et B10.3 |

La charte contient le schéma des phases et de leurs dépendances (`programme-r-phases.svg`).

\## 3. Le pipeline R0.6

`programme-r-pipeline.svg` montre l'assemblage :

**document → R0.1 régions → R0.2 contrôleur → passages → un des trois lecteurs → réponse citée ou refus.**

- **R0.1** : 16 PDF + 8 MD + 3 HTML + 3 DOCX/EPUB, **51 pages**, partition **1,000**, fidélité **1,000**.
- **R0.2** : cinq modes (`survol`, `balayage`, `lecture`, `relecture`, `arrêt`), budget en **octets**, récupération **1,00** à **30 %** sur les 5 types.
- **R0.3** : 30 documents, **249 questi
… [5445 caractères tronqués]

### Tour 10 — donc, on n'a pas encore de bloc d'étiquetage de structure linguistique?

*6 appels d'outils.* Actions notables :

- glob
- bash — Chercher un bloc ou un étiqueteur existant
- bash — Vérifier les niveaux couverts par R0.1 et la coloration
- bash — Lire le contrat de bloc/flux existant
- bash — Lire le contrat d'un bloc existant
- bash — Confirmer l'absence des fichiers du bloc linguistique

**Synthèse produite :**

⏵ Vérifié : oui pour les régions et les candidats, non pour un bloc linguistique

**Non — pas encore.** Il y a trois briques qui en approchent, mais aucune n'est le **bloc d'étiquetage de structure linguistique** au sens Drave : un bloc typé, multi-niveaux, multilingue, avec un contrat, une trace, un coût et une porte.

\## Ce qui existe

| brique | ce qu'elle fait | ce qu'elle n'est pas |
|---|---|---|
| **R0.1 — `graphe_document.py`** | découpe un document en **régions** (titre, section, paragraphe, tableau, code, maths, figure), avec offsets et provenance | ce n'est pas de la linguistique : aucun mot, aucune phrase, aucun rôle ; le vocabulaire des régions est fermé |
| **R4.1–R4.4** | lisent la **structure** : tableaux (996 cellules), code (AST), maths (sympy), scans (OCR) | ce n'est pas de la langue : ce sont des blocs structurels, pas des étiquettes morphologiques ou syntaxiques |
| **S — `tools/structures/generateur.py`** | segmente en **GN/GV/GP/REL/SUB**, devine des rôles par la préposition, produit des **candidats d'attachement** ; 7 phrases, 11 tests | ce n'est pas un bloc : c'est un **générateur de candidats** pour validation humaine, français, sans POS par mot, sans morphologie, sans phrase/document, sans contrat de flux, sans porte |
| **La RSN** | la **cible** : une structure multi-niveaux (graphémique, morphologique, syntaxique, sémantique, discursif) | ce n'est pas l'étiqueteur : aucun code ne remplit aujourd'hui les niveaux de surface ; B travaille le sens (15 champs, 502 classes), N lit des octets |
| **`pre-traitement-linguistique.md`** | l'**analyse** de ce que le CPU peut étiqueter, la cascade et le protocole | ce n'est pas une implémentation : pas de `bloc-langue`, pas de `bloc-coloration`, pas de `porte-coloration` |

Le constat est net : `docs/implantation/` n'a que `bloc-tableaux.md`, `bloc-code.md` et `bloc-maths.md` ; `tools/` n'a que `bloc_tableaux.py`, `bloc_code.py`, `bloc_maths.py`. Il n'y a **ni `bloc_coloration.py`, ni `bloc_langue.py`, ni `porte-coloration.sh`**.

\## Pourquoi la coloration n'est pas encore le bloc

Le générateur S est le **bon germe**, mais il lui manque exactement ce qui fait un bloc :

- **un contrat de flux** : entrée (texte/octets + langue), sortie (liste valuée d'annotations avec `span`, `niveau`, `type`, `rôle`, `source`, `confiance`, `candidats`), coût, trace, rejeu, refus ;
- **les niveaux** : aujourd'hui il fait le **syntagme** (GN/GV/GP/REL/SUB) ; il ne fait ni `lang` (script/langue), ni `tok` (fr
… [2675 caractères tronqués]

### Tour 11 — fait les deux. Le bloc langue doit couvrir l'étiquetage tous les niveaux linguistiques jusqu'à la pragmatique. on doit a … [231 caractères tronqués]

*42 appels d'outils.* Actions notables :

- bash — Trouver le corpus multilingue UDHR
- bash — Trouver le modèle local et l'adaptateur neuronal
- bash — Vérifier les schémas et les API à réutiliser
- bash — Compter les langues UDHR et vérifier llama-cli
- bash — Compter les langues et scripts UDHR
- bash — Vérifier les tests et le split UDHR
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py`
- bash — Corriger et tester le bloc sur une phrase
- bash — Brancher le générateur S et corriger les prépositions
- bash — Voir la ligne DET restante
- bash — Corriger la classe de « de »
- bash — Tester les modes et l'autotest UDHR
- bash — Lire les résultats de langue et de substitution
- bash — Ajouter le seuil de langue et la fusion sans chevauchement
- … et 26 autres

**Synthèse produite :**

⏵ Bloc livré : neuf niveaux, 398 langues, heuristique et neuronal substituables

Les deux sont faits : le **contrat** et le **bloc exécutable**. Commit **`651bfc90`**.

\## 1. Le contrat — `docs/implantation/bloc-linguistique.md`

Un seul contrat, **neuf niveaux** :

| niveau | heuristique CPU | neuronal | exemple |
|---|---:|---:|---|
| graphème | 0,99 | — | script, classe, normalisation |
| morphème | 0,32 | 0,80 | affixes, racine (candidats) |
| mot | 0,98 | 0,80 | frontières, nombres, URLs, emoji |
| pos | 0,92 fermé / 0,30 ouvert | 0,82 | DET/PREP/PRON/CONJ/AUX, classes ouvertes |
| syntagme | 0,40 | 0,78 | GN/GV/GP/REL/SUB, rôles, attachements |
| phrase | 0,85 | 0,90 | type, négation, modalité |
| discours | 0,55 | 0,80 | paragraphe, connecteur, relation |
| pragmatique | 0,45 / 0,25 | 0,80 | acte, double sens, contexte |
| document | 0,70 | 0,80 | région, titre, provenance |

Chaque étiquette porte `niveau`, `span`, `type`, `valeur`, `source`, `confiance`, `candidats`,
`langue`, `script`. Une `Annotation` porte les étiquettes, les **unités sémantiques**, la
fraction, la trace, le coût et le refus. **La RSN n'est pas touchée** : l'annotation de langue,
script, source et confiance vit à côté du corps ; le corps reste neutre.

Deux schémas : `bloc-linguistique-niveaux.svg` et `bloc-linguistique-substitution.svg`.

\## 2. Le bloc — `tools/bloc_linguistique.py`

- **`Heuristique`** : CPU, déterministe, sans GPU. Profils de trigrammes par langue, script
  Unicode, mots, classes fermées fr/en, affixes, phrases, connecteurs, actes de parole, régions.
  Le **générateur de la coloration** (`tools/structures/generateur.py`) est importé **en lecture
  seule** pour les syntagmes : sur « Le chat de la voisine qui dort sur le toit se réveille. », il
  rend GN/GP/REL/GV et les deux candidats d'attachement.
- **`MockNeuronal`** : le **double de contrat** — déterministe, sans GPU, il rend les niveaux
  profonds avec `source = neuronal`. Il prouve la substitution et le parallèle, pas la qualité.
- **`NeuronalLLM`** : l'**adaptateur réel** — prompt JSON, `llama-cli`, parsing, refus explicite.
  Le vrai `Qwen2.5-0.5B` local **n'a pas fini** dans le délai (110 s, puis 35 s en CPU pur) : sa
  qualité n'est **pas revendiquée**. Il est testé avec un **faux `llama-cli`** qui rend le JSON :
  le chemin réel est vérifié.
- **`Parallele`** : fusion par `(niveau, span, type, source)` ; à niveau égal, la plus confiante
  gagne, **sauf le syntagme**, où la segmentation heuristique 
… [3426 caractères tronqués]

### Tour 12 — lire docs/pilotage/plan-travail.md et avancer

*26 appels d'outils.* Actions notables :

- read
- bash — Lire les sessions actives et les territoires
- bash — Trouver B13 et l'état du moteur de pensée
- bash — Lire le moteur de pensée et ses types
- bash — Lire les portes et stratégies du moteur
- bash — Lire les types et la fin du moteur
- bash — Écrire AC-3 et le CSP de test
- bash — Tester AC-3 sur la carte et la contradiction
- bash — Tester la propagation AC-3 et la contradiction
- bash — Écrire alpha-bêta et tester les coups
- bash — Déboguer l'état du morpion
- bash — Corriger le tour et tester alpha-bêta
- bash — Corriger l'évaluation et tester alpha-bêta
- bash — Ajouter les portes AC-3 et alpha-bêta, les exécuter
- … et 12 autres

**Synthèse produite :**

⏵ Plan lu, B13 avancé : AC-3 et alpha-bêta tiennent 8/8 portes

J'ai lu `docs/pilotage/plan-travail.md` : la session **L** (langue et pensée, c'est la nôtre) a pour mandat le bloc langue, la cascade, la pragmatique et **B13** ; sa prochaine action était « le contrat, puis la mesure 71 langues ; **AC-3/alpha-bêta** ». Le contrat et les 398 langues étaient faits ; j'ai avancé **B13 : AC-3 et alpha-bêta**. Commit **`3c749d27`**.

\## 1. AC-3 : la contrainte propage

`tools/pensee/csp.py` : le CSP, l'opérateur `retirer`, la stratégie `AC3` branchée sur la **même** boucle `Moteur`/`Store`/`Trace` que BFS/A*.

| cas | résultat |
|---|---|
| **chaîne** `A∈{r}`, `B∈{r,g}`, `C∈{r,g}`, `A≠B`, `B≠C` | B perd `r`, C perd `g` → **A=r, B=g, C=r** ; 2 valeurs retirées ; arc-consistance vraie ; solution ; `settled` |
| **carte d'Australie** (7 variables, 3 couleurs, 9 contraintes) | **aucune réduction** : la carte est déjà arc-consistante ; le backtracking trouve `WA=g, NT=b, SA=r, Q=g, NSW=b, V=g, T=b` |
| **contradiction** `A∈{r}`, `B∈{r}`, `A≠B` | domaine de A **vide** ; `resoudre` rend `None` |

La carte est le **contrôle** : AC-3 ne prouve pas une solution, il **réduit** ; quand il n'y a rien à réduire, il ne dit rien. La contradiction est **vue**, pas devinée.

\## 2. Alpha-bêta : gagner, bloquer, couper

`tools/pensee/jeux.py` : le morpion, le décideur `AlphaBeta`, le minimax exact comme contrôle.

| cas | résultat |
|---|---|
| **gagner en un coup** `X X . / O O . / . . .` | joue **case 2**, X gagne |
| **bloquer** `X . . / O O . / X . .` | joue **case 5** |
| **contrôle négatif** profondeur 1, évaluation nulle | joue **case 1** : il ne voit pas la menace |
| **coupe** plateau vide, profondeur 5 | **1 495 nœuds / 296 coupes** contre **18 730 nœuds** au minimax — même coup, **12,5× moins de nœuds** |

Le contrat est respecté au niveau des types : mêmes `Etat`, `Probleme`, `Decision`, `Store`, `Trace`, mêmes opérateurs. **Mais alpha-bêta n'est pas une stratégie de la boucle anytime** : la valeur remonte l'arbre, alors que la boucle la propage vers l'avant. C'est un **décideur** deux joueurs ; le rapport le dit au lieu de le cacher.

\## 3. Les portes

`python3 -m tools.pensee.autotest` → **8/8** :

- T0 store canonique, T1 rejeu, T1 graine, T2 stratégies, T3 anytime, T4 justification ;
- **T5 AC-3** : chaîne, carte, contradiction ;
- **T6 alpha-bêta** : gain, blocage, profondeur 1 qui rate, coupe.

Les portes T5/T6 du contrat — « un solveur se branche », « le coût est 
… [1983 caractères tronqués]

### Tour 13 — suis le plan, continue jusqu'à 8h demain matin

*12 appels d'outils.* Actions notables :

- create_goal
- bash — Lire le contrat DRVF thought et les types de trace
- bash — Écrire et tester le codec DRVF thought
- bash — Ajouter la porte DRVF et l'exécuter
- bash — Écrire la fiche DRVF et mettre l'état à jour
- bash — Vérifier les compteurs et les portes après le DRVF
- bash — Aligner les compteurs de la fiche DRVF
- bash — Committer le profil DRVF thought
- job_output
- bash — Diagnostiquer la course de commits
- bash — Voir ce que le commit concurrent a emporté
- bash — Voir la modification d'état restante et la cohérence

**Synthèse produite :**

⏵ DRVF `thought` livré (9/9) ; le goal continue vers le banc anytime

Le tour DRVF est fait, et le goal créé pour tenir jusqu'à **8 h demain** continue.

\## Ce qui est livré

- **`tools/pensee/trace.py`** : enveloppe `DRVF` (magic, version `u16`, profil `thought u16`, longueur `u32`) + charge JSON canonique `{probleme, racine, evenements}`. La racine porte l'état complet ; chaque événement porte `parent`, `enfant`, `operateur`, `params`, `score`, `cout`, `strategie`, `pas`.
- **Rejeu** : les 93 enfants sont **recalculés** par les opérateurs, empreintes et scores vérifiés ; `diff(trace, rejeu) = None`.
- **Corruption** : un score modifié dans le fichier **lève** ; `diff_fichiers` localise l'événement 0.
- **Mesure** : **23 597 octets**, **93 événements**, rejeu identique, diff 0.
- **Portes** : `python3 -m tools.pensee.autotest` → **9/9** (T0–T6 + T1 DRVF).
- **Fiche** : [`rapport-pensee-drvf.md`](../../reports/rapport-pensee-drvf.md) ; JSON [`pensee-drvf.json`](../../reports/pensee-drvf.json) ; contrat `moteur-de-pensee.md` §6.

\## La course de commit

Mon commit B13 a perdu la course : HEAD a été déplacé par le commit **`d51b4df0`** (D/R/A, « texte intégral 9 langues »), qui a **emporté les fichiers déjà stagés** — `trace.py`, `autotest.py`, la fiche, le JSON, les docs. Le contenu est donc **dans HEAD**, mais le message du commit est celui de D/R/A, pas « B13 — DRVF ». Je le note : la prochaine fenêtre d'intégration peut ajouter un commit B13 pour le banc, avec le bon chiffre.

\## L'état

- `en-cours`, `roadmap`, `chantiers`, `plan-travail`, plan `e181ce02` : B13 passe à **DRVF fait (9/9), banc anytime** ; L garde **gold/neuronal**.
- `revue_documentation` : **390 fiches / 477 JSON / 118 docs / 81 portes** — ✅.
- `taille`, `porte-tableaux`, `verifier_schemas`, `verifie_journal`, `verifie_en_cours`, `autotest 9/9` — ✅.
- Le working tree a une ligne D/R/A (9 langues en cours) que je n'ai **pas** committée : elle appartient à D/R/A.
- `sessions.py --check` signale le plan **`fe3c05f0` (R4.4)** actif, non listé et périmé de 45 min ; je ne l'ai pas touché — le hub doit l'intégrer ou le clore.

\## La suite, dans l'ordre du plan

1. **B13 — banc anytime** : budgets croissants, best-so-far, **AUC**, **regret**, par stratégie (BFS, greedy, A*, MCTS-lite) sur les cruches et un taquin 3×3 ; fiche + JSON + porte.
2. **B13 — DRVF pour AC-3/alpha-bêta** si le banc le demande.
3. **L — gold** POS/syntagme/pragmatique (100–200 phrases) ; puis **modèle neuronal qualifié**
… [268 caractères tronqués]

### Tour 14 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1003 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Lire le score et l'heuristique des cruches
- bash — Écrire le taquin et le banc anytime, l'exécuter
- bash — Ajuster les budgets et relancer le banc
- bash — Ajouter la porte T7, générer le JSON du banc
- bash — Écrire la fiche du banc et mettre l'état à jour
- bash — Vérifier le banc et les compteurs
- bash — Committer le banc anytime et la fiche
- job_output
- bash — Confirmer l'état final du round

**Synthèse produite :**

⏵ B13 v0 complet : banc 10/10, A* 32 nœuds ; le round suivant attaque le gold L

Le round 1 du goal est livré : le **banc anytime** ferme la boucle B13. Commit **`deb0f96f`**.

\## Le banc

| problème | stratégie | AUC | regret | but |
|---|---|---:|---:|---:|
| cruches | **A*/greedy** | **0,528** | **0** | **32 nœuds** |
| cruches | BFS | 0,328 | 0 | 128 |
| cruches | aléatoire | 0,246 | 0,50 | — |
| taquin 3×3 (8 coups) | **A*/greedy** | **0,624** | **0** | **32 nœuds** |
| taquin | BFS | 0,281 | 0 | 1024 |
| taquin | aléatoire | 0,116 | 0,833 | — |

L'A* est **2,1×** l'aléatoire sur les cruches, **5,4×** sur le taquin ; le MCTS-lite nu reste sous l'aléatoire (contrôle). La fiche [`rapport-pensee-banc.md`](../../reports/rapport-pensee-banc.md) et le JSON [`pensee-banc.json`](../../reports/pensee-banc.json) portent les courbes.

**La limite est écrite** : A* = greedy sur ces deux problèmes, parce que le score `1/(1+distance)` contient déjà l'information que l'heuristique ajoute. Ce n'est pas une victoire de l'A* : c'est une limite du score ; un score 0/1 et un opérateur hétérogène les sépareraient.

\## B13 v0 — complet

- **AC-3** et **alpha-bêta** : 8/8, 1 495 nœuds/296 coupes contre 18 730 au minimax.
- **DRVF `thought`** : 9/9, 23 597 octets, 93 événements, rejeu identique, corruption refusée.
- **Banc anytime** : 10/10, AUC/regret/budget du but.
- Le contrat `moteur-de-pensee.md` a T7 et les fichiers `taquin.py`/`banc.py`.

\## L'état

- `revue` : **391 fiches / 478 JSON / 118 docs / 81 portes** — ✅.
- `en-cours` : **1 612 mots**, **2 sessions** (L et R4.4), 10 puces, 5 questions ; T0 dans le budget.
- `sessions.py --check` : le plan **R4.4 `fe3c05f0`** est listé mais son heartbeat est périmé de 53 min ; la session R4.4 doit le rafraîchir — je ne l'ai pas touché.
- `autotest` : **10/10** ; toutes les portes légères passent.

\## Le round suivant

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain**. La prochaine action du plan L est le **gold POS/syntagme/pragmatique** (100–200 phrases), puis la **qualification neuronale** et la **cascade mesurée** :

- si le modèle local reste indisponible (`llama-cli` expiré), le gold mesurera l'**heuristique** et le **mock de contrat**, et la limite « neuronal non qualifié » restera écrite ;
- si le gold bloque, la file prend les **opérateurs hétérogènes/DRVM** de B13, sans attendre.

Le prochain round démarre sur le gold L.

### Tour 15 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1003 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Repérer les lexiques et la POS à enrichir
- bash — Lire les lexiques et la fonction POS
- bash — Enrichir les lexiques POS et la pragmatique
- bash — Écrire le gold v0 de 20 phrases
- bash — Écrire l'évaluateur du gold et le lancer
- bash — Générer le JSON du gold avec le test neuronal réel
- bash — Corriger la fusion des types complémentaires et remesurer
- bash — Ajouter le gold à la porte, la fiche et l'état
- bash — Vérifier le budget T0 après le gold
- bash — Rentrer dans le budget T0
- bash — Passer toutes les portes après le gold
- bash — Committer le gold v0 et l'évaluation
- job_output
- bash — Lire le hash et confirmer l'état du round

**Synthèse produite :**

⏵ Gold v0 mesuré : POS 0,924, syntagmes 0,356, pragmatique 1,0/1,0/0,95/0,9

Le round 2 du goal est livré : le **gold v0** du bloc linguistique, mesuré. Commit **`550cd76d`**.

\## Le gold

**20 phrases** (14 françaises, 6 anglaises), **105 tokens**, écrites à la main après le bloc — pas tirées du banc S. Chaque phrase porte ses POS, ses segments GN/GV/GP/REL/SUB et son pragmatique (acte, négation, modalité, double sens). Les spans sont calculés par sous-chaîne et vérifiés.

\## Les résultats

| lecture | POS | fermé | ouvert | syntagmes F1 | acte | nég. | mod. | double | fraction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **heuristique** | **0,924** | **0,912** | **0,938** | **0,356** | **1,0** | **1,0** | **0,95** | **0,9** | 0,469 |
| mock seul | 0,486 | 0,105 | 0,938 | 0,244 | 1,0 | 0,9 | 0,9 | 0,9 | 0,525 |
| **parallèle** | **0,924** | **0,912** | **0,938** | **0,356** | **1,0** | **1,0** | **0,95** | **0,9** | 0,525 |
| **cascade** | **0,924** | **0,912** | **0,938** | **0,356** | **1,0** | **1,0** | **0,95** | **0,9** | 0,525 |

- Les **classes fermées** sont à 0,912 ; les ouvertes à 0,938 ; les deux erreurs POS sont `que`/`that` lus PRON au lieu de CONJ.
- Le **syntagme** est le point faible : F1 **0,356** (P 0,471 / R 0,286) — c'est surtout un **désaccord de segmentation** entre le générateur S et le gold.
- La **fusion a été corrigée** : les types complémentaires d'un même niveau (`phrase.type` / `négation` / `modalité`, `pragmatique.acte` / `double_sens`) ne se suppriment plus entre eux. Avant, le mock effaçait la négation ; maintenant le parallèle et la cascade la **préservent** (1,0).
- La **cascade** appelle le neuronal 20 fois sur 20 (les niveaux profonds restent sous 0,6) et couvre **52,5 %** en unités sémantiques.

\## Le vrai neuronal : refusé, pas simulé

`--reel` essaie `NeuronalLLM` avec `Qwen2.5-0.5B-Q4_0` et 10 s : **`RefusNeuronal`** — le `llama-cli` local n'a pas rendu de JSON. Le mock est un **double de contrat** ; la cascade est mesurée avec lui, pas avec un modèle qualifié. La limite est écrite dans la fiche.

\## L'état

- Fiche : [`rapport-pensee-gold-linguistique.md`](../../reports/rapport-pensee-gold-linguistique.md) ; JSON [`pensee-gold-linguistique.json`](../../reports/pensee-gold-linguistique.json) ; le gold [`gold.py`](../../tools/tests/linguistique/gold.py) / [`gold.json`](../../tools/tests/linguistique/gold.json).
- Porte `porte-bloc-linguistique` : **verte** (tests + autotest 398 langues + gold) ; `porte-pens
… [1086 caractères tronqués]

### Tour 16 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1003 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — Inspecter l'état courant et les compteurs du round 3
- bash — Générer 160 phrases synthétiques annotées
- bash — Étendre l'évaluateur au gold 180 et au syntagme par tête
- bash — Ajuster les seuils par source et relancer le gold 180
- bash — Lire les métriques détaillées du gold 180
- bash — Mettre à jour la fiche, le contrat et l'état pour le gold 180
- bash — Passer toutes les portes après le gold 180
- bash — Lire le tableau des compteurs corrompu
- bash — Réparer le tableau des compteurs partagé
- bash — Aligner le compteur JSON et vérifier les portes
- bash — Committer le gold 180 et la mesure par tête
- job_output

**Synthèse produite :**

⏵ Gold 180 livré : POS 0,751, tête 0,560, cascade 67,1 % ; neuronal réel toujours refusé

Le round 3 du goal est livré : le **gold 180** est mesuré, avec la **tête** comme métrique de syntagme. Commit **`53dfd584`**.

\## Le gold étendu

**180 phrases** = **20 réelles** écrites à la main + **160 synthétiques** d'une **grammaire indépendante** (GN, GV, GP, REL, SUB, question, exclamation, impératif, négation, modalité, double sens), **804 tokens**. Le lexique synthétique est **disjoint** des listes de l'heuristique (`renard`, `montagne`, `saute`, `calme`…) : il mesure la généralisation des classes ouvertes.

| lecture | source | POS | fermé | ouvert | exact | **tête** | acte | nég. | mod. | double | fraction |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **heuristique** | **180** | **0,751** | **0,939** | **0,621** | **0,194** | **0,560** | **1,0** | **1,0** | **0,994** | **0,889** | **0,638** |
| heuristique | 20 réels | 0,924 | 0,912 | 0,938 | 0,356 | 0,489 | 1,0 | 1,0 | 0,950 | 0,900 | 0,469 |
| heuristique | 160 synth. | 0,725 | 0,945 | 0,586 | 0,168 | **0,570** | 1,0 | 1,0 | 1,000 | 0,888 | 0,659 |
| mock seul | 180 | 0,427 | 0,146 | 0,621 | 0,115 | 0,534 | 1,0 | 0,872 | 0,883 | 0,922 | 0,671 |
| **cascade** | **180** | **0,751** | **0,939** | **0,621** | **0,194** | **0,560** | **1,0** | **1,0** | **0,994** | **0,889** | **0,671** |

**Ce que ça dit** :

- Les **classes fermées** tiennent (0,939) ; les **ouvertes chutent à 0,621** sur le lexique disjoint — les verbes/adjectifs inconnus tombent en NOUN. C'est le coût réel de la généralisation, mesuré.
- **exact 0,194 vs tête 0,560** : le F1 exact bas est surtout un **désaccord de segmentation** entre le générateur S et la grammaire ; la **tête** (type au premier token) monte à **0,560**. La tête sépare la découpe de l'attachement ; l'exact reste la mesure de la découpe.
- **pragmatique 1,0/1,0/0,994/0,889** ; la cascade **préserve** la négation (fusion par type) et couvre **67,1 %** en unités sémantiques.
- **Le vrai neuronal est refusé** (`RefusNeuronal`, `llama-cli` 10 s) : le mock est un double de contrat ; la qualification neuronale reste à faire.

\## L'état

- Fiche : [`rapport-pensee-gold-linguistique.md`](../../reports/rapport-pensee-gold-linguistique.md) ; JSON [`pensee-gold-linguistique.json`](../../reports/pensee-gold-linguistique.json) ; gold [`gold_synthetique.py`](../../tools/tests/linguistique/gold_synthetique.py) / [`.json`](../../tools/tests/linguistique/gold_synthetique
… [1107 caractères tronqués]

### Tour 17 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1003 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Inspecter l'attachement S et les taggers disponibles
- bash — Lire les cibles S et la construction des étiquettes syntagme
- bash — Annoter les cibles d'attachement dans les deux golds
- bash — Corriger le générateur synthétique et vérifier les cibles
- bash — Mesurer l'attachement top-1/top-k sur les deux golds
- bash — Exposer toutes les cibles S et remesurer l'attachement
- bash — Corriger la cible par segment et remesurer
- bash — Ajouter les seuils d'attachement au verdict
- bash — Insérer la fiche d'attachement et les limites
- bash — Mettre l'état à jour pour l'attachement
- bash — Lire les compteurs réels et le tableau corrompu
- bash — Réparer les compteurs et passer les portes
- bash — Committer l'attachement mesuré et la fiche
- job_output

**Synthèse produite :**

⏵ Attachement mesuré : top-1 0,294, top-k 0,338, hasard 0,015 ; la couverture de 34 % est la limite

Le round 4 du goal est livré : l'**attachement** des GP/REL/SUB est mesuré sur le gold 180. Commit **`c5d38030`**.

\## Le dispositif

Les deux golds annotent désormais la **cible** d'attachement : **68 cibles** (13 dans les 20 phrases réelles, 55 dans les 160 synthétiques). Le générateur S propose un attachement ; le bloc expose **toutes** ses cibles (pas seulement le dernier segment ambigu) via `_tokens`/`_segmente` en **lecture seule** — un couplage à l'API interne du S, déclaré.

\## Les résultats

| lecture | source | cibles | couv. | top-1 | top-1/couv. | top-k |
|---|---:|---:|---:|---:|---:|---:|
| **heuristique** | **180** | **68** | **0,338** | **0,294** | **0,870** | **0,338** |
| heuristique | 20 réels | 13 | 0,385 | 0,154 | 0,400 | 0,385 |
| heuristique | 160 synth. | 55 | 0,327 | 0,327 | **1,000** | 0,327 |
| mock seul | 180 | 68 | 0,338 | 0 | 0 | 0 |
| **hasard** | 180 | 68 | — | **0,015** | — | — |

**Ce que ça dit** :

- **La couverture (34 %) est la limite**, pas la cible : le S et le gold ne découpent pas les mêmes **spans** ; seuls 23 des 68 segments à cible sont alignés.
- **Sur les 23 alignés** : le top-k est **100 %**, le top-1 **87 %** ; quand le S propose un attachement, la bonne cible est presque toujours dans ses candidats.
- **Réels 40 %** : les GP au verbe (`dans le parc` → `vu`) sont lus par le S comme le GN le plus proche (`l'homme`) ; le gold préfère le verbe — le désaccord classique d'attachement.
- **Synthétiques 100 %** : la grammaire attache régulièrement ; le S retrouve la cible.
- **Hasard 1,5 %** : le contrôle négatif.
- **`exact` 0** : le S rend la cible en **phrase** (`a vu`), le gold en **tête** (`vu`) ; l'égalité stricte est trop dure, la containment est la bonne mesure.
- **Les 3 cibles anglaises** ne sont pas couvertes (le S est français) : la couverture réelle française est de 23/65.

\## L'état

- Fiche : [`rapport-pensee-gold-linguistique.md`](../../reports/rapport-pensee-gold-linguistique.md) ; JSON [`pensee-gold-linguistique.json`](../../reports/pensee-gold-linguistique.json) ; cibles dans [`gold.py`](../../tools/tests/linguistique/gold.py) et [`gold_synthetique.py`](../../tools/tests/linguistique/gold_synthetique.py).
- Porte `porte-bloc-linguistique` **verte** (gold 180 + attachement + tests + autotest 398 langues) ; `porte-pensee` **10/10**.
- `revue` : **392 fiches / 490 JSON / 118 docs / 81 portes** — ✅ ; 
… [990 caractères tronqués]

### Tour 18 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1003 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Inspecter l'état avant l'attachement par tête
- bash — Ajouter l'attachement par tête et remesurer
- bash — Mettre à jour la fiche et l'état pour l'attachement par tête
- bash — Passer toutes les portes après l'attachement par tête
- bash — Committer l'attachement par tête
- job_output
- bash — Confirmer que le contenu de l'attachement est dans HEAD

**Synthèse produite :**

⏵ Attachement par tête : couverture 1,0, top-1 0,870, top-k 1,0 ; le span reste 0,338

Le round 5 du goal est livré : l'**attachement par tête** mesure la cible sans que la découpe du S la masque.

\## Le résultat

| lecture | source | cibles | couv. tête | **top-1 tête** | **top-k tête** | couv. span | top-1 span |
|---|---:|---:|---:|---:|---:|---:|---:|
| **heuristique** | **180** | **68** | **1,000** | **0,870** | **1,000** | 0,338 | 0,294 |
| heuristique | 20 réels | 13 | 1,000 | 0,400 | 1,000 | 0,385 | 0,154 |
| heuristique | 160 synth. | 55 | 1,000 | **1,000** | 1,000 | 0,327 | 0,327 |
| mock seul | 180 | 68 | 1,000 | 0 | 0 | 0,338 | 0 |
| **hasard** | 180 | 68 | — | **0,015** | — | — | — |

**Ce que ça dit** :

- **La couverture par tête est de 100 %** : le segment prédit qui couvre la **tête** du gold (même type) existe toujours. La couverture de 34 % par **span** était un désaccord de **segmentation**, pas d'attachement.
- **Top-1 tête 87 %, top-k tête 100 %** : la bonne cible est **toujours** dans les candidats du S, et en premier **87 %** du temps.
- **Réels 40 %** : les GP au verbe (`dans le parc` → `vu`) sont lus par le S comme le GN le plus proche (`l'homme`) ; le gold préfère le verbe — le désaccord classique d'attachement, que le top-1 paie.
- **Synthétiques 100 %** : la grammaire attache régulièrement ; le S retrouve la cible.
- **Hasard 1,5 %** : le contrôle négatif.
- **Le span** (34 %, top-1 29 %) reste la mesure de la **découpe** ; la tête est la mesure de l'**attachement**.

\## L'état

- Fiche : [`rapport-pensee-gold-linguistique.md`](../../reports/rapport-pensee-gold-linguistique.md) ; JSON [`pensee-gold-linguistique.json`](../../reports/pensee-gold-linguistique.json) ; évaluateur [`evaluer_gold.py`](../../tools/tests/linguistique/evaluer_gold.py).
- Portes : `porte-bloc-linguistique` **verte** (gold 180 + attachement + tests + autotest 398 langues), `porte-pensee` **10/10**, `taille`, `porte-tableaux`, `schemas`, `journal`, `verifie_en_cours`, `sessions` — **vertes** avant le commit.
- **Course de commit** : le commit **`bcf13fb0`** (D/R/A, six corpus) a emporté mes fichiers **stagés** ; le contenu de l'attachement par tête est bien dans HEAD (`attachement_tete`), mais le message est celui de D/R/A. Le prochain round peut ajouter un commit L/B13 avec le bon chiffre.
- `revue` : rouge sur **un seul compteur** (en-cours 490, disque 491) : un JSON de corpus est arrivé après mon commit ; le prochain round aligne.
- `en-cours` : 2 sessio
… [829 caractères tronqués]

### Tour 19 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1003 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Inspecter DRVM, opérateurs et compteurs
- bash — Inspecter le modèle natif/DRVM et ses points d'appel
- bash — Chercher le serveur natif et les poids DRVM
- bash — Écrire le registre hétérogène et le conteneur DRVM
- bash — Lire les champs de Candidat
- bash — Corriger le champ id et exécuter le DRVM
- bash — Corriger le score et exécuter les trois stratégies
- bash — Ajouter la porte T8 et lancer l'autotest
- bash — Écrire la fiche des opérateurs et mettre l'état à jour
- bash — Passer les portes après les opérateurs hétérogènes
- bash — Rentrer dans T0 et aligner le compteur JSON
- bash — Rentrer dans T0 et repasser les portes
- bash — Committer les opérateurs hétérogènes
- job_output

**Synthèse produite :**

⏵ Opérateurs hétérogènes : 3 genres, sonde 4 appels/coût 48, aveugle 1/33 ; 11/11 portes

Le round 6 du goal est livré : B13 sait faire coexister des opérateurs **symbolique**, **numérique** et **neuronal** dans le même moteur. Commit **`f5d1256d`**.

\## Le résultat

Grille **5×5**, départ `(0,0)`, but `(4,4)` ; trois opérateurs : `pas` (symbolique, coût 1), `saut` (numérique, coût 2), `sonde` (neuronal, coût 5, un appel à la politique).

| stratégie | politique | nœuds | pas | saut | sonde | coût | appels | but |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **A*** | **manhattan** | **23** | 10 | 9 | **4** | **48** | **4** | **oui** |
| A* | aveugle | 20 | 10 | 9 | **1** | 33 | 4 | oui |
| BFS | manhattan | 130 | 63 | 47 | 20 | 257 | 20 | oui |
| BFS | aveugle | 119 | 63 | 47 | 9 | 202 | 20 | oui |

**Ce que ça dit** :

- **Les trois genres coexistent** et sont tracés : le registre rend les genres, le bilan compte chaque opérateur, le coût est `coût × occurrences`.
- **La sonde sert** avec la politique manhattan (**4 nœuds**, **4 appels**, coût 48) ; avec la politique **aveugle**, elle n'est presque pas utilisée (**1 nœud**) et la recherche résout par `pas`/`saut` — le contrôle négatif du **mauvais** opérateur.
- **Le coût est un choix** : l'A* paie 48 pour 23 nœuds, le BFS 257 pour 130 ; le neuronal est cher (5) et doit être **justifié** par la politique, pas par le moteur.
- **A* = greedy** sur ce score (`1/(1+distance)`), comme au banc ; ce n'est pas un bug des opérateurs.
- **Le DRVM** est le **conteneur d'exécution** (registre, politique, moteur, trace, bilan) ; il ne faut pas le confondre avec le **format DRVM** de N0.

\## L'état

- Fiche : [`rapport-pensee-operateurs.md`](../../reports/rapport-pensee-operateurs.md) ; JSON [`pensee-operateurs.json`](../../reports/pensee-operateurs.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T8 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **11/11 portes** ; `porte-bloc-linguistique` **verte** (gold 180 + attachement + 398 langues) ; `revue` : **393 fiches / 494 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Contrat `moteur-de-pensee.md` : T8 ajouté, `operateurs.py` au plan de fichiers.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, `spacy`/`stanza`/`nltk`/`transformers` absents, et **aucun poids `drave-n0`** n'est présent pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé ; la session R4.4 doit
… [658 caractères tronqués]

### Tour 20 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1003 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Annoter les deux lectures de l'attachement
- bash — Remesurer l'attachement avec les deux lectures
- bash — Mettre à jour la fiche et l'état pour la lecture double
- bash — Passer les portes après la lecture double
- bash — Committer la lecture double du gold
- job_output
- bash — Voir si le commit concurrent a emporté la lecture double
- bash — Voir ce qui reste à committer après la course
- bash — Recommitter la lecture double sur le nouveau HEAD

**Synthèse produite :**

⏵ Lecture double : top-1 tête 0,957, 0,800 réel/1,0 synth, 29 cibles ambiguës

Le round 7 du goal est livré : le gold annote désormais les **deux lectures** des attachements ambigus. Commit **`c6fb94e2`**.

\## Le résultat

**97 cibles** d'attachement (18 réelles, 79 synthétiques), dont **29 ambiguës** annotées en double lecture (`dans le parc` → `vu` **ou** `l'homme`, `avec le télescope` → `vu` **ou** `l'homme`, `à manger` → `prêt` **ou** `canard`).

| lecture | cibles | ambiguës | couv. tête | top-1 tête (1 lecture) | **top-1 tête (2 lectures)** | top-k |
|---|---:|---:|---:|---:|---:|---:|
| **heuristique 180** | **97** | **29** | 1,000 | 0,870 | **0,957** | **1,000** |
| heuristique 20 réels | 18 | 5 | 1,000 | 0,400 | **0,800** | 1,000 |
| heuristique 160 synth. | 79 | 24 | 1,000 | 1,000 | **1,000** | 1,000 |
| mock seul | 97 | 29 | 1,000 | 0 | 0 | 0 |
| **hasard** | 97 | — | — | **0,015** | — | — |

**Ce que ça dit** :

- **Le top-1 tête passe de 0,870 à 0,957** quand on accepte les deux lectures ; les **réels** passent de **40 % à 80 %**, les synthétiques restent à 100 %.
- **Le span** reste la mesure de la découpe : 0,323 de top-1 (contre 0,294 avec une seule lecture), 0,338 de couverture.
- **Le désaccord restant (20 %) des réels** est un cas où le S ne propose **aucune** des deux lectures ; le gold les déclare.
- **Le hasard** 1,5 % ; le mock 0 ; la tête est la bonne mesure de l'attachement, le span celle de la segmentation.

\## L'état

- Fiche : [`rapport-pensee-gold-linguistique.md`](../../reports/rapport-pensee-gold-linguistique.md) ; JSON [`pensee-gold-linguistique.json`](../../reports/pensee-gold-linguistique.json) ; golds [`gold.py`](../../tools/tests/linguistique/gold.py) / [`gold_synthetique.py`](../../tools/tests/linguistique/gold_synthetique.py) ; évaluateur [`evaluer_gold.py`](../../tools/tests/linguistique/evaluer_gold.py).
- Portes : `porte-bloc-linguistique` **verte** (gold 180 + attachement + 398 langues), `porte-pensee` **11/11** (opérateurs hétérogènes), `revue` **393 fiches / 496 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- **Le commit `c6fb94e2`** porte aussi deux fichiers N2 arrivés dans l'index (`rapport-n2-canal.md`, `canal_structure.py`) : les sessions concurrentes partagent l'index ; le contenu de la lecture double est bien dans HEAD.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.p
… [647 caractères tronqués]

### Tour 21 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1003 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — Ajouter le cadenas où la sonde est nécessaire
- bash — Ajouter la porte T9 et lancer l'autotest
- bash — Écrire la fiche du neuronal nécessaire et l'état
- bash — Passer les portes après le neuronal nécessaire
- bash — Rentrer dans T0 et aligner les compteurs
- bash — Aligner le compteur JSON et vérifier les portes
- bash — Committer le neuronal nécessaire
- job_output
- bash — Voir si le commit concurrent a emporté le neuronal nécessaire
- bash — Recommitter le neuronal nécessaire sur le nouveau HEAD
- bash — Ajouter la fiche à l'état et committer

**Synthèse produite :**

⏵ Neuronal nécessaire : cadenas, sonde seule, avant 3 appels/but, aveugle 20/sans but ; 12/12

Le round 8 du goal est livré : un problème où le neuronal n'est plus **utile** mais **nécessaire**. Commit **`15c69b98`**.

\## Le cadenas

État : une position `0..3`. **Un seul opérateur**, `sonde` (genre **neuronal**) : la politique propose `avant` ou `arrière`, le moteur avance d'un cran. But : `3`.

| politique | nœuds | appels | coût | but |
|---|---:|---:|---:|---|
| **avant** | **3** | **3** | **3** | **oui** |
| arrière (aveugle) | 20 | 20 | 20 | **non** |

**Ce que ça dit** :

- **Le seul chemin est la politique** : `pas` et `saut` n'existent pas dans ce registre ; le moteur ne peut avancer que par la sonde.
- **La bonne politique atteint le but en 3 coups** ; **l'aveugle tourne** (0→1→0→…) et échoue même avec 20 nœuds : le contrôle négatif n'est plus « inutile », il est **décisif**.
- **Le coût est le coût du modèle** : 3 appels contre 20 ; la politique est le **seul** levier.
- Le **`DRVM`** utilise désormais le **but du problème courant** (grille ou cadenas), pas une constante.

\## L'état

- Fiche : [`rapport-pensee-necessaire.md`](../../reports/rapport-pensee-necessaire.md) ; JSON [`pensee-necessaire.json`](../../reports/pensee-necessaire.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T9 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **12/12 portes** ; `porte-bloc-linguistique` **verte** (gold 180 + attachement + 398 langues) ; `revue` **395 fiches / 498 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget ; `sessions.py` : le plan R4.4 reste périmé (session R4.4).
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle. Le cadenas mesure la **nécessité structurelle**, pas la qualité d'un modèle.

\## La suite

1. **L — 200+ phrases réelles** (relatives, portée, anglais) : le gold synthétique ne remplace pas le réel.
2. **Politique DRVM/native** et coût mesuré, si les poids natifs arrivent.
3. **Cadenas non linéaire** (plusieurs chemins, un piège) pour que la politique puisse être **bonne** ou **mauvaise** sans être trivialement l'une ou l'autre.
4. **Modèle neuronal** si un tagger/runner se débloque ; sinon, garder le mock et le dire.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque les 200+ phrases réelles du gold L.

### Tour 22 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1003 caractères tronqués]

*15 appels d'outils.* Actions notables :

- bash — Écrire 40 phrases réelles supplémentaires
- bash — Corriger la phrase r030 et générer le gold réel
- bash — Mesurer le gold avec les 60 phrases réelles
- bash — Mettre à jour la fiche et l'état pour le gold 220
- bash — Rentrer dans T0 et aligner les compteurs
- bash — Corriger la ligne des compteurs et relancer la revue
- bash — Aligner les compteurs et passer les portes
- bash — Committer le gold 220 avec 40 phrases réelles
- job_output
- bash — Voir si la course a emporté le gold 220
- bash — Recommitter le gold 220 sur le nouveau HEAD
- bash — Vérifier si le gold 220 est dans HEAD
- bash — Recommitter le gold 220 avec réessai

**Synthèse produite :**

⏵ Gold 220 : 60 réels + 160 synthétiques, POS 0,765 (réel 0,861), tête 0,510 ; 12/12

Le round 9 du goal est livré : le gold réel passe de 20 à **60 phrases**, le gold total à **220**. Commit **`46fa2c82`**.

\## Le gold 220

**60 phrases réelles** (20 dans `gold.py` + **40 nouvelles** dans `gold_reel.py`, 20 françaises et 20 anglaises) + **160 synthétiques** ; **993 tokens**. Les 40 nouvelles sont écrites après le bloc, avec POS, segments GN/GV/GP/REL/SUB et pragmatique (négation, modalité, question, double sens).

| lecture | phrases | POS | syntagmes exacts | tête | att. tête | top-k tête |
|---|---:|---:|---:|---:|---:|---:|
| **heuristique — 220** | **220** | **0,765** | **0,190** | **0,510** | 0,957 | **1,000** |
| heuristique — 60 réels | 60 | **0,861** | 0,241 | 0,370 | 0,800 | 1,000 |
| dont 20 réels | 20 | 0,924 | 0,356 | 0,489 | 0,800 | 1,000 |
| dont 40 nouveaux | 40 | 0,825 | 0,176 | 0,302 | — | — |
| heuristique — 160 synth. | 160 | 0,725 | 0,168 | **0,570** | 1,000 | 1,000 |
| mock seul — 220 | 220 | 0,416 | 0,147 | 0,538 | 0 | 0 |
| **hasard** | 220 | — | — | — | **0,015** | — |

**Ce que ça dit** :

- **Les 60 réels** : POS **0,861**, contre 0,725 sur le synthétique ; les 40 nouvelles (0,825) sont un peu sous les 20 premières (0,924) — c'est la **variété réelle** qui coûte.
- **Le syntagme exact** reste bas (0,190 ; 0,241 sur le réel) : c'est la **découpe** du S, pas la structure ; la **tête** est à 0,510.
- **L'attachement** est mesuré sur **97 cibles** (les 20 réels + les 160 synthétiques) ; les **40 nouvelles n'ont pas encore de cible** : leur attachement n'est pas compté, et le top-1 tête reste 0,957 sur les 97.
- **Le hasard** 1,5 % ; le mock 0 ; les 60 réels sont un **vrai** test, pas un doublon du générateur.

\## L'état

- Fiche : [`rapport-pensee-gold-linguistique.md`](../../reports/rapport-pensee-gold-linguistique.md) ; JSON [`pensee-gold-linguistique.json`](../../reports/pensee-gold-linguistique.json) ; golds [`gold_reel.py`](../../tools/tests/linguistique/gold_reel.py) / [`gold_reel.json`](../../tools/tests/linguistique/gold_reel.json).
- Portes : `porte-bloc-linguistique` **verte** (gold 220 + tests + 398 langues), `porte-pensee` **12/12**, `revue` **396 fiches / 498 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` r
… [596 caractères tronqués]

### Tour 23 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Annoter les cibles des 40 nouvelles phrases réelles
- bash — Mesurer l'attachement sur les 60 phrases réelles
- bash — Mettre à jour la fiche et l'état pour les 60 réels
- bash — Passer les portes et committer les cibles des 60 réels
- job_output

**Synthèse produite :**

⏵ Attachement des 60 réels : tête top-1 0,972 (0,929 réel), 36 cibles ambiguës ; 12/12

Le round 10 du goal est livré : les **40 nouvelles phrases réelles** ont leurs **cibles d'attachement**, et le réel est enfin mesuré sur les deux niveaux. Commit **`9396fa40`**.

\## Le résultat

**21 cibles** ajoutées aux 40 nouvelles (dont 4 ambiguës) ; le réel passe à **60 phrases** avec **30 cibles** ; le total à **85 cibles** (30 réelles + 55 synthétiques), dont **36 ambiguës**.

| lecture | cibles | ambiguës | couv. tête | **top-1 tête** | **top-k tête** |
|---|---:|---:|---:|---:|---:|
| **heuristique 220** | **85** | **36** | **1,000** | **0,972** | **0,889** |
| heuristique 60 réels | 30 | 14 | 1,000 | **0,929** | **1,000** |
| dont 20 réels | 13 | 6 | 1,000 | 0,833 | 1,000 |
| dont 40 nouveaux | 17 | 8 | 1,000 | **1,000** | 1,000 |
| heuristique 160 synth. | 55 | 22 | 1,000 | 1,000 | 0,818 |
| mock seul | 85 | 36 | 1,000 | 0 | 0 |
| **hasard** | — | — | — | **0,015** | — |

**Ce que ça dit** :

- **Le réel tient** : top-1 tête **0,929** sur les 60 réels, **1,000** sur les 40 nouveaux ; la **couverture par tête est de 100 %**.
- **Les 36 cibles ambiguës** (double lecture) expliquent l'essentiel du gain : le top-1 des 20 premiers réels reste 0,833, celui des 40 nouveaux 1,000.
- **Le top-k** baisse à 0,889 sur les 220 (le S ne propose pas toujours la cible dans ses candidats) ; sur le réel, il est à 1,000.
- **Le span** reste la mesure de la découpe : top-1 0,412, top-k 0,377 ; la tête est la mesure de l'attachement.
- **Le POS** 0,765 (réel 0,861), le syntagme exact 0,210 (réel 0,294) — le gold réel est plus dur que le synthétique.

\## L'état

- Fiche : [`rapport-pensee-gold-linguistique.md`](../../reports/rapport-pensee-gold-linguistique.md) ; JSON [`pensee-gold-linguistique.json`](../../reports/pensee-gold-linguistique.json) ; golds [`gold_reel.py`](../../tools/tests/linguistique/gold_reel.py) / [`gold_reel.json`](../../tools/tests/linguistique/gold_reel.json).
- Portes : `porte-bloc-linguistique` **verte** (gold 220 + attachement + 398 langues), `porte-pensee` **12/12**, `revue` **397 fiches / 498 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé ; la session R4.4 doit le rafraîchir.

\## La suite

1. **200+ phrases réelles** : continue
… [480 caractères tronqués]

### Tour 24 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Ajouter 40 phrases réelles supplémentaires
- bash — Mesurer le gold avec les 100 phrases réelles
- bash — Mettre à jour la fiche et l'état pour les 100 réels
- bash — Passer les portes et committer le gold 260
- job_output

**Synthèse produite :**

⏵ Gold 260 : 100 réels + 160 synthétiques, POS 0,774, tête 0,954 (réel 0,909)

Le round 11 du goal est livré : le gold réel passe de 60 à **100 phrases**, le gold total à **260**. Commit **`5241f1f7`**.

\## Le gold 260

**100 phrases réelles** (20 dans `gold.py` + **80** dans `gold_reel.py`, 40 françaises et 40 anglaises) + **160 synthétiques** ; **1 199 tokens**. Les 80 nouvelles couvrent les GP (lieu, temps, destinataire, cible, moyen), les relatives (`que`, `où`, `that`, `where`), les adverbes, les négations, les questions, les modalités et les doubles sens.

| lecture | phrases | POS | exact | tête | att. tête | top-k tête |
|---|---:|---:|---:|---:|---:|---:|
| **heuristique — 260** | **260** | **0,774** | **0,210** | **0,486** | **0,954** | **0,909** |
| heuristique — 100 réels | 100 | **0,842** | 0,259 | 0,377 | **0,909** | **1,000** |
| dont 20 réels | 20 | 0,924 | 0,396 | 0,506 | 0,833 | 1,000 |
| dont 80 nouveaux | 80 | 0,820 | 0,222 | 0,342 | **0,938** | 1,000 |
| heuristique — 160 synth. | 160 | 0,725 | 0,175 | **0,562** | 1,000 | 0,818 |
| mock seul — 260 | 260 | 0,416 | 0,147 | 0,538 | 0 | 0 |
| **hasard** | — | — | — | — | **0,015** | — |

**Ce que ça dit** :

- **Le réel tient** : POS **0,842** sur les 100 réels (0,924 sur les 20 premiers, 0,820 sur les 80 nouveaux) ; le gold réel est **plus dur** que le synthétique (0,725).
- **L'attachement par tête** : **0,954** sur les 260, **0,909** sur le réel, **0,938** sur les 80 nouveaux ; la couverture par tête est de **100 %**.
- **Le top-k réel est à 1,000** : le S propose toujours la cible quand le gold la donne ; le top-k global (0,909) baisse sur les synthétiques.
- **Le span** reste la mesure de la découpe : **0,415** top-1, 0,396 top-k ; la tête est la mesure de l'attachement.
- **Le POS** 0,774 ; le syntagme exact 0,210 (réel 0,259) ; la complexité des 80 nouvelles fait baisser la tête (0,486 contre 0,510).

\## L'état

- Fiche : [`rapport-pensee-gold-linguistique.md`](../../reports/rapport-pensee-gold-linguistique.md) ; JSON [`pensee-gold-linguistique.json`](../../reports/pensee-gold-linguistique.json) ; golds [`gold_reel.py`](../../tools/tests/linguistique/gold_reel.py) / [`gold_reel.json`](../../tools/tests/linguistique/gold_reel.json).
- Portes : `porte-bloc-linguistique` **verte** (gold 260 + tests + 398 langues), `porte-pensee` **12/12**, `revue` **397 fiches / 498 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqu
… [738 caractères tronqués]

### Tour 25 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Ajouter 40 phrases réelles supplémentaires (r081-r120)
- bash — Mesurer le gold avec les 140 phrases réelles
- bash — Mettre à jour la fiche et l'état pour les 140 réels
- bash — Passer les portes et committer le gold 300
- job_output

**Synthèse produite :**

⏵ Gold 300 : 140 réels + 160 synthétiques, POS 0,773, tête 0,962 (réel 0,936)

Le round 12 du goal est livré : le gold réel passe de 100 à **140 phrases**, le gold total à **300**. Commit **`bcab8bd2`**.

\## Le gold 300

**140 phrases réelles** (20 dans `gold.py` + **120** dans `gold_reel.py`, 60 françaises et 60 anglaises) + **160 synthétiques** ; **1 402 tokens**. Les 120 nouvelles couvrent les GP (lieu, temps, destinataire, manière, cible), les relatives (`que`, `où`, `that`, `where`), les adjectifs, les adverbes et les questions.

| lecture | phrases | POS | exact | tête | att. tête | top-k tête |
|---|---:|---:|---:|---:|---:|---:|
| **heuristique — 300** | **300** | **0,773** | **0,213** | **0,466** | **0,962** | **0,925** |
| heuristique — 140 réels | 140 | **0,819** | 0,251 | 0,368 | **0,936** | **1,000** |
| dont 20 réels | 20 | 0,924 | 0,396 | 0,506 | 0,833 | 1,000 |
| dont 120 nouveaux | 120 | 0,801 | 0,225 | 0,343 | **0,960** | 1,000 |
| heuristique — 160 synth. | 160 | 0,725 | 0,175 | **0,562** | 1,000 | 0,818 |
| mock seul — 300 | 300 | 0,416 | 0,147 | 0,538 | 0 | 0 |
| **hasard** | — | — | — | — | **0,015** | — |

**Ce que ça dit** :

- **Le réel tient** : POS **0,819** sur les 140 réels ; les 120 nouveaux (0,801) restent au-dessus du synthétique (0,725) — le gold réel est plus dur mais pas effondré.
- **L'attachement par tête** : **0,962** sur les 300, **0,936** sur le réel, **0,960** sur les 120 nouveaux ; la couverture par tête est de **100 %**.
- **Le top-k réel est à 1,000** ; le top-k global (0,925) baisse sur les synthétiques (0,818).
- **Le span** reste la mesure de la découpe : **0,431** top-1, 0,415 top-k ; la tête est la mesure de l'attachement.
- **La complexité des 120 nouvelles** fait baisser la tête (0,466) et monte l'exact (0,213) ; le POS réel reste 0,819.

\## L'état

- Fiche : [`rapport-pensee-gold-linguistique.md`](../../reports/rapport-pensee-gold-linguistique.md) ; JSON [`pensee-gold-linguistique.json`](../../reports/pensee-gold-linguistique.json) ; golds [`gold_reel.py`](../../tools/tests/linguistique/gold_reel.py) / [`gold_reel.json`](../../tools/tests/linguistique/gold_reel.json).
- Portes : `porte-bloc-linguistique` **verte** (gold 300 + tests + 398 langues), `porte-pensee` **12/12**, `revue` **397 fiches / 498 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique
… [634 caractères tronqués]

### Tour 26 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Ajouter 60 phrases réelles (r121-r180), atteindre 200 réels
- bash — Mesurer le gold avec les 200 phrases réelles
- bash — Mettre à jour la fiche et l'état pour les 200 réels
- bash — Passer les portes et committer le gold 360
- job_output

**Synthèse produite :**

⏵ Gold 360 : 200 réels + 160 synthétiques, POS 0,772, tête 0,966 (réel 0,946) — cible 200+ atteinte

Le round 13 du goal est livré : le gold réel atteint **200 phrases**, la **cible 200+** est remplie. Commit **`adaaeae9`**.

\## Le gold 360

**200 phrases réelles** (20 dans `gold.py` + **180** dans `gold_reel.py`, 90 françaises et 90 anglaises) + **160 synthétiques** ; **1 698 tokens**. Les 180 nouvelles couvrent les GP (lieu, temps, destinataire, manière, cible), les relatives (`que`, `où`, `that`, `where`), les adjectifs, les adverbes, les questions et les négations.

| lecture | phrases | POS | exact | tête | att. tête | top-k tête |
|---|---:|---:|---:|---:|---:|---:|
| **heuristique — 360** | **360** | **0,772** | **0,198** | **0,435** | **0,966** | **0,932** |
| heuristique — 200 réels | 200 | **0,804** | 0,213 | 0,345 | **0,946** | **1,000** |
| dont 20 réels | 20 | 0,924 | 0,396 | 0,506 | 0,833 | 1,000 |
| dont 180 nouveaux | 180 | 0,790 | 0,192 | 0,326 | **0,968** | 1,000 |
| heuristique — 160 synth. | 160 | 0,725 | 0,175 | **0,562** | 1,000 | 0,818 |
| mock seul — 360 | 360 | 0,416 | 0,147 | 0,538 | 0 | 0 |
| **hasard** | — | — | — | — | **0,015** | — |

**Ce que ça dit** :

- **La cible 200+ est atteinte** : 200 phrases réelles, POS **0,804**, contre 0,725 sur le synthétique.
- **L'attachement par tête** : **0,966** sur les 360, **0,946** sur le réel, **0,968** sur les 180 nouveaux ; la couverture par tête est de **100 %**.
- **Le top-k réel est à 1,000** ; le top-k global (0,932) baisse sur les synthétiques (0,818).
- **Le span** reste la mesure de la découpe : **0,428** top-1, 0,413 top-k ; la tête est la mesure de l'attachement.
- **La complexité des 180 nouvelles** fait baisser la tête (0,435) et l'exact (0,198) ; le POS réel reste 0,804.

\## L'état

- Fiche : [`rapport-pensee-gold-linguistique.md`](../../reports/rapport-pensee-gold-linguistique.md) ; JSON [`pensee-gold-linguistique.json`](../../reports/pensee-gold-linguistique.json) ; golds [`gold_reel.py`](../../tools/tests/linguistique/gold_reel.py) / [`gold_reel.json`](../../tools/tests/linguistique/gold_reel.json).
- Portes : `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues), `porte-pensee` **12/12**, `revue` **397 fiches / 498 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le 
… [668 caractères tronqués]

### Tour 27 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Ajouter le labyrinthe non linéaire et l'exécuter
- bash — Ajouter la porte T10 et lancer l'autotest
- bash — Écrire la fiche du labyrinthe et l'état
- bash — Rentrer dans T0
- bash — Passer les portes et committer le labyrinthe
- job_output

**Synthèse produite :**

⏵ Labyrinthe non linéaire : bonne politique 17 nœuds/34 (sonde 2), aveugle 15/24 (sonde 0) ; 13/13

Le round 14 du goal est livré : le **labyrinthe non linéaire** mesure l'usage du neuronal sur plusieurs chemins. Commit **`0e5d99fe`**.

\## Le labyrinthe

Grille **5×5**, murs `{(0,1),(1,1),(2,1),(4,1),(1,3),(2,3),(3,3)}`, départ `(0,0)`, but `(4,4)`. Trois opérateurs : `pas` (symbolique, 1), `saut` (numérique, 2), `sonde` (neuronal, 5).

| politique | nœuds | pas | saut | sonde | coût | appels | but |
|---|---:|---:|---:|---:|---:|---:|---|
| **manhattan** | **17** | 6 | 9 | **2** | **34** | **4** | **oui** |
| aveugle | 15 | 6 | 9 | **0** | 24 | 4 | oui |

**Ce que ça dit** :

- **La bonne politique utilise la sonde** (2 nœuds) ; l'**aveugle** l'ignore complètement : ses propositions tombent sur les murs ou le piège, l'A* les écarte.
- **L'aveugle résout quand même** par `pas`/`saut` : le neuronal est **utile** ici, pas **nécessaire** — la limite est écrite.
- **Le coût plus bas de l'aveugle** (24) vient de l'absence d'appels à la sonde (coût 5 déclaré) ; le neuronal est cher et doit être justifié.
- **Le labyrinthe est non linéaire** (plusieurs chemins, un piège), mais le symbolique/numérique suffit ; le prochain banc devra piéger l'aveugle.

\## L'état

- Fiche : [`rapport-pensee-labyrinthe.md`](../../reports/rapport-pensee-labyrinthe.md) ; JSON [`pensee-labyrinthe.json`](../../reports/pensee-labyrinthe.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T10 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **13/13 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **398 fiches / 499 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé ; la session R4.4 doit le rafraîchir.

\## La suite

1. **Un labyrinthe où l'aveugle échoue** : un piège qui **bloque** le pas/saut (une porte qui ne s'ouvre que par la sonde), pour que la négative échoue vraiment.
2. **Politique DRVM/native** et coût mesuré, si les poids natifs arrivent.
3. **L** : 200 réels atteints ; le gold peut encore grandir (relatives, portée, anglais).
4. **Modèle neuronal** si un tagger/runner se débloque ; sinon, garder le mock et le dire.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round 
… [42 caractères tronqués]

### Tour 28 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Ajouter le labyrinthe à porte et l'exécuter
- bash — Fermer l'autre chemin et vérifier que l'aveugle échoue
- bash — Fermer le bas et vérifier que l'aveugle échoue
- bash — Ajouter la porte T11 et lancer l'autotest
- bash — Écrire la fiche de la porte et l'état
- bash — Passer les portes et committer la porte neuronale
- job_output

**Synthèse produite :**

⏵ Porte neuronale : bonne politique 28 nœuds/58 (sonde 5), aveugle 200/483 sans but ; 14/14

Le round 15 du goal est livré : la **porte neuronale** rend le modèle **nécessaire**, pas seulement utile. Commit **`5853b206`**.

\## La porte

Grille **5×5**, murs `{(0,1),(1,1),(2,1),(4,1),(4,2),(1,2),(2,2),(1,3),(3,4)}`, porte `(3,3)`, départ `(0,0)`, but `(4,4)`. La porte ne s'ouvre que si la **politique** propose la direction de la porte (`bas` depuis `(3,2)`) ; les `pas`/`saut` sont bloqués par la porte fermée.

| politique | nœuds | pas | saut | sonde | coût | appels | but |
|---|---:|---:|---:|---:|---:|---:|---|
| **manhattan** | **28** | 13 | 10 | **5** | **58** | 7 | **oui** |
| aveugle | 200 | 100 | 39 | 61 | 483 | 66 | **non** |

**Ce que ça dit** :

- **Le neuronal est nécessaire** : la porte ne s'ouvre que par la **bonne** politique ; l'aveugle propose la mauvaise direction, la porte reste fermée, le but est inatteignable.
- **L'aveugle épuise son budget** (200 nœuds) sans atteindre le but ; le coût 483 est le prix de ses 61 appels inutiles à la sonde.
- **La bonne politique paie** 58 pour 28 nœuds, dont 5 sondes : le neuronal est **cher** et **décisif** ici.
- **La porte est le seul chemin** : les murs `(4,2)` et `(3,4)` bouchent les contournements.

\## L'état

- Fiche : [`rapport-pensee-porte.md`](../../reports/rapport-pensee-porte.md) ; JSON [`pensee-porte.json`](../../reports/pensee-porte.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T11 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **14/14 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **399 fiches / 500 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé ; la session R4.4 doit le rafraîchir.

\## La suite

1. **Politique DRVM/native** : brancher un vrai modèle quand ses poids seront là ; la porte mesurera la **qualité** de la politique, pas seulement sa nécessité.
2. **Coût mesuré** : remplacer le coût 5 par la latence réelle.
3. **L** : 200 réels atteints ; le gold peut encore grandir.
4. **B13** : une porte **apprise** (le modèle doit découvrir la direction) plutôt que déclarée.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque la porte apprise ou la politique D
… [11 caractères tronqués]

### Tour 29 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — Ajouter la politique apprise par Q-learning et la tester
- bash — Importer random et tester la politique apprise
- bash — Ajouter la porte T12 et lancer l'autotest
- bash — Écrire la fiche de la porte apprise et l'état
- bash — Rentrer dans T0 et passer les portes
- bash — Trim final pour T0
- bash — Trim final et portes
- bash — Committer la porte apprise
- job_output
- bash — Vérifier l'état et la fiche à référencer
- bash — Référencer la fiche, trim et committer

**Synthèse produite :**

⏵ Porte apprise : Q-table 67 états, 30 nœuds/but (sonde 7), 200 épisodes ; 15/15

Le round 16 du goal est livré : la politique **apprise** découvre la porte seule, sans règle. Commit **`ad3da0b6`**.

\## La porte apprise

La `PolitiqueApprise` ne connaît **pas** la direction de la porte : elle apprend par **Q-learning tabulaire** (récompense +1 au but, -0,01 par pas, +0,1 à l'ouverture), **200 épisodes**, ε-greedy.

| politique | états-Q | nœuds | sonde | coût | but |
|---|---:|---:|---:|---:|---|
| **apprise (200 épisodes)** | **67** | **30** | **7** | **68** | **oui** |
| manhattan (règle) | — | 28 | 5 | 58 | oui |
| aveugle | — | 200 | 61 | 483 | non |

**Ce que ça dit** :

- **Le modèle apprend la porte** : **67 états-Q** suffisent, sans la règle déclarée ; le but est atteint en 30 nœuds.
- **Il paie un peu plus que la règle** (68 contre 58, 30 contre 28) : l'apprentissage tabulaire est **proche** de la règle, pas identique.
- **L'aveugle reste le négatif** (200 nœuds, sans but) : la Q-table n'est pas l'aveugle.
- **La Q-table est petite** (67 états) : le labyrinthe 5×5 est un jouet, mais il prouve que le **modèle** peut être une **table apprise**, pas seulement une règle.

\## L'état

- Fiche : [`rapport-pensee-porte-apprise.md`](../../reports/rapport-pensee-porte-apprise.md) ; JSON [`pensee-porte-apprise.json`](../../reports/pensee-porte-apprise.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T12 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **15/15 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` : la dernière passe a vu **501/502 JSON** (un JSON concurrent est arrivé) — le prochain round aligne le compteur.
- `en-cours` 2 sessions, T0 dans le budget ; `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.

\## La suite

1. **Courbe d'apprentissage** : tracer le but/nœuds contre les épisodes (50, 100, 200, 400, 800) et sur plusieurs graines.
2. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
3. **L** : 200 réels atteints ; le gold peut encore grandir.
4. **B13** : une porte **stochastique** ou **cachée**, pour que l'apprentissage soit un vrai défi.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round trace la courbe d'apprentissage de la porte.

### Tour 30 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Tracer la courbe d'apprentissage de la porte
- bash — Ajouter la porte T13 et lancer l'autotest
- bash — Écrire la fiche de la courbe et l'état
- bash — Passer les portes et committer la courbe
- job_output

**Synthèse produite :**

⏵ Courbe d'apprentissage : 15/15 buts (50–800 épisodes × 3 graines), 30 nœuds, Q 52–83 ; 16/16

Le round 17 du goal est livré : la **courbe d'apprentissage** de la porte est tracée sur 15 runs. Commit **`039e0500`**.

\## La courbe

`PolitiqueApprise` (Q-learning tabulaire) entraînée sur **5 budgets d'épisodes** (50, 100, 200, 400, 800) × **3 graines** (15 runs).

| épisodes | graines | états-Q | nœuds | sonde | coût | buts |
|---:|---:|---:|---:|---:|---:|---:|
| 50 | 0,1,2 | 52–74 | 30 | 7 | 68 | **3/3** |
| 100 | 0,1,2 | 52–74 | 30 | 7 | 68 | **3/3** |
| 200 | 0,1,2 | 61–74 | 30 | 7 | 68 | **3/3** |
| 400 | 0,1,2 | 62–83 | 30 | 7 | 68 | **3/3** |
| 800 | 0,1,2 | 62–83 | 30 | 7 | 68 | **3/3** |

**Ce que ça dit** :

- **La porte est apprise dès 50 épisodes** : 15/15 runs atteignent le but ; le Q-learning tabulaire n'a pas besoin de 200 épisodes pour trouver la direction.
- **La performance est plate** (30 nœuds, coût 68) : une fois la porte connue, l'A* fait le reste ; les épisodes supplémentaires n'améliorent pas le chemin.
- **La Q-table grandit** (52 → 83 états) : plus d'exploration, plus de couples état-action, mais pas de gain de chemin.
- **Les 3 graines convergent** : la porte n'est pas un coup de chance d'une graine.
- **La limite est écrite** : l'A* **masque** la politique ; la courbe plate mesure l'A*, pas l'apprentissage seul.

\## L'état

- Fiche : [`rapport-pensee-courbe.md`](../../reports/rapport-pensee-courbe.md) ; JSON [`pensee-courbe.json`](../../reports/pensee-courbe.json) ; code [`courbe.py`](../../tools/pensee/courbe.py) ; T13 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **16/16 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **402 fiches / 504 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **La politique seule** (sans A*) : mesurer le taux de but et les nœuds par épisodes, pour voir l'apprentissage sans le masque de l'A*.
2. **Porte stochastique** : l'ouverture réussit à 80 % ; la politique doit réessayer.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round mesure la politique seu
… [12 caractères tronqués]

### Tour 31 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Mesurer la politique seule sans A*
- bash — Ajouter la porte T14 et lancer l'autotest
- bash — Écrire la fiche de la politique seule et l'état
- bash — Aligner les compteurs et passer les portes
- bash — Committer la politique seule
- job_output

**Synthèse produite :**

⏵ Politique seule : 8 pas, 15/15 buts sans A* ; 17/17

Le round 18 du goal est livré : la **politique seule** conduit le labyrinthe à porte **sans A***. Commit **`82580dda`**.

\## La politique seule

La `PolitiqueApprise` entraînée suit son **argmax Q** à chaque état `(x, y, open)` ; aucun A*, aucun budget de recherche. La porte s'ouvre si l'action la vise.

| épisodes | graines | états-Q | buts seuls | pas | but avec A* |
|---:|---:|---:|---:|---:|---:|
| 50 | 0,1,2 | 52–74 | **3/3** | **8** | 3/3 |
| 100 | 0,1,2 | 52–74 | **3/3** | **8** | 3/3 |
| 200 | 0,1,2 | 61–74 | **3/3** | **8** | 3/3 |
| 400 | 0,1,2 | 62–83 | **3/3** | **8** | 3/3 |
| 800 | 0,1,2 | 62–83 | **3/3** | **8** | 3/3 |

**Ce que ça dit** :

- **La politique seule atteint le but en 8 pas** : c'est le **chemin optimal** (Manhattan 8) ; la Q-table n'a pas seulement appris la porte, elle a appris le **chemin**.
- **15/15 runs**, y compris à **50 épisodes** : l'apprentissage est **complet** très tôt sur ce jouet ; les épisodes supplémentaires ne changent pas le chemin.
- **L'A* n'était pas nécessaire** pour exécuter : il servait de **cadre** à la sonde ; la politique seule est le **vrai** test de ce qui est appris.
- **La Q-table reste petite** (52–83 états) : le jouet est déterministe, mais la preuve est claire : le modèle peut être une **table** qui **conduit**.

\## L'état

- Fiche : [`rapport-pensee-seule.md`](../../reports/rapport-pensee-seule.md) ; JSON [`pensee-courbe.json`](../../reports/pensee-courbe.json) ; code [`courbe.py`](../../tools/pensee/courbe.py) ; T14 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **17/17 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **404 fiches / 505 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Porte stochastique** : 80 % d'ouverture ; la politique doit réessayer.
2. **Labyrinthe plus long** : tester la **généralisation** de la table (ou un réseau).
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque la porte stochastique.

### Tour 32 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Ajouter la porte stochastique et la tester
- bash — Ajouter la porte T15 et lancer l'autotest
- bash — Écrire la fiche stochastique et l'état
- bash — Passer les portes et committer la porte stochastique
- job_output

**Synthèse produite :**

⏵ Porte stochastique : 80 %, 30 nœuds/but, sonde 7 ; 18/18

Le round 19 du goal est livré : la **porte stochastique** à 80 % ne bloque pas la politique apprise. Commit **`f9c112fd`**.

\## La porte stochastique

Même labyrinthe que T11, mais `sonde_p_sto` ouvre la porte avec **80 %** de probabilité ; en cas d'échec, l'état **reste** (la politique doit réessayer). La politique est celle de T12 (200 épisodes, graine 0), entraînée sur la porte **déterministe**.

| essai | nœuds | sonde | coût | but |
|---|---:|---:|---:|---|
| **apprise + A*** | **30** | **7** | **68** | **oui** |

**Ce que ça dit** :

- **Le bruit ne bloque pas** : l'A* explore et la sonde réessaie ; le but est atteint en 30 nœuds, comme sur la porte déterministe.
- **La politique apprise transfère** : elle n'a pas été entraînée sur le bruit, mais elle vise toujours la porte ; le moteur gère les échecs.
- **Le coût est identique** (68) : les 7 appels de sonde incluent les essais.
- **Le vrai test serait la politique seule** sur le bruit : elle peut tourner si la porte résiste ; c'est la prochaine mesure.

\## L'état

- Fiche : [`rapport-pensee-stochastique.md`](../../reports/rapport-pensee-stochastique.md) ; JSON [`pensee-stochastique.json`](../../reports/pensee-stochastique.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T15 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **18/18 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **405 fiches / 506 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **La politique seule sur le bruit** : combien de fois tourne-t-elle avant d'ouvrir ?
2. **Porte qui se referme** : après un pas, la porte se referme ; le moteur doit repasser.
3. **Porte apprise avec le bruit** : entraîner sur la porte stochastique.
4. **Politique DRVM/native** : un vrai modèle quand les poids seront là.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round mesure la politique seule sur le bruit.

### Tour 33 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Mesurer la politique seule sur la porte stochastique
- bash — Ajouter la porte T16 et lancer l'autotest
- bash — Écrire la fiche de la politique seule sur le bruit
- bash — Aligner le compteur et passer les portes
- bash — Committer la politique seule sur le bruit
- job_output

**Synthèse produite :**

⏵ Politique seule sur le bruit : 8–10 pas, 1–3 essais, 15/15 buts ; 19/19

Le round 20 du goal est livré : la **politique seule** réessaie la porte à 80 % et atteint le but. Commit **`99f8dcb2`**.

\## La politique seule sur le bruit

À l'état `(3,2,False)`, la politique propose `bas` ; la porte s'ouvre avec **80 %** ; en cas d'échec, l'état reste et la politique **réessaie**. Aucun A*, aucun budget de recherche.

| épisodes | graines | buts seuls | pas | essais | but seul (déterministe) |
|---:|---:|---:|---:|---:|---:|
| 50 | 0,1,2 | **3/3** | 8–10 | 1–3 | 3/3 (8) |
| 100 | 0,1,2 | **3/3** | 8–10 | 1–3 | 3/3 (8) |
| 200 | 0,1,2 | **3/3** | 8–10 | 1–3 | 3/3 (8) |
| 400 | 0,1,2 | **3/3** | 8–10 | 1–3 | 3/3 (8) |
| 800 | 0,1,2 | **3/3** | 8–10 | 1–3 | 3/3 (8) |

**Ce que ça dit** :

- **La politique seule persiste** : elle réessaie (1–3 essais) et atteint le but en 8–10 pas ; la Q-table **transfère** du déterministe au bruit.
- **Le coût du bruit est faible** : +1 à +2 pas, +1 à +3 essais ; le chemin reste optimal une fois la porte ouverte.
- **15/15 runs** ; les 3 graines ont des essais différents (1, 2, 3) mais toutes réussissent.
- **La Q-table reste petite** (52–83 états) : le bruit ne change pas sa taille, seulement le nombre d'essais.

\## L'état

- Fiche : [`rapport-pensee-sto-seule.md`](../../reports/rapport-pensee-sto-seule.md) ; JSON [`pensee-courbe.json`](../../reports/pensee-courbe.json) ; code [`courbe.py`](../../tools/pensee/courbe.py) ; T16 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **19/19 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **406 fiches / 506 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Porte qui se referme** : après un pas, la porte se referme ; le moteur doit repasser.
2. **Porte apprise avec le bruit** : entraîner sur la porte stochastique.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque la porte qui se referme.

### Tour 34 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Ajouter la porte qui se referme et la tester
- bash — Ajouter la porte T17 et lancer l'autotest
- bash — Écrire la fiche de la porte qui se referme
- bash — Ajuster la date et passer les portes
- bash — Committer la porte qui se referme
- job_output

**Synthèse produite :**

⏵ Porte qui se referme : 27 nœuds/but, sonde 5, coût 57 ; 20/20

Le round 21 du goal est livré : la **porte qui se referme** derrière le passage ne bloque pas l'A*. Commit **`bcf6c281`**.

\## La porte qui se referme

Même labyrinthe que T11, mais la porte `(3,3)` se **referme** dès qu'on la franchit : l'état `(x, y, open)` passe à `open = False` sur la case `(3,3)`. La politique doit l'ouvrir **avant** de passer ; une fois passée, elle ne peut plus revenir.

| politique | nœuds | pas | saut | sonde | coût | but |
|---|---:|---:|---:|---:|---:|---|
| **manhattan** | **27** | 12 | 10 | **5** | **57** | **oui** |

**Ce que ça dit** :

- **Le moteur gère la fermeture** : l'A* explore la porte, la franchit, la porte se referme, et le but est atteint sans retour.
- **La sonde reste nécessaire** (5 appels) : sans elle, la porte reste fermée.
- **Le coût baisse** (57 contre 58 sur T11) : le chemin est un peu plus court, la porte se refermant derrière.
- **Le vrai piège serait une porte qui se referme avant le passage** : ce banc la referme **après** — c'est la prochaine étape.

\## L'état

- Fiche : [`rapport-pensee-ferme.md`](../../reports/rapport-pensee-ferme.md) ; JSON [`pensee-ferme.json`](../../reports/pensee-ferme.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T17 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **20/20 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **407 fiches / 507 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Porte qui se referme avant le passage** : le moteur doit rouvrir et repasser.
2. **Q-table sur la porte qui se referme** : la politique apprend le nouveau modèle.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque la porte qui se referme **avant** le passage.

### Tour 35 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Ajouter la porte à un tour et la tester
- bash — Ajouter la porte T18 et lancer l'autotest
- bash — Écrire la fiche de la porte à un tour
- bash — Ajuster la date et passer les portes
- bash — Committer la porte à un tour
- job_output

**Synthèse produite :**

⏵ Porte à un tour : 27 nœuds/but, sonde 5, coût 57 ; 21/21

Le round 22 du goal est livré : la **porte à un tour** oblige la sonde à ouvrir **et** passer dans le même pas. Commit **`e2770e7a`**.

\## La porte à un tour

Même labyrinthe que T11, mais l'ouverture de la porte ne dure **qu'un pas** : la `sonde` doit ouvrir la porte **et** franchir la case dans le **même** appel. Un `pas`/`saut` séparé ne voit jamais la porte ouverte.

| politique | nœuds | pas | saut | sonde | coût | but |
|---|---:|---:|---:|---:|---:|---|
| **manhattan** | **27** | 12 | 10 | **5** | **57** | **oui** |

**Ce que ça dit** :

- **L'ouverture d'un tour suffit** : la sonde ouvre et passe dans le même pas ; le but est atteint en 27 nœuds, comme sur la porte stable (T11 : 28) et la porte qui se referme (T17 : 27).
- **Le `pas`/`saut` ne peuvent pas tricher** : ils ne voient jamais la porte ouverte ; seule la sonde franchit.
- **Le coût est stable** (57) : 5 sondes, 7 appels ; la porte minute ne coûte pas plus cher.
- **Le vrai piège serait une porte qui se referme avant le passage et un agent qui doit revenir** ; ce banc laisse l'agent passer directement.

\## L'état

- Fiche : [`rapport-pensee-minute.md`](../../reports/rapport-pensee-minute.md) ; JSON [`pensee-minute.json`](../../reports/pensee-minute.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T18 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **21/21 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **408 fiches / 508 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Q-table sur la porte minute** : la politique apprend l'ouverture-passage.
2. **Fenêtre temporelle** : la porte s'ouvre tous les 3 pas ; le moteur doit attendre.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque la fenêtre temporelle.

### Tour 36 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Ajouter la fenêtre temporelle et la tester
- bash — Tester la fenêtre avec un budget plus grand
- bash — Ajouter la porte T19 (Q-table sur la minute)
- bash — Écrire la fiche de la Q-table sur la porte minute
- bash — Ajuster la date et passer les portes
- bash — Committer la Q-table sur la porte minute
- job_output

**Synthèse produite :**

⏵ Q-table sur la porte minute : 28 nœuds/but, sonde 6, coût 62 ; 22/22

Le round 23 du goal est livré : la **Q-table transfère** à la **porte à un tour** et l'ouvre-passage. Commit **`55b1523c`**.

\## La Q-table sur la porte minute

Même labyrinthe que T18, mais la politique est la `PolitiqueApprise` (200 épisodes, graine 0), entraînée sur la porte **déterministe** T11, au lieu de la règle manhattan. La porte ne s'ouvre qu'un pas ; la sonde ouvre **et** passe.

| politique | nœuds | pas | saut | sonde | coût | but |
|---|---:|---:|---:|---:|---:|---|
| **apprise** | **28** | 13 | 10 | **6** | **62** | **oui** |
| manhattan (T18) | 27 | 12 | 10 | 5 | 57 | oui |

**Ce que ça dit** :

- **La Q-table transfère** à la porte minute : elle vise la porte, la sonde ouvre et passe ; le but est atteint en 28 nœuds.
- **Elle paie +1 nœud et +1 sonde** par rapport à la règle (62 contre 57) : l'apprentissage tabulaire est proche, pas identique.
- **La politique apprise n'a pas été entraînée sur la porte minute** : c'est un **transfert** du déterministe vers la porte à un tour.
- **Le coût reste modeste** (62) : la porte minute ne coûte pas plus cher que la porte stable.

\## L'état

- Fiche : [`rapport-pensee-minute-apprise.md`](../../reports/rapport-pensee-minute-apprise.md) ; JSON [`pensee-minute-apprise.json`](../../reports/pensee-minute-apprise.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T19 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **22/22 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **409 fiches / 509 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **La politique seule sur la porte minute** : sans A*, la Q-table ouvre et passe-t-elle ?
2. **Porte mobile** : la porte change de case ; la politique doit s'adapter.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque la politique seule sur la porte minute.

### Tour 37 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Mesurer la politique seule sur la porte minute
- bash — Ajouter la porte T20 (politique seule/minute)
- bash — Écrire la fiche de la politique seule/minute
- bash — Ajuster la date, le compteur et passer les portes
- bash — Committer la politique seule/minute
- job_output

**Synthèse produite :**

⏵ Politique seule/minute : 9/9 échecs, l'A* nécessaire ; 23/23

Le round 24 du goal est livré : la **politique seule échoue** sur la porte minute — la **négative** est mesurée, l'A* était nécessaire. Commit **`be503e31`**.

\## La politique seule sur la porte minute

La `PolitiqueApprise` (entraînée sur la porte **déterministe**) est exécutée **seule** sur la porte **à un tour** : elle doit ouvrir **et** passer dans le même pas.

| épisodes | graines | buts seuls | pas | A* + sonde (T19) |
|---:|---:|---:|---:|---:|
| 50 | 0,1,2 | **0/3** | 200 | 28 nœuds |
| 100 | 0,1,2 | **0/3** | 200 | 28 nœuds |
| 200 | 0,1,2 | **0/3** | 200 | 28 nœuds |

**Ce que ça dit** :

- **La politique seule échoue** sur la porte minute : la Q-table a appris la porte stable, pas l'ouverture-passage d'un tour.
- **L'A* était nécessaire** : c'est lui qui explore et trouve la séquence ouverture-passage ; la politique seule ne la connaît pas.
- **Le transfert a une limite** : la Q-table transfère à la porte stochastique (T16) mais pas à la porte minute seule ; le **contexte temporel** n'est pas dans sa table.
- **La négative est explicite** : 9/9 échecs, 200 pas ; la porte T20 vérifie l'échec, pas la réussite.

\## L'état

- Fiche : [`rapport-pensee-minute-seule.md`](../../reports/rapport-pensee-minute-seule.md) ; JSON [`pensee-courbe.json`](../../reports/pensee-courbe.json) ; code [`courbe.py`](../../tools/pensee/courbe.py) ; T20 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **23/23 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **410 fiches / 509 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Entraîner sur la porte minute** : la Q-table apprend-elle l'ouverture-passage ?
2. **Porte mobile** : la porte change de case ; la politique doit s'adapter.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round entraîne la Q-table sur la porte minute.

### Tour 38 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Ajouter la Q-table entraînée sur la porte minute
- bash — Ajouter la porte T21 (Q-table entraînée/minute)
- bash — Écrire la fiche de la Q-table entraînée/minute
- bash — Ajuster la date et passer les portes
- bash — Committer la Q-table entraînée/minute
- job_output

**Synthèse produite :**

⏵ Q-table entraînée/minute : 60 états-Q, la politique seule échoue ; 24/24

Le round 25 du goal est livré : même **entraînée sur la porte minute**, la politique seule échoue — la **négative** tient. Commit **`e651ffcb`**.

\## La Q-table entraînée sur la minute

`PolitiqueAppriseMinute` (Q-learning, 200 épisodes, graine 0) apprend l'**ouverture-passage** : à `(3,2)`, l'action `bas` passe directement à `(3,3)` (récompense +0,1). Elle est ensuite exécutée **seule**, sans A*.

| politique | états-Q | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **apprise minute** | **60** | **0** | **8** | 28 nœuds |

**Ce que ça dit** :

- **Même entraînée sur la minute, la politique seule échoue** : la `seule_minute` s'arrête quand la politique ne propose plus d'action ; la Q-table n'a pas la **politique complète**.
- **L'A* reste nécessaire** : c'est lui qui explore et atteint le but (T19) ; la politique seule ne le fait pas, même entraînée.
- **La Q-table apprend l'ouverture-passage** (60 états, +0,1) mais pas la **séquence complète** : la récompense +1 au but est trop rare pour la table.
- **La négative est explicite** : 0 but, 8 pas, 60 états-Q.

\## L'état

- Fiche : [`rapport-pensee-minute-entrainee.md`](../../reports/rapport-pensee-minute-entrainee.md) ; JSON [`pensee-minute-entrainee.json`](../../reports/pensee-minute-entrainee.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T21 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **24/24 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **411 fiches / 510 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Reward shaping** : récompenser l'approche de la porte pour compléter la politique.
2. **Réseau** : une politique paramétrique au lieu de la table.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque le reward shaping.

### Tour 39 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Ajouter le reward shaping et tester la politique seule
- bash — Ajouter la porte T22 (reward shaping)
- bash — Écrire la fiche du reward shaping
- bash — Passer les portes et committer le reward shaping
- job_output

**Synthèse produite :**

⏵ Reward shaping : 56 états-Q, la politique seule échoue encore ; 25/25

Le round 26 du goal est livré : le **reward shaping** ne suffit pas — la **négative** tient. Commit **`28f5d388`**.

\## Le reward shaping

`PolitiqueAppriseShaping` (Q-learning + récompense **dense** : -0,01 par pas, +0,1 par case gagnée vers le but, +0,1 à l'ouverture), 200 épisodes, graine 0, 56 états-Q. Exécutée **seule**, sans A*.

| politique | états-Q | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **apprise shaping** | **56** | **0** | **8** | 28 nœuds |
| apprise minute (T21) | 60 | 0 | 8 | 28 nœuds |

**Ce que ça dit** :

- **Le shaping ne suffit pas** : la politique seule échoue encore en 8 pas ; la Q-table apprend la **distance** mais pas la **séquence complète**.
- **L'A* reste nécessaire** : c'est lui qui explore et atteint le but (T19) ; la politique seule ne le fait pas, même avec une récompense dense.
- **La Q-table reste petite** (56 états) : le shaping ne change pas fondamentalement la table.
- **La négative est explicite** : 0 but, 8 pas, 56 états-Q.

\## L'état

- Fiche : [`rapport-pensee-shaping.md`](../../reports/rapport-pensee-shaping.md) ; JSON [`pensee-shaping.json`](../../reports/pensee-shaping.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T22 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **25/25 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **412 fiches / 511 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Réseau** : une politique paramétrique au lieu de la table, capable de **généraliser**.
2. **Shaping potentiel** : un shaping qui préserve la politique optimale.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque le réseau.

### Tour 40 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Ajouter le réseau linéaire par imitation
- bash — Ajouter _pas au réseau et tester
- bash — Ajouter la porte T23 (réseau linéaire)
- bash — Écrire la fiche du réseau linéaire
- bash — Passer les portes et committer le réseau linéaire
- job_output

**Synthèse produite :**

⏵ Réseau linéaire : 12 poids, l'imitation échoue seule ; 26/26

Le round 27 du goal est livré : le **réseau linéaire** par imitation ne généralise pas la politique du professeur. Commit **`de6dbe0e`**.

\## Le réseau linéaire

Un perceptron `(x/4, y/4, 1) → 4 actions` (**12 poids**) apprend l'action du professeur (la Q-table de la porte minute) sur les 25 états ; il est ensuite exécuté **seul**, sans A*.

| politique | poids | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **réseau linéaire** | **12** | **0** | **200** | 28 nœuds |

**Ce que ça dit** :

- **L'imitation ne suffit pas** : le réseau apprend des **scores** mais pas la **séquence** de la porte minute ; la politique seule échoue.
- **12 poids ne peuvent pas représenter** la politique du professeur (la table a 60 états) : c'est une **sous-capacité**, pas seulement un défaut d'entraînement.
- **L'A* reste nécessaire** : c'est lui qui explore et atteint le but (T19) ; le réseau seul ne le fait pas.
- **La négative est explicite** : 0 but, 200 pas, 12 poids.

\## L'état

- Fiche : [`rapport-pensee-reseau.md`](../../reports/rapport-pensee-reseau.md) ; JSON [`pensee-reseau.json`](../../reports/pensee-reseau.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T23 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **26/26 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **413 fiches / 512 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **MLP** : une couche cachée, plus de capacité, la même imitation.
2. **Distillation** : entraîner sur les **chemins** du professeur, pas seulement les états.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque le MLP.

### Tour 41 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Ajouter le MLP par imitation et tester
- bash — Remplacer le MLP torch par une implémentation pure Python
- bash — Ajouter la porte T24 (MLP)
- bash — Écrire la fiche du MLP
- bash — Passer les portes et committer le MLP
- job_output

**Synthèse produite :**

⏵ MLP : 60 poids, l'imitation échoue encore seule ; 27/27

Le round 28 du goal est livré : le **MLP** (2→8→4) ne suffit pas non plus — l'imitation d'un professeur incomplet hérite de ses limites. Commit **`cd19396b`**.

\## Le MLP

Forward `(x/4, y/4)` → 8 tanh → 4 softmax ; cross-entropy et rétropropagation **manuelles** (pas de torch dans l'environnement), 500 époques, lr 0,10, imitation du professeur (la Q-table de la porte minute) sur les 23 états hors but. Puis exécution **seule**, sans A*.

| politique | poids | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **MLP** | **60** | **0** | **200** | 28 nœuds |
| réseau linéaire (T23) | 12 | 0 | 200 | 28 nœuds |

**Ce que ça dit** :

- **Le MLP échoue encore** : la couche cachée et la rétropropagation ne suffisent pas à reproduire la politique du professeur ; la politique seule tourne.
- **Le professeur est lui-même incomplet** (T21 : la Q-table seule échoue) : l'imitation d'un professeur incomplet ne peut pas dépasser le professeur.
- **L'A* reste nécessaire** : c'est lui qui explore et atteint le but (T19).
- **La négative est explicite** : 0 but, 200 pas, 60 poids.

\## L'état

- Fiche : [`rapport-pensee-mlp.md`](../../reports/rapport-pensee-mlp.md) ; JSON [`pensee-mlp.json`](../../reports/pensee-mlp.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T24 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **27/27 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **414 fiches / 513 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Professeur complet** : d'abord une Q-table qui réussit seule (T21), puis imitation.
2. **Apprentissage par renforcement** : le MLP apprend par essais, pas par imitation.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque le professeur complet.

### Tour 42 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Ajouter le professeur complet et tester
- bash — Ajouter la porte T25 (professeur complet)
- bash — Écrire la fiche du professeur complet
- bash — Passer les portes et committer le professeur complet
- job_output

**Synthèse produite :**

⏵ Professeur complet : 56 états-Q, il échoue encore seul ; 28/28

Le round 29 du goal est livré : même avec le **+1 au but**, le **professeur complet** échoue seul — la politique est **incomplète**. Commit **`8dff8b7f`**.

\## Le professeur complet

`PolitiqueAppriseComplete` — shaping (-0,01/pas + 0,1/case + 0,1/ouverture) **+ 1 au but**, 1000 épisodes, graine 0, 56 états-Q. Exécutée **seule**, sans A*.

| politique | états-Q | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **professeur complet** | **56** | **0** | **8** | 28 nœuds |
| apprise minute (T21) | 60 | 0 | 8 | 28 nœuds |

**Ce que ça dit** :

- **Le professeur complet échoue encore** : la `seule_minute` s'arrête quand la politique ne propose plus d'action ; la Q-table n'a pas la **séquence complète**.
- **+1 au but ne change rien** (56 états) : la récompense rare n'est pas la cause ; c'est la **structure** de la politique (le `propose` renvoie `None` avant le but).
- **L'imitation ne pouvait pas dépasser** ce professeur (T23/T24) ; c'est cohérent.
- **L'A* reste nécessaire** (T19) : c'est lui qui explore et atteint le but.

\## L'état

- Fiche : [`rapport-pensee-professeur.md`](../../reports/rapport-pensee-professeur.md) ; JSON [`pensee-professeur.json`](../../reports/pensee-professeur.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T25 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **28/28 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **415 fiches / 514 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Politique sans `None`** : au pire, une action par défaut (attendre) au lieu de `None`.
2. **Curriculum** : commencer par des états proches du but, puis reculer.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque la politique sans `None`.

### Tour 43 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Faire que le professeur ne renvoie plus None
- bash — Ajouter la porte T26 (politique sans None)
- bash — Écrire la fiche de la politique sans None
- bash — Passer les portes et committer la politique sans None
- job_output

**Synthèse produite :**

⏵ Politique sans None : 56 états-Q, elle tourne 200 pas ; 29/29

Le round 30 du goal est livré : la **politique sans `None`** tourne 200 pas sans atteindre le but — le `None` n'était pas la cause, la politique reste incomplète. Commit **`d0c231ae`**.

\## La politique sans None

Même professeur que T25 (56 états-Q), mais `propose` renvoie **toujours** une action (au but, l'argmax). La `seule_minute` ne s'arrête donc plus au `None` : elle tourne jusqu'au budget.

| politique | états-Q | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **sans None** | **56** | **0** | **200** | 28 nœuds |
| avec None (T25) | 56 | 0 | 8 | 28 nœuds |

**Ce que ça dit** :

- **Le `None` n'était pas la cause** : sans lui, la politique **tourne** (200 pas) au lieu de s'arrêter ; elle n'atteint toujours pas le but.
- **La politique est incomplète** : la Q-table apprend des actions locales, pas la **séquence** de la porte minute.
- **L'A* reste nécessaire** (T19) : c'est lui qui explore et atteint le but.
- **Note de cohérence** : le T25 (l'ancien 8 pas) passe à 200 pas avec ce changement ; sa **négative** (échec) reste vraie.

\## L'état

- Fiche : [`rapport-pensee-sans-none.md`](../../reports/rapport-pensee-sans-none.md) ; JSON [`pensee-sans-none.json`](../../reports/pensee-sans-none.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T26 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **29/29 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **416 fiches / 515 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Curriculum** : commencer par des états proches du but, puis reculer.
2. **Critère d'arrêt** : une politique qui **s'arrête** au but, pas une rustine.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque le curriculum.

### Tour 44 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*35 appels d'outils.* Actions notables :

- bash — Inspecter les méthodes de PolitiqueApprise
- bash — Lire apprendre et _q de PolitiqueApprise
- bash — Tracer le chemin glouton de la politique
- bash — Relire seule_minute
- bash — Corriger la comparaison de seule_minute et re-mesurer
- bash — Voir quelles portes changent après la correction
- bash — Corriger les portes T21/T22/T25/T26 et ajouter T27
- bash — Écrire la fiche de correction et corriger les fiches
- bash — Aligner le compteur et passer toutes les portes
- job_output
- bash — Inspecter le diagramme inline de roadmap.md
- bash — Voir le diff de roadmap et la fin du bloc
- bash — Comprendre la validation des diagrammes inline
- bash — Lire la fonction de validation inline
- … et 16 autres

**Synthèse produite :**

⏵ Correction de mesure : bug de seule_minute, 4 politiques à but/8, 4 fiches corrigées ; 30/30

Le round 31 du goal a trouvé un **bug de mesure** : il invalidait quatre fiches. Il est corrigé. Commit **`0fb426cc`**.

\## Le bug

`seule_minute` comparait un triplet `(x, y, open)` à `P_BUT` (un couple) :

```python
cle = (0, 0, False)          # triplet
if cle == P_BUT:             # (4, 4) contre (4, 4, False) : toujours faux
    return True, pas
```

La comparaison était **toujours fausse** : la fonction rendait « échec » même quand la politique atteignait le but. Les fiches T21, T22, T25, T26 ont conclu « la politique seule échoue » sur cette base.

\## La mesure corrigée

| politique | avant (bug) | après (corrigé) |
|---|---|---|
| minute entraînée (T21) | échec/8 | **but/8** |
| shaping (T22) | échec/8 | **but/8** |
| professeur complet (T25) | échec/8 | **but/8** |
| sans None (T26) | échec/200 | **but/8** |
| stable entraînée (T20, contrôle) | échec/200 | **échec/200** |
| réseau (T23) / MLP (T24) | échec/200 | **échec/200** |

**Ce que ça dit** :

- **Le bug était dans la mesure, pas dans le modèle** : les quatre politiques entraînées sur la porte minute **atteignent le but en 8 pas**, le chemin optimal.
- **Les contrôles tiennent** : la politique entraînée sur la porte **stable**, le réseau et le MLP échouent toujours — la correction ne rend pas tout vrai.
- **Quatre fiches sont corrigées** : T21, T22, T25, T26 portent un avertissement en tête et renvoient à la correction.
- **Une porte est née de la correction** : **T27** vérifie la positive (minute but/8) **et** la négative (stable échec/200) — la comparaison de structures est désormais testée.

\## L'état

- Fiche : [`rapport-pensee-correction.md`](../../reports/rapport-pensee-correction.md) ; JSON [`pensee-correction.json`](../../reports/pensee-correction.json) ; code [`courbe.py`](../../tools/pensee/courbe.py) ; T27 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **30/30 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **418 fiches / 516 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- Note : `verifier_schemas` a échoué deux fois sur le Gantt de `roadmap.md` (rendu PlantUML, 7 s sous charge) puis est passé — flake d'environnement, pas une régression de contenu.

\## La suite


… [455 caractères tronqués]

### Tour 45 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Refactorer les mesures avec trace
- bash — Créer l'audit des mesures seule
- bash — Ajouter la porte T28 (audit)
- bash — Écrire la fiche de l'audit
- job_output
- bash — Passer toutes les portes
- bash — Committer l'audit

**Synthèse produite :**

⏵ Audit des mesures : 15/15 cohérentes, la politique minute ne transfère pas au bruit ; 31/31

Le round 32 du goal est livré : les trois mesures « seule » rendent désormais leur **état final** et leur **chemin**, et l'audit vérifie leur cohérence. Commit **`da55b97d`**.

\## L'audit

`trace_seule`, `trace_seule_sto`, `trace_seule_minute` rendent `(but, pas, état final, chemin)` ; les fonctions publiques n'en gardent que `(but, pas)`. L'audit vérifie `but == (final == P_BUT)` et `pas == len(chemin)` sur **5 politiques × 3 mondes = 15/15**.

| politique | stable | minute | stochastique |
|---|---|---|---|
| **stable** (T16) | but/8 | échec/200 | **but/9 (2 essais)** |
| **minute** (T21) | but/8 | **but/8** | **échec/200** |
| **complete** (T25) | but/8 | but/8 | **échec/200** |
| **reseau** | échec/200 | échec/200 | échec/200 |
| **mlp** | échec/200 | échec/200 | échec/200 |

**Ce que ça dit** :

- **La correction du round 31 est confirmée** : la politique minute atteint le but en 8 pas sur la porte minute ; la stable échoue (contrôle négatif).
- **Le transfert a un trou** : la politique entraînée sur la porte **minute** ne sait pas gérer l'état `open=True` (la porte stochastique ouverte) ; elle tourne (final `[3,0]`). La politique entraînée sur la porte **stable** voit ces états et réussit (9 pas, 2 essais).
- **Les réseaux échouent partout** : l'imitation des Q-tables ne conduit pas (T23/T24).
- **15/15 cohérentes** : la mesure ne ment plus ; le bug de comparaison est mort.

\## L'état

- Fiche : [`rapport-pensee-audit.md`](../../reports/rapport-pensee-audit.md) ; JSON [`pensee-audit.json`](../../reports/pensee-audit.json) ; code [`audit.py`](../../tools/pensee/audit.py) ; T28 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **31/31 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **419 fiches / 517 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Curriculum des états `open`** : entraîner la politique minute sur la porte stochastique ; combler le trou de transfert.
2. **Porte mobile** : la porte change de case ; mesurer la robustesse.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

… [117 caractères tronqués]

### Tour 46 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Ajouter la politique entraînée sur la porte stochastique
- bash — Ajouter la porte T29 (curriculum open)
- job_output
- bash — Écrire la fiche du curriculum open
- bash — Passer toutes les portes
- bash — Committer le curriculum open

**Synthèse produite :**

⏵ Curriculum open : 74 états-Q, bruit but/9 et stable but/8 ; 32/32

Le round 33 du goal est livré : le **trou de transfert** de l'audit est comblé — la politique entraînée sur le bruit apprend les états `open`. Commit **`7367b314`**.

\## Le curriculum

Même labyrinthe que T16-T21, mais la récompense **simule la porte stochastique** à l'entraînement (80 % d'ouverture, sinon l'état reste) : la Q-table voit les états `open=True` et `open=False`. 1000 épisodes, graine 0, **74 états-Q**. Puis exécution **seule**, sans A*.

| politique | états-Q | bruit (seule) | stable (seule) |
|---|---:|---|---|
| **ouverte** | **74** | **but/9 (2 essais)** | **but/8** |
| minute (T21) | 60 | échec/200 | but/8 |

**Ce que ça dit** :

- **Le trou de transfert est comblé** : la politique entraînée sur le bruit réussit seule sur le bruit **et** sur la porte stable ; les deux mondes partagent la structure.
- **Le coût du bruit est faible** : +1 pas et 2 essais sur la porte stochastique, par rapport au chemin optimal (8).
- **La robustesse s'apprend** : ce n'est pas la porte qui change, c'est la **distribution des états** visités à l'entraînement ; le curriculum `open` suffit.
- **La négative reste** : la politique minute (T21/T28) échoue sur le bruit ; le contraste minute vs ouverte est le contrôle.

\## L'état

- Fiche : [`rapport-pensee-ouverte.md`](../../reports/rapport-pensee-ouverte.md) ; JSON [`pensee-ouverte.json`](../../reports/pensee-ouverte.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T29 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **32/32 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **420 fiches / 518 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- Le commit a demandé **5 essais** (courses Git : `index.lock`, HEAD déplacé par 3 commits concurrents).

\## La suite

1. **Plusieurs graines** : la robustesse tient-elle hors graine 0 ?
2. **Porte mobile** : la porte change de case ; le curriculum doit suivre.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round vérifie la robustesse sur plusieurs graines.

### Tour 47 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Mesurer la robustesse sur 5 graines
- bash — Ajouter la porte T30 (5 graines)
- bash — Écrire la fiche de la robustesse sur 5 graines
- bash — Voir la ligne des compteurs
- bash — Aligner les compteurs et passer les portes
- bash — Committer la robustesse sur 5 graines
- job_output

**Synthèse produite :**

⏵ Robustesse sur 5 graines : 5/5 bruits, 5/5 stables, 33/33

Le round 34 du goal est livré : le **curriculum `open`** tient sur **5 graines**. Commit **`efaaa945`**.

\## Les 5 graines

`PolitiqueAppriseOuverte` entraînée (1000 épisodes) sur 5 graines, exécutée seule sur le bruit (même graine) et sur la porte stable.

| graine | états-Q | bruit (seule) | stable (seule) |
|---:|---:|---|---|
| 0 | 74 | but/9 (2 essais) | but/8 |
| 1 | 85 | but/8 (1 essai) | but/8 |
| 2 | 61 | but/10 (3 essais) | but/8 |
| 3 | 85 | but/8 (1 essai) | but/9 |
| 4 | 72 | but/8 (1 essai) | but/8 |

**Ce que ça dit** :

- **5/5 sur le bruit** : le curriculum `open` tient hors graine 0 ; le trou de transfert (T28) est comblé de façon **robuste**.
- **5/5 sur la porte stable** : la politique entraînée sur le bruit **généralise** au monde déterministe (8–9 pas).
- **Le coût du bruit varie** : 1 à 3 essais, 8 à 10 pas ; la Q-table apprend l'ouverture probabiliste, pas un chemin unique.
- **La taille varie** (61–85 états) sans changer le résultat : la structure compte plus que la taille.

\## L'état

- Fiche : [`rapport-pensee-graines.md`](../../reports/rapport-pensee-graines.md) ; JSON [`pensee-graines.json`](../../reports/pensee-graines.json) ; code [`graines.py`](../../tools/pensee/graines.py) ; T30 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **33/33 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **422 fiches / 519 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.
- `sessions.py` : le plan R4.4 `fe3c05f0` reste périmé.

\## La suite

1. **Porte mobile** : la porte change de case ; le curriculum doit suivre.
2. **Bruit variable** : 60 %, 90 % ; mesurer la dégradation.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round attaque la porte mobile.

### Tour 48 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Relire les définitions du labyrinthe à porte
- bash — Lire le labyrinthe à porte
- bash — Ajouter la porte mobile et la tester
- bash — Ajouter la porte T31 (porte mobile)
- bash — Écrire la fiche de la porte mobile
- bash — Trim, compteurs et portes
- bash — Committer la porte mobile
- job_output

**Synthèse produite :**

⏵ Porte mobile : 2 positions, A* 2/2, politique seule but/8, 170 états-Q ; 34/34

Le round 35 du goal est livré : la **porte mobile** (deux positions) est apprise par **une seule politique**. Commit **`bd93762d`**.

\## La porte mobile

Deux labyrinthes jumeaux : la porte est à `(3,3)` (route du haut, par `(3,2)`) ou à `(1,3)` (route de gauche, par `(0,3)`). La case de l'autre porte est **libre**. L'état est `(x, y, open, d)` où `d` est la position de la porte.

| d | A* + sonde | politique seule | états-Q |
|---|---|---:|---:|
| 0 (porte 3,3) | but, 29 nœuds, sonde 5, coût 60 | **but/8** | 170 |
| 1 (porte 1,3) | but, 29 nœuds, sonde 5, coût 59 | **but/8** | 170 |

**Ce que ça dit** :

- **La politique généralise** : une seule Q-table (170 états, `d` dans l'état) réussit aux deux positions ; elle n'apprend pas deux politiques séparées.
- **L'A* aussi** : la sonde ouvre la porte visée, la route est trouvée aux deux positions.
- **Le coût est stable** (59–60) : la porte mobile ne coûte pas plus cher que la porte fixe (57–58).
- **La mobilité est peu coûteuse en états** : 170 états pour deux labyrinthes, contre 56–74 pour un seul ; la structure `d` porte l'information.

\## L'état

- Fiche : [`rapport-pensee-mobile.md`](../../reports/rapport-pensee-mobile.md) ; JSON [`pensee-mobile.json`](../../reports/pensee-mobile.json) ; code [`operateurs.py`](../../tools/pensee/operateurs.py) ; T31 dans [`autotest.py`](../../tools/pensee/autotest.py).
- **34/34 portes** ; `porte-bloc-linguistique` **verte** (gold 360 + tests + 398 langues) ; `revue` **423 fiches / 521 JSON / 118 docs / 81 portes** — ✅ ; `en-cours` 2 sessions, T0 dans le budget.
- Le **vrai modèle neuronal** reste **bloqué** : `llama-cli` refusé, taggers absents, **aucun poids `drave-n0`** pour une politique DRVM réelle.

\## La suite

1. **Plusieurs graines** : la porte mobile tient-elle hors graine 0 ?
2. **Porte qui bouge** : `d` change en cours d'épisode ; l'état doit suivre.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

Le goal `goal-7beacaeb` reste actif jusqu'à **8 h demain** ; le prochain round vérifie la porte mobile sur plusieurs graines.

### Tour 49 — <goal_round> Objective: "Suivre docs/pilotage/plan-travail.md jusqu'au 2026-11-02 08:00 EST (session L/B13) : livrer le  … [1004 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Mesurer la porte mobile sur 5 graines
- bash — Ajouter la porte T32 (mobile 5 graines)
- bash — Écrire la fiche de la porte mobile sur 5 graines
- bash — Passer toutes les portes
- bash — Committer la porte mobile sur 5 graines
- job_output

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/svgkit.py` | 1 | 0 |
| `/tmp/gen_natif.py` | 1 | 0 |
| `/tmp/gen_diehl.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/modele-natif.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/diehl-cook.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md` | 0 | 8 |
| `/tmp/gen_plus.py` | 1 | 0 |
| `/tmp/enrichir.py` | 1 | 0 |
| `/tmp/gen_pensee.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/pensee-iterative.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/moteur-de-pensee.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_corpus.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_export.py` | 1 | 0 |
| `/tmp/gen_heuristique.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/pre-traitement-linguistique.md` | 1 | 0 |
| `/tmp/gen_programme_r.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/programme-r.md` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/bloc-linguistique.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bloc-linguistique.md` | 1 | 0 |

### Sous-agents lancés

- tour 1 — Revue visuelle des 7 schémas
- tour 1 — Test revue visuelle

### Commandes exécutées (échantillon)

- **T1** Lister la structure du dépôt
- **T1** Chercher Diehl/Cook, LIF, STDP dans docs et code
- **T1** Lire la vision
- **T1** Lire contexte et sommaire docs
- **T1** Chercher références Diehl & Cook
- **T1** Lire la méthode illustrations et l'index des schémas
- **T1** Inspecter le moteur drave-core
- **T1** Lire la spec DRVF
- **T1** Lire la synthèse chapitre 7
- **T1** Lire l'archive sur les réseaux impulsionnels
- **T1** Lire le bus et le chemin natif
- **T1** Chercher le principe de séparation
- **T1** Lire le protocole sémantique et la fiche couche/étage
- **T1** Lire fiches RSN et un SVG existant
- **T1** État git et état courant
- **T1** Repérer la ligne N de la roadmap
- **T1** Repérer les fiches natives dans reports
- **T1** Lire le lecteur DRVM
- **T1** Trouver les outils DRVM
- **T1** Inspecter le fixture DRVM
- **T1** Afficher le manifeste du modèle témoin
- **T1** Extraire les paramètres du texte de l'article
- **T1** Lister les fichiers du dépôt de référence
- **T1** Récupérer le code de référence et ses paramètres
- **T1** Lire les paramètres complets du code de référence
- **T1** Lire inhibition et normalisation
- **T1** Lire le générateur de connexions
- **T1** Lire la doctrine des trois niveaux (jeux symboliques)
- **T1** Lire le vérificateur de schémas
- **T1** Lire la revue de documentation et le budget
- **T1** Lire la suite de la revue (classement, navigation)
- **T1** Lire deux SVG existants pour le style
- **T1** Lire la porte des tableaux et le vérificateur d'état
- **T1** Lire le README du moteur et la liste valuée
- **T1** Repérer les mécanismes d'exécution
- **T1** Lire la section N de la roadmap
- **T1** Lire la carte des sujets
- **T1** Lire l'écrivain DRVM
- **T1** Vérifier la date et la règle d'état à jour
- **T1** Voir la modification en cours de l'état
- … et 577 autres

## 4. Mesures et résultats marquants

- **T1** `- **La sparsité ne gagne pas toujours** : le croisement push/pull est mesuré à ~22 % de densité ; en dessous, les`
- **T1** `(9,23–9,96 M), un meilleur écart **4,40 % à 31,63 M / 610 exemples**, une **fenêtre** (3,71 % à 500 pas, 1,29 %`
- **T1** `à 750, −0,49 % à 1 000) et un **négatif à 30 langues**. La capacité ne paie **qu'avec les données**.`
- **T1** `trace creuse (39,9 % d'activité) : 6,04 et 3,04 — deux centièmes de plus, parce que`
- **T1** `99,9997 % des cas (22 échappements sur 8 790 000 mesurés). Trois octets par`
- **T1** `| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |`
- **T1** `| trace dense, 512 jetons | 66 370 408 o | **45 079 930 o (−32,1 %)** |`
- **T1** `| rejeu `--flux-forcer` | 19,3885 | **19,4029 (+0,074 %)** |`
- **T1** `| neurones actifs | 22 008 776 | 21 630 645 (−1,7 % : les valeurs qui s'arrondissent à zéro ne sont pas écrites) |`
- **T1** `| erreur par valeur | nulle | RMS **0,085 %** du max de la liste (max 0,394 %) |`
- **T1** `jetons, 16 par lot, seuil 0,01 : **1,5 ko par jeton au lieu de 3,5** (÷2,3) pour`
- **T1** `f32 dense (3,5 ko par jeton) ; le lot en LISTES est le mode 4 (1,5 ko par jeton,`
- **T1** `- **la langue est lisible partout** dans l'état d'un modèle entraîné (80 à 100 % dès la couche 1, sur 5 modèles`
- **T1** `- **le sens est aligné malgré la langue** : le même article UDHR se retrouve d'une langue à l'autre à **96 %** sur`
- **T1** `les paires bien couvertes, **16 %** sur un échantillon stratifié de 100 langues, et **3,5×** le hasard dans un`
- **T1** `- **la restitution exacte** (même langue, à l'identique) est **parfaite pour un modèle spécialisé** (85 % de`
- **T1** `fragments exacts) et **s'effondre quand il partage 448 langues** (0,6 %) : la capacité ne se partage pas`
- **T1** `- **la hiérarchie des surfaces** : langues **96 %** > dialectes **52-97 %** > styles (traducteurs) **24 %** — et les`
- **T1** `trois sont **lues à 100 %**. *L'étage entrée-sortie n'efface aucune surface : il en aligne le sens.*`
- **T1** `- **le bruit d'entrée est signalable** (fautes et langues mêlées : détection 100 %, AUC 1,00) **mais pas`
- **T1** `- **La langue est un petit paramètre** : **1,33 %** des poids (32 768 au dernier étage), bascule **5 ms**,`
- **T1** `**530 Ko** (mesures 3 et 7). Un module de langue peut donc être **petit** et **chargé à la demande**.`
- **T1** `- **Le partage détruit la restitution** : **85 %** de fragments exacts pour un modèle spécialisé, **4 %** quand il`
- **T1** `- **Mais l'espace sémantique est partagé** : **96 %** de retrieval croisé sur les paires couvertes (mesure 39) ; le`
- **T1** `**Ce que cela autorise** : un **noyau partagé** (le sens, 96 %) + des **modules de surface par langue** (entrée et`
- **T1** `sortie : embeddings, tête, adaptateurs), **routés par segment** et **chargés à la demande** (5 ms / 530 Ko). C'est`
- **T1** `langue contre modèle partagé 448 langues, pour répliquer 85 % → 4 %.`
- **T1** `3. **le style** : il est lisible, mais le sens ne le traverse qu'à 24 % — comment l'augmenter sans perdre le style ?`
- **T1** `de 77-88 µJ à **0,594 µJ**. Résultat : 74,81 % sur ImageNet en 4 pas de temps.`
- **T1** `15 % de spikes non nuls en moyenne. 46 M et 216 M de paramètres, **32,2× moins`
- **T1** `redeviennent des accumulations. Gain : **+1,04 % de précision ET −57,34 %`
- **T1** `| Taux d'activation mesuré | **R̂ ≈ 0,15** (SpikeGPT) | **0,00 % de zéros** sur un LLM dense entraîné |`
- **T1** `| Arithmétique | ET logique + **AC** (accumulation) | MAC (mais décalages+additions validés, 0 DSP sur FPGA) |`
- **T1** `| Énergie par opération | E_AC = 0,9 pJ contre E_MAC = 4,5 pJ (Horowitz) | 8,3 nJ/événement (FPGA, **projeté** : 4,83 G évts/s, limite DDR3) contre 57 nJ (CPU, **mesuré**) — rapport 6,9× |`
- **T1** `qui s'active » reste théorique. À seuil 5 % du max, la densité mesurée tombe à`
- **T1** `**17,9 %** — sous le croisement push/pull de **22 %**`
- **T1** `(2,0 ms à 64 tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192) et ses poids`
- **T1** `| Débit mesuré (CPU, 16 threads) | 5,3 G évts/s | 5,3 G évts/s |`
- **T1** `| Temps par token | 63 ms | **~10 ms** |`
- **T1** `| Débit | 15,8 tok/s | **~100 tok/s** |`
- **T1** `- Les gains annoncés (32×, 57 %) sont **théoriques**, calculés avec`
- **T1** `écart relatif réel (4,40 %) mais **transitoire** : à 1 000 pas, le contrôle repasse, et à 30 langues l'effet se`
- **T1** `- **batch 16, seq 384** : le GPU est à ~95 %, la mémoire à ~15 Go par carte ; le CPU ne fait qu'un fil par`
- **T1** `<text x="450" y="350" text-anchor="middle" font-size="12.5" fill="#334155">B11 : codec 100 % (79/79, 449/449), surface 33/79, natif 59,8 / 40,7. B12 : modules M1–M9.</text>`
- **T1** `4442c64c N2 — L'ÉTAT DE SECTION NE SE DISTINGUE PAS D'UN ÉTAT ÉTRANGER (+0,36 % CONTRE +0,37 %)`
- **T1** `4 sources, **B′** quotas égaux (le manifeste est à **82 % anglais**), **C** curriculum 129`
- **T1** `sur A ; la hiérarchie est écartée deux fois, restent **le curriculum et les données** (41 Mo,`
- **T1** `- **R13 — la tokenisation** : **close**, décision **octets** — BPE 512 +0,39 % (bruit), BPE`
- **T1** `1024 +4,09 %, anglais +4,22/+6,59 % à octets égaux ; fiche`
- **T1** `- **B10.2bis — décodeur** : 3×3 : **11,1** ; capacité 11,8 ; **mots 32,5** ;`
- **T1** `- **B11.10** : **hybride 4/4** — codec **161/161**, ambiguïtés refusées ; **69,3 %** natif ;`
- **T1** `**N2.h2** (distillation, professeur refait, 3 graines) : **2,9935** contre **2,9927** (+0,029 %) ;`
- **T1** `84:[N0/N1] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `85:[N2] lasts 4 days and is 30% complete and is colored in #b26a00`
- **T1** `168:| **N1** | `drave-n0` : 11,47 M, 6 blocs, octets, attention locale, FFN creux, 3 têtes précoces | ✅ | aucune — PPL **3,465** avec pont (**4,080** sans) ; têtes **57,6 / 61,6 / 62,1 %** contre **62`
- **T1** `41:| [`rapport-native-distillation-50k.md`](rapport-native-distillation-50k.md) | **N2.11** — 50 000 pas : PPL **3,082**, plateau ; tête 3 **68,70 %** |`
- **T1** `51:| [`rapport-native-service-rust.md`](rapport-native-service-rust.md) | **N4.3** — service Rust natif avec cache : **611 ms**, 53 octets |`
- **T1** `54:| [`rapport-native-distillation-20k.md`](rapport-native-distillation-20k.md) | **N2.8** — 20 000 pas : PPL **3,123** contre **3,295**, précision **67,96 %**, gap **+0,768** |`
- **T1** `60:| [`rapport-native-cache.md`](rapport-native-cache.md) | **N0.9** — cache KV natif : sortie identique à Python, **592,6 ms**, 53 octets |`
- **T1** `67:| [`rapport-native-distillation-tetes.md`](rapport-native-distillation-tetes.md) | **N2.4** — têtes dans la distillation : PPL **3,295**, pas de gain ; tête 3 **62,98 %** > principale **62,35 %** |`
- **T1** `85:| [`rapport-deepseek.md`](rapport-deepseek.md) | **B9** : DeepSeek pour le langage, 310 prompts, chrF, le natif sur GPU, la transition 9,23–9,96 M, la fenêtre 610/20 (3,71 % à 500 pas) et le négati`
- **T1** `34:In order to understand how the mammalian neocortex is performing computations, two things are necessary; we need to have a good understanding of the available neuronal processing units and mechanis`
- **T1** `45:Here we present a spiking neural network which relies on a combination of biologically plausible mechanisms and which uses unsupervised learning, i.e., the weights of the network learn the structur`
- **T1** `56:We use biologically plausible ranges for almost all of the parameters in our simulations, including time constants of membranes, synapses and learning windows (Jug, 2012 ); the exception is the tim`
- **T1** `79:The input to the network is based on the MNIST dataset which contains 60,000 training examples and 10,000 test examples of 28 28 pixel images of the digits 0 9 (LeCun et al., 1998 ). The input is p`
- **T1** `81:To train the network, we present digits from the MNIST training set (60,000 examples) to the network. Before presenting a new image, there is a 150 ms phase without any input to allow all variables`
- **T1** `87:Additionally to the 100 neuron network, we trained and tested three other networks with 400, 1600, and 6400 excitatory neurons by presenting 3, 7, and 15 times the entire MNIST training set; the fo`
- **T1** `95:The presented network achieves good classification performance on the MNIST benchmark using SNNs with unsupervised learning made of biologically plausible components. A comparison of spiking neural`
- **T1** `170:A network architecture similar to ours is presented in Querlioz et al. ( 2011a , 2013 ) and Bichler et al. ( 2012 ), using the learning rule presented in Querlioz et al. ( 2011b ). The main differ`
- **T1** `178:Intuitively, the function of the network is similar to competitive learning procedures (McClelland et al., 1986 ) like self-organizing maps (Kohonen, 1990 ) or neural-gas (Fritzke, 1995 ), which s`
- **T1** `First run the main file "Diehl&Cook_spiking_MNIST.py" (which by default uses the pretrained weights) and wait until the simulation finished (on recent hardware this should take about 30min). After the`
- **T1** `At first you have to modify the main file "Diehl&Cook_spiking_MNIST.py" by changing line 210 to "test_mode = False" to train the network. The resulting weights will be stored in the subfolder "weights`
- **T1** `<text x="450" y="366" text-anchor="middle" font-size="13" fill="#0f172a">1 608 octets par flux à 256 jetons · 0,25 Mbit/s · latence ≤ 20 ms</text>`
- **T1** `### Tailles d'encodage (bits/poids, densité 99,2 %)`
- **T1** `qui perd la magnitude. Les listes ne gagnent que sous ~20 % de densité : c'est la`
- **T1** `| 0 % | 0 | — | — | **0,049** | **×10** |`
- **T1** `| 1 % | 43 560 | 0,11 G év/s | **0,84** | 0,052 | ×7,5 |`
- **T1** `| 5 % | 217 851 | 0,54 | **2,95** | 0,074 | ×5,5 |`
- **T1** `| 10 % | 433 035 | 1,07 | **4,02** | 0,108 | ×3,8 |`
- **T1** `| 25 % | 1 082 120 | 2,31 | **4,91** | 0,220 | ×2,1 |`
- **T1** `| 50 % | 2 163 317 | 3,76 | **5,51** | 0,392 | ×1,5 |`
- **T1** `| 100 % | 4 325 087 | 5,77 | **5,80** | 0,746 | ×1,0 |`
- **T1** `- **Coût fixe : 0,484 ms → 0,049 ms** grâce au pool persistant (threads et`
- **T1** `**×8,5 en régime creux**, précisément le régime qui nous intéresse.`
- **T1** `- **Le débit varie de ×15** entre densité nulle (0,049 ms) et pleine (0,746 ms) —`
- **T1** `- **Pic : 5,80 G événements/s** (contre 4,66 avant), soit 75 % du banc C de`
- **T1** `À 100 % de densité : bitmap 4,07 G év/s contre **5,80** pour les varints. Le chemin`
- **T1** `| multiplication i8×i8 | 2,5 ms | — |`
- **T1** `| décalages + additions | 110,7 ms | ×44 |`
- **T1** `1. ~~Pool de threads persistant~~ ✅ fait (×10 sur le coût fixe).`
- **T1** `(le plancher de 0,049 ms reste dominé par la réduction des 896 sorties × 16 threads).`
- **T1** `5,8 G év/s ; regrouper les événements d'une même plage de destinations`
- **T1** `| **N1** | `drave-n0` : 11,47 M, 6 blocs, octets, attention locale, FFN creux, 3 têtes précoces | ✅ | aucune — PPL **3,465** avec pont (**4,080** sans) ; têtes **57,6 / 61,6 / 62,1 %** contre **62,7 %`
- **T1** `2. **Le saut de calcul existe, le saut de contenu n'existe pas.** La sortie précoce gagne **24,05 %** de temps en`
- **T1** `| **A7** la grappe déportée | **fait** — relais 42,5477, grappe 21 %, transport 4,22× | [la roadmap](../pilotage/roadmap.md) |`
- **T1** `| **B5/B6** les jeux symboliques | **faits** — 112 items, 100 % au niveau 4, pensée 5/5 | [le concept](jeux-symboliques.md) · [la fiche](../../reports/rapport-jeux-symboliques.md) |`
- **T1** `| **B9** le banc externe | **mesuré** — seuil 9,23–9,96 M, 31,63 M/610 4,40 %, fenêtre, négatif 30 langues | [le concept](../implantation/llm-externe.md) · [la fiche](../../reports/rapport-deepseek.md`
- **T1** `| **B11** la base d'universaux typés | **premier passage** — codec 100 % (79/79, 449/449) ; natif synthétique normalisé 55,7 % (invariance 37,0 %) ; codec + contexte 528/528 (100 %) ; natif contexte s`
- **T1** `| **C3.2e** sous-familles autres | **mesuré** — uralic 46,7→100 %, benue 88 %, austro 60,3 %, afro ouest 53,5 % | [la fiche](../../reports/rapport-sous-familles-autres.md) |`
- **T1** `| **C3.2d** sous-familles IE | **mesuré** — 54,6–100 % ; l'IE à 14,7 % est un effet de composition | [la fiche](../../reports/rapport-ie-sous-familles.md) |`
- **T1** `| **C3.2c** 9 familles | **mesuré** — 7/9 > 30 %, moyenne 69,5 %, contrôle 0 ; indo-européen 14,7 %, uralic 46,7 % | [la fiche](../../reports/rapport-familles-9.md) |`
- **T1** `| **B23** routeur M1→M2 | **partiel** — espaces 41,8 % vs 11,6 % ; typo 56,2 % < M2 68,3 % ; collision de lexique | [la fiche](../../reports/rapport-routeur-m1-m2.md) |`
- **T1** `| **B22** M2 typos | **niche robuste** — M2 62–80 % contre M1 24–45 % sur 4 types de typos | [la fiche](../../reports/rapport-m2-typo.md) |`
- **T1** `| **B17** mémoire LFU | **filtre** — LFU 9,28 % suffixe vs FIFO 5,03 % ; M8 couverture 70,75 %, lookup 100 %, généralisation 0 | [la fiche](../../reports/rapport-pipeline-memoire.md) |`
- **T1** `| **B14** M2 dans la chaîne | **rameau** — M1 100 %, M2 93,4/93,6 %, aucun étage ne consomme M2 ; M5 plateau 18,70 % vs 12,60 % | [la fiche](../../reports/rapport-pipeline-m2.md) |`
- **T1** `| **B15** M1 multilingue | **66 langues** — 528/528 ; 26/26 variantes et 15/15 interlangues invariantes ; contrôle permuté 0/90 % | [la fiche](../../reports/rapport-multilingue.md) |`
- **T1** `| **B13** la chaîne sémantique | **intégration** — M1 528/528 ; M5 contexte 18,7 % vs 12,6 % ; M6 94,3 % ; M8 57,95 % (borne haute) | [la fiche](../../reports/rapport-pipeline-semantique.md) · [le cod`
- **T1** `| **B12** les modules cerveau-langage | **premier passage** — M1 528/528 ; M2 **98,6 / 93,2** (double dissociation) ; M8 **96,48 %** hors stock ; M5/M6/M7 négatifs ; M9 lésions | [les modules](modules`
- **T1** `touche **25 % des activations × 50 % des poids = 12,5 %** des poids par jeton`
- **T1** `(campagne, § 5 ter), alors qu'un pas d'entraînement par gradient en touche **100 %**.`
- **T1** `d'événement, décroissance, forme signée) : gains en échantillon −0,73 % au mieux,`
- **T1** `**transfert nul** sur un autre texte, et **dégradation de 5 à 10 % sur des langues`
- **T1** `**(b) Un signal global, lui, apprend.** La distillation (−13,8 % sur un modèle routé`
- **T1** `à dim 512 ; −0,3 % sur un dense creux) est notre seul mécanisme de crédit, et il`
- **T1** `**(c) Les contraintes dures apprises marchent.** k-WTA à 25 % : le modèle creux fait`
- **T1** `*mieux* que dense, là où le témoin s'effondre (+118 %). Élagage appris à 50 % :`
- **T1** `÷2 lectures, qualité inchangée (+0,3 %). **Le substrat accepte d'apprendre sous`
- **T1** `**(d) Un connectome inné aléatoire coûte 1 % — ATTENTION : sur l'attention seulement, rétracté le 11/10 (+9,4 % pour le modèle entier).** Masque de 25 % des connexions tiré à`
- **T1** `la naissance, jamais modifié : perplexité 5,0472 contre 4,9959, événements **÷4,1**,`
- **T1** `débit **×2,1** (§ 4 bis de `biologie-pour-drave.md`). **La structure peut être`
- … (tronqué)

## 5. Erreurs rencontrées

14 sorties en erreur ou divergentes. Les premières :

- **T6** : === PID 6207    6207 sam oct 31 17:17:42 2026 pts/0       18:36:13 node /home/stephane/.local/share/../bin/dsh --profile dsh-tui === PID 7237    7237 sam oct 31 17:18:50 2026 pts/3       18:35:05 node
- **T8** : -rw-------. 1 stephane stephane 9488 31 oct 18:02 /tmp/svgkit.py [exit code: 2]
- **T8** : [stderr] Traceback (most recent call last):   File "<string>", line 1, in <module>     import cairosvg; cairosvg.svg2png(url='docs/schemas/heuristique-niveaux.svg', write_to='/tmp/heur-niveaux.png', o
- **T11** : /home/stephane/.local/bin/llama-cli Qwen2.5-0.5B-Q4_0.gguf Qwen2.5-0.5B-Q8_0.gguf vision llm porte_mistral.py porte-mistral.sh tokenize_llama tokenize_llama.cpp === llm_externe === [exit code: 2]
- **T12** : COMPILE=0 [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/jeux.py", line 182, in decider     _, m
- **T12** : [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/jeux.py", line 43, in joueur_de     return next(c
- **T12** : ok [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/jeux.py", line 182, in decider     _, meilleur
- **T17** : gold cibles ok 20 phrases, 105 tokens → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold.json [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/s
- **T19** : COMPILE=0 [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/operateurs.py", line 213, in penser    
- **T19** : ok [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/operateurs.py", line 231, in instantane     b[
- **T21** : 35bf5588 DONNÉES — NEUF CORPUS EN TEXTE INTÉGRAL (FR, AR, PT, ZH, JA, IT, RU, ES, DE) : 14,51 M ARTICLES, 59,0 GO, 8 KO 0 === HEAD has ? ===  docs/pilotage/en-cours.md                          | 22 ++
- **T29** : 5853b206 B13 — LA PORTE NEURONALE : BONNE POLITIQUE 28 NŒUDS/58 (SONDE 5), AVEUGLE 200/483 SANS BUT ; 14/14 ok [stderr] Traceback (most recent call last):   File "<stdin>", line 4, in <module>   File 
- **T40** : 28f5d388 B13 — LE REWARD SHAPING : 56 ÉTATS-Q, LA POLITIQUE SEULE ÉCHOUE ENCORE ; 25/25 ok [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "/home/stephane/Data
- **T41** : de6dbe0e B13 — LE RÉSEAU LINÉAIRE : 12 POIDS, L'IMITATION ÉCHOUE SEULE ; 26/26 ok [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "/home/stephane/Data13TB/step

## 6. Commits

- DOCS — LE MODÈLE NATIF ET DIEHL & COOK, 13 SCHÉMAS : LA SÉPARATION À TROIS NIVEAUX" 2>&1 | tail -30; echo "EXIT=${PIPESTATUS[0]}"
- DOCS — DIEHL & COOK : UNITÉS, DÉLAIS ET TRACE DES INHIBITEURS" 2>&1 | tail -12; echo "EXIT=${PIPESTATUS[0]}"
- DOCS — LE MODÈLE NATIF ET DIEHL & COOK ENRICHIS : QUOTIENT, TYPES, NEUTRALITÉ, DÉTERMINISME, BANC, CONFORMITÉ" 2>&1 | tail -12; echo "EXIT=${PIPESTATUS[0]}"
- DOCS — LE COÛT CACHÉ DE LA STDP SYMÉTRIQUE, LA LECTURE D'UN PAS ET LES QUESTIONS OUVERTES" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- DOCS — SEUILS PRÉ-ENREGISTRÉS ET COÛT DE LA STDP : LE RENVERSEMENT" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- DOCS — LE CONTRAT EST L'INVARIANT, LA TECHNOLOGIE EST LA VARIABLE : MODES, GRANULARITÉ, GRAPHE DYNAMIQUE" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- PENSÉE — TOUR 1-2 : LA RSN PLURIELLE ET L'ARBRE D'ÉTATS" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- PENSÉE — TOURS 3-4 : LE CYCLE MULTI-NIVEAUX ET LE PORTEFEUILLE DE STRATÉGIES" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- PENSÉE — TOURS 5-10 : CONTRAT, ANYTIME, MÉTA, MÉMOIRE, MESURE" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- ÉTAT — TROIS SESSIONS, PLAN/AMBITION/STRATÉGIE/OBJECTIF FINAL, ET LE CONTRAT DU MOTEUR" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- ÉTAT — N2.h ET R4.4 CLOSES, PENSÉE v0 ACTIVE : L'ÉTAT SUIT LES MANDATS" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- EXPORT — LA BANQUE VALIDÉE DEVIENT UN CORPUS JSONL (SPANS VÉRIFIÉS)" 2>&1 | tail -5; echo "EXIT=${PIPESTATUS[0]}"
- S — L'EXPORT CORPUS EST BRANCHÉ (14 TESTS) ; R4.4 — LES TROIS RESTES SONT DES LIMITES NOMMÉES" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- S — L'EXPORT CORPUS EST BRANCHÉ (14 TESTS) ; R4.4 — LES TROIS RESTES SONT DES LIMITES NOMMÉES" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- ÉTAT — R4.4 CLOSE PAR SES LIMITES ; S RESTE À L'AUTRE TUI (11 TESTS)" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- ÉTAT — COMPTEUR JSON 459 APRÈS LE CORPUS CONTAMINATION" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- COLORATION — LA COUCHE HEURISTIQUE : CE QUE LE CPU ÉTIQUETTE AVANT LE RÉSEAU" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- R — LA CHARTE DU PROGRAMME : SIX PHASES, TROIS LOIS, CE QUI TIENT ET CE QUI MANQUE" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- ÉTAT — COMPTEUR JSON 467 (CORPUS WIKI)" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- BLOC LINGUISTIQUE — NEUF NIVEAUX, HEURISTIQUE ET NEURONAL, 398 LANGUES À 0,9687" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- B13 — AC-3 ET ALPHA-BÊTA : 8/8 PORTES, 1 495 NŒUDS/296 COUPES CONTRE 18 730" 2>&1 | tail -8; echo "EXIT=${PIPESTATUS[0]}"
- B13 — DRVF THOUGHT : 23 597 OCTETS, 93 ÉVÉNEMENTS, REJEU IDENTIQUE, CORRUPTION REFUSÉE" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- B13 — LE BANC ANYTIME : A* BUT EN 32 NŒUDS, AUC 0,528/0,624 CONTRE 0,246/0,116 À L'ALÉATOIRE" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- L — GOLD v0 : 20 PHRASES, POS 0,924, SYNTAGMES 0,356, PRAGMATIQUE 1,0/1,0/0,95/0,9" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- L — GOLD 180 : POS 0,751 (0,924 RÉEL / 0,725 SYNTH), TÊTE 0,560, PRAGMATIQUE 1,0/1,0/0,99/0,89" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- L — ATTACHEMENT : TOP-1 0,294 / TOP-K 0,338 SUR 68 CIBLES (COUVERTURE 0,338), HASARD 0,015" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- L — ATTACHEMENT PAR TÊTE : COUVERTURE 1,0, TOP-1 0,870, TOP-K 1,0 (SPAN 0,338/0,294)" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- B13 — OPÉRATEURS HÉTÉROGÈNES : 3 GENRES, SONDE 4 APPELS/COÛT 48 VS AVEUGLE 1/33 (11/11)" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- L — LECTURE DOUBLE : TOP-1 TÊTE 0,957 (0,800 RÉEL/1,0 SYNTH), 29 CIBLES AMBIGUËS" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- L — LECTURE DOUBLE : TOP-1 TÊTE 0,957 (0,800 RÉEL/1,0 SYNTH), 29 CIBLES AMBIGUËS" 2>&1 | tail -6; echo "EXIT=${PIPESTATUS[0]}"
- B13 — LE NEURONAL NÉCESSAIRE : CADENAS, SONDE SEULE, AVANT 3 APPELS/BUT, AVEUGLE 20/SANS BUT (12/12)" 2>&1 | tail -5; echo "EXIT=${PIPESTATUS[0]}"
- B13 — LE NEURONAL NÉCESSAIRE : CADENAS, SONDE SEULE, AVANT 3 APPELS/BUT, AVEUGLE 20/SANS BUT (12/12)" 2>&1 | tail -5; echo "EXIT=${PIPESTATUS[0]}"
- B13 — LE NEURONAL NÉCESSAIRE : CADENAS, SONDE SEULE, AVANT 3 APPELS/BUT, AVEUGLE 20/SANS BUT (12/12)" 2>&1 | tail -5; echo "EXIT=${PIPESTATUS[0]}"
- L — GOLD 220 : 60 RÉELS + 160 SYNTHÉTIQUES, POS 0,765 (RÉEL 0,861), TÊTE 0,510" 2>&1 | tail -5; echo "EXIT=${PIPESTATUS[0]}"
- L — GOLD 220 : 60 RÉELS + 160 SYNTHÉTIQUES, POS 0,765 (RÉEL 0,861), TÊTE 0,510" 2>&1 | tail -5; echo "EXIT=${PIPESTATUS[0]}"
- L — GOLD 220 : 60 RÉELS + 160 SYNTHÉTIQUES, POS 0,765 (RÉEL 0,861), TÊTE 0,510" 2>&1 | tail -4; then :; fi   if git log -1 --format='%s' | grep -q "GOLD 220"; t
- L — GOLD 220 : CIBLES DES 60 RÉELS, ATTACHEMENT TÊTE 0,972 (0,929 RÉEL), 36 AMBIGUËS" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "CIBLES DES 60"; th
- L — GOLD 260 : 100 RÉELS + 160 SYNTHÉTIQUES, POS 0,774, TÊTE 0,954 (RÉEL 0,909)" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "GOLD 260"; then echo "C
- L — GOLD 300 : 140 RÉELS + 160 SYNTHÉTIQUES, POS 0,773, TÊTE 0,962 (RÉEL 0,936)" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "GOLD 300"; then echo "C
- L — GOLD 360 : 200 RÉELS + 160 SYNTHÉTIQUES, POS 0,772, TÊTE 0,966 (RÉEL 0,946)" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "GOLD 360"; then echo "C
- B13 — LE LABYRINTHE NON LINÉAIRE : BONNE POLITIQUE 17 NŒUDS/34 (SONDE 2), AVEUGLE 15/24 (SONDE 0) ; 13/13" 2>&1 | tail -3   if git log -1 --format='%s' | grep -
- B13 — LA PORTE NEURONALE : BONNE POLITIQUE 28 NŒUDS/58 (SONDE 5), AVEUGLE 200/483 SANS BUT ; 14/14" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "PORT
- B13 — LA PORTE APPRISE : Q-TABLE 67 ÉTATS, 30 NŒUDS/BUT (SONDE 7), 200 ÉPISODES ; 15/15" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "PORTE APPRISE";
- B13 — LA PORTE APPRISE : Q-TABLE 67 ÉTATS, 30 NŒUDS/BUT (SONDE 7), 200 ÉPISODES ; 15/15" 2>&1 | tail -4; echo "EXIT=${PIPESTATUS[0]}"
- B13 — LA COURBE : 15/15 BUTS (50–800 ÉPISODES × 3 GRAINES), 30 NŒUDS, Q 52–83 ; 16/16" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "LA COURBE"; then 
- B13 — LA POLITIQUE SEULE : 8 PAS, 15/15 BUTS SANS A* ; 17/17" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "POLITIQUE SEULE"; then echo "COMMIT OK $i"
- B13 — LA PORTE STOCHASTIQUE : 80 %, 30 NŒUDS/BUT, SONDE 7 ; 18/18" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "PORTE STOCHASTIQUE"; then echo "COMMI
- B13 — LA POLITIQUE SEULE SUR LE BRUIT : 8–10 PAS, 1–3 ESSAIS, 15/15 BUTS ; 19/19" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "SUR LE BRUIT"; then ec
- B13 — LA PORTE QUI SE REFERME : 27 NŒUDS/BUT, SONDE 5, COÛT 57 ; 20/20" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "SE REFERME"; then echo "COMMIT O
- B13 — LA PORTE À UN TOUR : 27 NŒUDS/BUT, SONDE 5, COÛT 57 ; 21/21" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "UN TOUR"; then echo "COMMIT OK $i"; b
- B13 — LA Q-TABLE SUR LA PORTE MINUTE : 28 NŒUDS/BUT, SONDE 6, COÛT 62 ; 22/22" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "Q-TABLE SUR LA PORTE"; th
- B13 — LA POLITIQUE SEULE SUR LA PORTE MINUTE : 9/9 ÉCHECS, L'A* ÉTAIT NÉCESSAIRE ; 23/23" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "MINUTE : 9/9";
- B13 — LA Q-TABLE ENTRAÎNÉE/MINUTE : 60 ÉTATS-Q, LA POLITIQUE SEULE ÉCHOUE ; 24/24" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "ENTRAÎNÉE/MINUTE"; th
- B13 — LE REWARD SHAPING : 56 ÉTATS-Q, LA POLITIQUE SEULE ÉCHOUE ENCORE ; 25/25" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "REWARD SHAPING"; then ec
- B13 — LE RÉSEAU LINÉAIRE : 12 POIDS, L'IMITATION ÉCHOUE SEULE ; 26/26" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "RÉSEAU LINÉAIRE"; then echo "COMM
- B13 — LE MLP : 60 POIDS, L'IMITATION ÉCHOUE ENCORE SEULE ; 27/27" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "LE MLP"; then echo "COMMIT OK $i"; bre
- B13 — LE PROFESSEUR COMPLET : 56 ÉTATS-Q, IL ÉCHOUE ENCORE SEUL ; 28/28" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "PROFESSEUR COMPLET"; then echo 
- B13 — LA POLITIQUE SANS NONE : 56 ÉTATS-Q, ELLE TOURNE 200 PAS ; 29/29" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "SANS NONE"; then echo "COMMIT OK
- B13 — LA MESURE CORRIGÉE : BUG DE seule_minute, 4 POLITIQUES À BUT/8, 4 FICHES CORRIGÉES ; 30/30" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "MESURE
- B13 — LA MESURE CORRIGÉE : BUG DE seule_minute, 4 POLITIQUES À BUT/8, 4 FICHES CORRIGÉES ; 30/30" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "MESURE
- B13 — L'AUDIT DES MESURES : 15/15 COHÉRENTES, LA MINUTE NE TRANSFÈRE PAS AU BRUIT ; 31/31" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "AUDIT DES MES
- B13 — LE CURRICULUM OPEN : 74 ÉTATS-Q, BRUIT BUT/9 ET STABLE BUT/8 ; 32/32" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "CURRICULUM OPEN"; then echo 
- B13 — LA ROBUSTESSE SUR 5 GRAINES : 5/5 BRUITS, 5/5 STABLES ; 33/33" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "5 GRAINES"; then echo "COMMIT OK $i
- B13 — LA PORTE MOBILE : 2 POSITIONS, A* 2/2, POLITIQUE SEULE BUT/8, 170 ÉTATS-Q ; 34/34" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "PORTE MOBILE"; 
- B13 — LA PORTE MOBILE SUR 5 GRAINES : 5/5 D0, 5/5 D1, 147–184 ÉTATS-Q ; 35/35" 2>&1 | tail -3   if git log -1 --format='%s' | grep -q "MOBILE SUR 5 GRAINES"; th


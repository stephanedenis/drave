# Session e181ce02 — Documentation Drave avec diagrammes et implémentation

> **Journaux :** [le jour](../../2026-10-31/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `e181ce02-cd50-488a-a6be-e84b79d40dcc` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-31 17:40 |
| Durée | 25.9 h |
| Tours | 13 |
| Messages | 423 |
| Appels d'outils | 458 |
| Fichiers touchés | 25 |
| Commandes | 359 |
| Sous-agents | 2 |
| Commits | 22 |
| Compactages de contexte | 1 |

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

*8 appels d'outils.* Actions notables :

- create_goal
- bash — Lire le contrat DRVF thought et les types de trace
- bash — Écrire et tester le codec DRVF thought
- bash — Ajouter la porte DRVF et l'exécuter
- bash — Écrire la fiche DRVF et mettre l'état à jour
- bash — Vérifier les compteurs et les portes après le DRVF
- bash — Aligner les compteurs de la fiche DRVF
- bash — Committer le profil DRVF thought

**Synthèse produite :**

⏵ B13 suite : j'encode la trace en DRVF `thought`, avec rejeu et diff vérifiés

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
- … et 319 autres

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

7 sorties en erreur ou divergentes. Les premières :

- **T6** : === PID 6207    6207 sam oct 31 17:17:42 2026 pts/0       18:36:13 node /home/stephane/.local/share/../bin/dsh --profile dsh-tui === PID 7237    7237 sam oct 31 17:18:50 2026 pts/3       18:35:05 node
- **T8** : -rw-------. 1 stephane stephane 9488 31 oct 18:02 /tmp/svgkit.py [exit code: 2]
- **T8** : [stderr] Traceback (most recent call last):   File "<string>", line 1, in <module>     import cairosvg; cairosvg.svg2png(url='docs/schemas/heuristique-niveaux.svg', write_to='/tmp/heur-niveaux.png', o
- **T11** : /home/stephane/.local/bin/llama-cli Qwen2.5-0.5B-Q4_0.gguf Qwen2.5-0.5B-Q8_0.gguf vision llm porte_mistral.py porte-mistral.sh tokenize_llama tokenize_llama.cpp === llm_externe === [exit code: 2]
- **T12** : COMPILE=0 [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/jeux.py", line 182, in decider     _, m
- **T12** : [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/jeux.py", line 43, in joueur_de     return next(c
- **T12** : ok [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/jeux.py", line 182, in decider     _, meilleur

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


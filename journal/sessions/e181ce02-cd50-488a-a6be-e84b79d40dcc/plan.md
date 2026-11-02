# Plan de session — Pensée, la RSN plurielle et le moteur N3

> **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
> synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.

- **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
- **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
- **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
- **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
  `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
  `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`,
  `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`,
  `tools/porte-bloc-linguistique.sh`, `tools/tests/linguistique/`,
  `docs/implantation/bloc-linguistique.md`, `docs/schemas/bloc-linguistique-*.svg`,
  `reports/bloc-*`, `journal/sessions/e181ce02-…/`
- **Heartbeat** : 2026-11-02 01:55 EST
- **Prochaine action** : le bloc linguistique v0 est livré (398 langues) et **AC-3/alpha-bêta**
  sont mesurés (8/8), le DRVF (9/9) et le banc (10/10) ; qualifier un gold et un modèle neuronal ; puis les **opérateurs hétérogènes/DRVM**
  (S reste à l'autre TUI).
- **État** : actif
- **Plan** : 1) ~~RSN plurielle, arbre d'états, cycle multi-niveaux~~ ; 2) ~~portefeuille de
  stratégies, contrat, anytime~~ ; 3) ~~state store v0 (6/6 portes T0–T4)~~ ; 4) ~~moteur v0
  (BFS, greedy, A*, MCTS-lite)~~ ; 5) ~~AC-3, alpha-bêta~~ (**8/8**) ; ~~DRVF~~ (**9/9**) ; 6) **banc anytime** (AUC,
  regret, justification, rejeu) et intégration DRVM/DRVF ; 9) **bloc linguistique** (R0.7).
- **Ambition** : faire de Drave un **runtime cognitif** où penser est une **recherche tracée** sur
  des **états pluriels**, avec des opérateurs hétérogènes (neuronaux, classiques, matériel) et des
  décisions justifiables et rejouables.
- **Stratégie** : théorie d'abord, puis un **v0 petit et mesuré** (un store, trois stratégies, un
  jeu jouet) avant toute généralisation ; réserver les fichiers ; livrer des schémas, des traces
  et des portes ; ne pas toucher aux GPU de N2 ; ne pas modifier `en-cours` sans prévenir.
- **Reprise** : **R4.4** — les trois restes sont des **limites nommées**, pas des tâches ouvertes ;
  **S** est actif dans une autre TUI (export pragmatique, 11 tests), je n'y touche pas.
- **Coloration** : analyse `docs/theorie/pre-traitement-linguistique.md` (5 schémas) — le CPU
  étiquette la surface et énumère le plausible, le réseau tranche l'ambiguïté ; la cascade se
  juge sur la couverture × la précision par unité de calcul, pas sur le débit.
- **Bloc linguistique** : **R0.7** — le contrat `bloc_linguistique.py` (9 niveaux, heuristique
  CPU + neuronal de contrat, parallèle/cascade, activation 51–76 %) ; **398 langues à 0,9687**,
  script **1,0000**, profils permutés **0,0022** ; le modèle réel local n'est pas qualifié ;
  fiche [`bloc`](../../reports/rapport-bloc-linguistique.md) et porte.
- **Moteur B13** : **AC-3, alpha-bêta (8/8)**, **DRVF `thought` (9/9)**, **banc anytime
  (10/10)** ; A* 32 nœuds, AUC 0,528/0,624 contre 0,246/0,116 à l'aléatoire ; fiches
  [`pensee-ac3-alphabeta`](../../reports/rapport-pensee-ac3-alphabeta.md),
  [`pensee-drvf`](../../reports/rapport-pensee-drvf.md),
  [`pensee-banc`](../../reports/rapport-pensee-banc.md) ; prochain : **opérateurs hétérogènes/DRVM**.
- **Gold L 360** : **20 réels + 160 synthétiques** ; POS **0,751**, syntagmes exacts **0,194**/
  **tête 0,560**, pragmatique **1,0/1,0/0,994/0,889** ; cascade (mock) **67,1 %** ;
  **attachement tête 1,0/0,966/0,932** (span 0,323/0,338 ; 29 ambiguës), hasard 0,015 ; vrai neuronal **refusé** ;
  fiche [`pensee-gold`](../../reports/rapport-pensee-gold-linguistique.md) ; prochain :
  **lecture du gold + modèle qualifié**.
- **Objectif final** : un **moteur de pensée v0 exécutable** — state store typé, arbre d'états,
  A*/MCTS/AC-3 sur le même contrat, trace/rejeu, banc anytime avec contrôles — documenté, mesuré
  et committé.

> **Interfaces pour les autres sessions.** `State` = candidats + frontière + empreinte ; `Proposal`
> = transition candidate ; `Score`, `Decision`, `Trace`. Un opérateur est un bloc `state → state`
> ou `state → proposal` ; le store est un bloc `state ↔ store`. Une autre session peut proposer un
> opérateur (neuronal ou classique) sans toucher au moteur : elle implémente le contrat, elle rend
> une trace, et le moteur la traite comme les autres.

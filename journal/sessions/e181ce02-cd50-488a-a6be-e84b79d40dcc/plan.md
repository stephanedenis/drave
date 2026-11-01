# Plan de session — Pensée, la RSN plurielle et le moteur N3

> **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
> synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.

- **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
- **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3
- **Périmètre** : Pensée
- **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
  `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
  `journal/sessions/e181ce02-…/`
- **Heartbeat** : 2026-11-01 10:55 EST
- **Prochaine action** : AC-3, alpha-bêta, l'intégration DRVF et le banc anytime — le state store
  v0 et ses six portes sont committés (`a20de579`).
- **État** : actif
- **Plan** : 1) ~~RSN plurielle, arbre d'états, cycle multi-niveaux~~ ; 2) ~~portefeuille de
  stratégies, contrat, anytime~~ ; 3) ~~state store v0 (6/6 portes T0–T4)~~ ; 4) ~~moteur v0
  (BFS, greedy, A*, MCTS-lite)~~ ; 5) **AC-3, alpha-bêta, DRVF** ; 6) **banc anytime** (AUC,
  regret, justification, rejeu) et intégration DRVM/DRVF.
- **Ambition** : faire de Drave un **runtime cognitif** où penser est une **recherche tracée** sur
  des **états pluriels**, avec des opérateurs hétérogènes (neuronaux, classiques, matériel) et des
  décisions justifiables et rejouables.
- **Stratégie** : théorie d'abord, puis un **v0 petit et mesuré** (un store, trois stratégies, un
  jeu jouet) avant toute généralisation ; réserver les fichiers ; livrer des schémas, des traces
  et des portes ; ne pas toucher aux GPU de N2 ; ne pas modifier `en-cours` sans prévenir.
- **Objectif final** : un **moteur de pensée v0 exécutable** — state store typé, arbre d'états,
  A*/MCTS/AC-3 sur le même contrat, trace/rejeu, banc anytime avec contrôles — documenté, mesuré
  et committé.

> **Interfaces pour les autres sessions.** `State` = candidats + frontière + empreinte ; `Proposal`
> = transition candidate ; `Score`, `Decision`, `Trace`. Un opérateur est un bloc `state → state`
> ou `state → proposal` ; le store est un bloc `state ↔ store`. Une autre session peut proposer un
> opérateur (neuronal ou classique) sans toucher au moteur : elle implémente le contrat, elle rend
> une trace, et le moteur la traite comme les autres.

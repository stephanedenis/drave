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
- **Heartbeat** : 2026-11-05 10:45 EST
- **Prochaine action** : les **22 échecs** d'attachement (verbes hors lexique, noms cibles) ; puis **documenter la convention** des cibles ; les **REL/SUB** (81 spans) sont chez S.
  200+** ; la porte stochastique/fenêtre attend une version API (serveur local interdit).
- **Arrêt** : 2026-11-02 15 h 06 (reboot) — reprise à **16 h 16** ; **actif** ; heartbeat rafraîchi.
- **État** : actif
- **Reprise** : le 04/11 10 h 14 ; quatre modes, élision 144/144.
- **Plan** : 1) ~~RSN plurielle, arbre d'états, cycle multi-niveaux~~ ; 2) ~~portefeuille de
  stratégies, contrat, anytime~~ ; 3) ~~state store v0 (6/6 portes T0–T4)~~ ; 4) ~~moteur v0
  (BFS, greedy, A*, MCTS-lite)~~ ; 5) ~~AC-3, alpha-bêta~~ (**8/8**) ; ~~DRVF~~ (**9/9**) ; 6) **banc anytime** (AUC,
  regret, justification, rejeu) et intégration DRVM/DRVF ; 9) ~~bloc linguistique~~ (R0.7, 398 langues) ; 10) ~~coréférence et absences~~ (140/140, gold 432) ; 11) ~~gold neuronal~~ (tagger 7B local, cascade POS 0,9440) ; 12) ~~syntagmes~~ (BIO 7B, exact 0,6173, tête 0,7606) ; 13) ~~cascade complète~~ (POS 0,9415, syntagmes 0,7539, acte 1,0) ; 14) ~~DRVM/native~~ (cadenas 3 nœuds avec règle, minimal 0 ; porte 27 nœuds avec règle) ; 15) ~~porte DRVM~~ (27 nœuds, 4 sonde) ; 16) ~~pragmatique neuronale~~ (négatif : dev 1,0, test 0,6375) ; 17) ~~porte B13~~ (134/140 : 6 S fixés + 2 test périmé ; le 140/140 ne se rejoue pas) ; 18) ~~porte minute~~ (26 nœuds, 4 sonde ; le labyrinthe échoue) ; 19) ~~porte mobile~~ (2/2 mais l'aveugle/labyrinthe passent ; test faible) ; 20) ~~porte B13 138~~ (6 S fixés ; T132/T133 restent).
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
  script **1,0000**, profils permutés **0,0022** ; les **taggers 7B** locaux sont qualifiés — POS
  (cascade **0,9440**), **syntagmes** (tête **0,7606**) et **cascade complète** (**0,9415 / 0,7539**,
  acte **1,0**) ; la **pragmatique neuronale** est mesurée (dev 1,0, test 0,6375 ; l'heuristique garde) ; restent **gold 200+** et **porte B13** ;
  fiche [`bloc`](../../reports/rapport-bloc-linguistique.md) et porte.
- **Moteur B13** : **AC-3, alpha-bêta (8/8)**, **DRVF `thought` (9/9)**, **banc anytime
  (10/10)**, **140/140** (T137 : 5 phrases sans antécédent, 0 lien ; 116 liens = 51 intra + 65 inter) ;
  A* 32 nœuds, AUC 0,528/0,624 contre 0,246/0,116 à l'aléatoire ; fiches
  [`pensee-ac3-alphabeta`](../../reports/rapport-pensee-ac3-alphabeta.md),
  [`pensee-drvf`](../../reports/rapport-pensee-drvf.md),
  [`pensee-banc`](../../reports/rapport-pensee-banc.md) ; fait : **politique DRVM/native** (`PolitiqueLLM` — cadenas 3 nœuds avec règle, porte 27 nœuds avec la règle, 200 sans) ; **pragmatique neuronale** mesurée (négatif : dev 1,0, test 0,6375) ; **porte B13** **134/140** (6 S fixés + 2 test périmé) ; **porte minute** **26 nœuds** (4 sonde) ; **porte mobile** **test faible** (2/2, l'aveugle/labyrinthe passent) ; **porte B13** **138/140** (6 S fixés ; T132/T133) ; prochain : **porte stochastique/fenêtre** et **gold 200+**.
- **Gold L** : **432 réels + 160 synthétiques + 20** ; POS **0,765**, syntagmes exacts **0,194**/
  **tête 0,560**, pragmatique **1,0/1,0/0,994/0,889** ; cascade (mock) **67,1 %** ;
  **attachement tête 1,0/0,966/0,932** (span 0,323/0,338 ; 29 ambiguës), hasard 0,015 ; **taggers
  7B locaux** — POS **0,8483**, cascade **0,9440** ; **syntagmes** **0,6173**, tête
  **0,7606**, cascade confiance **0,7592** ; **cascade complète** **0,9415 / 0,7539 / 1,0** ;
  fiches [`pensee-gold`](../../reports/rapport-pensee-gold-linguistique.md),
  [`pensee-gold-neuronal`](../../reports/rapport-pensee-gold-neuronal.md) et
  [`pensee-gold-syntagmes`](../../reports/rapport-pensee-gold-syntagmes.md) ; prochain :
  **gold 200+** et **porte B13** ; la coréférence est faite (116 liens).
- **Objectif final** : un **moteur de pensée v0 exécutable** — state store typé, arbre d'états,
  A*/MCTS/AC-3 sur le même contrat, trace/rejeu, banc anytime avec contrôles — documenté, mesuré
  et committé.

> **Interfaces pour les autres sessions.** `State` = candidats + frontière + empreinte ; `Proposal`
> = transition candidate ; `Score`, `Decision`, `Trace`. Un opérateur est un bloc `state → state`
> ou `state → proposal` ; le store est un bloc `state ↔ store`. Une autre session peut proposer un
> opérateur (neuronal ou classique) sans toucher au moteur : elle implémente le contrat, elle rend
> une trace, et le moteur la traite comme les autres.

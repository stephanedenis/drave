"""pensee — le moteur de pensée v0 : state store typé, arbre hashé, stratégies, trace.

Contrat : [`docs/implantation/moteur-de-pensee.md`](../../docs/implantation/moteur-de-pensee.md).
Théorie : [`docs/theorie/pensee-iterative.md`](../../docs/theorie/pensee-iterative.md).

    from tools.pensee.cruches import CRUCHES
    from tools.pensee.moteur import Moteur, AStar
    from tools.pensee.store import Budget
    decision = Moteur().boucle(CRUCHES, AStar(), Budget(200))
"""
from .coeur import Candidat, Decision, Etat, canonique, h
from .moteur import AStar, BFS, Greedy, MCTSLite, Moteur, Probleme, Proposition, Strategie
from .store import Budget, Store, Trace, diff, justification_valide, replay

__all__ = ["Candidat", "Etat", "Decision", "canonique", "h", "Store", "Budget", "Trace",
           "replay", "diff", "justification_valide", "Moteur", "Probleme", "Proposition",
           "Strategie", "BFS", "Greedy", "AStar", "MCTSLite"]

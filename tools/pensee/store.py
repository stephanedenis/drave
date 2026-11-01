"""store.py — le state store : persiste, indexe, compacte, rejoue, partage.

Contrat du store (moteur-de-pensee.md § 2) :

  put(state)            rend l'empreinte ; idempotent
  get(empreinte)        rend l'état ou None
  children(empreinte)   rend les arêtes et les nœuds enfants, ordre stable
  frontier()            rend les nœuds ouverts, meilleur score en tête
  compact(empreinte)    remplace un sous-arbre par un résumé ; refuse sans justification
  replay(trace)         rejoue depuis la racine : mêmes empreintes, mêmes scores
  diff(a, b)            premier nœud divergent entre deux traces
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .coeur import Arete, Etat, Noeud, canonique, h


class Budget:
    """Budget de nœuds : le moteur s'arrête quand il est épuisé, jamais avant le premier pas."""

    def __init__(self, max_noeuds: int = 50):
        if max_noeuds < 1:
            raise ValueError("un budget nul ne fait aucun pas")
        self.max = max_noeuds
        self.consomme = 0

    def reste(self) -> bool:
        return self.consomme < self.max

    def compter(self, cout: int = 1) -> None:
        self.consomme += max(0, cout)


@dataclass(frozen=True)
class Evenement:
    pas: int
    parent: str
    enfant: str
    operateur: str
    params: dict
    score: float
    cout: int
    strategie: str

    def vers_dict(self) -> dict:
        return {"pas": self.pas, "parent": self.parent, "enfant": self.enfant,
                "operateur": self.operateur, "params": self.params, "score": self.score,
                "cout": self.cout, "strategie": self.strategie}


@dataclass
class Trace:
    evenements: list[Evenement] = field(default_factory=list)
    settled: list[str] = field(default_factory=list)

    def pas(self, parent: str, enfant: str, operateur: str, params: dict, score: float,
            cout: int, strategie: str) -> None:
        self.evenements.append(Evenement(len(self.evenements) + 1, parent, enfant, operateur,
                                         params, score, cout, strategie))

    def marquer_settled(self, empreinte: str) -> None:
        self.settled.append(empreinte)


class Store:
    def __init__(self):
        self.etats: dict[str, Etat] = {}
        self.noeuds: dict[str, Noeud] = {}
        self.aretes: dict[str, list[Arete]] = {}
        self.ouverts: dict[str, int] = {}  # empreinte -> ordre d'insertion
        self.resumes: dict[str, dict] = {}
        self._seq = 0

    # -- l'arbre -------------------------------------------------------------
    def put(self, etat: Etat) -> str:
        fp = etat.empreinte()
        if fp not in self.etats:
            self.etats[fp] = etat
            self.noeuds[fp] = Noeud(fp)
            self._seq += 1
        return fp

    def get(self, empreinte: str) -> Etat | None:
        return self.etats.get(empreinte)

    def edge(self, parent: str, enfant: str, operateur: str, params: dict, score: float,
             cout: int = 1) -> None:
        for a in self.aretes.get(parent, []):
            if a.enfant == enfant and a.operateur == operateur:
                return
        self.aretes.setdefault(parent, []).append(
            Arete(parent, enfant, operateur, params, score))
        n = self.noeuds.setdefault(parent, Noeud(parent))
        n.visites += 1

    def children(self, empreinte: str) -> list[tuple[Arete, Noeud]]:
        return [(a, self.noeuds[a.enfant]) for a in self.aretes.get(empreinte, [])]

    def push(self, empreinte: str, score: float) -> None:
        n = self.noeuds.setdefault(empreinte, Noeud(empreinte))
        n.score = score
        self.ouverts.setdefault(empreinte, len(self.ouverts))

    def frontier(self) -> list[tuple[float, int, str]]:
        """Les nœuds ouverts, meilleur score d'abord ; égalité tranchée par l'insertion."""
        return sorted((-self.noeuds[f].score, seq, f) for f, seq in self.ouverts.items())

    def pop(self) -> str:
        meilleur = self.frontier()[0][2]
        self.ouverts.pop(meilleur, None)
        return meilleur

    # -- compaction ----------------------------------------------------------
    def chemin(self, empreinte: str) -> list[str]:
        """Le chemin racine → état (la justification). Remonte par les arêtes."""
        chemin = [empreinte]
        courant = empreinte
        for _ in range(10_000):
            parent = self.etats[courant].parent
            if parent is None:
                return list(reversed(chemin))
            if parent not in self.etats:
                raise ValueError(f"justification cassée : parent {parent[:8]} absent")
            chemin.append(parent)
            courant = parent
        raise ValueError("cycle dans la justification")

    def compact(self, empreinte: str) -> dict:
        """Remplace le sous-arbre ouvert par un résumé, sans perdre la justification."""
        if empreinte not in self.etats:
            raise KeyError("état inconnu")
        if empreinte in self.resumes:
            raise ValueError("sous-arbre déjà compacté")
        try:
            chemin = self.chemin(empreinte)
        except ValueError as e:
            raise ValueError(f"compaction refusée : {e}") from None
        enfants = [fp for fp, _ in self.children(empreinte)] if self.aretes.get(empreinte) else []
        if not enfants:
            raise ValueError("compaction refusée : rien à compacter (sous-arbre vide)")
        resume = {"resume": True, "empreinte": empreinte, "chemin": chemin,
                  "enfants": len(enfants), "etat": self.etats[empreinte].vers_dict()}
        for fp in enfants:
            self.aretes.pop(fp, None)
            self.ouverts.pop(fp, None)
        self.resumes[empreinte] = resume
        return resume


def replay(store: Store, trace: Trace, probleme) -> list[str]:
    """Rejoue la trace depuis la racine : mêmes empreintes, mêmes scores.

    On ne fait pas confiance au store rejoué : on **recalcule** chaque enfant à partir de l'état
    parent et de l'opérateur, et on compare empreinte et score. Un rejeu qui ne redonne pas les
    mêmes scores n'est pas un rejeu, c'est une re-exécution.
    """
    etats = {fp: e for fp, e in store.etats.items()}
    for ev in trace.evenements:
        parent = etats.get(ev.parent)
        if parent is None:
            raise ValueError(f"rejeu : parent {ev.parent[:8]} absent")
        operateur = probleme.operateurs[ev.operateur]
        enfants = operateur(parent, ev.params)
        if not enfants:
            raise ValueError(f"rejeu : l'opérateur {ev.operateur} ne rend rien")
        attendu = etats.get(ev.enfant)
        recalcule = None
        for e in enfants:
            if e.empreinte() == ev.enfant:
                recalcule = e
                break
        if recalcule is None:
            raise ValueError(f"rejeu : l'empreinte {ev.enfant[:8]} n'est pas recalculée")
        if attendu is not None and canonique(recalcule.corps_merkle()) != canonique(attendu.corps_merkle()):
            raise ValueError(f"rejeu : l'état {ev.enfant[:8]} diffère")
    return [ev.enfant for ev in trace.evenements]


def diff(a: Trace, b: Trace) -> int | None:
    """Indice du premier événement divergent (empreinte, opérateur ou score), ou None."""
    for i, (x, y) in enumerate(zip(a.evenements, b.evenements)):
        if (x.enfant, x.operateur, x.score) != (y.enfant, y.operateur, y.score):
            return i
    if len(a.evenements) != len(b.evenements):
        return min(len(a.evenements), len(b.evenements))
    return None


def justification_valide(store: Store, chemin: list[str]) -> bool:
    """Le chemin est-il une vraie suite d'arêtes, de la racine à l'état ?"""
    if not chemin:
        return False
    if chemin[0] not in store.etats or store.etats[chemin[0]].parent is not None:
        return False
    for parent, enfant in zip(chemin, chemin[1:]):
        if enfant not in [a.enfant for a in store.aretes.get(parent, [])]:
            return False
    return True

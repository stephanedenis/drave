"""csp.py — AC-3 : la propagation de contraintes, branchée sur la boucle du moteur.

Le problème est un **CSP** : des variables, des domaines finis, des contraintes binaires. Un
état du moteur porte les **domaines courants** ; l'opérateur `retirer` enlève une valeur ; la
stratégie `AC3` tient la file des arcs, révise et empile les voisins. Le point fixe est
**arc-consistant** ; il n'est pas toujours une solution — `resoudre` fait le backtracking, et le
test vérifie que le CSP réduit a bien une solution.

    from tools.pensee.csp import CARTE_AUSTRALIE, AC3, probleme_csp, resoudre
    d = Moteur().boucle(probleme_csp(CARTE_AUSTRALIE), AC3(CARTE_AUSTRALIE), Budget(200))
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .coeur import Candidat, Etat
from .moteur import Probleme, Proposition, Strategie


@dataclass(frozen=True)
class Contrainte:
    xi: str
    xj: str
    predicate: Callable[[object, object], bool]

    def supporte(self, vi, vj) -> bool:
        return bool(self.predicate(vi, vj))


@dataclass
class CSP:
    variables: tuple[str, ...]
    domaines: dict[str, tuple]
    contraintes: tuple[Contrainte, ...]

    def arcs(self) -> list[tuple[str, str]]:
        sortie = []
        for c in self.contraintes:
            sortie.append((c.xi, c.xj))
            sortie.append((c.xj, c.xi))
        return sortie

    def voisins(self, xi: str) -> list[str]:
        return sorted({c.xj for c in self.contraintes if c.xi == xi} |
                      {c.xi for c in self.contraintes if c.xj == xi})

    def contraintes_entre(self, xi: str, xj: str) -> list[Contrainte]:
        return [c for c in self.contraintes
                if (c.xi == xi and c.xj == xj) or (c.xi == xj and c.xj == xi)]


def etat_domaines(csp: CSP, domaines: dict[str, tuple], parent: str | None = None,
                  profondeur: int = 0) -> Etat:
    candidats = tuple(Candidat(var, {"var": var, "domaine": tuple(sorted(dom))})
                      for var, dom in sorted(domaines.items()))
    ident = "|".join(f"{v}:{','.join(map(str, sorted(d)))}" for v, d in sorted(domaines.items()))
    return Etat(ident, parent, profondeur, candidats)


def domaines_de(e: Etat) -> dict[str, tuple]:
    return {c.corps["var"]: tuple(c.corps["domaine"]) for c in e.candidats}


def retirer(e: Etat, params: dict) -> list[Etat]:
    var, valeur = params["var"], params["valeur"]
    domaines = domaines_de(e)
    if var not in domaines or valeur not in domaines[var]:
        return []
    domaines[var] = tuple(v for v in domaines[var] if v != valeur)
    return [etat_domaines(None, domaines, e.empreinte(), e.profondeur + 1)]


def score(e: Etat) -> float:
    """Le score préfère l'état **le plus propagé** : la somme des tailles de domaines la plus
    petite. Un domaine vide est un état de contradiction, pas un état « meilleur »."""
    return -float(sum(len(d) for d in domaines_de(e).values()))


def but(e: Etat) -> bool:
    return all(len(d) == 1 for d in domaines_de(e).values())


def probleme_csp(csp: CSP) -> Probleme:
    return Probleme(
        nom="csp",
        initial=lambda: etat_domaines(csp, csp.domaines),
        operateurs={"retirer": retirer},
        but=but,
        heuristique=score,
        score=score,
        csp=csp,
    )


class AC3(Strategie):
    """La file d'arcs : un retrait par proposition, puis les voisins de la variable révisée."""

    nom = "ac3"

    def __init__(self, csp: CSP):
        self.csp = csp
        self.file: list[tuple[str, str]] = csp.arcs()

    def choisir(self, store, probleme):
        return max(store.ouverts, key=lambda f: store.ouverts[f])

    def proposer(self, etat: Etat, probleme: Probleme) -> list[Proposition]:
        while self.file:
            xi, xj = self.file.pop(0)
            domaines = domaines_de(etat)
            if xi not in domaines or xj not in domaines:
                continue
            if not domaines[xi] or not domaines[xj]:
                continue
            contraintes = self.csp.contraintes_entre(xi, xj)
            if not contraintes:
                continue
            retire = [vi for vi in domaines[xi]
                      if not any(all(c.supporte(vi, vj) if c.xi == xi else c.supporte(vj, vi)
                                     for c in contraintes)
                                 for vj in domaines[xj])]
            if not retire:
                continue
            valeur = sorted(retire)[0]
            # après un retrait, il faut réviser le reste du domaine et les voisins
            self.file.append((xi, xj))
            for xk in self.csp.voisins(xi):
                if xk != xj:
                    self.file.append((xk, xi))
            return [Proposition(etat.empreinte(), "retirer", {"var": xi, "valeur": valeur})]
        return []


def verifier_arc_consistance(csp: CSP, domaines: dict[str, tuple]) -> bool:
    for c in csp.contraintes:
        for vi in domaines[c.xi]:
            if not any(c.supporte(vi, vj) for vj in domaines[c.xj]):
                return False
        for vj in domaines[c.xj]:
            if not any(c.supporte(vi, vj) for vi in domaines[c.xi]):
                return False
    return True


def resoudre(csp: CSP, domaines: dict[str, tuple] | None = None) -> dict[str, object] | None:
    """Backtracking : prouve que le point fixe de l'AC-3 n'est pas une impasse."""
    domaines = {v: tuple(d) for v, d in (domaines or csp.domaines).items()}

    def recursif(dom: dict[str, tuple]) -> dict[str, object] | None:
        if any(not d for d in dom.values()):
            return None
        non_assignees = [v for v in csp.variables if len(dom[v]) > 1]
        if not non_assignees:
            solution = {v: dom[v][0] for v in csp.variables}
            return solution if all(c.supporte(solution[c.xi], solution[c.xj])
                                   for c in csp.contraintes) else None
        var = min(non_assignees, key=lambda v: (len(dom[v]), v))
        for valeur in dom[var]:
            nouveau = dict(dom)
            nouveau[var] = (valeur,)
            conflit = any(len(nouveau[c.xi]) == 1 and len(nouveau[c.xj]) == 1 and
                          not c.supporte(nouveau[c.xi][0], nouveau[c.xj][0])
                          for c in csp.contraintes)
            if not conflit:
                résultat = recursif(nouveau)
                if résultat is not None:
                    return résultat
        return None

    return recursif(domaines)


# --------------------------------------------------------------------------- exemples


def _different(vi, vj) -> bool:
    return vi != vj


CARTE_AUSTRALIE = CSP(
    variables=("WA", "NT", "SA", "Q", "NSW", "V", "T"),
    domaines={v: ("r", "g", "b") for v in ("WA", "NT", "SA", "Q", "NSW", "V", "T")},
    contraintes=tuple(Contrainte(a, b, _different) for a, b in (
        ("WA", "NT"), ("WA", "SA"), ("NT", "SA"), ("NT", "Q"), ("SA", "Q"),
        ("SA", "NSW"), ("SA", "V"), ("Q", "NSW"), ("NSW", "V"))),
)

CSP_PROPAGATION = CSP(
    variables=("A", "B", "C"),
    domaines={"A": ("r",), "B": ("r", "g"), "C": ("r", "g")},
    contraintes=(Contrainte("A", "B", _different), Contrainte("B", "C", _different)),
)

CSP_CONTRADICTION = CSP(
    variables=("A", "B"),
    domaines={"A": ("r",), "B": ("r",)},
    contraintes=(Contrainte("A", "B", _different),),
)

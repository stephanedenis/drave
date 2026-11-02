"""operateurs.py — les opérateurs **hétérogènes** de B13 et le conteneur DRVM.

Un problème peut mélanger trois genres d'opérateurs :

  - **symbolique** : une règle discrète (`pas`, les quatre voisins) ;
  - **numérique** : un calcul de coût (`saut`, deux cases, coût 2) ;
  - **neuronal** : une **politique** qui propose le pas (`sonde`, coût 5, un appel).

Le `DRVM` est le **conteneur d'exécution** : il tient le registre, la politique, le moteur et
la trace, et rend un **bilan** (nœuds, coût par opérateur, appels au modèle, but). Le nom est
celui du runtime du moteur ; il ne faut pas le confondre avec le **format DRVM** du programme N.

La politique est un **double de contrat** (`PolitiqueManhattan`) : le vrai modèle natif n'a pas
de poids dans cet environnement ; la structure est prête pour un `PolitiqueDRVM`.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Callable

from .coeur import Candidat, Decision, Etat
from .moteur import AStar, BFS, Greedy, Moteur, Probleme
from .store import Budget

COTE = 5
BUT = (COTE - 1, COTE - 1)


# --------------------------------------------------------------------------- politiques


class Politique:
    nom = "politique"

    def __init__(self):
        self.appels = 0

    def propose(self, etat: Etat, but: tuple[int, int]) -> str | None:
        raise NotImplementedError

    def remise_a_zero(self):
        self.appels = 0


class PolitiqueManhattan(Politique):
    """Le double : choisit la direction qui rapproche le plus (Manhattan)."""

    nom = "manhattan"

    def propose(self, etat, but):
        x, y = _xy(etat)
        bx, by = but
        dx, dy = bx - x, by - y
        if abs(dx) >= abs(dy) and dx != 0:
            return "droite" if dx > 0 else "gauche"
        if dy != 0:
            return "bas" if dy > 0 else "haut"
        return None


class PolitiqueAveugle(Politique):
    """Le contrôle négatif : propose la direction **opposée** au but."""

    nom = "aveugle"

    def propose(self, etat, but):
        x, y = _xy(etat)
        bx, by = but
        dx, dy = bx - x, by - y
        if abs(dx) >= abs(dy) and dx != 0:
            return "gauche" if dx > 0 else "droite"
        if dy != 0:
            return "haut" if dy > 0 else "bas"
        return None


# --------------------------------------------------------------------------- état


def _etat(x: int, y: int, parent: str | None = None, profondeur: int = 0) -> Etat:
    return Etat(f"{x}:{y}", parent, profondeur,
                (Candidat("x", {"v": x}), Candidat("y", {"v": y})))


def _xy(e: Etat) -> tuple[int, int]:
    d = {c.id: c.corps["v"] for c in e.candidats}
    return int(d["x"]), int(d["y"])


def _dans(x: int, y: int) -> bool:
    return 0 <= x < COTE and 0 <= y < COTE


def _deplacer(e: Etat, dx: int, dy: int, cout_profondeur: int = 1) -> list[Etat]:
    x, y = _xy(e)
    nx, ny = x + dx, y + dy
    if not _dans(nx, ny):
        return []
    return [_etat(nx, ny, e.empreinte(), e.profondeur + cout_profondeur)]


# --------------------------------------------------------------------------- opérateurs


def pas(e: Etat, _p: dict | None = None) -> list[Etat]:
    """Symbolique : un pas orthogonal."""
    x, y = _xy(e)
    enfants = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        enfants += _deplacer(e, dx, dy)
    return enfants


def saut(e: Etat, _p: dict | None = None) -> list[Etat]:
    """Numérique : un saut de deux cases (coût 2)."""
    x, y = _xy(e)
    enfants = []
    for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
        enfants += _deplacer(e, dx, dy, 2)
    return enfants


POLITIQUE: list[Politique | None] = [None]


def sonde(e: Etat, _p: dict | None = None) -> list[Etat]:
    """Neuronal : la politique propose une direction ; un appel est compté."""
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, BUT)
    p.appels += 1
    return _deplacer(e, {"droite": 1, "gauche": -1, "bas": 0, "haut": 0}.get(direction, 0),
                     {"bas": 1, "haut": -1}.get(direction, 0))


def but(e: Etat) -> bool:
    return _xy(e) == BUT


def _manhattan(x: int, y: int) -> int:
    return abs(x - BUT[0]) + abs(y - BUT[1])


def score(e: Etat) -> float:
    x, y = _xy(e)
    return 1.0 / (1.0 + _manhattan(x, y))


def heuristique(e: Etat) -> float:
    x, y = _xy(e)
    return -float(_manhattan(x, y))


# --------------------------------------------------------------------------- registre / DRVM


@dataclass
class Operateur:
    nom: str
    genre: str
    cout: float
    applique: Callable
    description: str = ""


@dataclass
class Registre:
    operateurs: dict[str, Operateur] = field(default_factory=dict)

    def genres(self) -> set[str]:
        return {o.genre for o in self.operateurs.values()}

    def couts(self) -> dict[str, float]:
        return {n: o.cout for n, o in self.operateurs.items()}

    def total(self, compte: dict[str, int]) -> float:
        return round(sum(self.operateurs[n].cout * k for n, k in compte.items()
                         if n in self.operateurs), 1)


REGISTRE = Registre({
    "pas": Operateur("pas", "symbolique", 1.0, pas, "un pas orthogonal"),
    "saut": Operateur("saut", "numérique", 2.0, saut, "un saut de deux cases"),
    "sonde": Operateur("sonde", "neuronal", 5.0, sonde, "la politique propose le pas"),
})

GRILLE = Probleme(
    nom="grille",
    initial=lambda: _etat(0, 0),
    operateurs={n: o.applique for n, o in REGISTRE.operateurs.items()},
    but=but,
    heuristique=heuristique,
    score=score,
)


# --------------------------------------------------------------------------- cadenas (le neuronal nécessaire)

BUT_C = 3


def _etat_c(pos: int, parent: str | None = None, profondeur: int = 0) -> Etat:
    return Etat(f"c{pos}", parent, profondeur, (Candidat("pos", {"v": pos}),))


def _pos_c(e: Etat) -> int:
    return int(next(c for c in e.candidats if c.id == "pos").corps["v"])


class PolitiqueCadenas(Politique):
    nom = "cadenas_avant"

    def propose(self, etat, but):
        return "avant" if _pos_c(etat) < but else None


class PolitiqueCadenasAveugle(Politique):
    nom = "cadenas_arriere"

    def propose(self, etat, but):
        pos = _pos_c(etat)
        return "arriere" if pos > 0 else "avant"


def sonde_c(e: Etat, _p: dict | None = None) -> list[Etat]:
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, BUT_C)
    p.appels += 1
    if direction is None:
        return []
    pos = _pos_c(e)
    npos = pos + 1 if direction == "avant" else pos - 1
    return [_etat_c(npos, e.empreinte(), e.profondeur + 1)] if 0 <= npos <= BUT_C else []


def but_c(e: Etat) -> bool:
    return _pos_c(e) == BUT_C


def score_c(e: Etat) -> float:
    return 1.0 / (1.0 + max(0, BUT_C - _pos_c(e)))


def heuristique_c(e: Etat) -> float:
    return -float(max(0, BUT_C - _pos_c(e)))


REGISTRE_CADENAS = Registre({
    "sonde": Operateur("sonde", "neuronal", 1.0, sonde_c, "la politique propose le pas suivant"),
})

CADENAS = Probleme(
    nom="cadenas",
    initial=lambda: _etat_c(0),
    operateurs={"sonde": sonde_c},
    but=but_c,
    heuristique=heuristique_c,
    score=score_c,
)


# --------------------------------------------------------------------------- labyrinthe (le cadenas non linéaire)

MURS = {(0, 1), (1, 1), (2, 1), (4, 1), (1, 3), (2, 3), (3, 3)}
L_BUT = (4, 4)


def _etat_l(x: int, y: int, parent: str | None = None, profondeur: int = 0) -> Etat:
    return Etat(f"l{x}:{y}", parent, profondeur,
                (Candidat("x", {"v": x}), Candidat("y", {"v": y})))


def _xy_l(e: Etat) -> tuple[int, int]:
    d = {c.id: c.corps["v"] for c in e.candidats}
    return int(d["x"]), int(d["y"])


def _libre_l(x: int, y: int) -> bool:
    return 0 <= x < 5 and 0 <= y < 5 and (x, y) not in MURS


def _deplacer_l(e: Etat, dx: int, dy: int, profondeur: int = 1) -> list[Etat]:
    x, y = _xy_l(e)
    nx, ny = x + dx, y + dy
    if not _libre_l(nx, ny):
        return []
    return [_etat_l(nx, ny, e.empreinte(), e.profondeur + profondeur)]


def pas_l(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) for c in _deplacer_l(e, dx, dy)]


def saut_l(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)) for c in _deplacer_l(e, dx, dy, 2)]


def sonde_l(e: Etat, _p: dict | None = None) -> list[Etat]:
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, L_BUT)
    p.appels += 1
    return _deplacer_l(e, {"droite": 1, "gauche": -1, "bas": 0, "haut": 0}.get(direction, 0),
                       {"bas": 1, "haut": -1}.get(direction, 0))


def but_l(e: Etat) -> bool:
    return _xy_l(e) == L_BUT


def _man_l(x: int, y: int) -> int:
    return abs(x - L_BUT[0]) + abs(y - L_BUT[1])


def score_l(e: Etat) -> float:
    x, y = _xy_l(e)
    return 1.0 / (1.0 + _man_l(x, y))


def heuristique_l(e: Etat) -> float:
    x, y = _xy_l(e)
    return -float(_man_l(x, y))


REGISTRE_L = Registre({
    "pas": Operateur("pas", "symbolique", 1.0, pas_l, "un pas dans le labyrinthe"),
    "saut": Operateur("saut", "numérique", 2.0, saut_l, "un saut de deux cases"),
    "sonde": Operateur("sonde", "neuronal", 5.0, sonde_l, "la politique propose le pas"),
})

LABYRINTHE = Probleme(
    nom="labyrinthe",
    initial=lambda: _etat_l(0, 0),
    operateurs={n: o.applique for n, o in REGISTRE_L.operateurs.items()},
    but=but_l,
    heuristique=heuristique_l,
    score=score_l,
)


class DRVM:
    """Le conteneur d'exécution : registre, politique, moteur, trace, bilan."""

    def __init__(self, registre: Registre, politique: Politique):
        self.registre = registre
        self.politique = politique
        self.moteur: Moteur | None = None
        self.resultat: Decision | None = None
        self.probleme: Probleme | None = None

    def penser(self, probleme: Probleme, strategie, budget: Budget,
               arret_sur_but: bool = True) -> Decision:
        POLITIQUE[0] = self.politique
        self.politique.remise_a_zero()
        self.probleme = probleme
        self.moteur = Moteur()
        self.resultat = self.moteur.boucle(probleme, strategie, budget,
                                           arret_sur_but=arret_sur_but)
        return self.resultat

    def bilan(self) -> dict:
        assert self.moteur is not None and self.resultat is not None
        compte = Counter(e.operateur for e in self.moteur.trace.evenements)
        return {"noeuds": len(self.moteur.trace.evenements),
                "but": bool(self.resultat.etat) and self.probleme.but(self.resultat.etat),
                "par_operateur": dict(compte),
                "genres": sorted(self.registre.genres()),
                "cout": self.registre.total(dict(compte)),
                "appels": self.politique.appels,
                "budget": self.resultat.budget_consomme}

    def instantane(self) -> dict:
        b = self.bilan()
        b["politique"] = self.politique.nom
        b["score"] = self.probleme.score(self.resultat.etat) if self.resultat else 0.0
        return b


__all__ = ["BUT", "COTE", "DRVM", "GRILLE", "Operateur", "Politique", "PolitiqueAveugle",
           "PolitiqueManhattan", "REGISTRE", "Registre", "but", "heuristique", "pas", "saut",
           "score", "sonde", "CADENAS", "REGISTRE_CADENAS", "PolitiqueCadenas",
           "PolitiqueCadenasAveugle", "LABYRINTHE", "MURS", "REGISTRE_L"]

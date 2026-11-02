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

import math
import random
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


class PolitiqueApprise(Politique):
    """La porte **apprise** : une Q-table entraînée sur le labyrinthe à porte.

    Le modèle ne connaît pas la direction de la porte : il l'apprend par essais
    (Q-learning tabulaire, récompense +1 au but, -0,01 par pas, +0,1 à l'ouverture).
    """

    nom = "apprise"
    ACTIONS = ("haut", "bas", "gauche", "droite")

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, periode: int = 3):
        super().__init__()
        self.q: dict[tuple, float] = {}
        self.periode = periode
        self.episodes = episodes
        self.rng = random.Random(graine)
        self.alpha, self.gamma, self.eps = alpha, gamma, eps

    @staticmethod
    def _cle(e: Etat) -> tuple:
        d = {c.id: c.corps["v"] for c in e.candidats}
        return int(d["x"]), int(d["y"]), bool(d["open"])

    def _q(self, cle, a):
        return self.q.get((cle, a), 0.0)

    def _pas(self, cle, action, ouvre: bool):
        x, y, o = cle
        if ouvre and (x, y) == (3, 2) and action == "bas":
            o = True
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if not _libre_p(nx, ny, o):
            return cle, 0.0
        gain = 0.1 if (o and not cle[2]) else -0.01
        return (nx, ny, o), gain

    def apprendre(self) -> None:
        for _ in range(self.episodes):
            cle = (0, 0, False)
            for _ in range(120):
                if cle[:2] == P_BUT:
                    break
                if self.rng.random() < self.eps:
                    a = self.rng.choice(self.ACTIONS)
                else:
                    a = max(self.ACTIONS, key=lambda x: self._q(cle, x))
                ncle, gain = self._pas(cle, a, True)
                but = 1.0 if ncle[:2] == P_BUT else 0.0
                best = max(self._q(ncle, x) for x in self.ACTIONS)
                self.q[(cle, a)] = self._q(cle, a) + self.alpha * (
                    gain + but + self.gamma * best - self._q(cle, a))
                cle = ncle

    def propose(self, etat, but):
        cle = self._cle(etat)
        if cle[:2] == P_BUT:
            return None
        return max(self.ACTIONS, key=lambda x: self._q(cle, x))


class PolitiqueAppriseMinute(PolitiqueApprise):
    """La Q-table **entraînée sur la porte minute** : elle apprend l'ouverture-passage."""

    nom = "apprise_minute"

    def _pas(self, cle, action, ouvre: bool):
        x, y, o = cle
        if (x, y) == (3, 2) and action == "bas":
            return (3, 3, False), 0.1
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if not _libre_p(nx, ny, o):
            return cle, 0.0
        return (nx, ny, o), -0.01


class PolitiqueAppriseShaping(PolitiqueAppriseMinute):
    """La Q-table avec **reward shaping** : -0,01 par pas + 0,1 par case gagnée vers le but."""

    nom = "apprise_shaping"

    def _pas(self, cle, action, ouvre: bool):
        ncle, gain = super()._pas(cle, action, ouvre)
        if ncle == cle:
            return cle, 0.0
        d0 = abs(cle[0] - P_BUT[0]) + abs(cle[1] - P_BUT[1])
        d1 = abs(ncle[0] - P_BUT[0]) + abs(ncle[1] - P_BUT[1])
        return ncle, gain + 0.1 * (d0 - d1)


class PolitiqueReseau(Politique):
    """Un **réseau linéaire** (x, y, biais → 4 actions), entraîné par imitation du professeur.

    Le perceptron apprend l'action du professeur (la Q-table de la porte minute) sur les 25
    états ; il **généralise** ensuite à la politique seule. 12 poids, pas une table.
    """

    nom = "reseau"
    ACTIONS = ("haut", "bas", "gauche", "droite")

    def __init__(self, episodes: int = 400, graine: int = 0):
        super().__init__()
        self.w = [[0.0] * 4 for _ in range(3)]  # x, y, biais
        self.rng = random.Random(graine)
        self.episodes = episodes

    def _pas(self, cle, action, ouvre: bool):
        x, y, o = cle
        if (x, y) == (3, 2) and action == "bas":
            return (3, 3, False), 0.1
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if not _libre_p(nx, ny, o):
            return cle, 0.0
        return (nx, ny, o), -0.01

    def _entree(self, e: Etat) -> tuple[float, float, float]:
        x, y = _xy_p(e)
        return x / 4.0, y / 4.0, 1.0

    def _scores(self, e: Etat) -> list[float]:
        x, y, b = self._entree(e)
        return [self.w[0][a] * x + self.w[1][a] * y + self.w[2][a] for a in range(4)]

    def propose(self, etat, but):
        if _xy_p(etat) == P_BUT:
            return None
        s = self._scores(etat)
        return self.ACTIONS[max(range(4), key=lambda i: s[i])]

    def apprendre(self) -> "PolitiqueReseau":
        prof = PolitiqueAppriseMinute(episodes=200, graine=0)
        prof.apprendre()
        for _ in range(self.episodes):
            for x in range(5):
                for y in range(5):
                    if (x, y) == P_BUT:
                        continue
                    e = _etat_p(x, y, False)
                    a = prof.propose(e, P_BUT)
                    if a is None:
                        continue
                    vrai = self.ACTIONS.index(a)
                    s = self._scores(e)
                    pred = max(range(4), key=lambda i: s[i])
                    if pred != vrai:
                        self.w[0][vrai] += x / 4.0
                        self.w[1][vrai] += y / 4.0
                        self.w[2][vrai] += 1.0
                        self.w[0][pred] -= x / 4.0
                        self.w[1][pred] -= y / 4.0
                        self.w[2][pred] -= 1.0
        return self

    @property
    def nb_poids(self) -> int:
        return 12


class PolitiqueAppriseComplete(PolitiqueAppriseShaping):
    """La Q-table **complète** : shaping + récompense +1 au but, entraînée sur la porte minute."""

    nom = "complete"

    def _pas(self, cle, action, ouvre: bool):
        ncle, gain = super()._pas(cle, action, ouvre)
        if ncle[:2] == P_BUT:
            gain += 1.0
        return ncle, gain

    def propose(self, etat, but):
        """Jamais `None` : au but, la meilleure action (le `seule_minute` s'arrête seul)."""
        cle = self._cle(etat)
        return max(self.ACTIONS, key=lambda a: self._q(cle, a))


class PolitiqueAppriseOuverte(PolitiqueApprise):
    """La Q-table **entraînée sur la porte stochastique** (80 %) : elle apprend l'état `open`."""

    nom = "ouverte"

    def _pas(self, cle, action, ouvre: bool):
        x, y, o = cle
        if (x, y) == (3, 2) and action == "bas" and not o:
            if self.rng.random() < 0.8:
                return (3, 3, True), 0.1
            return cle, -0.01
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if not _libre_p(nx, ny, o):
            return cle, 0.0
        return (nx, ny, o), -0.01


class PolitiqueMLP(Politique):
    """Un **MLP** (2 → 8 → 4, tanh), entraîné par imitation du professeur (porte minute).

    Implémentation **pure Python** (pas de torch dans l'environnement) : forward, softmax,
    cross-entropy et rétropropagation manuels. Il peut représenter des décisions non linéaires.
    """

    nom = "mlp"
    ACTIONS = ("haut", "bas", "gauche", "droite")

    def __init__(self, epochs: int = 500, graine: int = 0):
        super().__init__()
        self.rng = random.Random(graine)
        self.W1 = [[self.rng.uniform(-0.5, 0.5) for _ in range(2)] for _ in range(8)]
        self.b1 = [0.0] * 8
        self.W2 = [[self.rng.uniform(-0.5, 0.5) for _ in range(8)] for _ in range(4)]
        self.b2 = [0.0] * 4
        self.epochs = epochs

    def _pas(self, cle, action, ouvre: bool):
        x, y, o = cle
        if (x, y) == (3, 2) and action == "bas":
            return (3, 3, False), 0.1
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if not _libre_p(nx, ny, o):
            return cle, 0.0
        return (nx, ny, o), -0.01

    def _forward(self, x, y):
        x0, y0 = x / 4.0, y / 4.0
        z1 = [self.W1[i][0] * x0 + self.W1[i][1] * y0 + self.b1[i] for i in range(8)]
        h = [math.tanh(v) for v in z1]
        z2 = [sum(self.W2[j][i] * h[i] for i in range(8)) + self.b2[j] for j in range(4)]
        m = max(z2)
        e = [math.exp(v - m) for v in z2]
        s = sum(e)
        return x0, y0, z1, h, z2, [v / s for v in e]

    def propose(self, etat, but):
        if _xy_p(etat) == P_BUT:
            return None
        x, y = _xy_p(etat)
        *_, p = self._forward(x, y)
        return self.ACTIONS[max(range(4), key=lambda j: p[j])]

    def apprendre(self) -> "PolitiqueMLP":
        prof = PolitiqueAppriseMinute(episodes=200, graine=0)
        prof.apprendre()
        X, Y = [], []
        for x in range(5):
            for y in range(5):
                if (x, y) == P_BUT:
                    continue
                a = prof.propose(_etat_p(x, y, False), P_BUT)
                if a is None:
                    continue
                X.append((x, y))
                Y.append(self.ACTIONS.index(a))
        lr = 0.10
        for _ in range(self.epochs):
            for (x, y), t in zip(X, Y):
                x0, y0, z1, h, z2, p = self._forward(x, y)
                d2 = p[:]
                d2[t] -= 1.0
                dW2 = [[d2[j] * h[i] for i in range(8)] for j in range(4)]
                db2 = d2[:]
                dh = [sum(self.W2[j][i] * d2[j] for j in range(4)) for i in range(8)]
                dz1 = [dh[i] * (1.0 - h[i] * h[i]) for i in range(8)]
                dW1 = [[dz1[i] * x0, dz1[i] * y0] for i in range(8)]
                for j in range(4):
                    for i in range(8):
                        self.W2[j][i] -= lr * dW2[j][i]
                    self.b2[j] -= lr * db2[j]
                for i in range(8):
                    self.W1[i][0] -= lr * dW1[i][0]
                    self.W1[i][1] -= lr * dW1[i][1]
                    self.b1[i] -= lr * dz1[i]
        return self

    @property
    def nb_poids(self) -> int:
        return 8 * 2 + 8 + 4 * 8 + 4


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


# --------------------------------------------------------------------------- labyrinthe à porte (le neuronal nécessaire)

MURS_P = {(0, 1), (1, 1), (2, 1), (4, 1), (4, 2), (1, 2), (2, 2), (1, 3), (3, 4)}
PORTE = (3, 3)
P_BUT = (4, 4)


def _etat_p(x: int, y: int, open_: bool, parent: str | None = None,
            profondeur: int = 0) -> Etat:
    return Etat(f"p{x}:{y}:{int(open_)}", parent, profondeur,
                (Candidat("x", {"v": x}), Candidat("y", {"v": y}),
                 Candidat("open", {"v": bool(open_)})))


def _xy_p(e: Etat) -> tuple[int, int]:
    d = {c.id: c.corps["v"] for c in e.candidats}
    return int(d["x"]), int(d["y"])


def _open_p(e: Etat) -> bool:
    return bool(next(c.corps["v"] for c in e.candidats if c.id == "open"))


def _libre_p(x: int, y: int, open_: bool) -> bool:
    if not (0 <= x < 5 and 0 <= y < 5) or (x, y) in MURS_P:
        return False
    return (x, y) != PORTE or open_


def _deplacer_p(e: Etat, dx: int, dy: int, profondeur: int = 1,
                open_: bool | None = None) -> list[Etat]:
    x, y = _xy_p(e)
    o = _open_p(e) if open_ is None else open_
    nx, ny = x + dx, y + dy
    if not _libre_p(nx, ny, o):
        return []
    return [_etat_p(nx, ny, o, e.empreinte(), e.profondeur + profondeur)]


def pas_p(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) for c in _deplacer_p(e, dx, dy)]


def saut_p(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)) for c in _deplacer_p(e, dx, dy, 2)]


def sonde_p(e: Etat, _p: dict | None = None) -> list[Etat]:
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, P_BUT)
    p.appels += 1
    if not direction:
        return []
    x, y = _xy_p(e)
    # la sonde ouvre la porte si la politique vise la porte ; elle avance ensuite.
    open_ = _open_p(e) or ((x, y) == (3, 2) and direction == "bas")
    dx = {"droite": 1, "gauche": -1}.get(direction, 0)
    dy = {"bas": 1, "haut": -1}.get(direction, 0)
    nx, ny = x + dx, y + dy
    if not _libre_p(nx, ny, open_):
        return [_etat_p(x, y, open_, e.empreinte(), e.profondeur)] if open_ != _open_p(e) else []
    return [_etat_p(nx, ny, open_, e.empreinte(), e.profondeur + 1)]


def but_p(e: Etat) -> bool:
    return _xy_p(e) == P_BUT


def _man_p(x: int, y: int) -> int:
    return abs(x - P_BUT[0]) + abs(y - P_BUT[1])


def score_p(e: Etat) -> float:
    x, y = _xy_p(e)
    return 1.0 / (1.0 + _man_p(x, y))


def heuristique_p(e: Etat) -> float:
    x, y = _xy_p(e)
    return -float(_man_p(x, y))


REGISTRE_P = Registre({
    "pas": Operateur("pas", "symbolique", 1.0, pas_p, "un pas ; la porte reste fermée"),
    "saut": Operateur("saut", "numérique", 2.0, saut_p, "un saut ; la porte reste fermée"),
    "sonde": Operateur("sonde", "neuronal", 5.0, sonde_p, "la politique ouvre la porte"),
})

LABYRINTHE_PORTE = Probleme(
    nom="labyrinthe_porte",
    initial=lambda: _etat_p(0, 0, False),
    operateurs={n: o.applique for n, o in REGISTRE_P.operateurs.items()},
    but=but_p,
    heuristique=heuristique_p,
    score=score_p,
)


# --------------------------------------------------------------------------- porte stochastique

def sonde_p_sto(e: Etat, _p: dict | None = None) -> list[Etat]:
    """La porte s'ouvre à 80 % ; sinon l'état reste (la politique doit réessayer)."""
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, P_BUT)
    p.appels += 1
    if not direction:
        return []
    x, y = _xy_p(e)
    open_ = _open_p(e)
    if (x, y) == (3, 2) and direction == "bas":
        if random.random() < 0.8:
            open_ = True
        else:
            return [_etat_p(x, y, open_, e.empreinte(), e.profondeur)]
    dx = {"droite": 1, "gauche": -1}.get(direction, 0)
    dy = {"bas": 1, "haut": -1}.get(direction, 0)
    nx, ny = x + dx, y + dy
    if not _libre_p(nx, ny, open_):
        return []
    return [_etat_p(nx, ny, open_, e.empreinte(), e.profondeur + 1)]


REGISTRE_PSTO = Registre({
    "pas": Operateur("pas", "symbolique", 1.0, pas_p, "un pas ; la porte reste fermée"),
    "saut": Operateur("saut", "numérique", 2.0, saut_p, "un saut ; la porte reste fermée"),
    "sonde": Operateur("sonde", "neuronal", 5.0, sonde_p_sto, "la politique tente la porte (80 %)"),
})

LABYRINTHE_PORTE_STO = Probleme(
    nom="labyrinthe_porte_sto",
    initial=lambda: _etat_p(0, 0, False),
    operateurs={n: o.applique for n, o in REGISTRE_PSTO.operateurs.items()},
    but=but_p,
    heuristique=heuristique_p,
    score=score_p,
)


# --------------------------------------------------------------------------- porte qui se referme

def _deplacer_pf(e: Etat, dx: int, dy: int, profondeur: int = 1) -> list[Etat]:
    x, y, o = _xy_p(e)[0], _xy_p(e)[1], _open_p(e)
    nx, ny = x + dx, y + dy
    if not _libre_p(nx, ny, o):
        return []
    # la porte se referme dès qu'on l'a franchie (ou qu'on la quitte)
    o2 = False if (nx, ny) == PORTE else o
    return [_etat_p(nx, ny, o2, e.empreinte(), e.profondeur + profondeur)]


def pas_pf(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) for c in _deplacer_pf(e, dx, dy)]


def saut_pf(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)) for c in _deplacer_pf(e, dx, dy, 2)]


def sonde_pf(e: Etat, _p: dict | None = None) -> list[Etat]:
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, P_BUT)
    p.appels += 1
    if not direction:
        return []
    x, y = _xy_p(e)
    open_ = _open_p(e) or ((x, y) == (3, 2) and direction == "bas")
    dx = {"droite": 1, "gauche": -1}.get(direction, 0)
    dy = {"bas": 1, "haut": -1}.get(direction, 0)
    nx, ny = x + dx, y + dy
    if not _libre_p(nx, ny, open_):
        return []
    o2 = False if (nx, ny) == PORTE else open_
    return [_etat_p(nx, ny, o2, e.empreinte(), e.profondeur + 1)]


REGISTRE_PF = Registre({
    "pas": Operateur("pas", "symbolique", 1.0, pas_pf, "un pas ; la porte se referme"),
    "saut": Operateur("saut", "numérique", 2.0, saut_pf, "un saut ; la porte se referme"),
    "sonde": Operateur("sonde", "neuronal", 5.0, sonde_pf, "la politique ouvre la porte"),
})

LABYRINTHE_PORTE_FERME = Probleme(
    nom="labyrinthe_porte_ferme",
    initial=lambda: _etat_p(0, 0, False),
    operateurs={n: o.applique for n, o in REGISTRE_PF.operateurs.items()},
    but=but_p,
    heuristique=heuristique_p,
    score=score_p,
)


# --------------------------------------------------------------------------- porte à un tour

def sonde_pm(e: Etat, _p: dict | None = None) -> list[Etat]:
    """La porte ne s'ouvre que le temps d'un pas : la sonde ouvre **et** passe dans le même tour."""
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, P_BUT)
    p.appels += 1
    if not direction:
        return []
    x, y = _xy_p(e)
    if (x, y) == (3, 2) and direction == "bas":
        # la porte s'ouvre et se referme dans le même pas : on passe directement.
        return [_etat_p(3, 3, False, e.empreinte(), e.profondeur + 1)]
    dx = {"droite": 1, "gauche": -1}.get(direction, 0)
    dy = {"bas": 1, "haut": -1}.get(direction, 0)
    nx, ny = x + dx, y + dy
    if not _libre_p(nx, ny, _open_p(e)):
        return []
    return [_etat_p(nx, ny, _open_p(e), e.empreinte(), e.profondeur + 1)]


REGISTRE_PM = Registre({
    "pas": Operateur("pas", "symbolique", 1.0, pas_pf, "un pas ; la porte est fermée"),
    "saut": Operateur("saut", "numérique", 2.0, saut_pf, "un saut ; la porte est fermée"),
    "sonde": Operateur("sonde", "neuronal", 5.0, sonde_pm, "la porte s'ouvre un tour, la sonde passe"),
})

LABYRINTHE_PORTE_MINUTE = Probleme(
    nom="labyrinthe_porte_minute",
    initial=lambda: _etat_p(0, 0, False),
    operateurs={n: o.applique for n, o in REGISTRE_PM.operateurs.items()},
    but=but_p,
    heuristique=heuristique_p,
    score=score_p,
)


class PolitiqueAppriseAleatoire(PolitiqueApprise):
    """La Q-table de la porte **aléatoire** : à chaque pas, la porte saute avec p = 0,2."""

    nom = "aleatoire"

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, p_saut: float = 0.2):
        super().__init__(episodes=episodes, graine=graine, alpha=alpha, gamma=gamma, eps=eps)
        self.p_saut = p_saut

    def _cle(self, e: Etat) -> tuple:
        return _xy_pmob(e)[0], _xy_pmob(e)[1], _open_pmob(e), _d_pmob(e)

    def _pas(self, cle, action, ouvre: bool):
        x, y, o, d = cle
        door = PORTES_MOBILE[d]
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if ouvre and not o and (nx, ny) == door:
            o = True
        if not _libre_pmob(nx, ny, o, d):
            return cle, 0.0
        d2 = 1 - d if self.rng.random() < self.p_saut else d
        gain = 0.1 if (o and not cle[2]) else -0.01
        return (nx, ny, o, d2), gain

    def apprendre(self) -> None:
        for _ in range(self.episodes):
            cle = (0, 0, False, 0)
            for _ in range(120):
                if cle[:2] == P_BUT:
                    break
                if self.rng.random() < self.eps:
                    a = self.rng.choice(self.ACTIONS)
                else:
                    a = max(self.ACTIONS, key=lambda x: self._q(cle, x))
                ncle, gain = self._pas(cle, a, True)
                but = 1.0 if ncle[:2] == P_BUT else 0.0
                best = max(self._q(ncle, x) for x in self.ACTIONS)
                self.q[(cle, a)] = self._q(cle, a) + self.alpha * (
                    gain + but + self.gamma * best - self._q(cle, a))
                cle = ncle

    def propose(self, etat, but):
        cle = self._cle(etat)
        return max(self.ACTIONS, key=lambda a: self._q(cle, a))


def seule_aleatoire(p: PolitiqueAppriseAleatoire, max_pas: int = 200) -> tuple[bool, int]:
    """La politique seule sur la porte aléatoire (le hasard est dans `_pas`)."""
    cle, pas = (0, 0, False, 0), 0
    for _ in range(max_pas):
        if cle[:2] == P_BUT:
            return True, pas
        e = _etat_pmob(cle[0], cle[1], cle[2], cle[3])
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas
        cle, _ = p._pas(cle, a, True)
        pas += 1
    return False, pas


def _obs_partielle(x: int, y: int, d: int) -> int:
    """La porte n'est vue qu'à distance de Manhattan ≤ 1 ; sinon -1 (inconnue)."""
    px, py = PORTES_MOBILE[d]
    return d if abs(x - px) + abs(y - py) <= 1 else -1


class PolitiqueApprisePartielle(PolitiqueApprise):
    """La Q-table à **observation partielle** : le souvenir de la porte (`vu`) est dans l'état.

    La politique croit la porte là où elle l'a vue ; le monde peut la faire sauter (20 %).
    """

    nom = "partielle"

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, p_saut: float = 0.2):
        super().__init__(episodes=episodes, graine=graine, alpha=alpha, gamma=gamma, eps=eps)
        self.p_saut = p_saut

    def _cle(self, e: Etat) -> tuple:
        return _xy_pmob(e)[0], _xy_pmob(e)[1], _open_pmob(e), _d_pmob(e)

    def _pas(self, cle, action, ouvre: bool):
        x, y, o, vu = cle
        d = vu if vu >= 0 else 0          # la croyance : la dernière porte vue
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if ouvre and not o and (nx, ny) == PORTES_MOBILE[d]:
            o = True
        if not _libre_pmob(nx, ny, o, d):
            return cle, 0.0
        monde = 1 - d if self.rng.random() < self.p_saut else d
        vu2 = _obs_partielle(nx, ny, monde)
        gain = 0.1 if (o and not cle[2]) else -0.01
        return (nx, ny, o, vu2), gain

    def apprendre(self) -> None:
        for _ in range(self.episodes):
            cle = (0, 0, False, _obs_partielle(0, 0, 0))
            for _ in range(120):
                if cle[:2] == P_BUT:
                    break
                if self.rng.random() < self.eps:
                    a = self.rng.choice(self.ACTIONS)
                else:
                    a = max(self.ACTIONS, key=lambda x: self._q(cle, x))
                ncle, gain = self._pas(cle, a, True)
                but = 1.0 if ncle[:2] == P_BUT else 0.0
                best = max(self._q(ncle, x) for x in self.ACTIONS)
                self.q[(cle, a)] = self._q(cle, a) + self.alpha * (
                    gain + but + self.gamma * best - self._q(cle, a))
                cle = ncle

    def propose(self, etat, but):
        cle = self._cle(etat)
        return max(self.ACTIONS, key=lambda a: self._q(cle, a))


def seule_partielle(p: PolitiqueApprisePartielle, max_pas: int = 200) -> tuple[bool, int]:
    """La politique seule à observation partielle (le hasard et la mémoire sont dans `_pas`)."""
    cle, pas = (0, 0, False, _obs_partielle(0, 0, 0)), 0
    for _ in range(max_pas):
        if cle[:2] == P_BUT:
            return True, pas
        e = _etat_pmob(cle[0], cle[1], cle[2], max(cle[3], 0))
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas
        cle, _ = p._pas(cle, a, True)
        pas += 1
    return False, pas


def _belief_bucket(p: float) -> int:
    return 0 if p < 0.25 else 1 if p < 0.5 else 2 if p < 0.75 else 3


_BELIEF_P = (0.1, 0.35, 0.65, 0.9)


class PolitiqueAppriseCroyance(PolitiqueApprise):
    """La Q-table à **croyance** : l'état porte la probabilité que la porte soit en (3,3)."""

    nom = "croyance"

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, p_saut: float = 0.2):
        super().__init__(episodes=episodes, graine=graine, alpha=alpha, gamma=gamma, eps=eps)
        self.p_saut = p_saut

    def _cle(self, e: Etat) -> tuple:
        return _xy_pmob(e)[0], _xy_pmob(e)[1], _open_pmob(e), _d_pmob(e)

    def _pas(self, cle, action, ouvre: bool):
        x, y, o, b = cle
        d = 0 if b >= 2 else 1          # la porte la plus probable
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if ouvre and not o and (nx, ny) == PORTES_MOBILE[d]:
            o = True
        if not _libre_pmob(nx, ny, o, d):
            return cle, 0.0
        monde = 1 - d if self.rng.random() < self.p_saut else d
        p0 = _BELIEF_P[b] * (1 - self.p_saut) + (1 - _BELIEF_P[b]) * self.p_saut
        vu = _obs_partielle(nx, ny, monde)
        if vu >= 0:
            p0 = 1.0 if vu == 0 else 0.0
        b2 = _belief_bucket(p0)
        gain = 0.1 if (o and not cle[2]) else -0.01
        return (nx, ny, o, b2), gain

    def apprendre(self) -> None:
        for _ in range(self.episodes):
            cle = (0, 0, False, 2)       # au départ, on ne sait pas : p(0) ≈ 0,65
            for _ in range(120):
                if cle[:2] == P_BUT:
                    break
                if self.rng.random() < self.eps:
                    a = self.rng.choice(self.ACTIONS)
                else:
                    a = max(self.ACTIONS, key=lambda x: self._q(cle, x))
                ncle, gain = self._pas(cle, a, True)
                but = 1.0 if ncle[:2] == P_BUT else 0.0
                best = max(self._q(ncle, x) for x in self.ACTIONS)
                self.q[(cle, a)] = self._q(cle, a) + self.alpha * (
                    gain + but + self.gamma * best - self._q(cle, a))
                cle = ncle

    def propose(self, etat, but):
        cle = self._cle(etat)
        return max(self.ACTIONS, key=lambda a: self._q(cle, a))


def seule_croyance(p: PolitiqueAppriseCroyance, max_pas: int = 200) -> tuple[bool, int]:
    """La politique seule avec la croyance (le hasard et l'observation sont dans `_pas`)."""
    cle, pas = (0, 0, False, 2), 0
    for _ in range(max_pas):
        if cle[:2] == P_BUT:
            return True, pas
        e = _etat_pmob(cle[0], cle[1], cle[2], 0 if cle[3] >= 2 else 1)
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas
        cle, _ = p._pas(cle, a, True)
        pas += 1
    return False, pas


class PolitiqueAppriseCurieuse(PolitiqueAppriseCroyance):
    """La croyance **+ curiosité** : bonus pour la certitude gagnée (aller voir la porte)."""

    nom = "curieuse"

    def _pas(self, cle, action, ouvre: bool):
        ncle, gain = super()._pas(cle, action, ouvre)
        cert0 = abs(_BELIEF_P[cle[3]] - 0.5)
        cert2 = abs(_BELIEF_P[ncle[3]] - 0.5)
        return ncle, gain + 0.5 * (cert2 - cert0)


def seule_curieuse(p: PolitiqueAppriseCurieuse, max_pas: int = 200) -> tuple[bool, int]:
    """La politique seule avec la curiosité (le hasard et l'observation sont dans `_pas`)."""
    cle, pas = (0, 0, False, 2), 0
    for _ in range(max_pas):
        if cle[:2] == P_BUT:
            return True, pas
        e = _etat_pmob(cle[0], cle[1], cle[2], 0 if cle[3] >= 2 else 1)
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas
        cle, _ = p._pas(cle, a, True)
        pas += 1
    return False, pas


class PolitiqueAppriseObservatrice(PolitiqueAppriseCroyance):
    """La croyance **+ action d'observer** : un geste révèle la porte (coût 0,1)."""

    nom = "observatrice"
    ACTIONS = ("haut", "bas", "gauche", "droite", "observer")

    def _pas(self, cle, action, d: int):
        x, y, o, b = cle
        if action == "observer":
            return (x, y, o, 3 if d == 0 else 0), -0.1, d
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        o2 = o or ((nx, ny) == PORTES_MOBILE[d])
        if not _libre_pmob(nx, ny, o2, d):
            return cle, 0.0, d
        monde = 1 - d if self.rng.random() < self.p_saut else d
        vu = _obs_partielle(nx, ny, monde)
        if vu >= 0:
            b2 = 3 if vu == 0 else 0
        else:
            b2 = _belief_bucket(_BELIEF_P[min(b, 3)] * (1 - self.p_saut)
                                + (1 - _BELIEF_P[min(b, 3)]) * self.p_saut)
        gain = 0.1 if (o2 and not o) else -0.01
        return (nx, ny, o2, b2), gain, monde

    def apprendre(self) -> None:
        for _ in range(self.episodes):
            d = self.rng.randint(0, 1)
            cle = (0, 0, False, 2)
            for _ in range(120):
                if cle[:2] == P_BUT:
                    break
                if self.rng.random() < self.eps:
                    a = self.rng.choice(self.ACTIONS)
                else:
                    a = max(self.ACTIONS, key=lambda x: self._q(cle, x))
                ncle, gain, d = self._pas(cle, a, d)
                but = 1.0 if ncle[:2] == P_BUT else 0.0
                best = max(self._q(ncle, x) for x in self.ACTIONS)
                self.q[(cle, a)] = self._q(cle, a) + self.alpha * (
                    gain + but + self.gamma * best - self._q(cle, a))
                cle = ncle

    def propose(self, etat, but):
        cle = self._cle(etat)
        return max(self.ACTIONS, key=lambda a: self._q(cle, a))


def seule_observatrice(p: PolitiqueAppriseObservatrice, max_pas: int = 200) -> tuple[bool, int]:
    """La politique seule avec l'action d'observer (le monde et l'observation sont dans `_pas`)."""
    d = p.rng.randint(0, 1)
    cle, pas = (0, 0, False, 2), 0
    for _ in range(max_pas):
        if cle[:2] == P_BUT:
            return True, pas
        e = _etat_pmob(cle[0], cle[1], cle[2], cle[3])
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas
        cle, _, d = p._pas(cle, a, d)
        pas += 1
    return False, pas


class PolitiqueAppriseObservatriceBruitee(PolitiqueAppriseObservatrice):
    """L'observatrice avec une révélation **bruitée** : 10 % du temps, la porte annoncée est fausse."""

    nom = "observatrice_bruitee"

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, p_saut: float = 0.2,
                 p_erreur: float = 0.1):
        super().__init__(episodes=episodes, graine=graine, alpha=alpha, gamma=gamma,
                         eps=eps, p_saut=p_saut)
        self.p_erreur = p_erreur

    def _pas(self, cle, action, d: int):
        x, y, o, b = cle
        if action == "observer":
            vu = d if self.rng.random() >= self.p_erreur else 1 - d
            return (x, y, o, 3 if vu == 0 else 0), -0.1, d
        return super()._pas(cle, action, d)


def seule_observatrice_bruitee(p: PolitiqueAppriseObservatriceBruitee,
                                max_pas: int = 200) -> tuple[bool, int]:
    return seule_observatrice(p, max_pas)


class PolitiqueAppriseVotante(PolitiqueAppriseObservatrice):
    """L'observatrice qui **vote deux fois** : 10 % d'erreur par look, 1 % sur le vote."""

    nom = "votante"

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, p_saut: float = 0.2,
                 p_erreur: float = 0.1):
        super().__init__(episodes=episodes, graine=graine, alpha=alpha, gamma=gamma,
                         eps=eps, p_saut=p_saut)
        self.p_erreur = p_erreur

    def _pas(self, cle, action, d: int):
        x, y, o, b = cle
        if action == "observer":
            v1 = d if self.rng.random() >= self.p_erreur else 1 - d
            v2 = d if self.rng.random() >= self.p_erreur else 1 - d
            if v1 == v2:
                b2 = 3 if v1 == 0 else 0
            else:
                b2 = 1 if v1 == 0 else 2      # égalité : la croyance reste hésitante
            return (x, y, o, b2), -0.2, d
        return super()._pas(cle, action, d)


def seule_votante(p: PolitiqueAppriseVotante, max_pas: int = 200) -> tuple[bool, int]:
    return seule_observatrice(p, max_pas)


class PolitiqueAppriseVotante3(PolitiqueAppriseObservatrice):
    """L'observatrice qui **vote trois fois** : 10 % d'erreur par look, 0,1 % sur le vote."""

    nom = "votante3"

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, p_saut: float = 0.2,
                 p_erreur: float = 0.1, looks: int = 3):
        super().__init__(episodes=episodes, graine=graine, alpha=alpha, gamma=gamma,
                         eps=eps, p_saut=p_saut)
        self.p_erreur = p_erreur
        self.looks = looks

    def _pas(self, cle, action, d: int):
        x, y, o, b = cle
        if action == "observer":
            votes = [d if self.rng.random() >= self.p_erreur else 1 - d
                     for _ in range(self.looks)]
            n0 = votes.count(0)
            b2 = 3 if n0 > self.looks // 2 else 0
            return (x, y, o, b2), -0.1 * self.looks, d
        return super()._pas(cle, action, d)


def seule_votante3(p: PolitiqueAppriseVotante3, max_pas: int = 200) -> tuple[bool, int]:
    return seule_observatrice(p, max_pas)


_BAYES_P = tuple(0.05 + 0.1 * i for i in range(10))   # p(d=0) sur 10 niveaux


def _bayes_bucket(p: float) -> int:
    i = int(round((p - 0.05) / 0.1))
    return max(0, min(9, i))


class PolitiqueAppriseBayes(PolitiqueAppriseObservatrice):
    """L'observatrice **bayésienne** : chaque look met à jour p(d=0) par la vraisemblance."""

    nom = "bayes"

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, p_saut: float = 0.2,
                 p_erreur: float = 0.1):
        super().__init__(episodes=episodes, graine=graine, alpha=alpha, gamma=gamma,
                         eps=eps, p_saut=p_saut)
        self.p_erreur = p_erreur

    def _pas(self, cle, action, d: int):
        x, y, o, b = cle
        if action == "observer":
            vu = d if self.rng.random() >= self.p_erreur else 1 - d
            p = _BAYES_P[min(b, 9)]
            v = 1.0 - self.p_erreur if vu == 0 else self.p_erreur
            p2 = p * v / (p * v + (1 - p) * (1 - v))
            return (x, y, o, _bayes_bucket(p2)), -0.1, d
        return super()._pas(cle, action, d)


def seule_bayes(p: PolitiqueAppriseBayes, max_pas: int = 200) -> tuple[bool, int]:
    return seule_observatrice(p, max_pas)


class PolitiqueAppriseBayes2(PolitiqueAppriseBayes):
    """Le bayésien à **deux looks** : deux mises à jour successives (0,99 de confiance)."""

    nom = "bayes2"

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, p_saut: float = 0.2,
                 p_erreur: float = 0.1, looks: int = 2):
        super().__init__(episodes=episodes, graine=graine, alpha=alpha, gamma=gamma,
                         eps=eps, p_saut=p_saut, p_erreur=p_erreur)
        self.looks = looks

    def _pas(self, cle, action, d: int):
        x, y, o, b = cle
        if action == "observer":
            p = _BAYES_P[min(b, 9)]
            for _ in range(self.looks):
                vu = d if self.rng.random() >= self.p_erreur else 1 - d
                v = 1.0 - self.p_erreur if vu == 0 else self.p_erreur
                p = p * v / (p * v + (1 - p) * (1 - v))
            return (x, y, o, _bayes_bucket(p)), -0.1 * self.looks, d
        return super()._pas(cle, action, d)


def seule_bayes2(p: PolitiqueAppriseBayes2, max_pas: int = 200) -> tuple[bool, int]:
    return seule_observatrice(p, max_pas)


class PolitiqueAppriseBayesAppris(PolitiqueAppriseBayes):
    """Le bayésien qui **apprend la vraisemblance** : v = taux de looks corrects observé."""

    nom = "bayes_appris"

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, p_saut: float = 0.2,
                 p_erreur: float = 0.1):
        super().__init__(episodes=episodes, graine=graine, alpha=alpha, gamma=gamma,
                         eps=eps, p_saut=p_saut, p_erreur=p_erreur)
        self.n_obs = 0
        self.n_correct = 0
        self.v = 0.5            # au départ : l'observation ne dit rien

    def _pas(self, cle, action, d: int):
        x, y, o, b = cle
        if action == "observer":
            vu = d if self.rng.random() >= self.p_erreur else 1 - d
            self.n_obs += 1
            self.n_correct += int(vu == d)
            self.v = max(0.01, min(0.99, self.n_correct / max(1, self.n_obs)))
            p = _BAYES_P[min(b, 9)]
            v = self.v if vu == 0 else 1.0 - self.v
            p2 = p * v / (p * v + (1 - p) * (1 - v))
            return (x, y, o, _bayes_bucket(p2)), -0.1, d
        return super()._pas(cle, action, d)


def seule_bayes_appris(p: PolitiqueAppriseBayesAppris, max_pas: int = 200) -> tuple[bool, int]:
    return seule_observatrice(p, max_pas)


# --------------------------------------------------------------------------- période qui change


def _d_phase(t: int) -> int:
    """La porte alterne : période 3 pour t < 6, période 2 ensuite (cycle de 10)."""
    t %= 10
    return (t // 3) % 2 if t < 6 else ((t - 6) // 2) % 2


def _etat_pp(x: int, y: int, open_: bool, t: int, parent: str | None = None,
             profondeur: int = 0) -> Etat:
    return Etat(f"q{x}:{y}:{int(open_)}:{t % 10}", parent, profondeur,
                (Candidat("x", {"v": x}), Candidat("y", {"v": y}),
                 Candidat("open", {"v": bool(open_)}), Candidat("t", {"v": int(t) % 10})))


def _xy_pp(e: Etat) -> tuple[int, int]:
    d = {c.id: c.corps["v"] for c in e.candidats}
    return int(d["x"]), int(d["y"])


def _open_pp(e: Etat) -> bool:
    return bool(next(c.corps["v"] for c in e.candidats if c.id == "open"))


def _t_pp(e: Etat) -> int:
    return int(next(c.corps["v"] for c in e.candidats if c.id == "t"))


def _libre_pp(x: int, y: int, open_: bool, t: int) -> bool:
    d = _d_phase(t)
    if not (0 <= x < 5 and 0 <= y < 5):
        return False
    if (x, y) == PORTES_MOBILE[d]:
        return open_
    if (x, y) in PORTES_MOBILE:
        return True
    return (x, y) not in MURS_P


def _deplacer_pp(e: Etat, dx: int, dy: int, profondeur: int = 1,
                 open_: bool | None = None) -> list[Etat]:
    x, y = _xy_pp(e)
    t = _t_pp(e)
    o = _open_pp(e) if open_ is None else open_
    nx, ny = x + dx, y + dy
    if not _libre_pp(nx, ny, o, t):
        return []
    return [_etat_pp(nx, ny, o, t + 1, e.empreinte(), e.profondeur + profondeur)]


def pas_pp(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) for c in _deplacer_pp(e, dx, dy)]


def saut_pp(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)) for c in _deplacer_pp(e, dx, dy, 2)]


def sonde_pp(e: Etat, _p: dict | None = None) -> list[Etat]:
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, P_BUT)
    p.appels += 1
    if not direction:
        return []
    x, y, t = _xy_pp(e)[0], _xy_pp(e)[1], _t_pp(e)
    dx = {"droite": 1, "gauche": -1}.get(direction, 0)
    dy = {"bas": 1, "haut": -1}.get(direction, 0)
    open_ = _open_pp(e) or ((x + dx, y + dy) == PORTES_MOBILE[_d_phase(t)])
    return _deplacer_pp(e, dx, dy, open_=open_)


def but_pp(e: Etat) -> bool:
    return _xy_pp(e) == P_BUT


def score_pp(e: Etat) -> float:
    x, y = _xy_pp(e)
    return 1.0 / (1.0 + abs(x - P_BUT[0]) + abs(y - P_BUT[1]))


def heuristique_pp(e: Etat) -> float:
    x, y = _xy_pp(e)
    return -float(abs(x - P_BUT[0]) + abs(y - P_BUT[1]))


REGISTRE_PP = Registre({
    "pas": Operateur("pas", "symbolique", 1.0, pas_pp, "un pas ; la période a changé"),
    "saut": Operateur("saut", "numérique", 2.0, saut_pp, "un saut ; la période a changé"),
    "sonde": Operateur("sonde", "neuronal", 5.0, sonde_pp, "la politique ouvre la porte du moment"),
})

LABYRINTHE_PORTE_PHASE = Probleme(
    nom="labyrinthe_porte_phase",
    initial=lambda: _etat_pp(0, 0, False, 0),
    operateurs={n: o.applique for n, o in REGISTRE_PP.operateurs.items()},
    but=but_pp,
    heuristique=heuristique_pp,
    score=score_pp,
)


class PolitiqueApprisePhase(PolitiqueApprise):
    """La Q-table de la porte **à période qui change** : l'état porte t % 10."""

    nom = "phase"

    def _cle(self, e: Etat) -> tuple:
        return _xy_pp(e)[0], _xy_pp(e)[1], _open_pp(e), _t_pp(e)

    def _pas(self, cle, action, ouvre: bool):
        x, y, o, t = cle
        d = _d_phase(t)
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if ouvre and not o and (nx, ny) == PORTES_MOBILE[d]:
            o = True
        if not _libre_pp(nx, ny, o, t):
            return cle, 0.0
        gain = 0.1 if (o and not cle[2]) else -0.01
        return (nx, ny, o, (t + 1) % 10), gain

    def apprendre(self) -> None:
        for _ in range(self.episodes):
            cle = (0, 0, False, 0)
            for _ in range(120):
                if cle[:2] == P_BUT:
                    break
                if self.rng.random() < self.eps:
                    a = self.rng.choice(self.ACTIONS)
                else:
                    a = max(self.ACTIONS, key=lambda x: self._q(cle, x))
                ncle, gain = self._pas(cle, a, True)
                but = 1.0 if ncle[:2] == P_BUT else 0.0
                best = max(self._q(ncle, x) for x in self.ACTIONS)
                self.q[(cle, a)] = self._q(cle, a) + self.alpha * (
                    gain + but + self.gamma * best - self._q(cle, a))
                cle = ncle

    def propose(self, etat, but):
        cle = self._cle(etat)
        return max(self.ACTIONS, key=lambda a: self._q(cle, a))


def seule_phase(p: PolitiqueApprisePhase, max_pas: int = 200) -> tuple[bool, int]:
    cle, pas = (0, 0, False, 0), 0
    for _ in range(max_pas):
        if cle[:2] == P_BUT:
            return True, pas
        e = _etat_pp(cle[0], cle[1], cle[2], cle[3])
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas
        cle, _ = p._pas(cle, a, True)
        pas += 1
    return False, pas


# --------------------------------------------------------------------------- porte qui bouge


def _d_bouge(t: int, periode: int = 3) -> int:
    return (t // periode) % 2


def _etat_pb(x: int, y: int, open_: bool, t: int, parent: str | None = None,
             profondeur: int = 0) -> Etat:
    return Etat(f"b{x}:{y}:{int(open_)}:{t % 6}", parent, profondeur,
                (Candidat("x", {"v": x}), Candidat("y", {"v": y}),
                 Candidat("open", {"v": bool(open_)}), Candidat("t", {"v": int(t) % 6})))


def _xy_pb(e: Etat) -> tuple[int, int]:
    d = {c.id: c.corps["v"] for c in e.candidats}
    return int(d["x"]), int(d["y"])


def _open_pb(e: Etat) -> bool:
    return bool(next(c.corps["v"] for c in e.candidats if c.id == "open"))


def _t_pb(e: Etat) -> int:
    return int(next(c.corps["v"] for c in e.candidats if c.id == "t"))


def _libre_pb(x: int, y: int, open_: bool, t: int, periode: int = 3) -> bool:
    d = _d_bouge(t, periode)
    if not (0 <= x < 5 and 0 <= y < 5):
        return False
    if (x, y) == PORTES_MOBILE[d]:
        return open_
    if (x, y) in PORTES_MOBILE:
        return True
    return (x, y) not in MURS_P


def _deplacer_pb(e: Etat, dx: int, dy: int, profondeur: int = 1,
                 open_: bool | None = None) -> list[Etat]:
    x, y = _xy_pb(e)
    t = _t_pb(e)
    o = _open_pb(e) if open_ is None else open_
    nx, ny = x + dx, y + dy
    if not _libre_pb(nx, ny, o, t):
        return []
    return [_etat_pb(nx, ny, o, t + 1, e.empreinte(), e.profondeur + profondeur)]


def pas_pb(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) for c in _deplacer_pb(e, dx, dy)]


def saut_pb(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)) for c in _deplacer_pb(e, dx, dy, 2)]


def sonde_pb(e: Etat, _p: dict | None = None) -> list[Etat]:
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, P_BUT)
    p.appels += 1
    if not direction:
        return []
    x, y, t = _xy_pb(e)[0], _xy_pb(e)[1], _t_pb(e)
    dx = {"droite": 1, "gauche": -1}.get(direction, 0)
    dy = {"bas": 1, "haut": -1}.get(direction, 0)
    open_ = _open_pb(e) or ((x + dx, y + dy) == PORTES_MOBILE[_d_bouge(t)])
    return _deplacer_pb(e, dx, dy, open_=open_)


def but_pb(e: Etat) -> bool:
    return _xy_pb(e) == P_BUT


def score_pb(e: Etat) -> float:
    x, y = _xy_pb(e)
    return 1.0 / (1.0 + abs(x - P_BUT[0]) + abs(y - P_BUT[1]))


def heuristique_pb(e: Etat) -> float:
    x, y = _xy_pb(e)
    return -float(abs(x - P_BUT[0]) + abs(y - P_BUT[1]))


REGISTRE_PB = Registre({
    "pas": Operateur("pas", "symbolique", 1.0, pas_pb, "un pas ; la porte bouge"),
    "saut": Operateur("saut", "numérique", 2.0, saut_pb, "un saut ; la porte bouge"),
    "sonde": Operateur("sonde", "neuronal", 5.0, sonde_pb, "la politique ouvre la porte du moment"),
})

LABYRINTHE_PORTE_BOUGE = Probleme(
    nom="labyrinthe_porte_bouge",
    initial=lambda: _etat_pb(0, 0, False, 0),
    operateurs={n: o.applique for n, o in REGISTRE_PB.operateurs.items()},
    but=but_pb,
    heuristique=heuristique_pb,
    score=score_pb,
)


class PolitiqueAppriseBouge(PolitiqueApprise):
    """La Q-table de la porte **qui bouge** : l'état porte l'horloge (t % 6)."""

    nom = "bouge"

    def __init__(self, episodes: int = 600, graine: int = 0, alpha: float = 0.25,
                 gamma: float = 0.95, eps: float = 0.25, periode: int = 3):
        super().__init__(episodes=episodes, graine=graine, alpha=alpha, gamma=gamma,
                         eps=eps, periode=periode)

    def _cle(self, e: Etat) -> tuple:
        return _xy_pb(e)[0], _xy_pb(e)[1], _open_pb(e), _t_pb(e)

    def _pas(self, cle, action, ouvre: bool):
        x, y, o, t = cle
        d = _d_bouge(t, self.periode)
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if ouvre and not o and (nx, ny) == PORTES_MOBILE[d]:
            o = True
        if not _libre_pb(nx, ny, o, t):
            return cle, 0.0
        gain = 0.1 if (o and not cle[2]) else -0.01
        return (nx, ny, o, (t + 1) % 6), gain

    def apprendre(self) -> None:
        for _ in range(self.episodes):
            cle = (0, 0, False, 0)
            for _ in range(120):
                if cle[:2] == P_BUT:
                    break
                if self.rng.random() < self.eps:
                    a = self.rng.choice(self.ACTIONS)
                else:
                    a = max(self.ACTIONS, key=lambda x: self._q(cle, x))
                ncle, gain = self._pas(cle, a, True)
                but = 1.0 if ncle[:2] == P_BUT else 0.0
                best = max(self._q(ncle, x) for x in self.ACTIONS)
                self.q[(cle, a)] = self._q(cle, a) + self.alpha * (
                    gain + but + self.gamma * best - self._q(cle, a))
                cle = ncle

    def propose(self, etat, but):
        cle = self._cle(etat)
        return max(self.ACTIONS, key=lambda a: self._q(cle, a))


def seule_bouge(p: PolitiqueAppriseBouge, max_pas: int = 200) -> tuple[bool, int]:
    """La politique seule sur la porte qui bouge."""
    cle, pas = (0, 0, False, 0), 0
    for _ in range(max_pas):
        if cle[:2] == P_BUT:
            return True, pas
        e = _etat_pb(cle[0], cle[1], cle[2], cle[3])
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas
        cle, _ = p._pas(cle, a, True)
        pas += 1
    return False, pas


# --------------------------------------------------------------------------- porte mobile


PORTES_MOBILE = ((3, 3), (1, 3))


def _etat_pmob(x: int, y: int, open_: bool, d: int, parent: str | None = None,
               profondeur: int = 0) -> Etat:
    return Etat(f"m{x}:{y}:{int(open_)}:{d}", parent, profondeur,
                (Candidat("x", {"v": x}), Candidat("y", {"v": y}),
                 Candidat("open", {"v": bool(open_)}), Candidat("d", {"v": int(d)})))


def _xy_pmob(e: Etat) -> tuple[int, int]:
    dd = {c.id: c.corps["v"] for c in e.candidats}
    return int(dd["x"]), int(dd["y"])


def _open_pmob(e: Etat) -> bool:
    return bool(next(c.corps["v"] for c in e.candidats if c.id == "open"))


def _d_pmob(e: Etat) -> int:
    return int(next(c.corps["v"] for c in e.candidats if c.id == "d"))


def _libre_pmob(x: int, y: int, open_: bool, d: int) -> bool:
    if not (0 <= x < 5 and 0 <= y < 5):
        return False
    if (x, y) == PORTES_MOBILE[d]:
        return open_
    if (x, y) in PORTES_MOBILE:
        return True            # l'autre porte est libre
    return (x, y) not in MURS_P


def _deplacer_pmob(e: Etat, dx: int, dy: int, profondeur: int = 1,
                   open_: bool | None = None) -> list[Etat]:
    x, y = _xy_pmob(e)
    o = _open_pmob(e) if open_ is None else open_
    d = _d_pmob(e)
    nx, ny = x + dx, y + dy
    if not _libre_pmob(nx, ny, o, d):
        return []
    return [_etat_pmob(nx, ny, o, d, e.empreinte(), e.profondeur + profondeur)]


def pas_pmob(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) for c in _deplacer_pmob(e, dx, dy)]


def saut_pmob(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)) for c in _deplacer_pmob(e, dx, dy, 2)]


def _vise_porte(e: Etat, direction: str) -> bool:
    x, y = _xy_pmob(e)
    d = _d_pmob(e)
    dx = {"droite": 1, "gauche": -1}.get(direction, 0)
    dy = {"bas": 1, "haut": -1}.get(direction, 0)
    return (x + dx, y + dy) == PORTES_MOBILE[d]


def sonde_pmob(e: Etat, _p: dict | None = None) -> list[Etat]:
    """La politique ouvre la porte **mobile** si elle la vise, puis avance."""
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, P_BUT)
    p.appels += 1
    if not direction:
        return []
    open_ = _open_pmob(e) or _vise_porte(e, direction)
    dx = {"droite": 1, "gauche": -1}.get(direction, 0)
    dy = {"bas": 1, "haut": -1}.get(direction, 0)
    return _deplacer_pmob(e, dx, dy, open_=open_)


def but_pmob(e: Etat) -> bool:
    return _xy_pmob(e) == P_BUT


def score_pmob(e: Etat) -> float:
    x, y = _xy_pmob(e)
    return 1.0 / (1.0 + abs(x - P_BUT[0]) + abs(y - P_BUT[1]))


def heuristique_pmob(e: Etat) -> float:
    x, y = _xy_pmob(e)
    return -float(abs(x - P_BUT[0]) + abs(y - P_BUT[1]))


REGISTRE_PMOB = Registre({
    "pas": Operateur("pas", "symbolique", 1.0, pas_pmob, "un pas ; la porte mobile reste fermée"),
    "saut": Operateur("saut", "numérique", 2.0, saut_pmob, "un saut ; la porte mobile reste fermée"),
    "sonde": Operateur("sonde", "neuronal", 5.0, sonde_pmob, "la politique ouvre la porte mobile"),
})


def _labyrinthe_mobile(d: int) -> Probleme:
    return Probleme(
        nom=f"labyrinthe_porte_mobile_{d}",
        initial=lambda: _etat_pmob(0, 0, False, d),
        operateurs={n: o.applique for n, o in REGISTRE_PMOB.operateurs.items()},
        but=but_pmob,
        heuristique=heuristique_pmob,
        score=score_pmob,
    )


LABYRINTHE_PORTE_MOBILE_0 = _labyrinthe_mobile(0)
LABYRINTHE_PORTE_MOBILE_1 = _labyrinthe_mobile(1)


class PolitiqueAppriseMobile(PolitiqueApprise):
    """La Q-table de la porte **mobile** : l'état porte la position de la porte (d)."""

    nom = "mobile"

    def _cle(self, e: Etat) -> tuple:
        return _xy_pmob(e)[0], _xy_pmob(e)[1], _open_pmob(e), _d_pmob(e)

    def _pas(self, cle, action, ouvre: bool):
        x, y, o, d = cle
        if ouvre and not o and _vise_porte(_etat_pmob(x, y, o, d), action):
            o = True
        dx = {"droite": 1, "gauche": -1}.get(action, 0)
        dy = {"bas": 1, "haut": -1}.get(action, 0)
        nx, ny = x + dx, y + dy
        if not _libre_pmob(nx, ny, o, d):
            return cle, 0.0
        gain = 0.1 if (o and not cle[2]) else -0.01
        return (nx, ny, o, d), gain

    def apprendre(self) -> None:
        for i in range(self.episodes):
            d = i % 2
            cle = (0, 0, False, d)
            for _ in range(120):
                if cle[:2] == P_BUT:
                    break
                if self.rng.random() < self.eps:
                    a = self.rng.choice(self.ACTIONS)
                else:
                    a = max(self.ACTIONS, key=lambda x: self._q(cle, x))
                ncle, gain = self._pas(cle, a, True)
                but = 1.0 if ncle[:2] == P_BUT else 0.0
                best = max(self._q(ncle, x) for x in self.ACTIONS)
                self.q[(cle, a)] = self._q(cle, a) + self.alpha * (
                    gain + but + self.gamma * best - self._q(cle, a))
                cle = ncle

    def propose(self, etat, but):
        cle = self._cle(etat)
        return max(self.ACTIONS, key=lambda a: self._q(cle, a))


def seule_mobile(p: PolitiqueAppriseMobile, d: int, max_pas: int = 200) -> tuple[bool, int]:
    """La politique seule sur la porte mobile (d = position de la porte)."""
    cle, pas = (0, 0, False, d), 0
    for _ in range(max_pas):
        if cle[:2] == P_BUT:
            return True, pas
        e = _etat_pmob(cle[0], cle[1], cle[2], cle[3])
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas
        cle, _ = p._pas(cle, a, True)
        pas += 1
    return False, pas


# --------------------------------------------------------------------------- fenêtre temporelle

def _etat_pw(x: int, y: int, t: int, parent: str | None = None,
             profondeur: int = 0) -> Etat:
    return Etat(f"w{x}:{y}:{t % 3}", parent, profondeur,
                (Candidat("x", {"v": x}), Candidat("y", {"v": y}),
                 Candidat("t", {"v": t % 3})))


def _xy_pw(e: Etat) -> tuple[int, int]:
    d = {c.id: c.corps["v"] for c in e.candidats}
    return int(d["x"]), int(d["y"])


def _t_pw(e: Etat) -> int:
    return int(next(c.corps["v"] for c in e.candidats if c.id == "t"))


def _open_pw(e: Etat) -> bool:
    return _t_pw(e) == 0


def _libre_pw(x: int, y: int, t: int) -> bool:
    if not (0 <= x < 5 and 0 <= y < 5) or (x, y) in MURS_P:
        return False
    return (x, y) != (3, 3) or t % 3 == 0


def _deplacer_pw(e: Etat, dx: int, dy: int, profondeur: int = 1) -> list[Etat]:
    x, y, t = _xy_pw(e)[0], _xy_pw(e)[1], _t_pw(e)
    nx, ny = x + dx, y + dy
    if not _libre_pw(nx, ny, t):
        return []
    return [_etat_pw(nx, ny, t + 1, e.empreinte(), e.profondeur + profondeur)]


def pas_pw(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) for c in _deplacer_pw(e, dx, dy)]


def saut_pw(e: Etat, _p: dict | None = None) -> list[Etat]:
    return [c for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)) for c in _deplacer_pw(e, dx, dy, 2)]


def attendre(e: Etat, _p: dict | None = None) -> list[Etat]:
    x, y, t = _xy_pw(e)[0], _xy_pw(e)[1], _t_pw(e)
    return [_etat_pw(x, y, t + 1, e.empreinte(), e.profondeur + 1)]


def sonde_pw(e: Etat, _p: dict | None = None) -> list[Etat]:
    p = POLITIQUE[0]
    if p is None:
        return []
    direction = p.propose(e, P_BUT)
    p.appels += 1
    if not direction:
        return []
    x, y, t = _xy_pw(e)[0], _xy_pw(e)[1], _t_pw(e)
    dx = {"droite": 1, "gauche": -1}.get(direction, 0)
    dy = {"bas": 1, "haut": -1}.get(direction, 0)
    nx, ny = x + dx, y + dy
    if not _libre_pw(nx, ny, t):
        return []
    return [_etat_pw(nx, ny, t + 1, e.empreinte(), e.profondeur + 1)]


def but_pw(e: Etat) -> bool:
    return _xy_pw(e) == P_BUT


def score_pw(e: Etat) -> float:
    x, y = _xy_pw(e)
    return 1.0 / (1.0 + abs(x - P_BUT[0]) + abs(y - P_BUT[1]))


def heuristique_pw(e: Etat) -> float:
    x, y = _xy_pw(e)
    return -float(abs(x - P_BUT[0]) + abs(y - P_BUT[1]))


REGISTRE_PW = Registre({
    "pas": Operateur("pas", "symbolique", 1.0, pas_pw, "un pas ; le temps avance"),
    "saut": Operateur("saut", "numérique", 2.0, saut_pw, "un saut ; le temps avance"),
    "attendre": Operateur("attendre", "temporel", 1.0, attendre, "attendre le tour de la porte"),
    "sonde": Operateur("sonde", "neuronal", 5.0, sonde_pw, "la politique propose le pas"),
})

LABYRINTHE_PORTE_FENETRE = Probleme(
    nom="labyrinthe_porte_fenetre",
    initial=lambda: _etat_pw(0, 0, 0),
    operateurs={n: o.applique for n, o in REGISTRE_PW.operateurs.items()},
    but=but_pw,
    heuristique=heuristique_pw,
    score=score_pw,
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
           "PolitiqueCadenasAveugle", "LABYRINTHE", "MURS", "REGISTRE_L", "PolitiqueApprise", "PolitiqueAppriseMinute", "PolitiqueAppriseShaping", "PolitiqueReseau", "PolitiqueMLP", "PolitiqueAppriseComplete", "PolitiqueAppriseOuverte",
           "LABYRINTHE_PORTE", "REGISTRE_P", "LABYRINTHE_PORTE_STO", "REGISTRE_PSTO",
           "LABYRINTHE_PORTE_FERME", "REGISTRE_PF",
           "LABYRINTHE_PORTE_MINUTE", "REGISTRE_PM",
           "LABYRINTHE_PORTE_FENETRE", "REGISTRE_PW"]

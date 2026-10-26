#!/usr/bin/env python3
"""regles.go — le go, plateau N×N, captures, ko simple, score Tromp-Taylor.

Le go est le jeu où la **règle locale** (une pierre sans liberté est prise) et la
**règle globale** (le ko, le score) se rencontrent. C'est un bon témoin pour
l'étage 2 : une action est un point (ou une passe), et la validité dépend de tout
le plateau. On implémente le **ko simple** (positionnelle immédiate), pas le ko
positionnel complet : c'est écrit dans la fiche, et le contrôle négatif le dit.

Le score est celui de Tromp-Taylor : pierres + territoire (les régions vides
bordées par une seule couleur), sans retirer les pierres mortes. C'est le score
des parties aléatoires et des playouts ; il ne prétend pas remplacer un arbitre
humain en fin de partie réelle.
"""
from __future__ import annotations

from typing import Iterable

from ..rsn import Annotation, RSN

VIDE, NOIR, BLANC = 0, 1, 2
_LETTRES_GTP = "ABCDEFGHJKLMNOPQRST"  # le go saute le I


class ErreurGo(ValueError):
    pass


def _coord(p: int, n: int) -> tuple[int, int]:
    return divmod(p, n)


def _idx(row: int, col: int, n: int) -> int:
    return row * n + col


def voisins(p: int, n: int) -> list[int]:
    row, col = _coord(p, n)
    out = []
    if row > 0:
        out.append(_idx(row - 1, col, n))
    if row < n - 1:
        out.append(_idx(row + 1, col, n))
    if col > 0:
        out.append(_idx(row, col - 1, n))
    if col < n - 1:
        out.append(_idx(row, col + 1, n))
    return out


def groupe(plateau: list[int], p: int, n: int) -> tuple[set[int], set[int]]:
    """Les pierres du groupe et ses libertés."""
    couleur = plateau[p]
    if couleur == VIDE:
        return set(), set()
    pierres, libertes = {p}, set()
    pile = [p]
    while pile:
        q = pile.pop()
        for r in voisins(q, n):
            if plateau[r] == VIDE:
                libertes.add(r)
            elif plateau[r] == couleur and r not in pierres:
                pierres.add(r)
                pile.append(r)
    return pierres, libertes


def _joue_sur(plateau: list[int], p: int, n: int, couleur: int) -> tuple[list[int], list[int]]:
    """Pose une pierre et retire les groupes ennemis sans liberté.

    Rend (nouveau plateau, points capturés). Ne teste ni le suicide ni le ko.
    """
    b = list(plateau)
    b[p] = couleur
    adv = BLANC if couleur == NOIR else NOIR
    captures: list[int] = []
    for r in voisins(p, n):
        if b[r] == adv:
            pierres, libs = groupe(b, r, n)
            if not libs:
                for q in pierres:
                    b[q] = VIDE
                captures.extend(sorted(pierres))
    return b, captures


class Position:
    __slots__ = ("n", "plateau", "trait", "ko", "passe", "komi", "abandon")

    def __init__(self, n: int = 9, plateau: list[int] | None = None,
                 trait: int = NOIR, ko: int = -1, passe: int = 0,
                 komi: int = 65, abandon: int = 0) -> None:
        if not 2 <= n <= 25:
            raise ErreurGo(f"taille de plateau invalide : {n}")
        self.n = n
        self.plateau = list(plateau) if plateau is not None else [VIDE] * (n * n)
        if len(self.plateau) != n * n:
            raise ErreurGo("le plateau ne fait pas N×N")
        if any(x not in (VIDE, NOIR, BLANC) for x in self.plateau):
            raise ErreurGo("pierre inconnue sur le plateau")
        self.trait = trait
        self.ko = ko
        self.passe = passe
        self.komi = komi
        self.abandon = abandon

    @classmethod
    def depart(cls, n: int = 9, komi: int = 65) -> "Position":
        return cls(n, None, NOIR, -1, 0, komi, 0)

    def copie(self) -> "Position":
        return Position(self.n, self.plateau, self.trait, self.ko, self.passe,
                        self.komi, self.abandon)

    # ---- légalité ------------------------------------------------------
    def _simule(self, p: int) -> tuple[list[int], list[int]]:
        return _joue_sur(self.plateau, p, self.n, self.trait)

    def coup_legal(self, p: int) -> bool:
        if not 0 <= p < self.n * self.n:
            return False
        if self.plateau[p] != VIDE:
            return False
        if p == self.ko:
            return False
        b, caps = self._simule(p)
        # suicide : le groupe de la pierre posée n'a aucune liberté
        _, libs = groupe(b, p, self.n)
        return bool(libs)

    def coups_legaux(self) -> list[int]:
        return [p for p in range(self.n * self.n) if self.coup_legal(p)]

    def nouveau_ko(self, p: int, captures: list[int]) -> int:
        """Ko simple : la prise d'UNE pierre par UNE pierre qui n'a qu'une liberté."""
        if len(captures) != 1:
            return -1
        # après le coup, le groupe de la pierre posée doit être seul et avoir
        # exactement une liberté (la case de la pierre prise)
        b, _ = _joue_sur(self.plateau, p, self.n, self.trait)
        pierres, libs = groupe(b, p, self.n)
        if len(pierres) == 1 and len(libs) == 1 and captures[0] in libs:
            return captures[0]
        return -1

    # ---- application ---------------------------------------------------
    def joue(self, p: int | None) -> "Position":
        """p=None (ou -1) = passe."""
        if p is None or p == -1:
            return Position(self.n, self.plateau, BLANC if self.trait == NOIR else NOIR,
                            -1, self.passe + 1, self.komi, self.abandon)
        if not self.coup_legal(p):
            raise ErreurGo(f"coup illégal en {p}")
        b, caps = self._simule(p)
        ko = self.nouveau_ko(p, caps)
        return Position(self.n, b, BLANC if self.trait == NOIR else NOIR,
                        ko, 0, self.komi, self.abandon)

    def passe_tour(self) -> "Position":
        return self.joue(None)

    def abandonne(self) -> "Position":
        q = self.copie()
        q.abandon = self.trait
        return q

    # ---- terminalité et score -----------------------------------------
    def terminal(self) -> bool:
        if self.abandon:
            return True
        if self.passe >= 2:
            return True
        # un plateau plein n'a plus de coup, mais la passe reste possible : on
        # ne déclare pas la fin sans deux passes (règle Tromp-Taylor).
        return False

    def territoire(self) -> tuple[int, int, int]:
        """(territoire noir, territoire blanc, neutre) en points."""
        vus: set[int] = set()
        noir = blanc = neutre = 0
        n = self.n
        for p in range(n * n):
            if self.plateau[p] != VIDE or p in vus:
                continue
            region = set()
            frontieres: set[int] = set()
            pile = [p]
            while pile:
                q = pile.pop()
                if q in vus:
                    continue
                vus.add(q)
                region.add(q)
                for r in voisins(q, n):
                    c = self.plateau[r]
                    if c == VIDE:
                        if r not in vus:
                            pile.append(r)
                    else:
                        frontieres.add(c)
            if frontieres == {NOIR}:
                noir += len(region)
            elif frontieres == {BLANC}:
                blanc += len(region)
            else:
                neutre += len(region)
        return noir, blanc, neutre

    def score(self) -> tuple[int, int]:
        """(score noir, score blanc) en DIXIÈMES de point (komi compris)."""
        pierres_n = sum(1 for x in self.plateau if x == NOIR)
        pierres_b = sum(1 for x in self.plateau if x == BLANC)
        terr_n, terr_b, _ = self.territoire()
        return (pierres_n + terr_n) * 10, (pierres_b + terr_b) * 10 + self.komi

    def difference(self) -> int:
        n, b = self.score()
        return n - b

    def resultat(self) -> str | None:
        if self.abandon:
            return "W+" if self.abandon == NOIR else "B+"
        if not self.terminal():
            return None
        d = self.difference()
        if d == 0:
            return "0"
        return ("B+" if d > 0 else "W+") + _format_points(abs(d))

    def utilite(self) -> float:
        """Du point de vue du joueur au trait, en dixièmes."""
        d = self.difference()
        return float(d if self.trait == NOIR else -d)

    def heuristique(self) -> float:
        return self.utilite()

    def cle(self) -> tuple:
        return tuple(self.plateau), self.trait, self.ko

    # ---- lecture/écriture ---------------------------------------------
    def vers_rsn(self, annotation: Annotation | None = None) -> RSN:
        return RSN("go", "etat", {
            "taille": self.n, "plateau": list(self.plateau), "trait": self.trait,
            "ko": self.ko if self.ko >= 0 else None, "passe": self.passe,
            "komi": self.komi,
        }, annotation or Annotation(langue="notation", format="gtp", surface=""))

    @classmethod
    def depuis_rsn(cls, rsn: RSN, valide: bool = True) -> "Position":
        c = rsn.corps
        pos = cls(int(c["taille"]), [int(x) for x in c["plateau"]],
                  int(c["trait"]), int(c["ko"]) if c.get("ko") is not None else -1,
                  int(c.get("passe", 0)), int(c.get("komi", 65)), int(c.get("abandon", 0)))
        if valide:
            # un ko ne peut pas désigner une case occupée
            if pos.ko >= 0 and pos.plateau[pos.ko] != VIDE:
                raise ErreurGo("ko sur une case occupée")
        return pos


def _format_points(d: int) -> str:
    """Dixièmes → « 3.5 » ou « 3 »."""
    if d % 10 == 0:
        return str(d // 10)
    return f"{d // 10}.{d % 10}"


# ---------------------------------------------------------------------------
# Coordonnées : GTP, SGF, (ligne, colonne)
# ---------------------------------------------------------------------------
def gtp_vers_point(s: str, n: int) -> int:
    s = s.strip().upper()
    if len(s) < 2:
        raise ErreurGo(f"coordonnée GTP invalide : {s!r}")
    col = _LETTRES_GTP.find(s[0])
    if col < 0 or col >= n:
        raise ErreurGo(f"colonne GTP invalide : {s[0]!r}")
    try:
        rang = int(s[1:])
    except ValueError:
        raise ErreurGo(f"rangée GTP invalide : {s!r}")
    if not 1 <= rang <= n:
        raise ErreurGo(f"rangée GTP hors plateau : {rang}")
    return (n - rang) * n + col


def point_vers_gtp(p: int, n: int) -> str:
    row, col = _coord(p, n)
    return f"{_LETTRES_GTP[col]}{n - row}"


def sgf_vers_point(s: str, n: int) -> int:
    if s in ("", "tt"):
        return -1  # passe dans l'ancien SGF
    if len(s) != 2:
        raise ErreurGo(f"coordonnée SGF invalide : {s!r}")
    col = ord(s[0]) - 97
    row = ord(s[1]) - 97
    if not (0 <= col < n and 0 <= row < n):
        raise ErreurGo(f"coordonnée SGF hors plateau : {s!r}")
    return row * n + col


def point_vers_sgf(p: int, n: int) -> str:
    if p < 0:
        return ""
    row, col = _coord(p, n)
    return chr(97 + col) + chr(97 + row)


def ligne_colonne_vers_point(ligne: int, colonne: int, n: int) -> int:
    if not (1 <= ligne <= n and 1 <= colonne <= n):
        raise ErreurGo("coordonnée hors plateau")
    return (n - ligne) * n + (colonne - 1)

#!/usr/bin/env python3
"""regles.dames — les dames anglaises (8×8), prises obligatoires.

Le jeu est le **témoin des règles contraintes** : la prise est obligatoire, une
prise multiple est une séquence, et le perft est connu (7, 49, 302, 1469, 7361,
36768 depuis la position initiale). C'est ce qui rend la couche sémantique
mesurable : une notation `c3xe5xg7` n'est pas une chaîne, c'est un **chemin**
que les règles doivent valider.

Conventions (anglaises, documentées) :
- 32 cases jouables, numérotées 1..32 de haut en bas ; 1 = b8, 32 = g1 ;
- les noirs (b) commencent et descendent (vers les numéros croissants) ;
- les blancs (w) montent ; les dames (B/W) vont dans les deux sens ;
- un pion ne prend que vers l'avant ; une dame prend dans les quatre sens ;
- une prise est obligatoire ; une prise multiple est une seule action ;
- un pion qui atteint la dernière rangée par une prise est promu et **s'arrête**
  (règle anglaise) ; une dame continue sa prise.
"""
from __future__ import annotations

from typing import NamedTuple

from ..rsn import Annotation, RSN

VIDE = 0
NOIR_PION, BLANC_PION, NOIR_DAME, BLANC_DAME = 1, 2, 3, 4
NOIR, BLANC = 1, 2

_LETTRES = "abcdefgh"


def _coord(n: int) -> tuple[int, int]:
    """Numéro 1..32 → (rangée 0..7 depuis le haut, colonne 0..7)."""
    i = n - 1
    row, k = divmod(i, 4)
    offset = (row + 1) % 2
    return row, 2 * k + offset


def _num(row: int, col: int) -> int:
    offset = (row + 1) % 2
    if not (0 <= row < 8 and offset <= col < 8 and (col - offset) % 2 == 0):
        raise ValueError(f"case claire ou hors plateau : {row},{col}")
    k = (col - offset) // 2
    return row * 4 + k + 1


def indice_vers_case(i: int) -> str:
    row, col = _coord(i + 1)
    return _LETTRES[col] + str(8 - row)


def case_vers_indice(s: str) -> int:
    s = s.strip().lower()
    if len(s) != 2 or s[0] not in _LETTRES or s[1] not in "12345678":
        raise ValueError(f"case invalide : {s!r}")
    col = _LETTRES.index(s[0])
    row = 8 - int(s[1])
    return _num(row, col) - 1


def numero_vers_indice(n: int) -> int:
    if not 1 <= n <= 32:
        raise ValueError(f"numéro de case hors 1..32 : {n}")
    return n - 1


def indice_vers_numero(i: int) -> int:
    return i + 1


# Directions : 0 haut-gauche, 1 haut-droite, 2 bas-gauche, 3 bas-droite.
_DIRS = ((-1, -1), (1, -1), (-1, 1), (1, 1))
VOISINS: list[list[int | None]] = [[None] * 4 for _ in range(32)]
SAUTS: list[list[tuple[int, int] | None]] = [[None] * 4 for _ in range(32)]
MILEU: dict[tuple[int, int], int] = {}
for _i in range(32):
    _row, _col = _coord(_i + 1)
    for _d, (_dc, _dr) in enumerate(_DIRS):
        _c1, _r1 = _col + _dc, _row + _dr
        _c2, _r2 = _col + 2 * _dc, _row + 2 * _dr
        if 0 <= _c1 < 8 and 0 <= _r1 < 8 and (_c1 + _r1) % 2 == 1:
            _j = _num(_r1, _c1) - 1
            VOISINS[_i][_d] = _j
            if 0 <= _c2 < 8 and 0 <= _r2 < 8 and (_c2 + _r2) % 2 == 1:
                _k = _num(_r2, _c2) - 1
                SAUTS[_i][_d] = (_j, _k)
                MILEU[(_i, _k)] = _j


class Coup(NamedTuple):
    chemin: tuple[int, ...]

    @property
    def prise(self) -> bool:
        return len(self.chemin) > 2

    def numerique(self) -> str:
        sep = "x" if self.prise else "-"
        return sep.join(str(i + 1) for i in self.chemin)

    def algebrique(self) -> str:
        sep = "x" if self.prise else "-"
        return sep.join(indice_vers_case(i) for i in self.chemin)


class ErreurDames(ValueError):
    pass


def _promotion_row(couleur: int) -> int:
    # noir descend : rangée 7 (bas) ; blanc monte : rangée 0 (haut)
    return 7 if couleur == NOIR else 0


def _est_pion(case: int) -> bool:
    return case in (NOIR_PION, BLANC_PION)


def _couleur(case: int) -> int:
    return NOIR if case in (NOIR_PION, NOIR_DAME) else BLANC


class Position:
    __slots__ = ("cases", "trait", "demi")

    def __init__(self, cases: list[int], trait: int = NOIR, demi: int = 0) -> None:
        if len(cases) != 32:
            raise ErreurDames("le plateau doit avoir 32 cases jouables")
        self.cases = cases
        self.trait = trait
        self.demi = demi

    @classmethod
    def depart(cls) -> "Position":
        cases = [VIDE] * 32
        for i in range(12):
            cases[i] = NOIR_PION
        for i in range(20, 32):
            cases[i] = BLANC_PION
        return cls(cases, NOIR, 0)

    def copie(self) -> "Position":
        return Position(list(self.cases), self.trait, self.demi)

    # ---- génération ----------------------------------------------------
    def _directions(self, case: int) -> tuple[int, ...]:
        if case == NOIR_PION or case == BLANC_PION:
            return (2, 3) if _couleur(case) == NOIR else (0, 1)
        return (0, 1, 2, 3)

    def _captures_piece(self, cases: list[int], i: int, piece: int,
                        chemin: list[int], prises: list[int], sortie: list[Coup]) -> None:
        couleur = _couleur(piece)
        dame = piece in (NOIR_DAME, BLANC_DAME)
        prolonge = False
        for d in self._directions(piece):
            saut = SAUTS[i][d]
            if saut is None:
                continue
            over, landing = saut
            cible = cases[over]
            # on ne reprend jamais la même pièce ; la case d'arrivée peut avoir
            # déjà été visitée par une dame (le chemin reste fini).
            if cible == VIDE or _couleur(cible) == couleur or over in prises:
                continue
            if cases[landing] != VIDE:
                continue
            prolonge = True
            nouveau = list(cases)
            nouveau[over] = VIDE
            nouveau[i] = VIDE
            nouveau[landing] = piece
            nouvelle_chemin = chemin + [landing]
            nouvelles_prises = prises + [over]
            # promotion : un pion qui arrive au bout s'arrête (règle anglaise)
            if not dame and landing // 4 == _promotion_row(couleur):
                sortie.append(Coup(tuple(nouvelle_chemin)))
                continue
            self._captures_piece(nouveau, landing, piece, nouvelle_chemin,
                                 nouvelles_prises, sortie)
        # fin de séquence : on ne garde que les prises MAXIMALES (on doit
        # continuer tant qu'une prise est possible)
        if not prolonge and len(chemin) > 1:
            sortie.append(Coup(tuple(chemin)))

    def captures(self) -> list[Coup]:
        sortie: list[Coup] = []
        for i, piece in enumerate(self.cases):
            if piece == VIDE or _couleur(piece) != self.trait:
                continue
            self._captures_piece(list(self.cases), i, piece, [i], [], sortie)
        # déduplique (deux ordres de prises peuvent produire le même chemin)
        vus = set()
        uniques = []
        for c in sortie:
            if c.chemin not in vus:
                vus.add(c.chemin)
                uniques.append(c)
        return uniques

    def simples(self) -> list[Coup]:
        sortie = []
        for i, piece in enumerate(self.cases):
            if piece == VIDE or _couleur(piece) != self.trait:
                continue
            for d in self._directions(piece):
                j = VOISINS[i][d]
                if j is not None and self.cases[j] == VIDE:
                    sortie.append(Coup((i, j)))
        return sortie

    def coups_legaux(self) -> list[Coup]:
        caps = self.captures()
        if caps:
            return caps
        return self.simples()

    # ---- application ---------------------------------------------------
    def est_prise(self, coup: Coup) -> bool:
        """Une prise = un saut : le milieu du pas est occupé avant le coup."""
        for a, b in zip(coup.chemin, coup.chemin[1:]):
            over = MILEU.get((a, b))
            if over is not None and self.cases[over] != VIDE:
                return True
        return False

    def applique(self, coup: Coup) -> "Position":
        legal = self.coups_legaux()
        if coup not in legal:
            raise ErreurDames(f"coup illégal : {coup.numerique()}")
        return self._applique_direct(coup)

    def _applique_direct(self, coup: Coup) -> "Position":
        cases = list(self.cases)
        piece = cases[coup.chemin[0]]
        if piece == VIDE or _couleur(piece) != self.trait:
            raise ErreurDames("pas de pièce au trait sur la case de départ")
        # retire les pièces sautées
        for a, b in zip(coup.chemin, coup.chemin[1:]):
            over = MILEU.get((a, b))
            if over is not None:
                cases[over] = VIDE
        # déplace
        cases[coup.chemin[0]] = VIDE
        arrivee = coup.chemin[-1]
        cases[arrivee] = piece
        # promotion
        if _est_pion(piece) and arrivee // 4 == _promotion_row(_couleur(piece)):
            cases[arrivee] = NOIR_DAME if _couleur(piece) == NOIR else BLANC_DAME
        # compteur de nulle : 80 demi-coups sans prise ni promotion
        promotion = (_est_pion(piece)
                     and arrivee // 4 == _promotion_row(_couleur(piece)))
        if self.est_prise(coup) or promotion:
            demi = 0
        else:
            demi = self.demi + 1
        return Position(cases, BLANC if self.trait == NOIR else NOIR, demi)

    # ---- terminalité ---------------------------------------------------
    def terminal(self) -> bool:
        if self.demi >= 80:
            return True
        return not self.coups_legaux()

    def resultat(self) -> str | None:
        if self.demi >= 80:
            return "1/2-1/2"
        if not self.coups_legaux():
            return "0-1" if self.trait == NOIR else "1-0"
        return None

    def pieces(self, couleur: int | None = None) -> list[int]:
        return [p for p in self.cases if p != VIDE and (couleur is None or _couleur(p) == couleur)]

    def heuristique(self) -> float:
        """Matériel + avancement + défense de la rangée de fond, du point de vue du trait."""
        score = 0.0
        for i, p in enumerate(self.cases):
            if p == VIDE:
                continue
            coul = _couleur(p)
            v = 175.0 if p in (NOIR_DAME, BLANC_DAME) else 100.0
            if p in (NOIR_PION, BLANC_PION):
                av = (i // 4) if coul == NOIR else (7 - i // 4)
                v += av * 8.0
                # un pion de fond défend la promotion
                if (coul == NOIR and i // 4 == 0) or (coul == BLANC and i // 4 == 7):
                    v += 12.0
            score += v if coul == self.trait else -v
        return score

    def utilite(self) -> float:
        r = self.resultat()
        if r is not None:
            if r == "1/2-1/2":
                return 0.0
            gagnant = NOIR if r == "0-1" else BLANC
            return 100000.0 if gagnant == self.trait else -100000.0
        return self.heuristique()

    def cle(self) -> tuple:
        return tuple(self.cases), self.trait

    # ---- perft ---------------------------------------------------------
    def perft(self, profondeur: int) -> int:
        if profondeur <= 0:
            return 1
        coups = self.coups_legaux()
        if profondeur == 1:
            return len(coups)
        n = 0
        for c in coups:
            n += self._applique_direct(c).perft(profondeur - 1)
        return n


# ---------------------------------------------------------------------------
# RSN ⇄ position
# ---------------------------------------------------------------------------
_CAR_TO_INT = {"b": NOIR_PION, "w": BLANC_PION, "B": NOIR_DAME, "W": BLANC_DAME, ".": VIDE}
_INT_TO_CAR = {v: k for k, v in _CAR_TO_INT.items()}


def etat_initial() -> RSN:
    pos = Position.depart()
    return rsn_depuis_position(pos, Annotation(langue="notation", format="compact", surface=""))


def rsn_depuis_position(pos: Position, annotation: Annotation | None = None) -> RSN:
    corps = {"variante": "anglaise",
             "cases": [_INT_TO_CAR[p] for p in pos.cases],
             "trait": "b" if pos.trait == NOIR else "w",
             "demi": pos.demi}
    return RSN("dames", "etat", corps,
               annotation or Annotation(langue="notation", format="compact", surface=""))


def position_depuis_rsn(rsn: RSN, valide: bool = True) -> Position:
    c = rsn.corps
    cases = [_CAR_TO_INT[x] for x in c["cases"]]
    trait = NOIR if c.get("trait", "b") == "b" else BLANC
    pos = Position(cases, trait, int(c.get("demi", 0)))
    if valide:
        for i, p in enumerate(cases):
            if p == NOIR_PION and i // 4 == 7:
                raise ErreurDames("pion noir sur la rangée de promotion")
            if p == BLANC_PION and i // 4 == 0:
                raise ErreurDames("pion blanc sur la rangée de promotion")
        if not pos.pieces(NOIR) or not pos.pieces(BLANC):
            raise ErreurDames("un camp n'a plus de pièce")
    return pos


def action_depuis_coup(coup: Coup, annotation: Annotation | None = None) -> RSN:
    return RSN("dames", "coup", {"chemin": list(coup.chemin)},
               annotation or Annotation(langue="notation", format="numerique", surface=""))


def coup_depuis_action(rsn: RSN, pos: Position | None = None) -> Coup:
    c = Coup(tuple(int(x) for x in rsn.corps["chemin"]))
    if pos is not None and c not in pos.coups_legaux():
        raise ErreurDames(f"coup illégal : {c.numerique()}")
    return c


def partie_depuis_rsn(rsn: RSN) -> tuple[Position, list[Coup]]:
    pos = position_depuis_rsn(RSN("dames", "etat", dict(rsn.corps["depart"])))
    coups = []
    for a in rsn.corps.get("coups", []):
        c = coup_depuis_action(RSN("dames", "coup", dict(a)), pos)
        pos = pos.applique(c)
        coups.append(c)
    return pos, coups


def rsn_partie(depart: RSN, coups: list[Coup], annotation: Annotation | None = None) -> RSN:
    return RSN("dames", "partie",
               {"depart": dict(depart.corps), "coups": [action_depuis_coup(c).corps for c in coups]},
               annotation or Annotation(langue="notation", format="liste", surface=""))

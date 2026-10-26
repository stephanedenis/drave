#!/usr/bin/env python3
"""regles.echecs — les règles complètes des échecs, sans dépendance.

Ce module est l'**étage 2** des échecs : il ne connaît que la position interne
(64 cases, trait, droits, en passant) et il rend les coups **légaux**, la
terminalité, une évaluation et le perft. Les notations (FEN, SAN, UCI, français)
sont dans `codecs/echecs.py` ; elles s'appuient sur ce module pour valider, pas
l'inverse.

Choix de représentation :
- indice 0 = a8, 7 = h8, 56 = a1, 63 = h1 (l'ordre de la FEN, lisible) ;
- pièce = (couleur << 3) | type, type 1..6 = pion, cavalier, fou, tour, dame, roi ;
- coups = (de, vers, promotion, drapeau), drapeau 0 normal, 1 double, 2 en
  passant, 3 petit roque, 4 grand roque ;
- `joue`/`annule` avec un undo : le perft et la recherche ne copient pas le
  plateau à chaque nœud ;
- hachage de Zobrist incrémental, pour la table de transposition de la recherche.

Le contrôle de correction est le **perft** : les nombres de feuilles aux
profondeurs 1-4 des six positions de référence sont connus et vérifiés dans
`tests/test_echecs.py`. Une règle oubliée (roque, en passant, promotion) change
le nombre immédiatement.
"""
from __future__ import annotations

import random
import re
from typing import Iterable, NamedTuple

from ..rsn import Annotation, RSN

# ---------------------------------------------------------------------------
# Constantes et tables précalculées
# ---------------------------------------------------------------------------
VIDE, PION, CAVALIER, FOU, TOUR, DAME, ROI = range(7)
BLANC, NOIR = 0, 1
NORMAL, DOUBLE, EP, ROQUE_K, ROQUE_Q = range(5)

FICHIERS = "abcdefgh"

# Valeurs matérielles (centipions) et tables de cases simplifiées.
VALEURS = {PION: 100, CAVALIER: 320, FOU: 330, TOUR: 500, DAME: 900, ROI: 0}
# Bonus de centralisation pour les pièces légères, avancement des pions.
_CENTRE = [
    0, 0, 1, 2, 2, 1, 0, 0,
    0, 1, 2, 3, 3, 2, 1, 0,
    1, 2, 3, 4, 4, 3, 2, 1,
    2, 3, 4, 5, 5, 4, 3, 2,
    2, 3, 4, 5, 5, 4, 3, 2,
    1, 2, 3, 4, 4, 3, 2, 1,
    0, 1, 2, 3, 3, 2, 1, 0,
    0, 0, 1, 2, 2, 1, 0, 0,
]
_AVANCE = [0] * 64
for _i in range(64):
    _r, _c = divmod(_i, 8)
    _AVANCE[_i] = (7 - _r) if _r < 4 else _r  # avancement du pion (0 = rangée de départ)


def piece(couleur: int, typ: int) -> int:
    return (couleur << 3) | typ


def couleur(p: int) -> int:
    return p >> 3


def typ(p: int) -> int:
    return p & 7


def case_vers_indice(c: str) -> int:
    c = c.strip().lower()
    if len(c) != 2 or c[0] not in FICHIERS or c[1] not in "12345678":
        raise ValueError(f"case invalide : {c!r}")
    return (8 - int(c[1])) * 8 + FICHIERS.index(c[0])


def indice_vers_case(i: int) -> str:
    return FICHIERS[i % 8] + str(8 - i // 8)


def _coord(i: int) -> tuple[int, int]:
    return divmod(i, 8)


def _idx(r: int, c: int) -> int:
    return r * 8 + c


def _dans(r: int, c: int) -> bool:
    return 0 <= r < 8 and 0 <= c < 8


# Voisins d'un cavalier et d'un roi.
_SAUTS_C = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
_SAUTS_R = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
VOISINS_CAVALIER = [[] for _ in range(64)]
VOISINS_ROI = [[] for _ in range(64)]
for _i in range(64):
    _r, _c = _coord(_i)
    for _dr, _dc in _SAUTS_C:
        if _dans(_r + _dr, _c + _dc):
            VOISINS_CAVALIER[_i].append(_idx(_r + _dr, _c + _dc))
    for _dr, _dc in _SAUTS_R:
        if _dans(_r + _dr, _c + _dc):
            VOISINS_ROI[_i].append(_idx(_r + _dr, _c + _dc))

# Rayons : pour chaque case et chaque direction, la liste ordonnée des cases.
_DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
RAYONS = [[[] for _ in _DIRS] for _ in range(64)]
for _i in range(64):
    _r, _c = _coord(_i)
    for _d, (_dr, _dc) in enumerate(_DIRS):
        _rr, _cc = _r + _dr, _c + _dc
        while _dans(_rr, _cc):
            RAYONS[_i][_d].append(_idx(_rr, _cc))
            _rr += _dr
            _cc += _dc

# Pions : poussées et sources d'attaque.
POUSSE = [[None] * 64 for _ in range(2)]
DOUBLE_POUSSEE = [[None] * 64 for _ in range(2)]
CAPTURES = [[[] for _ in range(64)] for _ in range(2)]
ATTAQUE_PION = [[[] for _ in range(64)] for _ in range(2)]
for _i in range(64):
    _r, _c = _coord(_i)
    # Blancs : vers le haut (row - 1). Noirs : vers le bas (row + 1).
    if _r > 0:
        POUSSE[BLANC][_i] = _idx(_r - 1, _c)
    if _r == 6:
        DOUBLE_POUSSEE[BLANC][_i] = _idx(_r - 2, _c)
    if _r < 7:
        POUSSE[NOIR][_i] = _idx(_r + 1, _c)
    if _r == 1:
        DOUBLE_POUSSEE[NOIR][_i] = _idx(_r + 2, _c)
    for _dc in (-1, 1):
        if _dans(_r - 1, _c + _dc):
            CAPTURES[BLANC][_i].append(_idx(_r - 1, _c + _dc))
        if _dans(_r + 1, _c + _dc):
            CAPTURES[NOIR][_i].append(_idx(_r + 1, _c + _dc))
for _i in range(64):
    for _t in CAPTURES[BLANC][_i]:
        ATTAQUE_PION[BLANC][_t].append(_i)
    for _t in CAPTURES[NOIR][_i]:
        ATTAQUE_PION[NOIR][_t].append(_i)

# Droits de roque par case de tour.
_DROIT_TOUR = {63: 1, 56: 2, 7: 4, 0: 8}  # h1, a1, h8, a8

# Zobrist : déterministe, pour que deux exécutions donnent les mêmes nœuds.
_rng = random.Random(20261025)
Z_PIECE = [[_rng.getrandbits(64) for _ in range(64)] for _ in range(12)]
Z_ROQUE = [_rng.getrandbits(64) for _ in range(16)]
Z_EP = [_rng.getrandbits(64) for _ in range(64)]
Z_TRAIT = _rng.getrandbits(64)


def _zi(p: int) -> int:
    return (couleur(p) * 6) + (typ(p) - 1)


class Coup(NamedTuple):
    de: int
    vers: int
    promotion: int | None = None
    drapeau: int = NORMAL

    def uci(self) -> str:
        s = indice_vers_case(self.de) + indice_vers_case(self.vers)
        if self.promotion:
            s += "nbrq"[self.promotion - CAVALIER]
        return s


class ErreurEchecs(ValueError):
    pass


# ---------------------------------------------------------------------------
# Position
# ---------------------------------------------------------------------------
class Position:
    __slots__ = ("plateau", "trait", "roques", "ep", "demi", "plein", "rois", "hash")

    def __init__(self, plateau: list[int], trait: int = BLANC, roques: int = 0,
                 ep: int = -1, demi: int = 0, plein: int = 1) -> None:
        if len(plateau) != 64:
            raise ErreurEchecs("le plateau doit avoir 64 cases")
        self.plateau = plateau
        self.trait = trait
        self.roques = roques
        self.ep = ep
        self.demi = demi
        self.plein = plein
        self.rois = [-1, -1]
        for i, p in enumerate(plateau):
            if p and typ(p) == ROI:
                self.rois[couleur(p)] = i
        self.hash = self._hash_complet()

    # ---- construction / lecture ---------------------------------------
    @classmethod
    def depart(cls) -> "Position":
        return cls.depuis_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    @classmethod
    def depuis_fen(cls, fen: str, valide: bool = True) -> "Position":
        champs = fen.strip().split()
        if len(champs) < 4:
            raise ErreurEchecs(f"FEN incomplète : {fen!r}")
        placement, trait_s, roques_s, ep_s = champs[:4]
        demi = int(champs[4]) if len(champs) > 4 and champs[4].isdigit() else 0
        plein = int(champs[5]) if len(champs) > 5 and champs[5].isdigit() else 1
        plateau = [0] * 64
        lignes = placement.split("/")
        if len(lignes) != 8:
            raise ErreurEchecs(f"FEN : {len(lignes)} rangées au lieu de 8")
        for r, ligne in enumerate(lignes):
            c = 0
            for ch in ligne:
                if ch.isdigit():
                    c += int(ch)
                    if c > 8:
                        raise ErreurEchecs(f"FEN : rangée {r + 1} trop longue")
                elif ch in "pnbrqkPNBRQK":
                    if c >= 8:
                        raise ErreurEchecs(f"FEN : rangée {r + 1} trop longue")
                    coul = BLANC if ch.isupper() else NOIR
                    t = "pnbrqk".index(ch.lower()) + 1
                    plateau[_idx(r, c)] = piece(coul, t)
                    c += 1
                else:
                    raise ErreurEchecs(f"FEN : caractère inconnu {ch!r}")
            if c != 8:
                raise ErreurEchecs(f"FEN : rangée {r + 1} fait {c} cases")
        if trait_s not in ("w", "b"):
            raise ErreurEchecs(f"FEN : trait {trait_s!r}")
        trait = BLANC if trait_s == "w" else NOIR
        roques = 0
        for ch in roques_s:
            roques |= {"K": 1, "Q": 2, "k": 4, "q": 8}.get(ch, 0)
        ep = -1 if ep_s == "-" else case_vers_indice(ep_s)
        pos = cls(plateau, trait, roques, ep, demi, plein)
        if valide:
            if pos.rois[0] < 0 or pos.rois[1] < 0:
                raise ErreurEchecs("FEN : il manque un roi")
            # le roi qui n'est pas au trait ne peut pas être en échec
            if pos.est_attaque(pos.rois[1 - trait], trait):
                raise ErreurEchecs("FEN : le roi adverse est en échec, position illégale")
        return pos

    def copie(self) -> "Position":
        return Position(list(self.plateau), self.trait, self.roques, self.ep,
                        self.demi, self.plein)

    def fen(self) -> str:
        lignes = []
        for r in range(8):
            ligne = []
            vide = 0
            for c in range(8):
                p = self.plateau[_idx(r, c)]
                if not p:
                    vide += 1
                else:
                    if vide:
                        ligne.append(str(vide))
                        vide = 0
                    ch = "pnbrqk"[typ(p) - 1]
                    ligne.append(ch.upper() if couleur(p) == BLANC else ch)
            if vide:
                ligne.append(str(vide))
            lignes.append("".join(ligne))
        roques = "".join(ch for bit, ch in ((1, "K"), (2, "Q"), (4, "k"), (8, "q"))
                         if self.roques & bit) or "-"
        ep = indice_vers_case(self.ep) if self.ep >= 0 else "-"
        return f"{'/'.join(lignes)} {'w' if self.trait == BLANC else 'b'} {roques} {ep} {self.demi} {self.plein}"

    def _hash_complet(self) -> int:
        h = 0
        for i, p in enumerate(self.plateau):
            if p:
                h ^= Z_PIECE[_zi(p)][i]
        h ^= Z_ROQUE[self.roques]
        if self.ep >= 0:
            h ^= Z_EP[self.ep]
        if self.trait == NOIR:
            h ^= Z_TRAIT
        return h

    # ---- attaque / échec ----------------------------------------------
    def est_attaque(self, case: int, par: int) -> bool:
        """La case est-elle attaquée par la couleur `par` ?"""
        p = self.plateau
        # pions
        for src in ATTAQUE_PION[par][case]:
            q = p[src]
            if q and couleur(q) == par and typ(q) == PION:
                return True
        # cavaliers
        for src in VOISINS_CAVALIER[case]:
            q = p[src]
            if q and couleur(q) == par and typ(q) == CAVALIER:
                return True
        # roi
        for src in VOISINS_ROI[case]:
            q = p[src]
            if q and couleur(q) == par and typ(q) == ROI:
                return True
        # glissants
        for d, (dr, dc) in enumerate(_DIRS):
            for src in RAYONS[case][d]:
                q = p[src]
                if not q:
                    continue
                if couleur(q) == par:
                    t = typ(q)
                    if (d < 4 and t in (TOUR, DAME)) or (d >= 4 and t in (FOU, DAME)):
                        return True
                break
        return False

    def en_echec(self, coul: int) -> bool:
        r = self.rois[coul]
        return r >= 0 and self.est_attaque(r, 1 - coul)

    def roi_en_echec(self) -> bool:
        return self.en_echec(self.trait)

    # ---- génération ----------------------------------------------------
    def pseudo_coups(self) -> list[Coup]:
        p = self.plateau
        trait = self.trait
        adv = 1 - trait
        coups: list[Coup] = []
        for i, q in enumerate(p):
            if not q or couleur(q) != trait:
                continue
            t = typ(q)
            if t == PION:
                poussee = POUSSE[trait][i]
                if poussee is not None and p[poussee] == 0:
                    _ajoute_pion(coups, i, poussee, NORMAL)
                    dbl = DOUBLE_POUSSEE[trait][i]
                    if dbl is not None and p[dbl] == 0:
                        coups.append(Coup(i, dbl, None, DOUBLE))
                for cap in CAPTURES[trait][i]:
                    qc = p[cap]
                    if qc and couleur(qc) == adv:
                        _ajoute_pion(coups, i, cap, NORMAL)
                    elif cap == self.ep and self.ep >= 0:
                        derriere = self.ep + 8 if trait == BLANC else self.ep - 8
                        if 0 <= derriere < 64 and p[derriere] == piece(adv, PION):
                            coups.append(Coup(i, cap, None, EP))
            elif t == CAVALIER:
                for j in VOISINS_CAVALIER[i]:
                    qc = p[j]
                    if not qc or couleur(qc) == adv:
                        coups.append(Coup(i, j))
            elif t == FOU or t == TOUR or t == DAME:
                d0, d1 = (4, 8) if t == FOU else ((0, 4) if t == TOUR else (0, 8))
                for d in range(d0, d1):
                    for j in RAYONS[i][d]:
                        qc = p[j]
                        if not qc:
                            coups.append(Coup(i, j))
                        else:
                            if couleur(qc) == adv:
                                coups.append(Coup(i, j))
                            break
            elif t == ROI:
                for j in VOISINS_ROI[i]:
                    qc = p[j]
                    if not qc or couleur(qc) == adv:
                        coups.append(Coup(i, j))
                # roques
                if trait == BLANC:
                    if i == 60:
                        if (self.roques & 1 and p[61] == 0 and p[62] == 0
                                and p[63] == piece(BLANC, TOUR)
                                and not self.est_attaque(60, NOIR)
                                and not self.est_attaque(61, NOIR)
                                and not self.est_attaque(62, NOIR)):
                            coups.append(Coup(60, 62, None, ROQUE_K))
                        if (self.roques & 2 and p[59] == 0 and p[58] == 0 and p[57] == 0
                                and p[56] == piece(BLANC, TOUR)
                                and not self.est_attaque(60, NOIR)
                                and not self.est_attaque(59, NOIR)
                                and not self.est_attaque(58, NOIR)):
                            coups.append(Coup(60, 58, None, ROQUE_Q))
                else:
                    if i == 4:
                        if (self.roques & 4 and p[5] == 0 and p[6] == 0
                                and p[7] == piece(NOIR, TOUR)
                                and not self.est_attaque(4, BLANC)
                                and not self.est_attaque(5, BLANC)
                                and not self.est_attaque(6, BLANC)):
                            coups.append(Coup(4, 6, None, ROQUE_K))
                        if (self.roques & 8 and p[3] == 0 and p[2] == 0 and p[1] == 0
                                and p[0] == piece(NOIR, TOUR)
                                and not self.est_attaque(4, BLANC)
                                and not self.est_attaque(3, BLANC)
                                and not self.est_attaque(2, BLANC)):
                            coups.append(Coup(4, 2, None, ROQUE_Q))
        return coups

    def coups_legaux(self) -> list[Coup]:
        coul = self.trait
        adv = 1 - coul
        legal = []
        for c in self.pseudo_coups():
            u = self.joue(c)
            if not self.est_attaque(self.rois[coul], adv):
                legal.append(c)
            self.annule(u)
        return legal

    # ---- jouer / annuler ----------------------------------------------
    def joue(self, coup: Coup) -> tuple:
        de, vers, promo, drapeau = coup
        p = self.plateau
        q = p[de]
        if not q or couleur(q) != self.trait:
            raise ErreurEchecs(f"coup illégal : pas de pièce au trait en {indice_vers_case(de)}")
        coul = couleur(q)
        t = typ(q)
        capture = p[vers]
        capture_sq = vers
        if drapeau == EP:
            capture_sq = vers + 8 if coul == BLANC else vers - 8
            capture = p[capture_sq]
        undo = (coup, q, capture, capture_sq, self.roques, self.ep, self.demi,
                self.plein, self.rois[0], self.rois[1], self.hash)

        # plateau
        p[de] = 0
        p[vers] = q
        if drapeau == EP:
            p[capture_sq] = 0
        if promo:
            p[vers] = piece(coul, promo)
        if drapeau == ROQUE_K:
            if coul == BLANC:
                p[61], p[63] = p[63], 0
            else:
                p[5], p[7] = p[7], 0
        elif drapeau == ROQUE_Q:
            if coul == BLANC:
                p[59], p[56] = p[56], 0
            else:
                p[3], p[0] = p[0], 0

        # roi
        if t == ROI:
            self.rois[coul] = vers

        # droits de roque
        ancien_roques = self.roques
        if t == ROI:
            self.roques &= ~(3 if coul == BLANC else 12)
        if t == TOUR and de in _DROIT_TOUR:
            self.roques &= ~_DROIT_TOUR[de]
        if capture and typ(capture) == TOUR and capture_sq in _DROIT_TOUR:
            self.roques &= ~_DROIT_TOUR[capture_sq]

        # en passant
        ancien_ep = self.ep
        self.ep = (de + vers) // 2 if drapeau == DOUBLE else -1

        # compteurs
        if t == PION or capture:
            self.demi = 0
        else:
            self.demi += 1
        if coul == NOIR:
            self.plein += 1
        self.trait = 1 - coul

        # hachage incrémental
        h = self.hash
        h ^= Z_PIECE[_zi(q)][de]
        h ^= Z_PIECE[_zi(q)][vers]
        if promo:
            h ^= Z_PIECE[_zi(piece(coul, PION))][vers] ^ Z_PIECE[_zi(piece(coul, promo))][vers]
        if capture:
            h ^= Z_PIECE[_zi(capture)][capture_sq]
        if drapeau == ROQUE_K:
            rook = piece(coul, TOUR)
            if coul == BLANC:
                h ^= Z_PIECE[_zi(rook)][63] ^ Z_PIECE[_zi(rook)][61]
            else:
                h ^= Z_PIECE[_zi(rook)][7] ^ Z_PIECE[_zi(rook)][5]
        elif drapeau == ROQUE_Q:
            rook = piece(coul, TOUR)
            if coul == BLANC:
                h ^= Z_PIECE[_zi(rook)][56] ^ Z_PIECE[_zi(rook)][59]
            else:
                h ^= Z_PIECE[_zi(rook)][0] ^ Z_PIECE[_zi(rook)][3]
        h ^= Z_ROQUE[ancien_roques] ^ Z_ROQUE[self.roques]
        if ancien_ep >= 0:
            h ^= Z_EP[ancien_ep]
        if self.ep >= 0:
            h ^= Z_EP[self.ep]
        h ^= Z_TRAIT
        self.hash = h
        return undo

    def annule(self, undo: tuple) -> None:
        coup, q, capture, capture_sq, roques, ep, demi, plein, rw, rb, h = undo
        de, vers, promo, drapeau = coup
        p = self.plateau
        coul = couleur(q)
        p[de] = q
        p[vers] = 0
        if capture:
            p[capture_sq] = capture
        if drapeau == ROQUE_K:
            if coul == BLANC:
                p[63] = p[61]; p[61] = 0
            else:
                p[7] = p[5]; p[5] = 0
        elif drapeau == ROQUE_Q:
            if coul == BLANC:
                p[56] = p[59]; p[59] = 0
            else:
                p[0] = p[3]; p[3] = 0
        self.trait = coul
        self.roques = roques
        self.ep = ep
        self.demi = demi
        self.plein = plein
        self.rois[0] = rw
        self.rois[1] = rb
        self.hash = h

    # ---- terminalité et évaluation ------------------------------------
    def terminal(self) -> bool:
        if self.demi >= 100:
            return True
        if self.insuffisant():
            return True
        return not self.coups_legaux()

    def insuffisant(self) -> bool:
        pieces = [typ(p) for p in self.plateau if p]
        if any(t in (PION, TOUR, DAME) for t in pieces):
            return False
        if pieces.count(CAVALIER) + pieces.count(FOU) <= 1:
            return True
        # deux fous du même camp sur des couleurs opposées : mat possible en théorie,
        # mais on ne prétend pas trancher ici ; on ne déclare pas nulle.
        return False

    def resultat(self) -> str | None:
        if not self.coups_legaux():
            if self.en_echec(self.trait):
                return "0-1" if self.trait == BLANC else "1-0"
            return "1/2-1/2"
        if self.demi >= 100 or self.insuffisant():
            return "1/2-1/2"
        return None

    def heuristique(self) -> float:
        """Évaluation statique, du point de vue du trait (centipions)."""
        score = 0
        for i, p in enumerate(self.plateau):
            if not p:
                continue
            t = typ(p)
            v = VALEURS[t]
            if t in (CAVALIER, FOU):
                v += _CENTRE[i] * 4
            elif t == PION:
                r = i // 8
                av = (6 - r) if couleur(p) == BLANC else (r - 1)
                v += max(0, min(5, av)) * 5
            elif t == ROI:
                # le roi vaut cher au centre en finale, mais on garde simple
                v += _CENTRE[i] * 2
            if couleur(p) == BLANC:
                score += v
            else:
                score -= v
        return float(score if self.trait == BLANC else -score)

    def utilite(self) -> float:
        res = self.resultat()
        if res is not None:
            if res == "1/2-1/2":
                return 0.0
            gagnant = BLANC if res == "1-0" else NOIR
            return 100000.0 if gagnant == self.trait else -100000.0
        return self.heuristique()

    def cle(self) -> int:
        return self.hash

    # ---- perft ---------------------------------------------------------
    def perft(self, profondeur: int) -> int:
        if profondeur <= 0:
            return 1
        legal = self.coups_legaux()
        if profondeur == 1:
            return len(legal)
        n = 0
        for c in legal:
            u = self.joue(c)
            n += self.perft(profondeur - 1)
            self.annule(u)
        return n

    # ---- SAN -----------------------------------------------------------
    def san(self, coup: Coup) -> str:
        de, vers, promo, drapeau = coup
        if drapeau == ROQUE_K:
            s = "O-O"
        elif drapeau == ROQUE_Q:
            s = "O-O-O"
        else:
            p = self.plateau[de]
            t = typ(p)
            prise = self.plateau[vers] != 0 or drapeau == EP
            if t == PION:
                s = (FICHIERS[de % 8] + "x" if prise else "") + indice_vers_case(vers)
                if promo:
                    s += "=" + "NBRQ"[promo - CAVALIER]
            else:
                s = {ROI: "K", DAME: "Q", TOUR: "R", FOU: "B", CAVALIER: "N"}[t]
                autres = [m for m in self.coups_legaux()
                          if m != coup and typ(self.plateau[m.de]) == t and m.vers == vers]
                if autres:
                    meme_fichier = any(m.de % 8 == de % 8 for m in autres)
                    meme_rangee = any(m.de // 8 == de // 8 for m in autres)
                    if not meme_fichier:
                        s += FICHIERS[de % 8]
                    elif not meme_rangee:
                        s += str(8 - de // 8)
                    else:
                        s += indice_vers_case(de)
                if prise:
                    s += "x"
                s += indice_vers_case(vers)
        # échec / mat
        u = self.joue(coup)
        adverse = self.trait
        if self.en_echec(adverse):
            if not self.coups_legaux():
                s += "#"
            else:
                s += "+"
        self.annule(u)
        return s

    def parse_san(self, texte: str, niveau: int = 4) -> tuple[Coup | None, list[Coup], list[str]]:
        """Lit un SAN ; rend (coup, candidats, ambiguïtés).

        Sans position, un SAN n'a pas de sens : c'est la position qui dit si
        `Cf3` est légal, si `R` est le roi français ou la tour anglaise. Le
        parsing est donc **contextuel** — et c'est précisément ce que le niveau 4
        ajoute au niveau 3.
        """
        amb: list[str] = []
        t = texte.strip()
        t = t.replace("0-0-0", "O-O-O").replace("0-0", "O-O")
        t = re.sub(r"e\.p\.?", "", t, flags=re.I)
        t = re.sub(r"[+#!?]+$", "", t)
        t = t.rstrip(". ")
        if t in ("O-O", "OO", "o-o"):
            cands = [c for c in self.coups_legaux() if c.drapeau == ROQUE_K]
            return (cands[0] if len(cands) == 1 else None), cands, ([] if cands else ["petit roque illégal"])
        if t in ("O-O-O", "OOO", "o-o-o"):
            cands = [c for c in self.coups_legaux() if c.drapeau == ROQUE_Q]
            return (cands[0] if len(cands) == 1 else None), cands, ([] if cands else ["grand roque illégal"])

        # Une capture de pion écrite en minuscules (`dxe5`, `bxc3`) commence
        # par une lettre qui est AUSSI une lettre de pièce (`D`, `B`, `C`, `F`).
        # On la traite comme un pion AVANT la lecture de pièce, sinon `dxe5`
        # deviendrait une dame française. Le SAN de pièce est en majuscule.
        m_pion = re.fullmatch(r"([a-h])x([a-h][1-8])(?:=?([QRBN]))?", t, flags=re.I)
        if m_pion and t[:1].islower():
            fich_p, dest_p, promo_p = m_pion.group(1), m_pion.group(2), m_pion.group(3)
            promo = None
            if promo_p:
                promo = "NBRQ".index(promo_p.upper()) + CAVALIER
            cands_p = [c for c in self.coups_legaux()
                       if typ(self.plateau[c.de]) == PION and c.vers == case_vers_indice(dest_p)
                       and c.de % 8 == FICHIERS.index(fich_p.lower())
                       and (self.plateau[c.vers] or c.drapeau == EP)
                       and (promo is None or c.promotion == promo)]
            if len(cands_p) == 1:
                return cands_p[0], cands_p, amb
            if cands_p:
                return None, cands_p, amb + ["capture de pion ambiguë"]

        m = re.fullmatch(r"([KQRBNCDTF])?([a-h])?([1-8])?x?([a-h][1-8])(?:=?([QRBNCDTF]))?", t,
                         flags=re.I)
        if not m:
            return None, [], [f"SAN illisible : {texte!r}"]
        lettre, fich, rang, dest_s, promo_s = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        lettre = lettre.upper() if lettre else None
        dest = case_vers_indice(dest_s)
        prise = "x" in t.lower()
        promo = None
        if promo_s:
            promo = "NBRQ".index(promo_s.upper()) + CAVALIER if promo_s.upper() in "NBRQ" else None
            if promo is None:
                return None, [], [f"promotion inconnue : {promo_s!r}"]

        def filtre(types: list[int]) -> list[Coup]:
            out = []
            for c in self.coups_legaux():
                p = self.plateau[c.de]
                if typ(p) not in types or c.vers != dest:
                    continue
                if fich and c.de % 8 != FICHIERS.index(fich.lower()):
                    continue
                if rang and c.de // 8 != 8 - int(rang):
                    continue
                if prise and not (self.plateau[c.vers] or c.drapeau == EP):
                    continue
                if promo is not None and c.promotion != promo:
                    continue
                if promo is None and c.promotion is not None:
                    continue
                out.append(c)
            return out

        # L'anglais d'abord : `R` est la tour, `B` le fou, `N` le cavalier. Si
        # aucune pièce anglaise ne peut jouer, on essaie les lettres françaises
        # (`R` roi, `D` dame, `T` tour, `F` fou, `C` cavalier).
        anglais = {"K": [ROI], "Q": [DAME], "R": [TOUR], "B": [FOU],
                   "N": [CAVALIER], "P": [PION]}
        francais = {"R": [ROI], "D": [DAME], "T": [TOUR], "F": [FOU],
                    "C": [CAVALIER]}
        if lettre is None:
            cands = filtre([PION])
        else:
            cands = filtre(anglais.get(lettre, []))
            if not cands:
                cands = filtre(francais.get(lettre, []))
        if len(cands) == 1:
            return cands[0], cands, amb
        if not cands:
            # Une promotion omise est fréquente : on propose les quatre, en
            # annotant l'ambiguïté (le niveau 4 refusera de choisir seul).
            if lettre is None:
                for c in self.coups_legaux():
                    if typ(self.plateau[c.de]) == PION and c.vers == dest and c.promotion:
                        cands.append(c)
                if len(cands) == 1:
                    return cands[0], cands, amb
                if cands:
                    return None, cands, amb + ["promotion non précisée"]
            return None, [], [f"SAN illégal dans cette position : {texte!r}"]
        return None, cands, amb + ["coup ambigu (désambiguïsation insuffisante)"]

    def parse_uci(self, texte: str) -> tuple[Coup | None, list[Coup], list[str]]:
        m = re.fullmatch(r"\s*([a-h][1-8])[- ]?([a-h][1-8])([nbrqNBRQ])?\s*", texte)
        if not m:
            return None, [], [f"UCI illisible : {texte!r}"]
        de = case_vers_indice(m.group(1))
        vers = case_vers_indice(m.group(2))
        promo = None
        if m.group(3):
            promo = "NBRQ".index(m.group(3).upper()) + CAVALIER
        cands = [c for c in self.coups_legaux()
                 if c.de == de and c.vers == vers and
                 (promo is None or c.promotion == promo)]
        if len(cands) == 1:
            return cands[0], cands, []
        if not cands:
            return None, [], [f"UCI illégal dans cette position : {texte!r}"]
        return None, cands, ["promotion non précisée"]


def _ajoute_pion(coups: list[Coup], de: int, vers: int, drapeau: int) -> None:
    r = vers // 8
    if r == 0 or r == 7:
        for promo in (DAME, TOUR, FOU, CAVALIER):
            coups.append(Coup(de, vers, promo, drapeau))
    else:
        coups.append(Coup(de, vers, None, drapeau))


# ---------------------------------------------------------------------------
# RSN ⇄ position
# ---------------------------------------------------------------------------
def etat_initial() -> RSN:
    pos = Position.depart()
    return rsn_depuis_position(pos, Annotation(langue="notation", format="fen", surface=""))


def rsn_depuis_position(pos: Position, annotation: Annotation | None = None) -> RSN:
    corps = {
        "plateau": pos.fen().split()[0],
        "trait": "w" if pos.trait == BLANC else "b",
        "roques": "".join(ch for bit, ch in ((1, "K"), (2, "Q"), (4, "k"), (8, "q"))
                          if pos.roques & bit) or "-",
        "ep": indice_vers_case(pos.ep) if pos.ep >= 0 else None,
        "demi": pos.demi,
        "plein": pos.plein,
    }
    return RSN("echecs", "etat", corps,
               annotation or Annotation(langue="notation", format="fen", surface=""))


def position_depuis_rsn(rsn: RSN, valide: bool = True) -> Position:
    c = rsn.corps
    roques = c.get("roques") or "-"
    ep = c.get("ep") or "-"
    fen = f"{c['plateau']} {c['trait']} {roques} {ep} {int(c.get('demi', 0))} {int(c.get('plein', 1))}"
    return Position.depuis_fen(fen, valide=valide)


def action_depuis_coup(coup: Coup, annotation: Annotation | None = None) -> RSN:
    corps = {
        "de": coup.de,
        "vers": coup.vers,
        "promotion": {CAVALIER: "n", FOU: "b", TOUR: "r", DAME: "q"}.get(coup.promotion),
        "roque": {ROQUE_K: "K", ROQUE_Q: "Q"}.get(coup.drapeau),
    }
    return RSN("echecs", "coup", corps,
               annotation or Annotation(langue="notation", format="uci", surface=""))


def coup_depuis_action(rsn: RSN, pos: Position | None = None) -> Coup:
    c = rsn.corps
    de, vers = int(c["de"]), int(c["vers"])
    promo = {"n": CAVALIER, "b": FOU, "r": TOUR, "q": DAME}.get(c.get("promotion") or "")
    roque = c.get("roque")
    if pos is not None:
        for m in pos.coups_legaux():
            if roque and m.drapeau == (ROQUE_K if roque == "K" else ROQUE_Q):
                return m
            if m.de == de and m.vers == vers and (promo is None or m.promotion == promo):
                return m
        raise ErreurEchecs(f"coup illégal : {de}→{vers}")
    drapeau = ROQUE_K if roque == "K" else ROQUE_Q if roque == "Q" else NORMAL
    return Coup(de, vers, promo, drapeau)


def partie_depuis_rsn(rsn: RSN, valide: bool = True) -> tuple[Position, list[Coup]]:
    c = rsn.corps
    depart = RSN("echecs", "etat", dict(c["depart"]))
    pos = position_depuis_rsn(depart, valide=valide)
    coups = []
    for a in c.get("coups", []):
        coup = coup_depuis_action(RSN("echecs", "coup", dict(a)), pos)
        pos.joue(coup)
        coups.append(coup)
    return pos, coups


def rsn_partie(depart: RSN, coups: list[Coup], annotation: Annotation | None = None) -> RSN:
    corps = {"depart": dict(depart.corps),
             "coups": [action_depuis_coup(c).corps for c in coups]}
    return RSN("echecs", "partie", corps,
               annotation or Annotation(langue="notation", format="pgn", surface=""))

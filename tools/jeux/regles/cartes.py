#!/usr/bin/env python3
"""regles.cartes — le whist : 4 joueurs, 52 cartes, 13 plis, un atout.

Le whist est le **témoin des jeux de cartes** : information imparfaite (on ne
voit que sa main), obligation de fournir la couleur demandée, et une résolution
de pli qui dépend de l'atout. L'étage 2 n'y fait pas de recherche exhaustive
(l'information est cachée) : il applique une **politique** lisible, et la mesure
compare cette politique à un joueur aléatoire sur des donnes reproductibles.

Conventions :
- joueurs 0=N, 1=E, 2=S, 3=W ; équipes 0-2 (N-S) et 1-3 (E-W) ;
- carte = (rang − 2) × 4 + couleur, rang 2..14 (14=As), couleur 0=C,1=D,2=H,3=S ;
- à l'entame, on mène n'importe quelle carte ; ensuite on **fournit** la couleur
  demandée si on l'a, sinon on défausse ou on coupe ;
- le pli est gagné par le plus haut atout joué, sinon par la plus haute carte de
  la couleur demandée ;
- le gagnant entame le pli suivant ; 13 plis, l'équipe qui en gagne le plus gagne.
"""
from __future__ import annotations

import random
from typing import NamedTuple

from ..rsn import Annotation, RSN

NOMS_JOUEURS = ("N", "E", "S", "W")
NOMS_EQUIPES = ("N-S", "E-W")
COULEURS = ("C", "D", "H", "S")  # trèfle, carreau, cœur, pique
NOMS_COULEURS_FR = ("trèfle", "carreau", "cœur", "pique")
NOMS_COULEURS_EN = ("club", "diamond", "heart", "spade")


class ErreurCartes(ValueError):
    pass


def rang(carte: int) -> int:
    return carte // 4 + 2


def couleur(carte: int) -> int:
    return carte % 4


def carte_id(r: int, c: int) -> int:
    if not (2 <= r <= 14 and 0 <= c <= 3):
        raise ErreurCartes(f"carte invalide : rang {r}, couleur {c}")
    return (r - 2) * 4 + c


def equipe(joueur: int) -> int:
    return joueur % 2


def partenaire(joueur: int) -> int:
    return (joueur + 2) % 4


def nom_carte(carte: int, langue: str = "fr") -> str:
    rangs_fr = {14: "as", 13: "roi", 12: "dame", 11: "valet", 10: "dix",
                9: "neuf", 8: "huit", 7: "sept", 6: "six", 5: "cinq",
                4: "quatre", 3: "trois", 2: "deux"}
    rangs_en = {14: "ace", 13: "king", 12: "queen", 11: "jack", 10: "ten",
                9: "nine", 8: "eight", 7: "seven", 6: "six", 5: "five",
                4: "four", 3: "three", 2: "two"}
    if langue == "en":
        return f"{rangs_en[rang(carte)]} of {NOMS_COULEURS_EN[couleur(carte)]}s"
    return f"{rangs_fr[rang(carte)]} de {NOMS_COULEURS_FR[couleur(carte)]}"


def nom_court(carte: int) -> str:
    r = rang(carte)
    lettre = {14: "A", 13: "K", 12: "Q", 11: "J", 10: "T"}.get(r, str(r))
    return lettre + COULEURS[couleur(carte)]


def _symbole(carte: int) -> str:
    return "A23456789TJQK"[rang(carte)] + COULEURS[couleur(carte)]


class Position:
    __slots__ = ("mains", "atout", "donneur", "entameur", "tour", "pli", "plis")

    def __init__(self, mains: list[list[int]], atout: int = -1, donneur: int = 0,
                 entameur: int = 0, tour: int = 0, pli: list[list[int]] | None = None,
                 plis: list[int] | None = None) -> None:
        if len(mains) != 4:
            raise ErreurCartes("il faut quatre mains")
        self.mains = [sorted(m) for m in mains]
        self.atout = atout
        self.donneur = donneur
        self.entameur = entameur
        self.tour = tour
        self.pli = [list(x) for x in (pli or [])]
        self.plis = list(plis or [0, 0])
        # une carte ne peut être que dans une main ou dans le pli
        vues = [c for m in self.mains for c in m] + [c for _, c in self.pli]
        if len(vues) != len(set(vues)):
            raise ErreurCartes("carte en double")
        for c in vues:
            if not 0 <= c < 52:
                raise ErreurCartes(f"carte hors jeu : {c}")
        if len(self.pli) > 4:
            raise ErreurCartes("un pli a plus de quatre cartes")
        if self.tour not in range(4) or self.entameur not in range(4):
            raise ErreurCartes("joueur hors 0..3")

    @classmethod
    def depart(cls, graine: int = 0, atout: int | None = None) -> "Position":
        rng = random.Random(graine)
        deck = list(range(52))
        rng.shuffle(deck)
        mains = [sorted(deck[i * 13:(i + 1) * 13]) for i in range(4)]
        at = (graine // 7) % 4 if atout is None else atout
        donneur = graine % 4
        entameur = (donneur + 1) % 4
        return cls(mains, at, donneur, entameur, entameur, [], [0, 0])

    def copie(self) -> "Position":
        return Position([list(m) for m in self.mains], self.atout, self.donneur,
                        self.entameur, self.tour, self.pli, self.plis)

    # ---- règles --------------------------------------------------------
    def couleur_demandee(self) -> int | None:
        return couleur(self.pli[0][1]) if self.pli else None

    def coups_legaux(self) -> list[int]:
        main = self.mains[self.tour]
        if not main:
            return []
        if not self.pli:
            return list(main)
        demandee = self.couleur_demandee()
        meme = [c for c in main if couleur(c) == demandee]
        return meme if meme else list(main)

    def coup_legal(self, carte: int) -> bool:
        return carte in self.coups_legaux()

    def gagnant_pli(self, pli: list[list[int]] | None = None) -> int:
        pli = self.pli if pli is None else pli
        if not pli:
            raise ErreurCartes("pli vide")
        demandee = couleur(pli[0][1])
        meilleur_joueur, meilleure = pli[0]
        meilleur_atout = self.atout >= 0 and couleur(meilleure) == self.atout
        for j, c in pli[1:]:
            est_atout = self.atout >= 0 and couleur(c) == self.atout
            if est_atout and not meilleur_atout:
                meilleur_joueur, meilleure, meilleur_atout = j, c, True
            elif est_atout == meilleur_atout and couleur(c) == (self.atout if est_atout else demandee):
                if rang(c) > rang(meilleure):
                    meilleur_joueur, meilleure = j, c
        return meilleur_joueur

    def gagne_avec(self, carte: int) -> bool:
        """La carte, jouée maintenant, gagnerait-elle le pli tel qu'il est ?"""
        return self.gagnant_pli(self.pli + [[self.tour, carte]]) == self.tour

    def joue(self, carte: int) -> "Position":
        if not self.coup_legal(carte):
            raise ErreurCartes(f"coup illégal : {nom_court(carte)}")
        mains = [list(m) for m in self.mains]
        mains[self.tour].remove(carte)
        pli = [list(x) for x in self.pli] + [[self.tour, carte]]
        plis = list(self.plis)
        tour = (self.tour + 1) % 4
        entameur = self.entameur
        if len(pli) == 4:
            gagnant = self.gagnant_pli(pli)
            plis[equipe(gagnant)] += 1
            tour = gagnant
            entameur = gagnant
            pli = []
        return Position(mains, self.atout, self.donneur, entameur, tour, pli, plis)

    def terminal(self) -> bool:
        return all(not m for m in self.mains) and not self.pli

    def resultat(self) -> str | None:
        if not self.terminal():
            return None
        if self.plis[0] > self.plis[1]:
            return "N-S"
        if self.plis[1] > self.plis[0]:
            return "E-W"
        return "égalité"

    def utilite(self) -> float:
        """Du point de vue de l'équipe du joueur au trait : différence de plis."""
        e = equipe(self.tour)
        return float(self.plis[e] - self.plis[1 - e])

    def heuristique(self) -> float:
        return self.utilite()

    def cle(self) -> tuple:
        return (tuple(tuple(m) for m in self.mains), self.atout, self.tour,
                tuple(tuple(x) for x in self.pli), tuple(self.plis))

    # ---- politique (l'étage 2 des cartes) ------------------------------
    def politique(self) -> int:
        """Une politique lisible : fournir, ne pas surjouer le partenaire, tenter
        de gagner au plus bas. Elle ne regarde JAMAIS les mains adverses."""
        legal = self.coups_legaux()
        if len(legal) == 1:
            return legal[0]
        if not self.pli:
            # entame : la couleur la plus longue hors atout, la plus haute carte
            couleurs: dict[int, list[int]] = {}
            for c in legal:
                couleurs.setdefault(couleur(c), []).append(c)
            choisies = [s for s in couleurs if s != self.atout] or list(couleurs)
            s = max(choisies, key=lambda x: (len(couleurs[x]), -x))
            return max(couleurs[s], key=rang)
        # on suit : le partenaire gagne-t-il déjà ?
        gagnant = self.gagnant_pli()
        if gagnant == partenaire(self.tour):
            return min(legal, key=rang)
        # tenter de gagner, au plus bas
        gagnants = [c for c in legal if self.gagne_avec(c)]
        if gagnants:
            return min(gagnants, key=rang)
        return min(legal, key=rang)


# ---------------------------------------------------------------------------
# RSN ⇄ position
# ---------------------------------------------------------------------------
def etat_initial(graine: int = 0, atout: int | None = None) -> RSN:
    pos = Position.depart(graine, atout)
    return rsn_depuis_position(pos, Annotation(langue="notation", format="donne", surface=""))


def rsn_depuis_position(pos: Position, annotation: Annotation | None = None) -> RSN:
    corps = {
        "jeu": "whist",
        "atout": COULEURS[pos.atout] if pos.atout >= 0 else None,
        "donneur": pos.donneur,
        "entameur": pos.entameur,
        "tour": pos.tour,
        "mains": [list(m) for m in pos.mains],
        "pli": [list(x) for x in pos.pli],
        "plis": list(pos.plis),
    }
    return RSN("cartes", "etat", corps,
               annotation or Annotation(langue="notation", format="donne", surface=""))


def position_depuis_rsn(rsn: RSN, valide: bool = True) -> Position:
    c = rsn.corps
    if c.get("jeu", "whist") != "whist":
        raise ErreurCartes(f"jeu de cartes non pris en charge : {c.get('jeu')!r}")
    atout = -1 if c.get("atout") is None else COULEURS.index(c["atout"])
    pos = Position([list(m) for m in c["mains"]], atout, int(c.get("donneur", 0)),
                   int(c.get("entameur", 0)), int(c.get("tour", 0)),
                   [list(x) for x in c.get("pli", [])], [int(x) for x in c.get("plis", [0, 0])])
    if valide and not pos.terminal():
        if not pos.mains[pos.tour]:
            raise ErreurCartes("le joueur au trait n'a plus de carte")
    return pos


def action_depuis_carte(carte: int, annotation: Annotation | None = None) -> RSN:
    return RSN("cartes", "coup", {"carte": carte},
               annotation or Annotation(langue="notation", format="carte", surface=""))


def carte_depuis_action(rsn: RSN, pos: Position | None = None) -> int:
    c = int(rsn.corps["carte"])
    if not 0 <= c < 52:
        raise ErreurCartes(f"carte hors jeu : {c}")
    if pos is not None and not pos.coup_legal(c):
        raise ErreurCartes(f"coup illégal : {nom_court(c)}")
    return c


def partie_depuis_rsn(rsn: RSN) -> tuple[Position, list[int]]:
    pos = position_depuis_rsn(RSN("cartes", "etat", dict(rsn.corps["depart"])))
    coups = []
    for a in rsn.corps.get("coups", []):
        c = carte_depuis_action(RSN("cartes", "coup", dict(a)), pos)
        pos = pos.joue(c)
        coups.append(c)
    return pos, coups


def rsn_partie(depart: RSN, coups: list[int], annotation: Annotation | None = None) -> RSN:
    return RSN("cartes", "partie",
               {"depart": dict(depart.corps), "coups": [action_depuis_carte(c).corps for c in coups]},
               annotation or Annotation(langue="notation", format="liste", surface=""))

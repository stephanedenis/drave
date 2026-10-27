#!/usr/bin/env python3
"""sequences.py — des parties jouées par les règles, pour M3/M5/M8.

Chaque pas porte : le code typé, la surface canonique, le contexte (résumé) et
la RSN. Les parties sont déterministes pour une graine donnée.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from jeux.codecs import codec
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G
from jeux.regles import morpion as M
from jeux.rsn import RSN
from semantique.universaux import code_rsn, resume_contexte


@dataclass(frozen=True)
class Pas:
    jeu: str
    code: dict
    surface: str
    contexte: str
    rsn: RSN


@dataclass(frozen=True)
class Sequence:
    jeu: str
    pas: tuple[Pas, ...]


def _surface(jeu: str, rsn: RSN, contexte, fmt: str) -> str:
    try:
        return codec(jeu).rend(rsn, format=fmt, contexte=contexte)
    except Exception:
        return ""


def _echecs(rng: random.Random, n: int) -> Sequence:
    pos = E.Position.depart()
    pas = []
    for _ in range(n):
        coups = pos.coups_legaux()
        if not coups:
            break
        c = rng.choice(coups)
        ctx = E.rsn_depuis_position(pos)
        r = E.action_depuis_coup(c)
        pas.append(Pas("echecs", code_rsn(r), _surface("echecs", r, ctx, "san"),
                       resume_contexte(ctx), r))
        pos.joue(c)
    return Sequence("echecs", tuple(pas))


def _dames(rng: random.Random, n: int) -> Sequence:
    pos = D.Position.depart()
    pas = []
    for _ in range(n):
        coups = pos.coups_legaux()
        if not coups:
            break
        c = rng.choice(coups)
        ctx = D.rsn_depuis_position(pos)
        r = D.action_depuis_coup(c)
        pas.append(Pas("dames", code_rsn(r), _surface("dames", r, ctx, "numerique"),
                       resume_contexte(ctx), r))
        pos = pos.applique(c)
    return Sequence("dames", tuple(pas))


def _go(rng: random.Random, n: int) -> Sequence:
    pos = G.Position.depart(9, 65)
    pas = []
    for _ in range(n):
        coups = pos.coups_legaux()
        p = rng.choice(coups) if coups and rng.random() > 0.1 else None
        ctx = pos.vers_rsn()
        r = RSN("go", "coup", {"taille": 9, "passe": True} if p is None else {"taille": 9, "point": p})
        pas.append(Pas("go", code_rsn(r), _surface("go", r, ctx, "gtp"),
                       resume_contexte(ctx), r))
        pos = pos.joue(p)
    return Sequence("go", tuple(pas))


def _morpion(rng: random.Random, n: int) -> Sequence:
    etat = M.etat_initial()
    pas = []
    for _ in range(min(n, 9)):
        coups = M.coups_legaux(etat)
        if not coups:
            break
        c = rng.choice(coups)
        ctx = etat
        pas.append(Pas("morpion", code_rsn(c), _surface("morpion", c, ctx, "cellule"),
                       resume_contexte(ctx), c))
        etat = M.applique(etat, c)
    return Sequence("morpion", tuple(pas))


def partie(jeu: str, graine: int = 0, n: int = 12) -> Sequence:
    rng = random.Random(graine)
    return {"echecs": _echecs, "dames": _dames, "go": _go, "morpion": _morpion}[jeu](rng, n)


def corpus(graine: int = 0, parties_par_jeu: int = 40, n: int = 12) -> list[Sequence]:
    out = []
    for k, jeu in enumerate(("echecs", "dames", "go", "morpion")):
        for i in range(parties_par_jeu):
            out.append(partie(jeu, graine + 1000 * k + i, n))
    return out

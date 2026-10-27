#!/usr/bin/env python3
"""synth_corpus.py — des surfaces synthétiques multilingues, labels RSN exacts.

Le codec classique est le professeur : on génère des surfaces à partir des
règles (coups légaux, cartes, points) et des libellés multilingues, puis on
entraîne le natif à lire ces surfaces. Les surfaces **réelles** B5/B7 ne sont
jamais utilisées à l'entraînement : elles servent de test de transfert.
"""
from __future__ import annotations

from dataclasses import dataclass

from jeux.lexique_multilingue import MULTI
from jeux.regles import cartes as C
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G
from jeux.regles import morpion as M
from jeux.rsn import RSN
from semantique.typed_corpus import ItemType
from semantique.universaux import code_rsn, resume_contexte

PIECES = ("P", "N", "B", "R", "Q", "K")
LETTRES_DAMES = "abcdefgh"


def _forme(concept: str, langue: str) -> str | None:
    f = MULTI.formes(concept, langue)
    return f[0] if f else None


def _item(texte: str, r: RSN, langue: str, paire: str, fmt: str = "synthetique",
          contexte: str = "") -> ItemType:
    return ItemType(texte, code_rsn(r), r.jeu, r.nature, langue, paire, fmt, contexte)


def items_synth() -> list[ItemType]:
    out: list[ItemType] = []
    langues = MULTI.langues
    # --- échecs : tous les coups légaux du départ, 3 formes ---
    ctx_e = resume_contexte(E.rsn_depuis_position(E.Position.depart()))
    pos = E.Position.depart()
    for coup in pos.coups_legaux():
        r = E.action_depuis_coup(coup)
        de, vers = r.corps["de"], r.corps["vers"]
        typ = E.typ(pos.plateau[de]) - 1
        lettre = PIECES[typ]
        for langue in langues:
            piece = _forme(f"echecs.piece.{lettre}", langue)
            if not piece:
                continue
            for texte in (f"{piece} {E.indice_vers_case(de)} {E.indice_vers_case(vers)}",
                          f"{E.indice_vers_case(de)}{E.indice_vers_case(vers)}",
                          f"{piece} {E.indice_vers_case(de)}-{E.indice_vers_case(vers)}"):
                out.append(_item(texte, r, langue, f"synth-echecs-{de}-{vers}", contexte=ctx_e))
    # --- dames : coups légaux du départ ---
    ctx_d = resume_contexte(D.rsn_depuis_position(D.Position.depart()))
    dp = D.Position.depart()
    for coup in dp.coups_legaux():
        r = D.action_depuis_coup(coup)
        a, b = coup.chemin[0], coup.chemin[-1]
        for langue in langues:
            jeu = _forme("jeu.dames", langue)
            if not jeu:
                continue
            out.append(_item(f"{jeu} {D.indice_vers_case(a)} {D.indice_vers_case(b)}",
                             r, langue, f"synth-dames-{a}-{b}", contexte=ctx_d))
    # --- go : tous les points et la passe ---
    ctx_g = resume_contexte(G.Position.depart(9, 65).vers_rsn())
    for langue in langues:
        jeu = _forme("jeu.go", langue)
        if not jeu:
            continue
        for p in range(81):
            r = RSN("go", "coup", {"taille": 9, "point": p})
            coord = G.point_vers_gtp(p, 9)
            out.append(_item(f"{jeu} {coord}", r, langue, f"synth-go-{p}", contexte=ctx_g))
            out.append(_item(f"{coord}", r, langue, f"synth-go-{p}", contexte=ctx_g))
        rp = RSN("go", "coup", {"taille": 9, "passe": True})
        passe = _forme("go.passe", langue) or "pass"
        out.append(_item(f"{jeu} {passe}", rp, langue, "synth-go-passe", contexte=ctx_g))
    # --- cartes : 52 cartes, rang + enseigne ---
    for langue in langues:
        for carte in range(52):
            rang = C.rang(carte) + 2
            suit = "CDHS"[C.couleur(carte)]
            r = C.action_depuis_carte(carte)
            rn = _forme(f"cartes.rang.{rang}", langue)
            sn = _forme(f"cartes.couleur.{suit}", langue)
            if rn and sn:
                out.append(_item(f"{rn} {sn}", r, langue, f"synth-cartes-{carte}"))
    # --- morpion : 9 cases, 2 symboles, avec et sans nom de jeu ---
    base_m = M.etat_initial()
    for langue in langues:
        jeu = _forme("jeu.morpion", langue)
        for case in range(9):
            for sym in ("X", "O"):
                r = RSN("morpion", "coup", {"case": case, "symbole": sym})
                ctx_m = resume_contexte(base_m.avec(corps={**base_m.corps, "trait": sym}))
                coord = f"{LETTRES_DAMES[case % 3]}{case // 3 + 1}"
                if jeu:
                    out.append(_item(f"{jeu} {coord}", r, langue, f"synth-morpion-{case}-{sym}", contexte=ctx_m))
                out.append(_item(f"{sym} {coord}", r, langue, f"synth-morpion-{case}-{sym}", contexte=ctx_m))
    return out

#!/usr/bin/env python3
"""M1 — hub sémantique typé : surface → code RSN, et retour canonique.

Le hub est la **zone de convergence** du système : il ne produit pas un vecteur
libre, il produit le code fixe de `universaux.py` (15 champs, 502 classes) en
s'appuyant sur le codec classique. Chaque perception et chaque restitution est
publiée sur le bus.
"""
from __future__ import annotations

from jeux.codecs import codec
from semantique.universaux import code_rsn, rsn_depuis_code
from .bus import Bus

FORMATS = {"morpion": "cellule", "echecs": "san", "dames": "numerique",
           "go": "gtp", "cartes": "carte"}


class Hub:
    nom = "M1-hub"

    def __init__(self, bus: Bus | None = None) -> None:
        self.bus = bus or Bus()
        self.dernier = None

    def percevoir(self, texte: str, jeu: str, contexte=None):
        try:
            lec = codec(jeu).lit(texte, niveau=4, contexte=contexte)
        except Exception as e:
            self.bus.publier("echec", {"texte": texte, "erreur": type(e).__name__}, self.nom)
            return None
        if not (lec and lec.rsn):
            self.bus.publier("echec", {"texte": texte, "erreur": "pas de RSN"}, self.nom)
            return None
        code = code_rsn(lec.rsn)
        self.dernier = code
        self.bus.publier("sens", code, self.nom,
                         {"jeu": jeu, "surface": texte, "langue": lec.langue})
        return code

    def rendre(self, code: dict, contexte=None):
        rsn = rsn_depuis_code(code)
        fmt = FORMATS.get(str(code.get("jeu")), "canonique")
        surface = codec(rsn.jeu).rend(rsn, format=fmt, contexte=contexte)
        self.bus.publier("surface", surface, self.nom,
                         {"jeu": rsn.jeu, "format": fmt})
        return surface

#!/usr/bin/env python3
"""corpus_multilingue.py — les mêmes connaissances, dans 71 langues.

Le corpus multilingue est **dérivé** du lexique Wikidata : pour chaque langue,
on prend les libellés disponibles et on construit des surfaces **à mots-clés**
(pièce + cases, rang + enseigne, nom du jeu + coordonnée). Ce n'est pas de la
grammaire : c'est la couche lexicale, celle qui doit déjà porter le sens avant
qu'une phrase soit possible.

Ce qui est **fort** : les pièces des échecs et les cartes, parce que le libellé
y porte tout le sens (un cavalier n'est pas un roi). Ce qui est **mixte** : les
noms de jeux + une coordonnée (go, dames, morpion), parce que la coordonnée est
déjà neutre ; cela vérifie qu'un mot étranger ne bloque pas la lecture.

Chaque item porte une **paire** (le même sens dans toutes les langues) : c'est
la mesure d'invariance inter-langues.
"""
from __future__ import annotations

from .corpus import Corpus
from .lexique_multilingue import MULTI
from .regles import cartes as C
from .regles import dames as D
from .regles import echecs as E
from .regles import go as G
from .regles import morpion as M
from .rsn import RSN


def _premier(concept: str, langue: str) -> str | None:
    formes = MULTI.formes(concept, langue)
    return formes[0] if formes else None


def construire_corpus_multilingue() -> Corpus:
    c = Corpus()
    depart = E.rsn_depuis_position(E.Position.depart())
    nf3 = E.action_depuis_coup(E.Coup(62, 45))
    e4 = E.action_depuis_coup(E.Coup(52, 36))
    vide_m = M.etat_initial()
    vide_g = G.Position.depart(9, 65).vers_rsn()
    depart_d = D.rsn_depuis_position(D.Position.depart())
    for langue in MULTI.langues:
        # --- échecs : la pièce est le mot-clé ---
        n = _premier("echecs.piece.N", langue)
        if n:
            c.ajoute("echecs", f"{n} g1 f3", nf3, contexte=depart,
                     format="multilingue", langue=langue, groupe="multilingue",
                     paire="ml-echecs-nf3")
        p = _premier("echecs.piece.P", langue)
        if p:
            c.ajoute("echecs", f"{p} e2 e4", e4, contexte=depart,
                     format="multilingue", langue=langue, groupe="multilingue",
                     paire="ml-echecs-e4")
        # --- cartes : rang + enseigne ---
        for rang, suit, paire in ((14, "H", "ml-cartes-ah"), (13, "S", "ml-cartes-ks"),
                                  (12, "D", "ml-cartes-qd"), (11, "C", "ml-cartes-jc")):
            r = _premier(f"cartes.rang.{rang}", langue)
            s = _premier(f"cartes.couleur.{suit}", langue)
            if r and s:
                carte = C.carte_id(rang, "CDHS".index(suit))
                c.ajoute("cartes", f"{r} {s}", C.action_depuis_carte(carte),
                         contexte=None, format="multilingue", langue=langue,
                         groupe="multilingue", paire=paire)
        # --- cartes : une basse carte, en chiffres + enseigne ---
        s = _premier("cartes.couleur.H", langue)
        if s:
            c.ajoute("cartes", f"10 {s}", C.action_depuis_carte(C.carte_id(10, 2)),
                     contexte=None, format="multilingue", langue=langue,
                     groupe="multilingue", paire="ml-cartes-10h")
        # --- go : nom du jeu + point, et passe ---
        g = _premier("jeu.go", langue)
        if g:
            c.ajoute("go", f"{g} D4", RSN("go", "coup", {"taille": 9, "point": 48}),
                     contexte=vide_g, format="multilingue", langue=langue,
                     groupe="multilingue", paire="ml-go-d4")
        passe = _premier("go.passe", langue)
        if passe:
            c.ajoute("go", passe, RSN("go", "coup", {"taille": 9, "passe": True}),
                     contexte=vide_g, format="multilingue", langue=langue,
                     groupe="multilingue", paire="ml-go-passe")
        # --- dames : nom du jeu + deux cases ---
        d = _premier("jeu.dames", langue)
        if d:
            c.ajoute("dames", f"{d} b6 c5", D.action_depuis_coup(D.Coup((8, 13))),
                     contexte=depart_d, format="multilingue", langue=langue,
                     groupe="multilingue", paire="ml-dames-b6c5")
        # --- morpion : nom du jeu + une case ---
        m = _premier("jeu.morpion", langue)
        if m:
            c.ajoute("morpion", f"{m} A1",
                     RSN("morpion", "coup", {"case": 0, "symbole": "X"}),
                     contexte=vide_m, format="multilingue", langue=langue,
                     groupe="multilingue", paire="ml-morpion-a1")
    return c


if __name__ == "__main__":
    corpus = construire_corpus_multilingue()
    print(f"{len(corpus.items)} items multilingues")
    for jeu, items in sorted(corpus.par_jeu().items()):
        print(f"  {jeu}: {len(items)}")

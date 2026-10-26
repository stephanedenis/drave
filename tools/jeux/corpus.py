#!/usr/bin/env python3
"""corpus.py — le corpus de surfaces, avec leur sens attendu.

Un item est un triplet (surface, contexte, RSN attendue). Le corpus est
**construit par le code**, pas stocké dans `data/` : il est reproductible, et on
peut le régénérer après chaque correction. Il couvre les cinq jeux, deux
langues, plusieurs notations, et des paires d'expressions **équivalentes** (pour
l'invariance) et **non équivalentes** (pour le contrôle de collision).

Règle : l'attendu est calculé par les **règles**, jamais recopié à la main. Si
le codec et les règles se contredisent, le corpus le dit — c'est un test, pas
une illustration.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .regles import cartes as C
from .regles import dames as D
from .regles import echecs as E
from .regles import go as G
from .regles import morpion as M
from .rsn import RSN


@dataclass(frozen=True)
class Item:
    jeu: str
    texte: str
    nature: str
    attendu: RSN
    contexte: RSN | None = None
    format: str = ""
    langue: str = ""
    groupe: str = ""
    paire: str | None = None
    contre: str | None = None  # paire NÉGATIVE : même `contre`, sens différent


@dataclass
class Corpus:
    items: list[Item] = field(default_factory=list)

    def ajoute(self, jeu: str, texte: str, attendu: RSN, *, contexte: RSN | None = None,
               format: str = "", langue: str = "", groupe: str = "",
               paire: str | None = None, contre: str | None = None) -> None:
        self.items.append(Item(jeu, texte, attendu.nature, attendu, contexte,
                               format, langue, groupe, paire, contre))

    def par_jeu(self) -> dict[str, list[Item]]:
        out: dict[str, list[Item]] = {}
        for it in self.items:
            out.setdefault(it.jeu, []).append(it)
        return out


# ---------------------------------------------------------------------------
# Morpion
# ---------------------------------------------------------------------------
def _morpion(c: Corpus) -> None:
    vide = M.etat_initial()
    xox = RSN("morpion", "etat", {"taille": 3,
                                  "cases": ["X", "O", "X", None, None, None, None, None, None],
                                  "trait": "O"})
    c.ajoute("morpion", ".../.../...", vide, format="grille", langue="notation", groupe="etat",
             paire="morpion-vide")
    c.ajoute("morpion", ". . . / . . . / . . .", vide, format="grille", langue="notation",
             groupe="etat", paire="morpion-vide")
    c.ajoute("morpion", "XOX/.../...", xox, format="grille", langue="notation", groupe="etat",
             paire="morpion-xox")
    c.ajoute("morpion", "X O X | . . . | . . .", xox, format="grille", langue="notation",
             groupe="etat", paire="morpion-xox")
    c.ajoute("morpion", "X,O,X,.,.,.,.,.,.", xox, format="grille", langue="notation",
             groupe="etat", paire="morpion-xox")
    c.ajoute("morpion", "XOX/.../... trait: O", xox, format="grille", langue="fr",
             groupe="etat", paire="morpion-xox")

    # actions : X au trait
    for texte in ("A1", "a1", "(1,1)", "1 1", "ligne 1 colonne 1", "case 1",
                  "haut gauche", "en haut à gauche", "top left", "coin haut gauche",
                  "X joue en haut à gauche", "X plays top left"):
        c.ajoute("morpion", texte, RSN("morpion", "coup", {"case": 0, "symbole": "X"}),
                 contexte=vide, format="cellule", langue="fr", groupe="coup",
                 paire="morpion-a1")
    for texte in ("milieu", "centre", "center", "case 5", "(2,2)",
                  "la croix au centre"):
        c.ajoute("morpion", texte, RSN("morpion", "coup", {"case": 4, "symbole": "X"}),
                 contexte=vide, format="cellule", langue="fr", groupe="coup",
                 paire="morpion-centre")
    # O au trait
    ctx_o = M.applique_indice(vide, 4)  # X au centre, O au trait
    c.ajoute("morpion", "O joue en bas à droite",
             RSN("morpion", "coup", {"case": 8, "symbole": "O"}),
             contexte=ctx_o, format="cellule", langue="fr", groupe="coup",
             paire="morpion-o-bas-droite")
    c.ajoute("morpion", "le rond joue au coin bas droit",
             RSN("morpion", "coup", {"case": 8, "symbole": "O"}),
             contexte=ctx_o, format="cellule", langue="fr", groupe="coup",
             paire="morpion-o-bas-droite")
    # partie
    partie = RSN("morpion", "partie", {
        "taille": 3, "coups": [0, 4, 8],
        "final": ["X", None, None, None, "O", None, None, None, "X"]})
    c.ajoute("morpion", "A1 B2 C3", partie, format="liste", langue="notation",
             groupe="partie", paire="morpion-partie")
    c.ajoute("morpion", "X A1 O B2 X C3", partie, format="liste", langue="fr",
             groupe="partie", paire="morpion-partie")
    # contrôle de collision
    c.ajoute("morpion", "A1", RSN("morpion", "coup", {"case": 0, "symbole": "X"}),
             contexte=vide, format="cellule", langue="notation", groupe="coup",
             contre="morpion-a1-vs-b1")
    c.ajoute("morpion", "B1", RSN("morpion", "coup", {"case": 1, "symbole": "X"}),
             contexte=vide, format="cellule", langue="notation", groupe="coup",
             contre="morpion-a1-vs-b1")
    c.ajoute("morpion", "XOX/.../...", xox, format="grille", langue="notation",
             groupe="etat", contre="morpion-xox-vs-oxx")
    c.ajoute("morpion", "OXX/.../...",
             RSN("morpion", "etat", {"taille": 3,
                                     "cases": ["O", "X", "X", None, None, None, None, None, None],
                                     "trait": "O"}),
             format="grille", langue="notation", groupe="etat", contre="morpion-xox-vs-oxx")


# ---------------------------------------------------------------------------
# Échecs
# ---------------------------------------------------------------------------
def _echecs(c: Corpus) -> None:
    depart = E.rsn_depuis_position(E.Position.depart())
    depart_corps = dict(depart.corps)
    # états
    c.ajoute("echecs", E.Position.depart().fen(), depart, format="fen",
             langue="notation", groupe="etat", paire="echecs-depart")
    c.ajoute("echecs",
             "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
             depart, format="fen", langue="notation", groupe="etat", paire="echecs-depart")
    # diagramme du départ
    from .codecs import rend
    diag = rend(depart, "diagramme")
    c.ajoute("echecs", diag, depart, format="diagramme", langue="notation",
             groupe="etat", paire="echecs-depart")
    # en passant sans capture : la FEN et la même sans ep sont le même sens
    fen_ep = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    # l'attendu est construit SANS le canonicaliseur du codec : c'est la FEN
    # sans en passant, qui est le sens visé. Le test n'est donc pas circulaire.
    etat_ep = E.rsn_depuis_position(E.Position.depuis_fen(
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"))
    c.ajoute("echecs", fen_ep, etat_ep, format="fen", langue="notation",
             groupe="etat", paire="echecs-ep-inutile")
    c.ajoute("echecs", "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
             etat_ep, format="fen", langue="notation", groupe="etat", paire="echecs-ep-inutile")
    # droits impossibles : sans tour, les droits ne veulent rien dire
    fen_droits = "4k3/8/8/8/8/8/8/4K3 w KQkq - 0 1"
    etat_droits = E.rsn_depuis_position(E.Position.depuis_fen(
        "4k3/8/8/8/8/8/8/4K3 w - - 0 1"))
    c.ajoute("echecs", fen_droits, etat_droits, format="fen", langue="notation",
             groupe="etat", paire="echecs-droits-impossibles")
    c.ajoute("echecs", "4k3/8/8/8/8/8/8/4K3 w - - 0 1", etat_droits,
             format="fen", langue="notation", groupe="etat", paire="echecs-droits-impossibles")

    # actions depuis le départ
    e2e4 = E.action_depuis_coup(E.Coup(52, 36))
    for texte in ("e2e4", "e2-e4", "e2 e4", "e4", "E4"):
        c.ajoute("echecs", texte, e2e4, contexte=depart, format="uci", langue="notation",
                 groupe="coup", paire="echecs-e4")
    c.ajoute("echecs", "le pion de e2 vers e4", e2e4, contexte=depart, format="francais",
             langue="fr", groupe="coup", paire="echecs-e4")
    c.ajoute("echecs", "pawn from e2 to e4", e2e4, contexte=depart, format="francais",
             langue="en", groupe="coup", paire="echecs-e4")
    nf3 = E.action_depuis_coup(E.Coup(62, 45))
    for texte, langue in (("Nf3", "notation"), ("Cf3", "fr"), ("g1f3", "notation"),
                          ("cavalier de g1 vers f3", "fr"),
                          ("le cavalier g1 va en f3", "fr"),
                          ("knight from g1 to f3", "en")):
        c.ajoute("echecs", texte, nf3, contexte=depart, format="san", langue=langue,
                 groupe="coup", paire="echecs-nf3")
    # roque
    ctx_roque = E.rsn_depuis_position(E.Position.depuis_fen("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"))
    c.ajoute("echecs", "O-O", E.action_depuis_coup(E.Coup(60, 62, None, E.ROQUE_K)),
             contexte=ctx_roque, format="san", langue="notation", groupe="coup",
             paire="echecs-petit-roque")
    c.ajoute("echecs", "petit roque", E.action_depuis_coup(E.Coup(60, 62, None, E.ROQUE_K)),
             contexte=ctx_roque, format="francais", langue="fr", groupe="coup",
             paire="echecs-petit-roque")
    c.ajoute("echecs", "O-O-O", E.action_depuis_coup(E.Coup(60, 58, None, E.ROQUE_Q)),
             contexte=ctx_roque, format="san", langue="notation", groupe="coup",
             paire="echecs-grand-roque")
    c.ajoute("echecs", "grand roque", E.action_depuis_coup(E.Coup(60, 58, None, E.ROQUE_Q)),
             contexte=ctx_roque, format="francais", langue="fr", groupe="coup",
             paire="echecs-grand-roque")
    # en passant
    ctx_ep = E.rsn_depuis_position(E.Position.depuis_fen(
        "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"))
    c.ajoute("echecs", "exd6", E.action_depuis_coup(E.Coup(28, 19, None, E.EP)),
             contexte=ctx_ep, format="san", langue="notation", groupe="coup",
             paire="echecs-ep")
    # promotion
    ctx_promo = E.rsn_depuis_position(E.Position.depuis_fen("8/P7/8/8/8/8/7p/4K2k w - - 0 1"))
    c.ajoute("echecs", "a8=Q", E.action_depuis_coup(E.Coup(8, 0, E.DAME)),
             contexte=ctx_promo, format="san", langue="notation", groupe="coup",
             paire="echecs-promotion")
    c.ajoute("echecs", "a7a8q", E.action_depuis_coup(E.Coup(8, 0, E.DAME)),
             contexte=ctx_promo, format="uci", langue="notation", groupe="coup",
             paire="echecs-promotion")
    # partie PGN
    pos = E.Position.depart()
    coups = []
    for s in ("e4", "e5", "Nf3", "Nc6"):
        cc, _, _ = pos.parse_san(s)
        pos.joue(cc)
        coups.append(cc)
    c.ajoute("echecs", "1. e4 e5 2. Nf3 Nc6", E.rsn_partie(depart, coups),
             format="pgn", langue="notation", groupe="partie", paire="echecs-pgn")
    # collision
    c.ajoute("echecs", "e2e4", e2e4, contexte=depart, format="uci", langue="notation",
             groupe="coup", contre="echecs-e4-vs-e3")
    c.ajoute("echecs", "e2e3", E.action_depuis_coup(E.Coup(52, 44)),
             contexte=depart, format="uci", langue="notation", groupe="coup",
             contre="echecs-e4-vs-e3")
    c.ajoute("echecs", "Nf3", nf3, contexte=depart, format="san", langue="notation",
             groupe="coup", contre="echecs-nf3-vs-nc3")
    c.ajoute("echecs", "Nc3", E.action_depuis_coup(E.Coup(57, 42)),
             contexte=depart, format="san", langue="notation", groupe="coup",
             contre="echecs-nf3-vs-nc3")
    c.ajoute("echecs", E.Position.depart().fen(), depart, format="fen",
             langue="notation", groupe="etat", contre="echecs-trait")
    c.ajoute("echecs",
             "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1",
             E.rsn_depuis_position(E.Position.depuis_fen(
                 "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")),
             format="fen", langue="notation", groupe="etat", contre="echecs-trait")


# ---------------------------------------------------------------------------
# Dames
# ---------------------------------------------------------------------------
def _dames(c: Corpus) -> None:
    depart = D.rsn_depuis_position(D.Position.depart())
    c.ajoute("dames", "bbbbbbbbbbbb........wwwwwwwwwwww b", depart, format="compact",
             langue="notation", groupe="etat", paire="dames-depart")
    from .codecs import rend
    diag = rend(depart, "diagramme")
    c.ajoute("dames", diag, depart, format="diagramme", langue="notation",
             groupe="etat", paire="dames-depart")

    # capture simple
    cases = [D.VIDE] * 32
    cases[8] = D.NOIR_PION
    cases[13] = D.BLANC_PION
    ctx_cap = D.rsn_depuis_position(D.Position(cases, D.NOIR))
    for texte in ("9x18", "b6xd4", "le pion b6 prend en d4", "b6 prend d4"):
        c.ajoute("dames", texte, D.action_depuis_coup(D.Coup((8, 17))),
                 contexte=ctx_cap, format="numerique", langue="fr", groupe="coup",
                 paire="dames-prise-simple")
    # multi-prise
    cases2 = [D.VIDE] * 32
    cases2[8] = D.NOIR_PION
    cases2[13] = D.BLANC_PION
    cases2[22] = D.BLANC_PION
    ctx_multi = D.rsn_depuis_position(D.Position(cases2, D.NOIR))
    for texte in ("9x18x27", "b6xd4xf2", "le pion b6 prend en d4 puis f2"):
        c.ajoute("dames", texte, D.action_depuis_coup(D.Coup((8, 17, 26))),
                 contexte=ctx_multi, format="numerique", langue="fr", groupe="coup",
                 paire="dames-prise-multiple")
    # simple noir / blanc
    c.ajoute("dames", "9-13", D.action_depuis_coup(D.Coup((8, 12))),
             contexte=depart, format="numerique", langue="notation", groupe="coup",
             paire="dames-simple")
    c.ajoute("dames", "9-14", D.action_depuis_coup(D.Coup((8, 13))),
             contexte=depart, format="numerique", langue="notation", groupe="coup",
             paire="dames-simple-c5")
    c.ajoute("dames", "b6-c5", D.action_depuis_coup(D.Coup((8, 13))),
             contexte=depart, format="algebrique", langue="notation", groupe="coup",
             paire="dames-simple-c5")
    c.ajoute("dames", "le pion de b6 vers c5", D.action_depuis_coup(D.Coup((8, 13))),
             contexte=depart, format="francais", langue="fr", groupe="coup",
             paire="dames-simple-c5")
    ctx_blanc = D.rsn_depuis_position(D.Position(D.Position.depart().cases, D.BLANC))
    c.ajoute("dames", "c3-d4", D.action_depuis_coup(D.Coup((21, 17))),
             contexte=ctx_blanc, format="algebrique", langue="notation", groupe="coup",
             paire="dames-blanc")
    # collision
    c.ajoute("dames", "9-13", D.action_depuis_coup(D.Coup((8, 12))),
             contexte=depart, format="numerique", langue="notation", groupe="coup",
             contre="dames-9-13-vs-10-14")
    c.ajoute("dames", "10-14", D.action_depuis_coup(D.Coup((9, 13))),
             contexte=depart, format="numerique", langue="notation", groupe="coup",
             contre="dames-9-13-vs-10-14")


# ---------------------------------------------------------------------------
# Go
# ---------------------------------------------------------------------------
def _go(c: Corpus) -> None:
    vide9 = G.Position.depart(9, 65).vers_rsn()
    from .codecs import rend
    diag = rend(vide9, "diagramme")
    c.ajoute("go", diag, vide9, format="diagramme", langue="notation",
             groupe="etat", paire="go-vide")
    # un petit plateau 5x5 avec deux pierres
    b = [G.VIDE] * 25
    b[2 * 5 + 2] = G.NOIR
    b[2 * 5 + 3] = G.BLANC
    pos5 = G.Position(5, b, G.BLANC, -1, 0, 65)
    etat5 = pos5.vers_rsn()
    c.ajoute("go", rend(etat5, "diagramme"), etat5, format="diagramme",
             langue="notation", groupe="etat", paire="go-5x5")

    a48 = RSN("go", "coup", {"taille": 9, "point": G.gtp_vers_point("D4", 9)})
    for texte, langue in (("D4", "notation"), ("d4", "notation"),
                          ("pierre noire en D4", "fr"),
                          ("ligne 4 colonne 4", "fr"),
                          ("jouer en D4", "fr")):
        c.ajoute("go", texte, a48, contexte=vide9, format="gtp", langue=langue,
                 groupe="coup", paire="go-d4")
    a_sgf = RSN("go", "coup", {"taille": 9, "point": G.sgf_vers_point("dd", 9)})
    c.ajoute("go", "B[dd]", a_sgf, contexte=vide9, format="sgf", langue="notation",
             groupe="coup", paire="go-dd")
    passe = RSN("go", "coup", {"taille": 9, "passe": True})
    for texte in ("pass", "passer", "je passe"):
        c.ajoute("go", texte, passe, contexte=vide9, format="gtp", langue="fr",
                 groupe="coup", paire="go-passe")
    # partie SGF
    dep = G.Position.depart(9, 65).vers_rsn()
    partie = RSN("go", "partie", {"depart": dict(dep.corps), "coups": [
        {"taille": 9, "point": 30}, {"taille": 9, "point": 40}]})
    c.ajoute("go", "(;GM[1]FF[4]SZ[9];B[dd];W[ee])", partie, format="sgf",
             langue="notation", groupe="partie", paire="go-partie")
    # collision
    a_d5 = RSN("go", "coup", {"taille": 9, "point": G.gtp_vers_point("D5", 9)})
    c.ajoute("go", "D4", a48, contexte=vide9, format="gtp", langue="notation",
             groupe="coup", contre="go-d4-vs-d5")
    c.ajoute("go", "D5", a_d5, contexte=vide9, format="gtp", langue="notation",
             groupe="coup", contre="go-d4-vs-d5")


# ---------------------------------------------------------------------------
# Cartes
# ---------------------------------------------------------------------------
def _cartes(c: Corpus) -> None:
    from .codecs import rend
    for graine, tag in ((42, "a"), (7, "b")):
        state = C.rsn_depuis_position(C.Position.depart(graine))
        c.ajoute("cartes", rend(state, "donne"), state, format="donne",
                 langue="notation", groupe="etat", paire=f"cartes-donne-{tag}")
        tour = int(state.corps["tour"])
        card = state.corps["mains"][tour][0]
        action = C.action_depuis_carte(card)
        for texte, langue in ((C.nom_court(card), "notation"),
                              (C.nom_carte(card, "fr"), "fr"),
                              (C.nom_carte(card, "en"), "en"),
                              ("je joue le " + C.nom_carte(card, "fr"), "fr")):
            c.ajoute("cartes", texte, action, contexte=state, format="carte",
                     langue=langue, groupe="coup", paire=f"cartes-carte-{tag}")
    # main
    main = RSN("cartes", "main", {"cartes": [42, 46, 50]})
    c.ajoute("cartes", "A♥ K♥ Q♥", main, format="liste", langue="notation",
             groupe="main", paire="cartes-main")
    c.ajoute("cartes", "Q♥ A♥ K♥", main, format="liste", langue="notation",
             groupe="main", paire="cartes-main")
    c.ajoute("cartes", "as de cœur, roi de cœur, dame de cœur", main,
             format="francais", langue="fr", groupe="main", paire="cartes-main")
    c.ajoute("cartes", "ace of hearts, king of hearts, queen of hearts", main,
             format="anglais", langue="en", groupe="main", paire="cartes-main")
    # collision
    autre = RSN("cartes", "main", {"cartes": [42, 46, 51]})
    c.ajoute("cartes", "A♥ K♥ Q♥", main, format="liste", langue="notation",
             groupe="main", contre="cartes-main-vs-autre")
    c.ajoute("cartes", "A♠ K♥ Q♥", autre, format="liste", langue="notation",
             groupe="main", contre="cartes-main-vs-autre")


def construire_corpus() -> Corpus:
    c = Corpus()
    _morpion(c)
    _echecs(c)
    _dames(c)
    _go(c)
    _cartes(c)
    return c


if __name__ == "__main__":
    corpus = construire_corpus()
    print(f"{len(corpus.items)} items")
    for jeu, items in sorted(corpus.par_jeu().items()):
        print(f"  {jeu}: {len(items)}")

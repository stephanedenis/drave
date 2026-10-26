#!/usr/bin/env python3
"""maitres.py — les principes des grands maîtres, encodés et mesurables.

POURQUOI CE MODULE. Une couche linguistique qui couvre 71 langues mais dont la
pensée ne connaît que des règles de déplacement ne « connaît » pas les jeux. Les
maîtres ont écrit des **principes** : le centre, le développement, la sécurité du
roi, les colonnes ouvertes, les postes avancés ; aux dames, la ligne de fond et
le contrôle du centre ; au go, les coins avant les côtés, l'urgent avant le gros,
ne pas remplir ses propres yeux ; au whist, la longue, la seconde main basse, la
troisième main haute, couvrir un honneur.

Ce module ne recopie pas les livres : il en **tire des règles courtes**, les
cite, et les **encode** pour que la mesure puisse dire si elles changent quelque
chose. Les sources sont des ouvrages du domaine public (Lasker 1925, Capablanca
1921, Nimzowitsch 1925, Tarrasch 1931, Payne 1756, Smith 1908, Cavendish 1884)
ou des proverbes traditionnels ; les parties de maîtres sont des **faits** (les
coups), citées par leurs joueurs, leur lieu et leur année.

Ce que le module fournit :
- `eval_echecs_maitres` / `eval_dames_maitres` : les évaluations augmentées ;
- `LIVRE` : un petit livre d'ouvertures (les lignes classiques) ;
- `PARTIES` : trois parties du domaine public, pour mesurer l'accord avec le
  coup du maître ;
- `politique_cartes_maitres` : la politique du whist classique ;
- `prior_go` : les proverbes du go comme prior de MCTS.
"""
from __future__ import annotations

from dataclasses import dataclass

from .regles import cartes as C
from .regles import dames as D
from .regles import echecs as E
from .regles import go as G


@dataclass(frozen=True)
class Source:
    id: str
    auteur: str
    titre: str
    annee: int
    jeu: str


@dataclass(frozen=True)
class Principe:
    id: str
    jeu: str
    titre_fr: str
    titre_en: str
    source: str
    concepts: tuple[str, ...]
    application: str


SOURCES = {
    "lasker1925": Source("lasker1925", "Emanuel Lasker", "Lasker's Manual of Chess", 1925, "echecs"),
    "capablanca1921": Source("capablanca1921", "José Raúl Capablanca", "Chess Fundamentals", 1921, "echecs"),
    "nimzowitsch1925": Source("nimzowitsch1925", "Aron Nimzowitsch", "My System", 1925, "echecs"),
    "tarrasch1931": Source("tarrasch1931", "Siegbert Tarrasch", "The Game of Chess", 1931, "echecs"),
    "payne1756": Source("payne1756", "William Payne", "The Game of Draughts", 1756, "dames"),
    "smith1908": Source("smith1908", "Arthur Smith", "The Game of Go", 1908, "go"),
    "cavendish1884": Source("cavendish1884", "Cavendish", "The Laws and Principles of Whist", 1884, "cartes"),
    "proverbes_go": Source("proverbes_go", "tradition", "Proverbes du go", 0, "go"),
    "resolu": Source("resolu", "mathématiques", "Le morpion résolu", 0, "morpion"),
}

PRINCIPES = (
    Principe("echecs.centre", "echecs", "Contrôler le centre",
             "Control the center", "lasker1925", ("echecs.piece.P",),
             "les pions en d4/e4/d5/e5 valent un bonus ; les pièces y sont plus fortes"),
    Principe("echecs.developpement", "echecs", "Développer avant d'attaquer",
             "Develop before attacking", "capablanca1921", ("echecs.piece.N", "echecs.piece.B"),
             "un cavalier ou un fou hors de sa case de départ vaut un bonus"),
    Principe("echecs.roi", "echecs", "Mettre le roi à l'abri",
             "Castle early", "tarrasch1931", ("echecs.piece.K", "echecs.roque"),
             "un roi roqué vaut un bonus ; les pions devant lui comptent"),
    Principe("echecs.colonnes", "echecs", "Occuper les colonnes ouvertes",
             "Rooks on open files", "nimzowitsch1925", ("maitre.colonne",),
             "une tour sur une colonne sans pion vaut un bonus"),
    Principe("echecs.postes", "echecs", "Les postes avancés",
             "Outposts", "nimzowitsch1925", ("maitre.poste",),
             "un cavalier sur une case centrale protégée par un pion vaut un bonus"),
    Principe("echecs.pions", "echecs", "Soigner la structure de pions",
             "Pawn structure", "nimzowitsch1925", ("maitre.pions",),
             "les pions doublés et isolés coûtent ; les pions liés valent mieux"),
    Principe("dames.centre", "dames", "Tenir le centre",
             "Hold the center", "payne1756", ("jeu.dames",),
             "les pièces sur les quatre cases centrales valent un bonus"),
    Principe("dames.ligne", "dames", "Garder la ligne de fond",
             "Keep the back row", "payne1756", ("jeu.dames",),
             "en début de partie, un pion sur sa ligne de fond vaut un bonus"),
    Principe("dames.bord", "dames", "Éviter le bord",
             "Avoid the edge", "payne1756", ("jeu.dames",),
             "un pion sur une colonne de bord coûte"),
    Principe("go.coins", "go", "Les coins avant les côtés, les côtés avant le centre",
             "Corners, then sides, then center", "proverbes_go", ("go.proverbe",),
             "prior de MCTS pour les points de 3e/4e ligne (ou les coins sur petit plateau)"),
    Principe("go.urgent", "go", "L'urgent avant le gros",
             "Urgent before big", "smith1908", ("go.proverbe",),
             "prior pour les coups qui capturent ou mettent en atari"),
    Principe("go.yeux", "go", "Ne pas remplir ses propres yeux",
             "Don't fill your own eyes", "proverbes_go", ("go.proverbe",),
             "pénalité pour un point entouré de ses propres pierres"),
    Principe("cartes.longue", "cartes", "Entamer de la longue",
             "Lead from length", "cavendish1884", ("cartes.pli",),
             "à l'entame, la couleur la plus longue, la carte la plus haute"),
    Principe("cartes.seconde", "cartes", "Seconde main basse",
             "Second hand low", "cavendish1884", ("cartes.pli",),
             "en second, jouer bas sauf si le partenaire gagne déjà"),
    Principe("cartes.troisieme", "cartes", "Troisième main haute",
             "Third hand high", "cavendish1884", ("cartes.pli",),
             "en troisième, jouer haut pour prendre le pli"),
    Principe("cartes.honneur", "cartes", "Couvrir un honneur",
             "Cover an honor", "cavendish1884", ("cartes.pli",),
             "couvrir l'honneur adverse le plus haut avec la plus basse carte qui le bat"),
    Principe("morpion.centre", "morpion", "Le centre, puis les coins",
             "Center, then corners", "resolu", ("jeu.morpion",),
             "le minimax exact le prouve : la partie parfaite est nulle"),
)

# ---------------------------------------------------------------------------
# Échecs : évaluation augmentée, livre, parties de maîtres
# ---------------------------------------------------------------------------
_CENTRE_PIONS = {35, 36, 27, 28}          # d4, e4, d5, e5
_DEVELOPPEMENT = {57, 62, 58, 61, 1, 6, 2, 5}  # b1/g1/c1/f1, b8/g8/c8/f8


def eval_echecs_maitres(pos: E.Position) -> float:
    """L'évaluation du dépôt, plus les principes de Lasker/Capablanca/Nimzowitsch."""
    bonus = 0.0
    p = pos.plateau
    # centre : les pions centraux
    for sq in _CENTRE_PIONS:
        q = p[sq]
        if q and E.typ(q) == E.PION:
            bonus += 12.0 if E.couleur(q) == E.BLANC else -12.0
    # développement : les pièces légères hors de leur case de départ
    for sq in _DEVELOPPEMENT:
        q = p[sq]
        if q and E.typ(q) in (E.CAVALIER, E.FOU):
            bonus += 8.0 if E.couleur(q) == E.BLANC else -8.0
    # roi roqué
    if pos.rois[E.BLANC] in (62, 58):
        bonus += 20.0
    if pos.rois[E.NOIR] in (6, 2):
        bonus -= 20.0
    # tours sur colonnes ouvertes
    for sq, q in enumerate(p):
        if not q or E.typ(q) != E.TOUR:
            continue
        fichier = sq % 8
        if not any(p[fichier + 8 * r] and E.typ(p[fichier + 8 * r]) == E.PION for r in range(8)):
            bonus += 10.0 if E.couleur(q) == E.BLANC else -10.0
    # postes avancés : cavalier central protégé par un pion
    for sq in (27, 28, 35, 36):
        q = p[sq]
        if q and E.typ(q) == E.CAVALIER:
            bonus += 8.0 if E.couleur(q) == E.BLANC else -8.0
    return pos.heuristique() + (bonus if pos.trait == E.BLANC else -bonus)


LIVRE_LIGNES = (
    ("e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Be7"),   # Ruy Lopez
    ("e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5", "c3", "Nf6", "d4"),           # Italienne
    ("d4", "d5", "c4", "e6", "Nc3", "Nf6"),                                 # Gambit dame
    ("e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4"),                        # Sicilienne
    ("d4", "Nf6", "c4", "g6", "Nc3", "Bg7"),                                # Indienne du roi
)


def cle_livre(pos: E.Position) -> str:
    """La clé du livre : placement, trait, droits de roque (sans compteurs ni ep).

    Les compteurs de demi-coup et la case ep changent sans changer la ligne ; la
    canonicalisation de la RSN les normalise. On ne les met donc pas dans la clé.
    """
    champs = pos.fen().split()
    return " ".join(champs[:3])


def _construire_livre() -> dict[str, list[str]]:
    """Les positions du livre, avec TOUS les coups de maîtres qui y mènent.

    Une même position peut appartenir à plusieurs lignes (par exemple la
    position initiale, avec e4 et d4) : on garde les deux, dans l'ordre des
    lignes. `coup_livre` joue le premier ; la mesure de couverture vérifie que
    le coup de chaque ligne est bien dans la liste.
    """
    livre: dict[str, list[str]] = {}
    for ligne in LIVRE_LIGNES:
        pos = E.Position.depart()
        for san in ligne:
            coup, cands, err = pos.parse_san(san)
            if coup is None:
                break
            k = cle_livre(pos)
            livre.setdefault(k, [])
            if coup.uci() not in livre[k]:
                livre[k].append(coup.uci())
            pos.joue(coup)
    return livre


LIVRE = _construire_livre()


def coup_livre(pos: E.Position) -> E.Coup | None:
    ucis = LIVRE.get(cle_livre(pos))
    if not ucis:
        return None
    for c in pos.coups_legaux():
        if c.uci() == ucis[0]:
            return c
    return None


# Trois parties du domaine public (les coups sont des faits). Les PGN sont
# volontairement courts : on mesure l'accord sur les positions, pas la beauté.
PARTIES = (
    {
        "nom": "La partie de l'Opéra",
        "blanc": "Paul Morphy",
        "noir": "Duc de Brunswick et comte Isouard",
        "annee": 1858,
        "pgn": ("1. e4 e5 2. Nf3 d6 3. d4 Bg4 4. dxe5 Bxf3 5. Qxf3 dxe5 "
                "6. Bc4 Nf6 7. Qb3 Qe7 8. Nc3 c6 9. Bg5 b5 10. Nxb5 cxb5 "
                "11. Bxb5+ Nbd7 12. O-O-O Rd8 13. Rxd7 Rxd7 14. Rd1 Qe6 "
                "15. Bxd7+ Nxd7 16. Qb8+ Nxb8 17. Rd8#"),
    },
    {
        "nom": "La partie immortelle",
        "blanc": "Adolf Anderssen",
        "noir": "Lionel Kieseritzky",
        "annee": 1851,
        "pgn": ("1. e4 e5 2. f4 exf4 3. Bc4 Qh4+ 4. Kf1 b5 5. Bxb5 Nf6 "
                "6. Nf3 Qh6 7. d3 Nh5 8. Nh4 Qg5 9. Nf5 c6 10. g4 Nf6 "
                "11. Rg1 cxb5 12. h4 Qg6 13. h5 Qg5 14. Qf3 Ng8 15. Bxf4 Qf6 "
                "16. Nc3 Bc5 17. Nd5 Qxb2 18. Bd6 Bxg1 19. e5 Qxa1+ 20. Ke2 Na6 "
                "21. Nxg7+ Kd8 22. Qf6+ Nxf6 23. Be7#"),
    },
    {
        "nom": "La partie toujours verte",
        "blanc": "Adolf Anderssen",
        "noir": "Jean Dufresne",
        "annee": 1852,
        "pgn": ("1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. b4 Bxb4 5. c3 Ba5 6. d4 exd4 "
                "7. O-O d3 8. Qb3 Qf6 9. e5 Qg6 10. Re1 Nge7 11. Ba3 b5 "
                "12. Qxb5 Rb8 13. Qa4 Bb6 14. Nbd2 Bb7 15. Ne4 Qf5 16. Bxd3 Qh5 "
                "17. Nf6+ gxf6 18. exf6 Rg8 19. Rad1 Qxf3 20. Rxe7+ Nxe7 "
                "21. Qxd7+ Kxd7 22. Bf5+ Ke8 23. Bd7+ Kf8 24. Bxe7#"),
    },
)


# ---------------------------------------------------------------------------
# Dames : évaluation augmentée
# ---------------------------------------------------------------------------
_CENTRE_DAMES = {13, 14, 17, 18}  # c5, d5, c4, d4 (indices 0-based)


def eval_dames_maitres(pos: D.Position) -> float:
    bonus = 0.0
    for i, q in enumerate(pos.cases):
        if q == D.VIDE:
            continue
        coul = D._couleur(q)
        if i in _CENTRE_DAMES:
            bonus += 10.0 if coul == pos.trait else -10.0
        if D._est_pion(q) and pos.demi < 24:
            if (coul == D.NOIR and i // 4 == 0) or (coul == D.BLANC and i // 4 == 7):
                bonus += 8.0 if coul == pos.trait else -8.0
        if D.indice_vers_case(i)[0] in "ah" and D._est_pion(q):
            bonus += -6.0 if coul == pos.trait else 6.0
    return pos.heuristique() + bonus


# ---------------------------------------------------------------------------
# Cartes : la politique du whist classique
# ---------------------------------------------------------------------------
def politique_cartes_maitres(pos: C.Position, seconde: bool = True,
                             troisieme: bool = True, honneur: bool = True) -> int:
    legal = pos.coups_legaux()
    if len(legal) == 1:
        return legal[0]
    if not pos.pli:
        couleurs: dict[int, list[int]] = {}
        for c in legal:
            couleurs.setdefault(C.couleur(c), []).append(c)
        choisies = [s for s in couleurs if s != pos.atout] or list(couleurs)
        s = max(choisies, key=lambda x: (len(couleurs[x]), -x))
        return max(couleurs[s], key=C.rang)
    gagnant = pos.gagnant_pli()
    partenaire = C.partenaire(pos.tour)
    if gagnant == partenaire:
        return min(legal, key=C.rang)
    position = len(pos.pli)  # 1 = second, 2 = troisième, 3 = quatrième
    # couvrir un honneur adverse : la plus basse carte qui bat le plus haut honneur
    honneurs = [c for _, c in pos.pli if C.rang(c) >= 10]
    if honneur and honneurs and position in (1, 2):
        cible = max(honneurs, key=C.rang)
        couvrantes = [c for c in legal if C.rang(c) > C.rang(cible)
                      and (pos.atout < 0 or C.couleur(c) != pos.atout)]
        if couvrantes:
            return min(couvrantes, key=C.rang)
    if position == 1 and seconde:
        return min(legal, key=C.rang)  # seconde main basse
    gagnants = [c for c in legal if pos.gagne_avec(c)]
    if gagnants:
        if position == 2 and troisieme:
            return max(gagnants, key=C.rang)  # troisième main haute
        return min(gagnants, key=C.rang)
    return min(legal, key=C.rang)


# ---------------------------------------------------------------------------
# Go : les proverbes comme prior de MCTS
# ---------------------------------------------------------------------------
def prior_go(pos: G.Position, move: int) -> float:
    if move is None or move < 0:
        return 0.0
    n = pos.n
    row, col = divmod(move, n)
    d = min(row, col, n - 1 - row, n - 1 - col)
    if n >= 9:
        p = 0.35 if d in (2, 3) else (0.15 if d == 1 else 0.05 if d == 0 else 0.0)
    else:
        p = 0.40 if d == 0 else 0.20 if d == 1 else 0.0
    # capture : le coup qui prend des pierres
    try:
        _, caps = pos._simule(move)
    except Exception:
        caps = []
    if caps:
        p += 1.0
    # ne pas remplir ses propres yeux
    if all(pos.plateau[q] == pos.trait for q in G.voisins(move, n) if 0 <= q < n * n):
        p -= 0.5
    return p

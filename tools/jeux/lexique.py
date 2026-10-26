#!/usr/bin/env python3
"""lexique.py — la couche lexicale : de la surface aux concepts, en FR et EN.

POURQUOI UN LEXIQUE SÉPARÉ. Une couche linguistique qui « comprend » les jeux ne
doit pas coder les mots dans les parseurs : elle doit avoir une **table** que
l'on peut (a) étendre à une langue sans toucher à la grammaire, (b) **permuter**
pour le contrôle négatif, et (c) mesurer. C'est ce que fait ce module.

Trois idées, et trois conséquences pour la mesure :

1. **normalisation** : la surface est ramenée à une forme comparable (NFKC,
   apostrophes, espaces, casse pliée, accents retirés pour la recherche) ;
2. **concepts** : chaque forme pointe vers un concept du jeu (`K`, `Q`, `♥`,
   `14`, `haut-gauche`…), jamais vers une chaîne de rendu ;
3. **ambiguïté portée** : une forme qui peut vouloir dire deux choses (le `R`
   français est le ROI, le `R` anglais est la TOUR) rend **deux** concepts avec
   leur langue — le niveau sémantique tranche par la légalité, et l'ambiguïté
   reste dans l'annotation.

Le lexique ne contient **aucune** règle de jeu : il ne sait pas qu'un roi ne
peut pas être capturé, ni qu'un pion va vers l'avant. C'est le rôle des règles.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable

# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------
_REMPLACEMENTS = {
    "\u2019": "'", "\u2018": "'", "\u02bc": "'", "\u00b4": "'",
    "\u2013": "-", "\u2014": "-", "\u2212": "-", "\u2011": "-",
    "\u00d7": "x", "\u2715": "x", "\u2716": "x",
    "\u00a0": " ", "\u202f": " ", "\u2009": " ", "\u2007": " ",
    "\u0153": "oe", "\u0152": "OE", "\u00e6": "ae", "\u00c6": "AE",
    # les quatre symboles de cartes ont une variante « creuse » : on les ramène
    # aux quatre pleins, seuls connus des lexiques.
    "\u2664": "\u2660", "\u2661": "\u2665",
    "\u2662": "\u2666", "\u2667": "\u2663",
}


def normalise(texte: str) -> str:
    """Forme comparable : NFKC, ponctuation typographique, espaces, bords.

    La casse N'EST PAS pliée ici : les notations formelles l'utilisent (le `N`
    de SAN est un cavalier, le `n` d'une case est une colonne). Les lexiques
    plient la casse au moment de la recherche.
    """
    t = unicodedata.normalize("NFKC", texte or "")
    for a, b in _REMPLACEMENTS.items():
        t = t.replace(a, b)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def plie(texte: str) -> str:
    """Casse pliée et accents retirés : la clé de recherche des mots."""
    t = unicodedata.normalize("NFD", normalise(texte).casefold())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.replace("'", "").replace("`", "")
    return re.sub(r"\s+", " ", t).strip()


def sans_espaces(texte: str) -> str:
    return re.sub(r"\s+", "", plie(texte))


# Un « mot » pour la couche lexicale : lettres/chiffres avec apostrophe interne,
# ou un symbole de carte, ou un signe de ponctuation isolé.
_UNITE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:['\u2019][A-Za-zÀ-ÖØ-öø-ÿ]+)?"
    r"|[\u2660\u2665\u2666\u2663]"
    r"|[^\sA-Za-zÀ-ÖØ-öø-ÿ0-9]"
)


def unites(texte: str) -> list[str]:
    """Découpe une surface en unités : mots, nombres, symboles, ponctuation."""
    return _UNITE.findall(normalise(texte))


def mots(texte: str) -> list[str]:
    """Les unités qui sont des mots/nombres, pliées (pour la détection de langue)."""
    return [plie(u) for u in unites(texte) if re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:'.*)?", u)]


# ---------------------------------------------------------------------------
# Le lexique : (domaine, langue) → {forme pliée: concept}
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Correspondance:
    concept: str
    langue: str
    domaine: str
    forme: str
    confiance: float = 1.0


class Lexique:
    """Une table de formes → concepts, par domaine et par langue.

    La table est **inversible** : `formes(domaine, concept, langue)` sert à la
    restitution (sens → surface), et c'est le même contenu qui est permuté pour
    le contrôle négatif de la couche lexicale.
    """

    def __init__(self) -> None:
        self._avant: dict[tuple[str, str], dict[str, str]] = {}
        self._arriere: dict[tuple[str, str], dict[str, list[str]]] = {}
        self._verrouille = False

    def ajoute(self, domaine: str, langue: str, formes: Iterable[str], concept: str) -> None:
        if self._verrouille:
            raise RuntimeError("lexique verrouillé")
        cles = self._avant.setdefault((domaine, langue), {})
        for f in formes:
            for forme in (plie(f), sans_espaces(f)):
                if not forme:
                    continue
                cles[forme] = concept
        ar = self._arriere.setdefault((domaine, langue), {})
        ar.setdefault(concept, [])
        for f in formes:
            if f not in ar[concept]:
                ar[concept].append(f)

    def cherche(self, domaine: str, forme: str, langues: Iterable[str] = ("fr", "en")) -> list[Correspondance]:
        """Toutes les lectures d'une forme, langues confondues.

        Deux langues peuvent donner deux concepts : c'est une **ambiguïté
        portée**, pas une erreur. Le appelant décide (légalité, contexte,
        confiance) et garde la trace dans `Annotation.ambiguites`.
        """
        f = plie(forme)
        fs = sans_espaces(forme)
        # Variantes de phrase : on retire un mot-outil à la fois, puis tous.
        # `haut à gauche` doit retrouver `haut gauche` ; `case du milieu` doit
        # retrouver `milieu`. On ne touche pas aux formes d'un seul mot.
        variantes: list[str] = []
        if " " in f:
            variantes.append(f)
            for mot in ("a", "au", "aux", "en", "le", "la", "les", "du", "de", "des", "l", "case", "cell", "square"):
                variantes.append(re.sub(rf"\b{mot}\b", " ", f))
            variantes.append(re.sub(r"\b(a|au|aux|en|le|la|les|du|de|des|l|case|cell|square)\b", " ", f))
        else:
            variantes.append(f)
        vues_variantes = []
        for v in variantes:
            v = re.sub(r"\s+", " ", v).strip()
            if v and v not in vues_variantes:
                vues_variantes.append(v)
        out: list[Correspondance] = []
        vus: set[tuple[str, str]] = set()
        for langue in langues:
            table = self._avant.get((domaine, langue), {})
            c = None
            for v in vues_variantes:
                c = table.get(v) or table.get(sans_espaces(v))
                if c is not None:
                    break
            if c is None:
                c = table.get(fs)
            if c is not None and (c, langue) not in vus:
                out.append(Correspondance(c, langue, domaine, forme))
                vus.add((c, langue))
        return out

    def concept(self, domaine: str, forme: str, langues: Iterable[str] = ("fr", "en"),
                defaut: str | None = None) -> str | None:
        cs = self.cherche(domaine, forme, langues)
        return cs[0].concept if cs else defaut

    def formes(self, domaine: str, concept: str, langue: str | None = None) -> list[str]:
        if langue is not None:
            return list(self._arriere.get((domaine, langue), {}).get(concept, []))
        out: list[str] = []
        for (d, _), table in self._arriere.items():
            if d == domaine:
                for f in table.get(concept, []):
                    if f not in out:
                        out.append(f)
        return out

    def domaines(self) -> list[str]:
        return sorted({d for d, _ in self._avant})

    # ---- contrôle négatif : permuter les concepts d'un domaine ----------
    def permute(self, domaine: str, decalage: int = 1) -> "Lexique":
        """Rend une COPIE où les concepts du domaine sont permutés cycliquement.

        C'est le contrôle négatif de la couche lexicale : si la couche porte
        vraiment du sens, une permutation must faire chuter la couverture ; si
        elle ne change rien, c'est que le parseur n'utilisait pas le lexique.
        """
        nouveau = Lexique()
        for (d, langue), table in self._avant.items():
            nouveau._avant[(d, langue)] = dict(table)
            nouveau._arriere[(d, langue)] = {k: list(v) for k, v in self._arriere[(d, langue)].items()}
        if domaine in nouveau.domaines():
            concepts = sorted({c for (d, _), t in nouveau._avant.items() if d == domaine for c in t.values()})
            if len(concepts) > 1:
                remap = {c: concepts[(i + decalage) % len(concepts)] for i, c in enumerate(concepts)}
                for (d, langue), table in nouveau._avant.items():
                    if d == domaine:
                        for k, c in list(table.items()):
                            table[k] = remap.get(c, c)
                for (d, langue), table in nouveau._arriere.items():
                    if d == domaine:
                        nouveau._arriere[(d, langue)] = {}
                        for k, formes in table.items():
                            nouveau._arriere[(d, langue)].setdefault(remap.get(k, k), []).extend(formes)
        return nouveau

    def verrouille(self) -> None:
        self._verrouille = True


# ---------------------------------------------------------------------------
# Les tables. On écrit les formes telles qu'un humain les tape : le lexique
# plie la casse et les accents ; les abréviations restent sensibles à la langue.
# ---------------------------------------------------------------------------
LEX = Lexique()


def _ajoute(domaine: str, concept: str, fr: Iterable[str], en: Iterable[str]) -> None:
    LEX.ajoute(domaine, "fr", fr, concept)
    LEX.ajoute(domaine, "en", en, concept)


# --- mots outils (communs) --------------------------------------------------
LEX.ajoute("commun.article", "fr",
           ["le", "la", "les", "l'", "un", "une", "des", "du", "de", "d'", "au", "aux"], "article")
LEX.ajoute("commun.article", "en", ["the", "a", "an", "of", "to", "from", "in", "on", "at"], "article")
LEX.ajoute("commun.et", "fr", ["et", "puis", "ensuite"], "et")
LEX.ajoute("commun.et", "en", ["and", "then"], "et")


def _verbes(domaine: str, fr: Iterable[str], en: Iterable[str]) -> None:
    LEX.ajoute(domaine, "fr", list(fr), "joue")
    LEX.ajoute(domaine, "en", list(en), "joue")


_verbes("commun.verbe",
        ["joue", "jouer", "va", "aller", "vais", "vas", "deplace", "deplacer", "deplacez",
         "prend", "prendre", "prends", "capture", "capturer", "capturez", "mange", "manger",
         "pose", "poser", "posez", "place", "placer", "placez", "passe", "passer", "passez",
         "saute", "sauter", "sautez", "avance", "avancer", "avancez", "recule", "reculer",
         "tire", "tirer", "donne", "donner", "jette", "jeter", "abats", "abattre"],
        ["play", "plays", "played", "move", "moves", "moved", "go", "goes", "went",
         "take", "takes", "took", "capture", "captures", "captured", "jump", "jumps",
         "jumped", "pass", "passes", "passed", "place", "places", "placed", "put",
         "advance", "advances", "play the", "throw", "throws", "discard", "discards",
         "lead", "leads", "follow", "follows"])

LEX.ajoute("commun.direction", "fr",
           ["vers", "en", "a", "au", "aux", "sur", "dans", "depuis", "de", "du", "d'",
            "contre", "devant", "derriere", "gauche", "droite", "avant", "arriere"],
           "vers")
LEX.ajoute("commun.direction", "en",
           ["to", "into", "onto", "from", "at", "on", "in", "against", "left", "right",
            "forward", "backward", "front", "back"], "vers")

# --- morpion ---------------------------------------------------------------
_ajoute("morpion.symbole", "X",
        ["x", "croix", "la croix", "les croix", "iks", "ix", "ex"],
        ["x", "cross", "the cross", "ex", "exes"])
_ajoute("morpion.symbole", "O",
        ["o", "rond", "cercle", "le rond", "zero", "oh"],
        ["o", "nought", "naught", "circle", "round", "zero", "oh"])
_ajoute("morpion.symbole", ".",
        ["vide", "case vide", "personne", "aucun", "point", "libre"],
        ["empty", "blank", "none", "free", "dot"])

_ajoute("morpion.case", "0",
        ["haut gauche", "en haut a gauche", "coin haut gauche", "a1", "1,1", "1 1",
         "ligne 1 colonne 1", "rangee 1 colonne 1", "r1c1", "case 1", "case numero 1"],
        ["top left", "upper left", "top-left", "a1", "1,1", "1 1", "row 1 column 1",
         "r1c1", "square 1", "cell 1"])
_ajoute("morpion.case", "1",
        ["haut", "haut milieu", "milieu haut", "a2", "1,2", "1 2", "ligne 1 colonne 2",
         "r1c2", "case 2", "case numero 2"],
        ["top", "top middle", "top center", "a2", "1,2", "1 2", "row 1 column 2",
         "r1c2", "square 2", "cell 2"])
_ajoute("morpion.case", "2",
        ["haut droite", "en haut a droite", "coin haut droit", "a3", "1,3", "1 3",
         "ligne 1 colonne 3", "r1c3", "case 3", "case numero 3"],
        ["top right", "upper right", "top-right", "a3", "1,3", "1 3", "row 1 column 3",
         "r1c3", "square 3", "cell 3"])
_ajoute("morpion.case", "3",
        ["gauche", "milieu gauche", "gauche milieu", "b1", "2,1", "2 1",
         "ligne 2 colonne 1", "r2c1", "case 4", "case numero 4"],
        ["left", "middle left", "center left", "b1", "2,1", "2 1", "row 2 column 1",
         "r2c1", "square 4", "cell 4"])
_ajoute("morpion.case", "4",
        ["centre", "milieu", "case centrale", "b2", "2,2", "2 2", "ligne 2 colonne 2",
         "r2c2", "case 5", "case numero 5"],
        ["center", "centre", "middle", "b2", "2,2", "2 2", "row 2 column 2",
         "r2c2", "square 5", "cell 5"])
_ajoute("morpion.case", "5",
        ["droite", "milieu droit", "droite milieu", "b3", "2,3", "2 3",
         "ligne 2 colonne 3", "r2c3", "case 6", "case numero 6"],
        ["right", "middle right", "center right", "b3", "2,3", "2 3", "row 2 column 3",
         "r2c3", "square 6", "cell 6"])
_ajoute("morpion.case", "6",
        ["bas gauche", "en bas a gauche", "coin bas gauche", "c1", "3,1", "3 1",
         "ligne 3 colonne 1", "r3c1", "case 7", "case numero 7"],
        ["bottom left", "lower left", "bottom-left", "c1", "3,1", "3 1", "row 3 column 1",
         "r3c1", "square 7", "cell 7"])
_ajoute("morpion.case", "7",
        ["bas", "bas milieu", "milieu bas", "c2", "3,2", "3 2", "ligne 3 colonne 2",
         "r3c2", "case 8", "case numero 8"],
        ["bottom", "bottom middle", "bottom center", "c2", "3,2", "3 2", "row 3 column 2",
         "r3c2", "square 8", "cell 8"])
_ajoute("morpion.case", "8",
        ["bas droite", "en bas a droite", "coin bas droit", "c3", "3,3", "3 3",
         "ligne 3 colonne 3", "r3c3", "case 9", "case numero 9"],
        ["bottom right", "lower right", "bottom-right", "c3", "3,3", "3 3", "row 3 column 3",
         "r3c3", "square 9", "cell 9"])

# --- échecs ----------------------------------------------------------------
_PIECES = {
    "K": (["roi", "le roi", "r"], ["king", "the king", "k"]),
    "Q": (["dame", "la dame", "reine", "d"], ["queen", "the queen", "q"]),
    "R": (["tour", "la tour", "t"], ["rook", "the rook", "r"]),
    "B": (["fou", "le fou", "f"], ["bishop", "the bishop", "b"]),
    "N": (["cavalier", "le cavalier", "c"], ["knight", "the knight", "n"]),
    "P": (["pion", "le pion", "p"], ["pawn", "the pawn", "p"]),
}
for _c, (_fr, _en) in _PIECES.items():
    _ajoute("echecs.piece", _c, _fr, _en)

_ajoute("echecs.couleur", "w", ["blanc", "blancs", "les blancs", "white"],
        ["white", "whites", "the whites"])
_ajoute("echecs.couleur", "b", ["noir", "noirs", "les noirs", "black"],
        ["black", "blacks", "the blacks"])
_ajoute("echecs.roque", "K",
        ["petit roque", "roque court", "roque du cote roi", "roque roi", "o-o", "0-0"],
        ["kingside castle", "short castle", "castle kingside", "o-o", "0-0"])
_ajoute("echecs.roque", "Q",
        ["grand roque", "roque long", "roque du cote dame", "roque dame", "o-o-o", "0-0-0"],
        ["queenside castle", "long castle", "castle queenside", "o-o-o", "0-0-0"])
_ajoute("echecs.verbe", "joue",
        ["joue", "jouer", "va", "aller", "deplace", "deplacer", "prend", "prendre",
         "capture", "capturer", "mange", "manger", "avance", "avancer", "recule", "reculer",
         "saute", "sauter", "promeut", "promouvoir", "roque", "roquer", "donne"],
        ["play", "moves", "move", "goes", "go", "takes", "take", "captures", "capture",
         "advances", "advance", "retreats", "retreat", "jumps", "jump", "promotes",
         "promote", "castles", "castle", "gives"])

# --- dames -----------------------------------------------------------------
_ajoute("dames.piece", "b", ["pion noir", "noir", "les noirs", "homme noir"],
        ["black man", "black piece", "black", "blacks"])
_ajoute("dames.piece", "w", ["pion blanc", "blanc", "les blancs", "homme blanc"],
        ["white man", "white piece", "white", "whites"])
_ajoute("dames.piece", "B", ["dame noire", "dame", "roi noir", "roi"],
        ["black king", "black queen", "king", "queen"])
_ajoute("dames.piece", "W", ["dame blanche", "roi blanc"],
        ["white king", "white queen"])
_ajoute("dames.verbe", "joue",
        ["joue", "jouer", "va", "aller", "deplace", "deplacer", "prend", "prendre",
         "capture", "capturer", "mange", "manger", "saute", "sauter", "promeut", "promouvoir"],
        ["play", "move", "go", "take", "capture", "jump", "promote", "advance"])

# --- go --------------------------------------------------------------------
_ajoute("go.pierre", "1", ["noir", "noire", "les noirs", "pierre noire", "b"],
        ["black", "blacks", "black stone", "b"])
_ajoute("go.pierre", "2", ["blanc", "blanche", "les blancs", "pierre blanche", "w"],
        ["white", "whites", "white stone", "w"])
_ajoute("go.verbe", "joue",
        ["joue", "jouer", "pose", "poser", "place", "placer", "met", "mettre", "passe",
         "passer", "abandonne", "abandonner"],
        ["play", "place", "put", "pass", "resign", "give up"])
_ajoute("go.passe", "passe",
        ["passe", "passer", "je passe", "pass", "passe son tour", "saute son tour"],
        ["pass", "passes", "i pass", "pass turn", "skip", "skips"])
_ajoute("go.abandon", "abandon",
        ["abandon", "abandonne", "je demissionne", "demission", "resigne"],
        ["resign", "resigns", "i resign", "give up"])

# --- cartes ----------------------------------------------------------------
_RANGS = {
    "14": (["as", "l'as", "ace"], ["ace", "the ace"]),
    "13": (["roi", "le roi", "king"], ["king", "the king"]),
    "12": (["dame", "la dame", "reine", "queen"], ["queen", "the queen"]),
    "11": (["valet", "le valet", "jack"], ["jack", "the jack"]),
    "10": (["dix", "le dix", "ten"], ["ten", "the ten"]),
    "9": (["neuf", "le neuf", "nine"], ["nine", "the nine"]),
    "8": (["huit", "le huit", "eight"], ["eight", "the eight"]),
    "7": (["sept", "le sept", "seven"], ["seven", "the seven"]),
    "6": (["six", "le six", "six"], ["six", "the six"]),
    "5": (["cinq", "le cinq", "five"], ["five", "the five"]),
    "4": (["quatre", "le quatre", "four"], ["four", "the four"]),
    "3": (["trois", "le trois", "three"], ["three", "the three"]),
    "2": (["deux", "le deux", "two"], ["two", "the two"]),
}
for _r, (_fr, _en) in _RANGS.items():
    _ajoute("cartes.rang", _r, _fr, _en)

_SUITS = {
    "C": (["trefle", "trefles", "club", "clubs", "\u2663"], ["club", "clubs", "\u2663"]),
    "D": (["carreau", "carreaux", "diamond", "diamonds", "\u2666"],
          ["diamond", "diamonds", "\u2666"]),
    "H": (["coeur", "coeurs", "heart", "hearts", "\u2665"], ["heart", "hearts", "\u2665"]),
    "S": (["pique", "piques", "spade", "spades", "\u2660"], ["spade", "spades", "\u2660"]),
}
for _s, (_fr, _en) in _SUITS.items():
    _ajoute("cartes.couleur", _s, _fr, _en)

_ajoute("cartes.verbe", "joue",
        ["joue", "jouer", "pose", "poser", "donne", "donner", "jette", "jeter",
         "abats", "abattre", "coupe", "couper", "suit", "fournit", "defausse", "defausser"],
        ["play", "plays", "lead", "leads", "follow", "follows", "throw", "throws",
         "discard", "discards", "lay", "lays", "put", "puts"])
_ajoute("cartes.main", "main", ["main", "les cartes", "jeu"], ["hand", "cards", "holding"])
_ajoute("cartes.pli", "pli", ["pli", "tour", "levée", "levee"], ["trick", "round"])
_ajoute("cartes.atout", "atout", ["atout", "l'atout", "trump"], ["trump", "trumps"])
_ajoute("cartes.partenaire", "partenaire", ["partenaire", "le partenaire", "coequipier"],
        ["partner", "teammate"])
_ajoute("cartes.entame", "entame", ["entame", "entameur", "commence", "le premier"],
        ["lead", "leader", "starts", "first"])

# Nombres ordinaux / cardinaux utiles pour les coordonnées et les plis.
_NOMBRES = {
    "0": (["zero", "zero"], ["zero"]),
    "1": (["un", "une", "premier", "premiere"], ["one", "first"]),
    "2": (["deux", "deuxieme", "second", "seconde"], ["two", "second"]),
    "3": (["trois", "troisieme"], ["three", "third"]),
    "4": (["quatre", "quatrieme"], ["four", "fourth"]),
    "5": (["cinq", "cinquieme"], ["five", "fifth"]),
    "6": (["six", "sixieme"], ["six", "sixth"]),
    "7": (["sept", "septieme"], ["seven", "seventh"]),
    "8": (["huit", "huitieme"], ["eight", "eighth"]),
    "9": (["neuf", "neuvieme"], ["nine", "ninth"]),
    "10": (["dix", "dixieme"], ["ten", "tenth"]),
}
for _n, (_fr, _en) in _NOMBRES.items():
    _ajoute("commun.nombre", _n, _fr, _en)

# Noms de jeux : pour la détection et les consignes.
_ajoute("jeu.nom", "morpion",
        ["morpion", "tic-tac-toe", "tic tac toe", "tic tac toe", "oxo"],
        ["tic-tac-toe", "tic tac toe", "noughts and crosses", "oxo"])
_ajoute("jeu.nom", "echecs",
        ["echecs", "les echecs", "jeu d'echecs", "chess"],
        ["chess", "the chess game"])
_ajoute("jeu.nom", "dames",
        ["dames", "les dames", "jeu de dames", "dames anglaises", "checkers", "draughts"],
        ["checkers", "draughts", "the checkers game"])
_ajoute("jeu.nom", "go",
        ["go", "jeu de go", "weiqi", "baduk"],
        ["go", "the game of go", "weiqi", "baduk"])
_ajoute("jeu.nom", "cartes",
        ["cartes", "jeu de cartes", "whist", "cartes a jouer"],
        ["cards", "card game", "whist", "playing cards"])

LEX.verrouille()


# ---------------------------------------------------------------------------
# Détection de langue : grossière, mais mesurée (et contrôlée par permutation).
# ---------------------------------------------------------------------------
_MOTS_FR = {"le", "la", "les", "un", "une", "des", "du", "de", "et", "joue", "jouer",
            "prend", "prendre", "case", "pion", "roi", "dame", "tour", "fou", "cavalier",
            "noir", "blanc", "coeur", "trefle", "carreau", "pique", "vers", "en", "au",
            "sur", "passe", "passez", "milieu", "gauche", "droite", "haut", "bas", "as"}
_MOTS_EN = {"the", "a", "an", "of", "to", "from", "and", "play", "plays", "move", "moves",
            "take", "takes", "square", "pawn", "king", "queen", "rook", "bishop", "knight",
            "black", "white", "heart", "hearts", "club", "clubs", "diamond", "diamonds",
            "spade", "spades", "top", "bottom", "left", "right", "center", "middle", "pass"}


def langue_probable(texte: str) -> tuple[str, float]:
    """« fr », « en », « notation » ou « inconnue », avec une confiance grossière."""
    ws = set(mots(texte))
    fr = len(ws & _MOTS_FR)
    en = len(ws & _MOTS_EN)
    if fr == 0 and en == 0:
        # Une notation formelle : beaucoup de chiffres/symboles, peu de lettres.
        lettres = sum(c.isalpha() for c in texte)
        chiffres = sum(c.isdigit() for c in texte)
        signes = sum(not c.isalnum() and not c.isspace() for c in texte)
        if chiffres + signes > 0 and lettres <= max(2, (chiffres + signes)):
            return "notation", 0.8
        return "inconnue", 0.0
    total = fr + en
    if fr == en:
        return "fr", 0.5  # égalité : on privilégie la langue du dépôt
    return ("fr" if fr > en else "en"), max(fr, en) / total


# ---------------------------------------------------------------------------
# Petites aides de lecture, partagées par les codecs.
# ---------------------------------------------------------------------------
def est_article(forme: str) -> bool:
    return bool(LEX.cherche("commun.article", forme))


def est_verbe(forme: str) -> bool:
    return bool(LEX.cherche("commun.verbe", forme))


def est_nombre(forme: str) -> int | None:
    cs = LEX.cherche("commun.nombre", forme)
    if cs:
        try:
            return int(cs[0].concept)
        except ValueError:
            return None
    try:
        return int(forme)
    except ValueError:
        return None


def est_symbole_carte(u: str) -> bool:
    return u in "\u2660\u2665\u2666\u2663"

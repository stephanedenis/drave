#!/usr/bin/env python3
"""codecs.echecs — la surface des échecs : FEN, SAN, UCI, français, PGN.

Les échecs sont le jeu où la **même position** a le plus de surfaces : une FEN,
un diagramme, un coup SAN (`Cf3`), un coup UCI (`g1f3`), une phrase française
(« le cavalier de g1 va en f3 »), une partie PGN. Le codec les ramène toutes à
la même RSN ; c'est cette invariance que `mesure.py` mesure.

Le codec ne contient **aucune règle** : il appelle `regles.echecs` pour les
coups légaux, la désambiguïsation SAN et la validité d'une FEN. C'est ce qui
permet de dire, dans la fiche, que l'étage 2 ne dépend pas de la surface.
"""
from __future__ import annotations

import re

from ..grammaire import naturel
from ..lexique import LEX, plie
from ..lexique_multilingue import MULTI
from ..rsn import Annotation, RSN
from ..regles import echecs as E
from .base import Arbre, Codec, Lecture

_LETTRES_PIECE = {"K": "K", "Q": "Q", "R": "R", "B": "B", "N": "N", "P": "P",
                  "C": "N", "D": "Q", "T": "R", "F": "B"}
_NOMS_PIECE = {E.ROI: "roi", E.DAME: "dame", E.TOUR: "tour", E.FOU: "fou",
               E.CAVALIER: "cavalier", E.PION: "pion"}
_NOMS_PIECE_EN = {E.ROI: "king", E.DAME: "queen", E.TOUR: "rook", E.FOU: "bishop",
                  E.CAVALIER: "knight", E.PION: "pawn"}


# ---------------------------------------------------------------------------
# Détection de forme
# ---------------------------------------------------------------------------
_RE_FEN = re.compile(r"(?:[rnbqkpRNBQKP1-8]+/){7}[rnbqkpRNBQKP1-8]+")
_RE_UCI = re.compile(r"^\s*([a-h][1-8])[- ]?([a-h][1-8])([nbrqNBRQ])?\s*$")


def _est_fen(texte: str) -> bool:
    return bool(_RE_FEN.search(texte)) and len(texte.split()) >= 2


def _est_pgn(texte: str) -> bool:
    t = texte.strip()
    if re.search(r'\[\w+\s+"', t):
        return True
    if re.search(r"\b\d+\.(?:\.\.)?(?!\d)\s*[KQRBNO0-9a-h]", t):
        return True
    # une suite de SAN/UCI séparés par des espaces, au moins deux
    jetons = [x for x in re.split(r"\s+", t) if x and not re.fullmatch(r"\d+\.+", x)]
    if len(jetons) >= 2:
        return all(_RE_UCI.fullmatch(x) or re.fullmatch(r"(?:O-O(?:-O)?|[KQRBN][a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?)", x)
                   for x in jetons)
    return False


def _lignes_diagramme(texte: str) -> list[str]:
    lignes = []
    for l in texte.splitlines():
        l = l.strip()
        if not l:
            continue
        # enlève un numéro de rangée « 8 | » ou « 8: »
        l = re.sub(r"^\d+\s*[|:]\s*", "", l)
        # enlève les coordonnées de bord « a b c ... »
        if re.fullmatch(r"[a-h](?:\s+[a-h]){7}", l):
            continue
        if re.match(r"(?:trait|roques?|ep|au tour|to move|turn)\b", l, re.I):
            continue
        lignes.append(l)
    return lignes


def _est_diagramme(texte: str) -> bool:
    lignes = _lignes_diagramme(texte)
    if len(lignes) != 8:
        return False
    for l in lignes:
        s = re.sub(r"\s+", "", l)
        if len(s) != 8:
            return False
        if not re.fullmatch(r"[rnbqkpRNBQKP.·+]+", s):
            return False
    return True


def _lit_diagramme(texte: str) -> E.Position:
    """Un diagramme 8×8, avec trait/roques/en passant optionnels."""
    lignes = _lignes_diagramme(texte)
    if len(lignes) != 8:
        raise E.ErreurEchecs("diagramme : il faut 8 rangées")
    plateau = [0] * 64
    for r, l in enumerate(lignes):
        s = re.sub(r"\s+", "", l)
        if len(s) != 8:
            raise E.ErreurEchecs(f"diagramme : rangée {r + 1} fait {len(s)} cases")
        for c, ch in enumerate(s):
            if ch in ".·+":
                continue
            if ch not in "pnbrqkPNBRQK":
                raise E.ErreurEchecs(f"diagramme : pièce inconnue {ch!r}")
            coul = E.BLANC if ch.isupper() else E.NOIR
            plateau[r * 8 + c] = E.piece(coul, "pnbrqk".index(ch.lower()) + 1)
    trait = E.BLANC
    roques = 0
    ep = -1
    m = re.search(r"(?:trait|au tour|to move|turn)\s*[:=]?\s*(w|b|blanc|noir|white|black)", texte, re.I)
    if m:
        trait = E.BLANC if m.group(1).lower() in ("w", "blanc", "white") else E.NOIR
    m = re.search(r"(?:roques?|castling)\s*[:=]\s*([KQkq-]+)", texte, re.I)
    if m:
        for ch in m.group(1):
            roques |= {"K": 1, "Q": 2, "k": 4, "q": 8}.get(ch, 0)
    m = re.search(r"(?:ep|en passant)\s*[:=]\s*([a-h][1-8]|-)", texte, re.I)
    if m and m.group(1) != "-":
        ep = E.case_vers_indice(m.group(1))
    return E.Position(plateau, trait, roques, ep, 0, 1)


# ---------------------------------------------------------------------------
# Canonicalisation sémantique (niveau 4)
# ---------------------------------------------------------------------------
def _canonise_position(pos: E.Position) -> E.Position:
    """Retire les droits impossibles et l'en passant qui ne capture rien.

    Une FEN peut dire `KQkq` sans tour, ou `e3` sans pion noir capable de
    prendre : ce sont des **surfaces** différentes pour un **même sens**. Les
    deux canonicalisations sont mesurées : elles ne changent pas les coups
    légaux, seulement l'empreinte.
    """
    p = pos.plateau
    roques = pos.roques
    if p[60] != E.piece(E.BLANC, E.ROI):
        roques &= ~3
    if p[63] != E.piece(E.BLANC, E.TOUR):
        roques &= ~1
    if p[56] != E.piece(E.BLANC, E.TOUR):
        roques &= ~2
    if p[4] != E.piece(E.NOIR, E.ROI):
        roques &= ~12
    if p[7] != E.piece(E.NOIR, E.TOUR):
        roques &= ~4
    if p[0] != E.piece(E.NOIR, E.TOUR):
        roques &= ~8
    if roques != pos.roques:
        pos = E.Position(list(p), pos.trait, roques, pos.ep, pos.demi, pos.plein)
    if pos.ep >= 0:
        if not any(c.drapeau == E.EP for c in pos.coups_legaux()):
            pos = E.Position(list(pos.plateau), pos.trait, pos.roques, -1, pos.demi, pos.plein)
    return pos


def _corps_etat(pos: E.Position) -> dict:
    return E.rsn_depuis_position(pos).corps


def _corps_coup(c: E.Coup) -> dict:
    return E.action_depuis_coup(c).corps


def _coup_depuis_corps(corps: dict) -> E.Coup:
    return E.Coup(int(corps["de"]), int(corps["vers"]),
                  {"n": E.CAVALIER, "b": E.FOU, "r": E.TOUR, "q": E.DAME}.get(corps.get("promotion") or ""),
                  {"K": E.ROQUE_K, "Q": E.ROQUE_Q}.get(corps.get("roque"), E.NORMAL))


# ---------------------------------------------------------------------------
# Lecture des phrases
# ---------------------------------------------------------------------------
def _piece_depuis_mots(t: str, langue: str | None) -> int | None:
    for u in re.findall(r"[a-z]+", t):
        if len(u) == 1:
            continue
        cs = LEX.cherche("echecs.piece", u, langues=(langue,) if langue else ("fr", "en"))
        if cs:
            return {"K": E.ROI, "Q": E.DAME, "R": E.TOUR, "B": E.FOU,
                    "N": E.CAVALIER, "P": E.PION}[cs[0].concept]
    # le lexique multilingue (53 langues) — les libellés sont des noms de pièces
    ms = MULTI.cherche("echecs.piece", t)
    if ms:
        return {"K": E.ROI, "Q": E.DAME, "R": E.TOUR, "B": E.FOU,
                "N": E.CAVALIER, "P": E.PION}[ms[0].valeur]
    # une lettre initiale française (C, D, T, F, R) ou anglaise
    m = re.match(r"\s*([KQRBNCDTFkqrbncdtf])\s*([a-h][1-8])", t)
    if m:
        cs = LEX.cherche("echecs.piece", m.group(1), langues=(langue,) if langue else ("fr", "en"))
        if cs:
            return {"K": E.ROI, "Q": E.DAME, "R": E.TOUR, "B": E.FOU,
                    "N": E.CAVALIER, "P": E.PION}[cs[0].concept]
    return None


def _lit_phrase(texte: str, pos: E.Position | None, niveau: int,
                langue: str | None) -> tuple[E.Coup | None, list[E.Coup], list[str], str | None]:
    """Une phrase naturelle → un coup (ou des candidats)."""
    t = naturel(texte)
    amb: list[str] = []
    # roques
    for forme, drapeau in (
            (("grand roque", "roque long", "roque cote dame", "queenside", "long castle", "o o o"), E.ROQUE_Q),
            (("petit roque", "roque court", "roque cote roi", "kingside", "short castle", "o o"), E.ROQUE_K)):
        if any(f in t for f in forme):
            if pos is None:
                de, vers = (60, 62) if drapeau == E.ROQUE_K else (60, 58)
                return E.Coup(de, vers, None, drapeau), [], ["position requise pour valider le roque"], "fr"
            cands = [c for c in pos.coups_legaux() if c.drapeau == drapeau]
            return (cands[0] if len(cands) == 1 else None), cands, amb, "fr"

    carres = re.findall(r"\b[a-h][1-8]\b", t)
    if not carres:
        return None, [], [f"aucune case dans la phrase : {texte!r}"], None
    de = E.case_vers_indice(carres[0]) if len(carres) >= 2 else None
    vers = E.case_vers_indice(carres[-1])
    ptype = _piece_depuis_mots(t, langue)
    prise = any(m in t for m in ("prend", "prends", "capture", "captures", "mange", "takes", "took"))
    promo = None
    if "promotion" in t or "promeut" in t or "promotes" in t:
        for u in re.findall(r"[a-z]+", t):
            cs = LEX.cherche("echecs.piece", u, langues=(langue,) if langue else ("fr", "en"))
            if cs and cs[0].concept in "QRBN":
                promo = {"Q": E.DAME, "R": E.TOUR, "B": E.FOU, "N": E.CAVALIER}[cs[0].concept]
                break
    if pos is None:
        if de is None:
            return None, [], ["position requise pour désambiguïser la pièce"], None
        return E.Coup(de, vers, promo), [], ["position requise pour valider"], "fr"
    types = [ptype] if ptype is not None else ([E.PION] if de is not None else [E.PION, E.CAVALIER, E.FOU, E.TOUR, E.DAME, E.ROI])
    cands = []
    for c in pos.coups_legaux():
        p = pos.plateau[c.de]
        if E.typ(p) not in types:
            continue
        if de is not None and c.de != de:
            continue
        if c.vers != vers:
            continue
        if prise and not (pos.plateau[c.vers] or c.drapeau == E.EP):
            continue
        if promo is not None and c.promotion != promo:
            continue
        cands.append(c)
    if len(cands) == 1:
        return cands[0], cands, amb, "fr"
    if not cands:
        return None, [], [f"aucun coup légal ne correspond à {texte!r}"], "fr"
    return None, cands, amb + ["plusieurs coups possibles"], "fr"


# ---------------------------------------------------------------------------
# Codec
# ---------------------------------------------------------------------------
class CodecEchecs(Codec):
    jeu = "echecs"
    formats = ("fen", "diagramme", "san", "uci", "francais", "pgn", "canonique")

    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
            langue: str | None = None) -> Lecture:
        lec = self.lecture(texte, niveau, langue)
        if not texte or not texte.strip():
            return self.echoue(lec, "surface vide")

        # 1. FEN = état
        if _est_fen(texte):
            try:
                pos = E.Position.depuis_fen(texte.strip(), valide=(niveau >= 4))
                if niveau >= 4:
                    pos = _canonise_position(pos)
            except Exception as e:
                return self.echoue(lec, f"FEN invalide : {e}")
            lec.format = "fen"
            lec.arbre = Arbre("etat_echecs", (("fen", pos.fen()),))
            return self.reussi(lec, E.rsn_depuis_position(pos), "fen", 1.0)

        # 2. diagramme = état
        if niveau >= 1 and _est_diagramme(texte):
            try:
                pos = _lit_diagramme(texte)
                if niveau >= 4:
                    pos = _canonise_position(pos)
            except Exception as e:
                return self.echoue(lec, f"diagramme invalide : {e}")
            lec.format = "diagramme"
            return self.reussi(lec, E.rsn_depuis_position(pos), "diagramme", 0.95,
                               ["droits de roque non précisés"] if "roque" not in naturel(texte) else [])

        # 3. PGN = partie
        if niveau >= 1 and _est_pgn(texte):
            try:
                partie, amb = self._lit_pgn(texte, niveau)
            except Exception as e:
                return self.echoue(lec, f"PGN illisible : {e}")
            lec.format = "pgn"
            lec.ambiguites = tuple(amb)
            return self.reussi(lec, partie, "pgn", 0.95, amb)

        # 4. un coup : il faut une position pour SAN, pas pour UCI
        pos = None
        if contexte is not None:
            try:
                pos = E.position_depuis_rsn(contexte, valide=True)
            except Exception as e:
                return self.echoue(lec, f"position de contexte invalide : {e}")

        # 4a. roque en toutes lettres (niveau 2) — une forme fermée, pas une phrase
        if niveau >= 2 and re.search(r"\b(petit roque|grand roque|roque court|roque long|"
                                     r"roque cote|kingside|queenside|castle|o o)\b",
                                     naturel(texte)):
            c, cands, amb, _ = _lit_phrase(texte, pos, niveau, langue)
            if c is not None:
                lec.format = "francais"
                return self.reussi(lec, E.action_depuis_coup(c), "francais", 0.95, amb)
            if cands:
                lec.candidats = [E.action_depuis_coup(x) for x in cands]
                return self.echoue(lec, "coup ambigu : " + " ; ".join(amb))
            return self.echoue(lec, "roque impossible dans cette position")

        # 4b. UCI / LAN — la forme canonique d'un coup, sans position
        m = _RE_UCI.fullmatch(texte)
        if m:
            if pos is not None:
                c, cands, amb = pos.parse_uci(texte)
                if c is not None:
                    lec.format = "uci"
                    return self.reussi(lec, E.action_depuis_coup(c), "uci", 1.0, amb)
                if cands:
                    lec.candidats = [E.action_depuis_coup(x) for x in cands]
                    return self.echoue(lec, "promotion non précisée")
                return self.echoue(lec, amb[0] if amb else "UCI illégal")
            # sans position : la forme suffit, la légalité viendra du niveau 4
            de = E.case_vers_indice(m.group(1))
            vers = E.case_vers_indice(m.group(2))
            promo = None
            if m.group(3):
                promo = "NBRQ".index(m.group(3).upper()) + E.CAVALIER
            lec.format = "uci"
            return self.reussi(lec, E.action_depuis_coup(E.Coup(de, vers, promo)),
                               "uci", 0.8, ["position requise pour valider"])

        # 4b-bis. une CASE seule (`E4`) : avec le jeu explicite, c'est une
        # référence de case, PAS un coup. Le SAN exige une position ; la case, non.
        # MAIS si une position est fournie, c'est le SAN qui tranche : sans ce
        # `pos is None`, `e4` avec `contexte=départ` devenait une requête de case
        # au lieu du coup `e2e4` (régression d1eb552b, 110/112 au niveau 4).
        m = re.fullmatch(r"([a-h][1-8])", texte.strip(), re.IGNORECASE)
        if m and pos is None:
            idx = E.case_vers_indice(m.group(1).lower())
            lec.format = "case"
            return self.reussi(lec, RSN("echecs", "requete", {"case": idx}),
                               "case", 0.8, ["case sans position : ce n'est pas un coup"])

        # 4c. SAN — exige la position (c'est la légalité qui désambiguïse)
        erreur_san = None
        if pos is not None and niveau >= 1:
            premier = texte.strip()[:1].upper()
            if niveau < 2 and premier in ("C", "D", "T", "F"):
                erreur_san = "lettres françaises : niveau 2"
            else:
                c, cands, amb = pos.parse_san(texte, niveau)
                if c is not None:
                    lec.format = "san"
                    return self.reussi(lec, E.action_depuis_coup(c), "san", 1.0, amb)
                if cands:
                    lec.candidats = [E.action_depuis_coup(x) for x in cands]
                    return self.echoue(lec, "coup ambigu : " + " ; ".join(amb))
                erreur_san = amb[0] if amb else f"SAN illégal : {texte!r}"
        elif pos is None:
            erreur_san = "position requise pour un SAN"

        # 4d. phrase naturelle (niveau 3) : deux cases, un verbe, une pièce
        if niveau >= 3:
            c, cands, amb, lang = _lit_phrase(texte, pos, niveau, langue)
            if c is not None:
                lec.format = "francais"
                return self.reussi(lec, E.action_depuis_coup(c), "francais", 0.9, amb)
            if cands:
                lec.candidats = [E.action_depuis_coup(x) for x in cands]
                return self.echoue(lec, "coup ambigu : " + " ; ".join(amb))

        return self.echoue(lec, erreur_san or "aucune lecture d'échecs")

    # ------------------------------------------------------------------
    def _lit_pgn(self, texte: str, niveau: int) -> tuple[RSN, list[str]]:
        amb: list[str] = []
        tags = dict(re.findall(r'\[(\w+)\s+"([^"]*)"\]', texte))
        depart = E.rsn_depuis_position(E.Position.depart())
        if "FEN" in tags:
            depart = E.rsn_depuis_position(E.Position.depuis_fen(tags["FEN"], valide=(niveau >= 4)))
        pos = E.position_depuis_rsn(depart, valide=(niveau >= 4))
        corps = re.sub(r"\{[^}]*\}", " ", texte)
        corps = re.sub(r"\([^)]*\)", " ", corps)
        corps = re.sub(r'\[[^\]]*\]', " ", corps)
        corps = re.sub(r"\$\d+", " ", corps)
        jetons = []
        for j in re.split(r"\s+", corps):
            if not j or re.fullmatch(r"\d+\.+", j):
                continue
            if j in ("1-0", "0-1", "1/2-1/2", "*"):
                continue
            jetons.append(j)
        coups: list[E.Coup] = []
        for j in jetons:
            j = re.sub(r"[!?]+$", "", j)
            c = None
            if j in ("O-O", "0-0", "O-O-O", "0-0-0"):
                c, cands, a = pos.parse_san(j, niveau)
            else:
                c, cands, a = pos.parse_san(j, niveau)
                if c is None:
                    c2, cands2, a2 = pos.parse_uci(j)
                    if c2 is not None:
                        c, cands, a = c2, cands2, a2
            if c is None:
                raise E.ErreurEchecs(f"coup PGN illisible : {j!r} ({a})")
            pos.joue(c)
            coups.append(c)
        if not coups:
            raise E.ErreurEchecs("PGN sans coup")
        return E.rsn_partie(depart, coups), amb

    # ------------------------------------------------------------------
    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
             contexte: RSN | None = None) -> str:
        if rsn.jeu != "echecs":
            raise ValueError("ce n'est pas une RSN d'échecs")
        if rsn.nature == "etat":
            pos = E.position_depuis_rsn(rsn)
            if format in ("fen", "canonique"):
                return pos.fen()
            if format == "diagramme":
                lignes = []
                for r in range(8):
                    ligne = []
                    for c in range(8):
                        p = pos.plateau[r * 8 + c]
                        if not p:
                            ligne.append(".")
                        else:
                            ch = "pnbrqk"[E.typ(p) - 1]
                            ligne.append(ch.upper() if E.couleur(p) == E.BLANC else ch)
                    lignes.append(" ".join(ligne))
                trait = "trait: w" if pos.trait == E.BLANC else "trait: b"
                roques = rsn.corps.get("roques") or "-"
                return "\n".join(lignes) + f"\n{trait} roques: {roques}"
            raise ValueError(f"format d'état inconnu : {format}")
        if rsn.nature == "coup":
            c = _coup_depuis_corps(rsn.corps)
            if format in ("uci", "canonique"):
                return c.uci()
            if format == "san":
                if contexte is None:
                    raise ValueError("le SAN exige la position de contexte")
                pos = E.position_depuis_rsn(contexte)
                return pos.san(E.coup_depuis_action(rsn, pos))
            if format == "francais":
                return _phrase_coup(rsn, langue)
            raise ValueError(f"format de coup inconnu : {format}")
        if rsn.nature == "partie":
            pos, coups = E.partie_depuis_rsn(rsn)
            if format in ("pgn", "canonique"):
                tags = []
                depart = RSN("echecs", "etat", dict(rsn.corps["depart"]))
                if depart.corps != E.rsn_depuis_position(E.Position.depart()).corps:
                    tags.append(f'[FEN "{E.position_depuis_rsn(depart).fen()}"]')
                # rejoue depuis le départ pour rendre le SAN
                p = E.position_depuis_rsn(depart)
                mots = []
                for i, c in enumerate(coups):
                    if i % 2 == 0:
                        mots.append(f"{i // 2 + 1}.")
                    mots.append(p.san(c))
                    p.joue(c)
                res = p.resultat() or "*"
                return ("\n".join(tags) + "\n" if tags else "") + " ".join(mots) + " " + res
            if format == "uci":
                return " ".join(c.uci() for c in coups)
            raise ValueError(f"format de partie inconnu : {format}")
        raise ValueError(f"nature inconnue : {rsn.nature}")

    # ------------------------------------------------------------------
    def detecte(self, texte: str) -> float:
        t = texte.lower()
        if "échecs" in t or "echecs" in t or "chess" in t:
            return 0.98
        if _est_fen(texte):
            return 0.99
        if _est_diagramme(texte):
            return 0.96
        if _est_pgn(texte):
            return 0.93
        if re.search(r"\b(petit roque|grand roque|castle|roque)\b", t):
            return 0.8
        if re.search(r"\b(?:O-O(?:-O)?|[KQRBNCDTF][a-h]?[1-8]?x?[a-h][1-8]|[a-h]x[a-h][1-8])\b",
                     texte):
            return 0.55
        if _RE_UCI.fullmatch(texte):
            return 0.45
        if re.search(r"\b[a-h][1-8]\b", texte):
            return 0.1
        return 0.0


def _phrase_coup(rsn: RSN, langue: str) -> str:
    c = _coup_depuis_corps(rsn.corps)
    if c.drapeau == E.ROQUE_K:
        return "petit roque" if langue == "fr" else "castle kingside"
    if c.drapeau == E.ROQUE_Q:
        return "grand roque" if langue == "fr" else "castle queenside"
    # Il faudrait la position pour savoir quelle pièce est en `de` ; la RSN d'un
    # coup ne la porte pas. On rend donc une forme UCI, qui est une surface
    # valide et sans ambiguïté — la phrase naturelle exige le contexte.
    return c.uci()


CODEC = CodecEchecs()

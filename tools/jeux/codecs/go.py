#!/usr/bin/env python3
"""codecs.go — la surface du go : GTP, SGF, diagramme, français.

Trois notations coexistent : **GTP** (`D4`, `pass`), **SGF** (`B[dd]`, `(;…;B[dd];W[pp])`)
et le **diagramme** (`X`/`O`/`.`). La couche française ajoute « pierre noire en
D4 » et « je passe ». Le codec les ramène à la même RSN : un point (ou une
passe), un plateau, un trait, le ko et le komi.

La légalité (occupation, suicide, ko) est validée au niveau 4 par
`regles.go` ; aux niveaux bas, la forme suffit. C'est le même contrat que pour
les autres jeux, et c'est ce qui rend l'ablation comparable.
"""
from __future__ import annotations

import re

from ..grammaire import naturel
from ..rsn import Annotation, RSN
from ..regles import go as G
from .base import Arbre, Codec, Lecture

_RE_GTP = re.compile(r"(?<![A-Za-z])([A-HJ-T])\s*(\d{1,2})(?!\d)", re.I)
_RE_META_TRAIT = re.compile(r"(?:trait|au tour|to move|turn)\s*[:=]?\s*(b|w|noir|blanc|black|white)", re.I)
_RE_META_KOMI = re.compile(r"(?:komi)\s*[:=]?\s*(-?\d+(?:[.,]\d+)?)", re.I)
_RE_META_KO = re.compile(r"(?:ko)\s*[:=]?\s*([A-HJ-T]\d{1,2}|-)", re.I)
_RE_META_PASSE = re.compile(r"(?:passe|passes|pass)\s*[:=]?\s*(\d+)", re.I)


def _komi_dixiemes(s: str) -> int:
    s = s.replace(",", ".")
    if "." in s:
        a, b = s.split(".", 1)
        b = (b + "0")[:1]
        return int(a) * 10 + (int(b) if a not in ("-0", "0") or int(a) == 0 else -int(b))
    return int(s) * 10


def _komi_texte(k: int) -> str:
    return str(k // 10) if k % 10 == 0 else f"{k // 10}.{k % 10}"


def _taille(contexte: RSN | None, defaut: int = 19) -> int:
    if contexte is not None:
        return int(contexte.corps.get("taille", defaut))
    return defaut


def _lignes(texte: str) -> list[str]:
    out = []
    for l in texte.splitlines():
        if not l.strip():
            continue
        out.append(l.rstrip())
    return out


def _est_diagramme(texte: str) -> bool:
    lignes = [l.strip() for l in _lignes(texte) if not re.match(
        r"(?:taille|trait|komi|ko|passe|size|to move|turn)\b", l.strip(), re.I)]
    lignes = [l for l in lignes if re.fullmatch(r"[.XOoxB W]+", l)]
    if len(lignes) < 2:
        return False
    tailles = {len(re.sub(r"\s+", "", l)) for l in lignes}
    return len(tailles) == 1 and len(lignes) == list(tailles)[0]


def _lit_diagramme(texte: str) -> G.Position:
    lignes_brutes = _lignes(texte)
    lignes = []
    for l in lignes_brutes:
        s = l.strip()
        if re.match(r"(?:taille|trait|komi|ko|passe|size|to move|turn)\b", s, re.I):
            continue
        s = re.sub(r"\s+", "", s)
        s = re.sub(r"^\d+\s*[|:]\s*", "", s)
        if re.fullmatch(r"[.XOoxB W]+", s):
            lignes.append(s)
    if not lignes:
        raise G.ErreurGo("diagramme vide")
    n = len(lignes)
    if n < 2 or any(len(l) != n for l in lignes):
        raise G.ErreurGo("diagramme : il faut N lignes de N cases")
    plateau = []
    for l in lignes:
        for ch in l:
            if ch in ".+":
                plateau.append(G.VIDE)
            elif ch in "XxBb":
                plateau.append(G.NOIR)
            elif ch in "OoWw":
                plateau.append(G.BLANC)
            else:
                raise G.ErreurGo(f"diagramme : caractère inconnu {ch!r}")
    trait = G.NOIR
    m = _RE_META_TRAIT.search(texte)
    if m:
        trait = G.NOIR if m.group(1).lower() in ("b", "noir", "black") else G.BLANC
    komi = 65
    m = _RE_META_KOMI.search(texte)
    if m:
        komi = _komi_dixiemes(m.group(1))
    ko = -1
    m = _RE_META_KO.search(texte)
    if m and m.group(1) != "-":
        ko = G.gtp_vers_point(m.group(1), n)
    passe = 0
    m = _RE_META_PASSE.search(texte)
    if m:
        passe = int(m.group(1))
    return G.Position(n, plateau, trait, ko, passe, komi)


def _lit_sgf(texte: str, n_defaut: int = 19) -> tuple[list[int], int, int] | None:
    """Lit un SGF simple : rend (coups, couleur_de_départ, komi) ou None."""
    t = texte.strip()
    if ";" not in t and not re.search(r"\b[BW]\[[a-s]{0,2}\]", t):
        return None
    m = re.search(r"SZ\s*\[\s*(\d+)\s*\]", t)
    if m:
        n = int(m.group(1))
    else:
        n = n_defaut
    komi = 65
    m = re.search(r"KM\s*\[\s*(-?\d+(?:\.\d+)?)\s*\]", t)
    if m:
        komi = _komi_dixiemes(m.group(1))
    coups: list[int] = []
    for m in re.finditer(r"(?:^|;)\s*([BW])\s*\[\s*([a-s]{0,2})\s*\]", t, re.M):
        coups.append(G.sgf_vers_point(m.group(2), n))
    if not coups:
        return None
    return coups, n, komi


class CodecGo(Codec):
    jeu = "go"
    formats = ("diagramme", "gtp", "sgf", "francais", "partie")

    # ------------------------------------------------------------------
    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
            langue: str | None = None) -> Lecture:
        lec = self.lecture(texte, niveau, langue)
        if not texte or not texte.strip():
            return self.echoue(lec, "surface vide")
        n_ctx = _taille(contexte)

        # 1. SGF (état de partie, action ou partie)
        if niveau >= 1 and ("B[" in texte or "W[" in texte) and (
                ";" in texte or re.match(r"\s*[BW]\s*\[", texte)):
            res = _lit_sgf(texte, n_ctx)
            if res is not None:
                coups, n, komi = res
                # une seule action SGF = un coup
                if len(coups) == 1 and not re.search(r";\s*[BW]\s*\[", texte):
                    lec.format = "sgf"
                    nn = n
                    return self.reussi(lec, RSN("go", "coup", {"taille": nn, "point": coups[0]}),
                                       "sgf", 0.95)
                try:
                    pos = G.Position.depart(n, komi)
                    depart = pos.vers_rsn()
                    joues = []
                    for p in coups:
                        if p < 0:
                            pos = pos.passe_tour()
                        else:
                            pos = pos.joue(p)
                        joues.append({"taille": n, "point": p} if p >= 0
                                     else {"taille": n, "passe": True})
                    lec.format = "sgf"
                    return self.reussi(lec, RSN("go", "partie",
                                                {"depart": dict(depart.corps), "coups": joues}),
                                       "sgf", 0.9)
                except Exception as e:
                    return self.echoue(lec, f"SGF illégal : {e}")

        # 2. diagramme = état
        if _est_diagramme(texte):
            if niveau < 1 and re.search(r"[XOoxBbWw]", texte):
                # le diagramme est la forme canonique de l'état : niveau 0
                pass
            try:
                pos = _lit_diagramme(texte)
                if niveau >= 4:
                    if pos.ko >= 0 and pos.plateau[pos.ko] != G.VIDE:
                        raise G.ErreurGo("ko sur une case occupée")
            except Exception as e:
                return self.echoue(lec, f"diagramme invalide : {e}")
            lec.format = "diagramme"
            lec.arbre = Arbre("etat_go", (("taille", pos.n), ("trait", pos.trait),
                                          ("plateau", tuple(pos.plateau))))
            return self.reussi(lec, pos.vers_rsn(), "diagramme", 1.0)

        # 3. action : passe, abandon, ou un point
        t = naturel(texte)
        if (niveau >= 2 and re.search(r"\b(passe|passer|je passe|pass|i pass|skip)\b", t)) or (
                niveau < 2 and t.strip() == "pass"):
            lec.format = "gtp"
            return self.reussi(lec, RSN("go", "coup", {"taille": n_ctx, "passe": True}), "gtp", 0.95)
        if (niveau >= 2 and re.search(r"\b(abandonne|abandon|resign|resigne|demission)\b", t)) or (
                niveau < 2 and t.strip() == "resign"):
            lec.format = "gtp"
            return self.reussi(lec, RSN("go", "coup", {"taille": n_ctx, "abandon": True}), "gtp", 0.95)

        points = self._points(texte, niveau, n_ctx)
        if len(points) == 1:
            p = points[0]
            if contexte is not None and niveau >= 4:
                try:
                    pos = G.Position.depuis_rsn(contexte)
                    if not pos.coup_legal(p):
                        return self.echoue(lec, f"coup illégal en {G.point_vers_gtp(p, pos.n)}")
                except Exception as e:
                    return self.echoue(lec, f"position de contexte invalide : {e}")
            lec.format = "gtp"
            lec.arbre = Arbre("coup_go", (("point", p),))
            return self.reussi(lec, RSN("go", "coup", {"taille": n_ctx, "point": p}), "gtp", 0.95,
                               [] if contexte is not None or niveau < 4 else ["position requise pour valider"])

        return self.echoue(lec, "aucune lecture de go (diagramme, GTP, SGF ou passe)")

    def _points(self, texte: str, niveau: int, n: int = 19) -> list[int]:
        t = texte.strip()
        # SGF ponctuel B[dd] / W[pp] / B[]
        m = re.fullmatch(r"\s*([BW])\s*\[\s*([a-s]{0,2})\s*\]\s*", t, re.I)
        if m:
            p = G.sgf_vers_point(m.group(2), n)
            return [] if p < 0 else [p]
        # coordonnée GTP en tête
        m = _RE_GTP.fullmatch(t)
        if m:
            try:
                return [G.gtp_vers_point(m.group(1) + m.group(2), n)]
            except G.ErreurGo:
                return []
        # « pierre noire en D4 », « jouer en D4 », « en D4 »
        if niveau >= 2:
            ms = list(_RE_GTP.finditer(t))
            if len(ms) == 1:
                try:
                    return [G.gtp_vers_point(ms[0].group(1) + ms[0].group(2), n)]
                except G.ErreurGo:
                    pass
        # ligne 4 colonne 4
        if niveau >= 2:
            m = re.search(r"(?:ligne|row)\s*(\d{1,2})\s*(?:et|,)?\s*(?:colonne|column)\s*(\d{1,2})", t, re.I)
            if m:
                return [G.ligne_colonne_vers_point(int(m.group(1)), int(m.group(2)), n)]
        return []

    # ------------------------------------------------------------------
    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
             contexte: RSN | None = None) -> str:
        if rsn.jeu != "go":
            raise ValueError("ce n'est pas une RSN de go")
        if rsn.nature == "etat":
            pos = G.Position.depuis_rsn(rsn, valide=False)
            if format in ("diagramme", "canonique"):
                lignes = []
                for row in range(pos.n):
                    ligne = []
                    for col in range(pos.n):
                        p = pos.plateau[row * pos.n + col]
                        ligne.append("." if p == G.VIDE else ("X" if p == G.NOIR else "O"))
                    lignes.append("".join(ligne))
                trait = "b" if pos.trait == G.NOIR else "w"
                ko = G.point_vers_gtp(pos.ko, pos.n) if pos.ko >= 0 else "-"
                return "\n".join(lignes) + (
                    f"\ntaille: {pos.n} trait: {trait} komi: {_komi_texte(pos.komi)} "
                    f"ko: {ko} passe: {pos.passe}")
            if format == "sgf":
                return self._sgf_etat(pos)
            raise ValueError(f"format d'état inconnu : {format}")
        if rsn.nature == "coup":
            if rsn.corps.get("passe"):
                return "pass" if format in ("gtp", "canonique") else "je passe"
            if rsn.corps.get("abandon"):
                return "resign" if format in ("gtp", "canonique") else "j'abandonne"
            p = int(rsn.corps["point"])
            n = int(rsn.corps.get("taille") or _taille(contexte))
            if format in ("gtp", "canonique"):
                return G.point_vers_gtp(p, n)
            if format == "sgf":
                couleur = "B"
                if contexte is not None:
                    couleur = "B" if int(contexte.corps["trait"]) == G.NOIR else "W"
                return f"{couleur}[{G.point_vers_sgf(p, n)}]"
            if format == "francais":
                couleur = "noire"
                if contexte is not None and int(contexte.corps["trait"]) == G.BLANC:
                    couleur = "blanche"
                return f"pierre {couleur} en {G.point_vers_gtp(p, n)}"
            raise ValueError(f"format de coup inconnu : {format}")
        if rsn.nature == "partie":
            depart = RSN("go", "etat", dict(rsn.corps["depart"]))
            pos = G.Position.depuis_rsn(depart)
            n = pos.n
            coups = []
            for a in rsn.corps.get("coups", []):
                if a.get("passe"):
                    coups.append(("B" if pos.trait == G.NOIR else "W", ""))
                    pos = pos.passe_tour()
                elif a.get("abandon"):
                    break
                else:
                    p = int(a["point"])
                    coups.append(("B" if pos.trait == G.NOIR else "W", G.point_vers_sgf(p, n)))
                    pos = pos.joue(p)
            if format in ("sgf", "canonique"):
                corps = ";".join(f"{c}[{s}]" for c, s in coups)
                return f"(;GM[1]FF[4]SZ[{n}]KM[{_komi_texte(pos.komi)}];{corps})"
            if format == "gtp":
                return " ".join(G.point_vers_gtp(G.sgf_vers_point(s, n), n) if s else "pass"
                                for _, s in coups)
            raise ValueError(f"format de partie inconnu : {format}")
        raise ValueError(f"nature inconnue : {rsn.nature}")

    def _sgf_etat(self, pos: G.Position) -> str:
        noirs = [G.point_vers_sgf(p, pos.n) for p in range(pos.n * pos.n)
                 if pos.plateau[p] == G.NOIR]
        blancs = [G.point_vers_sgf(p, pos.n) for p in range(pos.n * pos.n)
                  if pos.plateau[p] == G.BLANC]
        setup = ""
        if noirs:
            setup += "AB[" + "][".join(noirs) + "]"
        if blancs:
            setup += "AW[" + "][".join(blancs) + "]"
        return (f"(;GM[1]FF[4]SZ[{pos.n}]KM[{_komi_texte(pos.komi)}]{setup}"
                f"PL[{'B' if pos.trait == G.NOIR else 'W'}])")

    # ------------------------------------------------------------------
    def detecte(self, texte: str) -> float:
        t = texte.lower()
        if "go" in t.split() or "weiqi" in t or "baduk" in t:
            return 0.9
        if "(;" in texte or re.search(r"\b[BW]\[\s*[a-s]{0,2}\s*\]", texte):
            return 0.95
        if _est_diagramme(texte):
            return 0.9
        if re.search(r"\b(pierre|stone)\b", t) and _RE_GTP.search(texte):
            return 0.8
        if re.search(r"(?:ligne|row)\s*(?:[4-9]|[12]\d)\b", texte, re.I):
            return 0.7
        if re.fullmatch(r"\s*[A-HJ-T]\s*\d{1,2}\s*", texte):
            return 0.35
        if re.search(r"\b(passe|pass|passer|je passe|resign|abandonne)\b", t):
            return 0.25
        return 0.0


CODEC = CodecGo()

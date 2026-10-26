#!/usr/bin/env python3
"""codecs.dames — la surface des dames anglaises.

Trois écritures pour le même état : le **compact** (32 caractères + trait), le
**diagramme** 8×8, et les actions numériques (`11x18x27`) ou algébriques
(`c3xe5xg7`). La couche française ajoute « le pion de c3 prend en e5 ».

La difficulté propre aux dames est que **le chemin est l'action** : `c3xe5xg7`
n'est pas trois cases, c'est une prise multiple que les règles doivent valider.
C'est pourquoi le codec ne se contente pas d'extraire des cases : il appelle
`regles.dames` au niveau 4, et c'est cette validation qui rend la mesure honnête.
"""
from __future__ import annotations

import re

from ..grammaire import naturel
from ..lexique import LEX
from ..rsn import Annotation, RSN
from ..regles import dames as D
from .base import Arbre, Codec, Lecture

_RE_COMPACT = re.compile(r"^\s*([bwBW.]{32})(?:\s+([bw])(?:\s+(\d+))?)?\s*$")
_RE_NUM = re.compile(r"(?<![a-h0-9])(?:[1-9]|[12][0-9]|3[0-2])(?!\d)")
_RE_ALG = re.compile(r"(?<![a-h])[a-h][1-8]")


def _pieces_depuis_compact(s: str) -> list[str]:
    s = s.strip()
    if len(s) != 32 or any(c not in "bwBW." for c in s):
        raise D.ErreurDames(f"compact invalide : {s!r}")
    return list(s)


def _est_compact(texte: str) -> bool:
    return bool(_RE_COMPACT.fullmatch(texte))


def _lignes(texte: str) -> list[str]:
    out = []
    for l in texte.splitlines():
        l = l.strip()
        if not l:
            continue
        l = re.sub(r"^\d+\s*[|:]\s*", "", l)
        if re.fullmatch(r"[a-h](?:\s+[a-h]){7}", l):
            continue
        if re.match(r"(?:trait|demi|roques?|ep|au tour|to move|turn)\b", l, re.I):
            continue
        out.append(l)
    return out


def _est_diagramme(texte: str) -> bool:
    lignes = _lignes(texte)
    if len(lignes) != 8:
        return False
    for l in lignes:
        s = re.sub(r"\s+", "", l)
        if len(s) != 8 or not re.fullmatch(r"[-.·bwBW]+", s):
            return False
    return any(c in "bwBW" for l in lignes for c in l)


def _lit_diagramme(texte: str) -> D.Position:
    lignes = _lignes(texte)
    if len(lignes) != 8:
        raise D.ErreurDames("diagramme : il faut 8 rangées")
    cases = [D.VIDE] * 32
    for row, l in enumerate(lignes):
        s = re.sub(r"\s+", "", l)
        if len(s) != 8:
            raise D.ErreurDames(f"diagramme : rangée {row + 1} fait {len(s)} cases")
        for col, ch in enumerate(s):
            if (row + col) % 2 == 0:
                continue  # case claire
            i = D._num(row, col) - 1
            if ch in ".·":
                cases[i] = D.VIDE
            elif ch in "bwBW":
                cases[i] = D._CAR_TO_INT[ch]
            elif ch == "-":
                continue
            else:
                raise D.ErreurDames(f"diagramme : caractère inconnu {ch!r}")
    trait = D.NOIR
    m = re.search(r"(?:trait|au tour|to move|turn)\s*[:=]?\s*(b|w|noir|blanc|black|white)", texte, re.I)
    if m:
        trait = D.NOIR if m.group(1).lower() in ("b", "noir", "black") else D.BLANC
    demi = 0
    m = re.search(r"(?:demi|halfmove)\s*[:=]\s*(\d+)", texte, re.I)
    if m:
        demi = int(m.group(1))
    return D.Position(cases, trait, demi)


def _lit_compact(texte: str) -> D.Position:
    m = _RE_COMPACT.fullmatch(texte)
    if not m:
        raise D.ErreurDames("compact illisible")
    cases = [D._CAR_TO_INT[c] for c in m.group(1)]
    trait = D.NOIR if (m.group(2) or "b") == "b" else D.BLANC
    demi = int(m.group(3) or 0)
    return D.Position(cases, trait, demi)


def _carres(texte: str) -> tuple[list[int], str]:
    """Extrait les cases d'une action, en choisissant numérique ou algébrique."""
    t = naturel(texte)
    nums = [int(x) for x in _RE_NUM.findall(t)]
    algs = []
    for x in _RE_ALG.findall(t):
        try:
            algs.append(D.case_vers_indice(x))
        except ValueError:
            pass
    if len(nums) >= len(algs) and nums:
        return [n - 1 for n in nums], "numerique"
    return algs, "algebrique"


def _est_prise(texte: str) -> bool:
    t = naturel(texte)
    return ("x" in t or "prend" in t or "capture" in t or "mange" in t
            or "take" in t or "jump" in t)


class CodecDames(Codec):
    jeu = "dames"
    formats = ("compact", "diagramme", "numerique", "algebrique", "francais", "liste")

    # ------------------------------------------------------------------
    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
            langue: str | None = None) -> Lecture:
        lec = self.lecture(texte, niveau, langue)
        if not texte or not texte.strip():
            return self.echoue(lec, "surface vide")

        # 1. état compact
        if _est_compact(texte):
            try:
                pos = _lit_compact(texte)
                if niveau >= 4:
                    # validation : pions pas sur la rangée de promotion
                    D.position_depuis_rsn(D.rsn_depuis_position(pos), valide=True)
            except Exception as e:
                return self.echoue(lec, f"état compact invalide : {e}")
            lec.format = "compact"
            lec.arbre = Arbre("etat_dames", (("cases", tuple(pos.cases)), ("trait", pos.trait)))
            return self.reussi(lec, D.rsn_depuis_position(pos), "compact", 1.0)

        # 2. diagramme
        if niveau >= 1 and _est_diagramme(texte):
            try:
                pos = _lit_diagramme(texte)
                if niveau >= 4:
                    D.position_depuis_rsn(D.rsn_depuis_position(pos), valide=True)
            except Exception as e:
                return self.echoue(lec, f"diagramme invalide : {e}")
            lec.format = "diagramme"
            return self.reussi(lec, D.rsn_depuis_position(pos), "diagramme", 0.95)

        # 3. action(s)
        if niveau >= 0:
            # une partie = plusieurs actions séparées
            if niveau >= 1 and re.search(r"[,;\n]", texte):
                partie = self._lit_partie(texte, niveau)
                if partie is not None:
                    lec.format = "liste"
                    return self.reussi(lec, partie, "liste", 0.9)

            carres, forme = _carres(texte)
            if len(carres) >= 2:
                # niveau 0 : le numérique seul ; niveau 1 : l'algébrique aussi
                if niveau < 1 and forme != "numerique":
                    return self.echoue(lec, "forme algébrique : niveau 1")
                # niveau 2 : les mots français (pion, dame, prend)
                if niveau < 2 and re.search(r"[a-zA-Z]{3,}", texte) and forme == "numerique":
                    return self.echoue(lec, "mots français : niveau 2")
                coup = D.Coup(tuple(carres))
                if contexte is not None and niveau >= 4:
                    try:
                        pos = D.position_depuis_rsn(contexte)
                        if coup not in pos.coups_legaux():
                            return self.echoue(lec, f"coup illégal : {coup.numerique()}")
                    except Exception as e:
                        return self.echoue(lec, f"position de contexte invalide : {e}")
                lec.format = "algebrique" if forme == "algebrique" else "numerique"
                lec.arbre = Arbre("coup_dames", (("chemin", tuple(carres)), ("forme", forme)))
                return self.reussi(lec, D.action_depuis_coup(coup), lec.format, 1.0,
                                   [] if contexte is not None or niveau < 4 else ["position requise pour valider"])

        return self.echoue(lec, "aucune lecture de dames")

    def _lit_partie(self, texte: str, niveau: int) -> RSN | None:
        depart = D.rsn_depuis_position(D.Position.depart())
        pos = D.position_depuis_rsn(depart)
        segments = [s.strip() for s in re.split(r"[,;\n]+", texte) if s.strip()]
        if len(segments) < 2:
            return None
        coups = []
        for seg in segments:
            carres, _ = _carres(seg)
            if len(carres) < 2:
                return None
            c = D.Coup(tuple(carres))
            if niveau >= 4:
                if c not in pos.coups_legaux():
                    return None
            pos = pos.applique(c)
            coups.append(c)
        return D.rsn_partie(depart, coups)

    # ------------------------------------------------------------------
    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
             contexte: RSN | None = None) -> str:
        if rsn.jeu != "dames":
            raise ValueError("ce n'est pas une RSN de dames")
        if rsn.nature == "etat":
            pos = D.position_depuis_rsn(rsn, valide=False)
            if format in ("compact", "canonique"):
                s = "".join(D._INT_TO_CAR[p] for p in pos.cases)
                t = "b" if pos.trait == D.NOIR else "w"
                return s + " " + t + (f" {pos.demi}" if pos.demi else "")
            if format == "diagramme":
                lignes = []
                for row in range(8):
                    ligne = []
                    for col in range(8):
                        if (row + col) % 2 == 0:
                            ligne.append("-")
                        else:
                            i = D._num(row, col) - 1
                            ligne.append(D._INT_TO_CAR[pos.cases[i]] if pos.cases[i] else ".")
                    lignes.append(" ".join(ligne))
                trait = "trait: b" if pos.trait == D.NOIR else "trait: w"
                return "\n".join(lignes) + f"\n{trait}"
            raise ValueError(f"format d'état inconnu : {format}")
        if rsn.nature == "coup":
            c = D.coup_depuis_action(rsn)
            prise = len(c.chemin) > 2
            if contexte is not None:
                try:
                    pos = D.position_depuis_rsn(contexte)
                    prise = pos.est_prise(c)
                except Exception:
                    pass
            if format in ("numerique", "canonique"):
                sep = "x" if prise else "-"
                return sep.join(str(i + 1) for i in c.chemin)
            if format == "algebrique":
                sep = "x" if prise else "-"
                return sep.join(D.indice_vers_case(i) for i in c.chemin)
            if format == "francais":
                return _phrase(rsn, contexte, langue, prise)
            raise ValueError(f"format de coup inconnu : {format}")
        if rsn.nature == "partie":
            pos, coups = D.partie_depuis_rsn(rsn)
            if format in ("liste", "canonique"):
                return " ".join(c.numerique() for c in coups)
            if format == "algebrique":
                return " ".join(c.algebrique() for c in coups)
            raise ValueError(f"format de partie inconnu : {format}")
        raise ValueError(f"nature inconnue : {rsn.nature}")

    # ------------------------------------------------------------------
    def detecte(self, texte: str) -> float:
        t = texte.lower()
        if "dames" in t or "checkers" in t or "draughts" in t:
            return 0.95
        if _est_compact(texte):
            return 0.95
        if _est_diagramme(texte):
            return 0.9
        carres, forme = _carres(texte)
        if len(carres) >= 2 and ("x" in t or "-" in t):
            if forme == "numerique" and all(1 <= c + 1 <= 32 for c in carres):
                return 0.45
            if forme == "algebrique":
                return 0.2
        return 0.0


def _phrase(rsn: RSN, contexte: RSN | None, langue: str, prise: bool) -> str:
    c = D.coup_depuis_action(rsn)
    if contexte is None:
        return c.numerique()
    try:
        pos = D.position_depuis_rsn(contexte)
    except Exception:
        return c.numerique()
    piece = pos.cases[c.chemin[0]]
    if piece == D.VIDE:
        return c.numerique()
    nom = "pion" if piece in (D.NOIR_PION, D.BLANC_PION) else "dame"
    if langue == "en":
        nom = "man" if nom == "pion" else "king"
    debut = D.indice_vers_case(c.chemin[0])
    if len(c.chemin) == 2:
        fin = D.indice_vers_case(c.chemin[1])
        if prise:
            return f"le {nom} {debut} prend en {fin}" if langue == "fr" else f"the {nom} {debut} captures {fin}"
        return f"le {nom} de {debut} vers {fin}" if langue == "fr" else f"the {nom} from {debut} to {fin}"
    prises = [D.indice_vers_case(i) for i in c.chemin[1:]]
    if langue == "fr":
        return f"le {nom} {debut} prend en " + " puis en ".join(prises)
    return f"the {nom} {debut} captures " + " then ".join(prises)


CODEC = CodecDames()

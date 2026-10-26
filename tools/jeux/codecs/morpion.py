#!/usr/bin/env python3
"""codecs.morpion — la surface du morpion : grilles, cases, phrases.

Le morpion est le jeu le plus simple du contrat, et c'est pour ça qu'il sert de
**calibration** aux couches : une grille est un état, une case est un coup, une
suite de cases est une partie. On y voit les quatre couches à l'œuvre sans le
bruit des règles d'échecs.

Formats de surface reconnus :
- état : `XOX/.../...`, `X O X | . . . | . . .`, diagramme sur trois lignes,
  `X,O,X,.,.,.,.,.,.`, avec `trait: O` / `au tour de O` ;
- coup : `A1`, `(1,2)`, `ligne 2 colonne 3`, `milieu`, `haut gauche`, `X A1`,
  « la croix joue en haut à gauche », « X plays top left » ;
- partie : `A1 B2 C3`, `A1, B2, C3`, ou `X A1 O B2 X C3`.
"""
from __future__ import annotations

import re

from ..grammaire import naturel, nombre, segmente
from ..lexique import LEX, plie
from ..lexique_multilingue import MULTI
from ..rsn import Annotation, RSN
from ..regles import morpion as regles
from .base import Arbre, Codec, Lecture

_LIGNES_GAGNANTES = regles.LIGNES


def _case_coord(ligne: int, colonne: int) -> int:
    """Ligne 0 = haut, colonne 0 = gauche → indice 0..8."""
    return ligne * 3 + colonne


def _coord_case(i: int) -> tuple[int, int]:
    return divmod(i, 3)


def _nom_case(i: int, langue: str = "fr") -> str:
    formes = LEX.formes("morpion.case", str(i), langue)
    if formes:
        # la forme la plus « humaine » : la première déclarée
        return formes[0]
    l, c = _coord_case(i)
    return f"{'ABC'[l]}{c + 1}"


def _lit_case(texte: str, niveau: int, langue: str | None = None) -> tuple[int | None, list[str]]:
    """Une case, de la plus formelle à la plus naturelle. Rend (indice, ambiguïtés)."""
    t = naturel(texte)
    if not t:
        return None, []
    # 1. coordonnée canonique A1..C3 (niveau 0) — la casse est pliée par `naturel`.
    m = re.fullmatch(r"([abc])\s*([123])", t)
    if m:
        # convention : la LETTRE est la colonne, le CHIFFRE la ligne (A1 = haut gauche)
        return _case_coord(int(m.group(2)) - 1, "abc".index(m.group(1))), []
    # 2. (ligne, colonne), ligne 2 colonne 3, r2c3, 2,3
    m = re.fullmatch(r"\(?\s*([123])\s*[,; ]\s*([123])\s*\)?", t)
    if m:
        return _case_coord(int(m.group(1)) - 1, int(m.group(2)) - 1), []
    m = re.fullmatch(r"r\s*([123])\s*c\s*([123])", t)
    if m:
        return _case_coord(int(m.group(1)) - 1, int(m.group(2)) - 1), []
    m = re.search(r"ligne\s*([123])\s*(?:et\s*)?colonne\s*([123])", t) or \
        re.search(r"rangee\s*([123])\s*(?:et\s*)?colonne\s*([123])", t) or \
        re.search(r"row\s*([123])\s*(?:and\s*)?column\s*([123])", t)
    if m:
        return _case_coord(int(m.group(1)) - 1, int(m.group(2)) - 1), []
    # 3. « case N » (1..9), à partir du niveau 1
    if niveau >= 1:
        m = re.fullmatch(r"(?:case|cell|square|case numero|case n)\s*([1-9])", t)
        if m:
            return int(m.group(1)) - 1, []
        m = re.fullmatch(r"([1-9])", t)
        if m:
            return int(m.group(1)) - 1, []
    # 4. le lexique des neuf cases nommées (niveau 2)
    if niveau >= 2:
        cs = LEX.cherche("morpion.case", t, langues=(langue,) if langue else ("fr", "en"))
        if cs:
            return int(cs[0].concept), [c.concept for c in cs[1:]]
        # une forme peut être précédée d'un article ou d'un verbe
        for u in re.findall(r"[a-z]+", t):
            cs = LEX.cherche("morpion.case", u, langues=(langue,) if langue else ("fr", "en"))
            if cs:
                return int(cs[0].concept), []
    # 5. « ligne 2, colonne 3 » avec un mot pour le nombre (niveau 3)
    if niveau >= 3:
        m = re.search(r"(?:ligne|rangee|row)\s+([a-z0-9]+)\s*(?:et|,)?\s*(?:colonne|column)\s+([a-z0-9]+)", t)
        if m:
            l = nombre(m.group(1))
            c = nombre(m.group(2))
            if l and c and 1 <= l <= 3 and 1 <= c <= 3:
                return _case_coord(l - 1, c - 1), []
    return None, []


def _lit_symbole(texte: str, niveau: int) -> tuple[str | None, list[str]]:
    t = naturel(texte)
    if niveau < 2:
        m = re.fullmatch(r"([xo])", t)
        return (m.group(1).upper() if m else None), []
    # un symbole explicite en tête de phrase
    cs = LEX.cherche("morpion.symbole", t.split()[0] if t.split() else "")
    if cs:
        return cs[0].concept, [c.concept for c in cs[1:]]
    m = re.search(r"\b(x|croix|ex|iks|o|rond|cercle|zero|oh|cross|nought|naught|circle)\b", t)
    if m:
        cs = LEX.cherche("morpion.symbole", m.group(0))
        if cs:
            return cs[0].concept, []
    return None, []


def _cases_depuis_grille(texte: str, niveau: int) -> tuple[list[str | None] | None, str | None, list[str]]:
    """Lit une grille 3×3 ; rend (cases, trait explicite, ambiguïtés)."""
    brut = texte.strip()
    # enlève un préfixe de présentation
    brut = re.sub(r"^\s*(?:grille|plateau|position|grid|board|etat|état)\s*(?:est|:|=)?\s*",
                  "", brut, flags=re.I)
    # trait explicite
    trait = None
    m = re.search(r"(?:trait|au tour de|tour de|to move|turn)\s*[:=]?\s*(x|o|croix|rond|cross|nought|naught)",
                  brut, re.I)
    if m:
        s, _ = _lit_symbole(m.group(1), max(2, niveau))
        trait = s
        brut = brut[:m.start()] + brut[m.end():]
    brut = brut.strip()
    if not brut:
        return None, trait, []

    # 3 lignes séparées par / | retour à la ligne
    morceaux = segmente(brut, r"[/|\n]+")
    if len(morceaux) == 3:
        lignes = []
        for morceau in morceaux:
            # chaque ligne : XOX, X O X, X,O,X, X O X (3 cases)
            cellules = re.findall(r"[xXoO0.\-_ ]+", morceau)
            s = "".join(cellules).replace(" ", "")
            s = s.replace(",", "")
            if len(s) != 3:
                # peut-être des mots (croix, rond, vide) : on les lit au lexique
                mots = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+|[.]", morceau)
                if len(mots) == 3:
                    vals = []
                    for mot in mots:
                        if mot in ".-_":
                            vals.append(None)
                            continue
                        c, _ = _lit_symbole(mot, max(2, niveau))
                        vals.append(c if c in ("X", "O") else None)
                    lignes.append(vals)
                    continue
                return None, trait, []
            vals = []
            for ch in s:
                if ch in "._-":
                    vals.append(None)
                elif ch in "xX":
                    vals.append("X")
                elif ch in "oO0":
                    vals.append("O")
                else:
                    return None, trait, []
            lignes.append(vals)
        return [v for l in lignes for v in l], trait, []

    # 9 cases à plat séparées par des espaces/virgules
    jetons_ = [u for u in re.split(r"[\s,;]+", brut) if u]
    if len(jetons_) == 9:
        vals = []
        for u in jetons_:
            if u in ".-_":
                vals.append(None)
                continue
            c, _ = _lit_symbole(u, max(2, niveau)) if niveau >= 2 else (
                (u.upper() if u.lower() in ("x", "o") else None), [])
            if c not in ("X", "O"):
                return None, trait, []  # un mot inconnu n'est pas une case vide
            vals.append(c)
        return vals, trait, []

    # 9 caractères collés
    s = re.sub(r"[\s,;]+", "", brut)
    if len(s) == 9:
        vals = []
        for ch in s:
            if ch in "._-":
                vals.append(None)
            elif ch in "xX":
                vals.append("X")
            elif ch in "oO0":
                vals.append("O")
            else:
                return None, trait, []
        return vals, trait, []

    return None, trait, []


def _trait_derive(cases: list[str | None]) -> tuple[str | None, str | None]:
    """Le trait se déduit des comptes ; rend (trait, erreur)."""
    x = cases.count("X")
    o = cases.count("O")
    if x == o:
        return "X", None
    if x == o + 1:
        return "O", None
    return None, f"comptes impossibles : {x} X contre {o} O"


class CodecMorpion(Codec):
    jeu = "morpion"
    formats = ("grille", "diagramme", "canonique", "cellule", "texte", "liste", "naturel")

    # ------------------------------------------------------------------
    # Lecture
    # ------------------------------------------------------------------
    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
            langue: str | None = None) -> Lecture:
        lec = self.lecture(texte, niveau, langue, format="inconnu")
        if not texte or not texte.strip():
            return self.echoue(lec, "surface vide")
        texte = self.sans_nom_jeu(texte)

        # 1. une grille = un état
        cases, trait_exp, ambiguites = _cases_depuis_grille(texte, niveau)
        if cases is not None:
            lec.format = "grille"
            lec.ambiguites = tuple(ambiguites)
            if niveau < 4:
                # aux niveaux bas, on ne vérifie pas la cohérence des comptes
                trait = trait_exp or ("O" if cases.count("X") == cases.count("O") + 1 else "X")
            else:
                trait, err = _trait_derive(cases)
                if err:
                    return self.echoue(lec, err)
                if trait_exp is not None and trait_exp != trait:
                    return self.echoue(lec, f"le trait annoncé ({trait_exp}) contredit les comptes (attendu {trait})")
            rsn = RSN("morpion", "etat", {"taille": 3, "cases": cases, "trait": trait})
            lec.arbre = Arbre("etat_morpion", (("cases", tuple(c if c else "." for c in cases)),
                                               ("trait", trait)))
            return self.reussi(lec, rsn, "grille", 1.0, ambiguites)

        # 2. un coup = une case (+ un symbole éventuel)
        symbole, amb_s = _lit_symbole(texte, niveau)
        # on enlève le symbole et le verbe pour isoler la case
        reste = texte
        if symbole:
            reste = re.sub(r"\b(x|croix|ex|iks|o|rond|cercle|zero|oh|cross|nought|naught|circle)\b",
                           " ", reste, count=1, flags=re.I)
        reste = re.sub(r"\b(joue|jouer|va|aller|deplace|deplacer|prend|prendre|pose|poser|place|placer|"
                       r"play|plays|move|moves|go|goes|put|puts|place|places)\b",
                       " ", reste, count=1, flags=re.I)
        reste = re.sub(r"\b(en|au|a|dans|sur|sur la|in|at|on|to|the|le|la|les|case|cell|square)\b",
                       " ", reste, flags=re.I)
        reste = re.sub(r"\s+", " ", reste).strip(" ,.;:!")
        if reste:
            i, amb_c = _lit_case(reste, niveau, langue)
            if i is not None:
                lec.format = "cellule"
                lec.ambiguites = tuple(amb_s + amb_c)
                if contexte is not None:
                    if niveau >= 4:
                        ok, pourquoi = regles.coup_valide(
                            contexte, RSN("morpion", "coup", {"case": i, "symbole": symbole}))
                        if not ok:
                            return self.echoue(lec, pourquoi)
                    # le symbole est une conséquence du trait, pas une opinion de
                    # la surface : on le résout dès qu'on a la position.
                    if symbole is None:
                        symbole = regles.trait(contexte)
                rsn = RSN("morpion", "coup", {"case": i, "symbole": symbole})
                lec.arbre = Arbre("coup_morpion", (("case", i), ("symbole", symbole)))
                return self.reussi(lec, rsn, "cellule", 1.0, lec.ambiguites)

        # 3. une partie = une suite de cases
        if niveau >= 0:
            morceaux = [m for m in re.split(r"[\s,;]+", texte.strip()) if m]
            # enlève les numéros de tour « 1. », « 2. »
            morceaux = [m for m in morceaux if not re.fullmatch(r"\d+[.)]?", m)]
            if len(morceaux) >= 2:
                indices: list[int] = []
                symboles: list[str | None] = []
                ok = True
                en_attente: str | None = None
                for m in morceaux:
                    s, _ = _lit_symbole(m, niveau)
                    if s is not None and len(m) <= 10 and not re.search(r"\d", m):
                        # un symbole seul : il annonce la case qui suit
                        if en_attente is not None:
                            ok = False
                            break
                        en_attente = s
                        continue
                    mm = re.sub(r"\b(x|croix|o|rond|cross|nought|naught)\b", " ", m, flags=re.I)
                    i, _ = _lit_case(mm, niveau, langue)
                    if i is None:
                        ok = False
                        break
                    indices.append(i)
                    symboles.append(en_attente)
                    en_attente = None
                if en_attente is not None:
                    ok = False
                if ok and len(indices) >= 2:
                    lec.format = "liste"
                    # le final est DÉRIVABLE à tous les niveaux ; la validation
                    # de la légalité, elle, est le travail du niveau 4.
                    etat = regles.etat_initial()
                    for k, i in enumerate(indices):
                        s = symboles[k] if k < len(symboles) else None
                        if s is not None and s != regles.trait(etat):
                            if niveau >= 4:
                                return self.echoue(lec, f"coup {k + 1} : {s} joue hors de son tour")
                        if regles.terminal(etat) or etat.corps["cases"][i] is not None:
                            if niveau >= 4:
                                return self.echoue(lec, f"coup {k + 1} : illégal")
                            break
                        etat = regles.applique_indice(etat, i)
                    rsn = RSN("morpion", "partie",
                              {"taille": 3, "coups": indices,
                               "final": list(etat.corps["cases"])})
                    lec.arbre = Arbre("partie_morpion", (("coups", tuple(indices)),))
                    return self.reussi(lec, rsn, "liste", 0.95)

        return self.echoue(lec, "aucune lecture de morpion (grille, case ou partie)")

    # ------------------------------------------------------------------
    # Restitution
    # ------------------------------------------------------------------
    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
             contexte: RSN | None = None) -> str:
        if rsn.jeu != "morpion":
            raise ValueError("ce n'est pas une RSN de morpion")
        if rsn.nature == "etat":
            cases = list(rsn.corps.get("cases", []))
            if format in ("grille", "canonique", "ligne"):
                return "/".join("".join(c if c else "." for c in cases[i:i + 3])
                                for i in range(0, 9, 3))
            if format == "diagramme":
                return "\n".join(" ".join(c if c else "." for c in cases[i:i + 3])
                                 for i in range(0, 9, 3))
            raise ValueError(f"format d'état inconnu : {format}")
        if rsn.nature == "coup":
            i = int(rsn.corps.get("case"))
            s = rsn.corps.get("symbole")
            if format in ("canonique", "cellule"):
                return f"{'ABC'[i % 3]}{i // 3 + 1}"
            if format == "texte":
                return f"{s} {'ABC'[i % 3]}{i // 3 + 1}" if s else f"{'ABC'[i % 3]}{i // 3 + 1}"
            if format == "naturel":
                nom = _nom_case(i, langue)
                if s:
                    return f"{s} joue en {nom}"
                return f"jouer en {nom}"
            raise ValueError(f"format de coup inconnu : {format}")
        if rsn.nature == "partie":
            coups = [int(c) for c in rsn.corps.get("coups", [])]
            if format in ("canonique", "liste"):
                return " ".join(f"{'ABC'[i % 3]}{i // 3 + 1}" for i in coups)
            if format == "naturel":
                return " puis ".join(f"jouer en {_nom_case(i, langue)}" for i in coups)
            raise ValueError(f"format de partie inconnu : {format}")
        raise ValueError(f"nature inconnue : {rsn.nature}")

    # ------------------------------------------------------------------
    # Détection
    # ------------------------------------------------------------------
    def detecte(self, texte: str) -> float:
        t = texte.lower()
        if "morpion" in t or "tic-tac-toe" in t or "tic tac toe" in t or "noughts and crosses" in t:
            return 0.95
        cases, _, _ = _cases_depuis_grille(texte, 1)
        if cases is not None and not re.search(r"[a-h][1-8].*[a-h][1-8]", t):
            return 0.9
        # une suite de coups X/O (X A1 O B2) est du morpion, pas une grille
        if (len(re.findall(r"\b[XO]\b", texte)) >= 2
                and re.search(r"\b[A-C][1-3]\b", texte)):
            return 0.85
        # une case seule est ambiguë (échecs, dames, go) : confiance faible
        if _lit_case(texte, 2)[0] is not None and len(texte.split()) <= 4:
            return 0.5
        return 0.0


CODEC = CodecMorpion()

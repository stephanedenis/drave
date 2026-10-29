#!/usr/bin/env python3
"""bloc_maths.py — R4.3 : une formule est un AST évalué exactement, pas une surface.

POURQUOI CE FICHIER. Une formule mathématique n'est pas du texte : `\\frac{1}{3}+\\frac{1}{6}`
vaut `1/2`, et cette valeur n'est écrite nulle part. R0.1 range les formules en région
`maths` et le texte reste du texte ; un lecteur de surface peut retrouver les chiffres,
jamais la valeur. Le bloc classique, lui, parse, évalue exactement (fractions) et dérive —
pour un coût constant.

Ce que ce bloc ajoute, et qui se vérifie :
  1. **le parseur** — un sous-ensemble LaTeX : nombres, variables, `+ - * / ^`, `\\frac`,
     `\\sqrt`, `\\pi`, fonctions usuelles, parenthèses et accolades, équations `a = b` ;
     une macro inconnue ou une accolade non fermée est **refusée en la nommant** ;
  2. **l'évaluation exacte** — `fractions.Fraction` : `1/3 + 1/6 = 1/2`, `2^{-3} = 1/8` ;
     les irrationnels (π, sin, √2) passent en flottant, et le disent ;
  3. **la dérivation** — règles somme, produit, quotient, puissance et chaîne ;
  4. **la résolution** — une équation linéaire `ax + b = c` est résolue exactement ; une
     équation non linéaire est **refusée**, pas approximée ;
  5. **l'oracle indépendant** — chaque résultat est recoupé par **sympy** (évaluation,
     dérivée, solution) : deux implémentations, un même nombre, ou le test échoue.

La règle du dépôt : **classique d'abord** quand l'information est explicite. Une formule
est le cas le plus explicite qui soit.

Usage :
  python3 tools/bloc_maths.py --porte
  python3 tools/bloc_maths.py --mesure reports/r43-bloc-maths.json
  python3 tools/bloc_maths.py --calcule "\\frac{1}{3}+\\frac{1}{6}"
  python3 tools/bloc_maths.py --derive "x^2+3x" --var x
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import re
import sys
import time
from fractions import Fraction

RACINE = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = RACINE / "tools" / "tests" / "maths"


# ------------------------------------------------------------------ les exceptions

class Refus(Exception):
    """Une formule qu'on refuse de lire — et qu'on NOMME."""

    def __init__(self, raison: str, position: int | None = None, detail: str = "") -> None:
        super().__init__(f"{raison}{f' (position {position})' if position else ''}"
                         f"{f' : {detail}' if detail else ''}")
        self.raison = raison
        self.position = position
        self.detail = detail


class ErreurCalcul(Exception):
    """Une erreur de calcul (division par zéro, racine négative, variable absente)."""


# ------------------------------------------------------------------ les jetons

FONCTIONS = {"sin", "cos", "tan", "ln", "log", "exp"}
LETTRES_GRECQUES = {"alpha", "beta", "gamma", "delta", "theta", "lambda", "mu", "pi"}
RE_NOMBRE = re.compile(r"\d+(?:\.\d+)?")
RE_MACRO = re.compile(r"\\([a-zA-Z]+)")


def jetons(texte: str) -> list[tuple[str, str]]:
    """Découpe LaTeX en jetons typés ; refuse le caractère ou la macro inconnue."""
    sortie: list[tuple[str, str]] = []
    i, n = 0, len(texte)
    while i < n:
        c = texte[i]
        if c.isspace():
            i += 1
            continue
        if c == "\\":
            m = RE_MACRO.match(texte, i)
            if not m:
                raise Refus("macro invalide", i, texte[i:i + 12])
            nom = m.group(1)
            i = m.end()
            if nom in ("left", "right", "displaystyle", "textstyle"):
                continue
            if nom in ("cdot", "times", "ast"):
                sortie.append(("OP", "*"))
            elif nom == "div":
                sortie.append(("OP", "/"))
            elif nom == "pm":
                raise Refus("symbole ambigu", i, "\\pm")
            elif nom == "frac":
                sortie.append(("MACRO", "frac"))
            elif nom == "sqrt":
                sortie.append(("MACRO", "sqrt"))
            elif nom in FONCTIONS:
                sortie.append(("FN", nom))
            elif nom in LETTRES_GRECQUES:
                sortie.append(("VAR", nom))
            else:
                raise Refus("macro inconnue", i, f"\\{nom}")
            continue
        if c.isdigit() or (c == "." and i + 1 < n and texte[i + 1].isdigit()):
            m = RE_NOMBRE.match(texte, i)
            if not m:
                raise Refus("nombre invalide", i, texte[i:i + 8])
            sortie.append(("N", m.group(0)))
            i = m.end()
            continue
        if c.isalpha():
            sortie.append(("VAR", c))
            i += 1
            continue
        if c in "+-*/^=(){}[]":
            sortie.append(("OP", c))
            i += 1
            continue
        if c in ",;":
            i += 1
            continue
        raise Refus("caractère inconnu", i, c)
    return sortie


# ------------------------------------------------------------------ le parseur

def _n(valeur: Fraction | int) -> tuple:
    return ("n", Fraction(valeur))


def _somme(gauche, droite):
    return ("+", gauche, droite)


def _produit(gauche, droite):
    return ("*", gauche, droite)


def _moins(noeud):
    return ("neg", noeud)


def _puissance(base, exposant):
    return ("^", base, exposant)


class Analyseur:
    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        self.tokens = tokens
        self.pos = 0

    def courant(self) -> tuple[str, str] | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def avance(self) -> tuple[str, str]:
        if self.pos >= len(self.tokens):
            raise Refus("formule incomplète", self.pos)
        jeton = self.tokens[self.pos]
        self.pos += 1
        return jeton

    def attend(self, valeur: str) -> None:
        jeton = self.avance()
        if jeton[1] != valeur:
            raise Refus("symbole attendu", self.pos, f"« {valeur} » au lieu de « {jeton[1]} »")

    def expr(self):
        noeud = self.terme()
        while self.courant() in (("OP", "+"), ("OP", "-")):
            op = self.avance()[1]
            droite = self.terme()
            noeud = _somme(noeud, droite) if op == "+" else _somme(noeud, _moins(droite))
        return noeud

    def debute_un_facteur(self) -> bool:
        jeton = self.courant()
        if jeton is None:
            return False
        type_, valeur = jeton
        return type_ in ("N", "VAR", "FN") or (type_ == "MACRO") or \
            (type_ == "OP" and valeur in ("(", "{"))

    def terme(self):
        noeud = self.facteur()
        while True:
            jeton = self.courant()
            if jeton == ("OP", "*") or jeton == ("OP", "/"):
                op = self.avance()[1]
                droite = self.facteur()
                noeud = _produit(noeud, droite) if op == "*" else \
                    _produit(noeud, _puissance(droite, _n(-1)))
                continue
            if self.debute_un_facteur():
                # multiplication implicite : 2x, \frac{1}{2}x, \sqrt{2}\sqrt{3}
                noeud = _produit(noeud, self.facteur())
                continue
            return noeud

    def facteur(self):
        jeton = self.courant()
        if jeton == ("OP", "-"):
            self.avance()
            return _moins(self.facteur())
        if jeton == ("OP", "+"):
            self.avance()
            return self.facteur()
        base = self.atome()
        if self.courant() == ("OP", "^"):
            self.avance()
            return _puissance(base, self.facteur())
        return base

    def atome(self):
        jeton = self.avance()
        type_, valeur = jeton
        if type_ == "N":
            return _n(Fraction(valeur))
        if type_ == "VAR":
            return ("v", valeur)
        if type_ == "FN":
            argument = self.facteur() if self.courant() != ("OP", "^") else self.atome()
            return ("fn", valeur, argument)
        if type_ == "MACRO" and valeur == "frac":
            self.attend("{")
            numerateur = self.expr()
            self.attend("}")
            self.attend("{")
            denominateur = self.expr()
            self.attend("}")
            return _produit(numerateur, _puissance(denominateur, _n(-1)))
        if type_ == "MACRO" and valeur == "sqrt":
            self.attend("{")
            argument = self.expr()
            self.attend("}")
            return ("fn", "sqrt", argument)
        if type_ == "OP" and valeur in ("(", "{"):
            fermeture = ")" if valeur == "(" else "}"
            noeud = self.expr()
            self.attend(fermeture)
            return noeud
        raise Refus("symbole inattendu", self.pos, f"« {valeur} »")


def analyse_latex(texte: str):
    """L'AST d'une formule (ou d'une équation `a = b`), ou un refus nommé."""
    tokens = jetons(texte)
    if not tokens:
        raise Refus("formule vide")
    p = Analyseur(tokens)
    gauche = p.expr()
    if p.courant() == ("OP", "="):
        p.avance()
        droite = p.expr()
        if p.courant() is not None:
            raise Refus("reste après l'équation", p.pos)
        return ("eq", gauche, droite)
    if p.courant() is not None:
        raise Refus("reste après la formule", p.pos, str(p.courant()))
    return gauche


# ------------------------------------------------------------------ l'évaluation

def evaluer(noeud, env: dict | None = None):
    """La valeur : Fraction quand elle est rationnelle, float sinon. Refus explicite sinon."""
    env = env or {}

    def exacte(valeur):
        return isinstance(valeur, Fraction)

    def ev(n):
        type_ = n[0]
        if type_ == "n":
            return n[1]
        if type_ == "v":
            if n[1] == "pi":
                return math.pi
            if n[1] not in env:
                raise ErreurCalcul(f"variable absente : {n[1]}")
            valeur = env[n[1]]
            return valeur if isinstance(valeur, Fraction) else Fraction(valeur)
        if type_ == "+":
            return ev(n[1]) + ev(n[2])
        if type_ == "*":
            return ev(n[1]) * ev(n[2])
        if type_ == "neg":
            return -ev(n[1])
        if type_ == "^":
            base, exposant = ev(n[1]), ev(n[2])
            if isinstance(exposant, Fraction) and exposant.denominator == 1:
                if exposant.numerator >= 0:
                    return base ** exposant.numerator
                if base == 0:
                    raise ErreurCalcul("division par zéro (puissance négative de 0)")
                return Fraction(1, 1) / (base ** (-exposant.numerator))
            return float(base) ** float(exposant)
        if type_ == "fn":
            nom, argument = n[1], ev(n[2])
            if nom == "sqrt":
                if argument < 0:
                    raise ErreurCalcul("racine d'un nombre négatif")
                if exacte(argument) or isinstance(argument, int):
                    racine = math.isqrt(int(argument))
                    if Fraction(racine) ** 2 == Fraction(argument):
                        return Fraction(racine)
                return math.sqrt(float(argument))
            try:
                return {"sin": math.sin, "cos": math.cos, "tan": math.tan,
                        "ln": math.log, "log": math.log10, "exp": math.exp}[nom](
                    float(argument))
            except (ValueError, OverflowError) as exc:
                raise ErreurCalcul(f"{nom} : {exc}") from exc
        raise Refus("nœud inconnu", None, type_)

    return ev(noeud)


def est_exacte(valeur) -> bool:
    return isinstance(valeur, Fraction)


# ------------------------------------------------------------------ la dérivation

def derive(noeud, variable: str):
    """La dérivée exacte d'un AST par rapport à `variable`."""
    type_ = noeud[0]
    if type_ == "n":
        return _n(0)
    if type_ == "v":
        return _n(1 if noeud[1] == variable else 0)
    if type_ == "+":
        return _somme(derive(noeud[1], variable), derive(noeud[2], variable))
    if type_ == "neg":
        return _moins(derive(noeud[1], variable))
    if type_ == "*":
        gauche, droite = noeud[1], noeud[2]
        return _somme(_produit(derive(gauche, variable), droite),
                      _produit(gauche, derive(droite, variable)))
    if type_ == "^":
        base, exposant = noeud[1], noeud[2]
        if exposant[0] == "n":
            n = exposant[1]
            if n == 0:
                return _n(0)
            return _produit(_produit(exposant, _puissance(base, _n(n - 1))),
                            derive(base, variable))
        if base[0] == "n":
            return _produit(_produit(noeud, ("fn", "ln", base)), derive(exposant, variable))
        raise Refus("dérivée d'une puissance variable", None, "x^y")
    if type_ == "fn":
        nom, argument = noeud[1], noeud[2]
        interieur = derive(argument, variable)
        if nom == "sin":
            return _produit(("fn", "cos", argument), interieur)
        if nom == "cos":
            return _produit(_moins(("fn", "sin", argument)), interieur)
        if nom == "tan":
            return _produit(_puissance(("fn", "cos", argument), _n(-2)), interieur)
        if nom in ("ln", "log"):
            base = _n(math.log(10)) if nom == "log" else _n(1)
            return _produit(_puissance(argument, _n(-1)), _produit(base, interieur))
        if nom == "exp":
            return _produit(noeud, interieur)
        if nom == "sqrt":
            return _produit(_puissance(_produit(_n(2), ("fn", "sqrt", argument)), _n(-1)),
                            interieur)
        raise Refus("dérivée de fonction inconnue", None, nom)
    raise Refus("dérivée impossible", None, type_)


def simplifier(noeud):
    """Une simplification légère : constantes, identités, puissances — pour l'affichage."""
    type_ = noeud[0]
    if type_ in ("n", "v"):
        return noeud
    if type_ == "neg":
        interieur = simplifier(noeud[1])
        if interieur[0] == "n":
            return _n(-interieur[1])
        return _moins(interieur)
    if type_ == "+":
        gauche, droite = simplifier(noeud[1]), simplifier(noeud[2])
        if gauche[0] == "n" and droite[0] == "n":
            return _n(gauche[1] + droite[1])
        if gauche == _n(0):
            return droite
        if droite == _n(0):
            return gauche
        return _somme(gauche, droite)
    if type_ == "*":
        gauche, droite = simplifier(noeud[1]), simplifier(noeud[2])
        if gauche[0] == "n" and droite[0] == "n":
            return _n(gauche[1] * droite[1])
        if gauche == _n(0) or droite == _n(0):
            return _n(0)
        if gauche == _n(1):
            return droite
        if droite == _n(1):
            return gauche
        return _produit(gauche, droite)
    if type_ == "^":
        base, exposant = simplifier(noeud[1]), simplifier(noeud[2])
        if exposant[0] == "n":
            if exposant[1] == 0:
                return _n(1)
            if exposant[1] == 1:
                return base
            if base[0] == "n" and exposant[1].denominator == 1:
                return _n(base[1] ** exposant[1].numerator)
        return _puissance(base, exposant)
    if type_ == "fn":
        argument = simplifier(noeud[2])
        return ("fn", noeud[1], argument)
    return noeud


def resous(equation, variable: str) -> Fraction:
    """Résout une équation LINÉAIRE `a x + b = c` exactement ; refuse le reste.

    La linéarité se vérifie : la dérivée seconde de `gauche - droite` doit être nulle.
    Refuser une équation non linéaire vaut mieux que rendre une solution fausse.
    """
    if equation[0] != "eq":
        raise Refus("ce n'est pas une équation")
    f = _somme(equation[1], _moins(equation[2]))
    premiere = derive(f, variable)
    seconde = derive(premiere, variable)
    try:
        valeur_seconde = evaluer(seconde, {variable: Fraction(0)})
    except ErreurCalcul as exc:
        raise Refus("équation non linéaire", None, str(exc)) from exc
    if valeur_seconde != 0:
        raise Refus("équation non linéaire", None, f"dérivée seconde {valeur_seconde}")
    a = evaluer(premiere, {variable: Fraction(0)})
    b = evaluer(f, {variable: Fraction(0)})
    if a == 0:
        raise Refus("équation sans solution unique", None, "a = 0")
    return Fraction(-b) / Fraction(a)


# ------------------------------------------------------------------ l'oracle sympy

def vers_sympy(noeud, symboles: dict):
    """Traduit l'AST en expression sympy : l'oracle indépendant du calcul."""
    import sympy as sp

    type_ = noeud[0]
    if type_ == "n":
        return sp.Rational(noeud[1].numerator, noeud[1].denominator)
    if type_ == "v":
        if noeud[1] == "pi":
            return sp.pi
        if noeud[1] not in symboles:
            symboles[noeud[1]] = sp.Symbol(noeud[1])
        return symboles[noeud[1]]
    if type_ == "+":
        return vers_sympy(noeud[1], symboles) + vers_sympy(noeud[2], symboles)
    if type_ == "*":
        return vers_sympy(noeud[1], symboles) * vers_sympy(noeud[2], symboles)
    if type_ == "neg":
        return -vers_sympy(noeud[1], symboles)
    if type_ == "^":
        return vers_sympy(noeud[1], symboles) ** vers_sympy(noeud[2], symboles)
    if type_ == "fn":
        fonction = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "ln": sp.log,
                    "log": lambda a: sp.log(a, 10), "exp": sp.exp, "sqrt": sp.sqrt}[noeud[1]]
        return fonction(vers_sympy(noeud[2], symboles))
    raise Refus("traduction sympy impossible", None, type_)


def empreinte(noeud) -> str:
    return hashlib.sha256(repr(noeud).encode()).hexdigest()


# ------------------------------------------------------------------ les mesures

def charge() -> dict:
    return json.loads((FIXTURES / "formules.json").read_text(encoding="utf-8"))


def _meme(valeur, attendu: str | None, attendu_float: float | None,
          tolerance: float = 1e-9) -> bool:
    if attendu is not None:
        return est_exacte(valeur) and valeur == Fraction(attendu)
    if attendu_float is not None:
        return abs(float(valeur) - attendu_float) <= tolerance * max(1.0, abs(attendu_float))
    raise ValueError("attendu absent")


def _formules() -> dict:
    import sympy as sp

    donnees = charge()["formules"]
    resultats, exactes, sympy_ok = [], 0, 0
    for cas in donnees:
        ast = analyse_latex(cas["latex"])
        env = {nom: Fraction(valeur) for nom, valeur in cas.get("env", {}).items()}
        valeur = evaluer(ast, env)
        correct = _meme(valeur, cas.get("attendu"), cas.get("attendu_float"),
                        cas.get("tolerance", 1e-9))
        # l'oracle : la MÊME formule, traduite en sympy, doit donner le même nombre
        symbole = vers_sympy(ast, {})
        remplacement = {sp.Symbol(k): sp.Rational(Fraction(v).numerator,
                                                 Fraction(v).denominator)
                        for k, v in cas.get("env", {}).items()}
        oracle = sp.simplify(symbole.subs(remplacement))
        if est_exacte(valeur):
            oracle_correct = sp.simplify(oracle - sp.Rational(valeur.numerator,
                                                              valeur.denominator)) == 0
        else:
            oracle_correct = abs(float(oracle) - float(valeur)) <= 1e-9 * max(
                1.0, abs(float(valeur)))
        exactes += correct
        sympy_ok += oracle_correct
        resultats.append({"nom": cas["nom"], "latex": cas["latex"],
                          "valeur": str(valeur), "correct": correct,
                          "sympy": oracle_correct})
    return {"exactes": exactes, "sympy": sympy_ok, "total": len(donnees),
            "details": resultats}


def _derivees() -> dict:
    import sympy as sp

    donnees = charge()["derivees"]
    justes = 0
    details = []
    for cas in donnees:
        ast = analyse_latex(cas["latex"])
        derivee = derive(ast, cas["var"])
        symboles = {}
        reference = sp.diff(vers_sympy(ast, symboles), symboles[cas["var"]])
        points = [Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3), Fraction(5)]
        ok = True
        for point in points:
            try:
                nôtre = evaluer(derivee, {cas["var"]: point})
            except ErreurCalcul:
                continue
            attendu = float(reference.subs(symboles[cas["var"]], float(point)))
            if abs(float(nôtre) - attendu) > 1e-8 * max(1.0, abs(attendu)):
                ok = False
                break
        justes += ok
        details.append({"latex": cas["latex"], "derivee": repr(derivee)[:60],
                        "correct": ok})
    return {"justes": justes, "total": len(donnees), "details": details}


def _equations() -> dict:
    import sympy as sp

    donnees = charge()["equations"]
    justes = refuses = 0
    details = []
    for cas in donnees:
        ast = analyse_latex(cas["latex"])
        if cas.get("refus"):
            try:
                resous(ast, cas["var"])
                correct = False
            except Refus:
                correct = True
                refuses += 1
            details.append({"latex": cas["latex"], "refus": True, "correct": correct})
            justes += correct
            continue
        racine = resous(ast, cas["var"])
        symboles = {}
        reference = sp.solve(sp.Eq(vers_sympy(ast[1], symboles),
                                   vers_sympy(ast[2], symboles)), symboles[cas["var"]])
        oracle = Fraction(str(reference[0])) if reference else None
        correct = oracle is not None and racine == oracle and \
            _meme(racine, cas["attendu"], None)
        justes += correct
        details.append({"latex": cas["latex"], "racine": str(racine),
                        "oracle": str(oracle), "correct": correct})
    return {"justes": justes, "total": len(donnees), "refus": refuses,
            "details": details}


def controle_surface() -> dict:
    """La surface ne donne pas la valeur : le contrôle est construit pour qu'elle échoue.

    Un lecteur de surface lit le premier nombre de la formule (c'est ce que fait un
    gabarit de banc) ; l'AST rend la valeur. La valeur est dans le CALCUL, pas dans la ligne.
    """
    cas = [
        ("\\frac{1}{3}+\\frac{1}{6}", "1/2", "1"),
        ("2^{10}", "1024", "2"),
        ("\\sqrt{144}+1", "13", "144"),
    ]
    resultats = {}
    for latex, attendu, surface in cas:
        valeur = evaluer(analyse_latex(latex))
        resultats[latex] = {"attendu": attendu, "calcule": str(valeur),
                            "surface": surface,
                            "surface_correcte": surface == attendu,
                            "calcule_correct": str(valeur) == attendu}
    return resultats


def _refus() -> dict:
    cas = {
        "macro_inconnue": lambda: analyse_latex("\\int_0^1 x dx"),
        "accolade_ouverte": lambda: analyse_latex("\\frac{1}{"),
        "caractere_inconnu": lambda: analyse_latex("x @ y"),
        "syntaxe": lambda: analyse_latex("x +"),
        "division_zero": lambda: evaluer(analyse_latex("\\frac{1}{0}")),
        "racine_negative": lambda: evaluer(analyse_latex("\\sqrt{-1}")),
        "non_lineaire": lambda: resous(analyse_latex("x^2 = 4"), "x"),
        "variable_absente": lambda: evaluer(analyse_latex("x + 1")),
    }
    resultats = {}
    for nom, action in cas.items():
        try:
            action()
            resultats[nom] = None
        except (Refus, ErreurCalcul) as exc:
            resultats[nom] = f"{type(exc).__name__}: {exc}"
    return resultats


def _cout() -> dict:
    def synthetique(n: int) -> str:
        return "+".join("1" for _ in range(n))

    def temps(n: int) -> float:
        source = synthetique(n)
        debut = time.perf_counter()
        for _ in range(20):
            evaluer(analyse_latex(source))
        return time.perf_counter() - debut

    petit = min(temps(50) for _ in range(3))
    grand = min(temps(200) for _ in range(3))
    return {"petit": petit, "grand": grand, "ratio": grand / max(petit, 1e-9)}


def autotest() -> int:
    print("=== PORTE R4.3 — LE BLOC MATHS ===")
    problemes: list[str] = []

    formules = _formules()
    print(f"1. formules    : {formules['exactes']}/{formules['total']} exactes, "
          f"{formules['sympy']}/{formules['total']} confirmées par sympy")
    if formules["exactes"] != formules["total"]:
        problemes.append(f"formules fausses : "
                         f"{[d for d in formules['details'] if not d['correct']][:3]}")
    if formules["sympy"] != formules["total"]:
        problemes.append(f"sympy contredit : "
                         f"{[d for d in formules['details'] if not d['sympy']][:3]}")

    derivees = _derivees()
    print(f"2. dérivées    : {derivees['justes']}/{derivees['total']} justes "
          f"(5 points, oracle sympy)")
    if derivees["justes"] != derivees["total"]:
        problemes.append(f"dérivées fausses : "
                         f"{[d for d in derivees['details'] if not d['correct']][:3]}")

    equations = _equations()
    print(f"3. équations   : {equations['justes']}/{equations['total']} justes "
          f"({equations['refus']} refus attendu(s))")
    if equations["justes"] != equations["total"]:
        problemes.append(f"équations fausses : "
                         f"{[d for d in equations['details'] if not d['correct']][:3]}")

    controle = controle_surface()
    surface_fausse = sum(1 for r in controle.values() if not r["surface_correcte"])
    calcule_juste = sum(1 for r in controle.values() if r["calcule_correct"])
    print(f"4. contrôle    : surface fausse {surface_fausse}/{len(controle)}, "
          f"calcul juste {calcule_juste}/{len(controle)}")
    for latex, r in controle.items():
        print(f"     {latex:26s} calcule {r['calcule']:>6} · surface {r['surface']:>4}")
    if surface_fausse != len(controle):
        problemes.append("la surface n'échoue pas partout")
    if calcule_juste != len(controle):
        problemes.append("le calcul ne rend pas les valeurs attendues")

    refus = _refus()
    nommes = {k: v for k, v in refus.items() if v}
    print(f"5. refus       : {len(nommes)}/{len(refus)} nommés ({', '.join(nommes)})")
    if len(nommes) != len(refus):
        problemes.append(f"refus non nommés : {[k for k, v in refus.items() if not v]}")

    cout = _cout()
    print(f"6. coût        : ×{cout['ratio']:.2f} de temps pour ×4 termes "
          f"({cout['petit'] / 20 * 1000:.2f} ms / 50 additions)")
    if not (2.5 <= cout["ratio"] <= 6.0):
        problemes.append(f"coût non linéaire : ×{cout['ratio']:.2f} pour ×4")

    source = "\\frac{1}{3}+\\frac{1}{6}"
    empreintes = [empreinte(analyse_latex(source)) for _ in range(2)]
    print(f"7. rejeu       : {'identique' if empreintes[0] == empreintes[1] else 'DIFFÉRENT'}")
    if empreintes[0] != empreintes[1]:
        problemes.append("le rejeu ne redonne pas la même empreinte")

    if problemes:
        print("❌ porte bloc maths ROUGE")
        for probleme in problemes:
            print(f"   - {probleme}")
        return 1
    print("✅ porte bloc maths verte")
    return 0


def mesure(chemin: pathlib.Path) -> int:
    data = {
        "date": "2026-10-29",
        "ligne": "R4.3",
        "dispositif": {
            "corpus": "tools/tests/maths/formules.json (le dépôt n'a pas de corpus LaTeX)",
            "langage": "sous-ensemble LaTeX",
            "arithmetique": "fractions.Fraction (exacte) ; flottant pour les irrationnels",
            "oracle": "sympy (évaluation, dérivée, solution)",
            "machine": "CPU, aucun modèle chargé",
        },
        "formules": _formules(),
        "derivees": _derivees(),
        "equations": _equations(),
        "controles": controle_surface(),
        "refus": _refus(),
        "cout": {"ratio_x4": round(_cout()["ratio"], 2)},
        "rejeu": {"identique": empreinte(analyse_latex("\\frac{1}{3}+\\frac{1}{6}"))
                  == empreinte(analyse_latex("\\frac{1}{3}+\\frac{1}{6}"))},
    }
    chemin.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"écrit : {chemin}")
    print(json.dumps({k: v for k, v in data.items()
                      if k in ("formules", "derivees", "equations", "refus")},
                     ensure_ascii=False, indent=1)[:1800])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="R4.3 — le bloc maths.")
    ap.add_argument("--porte", action="store_true")
    ap.add_argument("--mesure", type=pathlib.Path)
    ap.add_argument("--calcule", type=str)
    ap.add_argument("--derive", type=str)
    ap.add_argument("--var", type=str, default="x")
    ap.add_argument("--autotest", action="store_true")
    args = ap.parse_args()
    if args.porte or args.autotest:
        return autotest()
    if args.mesure:
        return mesure(args.mesure)
    if args.calcule:
        try:
            valeur = evaluer(analyse_latex(args.calcule))
            print(f"{valeur} ({type(valeur).__name__})")
            return 0
        except (Refus, ErreurCalcul) as exc:
            print(f"refus : {exc}", file=sys.stderr)
            return 2
    if args.derive:
        try:
            print(repr(simplifier(derive(analyse_latex(args.derive), args.var))))
            return 0
        except (Refus, ErreurCalcul) as exc:
            print(f"refus : {exc}", file=sys.stderr)
            return 2
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

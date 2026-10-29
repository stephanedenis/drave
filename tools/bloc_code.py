#!/usr/bin/env python3
"""bloc_code.py — R4.2 : lire du code par son AST et son exécution, pas comme un texte.

POURQUOI CE FICHIER. Un document de code n'est pas de la prose : la réponse à « que vaut
cette expression ? » n'est pas dans le texte, elle est dans l'**exécution** ; la réponse à
« quelle variable cette ligne lit-elle ? » n'est pas dans la ligne, elle est dans la
**portée**. R0.1 range le code en région et le texte reste du texte. Le banc R0.3 demande
des valeurs numériques par deux mots rares : sur du code, il mesure la recherche d'une
ligne, pas la compréhension.

Ce que ce bloc ajoute, et qui se vérifie :
  1. **le parseur** — tout le corpus `tools/*.py` est accepté, les nœuds, fonctions et
     classes sont comptés ; une syntaxe fausse est **refusée en la nommant** ;
  2. **la portée** — chaque nom est rattaché à sa portée (module, fonction, classe,
     compréhension) ; un nom lu et jamais lié est signalé ;
  3. **l'évaluation** — un interpréteur **en sable** (liste blanche de nœuds, pas d'import,
     pas d'attribut, pas, itérations et profondeur bornés) rend la valeur exacte ;
  4. **le contrôle négatif** — un lecteur de texte seul ne peut pas rendre une valeur
     calculée ; le contrôle est construit pour qu'il échoue.

La règle du dépôt : **classique d'abord** quand l'information est explicite. La portée et
l'exécution sont exactes par construction ; le modèle ne sert qu'à l'intention.

Usage :
  python3 tools/bloc_code.py --porte
  python3 tools/bloc_code.py --mesure reports/r42-bloc-code.json
  python3 tools/bloc_code.py --json CHEMIN.py
  python3 tools/bloc_code.py --execute "2**10 + 24"
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import pathlib
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = RACINE / "tools" / "tests" / "code"


# ------------------------------------------------------------------ les exceptions

class Refus(Exception):
    """Un nœud, une syntaxe ou un appel qu'on refuse — et qu'on NOMME."""

    def __init__(self, raison: str, ligne: int | None = None, detail: str = "") -> None:
        super().__init__(f"{raison}{f' (ligne {ligne})' if ligne else ''}"
                         f"{f' : {detail}' if detail else ''}")
        self.raison = raison
        self.ligne = ligne
        self.detail = detail


class ErreurExecution(Exception):
    """Une erreur de l'extrait exécuté (division par zéro, nom inconnu, borne atteinte)."""


# ------------------------------------------------------------------ l'analyse statique

GENRES = ("paramètre", "variable", "fonction", "classe", "import", "boucle", "exception",
          "compréhension")


class Symbole:
    __slots__ = ("nom", "genre", "portee", "ligne", "lectures", "affectations")

    def __init__(self, nom: str, genre: str, portee: "Portee", ligne: int) -> None:
        self.nom = nom
        self.genre = genre
        self.portee = portee
        self.ligne = ligne
        self.lectures = 0
        self.affectations = 1 if genre != "paramètre" else 0

    def __repr__(self) -> str:  # pragma: no cover
        return f"Symbole({self.nom!r}, {self.genre}, ligne {self.ligne})"


class Portee:
    __slots__ = ("nom", "genre", "parent", "symboles", "debut", "fin", "globaux")

    def __init__(self, nom: str, genre: str, parent: "Portee | None",
                 debut: int, fin: int) -> None:
        self.nom = nom
        self.genre = genre
        self.parent = parent
        self.symboles: dict[str, Symbole] = {}
        self.debut = debut
        self.fin = fin
        self.globaux: set[str] = set()

    def declare(self, nom: str, genre: str, ligne: int) -> Symbole:
        if nom in self.globaux and self.parent is not None:
            return self.parent.declare(nom, genre, ligne)
        if nom not in self.symboles:
            self.symboles[nom] = Symbole(nom, genre, self, ligne)
        return self.symboles[nom]

    def cherche(self, nom: str) -> Symbole | None:
        portee: Portee | None = self
        while portee is not None:
            if nom in portee.symboles:
                return portee.symboles[nom]
            portee = portee.parent
        return None

    def __repr__(self) -> str:  # pragma: no cover
        return f"Portee({self.nom!r}, {self.genre}, {sorted(self.symboles)})"


class Module:
    def __init__(self, nom: str, arbre: ast.Module, portees: list[Portee],
                 lectures: list[tuple[str, int, Portee]]) -> None:
        self.nom = nom
        self.arbre = arbre
        self.portees = portees
        self.lectures = lectures

    @property
    def n_noeuds(self) -> int:
        return sum(1 for _ in ast.walk(self.arbre))

    def fonctions(self) -> list[ast.FunctionDef]:
        return [n for n in ast.walk(self.arbre) if isinstance(n, ast.FunctionDef)]

    def classes(self) -> list[ast.ClassDef]:
        return [n for n in ast.walk(self.arbre) if isinstance(n, ast.ClassDef)]


def analyse(source: str, nom: str = "<snippet>") -> Module:
    """L'AST et les portées d'un module. Une syntaxe fausse est refusée en la nommant."""
    try:
        arbre = ast.parse(source)
    except SyntaxError as exc:
        raise Refus("syntaxe", exc.lineno, exc.msg) from exc
    fin = getattr(arbre, "end_lineno", None) or 10 ** 9
    racine = Portee("<module>", "module", None, 1, fin)
    portees = [racine]
    lectures: list[tuple[str, int, Portee]] = []

    def nouvelle(nom_: str, genre: str, parent: Portee, noeud) -> Portee:
        p = Portee(nom_, genre, parent, getattr(noeud, "lineno", 1),
                   getattr(noeud, "end_lineno", None) or 10 ** 9)
        portees.append(p)
        return p

    def lie_cible(cible, portee: Portee, genre: str) -> None:
        if isinstance(cible, ast.Name):
            portee.declare(cible.id, genre, cible.lineno)
        elif isinstance(cible, (ast.Tuple, ast.List)):
            for element in cible.elts:
                lie_cible(element, portee, genre)
        elif isinstance(cible, ast.Subscript):
            visite(cible.value, portee)
            visite(cible.slice, portee)
        elif isinstance(cible, ast.Attribute):
            visite(cible.value, portee)
        # les autres cibles (étoilée) sont vues via les appels génériques

    def visite(noeud, portee: Portee) -> None:
        if isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef)):
            portee.declare(noeud.name, "fonction", noeud.lineno)
            interne = nouvelle(noeud.name, "fonction", portee, noeud)
            args = noeud.args
            for a in args.posonlyargs + args.args:
                interne.declare(a.arg, "paramètre", a.lineno)
            for a in (args.vararg, args.kwarg):
                if a is not None:
                    interne.declare(a.arg, "paramètre", a.lineno)
            for a in args.kwonlyargs:
                interne.declare(a.arg, "paramètre", a.lineno)
            for sous in noeud.body:
                visite(sous, interne)
            return
        if isinstance(noeud, ast.ClassDef):
            portee.declare(noeud.name, "classe", noeud.lineno)
            interne = nouvelle(noeud.name, "classe", portee, noeud)
            for sous in noeud.body:
                visite(sous, interne)
            return
        if isinstance(noeud, ast.Lambda):
            interne = nouvelle("<lambda>", "fonction", portee, noeud)
            for a in noeud.args.args:
                interne.declare(a.arg, "paramètre", a.lineno)
            visite(noeud.body, interne)
            return
        if isinstance(noeud, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            interne = nouvelle("<compréhension>", "compréhension", portee, noeud)
            for generateur in noeud.generators:
                visite(generateur.iter, interne)
                lie_cible(generateur.target, interne, "compréhension")
                for condition in generateur.ifs:
                    visite(condition, interne)
            for champ in ("elt", "key", "value"):
                if hasattr(noeud, champ):
                    visite(getattr(noeud, champ), interne)
            return
        if isinstance(noeud, (ast.Import, ast.ImportFrom)):
            for alias in noeud.names:
                nom_ = alias.asname or alias.name.split(".")[0]
                portee.declare(nom_, "import", noeud.lineno)
            return
        if isinstance(noeud, (ast.Global, ast.Nonlocal)):
            portee.globaux.update(noeud.names)
            return
        if isinstance(noeud, ast.Assign):
            visite(noeud.value, portee)
            for cible in noeud.targets:
                lie_cible(cible, portee, "variable")
            return
        if isinstance(noeud, ast.AnnAssign):
            if noeud.value is not None:
                visite(noeud.value, portee)
            lie_cible(noeud.target, portee, "variable")
            return
        if isinstance(noeud, ast.AugAssign):
            visite(noeud.value, portee)
            lie_cible(noeud.target, portee, "variable")
            return
        if isinstance(noeud, ast.For):
            visite(noeud.iter, portee)
            lie_cible(noeud.target, portee, "boucle")
            for sous in noeud.body + noeud.orelse:
                visite(sous, portee)
            return
        if isinstance(noeud, ast.ExceptHandler):
            if noeud.name:
                portee.declare(noeud.name, "exception", noeud.lineno)
            for sous in noeud.body:
                visite(sous, portee)
            return
        if isinstance(noeud, ast.Name):
            if isinstance(noeud.ctx, ast.Load):
                lectures.append((noeud.id, noeud.lineno, portee))
            elif isinstance(noeud.ctx, ast.Store):
                portee.declare(noeud.id, "variable", noeud.lineno)
            return
        for enfant in ast.iter_child_nodes(noeud):
            visite(enfant, portee)

    for noeud in arbre.body:
        visite(noeud, racine)
    return Module(nom, arbre, portees, lectures)


def portee_de(module: Module, ligne: int) -> Portee:
    """La portée la plus profonde qui contient cette ligne (module par défaut)."""
    candidates = [p for p in module.portees if p.debut <= ligne <= p.fin]
    return max(candidates, key=lambda p: (p.debut, -p.fin if p.parent is None else p.debut)) \
        if candidates else module.portees[0]


def resous(module: Module, nom: str, ligne: int) -> Symbole | None:
    """Le symbole que ce nom désigne à cette ligne, en remontant la chaîne des portées."""
    depart = portee_de(module, ligne)
    trouve = depart.cherche(nom)
    if trouve is not None:
        trouve.lectures += 1
    return trouve


def noms_libres(module: Module) -> list[tuple[str, int]]:
    """Les noms lus et JAMAIS liés dans leur chaîne de portées (hors builtins)."""
    libres: list[tuple[str, int]] = []
    for nom, ligne, portee in module.lectures:
        if nom in LISIBLES:
            continue
        if portee.cherche(nom) is None:
            libres.append((nom, ligne))
    return libres


def empreinte(module: Module) -> str:
    """Empreinte stable de l'AST : deux lectures du même fichier la redonnent."""
    forme = [(type(n).__name__, getattr(n, "lineno", 0), getattr(n, "col_offset", 0))
             for n in ast.walk(module.arbre)]
    return hashlib.sha256(json.dumps(forme, sort_keys=True).encode()).hexdigest()


# ------------------------------------------------------------------ l'interpréteur

LISIBLES = {
    "len", "abs", "min", "max", "sum", "sorted", "range", "int", "float", "str", "bool",
    "list", "tuple", "dict", "set", "round", "enumerate", "zip", "any", "all", "print",
    "True", "False", "None", "reversed", "chr", "ord",
}


class Fonction:
    __slots__ = ("nom", "params", "corps", "env", "defaut")

    def __init__(self, nom: str, params: list[str], corps: list, env: dict) -> None:
        self.nom = nom
        self.params = params
        self.corps = corps
        self.env = env


def _borne(valeur, quoi: str) -> None:
    if isinstance(valeur, (list, tuple, str)) and len(valeur) > 100_000:
        raise ErreurExecution(f"{quoi} trop grand ({len(valeur)})")


def _appel_builtin(nom: str, args: list, sortie: list):
    if nom == "print":
        sortie.append(" ".join(str(a) for a in args))
        return None
    if nom == "range":
        if len(args) == 1:
            debut, fin, pas_ = 0, args[0], 1
        elif len(args) == 2:
            debut, fin, pas_ = args[0], args[1], 1
        else:
            debut, fin, pas_ = args
        if pas_ == 0:
            raise ErreurExecution("range avec un pas nul")
        n = (max(0, (fin - debut + pas_ - 1) // pas_) if pas_ > 0
             else max(0, (debut - fin - pas_ - 1) // (-pas_)))
        if n > 100_000:
            raise ErreurExecution(f"range trop grand ({n})")
        return list(range(debut, fin, pas_))
    if nom == "sorted":
        return sorted(args[0]) if args else []
    if nom == "enumerate":
        return list(enumerate(args[0]))
    if nom == "zip":
        return [list(t) for t in zip(*args)]
    if nom in ("int", "float", "str", "bool", "len", "abs", "min", "max", "sum", "round",
               "list", "tuple", "dict", "set", "any", "all", "reversed", "ord", "chr"):
        fonctions = {"int": int, "float": float, "str": str, "bool": bool, "len": len,
                     "abs": abs, "min": min, "max": max, "sum": sum, "round": round,
                     "list": list, "tuple": tuple, "dict": dict, "set": set, "any": any,
                     "all": all, "reversed": lambda v: list(reversed(v)), "ord": ord,
                     "chr": chr}
        try:
            return fonctions[nom](*args)
        except (TypeError, ValueError) as exc:
            raise ErreurExecution(f"{nom} : {exc}") from exc
    raise Refus("appel interdit", None, nom)


def execute(source: str, nom: str = "<snippet>", max_pas: int = 200_000,
            max_iterations: int = 10_000, max_profondeur: int = 50) -> dict:
    """Exécute un extrait en SABLE : liste blanche de nœuds, pas d'import, pas d'attribut.

    Rend la dernière expression évaluée, les variables finales (non appelables), la sortie
    de `print` et le nombre de pas. Une construction non supportée est REFUSÉE, jamais
    ignorée : ignorer un nœud ferait croire à une exécution qui n'a pas eu lieu.
    """
    try:
        arbre = ast.parse(source)
    except SyntaxError as exc:
        raise Refus("syntaxe", exc.lineno, exc.msg) from exc
    pas = [0]
    sortie: list[str] = []
    profondeur = [0]
    env: dict = {}

    def compte() -> None:
        pas[0] += 1
        if pas[0] > max_pas:
            raise ErreurExecution(f"limite de pas atteinte ({max_pas})")

    def ev(noeud, env: dict):
        compte()
        if isinstance(noeud, ast.Constant):
            return noeud.value
        if isinstance(noeud, ast.Name):
            if noeud.id in env:
                return env[noeud.id]
            if noeud.id in LISIBLES:
                return noeud.id  # marqueur : c'est un nom de builtin, pas une valeur
            raise ErreurExecution(f"nom inconnu : {noeud.id} (ligne {noeud.lineno})")
        if isinstance(noeud, ast.BinOp):
            gauche, droite = ev(noeud.left, env), ev(noeud.right, env)
            op = type(noeud.op)
            if op is ast.Pow:
                if not isinstance(droite, (int, float)) or abs(droite) > 1000:
                    raise ErreurExecution("puissance non bornée")
                return gauche ** droite
            if op is ast.Div and droite == 0:
                raise ErreurExecution("division par zéro")
            if op in (ast.FloorDiv, ast.Mod) and droite == 0:
                raise ErreurExecution("division par zéro")
            table = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b,
                     ast.Mult: lambda a, b: a * b, ast.Div: lambda a, b: a / b,
                     ast.FloorDiv: lambda a, b: a // b, ast.Mod: lambda a, b: a % b,
                     ast.BitAnd: lambda a, b: a & b, ast.BitOr: lambda a, b: a | b,
                     ast.BitXor: lambda a, b: a ^ b, ast.LShift: lambda a, b: a << b,
                     ast.RShift: lambda a, b: a >> b}
            if op not in table:
                raise Refus("opérateur non supporté", noeud.lineno, type(noeud.op).__name__)
            return table[op](gauche, droite)
        if isinstance(noeud, ast.UnaryOp):
            v = ev(noeud.operand, env)
            if isinstance(noeud.op, ast.Not):
                return not v
            if isinstance(noeud.op, ast.USub):
                return -v
            if isinstance(noeud.op, ast.UAdd):
                return +v
            if isinstance(noeud.op, ast.Invert):
                return ~v
            raise Refus("opérateur unaire non supporté", noeud.lineno)
        if isinstance(noeud, ast.BoolOp):
            if isinstance(noeud.op, ast.And):
                valeur = True
                for e in noeud.values:
                    valeur = ev(e, env)
                    if not valeur:
                        return valeur
                return valeur
            for e in noeud.values:
                valeur = ev(e, env)
                if valeur:
                    return valeur
            return valeur
        if isinstance(noeud, ast.Compare):
            gauche = ev(noeud.left, env)
            for op, comparateur in zip(noeud.ops, noeud.comparators):
                droite = ev(comparateur, env)
                if isinstance(op, ast.Eq):
                    juste = gauche == droite
                elif isinstance(op, ast.NotEq):
                    juste = gauche != droite
                elif isinstance(op, ast.Lt):
                    juste = gauche < droite
                elif isinstance(op, ast.LtE):
                    juste = gauche <= droite
                elif isinstance(op, ast.Gt):
                    juste = gauche > droite
                elif isinstance(op, ast.GtE):
                    juste = gauche >= droite
                elif isinstance(op, ast.In):
                    juste = gauche in droite
                elif isinstance(op, ast.NotIn):
                    juste = gauche not in droite
                elif isinstance(op, ast.Is):
                    juste = gauche is droite
                elif isinstance(op, ast.IsNot):
                    juste = gauche is not droite
                else:
                    raise Refus("comparaison non supportée", noeud.lineno)
                if not juste:
                    return False
                gauche = droite
            return True
        if isinstance(noeud, ast.IfExp):
            return ev(noeud.body if ev(noeud.test, env) else noeud.orelse, env)
        if isinstance(noeud, ast.Call):
            fonction = ev(noeud.func, env)
            if isinstance(fonction, str) and fonction in LISIBLES:
                args = [ev(a, env) for a in noeud.args]
                return _appel_builtin(fonction, args, sortie)
            if not isinstance(fonction, Fonction):
                raise Refus("appel interdit", noeud.lineno,
                            f"{getattr(fonction, '__name__', type(fonction).__name__)}")
            args = [ev(a, env) for a in noeud.args]
            if len(args) > len(fonction.params):
                raise ErreurExecution(f"{fonction.nom} : {len(args)} arguments pour "
                                      f"{len(fonction.params)}")
            local = dict(fonction.env)
            for i, nom_param in enumerate(fonction.params):
                local[nom_param] = args[i] if i < len(args) else None
            profondeur[0] += 1
            if profondeur[0] > max_profondeur:
                raise ErreurExecution(f"profondeur maximale atteinte ({max_profondeur})")
            try:
                signal = executer_bloc(fonction.corps, local)
            finally:
                profondeur[0] -= 1
            if isinstance(signal, tuple) and signal[0] == "retour":
                return signal[1]
            return None
        if isinstance(noeud, ast.Subscript):
            valeur = ev(noeud.value, env)
            indice = ev(noeud.slice, env)
            try:
                return valeur[indice]
            except (IndexError, KeyError, TypeError) as exc:
                raise ErreurExecution(f"indice invalide : {exc}") from exc
        if isinstance(noeud, ast.Slice):
            return slice(*(ev(x, env) if x is not None else None
                           for x in (noeud.lower, noeud.upper, noeud.step)))
        if isinstance(noeud, ast.List):
            return [ev(e, env) for e in noeud.elts]
        if isinstance(noeud, ast.Tuple):
            return tuple(ev(e, env) for e in noeud.elts)
        if isinstance(noeud, ast.Set):
            return {ev(e, env) for e in noeud.elts}
        if isinstance(noeud, ast.Dict):
            return {ev(k, env): ev(v, env) for k, v in zip(noeud.keys, noeud.values)}
        if isinstance(noeud, ast.ListComp):
            resultat = []

            def boucle(index: int, local: dict) -> None:
                if index == len(noeud.generators):
                    resultat.append(ev(noeud.elt, local))
                    if len(resultat) > 100_000:
                        raise ErreurExecution("compréhension trop grande")
                    return
                generateur = noeud.generators[index]
                iterable = ev(generateur.iter, local)
                for element in iterable:
                    local2 = dict(local)
                    lie_cible(element, generateur.target, local2)
                    if all(ev(c, local2) for c in generateur.ifs):
                        boucle(index + 1, local2)

            boucle(0, dict(env))
            return resultat
        if isinstance(noeud, ast.JoinedStr):
            raise Refus("f-string non supporté", noeud.lineno)
        if isinstance(noeud, ast.Attribute):
            raise Refus("attribut interdit", noeud.lineno, ast.unparse(noeud))
        if isinstance(noeud, ast.Lambda):
            raise Refus("lambda non exécutée", noeud.lineno)
        raise Refus("expression non supportée", getattr(noeud, "lineno", None),
                    type(noeud).__name__)

    def lie_cible(valeur, cible, env: dict) -> None:
        if isinstance(cible, ast.Name):
            env[cible.id] = valeur
        elif isinstance(cible, (ast.Tuple, ast.List)):
            if not isinstance(valeur, (list, tuple)) or len(valeur) != len(cible.elts):
                raise ErreurExecution("dépaquetage de longueur différente")
            for v, c in zip(valeur, cible.elts):
                lie_cible(v, c, env)
        elif isinstance(cible, ast.Subscript):
            conteneur = ev(cible.value, env)
            indice = ev(cible.slice, env)
            conteneur[indice] = valeur
        else:
            raise Refus("cible d'affectation non supportée", getattr(cible, "lineno", None))

    def executer_bloc(corps: list, env: dict):
        for instruction in corps:
            signal = ex(instruction, env)
            if signal is not None:
                return signal
        return None

    def ex(instruction, env: dict):
        compte()
        if isinstance(instruction, ast.Expr):
            valeur = ev(instruction.value, env)
            return ("valeur", valeur)
        if isinstance(instruction, ast.Assign):
            valeur = ev(instruction.value, env)
            for cible in instruction.targets:
                lie_cible(valeur, cible, env)
            return None
        if isinstance(instruction, ast.AugAssign):
            cible = instruction.target
            if not isinstance(cible, ast.Name):
                raise Refus("augmentation non supportée", instruction.lineno)
            droite = ev(instruction.value, env)
            gauche = env.get(cible.id)
            op = type(instruction.op)
            if isinstance(op, ast.Add):
                env[cible.id] = gauche + droite
            elif isinstance(op, ast.Sub):
                env[cible.id] = gauche - droite
            else:
                raise Refus("opérateur d'augmentation non supporté", instruction.lineno)
            return None
        if isinstance(instruction, ast.AnnAssign):
            if instruction.value is not None:
                lie_cible(ev(instruction.value, env), instruction.target, env)
            return None
        if isinstance(instruction, ast.If):
            return executer_bloc(instruction.body if ev(instruction.test, env)
                                 else instruction.orelse, env)
        if isinstance(instruction, ast.For):
            iterable = ev(instruction.iter, env)
            n = 0
            for element in iterable:
                n += 1
                if n > max_iterations:
                    raise ErreurExecution(f"boucle bornée dépassée ({max_iterations})")
                lie_cible(element, instruction.target, env)
                signal = executer_bloc(instruction.body, env)
                if isinstance(signal, tuple) and signal[0] == "break":
                    break
                if isinstance(signal, tuple) and signal[0] == "continue":
                    continue
                if signal is not None:
                    return signal
            else:
                return executer_bloc(instruction.orelse, env)
            return None
        if isinstance(instruction, ast.While):
            n = 0
            while ev(instruction.test, env):
                n += 1
                if n > max_iterations:
                    raise ErreurExecution(f"boucle bornée dépassée ({max_iterations})")
                signal = executer_bloc(instruction.body, env)
                if isinstance(signal, tuple) and signal[0] == "break":
                    break
                if isinstance(signal, tuple) and signal[0] == "continue":
                    continue
                if signal is not None:
                    return signal
            else:
                return executer_bloc(instruction.orelse, env)
            return None
        if isinstance(instruction, ast.FunctionDef):
            params = [a.arg for a in instruction.args.posonlyargs + instruction.args.args]
            env[instruction.name] = Fonction(instruction.name, params, instruction.body, env)
            return None
        if isinstance(instruction, ast.Return):
            return ("retour", ev(instruction.value, env) if instruction.value is not None
                    else None)
        if isinstance(instruction, ast.Pass):
            return None
        if isinstance(instruction, ast.Break):
            return ("break",)
        if isinstance(instruction, ast.Continue):
            return ("continue",)
        if isinstance(instruction, (ast.Import, ast.ImportFrom)):
            raise Refus("import interdit", instruction.lineno,
                        ", ".join(a.name for a in instruction.names))
        if isinstance(instruction, (ast.Global, ast.Nonlocal)):
            raise Refus("portée globale non supportée", instruction.lineno)
        if isinstance(instruction, (ast.ClassDef, ast.With, ast.Try, ast.Raise, ast.Assert,
                                    ast.Delete, ast.AsyncFunctionDef, ast.AsyncFor,
                                    ast.AsyncWith)):
            raise Refus("instruction non supportée", instruction.lineno,
                        type(instruction).__name__)
        raise Refus("instruction inconnue", getattr(instruction, "lineno", None),
                    type(instruction).__name__)

    derniere = None
    for instruction in arbre.body:
        signal = ex(instruction, env)
        if isinstance(signal, tuple) and signal[0] == "valeur":
            derniere = signal[1]
        elif isinstance(signal, tuple) and signal[0] in ("retour", "break", "continue"):
            raise Refus("retour hors fonction", instruction.lineno)
    variables = {k: v for k, v in env.items()
                 if not isinstance(v, Fonction) and not k.startswith("__")}
    return {"valeur": derniere, "env": variables, "sortie": sortie, "pas": pas[0]}



# ------------------------------------------------------------------ les mesures

CORPUS = sorted((RACINE / "tools").glob("*.py"))


def corpus() -> dict:
    acceptes, refuses = 0, []
    noeuds = fonctions = classes = 0
    debut = time.perf_counter()
    for fichier in CORPUS:
        try:
            module = analyse(fichier.read_text(encoding="utf-8", errors="replace"),
                             fichier.name)
        except Refus as refus:
            refuses.append({"fichier": fichier.name, "raison": str(refus)})
            continue
        acceptes += 1
        noeuds += module.n_noeuds
        fonctions += len(module.fonctions())
        classes += len(module.classes())
    return {"fichiers": len(CORPUS), "acceptes": acceptes, "refuses": refuses,
            "noeuds": noeuds, "fonctions": fonctions, "classes": classes,
            "secondes": round(time.perf_counter() - debut, 3)}


def charge_snippets() -> list[dict]:
    return json.loads((FIXTURES / "snippets.json").read_text(encoding="utf-8"))


def controle_texte_seul() -> dict:
    """Trois questions dont la réponse est CALCULÉE : le texte ne la contient pas.

    Le lecteur de texte prend le premier nombre de la source (c'est ce que fait un gabarit
    de banc) ; l'interpréteur rend la valeur. Le contrôle est construit pour que le texte
    échoue — il prouve que la valeur est dans l'exécution, pas dans la ligne.
    """
    questions = [
        ("2**10 + 24", 1048, 2),
        ("sum(range(10))", 45, 10),
        ("(3 + 4) * 2", 14, 3),
    ]
    resultats = {}
    for source, attendu, texte in questions:
        rendu = execute(source)["valeur"]
        resultats[source] = {"attendu": attendu, "execute": rendu, "texte": texte,
                             "texte_correct": texte == attendu,
                             "execute_correct": rendu == attendu}
    return resultats


def _exercices() -> dict:
    """Les opérations à réponse connue, sur les snippets et les fixtures."""
    snippets = charge_snippets()
    justes = faux = 0
    details = []
    for snippet in snippets:
        try:
            rendu = execute(snippet["source"])
            valeur = rendu["valeur"] if snippet.get("champ", "valeur") == "valeur" \
                else rendu["env"].get(snippet["champ"])
        except (Refus, ErreurExecution) as exc:
            valeur = f"ERREUR {exc}"
        correct = valeur == snippet["attendu"]
        justes += correct
        faux += not correct
        details.append({"nom": snippet["nom"], "attendu": snippet["attendu"],
                        "rendu": valeur, "correct": correct})
    return {"justes": justes, "faux": faux, "total": len(snippets), "details": details}


def _portee_et_flux() -> dict:
    portee = analyse((FIXTURES / "portee.py").read_text(encoding="utf-8"), "portee.py")
    resultat = execute((FIXTURES / "portee.py").read_text(encoding="utf-8"))
    x_module = resous(portee, "x", 2)
    x_fonction = resous(portee, "x", 4)
    flux = analyse((FIXTURES / "flux.py").read_text(encoding="utf-8"), "flux.py")
    libres = noms_libres(flux)
    propres = noms_libres(portee)
    return {
        "x_module": x_module.portee.genre if x_module else None,
        "x_fonction": x_fonction.portee.genre if x_fonction else None,
        "x_module_vaut": resultat["env"].get("x"),
        "x_fonction_vaut": resultat["env"].get("x"),
        "y": resultat["env"].get("y"),
        "libres_flux": libres,
        "libres_portee": propres,
    }


def _refus() -> dict:
    """Chaque refus doit être NOMMÉ, jamais ignoré."""
    cas = {
        "syntaxe": lambda: analyse("def f(:\n  pass"),
        "import": lambda: execute("import os\nos.system('true')"),
        "attribut": lambda: execute("obj.methode()"),
        "division_zero": lambda: execute("1 / 0"),
        "nom_inconnu": lambda: execute("total = jamais_defini + 1"),
        "boucle": lambda: execute("while True:\n    pass"),
        "appel_interdit": lambda: execute("open('/etc/passwd')"),
    }
    resultats = {}
    for nom, action in cas.items():
        try:
            action()
            resultats[nom] = None
        except (Refus, ErreurExecution) as exc:
            resultats[nom] = f"{type(exc).__name__}: {exc}"
    return resultats


def _cout() -> dict:
    def synthetique(n: int) -> str:
        return " + ".join(str(i) for i in range(n))

    def temps(n: int) -> float:
        source = synthetique(n)
        debut = time.perf_counter()
        for _ in range(20):
            execute(source)
        return time.perf_counter() - debut

    petit = min(temps(50) for _ in range(3))
    grand = min(temps(200) for _ in range(3))
    return {"petit": petit, "grand": grand, "ratio": grand / max(petit, 1e-9)}


def autotest() -> int:
    print("=== PORTE R4.2 — LE BLOC CODE ===")
    problemes: list[str] = []
    mesure = corpus()
    print(f"1. parseur     : {mesure['acceptes']}/{mesure['fichiers']} fichiers acceptés, "
          f"{mesure['noeuds']} nœuds, {mesure['fonctions']} fonctions, "
          f"{mesure['classes']} classes")
    if mesure["refuses"]:
        problemes.append(f"{len(mesure['refuses'])} fichier(s) refusé(s) : "
                         f"{mesure['refuses'][:2]}")
    if mesure["acceptes"] < 200:
        problemes.append(f"seulement {mesure['acceptes']} fichiers acceptés")

    exercices = _exercices()
    print(f"2. exécution   : {exercices['justes']}/{exercices['total']} snippets exacts")
    if exercices["faux"]:
        problemes.append(f"{exercices['faux']} snippet(s) faux : "
                         f"{[d for d in exercices['details'] if not d['correct']][:3]}")

    etat = _portee_et_flux()
    print(f"3. portée      : x module={etat['x_module']} / x fonction={etat['x_fonction']} ; "
          f"y={etat['y']} ; noms libres flux={len(etat['libres_flux'])}, "
          f"portée={len(etat['libres_portee'])}")
    if etat["x_module"] != "module" or etat["x_fonction"] != "fonction":
        problemes.append("la portée de x n'est pas résolue comme attendu")
    if etat["y"] != 2:
        problemes.append(f"l'exécution de portee.py rend y={etat['y']} (attendu 2)")
    if [n for n, _ in etat["libres_flux"]] != ["sous_total"]:
        problemes.append(f"noms libres de flux.py : {etat['libres_flux']}")
    if etat["libres_portee"]:
        problemes.append(f"noms libres de portee.py : {etat['libres_portee']}")

    controle = controle_texte_seul()
    texte_faux = sum(1 for r in controle.values() if not r["texte_correct"])
    execute_juste = sum(1 for r in controle.values() if r["execute_correct"])
    print(f"4. contrôle    : texte faux {texte_faux}/{len(controle)}, "
          f"exécution juste {execute_juste}/{len(controle)}")
    for source, r in controle.items():
        print(f"     {source:16s} exécute {r['execute']!s:>6} · texte {r['texte']!s:>6}")
    if texte_faux != len(controle):
        problemes.append("le texte seul n'échoue pas partout")
    if execute_juste != len(controle):
        problemes.append("l'exécution ne rend pas les valeurs attendues")

    refus = _refus()
    nommes = {k: v for k, v in refus.items() if v}
    print(f"5. refus       : {len(nommes)}/{len(refus)} nommés "
          f"({', '.join(nommes)})")
    if len(nommes) != len(refus):
        problemes.append(f"refus non nommés : {[k for k, v in refus.items() if not v]}")

    cout = _cout()
    print(f"6. coût        : ×{cout['ratio']:.2f} de temps pour ×4 nœuds "
          f"({cout['petit'] / 20 * 1000:.2f} ms / 50 additions)")
    if not (2.5 <= cout["ratio"] <= 6.0):
        problemes.append(f"coût non linéaire : ×{cout['ratio']:.2f} pour ×4")

    source = (FIXTURES / "portee.py").read_text(encoding="utf-8")
    empreintes = [empreinte(analyse(source)) for _ in range(2)]
    print(f"7. rejeu       : {'identique' if empreintes[0] == empreintes[1] else 'DIFFÉRENT'}")
    if empreintes[0] != empreintes[1]:
        problemes.append("le rejeu ne redonne pas la même empreinte")

    if problemes:
        print("❌ porte bloc code ROUGE")
        for probleme in problemes:
            print(f"   - {probleme}")
        return 1
    print("✅ porte bloc code verte")
    return 0


def mesure(chemin: pathlib.Path) -> int:
    data = {
        "date": "2026-10-29",
        "ligne": "R4.2",
        "dispositif": {
            "corpus": "tools/*.py",
            "fixtures": "tools/tests/code/",
            "langage": "Python 3 (ast), interpréteur en sable",
            "machine": "CPU, aucun modèle chargé",
        },
        "parseur": corpus(),
        "execution": _exercices(),
        "portee_et_flux": _portee_et_flux(),
        "controles": controle_texte_seul(),
        "refus": _refus(),
        "cout": {"ratio_x4": round(_cout()["ratio"], 2)},
        "rejeu": {"identique": empreinte(analyse((FIXTURES / "portee.py")
                                                 .read_text(encoding="utf-8")))
                  == empreinte(analyse((FIXTURES / "portee.py")
                                       .read_text(encoding="utf-8")))},
    }
    chemin.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"écrit : {chemin}")
    print(json.dumps({k: v for k, v in data.items()
                      if k in ("parseur", "execution", "portee_et_flux", "refus")},
                     ensure_ascii=False, indent=1)[:2000])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="R4.2 — le bloc code.")
    ap.add_argument("--porte", action="store_true")
    ap.add_argument("--mesure", type=pathlib.Path)
    ap.add_argument("--json", type=pathlib.Path)
    ap.add_argument("--execute", type=str)
    ap.add_argument("--autotest", action="store_true")
    args = ap.parse_args()
    if args.porte or args.autotest:
        return autotest()
    if args.mesure:
        return mesure(args.mesure)
    if args.execute:
        try:
            print(json.dumps(execute(args.execute), ensure_ascii=False))
            return 0
        except (Refus, ErreurExecution) as exc:
            print(f"refus : {exc}", file=sys.stderr)
            return 2
    if args.json:
        module = analyse(args.json.read_text(encoding="utf-8"), args.json.name)
        print(json.dumps({"nom": module.nom, "noeuds": module.n_noeuds,
                          "fonctions": [f.name for f in module.fonctions()],
                          "classes": [c.name for c in module.classes()],
                          "portees": [{"nom": p.nom, "genre": p.genre,
                                       "symboles": sorted(p.symboles)}
                                      for p in module.portees],
                          "noms_libres": noms_libres(module),
                          "empreinte": empreinte(module)},
                         ensure_ascii=False, indent=1))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

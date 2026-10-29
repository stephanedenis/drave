#!/usr/bin/env python3
"""bloc_tableaux.py — R4.1 : un tableau est une GRILLE, pas une ligne de texte.

POURQUOI CE FICHIER. R0.1 range les tableaux en **régions** et en garde le texte, aplati :
chaque rangée devient une chaîne tabulée (`graphe_document.py`, `"\\t".join(cellules)`).
C'est suffisant pour *retrouver* une rangée, pas pour la *lire* : on ne peut pas demander
« la somme de la colonne coût », ni « la cellule (ligne 2, colonne durée) », ni joindre
deux tableaux sur une clé. Le banc R0.3 le montre : son type « tableau » rend 27/59
questions dont le gold est une rangée aplatie, et 20 de ces 27 attendent comme réponse le
numéro de l'étiquette de ligne (`B11` → « 11 ») — c'est-à-dire le premier nombre de la rangée.

Ce que ce bloc ajoute, et qui se vérifie :
  1. **la grille** — lignes, colonnes, en-têtes, fusions (`rowspan`/`colspan`), chaque
     cellule portant sa **provenance** exacte (ligne, indice de caractère, offset octet) ;
  2. **le typage** — une cellule est vide, entière, réelle ou texte ; les agrégats refusent
     une colonne non numérique au lieu de sauter les cellules qui dérangent ;
  3. **les opérations classiques** — `filtre`, `jointure`, `agrégat` ; elles rendent le
     résultat exact par construction, sans modèle ;
  4. **les refus nommés** — un tableau irrégulier, un tableau dans un tableau, un tableau
     sans en-tête sont *signalés*, jamais complétés en silence.

La règle du dépôt : **classique d'abord** quand l'information est explicite. Un parseur de
tableaux n'a pas besoin d'être appris ; il a besoin d'être exact, et de le prouver.

Usage :
  python3 tools/bloc_tableaux.py --porte
  python3 tools/bloc_tableaux.py --mesure reports/r41-bloc-tableaux.json
  python3 tools/bloc_tableaux.py --json CHEMIN.md
  python3 tools/bloc_tableaux.py --autotest
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import pathlib
import re
import sys
import time
from collections import Counter

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import graphe_document as gd  # noqa: E402  (inline : la définition partagée du texte visible)


# ------------------------------------------------------------------ les exceptions

class Refus(Exception):
    """Un tableau qu'on refuse de lire — et qu'on NOMME, au lieu de le deviner."""

    def __init__(self, raison: str, ligne: int | None = None, detail: str = "") -> None:
        super().__init__(f"{raison}{f' (ligne {ligne})' if ligne else ''}"
                         f"{f' : {detail}' if detail else ''}")
        self.raison = raison
        self.ligne = ligne
        self.detail = detail


class SansEntete(Exception):
    """Une opération qui exige un nom de colonne sur un tableau qui n'a pas d'en-tête."""


class ColonneInconnue(Exception):
    """Le nom demandé n'est pas un en-tête de ce tableau."""


class NonNumerique(Exception):
    """Un agrégat sur une colonne qui porte du texte : on refuse, on ne saute pas."""


# ------------------------------------------------------------------ le modèle

RE_PREFIXE = re.compile(r"^(\s*(?:>\s*)*)")
RE_SEPARATEUR = re.compile(r"^:?-{1,}:?$")
RE_DEBUT = re.compile(r"^\s*(?:>\s*)*\|")
RE_CITATION = re.compile(r"^\s*>\s*")
RE_NOMBRE = re.compile(r"^[−-]?\d{1,3}(?:[ \u00a0\u202f]\d{3})*(?:[.,]\d+)?$|^[−-]?\d+(?:[.,]\d+)?$")
RE_POURCENT = re.compile(r"^(.*?)\s*%$")


def _offsets(texte: str) -> list[int]:
    """L'offset OCTET du début de chaque ligne (un accent coûte deux octets)."""
    offsets, position = [], 0
    for ligne in texte.splitlines(keepends=True):
        offsets.append(position)
        position += len(ligne.encode("utf-8"))
    return offsets


def _nombre(texte: str) -> float | int | None:
    """La valeur numérique d'une cellule, ou None. On ne devine pas : `12–13` est du texte."""
    t = texte.strip()
    if not t:
        return None
    m = RE_POURCENT.match(t)
    if m:
        t = m.group(1)
    if not RE_NOMBRE.match(t):
        return None
    t = t.replace("−", "-").replace(" ", "").replace("\u00a0", "").replace("\u202f", "")
    if "," in t and "." in t:
        return None  # deux séparateurs décimaux : ambigu, donc texte
    virgule = "," in t
    t = t.replace(",", ".")
    try:
        valeur = float(t)
    except ValueError:
        return None
    if virgule or "." in t:
        return valeur
    return int(valeur)


def type_de(texte: str) -> str:
    """Le type d'une cellule : vide, entier, reel, texte."""
    if not texte.strip():
        return "vide"
    valeur = _nombre(texte)
    if valeur is None:
        return "texte"
    return "entier" if isinstance(valeur, int) else "reel"


class Cellule:
    """Une cellule et sa provenance. `brut` est le texte SOURCE exact ; `texte` le visible."""

    __slots__ = ("texte", "brut", "ligne", "colonne", "debut", "fin", "octet",
                 "fusion", "origine", "bloc")

    def __init__(self, texte: str, brut: str = "", ligne: int = 0, colonne: int = 0,
                 debut: int | None = None, fin: int | None = None, octet: int | None = None,
                 fusion: bool = False, origine: tuple[int, int] | None = None,
                 bloc: int | None = None) -> None:
        self.texte = texte
        self.brut = brut
        self.ligne = ligne
        self.colonne = colonne
        self.debut = debut
        self.fin = fin
        self.octet = octet
        self.fusion = fusion
        self.origine = origine
        self.bloc = bloc

    def valeur(self) -> float | int | None:
        return _nombre(self.texte)

    def __repr__(self) -> str:  # pragma: no cover - confort de débogage
        return f"Cellule({self.texte!r}, l={self.ligne}, c={self.colonne})"


class Grille:
    """Un tableau : en-têtes (ou None), lignes de cellules, fusions, provenance."""

    def __init__(self, source: str, format_: str, entetes: list[str] | None,
                 lignes: list[list[Cellule]], fusions: list[dict] | None = None,
                 sans_entete: bool = False, ligne_debut: int | None = None,
                 octet: int | None = None, legende: str | None = None,
                 refus: str | None = None,
                 entetes_cellules: list[Cellule] | None = None) -> None:
        self.source = source
        self.format = format_
        self.entetes = entetes
        self.entetes_cellules = entetes_cellules or []
        self.lignes = lignes
        self.fusions = fusions or []
        self.sans_entete = sans_entete
        self.ligne_debut = ligne_debut
        self.octet = octet
        self.legende = legende
        self.refus = refus

    @property
    def n_lignes(self) -> int:
        return len(self.lignes)

    @property
    def n_colonnes(self) -> int:
        return max([len(l) for l in self.lignes] + [len(self.entetes or [])])

    @property
    def n_cellules(self) -> int:
        return sum(len(l) for l in self.lignes)

    def colonne(self, nom: str) -> int:
        if self.entetes is None:
            raise SansEntete(f"{self.source} : pas d'en-tête, colonne « {nom} » impossible")
        if nom not in self.entetes:
            raise ColonneInconnue(f"{self.source} : colonne « {nom} » absente de "
                                  f"{self.entetes}")
        return self.entetes.index(nom)

    def resolue(self, ligne: int, colonne: int) -> Cellule:
        """La cellule d'origine : une case couverte par une fusion renvoie son origine."""
        cellule = self.lignes[ligne][colonne]
        if cellule.fusion and cellule.origine is not None:
            return self.lignes[cellule.origine[0]][cellule.origine[1]]
        return cellule

    def texte_plat(self) -> str:
        """Le texte tel que R0.1 le produit : rangées tabulées. C'est le CONTRÔLE négatif."""
        entetes = "\t".join(self.entetes) + "\n" if self.entetes else ""
        return entetes + "\n".join("\t".join(c.texte for c in l) for l in self.lignes)


# ------------------------------------------------------------------ le Markdown

def _cellules_ligne(ligne: str, prefixe: int) -> list[tuple[str, int, int]]:
    """Les champs d'une ligne de tableau : (brut, début, fin) dans la LIGNE originale.

    On découpe sur les `|` NON échappés. `\\|` reste dans le champ : c'est un caractère
    du texte, pas un séparateur. Les indices sont des indices de CARACTÈRE (pour la
    tranche Python) ; l'offset octet de la ligne est porté par la cellule.
    """
    champs: list[tuple[str, int, int]] = []
    debut = None
    i, n = prefixe, len(ligne)
    while i < n:
        c = ligne[i]
        if c == "\\" and i + 1 < n:
            i += 2
            continue
        if c == "|":
            if debut is not None:
                champs.append((ligne[debut:i], debut, i))
            debut = i + 1
        i += 1
    if debut is not None:
        reste = ligne[debut:]
        if reste.strip():
            champs.append((reste, debut, n))
    return champs


def _est_separateur(ligne: str) -> bool:
    m = RE_PREFIXE.match(ligne)
    champs = _cellules_ligne(ligne, len(m.group(1)))
    return bool(champs) and all(RE_SEPARATEUR.match(c[0].strip()) for c in champs)


def _ligne_tableau(ligne: str) -> bool:
    return bool(RE_DEBUT.match(ligne))


def _grille_markdown(lignes: list[str], offsets: list[int], debut: int,
                     source: str) -> tuple[Grille, int]:
    """Une grille à partir de `debut` ; rend (grille, index de la ligne suivante)."""
    prefixe = len(RE_PREFIXE.match(lignes[debut]).group(1))
    champs_entete = _cellules_ligne(lignes[debut], prefixe)
    if len(champs_entete) < 2:
        raise Refus("une seule colonne", debut + 1, "un tableau à 1 colonne n'est pas 2D")
    if not any(brut.strip() for brut, _, _ in champs_entete):
        raise Refus("en-tête vide", debut + 1)

    def cellule(brut: str, d: int, f: int, ligne_idx: int) -> Cellule:
        return Cellule(texte=gd.inline(brut), brut=brut, ligne=ligne_idx + 1,
                       debut=d, fin=f, octet=offsets[ligne_idx])

    i = debut + 1
    entetes: list[str] | None = None
    entetes_cellules: list[Cellule] = []
    sans_entete = True
    if i < len(lignes) and _est_separateur(lignes[i]):
        champs_sep = _cellules_ligne(lignes[i], len(RE_PREFIXE.match(lignes[i]).group(1)))
        if len(champs_sep) != len(champs_entete):
            raise Refus("séparateur incohérent", i + 1,
                        f"{len(champs_sep)} cellules pour {len(champs_entete)} colonnes")
        entetes_cellules = [cellule(brut, d, f, debut) for brut, d, f in champs_entete]
        entetes = [c.texte for c in entetes_cellules]
        sans_entete = False
        i += 1

    rangees: list[list[Cellule]] = []
    if sans_entete:
        rangees.append([cellule(brut, d, f, debut) for brut, d, f in champs_entete])
    while i < len(lignes) and _ligne_tableau(lignes[i]):
        p = len(RE_PREFIXE.match(lignes[i]).group(1))
        champs = _cellules_ligne(lignes[i], p)
        if len(champs) != len(champs_entete):
            raise Refus("rangée irrégulière", i + 1,
                        f"{len(champs)} cellules pour {len(champs_entete)} colonnes")
        rangees.append([cellule(brut, d, f, i) for brut, d, f in champs])
        i += 1

    grille = Grille(source=source, format_="markdown", entetes=entetes, lignes=rangees,
                    sans_entete=sans_entete, ligne_debut=debut + 1, octet=offsets[debut],
                    entetes_cellules=entetes_cellules)
    return grille, i


def markdown(chemin: pathlib.Path) -> list[Grille]:
    """Tous les tableaux Markdown d'un fichier, avec provenance. Les refus sont nommés."""
    texte = chemin.read_text(encoding="utf-8-sig")
    lignes = texte.splitlines()
    offsets = _offsets(texte)
    grilles: list[Grille] = []
    i = 0
    while i < len(lignes):
        if not _ligne_tableau(lignes[i]):
            i += 1
            continue
        try:
            grille, i = _grille_markdown(lignes, offsets, i, str(chemin))
            grilles.append(grille)
        except Refus as refus:
            grilles.append(Grille(source=str(chemin), format_="markdown", entetes=None,
                                  lignes=[], sans_entete=True, refus=str(refus)))
            while i < len(lignes) and _ligne_tableau(lignes[i]):
                i += 1
    return grilles


# ------------------------------------------------------------------ le HTML

def _proche(el, *tags: str):
    return next((a for a in el.iterancestors()
                 if isinstance(a.tag, str) and a.tag.lower() in tags), None)


def _dans(el, tag: str) -> bool:
    """Vrai si `el` a un ancêtre `tag` (thead, tbody…) dans le même tableau."""
    a = el.getparent()
    while a is not None and isinstance(a.tag, str):
        if a.tag.lower() == tag:
            return True
        a = a.getparent()
    return False


def _texte_html(el) -> str:
    return re.sub(r"[ \t\r\n]+", " ", el.text_content()).strip()


def _cellules_html(tr) -> list:
    return [c for c in tr if isinstance(c.tag, str) and c.tag.lower() in ("td", "th")]


def _entetes_html(lignes: list) -> list[str]:
    """Les en-têtes : une ligne = ses textes ; plusieurs lignes = jointes par « / ».

    Une en-tête FUSIONNÉE (colspan/rowspan) est refusée : la jointure par colonne
    inventerait une hiérarchie que le document ne dit pas.
    """
    rangees = [_cellules_html(tr) for tr in lignes]
    for rangee in rangees:
        if any(int(c.get("colspan") or 1) > 1 or int(c.get("rowspan") or 1) > 1
               for c in rangee):
            raise Refus("en-tête fusionné", lignes[0].sourceline if lignes else None)
    largeur = len(rangees[0])
    if any(len(r) != largeur for r in rangees):
        raise Refus("en-têtes de largeurs différentes")
    return [" / ".join(_texte_html(r[c]) for r in rangees) for c in range(largeur)]


def html(chemin: pathlib.Path) -> list[Grille]:
    """Tous les tableaux HTML d'un fichier : thead/th = en-têtes, fusions = spans."""
    import lxml.html  # dépendance déjà utilisée par le graphe (R0.1)

    octets = chemin.read_bytes()
    try:
        document = lxml.html.document_fromstring(octets.decode("utf-8-sig"))
    except (UnicodeDecodeError, ValueError):
        document = lxml.html.document_fromstring(octets)

    grilles: list[Grille] = []
    for table in document.iter("table"):
        if not isinstance(table.tag, str):
            continue
        if _proche(table, "table") is not None:
            continue  # traité — et refusé — avec son tableau parent
        rangees = [tr for tr in table.iter("tr") if _proche(tr, "table") is table]
        if not rangees:
            continue
        legende = next((_texte_html(c) for c in table.iter("caption")
                        if _proche(c, "table") is table), None)
        try:
            lignes_entete = [tr for tr in rangees if _dans(tr, "thead")]
            if lignes_entete:
                entetes = _entetes_html(lignes_entete)
                corps = [tr for tr in rangees if tr not in lignes_entete]
            else:
                premiere = _cellules_html(rangees[0])
                if premiere and all(c.tag.lower() == "th" for c in premiere):
                    entetes = [_texte_html(c) for c in premiere]
                    corps = rangees[1:]
                else:
                    entetes = None
                    corps = rangees

            occupe: dict[tuple[int, int], tuple[int, int]] = {}
            origine_de: dict[tuple[int, int], Cellule] = {}
            fusions: list[dict] = []
            largeur = len(entetes) if entetes else 0
            for r, tr in enumerate(corps):
                c = 0
                for cellule in _cellules_html(tr):
                    while (r, c) in occupe:
                        c += 1
                    if cellule.find(".//table") is not None:
                        raise Refus("tableau imbriqué dans une cellule", tr.sourceline,
                                    "refusé, pas aplati")
                    colspan = max(1, int(cellule.get("colspan") or 1))
                    rowspan = max(1, int(cellule.get("rowspan") or 1))
                    texte = _texte_html(cellule)
                    if rowspan > 1 or colspan > 1:
                        fusions.append({"ligne": r, "colonne": c, "lignes": rowspan,
                                        "colonnes": colspan, "texte": texte})
                    for dr in range(rowspan):
                        for dc in range(colspan):
                            occupe[(r + dr, c + dc)] = (r, c)
                            if (dr, dc) == (0, 0):
                                origine_de[(r, c)] = Cellule(
                                    texte=texte, brut=texte, ligne=(tr.sourceline or 0),
                                    colonne=c, bloc=r, origine=(r, c))
                            else:
                                origine_de[(r + dr, c + dc)] = Cellule(
                                    texte="", brut="", ligne=(tr.sourceline or 0),
                                    colonne=c + dc, fusion=True, origine=(r, c), bloc=r)
                    c += colspan
                    largeur = max(largeur, c)

            hauteur = max((r for (r, _) in occupe), default=-1) + 1
            if hauteur == 0:
                continue
            corps_grille = [[origine_de[(r, c)] for c in range(largeur)]
                            for r in range(hauteur)]
            if entetes is not None and largeur != len(entetes):
                raise Refus("largeur incohérente", table.sourceline,
                            f"{largeur} colonnes pour {len(entetes)} en-têtes")
            # la fidélité : la grille ne perd ni ne duplique aucune cellule du DOM
            du_dom = [_texte_html(c) for tr in corps for c in _cellules_html(tr)]
            de_la_grille = [c.texte for l in corps_grille for c in l if not c.fusion]
            if Counter(du_dom) != Counter(de_la_grille):
                raise Refus("fidélité HTML", table.sourceline,
                            f"{len(du_dom)} cellules du DOM contre "
                            f"{len(de_la_grille)} dans la grille")
        except Refus as refus:
            grilles.append(Grille(source=str(chemin), format_="html", entetes=None,
                                  lignes=[], sans_entete=True, refus=str(refus)))
            continue
        if not any(c.texte for l in corps_grille for c in l):
            continue
        grilles.append(Grille(source=str(chemin), format_="html", entetes=entetes,
                              lignes=corps_grille, fusions=fusions,
                              sans_entete=entetes is None,
                              ligne_debut=table.sourceline, legende=legende))
    return grilles


# ------------------------------------------------------------------ le CSV

def csv_(chemin: pathlib.Path, entetes: bool = True, limite: int | None = None) -> Grille:
    """Un CSV : la première ligne est l'en-tête (déclaré, pas deviné) ; largeur constante."""
    with chemin.open(newline="", encoding="utf-8-sig") as fichier:
        lecteur = csv.reader(fichier)
        rangees = [r for _, r in zip(range(limite or 10 ** 9), lecteur)]
    if not rangees:
        raise Refus("CSV vide", None)
    largeur = len(rangees[0])
    for numero, rangee in enumerate(rangees, start=1):
        if len(rangee) != largeur:
            raise Refus("rangée irrégulière", numero,
                        f"{len(rangee)} champs pour {largeur} colonnes")
        # le contrôle indépendant : le writer doit redonner exactement les mêmes champs
        tampon = io.StringIO()
        csv.writer(tampon).writerow(rangee)
        relu = next(csv.reader(io.StringIO(tampon.getvalue())))
        if relu != rangee:
            raise Refus("aller-retour CSV", numero, f"{rangee} ≠ {relu}")
    noms = [c.strip() for c in rangees[0]] if entetes else None
    debut = 2 if entetes else 1
    corps = [[Cellule(texte=c.strip(), brut=c, ligne=numero, colonne=col, bloc=numero - 1)
              for col, c in enumerate(rangee)]
             for numero, rangee in enumerate(rangees[1:] if entetes else rangees, start=debut)]
    return Grille(source=str(chemin), format_="csv", entetes=noms, lignes=corps,
                  sans_entete=not entetes, ligne_debut=1)


# ------------------------------------------------------------------ les opérations

def filtre(grille: Grille, colonne: str, valeur: str) -> list[list[Cellule]]:
    """Les rangées dont `colonne` vaut `valeur` (égalité numérique si les deux le sont)."""
    index = grille.colonne(colonne)
    cible = _nombre(valeur)
    gardees = []
    for numero, rangee in enumerate(grille.lignes):
        cellule = grille.resolue(numero, index)
        if cible is not None and cellule.valeur() is not None:
            if cellule.valeur() == cible:
                gardees.append(rangee)
        elif cellule.texte == valeur:
            gardees.append(rangee)
    return gardees


def agregat(grille: Grille, colonne: str, operation: str) -> float | int:
    """Somme, moyenne, min, max, compte d'une colonne NUMÉRIQUE.

    On refuse une colonne non numérique au lieu de sauter les cellules : sauter les
    cellules qui dérangent est la façon la plus sûre de rendre un agrégat faux sans le dire.
    """
    index = grille.colonne(colonne)
    valeurs: list[float | int] = []
    for numero in range(len(grille.lignes)):
        cellule = grille.resolue(numero, index)
        if cellule.texte.strip() == "":
            continue
        v = cellule.valeur()
        if v is None:
            raise NonNumerique(f"{grille.source} : « {cellule.texte} » n'est pas un nombre "
                               f"(colonne « {colonne} », ligne {numero + 1})")
        valeurs.append(v)
    if not valeurs:
        raise NonNumerique(f"{grille.source} : colonne « {colonne} » vide")
    if operation == "somme":
        return sum(valeurs)
    if operation == "moyenne":
        return sum(valeurs) / len(valeurs)
    if operation == "min":
        return min(valeurs)
    if operation == "max":
        return max(valeurs)
    if operation == "compte":
        return len(valeurs)
    raise ValueError(f"opération inconnue : {operation}")


def jointure(gauche: Grille, colonne_gauche: str,
             droite: Grille, colonne_droite: str) -> list[dict[str, str]]:
    """Jointure interne sur l'égalité des clés ; les clés absentes ne sont pas inventées."""
    if gauche.entetes is None or droite.entetes is None:
        raise SansEntete("une jointure exige deux en-têtes : on ne joint pas des colonnes "
                         "anonymes")
    ig, id_ = gauche.colonne(colonne_gauche), droite.colonne(colonne_droite)
    index: dict[str, list[list[Cellule]]] = {}
    for rangee in droite.lignes:
        index.setdefault(rangee[id_].texte.strip(), []).append(rangee)
    resultat: list[dict[str, str]] = []
    for rg in gauche.lignes:
        cle = rg[ig].texte.strip()
        for rd in index.get(cle, []):
            ligne = {f"g.{nom}": (rg[i].texte if i < len(rg) else "")
                     for i, nom in enumerate(gauche.entetes or [])}
            ligne.update({f"d.{nom}": (rd[i].texte if i < len(rd) else "")
                          for i, nom in enumerate(droite.entetes or [])})
            resultat.append(ligne)
    return resultat


# ------------------------------------------------------------------ le corpus et les mesures

CORPUS = [
    # documents du dépôt : les tables y sont réelles, et ils changent peu
    "docs/pilotage/manques.md",
    "docs/methode/resultats.md",
    "docs/implantation/document-graph.md",
    "docs/theorie/vision.md",
    "docs/pilotage/backlog/dependances.md",
    "docs/archive/plan-deepseek41-complet.md",   # tableau dans une citation
    "docs/archive/colab-reparti.md",             # tableau indenté dans une liste
    # HTML et CSV
    "tools/tests/documents/html/article.html",
    "tools/tests/documents/html/entites.html",
    "data/glottolog/languages.csv",
]

FIXTURES = RACINE / "tools" / "tests" / "tableaux"


def corpus_grilles() -> list[Grille]:
    """Le corpus : chaque fichier rend ses tableaux, les refus sont conservés (nommés)."""
    grilles: list[Grille] = []
    for chemin in CORPUS:
        fichier = RACINE / chemin
        if not fichier.exists():
            continue
        if fichier.suffix == ".csv":
            try:
                grilles.append(csv_(fichier, limite=21))
            except Refus as refus:
                grilles.append(Grille(source=chemin, format_="csv", entetes=None,
                                      lignes=[], sans_entete=True, refus=str(refus)))
        elif fichier.suffix in (".html", ".htm"):
            grilles.extend(html(fichier))
        else:
            grilles.extend(markdown(fichier))
    return grilles


def _grille_fixture(nom: str) -> Grille:
    chemin = FIXTURES / nom
    if chemin.suffix == ".csv":
        return csv_(chemin)
    if chemin.suffix == ".html":
        grille = html(chemin)[0]
    else:
        grille = markdown(chemin)[0]
    if grille.refus:
        raise Refus(grille.refus)
    return grille


def manifeste(grille: Grille) -> dict:
    """Empreinte stable d'une grille : deux lectures du même fichier la redonnent."""
    charge = {
        "source": grille.source,
        "format": grille.format,
        "entetes": grille.entetes,
        "fusions": grille.fusions,
        "cellules": [[{"t": c.texte, "f": c.fusion, "o": c.origine} for c in ligne]
                     for ligne in grille.lignes],
    }
    return {"sha256": hashlib.sha256(json.dumps(charge, ensure_ascii=False,
                                                sort_keys=True).encode()).hexdigest(),
            "n_lignes": grille.n_lignes, "n_colonnes": grille.n_colonnes}


def provenance_exacte(grilles: list[Grille]) -> tuple[int, int, list[str]]:
    """Chaque cellule Markdown doit être EXACTEMENT la tranche de source qu'elle déclare."""
    exactes = total = 0
    erreurs: list[str] = []
    for grille in grilles:
        if grille.format != "markdown":
            continue
        lignes = pathlib.Path(grille.source).read_text(encoding="utf-8-sig").splitlines()
        toutes = list(grille.entetes_cellules) + [c for r in grille.lignes for c in r]
        for cellule in toutes:
            total += 1
            if cellule.debut is None or cellule.fin is None:
                erreurs.append(f"{grille.source}: cellule sans provenance")
                continue
            tranche = lignes[cellule.ligne - 1][cellule.debut:cellule.fin]
            if tranche == cellule.brut and gd.inline(tranche) == cellule.texte:
                exactes += 1
            else:
                erreurs.append(f"{grille.source}:{cellule.ligne} "
                               f"« {tranche!r} » ≠ « {cellule.brut!r} »")
    return exactes, total, erreurs


def controle_texte_plat() -> dict:
    """Les trois questions de structure, et le contrôle « texte plat » qui DOIT échouer.

    Le texte plat garde les lignes et les mots, pas les colonnes : il ne peut pas
    distinguer deux colonnes numériques, ni désambiguïser une valeur répétée. Le contrôle
    est construit pour que la réponse plate soit fausse — ce n'est pas une preuve que tout
    lecteur plat échoue, c'est la preuve que la COLONNE porte l'information.
    """
    grille = _grille_fixture("mesures.md")
    plat = grille.texte_plat()
    resultats = {}

    # 1. somme d'une colonne dont une AUTRE colonne porte aussi des nombres
    attendu = agregat(grille, "coût", "somme")
    tous_nombres = sum(v for v in (_nombre(t) for t in
                                   re.findall(r"[−-]?\d+(?:[.,]\d+)?", plat))
                       if v is not None)
    resultats["somme_colonne"] = {"grille": attendu, "plat": tous_nombres,
                                  "plat_correct": tous_nombres == attendu}

    # 2. la cellule (ligne 2, colonne « durée ») — le plat rend la ligne entière
    index = grille.colonne("durée")
    attendu2 = grille.lignes[1][index].texte
    ligne_plate = "\t".join(c.texte for c in grille.lignes[1])
    resultats["cellule_2_2"] = {"grille": attendu2, "plat": ligne_plate,
                                "plat_correct": ligne_plate.strip() == attendu2}

    # 3. compter les lignes où « état » vaut « rouge » — le plat compte les autres colonnes
    attendu3 = len(filtre(grille, "état", "rouge"))
    plat3 = plat.count("rouge")
    resultats["filtre_etat"] = {"grille": attendu3, "plat": plat3,
                                "plat_correct": plat3 == attendu3}
    return resultats


def _attendus() -> dict:
    """Les opérations à réponse connue, sur des fixtures."""
    mesures = _grille_fixture("mesures.md")
    notes = _grille_fixture("notes.csv")
    eleves = _grille_fixture("eleves.csv")
    return {
        "somme_coût": (agregat(mesures, "coût", "somme"), 120),
        "moyenne_durée": (agregat(mesures, "durée", "moyenne"), 3.0),
        "min_coût": (agregat(mesures, "coût", "min"), 10),
        "max_coût": (agregat(mesures, "coût", "max"), 50),
        "filtre_rouge": (len(filtre(mesures, "état", "rouge")), 2),
        "filtre_numérique": (len(filtre(mesures, "coût", "40")), 1),
        "jointure_notes_élèves": (len(jointure(notes, "élève", eleves, "élève")), 3),
        "entête_multiniveau": (" · ".join(_grille_fixture("multi-niveaux.html").entetes or []),
                               "Région / Zone · Mois / Janvier · Mois / Février"),
    }


def _correct(valeur, attendu) -> bool:
    if isinstance(attendu, float) and isinstance(valeur, (int, float)):
        return abs(valeur - attendu) < 1e-9
    return valeur == attendu


def _synthetique(rangees: int) -> tuple[list[str], list[int]]:
    """Une grille en mémoire : le coût doit suivre les CELLULES, pas les fichiers."""
    lignes = ["| a | b | c |", "|---|---|---|"] + [
        f"| {i} | {i + 1} | {i + 2} |" for i in range(rangees)]
    offsets, position = [], 0
    for ligne in lignes:
        offsets.append(position)
        position += len(ligne.encode("utf-8")) + 1
    return lignes, offsets


def _linearite() -> dict:
    """Quatre fois plus de cellules doivent coûter ~quatre fois plus de temps."""
    def temps(rangees: int) -> float:
        lignes, offsets = _synthetique(rangees)
        debut = time.perf_counter()
        for _ in range(40):
            _grille_markdown(lignes, offsets, 0, "synthétique")
        return time.perf_counter() - debut

    petit = min(temps(50) for _ in range(3))
    grand = min(temps(200) for _ in range(3))
    return {"petit": petit, "grand": grand, "ratio": grand / max(petit, 1e-9)}


def autotest() -> int:
    """Le test que la porte appelle : corpus, provenance, en-têtes, opérations, contrôles."""
    print("=== PORTE R4.1 — LE BLOC TABLEAUX ===")
    problemes: list[str] = []
    grilles = corpus_grilles()
    refusees = [g for g in grilles if g.refus]
    tables = [g for g in grilles if not g.refus]
    cellules = sum(g.n_cellules for g in tables)
    avec_entete = sum(1 for g in tables if g.entetes is not None)

    exactes, total, erreurs = provenance_exacte(tables)
    formats = Counter(g.format for g in tables)
    print(f"1. corpus      : {len(tables)} tableaux, {cellules} cellules "
          f"({', '.join(f'{n} {f}' for f, n in sorted(formats.items()))}), "
          f"{len(refusees)} refus nommés")
    print(f"   provenance  : {exactes}/{total} cellules exactement à leur place")
    if total < 100:
        problemes.append(f"seulement {total} cellules mesurées (< 100)")
    if exactes != total:
        problemes.append(f"{total - exactes} cellules sans provenance exacte : "
                         f"{erreurs[:3]}")
    if avec_entete < 5:
        problemes.append(f"{avec_entete} tableaux avec en-tête (< 5)")

    # 2. les opérations, sur des fixtures à réponse connue
    attendus = _attendus()
    justes = sum(1 for valeur, attendu in attendus.values() if _correct(valeur, attendu))
    print(f"2. opérations  : {justes}/{len(attendus)} justes")
    for nom, (valeur, attendu) in attendus.items():
        if not _correct(valeur, attendu):
            problemes.append(f"opération « {nom} » : {valeur} ≠ {attendu}")

    # 3. les contrôles négatifs
    controle = controle_texte_plat()
    plats_faux = sum(1 for r in controle.values() if not r["plat_correct"])
    print(f"3. contrôle    : texte plat faux {plats_faux}/{len(controle)}, "
          f"grille juste {len(controle)}/{len(controle)}")
    for nom, resultat in controle.items():
        if not resultat["plat_correct"]:
            print(f"     {nom:14s} grille {resultat['grille']!s:>8} · "
                  f"plat {resultat['plat']!s:>8}")
    if plats_faux != len(controle):
        problemes.append("le texte plat ne rate pas tous les contrôles : le contrôle "
                         "ne prouve rien")

    # 3 bis. les refus nommés
    sans_entete = _grille_fixture("sans-entete.md")
    if not sans_entete.sans_entete or sans_entete.entetes is not None:
        problemes.append("un tableau sans en-tête n'est pas signalé")
    try:
        agregat(sans_entete, "coût", "somme")
        problemes.append("une opération a réussi sur un tableau sans en-tête")
    except SansEntete:
        pass
    try:
        _grille_fixture("irregulier.md")
        problemes.append("un tableau irrégulier a été accepté")
    except Refus:
        pass
    fusions = _grille_fixture("fusions.html")
    couvertes = sum(1 for l in fusions.lignes for c in l if c.fusion)
    if len(fusions.fusions) < 2 or couvertes < 2:
        problemes.append(f"fusions non marquées : {len(fusions.fusions)} fusions, "
                         f"{couvertes} cases couvertes")
    try:
        _grille_fixture("entete-fusionnee.html")
        problemes.append("une en-tête fusionnée a été acceptée (hiérarchie inventée)")
    except Refus:
        pass
    try:
        _grille_fixture("imbrique.html")
        problemes.append("un tableau imbriqué a été aplati en silence")
    except Refus:
        pass
    print(f"   refus        : sans en-tête signalé, irrégulier refusé, en-tête fusionnée "
          f"refusée, tableau imbriqué refusé, {len(fusions.fusions)} fusions marquées "
          f"({couvertes} cases couvertes)")

    # 3 ter. le typage : une colonne numérique s'agrège, une colonne de texte est refusée
    mesures = _grille_fixture("mesures.md")
    types_coût = [type_de(mesures.resolue(i, mesures.colonne("coût")).texte)
                  for i in range(mesures.n_lignes)]
    types_état = [type_de(mesures.resolue(i, mesures.colonne("état")).texte)
                  for i in range(mesures.n_lignes)]
    if types_coût != ["entier"] * mesures.n_lignes:
        problemes.append(f"typage du coût faux : {types_coût}")
    if set(types_état) != {"texte"}:
        problemes.append(f"typage de l'état faux : {types_état}")
    if _refus_nomme(lambda: agregat(mesures, "note", "somme")) != "NonNumerique":
        problemes.append("un agrégat sur une colonne de texte n'est pas refusé")
    print(f"   typage       : coût {types_coût.count('entier')}/{len(types_coût)} entiers, "
          f"état texte {types_état.count('texte')}/{len(types_état)}, "
          f"agrégat sur texte refusé")

    # 4. le coût : une grille 4× plus grande doit coûter ~4× plus cher (en mémoire)
    cout = _linearite()
    print(f"4. coût        : ×{cout['ratio']:.2f} de temps pour ×4 cellules "
          f"({cout['petit'] / 40 * 1000:.2f} ms / 150 cellules)")
    if not (2.5 <= cout["ratio"] <= 6.0):
        problemes.append(f"coût non linéaire : ×{cout['ratio']:.2f} pour ×4")

    # 5. le rejeu : deux lectures du même fichier donnent la même empreinte
    empreintes = [manifeste(g)["sha256"] for g in markdown(RACINE / CORPUS[0])]
    empreintes2 = [manifeste(g)["sha256"] for g in markdown(RACINE / CORPUS[0])]
    print(f"5. rejeu       : {'identique' if empreintes == empreintes2 else 'DIFFÉRENT'} "
          f"({len(empreintes)} tableaux)")
    if empreintes != empreintes2:
        problemes.append("le rejeu ne redonne pas la même empreinte")

    if problemes:
        print("❌ porte bloc tableaux ROUGE")
        for probleme in problemes:
            print(f"   - {probleme}")
        return 1
    print("✅ porte bloc tableaux verte")
    return 0


def mesure(chemin: pathlib.Path) -> int:
    """Le JSON de la fiche : les chiffres, le dispositif, les contrôles, les refus."""
    grilles = corpus_grilles()
    tables = [g for g in grilles if not g.refus]
    refusees = [g for g in grilles if g.refus]
    exactes, total, erreurs = provenance_exacte(tables)

    mesures = _grille_fixture("mesures.md")
    notes = _grille_fixture("notes.csv")
    eleves = _grille_fixture("eleves.csv")
    operations = {
        "somme_coût": agregat(mesures, "coût", "somme"),
        "moyenne_durée": agregat(mesures, "durée", "moyenne"),
        "min_coût": agregat(mesures, "coût", "min"),
        "max_coût": agregat(mesures, "coût", "max"),
        "filtre_rouge": len(filtre(mesures, "état", "rouge")),
        "jointure": len(jointure(notes, "élève", eleves, "élève")),
        "entête_multiniveau": _grille_fixture("multi-niveaux.html").entetes,
    }
    controles = controle_texte_plat()
    sans_entete = _grille_fixture("sans-entete.md")
    fusions = _grille_fixture("fusions.html")

    # coût : secondes par corpus complet, moyenne de 5 passes
    debut = time.perf_counter()
    for _ in range(5):
        corpus_grilles()
    duree = (time.perf_counter() - debut) / 5
    cellules = sum(g.n_cellules for g in tables)

    data = {
        "date": "2026-10-29",
        "ligne": "R4.1",
        "dispositif": {
            "corpus_fichiers": len({g.source for g in tables}),
            "corpus_tableaux": len(tables),
            "corpus_cellules": cellules,
            "formats": sorted({g.format for g in tables}),
            "machine": "CPU, aucun modèle chargé",
        },
        "grille": {
            "cellules_markdown_mesurees": total,
            "provenance_exacte": exactes,
            "avec_entete": sum(1 for g in tables if g.entetes is not None),
            "sans_entete": sum(1 for g in tables if g.sans_entete),
            "refus": [{"source": g.source, "raison": g.refus} for g in refusees],
            "erreurs": erreurs[:5],
        },
        "operations": operations,
        "controles": controles,
        "fusions": {"declarées": len(fusions.fusions),
                    "cases_couvertes": sum(1 for l in fusions.lignes for c in l if c.fusion)},
        "sans_entete": {"signale": sans_entete.sans_entete,
                        "operation_refusee": _refus_nomme(
                            lambda: agregat(sans_entete, "coût", "somme"))},
        "refus_fixtures": {
            "irregulier": _refus_nomme(lambda: _grille_fixture("irregulier.md")),
            "entete_fusionnee": _refus_nomme(
                lambda: _grille_fixture("entete-fusionnee.html")),
            "imbrique": _refus_nomme(lambda: _grille_fixture("imbrique.html")),
            "colonne_texte_non_sommable": _refus_nomme(
                lambda: agregat(mesures, "note", "somme")),
        },
        "cout": {"secondes_corpus": round(duree, 4),
                 "millisecondes_par_1000_cellules": round(duree / max(cellules, 1) * 1e6, 1),
                 "ratio_x4": round(_linearite()["ratio"], 2)},
        "rejeu": {"identique": [manifeste(g)["sha256"] for g in markdown(
            RACINE / CORPUS[0])] == [manifeste(g)["sha256"] for g in markdown(
                RACINE / CORPUS[0])]},
    }
    chemin.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"écrit : {chemin}")
    print(json.dumps({k: v for k, v in data.items() if k != "grille"},
                     ensure_ascii=False, indent=1))
    return 0


def _refus_nomme(action) -> str | None:
    try:
        action()
        return None
    except Exception as exc:  # noqa: BLE001 - on veut le NOM du refus, pas sa trace
        return type(exc).__name__


def main() -> int:
    ap = argparse.ArgumentParser(description="R4.1 — le bloc tableaux.")
    ap.add_argument("--porte", action="store_true", help="les contrôles de la porte")
    ap.add_argument("--mesure", type=pathlib.Path, help="écrit le JSON de la fiche")
    ap.add_argument("--json", type=pathlib.Path, help="les grilles d'un fichier")
    ap.add_argument("--autotest", action="store_true", help="alias de --porte")
    args = ap.parse_args()
    if args.porte or args.autotest:
        return autotest()
    if args.mesure:
        return mesure(args.mesure)
    if args.json:
        grilles = (csv_(args.json) if args.json.suffix == ".csv"
                   else html(args.json) if args.json.suffix in (".html", ".htm")
                   else markdown(args.json))
        if isinstance(grilles, Grille):
            grilles = [grilles]
        print(json.dumps([{"source": g.source, "format": g.format, "entetes": g.entetes,
                           "sans_entete": g.sans_entete, "refus": g.refus,
                           "fusions": g.fusions,
                           "lignes": [[c.texte for c in l] for l in g.lignes]}
                          for g in grilles], ensure_ascii=False, indent=1))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

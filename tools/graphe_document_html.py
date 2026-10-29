#!/usr/bin/env python3
"""Extrait le graphe de blocs d'un document HTML pour le chantier R0.1.

Le cœur assemble le manifeste et insère les blancs : ce module ne rend que des
blocs de corps, en ordre de DOM. Un `li` donne un bloc, même imbriqué ; son
texte est coupé autour des sous-listes, qui sortent à leur position. De même, un
paragraphe contenant une note (`sup`) ou une formule est coupé : la note sort en
bloc `note`, jamais comptée comme du corps. La fidélité se compare à
`text_content()` blancs retirés, car cette fonction ne sépare pas les blocs
(`<p>a</p><p>b</p>` donne « ab ») : comparer les espaces testerait la mise en
forme de la source, pas le texte visible.
"""
from __future__ import annotations

import difflib
import json
import pathlib
import re
import sys
from collections import Counter

import lxml.html

IGNORES = frozenset({"script", "style", "noscript", "nav"})
TITRES = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
BLOCS = frozenset("title h1 h2 h3 h4 h5 h6 p ul ol li table caption pre code "
                  "figure figcaption aside".split())
# Un marqueur de note (`marque<sup>1</sup>`) est un token numérique : le séparer
# des lettres rend le ratio insensible à la frontière de bloc, pas au contenu.
MOT = re.compile(r"\d+|[^\W\d_]+")


def _normalise(texte: str) -> str:
    """Compacte les blancs : le contrat veut des paragraphes sur une ligne."""
    return re.sub(r"\s+", " ", texte.replace("\u00a0", " ")).strip()


def _cle(texte: str) -> str:
    """Suite des caractères visibles, blancs retirés, pour l'égalité de fidélité."""
    return re.sub(r"\s+", "", texte.replace("\u00a0", " "))


def _est_math(el) -> bool:
    """`math`, `.math`, `[class*=math]` et `script[type*=math]` sont des formules."""
    tag = el.tag.lower()
    if tag == "math":
        return True
    if tag == "script":
        return "math" in (el.get("type") or "").lower()
    return "math" in (el.get("class") or "").lower()


def _ignore(el) -> bool:
    """Sortent du document les éléments de site ; un script de formule reste."""
    tag = el.tag.lower()
    return tag in IGNORES and not (tag == "script" and _est_math(el))


def _visible(el, exclure: frozenset[str] = frozenset()) -> str:
    """Texte brut d'un sous-arbre, sans les ignorés ni les tags de `exclure`."""
    if isinstance(el.tag, str) and _ignore(el):
        return ""
    morceaux = [el.text or ""]
    for enfant in el:
        if isinstance(enfant.tag, str) and enfant.tag.lower() not in exclure:
            morceaux.append(_visible(enfant, exclure))
        morceaux.append(enfant.tail or "")
    return "".join(morceaux)


def _texte(el, exclure: frozenset[str] = frozenset()) -> str:
    """Texte visible compacté, prêt pour le champ `texte` d'un bloc."""
    return _normalise(_visible(el, exclure))


def _est_note(el) -> bool:
    """Notes : `aside`, rôle doc-footnote, `.footnote`, `sup` qui porte du texte."""
    tag = el.tag.lower()
    if tag == "aside" or (el.get("role") or "").lower() == "doc-footnote":
        return True
    if "footnote" in (el.get("class") or "").lower().split():
        return True
    return tag == "sup" and bool(_texte(el))


def _special(el) -> bool:
    """Élément qui doit sortir en bloc propre, même au milieu d'un paragraphe."""
    return (_est_math(el) or _est_note(el)
            or el.tag.lower() in {"figure", "table", "pre", "ul", "ol"})


def _proche(el, *tags: str):
    """Ancêtre le plus proche portant l'un des tags, pour délimiter tables et listes."""
    return next((a for a in el.iterancestors()
                 if isinstance(a.tag, str) and a.tag.lower() in tags), None)


def _lire(chemin: pathlib.Path):
    """Décode d'abord en UTF-8 (souvent non déclaré) ; sinon lxml lit les octets."""
    octets = chemin.read_bytes()
    try:
        return lxml.html.document_fromstring(octets.decode("utf-8-sig"))
    except (UnicodeDecodeError, ValueError):
        return lxml.html.document_fromstring(octets)


def _reference(chemin: pathlib.Path) -> str:
    """Texte visible de référence : text_content() moins les éléments ignorés."""
    return _visible(_lire(chemin))


def analyse(chemin: pathlib.Path) -> list[dict]:
    """Blocs en ordre de lecture : ``{"type", "texte", "prov": {"bloc": n}}``."""
    blocs: list[dict] = []

    def ajoute(type_: str, texte: str, niveau: int | None = None) -> None:
        texte = texte.strip()
        if not texte:
            return
        prov = {"bloc": len(blocs)}
        if niveau is not None:
            prov["niveau"] = niveau
        blocs.append({"type": type_, "texte": texte, "prov": prov})

    def est_bloc(el) -> bool:
        tag = el.tag.lower()
        return tag not in {"html", "body", "head"} and (
            tag in BLOCS or _est_math(el) or _est_note(el))

    def decouper(el, type_: str, niveau: int | None = None, tout: bool = False) -> None:
        """Émet le texte d'un conteneur en blocs, coupé autour des éléments spéciaux.

        `tout=True` parcourt un conteneur structurel (body, div) : tout bloc du DOM
        y est une frontière. `tout=False` parcourt un p ou un li : seul un bloc
        réellement incompatible (note, formule, sous-liste) coupe le texte.
        """
        tampon: list[str] = []

        def vider() -> None:
            if tampon:
                ajoute(type_, _normalise("".join(tampon)), niveau)
                tampon.clear()

        def visiter(noeud) -> None:
            if noeud.text:
                tampon.append(noeud.text)
            for enfant in noeud:
                if not isinstance(enfant.tag, str):
                    continue
                if _ignore(enfant):
                    pass
                elif (est_bloc(enfant) if tout else _special(enfant)):
                    vider()
                    emettre(enfant)
                else:
                    visiter(enfant)
                if enfant.tail:
                    tampon.append(enfant.tail)

        visiter(el)
        vider()

    def emettre(el) -> None:
        tag = el.tag.lower()
        if _est_math(el):
            ajoute("maths", _normalise(
                el.get("alttext") or el.get("aria-label") or _texte(el)))
        elif _est_note(el):
            ajoute("note", _texte(el))
        elif tag in TITRES:
            decouper(el, "titre" if tag == "h1" else "section", int(tag[1]))
        elif tag == "title":
            ajoute("titre", _normalise(el.text_content()))
        elif tag in ("p", "li"):
            decouper(el, "paragraphe" if tag == "p" else "liste")
        elif tag in ("ul", "ol"):
            for li in el.iter("li"):
                if _proche(li, "ul", "ol") is el:
                    decouper(li, "liste")
        elif tag == "table":
            for cap in el.iter("caption"):
                if _proche(cap, "table") is el:
                    ajoute("legende", _texte(cap))
            lignes = ["\t".join(_texte(c) for c in ligne if isinstance(c.tag, str)
                                and c.tag.lower() in ("td", "th"))
                      for ligne in el.iter("tr") if _proche(ligne, "table") is el]
            if any(ligne.strip() for ligne in lignes):
                ajoute("tableau", "\n".join(lignes))
        elif tag in ("pre", "code"):
            ajoute("code", el.text_content())  # verbatim, seuls les bords sont ôtés
        elif tag == "figure":
            ajoute("figure", _texte(el, {"figcaption"}))
            for cap in el.iter("figcaption"):
                if _proche(cap, "figure") is el:
                    ajoute("legende", _texte(cap))
        else:  # caption ou figcaption hors conteneur
            ajoute("legende", _texte(el))

    decouper(_lire(chemin), "paragraphe", tout=True)
    return blocs


def verifie(chemin: pathlib.Path) -> tuple[bool, float, list[str]]:
    """Compare les blocs au texte visible ; rend égalité, ratio de mots et écarts."""
    blocs = analyse(chemin)
    attendu = _reference(chemin)
    obtenu = "".join(bloc["texte"] for bloc in blocs)
    egal = _cle(attendu) == _cle(obtenu)
    mots_a = MOT.findall(_normalise(attendu))
    mots_b = MOT.findall(_normalise(" ".join(bloc["texte"] for bloc in blocs)))
    communs = sum((Counter(mots_a) & Counter(mots_b)).values())
    ratio = 2.0 * communs / (len(mots_a) + len(mots_b)) if (mots_a or mots_b) else 1.0
    ecarts: list[str] = []
    if not egal:
        a, b = _cle(attendu), _cle(obtenu)
        for balise, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
            if balise != "equal":
                ecarts.append(
                    f"{balise} : attendu {a[i1:i2][:60]!r} / obtenu {b[j1:j2][:60]!r}")
                if len(ecarts) == 8:
                    break
    return egal, ratio, ecarts


def autotest() -> int:
    """Joue les trois fixtures : fidélité, ratio, types et verdict par fixture."""
    dossier = pathlib.Path(__file__).resolve().parent / "tests" / "documents" / "html"
    echecs = 0
    for nom in ("article.html", "deux-colonnes.html", "entites.html"):
        blocs = analyse(dossier / nom)
        ok, ratio, ecarts = verifie(dossier / nom)
        types = ", ".join(sorted({bloc["type"] for bloc in blocs}))
        print(f"{nom} : {len(blocs)} blocs, fidélité {'OK' if ok else 'ECHEC'}, "
              f"ratio {ratio:.3f}, types {types}")
        for ecart in ecarts:
            print(f"  écart : {ecart}")
        echecs += 0 if ok else 1
    print(f"verdict : {3 - echecs}/3 fixtures fidèles")
    return 0 if echecs == 0 else 1


def main(argv: list[str]) -> int:
    if "--autotest" in argv:
        return autotest()
    if len(argv) != 2:
        print("usage : graphe_document_html.py CHEMIN.html | --autotest", file=sys.stderr)
        return 2
    print(json.dumps(analyse(pathlib.Path(argv[1])), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

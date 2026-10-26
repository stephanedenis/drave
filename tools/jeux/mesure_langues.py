#!/usr/bin/env python3
"""mesure_langues.py — 71 langues, le même sens.

Trois mesures, trois contrôles :
1. **couverture** : combien de concepts du lexique ont un libellé dans combien
   de langues (Wikidata, 35 concepts, 71 langues) ;
2. **corpus** : les surfaces multilingues du corpus (pièces, cartes, noms de
   jeux + coordonnées), lues au niveau 4, comparées à la RSN attendue ;
3. **invariance** : les variantes d'une même paire (le même coup dans toutes
   les langues) doivent donner la même empreinte.

Contrôles : **permutation** des libellés entre concepts (le sens doit
s'effondrer), **notation** (les 112 items de notation sont lus dans chacune des
71 langues : la notation ne dépend pas de la langue), et **détection** des noms
de jeux.
"""
from __future__ import annotations

import time
from collections import Counter, defaultdict

from .codecs import base as B
from .codecs import cartes as CC
from .codecs import dames as CD
from .codecs import echecs as CE
from .codecs import go as CG
from .codecs import morpion as CM
from .codecs import detecte_jeu, lit
from .corpus import construire_corpus
from .corpus_multilingue import construire_corpus_multilingue
from .lexique_multilingue import MULTI

_MODULES = (B, CE, CC, CG, CD, CM)


def _parse(item, langue: str | None = None):
    return lit(item.texte, jeu=item.jeu, niveau=4, contexte=item.contexte,
               langue=langue if langue is not None else item.langue)


def _corpus_multilingue() -> dict:
    corpus = construire_corpus_multilingue()
    bons = 0
    par_langue: dict[str, dict] = {}
    for it in corpus.items:
        lec = _parse(it)
        ok = bool(lec.ok and lec.rsn and lec.rsn.corps == it.attendu.corps)
        bons += int(ok)
        d = par_langue.setdefault(it.langue, {"items": 0, "bons": 0, "forts": 0, "forts_bons": 0})
        d["items"] += 1
        d["bons"] += int(ok)
        if it.paire.startswith(("ml-echecs", "ml-cartes")):
            d["forts"] += 1
            d["forts_bons"] += int(ok)
    fortes = [l for l, d in par_langue.items() if d["forts"]]
    return {
        "items": len(corpus.items),
        "bons": bons,
        "langues_avec_items": len(par_langue),
        "langues_avec_items_forts": len(fortes),
        "par_langue": par_langue,
        "minimum": min((d["bons"] / d["items"] for d in par_langue.values()), default=0.0),
        "maximum": max((d["bons"] / d["items"] for d in par_langue.values()), default=0.0),
    }


def _invariance() -> dict:
    corpus = construire_corpus_multilingue()
    groupes: dict[str, list[str]] = defaultdict(list)
    for it in corpus.items:
        lec = _parse(it)
        if lec.ok and lec.rsn:
            groupes[it.paire].append(lec.rsn.empreinte())
    total = len(groupes)
    identiques = sum(1 for v in groupes.values() if len(set(v)) == 1)
    return {"paires": total, "invariantes": identiques,
            "detail": {k: len(set(v)) for k, v in sorted(groupes.items())}}


def _permutation() -> dict:
    corpus = construire_corpus_multilingue()
    perm = MULTI.permute()
    sauve = {m: m.MULTI for m in _MODULES}
    bons = forts_bons = 0
    forts = 0
    try:
        for m in _MODULES:
            m.MULTI = perm
        for it in corpus.items:
            lec = _parse(it)
            ok = bool(lec.ok and lec.rsn and lec.rsn.corps == it.attendu.corps)
            bons += int(ok)
            if it.paire.startswith(("ml-echecs", "ml-cartes")):
                forts += 1
                forts_bons += int(ok)
    finally:
        for m, v in sauve.items():
            m.MULTI = v
    return {"items": len(corpus.items), "bons": bons,
            "forts": forts, "forts_bons": forts_bons}


def _detection() -> dict:
    jeux = ("morpion", "echecs", "dames", "go", "cartes", "whist")
    total = bons = 0
    par_jeu: dict[str, dict] = {}
    for concept in jeux:
        attendu = "cartes" if concept == "whist" else concept
        d = par_jeu.setdefault(attendu, {"total": 0, "bons": 0})
        for langue in MULTI.langues:
            formes = MULTI.formes(f"jeu.{concept}", langue)
            if not formes:
                continue
            total += 1
            d["total"] += 1
            trouve = detecte_jeu(formes[0])
            if trouve is not None and trouve[0] == attendu:
                bons += 1
                d["bons"] += 1
    return {"total": total, "bons": bons, "par_jeu": par_jeu}


def _langue_detectee() -> dict:
    corpus = construire_corpus_multilingue()
    exacts = 0
    for it in corpus.items:
        lec = lit(it.texte, jeu=it.jeu, niveau=4, contexte=it.contexte)
        if lec.langue == it.langue:
            exacts += 1
    return {"items": len(corpus.items), "exacts": exacts}


_NOTATION_CARTE = __import__("re").compile(r"^[2-9TJQKA][CDHS]$")


def _est_notation(it) -> bool:
    """La surface est-elle une notation, indépendante de la langue ?"""
    import re
    t = it.texte.strip()
    f = it.format
    if f in ("fen", "grille", "diagramme", "compact", "donne", "pgn", "sgf",
             "gtp", "uci", "algebrique"):
        return True
    if f == "san":
        return bool(re.fullmatch(r"(?:O-O(?:-O)?|[KQRBNCDFT]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?)", t))
    if f == "numerique":
        return bool(re.fullmatch(r"[a-h]?[1-9][0-9]?(?:x[a-h]?[1-9][0-9]?)*(?:[-][1-9][0-9]?)?", t))
    if f == "cellule":
        return bool(re.fullmatch(r"[A-Ca-c][1-3]|\(\d,\d\)|\d \d", t))
    if f == "carte":
        return bool(_NOTATION_CARTE.fullmatch(t))
    if f == "liste":
        return all(_NOTATION_CARTE.fullmatch(x) for x in t.split())
    return False


def _notation(rapide: bool) -> dict:
    corpus = construire_corpus()
    items = [it for it in corpus.items if _est_notation(it)]
    langues = MULTI.langues if not rapide else MULTI.langues[:12]
    parses = 0
    bons = 0
    for langue in langues:
        for it in items:
            lec = lit(it.texte, jeu=it.jeu, niveau=4, contexte=it.contexte,
                      langue=langue)
            parses += 1
            if lec.ok and lec.rsn and lec.rsn.corps == it.attendu.corps:
                bons += 1
    return {"items": len(items), "langues": len(langues),
            "parses": parses, "bons": bons}


def _couverture() -> dict:
    cov = MULTI.couverture()
    cov["pieces"] = {k: len(MULTI.langues_du_concept(f"echecs.piece.{k}"))
                     for k in "KQRBNP"}
    cov["rangs"] = {k: len(MULTI.langues_du_concept(f"cartes.rang.{k}"))
                    for k in (14, 13, 12, 11)}
    cov["couleurs"] = {k: len(MULTI.langues_du_concept(f"cartes.couleur.{k}"))
                       for k in "CDHS"}
    cov["jeux"] = {k: len(MULTI.langues_du_concept(f"jeu.{k}"))
                   for k in ("morpion", "echecs", "dames", "go", "cartes", "whist")}
    return cov


def mesure_langues(rapide: bool = True) -> dict:
    t0 = time.perf_counter()
    couverture = _couverture()
    corpus = _corpus_multilingue()
    invariance = _invariance()
    permutation = _permutation()
    detection = _detection()
    langue = _langue_detectee()
    notation = _notation(rapide)
    return {
        "couverture": couverture,
        "corpus": corpus,
        "invariance": invariance,
        "permutation": permutation,
        "detection": detection,
        "langue_detectee": langue,
        "notation": notation,
        "duree_s": round(time.perf_counter() - t0, 3),
    }


if __name__ == "__main__":
    import argparse
    import json
    ap = argparse.ArgumentParser()
    ap.add_argument("--complet", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    if __name__ == "__main__":
        resultat = (mesure_langues if "mesure_langues" == "mesure_langues" else mesure_maitres)(
            rapide=not args.complet)
    if args.json:
        import pathlib
        pathlib.Path(args.json).write_text(
            json.dumps(resultat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(resultat, ensure_ascii=False, indent=1))

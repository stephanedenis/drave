#!/usr/bin/env python3
"""collecter_wikisource.py — la diversité du corpus : des textes FR hors Wikipédia.

POURQUOI. Le palier 1 a 7,5 Go de Wikipédia et ~0,1 Go hors Wikipédia : l'écart de
**diversité** est le vrai manque (l'inventaire du 18/11). Wikisource FR porte des
textes du domaine public (romans, contes, essais) sous forme de wikitexte. Cet
outil collecte les pages d'une catégorie, nettoie le wikitexte (réutilise le
nettoyage du corpus) et concatène — un corpus de livres, traçable (ids de page et
de révision).

Usage :
  python3 tools/collecter_wikisource.py --categorie "Catégorie:Romans" --limite 300 \
      --sortie work/livres/livres.txt --json work/livres/collecte.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from tools.nettoyer_corpus import nettoyer_ligne  # noqa: E402

API = "https://fr.wikisource.org/w/api.php"
UA = {"User-Agent": "Drave/0.1 (corpus de recherche; contact: stephane)"}

CAT_ESPACE = re.compile(r"\[\[(Catégorie|Category|Fichier|File|Image)\s*:[^\]]*\]\]", re.I)
POEM = re.compile(r"</?(poem|div|span|p|center|small|big)[^>]*>", re.I)
TOC = re.compile(r"__[A-Z]+__")
PARAM = re.compile(r"^\s*\|.*$")
SECTIONS = re.compile(r"^=+[^=\n]+=+\s*$")


def api(params: dict) -> dict:
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json"})
    for essai in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            time.sleep(2 + essai * 3)
    return {}


def membres(categorie: str, limite: int) -> list[str]:
    titres, continu = [], None
    while len(titres) < limite:
        p = {"action": "query", "list": "categorymembers", "cmtitle": categorie,
             "cmlimit": "500", "cmnamespace": "0"}
        if continu:
            p["cmcontinue"] = continu
        d = api(p)
        for m in d.get("query", {}).get("categorymembers", []):
            titres.append(m["title"])
        continu = d.get("continue", {}).get("cmcontinue")
        if not continu:
            break
    return titres[:limite]


def sous_pages(titre: str, maxi: int = 400) -> list[str]:
    """Les chapitres d'un livre : les pages de préfixe « <titre>/ »."""
    out, continu = [], None
    while len(out) < maxi:
        p = {"action": "list", "list": "allpages", "apprefix": titre + "/", "aplimit": "500",
             "apnamespace": "0", "action2": "query"}
        p["action"] = "query"
        p["list"] = "allpages"
        p["apprefix"] = titre + "/"
        p["aplimit"] = "500"
        p["apnamespace"] = "0"
        if continu:
            p["apcontinue"] = continu
        d = api(p)
        for m in d.get("query", {}).get("allpages", []):
            out.append(m["title"])
        continu = d.get("continue", {}).get("apcontinue")
        if not continu:
            break
    return out[:maxi]


def textes(titres: list[str]) -> list[tuple[str, int, str]]:
    """(titre, revid, wikitexte) par lots de 50."""
    out = []
    for i in range(0, len(titres), 50):
        lot = titres[i:i + 50]
        d = api({"action": "query", "prop": "revisions", "rvprop": "ids|content",
                 "rvslots": "main", "titles": "|".join(lot)})
        for page in d.get("query", {}).get("pages", {}).values():
            if "revisions" not in page or "missing" in page:
                continue
            r = page["revisions"][0]
            contenu = r.get("slots", {}).get("main", {}).get("*", "")
            out.append((page["title"], r.get("revid", 0), contenu))
    return out


def nettoie_wikitexte(t: str) -> str:
    t = CAT_ESPACE.sub("", t)
    t = POEM.sub("", t)
    t = TOC.sub("", t)
    t = re.sub(r"<[^>]{1,80}>", "", t)
    for _ in range(6):
        t2 = re.sub(r"\{\{[^{}]*\}\}", "", t)
        if t2 == t:
            break
        t = t2
    lignes = []
    for ligne in t.splitlines():
        if SECTIONS.match(ligne) or PARAM.match(ligne):
            continue
        l = nettoyer_ligne(ligne)
        lignes.append(l if l is not None else "")
    return "\n".join(lignes)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--categorie", default="Catégorie:Romans")
    ap.add_argument("--limite", type=int, default=300)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--json", default="")
    ap.add_argument("--min-octets", type=int, default=20_000)
    a = ap.parse_args()
    livres_titres = membres(a.categorie, a.limite)
    # Un livre de Wikisource est un portail : le texte est dans ses sous-pages.
    titres = []
    for t in livres_titres:
        chapitres = sous_pages(t)
        titres.extend(chapitres if chapitres else [t])
    print(f"  {len(livres_titres)} livres, {len(titres)} pages de texte", flush=True)
    livres, gardes, rejetes = [], [], []
    for titre, revid, contenu in textes(titres):
        texte = nettoie_wikitexte(contenu)
        if len(texte) < a.min_octets:
            rejetes.append({"titre": titre, "octets": len(texte)})
            continue
        livres.append(texte)
        gardes.append({"titre": titre, "revid": revid, "octets": len(texte)})
    sortie = pathlib.Path(a.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text("\n\n".join(livres) + "\n", encoding="utf-8")
    res = {"categorie": a.categorie, "pages": len(titres), "gardes": len(gardes),
           "rejetes": len(rejetes), "octets": sortie.stat().st_size,
           "pages_gardees": gardes, "pages_rejetees": rejetes[:20]}
    print(json.dumps({k: v for k, v in res.items() if k != "pages_gardees"}, ensure_ascii=False, indent=1))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()

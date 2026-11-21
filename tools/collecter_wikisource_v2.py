#!/usr/bin/env python3
"""collecter_wikisource_v2.py — le corpus Wikisource par les **Pages**, pas les portails.

POURQUOI CE FICHIER (et pourquoi le premierCollecteur a échoué). Le 19/11, la collecte par les
pages de l'espace principal rendait 1 241 octets pour 40 pages : ces pages sont des **portails**
qui ne contiennent que des transclusions (`<pages index="…" />`), et un lecteur de wikitexte n'y
voit rien. La voie directe est l'espace **Page:** (ns 104) : chaque page de fac-similé porte le
texte corrigé, et l'espace **Livre:** (ns 112) donne le point d'entrée.

CE QUE LE SCRIPT FAIT, PAR LIVRE :
1. liste les `Page:<fichier>/<n>` du livre (allpages, ns 104, préfixe) ;
2. récupère leur wikitexte par lots de 50 titres (prop=revisions) ;
3. nettoie : blocs `<noinclude>`, modèles `{{…}}`, liens `[[…]]`, références, balises ;
4. ordonne les pages par numéro et écrit un fichier par livre + un manifeste.

Usage :
  python3 tools/collecter_wikisource_v2.py --livre "Livre:Voltaire - Candide, 1759.djvu" \
      --sortie data/wikisource --manifeste reports/corpus-wikisource.json
  python3 tools/collecter_wikisource_v2.py --autotest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://fr.wikisource.org/w/api.php"
UA = "DraveCorpus/1.0 (corpus de recherche, contact local)"


def http(params: dict, essais: int = 5) -> dict:
    """Un appel API, poli : 1 s entre les appels, et cinq essais sur 429/5xx."""
    params = dict(params, format="json", formatversion="2")
    url = API + "?" + urllib.parse.urlencode(params)
    for essai in range(essais):
        time.sleep(1.0)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            if essai == essais - 1:
                raise
            print(f"    (essai {essai + 1} : {type(e).__name__} — on attend)")
            time.sleep(5 * (essai + 1))
    raise RuntimeError("inatteignable")


def pages_du_livre(fichier: str) -> list[str]:
    titres, cont = [], None
    while True:
        p = {"action": "query", "list": "allpages", "apnamespace": "104",
             "apprefix": f"{fichier}/", "aplimit": "500"}
        if cont:
            p["apcontinue"] = cont
        d = http(p)
        titres += [x["title"] for x in d.get("query", {}).get("allpages", [])]
        cont = d.get("continue", {}).get("apcontinue")
        if not cont:
            break
    return titres


def numero(titre: str) -> int:
    m = re.search(r"/(\d+)$", titre)
    return int(m.group(1)) if m else 0


def contenu(titres: list[str]) -> dict[str, str]:
    sortie = {}
    for i in range(0, len(titres), 50):
        lot = titres[i:i + 50]
        d = http({"action": "query", "prop": "revisions", "rvprop": "content",
                  "rvslots": "main", "titles": "|".join(lot)})
        for p in d.get("query", {}).get("pages", []):
            if "revisions" in p:
                sortie[p["title"]] = p["revisions"][0]["slots"]["main"]["content"]
        time.sleep(0.2)
    return sortie


def nettoie(t: str) -> str:
    t = re.sub(r"<noinclude>.*?</noinclude>", " ", t, flags=re.S)
    t = re.sub(r"<noinclude\s*/>|<noinclude>|</noinclude>", " ", t)
    t = re.sub(r"<ref[^>]*>.*?</ref>", " ", t, flags=re.S)
    t = re.sub(r"<ref[^>]*/>", " ", t)
    for _ in range(6):                      # modèles imbriqués
        t = re.sub(r"\{\{[^{}]*\}\}", " ", t)
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[https?://[^\s\]]+\s*([^\]]*)\]", r"\1", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"'{2,}", "", t)
    t = re.sub(r"[ \t]+", " ", t)
    lignes = [l.strip() for l in t.splitlines()]
    gardees = []
    for l in lignes:
        if not l or re.fullmatch(r"[\d\sIVXLC]+", l):
            continue
        # résidus de modèles coupés par le découpage en pages (« page=4|thumb|upright=2.2| »)
        if re.match(r"^[a-zà-ÿ_]+=", l) or re.fullmatch(r"[\w=.\s|]+", l) and "|" in l:
            continue
        if re.fullmatch(r"(thumb|upright|center|left|right|page)(\|[\w=.\s]*)*\|?", l):
            continue
        gardees.append(l)
    return "\n".join(gardees)


def collecter(livre: str) -> dict:
    fichier = livre.split(":", 1)[1]
    titres = pages_du_livre(fichier)
    titres.sort(key=numero)
    contenus = contenu(titres)
    morceaux = [nettoie(contenus[t]) for t in titres if t in contenus]
    texte = "\n".join(m for m in morceaux if m)
    return {"livre": livre, "pages": len(titres), "pages_lues": len(contenus),
            "octets": len(texte.encode("utf-8")), "texte": texte}


def autotest() -> int:
    brut = ("<noinclude>En-tête</noinclude>Le {{petit|chat}} [[dort|s'endort]] "
            "sur le [[tapis]].<ref>note</ref> 12")
    sortie = nettoie(brut)
    if "chat" in sortie or "En-tête" in sortie or "note" in sortie or "[[".__len__() and "[[[" in sortie:
        print(f"  ❌ autotest : {sortie!r}")
        return 1
    if "dort" in sortie.replace("s'endort", "") or "s'endort" not in sortie:
        print(f"  ❌ autotest lien : {sortie!r}")
        return 1
    print(f"  ✅ autotest : {sortie!r}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--livre", action="append", default=[])
    ap.add_argument("--sortie", default="data/wikisource")
    ap.add_argument("--manifeste", default="reports/corpus-wikisource.json")
    ap.add_argument("--autotest", action="store_true")
    a = ap.parse_args()
    if a.autotest:
        sys.exit(autotest())
    dossier = pathlib.Path(a.sortie)
    dossier.mkdir(parents=True, exist_ok=True)
    manifeste = []
    for livre in a.livre:
        r = collecter(livre)
        slug = re.sub(r"[^a-z0-9]+", "-", r["livre"].lower())[:60].strip("-")
        f = dossier / f"{slug}.txt"
        f.write_text(r["texte"] + "\n", encoding="utf-8")
        manifeste.append({"livre": r["livre"], "fichier": str(f), "pages": r["pages"],
                          "octets": r["octets"],
                          "sha256": hashlib.sha256(r["texte"].encode()).hexdigest()})
        print(f"  {r['livre'][:60]:<60} {r['pages']:>4} p · {r['octets']:>9} o")
    total = sum(x["octets"] for x in manifeste)
    pathlib.Path(a.manifeste).write_text(json.dumps(
        {"source": "fr.wikisource.org (Page:, ns 104)", "livres": manifeste,
         "octets_total": total}, ensure_ascii=False, indent=1) + "\n")
    print(f"  total : {total} o · manifeste {a.manifeste}")


if __name__ == "__main__":
    main()

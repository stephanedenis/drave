#!/usr/bin/env python3
"""importer_udhr.py — LE CORPUS PARALLÈLE UDHR : 400+ langues, 30 articles alignés.

POURQUOI CE CORPUS. Pour tester une **couche commune** qui abstrait la langue, il faut **le même contenu dans
beaucoup de langues** ✓✓ : c'est la seule façon de séparer « ce qui est dit » de « la langue qui le dit » ✓. La
**Déclaration universelle des droits de l'homme** est le texte le plus traduit du monde ✓ — et le corpus Unicode
UDHR (Office of the High Commissioner for Human Rights ✓) la donne en **459 fichiers XML**, avec le **même
découpage en 30 articles** ✓✓.

CE QU'IL Y A DANS LE CORPUS, ET C'EST TOUT L'INTÉRÊT ✓ :
  · **404 langues** avec leurs métadonnées (iso639-3, nom, **écriture**, sens d'écriture ✓) ;
  · **32 langues ont PLUSIEURS variantes** ✗✓ (l'occitan en a **7** ✓, le roumain 3, le hunde 3, l'allemand 2,
    le chinois 2, le grec 2…) — ce sont des **traductions différentes de la même langue**, exactement ce qu'il
    faut pour mesurer un **style de traducteur** ✓✓ ;
  · **30 articles alignés** (le même numéro = le même sens ✓✓) — c'est notre unité parallèle ✓ ;
  · et **7 écritures** dominantes (latin 324, cyrillique 29, arabe 8, devanagari 7, et le reste ✓).

SORTIE (dans --sortie) :
  · `langues.jsonl`  : une ligne par fichier XML (fichier, clé, iso3, nom, écriture, sens, nb d'articles) ;
  · `articles.jsonl` : une ligne par (fichier, article) — le **texte normalisé** ✓.

⚠️ CE QUE L'IMPORT NE FAIT PAS ✗, et qui devra être dit à chaque mesure : il **ne vérifie pas** que l'article N
d'une langue dit bien la même chose que l'article N d'une autre ✓ — c'est la **structure** du corpus XML qui le
garantit ✓✓, mais une traduction peut **fusionner ou scinder** un article ✗✓ (on le verra au nombre d'articles
par langue ✓).

Usage :
  python3 tools/importer_udhr.py --racine /home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml --sortie data/udhr
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys, unicodedata
import xml.etree.ElementTree as ET

NS = "{http://www.unhchr.ch/udhr}"


def texte(el) -> str:
    """Le texte d'un élément, normalisé : NFC, espaces compactés ✓."""
    t = "".join(el.itertext())
    t = unicodedata.normalize("NFC", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default="/home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml")
    ap.add_argument("--sortie", default="data/udhr")
    a = ap.parse_args()
    racine = pathlib.Path(a.racine)
    sortie = pathlib.Path(a.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    if not racine.is_dir():
        print(f"  ✗ racine introuvable : {racine}", file=sys.stderr)
        return 2

    langues, articles = [], []
    for f in sorted(racine.glob("udhr_*.xml")):
        try:
            racine_el = ET.parse(f).getroot()
        except ET.ParseError as e:
            print(f"  ✗ {f.name} : XML illisible ({e})")
            continue
        attrs = racine_el.attrib
        cles = " ".join(f"{k}={v}" for k, v in attrs.items() if k in ("iso639-3", "xml:lang", "key", "n", "dir", "iso15924"))
        iso3 = attrs.get("iso639-3", "")
        nom = attrs.get("n", "")
        script = attrs.get("iso15924", "")
        sens = attrs.get("dir", "")
        titre = texte(racine_el.find(f"{NS}title")) if racine_el.find(f"{NS}title") is not None else ""
        # le préambule ✓ (ses paragraphes, dans l'ordre ✓)
        pre = racine_el.find(f"{NS}preamble")
        pre_txt = " ".join(texte(p) for p in pre.findall(f"{NS}para")) if pre is not None else ""
        arts = racine_el.findall(f"{NS}article")
        langues.append({
            "fichier": f.name, "iso3": iso3, "nom": nom, "script": script, "sens": sens,
            "titre": titre, "nb_articles": len(arts), "preambule_car": len(pre_txt),
            "attrs": cles,
        })
        if pre_txt:
            articles.append({"fichier": f.name, "iso3": iso3, "nom": nom, "script": script,
                             "art": 0, "titre": "Préambule", "texte": pre_txt})
        for art in arts:
            num = art.attrib.get("number", "")
            # ⚠️ ON NE PREND QUE LES <para>, PAS LE <title> ✗✗. `itertext()` ramassait le titre (« Article 2 »,
            # « Artículo 2 », « 第2条 » ✓) — donc le MÊME CHIFFRE dans toutes les langues ✓✗. Un retrieval
            # cross-lingue pouvait alors apparier les articles **par leur numéro**, pas par leur sens ✓✗ — et le
            # score aurait été parfait pour la mauvaise raison ✓✓. C'est le seizième piège de la nuit : le
            # numéro était dans le texte.
            # on prend TOUS les enfants SAUF le titre ✓ (les articles énumérés sont dans <orderedlist> ✓✗,
            # pas dans <para> ✓ — d'où la moitié des articles perdue au premier essai ✓✓).
            morceaux = ["".join(ch.itertext()) for ch in art if ch.tag != f"{NS}title"]
            t = re.sub(r"\s+", " ", " ".join(morceaux)).strip()
            if t:
                articles.append({"fichier": f.name, "iso3": iso3, "nom": nom, "script": script,
                                 "art": int(num) if num.isdigit() else num, "titre": "", "texte": t})

    (sortie / "langues.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in langues))
    (sortie / "articles.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in articles))

    import collections
    c = collections.Counter(x["nb_articles"] for x in langues)
    par_iso = collections.Counter(x["iso3"] for x in langues)
    total_car = sum(len(x["texte"]) for x in articles)
    print(f"  {len(langues)} langues/fichiers · {len(articles)} articles · {total_car/1048576:.2f} Mo de texte")
    print(f"  articles par langue : {dict(sorted(c.items()))}")
    print(f"  écritures : {dict(collections.Counter(x['script'] for x in langues).most_common())}")
    dbl = {k: v for k, v in par_iso.items() if v > 1}
    print(f"  langues à plusieurs variantes : {len(dbl)} → {dict(sorted(dbl.items(), key=lambda kv: -kv[1])[:12])}")
    avec_clic = sum(1 for x in langues if re.search(r"[^\x00-\x7F]", x["titre"]))
    print(f"  ✓ écrit dans {sortie}/langues.jsonl et {sortie}/articles.jsonl")
    return 0


raise SystemExit(main())

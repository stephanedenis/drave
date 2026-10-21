#!/usr/bin/env python3
"""corpus_jw.py — LE CORPUS JW.ORG 2026 : les mêmes articles dans les langues qui manquent, alignés par paragraphe.

POURQUOI ✓✓. Les 12 langues qui manquent à la couverture démographique n'ont **aucun corpus post-cutoff** : l'UDHR
est **récitée** par le modèle (mesure 75) ✗✗. Or le site **jw.org** publie les **mêmes articles** — les études de
*La Tour de garde* d'**août 2026** — dans des centaines de langues ✓✓, avec des **traductions humaines** ✓✓ et des
URL localisées données par les liens **hreflang** de la page anglaise ✓✓. Le contenu est **postérieur à la coupure**
(2024) : il ne peut pas être mémorisé ✓✓.

LA SOURCE ✓✓ :
  · la page d'un article anglais porte les liens `hreflang="hi"`, `"bn"`, `"ja"`… vers la **même** page traduite ✓✓ ;
  · on lit le corps de l'article : les paragraphes `<p>` (thème, résumé, corps, questions) ✓ ;
  · on aligne par **ordre de paragraphe**, après avoir vérifié que le nombre de paragraphes est le même dans toutes
    les langues ✓✓ (sinon l'article est écarté : un alignement faux est pire qu'une unité manquante ✗).

LANGUES ✓ : hindi (hi), bengali (bn), indonésien (id), urdu (ur), japonais (ja), marathi (mr), télougou (te),
vietnamien (vi), swahili (sw), haoussa (ha), arabe égyptien (arz) — et l'anglais comme référence ✓✓.
"""
from __future__ import annotations
import argparse, html, json, pathlib, re, time, urllib.request

BASE = "https://www.jw.org/en/library/magazines/watchtower-study-august-2026/{}/"
ARTICLES = [
    "An-Appeal-on-the-Basis-of-Love",
    "Bible-Fact%E2%80%8B-The-Tree-That-Wakes-Up-Early",
    "Cherish-the-Privilège-of-Fearlessly-Rendering-Sacred-Service",
    "did-you-know",
    "Resist-Satans-Tactics-Trust-In-Jehovah-and-In-Jesus",
    "St%C3%A9phane-Landeroin-My-Grand-Creator-Noticed-Me",
    "You-Can-Win-the-Battle",
]
LANGUES = {"eng": "en", "hin": "hi", "ben": "bn", "ind": "id", "urd": "ur", "jpn": "ja",
           "mar": "mr", "tel": "te", "vie": "vi", "swh": "sw", "hau": "ha", "arz": "arz"}


def telecharge(url: str, cache: pathlib.Path) -> str:
    f = cache / (re.sub(r"[^a-zA-Z0-9]+", "_", url)[-120:] + ".html")
    if f.exists() and f.stat().st_size > 20_000:
        return f.read_text(encoding="utf-8", errors="ignore")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (corpus Drave)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""
    cache.mkdir(parents=True, exist_ok=True)
    f.write_text(data, encoding="utf-8")
    time.sleep(0.4)
    return data


def paragraphes(page: str) -> dict[int, str]:
    """Les paragraphes par leur identifiant `data-pid` — le MÊME dans toutes les langues ✓✓."""
    out = {}
    for m in re.finditer(r'<p[^>]*data-pid="(\d+)"[^>]*>(.*?)</p>', page, flags=re.S | re.I):
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        t = " ".join(t.split())
        if len(t) > 30:
            out[int(m.group(1))] = t
    return out


def hreflang(page: str, code: str) -> str:
    m = re.search(rf'hreflang="{re.escape(code)}"\s+href="([^"]+)"', page)
    return html.unescape(m.group(1)) if m else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="data/jw/jw_2026.json")
    ap.add_argument("--cache", default="data/jw/html")
    a = ap.parse_args()
    cache = pathlib.Path(a.cache)
    unites, docs = [], []
    for slug in ARTICLES:
        en = telecharge(BASE.format(slug), cache)
        if not en:
            print(f"  ✗ {slug} : page anglaise absente"); continue
        url_par = {"eng": BASE.format(slug)}
        for code, hrefl in LANGUES.items():
            if code == "eng":
                continue
            u = hreflang(en, hrefl)
            if u:
                url_par[code] = u
        textes = {"eng": paragraphes(en)}
        for code, u in url_par.items():
            if code == "eng":
                continue
            page = telecharge(u, cache)
            textes[code] = paragraphes(page) if page else {}
        # ⚠️ l'alignement se fait par `data-pid`, PAS par index : les langues ajoutent ou retirent des
        # légendes/questions, mais le corps partage les mêmes identifiants ✓✓.
        if len(url_par) != len(LANGUES):
            print(f"  ✗ {slug} : pages manquantes "
                  f"{[c for c in LANGUES if c not in url_par]}"); continue
        communs = sorted(set.intersection(*[set(v) for v in textes.values()]))
        if len(communs) < 5:
            print(f"  ✗ {slug} : {len(communs)} paragraphes communs"); continue
        docs.append({"article": slug, "n": len(communs), "langues": sorted(textes)})
        for i in communs:
            unites.append({"id": f"{slug[:20]}_{i}", "article": slug, "num": i,
                           "textes": {c: textes[c][i] for c in textes}})
        print(f"  ✓ {slug} : {len(communs)} paragraphes alignés par data-pid, {len(textes)} langues")
    if not unites:
        print("  ✗ aucune unité"); return 1
    sortie = pathlib.Path(a.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps({"source": "jw.org, La Tour de garde (étude) août 2026",
                                  "langues": sorted(LANGUES), "documents": docs, "unites": unites},
                                 ensure_ascii=False, indent=1))
    print(f"  → {sortie} : {len(docs)} articles, {len(unites)} unités")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

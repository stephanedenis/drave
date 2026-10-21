#!/usr/bin/env python3
"""corpus_pidgin_bbc.py — LE CORPUS BBC PIDGIN : des centaines d'articles, par sujets paginés.

POURQUOI ✓✓. L'écriture du pidgin manque de **données** (mesures 90-91) : 7 contes et 24 articles ne suffisent pas
✗✗. La BBC Pidgin publie des **milliers** d'articles ; la page d'accueil donne les **sujets**, et chaque sujet se
**paginate** (`?page=2`, …) ✓✓. On collecte les articles, on extrait le corps (`<p>`), et on garde un corpus
**monolingue** pour l'adaptation ✓✓.
"""
from __future__ import annotations
import argparse, html, json, pathlib, re, time, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (corpus Drave)"}
BASE = "https://www.bbc.com"


def get(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "ignore")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="data/pidgin/mono_bbc.json")
    ap.add_argument("--max-pages", type=int, default=8)
    a = ap.parse_args()
    accueil = get(BASE + "/pidgin")
    sujets = sorted(set(re.findall(r"/pidgin/topics/([a-z0-9]+)", accueil)))
    print(f"  {len(sujets)} sujets")
    ids = set()
    for s in sujets:
        for p in range(1, a.max_pages + 1):
            try:
                h = get(f"{BASE}/pidgin/topics/{s}" + (f"?page={p}" if p > 1 else ""))
            except Exception:
                break
            trouves = set(re.findall(r"/pidgin/articles/([a-z0-9]+)", h))
            avant = len(ids); ids |= trouves
            if len(ids) == avant:
                break
            time.sleep(0.1)
    print(f"  {len(ids)} articles distincts")
    textes = []
    for i, aid in enumerate(sorted(ids)):
        try:
            h = get(f"{BASE}/pidgin/articles/{aid}")
        except Exception:
            continue
        ps = [" ".join(html.unescape(re.sub(r"<[^>]+>", "", x)).split())
              for x in re.findall(r"<p[^>]*>(.*?)</p>", h, flags=re.S)]
        ps = [x for x in ps if len(x) > 80]
        if ps:
            textes.append(" ".join(ps))
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(ids)} articles · {len(textes)} textes")
        time.sleep(0.15)
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(textes, ensure_ascii=False, indent=0))
    print(f"  {len(textes)} textes · {sum(len(t) for t in textes)} caractères → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

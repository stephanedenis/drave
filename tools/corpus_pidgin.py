#!/usr/bin/env python3
"""corpus_pidgin.py — LE CORPUS PIDGIN NIGÉRIAN : les contes d'African Storybook, anglais et pidgin côte à côte.

POURQUOI ✓✓. Le pidgin nigérian est la **seule** des 20 langues les plus parlées qui manquait à la couverture
(mesure 76) ✗✗ : c'est un créole surtout **oral**, sans corpus parallèle post-cutoff ✗✓. Or le site **Storybooks
Nigeria** (Global-ASP) publie **40 contes** d'African Storybook en **anglais et pidgin nigérian**, **page par page**
✓✓ : chaque page HTML porte les deux textes dans ses `div.level2-txt` ✓✓ — l'alignement est donc **structurel**
(même page, même numéro) ✓✓.

⚠️ CE QUE CE CORPUS N'EST PAS ✗ : ce ne sont pas des textes **post-cutoff** (les contes sont anciens et publics) ✗✗ ;
la contamination est possible, et il faudra la **tester** (un jeton rare inséré) avant de conclure ✓✓. Le registre
est **narratif/enfantin**, pas juridique ni presse ✓✓.
"""
from __future__ import annotations
import argparse, html, json, pathlib, re, time, urllib.request

BASE = "https://global-asp.github.io/storybooks-nigeria/stories/pcm/{}/"
INDEX = "https://global-asp.github.io/storybooks-nigeria/stories/pcm/"
MARQUEURS_PCM = {"na", "sef", "dey", "em", "oo", "wetin", "don", "abeg", "sabi", "shey", "make", "go", "fit"}
MARQUEURS_EN = {"the", "was", "his", "her", "he", "she", "and", "to", "of", "in", "it", "they", "that"}


def telecharge(url: str, cache: pathlib.Path) -> str:
    f = cache / (re.sub(r"[^a-zA-Z0-9]+", "_", url)[-100:] + ".html")
    if f.exists() and f.stat().st_size > 5_000:
        return f.read_text(encoding="utf-8", errors="ignore")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (corpus Drave)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""
    cache.mkdir(parents=True, exist_ok=True)
    f.write_text(data, encoding="utf-8")
    time.sleep(0.2)
    return data


def slots(page: str) -> list[str]:
    out = []
    for m in re.finditer(r'<div class="[^"]*level2-txt[^"]*"[^>]*>(.*?)</div>', page, flags=re.S):
        t = " ".join(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split())
        if t:
            out.append(t)
    return out


def langue(t: str) -> str:
    mots = set(re.findall(r"[a-z']+", t.lower()))
    pcm = len(mots & MARQUEURS_PCM); en = len(mots & MARQUEURS_EN)
    if pcm > en:
        return "pcm"
    if en > pcm:
        return "eng"
    return "?"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="data/pidgin/pidgin.json")
    ap.add_argument("--cache", default="data/pidgin/html")
    a = ap.parse_args()
    cache = pathlib.Path(a.cache)
    accueil = telecharge(INDEX, cache)
    ids = sorted(set(re.findall(r"/storybooks-nigeria/stories/pcm/(\d+)/", accueil)))
    print(f"  {len(ids)} contes en pidgin")
    unites, docs = [], []
    for sid in ids:
        page = telecharge(BASE.format(sid), cache)
        s = slots(page)
        # les slots vont par page (3 par page) ; on apparie le premier anglais et le premier pidgin
        pages = []
        # ⚠️ sur la page PIDGIN, le triplet est [pidgin, anglais, pidgin] ✓✓ : l'appariement est
        # POSITIONNEL (0, 1), pas linguistique — les phrases courtes trompent le détecteur ✗✓.
        for i in range(0, len(s) - 2, 3):
            triplet = s[i:i + 3]
            if triplet[0] and triplet[1]:
                pages.append((triplet[1], triplet[0]))
        if len(pages) < 3:
            print(f"  ✗ {sid} : {len(pages)} pages appariées"); continue
        docs.append({"histoire": sid, "pages": len(pages)})
        for j, (eng, pcm) in enumerate(pages):
            unites.append({"id": f"{sid}_{j}", "histoire": sid, "page": j, "textes": {"eng": eng, "pcm": pcm}})
        print(f"  ✓ {sid} : {len(pages)} pages")
    if not unites:
        print("  ✗ aucune unité"); return 1
    ratios = sorted(len(u["textes"]["pcm"]) / max(1, len(u["textes"]["eng"])) for u in unites)
    sortie = pathlib.Path(a.sortie); sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps({"source": "African Storybook / Storybooks Nigeria (Global-ASP)",
                                  "langues": ["eng", "pcm"], "documents": docs, "unites": unites},
                                 ensure_ascii=False, indent=1))
    print(f"  longueur pcm/eng : médiane {ratios[len(ratios) // 2]:.2f} · min {ratios[0]:.2f} · max {ratios[-1]:.2f}")
    print(f"  → {sortie} : {len(docs)} contes, {len(unites)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

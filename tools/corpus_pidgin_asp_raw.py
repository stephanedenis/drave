#!/usr/bin/env python3
"""corpus_pidgin_asp_raw.py — les contes pidgin-anglais de la BASE BRUTE African Storybook.

POURQUOI ✓✓. L'African Storybook a **beaucoup plus** de traductions pidgin que les 7 du site Global-ASP ✓✓. La
base brute `asp-raw-db` (12 085 fichiers, un par version de conte) donne, pour chaque conte, ses **illustrations**
(identiques dans toutes les langues) et ses **pages** P1..Pn ✓✓ : on apparie l'anglais et le pidgin **par les
illustrations**, page par page ✓✓. C'est le registre des contes — le seul qui aide (mesures 96-104) ✓✓.
"""
from __future__ import annotations
import glob, json, os, re, sys
from collections import defaultdict

RACINE = "/tmp/asp_raw/asp-raw-db-master/data"


def parse(f: str) -> dict:
    d = {"pages": {}, "images": []}
    section = None
    for ligne in open(f, encoding="utf-8", errors="ignore"):
        l = ligne.rstrip("\n")
        m = re.match(r"^(url|id|title|author|artist|lang|level|lic|thumb|desc):\s*(.*)$", l)
        if m:
            d[m.group(1)] = m.group(2).strip(); continue
        if l.strip().lower().startswith("page_text"):
            section = "pages"; continue
        if l.strip().lower().startswith("images"):
            section = "images"; continue
        if section == "pages":
            mm = re.match(r"^P(\d+)\s+(.*)$", l)
            if mm:
                d["pages"][int(mm.group(1))] = mm.group(2).strip()
        elif section == "images" and l.strip():
            d["images"].append(l.strip())
    return d


def signature(d: dict) -> str:
    return "|".join(d["images"][:3]) if d["images"] else ""


def main() -> int:
    fichiers = glob.glob(os.path.join(RACINE, "*.txt"))
    print(f"  {len(fichiers)} fichiers ASP bruts")
    par_image = defaultdict(list); pcm = []
    for f in fichiers:
        d = parse(f)
        lang = (d.get("lang") or "").lower()
        if "pidgin" in lang or "naija" in lang:
            pcm.append(d)
        sig = signature(d)
        if sig:
            par_image[sig].append(d)
    print(f"  {len(pcm)} contes pidgin · {len(par_image)} signatures d'illustrations")
    paires, contes = [], []
    for d in pcm:
        sig = signature(d)
        anglais = [x for x in par_image.get(sig, []) if (x.get("lang") or "").lower() == "english"]
        if not anglais:
            continue
        en = anglais[0]
        n = 0
        for num in sorted(set(d["pages"]) & set(en["pages"])):
            a, b = en["pages"][num], d["pages"][num]
            if len(a) > 15 and len(b) > 15 and 0.3 < len(b) / max(1, len(a)) < 3.5:
                paires.append({"en": a, "pcm": b, "conte": d.get("title", ""), "id": d.get("id", ""), "page": num})
                n += 1
        if n:
            contes.append({"id": d.get("id", ""), "titre": d.get("title", ""), "pages": n})
    json.dump({"paires": paires, "contes": contes}, open("data/pidgin/asp_raw.json", "w"), ensure_ascii=False, indent=0)
    print(f"  {len(contes)} contes appariés · {len(paires)} paires → data/pidgin/asp_raw.json")
    for c in contes[:8]:
        print("   ", c)
    for x in paires[:2]:
        print("   EN :", x["en"][:100]); print("   PCM:", x["pcm"][:100])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

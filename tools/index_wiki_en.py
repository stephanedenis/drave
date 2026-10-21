#!/usr/bin/env python3
"""index_wiki_en.py — l'index des titres anglais du corpus local Nipada (28 126 morceaux, 34 Go).

POURQUOI ✓✓. Pour apparier la Wikipédia pidgin (dump local) avec l'anglais, il faut retrouver les articles
anglais **par titre** dans les morceaux locaux — sans API ✓✓. L'index JSON complet est trop lent (4 h) : on
extrait les titres par **regex** (I/O pur, pas de parse JSON), et on garde le fichier pour retrouver le texte ✓✓.
On compte les **doublons** (la déduplication demandée) ✓✓.
"""
from __future__ import annotations
import glob, json, os, re
from collections import Counter

racine = "/home/stephane/Data13TB/stephane/nipada/wikipedia_decompressed/en"
sortie = "data/pidgin/en_titles.tsv"
fichiers = sorted(glob.glob(os.path.join(racine, "wiki_en_chunk_*.json")))
print(f"{len(fichiers)} morceaux", flush=True)
motif = re.compile(r'"title":\s*"((?:[^"\\]|\\.)*)"')
vus = Counter(); n = 0
with open(sortie, "w", encoding="utf-8") as w:
    for i, f in enumerate(fichiers):
        fic = os.path.basename(f)
        with open(f, encoding="utf-8", errors="ignore") as r:
            for ligne in r:
                for m in motif.finditer(ligne):
                    try:
                        t = json.loads('"' + m.group(1) + '"')  # décoder \u00e9, \", etc.
                    except Exception:
                        t = m.group(1)
                    w.write(f"{t}\t{fic}\n"); vus[t] += 1; n += 1
        if i % 2000 == 0:
            print(f"  {i}/{len(fichiers)} · {n} titres", flush=True)
doublons = {t: c for t, c in vus.items() if c > 1}
print(f"TOTAL {n} titres · {len(vus)} uniques · {len(doublons)} doublons", flush=True)
json.dump({"titres": n, "uniques": len(vus), "doublons": doublons},
          open("data/pidgin/en_index_doublons.json", "w"), ensure_ascii=False)

#!/usr/bin/env python3
"""agrege_production.py — assemble `reports/n2-production-fenetre.json`."""
from __future__ import annotations
import argparse, json, pathlib

WORK = pathlib.Path("work/n2ac")
SOURCES = {
    "temoin_n2ac": "eval-mix60.json",
    "temoin_200k": "eval-mix200.json",
    "prod_512": "eval-mix512-15k.json",
    "prod_1024": "eval-mix1024-7.5k.json",
    "prod_2048": "eval-mix2048-3.75k.json",
    "prod_1024_30k": "eval-mix1024-30k.json",
    "prod_2048_15k": "eval-mix2048-15k.json",
    "prod_zero_512": "eval-mix512-zero-15k.json",
    "meme_texte_512": "queue-mix512.json",
    "meme_texte_1024": "queue-mix1024.json",
    "meme_texte_2048": "queue-mix2048.json",
    "miroir_512": "miroir-mix512-15k.json",
}
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="reports/n2-production-fenetre.json")
    a = ap.parse_args()
    out = {k: json.loads((WORK / v).read_text(encoding="utf-8"))
           for k, v in SOURCES.items() if (WORK / v).exists()}
    out["dispositif"] = {
        "corpus": "data/wiki_mix/propre/train.txt (1,02 Go) + canal",
        "recette": "RoPE, 34,3 M (384/512), lot 8, lr 3e-4, graine 1, seq = fenêtre, init mix-60k (N2.ac)",
        "temoin": "mix-60k = N2.ac (60 000 pas à 128) ; mix-200k (200 000 pas à 128)",
        "controles": ["permutation des octets", "même texte 256/512/1 024/2 000",
                      "miroir de copie", "affinage vs depuis zéro"],
    }
    p = pathlib.Path(a.sortie)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  {p} · {len(out)-1} source(s)")
if __name__ == "__main__":
    main()

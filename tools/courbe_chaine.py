#!/usr/bin/env python3
"""courbe_chaine.py — la table d'une chaîne d'entraînement (tranches + bancs).

POURQUOI. La nuit du 18/11 entraîne deux 150 M (corpus v1 et v2) en tranches de
10 000 pas, avec un banc après chacune. Lire 24 `.pt.json` et 24 JSON de banc à la
main, c'est se tromper : cet outil produit la table (PPL, précision, trois régimes
du banc) et le JSON de la courbe, tranche par tranche, en tolérant une chaîne
partielle (les tranches pas encore finies sont marquées `None`).

Usage :
  python3 tools/courbe_chaine.py --prefixe v2 --prefixe v1 --n 12 \
      --sortie reports/courbe-150m.json
"""
from __future__ import annotations

import argparse
import json
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent


def tranche(prefixe: str, i: int) -> dict | None:
    meta = RACINE / f"work/n4/{prefixe}{i}.pt.json"
    if not meta.exists():
        return None
    m = json.loads(meta.read_text())
    d = {"pas": m.get("pas"), "ppl_val": m.get("ppl_val"),
         "precision_main": m.get("precision_main"), "duree_s": m.get("duree_s")}
    wt = RACINE / f"reports/ppl-wikitext2-{prefixe}{i}.json"
    if wt.exists():
        d["wikitext2"] = json.loads(wt.read_text()).get("ppl")
    banc = RACINE / f"reports/banc-generation-{prefixe}{i}.json"
    if banc.exists():
        b = json.loads(banc.read_text())
        for nom, r in b.get("reglages", {}).items():
            d[nom] = {"mots_valides": r["mots_valides"], "repetition": r["repetition"],
                      "distinct_2": r["distinct_2"], "echo": r["echo"]}
    return d


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefixe", action="append", required=True)
    ap.add_argument("--n", type=int, default=12)
    # pas de fichier par défaut : une courbe p1/p2 a déjà écrasé courbe-150m.json
    ap.add_argument("--sortie", default="")
    a = ap.parse_args()
    doc = {"schema": "drave.courbe-chaine", "version": 1, "n": a.n, "chaines": {}}
    for p in a.prefixe:
        doc["chaines"][p] = [tranche(p, i) for i in range(1, a.n + 1)]
    sortie = None
    if a.sortie:
        sortie = pathlib.Path(a.sortie)
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")

    # La table lisible : une ligne par tranche finie.
    for p in a.prefixe:
        print(f"\n== {p}")
        print("  tranche   pas    PPL val   wikitext2   précision   greedy (val/rép)   top-40 (val/rép)   top-20 (val/rép)")
        for i, t in enumerate(doc["chaines"][p], 1):
            if t is None:
                continue
            g = t.get("greedy", {})
            t40 = t.get("top40_0.8", {})
            t20 = t.get("top20_0.5", {})
            wt2 = t.get("wikitext2")
            print(f"  {i:>7} {t['pas']:>6} {t['ppl_val']:>9.4f} "
                  f"{(f'{wt2:.4f}' if wt2 else '—'):>9} {t['precision_main']:>10.4f}   "
                  f"{g.get('mots_valides', 0):.3f}/{g.get('repetition', 0):<4.1f}      "
                  f"{t40.get('mots_valides', 0):.3f}/{t40.get('repetition', 0):<4.1f}      "
                  f"{t20.get('mots_valides', 0):.3f}/{t20.get('repetition', 0):<4.1f}")
    if sortie:
        print(f"\n  écrit : {sortie}")


if __name__ == "__main__":
    main()

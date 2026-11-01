#!/usr/bin/env python3
"""catalogue_corpus.py — la table des corpus Wikipédia, depuis leurs manifestes.

POURQUOI CE FICHIER. Chaque corpus de langue a son manifeste `reports/corpus-wiki-<langue>.json`.
Ce script les lit et rend une **table markdown** et des **totaux**, pour que la fiche et les
agents n'aient qu'une source : les manifestes. Il ne lit pas les données (elles sont gitignorées),
seulement les chiffres et les empreintes.

Usage : python3 tools/catalogue_corpus.py [--sortie table.md]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
ORDRE = ["fr", "en", "de", "es", "ru", "it", "ja", "zh", "pt", "ar"]


def humain(octets: int) -> str:
    for unite in ("o", "Ko", "Mo", "Go", "To"):
        if octets < 1000:
            return f"{octets:.0f} {unite}"
        octets /= 1000
    return f"{octets:.1f} Po"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sortie", type=pathlib.Path)
    args = ap.parse_args()
    manifestes = {}
    for p in sorted((RACINE / "reports").glob("corpus-wiki-*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if "articles_gardes" in d:
            manifestes[d.get("langue", p.stem.split("-")[-1])] = (d, p)
    lignes = []
    total_a = total_c = total_o = total_m = 0
    for langue in ORDRE:
        if langue not in manifestes:
            continue
        d, p = manifestes[langue]
        octets = sum(d.get("octets", {}).values())
        total_a += d["articles_gardes"]
        total_c += d["caracteres_gardes"]
        total_o += octets
        if langue in ("ja", "zh"):
            mots = "— (caractères)"
        else:
            mots = f"{d['mots_estimes'] / 1e6:.0f} M"
            total_m += d["mots_estimes"]
        lignes.append(
            f"| **{langue}** | {d['articles_gardes']:,} | {d['caracteres_gardes'] / 1e9:.2f} G "
            f"| {mots} | {d['octets']['train'] / 1e9:.2f} Go / "
            f"{d['octets']['val'] / 1e6:.0f} Mo / {d['octets']['test'] / 1e6:.0f} Mo "
            f"| [`{p.name}`]({p.name}) |".replace(",", " "))
    entete = ("| langue | articles | caractères | mots (est.) | train / val / test | manifeste |\n"
              "|---|---:|---:|---:|---:|---|")
    table = entete + "\n" + "\n".join(lignes)
    total = (f"\n\n**Total : {total_a:,} articles · {total_c / 1e9:.2f} G caractères · "
             f"{total_m / 1e6:.0f} M mots (langues à espaces ; ja/zh comptés en caractères) · "
             f"{total_o / 1e9:.1f} Go**".replace(",", " "))
    print(table + total)
    if args.sortie:
        args.sortie.write_text(table + total + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""catalogue_corpus.py — la table des corpus Wikipédia, depuis leurs manifestes.

POURQUOI CE FICHIER. Chaque corpus de langue a son manifeste `reports/corpus-wiki-<langue>.json`.
Ce script les lit et rend une **table markdown** et des **totaux**, pour que la fiche et les
agents n'aient qu'une source : les manifestes. Il ne lit pas les données (elles sont gitignorées),
seulement les chiffres et les empreintes.

Usage : python3 tools/catalogue_corpus.py [--sortie table.md] [--texte]
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
    ap.add_argument("--texte", action="store_true",
                    help="le catalogue du texte intégral (les manifestes -texte.json)")
    args = ap.parse_args()
    manifestes = {}
    for p in sorted((RACINE / "reports").glob("corpus-wiki-*.json")):
        if not p.name.endswith("-texte.json") or "pilote" in p.name:
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        if "articles_gardes" in d:
            manifestes[d.get("langue", p.stem.split("-")[-1])] = (d, p)
    if not manifestes:
        print("aucun manifeste -texte.json", file=sys.stderr)
        return 1
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
        c = RACINE / "reports" / f"corpus-wiki-{langue}-texte-contamination.json"
        fuite = "—"
        ev = "—"
        if c.exists():
            dc = json.loads(c.read_text(encoding="utf-8"))
            taux = dc.get("doublons_entre_splits_troncon", {}).get("par_split", {})
            fuite = f"{max((v['taux'] for v in taux.values()), default=0) * 100:.1f} %"
            trouvees = [e for e in dc.get("recouvrement_eval", []) if e.get("trouvees")]
            ev = ", ".join(f"{e['fichier'].split('-')[-1].replace('.txt','')} {e['trouvees']}/{e['fenetres']}"
                           for e in trouvees) if trouvees else "0"
        lignes.append(
            f"| **{langue}** | {d['articles_gardes']:,} | {d['caracteres_gardes'] / 1e9:.2f} G "
            f"| {mots} | {octets / 1e9:.2f} Go | {fuite} | {ev} "
            f"| [`{p.name}`]({p.name}) |".replace(",", " "))
    entete = ("| langue | articles | caractères | mots (est.) | octets | fuite 8 Ko | éval (trouvées) | manifeste |\n"
              "|---|---:|---:|---:|---:|---:|---|---|")
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

#!/usr/bin/env python3
"""banc_grammaticalite.py — le natif jugé par le bloc linguistique de Drave.

POURQUOI. Le banc de génération dit que le natif produit des mots mais pas des
phrases. Ce banc le mesure **avec notre propre analyseur** : sur les générations
du natif (et le contrôle aléatoire), il compte les **GV** (un texte sans verbe
n'est pas une phrase), les **GN**, la part des **classes fermées** (le ciment :
DET, PREP, CONJ, PRON), et les **attachements** réussis.

LA MESURE. Pour chaque génération : `gv`, `gn`, `mots`, `ciment` (la fraction
des mots en classe fermée), `attaches` (les segments avec une cible / les
segments). Le **contrôle** : les générations du modèle aléatoire, traitées
par le même analyseur. Si le natif a une syntaxe, il doit avoir **plus de GV**
et **plus d'attachements** que le hasard ; sinon, le banc dit qu'il n'en a pas.

Usage :
  python3 tools/banc_grammaticalite.py --entree reports/banc-generation.json \
      --controle reports/banc-generation-aleatoire.json --sortie reports/banc-grammaticalite.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from tools import bloc_linguistique as bl  # noqa: E402

FERMEES = {"DET", "PREP", "CONJ", "PRON", "AUX", "PONCT"}


def mesurer(texte: str, analyseur) -> dict:
    a = analyseur.analyser(texte, "fr")
    pos = [e for e in a.etiquettes if e.niveau == "pos"]
    gv = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GV"]
    gn = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GN"]
    synt = [e for e in a.etiquettes if e.niveau == "syntagme"]
    attaches = sum(1 for e in synt if (e.meta.get("attachement") or {}).get("cible"))
    ciment = sum(1 for e in pos if e.type in FERMEES)
    return {"mots": len(pos), "gv": len(gv), "gn": len(gn),
            "ciment": round(ciment / max(1, len(pos)), 4),
            "attaches": round(attaches / max(1, len(synt)), 4)}


def agreger(lignes: list[dict], analyseur) -> dict:
    ms = [mesurer(l["texte"], analyseur) for l in lignes]
    n = len(ms)
    return {"textes": n,
            "gv_moyen": round(sum(m["gv"] for m in ms) / n, 2),
            "gn_moyen": round(sum(m["gn"] for m in ms) / n, 2),
            "mots_moyen": round(sum(m["mots"] for m in ms) / n, 1),
            "ciment": round(sum(m["ciment"] for m in ms) / n, 4),
            "attaches": round(sum(m["attaches"] for m in ms) / n, 4),
            "sans_verbe": round(sum(1 for m in ms if m["gv"] == 0) / n, 4)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entree", default="reports/banc-generation.json")
    ap.add_argument("--controle", default="reports/banc-generation-aleatoire.json")
    ap.add_argument("--sortie", default="reports/banc-grammaticalite.json")
    a = ap.parse_args()
    analyseur = bl.Heuristique()
    sortie = {}
    for etiquette, chemin in (("natif", a.entree), ("aleatoire", a.controle)):
        if not pathlib.Path(chemin).exists():
            continue
        d = json.loads(pathlib.Path(chemin).read_text(encoding="utf-8"))
        sortie[etiquette] = {nom: agreger(r["lignes"], analyseur)
                             for nom, r in d["reglages"].items()}
    pathlib.Path(a.sortie).write_text(json.dumps(sortie, ensure_ascii=False, indent=1) + "\n",
                                      encoding="utf-8")
    for et, reglages in sortie.items():
        for nom, r in reglages.items():
            print(f"{et:9s} {nom:10s} gv={r['gv_moyen']:.2f} gn={r['gn_moyen']:.2f} "
                  f"mots={r['mots_moyen']:.1f} ciment={r['ciment']:.3f} "
                  f"attaches={r['attaches']:.3f} sans_verbe={r['sans_verbe']:.2f}")


if __name__ == "__main__":
    main()

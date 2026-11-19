#!/usr/bin/env python3
"""reflow_corpus.py — recoller les paragraphes du plein texte (défragmentation).

POURQUOI. Le 19/11, la mesure a montré que le corpus v2 fait **108,8 octets par ligne**
contre **410,2** pour v1 : le plein texte est fragmenté (titres, listes, lignes courtes),
et le modèle de bytes apprend une distribution de sauts de ligne quatre fois plus dense.
Le nettoyage ([[nettoyer_corpus.py]]) retire le balisage mais ne recolle rien ; cet outil
recolle les lignes consécutives d'un paragraphe en **une seule ligne**, et garde une ligne
vide entre paragraphes. C'est le test de l'hypothèse « structure » : à contenu égal, la
maille de v1.

Usage :
  python3 tools/reflow_corpus.py --entree work/clean/train.txt --sortie work/reflow/train.txt
  python3 tools/reflow_corpus.py --autotest
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys


def autotest() -> int:
    entree = "Titre\nLigne une\nLigne deux.\n\nLigne trois\n"
    attendu = "Titre Ligne une Ligne deux.\n\nLigne trois\n"
    obtenu = "".join(un_paragraphe(entree.splitlines(keepends=True)))
    if obtenu != attendu:
        print(f"  ❌ reflow : {obtenu!r} ≠ {attendu!r}")
        return 1
    print("  ✅ autotest : deux paragraphes recollés, la ligne vide sépare")
    return 0


def un_paragraphe(lignes):
    """Regroupe les lignes non vides consécutives en une seule ligne."""
    bloc: list[str] = []

    def vider():
        if bloc:
            yield " ".join(m.strip() for m in bloc if m.strip()) + "\n"
            bloc.clear()

    for ligne in lignes:
        if ligne.strip():
            bloc.append(ligne.rstrip("\n"))
        else:
            yield from vider()
            yield "\n"
    yield from vider()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entree", default="")
    ap.add_argument("--sortie", default="")
    ap.add_argument("--json", default="")
    ap.add_argument("--autotest", action="store_true")
    a = ap.parse_args()
    if a.autotest:
        return autotest()
    if not a.entree or not a.sortie:
        ap.error("--entree et --sortie sont requis (sauf --autotest)")
    src = pathlib.Path(a.entree)
    dst = pathlib.Path(a.sortie)
    dst.parent.mkdir(parents=True, exist_ok=True)
    lignes_in = lignes_out = octets_in = octets_out = 0
    with src.open("r", encoding="utf-8", errors="replace") as f, dst.open("w", encoding="utf-8") as g:
        for ligne in un_paragraphe(f):
            g.write(ligne)
            if ligne.strip():
                lignes_out += 1
                octets_out += len(ligne.encode("utf-8"))
            else:
                octets_out += 1
    octets_in = src.stat().st_size
    res = {"entree": str(src), "sortie": str(dst), "octets_in": octets_in,
           "octets_out": octets_out, "lignes_out": lignes_out,
           "octets_par_ligne": round(octets_out / max(1, lignes_out), 1)}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

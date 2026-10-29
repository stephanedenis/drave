#!/usr/bin/env python3
"""corpus_gele.py — le corpus des bancs, figé et vérifiable.

POURQUOI CE FICHIER EXISTE. Les bancs de R0.3 sont adossés à des documents **vivants** : quand
une session réécrit `continuite.md`, le gold d'une question ne résout plus et le banc ment
(arrivé le 29/10 : une question perdue, puis deux). Un banc qui bouge avec la documentation ne
mesure pas une progression, il mesure le dernier commit.

Le gel : chaque document du corpus est **copié** dans `tools/tests/documents/corpus/`, avec son
sha256 et sa source. Les constructeurs de bancs lisent la copie ; la source peut évoluer sans
casser le banc. `--verifie` recalcule les empreintes : une copie modifiée est signalée.

Usage :
  python3 tools/corpus_gele.py --fige      # copie et écrit le manifeste
  python3 tools/corpus_gele.py --verifie   # recalcule les sha256
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
CORPUS = RACINE / "tools/tests/documents/corpus"
MANIFESTE = CORPUS / "manifeste.json"


def sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def sources_actuelles() -> list[tuple[str, str]]:
    """La liste (source, type) : le manifeste s'il existe, sinon l'union des deux bancs."""
    if MANIFESTE.exists():
        m = json.loads(MANIFESTE.read_text(encoding="utf-8"))
        return [(e["source"], e["type"]) for e in m["documents"]]
    vus: dict[str, str] = {}
    for nom in ("bench-complet.json", "bench-durci.json"):
        f = RACINE / "tools/tests/documents" / nom
        if not f.exists():
            continue
        for d in json.loads(f.read_text(encoding="utf-8"))["documents"]:
            if not d["chemin"].startswith("tools/tests/documents/corpus/"):
                vus[d["chemin"]] = d["type"]
    return sorted(vus.items())


def fige() -> int:
    entrees = []
    for source, type_ in sources_actuelles():
        original = RACINE / source
        if not original.exists():
            print(f"  ⚠️ source absente : {source}")
            continue
        copie = CORPUS / type_ / original.name
        copie.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original, copie)
        entrees.append({"source": source,
                        "copie": str(copie.relative_to(RACINE)),
                        "type": type_, "octets": copie.stat().st_size,
                        "sha256": sha256(copie)})
    MANIFESTE.write_text(json.dumps(
        {"version": 1, "date": "2026-10-30",
         "note": "Corpus gelé des bancs R0.3 : la source peut évoluer, la copie est le banc.",
         "documents": entrees}, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(e["octets"] for e in entrees)
    print(f"{len(entrees)} documents figés · {total} octets → {MANIFESTE.relative_to(RACINE)}")
    return 0


def verifie() -> int:
    if not MANIFESTE.exists():
        print("❌ manifeste absent : lancer --fige")
        return 1
    m = json.loads(MANIFESTE.read_text(encoding="utf-8"))
    problemes = 0
    for e in m["documents"]:
        copie = RACINE / e["copie"]
        if not copie.exists():
            print(f"❌ copie absente : {e['copie']}")
            problemes += 1
        elif sha256(copie) != e["sha256"]:
            print(f"❌ empreinte changée : {e['copie']}")
            problemes += 1
    print(f"{len(m['documents'])} documents · {problemes} problème(s)")
    return 0 if problemes == 0 else 1


def chemin_fige(source: str) -> pathlib.Path:
    """Le chemin de la copie pour une source donnée (ou la source si elle n'est pas gelée)."""
    if not MANIFESTE.exists():
        return RACINE / source
    m = json.loads(MANIFESTE.read_text(encoding="utf-8"))
    for e in m["documents"]:
        if e["source"] == source:
            return RACINE / e["copie"]
    return RACINE / source


def main() -> int:
    ap = argparse.ArgumentParser(description="Le corpus gelé des bancs.")
    ap.add_argument("--fige", action="store_true")
    ap.add_argument("--verifie", action="store_true")
    args = ap.parse_args()
    if args.fige:
        return fige()
    if args.verifie:
        return verifie()
    ap.error("--fige ou --verifie")
    return 2


if __name__ == "__main__":
    sys.exit(main())

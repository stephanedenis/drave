#!/usr/bin/env python3
"""epingle_corpus.py — l'épingle du corpus d'entraînement : sans elle, chaque PPL est une rumeur.

POURQUOI CE FICHIER EXISTE. L'alerte du 16/11 (`reports/rapport-native-reproductibilite.md`) a
montré que le `ppl_val` 2,40 annoncé **ne se reproduit pas** avec le `val.txt` actuel (17,3 à 22,6
selon le morceau lu). Un corpus qui bouge sous un modèle rend chaque perplexité incomparable à la
précédente. L'épingle est le sha256 du **train**, du **val** et de leurs canaux, la taille, la date
et le nombre de lignes — écrits dans un manifeste, revérifiables.

CE QU'ELLE NE FAIT PAS : elle ne modifie pas `data/` (territoire D) ; elle ne copie pas 1 Go.

Usage :
  python3 tools/epingle_corpus.py --corpus data/wiki_mix/propre --sortie reports/corpus-epingle.json
  python3 tools/epingle_corpus.py --corpus data/wiki_mix/propre --sortie reports/corpus-epingle.json --verifie
  python3 tools/epingle_corpus.py --autotest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import tempfile
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
MOTIFS = ("*.txt", "*.canal")


def empreinte(chemin: pathlib.Path, bloc: int = 1 << 23) -> dict:
    """sha256, octets, lignes — en une seule passe, en flux (pas de 1 Go en RAM)."""
    h = hashlib.sha256()
    octets = 0
    lignes = 0
    with chemin.open("rb") as f:
        while True:
            b = f.read(bloc)
            if not b:
                break
            h.update(b)
            octets += len(b)
            lignes += b.count(b"\n")
    return {"sha256": h.hexdigest(), "octets": octets, "lignes": lignes,
            "mtime": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(chemin.stat().st_mtime))}


def manifeste(dossier: pathlib.Path) -> dict:
    fichiers = {}
    for motif in MOTIFS:
        for p in sorted(dossier.glob(motif)):
            fichiers[p.name] = empreinte(p)
    if not fichiers:
        raise SystemExit(f"aucun fichier à épingler dans {dossier}")
    canon = json.dumps({n: {k: v for k, v in e.items() if k != "mtime"}
                        for n, e in sorted(fichiers.items())},
                       sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return {"schema": "drave.corpus-epingle", "version": 1,
            "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "corpus": str(dossier),
            "note": "sha256 du train, du val et des canaux ; --verifie recalcule et compare "
                    "l'empreinte de chaque fichier et l'empreinte du manifeste",
            "fichiers": fichiers,
            "manifeste_sha256": hashlib.sha256(canon.encode("utf-8")).hexdigest()}


def verifie(manifeste_json: pathlib.Path) -> int:
    doc = json.loads(manifeste_json.read_text())
    dossier = pathlib.Path(doc["corpus"])
    if not dossier.is_absolute():
        dossier = RACINE / dossier
    faute = 0
    for nom, attendu in doc["fichiers"].items():
        chemin = dossier / nom
        if not chemin.exists():
            print(f"  ❌ {nom} : ABSENT")
            faute += 1
            continue
        actuel = empreinte(chemin)
        if actuel["sha256"] != attendu["sha256"] or actuel["octets"] != attendu["octets"]:
            print(f"  ❌ {nom} : {actuel['sha256'][:16]}… ≠ {attendu['sha256'][:16]}…")
            faute += 1
        else:
            print(f"  ✅ {nom} : {actuel['sha256'][:16]}… ({actuel['octets']} o)")
    canon = json.dumps({n: {k: v for k, v in e.items() if k != 'mtime'}
                        for n, e in sorted(doc["fichiers"].items())}, sort_keys=True,
                       ensure_ascii=False, separators=(",", ":"))
    if hashlib.sha256(canon.encode("utf-8")).hexdigest() != doc["manifeste_sha256"]:
        print("  ❌ le manifeste lui-même a été modifié (empreinte du manifeste)")
        faute += 1
    return 0 if faute == 0 else 1


def autotest() -> int:
    """Le contrôle négatif : épingle un fichier, vérifie, change UN octet, re-vérifie."""
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        (d / "train.txt").write_bytes(b"le corpus\n" * 1000)
        (d / "val.txt").write_bytes(b"la validation\n" * 100)
        m = manifeste(d)
        p = d / "epingle.json"
        p.write_text(json.dumps(m))
        print("  cas 1 : intact")
        if verifie(p) != 0:
            print("  ❌ l'épingle ne reconnaît pas un corpus intact")
            return 1
        b = bytearray((d / "train.txt").read_bytes())
        b[10] ^= 0xFF
        (d / "train.txt").write_bytes(bytes(b))
        print("  cas 2 : un octet changé")
        if verifie(p) == 0:
            print("  ❌ l'épingle ne voit pas un octet changé")
            return 1
    print("  ✅ autotest : intact reconnu, un octet changé détecté")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", default="data/wiki_mix/propre")
    ap.add_argument("--sortie", default="reports/corpus-epingle.json")
    ap.add_argument("--verifie", action="store_true", help="recalcule et compare au manifeste")
    ap.add_argument("--autotest", action="store_true")
    a = ap.parse_args()
    if a.autotest:
        return autotest()
    sortie = pathlib.Path(a.sortie)
    if a.verifie:
        return verifie(sortie)
    dossier = pathlib.Path(a.corpus)
    if not dossier.is_absolute():
        dossier = RACINE / dossier
    doc = manifeste(dossier)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(f"corpus épinglé : {dossier}")
    for nom, e in doc["fichiers"].items():
        print(f"  {nom:12} {e['sha256'][:16]}… {e['octets']:>13} o  {e['lignes']:>11} lignes  {e['mtime']}")
    print(f"  manifeste : {doc['manifeste_sha256'][:16]}… → {sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

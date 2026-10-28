#!/usr/bin/env python3
"""drvm_trace.py — N0.5 : trace et rejeu d'un DRVM.

Le moteur n'exécute pas encore la passe avant d'un bloc DRVM : cette trace porte
donc sur le **contenu** (manifeste, blocs, tenseurs), pas sur les logits. Elle
répond à : le DRVM relu est-il exactement celui qui a été écrit ?
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib

from tools.drvm import _canonique, read_drvm


def tracer(drvm: str) -> dict:
    with read_drvm(drvm) as d:
        tensors = []
        for t in d.manifest["tensors"]:
            b = bytes(d.tensor(t["name"]))
            tensors.append({"name": t["name"], "bloc": t["bloc"],
                           "nbytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
        return {"format": "DRVM-TRACE", "version": 0, "source": str(drvm),
                "manifeste_sha256": hashlib.sha256(_canonique(d.manifest)).hexdigest(),
                "blocs": [b["id"] for b in d.manifest["graph"]["blocks"]],
                "tenseurs": tensors}


def rejouer(drvm: str, trace: dict) -> dict:
    attendu = trace.get("tenseurs", [])
    with read_drvm(drvm) as d:
        actuels = {t["name"]: hashlib.sha256(bytes(d.tensor(t["name"]))).hexdigest()
                   for t in d.manifest["tensors"]}
    mauvais = [t["name"] for t in attendu if actuels.get(t["name"]) != t["sha256"]]
    manquants = [t["name"] for t in attendu if t["name"] not in actuels]
    return {"identiques": not mauvais and not manquants,
            "tenseurs": len(attendu), "mauvais": mauvais, "manquants": manquants,
            "manifeste_sha256": hashlib.sha256(
                _canonique(d.manifest)).hexdigest() == trace.get("manifeste_sha256")}


def main() -> None:
    ap = argparse.ArgumentParser(description="trace/rejeu DRVM")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("trace"); a.add_argument("drvm"); a.add_argument("sortie")
    b = sub.add_parser("replay"); b.add_argument("drvm"); b.add_argument("trace")
    x = ap.parse_args()
    if x.cmd == "trace":
        t = tracer(x.drvm); pathlib.Path(x.sortie).write_text(
            json.dumps(t, ensure_ascii=False, indent=1) + "\n")
        print(json.dumps({"trace": x.sortie, "tenseurs": len(t["tenseurs"])}, indent=1))
    else:
        t = json.loads(pathlib.Path(x.trace).read_text())
        print(json.dumps(rejouer(x.drvm, t), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

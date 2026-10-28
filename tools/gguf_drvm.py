#!/usr/bin/env python3
"""gguf_drvm.py — N0.4 : conversion GGUF ↔ DRVM v0.

DRVM est le format natif ; GGUF reste un **format d'import/export**. La conversion
conserve les **octets des tenseurs** et le bloc de métadonnées GGUF (tokenizer
compris), pas les conventions d'exécution de GGUF.

Usage :
  python3 tools/gguf_drvm.py gguf2drvm MODELE.gguf MODELE.drvm
  python3 tools/gguf_drvm.py drvm2gguf MODELE.drvm MODELE.gguf
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import struct

from tools.convertir_clusters import lire_entete, parcourir_kv
from tools.drvm import TensorSpec, read_drvm, write_drvm

NOM_KV = "__gguf_kv"


def _octets_tenseur(source: str, base: int, offset: int, octets: int) -> bytes:
    with open(source, "rb") as f:
        f.seek(base + offset)
        b = f.read(octets)
    if len(b) != octets:
        raise ValueError(f"tenseur tronqué dans {source}")
    return b


def gguf_vers_drvm(gguf: str, drvm: str) -> dict:
    kv, tenseurs, base, alignement, n_t, version = lire_entete(gguf)
    n_kv, _ = parcourir_kv(kv)
    specs = [TensorSpec(NOM_KV, kv, dtype="u8", shape=(len(kv),), bloc="import",
                        quant="gguf_kv")]
    for t in tenseurs:
        data = _octets_tenseur(gguf, base, int(t["offset"]), int(t["octets"]))
        specs.append(TensorSpec(t["nom"], data, dtype=f"gguf_{t['ttype']}",
                                shape=tuple(int(d) for d in t["dims"]),
                                bloc="import", quant=str(t["ttype"])))
    manifeste = {
        "format": "DRVM", "version": 0,
        "model": {"name": pathlib.Path(gguf).stem, "parametres": 0,
                  "tokenizer": {"kind": "gguf", "source": pathlib.Path(gguf).name}},
        "graph": {"regions": [{"id": "r0", "blocks": ["import"]}],
                  "blocks": [{"id": "import", "kind": "input", "inputs": [], "outputs": ["h"]}],
                  "routes": [], "heads": [], "thought": None, "bridge": None},
        "execution": {"activation": "DRVF", "placement": "local",
                      "import": {"format": "GGUF", "version": version,
                                 "alignement": alignement, "n_tenseurs": n_t,
                                 "n_kv": n_kv,
                                 "kv_sha256": hashlib.sha256(kv).hexdigest()}},
    }
    h = write_drvm(drvm, manifeste, specs)
    return {"gguf": gguf, "drvm": drvm, "tenseurs": n_t, "kv_octets": len(kv),
            "sha256_drvm": h}


def drvm_vers_gguf(drvm: str, gguf: str) -> dict:
    with read_drvm(drvm) as d:
        imp = d.manifest["execution"].get("import")
        if not imp or imp.get("format") != "GGUF":
            raise ValueError("ce DRVM n'a pas été importé d'un GGUF")
        kv = bytes(d.tensor(NOM_KV))
        tenseurs = [t for t in d.manifest["tensors"] if t["name"] != NOM_KV]
        n_kv, _ = parcourir_kv(kv)
        alignement = int(imp.get("alignement", 32))
        with open(gguf, "wb") as f:
            f.write(b"GGUF")
            f.write(struct.pack("<I", int(imp.get("version", 3))))
            f.write(struct.pack("<Q", len(tenseurs)))
            f.write(struct.pack("<Q", n_kv))
            f.write(kv)
            decalage = 0
            for t in tenseurs:
                nom = t["name"].encode("utf-8")
                f.write(struct.pack("<Q", len(nom))); f.write(nom)
                dims = [int(x) for x in t["shape"]]
                f.write(struct.pack("<I", len(dims)))
                for x in reversed(dims):
                    f.write(struct.pack("<Q", x))
                f.write(struct.pack("<I", int(t.get("quant") or 0)))
                f.write(struct.pack("<Q", decalage))
                decalage += int(t["nbytes"])
            fin = f.tell()
            pad = (alignement - fin % alignement) % alignement
            f.write(b"\0" * pad)
            for t in tenseurs:
                f.write(bytes(d.tensor(t["name"])))
    return {"drvm": drvm, "gguf": gguf, "tenseurs": len(tenseurs),
            "sha256_gguf": hashlib.sha256(pathlib.Path(gguf).read_bytes()).hexdigest()}


def main() -> None:
    ap = argparse.ArgumentParser(description="GGUF ↔ DRVM")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("gguf2drvm"); a.add_argument("source"); a.add_argument("sortie")
    b = sub.add_parser("drvm2gguf"); b.add_argument("source"); b.add_argument("sortie")
    args = ap.parse_args()
    if args.cmd == "gguf2drvm":
        print(json.dumps(gguf_vers_drvm(args.source, args.sortie), ensure_ascii=False, indent=1))
    else:
        print(json.dumps(drvm_vers_gguf(args.source, args.sortie), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

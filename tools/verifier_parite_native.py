#!/usr/bin/env python3
"""verifier_parite_native.py — N0.8 : parité Rust natif ↔ Python sur plusieurs prompts.

Le Rust imprime les 5 premiers logits ; ce script les compare à la référence
PyTorch. Aucun tirage aléatoire : liste de prompts fixe.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess

import torch
from tools.native_model import NativeConfig, NativeModel

PROMPTS = [
    "La France est un pays",
    "Le chat dort sur",
    "Demain, nous irons",
    "def addition(a, b):",
    "Once upon a time",
]


def reference(modele, p, k=5):
    ids = torch.tensor([list(p.encode())])
    with torch.no_grad():
        logits = modele(ids)["logits"][0, -1]
    v, i = logits.topk(k)
    return [(int(i[j]), float(v[j])) for j in range(k)]


def rust(chemin, drvm, p, k=5):
    out = subprocess.run([chemin, "--drvm-forward", drvm, p], capture_output=True, text=True).stdout
    vals = re.findall(r"octet\s+(\d+).*?logit\s+(-?\d+\.\d+)", out)
    return [(int(a), float(b)) for a, b in vals[:k]]


def main() -> None:
    ap = argparse.ArgumentParser(description="parité Rust natif ↔ Python sur 5 prompts fixes")
    ap.add_argument("--checkpoint", default="/tmp/drave-n0-pont.pt")
    ap.add_argument("--drvm", default="/tmp/drave-n0-pont.drvm")
    ap.add_argument("--binaire", default="./drave-core/target/release/drave")
    ap.add_argument("--sortie", default="reports/native-parite.json")
    a = ap.parse_args()
    ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items() if k in NativeConfig.__annotations__})
    m = NativeModel(cfg); m.load_state_dict(ck["state"]); m.eval()
    a_binaire, a_drvm, sortie = a.binaire, a.drvm, a.sortie
    res = []
    for p in PROMPTS:
        a = reference(m, p); b = rust(a_binaire, a_drvm, p)
        ok_top1 = a[0][0] == b[0][0] if b else False
        ok_top5 = [x[0] for x in a] == [x[0] for x in b]
        ecart = max((abs(a[i][1] - b[i][1]) for i in range(min(len(a), len(b)))), default=999.0)
        res.append({"prompt": p, "top1_identique": ok_top1, "top5_identique": ok_top5,
                    "ecart_max": ecart, "python": a, "rust": b})
        print(f"{p!r} · top1 {ok_top1} · top5 {ok_top5} · écart max {ecart:.5f}")
    pathlib.Path(sortie).write_text(json.dumps(
        {"prompts": res, "top1": sum(r["top1_identique"] for r in res),
         "top5": sum(r["top5_identique"] for r in res), "n": len(res)}, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({"top1": sum(r["top1_identique"] for r in res),
                      "top5": sum(r["top5_identique"] for r in res), "n": len(res)}, indent=1))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fabrique un greffon (neurone ajouté) pour qtrinet-core.

Trois modes :
  zero     u = v = d = 0            -> doit donner EXACTEMENT la perplexité de base
  random   directions aléatoires    -> doit dégrader (prouve que le nœud est câblé)
  croise   u = ligne i de gate, v = ligne j de up (i != j), d ajusté à l'échelle
           -> appariement que le réseau n'a jamais calculé

Le réseau d'origine n'apparie que gate[i] avec up[i]. Un produit de deux formes
linéaires étant quadratique, un appariement croisé est une caractéristique neuve.

Usage : python3 tools/make_patch.py <mode> <couche> <sortie.bin> [--scale S] [--i I] [--j J]
"""
import argparse, struct, sys
import numpy as np
sys.path.insert(0, 'src')
from gguf_min import GGUF

MAGIE = b"QPAT"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["zero", "random", "croise"])
    ap.add_argument("layer", type=int)
    ap.add_argument("out")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--i", type=int, default=0)
    ap.add_argument("--j", type=int, default=1)
    ap.add_argument("--gguf", default="models/Qwen2.5-0.5B-Q8_0.gguf")
    a = ap.parse_args()

    g = GGUF(a.gguf)
    n = int(g.tensors[f"blk.{a.layer}.ffn_gate.weight"].shape[1])
    if a.mode == "zero":
        u = v = d = np.zeros(n, np.float32)
    elif a.mode == "random":
        rng = np.random.default_rng(1)
        s = 1e-3 * a.scale
        u = (rng.standard_normal(n) * s).astype(np.float32)
        v = (rng.standard_normal(n) * s).astype(np.float32)
        d = (rng.standard_normal(n) * s).astype(np.float32)
    else:
        Wg = g.dequant(f"blk.{a.layer}.ffn_gate.weight").astype(np.float32)
        Wu = g.dequant(f"blk.{a.layer}.ffn_up.weight").astype(np.float32)
        u = Wg[a.i % Wg.shape[0]].copy()
        v = Wu[a.j % Wu.shape[0]].copy()
        # d : direction de sortie associée à la ligne i du down d'origine,
        # mise à l'échelle — point de départ, l'ajustement viendra après
        Wd = g.dequant(f"blk.{a.layer}.ffn_down.weight").astype(np.float32)   # [896, 4864]
        d = (Wd[:, a.i % Wd.shape[1]] * a.scale).astype(np.float32)
    u = np.asarray(u, np.float32); v = np.asarray(v, np.float32); d = np.asarray(d, np.float32)
    with open(a.out, "wb") as f:
        f.write(MAGIE + struct.pack("<III", 1, a.layer, n))
        f.write(u.tobytes()); f.write(v.tobytes()); f.write(d.tobytes())
    print(f"greffon {a.mode} couche {a.layer} -> {a.out}  "
          f"(|u|={np.linalg.norm(u):.3f} |v|={np.linalg.norm(v):.3f} |d|={np.linalg.norm(d):.3f})")

main()

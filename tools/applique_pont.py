#!/usr/bin/env python3
"""applique_pont.py — le pont s'applique à N'IMPORTE QUELLE trace, langue inconnue.

Le pont est un artefact : trois matrices ajustées une fois (`pont_semantique.npz`),
et une application qui tient en trois lignes :

    abstrait = (plongee · W0) · Pᵀ + moy

`plongee` est la représentation du jeton à la COUCHE 0 — donc n'importe quel texte,
dans n'importe quelle langue, dès lors qu'on peut le faire passer par le modèle.

Usage : applique_pont.py <pont.npz> <trace.drvf> [--sortie abstrait.npy]
"""
import struct, sys
import numpy as np


def lire(chemin):
    def paires(f, n, version, bloc=32):
        ech = None
        if version == 3:
            nb, = struct.unpack("<I", f.read(4))
            ech = [struct.unpack("<e", f.read(2))[0] for _ in range(nb)]
        out, prev = [], 0
        for _ in range(n):
            if version == 1:
                i, = struct.unpack("<I", f.read(4))
            else:
                e, = struct.unpack("<B", f.read(1))
                i = struct.unpack("<H", f.read(2))[0] if e == 255 else prev + e
                prev = i
            if version == 3:
                v, = struct.unpack("<b", f.read(1))
                out.append((i, v * (ech[i // bloc] if ech else 1.0)))
            else:
                v, = struct.unpack("<h", f.read(2))
                out.append((i, v))
        return out

    with open(chemin, "rb") as f:
        assert f.read(4) == b"DRVF"
        version, = struct.unpack("<H", f.read(2))
        n_layer, hidden = struct.unpack("<II", f.read(8))
        pp = {}
        while True:
            b = f.read(2)
            if len(b) < 2: break
            c, = struct.unpack("<H", b)
            if c == 0xFFFF: break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            pp[(c, pos)] = paires(f, n, version)
    return hidden, pp


def main():
    if len(sys.argv) < 3:
        print(__doc__); return 1
    a = np.load(sys.argv[1], allow_pickle=True)
    P, moy, W0 = a["P"], a["moy"], a["W0"]
    hidden, pp = lire(sys.argv[2])
    positions = sorted(p for (c, p) in pp if c == 0)
    E = np.zeros((len(positions), hidden), dtype=np.float32)
    for k, p in enumerate(positions):
        for i, v in pp[(0, p)]:
            if i < hidden: E[k, i] = v
    A = (E @ W0) @ P.T + moy
    n = np.linalg.norm(A, axis=1, keepdims=True); n[n == 0] = 1
    U = (A / n)
    print(f"# {len(positions)} positions · abstrait {A.shape} (couche {int(a['couche'])} du professeur)")
    if len(U) > 1:
        S = U @ U.T
        iu = np.triu_indices(len(U), 1)
        print(f"#   cohérence interne (positions entre elles) : {S[iu].mean():.4f}")
    print(f"#   dernière position, premiers canaux : {' '.join(f'{v:+.4f}' for v in A[-1][:6])}")
    if "--sortie" in sys.argv:
        np.save(sys.argv[sys.argv.index("--sortie") + 1], A)
        print(f"# écrit : {sys.argv[sys.argv.index('--sortie') + 1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

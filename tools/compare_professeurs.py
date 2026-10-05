#!/usr/bin/env python3
"""compare_professeurs.py — les professeurs et notre pont, sur le MÊME périmètre.

Une comparaison d'invariance n'a de sens que si TOUT est mesuré sur les mêmes
langues, les mêmes unités et la même position. Ce tool prend une trace par
langue, lit une couche, et rend l'invariance inter-langue de la dernière
position — exactement la métrique des rapports précédents.

Usage : compare_professeurs.py <dossier> --couche N [--hidden H] [--etiquette "…"]
"""
import glob, os, struct, sys
import numpy as np


def lire(chemin, couches):
    """Lit UNE fois et rend, pour chaque couche demandée, le vecteur de la
    DERNIÈRE position. Le corps de chaque enregistrement est toujours parcouru —
    c'est la seule façon d'avancer dans le fichier — mais on ne le garde que
    s'il est demandé."""
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

    garde = {}
    with open(chemin, "rb") as f:
        assert f.read(4) == b"DRVF"
        version, = struct.unpack("<H", f.read(2))
        nl, hid = struct.unpack("<II", f.read(8))
        while True:
            b = f.read(2)
            if len(b) < 2:
                break
            c, = struct.unpack("<H", b)
            if c == 0xFFFF:
                break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            pp = paires(f, n, version)
            if c in couches:
                garde.setdefault(c, {})[pos] = pp
    sorties = {}
    for c in couches:
        d = garde.get(c) or {}
        if not d:
            sorties[c] = None; continue
        p = max(d)
        v = np.zeros(hid)
        for i, val in d[p]:
            if i < hid:
                v[i] = val
        sorties[c] = v
    return nl, hid, sorties


def inv(V):
    n = np.linalg.norm(V, axis=1, keepdims=True); n[n == 0] = 1
    S = (V/n) @ (V/n).T
    iu = np.triu_indices(len(V), 1)
    return float(S[iu].mean()), float(S[iu].min())


def main():
    d = sys.argv[1]
    cs = (sys.argv[sys.argv.index("--couches")+1] if "--couches" in sys.argv
          else sys.argv[sys.argv.index("--couche")+1] if "--couche" in sys.argv
          else "10")
    couches = [int(x) for x in cs.split(",")]
    etq = sys.argv[sys.argv.index("--etiquette")+1] if "--etiquette" in sys.argv else d
    noms, vecs = [], {c: [] for c in couches}
    for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
        nl, hid, s2 = lire(f, set(couches))
        noms.append(os.path.basename(f)[:-5])
        for c in couches:
            if s2[c] is not None:
                vecs[c].append(s2[c])
    print(f"# {etq} — {len(noms)} langues : {' '.join(noms)}")
    for c in couches:
        if len(vecs[c]) < 2:
            print(f"  couche {c:>2} : absente"); continue
        m, mi = inv(np.array(vecs[c]))
        print(f"  couche {c:>2} : invariance {m:.4f} · pire paire {mi:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

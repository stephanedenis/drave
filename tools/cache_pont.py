#!/usr/bin/env python3
"""cache_pont.py — parse UNE fois les traces, puis toutes les expériences sont rapides.

Le goulot de `pont_reservoir.py` n'est pas le réservoir (64 neurones, quelques
milliers de pas) mais la LECTURE : 2,1 Go de DRVF en Python pur, ~10 min par
essai. Hors de question de balayer des réglages à ce prix.

Usage : cache_pont.py <dossier> <sortie.npz> [--couche 10] [--hidden 896]
"""
import glob, os, struct, sys
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
        assert f.read(4) == b"DRVF", f"{chemin} : pas une trace DRVF"
        version, = struct.unpack("<H", f.read(2))
        n_layer, hidden = struct.unpack("<II", f.read(8))
        pp = {}
        while True:
            b = f.read(2)
            if len(b) < 2:
                break
            cc, = struct.unpack("<H", b)
            if cc == 0xFFFF:
                break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            pp[(cc, pos)] = paires(f, n, version)
    return hidden, pp


def main():
    d, sortie = sys.argv[1], sys.argv[2]
    c = int(sys.argv[sys.argv.index("--couche") + 1]) if "--couche" in sys.argv else 10
    hidden = int(sys.argv[sys.argv.index("--hidden") + 1]) if "--hidden" in sys.argv else 896
    cles, E, Y = [], [], []
    for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
        h, pp = lire(f)
        pos = sorted(p for (cc, p) in pp if cc == 0)
        e = np.zeros((len(pos), h), dtype=np.float32)
        y = np.zeros((len(pos), h), dtype=np.float32)
        for k, p in enumerate(pos):
            for i, v in pp[(0, p)]:
                if i < h: e[k, i] = v
            for i, v in pp.get((c, p), []):
                if i < h: y[k, i] = v
        cles.append(os.path.basename(f)[:-5]); E.append(e); Y.append(y)
        print(f"  {cles[-1]} : {len(pos)} pas", flush=True)
    np.savez_compressed(sortie, cles=np.array(cles), hidden=hidden,
                        **{f"E{i}": e for i, e in enumerate(E)},
                        **{f"Y{i}": y for i, y in enumerate(Y)})
    print(f"{sortie} : {len(cles)} langues · {sum(len(e) for e in E)} pas")


if __name__ == "__main__":
    sys.exit(main())

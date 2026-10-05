#!/usr/bin/env python3
"""sous_ensemble_actif.py — quelle PART de la couche sémantique porte un énoncé ?

Question posée : pour un énoncé donné, dans une langue donnée, seule une partie
de la couche de référence devrait être active. Ce tool le mesure, au lieu de le
supposer :

  - combien de canaux portent 50 %, 90 %, 99 % de l'énergie ?
  - le sous-ensemble actif est-il le MÊME d'une langue à l'autre pour le même
    énoncé, ou propre à chaque langue ?

Usage : sous_ensemble_actif.py <dossier> --couche 10 [--position derniere|toutes]
"""
import glob, os, struct, sys
import numpy as np


def lire(chemin, couche):
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

    pos_voulues = {}
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
            if c == couche:
                pos_voulues[pos] = pp
    return hid, pos_voulues


def vecteur(pp, hid):
    v = np.zeros(hid)
    for i, val in pp:
        if i < hid:
            v[i] = val
    return v


def main():
    d = sys.argv[1]
    c = int(sys.argv[sys.argv.index("--couche")+1]) if "--couche" in sys.argv else 10
    noms, V = [], []
    for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
        hid, pos = lire(f, c)
        if not pos:
            continue
        p = max(pos)
        V.append(vecteur(pos[p], hid)); noms.append(os.path.basename(f)[:-5])
    V = np.array(V)
    print(f"# {len(noms)} langues · couche {c} · dernière position · {V.shape[1]} canaux")
    E = V**2
    tot = E.sum(1, keepdims=True); tot[tot == 0] = 1
    part = np.sort(E/tot, axis=1)[:, ::-1]
    cum = np.cumsum(part, axis=1)
    print(f"\n{'langue':>6} {'50 %':>7} {'90 %':>7} {'99 %':>7} {'canaux>0':>9}")
    for i, L in enumerate(noms):
        n50 = int(np.searchsorted(cum[i], 0.50)+1)
        n90 = int(np.searchsorted(cum[i], 0.90)+1)
        n99 = int(np.searchsorted(cum[i], 0.99)+1)
        nz = int((V[i] != 0).sum())
        print(f"{L:>6} {n50:>7} {n90:>7} {n99:>7} {nz:>9}")
    m50 = np.mean([np.searchsorted(cum[i], 0.50)+1 for i in range(len(noms))])
    m90 = np.mean([np.searchsorted(cum[i], 0.90)+1 for i in range(len(noms))])
    m99 = np.mean([np.searchsorted(cum[i], 0.99)+1 for i in range(len(noms))])
    H = V.shape[1]
    print(f"\nmoyennes : 50 % sur {m50:.0f}/{H} canaux ({100*m50/H:.0f} %) · "
          f"90 % sur {m90:.0f} ({100*m90/H:.0f} %) · 99 % sur {m99:.0f} ({100*m99/H:.0f} %)")
    # le sous-ensemble actif est-il partagé entre langues ?
    A = (V != 0)
    inter = A.sum(0); union = (A.sum(0) > 0).sum()
    print(f"\ncanaux actifs dans AU MOINS une langue : {union}/{H}")
    print(f"canaux actifs dans TOUTES les langues  : {int((inter == len(noms)).sum())}/{H}")
    print(f"moyenne de langues par canal actif     : {inter.mean():.2f} sur {len(noms)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

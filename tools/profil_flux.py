#!/usr/bin/env python3
"""Profilage par neurone à partir d'une trace de flux (format DRVF).

Ce que la vision demande, rendu calculable : « quels neurones s'allument, à
quelle fréquence, avec quelle magnitude » — par couche, depuis n'importe quelle
trace, sans instrumenter le moteur autrement.

Usage : profil_flux.py <trace> [--couche N] [--top 6] [--csv sortie.csv]
"""
import struct
import sys


def lire(chemin):
    with open(chemin, "rb") as f:
        assert f.read(4) == b"DRVF", "ce n'est pas une trace DRVF"
        struct.unpack("<H", f.read(2))
        n_layer, hidden = struct.unpack("<II", f.read(8))
        listes = []
        while True:
            b = f.read(2)
            if len(b) < 2:
                break
            couche, = struct.unpack("<H", b)
            if couche == 0xFFFF:
                break
            pos, n, echelle = struct.unpack("<IIf", f.read(12))
            actifs = []
            for _ in range(n):
                i, v = struct.unpack("<Ih", f.read(6))
                actifs.append((i, v * echelle))
            listes.append((couche, pos, echelle, actifs))
    return n_layer, hidden, listes


def main():
    trace = sys.argv[1]
    top = 6
    if "--top" in sys.argv:
        top = int(sys.argv[sys.argv.index("--top") + 1])
    csv = None
    if "--csv" in sys.argv:
        csv = sys.argv[sys.argv.index("--csv") + 1]
    n_layer, hidden, listes = lire(trace)
    print(f"{trace} : {len(listes)} listes · {n_layer} couches · {hidden} cachés")
    par_couche = {}
    for couche, _, _, actifs in listes:
        d = par_couche.setdefault(couche, {"n": 0, "actifs": 0, "freq": {}, "mag": {}})
        d["n"] += 1
        d["actifs"] += len(actifs)
        for i, v in actifs:
            d["freq"][i] = d["freq"].get(i, 0) + 1
            d["mag"][i] = d["mag"].get(i, 0.0) + abs(v)
    lignes = []
    print(f"{'couche':>9} {'densité':>9} {'top 10 % portent':>17} {'neurone le + fort':>18} {'part':>7}")
    for couche in sorted(par_couche):
        d = par_couche[couche]
        densite = d["actifs"] / (d["n"] * hidden) if d["n"] else 0.0
        tot = sum(d["mag"].values()) or 1.0
        forts = sorted(d["mag"].items(), key=lambda kv: -kv[1])
        n10 = max(1, len(forts) // 10)
        part10 = sum(v for _, v in forts[:n10]) / tot
        i_max, m_max = forts[0]
        nom = f"{couche}" if couche < 1000 else f"FFN {couche - 1000}"
        print(f"{nom:>9} {100*densite:>8.1f}% {100*part10:>16.1f}% {i_max:>18} {100*m_max/tot:>6.1f}%")
        for i, v in forts[:top]:
            lignes.append((couche, i, v, d["freq"].get(i, 0)))
    if csv:
        with open(csv, "w") as f:
            f.write("couche,neurone,magnitude,frequence\n")
            for couche, i, v, fr in lignes:
                f.write(f"{couche},{i},{v:.4f},{fr}\n")
        print(f"{len(lignes)} neurones exportés dans {csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

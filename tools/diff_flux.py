#!/usr/bin/env python3
"""Diff de deux traces de **flux d'activation** (format DRVF).

C'est l'outil qui manquait à la vision : deux exécutions du même modèle, et on
veut savoir non pas « la perplexité a bougé » mais **où** le flux diverge, à
quelle couche, à quel jeton, et de combien.

Usage : diff_flux.py <traceA> <traceB> [--top 8]
"""
import struct
import sys


def lire(chemin):
    with open(chemin, "rb") as f:
        assert f.read(4) == b"DRVF", "ce n'est pas une trace DRVF"
        version, = struct.unpack("<H", f.read(2))
        n_layer, hidden = struct.unpack("<II", f.read(8))
        listes = {}
        while True:
            b = f.read(2)
            if len(b) < 2:
                break
            couche, = struct.unpack("<H", b)
            if couche == 0xFFFF:
                break
            pos, n, echelle = struct.unpack("<IIf", f.read(12))
            actifs = {}
            for _ in range(n):
                i, v = struct.unpack("<Ih", f.read(6))
                actifs[i] = v
            listes[(couche, pos)] = (echelle, actifs)
    return version, n_layer, hidden, listes


def main():
    a = lire(sys.argv[1])
    b = lire(sys.argv[2])
    top = 8
    if "--top" in sys.argv:
        top = int(sys.argv[sys.argv.index("--top") + 1])
    la, lb = a[3], b[3]
    print(f"trace A : {len(la)} listes · trace B : {len(lb)} listes "
          f"· version {a[0]} · {a[1]} couches · {a[2]} cachés")
    communes = sorted(set(la) & set(lb))
    if not communes:
        print("aucune liste commune : les deux traces ne portent pas sur la même exécution")
        return 1
    par_couche = {}
    premier = None
    for cle in communes:
        ea, aa = la[cle]
        eb, ab = lb[cle]
        # On compare les valeurs DÉQUANTIFIÉES (valeur × échelle) : comparer les
        # entiers bruts de deux exécutions dont les échelles diffèrent ne veut
        # rien dire — la première version de cet outil affichait des écarts de
        # 1e8 pour cette raison.
        n = 0
        mx = 0.0
        for i in set(aa) | set(ab):
            d = abs(aa.get(i, 0) * ea - ab.get(i, 0) * eb)
            if d > 0.0:
                n += 1
                if d > mx:
                    mx = d
        if n == 0:
            continue
        couche, pos = cle
        # écart relatif à la DYNAMIQUE de la liste : comparable entre couches
        dyn = ea * 32767.0 if ea > 0 else 1.0
        rel = mx / dyn
        c = par_couche.setdefault(couche, [0, 0.0, None])
        c[0] += n
        c[1] = max(c[1], rel)
        c[2] = pos if c[2] is None else c[2]
        if premier is None:
            premier = (couche, pos, n, rel)
    if premier is None:
        print("les deux flux sont IDENTIQUES, neurone par neurone")
        return 0
    print(f"première divergence : couche {premier[0]} · jeton {premier[1]} · "
          f"{premier[2]} neurones · écart max {premier[3]:.3e} (de la dynamique)")
    print(f"{'couche':>8} {'neurones changés':>17} {'écart / dynamique':>19} {'1er jeton':>10}")
    for couche, (n, rel, pos) in sorted(par_couche.items(), key=lambda kv: -kv[1][1])[:top]:
        nom = f"{couche}" if couche < 1000 else f"FFN {couche - 1000}"
        print(f"{nom:>8} {n:>17} {rel:>19.3e} {pos:>10}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

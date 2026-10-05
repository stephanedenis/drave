#!/usr/bin/env python3
"""cancellation_langue.py — le composant « langue » est-il SOUSTRACTIBLE ?

Le fondement de la règle contrastive : si l'on peut annuler le composant de langue
par une simple soustraction, alors « rétroactivité négative » est la bonne
direction, et la règle anti-hebbienne n'est que la façon de l'APPRENDRE.

Ce que l'outil fait, sur des traces réelles :

  1. pour chaque langue L, la moyenne sur les positions `x̄_L` — le « portrait de
     langue » de l'article ;
  2. le décalage de langue `δ_L = x̄_L − moyenne_des_langues` ;
  3. on SOUSTRAIT δ_L de chaque position, et on re-mesure la similarité cosinus
     entre langues.

**Le témoin est dans l'outil** : on fait la MÊME chose avec un δ tiré au hasard de
même norme. Si la soustraction du vrai δ ne fait pas mieux que le hasard, alors
elle ne retire pas de la langue — elle retire de la norme.

**Ce que ce n'est PAS** : δ est calculé SUR LES LANGues DE TEST, donc c'est un
oracle. Le chiffre obtenu est une BORNE SUPÉRIEURE de ce qu'un apprentissage
pourrait atteindre, pas une méthode déployable. Il dit si la direction existe.

Usage : cancellation_langue.py <dossier .drvf> [--base 0] [--couche 10]
"""
import glob
import os
import random
import struct
import sys
from itertools import combinations


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
        par_pos = {}
        while True:
            b = f.read(2)
            if len(b) < 2: break
            couche, = struct.unpack("<H", b)
            if couche == 0xFFFF: break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            par_pos[(couche, pos)] = paires(f, n, version)
    return n_layer, hidden, par_pos


def vect(par_pos, couche, pos, hidden):
    v = [0.0] * hidden
    for i, val in par_pos.get((couche, pos), []):
        if i < hidden: v[i] = val
    return v


def cos(a, b):
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return None if na == 0 or nb == 0 else sum(x * y for x, y in zip(a, b)) / (na * nb)


def moyenne(listes):
    n = len(listes)
    return [sum(v[i] for v in listes) / n for i in range(len(listes[0]))]


def score(traces, couche, hidden, delta=None):
    """Cosinus moyen de toutes les paires, à la dernière position, δ soustrait."""
    derniers = {}
    for lang, pp in traces.items():
        pos = max(p for (c, p) in pp if c == couche)
        derniers[lang] = vect(pp, couche, pos, hidden)
    if delta:
        for lang in derniers:
            d = delta[lang]
            derniers[lang] = [a - b for a, b in zip(derniers[lang], d)]
    vals = [cos(derniers[a], derniers[b]) for a, b in combinations(sorted(derniers), 2)]
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals), min(vals)


def main():
    d = sys.argv[1]
    base = int(sys.argv[sys.argv.index("--base") + 1]) if "--base" in sys.argv else 0
    couche = int(sys.argv[sys.argv.index("--couche") + 1]) if "--couche" in sys.argv else 10
    traces = {}
    for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
        n_layer, hidden, pp = lire(f)
        traces[os.path.basename(f)[:-5]] = pp
    c = base + couche
    # portraits de langue : moyenne sur TOUTES les positions de l'article
    portraits = {}
    for lang, pp in traces.items():
        positions = [p for (cc, p) in pp if cc == c]
        portraits[lang] = moyenne([vect(pp, c, p, hidden) for p in positions])
    moyen = moyenne(list(portraits.values()))
    delta = {l: [a - b for a, b in zip(portraits[l], moyen)] for l in portraits}

    m0, min0 = score(traces, c, hidden)
    m1, min1 = score(traces, c, hidden, delta)
    # TÉMOIN : mêmes normes, directions au hasard
    rnd = random.Random(1)
    hasard = {l: [rnd.gauss(0, 1) for _ in range(hidden)] for l in portraits}
    for l in hasard:
        n0 = sum(x * x for x in delta[l]) ** 0.5
        n1 = sum(x * x for x in hasard[l]) ** 0.5 or 1.0
        hasard[l] = [x * n0 / n1 for x in hasard[l]]
    m2, min2 = score(traces, c, hidden, hasard)

    print(f"# {len(traces)} langues · couche {couche} (base {base}) · "
          f"{len(list(combinations(traces, 2)))} paires")
    print(f"{'lecture':<34} {'cos moyen':>10} {'pire paire':>11}")
    print(f"{'brute':<34} {m0:>10.4f} {min0:>11.4f}")
    print(f"{'δ de langue SOUSTRAIT':<34} {m1:>10.4f} {min1:>11.4f}")
    print(f"{'TÉMOIN : δ au hasard, même norme':<34} {m2:>10.4f} {min2:>11.4f}")
    print(f"\n# δ de langue : gain {(m1-m0):+.4f} · témoin {(m2-m0):+.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

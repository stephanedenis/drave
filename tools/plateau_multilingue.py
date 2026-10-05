#!/usr/bin/env python3
"""plateau_multilingue.py — à quelle profondeur les langues se rejoignent-elles ?

Étend `invariance_semantique.py` d'une paire à N langues : pour chaque couche, la
similarité cosinus MOYENNE de toutes les paires de langues, sur la dernière
position (la représentation de l'énoncé entier).

Ce que ça mesure, et pourquoi c'est la base de toute émulation sémantique : un
modèle qui « répond la même chose » dans dix langues doit avoir, quelque part,
une représentation qui ne dépend plus de la langue. La couche où la similarité
est maximale est cette couche-là — et c'est là qu'un adaptateur a un sens.

Usage : plateau_multilingue.py <dossier de traces .drvf> [--base 0]
"""
import glob
import os
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
        assert f.read(4) == b"DRVF", f"{chemin} : pas une trace DRVF"
        version, = struct.unpack("<H", f.read(2))
        n_layer, hidden = struct.unpack("<II", f.read(8))
        listes = []
        while True:
            b = f.read(2)
            if len(b) < 2:
                break
            couche, = struct.unpack("<H", b)
            if couche == 0xFFFF:
                break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            listes.append((couche, pos, ech, paires(f, n, version)))
    return n_layer, hidden, listes


def cos(a, b):
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return None
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 1
    base = int(sys.argv[sys.argv.index("--base") + 1]) if "--base" in sys.argv else 0
    traces = {}
    for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.drvf"))):
        lang = os.path.basename(f)[:-5]
        n_layer, hidden, listes = lire(f)
        derniere = {}
        for (c, p, _, _) in listes:
            if p > derniere.get(c, -1):
                derniere[c] = p
        vect = {}
        for c in derniere:
            v = [0.0] * hidden
            for (cc, pp, ech, prs) in listes:
                if cc == c and pp == derniere[c]:
                    for i, val in prs:
                        if i < hidden:
                            v[i] = val * ech
            vect[c] = v
        traces[lang] = (hidden, vect)
    langs = sorted(traces)
    print(f"# {len(langs)} langues : {' '.join(langs)}")
    couches = sorted(set.intersection(*[set(t[1]) for t in traces.values()]))
    print(f"{'couche':>7} {'cos moyen':>10} {'min':>8} {'paires':>7}")
    meilleur = (-1.0, -1)
    for c in couches:
        if c < base or c >= base + 1000:
            continue
        vals = []
        for a, b in combinations(langs, 2):
            s = cos(traces[a][1][c], traces[b][1][c])
            if s is not None:
                vals.append(s)
        if not vals:
            continue
        m = sum(vals) / len(vals)
        if m > meilleur[0]:
            meilleur = (m, c - base)
        print(f"{c - base:>7} {m:>10.4f} {min(vals):>8.4f} {len(vals):>7}")
    print(f"\n# maximum : {meilleur[0]:.4f} à la couche {meilleur[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

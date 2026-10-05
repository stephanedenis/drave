#!/usr/bin/env python3
"""lecture_plateau.py — le plateau dépend-il de la LECTURE, ou seulement du modèle ?

Question posée : peut-on rapprocher les langues SANS rien entraîner, en changeant
seulement la façon de LIRE les couches ? Trois lectures comparées, sur les mêmes
traces :

  - une couche seule ;
  - la MOYENNE de k couches voisines centrées sur le plateau ;
  - la moyenne PONDÉRÉE par l'inverse de la variance inter-langue de chaque couche
    (les couches qui divergent le plus entre langues pèsent le moins).

Aucune n'apprend : ce sont trois façons de lire ce que le modèle a déjà calculé.
C'est la version « inférence seule » de la question — et si elle paie, elle paie
sans corpus, sans règle locale, sans rien.

Usage : lecture_plateau.py <dossier de traces .drvf> [--base 0]
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
        assert f.read(4) == b"DRVF"
        version, = struct.unpack("<H", f.read(2))
        n_layer, hidden = struct.unpack("<II", f.read(8))
        listes = []
        while True:
            b = f.read(2)
            if len(b) < 2: break
            couche, = struct.unpack("<H", b)
            if couche == 0xFFFF: break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            listes.append((couche, pos, ech, paires(f, n, version)))
    return n_layer, hidden, listes


def cos(a, b):
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return None if na == 0 or nb == 0 else sum(x * y for x, y in zip(a, b)) / (na * nb)


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 1
    base = int(sys.argv[sys.argv.index("--base") + 1]) if "--base" in sys.argv else 0
    traces = {}
    for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.drvf"))):
        n_layer, hidden, listes = lire(f)
        derniere = {}
        for (c, p, _, _) in listes:
            if p > derniere.get(c, -1): derniere[c] = p
        vect = {}
        for c in derniere:
            v = [0.0] * hidden
            for (cc, pp, ech, prs) in listes:
                if cc == c and pp == derniere[c]:
                    for i, val in prs:
                        if i < hidden: v[i] = val * ech
            vect[c] = v
        traces[os.path.basename(f)[:-5]] = vect
    langs = sorted(traces)
    couches = sorted(set.intersection(*[set(t) for t in traces.values()]))
    couches = [c for c in couches if base <= c < base + 1000]

    def moy(poids):
        """Score d'une combinaison : cosinus moyen de toutes les paires."""
        tot, n = 0.0, 0
        for a, b in combinations(langs, 2):
            va = [0.0] * len(traces[a][couches[0]])
            vb = [0.0] * len(va)
            for c, w in poids:
                if w == 0: continue
                for i, x in enumerate(traces[a][c]): va[i] += w * x
                for i, y in enumerate(traces[b][c]): vb[i] += w * y
            s = cos(va, vb)
            if s is not None: tot += s; n += 1
        return tot / max(n, 1)

    print(f"# {len(langs)} langues · {len(couches)} couches · base {base}")
    seul = [(c - base, moy([(c, 1.0)])) for c in couches]
    meilleur_seul = max(seul, key=lambda t: t[1])
    print(f"\n1. COUCHE SEULE — meilleure : couche {meilleur_seul[0]} → {meilleur_seul[1]:.4f}")
    for k, v in sorted(seul, key=lambda t: -t[1])[:4]:
        print(f"     couche {k:>3} : {v:.4f}")

    k = 3
    meilleur_moy = (-1, None)
    for i in range(len(couches) - k + 1):
        grp = couches[i:i + k]
        s = moy([(c, 1.0 / k) for c in grp])
        if s > meilleur_moy[0]: meilleur_moy = (s, grp)
    print(f"\n2. MOYENNE de {k} couches voisines — meilleure : "
          f"couches {[c - base for c in meilleur_moy[1]]} → {meilleur_moy[0]:.4f}")

    # pondération par l'inverse de la dispersion inter-langue de chaque couche
    disp = {}
    for c in couches:
        v = [traces[l][c] for l in langs]
        m = [sum(x[i] for x in v) / len(v) for i in range(len(v[0]))]
        disp[c] = sum(sum((x[i] - m[i]) ** 2 for i in range(len(m))) for x in v) / len(v)
    inv = {c: 1.0 / (disp[c] + 1e-9) for c in couches}
    tot = sum(inv.values())
    s_inv = moy([(c, inv[c] / tot) for c in couches])
    print(f"\n3. MOYENNE PONDÉRÉE par l'inverse de la dispersion inter-langue → {s_inv:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

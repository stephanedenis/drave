#!/usr/bin/env python3
"""invariance_semantique.py — à quelle profondeur la représentation devient-elle
sémantique plutôt que de surface ?

Idée (Stéphane) : garder les PREMIÈRES couches d'un grand modèle jusqu'au niveau
où la représentation est « en sémantique pure », puis reproduire les couches du
milieu par un modèle récurrent — donc sans les entraîner.

La mesure qui décide de ce niveau : l'INVARIANCE À LA FORME DE SURFACE. Deux
phrases de même sens dans deux langues doivent se ressembler d'autant plus qu'on
monte dans la pile — si l'hypothèse est vraie. Si la similarité ne monte jamais,
il n'y a pas de « niveau sémantique » à trouver, et l'architecture en trois blocs
n'a pas de point de coupe.

Usage : invariance_semantique.py <trace_A.drvf> <trace_B.drvf> [--base 0|1000]
"""
import struct
import sys


def lire(chemin):
    """Lit une trace DRVF (v1, v2 ou v3) — même lecteur que `analyse_flux.py`,
    pour ne pas en entretenir deux."""
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
                if e == 255:
                    i, = struct.unpack("<H", f.read(2))
                else:
                    i = prev + e
                prev = i
            if version == 3:
                v, = struct.unpack("<b", f.read(1))
                out.append((i, v * (ech[i // bloc] if ech else 1.0)))
            else:
                v, = struct.unpack("<h", f.read(2))
                out.append((i, v))
        return out

    with open(chemin, "rb") as f:
        assert f.read(4) == b"DRVF", "ce n'est pas une trace DRVF"
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


def vecteur(listes, couche, pos, hidden):
    """Le vecteur dense d'une (couche, position) : les listes sont des ÉCARTS
    quantifiés, donc ce qu'on reconstruit est le flux tel que le moteur l'a
    transporté — c'est ce transport-là qu'on mesure."""
    v = [0.0] * hidden
    for (c, p, ech, prs) in listes:
        if c == couche and p == pos:
            for i, val in prs:
                if i < hidden:
                    v[i] = val * ech
    return v


def cos(a, b):
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    base = 0
    if "--base" in sys.argv:
        base = int(sys.argv[sys.argv.index("--base") + 1])
    nA, hA, lA = lire(sys.argv[1])
    nB, hB, lB = lire(sys.argv[2])
    assert hA == hB, f"largeurs différentes : {hA} et {hB}"
    # dernière position de chaque trace, par couche
    def derniere(listes):
        m = {}
        for (c, p, _, _) in listes:
            if p > m.get(c, -1):
                m[c] = p
        return m
    dA, dB = derniere(lA), derniere(lB)
    print(f"# {nA} couches · largeur {hA} · base {base} (0 = attention, 1000 = FFN)")
    print(f"# A : dernière position {max(dA.values())} · B : {max(dB.values())}")
    print(f"{'couche':>7} {'similarité':>11}")
    meilleur = (0.0, -1)
    for c in sorted(set(dA) & set(dB)):
        if c < base or c >= base + 1000:
            continue
        a = vecteur(lA, c, dA[c], hA)
        b = vecteur(lB, c, dB[c], hB)
        s = cos(a, b)
        if s > meilleur[0]:
            meilleur = (s, c)
        print(f"{c - base:>7} {s:>11.4f}")
    print(f"\n# similarité maximale : {meilleur[0]:.4f} à la couche {meilleur[1] - base}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

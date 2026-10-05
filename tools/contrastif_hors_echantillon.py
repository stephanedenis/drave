#!/usr/bin/env python3
"""contrastif_hors_echantillon.py — la règle contrastive APPRISE sur des langues
d'entraînement, TESTÉE sur des langues jamais vues.

C'est le test que la règle de Hebb non ciblée a échoué (§9 de
`note-cancellation-evenementielle.md`) : elle montait en échantillon et
**dégradait** les langues tenues à l'écart.

La règle contrastive, elle, n'accumule que ce qui CHANGE AVEC LA LANGUE :

    D  -=  η · Σ_L (x̄_L − x̄̄) ⊗ (x̄_L − x̄̄)
    x'  =  x + D·x

où `x̄_L` est la moyenne de l'activation sur l'article dans la langue L. C'est
l'anti-Hebbien sur la covariance INTER-LANGUE : il ne pénalise que ce qui varie
avec la langue, donc il préserve par construction ce qui ne varie pas.

Témoin obligatoire : mêmes normes, directions au hasard.

Usage : contrastif_hors_echantillon.py <dossier_train> <dossier_test>
                                      [--couche 10] [--eta 1.0]
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
        pp = {}
        while True:
            b = f.read(2)
            if len(b) < 2: break
            couche, = struct.unpack("<H", b)
            if couche == 0xFFFF: break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            pp[(couche, pos)] = paires(f, n, version)
    return hidden, pp


def charge(dossier):
    out = {}
    for f in sorted(glob.glob(os.path.join(dossier, "*.drvf"))):
        hidden, pp = lire(f)
        out[os.path.basename(f)[:-5]] = (hidden, pp)
    return out


def v(pp, c, p, hidden):
    x = [0.0] * hidden
    for i, val in pp.get((c, p), []):
        if i < hidden: x[i] = val
    return x


def moyenne(listes):
    n = len(listes)
    return [sum(x[i] for x in listes) / n for i in range(len(listes[0]))]


def cos(a, b):
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return None if na == 0 or nb == 0 else sum(x * y for x, y in zip(a, b)) / (na * nb)


def mesure(traces, c, hidden, D=None, eta=0.0):
    """Cosinus à la DERNIÈRE position, D appliqué si fourni."""
    vs = {}
    for lang, (h, pp) in traces.items():
        pos = max(p for (cc, p) in pp if cc == c)
        x = v(pp, c, pos, hidden)
        if D is not None:
            y = [0.0] * hidden
            for i in range(hidden):
                if x[i] == 0.0: continue
                ligne = D[i]
                for j in range(hidden):
                    y[j] += eta * x[i] * ligne[j] if False else 0.0
            # D est symétrique (covariance) : on l'applique en une passe
            y = [sum(D[i][j] * x[j] for j in range(hidden)) for i in range(hidden)]
            x = [a + eta * b for a, b in zip(x, y)]
        vs[lang] = x
    vals = [cos(vs[a], vs[b]) for a, b in combinations(sorted(vs), 2)]
    vals = [s for s in vals if s is not None]
    return sum(vals) / len(vals), min(vals)


def main():
    dtr, dte = sys.argv[1], sys.argv[2]
    c = int(sys.argv[sys.argv.index("--couche") + 1]) if "--couche" in sys.argv else 10
    eta = float(sys.argv[sys.argv.index("--eta") + 1]) if "--eta" in sys.argv else 1.0
    tr, te = charge(dtr), charge(dte)
    hidden = list(tr.values())[0][0]
    # moyennes d'article sur les langues d'ENTRAÎNEMENT
    port = {}
    for lang, (h, pp) in tr.items():
        pos = [p for (cc, p) in pp if cc == c]
        port[lang] = moyenne([v(pp, c, p, hidden) for p in pos])
    moy = moyenne(list(port.values()))
    # covariance inter-langue : D[i][j] = −Σ_L (x̄_L−x̄̄)_i (x̄_L−x̄̄)_j  normalisée
    D = [[0.0] * hidden for _ in range(hidden)]
    n_l = len(port)
    for lang in port:
        d = [a - b for a, b in zip(port[lang], moy)]
        idx = [i for i in range(hidden) if abs(d[i]) > 1e-9]
        for i in idx:
            di = d[i]
            for j in idx:
                D[i][j] -= di * d[j] / n_l
    # normalisation : ρ(D) ≈ plus grande valeur propre ; on borne par la norme de Frobenius
    fro = sum(D[i][j] ** 2 for i in range(hidden) for j in range(hidden)) ** 0.5
    if fro > 0:
        for i in range(hidden):
            for j in range(hidden):
                D[i][j] /= fro
    rnd = random.Random(7)
    Dh = [[rnd.gauss(0, 1) / (hidden ** 0.5) for _ in range(hidden)] for _ in range(hidden)]

    print(f"# entraînement : {len(tr)} langues ({' '.join(sorted(tr))})")
    print(f"# test         : {len(te)} langues ({' '.join(sorted(te))}) — JAMAIS vues")
    print(f"# couche {c} · η {eta} · ‖D‖_F {fro:.3e} après normalisation")
    print(f"\n{'lecture':<38} {'cos moyen':>10} {'pire paire':>11}")
    for nom, Dx in (("brute", None), ("contrastif appris (train)", D),
                    ("TÉMOIN : même norme, hasard", Dh)):
        m, mi = mesure(te, c, hidden, Dx, eta)
        print(f"{nom:<38} {m:>10.4f} {mi:>11.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

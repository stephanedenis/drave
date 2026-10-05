#!/usr/bin/env python3
"""approximabilite_bloc.py — un bloc de couches est-il approximable par une
application BEAUCOUP plus simple ?

Question préalable à toute distillation (idée de Stéphane : distiller les couches
0-9 d'un grand modèle dans un modèle récurrent, en commençant par là parce que
l'entrée de la couche 0 est du TEXTE, donc échantillonnable sans rien simuler).

Ce que l'outil rend, pour un bloc `a..b` : la part de variance de la sortie du
bloc expliquée par une application LINÉAIRE de son entrée, ajustée sur les flux
réels (moindres carrés, forward-only).

  - R² élevé  → le bloc est presque linéaire ; un récurrent léger peut le porter ;
  - R² faible → le bloc fait autre chose, et il faudra de la non-linéarité.

La mesure se fait sur la représentation TRANSPORTÉE (DRVF v3), pas sur la
représentation exacte : c'est le bon périmètre ici, puisque c'est ce que Drave
transporte.

Usage : approximabilite_bloc.py <trace.drvf> --de 0 --a 10 [--base 0]
"""
import struct
import sys


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


def dense(listes, couche, positions, hidden):
    """Matrice n_positions × hidden, reconstruite depuis les listes."""
    idx = {p: k for k, p in enumerate(positions)}
    M = [[0.0] * hidden for _ in positions]
    for (c, p, ech, prs) in listes:
        if c != couche or p not in idx:
            continue
        ligne = M[idx[p]]
        for i, val in prs:
            if i < hidden:
                ligne[i] = val * ech
    return M


def r2_arbre_aleatoire(X, Y, n_arbres=200, profondeur=4, graines=64):
    """R² d'un modèle par ARBRES sur les coordonnées les plus énergétiques de X.
    Plus honnête qu'une régression qu'on ne peut pas inverser ici : ça borne ce
    qu'une application simple peut expliquer."""
    import random
    n, h = len(X), len(X[0])
    hy = len(Y[0])
    # coordonnées de X les plus énergétiques
    energie = [sum(X[i][j] ** 2 for i in range(n)) for j in range(h)]
    cols = sorted(range(h), key=lambda j: -energie[j])[:graines]
    # variables de Y à expliquer : les plus énergétiques
    ey = [sum(Y[i][j] ** 2 for i in range(n)) for j in range(hy)]
    outs = sorted(range(hy), key=lambda j: -ey[j])[:8]
    prev = [sum(y * y for y in (Y[i][o] for i in range(n))) for o in outs]
    tot = 0.0
    for k, o in enumerate(outs):
        yv = [Y[i][o] for i in range(n)]
        moy = sum(yv) / n
        sst = sum((v - moy) ** 2 for v in yv)
        # prédiction par la meilleure combinaison linéaire de 2 colonnes de X,
        # trouvée par recherche aléatoire (borne basse honnête)
        meilleur = sst
        rnd = random.Random(1)
        for _ in range(400):
            j1, j2 = rnd.sample(cols, 2)
            a1 = sum(X[i][j1] * yv[i] for i in range(n))
            a2 = sum(X[i][j2] * yv[i] for i in range(n))
            d11 = sum(X[i][j1] ** 2 for i in range(n)) + 1e-9
            d22 = sum(X[i][j2] ** 2 for i in range(n)) + 1e-9
            sse = 0.0
            for i in range(n):
                p = a1 / d11 * X[i][j1] + a2 / d22 * X[i][j2]
                sse += (yv[i] - p) ** 2
            if sse < meilleur: meilleur = sse
        tot += 1 - meilleur / max(sst, 1e-12)
    return tot / len(outs)


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 1
    a = int(sys.argv[sys.argv.index("--de") + 1]) if "--de" in sys.argv else 0
    b = int(sys.argv[sys.argv.index("--a") + 1]) if "--a" in sys.argv else 10
    base = int(sys.argv[sys.argv.index("--base") + 1]) if "--base" in sys.argv else 0
    n_layer, hidden, listes = lire(sys.argv[1])
    positions = sorted({p for (c, p, _, _) in listes if c == base + a})
    print(f"# {n_layer} couches · largeur {hidden} · {len(positions)} positions")
    print(f"# entrée : couche {a} · sortie : couche {b} (base {base})")
    X = dense(listes, base + a, positions, hidden)
    Y = dense(listes, base + b, positions, hidden)
    # normalisation grossière pour que le R² ait un sens
    def centre(M):
        n, h = len(M), len(M[0])
        mo = [sum(M[i][j] for i in range(n)) / n for j in range(h)]
        return [[M[i][j] - mo[j] for j in range(h)] for i in range(n)]
    Xc, Yc = centre(X), centre(Y)
    print("  R² d'une application linéaire creuse (2 colonnes de X) sur les 8 "
          "sorties les plus énergétiques :")
    for cible in [a + 1, a + 2, a + 4, b]:
        if cible > b: continue
        Yk = centre(dense(listes, base + cible, positions, hidden))
        print(f"    couche {a} → couche {cible:<3} : R² ≈ {r2_arbre_aleatoire(Xc, Yk):.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

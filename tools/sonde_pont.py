#!/usr/bin/env python3
"""sonde_pont.py — le pont garde-t-il l'information PRÉDICTIVE du professeur ?

La réserve du rapport : le pont est PLUS invariant que le professeur, mais il peut
obtenir cette invariance en **jetant** de l'information propre à la langue — et
cette information peut servir en aval. Le dire ne suffit pas, il faut le mesurer.

**Sonde** : depuis l'état au jeton t, prédire la **plongée du jeton t+1** (couche 0
à t+1). Une régression linéaire, ajustée sur les langues d'entraînement, testée sur
les langues tenues à l'écart. On compare trois états :

  - le professeur (couche L du gros modèle) ;
  - le pont (notre artefact) ;
  - la plongée du jeton courant seule (témoin bas).

Si la sonde depuis le pont vaut celle depuis le professeur, le pont a gardé ce qui
sert à prédire la suite — et son invariance n'est pas obtenue en jetant l'utile.

Usage : sonde_pont.py <dossier_train> <dossier_test> <pont.npz> [--couche 10]
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
        assert f.read(4) == b"DRVF"
        version, = struct.unpack("<H", f.read(2))
        n_layer, hidden = struct.unpack("<II", f.read(8))
        pp = {}
        while True:
            b = f.read(2)
            if len(b) < 2: break
            c, = struct.unpack("<H", b)
            if c == 0xFFFF: break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            pp[(c, pos)] = paires(f, n, version)
    return hidden, pp


def mat(pp, c, hidden):
    positions = sorted(p for (cc, p) in pp if cc == c)
    M = np.zeros((len(positions), hidden), dtype=np.float64)
    for k, p in enumerate(positions):
        for i, v in pp[(c, p)]:
            if i < hidden: M[k, i] = v
    return M


def ajuste(X, Y, lam=1e-2):
    return np.linalg.solve(X.T @ X + lam * len(X) * np.eye(X.shape[1]), X.T @ Y)


def r2(X, W, Y):
    P = X @ W
    sse = ((Y - P) ** 2).sum()
    sst = ((Y - Y.mean(axis=0)) ** 2).sum()
    return 1.0 - sse / max(sst, 1e-12)


def main():
    dtr, dte, pont = sys.argv[1], sys.argv[2], sys.argv[3]
    c = int(sys.argv[sys.argv.index("--couche") + 1]) if "--couche" in sys.argv else 10
    a = np.load(pont, allow_pickle=True)
    P, moy, W0 = a["P"], a["moy"], a["W0"]

    def charge(d):
        out = {}
        for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
            hidden, pp = lire(f)
            out[os.path.basename(f)[:-5]] = pp
        return out

    tr, te = charge(dtr), charge(dte)

    def paires_etat(d):
        Xe, Xp, Xb, Y = [], [], [], []
        for l, pp in d.items():
            E = mat(pp, 0, 896)
            T = mat(pp, c, 896)
            B = (E @ W0) @ P.T + moy
            for t in range(len(E) - 1):
                Xe.append(E[t]); Xp.append(T[t]); Xb.append(B[t]); Y.append(E[t + 1])
        return (np.array(Xe), np.array(Xp), np.array(Xb), np.array(Y))

    Etr, Ptr, Btr, Ytr = paires_etat(tr)
    Ete, Pte, Bte, Yte = paires_etat(te)
    Wp = ajuste(Ptr, Ytr); Wb = ajuste(Btr, Ytr); We = ajuste(Etr, Ytr)
    print(f"# entraînement {len(Etr)} pas · test {len(Ete)} pas · cible : la plongée du jeton SUIVANT")
    print(f"{'état utilisé comme entrée':<44} {'R² entr.':>10} {'R² test':>10}")
    for nom, W, Xa, Xb_ in (("professeur (couche %d du gros modèle)" % c, Wp, Ptr, Pte),
                            ("PONT (notre artefact)", Wb, Btr, Bte),
                            ("témoin bas : plongée du jeton courant", We, Etr, Ete)):
        print(f"{nom:<44} {r2(Xa, W, Ytr):>10.4f} {r2(Xb_, W, Yte):>10.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

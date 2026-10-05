#!/usr/bin/env python3
"""pont_fidele.py — émuler le professeur LE PLUS FIDÈLEMENT POSSIBLE, à moindre coût.

Correction d'une faute de mesure : `pont_recurrent.py` comparait la fidélité DANS
LE SOUS-ESPACE du rang courant. Comparer un rang 1 et un rang 64 ainsi revient à
comparer deux espaces différents — les chiffres ne sont pas comparables, et c'est
ce qui faisait « baisser » la fidélité quand on ajoutait des neurones.

Ici tout est mesuré **dans l'espace complet de 896 canaux**, contre la sortie
réelle du professeur. Les modèles sont comparés à coût égal et à coût libre :

  - LINÉAIRE de rang r        : y = (e·U)·Vᵀ + moy            (r neurones)
  - DEUX COUCHES (ELM)        : y = tanh(e·R)·W              (H neurones cachés)
    R est ALÉATOIRE et GELÉ ; seul W s'ajuste, par moindres carrés — aucune
    rétropropagation, et R n'a pas besoin d'être distribué de la même façon que W.

Usage : pont_fidele.py <dossier_train> <dossier_test> [--couche 10]
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


def mats(pp, c, hidden):
    """Rend (plongées, cibles) — deux matrices n_positions × hidden."""
    pos = sorted(p for (cc, p) in pp if cc in (0, c))
    E, Y = [], []
    for p in sorted(p for (cc, p) in pp if cc == 0):
        e = np.zeros(hidden); 
        for i, v in pp[(0, p)]:
            if i < hidden: e[i] = v
        y = np.zeros(hidden)
        for i, v in pp.get((c, p), []):
            if i < hidden: y[i] = v
        E.append(e); Y.append(y)
    return np.array(E), np.array(Y)


def charge(d, c, hidden):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
        h, pp = lire(f)
        out[os.path.basename(f)[:-5]] = mats(pp, c, h)
    return out


def cos_lignes(A, B):
    na = np.linalg.norm(A, axis=1); nb = np.linalg.norm(B, axis=1)
    ok = (na > 0) & (nb > 0)
    return float(np.mean(np.sum(A[ok] * B[ok], axis=1) / (na[ok] * nb[ok])))


def inv(V):
    n = np.linalg.norm(V, axis=1, keepdims=True); n[n == 0] = 1
    S = (V / n) @ (V / n).T
    iu = np.triu_indices(len(V), 1)
    return float(S[iu].mean()), float(S[iu].min())


def main():
    dtr, dte = sys.argv[1], sys.argv[2]
    c = int(sys.argv[sys.argv.index("--couche") + 1]) if "--couche" in sys.argv else 10
    tr, te = charge(dtr, c, 896), charge(dte, c, 896)
    Etr = np.vstack([e for e, _ in tr.values()]); Ytr = np.vstack([y for _, y in tr.values()])
    Ete = np.vstack([e for e, _ in te.values()]); Yte = np.vstack([y for _, y in te.values()])
    mt = Ytr.mean(axis=0)
    print(f"# professeur : couche {c} · {Etr.shape[0]} pas d'entraînement · {Ete.shape[0]} de test")
    print(f"# fidélité mesurée DANS L'ESPACE COMPLET (896 canaux), contre la sortie réelle")
    print(f"\n{'modèle':<34} {'fid. train':>11} {'fid. TEST':>11} {'params':>10} {'invariance':>11}")
    moy_tr = np.tile(mt, (len(Etr), 1))
    print(f"{'constante (sortie moyenne)':<34} {cos_lignes(moy_tr, Ytr):>11.4f} "
          f"{cos_lignes(np.tile(mt, (len(Ete), 1)), Yte):>11.4f} {896:>10} "
          f"{inv(Yte)[0]:>11.4f}")

    # --- LINÉAIRE de rang r (r neurones)
    U, S, Vt = np.linalg.svd(Ytr - mt, full_matrices=False)
    for r in (1, 2, 4, 8, 16, 32, 64, 128):
        P = Vt[:r].T
        Z = (Ytr - mt) @ P
        W = np.linalg.solve(Etr.T @ Etr + 1e-2 * len(Etr) * np.eye(896), Etr.T @ Z)
        ftr = cos_lignes((Etr @ W) @ P.T + mt, Ytr)
        fte = cos_lignes((Ete @ W) @ P.T + mt, Yte)
        print(f"{'linéaire, ' + str(r) + ' neurone(s)':<34} {ftr:>11.4f} {fte:>11.4f} "
              f"{896 * r + 896:>10} {inv((Ete @ W) @ P.T + mt)[0]:>11.4f}")

    # --- DEUX COUCHES : projection aléatoire GELÉE + non-linéarité + lecture LS
    for H in (64, 256, 1024, 4096):
        R = np.random.RandomState(11).randn(896, H) / np.sqrt(896)
        Atr = np.tanh(Etr @ R); Ate = np.tanh(Ete @ R)
        W = np.linalg.solve(Atr.T @ Atr + 1e-1 * len(Atr) * np.eye(H), Atr.T @ (Ytr - mt))
        ftr = cos_lignes(Atr @ W + mt, Ytr)
        fte = cos_lignes(Ate @ W + mt, Yte)
        print(f"{'2 couches, ' + str(H) + ' cachés (ELM)':<34} {ftr:>11.4f} {fte:>11.4f} "
              f"{896 * H + H * 896:>10} {inv(Ate @ W + mt)[0]:>11.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

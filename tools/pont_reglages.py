#!/usr/bin/env python3
"""pont_reglages.py — où est la marge du pont récurrent ?

`pont_reservoir.py` a établi le résultat, mais avec QUATRE réglages figés sans
justification : fuite a = 0,5, rayon spectral 0,9, ride 1e-1, graine 5, et UN
SEUL tirage du réservoir. Ce tool balaie ces leviers et dit lesquels paient.

Rien ne se rétropropage : A et B restent aléatoires et gelés, seule la lecture W
s'ajuste par moindres carrés. Un ensemble de K réservoirs reste distribuable —
chaque nœud tire les mêmes A/B de la même graine.

Usage : pont_reglages.py <train.npz> <test.npz> [--levier fuite|rayon|neurones|ensemble|saut|tous]
"""
import sys
import numpy as np


def charge(p):
    z = np.load(p, allow_pickle=True)
    cles = [str(c) for c in z["cles"]]
    return cles, [z[f"E{i}"] for i in range(len(cles))], [z[f"Y{i}"] for i in range(len(cles))], int(z["hidden"])


def cos_lignes(A, B):
    na = np.linalg.norm(A, axis=1); nb = np.linalg.norm(B, axis=1)
    ok = (na > 0) & (nb > 0)
    return float(np.mean(np.sum(A[ok]*B[ok], axis=1)/(na[ok]*nb[ok])))


def inv(V):
    n = np.linalg.norm(V, axis=1, keepdims=True); n[n == 0] = 1
    S = (V/n) @ (V/n).T
    iu = np.triu_indices(len(V), 1)
    return float(S[iu].mean()), float(S[iu].min())


def tirer(N, H, rayon, graine):
    rng = np.random.RandomState(graine)
    A = rng.randn(N, N) / np.sqrt(N)
    A *= rayon / max(abs(np.linalg.eigvals(A)))
    B = rng.randn(N, H) / np.sqrt(H)
    return A, B


def etats(E, A, B, a):
    """s_t = (1-a)s_(t-1) + a·tanh(A s_(t-1) + B e_t) — A, B GELÉS."""
    N = A.shape[0]
    out = np.zeros((len(E), N), dtype=np.float32)
    s = np.zeros(N)
    for t in range(len(E)):
        s = (1-a)*s + a*np.tanh(A @ s + B @ E[t])
        out[t] = s
    return out


def ajuste(X, Y, mt, ride=1e-1):
    W = np.linalg.solve(X.T @ X + ride*len(X)*np.eye(X.shape[1]), X.T @ (Y - mt))
    return W


def essai(tr, te, N=64, a=0.5, rayon=0.9, graine=5, K=1, saut=False, ride=1e-1):
    cltr, Etr, Ytr, H = tr
    clte, Ete, Yte, _ = te
    mt = np.vstack(Ytr).mean(axis=0)
    Xtr, Xte = [], []
    for k in range(K):
        A, B = tirer(N, H, rayon, graine + k)
        for E, acc in ((Etr, Xtr), (Ete, Xte)):
            S = [etats(e, A, B, a) for e in E]
            acc.append(S)
    # K réservoirs = K blocs de colonnes (les jetons restent les lignes) : un
    # ensemble ne change pas le nombre de pas, il élargit la lecture.
    def monte(listes, E):
        cols = [np.vstack([x for x in S]) for S in listes]
        if saut: cols.append(np.vstack(E))
        return np.hstack(cols)
    Xtr_m = monte(Xtr, Etr)
    Xte_m = monte(Xte, Ete)
    Ytr_m = np.vstack(Ytr); Yte_m = np.vstack(Yte)
    W = ajuste(Xtr_m, Ytr_m, mt, ride)
    ftr = cos_lignes(Xtr_m @ W + mt, Ytr_m)
    fte = cos_lignes(Xte_m @ W + mt, Yte_m)
    # invariance : dernier état de chaque langue de test
    dernier = []
    for i in range(len(clte)):
        St = np.hstack([S[i] for S in Xte])   # K blocs de colonnes, comme la lecture
        if saut:
            St = np.hstack([St, Ete[i]])
        dernier.append((St @ W + mt)[-1])
    m, mi = inv(np.array(dernier))
    base = cos_lignes(np.tile(mt, (len(Yte_m), 1)), Yte_m)
    return ftr, fte, m, mi, base, Xtr_m.shape[1]


def main():
    tr = charge(sys.argv[1]); te = charge(sys.argv[2])
    levier = sys.argv[sys.argv.index("--levier") + 1] if "--levier" in sys.argv else "tous"
    cltr, Etr, Ytr, H = tr
    print(f"# entraînement {sum(len(e) for e in Etr)} pas · test {sum(len(e) for e in te[1])} pas")
    ref = essai(tr, te, N=64, a=0.5, rayon=0.9, graine=5)
    print(f"\n{'réglage':<40} {'fid train':>10} {'fid TEST':>10} {'invar.':>8} {'pire':>7} {'dim':>6}")
    print(f"{'RÉFÉRENCE (a=0,5 rayon=0,9 graine=5)':<40} {ref[0]:>10.4f} {ref[1]:>10.4f} "
          f"{ref[2]:>8.4f} {ref[3]:>7.4f} {ref[5]:>6}")
    print(f"{'  constante (témoin)':<40} {'—':>10} {ref[4]:>10.4f} {inv(np.vstack(te[2]))[0]:>8.4f}")
    grilles = {
        "fuite":   [("a=0,05", dict(a=0.05)), ("a=0,1", dict(a=0.1)), ("a=0,2", dict(a=0.2)),
                    ("a=0,35", dict(a=0.35)), ("a=0,7", dict(a=0.7)), ("a=0,85", dict(a=0.85))],
        "rayon":   [("rayon=0,7", dict(rayon=0.7)), ("rayon=0,98", dict(rayon=0.98)), ("rayon=1,05", dict(rayon=1.05)), ("rayon=1,2", dict(rayon=1.2))],
        "neurones":[("N=8", dict(N=8)), ("N=16", dict(N=16)), ("N=32", dict(N=32)),
                    ("N=128", dict(N=128)), ("N=256", dict(N=256))],
        "ensemble":[("ensemble K=2", dict(K=2)), ("ensemble K=4", dict(K=4)), ("ensemble K=8", dict(K=8))],
        "saut":    [("saut (e_t dans la régression)", dict(saut=True)),
                    ("N=32 saut", dict(N=32, saut=True)),
                    ("a=0,2 N=32 saut", dict(a=0.2, N=32, saut=True)),
                    ("a=0,2 saut", dict(a=0.2, saut=True)),
                    ("a=0,2 N=32", dict(a=0.2, N=32))],
        "combine": [("a=0,2 ride=0,3", dict(a=0.2, ride=0.3)),
                    ("a=0,2 ride=1,0", dict(a=0.2, ride=1.0)),
                    ("a=0,2 N=32 ride=1,0", dict(a=0.2, N=32, ride=1.0)),
                    ("a=0,2 N=16 ride=1,0", dict(a=0.2, N=16, ride=1.0)),
                    ("a=0,2 K=2 ride=1,0", dict(a=0.2, K=2, ride=1.0)),
                    ("a=0,35 ride=1,0", dict(a=0.35, ride=1.0)),
                    ("a=0,2 N=128 ride=1,0", dict(a=0.2, N=128, ride=1.0))],
        "ride":    [("ride 1e-3", dict(ride=1e-3)), ("ride 1e-2", dict(ride=1e-2)), ("ride 1,0", dict(ride=1.0)), ("ride 10", dict(ride=10.0))],
    }
    for cle, liste in grilles.items():
        if levier not in ("tous", cle): continue
        for nom, kw in liste:
            ftr, fte, m, mi, base, dim = essai(tr, te, **kw)
            print(f"{nom:<40} {ftr:>10.4f} {fte:>10.4f} {m:>8.4f} {mi:>7.4f} {dim:>6}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

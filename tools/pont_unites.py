#!/usr/bin/env python3
"""pont_unites.py — notre pont, mesuré PAR UNITÉ.

Pendant de `invariance_unites.py`, qui mesure le professeur. Ici on entraîne le
pont sur les unités des langues d'apprentissage, on le transporte sur les langues
tenues à l'écart, et on mesure :

  - la fidélité (le pont contre la couche du professeur) ;
  - l'invariance PAR UNITÉ de notre sortie : pour chaque unité k, la similarité
    entre les langues, à contenu égal — dix points de mesure au lieu d'un ;
  - la même chose pour le professeur, sur le même panel, pour référence ;
  - le diagnostic oracle, sur les deux panneaux.

Les entrées des caches doivent être nommées `<langue>_<k>` (c'est ce que produit
le traçage par unité).

Usage : pont_unites.py <train.npz> <test.npz> [--canaux 0.5] [--lecture quadratique]
"""
import sys
import numpy as np
sys.path.insert(0, "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools")
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402


def inv_par_unite(noms, Xs):
    """Pour chaque unité, la similarité entre langues de la DERNIÈRE position."""
    par = {}
    for nom, X in zip(noms, Xs):
        L, _, k = nom.rpartition("_")
        par.setdefault(k, {})[L] = X[-1]
    res = []
    for k in sorted(par):
        noms_k = sorted(par[k])
        if len(noms_k) < 2:
            continue
        V = np.array([par[k][L] for L in noms_k])
        N = np.linalg.norm(V, axis=1, keepdims=True); N[N == 0] = 1
        S = (V/N) @ (V/N).T
        iu = np.triu_indices(len(noms_k), 1)
        j = int(np.argmin(S[iu]))
        res.append((k, len(noms_k), float(S[iu].mean()), float(S[iu].min()),
                    f"{noms_k[iu[0][j]]}–{noms_k[iu[1][j]]}"))
    return res


def main():
    pa, pb = sys.argv[1], sys.argv[2]
    part = float(sys.argv[sys.argv.index("--canaux")+1]) if "--canaux" in sys.argv else 0.0
    a_ = float(sys.argv[sys.argv.index("--a")+1]) if "--a" in sys.argv else 0.5
    ride = float(sys.argv[sys.argv.index("--ride")+1]) if "--ride" in sys.argv else 1.0
    graine = int(sys.argv[sys.argv.index("--graine")+1]) if "--graine" in sys.argv else 5
    quad = "--lecture" in sys.argv and sys.argv[sys.argv.index("--lecture")+1] == "quadratique"

    clA, EA, YA, H = charge(pa)
    clB, EB, YB, _ = charge(pb)
    if part > 0.0:
        E = np.vstack([y**2 for y in YA]).sum(0); o = np.argsort(-E)
        c = np.cumsum(E[o])/E.sum(); g = np.sort(o[:int(np.searchsorted(c, part)+1)])
        YA = [y[:, g] for y in YA]; YB = [y[:, g] for y in YB]
        print(f"# sous-ensemble actif : {len(g)}/{H} canaux, masque lu sur l'apprentissage")

    # langues distinctes pour découper apprentissage / validation
    def langue(n): return n.rpartition("_")[0]
    langsA = sorted({langue(n) for n in clA})
    n_val = max(2, len(langsA)//10)
    val = set(langsA[:n_val])
    itr = [i for i, n in enumerate(clA) if langue(n) not in val]
    ival = [i for i, n in enumerate(clA) if langue(n) in val]
    print(f"# {len(langsA)} langues d'apprentissage · {len(itr)} unités apprises · "
          f"{len(ival)} en validation · {len(clB)} unités de test")

    P = Pont((clA, EA, YA), a_, graine, H)
    P.quadratique = quad
    mt = np.vstack([YA[i] for i in itr]).mean(0)
    val_max, sans_gain, patience, gain_min = -1.0, 0, 8, 0.0005
    while P.compte_neurones < 120:
        P.nait(1, nouvelle_couche=(P.compte_neurones == 0))
        idx = np.arange(P.compte_neurones)
        f = P.fid(idx, P.ajuste(idx, ride, mt, itr), mt, ival)
        if f > val_max + gain_min:
            val_max, sans_gain = f, 0
        else:
            sans_gain += 1
            if sans_gain >= patience:
                break
    idx = np.arange(P.compte_neurones)
    W = P.ajuste(idx, ride, mt, itr)
    fA = P.fid(idx, W, mt, ival)

    Xb = P.recalcule(idx, EB)
    fB = P.evalue(Xb, YB, W, mt)
    A_ = P.phi(np.vstack(Xb)); B_ = np.vstack(YB)
    Wo = np.linalg.solve(A_.T @ A_ + ride*len(A_)*np.eye(A_.shape[1]), A_.T @ (B_ - mt))
    oracle = cos_lignes(A_ @ Wo + mt, B_)

    print(f"\n# PONT : {P.compte_neurones} neurones · {len(P.couches)} couches {P.couches}")
    print(f"#   fidélité validation   : {fA:.4f}")
    print(f"#   fidélité TEST         : {fB:.4f}")
    print(f"#   oracle TEST           : {oracle:.4f}   (écart {oracle-fB:+.4f})")
    inv_m, inv_min = P.invariance(Xb, W, mt)     # UN seul calcul, pas deux
    print(f"#   invariance TEST       : {inv_m:.4f} · pire {inv_min:.4f}")

    print(f"\n# INVARIANCE PAR UNITÉ — professeur contre notre sortie")
    print(f"{'unité':>6} {'langues':>8} {'professeur':>11} {'notre sortie':>13} "
          f"{'pire (nous)':>12}   pire couple")
    pr = {k: (m, mi, c) for k, _, m, mi, c in inv_par_unite(clB, YB)}
    no = {k: (m, mi, c) for k, _, m, mi, c in
          inv_par_unite(clB, [P.phi(x) @ W + mt for x in Xb])}
    for k in sorted(pr):
        m, mi, c = pr[k]
        if k in no:
            mn, mino, cn = no[k]
            print(f"{k:>6} {len(clB)//max(len(pr),1):>8} {m:>11.4f} {mn:>13.4f} "
                  f"{mino:>12.4f}   {cn}")
    if pr and no:
        print(f"\nMOYENNE professeur {np.mean([v[0] for v in pr.values()]):.4f} · "
              f"notre sortie {np.mean([v[0] for v in no.values()]):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

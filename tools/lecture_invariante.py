#!/usr/bin/env python3
"""lecture_invariante.py — ajuster la lecture SOUS CONTRAINTE d'invariance.

MESURÉ AU §47 : dans la croissance, fidélité et invariance tirent en sens opposé —
de 8 à 179 neurones, +0,0185 de fidélité pour −0,0776 d'invariance et −0,1805 de
pire paire. Ce n'est pas un accident : la lecture est ajustée pour reproduire le
professeur, qui garde lui-même beaucoup de structure propre aux langues.

L'ajustement ordinaire minimise ‖XW − Y‖² SEUL. Il ignore l'invariance. Or la
pénalité manquante reste QUADRATIQUE en W :

    P(W) = Σ_i n_i ‖m_i − m̄‖²        (variance INTER-LANGUE de la sortie)

donc l'objectif total `‖XW − Y‖² + μ·P(W)` a toujours une solution en FORME FERMÉE :

    (XᵀX + μ·C + ride·I) W = Xᵀ(Y − mt),   C = Σ_i n_i (M_i − M̄)ᵀ(M_i − M̄)

On ne change pas d'algorithme, on change d'OBJECTIF.

PRÉDICTION, ÉCRITE AVANT LA MESURE : pénaliser doit faire monter l'invariance et
baisser la fidélité. Le point intéressant n'est pas « est-ce que ça marche » mais
**le TAUX D'ÉCHANGE** : si l'invariance gagne beaucoup pour peu de fidélité, le
curseur est un vrai levier ; si les deux se dégradent ensemble, l'objectif était déjà
au mieux.

Usage : lecture_invariante.py <cache_appr.npz> <cache_test.npz> [--neur 40]
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def inv_last(V):
    """Invariance inter-langue et pire paire, sur la DERNIÈRE position."""
    N = V/np.maximum(np.linalg.norm(V, axis=1, keepdims=True), 1e-12)
    S = N @ N.T
    iu = np.triu_indices(len(V), 1)
    return float(S[iu].mean()), float(S[iu].min())


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 40))
    part = float(opt("--part", 0.5))
    ride, graine = 0.03, 5
    mus = [float(x) for x in opt("--mus", "0,0.001,0.003,0.01,0.03,0.1,0.3,1").split(",")]

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]
    itr = np.arange(len(cltr))
    ival = itr[::7]
    iap = np.array([i for i in itr if i not in set(ival.tolist())])
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)
    print(f"# {len(garde)} canaux · {len(iap)} ajustement · {len(ival)} validation "
          f"· {len(clte)} test")

    t = time.time()
    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s), "
          f"construit en {time.time()-t:.0f} s")

    Xv = P.recalcule(idx, [Etr[i] for i in ival])
    Yv = [Ytr[i] for i in ival]
    Xt = P.recalcule(idx, Ete)
    pro = np.array([Yte[k][-1] for k in range(len(clte))])
    ip, pp = inv_last(pro)
    print(f"# INVARIANCE DU PROFESSEUR : {ip:.4f} · pire paire {pp:.4f}")

    print(f"\n# {'mu':>7}{'fid VAL':>10}{'fid TEST':>10}{'INVARIANCE':>12}"
          f"{'pire paire':>12}{'vs mu=0':>10}")
    base = None
    for mu in mus:
        P.mu_inv = mu
        W = P.ajuste(idx, ride, mt, iap)
        fv = cos_lignes(P.phi(np.vstack(Xv)) @ W + mt, np.vstack(Yv))
        ft = cos_lignes(P.phi(np.vstack(Xt)) @ W + mt, np.vstack(Yte))
        nos = np.array([(P.phi(P._norm(Xt[k])) @ W + mt)[-1]
                        for k in range(len(clte))])
        iv, pv = inv_last(nos)
        if base is None:
            base = (fv, ft, iv, pv)
        print(f" {mu:>7.3f}{fv:>10.4f}{ft:>10.4f}{iv:>12.4f}{pv:>12.4f}"
              f"{iv-base[2]:>+10.4f}")
    P.mu_inv = 0.0
    print(f"\n# PRÉDICTION : l'invariance doit MONTER et la fidélité BAISSER.")
    print(f"# Le taux d'échange se lit entre mu=0 et le point où le gain d'invariance")
    print(f"# cesse de valoir sa perte de fidélité.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

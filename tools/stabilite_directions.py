#!/usr/bin/env python3
"""stabilite_directions.py — les directions du discriminant viennent-elles des DONNÉES ou du TIRAGE ?

LA QUESTION. Le §92 montre qu'un discriminant de rang 2 appris sur nos sorties sépare le
contenu de la langue mieux que le professeur sur dix des quinze paires. Mais **nos sorties
dépendent d'un tirage aléatoire gelé** : `P` et `B` sont tirés avec `np.random.RandomState(5)`.
La question est donc :

> **L'axe contenu/langue que le discriminant trouve est-il une propriété de la structure
> exposée par le professeur, ou une propriété de NOTRE tirage ?**

Si deux graines différentes donnent des sous-espaces très différents, alors « la direction du
contenu » n'existe pas dans notre représentation — elle est fabriquée par le tirage, et le
résultat du §92 ne se reproduirait pas avec une autre graine.

CE QUI EST MESURÉ. Pour chaque graine, on apprend le pont, on lit les sorties, on apprend le
discriminant, et on garde le sous-espace `V_r` de ses `r` premiers axes. Puis on mesure les
**angles principaux** entre les sous-espaces deux à deux :

    V_iᵀ V_j = U Σ Wᵀ      σ_k = cos(θ_k)

Un écart de 0° signifie « même sous-espace » ; 90° signifie « orthogonal ». Comme le
discriminant est défini au signe près et que le sous-espace est de dimension r, ce sont les
angles qui comptent, pas les vecteurs.

RÉSERVE. `C_lang` est de rang au plus `n_langues − 1` et on la régularise : les axes au-delà
des premiers sont mal déterminés **par construction**. C'est pourquoi on regarde r = 2 (le
rang utile sur 3 langues, et l'optimum constaté partout) et r = 5.

Usage : stabilite_directions.py <appr.npz> <disc.npz> <eval.npz>
                               [--graines 5,6,7,8,9,10] [--neur 120] [--rangs 2,5]
"""
import os
import sys
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def decompose(noms, M):
    m = M.mean(0)
    par_l, par_c = {}, {}
    for i, n in enumerate(noms):
        L, _, k = n.partition("_")
        par_l.setdefault(L, []).append(i)
        par_c.setdefault(k, []).append(i)
    comm = [k for k, idx in par_c.items() if len(idx) == len(par_l)]
    Pl = float(np.mean([np.sum((M[idx].mean(0) - m)**2) for idx in par_l.values()]))
    Pc = float(np.mean([np.sum((M[par_c[k]].mean(0) - m)**2) for k in comm]))
    return Pl, Pc, Pc/max(Pl, 1e-12)


def moyennes_sortie(P, idx, W, mt, E):
    X = P.recalcule(idx, E)
    return np.vstack([(P.phi(P._norm(X[k])) @ W + mt).mean(0) for k in range(len(E))])


def angles(Va, Vb):
    """Angles principaux entre deux sous-espaces orthonormés, en degrés."""
    s = np.linalg.svd(Va.T @ Vb, compute_uv=False)
    s = np.clip(s, -1.0, 1.0)
    return np.degrees(np.arccos(s))


def main():
    tr_p, disc_p, te_p = sys.argv[1], sys.argv[2], sys.argv[3]
    graines = [int(x) for x in opt("--graines", "5,6,7,8,9,10").split(",")]
    n_neur = int(opt("--neur", 120))
    rangs = [int(x) for x in opt("--rangs", "2,5").split(",")]

    cltr, Etr, Ytr, _ = charge(tr_p)
    cldi, Edi, Ydi, _ = charge(disc_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= 0.5)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Ydi = [y[:, garde] for y in Ydi]
    Yte = [y[:, garde] for y in Yte]
    ncan = len(garde)
    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)
    pro_te = np.vstack([y.mean(0) for y in Yte])
    rp = decompose(clte, pro_te)
    print(f"# {len(cltr)} entrées d'apprentissage · {len(cldi)} pour le discriminant"
          f" · {len(clte)} de test · {ncan} canaux · {len(graines)} graines")

    # le panel du discriminant, mis en groupes une fois
    pc, pl = {}, {}
    for i, n in enumerate(cldi):
        L, _, k = n.partition("_")
        pl.setdefault(L, []).append(i)
        pc.setdefault(k, []).append(i)
    comm = [k for k, v in pc.items() if len(v) == len(pl)]

    sous, rap = {}, {}
    for g in graines:
        P = Pont((cltr, Etr, Ytr), 0.2, g, ncan)
        P.quadratique = True
        P.a_min, P.a_max = 0.02, 0.8
        P.nait(n_neur, True)
        idx = np.arange(P.compte_neurones)
        W = P.ajuste(idx, 0.03, mt, itr)
        Mdi = moyennes_sortie(P, idx, W, mt, Edi)
        mdi = Mdi.mean(0)

        def covg(par):
            C = np.zeros((ncan, ncan))
            for v in par.values():
                d = Mdi[v].mean(0) - mdi
                C += np.outer(d, d)
            return C/max(len(par), 1)

        Cc = covg({k: pc[k] for k in comm})
        Cl = covg(pl)
        lam = max(1e-2*np.trace(Cl)/ncan, 1e-12)
        w, V = np.linalg.eigh(np.linalg.solve(Cl + lam*np.eye(ncan), Cc))
        V = V[:, np.argsort(-w)]
        Mte = moyennes_sortie(P, idx, W, mt, Ete)
        d = decompose(clte, Mte)
        rap[g] = (d[2], d[2]/rp[2], w[-1])
        sous[g] = {r: V[:, :r] for r in rangs}
        # LE CHIFFRE QUI COMPTE : le rapport APRÈS projection, graine par graine. Si
        # les sous-espaces tournent d'une graine à l'autre, le gain du discriminant
        # tourne avec eux — et le résultat du §92 serait un artefact de graine.
        proj = {}
        for r in rangs:
            Vr = V[:, :r]
            Mp = (Mte - mdi) @ Vr @ Vr.T + mdi
            dd = decompose(clte, Mp)
            proj[r] = dd[2]
        rap[g] = (d[2], d[2]/rp[2], w[-1], proj)
        ligne = " · ".join(f"rang {r} {proj[r]:>7.3f} ({proj[r]/rp[2]:>6.1%})"
                           for r in rangs)
        print(f"  graine {g:>3} : rapport {d[2]:>7.3f} ({d[2]/rp[2]:>5.1%})"
              f" · λ₁ {w[-1]:>9.1f} · APRÈS PROJECTION {ligne}", flush=True)

    print(f"\n# ANGLES PRINCIPAUX entre les sous-espaces des différentes graines")
    for r in rangs:
        tous = []
        for a, b in combinations(graines, 2):
            an = angles(sous[a][r], sous[b][r])
            tous.append(an)
        T = np.array(tous)
        print(f"  rang {r} : {len(tous)} paires · angle MAXIMAL "
              f"moyen {T[:, -1].mean():>6.1f}° (min {T[:, -1].min():.1f}°, "
              f"max {T[:, -1].max():.1f}°) · angle 1er axe moyen "
              f"{T[:, 0].mean():>6.1f}°")
    v = np.array([rap[g][0] for g in graines])
    print(f"\n# rapport selon la graine : moyenne {v.mean():.3f} · écart-type {v.std():.3f}"
          f" · min {v.min():.3f} · max {v.max():.3f}")
    for r in rangs:
        pv = np.array([rap[g][3][r] for g in graines])
        pv = pv/rp[2]
        print(f"# APRÈS PROJECTION rang {r} : moyenne {pv.mean():>7.1%} · "
              f"écart-type {pv.std():>6.1%} · min {pv.min():>7.1%} · "
              f"max {pv.max():>7.1%} · étalement ×{pv.max()/max(pv.min(),1e-9):.2f}")
    print(f"# professeur {rp[2]:.3f} · part moyenne "
          f"{np.mean([rap[g][1] for g in graines]):.1%}")
    print(f"\n# Lecture : un angle MAXIMAL proche de 90° signifie que les sous-espaces")
    print(f"# n'ont plus rien en commun — la « direction du contenu » serait alors une")
    print(f"# propriété du TIRAGE et non des données. Proche de 0°, elle est dans les")
    print(f"# données. Le 1er axe est plus stable que le second : c'est attendu, et")
    print(f"# c'est le second qui décide de la séparation fine.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

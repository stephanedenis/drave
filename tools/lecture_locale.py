#!/usr/bin/env python3
"""LECTURE LOCALE — remplacer le fit global par une règle de corrélation.

POURQUOI CETTE EXPÉRIENCE. Le mode matriciel n'est pas dans la simulation des
neurones : il est dans la LECTURE. Mesuré (§35) :
  - construire le réservoir : 24 µs par pas, 0,4 min pour 40 neurones ;
  - ajuster la lecture     : une régression sur 472 472 lignes, coût
    O(lignes × caractéristiques²) — 22 min à 1 296 colonnes, ~80 min à 2 496.
La contrainte « pas de rétropropagation » est aujourd'hui satisfaite par une
solution en forme fermée (ridge), et c'est ELLE qui impose la Gram dense.

Or il existe une règle LOCALE, sans rétropropagation, qui converge vers la même
solution : les moindres carrés moyens normalisés (NLMS) —
    W ← W + η·(y_t − W·x_t)·x_tᵀ / ||x_t||²
Chaque pas ne coûte que O(caractéristiques) au lieu de O(caractéristiques²) pour
l'accumulation, et **rien n'est matriciel** : pas de Gram, pas d'inversion, pas de
472 472 lignes en mémoire. C'est exactement la règle « delta », celle que le
neuronspikes décrit quand il fait naître et mourir les connexions par corrélation.

LA QUESTION MESURÉE : cette règle atteint-elle la fidélité du ridge ?
  - si OUI : le mode matriciel disparaît, et avec lui le goulot de 22 minutes ;
  - si NON : on saura combien coûte l'exactitude, et sur quel panneau.

PRÉDICTION, ÉCRITE AVANT LA MESURE : NLMS doit approcher le ridge sur le panneau
d'entraînement mais **transférer moins bien**, parce qu'il converge vers la même
solution en moyenne mais avec une variance qui dépend de l'ordre des exemples — et
l'ordre est ici l'ordre des langues, donc du vivier.

Usage : lecture_locale.py <cache_appr.npz> <cache_test.npz> [--neur 40]
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 40))
    part = float(opt("--part", 0.5))
    graine, ride = 5, 0.03
    etas = [float(x) for x in opt("--etas", "0.01,0.05,0.2,0.5,1.0").split(",")]
    passes = int(opt("--passes", 3))

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
    print(f"# {len(garde)} canaux · {n_neur} neurones · ride {ride} · "
          f"{len(iap)} ajustement / {len(ival)} validation / {len(clte)} test")

    t = time.time()
    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    print(f"# réseau {P.compte_neurones} neurones / {len(P.couches)} couche(s), "
          f"construit en {time.time()-t:.0f} s")

    Aap = P.phi(np.vstack([P.X[i][:, idx] for i in iap]))
    Bap = np.vstack([Ytr[i] for i in iap]) - mt
    Av = P.phi(np.vstack(P.recalcule(idx, [Etr[i] for i in ival])))
    Yv = np.vstack([Ytr[i] for i in ival])
    At = P.phi(np.vstack(P.recalcule(idx, Ete)))
    Yt = np.vstack(Yte)
    Tv = cos_lignes(np.tile(mt, (len(Yv), 1)), Yv)
    Tt = cos_lignes(np.tile(mt, (len(Yt), 1)), Yt)
    nf = Aap.shape[1]

    # ---------------------------------------------------------------- RÉFÉRENCE
    t = time.time()
    Wr = np.linalg.solve(Aap.T @ Aap + ride*len(Aap)*np.eye(nf), Aap.T @ Bap)
    t_ridge = time.time() - t
    print(f"\n=== RIDGE (référence, mode matriciel) ===")
    print(f"#   Gram {nf}×{nf} sur {len(Aap)} lignes · {t_ridge:.1f} s")
    print(f"#   VALID {cos_lignes(Av @ Wr + mt, Yv):.4f} · "
          f"TEST {cos_lignes(At @ Wr + mt, Yt):.4f}")
    fr_v = cos_lignes(Av @ Wr + mt, Yv)
    fr_t = cos_lignes(At @ Wr + mt, Yt)

    # ---------------------------------------------------------------- NLMS
    #
    # SOUS-ÉCHANTILLONNAGE. NLMS est intrinsèquement séquentiel : une ligne à la
    # fois, donc une itération Python par ligne. À 472 472 lignes et 15 passes cela
    # ferait 7 millions d'itérations. On garde une ligne sur `se` — le §35.5 a
    # mesuré que cela coûte 0,0045 de fidélité au ridge, et NLMS compense par des
    # passes supplémentaires sur moins de lignes.
    se = int(opt("--sous-ech", 5))
    courbe = "--courbe" in sys.argv
    W0 = np.zeros((nf, len(garde)))
    print(f"\n=== NLMS (règle LOCALE, sans Gram, sans inversion) ===")
    print(f"# W ← W + η·(y − Wx)·xᵀ/||x||²  ·  {passes} passes · 1 ligne sur {se}")
    if courbe:
        # NLMS est un SOLVEUR ITÉRATIF, pas une solution en forme fermée : une
        # passe ne converge pas (mesuré : 0,2587 contre 0,6233 pour le ridge). La
        # seule question qui compte est donc « combien de passes pour atteindre le
        # ridge, et à quel coût cumulé ». On relève la qualité APRÈS CHAQUE PASSE.
        print(f"# COURBE DE CONVERGENCE — qualité après chaque passe")
        print(f"\n# {'eta':>5}{'passe':>7}{'cumul s':>10}{'VALID':>9}{'TEST':>9}"
              f"{'vs ridge':>10}")
        for eta in etas:
            W = W0.copy()
            t0 = time.time()
            for p in range(1, passes + 1):
                for i in iap:
                    A = P.phi(P.X[i][:, idx])[::se]
                    B = Ytr[i][::se] - mt
                    for k in range(len(A)):
                        x = A[k]
                        nx = eta/(float(x @ x) + 1e-9)
                        e = B[k] - W.T @ x
                        W += nx*np.outer(x, e)
                fv = cos_lignes(Av @ W + mt, Yv)
                ft = cos_lignes(At @ W + mt, Yt)
                print(f" {eta:>5.2f}{p:>7}{time.time()-t0:>10.1f}{fv:>9.4f}"
                      f"{ft:>9.4f}{ft-fr_t:>+10.4f}")
        print(f"\n# RIDGE (référence) : VALID {fr_v:.4f} · TEST {fr_t:.4f} "
              f"en {t_ridge:.1f} s, en UNE fois")
        return 0
    print(f"\n# {'eta':>6}{'passes':>7}{'secondes':>10}{'VALID':>9}{'TEST':>9}"
          f"{'vs ridge TEST':>15}")
    meilleur = None
    for eta in etas:
        W = W0.copy()
        t = time.time()
        for _ in range(passes):
            for i in iap:
                A = P.phi(P.X[i][:, idx])[::se]
                B = Ytr[i][::se] - mt
                for k in range(len(A)):
                    x = A[k]
                    nx = eta/(float(x @ x) + 1e-9)
                    e = B[k] - W.T @ x
                    # W a la forme (caractéristiques, sorties) : l'incrément est
                    # x·eᵀ, PAS e·xᵀ. L'erreur de sens a tué le premier lancement,
                    # et son traceback est parti sur un stderr mal redirigé.
                    W += nx*np.outer(x, e)
        dt = time.time() - t
        fv = cos_lignes(Av @ W + mt, Yv)
        ft = cos_lignes(At @ W + mt, Yt)
        print(f" {eta:>6.2f}{passes:>7}{dt:>10.1f}{fv:>9.4f}{ft:>9.4f}"
              f"{ft-fr_t:>+15.4f}")
        if meilleur is None or ft > meilleur[2]:
            meilleur = (eta, fv, ft, dt)

    print(f"\n# témoins : VALID {Tv:.4f} · TEST {Tt:.4f}")
    print(f"# RIDGE   : VALID {fr_v:.4f} · TEST {fr_t:.4f}   ({t_ridge:.1f} s)")
    eta, fv, ft, dt = meilleur
    print(f"# NLMS    : VALID {fv:.4f} · TEST {ft:.4f}   ({dt:.1f} s, η={eta})")
    print(f"# COÛT    : ridge {t_ridge:.1f} s contre NLMS {dt:.1f} s "
          f"→ rapport {t_ridge/max(dt,1e-9):.1f}×")
    print(f"# QUALITÉ : écart NLMS − ridge sur TEST = {ft-fr_t:+.4f}")
    print(f"\n# PRÉDICTION : NLMS doit approcher sur l'apprentissage et transférer un")
    print(f"# peu moins bien. Si l'écart TEST reste sous 0,005, le mode matriciel")
    print(f"# n'a plus de raison d'être.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

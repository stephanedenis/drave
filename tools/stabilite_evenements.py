#!/usr/bin/env python3
"""STABILITÉ ET ÉVÉNEMENTS — deux questions posées, deux mesures.

QUESTION 1 — OSCILLATION. La récurrence du pont est
    s_t = (1-a)·s_{t-1} + a·tanh(P·s_{t-1} + B·e_t)
avec `P` et `B` aléatoires et GELÉS. Un modèle récursif peut se mettre à osciller
— « épilepsie » — au lieu de se stabiliser en quelques cycles. La question n'est pas
rhétorique : le jacobien du point fixe vaut
    J = (1-a)·I + a·D·P,   D = diag(1 - tanh²)
et son rayon spectral décide. On le mesure sur le `P` réellement utilisé, pour
plusieurs `a`, et on le compare au comportement observé (la norme de l'état
diverge-t-elle ?).

QUESTION 2 — ÉVÉNEMENTS. Une implémentation par événements ne paie que ce qui
CHANGE. Le gain possible se mesure : quelle fraction des neurones bougent
réellement à chaque pas ? Si la plupart sont saturés (tanh ≈ ±1, dérivée ≈ 0), ils
ne produisent aucun événement et le calcul matriciel paie pour rien.

C'est la mesure qui dit si le passage à l'événementiel (ou aux impulsions) est un
gain de 2× ou de 100×.

Usage : stabilite_evenements.py <cache_appr.npz> <cache_test.npz>
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 40))
    part = float(opt("--part", 0.5))
    graine = 5

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    print(f"# {len(garde)} canaux · {n_neur} neurones · "
          f"{len(cltr)} langues d'apprentissage")

    # ------------------------------------------------------------------ STABILITÉ
    print(f"\n=== QUESTION 1 — LE RAYON SPECTRAL DU JACOBIEN ===")
    print(f"# J = (1-a)·I + a·D·P.  D = diag(1 - tanh²) est la pente locale.")
    print(f"# rayon < 1 : l'état se stabilise · rayon > 1 : il peut diverger ou osciller")
    print(f"\n# {'a':>7}{'rayon (D=I)':>14}{'rayon (D observé)':>19}"
          f"{'max ||s|| observé':>19}{'verdict':>12}")
    seuils = []
    for a in (0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.95, 1.2):
        P = Pont((cltr, Etr, Ytr), a, graine, len(garde))
        P.quadratique = True
        P.nait(n_neur, True)
        # P effectif : le bloc de récurrence interne de la couche (W_self restreint
        # aux neurones entre eux ; W_par est nul en couche 0)
        Ws = np.array([p[1][-n_neur:] for p in P.poids])       # (n, n)
        r_id = float(np.max(np.abs(np.linalg.eigvals((1-a)*np.eye(n_neur) + a*Ws))))
        # pente observée : s = tanh(...) donc D = 1 - s², estimée sur le corpus
        S = P.X[0][:2000]
        D = np.diag(np.clip(1.0 - (S**2).mean(0), 1e-6, 1.0))
        r_obs = float(np.max(np.abs(np.linalg.eigvals(
            (1-a)*np.eye(n_neur) + a*D@Ws))))
        mx = max(float(np.abs(x).max()) for x in P.X[:20])
        verdict = "STABLE" if r_obs < 1.0 else "OSCILLE"
        print(f" {a:>7.2f}{r_id:>14.3f}{r_obs:>19.3f}{mx:>19.3f}{verdict:>12}")
        if r_obs < 1.0:
            seuils.append(a)
    if seuils:
        print(f"\n# plus grand `a` mesuré STABLE : {max(seuils)}")
    print(f"# a=0,2 est la valeur du pont. La marge est le rapport 1/rayon.")

    # ------------------------------------------------------------------ ÉVÉNEMENTS
    print(f"\n=== QUESTION 2 — COMBIEN DE NEURONES BOUGENT À CHAQUE PAS ? ===")
    print(f"# « événement » = |s_t - s_(t-1)| > seuil. On compte sur du corpus réel.")
    for a in (0.2, 0.8):
        P = Pont((cltr, Etr, Ytr), a, graine, len(garde))
        P.quadratique = True
        P.nait(n_neur, True)
        S = np.vstack([x for x in P.X[:80]])
        d = np.abs(np.diff(S, axis=0))
        print(f"\n# a = {a}")
        print(f"#   {'seuil':>10}{'événements':>13}{'neurones morts':>16}")
        for eps in (1e-6, 1e-5, 1e-4, 1e-3, 1e-2):
            taux = float((d > eps).mean())
            morts = float((d.std(0) < eps).mean())
            print(f"#   {eps:>10.0e}{taux:>12.1%}{morts:>16.1%}")
        # saturation : un neurone saturé a une dérivée nulle, donc ne transmettra rien
        sat = float((np.abs(S) > 0.99).mean())
        print(f"#   neurones SATURÉS (|s| > 0,99, dérivée ≈ 0) : {sat:.1%} des pas")
        print(f"#   → une implémentation par événements paierait "
              f"{1-float((d>1e-4).mean()):.1%} de pas en MOINS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

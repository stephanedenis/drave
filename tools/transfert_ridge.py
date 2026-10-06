#!/usr/bin/env python3
"""LE READOUT SUR-APPREND-IL LE VIVIER ? — balayage du ride, deux panneaux.

DIAGNOSTIC ÉTABLI (§36). Avec le protocole à deux panneaux :
    écart à l'oracle — VALIDATION (même vivier) : +0,0112
    écart à l'oracle — TEST (hors vivier)       : +0,0975
Dans le vivier notre lecture partagée est quasi optimale ; hors vivier il reste
0,0975 sur la table. Le goulot est le TRANSFERT.

L'HYPOTHÈSE LA PLUS SIMPLE, et elle se teste à un paramètre près : si la lecture
transfère mal, c'est peut-être qu'elle s'ajuste à des directions PROPRES AU VIVIER.
Le remède classique est de régulariser davantage. Or le ride est aujourd'hui une
constante choisie à la main (0,3), jamais balayée sur ce critère.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si le readout sur-apprend le vivier, augmenter
le ride doit
  - DÉGRADER légèrement la validation (moins bon ajustement dans le vivier),
  - AMÉLIORER le test (moins de directions propres au vivier),
  - donc RÉDUIRE l'écart à l'oracle hors vivier.
Si les deux se dégradent ensemble, l'hypothèse est fausse et le transfert manquant
n'est pas du sur-apprentissage.

Usage : transfert_ridge.py <cache_appr.npz> <cache_test.npz> [--neur 40]
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
    a, graine = 0.2, 5
    rides = [float(x) for x in opt("--rides", "0.03,0.1,0.3,1,3,10,30").split(",")]

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)

    vivant = np.zeros(Ytr[0].shape[1])
    for i in range(len(cltr)):
        vivant += ((Ytr[i] != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(cltr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]
    print(f"# {len(cltr)} langues d'apprentissage · {len(clte)} de test · "
          f"{len(garde)}/{H} canaux")

    itr = np.arange(len(cltr))
    ival = itr[::7]
    iap = np.array([i for i in itr if i not in set(ival.tolist())])
    print(f"# vivier : {len(iap)} ajustement · {len(ival)} validation (même vivier) "
          f"· {len(clte)} test (hors vivier)")
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    t = time.time()
    P = Pont((cltr, Etr, Ytr), a, graine, len(garde))
    P.quadratique = True
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    print(f"# réseau : {P.compte_neurones} neurones · {len(P.couches)} couche(s) "
          f"(construit en {time.time()-t:.0f} s)")

    # caractéristiques mises en forme UNE fois : le balayage ne coûte plus que des
    # inversions de taille 80, soit des millisecondes
    Aap = P.phi(np.vstack([P.X[i][:, idx] for i in iap]))
    Bap = np.vstack([Ytr[i] for i in iap]) - mt
    Xv = P.recalcule(idx, [Etr[i] for i in ival])
    Av = P.phi(np.vstack(Xv))
    Bv = np.vstack([Ytr[i] for i in ival]) - mt
    Xt = P.recalcule(idx, Ete)
    print(f"# caractéristiques prêtes · {Aap.shape[1]} colonnes")

    # La Gram du vivier est calculée UNE fois : le balayage ne coûte plus que des
    # inversions de taille 80, soit des millisecondes par valeur de ride.
    Gap = Aap.T @ Aap
    Dap = Aap.T @ Bap
    # panneaux de test et de validation, mis en forme une fois
    Yv_full = [Ytr[i] for i in ival]
    Av = P.phi(np.vstack(Xv))
    Gv = Av.T @ Av
    Dv = Av.T @ (np.vstack(Yv_full) - mt)
    At = P.phi(np.vstack(Xt))
    Gt = At.T @ At
    Dt = At.T @ (np.vstack(Yte) - mt)
    Tv = np.mean([cos_lignes(np.tile(mt, (len(y), 1)), y) for y in Yv_full])
    Tt = np.mean([cos_lignes(np.tile(mt, (len(y), 1)), y) for y in Yte])
    print(f"# caractéristiques prêtes · {Aap.shape[1]} colonnes · "
          f"témoins : VALID {Tv:.4f} · TEST {Tt:.4f}")

    lignes = []
    for ride in rides:
        reg = ride*len(Aap)*np.eye(Aap.shape[1])
        W = np.linalg.solve(Gap + reg, Dap)
        Wo_v = np.linalg.solve(Gv + ride*len(Av)*np.eye(Av.shape[1]), Dv)
        Wo_t = np.linalg.solve(Gt + ride*len(At)*np.eye(At.shape[1]), Dt)
        fv = cos_lignes(Av @ W + mt, np.vstack(Yv_full))
        ov = cos_lignes(Av @ Wo_v + mt, np.vstack(Yv_full))
        ft = cos_lignes(At @ W + mt, np.vstack(Yte))
        ot = cos_lignes(At @ Wo_t + mt, np.vstack(Yte))
        lignes.append((ride, fv, ov, ft, ot))
        print(f"  ride {ride:>6} : VALID fid {fv:.4f} oracle {ov:.4f} "
              f"écart {ov-fv:+.4f}  |  TEST fid {ft:.4f} oracle {ot:.4f} "
              f"écart {ot-ft:+.4f}")

    print(f"\n# {'ride':>6}{'VALID fid':>11}{'VALID écart':>13}"
          f"{'TEST fid':>10}{'TEST écart':>12}")
    for ride, fv, ov, ft, ot in lignes:
        print(f"# {ride:>6}{fv:>11.4f}{ov-fv:>+13.4f}{ft:>10.4f}{ot-ft:>+12.4f}")
    print(f"\n# PRÉDICTION : si le readout sur-apprend le vivier, l'écart TEST doit")
    print(f"# DIMINUER quand le ride augmente. Le ride actuel du pont est 0,3.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""SATURATION — à quel gain la dynamique devient-elle creuse, et à quel prix ?

MESURÉ AU §38 : à `gain = 1` (la valeur du pont), le `tanh` ne sature que **0,6 %**
du temps et 99,8 % des couples (neurone, pas) changent à chaque pas. Une
implémentation par événements ne paierait donc rien. La dynamique vit dans son
régime LINÉAIRE.

Or une impulsion est creuse **par construction** : seuil, émission, remise à zéro.
Pour que la parcimonie apparaisse, il faut pousser les neurones à BASCULER. Le seul
levier disponible sans toucher à la dynamique est le **gain d'entrée** — `B` est
multiplié par ce gain, donc le pilotage du `tanh` augmente.

LA QUESTION, ET ELLE EST À DOUBLE TRANCHANT. Si un gain élevé fait saturer 50 % des
neurones, la porte des impulsions s'ouvre — mais si cette saturation détruit la
fidélité, l'impulsion n'est pas gratuite. Ce script mesure **les deux ensemble** :
taux de saturation, taux d'événements, et fidélité.

PRÉDICTION, ÉCRITE AVANT LA MESURE : la fidélité doit se dégrader quand la
saturation augmente, parce qu'un neurone saturé ne transmet plus de gradient
d'information — il dit « oui » ou « non » et rien entre les deux. Le point
intéressant est **où se situe le genou** : s'il existe un gain qui donne 30-50 % de
saturation tout en gardant la fidélité, l'impulsion est ouverte ; sinon, elle coûte
ce qu'elle rapporte.

Usage : saturation.py <cache_appr.npz> <cache_test.npz> [--neur 40]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 40))
    part = float(opt("--part", 0.5))
    graine, ride = 5, 0.03          # ← le ride corrigé du §37
    gains = [float(x) for x in opt("--gains", "0.003,0.01,0.03,0.1,0.3,1").split(",")]

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]
    print(f"# {len(garde)} canaux · {n_neur} neurones · ride {ride}")

    itr = np.arange(len(cltr))
    ival = itr[::7]
    iap = np.array([i for i in itr if i not in set(ival.tolist())])
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)
    Tv = np.mean([cos_lignes(np.tile(mt, (len(Ytr[i]), 1)), Ytr[i]) for i in ival])
    Tt = np.mean([cos_lignes(np.tile(mt, (len(Yte[k]), 1)), Yte[k])
                  for k in range(len(clte))])

    print(f"\n# {'gain':>6}{'saturation':>12}{'événem. 1e-4':>15}"
          f"{'VALID fid':>11}{'TEST fid':>10}{'apport TEST':>13}")
    lignes = []
    for g in gains:
        P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
        P.quadratique = True
        P.gain_entree = g
        P.nait(n_neur, True)
        S = np.vstack([x for x in P.X[:80]])
        sat = float((np.abs(S) > 0.99).mean())
        d = np.abs(np.diff(S, axis=0))
        ev = float((d > 1e-4).mean())

        idx = np.arange(P.compte_neurones)
        W = P.ajuste(idx, ride, mt, iap)
        Xv = P.recalcule(idx, [Etr[i] for i in ival])
        Yv = [Ytr[i] for i in ival]
        fv = cos_lignes(P.phi(np.vstack(Xv)) @ W + mt, np.vstack(Yv))
        Xt = P.recalcule(idx, Ete)
        ft = cos_lignes(P.phi(np.vstack(Xt)) @ W + mt, np.vstack(Yte))
        lignes.append((g, sat, ev, fv, ft))
        print(f" {g:>6.1f}{sat:>11.1%}{ev:>15.1%}{fv:>11.4f}{ft:>10.4f}"
              f"{ft-Tt:>+13.4f}")
        del P, S, d, Xv, Xt

    print(f"\n# témoins : VALID {Tv:.4f} · TEST {Tt:.4f}")
    print(f"# Le gain 1 est la valeur actuelle : 0,6 % de saturation, "
          f"l'événementiel ne paie rien.")
    print(f"# PRÉDICTION : la fidélité se dégrade quand la saturation monte. "
          f"Le genou est le gain")
    print(f"# qui donne 30-50 % de saturation en gardant la fidélité.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

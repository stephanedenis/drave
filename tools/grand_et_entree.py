#!/usr/bin/env python3
"""A200 + ENTRÉE — la mesure qui manquait, et la plus informative.

§31 a montré que l'entrée seule (C_quad, 1 792 caractéristiques) vaut 0,6536, et
qu'un réservoir de 40 neurones y ajoute +0,0073 (B = 0,6609). Mais un réservoir de
200 neurones seul vaut 0,6218 — il progresse avec la taille. La question qui décide
de l'avenir du pont :

    un GROS réservoir ajoute-t-il davantage quand on lui donne aussi l'entrée ?

Si oui, le réservoir n'est pas inutile — il est seulement trop petit, et la voie est
d'ajouter des neurones. Si le supplément reste ~0,007 quelles que soient la taille,
alors la récurrence n'apporte rien que l'entrée ne portait déjà, et c'est
l'architecture qu'il faut revoir, pas sa taille.

Ce script ne fait QUE cela : pas de C_lin, pas de A200 seul — ces nombres sont au
§31 et n'ont pas à être repayés.

Usage : grand_et_entree.py <cache_appr.npz> <cache_test.npz> [--grand 200]
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
    part = float(opt("--part", 0.5))
    grand = int(opt("--grand", 200))
    a, graine, ride = 0.2, 5, 0.3

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)

    vivant = np.zeros(Ytr[0].shape[1])
    for i in range(len(cltr)):
        vivant += ((Ytr[i] != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(cltr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]
    Etr_c = [e - e.mean(0, keepdims=True) for e in Etr]
    Ete_c = [e - e.mean(0, keepdims=True) for e in Ete]
    print(f"# {len(cltr)} langues · {len(clte)} de test · {len(garde)}/{H} canaux")

    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)
    quad = lambda X: np.hstack([X, X*X])  # noqa: E731

    def evalue(fait, nom):
        G = D = None
        ntot = 0
        for i in itr:
            Ai = fait(i, True)
            G = Ai.T @ Ai if G is None else G + Ai.T @ Ai
            D = Ai.T @ (Ytr[i] - mt) if D is None else D + Ai.T @ (Ytr[i] - mt)
            ntot += len(Ai)
            del Ai
        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]), D)
        res = {cl: cos_lignes(fait(k, False) @ W + mt, Yte[k])
               for k, cl in enumerate(clte)}
        T = {cl: cos_lignes(np.tile(mt, (len(Yte[k]), 1)), Yte[k])
             for k, cl in enumerate(clte)}
        f = np.mean(list(res.values()))
        ap = np.mean([res[c] - T[c] for c in clte])
        print(f"  {nom:<26} {G.shape[0]:>5} caract. · fidélité {f:.4f} · "
              f"apport {ap:+.4f}")
        return res

    t = time.time()
    P = Pont((cltr, Etr, Ytr), a, graine, len(garde))
    P.quadratique = True
    P.nait(grand, True)
    Xte = P.recalcule(np.arange(P.compte_neurones), Ete)
    print(f"# pont {grand} neurones construit en {time.time()-t:.0f} s")

    print("\n=== MESURES ===")
    a_g = evalue(lambda i, tr: quad(P.X[i] if tr else Xte[i]), f"A{grand} seul")
    # L'ENTRÉE EST PRISE LINÉAIRE, PAS QUADRATIQUE. `quad(hstack([X, E]))`
    # produisait 2 192 colonnes et faisait mourir le processus deux fois. Or la
    # comparaison honnête n'a pas besoin des carrés de l'entrée : il suffit de
    # mettre le réservoir à côté de la MÊME représentation de l'entrée que celle
    # déjà mesurée seule (C_lin = 0,6364, §31). On isole ainsi exactement ce que
    # les 400 colonnes du réservoir ajoutent à 896 colonnes d'entrée.
    b_g = evalue(lambda i, tr: np.hstack([quad(P.X[i] if tr else Xte[i]),
                                          Etr_c[i] if tr else Ete_c[i]]),
                 f"A{grand} + entrée LINÉAIRE")

    print(f"\n# CE QUE LE RÉSERVOIR AJOUTE PAR-DESSUS L'ENTRÉE LINÉAIRE")
    print(f"#   C_lin (entrée seule, 896 colonnes, §31) = 0,6364")
    print(f"#   A{grand} + entrée  −  C_lin = "
          f"{np.mean(list(b_g.values())) - 0.6364:+.4f}")
    print(f"#   rappel : A40 + entrée quadratique − C_quad = +0,0073")
    print(f"#   et A{grand} seul − A40 seul = "
          f"{np.mean(list(a_g.values())) - 0.5972:+.4f}")

    csv = opt("--csv", "/tmp/grand_et_entree.csv")
    with open(csv, "w") as fh:
        fh.write(f"langue;temoin;a{grand};a{grand}_entree\n")
        for k, cl in enumerate(clte):
            tm = cos_lignes(np.tile(mt, (len(Yte[k]), 1)), Yte[k])
            fh.write(f"{cl};{tm:.6f};{a_g[cl]:.6f};{b_g[cl]:.6f}\n")
    print(f"# table écrite : {csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

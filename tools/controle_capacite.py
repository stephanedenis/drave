#!/usr/bin/env python3
"""CONTRÔLE DE CAPACITÉ — l'entrée gagne-t-elle par NATURE ou par TAILLE ?

§29 a mesuré : une lecture quadratique sur l'entrée SEULE (1 792 caractéristiques,
aucun neurone) fait 0,6536, contre 0,5972 pour 40 neurones récurrents (80
caractéristiques). Mais C a 22× plus de colonnes que A. Une partie de l'écart peut
être de la CAPACITÉ, pas de la nature. Ce script tranche :

  C_lin   — entrée seule, lecture LINÉAIRE (896 colonnes). Si C_lin ≈ C_quad, la
            non-linéarité ne sert à rien et tout est linéaire dans l'entrée.
  C_quad  — entrée seule, quadratique (1 792). Rappel : 0,6536.
  A40     — 40 neurones, quadratique (80). Rappel : 0,5972.
  A200    — 200 neurones, quadratique (400). Le réservoir peut-il rattraper par la
            taille ? 200 neurones pour 400 colonnes, contre 1 792 pour l'entrée :
            le budget de colonnes reste favorable à l'entrée, mais l'écart de
            capacité passe de 22× à 4,5×.
  A200+E  — 200 neurones ET l'entrée. Ce que le réservoir ajoute quand on lui donne
            à la fois la taille et l'accès direct.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si l'avantage de C vient de la capacité, A200
doit se rapprocher nettement de C_quad. S'il vient de la nature — le réservoir
détruit l'information par son tanh et sa récurrence — A200 restera loin derrière
malgré 5× plus de neurones.

Usage : controle_capacite.py <cache_appr.npz> <cache_test.npz>
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
    print(f"# {len(cltr)} langues d'apprentissage · {len(clte)} de test · "
          f"{len(garde)}/{H} canaux")

    # entrée centrée par langue — calculable à l'inférence, sans étiquette
    Etr_c = [e - e.mean(0, keepdims=True) for e in Etr]
    Ete_c = [e - e.mean(0, keepdims=True) for e in Ete]

    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    def evalue(fait, nom):
        G = D = None
        ntot = 0
        for i in itr:
            Ai = fait(i)
            G = Ai.T @ Ai if G is None else G + Ai.T @ Ai
            Yi = Ytr[i] - mt
            D = Ai.T @ Yi if D is None else D + Ai.T @ Yi
            ntot += len(Ai)
            del Ai
        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]), D)
        res = {cl: cos_lignes(fait(len(cltr)+k) @ W + mt, Yte[k])
               for k, cl in enumerate(clte)}
        print(f"  {nom:<22} {G.shape[0]:>5} caractérisques · fidélité "
              f"{np.mean(list(res.values())):.4f}")
        return res

    def quad(X):
        X = np.asarray(X, dtype=np.float64)
        return np.hstack([X, X*X])

    def ident(X):
        return np.asarray(X, dtype=np.float64)

    print("\n=== LECTURES SUR L'ENTRÉE SEULE (aucun neurone) ===")
    C_lin = evalue(lambda i: ident(Etr_c[i] if i < len(cltr)
                                   else Ete_c[i-len(cltr)]), "C_lin (linéaire)")

    def pont(n):
        t = time.time()
        P = Pont((cltr, Etr, Ytr), a, graine, len(garde))
        P.quadratique = True
        P.nait(n, True)
        print(f"  [pont {n} neurones construit en {time.time()-t:.0f} s]")
        return P

    print("\n=== RÉSERVOIRS ===")
    P = pont(grand)
    Xte = P.recalcule(np.arange(P.compte_neurones), Ete)
    Xtr_l = P.X

    A_g = evalue(lambda i: quad(Xtr_l[i] if i < len(cltr) else Xte[i-len(cltr)]),
                 f"A{grand} (quadratique)")

    def fait_plus(i):
        if i < len(cltr):
            return quad(np.hstack([Xtr_l[i], Etr_c[i]]))
        k = i - len(cltr)
        return quad(np.hstack([Xte[k], Ete_c[k]]))

    B_g = evalue(fait_plus, f"A{grand} + entrée")

    def temoin():
        return {cl: cos_lignes(np.tile(mt, (len(Yte[k]), 1)), Yte[k])
                for k, cl in enumerate(clte)}
    T = temoin()

    print(f"\n=== APPORT PROPRE (fidélité − témoin) ===")
    print(f"# témoin constant moyen : {np.mean(list(T.values())):.4f}")
    for nom, r in [("C_lin (entrée, linéaire)", C_lin),
                   (f"A{grand} (réservoir)", A_g),
                   (f"A{grand} + entrée", B_g)]:
        print(f"#   {nom:<26} fidélité {np.mean(list(r.values())):.4f} · "
              f"apport {np.mean([r[c]-T[c] for c in clte]):+.4f}")
    print(f"#   rappels §29 : C_quad (entrée, quadratique) 0,6536 · "
          f"A40 (réservoir) 0,5972 · A40+entrée 0,6609")

    print(f"\n# LANGUES SUIVIES (fidélités brutes)")
    print(f"# {'langue':<6}{'C_lin':>9}{f'A{grand}':>9}{f'A{grand}+e':>11}")
    for c in ("deu", "heb", "jpn", "kor", "srp", "dzo", "fuf", "csw", "xsm", "ell"):
        if c in clte:
            print(f"  {c:<6}{C_lin[c]:>9.4f}{A_g[c]:>9.4f}{B_g[c]:>11.4f}")

    csv = opt("--csv", "/tmp/controle_capacite.csv")
    with open(csv, "w") as fh:
        fh.write(f"langue;temoin;c_lin;a{grand};a{grand}_entree;c_quad_ref;a40_ref\n")
        ref = {l.strip().split(';')[0]: l.strip().split(';')
               for l in open('/tmp/profil_langues.csv') if l.strip()}
        for c in clte:
            r = ref.get(c)
            # colonnes de profil_langues.csv : 5 témoin · 6 fid_ref · 9 fid_multi
            fh.write(f"{c};{T[c]:.6f};{C_lin[c]:.6f};{A_g[c]:.6f};{B_g[c]:.6f};"
                     f"{float(r[9]) if r else float('nan'):.6f};"
                     f"{float(r[6]) if r else float('nan'):.6f}\n")
    print(f"\n# table écrite : {csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

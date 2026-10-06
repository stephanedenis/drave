#!/usr/bin/env python3
"""QUATRE LEVIERS POUR LES LANGUES NON SERVIES — mesurés sur le MÊME vivier.

ÉTABLI (§27) : l'apport propre du pont (`fidélité − témoin constant`) vaut +0,0885
sur `dzo` mais +0,0014 sur `heb`. Sur `deu`, `jpn`, `kor`, `heb`, `srp`, ni la
constante ni le pont ne servent à grand-chose. Et un ajustement PRIVÉ (l'oracle)
ne les sauve pas non plus : deu 0,539, jpn 0,575. Le goulot est donc dans les
CARACTÉRISTIQUES, pas dans le partage.

Quatre candidats, à nombre de neurones constant quand c'est possible :

  A. référence    — 1 couche de 40 neurones, lecture quadratique
  B. + entrée     — la lecture voit AUSSI le jeton courant `e_t` (connexion directe)
  C. entrée seule — la lecture ne voit QUE `e_t`, aucun neurone. C'est le TÉMOIN qui
                    dit si le réservoir sert à quelque chose : si C ≈ A, tout le
                    travail est déjà fait par la couche 0.
  D. 2 couches    — 20 + 20 neurones. Même budget, composition en plus. C'est la
                    question de la mission : une couche de plus achète-t-elle
                    quelque chose que des neurones en plus n'achètent pas ?

MÉMOIRE. Les variantes B et C produisent des matrices à ~1 900 colonnes sur
~700 000 lignes : 10 Go si on les matérialisait. On n'accumule donc que la Gram
`AᵀA` et le second membre `Aᵀ(Y − mt)`, langue par langue. Jamais de matrice
complète.

Usage : leviers_pont.py <cache_appr.npz> <cache_test.npz> [--neur 40]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402

SOURCE = "/tmp/udhr10_toutes"
CLES = ["deu", "heb", "jpn", "kor", "srp", "dzo", "fuf", "csw", "xsm", "ell"]


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 40))
    part = float(opt("--part", 0.5))
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

    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    # L'entrée est CENTRÉE par langue (son jeton moyen est retiré) pour les
    # variantes B et C. Sans cela, la lecture linéaire est dominée par le décalage
    # massivement propre à la langue — écriture, morphologie — qui ne dit aucun
    # contenu. C'est l'option `--centre-entree` déjà documentée, et ce décalage est
    # calculable à l'inférence sur l'entrée elle-même, sans aucune étiquette.
    Etr_c = [e - e.mean(0, keepdims=True) for e in Etr]
    Ete_c = [e - e.mean(0, keepdims=True) for e in Ete]

    def phi(X):
        X = np.asarray(X, dtype=np.float64)
        return np.hstack([X, X*X])

    def evalue(fait, nom):
        """`fait(i)` rend les caractéristiques d'apprentissage de la langue i ;
        `fait(N+i)` celles de la langue de test i. Accumulation en flux."""
        G = D = None
        ntot = 0
        for i in itr:
            Ai = phi(fait(i))
            G = Ai.T @ Ai if G is None else G + Ai.T @ Ai
            Yi = Ytr[i] - mt
            D = Ai.T @ Yi if D is None else D + Ai.T @ Yi
            ntot += len(Ai)
            del Ai
        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]), D)
        res = {}
        for k, cl in enumerate(clte):
            Ak = phi(fait(len(cltr) + k))
            res[cl] = cos_lignes(Ak @ W + mt, Yte[k])
            del Ak
        print(f"\n=== {nom} ===")
        print(f"#   {G.shape[0]} caractéristiques · {ntot} pas d'apprentissage · "
              f"fidélité TEST moyenne {np.mean(list(res.values())):.4f}")
        return res

    T = {cl: cos_lignes(np.tile(mt, (len(Yte[k]), 1)), Yte[k])
         for k, cl in enumerate(clte)}
    print(f"# témoin constant moyen : {np.mean(list(T.values())):.4f}")

    def pont(couches):
        P = Pont((cltr, Etr, Ytr), a, graine, len(garde))
        P.quadratique = True
        for nc in couches:
            P.nait(nc, True)
        return P

    P1 = pont([n_neur])
    print(f"# A : {P1.compte_neurones} neurones · {len(P1.couches)} couche(s) "
          f"{P1.couches}")
    Xtr1, Xte1 = P1.X, P1.recalcule(np.arange(P1.compte_neurones), Ete)

    A = evalue(lambda i: Xtr1[i] if i < len(cltr) else Xte1[i - len(cltr)],
               "A · référence — 1 couche de 40")

    B = evalue(lambda i: (np.hstack([Xtr1[i], Etr_c[i]]) if i < len(cltr)
                          else np.hstack([Xte1[i-len(cltr)], Ete_c[i-len(cltr)]])),
               "B · + le jeton courant e_t dans la lecture")

    C = evalue(lambda i: Etr_c[i] if i < len(cltr) else Ete_c[i - len(cltr)],
               "C · l'entrée SEULE, aucun neurone — témoin du réservoir")

    P2 = pont([n_neur//2, n_neur - n_neur//2])
    print(f"# D : {P2.compte_neurones} neurones · {len(P2.couches)} couches "
          f"{P2.couches}")
    Xte2 = P2.recalcule(np.arange(P2.compte_neurones), Ete)
    D = evalue(lambda i: P2.X[i] if i < len(cltr) else Xte2[i - len(cltr)],
               "D · 2 couches de 20 (même budget)")

    cl = clte
    print(f"\n=== APPORT PROPRE (fidélité − témoin constant), trié ===")
    print(f"# {'langue':<6}{'témoin':>8}{'A réf':>9}{'B +e_t':>9}{'C e_t':>9}{'D 2c':>9}")
    for k in np.argsort([A[c] - T[c] for c in cl]):
        c = cl[k]
        print(f"  {c:<6}{T[c]:>8.3f}{A[c]-T[c]:>+9.4f}{B[c]-T[c]:>+9.4f}"
              f"{C[c]-T[c]:>+9.4f}{D[c]-T[c]:>+9.4f}")
    print(f"\n# MOYENNES")
    for nom, r in [("A réf", A), ("B +e_t", B), ("C e_t seul", C), ("D 2 couches", D)]:
        print(f"#   {nom:<12} fidélité {np.mean(list(r.values())):.4f} · apport "
              f"{np.mean([r[c]-T[c] for c in cl]):+.4f}")
    print(f"\n# LANGUES SUIVIES (fidélités brutes)")
    print(f"# {'langue':<6}{'frag':>7}{'A':>9}{'B':>9}{'C':>9}{'D':>9}")
    for c in CLES:
        if c not in cl:
            continue
        p = os.path.join(SOURCE, c + ".txt")
        n = len(open(p, encoding="utf-8", errors="replace").read()) if os.path.exists(p) else 0
        k = cl.index(c)
        print(f"  {c:<6}{len(Yte[k])/max(n,1):>7.3f}{A[c]:>9.4f}{B[c]:>9.4f}"
              f"{C[c]:>9.4f}{D[c]:>9.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

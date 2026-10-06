#!/usr/bin/env python3
"""TEXTE NEUF — la lecture directe gagne-t-elle par nature, ou par ALIGNEMENT ?

LE DOUTE, ET IL EST SÉRIEUX. L'UDHR est UN SEUL texte traduit en 392 langues. À la
position t, toutes les langues disent LA MÊME CHOSE. Or la couche 0 encode la
position (encodage rotationnel) : une lecture `e_t → y_t`, même purement linéaire,
peut donc apprendre « à la position t, sors le vecteur typique de t » — et réussir
sans rien comprendre à la langue. Ce serait un artefact du corpus, pas une capacité.

Cela expliquerait tout le §29 : C (entrée seule) bat A (réservoir) parce que le
réservoir, lui, ne peut pas lire la position directement.

LE TEST. Wikipedia n'est PAS aligné : les 480 tranches anglaises et les 480
tranches françaises sont des ARTICLES DIFFÉRENTS. À l'intérieur d'une même langue,
les tranches ne partagent pas non plus leur contenu. On entraîne donc sur 400
tranches et on évalue sur 80 tranches JAMAIS VUES — du texte neuf, sans alignement
positionnel possible.

PRÉDICTION, ÉCRITE AVANT LA MESURE :
  - si C gagne par alignement, son avantage sur A doit DISPARAÎTRE sur texte neuf,
    et les deux doivent retomber près du témoin constant ;
  - si C gagne par nature, son avantage doit se maintenir.

Usage : corpus_neuf.py <cache.npz> [--appr 400] [--neur 40] [--couche 10]
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
    p = sys.argv[1]
    n_appr = int(opt("--appr", 400))
    n_neur = int(opt("--neur", 40))
    a, graine, ride = 0.2, 5, 0.3

    cles, E, Y, H = charge(p)
    if n_appr >= len(cles):
        n_appr = int(len(cles)*0.8)
    itr, ite = list(range(n_appr)), list(range(n_appr, len(cles)))
    print(f"# {p}")
    print(f"# {len(cles)} tranches · {len(itr)} apprentissage · {len(ite)} test "
          f"(JAMAIS VUES)")
    print(f"# pas — apprentissage {sum(len(E[i]) for i in itr)} · "
          f"test {sum(len(E[i]) for i in ite)}")

    Etr = [E[i] for i in itr]; Ytr = [Y[i] for i in itr]
    Ete = [E[i] for i in ite]; Yte = [Y[i] for i in ite]
    Etr_c = [e - e.mean(0, keepdims=True) for e in Etr]
    Ete_c = [e - e.mean(0, keepdims=True) for e in Ete]

    mt = np.vstack(Ytr).mean(axis=0)

    def evalue(fait, nom):
        G = D = None
        ntot = 0
        for i in range(len(Etr)):
            Ai = fait(i, True)
            G = Ai.T @ Ai if G is None else G + Ai.T @ Ai
            Yi = Ytr[i] - mt
            D = Ai.T @ Yi if D is None else D + Ai.T @ Yi
            ntot += len(Ai)
            del Ai
        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]), D)
        res = [cos_lignes(fait(k, False) @ W + mt, Yte[k]) for k in range(len(Ete))]
        print(f"  {nom:<24} {G.shape[0]:>5} caract. · fidélité {np.mean(res):.4f} "
              f"· médiane {np.median(res):.4f} · min {np.min(res):.4f}")
        return float(np.mean(res)), res

    ident = lambda X: np.asarray(X, dtype=np.float64)          # noqa: E731
    quad = lambda X: np.hstack([X, X*X])                        # noqa: E731

    tem = float(np.mean([cos_lignes(np.tile(mt, (len(Yte[k]), 1)), Yte[k])
                         for k in range(len(Ete))]))
    print(f"\n# témoin constant sur le TEST neuf : {tem:.4f}")

    print("\n=== SANS AUCUN NEURONE ===")
    c_lin = evalue(lambda i, tr: ident(Etr_c[i] if tr else Ete_c[i]), "C_lin (linéaire)")
    c_qua = evalue(lambda i, tr: quad(Etr_c[i] if tr else Ete_c[i]), "C_quad (quadratique)")

    print("\n=== RÉSERVOIR ===")
    t = time.time()
    P = Pont(( [f"t{i}" for i in range(len(Etr))], Etr, Ytr), a, graine, Ytr[0].shape[1])
    P.quadratique = True
    P.nait(n_neur, True)
    print(f"  [pont construit en {time.time()-t:.0f} s]")
    Xte = P.recalcule(np.arange(P.compte_neurones), Ete)
    a40 = evalue(lambda i, tr: quad(P.X[i] if tr else Xte[i]), "A40 (réservoir)")

    def fait_plus(i, tr):
        return quad(np.hstack([P.X[i] if tr else Xte[i],
                               Etr_c[i] if tr else Ete_c[i]]))
    a40e = evalue(fait_plus, "A40 + entrée")

    print(f"\n=== VERDICT ===")
    for nom, f in [("C_lin (entrée seule)", c_lin), ("C_quad (entrée seule)", c_qua),
                   ("A40 (réservoir)", a40), ("A40 + entrée", a40e)]:
        print(f"#   {nom:<24} {f[0]:.4f}  (apport {f[0]-tem:+.4f})")
    print(f"#   avantage de l'entrée seule sur le réservoir : "
          f"{c_qua[0]-a40[0]:+.4f}")
    print(f"#   rappel UDHR (texte ALIGNÉ) : C_quad 0,6536 · A40 0,5972 "
          f"→ avantage +0,0564")
    return 0


if __name__ == "__main__":
    sys.exit(main())

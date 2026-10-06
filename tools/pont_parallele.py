#!/usr/bin/env python3
"""pont_parallele.py — le pont sur un corpus PARALLÈLE, segment par segment.

Différence de fond avec `pont_generatif.py` : là-bas les langues ne sont pas
appariées et l'invariance se mesure entre TOUTES les paires de langues ; ici les
segments SONT appariés (la scène s dans la langue A et la scène s dans la langue
B), donc l'invariance se mesure **segment par segment**. Comparer toutes les
paires ici n'aurait aucun sens : deux scènes différentes ne doivent PAS se
ressembler.

Ce que le tool mesure :
  - fidélité sur A (apprise) et sur B (transférée) ;
  - l'invariance inter-langue du PROFESSEUR, segment par segment — la référence ;
  - l'invariance inter-langue de NOTRE SORTIE, segment par segment ;
  - le diagnostic oracle, sur les deux langues.

Aucune rétropropagation : A et B aléatoires et gelés, seule la lecture s'ajuste.

Usage : pont_parallele.py <cache_A.npz> <cache_B.npz> [--couche 10] [--canaux 0.5]
"""
import sys
import numpy as np
sys.path.insert(0, "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools")
from pont_generatif import Pont, charge, cos_lignes, inv  # noqa: E402


def appariement_par_taille(yA, yB):
    """Appariement par DÉFAUT : les caches sont déjà dans l'ordre des segments."""
    n = min(len(yA), len(yB))
    return list(range(n)), list(range(n))


def main():
    pa, pb = sys.argv[1], sys.argv[2]
    couche = int(sys.argv[sys.argv.index("--couche")+1]) if "--couche" in sys.argv else 10
    part = float(sys.argv[sys.argv.index("--canaux")+1]) if "--canaux" in sys.argv else 0.0
    a_ = float(sys.argv[sys.argv.index("--a")+1]) if "--a" in sys.argv else 0.5
    ride = float(sys.argv[sys.argv.index("--ride")+1]) if "--ride" in sys.argv else 1.0
    graine = int(sys.argv[sys.argv.index("--graine")+1]) if "--graine" in sys.argv else 5

    clA, EA, YA, H = charge(pa)
    clB, EB, YB, _ = charge(pb)
    n = min(len(clA), len(clB))
    clA, EA, YA = clA[:n], EA[:n], YA[:n]
    clB, EB, YB = clB[:n], EB[:n], YB[:n]

    if part > 0.0:
        E_ref = np.vstack([y**2 for y in YA]).sum(0)
        o = np.argsort(-E_ref); c = np.cumsum(E_ref[o])/E_ref.sum()
        g = np.sort(o[:int(np.searchsorted(c, part)+1)])
        YA = [y[:, g] for y in YA]; YB = [y[:, g] for y in YB]
        print(f"# sous-ensemble actif : {len(g)}/{H} canaux sur l'apprentissage de A")

    print(f"# {n} segments appariés · A={clA[0]}… · B={clB[0]}… · couche {couche}")

    # ---- invariance du PROFESSEUR, segment par segment (la référence)
    def inv_appariee(VA, VB, quel="derniere"):
        cs = []
        for i in range(n):
            xa = VA[i][-1]; xb = VB[i][-1]
            na, nb = np.linalg.norm(xa), np.linalg.norm(xb)
            if na > 0 and nb > 0:
                cs.append(float(xa @ xb/(na*nb)))
        return (float(np.mean(cs)), float(np.min(cs))) if cs else (0.0, 0.0)

    prof, prof_min = inv_appariee(YA, YB)
    print(f"# invariance du PROFESSEUR (segment par segment) : {prof:.4f} · "
          f"pire segment {prof_min:.4f}")

    # ---- le pont : entraîné sur A, éprouvé sur A et sur B (même lecture)
    P = Pont((clA, EA, YA), a_, graine, H)
    idx = np.arange(0)
    # naissance : un neurone à la fois, mêmes règles que pont_generatif
    import numpy as _np
    val_max, sans_gain, patience, gain_min = -1.0, 0, 8, 0.0005
    toutes = list(range(n))
    while P.compte_neurones < 120:
        P.nait(1, nouvelle_couche=(P.compte_neurones == 0))
        idx = _np.arange(P.compte_neurones)
        W = P.ajuste(idx, ride, _np.vstack(YA).mean(0), toutes)
        f = P.fid(idx, W, _np.vstack(YA).mean(0), toutes)
        if f > val_max + gain_min:
            val_max = f; sans_gain = 0
        else:
            sans_gain += 1
            if sans_gain >= patience:
                break
    mtA = np.vstack(YA).mean(0)
    W = P.ajuste(idx, ride, mtA, toutes)
    fA = P.fid(idx, W, mtA, toutes)

    P2 = Pont((clB, EB, YB), a_, graine, H)   # MÊMES graine et poids : on rejoue
    # on reconstruit exactement le même réseau sur B en rejouant les naissances
    P2.poids = [tuple(x) for x in P.poids]; P2.couches = list(P.couches)
    P2.compte_neurones = P.compte_neurones
    P2.X = [np.zeros((len(e), 0), dtype=np.float32) for e in P2.E]
    # on recalcule par couche, en réutilisant la généalogie
    P2.X = P2.recalcule(list(range(P2.compte_neurones)), EB)
    fB = P2.evalue(P2.X, YB, W, mtA)
    mB, mBmin = inv_appariee([P2.phi(x) @ W + mtA for x in P2.X],
                             [P.phi(x) @ W + mtA for x in P.X])
    print(f"\n# le PONT (lecture apprise sur A, même lecture appliquée à B)")
    print(f"#   fidélité sur A        : {fA:.4f}")
    print(f"#   fidélité sur B        : {fB:.4f}   (transférée, sans réapprentissage)")
    print(f"#   invariance de SORTIE  : {mB:.4f} · pire segment {mBmin:.4f}")
    print(f"#   taille                : {P.compte_neurones} neurones · "
          f"{len(P.couches)} couches {P.couches}")

    # ---- oracle : ce que la lecture pourrait faire si elle était apprise sur B
    Xb = P2.X
    A_ = P2.phi(np.vstack(Xb)); B_ = np.vstack(YB)
    Wo = np.linalg.solve(A_.T @ A_ + ride*len(A_)*np.eye(A_.shape[1]), A_.T @ (B_ - mtA))
    print(f"#   oracle sur B          : {cos_lignes(A_ @ Wo + mtA, B_):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

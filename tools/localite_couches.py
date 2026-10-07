#!/usr/bin/env python3
"""localite_couches.py — une couche doit-elle quelque chose au CONTEXTE, ou au jeton ?

LA QUESTION, ET ELLE DÉCIDE D'UNE ARCHITECTURE. Notre pont est RÉCURRENT :
`s_t = (1−a)·s_{t−1} + a·tanh(P·s_{t−1} + B·e_t)`. La récurrence n'a de sens que si la
cible dépend du contexte. Si la couche 8 d'un transformer n'était, à chaque position,
qu'une fonction du jeton courant, alors un simple réseau par position suffirait — et une
bonne partie de la machinerie du pont serait de la complexité inutile.

CE QUI EST MESURÉ. À chaque position p, on cherche à prédire `h_c(p)` — la couche c du
professeur — à partir d'une FENÊTRE de la couche 0 : `h_0(p), h_0(p−1), …, h_0(p−k)`.
Régression ridge, forme fermée. On lit :

    R²(0)        ce qu'explique le JETON COURANT seul
    R²(k)        ce qu'explique une fenêtre de k+1 jetons
    gain(k)      R²(k) − R²(0) : ce que le CONTEXTE ajoute

RÉSERVE, ET ELLE EST RÉELLE. C'est une mesure LINÉAIRE. Un professeur peut faire dépendre
`h_c(p)` du contexte d'une façon qu'aucune combinaison linéaire d'une fenêtre ne capte. Un
gain faible ne prouve donc pas que la couche est locale — il prouve qu'**aucune lecture
linéaire** ne tire profit du contexte. C'est exactement le genre de lecture que NOUS
savons construire, donc c'est le chiffre qui nous renseigne, à condition de ne pas le
présenter comme une preuve.

Lecture des traces : DRVF v2, paires ENTRELACÉES (écart, indice absolu si écart==255, puis
valeur), aucune échelle appliquée. On garde toutes les positions, pas une moyenne.

Usage : localite_couches.py <dossier_traces> --couches 1,2,3,5,8 [--fenetre 4]
                            [--langues en] [--ride 1.0] [--max-articles 50]
"""
import glob
import os
import struct
import sys

import numpy as np


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def lire_positions(chemin, couches):
    """{couche: (positions × 896)} — TOUTES les positions, pas une moyenne."""
    voulues = set(couches) | {0}
    par_pos = {c: {} for c in voulues}
    hid = 896
    with open(chemin, "rb") as f:
        if f.read(4) != b"DRVF":
            return None
        version, = struct.unpack("<H", f.read(2))
        nl, hid = struct.unpack("<II", f.read(8))
        while True:
            e = f.read(2)
            if len(e) < 2:
                break
            c, = struct.unpack("<H", e)
            if c == 0xFFFF:
                break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            debut = f.tell()
            buf = f.read(5*n)
            try:
                idx = np.empty(n, dtype=np.int32)
                val = np.empty(n, dtype=np.int32)
                off = prev = 0
                for k in range(n):
                    d = buf[off]
                    off += 1
                    if d == 255:
                        i = buf[off] | (buf[off+1] << 8)
                        off += 2
                    else:
                        i = prev + d
                    prev = i
                    v = buf[off] | (buf[off+1] << 8)
                    if v >= 32768:
                        v -= 65536
                    off += 2
                    idx[k] = i
                    val[k] = v
            except Exception:
                break
            f.seek(debut + off)
            if c in voulues:
                v = np.zeros(hid, dtype=np.float64)
                ok = idx < hid
                v[idx[ok]] = val[ok]
                par_pos[c][pos] = v
    if not all(par_pos[c] for c in voulues):
        return None
    pos = sorted(set.intersection(*[set(par_pos[c]) for c in voulues]))
    return {c: np.vstack([par_pos[c][p] for p in pos]) for c in voulues}


def main():
    d = sys.argv[1]
    cs = [int(x) for x in opt("--couches", "1,2,3,5,8").split(",")]
    K = int(opt("--fenetre", 4))
    ride = float(opt("--ride", 1.0))
    maxi = int(opt("--max-articles", 50))
    gardees = {x.strip() for x in opt("--langues", "").split(",") if x.strip()}
    fs = sorted(glob.glob(os.path.join(d, "*.drvf")))
    if gardees:
        fs = [f for f in fs if os.path.basename(f).partition("_")[0] in gardees]
    vus = set()
    retenus = []
    for f in fs:
        k = os.path.basename(f).partition("_")[2]
        if k not in vus:
            if len(vus) >= maxi:
                continue
            vus.add(k)
        retenus.append(f)
    print(f"# {len(retenus)} traces · fenêtre {K} · ride {ride} · "
          f"{len(vus)} contenus")

    # Grammaires accumulées : on ne matérialise JAMAIS la matrice des features.
    #
    # `G = XᵀX` NE DÉPEND PAS DE LA COUCHE. La première version le recalculait une
    # fois par couche — cinq fois le même produit, soit 30 s par trace au lieu de 7.
    # Sur 300 traces : 2 h 30 au lieu de 35 min. Le BLAS disponible ici fait 6 GFLOPS
    # mono-thread (vérifié : `OPENBLAS_NUM_THREADS=16` ne change rien), donc chaque
    # produit 4480×900×4480 coûte 6 s — ce n'est pas un coût qu'on peut gaspiller.
    nf = 896*(K+1)
    G = np.zeros((nf, nf))
    G0 = np.zeros((896, 896))
    D = {c: np.zeros((nf, 896)) for c in cs}
    D0 = {c: np.zeros((896, 896)) for c in cs}
    somme = {c: np.zeros(896) for c in cs}
    carre = {c: 0.0 for c in cs}
    ntot = 0
    for f in retenus:
        r = lire_positions(f, cs)
        if r is None:
            continue
        E = r[0]
        if len(E) <= K+1:
            continue
        # fenêtre : les K positions précédentes, puis la position courante
        X = np.hstack([np.roll(E, k, axis=0) for k in range(K, -1, -1)])
        X = X[K:]
        Xc = X[:, 896*K:]
        G += X.T @ X
        G0 += Xc.T @ Xc
        for c in cs:
            Y = r[c][K:]
            D[c] += X.T @ Y
            D0[c] += Xc.T @ Y
            somme[c] += Y.sum(0)
            carre[c] += float((Y*Y).sum())
        ntot += len(X)
    print(f"# {ntot} positions appariées", flush=True)

    print(f"\n# {'couche':>7}{'R²(0)':>10}{'R²(fenêtre)':>13}{'gain':>9}"
          f"{'gain relatif':>14}")
    for c in cs:
        # R² global = 1 − SSE/SST. SSE = trace(Wᵀ D) ; SST = Σy² − n·‖μ‖².
        mu = somme[c]/ntot
        sst = carre[c] - ntot*float((mu*mu).sum())
        # SSE, ET NON « trace(WᵀD) ». La première version prenait `trace(WᵀD)` — qui
        # est la partie EXPLIQUÉE, pas l'erreur — pour la somme des carrés résiduels.
        # Le symptôme était des R² NÉGATIFS qui empiraient avec la taille de la
        # fenêtre : un modèle plus grand semblait faire moins bien, ce qui est
        # impossible à pénalité égale (le grand modèle contient le petit). La bonne
        # identité est   SSE = ‖Y‖² − 2·tr(WᵀD) + tr(WᵀGW).
        r2, sse = {}, {}
        for nom, g, dd in (("0", G0, D0[c]), (f"{K}", G, D[c])):
            W = np.linalg.solve(g + ride*ntot*np.eye(g.shape[0]), dd)
            e = carre[c] - 2.0*float(np.trace(W.T @ dd)) + float(np.trace(W.T @ (g @ W)))
            sse[nom] = e
            r2[nom] = 1.0 - e/sst
        r2_0, r2_k = r2["0"], r2[f"{K}"]
        # CONTRÔLE : à pénalité égale, le modèle à fenêtre CONTIENT le modèle local
        # (il suffit d'annuler les blocs décalés), donc sa SSE doit être ≤. Si ce
        # n'est pas le cas, c'est la mesure qui est fausse, pas le professeur.
        assert sse[f"{K}"] <= sse["0"] + 1e-6*max(1.0, sse["0"]), (
            f"couche {c} : SSE(fenetre) {sse[f'{K}']:.1f} > SSE(jeton) {sse['0']:.1f}"
            " - mesure incoherente")
        gain = r2_k - r2_0
        print(f" {c:>7}{r2_0:>10.4f}{r2_k:>13.4f}{gain:>9.4f}"
              f"{(gain/max(1e-12, 1-r2_0)):>13.1%}")
    print(f"\n# R²(0) : le JETON COURANT seul (lecture linéaire de la couche 0).")
    print(f"# gain : ce qu'une fenêtre de {K+1} jetons ajoute — donc ce que le CONTEXTE")
    print(f"# apporte à une lecture LINÉAIRE. « gain relatif » : la part de ce que le")
    print(f"# jeton seul laissait inexpliqué et que le contexte récupère.")
    print(f"# RÉSERVE : mesure LINÉAIRE. Un gain faible ne prouve pas la localité — il")
    print(f"# prouve qu'aucune lecture linéaire n'en tire profit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

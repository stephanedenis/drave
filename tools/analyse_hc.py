#!/usr/bin/env python3
"""analyse_hc.py — les 24 poids d'un raccord à hyper-connexions, relus et jugés.

C'est l'outil de la **porte Drave de P1** (`docs/plan-deepseek41-complet.md`) :
les coefficients de connexion étaient calculés à chaque jeton puis jetés — un
forward muet. Le moteur les écrit maintenant (`DRAVE_DUMP_COUCHES`, noms
`hc_attn` et `hc_ffn`, 24 f32 dans cet ordre : 4 `pre` + 4 `post` + 16 `comb`),
et cet outil répond aux deux questions du plan :

  1. **combien des 16 connexions sont significatives ?** (une matrice de
     Sinkhorn 4×4 bistochastique a une moyenne de 0,25 par entrée : est
     « négligeable » ce qui est très en dessous) ;
  2. **sont-elles stables d'un jeton à l'autre ?** — par entrée (coefficient de
     variation sur les positions) et globalement (corrélation entre matrices de
     positions consécutives).

Il vérifie aussi ce que le Sinkhorn PROMET : lignes et colonnes de `comb`
somment à 1 (à `eps` près). Un `comb` qui ne l'est pas dirait que la
normalisation n'a pas convergé — et personne ne le verrait autrement.

Usage :
    analyse_hc.py <prefixe> [--couches 0,1,2] [--positions 0,1,2,3] [--seuil 0.05]
"""
import os
import struct
import sys

import numpy as np

# Le Sinkhorn promet une matrice bistochastique ; au-delà de cet écart, la
# promesse n'est pas tenue et l'outil sort en erreur (c'est une porte).
TOLERANCE_BISTO = 1e-3


def lire(chemin):
    with open(chemin, "rb") as f:
        return np.frombuffer(f.read(), dtype="<f4").astype(np.float64)


def charge(prefixe, nom, couches, positions):
    """Rend {couche: {pos: (pre, post, comb)}} pour les vidages présents."""
    out = {}
    for l in couches:
        for p in positions:
            chemin = f"{prefixe}-{nom}-{l}-{p}.bin"
            if not os.path.exists(chemin):
                continue
            v = lire(chemin)
            if len(v) != 24:
                print(f"⚠️  {chemin} : {len(v)} valeurs au lieu de 24 — ignoré")
                continue
            out.setdefault(l, {})[p] = (v[:4], v[4:8], v[8:].reshape(4, 4))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    prefixe = sys.argv[1]
    couches = list(range(43))
    positions = [0, 1, 2, 3]
    seuil = 0.05
    for i, a in enumerate(sys.argv):
        if a == "--couches" and i + 1 < len(sys.argv):
            couches = [int(x) for x in sys.argv[i + 1].split(",")]
        if a == "--positions" and i + 1 < len(sys.argv):
            positions = [int(x) for x in sys.argv[i + 1].split(",")]
        if a == "--seuil" and i + 1 < len(sys.argv):
            seuil = float(sys.argv[i + 1])

    for nom in ("hc_attn", "hc_ffn"):
        d = charge(prefixe, nom, couches, positions)
        if not d:
            continue
        n_pos = sum(len(v) for v in d.values())
        print(f"\n=== {nom} : {len(d)} couches × {n_pos // max(len(d),1)} positions ===")
        print(f"{'couche':>7} {'|comb-1|':>9} {'conn.>seuil':>12} {'CV moyen':>9} "
              f"{'corr. pos':>10} {'pre moy':>8} {'post moy':>9}")
        cv_tot, nb_tot, n_tot, corr_tot, ecart_tot = [], 0, 0, [], []
        for l in sorted(d):
            mats = np.array([d[l][p][2] for p in sorted(d[l])])       # (n_pos,4,4)
            pres = np.array([d[l][p][0] for p in sorted(d[l])])
            posts = np.array([d[l][p][1] for p in sorted(d[l])])
            # Le Sinkhorn promet une matrice bistochastique : le vérifier.
            ecart = max(np.abs(mats.sum(axis=1) - 1).max(),
                        np.abs(mats.sum(axis=0) - 1).max())
            ecart_tot.append(ecart)
            # Significatives : au-dessus du seuil, en moyenne sur les positions.
            moy = mats.mean(axis=0)
            nb = int((moy >= seuil).sum())
            cv = float((mats.std(axis=0) / (moy + 1e-12)).mean())
            if len(mats) > 1:
                a = mats[:-1].reshape(len(mats) - 1, -1)
                b = mats[1:].reshape(len(mats) - 1, -1)
                corr = float(np.mean([np.corrcoef(a[i], b[i])[0, 1]
                                      for i in range(len(a))]))
            else:
                corr = float("nan")
            print(f"{l:7d} {ecart:9.2e} {nb:8d}/16 {cv:9.3f} {corr:10.3f} "
                  f"{pres.mean():8.3f} {posts.mean():9.3f}")
            cv_tot.append(cv); nb_tot += nb; n_tot += 16
            if not np.isnan(corr):
                corr_tot.append(corr)
        print(f"\n  connexions significatives (≥ {seuil}) : {nb_tot}/{n_tot} "
              f"({100*nb_tot/max(n_tot,1):.0f} %)")
        print(f"  bistochastique : écart max |somme−1| = {max(ecart_tot):.2e} "
              f"(le Sinkhorn tient sa promesse)"
              if max(ecart_tot) < 1e-3 else
              f"  ⚠️  bistochastique : écart max |somme−1| = {max(ecart_tot):.2e}")
        if corr_tot:
            print(f"  stabilité entre positions consécutives : corrélation moyenne "
                  f"{np.mean(corr_tot):.4f} (min {min(corr_tot):.4f})")
        print(f"  variabilité par entrée : CV moyen {np.mean(cv_tot):.3f} "
              f"(max {max(cv_tot):.3f})")
        if max(ecart_tot) > TOLERANCE_BISTO:
            print(f"❌ PORTE P1 NON TENUE : comb non bistochastique "
                  f"({max(ecart_tot):.2e} > {TOLERANCE_BISTO:g})")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

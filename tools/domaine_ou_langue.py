#!/usr/bin/env python3
"""domaine_ou_langue.py — qu'est-ce qui rapproche deux représentations : le SUJET ou la LANGUE ?

Hypothèse testée : « certains mots et groupes de mots sont spécifiques à leur domaine ;
ils sont plus communs à leur domaine qu'à leur langue. »

Le traçage par unité donne les deux axes à la fois :
  - MÊME unité (même contenu), langues DIFFÉRENTES  -> similarité S_langue
  - MÊME langue, unités DIFFÉRENTES (contenus ≠)    -> similarité S_domaine

Si S_langue > S_domaine, la représentation se rapproche par CONTENU plus que par
langue — l'hypothèse tient. Sinon, la langue domine.

Usage : domaine_ou_langue.py <dossier> [--couches 0,8,10]
"""
import glob, os, sys
import numpy as np
sys.path.insert(0, "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools")
from invariance_unites import lire


def main():
    d = sys.argv[1]
    cs = [int(x) for x in (sys.argv[sys.argv.index("--couches")+1].split(",")
                           if "--couches" in sys.argv else ["0","8","10"])]
    par = {}
    for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
        b = os.path.basename(f)[:-5]
        if "_" not in b: continue
        L, k = b.rsplit("_", 1)
        try: k = int(k)
        except ValueError: continue
        for c in cs:
            hid, v = lire(f, c)
            if v is not None:
                par.setdefault(c, {}).setdefault(L, {})[k] = v
    for c in cs:
        langues = {L: ks for L, ks in par.get(c, {}).items() if len(ks) == 10}
        if len(langues) < 3:
            print(f"couche {c} : {len(langues)} langues complètes — insuffisant"); continue
        noms = sorted(langues)
        # S_langue : même unité, langues différentes
        sl = []
        for k in range(10):
            V = np.array([langues[L][k] for L in noms])
            N = np.linalg.norm(V, axis=1); ok = N > 0
            if ok.sum() < 2: continue
            M = V[ok]/N[ok][:, None]
            S = M @ M.T; iu = np.triu_indices(len(M), 1)
            sl += list(S[iu])
        # S_domaine : même langue, unités différentes
        sd = []
        for L in noms:
            V = np.array([langues[L][k] for k in range(10)])
            N = np.linalg.norm(V, axis=1); ok = N > 0
            if ok.sum() < 2: continue
            M = V[ok]/N[ok][:, None]
            S = M @ M.T; iu = np.triu_indices(len(M), 1)
            sd += list(S[iu])
        ml, md = float(np.mean(sl)), float(np.mean(sd))
        verdict = "CONTENU domine" if ml > md else "LANGUE domine"
        print(f"couche {c:>2} : S_langue {ml:.4f} · S_domaine {md:.4f} · "
              f"écart {ml-md:+.4f}  -> {verdict}")
    print(f"\n({len(noms)} langues, 10 unités chacune)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

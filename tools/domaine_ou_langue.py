#!/usr/bin/env python3
"""domaine_ou_langue.py — qu'est-ce qui rapproche deux représentations : le SUJET ou la LANGUE ?

Hypothèse testée : « certains mots et groupes de mots sont spécifiques à leur domaine ;
ils sont plus communs à leur domaine qu'à leur langue. »

Deux axes, mesurés sur les mêmes représentations :
  - MÊME contenu (même unité, ou même article), langues DIFFÉRENTES -> S_langue
  - MÊME langue, contenus DIFFÉRENTS                                -> S_domaine

Si S_langue > S_domaine, la représentation se rapproche par CONTENU plus que par
langue — l'hypothèse tient. Sinon, la langue domine.

GÉNÉRALISÉ POUR WIKIPEDIA. La version d'origine exigeait des unités NUMÉROTÉES et
exactement dix par langue, ce qui la limitait à l'UDHR. Elle accepte maintenant
n'importe quelle étiquette (les articles Wikipedia s'appellent `en_Albert_Einstein`)
et un nombre d'unités quelconque par langue.

L'UDHR EST MONO-DOMAINE : le même texte juridique dans 392 langues. Le test y est
donc biaisé — les « contenus différents » n'en sont pas vraiment. C'est seulement
avec un corpus MULTI-DOMAINE aligné (482 articles Wikipedia × 6 langues, §45) que
l'hypothèse devient réellement testable.

Usage : domaine_ou_langue.py <dossier> [--couches 0,8,10] [--min-unites 10]
                             [--max-unites 0]
"""
import glob
import os
import sys

import numpy as np

sys.path.insert(0, "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools")
from invariance_unites import lire  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom)+1] if nom in sys.argv else defaut


def main():
    d = sys.argv[1]
    cs = [int(x) for x in opt("--couches", "0,8,10").split(",")]
    min_u = int(opt("--min-unites", 10))
    max_u = int(opt("--max-unites", 0))

    par = {}
    for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
        b = os.path.basename(f)[:-5]
        if "_" not in b:
            continue
        # L'ÉTIQUETTE PEUT CONTENIR DES SOULIGNÉS (« en_Albert_Einstein ») : on
        # coupe au PREMIER souligné, pas au dernier.
        L, k = b.split("_", 1)
        for c in cs:
            hid, v = lire(f, c)
            if v is not None:
                par.setdefault(c, {}).setdefault(L, {})[k] = v

    for c in sorted(par):
        # on ne garde que les contenus présents dans TOUTES les langues : sans cela
        # S_langue porterait sur des paires de contenus différents.
        compte = {}
        for L, ks in par[c].items():
            for k in ks:
                compte[k] = compte.get(k, 0) + 1
        commun = sorted(k for k, n in compte.items() if n == len(par[c]))
        if max_u > 0:
            commun = commun[:max_u]
        if not commun:
            print(f"couche {c} : aucun contenu présent dans les "
                  f"{len(par[c])} langues")
            continue
        noms = sorted(par[c])
        n_u = len(commun)

        def moy_croisee(vecteurs):
            V = np.array(vecteurs)
            N = np.linalg.norm(V, axis=1)
            ok = N > 0
            if ok.sum() < 2:
                return []
            M = V[ok]/N[ok][:, None]
            S = M @ M.T
            iu = np.triu_indices(len(M), 1)
            return list(S[iu])

        sl = []
        for k in commun:
            sl += moy_croisee([par[c][L][k] for L in noms])
        sd = []
        for L in noms:
            sd += moy_croisee([par[c][L][k] for k in commun])
        if not sl or not sd:
            print(f"couche {c} : pas assez de paires"); continue
        ml, md = float(np.mean(sl)), float(np.mean(sd))
        verdict = "CONTENU domine" if ml > md else "LANGUE domine"
        print(f"couche {c:>2} : S_langue {ml:.4f} · S_domaine {md:.4f} · "
              f"écart {ml-md:+.4f}  -> {verdict}")
        print(f"          ({len(noms)} langues · {n_u} contenus communs · "
              f"{len(sl)} paires inter-langues · {len(sd)} paires intra-langue)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

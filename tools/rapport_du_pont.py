#!/usr/bin/env python3
"""rapport_du_pont.py — le rapport contenu/langue de NOTRE pont, panel par panel.

POURQUOI. Le chiffre « le professeur est à 12,001, nous à 2,487 » a servi de boussole.
Or `ancre_professeur.py` et `profil_couches.py` viennent d'établir que ce 12,001 est
mesuré sur TROIS LANGUES ROMANES (es/it/pt) : sur six langues le même professeur, à la
même couche, est à 1,697, et sur sa PIRE paire (de–en) à 1,494. Un chiffre-cible qui
varie d'un facteur 8 selon le panel ne peut pas servir de cible sans être nommé.

Cet outil mesure donc LES DEUX — notre pont et le professeur — sur le MÊME panel, et
donne la table des paires. Le protocole est celui de `discriminant_contenu` : masque des
canaux vivants (≥ 0,5), 120 neurones, lecture quadratique, ride 0,03, graine 5 —
c'est-à-dire la référence du dépôt, pas un réglage choisi pour l'occasion.

RÉSERVE. Quand l'évaluation porte sur le cache d'APPRENTISSAGE, notre chiffre est
IN-SAMPLE et le professeur, lui, ne l'est jamais. La comparaison n'est alors valable que
pour le professeur ; elle est signalée comme telle.

Usage : rapport_du_pont.py <cache_appr.npz> <cache_eval.npz> [--neur 120] [--paires]
"""
import os
import sys
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def decompose(noms, M):
    m = M.mean(0)
    par_l, par_c = {}, {}
    for i, n in enumerate(noms):
        L, _, k = n.partition("_")
        par_l.setdefault(L, []).append(i)
        par_c.setdefault(k, []).append(i)
    comm = [k for k, idx in par_c.items() if len(idx) == len(par_l)]
    if not comm or len(par_l) < 2:
        return None
    Pl = float(np.mean([np.sum((M[idx].mean(0) - m)**2) for idx in par_l.values()]))
    Pc = float(np.mean([np.sum((M[par_c[k]].mean(0) - m)**2) for k in comm]))
    return Pl, Pc, Pc/max(Pl, 1e-12)


def paires(noms, M, titre):
    langues = sorted({n.partition("_")[0] for n in noms})
    if len(langues) < 2:
        return
    res = []
    for a, b in combinations(langues, 2):
        sel = [i for i, n in enumerate(noms) if n.partition("_")[0] in (a, b)]
        r = decompose([noms[i] for i in sel], M[sel]) if len(sel) >= 4 else None
        if r:
            res.append((r[2], a, b, r[0], r[1]))
    if not res:
        return
    print(f"\n# --- paires : {titre} ---")
    print(f"# {'paire':<10}{'P_lang':>10}{'P_cont':>11}{'RAPPORT':>10}")
    tri = sorted(res)
    for r, a, b, pl, pcn in tri:
        print(f" {a+'–'+b:<10}{pl:>10.1f}{pcn:>11.1f}{r:>10.3f}")
    # ATTENTION : `res` est dans l'ordre des combinaisons, PAS trié. Lire `res[0]`
    # comme « la pire » donnait la première paire alphabétique — un résumé faux à
    # côté d'une table juste. On trie une fois et on lit le tri.
    print(f"# pire {tri[0][1]}–{tri[0][2]} {tri[0][0]:.3f} · meilleure "
          f"{tri[-1][1]}–{tri[-1][2]} {tri[-1][0]:.3f} · étalement "
          f"×{tri[-1][0]/max(tri[0][0], 1e-12):.1f}")


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 120))
    part = float(opt("--part", 0.5))
    ride, graine = 0.03, 5

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]
    print(f"# apprentissage {tr_p} ({len(cltr)} entrées, "
          f"{', '.join(sorted({c.partition('_')[0] for c in cltr}))})")
    print(f"# évaluation    {te_p} ({len(clte)} entrées, "
          f"{', '.join(sorted({c.partition('_')[0] for c in clte}))}) · "
          f"{len(garde)} canaux")

    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)
    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    W = P.ajuste(idx, ride, mt, itr)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s) · "
          f"quadratique · ride {ride} · graine {graine}")

    Xt = P.recalcule(idx, Ete)
    Ot = np.vstack([P.phi(P._norm(Xt[k])) @ W + mt for k in range(len(clte))])
    bo = np.cumsum([0] + [len(Yte[k]) for k in range(len(clte))])
    nos = np.vstack([Ot[bo[k]:bo[k+1]].mean(0) for k in range(len(clte))])
    pro = np.vstack([y.mean(0) for y in Yte])
    ft = cos_lignes(Ot, np.vstack(Yte))

    meme = os.path.abspath(tr_p) == os.path.abspath(te_p)
    print(f"\n# fidélité de TEST {ft:.4f}"
          + ("   (ATTENTION : évaluation sur le cache d'APPRENTISSAGE — in-sample "
             "pour nous)" if meme else ""))
    print(f"\n# {'':<14}{'P_lang':>10}{'P_cont':>11}{'RAPPORT':>10}")
    for nom, M in (("PROFESSEUR", pro), ("NOTRE PONT", nos)):
        r = decompose(clte, M)
        print(f"  {nom:<14}{r[0]:>10.1f}{r[1]:>11.1f}{r[2]:>10.3f}")
    rp, rn = decompose(clte, pro), decompose(clte, nos)
    print(f"  {'PART DU PROF':<14}{'':>10}{'':>11}{rn[2]/max(rp[2],1e-12):>9.1%}")
    if "--paires" in sys.argv:
        paires(clte, pro, "PROFESSEUR")
        paires(clte, nos, "NOTRE PONT")
    return 0


if __name__ == "__main__":
    sys.exit(main())

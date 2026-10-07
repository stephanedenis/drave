#!/usr/bin/env python3
"""discriminant_transfert.py — les directions apprises sur un panel servent-elles sur un autre ?

LA QUESTION, ET ELLE EST NEUVE. Le §80 a mesuré qu'un discriminant linéaire appris portait
le rapport contenu/langue à **105 % du professeur**. Mais ce résultat a été obtenu SUR LE
PANEL ROMAN (es/it/pt) et mesuré SUR CE MÊME PANEL. Or le §83 vient d'établir que le
professeur lui-même vaut 12,001 sur ce panel et **1,494 sur sa pire paire (de–en)**.

Un projecteur appris à séparer l'espagnol, l'italien et le portugais sait-il séparer
l'allemand de l'anglais ? Rien ne l'assure : le discriminant maximise `C_cont/C_lang`, et
`C_lang` est estimé sur LES LANGUES DU PANEL D'APPRENTISSAGE. Si l'axe de langue appris est
« l'axe roman », il peut être orthogonal à « l'axe germanique ».

CE QUI EST MESURÉ. Trois caches, quatre cas. Le pont est appris sur `--appr` ; le
discriminant sur `--disc` ; la mesure sur `--eval`. Les cas se lisent deux à deux :
dans-panel contre transfert, dans les deux sens.

    appris      discriminant   évalué        ce que ça dit
    de/en/fr    es/it/pt       es/it/pt      le §80 (référence, dans-panel)
    de/en/fr    es/it/pt       de/en/fr      TRANSFERT roman -> germanique
    de/en/fr    de/en/fr       de/en/fr      dans-panel sur le panel difficile
    de/en/fr    de/en/fr       es/it/pt      TRANSFERT germanique -> roman

ÉCONOMIE DE CALCUL. Le projecteur est AFFINE, donc la moyenne d'une entrée projetée est la
projection de sa moyenne. On ne matérialise jamais les positions : on ne garde que les
MOYENNES par entrée. Le rapport est invariant d'échelle, donc la constante importe peu — on
la garde tout de même pour rester fidèle à `discriminant_contenu`.

Usage : discriminant_transfert.py <appr.npz> <disc.npz> <eval.npz>
                                  [--neur 120] [--rangs 0,2,5,10,20,40] [--paires]
"""
import os
import sys
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge  # noqa: E402


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


def paires(noms, M, titre, indent="   ", ref=None, alpha=1.0):
    """Table des paires. `ref` et `alpha` : table AMPLIFIÉE, avec la part du professeur.

    L'amplification est GLOBALE (une seule constante pour toutes les paires), parce
    qu'on ne peut pas choisir une échelle par paire sur du texte neuf.
    """
    langues = sorted({n.partition("_")[0] for n in noms})
    res = []
    for a, b in combinations(langues, 2):
        sel = [i for i, n in enumerate(noms) if n.partition("_")[0] in (a, b)]
        if len(sel) >= 4:
            r = decompose([noms[i] for i in sel], M[sel])
            if r:
                res.append((r[2], a, b, r[0], r[1]))
    if not res:
        return
    tri = sorted(res)
    print(f"{indent}# {titre} — pire {tri[0][1]}–{tri[0][2]} {tri[0][0]:.3f} · "
          f"meilleure {tri[-1][1]}–{tri[-1][2]} {tri[-1][0]:.3f}")
    print(f"{indent}# " + " · ".join(f"{a}–{b} {r:.2f}" for r, a, b, _, _ in tri))
    if ref is None:
        return
    # table amplifiée : P_cont ramené à celui du professeur, puis part de P_lang
    print(f"{indent}# {'paire':<9}{'P_cont':>9}{'% prof':>9}{'P_lang':>10}"
          f"{'% prof':>9}{'RAPPORT':>9}{'% prof':>9}")
    for r, a, b, pl, pc in tri:
        rr = decompose([noms[i] for i in
                        [j for j, n in enumerate(noms)
                         if n.partition("_")[0] in (a, b)]],
                       ref[[j for j, n in enumerate(noms)
                            if n.partition("_")[0] in (a, b)]])
        pl2, pc2 = pl*alpha*alpha, pc*alpha*alpha
        verdict = "ok" if pl2 <= rr[0] else "P_lang DÉPASSE"
        print(f"{indent}  {a}–{b:<7}{pc2:>9.1f}{pc2/rr[1]:>8.0%}{pl2:>10.1f}"
              f"{pl2/rr[0]:>8.0%}{r:>9.3f}{r/rr[2]:>8.0%}   {verdict}")


def moyennes_sortie(P, idx, W, mt, E):
    """Moyenne, par entrée, de la sortie du pont — sans jamais empiler les positions."""
    X = P.recalcule(idx, E)
    return np.vstack([(P.phi(P._norm(X[k])) @ W + mt).mean(0) for k in range(len(E))])


def moyennes_prof(Y):
    return np.vstack([y.mean(0) for y in Y])


def main():
    tr_p, disc_p, te_p = sys.argv[1], sys.argv[2], sys.argv[3]
    n_neur = int(opt("--neur", 120))
    rangs = [int(x) for x in opt("--rangs", "0,2,5,10,20,40").split(",")]

    cltr, Etr, Ytr, _ = charge(tr_p)
    cldi, Edi, Ydi, _ = charge(disc_p)
    clte, Ete, Yte, _ = charge(te_p)
    # `--langues-disc` : restreindre le PANEL sur lequel le discriminant est appris,
    # sans toucher ni au pont ni à l'évaluation. C'est ce qui permet de demander :
    # « un axe appris sur trois langues vaut-il sur six ? »
    if opt("--langues-disc", ""):
        gard = {x.strip() for x in opt("--langues-disc", "").split(",") if x.strip()}
        sel = [i for i, c in enumerate(cldi) if c.partition("_")[0] in gard]
        print(f"# PANEL DU DISCRIMINANT restreint à {sorted(gard)} : "
              f"{len(sel)} entrées sur {len(cldi)}")
        cldi = [cldi[i] for i in sel]
        Edi = [Edi[i] for i in sel]
        Ydi = [Ydi[i] for i in sel]

    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= 0.5)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Ydi = [y[:, garde] for y in Ydi]
    Yte = [y[:, garde] for y in Yte]
    ncan = len(garde)

    def langs(cl):
        return ",".join(sorted({c.partition("_")[0] for c in cl}))

    print(f"# pont appris sur {langs(cltr)} · discriminant appris sur {langs(cldi)}"
          f" · mesuré sur {langs(clte)} · {ncan} canaux")
    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)
    P = Pont((cltr, Etr, Ytr), 0.2, 5, ncan)
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    W = P.ajuste(idx, 0.03, mt, itr)
    print(f"# {P.compte_neurones} neurones · quadratique · ride 0,03 · graine 5")

    # ------------------------------------------------ le discriminant, sur SON panel
    Mdi = moyennes_sortie(P, idx, W, mt, Edi)
    mdi = Mdi.mean(0)
    pc, pl = {}, {}
    for i, n in enumerate(cldi):
        L, _, k = n.partition("_")
        pl.setdefault(L, []).append(i)
        pc.setdefault(k, []).append(i)
    comm = [k for k, v in pc.items() if len(v) == len(pl)]

    def covg(M, par):
        C = np.zeros((ncan, ncan))
        for v in par.values():
            d = M[v].mean(0) - mdi
            C += np.outer(d, d)
        return C/max(len(par), 1)

    Cc, Cl = covg(Mdi, {k: pc[k] for k in comm}), covg(Mdi, pl)
    lam = max(1e-2*np.trace(Cl)/ncan, 1e-12)
    w, V = np.linalg.eigh(np.linalg.solve(Cl + lam*np.eye(ncan), Cc))
    V = V[:, np.argsort(-w)]
    print(f"# plancher {lam:.3e} · {len(comm)} contenus · {len(pl)} langues · "
          f"valeurs propres " + " ".join(f"{x:.1f}" for x in np.sort(w)[::-1][:6]))

    # ------------------------------------------------ la mesure, sur le panel d'évaluation
    Mte = moyennes_sortie(P, idx, W, mt, Ete)
    Mpr = moyennes_prof(Yte)
    rp = decompose(clte, Mpr)
    rn = decompose(clte, Mte)
    print(f"\n# {'':<22}{'P_lang':>10}{'P_cont':>11}{'RAPPORT':>10}{'part prof':>11}")
    print(f"  {'PROFESSEUR':<20}{rp[0]:>10.1f}{rp[1]:>11.1f}{rp[2]:>10.3f}{'':>11}")
    print(f"  {'NOTRE PONT (rang 0)':<20}{rn[0]:>10.1f}{rn[1]:>11.1f}{rn[2]:>10.3f}"
          f"{rn[2]/rp[2]:>10.1%}")
    for r in rangs:
        if r == 0:
            continue
        Vr = V[:, :r]
        Mp = (Mte - mdi) @ Vr @ Vr.T + mdi
        d = decompose(clte, Mp)
        etiq = f"NOTRE PONT (rang {r})"
        print(f"  {etiq:<20}{d[0]:>10.1f}{d[1]:>11.1f}{d[2]:>10.3f}"
              f"{d[2]/rp[2]:>10.1%}")
        # L'ÉCHELLE N'EST PAS UN DÉFAUT. `P_lang` et `P_cont` sont TOUS DEUX
        # quadratiques en l'amplitude (§67) : une seule constante multiplie les deux
        # par le même facteur et laisse le rapport — donc la fidélité, qui est un
        # cosinus — exactement inchangés. Comparer nos deux énergies BRUTES à celles
        # du professeur revient donc à compter un défaut qui n'en est pas un. La
        # question qui compte est : une fois l'énergie de contenu RAMENÉE à celle du
        # professeur, où tombe celle de langue ? Le critère du §62.3 est « P_cont
        # proche du professeur ET P_lang qui ne le dépasse pas ».
        if d[1] > 0:
            a = float(np.sqrt(rp[1]/d[1]))
            print(f"  {'  ↳ amplifié ×'+format(a, '.2f'):<20}"
                  f"{d[0]*a*a:>10.1f}{d[1]*a*a:>11.1f}{d[2]:>10.3f}"
                  f"{d[2]/rp[2]:>10.1%}"
                  f"   (P_lang {d[0]*a*a/rp[0]:.0%} · P_cont 100 %)")
    if "--paires" in sys.argv:
        paires(clte, Mte, "rang 0 — NOTRE PONT")
        for r in rangs:
            if r:
                Vr = V[:, :r]
                Mp = (Mte - mdi) @ Vr @ Vr.T + mdi
                d = decompose(clte, Mp)
                a = float(np.sqrt(rp[1]/d[1])) if d[1] > 0 else 1.0
                paires(clte, Mp, f"rang {r}", ref=Mpr, alpha=a)
    print(f"\n# Le discriminant est APPRIS sur le panel « {langs(cldi)} » et MESURÉ sur"
          f" « {langs(clte)} ».")
    print(f"# Si les deux sont le même, c'est la référence du §80. Sinon, c'est un")
    print(f"# TRANSFERT — et c'est la question : un axe de langue appris sur un panel")
    print(f"# sait-il séparer les langues d'un autre ?")
    return 0


if __name__ == "__main__":
    sys.exit(main())

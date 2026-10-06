#!/usr/bin/env python3
"""PROFIL PAR LANGUE — la norme de la cible explique-t-elle la fidélité ?

LA QUESTION. La fidélité du pont est un COSINUS (mesurée ligne à ligne) : elle
est donc insensible à l'échelle. Pourtant les langues du corpus n'ont pas la même
NORME de représentation — mesuré 282 à 537 selon la langue sur 22 langues (§26 du
rapport). Si la norme joue un rôle, ce ne peut donc PAS être dans la métrique :
ce ne peut être que dans le FIT.

LA RÉGRESSION AUX MOINDRES CARRÉS MINIMISE UNE ERREUR ABSOLUE. Une langue dont
les cibles ont une norme double contribue QUATRE FOIS plus à l'objectif. La
lecture partagée est donc tirée vers les langues « fortes », au détriment des
langues « faibles » — alors même que la métrique finale est neutre.

PRÉDICTION, ÉCRITE AVANT LA MESURE : la fidélité par langue doit être
NÉGATIVEMENT corrélée à la norme de sa cible.

Ce script ne fait AUCUNE croissance : il naît un réseau de taille fixe, ajuste
une lecture, et profile. C'est un diagnostic, pas un résultat de modèle.

Usage : profil_langues.py <cache_appr.npz> <cache_test.npz> [--neur 40] [--part 0.5]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def rang(v):
    """Rangs moyens (gère les ex æquo) — pour une corrélation de Spearman."""
    v = np.asarray(v, dtype=float)
    o = np.argsort(v)
    r = np.empty(len(v), dtype=float)
    r[o] = np.arange(len(v), dtype=float)
    # moyenne des rangs sur les groupes d'égaux
    for val in np.unique(v):
        m = v == val
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def corr(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    p = float(np.corrcoef(x, y)[0, 1])
    s = float(np.corrcoef(rang(x), rang(y))[0, 1])
    return p, s


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 40))
    part = float(opt("--part", 0.5))
    a, graine, ride = 0.2, 5, 0.3

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    print(f"# {len(cltr)} langues d'apprentissage · {len(clte)} langues de test · H={H}")

    # --- norme AVANT tout masque : c'est le périmètre du §26, pour comparaison
    norme_pleine = {cl: float(np.linalg.norm(Yte[i], axis=1).mean())
                    for i, cl in enumerate(clte)}

    # --- masque des canaux PARTAGÉS, calculé sur l'apprentissage SEUL
    vivant = np.zeros(Ytr[0].shape[1])
    for i in range(len(cltr)):
        vivant += ((Ytr[i] != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(cltr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]
    print(f"# canaux partagés : {len(garde)}/{H} ({len(garde)/H:.0%}) — "
          f"présents dans au moins {part:.0%} des langues d'apprentissage")

    # --- un réseau de taille FIXE. On ne cherche pas le meilleur : on mesure
    #     si la lecture partagée sert également toutes les langues.
    P = Pont((cltr, Etr, Ytr), a, graine, len(garde))
    P.quadratique = True
    P.nait(n_neur, True)
    print(f"# réseau : {P.compte_neurones} neurones · {len(P.couches)} couche(s) "
          f"{P.couches} · lecture quadratique")

    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)
    idx = np.arange(P.compte_neurones)

    # --- trajectoires du TEST
    Xte = P.recalcule(idx, Ete)

    def profil(W, nom):
        lignes = []
        for k, cl in enumerate(clte):
            A = P.phi(P._norm(Xte[k])) @ W + mt
            B = Yte[k]
            # ORACLE PAR LANGUE : une lecture ajustée SUR la langue elle-même.
            # Diagnostic, pas modèle. Il sépare deux causes que la fidélité seule
            # confond : des CARACTÉRISTIQUES qui ne portent pas le contenu (oracle
            # bas lui aussi), ou un PARTAGE qui sert mal certaines langues (oracle
            # haut alors que la lecture commune est basse).
            Ao = P.phi(P._norm(Xte[k]))
            Wo = np.linalg.solve(Ao.T @ Ao + ride*len(Ao)*np.eye(Ao.shape[1]),
                                 Ao.T @ (B - mt))
            lignes.append({
                "cl": cl,
                "fid": cos_lignes(A, B),
                "oracle": cos_lignes(Ao @ Wo + mt, B),
                "temoin": cos_lignes(np.tile(mt, (len(B), 1)), B),
                "norme": float(np.linalg.norm(B, axis=1).mean()),
                "norme_pleine": norme_pleine[cl],
                "pas": len(B),
            })
        f = [r["fid"] for r in lignes]
        n = [r["norme"] for r in lignes]
        orc = [r["oracle"] for r in lignes]
        tem = [r["temoin"] for r in lignes]
        p, s = corr(n, f)
        print(f"\n=== {nom} ===")
        print(f"#   fidélité TEST moyenne {np.mean(f):.4f} · Pearson norme→fid {p:+.4f} "
              f"· Spearman {s:+.4f}")
        print(f"#   TÉMOIN CONSTANT par langue : moyenne {np.mean(tem):.4f} "
              f"· écart du pont {np.mean(f)-np.mean(tem):+.4f}")
        print(f"#   ORACLE par langue          : moyenne {np.mean(orc):.4f} "
              f"· écart au pont {np.mean(orc)-np.mean(f):+.4f}")
        print(f"#   oracle ↔ norme : Pearson {corr(n, orc)[0]:+.4f} · "
              f"Spearman {corr(n, orc)[1]:+.4f}")
        gain = np.array(orc) - np.array(f)
        print(f"#   (oracle − pont) ↔ norme : Pearson {corr(n, gain)[0]:+.4f}   "
              f"← positif = les langues à forte norme sont celles que le PARTAGE "
              f"pénalise")
        o = np.argsort(n)
        q = len(o)//4
        qs = []
        for sl in (o[:q], o[q:2*q], o[2*q:3*q], o[3*q:]):
            qs.append(np.mean([f[j] for j in sl]))
        print(f"#   par quartile de norme : Q1 {qs[0]:.4f} · Q2 {qs[1]:.4f} · "
              f"Q3 {qs[2]:.4f} · Q4 {qs[3]:.4f}   (Q4-Q1 {qs[3]-qs[0]:+.4f})")
        # LONGUEUR. `norme` et `pas` sont fortement confondus : il faut donc les
        # séparer, sinon on attribue à la norme ce qui vient de la longueur.
        # Toutes les corrélations sont calculées ICI, où l'indexation est
        # cohérente — une transcription manuelle d'un tableau trié vers l'ordre du
        # cache a déjà produit un jeu de corrélations entièrement faux.
        lp = np.log([r["pas"] for r in lignes])
        p2, s2 = corr(lp, f)
        p3, s3 = corr(lp, n)
        print(f"#   fid ↔ log(pas)  : Pearson {p2:+.4f} · Spearman {s2:+.4f}")
        print(f"#   norme ↔ log(pas): Pearson {p3:+.4f} · Spearman {s3:+.4f}")
        f_, n_ = np.asarray(f, float), np.asarray(n, float)

        def part(x, y, z):
            ex = x - np.polyval(np.polyfit(z, x, 1), z)
            ey = y - np.polyval(np.polyfit(z, y, 1), z)
            return float(np.corrcoef(ex, ey)[0, 1])
        print(f"#   fid ↔ norme   | log(pas) : {part(f_, n_, lp):+.4f}")
        print(f"#   fid ↔ log(pas)| norme    : {part(f_, lp, n_):+.4f}")
        return lignes

    # --- FIT ORDINAIRE : l'objectif est absolu, la métrique est un cosinus.
    lignes = profil(P.ajuste(idx, ride, mt, itr), "FIT ORDINAIRE (référence)")

    # --- FIT PONDÉRÉ : chaque langue pèse selon 1/norme², donc erreur relative.
    #     PRÉDICTION, écrite avant la mesure : si l'effet vient de la PONDÉRATION
    #     du fit, la corrélation doit se rapprocher de zéro et Q4 doit remonter.
    #     S'il vient d'une difficulté INTRINSÈQUE des langues à forte norme, la
    #     pondération ne fera que déplacer le problème (Q4 plat, Q1 qui baisse).
    P.pese = [1.0/max(float(np.linalg.norm(Ytr[i], axis=1).mean()), 1e-9)**2
              for i in range(len(cltr))]
    profil(P.ajuste(idx, ride, mt, itr), "FIT PONDÉRÉ PAR LANGUE (1/norme²)")
    P.pese = None

    print(f"\n# DÉTAIL (trié par norme décroissante)")
    print(f"{'langue':<10} {'fidélité':>9} {'norme':>8} {'norme 896':>10} {'pas':>5}")
    for r in sorted(lignes, key=lambda r: -r["norme"]):
        print(f"{r['cl']:<10} {r['fid']:>9.4f} {r['norme']:>8.1f} "
              f"{r['norme_pleine']:>10.1f} {r['pas']:>5}")

    # --- CSV : pour que toute analyse ultérieure parte des NOMS et jamais d'un
    #     tableau trié recopié à la main (erreur déjà commise, corrélations
    #     entièrement fausses).
    csv = opt("--csv", "/tmp/profil_langues.csv")
    with open(csv, "w") as fh:
        fh.write("langue;fidelite;oracle;temoin;norme;norme896;pas\n")
        for r in lignes:
            fh.write(f"{r['cl']};{r['fid']:.6f};{r['oracle']:.6f};{r['temoin']:.6f};{r['norme']:.3f};"
                     f"{r['norme_pleine']:.3f};{r['pas']}\n")
    print(f"# table écrite : {csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

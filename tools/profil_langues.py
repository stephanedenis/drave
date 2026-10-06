#!/usr/bin/env python3
"""PROFIL PAR LANGUE — le pont sert-il également toutes les langues ?

CE QUI A ÉTÉ ÉTABLI (§27 du rapport), et qui commande ce script :

  1. `corr(fidélité, témoin constant) = +0,977`. La fidélité d'une langue est
     presque entièrement le témoin constant : son classement ne dit RIEN du pont.
  2. Ce qu'il faut regarder, c'est l'APPORT PROPRE `fidélité − témoin`. Il est
     prédit par la FRAGMENTATION du tokeniseur (jetons/caractère), R² 0,67, et
     ce n'est pas un effet de marge (R² 0,013 pour `1 − témoin`).
  3. Sur `heb` l'apport vaut +0,0014 : rien. Sur `deu`, `jpn`, `kor`, `srp` la
     constante est mauvaise et le pont n'y ajoute rien. Ces langues ne sont pas
     servies.

L'HYPOTHÈSE TESTÉE ICI. La quantité de contenu par jeton varie de 6× selon la
langue (1,578 jeton/caractère en pular contre 0,271 en allemand). Le réservoir
avait UNE constante de temps, donc UNE échelle de mémoire : la même en jetons,
donc 6× différente en contenu. On lui donne des constantes ÉTALÉES
logarithmiquement — le réservoir devient multi-échelle et choisit lui-même.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si la mémoire mono-échelle est la limite,
l'apport doit augmenter PRÉFÉRENTIELLEMENT sur les langues faiblement
fragmentées (deu 0,271 · pam 0,332 · tpi 0,352), c'est-à-dire là où le pont
n'apporte rien aujourd'hui.

Usage : profil_langues.py <cache_appr.npz> <cache_test.npz> [--neur 40] [--part 0.5]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402

SOURCE = "/tmp/udhr10_toutes"


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def rang(v):
    v = np.asarray(v, dtype=float)
    o = np.argsort(v)
    r = np.empty(len(v), dtype=float)
    r[o] = np.arange(len(v), dtype=float)
    for val in np.unique(v):
        m = v == val
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def corr(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return float(np.corrcoef(x, y)[0, 1]), \
        float(np.corrcoef(rang(x), rang(y))[0, 1])


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 40))
    part = float(opt("--part", 0.5))
    a, graine, ride = 0.2, 5, 0.3

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    print(f"# {len(cltr)} langues d'apprentissage · {len(clte)} langues de test · H={H}")

    norme_pleine = {cl: float(np.linalg.norm(Yte[i], axis=1).mean())
                    for i, cl in enumerate(clte)}

    vivant = np.zeros(Ytr[0].shape[1])
    for i in range(len(cltr)):
        vivant += ((Ytr[i] != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(cltr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]
    print(f"# canaux partagés : {len(garde)}/{H} ({len(garde)/H:.0%})")

    # fragmentation : jetons par caractère, mesurée sur le texte source. Elle est
    # calculable à l'inférence à partir du seul tokeniseur, sans aucune étiquette.
    tk = {}
    for i, cl in enumerate(clte):
        p = os.path.join(SOURCE, cl + ".txt")
        n = len(open(p, encoding="utf-8", errors="replace").read()) if os.path.exists(p) else 0
        tk[cl] = len(Yte[i])/max(n, 1)

    itr = np.arange(len(cltr))
    # DEUX PANNEAUX, comme l'exige le protocole. Le TEST est HORS VIVIER (langues
    # jamais vues). La VALIDATION est du MÊME VIVIER que l'apprentissage : elle dit
    # si un écart vient du transfert ou des caractéristiques. Un langage
    # d'apprentissage sur sept est mis de côté — il sert à la validation ET reste
    # dans le vivier dont `mt` est tiré.
    ival = itr[::7]
    iap = np.array([i for i in itr if i not in set(ival.tolist())])
    print(f"# vivier : {len(iap)} langues d'ajustement · {len(ival)} de validation "
          f"(même vivier) · {len(clte)} de test (hors vivier)")
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)
    Ev = [Etr[i] for i in ival]
    Yv = [Ytr[i] for i in ival]

    def oracle_sur(P, W, Ek, Yk):
        """Un ajustement PRIVÉ sur le jeu évalué : diagnostic, pas modèle."""
        Xk = P.recalcule(np.arange(P.compte_neurones), Ek)
        A = P.phi(np.vstack(Xk))
        B = np.vstack(Yk)
        Wo = np.linalg.solve(A.T @ A + ride*len(A)*np.eye(A.shape[1]), A.T @ (B - mt))
        return cos_lignes(A @ Wo + mt, B), cos_lignes(A @ W + mt, B)

    def mesure(a_min, a_max, nom):
        P = Pont((cltr, Etr, Ytr), a, graine, len(garde))
        P.quadratique = True
        P.a_min, P.a_max = a_min, a_max
        P.nait(n_neur, True)
        idx = np.arange(P.compte_neurones)
        # la lecture est ajustée sur le VIVIER D'AJUSTEMENT, pas sur la validation
        W = P.ajuste(idx, ride, mt, iap)
        Xte = P.recalcule(idx, Ete)
        lignes = []
        for k, cl in enumerate(clte):
            B = Yte[k]
            A = P.phi(P._norm(Xte[k]))
            lignes.append({
                "cl": cl,
                "fid": cos_lignes(A @ W + mt, B),
                "oracle": cos_lignes(
                    A @ np.linalg.solve(A.T @ A + ride*len(A)*np.eye(A.shape[1]),
                                        A.T @ (B - mt)) + mt, B),
                "temoin": cos_lignes(np.tile(mt, (len(B), 1)), B),
                "norme": float(np.linalg.norm(B, axis=1).mean()),
                "norme_pleine": norme_pleine[cl],
                "pas": len(B),
                "frag": tk[cl],
            })
        f = np.array([r["fid"] for r in lignes])
        g = np.array([r["fid"] - r["temoin"] for r in lignes])
        o = np.array([r["oracle"] for r in lignes])
        t = np.array([r["temoin"] for r in lignes])
        n = np.array([r["norme"] for r in lignes])
        fr = np.array([r["frag"] for r in lignes])
        print(f"\n=== {nom} ===")
        if P.a_min is not None:
            av = np.array(P.a_neur)
            print(f"#   constantes de temps : {av.min():.3f} à {av.max():.3f} "
                  f"(médiane {np.median(av):.3f})")
        else:
            print(f"#   constante de temps unique : {a}")
        print(f"#   TAILLE DU RÉSEAU : {P.compte_neurones} neurones · "
              f"{len(P.couches)} couche(s) {P.couches} · "
              f"{P.phi(np.zeros((1, P.compte_neurones))).shape[1]} caractéristiques")
        print(f"#   TEST       (hors vivier) : fidélité {f.mean():.4f} · "
              f"témoin {t.mean():.4f} · APPORT {g.mean():+.4f} · oracle {o.mean():.4f}")
        ov, nv = oracle_sur(P, W, Ev, Yv)
        tv = np.mean([cos_lignes(np.tile(mt, (len(Yv[i]), 1)), Yv[i])
                      for i in range(len(Yv))])
        print(f"#   VALIDATION (même vivier) : fidélité {nv:.4f} · témoin {tv:.4f} · "
              f"APPORT {nv-tv:+.4f} · oracle {ov:.4f}")
        print(f"#   écart à l'oracle : TEST (hors vivier) {o.mean()-f.mean():+.4f} · "
              f"VALIDATION (même vivier) {ov-nv:+.4f}")
        print(f"#   apport ↔ fragmentation : Pearson {corr(fr, g)[0]:+.4f} "
              f"(R² {corr(fr, g)[0]**2:.4f})")
        print(f"#   apport ↔ norme         : Pearson {corr(n, g)[0]:+.4f}")
        print(f"#   oracle ↔ norme         : Pearson {corr(n, o)[0]:+.4f}")
        return lignes, g

    ref, g_ref = mesure(None, None, "MONO-ÉCHELLE (référence, a=0,2)")
    a_min = float(opt("--a-min", 0.02))
    a_max = float(opt("--a-max", 0.8))
    multi, g_mul = mesure(a_min, a_max, f"MULTI-ÉCHELLE (a de {a_min} à {a_max})")

    # --- la comparaison qui répond à la prédiction
    d = g_mul - g_ref
    fr = np.array([r["frag"] for r in ref])
    print(f"\n=== EFFET DU MULTI-ÉCHELLE SUR L'APPORT PROPRE ===")
    print(f"#   apport moyen : {g_ref.mean():+.4f} → {g_mul.mean():+.4f} "
          f"({d.mean():+.4f})")
    print(f"#   PRÉDICTION : l'effet doit être plus grand là où la fragmentation est "
          f"FAIBLE")
    print(f"#   corrélation (effet) ↔ fragmentation : Pearson {corr(fr, d)[0]:+.4f}")
    cl = [r["cl"] for r in ref]
    o = np.argsort(fr)
    print(f"\n#{'langue':<7}{'frag':>7}{'apport réf':>12}{'apport multi':>14}{'effet':>9}")
    for j in o:
        print(f" {cl[j]:<7}{fr[j]:>7.3f}{g_ref[j]:>+12.4f}{g_mul[j]:>+14.4f}"
              f"{d[j]:>+9.4f}")

    csv = opt("--csv", "/tmp/profil_langues.csv")
    with open(csv, "w") as fh:
        fh.write("langue;frag;norme;norme896;pas;temoin;fid_ref;oracle_ref;"
                 "apport_ref;fid_multi;apport_multi\n")
        for i, r in enumerate(ref):
            fh.write(f"{r['cl']};{r['frag']:.4f};{r['norme']:.3f};"
                     f"{r['norme_pleine']:.3f};{r['pas']};{r['temoin']:.6f};"
                     f"{r['fid']:.6f};{r['oracle']:.6f};{g_ref[i]:.6f};"
                     f"{multi[i]['fid']:.6f};{g_mul[i]:.6f}\n")
    print(f"\n# table écrite : {csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

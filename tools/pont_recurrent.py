#!/usr/bin/env python3
"""pont_recurrent.py — notre pont linguistique-sémantique, appris en BOÎTE NOIRE.

MISSION (clarifiée par Stéphane) : **pas** reproduire le gros modèle couche par
couche. Construire un modèle **récurrent à n couches** qui rend, pour n'importe
quelle langue, **le premier niveau abstrait** du gros modèle — celui où la
représentation cesse d'être dominée par la langue.

Le gros modèle est une BOÎTE NOIRE : on ne prend que son entrée et sa sortie.
`--trace-flux` les donne toutes les deux — la couche 0 EST la plongée du jeton,
et la couche L EST la cible.

  s_t = A·s_{t−1} + B·e_t        état récurrent (le « pont »)
  ŷ_t = s_t                       la sortie visée est l'état abstrait

Ajustement par MOINDRES CARRÉS (crête, forme fermée) — pas de rétropropagation,
pas de gradient. Puis essai en BOUCLE FERMÉE : on part de zéro et on laisse la
récurrence courir, sans jamais lui donner l'état du professeur.

Usage : pont_recurrent.py <dossier_train> <dossier_test> [--couche 10] [--rang 64]
"""
import glob, os, struct, sys
from itertools import combinations
import numpy as np


def lire(chemin):
    def paires(f, n, version, bloc=32):
        ech = None
        if version == 3:
            nb, = struct.unpack("<I", f.read(4))
            ech = [struct.unpack("<e", f.read(2))[0] for _ in range(nb)]
        out, prev = [], 0
        for _ in range(n):
            if version == 1:
                i, = struct.unpack("<I", f.read(4))
            else:
                e, = struct.unpack("<B", f.read(1))
                i = struct.unpack("<H", f.read(2))[0] if e == 255 else prev + e
                prev = i
            if version == 3:
                v, = struct.unpack("<b", f.read(1))
                out.append((i, v * (ech[i // bloc] if ech else 1.0)))
            else:
                v, = struct.unpack("<h", f.read(2))
                out.append((i, v))
        return out

    with open(chemin, "rb") as f:
        assert f.read(4) == b"DRVF"
        version, = struct.unpack("<H", f.read(2))
        n_layer, hidden = struct.unpack("<II", f.read(8))
        pp = {}
        while True:
            b = f.read(2)
            if len(b) < 2: break
            c, = struct.unpack("<H", b)
            if c == 0xFFFF: break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            pp[(c, pos)] = paires(f, n, version)
    return hidden, pp


def seq(pp, c, hidden):
    """La séquence ordonnée des vecteurs de la couche c."""
    positions = sorted(p for (cc, p) in pp if cc == c)
    M = np.zeros((len(positions), hidden), dtype=np.float32)
    for k, p in enumerate(positions):
        for i, v in pp[(c, p)]:
            if i < hidden: M[k, i] = v
    return M


def cos_moyen(V):
    """Cosinus moyen de toutes les paires de lignes."""
    n = np.linalg.norm(V, axis=1, keepdims=True)
    n[n == 0] = 1
    U = V / n
    S = U @ U.T
    iu = np.triu_indices(len(V), 1)
    return float(S[iu].mean()), float(S[iu].min())


def main():
    dtr, dte = sys.argv[1], sys.argv[2]
    c = int(sys.argv[sys.argv.index("--couche") + 1]) if "--couche" in sys.argv else 10
    rang = int(sys.argv[sys.argv.index("--rang") + 1]) if "--rang" in sys.argv else 64
    tr, te = {}, {}
    for d, dst in ((dtr, tr), (dte, te)):
        for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
            hidden, pp = lire(f)
            dst[os.path.basename(f)[:-5]] = (seq(pp, 0, hidden), seq(pp, c, hidden))
    hidden = list(tr.values())[0][1].shape[1]

    # --- rang réduit : on ajuste dans un sous-espace, sinon 896x896 sur quelques
    #     centaines d'exemples est sous-déterminé et la crête ferait tout le travail
    Y = np.vstack([y for _, y in tr.values()])
    moy = Y.mean(axis=0)
    U, S, Vt = np.linalg.svd(Y - moy, full_matrices=False)
    P = Vt[:rang].T                       # (hidden, rang) : le sous-espace abstrait
    Z = {l: (y - moy) @ P for l, (_, y) in tr.items()}

    # --- ajustement de s_t = A s_{t-1} + B e_t, en moindres carrés (crête)
    Xs, Ys = [], []
    for l, (e, _) in tr.items():
        z = Z[l]
        for t in range(1, len(z)):
            Xs.append(np.concatenate([z[t - 1], e[t]]))
            Ys.append(z[t])
    Xs = np.array(Xs, dtype=np.float64); Ys = np.array(Ys, dtype=np.float64)
    lam = 1e-2 * len(Xs)
    W = np.linalg.solve(Xs.T @ Xs + lam * np.eye(Xs.shape[1]), Xs.T @ Ys)
    A = W[:rang].T; B = W[rang:].T
    # **Le rayon spectral commande tout.** Un ajustement en UN PAS peut être
    # excellent alors que la BOUCLE FERMÉE diverge : c'est le mode d'échec
    # classique d'une récurrence apprise par moindres carrés. On le mesure, et on
    # ramène le rayon sous 1 — sinon on ne teste pas le pont, on teste une
    # explosion.
    rho = float(max(abs(np.linalg.eigvals(A))))
    cible = float(sys.argv[sys.argv.index("--rho") + 1]) if "--rho" in sys.argv else 0.95
    if rho > 0:
        A = A * (cible / rho)
    rho2 = float(max(abs(np.linalg.eigvals(A))))
    print(f"# A : rayon spectral {rho:.3f} -> {rho2:.3f} (ramené à {cible})")
    print(f"# professeur : couche {c} · {hidden} canaux · sous-espace de rang {rang}")
    print(f"# entraînement : {len(tr)} langues ({len(Xs)} pas) · test : {len(te)} langues JAMAIS vues")
    print(f"# étudiant : s_t = A s_(t-1) + B e_t  — A {A.shape}, B {B.shape}")

    # --- BOUCLE FERMÉE, sur les langues tenues à l'écart
    def etudiant(e):
        s = np.zeros(rang)
        out = np.zeros((len(e), rang))
        for t in range(len(e)):
            s = A @ s + B @ e[t]
            out[t] = s
        return out

    # fidélité en UN PAS (professeur donné) — sépare « le pont est faux » de
    # « la boucle diverge »
    Xs2, Ys2 = [], []
    for l, (e, _) in {**tr, **te}.items():
        z = (({**tr, **te}[l][1]) - moy) @ P
        for t in range(1, len(z)):
            Xs2.append(np.concatenate([z[t-1], e[t]])); Ys2.append(z[t])
    Xs2 = np.array(Xs2); Ys2 = np.array(Ys2)
    P1 = Xs2 @ W
    n1 = np.linalg.norm(Ys2, axis=1); n2 = np.linalg.norm(P1, axis=1)
    ok = (n1 > 0) & (n2 > 0)
    un_pas = float((np.sum(Ys2[ok]*P1[ok], axis=1)/(n1[ok]*n2[ok])).mean())
    print(f"\n# fidélité en UN PAS (professeur donné) : {un_pas:.4f}")
    # TÉMOIN SANS RÉCURRENCE : y_t prédit par une application linéaire de e_t SEUL.
    # Sans lui, on ne saurait pas si la récurrence apporte quoi que ce soit — ou si
    # tout le signal est déjà dans la plongée du jeton courant.
    Xe, Ye = [], []
    for l, (e, y) in {**tr, **te}.items():
        z = (y - moy) @ P
        for t in range(len(z)):
            Xe.append(e[t]); Ye.append(z[t])
    Xe = np.array(Xe); Ye = np.array(Ye)
    W0 = np.linalg.solve(Xe.T @ Xe + 1e-2 * len(Xe) * np.eye(Xe.shape[1]), Xe.T @ Ye)
    Q = Xe @ W0
    n1 = np.linalg.norm(Ye, axis=1); n2 = np.linalg.norm(Q, axis=1)
    ok = (n1 > 0) & (n2 > 0)
    sans_rec = float((np.sum(Ye[ok]*Q[ok], axis=1)/(n1[ok]*n2[ok])).mean())
    print(f"# TÉMOIN sans récurrence (linéaire de e_t seul) : {sans_rec:.4f}")

    # --- LE CHIFFRE QUI DÉCIDE DE LA MISSION : ce pont LINÉAIRE, à lui seul,
    #     reproduit-il l'INVARIANCE INTER-LANGUE du professeur ?
    prof = np.array([te[l][1][-1] for l in sorted(te)])
    lin  = np.array([ (te[l][0][-1] @ W0) @ P.T + moy for l in sorted(te)])
    mp, mip = cos_moyen(prof)
    ml, mil = cos_moyen(lin)
    print(f"\n# INVARIANCE INTER-LANGUE (dernière position, langues JAMAIS vues) :")
    print(f"#   professeur (couche {c})            : cos moyen {mp:.4f} · pire paire {mip:.4f}")
    print(f"#   pont LINÉAIRE de la plongée seule : cos moyen {ml:.4f} · pire paire {mil:.4f}")
    print(f"\n{'langue':<6} {'cos(étudiant, professeur)':>26}")
    cs = []
    for l, (e, y) in sorted(te.items()):
        z = (y - moy) @ P
        zh = etudiant(e.astype(np.float64))
        n1 = np.linalg.norm(z, axis=1); n2 = np.linalg.norm(zh, axis=1)
        ok = (n1 > 0) & (n2 > 0)
        cc = float((np.sum(z[ok] * zh[ok], axis=1) / (n1[ok] * n2[ok])).mean())
        cs.append(cc)
        print(f"{l:<6} {cc:>26.4f}")
    print(f"\n# fidélité moyenne à la boîte noire : {np.mean(cs):.4f}")

    # --- SAUVEGARDE DE L'ARTEFACT : c'est ce qui fait du pont un OBJET utilisable
    #     et pas seulement une mesure. `pont_semantique.npz` porte les trois pièces
    #     (W sous-espace, moy, W0) et `outils_pont.py` sait l'appliquer.
    chemin = os.environ.get("DRAVE_PONT_SORTIE", "pont_semantique.npz")
    np.savez(chemin, P=P, moy=moy, W0=W0, couche=c, rang=rang,
             langues_train=np.array(sorted(tr)), langues_test=np.array(sorted(te)))
    print(f"# artefact écrit : {chemin}  (P {P.shape}, W0 {W0.shape}, moy {moy.shape})")
    print(f"#   usage : python3 tools/applique_pont.py {chemin} <trace.drvf>")

    # --- LE CHIFFRE QUI COMPTE : le pont est-il aussi invariANT que le professeur ?
    def dernier(dst, cle):
        return np.array([dst[l][cle][-1] for l in sorted(dst)])
    prof = dernier(te, 1)
    etu = np.array([etudiant(e.astype(np.float64))[-1] for l, (e, y) in sorted(te.items())])
    mp, mip = cos_moyen(prof)
    me, mie = cos_moyen(etu)
    print(f"\n# INVARIANCE INTER-LANGUE à la dernière position, langues tenues à l'écart :")
    print(f"#   professeur (couche {c}) : cos moyen {mp:.4f} · pire paire {mip:.4f}")
    print(f"#   étudiant RÉCURRENT (écarté — voir le témoin) : cos moyen {me:.4f} · pire paire {mie:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

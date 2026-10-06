#!/usr/bin/env python3
"""invariance_unites.py — l'invariance par UNITÉ, dix points au lieu d'un.

L'outil multilingue mesure l'invariance entre TOUTES les paires d'entrées. Ici les
entrées sont appariées par unité : le fichier `<langue>_<k>.drvf` est la k-ième
unité de cette langue, et toutes les langues disent la MÊME unité k. On mesure
donc, pour chaque k, la similarité entre langues — et « la pire paire » porte
enfin sur une unité précise et nommable au lieu d'être un agrégat.

Usage : invariance_unites.py <dossier> --couche 10 [--masque fichier.npz]
"""
import glob, os, re, struct, sys
import numpy as np


def lire(chemin, couche):
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
                out.append((i, v*(ech[i//bloc] if ech else 1.0)))
            else:
                v, = struct.unpack("<h", f.read(2))
                out.append((i, v))
        return out

    pos_voulues = {}
    tronque = False
    with open(chemin, "rb") as f:
        assert f.read(4) == b"DRVF"
        version, = struct.unpack("<H", f.read(2))
        nl, hid = struct.unpack("<II", f.read(8))
        while True:
            b = f.read(2)
            if len(b) < 2:
                break
            c, = struct.unpack("<H", b)
            if c == 0xFFFF:
                break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            # UNE TRACE INTERROMPUE LAISSE UNE QUEUE TRONQUÉE : un traçage arrêté
            # en cours d'écriture produit un fichier valide jusqu'à un point et
            # coupé après. On garde ce qui a été lu au lieu de tout perdre — sans
            # quoi un simple arrêt rend le fichier inexploitable.
            try:
                pp = paires(f, n, version)
            except Exception:
                tronque = True
                break
            if c == couche:
                pos_voulues[pos] = pp
    if tronque:
        print(f"  (tronquée : {os.path.basename(chemin)} — on garde ce qui est lisible)")
    if not pos_voulues:
        return hid, None
    p = max(pos_voulues)
    v = np.zeros(hid)
    for i, val in pos_voulues[p]:
        if i < hid:
            v[i] = val
    return hid, v


def inv(V):
    n = np.linalg.norm(V, axis=1, keepdims=True); n[n == 0] = 1
    S = (V/n) @ (V/n).T
    iu = np.triu_indices(len(V), 1)
    return float(S[iu].mean()), float(S[iu].min()), S


def main():
    d = sys.argv[1]
    c = int(sys.argv[sys.argv.index("--couche")+1]) if "--couche" in sys.argv else 10
    masque = None
    if "--masque" in sys.argv:
        z = np.load(sys.argv[sys.argv.index("--masque")+1], allow_pickle=True)
        masque = z["garde"] if "garde" in z else None
    par_unite = {}
    for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
        m = re.match(r"(.+)_(\d+)\.drvf$", os.path.basename(f))
        if not m:
            continue
        L, k = m.group(1), int(m.group(2))
        hid, v = lire(f, c)
        if v is None:
            continue
        if masque is not None:
            v = v[masque]
        par_unite.setdefault(k, {})[L] = v
    if not par_unite:
        print("aucun fichier au format <langue>_<k>.drvf"); return 1
    print(f"# {len(par_unite)} unités · {len(next(iter(par_unite.values())))} langues max "
          f"· couche {c}" + (" · masque appliqué" if masque is not None else ""))
    print(f"\n{'unité':>6} {'langues':>8} {'invariance':>11} {'pire paire':>11}   pire couple")
    tot, pires = [], []
    for k in sorted(par_unite):
        noms = sorted(par_unite[k])
        V = np.array([par_unite[k][L] for L in noms])
        if len(V) < 2:
            continue
        m, mi, S = inv(V)
        iu = np.triu_indices(len(noms), 1)
        j = int(np.argmin(S[iu]))
        couple = f"{noms[iu[0][j]]}–{noms[iu[1][j]]}"
        tot.append(m); pires.append(mi)
        print(f"{k:>6} {len(noms):>8} {m:>11.4f} {mi:>11.4f}   {couple}")
    if tot:
        print(f"\nMOYENNE sur {len(tot)} unités : invariance {np.mean(tot):.4f} · "
              f"pire paire {np.mean(pires):.4f}")
        print(f"pire unité : {np.min(tot):.4f} · pire paire absolue {np.min(pires):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

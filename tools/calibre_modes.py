#!/usr/bin/env python3
"""calibre_modes.py — le mode DENSE trace-t-il la même chose que le mode ÉVÉNEMENTIEL ?

POURQUOI LA QUESTION SE POSE. Le mode par défaut du moteur construit ses listes
d'événements **au chargement** : sur Qwen2.5-0.5B, 15,6 M d'événements pour ~6 s,
à chaque invocation. Le calcul par jeton, lui, est identique (mesuré : 32,4 contre
32,3 ms/jeton). Sur un corpus de 455 langues tracées une par une, ces 6 s fixes
coûtent **45 minutes** — d'où l'envie de tracer en `--dense`.

MAIS TOUT CE DÉPÔT A ÉTÉ TRACÉ EN MODE ÉVÉNEMENTIEL. Changer de mode sans le
mesurer rendrait le nouveau corpus incomparable à l'ancien sans que rien ne le
dise. Le moteur annonce déjà, ailleurs, que les deux chemins diffèrent
légèrement (corrélations 0,998 contre 0,9998 contre la référence) — ce n'est pas
« identique », c'est « proche », et « proche » doit se chiffrer.

CE QUI EST MESURÉ : pour chaque langue, les mêmes positions, la même couche, et
la similarité cosinus entre les deux traces. On rapporte le cosinus minimum, la
moyenne, et la norme relative — parce qu'un vecteur trois fois plus petit mais
colinéaire ne se voit pas dans un cosinus seul.

Usage : calibre_modes.py <dossier_textes> <sortie_temp> [--langues eng,fra,deu]
                         [--modele models/Qwen2.5-0.5B-Q8_0.gguf] [--ctx 256]
"""
import glob
import os
import struct
import subprocess
import sys

import numpy as np


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def lire(chemin):
    """{couche: (positions × 896)} — paires ENTRELACÉES, cf. flux_codec.decoder."""
    out, hid = {}, 896
    with open(chemin, "rb") as f:
        if f.read(4) != b"DRVF":
            return None
        version, = struct.unpack("<H", f.read(2))
        nl, hid = struct.unpack("<II", f.read(8))
        par_pos = {}
        while True:
            b = f.read(2)
            if len(b) < 2:
                break
            c, = struct.unpack("<H", b)
            if c == 0xFFFF:
                break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            debut = f.tell()
            buf = f.read(5*n)
            try:
                idx = np.empty(n, dtype=np.int32); val = np.empty(n, dtype=np.int32)
                off = prev = 0
                for k in range(n):
                    d = buf[off]; off += 1
                    if d == 255:
                        i = buf[off] | (buf[off+1] << 8); off += 2
                    else:
                        i = prev + d
                    prev = i
                    v = buf[off] | (buf[off+1] << 8)
                    if v >= 32768:
                        v -= 65536
                    off += 2
                    idx[k] = i; val[k] = v
            except Exception:
                break
            f.seek(debut + off)
            v = np.zeros(hid)
            ok = idx < hid
            v[idx[ok]] = val[ok]
            par_pos.setdefault(c, {})[pos] = v
        for c, d in par_pos.items():
            p = sorted(d)
            out[c] = np.vstack([d[x] for x in p])
    return out


def trace(modele, texte, sortie, ctx, dense):
    cmd = ["./drave-core/target/release/drave", modele, "--infer", "--ctx", str(ctx),
           "--couches", "0:24", "--lot", "1", "--n", "0",
           "--trace-couches", ",".join(str(i) for i in range(24)),
           "--prompt", texte, "--trace-flux", sortie]
    if dense:
        cmd.insert(2, "--dense")
    r = subprocess.run(cmd, capture_output=True)
    return r.returncode == 0 and os.path.exists(sortie)


def main():
    dossier = sys.argv[1]
    tmp = sys.argv[2]
    langues = [x.strip() for x in opt("--langues", "eng,fra,deu,spa,rus,ell,jpn,tha").split(",")]
    modele = opt("--modele", "models/Qwen2.5-0.5B-Q8_0.gguf")
    ctx = int(opt("--ctx", 256))
    os.makedirs(tmp, exist_ok=True)
    print(f"# {len(langues)} langues · modèle {modele} · ctx {ctx}")
    print(f"# {'langue':<8}{'positions':>10}{'cos min':>10}{'cos moyen':>11}"
          f"{'‖dense‖/‖évén‖':>16}")
    tous = []
    for L in langues:
        f = os.path.join(dossier, f"{L}.txt")
        if not os.path.exists(f):
            print(f"  {L:<8} absent"); continue
        texte = open(f, encoding="utf-8").read().strip()
        a, b = os.path.join(tmp, f"{L}.ev.drvf"), os.path.join(tmp, f"{L}.de.drvf")
        if not trace(modele, texte, a, ctx, False):
            print(f"  {L:<8} traçage ÉVÉNEMENTIEL en échec"); continue
        if not trace(modele, texte, b, ctx, True):
            print(f"  {L:<8} traçage DENSE en échec"); continue
        A, B = lire(a), lire(b)
        if not A or not B:
            print(f"  {L:<8} lecture impossible"); continue
        cs, rap = [], []
        npos = 0
        for c in sorted(set(A) & set(B)):
            m = min(len(A[c]), len(B[c]))
            if m == 0:
                continue
            x, y = A[c][:m], B[c][:m]
            nx = np.linalg.norm(x, axis=1); ny = np.linalg.norm(y, axis=1)
            ok = (nx > 0) & (ny > 0)
            if not ok.any():
                continue
            cs += list(np.sum(x[ok]*y[ok], axis=1)/(nx[ok]*ny[ok]))
            rap += list(ny[ok]/nx[ok])
            npos = max(npos, m)
        if cs:
            cs = np.array(cs); rap = np.array(rap)
            tous += list(cs)
            print(f"  {L:<8}{npos:>10}{cs.min():>10.4f}{cs.mean():>11.4f}"
                  f"{rap.mean():>16.3f}")
    if tous:
        t = np.array(tous)
        print(f"\n# SUR TOUT : cos minimum {t.min():.4f} · moyen {t.mean():.4f} · "
              f"5ᵉ centile {np.percentile(t, 5):.4f}")
        print(f"# Un cosinus de 0,999 signifie que les deux modes tracent la même "
              f"chose à 0,1 % près de direction.")
        print(f"# Un cosinus plus bas signifie que le corpus tracé en dense n'est PAS "
              f"comparable aux corpus tracés en événementiel — et il faut le dire.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

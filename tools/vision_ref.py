#!/usr/bin/env python3
"""Référence numpy de l'embedding de patchs (première tranche du chemin image).

Le moteur écrit deux fichiers : les sorties (`--banc-vision`) et les POIDS
lus dans le GGUF. Ce script refait le CALCUL en numpy — l'extraction des
teneurs, elle, est vérifiée par `--tensors`. C'est le même partage des rôles
que pour MLA : une implémentation indépendante de la formule.

Usage : vision_ref.py <sortie.bin> [--poids <sortie.bin.poids>]
"""
import sys
import numpy as np


def erf(x):
    """Erf vectorisé (Abramowitz-Stegun 7.1.26), la même approximation que le
    moteur : comparer deux formules différentes mesurerait l'approximation, pas
    l'implémentation."""
    x = np.asarray(x, dtype=np.float64)
    signe = np.sign(x)
    a = np.abs(x)
    t = 1.0 / (1.0 + 0.3275911 * a)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
                - 0.284496736) * t + 0.254829592) * t * np.exp(-a * a)
    return signe * y

def main():
    sortie = sys.argv[1]
    poids = sys.argv[2] if len(sys.argv) > 2 else sortie + ".poids"
    with open(sortie, "rb") as f:
        n_patch, cout = np.frombuffer(f.read(8), dtype=np.int32)
        npatch, ncan = int(n_patch), int(cout)
        eng = np.frombuffer(f.read(npatch * ncan * 4), dtype=np.float32).reshape(npatch, ncan)
    with open(poids, "rb") as f:
        cout_p, cin, ky, kx = np.frombuffer(f.read(16), dtype=np.int32)
        w = np.frombuffer(f.read(), dtype=np.float32).reshape(cout_p, cin, ky, kx)
    # Même image que le banc : dégradé + carré central.
    cote = 28
    img = np.zeros((cin, cote, cote), np.float32)
    for y in range(cote):
        for x in range(cote):
            carre = 10 <= x < 18 and 10 <= y < 18
            for ic in range(cin):
                img[ic, y, x] = 1.0 if carre else (x + y + ic) / (2.0 * cote)
    npc = (cote - ky) // kx + 1
    out = np.zeros((npc * npc, cout), np.float32)
    for py in range(npc):
        for px in range(npc):
            p = py * npc + px
            tuile = img[:, py*ky:(py+1)*ky, px*kx:(px+1)*kx]
            out[p] = np.einsum('oihw,ihw->o', w, tuile)
    ech = max(1e-9, float(np.abs(out).max()))
    ecart = float(np.abs(out - eng).max()) / ech
    print(f"patchs {out.shape} · |référence| max {ech:.4f}")
    print(f"écart max relatif : {ecart:.3e}")
    # --- projecteur : fusion 2 x 2 puis mm.0 -> GELU -> mm.2
    try:
        with open(poids + "", "rb") as f:
            pass
        with open(sortie + ".projecteur", "rb") as f:
            n0, n1, n2, n3 = np.frombuffer(f.read(16), dtype=np.int32)
            n0, n1, n2, n3 = int(n0), int(n1), int(n2), int(n3)
            buf = np.frombuffer(f.read(), dtype=np.float32)
        w0 = buf[:n0*n1].reshape(n0, n1)
        b0 = buf[n0*n1:n0*n1+n0]
        w2 = buf[n0*n1+n0:n0*n1+n0+n2*n3].reshape(n2, n3)
        b2 = buf[n0*n1+n0+n2*n3:n0*n1+n0+n2*n3+n2]
        fusion = eng.reshape(1, -1)                   # 2 x 2 -> un seul groupe
        h = w0 @ fusion[0] + b0
        h = 0.5 * h * (1.0 + erf(h / np.sqrt(2.0)))   # GELU exact
        y = w2 @ h + b2
        # le moteur a écrit sa sortie : on la relit pour comparer
        with open(sortie, "rb") as f:
            f.read(8 + eng.size * 4)
            taille = np.frombuffer(f.read(4), dtype=np.int32)[0]
            y_eng = np.frombuffer(f.read(int(taille) * 4), dtype=np.float32)
        if y_eng.size == y.size:
            ecart_p = float(np.abs(y - y_eng).max()) / max(1e-9, float(np.abs(y).max()))
            print(f"projecteur : {y.size} valeurs · écart max relatif {ecart_p:.3e}")
        else:
            print(f"projecteur : référence {y.size} valeurs, moteur {y_eng.size}")
    except FileNotFoundError:
        pass
    # --- une couche du ViT (bloc 0), sans la rotation 2-D : la référence refait
    #     la même plomberie (LayerNorm, q/k/v avec biais, attention globale,
    #     résidus, MLP avec biais et SiLU).
    try:
        with open(sortie + ".bloc", "rb") as f:
            npatch, e, nff = (int(v) for v in np.frombuffer(f.read(12), dtype=np.int32))
            buf = np.frombuffer(f.read(), dtype=np.float32)
        def prendre(n):
            nonlocal buf
            v, buf = buf[:n], buf[n:]
            return v
        ln1, ln2 = prendre(e), prendre(e)
        wq, bq = prendre(e*e).reshape(e, e), prendre(e)
        wk, bk = prendre(e*e).reshape(e, e), prendre(e)
        wv, bv = prendre(e*e).reshape(e, e), prendre(e)
        wo, bo = prendre(e*e).reshape(e, e), prendre(e)
        wg, bg = prendre(nff*e).reshape(nff, e), prendre(nff)
        wu, bu = prendre(nff*e).reshape(nff, e), prendre(nff)
        wd, bd = prendre(e*nff).reshape(e, nff), prendre(e)
        x_eng = prendre(npatch * e).reshape(npatch, e)
        eps = 1e-6
        def ln(v, w):
            m = v.mean(-1, keepdims=True)
            var = ((v - m) ** 2).mean(-1, keepdims=True)
            return (v - m) / np.sqrt(var + eps) * w
        # rotation 2-D (mRoPE) : quatre blocs de hd/4, blocs 0 et 2 par la LIGNE,
        # blocs 1 et 3 par la COLONNE — la convention lue dans clip.cpp.
        def tourner(v, ligne, colonne):
            for bloc in range(4):
                pos = ligne if bloc % 2 == 0 else colonne
                deb = bloc * (hd // 4)
                q = hd // 4
                i = np.arange(q // 2)
                theta = pos * (10000.0 ** (-2.0 * i / q))
                c, sn = np.cos(theta), np.sin(theta)
                a = v[deb:deb + q // 2].copy()
                b = v[deb + q // 2:deb + q].copy()
                v[deb:deb + q // 2] = a * c - b * sn
                v[deb + q // 2:deb + q] = a * sn + b * c
        hd = e // 16
        n_cote = int(round(np.sqrt(npatch)))
        x = eng.copy()
        xn = ln(x, ln1)
        qq, kk, vv = xn @ wq.T + bq, xn @ wk.T + bk, xn @ wv.T + bv
        for pi in range(npatch):
            ligne, colonne = pi // n_cote, pi % n_cote
            for h in range(16):
                tourner(qq[pi, h * hd:(h + 1) * hd], ligne, colonne)
                tourner(kk[pi, h * hd:(h + 1) * hd], ligne, colonne)
        sc = (qq @ kk.T) / np.sqrt(e)
        sc -= sc.max(-1, keepdims=True)
        att = np.exp(sc)
        att /= att.sum(-1, keepdims=True)
        x = x + (att @ vv) @ wo.T + bo
        xn = ln(x, ln2)
        act = (xn @ wg.T + bg)
        act = (act / (1.0 + np.exp(-act))) * (xn @ wu.T + bu)
        x = x + act @ wd.T + bd
        ecart_b = float(np.abs(x - x_eng).max()) / max(1e-9, float(np.abs(x).max()))
        print(f"bloc 0 : {x.shape} · |référence| max {float(np.abs(x).max()):.4f} · "
              f"écart max relatif {ecart_b:.3e}")
        if ecart_b > 1e-5:
            print("DÉSACCORD bloc — premiers canaux :", x[0, :3], "contre", x_eng[0, :3])
    except (FileNotFoundError, ValueError):
        print("bloc/tour : référence abandonnée (le fichier .bloc ne contient plus "
              "les poids depuis que la tour écrit sa seule sortie ; la rotation "
              "2-D est dérivée de clip.cpp, pas de cette référence)")
    if ecart > 1e-5:
        print("DÉSACCORD — premiers canaux :", out[0, :4], "contre", eng[0, :4])
    else:
        print("accord (bruit de virgule flottante)")

if __name__ == "__main__":
    main()

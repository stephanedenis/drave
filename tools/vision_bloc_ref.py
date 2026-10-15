#!/usr/bin/env python3
"""vision_bloc_ref.py — la tour de vision du moteur, refaite en numpy **À POIDS ÉGAUX**.

POURQUOI CE SCRIPT, ET EN QUOI IL DIFFÈRE DES DEUX AUTRES RÉFÉRENCES.

  * `tools/vision_ref.py` (10/10) refait l'**embedding de patchs** — et il a été écrit **d'après les
    hypothèses du moteur**, donc il ne pouvait pas les mettre en défaut ;
  * `tools/vision_hf_ref.py` (15/10) confronte le moteur à `transformers`, une implémentation
    **indépendante** — c'est lui qui a trouvé les vrais bugs (biais des LayerNorm, convention de
    rotation) — mais il compare des poids **différents** (f32 contre Q8_0) : son écart mêle donc la
    quantification et les conventions ;
  * **ce script-ci** refait la formule en numpy **sur les poids que le moteur a réellement lus**
    (`DRAVE_VISION_POIDS=1` → `<sortie>.poidsbloc`, déquantifiés du Q8_0). L'écart qu'il mesure ne
    peut donc venir **que des conventions** — et c'est ce qu'on veut savoir.

Mesure du 15/10 sur le bloc 0 : **cosinus +1,00000059**, écart max relatif **5,94e-06** (l'arrondi
f32) — les conventions du moteur sont **justes**, et l'écart de 7,45 % qu'on mesurait contre la
référence f32 est de la **quantification**.

Usage :
  DRAVE_VISION_POIDS=1 DRAVE_VISION_NOYAU=noyau.f32 DRAVE_VISION_COUCHES=32 \\
      drave <mmproj> --banc-vision /tmp/tour.bin
  python tools/vision_bloc_ref.py --tour /tmp/tour.bin --poids /tmp/tour.bin.poidsbloc [--couches 32]
"""
from __future__ import annotations

import argparse
import pathlib
import struct

import numpy as np


def lire_entete(chemin: str, n_entiers: int = 2) -> np.ndarray:
    b = pathlib.Path(chemin).read_bytes()
    dims = struct.unpack_from(f"<{n_entiers}i", b, 0)
    return np.frombuffer(b, dtype="<f4", offset=4 * n_entiers).reshape(*dims)


def ln(v, w, bias, eps=1e-6):
    m = v.mean(-1, keepdims=True)
    var = ((v - m) ** 2).mean(-1, keepdims=True)
    return (v - m) / np.sqrt(var + eps) * w + bias


def tourner(v, ligne, colonne, hd):
    """La rotation 2-D, dans la convention de la SOURCE (Qwen2-VL) :
    `rotate_half` apparie i et i + hd/2 ; 20 fréquences ligne puis 20 colonne ; 10000^(-j/20)."""
    demi = hd // 2
    nf = demi // 2
    for j in range(nf):
        f = 10000.0 ** (-j / nf)
        for base, pos in ((j, ligne), (nf + j, colonne)):
            th = pos * f
            c, s = np.cos(th), np.sin(th)
            a, b = v[base], v[base + demi]
            v[base] = a * c - b * s
            v[base + demi] = a * s + b * c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tour", required=True, help="fichier .bin du banc (embedding + sortie)")
    ap.add_argument("--poids", required=True, help="fichier .poidsbloc (DRAVE_VISION_POIDS=1)")
    ap.add_argument("--couches", type=int, default=1,
                    help="nombre de couches à refaire (⚠ le fichier de poids ne porte QUE la couche "
                         "déchargée par DRAVE_VISION_POIDS : au-delà de 1, la formule rejouerait la "
                         "même couche, ce qui ne prouve rien — le script le dit)")
    a = ap.parse_args()

    brut = pathlib.Path(a.poids).read_bytes()
    e, nff, nh, couche_poids = struct.unpack_from("<iiii", brut, 0)
    # Les tenseurs sont écrits DANS L'ORDRE du moteur, sans étiquette (c'est le même ordre que
    # `poids_bloc` dans `run_banc_vision`) : on les consomme donc en séquence, avec un curseur.
    # (La première version de ce script faisait cela dans une lambda qui modifiait une variable
    # globale — illisible et fragile ; réécrit en fonction.)
    curseur = [16]

    def pr(n: int) -> np.ndarray:
        deb = curseur[0]
        curseur[0] = deb + 4 * n
        return np.frombuffer(brut, dtype="<f4", offset=deb, count=n).copy()

    ln1, ln1b, ln2, ln2b = pr(e), pr(e), pr(e), pr(e)
    wq, bq = pr(e * e).reshape(e, e), pr(e)
    wk, bk = pr(e * e).reshape(e, e), pr(e)
    wv, bv = pr(e * e).reshape(e, e), pr(e)
    wo, bo = pr(e * e).reshape(e, e), pr(e)
    w1, b1 = pr(nff * e).reshape(nff, e), pr(nff)
    w2, b2 = pr(e * nff).reshape(e, nff), pr(e)

    if a.couches > 1:
        print(f"  ⚠️ --couches {a.couches} : le fichier de poids ne porte que la COUCHE "
              f"{couche_poids} — au-delà d'une couche, la formule rejouerait la même. Vérifier une "
              f"couche profonde demande `DRAVE_VISION_POIDS=<l>` et son propre déchargement.")
        return 1
    x = lire_entete(a.tour)          # l'embedding de patchs écrit par le banc
    npatch = x.shape[0]
    hd = e // nh
    n_cote = int(round(np.sqrt(npatch)))
    for couche in range(a.couches):
        xn = ln(x, ln1, ln1b)
        qq, kk, vv = xn @ wq.T + bq, xn @ wk.T + bk, xn @ wv.T + bv
        for pi in range(npatch):
            ligne, colonne = pi // n_cote, pi % n_cote
            for h in range(nh):
                tourner(qq[pi, h * hd:(h + 1) * hd], ligne, colonne, hd)
                tourner(kk[pi, h * hd:(h + 1) * hd], ligne, colonne, hd)
        sc = (qq @ kk.T) / np.sqrt(hd)
        sc -= sc.max(-1, keepdims=True)
        att = np.exp(sc)
        att /= att.sum(-1, keepdims=True)
        x = x + (att @ vv) @ wo.T + bo
        xn2 = ln(x, ln2, ln2b)
        act = xn2 @ w1.T + b1
        act = act / (1.0 + np.exp(-1.702 * act))          # quick-GELU, comme la source
        x = x + act @ w2.T + b2
        fichier = f"{a.tour}.couche{couche_poids}"
        if not pathlib.Path(fichier).exists():
            print(f"  ⚠️ {fichier} absent : le moteur n'a pas été lancé avec DRAVE_VISION_COUCHES")
            return 1
        eng = lire_entete(fichier)
        cos = float((x.ravel() @ eng.ravel()) / (np.linalg.norm(x) * np.linalg.norm(eng) + 1e-12))
        ecart = float(np.abs(x - eng).max() / max(1e-9, np.abs(x).max()))
        print(f"couche {couche_poids} À POIDS ÉGAUX : numpy {np.linalg.norm(x):.4f} · "
              f"moteur {np.linalg.norm(eng):.4f} · cosinus {cos:+.8f} · écart max relatif {ecart:.3e}")
        if ecart > 1e-4:
            print("  ❌ les CONVENTIONS diffèrent (l'écart ne peut pas venir de la quantification, "
                  "les poids sont les mêmes)")
            return 1
    print("\n  ✅ les conventions du moteur sont celles de la formule (l'écart restant contre une "
          "référence f32 est de la QUANTIFICATION)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

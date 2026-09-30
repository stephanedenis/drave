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

def main():
    sortie = sys.argv[1]
    poids = sys.argv[2] if len(sys.argv) > 2 else sortie + ".poids"
    with open(sortie, "rb") as f:
        n_patch, cout = np.frombuffer(f.read(8), dtype=np.int32)
        eng = np.frombuffer(f.read(), dtype=np.float32).reshape(int(n_patch), int(cout))
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
    if ecart > 1e-5:
        print("DÉSACCORD — premiers canaux :", out[0, :4], "contre", eng[0, :4])
    else:
        print("accord (bruit de virgule flottante)")

if __name__ == "__main__":
    main()

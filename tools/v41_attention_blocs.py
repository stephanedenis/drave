#!/usr/bin/env python3
"""Le CŒUR de l'attention d'une couche COMPRESSÉE : fenêtre brute + blocs.

C'est la dernière pièce de l'attention jamais vérifiée : `v41_attention_coeur.py`
couvre la couche 0 (ratio 0, fenêtre seule), celui-ci ajoute les BLOCS COMPRESSÉS
et la règle de visibilité (`n_visible = (pos+1)/ratio` : un bloc n'est visible
qu'une fois complet), puis compare la somme pondérée au vide `attn_brut`.

  clés  = les latents post-rotation des positions [debut_fenetre, pos]   (dq kv_rope)
        + les blocs `comp_bloc<b>` pour b = 0..n_vis-1
  score = (q_h · clé) / sqrt(head_dim)   ·   puits appris, BRUT, dans le softmax
  somme = Σ poids · clé

Usage : python3 tools/v41_attention_blocs.py <modele.gguf> <prefixe_dump> <couche> <pos> [ratio]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier_v41_mhc import Gguf, dump


def principale():
    modele, prefixe, couche, pos = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    ratio = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    g = Gguf(modele)
    nom = lambda s: f"blk.{couche}.{s}"
    hd = g.tenseurs[nom("attn_kv.weight")][0][1]
    nh = g.tenseurs[nom("attn_q_b.weight")][0][1] // hd
    fenetre = 128
    n = pos + 1
    debut = n - fenetre if n > fenetre else 0
    n_vis = n // ratio
    q = dump(prefixe, "q_rope", couche, pos)
    cles = [dump(prefixe, "kv_rope", couche, t) for t in range(debut, n)]
    noms_blocs = []
    for b in range(n_vis):
        for essai in (f"comp_bloc{b}",):
            try:
                cles.append(dump(prefixe, essai, couche, pos - (n - 1 - (b + 1) * ratio + ratio - 1)))
                noms_blocs.append(b)
            except FileNotFoundError:
                pass
    # les blocs sont vidés à la POSITION où ils sont publiés : `pos = (b+1)*ratio - 1`
    cles = [dump(prefixe, "kv_rope", couche, t) for t in range(debut, n)]
    for b in range(n_vis):
        p_bloc = (b + 1) * ratio - 1
        cles.append(dump(prefixe, f"comp_bloc{b}", couche, p_bloc))
    puits = g.lire(nom("attn_sinks.weight")).ravel()
    scale = 1.0 / np.sqrt(hd)
    sortie = np.zeros(nh * hd)
    for h in range(nh):
        qh = q[h * hd:(h + 1) * hd]
        sc = np.array([float(qh @ k) for k in cles]) * scale
        logits = np.concatenate([sc, [float(puits[h])]])
        e = np.exp(logits - logits.max())
        w = e / e.sum()
        acc = np.zeros(hd)
        for t, k in enumerate(cles):
            acc += w[t] * k
        sortie[h * hd:(h + 1) * hd] = acc
    ref = dump(prefixe, "attn_brut", couche, pos)
    print(f"couche {couche} pos {pos} (ratio {ratio}) : {len(cles)} clés "
          f"({n - debut} fenêtre + {n_vis} blocs) · écart max {np.max(np.abs(sortie - ref)):.3e} "
          f"(dynamique {np.max(np.abs(ref)):.3e}) · normes {np.linalg.norm(sortie):.4f} / "
          f"{np.linalg.norm(ref):.4f}")


if __name__ == "__main__":
    principale()

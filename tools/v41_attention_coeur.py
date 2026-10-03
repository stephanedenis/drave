#!/usr/bin/env python3
"""Référence numpy du CŒUR de l'attention V4.1 : scores, softmax (puits), somme
pondérée, dé-rotation et sortie groupée.

Suite de `v41_attention_reference.py` (projections, normes et rotations vérifiées
à 1e-6). Ici on recompose, depuis les vides du moteur et les tenseurs du fichier :

    scores_h(t) = (q_h · kv_t) / sqrt(head_dim)        pour t = 0..pos
    logits      = [scores…, puits_h]                   (le puits entre BRUT)
    w           = softmax(logits)
    attn_brut_h = Σ_t w_t · kv_t                       ← vide `attn_brut`
    dé-rotation = RoPE INVERSE sur les n_rot dernières composantes
    oa_g        = W_o_a[g] · sortie[g·gdim..]           (Q8_0, par groupe de têtes)
    attn_out    = W_o_b · oa                           ← vide `attn_out`

À ctx ≤ window et pour une couche de ratio 0, toutes les positions 0..pos sont
visibles et il n'y a aucun bloc compressé : c'est une attention causale ordinaire.

Usage : python3 tools/v41_attention_coeur.py <modele.gguf> <prefixe_dump> <couche> <pos>
"""
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from verifier_v41_mhc import Gguf, dump
from v41_attention_reference import matvec_q8_0, rope_norm, BASE


def principale():
    modele, prefixe, couche, pos = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    g = Gguf(modele)
    nom = lambda s: f"blk.{couche}.{s}"
    hd = g.tenseurs[nom("attn_kv.weight")][0][1]          # 512
    nh = g.tenseurs[nom("attn_q_b.weight")][0][1] // hd   # 64
    # `wo_a` : [gdim, n_groups · o_lora] · `wo_b` : [n_groups · o_lora, hidden].
    # On dérive tout de `gdim` et de `hd` (aucune constante de configuration) :
    #   hpg = gdim / hd (têtes par groupe) · n_groups = nh / hpg · o_lora = …
    dims_a = g.tenseurs[nom("attn_output_a.weight")][0]
    dims_b = g.tenseurs[nom("attn_output_b.weight")][0]
    gdim = dims_a[0]
    hpg = gdim // hd
    n_groups = nh // hpg
    o_lora = dims_b[0] // n_groups
    nrot = 64
    scale = 1.0 / np.sqrt(hd)
    q = dump(prefixe, "q_rope", couche, pos)
    kv = [dump(prefixe, "kv_rope", couche, t) for t in range(pos + 1)]
    puits = g.lire(nom("attn_sinks.weight")).ravel()
    print(f"couche {couche} pos {pos} : hd {hd} · {nh} têtes · {n_groups} groupes × "
          f"{o_lora} (gdim {gdim}) · puits {puits.shape}")
    sortie = np.zeros(nh * hd)
    for h in range(nh):
        qh = q[h * hd:(h + 1) * hd]
        sc = np.array([float(qh @ k) for k in kv]) * scale
        logits = np.concatenate([sc, [float(puits[h])]])
        e = np.exp(logits - logits.max())
        w = e / e.sum()
        acc = np.zeros(hd)
        for t in range(pos + 1):
            acc += w[t] * kv[t]
        sortie[h * hd:(h + 1) * hd] = acc
    ref = dump(prefixe, "attn_brut", couche, pos)
    print(f"  attn_brut (scores + puits + somme) : écart max {np.max(np.abs(sortie - ref)):.3e} "
          f"(dynamique {np.max(np.abs(ref)):.3e})")
    # dé-rotation : RoPE INVERSE sur les n_rot dernières de chaque tête
    op = np.concatenate([sortie[h * hd + hd - nrot:h * hd + hd] for h in range(nh)])
    op = rope_norm(op, nh, nrot, pos, BASE, nrot)          # NORM
    # l'inverse : même appariement, angle opposé
    op = np.concatenate([sortie[h * hd + hd - nrot:h * hd + hd] for h in range(nh)])
    op = op.reshape(nh, nrot)
    for h in range(nh):
        for i in range(nrot // 2):
            f = 1.0 / BASE ** (2.0 * i / nrot)
            s, c = np.sin(-pos * f), np.cos(-pos * f)
            a, b = op[h, 2 * i], op[h, 2 * i + 1]
            op[h, 2 * i] = a * c - b * s
            op[h, 2 * i + 1] = b * c + a * s
    sortie2 = sortie.copy()
    for h in range(nh):
        sortie2[h * hd + hd - nrot:h * hd + hd] = op[h]
    oa = np.zeros(n_groups * o_lora)
    for gg in range(n_groups):
        M = np.array([__import__("v41_attention_reference").dequant_q8_0_ligne(
            g, nom("attn_output_a.weight"), gg * o_lora + o)
            for o in range(o_lora)])
        oa[gg * o_lora:(gg + 1) * o_lora] = M @ sortie2[gg * gdim:(gg + 1) * gdim]
    Mb = np.array([__import__("v41_attention_reference").dequant_q8_0_ligne(
        g, nom("attn_output_b.weight"), o) for o in range(g.tenseurs[nom("attn_output_b.weight")][0][1])])
    calc = Mb @ oa
    ref2 = dump(prefixe, "attn_out", couche, pos)
    print(f"  attn_out (dé-rotation + wo_a + wo_b) : écart max {np.max(np.abs(calc - ref2)):.3e} "
          f"(dynamique {np.max(np.abs(ref2)):.3e}) · normes "
          f"{np.linalg.norm(calc):.4f} / {np.linalg.norm(ref2):.4f}")


if __name__ == "__main__":
    principale()

#!/usr/bin/env python3
"""Compare deux fichiers de logits au format :
   int32 n_vocab, int32 n_pos, puis n_pos lignes de n_vocab f32 (petit-boutiste).

Usage : compare_logits.py <notre.bin> <reference.bin> [ids.txt]

Rend : par position, la perte (NLL) de chacun, l'écart de NLL, le rang du jeton
cible dans chacun, et l'accord du top-1. C'est ce qui localise une divergence :
une erreur d'embedding ou de norme se voit dès la position 0 ; une erreur de
position (RoPE) fait croître l'écart avec la position ; une erreur de MoE ou de
tête fait décrocher toutes les positions d'un coup.
"""
import struct, sys, math

try:
    import numpy as np
except ImportError:
    np = None


def lire(chemin):
    with open(chemin, 'rb') as f:
        n_vocab, n_pos = struct.unpack('<ii', f.read(8))
        data = f.read(n_pos * n_vocab * 4)
    assert len(data) == n_pos * n_vocab * 4, f"{chemin} tronqué"
    if np is not None:
        a = np.frombuffer(data, dtype='<f4').reshape(n_pos, n_vocab)
    else:
        a = [list(struct.unpack(f'<{n_vocab}f', data[i*n_vocab*4:(i+1)*n_vocab*4]))
             for i in range(n_pos)]
    return n_vocab, n_pos, a


def nll_et_rang(ligne, cible):
    mx = max(ligne)
    se = sum(math.exp(v - mx) for v in ligne)
    lse = mx + math.log(se)
    nll = lse - ligne[cible]
    rang = 1 + sum(1 for v in ligne if v > ligne[cible])
    return nll, rang, max(range(len(ligne)), key=lambda i: ligne[i])


def main():
    notre_f, ref_f = sys.argv[1], sys.argv[2]
    ids = None
    if len(sys.argv) > 3:
        ids = [int(x) for x in open(sys.argv[3]).read().replace(',', ' ').split()]
    nv_a, np_a, A = lire(notre_f)
    nv_b, np_b, B = lire(ref_f)
    assert nv_a == nv_b, f"vocabulaires différents : {nv_a} contre {nv_b}"
    n = min(np_a, np_b)
    print(f"notre : {np_a} positions x {nv_a} · référence : {np_b} positions x {nv_b}")
    if np_a != np_b:
        print("ATTENTION : nombres de positions différents, comparaison sur le minimum")

    print(f"{'pos':>5} {'cible':>7} {'NLL nous':>9} {'NLL réf':>9} {'écart':>8} "
          f"{'rang nous':>9} {'rang réf':>9} {'top1 nous':>9} {'top1 réf':>9} {'accord':>7}")
    tot_a = tot_b = 0.0
    ecarts = []
    for i in range(n):
        cible = ids[i + 1] if ids and i + 1 < len(ids) else None
        if cible is None:
            break
        na, ra, t1a = nll_et_rang(A[i], cible)
        nb, rb, t1b = nll_et_rang(B[i], cible)
        tot_a += na; tot_b += nb
        ecarts.append(abs(na - nb))
        if i < 24 or i % 32 == 0:
            print(f"{i:5d} {cible:7d} {na:9.4f} {nb:9.4f} {na-nb:+8.4f} "
                  f"{ra:9d} {rb:9d} {t1a:9d} {t1b:9d} {'oui' if t1a == t1b else 'NON':>7}")
    if ecarts and np is not None:
        e = np.array(ecarts)
        print(f"\nécart |NLL| : moyenne {e.mean():.4f} · médiane {np.median(e):.4f} · max {e.max():.4f}")
    print(f"perplexité nous : {math.exp(tot_a/n):.4f}   référence : {math.exp(tot_b/n):.4f}   "
          f"({n} positions)")
    # corrélation ligne à ligne sur la première position
    if np is not None and n:
        a0 = np.asarray(A[0], dtype='f8'); b0 = np.asarray(B[0], dtype='f8')
        a0 -= a0.mean(); b0 -= b0.mean()
        c = float((a0 @ b0) / (np.linalg.norm(a0) * np.linalg.norm(b0) + 1e-12))
        print(f"corrélation des logits (position 0) : {c:.6f}")


if __name__ == '__main__':
    main()

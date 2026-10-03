#!/usr/bin/env python3
"""Témoin du test `yarn_du_compresseur_conforme_a_ggml` (Model::rope_norm_yarn).

Le test unitaire colle ces huit valeurs ; ce script les **recalcule depuis ggml**
(`ggml/src/ggml-cpu/ops.cpp:5959-5981` pour `rope_yarn_ramp`/`rope_yarn`,
`ggml/src/ggml.c:4467-4480` pour `ggml_rope_yarn_corr_dims`) — c'est la seconde
implémentation du même calcul, dans un autre langage.

Pourquoi il existe : le test citait ce fichier alors qu'il n'existait pas ; un
témoin qu'on ne peut pas recalculer ne prouve rien.

Usage :  python3 tools/rope_yarn_temoin.py
"""
import numpy as np

N_ROT, BASE, POS = 8, 160_000.0, 124
FACTEUR, BETA_RAPIDE, BETA_LENT, CTX_ORIGINE = 16.0, 32.0, 1.0, 65_536.0


def corr_dim(n_dims, n_ctx_orig, n_rot, base):
    return n_dims * np.log(n_ctx_orig / (n_rot * 2 * np.pi)) / (2 * np.log(base))


def corr_dims(n_dims, n_ctx_orig, base, beta_fast, beta_slow):
    return (max(0.0, np.floor(corr_dim(n_dims, n_ctx_orig, beta_fast, base))),
            min(n_dims - 1.0, np.ceil(corr_dim(n_dims, n_ctx_orig, beta_slow, base))))


def rope_yarn(x, pos):
    v = np.asarray(x, dtype=np.float64).copy()
    theta_scale = BASE ** (-2.0 / N_ROT)
    theta = float(pos)
    c0, c1 = corr_dims(N_ROT, CTX_ORIGINE, BASE, BETA_RAPIDE, BETA_LENT)
    for i0 in range(0, N_ROT, 2):
        theta_extrap = theta
        theta_interp = theta_extrap / FACTEUR
        # `rope_yarn_ramp(low, high, i0) = 1 - clamp((i0/2 - low)/(high - low))`
        rampe = 1.0 - min(1.0, max(0.0, (i0 / 2 - c0) / max(0.001, c1 - c0)))
        th = theta_interp * (1.0 - rampe) + theta_extrap * rampe
        c, s = np.cos(th), np.sin(th)
        a, b = v[i0], v[i0 + 1]
        v[i0], v[i0 + 1] = a * c - b * s, b * c + a * s
        theta *= theta_scale
    return v, (c0, c1)


if __name__ == "__main__":
    x = [0.5, -1.25, 2.0, 0.75, -0.5, 1.5, -2.0, 0.25]
    v, corr = rope_yarn(x, POS)
    print(f"// corr_dims = {corr} (bornées : max(0,·), min(n_dims−1,·))")
    print("let attendu = [" + ", ".join(f"{u:.9e}f32" for u in v) + "];")

#!/usr/bin/env python3
"""Référence **numpy** des hyper-connexions de DeepSeek-V4, et valeurs-témoins.

Les formules sont recopiées des opérations ggml de
`llama.cpp/src/models/deepseek4.cpp` (`build_hc_pre`, `build_hc_sinkhorn`,
`build_hc_post`, `build_hc_head`), **pas** de l'implémentation Rust : c'est ce
qui rend la comparaison utile. Les mêmes formules sont écrites deux fois, dans
deux langages — un écart se voit.

Ce que le script imprime est collé dans le test Rust
`model::tests_hc::hyper_connexions_conforme_a_la_reference` : petite dimension
(`hc = 4`, `h = 3`) et poids entiers, pour que le test se relise à la main.

Usage :  python3 tools/hc_synthetique.py
"""
import numpy as np

HC, H = 4, 3
EPS = 1e-6           # hyper_connection.epsilon (V4.1)
ITERS = 20           # hyper_connection.sinkhorn_iterations (V4.1)


def rms_norm_sans_poids(x, eps):
    """`ggml_rms_norm` SEUL : aucune échelle apprise, contrairement à nos rmsnorm."""
    return x / np.sqrt(np.mean(x * x) + eps)


def sinkhorn(brut, hc, iters, eps):
    """`brut` est PLAT, à la disposition de ggml : l'index RAPIDE est la
    destination (`comb[d + s*hc]`), parce que `comb` est une vue 2d de `mixes`
    (`ne0` = 16 valeurs contiguës) reshapée en `[hc, hc]` — et dans ggml `ne0`
    est la dimension rapide. Se tromper là-dessus donne une matrice transposée,
    donc une double stochasticité qui a l'air juste. Vérifié sur la référence :
    `build_hc_post` lit `comb->nb[0]*dst + comb->nb[1]*src`.

    Ordre exact : softmax sur les destinations, +eps, une passe « sources », puis
    (iters − 1) paires (destinations, sources)."""
    c = np.asarray(brut, dtype=np.float64).reshape(hc, hc)   # [src, dst], dst rapide
    m = c.max(axis=1, keepdims=True)                          # par source
    e = np.exp(c - m)
    c = e / e.sum(axis=1, keepdims=True)
    c = c + eps
    c = c / (c.sum(axis=0, keepdims=True) + eps)              # sources, par destination
    for _ in range(1, iters):
        c = c / (c.sum(axis=1, keepdims=True) + eps)          # destinations, par source
        c = c / (c.sum(axis=0, keepdims=True) + eps)          # sources, par destination
    return c.reshape(-1)                                       # plat, d + s*hc


def hc_sortie(x, melange, base, scale, hc, eps, iters):
    """Rend (pre, post, comb) — l'équivalent de `build_hc_pre`."""
    flat = rms_norm_sans_poids(x.reshape(-1), 1e-20)
    mixes = melange @ flat                                # [2*hc + hc*hc]
    sig = lambda v: 1.0 / (1.0 + np.exp(-v))
    pre = sig(mixes[:hc] * scale[0] + base[:hc]) + eps
    post = 2.0 * sig(mixes[hc:2 * hc] * scale[1] + base[hc:2 * hc])
    brut = mixes[2 * hc:] * scale[2] + base[2 * hc:]
    comb = sinkhorn(brut, hc, iters, eps)                 # plat : comb[d + s*hc]
    return pre, post, comb


def main():
    rng = np.random.default_rng(20261002)
    # Poids entiers petits : le test Rust se relit sans calculatrice.
    melange = rng.integers(-2, 3, size=(2 * HC + HC * HC, HC * H)).astype(np.float64)
    base = rng.integers(-1, 2, size=2 * HC + HC * HC).astype(np.float64)
    scale = np.array([0.5, 1.5, 2.0])
    x = rng.integers(-2, 3, size=(HC, H)).astype(np.float64)
    y = rng.integers(-2, 3, size=H).astype(np.float64)

    pre, post, comb = hc_sortie(x, melange, base, scale, HC, EPS, ITERS)
    entree = sum(x[ih] * pre[ih] for ih in range(HC))
    sortie = np.stack([y * post[d] + sum(x[s] * comb[d + s * HC] for s in range(HC))
                       for d in range(HC)])

    def c(v, n=9):
        return ", ".join(f"{float(u):.{n}e}" for u in np.asarray(v).reshape(-1))

    print(f"// généré par tools/hc_synthetique.py — ne pas éditer à la main")
    print(f"const MELANGE: [f32; {melange.size}] = [{c(melange)}];")
    print(f"const BASE: [f32; {base.size}] = [{c(base)}];")
    print(f"const SCALE: [f32; 3] = [{c(scale)}];")
    print(f"const X: [f32; {x.size}] = [{c(x)}];")
    print(f"const Y: [f32; {y.size}] = [{c(y)}];")
    print(f"const PRE: [f32; {HC}] = [{c(pre)}];")
    print(f"const POST: [f32; {HC}] = [{c(post)}];")
    print(f"const COMB: [f32; {HC * HC}] = [{c(comb)}];")
    print(f"const ENTREE: [f32; {H}] = [{c(entree)}];")
    print(f"const SORTIE: [f32; {HC * H}] = [{c(sortie)}];")
    # Invariants lisibles : la matrice de connexions est doublement stochastique
    # à eps près (c'est ce que Sinkhorn garantit, et c'est vérifiable à la main).
    M = comb.reshape(HC, HC)   # [src, dst] : la destination est l'index rapide
    print(f"// sommes par destination (doivent valoir 1 à eps près) : {c(M.sum(axis=0))}")
    print(f"// sommes par source      : {c(M.sum(axis=1))} (dérivent de eps)")


if __name__ == "__main__":
    main()

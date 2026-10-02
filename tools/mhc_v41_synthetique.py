#!/usr/bin/env python3
"""Référence **numpy** de la chaîne mHC *retardée* de DeepSeek-V4.1.

Pourquoi un second script : `hc_synthetique.py` recopie `llama.cpp`
(`deepseek4.cpp`), c'est-à-dire **V4**, où chaque raccord se replie avec ses
PROPRES coefficients. V4.1 ne fait pas ça — c'est une autre chaîne, et la
confondre avec la première donne des nombres plausibles et faux.

Les formules ci-dessous sont recopiées de la référence d'exécution de V4.1 :

  * `vllm/model_executor/kernels/mhc/torch.py` → `mhc_pre_delayed_torch`
    (« Reference for mHC pre using coefficients from the previous sublayer ») :
    les mélanges sont calculés sur le flux, la `pre` **calculée** ressort, et le
    repliement se fait avec la `pre` **reçue** ;
  * `vllm/models/deepseek_v41/nvidia/model.py` → `mhc_shifted_post_pre` (le
    `post` d'abord, puis la `pre` retardée), le commentaire « The reference
    collapses each sublayer's input with the *previous* sublayer's pre-mix :
    attention uses the pre-mix carried in (identity for the first layer), the
    FFN uses this layer's attention pre-mix », et la fin de modèle
    `hc_collapse_triton(hidden_states, pre_mix)` + `self.norm`
    (« v4.1 has no learned hc_head »).

**Pas** de l'implémentation Rust : c'est ce qui rend la comparaison utile.

Ce que le script imprime est collé dans le test Rust
`model::tests_hc::chaine_retardee_v41` : dimensions minuscules (`hc = 4`,
`h = 2`) et poids entiers, pour que le test se relise à la main.

Usage :  python3 tools/mhc_v41_synthetique.py
"""
import numpy as np

HC, H = 4, 2
RMS_EPS = 1e-20      # config `rms_norm_eps` de V4.1 (et non `hc_eps` !)
HC_EPS = 1e-6        # config `hc_eps` : pré-mix ET Sinkhorn
ITERS = 20


def rms_norm_sans_poids(x, eps=RMS_EPS):
    return x / np.sqrt(np.mean(x * x) + eps)


def sinkhorn(brut, hc, iters, eps):
    """`comb` : softmax sur les destinations (l'index RAPIDE, celui de ggml),
    puis normalisations alternées — sources d'abord, puis `iters − 1` paires."""
    c = np.asarray(brut, dtype=np.float64).reshape(hc, hc)      # [src, dst]
    m = c.max(axis=1, keepdims=True)
    e = np.exp(c - m)
    c = e / e.sum(axis=1, keepdims=True)
    c = c + eps
    c = c / (c.sum(axis=0, keepdims=True) + eps)
    for _ in range(1, iters):
        c = c / (c.sum(axis=1, keepdims=True) + eps)
        c = c / (c.sum(axis=0, keepdims=True) + eps)
    return c.reshape(-1)                                        # plat : d + s*hc


def hc_pre_retardee(residual, melange, base, scale, pre_mix):
    """`mhc_pre_delayed_torch` : rend `(pre, post, comb, entree)`.

    `pre_mix = None` → la copie 0 est l'entrée (`residual[:, 0]`), ce que la
    référence fait au tout premier raccord du modèle.
    """
    plat = residual.reshape(-1)
    mixes = np.asarray(melange, dtype=np.float64) @ rms_norm_sans_poids(plat)
    sig = lambda v: 1.0 / (1.0 + np.exp(-v))
    pre = sig(mixes[:HC] * scale[0] + base[:HC]) + HC_EPS
    post = 2.0 * sig(mixes[HC:2 * HC] * scale[1] + base[HC:2 * HC])
    brut = mixes[2 * HC:] * scale[2] + base[2 * HC:]
    comb = sinkhorn(brut, HC, ITERS, HC_EPS)
    entree = (residual[0].copy() if pre_mix is None
              else (pre_mix.reshape(HC, 1) * residual).sum(axis=0))
    return pre, post, comb, entree


def hc_post(y, residu, post, comb):
    return np.stack([y * post[d] + sum(residu[s] * comb[d + s * HC] for s in range(HC))
                     for d in range(HC)])


def main():
    rng = np.random.default_rng(20261002)
    # Poids entiers petits : le test Rust se relit sans calculatrice.
    def poids(n):
        return rng.integers(-2, 3, size=n).astype(np.float64)
    MIX = 2 * HC + HC * HC
    mel_a = poids((MIX, HC * H))
    mel_f = poids((MIX, HC * H))
    base_a, base_f = poids(MIX), poids(MIX)
    scale_a, scale_f = np.array([0.5, 1.5, 2.0]), np.array([1.0, 0.5, 2.0])
    v = poids(H)                      # l'état initial, en HC copies IDENTIQUES
    # Les sorties des sous-couches DÉPENDENT de l'entrée repliée : sans cela les
    # deux chaînes donneraient le même résultat et le test ne prouverait rien
    # (c'est exactement l'erreur qu'a faite la première version de ce script).
    w_a, w_f = poids((H, H)), poids((H, H))
    norme_sortie = np.array([1.0, 2.0])

    # ---- chaîne RETARDÉE (V4.1)
    x0 = np.tile(v, (HC, 1))
    pre_a, post_a, comb_a, entree_a = hc_pre_retardee(x0, mel_a, base_a, scale_a, None)
    y_a = w_a @ entree_a
    x1 = hc_post(y_a, x0, post_a, comb_a)
    pre_f, post_f, comb_f, entree_f = hc_pre_retardee(x1, mel_f, base_f, scale_f, pre_a)
    y_f = w_f @ entree_f
    x2 = hc_post(y_f, x1, post_f, comb_f)
    replie = (pre_f.reshape(HC, 1) * x2).sum(axis=0)          # la tête
    tete = rms_norm_sans_poids(replie) * norme_sortie

    # ---- même graphe, coefficients NON retardés (V4) : sert à montrer que le
    #      retard est OBSERVABLE, donc que ce n'est pas un détail d'écriture.
    pre_a2, post_a2, comb_a2, _ = hc_pre_retardee(x0, mel_a, base_a, scale_a, None)
    entree_a2 = (pre_a2.reshape(HC, 1) * x0).sum(axis=0)
    x1b = hc_post(w_a @ entree_a2, x0, post_a2, comb_a2)
    pre_f2, post_f2, comb_f2, _ = hc_pre_retardee(x1b, mel_f, base_f, scale_f, None)
    entree_f2 = (pre_f2.reshape(HC, 1) * x1b).sum(axis=0)
    x2b = hc_post(w_f @ entree_f2, x1b, post_f2, comb_f2)
    tete_b = rms_norm_sans_poids((pre_f2.reshape(HC, 1) * x2b).sum(axis=0)) * norme_sortie

    def c(w, n=9):
        return ", ".join(f"{float(u):.{n}e}" for u in np.asarray(w).reshape(-1))

    print("// généré par tools/mhc_v41_synthetique.py — ne pas éditer à la main")
    print("// V4.1 : la `pre` d'un raccord sert au raccord SUIVANT, et la tête se")
    print("// replie avec la `pre` de la dernière FFN (pas de `output_hc_*`).")
    print(f"const MEL_A: [f32; {mel_a.size}] = [{c(mel_a)}];")
    print(f"const BASE_A: [f32; {base_a.size}] = [{c(base_a)}];")
    print(f"const SCALE_A: [f32; 3] = [{c(scale_a)}];")
    print(f"const MEL_F: [f32; {mel_f.size}] = [{c(mel_f)}];")
    print(f"const BASE_F: [f32; {base_f.size}] = [{c(base_f)}];")
    print(f"const SCALE_F: [f32; 3] = [{c(scale_f)}];")
    print(f"const V0: [f32; {H}] = [{c(v)}];")
    print(f"const W_A: [f32; {H * H}] = [{c(w_a)}];")
    print(f"const W_F: [f32; {H * H}] = [{c(w_f)}];")
    print(f"const NORME_SORTIE: [f32; {H}] = [{c(norme_sortie)}];")
    print(f"const PRE_A: [f32; {HC}] = [{c(pre_a)}];")
    print(f"const PRE_F: [f32; {HC}] = [{c(pre_f)}];")
    print(f"const ENTREE_A: [f32; {H}] = [{c(entree_a)}];")
    print(f"const ENTREE_F: [f32; {H}] = [{c(entree_f)}];")
    print(f"const X2: [f32; {HC * H}] = [{c(x2)}];")
    print(f"const TETE: [f32; {H}] = [{c(tete)}];")
    # Le contrôle qui donne son sens au reste : les deux chaînes DIFFÈRENT.
    ecart = np.max(np.abs(tete - tete_b)) / max(np.max(np.abs(tete_b)), 1e-30)
    print(f"// écart relatif tête retardée / tête directe : {ecart:.4f}"
          "  (le retard n'est pas cosmétique)")
    print(f"// entrée du premier raccord (copie 0, NON mélangée) : {c(entree_a)}")


if __name__ == "__main__":
    main()

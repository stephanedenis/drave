#!/usr/bin/env python3
"""kv_attention.py — A7.11 : le KV int8 change-t-il l'attention ?

A7.10 mesurait la reconstruction du cache. Ici on va jusqu'à la **sortie
d'attention** : Q aléatoire, K/V du cache, softmax, sortie f32 vs KV int8.
Ce n'est pas un modèle : c'est la sensibilité de l'attention à la quantization.
"""
from __future__ import annotations

import json

import numpy as np

from tools.kv_int8 import decoder, encoder
from tools.kv_reseau import _kv


def _attention(q: np.ndarray, k: np.ndarray, v: np.ndarray) -> np.ndarray:
    # q : (ntok, h, d), k/v : (ntok, h, d) -> (ntok, h, d)
    scores = np.einsum("thd,shd->hts", q, k) / np.sqrt(q.shape[-1])
    scores = scores - scores.max(axis=-1, keepdims=True)
    p = np.exp(scores)
    p /= p.sum(axis=-1, keepdims=True)
    return np.einsum("hts,shd->thd", p, v)


def mesurer(ntok: int = 64, graine: int = 0) -> dict:
    rng = np.random.default_rng(graine)
    q = rng.standard_normal((ntok, 2, 64)).astype(np.float32)
    kv = _kv(ntok)
    k = kv[0]  # (ntok, 2, 64)
    v = kv[1]
    out_f32 = _attention(q, k, v)
    kv_q = decoder(encoder(kv))
    k_q = kv_q[0]
    v_q = kv_q[1]
    out_q = _attention(q, k_q, v_q)
    diff = np.abs(out_f32 - out_q)
    return {
        "ntok": ntok, "d": 64, "h": 2,
        "diff_max": float(diff.max()),
        "diff_moyenne": float(diff.mean()),
        "argmax_accord": float((out_f32.argmax(-1) == out_q.argmax(-1)).mean()),
        "correlation": float(np.corrcoef(out_f32.ravel(), out_q.ravel())[0, 1]),
        "octets_f32": int(kv.size * 4 + 12),
        "octets_int8": int(len(encoder(kv))),
        "ratio": len(encoder(kv)) / (kv.size * 4 + 12),
    }


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

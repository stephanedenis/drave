"""
Qtrinet — forward pass Qwen2 en numpy pur (aucune dépendance ML).

Sert de **modèle d'or** pour l'architecture événementielle : il donne les
activations réelles, donc le nombre d'événements par couche et par token — et
c'est cette distribution qui détermine le débit variable de la cascade.

Architecture Qwen2 : RMSNorm, RoPE (freq_base 1e6), GQA, biais QKV, SwiGLU,
embeddings liés (pas de tenseur de sortie séparé).
"""

from __future__ import annotations

import numpy as np


def rms_norm(x: np.ndarray, w: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    return (x / np.sqrt((x * x).mean(-1, keepdims=True) + eps)) * w


def silu(x: np.ndarray) -> np.ndarray:
    return x / (1.0 + np.exp(-x))


def rope(x: np.ndarray, positions: np.ndarray, base: float = 1e6) -> np.ndarray:
    """RoPE appliqué à (T, n_head, head_dim), par paires."""
    T, H, D = x.shape
    half = D // 2
    inv = 1.0 / (base ** (np.arange(0, half, dtype=np.float32) / half))
    ang = positions[:, None].astype(np.float32) * inv[None, :]      # (T, half)
    cos, sin = np.cos(ang)[:, None, :], np.sin(ang)[:, None, :]     # (T,1,half)
    x1, x2 = x[..., :half], x[..., half:]
    return np.concatenate([x1 * cos - x2 * sin, x1 * sin + x2 * cos], axis=-1)


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - x.max(axis=axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)


class Qwen2:
    """Poids chargés depuis un GGUF, en float32."""

    def __init__(self, g, verbose: bool = False):
        self.g = g
        a = g.arch()
        self.n_layer = int(g.cfg("block_count"))
        self.n_head = int(g.cfg("attention.head_count"))
        self.n_kv = int(g.cfg("attention.head_count_kv"))
        self.hidden = int(g.cfg("embedding_length"))
        self.inter = int(g.cfg("feed_forward_length"))
        self.eps = float(g.cfg("attention.layer_norm_rms_epsilon", 1e-6))
        self.rope_base = float(g.cfg("rope.freq_base", 1e4))
        self.head_dim = self.hidden // self.n_head
        self.kv_dim = self.n_kv * self.head_dim
        self.n_rep = self.n_head // self.n_kv

        self.embd = g.dequant("token_embd.weight")          # (vocab, hidden)
        self.out_norm = g.dequant("output_norm.weight")
        self.layers = []
        for L in range(self.n_layer):
            d = {"attn_norm": g.dequant(f"blk.{L}.attn_norm.weight"),
                 "ffn_norm": g.dequant(f"blk.{L}.ffn_norm.weight"),
                 "Wq": g.dequant(f"blk.{L}.attn_q.weight"),
                 "bq": g.dequant(f"blk.{L}.attn_q.bias"),
                 "Wk": g.dequant(f"blk.{L}.attn_k.weight"),
                 "bk": g.dequant(f"blk.{L}.attn_k.bias"),
                 "Wv": g.dequant(f"blk.{L}.attn_v.weight"),
                 "bv": g.dequant(f"blk.{L}.attn_v.bias"),
                 "Wo": g.dequant(f"blk.{L}.attn_output.weight"),
                 "Wg": g.dequant(f"blk.{L}.ffn_gate.weight"),
                 "Wu": g.dequant(f"blk.{L}.ffn_up.weight"),
                 "Wd": g.dequant(f"blk.{L}.ffn_down.weight")}
            self.layers.append(d)
            if verbose and L == 0:
                print(f"  couche {L} chargée, Wq {d['Wq'].shape}")

    # ------------------------------------------------------------------ forward
    def forward(self, ids: np.ndarray, collect: dict | None = None) -> np.ndarray:
        """Retourne les logits (T, vocab). `collect` reçoit les activations clés."""
        T = len(ids)
        pos = np.arange(T)
        h = self.embd[ids].astype(np.float32)

        for L, d in enumerate(self.layers):
            # ---- attention ----
            xn = rms_norm(h, d["attn_norm"], self.eps)
            if collect is not None:
                collect.setdefault("ffn_in", []).append(xn)
            q = (xn @ d["Wq"].T + d["bq"]).reshape(T, self.n_head, self.head_dim)
            k = (xn @ d["Wk"].T + d["bk"]).reshape(T, self.n_kv, self.head_dim)
            v = (xn @ d["Wv"].T + d["bv"]).reshape(T, self.n_kv, self.head_dim)
            q, k = rope(q, pos, self.rope_base), rope(k, pos, self.rope_base)

            k = np.repeat(k, self.n_rep, axis=1)       # GQA : 1 KV pour n_rep Q
            v = np.repeat(v, self.n_rep, axis=1)
            sc = np.einsum("thd,shd->hts", q, k) / np.sqrt(self.head_dim)
            mask = np.triu(np.full((T, T), -np.inf, dtype=np.float32), 1)
            p = softmax(sc + mask[None], axis=-1)      # (H, T, T)
            if collect is not None:
                collect.setdefault("attn_probs", []).append(p)
            o = np.einsum("hts,shd->thd", p, v).reshape(T, self.hidden)
            h = h + o @ d["Wo"].T

            # ---- MLP (SwiGLU) ----
            xn2 = rms_norm(h, d["ffn_norm"], self.eps)
            if collect is not None:
                collect.setdefault("mlp_in", []).append(xn2)
            g_ = silu(xn2 @ d["Wg"].T)
            if collect is not None:
                collect.setdefault("mlp_gate", []).append(g_)
            h = h + (g_ * (xn2 @ d["Wu"].T)) @ d["Wd"].T

        if collect is not None:
            collect["final_hidden"] = h
        return rms_norm(h, self.out_norm, self.eps) @ self.embd.T

    # ---------------------------------------------------------------- perplexité
    def perplexity(self, ids: np.ndarray, block: int = 512) -> float:
        """Perplexité en fenêtres glissantes non recouvrantes."""
        nll, ntok = 0.0, 0
        for s in range(0, len(ids) - 1, block):
            chunk = ids[s:s + block]
            if len(chunk) < 2:
                break
            logits = self.forward(chunk)
            lp = logits[:-1] - np.log(np.exp(logits[:-1]).sum(-1, keepdims=True))
            tgt = chunk[1:]
            nll += float(-lp[np.arange(len(tgt)), tgt].sum())
            ntok += len(tgt)
        return float(np.exp(nll / max(ntok, 1)))

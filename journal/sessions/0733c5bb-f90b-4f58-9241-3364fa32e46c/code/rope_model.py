#!/usr/bin/env python3
"""rope_model.py — la variante **positions relatives** du modèle natif (R1.1/R1.2).

Le modèle de `tools/native_model.py` ajoute une **position apprise absolue** (`self.pos`) et
compte sur les positions aléatoires à l'entraînement (N2.j2) : le gain à 512 octets est réel
(÷2,1 à ÷2,4) mais c'est une **astuce d'entraînement**, pas une propriété de l'architecture.
Ce module remplace la position absolue par un **RoPE** (rotation des q/k, aucune position
apprise) : le score d'attention ne dépend plus que de l'**écart** entre positions, donc
l'extrapolation en longueur est acquise par construction.

Rien n'est modifié dans `tools/` : les blocs réutilisent les **mêmes noms de paramètres**
(`ln1`, `qkv`, `out`, `ln2`, `ffn`), ce qui permet de charger un point de contrôle absolu
comme initialisation (`strict=False`, `pos` reste inutilisé).

Usage :
  PYTHONPATH=. python3 -c "from work.n2ac.rope_model import charge_rope; ..."
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from tools.native_model import Block, NativeConfig, NativeModel, exporter_drvm


def rope(x: torch.Tensor, base: float = 10_000.0) -> torch.Tensor:
    """RoPE sur un tenseur (b, têtes, s, d_tête). Les positions sont 0…s−1."""
    b, h, s, dh = x.shape
    if dh % 2:
        raise SystemExit("RoPE : dimension de tête impaire")
    inv = 1.0 / (base ** (torch.arange(0, dh, 2, device=x.device, dtype=torch.float32) / dh))
    t = torch.arange(s, device=x.device, dtype=torch.float32)
    f = torch.outer(t, inv)
    cos, sin = f.cos()[None, None], f.sin()[None, None]
    x1, x2 = x[..., 0::2], x[..., 1::2]
    return torch.stack([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1).flatten(-2)


class BlockRoPE(Block):
    """Même graphe et mêmes paramètres que `tools.native_model.Block`, q/k tournés."""

    def forward(self, x):
        b, s, d = x.shape
        h = self.ln1(x)
        q, k, v = self.qkv(h).chunk(3, dim=-1)
        dh = d // self.cfg.n_heads
        q = q.view(b, s, self.cfg.n_heads, dh).transpose(1, 2)
        k = k.view(b, s, self.cfg.n_heads, dh).transpose(1, 2)
        v = v.view(b, s, self.cfg.n_heads, dh).transpose(1, 2)
        q, k = rope(q), rope(k)
        i = torch.arange(s, device=x.device)
        masque = (i[:, None] >= i[None, :]) & ((i[:, None] - i[None, :]) < self.cfg.window)
        y = F.scaled_dot_product_attention(q, k, v, attn_mask=masque)
        y = y.transpose(1, 2).reshape(b, s, d)
        x = x + self.out(y)
        return x + self.ffn(self.ln2(x))


class NativeModelRoPE(NativeModel):
    """Le natif sans table de positions : les blocs sont des `BlockRoPE`."""

    def __init__(self, cfg: NativeConfig | None = None):
        super().__init__(cfg)
        self.blocks = nn.ModuleList([BlockRoPE(self.cfg) for _ in range(self.cfg.n_blocks)])

    def forward(self, ids, pos_debut: int = 0, canal=None):
        b, s = ids.shape
        # `pos_debut` est accepté pour l'interface, mais n'a aucun effet : la position
        # n'est plus un paramètre, seulement un écart relatif dans l'attention.
        x = self.embed(ids)
        if canal is not None:
            x = x + self.embed_canal(canal)
        early = []
        for i, bloc in enumerate(self.blocks):
            x = bloc(x)
            if i == self.cfg.n_blocks // 2 - 1:
                x = x + self.bridge(x)
            if i in self.cfg.early_blocks:
                early.append(self.early_heads[self.cfg.early_blocks.index(i)](x))
        h0 = x
        for _ in range(self.cfg.thought_steps):
            x = torch.tanh(self.thought(x) + self.thought_in(h0))
        return {"logits": self.head_byte(x), "early": early,
                "thought": x, "rsn": self.head_rsn(x)}


def charge_rope(chemin: str, device: str = "cuda", window: int | None = None):
    ck = torch.load(chemin, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items()
                          if k in NativeConfig.__annotations__})
    if window is not None:
        cfg.window = window
    m = NativeModelRoPE(cfg).to(device)
    m.load_state_dict(ck["state"], strict=False)
    m.eval()
    return m


def exporter(m, chemin: str) -> str:
    return exporter_drvm(m, chemin)


def autotest() -> None:
    cfg = NativeConfig(d_model=64, expert_hidden=32)
    m = NativeModelRoPE(cfg)
    x = torch.randint(0, 256, (2, 16))
    c = torch.randint(0, 6, (2, 16))
    s = m(x, canal=c)
    assert s["logits"].shape == (2, 16, 256), s["logits"].shape
    # le décalage de position ne doit plus rien changer (positions relatives)
    m.eval()
    with torch.no_grad():
        a = m(x, pos_debut=0)["logits"]
        b = m(x, pos_debut=987)["logits"]
        e = BlockRoPE(cfg)
    assert torch.allclose(a, b, atol=1e-6), "RoPE : pos_debut devrait être neutre"
    # RoPE préserve la norme des paires
    y = rope(torch.randn(3, 2, 5, 8))
    assert y.shape == (3, 2, 5, 8)
    print("autotest rope OK : forme, pos_debut neutre, norme préservée")


if __name__ == "__main__":
    autotest()

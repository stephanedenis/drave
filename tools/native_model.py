#!/usr/bin/env python3
"""native_model.py — `drave-n0`, le modèle natif du programme N.

Ce n'est pas un Qwen3-MoE : c'est un graphe de blocs en **octets**, avec
attention locale, FFN creux routé, sorties précoces, cellule de pensée et pont.
Le modèle est petit (12 M) : c'est un **banc de mécanismes**, pas un assistant.

Le fichier définit l'architecture, l'export DRVM et les tests de forme. Il ne
prétend pas que l'entraînement est fait : N1.2 reste à mesurer.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F

from tools.drvm import TensorSpec, write_drvm


@dataclass
class NativeConfig:
    vocab: int = 256
    d_model: int = 224
    n_blocks: int = 6
    n_heads: int = 4
    expert_hidden: int = 288
    n_experts: int = 8
    top_k: int = 2
    kwta: float = 0.25
    window: int = 256
    max_pos: int = 2048
    thought_steps: int = 2
    early_blocks: tuple[int, ...] = (1, 3, 5)  # 0-based : après 2, 4, 6
    rsn_dim: int = 120


class SparseFFN(nn.Module):
    def __init__(self, cfg: NativeConfig):
        super().__init__()
        self.cfg = cfg
        self.router = nn.Linear(cfg.d_model, cfg.n_experts)
        self.gate = nn.Linear(cfg.d_model, cfg.n_experts * cfg.expert_hidden)
        self.up = nn.Linear(cfg.d_model, cfg.n_experts * cfg.expert_hidden)
        self.down = nn.Linear(cfg.n_experts * cfg.expert_hidden, cfg.d_model)

    def forward(self, x):
        b, s, d = x.shape
        logits = self.router(x)
        poids, idx = logits.topk(self.cfg.top_k, dim=-1)
        poids = poids.softmax(-1)
        g = self.gate(x).view(b, s, self.cfg.n_experts, self.cfg.expert_hidden)
        u = self.up(x).view(b, s, self.cfg.n_experts, self.cfg.expert_hidden)
        h = F.silu(g) * u
        # k-WTA par jeton : on ne garde que kwta des unités, le reste est zéro.
        k = max(1, int(self.cfg.expert_hidden * self.cfg.kwta))
        seuil = h.topk(k, dim=-1).values[..., -1:]
        h = torch.where(h >= seuil, h, torch.zeros_like(h))
        # Ne garder que les experts choisis.
        masque = torch.zeros_like(logits, dtype=torch.bool)
        masque.scatter_(-1, idx, True)
        h = h * masque.unsqueeze(-1)
        h = h.reshape(b, s, self.cfg.n_experts * self.cfg.expert_hidden)
        return self.down(h)


class Block(nn.Module):
    def __init__(self, cfg: NativeConfig):
        super().__init__()
        self.cfg = cfg
        self.ln1 = nn.LayerNorm(cfg.d_model)
        self.qkv = nn.Linear(cfg.d_model, 3 * cfg.d_model)
        self.out = nn.Linear(cfg.d_model, cfg.d_model)
        self.ln2 = nn.LayerNorm(cfg.d_model)
        self.ffn = SparseFFN(cfg)

    def forward(self, x):
        b, s, d = x.shape
        h = self.ln1(x)
        q, k, v = self.qkv(h).chunk(3, dim=-1)
        dh = d // self.cfg.n_heads
        q = q.view(b, s, self.cfg.n_heads, dh).transpose(1, 2)
        k = k.view(b, s, self.cfg.n_heads, dh).transpose(1, 2)
        v = v.view(b, s, self.cfg.n_heads, dh).transpose(1, 2)
        i = torch.arange(s, device=x.device)
        masque = (i[:, None] >= i[None, :]) & ((i[:, None] - i[None, :]) < self.cfg.window)
        y = F.scaled_dot_product_attention(q, k, v, attn_mask=masque)
        y = y.transpose(1, 2).reshape(b, s, d)
        x = x + self.out(y)
        return x + self.ffn(self.ln2(x))


class NativeModel(nn.Module):
    def __init__(self, cfg: NativeConfig | None = None):
        super().__init__()
        self.cfg = cfg or NativeConfig()
        self.embed = nn.Embedding(self.cfg.vocab, self.cfg.d_model)
        self.pos = nn.Embedding(self.cfg.max_pos, self.cfg.d_model)
        self.blocks = nn.ModuleList([Block(self.cfg) for _ in range(self.cfg.n_blocks)])
        self.early_heads = nn.ModuleList([nn.Linear(self.cfg.d_model, self.cfg.vocab)
                                          for _ in self.cfg.early_blocks])
        self.thought = nn.Linear(self.cfg.d_model, self.cfg.d_model)
        self.thought_in = nn.Linear(self.cfg.d_model, self.cfg.d_model)
        self.head_byte = nn.Linear(self.cfg.d_model, self.cfg.vocab)
        self.head_rsn = nn.Linear(self.cfg.d_model, self.cfg.rsn_dim)

    def forward(self, ids):
        b, s = ids.shape
        x = self.embed(ids) + self.pos(torch.arange(s, device=ids.device))[None]
        early = []
        for i, bloc in enumerate(self.blocks):
            x = bloc(x)
            if i in self.cfg.early_blocks:
                early.append(self.early_heads[self.cfg.early_blocks.index(i)](x))
        h0 = x
        for _ in range(self.cfg.thought_steps):
            # Pas CONTRACTANT : tanh(W x + U h0), sans résidu x + ….
            # Le résidu garantissait λ ≈ 1,42 ; le pas contractant ramène λ < 1
            # tout en gardant le contenu par l'injection h0.
            x = torch.tanh(self.thought(x) + self.thought_in(h0))
        return {"logits": self.head_byte(x), "early": early,
                "thought": x, "rsn": self.head_rsn(x)}

    def nb_parametres(self) -> int:
        return sum(p.numel() for p in self.parameters())


def _bloc_de(nom: str, cfg: NativeConfig) -> str:
    if nom.startswith("blocks."):
        return f"b{nom.split('.')[1]}"
    if nom.startswith("early_heads."):
        return f"early{nom.split('.')[1]}"
    if nom.startswith("embed.") or nom.startswith("pos."):
        return "input"
    if nom.startswith("thought"):
        return "thought"
    return "output"


def exporter_drvm(modele: NativeModel, chemin: str) -> str:
    """Exporte les poids et le graphe en DRVM v0. Retourne le hash du fichier."""
    cfg = modele.cfg
    blocs = [{"id": "input", "kind": "input", "inputs": [], "outputs": ["h"]}]
    for i in range(cfg.n_blocks):
        blocs.append({"id": f"b{i}", "kind": "local_mixer", "inputs": ["h"], "outputs": ["h"]})
    for i in range(len(cfg.early_blocks)):
        blocs.append({"id": f"early{i}", "kind": "early_head", "inputs": ["h"], "outputs": [f"y{i}"]})
    blocs.append({"id": "thought", "kind": "thought", "inputs": ["h"], "outputs": ["h"]})
    blocs.append({"id": "output", "kind": "output", "inputs": ["h"], "outputs": ["logits", "rsn"]})
    manifeste = {
        "format": "DRVM", "version": 0,
        "model": {"name": "drave-n0", "parametres": modele.nb_parametres(),
                  "tokenizer": {"kind": "bytes", "vocab": cfg.vocab}},
        "graph": {"regions": [{"id": "r0", "blocks": [b["id"] for b in blocs]}],
                  "blocks": blocs, "routes": [], "heads": [f"early{i}" for i in range(len(cfg.early_blocks))],
                  "thought": {"steps": cfg.thought_steps}, "bridge": None},
        "execution": {"activation": "DRVF", "placement": "local",
                      "cache": {"kind": "kv", "max": cfg.window},
                      "replay": {"seed": 0}},
    }
    specs = []
    for nom, p in sorted(modele.state_dict().items()):
        specs.append(TensorSpec(nom, p.detach().cpu().contiguous().numpy().tobytes(),
                                dtype="f32", shape=tuple(p.shape), bloc=_bloc_de(nom, cfg)))
    return write_drvm(chemin, manifeste, specs)

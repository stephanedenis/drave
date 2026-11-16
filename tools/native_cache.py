#!/usr/bin/env python3
"""native_cache.py — la génération avec cache KV (le levier ×14-28 sur CPU).

POURQUOI. `generer_natif` recalcule les 1 024 positions à **chaque** octet : 28 ms
par octet sur CPU. Le cache KV ne calcule que le **nouveau** jeton : la passe
devient O(1) par jeton (le K/V des positions passées est réutilisé).

CONTRAT. `passe(modele, ids, cache)` : si `cache` est None, la passe est complète
(le préfill) et le cache est rempli ; sinon `ids` doit être **un** jeton et la
passe ne calcule que lui. Les logits rendus sont identiques au modèle complet
(le test de parité le vérifie).

Usage :
  python3 tools/native_cache.py --modele work/n2ac/mix1024-60k.pt \
      --prompt "La France est un pays" --n 16
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
import time

import torch
import torch.nn.functional as F

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from tools.generer_natif import charger  # noqa: E402
from tools.native_model import NativeConfig, NativeModel  # noqa: E402


def _bloc_avec_cache(bloc, x, cache, i):
    """Le forward d'un bloc avec le K/V des positions passées (le cache)."""
    b, s, d = x.shape
    cfg = bloc.cfg
    h = bloc.ln1(x)
    qkv = bloc.qkv(h)
    q, k, v = qkv.chunk(3, dim=-1)
    dh = d // cfg.n_heads
    q = q.view(b, s, cfg.n_heads, dh).transpose(1, 2)
    k = k.view(b, s, cfg.n_heads, dh).transpose(1, 2)
    v = v.view(b, s, cfg.n_heads, dh).transpose(1, 2)
    if cache is not None and cache[i] is not None:
        k = torch.cat([cache[i][0], k], dim=2)
        v = torch.cat([cache[i][1], v], dim=2)
    if cache is not None:
        cache[i] = (k, v)
    pos_q = torch.arange(q.shape[2], device=x.device)[-s:] if cache is not None else torch.arange(s, device=x.device)
    # l'attention : le masque causal reste vrai (le cache ne contient que le passé)
    n_k = k.shape[2]
    i_q = torch.arange(n_k - s, n_k, device=x.device) if s < n_k else torch.arange(s, device=x.device)
    i_k = torch.arange(n_k, device=x.device)
    masque = (i_q[:, None] >= i_k[None, :]) & ((i_q[:, None] - i_k[None, :]) < cfg.window)
    y = F.scaled_dot_product_attention(q, k, v, attn_mask=masque)
    y = y.transpose(1, 2).reshape(b, s, d)
    x = x + bloc.out(y)
    return x + bloc.ffn(bloc.ln2(x))


@torch.no_grad()
def passe(modele, ids: list[int], cache: list | None = None, pos_debut: int = 0):
    """Les logits du dernier jeton ; le cache (par bloc) est rempli ou prolongé."""
    x = torch.tensor([ids], dtype=torch.long)
    x = modele.embed(x) + modele.pos(torch.arange(len(ids), device=x.device) + pos_debut)[None]
    nouveaux = [None] * len(modele.blocks) if cache is None else cache
    for i, bloc in enumerate(modele.blocks):
        x = _bloc_avec_cache(bloc, x, nouveaux, i)
        if i == modele.cfg.n_blocks // 2 - 1:
            x = x + modele.bridge(x)
    h0 = x
    for _ in range(modele.cfg.thought_steps):
        x = torch.tanh(modele.thought(x) + modele.thought_in(h0))
    return modele.head_byte(x)[0, -1], nouveaux


@torch.no_grad()
def generer(modele, prompt: str, n: int = 64, fenetre: int = 1024):
    ids = list(prompt.encode("utf-8")) or [32]
    logits, cache = passe(modele, ids)
    sortie = list(ids)
    for _ in range(n):
        suivant = int(logits.argmax())
        sortie.append(suivant)
        if len(sortie) >= fenetre:
            break
        logits, cache = passe(modele, [suivant], cache, pos_debut=len(sortie) - 1)
    return bytes(sortie).decode("utf-8", "replace")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="work/n2ac/mix1024-60k.pt")
    ap.add_argument("--prompt", default="La France est un pays")
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    modele, cfg = charger(a.modele)
    t0 = time.perf_counter()
    texte = generer(modele, a.prompt, a.n, min(cfg.window, cfg.max_pos))
    dt = time.perf_counter() - t0
    if a.json:
        print(json.dumps({"schema": "drave.generation", "version": 1, "moteur": "torch+kvcache",
                          "modele": a.modele, "prompt": a.prompt, "n": a.n, "texte": texte,
                          "s": round(dt, 3), "octets_s": round(a.n / dt, 1)}, ensure_ascii=False))
    else:
        print(texte)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""kv_ppl.py — A7.12 : la PPL d'un vrai modèle avec K/V quantifiés int8.

A7.10/A7.11 mesuraient la reconstruction et l'attention isolée. Ici on branche
des hooks sur `k_proj` et `v_proj` de **toutes** les couches de Qwen2.5-0.5B :
la sortie est quantifiée par canal (int8), déquantifiée, puis l'attention
continue. On compare la PPL au modèle intact.
"""
from __future__ import annotations

import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODELE = "Qwen/Qwen2.5-0.5B-Instruct"
TEXTES = [
    "La mesure est reine ; ce qui n'est pas compté n'existe pas.",
    "Un train part de Montréal à 8 h et roule à 90 km/h.",
    "def fibonacci(n):\n    if n < 2:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n",
    "Toute personne a droit à la liberté d'expression.",
    "Le silence est la réponse que le monde préfère.",
]


def _ppl(modele, tok, textes, device="cuda"):
    total, n = 0.0, 0
    with torch.no_grad():
        for t in textes:
            ids = tok(t, return_tensors="pt").input_ids.to(device)
            if ids.shape[1] < 2:
                continue
            out = modele(ids, labels=ids)
            total += float(out.loss) * (ids.shape[1] - 1)
            n += ids.shape[1] - 1
    return total / max(1, n), n


def _hook(module, entree, sortie):
    # sortie : (1, seq, 2 * head_dim * n_kv_heads)
    x = sortie
    echelle = x.abs().amax(dim=0, keepdim=True).clamp_min(1e-12) / 127.0
    q = (x / echelle).round().clamp(-127, 127)
    return q * echelle


def mesurer(device: str = "cuda") -> dict:
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    base, n = _ppl(m, tok, TEXTES, device)
    hooks = []
    for layer in m.model.layers:
        hooks.append(layer.self_attn.k_proj.register_forward_hook(_hook))
        hooks.append(layer.self_attn.v_proj.register_forward_hook(_hook))
    quant, _ = _ppl(m, tok, TEXTES, device)
    for h in hooks:
        h.remove()
    return {
        "modele": MODELE, "device": device, "ntokens": n,
        "ppl_base": base, "ppl_kv_int8": quant,
        "delta": quant - base, "ratio": quant / base,
        "couches": len(m.model.layers),
    }


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

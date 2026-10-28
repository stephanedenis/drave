#!/usr/bin/env python3
"""kv_gen.py — A7.14 : génération greedy avec K/V int8.

A7.13 mesurait la PPL. Ici on génère 16 jetons en greedy avec les mêmes hooks
int8 par canal sur k_proj/v_proj, et on compare les jetons au modèle intact.
"""
from __future__ import annotations

import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from tools.kv_ppl import MODELE, _hook

PROMPT = "La mesure est reine parce que"


def _gen(modele, ids, n=16):
    with torch.no_grad():
        out = modele.generate(ids, max_new_tokens=n, do_sample=False,
                              pad_token_id=0)
    return out[0, ids.shape[1]:].tolist()


def mesurer(device: str = "cuda", n: int = 16) -> dict:
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    ids = tok(PROMPT, return_tensors="pt").input_ids.to(device)
    base = _gen(m, ids, n)
    hooks = []
    for layer in m.model.layers:
        hooks.append(layer.self_attn.k_proj.register_forward_hook(_hook))
        hooks.append(layer.self_attn.v_proj.register_forward_hook(_hook))
    quant = _gen(m, ids, n)
    for h in hooks:
        h.remove()
    return {"modele": MODELE, "device": device, "prompt": PROMPT, "n": n,
            "base": base, "kv_int8": quant,
            "identiques": base == quant,
            "accord": sum(a == b for a, b in zip(base, quant)) / max(1, len(base)),
            "texte_base": tok.decode(base), "texte_int8": tok.decode(quant)}


if __name__ == "__main__":
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))

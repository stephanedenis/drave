#!/usr/bin/env python3
"""kv_ppl_long.py — A7.13 : K/V int8 sur 512 jetons.

A7.12 ne testait que 85 jetons. Ici on prend un texte long (UDHR concaténé)
et on mesure la PPL avec les mêmes hooks int8 par canal sur les 24 couches.
"""
from __future__ import annotations

import json
import pathlib

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from tools.kv_ppl import MODELE, _hook


def _texte() -> str:
    p = pathlib.Path("data/udhr/udhr_10_train.txt")
    if p.exists():
        return p.read_text(encoding="utf-8")
    return "La mesure est reine. " * 200


def _ppl(modele, ids):
    with torch.no_grad():
        out = modele(ids, labels=ids)
    return float(out.loss), int(ids.shape[1] - 1)


def mesurer(ntok: int = 512, device: str = "cuda") -> dict:
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    ids = tok(_texte(), return_tensors="pt").input_ids[:, :ntok].to(device)
    if ids.shape[1] < 8:
        raise ValueError("texte trop court")
    base, n = _ppl(m, ids)
    hooks = []
    for layer in m.model.layers:
        hooks.append(layer.self_attn.k_proj.register_forward_hook(_hook))
        hooks.append(layer.self_attn.v_proj.register_forward_hook(_hook))
    quant, _ = _ppl(m, ids)
    for h in hooks:
        h.remove()
    return {"modele": MODELE, "device": device, "ntokens": n,
            "ppl_base": base, "ppl_kv_int8": quant,
            "delta": quant - base, "ratio": quant / base,
            "couches": len(m.model.layers)}


if __name__ == "__main__":
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))

#!/usr/bin/env python3
"""kv_cache_int8.py — A7.16 : cache KV int8 réellement stocké.

A7.12–A7.15 quantifiaient les projections avant l'attention. Ici on quantifie
le **cache** lui-même : `CacheInt8` remplace `DynamicCache`, quantifie `keys` et
`values` après chaque `update`, et le pas suivant lit le cache quantifié.
"""
from __future__ import annotations

import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.cache_utils import DynamicCache

from tools.kv_ppl import MODELE

PROMPT = "La mesure est reine parce que"


def _q(x: torch.Tensor) -> torch.Tensor:
    # x : (batch, heads, seq, head_dim) -> échelle par (batch, heads, 1, head_dim)
    echelle = x.abs().amax(dim=-2, keepdim=True).clamp_min(1e-12) / 127.0
    q = (x / echelle).round().clamp(-127, 127)
    return q * echelle


class CacheInt8(DynamicCache):
    """Un cache dynamique dont les K/V stockés sont quantifiés int8 par canal."""

    def update(self, key_states, value_states, layer_idx, *args, **kwargs):
        keys, values = super().update(key_states, value_states, layer_idx, *args, **kwargs)
        layer = self.layers[layer_idx]
        layer.keys = _q(layer.keys)
        layer.values = _q(layer.values)
        return keys, values


def _gen(modele, ids, n):
    with torch.no_grad():
        out = modele.generate(ids, max_new_tokens=n, do_sample=False,
                              pad_token_id=0)
    return out[0, ids.shape[1]:].tolist()


def mesurer(device: str = "cuda", n: int = 32) -> dict:
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    ids = tok(PROMPT, return_tensors="pt").input_ids.to(device)
    base = _gen(m, ids, n)
    quant = _gen(m, ids, n)  # remplacé ci-dessous par un cache int8
    # generate avec cache int8
    with torch.no_grad():
        out = m.generate(ids, max_new_tokens=n, do_sample=False,
                         past_key_values=CacheInt8(), pad_token_id=0)
    quant = out[0, ids.shape[1]:].tolist()
    return {"modele": MODELE, "device": device, "prompt": PROMPT, "n": n,
            "base": base, "cache_int8": quant,
            "identiques": base == quant,
            "accord": sum(a == b for a, b in zip(base, quant)) / max(1, len(base))}


if __name__ == "__main__":
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


class CacheInt8Bloc(CacheInt8):
    """Cache int8 avec une échelle par bloc de 32 jetons (au lieu d'un canal global)."""

    bloc = 32

    def update(self, key_states, value_states, layer_idx, *args, **kwargs):
        keys, values = DynamicCache.update(self, key_states, value_states, layer_idx, *args, **kwargs)
        layer = self.layers[layer_idx]
        layer.keys = self._q_bloc(layer.keys)
        layer.values = self._q_bloc(layer.values)
        return keys, values

    def _q_bloc(self, x):
        # x : (batch, heads, seq, dim) ; blocs sur seq
        morceaux = []
        for i in range(0, x.shape[-2], self.bloc):
            m = x[..., i:i + self.bloc, :]
            echelle = m.abs().amax(dim=-2, keepdim=True).clamp_min(1e-12) / 127.0
            morceaux.append((m / echelle).round().clamp(-127, 127) * echelle)
        return torch.cat(morceaux, dim=-2)


def mesurer_bloc(device: str = "cuda", n: int = 128) -> dict:
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    ids = tok(PROMPT, return_tensors="pt").input_ids.to(device)
    base = _gen(m, ids, n)
    with torch.no_grad():
        out = m.generate(ids, max_new_tokens=n, do_sample=False,
                         past_key_values=CacheInt8Bloc(), pad_token_id=0)
    q = out[0, ids.shape[1]:].tolist()
    return {"modele": MODELE, "device": device, "prompt": PROMPT, "n": n,
            "base": base, "cache_int8_bloc": q,
            "identiques": base == q,
            "accord": sum(a == b for a, b in zip(base, q)) / max(1, len(base))}


class CacheMixte(DynamicCache):
    """Cache mixte : K/V f32 pour les 64 premiers jetons, int8 au-delà."""

    seuil = 64

    def update(self, key_states, value_states, layer_idx, *args, **kwargs):
        keys, values = super().update(key_states, value_states, layer_idx, *args, **kwargs)
        layer = self.layers[layer_idx]
        if layer.keys.shape[-2] > self.seuil:
            layer.keys[..., self.seuil:, :] = _q(layer.keys[..., self.seuil:, :])
            layer.values[..., self.seuil:, :] = _q(layer.values[..., self.seuil:, :])
        return keys, values


def mesurer_mixte(device: str = "cuda", n: int = 128) -> dict:
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    ids = tok(PROMPT, return_tensors="pt").input_ids.to(device)
    base = _gen(m, ids, n)
    with torch.no_grad():
        out = m.generate(ids, max_new_tokens=n, do_sample=False,
                         past_key_values=CacheMixte(), pad_token_id=0)
    q = out[0, ids.shape[1]:].tolist()
    return {"modele": MODELE, "device": device, "prompt": PROMPT, "n": n,
            "base": base, "cache_mixte": q,
            "identiques": base == q,
            "accord": sum(a == b for a, b in zip(base, q)) / max(1, len(base))}


class CacheFenetre(DynamicCache):
    """Cache à fenêtre f32 : les 64 derniers jetons restent f32, le reste int8."""

    fenetre = 64

    def update(self, key_states, value_states, layer_idx, *args, **kwargs):
        keys, values = super().update(key_states, value_states, layer_idx, *args, **kwargs)
        layer = self.layers[layer_idx]
        if layer.keys.shape[-2] > self.fenetre:
            layer.keys[..., :-self.fenetre, :] = _q(layer.keys[..., :-self.fenetre, :])
            layer.values[..., :-self.fenetre, :] = _q(layer.values[..., :-self.fenetre, :])
        return keys, values


def mesurer_fenetre(device: str = "cuda", n: int = 256) -> dict:
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    ids = tok(PROMPT, return_tensors="pt").input_ids.to(device)
    base = _gen(m, ids, n)
    with torch.no_grad():
        out = m.generate(ids, max_new_tokens=n, do_sample=False,
                         past_key_values=CacheFenetre(), pad_token_id=0)
    q = out[0, ids.shape[1]:].tolist()
    return {"modele": MODELE, "device": device, "prompt": PROMPT, "n": n,
            "base": base, "cache_fenetre": q,
            "identiques": base == q,
            "accord": sum(a == b for a, b in zip(base, q)) / max(1, len(base))}


class CacheMixte128(CacheMixte):
    """Cache mixte avec 128 premiers jetons en f32 (au lieu de 64)."""

    seuil = 128


def mesurer_mixte128(device: str = "cuda", n: int = 256) -> dict:
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    ids = tok(PROMPT, return_tensors="pt").input_ids.to(device)
    base = _gen(m, ids, n)
    with torch.no_grad():
        out = m.generate(ids, max_new_tokens=n, do_sample=False,
                         past_key_values=CacheMixte128(), pad_token_id=0)
    q = out[0, ids.shape[1]:].tolist()
    return {"modele": MODELE, "device": device, "prompt": PROMPT, "n": n,
            "base": base, "cache_mixte128": q,
            "identiques": base == q,
            "accord": sum(a == b for a, b in zip(base, q)) / max(1, len(base))}


class CacheMixte32(CacheMixte):
    """Cache mixte avec 32 premiers jetons en f32."""

    seuil = 32


def mesurer_mixte32(device: str = "cuda", n: int = 256) -> dict:
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    ids = tok(PROMPT, return_tensors="pt").input_ids.to(device)
    base = _gen(m, ids, n)
    with torch.no_grad():
        out = m.generate(ids, max_new_tokens=n, do_sample=False,
                         past_key_values=CacheMixte32(), pad_token_id=0)
    q = out[0, ids.shape[1]:].tolist()
    return {"modele": MODELE, "device": device, "prompt": PROMPT, "n": n,
            "base": base, "cache_mixte32": q,
            "identiques": base == q,
            "accord": sum(a == b for a, b in zip(base, q)) / max(1, len(base))}


class CacheMixte48(CacheMixte):
    seuil = 48


class CacheMixte96(CacheMixte):
    seuil = 96


def _mesurer_seuil(classe, device="cuda", n=256):
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    ids = tok(PROMPT, return_tensors="pt").input_ids.to(device)
    base = _gen(m, ids, n)
    with torch.no_grad():
        out = m.generate(ids, max_new_tokens=n, do_sample=False,
                         past_key_values=classe(), pad_token_id=0)
    q = out[0, ids.shape[1]:].tolist()
    first = next((i for i, (x, y) in enumerate(zip(base, q)) if x != y), None)
    return {"n": n, "premier_divergence": first,
            "accord": sum(a == b for a, b in zip(base, q)) / max(1, len(base)),
            "identiques": base == q}


def mesurer_48(device="cuda", n=256):
    return _mesurer_seuil(CacheMixte48, device, n)


def mesurer_96(device="cuda", n=256):
    return _mesurer_seuil(CacheMixte96, device, n)


PROMPTS = [
    "La mesure est reine parce que",
    "Un train part de Montréal à 8 h et roule à 90 km/h. Il croise",
    "Toute personne a droit à la liberté d'expression, ce qui signifie",
]


def mesurer_multi(device: str = "cuda", n: int = 256) -> dict:
    tok = AutoTokenizer.from_pretrained(MODELE)
    m = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32).to(device).eval()
    lignes = []
    for p in PROMPTS:
        ids = tok(p, return_tensors="pt").input_ids.to(device)
        base = _gen(m, ids, n)
        with torch.no_grad():
            out = m.generate(ids, max_new_tokens=n, do_sample=False,
                             past_key_values=CacheMixte(), pad_token_id=0)
        q = out[0, ids.shape[1]:].tolist()
        first = next((i for i, (x, y) in enumerate(zip(base, q)) if x != y), None)
        lignes.append({"prompt": p, "premier_divergence": first,
                       "accord": sum(a == b for a, b in zip(base, q)) / max(1, len(base))})
    return {"n": n, "seuil": 64, "prompts": lignes,
            "accord_moyen": sum(l["accord"] for l in lignes) / len(lignes)}

#!/usr/bin/env python3
"""generer_natif.py — N4.1 : génération contrôlée avec `drave-n0`.

Le modèle est byte-level : le prompt est encodé en UTF-8, la sortie est décodée
en UTF-8 avec remplacement. La génération par défaut est **greedy** et
déterministe ; `--top-k` restreint le choix sans tirage aléatoire.
"""
from __future__ import annotations

import argparse
import json
import pathlib

import torch
import torch.nn.functional as F

from tools.native_model import NativeConfig, NativeModel


def charger(chemin: str, device: str = "cpu"):
    ck = torch.load(chemin, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items() if k in NativeConfig.__annotations__})
    m = NativeModel(cfg); m.load_state_dict(ck["state"]); m.to(device).eval()
    return m, cfg


@torch.no_grad()
def generer(modele, prompt: str, n: int = 128, top_k: int = 0, temperature: float = 0.0,
            penalite: float = 0.0):
    ids = list(prompt.encode("utf-8"))
    if not ids:
        ids = [32]
    for _ in range(n):
        x = torch.tensor([ids[-modele.cfg.max_pos:]], dtype=torch.long,
                         device=next(modele.parameters()).device)
        logits = modele(x)["logits"][0, -1]
        if penalite > 0 and len(ids) > len(prompt.encode()):
            recents = ids[-32:]
            for b in set(recents):
                logits[b] -= penalite * recents.count(b)
        if temperature <= 0:
            suivant = int(logits.argmax())
        else:
            logits = logits / temperature
            if top_k > 0:
                v, i = logits.topk(min(top_k, logits.numel()))
                logits = torch.full_like(logits, float("-inf")); logits[i] = v
            suivant = int(torch.multinomial(F.softmax(logits, -1), 1))
        ids.append(suivant)
        if suivant == 10 and len(ids) > len(prompt.encode()):
            break
    return bytes(ids)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="/tmp/drave-n0-distille.pt")
    ap.add_argument("--prompt", default="La France est un pays")
    ap.add_argument("--n", type=int, default=128)
    ap.add_argument("--top-k", type=int, default=0)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--penalite", type=float, default=0.0,
                    help="pénalité de répétition (soustraction par fréquence sur 32 octets)")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--json", default="reports/native-generation.json")
    a = ap.parse_args()
    m, cfg = charger(a.modele, a.device)
    b = generer(m, a.prompt, a.n, a.top_k, a.temperature)
    texte = b.decode("utf-8", errors="replace")
    res = {"modele": a.modele, "parametres": m.nb_parametres(), "prompt": a.prompt,
           "n": a.n, "top_k": a.top_k, "temperature": a.temperature,
           "octets": len(b), "texte": texte}
    pathlib.Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    print(texte)


if __name__ == "__main__":
    main()

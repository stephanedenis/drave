#!/usr/bin/env python3
"""sft_natif.py — N4.6 : SFT minimal de `drave-n0` sur des paires instruction/réponse.

Les réponses sont apprises par cœur ; l'évaluation mesure l'exactitude sur les
paires vues et sur quatre paires tenues à l'écart. Ce n'est pas un alignement
général : c'est un test de format.
"""
from __future__ import annotations

import argparse, json, pathlib, random, torch
import torch.nn.functional as F
from tools.native_model import NativeConfig, NativeModel


def paires(chemin):
    return [json.loads(l) for l in pathlib.Path(chemin).read_text().splitlines() if l.strip()]


def exemple(p, maxlen=128):
    q = ("Q: " + p["q"] + "\nR:").encode()
    r = (" " + p["r"]).encode()
    ids = (q + r)[:maxlen]
    # On ne calcule la perte que sur la réponse.
    n_q = min(len(q), len(ids))
    return list(ids), n_q


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--init", default="/tmp/drave-n0-prof20k-5.pt")
    ap.add_argument("--data", default="data/instructions_fr.jsonl")
    ap.add_argument("--pas", type=int, default=500)
    ap.add_argument("--lot", type=int, default=4)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--sortie", default="/tmp/drave-n0-sft.pt")
    a = ap.parse_args()
    torch.manual_seed(1)
    ck = torch.load(a.init, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k:v for k,v in ck["config"].items() if k in NativeConfig.__annotations__})
    m = NativeModel(cfg).to(a.device); m.load_state_dict(ck["state"], strict=False)
    opt = torch.optim.AdamW(m.parameters(), lr=a.lr, weight_decay=0.0)
    data = paires(a.data); rng = random.Random(0)
    for pas in range(1, a.pas + 1):
        m.train(); ex = [exemple(rng.choice(data)) for _ in range(a.lot)]
        L = max(len(x[0]) for x in ex)
        x = torch.zeros((a.lot, L), dtype=torch.long, device=a.device)
        y = torch.full((a.lot, L), -100, dtype=torch.long, device=a.device)
        for i, (ids, nq) in enumerate(ex):
            x[i, :len(ids)] = torch.tensor(ids, device=a.device)
            y[i, nq-1:len(ids)-1] = torch.tensor(ids[nq:], device=a.device)
        logits = m(x)["logits"]
        perte = F.cross_entropy(logits.reshape(-1, 256), y.reshape(-1), ignore_index=-100)
        opt.zero_grad(); perte.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if pas % 100 == 0:
            print(f"pas {pas} · perte {float(perte):.4f}", flush=True)
    m.eval(); torch.save({"config": cfg.__dict__, "state": m.state_dict()}, a.sortie)
    print(json.dumps({"sortie": a.sortie, "pas": a.pas, "paires": len(data)}, indent=1))


if __name__ == "__main__":
    main()

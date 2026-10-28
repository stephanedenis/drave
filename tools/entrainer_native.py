#!/usr/bin/env python3
"""entrainer_native.py — entraînement de base de `drave-n0`.

Ce n'est que le **prochain octet** : les pertes locales, les têtes précoces, la
pensée et le pont viendront après. Le but est de mesurer la PPL du modèle natif
et de produire un DRVM lisible par le moteur.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import time

import torch
import torch.nn.functional as F

from tools.native_model import NativeConfig, NativeModel, exporter_drvm


def charger(chemin: str) -> torch.Tensor:
    b = pathlib.Path(chemin).read_bytes()
    if len(b) < 100_000:
        raise SystemExit(f"{chemin} : corpus trop court")
    return torch.tensor(list(b), dtype=torch.long)


def lot(data: torch.Tensor, n: int, seq: int, device: str):
    i = torch.randint(0, len(data) - seq - 1, (n,))
    x = torch.stack([data[j:j + seq] for j in i]).to(device)
    y = torch.stack([data[j + 1:j + seq + 1] for j in i]).to(device)
    return x, y


def ppl(modele, data, seq, lot_n, device, n_lots=8):
    modele.eval(); total = 0.0; n = 0
    with torch.no_grad():
        for _ in range(n_lots):
            x, y = lot(data, lot_n, seq, device)
            logits = modele(x)["logits"]
            total += float(F.cross_entropy(logits.reshape(-1, 256), y.reshape(-1),
                                           reduction="sum"))
            n += y.numel()
    return math.exp(total / max(1, n)), n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/corpus_fr.txt")
    ap.add_argument("--pas", type=int, default=200)
    ap.add_argument("--seq", type=int, default=128)
    ap.add_argument("--lot", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--sortie", default="/tmp/drave-n0.pt")
    ap.add_argument("--drvm", default="/tmp/drave-n0.drvm")
    ap.add_argument("--graine", type=int, default=1)
    a = ap.parse_args()
    torch.manual_seed(a.graine)
    data = charger(a.corpus)
    n_val = max(10_000, len(data) // 20)
    train, val = data[:-n_val], data[-n_val:]
    cfg = NativeConfig()
    modele = NativeModel(cfg).to(a.device)
    opt = torch.optim.AdamW(modele.parameters(), lr=a.lr, weight_decay=0.01)
    t0 = time.time(); pertes = []
    for pas in range(1, a.pas + 1):
        modele.train()
        x, y = lot(train, a.lot, a.seq, a.device)
        logits = modele(x)["logits"]
        perte = F.cross_entropy(logits.reshape(-1, 256), y.reshape(-1))
        opt.zero_grad(); perte.backward()
        torch.nn.utils.clip_grad_norm_(modele.parameters(), 1.0)
        opt.step(); pertes.append(float(perte))
        if pas % 50 == 0 or pas == 1:
            p, n = ppl(modele, val, a.seq, a.lot, a.device, n_lots=2)
            print(f"pas {pas:4d} · perte {float(perte):.4f} · PPL val {p:.3f} · {time.time()-t0:.0f} s", flush=True)
    p_val, n_tok = ppl(modele, val, a.seq, a.lot, a.device, n_lots=8)
    modele.eval()
    torch.save({"config": cfg.__dict__, "state": modele.state_dict()}, a.sortie)
    h = exporter_drvm(modele, a.drvm)
    res = {"modele": "drave-n0", "parametres": modele.nb_parametres(),
           "corpus": a.corpus, "octets": len(data), "pas": a.pas,
           "seq": a.seq, "lot": a.lot, "lr": a.lr, "graine": a.graine,
           "perte_finale": pertes[-1], "ppl_val": p_val, "jetons_val": n_tok,
           "drvm": a.drvm, "sha256_drvm": h, "duree_s": time.time() - t0}
    pathlib.Path(a.sortie + ".json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

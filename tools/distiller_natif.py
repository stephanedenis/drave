#!/usr/bin/env python3
"""distiller_natif.py — N2.3 : distiller `drave-n0` depuis un professeur octet.

Le professeur est un Qwen3-MoE byte-level entraîné par `entrainer_moteur.py`
(`/tmp/route-teacher`), le student est `drave-n0`. Les deux parlent 256 octets :
la distillation est donc directe, sans tokenizer intermédiaire.
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


def charger(txt: str) -> torch.Tensor:
    b = pathlib.Path(txt).read_bytes()
    return torch.tensor(list(b), dtype=torch.long)


def lot(data, n, seq, device):
    i = torch.randint(0, len(data) - seq - 1, (n,))
    x = torch.stack([data[j:j + seq] for j in i]).to(device)
    y = torch.stack([data[j + 1:j + seq + 1] for j in i]).to(device)
    return x, y


def ppl(modele, data, seq, lot_n, device, n_lots=8):
    modele.eval(); tot = 0.0; n = 0
    with torch.no_grad():
        for _ in range(n_lots):
            x, y = lot(data, lot_n, seq, device)
            logits = modele(x)["logits"]
            tot += float(F.cross_entropy(logits.reshape(-1, 256), y.reshape(-1),
                                         reduction="sum")); n += y.numel()
    return math.exp(tot / max(1, n))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--enseignant", default="/tmp/route-teacher")
    ap.add_argument("--init", default="/tmp/drave-n0-pont.pt")
    ap.add_argument("--train", default="data/corpus_fr_train.txt")
    ap.add_argument("--val", default="data/corpus_fr_val.txt")
    ap.add_argument("--pas", type=int, default=2000)
    ap.add_argument("--lot", type=int, default=16)
    ap.add_argument("--seq", type=int, default=128)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--temperature", type=float, default=2.0)
    ap.add_argument("--alpha", type=float, default=0.7)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--sortie", default="/tmp/drave-n0-distille.pt")
    ap.add_argument("--drvm", default="/tmp/drave-n0-distille.drvm")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--tetes", action=argparse.BooleanOptionalAction, default=True,
                    help="ajouter les têtes précoces à la distillation")
    a = ap.parse_args()
    torch.manual_seed(a.graine)
    from transformers import AutoModelForCausalLM
    prof = AutoModelForCausalLM.from_pretrained(a.enseignant, dtype=torch.float32).to(a.device).eval()
    for p in prof.parameters(): p.requires_grad_(False)
    ck = torch.load(a.init, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items() if k in NativeConfig.__annotations__})
    etu = NativeModel(cfg).to(a.device); etu.load_state_dict(ck["state"])
    opt = torch.optim.AdamW(etu.parameters(), lr=a.lr, weight_decay=0.01)
    train, val = charger(a.train), charger(a.val)
    t0 = time.time(); pertes = []
    for pas in range(1, a.pas + 1):
        etu.train(); x, y = lot(train, a.lot, a.seq, a.device)
        with torch.no_grad():
            lp = prof(x).logits
        sortie = etu(x); ls = sortie["logits"]
        T = a.temperature
        kd = F.kl_div(F.log_softmax(ls / T, -1), F.softmax(lp / T, -1),
                      reduction="batchmean", log_target=False) * (T * T)
        ce = F.cross_entropy(ls.reshape(-1, 256), y.reshape(-1))
        perte = a.alpha * kd + (1 - a.alpha) * ce
        if a.tetes:
            for e in sortie["early"]:
                perte = perte + 0.1 * F.cross_entropy(e.reshape(-1, 256), y.reshape(-1))
        opt.zero_grad(); perte.backward()
        torch.nn.utils.clip_grad_norm_(etu.parameters(), 1.0)
        opt.step(); pertes.append(float(perte))
        if pas % 250 == 0:
            p = ppl(etu, val, a.seq, a.lot, a.device, n_lots=2)
            print(f"pas {pas:4d} · perte {float(perte):.4f} · PPL {p:.3f} · {time.time()-t0:.0f} s", flush=True)
    p_etu = ppl(etu, val, a.seq, a.lot, a.device, n_lots=8)
    etu.eval(); bons_main = 0; bons_early = [0]*len(etu.cfg.early_blocks); n_ev = 0
    with torch.no_grad():
        for _ in range(4):
            x, y = lot(val, a.lot, a.seq, a.device)
            s = etu(x)
            bons_main += int((s["logits"].argmax(-1) == y).sum())
            for j, e in enumerate(s["early"]):
                bons_early[j] += int((e.argmax(-1) == y).sum())
            n_ev += y.numel()
    prec_main = bons_main/max(1,n_ev); prec_early = [b/max(1,n_ev) for b in bons_early]
    etu.eval(); torch.save({"config": cfg.__dict__, "state": etu.state_dict()}, a.sortie)
    h = exporter_drvm(etu, a.drvm)
    res = {"professeur": a.enseignant, "student": a.sortie, "pas": a.pas,
           "lot": a.lot, "seq": a.seq, "lr": a.lr, "temperature": a.temperature,
           "alpha": a.alpha, "tetes": a.tetes, "perte_finale": pertes[-1], "ppl_val": p_etu,
           "precision_main": prec_main, "precision_early": prec_early,
           "drvm": a.drvm, "sha256_drvm": h, "duree_s": time.time() - t0}
    pathlib.Path(a.sortie + ".json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

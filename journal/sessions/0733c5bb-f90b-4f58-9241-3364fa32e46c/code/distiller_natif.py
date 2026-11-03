#!/usr/bin/env python3
"""distiller_natif.py — distillation natif → natif : le professeur long, l'élève court.

Le dépôt distillait depuis un professeur **HuggingFace** (`tools/distiller_budget.py`). Ici le
professeur est un `drave-n0` **RoPE à fenêtre longue** (par exemple `rope1024-20k`, 2,6256 à
1 000 octets) et l'élève est un `drave-n0` RoPE **plus petit ou à fenêtre courte**, entraîné sur
des séquences courtes : on mesure ce que les **cibles douces** d'un professeur qui voit loin
apportent à un élève qui ne voit pas si loin.

Perte : `(1-α) · CE(dur, y) + α · T² · KL(professeur_T ‖ élève_T)`, sur les mêmes fenêtres
(octets et canal identiques, Van der Corput), ce qui rend la comparaison à un entraînement
« dur » **à budget strictement égal** (mêmes pas, mêmes lots, même graine, même init).

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/distiller_natif.py \
      --professeur work/n2ac/rope1024-20k.pt --pas 8000 --seq 512 --window 512 \
      --dim 224 --expert-hidden 288 --alpha 0.5 --T 2 \
      --sortie work/n2ac/kd-1147m-512.pt
"""
from __future__ import annotations

import argparse
import json
import pathlib
import time

import torch
import torch.nn.functional as F

from tools.native_model import NativeConfig
from tools.entrainer_native import charger, charger_canal, lot
from work.n2ac.rope_model import NativeModelRoPE, charge_rope


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--professeur", default="work/n2ac/rope1024-20k.pt")
    ap.add_argument("--corpus", default="data/wiki_fr/propre/train.txt")
    ap.add_argument("--canal", default="data/wiki_fr/propre/train.canal")
    ap.add_argument("--pas", type=int, default=8000)
    ap.add_argument("--seq", type=int, default=512)
    ap.add_argument("--window", type=int, default=512)
    ap.add_argument("--lot", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--alpha", type=float, default=0.5)
    ap.add_argument("--T", type=float, default=2.0)
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--dim", type=int, default=224)
    ap.add_argument("--expert-hidden", type=int, default=288)
    ap.add_argument("--init", default=None)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--sortie", default="work/n2ac/kd.pt")
    ap.add_argument("--drvm", default="work/n2ac/kd.drvm")
    a = ap.parse_args()

    torch.manual_seed(a.graine)
    # L'ÉLÈVE D'ABORD : il doit recevoir le même tirage aléatoire que dans `entrainer_rope.py`
    # (le professeur, s'il était chargé avant, consommerait le RNG et l'init différerait).
    cfg = NativeConfig(d_model=a.dim, expert_hidden=a.expert_hidden, window=a.window,
                       max_pos=2048)
    eleve = NativeModelRoPE(cfg).to(a.device)
    data = charger(a.corpus)
    canal_data = charger_canal(a.canal)
    n_val = max(10_000, len(data) // 20)
    train, val = data[:-n_val], data[-n_val:]
    ctrain, cval = canal_data[:-n_val], canal_data[-n_val:]

    prof = charge_rope(a.professeur, device=a.device)
    prof.eval()
    for p in prof.parameters():
        p.requires_grad_(False)
    print(f"  professeur : {a.professeur} (fenêtre {prof.cfg.window})", flush=True)
    if a.init:
        ck = torch.load(a.init, map_location="cpu", weights_only=False)
        eleve.load_state_dict(ck["state"], strict=False)
        print(f"  init : {a.init}", flush=True)
    opt = torch.optim.AdamW(eleve.parameters(), lr=a.lr, weight_decay=0.01)
    t0 = time.time()
    derniere = 0.0
    for pas in range(1, a.pas + 1):
        eleve.train()
        x, y, c = lot(train, a.lot, a.seq, a.device, pas * a.lot, ctrain)
        with torch.no_grad():
            logits_p = prof(x, canal=c)["logits"]
        logits_e = eleve(x, canal=c)["logits"]
        dure = F.cross_entropy(logits_e.reshape(-1, 256), y.reshape(-1))
        douce = F.kl_div(F.log_softmax(logits_e.reshape(-1, 256) / a.T, dim=-1),
                         F.softmax(logits_p.reshape(-1, 256) / a.T, dim=-1),
                         reduction="batchmean") * (a.T ** 2)
        perte = (1 - a.alpha) * dure + a.alpha * douce
        # Parité avec `entrainer_rope.py` : les têtes précoces sont supervisées aussi, pour que
        # la comparaison « distillée vs dure » porte sur le MÊME entraînement.
        for e in eleve(x, canal=c)["early"]:
            perte = perte + F.cross_entropy(e.reshape(-1, 256), y.reshape(-1)) / (
                1 + len(eleve.cfg.early_blocks))
        opt.zero_grad()
        perte.backward()
        torch.nn.utils.clip_grad_norm_(eleve.parameters(), 1.0)
        opt.step()
        derniere = float(perte)
        if pas % 50 == 0 or pas == 1:
            print(f"pas {pas:5d} · perte {derniere:.4f} · dure {float(dure):.4f} · "
                  f"douce {float(douce):.4f} · {time.time() - t0:.0f} s", flush=True)
    eleve.eval()
    torch.save({"config": cfg.__dict__, "state": eleve.state_dict()}, a.sortie)
    res = {"modele": "drave-n0-rope-kd", "professeur": a.professeur, "pas": a.pas,
           "seq": a.seq, "window": a.window, "alpha": a.alpha, "T": a.T,
           "dim": a.dim, "expert_hidden": a.expert_hidden, "graine": a.graine,
           "perte_finale": derniere, "duree_s": time.time() - t0, "corpus": a.corpus}
    pathlib.Path(a.sortie + ".json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()

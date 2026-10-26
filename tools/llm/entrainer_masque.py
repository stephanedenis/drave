#!/usr/bin/env python3
"""entrainer_masque.py — distiller `route` sans compter la perte des prompts.

Le corpus de `distillation.py` mêle le prompt et la réponse. Le premier
entraînement comptait la perte sur **tout** le texte : le modèle apprenait
surtout la distribution des réponses, et le contrôle mélangé faisait aussi bien.
Ici, le prompt est **lu** (il conditionne l'état) mais sa perte est **masquée** :
seule la réponse du professeur compte.

Ce script est un **banc**, pas le moteur : il utilise l'architecture de
`entrainer_moteur.construire` (Qwen3-MoE, exportable) et la même tokenisation
byte-level, mais sa boucle est séparée pour que le masque soit explicite.

Usage :
    python3 tools/llm/entrainer_masque.py \
        --train data/deepseek/distillation-300/train.txt \
        --val data/deepseek/distillation-300/val.txt \
        --dim 192 --couches 4 --cache 384 --experts 8 --k 2 \
        --pas 500 --sortie /tmp/natif-masque
"""
from __future__ import annotations

import argparse
import math
import pathlib
import random
import sys
import time
from types import SimpleNamespace

import torch
import torch.nn.functional as F

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from entrainer_moteur import construire  # noqa: E402
from llm.masque import exemples, fenetre, fenetres_validation  # noqa: E402


def _modele(args, dev):
    a = SimpleNamespace(
        famille="route", dim=args.dim, couches=args.couches, tetes=args.tetes,
        cache=args.cache, cache_perle=max(1, args.cache // max(1, args.k)),
        experts=args.experts, k=args.k, seq=args.seq, init=args.init,
        graine=args.graine)
    modele, _ = construire("route", a)
    return modele.to(dev)


def _perte(modele, x, m):
    sortie = modele(input_ids=x)
    logits = sortie.logits[:, :-1, :]
    cibles = x[:, 1:]
    masque = m[:, 1:]
    perte = F.cross_entropy(logits.reshape(-1, logits.shape[-1]),
                            cibles.reshape(-1), reduction="none").reshape(cibles.shape)
    return (perte * masque).sum() / masque.sum().clamp_min(1.0), masque.sum()


def _validation(modele, exemples_val, seq, dev, max_exemples: int = 200):
    modele.eval()
    total, n = 0.0, 0.0
    with torch.no_grad():
        for prompt, reponse in exemples_val[:max_exemples]:
            for x, m in fenetres_validation(prompt, reponse, seq):
                xt = torch.tensor([x], dtype=torch.long, device=dev)
                mt = torch.tensor([m], dtype=torch.float32, device=dev)
                p, k = _perte(modele, xt, mt)
                total += float(p) * float(k)
                n += float(k)
    modele.train()
    return total / max(n, 1.0) / math.log(2), int(n)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="data/deepseek/distillation-300/train.txt")
    ap.add_argument("--val", default="data/deepseek/distillation-300/val.txt")
    ap.add_argument("--dim", type=int, default=192)
    ap.add_argument("--couches", type=int, default=4)
    ap.add_argument("--tetes", type=int, default=8)
    ap.add_argument("--cache", type=int, default=384)
    ap.add_argument("--experts", type=int, default=8)
    ap.add_argument("--k", type=int, default=2)
    ap.add_argument("--seq", type=int, default=128)
    ap.add_argument("--lot", type=int, default=8)
    ap.add_argument("--pas", type=int, default=500)
    ap.add_argument("--eval-tous", type=int, default=250)
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--init", type=float, default=0.08)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--warmup", type=int, default=50)
    ap.add_argument("--clip", type=float, default=1.0)
    ap.add_argument("--sans-gpu", action="store_true")
    ap.add_argument("--sortie", default="")
    args = ap.parse_args()
    dev = torch.device("cpu" if args.sans_gpu or not torch.cuda.is_available() else "cuda")
    torch.manual_seed(args.graine)
    rng = random.Random(args.graine)
    train = exemples(pathlib.Path(args.train).read_text(encoding="utf-8"))
    val = exemples(pathlib.Path(args.val).read_text(encoding="utf-8"))
    modele = _modele(args, dev)
    n_params = sum(p.numel() for p in modele.parameters())
    print(f"# route masque · {n_params/1e6:.2f} M parametres · {dev} · "
          f"{len(train)} train / {len(val)} val · seq {args.seq}")
    opt = torch.optim.AdamW(modele.parameters(), lr=args.lr)
    if args.warmup > 0:
        plan = torch.optim.lr_scheduler.LambdaLR(
            opt, lambda pas: min(1.0, (pas + 1) / args.warmup))
    else:
        plan = None
    t0 = time.monotonic()
    for pas in range(1, args.pas + 1):
        xs, ms = [], []
        for _ in range(args.lot):
            prompt, reponse = rng.choice(train)
            x, m = fenetre(prompt, reponse, args.seq, rng)
            xs.append(x)
            ms.append(m)
        x = torch.tensor(xs, dtype=torch.long, device=dev)
        m = torch.tensor(ms, dtype=torch.float32, device=dev)
        perte, _ = _perte(modele, x, m)
        opt.zero_grad()
        perte.backward()
        if args.clip > 0:
            torch.nn.utils.clip_grad_norm_(modele.parameters(), args.clip)
        opt.step()
        if plan is not None:
            plan.step()
        if pas % args.eval_tous == 0 or pas == args.pas:
            v, n = _validation(modele, val, args.seq, dev)
            print(f"  pas {pas:5d} · perte {float(perte.detach()):.4f} · val {v:.4f} bits/octet "
                  f"· {time.monotonic()-t0:.0f} s · {n} cibles")
    if args.sortie:
        torch.save({"etat": modele.state_dict(),
                    "args": vars(args)}, args.sortie)
        print(f"  # etat ecrit dans {args.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

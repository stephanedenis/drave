#!/usr/bin/env python3
"""bench/gpu_scatter.py — P1 : la dispersion GPU optimisée bat-elle la projection FPGA ?

LA QUESTION. Le bilan multi-matériel mesure la dispersion GPU à **18,1 G év/s**
avec une primitive à atomiques (type `np.add.at`), et projette **19,3 G év/s**
pour 4 cartes Stratix V (4 × 4,83 G, bornées par leur DDR3). Le FPGA n'a donc,
au mieux, qu'un avantage de 1,07× sur le débit d'événements — et cet avantage
repose sur une primitive GPU **non optimisée**. Avant d'écrire une ligne de RTL,
il faut mesurer la dispersion GPU **optimisée** : c'est la porte P1 d'A5.4.

LES DEUX MÉTHODES.
  1. `index_add_` sur un accumulateur 1-D : atomiques, la référence.
  2. Accumulateurs par **bancs** : `B` accumulateurs, l'événement `i` va au banc
     `i % B`, puis réduction. L'entier est exact, donc le résultat est identique
     au bit près ; seule la contention change.

CONTRÔLE NÉGATIF. Les deux méthodes doivent rendre des accumulateurs **bit-exacts**
(l'entier est associatif) ; un petit cas est comparé à une référence CPU
(`np.bincount`). Si les trois ne s'accordent pas, le banc mesure autre chose que
ce qu'il croit.

Usage :
  python3 bench/gpu_scatter.py --n 67108864 --sortie reports/gpu-scatter.json
"""
from __future__ import annotations

import argparse
import json
import statistics
import time

import numpy as np
import torch


def _dest_val(n: int, o: int, device: torch.device, graine: int = 7):
    g = torch.Generator(device=device).manual_seed(graine)
    dest = torch.randint(0, o, (n,), generator=g, device=device, dtype=torch.int64)
    vals = torch.randint(-8, 9, (n,), generator=g, device=device, dtype=torch.int32)
    return dest, vals


def _bancs(dest: torch.Tensor, b: int, o: int) -> torch.Tensor:
    """L'indice plat du banc de chaque événement : banc * o + destination."""
    n = dest.numel()
    banque = torch.arange(n, device=dest.device, dtype=torch.int64) % b
    return banque * o + dest


def dispersion(dest, vals, o, methode, b=1, reps=3):
    """Temps médian d'une dispersion, et son accumulateur."""
    acc = None
    temps = []
    for _ in range(reps):
        if methode == "index_add":
            acc = torch.zeros(o, dtype=torch.int32, device=dest.device)
            idx = dest
        else:
            acc = torch.zeros(b * o, dtype=torch.int32, device=dest.device)
            idx = _bancs(dest, b, o)
        torch.cuda.synchronize()
        t0 = time.perf_counter()
        acc.index_add_(0, idx, vals)
        torch.cuda.synchronize()
        temps.append(time.perf_counter() - t0)
    if methode != "index_add":
        acc = acc.view(b, o).sum(0)
    return statistics.median(temps), acc


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1 << 26)   # 67,1 M d'événements
    ap.add_argument("--o", type=int, default=4096)      # l'accumulateur du PE (4096 × 24 bits)
    ap.add_argument("--bancs", type=str, default="1,4,16,64")
    ap.add_argument("--gpu", type=int, default=0, help="ordinal CUDA (contrôle inter-cartes)")
    ap.add_argument("--sortie", default="")
    a = ap.parse_args()
    assert torch.cuda.is_available(), "pas de CUDA"
    dev = torch.device(f"cuda:{a.gpu}")
    torch.cuda.set_device(dev)
    props = torch.cuda.get_device_properties(dev)
    print(f"carte : {props.name} · {props.total_memory / 2**30:.1f} Gio · "
          f"{props.multi_processor_count} SM")

    dest, vals = _dest_val(a.n, a.o, dev)

    # Contrôle du harnais : un petit cas comparé à la référence CPU.
    n_petit = 1 << 20
    d_petit, v_petit = _dest_val(n_petit, a.o, dev, graine=1)
    _, acc_np = dispersion(d_petit, v_petit, a.o, "index_add", reps=1)
    cpu = np.bincount(d_petit.cpu().numpy(), weights=v_petit.cpu().numpy().astype(np.float64),
                      minlength=a.o).astype(np.int64)
    ecart = int(np.max(np.abs(cpu - acc_np.cpu().numpy().astype(np.int64))))
    print(f"contrôle CPU (np.bincount) : écart maximal = {ecart}")
    assert ecart == 0, "le harnais GPU ne reproduit pas la référence CPU"

    resultats = {}
    ref = None
    for methode, b in [("index_add", 1)] + [("bancs", int(x)) for x in a.bancs.split(",")]:
        temps, acc = dispersion(dest, vals, a.o, methode, b)
        debit = a.n / temps / 1e9
        nom = f"{methode}" + (f"_b{b}" if methode == "bancs" else "")
        resultats[nom] = {"ms": temps * 1e3, "G_ev_s": debit, "bancs": b}
        print(f"  {nom:14} {temps * 1e3:7.2f} ms  → {debit:6.2f} G év/s")
        if ref is None:
            ref = acc
        else:
            assert torch.equal(ref, acc), f"{nom} ne rend pas le même accumulateur (bit-exact)"
    print("  ✅ toutes les méthodes rendent le MÊME accumulateur (bit-exact)")

    meilleur = max(v["G_ev_s"] for v in resultats.values())
    print(f"meilleur débit : {meilleur:.2f} G év/s  (projection FPGA 4 cartes : 19,3 · "
          f"référence atomiques mesurée : 18,1)")
    if a.sortie:
        with open(a.sortie, "w", encoding="utf-8") as f:
            json.dump({"schema": "drave.gpu-scatter", "version": 1,
                       "carte": props.name, "gpu": a.gpu, "n": a.n, "o": a.o,
                       "resultats": resultats, "meilleur_G_ev_s": meilleur,
                       "controle_cpu_ecart": ecart}, f, indent=1, ensure_ascii=False)
        print(f"  écrit : {a.sortie}")


if __name__ == "__main__":
    main()

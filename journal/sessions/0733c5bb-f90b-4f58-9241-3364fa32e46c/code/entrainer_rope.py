#!/usr/bin/env python3
"""entrainer_rope.py — la recette N2 avec positions **relatives** (R1.1/R1.2).

Identique à `tools/entrainer_native.py` (mêmes fenêtres Van der Corput, même mètre, même
supervision des têtes précoces) à trois exceptions près, toutes déclarées :

  - les blocs sont des `BlockRoPE` (`work/n2ac/rope_model.py`) : plus de table de positions ;
  - `--window` règle le masque d'attention (256 par défaut, la recette N2) ;
  - `--seq` peut dépasser la fenêtre (R1.2) : c'est la fenêtre qui décide de ce que le
    modèle peut lire, pas la longueur de la séquence.

`--positions-aleatoires` est conservé pour la parité d'interface : avec RoPE il est **neutre**
(le décalage de position n'entre plus dans le calcul), ce que l'autotest vérifie.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
      --corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
      --pas 20000 --dim 384 --expert-hidden 512 --init work/n2j/base-wiki-45m.pt \
      --sortie work/n2ac/rope-20k.pt --drvm work/n2ac/rope-20k.drvm
"""
from __future__ import annotations

import argparse
import json
import pathlib
import time

import torch
import torch.nn.functional as F

from tools.native_model import NativeConfig, exporter_drvm
from tools.entrainer_native import charger, charger_canal, lot, ppl
from work.n2ac.rope_model import NativeModelRoPE


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/wiki_fr/propre/train.txt")
    ap.add_argument("--canal", default=None)
    ap.add_argument("--pas", type=int, default=20000)
    ap.add_argument("--seq", type=int, default=128)
    ap.add_argument("--lot", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--sortie", default="work/n2ac/rope.pt")
    ap.add_argument("--drvm", default="work/n2ac/rope.drvm")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--dim", type=int, default=384)
    ap.add_argument("--expert-hidden", type=int, default=512)
    ap.add_argument("--window", type=int, default=256)
    ap.add_argument("--positions-aleatoires", type=int, default=0,
                    help="neutre avec RoPE (gardé pour la parité de l'interface)")
    ap.add_argument("--init", default=None)
    ap.add_argument("--tetes", action=argparse.BooleanOptionalAction, default=True)
    a = ap.parse_args()

    torch.manual_seed(a.graine)
    data = charger(a.corpus)
    canal_data = charger_canal(a.canal) if a.canal else None
    n_val = max(10_000, len(data) // 20)
    train, val = data[:-n_val], data[-n_val:]
    canal_train = canal_data[:-n_val] if canal_data is not None else None
    canal_val = canal_data[-n_val:] if canal_data is not None else None
    cfg = NativeConfig(d_model=a.dim, expert_hidden=a.expert_hidden, window=a.window,
                       max_pos=max(2048, a.seq + 1))
    modele = NativeModelRoPE(cfg).to(a.device)
    if a.init:
        ck = torch.load(a.init, map_location="cpu", weights_only=False)
        modele.load_state_dict(ck["state"], strict=False)
        print(f"  init : {a.init}", flush=True)
    opt = torch.optim.AdamW(modele.parameters(), lr=a.lr, weight_decay=0.01)
    t0 = time.time()
    pertes = []
    for pas in range(1, a.pas + 1):
        modele.train()
        x, y, c = lot(train, a.lot, a.seq, a.device, pas * a.lot, canal_train)
        sortie = modele(x, canal=c)
        pertes = [F.cross_entropy(sortie["logits"].reshape(-1, 256), y.reshape(-1))]
        if a.tetes:
            for e in sortie["early"]:
                pertes.append(F.cross_entropy(e.reshape(-1, 256), y.reshape(-1)))
        perte = sum(pertes) / len(pertes)
        opt.zero_grad()
        perte.backward()
        torch.nn.utils.clip_grad_norm_(modele.parameters(), 1.0)
        opt.step()
        pertes.append(float(perte))
        if pas % 50 == 0 or pas == 1:
            p, n = ppl(modele, val, a.seq, a.lot, a.device, n_lots=2, canal=canal_val)
            print(f"pas {pas:6d} · perte {float(perte):.4f} · PPL val {p:.3f} · "
                  f"{time.time() - t0:.0f} s", flush=True)
    p_val, n_tok = ppl(modele, val, a.seq, a.lot, a.device, n_lots=8, canal=canal_val)
    modele.eval()
    torch.save({"config": cfg.__dict__, "state": modele.state_dict()}, a.sortie)
    h = exporter_drvm(modele, a.drvm)
    res = {"modele": "drave-n0-rope", "parametres": modele.nb_parametres(),
           "corpus": a.corpus, "octets": len(data), "pas": a.pas, "seq": a.seq,
           "lot": a.lot, "lr": a.lr, "graine": a.graine, "window": a.window,
           "positions": "rope", "init": a.init,
           "perte_finale": pertes[-1], "ppl_val": p_val, "jetons_val": n_tok,
           "tetes": a.tetes, "drvm": a.drvm, "sha256_drvm": h,
           "duree_s": time.time() - t0}
    pathlib.Path(a.sortie + ".json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1), flush=True)


if __name__ == "__main__":
    main()

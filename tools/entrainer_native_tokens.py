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
from tools.vdc import departs_vdc


def charger_ids(chemin: str) -> torch.Tensor:
    data = torch.load(chemin, map_location="cpu")
    if data.numel() < 100_000:
        raise SystemExit(f"{chemin} : corpus trop court")
    return data.to(torch.long)


def lot(data: torch.Tensor, n: int, seq: int, device: str, compteur: int):
    # Van der Corput : même compteur = mêmes fenêtres, sans état aléatoire.
    i = torch.tensor(departs_vdc(compteur, n, len(data) - seq - 1, seq), dtype=torch.long)
    x = torch.stack([data[j:j + seq] for j in i]).to(device)
    y = torch.stack([data[j + 1:j + seq + 1] for j in i]).to(device)
    return x, y


def ppl(modele, data, seq, lot_n, device, vocab, n_lots=8, compteur=0):
    modele.eval(); total = 0.0; n = 0
    with torch.no_grad():
        for _ in range(n_lots):
            x, y = lot(data, lot_n, seq, device, compteur + _ * lot_n)
            logits = modele(x)["logits"]
            total += float(F.cross_entropy(logits.reshape(-1, vocab), y.reshape(-1),
                                           reduction="sum"))
            n += y.numel()
    return math.exp(total / max(1, n)), n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True, help="tenseur .pt d'identifiants")
    ap.add_argument("--vocab", type=int, default=256)
    ap.add_argument("--octets", type=int, default=0, help="octets du corpus (bits/octet)")
    ap.add_argument("--pas", type=int, default=200)
    ap.add_argument("--seq", type=int, default=128)
    ap.add_argument("--lot", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--sortie", default="/tmp/drave-n0.pt")
    ap.add_argument("--drvm", default="/tmp/drave-n0.drvm")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--tetes", action=argparse.BooleanOptionalAction, default=True,
                    help="entraîner aussi les têtes précoces")
    a = ap.parse_args()
    torch.manual_seed(a.graine)
    data = charger_ids(a.ids)
    n_val = max(10_000, len(data) // 20)
    train, val = data[:-n_val], data[-n_val:]
    cfg = NativeConfig(vocab=a.vocab)
    modele = NativeModel(cfg).to(a.device)
    opt = torch.optim.AdamW(modele.parameters(), lr=a.lr, weight_decay=0.01)
    t0 = time.time(); pertes = []
    for pas in range(1, a.pas + 1):
        modele.train()
        x, y = lot(train, a.lot, a.seq, a.device, pas * a.lot)
        sortie = modele(x)
        pertes = [F.cross_entropy(sortie["logits"].reshape(-1, a.vocab), y.reshape(-1))]
        if a.tetes:
            for e in sortie["early"]:
                pertes.append(F.cross_entropy(e.reshape(-1, a.vocab), y.reshape(-1)))
        perte = sum(pertes) / len(pertes)
        opt.zero_grad(); perte.backward()
        torch.nn.utils.clip_grad_norm_(modele.parameters(), 1.0)
        opt.step(); pertes.append(float(perte))
        if pas % 50 == 0 or pas == 1:
            p, n = ppl(modele, val, a.seq, a.lot, a.device, a.vocab, n_lots=2)
            print(f"pas {pas:4d} · perte {float(perte):.4f} · PPL val {p:.3f} · {time.time()-t0:.0f} s", flush=True)
    p_val, n_tok = ppl(modele, val, a.seq, a.lot, a.device, a.vocab, n_lots=8)
    # Précision top-1 : tête principale et têtes précoces.
    modele.eval(); bons_main = 0; bons_early = [0] * len(modele.cfg.early_blocks); n_eval = 0
    with torch.no_grad():
        for _ in range(4):
            x, y = lot(val, a.lot, a.seq, a.device, 10_000_000 + _ * a.lot)
            s = modele(x)
            bons_main += int((s["logits"].argmax(-1) == y).sum())
            for j, e in enumerate(s["early"]):
                bons_early[j] += int((e.argmax(-1) == y).sum())
            n_eval += y.numel()
    prec_main = bons_main / max(1, n_eval)
    prec_early = [b / max(1, n_eval) for b in bons_early]
    modele.eval()
    torch.save({"config": cfg.__dict__, "state": modele.state_dict()}, a.sortie)
    h = exporter_drvm(modele, a.drvm)
    res = {"modele": "drave-n0", "parametres": modele.nb_parametres(),
           "ids": a.ids, "octets": a.octets or len(data), "pas": a.pas, "vocab": a.vocab,
           "seq": a.seq, "lot": a.lot, "lr": a.lr, "graine": a.graine,
           "perte_finale": pertes[-1], "ppl_val": p_val, "jetons_val": n_tok,
           "tetes": a.tetes, "precision_main": prec_main,
           "precision_early": prec_early,
           "drvm": a.drvm, "sha256_drvm": h, "duree_s": time.time() - t0}
    octets = a.octets or len(data)
    res["bits_par_octet"] = math.log2(max(p_val, 1e-30)) * len(data) / max(octets, 1)
    res["tokens_par_octet"] = len(data) / max(octets, 1)
    pathlib.Path(a.sortie + ".json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

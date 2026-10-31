#!/usr/bin/env python3
"""distiller_section.py — N2 : distillation avec ou sans état de section.

Le dispositif de N2 est reconstruit : professeur byte-level (23,5 M) entraîné par
`entrainer_moteur.py`, élève `drave-n0` (11,5 M) distillé par `distiller_natif.py`.
Ce script rejoue la distillation **par segments** pour comparer trois bras à budget
strictement égal :

  temoin     : l'élève nu, segments indépendants (aucun état) ;
  hierarchie : un état de section (GRUCell) transporté du segment précédent ;
  controle   : même architecture, état **roulé** = celui d'un autre document du lot.

Chaque pas voit `lot × nseg × seg` octets ; les deux bras voient les mêmes fenêtres
(Van der Corput, déterministe par graine). L'état est détaché entre segments (BPTT
tronquée à un segment) et repart de zéro à chaque pas : les échantillons sont des
documents indépendants.

Usage :
  PYTHONPATH=. gpu-env/bin/python tools/distiller_section.py \
      --enseignant /tmp/n2-campagne/route-teacher-20k \
      --init /tmp/n2-campagne/drave-n0-base-20k.pt \
      --bras hierarchie --graine 1 --pas 5000 --lot 8 --nseg 4 --seg 128 \
      --sortie /tmp/n2-campagne/hierarchie-g1.pt
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import time

import torch
import torch.nn as nn
import torch.nn.functional as F

from tools.native_model import NativeConfig, NativeModel, exporter_drvm
from tools.vdc import departs_vdc


class HierarchieModel(NativeModel):
    """NativeModel + état de section injecté avant les blocs."""

    def __init__(self, cfg: NativeConfig):
        super().__init__(cfg)
        self.section_cell = nn.GRUCell(cfg.d_model, cfg.section_dim)
        self.section_inj = nn.Linear(cfg.section_dim, cfg.d_model, bias=False)

    def forward(self, ids, etat=None):
        b, s = ids.shape
        x = self.embed(ids) + self.pos(torch.arange(s, device=ids.device))[None]
        if etat is not None:
            x = x + self.section_inj(etat)[:, None, :]
        early, local = [], []
        for i, bloc in enumerate(self.blocks):
            x = bloc(x)
            if i == self.cfg.n_blocks // 2 - 1:
                x = x + self.bridge(x)
            local.append(self.local_heads[i](x))
            if i in self.cfg.early_blocks:
                early.append(self.early_heads[self.cfg.early_blocks.index(i)](x))
        h0 = x
        for _ in range(self.cfg.thought_steps):
            x = torch.tanh(self.thought(x) + self.thought_in(h0))
        h = etat if etat is not None else x.new_zeros(b, self.cfg.section_dim)
        return {"logits": self.head_byte(x), "early": early, "local": local,
                "thought": x, "etat": self.section_cell(x.mean(dim=1), h)}


def charger(txt: str) -> torch.Tensor:
    b = pathlib.Path(txt).read_bytes()
    if len(b) < 100_000:
        raise SystemExit(f"{txt} : corpus trop court")
    return torch.tensor(list(b), dtype=torch.long)


def decoupes(data, n, nseg, seg, device, compteur):
    total = nseg * seg + 1
    departs = departs_vdc(compteur, n, len(data) - total - 2, total)
    i = torch.tensor(departs, dtype=torch.long)
    return torch.stack([data[j:j + total] for j in i]).to(device)


def ppl(etu, data, nseg, seg, lot_n, device, bras, n_lots=8, compteur=0):
    etu.eval(); tot = 0.0; n = 0
    with torch.no_grad():
        for k in range(n_lots):
            x = decoupes(data, lot_n, nseg, seg, device, compteur + k * lot_n)
            perte, ntok = 0.0, 0
            etat = None
            for j in range(nseg):
                ids = x[:, j * seg:(j + 1) * seg]
                cible = x[:, j * seg + 1:(j + 1) * seg + 1]
                if bras == "temoin":
                    sortie = etu(ids)
                else:
                    sortie = etu(ids, etat)
                    etat = sortie["etat"].detach()
                perte += float(F.cross_entropy(sortie["logits"].reshape(-1, 256),
                                               cible.reshape(-1), reduction="sum"))
                ntok += cible.numel()
            tot += perte; n += ntok
    return math.exp(tot / max(1, n))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--enseignant", default="/tmp/n2-campagne/route-teacher-20k")
    ap.add_argument("--init", required=True, help="checkpoint de base de l'élève")
    ap.add_argument("--train", default="data/corpus_fr_train.txt")
    ap.add_argument("--val", default="data/corpus_fr_val.txt")
    ap.add_argument("--bras", choices=("temoin", "hierarchie", "controle"), default="temoin")
    ap.add_argument("--pas", type=int, default=5000)
    ap.add_argument("--lot", type=int, default=8)
    ap.add_argument("--nseg", type=int, default=4)
    ap.add_argument("--seg", type=int, default=128)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--temperature", type=float, default=2.0)
    ap.add_argument("--alpha", type=float, default=0.7)
    ap.add_argument("--section-dim", type=int, default=224)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--drvm", default="")
    a = ap.parse_args()

    torch.manual_seed(a.graine)
    from transformers import AutoModelForCausalLM
    prof = AutoModelForCausalLM.from_pretrained(a.enseignant,
                                                dtype=torch.float32).to(a.device).eval()
    for p in prof.parameters():
        p.requires_grad_(False)

    ck = torch.load(a.init, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items()
                          if k in NativeConfig.__annotations__})
    cfg.section_dim = a.section_dim
    etu = (HierarchieModel(cfg) if a.bras != "temoin" else NativeModel(cfg)).to(a.device)
    etu.load_state_dict(ck["state"], strict=False)
    opt = torch.optim.AdamW(etu.parameters(), lr=a.lr, weight_decay=0.01)

    train, val = charger(a.train), charger(a.val)
    t0 = time.time()
    for pas in range(1, a.pas + 1):
        etu.train()
        x = decoupes(train, a.lot, a.nseg, a.seg, a.device, pas * a.lot + (a.graine - 1) * 10_000_019)
        etat = None
        pertes = []
        for j in range(a.nseg):
            ids = x[:, j * a.seg:(j + 1) * a.seg]
            cible = x[:, j * a.seg + 1:(j + 1) * a.seg + 1]
            with torch.no_grad():
                lp = prof(ids).logits
            if a.bras == "temoin":
                sortie = etu(ids)
            else:
                if a.bras == "controle" and etat is not None:
                    etat = etat.roll(1, dims=0)
                sortie = etu(ids, etat)
                etat = sortie["etat"].detach()
            ls = sortie["logits"]
            T = a.temperature
            kd = F.kl_div(F.log_softmax(ls / T, -1), F.softmax(lp / T, -1),
                          reduction="batchmean", log_target=False) * (T * T)
            ce = F.cross_entropy(ls.reshape(-1, 256), cible.reshape(-1))
            perte = a.alpha * kd + (1 - a.alpha) * ce
            for e in sortie["early"]:
                perte = perte + 0.1 * F.cross_entropy(e.reshape(-1, 256), cible.reshape(-1))
            for l in sortie["local"]:
                perte = perte + 0.05 * F.cross_entropy(l.reshape(-1, 256), cible.reshape(-1))
            pertes.append(perte)
        perte_moy = sum(pertes) / len(pertes)
        opt.zero_grad(); perte_moy.backward()
        torch.nn.utils.clip_grad_norm_(etu.parameters(), 1.0)
        opt.step()
        if pas % 250 == 0 or pas == 1:
            p = ppl(etu, val, a.nseg, a.seg, a.lot, a.device, a.bras, n_lots=2)
            print(f"pas {pas:5d} · perte {float(perte_moy):.4f} · PPL {p:.4f} · "
                  f"{time.time()-t0:.0f} s", flush=True)

    p_final = ppl(etu, val, a.nseg, a.seg, a.lot, a.device, a.bras, n_lots=8)
    etu.eval(); bons, n_ev = 0, 0
    with torch.no_grad():
        for k in range(4):
            x = decoupes(val, a.lot, a.nseg, a.seg, a.device, 10_000_000 + k * a.lot)
            etat = None
            for j in range(a.nseg):
                ids = x[:, j * a.seg:(j + 1) * a.seg]
                cible = x[:, j * a.seg + 1:(j + 1) * a.seg + 1]
                sortie = etu(ids) if a.bras == "temoin" else etu(ids, etat)
                if a.bras != "temoin":
                    etat = sortie["etat"].detach()
                if a.bras == "controle" and etat is not None:
                    etat = etat.roll(1, dims=0)
                bons += int((sortie["logits"].argmax(-1) == cible).sum())
                n_ev += cible.numel()
    torch.save({"config": cfg.__dict__, "state": etu.state_dict()}, a.sortie)
    drvm = a.drvm or (a.sortie + ".drvm")
    h = exporter_drvm(etu, drvm)
    res = {"bras": a.bras, "graine": a.graine, "pas": a.pas, "lot": a.lot,
           "nseg": a.nseg, "seg": a.seg, "lr": a.lr, "temperature": a.temperature,
           "alpha": a.alpha, "octets_vus": a.pas * a.lot * a.nseg * a.seg,
           "ppl_val": p_final, "precision_main": bons / max(1, n_ev),
           "parametres": etu.nb_parametres(), "duree_s": round(time.time() - t0, 1),
           "professeur": a.enseignant, "init": a.init, "drvm": drvm, "sha256_drvm": h}
    pathlib.Path(a.sortie + ".json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

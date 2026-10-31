#!/usr/bin/env python3
"""entrainer_section.py — ablation « état de section » pour N2.

Deux bras, mêmes octets vus, mêmes fenêtres, même budget :
  temoin     : NativeModel nu, segments de 128 enchaînés sans état ;
  hierarchie : HierarchieModel, un état de section (GRUCell) transporté d'un
               segment au suivant et injecté dans les activations ;
  controle   : bras hiérarchie avec l'état d'un AUTRE document (mélangé dans le
               lot) — si le gain survit, il vient des paramètres, pas du contenu.

Ségments : nseg × seg octets par échantillon. La perte est la moyenne des CE des
segments ; l'état est détaché à chaque segment (BPTT tronquée, à déclarer).
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

from tools.native_model import NativeConfig, NativeModel
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


def charger(chemin: str) -> torch.Tensor:
    b = pathlib.Path(chemin).read_bytes()
    if len(b) < 100_000:
        raise SystemExit(f"{chemin} : corpus trop court")
    return torch.tensor(list(b), dtype=torch.long)


def decoupes(data: torch.Tensor, n: int, nseg: int, seg: int, device: str, compteur: int):
    """n échantillons de nseg×seg octets, départs Van der Corput (déterministes)."""
    total = nseg * seg + 1  # un octet de plus : la cible du dernier segment
    departs = departs_vdc(compteur, n, len(data) - total - 2, total)
    i = torch.tensor(departs, dtype=torch.long)
    return torch.stack([data[j:j + total] for j in i]).to(device)


def passe(modele, x, nseg, seg, bras, etat=None):
    """Une passe avant segment par segment ; rend (perte, précision, état)."""
    b = x.shape[0]
    pertes, bons, n = [], 0, 0
    for k in range(nseg):
        seg_ids = x[:, k * seg:(k + 1) * seg]
        if bras == "temoin":
            sortie = modele(seg_ids)
        else:
            if bras == "controle" and etat is not None and b > 1:
                # état d'un autre document du lot : même forme, autre contenu.
                etat = etat.roll(1, dims=0)
            sortie = modele(seg_ids, etat)
            etat = sortie["etat"].detach()
        cible = x[:, k * seg + 1:(k + 1) * seg + 1]
        pertes.append(F.cross_entropy(sortie["logits"].reshape(-1, 256), cible.reshape(-1)))
        bons += int((sortie["logits"].argmax(-1) == cible).sum())
        n += cible.numel()
    return sum(pertes) / len(pertes), bons / max(1, n), etat


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/corpus_fr.txt")
    ap.add_argument("--bras", choices=("temoin", "hierarchie", "controle"), default="temoin")
    ap.add_argument("--pas", type=int, default=2500)
    ap.add_argument("--seg", type=int, default=128)
    ap.add_argument("--nseg", type=int, default=4)
    ap.add_argument("--lot", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--section-dim", type=int, default=224)
    ap.add_argument("--eval-tous", type=int, default=250)
    ap.add_argument("--sortie", default="/tmp/n2h/resultat.json")
    a = ap.parse_args()

    torch.manual_seed(a.graine)
    data = charger(a.corpus)
    n_val = max(10_000, len(data) // 20)
    train, val = data[:-n_val], data[-n_val:]

    cfg = NativeConfig()
    cfg.section_dim = a.section_dim
    cfg.hierarchie = a.bras != "temoin"
    modele = (HierarchieModel(cfg) if cfg.hierarchie else NativeModel(cfg)).to(a.device)
    opt = torch.optim.AdamW(modele.parameters(), lr=a.lr, weight_decay=0.01)
    t0 = time.time()
    historique = []
    for pas in range(1, a.pas + 1):
        modele.train()
        x = decoupes(train, a.lot, a.nseg, a.seg, a.device, pas * a.lot)
        # état neuf par lot : chaque échantillon est un document indépendant.
        perte, prec, _ = passe(modele, x, a.nseg, a.seg, a.bras, None)
        opt.zero_grad(); perte.backward()
        torch.nn.utils.clip_grad_norm_(modele.parameters(), 1.0)
        opt.step()
        if pas % a.eval_tous == 0 or pas == 1:
            modele.eval(); tot, nn_, bons = 0.0, 0, 0
            with torch.no_grad():
                for i in range(4):
                    xv = decoupes(val, 4, a.nseg, a.seg, a.device, 10_000_000 + i * 4)
                    p, pr, _ = passe(modele, xv, a.nseg, a.seg, a.bras, None)
                    tot += p.item() * (a.nseg * a.seg * 4); nn_ += a.nseg * a.seg * 4
                    bons += pr * (a.nseg * a.seg * 4)
            ppl = math.exp(tot / nn_)
            historique.append({"pas": pas, "perte": float(perte), "ppl": ppl,
                               "prec": bons / nn_, "t": round(time.time() - t0, 1)})
            print(f"pas {pas:5d} · perte {float(perte):.4f} · PPL val {ppl:.4f} · "
                  f"prec {bons/nn_:.4f} · {time.time()-t0:.0f} s", flush=True)

    final = historique[-1]
    res = {"bras": a.bras, "graine": a.graine, "pas": a.pas, "nseg": a.nseg, "seg": a.seg,
           "lot": a.lot, "octets_vus": a.pas * a.lot * a.nseg * a.seg,
           "parametres": modele.nb_parametres(), "ppl_val": final["ppl"],
           "prec_val": final["prec"], "duree_s": round(time.time() - t0, 1),
           "historique": historique, "corpus": a.corpus}
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "historique"},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

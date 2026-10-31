#!/usr/bin/env python3
"""eval_n2.py — PPL des points de contrôle N2, trois protocoles.

  standard     : 128 octets indépendants — comparable entre bras et à d'autres runs ;
  segmente     : 4×128 avec état transporté — le protocole de l'entraînement ;
  segmente-sans: 4×128 avec état remis à zéro à chaque segment — contrôle du précédent.

Usage : PYTHONPATH=. gpu-env/bin/python tools/eval_n2.py /tmp/n2-campagne/*-g*.pt
        (sans argument : les points de contrôle de /tmp/n2-campagne)
"""
import glob
import json
import math
import pathlib
import sys

import torch
import torch.nn.functional as F

from tools.native_model import NativeConfig, NativeModel
from tools.distiller_section import HierarchieModel, decoupes
from tools.vdc import departs_vdc

LOTS = 32          # 32 lots × 8 = 256 fenêtres par protocole


def charger(txt):
    return torch.tensor(list(pathlib.Path(txt).read_bytes()), dtype=torch.long)


def ppl_standard(m, data, seq=128, lot=8, device="cuda"):
    m.eval(); tot = 0.0; n = 0
    with torch.no_grad():
        for k in range(LOTS):
            i = torch.tensor(departs_vdc(40_000_000 + k * lot, lot, len(data) - seq - 1, seq),
                             dtype=torch.long)
            x = torch.stack([data[j:j + seq] for j in i]).to(device)
            y = torch.stack([data[j + 1:j + seq + 1] for j in i]).to(device)
            tot += float(F.cross_entropy(m(x)["logits"].reshape(-1, 256), y.reshape(-1),
                                         reduction="sum"))
            n += y.numel()
    return math.exp(tot / n)


def ppl_segmente(m, data, nseg=4, seg=128, lot=8, device="cuda", avec_etat=True):
    m.eval(); tot = 0.0; n = 0
    with torch.no_grad():
        for k in range(LOTS):
            x = decoupes(data, lot, nseg, seg, device, 60_000_000 + k * lot)
            etat = None
            for j in range(nseg):
                ids = x[:, j * seg:(j + 1) * seg]
                cible = x[:, j * seg + 1:(j + 1) * seg + 1]
                if avec_etat:
                    sortie = m(ids, etat)
                    etat = sortie["etat"].detach()
                else:
                    sortie = m(ids)
                tot += float(F.cross_entropy(sortie["logits"].reshape(-1, 256),
                                             cible.reshape(-1), reduction="sum"))
                n += cible.numel()
    return math.exp(tot / n)


def main():
    fichiers = sys.argv[1:] or sorted(glob.glob("/tmp/n2-campagne/*-g*.pt"))
    val = charger("data/corpus_fr_val.txt")
    sorties = []
    for f in sorted(fichiers):
        ck = torch.load(f, map_location="cpu", weights_only=False)
        cfg = NativeConfig(**{k: v for k, v in ck["config"].items()
                              if k in NativeConfig.__annotations__})
        cfg.section_dim = 224
        a_etat = "section_cell.weight_ih" in ck["state"]
        m = (HierarchieModel(cfg) if a_etat else NativeModel(cfg)).cuda()
        m.load_state_dict(ck["state"], strict=False)
        r = {"fichier": pathlib.Path(f).name,
             "bras": pathlib.Path(f).name.split("-g")[0],
             "graine": int(pathlib.Path(f).stem.split("-g")[1]),
             "ppl_standard": round(ppl_standard(m, val), 4),
             "ppl_segmente": round(ppl_segmente(m, val, avec_etat=a_etat), 4),
             "ppl_segmente_sans_etat": round(ppl_segmente(m, val, avec_etat=False), 4)}
        print(json.dumps(r, ensure_ascii=False), flush=True)
        sorties.append(r)
    pathlib.Path("/tmp/n2-campagne/evaluations-finales.json").write_text(
        json.dumps(sorties, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()

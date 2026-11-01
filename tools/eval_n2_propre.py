#!/usr/bin/env python3
"""eval_n2_propre.py — la porte honnête : PPL sur un corpus dédupliqué, et hors domaine.

Le corpus de `data/corpus_propre/` est construit par `tools/corpus_propre.py` : passages
répétés retirés, split par chunks contigus, **zéro fenêtre de validation dans
l'entraînement** (vérifié). Ce script évalue un point de contrôle :

  val / test        : in-domain, fenêtres tirées **dans** un chunk (jamais à cheval sur le
                      collage de deux chunks, qui est un artefact du split) ;
  litterature       : `data/corpus_fr_litterature.txt` (Verne, public domain) — jamais vu ;
  anglais           : `data/corpus_en.txt` (Wikipédia) — jamais vu ;
  wikitext2         : `data/wikitext2_test.txt` — jamais vu ;
  permute           : contrôle négatif, mêmes octets de validation, ordre détruit ;
  decomposition     : PPL des têtes précoces (après 2, 4, 6 blocs) et sans la boucle de
                      pensée — ce que chaque pièce porte, et ce que l'arrêt précoce coûte ;
  longueurs         : PPL à 129, 192, 256, 384, 512 octets — le verrou de longueur, mesuré
                      sur un texte propre.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python tools/eval_n2_propre.py <point.pt> \
      [--longueurs] [--decomposition] [--sortie work/n2h/eval.json]
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib

import torch
import torch.nn.functional as F

from tools.native_model import NativeConfig, NativeModel
from tools.vdc import departs_vdc, ordre_vdc

RACINE = pathlib.Path(__file__).resolve().parent.parent
CORPUS = RACINE / "data/corpus_propre"


def charger_bytes(chemin) -> torch.Tensor:
    return torch.tensor(list(pathlib.Path(chemin).read_bytes()), dtype=torch.long)


def charge(chemin, device="cuda"):
    ck = torch.load(chemin, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items()
                          if k in NativeConfig.__annotations__})
    m = NativeModel(cfg).to(device)
    m.load_state_dict(ck["state"], strict=False)
    m.eval()
    return m


def fenetres_dans_chunks(data, n, long, compteur, chunk, device="cuda"):
    """n fenêtres de `long` octets, chacune **dans** un chunk (jamais sur un collage)."""
    n_chunks = max(1, len(data) // chunk)
    out = []
    for k in range(n):
        c = departs_vdc(compteur + k, 1, n_chunks, long)[0]
        debut = c * chunk
        marge = min(chunk, len(data) - debut) - long - 1
        if marge <= 0:
            continue
        r = departs_vdc(compteur + 10_000_003 + k, 1, marge, long)[0]
        j = debut + r
        out.append(data[j:j + long])
    return torch.stack(out).to(device)


def ppl_sur_fenetres(m, x):
    with torch.no_grad():
        logits = m(x[:, :-1])["logits"]
        tot = float(F.cross_entropy(logits.reshape(-1, 256), x[:, 1:].reshape(-1),
                                    reduction="sum"))
    return math.exp(tot / x[:, 1:].numel())


def ppl_protocole(m, data, long, lot, chunk, compteur=0, n_lots=8, device="cuda"):
    tot, n = 0.0, 0
    with torch.no_grad():
        for k in range(n_lots):
            x = fenetres_dans_chunks(data, lot, long + 1, compteur + k * lot, chunk, device)
            logits = m(x[:, :-1])["logits"]
            tot += float(F.cross_entropy(logits.reshape(-1, 256), x[:, 1:].reshape(-1),
                                         reduction="sum"))
            n += x[:, 1:].numel()
    return math.exp(tot / n)


def decompose(m, data, chunk, device="cuda"):
    """PPL des têtes précoces et effet de la boucle de pensée."""
    x = fenetres_dans_chunks(data, 128, 129, 700, chunk, device)
    y = x[:, 1:]
    res = {}
    with torch.no_grad():
        s = m(x[:, :-1])
        res["complete"] = round(math.exp(float(F.cross_entropy(
            s["logits"].reshape(-1, 256), y.reshape(-1)))), 4)
        for i, e in enumerate(s["early"]):
            res[f"apres_{m.cfg.early_blocks[i] + 1}_blocs"] = round(math.exp(float(
                F.cross_entropy(e.reshape(-1, 256), y.reshape(-1)))), 4)
    ancien = m.cfg.thought_steps
    m.cfg.thought_steps = 0
    res["sans_pensee"] = round(ppl_sur_fenetres(m, x), 4)
    m.cfg.thought_steps = ancien
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("point")
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--longueurs", action="store_true")
    ap.add_argument("--decomposition", action="store_true")
    ap.add_argument("--sortie", default=None)
    ap.add_argument("--device", default="cuda")
    a = ap.parse_args()

    val = charger_bytes(CORPUS / "val.txt")
    test = charger_bytes(CORPUS / "test.txt")
    lit = charger_bytes(RACINE / "data/corpus_fr_litterature.txt")
    litt_propre = charger_bytes(RACINE / "data/corpus_litt_propre/val.txt")
    ang = charger_bytes(RACINE / "data/corpus_en.txt")
    wt = charger_bytes(RACINE / "data/wikitext2_test.txt")
    perm = val[torch.tensor(ordre_vdc(len(val)), dtype=torch.long)]

    m = charge(a.point, a.device)
    r = {"fichier": pathlib.Path(a.point).name, "params": m.nb_parametres(),
         "val": round(ppl_protocole(m, val, 128, 16, a.chunk, device=a.device), 4),
         "test": round(ppl_protocole(m, test, 128, 16, a.chunk, 5_000_000, device=a.device), 4),
         "litterature": round(ppl_protocole(m, lit, 128, 16, a.chunk, 1_000_000,
                                            device=a.device), 4),
         "litterature_propre": round(ppl_protocole(m, litt_propre, 128, 16, a.chunk, 3_000_000,
                                                   device=a.device), 4),
         "anglais": round(ppl_protocole(m, ang, 128, 16, a.chunk, 5_000_000,
                                        device=a.device), 4),
         "wikitext2": round(ppl_protocole(m, wt, 128, 16, a.chunk, 0, device=a.device), 4),
         "permute": round(ppl_protocole(m, perm, 128, 16, a.chunk, 900_000, device=a.device), 4)}
    if a.decomposition:
        r["decomposition"] = decompose(m, val, a.chunk, a.device)
    if a.longueurs:
        r["longueurs"] = {str(L): round(ppl_protocole(m, val, L, 16, a.chunk, device=a.device), 4)
                          for L in (129, 192, 256, 384, 512)}
    print(json.dumps(r, ensure_ascii=False), flush=True)
    if a.sortie:
        p = pathlib.Path(a.sortie)
        existant = json.loads(p.read_text()) if p.exists() else []
        existant.append(r)
        p.write_text(json.dumps(existant, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()

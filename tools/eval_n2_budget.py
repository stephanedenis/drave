#!/usr/bin/env python3
"""eval_n2_budget.py — N2.d : PPL des points de contrôle, validation décontaminée.

La campagne N2.d (`tools/distiller_budget.py`) a mesuré le budget, les données et le
curriculum. Deux choses ont été trouvées en l'évaluant, et ce script les rend
reproductibles :

1. **Le protocole historique est contaminé.** `data/corpus_fr_val.txt` est la queue de
   `data/corpus_fr.txt`, `corpus_fr_train.txt` sa tête : les positions sont disjointes,
   mais le corpus empile des documents qui se recopient. Un tiers des fenêtres du
   protocole (8 lots × 16 × 128, compteur 0) apparaissent **verbatim** dans
   l'entraînement — la PPL y est plus basse de 0,3 à 0,4.
2. **La grille de la campagne décale la PPL.** L'entraînement évalue sur des fenêtres de
   seq+1 (borne len−seq−2) ; le protocole historique échantillonne sur des fenêtres de
   seq (borne len−seq−1). L'écart vaut +0,0014 à 128 et +0,0102 à 129 : ce script
   rétablit la grille d'origine pour que les colonnes soient comparables à 2,7078
   (N2.19) et 2,6998 (N2.33).

Colonnes rendues, pour chaque point de contrôle :
  ppl_protocole    : 8 × 16 × 128 depuis le compteur 0 — le protocole publié ;
  ppl_129          : 8 × 15 × 129 — le protocole de N2.33 ;
  ppl_propres      : 128 fenêtres dont le contenu n'est **pas** verbatim dans train ;
  ppl_contaminees  : 128 fenêtres dont le contenu **est** verbatim dans train ;
  ppl_permute      : contrôle négatif, mêmes octets de validation, ordre détruit ;
  precision_main   : top-1 sur 128 fenêtres ;
  ppl_multi_val    : (bras multi seulement) validation du manifeste 4 sources.

Usage :
  python3 tools/eval_n2_budget.py --contamination        # les taux, sans modèle
  PYTHONPATH=. ~/gpu-env/bin/python tools/eval_n2_budget.py work/n2d/*.pt \
      [--grilles] [--sortie work/n2d/evaluations-finales.json]
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

import torch
import torch.nn.functional as F

from tools.native_model import NativeConfig, NativeModel
from tools.vdc import departs_vdc, ordre_vdc

RACINE = pathlib.Path(__file__).resolve().parent.parent
SEQ = 128


def _val() -> torch.Tensor:
    return torch.tensor(list((RACINE / "data/corpus_fr_val.txt").read_bytes()), dtype=torch.long)


def _train() -> bytes:
    return (RACINE / "data/corpus_fr_train.txt").read_bytes()


def verbatim(train: bytes, fenetre: torch.Tensor) -> bool:
    return train.find(bytes(fenetre.tolist())) >= 0


def echantillon(val, train, propre: bool, n: int = 128, maxi: int = 6000):
    """n fenêtres de 129 octets en ordre de van der Corput, propres ou contaminées."""
    gardees = []
    for k in range(maxi):
        j = departs_vdc(k, 1, len(val) - SEQ - 1, SEQ)[0]
        w = val[j:j + SEQ + 1]
        if verbatim(train, w) != propre:
            gardees.append(w)
            if len(gardees) == n:
                return gardees
    raise SystemExit(f"pas assez de fenêtres ({len(gardees)})")


def ppl_fenetres(m, fenetres, device="cuda"):
    x = torch.stack(fenetres).to(device)
    with torch.no_grad():
        logits = m(x[:, :-1])["logits"]
        tot = float(F.cross_entropy(logits.reshape(-1, 256), x[:, 1:].reshape(-1),
                                    reduction="sum"))
    return math.exp(tot / x[:, 1:].numel())


def ppl_protocole(m, val, seq, lot, compteur=0, n_lots=8, device="cuda"):
    tot, n = 0.0, 0
    with torch.no_grad():
        for k in range(n_lots):
            i = torch.tensor(departs_vdc(compteur + k * lot, lot, len(val) - seq - 1, seq),
                             dtype=torch.long)
            x = torch.stack([val[j:j + seq + 1] for j in i]).to(device)
            logits = m(x[:, :-1])["logits"]
            tot += float(F.cross_entropy(logits.reshape(-1, 256), x[:, 1:].reshape(-1),
                                         reduction="sum"))
            n += x[:, 1:].numel()
    return math.exp(tot / n)


def charge(chemin: str, device="cuda"):
    ck = torch.load(chemin, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items()
                          if k in NativeConfig.__annotations__})
    m = NativeModel(cfg).to(device)
    m.load_state_dict(ck["state"], strict=False)
    m.eval()
    return m


def contamination(val, train, n_echantillon=300, graine=0):
    """Taux de fenêtres de validation présentes verbatim dans l'entraînement."""
    import random
    rng = random.Random(graine)
    ech = [val[rng.randrange(0, len(val) - SEQ - 1):][:SEQ + 1] for _ in range(n_echantillon)]
    taux_ech = sum(verbatim(train, w) for w in ech) / len(ech)
    protocole = []
    for k in range(8):
        for j in departs_vdc(k * 16, 16, len(val) - SEQ - 1, SEQ):
            protocole.append(val[j:j + SEQ + 1])
    touches = sum(verbatim(train, w) for w in protocole)
    rng2 = random.Random(graine + 1)
    ech_train = [train[rng2.randrange(0, len(train) - SEQ - 1):][:SEQ + 1]
                 for _ in range(200)]
    dupliques = sum(train.count(w) > 1 for w in ech_train)
    return {"echantillon_validation": n_echantillon, "taux_validation": round(taux_ech, 4),
            "protocole_fenetres": len(protocole), "protocole_contaminees": touches,
            "taux_protocole": round(touches / len(protocole), 4),
            "echantillon_train": 200, "train_duplique": dupliques,
            "taux_train_duplique": round(dupliques / 200, 4)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("points", nargs="*")
    ap.add_argument("--contamination", action="store_true")
    ap.add_argument("--grilles", action="store_true",
                    help="PPL sur quatre compteurs et deux tailles de lot (robustesse)")
    ap.add_argument("--manifeste", default="reports/native-corpus-multi.json")
    ap.add_argument("--sortie", default=None)
    ap.add_argument("--device", default="cuda")
    a = ap.parse_args()

    val, train = _val(), _train()
    if a.contamination:
        print(json.dumps(contamination(val, train), ensure_ascii=False))
        return
    if not a.points:
        raise SystemExit("aucun point de contrôle")

    propres, contaminees = echantillon(val, train, True), echantillon(val, train, False)
    perm = val[torch.tensor(ordre_vdc(len(val)), dtype=torch.long)]
    multi = None
    resultats = []
    for f in a.points:
        m = charge(f, a.device)
        r = {"fichier": pathlib.Path(f).name, "params": m.nb_parametres(),
             "ppl_protocole": round(ppl_protocole(m, val, 128, 16, device=a.device), 4),
             "ppl_129": round(ppl_protocole(m, val, 129, 15, device=a.device), 4),
             "ppl_propres": round(ppl_fenetres(m, propres, a.device), 4),
             "ppl_contaminees": round(ppl_fenetres(m, contaminees, a.device), 4),
             "ppl_permute": round(ppl_fenetres(
                 m, [perm[j:j + SEQ + 1] for j in
                     departs_vdc(0, 16, len(perm) - SEQ - 1, SEQ)], a.device), 4)}
        bons, n_ev = 0, 0
        with torch.no_grad():
            for k in range(8):
                i = torch.tensor(departs_vdc(80_000_000 + k * 16, 16, len(val) - 129, 128),
                                 dtype=torch.long)
                x = torch.stack([val[j:j + 129] for j in i]).to(a.device)
                s = m(x[:, :-1])
                bons += int((s["logits"].argmax(-1) == x[:, 1:]).sum())
                n_ev += x[:, 1:].numel()
        r["precision_main"] = round(bons / max(1, n_ev), 4)
        if a.grilles:
            r["grilles"] = {f"{c}/{lot}": round(ppl_protocole(m, val, 128, lot, c, device=a.device), 4)
                            for c in (0, 1_000_003, 2_000_009, 3_000_029) for lot in (16, 8)}
        if "-multi" in r["fichier"] or "-equilibre" in r["fichier"]:
            if multi is None:
                from tools.distiller_budget import CorpusMulti
                multi = CorpusMulti(a.manifeste)
            tot, n = 0.0, 0
            with torch.no_grad():
                for k in range(8):
                    idx = departs_vdc(90_000_000 + k * 16, 16, len(multi.val), 128)
                    x = torch.tensor([multi._fenetre(*multi.val[i], 129) for i in idx],
                                     dtype=torch.long).to(a.device)
                    logits = m(x[:, :-1])["logits"]
                    tot += float(F.cross_entropy(logits.reshape(-1, 256), x[:, 1:].reshape(-1),
                                                 reduction="sum"))
                    n += x[:, 1:].numel()
            r["ppl_multi_val"] = round(math.exp(tot / n), 4)
        print(json.dumps(r, ensure_ascii=False), flush=True)
        resultats.append(r)
    if a.sortie:
        pathlib.Path(a.sortie).write_text(json.dumps(resultats, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()

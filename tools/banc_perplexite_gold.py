#!/usr/bin/env python3
"""banc_perplexite_gold.py — la PPL du natif sur le gold linguistique.

POURQUOI. La PPL 2,40 du `drave-n0` a été mesurée sur sa **validation** (le wiki
même distribution). Le gold linguistique (612 phrases, 452 réelles) est un autre
domaine : le natif le modélise-t-il, ou n'a-t-il appris que le wiki ? La réponse
informe le plan (la donnée du palier 1).

MESURE. Pour chaque phrase du gold (par langue), la somme des log-probas du
prochain octet sous le modèle ; la **PPL** = exp(la moyenne par octet) ; le
**bits/octet** = la moyenne × log2(e). Le contrôle : le même calcul sur le
`val.txt` du corpus (la référence 2,40).

Usage (torch) :
  python3 tools/banc_perplexite_gold.py --modele work/n2ac/mix1024-60k.pt \
      --sortie reports/banc-perplexite-gold.json
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

import torch
import torch.nn.functional as F

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from tools.native_model import NativeConfig, NativeModel  # noqa: E402
from tools.tests.linguistique.evaluer_gold import charger  # noqa: E402
from tools.canal_structure import canal as canal_de  # noqa: E402


def charger_modele(chemin: str):
    ck = torch.load(chemin, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items() if k in NativeConfig.__annotations__})
    m = NativeModel(cfg)
    m.load_state_dict(ck["state"])
    m.eval()
    return m, cfg


@torch.no_grad()
def ppl_texte(modele, cfg, texte: str, fenetre: int) -> tuple[float, int]:
    ids = list(texte.encode("utf-8"))
    if len(ids) < 2:
        return (float("nan"), 0)
    ids = ids[-(fenetre + 1):]
    x = torch.tensor([ids[:-1]], dtype=torch.long)
    cible = torch.tensor(ids[1:], dtype=torch.long)
    classes = list(canal_de(texte))  # une classe par octet, alignée sur `ids`
    canal = torch.tensor([classes[: len(ids) - 1]])
    logits = modele(x, canal=canal)["logits"][0]
    perte = F.cross_entropy(logits, cible, reduction="sum").item()
    return (perte, len(ids) - 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", required=True)
    ap.add_argument("--sortie", default="reports/banc-perplexite-gold.json")
    ap.add_argument("--val", default="", help="le val.txt pour la référence")
    ap.add_argument("--limite", type=int, default=0)
    a = ap.parse_args()
    modele, cfg = charger_modele(a.modele)
    fenetre = min(cfg.window, cfg.max_pos) - 1
    phrases = charger()
    if a.limite:
        phrases = phrases[: a.limite]
    par_langue: dict[str, list[float]] = {}
    for p in phrases:
        perte, n = ppl_texte(modele, cfg, p["texte"], fenetre)
        if n:
            par_langue.setdefault(p.get("langue") or "und", []).append(perte / n)
    resultat = {"modele": a.modele, "phrases": len(phrases), "fenetre": fenetre,
                "par_langue": {}, "global": {}}
    total = []
    for langue, pertes in sorted(par_langue.items()):
        moy = sum(pertes) / len(pertes)
        resultat["par_langue"][langue] = {"n": len(pertes), "ppl": round(math.exp(moy), 3),
                                          "bits_octet": round(moy / math.log(2), 3)}
        total += pertes
    if total:
        moy = sum(total) / len(total)
        resultat["global"] = {"n": len(total), "ppl": round(math.exp(moy), 3),
                              "bits_octet": round(moy / math.log(2), 3)}
    if a.val and pathlib.Path(a.val).exists():
        texte = pathlib.Path(a.val).read_text(encoding="utf-8", errors="replace")[:4_096]
        perte, n = ppl_texte(modele, cfg, texte, fenetre)
        resultat["reference_val"] = {"octets": n, "ppl": round(math.exp(perte / n), 3)}
    pathlib.Path(a.sortie).write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                                      encoding="utf-8")
    print(json.dumps(resultat, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

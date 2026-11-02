#!/usr/bin/env python3
"""eval_200k.py — les cinq PPL du run long, la courbe de longueur et le contrôle par permutation.

Protocole identique à N2.ac (rapport-n2-melange) : canal fourni à l'évaluation, fenêtres
tirées par Van der Corput dans des chunks de 8192 octets, 8 lots de 16 fenêtres.
En plus :
  - la **courbe de longueur** 128 / 256 / 512 sur les deux validations appariées ;
  - le **contrôle négatif par permutation** : mêmes octets, ordre détruit (octets *et*
    canal permutés par la même permutation), sur 4 Mo de la validation française.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/eval_200k.py <point.pt> [--sortie x.json]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "work/n2j")

import torch  # noqa: E402

from tools.eval_n2_propre import charge, charger_bytes, ordre_vdc  # noqa: E402
from tools.canal_structure import canal as canal_de  # noqa: E402
import evalue_canal as ec  # noqa: E402


def canal_bytes(chemin: str) -> torch.Tensor:
    return torch.tensor(list(pathlib.Path(chemin).read_bytes()), dtype=torch.long)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("point")
    ap.add_argument("--sortie", default=None)
    a = ap.parse_args()

    m = charge(a.point)
    res = {"fichier": pathlib.Path(a.point).name, "params": m.nb_parametres()}

    # 1. Les deux validations appariées, avec le canal, à trois longueurs.
    for nom, d in (("val_fr", "data/wiki_fr/propre"), ("val_big", "data/wiki_big/propre")):
        val = charger_bytes(f"{d}/val.txt")
        ct = canal_bytes(f"{d}/val.canal")
        for L in (128, 256, 512):
            res[f"{nom}_L{L}"] = ec.ppl(m, val, ct, L, avec_canal=True)
        # 2. Contrôle négatif : mêmes octets, ordre détruit (octets et canal ensemble).
        n = 4_000_000
        perm = torch.tensor(ordre_vdc(n), dtype=torch.long)
        res[f"{nom}_permute"] = ec.ppl(m, val[:n][perm], ct[:n][perm], 128, avec_canal=True)
        del val, ct
        torch.cuda.empty_cache()

    # 3. Le corpus propre du dépôt (3,6 Mo) : la distribution de la « porte 2,5 », ici en
    #    transfert (le run n'a jamais vu ce texte) — ce n'est PAS la porte, c'est un transfert.
    propre = pathlib.Path("data/corpus_propre/val.txt").read_text(encoding="utf-8",
                                                                  errors="replace")
    data = charger_bytes("data/corpus_propre/val.txt")
    ct = torch.tensor(list(canal_de(propre)), dtype=torch.long)
    res["corpus_propre_val"] = ec.ppl(m, data, ct, 128, avec_canal=True)
    del data, ct
    torch.cuda.empty_cache()

    # 4. Hors domaine, canal recalculé sur le texte.
    for nom, chemin in (("litterature", "data/corpus_fr_litterature.txt"),
                        ("anglais", "data/corpus_en.txt"),
                        ("wikitext2", "data/wikitext2_test.txt")):
        texte = pathlib.Path(chemin).read_text(encoding="utf-8", errors="replace")
        data = charger_bytes(chemin)
        ct = torch.tensor(list(canal_de(texte)), dtype=torch.long)
        res[nom] = ec.ppl(m, data, ct, 128, avec_canal=True)
        del data, ct
        torch.cuda.empty_cache()

    print(json.dumps(res, ensure_ascii=False, indent=1), flush=True)
    if a.sortie:
        p = pathlib.Path(a.sortie)
        p.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

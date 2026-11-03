#!/usr/bin/env python3
"""cout_fenetre.py — ms par octet, à la longueur native de chaque fenêtre.

La PPL ne montre pas le prix : l'attention coûte O(L²) par couche, donc doubler la fenêtre
quadruple le travail d'attention par octet. Ce banc mesure le **temps mural** d'une passe avant
(batch 8, longueur = fenêtre du modèle), après échauffement, GPU partagé — les valeurs absolues
sont donc pessimistes, les **rapports** sont l'information.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/cout_fenetre.py [--passes 10]
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, ".")
import torch
from work.n2ac.rope_model import charge_rope

MODELES = [("fenêtre 256", "work/n2ac/rope-20k.pt", 256),
           ("fenêtre 512", "work/n2ac/rope512-5k.pt", 512),
           ("fenêtre 1 024", "work/n2ac/rope1024-20k.pt", 1024),
           ("fenêtre 2 048", "work/n2ac/rope2048-1.25k.pt", 2048)]

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--passes", type=int, default=10)
    a = ap.parse_args()
    res = {}
    for nom, chemin, L in MODELES:
        if not pathlib.Path(chemin).exists():
            continue
        m = charge_rope(chemin)
        x = torch.randint(0, 256, (8, L), device="cuda")
        c = torch.randint(0, 6, (8, L), device="cuda")
        with torch.no_grad():
            for _ in range(3):
                m(x, canal=c)
            torch.cuda.synchronize()
            t0 = time.time()
            for _ in range(a.passes):
                m(x, canal=c)
            torch.cuda.synchronize()
        dt = (time.time() - t0) / a.passes
        res[nom] = {"L": L, "ms_passe": round(dt * 1e3, 2),
                    "ms_par_octet_lot8": round(dt * 1e3 / (8 * L), 5),
                    "octets_par_s": int(8 * L / dt)}
        print(f"  {nom:14s} L={L:5d} · {res[nom]['ms_passe']:8.2f} ms/passe · "
              f"{res[nom]['octets_par_s']:9d} octets/s", flush=True)
        del m
        torch.cuda.empty_cache()
    print(json.dumps(res, ensure_ascii=False))

if __name__ == "__main__":
    main()

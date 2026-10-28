#!/usr/bin/env python3
"""corpus_natif.py — N2.1 : fenêtres d'entraînement pour `drave-n0`.

Découpe un corpus d'octets en fenêtres de `fenetre` octets, avec un pas fixe,
puis un split train/validation déterministe. Écrit un manifeste JSON (offsets)
et, si demandé, un fichier binaire concaténé — les corpus de `data/` sont
ignorés par git.
"""
from __future__ import annotations

import argparse
import json
import pathlib
from tools.vdc import ordre_vdc


def construire_multi(sources: list[str], fenetre: int = 128, pas: int = 64,
                     max_fenetres: int = 50_000, val: int = 5_000,
                     graine: int = 0) -> dict:
    """Fenêtres sur plusieurs sources, sans concaténer les fichiers."""
    par_source = []
    for src in sources:
        b = pathlib.Path(src).read_bytes()
        offsets = list(range(0, max(0, len(b) - fenetre + 1), pas))
        par_source.append({"source": src, "octets": len(b), "fenetres": len(offsets)})
    # Répartition équilibrée, plafonnée à max_fenetres.
    total = sum(x["fenetres"] for x in par_source)
    quotas = {x["source"]: max(1, max_fenetres * x["fenetres"] // total) for x in par_source}
    offsets = []
    for src, q in quotas.items():
        b = pathlib.Path(src).read_bytes()
        offs = list(range(0, max(0, len(b) - fenetre + 1), pas))[:q]
        for o in offs:
            offsets.append({"source": src, "offset": o})
    ordre = ordre_vdc(len(offsets))
    offsets = [offsets[i] for i in ordre][:max_fenetres]
    n_val = min(val, len(offsets) // 2)
    return {"sources": par_source, "fenetre": fenetre, "pas": pas,
            "ordre": "van_der_corput", "fenetres": len(offsets),
            "train": len(offsets) - n_val, "val": n_val,
            "graine": graine, "premier_offset": offsets[0] if offsets else None,
            "licence": "sources locales — licences à vérifier avant diffusion",
            "note": "manifeste d'offsets multi-sources ; les corpus ne sont pas versionnés"}


def construire(source: str, fenetre: int = 128, pas: int = 64,
               max_fenetres: int = 50_000, val: int = 5_000,
               graine: int = 0) -> dict:
    b = pathlib.Path(source).read_bytes()
    if fenetre < 2 or pas < 1:
        raise ValueError("fenetre >= 2 et pas >= 1")
    if len(b) < fenetre:
        raise ValueError("corpus trop court")
    offsets = list(range(0, len(b) - fenetre + 1, pas))[:max_fenetres]
    ordre = ordre_vdc(len(offsets))
    offsets = [offsets[i] for i in ordre]
    n_val = min(val, len(offsets) // 2)
    return {
        "source": source, "octets": len(b), "fenetre": fenetre, "pas": pas,
        "ordre": "van_der_corput", "fenetres": len(offsets),
        "train": len(offsets) - n_val, "val": n_val,
        "graine": graine, "premier_offset": offsets[0] if offsets else None,
        "licence": "source locale data/corpus_fr.txt — licence à vérifier avant diffusion",
        "note": "manifeste d'offsets ; le corpus n'est pas versionné",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="data/corpus_fr.txt")
    ap.add_argument("--sources", nargs="+", default=None)
    ap.add_argument("--fenetre", type=int, default=128)
    ap.add_argument("--pas", type=int, default=64)
    ap.add_argument("--max", type=int, default=50_000)
    ap.add_argument("--val", type=int, default=5_000)
    ap.add_argument("--graine", type=int, default=0)
    ap.add_argument("--sortie", default="reports/native-corpus.json")
    a = ap.parse_args()
    if a.sources:
        d = construire_multi(a.sources, a.fenetre, a.pas, a.max, a.val, a.graine)
    else:
        d = construire(a.source, a.fenetre, a.pas, a.max, a.val, a.graine)
    pathlib.Path(a.sortie).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    cles = ("fenetres","train","val","fenetre","pas")
    print(json.dumps({k: d[k] for k in cles} | ({"sources": d["sources"]} if "sources" in d else {"source": d["source"], "octets": d["octets"]}),
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

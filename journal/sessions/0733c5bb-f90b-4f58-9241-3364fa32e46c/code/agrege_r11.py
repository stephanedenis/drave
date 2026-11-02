#!/usr/bin/env python3
"""agrege_r11.py — assemble `reports/n2-r11.json` depuis les sorties brutes de `work/n2ac/`.

Rien n'est recopié à la main : chaque valeur vient d'un fichier produit par une commande
nommée dans la fiche. Un fichier absent est simplement omis (le banc peut être partiel).

Usage :
  python3 work/n2ac/agrege_r11.py [--sortie reports/n2-r11.json]
"""
from __future__ import annotations

import argparse
import json
import pathlib

WORK = pathlib.Path("work/n2ac")

SOURCES = {
    "courbe_rope_graine1": "courbe-rope.json",
    "courbe_absolu": "courbe-absolu.json",
    "courbe_rope_graine2": "courbe-rope-g2.json",
    "courbe_absolu_pos1152": "courbe-absolu-pos1152.json",
    "courbe_rope512_5k": "courbe-rope512-5k.json",
    "courbe_rope512_20k": "courbe-rope512-20k.json",
    "meme_texte_rope": "queue-rope.json",
    "meme_texte_absolu": "queue-absolu.json",
    "meme_texte_rope512": "queue-rope512.json",
    "miroir_copie_rope": "miroir-rope.json",
    "entrainement_graine1": "rope-20k.pt.json",
    "entrainement_graine2": "rope-20k-g2.pt.json",
    "entrainement_rope512_5k": "rope512-5k.pt.json",
    "entrainement_rope512_20k": "rope512-20k.pt.json",
    "zero_absolu": "zero-absolu.pt.json",
    "zero_rope": "zero-rope.pt.json",
    "courbe_zero_absolu": "courbe-zero-absolu.json",
    "courbe_zero_rope": "courbe-zero-rope.json",
    "courbe_zero_rope_40k": "courbe-zero-rope-40k.json",
    "meme_texte_zero_rope_40k": "queue-zero-rope-40k.json",
    "entrainement_zero_absolu": "zero-absolu.pt.json",
    "entrainement_zero_rope": "zero-rope.pt.json",
    "entrainement_zero_rope_40k": "zero-rope-40k.pt.json",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="reports/n2-r11.json")
    a = ap.parse_args()
    out = {}
    for cle, nom in SOURCES.items():
        p = WORK / nom
        if p.exists():
            out[cle] = json.loads(p.read_text(encoding="utf-8"))
    out["dispositif"] = {
        "modele": "drave-n0 / RoPE (work.n2ac.rope_model.NativeModelRoPE)",
        "recette": "34,3 M (384/512), 20 000 pas × 8 × 128, lr 3e-4, graine 1, canal, "
                   "init work/n2j/base-wiki-45m.pt",
        "corpus": "data/wiki_fr/propre/train.txt (186 Mo), canal data/wiki_fr/propre/train.canal",
        "evaluation": "work/n2j/evalue_canal.py : canal fourni, fenêtres Van der Corput, "
                      "chunks 8192, 8 lots × 16 fenêtres",
        "controle_absolu": "work/n2j/base-34m-canal.pt (même recette, positions absolues)",
        "controles": [
            "même texte à contexte 256/512/1000 (eval_fenetre)",
            "table de positions : lignes 512+ non entraînées (norme)",
            "absolu avec positions 0–1279 entraînées (absolu-pos1152)",
            "miroir de copie à distance (miroir_copie) — muet, voir la fiche",
        ],
    }
    p = pathlib.Path(a.sortie)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  {p} · {len(out) - 1} source(s)")


if __name__ == "__main__":
    main()

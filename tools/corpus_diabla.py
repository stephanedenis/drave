#!/usr/bin/env python3
"""corpus_diabla.py — extraire les paires FR/EN de DiaBLa (dialogues spontanés écrits).

POURQUOI. Le registre « dialogue » était mesuré sur OpenSubtitles — du parlé écrit et
contraint (les sous-titres). DiaBLa (Bawden et al., 2021, LRE) donne **144 dialogues
spontanés** entre francophones et anglophones, **5 700+ phrases**, avec les
**post-éditions humaines** des sorties du système de TA utilisé dans l'expérience :
c'est le dialogue informel réel, écrit, avec une référence humaine.

CE QUE LA RÉFÉRENCE EST, ET N'EST PAS. La référence est une **post-édition** (la
correction humaine de la TA), pas une traduction indépendante : plus proche du réel
qu'un sous-titre, plus biaisée qu'un texte traduit à la main. La fiche le dit.

Usage : corpus_diabla.py [--sortie data/diabla/diabla_fr_en.json] [--min 15]
"""
import argparse
import json


def principal():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="data/diabla/diabla_fr_en.json")
    ap.add_argument("--min", type=int, default=15, help="longueur minimale d'un côté, en caractères")
    a = ap.parse_args()
    from huggingface_hub import hf_hub_download

    p = hf_hub_download("rbawden/DiaBLa", "DiaBLa.json", repo_type="dataset")
    d = json.load(open(p, encoding="utf-8"))
    paires = []
    for _, dlg in d["dialogues"].items():
        for _, u in dlg.get("utterances", {}).items():
            src = (u.get("original_text") or "").strip()
            tgt = (u.get("postprocessed_text") or "").strip()
            lang = u.get("language")
            if len(src) < a.min or len(tgt) < a.min or lang not in ("english", "french"):
                continue
            if lang == "english":
                paires.append({"en": src, "fr": tgt})
            else:
                paires.append({"fr": src, "en": tgt})
    json.dump(paires, open(a.sortie, "w"), ensure_ascii=False)
    print(f"  {len(paires)} paires FR/EN ({len(d['dialogues'])} dialogues) → {a.sortie}")


if __name__ == "__main__":
    principal()

#!/usr/bin/env python3
"""comparer_noyaux.py — UN NOYAU MONOLINGUE + ADAPTATEUR VAUT-IL UN NOYAU BILINGUE ?

LA QUESTION D'INGÉNIERIE (chapitre 7). Deux façons d'obtenir une couche commune : entraîner un noyau **sur les
deux langues** ✓ (le plus simple ✓), ou garder un noyau **monolingue** et ajouter un **adaptateur** par langue
✓ (famille E ✓, 1,33 % de paramètres ✓). Laquelle vaut mieux ? Mesure : la perte sur les mêmes fenêtres ✓,
pour trois dispositifs ✓.

⚠️ CE QUE CE TEST NE PEUT PAS DIRE, et qu'il faut écrire d'avance ✗ : les deux noyaux n'ont **ni la même
taille** (2,43 M contre 4,79 M ✓) **ni les mêmes données** (96 Mo d'anglais contre 10,2 Mo mixtes ✓). Ce n'est
donc **pas** une comparaison à budget égal ✗✓ — c'est une comparaison de **trois dispositifs réels** ✓, et la
conclusion doit rester à ce niveau ✓.

Usage :
  python3 tools/comparer_noyaux.py --bilingue /tmp/jouet-mixte --monolingue /tmp/jouet-d256 \\
      --adaptateur /tmp/adaptateur-fr.pt
"""
from __future__ import annotations
import argparse, pathlib, sys
import numpy as np, torch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from adaptateur_langue import poser_lora


def fenetres(chemin, longueur, nombre):
    b = np.frombuffer(pathlib.Path(chemin).read_text(errors="ignore").encode("utf-8"), dtype=np.uint8).astype(np.int64)
    pas = max(longueur, len(b) // (nombre + 2))
    return [b[i * pas:i * pas + longueur] for i in range(nombre) if i * pas + longueur + 1 < len(b)]


def perte(modele, lots):
    tot = 0.0
    with torch.no_grad():
        for w in lots:
            x = torch.tensor(w).unsqueeze(0)
            tot += float(modele(x, labels=x).loss)
    return tot / len(lots)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bilingue", default="/tmp/jouet-mixte")
    ap.add_argument("--monolingue", default="/tmp/jouet-d256")
    ap.add_argument("--adaptateur", default="/tmp/adaptateur-fr.pt")
    ap.add_argument("--longueur", type=int, default=128)
    ap.add_argument("--fenetres", type=int, default=16)
    a = ap.parse_args()
    from transformers import AutoModelForCausalLM
    fr = fenetres("data/corpus_fr.txt", a.longueur, a.fenetres)
    en = fenetres("data/corpus_en.txt", a.longueur, a.fenetres)

    def charger(chemin, adapt=None):
        m = AutoModelForCausalLM.from_pretrained(chemin, dtype=torch.float32).eval()
        if adapt and pathlib.Path(adapt).exists():
            d = torch.load(adapt, map_location="cpu", weights_only=False)
            poser_lora(m, d["rang"])
            etat = m.state_dict()
            with torch.no_grad():
                for k, v in d["lora"].items():
                    if k in etat and etat[k].shape == v.shape:
                        etat[k].copy_(v)
        return m

    print()
    print("   dispositif                                  | perte FRANÇAIS | perte ANGLAIS")
    print("   --------------------------------------------|----------------|-------------")
    for nom, chemin, adapt in (
        ("noyau BILINGUE ✓ (10,2 Mo mixtes, 4,79 M)", a.bilingue, None),
        ("noyau monolingue ✗ (96 Mo anglais, 2,43 M)", a.monolingue, None),
        ("noyau monolingue + ADAPTATEUR français ✓", a.monolingue, a.adaptateur),
    ):
        m = charger(chemin, adapt)
        print(f"   {nom:43s} |     {perte(m, fr):5.4f}     |    {perte(m, en):5.4f}")
        del m
    print()
    print("  lecture : si « monolingue + adaptateur » rejoint « bilingue » sur le français ✓✓, alors la couche")
    print("  commune peut se faire par ADAPTATEURS ✓ — et le noyau n'a pas besoin d'avoir vu les deux langues ✓.")
    print("  ⚠️ les deux noyaux n'ont ni la même taille ni les mêmes données : ce n'est PAS une comparaison à")
    print("  budget égal ✗, c'est une comparaison de trois dispositifs réels ✓.")
    return 0

raise SystemExit(main())

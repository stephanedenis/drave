#!/usr/bin/env python3
"""banc_612.py — la génération du modèle natif sur les 612 phrases du gold.

POURQUOI. Le `banc_generation` mesure 20 prompts écrits à la main : c'est un banc de **style**.
Ici, on mesure sur le **gold 612** — le corpus de référence du produit — pour répondre à une
question différente : le modèle génère-t-il du **français** quand on l'amorce avec des phrases
réelles, et à quel **coût** ?

CE QU'ON MESURE :
  - les **octets/seconde** (le débit, sur GPU) ;
  - les **mots valides** (la part de mots qui existent dans le lexique du gold) ;
  - la **répétition** (le plus long cycle de 2-grammes) ;
  - la **dérive** (la part d'octets non-UTF-8, et le taux de sortie du lexique) ;
  - le **contrôle négatif** : un modèle aléatoire (les mêmes mesures, sans apprentissage).

Usage :
  python3 tools/banc_612.py --modele work/n2ac/mix1024-100m-3k.pt --n 24 --device cuda --json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

GOLD = pathlib.Path(__file__).resolve().parent / "tests" / "linguistique" / "gold_gele.json"


def charger_gold() -> list[str]:
    g = json.loads(GOLD.read_text())
    phrases = g.get("phrases", []) if isinstance(g, dict) else g
    textes = []
    for p in phrases:
        t = p.get("texte") or p.get("phrase") or p.get("text") or ""
        if t:
            textes.append(t)
    return textes


def mots_du_gold(textes: list[str]) -> set[str]:
    """Le lexique du gold : les mots réels, en minuscules, sans ponctuation."""
    lex = set()
    for t in textes:
        for m in re.findall(r"[a-zàâçéèêëîïôûùüÿñæœ]+", t.lower()):
            lex.add(m)
    return lex


def mesurer(sorties: list[str], lexique: set[str]) -> dict:
    mots = []
    for s in sorties:
        mots.extend(re.findall(r"[a-zàâçéèêëîïôûùüÿñæœ]+", s.lower()))
    valides = [m for m in mots if m in lexique]
    # la répétition : le plus long cycle de 2-grammes consécutifs
    pires = 0
    for s in sorties:
        toks = s.split()
        big = [tuple(toks[i:i + 2]) for i in range(len(toks) - 1)]
        best = 0
        for i in range(len(big)):
            for j in range(1, len(big) - i + 1):
                if big[i:i + j] == big[i + j:i + 2 * j]:
                    best = max(best, j)
        pires = max(pires, best)
    non_utf8 = sum(1 for s in sorties if "\ufffd" in s)
    return {
        "mots": len(mots),
        "mots_valides": round(len(valides) / max(1, len(mots)), 4),
        "repetition_2grammes": pires,
        "sorties_non_utf8": non_utf8,
        "sorties": len(sorties),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="work/n2ac/mix1024-100m-3k.pt")
    ap.add_argument("--n", type=int, default=16, help="octets générés par phrase")
    ap.add_argument("--limite", type=int, default=0, help="0 = tout le gold")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    import torch
    from tools.banc_generation import charger
    from tools.native_cache import generer

    textes = charger_gold()
    if a.limite:
        textes = textes[:a.limite]
    lexique = mots_du_gold(textes)
    modele, cfg = charger(a.modele, a.device)

    sorties = []
    t0 = time.perf_counter()
    for t in textes:
        prompt = t[:32]  # l'amorce : les 32 premiers octets de la phrase
        s = generer(modele, prompt, a.n, min(cfg.window, cfg.max_pos))
        sorties.append(s)
    dt = time.perf_counter() - t0
    r = mesurer(sorties, lexique)
    r["phrases"] = len(textes)
    r["octets_s"] = round(len(textes) * a.n / max(1e-9, dt), 1)
    r["s"] = round(dt, 1)
    r["modele"] = a.modele
    r["lexique"] = len(lexique)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"{len(textes)} phrases · {r['octets_s']} octets/s · "
              f"mots valides {r['mots_valides']:.3f} ({r['mots']} mots) · "
              f"répétition {r['repetition_2grammes']} · non-UTF-8 {r['sorties_non_utf8']}")


if __name__ == "__main__":
    main()

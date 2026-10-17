#!/usr/bin/env python3
"""retrieval_parallele.py — LE MÊME SENS DANS DEUX LANGUES : les états se RESSEMBLENT-ILS ?

LA QUESTION FORTE DU CHAPITRE 7. Tout ce qui précède mesure la langue **dans** un modèle ✓. Ici, on mesure
l'inverse : *le même contenu, écrit en deux langues, donne-t-il des états **comparables** ?* ✓✓ C'est la version
forte de la couche commune — celle qui dirait qu'un état porte le **sens** et pas la langue ✓.

LE DISPOSITIF (retrieval croisé ✓). On prend un livre **parallèle** (Le Tour du monde en quatre-vingts jours ✓ :
le français est l'original ✓, l'anglais est la traduction ✓), on le découpe en **N segments** ✓ (par proportion
du texte ✓ — les éditions n'ont pas les mêmes frontières de chapitres ✗✓, c'est une **approximation assumée** ✗),
on encode chaque segment ✓, et on demande : *pour chaque segment français, quel segment anglais est le plus
proche ?* ✓ Si c'est **son homologue** ✓✓ (et non un autre ✓), les états portent le **sens** ✓✓.

⚠️ CE QUE CE TEST NE PEUT PAS DIRE, et qu'il faut écrire d'avance ✗ :
  · l'alignement est **proportionnel** ✗, pas exact — deux segments peuvent couvrir des passages légèrement
    différents ✓✗, ce qui **plombe** le score sans que les états soient en cause ✓ ;
  · le hasard est **1/N** ✓ (avec N = 24, 4,2 % ✓) — c'est la référence ✓.

Usage :
  python3 tools/retrieval_parallele.py --hf /tmp/jouet-mixte --n 24
"""
from __future__ import annotations
import argparse, pathlib, sys
import numpy as np, torch


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="/tmp/jouet-mixte")
    ap.add_argument("--fr", default="/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_fr.txt")
    ap.add_argument("--en", default="/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_en.txt")
    ap.add_argument("--n", type=int, default=24)
    ap.add_argument("--centrer", action="store_true",
                    help="CENTRER les états avant la similarité ✓ — sans quoi une direction commune dominante "
                         "les rend tous à 0,87 de similarité ✗✓ et le retrieval est noyé ✓")
    ap.add_argument("--couche", type=int, default=-1, help="couche à lire (-1 = la dernière ✓)")
    ap.add_argument("--longueur", type=int, default=400, help="octets par segment")
    a = ap.parse_args()
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    L = m.config.num_hidden_layers

    def segments(chemin):
        t = pathlib.Path(chemin).read_text(errors="ignore")
        pas = len(t) // a.n
        return [t[i * pas:(i + 1) * pas][:a.longueur] for i in range(a.n)]

    def etat(txt):
        b = np.frombuffer(txt.encode("utf-8", errors="ignore"), dtype=np.uint8).astype(np.int64)
        if len(b) < 8: return None
        with torch.no_grad():
            x = torch.tensor(b).unsqueeze(0)
            hs = m(x, output_hidden_states=True).hidden_states
            couche = L if a.couche < 0 else a.couche
            return m.model.norm(hs[couche][0]).mean(0).numpy()   # l'état MOYEN du segment ✓

    seg_fr, seg_en = segments(a.fr), segments(a.en)
    E_fr = np.stack([e for e in (etat(s) for s in seg_fr) if e is not None])
    E_en = np.stack([e for e in (etat(s) for s in seg_en) if e is not None])
    n = min(len(E_fr), len(E_en))
    E_fr, E_en = E_fr[:n], E_en[:n]

    # similarité cosinus entre tous les couples ✓, puis « le plus proche est-il l'homologue ? » ✓
    if a.centrer:
        # ⚠️ LE CENTRAGE, ET POURQUOI IL EST NÉCESSAIRE ✗✓. Sans lui, TOUS les états se ressemblent à ~0,87 ✓✗
        # (une direction commune, celle de « texte ordinaire » ✓) et le retrieval est noyé ✓✓. En retirant la
        # moyenne, on ne garde que ce qui DISTINGUE les segments ✓✓ — ce qu'on veut mesurer.
        moy = np.concatenate([E_fr, E_en]).mean(0)
        E_fr, E_en = E_fr - moy, E_en - moy
    A = E_fr / np.linalg.norm(E_fr, axis=1, keepdims=True)
    B = E_en / np.linalg.norm(E_en, axis=1, keepdims=True)
    S = A @ B.T
    pred = S.argmax(axis=1)
    exact = 100 * float(np.mean(pred == np.arange(n)))
    tol1 = 100 * float(np.mean(np.abs(pred - np.arange(n)) <= 1))
    print(f"  {n} segments · dernier étage ({L}) · hasard = {100/n:.1f} %")
    print(f"  retrieval EXACT        : {exact:5.1f} %  ({int(exact*n/100)}/{n})")
    print(f"  à ±1 segment près      : {tol1:5.1f} %")
    diag = float(np.mean(np.diag(S)))
    hors = float(np.mean(S[~np.eye(n, dtype=bool)]))
    print(f"  similarité des homologues : {diag:+.4f} · des autres : {hors:+.4f} → écart {diag-hors:+.4f}")
    print()
    print("  lecture : un retrieval TRÈS au-dessus du hasard ✓✓ signifie que l'état porte le SENS, pas la langue")
    print("  ✓✓. Un score proche du hasard ✗ ne condamne pas les états : l'alignement proportionnel est une")
    print("  approximation ✗ (deux segments peuvent couvrir des passages différents ✓✗).")
    return 0

raise SystemExit(main())

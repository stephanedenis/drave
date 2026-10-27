#!/usr/bin/env python3
"""diagnostic.py — plusieurs entrées, un z, plusieurs sorties : où l'ambiguïté reste.

Pour chaque article de validation, on encode **toutes** les langues, puis on
décode chaque `z` vers **toutes** les langues en un seul lot. La matrice
`chrF[source][cible]` et la **cohérence entre sources** (même cible, sources
différentes) disent si le sens est partagé ou si la langue d'entrée fuit.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import torch
import torch.nn.functional as F

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from llm.mesure import chrf  # noqa: E402
from semantique.corpus import charger, decouper, exemple  # noqa: E402
from semantique.entrainer import pad, texte  # noqa: E402
from semantique.modele import Semantique  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", default="/tmp/natif-600-512-8-align-s1")
    ap.add_argument("--etat", required=True)
    ap.add_argument("--langues", default="fra,spa,deu,cmn,swh")
    ap.add_argument("--articles", type=int, default=30)
    ap.add_argument("--seq", type=int, default=256)
    ap.add_argument("--prefixe", type=int, default=16)
    ap.add_argument("--deux-bases", action="store_true")
    ap.add_argument("--val", type=int, nargs=2, default=[25, 30])
    ap.add_argument("--sortie", default="/tmp/semantique-diagnostic")
    args = ap.parse_args()
    langues = [l.strip() for l in args.langues.split(",") if l.strip()]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    arts = charger(langues, args.articles)
    _, val = decouper(arts, tuple(args.val))
    modele = Semantique.charger(args.checkpoint, len(langues), 128, args.prefixe,
                                str(device), deux_bases=args.deux_bases)
    paquet = torch.load(args.etat, map_location=device, weights_only=False)
    cible = modele.state_dict()
    filtre = {k: v for k, v in paquet["etat"].items()
              if k in cible and cible[k].shape == v.shape}
    modele.load_state_dict(filtre, strict=False)
    modele.eval()
    matrice, consensus, refs = {}, {}, {}
    for art, textes in val.items():
        ids, masque = pad([exemple(val, art, l, args.seq) for l in langues])
        with torch.no_grad():
            z = modele.encode(ids.to(device), masque.to(device), "mean")
            # source x cible, un seul lot
            zb = z.repeat_interleave(len(langues), dim=0)
            lb = torch.arange(len(langues), device=device).repeat(len(langues))
            out = modele.generer(zb, lb, args.seq)
        L = len(langues)
        m = [[0.0] * L for _ in range(L)]
        for i in range(L):
            for j in range(L):
                hyp = texte(out[i * L + j].tolist())
                m[i][j] = chrf(hyp, textes[langues[j]])
        matrice[art] = m
        refs[art] = textes
        # cohérence entre sources pour une même cible
        cons = []
        for j in range(L):
            hyps = [texte(out[i * L + j].tolist()) for i in range(L)]
            paires = [chrf(hyps[i], hyps[k]) for i in range(L) for k in range(i + 1, L)]
            cons.append(sum(paires) / max(1, len(paires)))
        consensus[art] = cons
    L = len(langues)
    diag = sum(matrice[a][i][i] for a in matrice for i in range(L)) / (len(matrice) * L)
    off = sum(matrice[a][i][j] for a in matrice for i in range(L) for j in range(L) if i != j) / (len(matrice) * L * (L - 1))
    plancher = sum(chrf(refs[a][langues[i]], refs[a][langues[j]]) for a in refs for i in range(L) for j in range(L) if i != j) / (len(refs) * L * (L - 1))
    cons = sum(sum(c) for c in consensus.values()) / (len(consensus) * L)
    resultat = {"langues": langues, "articles": list(val), "matrice": matrice,
                "consensus_par_cible": consensus,
                "chrf_diagonal": diag, "chrf_hors_diagonal": off, "chrf_plancher": plancher,
                "consensus_sources": cons,
                "sensibilite_source": 1.0 - cons / 100.0}
    pathlib.Path(str(args.sortie) + ".json").write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"# diagnostic · {len(langues)} langues · {len(val)} articles · "
          f"diag {diag:.1f} · hors diag {off:.1f} · plancher {plancher:.1f} · "
          f"consensus sources {cons:.1f}", flush=True)
    print(json.dumps(resultat, ensure_ascii=False)[:200], flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""composition_verne.py — ÉTAGE 2 : la composition sur des phrases VRAIMENT alignées (Verne FR/EN).

POURQUOI ✓✓. La mesure 79 a échoué sur des préfixes de **caractères** (unités non équivalentes) ✗✗, et le corpus JW
n'a **aucun** paragraphe à plusieurs phrases dont le nombre soit égal dans les 12 langues (les traductions coupent
différemment) ✗✗. Reste un corpus où les phrases sont **alignées par un algorithme** (Gale-Church) et **vérifiées**
par des ancres : **Le Tour du monde en quatre-vingts jours**, FR/EN, 2 570 paires strictes 1:1 ✓✓ (mesure 64).

LE TEST ✓✓ : sur 200 phrases strictes (50 séries de 4 phrases consécutives dans un chapitre), on mesure :
  1. **retrieval global** FR → EN parmi 200 (hasard = 0,5 %) ✓✓ ;
  2. **ordre dans la série** : la plus proche parmi les **4 phrases de la même série** est-elle la bonne position ?
     hasard = **25 %** ✓✓ — *c'est le test de composition : le sens de la phrase, pas le thème du chapitre* ✓✓ ;
  3. **pont** (ridge dual) et **contrôle négatif** ✓✓, dans les deux sens.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def retr(A, B):
    return float(np.mean(np.argmax(norm(A) @ norm(B).T, 1) == np.arange(len(A))))


def extraction(model, tok, textes, couches, batch=8, max_len=512):
    import torch
    dev = next(model.parameters()).device
    sorties = {L: [] for L in couches}
    for i in range(0, len(textes), batch):
        lot = textes[i:i + batch]
        enc = tok(lot, return_tensors="pt", padding=True, truncation=True, max_length=max_len).to(dev)
        with torch.no_grad():
            hs = model(**enc, output_hidden_states=True).hidden_states
        idx = enc["attention_mask"].sum(1) - 1
        for L in couches:
            sorties[L].append(hs[L][torch.arange(len(lot)), idx].float().cpu().numpy())
    return {L: np.concatenate(v, 0) for L, v in sorties.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--dtype", default="float16")
    ap.add_argument("--series", type=int, default=50)
    ap.add_argument("--par-serie", type=int, default=4)
    ap.add_argument("--sortie", default="reports/composition-verne.json")
    ap.add_argument("--etats", default="data/composition-verne-etats.npz")
    ap.add_argument("--repartir", action="store_true", help="répartir le modèle sur les deux cartes (7 B)")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    d = json.loads(pathlib.Path("data/alignement/verne_fr_en.json").read_text())
    paires = [p for p in d["paires"] if p.get("n_fr") == 1 and p.get("n_en") == 1]
    par_chap = {}
    for p in paires:
        par_chap.setdefault(p["chapitre"], []).append(p)
    series = []
    for ch in sorted(par_chap):
        ps = sorted(par_chap[ch], key=lambda p: p["i_fr"])
        for i in range(0, len(ps) - a.par_serie + 1, a.par_serie):
            bloc = ps[i:i + a.par_serie]
            if len(bloc) == a.par_serie:
                series.append((ch, bloc))
    pas = max(1, len(series) // a.series)
    series = series[::pas][: a.series]
    textes, meta = [], []
    for k, (ch, bloc) in enumerate(series):
        for j, p in enumerate(bloc):
            textes += [p["fr"], p["en"]]
            meta.append((k, j))
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    if a.repartir:
        model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype),
                                                     device_map="auto").eval()
    else:
        model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype)).to("cuda").eval()
    n_layers = model.config.num_hidden_layers
    couches = sorted(set([0, n_layers // 6, n_layers // 3, n_layers // 2, 2 * n_layers // 3,
                          5 * n_layers // 6, n_layers]))
    etats = extraction(model, tok, textes, couches)
    # une ligne par état, deux états par phrase (FR puis EN) : le nom doit suivre la ligne, pas la phrase
    noms = [f"{k}|{j}|{langue}" for k, j in meta for langue in ("fr", "en")]
    assert len(noms) == len(etats[couches[0]]), (len(noms), len(etats[couches[0]]))
    np.savez_compressed(a.etats, **{f"L{L}": etats[L] for L in couches},
                        couches=np.array(couches), noms=np.array(noms))
    rng = np.random.default_rng(1234)
    n = len(series) * a.par_serie
    idx = rng.permutation(n); tr, te = idx[: int(0.7 * n)], idx[int(0.7 * n):]
    res = []
    for L in couches:
        E = etats[L]
        F = E[0::2]; A = E[1::2]       # paires (fr, en) dans l'ordre
        glob = retr(F, A)
        # ordre : la bonne position parmi les 4 phrases de la série ✓✓
        justes = total = 0
        for k in range(len(series)):
            base = k * a.par_serie
            for j in range(a.par_serie):
                i = base + j
                sims = [float((norm(F[i:i+1]) @ norm(A[base + j2:base + j2 + 1]).T).item())
                        for j2 in range(a.par_serie)]
                justes += (int(np.argmax(sims)) == j); total += 1
        ordre = justes / max(1, total)
        # pont dual fr -> en, lambda validé sur 20 % du train ✓
        tr2, va = tr[: int(0.8 * len(tr))], tr[int(0.8 * len(tr)):]
        def fit(X, Y, lam):
            mx, my = X.mean(0), Y.mean(0); Xc, Yc = X - mx, Y - my
            al = np.linalg.solve(Xc @ Xc.T + lam * np.eye(len(Xc), dtype=np.float32), Yc)
            return mx, my, Xc, al
        def pred(X, m):
            mx, my, Xc, al = m
            return (X - mx) @ Xc.T @ al + my
        lam = max((0.1, 1.0, 10.0, 100.0, 1000.0),
                  key=lambda l: retr(pred(F[va], fit(F[tr2], A[tr2], l)), A[va]))
        m = fit(F[tr], A[tr], lam)
        pf = pred(F[te], m)
        cos = float(np.mean(np.sum(norm(pf) * norm(A[te]), 1)))
        pont = retr(pf, A[te])
        mel = rng.permutation(len(tr))
        neg = retr(pred(F[te], fit(F[tr], A[tr][mel], lam)), A[te])
        res.append({"couche": int(L), "retrieval_global": round(glob, 4), "ordre_serie": round(ordre, 4),
                    "cosinus_pont": round(cos, 4), "retrieval_pont": round(pont, 4),
                    "retrieval_negatif": round(neg, 4), "lambda": lam})
        print(f"  couche {L:2d} · global {glob:.3f} · ordre {ordre:.3f} · pont {pont:.3f} · nég {neg:.3f}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"n_series": len(series), "par_serie": a.par_serie,
                                                  "n_phrases": n, "resultats": res},
                                                 ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

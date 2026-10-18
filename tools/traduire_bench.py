#!/usr/bin/env python3
"""traduire_bench.py — LA QUALITÉ DE TRADUCTEUR, MESURÉE (chrF contre traduction humaine).

POURQUOI CE BANC. Les mesures de la série UDHR testaient le **retrieval** (retrouver le même article) — une
propriété de l'état, pas une qualité de **traduction** ✓✗. Ici, on demande au modèle de **traduire** ✓, et on
compare sa sortie à la **traduction humaine de référence** ✓✓ (les 448 langues UDHR sont des traductions humaines
alignées ✓ ; Verne et Alice donnent les domaines littéraires ✓).

LA MÉTRIQUE. **chrF** (Popović 2015 ✓) : F-score de n-grammes de **caractères** (n = 1..6, β = 2 ✓), insensible à
la tokenisation ✓ — c'est la métrique standard pour les langues à morphologie riche et les écritures non latines
✓✓. On rapporte aussi deux **bornes** : la source elle-même comparée à la référence ✓ (le plancher : « ne rien
traduire » ✓✗) et une référence **mélangée** ✓ (le hasard ✓).

⚠️ CE QUE CE BANC NE DIT PAS ✗ : chrF mesure la **ressemblance de surface** avec UNE référence humaine ✓✗ — une
bonne traduction peut différer ; et Qwen 0,5 B est un petit modèle ✓, les scores seront bas ✓✓ : c'est un
**classement relatif** entre domaines et paires, pas une note absolue ✓.
"""
from __future__ import annotations
import argparse, json, pathlib, random, unicodedata
import numpy as np


def chrf(hyp: str, ref: str, n_max: int = 6, beta: float = 2.0) -> float:
    """chrF : F-beta sur les n-grammes de caractères (n=1..6) ✓."""
    hyp = " ".join(unicodedata.normalize("NFC", hyp).split())
    ref = " ".join(unicodedata.normalize("NFC", ref).split())
    if not hyp or not ref:
        return 0.0
    prec, rec = [], []
    for n in range(1, n_max + 1):
        H = [hyp[i:i + n] for i in range(max(0, len(hyp) - n + 1))]
        R = [ref[i:i + n] for i in range(max(0, len(ref) - n + 1))]
        from collections import Counter
        ch, cr = Counter(H), Counter(R)
        inter = sum((ch & cr).values())
        prec.append(inter / max(1, len(H)))
        rec.append(inter / max(1, len(R)))
    p, r = float(np.mean(prec)), float(np.mean(rec))
    b2 = beta * beta
    return 100 * (1 + b2) * p * r / max(1e-9, b2 * p + r)


def charger_udhr():
    arts = [json.loads(l) for l in pathlib.Path("data/udhr/articles_propres.jsonl").read_text().splitlines()]
    par = {}
    for x in arts:
        par.setdefault(x["iso3"], {})[int(x["art"])] = x["texte"]
    return par


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--paires", default="fra:eng,eng:fra,fra:deu,fra:spa,fra:cmn")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--max-jetons", type=int, default=160)
    ap.add_argument("--sortie", default="reports/traduction-legal.json")
    a = ap.parse_args()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).to(device).eval()
    tok = AutoTokenizer.from_pretrained(a.hf)
    par = charger_udhr()
    noms = {"fra": "French", "eng": "English", "deu": "German", "spa": "Spanish", "ita": "Italian",
            "cmn": "Chinese", "rus": "Russian", "jpn": "Japanese"}
    resultats = []
    rng = random.Random(0)
    for paire in a.paires.split(","):
        src, dst = paire.split(":")
        if src not in par or dst not in par:
            print(f"  ✗ {paire} : langue absente"); continue
        arts = sorted(set(par[src]) & set(par[dst]))[: a.n]
        scores, plancher, hasard = [], [], []
        for n in arts:
            texte = par[src][n]
            demande = (f"Translate the following text into {noms.get(dst, dst)}. "
                       f"Answer with the translation only.\n\n{texte}")
            ids = tok(demande, return_tensors="pt").to(device)
            with torch.no_grad():
                g = m.generate(**ids, max_new_tokens=a.max_jetons, do_sample=False,
                               pad_token_id=tok.eos_token_id)
            sortie = tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)
            ref = par[dst][n]
            scores.append(chrf(sortie, ref))
            plancher.append(chrf(texte, ref))                 # « ne rien traduire » ✓✗
            autres = [par[dst][k] for k in par[dst] if k != n]
            hasard.append(chrf(sortie, rng.choice(autres)))   # référence mélangée ✓
        resultats.append({"paire": paire, "n": len(scores), "chrf": float(np.mean(scores)),
                          "plancher_source": float(np.mean(plancher)), "hasard": float(np.mean(hasard))})
        print(f"  {paire:9s} · chrF {np.mean(scores):5.1f} · plancher source {np.mean(plancher):5.1f} · "
              f"hasard {np.mean(hasard):5.1f} · {len(scores)} articles")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(resultats, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

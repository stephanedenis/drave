#!/usr/bin/env python3
"""miroir_boucle.py — LE MIROIR DE SORTIE VALIDE-T-IL L'ENTRÉE ? (boucle de traduction)

LE PRINCIPE (AGENTS.md §7). La sortie (**sens → texte**) est plus fiable que l'entrée (**texte → sens**) parce
qu'elle part d'un sens propre. On s'en sert comme **miroir** : ce que l'entrée a compris doit pouvoir être
**redît par la sortie** ✓✓. Le test le plus direct : **traduire, puis revenir** — entrée A → sortie B → entrée A ✓.

TROIS CHIFFRES ✗ :
  · **chrF direct** (A→B contre la référence humaine) ✓ : la qualité de la sortie ;
  · **chrF de boucle** (A→B→A contre la source) ✓✓ : la **cohérence** du miroir — c'est le juge de l'entrée ;
  · **plancher** (la source contre elle-même = 100, et la sortie directe contre la référence) ✓.

⚠️ CE QUE LA BOUCLE NE DIT PAS ✗ : une boucle fidèle peut être **fidèle à une erreur** ✓✗ (le modèle traduit mal
puis retraduit sa propre erreur) — c'est pourquoi on lit les deux chiffres **ensemble** ✓✓ : boucle haute **et**
direct haut = miroir fiable ; boucle haute **seule** = le modèle est cohérent avec lui-même, pas avec la référence
✗✓.
"""
from __future__ import annotations
import argparse, json, pathlib, unicodedata
import numpy as np
from collections import Counter


def chrf(hyp: str, ref: str, n_max: int = 6, beta: float = 2.0) -> float:
    hyp = " ".join(unicodedata.normalize("NFC", hyp).split())
    ref = " ".join(unicodedata.normalize("NFC", ref).split())
    if not hyp or not ref:
        return 0.0
    prec, rec = [], []
    for n in range(1, n_max + 1):
        ch = Counter(hyp[i:i + n] for i in range(max(0, len(hyp) - n + 1)))
        cr = Counter(ref[i:i + n] for i in range(max(0, len(ref) - n + 1)))
        inter = sum((ch & cr).values())
        prec.append(inter / max(1, sum(ch.values())))
        rec.append(inter / max(1, sum(cr.values())))
    p, r = float(np.mean(prec)), float(np.mean(rec))
    b2 = beta * beta
    return 100 * (1 + b2) * p * r / max(1e-9, b2 * p + r)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--paire", default="fra:eng")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--max-jetons", type=int, default=160)
    ap.add_argument("--sortie", default="reports/miroir-boucle.json")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).to(device).eval()
    tok = AutoTokenizer.from_pretrained(a.hf)
    arts = [json.loads(l) for l in pathlib.Path("data/udhr/articles_propres.jsonl").read_text().splitlines()]
    par = {}
    for x in arts:
        par.setdefault(x["iso3"], {})[int(x["art"])] = x["texte"]
    src, dst = a.paire.split(":")
    noms = {"fra": "French", "eng": "English", "deu": "German", "spa": "Spanish", "cmn": "Chinese"}
    def traduire(texte, langue):
        demande = f"Translate the following text into {noms.get(langue, langue)}. Answer with the translation only.\n\n{texte}"
        ids = tok(demande, return_tensors="pt").to(device)
        with torch.no_grad():
            g = m.generate(**ids, max_new_tokens=a.max_jetons, do_sample=False, pad_token_id=tok.eos_token_id)
        return tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()
    res = []
    for n in sorted(set(par[src]) & set(par[dst]))[: a.n]:
        direct = traduire(par[src][n], dst)
        retour = traduire(direct, src)
        res.append({"article": n, "chrf_direct": chrf(direct, par[dst][n]),
                    "chrf_boucle": chrf(retour, par[src][n]),
                    "plancher_source": chrf(par[src][n], par[src][n])})
    d = float(np.mean([r["chrf_direct"] for r in res]))
    b = float(np.mean([r["chrf_boucle"] for r in res]))
    print(f"  {a.paire} · {len(res)} articles · chrF direct {d:5.1f} · chrF boucle {b:5.1f} · plancher 100")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"paire": a.paire, "direct": d, "boucle": b, "detail": res},
                                                 ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

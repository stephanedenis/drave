#!/usr/bin/env python3
"""registre_parle.py — LE REGISTRE PARLÉ : qualité de traducteur sur TED2020 (discours réels, traductions humaines).

POURQUOI ✓✓. Les mesures 64 et 68 ont couvert le juridique, la presse et le littéraire ; le **parlé** et le
**technique** manquaient. TED2020 est un corpus **parallèle humain** (les traductions des conférences TED, faites par
des bénévoles) : un registre **parlé** (transcriptions de discours), souvent **technique** (sciences, ingénierie) ✓✓.

CE QU'ON MESURE ✓✓, dans les deux sens (le miroir entrée/sortie) :
  · le **chrF** de la traduction du modèle contre la référence humaine ✓ ;
  · le **plancher** (chrF de la source contre la référence : « ne rien traduire ») ✓✓ ;
  · la **marge** (traduction − plancher) et son **IC bootstrap** (1 000 rééchantillonnages appariés) ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · une marge positive et large → le modèle traduit le parlé ✓✓ ;
  · une marge faible ou nulle → le parlé est un registre où il ne traduit pas ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib, random
import numpy as np


def chrf(hyp: str, ref: str, n_max: int = 6, beta: float = 2.0) -> float:
    from collections import Counter
    hyp = " ".join(hyp.split()); ref = " ".join(ref.split())
    if not hyp or not ref:
        return 0.0
    prec, rec = [], []
    for n in range(1, n_max + 1):
        H = [hyp[i:i + n] for i in range(max(0, len(hyp) - n + 1))]
        R = [ref[i:i + n] for i in range(max(0, len(ref) - n + 1))]
        ch, cr = Counter(H), Counter(R)
        inter = sum((ch & cr).values())
        prec.append(inter / max(1, len(H))); rec.append(inter / max(1, len(R)))
    p, r = float(np.mean(prec)), float(np.mean(rec))
    b2 = beta * beta
    return 100 * (1 + b2) * p * r / max(1e-9, b2 * p + r)


def ic(marges, n=1000, graine=1234):
    rng = np.random.default_rng(graine)
    m = np.asarray(marges, dtype=np.float64)
    moy = float(m.mean())
    ech = [float(rng.choice(m, len(m), replace=True).mean()) for _ in range(n)]
    return moy, float(np.percentile(ech, 2.5)), float(np.percentile(ech, 97.5))


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-7B-Instruct")
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--sens", choices=["en-fr", "fr-en", "both"], default="both")
    ap.add_argument("--corpus", default="data/ted2020/ted_fr_en.json")
    ap.add_argument("--graine", type=int, default=1234)
    ap.add_argument("--sortie", default="reports/registre-parle-7b.json")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    pairs = json.loads(pathlib.Path(a.corpus).read_text())
    rng = random.Random(a.graine); rng.shuffle(pairs)
    pairs = pairs[:a.n]
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()
    res = {"hf": a.hf, "n": len(pairs), "directions": {}}

    def traduire(texte, consigne):
        msg = [{"role": "user", "content": f"{consigne}\n\n{texte}"}]
        p = tok.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        enc = tok(p, return_tensors="pt", truncation=True, max_length=512).to("cuda")
        with torch.no_grad():
            g = model.generate(**enc, max_new_tokens=256, do_sample=False, pad_token_id=tok.eos_token_id)
        out = tok.decode(g[0][enc["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        return out.split("\n\n")[0].strip().strip('"').strip()

    for sens in (["en-fr", "fr-en"] if a.sens == "both" else [a.sens]):
        src, ref, consigne = ("en", "fr", "Traduis en français. Ne donne que la traduction.") if sens == "en-fr" \
            else ("fr", "en", "Translate into English. Give only the translation.")
        notes, planchers = [], []
        for i, p in enumerate(pairs):
            hyp = traduire(p[src], consigne)
            notes.append(chrf(hyp, p[ref]))
            planchers.append(chrf(p[src], p[ref]))
            if (i + 1) % 50 == 0:
                print(f"  {sens} {i + 1}/{len(pairs)} · chrF {np.mean(notes):.1f} · plancher {np.mean(planchers):.1f}")
        marges = [x - y for x, y in zip(notes, planchers)]
        moy, lo, hi = ic(marges)
        res["directions"][sens] = {"chrf": round(float(np.mean(notes)), 2),
                                   "plancher": round(float(np.mean(planchers)), 2),
                                   "marge": round(moy, 2), "ic95": [round(lo, 2), round(hi, 2)],
                                   "notes": [round(x, 1) for x in notes],
                                   "planchers": [round(y, 1) for y in planchers]}
        print(f"  {sens} : chrF {res['directions'][sens]['chrf']:.1f} · plancher "
              f"{res['directions'][sens]['plancher']:.1f} · **marge {moy:.1f}** [{lo:.1f} ; {hi:.1f}]")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())

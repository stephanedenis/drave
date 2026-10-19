#!/usr/bin/env python3
"""bruit_entree.py — LES MARQUEURS VOIENT-ILS LES IMPERFECTIONS DE L'ENTRÉE ?

LE PRINCIPE (AGENTS.md §7). L'entrée (**texte → sens**) est la partie imparfaite : bruit, langues mêlées, accents
perdus, coquilles ✓✗. Si les **marqueurs de bruit** (surprisal par token, langue, longueur ✓) ne **bougent pas**
quand l'entrée est abîmée, l'interface ne peut pas signaler le bruit au module de pensée ✗✗.

CE QU'ON FAIT. On prend des articles propres (UDHR français ✓) et on fabrique quatre versions :
  · **propre** (référence) ;
  · **fautes** : 10 % des caractères remplacés par un caractère voisin ✓ ;
  · **langue mêlée** : 30 % du texte remplacé par l'article anglais correspondant ✓✓ ;
  · **accents perdus** : tous les accents retirés ✓.
On mesure, pour chaque version : **surprisal moyenne par token** ✓, **bits par phrase** ✓, **fraction de tokens
coûteux** ✓, et **langue répondue** ✓. *Si le bruit est vu, la surprisal monte et/ou la langue devient incertaine* ✓✓.

⚠️ CE QUE ÇA NE DIT PAS ✗ : que le modèle **corrige** le bruit ✓✗ — seulement qu'il le **voit** ✓.
"""
from __future__ import annotations
import argparse, json, math, pathlib, random
import numpy as np


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--sortie", default="reports/bruit-entree.json")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).to(dev).eval()
    tok = AutoTokenizer.from_pretrained(a.hf)
    fr, en = {}, {}
    for l in pathlib.Path("data/udhr/articles_propres.jsonl").read_text().splitlines():
        x = json.loads(l)
        if x["iso3"] == "fra": fr[int(x["art"])] = x["texte"]
        if x["iso3"] == "eng": en[int(x["art"])] = x["texte"]
    rng = random.Random(0)
    def mesure(t):
        ids = tok(t, return_tensors="pt").to(dev)
        with torch.no_grad():
            lp = torch.log_softmax(m(**ids).logits[0], dim=-1)
        c = ids["input_ids"][0][1:]
        sur = (-lp[:-1].gather(1, c.unsqueeze(1)).squeeze(1) / math.log(2)).cpu().numpy()
        msgs = [{"role": "user", "content": "In one word, what language is this text written in? "
                                            "Answer with the language name only.\n\n" + t[:400]}]
        p = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        with torch.no_grad():
            lg = torch.log_softmax(m(**tok(p, return_tensors="pt").to(dev)).logits[0, -1], dim=-1)
        return float(sur.mean()), float(sur.sum()), float((sur > 4).mean()), tok.decode([int(lg.argmax())]).strip().lower()
    res = []
    for n in sorted(fr)[: a.n]:
        propre = fr[n]
        fautes = list(propre)
        for k in range(0, len(fautes), 10):
            if rng.random() < 0.5:
                fautes[k] = rng.choice("abcdefghijklmnopqrstuvwxyzéèêàç")
        melange = propre
        if n in en:
            coup = len(propre) // 3
            melange = propre[:coup] + " " + en[n][:coup] + " " + propre[2 * coup:]
        # ⚠️ LES ACCENTS PERDUS : un bruit très courant sur les entrées réelles ✓✓ (copier-coller, OCR, claviers ✓)
        import unicodedata
        sans = "".join(ch for ch in unicodedata.normalize("NFD", propre) if unicodedata.category(ch) != "Mn")
        for nom, t in (("propre", propre), ("fautes 10%", "".join(fautes)),
                       ("langue mêlée 30%", melange), ("accents perdus", sans)):
            s, tot, cout, lang = mesure(t)
            res.append({"article": n, "version": nom, "surprisal_moyenne": s, "bits_total": tot,
                        "tokens_couteux": cout, "langue": lang})
            print(f"  art.{n} {nom:16s} · {s:5.2f} bits/token · {tot:6.0f} bits · coûteux {cout:4.0%} · langue « {lang} »")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""pidgin_fewshot.py — LE PIDGIN AVEC EXEMPLES : le modèle peut-il produire du naijá s'il en voit ?

POURQUOI ✓✓. La mesure 86 a montré que, **sans exemple**, le modèle ne traduit pas vers le pidgin : 33,9 de chrF
contre un **plancher de 35,3** (marge −1,5) — il **copie/adapte** l'anglais ✗✗. *Mais sait-il le faire s'il voit
deux exemples ?* ✓✓ C'est la question de la **couverture** : un modèle peut **ne pas connaître** une langue en
zéro-shot et la **produire** en **contexte** (in-context learning) ✓✓.

LE DISPOSITIF ✓✓ : le corpus African Storybook (50 pages, 5 contes) ✓. Deux pages d'un conte servent d'**exemples**
(elles sont **retirées** du test) ; on teste sur **20 pages** d'un autre conte ✓✓. Prompt à deux exemples, puis la
page à traduire ✓. On mesure le **chrF**, le **plancher** (source contre référence) et le **hasard** (référence
tirée au hasard) ✓✓, dans les deux sens ✓✓.

⚠️ CE QUE CELA NE DIT PAS ✗ : deux exemples ne font pas un apprentissage ; le résultat mesure la **capacité en
contexte**, pas une compétence stable ✓✓ ; et le corpus reste **non post-cutoff** ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-7B-Instruct")
    ap.add_argument("--dtype", default="float16")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--sortie", default="reports/pidgin-fewshot.json")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    data = json.loads(pathlib.Path("data/pidgin/pidgin.json").read_text())
    unites = data["unites"]
    histoires = sorted({u["histoire"] for u in unites})
    ex_h = histoires[0]
    test_h = histoires[-1]
    ex = [u for u in unites if u["histoire"] == ex_h][:2]
    test = [u for u in unites if u["histoire"] == test_h][: a.n]
    tok = AutoTokenizer.from_pretrained(a.hf)
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype)).to("cuda").eval()

    def genere(prompt: str) -> str:
        p = tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False,
                                    add_generation_prompt=True)
        ids = tok(p, return_tensors="pt").to(model.device)
        with torch.no_grad():
            g = model.generate(**ids, max_new_tokens=300, do_sample=False, pad_token_id=tok.eos_token_id)
        return tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    def prompt_vers_pcm(src: str) -> str:
        t = ("Translate from English into Nigerian Pidgin (Naijá).\n\n")
        for u in ex:
            t += f"English: {u['textes']['eng']}\nNigerian Pidgin: {u['textes']['pcm']}\n\n"
        return t + f"English: {src}\nNigerian Pidgin:"

    def prompt_vers_eng(src: str) -> str:
        t = ("Translate from Nigerian Pidgin (Naijá) into English.\n\n")
        for u in ex:
            t += f"Nigerian Pidgin: {u['textes']['pcm']}\nEnglish: {u['textes']['eng']}\n\n"
        return t + f"Nigerian Pidgin: {src}\nEnglish:"

    rng = np.random.default_rng(1234)
    res = {}
    for sens, (src_lang, dst_lang, prompt) in {"eng→pcm": ("eng", "pcm", prompt_vers_pcm),
                                                "pcm→eng": ("pcm", "eng", prompt_vers_eng)}.items():
        scores, planchers, hasards = [], [], []
        for u in test:
            sortie = genere(prompt(u["textes"][src_lang]))
            ref = u["textes"][dst_lang]
            scores.append(chrf(sortie, ref))
            planchers.append(chrf(u["textes"][src_lang], ref))
            hasards.append(chrf(test[rng.integers(0, len(test))]["textes"][dst_lang], ref))
        res[sens] = {"chrf": round(float(np.mean(scores)), 1),
                     "plancher": round(float(np.mean(planchers)), 1),
                     "hasard": round(float(np.mean(hasards)), 1),
                     "marge_plancher": round(float(np.mean(scores) - np.mean(planchers)), 1),
                     "marge_hasard": round(float(np.mean(scores) - np.mean(hasards)), 1),
                     "n": len(test)}
        print(f"  {sens} : chrF {res[sens]['chrf']} · plancher {res[sens]['plancher']} · "
              f"marge {res[sens]['marge_plancher']:+} · hasard {res[sens]['hasard']}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"hf": a.hf, "exemples": ex_h, "test": test_h,
                                                  "resultats": res}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

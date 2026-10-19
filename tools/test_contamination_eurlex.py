#!/usr/bin/env python3
"""test_contamination_eurlex.py — LE CONTRÔLE POSITIF : sur un texte post-cutoff, le modèle TRADUIT-il ?

POURQUOI ✓✓. La mesure 61 montre que sur l'UDHR, le 7 B **remplace** un mot absurde par le mot canonique
(« en dignité et en couleur » → « in dignity and rights ») : il récite ✓✗. Mais un sceptique peut dire que le mot
absurde est « corrigé » parce qu'il est absurde, ou que la phrase est trop courte ✓✗. Ce contrôle prend le **même
modèle, la même consigne, le même domaine juridique**, mais un texte qu'il n'a **pas pu mémoriser** : un règlement
européen de **2025** (postérieur à sa coupure) ✓✓. On y substitue un mot, on traduit vers le français, et on regarde
si le mot **substitué** arrive dans la sortie ✓✓.

  - si le modèle transporte la substitution sur EUR-Lex (texte neuf) mais pas sur l'UDHR (texte mémorisé),
    la différence **est** la mémoire ✓✓ — pas la difficulté, pas la longueur, pas le domaine ✓✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib, re, unicodedata

# (unité, mot anglais remplacé, mot anglais substitué, mot français attendu)
SUBSTITUTIONS = [
    ("rct_1", "Ukraine", "Utopia", r"\butopie\b"),
    ("rct_3", "Investment", "Chocolate", r"\bchocolat\b"),
    ("rct_4", "ammunition", "bananas", r"\bbananes?\b"),
    ("rct_5", "Procurement", "picnic", r"\bpique-?nique\b"),
    ("rct_7", "Programme", "recipe", r"\brecette\b"),
    ("rct_10", "financial", "chocolate", r"\bchocolat\b"),
]


def nz(t: str) -> str:
    return " ".join(unicodedata.normalize("NFC", t).lower().split())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--dtype", default="bfloat16", choices=["float32", "bfloat16"])
    ap.add_argument("--corpus", default="data/eurlex/32025R1106.json")
    ap.add_argument("--sortie", default="reports/contamination-eurlex.json")
    ap.add_argument("--litteral", action="store_true")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype)).to("cuda").eval()
    tok = AutoTokenizer.from_pretrained(a.hf)
    unites = {u["id"]: u for u in json.loads(pathlib.Path(a.corpus).read_text())["unites"]}

    def genere(texte: str) -> str:
        consigne = ("Translate the following text into French. Answer with the translation only.")
        if a.litteral:
            consigne = ("Translate the following text into French. Translate literally and do not correct or "
                        "normalise anything, even if it seems strange. Answer with the translation only.")
        prompt = tok.apply_chat_template([{"role": "user", "content": consigne + "\n\n" + texte}],
                                         tokenize=False, add_generation_prompt=True)
        ids = tok(prompt, return_tensors="pt").to(m.device)
        with torch.no_grad():
            g = m.generate(**ids, max_new_tokens=500, do_sample=False, pad_token_id=tok.eos_token_id)
        return tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)

    res = []
    for uid, vieux, neuf, attendu in SUBSTITUTIONS:
        source = unites[uid]["textes"]["eng"]
        m2 = re.search(re.escape(vieux), source, re.I)
        if not m2:
            print(f"  ✗ {uid} : « {vieux} » absent"); continue
        modifiee = source[:m2.start()] + neuf + source[m2.end():]
        sortie = genere(modifiee)
        porte = bool(re.search(attendu, nz(sortie)))
        res.append({"unite": uid, "vieux": vieux, "neuf": neuf, "attendu": attendu,
                    "source_modifiee": modifiee, "sortie": sortie, "porte_le_neuf": porte})
        print(f"  {uid:7s} · {neuf:10s} → {'TRADUIT' if porte else '✗ PERDU'} · {sortie[:110].replace(chr(10), ' ')}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"litteral": a.litteral, "resultats": res},
                                                 ensure_ascii=False, indent=1))
    print(f"  → {sum(r['porte_le_neuf'] for r in res)}/{len(res)} substitutions TRANSPORTÉES sur un texte "
          f"post-cutoff · {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

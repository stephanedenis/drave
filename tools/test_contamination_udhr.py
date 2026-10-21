#!/usr/bin/env python3
"""test_contamination_udhr.py — L'UDHR EST-ELLE RÉCITÉE DANS LES LANGUES QUI MANQUENT ?

POURQUOI ✓✓. La mesure 61 a montré que l'UDHR est **contaminée** pour les grandes langues : le 7 B récite
l'article 1 au lieu de traduire ✓✗. Mais les **13 langues manquantes** de la couverture démographique (hindi, arabe,
bengali, indonésien, urdu, japonais, pidgin nigérian, marathi, vietnamien, télougou, swahili, haoussa…) n'ont, pour
la plupart, **aucun corpus post-cutoff** : l'UDHR est la seule ressource humaine alignée ✓✗. *Peut-on l'utiliser
là où le modèle ne l'a peut-être pas mémorisée ?* ✓✓

LE TEST ✓✓. Pour chaque langue, on prend 5 articles, on **ajoute une phrase neuve** « Zorblax is here. » à la fin,
et on demande la traduction **vers l'anglais** ✓. Si le modèle traduit ce qu'il lit, le nom **Zorblax** apparaît
dans la sortie anglaise ✓✓ ; s'il **récite** la traduction officielle, la phrase neuve disparaît ✗✗. On traduit
aussi l'article **non modifié** pour mesurer le chrF contre la référence anglaise et voir la qualité ✓.

VERDICT PAR LANGUE ✓✗ :
  · **traduit** : le jeton est porté dans au moins 4 articles sur 5 ✓✓ → l'UDHR est utilisable comme banc ;
  · **récite** : le jeton disparaît **et** le chrF est très haut (≥ 75) **et** la sortie est en anglais ✓✗ →
    l'UDHR est contaminée, il faut un corpus post-cutoff ;
  · **ne sait pas** : le jeton disparaît, le chrF est bas, la sortie n'est pas de l'anglais propre ✓✗ → le modèle
    ne traduit pas cette langue ; le banc mesurerait son incapacité, pas sa mémoire.

⚠️ CE QUE LE TEST NE DIT PAS ✗ : un modèle peut **ignorer** une phrase ajoutée sans avoir mémorisé l'UDHR ✓✗ ; le
taux de portage est un **indice**, pas une preuve ; on garde les sorties pour l'audit humain ✓.
"""
from __future__ import annotations
import argparse, json, pathlib, re, unicodedata
import numpy as np


def chrf(hyp: str, ref: str, n_max: int = 6, beta: float = 2.0) -> float:
    from collections import Counter
    hyp = " ".join(unicodedata.normalize("NFC", hyp).split())
    ref = " ".join(unicodedata.normalize("NFC", ref).split())
    if not hyp or not ref:
        return 0.0
    prec, rec = [], []
    for n in range(1, n_max + 1):
        H = [hyp[i:i + n] for i in range(max(0, len(hyp) - n + 1))]
        R = [ref[i:i + n] for i in range(max(0, len(ref) - n + 1))]
        ch, cr = Counter(H), Counter(R)
        inter = sum((ch & cr).values())
        prec.append(inter / max(1, len(H)))
        rec.append(inter / max(1, len(R)))
    p, r = float(np.mean(prec)), float(np.mean(rec))
    b2 = beta * beta
    return 100 * (1 + b2) * p * r / max(1e-9, b2 * p + r)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--langues", default="hin,arb,ben,ind,urd,jpn,pcm,mar,vie,tel,swh,hau")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--dtype", default="float16", choices=["float32", "bfloat16", "float16"])
    ap.add_argument("--sortie", default="reports/contamination-udhr-langues.json")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype)).to("cuda").eval()
    tok = AutoTokenizer.from_pretrained(a.hf)
    par = {}
    for l in pathlib.Path("data/udhr/articles_propres.jsonl").read_text().splitlines():
        x = json.loads(l)
        par.setdefault(x["iso3"], {})[int(x["art"])] = x["texte"]

    def genere(texte: str) -> str:
        demande = ("Translate the following text into English. Answer with the translation only.\n\n" + texte)
        prompt = tok.apply_chat_template([{"role": "user", "content": demande}], tokenize=False,
                                         add_generation_prompt=True)
        ids = tok(prompt, return_tensors="pt").to(m.device)
        with torch.no_grad():
            g = m.generate(**ids, max_new_tokens=500, do_sample=False, pad_token_id=tok.eos_token_id)
        return tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    res = []
    for lg in a.langues.split(","):
        if lg not in par or "eng" not in par:
            print(f"  ✗ {lg} : absent de l'UDHR"); continue
        arts = sorted(set(par[lg]) & set(par.get("eng", {})))[: a.n]
        portes = 0; chrf_scores = []; details = []
        for n in arts:
            src, ref = par[lg][n], par["eng"][n]
            sortie = genere(src + " Zorblax is here.")
            porte = "zorblax" in sortie.lower() or "зорблакс" in sortie.lower()
            portes += porte
            # la traduction non modifiée : le chrF et la langue de sortie ✓
            sortie_clean = genere(src)
            c = chrf(sortie_clean, ref)
            chrf_scores.append(c)
            details.append({"article": n, "porte_le_jeton": porte, "chrf": round(c, 1),
                            "sortie_avec_jeton": sortie[:400], "sortie": sortie_clean[:400]})
        moyenne = float(np.mean(chrf_scores)) if chrf_scores else 0.0
        if portes >= max(4, a.n - 1):
            verdict = "traduit"
        elif moyenne >= 75:
            verdict = "récite"
        else:
            verdict = "ne sait pas"
        res.append({"langue": lg, "n": len(arts), "jeton_porte": portes, "chrf": round(moyenne, 1),
                    "verdict": verdict, "details": details})
        print(f"  {lg:4s} · jeton porté {portes}/{len(arts)} · chrF moyen {moyenne:5.1f} · {verdict.upper()}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

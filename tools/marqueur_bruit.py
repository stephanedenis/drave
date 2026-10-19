#!/usr/bin/env python3
"""marqueur_bruit.py — LE SENS EXTRAIT PORTE SON BRUIT (AGENTS.md §7, règle 3).

POURQUOI. L'entrée (**texte → sens**) est la partie **imparfaite** de la couche : bruit, orthographes multiples,
langues mêlées, coquilles ✓✗. La sortie, plus fiable, sert de **miroir** pour la juger ✓✓ ; mais pour que le module
de pensée abstraite ne reçoive pas un sens **lissé**, l'interface doit porter des **marqueurs de bruit** ✓✓ :
*confiance par token, tokens ambigus, langue détectée avec sa probabilité* ✓.

CE QU'IL MESURE, avec Qwen ✓ :
  · **entropie par token** ✓ : H = −Σ p log₂ p sur la distribution du modèle au token suivant l'id ; normalisée par
    log₂(vocabulaire) ✓ — un token certain a une entropie proche de 0 ✓✓, un token ambigu proche de 1 ✗✓ ;
  · **tokens ambigus** ✓ : la fraction où l'entropie dépasse un seuil (0,5 par défaut ✓) ;
  · **langue probable** ✓ : on demande au modèle de nommer la langue, et on lit la **probabilité** de chaque nom
    candidat au premier token généré ✓✓ (pas de génération libre : une distribution sur les noms ✓).

SORTIE : un JSON par texte (`--sortie`), avec la liste des tokens (id, entropie, drapeau) et le résumé.
⚠️ CE QUE CE N'EST PAS ✗ : ce n'est **pas** la confiance de la traduction ✓ (elle est mesurée par la boucle, mesure
51) — c'est la confiance de l'**entrée** ✓✓, c'est-à-dire ce qu'on sait de ce qu'on a lu ✓.
"""
from __future__ import annotations
import argparse, json, math, pathlib
import numpy as np


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--langues", default="fra,eng,cmn")
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--seuil", type=float, default=0.5)
    ap.add_argument("--sortie", default="reports/marqueurs-bruit.json")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).to(dev).eval()
    tok = AutoTokenizer.from_pretrained(a.hf)
    par = {}
    for l in pathlib.Path("data/udhr/articles_propres.jsonl").read_text().splitlines():
        x = json.loads(l)
        par.setdefault(x["iso3"], {})[int(x["art"])] = x["texte"]
    NOMS = {"fra": "French", "eng": "English", "deu": "German", "spa": "Spanish", "cmn": "Chinese",
            "rus": "Russian", "jpn": "Japanese", "ita": "Italian", "por": "Portuguese", "ara": "Arabic"}
    res = []
    for iso in a.langues.split(","):
        for n in sorted(par.get(iso, {}))[: a.n]:
            texte = par[iso][n]
            ids = tok(texte, return_tensors="pt").to(dev)
            with torch.no_grad():
                logits = m(**ids).logits[0]
                logp = torch.log_softmax(logits, dim=-1)
                p = logp.exp()
                H = -(p * logp).sum(-1) / math.log(p.shape[-1])       # entropie normalisée ✓
            H = H.cpu().numpy()
            # la langue probable : distribution sur les noms candidats au PREMIER token ✓
            demande = f"What language is this text?\n\n{texte[:400]}\n\nLanguage:"
            did = tok(demande, return_tensors="pt").to(dev)
            with torch.no_grad():
                lp = torch.log_softmax(m(**did).logits[0, -1], dim=-1)
            probs = {}
            for code, nom in NOMS.items():
                tid = tok(" " + nom, add_special_tokens=False).input_ids
                if tid:
                    probs[code] = float(lp[tid[0]].exp())
            tot = sum(probs.values()) or 1.0
            probs = {k: v / tot for k, v in probs.items()}
            best = max(probs, key=probs.get)
            res.append({"iso3": iso, "article": n, "tokens": int(len(ids["input_ids"][0])),
                        "entropie_moyenne": float(H.mean()), "entropie_max": float(H.max()),
                        "tokens_ambigus": float((H > a.seuil).mean()),
                        "langue_probable": best, "proba_langue": probs[best], "probas": probs})
            print(f"  {iso} art.{n:2d} · {len(ids['input_ids'][0]):3d} tokens · entropie {H.mean():.3f} "
                  f"· ambigus {(H > a.seuil).mean():.1%} · langue {best} {probs[best]:.2f}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

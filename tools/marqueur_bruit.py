#!/usr/bin/env python3
"""marqueur_bruit.py — LE SENS EXTRAIT PORTE SON BRUIT (AGENTS.md §7, règle 3), mesuré en bits par CARACTÈRE.

LES DEUX ERREURS DE LA PREMIÈRE VERSION ✗✗, et ce qu'elles m'ont appris :
  1. je mesurais l'**entropie** de la distribution ✓✗ (« combien le modèle hésite avant de voir le token ») au
     lieu de la **surprisal du token réel** ✓✓ (« combien le token a coûté ») : −log₂ p(w_t) ✓. C'est la seule
     mesure qui s'additionne en bits ✓.
  2. je comparais des entropies **par token** ✗✗ : un token chinois porte 2 à 3 caractères, un token français
     moins d'un demi-mot ✓✗ — la comparaison entre langues était un **artefact de tokenisation** ✓✓. On divise
     donc par la longueur (en caractères) du token ✓ : **bits par caractère** ✓✓.
  3. et ma consigne de langue (« Language: texte ») faisait **continuer** le texte ✗✗ : le modèle répondait « c »,
     « is », « 他們 » ✓✗. On passe par le **gabarit de conversation** du modèle instruct ✓✓ et on lit le premier
     token de sa réponse ✓.

TROIS MARQUEURS ✗ : **bits par caractère** ✓ (surprisal moyenne ✓), **tokens coûteux** (surprisal > 4 bits ✓),
**langue répondue** (premier token de la réponse, avec sa probabilité ✓).
"""
from __future__ import annotations
import argparse, json, math, pathlib
import numpy as np


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--langues", default="fra,eng,cmn")
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--seuil", type=float, default=4.0)
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
    res = []
    for iso in a.langues.split(","):
        for n in sorted(par.get(iso, {}))[: a.n]:
            texte = par[iso][n]
            ids = tok(texte, return_tensors="pt").to(dev)
            with torch.no_grad():
                logp = torch.log_softmax(m(**ids).logits[0], dim=-1)
            cibles = ids["input_ids"][0][1:]
            surprisal = (-logp[:-1].gather(1, cibles.unsqueeze(1)).squeeze(1) / math.log(2)).cpu().numpy()
            longueurs = np.array([max(1, len(tok.decode([int(t)]))) for t in cibles])
            # ⚠️ LES BITS PAR CARACTÈRE NE SONT PAS COMPARABLES ENTRE ÉCRITURES ✗✗ : un caractère chinois porte
            # un mot, une lettre latine un morceau de mot ✓✗. L'unité juste est **bits par TOKEN** ✓✓ (la
            # tokenisation est adaptée à chaque écriture ✓) — et le **total** de bits pour le texte ✓.
            bits_par_token = float(surprisal.mean())
            bits_total = float(surprisal.sum())
            # la langue : gabarit de conversation ✓✓, réponse en un mot ✓
            messages = [{"role": "user", "content": "In one word, what language is this text written in? "
                                                     "Answer with the language name only.\n\n" + texte[:400]}]
            prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            did = tok(prompt, return_tensors="pt").to(dev)
            with torch.no_grad():
                lg = torch.log_softmax(m(**did).logits[0, -1], dim=-1)
            rep = int(lg.argmax())
            langue = tok.decode([rep]).strip().lower() or "?"
            res.append({"iso3": iso, "article": n, "tokens": int(len(cibles)),
                        "bits_par_token": bits_par_token, "bits_total": bits_total,
                        "tokens_couteux": float((surprisal > a.seuil).mean()),
                        "langue_repondue": langue, "proba_reponse": float(lg[rep].exp())})
            print(f"  {iso} art.{n:2d} · {len(cibles):3d} tokens · {bits_par_token:5.2f} bits/token "
                  f"· {bits_total:6.0f} bits · "
                  f"coûteux {(surprisal > a.seuil).mean():.1%} · langue « {langue} » ({float(lg[rep].exp()):.2f})")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

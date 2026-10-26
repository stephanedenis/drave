#!/usr/bin/env python3
"""mesure.py — ce que le banc DeepSeek coûte et ce qu'il rend.

Deux mesures, sans dépendance :
- **coût** : tokens d'entrée/sortie, latence, taux de cache ;
- **qualité des traductions** : chrF (n-grammes de caractères, β=2) contre la
  traduction humaine officielle de l'UDHR, avec le **plancher** source→référence
  (le même chrF sans traduction). On ne prétend pas mesurer « la compréhension » :
  on mesure une reproduction de traduction humaine sur cinq articles publics.

Les entrées `dry_run` sont ignorées : elles ne sont pas des sorties du professeur.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
from collections import Counter, defaultdict


def chrf(hyp: str, ref: str, n_max: int = 6, beta: float = 2.0) -> float:
    from collections import Counter
    hyp = " ".join(hyp.split())
    ref = " ".join(ref.split())
    if not hyp or not ref:
        return 0.0
    prec, rec = [], []
    for n in range(1, n_max + 1):
        H = [hyp[i:i + n] for i in range(max(0, len(hyp) - n + 1))]
        R = [ref[i:i + n] for i in range(max(0, len(ref) - n + 1))]
        ch, cr = Counter(H), Counter(R)
        inter = sum((ch & cr).values())
        if not R:
            # un ordre plus grand que la référence n'existe pas : on ne le
            # compte pas comme un zéro (sinon « abc » contre « abc » vaudrait 50).
            continue
        prec.append(inter / max(1, len(H)))
        rec.append(inter / max(1, len(R)))
    p = sum(prec) / len(prec)
    r = sum(rec) / len(rec)
    b2 = beta * beta
    return 100 * (1 + b2) * p * r / max(1e-9, b2 * p + r)


def lire(chemin: str | pathlib.Path) -> list[dict]:
    out = []
    for ligne in pathlib.Path(chemin).read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        try:
            d = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if d.get("dry_run") or not d.get("reponse"):
            continue
        out.append(d)
    return out


def mesure(chemin: str | pathlib.Path) -> dict:
    entrees = lire(chemin)
    if not entrees:
        return {"exemples": 0, "vide": True}
    latences = [float(d.get("latence_s", 0.0)) for d in entrees]
    tokens_in = sum(int((d.get("usage") or {}).get("prompt_tokens", 0)) for d in entrees)
    tokens_out = sum(int((d.get("usage") or {}).get("completion_tokens", 0)) for d in entrees)
    caches = sum(1 for d in entrees if d.get("cache"))
    par_langue: dict[str, list[float]] = defaultdict(list)
    planchers: dict[str, list[float]] = defaultdict(list)
    jeux = 0
    for d in entrees:
        meta = d.get("meta") or {}
        if meta.get("categorie") != "traduction":
            jeux += 1
            continue
        ref = meta.get("reference") or ""
        source = d.get("prompt", "").split("\n\n", 1)[-1]
        langue = meta.get("cible_iso3") or "?"
        par_langue[langue].append(chrf(d.get("reponse", ""), ref))
        planchers[langue].append(chrf(source, ref))
    scores = [x for v in par_langue.values() for x in v]
    plans = [x for v in planchers.values() for x in v]
    source = pathlib.Path(chemin)
    return {
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest() if source.is_file() else "",
        "exemples": len(entrees),
        "traductions": len(scores),
        "jeux": jeux,
        "tokens_entree": tokens_in,
        "tokens_sortie": tokens_out,
        "latence_moyenne_s": round(sum(latences) / len(latences), 3),
        "caches": caches,
        "chrF_moyen": round(sum(scores) / len(scores), 2) if scores else None,
        "chrF_plancher": round(sum(plans) / len(plans), 2) if plans else None,
        "par_langue": {l: {"n": len(v), "chrF": round(sum(v) / len(v), 2),
                           "plancher": round(sum(planchers[l]) / len(planchers[l]), 2)}
                       for l, v in sorted(par_langue.items())},
        "modeles": dict(Counter(d.get("modele", "?") for d in entrees)),
    }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--entree", default="data/deepseek/enseignant.jsonl")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    r = mesure(a.entree)
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n",
                                        encoding="utf-8")
    print(json.dumps(r, ensure_ascii=False, indent=1))
    raise SystemExit(0 if not r.get("vide") else 1)

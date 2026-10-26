#!/usr/bin/env python3
"""enseignant.py — construire le corpus du professeur DeepSeek.

Le corpus est un **JSONL** : chaque ligne porte le prompt, la réponse du professeur,
l'usage (tokens), la latence et le cache. Il ne contient **aucune clé**. Les
réponses peuvent ensuite servir à entraîner/distiller l'élève natif `route`
(autorisation explicite de la licence DeepSeek).

Le script est **reprenable** : une ligne déjà présente n'est pas redemandée. Le
mode `--dry-run` ne fait aucune requête : il écrit des réponses factices, que
`distillation.py` ignore — un dry-run ne doit jamais devenir un corpus
d'entraînement.

Usage :
    python3 tools/llm/enseignant.py --prompts tools/llm/prompts_publics.jsonl \
        --sortie data/deepseek/enseignant.jsonl --limite 5 --dry-run
    DEEPSEEK_API_KEY=... python3 tools/llm/enseignant.py \
        --prompts tools/llm/prompts_publics.jsonl --sortie data/deepseek/enseignant.jsonl
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

if __package__:
    from .deepseek import DeepSeek, ErreurDeepSeek
else:  # exécution directe : python3 tools/llm/enseignant.py
    from deepseek import DeepSeek, ErreurDeepSeek


def charger_prompts(chemin: str | pathlib.Path) -> list[dict]:
    prompts = []
    for ligne in pathlib.Path(chemin).read_text(encoding="utf-8").splitlines():
        if ligne.strip():
            prompts.append(json.loads(ligne))
    return prompts


def _deja_faits(chemin: pathlib.Path, dry_run: bool) -> set[str]:
    if not chemin.is_file():
        return set()
    faits = set()
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        try:
            d = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if bool(d.get("dry_run")) == dry_run:
            faits.add(d.get("id", ""))
    return faits


def generer(prompts: list[dict], sortie: str | pathlib.Path, client: DeepSeek,
            *, dry_run: bool = False, limite: int | None = None,
            reprise: bool = True, temperature: float = 0.0,
            max_tokens: int = 1024, cache: bool = True,
            ecraser: bool = False) -> dict:
    chemin = pathlib.Path(sortie)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    if ecraser and chemin.is_file():
        chemin.unlink()
    faits = _deja_faits(chemin, dry_run) if reprise and not ecraser else set()
    a_faire = [p for p in prompts if p["id"] not in faits]
    if limite is not None:
        a_faire = a_faire[:limite]
    stats = {"demandes": 0, "reussies": 0, "echecs": 0,
             "tokens_entree": 0, "tokens_sortie": 0,
             "latence_s": 0.0, "caches": 0, "dry_run": dry_run}
    with chemin.open("a", encoding="utf-8") as f:
        for p in a_faire:
            stats["demandes"] += 1
            try:
                r = client.demande(p["prompt"], system=p.get("system"),
                                   temperature=temperature, max_tokens=max_tokens,
                                   dry_run=dry_run, cache=cache)
            except ErreurDeepSeek as e:
                stats["echecs"] += 1
                print(f"  échec {p['id']} : {e}", file=sys.stderr)
                continue
            usage = r.usage or {}
            stats["reussies"] += 1
            stats["tokens_entree"] += int(usage.get("prompt_tokens", 0))
            stats["tokens_sortie"] += int(usage.get("completion_tokens", 0))
            stats["latence_s"] += float(r.latence_s)
            stats["caches"] += int(r.cache)
            ligne = {
                "id": p["id"],
                "system": p.get("system"),
                "prompt": p["prompt"],
                "reponse": r.contenu,
                "raisonnement": r.raisonnement,
                "usage": usage,
                "latence_s": r.latence_s,
                "cache": r.cache,
                "modele": r.modele,
                "dry_run": dry_run,
                "recu_le": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "meta": p.get("meta", {}),
            }
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
            f.flush()
    stats["latence_s"] = round(stats["latence_s"], 3)
    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description="le corpus du professeur DeepSeek")
    ap.add_argument("--prompts", default=str(pathlib.Path(__file__).with_name("prompts_publics.jsonl")))
    ap.add_argument("--sortie", default="data/deepseek/enseignant.jsonl")
    ap.add_argument("--limite", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ecraser", action="store_true")
    ap.add_argument("--sans-cache", action="store_true")
    ap.add_argument("--modele", default=None)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--max-tokens", type=int, default=1024)
    args = ap.parse_args()
    prompts = charger_prompts(args.prompts)
    client = DeepSeek(modele=args.modele)
    stats = generer(prompts, args.sortie, client, dry_run=args.dry_run,
                    limite=args.limite, cache=not args.sans_cache,
                    temperature=args.temperature, max_tokens=args.max_tokens,
                    ecraser=args.ecraser)
    print(json.dumps(stats, ensure_ascii=False, indent=1))
    return 0 if stats["echecs"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

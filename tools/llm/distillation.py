#!/usr/bin/env python3
"""distillation.py — du corpus DeepSeek au corpus d'entraînement de `route`.

DeepSeek ne donne pas ses logits : la distillation est **au niveau des
séquences**. On transforme chaque réponse du professeur en un texte que le
modèle natif (byte-level, `entrainer_moteur.py`) sait lire, avec un découpage
**train / validation par identifiant** — pas par ligne, pour qu'aucun exemple ne
fuite d'un côté à l'autre.

Les entrées `dry_run` sont **ignorées** : un faux professeur ne doit jamais
devenir un corpus d'entraînement. Le corpus produit est dans `data/` (gitignoré) ;
seul le code est versionné.

Usage :
    python3 tools/llm/distillation.py --entree data/deepseek/enseignant.jsonl \
        --sortie data/deepseek/distillation
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import time


def lire_enseignant(chemin: str | pathlib.Path) -> list[dict]:
    vus: dict[str, dict] = {}
    for ligne in pathlib.Path(chemin).read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        try:
            d = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if d.get("dry_run") or not d.get("reponse"):
            continue
        vus[d["id"]] = d
    return list(vus.values())


def _exemple(d: dict, reponse_seule: bool) -> str:
    if reponse_seule:
        return f"### professeur\n{d['reponse'].strip()}\n"
    system = (d.get("system") or "").strip()
    return (f"### system\n{system}\n### user\n{d['prompt'].strip()}\n"
            f"### professeur\n{d['reponse'].strip()}\n")


def _est_validation(ident: str) -> bool:
    return int(hashlib.sha256(ident.encode("utf-8")).hexdigest(), 16) % 10 == 0


def construire(entree: str | pathlib.Path, sortie: str | pathlib.Path,
               *, reponse_seule: bool = False, min_caracteres: int = 0,
               max_caracteres: int | None = None, permuter: bool = False) -> dict:
    exemples = lire_enseignant(entree)
    if permuter:
        # Contrôle négatif : mêmes prompts, réponses **mélangées**. L'élève ne
        # peut pas apprendre la bonne réponse ; sa validation doit être pire.
        ids_val = {d["id"] for d in exemples if _est_validation(d["id"])}
        entrain = [d for d in exemples if d["id"] not in ids_val]
        reponses = [d["reponse"] for d in entrain]
        random.Random(0).shuffle(reponses)
        remplace = {d["id"]: r for d, r in zip(entrain, reponses)}
        exemples = [dict(d, reponse=remplace.get(d["id"], d["reponse"]))
                    for d in exemples]
    train: list[str] = []
    val: list[str] = []
    for d in sorted(exemples, key=lambda x: x["id"]):
        texte = _exemple(d, reponse_seule)
        if len(texte) < min_caracteres:
            continue
        if max_caracteres is not None:
            texte = texte[:max_caracteres]
        (val if _est_validation(d["id"]) else train).append(texte)
    # au moins un exemple de validation quand il y a de quoi
    if not val and len(train) >= 5:
        val.append(train.pop())
    dossier = pathlib.Path(sortie)
    dossier.mkdir(parents=True, exist_ok=True)
    (dossier / "train.txt").write_text("\n".join(train) + ("\n" if train else ""),
                                       encoding="utf-8")
    (dossier / "val.txt").write_text("\n".join(val) + ("\n" if val else ""),
                                     encoding="utf-8")
    source = pathlib.Path(entree).read_bytes() if pathlib.Path(entree).is_file() else b""
    meta = {
        "source": str(entree),
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "exemples": len(train) + len(val),
        "train": len(train),
        "val": len(val),
        "caracteres_train": sum(len(x) for x in train),
        "caracteres_val": sum(len(x) for x in val),
        "reponse_seule": reponse_seule,
        "permute": permuter,
        "modeles": sorted({d.get("modele", "") for d in exemples if d.get("modele")}),
        "date": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    (dossier / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n",
                                       encoding="utf-8")
    return meta


def main() -> int:
    ap = argparse.ArgumentParser(description="corpus de distillation pour le modèle natif")
    ap.add_argument("--entree", default="data/deepseek/enseignant.jsonl")
    ap.add_argument("--sortie", default="data/deepseek/distillation")
    ap.add_argument("--reponse-seule", action="store_true")
    ap.add_argument("--min-caracteres", type=int, default=0)
    ap.add_argument("--max-caracteres", type=int, default=None)
    ap.add_argument("--permuter", action="store_true",
                    help="contrôle négatif : mélanger les réponses entre prompts")
    args = ap.parse_args()
    meta = construire(args.entree, args.sortie, reponse_seule=args.reponse_seule,
                      min_caracteres=args.min_caracteres,
                      max_caracteres=args.max_caracteres, permuter=args.permuter)
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    return 0 if meta["exemples"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

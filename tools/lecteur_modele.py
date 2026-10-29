#!/usr/bin/env python3
"""lecteur_modele.py — R0.3 : un modèle lit le contexte que le contrôleur a sélectionné.

POURQUOI CE FICHIER. Le lecteur extractif de R0.2 plafonne : même en lisant tout, il ne
trouve la valeur que dans 25 à 75 % des cas. La question de R0.3 est donc : ce plafond est-il
celui du **lecteur**, ou celui du **document** ? On branche un modèle qui lit le contexte
sélectionné et on compare, à fenêtre égale, trois façons de remplir la fenêtre :

  - **le contrôleur** : les passages qu'il a choisis (R0.2), par score ;
  - **le début** : les premiers passages du document, dans l'ordre de lecture — ce que fait un
    lecteur naïf quand le document ne tient pas dans la fenêtre ;
  - **le hasard** : des passages tirés au sort, même budget.

**Le GPU, pas le CPU.** Le moteur Drave exécute `--infer` sur le CPU (20 fils) : mesurer un
lecteur avec lui saturait la machine (~38 cœurs quand deux bancs tournaient) pour 30 jetons/s.
`llama-cli` a un build CUDA et lit le même GGUF à **1 409 t/s** de prompt et **273 t/s** de
génération. On garde donc le CPU pour le moteur et les portes, et le GPU pour ce banc — un seul
GPU (`CUDA_VISIBLE_DEVICES=0`), l'autre reste à N2.

La génération est **greedy** (`--temp 0`) : rejouable.

Usage :
  python3 tools/lecteur_modele.py --question "…" --contexte /tmp/contexte.txt
  python3 tools/lecteur_modele.py --autotest
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
BINAIRE = shutil.which("llama-cli") or "llama-cli"
MODELE = RACINE / "models/Qwen2.5-0.5B-Q8_0.gguf"
CONTEXTE_MAX = 1200  # caractères : ~300 jetons, sous la fenêtre
JETONS = 24
GPU = os.environ.get("LECTEUR_GPU", "0")  # un seul GPU : l'autre reste à N2


def generer(prompt: str, jetons: int = JETONS) -> tuple[str, float]:
    """Une génération greedy sur GPU. Rend le texte et la durée murale."""
    debut = time.time()
    environnement = dict(os.environ, CUDA_VISIBLE_DEVICES=GPU)
    sortie = subprocess.run(
        [BINAIRE, "-m", str(MODELE), "-p", prompt, "-n", str(jetons),
         "--temp", "0", "-ngl", "99", "-t", "4",
         "--no-warmup", "--single-turn"],
        capture_output=True, text=True, timeout=600, env=environnement,
        stdin=subprocess.DEVNULL,
    )
    duree = time.time() - debut
    if sortie.returncode != 0:
        raise RuntimeError(f"llama-cli a échoué : {sortie.stderr[-400:]}")
    return sortie.stdout, duree


def extrait(texte: str, prompt: str) -> str:
    """La réponse est ce que le modèle ajoute au prompt. llama.cpp imprime un bandeau PUIS
    l'écho du prompt — tronqué quand il est long. On borde donc la sortie par la fin
    (« [ Prompt: », « Exiting »), puis on coupe après le dernier marqueur d'écho connu :
    la troncature, ou la fin du prompt. Si aucun n'est présent, on ne rend RIEN — mieux vaut
    une réponse vide qu'un bandeau compté comme une réponse (c'est ce qui a fait marquer
    « hasard » à tort au premier passage)."""
    for coupe in ("\n[ Prompt:", "\nExiting", "<|endoftext|>"):
        texte = texte.split(coupe)[0]
    for marqueur in ("... (truncated)", prompt[-60:], prompt[-30:], "Réponse :"):
        if marqueur and marqueur in texte:
            return texte.rsplit(marqueur, 1)[1].strip()
    return ""


def repondre(question: str, passages: list[dict], max_caracteres: int = CONTEXTE_MAX) -> dict:
    """Le modèle lit les passages dans l'ordre reçu, et répond. Le contexte est borné par la
    fenêtre, pas par le budget : c'est la fenêtre qui décide de ce qui tient."""
    contexte = "\n".join(p["texte"] for p in passages)[:max_caracteres]
    prompt = f"Contexte : {contexte}\nQuestion : {question}\nRéponse :"
    brut, duree = generer(prompt)
    return {"texte": extrait(brut, prompt), "brut": brut[-200:], "duree_s": round(duree, 2),
            "caracteres": len(contexte), "gpu": GPU}


def autotest() -> int:
    """Un contrôle qui doit PASSER et un qui doit ÉCHOUER : le modèle trouve la valeur quand
    elle est dans le contexte, et il ne l'invente pas quand elle n'y est pas."""
    question = "Combien d'octets coûte le mode dense par flux ?"
    r = repondre(question, [{"texte": "Le mode dense coûte 3 663 octets par flux (79 d'en-tête + 896 × 4)."}])
    trouve = "3663" in re.sub(r"\s+", "", r["texte"]) or "3 663" in r["texte"]
    print(f"avec contexte : {r['texte'][:80]!r} → {'trouvé' if trouve else 'NON trouvé'} ({r['duree_s']} s, GPU {r['gpu']})")
    r2 = repondre(question, [{"texte": "Le ciel est bleu et la terre est verte."}])
    invente = "3663" in re.sub(r"\s+", "", r2["texte"]) or "3 663" in r2["texte"]
    print(f"sans contexte : {r2['texte'][:80]!r} → {'INVENTÉ' if invente else 'pas inventé'} ({r2['duree_s']} s)")
    return 0 if trouve and not invente else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="R0.3 — le lecteur modèle (GPU).")
    ap.add_argument("--question")
    ap.add_argument("--contexte", type=pathlib.Path)
    ap.add_argument("--autotest", action="store_true")
    args = ap.parse_args()
    if args.autotest:
        return autotest()
    if not args.question:
        ap.error("--question est requis")
    passages = [{"texte": args.contexte.read_text(encoding="utf-8")}] if args.contexte else []
    r = repondre(args.question, passages)
    print(f"réponse : {r['texte']}")
    print(f"durée : {r['duree_s']} s · contexte : {r['caracteres']} caractères · GPU {r['gpu']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""lecteur_modele.py — R0.3 : un modèle lit le contexte que le contrôleur a sélectionné.

POURQUOI CE FICHIER. Le lecteur extractif de R0.2 plafonne : même en lisant tout, il ne
trouve la valeur que dans 25 à 75 % des cas. La question de R0.3 est donc : ce plafond est-il
celui du **lecteur**, ou celui du **document** ? On branche un modèle qui lit le contexte
sélectionné et on compare, à fenêtre égale, trois façons de remplir la fenêtre :

  - **le contrôleur** : les passages qu'il a choisis (R0.2) ;
  - **le début** : les premiers passages du document, dans l'ordre de lecture — ce que fait
    un lecteur naïf quand le document ne tient pas dans la fenêtre ;
  - **le hasard** : des passages tirés au sort, même budget.

Si le contrôleur bat le début et le hasard, la sélection compte. S'il ne les bat pas, elle ne
sert à rien et il faut le dire.

Le modèle est **Qwen2.5-0.5B**, exécuté par le moteur Drave (`--infer --temp 0`) : aucune
API, aucun réseau, et le même moteur que le reste du dépôt. La génération est **greedy**,
donc rejouable.

Usage :
  python3 tools/lecteur_modele.py --question "…" --contexte /tmp/contexte.txt
  python3 tools/lecteur_modele.py --autotest
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
BINAIRE = RACINE / "drave-core/target/release/drave"
MODELE = RACINE / "models/Qwen2.5-0.5B-Q8_0.gguf"
CONTEXTE_MAX = 1200  # caractères : ~300 jetons, sous la fenêtre de 512
JETONS = 24


def generer(prompt: str, jetons: int = JETONS, ctx: int = 512) -> tuple[str, float]:
    """Une génération greedy. Rend le texte et la durée murale (l'instrument, pas le résultat)."""
    import time
    debut = time.time()
    sortie = subprocess.run(
        [str(BINAIRE), str(MODELE), "--infer", "--prompt", prompt,
         "--n", str(jetons), "--temp", "0", "--ctx", str(ctx)],
        capture_output=True, text=True, timeout=600,
    )
    duree = time.time() - debut
    if sortie.returncode != 0:
        raise RuntimeError(f"le moteur a échoué : {sortie.stderr[-400:]}")
    texte = sortie.stdout
    if "--- texte ---" in texte:
        texte = texte.split("--- texte ---", 1)[1].split("--- ids générés", 1)[0]
    return texte, duree


def extrait(texte: str, prompt: str) -> str:
    """La réponse est ce qui suit le dernier « Réponse : » — le moteur rend le prompt avec.
    On coupe au premier arrêt naturel : fin de ligne, jeton de fin, ou tour de dialogue."""
    if "Réponse :" in texte:
        texte = texte.rsplit("Réponse :", 1)[1]
    elif len(prompt) < len(texte):
        texte = texte[len(prompt):]
    for coupe in ("<|endoftext|>", "\n", "Human:", "Question :", "Contexte :"):
        texte = texte.split(coupe)[0]
    return texte.strip()


def repondre(question: str, passages: list[dict], max_caracteres: int = CONTEXTE_MAX) -> dict:
    """Le modèle lit les passages, dans l'ordre de lecture, et répond. Le contexte est borné
    par la fenêtre, pas par le budget : c'est la fenêtre qui décide de ce qui tient."""
    contexte = "\n".join(p["texte"] for p in passages)[:max_caracteres]
    prompt = f"Contexte : {contexte}\nQuestion : {question}\nRéponse :"
    brut, duree = generer(prompt)
    return {"texte": extrait(brut, prompt), "brut": brut[-300:], "duree_s": round(duree, 2),
            "caracteres": len(contexte)}


def autotest() -> int:
    """Un contrôle qui doit PASSER et un qui doit ÉCHOUER : le modèle trouve la valeur quand
    elle est dans le contexte, et il ne l'invente pas quand elle n'y est pas."""
    contexte = ("Le mode dense coûte 3 663 octets par flux (79 d'en-tête + 896 × 4). "
                "Le mode liste coûte 79 + 4 × le nombre d'actifs.")
    question = "Combien d'octets coûte le mode dense par flux ?"
    p = [{"texte": contexte}]
    r = repondre(question, p)
    trouve = "3663" in re.sub(r"\s+", "", r["texte"]) or "3 663" in r["texte"]
    print(f"avec contexte  : {r['texte'][:90]!r} → {'trouvé' if trouve else 'NON trouvé'} ({r['duree_s']} s)")
    r2 = repondre(question, [{"texte": "Le ciel est bleu et la terre est verte."}])
    invente = "3663" in re.sub(r"\s+", "", r2["texte"]) or "3 663" in r2["texte"]
    print(f"sans contexte  : {r2['texte'][:90]!r} → {'INVENTÉ' if invente else 'pas inventé'} ({r2['duree_s']} s)")
    return 0 if trouve and not invente else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="R0.3 — le lecteur modèle.")
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
    print(f"durée : {r['duree_s']} s · contexte : {r['caracteres']} caractères")
    return 0


if __name__ == "__main__":
    sys.exit(main())

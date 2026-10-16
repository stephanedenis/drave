#!/usr/bin/env python3
"""chat.py — PARLER À DRAVE : le point d'entrée qui manquait.

POURQUOI CE FICHIER EXISTE. Le moteur sait déjà converser ✓ — mais pour l'utiliser il fallait
**découvrir** trois choses en lisant la source ✗ :
  1. `--chat` **seul ne fait rien** ✗ : le gabarit de conversation n'est appliqué que si `--prompt` est
     fourni ✓ (sans lui, le moteur retombe sur un **banc de mesure** ✗✓ — mesuré le 16/10 : la commande
     a affiché « Taille exacte des encodages » au lieu de répondre ✓) ;
  2. **il n'existe AUCUN mode silencieux** ✗ : le moteur imprime sa télémétrie (paires poids × activation,
     densités, postes par token ✓) **après** la réponse ✓ — donc la réponse existe, mais elle est noyée ✗ ;
  3. il n'y a **pas de `--aide`** ✗ (un drapeau inconnu est signalé « sans effet » ✓ — c'est bien ✓ —
     mais rien ne dit ce qui existe ✓).
Ce script ne remplace pas le moteur ✗ : il lui parle **correctement** ✓ et ne montre que la réponse ✓.

CE QU'IL FAIT :
  · il tient la **conversation** (le gabarit Qwen est construit ici, tour par tour ✓ — le moteur reçoit
    l'invite complète ✓, sans `--chat` ✗, pour ne pas l'emballer deux fois ✓) ;
  · il **coupe la télémétrie** ✓ (tout ce qui suit la ligne « --- mesure --- » ✓) ;
  · il garde les commandes utiles : `/aide`, `/reset`, `/temp 0.7`, `/n 256`, `/ctx 2048`, `/system …`,
    `/quitter` ✓.

Usage :
  python3 tools/chat.py [--modele models/Qwen2.5-0.5B-Q8_0.gguf] [--ctx 2048] [--n 256] [--temp 0.7]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
DEBUT_ASSISTANT = "<|im_start|>assistant\n"


def gabarit(systeme: str, tours: list[tuple[str, str]]) -> str:
    """Le gabarit de conversation Qwen2.5 ✓ — construit ICI, pour que l'historique complet parte au
    moteur sans qu'il l'emballe une seconde fois ✗."""
    t = f"<|im_start|>system\n{systeme}<|im_end|>\n"
    for role, texte in tours:
        t += f"<|im_start|>{role}\n{texte}<|im_end|>\n"
    return t + DEBUT_ASSISTANT


def repondre(moteur: str, modele: str, invite: str, ctx: int, n: int, temp: float, threads: int) -> str:
    r = subprocess.run([moteur, modele, "--infer", "--prompt", invite, "--n", str(n),
                        "--ctx", str(ctx), "--threads", str(threads), "--temp", str(temp)],
                       capture_output=True, text=True, timeout=3600)
    corps = r.stdout + r.stderr
    # ⚠️ L'ORDRE COMPTE, ET LE PREMIER ESSAI S'EST TROMPÉ ✗. Le moteur imprime sa configuration
    # (`[config]`, `[modele]`) AVANT tout ✓ — couper au premier marqueur d'instrumentation **du texte
    # entier** coupait donc tout ✗✓ (résultat : « pas de réponse » ✓). On fait l'inverse :
    #   1. on repère le DERNIER `\n<|im_start|>assistant\n` ✓ (l'invite est ré-échographiée par le
    #      moteur ✓, donc le dernier est celui de la vraie réponse ✓) ;
    #   2. **puis** on coupe à la première instrumentation QUI SUIT ce point ✓.
    i = corps.rfind(DEBUT_ASSISTANT)
    corps = corps[i + len(DEBUT_ASSISTANT):] if i >= 0 else corps
    MARQUEURS = ("--- mesure ---", "--- ids générés", "événements :", "paires (poids × activation)",
                 "[tete]", "postes (ms/token)", "\n[", "\nvous >")
    coupe = len(corps)
    for mq in MARQUEURS:
        k = corps.find(mq)
        if k >= 0:
            coupe = min(coupe, k)
    corps = corps[:coupe]
    # ET ON COUPE AU MARQUEUR DE FIN ✗ : sans `--chat`, le moteur **ne s'arrête pas** à `<|im_end|>` ✗
    # (c'est `--chat` qui pose `stop_id` ✓) — il continue donc à écrire le tour SUIVANT, gabarit
    # compris ✓✗ (mesuré : « …est "chevaux". |/|>system Tu es un assistant utile… » ✗). Le premier
    # marqueur de fin est la vraie fin de la réponse ✓.
    # ⚠️ ET LE MARQUEUR DE FIN ARRIVE **MALTRAITÉ** ✗ : mesuré, le modèle écrit « |/|> » là où le
    # gabarit attend « <|im_end|> » ✓ — c'est un jeton spécial que la quantification rend approximatif ✓,
    # et couper sur la seule forme propre laissait passer le tour suivant ✗✓. On coupe donc sur les
    # DEUX formes ✓, et sur les débris de gabarit qui les accompagnent ✓.
    for fin in ("<|im_end|>", "<|endoftext|>", "<|im_start|>", "|/|>", "|>system", "<|im_start|>"):
        k = corps.find(fin)
        if k >= 0:
            corps = corps[:k]
    corps = corps.strip()
    return corps or "(pas de réponse — voir la sortie brute avec /brut)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default=str(RACINE / "models" / "Qwen2.5-0.5B-Q8_0.gguf"))
    ap.add_argument("--moteur", default=str(RACINE / "drave-core" / "target" / "release" / "drave"))
    ap.add_argument("--ctx", type=int, default=2048)
    ap.add_argument("--n", type=int, default=256, help="jetons à générer par réponse")
    ap.add_argument("--temp", type=float, default=0.7)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--systeme", default="Tu es un assistant utile. Réponds en français, brièvement.")
    a = ap.parse_args()

    if not pathlib.Path(a.modele).exists():
        sys.exit(f"modèle absent : {a.modele}\n(les modèles disponibles sont dans models/ ✓)")
    if not pathlib.Path(a.moteur).exists():
        sys.exit(f"moteur absent : {a.moteur}\n(construire : cargo build --release --manifest-path drave-core/Cargo.toml)")

    print(f"Drave — {pathlib.Path(a.modele).name} · ctx {a.ctx} · n {a.n} · temp {a.temp}")
    print("commandes : /aide · /reset · /temp X · /n X · /ctx X · /system TEXTE · /brut · /quitter")
    print()
    tours: list[tuple[str, str]] = []
    systeme = a.systeme
    brut = False
    while True:
        try:
            ligne = input("vous > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not ligne:
            continue
        if ligne.startswith("/"):
            cmd, _, arg = ligne[1:].partition(" ")
            if cmd in ("quitter", "q", "exit"):
                break
            if cmd == "aide":
                print("  /reset            repartir de zéro")
                print("  /system TEXTE     changer la consigne système")
                print("  /temp X · /n X · /ctx X   régler la génération")
                print("  /brut             montrer la sortie BRUTE du moteur (télémétrie comprise)")
                print("  /quitter")
                continue
            if cmd == "reset":
                tours.clear(); print("  (conversation remise à zéro)"); continue
            if cmd == "system":
                systeme = arg; print("  (consigne système changée)"); continue
            if cmd in ("temp", "n", "ctx"):
                try:
                    v = float(arg); v = int(v) if cmd in ("n", "ctx") else v
                except ValueError:
                    print(f"  valeur invalide : {arg}"); continue
                setattr(a, {"temp": "temp", "n": "n", "ctx": "ctx"}[cmd], v)
                print(f"  {cmd} = {v}"); continue
            if cmd == "brut":
                brut = not brut; print(f"  sortie brute : {'OUI' if brut else 'non'}"); continue
            print(f"  commande inconnue : /{cmd} (essaie /aide)"); continue

        tours.append(("user", ligne))
        invite = gabarit(systeme, tours)
        try:
            rep = repondre(a.moteur, a.modele, invite, a.ctx, a.n, a.temp, a.threads)
        except subprocess.TimeoutExpired:
            print("  (le moteur n'a pas répondu dans l'heure — réponse abandonnée)")
            tours.pop()
            continue
        tours.append(("assistant", rep))
        print(f"drave > {rep}" if not brut else rep)
        print()
    print("à bientôt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

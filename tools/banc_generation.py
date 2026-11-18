#!/usr/bin/env python3
"""banc_generation.py — le banc de génération du modèle natif (diagnostic, pas un produit).

POURQUOI. Le modèle natif (`drave-n0`, 34 M) a une PPL de 2,40 mais l'archive dit
« cohérent 12 octets puis dérive ». Ce banc mesure ce que la PPL ne dit pas : sur
20 prompts fixes et trois réglages, la **qualité du texte produit** (mots réels,
diversité, répétition), la **vitesse** et la **mémoire**, avec un **contrôle
aléatoire** (la même architecture, poids au hasard) — sans lui, aucun chiffre ne
se lit.

CE QU'IL MESURE, PAR RÉGLAGE.
  - `octets` / `secondes` / `octets_s` : le débit de génération (byte-level) ;
  - `mots` : les mots décodés (UTF-8 avec remplacement) ;
  - `mots_valides` : la fraction des mots présents dans le vocabulaire du corpus
    (`data/wiki_mix/propre/train.txt`, les 50 000 formes les plus fréquentes) —
    le proxy de « ce sont des mots français » ;
  - `distinct_2` : la diversité (les bigrammes de mots distincts / total) ;
  - `repetition` : le plus grand nombre d'occurrences d'un trigramme (la dérive) ;
  - `echo` : la fraction du prompt recopiée telle quelle (greedy la produit souvent).

LE CONTRÔLE NÉGATIF. `--aleatoire` : la même architecture, les poids au hasard.
Ses mesures doivent être **franchement pires** sur les mots valides et la
répétition ; sinon le banc mesure le corpus, pas le modèle.

Usage :
  python3 tools/banc_generation.py --modele work/n2ac/mix1024-60k.pt \
      --sortie reports/banc-generation.json
  python3 tools/banc_generation.py --modele work/n2ac/mix1024-60k.pt --aleatoire
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys
import time

import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from tools.native_model import NativeConfig, NativeModel  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
CORPUS = RACINE / "data/wiki_mix/propre/train.txt"

PROMPTS = [
    "La France est un pays",
    "Dans les années 1950",
    "Il était une fois",
    "Le chat",
    "La mer",
    "Les enfants jouent",
    "Le gouvernement a décidé",
    "Paris est",
    "Un homme",
    "La musique",
    "Le livre",
    "La guerre",
    "L'économie",
    "Le sport",
    "La science",
    "La ville",
    "Le temps",
    "La vie",
    "Le monde",
    "La question",
]

REGLAGES = [
    {"nom": "greedy", "top_k": 0, "temperature": 0.0},
    {"nom": "top40_0.8", "top_k": 40, "temperature": 0.8},
    {"nom": "top20_0.5", "top_k": 20, "temperature": 0.5},
]


def charger(chemin: str, device: str = "cpu"):
    ck = torch.load(chemin, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items() if k in NativeConfig.__annotations__})
    m = NativeModel(cfg)
    m.load_state_dict(ck["state"])
    m.to(device).eval()
    return m, cfg


def charger_aleatoire(cfg: NativeConfig, graine: int = 1234):
    torch.manual_seed(graine)
    m = NativeModel(cfg)
    m.eval()
    return m


def vocabulaires(limite: int = 50_000) -> set[str]:
    """Les `limite` formes les plus fréquentes du corpus (le vocabulaire de référence)."""
    if not CORPUS.exists():
        return set()
    c = collections.Counter()
    with CORPUS.open("r", encoding="utf-8", errors="replace") as f:
        for ligne in f:
            c.update(ligne.split())
    return {m for m, _ in c.most_common(limite)}


def normaliser(mot: str) -> str:
    return mot.strip(".,;:!?«»\"'()[]{}…").lower()


def mesurer(texte: str, prompt: str, vocab: set[str]) -> dict:
    """Le texte **entier** (prompt + génération) ; l'echo se mesure sur la partie générée."""
    mots = [normaliser(m) for m in texte.split() if m.strip()]
    mots = [m for m in mots if m]
    valides = sum(1 for m in mots if m in vocab) / max(1, len(mots))
    bigrammes = list(zip(mots, mots[1:]))
    distinct_2 = len(set(bigrammes)) / max(1, len(bigrammes))
    trigrammes = collections.Counter(zip(mots, mots[1:], mots[2:]))
    repetition = max(trigrammes.values()) if trigrammes else 0
    # l'écho : la fraction des mots **générés** qui recopient le prompt
    generes = texte[len(prompt):] if texte.startswith(prompt) else texte
    mots_prompt = {normaliser(m) for m in prompt.split()}
    mots_gen = [normaliser(m) for m in generes.split() if m.strip()]
    echo = sum(1 for m in mots_gen if m in mots_prompt) / max(1, len(mots_gen))
    return {"mots": len(mots), "mots_valides": round(valides, 4),
            "distinct_2": round(distinct_2, 4), "repetition": repetition,
            "echo": echo}


@torch.no_grad()
def generer(modele, prompt: str, n: int, top_k: int, temperature: float) -> tuple[str, int]:
    ids = list(prompt.encode("utf-8"))
    debut = time.perf_counter()
    for _ in range(n):
        x = torch.tensor([ids[-modele.cfg.max_pos:]], dtype=torch.long,
                         device=modele.embed.weight.device)
        logits = modele(x)["logits"][0, -1]
        if temperature <= 0:
            suivant = int(logits.argmax())
        else:
            logits = logits / temperature
            if top_k > 0:
                v, i = logits.topk(min(top_k, logits.numel()))
                logits = torch.full_like(logits, float("-inf"))
                logits[i] = v
            suivant = int(torch.multinomial(torch.softmax(logits, -1), 1))
        ids.append(suivant)
        if suivant == 10 and len(ids) > len(prompt.encode("utf-8")):
            break
    duree = time.perf_counter() - debut
    return bytes(ids).decode("utf-8", "replace"), len(ids)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", required=True)
    ap.add_argument("--n", type=int, default=128)
    ap.add_argument("--sortie", default="")
    ap.add_argument("--aleatoire", action="store_true", help="le contrôle : poids au hasard")
    ap.add_argument("--limite-vocab", type=int, default=50_000)
    ap.add_argument("--device", default="cpu")
    a = ap.parse_args()

    vocab = vocabulaires(a.limite_vocab)
    if a.aleatoire:
        ck = torch.load(a.modele, map_location="cpu", weights_only=False)
        cfg = NativeConfig(**{k: v for k, v in ck["config"].items() if k in NativeConfig.__annotations__})
        modele = charger_aleatoire(cfg)
    else:
        modele, cfg = charger(a.modele, a.device)

    resultat = {"modele": a.modele, "aleatoire": bool(a.aleatoire), "n": a.n,
                "vocabulaire": len(vocab), "reglages": {}, "prompts": PROMPTS}
    for reglage in REGLAGES:
        lignes, t0 = [], time.perf_counter()
        for prompt in PROMPTS:
            texte, nb = generer(modele, prompt, a.n, reglage["top_k"], reglage["temperature"])
            m = mesurer(texte, prompt, vocab)
            m.update({"prompt": prompt, "texte": texte, "octets": nb - len(prompt.encode())})
            lignes.append(m)
        total_s = time.perf_counter() - t0
        octets = sum(m["octets"] for m in lignes)
        resultat["reglages"][reglage["nom"]] = {
            "mots_valides": round(sum(m["mots_valides"] for m in lignes) / len(lignes), 4),
            "distinct_2": round(sum(m["distinct_2"] for m in lignes) / len(lignes), 4),
            "repetition": max(m["repetition"] for m in lignes),
            "echo": round(sum(m["echo"] for m in lignes) / len(lignes), 4),
            "octets": octets, "secondes": round(total_s, 2),
            "octets_s": round(octets / max(total_s, 1e-9), 1),
            "echantillons": lignes[:3],
            "lignes": lignes,
        }
    texte = json.dumps(resultat, ensure_ascii=False, indent=1)
    if a.sortie:
        pathlib.Path(a.sortie).write_text(texte + "\n", encoding="utf-8")
        print(f"écrit : {a.sortie}")
    for nom, r in resultat["reglages"].items():
        print(f"{nom:12s} mots_valides={r['mots_valides']:.3f} distinct_2={r['distinct_2']:.3f} "
              f"repetition={r['repetition']} echo={r['echo']:.2f} octets/s={r['octets_s']}")


if __name__ == "__main__":
    main()

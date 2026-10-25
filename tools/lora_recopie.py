#!/usr/bin/env python3
"""lora_recopie.py — ÉTAPE −1 : rendre la COPIE possible, pour que l'empreinte soit mesurable.

POURQUOI. La question de Stéphane (16/10) — « peut-on demander à un LLM de **présenter littéralement** un
texte soumis en entrée afin d'aller chercher des **empreintes à reproduire** ? » — suppose que le modèle
**sache recopier** ✓. Mesuré : le 0,5 B disponible en est **incapable** ✗ (**0 / 128** jetons recopiés ✓).
Sans copie, pas d'empreinte ; sans empreinte, rien à aligner ✓✓.

CE QU'IL ENTRAÎNE, ET LE CONTRÔLE QUI VA AVEC. Un **LoRA** (rang 8 sur q/k/v/o et les projections du MLP)
sur des paires tirées du corpus :
  · **positive** : « Recopie exactement le texte suivant :\n<texte>\nRecopie :\n<texte> » ✓ — la cible EST
    la copie ✓ ;
  · **de contrôle** : « Résume en une phrase :\n<texte>\nRésumé :\n<autre texte> » ✗ — sans elle, le modèle
    pourrait apprendre « répète toujours l'entrée » ✗✓, ce qui **détruirait** la mesure d'empreinte ✓ (on
    croirait lire une copie alors qu'on lirait un réflexe de perroquet ✗).

Ce qu'il écrit : l'adaptateur (`--sortie`, un `.pt`) et **le taux de recopie AVANT et APRÈS**, mesuré sur
des textes **jamais vus** ✓, avec le **contrôle** ✓.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/lora_recopie.py --hf <snapshot> --ids <corpus> \\
      [--pas 1500] [--rang 8] [--lr 1e-3] [--sortie /tmp/lora-recopie.pt]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import re
import sys
import time

import torch
import torch.nn as nn


class LoRA(nn.Module):
    """Le LoRA du dépôt, en petit : `W ← W + (α/r)·B·A`, A et B sur les projections d'attention et de MLP."""

    def __init__(self, module: nn.Linear, rang: int, alpha: float, graine: int = 0):
        super().__init__()
        g = torch.Generator().manual_seed(graine)
        self.A = nn.Parameter(torch.randn(rang, module.in_features, generator=g) * 0.01)
        self.B = nn.Parameter(torch.zeros(module.out_features, rang))
        self.echelle = alpha / rang
        self.base = module

    def forward(self, x):
        return self.base(x) + self.echelle * ((x @ self.A.T) @ self.B.T)


def poser_lora(modele, rang: int, alpha: float):
    """On ne touche QUE les projections (`q/k/v/o`, `gate/up/down`) et on GÈLE tout le reste ✓."""
    poses = []
    for couche in modele.model.layers:
        for nom in ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"):
            lin = getattr(couche.self_attn if "proj" in nom and nom in ("q_proj", "k_proj", "v_proj", "o_proj")
                          else couche.mlp, nom, None)
            if isinstance(lin, nn.Linear):
                remp = LoRA(lin, rang, alpha, graine=len(poses))
                if nom in ("q_proj", "k_proj", "v_proj", "o_proj"):
                    setattr(couche.self_attn, nom, remp)
                else:
                    setattr(couche.mlp, nom, remp)
                poses.append(remp)
    for p in modele.parameters():
        p.requires_grad_(False)
    for m in poses:
        m.A.requires_grad_(True); m.B.requires_grad_(True)
    return poses


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--ids", default="", help="corpus d'identifiants (le même que le moteur)")
    ap.add_argument("--famille", default="",
                    help="C3.2b : un corpus découpé par famille (C3.2a) — data/udhr/familles/<slug>.jsonl")
    ap.add_argument("--pas", type=int, default=1500)
    ap.add_argument("--rang", type=int, default=8)
    ap.add_argument("--alpha", type=float, default=16.0)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--longueur", type=int, default=96, help="longueur du texte à recopier (jetons)")
    ap.add_argument("--lot", type=int, default=4)
    ap.add_argument("--eval-tous", type=int, default=250)
    ap.add_argument("--eval-textes", type=int, default=3,
                    help="le nombre de textes d'évaluation (3 par défaut ; 8+ pour C3.2c)")
    ap.add_argument("--sortie", default="/tmp/lora-recopie.pt")
    ap.add_argument("--graine", type=int, default=0)
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.manual_seed(a.graine)
    tok = AutoTokenizer.from_pretrained(a.hf)
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    assert a.ids or a.famille, "il faut --ids (des identifiants) ou --famille (un corpus C3.2a)"
    if a.famille:
        # C3.2b : le corpus d'une FAMILLE — on encode ses « texte » avec le tokenizer du modèle.
        arts = [json.loads(l) for l in pathlib.Path(a.famille).read_text(encoding="utf-8").splitlines()
                if l.strip()]
        ids = []
        for art in arts:
            ids.extend(tok(art["texte"], add_special_tokens=False).input_ids)
    else:
        ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.ids).read_text()) if x.strip()]
    L = a.longueur

    def morceaux(n, debut):
        return [ids[i:i + L] for i in range(debut, min(len(ids) - L, debut + n * 4096), 4096)][:n]

    def paire(ids_txt, recopie: bool):
        """La paire (invite, cible) : la cible est la COPIE, ou un texte DIFFÉRENT pour le contrôle ✗."""
        txt = tok.decode(ids_txt)
        if recopie:
            invite = "Recopie exactement le texte suivant :\n" + txt + "\nRecopie :\n"
            return invite, txt
        invite = "Résume en une phrase :\n" + txt + "\nRésumé :\n"
        return invite, "This text is about a topic."      # cible DIFFÉRENTE : interdit le perroquet ✗

    def taux_recopie(modele, textes):
        """Le taux de recopie = la fraction du PLUS LONG PRÉFIXE exact, moyennée ✓ (+ le contrôle ✗)."""
        bons, controles = [], []
        with torch.no_grad():
            for t in textes:
                for recopie in (True, False):
                    inv, cible = paire(t, recopie)
                    b = tok(inv, return_tensors="pt").input_ids
                    g = modele.generate(b, max_new_tokens=L, do_sample=False,
                                        pad_token_id=tok.eos_token_id)
                    sortie = tok.decode(g[0][b.shape[1]:])
                    c = 0
                    for x, y in zip(sortie, cible):
                        if x != y: break
                        c += 1
                    (bons if recopie else controles).append(c / max(1, len(cible)))
        return 100 * sum(bons) / len(bons), 100 * sum(controles) / len(controles)

    eval_txt = morceaux(a.eval_textes, 60_000)                       # des textes JAMAIS vus à l'entraînement ✓
    poses = poser_lora(m, a.rang, a.alpha)
    n_param = sum(p.numel() for mod in poses for p in (mod.A, mod.B))
    print(f"LoRA : {len(poses)} projections · {n_param:,} paramètres ({100 * n_param / sum(p.numel() for p in m.parameters()):.4f} % du modèle)")

    avant = taux_recopie(m, eval_txt)
    print(f"AVANT : recopie {avant[0]:5.1f} % · contrôle (résumé) {avant[1]:5.1f} %")

    opt = torch.optim.AdamW([p for mod in poses for p in (mod.A, mod.B)], lr=a.lr)
    train = morceaux(64, 0)
    t0 = time.time()
    for pas in range(1, a.pas + 1):
        lot = random.sample(train, a.lot)
        pertes = []
        for t in lot:
            inv, cible = paire(t, True)                  # on n'entraîne QUE la recopie ✓
            b = tok(inv, return_tensors="pt").input_ids[0]
            c = tok(cible, return_tensors="pt").input_ids[0]
            seq = torch.cat([b, c]).unsqueeze(0)
            logits = m(seq).logits[0]
            # la perte ne porte QUE sur les jetons de la CIBLE ✓ (sinon on apprend l'invite ✗)
            lg = logits[len(b) - 1:len(b) - 1 + len(c)]
            pertes.append(nn.functional.cross_entropy(lg, c))
        perte = torch.stack(pertes).mean()
        opt.zero_grad(); perte.backward(); opt.step()
        if a.eval_tous > 0 and (pas % a.eval_tous == 0 or pas == a.pas):
            t = taux_recopie(m, eval_txt)
            print(f"  pas {pas:>5} · perte {float(perte):.4f} · recopie {t[0]:5.1f} % · contrôle {t[1]:5.1f} %"
                  f" · {time.time() - t0:.0f} s")
    apres = taux_recopie(m, eval_txt)
    print()
    print(f"APRÈS : recopie {apres[0]:5.1f} % · contrôle (résumé) {apres[1]:5.1f} %")
    torch.save({"lora": [{"nom": str(i), "A": mod.A.detach(), "B": mod.B.detach(),
                          "echelle": mod.echelle} for i, mod in enumerate(poses)],
                "rang": a.rang, "alpha": a.alpha, "longueur": L,
                "recopie_avant": avant[0], "recopie_apres": apres[0],
                "controle_avant": avant[1], "controle_apres": apres[1]}, a.sortie)
    print(f"adaptateur écrit dans {a.sortie}")
    if apres[0] > 50 and apres[1] < 20:
        print("  ✅ LA COPIE EST ACQUISE et le perroquet est évité : l'empreinte sera mesurable ✓✓")
    elif apres[0] > 50:
        print("  ⚠️ la copie est acquise MAIS le contrôle monte trop ✗ : le modèle répète sans discernement ✗✓")
    else:
        print("  ✗ la copie n'est pas acquise : monter le nombre de pas, le rang, ou le taux ✗")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""cout_bascule.py — LA LANGUE COMME PARAMÈTRE VIDEUT-ELLE ÊTRE UTILISÉE ? (le coût de la bascule)

LA QUESTION (chapitre 7, après six mesures). « La langue est un paramètre de 1,33 % » ✓✓ — mais si changer de
langue coûte le rechargement d'un modèle ✗, le paramètre n'est qu'une élégance ✗✓. Ce que « paramètre » doit
vouloir dire en pratique : **on échange quelques kilo-octets, pas un modèle** ✓✓.

CE QUE CET OUTIL MESURE, en trois temps :
  1. le **temps de chargement** d'un adaptateur depuis le disque ✓ (répété, on garde la médiane ✓) ;
  2. le **temps d'application** au modèle — copier ses paramètres dans les couches ✓ (c'est la bascule ✓) ;
  3. et pour comparer ✗ : le **temps de rechargement d'un modèle entier** ✓ (la méthode naïve ✓).

Et il donne le **rapport** entre les deux ✓ : c'est le chiffre qui dit si l'idée est utilisable ✓².

⚠️ CE QUE CE TEST NE DIT PAS : ces temps sont mesurés sur des modèles-JOUETS (2,4 M ✓) — sur un modèle de
7 milliards, le rechargement serait **beaucoup** plus lent ✓✓ (donc le rapport serait **meilleur** ✓), mais
l'adaptateur pèserait aussi plus lourd ✓. La conclusion à retenir est le **principe** : on échange des
paramètres, pas un modèle ✓✓.

Usage :
  python3 tools/cout_bascule.py --hf /tmp/jouet-d256 --adaptateur /tmp/adaptateur-fr.pt [--essais 5]
"""
from __future__ import annotations

import argparse
import pathlib
import statistics
import sys
import time

import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from adaptateur_langue import poser_lora


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--adaptateur", default="/tmp/adaptateur-fr.pt")
    ap.add_argument("--essais", type=int, default=5)
    a = ap.parse_args()
    from transformers import AutoModelForCausalLM

    chemin = pathlib.Path(a.adaptateur)
    if not chemin.exists():
        sys.exit(f"adaptateur absent : {chemin}")
    poids_adapt = chemin.stat().st_size

    # 1. le chargement de l'adaptateur (répété ✓)
    temps_chargement = []
    for _ in range(a.essais):
        t0 = time.perf_counter()
        d = torch.load(chemin, map_location="cpu", weights_only=False)
        temps_chargement.append((time.perf_counter() - t0) * 1000)

    # 2. l'application au modèle (la bascule ✓)
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    poses = poser_lora(m, d["rang"])
    etat = m.state_dict()
    temps_application = []
    for _ in range(a.essais):
        t0 = time.perf_counter()
        with torch.no_grad():
            for k, v in d["lora"].items():
                if k in etat and etat[k].shape == v.shape:
                    etat[k].copy_(v)
        temps_application.append((time.perf_counter() - t0) * 1000)
    poids_modele = sum(p.numel() for p in m.parameters()) * 4
    del m

    # 3. le rechargement complet (la méthode naïve ✗)
    temps_modele = []
    for _ in range(max(1, a.essais // 2)):
        t0 = time.perf_counter()
        m2 = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
        temps_modele.append((time.perf_counter() - t0) * 1000)
        del m2

    med = statistics.median
    c, ap_, mo = med(temps_chargement), med(temps_application), med(temps_modele)
    print()
    print("   ce qu'on échange            | taille        | temps médian")
    print("   ----------------------------|---------------|-------------")
    print(f"   adaptateur (chargement)     | {poids_adapt/1024:8.0f} Ko   | {c:8.2f} ms")
    print(f"   adaptateur (application)    |               | {ap_:8.2f} ms")
    print(f"   modèle entier (recharge ✗)  | {poids_modele/1048576:8.1f} Mo   | {mo:8.2f} ms")
    print()
    total = c + ap_
    print(f"  bascule de langue : {total:.1f} ms · rechargement du modèle : {mo:.0f} ms "
          f"→ rapport ×{mo/total:.0f} ✓✓")
    print(f"  en mémoire : {poids_adapt/1024:.0f} Ko par langue, contre {poids_modele/1048576:.1f} Mo "
          f"pour un modèle par langue ✓")
    print()
    print("  lecture : on échange des PARAMÈTRES, pas un modèle ✓✓ — et le rapport ne fera que s'améliorer")
    print("  avec la taille du modèle ✓ (un modèle de 7 B pèse des milliers de fois plus qu'un adaptateur).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

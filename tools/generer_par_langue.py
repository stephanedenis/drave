#!/usr/bin/env python3
"""generer_par_langue.py — LA LANGUE COMME PARAMÈTRE, VUE DE LA SORTIE.

LA QUESTION (chapitre 7, cinquième mesure). L'adaptateur fait passer la perplexité française de 3,19 à 1,50
✓✓ — mais cela ne dit **pas** dans quelle langue le modèle **écrit** ✗. Or c'est ce que « la langue comme
paramètre » doit vouloir dire : **la sortie suit l'adaptateur, pas l'amorce** ✓✓.

CE QUE CET OUTIL FAIT. Il charge un noyau **gelé** ✓, applique un adaptateur ✓ (ou aucun ✓), et **génère** à
partir d'une amorce courte ✓ — dans les deux langues ✓. Puis il **classe** la sortie par ses **mots-outils**
(les plus discriminants et les plus robustes à un texte de mauvaise qualité ✓) :

* si la sortie suit **l'amorce** ✗ → la langue n'est qu'une entrée, pas un paramètre ✗ ;
* si la sortie suit **l'adaptateur** ✓✓ → la langue est bien un paramètre de sortie ✓✓.

⚠️ CE QUE CE TEST NE DIRA PAS : sur un modèle de 2,4 M paramètres en octets, le texte généré est **de la bouillie**
✗ — l'outil ne mesure donc **pas** la qualité ✗, seulement la **langue** (les mots-outils ✓). C'est écrit ici
pour que personne ne lise « ça écrit bien » là où il n'y a que « ça écrit français » ✓.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/generer_par_langue.py --hf /tmp/jouet-d256 \\
      --adaptateur-fr /tmp/adaptateur-fr.pt --adaptateur-en /tmp/adaptateur-langue-en.pt
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from adaptateur_langue import poser_lora   # la même pose de LoRA, pour recharger à l'identique ✓

MOTS_FR = set("le la les de des du un une et est sont que qui pour pas par dans sur au aux ce cette ces il elle ils elles nous vous je tu on se sa son leur plus avec sans être avoir fait comme mais ou donc car si tout bien très deux trois autre même aussi entre depuis pendant après avant contre vers chez".split())
MOTS_EN = set("the a an and is are was were of to in for on with that this these those it its they them we you he she his her their not have has had do does did but or if so all more very two three other same also between since during after before against toward at by from".split())


def langue(texte: str) -> tuple[int, int]:
    """Compte les mots-outils français et anglais ✓ — le classifieur le plus simple qui tienne sur de la
    bouillie ✓."""
    mots = re.findall(r"[a-zA-ZÀ-ÿ']+", texte.lower())
    fr = sum(1 for m in mots if m in MOTS_FR)
    en = sum(1 for m in mots if m in MOTS_EN)
    return fr, en


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--adaptateur-fr", default="/tmp/adaptateur-fr.pt")
    ap.add_argument("--adaptateur-en", default="/tmp/adaptateur-langue-en.pt")
    ap.add_argument("--tokeniseur", action="store_true",
                    help="générer avec le tokeniseur du modèle ✓ (au lieu des octets ✗)")
    ap.add_argument("--n", type=int, default=120)
    ap.add_argument("--temp", type=float, default=0.8)
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM
    amorces = {"anglais": "The cat sat on the ", "français": "Le chat s'est assis sur la "}
    adaptateurs = [("aucun", None)]
    for nom, chemin in (("français", a.adaptateur_fr), ("anglais", a.adaptateur_en)):
        if pathlib.Path(chemin).exists():
            adaptateurs.append((nom, chemin))
        else:
            print(f"  (adaptateur {nom} absent : {chemin})")

    print()
    print("   amorce     | adaptateur | langue de la SORTIE (mots-outils fr / en) | verdict")
    print("   -----------|------------|-------------------------------------------|--------")
    for nom_amorce, amorce in amorces.items():
        for nom_adapt, chemin in adaptateurs:
            m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
            if chemin:
                d = torch.load(chemin, map_location="cpu", weights_only=False)
                poses = poser_lora(m, d["rang"])
                etat = m.state_dict()
                with torch.no_grad():
                    # on recharge les LoRA sauvés : les clés se terminent par « .A » / « .B » ✓
                    for k, v in d["lora"].items():
                        if k in etat and etat[k].shape == v.shape:
                            etat[k].copy_(v)
            if a.tokeniseur:
                from transformers import AutoTokenizer
                tk = AutoTokenizer.from_pretrained(a.hf)
                b = torch.tensor([tk(amorce, add_special_tokens=False).input_ids])
            else:
                b = torch.tensor([list(amorce.encode("utf-8"))])
            with torch.no_grad():
                g = m.generate(b, max_new_tokens=a.n, do_sample=True, temperature=a.temp,
                               top_k=20, pad_token_id=0)
            if a.tokeniseur:
                sortie = tk.decode(g[0][b.shape[1]:].tolist(), skip_special_tokens=True)
            else:
                sortie = bytes(g[0][b.shape[1]:].tolist()).decode("utf-8", errors="ignore")
            fr, en = langue(sortie)
            suivi = "suit l'amorce" if (nom_amorce == "français") == (fr > en) else "suit l'adaptateur" if nom_adapt != "aucun" else "—"
            print(f"   {nom_amorce:10s} | {nom_adapt:10s} | fr {fr:3d} · en {en:3d}  ({sortie[:26]!r}) | {suivi}")
            del m
    print()
    print("  lecture : si la sortie change de langue avec l'ADAPTATEUR ✓✓, la langue est un paramètre de sortie ✓.")
    print("  ⚠️ sur un modèle de 2,4 M en octets, le texte est de la bouillie : ce test mesure la LANGUE, pas la")
    print("  qualité ✗.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

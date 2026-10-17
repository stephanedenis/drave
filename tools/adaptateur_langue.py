#!/usr/bin/env python3
"""adaptateur_langue.py — LA LANGUE COMME PARAMÈTRE : un petit adaptateur peut-il suffire ?

LA QUESTION (famille E du chapitre 7). Le noyau d'un modèle bilingue est **neutre** (couches 1-2 au hasard,
mesuré le 17/10 ✓). Mais un modèle **monolingue** (entraîné sur l'anglais seul ✓) n'a aucune raison d'être
neutre devant du français ✗ : ses états de français sont **hors distribution** ✓. La question de la famille E
est donc : **un petit adaptateur peut-il absorber la langue** ✓ — c'est-à-dire faire que le noyau voie le
français comme de l'anglais ✓ — **sans toucher un seul poids du noyau** ✓✓ ?

CE QUE CET OUTIL FAIT. Il gèle tout le modèle ✓, pose un **LoRA** (rang faible ✓) sur les projections
d'attention et de MLP ✓, et l'entraîne sur un texte **français** avec l'objectif ordinaire de langue
(prédire l'octet suivant ✓). Puis il compare, **avec et sans** l'adaptateur :
  · la **perplexité** sur du français ✓ (l'adaptateur doit l'améliorer ✓) ;
  · la **précision du classifieur de langue** sur l'état du noyau ✓ (l'adaptateur doit la **faire baisser** ✓✓
    — c'est-à-dire rendre les états français **semblables** aux états anglais ✓).

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/adaptateur_langue.py --hf /tmp/jouet-d256 \\
      --fr data/corpus_fr.txt --pas 2000 [--rang 8] [--sortie /tmp/adaptateur-fr.pt]
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))


COUCHES_CIBLES = ""


def poser_lora(modele, rang: int, alpha: float = 16.0):
    """Un LoRA sur `q/k/v/o` et `gate/up/down` ✓ — le noyau reste gelé ✓."""
    class LoRA(nn.Module):
        def __init__(self, base, r, a_, g):
            super().__init__()
            self.base = base
            gen = torch.Generator().manual_seed(g)
            # ⚠️ LES PARAMÈTRES DU LoRA DOIVENT VIVRE SUR LE MÊME DISPOSITIF QUE LE NOYAU ✗✓. Créés sur CPU
            # alors que le noyau est sur cuda:0, ils faisaient échouer la première multiplication ✓✓ (le
            # quatorzième piège de la nuit : deux objets qui doivent être ensemble et ne le sont pas).
            dev = base.weight.device
            self.A = nn.Parameter((torch.randn(r, base.in_features, generator=gen) * 0.01).to(dev))
            self.B = nn.Parameter(torch.zeros(base.out_features, r, device=dev))
            self.ech = a_ / r

        def forward(self, x):
            return self.base(x) + self.ech * ((x @ self.A.T) @ self.B.T)

    poses = []
    choisies = {int(x) for x in COUCHES_CIBLES.split(",") if x.strip()} or None
    for i, couche in enumerate(modele.model.layers):
        if choisies is not None and i not in choisies:
            continue
        for nom, conteneur in (("q_proj", couche.self_attn), ("k_proj", couche.self_attn),
                               ("v_proj", couche.self_attn), ("o_proj", couche.self_attn),
                               ("gate_proj", couche.mlp), ("up_proj", couche.mlp), ("down_proj", couche.mlp)):
            lin = getattr(conteneur, nom, None)
            if isinstance(lin, nn.Linear):
                setattr(conteneur, nom, LoRA(lin, rang, alpha, len(poses)))
                poses.append(conteneur)
    for p in modele.parameters():
        p.requires_grad_(False)
    params = []
    for c in poses:
        for nom in ("A", "B"):
            pass
    for m in modele.modules():
        if isinstance(m, LoRA):
            m.A.requires_grad_(True); m.B.requires_grad_(True)
            params += [m.A, m.B]
    return params


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--fr", default="data/corpus_fr.txt")
    ap.add_argument("--en", default="data/corpus_en.txt")
    ap.add_argument("--pas", type=int, default=2000)
    ap.add_argument("--rang", type=int, default=8)
    ap.add_argument("--lr", type=float, default=2e-3)
    ap.add_argument("--seq", type=int, default=128)
    ap.add_argument("--lot", type=int, default=4)
    ap.add_argument("--couches", default="",
                    help="où poser l'adaptateur : indices de couches (ex. « 3 » = dernier étage) ; vide = "
                         "partout. La question : la langue vit-elle à la SURFACE (dernier étage) ou partout ?")
    ap.add_argument("--tokeniseur", action="store_true",
                    help="encoder avec le TOKENISEUR du modèle ✓ au lieu des octets ✗ — indispensable pour un "
                         "modèle qui n'est pas en octets (Qwen ✓) : sinon il reçoit des identifiants invalides ✗✓")
    ap.add_argument("--sortie", default="/tmp/adaptateur-fr.pt")
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM
    # ⚠️ SUR LA CARTE, PAS SUR LE CPU ✗✗. Le modèle était chargé sans jamais être déplacé ✓✗ : sur les
    # modèles-jouets (2,4 M ✓) le CPU suffisait à peine ✓, mais sur un 0,5 B il a tourné **8 heures de CPU en
    # 32 minutes** ✓✗ sans finir. C'est la TREIZIÈME leçon d'instrument de la nuit, et la plus bête : un
    # dispositif qui n'est pas là où l'on croit ✓✓.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).to(device).eval()
    tok = None
    if a.tokeniseur:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(a.hf)

    def encoder(chemin):
        texte = pathlib.Path(chemin).read_text(errors="ignore")
        if tok is not None:
            return np.array(tok(texte, add_special_tokens=False).input_ids, dtype=np.int64)
        return np.frombuffer(texte.encode("utf-8"), dtype=np.uint8).astype(np.int64)

    fr = encoder(a.fr)
    en = encoder(a.en)

    def perte_langue(tab, n=8):
        tot = 0.0
        with torch.no_grad():
            for i in range(n):
                d = (i * 7919) % (len(tab) - a.seq - 1)
                x = torch.tensor(tab[d:d + a.seq]).unsqueeze(0).to(device)
                tot += float(m(x, labels=x).loss)
        return tot / n

    p_fr_avant, p_en_avant = perte_langue(fr), perte_langue(en)
    print(f"  AVANT : perte français {p_fr_avant:.4f} · perte anglais {p_en_avant:.4f}")

    global COUCHES_CIBLES
    COUCHES_CIBLES = a.couches
    params = poser_lora(m, a.rang)
    n = sum(p.numel() for p in params)
    total = sum(p.numel() for p in m.parameters())
    print(f"  LoRA : {n:,} paramètres ({100 * n / total:.3f} % du modèle) · noyau gelé ✓")

    opt = torch.optim.AdamW(params, lr=a.lr)
    g = torch.Generator().manual_seed(0)
    for pas in range(1, a.pas + 1):
        idx = torch.randint(0, len(fr) - a.seq - 1, (a.lot,), generator=g)
        x = torch.stack([torch.tensor(fr[i:i + a.seq]) for i in idx]).to(device)
        perte = m(x, labels=x).loss
        opt.zero_grad(); perte.backward(); opt.step()
        if pas % 500 == 0 or pas == a.pas:
            print(f"  pas {pas:>5} · perte {float(perte):.4f} · français {perte_langue(fr):.4f} · anglais {perte_langue(en):.4f}")

    p_fr_apres, p_en_apres = perte_langue(fr), perte_langue(en)
    print()
    print(f"  APRÈS : perte français {p_fr_apres:.4f} ({100*(p_fr_apres-p_fr_avant)/p_fr_avant:+.1f} %) · "
          f"anglais {p_en_apres:.4f} ({100*(p_en_apres-p_en_avant)/p_en_avant:+.1f} %)")
    torch.save({"lora": {k: v for k, v in m.state_dict().items() if any(s in k for s in (".A", ".B"))},
                "rang": a.rang, "fr_avant": p_fr_avant, "fr_apres": p_fr_apres,
                "en_avant": p_en_avant, "en_apres": p_en_apres}, a.sortie)
    print(f"  adaptateur écrit dans {a.sortie}")
    if p_fr_apres < p_fr_avant * 0.95 and p_en_apres < p_en_avant * 1.05:
        print("  ✅ l'adaptateur AMÉLIORE le français sans abîmer l'anglais : la langue est un paramètre ✓✓")
    elif p_fr_apres < p_fr_avant:
        print("  ⚠️ il améliore le français mais abîme l'anglais ✗ : il ne fait pas que traduire ✓")
    else:
        print("  ✗ il n'améliore pas le français : le rang ou le nombre de pas est trop faible ✗")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

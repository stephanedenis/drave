#!/usr/bin/env python3
"""cycle_entraine.py — C2 bis : un cycle ENTRAÎNÉ vaut-il mieux qu'une passe ?

CE QUI A ÉTÉ MESURÉ HIER SOIR (14/10). Le cycle à deux régions **existe** et il est exact : au
pas 1, il rend exactement la perplexité de la chaîne (`reports/rapport-cycle-c2.md`). Mais **non
entraîné, il diverge** : 14,65 → 275,52 → 940,22 → 2 988,46 en quatre pas — ce que la note
annonçait (« un cycle à gain ≥ 1 diverge ») et ce que la récurrence locale disait déjà (« un écho,
pas une mémoire »). Ce fichier pose la question qui reste, et c'est **la seule** qui compte pour
le cerveau : **un cycle entraîné peut-il servir à quelque chose ?**

L'IDÉE, ET ELLE EST CELLE DU CORTEX. Une boucle cortico-thalamique ne « repasse » pas pour rien :
elle **raffine** — chaque passage doit rendre la représentation plus utile. Ici, cela se mesure
exactement : la perplexité du prochain jeton **à chaque pas**. Un cycle utile est un cycle dont la
perplexité **baisse** avec les pas ; un cycle inutile diverge ou stagne.

CE QUI EST ENTRAÎNÉ. Un LoRA (rang faible sur q/k/v/o) sur les couches, avec pour objectif la
somme des pertes **de tous les pas** — donc le réseau apprend à ce que son propre retour soit
*exploitable*, pas seulement à prédire une fois.

TROIS BRAS, MÊME PROTOCOLE :

  * **non entraîné** : la trajectoire de la veille (elle diverge) ;
  * **entraîné** : la même trajectoire, après apprentissage ;
  * **référence** : le modèle **sans boucle** (une passe) — le chiffre à battre, et il est dur :
    un cycle qui ne fait pas mieux qu'une passe coûte N fois plus cher pour rien.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/cycle_entraine.py --train 8 --pas-temps 4 --epoques 8 \\
      [--json f.json] [--sauver lora.pt]
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import re

import numpy as np
import torch
import torch.nn as nn

SNAPSHOT_DEFAUT = ("/home/stephane/IA/cache/huggingface/hub/"
                   "models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/"
                   "7ae557604adf67be50417f59c2c2f167def9a775")


class LoraLineaire(nn.Module):
    def __init__(self, base: nn.Linear, rang: int, alpha: float):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad_(False)
        self.A = nn.Parameter(torch.empty(rang, base.in_features))
        self.B = nn.Parameter(torch.zeros(base.out_features, rang))
        nn.init.kaiming_uniform_(self.A, a=math.sqrt(5))
        self.echelle = alpha / rang

    def forward(self, x):
        return self.base(x) + (x @ self.A.T @ self.B.T) * self.echelle


class Cycle:
    """Le cycle à deux régions, **exactement** comme le pilote le déroule.

    Région A = couches [0, coupe), région B = [coupe, 24). Un pas : l'entrée traverse A, son
    résidu BRUT entre dans B, le résidu brut de B est la sortie — et il redevient l'entrée du pas
    suivant (c'est le lien récurrent `r1 → r0`). Le pas 1 fait exception : il n'a pas d'état
    d'avant, donc A tourne sur l'embarquement du texte (le seul pas où le graphe voit le monde).
    """

    def __init__(self, modele, coupe: int, pas_temps: int, dev: str):
        self.m, self.coupe, self.T, self.dev = modele, coupe, pas_temps, dev
        self.brut = {}

        def crochet(_m, _e, sortie):
            self.brut["x"] = sortie[0] if isinstance(sortie, tuple) else sortie

        self.m.model.layers[-1].register_forward_hook(crochet)

    def pas(self, x=None, ids=None):
        """Un pas. `x` = états d'entrée (None au pas 1 : on part de l'embarquement)."""
        h = self.m.model.embed_tokens(ids) if x is None else x
        out = self.m.model(inputs_embeds=h, output_hidden_states=True, use_cache=False)
        a = out.hidden_states[self.coupe]      # résidu brut après la couche coupe-1
        b = self.brut["x"]                     # résidu brut après la dernière couche
        return a, b

    def trajectoire(self, ids, grad=True):
        """Rend [(logits_1, b_1), …]. Les logits sont calculés sur le résidu brut de B."""
        ctx = torch.enable_grad() if grad else torch.no_grad()
        sorties = []
        with ctx:
            x = None
            for _ in range(self.T):
                a, b = self.pas(x=x, ids=ids)
                logits = self.m.lm_head(self.m.model.norm(b))
                sorties.append((logits, b))
                x = b
        return sorties


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default=SNAPSHOT_DEFAUT)
    ap.add_argument("--ids", default="/tmp/campagne24/ids_0.5B-Q8.txt")
    ap.add_argument("--train", type=int, default=8, help="morceaux d'entraînement")
    ap.add_argument("--val", type=int, default=1)
    ap.add_argument("--test", type=int, default=2)
    ap.add_argument("--taille", type=int, default=256)
    ap.add_argument("--pas-temps", type=int, default=4)
    ap.add_argument("--coupe", type=int, default=12, help="couche de coupe (région A = 0..coupe-1)")
    ap.add_argument("--epoques", type=int, default=8)
    ap.add_argument("--rang", type=int, default=8)
    ap.add_argument("--alpha", type=float, default=16.0)
    ap.add_argument("--couches-lora", type=int, default=24)
    ap.add_argument("--pas-lora", type=float, default=1e-3)
    ap.add_argument("--objectif", choices=["somme", "dernier", "point-fixe"], default="somme",
                    help="somme = les T pertes (le réglage de la fiche C2 bis) · dernier = le "
                         "dernier pas seul · point-fixe = somme + pénalité de CONVERGENCE "
                         "(la boucle doit se poser, pas seulement prédire)")
    ap.add_argument("--beta", type=float, default=1.0, help="poids de la pénalité de point fixe")
    ap.add_argument("--graine", type=int, default=0)
    ap.add_argument("--json", default=None)
    ap.add_argument("--sauver", default=None)
    a = ap.parse_args()

    torch.manual_seed(a.graine); np.random.seed(a.graine)
    dev = "cuda"
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.modele, dtype=torch.float32).to(dev).eval()
    for p in m.parameters():
        p.requires_grad_(False)
    loras = []
    for i in range(a.couches_lora):
        attn = m.model.layers[i].self_attn
        for nom in ("q_proj", "k_proj", "v_proj", "o_proj"):
            base = getattr(attn, nom)
            lora = LoraLineaire(base, a.rang, a.alpha).to(base.weight.device, base.weight.dtype)
            setattr(attn, nom, lora)
            loras += [lora.A, lora.B]
    cyc = Cycle(m, a.coupe, a.pas_temps, dev)
    print(f"cycle : {a.pas_temps} pas · coupe {a.coupe}/24 · LoRA rang {a.rang} sur "
          f"{a.couches_lora} couches ({sum(p.numel() for p in loras):,} paramètres)")

    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.ids).read_text()) if x.strip()]
    n = a.train + a.val + a.test
    pas = len(ids) // (n + 1)
    morceaux = [ids[i * pas: i * pas + a.taille] for i in range(n)]
    tr = morceaux[:a.train]
    va = morceaux[a.train]
    te = morceaux[a.train + a.val:]

    def ppl_trajectoire(morceaux_ids, grad=False):
        """Perplexité à chaque pas, sur les positions 4.. (la convention du moteur)."""
        tot = [0.0] * a.pas_temps
        cnt = 0
        ctx = torch.enable_grad() if grad else torch.no_grad()
        for ids_m in morceaux_ids:
            t = torch.tensor([ids_m], device=dev)
            with ctx:
                for j, (logits, _) in enumerate(cyc.trajectoire(t, grad=grad)):
                    cible = t[0, 5:]
                    perte = nn.functional.cross_entropy(logits[0, 4:-1].float(), cible,
                                                        reduction="sum")
                    tot[j] += float(perte.detach() if grad else perte)
            cnt += len(ids_m) - 5
        return [float(np.exp(x / max(cnt, 1))) for x in tot]

    avant = ppl_trajectoire(te)
    print("  avant  : " + " · ".join(f"pas {j + 1} {p:,.2f}" for j, p in enumerate(avant)))

    opt = torch.optim.Adam([{"params": loras, "lr": a.pas_lora}])
    meilleur = (1e18, None)
    for e in range(a.epoques):
        tot, cnt = 0.0, 0
        for ids_m in tr:
            t = torch.tensor([ids_m], device=dev)
            opt.zero_grad()
            perte_tot = 0.0
            precedent = None
            for j, (logits, b) in enumerate(cyc.trajectoire(t, grad=True)):
                ce = nn.functional.cross_entropy(logits[0, 4:-1].float(), t[0, 5:])
                if a.objectif == "dernier":
                    perte_tot = ce if j == a.pas_temps - 1 else perte_tot
                else:
                    perte_tot = perte_tot + ce
                if a.objectif == "point-fixe" and precedent is not None:
                    # LA BOUCLE DOIT SE POSER : on pénalise le DÉPLACEMENT de l'état entre deux
                    # pas, en relatif (un état qui change de 1 % d'un pas à l'autre est un point
                    # fixe ; un état qui double diverge). C'est la piste nommée par la fiche C2 bis.
                    num = (b - precedent).pow(2).mean()
                    den = precedent.pow(2).mean() + 1e-6
                    perte_tot = perte_tot + a.beta * (num / den)
                precedent = b.detach()
            perte_tot.backward(); opt.step()
            tot += float(perte_tot.detach()); cnt += 1
        pv = ppl_trajectoire([va])[-1]        # l'époque se choisit sur le DERNIER pas, en validation
        marque = ""
        if pv < meilleur[0]:
            meilleur = (pv, [p.detach().clone() for p in loras]); marque = "  ← meilleur (validation)"
        print(f"    époque {e + 1:>2}/{a.epoques} · perte moyenne {tot / max(cnt, 1):.4f} · "
              f"validation (dernier pas) {pv:,.2f}{marque}")
    for p, q in zip(loras, meilleur[1]):
        p.data.copy_(q)

    apres = ppl_trajectoire(te)
    print("  après  : " + " · ".join(f"pas {j + 1} {p:,.2f}" for j, p in enumerate(apres)))

    # Référence : le modèle SANS boucle (une passe) — le chiffre à battre.
    sans = []
    with torch.no_grad():
        for ids_m in te:
            t = torch.tensor([ids_m], device=dev)
            logits = m(input_ids=t, use_cache=False).logits
            sans.append(float(nn.functional.cross_entropy(logits[0, 4:-1].float(), t[0, 5:],
                                                          reduction="sum")))
    cnt = sum(len(x) - 5 for x in te)
    ppl_sans = float(np.exp(sum(sans) / max(cnt, 1)))

    print()
    print("| pas | non entraîné | **entraîné** | une passe (référence) |")
    print("|---:|---:|---:|---:|")
    for j in range(a.pas_temps):
        ref = f"{ppl_sans:,.2f}" if j == 0 else "—"
        print(f"| {j + 1} | {avant[j]:,.2f} | **{apres[j]:,.2f}** | {ref} |")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"pas_temps": a.pas_temps, "coupe": a.coupe, "avant": avant, "apres": apres,
             "une_passe": ppl_sans, "epoques": a.epoques, "rang": a.rang}, indent=1,
            ensure_ascii=False))
    if a.sauver:
        torch.save({"rang": a.rang, "alpha": a.alpha, "profondeur": a.couches_lora,
                    "adaptateur": None,
                    "lora": [{"nom": f"model.layers.{i}.self_attn.{p}_proj.weight",
                              "A": getattr(m.model.layers[i].self_attn, p + "_proj").A.detach().cpu(),
                              "B": getattr(m.model.layers[i].self_attn, p + "_proj").B.detach().cpu(),
                              "echelle": a.alpha / a.rang}
                             for i in range(a.couches_lora) for p in ("q", "k", "v", "o")]},
                   a.sauver)
        print(f"LoRA écrit : {a.sauver}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

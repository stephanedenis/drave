#!/usr/bin/env python3
"""m8_plage_activations.py — M8, test n°1 : les activations du modèle log-normal tiennent-elles
dans ce que le moteur sait représenter ?

LE FAIT À EXPLIQUER (M8, `reports/rapport-m8-log-normal.md`). Le même entraînement, la même
quantification, des fichiers GGUF structurellement identiques — et pourtant le modèle **dense**
rend **×1,44** de perplexité à l'export quand le **log-normal** en rend **×78**. Trois causes sont
éliminées (poids, quantification, structure) ; l'hypothèse restante est que le **moteur traite les
activations d'une façon que PyTorch n'a pas**.

CE QUE LE MOTEUR FAIT, ET QUI EST LE CŒUR DE L'ESSAI. Il quantifie les activations **par vecteur** :
`échelle = max|a| / niveaux`, puis arrondit. Deux conséquences, et une seule est visible dans une
perplexité :

  1. **précision** : tout ce qui est plus petit que `max|a| / (2 × niveaux)` devient **zéro**. Si un
     vecteur porte à la fois 1e6 et 1, le 1 disparaît ;
  2. **saturation** : au-delà de `niveaux`, ça s'écrase — mais le moteur **adapte** l'échelle, donc
     ce n'est pas la saturation qui guette ici, c'est la **perte des petits**.

Un modèle log-normal (`|w| = exp(θ)`) couvre par construction plusieurs ordres de grandeur. Si ses
vecteurs d'activation ont une **plage dynamique** bien plus large que ceux du dense, la
quantification par vecteur les détruit — et c'est la cause, chiffrée.

Usage :
  tools/m8_plage_activations.py --dense /tmp/e6/dense.gguf --lognormal /tmp/e6/lognormal.gguf \
      --val /tmp/e6/val.txt --limite 512 [--niveaux 32767]
"""
from __future__ import annotations

import argparse
import collections

import numpy as np
import torch
from transformers import AutoModelForCausalLM


def charger(chemin: str, appareil: str):
    m = AutoModelForCausalLM.from_pretrained(chemin, dtype=torch.float32).to(appareil).eval()
    return m


@torch.no_grad()
def plages(modele, x: torch.Tensor, appareil: str):
    """{nom du module: (max|a|, médiane|a| des non nuls)} sur tout le passage avant."""
    stats = collections.OrderedDict()
    prises = []

    def accroche(nom):
        def f(_mod, _entree, sortie):
            a = sortie.detach().float().abs().flatten()
            nz = a[a > 0]
            med = float(nz.median()) if nz.numel() else 0.0
            stats[nom] = (float(a.max()) if a.numel() else 0.0, med)
        return f

    for nom, mod in modele.named_modules():
        if isinstance(mod, torch.nn.Linear):
            prises.append(mod.register_forward_hook(accroche(nom)))
    modele(x.to(appareil))
    for p in prises:
        p.remove()
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dense", required=True)
    ap.add_argument("--lognormal", required=True)
    ap.add_argument("--val", required=True)
    ap.add_argument("--limite", type=int, default=512)
    ap.add_argument("--niveaux", type=int, default=32767,
                    help="niveaux du moteur en 16 bits (2^15 − 1)")
    a = ap.parse_args()

    brut = open(a.val, "rb").read()[: a.limite]
    x = torch.tensor([[b for b in brut]], dtype=torch.long)
    appareil = "cuda" if torch.cuda.is_available() else "cpu"

    resultats = {}
    for nom, chemin in (("dense", a.dense), ("log-normal", a.lognormal)):
        m = charger(chemin, appareil)
        # les POIDS d'abord : c'est là que le variant se distingue, et il faut le vérifier
        poids = [(n, p.detach().float().abs()) for n, p in m.named_parameters() if p.dim() >= 2]
        wmax = max(float(p.max()) for _, p in poids)
        wmin_nonzero = min(float(p[p > 0].min()) for _, p in poids if (p > 0).any())
        resultats[nom] = (plages(m, x, appareil), wmax, wmin_nonzero)
        del m
        torch.cuda.empty_cache() if appareil == "cuda" else None

    stats_d, wmax_d, wmin_d = resultats["dense"]
    stats_l, wmax_l, wmin_l = resultats["log-normal"]
    print(f"\npoids : dense |w| de {wmin_d:.3e} à {wmax_d:.3e} (rapport {wmax_d / wmin_d:,.0f})")
    print(f"        log-normal |w| de {wmin_l:.3e} à {wmax_l:.3e} (rapport {wmax_l / wmin_l:,.0f})")

    print(f"\nactivations, {len(brut)} octets de contexte, quantization par vecteur à "
          f"{a.niveaux} niveaux :\n")
    print("| module | max\\|a\\| dense | plage dense | max\\|a\\| log-normal | plage log-normal | "
          "effacé dense | effacé log-normal |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    lignes = []
    for nom in stats_d:
        if nom not in stats_l:
            continue
        md, med_d = stats_d[nom]
        ml, med_l = stats_l[nom]
        # « effacé » : part des valeurs sous le pas de quantification (max/niveaux)
        pas_d, pas_l = md / a.niveaux, ml / a.niveaux
        eff_d = pas_d / med_d if med_d > 0 else float("inf")
        eff_l = pas_l / med_l if med_l > 0 else float("inf")
        lignes.append((nom, md, med_d, ml, med_l, eff_d, eff_l))

    # On n'affiche que les projections où le variant se distingue vraiment, plus les extrêmes.
    lignes.sort(key=lambda l: -(l[6] / l[5] if l[5] > 0 else 0))
    for nom, md, med_d, ml, med_l, eff_d, eff_l in lignes[:14]:
        print(f"| `{nom}` | {md:,.3e} | {md / med_d if med_d else 0:,.1f} | {ml:,.3e} | "
              f"{ml / med_l if med_l else 0:,.1f} | {eff_d:,.4f} | {eff_l:,.4f} |")
    print()
    print("« plage » = max|a| / médiane des non nuls (la plage dynamique du vecteur).")
    print("« effacé » = pas de quantification (max/niveaux) divisé par la médiane : au-delà de 1,")
    print("la moitié des valeurs sont arrondies à zéro. C'est le seul chiffre qui compte ici.")
    pire_d = max(l[5] for l in lignes)
    pire_l = max(l[6] for l in lignes)
    print(f"\nle PIRE module : dense {pire_d:,.4f} · log-normal {pire_l:,.4f} "
          f"(×{pire_l / pire_d if pire_d else 0:,.2f})")
    if pire_l > 1.0 > pire_d:
        print("  ⇒ la quantification par vecteur EFFACE la moitié des valeurs du log-normal et pas "
              "celles du dense : l'hypothèse de M8 est vérifiée par cette mesure")
    elif pire_l > pire_d * 2:
        print("  ⇒ le log-normal est bien plus exposé, sans franchir le seuil d'effacement : "
              "l'hypothèse est soutenue, pas prouvée")
    else:
        print("  ⇒ les deux modèles sont exposés pareil : l'hypothèse « traitement d'activation » "
              "n'est PAS soutenue par cette mesure, et il faut chercher ailleurs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

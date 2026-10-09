#!/usr/bin/env python3
"""speculatif.py — le taux d'acceptation d'un brouillon, mesuré AVANT d'écrire du moteur.

POURQUOI CE CHIFFRE AVANT CE CODE. Le décodage spéculatif est le multiplicateur
de la feuille de route : il rend le décodage **par lots**, donc il ferait servir
au décodage ce que le regroupement par experts donne déjà au préremplissage. Le
moteur n'en a **aucune** implémentation (`grep eagle|brouillon|specul` dans
`drave-core/src/` = 0), et le seul brouillon présent sur le disque
(`eagle3-gpt-oss-120b`) ne peut pas servir tel quel : un Eagle3 s'attache aux
états cachés de SA cible, ce n'est pas un modèle autonome.

Avant d'écrire du moteur, il faut donc la seule mesure qui décide : **quel taux
d'acceptation un petit modèle de la même famille donne-t-il pour un plus gros ?**
Un brouillon rejeté coûte plus qu'il ne rapporte ; un brouillon accepté 3 fois sur
4 vaut ~2,5× sur le décodage.

CE QUI EST MESURÉ : pour k = 1..8, la longueur du préfixe commun entre la suite
gloutonne du brouillon et celle de la cible. C'est le taux d'acceptation en
décodage glouton — la borne utile, et la seule qui se mesure sans écrire le
décodage lui-même. On rapporte aussi l'espérance de gain sous la formule
standard, avec le coût relatif mesuré des deux modèles.

Usage :
    speculatif.py [--brouillon Qwen/Qwen2.5-0.5B] [--cible Qwen/Qwen2.5-1.5B]
                  [--k 8] [--prefixes 40] [--jetons 64]
"""
import argparse
import json
import math
import os
import sys

import numpy as np
import torch


def charger(nom):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(nom)
    m = AutoModelForCausalLM.from_pretrained(nom, dtype=torch.float16).eval()
    return tok, m


@torch.no_grad()
def suite_gloutonne(modele, ids, k, dev):
    """Les k jetons que le modèle choisit lui-même, en glouton, avec cache KV."""
    sortie = modele(ids.to(dev), use_cache=True)
    past = sortie.past_key_values
    logits = sortie.logits[:, -1, :]
    jetons = []
    for _ in range(k):
        t = int(logits.argmax(-1)[0])
        jetons.append(t)
        if len(jetons) == k:
            break
        sortie = modele(torch.tensor([[t]], device=dev), past_key_values=past, use_cache=True)
        past = sortie.past_key_values
        logits = sortie.logits[:, -1, :]
    return jetons


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--brouillon", default="Qwen/Qwen2.5-0.5B")
    p.add_argument("--cible", default="Qwen/Qwen2.5-1.5B")
    p.add_argument("--k", type=int, default=8)
    p.add_argument("--prefixes", type=int, default=40)
    p.add_argument("--jetons", type=int, default=64)
    p.add_argument("--corpus", default="data/corpus_en_val.txt")
    p.add_argument("--sans-gpu", action="store_true")
    a = p.parse_args()
    dev = torch.device("cpu" if a.sans_gpu or not torch.cuda.is_available() else "cuda")

    tok_b, mb = charger(a.brouillon)
    mb = mb.to(dev)
    tok_c, mc = charger(a.cible)
    mc = mc.to(dev)
    print(f"# brouillon {a.brouillon} · cible {a.cible} · appareil {dev}")
    if tok_b.get_vocab() != tok_c.get_vocab():
        # Deux tokenizers différents rendent la mesure vide de sens : le brouillon
        # proposerait des jetons que la cible ne peut pas représenter.
        print("# ATTENTION : vocabulaires différents — la mesure ne vaut rien")
        return 1

    texte = open(a.corpus, encoding="utf-8", errors="replace").read(200_000)
    ids_tous = tok_b(texte)["input_ids"]
    pas = max(1, (len(ids_tous) - a.jetons - a.k - 2) // a.prefixes)
    longueurs = []
    for i in range(a.prefixes):
        deb = i * pas
        prefixe = torch.tensor([ids_tous[deb:deb + a.jetons]])
        pb = suite_gloutonne(mb, prefixe, a.k, dev)
        pc = suite_gloutonne(mc, prefixe, a.k, dev)
        commun = 0
        for x, y in zip(pb, pc):
            if x != y:
                break
            commun += 1
        longueurs.append(commun)
    longueurs = np.array(longueurs)
    print(f"# {a.prefixes} préfixes de {a.jetons} jetons · k = {a.k}")
    print(f"# acceptation moyenne : {longueurs.mean():.2f} jetons sur {a.k} "
          f"({longueurs.mean()/a.k*100:.1f} %) · médiane {np.median(longueurs):.0f} "
          f"· minimum {longueurs.min()} · maximum {longueurs.max()}")
    for seuil in (1, 2, 3, 4):
        print(f"#   au moins {seuil} jeton(s) accepté(s) : "
              f"{(longueurs >= seuil).mean()*100:.0f} % des préfixes")
    # Espérance de gain, avec le coût relatif mesuré des deux modèles.
    for c in (0.25, 0.33, 0.5):
        gain = (longueurs.mean() + 1) / (1 + a.k * c)
        print(f"#   gain espéré si le brouillon coûte {c:.2f}× la cible par pas : ×{gain:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

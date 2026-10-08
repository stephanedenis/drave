#!/usr/bin/env python3
"""porte_moteur.py — la référence PyTorch qui rend la porte d'exécution HONNÊTE.

POURQUOI. Comparer le moteur à un modèle en f32 ne mesure pas le moteur : ça
mesure la quantification Q8_0/Q4_0 que l'export a appliquée. Le moteur, lui,
part des poids QUANTIFIÉS. La référence doit donc partir des mêmes — c'est la
méthode du dépôt : « une seconde implémentation de la même formule, pas une
seconde exécution de la même implémentation ».

Ce que ce script fait, exactement :
  1. charge le modèle HF ;
  2. lui applique la MÊME quantification que `exporter_gguf.py` (Q8_0 sur les
     tenseurs 2D, Q4_0 sur les experts, en séparant `gate_up_proj` en deux
     moitiés comme le fait l'export) ;
  3. calcule les logits de référence et les écrit au format du moteur
     (`--logits-bin` : int32 n_vocab, int32 n_pos, puis n_pos lignes de f32).

Usage :
    porte_moteur.py --hf modele_hf/ --ids ids.txt --logits ref.bin [--n 256]
"""
import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exporter_gguf import q4_0_decoder, q4_0_encoder, q8_0_decoder, q8_0_encoder  # noqa: E402


def arrondi(enc, dec, a):
    a = np.ascontiguousarray(a, dtype=np.float32)
    return dec(enc(a), a.shape)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--hf", required=True)
    p.add_argument("--ids", required=True)
    p.add_argument("--logits", required=True)
    p.add_argument("--n", type=int, default=0, help="0 = tout le fichier d'ids")
    a = p.parse_args()

    from transformers import Qwen3MoeForCausalLM
    modele = Qwen3MoeForCausalLM.from_pretrained(a.hf, dtype=torch.float32)
    cfg = json.load(open(os.path.join(a.hf, "config.json")))
    sd = modele.state_dict()
    n_exp, n_ff = cfg["num_local_experts"], cfg["moe_intermediate_size"]

    n_q8 = n_q4 = 0
    for k in list(sd.keys()):
        # Les experts FUSIONNÉS ne finissent PAS par « .weight »
        # (`mlp.experts.gate_up_proj`) : un filtre sur le suffixe les laissait en
        # f32, et la « porte » comparait alors le Q4_0 du moteur à un modèle qui
        # ne l'avait jamais reçu.
        est_poids = k.endswith(".weight") or "gate_up_proj" in k or "down_proj" in k
        if not est_poids:
            continue
        w = sd[k].detach().cpu().numpy().astype(np.float32)
        if w.ndim == 3 and "gate_up_proj" in k:          # (E, 2·ff, d) fusionné
            gauche = arrondi(q4_0_encoder, q4_0_decoder, w[:, :n_ff, :])
            droite = arrondi(q4_0_encoder, q4_0_decoder, w[:, n_ff:, :])
            sd[k] = torch.tensor(np.concatenate([gauche, droite], axis=1))
            n_q4 += 1
        elif w.ndim == 3 and "down_proj" in k:
            sd[k] = torch.tensor(arrondi(q4_0_encoder, q4_0_decoder, w))
            n_q4 += 1
        elif w.ndim == 2 and w.shape[-1] % 32 == 0:
            sd[k] = torch.tensor(arrondi(q8_0_encoder, q8_0_decoder, w))
            n_q8 += 1
    modele.load_state_dict(sd)
    modele.eval()
    print(f"# quantification appliquée à la référence : {n_q8} tenseurs Q8_0, {n_q4} experts Q4_0")

    ids = np.array([int(v) for v in open(a.ids).read().strip().split(",")], dtype=np.int64)
    if a.n:
        ids = ids[:a.n]
    x = torch.tensor(ids).unsqueeze(0)
    with torch.no_grad():
        logits = modele(x).logits[0].float().numpy()          # (n_pos, vocab)
    # Perplexité sur les prédictions décalées, comme le moteur.
    lg = logits[:-1]
    cible = ids[1:]
    mx = lg.max(axis=-1, keepdims=True)
    lse = mx[:, 0] + np.log(np.exp(lg - mx).sum(axis=-1))
    nll = float((lse - lg[np.arange(len(cible)), cible]).mean())
    print(f"# référence : {len(cible)} prédictions · NLL {nll:.4f} nats · "
          f"perplexité {np.exp(nll):.4f}")

    with open(a.logits, "wb") as f:
        f.write(np.int32([logits.shape[1]]).tobytes())
        f.write(np.int32([logits.shape[0]]).tobytes())
        f.write(logits.astype(np.float32).tobytes())
    print(f"# logits écrits : {a.logits} ({logits.shape[0]} positions × {logits.shape[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

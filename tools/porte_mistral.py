#!/usr/bin/env python3
"""porte_mistral.py — la famille Mistral a-t-elle une porte, elle aussi ?

POURQUOI CE SCRIPT EXISTE. `codestral-22B` a rendu **35 657** de perplexité sur de
la prose dans la campagne — 4 000 fois le Qwen3-30B-A3B. Deux explications
tiennent : le modèle est spécialisé pour le **code** et mauvais en prose, ou le
moteur exécute mal l'architecture **Mistral**. Or cette famille n'a **aucune
porte** dans `tools/portes.sh` : Qwen, GLM, V4, gpt-oss, Kimi en ont une, Mistral
non. Un chiffre aberrant sur une famille non couverte n'est pas un résultat,
c'est un trou.

Ce script comble le trou par la méthode du dépôt : exporter un modèle Mistral,
fabriquer la référence PyTorch **sur les mêmes poids quantifiés**, et confronter
les logits du moteur. On utilise un Mistral minuscule et **aléatoire**
(`hf-internal-testing/tiny-random-MistralForCausalLM`) : sa perplexité ne veut
rien dire, mais ses LOGITS, eux, doivent coïncider — c'est tout ce qu'une porte
de correction demande.

Écrit à part de `exporter_gguf.py`, qui tournait pendant ce temps dans la chaîne
d'export : modifier un outil en cours d'usage est le meilleur moyen de corrompre
les résultats du même nuit.

Usage :
    porte_mistral.py --hf <dossier> --gguf sortie.gguf --logits ref.bin [--ids ids.txt]
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exporter_gguf import ecrire_gguf  # noqa: F401


def kv_depuis_config(cfg):
    """Les clefs que `gguf.rs::cfg` ira chercher : elles sont préfixées par le nom
    d'architecture déclaré ici. Se tromper de préfixe ne lève rien — le moteur
    lit ses défauts et exécute un AUTRE modèle, en silence."""
    arch = "llama"
    n_tete = cfg["num_attention_heads"]
    d = cfg["hidden_size"]
    return [
        ("general.architecture", arch),
        ("general.name", cfg.get("_name_or_path", "mistral")),
        ("general.file_type", 0),
        (f"{arch}.block_count", int(cfg["num_hidden_layers"])),
        (f"{arch}.context_length", int(cfg.get("max_position_embeddings", 2048))),
        (f"{arch}.embedding_length", int(d)),
        (f"{arch}.feed_forward_length", int(cfg["intermediate_size"])),
        (f"{arch}.attention.head_count", int(n_tete)),
        (f"{arch}.attention.head_count_kv", int(cfg.get("num_key_value_heads", n_tete))),
        (f"{arch}.attention.layer_norm_rms_epsilon", float(cfg.get("rms_norm_eps", 1e-6))),
        (f"{arch}.rope.freq_base", float(cfg.get("rope_theta", 10000.0))),
        # La fenêtre glissante de Mistral : la déclarer évite que le moteur
        # applique une attention pleine là où le modèle en attend une locale.
        (f"{arch}.attention.sliding_window", int(cfg.get("sliding_window") or 0)),
    ]


def tenseurs_depuis_hf(poids, cfg):
    from exporter_gguf import GGML_Q8_0, q8_0_encoder

    def q8(nom, arr):
        return (nom, (q8_0_encoder(arr), GGML_Q8_0, arr.shape))

    t = [q8("token_embd.weight", poids["model.embed_tokens.weight"]),
         ("output_norm.weight", poids["model.norm.weight"])]
    t.append(q8("output.weight", poids.get("lm_head.weight", poids["model.embed_tokens.weight"])))
    for l in range(cfg["num_hidden_layers"]):
        p, b = f"model.layers.{l}.", f"blk.{l}."
        t += [(b + "attn_norm.weight", poids[p + "input_layernorm.weight"]),
              q8(b + "attn_q.weight", poids[p + "self_attn.q_proj.weight"]),
              q8(b + "attn_k.weight", poids[p + "self_attn.k_proj.weight"]),
              q8(b + "attn_v.weight", poids[p + "self_attn.v_proj.weight"]),
              q8(b + "attn_output.weight", poids[p + "self_attn.o_proj.weight"]),
              (b + "ffn_norm.weight", poids[p + "post_attention_layernorm.weight"]),
              q8(b + "ffn_gate.weight", poids[p + "mlp.gate_proj.weight"]),
              q8(b + "ffn_up.weight", poids[p + "mlp.up_proj.weight"]),
              q8(b + "ffn_down.weight", poids[p + "mlp.down_proj.weight"])]
    return t


def reference(hf, ids_path, sortie):
    """La référence PyTorch, quantifiée EXACTEMENT comme l'export : sans cela la
    porte mesurerait la quantification, pas le calcul du moteur."""
    import torch
    import torch as _t
    from transformers import MistralForCausalLM

    from exporter_gguf import q8_0_decoder, q8_0_encoder
    cfg = json.load(open(os.path.join(hf, "config.json")))
    # `from_pretrained` — et surtout PAS `MistralForCausalLM(config)` : instancier
    # depuis la configuration crée un modèle aux poids ALÉATOIRES, et la
    # « référence » ne contient alors plus le modèle entraîné. La porte comparait
    # le moteur (bons poids) à un modèle aléatoire, et rendait « NON TENUE » —
    # une fausse alerte qui accuse le moteur d'un défaut du script de référence.
    modele = MistralForCausalLM.from_pretrained(hf, dtype=torch.float32)
    sd = modele.state_dict()
    n = 0
    for k in list(sd.keys()):
        if not k.endswith(".weight"):
            continue
        w = sd[k].detach().cpu().numpy().astype(np.float32)
        if w.ndim == 2 and w.shape[-1] % 32 == 0:
            a = np.ascontiguousarray(w)
            sd[k] = torch.tensor(q8_0_decoder(q8_0_encoder(a), a.shape))
            n += 1
    modele.load_state_dict(sd)
    modele.eval()
    print(f"# référence : {n} tenseurs quantifiés en Q8_0 (les mêmes que l'export)")

    ids = np.array([int(v) for v in open(ids_path).read().strip().split(",")], dtype=np.int64)
    with torch.no_grad():
        logits = modele(torch.tensor(ids).unsqueeze(0)).logits[0].float().numpy()
    lg, cible = logits[:-1], ids[1:]
    mx = lg.max(axis=-1, keepdims=True)
    lse = mx[:, 0] + np.log(np.exp(lg - mx).sum(axis=-1))
    nll = float((lse - lg[np.arange(len(cible)), cible]).mean())
    print(f"# référence : {len(cible)} prédictions · NLL {nll:.4f} nats · perplexité {np.exp(nll):.4f}")
    with open(sortie, "wb") as f:
        f.write(np.int32([logits.shape[1]]).tobytes())
        f.write(np.int32([logits.shape[0]]).tobytes())
        f.write(logits.astype(np.float32).tobytes())
    print(f"# logits écrits : {sortie}")
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--hf", required=True)
    p.add_argument("--gguf", default="")
    p.add_argument("--logits", default="")
    p.add_argument("--ids", default="")
    a = p.parse_args()
    cfg = json.load(open(os.path.join(a.hf, "config.json")))
    if a.gguf:
        # Les petits modèles de test n'ont pas toujours de safetensors : on lit
        # ce qui est là, dans l'ordre du plus sûr au plus ancien.
        poids = None
        for nom in ("model.safetensors", "pytorch_model.bin"):
            chemin = os.path.join(a.hf, nom)
            if not os.path.exists(chemin):
                continue
            if nom.endswith(".safetensors"):
                from safetensors.numpy import load_file
                poids = load_file(chemin)
            else:
                import torch
                brut = torch.load(chemin, map_location="cpu", weights_only=True)
                poids = {k: v.float().numpy() for k, v in brut.items()}
            break
        if poids is None:
            sys.exit(f"aucun poids lisible dans {a.hf}")
        tenseurs = tenseurs_depuis_hf(poids, cfg)
        octets = ecrire_gguf(a.gguf, kv_depuis_config(cfg), tenseurs)
        print(f"# {a.gguf} : {len(tenseurs)} tenseurs · {octets/1e6:.2f} Mo · "
              f"{cfg['num_hidden_layers']} couches · {cfg['hidden_size']} cachés")
    if a.logits and a.ids:
        return reference(a.hf, a.ids, a.logits)
    return 0


if __name__ == "__main__":
    sys.exit(main())

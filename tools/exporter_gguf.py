#!/usr/bin/env python3
"""exporter_gguf.py — écrire un GGUF que Drave exécute, depuis un modèle PyTorch.

POURQUOI. L'objectif du chantier demande une **porte d'exécution** : que le
modèle entraîné ici tourne dans le MOTEUR, et pas seulement dans PyTorch. Le
moteur lit le GGUF en place et n'a pas de convertisseur ; ce fichier est ce
convertisseur, pour la famille MoE qu'il exécute déjà — routeur
`ffn_gate_inp.weight`, experts SwiGLU `ffn_{gate,up,down}_exps.weight`, normes
RMS, RoPE « neox », GQA. C'est la famille de Qwen3-30B-A3B, dont la porte est
tenue à **799,8557** (`tools/portes.sh`), donc le chemin est vérifié.

CE QU'IL FAUT RESPECTER, ET QUI SE PAIE CASH SINON :
  * les dims sont écrites **à l'envers** (ggml range la plus rapide d'abord) —
    le moteur les remet en convention numpy à la lecture (`gguf.rs`) ;
  * les experts sont en **[n_expert, n_ff, n_embd]** (`ffn_down_exps` :
    [n_expert, n_embd, n_ff]) ;
  * `gate_up_proj` de HF est FUSIONNÉ : `gate` = première moitié, `up` = seconde
    (`modeling_qwen3_moe.py` : `.chunk(2, dim=-1)`) ;
  * `norm_topk_prob` doit être déclaré (`expert_weights_norm`), sinon le moteur
    ne renormalise pas les poids du top-k et le routage change EN SILENCE ;
  * l'alignement des données est de 32 octets (le moteur le lit dans l'en-tête).

MODÈLE ENTRANT : un dossier `save_pretrained` de `Qwen3MoeForCausalLM`
(config.json + model.safetensors), à n'importe quelle taille.

Usage :
    exporter_gguf.py --hf modele_hf/ --sortie modele.gguf [--f16]
"""
import argparse
import json
import os
import struct
import sys

import numpy as np

GGML_F32, GGML_F16 = 0, 1
GGML_Q4_0, GGML_Q8_0 = 2, 8
GGUF_VERSION = 3
ALIGNEMENT = 32


# ------------------------------------------------------------------ Q8_0
# Les projections DENSES (attention, tête, embedding, routeur) sont lues par le
# moteur en Q8_0 : `q8_view` refuse tout autre type (« type 0 non géré » pour un
# F32). Q8_0 est donc le format d'échange, et l'écrire ici évite de dépendre d'un
# convertisseur externe.
def q8_0_encoder(a):
    """Blocs de 32 : échelle f16 (`amax/127`) puis 32 entiers signés."""
    a = np.ascontiguousarray(a, dtype=np.float32)
    assert a.shape[-1] % 32 == 0, f"dernière dimension non multiple de 32 : {a.shape}"
    plat = a.reshape(-1, 32)
    amax = np.abs(plat).max(axis=1)
    d = (amax / 127.0).astype(np.float32)
    inv = np.where(d != 0, 1.0 / np.where(d == 0, 1.0, d), 0.0).astype(np.float32)
    q = np.clip(np.rint(plat * inv[:, None]), -127, 127).astype(np.int8)
    octets = np.empty((plat.shape[0], 34), dtype=np.uint8)
    octets[:, :2] = d.astype(np.float16).view(np.uint8).reshape(-1, 2)
    octets[:, 2:] = q.view(np.uint8)
    return octets.tobytes()


def q8_0_decoder(brut, forme):
    a = np.frombuffer(brut, dtype=np.uint8).reshape(-1, 34)
    d = a[:, :2].copy().view(np.float16).reshape(-1).astype(np.float32)
    q = a[:, 2:].copy().view(np.int8).astype(np.float32)
    return (q * d[:, None]).reshape(forme)


# ------------------------------------------------------------------- Q4_0
# Le moteur n'a de noyau (ni de déquantification) que pour une liste de formats
# d'experts : Q4_K, Q6_K, MXFP4, Q4_0 et les super-blocs « sans noyau ». Un
# tenseur d'experts en F32 est REFUSÉ — « format sans noyau ni déquantification »
# — et la couche retombe alors sur une FFN dense… qui n'existe pas : le
# chargement meurt sur « blk.0.ffn_gate.weight absent ». Q4_0 est le plus simple
# à écrire exactement, et il est relu par un vrai noyau.
def q4_0_encoder(a):
    """Blocs de 32 poids : échelle f16 puis 16 octets (nibbles bas = 0..15,
    nibbles hauts = 16..31). Reproduction de `quantize_row_q4_0_ref` de ggml —
    `d = max_signe / -8`, `q = min(15, tronc(v/d + 8,5))`."""
    a = np.ascontiguousarray(a, dtype=np.float32)
    assert a.shape[-1] % 32 == 0, (
        f"dernière dimension {a.shape} non multiple de 32 : les blocs ggml font 32 poids, "
        f"et le moteur REFUSE une couche dont l'entrée n'est pas un multiple de 32. "
        f"Choisir une largeur d'expert multiple de 32.")
    plat = a.reshape(-1, 32)
    idx = np.abs(plat).argmax(axis=1)
    mx = plat[np.arange(plat.shape[0]), idx]
    d = (mx / -8.0).astype(np.float32)
    inv = np.where(d != 0, 1.0 / np.where(d == 0, 1.0, d), 0.0).astype(np.float32)
    q = np.clip(np.floor(plat * inv[:, None] + 8.5), 0, 15).astype(np.uint8)
    octets = np.empty((plat.shape[0], 18), dtype=np.uint8)
    octets[:, :2] = d.astype(np.float16).view(np.uint8).reshape(-1, 2)
    octets[:, 2:] = (q[:, :16] | (q[:, 16:] << 4)).astype(np.uint8)
    return octets.tobytes()


def q4_0_decoder(brut, forme):
    """Le chemin inverse — c'est lui qui fabrique la RÉFÉRENCE en PyTorch.

    Sans lui, la comparaison moteur/référence mesurerait la quantification Q4_0
    au lieu du calcul du moteur : les deux côtés doivent partir des MÊMES poids.
    """
    a = np.frombuffer(brut, dtype=np.uint8).reshape(-1, 18)
    d = a[:, :2].copy().view(np.float16).reshape(-1).astype(np.float32)
    qs = a[:, 2:]
    bas = (qs & 0x0F).astype(np.float32) - 8.0
    haut = ((qs >> 4) & 0x0F).astype(np.float32) - 8.0
    plat = np.concatenate([bas, haut], axis=1) * d[:, None]
    return plat.reshape(forme)


def _chaine(f, texte):
    b = texte.encode("utf-8")
    f.write(struct.pack("<Q", len(b)))
    f.write(b)


def _kv(f, cle, val):
    _chaine(f, cle)
    if isinstance(val, bool):
        f.write(struct.pack("<I", 7))
        f.write(struct.pack("<?", val))
    elif isinstance(val, int):
        f.write(struct.pack("<I", 4))
        f.write(struct.pack("<I", val))
    elif isinstance(val, float):
        f.write(struct.pack("<I", 6))
        f.write(struct.pack("<f", val))
    elif isinstance(val, str):
        f.write(struct.pack("<I", 8))
        _chaine(f, val)
    elif isinstance(val, (list, tuple)) and val and isinstance(val[0], str):
        f.write(struct.pack("<I", 9))          # tableau
        f.write(struct.pack("<I", 8))          # d'éléments de type chaîne
        f.write(struct.pack("<Q", len(val)))
        for v in val:
            _chaine(f, v)
    else:
        raise TypeError(f"type GGUF non géré pour {cle} : {type(val)}")


def ecrire_gguf(chemin, kv, tenseurs, f16=False):
    """`tenseurs` : liste de (nom, tableau numpy) — tableau converti en f32/f16 —
    ou de (nom, (octets, type_ggml)) pour un format écrit à la main (Q4_0)."""
    with open(chemin, "wb") as f:
        f.write(b"GGUF")
        f.write(struct.pack("<I", GGUF_VERSION))
        f.write(struct.pack("<Q", len(tenseurs)))
        f.write(struct.pack("<Q", len(kv)))
        for cle, val in kv:
            _kv(f, cle, val)
        decalage = 0
        donnees = []
        for nom, contenu in tenseurs:
            if isinstance(contenu, tuple):          # (octets, ttype, forme)
                brut, ttype, forme = contenu
                dims, octets = forme, brut
            else:
                a = np.ascontiguousarray(contenu.astype(np.float16 if f16 else np.float32))
                ttype = GGML_F16 if f16 else GGML_F32
                dims, octets = a.shape, a.tobytes()
            _chaine(f, nom)
            f.write(struct.pack("<I", len(dims)))
            for d in reversed(dims):        # ggml range à l'envers
                f.write(struct.pack("<Q", int(d)))
            f.write(struct.pack("<I", ttype))
            f.write(struct.pack("<Q", decalage))
            decalage += len(octets)
            donnees.append(octets)
        fin = f.tell()
        f.write(b"\0" * ((ALIGNEMENT - fin % ALIGNEMENT) % ALIGNEMENT))
        for o in donnees:
            f.write(o)
    return sum(len(o) for o in donnees)


def _poids(dossier):
    from safetensors.numpy import load_file
    return load_file(os.path.join(dossier, "model.safetensors"))


def _experts(poids, p, n_exp):
    """Les trois projections d'experts, dans les DEUX dispositions possibles.

    Le même modèle se présente de deux façons selon le chemin : en mémoire (et
    pour les modèles récents), les experts sont FUSIONNÉS
    (`experts.gate_up_proj`, forme (E, 2·ff, d), `gate` = première moitié —
    `modeling_qwen3_moe.py` fait `.chunk(2, dim=-1)`) ; sur disque, ils sont
    souvent écrits UN PAR UN (`experts.{e}.gate_proj.weight`). Lire la mauvaise
    disposition ne lève aucune erreur de forme : on empile les mauvais tenseurs
    et le modèle tourne avec d'autres poids.
    """
    if p + "mlp.experts.gate_up_proj" in poids:
        gu = poids[p + "mlp.experts.gate_up_proj"]
        n_ff = gu.shape[1] // 2
        return gu[:, :n_ff, :], gu[:, n_ff:, :], poids[p + "mlp.experts.down_proj"]
    gate = np.stack([poids[f"{p}mlp.experts.{e}.gate_proj.weight"] for e in range(n_exp)])
    up = np.stack([poids[f"{p}mlp.experts.{e}.up_proj.weight"] for e in range(n_exp)])
    down = np.stack([poids[f"{p}mlp.experts.{e}.down_proj.weight"] for e in range(n_exp)])
    return gate, up, down


def tenseurs_depuis_hf(poids, cfg, experts_q4=True):
    """La table de conversion, et les pièges qu'elle évite (cf. docstring).

    Les tenseurs 2D sont écrits en **Q8_0** : c'est le type que `q8_view` et
    l'emprunt de blocs attendent côté moteur. Les normes (1D) restent en F32 —
    les quantifier n'apporterait rien et changerait le calcul.
    """
    n_l = cfg["num_hidden_layers"]
    est_moe = _arch(cfg) == "qwen3moe"
    n_exp = int(cfg.get("num_experts", cfg.get("num_local_experts")) or 0)

    def q8(nom, arr):
        return (nom, (q8_0_encoder(arr), GGML_Q8_0, arr.shape))

    t = [q8("token_embd.weight", poids["model.embed_tokens.weight"]),
         ("output_norm.weight", poids["model.norm.weight"])]
    # Embeddings liés (Qwen3) : le moteur exige la tête, on la donne.
    t.append(q8("output.weight", poids.get("lm_head.weight", poids["model.embed_tokens.weight"])))
    for l in range(n_l):
        p, b = f"model.layers.{l}.", f"blk.{l}."
        t += [("blk.%d.attn_norm.weight" % l, poids[p + "input_layernorm.weight"]),
              q8(b + "attn_q.weight", poids[p + "self_attn.q_proj.weight"]),
              q8(b + "attn_k.weight", poids[p + "self_attn.k_proj.weight"]),
              q8(b + "attn_v.weight", poids[p + "self_attn.v_proj.weight"]),
              q8(b + "attn_output.weight", poids[p + "self_attn.o_proj.weight"]),
              (b + "ffn_norm.weight", poids[p + "post_attention_layernorm.weight"])]
        if est_moe:
            # Le ROUTEUR n'existe que dans la famille MoE : l'ajouter à un modèle
            # dense lève une KeyError sur `mlp.gate.weight` — nom qui, dans un
            # dense, désigne la PREMIÈRE matrice du SwiGLU, pas un routeur.
            t.append(q8(b + "ffn_gate_inp.weight", poids[p + "mlp.gate.weight"]))
        if p + "self_attn.q_norm.weight" in poids:
            t += [(b + "attn_q_norm.weight", poids[p + "self_attn.q_norm.weight"]),
                  (b + "attn_k_norm.weight", poids[p + "self_attn.k_norm.weight"])]
        if est_moe:
            gate, up, down = _experts(poids, p, n_exp)
            for nom, arr in (("ffn_gate_exps.weight", gate), ("ffn_up_exps.weight", up),
                             ("ffn_down_exps.weight", down)):
                if experts_q4:
                    t.append((b + nom, (q4_0_encoder(arr), GGML_Q4_0, arr.shape)))
                else:
                    t.append((b + nom, arr))
        else:
            # Jumeau dense : sa FFN peut être quantifiée en Q4_0 COMME les experts
            # du routé. Sans cela, la comparaison « à lecture égale » serait
            # faussée d'un facteur 1,8 sur les octets — le routé stockant ses
            # experts en 4 bits et le dense sa FFN en 8.
            for nom, cle in (("ffn_gate.weight", "mlp.gate_proj.weight"),
                             ("ffn_up.weight", "mlp.up_proj.weight"),
                             ("ffn_down.weight", "mlp.down_proj.weight")):
                arr = poids[p + cle]
                if experts_q4:
                    t.append((b + nom, (q4_0_encoder(arr), GGML_Q4_0, arr.shape)))
                else:
                    t.append(q8(b + nom, arr))
    return t


def quant_du_tenseur(nom_hf):
    """Quel type GGUF l'export écrit pour ce tenseur — 'q4', 'q8', ou None.

    LA MÊME règle sert à l'export ET à la référence (`porte_moteur.py`) : sans ce
    point unique, la référence quantifiait la FFN dense en Q8_0 là où l'export
    l'écrivait en Q4_0, et la « porte » comparait deux quantifications
    différentes au lieu de comparer le moteur à la référence.
    """
    if "gate_up_proj" in nom_hf:
        return "q4"                                    # experts fusionnés (MoE)
    if ".mlp." in nom_hf and nom_hf.endswith(("gate_proj.weight", "up_proj.weight",
                                              "down_proj.weight")):
        return "q4"                                    # experts éclatés, ou FFN dense
    if nom_hf.endswith(".weight"):
        return "q8"
    return None


def _arch(cfg):
    """Le nom d'architecture que le moteur lira dans `general.architecture` :
    c'est lui qui préfixe TOUTES les clefs de configuration (`gguf.rs::cfg`)."""
    mt = cfg.get("model_type", "qwen3_moe")
    return "qwen3" if mt == "qwen3" else "qwen3moe"


def kv_depuis_config(cfg):
    arch = _arch(cfg)
    est_moe = arch == "qwen3moe"
    rope = cfg.get("rope_parameters") or {}
    theta = float(rope.get("rope_theta", cfg.get("rope_theta", 10000.0)))
    n_tete = cfg["num_attention_heads"]
    d = cfg["hidden_size"]
    kv = [
        ("general.architecture", arch),
        ("general.name", cfg.get("_name_or_path", "modele-drave")),
        ("general.file_type", 0),
        (f"{arch}.block_count", int(cfg["num_hidden_layers"])),
        (f"{arch}.context_length", int(cfg.get("max_position_embeddings", 2048))),
        (f"{arch}.embedding_length", int(d)),
        (f"{arch}.feed_forward_length", int(cfg.get("intermediate_size", 4 * d))),
        (f"{arch}.attention.head_count", int(n_tete)),
        (f"{arch}.attention.head_count_kv", int(cfg.get("num_key_value_heads", n_tete))),
        (f"{arch}.attention.key_length", int(cfg.get("head_dim", d // n_tete))),
        (f"{arch}.attention.value_length", int(cfg.get("head_dim", d // n_tete))),
        (f"{arch}.attention.layer_norm_rms_epsilon", float(cfg.get("rms_norm_eps", 1e-6))),
        (f"{arch}.rope.freq_base", theta),
    ]
    if not est_moe:
        return kv
    # Transformers 5 nomme le champ `num_local_experts` (héritage Mixtral) là où
    # les cartes de Qwen disent `num_experts` : lire le mauvais nom ne lève pas
    # d'erreur, il écrit `expert_count = 0` — et le moteur exécute alors un
    # modèle SANS experts, en silence.
    n_exp = cfg.get("num_experts", cfg.get("num_local_experts"))
    if not n_exp:
        raise KeyError("ni num_experts ni num_local_experts dans la configuration")
    kv += [
        (f"{arch}.expert_count", int(n_exp)),
        (f"{arch}.expert_used_count", int(cfg["num_experts_per_tok"])),
        (f"{arch}.expert_feed_forward_length", int(cfg["moe_intermediate_size"])),
        # Le drapeau qui, oublié, change le routage en silence.
        (f"{arch}.expert_weights_norm", bool(cfg.get("norm_topk_prob", True))),
    ]
    return kv


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--hf", required=True, help="dossier save_pretrained (config.json + safetensors)")
    p.add_argument("--sortie", required=True)
    p.add_argument("--f16", action="store_true")
    a = p.parse_args()
    cfg = json.load(open(os.path.join(a.hf, "config.json")))
    poids = _poids(a.hf)
    kv = kv_depuis_config(cfg)
    tenseurs = tenseurs_depuis_hf(poids, cfg, experts_q4=True)
    octets = ecrire_gguf(a.sortie, kv, tenseurs, a.f16)
    print(f"# {a.sortie} : {len(tenseurs)} tenseurs · {octets/1e6:.1f} Mo "
          f"({'f16' if a.f16 else 'f32'} pour les normes, Q8_0 pour les projections, "
          f"Q4_0 pour la FFN et les experts) · {len(kv)} métadonnées")
    n_exp = cfg.get("num_experts", cfg.get("num_local_experts"))
    detail = (f"{n_exp} experts (top-{cfg['num_experts_per_tok']}) · "
              f"norm_topk_prob={cfg.get('norm_topk_prob', True)}" if n_exp else "FFN dense")
    print(f"# architecture {cfg['num_hidden_layers']} couches · {cfg['hidden_size']} cachés · {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

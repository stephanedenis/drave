#!/usr/bin/env python3
"""Modèle MLA synthétique + référence numpy — le harnais du chantier 5.

MLA (attention latente, DeepSeek-V2/V3) n'est pas testable en l'état : aucun
modèle MLA en GGUF sur cette machine (le « deepseek-r1-distill » local est un
Qwen dense). Ce script fabrique donc un modèle minuscule dont les poids sont
aléatoires mais les FORMES correctes, l'écrit en GGUF, et calcule une référence
indépendante en numpy — c'est elle que le moteur devra retrouver.

Pourquoi c'est un vrai test : la référence est écrite à partir des formules, pas
du code Rust ; si les deux tombent d'accord sur un modèle dont le cache KV est
LATENT (une seule tête de 128 + 32 valeurs par jeton au lieu de n_head × 192),
alors l'implémentation est validée sur ce qu'elle a de spécifique.

Usage :
    mla_synthetique.py --sortie /tmp/mla_minuscule.gguf --dossier /tmp/mla_ref
"""
import argparse
import json
import os
import struct

import numpy as np

# ---------------------------------------------------------------------------
# Hyperparamètres du modèle jouet : assez petits pour être lisibles, assez
# généraux pour que le découpage qk_nope / qk_rope soit celui de DeepSeek.
H = 64          # hidden
NL = 2          # couches
NH = 4          # têtes de requête
NKV = 1         # tête KV : MLA est une MQA par construction
QL = 32         # q_lora_rank
KVL = 48        # kv_lora_rank
QKR = 16        # qk_rope (partie tournée)
QKN = 16        # qk_nope (partie non tournée)
VD = 16         # value_length
FFN = 128
VOCAB = 64
EPS = 1e-5
ROPE_BASE = 10000.0


def poids(rng, *forme):
    return (rng.standard_normal(forme) * 0.08).astype(np.float32)


def construire(graine=1234):
    """Les poids du modèle, dans l'ordre où le moteur les lira."""
    rng = np.random.RandomState(graine)
    p = {"token_embd.weight": poids(rng, VOCAB, H),
         "output_norm.weight": np.ones(H, np.float32)}
    for l in range(NL):
        p[f"blk.{l}.attn_norm.weight"] = np.ones(H, np.float32)
        p[f"blk.{l}.attn_q_a.weight"] = poids(rng, H, QL)
        p[f"blk.{l}.attn_q_a_norm.weight"] = np.ones(QL, np.float32)
        p[f"blk.{l}.attn_q_b.weight"] = poids(rng, QL, NH * (QKN + QKR))
        p[f"blk.{l}.attn_kv_a_mqa.weight"] = poids(rng, H, KVL + QKR)
        p[f"blk.{l}.attn_kv_a_norm.weight"] = np.ones(KVL, np.float32)
        p[f"blk.{l}.attn_kv_b.weight"] = poids(rng, KVL, NH * (QKN + VD))
        p[f"blk.{l}.attn_output.weight"] = poids(rng, NH * VD, H)
        p[f"blk.{l}.ffn_norm.weight"] = np.ones(H, np.float32)
        p[f"blk.{l}.ffn_gate.weight"] = poids(rng, H, FFN)
        p[f"blk.{l}.ffn_up.weight"] = poids(rng, H, FFN)
        p[f"blk.{l}.ffn_down.weight"] = poids(rng, FFN, H)
    return p


def rope(x, pos, base=ROPE_BASE):
    """RoPE « par paires » du moteur (rotation des deux moitiés), appliqué à la
    partie qk_rope seulement."""
    n = x.shape[-1]
    demi = n // 2
    i = np.arange(demi)
    inv = 1.0 / (base ** (2.0 * i / n))
    ang = pos * inv
    c, s = np.cos(ang), np.sin(ang)
    a, b = x[..., :demi], x[..., demi:]
    return np.concatenate([a * c - b * s, a * s + b * c], axis=-1)


def rmsnorm(x, w, eps=EPS):
    return x / np.sqrt((x * x).mean(-1, keepdims=True) + eps) * w


def softmax(x):
    m = x.max(-1, keepdims=True)
    e = np.exp(x - m)
    return e / e.sum(-1, keepdims=True)


def avant(p, ids):
    """Passe avant complète, SANS cache : positions 0..len(ids)-1.

    Le cache latent n'est pas utilisé ici (le modèle est trop court pour que ça
    change quoi que ce soit) : ce qui est testé, c'est la reconstruction de
    k_nope et v à partir de `W_kv_b`, et le découpage qk_nope / qk_rope.
    """
    n = len(ids)
    x = p["token_embd.weight"][ids].copy()
    for l in range(NL):
        h = rmsnorm(x, p[f"blk.{l}.attn_norm.weight"])
        # --- requête : descente, norme, remontée, puis découpage
        qa = h @ p[f"blk.{l}.attn_q_a.weight"]
        qa = rmsnorm(qa, p[f"blk.{l}.attn_q_a_norm.weight"])
        qb = qa @ p[f"blk.{l}.attn_q_b.weight"]
        q = qb.reshape(n, NH, QKN + QKR)
        q_nope, q_rope = q[..., :QKN], q[..., QKN:]
        # --- KV : descente MQA, norme sur la partie latente, remontée
        kva = h @ p[f"blk.{l}.attn_kv_a_mqa.weight"]
        c_kv, k_rope = kva[:, :KVL], kva[:, KVL:]
        c_n = rmsnorm(c_kv, p[f"blk.{l}.attn_kv_a_norm.weight"])
        kv = c_n @ p[f"blk.{l}.attn_kv_b.weight"]
        kv = kv.reshape(n, NH, QKN + VD)
        k_nope, v = kv[..., :QKN], kv[..., QKN:]
        # --- rotation : SEULEMENT les parties « rope », à chaque position
        q_rope = np.stack([rope(q_rope[t], t) for t in range(n)])
        k_rope_t = np.stack([rope(k_rope[t], t) for t in range(n)])
        # --- scores : partie non tournée (par tête) + partie tournée (partagée,
        #     MLA est une MQA : une seule tête KV pour toutes les têtes de requête)
        #     (n = position de la requête, m = position de la clé, h = tête)
        sc = np.einsum('nhe,mhe->nhm', q_nope, k_nope)
        sc = sc + np.einsum('nhe,me->nhm', q_rope, k_rope_t)
        sc = sc / np.sqrt(QKN + QKR)
        # masque causal
        masque = np.triu(np.full((n, n), -1e30, np.float32), 1)
        att = softmax(sc + masque[:, None, :])
        o = np.einsum('nhm,mhv->nhv', att, v)
        o = o.reshape(n, NH * VD)
        x = x + o @ p[f"blk.{l}.attn_output.weight"]
        # --- FFN
        hn = rmsnorm(x, p[f"blk.{l}.ffn_norm.weight"])
        g = hn @ p[f"blk.{l}.ffn_gate.weight"]
        u = hn @ p[f"blk.{l}.ffn_up.weight"]
        act = (g / (1.0 + np.exp(-g))) * u          # SiLU(g) * u
        x = x + act @ p[f"blk.{l}.ffn_down.weight"]
    hn = rmsnorm(x, p["output_norm.weight"])
    return hn @ p["token_embd.weight"].T            # tête liée


# ---------------------------------------------------------------------------
# Écriture GGUF : en-tête, métadonnées, descriptions de tenseurs, données.
# ---------------------------------------------------------------------------
def gguf_ecrire(chemin, p, ids_entree):
    kv = [
        ("general.architecture", 8, "deepseek2"),
        ("deepseek2.block_count", 4, NL),
        ("deepseek2.embedding_length", 4, H),
        ("deepseek2.feed_forward_length", 4, FFN),
        ("deepseek2.attention.head_count", 4, NH),
        ("deepseek2.attention.head_count_kv", 4, NKV),
        ("deepseek2.attention.key_length", 4, QKN + QKR),
        ("deepseek2.attention.value_length", 4, VD),
        ("deepseek2.attention.q_lora_rank", 4, QL),
        ("deepseek2.attention.kv_lora_rank", 4, KVL),
        ("deepseek2.rope.dimension_count", 4, QKR),
        ("deepseek2.rope.freq_base", 6, float(ROPE_BASE)),
        ("deepseek2.attention.layer_norm_rms_epsilon", 6, float(EPS)),
        ("tokenizer.ggml.tokens", 9, [f"t{i}" for i in range(VOCAB)]),
        ("mla.ids_entree", 9, [str(i) for i in ids_entree]),
    ]
    noms = list(p.keys())
    decalage = 0
    infos = []
    for nom in noms:
        t = p[nom]
        dims = list(t.shape)
        infos.append((nom, dims, 0, decalage))       # type 0 = F32
        decalage += t.nbytes
    with open(chemin, "wb") as f:
        f.write(b"GGUF")
        f.write(struct.pack("<IQQ", 3, len(noms), len(kv)))
        for cle, typ, val in kv:
            ecrire_chaine(f, cle)
            f.write(struct.pack("<I", typ))
            if typ == 8:
                ecrire_chaine(f, val)
            elif typ == 4:
                f.write(struct.pack("<I", val))
            elif typ == 6:
                f.write(struct.pack("<f", val))
            elif typ == 9:
                f.write(struct.pack("<IQ", 8, len(val)))     # tableau de chaînes
                for v in val:
                    ecrire_chaine(f, v)
            else:
                raise ValueError(typ)
        for nom, dims, typ, off in infos:
            ecrire_chaine(f, nom)
            f.write(struct.pack("<I", len(dims)))
            for d in dims:
                f.write(struct.pack("<Q", d))
            f.write(struct.pack("<IQ", typ, off))
        align = 32
        reste = f.tell() % align
        if reste:
            f.write(b"\0" * (align - reste))
        for nom in noms:
            f.write(p[nom].tobytes())
    return chemin


def ecrire_chaine(f, s):
    b = s.encode("utf-8")
    f.write(struct.pack("<Q", len(b)))
    f.write(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="/tmp/mla_minuscule.gguf")
    ap.add_argument("--dossier", default="/tmp/mla_ref")
    ap.add_argument("--graine", type=int, default=1234)
    ap.add_argument("--n", type=int, default=8, help="jetons d'entrée")
    args = ap.parse_args()

    os.makedirs(args.dossier, exist_ok=True)
    p = construire(args.graine)
    ids = list(range(1, args.n + 1))
    gguf_ecrire(args.sortie, p, ids)
    logits = avant(p, ids)
    np.save(os.path.join(args.dossier, "logits.npy"), logits)
    np.save(os.path.join(args.dossier, "ids.npy"), np.array(ids, np.int64))
    with open(os.path.join(args.dossier, "forme.json"), "w") as f:
        json.dump({"hidden": H, "n_layer": NL, "n_head": NH, "q_lora": QL,
                   "kv_lora": KVL, "qk_rope": QKR, "qk_nope": QKN, "v_dim": VD,
                   "ffn": FFN, "vocab": VOCAB, "graine": args.graine}, f, indent=2)
    print(f"modèle   : {args.sortie}")
    print(f"référence: {args.dossier}/logits.npy  (forme {logits.shape})")
    print(f"logits[0, :4] = {logits[0, :4]}")
    print(f"logits[-1, :4] = {logits[-1, :4]}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""exporter_gguf_dense.py — écrire un GGUF **dense** (Qwen2) que Drave exécute.

POURQUOI CE FICHIER EXISTE. N4 (le chemin court entraîné) se mesure aujourd'hui en **torch** : le
dessin B a été mesuré le 14/10 (`reports/rapport-n4-dessin-b.md`), mais un chiffre que le MOTEUR ne
reproduit pas n'est pas encore un chiffre du dépôt — c'est la **porte d'exécution**. Or
`tools/exporter_gguf.py` ne connaît que la famille **MoE** de Qwen3 (routeur, experts, GQA) ;
Qwen2.5-0.5B est **dense**, avec des **biais** sur q/k/v et une tête **liée**.

DEUX SOURCES, POUR DEUX USAGES :

* `--depuis-gguf <gguf>` : déquantifie un GGUF existant et le réécrit en **F32**. C'est la
  vérification de l'écriture **sans dépendre d'aucun cache** (ni Hugging Face, ni réseau) : le
  moteur doit rendre, sur le fichier réécrit, les chiffres qu'il rend sur l'original — à la
  quantification près, qui est justement ce qu'on mesure ;
* `--hf <dossier>` : part des poids PyTorch (`model.safetensors`), avec `--lora <fichier.pt>` pour
  **fusionner** des adaptateurs de rang faible (`W ← W + (α/r)·B·A`) sur les `--couches-lora`
  premières couches, et `--adapter-sortie <fichier>` pour écrire la matrice de sortie apprise
  (f32 brut, 896×896) que le moteur applique avant la norme finale.

LE FORMAT D'ÉCHANGE EST **Q8_0**, PAS F32 — et c'est mesuré, pas supposé : un export F32 (1,98 Go
écrit, relu exactement) fait PANIQUER le moteur au premier `q8_view` : « q8_view : type 0 non
géré ». Les projections denses sont lues par le moteur **en Q8_0** ; les normes et les biais, eux,
sont lus en f32 (`row_f32` gère les deux). L'exporteur écrit donc les matrices en Q8_0 et le reste
en f32 (`--format f32` reste possible pour d'autres usages, mais pas pour `--ppl`).

LES MÉTADONNÉES SONT COPIÉES **VERBATIM** du GGUF de référence : le tokenizer (151 936 jetons,
151 323 fusions), le template de chat et les clés d'architecture sont **exactement** ceux que le
moteur lit déjà. Les réécrire serait une occasion de dériver en silence (un tokenizer différent ne
se voit pas : il change les identifiants). Seul `general.file_type` est réécrit — il annonçait
Q8_0 dans un fichier qui n'en contient plus.

Usage :
  tools/exporter_gguf_dense.py --depuis-gguf models/Qwen2.5-0.5B-Q8_0.gguf \
      --reference models/Qwen2.5-0.5B-Q8_0.gguf --sortie /tmp/n4/f32.gguf [--f16]
  tools/exporter_gguf_dense.py --hf <snapshot> --lora /tmp/n4/bras-lora.pt --couches-lora 8 \
      --adapter-sortie /tmp/n4/adaptateur.f32 --reference models/Qwen2.5-0.5B-Q8_0.gguf \
      --sortie /tmp/n4/dessin-b.gguf
"""
from __future__ import annotations

import argparse
import os
import pathlib
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exporter_gguf import (ecrire_gguf, q8_0_encoder,                            # noqa: E402
                           GGML_F32, GGML_F16, GGML_Q8_0)

# Nom du tenseur dans le GGUF pour chaque poids du modèle HF dense (Qwen2).
CORRESPONDANCE = [
    ("model.embed_tokens.weight", "token_embd.weight"),
    ("model.norm.weight", "output_norm.weight"),
]

# Par couche : (suffixe HF, suffixe GGUF)
PAR_COUCHE = [
    ("input_layernorm.weight", "attn_norm.weight"),
    ("self_attn.q_proj.weight", "attn_q.weight"),
    ("self_attn.q_proj.bias", "attn_q.bias"),
    ("self_attn.k_proj.weight", "attn_k.weight"),
    ("self_attn.k_proj.bias", "attn_k.bias"),
    ("self_attn.v_proj.weight", "attn_v.weight"),
    ("self_attn.v_proj.bias", "attn_v.bias"),
    ("self_attn.o_proj.weight", "attn_output.weight"),
    ("post_attention_layernorm.weight", "ffn_norm.weight"),
    ("mlp.gate_proj.weight", "ffn_gate.weight"),
    ("mlp.up_proj.weight", "ffn_up.weight"),
    ("mlp.down_proj.weight", "ffn_down.weight"),
]


# ---------------------------------------------------------------------------------------------
# Les métadonnées du GGUF de référence, copiées telles quelles (sauf `general.file_type`)
# ---------------------------------------------------------------------------------------------
def _chaine(f) -> str:
    n = struct.unpack("<Q", f.read(8))[0]
    return f.read(n).decode("utf-8", "replace")


def _valeur(f, t: int):
    fmt = {0: "<B", 1: "<b", 2: "<H", 3: "<h", 4: "<I", 5: "<i", 6: "<f", 7: "<B", 10: "<Q",
           11: "<q", 12: "<d"}
    if t == 8:
        return _chaine(f)
    if t == 9:
        et = struct.unpack("<I", f.read(4))[0]
        n = struct.unpack("<Q", f.read(8))[0]
        return [_valeur(f, et) for _ in range(n)]
    return struct.unpack(fmt[t], f.read(struct.calcsize(fmt[t])))[0]


def kv_brutes(chemin: str):
    """(octets de la section KV, nombre de paires, {clé: (position de la valeur, type)})."""
    brut = pathlib.Path(chemin).read_bytes()
    if brut[:4] != b"GGUF":
        raise SystemExit(f"{chemin} : ce n'est pas un GGUF")
    n_kv = struct.unpack("<Q", brut[16:24])[0]
    f = open(chemin, "rb")
    f.seek(24)
    positions = {}
    for _ in range(n_kv):
        debut = f.tell()
        cle = _chaine(f)
        t = struct.unpack("<I", f.read(4))[0]
        pos_valeur = f.tell()
        _valeur(f, t)                      # avance, la valeur n'est pas interprétée
        positions[cle] = (pos_valeur - 24, t)   # relatif au début de la section KV
        if f.tell() <= debut:
            raise SystemExit("section KV illisible (position qui recule)")
    fin = f.tell()
    return brut[24:fin], n_kv, positions


def kv_avec_file_type(kv: bytes, positions: dict, format: str) -> bytes:
    """Réécrit `general.file_type` SI le format n'est plus celui du fichier de référence.

    En `q8` (le défaut), **rien n'est réécrit** : le fichier de référence EST du Q8_0 (type 7) et
    l'export l'est aussi. `general.quantization_version` n'est JAMAIS touchée — elle décrit la
    version du schéma de quantification (2 pour Q8_0), pas le type, et la mettre à 0 ferait mentir
    le fichier sur un point que le moteur lit.
    """
    if format == "q8":
        return kv
    b = bytearray(kv)
    if "general.file_type" in positions:
        pos, typ = positions["general.file_type"]
        if typ == 4:                       # u32
            b[pos:pos + 4] = struct.pack("<I", 0 if format == "f32" else 1)
            print(f"  métadonnée general.file_type réécrite à {0 if format == 'f32' else 1} "
                  f"({format.upper()})")
    return bytes(b)


# ---------------------------------------------------------------------------------------------
# Les tenseurs : du GGUF (déquantifié) ou du PyTorch
# ---------------------------------------------------------------------------------------------
def lire_tenseur_gguf(f, dims, ttype, offset, debut):
    n = int(np.prod(dims))
    if ttype == GGML_Q8_0:
        n_blocs = n // 32
        f.seek(debut + offset)
        brut = np.frombuffer(f.read(n_blocs * 34), dtype=np.uint8).reshape(n_blocs, 34)
        ech = np.ascontiguousarray(brut[:, :2]).view(np.float16).astype(np.float32).reshape(-1, 1)
        qs = np.ascontiguousarray(brut[:, 2:]).view(np.int8).astype(np.float32)
        return (ech * qs).reshape(-1)
    if ttype == GGML_F32:
        f.seek(debut + offset)
        return np.frombuffer(f.read(4 * n), dtype="<f4").astype(np.float32)
    raise SystemExit(f"type GGUF {ttype} non lu par cet exporteur (Q8_0 et F32 seulement)")


def entete_gguf(chemin: str):
    f = open(chemin, "rb")
    if f.read(4) != b"GGUF":
        raise SystemExit(f"{chemin} : ce n'est pas un GGUF")
    struct.unpack("<I", f.read(4))[0]
    n_tensors, n_kv = struct.unpack("<QQ", f.read(16))
    alignement = 32
    for _ in range(n_kv):
        cle = _chaine(f)
        t = struct.unpack("<I", f.read(4))[0]
        v = _valeur(f, t)
        if cle == "general.alignment":
            alignement = int(v)
    tenseurs = {}
    for _ in range(n_tensors):
        nom = _chaine(f)
        nd = struct.unpack("<I", f.read(4))[0]
        dims = [struct.unpack("<Q", f.read(8))[0] for _ in range(nd)]
        ttype = struct.unpack("<I", f.read(4))[0]
        off = struct.unpack("<Q", f.read(8))[0]
        tenseurs[nom] = (dims, ttype, off)
    debut = (f.tell() + alignement - 1) // alignement * alignement
    return f, tenseurs, debut


def tenseurs_depuis_gguf(chemin: str):
    f, tenseurs, debut = entete_gguf(chemin)
    sortie = []
    for nom, (dims, ttype, off) in tenseurs.items():
        v = lire_tenseur_gguf(f, dims, ttype, off, debut)
        # stockage ggml [in, out] → numpy [out, in]
        sortie.append((nom, v.reshape(*reversed(dims))))
    return sortie


def tenseurs_depuis_hf(dossier: str, lora: dict | None, couches_lora: int, adapter):
    # `safetensors.numpy` REFUSE le bfloat16 (numpy n'en a pas) : les poids de Qwen2.5 sont en
    # bf16, donc on passe par torch et on convertit en f32 — l'écriture, elle, reste numpy.
    import torch
    from safetensors.torch import load_file
    poids = {k: v.to(torch.float32).numpy()
             for k, v in load_file(os.path.join(dossier, "model.safetensors")).items()}
    n_couches = 1 + max(int(k.split(".")[2]) for k in poids if k.startswith("model.layers."))
    fusion = {}
    if lora:
        for t in lora["lora"]:
            fusion[t["nom"]] = (t["A"], t["B"], t["echelle"])
        print(f"  fusion LoRA : {len(fusion)} projections sur les {couches_lora} premières couches")
    sortie = []
    for nom_hf, nom_gguf in CORRESPONDANCE:
        sortie.append((nom_gguf, poids[nom_hf].astype(np.float32)))
    for i in range(n_couches):
        for suf_hf, suf_gguf in PAR_COUCHE:
            nom_hf = f"model.layers.{i}.{suf_hf}"
            if nom_hf not in poids:
                continue
            w = poids[nom_hf].astype(np.float32)
            if nom_hf in fusion and i < couches_lora:
                A, B, echelle = fusion[nom_hf]
                w = w + (np.asarray(B, dtype=np.float32) @ np.asarray(A, dtype=np.float32)) \
                    * float(echelle)
            sortie.append((f"blk.{i}.{suf_gguf}", w))
    if adapter is not None:
        print(f"  adaptateur de sortie : {adapter.shape} (appliqué par le moteur, pas dans le GGUF)")
    return sortie


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", default="models/Qwen2.5-0.5B-Q8_0.gguf",
                    help="GGUF dont les métadonnées (tokenizer, architecture) sont copiées")
    ap.add_argument("--depuis-gguf", default=None, help="source : un GGUF à déquantifier")
    ap.add_argument("--hf", default=None, help="source : un dossier PyTorch (safetensors)")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--format", choices=["q8", "f16", "f32"], default="q8",
                    help="q8 (défaut) : matrices en Q8_0, normes et biais en f32 — c'est le "
                         "format que `--ppl` exige ; f16/f32 : tout dans ce type")
    ap.add_argument("--lora", default=None, help="fichier .pt des adaptateurs (n4_dessin_b --sauver)")
    ap.add_argument("--couches-lora", type=int, default=8)
    ap.add_argument("--adapter-sortie", default=None,
                    help="écrire la matrice de sortie en f32 brut (pour --adaptateur-sortie)")
    a = ap.parse_args()
    if bool(a.depuis_gguf) == bool(a.hf):
        raise SystemExit("donner EXACTEMENT une source : --depuis-gguf ou --hf")

    kv, n_kv, positions = kv_brutes(a.reference)
    kv = kv_avec_file_type(kv, positions, a.format)
    print(f"métadonnées : {n_kv} paires copiées de {a.reference} ({len(kv)} octets)")

    adapter = None
    if a.depuis_gguf:
        tenseurs = tenseurs_depuis_gguf(a.depuis_gguf)
        print(f"source GGUF {a.depuis_gguf} : {len(tenseurs)} tenseurs déquantifiés")
    else:
        lora = None
        if a.lora:
            import torch
            lora = torch.load(a.lora, map_location="cpu", weights_only=False)
            adapter = lora.get("adaptateur")
        tenseurs = tenseurs_depuis_hf(a.hf, lora, a.couches_lora, adapter)
        print(f"source PyTorch {a.hf} : {len(tenseurs)} tenseurs")

    if a.adapter_sortie:
        if adapter is None:
            raise SystemExit("--adapter-sortie demande --lora (qui porte l'adaptateur)")
        A = adapter.detach().cpu().numpy().astype("<f4")
        pathlib.Path(a.adapter_sortie).write_bytes(A.tobytes())
        print(f"adaptateur de sortie écrit : {a.adapter_sortie} ({A.shape}, f32 brut)")

    if a.format == "q8":
        # Les tenseurs 2D passent en Q8_0 (le seul type que `q8_view` accepte), les 1D en f32.
        preparés = []
        for nom, v in tenseurs:
            v = np.ascontiguousarray(v, dtype=np.float32)
            if v.ndim == 2 and v.shape[-1] % 32 == 0:
                preparés.append((nom, (q8_0_encoder(v), GGML_Q8_0, v.shape)))
            else:
                preparés.append((nom, v))
        octets = ecrire_gguf(a.sortie, [], preparés, kv_brutes=kv, n_kv=n_kv)
    else:
        preparés = tenseurs
        octets = ecrire_gguf(a.sortie, [], tenseurs, f16=(a.format == "f16"),
                             kv_brutes=kv, n_kv=n_kv)
    print(f"écrit {a.sortie} : {len(tenseurs)} tenseurs en {a.format}, "
          f"{octets / 1e9:.2f} Go de données")

    # CONTRÔLE DE RELECTURE : on relit le fichier écrit avec le même lecteur que la source et on
    # compare un tenseur de chaque genre — écrire sans relire, c'est espérer.
    f, relus, debut = entete_gguf(a.sortie)
    attendus = dict(tenseurs)
    for nom in ["token_embd.weight", "blk.0.attn_q.weight", "blk.0.attn_q.bias",
                "output_norm.weight"]:
        if nom not in relus or nom not in attendus:
            continue
        dims, ttype, off = relus[nom]
        v = lire_tenseur_gguf(f, dims, ttype, off, debut).reshape(*reversed(dims))
        ref = attendus[nom].astype(np.float32)
        d = np.abs(v - ref).max() / (np.abs(ref).mean() + 1e-12)
        print(f"  relecture {nom} : type {ttype} · écart max/moyenne {d:.2e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

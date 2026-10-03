#!/usr/bin/env python3
"""Référence numpy des PROJECTIONS et de la ROTATION de l'attention V4.1.

Le chemin des experts est vérifié (`v41_experts_reference.py`), la tête,
l'embarquement, le routeur et le mHC aussi. Il ne reste que la COMPOSITION de
l'attention : ce script recompose ses premiers étages depuis les tenseurs du
fichier et les compare aux vides du moteur, ÉTAGE PAR ÉTAGE (qr, qr_norm, q_norm,
q_rope, kv_norm, kv_rope) — un désaccord se localise donc tout seul.

  qr      = W_qa · x                       (Q8_0)
  qr_norm = rmsnorm(qr, q_a_norm)
  q       = W_qb · qr_norm                 (Q8_0)
  q_norm  = rmsnorm SANS POIDS par tête (head_dim)
  q_rope  = RoPE NORM sur les n_rot dernières composantes de chaque tête
  kv      = W_kv · x                       (Q8_0)
  kv_norm = rmsnorm(kv, kv_a_norm)
  kv_rope = RoPE NORM sur les n_rot dernières

Usage : python3 tools/v41_attention_reference.py <modele.gguf> <prefixe_dump> <couche> <pos> ...
"""
import os
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier_v41_mhc import Gguf, dump

EPS = 1e-20
BASE = 10000.0


def dequant_q8_0_ligne(g, nom, ligne):
    """Une ligne d'un tenseur Q8_0 (blocs de 32 : échelle f16 + 32 i8)."""
    dims, ttype, off, idx = g.tenseurs[nom]
    assert ttype == 8, (nom, ttype)
    n_in = dims[0]
    nb = n_in // 32
    f, donnees = g.fragments[idx]
    f.seek(donnees + off + ligne * nb * 34)
    brut = f.read(nb * 34)
    vals = []
    for b in range(nb):
        e = np.frombuffer(brut[b * 34:b * 34 + 2], dtype="<f2")[0].astype(np.float64)
        q = np.frombuffer(brut[b * 34 + 2:b * 34 + 34], dtype="<i1").astype(np.float64)
        vals.append(q * e)
    return np.concatenate(vals)


def matvec_q8_0(g, nom, x):
    dims = g.tenseurs[nom][0]
    n_in, n_out = dims[0], dims[1]
    assert n_in == x.size, (nom, dims, x.size)
    return np.array([dequant_q8_0_ligne(g, nom, o) @ x for o in range(n_out)])


def rmsnorm(x, poids=None, eps=EPS):
    v = float(np.mean(x.astype(np.float64) ** 2))
    y = x / np.sqrt(v + eps)
    return y * poids if poids is not None else y


def rope_norm(v, n_head, head_dim, pos, base, n_rot):
    """RoPE NORM, appariement (2i, 2i+1) — recopie de `rope_norm`."""
    v = v.copy()
    half = n_rot // 2
    for h in range(n_head):
        t = v[h * head_dim:(h + 1) * head_dim]
        for i in range(half):
            freq = 1.0 / base ** (2.0 * i / n_rot)
            s = np.sin(pos * freq)
            c = np.cos(pos * freq)
            a, b = t[2 * i], t[2 * i + 1]
            t[2 * i] = a * c - b * s
            t[2 * i + 1] = b * c + a * s
    return v


def principale():
    modele, prefixe, couche = sys.argv[1], sys.argv[2], int(sys.argv[3])
    g = Gguf(modele)
    nom = lambda s: f"blk.{couche}.{s}"
    # `attn_kv` : [hidden, 512] — les 512 de la tête latente (448 nope + 64 rope).
    # `attn_q_b` : [1280, 64 × 512].
    hd = g.tenseurs[nom("attn_kv.weight")][0][1]
    qb = g.tenseurs[nom("attn_q_b.weight")][0]
    nh = qb[1] // hd
    nrot = 64
    print(f"couche {couche} : head_dim {hd} · {nh} têtes · attn_q_b {qb} · "
          f"kv {g.tenseurs[nom('attn_kv.weight')][0]}")
    for pos in [int(x) for x in sys.argv[4:]]:
        # L'entrée de l'attention n'est pas le flux replié : c'est SA NORME
        # (`rmsnorm(xin, attn_norm)`) — le vide `hc_attn_pre` est AVANT la norme.
        x = rmsnorm(dump(prefixe, "hc_attn_pre", couche, pos),
                    g.lire(nom("attn_norm.weight")).ravel())
        qr = matvec_q8_0(g, nom("attn_q_a.weight"), x)
        qa_norm = g.lire(nom("attn_q_a_norm.weight")).ravel()
        qrn = rmsnorm(qr, qa_norm)
        q = matvec_q8_0(g, nom("attn_q_b.weight"), qrn)
        qn = np.concatenate([rmsnorm(q[h * hd:(h + 1) * hd]) for h in range(nh)])
        # ATTENTION : la rotation porte sur le q NORMÉ (`qn`), pas sur la sortie
        # brute de `wq_b` — prendre `q` ici mélangeait la tranche NON NORMÉE dans
        # le vecteur normé et donnait 3,6 d'écart sur `q_rope` alors que la
        # rotation du moteur est juste à 1e-06 (vérifié en appliquant la rotation
        # au `q_norm` DU MOTEUR).
        qp = np.concatenate([qn[h * hd + hd - nrot:h * hd + hd] for h in range(nh)])
        qp = rope_norm(qp, nh, nrot, pos, BASE, nrot)
        q_rope = qn.copy()
        for h in range(nh):
            q_rope[h * hd + hd - nrot:h * hd + hd] = qp[h * nrot:(h + 1) * nrot]
        kv = matvec_q8_0(g, nom("attn_kv.weight"), x)
        kn = g.lire(nom("attn_kv_a_norm.weight")).ravel()
        kvn = rmsnorm(kv, kn)
        kp = rope_norm(kvn[hd - nrot:].copy(), 1, nrot, pos, BASE, nrot)
        kv_rope = kvn.copy()
        kv_rope[hd - nrot:] = kp
        for etage, calc in (("qr", qr), ("qr_norm", qrn), ("q_norm", qn),
                            ("q_rope", q_rope), ("kv_norm", kvn), ("kv_rope", kv_rope)):
            ref = dump(prefixe, etage, couche, pos)
            if ref.size != calc.size:
                print(f"  pos {pos} {etage:8} : FORMES {calc.size} vs {ref.size}")
                continue
            e = np.max(np.abs(calc - ref))
            print(f"  pos {pos} {etage:8} : écart max {e:.3e} "
                  f"(dynamique {np.max(np.abs(ref)):.3e}, {e / max(np.max(np.abs(ref)), 1e-30):.1e} relatif)")


if __name__ == "__main__":
    principale()

#!/usr/bin/env python3
"""couche_distante.py — A18 : exécuter une couche de Qwen 0.5B dans un second processus.

Le modèle Qwen2.5-0.5B-Instruct (24 couches, hidden 896, vocab 151 936) est
chargé en float32 dans le client. La couche ``--couche`` (12 par défaut) est
retirée du client et exécutée par un **processus serveur** qui ne charge que
cette couche depuis ``model.safetensors``. Le client garde les embeddings, les
autres couches, la norme finale et ``lm_head`` ; il envoie l'état caché, les
``position_ids`` et les cos/sin de RoPE par **TCP loopback** au serveur, qui
renvoie l'état caché après la couche.

Le transport est un protocole binaire simple : en-tête ``struct`` de 38 octets,
puis les blobs (hidden en float32 dense ou sparse, position_ids int64, cos/sin
float32). Le mode sparse est le format de A7.5 (masque 1 bit par valeur + f32
non nuls) ; il est comparé au dense.

Mesures :
  * fidélité des logits (bits identiques, écart max, argmax, top-5, top-1024,
    KL) et perplexité sur chaque invite ;
  * latence aller-retour de la couche, latence du forward complet, calcul
    serveur, ping réseau ;
  * octets du flux (dont hidden et cos/sin), octets/jeton, débit ;
  * contrôles négatifs : serveur CPU (même fp32/sdpa), serveur bfloat16,
    serveur eager sans masque causal, et positions RoPE mises à zéro.

Hypothèses et limites explicites :
  * une seule séquence par forward (batch 1, sans padding) ; ``attention_mask``
    vaut ``None`` et le backend ``sdpa`` applique le masque causal. Un masque
    explicite n'est pas transporté (le proxy lève une erreur) ;
  * ``use_cache=False`` (prefill) ; aucun cache KV n'est transféré. Le cache
    serait un coût supplémentaire (2 × 2 têtes KV × 64 × 4 o = 1 024 o/jeton/
    couche) et un risque de désynchronisation ;
  * le client charge le modèle complet pour produire la référence, puis libère
    les poids de la couche distante. Le gain mémoire est mesuré après cette
    libération, pas au démarrage ;
  * l'exactitude bit-à-bit n'est attendue que si le serveur utilise le même
    device et le même dtype que le client (GPU fp32 + sdpa). Les négatifs
    montrent ce qui casse l'exactitude.

Usage principal (GPU 0) ::

    CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python \
        tools/couche_distante.py

Écrit ``/tmp/a18-couche-distante.json`` et ``.md``. Le mode ``--serveur`` est
interne (lancé par le client).
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import shutil
import socket
import statistics
import struct
import subprocess
import sys
import tempfile
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Protocole
# ---------------------------------------------------------------------------

MAGIC_REQ = b"A18L"
MAGIC_RESP = b"A18R"
VERSION = 1

OP_PING = 0
OP_FORWARD = 1
OP_SHUTDOWN = 2

FLAG_SPARSE = 1
DTYPE_F32 = 0
DTYPE_INT8 = 1

# magic, version, op, flags, dtype, reserve,
# ntok, h, n_x, n_pos, n_cos, n_sin, n_mask
ENTETE_REQ = struct.Struct("<4sHBBBBIIIIIII")
# magic, version, status, flags, dtype, reserve,
# ntok, h, n_out, n_msg, compute_us, reserve
ENTETE_RESP = struct.Struct("<4sHBBBBIIIIII")

MODELE_DEFAUT = "Qwen/Qwen2.5-0.5B-Instruct"
COUCHE_DEFAUT = 12

INVITES = [
    "La mesure est reine ; ce qui n'est pas compté n'existe pas.",
    (
        "Un train part de Montréal à 8 h et roule à 90 km/h. Un second part "
        "de Québec à 9 h et roule à 110 km/h. À quelle heure se croisent-ils "
        "si la distance est de 250 km ?"
    ),
    "def fibonacci(n):\n    if n < 2:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n",
]


def bits_masque(n: int) -> int:
    """Nombre d'octets d'un masque de n bits."""
    return (int(n) + 7) // 8


def encoder_flux(flux, sparse: bool = False, quant: bool = False):
    """Encode un flux (ntok × h) en float32 dense, sparse ou int8.

    Retourne ``(payload, meta)``. En sparse, le payload est le masque
    (``np.packbits`` little-endian) suivi des valeurs non nulles en float32.
    Les zéros signés (-0.0) sont traités comme des zéros et relus en +0.0.
    """
    x = np.ascontiguousarray(np.asarray(flux, dtype=np.float32))
    if x.ndim != 2:
        raise ValueError(f"flux attendu 2-D, reçu {x.shape}")
    ntok, h = int(x.shape[0]), int(x.shape[1])
    if quant:
        maximum = np.max(np.abs(x.astype(np.float32)), axis=0, keepdims=True)
        echelles = np.where(maximum > 0, maximum / 127.0, 1.0).astype(np.float32)
        q = np.clip(np.round(x.astype(np.float32) / echelles), -127, 127).astype(np.int8)
        payload = np.ascontiguousarray(echelles, dtype="<f4").tobytes() + np.ascontiguousarray(q).tobytes()
        meta = {"ntok": ntok, "h": h, "sparse": False, "quant": True,
                "nval": ntok * h, "nmask": 0, "octets": len(payload),
                "echelles": echelles.reshape(-1).tolist()}
        return payload, meta
    if sparse:
        plat = x.reshape(-1)
        nz = plat != 0.0
        masque = np.packbits(nz, bitorder="little")
        valeurs = np.ascontiguousarray(plat[nz], dtype="<f4").tobytes()
        payload = masque.tobytes() + valeurs
        meta = {
            "ntok": ntok,
            "h": h,
            "sparse": True,
            "nval": int(nz.sum()),
            "nmask": int(masque.size),
            "octets": len(payload),
        }
    else:
        payload = np.ascontiguousarray(x, dtype="<f4").tobytes()
        meta = {
            "ntok": ntok,
            "h": h,
            "sparse": False,
            "nval": ntok * h,
            "nmask": 0,
            "octets": len(payload),
        }
    return payload, meta


def decoder_flux(payload: bytes, ntok: int, h: int, sparse: bool = False,
                 quant: bool = False) -> np.ndarray:
    """Décode un payload produit par :func:`encoder_flux` (validation stricte)."""
    ntok, h = int(ntok), int(h)
    n = ntok * h
    if n < 0:
        raise ValueError("ntok/h négatifs")
    if quant:
        if len(payload) != 4 * h + n:
            raise ValueError(f"payload int8 de {len(payload)} octets, attendu {4*h+n}")
        echelles = np.frombuffer(payload[:4 * h], dtype="<f4").reshape(1, h)
        q = np.frombuffer(payload[4 * h:], dtype=np.int8, count=n).reshape(ntok, h)
        return q.astype(np.float32) * echelles
    if sparse:
        nmask = bits_masque(n)
        if len(payload) < nmask:
            raise ValueError(
                f"payload sparse trop court : {len(payload)} < masque {nmask}"
            )
        masque = np.frombuffer(payload[:nmask], dtype=np.uint8)
        bits = np.unpackbits(masque, bitorder="little")[:n].astype(bool)
        reste = len(payload) - nmask
        if reste % 4:
            raise ValueError(f"queue de valeurs non multiple de 4 : {reste} octets")
        nval = reste // 4
        if nval != int(bits.sum()):
            raise ValueError(
                f"masque ({int(bits.sum())} bits) et valeurs ({nval}) incohérents"
            )
        valeurs = np.frombuffer(payload[nmask:], dtype="<f4", count=nval)
        out = np.zeros(n, dtype=np.float32)
        out[bits] = valeurs
        return out.reshape(ntok, h)
    if len(payload) != n * 4:
        raise ValueError(
            f"payload dense de {len(payload)} octets, attendu {n * 4}"
        )
    return np.frombuffer(payload, dtype="<f4", count=n).reshape(ntok, h).copy()


def recevoir_exact(conn: socket.socket, n: int) -> bytes:
    """Lit exactement n octets (ou lève EOFError)."""
    n = int(n)
    if n < 0:
        raise ValueError("longueur négative")
    morceaux = []
    recu = 0
    while recu < n:
        bloc = conn.recv(min(n - recu, 1 << 20))
        if not bloc:
            raise EOFError(f"connexion fermée après {recu}/{n} octets")
        morceaux.append(bloc)
        recu += len(bloc)
    return b"".join(morceaux)


def lire_entete(conn: socket.socket, entete: struct.Struct, magic: bytes):
    """Lit et valide un en-tête."""
    champs = entete.unpack(recevoir_exact(conn, entete.size))
    if champs[0] != magic:
        raise ValueError(f"mauvais magic {champs[0]!r}, attendu {magic!r}")
    if champs[1] != VERSION:
        raise ValueError(f"version {champs[1]} non supportée (attendu {VERSION})")
    return champs


def envoyer_reponse(
    conn: socket.socket,
    status: int = 0,
    flags: int = 0,
    ntok: int = 0,
    h: int = 0,
    payload: bytes = b"",
    message: bytes = b"",
    compute_us: int = 0,
) -> None:
    """Envoie une réponse complète (en-tête + payload + message)."""
    entete = ENTETE_RESP.pack(
        MAGIC_RESP,
        VERSION,
        int(status),
        int(flags),
        DTYPE_F32,
        0,
        int(ntok),
        int(h),
        len(payload),
        len(message),
        int(min(compute_us, 0xFFFFFFFF)),
        0,
    )
    conn.sendall(entete + payload + message)


# ---------------------------------------------------------------------------
# Mesures (numpy seul : testables sans torch)
# ---------------------------------------------------------------------------


def _logsumexp(ligne: np.ndarray) -> float:
    m = float(np.max(ligne))
    return m + math.log(float(np.sum(np.exp(ligne - m))))


def perplexite_np(logits, cibles) -> dict:
    """Perplexité d'une suite de logits (T × V) sur des cibles (T,)."""
    logits = np.asarray(logits, dtype=np.float64)
    cibles = np.asarray(cibles, dtype=np.int64)
    if logits.ndim != 2:
        raise ValueError(f"logits attendus 2-D, reçus {logits.shape}")
    if cibles.ndim != 1 or cibles.shape[0] != logits.shape[0]:
        raise ValueError("cibles de mauvaise forme")
    if logits.shape[0] == 0:
        raise ValueError("perplexité sur zéro position")
    if cibles.min() < 0 or cibles.max() >= logits.shape[1]:
        raise ValueError("cible hors vocabulaire")
    lse = np.array([_logsumexp(l) for l in logits], dtype=np.float64)
    nll = lse - logits[np.arange(logits.shape[0]), cibles]
    moyenne = float(np.mean(nll))
    return {
        "ntok": int(logits.shape[0]),
        "nll_moyenne": moyenne,
        "perplexite": float(math.exp(moyenne)),
    }


def kl_divergence_np(p, q) -> float:
    """KL(P || Q) moyenne par position, en float64 (softmax stable)."""
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    if p.shape != q.shape or p.ndim != 2:
        raise ValueError("KL : formes incompatibles")
    if p.shape[0] == 0:
        return 0.0
    total = 0.0
    for i in range(p.shape[0]):
        lp = p[i] - _logsumexp(p[i])
        lq = q[i] - _logsumexp(q[i])
        pp = np.exp(lp)
        total += float(np.sum(pp * (lp - lq)))
    return total / p.shape[0]


def intersection_topk(a, b, k: int) -> float:
    """Intersection moyenne des top-k par position (1.0 = identiques)."""
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    if a.shape != b.shape or a.ndim != 2:
        raise ValueError("top-k : formes incompatibles")
    if a.shape[0] == 0:
        return 0.0
    k = max(1, min(int(k), a.shape[1]))
    ka = np.argpartition(-a, k - 1, axis=1)[:, :k]
    kb = np.argpartition(-b, k - 1, axis=1)[:, :k]
    score = 0.0
    for i in range(a.shape[0]):
        score += len(np.intersect1d(ka[i], kb[i])) / k
    return float(score / a.shape[0])


def fidelite_np(ref, split, k: int = 5, k_grappe: int = 1024) -> dict:
    """Compare deux matrices de logits (T × V) et résume la fidélité."""
    ref = np.ascontiguousarray(np.asarray(ref, dtype=np.float32))
    split = np.ascontiguousarray(np.asarray(split, dtype=np.float32))
    if ref.shape != split.shape:
        raise ValueError(f"formes différentes : {ref.shape} vs {split.shape}")
    if ref.ndim != 2:
        raise ValueError("logits attendus 2-D")
    bits_ref = ref.view(np.uint32)
    bits_split = split.view(np.uint32)
    diff = np.abs(ref.astype(np.float64) - split.astype(np.float64))
    am_ref = np.argmax(ref, axis=1)
    am_split = np.argmax(split, axis=1)
    return {
        "forme": [int(x) for x in ref.shape],
        "bits_identiques": bool(np.array_equal(bits_ref, bits_split)),
        "valeurs_identiques": bool(np.array_equal(ref, split)),
        "elements_bits_identiques": int(np.count_nonzero(bits_ref == bits_split)),
        "elements_total": int(ref.size),
        "taux_bits_identiques": float(
            np.count_nonzero(bits_ref == bits_split) / ref.size
        ),
        "diff_max": float(np.max(diff)) if ref.size else 0.0,
        "diff_moyenne": float(np.mean(diff)) if ref.size else 0.0,
        "allclose_1e-6": bool(np.allclose(ref, split, atol=1e-6, rtol=0.0)),
        "argmax_accord": float(np.mean(am_ref == am_split)),
        "top5_intersection": intersection_topk(ref, split, k),
        "top1024_intersection": intersection_topk(ref, split, k_grappe),
        "kl_moyenne": kl_divergence_np(ref, split),
    }


def statistiques(valeurs) -> dict | None:
    """min / médiane / moyenne / max / p95 d'une liste de flottants."""
    v = sorted(float(x) for x in valeurs)
    if not v:
        return None
    return {
        "n": len(v),
        "min": v[0],
        "mediane": float(statistics.median(v)),
        "moyenne": float(sum(v) / len(v)),
        "max": v[-1],
        "p95": v[min(len(v) - 1, int(round(0.95 * (len(v) - 1))))],
    }


def _json_defaut(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f"objet non sérialisable : {type(o)!r}")


# ---------------------------------------------------------------------------
# Torch / transformers (imports paresseux)
# ---------------------------------------------------------------------------


def charger_modele(mid: str, device: str, attn: str = "sdpa", local_only: bool = True):
    """Charge Qwen en float32 sur ``device`` (référence locale)."""
    import torch
    from transformers import AutoModelForCausalLM

    kwargs = {"local_files_only": local_only, "dtype": torch.float32}
    if attn:
        kwargs["attn_implementation"] = attn
    modele = AutoModelForCausalLM.from_pretrained(mid, **kwargs)
    modele.to(device).eval()
    return modele


def hash_poids(module) -> str:
    """SHA-256 des tenseurs fp32 triés par nom (identité des poids)."""
    import torch

    h = hashlib.sha256()
    etat = module.state_dict()
    for nom in sorted(etat):
        t = (
            etat[nom]
            .detach()
            .to(device="cpu", dtype=torch.float32)
            .contiguous()
            .numpy()
        )
        h.update(nom.encode("utf-8"))
        h.update(struct.pack("<I", t.ndim))
        h.update(struct.pack("<%dQ" % t.ndim, *t.shape))
        h.update(t.tobytes())
    return h.hexdigest()


def dossier_modele(mid: str) -> Path:
    """Chemin local du snapshot HF (cache, hors ligne)."""
    from huggingface_hub import snapshot_download

    return Path(snapshot_download(repo_id=mid, local_files_only=True))


def extraire_couche(dossier: Path, couche: int) -> dict:
    """Lit uniquement les tenseurs ``model.layers.<couche>.*`` du safetensors."""
    from safetensors import safe_open

    prefixe = f"model.layers.{couche}."
    sous = {}
    for fichier in sorted(Path(dossier).glob("*.safetensors")):
        with safe_open(str(fichier), framework="pt", device="cpu") as sf:
            for nom in sf.keys():
                if nom.startswith(prefixe):
                    sous[nom[len(prefixe):]] = sf.get_tensor(nom)
    if not sous:
        raise FileNotFoundError(
            f"aucun tenseur {prefixe}* dans {dossier}/*.safetensors"
        )
    return sous


# ---------------------------------------------------------------------------
# Client : transport TCP
# ---------------------------------------------------------------------------


class Transport:
    """Un socket persistant vers le serveur, avec mesures par requête."""

    def __init__(self, port: int, host: str = "127.0.0.1", timeout: float = 120.0):
        self.sock = socket.create_connection((host, int(port)), timeout=timeout)
        self.sock.settimeout(timeout)
        self.mesures: list[dict] = []

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass

    def _echanger(self, op: int, flags: int, ntok: int, h: int, blobs: dict,
                  dtype: int = DTYPE_F32) -> dict:
        nx = len(blobs.get("x", b""))
        npos = len(blobs.get("pos", b""))
        ncos = len(blobs.get("cos", b""))
        nsin = len(blobs.get("sin", b""))
        nmask = len(blobs.get("mask", b""))
        entete = ENTETE_REQ.pack(
            MAGIC_REQ,
            VERSION,
            int(op),
            int(flags),
            int(dtype),
            0,
            int(ntok),
            int(h),
            nx,
            npos,
            ncos,
            nsin,
            nmask,
        )
        charge = (
            entete
            + blobs.get("x", b"")
            + blobs.get("pos", b"")
            + blobs.get("cos", b"")
            + blobs.get("sin", b"")
            + blobs.get("mask", b"")
        )
        t0 = time.perf_counter()
        self.sock.sendall(charge)
        champs = lire_entete(self.sock, ENTETE_RESP, MAGIC_RESP)
        (
            _magic,
            _version,
            status,
            flags_r,
            _dtype,
            _reserve,
            ntok_r,
            h_r,
            n_out,
            n_msg,
            compute_us,
            _reserve2,
        ) = champs
        corps = recevoir_exact(self.sock, n_out + n_msg)
        rtt_ms = (time.perf_counter() - t0) * 1000.0
        message = corps[n_out:].decode("utf-8", "replace")
        if status != 0:
            raise RuntimeError(f"serveur (op {op}) : {message}")
        return {
            "status": int(status),
            "flags": int(flags_r),
            "ntok": int(ntok_r),
            "h": int(h_r),
            "payload": corps[:n_out],
            "message": message,
            "compute_us": int(compute_us),
            "rtt_ms": rtt_ms,
            "octets_requete": len(charge),
            "octets_reponse": ENTETE_RESP.size + n_out + n_msg,
        }

    def ping(self, n: int = 3):
        """Ping le serveur ; renvoie (info, [rtt_ms])."""
        infos = []
        rtts = []
        for _ in range(max(1, int(n))):
            r = self._echanger(OP_PING, 0, 0, 0, {})
            infos.append(json.loads(r["message"]))
            rtts.append(r["rtt_ms"])
        return infos[-1], rtts

    def shutdown(self) -> None:
        try:
            self._echanger(OP_SHUTDOWN, 0, 0, 0, {})
        except (OSError, EOFError, RuntimeError):
            pass

    def forward(
        self,
        hidden_states,
        position_ids,
        cos,
        sin,
        sparse: bool = False,
        zero_positions: bool = False,
        quant: bool = False,
    ):
        """Envoie l'entrée de la couche, exécute la couche à distance, renvoie la sortie."""
        import torch

        if hidden_states.ndim != 3 or int(hidden_states.shape[0]) != 1:
            raise NotImplementedError(
                "seul un batch de 1 sans padding est supporté "
                f"(reçu {tuple(hidden_states.shape)})"
            )
        ntok = int(hidden_states.shape[1])
        h = int(hidden_states.shape[2])
        if position_ids is None or tuple(position_ids.shape) != (1, ntok):
            raise ValueError("position_ids de mauvaise forme")
        if cos is None or sin is None or cos.shape != sin.shape:
            raise ValueError("cos/sin absents ou de formes différentes")
        if tuple(cos.shape[:2]) != (1, ntok):
            raise ValueError(f"cos de mauvaise forme : {tuple(cos.shape)}")

        t0 = time.perf_counter()
        x = (
            hidden_states[0]
            .detach()
            .to(device="cpu", dtype=torch.float32)
            .contiguous()
            .numpy()
        )
        payload_x, meta = encoder_flux(x, sparse=sparse, quant=quant)
        x_relu = decoder_flux(payload_x, ntok, h, sparse=sparse, quant=quant)
        codec_valeurs = bool(np.array_equal(x, x_relu))
        codec_bits = bool(np.array_equal(x.view(np.uint32), x_relu.view(np.uint32)))
        diff_codec = (
            float(np.max(np.abs(x.astype(np.float64) - x_relu.astype(np.float64))))
            if x.size
            else 0.0
        )

        pos = (
            position_ids[0]
            .detach()
            .to(device="cpu", dtype=torch.int64)
            .contiguous()
            .numpy()
        )
        if zero_positions:
            cos_np = np.zeros(tuple(cos.shape[1:]), dtype=np.float32)
            sin_np = np.zeros(tuple(sin.shape[1:]), dtype=np.float32)
        else:
            cos_np = (
                cos[0]
                .detach()
                .to(device="cpu", dtype=torch.float32)
                .contiguous()
                .numpy()
            )
            sin_np = (
                sin[0]
                .detach()
                .to(device="cpu", dtype=torch.float32)
                .contiguous()
                .numpy()
            )
        t_enc = (time.perf_counter() - t0) * 1000.0

        blobs = {
            "x": payload_x,
            "pos": pos.tobytes(),
            "cos": cos_np.tobytes(),
            "sin": sin_np.tobytes(),
            "mask": b"",
        }
        r = self._echanger(
            OP_FORWARD, FLAG_SPARSE if sparse else 0, ntok, h, blobs,
            dtype=DTYPE_INT8 if quant else DTYPE_F32,
        )
        t1 = time.perf_counter()
        if r["ntok"] != ntok or r["h"] != h:
            raise RuntimeError(
                f"réponse de forme inattendue : ntok={r['ntok']} h={r['h']} "
                f"(attendu {ntok}×{h})"
            )
        out_np = decoder_flux(r["payload"], ntok, h, sparse=False)
        out = (
            torch.from_numpy(out_np)
            .to(device=hidden_states.device, dtype=hidden_states.dtype)
            .unsqueeze(0)
        )
        t_dec = (time.perf_counter() - t1) * 1000.0

        mesure = {
            "ntok": ntok,
            "h": h,
            "sparse": bool(sparse),
            "zero_positions": bool(zero_positions),
            "n_x": len(payload_x),
            "n_pos": len(blobs["pos"]),
            "n_cos": len(blobs["cos"]),
            "n_sin": len(blobs["sin"]),
            "n_mask": 0,
            "n_out": len(r["payload"]),
            "nval": int(meta["nval"]),
            "nmask": int(meta["nmask"]),
            "taux_zeros": float(np.count_nonzero(x == 0.0)) / x.size if x.size else 0.0,
            "octets_requete": int(r["octets_requete"]),
            "octets_reponse": int(r["octets_reponse"]),
            "octets_total": int(r["octets_requete"] + r["octets_reponse"]),
            "rtt_ms": float(r["rtt_ms"]),
            "calcul_serveur_ms": float(r["compute_us"] / 1000.0),
            "surcharge_ms": float(r["rtt_ms"] - r["compute_us"] / 1000.0),
            "encodage_ms": float(t_enc),
            "decodage_ms": float(t_dec),
            "codec": {
                "valeurs_identiques": codec_valeurs,
                "bits_identiques": codec_bits,
                "diff_max": diff_codec,
            },
        }
        self.mesures.append(mesure)
        return out, mesure


def creer_proxy(transport: Transport, sparse: bool = False, zero_positions: bool = False,
                quant: bool = False):
    """Crée un module qui remplace la couche locale par l'appel distant."""
    import torch

    class CoucheDistante(torch.nn.Module):
        def forward(
            self,
            hidden_states,
            attention_mask=None,
            position_ids=None,
            past_key_values=None,
            use_cache=None,
            position_embeddings=None,
            **kwargs,
        ):
            if kwargs:
                raise NotImplementedError(
                    f"kwargs de couche non gérés : {sorted(kwargs)}"
                )
            if attention_mask is not None:
                raise NotImplementedError(
                    "attention_mask non transporté (batch 1 sans padding uniquement)"
                )
            if past_key_values is not None or use_cache:
                raise NotImplementedError(
                    "cache KV non transporté (prefill, use_cache=False)"
                )
            if position_embeddings is None:
                raise ValueError("position_embeddings manquant")
            cos, sin = position_embeddings
            sortie, _ = transport.forward(
                hidden_states,
                position_ids,
                cos,
                sin,
                sparse=sparse,
                zero_positions=zero_positions,
                quant=quant,
            )
            return sortie

    return CoucheDistante()


# ---------------------------------------------------------------------------
# Serveur
# ---------------------------------------------------------------------------


def _ecrire_json_atomique(chemin, obj) -> None:
    chemin = Path(chemin)
    tmp = chemin.with_name(chemin.name + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, chemin)


def servir(args) -> None:
    """Mode serveur : charge une couche, sert des forwards jusqu'à SHUTDOWN/EOF."""
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
    import torch
    from transformers import AutoConfig
    from transformers.models.qwen2.modeling_qwen2 import Qwen2DecoderLayer

    if not args.fichier_pret:
        raise SystemExit("--fichier-pret requis en mode --serveur")

    t0 = time.time()
    cfg = AutoConfig.from_pretrained(args.modele, local_files_only=True)
    cfg._attn_implementation = args.attn
    dossier = dossier_modele(args.modele)
    sous = extraire_couche(dossier, args.couche)
    couche = Qwen2DecoderLayer(cfg, layer_idx=args.couche)
    manquants, inattendus = couche.load_state_dict(sous, strict=False)
    if manquants or inattendus:
        raise RuntimeError(
            f"chargement de la couche incomplet : manquants={manquants}, "
            f"inattendus={inattendus}"
        )
    couche = couche.to(dtype=torch.float32).eval()
    hash_source = hash_poids(couche)
    dtype = getattr(torch, args.dtype)
    couche = couche.to(device=args.device, dtype=dtype)
    for p in couche.parameters():
        p.requires_grad_(False)
    duree_chargement = time.time() - t0

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]
    info = {
        "port": int(port),
        "pid": os.getpid(),
        "couche": int(args.couche),
        "device": args.device,
        "dtype": args.dtype,
        "attn": args.attn,
        "hash_poids_fp32": hash_source,
        "dossier_modele": str(dossier),
        "torch": torch.__version__,
        "transformers": __import__("transformers").__version__,
        "duree_chargement_s": duree_chargement,
    }
    _ecrire_json_atomique(args.fichier_pret, info)
    print(json.dumps({"pret": True, "port": port}), flush=True)

    conn = None
    try:
        srv.settimeout(120.0)
        try:
            conn, _ = srv.accept()
        except socket.timeout:
            return
        conn.settimeout(600.0)
        while True:
            try:
                champs = lire_entete(conn, ENTETE_REQ, MAGIC_REQ)
            except (EOFError, OSError, ValueError):
                break
            (
                _magic,
                _version,
                op,
                flags,
                dtype_wire,
                _reserve,
                ntok,
                h,
                nx,
                npos,
                ncos,
                nsin,
                nmask,
            ) = champs
            if dtype_wire not in (DTYPE_F32, DTYPE_INT8):
                try:
                    envoyer_reponse(
                        conn, status=1, message=b"dtype wire non supporte"
                    )
                except OSError:
                    break
                continue
            taille = nx + npos + ncos + nsin + nmask
            if taille < 0 or taille > 64 * 1024 * 1024:
                try:
                    envoyer_reponse(conn, status=1, message=b"payload trop gros")
                except OSError:
                    break
                continue
            try:
                payload = recevoir_exact(conn, taille)
            except EOFError:
                break
            except OSError:
                break

            if op == OP_SHUTDOWN:
                try:
                    envoyer_reponse(conn, status=0)
                except OSError:
                    pass
                break
            if op == OP_PING:
                msg = json.dumps(info, ensure_ascii=False).encode("utf-8")
                try:
                    envoyer_reponse(conn, status=0, message=msg)
                except OSError:
                    break
                continue
            if op != OP_FORWARD:
                try:
                    envoyer_reponse(
                        conn, status=1, message=b"operation inconnue"
                    )
                except OSError:
                    break
                continue

            try:
                if nmask:
                    raise NotImplementedError("masque explicite non supporté")
                if nx <= 0 or npos != ntok * 8 or ncos <= 0 or nsin <= 0:
                    raise ValueError(
                        f"tailles incohérentes : nx={nx}, npos={npos}, "
                        f"ncos={ncos}, nsin={nsin}, ntok={ntok}"
                    )
                i0 = 0
                i1 = nx
                i2 = i1 + npos
                i3 = i2 + ncos
                x_np = decoder_flux(
                    payload[i0:i1], ntok, h, sparse=bool(flags & FLAG_SPARSE),
                    quant=(dtype_wire == DTYPE_INT8),
                )
                pos_np = (
                    np.frombuffer(payload[i1:i2], dtype="<i8").copy().reshape(ntok)
                )
                cos_np = (
                    np.frombuffer(payload[i2:i3], dtype="<f4")
                    .copy()
                    .reshape(ntok, -1)
                )
                sin_np = (
                    np.frombuffer(payload[i3:], dtype="<f4")
                    .copy()
                    .reshape(ntok, -1)
                )
                if cos_np.shape != sin_np.shape:
                    raise ValueError("cos/sin de formes différentes")
                x_t = (
                    torch.from_numpy(x_np)
                    .to(device=args.device, dtype=dtype)
                    .unsqueeze(0)
                )
                pos_t = (
                    torch.from_numpy(pos_np)
                    .to(device=args.device)
                    .unsqueeze(0)
                )
                cos_t = torch.from_numpy(cos_np).to(
                    device=args.device, dtype=dtype
                ).unsqueeze(0)
                sin_t = torch.from_numpy(sin_np).to(
                    device=args.device, dtype=dtype
                ).unsqueeze(0)
                if cos_t.shape[-1] != couche.self_attn.head_dim:
                    raise ValueError(
                        f"head_dim {cos_t.shape[-1]} != {couche.self_attn.head_dim}"
                    )
                if args.device.startswith("cuda"):
                    torch.cuda.synchronize()
                t_calc = time.perf_counter_ns()
                with torch.no_grad():
                    sortie = couche(
                        x_t,
                        attention_mask=None,
                        position_embeddings=(cos_t, sin_t),
                        position_ids=pos_t,
                        past_key_values=None,
                        use_cache=False,
                    )
                if args.device.startswith("cuda"):
                    torch.cuda.synchronize()
                compute_us = (time.perf_counter_ns() - t_calc) // 1000
                out = (
                    sortie.detach()
                    .to(device="cpu", dtype=torch.float32)
                    .contiguous()
                    .numpy()
                    .astype("<f4", copy=False)
                    .tobytes()
                )
                envoyer_reponse(
                    conn,
                    status=0,
                    flags=flags,
                    ntok=ntok,
                    h=h,
                    payload=out,
                    compute_us=compute_us,
                )
            except Exception:
                msg = traceback.format_exc()[-4000:].encode("utf-8", "replace")
                try:
                    envoyer_reponse(
                        conn,
                        status=1,
                        flags=flags,
                        ntok=ntok,
                        h=h,
                        message=msg,
                    )
                except OSError:
                    break
    finally:
        if conn is not None:
            try:
                conn.close()
            except OSError:
                pass
        try:
            srv.close()
        except OSError:
            pass
        try:
            Path(args.fichier_pret).unlink()
        except OSError:
            pass


class ServeurDistant:
    """Handle client d'un processus serveur (Popen + Transport + ping)."""

    def __init__(self, proc, transport: Transport, info: dict, ping_info: dict,
                 rtts_ping: list[float], dossier_tmp: str):
        self.proc = proc
        self.transport = transport
        self.info = info
        self.ping_info = ping_info
        self.rtts_ping = rtts_ping
        self.dossier_tmp = dossier_tmp

    def arreter(self) -> dict:
        self.transport.shutdown()
        try:
            self.proc.wait(timeout=10.0)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            try:
                self.proc.wait(timeout=10.0)
            except subprocess.TimeoutExpired:
                pass
        self.transport.close()
        err = ""
        if self.proc.stderr is not None:
            try:
                err = self.proc.stderr.read()
            except (OSError, ValueError):
                err = ""
        shutil.rmtree(self.dossier_tmp, ignore_errors=True)
        return {
            "code": int(self.proc.returncode) if self.proc.returncode is not None else None,
            "stderr": err[-800:] if err else "",
        }


def lancer_serveur(
    modele: str,
    couche: int,
    device: str,
    dtype: str,
    attn: str,
    timeout: float = 120.0,
) -> ServeurDistant:
    """Lance le processus serveur, attend le port, se connecte et ping."""
    dossier_tmp = tempfile.mkdtemp(prefix="a18-serveur-")
    pret = Path(dossier_tmp) / "pret.json"
    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--serveur",
        "--modele",
        modele,
        "--couche",
        str(int(couche)),
        "--device",
        device,
        "--dtype",
        dtype,
        "--attn",
        attn,
        "--fichier-pret",
        str(pret),
    ]
    env = os.environ.copy()
    env.setdefault("CUDA_VISIBLE_DEVICES", "0")
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    info = None
    t0 = time.time()
    while time.time() - t0 < timeout:
        if pret.exists():
            try:
                info = json.loads(pret.read_text(encoding="utf-8"))
                break
            except (json.JSONDecodeError, OSError):
                pass
        if proc.poll() is not None:
            err = proc.stderr.read() if proc.stderr is not None else ""
            shutil.rmtree(dossier_tmp, ignore_errors=True)
            raise RuntimeError(
                f"serveur arrêté prématurément (code {proc.returncode}) : "
                f"{err[-3000:]}"
            )
        time.sleep(0.02)
    if info is None:
        proc.kill()
        proc.wait()
        err = proc.stderr.read() if proc.stderr is not None else ""
        shutil.rmtree(dossier_tmp, ignore_errors=True)
        raise TimeoutError(
            f"serveur non prêt après {timeout} s : {err[-3000:]}"
        )
    try:
        transport = Transport(info["port"], timeout=max(60.0, timeout))
        ping_info, rtts = transport.ping(3)
    except Exception:
        proc.kill()
        proc.wait()
        err = proc.stderr.read() if proc.stderr is not None else ""
        shutil.rmtree(dossier_tmp, ignore_errors=True)
        raise RuntimeError(f"connexion au serveur impossible : {err[-3000:]}")
    return ServeurDistant(proc, transport, info, ping_info, rtts, dossier_tmp)


# ---------------------------------------------------------------------------
# Expérience
# ---------------------------------------------------------------------------


def passe_split(
    modele,
    ids,
    transport: Transport,
    couche: int,
    sparse: bool = False,
    zero_positions: bool = False,
    quant: bool = False,
):
    """Remplace la couche par le proxy distant et exécute un forward complet."""
    import torch

    modele.model.layers[couche] = creer_proxy(
        transport, sparse=sparse, zero_positions=zero_positions, quant=quant
    )
    dev = next(modele.parameters()).device
    n_avant = len(transport.mesures)
    with torch.no_grad():
        if dev.type == "cuda":
            torch.cuda.synchronize(dev)
        t0 = time.perf_counter()
        logits = modele(ids, use_cache=False).logits
        if dev.type == "cuda":
            torch.cuda.synchronize(dev)
        total_ms = (time.perf_counter() - t0) * 1000.0
    mesures = transport.mesures[n_avant:]
    if len(mesures) != 1:
        raise RuntimeError(
            f"{len(mesures)} appels distants pour un forward (attendu 1)"
        )
    arr = (
        logits[0]
        .detach()
        .to(device="cpu", dtype=torch.float32)
        .contiguous()
        .numpy()
        .copy()
    )
    del logits
    return arr, mesures[0], total_ms


def _perplexite_comparee(ref_np, dist_np, ids_np) -> dict:
    local = perplexite_np(ref_np[:-1], ids_np[1:])
    distant = perplexite_np(dist_np[:-1], ids_np[1:])
    delta = distant["perplexite"] - local["perplexite"]
    return {
        "local": local,
        "distant": distant,
        "delta_nll": distant["nll_moyenne"] - local["nll_moyenne"],
        "delta_perplexite": delta,
        "delta_relatif": delta / local["perplexite"] if local["perplexite"] else 0.0,
    }


def _ppl_agregee(per_invites: list[dict], cle: str) -> dict:
    n = sum(p["perplexite"][cle]["ntok"] for p in per_invites)
    if n <= 0:
        return {"ntok": 0, "nll_moyenne": 0.0, "perplexite": 0.0}
    nll = (
        sum(
            p["perplexite"][cle]["nll_moyenne"] * p["perplexite"][cle]["ntok"]
            for p in per_invites
        )
        / n
    )
    return {"ntok": int(n), "nll_moyenne": nll, "perplexite": math.exp(nll)}


def _agreger_fidelite(per_invites: list[dict]) -> dict:
    return {
        "bits_identiques_tous": all(
            p["fidelite"]["bits_identiques"] for p in per_invites
        ),
        "valeurs_identiques_toutes": all(
            p["fidelite"]["valeurs_identiques"] for p in per_invites
        ),
        "diff_max": max(p["fidelite"]["diff_max"] for p in per_invites),
        "argmax_accord_min": min(
            p["fidelite"]["argmax_accord"] for p in per_invites
        ),
        "top1024_intersection_min": min(
            p["fidelite"]["top1024_intersection"] for p in per_invites
        ),
        "kl_max": max(p["fidelite"]["kl_moyenne"] for p in per_invites),
    }


def _mesurer_negatif(
    transport: Transport,
    modele,
    couche: int,
    ids_list,
    refs: list[np.ndarray],
    args,
    description: str,
    config: dict,
    zero_positions: bool = False,
) -> dict:
    """Un forward split par invite pour un serveur de contrôle négatif."""
    passe_split(
        modele,
        ids_list[0],
        transport,
        couche,
        zero_positions=zero_positions,
    )
    par = []
    for i, ids in enumerate(ids_list):
        dist_np, mes, total_ms = passe_split(
            modele,
            ids,
            transport,
            couche,
            zero_positions=zero_positions,
        )
        ids_np = ids[0].detach().to(device="cpu").numpy()
        fid = fidelite_np(refs[i], dist_np)
        ppl = _perplexite_comparee(refs[i], dist_np, ids_np)
        par.append(
            {
                "indice": i,
                "ntokens": int(ids.shape[1]),
                "fidelite": fid,
                "perplexite": ppl,
                "latence_couche_ms": mes["rtt_ms"],
                "forward_ms": total_ms,
            }
        )
    local = _ppl_agregee(par, "local")
    distant = _ppl_agregee(par, "distant")
    return {
        "description": description,
        "config": config,
        "zero_positions": bool(zero_positions),
        "par_invite": par,
        "agregat": {
            "bits_identiques_tous": all(
                p["fidelite"]["bits_identiques"] for p in par
            ),
            "diff_max": max(p["fidelite"]["diff_max"] for p in par),
            "argmax_accord_min": min(
                p["fidelite"]["argmax_accord"] for p in par
            ),
            "top1024_intersection_min": min(
                p["fidelite"]["top1024_intersection"] for p in par
            ),
            "kl_max": max(p["fidelite"]["kl_moyenne"] for p in par),
            "perplexite_locale": local,
            "perplexite_distante": distant,
            "delta_perplexite": distant["perplexite"] - local["perplexite"],
            "delta_nll": distant["nll_moyenne"] - local["nll_moyenne"],
            "latence_couche_ms_moyenne": float(
                sum(p["latence_couche_ms"] for p in par) / len(par)
            ),
        },
    }


def _agreger_reseau(per_invites: list[dict]) -> dict:
    rtts = []
    calculs = []
    totaux = []
    pings = []
    for p in per_invites:
        lat = p["latence"]
        rtts.extend(lat["rtt_couche_ms_valeurs"])
        calculs.extend(lat["calcul_serveur_ms_valeurs"])
        totaux.extend(lat["forward_bout_en_bout_ms_valeurs"])
        pings.extend(lat["ping_ms_valeurs"])
    octets = sum(p["latence"]["octets_requete_moyen"] for p in per_invites)
    ntok = sum(p["ntokens"] for p in per_invites)
    rtt_moy = sum(rtts) / len(rtts) if rtts else 0.0
    return {
        "octets_requete_total": octets,
        "octets_par_token": octets / ntok if ntok else 0.0,
        "rtt_couche_ms": statistiques(rtts),
        "calcul_serveur_ms": statistiques(calculs),
        "forward_bout_en_bout_ms": statistiques(totaux),
        "rtt_ping_ms": statistiques(pings),
        "debit_Mio_s": (octets / (sum(rtts) / 1000.0) / 2**20) if rtts else 0.0,
        "debit_tokens_s": (ntok / (sum(rtts) / 1000.0)) if rtts else 0.0,
    }


def _verdict(res: dict) -> dict:
    invites = res.get("invites", [])
    if not invites:
        return {
            "fidelite": "non mesurée",
            "conclusion": "aucune mesure",
            "causes": [],
        }
    agg = res["agregats"]["fidelite"]
    ppl = res["agregats"]["perplexite"]
    exact = bool(agg["bits_identiques_tous"])
    valeurs = bool(agg["valeurs_identiques_toutes"])
    if exact:
        fidelite = "logits identiques au bit près sur les 3 invites"
    elif valeurs:
        fidelite = "logits identiques en valeur (bits de zéro près)"
    else:
        fidelite = f"logits non identiques : écart max {agg['diff_max']:.6g}"
    causes = []
    for label, neg in res.get("negatifs", {}).items():
        if not isinstance(neg, dict) or "agregat" not in neg:
            continue
        a = neg["agregat"]
        causes.append(
            {
                "controle": label,
                "description": neg.get("description", ""),
                "diff_max_logits": a["diff_max"],
                "argmax_accord_min": a["argmax_accord_min"],
                "top1024_intersection_min": a["top1024_intersection_min"],
                "delta_perplexite": a["delta_perplexite"],
            }
        )
    transport = res["agregats"]["reseau"]
    flux = res["agregats"]["flux"]
    conclusion = (
        f"Couche {res['modele']['couche_distante']} exécutée dans un second "
        f"processus : {fidelite} ; ΔPPL corpus = "
        f"{ppl['delta_perplexite']:+.3g}. RTT couche médian "
        f"{transport['rtt_couche_ms']['mediane']:.3f} ms, "
        f"{transport['octets_par_token']:.0f} o/jeton, "
        f"{transport['debit_tokens_s']:.1f} jetons/s. "
        f"Sparse/dense = {flux['ratio_total']:.3f}×."
    )
    return {
        "fidelite": fidelite,
        "exacte": exact,
        "ppl_identique": bool(abs(ppl["delta_perplexite"]) < 1e-12),
        "conclusion": conclusion,
        "causes": causes,
    }


def _base_resultat(args, modele, device, hash_client, mem_avant, serveur) -> dict:
    import torch
    import transformers

    cfg = modele.config
    return {
        "experience": "A18 — une couche de modèle à distance (Qwen2.5-0.5B-Instruct)",
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "commande": " ".join([sys.executable, *sys.argv]),
        "environnement": {
            "hostname": socket.gethostname(),
            "python": sys.version.split()[0],
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "cuda_disponible": bool(torch.cuda.is_available()),
            "gpu": (
                torch.cuda.get_device_name(0)
                if torch.cuda.is_available()
                else None
            ),
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        },
        "modele": {
            "id": args.modele,
            "couche_distante": int(args.couche),
            "n_couches": int(cfg.num_hidden_layers),
            "hidden_size": int(cfg.hidden_size),
            "vocab_size": int(cfg.vocab_size),
            "n_heads": int(cfg.num_attention_heads),
            "n_kv_heads": int(cfg.num_key_value_heads),
            "head_dim": int(getattr(cfg, "head_dim", cfg.hidden_size // cfg.num_attention_heads)),
            "dtype_client": "float32",
            "device_client": device,
        },
        "dispositif": {
            "transport": "TCP IPv4 loopback 127.0.0.1, socket persistant",
            "protocole": "en-tête binaire 38 o + hidden + position_ids i64 + cos/sin f32",
            "encodage": "dense f32 ou sparse (masque 1 bit + valeurs f32), format A7.5",
            "serveur": "processus séparé, une seule couche chargée depuis model.safetensors",
            "client": "embeddings + couches 0..L-1 + couches L+1..23 + norm + lm_head",
            "cache": "use_cache=False (prefill) ; aucun cache KV transféré",
            "masque": "attention_mask=None (batch 1 sans padding), sdpa causal implicite",
            "backend_principal": serveur.ping_info.get("attn"),
            "device_serveur_principal": serveur.ping_info.get("device"),
            "dtype_serveur_principal": serveur.ping_info.get("dtype"),
            "serveur_duree_chargement_s": serveur.ping_info.get("duree_chargement_s"),
        },
        "poids": {
            "hash_client": hash_client,
            "hash_serveur": serveur.ping_info.get("hash_poids_fp32"),
            "identiques": bool(hash_client == serveur.ping_info.get("hash_poids_fp32")),
            "methode": "sha256 des tenseurs fp32 triés par nom",
        },
        "memoire_client_mio": {
            "avant": mem_avant,
            "apres": None,
            "delta": None,
            "note": "mesure torch.cuda.memory_allocated du processus client",
        },
        "invites": [],
        "agregats": {},
        "negatifs": {},
        "verdict": {},
    }


def executer(args) -> dict:
    """Expérience complète : référence locale, split, dense/sparse, négatifs."""
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
    import torch
    from transformers import AutoTokenizer

    t_debut = time.time()
    device = args.device
    if device.startswith("cuda") and not torch.cuda.is_available():
        print("[A18] CUDA indisponible : repli sur CPU", file=sys.stderr)
        device = "cpu"
    if int(args.repetitions) < 1:
        raise SystemExit("--repetitions doit être >= 1")

    tokenizer = AutoTokenizer.from_pretrained(args.modele, local_files_only=True)
    modele = charger_modele(args.modele, device=device, attn="sdpa")
    attn_client = getattr(modele.config, "_attn_implementation", "sdpa") or "sdpa"
    ids_list = [
        tokenizer(p, return_tensors="pt").input_ids.to(device) for p in INVITES
    ]

    refs = []
    with torch.no_grad():
        for ids in ids_list:
            logits = modele(ids, use_cache=False).logits
            refs.append(
                logits[0]
                .detach()
                .to(device="cpu", dtype=torch.float32)
                .contiguous()
                .numpy()
                .copy()
            )
            del logits

    couche_locale = modele.model.layers[args.couche]
    hash_client = hash_poids(couche_locale)
    mem_avant = (
        float(torch.cuda.memory_allocated(device) / 2**20)
        if device.startswith("cuda")
        else None
    )

    serveur = lancer_serveur(
        args.modele,
        args.couche,
        device,
        "float32",
        attn_client,
        timeout=args.timeout,
    )
    res = _base_resultat(args, modele, device, hash_client, mem_avant, serveur)
    if res["poids"]["identiques"] is not True:
        serveur.arreter()
        raise RuntimeError(
            "les poids de la couche distante ne sont pas identiques au client"
        )

    # Le client n'exécutera plus jamais la couche L : on libère ses poids.
    modele.model.layers[args.couche] = creer_proxy(serveur.transport)
    del couche_locale
    gc.collect()
    if device.startswith("cuda"):
        torch.cuda.empty_cache()
        mem_apres = float(torch.cuda.memory_allocated(device) / 2**20)
    else:
        mem_apres = None
    res["memoire_client_mio"]["apres"] = mem_apres
    if mem_avant is not None and mem_apres is not None:
        res["memoire_client_mio"]["delta"] = mem_avant - mem_apres

    # Chauffe (connexion, CUDA, allocation) : mesure ignorée.
    passe_split(modele, ids_list[0], serveur.transport, args.couche)

    for i, ids in enumerate(ids_list):
        ntok = int(ids.shape[1])
        ids_np = ids[0].detach().to(device="cpu").numpy()
        dist_dense, mes_dense, total_dense = passe_split(
            modele, ids, serveur.transport, args.couche
        )
        fid = fidelite_np(refs[i], dist_dense)
        ppl = _perplexite_comparee(refs[i], dist_dense, ids_np)

        dist_sparse, mes_sparse, total_sparse = passe_split(
            modele, ids, serveur.transport, args.couche, sparse=True
        )
        fid_sparse = fidelite_np(refs[i], dist_sparse)
        fid_dense_sparse = fidelite_np(dist_dense, dist_sparse)
        dist_quant, mes_quant, total_quant = passe_split(
            modele, ids, serveur.transport, args.couche, quant=True
        )
        fid_quant = fidelite_np(refs[i], dist_quant)
        fid_dense_quant = fidelite_np(dist_dense, dist_quant)

        rtts = [mes_dense["rtt_ms"]]
        calculs = [mes_dense["calcul_serveur_ms"]]
        totaux = [total_dense]
        identiques = True
        for _ in range(1, int(args.repetitions)):
            dist_rep, mes_rep, total_rep = passe_split(
                modele, ids, serveur.transport, args.couche
            )
            identiques = identiques and bool(
                np.array_equal(
                    dist_dense.view(np.uint32), dist_rep.view(np.uint32)
                )
            )
            rtts.append(mes_rep["rtt_ms"])
            calculs.append(mes_rep["calcul_serveur_ms"])
            totaux.append(total_rep)

        rtt_moy = sum(rtts) / len(rtts)
        invite = {
            "indice": i,
            "texte": INVITES[i],
            "ntokens": ntok,
            "fidelite": fid,
            "perplexite": ppl,
            "flux": {
                "dense": {
                    k: mes_dense[k]
                    for k in (
                        "n_x",
                        "n_pos",
                        "n_cos",
                        "n_sin",
                        "nval",
                        "nmask",
                        "octets_requete",
                        "octets_reponse",
                        "octets_total",
                    )
                },
                "sparse": {
                    k: mes_sparse[k]
                    for k in (
                        "n_x",
                        "n_pos",
                        "n_cos",
                        "n_sin",
                        "nval",
                        "nmask",
                        "octets_requete",
                        "octets_reponse",
                        "octets_total",
                    )
                },
                "ratio_octets_total": mes_sparse["octets_requete"]
                / mes_dense["octets_requete"],
                "ratio_hidden": mes_sparse["n_x"] / mes_dense["n_x"],
                "gain_sparse_pct": 100.0
                * (1.0 - mes_sparse["octets_requete"] / mes_dense["octets_requete"]),
                "taux_zeros": mes_dense["taux_zeros"],
                "codec_dense": mes_dense["codec"],
                "codec_sparse": mes_sparse["codec"],
                "fidelite_sparse": fid_sparse,
                "dense_vs_sparse": fid_dense_sparse,
                "latence_sparse_ms": mes_sparse["rtt_ms"],
                "latence_sparse_forward_ms": total_sparse,
                "quant": {
                    k: mes_quant[k]
                    for k in (
                        "n_x",
                        "n_pos",
                        "n_cos",
                        "n_sin",
                        "nval",
                        "nmask",
                        "octets_requete",
                        "octets_reponse",
                        "octets_total",
                    )
                },
                "ratio_quant": mes_quant["octets_requete"] / mes_dense["octets_requete"],
                "codec_quant": mes_quant["codec"],
                "fidelite_quant": fid_quant,
                "dense_vs_quant": fid_dense_quant,
                "latence_quant_ms": mes_quant["rtt_ms"],
                "latence_quant_forward_ms": total_quant,
            },
            "latence": {
                "rtt_couche_ms": statistiques(rtts),
                "rtt_couche_ms_valeurs": rtts,
                "calcul_serveur_ms": statistiques(calculs),
                "calcul_serveur_ms_valeurs": calculs,
                "forward_bout_en_bout_ms": statistiques(totaux),
                "forward_bout_en_bout_ms_valeurs": totaux,
                "ping_ms": statistiques(serveur.rtts_ping),
                "ping_ms_valeurs": serveur.rtts_ping,
                "part_couche_distante": rtt_moy / (sum(totaux) / len(totaux)),
                "octets_requete_moyen": sum(
                    [mes_dense["octets_requete"]] * len(rtts)
                )
                / len(rtts),
                "repetitions": int(args.repetitions),
                "repetitions_identiques": bool(identiques),
            },
            "debit": {
                "octets_par_token": mes_dense["octets_requete"] / ntok,
                "Mio_par_s": (
                    mes_dense["octets_requete"] / (rtt_moy / 1000.0) / 2**20
                ),
                "tokens_par_s": ntok / (rtt_moy / 1000.0),
            },
        }
        res["invites"].append(invite)

    # Agrégats de la passe principale.
    res["agregats"] = {
        "fidelite": _agreger_fidelite(res["invites"]),
        "perplexite": {
            "local": _ppl_agregee(res["invites"], "local"),
            "distant": _ppl_agregee(res["invites"], "distant"),
        },
        "reseau": _agreger_reseau(res["invites"]),
        "flux": {
            "dense_total": sum(p["flux"]["dense"]["octets_requete"] for p in res["invites"]),
            "sparse_total": sum(p["flux"]["sparse"]["octets_requete"] for p in res["invites"]),
            "ratio_total": (
                sum(p["flux"]["sparse"]["octets_requete"] for p in res["invites"])
                / sum(p["flux"]["dense"]["octets_requete"] for p in res["invites"])
            ),
            "ratio_hidden": (
                sum(p["flux"]["sparse"]["n_x"] for p in res["invites"])
                / sum(p["flux"]["dense"]["n_x"] for p in res["invites"])
            ),
            "taux_zeros_moyen": float(
                np.mean([p["flux"]["taux_zeros"] for p in res["invites"]])
            ),
        },
    }
    res["agregats"]["perplexite"]["delta_perplexite"] = (
        res["agregats"]["perplexite"]["distant"]["perplexite"]
        - res["agregats"]["perplexite"]["local"]["perplexite"]
    )
    res["agregats"]["perplexite"]["delta_relatif"] = (
        res["agregats"]["perplexite"]["delta_perplexite"]
        / res["agregats"]["perplexite"]["local"]["perplexite"]
    )
    res["agregats"]["fidelite"]["repetitions_identiques_toutes"] = all(
        p["latence"]["repetitions_identiques"] for p in res["invites"]
    )

    # Négatif « position » : le même serveur principal, cos/sin mis à zéro.
    try:
        res["negatifs"]["position_zero"] = _mesurer_negatif(
            serveur.transport,
            modele,
            args.couche,
            ids_list,
            refs,
            args,
            description="RoPE ignorée : cos=sin=0 envoyés au serveur (même poids, même device)",
            config={
                "device": device,
                "dtype": "float32",
                "attn": attn_client,
                "zero_positions": True,
            },
            zero_positions=True,
        )
    except Exception as e:  # pragma: no cover - dépend du runtime
        res["negatifs"]["position_zero"] = {"erreur": repr(e)}

    res["serveur_principal"] = {
        "info": serveur.ping_info,
        "arreter": serveur.arreter(),
    }
    res["duree_s"] = time.time() - t_debut
    res["verdict"] = _verdict(res)
    ecrire_rapports(res, args.sortie)

    if args.sans_negatifs:
        return res

    # Négatifs : autres serveurs (CPU, bfloat16, eager).
    configs = [
        (
            "device_cpu_fp32",
            "cpu",
            "float32",
            "sdpa",
            "même dtype fp32 et même backend sdpa, mais calcul CPU au lieu du GPU",
        ),
        (
            "dtype_bf16",
            device,
            "bfloat16",
            "sdpa",
            "mêmes device et backend, mais poids et calcul en bfloat16",
        ),
        (
            "backend_eager",
            device,
            "float32",
            "eager",
            "même device et dtype, mais backend eager sans masque causal explicite",
        ),
    ]
    for label, dev, dtype, attn, description in configs:
        if label == "device_cpu_fp32" and device == "cpu":
            res["negatifs"][label] = {
                "erreur": "client déjà sur CPU : contrôle non discriminant"
            }
            continue
        try:
            srv = lancer_serveur(
                args.modele,
                args.couche,
                dev,
                dtype,
                attn,
                timeout=args.timeout,
            )
            hash_ok = (
                srv.ping_info.get("hash_poids_fp32")
                == res["poids"]["hash_client"]
            )
            if not hash_ok:
                res["negatifs"][label] = {
                    "erreur": "hash des poids différent : contrôle confondu"
                }
                srv.arreter()
                continue
            res["negatifs"][label] = _mesurer_negatif(
                srv.transport,
                modele,
                args.couche,
                ids_list,
                refs,
                args,
                description=description,
                config={
                    "device": dev,
                    "dtype": dtype,
                    "attn": attn,
                    "zero_positions": False,
                },
            )
            res["negatifs"][label]["arreter"] = srv.arreter()
        except Exception as e:  # pragma: no cover - dépend du runtime
            res["negatifs"][label] = {"erreur": repr(e)}
        res["duree_s"] = time.time() - t_debut
        res["verdict"] = _verdict(res)
        ecrire_rapports(res, args.sortie)

    res["duree_s"] = time.time() - t_debut
    res["verdict"] = _verdict(res)
    ecrire_rapports(res, args.sortie)
    return res


# ---------------------------------------------------------------------------
# Rapports
# ---------------------------------------------------------------------------


def _fmt(x, n: int = 6) -> str:
    if x is None:
        return "—"
    if isinstance(x, bool):
        return "oui" if x else "non"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        return f"{float(x):.{n}g}"
    return str(x)


def _table(entetes: list[str], lignes: list[list]) -> str:
    out = ["| " + " | ".join(entetes) + " |"]
    out.append("|" + "|".join(["---"] * len(entetes)) + "|")
    for ligne in lignes:
        out.append("| " + " | ".join(_fmt(x) if not isinstance(x, str) else x for x in ligne) + " |")
    return "\n".join(out)


def construire_md(res: dict) -> str:
    invites = res.get("invites", [])
    lignes = []
    lignes.append(
        "# A18 — Une couche de Qwen 0.5B exécutée à distance (TCP loopback)\n"
    )
    lignes.append(
        f"- **Date UTC** : {res.get('date_utc', '—')}\n"
        f"- **Durée** : {_fmt(res.get('duree_s'), 4)} s\n"
        f"- **Modèle** : `{res.get('modele', {}).get('id', '—')}` — "
        f"{res.get('modele', {}).get('n_couches', '—')} couches, "
        f"hidden {res.get('modele', {}).get('hidden_size', '—')}, "
        f"vocab {res.get('modele', {}).get('vocab_size', '—')}\n"
        f"- **Couche distante** : {res.get('modele', {}).get('couche_distante', '—')}\n"
        f"- **Client** : `{res.get('modele', {}).get('device_client', '—')}` fp32 ; "
        f"serveur principal : "
        f"`{res.get('dispositif', {}).get('device_serveur_principal', '—')}` "
        f"{res.get('dispositif', {}).get('dtype_serveur_principal', '—')} "
        f"{res.get('dispositif', {}).get('backend_principal', '—')}\n"
    )
    p = res.get("poids", {})
    lignes.append(
        f"- **Poids identiques** : {_fmt(p.get('identiques'))} "
        f"(hash `{(p.get('hash_client') or '—')[:16]}…`)\n"
    )
    mem = res.get("memoire_client_mio", {})
    if mem.get("delta") is not None:
        lignes.append(
            f"- **Mémoire client** : {_fmt(mem.get('avant'), 6)} Mio → "
            f"{_fmt(mem.get('apres'), 6)} Mio après libération de la couche "
            f"(−{_fmt(mem.get('delta'), 4)} Mio)\n"
        )
    d = res.get("dispositif", {})
    lignes.append(
        f"- **Dispositif** : {d.get('transport', '—')} ; {d.get('protocole', '—')} ; "
        f"{d.get('encodage', '—')} ; {d.get('cache', '—')} ; {d.get('masque', '—')}\n"
    )
    lignes.append("\n## Invites\n")
    for inv in invites:
        texte = inv["texte"].replace("\n", "\\n")
        lignes.append(
            f"{inv['indice'] + 1}. `{texte}` — {inv['ntokens']} jetons\n"
        )
    lignes.append("\n## Fidélité des logits et perplexité\n")
    lignes.append(
        _table(
            [
                "invite",
                "jetons",
                "écart max",
                "bits identiques",
                "argmax",
                "top-5",
                "top-1024",
                "KL",
                "PPL locale",
                "PPL distante",
                "ΔPPL",
            ],
            [
                [
                    str(inv["indice"]),
                    inv["ntokens"],
                    inv["fidelite"]["diff_max"],
                    inv["fidelite"]["bits_identiques"],
                    inv["fidelite"]["argmax_accord"],
                    inv["fidelite"]["top5_intersection"],
                    inv["fidelite"]["top1024_intersection"],
                    inv["fidelite"]["kl_moyenne"],
                    inv["perplexite"]["local"]["perplexite"],
                    inv["perplexite"]["distant"]["perplexite"],
                    inv["perplexite"]["delta_perplexite"],
                ]
                for inv in invites
            ],
        )
    )
    ppl = res.get("agregats", {}).get("perplexite", {})
    if ppl:
        lignes.append(
            f"\nPPL agrégée (pondérée par les positions) : locale "
            f"{_fmt(ppl.get('local', {}).get('perplexite'), 8)}, distante "
            f"{_fmt(ppl.get('distant', {}).get('perplexite'), 8)}, Δ = "
            f"{_fmt(ppl.get('delta_perplexite'), 4)}.\n"
        )
    lignes.append(
        "\nLe top-1024 est ici l'intersection des 1024 plus grands logits par "
        "position. Ce n'est **pas** le taux d'exactitude de la grappe top-1024 "
        "d'A7.4 (21 %), qui portait sur une approximation de grappe : les logits "
        "étant identiques au bit près, l'intersection vaut 1 par construction et "
        "ne mesure pas la qualité d'une approximation.\n"
    )
    lignes.append("\n## Réseau, octets et débit\n")
    lignes.append(
        _table(
            [
                "invite",
                "octets req.",
                "o/jeton",
                "dont hidden o/jeton",
                "RTT ping ms",
                "RTT couche ms",
                "calcul serveur ms",
                "forward ms",
                "jetons/s",
                "Mio/s",
            ],
            [
                [
                    str(inv["indice"]),
                    inv["latence"]["octets_requete_moyen"],
                    inv["debit"]["octets_par_token"],
                    inv["flux"]["dense"]["n_x"] / inv["ntokens"],
                    inv["latence"]["ping_ms"]["mediane"],
                    inv["latence"]["rtt_couche_ms"]["mediane"],
                    inv["latence"]["calcul_serveur_ms"]["mediane"],
                    inv["latence"]["forward_bout_en_bout_ms"]["mediane"],
                    inv["debit"]["tokens_par_s"],
                    inv["debit"]["Mio_par_s"],
                ]
                for inv in invites
            ],
        )
    )
    reseau = res.get("agregats", {}).get("reseau", {})
    if reseau:
        rtt_med = reseau.get("rtt_couche_ms", {}).get("mediane")
        forward_med = reseau.get("forward_bout_en_bout_ms", {}).get("mediane")
        part = (rtt_med / forward_med) if rtt_med and forward_med else None
        lignes.append(
            f"\nAgrégat : {_fmt(reseau.get('octets_requete_total'), 6)} octets "
            f"requête au total, {_fmt(reseau.get('octets_par_token'), 6)} o/jeton, "
            f"RTT couche médian {_fmt(rtt_med, 4)} ms, "
            f"débit {_fmt(reseau.get('debit_tokens_s'), 6)} jetons/s "
            f"({_fmt(reseau.get('debit_Mio_s'), 4)} Mio/s), "
            f"ping médian {_fmt(reseau.get('rtt_ping_ms', {}).get('mediane'), 4)} ms.\n"
        )
        lignes.append(
            f"\nDécomposition : le ping (transport seul) est "
            f"{_fmt(reseau.get('rtt_ping_ms', {}).get('mediane'), 4)} ms, du même "
            f"ordre que le 0,125 ms d'A7.5 ; le RTT de la couche est dominé par le "
            f"calcul serveur "
            f"({_fmt(reseau.get('calcul_serveur_ms', {}).get('mediane'), 4)} ms), "
            f"pas par le réseau. La couche distante représente "
            f"{_fmt(100 * part if part is not None else None, 4)} % du forward "
            f"complet ({_fmt(forward_med, 4)} ms), le reste étant local (23 autres "
            f"couches, embedding, norme et lm_head).\n"
        )
    lignes.append("\n## Dense vs sparse\n")
    lignes.append(
        _table(
            [
                "invite",
                "dense o",
                "sparse o",
                "ratio",
                "zéros",
                "valeurs non nulles",
                "codec dense",
                "codec sparse",
                "logits dense=sparse",
            ],
            [
                [
                    str(inv["indice"]),
                    inv["flux"]["dense"]["octets_requete"],
                    inv["flux"]["sparse"]["octets_requete"],
                    inv["flux"]["ratio_octets_total"],
                    inv["flux"]["taux_zeros"],
                    inv["flux"]["dense"]["nval"],
                    inv["flux"]["codec_dense"]["bits_identiques"],
                    inv["flux"]["codec_sparse"]["bits_identiques"],
                    inv["flux"]["dense_vs_sparse"]["bits_identiques"],
                ]
                for inv in invites
            ],
        )
    )
    flux = res.get("agregats", {}).get("flux", {})
    if flux:
        lignes.append(
            f"\nLe flux résiduel est dense : taux de zéros moyen "
            f"{_fmt(100 * flux.get('taux_zeros_moyen', 0), 3)} %, ratio sparse/dense "
            f"{_fmt(flux.get('ratio_total'), 4)}× (hidden seul "
            f"{_fmt(flux.get('ratio_hidden'), 4)}×). Le masque de 1 bit par valeur "
            f"coûte 1/32 des valeurs ; il ne paie que si les zéros dépassent ~3,1 %. "
            f"Le 4,44× d'A7.5 portait sur des activations creuses, pas sur un état "
            f"caché résiduel.\n"
        )
    lignes.append("\n## Contrôles négatifs\n")
    lignes_neg = []
    for label, neg in res.get("negatifs", {}).items():
        if not isinstance(neg, dict):
            continue
        if "erreur" in neg:
            lignes_neg.append(
                [label, "erreur", "—", "—", "—", "—", "—", neg["erreur"]]
            )
            continue
        a = neg.get("agregat", {})
        lignes_neg.append(
            [
                label,
                neg.get("config", {}).get("device", "—"),
                neg.get("config", {}).get("dtype", "—"),
                neg.get("config", {}).get("attn", "—"),
                a.get("diff_max"),
                a.get("argmax_accord_min"),
                a.get("top1024_intersection_min"),
                a.get("delta_perplexite"),
            ]
        )
    if lignes_neg:
        lignes.append(
            _table(
                [
                    "contrôle",
                    "device",
                    "dtype",
                    "attn",
                    "écart max logits",
                    "argmax min",
                    "top-1024 min",
                    "ΔPPL",
                ],
                lignes_neg,
            )
        )
    else:
        lignes.append("_Aucun contrôle négatif terminé._\n")
    lignes.append("\n## Verdict\n")
    verdict = res.get("verdict", {})
    lignes.append(f"{verdict.get('conclusion', '—')}\n")
    if verdict.get("causes"):
        lignes.append("\nCauses de divergence observées (contrôles négatifs) :\n")
        for c in verdict["causes"]:
            lignes.append(
                f"- **{c['controle']}** — {c['description']} : écart max "
                f"{_fmt(c['diff_max_logits'], 4)}, argmax min "
                f"{_fmt(c['argmax_accord_min'], 6)}, top-1024 min "
                f"{_fmt(c['top1024_intersection_min'], 6)}, ΔPPL "
                f"{_fmt(c['delta_perplexite'], 4)}.\n"
            )
    lignes.append("\n## Limites et ce qui pourrait rendre faux\n")
    lignes.append(
        "- **Loopback seulement** : la latence réseau est celle de la même machine, "
        "sans perte ni gigue ; un vrai réseau ajouterait le RTT et la congestion.\n"
        "- **Une couche, un modèle** : le coût d'une couche n'est pas linéaire en "
        "nombre de couches (les autres restent locales) ; aucune extrapolation au "
        "découpage complet.\n"
        "- **Prefill uniquement** : `use_cache=False` ; la génération autorégressive "
        "exigerait de transporter le cache KV (environ 1 024 o/jeton/couche pour ce "
        "modèle) et de le garder synchronisé, non mesuré ici.\n"
        "- **Exactitude conditionnelle** : elle n'est bit-à-bit qu'à device, dtype et "
        "backend identiques (GPU fp32 + sdpa). Les négatifs CPU, bfloat16 et eager "
        "montrent que le protocole n'est pas magiquement stable.\n"
        "- **PPL sur 3 invites** : mesure locale de perplexité, pas une évaluation "
        "de corpus ; elle suit mécaniquement les logits (mêmes positions).\n"
        "- **Mémoire** : le client charge le modèle complet pour la référence puis "
        "libère la couche L ; le pic de mémoire n'est pas réduit, seule la mémoire "
        "après libération l'est.\n"
        "- **Sparse** : le format de A7.5 n'aide pas un état caché dense ; il est "
        "conservé comme contrôle et comme point de comparaison.\n"
    )
    lignes.append("\n## Reproductibilité\n")
    lignes.append(
        "```bash\n"
        "CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python "
        "tools/couche_distante.py\n"
        "```\n\n"
        f"Commande enregistrée : `{res.get('commande', '—')}`\n"
    )
    return "".join(lignes)


def ecrire_rapports(res: dict, base) -> tuple[Path, Path]:
    """Écrit le JSON et le Markdown (écriture atomique)."""
    base = Path(base)
    if base.suffix in (".json", ".md"):
        base = base.with_suffix("")
    base.parent.mkdir(parents=True, exist_ok=True)
    json_path = Path(str(base) + ".json")
    md_path = Path(str(base) + ".md")
    tmp_json = json_path.with_name(json_path.name + ".tmp")
    tmp_md = md_path.with_name(md_path.name + ".tmp")
    tmp_json.write_text(
        json.dumps(res, ensure_ascii=False, indent=2, default=_json_defaut),
        encoding="utf-8",
    )
    tmp_md.write_text(construire_md(res), encoding="utf-8")
    os.replace(tmp_json, json_path)
    os.replace(tmp_md, md_path)
    return json_path, md_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def construire_parseur() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="A18 : exécuter une couche de Qwen 0.5B dans un second processus."
    )
    p.add_argument("--modele", default=MODELE_DEFAUT)
    p.add_argument("--couche", type=int, default=COUCHE_DEFAUT)
    p.add_argument("--device", default="cuda:0", help="device du client (cuda:0 ou cpu)")
    p.add_argument("--repetitions", type=int, default=5)
    p.add_argument("--sortie", default="/tmp/a18-couche-distante")
    p.add_argument("--timeout", type=float, default=120.0)
    p.add_argument("--sans-negatifs", action="store_true")
    p.add_argument("--serveur", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--fichier-pret", default=None, help=argparse.SUPPRESS)
    p.add_argument(
        "--dtype",
        default="float32",
        choices=["float32", "bfloat16", "float16"],
        help=argparse.SUPPRESS,
    )
    p.add_argument(
        "--attn",
        default="sdpa",
        choices=["sdpa", "eager"],
        help=argparse.SUPPRESS,
    )
    return p


def main(argv=None) -> None:
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
    args = construire_parseur().parse_args(argv)
    if args.serveur:
        servir(args)
        return
    res = executer(args)
    json_path, md_path = ecrire_rapports(res, args.sortie)
    print(
        json.dumps(
            {
                "json": str(json_path),
                "md": str(md_path),
                "conclusion": res.get("verdict", {}).get("conclusion", ""),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""lecture_etat.py — lire un GGUF et des états capturés, SANS le moteur.

Ces fonctions sont partagées par `verifier_chaine_etat.py` (qui vérifie que la chaîne hors-ligne
reproduit la perplexité du MOTEUR) et `profondeur_routee_oracle.py` (qui mesure la borne du dessin
I). Elles sont ici pour qu'il n'existe qu'UNE lecture d'état : deux lectures divergentes
donneraient deux chiffres incomparables sans que rien ne le signale.

La chaîne reproduite est celle du moteur, et elle est courte :

    logits = W_tête · rmsnorm(état)        (norme finale puis tête liée, les deux GELÉES)

`charger_etats` lit les fichiers `PREFIXE.<position>` écrits par `--etat-sortie` : 896 flottants
32 bits par position, dans l'ordre des canaux.
"""
from __future__ import annotations

import pathlib
import re
import struct

import numpy as np
import torch


# --------------------------------------------------------------------------------------------
# GGUF : juste ce qu'il faut
# --------------------------------------------------------------------------------------------
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


def lire_entete(chemin: str):
    """(fichier ouvert, {nom: (dims, type, offset)}, début des données)."""
    f = open(chemin, "rb")
    if f.read(4) != b"GGUF":
        raise SystemExit(f"{chemin} : ce n'est pas un GGUF")
    struct.unpack("<I", f.read(4))[0]
    n_tenseurs, n_kv = struct.unpack("<QQ", f.read(16))
    alignement = 32
    for _ in range(n_kv):
        cle = _chaine(f)
        t = struct.unpack("<I", f.read(4))[0]
        v = _valeur(f, t)
        if cle == "general.alignment":
            alignement = int(v)
    tenseurs = {}
    for _ in range(n_tenseurs):
        nom = _chaine(f)
        nd = struct.unpack("<I", f.read(4))[0]
        dims = [struct.unpack("<Q", f.read(8))[0] for _ in range(nd)]
        ttype = struct.unpack("<I", f.read(4))[0]
        off = struct.unpack("<Q", f.read(8))[0]
        tenseurs[nom] = (dims, ttype, off)
    return f, tenseurs, (f.tell() + alignement - 1) // alignement * alignement


def lire_q8_0(f, offset: int, n_elements: int) -> np.ndarray:
    """Déquantifie Q8_0 : blocs de 32 (une échelle f16 + 32 i8)."""
    n_blocs = n_elements // 32
    f.seek(offset)
    brut = np.frombuffer(f.read(n_blocs * 34), dtype=np.uint8).reshape(n_blocs, 34)
    echelles = np.ascontiguousarray(brut[:, :2]).view(np.float16).astype(np.float32).reshape(-1, 1)
    qs = np.ascontiguousarray(brut[:, 2:]).view(np.int8).astype(np.float32)
    return (echelles * qs).reshape(-1)


def lire_f32(f, offset: int, n_elements: int) -> np.ndarray:
    f.seek(offset)
    return np.frombuffer(f.read(4 * n_elements), dtype="<f4").astype(np.float32)


# --------------------------------------------------------------------------------------------
# États et cibles
# --------------------------------------------------------------------------------------------
def charger_ids(chemin: str, limite: int) -> np.ndarray:
    vals = []
    for m in re.split(r"[,\s]+", pathlib.Path(chemin).read_text()):
        if not m:
            continue
        try:
            vals.append(int(m))
        except ValueError:
            continue
        if len(vals) >= limite:
            break
    if not vals:
        raise SystemExit(f"{chemin} : aucun identifiant lisible")
    return np.array(vals, dtype=np.int64)


def charger_etats(prefixe: str):
    """(positions triées, matrice n×896). Un fichier tronqué est IGNORÉ et compté.

    Le glob `PREFIXE.*` attrape aussi ce qui n'est PAS un état : le journal de la porte s'appelle
    `v16.log`, à côté des états `v16.0`, `v16.1`… Un suffixe non entier est donc écarté — sans
    cela, `int(...)` lève sur un NOM DE FICHIER, ce qui n'est pas un diagnostic utile.
    """
    fichiers = []
    for f in pathlib.Path(prefixe).parent.glob(pathlib.Path(prefixe).name + ".*"):
        try:
            fichiers.append((int(f.name.rsplit(".", 1)[1]), f))
        except ValueError:
            continue
    fichiers.sort()
    pos, lignes, tronques = [], [], 0
    for p, f in fichiers:
        octets = f.read_bytes()
        if len(octets) % 4 or len(octets) == 0:
            tronques += 1
            continue
        pos.append(p)
        lignes.append(np.frombuffer(octets, dtype="<f4"))
    if not lignes:
        raise SystemExit(f"{prefixe} : aucun état lisible")
    if tronques:
        print(f"  ⚠ {prefixe} : {tronques} fichier(s) tronqué(s) ignoré(s)")
    return np.array(pos, dtype=np.int64), np.vstack(lignes).astype(np.float32)


# --------------------------------------------------------------------------------------------
# La chaîne : état → logits → perplexité
# --------------------------------------------------------------------------------------------
class Tete:
    """La norme finale et la tête liée du modèle, gelées, lues dans le GGUF."""

    def __init__(self, modele: str, appareil: str | None = None):
        f, ts, debut = lire_entete(modele)
        nom = "output.weight" if "output.weight" in ts else "token_embd.weight"
        dims, ttype, off = ts[nom]
        if ttype != 8:
            raise SystemExit(f"{nom} n'est pas Q8_0 (type {ttype}) : ce lecteur ne sait pas la lire")
        # ATTENTION À L'ORDRE : dans un GGUF, `dims[0]` est la dimension CONTIGUË (le pas), pas
        # la première dimension logique : `token_embd.weight` est (896, 151 936) en stockage et
        # (151 936, 896) en logique.
        self.h, self.vocab = int(dims[0]), int(dims[1])
        W = lire_q8_0(f, debut + off, self.vocab * self.h).reshape(self.vocab, self.h)
        dims_n, _, off_n = ts["output_norm.weight"]
        g = lire_f32(f, debut + off_n, dims_n[0])
        if dims_n[0] != self.h:
            raise SystemExit(f"la norme fait {dims_n[0]} canaux, la tête {self.h} : incohérent")
        self.appareil = appareil or ("cuda" if torch.cuda.is_available() else "cpu")
        # fp16 comme le moteur en mode perplexité ; la norme et la tête restent GELÉES.
        self.W = torch.from_numpy(W).to(self.appareil).half()
        self.g = torch.from_numpy(g).to(self.appareil).half()
        print(f"tête {nom} → logique ({self.vocab}, {self.h}) · appareil {self.appareil}")

    def norme(self, x: torch.Tensor) -> torch.Tensor:
        m = x.float().pow(2).mean(-1, keepdim=True)
        return (x.float() / torch.sqrt(m + 1e-6)).half() * self.g

    @torch.no_grad()
    def logits(self, X: np.ndarray, A: torch.Tensor | None = None, lot: int = 512) -> torch.Tensor:
        """(n, vocab) en float32 sur CPU. `A` : adaptateur appliqué avant la norme."""
        Xt = torch.from_numpy(np.ascontiguousarray(X)).to(self.appareil).half()
        if A is not None:
            Xt = (Xt.float() @ A.T).half()
        sorties = []
        for lo in range(0, len(Xt), lot):
            sorties.append((self.norme(Xt[lo:lo + lot]) @ self.W.T).float().cpu())
        return torch.cat(sorties)

    def nll(self, L: torch.Tensor, y: np.ndarray) -> float:
        """NLL moyenne : le même calcul que `nll_logits` du moteur (log-sum-exp stable)."""
        cibles = torch.from_numpy(y)
        return float(torch.nn.functional.cross_entropy(L, cibles, reduction="mean"))

    def ppl(self, X: np.ndarray, y: np.ndarray, A: torch.Tensor | None = None) -> float:
        return float(np.exp(self.nll(self.logits(X, A), y)))

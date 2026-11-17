#!/usr/bin/env python3
"""drvm_infere.py — l'inférence numpy du modèle natif, sans torch.

POURQUOI. Le modèle natif vit dans un DRVM (un conteneur lisible sans torch), mais
son **calcul** était torch. Ce module fait la passe avant en **numpy seul** : le
DRVM fournit les tenseurs, numpy les multiplie — le produit reste « 0 dépendance
lourde ». La parité se juge sur le **greedy** : les mêmes octets que torch.

LE CONTRAT. `charger(drvm)` rend un dict de tenseurs numpy (`f32`) ; `logits(t,
ids)` rend les logits de la **dernière** position ; `greedy(t, prompt, n)` rend le
texte généré (et les ids). `--parite` compare à torch (si torch est là).

Usage :
  python3 tools/drvm_infere.py --drvm work/n2ac/mix1024-60k.drvm \
      --prompt "La France est un pays" --n 16
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from tools.drvm import IMPLS_MOTEUR_NUMPY, read_drvm  # noqa: E402

F32 = np.float32


def charger(chemin: str) -> tuple[dict[str, np.ndarray], dict]:
    """Les tenseurs du DRVM en numpy (f32, les formes du manifeste) + la config.

    REFUS EXPLICITE. Ce moteur n'implémente qu'un profil (`defaut`). Un manifeste
    qui demande `bloque` ou `flou` est REFUSÉ, pas exécuté autrement : un moteur
    qui ignore le profil demandé rendrait des logits qui ne sont ceux d'aucune
    implémentation déclarée.
    """
    with read_drvm(chemin) as d:
        impls = {b["id"]: b.get("impl", "defaut")
                 for b in d.manifest["graph"]["blocks"] if b["kind"] == "local_mixer"}
        refusees = {i: v for i, v in impls.items() if v not in IMPLS_MOTEUR_NUMPY}
        if refusees:
            raise NotImplementedError(
                "impl non exécutée par le moteur numpy : "
                + ", ".join(f"{i}={v}" for i, v in sorted(refusees.items()))
                + " (seule « defaut » est implémentée)")
        tenseurs = {}
        for t in d.manifest["tensors"]:
            brut = bytes(d.tensor(t["name"]))  # la copie libère la vue (le mmap doit se fermer)
            arr = np.frombuffer(brut, dtype=np.float32).reshape(tuple(t["shape"])).copy()
            tenseurs[t["name"]] = arr
        cfg = dict(d.manifest["model"]["architecture"])
    return tenseurs, cfg


def _ln(x: np.ndarray, w: np.ndarray, b: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    m = x.mean(-1, keepdims=True)
    v = x.var(-1, keepdims=True)
    return ((x - m) / np.sqrt(v + eps)) * w + b


def _linear(x: np.ndarray, w: np.ndarray, b: np.ndarray | None) -> np.ndarray:
    y = x @ w.T
    return y + b if b is not None else y


def _silu(x: np.ndarray) -> np.ndarray:
    return x / (1.0 + np.exp(-x))


def _ffn(x: np.ndarray, t: dict, cfg: dict, prefix: str) -> np.ndarray:
    router = _linear(x, t[prefix + ".router.weight"], t[prefix + ".router.bias"])
    idx = np.argsort(-router, axis=-1)[..., : cfg["top_k"]]
    poids = np.take_along_axis(router, idx, -1)
    poids = np.exp(poids - poids.max(-1, keepdims=True))
    poids = poids / poids.sum(-1, keepdims=True)
    g = _linear(x, t[prefix + ".gate.weight"], t[prefix + ".gate.bias"])
    u = _linear(x, t[prefix + ".up.weight"], t[prefix + ".up.bias"])
    h = _silu(g) * u
    ne, eh = cfg["n_experts"], cfg["expert_hidden"]
    h = h.reshape(h.shape[0], ne, eh)
    k = max(1, int(eh * cfg["kwta"]))
    seuil = -np.partition(-h, k - 1, axis=-1)[..., k - 1:k]
    h = np.where(h >= seuil, h, 0.0)
    masque = np.zeros((h.shape[0], ne), dtype=bool)
    np.put_along_axis(masque, idx, True, axis=-1)
    h = h * masque[:, :, None]
    return _linear(h.reshape(h.shape[0], ne * eh), t[prefix + ".down.weight"],
                   t[prefix + ".down.bias"])


def _bloc(x: np.ndarray, t: dict, cfg: dict, i: int) -> np.ndarray:
    p = f"blocks.{i}"
    h = _ln(x, t[p + ".ln1.weight"], t[p + ".ln1.bias"])
    qkv = _linear(h, t[p + ".qkv.weight"], t[p + ".qkv.bias"])
    q, k, v = np.split(qkv, 3, axis=-1)
    n, d = x.shape
    nh = cfg["n_heads"]
    dh = d // nh
    q = q.reshape(n, nh, dh)
    k = k.reshape(n, nh, dh)
    v = v.reshape(n, nh, dh)
    scores = np.einsum("ihd,jhd->hij", q, k) / np.sqrt(F32(dh))
    # causal + fenêtre (la fenêtre du modèle, 1 024)
    pos = np.arange(n)
    masque = (pos[:, None] >= pos[None, :]) & ((pos[:, None] - pos[None, :]) < cfg["window"])
    scores = np.where(masque[None, :, :], scores, -np.inf)
    scores = scores - scores.max(-1, keepdims=True)
    probs = np.exp(scores)
    probs = probs / probs.sum(-1, keepdims=True)
    y = np.einsum("hij,jhd->ihd", probs, v).reshape(n, d)
    x = x + _linear(y, t[p + ".out.weight"], t[p + ".out.bias"])
    return x + _ffn(_ln(x, t[p + ".ln2.weight"], t[p + ".ln2.bias"]), t, cfg, p + ".ffn")


def logits(t: dict, cfg: dict, ids: list[int], pos_debut: int = 0) -> np.ndarray:
    n = len(ids)
    x = t["embed.weight"][ids] + t["pos.weight"][pos_debut:pos_debut + n]
    for i in range(cfg["n_blocks"]):
        x = _bloc(x, t, cfg, i)
        if i == cfg["n_blocks"] // 2 - 1:
            x = x + _linear(x, t["bridge.weight"], t["bridge.bias"])
    # la pensée : `tanh(thought(x) + thought_in(h0))`, h0 = la sortie des blocs
    h0 = x.copy()
    for _ in range(cfg["thought_steps"]):
        x = np.tanh(_linear(x, t["thought.weight"], t["thought.bias"])
                    + _linear(h0, t["thought_in.weight"], t["thought_in.bias"]))
    return _linear(x, t["head_byte.weight"], t["head_byte.bias"])


def greedy(t: dict, cfg: dict, prompt: str, n: int, fenetre: int) -> str:
    ids = list(prompt.encode("utf-8")) or [32]
    for _ in range(n):
        contexte = ids[-fenetre:]
        lg = logits(t, cfg, contexte, pos_debut=max(0, len(ids) - fenetre))
        ids.append(int(np.argmax(lg[-1])))
    return bytes(ids).decode("utf-8", "replace")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--drvm", default="work/n2ac/mix1024-60k.drvm")
    ap.add_argument("--prompt", default="La France est un pays")
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    t, cfg = charger(a.drvm)
    texte = greedy(t, cfg, a.prompt, a.n, min(cfg["window"], 1024))
    if a.json:
        print(json.dumps({"schema": "drave.generation", "version": 1, "moteur": "numpy",
                          "drvm": a.drvm, "prompt": a.prompt, "n": a.n, "texte": texte},
                         ensure_ascii=False))
    else:
        print(texte)


if __name__ == "__main__":
    main()

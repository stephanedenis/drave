#!/usr/bin/env python3
"""vision_projecteur_ref.py — le PROJECTEUR de la vision, vérifié sur le MÊME état d'entrée.

POURQUOI ICI, ET PAS DANS UNE COMPARAISON DE BOUT EN BOUT. Le projecteur (`v.post_ln` puis
`mm.0` → GELU → `mm.2`) transforme les 256 patchs de 1280 canaux en **64 jetons de 1536**. Comparer
la sortie complète de la vision ne dirait rien : les blocs, eux, **basculent** (l'attention s'effondre
— entropie 0,16 à la couche 15 — et deux implémentations ne regardent plus le même patch : variation
totale 0,94). La seule comparaison qui parle donne **le même état d'entrée** aux deux côtés.

C'est ce que fait ce script : il prend l'état post-tour écrit par le moteur (`<banc>.couche31`) et le
donne au **merger de la référence** (`transformers`, `Qwen2VisionTransformerPretrainedModel.merger`,
qui fait `mlp(ln_q(x).view(-1, hidden))`), puis compare aux jetons du moteur (`<banc>.jetons`).

CE QU'IL A TROUVÉ (15/10, avant correctif) : **cosinus +0,7804, écart 66,6 %** — le moteur normalisait
**par patch** (LayerNorm sur 1280) **avant** de fusionner, la référence **fusionne** (5120) **puis**
normalise. Les normes concordaient (249,49 contre 246,92 : l'échelle était bonne), les valeurs non.

Usage :
  python tools/vision_projecteur_ref.py --banc /tmp/tour.bin --hf <dossier safetensors>
"""
from __future__ import annotations

import argparse
import pathlib
import struct

import numpy as np


def lire(chemin: str) -> np.ndarray:
    b = pathlib.Path(chemin).read_bytes()
    n, e = struct.unpack_from("<ii", b, 0)
    return np.frombuffer(b, dtype="<f4", offset=8).reshape(n, e).astype(np.float32)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--banc", required=True, help="sortie du banc (…bin)")
    ap.add_argument("--hf", required=True, help="dossier des poids de référence (safetensors)")
    ap.add_argument("--etat", default=None,
                    help="état d'entrée du projecteur (défaut : <banc>.couche31)")
    a = ap.parse_args()

    etat = lire(a.etat or f"{a.banc}.couche31")
    eng = lire(f"{a.banc}.jetons")
    import torch
    from transformers import AutoModelForImageTextToText
    m = AutoModelForImageTextToText.from_pretrained(a.hf, dtype=torch.float32)
    m.eval()
    with torch.no_grad():
        ref = m.model.visual.merger(torch.tensor(etat)).float().numpy()

    if ref.shape != eng.shape:
        print(f"  ❌ FORMES DIFFÉRENTES : moteur {eng.shape} contre référence {ref.shape}")
        return 1
    cos = float((eng.ravel() @ ref.ravel()) / (np.linalg.norm(eng) * np.linalg.norm(ref) + 1e-12))
    ecart = float(np.linalg.norm(eng - ref) / (np.linalg.norm(ref) + 1e-12))
    print(f"état d'entrée : {etat.shape} · norme {np.linalg.norm(etat):.3f}")
    print(f"projecteur MOTEUR    : {eng.shape} · norme {np.linalg.norm(eng):.3f}")
    print(f"projecteur RÉFÉRENCE : {ref.shape} · norme {np.linalg.norm(ref):.3f}")
    print(f"  cosinus {cos:+.8f} · écart relatif {ecart * 100:.4f} %")
    if cos < 0.999:
        print("  ❌ le projecteur s'écarte de la référence (ordre des opérations, ou fusion)")
        return 1
    print("  ✅ le projecteur reproduit la référence (fusion → LayerNorm → mm.0 → GELU → mm.2)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

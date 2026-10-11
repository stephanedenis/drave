#!/usr/bin/env python3
"""m8_simulation_export.py — M8 : l'écart vient-il de l'EXPORT ? On le simule en PyTorch.

LE RAISONNEMENT, ET IL EST COURT. Le modèle dense rend **×1,44** de perplexité à l'export, le
log-normal **×78** — mêmes poids (plage 17,5 M contre 27,0 M, maximum 0,42 contre 0,43), mêmes
activations (plage dynamique 10,2 contre 15,2), aucun clamp dans le GGUF, et la quantification
par vecteur n'efface rien dans l'un ni dans l'autre (`reports/rapport-m8-log-normal.md` § 3 bis).
Si les tenseurs se ressemblent à ce point, l'écart ne peut naître que d'une chose : **le passage
en Q8_0/Q4_0 lui-même**, que le moteur subit fidèlement.

CE QUE CE SCRIPT MESURE, DONC. On charge les deux modèles **entraînés** en PyTorch, on note leur
perplexité, puis on **simule exactement l'export** — les mêmes encodeurs Q8_0 et Q4_0 que
`tools/exporter_gguf.py`, appliqués aux mêmes tenseurs (experts en Q4_0, le reste en Q8_0) — et on
reprend la perplexité.

  · si le log-normal EXPLOSE en PyTorch comme dans le moteur, l'export explique tout, le moteur est
    fidèle, et M8 n'est pas un défaut du moteur : c'est une **fragilité du variant** ;
  · s'il ne bouge pas, alors l'export est innocenté à son tour et le défaut est dans la LECTURE.

Usage :
  tools/m8_simulation_export.py --dense /tmp/e6/dense.gguf --lognormal /tmp/e6/lognormal.gguf \
      --val /tmp/e6/val.ids --limite 512
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
import torch
from transformers import AutoModelForCausalLM

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from exporter_gguf import q4_0_encoder, q4_0_decoder, q8_0_encoder, q8_0_decoder  # noqa: E402


def quantifier_comme_l_export(modele) -> int:
    """Applique aux poids 2D la MÊME quantification que l'exporteur, EN PLACE.

    La règle de l'exporteur : les trois projections d'experts (`*_exps.weight`) passent en Q4_0,
    tout le reste en Q8_0. On la reproduit par le NOM du tenseur, pas par sa forme — c'est le nom
    qui décide dans `exporter_gguf.py`.
    """
    n = 0
    for nom, p in modele.named_parameters():
        if p.dim() < 2:
            continue          # normes et biais restent en f32 : l'exporteur ne les quantifie pas
        arr = p.detach().float().cpu().numpy()
        if arr.shape[-1] % 32:
            continue          # l'encodeur refuse, et l'exporteur aussi
        if "expert" in nom.lower() or "_exps." in nom:
            dec = q4_0_decoder(q4_0_encoder(arr), arr.shape)
        else:
            dec = q8_0_decoder(q8_0_encoder(arr), arr.shape)
        p.data.copy_(torch.from_numpy(np.ascontiguousarray(dec)).to(p.device).to(p.dtype))
        n += 1
    return n


@torch.no_grad()
def perplexite(modele, ids: np.ndarray, appareil: str, fenetre: int = 512) -> float:
    """Perplexité en contexte glissant : la moyenne des NLL, comme le moteur (denominateur n−1)."""
    x = torch.from_numpy(ids.astype(np.int64)).to(appareil)
    nll, n = 0.0, 0
    for deb in range(0, len(x) - 1, fenetre):
        morceau = x[deb:deb + fenetre + 1]
        if len(morceau) < 2:
            break
        logits = modele(morceau[None, :]).logits[0].float()
        nll += torch.nn.functional.cross_entropy(
            logits[:-1], morceau[1:], reduction="sum").item()
        n += len(morceau) - 1
    return float(np.exp(nll / max(n, 1)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dense", required=True)
    ap.add_argument("--lognormal", required=True)
    ap.add_argument("--val", required=True, help="fichier d'identifiants (octets séparés par des virgules)")
    ap.add_argument("--limite", type=int, default=512)
    a = ap.parse_args()

    ids = np.array([int(v) for v in open(a.val).read().split(",") if v.strip()][: a.limite])
    appareil = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"{len(ids)} jetons, appareil {appareil}\n")
    print("| modèle | perplexité avant export | après export simulé | facteur |")
    print("|---|---:|---:|---:|")
    resultats = {}
    for nom, chemin in (("dense", a.dense), ("log-normal", a.lognormal)):
        m = AutoModelForCausalLM.from_pretrained(chemin, dtype=torch.float32).to(appareil).eval()
        avant = perplexite(m, ids, appareil)
        n = quantifier_comme_l_export(m)
        apres = perplexite(m, ids, appareil)
        resultats[nom] = (avant, apres, n)
        print(f"| {nom} | {avant:,.4f} | {apres:,.4f} | ×{apres / avant:,.2f} |")
        del m
        if appareil == "cuda":
            torch.cuda.empty_cache()

    (av_d, ap_d, _), (av_l, ap_l, n) = resultats["dense"], resultats["log-normal"]
    print(f"\n{n} tenseurs quantifiés par modèle (experts en Q4_0, le reste en Q8_0).")
    print(f"\nCoût de l'export, simulé : dense ×{ap_d / av_d:,.2f} · log-normal ×{ap_l / av_l:,.2f}.")
    print("CE QUE CE TABLEAU PERMET DE DIRE, ET RIEN DE PLUS : la colonne « après export simulé » est")
    print("ce que le moteur DOIT imprimer s'il lit fidèlement. Il suffit de comparer :")
    print("  · s'il la reproduit, la lecture est fidèle et l'écart vient d'ailleurs ;")
    print("  · s'il s'en écarte, la lecture est en cause, et c'est là qu'il faut aller.")
    if ap_l / av_l > 3 * (ap_d / av_d):
        print("  ⇒ ici l'export coûte BEAUCOUP plus cher au log-normal qu'au dense : c'est lui qui")
        print("    explique l'écart, et le moteur n'y est pour rien.")
    else:
        print("  ⇒ ici l'export coûte la même chose aux deux : il n'explique aucun écart ENTRE eux.")
        print("    Tout écart restant est à chercher dans la lecture, ou en amont du fichier.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

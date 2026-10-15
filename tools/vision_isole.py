#!/usr/bin/env python3
"""vision_isole.py — vérifier les conventions d'une couche PROFONDE, en ISOLATION.

POURQUOI L'ISOLATION, ET PAS UNE COMPARAISON DE SORTIES. Comparer les sorties de la tour du moteur
à celles d'une formule indépendante ne dit rien au-delà de la couche ~8 : l'attention **s'effondre**
(entropie 3,36 à la couche 1, **0,16** à la couche 15) et **bascule** d'un patch à l'autre — la
variation totale entre les deux implémentations atteint **0,94** (mesuré le 15/10). Aucune tolérance
ne réconcilie deux calculs qui ne regardent plus le même endroit, et ce n'est la faute d'aucun des
deux.

LA MÉTHODE. On donne aux DEUX implémentations **le même état d'entrée** et on compare la sortie de
la couche **seule** :
  1. le moteur déroule la tour et écrit l'état après chaque couche (`DRAVE_VISION_COUCHES=N`) ;
  2. pour la couche L, on reprend l'état de la couche L-1 et on **demande au moteur de ne calculer
     que L** (`DRAVE_VISION_ENTREE` + `DRAVE_VISION_ETAT=L`) ;
  3. la formule numpy refait **cette** couche depuis le même état, et on compare.

Résultat du 15/10 sur la couche 15 (la plus « chaotique » de la tour) : **cosinus +1,00000141**,
écart max relatif **1,14e-06** — les conventions du moteur sont **justes**, et l'écart de 0,75 qu'on
mesurait sur les sorties était bien la bascule de l'attention, pas une erreur de code.

Usage :
  python tools/vision_isole.py --banc /tmp/tour.bin --poids /tmp/tour.bin.poids32 \\
      --couches 1,8,15,23,31 [--moteur ./drave-core/target/release/drave --mmproj models/vision/…]
"""
from __future__ import annotations

import argparse
import os
import pathlib
import struct
import subprocess
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from vision_bloc_ref import ln, tourner          # noqa: E402


def lire(chemin: str) -> np.ndarray:
    b = pathlib.Path(chemin).read_bytes()
    n, e = struct.unpack_from("<ii", b, 0)
    return np.frombuffer(b, dtype="<f4", offset=8).reshape(n, e).astype(np.float32)


def couche_numpy(x, poids: np.ndarray, e: int, nff: int, nh: int) -> np.ndarray:
    """Une couche, la formule du moteur, écrite indépendamment (mêmes conventions, autre code)."""
    cur = [0]

    def pr(n):
        deb = cur[0]
        cur[0] = deb + n
        return poids[deb:deb + n].copy()

    ln1, ln1b, ln2, ln2b = pr(e), pr(e), pr(e), pr(e)
    wq, bq = pr(e * e).reshape(e, e), pr(e)
    wk, bk = pr(e * e).reshape(e, e), pr(e)
    wv, bv = pr(e * e).reshape(e, e), pr(e)
    wo, bo = pr(e * e).reshape(e, e), pr(e)
    w1, b1 = pr(nff * e).reshape(nff, e), pr(nff)
    w2, b2 = pr(e * nff).reshape(e, nff), pr(e)
    hd = e // nh
    nc = int(round(np.sqrt(x.shape[0])))
    xn = ln(x, ln1, ln1b)
    qq, kk, vv = xn @ wq.T + bq, xn @ wk.T + bk, xn @ wv.T + bv
    for pi in range(x.shape[0]):
        for h in range(nh):
            tourner(qq[pi, h * hd:(h + 1) * hd], pi // nc, pi % nc, hd)
            tourner(kk[pi, h * hd:(h + 1) * hd], pi // nc, pi % nc, hd)
    sc = (qq @ kk.T) / np.sqrt(hd)
    sc -= sc.max(-1, keepdims=True)
    att = np.exp(sc)
    att /= att.sum(-1, keepdims=True)
    y = x + (att @ vv) @ wo.T + bo
    xn2 = ln(y, ln2, ln2b)
    act = xn2 @ w1.T + b1
    act = act / (1.0 + np.exp(-1.702 * act))          # quick-GELU
    return y + act @ w2.T + b2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--banc", required=True, help="sortie du banc (tour complète, DRAVE_VISION_COUCHES=N)")
    ap.add_argument("--poids", required=True, help="…poids32 (DRAVE_VISION_POIDS=all)")
    ap.add_argument("--mmproj", default="models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf")
    ap.add_argument("--moteur", default="./drave-core/target/release/drave")
    ap.add_argument("--noyau", default="/tmp/vision-noyau-somme.f32",
                    help="noyau de patchs réparé (le mmproj a perdu une tranche temporelle)")
    ap.add_argument("--image", default=None, help="image f32 fournie (DRAVE_VISION_IMAGE)")
    ap.add_argument("--couches", default="1,8,15,23,31")
    a = ap.parse_args()

    brut = pathlib.Path(a.poids).read_bytes()
    e, nff, nh, nl = struct.unpack_from("<iiii", brut, 0)
    octets = 4 * (4 * e + 4 * (e * e + e) + (nff * e + nff) + (e * nff + e))
    pires = 0.0
    for L in [int(x) for x in a.couches.split(",")]:
        etat = f"{a.banc}.couche{L - 1}" if L > 0 else f"{a.banc}"
        if not pathlib.Path(etat).exists():
            print(f"  ⚠️ {etat} absent (lancer le banc avec DRAVE_VISION_COUCHES={L})")
            return 1
        tmp = f"/tmp/vision-isole{L}.f32"
        pathlib.Path(tmp).write_bytes(pathlib.Path(etat).read_bytes()[8:])
        env = dict(os.environ, DRAVE_VISION_ENTREE=tmp, DRAVE_VISION_ETAT=str(L),
                   DRAVE_VISION_COUCHES=str(L + 1))
        if a.noyau:
            env["DRAVE_VISION_NOYAU"] = a.noyau
        if a.image:
            env["DRAVE_VISION_IMAGE"] = a.image
        sortie = f"/tmp/vision-isole{L}.bin"
        r = subprocess.run([a.moteur, a.mmproj, "--banc-vision", sortie],
                           env=env, capture_output=True, text=True)
        if not pathlib.Path(f"{sortie}.couche{L}").exists():
            print(f"  ❌ le moteur n'a pas écrit la couche {L} :\n{r.stdout[-300:]}\n{r.stderr[-300:]}")
            return 1
        poids = np.frombuffer(brut, dtype="<f4", offset=16 + L * octets,
                              count=octets // 4).copy()
        x = lire(etat)
        y = couche_numpy(x, poids, e, nff, nh)
        eng = lire(f"{sortie}.couche{L}")
        cos = float((y.ravel() @ eng.ravel()) / (np.linalg.norm(y) * np.linalg.norm(eng) + 1e-12))
        ecart = float(np.abs(y - eng).max() / max(1e-9, np.abs(y).max()))
        pires = max(pires, ecart)
        etat_txt = "✅" if ecart < 1e-4 else "❌"
        print(f"  {etat_txt} couche {L:>2} EN ISOLATION : cosinus {cos:+.8f} · "
              f"écart max relatif {ecart:.3e}")
    print(f"\n  écart max sur les couches vérifiées : {pires:.3e}")
    print("  ✅ les conventions de ces couches sont celles de la formule" if pires < 1e-4
          else "  ❌ au moins une couche s'écarte des conventions")
    return 0 if pires < 1e-4 else 1


if __name__ == "__main__":
    raise SystemExit(main())

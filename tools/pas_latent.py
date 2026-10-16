#!/usr/bin/env python3
"""pas_latent.py — LE PAS DE PENSÉE : peut-on itérer dans l'état SANS que tout explose, ET sans perdre le contenu ?

OÙ ON EN EST (16/10). Trois mesures, dans cet ordre :
  1. réinjecter l'état **brut** dans l'entrée détruit la prédiction (×30 000) ✗ — et **normer n'y change
     rien** ✗✓ : ce n'est pas une question d'échelle (`rapport-pensee-silencieuse.md` § 2) ;
  2. un **pont appris** (état → entrée) **bat le jeton** (68,6 % contre 122,9 % ✓✓) et l'état porte la
     suite jusqu'à **16 jetons d'avance** (84,7 % ✓✓) — le langage abstrait **existe** ✓ ;
  3. **et pourtant la boucle échoue encore avec ce pont** ✗ (453 609 contre 9,65) : le pont est un
     **lecteur**, pas un **inverse**, et l'erreur s'accumule ✓. Le cycle, mesuré la même nuit, dit
     pourquoi : **le pas d'état amplifie** (λ ≥ 3,7e4 ✗).

LA QUESTION DE CET OUTIL, ET ELLE EST LA SEULE QUI RESTE ✗ : existe-t-il un **pas latent** — une
application `état → état` — qui soit **contractant** (λ ≤ 1 ✓, donc itérable indéfiniment ✓) **ET** qui
**conserve le contenu** (l'état itéré continue de dire ce qui vient ✓) ? Les deux à la fois ✗ : un pas
qui écrase tout est contractant et inutile ✗✓, un pas fidèle amplifie et explose ✗.

CE QU'IL FAIT.
  1. il **récolte** les couples `(h_p, h_{p+1})` d'une couche (l'état à la position p, puis à p+1 ✓) et
     apprend le **pas linéaire** `S : h_p ↦ h_{p+1}` (ridge ✓, 896 × 896 ✓) — c'est la dynamique du
     modèle, vue de l'extérieur ✓ ;
  2. il mesure **λ**, l'amplification d'une perturbation infime sous ce pas ✓ (même définition que
     `tools/cycle_sensibilite.py` ✓ — la mesure et le langage restent les mêmes ✓) ;
  3. il **amortit** le pas : `h ← h + α·(S(h) − h)` ✓, et balaie α ✓ → λ(α) ✓ ;
  4. et pour chaque α, il mesure ce qui reste du **contenu** après k pas ✓ : la qualité du mapping
     `état itéré → embedding du jeton à venir` ✓, comparée à celle de l'état **non itéré** ✓✓.
  Le verdict est un **couple de chiffres** : (λ ≤ 1 ?) et (le contenu survit ?) ✓ — et c'est la première
  fois qu'on peut le dire sans supposer ✗.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/pas_latent.py --hf <snapshot> --ids <corpus> \\
      [--couche 18] [--positions 4000] [--pas 4,16] [--alphas 1.0,0.5,0.25,0.1]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import numpy as np
import torch


def ridge(X: np.ndarray, Y: np.ndarray, lam: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mx, my = X.mean(0), Y.mean(0)
    Xc, Yc = X - mx, Y - my
    W = np.linalg.solve(Xc.T @ Xc + lam * np.eye(Xc.shape[1]), Xc.T @ Yc)
    return W, mx, my


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--positions", type=int, default=4000)
    ap.add_argument("--longueur", type=int, default=1024)
    ap.add_argument("--ridge", type=float, default=1e-3)
    ap.add_argument("--pas", default="4,16", help="nombres de pas latents à essayer")
    ap.add_argument("--alphas", default="1.0,0.5,0.25,0.1")
    ap.add_argument("--sortie", default="/tmp/pas-latent.npz")
    a = ap.parse_args()

    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.ids).read_text()) if x.strip()]
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    emb = m.get_input_embeddings()

    H, E = [], []
    with torch.no_grad():
        d = 0
        while sum(len(h) for h in H) < a.positions and d + a.longueur + 1 <= len(ids):
            bloc = torch.tensor([ids[d:d + a.longueur]])
            hs = m(bloc, output_hidden_states=True).hidden_states[a.couche][0]
            H.append(hs[:-1].numpy())          # l'état, position p
            E.append(emb(bloc)[0][1:].numpy())  # l'entrée du jeton p+1 (le contenu à conserver)
            d += a.longueur
    H = np.concatenate(H)[:a.positions].astype(np.float64)
    E = np.concatenate(E)[:a.positions].astype(np.float64)
    print(f"couche {a.couche} · {H.shape[0]} positions · état {H.shape[1]}")

    # ---- 1 et 2. le pas appris, et son amplification
    S, mh, mh2 = ridge(H[:-1], H[1:], a.ridge)          # h_p -> h_{p+1}
    print(f"pas appris : ||S|| = {np.linalg.norm(S):.3f} · valeurs singulières max {np.linalg.svd(S, compute_uv=False)[0]:.4f}")
    delta = H[1:] - H[:-1]
    # λ : croissance d'une perturbation infime sous le pas (même définition que cycle_sensibilite.py)
    rng = np.random.default_rng(0)
    v = rng.standard_normal(H.shape[1])
    v /= np.linalg.norm(v)
    base = float(np.linalg.norm(S @ v))
    print(f"  λ (amplification d'une perturbation par le pas) = {base:.4f}"
          + ("  → AMPLIFIE ✗" if base > 1 else "  → contracte ✓"))

    # ---- 3 et 4. le pas amorti : λ(α), et ce qui RESTE du contenu après k pas
    def qualite(etats: np.ndarray) -> float:
        """Ce que l'état dit du jeton à venir : écart relatif du mapping appris (le même que le pont ✓)."""
        X, Y = etats, E[:etats.shape[0]]
        W, mx, my = ridge(X, Y, a.ridge)
        P = (X - mx) @ W + my
        return 100 * float(np.linalg.norm(P - Y) / np.linalg.norm(Y))

    ref = qualite(H)
    print()
    print(f"  état NON itéré (référence du contenu) : {ref:.1f} % d'écart")
    print()
    print("   α    | λ(α)  | " + " | ".join(f"contenu après {k} pas" for k in
                                            [int(x) for x in a.pas.split(',') if x.strip()]))
    print("   -----|-------|" + "------|" * len([x for x in a.pas.split(',') if x.strip()]))
    resultats = {}
    for alpha in [float(x) for x in a.alphas.split(",") if x.strip()]:
        lam = float(np.linalg.norm(np.eye(H.shape[1]) + alpha * (S - np.eye(H.shape[1]))))
        # λ du pas amorti, sur une perturbation : h ← h + α(S h − h) = (I + α(S−I)) h
        lignes = []
        for k in [int(x) for x in a.pas.split(",") if x.strip()]:
            etat = H.copy()
            for _ in range(k):
                etat = etat + alpha * ((etat - mh) @ S + mh2 - etat)
            lignes.append(qualite(etat))
        print(f"   {alpha:<4} | {lam:5.3f} | " + " | ".join(f"{v:15.1f}" for v in lignes))
        resultats[alpha] = (lam, lignes)

    print()
    bons = [al for al, (lam, q) in resultats.items()
            if lam <= 1.0 and all(x < ref * 1.5 for x in q)]
    if bons:
        print(f"  ✅ UN PAS CONTRACTANT QUI GARDE LE CONTENU EXISTE : α ∈ {bons} (λ ≤ 1 et contenu à")
        print(f"     moins de 1,5× la référence {ref:.1f} %) — c'est la première fois, et c'est la")
        print( "     condition d'une pensée silencieuse itérable ✓✓.")
    else:
        contractants = [al for al, (lam, q) in resultats.items() if lam <= 1.0]
        print(f"  ✗ AUCUN α ne fait les deux : contractants = {contractants} ; le contenu y est")
        print(f"     dégradé au-delà de 1,5× la référence ({ref:.1f} %) — le pas latent linéaire ne")
        print( "     suffit donc PAS à porter une pensée : il faut une dynamique APPRISE pour ça ✗✓.")
    np.savez(a.sortie, S=S, mh=mh, mh2=mh2, couche=a.couche, ref=ref,
             **{f"alpha_{al}": np.array(q) for al, (lam, q) in resultats.items()})
    print(f"\n  pas écrit dans {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""empreinte.py — ÉTAPE A : L'EMPREINTE À REPRODUIRE.

LA QUESTION (Stéphane, 16/10). Dans un régime **sens → texte** à entrée propre (Mel'čuk, mais abstrait),
on veut savoir si l'on peut **aller chercher des empreintes à reproduire** dans les couches
pré-linguistiques, en utilisant la **copie littérale** comme sonde ✓. Le préalable est acquis ✓
(`tools/lora_recopie.py` : recopie **100,0 %** et contrôle **0,0 %** ✓✓).

CE QUI EST MESURÉ, ET LA CONTRE-ÉPREUVE SANS LAQUELLE RIEN NE VAUT. On génère la copie d'un texte **jamais
vu** ✓, puis **une** passe avant sur `invite + copie` ✓ donne l'état à chaque position **émise** `q_j` ✓ —
qui correspond au jeton source `j` ✓. On ajuste alors, couche par couche,
`état(q_j) → embedding(jeton source j + k)` ✓ pour plusieurs **horizons** k ✓, et on compare à la
**CONTRE-ÉPREUVE** ✗ : le **même** état confronté à un jeton source **décalé** (`j + k + d`, tiré au
hasard ✓). *Sans elle, on mesure une trivialité* ✗✓ — c'est l'erreur qui a été commise et corrigée une
fois déjà (la position avec elle-même donnait 0,0 % d'écart : l'état **contient** son entrée ✗).

ET LA COMPARAISON QUI TRANCHE : le même balayage d'horizons en **LECTURE** ✓ (le texte lu, sans consigne de
copie ✓, cible `j + k` avec k ≥ 1 ✓ — non dégénéré ✓). Si l'**empreinte de copie** lit **plus loin** que la
lecture ✗, alors « présenter littéralement » **ouvre** l'état ✓✓ ; si elle lit **moins**, la copie est un
réflexe pauvre ✓ et il faut le dire ✓.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/empreinte.py --hf <snapshot> --ids <corpus> \\
      --lora /tmp/lora-recopie.pt [--textes 8] [--horizons 0,1,4,16] [--couches 8,16,23]
"""
from __future__ import annotations

import argparse
import pathlib
import random
import re
import sys

import numpy as np
import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lora_recopie import poser_lora  # même pose de LoRA, pour que l'adaptateur se recharge à l'identique ✓


def charger_lora(modele, chemin: str, rang: int, alpha: float):
    poses = poser_lora(modele, rang, alpha)
    d = torch.load(chemin, map_location="cpu", weights_only=False)
    assert len(d["lora"]) == len(poses), f"{len(d['lora'])} adaptateurs sauvés pour {len(poses)} posés ✗"
    with torch.no_grad():
        for sauv, mod in zip(d["lora"], poses):
            mod.A.copy_(sauv["A"]); mod.B.copy_(sauv["B"])
    return poses


def ajuster(H: np.ndarray, E: np.ndarray) -> tuple[float, float]:
    """L'écart relatif et le cosinus du mapping appris `état → embedding` (ridge ✓).

    ⚠️ LA DÉGÉNÉRESCENCE PAR LE NOMBRE DE POSITIONS ✗✗. Un ridge à 896 coefficients ajusté sur MOINS de
    896 positions **interpole** : l'erreur tombe à ~0 % ✓ et la contre-épreuve aussi ✓ — donc **on ne
    mesure RIEN** ✓✗ (c'est ce qui est arrivé : « 0,0 (0,1) » partout ✓). C'est la deuxième fois de la
    soirée qu'une mesure se déguise en résultat ✓✓ (la première : la position avec elle-même ✓). La règle
    qui sauve : **exiger n > 3 × 896**, et l'écrire à côté du chiffre ✓."""
    assert H.shape[0] > 3 * H.shape[1], f"trop peu de positions : {H.shape[0]} pour {H.shape[1]} coefficients ✗"
    mh, me = H.mean(0), E.mean(0)
    Hc, Ec = H - mh, E - me
    W = np.linalg.solve(Hc.T @ Hc + 1e-3 * np.eye(Hc.shape[1]), Hc.T @ Ec)
    P = Hc @ W + me
    rel = 100 * float(np.linalg.norm(P - E) / np.linalg.norm(E))
    cos = float(np.mean(np.sum(P * E, axis=1) /
                        (np.linalg.norm(P, axis=1) * np.linalg.norm(E, axis=1) + 1e-12)))
    return rel, cos


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--lora", default="/tmp/lora-recopie.pt")
    ap.add_argument("--textes", type=int, default=8, help="nombre de textes jamais vus")
    ap.add_argument("--longueur", type=int, default=64)
    ap.add_argument("--horizons", default="0,1,4,16")
    ap.add_argument("--couches", default="8,16,23")
    ap.add_argument("--decalage", type=int, default=7, help="décalage de la CONTRE-ÉPREUVE ✗")
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(a.hf)
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    if pathlib.Path(a.lora).exists():
        d = torch.load(a.lora, map_location="cpu", weights_only=False)
        charger_lora(m, a.lora, d["rang"], d["alpha"])
        print(f"LoRA rechargé : recopie {d['recopie_apres']:.1f} % · contrôle {d['controle_apres']:.1f} % ✓")
    else:
        sys.exit(f"adaptateur absent : {a.lora} (lancer d'abord tools/lora_recopie.py)")
    emb = m.get_input_embeddings()
    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.ids).read_text()) if x.strip()]
    L = a.longueur
    couches = [int(x) for x in a.couches.split(",")]
    horizons = [int(x) for x in a.horizons.split(",")]

    # les états, couche par couche, dans les DEUX régimes
    copie_H = {Lc: [] for Lc in couches}; copie_E = []
    lecture_H = {Lc: [] for Lc in couches}; lecture_E = []
    exacts = []
    for t in range(a.textes):
        # ⚠️ PAS D'ALLER-RETOUR DÉCODAGE/RÉ-ENCODAGE ✗ : il peut rendre un texte VIDE (mesuré : le
        # générateur a reçu `max_new_tokens=0` ✓) et, même quand il réussit, il change les identifiants ✓.
        # La source EST la tranche d'identifiants ✓ ; le texte n'en est que la forme lisible ✓.
        # ⚠️ ET IL FAUT QUE LES TEXTES EXISTENT ✗ : le premier essai prenait `70 000 + t*5 000` ✓, or
        # le corpus fait 85 626 jetons ✓ — au-delà du 4ᵉ texte la tranche était VIDE ✓✗ (d'où « n=149 »
        # sur 24 textes demandés ✓). On avance par pas de 3 000 ✓, ce qui donne ~28 textes ✓ ET évite les
        # 21 tranches vues à l'entraînement (le LoRA a appris `i, i+4096, …` ✓ — aucun multiple de 3 000
        # ne tombe sur un multiple de 4 096 avant longtemps ✓).
        d = 1_000 + t * 3_000
        src = ids[d:d + L]
        txt = tok.decode(src)
        if len(src) < 8 or not txt.strip():
            continue
        inv = "Recopie exactement le texte suivant :\n" + txt + "\nRecopie :\n"
        b = tok(inv, return_tensors="pt").input_ids
        with torch.no_grad():
            g = m.generate(b, max_new_tokens=len(src), do_sample=False, pad_token_id=tok.eos_token_id)
            gen = g[0][b.shape[1]:]
        n_exact = 0
        for x, y in zip(gen.tolist(), src):          # src est une LISTE d identifiants (plus de .tolist())
            if x != y: break
            n_exact += 1
        exacts.append(100 * n_exact / len(src))
        # UNE passe avant sur invite + copie GÉNÉRÉE : les états des positions ÉMISES ✓
        seq = torch.cat([b[0], gen]).unsqueeze(0)
        with torch.no_grad():
            hs = m(seq, output_hidden_states=True).hidden_states
            E = emb(seq)[0][b.shape[1]:b.shape[1] + n_exact].numpy().astype(np.float64)
        for Lc in couches:
            copie_H[Lc].append(hs[Lc][0][b.shape[1]:b.shape[1] + n_exact].numpy().astype(np.float64))
        copie_E.append(E)
        # LE MÊME TEXTE, EN LECTURE (sans consigne de copie) ✓
        br = tok(txt, return_tensors="pt").input_ids
        with torch.no_grad():
            hsr = m(br, output_hidden_states=True).hidden_states
            Er = emb(br)[0][:n_exact].numpy().astype(np.float64)
        for Lc in couches:
            lecture_H[Lc].append(hsr[Lc][0][:n_exact].numpy().astype(np.float64))
        lecture_E.append(Er)

    tot = sum(x.shape[0] for x in copie_H[couches[0]]) if copie_H[couches[0]] else 0
    print(f"textes : {a.textes} · longueur {L} · recopie exacte moyenne {np.mean(exacts) if exacts else 0:.1f} %"
          f" · positions RÉELLEMENT récoltées : {tot} (détail : {[f'{e:.0f} %' for e in exacts]})")
    print()
    print("  L'EMPREINTE : écart relatif du mapping état(émis) → embedding du jeton source, par horizon k")
    print("  (contre-épreuve = même état, jeton source DÉCALÉ de %d ✗)" % a.decalage)
    print()
    print("   couche | régime  | " + " | ".join(f"k={k:<2} (contre)" for k in horizons))
    print("   -------|---------|" + "--------------|" * len(horizons))
    for Lc in couches:
        for regime, Hl, El in (("COPIE", copie_H[Lc], copie_E), ("lecture", lecture_H[Lc], lecture_E)):
            cellules = []
            for k in horizons:
                H = np.concatenate(Hl); E = np.concatenate(El)
                n = min(H.shape[0], E.shape[0]) - k - a.decalage
                # ⚠️ LE SEUIL COMPTE ✗ : un ridge de 896 coefficients sur 156 positions est SOUS-
                # DÉTERMINÉ (il apprendrait le bruit ✓). Il faut au moins ~300 positions ✓ — d'où
                # `--textes 20`, et le seuil à 300 ✓✓.
                if n <= 2688: cellules.append(f"   (n={n} < 2688)"); continue
                vrai = ajuster(H[:n], E[k:k + n])[0]
                faux = ajuster(H[:n], E[k + a.decalage:k + a.decalage + n])[0]
                cellules.append(f"{vrai:5.1f} ({faux:5.1f})")
            n_pos = sum(x.shape[0] for x in Hl)
            print(f"   {Lc:>6} | {regime:7s} | " + " | ".join(cellules)
                  + (f"   [positions : {n_pos}]" if regime == "COPIE" else ""))
    print()
    print("   lecture : dans chaque case, l'écart du VRAI alignement et, entre parenthèses, celui de la")
    print("   CONTRE-ÉPREUVE ✗. Un vrai nettement plus BAS que la contre-épreuve = l'état porte bien")
    print("   l'empreinte du jeton reproduit ✓✓ ; des deux valeurs proches = on ne mesure rien ✗✓.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

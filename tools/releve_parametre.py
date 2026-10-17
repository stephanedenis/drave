#!/usr/bin/env python3
"""releve_parametre.py — COMBIEN DE PARAMÈTRES POUR LA LANGUE DANS LE RELEVÉ ?

LE CONSTAT (chapitre 7, mesure 8). La langue est **illisible** dans l'état (50,2 % = le hasard ✓✓) mais elle
**pèse** dans le relevé (état → mots) : la diagonale (même langue) bat le croisé de **+8,7** (linéaire) à
**+19,5** (non linéaire) ✗. Un relevé par langue coûte `dim × dim` = **65 536** poids ✓ — plus qu'un adaptateur
de surface (32 768 ✓) ✗✓. D'où la question : **la langue, dans le relevé, est-elle une correction de rang
faible ?** ✓

CE QU'IL MESURE. Un relevé **partagé** `W0` (ajusté sur les deux langues ✓), puis pour chaque langue la
**meilleure correction de rang 1** de son relevance propre ✓ — `W_l ≈ W0 + u_l·v_lᵀ`, soit **512 poids** par
langue ✓✓ (2 × 256). On compare trois choses : le partagé (0 paramètre de langue ✗), le rang-1 (512 ✓), et le
relevé complet (65 536 ✗).

Si le rang-1 retrouve l'essentiel de l'écart ✓✓ → **la langue est un paramètre de rang 1** ✓✓, et le « relevé
paramétré » coûte quelques centaines de poids, pas des dizaines de milliers ✓.

Usage : python3 tools/releve_parametre.py --hf /tmp/jouet-mixte
"""
from __future__ import annotations
import argparse, pathlib, sys
import numpy as np, torch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from contenu_par_couche import lambda_cv

def ajuster(H, E, lam=None):
    mh, me = H.mean(0), E.mean(0)
    Hc, Ec = H - mh, E - me
    if lam is None:
        lam = lambda_cv(H, E)
    W = np.linalg.solve(Hc.T @ Hc + lam * np.eye(Hc.shape[1]), Hc.T @ Ec)
    return W, mh, me

def erreur(W, mh, me, H, E):
    P = (H - mh) @ W + me
    return 100 * float(np.linalg.norm(P - E) / np.linalg.norm(E))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="/tmp/jouet-mixte")
    ap.add_argument("--en", default="data/corpus_en.txt")
    ap.add_argument("--fr", default="data/corpus_fr.txt")
    ap.add_argument("--longueur", type=int, default=128)
    ap.add_argument("--fenetres", type=int, default=200)
    a = ap.parse_args()
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    L = m.config.num_hidden_layers

    def recolter(chemin):
        b = np.frombuffer(pathlib.Path(chemin).read_text(errors="ignore").encode("utf-8"), dtype=np.uint8).astype(np.int64)
        pas = max(a.longueur, len(b) // (a.fenetres + 2))
        S, T = [], []
        with torch.no_grad():
            for i in range(a.fenetres):
                d = i * pas
                if d + a.longueur + 1 >= len(b): break
                x = torch.tensor(b[d:d + a.longueur]).unsqueeze(0)
                hs = m(x, output_hidden_states=True).hidden_states
                S.append(m.model.norm(hs[L][0]).numpy().astype(np.float64))
                T.append(m.get_input_embeddings()(torch.tensor(b[d+1:d+a.longueur+1])).unsqueeze(0)[0].numpy().astype(np.float64))
        return np.concatenate(S), np.concatenate(T)

    S_en, T_en = recolter(a.en); S_fr, T_fr = recolter(a.fr)
    n = min(len(S_en), len(S_fr))
    # moitié entraînement / moitié test, dans chaque langue ✓
    def coupe(S, T):
        k = int(len(S) * 0.6); return S[:k], T[:k], S[k:], T[k:]
    Sen_tr, Ten_tr, Sen_te, Ten_te = coupe(S_en, T_en)
    Sfr_tr, Tfr_tr, Sfr_te, Tfr_te = coupe(S_fr, T_fr)
    ntr = min(len(Sen_tr), len(Sfr_tr))

    # 1. le relevé PARTAGÉ (aucun paramètre de langue ✗)
    W0, mh, me = ajuster(np.concatenate([Sen_tr[:ntr], Sfr_tr[:ntr]]),
                         np.concatenate([Ten_tr[:ntr], Tfr_tr[:ntr]]))
    p_en = erreur(W0, mh, me, Sen_te, Ten_te)
    p_fr = erreur(W0, mh, me, Sfr_te, Tfr_te)

    # 2. les relevés COMPLETS par langue (65 536 poids ✗)
    W_en, mh_en, me_en = ajuster(Sen_tr, Ten_tr)
    W_fr, mh_fr, me_fr = ajuster(Sfr_tr, Tfr_tr)
    f_en = erreur(W_en, mh_en, me_en, Sen_te, Ten_te)
    f_fr = erreur(W_fr, mh_fr, me_fr, Sfr_te, Tfr_te)

    # 3. le relevé partagé + une correction de RANG 1 par langue (512 poids ✓✓)
    def rang1(W_langue):
        R = W_langue - W0
        u, s, vt = np.linalg.svd(R, full_matrices=False)
        return np.outer(u[:, 0] * s[0], vt[0])

    W_en1 = W0 + rang1(W_en)
    W_fr1 = W0 + rang1(W_fr)
    r_en = erreur(W_en1, mh, me, Sen_te, Ten_te)
    r_fr = erreur(W_fr1, mh, me, Sfr_te, Tfr_te)

    print(f"  dernier étage ({L}) · {ntr} fenêtres par langue à l'entraînement\n")
    print("   relevé                          | paramètres de LANGUE | anglais | français")
    print("   --------------------------------|----------------------|---------|---------")
    print(f"   partagé (aucun ✗)               |            0         | {p_en:5.1f} % | {p_fr:5.1f} %")
    print(f"   partagé + RANG 1 par langue ✓   |          512 ✓       | {r_en:5.1f} % | {r_fr:5.1f} %")
    print(f"   complet par langue ✗            |       65 536         | {f_en:5.1f} % | {f_fr:5.1f} %")
    gain = lambda part, rg, full: 100 * (part - rg) / max(1e-9, part - full)
    print()
    print(f"  le rang 1 récupère {gain(p_en, r_en, f_en):5.1f} % de l'écart en anglais "
          f"et {gain(p_fr, r_fr, f_fr):5.1f} % en français")
    print()
    print("  lecture : si le rang 1 récupère l'essentiel ✓✓, la langue est un paramètre de RANG 1 dans le relevé")
    print("  — quelques centaines de poids, pas des dizaines de milliers ✓.")
    return 0

raise SystemExit(main())

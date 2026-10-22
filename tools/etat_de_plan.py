#!/usr/bin/env python3
"""etat_de_plan.py — ÉTAGE 2 : un état de CONTEXTE apprend-il la phrase suivante, là où l'état d'une phrase échoue ?

POURQUOI ✓✓. Les mesures 113-115 ont tranché : l'état d'une **phrase** ne porte pas la phrase suivante — ni le
linéaire (qui prédit la moyenne), ni le MLP contrastif (qui mémorise), même avec 1 323 transitions ✗✗. L'hypothèse de
la nouvelle phase : ce n'est pas l'**information** qui manque, c'est le **plan** — un état qui résume la série lue
jusqu'ici, et non la phrase courante.

CE QU'ON MESURE ✓✓, sur des séries de **8 phrases consécutives** (Verne FR, 3 B) :
  1. le **contexte** (moyenne des états lus) + une carte linéaire : retrouve-t-il la phrase suivante parmi les 8 de
     la série (hasard 12,5 %) ? ✓✓
  2. un **GRU** (état récurrent, 256) entraîné par InfoNCE sur les mêmes transitions : le contexte **appris** fait-il
     mieux que la phrase seule ? ✓✓
  3. les **baselines** : la phrase seule (mesure 113, au hasard) et le **contrôle négatif** (cibles mélangées) ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · contexte **au-dessus du hasard** → le plan est extractible des états ; l'architecture suivante est un état
    récurrent entraîné ✓✓ ;
  · contexte **au hasard** → les états figés ne portent pas le plan ; il faudra l'entraîner dans le modèle ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np
import torch
import torch.nn as nn


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def retrieval_8_pos(pred, cand, position):
    sims = np.einsum("nd,nkd->nk", norm(pred), norm(cand))
    return float(np.mean(np.argmax(sims, 1) == position))


def contenu_8(pred, cand):
    """8 candidats NON VUS d'autres séries, au même pas : hasard 12,5 %. Teste le contenu, pas la position."""
    justes = tot = 0
    for i in range(0, len(pred), 8):
        idx = list(range(i, min(i + 8, len(pred))))
        if len(idx) < 8:
            continue
        sims = norm(pred[idx]) @ norm(cand[idx]).T
        justes += int(np.sum(np.argmax(sims, 1) == np.arange(8))); tot += 8
    return justes / max(1, tot)


class Recurrent(nn.Module):
    def __init__(self, d, cache=256):
        super().__init__()
        self.gru = nn.GRU(d, cache, batch_first=True)
        self.sortie = nn.Linear(cache, d)

    def forward(self, x):
        h, _ = self.gru(x)
        return self.sortie(h)


def entrainer(X, C, cache, epochs, lr, graine, lot=64, tau=0.05):
    """X : (n, T, d) ; C : (n, T-1, d) ; à chaque pas t, prédire C[:, t] depuis X[:, :t+1]."""
    torch.manual_seed(graine)
    Xt = torch.from_numpy(X); Ct = torch.from_numpy(C)
    n, T, d = Xt.shape
    m = Recurrent(d, cache)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=1e-4)
    generateur = torch.Generator().manual_seed(graine)
    perte = torch.tensor(0.0)
    for _ in range(epochs):
        ordre = torch.randperm(n, generator=generateur)
        for deb in range(0, n, lot):
            idx = ordre[deb:deb + lot]
            h = m(Xt[idx])
            pred = h[:, :-1, :].reshape(-1, d)
            cible = Ct[idx].reshape(-1, d)
            logits = (torch.nn.functional.normalize(pred, dim=1) @ torch.nn.functional.normalize(cible, dim=1).T) / tau
            perte = torch.nn.functional.cross_entropy(logits, torch.arange(len(pred)))
            opt.zero_grad(); perte.backward(); opt.step()
    return m, float(perte.detach())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", required=True)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--par-serie", type=int, default=8)
    ap.add_argument("--cache", type=int, default=256)
    ap.add_argument("--epochs", type=int, default=80)
    ap.add_argument("--graines", type=int, default=2)
    ap.add_argument("--lot", type=int, default=64)
    a = ap.parse_args()
    z = np.load(a.etats, allow_pickle=False)
    couches = [int(c) for c in z["couches"]]
    E0 = z[f"L{couches[0]}"]
    n_lignes = E0.shape[0]
    n_phrases = n_lignes // 2
    T = a.par_serie
    n_series = n_phrases // T
    assert n_lignes % 2 == 0 and n_phrases % T == 0, (n_lignes, n_phrases, T)
    rng = np.random.default_rng(1234)
    cles = np.arange(n_series); rng.shuffle(cles)
    n_tr = int(0.7 * n_series)
    tr, te = cles[:n_tr], cles[n_tr:]
    res = []
    for L in couches:
        E = z[f"L{L}"].astype(np.float32)
        F = E[0::2]
        assert len(F) == n_phrases
        X = F.reshape(n_series, T, -1)
        moy = X[tr].mean((0, 1), keepdims=True)
        ect = X[tr].std((0, 1), keepdims=True) + 1e-6
        Z = (X - moy) / ect
        Xtr, Xte = Z[tr], Z[te]
        Ctr = Xtr[:, 1:, :]
        Cte_true = Xte[:, 1:, :]
        # --- contexte = moyenne des états lus ; carte linéaire (ridge) ---
        prefixe = np.cumsum(Xtr, 1) / np.arange(1, T + 1)[None, :, None]
        src = np.arange(n_tr * T).reshape(n_tr, T)[:, :-1].reshape(-1)
        cible = np.arange(n_tr * T).reshape(n_tr, T)[:, 1:].reshape(-1)
        A_ = np.hstack([prefixe.reshape(-1, Xtr.shape[2])[src], np.ones((len(src), 1), np.float32)])
        y_ = Xtr.reshape(-1, Xtr.shape[2])[cible]
        W = np.linalg.solve(A_.T @ A_ + 10.0 * np.eye(A_.shape[1], dtype=np.float32), A_.T @ y_)
        prefixe_te = np.cumsum(Xte, 1) / np.arange(1, T + 1)[None, :, None]
        src_te = np.arange(len(te) * T).reshape(len(te), T)[:, :-1].reshape(-1)
        pred_moy = (np.hstack([prefixe_te.reshape(-1, Xte.shape[2])[src_te], np.ones((len(src_te), 1), np.float32)]) @ W)
        pred_moy = pred_moy.reshape(len(te), T - 1, -1) * ect + moy   # retour à l'espace des états bruts
        ret_moy = [retrieval_8_pos(pred_moy[:, t, :], X[te], t + 1) for t in range(T - 1)]
        cont_moy = [contenu_8(pred_moy[:, t, :], X[te][:, t + 1]) for t in range(T - 1)]
        # --- GRU contrastif, et contrôle négatif (cibles mélangées) ---
        Cmel = Ctr.reshape(-1, Ctr.shape[2])[np.random.default_rng(99).permutation(n_tr * (T - 1))]
        Cmel = Cmel.reshape(n_tr, T - 1, -1).astype(np.float32)
        ret_gru, ret_neg, cont_gru, cont_neg = [], [], [], []
        for g in range(a.graines):
            m, perte = entrainer(Xtr, Ctr, a.cache, a.epochs, 1e-3, graine=1000 + g, lot=a.lot)
            with torch.no_grad():
                h = m(torch.from_numpy(Xte)).numpy() * ect + moy
            ret_gru.append([retrieval_8_pos(h[:, t, :], X[te], t + 1) for t in range(T - 1)])
            cont_gru.append([contenu_8(h[:, t, :], X[te][:, t + 1]) for t in range(T - 1)])
            mn, _ = entrainer(Xtr, Cmel, a.cache, a.epochs, 1e-3, graine=2000 + g, lot=a.lot)
            with torch.no_grad():
                hn = mn(torch.from_numpy(Xte)).numpy() * ect + moy
            ret_neg.append([retrieval_8_pos(hn[:, t, :], X[te], t + 1) for t in range(T - 1)])
            cont_neg.append([contenu_8(hn[:, t, :], X[te][:, t + 1]) for t in range(T - 1)])
        res.append({
            "couche": int(L),
            "moyenne_contexte": [round(x, 4) for x in ret_moy],
            "gru": [[round(x, 4) for x in r] for r in ret_gru],
            "gru_moyen": [round(float(np.mean([r[t] for r in ret_gru])), 4) for t in range(T - 1)],
            "negatif": [[round(x, 4) for x in r] for r in ret_neg],
            "negatif_moyen": [round(float(np.mean([r[t] for r in ret_neg])), 4) for t in range(T - 1)],
            "contenu_moyenne": [round(x, 4) for x in cont_moy],
            "contenu_gru_moyen": [round(float(np.mean([r[t] for r in cont_gru])), 4) for t in range(T - 1)],
            "contenu_negatif_moyen": [round(float(np.mean([r[t] for r in cont_neg])), 4) for t in range(T - 1)],
        })
        print(f"  L{L:<2} série: moyenne {res[-1]['moyenne_contexte']} · GRU {res[-1]['gru_moyen']} · "
              f"négatif {res[-1]['negatif_moyen']} | contenu: moyenne {res[-1]['contenu_moyenne']} · "
              f"GRU {res[-1]['contenu_gru_moyen']} (hasards {1 / T:.3f} / 0,125)")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({
        "etats": a.etats, "n_series": n_series, "n_series_train": len(tr), "n_series_test": len(te),
        "par_serie": T, "hasard": round(1.0 / T, 4), "graines": a.graines, "epochs": a.epochs,
        "resultats": res}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

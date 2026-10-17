#!/usr/bin/env python3
"""penser_sans_langue.py — LA PENSÉE ITÉRÉE EST-ELLE SANS LANGUE ?

LES DEUX MOITIÉS DE LA QUESTION, ET LEUR JONCTION.
  · chapitre 7 : l'état est **neutre** (un classifieur de langue y est au hasard ✓✓) ;
  · chapitre 5 : on peut **itérer** l'état (un opérateur appris, contractant ✓), mais le contenu ne tient
    qu'un pas ✗.
La jonction n'a jamais été mesurée ✗ : **itérer préserve-t-il la neutralité ?** Si un classifieur de langue
reste **au hasard** après k pas ✓✓, alors la pensée itérée est **sans langue** ✓✓✓ — c'est la propriété qu'un
« cerveau » doit avoir : *penser ne dépend pas de la langue où l'on parle* ✓.

CE QU'IL FAIT. Il entraîne le même opérateur que `operateur_pensee.py` (identité + petit MLP ✓, terme de
contenu ✓ et pénalité de contraction ✓) sur les états du modèle **bilingue** ✓, puis mesure, **pour k = 0, 1,
2, 4** : le **contenu** ✓ (état → embedding suivant ✓) et la **précision du classifieur de langue** ✓.
Le repère est le hasard (50 %) ✓ : si elle y reste, la langue n'est pas revenue ✓✓.

Usage : python3 tools/penser_sans_langue.py --hf /tmp/jouet-mixte
"""
from __future__ import annotations
import argparse, pathlib, sys
import numpy as np, torch, torch.nn as nn
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from contenu_par_couche import contenu


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="/tmp/jouet-mixte")
    ap.add_argument("--en", default="data/corpus_en.txt")
    ap.add_argument("--fr", default="data/corpus_fr.txt")
    ap.add_argument("--longueur", type=int, default=128)
    ap.add_argument("--fenetres", type=int, default=150)
    ap.add_argument("--pas", type=int, default=3000)
    ap.add_argument("--k-entrainement", type=int, default=0,
                    help="entraîner sur k pas TIRÉS entre 1 et cette valeur ✓ (la recette du 16/10 qui rend "
                         "l'itération plate ✓) — et voir si la neutralité de langue SURVIT ✗✓")
    a = ap.parse_args()
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    for p in m.parameters():
        p.requires_grad_(False)
    L = m.config.num_hidden_layers
    dim = m.config.hidden_size

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
                S.append(m.model.norm(hs[L][0]).numpy().astype(np.float32))
                T.append(m.get_input_embeddings()(torch.tensor(b[d+1:d+a.longueur+1])).unsqueeze(0)[0].numpy().astype(np.float32))
        return np.concatenate(S), np.concatenate(T)

    S_en, T_en = recolter(a.en); S_fr, T_fr = recolter(a.fr)
    n = min(len(S_en), len(S_fr))
    S = np.concatenate([S_en[:n], S_fr[:n]]); T = np.concatenate([T_en[:n], T_fr[:n]])
    y = np.concatenate([np.ones(n), -np.ones(n)]).astype(np.float32)
    print(f"  {L} étages · {n} fenêtres par langue · dimension {dim}")

    class Cellule(nn.Module):
        def __init__(self):
            super().__init__()
            self.f = nn.Sequential(nn.Linear(dim, 256), nn.GELU(), nn.Linear(256, dim))
        def forward(self, x):
            return x + self.f(x) * 0.1          # pas borné ✓ (leçon du 16/10)

    cel = Cellule().cuda()
    opt = torch.optim.AdamW(cel.parameters(), lr=1e-3)
    X = torch.tensor(S).cuda(); Y = torch.tensor(T).cuda()
    for pas in range(1, a.pas + 1):
        idx = torch.randperm(X.shape[0])[:512]
        z = X[idx]
        # ⚠️ ENTRAÎNER SUR k PAS, PAS SUR UN SEUL ✓ (leçon du 16/10 : sans cela, l'opérateur ne vaut que
        # pour un pas ✗). k est TIRÉ entre 1 et k_max, et le contenu porte sur C^k(x) ✓.
        kk = int(torch.randint(1, a.k_entrainement + 1, (1,)).item()) if a.k_entrainement else 1
        for _ in range(kk):
            z = cel(z)
        perte = ((z - Y[idx]) ** 2).mean()
        delta = torch.randn_like(X[idx]) * 1e-3
        lam = ((cel(X[idx] + delta) - z).norm(dim=-1) / delta.norm(dim=-1)).mean()
        perte = perte + 10.0 * torch.clamp(lam - 1.0, min=0.0) ** 2
        opt.zero_grad(); perte.backward(); opt.step()

    def classe_langue(Z):
        """Précision d'un classifieur linéaire de langue sur les états itérés ✓ (moitié test ✓)."""
        Zn = Z.cpu().numpy().astype(np.float64)
        n2 = Zn.shape[0] // 2
        mx = Zn[:n2].mean(0); Xc = Zn[:n2] - mx
        w = np.linalg.solve(Xc.T @ Xc + 10.0 * np.eye(Xc.shape[1]), Xc.T @ y[:n2])
        acc = 100 * float(np.mean(np.sign((Zn[n2:] - mx) @ w) == y[n2:]))
        return max(acc, 100 - acc)              # le signe est arbitraire ✗✓ (leçon du 17/10)

    print()
    print("   pas d'itération | contenu (état → mot suivant) | langue (hasard = 50 %)")
    print("   ----------------|-----------------------------|----------------------")
    with torch.no_grad():
        for k in (0, 1, 2, 3, 4, 8):
            # ⚠️ ON REPART DE L'ÉTAT D'ORIGINE À CHAQUE FOIS ✗✓. Mon premier essai faisait `Z = cel(Z)` en
            # accumulant ✓✗ : les lignes « k=2 » et « k=4 » ne montraient pas 2 et 4 pas, mais 2 et 3 ✓✗
            # (le label mentait, pas la mesure ✓). C'est la NEUVIÈME fois qu'un chiffre se déguise — et cette
            # fois c'était mon code de boucle ✓✓.
            Z = X.clone()
            for _ in range(k):
                Z = cel(Z)
            c = contenu(Z.cpu().numpy().astype(np.float64), T.astype(np.float64))
            print(f"   {k:>14} |            {c:5.1f} %          |   {classe_langue(Z):5.1f} %")
    print()
    print("  lecture : si la précision de langue reste autour de 50 % ✓✓, la PENSÉE ITÉRÉE EST SANS LANGUE ✓✓ —")
    print("  la propriété qu'on cherchait. Si elle monte ✗, l'itération fait revenir la langue.")
    return 0

raise SystemExit(main())

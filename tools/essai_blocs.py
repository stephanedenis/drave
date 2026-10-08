#!/usr/bin/env python3
"""essai_blocs.py — le régime où Drave a un avantage : gros modèle, peu lu.

POURQUOI CE BANC, APRÈS LE PREMIER. `tools/essai_decharge.py` a établi deux
choses, toutes deux mesurées :

  1. la parcimonie **s'entraîne** (R̂ = 0,17, réglable jusqu'à 0,03) — la
     question ouverte du programme de recherche est tranchée ;
  2. mais à 1,9 M paramètres, **tout tient dans le cache** : le pull dense lit
     ses poids à 14,0 Go/s (67 % de la bande passante mesurée) et le chemin par
     listes n'a structurellement rien à gagner. Un événement coûte même 2,9×
     (valué) à 4,3× (signé) un poids dense lu.

La conséquence est un changement de cible : l'avantage de Drave — **ne lire que
ce qui parle** — ne se manifeste que sur un modèle **plus gros que la mémoire**,
dont chaque jeton ne réveille qu'une petite fraction. C'est la leçon du disque
de Kimi-K3 (206,58 Gio lus pour 4 jetons, 87,6 % d'occupation disque).

CE QU'ON MESURE DONC ICI : pas des MACs, pas des événements — des **OCTETS LUS
PAR JETON**, et la qualité obtenue pour ces octets. La comparaison honnête n'est
pas « même nombre de paramètres » (le routé en aurait huit fois plus) mais
**même lecture** : un modèle routé qui lit k/E de ses experts se compare à un
dense **de la taille de ce qu'il lit**.

Le dispositif :
  * FFN dense (le jumeau) : `dim → cache → dim` ;
  * FFN routé : `E` experts de `cache_expert`, routeur linéaire, top-k par jeton,
    perte d'équilibrage — les jetons sont réellement regroupés par expert
    (dispatch par expert, pas de calcul masqué), donc le coût mesuré est le coût
    réel ;
  * option `--decharge` : l'intérieur de chaque expert devient discret
    (Heaviside après normalisation par lot), ce qui ajoute l'axe événementiel.

Usage :
    essai_blocs.py --dim 192 --couches 4 --cache 768 --experts 8 --k 2
    essai_blocs.py --dim 192 --couches 4 --cache 768 --experts 8 --k 2 --decharge
"""
import argparse
import math
import os
import sys
import time

import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from essai_decharge import (  # noqa: E402
    COUT_EV_NS, COUT_POIDS_NS, NormeLot, Rapport, charger, decharge, evaluer,
    lot_aleatoire,
)


# --------------------------------------------------------------------- FFN
# SwiGLU, PAS GELU — et ce n'est pas un détail de goût : c'est la forme que le
# moteur sait déjà exécuter (`a = silu(u·x) · (v·x)`, `drave-core/src/model.rs`
# § expert), avec les tenseurs `ffn_gate_exps` / `ffn_up_exps` / `ffn_down_exps`.
# Un modèle entraîné ici peut donc être exporté en GGUF et exécuté par Drave sans
# une ligne de noyau nouvelle — c'est la porte d'exécution de l'objectif.
def _swiglu(gate, up, x):
    return torch.nn.functional.silu(gate(x)) * up(x)


class FfnDense(nn.Module):
    """Le jumeau : SwiGLU ordinaire, rien de creux."""

    def __init__(self, d, cache):
        super().__init__()
        self.gate = nn.Linear(d, cache, bias=False)
        self.up = nn.Linear(d, cache, bias=False)
        self.down = nn.Linear(cache, d, bias=False)

    def forward(self, x, rap=None, nom=""):
        return self.down(_swiglu(self.gate, self.up, x))

    def poids(self):
        return (self.gate.weight.numel() + self.up.weight.numel()
                + self.down.weight.numel())


class FfnDecharge(nn.Module):
    """SwiGLU dont l'entrée de CHAQUE couche linéaire est discrète.

    L'ordre est celui de Spikingformer : le résiduel reste flottant, mais aucune
    couche linéaire ne reçoit autre chose qu'un train de décharges.
    """

    def __init__(self, d, cache, seuil=1.0):
        super().__init__()
        self.bn_in = NormeLot(d)
        self.gate = nn.Linear(d, cache, bias=False)
        self.up = nn.Linear(d, cache, bias=False)
        self.bn_h = NormeLot(cache)
        self.down = nn.Linear(cache, d, bias=False)
        self.seuil = seuil

    def forward(self, x, rap=None, nom=""):
        s = decharge(self.bn_in(x) - self.seuil)
        if rap is not None:
            rap.note(nom + ".in", s)
        m = decharge(self.bn_h(_swiglu(self.gate, self.up, s)) - self.seuil)
        if rap is not None:
            rap.note(nom + ".milieu", m)
        return self.down(m)

    def poids(self):
        return (self.gate.weight.numel() + self.up.weight.numel()
                + self.down.weight.numel())


class FfnRoutee(nn.Module):
    """E experts, k choisis par jeton — avec DISPATCH réel par expert.

    Le coût d'un modèle routé se lit dans ce qu'il LIT : k/E des poids d'experts
    par jeton. Encore faut-il que le calcul suive : les jetons sont regroupés par
    expert (`index_select`), l'expert ne calcule que sur eux, et le résultat est
    réaccumulé (`index_add_`). Un calcul « tous les experts sur tous les jetons,
    masqué ensuite » aurait le même résultat et un tout autre coût — il ne
    mesurerait rien.
    """

    def __init__(self, d, cache, n_experts, k, decharge=False, seuil=1.0):
        super().__init__()
        self.n_experts, self.k = n_experts, k
        self.routeur = nn.Linear(d, n_experts, bias=False)
        Fab = FfnDecharge if decharge else FfnDense
        self.experts = nn.ModuleList([Fab(d, cache, seuil) if decharge else Fab(d, cache)
                                      for _ in range(n_experts)])

    def forward(self, x, rap=None, nom=""):
        B, T, D = x.shape
        pr = self.routeur(x).softmax(-1)                  # (B,T,E)
        val, idx = pr.topk(self.k, dim=-1)                # (B,T,k)
        val = val / val.sum(-1, keepdim=True).clamp_min(1e-9)
        y = torch.zeros_like(x)
        xf = x.reshape(-1, D)
        idxf = idx.reshape(-1, self.k)
        valf = val.reshape(-1, self.k)
        yf = y.view(-1, D)
        for e in range(self.n_experts):
            sel = (idxf == e).any(dim=-1).nonzero().squeeze(-1)
            if sel.numel() == 0:
                continue
            poids = ((idxf[sel] == e).to(valf.dtype) * valf[sel]).sum(dim=-1, keepdim=True)
            yf.index_add_(0, sel, self.experts[e](xf.index_select(0, sel), rap,
                                                  f"{nom}.e{e}") * poids)
        # Perte d'équilibrage : sans elle, le routeur envoie tout au même expert
        # et le modèle routé devient un modèle dense mal calculé.
        f = torch.stack([(idxf == e).any(dim=-1).to(pr.dtype).mean()
                         for e in range(self.n_experts)])
        self.derniere_perte_eq = self.n_experts * (f * pr.mean(dim=(0, 1))).sum()
        return y

    def poids(self):
        return self.routeur.weight.numel() + self.n_experts * self.experts[0].poids()

    def poids_actifs(self):
        """Ce qu'un jeton LIT réellement : le routeur + k experts sur E."""
        return self.routeur.weight.numel() + self.k * self.experts[0].poids()


# -------------------------------------------------------------------- blocs
class Bloc(nn.Module):
    """Attention (identique dans les deux familles) + FFN au choix."""

    def __init__(self, d, tetes, ffn, decharge=False, seuil=1.0):
        super().__init__()
        self.dh = d // tetes
        self.tetes = tetes
        self.decharge = decharge
        self.seuil = seuil
        self.norme1 = NormeLot(d) if decharge else nn.LayerNorm(d)
        self.wq = nn.Linear(d, d, bias=False)
        self.wk = nn.Linear(d, d, bias=False)
        self.wv = nn.Linear(d, d, bias=False)
        self.wo = nn.Linear(d, d, bias=False)
        self.ffn = ffn
        if decharge:
            self.bn_o = NormeLot(d)

    def forward(self, x, masque, rap=None, nom=""):
        B, T, D = x.shape
        if self.decharge:
            s = decharge(self.norme1(x) - self.seuil)
            if rap is not None:
                rap.note(nom + ".in", s)
        else:
            s = self.norme1(x)
        q = self.wq(s).view(B, T, self.tetes, self.dh).transpose(1, 2)
        k = self.wk(s).view(B, T, self.tetes, self.dh).transpose(1, 2)
        v = self.wv(s).view(B, T, self.tetes, self.dh).transpose(1, 2)
        att = (q @ k.transpose(-1, -2)) / math.sqrt(self.dh)
        if self.decharge:
            att = att.masked_fill(masque, 0.0)
        else:
            att = att.masked_fill(masque, float("-inf")).softmax(-1)
        o = (att @ v).transpose(1, 2).reshape(B, T, D)
        if self.decharge:
            o = decharge(self.bn_o(o) - self.seuil)
            if rap is not None:
                rap.note(nom + ".o", o)
        x = x + self.wo(o)
        return x + self.ffn(x, rap, nom + ".ffn")

    def poids_attention(self):
        return (self.wq.weight.numel() + self.wk.weight.numel()
                + self.wv.weight.numel() + self.wo.weight.numel())


class Modele(nn.Module):
    def __init__(self, vocab, d, couches, tetes, cache, experts, k, decharge, seuil):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        blocs = []
        for _ in range(couches):
            if experts > 1:
                ffn = FfnRoutee(d, cache, experts, k, decharge, seuil)
            else:
                ffn = FfnDecharge(d, cache, seuil) if decharge else FfnDense(d, cache)
            blocs.append(Bloc(d, tetes, ffn, decharge, seuil))
        self.blocs = nn.ModuleList(blocs)
        self.norme_f = NormeLot(d) if decharge else nn.LayerNorm(d)
        self.tete = nn.Linear(d, vocab, bias=False)
        self.decharge = decharge

    def forward(self, idx, rap=None):
        B, T = idx.shape
        x = self.emb(idx)
        masque = torch.triu(torch.ones(T, T, dtype=torch.bool, device=idx.device), diagonal=1)
        for i, b in enumerate(self.blocs):
            x = b(x, masque, rap, nom=f"bloc{i}")
        return self.tete(self.norme_f(x))

    def perte_equilibrage(self):
        return sum(b.ffn.derniere_perte_eq for b in self.blocs
                   if hasattr(b.ffn, "derniere_perte_eq"))

    def poids(self):
        return sum(p.numel() for p in self.parameters())

    def poids_du_calcul(self):
        """Poids réellement traversés par un jeton, hors embedding et tête."""
        return sum(b.poids_attention() + b.ffn.poids_actifs()
                   if hasattr(b.ffn, "poids_actifs") else b.poids_attention() + b.ffn.poids()
                   for b in self.blocs)


# ---------------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--donnees", nargs="+", default=["data/corpus_en.txt"])
    p.add_argument("--validation", default="data/corpus_en_val.txt")
    p.add_argument("--dim", type=int, default=192)
    p.add_argument("--couches", type=int, default=4)
    p.add_argument("--tetes", type=int, default=4)
    p.add_argument("--cache", type=int, default=0, help="largeur du FFN dense (0 = 4 × dim)")
    p.add_argument("--cache-expert", type=int, default=0,
                   help="largeur d'un expert (0 = cache / k : lecture ÉGALE par défaut)")
    p.add_argument("--seul", choices=["dense", "route"], default=None)
    p.add_argument("--experts", type=int, default=8)
    p.add_argument("--k", type=int, default=2)
    p.add_argument("--decharge", action="store_true")
    p.add_argument("--seuil", type=float, default=1.0)
    p.add_argument("--seq", type=int, default=128)
    p.add_argument("--lot", type=int, default=32)
    p.add_argument("--pas", type=int, default=8000)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--graine", type=int, default=1)
    p.add_argument("--eval-tous", type=int, default=500)
    p.add_argument("--coef-equilibrage", type=float, default=0.01)
    p.add_argument("--sans-gpu", action="store_true")
    a = p.parse_args()
    cache = a.cache or 4 * a.dim
    # Par défaut, un jeton LIT la même chose dans les deux familles : k experts de
    # `cache_expert` valent le FFN dense de `cache`. C'est la seule comparaison
    # dont le résultat veut dire quelque chose — le routé stocke alors k/E fois
    # moins que ce qu'il possède.
    cache_expert = a.cache_expert or max(1, cache // max(1, a.k))

    torch.manual_seed(a.graine)
    dev = torch.device("cpu" if a.sans_gpu or not torch.cuda.is_available() else "cuda")
    train = charger(a.donnees)
    val = charger([a.validation])
    print(f"# corpus {len(train)} octets d'apprentissage · {len(val)} de validation · {dev}")

    # Deux familles, MÊME attention, même budget d'optimisation. Le dense a
    # `cache` par couche ; le routé a `experts` experts de `cache_expert` chacun
    # et n'en lit que `k` — soit, par défaut, la MÊME lecture par jeton.
    familles = [("dense", 1, cache), ("routé", a.experts, cache_expert)]
    if a.seul == "dense":
        familles = familles[:1]
    elif a.seul == "route":
        familles = familles[1:]
    resultats = {}
    for nom, experts, largeur in familles:
        torch.manual_seed(a.graine)
        g = torch.Generator().manual_seed(a.graine)
        modele = Modele(256, a.dim, a.couches, a.tetes, largeur, experts, a.k,
                        a.decharge, a.seuil).to(dev)
        opt = torch.optim.AdamW(modele.parameters(), lr=a.lr, weight_decay=0.01)
        print(f"\n=== {nom} · {modele.poids()} paramètres · "
              f"{modele.poids_du_calcul()} poids traversés par jeton · lr {a.lr} ===")
        debut = time.time()
        meilleur = (float("inf"), None, 0)
        for pas in range(1, a.pas + 1):
            x, y = lot_aleatoire(train, a.seq, a.lot, g)
            x, y = x.to(dev), y.to(dev)
            logits = modele(x)
            perte = nn.functional.cross_entropy(logits.reshape(-1, logits.shape[-1]), y.reshape(-1))
            if experts > 1:
                perte = perte + a.coef_equilibrage * modele.perte_equilibrage()
            opt.zero_grad(set_to_none=True)
            perte.backward()
            torch.nn.utils.clip_grad_norm_(modele.parameters(), 1.0)
            opt.step()
            if pas % a.eval_tous == 0 or pas == a.pas:
                bpc = evaluer(modele, val, a.seq, a.lot)
                if bpc < meilleur[0]:
                    meilleur = (bpc, {kk: v.detach().clone() for kk, v in modele.state_dict().items()}, pas)
                print(f"  pas {pas:>6} · perte {perte.item():.4f} · val {bpc:.4f} bits/octet "
                      f"· {time.time()-debut:.0f} s")
        modele.load_state_dict(meilleur[1])
        rap = Rapport()
        bpc = evaluer(modele, val, a.seq, a.lot, rap, max_lots=40)
        taux = rap.table()
        actifs = modele.poids_du_calcul()
        octets = actifs  # 1 octet par poids (Q8)
        print(f"\n  # meilleur point : pas {meilleur[2]} · val {bpc:.4f} bits/octet")
        print(f"  # paramètres {modele.poids()/1e6:.2f} M · traversés/jeton {actifs/1e6:.2f} M "
              f"· octets lus/jeton {octets/1e6:.2f} Mo (Q8) · {octets/4e6:.2f} Mo (2 bits)")
        if a.decharge and taux:
            rmoy = sum(taux.values()) / len(taux)
            poids_ffn = sum((b.ffn.poids_actifs() if hasattr(b.ffn, "poids_actifs")
                             else b.ffn.poids()) for b in modele.blocs)
            ev = rmoy * poids_ffn   # approximation assumée : taux moyen × poids du FFN
            print(f"  # R̂ moyen {rmoy:.4f} · {ev/1e6:.2f} M événements/jeton dans les FFN")
            print(f"  # temps MARGINAL du chemin par listes : "
                  f"{COUT_EV_NS[False]*1e-6*ev:.3f} ms contre "
                  f"{COUT_POIDS_NS*1e-6*actifs:.3f} ms au dense")
        resultats[nom] = (bpc, modele.poids(), actifs)
        del modele
        torch.cuda.empty_cache()

    if len(resultats) == 2:
        (bd, pd_, ad), (br, pr_, ar) = resultats["dense"], resultats["routé"]
        print("\n=== VERDICT (validation tenue à l'écart) ===")
        print(f"  dense : {pd_/1e6:>7.2f} M paramètres · {ad/1e6:>7.2f} M poids traversés "
              f"· {bd:.4f} bits/octet")
        print(f"  routé : {pr_/1e6:>7.2f} M paramètres · {ar/1e6:>7.2f} M poids traversés "
              f"· {br:.4f} bits/octet")
        print(f"  à lecture ÉGALE ({ad/1e6:.2f} M poids) : écart {br-bd:+.4f} bits/octet "
              f"pour {pr_/ad:.2f}× plus de paramètres stockés")
    return 0


if __name__ == "__main__":
    sys.exit(main())

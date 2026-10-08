#!/usr/bin/env python3
"""essai_decharge.py — la parcimonie ENTRAÎNÉE, mesurée contre un jumeau dense.

POURQUOI CE BANC. Le dépôt a mesuré deux choses qui se tiennent par la main :

  * un LLM dense n'a JAMAIS d'activation exactement nulle (**0,00 % de zéros**) :
    le débit est donc constant, et « on ne paie que ce qui s'active » reste une
    promesse théorique (`reports/rapport-parcimonie-imposee.md`) ;
  * imposer la parcimonie APRÈS l'entraînement plafonne à **−15 % d'événements
    pour +0,6 à +1,2 % de perplexité** — et le seuil absolu est pire encore
    (`reports/rapport-campagne-parcimonie.md`).

La conclusion était déjà écrite dans `docs/programme-recherche.md` §2 ter :
**« la parcimonie ne s'impose pas, elle s'entraîne »**. Ce script est le premier
essai de cette phrase — un modèle dont les activations sont discrètes **par
construction** (Heaviside après normalisation par lot), entraîné au **gradient de
substitution**, contre un jumeau **dense** de mêmes paramètres et de même budget.

CE QUI EST MESURÉ, ET POURQUOI CES GRANDEURS

  * **bits par octet** sur une validation tenue à l'écart — la qualité. Le corpus
    est lu en octets UTF-8 : 256 symboles, aucun alphabet à choisir, aucun
    caractère inconnu, et la mesure reste comparable d'un corpus à l'autre ;
  * **R̂**, la fraction d'unités actives, site par site — la parcimonie
    réellement obtenue, pas celle qu'on espère ;
  * **événements/token** contre **MACs/token**, puis le **temps** : la loi
    mesurée du dépôt dit qu'un événement n'est PAS un MAC. Sur
    `blk.0.ffn_gate.weight` (4,36 M poids, 16 threads), push/pull vaut 0,48 à
    10 % de densité, 1,11 à 25 % et **4,69 à 100 %** : le chemin par listes
    traite 4,69× moins d'opérations par seconde que le produit scalaire dense
    (`reports/rapport-croisement-push-pull.md`). Le coût en temps d'un modèle à
    densité d vaut donc `d × 4,69` en équivalents-MAC — c'est ce facteur qui
    ramène le « 6,7× moins d'événements » de SpikeGPT à ~1,5× de temps réel.

CE QUE CE N'EST PAS. Pas un modèle de production : un banc qui dit si la
parcimonie entraînée tient à notre échelle, à quel prix en qualité, et à quel
prix en TEMPS.

Usage :
    essai_decharge.py --dim 256 --pas 8000
    essai_decharge.py --decharge-seul --seuil 1.5     # balayer la densité
    essai_decharge.py --dim 256 --dense-seul --lr 3e-4
"""
import argparse
import glob
import math
import sys
import time

import numpy as np
import torch
import torch.nn as nn


# ------------------------------------------------------------------ décharge
class Substitut(torch.autograd.Function):
    """Heaviside franche en avant, sigmoïde rapide en arrière (α = 4).

    C'est la brique qui manquait au dépôt : sans elle, la décharge est un
    échelon de gradient nul partout, et rien ne s'entraîne. Le gradient de
    substitution est une approximation assumée — elle est ici mesurée, pas
    supposée : si le modèle ne descend pas, c'est elle qu'il faut accuser.
    """

    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return (x > 0).to(x.dtype)

    @staticmethod
    def backward(ctx, g):
        (x,) = ctx.saved_tensors
        return g * (4.0 / (1.0 + 4.0 * x.abs()) ** 2)


def decharge(x):
    return Substitut.apply(x)


# ---------------------------------------------------------------------------
# LA LOI DU COÛT, MESURÉE DANS LE MOTEUR (et pas déduite des documents).
#
# Banc du moteur, `blk.0.ffn_gate.weight` (4864 × 896 = 4,36 M poids, 16 fils,
# 20,8 Go/s de bande passante mesurée), binaire du 07/10 :
#
#   densité   pull dense   push valué (int8)   push signe (FusedSign)
#      1 %      0,312 ms       0,023 ms             0,032 ms
#      5 %      0,313 ms       0,060 ms             0,082 ms
#     10 %      0,312 ms       0,104 ms             0,142 ms
#     25 %      0,312 ms       0,240 ms             0,340 ms
#    100 %      0,311 ms       0,916 ms             1,322 ms
#
# Le pull est au mur mémoire (14,0 Go/s = 67 % du repère). Aux faibles densités
# les deux push sont linéaires en événements :
#   valué : (0,0137 ms + 0,210 ns × événements) par couche
#   signe : (0,0110 ms + 0,305 ns × événements) par couche
# soit **2,9× et 4,3× le coût d'un poids dense** (0,0716 ns). Deux conséquences
# que le dépôt n'avait pas : le croisement du chemin SIGNÉ est à ~9 % de densité
# (pas 22 %), et « 6,7× moins d'événements » ne vaut pas 6,7× de temps.
#
# Le push signé est aujourd'hui PLUS CHER par événement que le push valué, alors
# qu'il stocke 1 bit au lieu de 8 : c'est un défaut de noyau, pas une loi de la
# nature — `FusedSign` n'a pas reçu le traitement AVX2 du push int8. À mesurer
# avant de conclure quoi que ce soit sur les poids binaires.
COUT_POIDS_NS = 0.0716          # pull dense : ns par poids lu
COUT_EV_NS = {False: 0.210, True: 0.305}   # push : ns par événement poussé
COUT_FIXE_MS = {False: 0.0137, True: 0.0110}  # push : coût fixe par couche et appel
FACTEUR_PUSH = 4.69             # ancienne loi (documents), gardée pour comparaison


class NormeLot(nn.Module):
    """Normalisation par LOT sur toutes les dimensions sauf la dernière.

    Spikformer rapporte que la normalisation de couche « ne s'applique pas » aux
    réseaux à décharge. La raison est structurelle : c'est la statistique du lot
    qui place la pré-activation à moyenne 0 et écart 1, donc qui donne au seuil
    (1,0) le même sens d'une couche à l'autre. À l'initialisation, une gaussienne
    centrée réduite dépasse 1,0 dans **~15,9 %** de ses cas — c'est exactement le
    R̂ ≈ 0,15 de SpikeGPT, obtenu sans le poser à la main.
    """

    def __init__(self, d, moment=0.1):
        super().__init__()
        self.poids = nn.Parameter(torch.ones(d))
        self.biais = nn.Parameter(torch.zeros(d))
        self.register_buffer("moy", torch.zeros(d))
        self.register_buffer("var", torch.ones(d))
        self.moment = moment

    def forward(self, x):
        plat = x.reshape(-1, x.shape[-1])
        if self.training:
            m = plat.mean(dim=0)
            v = plat.var(dim=0, unbiased=False)
            with torch.no_grad():
                self.moy.mul_(1 - self.moment).add_(self.moment * m.detach())
                self.var.mul_(1 - self.moment).add_(self.moment * v.detach())
        else:
            m, v = self.moy, self.var
        return (x - m) / torch.sqrt(v + 1e-5) * self.poids + self.biais


class LineaireSignes(nn.Module):
    """Poids dans {−1, 0, +1} au calcul, f32 pour l'optimiseur (gradient droit).

    Ce que ça change n'est pas cosmétique. Avec une entrée **binaire** et un
    poids à trois états, le produit matriciel cesse d'être un produit : c'est une
    **accumulation conditionnelle** — « ajouter +1, ajouter −1, ou ne rien
    faire ». C'est exactement ce que le moteur sait faire en listes fusionnées
    (`FusedSign`, 1 bit par événement, `drave-core/src/list.rs:187`) et ce que la
    carte Stratix V faisait sans un seul multiplieur (`rapport-encodage.md`).
    Le nombre de bits de poids tombe à ~1,6 au lieu de 8.

    Le coût du push par SIGNE n'a jamais été chronométré dans le moteur : la loi
    `FACTEUR_PUSH = 4,69` a été mesurée sur des événements **valués** (int8), où
    chaque événement se décode et se multiplie. Tant que `FusedSign::accumulate`
    n'a pas son banc, le temps affiché ici reste celui du chemin valué — étiqueté
    comme tel, jamais présenté comme acquis.
    """

    def __init__(self, n_in, n_out, alpha=0.0):
        super().__init__()
        self.poids = nn.Parameter(torch.randn(n_out, n_in) * (1.0 / math.sqrt(n_in)))
        self.gamma = nn.Parameter(torch.ones(n_out))
        self.alpha = alpha

    @property
    def weight(self):
        return self.poids  # pour que plan_de_cout() et les comptes restent justes

    def forward(self, x):
        w = self.poids
        if self.alpha > 0.0:                      # ternaire : un seuil par ligne
            seuil = self.alpha * w.abs().amax(dim=1, keepdim=True)
            wq = torch.sign(w) * (w.abs() >= seuil)
        else:                                     # binaire : ±1 partout
            wq = torch.sign(w)
        wq = w + (wq - w).detach()                # gradient droit
        return torch.nn.functional.linear(x, wq) * self.gamma


def lineaire(n_in, n_out, signes, alpha):
    return LineaireSignes(n_in, n_out, alpha) if signes else nn.Linear(n_in, n_out, bias=False)


class Rapport:
    """Compte les unités actives par site, sans casser le graphe."""

    def __init__(self):
        self.sites = {}

    def note(self, nom, s):
        a = self.sites.setdefault(nom, [0.0, 0])
        a[0] += float(s.detach().mean())
        a[1] += 1

    def table(self):
        return {k: v[0] / max(v[1], 1) for k, v in self.sites.items()}

    def remise(self):
        for v in self.sites.values():
            v[0], v[1] = 0.0, 0


# -------------------------------------------------------------------- blocs
class BlocDecharge(nn.Module):
    """Un bloc où CHAQUE produit matriciel reçoit un vecteur DISCRET.

    L'ordre du résiduel est celui de **Spikingformer** : le flux résiduel reste
    flottant (ce ne sont que des additions), mais l'entrée de chaque couche
    linéaire est un train de décharges. C'est la contrainte qui fait que le coût
    suit l'activité : une unité silencieuse ne fait lire **aucun** poids.
    L'attention est sans softmax et décomposable (Spikformer) : Q, K, V sont des
    décharges, donc le score est un compte entier et le softmax disparaît.
    """

    def __init__(self, d, tetes, cache, seuil, signes=False, alpha=0.0):
        super().__init__()
        self.tetes, self.dh, self.seuil = tetes, d // tetes, seuil
        self.bn_in = NormeLot(d)
        self.wq = lineaire(d, d, signes, alpha)
        self.wk = lineaire(d, d, signes, alpha)
        self.wv = lineaire(d, d, signes, alpha)
        self.bn_q, self.bn_k, self.bn_v = NormeLot(self.dh), NormeLot(self.dh), NormeLot(self.dh)
        self.bn_o = NormeLot(d)
        self.wo = lineaire(d, d, signes, alpha)
        self.bn_mid = NormeLot(d)
        self.fc1 = lineaire(d, cache, signes, alpha)
        self.bn_fc1 = NormeLot(cache)
        self.fc2 = lineaire(cache, d, signes, alpha)

    def forward(self, x, masque, rap=None, nom=""):
        B, T, D = x.shape
        s = decharge(self.bn_in(x) - self.seuil)
        if rap is not None:
            rap.note(nom + ".in", s)
        q = decharge(self.bn_q(self.wq(s).view(B, T, self.tetes, self.dh)) - self.seuil)
        k = decharge(self.bn_k(self.wk(s).view(B, T, self.tetes, self.dh)) - self.seuil)
        v = decharge(self.bn_v(self.wv(s).view(B, T, self.tetes, self.dh)) - self.seuil)
        if rap is not None:
            rap.note(nom + ".q", q)
            rap.note(nom + ".k", k)
            rap.note(nom + ".v", v)
        att = torch.einsum("bthd,bshd->bhts", q, k) / math.sqrt(self.dh)
        att = att.masked_fill(masque, 0.0)
        o = torch.einsum("bhts,bshd->bthd", att, v).reshape(B, T, D)
        o = decharge(self.bn_o(o) - self.seuil)
        if rap is not None:
            rap.note(nom + ".o", o)
        x = x + self.wo(o)
        h = decharge(self.bn_mid(x) - self.seuil)
        if rap is not None:
            rap.note(nom + ".ffn_in", h)
        h2 = decharge(self.bn_fc1(self.fc1(h)) - self.seuil)
        if rap is not None:
            rap.note(nom + ".ffn_milieu", h2)
        return x + self.fc2(h2)


class BlocDense(nn.Module):
    """Le jumeau dense : mêmes formes, mêmes paramètres, calcul ordinaire."""

    def __init__(self, d, tetes, cache):
        super().__init__()
        self.tetes, self.dh = tetes, d // tetes
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.wq = nn.Linear(d, d, bias=False)
        self.wk = nn.Linear(d, d, bias=False)
        self.wv = nn.Linear(d, d, bias=False)
        self.wo = nn.Linear(d, d, bias=False)
        self.fc1 = nn.Linear(d, cache)
        self.fc2 = nn.Linear(cache, d)

    def forward(self, x, masque, rap=None, nom=""):
        B, T, D = x.shape
        y = self.ln1(x)
        q = self.wq(y).view(B, T, self.tetes, self.dh).transpose(1, 2)
        k = self.wk(y).view(B, T, self.tetes, self.dh).transpose(1, 2)
        v = self.wv(y).view(B, T, self.tetes, self.dh).transpose(1, 2)
        att = (q @ k.transpose(-1, -2)) / math.sqrt(self.dh)
        att = att.masked_fill(masque, float("-inf")).softmax(-1)
        o = (att @ v).transpose(1, 2).reshape(B, T, D)
        x = x + self.wo(o)
        return x + self.fc2(torch.nn.functional.gelu(self.fc1(self.ln2(x))))


class Modele(nn.Module):
    def __init__(self, vocab, d, couches, tetes, cache, seuil, dense=False,
                 signes=False, alpha=0.0):
        super().__init__()
        self.dense = dense
        self.signes = signes and not dense
        self.emb = nn.Embedding(vocab, d)
        if dense:
            self.blocs = nn.ModuleList([BlocDense(d, tetes, cache) for _ in range(couches)])
            self.ln_f = nn.LayerNorm(d)
        else:
            self.blocs = nn.ModuleList([BlocDecharge(d, tetes, cache, seuil, signes, alpha)
                                        for _ in range(couches)])
            self.bn_f = NormeLot(d)
        # La tête reste dense : elle est petite (d × vocab), et la quantifier
        # aux signes coûterait plus en qualité qu'elle ne rapporte en octets.
        self.tete = nn.Linear(d, vocab, bias=False)

    def forward(self, idx, rap=None):
        B, T = idx.shape
        x = self.emb(idx)
        masque = torch.triu(torch.ones(T, T, dtype=torch.bool, device=idx.device), diagonal=1)
        for i, b in enumerate(self.blocs):
            x = b(x, masque, rap, nom=f"bloc{i}")
        x = self.ln_f(x) if self.dense else self.bn_f(x)
        return self.tete(x)

    def nb_poids(self):
        return sum(p.numel() for p in self.parameters())

    def plan_de_cout(self):
        """[(clé de taux d'entrée, nombre de poids)] — le coût suit l'entrée.

        Pour une couche linéaire à entrée discrète de taux r, le nombre
        d'accumulations vaut `r × nb_poids` : chaque poids n'est lu que par les
        unités actives qui le traversent. Le plan dit donc, site par site, ce
        qu'on paiera au jeton.
        """
        plan = []
        for i, b in enumerate(self.blocs):
            if self.dense:
                plan += [(None, b.wq.weight.numel()), (None, b.wk.weight.numel()),
                         (None, b.wv.weight.numel()), (None, b.wo.weight.numel()),
                         (None, b.fc1.weight.numel()), (None, b.fc2.weight.numel())]
            else:
                plan += [(f"bloc{i}.in", b.wq.weight.numel()), (f"bloc{i}.in", b.wk.weight.numel()),
                         (f"bloc{i}.in", b.wv.weight.numel()), (f"bloc{i}.o", b.wo.weight.numel()),
                         (f"bloc{i}.ffn_in", b.fc1.weight.numel()),
                         (f"bloc{i}.ffn_milieu", b.fc2.weight.numel())]
        return plan


# -------------------------------------------------------------------- données
def charger(chemins):
    """Octets UTF-8 — 256 symboles, aucun alphabet à choisir.

    Lire en octets plutôt qu'en caractères n'est pas un détail : le corpus
    Wikipedia complet porte 3 237 caractères distincts, donc un embedding de
    3 237 entrées coûterait plus cher que le reste du modèle, et une découpe en
    « caractères » ferait dépendre la mesure du corpus choisi. En octets, la
    mesure (bits par octet) est comparable partout.
    """
    morceaux = []
    for c in chemins:
        for f in sorted(glob.glob(c)):
            with open(f, "rb") as fh:
                morceaux.append(fh.read())
    if not morceaux:
        sys.exit(f"aucun fichier pour {chemins}")
    return np.frombuffer(b"".join(morceaux), dtype=np.uint8)


def lot_aleatoire(ids, seq, lot, generateur):
    i = torch.randint(0, len(ids) - seq - 1, (lot,), generator=generateur).numpy()
    return (torch.from_numpy(np.stack([ids[j:j + seq] for j in i]).astype(np.int64)),
            torch.from_numpy(np.stack([ids[j + 1:j + seq + 1] for j in i]).astype(np.int64)))


def lots_valides(ids, seq, lot):
    """Validation par fenêtres contiguës — jamais de recouvrement."""
    n = (len(ids) - 1) // seq
    for k in range(0, max(0, n - lot + 1), lot):
        x = np.stack([ids[(k + j) * seq:(k + j) * seq + seq] for j in range(lot)])
        y = np.stack([ids[(k + j) * seq + 1:(k + j) * seq + seq + 1] for j in range(lot)])
        yield torch.from_numpy(x.astype(np.int64)), torch.from_numpy(y.astype(np.int64))


@torch.no_grad()
def evaluer(modele, ids, seq, lot, rap=None, max_lots=20):
    modele.eval()
    dev = next(modele.parameters()).device
    perte, n = 0.0, 0
    for k, (x, y) in enumerate(lots_valides(ids, seq, lot)):
        x, y = x.to(dev), y.to(dev)
        logits = modele(x, rap)
        perte += nn.functional.cross_entropy(
            logits.reshape(-1, logits.shape[-1]), y.reshape(-1), reduction="sum").item()
        n += y.numel()
        if k + 1 >= max_lots:
            break
    modele.train()
    return perte / max(n, 1) / math.log(2.0)  # bits par octet


# ---------------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--donnees", nargs="+", default=["data/corpus_en.txt"])
    p.add_argument("--validation", default="data/corpus_en_val.txt")
    p.add_argument("--val-fraction", type=float, default=0.0,
                   help="si > 0 et --validation absent : découpe les données")

    p.add_argument("--dim", type=int, default=192)
    p.add_argument("--couches", type=int, default=4)
    p.add_argument("--tetes", type=int, default=4)
    p.add_argument("--cache", type=int, default=0, help="0 = 4 × dim")
    p.add_argument("--seuil", type=float, default=1.0)
    p.add_argument("--poids-signes", action="store_true",
                   help="poids dans {−1,0,+1} : le produit devient une accumulation")
    p.add_argument("--alpha", type=float, default=0.0,
                   help="seuil ternaire (fraction du max par ligne) ; 0 = binaire")
    p.add_argument("--seq", type=int, default=128)
    p.add_argument("--lot", type=int, default=32)
    p.add_argument("--pas", type=int, default=8000)
    p.add_argument("--lr", type=float, default=3e-3)
    p.add_argument("--graine", type=int, default=1)
    p.add_argument("--eval-tous", type=int, default=500)
    p.add_argument("--dense-seul", action="store_true")
    p.add_argument("--decharge-seul", action="store_true")
    p.add_argument("--sans-gpu", action="store_true")
    a = p.parse_args()
    if a.dense_seul and a.decharge_seul:
        p.error("--dense-seul et --decharge-seul s'excluent")
    cache = a.cache or 4 * a.dim

    torch.manual_seed(a.graine)
    dev = torch.device("cpu" if a.sans_gpu or not torch.cuda.is_available() else "cuda")
    train = charger(a.donnees)
    if a.validation and glob.glob(a.validation):
        val = charger([a.validation])
    else:
        coupe = int(len(train) * (1.0 - a.val_fraction))
        train, val = train[:coupe], train[coupe:]
    print(f"# corpus {len(train)} octets d'apprentissage · {len(val)} de validation "
          f"· appareil {dev}")

    resultats = {}
    variantes = [True] if a.dense_seul else ([False] if a.decharge_seul else [False, True])
    for dense in variantes:
        nom = "dense" if dense else "décharge"
        torch.manual_seed(a.graine)  # mêmes poids initiaux, même tirage
        g = torch.Generator().manual_seed(a.graine)
        modele = Modele(256, a.dim, a.couches, a.tetes, cache, a.seuil, dense,
                        a.poids_signes, a.alpha).to(dev)
        opt = torch.optim.AdamW(modele.parameters(), lr=a.lr, weight_decay=0.01)
        plan = modele.plan_de_cout()
        etiquette = ""
        if not dense and a.poids_signes:
            etiquette = (" · poids " + ("ternaires α=%.2f" % a.alpha if a.alpha > 0 else "binaires")
                         + " (accumulation seule)")
        print(f"\n=== {nom} · {modele.nb_poids()} paramètres · "
              f"{sum(n for _, n in plan)} poids dans les couches linéaires · lr {a.lr}{etiquette} ===")
        debut = time.time()
        meilleur = (float("inf"), None, 0)
        for pas in range(1, a.pas + 1):
            x, y = lot_aleatoire(train, a.seq, a.lot, g)
            x, y = x.to(dev), y.to(dev)
            logits = modele(x)
            perte = nn.functional.cross_entropy(logits.reshape(-1, logits.shape[-1]), y.reshape(-1))
            opt.zero_grad(set_to_none=True)
            perte.backward()
            torch.nn.utils.clip_grad_norm_(modele.parameters(), 1.0)
            opt.step()
            if pas % a.eval_tous == 0 or pas == a.pas:
                bpc = evaluer(modele, val, a.seq, a.lot)
                # On garde le MEILLEUR point de validation : comparer deux
                # modèles au pas final mesurerait la vitesse de surapprentissage.
                if bpc < meilleur[0]:
                    meilleur = (bpc, {k: v.detach().clone() for k, v in modele.state_dict().items()}, pas)
                print(f"  pas {pas:>6} · perte {perte.item():.4f} · val {bpc:.4f} bits/octet "
                      f"· {time.time()-debut:.0f} s")
        if meilleur[1] is not None:
            modele.load_state_dict(meilleur[1])
            print(f"  # meilleur point : pas {meilleur[2]} · val {meilleur[0]:.4f} bits/octet")
        rap = Rapport()
        bpc = evaluer(modele, val, a.seq, a.lot, rap, max_lots=40)
        taux = rap.table()
        poids_lineaires = sum(n for _, n in plan)
        # Temps projeté, couche par couche, avec la loi mesurée dans le moteur
        # (coût fixe + coût par événement pour le push ; coût par poids pour le
        # pull dense). On ne compare pas des événements à des MACs : on compare
        # des millisecondes.
        temps_dense = COUT_POIDS_NS * 1e-6 * poids_lineaires
        if dense:
            cout, densite = poids_lineaires, 1.0
            print(f"\n  # MACs/token {cout/1e6:.2f} M · val {bpc:.4f} bits/octet")
            print(f"  # temps projeté {temps_dense:.3f} ms/token de poids linéaires "
                  f"(le pull est au mur mémoire mesuré)")
        else:
            cout = sum(taux.get(cle, 0.0) * n for cle, n in plan)
            rmoy = sum(taux.values()) / max(len(taux), 1)
            densite = cout / poids_lineaires
            signes = bool(a.poids_signes)
            # Coût MARGINAL seul : le coût fixe par appel (0,011 à 0,014 ms sur une
            # matrice de 4 864 × 896) dépend de la taille de l'accumulateur et du
            # nombre d'appels ; il n'est pas extrapolable couche par couche sans
            # mensonge. On le dit au lieu de l'inclure.
            temps_push = sum(COUT_EV_NS[signes] * 1e-6 * taux.get(cle, 0.0) * n
                             for cle, n in plan)
            print(f"\n  # événements/token {cout/1e6:.2f} M · R̂ moyen {rmoy:.4f} "
                  f"· densité {densite:.4f} · val {bpc:.4f} bits/octet")
            print(f"  # temps MARGINAL projeté ({COUT_EV_NS[signes]:.3f} ns/événement"
                  f"{', poids signés' if signes else ', événements valués'}) : "
                  f"{temps_push:.3f} ms contre {temps_dense:.3f} ms au dense "
                  f"→ {temps_push/temps_dense:.3f}× ({temps_dense/temps_push:.2f}× plus rapide)")
            print(f"  #   hors coût fixe par appel (~0,011-0,014 ms sur 4 864 × 896, "
                  f"non extrapolable)")
            for k in sorted(taux):
                print(f"  #   {k:<18} R̂ {taux[k]:.4f}")
        resultats[nom] = (bpc, cout, modele.nb_poids(), cout / poids_lineaires)

    if len(resultats) == 2:
        (bd, cd, pd_, dd), (bp, cp, pp, dp) = resultats["dense"], resultats["décharge"]
        print("\n=== VERDICT (validation tenue à l'écart) ===")
        print(f"  dense    : {pd_:>9} paramètres · {bd:.4f} bits/octet · {cd/1e6:>7.2f} M MACs/token")
        print(f"  décharge : {pp:>9} paramètres · {bp:.4f} bits/octet · {cp/1e6:>7.2f} M événements/token")
        print(f"  rapport de coût (événements/MACs) {cp/cd:.3f} · écart de qualité {bp-bd:+.3f} bits/octet")
        print(f"  (loi du coût mesurée dans le moteur : pull 0,0716 ns/poids · "
              f"push 0,210 ns/événement valué · 0,305 ns/événement signé)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

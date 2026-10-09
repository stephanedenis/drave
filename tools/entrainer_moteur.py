#!/usr/bin/env python3
"""entrainer_moteur.py — entraîner un modèle que DRAVE SAIT EXÉCUTER.

POURQUOI CE SCRIPT APRÈS LES BANCS. `essai_decharge.py` et `essai_blocs.py` ont
mesuré la qualité et le coût des deux familles, mais dans des architectures
« de banc » (LayerNorm, pas de RoPE, pas de GQA) que le moteur ne sait pas
exécuter. Ici, l'architecture est celle du moteur — Qwen3 dense ou Qwen3-MoE :
RMSNorm, RoPE « neox », GQA, SwiGLU — donc le modèle entraîné est exportable
(`tools/exporter_gguf.py`) et sa porte d'exécution se vérifie
(`tools/porte_moteur.py` + `compare_logits.py --porte`).

LE POINT DE LA COMPARAISON : À LECTURE ÉGALE. Un jeton ne lit ni le même nombre
de paramètres ni les mêmes octets selon la famille. Le jumeau dense est donc
dimensionné pour LIRE autant que le routé : `intermediate = k × moe_intermediate`.
Le routé stocke alors `E/k` fois plus de poids qu'il n'en lit — c'est tout son
intérêt, et c'est ce que la mesure doit départager.

Usage :
    entrainer_moteur.py --famille route --dim 192 --couches 4 --experts 8 --k 2 \
        --cache 384 --pas 20000 --sortie /tmp/modele_route
    entrainer_moteur.py --famille dense --dim 192 --couches 4 --cache 768 \
        --pas 20000 --sortie /tmp/modele_dense
"""
import argparse
import math
import os
import sys
import time

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from essai_decharge import charger, lot_aleatoire  # noqa: E402


def construire(famille, a):
    from transformers import Qwen3Config, Qwen3ForCausalLM, Qwen3MoeConfig, Qwen3MoeForCausalLM
    commun = dict(vocab_size=256, hidden_size=a.dim, num_hidden_layers=a.couches,
                  num_attention_heads=a.tetes, num_key_value_heads=max(1, a.tetes // 2),
                  max_position_embeddings=a.seq * 4, rms_norm_eps=1e-6,
                  tie_word_embeddings=True,
                  # `head_dim` DOIT être posé : `Qwen3Config` en a un défaut de 128,
                  # indépendant de `hidden_size`, alors que `Qwen3MoeConfig` prend
                  # `hidden // têtes`. Sans cette ligne, les deux familles
                  # n'avaient pas la même attention du tout — le jumeau dense
                  # lisait 1,2 M poids d'attention contre 0,4 M pour le routé, et
                  # la comparaison « à lecture égale » ne comparait rien.
                  head_dim=a.dim // a.tetes,
                  # `initializer_range` : le défaut de HuggingFace (0,02) est
                  # calibré pour des modèles de plusieurs centaines de millions
                  # de paramètres. À 2 M, il laisse les logits si proches de zéro
                  # que le softmax part uniforme et que l'apprentissage rampe
                  # (mesuré : 7,4 bits/octet après 20 000 pas, contre 2,2 pour le
                  # même modèle initialisé à la main par les bancs). Ce n'est pas
                  # un détail de goût, c'est ce qui rend la comparaison valide.
                  initializer_range=a.init,
                  rope_parameters={"rope_theta": 10000.0, "rope_type": "default"})
    if famille == "dense":
        cfg = Qwen3Config(intermediate_size=a.cache, **commun)
        return Qwen3ForCausalLM(cfg), cfg
    cfg = Qwen3MoeConfig(intermediate_size=a.cache, moe_intermediate_size=a.cache_perle,
                         num_experts=a.experts, num_experts_per_tok=a.k,
                         norm_topk_prob=True, **commun)
    return Qwen3MoeForCausalLM(cfg), cfg


def installer_kwta(modele, fraction, cibles=None):
    """Entraîne le modèle À VIVRE CREUX : k-WTA sur l'entrée des projections de
    sortie (celle de l'attention, celle de la FFN).

    POURQUOI À L'ENTRAÎNEMENT ET PAS À L'EXÉCUTION. Le moteur sait déjà imposer
    un top-k sur les activations (`--act-topk`, `--topk-o`, `--topk-down`), et la
    campagne a mesuré ce que cela coûte sur un modèle qui n'a jamais appris à
    l'être : **+4 % de perplexité pour −30 % d'événements** au mieux (k-WTA 70 %),
    +63 % à 50 % (§ 19 du rapport). Un modèle DENSE reste dense : la parcimonie
    imposée ne fait que dégrader. Ici, on applique EXACTEMENT la même opération
    pendant l'apprentissage — garder les k plus grandes magnitudes, annuler le
    reste — pour que le modèle apprenne une représentation qui survit à la
    coupure. C'est la seule façon de savoir si l'architecture événementielle a
    un avenir sur un modèle dense, ou seulement sur un MoE.

    `fraction` = part GARDÉE (0,25 = on garde 25 %, on annule 75 %).

    PAR DÉFAUT, TOUTES LES PROJECTIONS. Le moteur a un top-k GLOBAL (`--act-topk`)
    qui s'applique à l'entrée de chaque matvec ; entraîner sur un sous-ensemble et
    évaluer avec le réglage global mesurerait deux modèles différents. On couvre
    donc toutes les couches linéaires, comme le fait le moteur.
    """
    k = {"n": 0}

    def fabrique(f):
        def h(mod, entree):
            x = entree[0]
            garde = max(1, int(round(f * x.shape[-1])))
            idx = x.abs().topk(garde, dim=-1).indices
            masque = torch.zeros_like(x).scatter_(-1, idx, 1.0)
            k["n"] += 1
            return (x * masque,) + tuple(entree[1:])
        return h

    n = 0
    for nom, mod in modele.named_modules():
        if isinstance(mod, nn.Linear) and (cibles is None or nom.endswith(cibles)):
            mod.register_forward_pre_hook(fabrique(fraction))
            n += 1
    print(f"# k-WTA à l'entraînement : {fraction:.0%} gardés sur {n} projections "
          f"(toutes les couches linéaires, comme `--act-topk` du moteur)")
    return n


class PoidsLogNormaux(nn.Module):
    """`w = signe_inné · e^{theta}` — log-normale par construction, signes FIXÉS.

    POURQUOI (docs/biologie-pour-drave.md § 3 ter). Les efficacités synaptiques
    corticales sont log-normales sur plusieurs ordres de grandeur ; nos modèles sont
    quasi gaussiens (p99,9/médiane 5,2), d'où un élagage gratuit à 50 % et fatal à
    25 %. Une distribution multiplicative est élagable par construction.

    ET POURQUOI LES SIGNES SONT FIXÉS : en biologie, un neurone est excitateur OU
    inhibiteur — son signe ne change pas (principe de Dale). Le figer à la naissance
    est donc fidèle *et* numériquement nécessaire : une reparamétrisation qui
    déduirait le signe de `theta` ne peut pas représenter un petit poids positif
    (|w| = e^{theta} ≥ 1 dès que theta > 0), et l'entraînement diverge — mesuré,
    perte 12 137 après 400 pas.

    `theta` est la log-magnitude, apprise ; `signes` est un tampon figé.
    """

    def __init__(self, signes):
        super().__init__()
        self.register_buffer("signes", signes)

    def forward(self, theta):
        # Borne douce : e^{theta} sans borne laisse un pas d'AdamW multiplier un
        # poids par e^{0,3} ≈ 1,35 ; au-delà de ±12 nats on est déjà à 1,6×10^5.
        return self.signes * theta.clamp(-12.0, 6.0).exp()


def installer_poids_lognormaux(modele):
    """θ = log|w| appris, signes figés à la naissance (principe de Dale)."""
    from torch.nn.utils.parametrize import register_parametrization
    n = 0
    for mod in modele.modules():
        if isinstance(mod, nn.Linear):
            with torch.no_grad():
                w = mod.weight
                signes = w.sign().clone()
                theta0 = w.abs().clamp(min=1e-6).log()
            register_parametrization(mod, "weight", PoidsLogNormaux(signes))
            with torch.no_grad():
                mod.parametrizations.weight.original.copy_(theta0)
            n += 1
    return n


def materialiser_poids(modele):
    """Écrit les poids DÉFINITIFS, puis retire la reparamétrisation.

    POURQUOI LA COPIE EST EXPLICITE (défaut trouvé le 9/10). Le premier essai se
    contentait de `remove_parametrizations` : le fichier sauvé portait alors des
    poids qui ne reproduisaient PAS le modèle entraîné — validation 2,2662 bits/octet
    à l'entraînement, perplexité 8 668 dans le moteur et **15 552** pour la référence
    PyTorch sur les mêmes poids quantifiés (donc le fichier, pas le moteur). On
    recalcule donc la valeur exacte du `forward` — `signes · clamp(theta, −12, 6).exp()`
    — et on l'écrit AVANT de retirer la reparamétrisation, en le VÉRIFIANT.
    """
    from torch.nn.utils.parametrize import remove_parametrizations
    n, ecart = 0, 0.0
    with torch.no_grad():
        for mod in modele.modules():
            if hasattr(mod, "parametrizations") and hasattr(mod.parametrizations, "weight"):
                par = mod.parametrizations.weight
                theta = par.original
                signes = par[0].signes
                attendu = signes * theta.clamp(-12.0, 6.0).exp()
                ecart = max(ecart, float((mod.weight - attendu).abs().max()))
                mod.weight.copy_(attendu)
                remove_parametrizations(mod, "weight")
                n += 1
    print(f"# matérialisation : {n} couches · écart max avant copie {ecart:.3e} "
          f"(0 = la reparamétrisation était déjà cohérente)")
    return n


def elaguer_lignes(modele, garde):
    """Élagage par MAGNITUDE, par LIGNE de sortie — la règle exacte de `--keep`.

    POURQUOI LES DEUX AXES. Le coût de Drave est un nombre de PAIRES (poids non nul
    × activation vivante) : la sparsité d'activation divise ce nombre, la sparsité
    de POIDS le divise aussi, et les deux se multiplient — mesuré le 9/10 sur
    `m8_d512_kwta25` : 100 %/100 % = 1 586 M paires, 25 %/100 % = 399 M,
    25 %/50 % = 201 M, soit ÷7,9 pour la combinaison. À 50 % de poids gardés la
    perplexité ne bouge pas (3,9139 contre 3,9152) ; à 25 % elle s'effondre.

    Ici on l'APPREND au lieu de l'imposer : le modèle s'adapte aux poids qui
    restent. La règle est copiée de `model.rs::prune_rows` — garder les k plus
    grandes magnitudes de chaque ligne — pour que l'entraînement et l'exécution
    parlent du même modèle.
    """
    n = 0
    with torch.no_grad():
        for mod in modele.modules():
            if isinstance(mod, nn.Linear):
                w = mod.weight
                k = max(1, int(round(garde * w.shape[1])))
                idx = w.abs().topk(k, dim=1).indices
                w.mul_(torch.zeros_like(w).scatter_(1, idx, 1.0))
                n += 1
    return n


def installer_masque_inne(modele, garde, graine):
    """Un CONNECTOME INNÉ : masque de connexions tiré UNE fois, puis jamais modifié.

    POURQUOI CETTE EXPÉRIENCE (docs/biologie-pour-drave.md, § 4). Le cerveau a un
    plan de câblage largement partagé entre individus, très creux (~10 % de
    probabilité de connexion, ~7 000 synapses par neurone) et dont seuls les POIDS
    changent avec l'apprentissage. Si la structure peut être fixée à la naissance,
    alors le coût d'exécution d'un modèle est **borné à la compilation** — le
    nombre de paires par jeton est connu avant le premier pas d'entraînement — et
    l'architecture événementielle n'a plus besoin d'un top-k à l'exécution, ni de la
    fragilité qui va avec (« exécuter au taux appris, sinon le modèle se dégrade »,
    § 5 ter de la campagne).

    Ce n'est PAS de l'élagage : on ne retire pas des poids devenus petits, on
    interdit des connexions dès le départ, et le tirage est aléatoire — c'est le
    point : si un masque ALÉATOIRE fixe suffit, alors la structure n'a pas besoin
    d'être apprise ; sinon, il faudra apprendre *où* sont les connexions.
    """
    gen = torch.Generator().manual_seed(graine)
    masques = {}
    for nom, mod in modele.named_modules():
        if isinstance(mod, nn.Linear):
            w = mod.weight
            k = max(1, int(round(garde * w.shape[1])))
            # Le tirage se fait sur CPU (reproductible quelle que soit la
            # machine), le masque vit sur le même appareil que les poids.
            idx = torch.argsort(torch.rand(w.shape, generator=gen), dim=1)[:, :k]
            masques[nom] = torch.zeros_like(w).scatter_(1, idx.to(w.device), 1.0)
    return masques


def appliquer_masque(modele, masques):
    """Le masque est réappliqué après CHAQUE pas : une connexion absente le reste."""
    with torch.no_grad():
        for nom, mod in modele.named_modules():
            if isinstance(mod, nn.Linear) and nom in masques:
                mod.weight.mul_(masques[nom])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--famille", choices=["dense", "route"], default="route")
    p.add_argument("--donnees", nargs="+", default=["data/corpus_en.txt"])
    p.add_argument("--validation", default="data/corpus_en_val.txt")
    p.add_argument("--dim", type=int, default=192)
    p.add_argument("--couches", type=int, default=4)
    p.add_argument("--tetes", type=int, default=4)
    p.add_argument("--cache", type=int, default=768, help="FFN dense, ou largeur d'expert")
    p.add_argument("--cache-perle", type=int, default=0, help="largeur d'un expert (routé)")
    p.add_argument("--experts", type=int, default=8)
    p.add_argument("--k", type=int, default=2)
    p.add_argument("--seq", type=int, default=128)
    p.add_argument("--lot", type=int, default=32)
    p.add_argument("--pas", type=int, default=20000)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--graine", type=int, default=1)
    p.add_argument("--init", type=float, default=0.08, help="écart-type d'initialisation")
    p.add_argument("--enseignant", default="", help="dossier d'un modèle gelé à imiter")
    p.add_argument("--alpha-distill", type=float, default=0.0,
                   help="poids de la KL d'enseignant ; 0 = apprentissage ordinaire")
    p.add_argument("--temperature", type=float, default=2.0, help="température de distillation")
    p.add_argument("--eval-tous", type=int, default=1000)
    p.add_argument("--sortie", required=True)
    p.add_argument("--kwta", type=float, default=0.0,
                   help="part GARDÉE par k-WTA sur l'entrée de o_proj/down_proj "
                        "(0 = aucun ; 0,25 = on annule 75 %% des activations)")
    p.add_argument("--elagage", type=float, default=0.0,
                   help="part GARDÉE des poids, par ligne de sortie (0 = aucun "
                        "élagage ; 0,5 = on annule la moitié des poids de chaque ligne)")
    p.add_argument("--elagage-tous", type=int, default=500,
                   help="pas entre deux élagages (rampe cubique de 1,0 vers la cible)")
    p.add_argument("--masque", type=float, default=0.0,
                   help="part des CONNEXIONS existantes à la naissance (0 = dense ; "
                        "0,25 = un connectome inné qui ne garde qu'un quart des poids "
                        "par ligne, tiré aléatoirement, jamais modifié)")
    p.add_argument("--poids-lognormaux", action="store_true",
                   help="apprendre theta et exécuter w = signe(theta)·exp(|theta|) — "
                        "distribution log-normale, comme les synapses corticales")
    p.add_argument("--sans-gpu", action="store_true")
    a = p.parse_args()
    # Lecture égale par construction : k experts lisent ce que lit le FFN dense.
    if not a.cache_perle:
        a.cache_perle = max(1, a.cache // max(1, a.k))

    torch.manual_seed(a.graine)
    dev = torch.device("cpu" if a.sans_gpu or not torch.cuda.is_available() else "cuda")
    train = charger(a.donnees)
    val = charger([a.validation])
    modele, cfg = construire(a.famille, a)
    modele = modele.to(dev)
    n_params = sum(q.numel() for q in modele.parameters())
    d = a.dim
    lit = 4 * d * d + a.k * 3 * d * a.cache_perle     # attention + k experts SwiGLU
    stocke = 4 * d * d + (a.experts * 3 * d * a.cache_perle if a.famille == "route"
                          else 3 * d * a.cache)
    print(f"# {a.famille} · {n_params/1e6:.2f} M paramètres · "
          f"{lit/1e6:.2f} M poids LUS par jeton et par couche · "
          f"{stocke/1e6:.2f} M stockés · corpus {len(train)} octets · {dev}")

    if a.kwta > 0.0:
        installer_kwta(modele, a.kwta)
    if a.elagage > 0.0:
        print(f"# élagage APPRIS : {a.elagage:.0%} des poids gardés par ligne, "
              f"rampe sur la première moitié de l'entraînement")
    masques = None
    if a.masque > 0.0:
        masques = installer_masque_inne(modele, a.masque, a.graine)
        print(f"# CONNECTOME INNÉ : {a.masque:.0%} des connexions, tirées une fois "
              f"(graine {a.graine}) et jamais modifiées — "
              f"{sum(m.sum().item() for m in masques.values())/1e6:.2f} M connexions")

    if a.poids_lognormaux:
        n = installer_poids_lognormaux(modele)
        print(f"# POIDS LOG-NORMAUX : {n} couches reparamétrées "
              f"(w = signe(theta)·exp(|theta|))")

    # AVEC DES POIDS LOG-NORMAUX, LA DÉCROISSANCE DE POIDS EST PROSCRITE : elle
    # s'applique à `theta`, pas à `w`, et tirer theta vers 0 pousse |w| vers 1 au
    # lieu de 0 — le modèle ne peut plus éteindre une connexion et l'entraînement
    # diverge (mesuré : perte 8 458 en 200 pas). Le taux d'apprentissage est réduit
    # pour la même raison : un pas sur theta est un pas MULTIPLICATIF sur w.
    decroissance = 0.0 if a.poids_lognormaux else 0.01
    if a.poids_lognormaux:
        a.lr = min(a.lr, 3e-4)
    opt = torch.optim.AdamW(modele.parameters(), lr=a.lr, weight_decay=decroissance)
    g = torch.Generator().manual_seed(a.graine)
    meilleur = (float("inf"), None, 0)
    debut = time.time()
    modele.train()
    # DISTILLATION : un enseignant gelé, de la MÊME famille et du MÊME tokenizer,
    # dont on imite la distribution entière et pas seulement l'argmax. C'est le
    # levier que le dépôt n'avait jamais essayé (inventaire du 08/10 : « aucune
    # distillation, mentionnée mais jamais réalisée »), et c'est le seul qui
    # puisse rattraper l'écart de qualité d'un modèle creux sans lui ajouter de
    # paramètres. `alpha` = 0 → apprentissage ordinaire, mesurable en A/B.
    enseignant = None
    if a.enseignant:
        from transformers import AutoModelForCausalLM
        enseignant = AutoModelForCausalLM.from_pretrained(a.enseignant,
                                                          dtype=torch.float32).to(dev).eval()
        for p in enseignant.parameters():
            p.requires_grad_(False)
        print(f"# distillation depuis {a.enseignant} · alpha {a.alpha_distill} · "
              f"température {a.temperature}")

    for pas in range(1, a.pas + 1):
        x, y = lot_aleatoire(train, a.seq, a.lot, g)
        x = x.to(dev)
        # Entrée et étiquettes = LA MÊME séquence : le modèle décale lui-même
        # (`shift_logits`/`shift_labels`). Passer `y` — déjà décalé par
        # `lot_aleatoire` — décale DEUX FOIS, et l'entraînement optimise alors la
        # prédiction de t+2 : un autre objectif, qui ne donne pas un modèle de
        # langage. Mesuré : perte d'entraînement 1,9 nat, et 7,9 bits/octet
        # partout à la fin, soit l'uniforme. Les bancs (`essai_decharge`,
        # `essai_blocs`) n'ont pas ce défaut : ils appellent `cross_entropy`
        # eux-mêmes sur des fenêtres décalées une seule fois.
        sortie = modele(input_ids=x, labels=x)
        perte = sortie.loss
        if enseignant is not None and a.alpha_distill > 0.0:
            # KL(enseignant || eleve), température T : `T²` remet le gradient à
            # l'échelle de la CE — sans lui, la distillation douce pèse T² fois
            # trop et écrase l'apprentissage.
            with torch.no_grad():
                lgt_e = enseignant(input_ids=x).logits
            lgt_s = sortie.logits
            logp_s = torch.log_softmax(lgt_s / a.temperature, dim=-1)
            p_e = torch.softmax(lgt_e / a.temperature, dim=-1)
            # `batchmean` divise par la TAILLE DU LOT, pas par le nombre de
            # jetons : sur des logits (lot, séquence, vocabulaire), la KL sortait
            # 128 fois trop grande (mesuré : perte 622 au lieu de ~10). On
            # redivise par la longueur de séquence, sinon la distillation écrase
            # l'apprentissage au lieu de le guider.
            kl = torch.nn.functional.kl_div(logp_s, p_e, reduction="batchmean") / x.shape[1]
            perte = (1.0 - a.alpha_distill) * perte + a.alpha_distill * (a.temperature ** 2) * kl
        opt.zero_grad(set_to_none=True)
        perte.backward()
        torch.nn.utils.clip_grad_norm_(modele.parameters(), 1.0)
        opt.step()
        if masques is not None:
            appliquer_masque(modele, masques)
        # ÉLAGAGE À RAMPE CUBIQUE : on ne coupe pas la moitié des poids au premier
        # pas (le modèle n'a rien appris), on y va progressivement — c'est la
        # différence entre élaguer et détruire.
        if a.elagage > 0.0 and pas % a.elagage_tous == 0:
            frac = min(1.0, pas / max(1, a.pas * 0.5)) ** 3
            garde = 1.0 - (1.0 - a.elagage) * frac
            if garde < 1.0:
                elaguer_lignes(modele, garde)

        if pas % a.eval_tous == 0 or pas == a.pas:
            modele.eval()
            tot, n = 0.0, 0
            with torch.no_grad():
                for k in range(min(8, (len(val) - 1) // (a.seq * a.lot))):
                    xv = torch.from_numpy(
                        np.stack([val[(k * a.lot + j) * a.seq:(k * a.lot + j) * a.seq + a.seq]
                                  for j in range(a.lot)]).astype(np.int64)).to(dev)
                    # LA MÊME séquence en entrée et en étiquettes : le modèle
                    # décale lui-même (`shift_logits`/`shift_labels`). Passer une
                    # entrée DÉJÀ décalée avec des étiquettes décalées décale
                    # DEUX FOIS et mesure la prédiction de t+2 — l'erreur a été
                    # commise ici, et elle a produit des « 2,95 bits/octet » pour
                    # un modèle dont la vraie mesure est 7,5.
                    tot += float(modele(input_ids=xv, labels=xv).loss) * xv.numel()
                    n += xv.numel()
            bpo = tot / max(n, 1) / math.log(2)
            if bpo < meilleur[0]:
                meilleur = (bpo, {kk: v.detach().clone() for kk, v in modele.state_dict().items()}, pas)
            print(f"  pas {pas:>6} · perte {perte.item():.4f} · val {bpo:.4f} bits/octet "
                  f"· {time.time()-debut:.0f} s")
            modele.train()

    modele.load_state_dict(meilleur[1])
    # L'export lit des poids ORDINAIRES : on matérialise avant d'écrire (sinon le
    # fichier porterait des clés `parametrizations.weight.original` que l'exporteur
    # ne connaît pas).
    if a.poids_lognormaux:
        materialiser_poids(modele)
    modele.eval()
    os.makedirs(a.sortie, exist_ok=True)
    modele.save_pretrained(a.sortie)
    print(f"\n  # meilleur point : pas {meilleur[2]} · val {meilleur[0]:.4f} bits/octet")
    print(f"  # écrit dans {a.sortie} · {n_params/1e6:.2f} M paramètres · "
          f"{lit/1e6:.2f} M poids lus/jeton/couche")
    return 0


if __name__ == "__main__":
    sys.exit(main())

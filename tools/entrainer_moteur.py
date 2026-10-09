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

    opt = torch.optim.AdamW(modele.parameters(), lr=a.lr, weight_decay=0.01)
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
    modele.eval()
    os.makedirs(a.sortie, exist_ok=True)
    modele.save_pretrained(a.sortie)
    print(f"\n  # meilleur point : pas {meilleur[2]} · val {meilleur[0]:.4f} bits/octet")
    print(f"  # écrit dans {a.sortie} · {n_params/1e6:.2f} M paramètres · "
          f"{lit/1e6:.2f} M poids lus/jeton/couche")
    return 0


if __name__ == "__main__":
    sys.exit(main())

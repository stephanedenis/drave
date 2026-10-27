#!/usr/bin/env python3
"""entrainer_nvlink.py — le protocole sémantique sur les deux GPU, par NVLink.

Ce script est lancé par `torchrun --nproc_per_node=2`. Chaque rang lit le même
article, mais dans des langues **différentes** ; les `z` sont rassemblés par
`all_gather` (NVLink, NCCL), et la contrastive est calculée sur les **articles**
comme positifs : plusieurs entrées, une sémantique commune. Le décodeur produit
la cible locale et une **seconde langue** — les sorties multilingues simultanées
servent au diagnostic d'ambiguïté.

La communication GPU-GPU est explicite :
- `all_gather` des `z` et des identifiants d'articles (NVLink) ;
- `DistributedDataParallel` pour l'all-reduce des gradients (NVLink) ;
- `NCCL_P2P_LEVEL=NVL` est posé par l'appelant pour forcer le lien direct.

Usage :
    NCCL_P2P_LEVEL=NVL torchrun --standalone --nproc_per_node=2 \
        tools/semantique/entrainer_nvlink.py --langues ... --pas 200
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import random
import sys
import time

import torch
import torch.distributed as dist
import torch.nn.functional as F

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from semantique.corpus import charger, decouper, exemple  # noqa: E402
from semantique.entrainer import info_nce, metriques, pad  # noqa: E402
from semantique.modele import Semantique  # noqa: E402


def lot_distribue(articles, langues, arts, lot, seq, rng):
    src = [rng.choice(langues) for _ in arts]
    tgt = [rng.choice([l for l in langues if l != s]) for s in src]
    ext = [rng.choice([l for l in langues if l != s]) for s in src]
    xs = [exemple(articles, a, s, seq) for a, s in zip(arts, src)]
    xt = [exemple(articles, a, t, seq) for a, t in zip(arts, tgt)]
    xe = [exemple(articles, a, e, seq) for a, e in zip(arts, ext)]
    return (xs, [langues.index(s) for s in src],
            xt, [langues.index(t) for t in tgt],
            xe, [langues.index(e) for e in ext])


class AllGather(torch.autograd.Function):
    """All-gather différentiable : le gradient revient à la tranche locale.

    `all_gather` détaché était le bug : la contrastive ne touchait jamais `z`,
    et `z` ne pouvait apprendre que l'alignement (qui collapse) et l'adversaire.
    """
    @staticmethod
    def forward(ctx, t: torch.Tensor) -> torch.Tensor:
        ctx.rang = dist.get_rank()
        ctx.taille = t.shape[0]
        out = [torch.zeros_like(t) for _ in range(dist.get_world_size())]
        dist.all_gather(out, t.contiguous())
        return torch.cat(out, 0)

    @staticmethod
    def backward(ctx, g: torch.Tensor) -> torch.Tensor:
        return g[ctx.rang * ctx.taille:(ctx.rang + 1) * ctx.taille]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", default="/tmp/natif-600-512-8-align-s1")
    ap.add_argument("--langues", default="fra,spa,deu,ita,por,rus,arb,cmn,hin,swh")
    ap.add_argument("--articles", type=int, default=30)
    ap.add_argument("--seq", type=int, default=256)
    ap.add_argument("--lot", type=int, default=8)
    ap.add_argument("--pas", type=int, default=200)
    ap.add_argument("--eval-tous", type=int, default=50)
    ap.add_argument("--patience", type=int, default=3)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--lr-base", type=float, default=1e-5)
    ap.add_argument("--lr-tete", type=float, default=1e-3)
    ap.add_argument("--d-sem", type=int, default=128)
    ap.add_argument("--prefixe", type=int, default=4)
    ap.add_argument("--pooling", default="mean", choices=("mean", "last"))
    ap.add_argument("--adv", type=float, default=0.5)
    ap.add_argument("--contrastif", type=float, default=1.0)
    ap.add_argument("--temperature", type=float, default=0.07)
    ap.add_argument("--align", type=float, default=0.1)
    ap.add_argument("--etat", default="",
                    help="état encodeur/décodeur à recharger (étage B)")
    ap.add_argument("--deux-bases", action="store_true",
                    help="étage B : copie de la base pour le décodeur, l'encodeur reste gelé")
    ap.add_argument("--lr-decode", type=float, default=2e-4)
    ap.add_argument("--gele-encodeur", action="store_true",
                    help="étage B : geler base et tête sémantique, entraîner le décodeur")
    ap.add_argument("--sans-decode", action="store_true",
                    help="étage A : entraîner l'encodeur seul (contrastive + alignement + adversaire)")
    ap.add_argument("--sans-chrf", action="store_true",
                    help="ne pas générer pendant l'évaluation (étage A)")
    ap.add_argument("--sorties", type=int, default=1,
                    help="langues cibles simultanées en plus de la cible principale (0/1/2)")
    ap.add_argument("--eval-chrf-articles", type=int, default=3)
    ap.add_argument("--eval-cibles", default="fra,spa,deu,cmn")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--sortie", default="/tmp/semantique-nvlink")
    args = ap.parse_args()
    dist.init_process_group("nccl")
    rang = dist.get_rank()
    monde = dist.get_world_size()
    local = int(os.environ.get("LOCAL_RANK", rang))
    torch.cuda.set_device(local)
    device = torch.device("cuda", local)
    torch.set_num_threads(2)
    langues = [l.strip() for l in args.langues.split(",") if l.strip()]
    articles = charger(langues, args.articles)
    train, val = decouper(articles)
    torch.manual_seed(args.graine + rang)
    rng = random.Random(args.graine + 1000 * rang)
    modele = Semantique.charger(args.checkpoint, len(langues), args.d_sem, args.prefixe, str(device),
                                deux_bases=args.deux_bases)
    if args.etat:
        paquet = torch.load(args.etat, map_location=device, weights_only=False)
        cible = modele.state_dict()
        filtre = {k: v for k, v in paquet["etat"].items()
                  if k in cible and cible[k].shape == v.shape}
        manquants = modele.load_state_dict(filtre, strict=False)
        if rang == 0 and (manquants.missing_keys or manquants.unexpected_keys):
            print(f"# état partiel : {len(manquants.missing_keys)} clés manquantes, "
                  f"{len(manquants.unexpected_keys)} inattendues", flush=True)
        if rang == 0:
            print(f"# état rechargé : {args.etat} (pas {paquet.get('meilleur')})", flush=True)
    if args.gele_encodeur:
        for nom, p in modele.named_parameters():
            if nom.startswith(("base.", "tete.")):
                p.requires_grad = False
    n_params = sum(p.numel() for p in modele.parameters())
    if rang == 0:
        print(f"# NVLink · {monde} rangs · {n_params/1e6:.2f} M · {len(langues)} langues · "
              f"{len(train)} train / {len(val)} val · seq {args.seq} · lot {args.lot}/rang · "
              f"sorties +{args.sorties}", flush=True)
    base_params = [p for n, p in modele.named_parameters() if n.startswith("base.")]
    decode_params = [p for n, p in modele.named_parameters() if n.startswith("base_decode.")]
    tete_params = [p for n, p in modele.named_parameters()
                   if not n.startswith(("base.", "base_decode."))]
    groupes = [{"params": base_params, "lr": args.lr_base},
               {"params": tete_params, "lr": args.lr_tete}]
    if decode_params:
        groupes.append({"params": decode_params, "lr": args.lr_decode})
    opt = torch.optim.AdamW(groupes, lr=args.lr)
    meilleur = (-1.0, 0)
    sans_gain = 0
    historique = []
    arts_train = list(train)
    t0 = time.monotonic()
    for pas in range(1, args.pas + 1):
        # mêmes articles sur les deux rangs, langues différentes par rang
        rng_arts = random.Random(args.graine * 1_000_003 + pas)
        # les articles du lot GLOBAL sont distincts : les rangs prennent des
        # moitiés disjointes, et les négatifs contrastifs existent enfin.
        global_arts = rng_arts.sample(arts_train, min(len(arts_train), args.lot * monde))
        arts = global_arts[rang * args.lot:(rang + 1) * args.lot]
        if len(arts) < args.lot:
            arts = (arts * args.lot)[:args.lot]
        xs, ls, xt, lt, xe, le = lot_distribue(train, langues, arts, args.lot, args.seq, rng)
        x_s, m_s = pad(xs); x_t, m_t = pad(xt); x_e, m_e = pad(xe)
        x_s, m_s, x_t, m_t, x_e, m_e = (x.to(device) for x in (x_s, m_s, x_t, m_t, x_e, m_e))
        ls_t = torch.tensor(ls, device=device); lt_t = torch.tensor(lt, device=device)
        le_t = torch.tensor(le, device=device)
        z_s = modele.encode(x_s, m_s, args.pooling)
        z_t = modele.encode(x_t, m_t, args.pooling)
        z_e = modele.encode(x_e, m_e, args.pooling) if args.sorties else None
        if args.sans_decode:
            rec = trans = sorties = torch.zeros((), device=device)
        else:
            rec = (modele.perte_texte(z_s, ls_t, x_s, m_s)
                   + modele.perte_texte(z_t, lt_t, x_t, m_t))
            trans = (modele.perte_texte(z_s, lt_t, x_t, m_t)
                     + modele.perte_texte(z_t, ls_t, x_s, m_s))
            sorties = torch.zeros((), device=device)
            if args.sorties:
                sorties = (modele.perte_texte(z_s, le_t, x_e, m_e)
                           + modele.perte_texte(z_t, le_t, x_e, m_e))
        # all-gather NVLink : plusieurs entrées, même article
        zs = AllGather.apply(z_s); zt = AllGather.apply(z_t)
        arts_t = torch.tensor(arts, device=device)
        arts_all = torch.cat([torch.zeros_like(arts_t) for _ in range(monde)])
        dist.all_gather(list(arts_all.chunk(monde)), arts_t)
        sim = zs @ zt.T / args.temperature
        masque = arts_all[:, None] == arts_all[None, :]
        logp = sim - torch.logsumexp(sim, dim=1, keepdim=True)
        contrastif_global = -(logp[masque].sum() / masque.sum().clamp_min(1))
        contrastif_local = info_nce(z_s, z_t, args.temperature)
        contrastif = 0.5 * (contrastif_global + contrastif_local)
        align = (1.0 - (z_s * z_t).sum(dim=-1)).mean()
        adv = (F.cross_entropy(modele.classif_langue(modele.retour_inverse(z_s)), ls_t)
               + F.cross_entropy(modele.classif_langue(modele.retour_inverse(z_t)), lt_t))
        perte = (rec + trans + sorties + args.align * align
                 + args.contrastif * contrastif + args.adv * adv)
        opt.zero_grad()
        perte.backward()
        # all-reduce des gradients sur NVLink (pas de DDP : la boucle appelle le module directement)
        for p in modele.parameters():
            if p.grad is not None:
                dist.all_reduce(p.grad, op=dist.ReduceOp.SUM)
                p.grad /= monde
        torch.nn.utils.clip_grad_norm_(modele.parameters(), 1.0)
        opt.step()
        if pas % args.eval_tous == 0 or pas == args.pas:
            if rang == 0:
                cibles = [l.strip() for l in args.eval_cibles.split(",") if l.strip() in langues]
                m = metriques(modele, train, val, langues, args.seq, device,
                              articles_chrf=args.eval_chrf_articles, cibles_chrf=cibles,
                              pooling=args.pooling, generer=not args.sans_chrf)
                m.update({"pas": pas, "perte": float(perte.detach()),
                          "contrastif": float(contrastif.detach()), "adversaire": float(adv.detach()),
                          "secondes": time.monotonic() - t0})
                historique.append(m)
                print(f"  pas {pas:4d} · perte {m['perte']:.3f} · align {m['alignement']:.3f} · "
                      f"rappel {m['rappel']:.3f} (mélangé {m['rappel_melange']:.3f}) · "
                      f"sonde {m['sonde_langue']:.3f} · chrF rec {m['chrf_reconstruction']:.1f} / "
                      f"trad {m['chrf_traduction']:.1f} / plancher {m['chrf_plancher']:.1f} · "
                      f"{m['secondes']:.0f} s", flush=True)
                if m["rappel"] > meilleur[0] + 1e-6:
                    meilleur = (m["rappel"], pas); sans_gain = 0
                else:
                    sans_gain += 1
            dist.barrier()
        if sans_gain >= args.patience:
            break
    if rang == 0:
        pathlib.Path(args.sortie).parent.mkdir(parents=True, exist_ok=True)
        torch.save({"etat": modele.state_dict(), "langues": langues,
                    "config": {"d_sem": args.d_sem, "prefixe": args.prefixe,
                               "seq": args.seq, "checkpoint": args.checkpoint},
                    "meilleur": meilleur[1]}, args.sortie)
        pathlib.Path(str(args.sortie) + ".json").write_text(
            json.dumps({"langues": langues, "train": list(train), "val": list(val),
                        "meilleur_pas": meilleur[1], "historique": historique},
                       ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"# écrit {args.sortie} · meilleur pas {meilleur[1]}", flush=True)
    dist.barrier()
    dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

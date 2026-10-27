#!/usr/bin/env python3
"""entrainer.py — le protocole sémantique natif, première version.

Trois choses, dans cet ordre :
1. **rejouer** des entrées multilingues parallèles : le même article, dans plusieurs
   langues, doit donner le même `z` (alignement) et se reconstruire (même langue) ;
2. **sens → texte** : de `z` et de la langue cible, le décodeur produit le texte ;
   la traduction est mesurée contre la référence humaine, avec le plancher
   source→référence ;
3. **convergence** : on arrête quand le rappel parallèle ne progresse plus ; la
   sonde de langue et le rappel mélangé sont les contrôles négatifs.

Usage :
    python3 tools/semantique/entrainer.py --checkpoint /tmp/natif-600-512-8-align-s1 \
        --pas 600 --eval-tous 100 --sortie /tmp/semantique-poc
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import random
import sys
import time

import torch
import torch.nn.functional as F

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from llm.mesure import chrf  # noqa: E402
from semantique.corpus import LANGUES, charger, decouper, exemple, lot  # noqa: E402
from semantique.modele import Semantique  # noqa: E402


def pad(seqs: list[list[int]], pad_id: int = 0):
    L = max(len(s) for s in seqs)
    ids = torch.full((len(seqs), L), pad_id, dtype=torch.long)
    masque = torch.zeros((len(seqs), L), dtype=torch.long)
    for i, s in enumerate(seqs):
        ids[i, :len(s)] = torch.tensor(s)
        masque[i, :len(s)] = 1
    return ids, masque


def info_nce(z_s: torch.Tensor, z_t: torch.Tensor, temperature: float = 0.07) -> torch.Tensor:
    """Les paires parallèles doivent être plus proches que les autres du lot.

    L'alignement seul collapse : tous les z se ressemblent (cosinus 0,98) et le
    rappel reste au hasard. La contrastive est ce qui rend le sens **discriminant**.
    """
    logits = z_s @ z_t.T / temperature
    cibles = torch.arange(z_s.shape[0], device=z_s.device)
    return 0.5 * (F.cross_entropy(logits, cibles) + F.cross_entropy(logits.T, cibles))


def tronque(texte: str, seq: int) -> str:
    """La référence à la même longueur que la cible générée."""
    return texte.encode("utf-8")[:seq].decode("utf-8", "ignore")


def texte(ids) -> str:
    return bytes(int(i) % 256 for i in ids).decode("utf-8", "replace").strip()


@torch.no_grad()
def etats(model, articles, langues, seq, device, pooling="mean", lot=64):
    cles = [(a, l) for a in articles for l in langues]
    z = {a: {} for a in articles}
    for debut in range(0, len(cles), lot):
        morceau = cles[debut:debut + lot]
        ids, masque = pad([exemple(articles, a, l, seq) for a, l in morceau])
        zz = model.encode(ids.to(device), masque.to(device), pooling=pooling)
        for (a, l), v in zip(morceau, zz):
            z[a][l] = v
    return z


@torch.no_grad()
def metriques(model, train, val, langues, seq, device, generer=True,
              articles_chrf: int = 3, cibles_chrf: list[str] | None = None,
              pooling: str = "mean"):
    model.eval()
    ztr = etats(model, train, langues, seq, device, pooling=pooling)
    zva = etats(model, val, langues, seq, device, pooling=pooling)
    arts = list(val)
    # alignement : mêmes articles, langues différentes
    align = []
    for art in arts:
        for i, a in enumerate(langues):
            for b in langues[i + 1:]:
                align.append(float(F.cosine_similarity(zva[art][a], zva[art][b], dim=0)))
    align = sum(align) / max(1, len(align))
    # rappels vectorisés : A [n_arts,d] @ B.T
    correct = total = 0
    for src in langues:
        A = torch.stack([zva[a][src] for a in arts])
        for tgt in langues:
            if tgt == src:
                continue
            B = torch.stack([zva[a][tgt] for a in arts])
            sims = A @ B.T
            correct += int((sims.argmax(dim=1) == torch.arange(len(arts), device=sims.device)).sum())
            total += len(arts)
    rappel = correct / max(1, total)
    # contrôle : les articles sont mélangés dans la cible
    perm = torch.tensor(random.Random(0).sample(range(len(arts)), len(arts)), device=device)
    correct = total = 0
    for src in langues:
        A = torch.stack([zva[a][src] for a in arts])
        for tgt in langues:
            if tgt == src:
                continue
            B = torch.stack([zva[a][tgt] for a in arts])[perm]
            sims = A @ B.T
            correct += int((sims.argmax(dim=1) == torch.arange(len(arts), device=sims.device)).sum())
            total += len(arts)
    rappel_melange = correct / max(1, total)
    # sonde de langue : centroïdes d'entraînement, z de validation
    centro = torch.stack([torch.stack([ztr[a][l] for a in ztr]).mean(0) for l in langues])
    correct = total = 0
    for l in langues:
        Z = torch.stack([zva[a][l] for a in arts])
        correct += int((Z @ centro.T).argmax(dim=1).eq(langues.index(l)).sum())
        total += len(arts)
    sonde = correct / max(1, total)
    # chrF : source français -> chaque langue, et reconstruction
    rec, trans, plancher = [], [], []
    if generer:
        cibles = cibles_chrf or [l for l in ("fra", "spa", "deu", "cmn") if l in langues]
        travaux = [(art, tgt) for art in arts[:max(1, articles_chrf)] for tgt in cibles]
        if travaux:
            zb = torch.stack([zva[a]["fra"] for a, _ in travaux])
            lb = torch.tensor([langues.index(t) for _, t in travaux], device=device)
            ids = model.generer(zb, lb, seq)
            for (art, tgt), ligne in zip(travaux, ids):
                hyp = texte(ligne.tolist())
                ref = tronque(val[art][tgt], seq)
                plancher.append(chrf(tronque(val[art]["fra"], seq), ref))
                (rec if tgt == "fra" else trans).append(chrf(hyp, ref))
    model.train()
    return {
        "alignement": align,
        "rappel": rappel,
        "rappel_melange": rappel_melange,
        "sonde_langue": sonde,
        "chrf_reconstruction": sum(rec) / max(1, len(rec)),
        "chrf_traduction": sum(trans) / max(1, len(trans)),
        "chrf_plancher": sum(plancher) / max(1, len(plancher)),
        "n_rappel": total,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", default="/tmp/natif-600-512-8-align-s1")
    ap.add_argument("--langues", default=",".join(LANGUES))
    ap.add_argument("--articles", type=int, default=30)
    ap.add_argument("--seq", type=int, default=128)
    ap.add_argument("--lot", type=int, default=8)
    ap.add_argument("--pas", type=int, default=600)
    ap.add_argument("--eval-tous", type=int, default=100)
    ap.add_argument("--patience", type=int, default=3)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--d-sem", type=int, default=128)
    ap.add_argument("--prefixe", type=int, default=4)
    ap.add_argument("--pooling", default="mean", choices=("mean", "last"))
    ap.add_argument("--adv", type=float, default=0.5,
                    help="poids de la confusion de langue (gradient inversé ; 0 = désactivé)")
    ap.add_argument("--contrastif", type=float, default=1.0,
                    help="poids de l'InfoNCE parallèle (0 = alignement seul, qui collapse)")
    ap.add_argument("--temperature", type=float, default=0.07)
    ap.add_argument("--align", type=float, default=0.1)
    ap.add_argument("--eval-chrf-articles", type=int, default=3)
    ap.add_argument("--eval-cibles", default="fra,spa,deu,cmn")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--sortie", default="/tmp/semantique-poc")
    ap.add_argument("--sans-gpu", action="store_true")
    args = ap.parse_args()
    langues = [l.strip() for l in args.langues.split(",") if l.strip()]
    device = torch.device("cpu" if args.sans_gpu or not torch.cuda.is_available() else "cuda")
    torch.manual_seed(args.graine)
    rng = random.Random(args.graine)
    articles = charger(langues, args.articles)
    train, val = decouper(articles)
    if not train or not val:
        print(f"# corpus vide : {len(articles)} articles, {len(train)} train, {len(val)} val")
        return 2
    print(f"# sémantique · {len(langues)} langues · {len(articles)} articles · "
          f"{len(train)} train / {len(val)} val · {device}")
    torch.set_num_threads(max(1, min(4, torch.get_num_threads())))
    model = Semantique.charger(args.checkpoint, len(langues), args.d_sem, args.prefixe, str(device))
    n_params = sum(p.numel() for p in model.parameters())
    print(f"# base {args.checkpoint} · {n_params/1e6:.2f} M paramètres · d_sem {args.d_sem} · "
          f"préfixe {args.prefixe}")
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    meilleur = (-1.0, 0, None)
    sans_gain = 0
    historique = []
    t0 = time.monotonic()
    for pas in range(1, args.pas + 1):
        xs, ls, xt, lt, _ = lot(train, langues, args.lot, args.seq, rng)
        x_s, m_s = pad(xs)
        x_t, m_t = pad(xt)
        x_s, m_s, x_t, m_t = x_s.to(device), m_s.to(device), x_t.to(device), m_t.to(device)
        ls_t = torch.tensor(ls, device=device)
        lt_t = torch.tensor(lt, device=device)
        z_s = model.encode(x_s, m_s, pooling=args.pooling)
        z_t = model.encode(x_t, m_t, pooling=args.pooling)
        align = (1.0 - (z_s * z_t).sum(dim=-1)).mean()
        rec = model.perte_texte(z_s, ls_t, x_s, m_s) + model.perte_texte(z_t, lt_t, x_t, m_t)
        trans = model.perte_texte(z_s, lt_t, x_t, m_t) + model.perte_texte(z_t, ls_t, x_s, m_s)
        z_s_adv = model.retour_inverse(z_s)
        z_t_adv = model.retour_inverse(z_t)
        adv = (F.cross_entropy(model.classif_langue(z_s_adv), ls_t)
               + F.cross_entropy(model.classif_langue(z_t_adv), lt_t))
        contraste = info_nce(z_s, z_t, args.temperature)
        perte = rec + trans + args.align * align + args.contrastif * contraste + args.adv * adv
        opt.zero_grad()
        perte.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if pas % args.eval_tous == 0 or pas == args.pas:
            cibles = [l.strip() for l in args.eval_cibles.split(",") if l.strip() in langues]
            m = metriques(model, train, val, langues, args.seq, device,
                          articles_chrf=args.eval_chrf_articles, cibles_chrf=cibles,
                          pooling=args.pooling)
            m.update({"pas": pas, "perte": float(perte.detach()), "secondes": time.monotonic() - t0})
            historique.append(m)
            print(f"  pas {pas:5d} · perte {m['perte']:.4f} · align {m['alignement']:.3f} · "
                  f"rappel {m['rappel']:.3f} (mélangé {m['rappel_melange']:.3f}) · "
                  f"sonde {m['sonde_langue']:.3f} · chrF rec {m['chrf_reconstruction']:.1f} / "
                  f"trad {m['chrf_traduction']:.1f} / plancher {m['chrf_plancher']:.1f} · "
                  f"{m['secondes']:.0f} s")
            if m["rappel"] > meilleur[0] + 1e-6:
                meilleur = (m["rappel"], pas, m)
                sans_gain = 0
            else:
                sans_gain += 1
            if sans_gain >= args.patience:
                print(f"  # convergence : rappel sans gain depuis {sans_gain} évaluations")
                break
    pathlib.Path(args.sortie).parent.mkdir(parents=True, exist_ok=True)
    torch.save({"etat": model.state_dict(), "langues": langues,
                "config": {"d_sem": args.d_sem, "prefixe": args.prefixe,
                           "checkpoint": args.checkpoint, "seq": args.seq},
                "meilleur": meilleur[1]}, args.sortie)
    json_path = pathlib.Path(str(args.sortie) + ".json")
    json_path.write_text(json.dumps({"langues": langues, "train": list(train), "val": list(val),
                                     "meilleur_pas": meilleur[1], "historique": historique},
                                    ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"# écrit {args.sortie} et {json_path} · meilleur pas {meilleur[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

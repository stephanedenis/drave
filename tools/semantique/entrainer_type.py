#!/usr/bin/env python3
"""entrainer_type.py — le modèle natif sur une base fixe d'universaux.

La sortie n'est plus un vecteur libre : c'est un **code typé** de 15 champs fixes
(jeu, action, source, cible, promotion, roque, case, symbole, carte, taille,
point, passe, chemin 0..2). Chaque champ a un vocabulaire fixe ; l'embedding est
le one-hot concaténé, et la lecture est un `argmax` — donc **déterministe**.

Le décodeur n'est pas neuronal : c'est le **codec classique** du jeu, qui rend la
RSN en surface. C'est l'hybride demandé : un bloc neuronal pour lire la surface,
un bloc classique pour rendre le sens.
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import random
import sys
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from jeux.codecs import codec  # noqa: E402
from semantique.entrainer import pad  # noqa: E402
from semantique.typed_corpus import decouper, items, lot, lot_par_paire  # noqa: E402
from semantique.synth_corpus import items_synth  # noqa: E402
from semantique.modele import RetourInverse  # noqa: E402
from semantique.universaux import CHAMPS, code_rsn, index_code, rsn_depuis_code  # noqa: E402


class ModeleType(nn.Module):
    def __init__(self, base: nn.Module, n_langues: int = 1):
        super().__init__()
        self.base = base
        self.d_model = int(base.config.hidden_size)
        self.tetes = nn.ModuleList([nn.Linear(self.d_model, len(vals)) for _, vals in CHAMPS])
        self.langue = nn.Linear(self.d_model, n_langues) if n_langues > 1 else None

    def encode(self, ids, masque):
        sortie = self.base(input_ids=ids, attention_mask=masque, output_hidden_states=True)
        h = sortie.hidden_states[-1]
        m = masque.unsqueeze(-1).to(h.dtype)
        return (h * m).sum(dim=1) / m.sum(dim=1).clamp(min=1)

    def logits_depuis_h(self, h):
        return [tete(h) for tete in self.tetes]

    def logits(self, ids, masque):
        return self.logits_depuis_h(self.encode(ids, masque))


def labels(items_, index: dict[str, int]):
    return {nom: torch.tensor([index[nom][i.code[nom]] for i in items_], dtype=torch.long)
            for nom, _ in CHAMPS}


def predire_lot(modele, items_, seq, device, lot=64):
    """Comme predire, mais lit correctement les 15 têtes par item."""
    modele.eval()
    out = []
    with torch.no_grad():
        for debut in range(0, len(items_), lot):
            mor = items_[debut:debut + lot]
            xs = [list(i.texte.encode("utf-8"))[:seq] for i in mor]
            x, m = pad(xs)
            logits = modele.logits(x.to(device), m.to(device))
            for j in range(len(mor)):
                code = {nom: CHAMPS[f][1][int(logits[f][j].argmax())]
                        for f, (nom, _) in enumerate(CHAMPS)}
                out.append(code)
    return out


def consistance(logits, choix):
    """Même paire, langues différentes → mêmes distributions par champ."""
    groupes = {}
    for j, it in enumerate(choix):
        groupes.setdefault(it.paire, []).append(j)
    total = 0.0
    n = 0
    for idx in groupes.values():
        if len(idx) < 2:
            continue
        for f, _ in enumerate(CHAMPS):
            p = F.softmax(logits[f][idx], dim=-1)
            total = total + ((p - p.mean(dim=0)) ** 2).mean()
            n += 1
    return total / max(1, n)


def exactitude(items_, codes):
    n = len(items_)
    par_champ = {nom: 0 for nom, _ in CHAMPS}
    exact = 0
    for it, c in zip(items_, codes):
        if all(c[nom] == it.code[nom] for nom, _ in CHAMPS):
            exact += 1
        for nom, _ in CHAMPS:
            par_champ[nom] += int(c[nom] == it.code[nom])
    return {"exact": exact / max(1, n), **{nom: v / max(1, n) for nom, v in par_champ.items()}}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", default="/tmp/natif-600-512-8-align-s1")
    ap.add_argument("--seq", type=int, default=64)
    ap.add_argument("--lot", type=int, default=32)
    ap.add_argument("--pas", type=int, default=500)
    ap.add_argument("--eval-tous", type=int, default=100)
    ap.add_argument("--patience", type=int, default=3)
    ap.add_argument("--lr-base", type=float, default=2e-4)
    ap.add_argument("--lr-tete", type=float, default=1e-3)
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--gele-base", action="store_true")
    ap.add_argument("--synth", action="store_true",
                    help="entraîner sur les surfaces synthétiques, tester sur les surfaces réelles")
    ap.add_argument("--synth-max-par-jeu", type=int, default=4000)
    ap.add_argument("--consistance", type=float, default=0.0,
                    help="poids de la cohérence entre langues d'une même paire")
    ap.add_argument("--par-paire", type=int, default=4)
    ap.add_argument("--adv-langue", type=float, default=0.0,
                    help="poids de l'adversaire de langue (gradient inversé)")
    ap.add_argument("--sortie", default="/tmp/semantique-type")
    args = ap.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(args.graine)
    rng = random.Random(args.graine)
    its = items()
    if args.synth:
        synth = items_synth()
        par_jeu = {}
        for it in synth:
            par_jeu.setdefault(it.jeu, []).append(it)
        train = []
        for jeu, lst in par_jeu.items():
            rng.shuffle(lst)
            train.extend(lst[:args.synth_max_par_jeu])
        val = its
        print(f"# synth · {len(train)} train synthétiques · {len(val)} surfaces réelles de test", flush=True)
    else:
        train, val = decouper(its, args.graine, 0.2)
    print(f"# typé · {len(its)} items · {len(train)} train / {len(val)} val · "
          f"{len({i.paire for i in train})} paires train · {len({i.paire for i in val})} val · "
          f"{len(CHAMPS)} champs · {sum(len(v) for _, v in CHAMPS)} classes", flush=True)
    langues_train = sorted({it.langue for it in train})
    idx_langue = {l: i for i, l in enumerate(langues_train)}
    base = AutoModelForCausalLM.from_pretrained(args.checkpoint, dtype=torch.float32)
    modele = ModeleType(base, len(langues_train)).to(device)
    if args.gele_base:
        for p in modele.base.parameters():
            p.requires_grad = False
    opt = torch.optim.AdamW([
        {"params": modele.base.parameters(), "lr": args.lr_base},
        {"params": modele.tetes.parameters(), "lr": args.lr_tete},
    ])
    if modele.langue is not None:
        opt.add_param_group({"params": modele.langue.parameters(), "lr": args.lr_tete})
    index = {nom: {v: i for i, v in enumerate(vals)} for nom, vals in CHAMPS}
    ytr = {k: v.to(device) for k, v in labels(train, index).items()}
    yva = labels(val, index)
    id_train = {id(it): j for j, it in enumerate(train)}
    # majorité d'entraînement (contrôle)
    majoritaire = {}
    for nom, _ in CHAMPS:
        majoritaire[nom] = collections.Counter(i.code[nom] for i in train).most_common(1)[0][0]
    meilleur = (-1.0, 0)
    sans_gain = 0
    hist = []
    t0 = time.monotonic()
    for pas in range(1, args.pas + 1):
        if args.synth:
            xs, choix = lot_par_paire(train, args.lot, args.seq, rng, args.par_paire)
        else:
            xs, choix = lot(train, args.lot, args.seq, rng)
        x, m = pad(xs)
        x, m = x.to(device), m.to(device)
        h = modele.encode(x, m)
        logits = modele.logits_depuis_h(h)
        idx = torch.tensor([id_train[id(c)] for c in choix], device=device)
        ce = sum(F.cross_entropy(logits[f], ytr[nom][idx])
                 for f, (nom, _) in enumerate(CHAMPS))
        cons = consistance(logits, choix) if args.consistance else torch.zeros((), device=device)
        adv = torch.zeros((), device=device)
        if args.adv_langue and modele.langue is not None:
            yl = torch.tensor([idx_langue[c.langue] for c in choix], device=device)
            adv = F.cross_entropy(modele.langue(RetourInverse.apply(h)), yl)
        perte = ce + args.consistance * cons + args.adv_langue * adv
        opt.zero_grad(); perte.backward()
        torch.nn.utils.clip_grad_norm_(modele.parameters(), 1.0)
        opt.step()
        if pas % args.eval_tous == 0 or pas == args.pas:
            codes = predire_lot(modele, val, args.seq, device)
            acc = exactitude(val, codes)
            hist.append({"pas": pas, "perte": float(perte.detach()),
                         "consistance": float(cons.detach()),
                         "adv_langue": float(adv.detach()), **acc,
                         "secondes": time.monotonic() - t0})
            print(f"  pas {pas:4d} · perte {float(perte.detach()):.3f} · exact {acc['exact']:.3f} · "
                  f"jeu {acc['jeu']:.3f} · action {acc['action']:.3f} · de {acc['de']:.3f} · "
                  f"vers {acc['vers']:.3f} · carte {acc['carte']:.3f} · {time.monotonic()-t0:.0f} s",
                  flush=True)
            if acc["exact"] > meilleur[0]:
                meilleur = (acc["exact"], pas); sans_gain = 0
            else:
                sans_gain += 1
            if sans_gain >= args.patience:
                break
    codes_tr = predire_lot(modele, train, args.seq, device)
    acc_tr = exactitude(train, codes_tr)
    codes = predire_lot(modele, val, args.seq, device)
    acc = exactitude(val, codes)
    # contrôle majoritaire
    acc_maj = exactitude(val, [majoritaire for _ in val])
    # invariance par paire : les surfaces d'une même paire doivent donner le même code
    groupes = collections.defaultdict(list)
    for it, c in zip(val, codes):
        groupes[it.paire].append(tuple(c[nom] for nom, _ in CHAMPS))
    inv = [len(set(v)) == 1 for v in groupes.values() if len(v) > 1]
    # rendu classique sur les formats canoniques
    rendus = []
    for it, c in zip(val, codes):
        if it.format in ("multilingue", "inconnu"):
            continue
        try:
            surf = codec(it.jeu).rend(rsn_depuis_code(c), format=it.format)
        except Exception:
            continue
        rendus.append(surf.strip().lower() == it.texte.strip().lower())
    # déterminisme
    codes2 = predire_lot(modele, val, args.seq, device)
    det = sum(a == b for a, b in zip(codes, codes2)) / max(1, len(codes))
    resultat = {"items": len(its), "train": len(train), "val": len(val),
                "paires_val": len(groupes), "champs": len(CHAMPS),
                "meilleur_pas": meilleur[1], "train_exact": acc_tr["exact"],
                "train_par_champ": {nom: acc_tr[nom] for nom, _ in CHAMPS},
                "exact": acc["exact"],
                "par_champ": {nom: acc[nom] for nom, _ in CHAMPS},
                "majoritaire_exact": acc_maj["exact"],
                "invariance_paires": sum(inv) / max(1, len(inv)),
                "determinisme": det,
                "rendu_classique": sum(rendus) / max(1, len(rendus)),
                "n_rendu": len(rendus),
                "historique": hist}
    pathlib.Path(str(args.sortie) + ".json").write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"# train exact {acc_tr['exact']:.3f} · exact {acc['exact']:.3f} · majoritaire {acc_maj['exact']:.3f} · "
          f"invariance paires {resultat['invariance_paires']:.3f} · "
          f"déterminisme {det:.3f} · rendu classique {resultat['rendu_classique']:.3f} "
          f"({len(rendus)})", flush=True)
    print(f"# écrit {args.sortie}.json", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

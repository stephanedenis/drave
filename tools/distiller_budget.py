#!/usr/bin/env python3
"""distiller_budget.py — N2 : le budget, les données et le curriculum de longueur.

Le dispositif de N2 est reconstruit (professeur byte-level 23,57 M, élève
`drave-n0` 11,47 M) et conservé dans
`/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/`. La distillation de la
veille ne voyait que **20,48 Mo** d'un seul corpus, sur 5 000 pas. Ce script
rejoue le **budget complet** — 20 000 pas × 16 × 128 = **41 Mo** — et permet de
comparer, à budget strictement égal :

  --corpus fr     : `data/corpus_fr_train.txt` (français seul) ;
  --corpus multi  : le manifeste `reports/native-corpus-multi.json` (quatre
                    sources : français, UDHR, anglais, littérature mixte),
                    reconstruit à l'identique (quotas + ordre de van der Corput).

Un **plan** de stages `seq:pas:lr` enchaîne les longueurs et les taux
d'apprentissage dans un même run (le curriculum 129 de N2.33 est le dernier
stage : `129:10000:5e-6`, lot 15).

Chaque run est évalué sous les protocoles qui ont produit les chiffres
historiques, pour que la comparaison soit licite :

  ppl_128_lot16  : 8 lots × 16 fenêtres de 128 — **le protocole de 2,7078** (N2.19) ;
  ppl_129_lot15  : 8 lots × 15 fenêtres de 129 — **le protocole de 2,6998** (N2.33) ;
  ppl_permute    : contrôle négatif — mêmes octets de validation, ordre détruit.

Les graines décalent les fenêtres (Van der Corput n'a pas d'état) :
`compteur += (graine − 1) × 10 000 019`, comme la campagne de la veille.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python tools/distiller_budget.py \
      --enseignant .../route-teacher-20k --init .../drave-n0-base-20k.pt \
      --corpus fr --stages "128:10000:1e-4,128:10000:3e-5" --graine 1 \
      --sortie /chemin/fr-g1.pt
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import time

import torch
import torch.nn.functional as F

from tools.native_model import NativeConfig, NativeModel
from tools.vdc import departs_vdc, ordre_vdc

DECALAGE_GRAINE = 10_000_019
ARTEFACTS = pathlib.Path("/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts")


def charger(txt: str | pathlib.Path) -> torch.Tensor:
    return torch.tensor(list(pathlib.Path(txt).read_bytes()), dtype=torch.long)


def lot_fr(data, n, seq, device, compteur):
    """n fenêtres de seq+1 octets : l'entrée est x[:, :-1], la cible x[:, 1:]."""
    i = torch.tensor(departs_vdc(compteur, n, len(data) - seq - 2, seq), dtype=torch.long)
    return torch.stack([data[j:j + seq + 1] for j in i]).to(device)


class CorpusMulti:
    """Fenêtres multi-sources reconstruites depuis le manifeste (offsets seuls)."""

    def __init__(self, manifeste: str, quotas: str = "proportionnel", seq_max: int = 256):
        m = json.loads(pathlib.Path(manifeste).read_text())
        self.mode = quotas
        self.fenetre, self.pas, self.max_fenetres = m["fenetre"], m["pas"], m["fenetres"]
        self.fichiers = {s["source"]: pathlib.Path(s["source"]).read_bytes()
                         for s in m["sources"]}
        sources = m["sources"]
        total = sum(s["fenetres"] for s in sources)
        # `round` reproduit le manifeste (49 999 fenêtres) ; `//` en perdait deux.
        # Le manifeste est **proportionnel** : l'anglais y prend 41 257 des 49 999
        # fenêtres (82 %). `equilibre` donne le même quota à chaque source.
        if self.mode == "equilibre":
            par_source = {s["source"]: self.max_fenetres // len(sources) for s in sources}
        else:
            par_source = {s["source"]: max(1, round(self.max_fenetres * s["fenetres"] / total))
                          for s in sources}
        offsets = []
        for s in sources:
            q = par_source[s["source"]]
            offsets += [(s["source"], o) for o in
                        range(0, max(0, len(self.fichiers[s["source"]]) - self.fenetre + 1),
                              self.pas)[:q]]
        offsets = [offsets[i] for i in ordre_vdc(len(offsets))][:self.max_fenetres]
        n_val = min(5000, len(offsets) // 2)
        self.train, self.val = offsets[:-n_val], offsets[-n_val:]
        if self.mode == "proportionnel":
            assert len(self.train) == m["train"] and len(self.val) == m["val"], (
                f"manifeste non reproduit : {len(self.train)}/{len(self.val)} "
                f"au lieu de {m['train']}/{m['val']}")

    def _fenetre(self, source: str, offset: int, seq: int) -> list[int]:
        octets = self.fichiers[source]
        if offset + seq > len(octets):
            offset = max(0, len(octets) - seq)
        return list(octets[offset:offset + seq])

    def lot(self, n, seq, device, compteur):
        """n fenêtres de seq+1 octets, lues à leur offset source."""
        idx = departs_vdc(compteur, n, len(self.train), seq)
        xs = [self._fenetre(*self.train[i], seq + 1) for i in idx]
        return torch.tensor(xs, dtype=torch.long).to(device)


def cible(x):
    return x[:, 1:]


def ppl(modele, lots, seq, n_lots, device):
    modele.eval(); tot = 0.0; n = 0
    with torch.no_grad():
        for k in range(n_lots):
            x = lots(k)
            y = cible(x)
            logits = modele(x[:, :-1])["logits"]
            tot += float(F.cross_entropy(logits.reshape(-1, 256), y.reshape(-1),
                                         reduction="sum"))
            n += y.numel()
    return math.exp(tot / max(1, n))


def plan_depuis(texte: str) -> list[tuple[int, int, float]]:
    plan = []
    for bloc in texte.split(","):
        seq, pas, lr = bloc.split(":")
        plan.append((int(seq), int(pas), float(lr)))
    return plan


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--enseignant", default=str(ARTEFACTS / "route-teacher-20k"))
    ap.add_argument("--init", default=str(ARTEFACTS / "drave-n0-base-20k.pt"))
    ap.add_argument("--corpus", choices=("fr", "multi"), default="fr")
    ap.add_argument("--manifeste", default="reports/native-corpus-multi.json")
    ap.add_argument("--quotas", choices=("proportionnel", "equilibre"), default="proportionnel",
                    help="proportionnel = le manifeste (82 %% anglais) ; equilibre = même part")
    ap.add_argument("--train", default="data/corpus_fr_train.txt")
    ap.add_argument("--val", default="data/corpus_fr_val.txt")
    ap.add_argument("--stages", default="128:10000:1e-4,128:10000:3e-5")
    ap.add_argument("--lot", type=int, default=16)
    ap.add_argument("--temperature", type=float, default=2.0)
    ap.add_argument("--alpha", type=float, default=0.7)
    ap.add_argument("--tetes", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--log", default=None)
    a = ap.parse_args()

    torch.manual_seed(a.graine)
    plan = plan_depuis(a.stages)
    decalage = (a.graine - 1) * DECALAGE_GRAINE
    sortie = pathlib.Path(a.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    log = open(a.log, "a") if a.log else None

    def dire(txt):
        print(txt, flush=True)
        if log:
            log.write(txt + "\n"); log.flush()

    from transformers import AutoModelForCausalLM
    prof = AutoModelForCausalLM.from_pretrained(a.enseignant, dtype=torch.float32).to(a.device).eval()
    for p in prof.parameters():
        p.requires_grad_(False)
    ck = torch.load(a.init, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items()
                          if k in NativeConfig.__annotations__})
    etu = NativeModel(cfg).to(a.device)
    manquants = etu.load_state_dict(ck["state"], strict=False)
    dire(f"# init {a.init} · manquants {list(manquants.missing_keys)[:6]} · "
         f"graine {a.graine} · décalage {decalage}")
    opt = torch.optim.AdamW(etu.parameters(), lr=plan[0][2], weight_decay=0.01)

    corpus = None
    if a.corpus == "fr":
        train = charger(a.train)
        lots = lambda compteur, n, seq: lot_fr(train, n, seq, a.device, compteur)
    else:
        corpus = CorpusMulti(a.manifeste, a.quotas)
        dire(f"# manifeste reproduit : {len(corpus.train)} train / {len(corpus.val)} val")
        lots = lambda compteur, n, seq: corpus.lot(n, seq, a.device, compteur)

    val = charger(a.val)
    val_perm = val[torch.tensor(ordre_vdc(len(val)), dtype=torch.long)]

    def eval_hist(seq, lot, n_lots=8, source=val):
        return ppl(etu, lambda k: lot_fr(source, lot, seq, a.device, k * lot), seq, n_lots,
                   a.device)

    t0 = time.time(); pas_global = 0; pertes = []; courbe = []
    for seq, n_pas, lr in plan:
        for g in opt.param_groups:
            g["lr"] = lr
        dire(f"# stage seq {seq} · {n_pas} pas · lr {lr}")
        for _ in range(n_pas):
            pas_global += 1
            etu.train()
            x = lots(decalage + pas_global * a.lot, a.lot, seq)
            x, y = x[:, :-1], cible(x)
            with torch.no_grad():
                lp = prof(x).logits
            sortie_m = etu(x)
            ls = sortie_m["logits"]
            T = a.temperature
            kd = F.kl_div(F.log_softmax(ls / T, -1), F.softmax(lp / T, -1),
                          reduction="batchmean", log_target=False) * (T * T)
            ce = F.cross_entropy(ls.reshape(-1, 256), y.reshape(-1))
            perte = a.alpha * kd + (1 - a.alpha) * ce
            if a.tetes:
                for e in sortie_m["early"]:
                    perte = perte + 0.1 * F.cross_entropy(e.reshape(-1, 256), y.reshape(-1))
                for l in sortie_m["local"]:
                    perte = perte + 0.05 * F.cross_entropy(l.reshape(-1, 256), y.reshape(-1))
            opt.zero_grad(); perte.backward()
            torch.nn.utils.clip_grad_norm_(etu.parameters(), 1.0)
            opt.step(); pertes.append(float(perte))
            if pas_global % 250 == 0:
                p = eval_hist(seq, 4, n_lots=2)
                dire(f"pas {pas_global:5d} · seq {seq} · perte {float(perte):.4f} · "
                     f"PPL 128/4 {p:.4f} · {time.time() - t0:.0f} s")
                courbe.append({"pas": pas_global, "seq": seq, "perte": float(perte), "ppl": p})

    # Évaluation finale, sous les protocoles historiques.
    etu.eval()
    res = {
        "init": a.init, "corpus": a.corpus, "graine": a.graine, "plan": plan,
        "lot": a.lot, "temperature": a.temperature, "alpha": a.alpha, "tetes": a.tetes,
        "pas": pas_global, "octets_vus": sum(n * a.lot * q for q, n, _ in plan),
        "perte_finale": pertes[-1],
        "ppl_128_lot16": eval_hist(128, 16),
        "ppl_128_lot8": eval_hist(128, 8),
        "ppl_129_lot15": eval_hist(129, 15),
        "ppl_permute": ppl(etu, lambda k: lot_fr(val_perm, 16, 128, a.device, 90_000_000 + k * 16),
                           128, 8, a.device),
    }
    if corpus is not None:
        res["ppl_multi_val"] = ppl(
            etu, lambda k: torch.tensor(
                [corpus._fenetre(*corpus.val[i], 129) for i in
                 departs_vdc(90_000_000 + k * 16, 16, len(corpus.val), 128)], dtype=torch.long
            ).to(a.device), 128, 8, a.device)
    # Précision sur la **validation**, pas sur l'entraînement : la version
    # d'origine échantillonnait `lots` (le corpus d'entraînement) et surestimait
    # le top-1 — corrigé le 31/10 après la campagne N2.d, qui garde donc ce champ
    # sur l'entraînement dans ses JSON ; la fiche lit `tools/eval_n2_budget.py`.
    bons = [0] * (len(cfg.early_blocks) + 1); n_ev = 0
    with torch.no_grad():
        for k in range(4):
            i = torch.tensor(departs_vdc(80_000_000 + k * a.lot, a.lot,
                                         len(val) - 129, 128), dtype=torch.long)
            x = torch.stack([val[j:j + 129] for j in i]).to(a.device)
            s = etu(x[:, :-1])
            bons[0] += int((s["logits"].argmax(-1) == x[:, 1:]).sum())
            for j, e in enumerate(s["early"]):
                bons[j + 1] += int((e.argmax(-1) == x[:, 1:]).sum())
            n_ev += x[:, 1:].numel()
    res["precision_main"] = bons[0] / max(1, n_ev)
    res["precision_early"] = [b / max(1, n_ev) for b in bons[1:]]
    res["duree_s"] = time.time() - t0
    res["courbe"] = courbe
    torch.save({"config": cfg.__dict__, "state": etu.state_dict()}, sortie)
    sortie.with_suffix(".json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    dire(json.dumps({k: v for k, v in res.items() if k != "courbe"},
                    ensure_ascii=False, indent=1))
    if log:
        log.close()


if __name__ == "__main__":
    main()

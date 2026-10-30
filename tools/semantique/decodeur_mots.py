#!/usr/bin/env python3
"""decodeur_mots.py — B10 : un décodeur au niveau du MOT, conditionné sur le même `z`.

POURQUOI CE FICHIER. B10.2bis a testé quatre leviers et quatre négatifs : l'attention croisée,
la durée, le corpus (JW) et la capacité (31,77 M) ne franchissent pas le plancher chrF. Le
décodeur du protocole génère des **octets** (le modèle natif a 256 symboles) : la question qui
reste est l'**objectif de décodage**. Ce fichier en construit un autre, à protocole constant :
le même `z` (encodeur gelé, 9,29 M) et le même découpage 24/6, mais un décodeur qui produit des
**mots** — embedding de mots, embedding de langue, attention croisée sur `z`, sortie softmax
sur le vocabulaire.

Ce que l'expérience mesure :
  - le **chrF** de la traduction (fra → spa/deu/ita/por/rus/swh), 3 graines, contre le
    décodeur octet (11,1 sur les mêmes articles) et contre le **plancher** source→référence ;
  - les **contrôles** : `z` d'un autre article (le décodeur doit s'effondrer), langue cible
    changée (il doit changera), et le plancher.

Ce qu'elle ne mesure pas : le cas des langues sans espaces (cmn) — le découpage en mots y est
approximatif ; et la comparaison des chrF entre unités différentes (octets contre mots) est une
comparaison de **systèmes**, pas de calculs identiques.

Usage :
  gpu-env/bin/python3 tools/semantique/decodeur_mots.py --graine 1 --pas 3000 --sortie /tmp/mots-s1
  gpu-env/bin/python3 tools/semantique/decodeur_mots.py --mesure reports/b10-decodeur-mots.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import statistics
import sys
import time

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from llm.mesure import chrf  # noqa: E402
from semantique import corpus as corpus_udhr  # noqa: E402
from semantique import corpus_jw  # noqa: E402
from semantique.modele import Semantique  # noqa: E402

CHECKPOINT = "/tmp/natif-224-6-align-s1"
D_SEM = 128
D = 128
MAX_MOTS = 64

# Les réglages dépendent du corpus : deux mondes, deux protocoles.
CONFIGS = {
    "udhr": {"module": corpus_udhr, "encodeur": "/tmp/b102bis-a-s1",
             "langues": [l for l in corpus_udhr.LANGUES if l != "cmn"],
             "source": "fra", "cibles": ["spa", "deu", "ita", "por", "rus", "swh"]},
    "jw": {"module": corpus_jw, "encodeur": "/tmp/jw-a-s1",
           "langues": [l for l in corpus_jw.LANGUES if l != "jpn"],
           "source": "eng", "cibles": ["ind", "swh", "vie"]},
}
CONFIG = CONFIGS["udhr"]
CIBLES = CONFIG["cibles"]
SOURCE = CONFIG["source"]
ENCODEUR_ENTRAINE = CONFIG["encodeur"]


# ------------------------------------------------------------------ le vocabulaire

class Vocabulaire:
    def __init__(self, articles: dict, langues: list[str], max_mots: int = 20000) -> None:
        from collections import Counter
        compte: Counter = Counter()
        for textes in articles.values():
            for langue in langues:
                compte.update(textes[langue].split())
        self.mots = ["<pad>", "<unk>", "<bos>", "<eos>"] + \
                    [m for m, _ in compte.most_common(max_mots)]
        self.index = {m: i for i, m in enumerate(self.mots)}
        self.langues = {l: i for i, l in enumerate(langues)}

    def __len__(self) -> int:
        return len(self.mots)

    def encode(self, texte: str, max_mots: int = MAX_MOTS) -> list[int]:
        ids = [self.index.get(m, 1) for m in texte.split()][:max_mots]
        return ids + [3]  # <eos>

    def decode(self, ids: list[int]) -> str:
        mots = []
        for i in ids:
            if i == 3:
                break
            if i > 3:
                mots.append(self.mots[i])
        return " ".join(mots)


# ------------------------------------------------------------------ le décodeur

class DecodeurMots(nn.Module):
    """Un petit décodeur autoregressif de mots, conditionné par `z` et la langue cible."""

    def __init__(self, n_vocab: int, n_langues: int, d: int = D, d_sem: int = D_SEM,
                 couches: int = 2, tetes: int = 4) -> None:
        super().__init__()
        self.mots = nn.Embedding(n_vocab, d, padding_idx=0)
        self.langue = nn.Embedding(n_langues, d)
        self.position = nn.Embedding(MAX_MOTS + 2, d)
        self.z = nn.Linear(d_sem, d)
        couche = nn.TransformerDecoderLayer(d, tetes, 4 * d, batch_first=True,
                                            dropout=0.1, norm_first=True)
        self.decodeur = nn.TransformerDecoder(couche, couches)
        self.sortie = nn.Linear(d, n_vocab)

    def forward(self, tokens: torch.Tensor, langue: torch.Tensor, z: torch.Tensor):
        B, T = tokens.shape
        positions = torch.arange(T, device=tokens.device).unsqueeze(0)
        h = self.mots(tokens) + self.position(positions) + self.langue(langue).unsqueeze(1)
        memoire = self.z(z).unsqueeze(1)
        masque = torch.triu(torch.ones(T, T, device=tokens.device, dtype=torch.bool), 1)
        sortie = self.decodeur(h, memoire, tgt_mask=masque)
        return self.sortie(sortie)

    @torch.no_grad()
    def generer(self, z: torch.Tensor, langue: torch.Tensor, max_mots: int = MAX_MOTS):
        B = z.shape[0]
        tokens = torch.full((B, 1), 2, dtype=torch.long, device=z.device)  # <bos>
        finis = torch.zeros(B, dtype=torch.bool, device=z.device)
        for _ in range(max_mots):
            logits = self.forward(tokens, langue, z)[:, -1]
            suivant = logits.argmax(dim=-1)
            suivant = torch.where(finis, torch.full_like(suivant, 0), suivant)
            tokens = torch.cat([tokens, suivant.unsqueeze(1)], dim=1)
            finis |= suivant == 3
            if bool(finis.all()):
                break
        return tokens


# ------------------------------------------------------------------ les données

def _configurer(corpus: str) -> None:
    """Fixe le monde (corpus, encodeur, source, cibles) pour la durée du run."""
    global CONFIG, CIBLES, SOURCE, ENCODEUR_ENTRAINE
    CONFIG = CONFIGS[corpus]
    CIBLES = CONFIG["cibles"]
    SOURCE = CONFIG["source"]
    ENCODEUR_ENTRAINE = CONFIG["encodeur"]


def etats_encodeur(articles: dict, langues: list[str], device, seq: int = 128) -> dict:
    """Le `z` GELÉ de chaque (article, langue) : l'encodeur ne bouge pas."""
    # L'encodeur est celui de B10.2bis, ENTRAÎNÉ puis GELÉ : le checkpoint de base seul
    # n'a pas de tête (elle est créée aléatoirement) — geler une tête au hasard ne
    # mesurerait rien. On recharge l'état sauvé par entrainer.py.
    model = Semantique.charger(CHECKPOINT, len(CONFIG["module"].LANGUES), D_SEM, 4,
                               str(device))
    etat = torch.load(ENCODEUR_ENTRAINE, map_location="cpu")
    model.load_state_dict(etat["etat"])
    model.eval()
    cache: dict = {}
    with torch.no_grad():
        for art, textes in articles.items():
            for langue in langues:
                ids = torch.tensor([CONFIG["module"].exemple(articles, art, langue, seq)],
                                   device=device)
                masque = torch.ones_like(ids)
                cache[(art, langue)] = model.encode(ids, masque)[0].cpu()
    del model
    torch.cuda.empty_cache()
    return cache


def paires(articles: dict, langues: list[str], rng: random.Random, n: int):
    arts = list(articles)
    return [(rng.choice(arts), rng.choice(langues), rng.choice(langues)) for _ in range(n)]


# ------------------------------------------------------------------ l'entraînement

def entrainer(articles: dict, val: dict, z: dict, vocab: Vocabulaire, langues: list[str],
              graine: int, pas: int, device, lot: int = 32, lr: float = 1e-3,
              eval_tous: int = 500, contraste: float = 0.0, marge: float = 1.0) -> dict:
    torch.manual_seed(graine)
    rng = random.Random(graine)
    model = DecodeurMots(len(vocab), len(langues)).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=lr)
    historique = []
    for etape in range(1, pas + 1):
        lot_ = paires(articles, langues, rng, lot)
        lot_ = [(a, s, t) for a, s, t in lot_ if s != t]
        if not lot_:
            continue
        zs = torch.stack([z[(a, s)] for a, s, _ in lot_]).to(device)
        langues_t = torch.tensor([vocab.langues[t] for _, _, t in lot_], device=device)
        cibles = [vocab.encode(articles[a][t]) for a, _, t in lot_]
        T = max(len(c) for c in cibles)
        tokens = torch.zeros((len(cibles), T), dtype=torch.long)
        labels = torch.full((len(cibles), T), -100, dtype=torch.long)
        for i, c in enumerate(cibles):
            tokens[i, :len(c)] = torch.tensor([2] + c[:-1])  # <bos> + mots
            labels[i, :len(c)] = torch.tensor(c)
        tokens, labels = tokens.to(device), labels.to(device)
        logits = model(tokens, langues_t, zs)
        perte = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), labels.reshape(-1),
                                ignore_index=-100)
        # Terme contrastif : le décodeur doit préférer le z CORRECT au z d'une autre unité.
        # Sans lui, la langue et le registre suffisent (le z ne porte que ~2 points).
        if contraste > 0:
            zs_melange = zs.roll(1, dims=0)
            logits_s = model(tokens, langues_t, zs_melange)
            perte_s = F.cross_entropy(logits_s.reshape(-1, logits_s.shape[-1]),
                                      labels.reshape(-1), ignore_index=-100)
            perte = perte + contraste * torch.relu(marge - (perte_s - perte.detach()))
        opt.zero_grad()
        perte.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if etape % eval_tous == 0 or etape == pas:
            m = evaluer(model, val, z, vocab, langues, device)
            m.update({"pas": etape, "perte": float(perte.detach()), "graine": graine})
            historique.append(m)
            print(f"  pas {etape:5d} · perte {m['perte']:.3f} · chrF rec {m['chrf_rec']:.1f} / "
                  f"trad {m['chrf_trad']:.1f} / plancher {m['chrf_plancher']:.1f}")
    return {"historique": historique, "model": model}


@torch.no_grad()
def evaluer(model, val: dict, z: dict, vocab: Vocabulaire, langues: list[str],
            device) -> dict:
    model.eval()
    rec, trad, plancher = [], [], []
    for art in val:
        zs = z[(art, SOURCE)].unsqueeze(0).to(device)
        for cible in [SOURCE] + [c for c in CIBLES if c in langues]:
            langue = torch.tensor([vocab.langues[cible]], device=device)
            ids = model.generer(zs, langue)[0].tolist()[1:]
            hyp = vocab.decode(ids)
            ref = " ".join(val[art][cible].split()[:MAX_MOTS])
            src = " ".join(val[art][SOURCE].split()[:MAX_MOTS])
            plancher.append(chrf(src, ref))
            (rec if cible == SOURCE else trad).append(chrf(hyp, ref))
    model.train()
    return {"chrf_rec": sum(rec) / max(1, len(rec)),
            "chrf_trad": sum(trad) / max(1, len(trad)),
            "chrf_plancher": sum(plancher) / max(1, len(plancher))}


@torch.no_grad()
def controles(model, val: dict, z: dict, vocab: Vocabulaire, langues: list[str],
              device) -> dict:
    """Les contrôles du décodeur ENTRAÎNÉ : le z et la langue doivent porter.

    - `z` mélangé : chaque article reçoit le `z` d'un AUTRE article — le chrF doit s'effondrer.
    - langue mélangée : la cible est générée avec la langue d'une AUTRE cible — le chrF doit
      chuter (le décodeur n'a pas appris à ignorer la langue).
    """
    model.eval()
    arts = list(val)
    cibles = [c for c in CIBLES if c in langues]
    z_melange, langue_melangee = [], []
    for i, art in enumerate(arts):
        autre = arts[(i + 1) % len(arts)]
        for cible in cibles:
            ref = " ".join(val[art][cible].split()[:MAX_MOTS])
            zs = z[(autre, SOURCE)].unsqueeze(0).to(device)
            langue = torch.tensor([vocab.langues[cible]], device=device)
            hyp = vocab.decode(model.generer(zs, langue)[0].tolist()[1:])
            z_melange.append(chrf(hyp, ref))
            zs = z[(art, SOURCE)].unsqueeze(0).to(device)
            autre_cible = cibles[(cibles.index(cible) + 1) % len(cibles)]
            langue = torch.tensor([vocab.langues[autre_cible]], device=device)
            hyp = vocab.decode(model.generer(zs, langue)[0].tolist()[1:])
            langue_melangee.append(chrf(hyp, ref))
    model.train()
    return {"chrf_z_melange": sum(z_melange) / max(1, len(z_melange)),
            "chrf_langue_melangee": sum(langue_melangee) / max(1, len(langue_melangee))}


# ------------------------------------------------------------------ les modes

def une_graine(graine: int, pas: int, device, seq: int = 128, contraste: float = 0.0,
               marge: float = 1.0) -> dict:
    langues = CONFIG["langues"]
    articles = CONFIG["module"].charger(langues)
    train, val = CONFIG["module"].decouper(articles)
    vocab = Vocabulaire(train, langues)
    z = etats_encodeur(articles, langues, device, seq)
    debut = time.monotonic()
    resultat = entrainer(train, val, z, vocab, langues, graine, pas, device,
                         contraste=contraste, marge=marge)
    meilleur = max(resultat["historique"], key=lambda m: m["chrf_trad"])
    controles_ = controles(resultat["model"], val, z, vocab, langues, device)
    return {"graine": graine, "meilleur": meilleur, "controles": controles_,
            "historique": resultat["historique"],
            "secondes": round(time.monotonic() - debut, 1),
            "vocabulaire": len(vocab)}


def mesure(chemin: pathlib.Path, pas: int, graines: list[int], corpus: str = "udhr",
           contraste: float = 0.0, marge: float = 1.0) -> int:
    _configurer(corpus)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    resultats = [une_graine(g, pas, device, contraste=contraste, marge=marge)
                 for g in graines]
    trad = [r["meilleur"]["chrf_trad"] for r in resultats]
    rec = [r["meilleur"]["chrf_rec"] for r in resultats]
    plancher = resultats[0]["meilleur"]["chrf_plancher"]
    donnees = {
        "date": "2026-10-29", "ligne": "B10",
        "dispositif": {
            "corpus": ("JW : 139 unités, 5 articles, 11 langues avec espaces (jpn exclu)"
                       if corpus == "jw" else
                       "UDHR 30 articles, 9 langues avec espaces (cmn exclu)"),
            "decoupage": "24 train / 6 validation (articles 25-30)",
            "encodeur": f"{CHECKPOINT} + {ENCODEUR_ENTRAINE} (gelé)",
            "decodeur": "mots : embedding + langue + 2 couches d'attention croisée sur z",
            "pas": pas, "graines": graines, "cibles": CIBLES,
            "contraste": contraste, "marge": marge,
        },
        "resultats": [{"graine": r["graine"], "meilleur": r["meilleur"],
                       "controles": r["controles"],
                       "secondes": r["secondes"], "vocabulaire": r["vocabulaire"]}
                      for r in resultats],
        "controles_moyens": {
            "chrf_z_melange": round(statistics.mean([r["controles"]["chrf_z_melange"]
                                                      for r in resultats]), 2),
            "chrf_langue_melangee": round(statistics.mean(
                [r["controles"]["chrf_langue_melangee"] for r in resultats]), 2)},
        "moyennes": {"chrf_trad": round(statistics.mean(trad), 2),
                     "chrf_rec": round(statistics.mean(rec), 2),
                     "chrf_plancher": round(plancher, 2)},
        "reference_octets": {"chrf_trad": 11.1, "chrf_rec": 17.4, "chrf_plancher": 38.5},
        "verdict": ("l'objectif mot bat l'octet" if statistics.mean(trad) > 11.1 + 1.0
                    else "l'objectif mot ne bat pas l'octet"),
    }
    chemin.write_text(json.dumps(donnees, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"écrit : {chemin}")
    print(json.dumps(donnees["moyennes"], ensure_ascii=False))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="B10 — le décodeur au niveau du mot.")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--pas", type=int, default=3000)
    ap.add_argument("--sortie", default="/tmp/mots-s1")
    ap.add_argument("--corpus", default="udhr", choices=("udhr", "jw"))
    ap.add_argument("--contraste", type=float, default=0.0)
    ap.add_argument("--marge", type=float, default=1.0)
    ap.add_argument("--mesure", type=pathlib.Path)
    ap.add_argument("--graines", default="1,2,3")
    args = ap.parse_args()
    if args.mesure:
        graines = [int(g) for g in args.graines.split(",") if g.strip()]
        return mesure(args.mesure, args.pas, graines, args.corpus,
                      args.contraste, args.marge)
    _configurer(args.corpus)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    r = une_graine(args.graine, args.pas, device, contraste=args.contraste, marge=args.marge)
    pathlib.Path(args.sortie + ".json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"écrit {args.sortie}.json · meilleur {r['meilleur']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

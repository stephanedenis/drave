#!/usr/bin/env python3
"""M2 — deux voies : ventrale (quoi) et dorsale (où/comment).

Un même encodeur de surface alimente deux têtes séparées : l'une lit l'**action**
(voie ventrale), l'autre la **source** `de` (voie dorsale). On peut léser une tête
sans toucher l'autre : c'est la double dissociation minimale.
"""
from __future__ import annotations

import collections
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM

from semantique.entrainer import pad
from semantique.normalisation import normaliser
from semantique.typed_corpus import decouper, items, octets
from semantique.universaux import CHAMPS


class Voies(nn.Module):
    nom = "M2-voies"

    def __init__(self, base: nn.Module):
        super().__init__()
        self.base = base
        self.d_model = int(base.config.hidden_size)
        self.ventral = nn.Linear(self.d_model, 5)      # jeu
        self.dorsal = nn.Linear(self.d_model, 65)      # de (absent + 64 cases)
        self._idx_jeu = {v: i for i, v in enumerate(CHAMPS[0][1])}
        self._idx_de = {v: i for i, v in enumerate(CHAMPS[2][1])}

    def encode(self, ids, masque):
        s = self.base(input_ids=ids, attention_mask=masque, output_hidden_states=True)
        h = s.hidden_states[-1]
        m = masque.unsqueeze(-1).to(h.dtype)
        return (h * m).sum(1) / m.sum(1).clamp(min=1)

    def logits(self, ids, masque):
        h = self.encode(ids, masque)
        return self.ventral(h), self.dorsal(h)


def _lot(items_, lot, seq, rng):
    choix = [rng.choice(items_) for _ in range(lot)]
    return pad([octets(normaliser(i.texte), seq) for i in choix]), choix


def entrainer(base, pas: int = 400, lot: int = 32, seq: int = 64, graine: int = 1,
              device: str = "cuda"):
    rng = random.Random(graine)
    its = items()
    train, val = decouper(its, graine, 0.2)
    train = [i for i in train if i.code["de"] is not None]
    val = [i for i in val if i.code["de"] is not None]
    m = Voies(base).to(device)
    for p in m.base.parameters():
        p.requires_grad = False
    opt = torch.optim.AdamW([{"params": m.ventral.parameters(), "lr": 1e-3},
                             {"params": m.dorsal.parameters(), "lr": 1e-3}])
    ia, ide = m._idx_jeu, m._idx_de
    for etape in range(1, pas + 1):
        (x, masque), choix = _lot(train, lot, seq, rng)
        x, masque = x.to(device), masque.to(device)
        va, vd = m.logits(x, masque)
        cible_a = torch.tensor([ia[c.code["jeu"]] for c in choix], device=device)
        cible_d = torch.tensor([ide[c.code["de"]] for c in choix], device=device)
        perte = F.cross_entropy(va, cible_a) + F.cross_entropy(vd, cible_d)
        opt.zero_grad(); perte.backward(); opt.step()
    return m, val


@torch.no_grad()
def evaluer(m: Voies, val, device: str = "cuda", lese: str | None = None):
    m.eval()
    ok_a = ok_d = 0
    n = 0
    for d in range(0, len(val), 64):
        mor = val[d:d + 64]
        x, masque = pad([octets(normaliser(i.texte), 64) for i in mor])
        va, vd = m.logits(x.to(device), masque.to(device))
        if lese == "ventral":
            va = torch.randn_like(va)
        if lese == "dorsal":
            vd = torch.randn_like(vd)
        pa = va.argmax(1).tolist(); pd = vd.argmax(1).tolist()
        for j, it in enumerate(mor):
            ok_a += int(pa[j] == m._idx_jeu[it.code["jeu"]])
            ok_d += int(pd[j] == m._idx_de[it.code["de"]])
            n += 1
    return {"jeu": ok_a / max(1, n), "de": ok_d / max(1, n), "n": n}

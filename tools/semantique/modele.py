#!/usr/bin/env python3
"""modele.py — l'encodeur sémantique et le décodeur sens→texte du natif.

Le même `route` fait les deux :
- **encodeur** : il lit la surface (octets), et l'état caché du dernier octet est
  projeté en un vecteur `z` de dimension `d_sem`, normalisé ;
- **décodeur** : `z` devient `k` préfixes doux, plus un jeton de **langue cible**,
  et le même `route` génère la texte cible. La langue est dans le décodeur, pas
  dans `z` : c'est la condition pour que `z` soit un sens partagé.

Le protocole n'ajoute donc ni un second modèle ni un tokeniseur : il ajoute une
tête, un préfixe et une table de langues au modèle natif.
"""
from __future__ import annotations

import copy

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM


class RetourInverse(torch.autograd.Function):
    """Identité en avant, gradient inversé en arrière : la langue ne doit pas rester dans z."""
    @staticmethod
    def forward(ctx, x):
        return x

    @staticmethod
    def backward(ctx, g):
        return -g


class Semantique(nn.Module):
    def __init__(self, base: nn.Module, n_langues: int, d_sem: int = 128,
                 k_prefixe: int = 4, deux_bases: bool = False):
        super().__init__()
        self.base = base
        self.base_decode = copy.deepcopy(base) if deux_bases else self.base
        self.d_model = int(base.config.hidden_size)
        self.d_sem = d_sem
        self.k = k_prefixe
        self.tete = nn.Sequential(nn.LayerNorm(self.d_model), nn.Linear(self.d_model, d_sem))
        self.prefixe = nn.Linear(d_sem, k_prefixe * self.d_model)
        self.langue = nn.Embedding(n_langues, self.d_model)
        self.classif_langue = nn.Linear(d_sem, n_langues)

    @classmethod
    def charger(cls, checkpoint: str, n_langues: int, d_sem: int = 128,
                k_prefixe: int = 4, device: str = "cuda", deux_bases: bool = False):
        base = AutoModelForCausalLM.from_pretrained(checkpoint, dtype=torch.float32)
        return cls(base, n_langues, d_sem, k_prefixe, deux_bases).to(device)

    def encode(self, ids: torch.Tensor, masque: torch.Tensor,
               pooling: str = "mean") -> torch.Tensor:
        """ids [B,L], masque [B,L] (1 = vrai octet) -> z [B,d_sem], normalisé.

        Le **mean pooling** est le défaut : prendre le dernier octet d'un article
        tronqué ne voit que sa fin, et deux articles différents se ressemblent.
        Le dernier état reste disponible pour l'A/B (`--pooling last`).
        """
        sortie = self.base(input_ids=ids, attention_mask=masque, output_hidden_states=True)
        h = sortie.hidden_states[-1]
        if pooling == "last":
            longueurs = masque.sum(dim=1).clamp(min=1).long()
            idx = torch.arange(h.shape[0], device=h.device)
            z = h[idx, longueurs - 1]
        else:
            m = masque.unsqueeze(-1).to(h.dtype)
            z = (h * m).sum(dim=1) / m.sum(dim=1).clamp(min=1)
        z = self.tete(z)
        return F.normalize(z, dim=-1)

    def retour_inverse(self, z: torch.Tensor) -> torch.Tensor:
        return RetourInverse.apply(z)

    def _prefixe(self, z: torch.Tensor, langues: torch.Tensor) -> torch.Tensor:
        p = self.prefixe(z).view(z.shape[0], self.k, self.d_model)
        l = self.langue(langues).unsqueeze(1)
        return torch.cat([p, l], dim=1)

    def perte_texte(self, z: torch.Tensor, langues: torch.Tensor,
                    cibles: torch.Tensor, masque_cibles: torch.Tensor) -> torch.Tensor:
        """La perte de génération conditionnée par z et la langue cible.

        `cibles` [B,T] est la suite d'octets cible ; le dernier préfixe prédit le
        premier octet, puis chaque octet prédit le suivant. Les positions de
        remplissage sont masquées.
        """
        B, T = cibles.shape
        P = self.k + 1
        prefixe = self._prefixe(z, langues)
        dec_in = cibles[:, :-1]
        emb_in = self.base_decode.get_input_embeddings()(dec_in)
        emb = torch.cat([prefixe, emb_in], dim=1)
        labels = torch.full((B, emb.shape[1]), -100, dtype=torch.long, device=cibles.device)
        labels[:, P - 1:P - 1 + T] = cibles.masked_fill(masque_cibles == 0, -100)
        attn = torch.cat([
            torch.ones(B, P, dtype=torch.long, device=cibles.device),
            masque_cibles[:, :-1].long(),
        ], dim=1)
        sortie = self.base_decode(inputs_embeds=emb, attention_mask=attn, labels=labels)
        return sortie.loss

    @torch.no_grad()
    def generer(self, z: torch.Tensor, langues: torch.Tensor,
                max_new: int = 128) -> torch.Tensor:
        """Génère les octets cibles à partir de z (greedy)."""
        self.base_decode.eval()
        prefixe = self._prefixe(z, langues)
        attn = torch.ones(prefixe.shape[:2], dtype=torch.long, device=prefixe.device)
        return self.base_decode.generate(
            inputs_embeds=prefixe, attention_mask=attn,
            max_new_tokens=max_new, do_sample=False, eos_token_id=None, pad_token_id=0)

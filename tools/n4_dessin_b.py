#!/usr/bin/env python3
"""n4_dessin_b.py — N4 : les COUCHES BASSES peuvent-elles apprendre à rendre leur état lisible ?

LA QUESTION, ET POURQUOI ELLE SE POSE MAINTENANT. C8 a mesuré que le chemin tronqué à 8 couches,
lu par un **adaptateur de sortie entraîné** sur des couches **gelées**, plafonne à **267,98**
(m32, k = 30 morceaux, tête empruntée 4 481 378,88, modèle complet 7,42) : la courbe monte encore
avec la donnée mais ÷1,4 par doublement, et agrandir l'adaptateur **dégrade** (376,01 pour un
non-linéaire à données égales). L'explication mesurée est dans
`reports/rapport-c8-echelle.md` § 2septies : l'état de profondeur 16 est prédictible à **R² 0,65**
depuis l'état de profondeur 8 par une carte linéaire, mais les **pas élémentaires** le sont mieux
(0,78 · 0,75) — donc **~35 % de la variance profonde est CRÉÉE par les couches intermédiaires**,
et un adaptateur sur un chemin gelé ne peut pas la fabriquer.

D'OÙ LE DESSIN B (`docs/note-chemin-court-n4.md` § 2) : entraîner les couches basses elles-mêmes
(LoRA de rang faible sur q/k/v/o des L premières couches), pour qu'elles produisent un état *plus
lisible*, au lieu de seulement mieux cadrer l'état existant (dessin A). Ici les deux sont mesurés
côte à côte, sur les **mêmes** morceaux, la **même** graine et la **même** validation.

LES CINQ PORTES, ÉCRITES AVANT LE CODE (note § 3) — elles sont imprimées à chaque exécution :
  1. **invariant d'identité** : adaptateur = identité ET LoRA = 0 ⇒ le chemin tronqué rend
     **exactement** la perplexité de la tête empruntée (aucun octet ne change) ;
  2. **le témoin « tête empruntée » reste dans la table** (et le modèle complet aussi) ;
  3. **test sur deux morceaux jamais vus** (m32 et m20 : le morceau de test pèse ×10) ;
  4. **deux graines** au minimum (la graine pèse 0,7 % : en dessous, un gain n'est pas un gain) ;
  5. **l'époque se choisit sur la validation**, jamais sur le test.
  + deux portes de **concordance** (elles valident la chaîne torch contre le MOTEUR, qui est la
  référence du dépôt) : le modèle complet et le chemin tronqué à tête empruntée doivent rendre,
  en torch, les chiffres que `drave` rend sur les mêmes morceaux.

CE QUI N'EST PAS LA MÊME CHOSE QUE LE MOTEUR, ET QUI EST DIT. Les états du moteur viennent d'un
GGUF **Q8_0** ; ici on entraîne sur les poids **fp32** du même modèle (`Qwen2.5-0.5B-Instruct`,
vérifié : les normes du GGUF sont **identiques au bit** à celles de ce dépôt HF, les matrices à
5,5e-3 près, ce qui est l'erreur Q8_0). Les portes de concordance chiffrent cet écart.

CE QUI SUIT, ET QUI EST LA PORTE D'EXÉCUTION (14/10). Ce banc mesure en torch ; pour que le
MOTEUR rende le même verdict, trois commandes (`reports/rapport-n4-porte-execution.md`) :

  # 1. entraîner ET écrire les poids appris
  CUDA_VISIBLE_DEVICES=0 $PY tools/n4_dessin_b.py --profondeur 8 --train 30 --exclure 20 \
      --val 30,31 --test 32,20 --epoques 20 --graine 0 --bras adaptateur,lora,lora+adaptateur \
      --sauver /tmp/n4/poids --json /tmp/n4/exec.json
  # 2. exporter le modèle dense (LoRA fusionné) et le lecteur appris
  $PY tools/exporter_gguf_dense.py --hf <snapshot HF> --lora /tmp/n4/poids-lora_adaptateur.pt \
      --couches-lora 8 --adapter-sortie /tmp/n4/adaptateur.f32 --sortie /tmp/n4/modele.gguf
  # 3. mesurer dans le moteur
  ./drave-core/target/release/drave /tmp/n4/modele.gguf --ppl morceau.txt --limit 1024 --ctx 1024 \
      --threads 8 --couches 0:8 --tete-partielle --adaptateur-sortie /tmp/n4/adaptateur.f32

ATTENTION À LA REPRODUCTIBILITÉ (mesuré le 14/10) : le bras `adaptateur` (états précalculés) rend
le MÊME chiffre d'une exécution à l'autre, mais les bras qui rétropropagent à travers les couches
donnent ÷1,32 · ÷1,46 · ÷1,43 sur m32 à graine fixée — citer un chiffre LoRA avec son étendue.

Usage :
  CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python tools/n4_dessin_b.py \
      --profondeur 8 --train 30 --val 30,31 --test 32,20 --graine 0 --epoques 20 \
      --bras adaptateur,lora,lora+adaptateur --json /tmp/n4/graine0.json
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import subprocess
import time

import numpy as np
import torch
import torch.nn as nn

IDS_DEFAUT = "/tmp/campagne24/ids_0.5B-Q8.txt"
GGUF_DEFAUT = "models/Qwen2.5-0.5B-Q8_0.gguf"
SNAPSHOT_DEFAUT = ("/home/stephane/IA/cache/huggingface/hub/"
                   "models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/"
                   "7ae557604adf67be50417f59c2c2f167def9a775")
# Repères du MOTEUR (drave), lus sur la machine le 2026-10-14, mêmes morceaux :
#   modèle complet   : m32 7,4242 · m20 19,1237
#   tronqué 0:8      : m32 4 481 378,8799 · m20 1 790 749,9836
#   tronqué 0:4      : m32 24 656 438,5178 · m20 8 174 482,8297
REPERES_MOTEUR = {"complet": {"m32": 7.4242, "m20": 19.1237},
                  "tronque4": {"m32": 24656438.5178, "m20": 8174482.8297},
                  "tronque8": {"m32": 4481378.8799, "m20": 1790749.9836}}


# ---------------------------------------------------------------------------------------------
# Les morceaux : exactement le découpage de `tools/c8_corpus.sh` (pas = len/(n+1))
# ---------------------------------------------------------------------------------------------
def decouper(ids: list[int], n: int, taille: int) -> list[list[int]]:
    pas = len(ids) // (n + 1)
    if pas <= taille:
        raise SystemExit(f"corpus trop court : {len(ids)} jetons pour {n} morceaux de {taille}")
    return [ids[i * pas: i * pas + taille] for i in range(n)]


def lire_ids(chemin: str) -> list[int]:
    return [int(x) for x in re.split(r"[,\s]+", pathlib.Path(chemin).read_text()) if x.strip()]


# ---------------------------------------------------------------------------------------------
# Le LoRA : rang faible sur q/k/v/o. B = 0 au départ ⇒ le chemin est EXACTEMENT le modèle de base
# (invariant d'identité, porte 1 : la fonction est la même au bit près, pas « à peu près »).
# ---------------------------------------------------------------------------------------------
class LoraLineaire(nn.Module):
    def __init__(self, base: nn.Linear, rang: int, alpha: float):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad_(False)
        self.A = nn.Parameter(torch.empty(rang, base.in_features))
        self.B = nn.Parameter(torch.zeros(base.out_features, rang))
        nn.init.kaiming_uniform_(self.A, a=math.sqrt(5))
        self.echelle = alpha / rang

    def forward(self, x):
        return self.base(x) + (x @ self.A.T @ self.B.T) * self.echelle


def poser_lora(modele, profondeur: int, rang: int, alpha: float):
    """Remplace q/k/v/o des `profondeur` premières couches par leur version LoRA.

    Rend `(paramètres, fiches)` : la fiche porte le **nom HF** du poids (`model.layers.3.
    self_attn.q_proj.weight`) et l'échelle — c'est ce qui permet à `exporter_gguf_dense.py` de
    FUSIONNER l'adaptateur dans un GGUF (`W ← W + (α/r)·B·A`), c'est-à-dire de rendre le chemin
    court exécutable par le moteur."""
    params, fiches = [], []
    for i in range(profondeur):
        attn = modele.model.layers[i].self_attn
        for nom in ("q_proj", "k_proj", "v_proj", "o_proj"):
            base = getattr(attn, nom)
            lora = LoraLineaire(base, rang, alpha).to(base.weight.device, base.weight.dtype)
            setattr(attn, nom, lora)
            params += [lora.A, lora.B]
            fiches.append({"nom": f"model.layers.{i}.self_attn.{nom}.weight",
                           "A": lora.A, "B": lora.B, "echelle": lora.echelle})
    return params, fiches


# ---------------------------------------------------------------------------------------------
# L'entraînement et la mesure
# ---------------------------------------------------------------------------------------------
class Banc:
    def __init__(self, a):
        from transformers import AutoModelForCausalLM
        t0 = time.time()
        self.m = AutoModelForCausalLM.from_pretrained(a.modele, dtype=torch.float32)
        self.m.eval()
        for p in self.m.parameters():
            p.requires_grad_(False)
        self.dev = "cuda" if torch.cuda.is_available() else "cpu"
        self.m.to(self.dev)
        self.toutes = list(self.m.model.layers)          # les 24 couches, dans l'ordre
        self.L = a.profondeur
        self.liste_tronquee = nn.ModuleList(self.toutes[:self.L])
        self.liste_pleine = self.m.model.layers
        self.tete = self.m.lm_head.weight                # LIÉE à l'embedding (tie_word_embeddings)
        self.lora_params, self.lora_specs = (poser_lora(self.m, self.L, a.rang, a.alpha)
                                             if a.rang > 0 else ([], []))
        print(f"modèle {a.modele.split('/')[-3]} · {len(self.toutes)} couches · troncature à {self.L} "
              f"· LoRA rang {a.rang} sur {len(self.lora_params) // 2} projections "
              f"({sum(p.numel() for p in self.lora_params):,} paramètres) · {self.dev} "
              f"· chargé en {time.time() - t0:.1f} s")
        self.initial_lora = [p.detach().clone() for p in self.lora_params]
        # L'ÉTAT BRUT, CAPTURÉ PAR UN CROCHET. `output_hidden_states` ne le donne PAS pour un
        # modèle tronqué : la liste se termine par l'état **après la norme finale** (la norme est
        # appliquée en fin de boucle, et un modèle à L couches a L+1 entrées dont la dernière est
        # normée). Prendre `hidden_states[L]` rendait donc un état NORMÉ, que l'adaptateur
        # normalisait une seconde fois : la porte 1 l'a attrapé (18 774 866 au lieu de
        # 4 476 128, un facteur 4,19 — sans elle, ce bug aurait été publié comme un résultat).
        self._etat: dict = {}

        def crochet(_module, _entree, sortie):
            self._etat["x"] = sortie[0] if isinstance(sortie, tuple) else sortie

        self.liste_tronquee[-1].register_forward_hook(crochet)

    # ---- le chemin tronqué : `norme(état_L) · tête liée`, exactement la chaîne du moteur ----
    def _tronque(self, ids: torch.Tensor, grad: bool) -> torch.Tensor:
        self.m.model.layers = self.liste_tronquee
        ctx = torch.enable_grad() if grad else torch.no_grad()
        with ctx:
            out = self.m(ids, use_cache=False)
            return out.logits

    def _complet(self, ids: torch.Tensor) -> torch.Tensor:
        self.m.model.layers = self.liste_pleine
        with torch.no_grad():
            return self.m(ids, use_cache=False).logits

    def _brut(self, ids: torch.Tensor):
        """Le forward tronqué, et l'état brut (avant norme) laissé par le crochet."""
        self.m.model.layers = self.liste_tronquee
        self.m(ids, use_cache=False)
        return self._etat["x"]

    def etat_tronque(self, ids: torch.Tensor) -> torch.Tensor:
        """L'état de profondeur L AVANT la norme finale — ce que le moteur écrit."""
        with torch.no_grad():
            return self._brut(ids)

    @torch.no_grad()
    def accord(self, morceaux, logits_fn) -> float:
        """L'ACCORD avec le maître : la fraction de positions où le chemin court choisit le MÊME
        jeton que le modèle complet. C'est la mesure qui manquait — un étudiant peut être bon en
        perplexité et répondre autre chose (mesuré : 0 jeton sur 96 en génération)."""
        justes, n = 0, 0
        for ids in morceaux:
            etudiant = logits_fn(ids)[:, 4:-1].argmax(-1)
            maitre = self._complet(ids)[:, 4:-1].argmax(-1)
            justes += int((etudiant == maitre).sum())
            n += etudiant.numel()
        return justes / max(n, 1)

    # ---- perplexité sur les positions 4.. : la convention du moteur (--etat-pos commence à 4) ----
    # La perte se calcule LIGNE PAR LIGNE : un lot de k morceaux concaténés n'est pas une seule
    # séquence — la dernière position d'un morceau ne prédit pas la première du suivant, et
    # l'attention ne traverse pas la frontière (chaque ligne est une séquence à part entière).
    def ppl(self, morceaux: list[torch.Tensor], logits_fn, debut=4) -> float:
        nll, n = 0.0, 0
        with torch.no_grad():
            for ids in morceaux:
                logits = logits_fn(ids)
                for r in range(logits.shape[0]):
                    perte = nn.functional.cross_entropy(logits[r, debut:-1].float(),
                                                        ids[r, debut + 1:], reduction="sum")
                    nll += float(perte)
                    n += len(ids[r]) - debut - 1
        return float(np.exp(nll / max(n, 1)))


def entrainer(banc: Banc, bras: str, train, val, tests, a) -> dict:
    """Entraîne UN bras et rend ses perplexités. Chaque bras part du même modèle, de la même
    graine et de la même validation : la comparaison est appariée.

    DEUX BOUCLES, PARCE QUE LES DEUX DESSINS N'ONT PAS LES MÊMES GRADIENTS.

    * **dessin A** (adaptateur seul, couches gelées) : les états ne bougent pas — ils sont donc
      calculés UNE fois, et l'adaptateur s'entraîne sur des lots de 256 états, c'est-à-dire le
      **protocole publié** (`c8_entrainer_tete.py` : lots de 256, Adam 1e-2, époque choisie sur la
      validation). C'est ce qui rend la comparaison avec le 267,98 de
      `reports/rapport-c8-echelle.md` (§ 2bis, profondeur 8) légitime ;
    * **dessins B et A+B** : le gradient doit traverser les couches — les lots sont des
      **morceaux** (1 019 positions chacun) et l'adaptateur, quand il est là, apprend avec le même
      pas que le LoRA. Entraîner l'adaptateur à 1e-2 sur des lots de 2 048 états le faisait
      **diverger** (4,48 M → 2,9e13 en deux pas, mesuré le 14/10) : son pas est celui du protocole
      publié quand il est seul, plus petit quand il apprend en même temps que les couches.
    """
    torch.manual_seed(a.graine)
    np.random.seed(a.graine)
    dev = banc.dev
    avec_lora = "lora" in bras
    for p, init in zip(banc.lora_params, banc.initial_lora):
        p.data.copy_(init)
        p.requires_grad_(avec_lora)
    adaptateur = (nn.Parameter(torch.eye(banc.tete.shape[1], device=dev, dtype=torch.float32))
                  if "adaptateur" in bras else None)

    def tete_logits(x):
        z = (x @ adaptateur.T).float() if adaptateur is not None else x
        return banc.m.model.norm(z) @ banc.tete.T

    def instantane():
        return {"adaptateur": None if adaptateur is None else adaptateur.detach().clone(),
                "lora": [p.detach().clone() for p in banc.lora_params] if avec_lora else None}

    def tenseurs():
        """Les poids APPRIS, prêts pour l'export (noms HF + échelle pour la fusion)."""
        return {"adaptateur": None if adaptateur is None else adaptateur.detach().cpu(),
                "lora": ([{"nom": f["nom"], "A": f["A"].detach().cpu(), "B": f["B"].detach().cpu(),
                           "echelle": f["echelle"]} for f in banc.lora_specs]
                         if avec_lora else [])}

    def restaurer(snap):
        if adaptateur is not None:
            adaptateur.data.copy_(snap["adaptateur"])
        if snap["lora"] is not None:
            for p, v in zip(banc.lora_params, snap["lora"]):
                p.data.copy_(v)

    # ================================ dessin A : états gelés ================================
    if adaptateur is not None and not avec_lora:
        def empiler(morceaux):
            Xs, Ys = [], []
            with torch.no_grad():
                for ids in morceaux:
                    x = banc.etat_tronque(ids)[0]                 # [taille, 896], état BRUT
                    Xs.append(x[4:-1])                            # positions 4.. : convention moteur
                    Ys.append(ids[0, 5:])
            return torch.cat(Xs).contiguous(), torch.cat(Ys)

        Xtr, ytr = empiler(train)
        Xva, yva = empiler(val)
        Xte = {nom: empiler(ms) for nom, ms in tests}

        def ppl_etats(X, y) -> float:
            nll, n = 0.0, 0
            with torch.no_grad():
                for d in range(0, len(y), 512):
                    logits = tete_logits(X[d:d + 512]).float()
                    nll += float(nn.functional.cross_entropy(logits, y[d:d + 512],
                                                             reduction="sum"))
                    n += len(y[d:d + 512])
            return float(np.exp(nll / max(n, 1)))

        opt = torch.optim.Adam([adaptateur], lr=a.pas_adaptateur)
        ppl_depart_val = ppl_etats(Xva, yva)
        ppl_depart = ppl_etats(*Xte[tests[0][0]])
        # CONSOLIDATION (C7) : le modèle COMPLET, avant tout pas — c'est le « avant » du rejeu, et il
        # ne dépend pas du bras (mêmes poids de départ).
        plein_avant = ({n: banc.ppl(ms, banc._complet) for n, ms in tests}
                                   if getattr(a, "eval_plein", False) else None)
        meilleur = (ppl_depart_val, 0, instantane())
        journal = []
        for e in range(a.epoques):
            perm = torch.randperm(len(ytr), device=dev)
            tot, n = 0.0, 0
            for d in range(0, len(perm), a.lots_etats):
                idx = perm[d:d + a.lots_etats]
                opt.zero_grad()
                logits = tete_logits(Xtr[idx]).float()
                l = nn.functional.cross_entropy(logits, ytr[idx])
                l.backward()
                opt.step()
                tot += float(l.detach()) * len(idx)
                n += len(idx)
            ppl_val = ppl_etats(Xva, yva)
            marque = ""
            if ppl_val < meilleur[0]:
                meilleur = (ppl_val, e + 1, instantane())
                marque = "  ← meilleur (validation)"
            journal.append({"epoque": e + 1, "perte_train": float(np.exp(tot / max(n, 1))),
                            "val": ppl_val})
            if e == 0 or (e + 1) % max(1, a.epoques // 10) == 0 or marque:
                print(f"    époque {e + 1:>3}/{a.epoques} · train "
                      f"{np.exp(tot / max(n, 1)):>12,.2f} · validation {ppl_val:>12,.2f}{marque}")
        restaurer(meilleur[2])
        res = {"bras": bras, "epoque": meilleur[1], "val": meilleur[0],
               "val_depart": ppl_depart_val, "test_depart_premier": ppl_depart,
               "journal": journal, "train": ppl_etats(Xtr, ytr), "tenseurs": tenseurs()}
        if accord_avant is not None:
            res["accord_avant"] = accord_avant
            res["accord"] = {n: banc.accord(ms, lambda ids: logits_chemin(ids, False))
                             for n, ms in tests}
        for nom, (X, y) in Xte.items():
            res[nom] = ppl_etats(X, y)
        if plein_avant is not None:
            res["plein_avant"] = plein_avant
            res["plein_apres"] = {n: banc.ppl(ms, banc._complet) for n, ms in tests}
        return res

    # ========================= dessins B et A+B : à travers les couches =========================
    plein_obj = getattr(a, "objectif", "tronque") == "plein"
    distiller = getattr(a, "distiller", False)

    def logits_chemin(ids, grad=False):
        if plein_obj:
            # Consolidation : l'objectif est le MODÈLE COMPLET — la perte du cerveau entier, et la
            # rétropropagation traverse les 24 couches (l'adaptateur de sortie, lui, ne joue pas :
            # il n'existe que sur un chemin tronqué).
            if grad:
                banc.m.model.layers = banc.liste_pleine
                return banc.m(ids, use_cache=False).logits
            return banc._complet(ids)
        if grad:
            return tete_logits(banc._brut(ids))
        with torch.no_grad():
            return tete_logits(banc.etat_tronque(ids))

    def perte_morceaux(lot):
        logits = logits_chemin(lot, grad=True)
        if distiller:
            # E5 — DISTILLATION : la cible n'est plus le jeton suivant, c'est la DISTRIBUTION du
            # maître (le modèle complet, gelé). Sans cela, un étudiant peut être excellent en
            # perplexité et répondre autre chose : mesuré le 15/10, **0 jeton sur 96** partagé
            # avec le maître en génération.
            with torch.no_grad():
                logits_maitre = banc._complet(lot)[:, 4:-1].float() / a.temperature
            etudiant = logits[:, 4:-1].float() / a.temperature
            kl = nn.functional.kl_div(
                nn.functional.log_softmax(etudiant, dim=-1),
                nn.functional.softmax(logits_maitre, dim=-1), reduction="batchmean")
            if a.melange <= 0.0:
                return kl
            # E5 bis — le MÉLANGE : garder la cible dure (le jeton) en plus de la distribution du
            # maître. La fiche E5 a montré que la distillation pure fait ×1,8 sur l'accord et coûte
            # ×3,2 de perplexité ; le mélange est la façon classique de payer les deux.
            logits_bruts = logits[:, 4:-1].float()
            ce = nn.functional.cross_entropy(
                logits_bruts.reshape(-1, logits_bruts.shape[-1]), lot[:, 5:].reshape(-1))
            return kl + a.melange * ce
        cibles = lot[:, 5:].reshape(-1)
        return nn.functional.cross_entropy(
            logits[:, 4:-1].reshape(-1, logits.shape[-1]).float(), cibles)

    groupes = []
    if adaptateur is not None:
        groupes.append({"params": [adaptateur], "lr": a.pas_adaptateur_joint})
    groupes.append({"params": banc.lora_params, "lr": a.pas_lora})
    opt = torch.optim.Adam(groupes)

    ppl_depart_val = banc.ppl(val, lambda ids: logits_chemin(ids, False))
    ppl_depart = banc.ppl(tests[0][1], lambda ids: logits_chemin(ids, False))
    accord_avant = ({n: banc.accord(ms, lambda ids: logits_chemin(ids, False))
                     for n, ms in tests} if a.accord else None)
    # CONSOLIDATION (C7) : le modèle COMPLET, avant tout pas — c'est le « avant » du rejeu, et il
    # ne dépend pas du bras (mêmes poids de départ).
    plein_avant = ({n: banc.ppl(ms, banc._complet) for n, ms in tests}
                   if getattr(a, "eval_plein", False) else None)
    meilleur = (ppl_depart_val, 0, instantane())
    journal = []
    for e in range(a.epoques):
        ordre = torch.randperm(len(train), device=dev)
        tot, n = 0.0, 0
        for d in range(0, len(ordre), a.lots):
            idx = ordre[d:d + a.lots]
            lot = torch.cat([train[i] for i in idx], dim=0)
            opt.zero_grad()
            l = perte_morceaux(lot)
            l.backward()
            opt.step()
            ntok = lot.shape[0] * (lot.shape[1] - 5)
            tot += float(l.detach()) * ntok
            n += ntok
        ppl_val = banc.ppl(val, lambda ids: logits_chemin(ids, False))
        marque = ""
        if ppl_val < meilleur[0]:
            meilleur = (ppl_val, e + 1, instantane())
            marque = "  ← meilleur (validation)"
        journal.append({"epoque": e + 1, "perte_train": float(np.exp(tot / max(n, 1))),
                        "val": ppl_val})
        if e == 0 or (e + 1) % max(1, a.epoques // 10) == 0 or marque:
            print(f"    époque {e + 1:>3}/{a.epoques} · train (perplexité équivalente) "
                  f"{np.exp(tot / max(n, 1)):>12,.2f} "
                  f"· validation {ppl_val:>12,.2f}{marque}")

    restaurer(meilleur[2])
    res = {"bras": bras, "epoque": meilleur[1], "val": meilleur[0],
           "val_depart": ppl_depart_val, "test_depart_premier": ppl_depart,
           "journal": journal, "tenseurs": tenseurs(),
           "train": banc.ppl(train, lambda ids: logits_chemin(ids, False))}
    if accord_avant is not None:
        res["accord_avant"] = accord_avant
        res["accord"] = {n: banc.accord(ms, lambda ids: logits_chemin(ids, False))
                         for n, ms in tests}
    for nom, morceaux in tests:
        res[nom] = banc.ppl(morceaux, lambda ids: logits_chemin(ids, False))
    if plein_avant is not None:
        res["plein_avant"] = plein_avant
        res["plein_apres"] = {n: banc.ppl(ms, banc._complet) for n, ms in tests}
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default=SNAPSHOT_DEFAUT)
    ap.add_argument("--ids", default=IDS_DEFAUT)
    ap.add_argument("--morceaux", type=int, default=33)
    ap.add_argument("--taille", type=int, default=1024)
    ap.add_argument("--profondeur", type=int, default=8)
    ap.add_argument("--train", type=int, default=30,
                    help="nombre de morceaux d'entraînement (les premiers : m0..m{k-1})")
    ap.add_argument("--rejeu", default="",
                    help="LISTE explicite des morceaux rejoués (ex. « 0,1,2 ») : c'est le protocole "
                         "de SOMMEIL — à volume égal, ce qu'on rejoue compte-t-il ?")
    ap.add_argument("--exclure", default="",
                    help="morceaux à RETIRER de l'entraînement (ex. 20) : un morceau de test qui "
                         "tombe dans la plage d'entraînement n'est PAS « jamais vu » — c'est le "
                         "piège qui a fait publier 17,35 sur m20 le 13/10")
    ap.add_argument("--val", default="30,31")
    ap.add_argument("--test", default="32,20")
    ap.add_argument("--graine", type=int, default=0)
    ap.add_argument("--epoques", type=int, default=20)
    ap.add_argument("--rang", type=int, default=8)
    ap.add_argument("--alpha", type=float, default=16.0)
    ap.add_argument("--pas-adaptateur", type=float, default=1e-2)
    ap.add_argument("--pas-lora", type=float, default=1e-3)
    ap.add_argument("--lots", type=int, default=2, help="morceaux par lot (dessins B et A+B)")
    ap.add_argument("--lots-etats", type=int, default=256,
                    help="états par lot pour le dessin A (256 = le protocole publié)")
    ap.add_argument("--pas-adaptateur-joint", type=float, default=1e-3,
                    help="pas de l'adaptateur quand il apprend EN MÊME TEMPS que les couches")
    ap.add_argument("--bras", default="adaptateur,lora,lora+adaptateur")
    ap.add_argument("--json", default=None)
    ap.add_argument("--sauver", default=None,
                    help="préfixe : écrire les poids APPRIS de chaque bras (PREFIXE-<bras>.pt) "
                         "pour que l'exporteur GGUF les fusionne")
    ap.add_argument("--etat-moteur", default=None,
                    help="préfixe d'états capturés par le moteur (--etat-sortie) pour vérifier "
                         "que l'état BRUT de la chaîne torch est celui du moteur")
    ap.add_argument("--hors", default=None,
                    help="fichier d'identifiants d'un AUTRE corpus : un morceau de `--taille` "
                         "jetons y est pris à `--hors-debut` et sert de test HORS DOMAINE "
                         "(la consolidation en domaine ne dit pas ce qu'elle fait ailleurs)")
    ap.add_argument("--hors-debut", type=int, default=0)
    ap.add_argument("--hors-nom", default="hors")
    ap.add_argument("--melanger-rejeu", action="store_true",
                    help="CONTRÔLE : mélanger l'ordre des jetons des morceaux REJOUÉS (même "
                         "volume, même vocabulaire, plus de séquence) — si la consolidation "
                         "améliore encore, ce n'est pas de l'apprentissage")
    ap.add_argument("--objectif", choices=["tronque", "plein"], default="tronque",
                    help="sur quoi le LoRA apprend : le chemin TRONQUÉ (défaut, c'est N4) ou le "
                         "MODÈLE COMPLET (c'est la consolidation C7 : on consolide le cerveau "
                         "entier, pas un réflexe)")
    ap.add_argument("--distiller", action="store_true",
                    help="E5 : l'objectif devient la DISTILLATION — le chemin court doit reproduire la "
                         "distribution du MODÈLE COMPLET (KL), pas prédire le texte. C'est la "
                         "réponse au constat du 15/10 : entraîné à la perplexité, le réflexe ne "
                         "partage AUCUN jeton avec le cerveau (0/96 en génération)")
    ap.add_argument("--temperature", type=float, default=1.0, help="température de distillation")
    ap.add_argument("--melange", type=float, default=0.0,
                    help="E5 bis : perte = KL + melange × CE. La question ouverte de la fiche E5 : "
                         "gagner l'ACCORD (distillation) sans perdre la PERPLEXITÉ (texte)")
    ap.add_argument("--accord", action="store_true",
                    help="mesurer l'ACCORD avec le maître (fraction de positions où le chemin "
                         "court choisit le même jeton que le modèle complet), avant et après")
    ap.add_argument("--eval-plein", action="store_true",
                    help="mesurer aussi la perplexité du MODÈLE COMPLET (avant et après chaque "
                         "bras) sur les morceaux de test et de validation : c'est la mesure de "
                         "CONSOLIDATION (plan cerveau, C7 : « la perplexité baisse-t-elle sur un "
                         "jeu NON rejoué ? »)")
    ap.add_argument("--sans-portes", action="store_true",
                    help="sauter les portes de concordance (déjà mesurées)")
    a = ap.parse_args()

    # UN PRÉREQUIS DANS /tmp EST RÉGÉNÉRÉ, JAMAIS SUPPOSÉ (règle du 12/10, `tools/_corpus.sh`) :
    # le corpus est `data/wikitext2_test.txt` tokenisé par le modèle — identique au bit près.
    if not pathlib.Path(a.ids).exists():
        if a.ids != IDS_DEFAUT:
            raise SystemExit(f"{a.ids} absent (seul le chemin par défaut est régénérable)")
        moteur = pathlib.Path("drave-core/target/release/drave")
        if not (moteur.exists() and pathlib.Path(GGUF_DEFAUT).exists()):
            raise SystemExit(f"{a.ids} absent ET non régénérable ({moteur} ou {GGUF_DEFAUT} "
                             f"manquant) — lancer depuis la racine du dépôt")
        print(f"corpus {a.ids} absent — régénéré depuis data/wikitext2_test.txt (comme les portes)")
        pathlib.Path(a.ids).parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(moteur), GGUF_DEFAUT, "--tokenize",
                        "--fichier", "data/wikitext2_test.txt", "--sortie", a.ids], check=True)
    ids = lire_ids(a.ids)
    morceaux = decouper(ids, a.morceaux, a.taille)
    idx_val = [int(x) for x in a.val.split(",")]
    idx_test = [(f"m{int(x)}", [int(x)]) for x in a.test.split(",")]
    exclus = {int(x) for x in a.exclure.split(",") if x.strip()}
    if a.rejeu:
        train_idx = [int(x) for x in a.rejeu.split(",") if x.strip()]
    else:
        train_idx = [i for i in range(a.train) if i not in exclus]
    print(f"corpus {len(ids)} jetons · {a.morceaux} morceaux de {a.taille} · "
          f"entraînement {'m' + ',m'.join(str(i) for i in train_idx) if a.rejeu else f'm0..m{a.train - 1}'}"
          + (f" MOINS {sorted(exclus)}" if exclus else "")
          + f" ({len(train_idx)} morceaux) · validation {a.val} · test "
          f"{', '.join(n for n, _ in idx_test)} (jamais vus)")

    banc = Banc(a)
    T = lambda l: [torch.tensor([m], device=banc.dev) for m in l]      # noqa: E731
    if a.melanger_rejeu:
        g = np.random.default_rng(a.graine)
        melanges = [list(g.permutation(morceaux[i])) for i in train_idx]
        print("  ⚠ rejeu MÉLANGÉ (contrôle) : l'ordre des jetons des morceaux rejoués est détruit")
    else:
        melanges = [morceaux[i] for i in train_idx]
    train = T(melanges)
    val = T([morceaux[i] for i in idx_val])
    tests = [(nom, T([morceaux[i] for i in idxs])) for nom, idxs in idx_test]
    if a.hors:
        ids_hors = lire_ids(a.hors)
        debut = a.hors_debut
        if debut + a.taille > len(ids_hors):
            raise SystemExit(f"{a.hors} : {len(ids_hors)} jetons, il en faut {a.taille} à partir "
                             f"de {debut}")
        morceau_hors = ids_hors[debut:debut + a.taille]
        tests.append((a.hors_nom, T([morceau_hors])))
        print(f"  test HORS DOMAINE « {a.hors_nom} » : {a.hors} jetons {debut}..{debut + a.taille}")

    for nom, idxs in idx_test:
        if idxs[0] in train_idx:
            print(f"  ⚠ FUITE : {nom} est dans la plage d'entraînement — son chiffre ne sera pas "
                  f"un chiffre « jamais vu » (utiliser --exclure {idxs[0]})")
    resultats = {"graine": a.graine, "profondeur": a.profondeur, "rang": a.rang,
                 "morceaux": a.morceaux, "train": a.train, "exclus": sorted(exclus),
                 "val": a.val, "test": a.test, "bras": {}}

    print("\n== Portes de concordance : la chaîne torch contre le MOTEUR ==")
    ppl_complet = {nom: banc.ppl(ms, banc._complet) for nom, ms in tests}
    for nom, v in ppl_complet.items():
        ref = REPERES_MOTEUR["complet"].get(nom)
        if ref:
            print(f"  modèle complet {nom} : moteur {ref:,.4f} · torch {v:,.4f} "
                  f"(écart {100 * (v - ref) / ref:+.2f} %)")
            resultats.setdefault("concordance_complet", {})[nom] = [ref, v]
        else:
            print(f"  modèle complet {nom} : torch {v:,.4f} (pas de repère moteur)")
    ppl_empruntee = {nom: banc.ppl(ms, lambda x: banc._tronque(x, False)) for nom, ms in tests}
    for nom, v in ppl_empruntee.items():
        ref = REPERES_MOTEUR.get(f"tronque{a.profondeur}", {}).get(nom)
        if ref:
            print(f"  tronqué {a.profondeur} couches, tête empruntée {nom} : moteur {ref:,.4f} · "
                  f"torch {v:,.4f} (écart {100 * (v - ref) / ref:+.2f} %)")
            resultats.setdefault("concordance_tronque", {})[nom] = [ref, v]
        else:
            print(f"  tronqué {a.profondeur} couches, tête empruntée {nom} : torch {v:,.4f}")

    if a.etat_moteur:
        ms = tests[0][1][0]
        x = banc.etat_tronque(ms)[0].cpu().numpy()
        base = pathlib.Path(a.etat_moteur)
        cos = []
        for pos in range(4, a.taille):
            f = base.parent / f"{base.name}.{pos}"
            if not f.exists():
                continue
            v = np.frombuffer(f.read_bytes(), dtype="<f4")
            cos.append(float(x[pos] @ v / (np.linalg.norm(x[pos]) * np.linalg.norm(v) + 1e-12)))
        if cos:
            print(f"  état BRUT de profondeur {a.profondeur}, {len(cos)} positions du morceau "
                  f"{idx_test[0][0]} : cos min {min(cos):.5f} · médian {np.median(cos):.5f} · "
                  f"max {max(cos):.5f} (le moteur lit du Q8_0, la chaîne torch de l'fp32)")
            resultats["concordance_etat"] = {"n": len(cos), "cos_min": min(cos),
                                             "cos_median": float(np.median(cos))}
        else:
            print(f"  ⚠ --etat-moteur {a.etat_moteur} : aucun état lisible")

    print(f"\n== Les bras (profondeur {a.profondeur} sur {len(banc.toutes)} couches, "
          f"{a.train} morceaux d'entraînement, graine {a.graine}) ==")
    resultats["empruntee"] = ppl_empruntee
    resultats["complet"] = ppl_complet
    for bras in [b for b in a.bras.split(",") if not (a.rang <= 0 and "lora" in b)]:
        print(f"\n  --- bras « {bras} » ---")
        r = entrainer(banc, bras, train, val, tests, a)
        # porte 1 : à l'époque 0 (aucun pas encore fait), la perplexité doit être CELLE de la
        # tête empruntée — l'écart est imprimé, il doit être 0,00e0
        ecart = abs(r["test_depart_premier"] - ppl_empruntee[idx_test[0][0]])
        rel = ecart / ppl_empruntee[idx_test[0][0]]
        print(f"    porte 1 (invariant d'identité, avant tout pas) : "
              f"{r['test_depart_premier']:,.4f} contre {ppl_empruntee[idx_test[0][0]]:,.4f} "
              f"⇒ écart {rel:.2e}")
        r["invariant_identite"] = rel
        if a.sauver:
            import torch as _t
            chemin = f"{a.sauver}-{bras.replace('+', '_')}.pt"
            _t.save({"bras": bras, "graine": a.graine, "profondeur": a.profondeur,
                     "rang": a.rang, "alpha": a.alpha, "epoque": r["epoque"],
                     "val": r["val"], "m32": r["m32"], "m20": r["m20"],
                     "adaptateur": r["tenseurs"]["adaptateur"], "lora": r["tenseurs"]["lora"]},
                    chemin)
            print(f"    poids écrits : {chemin}")
        del r["tenseurs"]
        resultats["bras"][bras] = r

    noms = [n for n, _ in idx_test]
    entete = " | ".join(f"TEST {n}" for n in noms)
    print(f"\n| bras | époque (validation) | validation {a.val} | {entete} |")
    print("|---|---:|---:|" + "---:|" * len(noms))

    def ligne(etiquette: str, epoque: str, validation: str, ppl: dict) -> str:
        return f"| {etiquette} | {epoque} | {validation} | " + \
               " | ".join(f"{ppl[k]:,.4f}" for k in noms) + " |"

    print(ligne("**modèle complet** (référence)", "—", "—", ppl_complet))
    print(ligne("chemin tronqué, tête **empruntée**", "—", "—", ppl_empruntee))
    for bras, r in resultats["bras"].items():
        print(ligne(f"`{bras}`", str(r["epoque"]), f"{r['val']:,.4f}", r))
    if a.accord:
        print("\n| accord avec le maître (positions 4..) | " + " | ".join(noms) + " |")
        print("|---|" + "---:|" * len(noms))
        for bras, r in resultats["bras"].items():
            if "accord" in r:
                print(f"| après `{bras}` | " + " | ".join(
                    f"**{r['accord'][k] * 100:.1f} %** (avant {r['accord_avant'][k] * 100:.1f} %)"
                    for k in noms) + " |")
    if a.eval_plein:
        print("\n| modèle COMPLET (consolidation) | avant | — | " +
              " | ".join(f"{r['plein_avant'][k]:,.4f}" for k in noms) + " |")
        for bras, r in resultats["bras"].items():
            cellules = []
            for k in noms:
                av, ap = r["plein_avant"][k], r["plein_apres"][k]
                cellules.append(f"{ap:,.4f} ({100 * (ap - av) / av:+.2f} %)")
            print(f"| après `{bras}` | — | — | " + " | ".join(cellules) + " |")

    if a.json:
        pathlib.Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.json).write_text(json.dumps(resultats, indent=1, ensure_ascii=False))
        print(f"\nrésultats écrits dans {a.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

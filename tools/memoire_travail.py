#!/usr/bin/env python3
"""memoire_travail.py — N5 : le MODÈLE peut-il APPRENDRE à retenir ?

LE MANQUE, TEL QU'IL EST MESURÉ. `reports/rapport-c8-peripherie.md` § 2 bis, sur 4 096 pas d'un
signal de bruit injecté dans un canal (`drave --entree signal:F --recurent`) : une lecture — même
non linéaire — retrouve le signal **courant** (R² **+0,992**) mais **pas** celui d'il y a 8 pas
(R² **−0,681**) ; une **ligne à retard** le rend exactement (R² **1,000**, zéro paire). La
conclusion de la fiche est explicite : « le modèle n'a jamais été entraîné à retenir un scalaire
injecté, donc il ne le retient pas. La suite est un **entraînement** ». C'est ce fichier.

LE PROTOCOLE EST CELUI DE LA CAMPAGNE (sinon les chiffres ne se comparent pas) :

  · un **jeton de base** fixe, et `L` pas ; à chaque pas, le signal `v[t]` est posé sur UN canal de
    l'embarquement — c'est `--entree signal:F --entree-canal C --entree-gain G --recurent` ;
  · la sonde apprend sur la **première moitié** d'une séquence et se mesure sur la **seconde** ;
  · trois cibles, dont un **témoin** : `v[t]` (le présent, doit rester lisible), `v[t−k]` (la
    mémoire — c'est la question), `v[t+1]` (l'avenir, doit rester illisible, sinon ça fuit).

TROIS BRAS, ET UN CONTRÔLE :

  * **gelé** : sonde seule sur le modèle non entraîné → doit reproduire ≈ −0,68 (chiffre publié) ;
  * **entraîné** : LoRA (rang faible sur q/k/v/o) + sonde appris **ensemble** → le réseau a le
    droit de changer pour rendre le passé lisible ;
  * **contrôle** : cibles de la mémoire **mélangées** — une sonde qui « retrouve » un signal
    mélangé ne mesure rien ;
  * **référence haute** : le **tampon** (`--entree-memoire`, canaux suivants) donne R² 1,000 pour
    **zéro paire** — un entraînement qui l'égale est donc inutile, et c'est la comparaison qui
    décide du mécanisme le plus efficient pour cette faculté.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/memoire_travail.py --sequences 4 --pas 1024 --retard 8 \\
      --epoques 6 [--tampon] [--json f.json] [--sauver lora.pt]
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib

import numpy as np
import torch
import torch.nn as nn

SNAPSHOT_DEFAUT = ("/home/stephane/IA/cache/huggingface/hub/"
                   "models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/"
                   "7ae557604adf67be50417f59c2c2f167def9a775")


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


def poser_lora(modele, couches: int, rang: int, alpha: float):
    params = []
    for i in range(couches):
        attn = modele.model.layers[i].self_attn
        for nom in ("q_proj", "k_proj", "v_proj", "o_proj"):
            base = getattr(attn, nom)
            lora = LoraLineaire(base, rang, alpha).to(base.weight.device, base.weight.dtype)
            setattr(attn, nom, lora)
            params += [lora.A, lora.B]
    return params


def r2(prev, cible) -> float:
    prev = np.asarray(prev, dtype=np.float64)
    cible = np.asarray(cible, dtype=np.float64)
    return float(1.0 - ((cible - prev) ** 2).sum() / (((cible - cible.mean()) ** 2).sum() + 1e-12))


def ridge(Xtr, ytr, Xte):
    """La sonde LINÉAIRE de la campagne (`tools/peripherie_memoire.py`) : moindres carrés
    régularisés, entrées standardisées, solution FERMÉE.

    POURQUOI ELLE ET PAS ADAM. Le premier essai de cet outil ajustait la sonde par Adam, sans
    standardiser, et rendait **−0,11 pour le signal PRÉSENT** là où la campagne publie **+0,992** :
    ce n'était pas le modèle, c'était la sonde. Avec la solution fermée sur les mêmes états, le
    présent rend **+0,991** (mesuré) — donc la comparaison avec les chiffres publiés est légitime.
    """
    Xtr = np.asarray(Xtr, dtype=np.float64); Xte = np.asarray(Xte, dtype=np.float64)
    ytr = np.asarray(ytr, dtype=np.float64)
    moy, ect = Xtr.mean(0), Xtr.std(0) + 1e-6
    A, B = (Xtr - moy) / ect, (Xte - moy) / ect
    yc = ytr - ytr.mean()
    w = np.linalg.solve(A.T @ A + np.eye(A.shape[1]), A.T @ yc)
    return B @ w + ytr.mean()


def faire_sonde(h: int, cachee: int, dev: str) -> nn.Module:
    if cachee > 0:
        return nn.Sequential(nn.Linear(h, cachee), nn.GELU(), nn.Linear(cachee, 1)).to(dev)
    return nn.Linear(h, 1).to(dev)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default=SNAPSHOT_DEFAUT)
    ap.add_argument("--jeton-base", type=int, default=220,
                    help="le jeton de base des pas (l'entrée ne porte QUE le signal)")
    ap.add_argument("--canal", type=int, default=0)
    ap.add_argument("--gain", type=float, default=1.0, help="gain du signal (la campagne : 1,0)")
    ap.add_argument("--retard", type=int, default=8)
    ap.add_argument("--pas", type=int, default=1024, help="longueur d'une séquence (pas)")
    ap.add_argument("--sequences", type=int, default=4,
                    help="séquences d'ENTRAÎNEMENT (la sonde apprend sur leur première moitié)")
    ap.add_argument("--epoques", type=int, default=6)
    ap.add_argument("--rang", type=int, default=8)
    ap.add_argument("--alpha", type=float, default=16.0)
    ap.add_argument("--couches-lora", type=int, default=24)
    ap.add_argument("--pas-lora", type=float, default=1e-3)
    ap.add_argument("--pas-sonde", type=float, default=1e-2)
    ap.add_argument("--cachee-sonde", type=int, default=0, help="0 = sonde linéaire")
    ap.add_argument("--iterations-sonde", type=int, default=600)
    ap.add_argument("--changement", action="store_true",
                    help="mesurer aussi la cible v[t] − v[t−1] : l'HABITUATION (gain négatif) "
                         "rend-elle le CHANGEMENT plus lisible que la valeur ?")
    ap.add_argument("--tampon", action="store_true",
                    help="donner le passé au réseau (canal `canal+retard` : c'est "
                         "`--entree-memoire`) — la référence haute, R² 1,000 pour 0 paire")
    ap.add_argument("--graine", type=int, default=0)
    ap.add_argument("--json", default=None)
    ap.add_argument("--sauver", default=None, help="écrire le LoRA appris (.pt) pour l'export")
    a = ap.parse_args()

    torch.manual_seed(a.graine); np.random.seed(a.graine)
    dev = "cuda"
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.modele, dtype=torch.float32).to(dev).eval()
    for p in m.parameters():
        p.requires_grad_(False)
    loras = poser_lora(m, a.couches_lora, a.rang, a.alpha)
    h = m.config.hidden_size
    gen = np.random.default_rng(a.graine)
    k = a.retard

    def sequence(L: int, grad: bool = True):
        """Un pas = le jeton de base + le signal sur un canal. Rend (états [L, h], v [L]).

        `grad=False` pour la sonde GELÉE : ses états ne doivent pas porter de graphe, sinon le
        premier `backward` le libère et le second lève « backward through the graph a second
        time » (attrapé au premier essai)."""
        v = gen.uniform(-2.0, 2.0, size=L).astype(np.float32)     # « bruit », comme la campagne
        # LE SIGNAL EST POSÉ SANS MODIFICATION EN PLACE : `emb[0, :, canal] += …` modifie une VUE
        # de l'embarquement, et autograd refuse alors de remonter le graphe (« a variable needed
        # for gradient computation has been modified by an inplace operation »). On construit donc
        # un delta, et on ADDITIONNE — c'est le même calcul, sans piège.
        emb = m.model.embed_tokens(torch.full((1, L), a.jeton_base, device=dev))
        delta = torch.zeros(1, L, h, device=dev)
        delta[0, :, a.canal] = a.gain * torch.tensor(v, device=dev)
        if a.tampon:
            decale = np.concatenate([np.zeros(k, dtype=np.float32), v[:L - k]])
            delta[0, :, a.canal + k] = a.gain * torch.tensor(decale, device=dev)
        emb = emb + delta
        # ON LIT L'ÉTAT DU MODÈLE SEUL (`m.model`), PAS LES LOGITS : la tête de sortie coûterait
        # 151 936 × L flottants par pas (2,5 Go à 4 096 pas) pour rien — la sonde ne lit que
        # l'état caché, et `Qwen2Model.last_hidden_state` est **le même** tenseur que
        # `hidden_states[-1]` du modèle complet (après la norme finale).
        if grad:
            return m.model(inputs_embeds=emb, use_cache=False).last_hidden_state[0], v
        with torch.no_grad():
            return m.model(inputs_embeds=emb, use_cache=False).last_hidden_state[0], v

    def tranche(st, v, debut, fin, changement=False):
        """Les lignes [debut, fin) et leurs cibles alignées.

        `mémoire` = v[t−k], `présent` = v[t], `avenir` = v[t+1] — et, si `changement`,
        `v[t] − v[t−1]` : ce que l'HABITUATION (gain négatif sur le tampon) devrait rendre lisible.
        La dernière ligne de `avenir` sort de la séquence, donc on s'arrête un pas avant.
        """
        # LA DERNIÈRE LIGNE N'A PAS D'AVENIR : on la retire pour TOUTES les cibles, sinon les
        # quatre tenseurs n'ont plus la même longueur (attrapé au premier essai).
        fin = min(fin, len(v) - 1)
        out = (st[debut:fin],
               torch.tensor(v[debut - k:fin - k], device=dev),
               torch.tensor(v[debut:fin], device=dev),
               torch.tensor(v[debut + 1:fin + 1], device=dev))
        if changement:
            out = out + (torch.tensor(v[debut:fin] - v[debut - 1:fin - 1], device=dev),)
        return out

    # ---------------------------------------------------------------- bras GELÉ
    # LE PROTOCOLE DE LA CAMPAGNE : la sonde apprend sur la PREMIÈRE moitié d'une séquence et se
    # mesure sur la SECONDE — même séquence. (Apprendre sur une séquence et mesurer sur une AUTRE
    # ne reproduit PAS les chiffres publiés : la lecture d'un canal dépend du contexte, et le
    # premier essai de cet outil rendait −3,6 au lieu de −0,68 pour cette seule raison.)
    st_te, v_te = sequence(a.pas, grad=False)
    dem = a.pas // 2
    ta = tranche(st_te, v_te, k, dem, a.changement)
    tb = tranche(st_te, v_te, dem, a.pas, a.changement)
    Xa, ya, pa, aa = ta[0], ta[1], ta[2], ta[3]
    Xb, yb, pb, ab = tb[0], tb[1], tb[2], tb[3]
    # UNE SONDE PAR CIBLE. Le premier essai n'en ajustait qu'une (sur la mémoire) et la mesurait
    # aussi contre le PRÉSENT : elle rendait alors −0,93 pour le présent, là où la campagne publie
    # +0,992. On ajuste donc trois sondes, comme la campagne.
    Xa_np, Xb_np = Xa.cpu().numpy(), Xb.cpu().numpy()
    r2_gele_pres = r2(ridge(Xa_np, pa.cpu().numpy(), Xb_np), pb.cpu().numpy())
    r2_gele_mem = r2(ridge(Xa_np, ya.cpu().numpy(), Xb_np), yb.cpu().numpy())
    # L'HABITUATION : la cible « changement » (v[t] − v[t−1]). Si le gain négatif sert à quelque
    # chose, c'est ici que ça se voit — et nulle part ailleurs (le passé, lui, reste lisible).
    r2_gele_chg = (r2(ridge(Xa_np, ta[4].cpu().numpy(), Xb_np), tb[4].cpu().numpy())
                   if a.changement else float("nan"))
    r2_gele_av = r2(ridge(Xa_np, aa.cpu().numpy(), Xb_np), ab.cpu().numpy())
    if a.changement:
        print(f"  gelé    : CHANGEMENT R² {r2_gele_chg:+.3f} (la cible de l'habituation)")
    print(f"  gelé    : mémoire R² {r2_gele_mem:+.3f} · présent R² {r2_gele_pres:+.3f} "
          f"(chiffres publiés : −0,681 / +0,992)")

    # ---------------------------------------------------------------- bras ENTRAÎNÉ
    sonde2 = faire_sonde(h, a.cachee_sonde, dev)
    opt = torch.optim.Adam([{"params": sonde2.parameters(), "lr": a.pas_sonde},
                            {"params": loras, "lr": a.pas_lora}])
    meilleur = (1e18, None, None)
    for e in range(a.epoques):
        # UNE SÉQUENCE À LA FOIS : avancer, reculer, mettre à jour. Calculer toutes les séquences
        # d'abord ferait capturer le MÊME `A` par tous les graphes, et le premier `opt.step()`
        # le modifierait en place — le second `backward` lèverait « a variable needed for gradient
        # computation has been modified by an inplace operation » (attrapé au premier essai).
        total = 0.0
        for _ in range(a.sequences):
            st, v = sequence(a.pas)
            Xa, ya, _, _ = tranche(st, v, k, a.pas // 2)
            opt.zero_grad()
            perte = nn.functional.mse_loss(sonde2(Xa).squeeze(-1), ya)
            perte.backward(); opt.step()
            total += float(perte.detach())
        # l'époque se choisit sur une séquence de VALIDATION (jamais celle du test final)
        st_va, v_va = sequence(a.pas, grad=False)
        Xa_va, ya_va, _, _ = tranche(st_va, v_va, k, a.pas // 2)
        with torch.no_grad():
            pv = nn.functional.mse_loss(sonde2(Xa_va).squeeze(-1), ya_va).item()
        marque = ""
        if pv < meilleur[0]:
            meilleur = (pv, {n: t.detach().clone() for n, t in sonde2.state_dict().items()},
                        [q.detach().clone() for q in loras])
            marque = "  ← meilleur (validation)"
        print(f"    époque {e + 1:>2}/{a.epoques} · perte train {total / a.sequences:.5f} · "
              f"validation {pv:.5f}{marque}")
    sonde2.load_state_dict(meilleur[1])
    for q, r in zip(loras, meilleur[2]):
        q.data.copy_(r)
    # LA SONDE DU BRAS ENTRAÎNÉ EST RÉAJUSTÉE SUR LA PREMIÈRE MOITIÉ DE LA SÉQUENCE DE MESURE —
    # exactement comme pour le bras gelé : sinon on comparerait deux protocoles, pas deux modèles.
    st_te2, v_te2 = sequence(a.pas, grad=False)
    dem = a.pas // 2
    Xa2, ya2, pa2, aa2 = tranche(st_te2, v_te2, k, dem)
    Xb2, yb2, pb2, ab2 = tranche(st_te2, v_te2, dem, a.pas)
    Xa2_np, Xb2_np = Xa2.cpu().numpy(), Xb2.cpu().numpy()
    r2_ent_mem = r2(ridge(Xa2_np, ya2.cpu().numpy(), Xb2_np), yb2.cpu().numpy())
    r2_ent_pres = r2(ridge(Xa2_np, pa2.cpu().numpy(), Xb2_np), pb2.cpu().numpy())
    r2_ent_av = r2(ridge(Xa2_np, aa2.cpu().numpy(), Xb2_np), ab2.cpu().numpy())
    r2_mel = r2(ridge(Xa2_np, ya2.cpu().numpy(), Xb2_np), gen.permutation(yb2.cpu().numpy()))
    print(f"  entraîné: mémoire R² {r2_ent_mem:+.3f} · présent R² {r2_ent_pres:+.3f} · "
          f"avenir (témoin) {r2_ent_av:+.3f} · cibles mélangées {r2_mel:+.3f}")

    print()
    print(f"| bras | R²(v[t−{k}]) mémoire | R²(v[t]) présent | R²(v[t+1]) témoin |")
    print("|---|---:|---:|---:|")
    print(f"| gelé + sonde | {r2_gele_mem:+.3f} | {r2_gele_pres:+.3f} | {r2_gele_av:+.3f} |")
    print(f"| **entraîné** (LoRA + sonde) | **{r2_ent_mem:+.3f}** | {r2_ent_pres:+.3f} | "
          f"{r2_ent_av:+.3f} |")
    print(f"| contrôle : cibles mélangées | {r2_mel:+.3f} | — | — |")
    print(f"| référence : tampon (`--entree-memoire`) | **1,000** | 1,000 | — |")
    if a.sauver:
        torch.save({"rang": a.rang, "alpha": a.alpha, "profondeur": a.couches_lora,
                    "adaptateur": None,
                    "lora": [{"nom": f"model.layers.{i}.self_attn.{p}_proj.weight",
                              "A": getattr(m.model.layers[i].self_attn, p + "_proj").A.detach().cpu(),
                              "B": getattr(m.model.layers[i].self_attn, p + "_proj").B.detach().cpu(),
                              "echelle": a.alpha / a.rang}
                             for i in range(a.couches_lora)
                             for p in ("q", "k", "v", "o")]}, a.sauver)
        print(f"LoRA écrit : {a.sauver}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"retard": k, "canal": a.canal, "gain": a.gain, "tampon": a.tampon,
             "gele_memoire": r2_gele_mem, "gele_present": r2_gele_pres,
             "gele_changement": r2_gele_chg,
             "entraine_memoire": r2_ent_mem, "entraine_present": r2_ent_pres,
             "entraine_avenir": r2_ent_av, "melange": r2_mel}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

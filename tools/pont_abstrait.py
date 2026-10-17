#!/usr/bin/env python3
"""pont_abstrait.py — LE LANGAGE ABSTRAIT ENTRE LA SORTIE PRÉ-LINGUISTIQUE ET L'ENTRÉE POST-LINGUISTIQUE.

LA QUESTION (de Stéphane, 16/10). Penser sans verbaliser n'est pas « réinjecter l'état » ✗ (mesuré : la
boucle naïve détruit la prédiction de cinq ordres de grandeur, et **normer n'y change rien** ✗✓ —
`rapport-pensee-silencieuse.md` § 2 ✓). C'est un **mode de fonctionnement différent** ✓ : il faut un
**langage abstrait** qui fasse correspondre

    la SORTIE pré-linguistique   (le résidu brut, avant la norme finale et avant la tête ✗)
    à l'ENTRÉE post-linguistique  (l'espace des embeddings de jetons, ce que le modèle sait RELIRE ✓)

et ce langage, il faut l'**apprendre** ✓ — pas l'espérer ✓.

CE QUE CET OUTIL FAIT, EN TROIS TEMPS.
  1. **Récolter des couples** ✓ : sur un texte, pour chaque position `p`, on prend
     `h_p` = l'état caché **après la dernière couche et AVANT la norme** ✓ (la sortie pré-linguistique ✓)
     et `e_{p+1}` = l'**embedding du jeton suivant** ✓ (l'entrée post-linguistique ✓). C'est le couple
     « ce que le modèle pense » → « ce qu'il lirait ensuite » ✓✓.
  2. **Apprendre le mapping** ✓ `M : h_p ↦ e_{p+1}` — **ridge** d'abord (linéaire, 896 × 896 ✓, fermé,
     instantané ✓), puis un **MLP** si le linéaire ne suffit pas ✗ (le non-linéaire est la question
     suivante ✓, pas la première ✓).
  3. **Comparer à trois témoins** ✓, et c'est là que la question est tranchée :
     * **le témoin bête** : l'embedding **moyen** du corpus ✗ (le « langage » qui ne dit rien ✓) ;
     * **le témoin du JETON** ✓ : l'embedding du jeton que le modèle **prédirait** (argmax ✓) — c'est le
       **repli sur le mode jeton** ✗✓, celui que Stéphane demande de ne PAS prendre ✓ ;
     * **le témoin ORACLE** : l'embedding du **vrai** jeton suivant ✗ (la borne supérieure ✓).
     Si le mapping appris fait **mieux que le témoin du jeton** ✓✓, alors il y a bien un **langage
     abstrait** qui porte plus que le mot ✗✓ ; s'il fait moins bien, la verbalisation est le pont le
     moins cher ✓ (et on sait pourquoi ✓).

CE QU'IL ÉCRIT : le mapping (`--sortie`, un `.npz` : `W`, `b`, et les statistiques ✓) — que
`tools/pensee_silencieuse.py --pont` sait ensuite **injecter** dans la boucle silencieuse ✓.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/pont_abstrait.py --hf <snapshot> --ids <fichier d'ids> \\
      [--positions 4000] [--ridge 1e-3] [--sortie /tmp/pont-abstrait.npz]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import numpy as np
import torch


def _lambda_cv(H: np.ndarray, E: np.ndarray, k: int = 3) -> float:
    """λ de ridge par VALIDATION CROISÉE ✗✓ (leçon du § 25 : un λ fixé rend les chiffres dépendants des
    réglages). Même fonction que dans `banc_lecteur.py` et `empreinte.py` ✓."""
    plis = np.array_split(np.arange(H.shape[0]), k)
    meilleur, err_min = 1e-3, 1e30
    for lam in (1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0):
        err = 0.0
        for i in range(k):
            te = plis[i]
            tr = np.concatenate([plis[j] for j in range(k) if j != i])
            mh, me = H[tr].mean(0), E[tr].mean(0)
            Hc, Ec = H[tr] - mh, E[tr] - me
            W = np.linalg.solve(Hc.T @ Hc + lam * np.eye(Hc.shape[1]), Hc.T @ Ec)
            err += float(np.linalg.norm((H[te] - mh) @ W + me - E[te]) ** 2)
        if err < err_min:
            meilleur, err_min = lam, err
    return meilleur


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True, help="dossier des poids de référence (safetensors)")
    ap.add_argument("--ids", required=True, help="corpus d'identifiants (identiques au moteur)")
    ap.add_argument("--positions", type=int, default=4000, help="nombre de positions récoltées")
    ap.add_argument("--longueur", type=int, default=1024, help="longueur d'une fenêtre")
    ap.add_argument("--ridge", type=float, default=1e-3)
    ap.add_argument("--sortie", default="/tmp/pont-abstrait.npz")
    ap.add_argument("--couches", default="",
                    help="couches à sonder (ex. « 2,8,16,23 ») : LA QUESTION « tu as ce qu'il te faut "
                         "dans les couches intermédiaires » se répond couche par couche")
    ap.add_argument("--norme", action="store_true",
                    help="prendre l'état APRÈS la norme finale (c'est celui que l'alignement entraîne ✓) "
                         "au lieu du résidu brut avant la norme ✗")
    ap.add_argument("--horizons", default="1,4,16",
                    help="combien de jetons D'AVANCE le mapping doit prédire (1 = le suivant)")
    a = ap.parse_args()

    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.ids).read_text()) if x.strip()]
    if len(ids) < a.longueur + 1:
        sys.exit(f"corpus trop court : {len(ids)}")
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    emb = m.get_input_embeddings()

    H, E = [], []
    with torch.no_grad():
        debut = 0
        while sum(len(h) for h in H) < a.positions and debut + a.longueur + 1 <= len(ids):
            bloc = torch.tensor([ids[debut:debut + a.longueur]])
            sortie = m(bloc, output_hidden_states=True)
            # ⚠️ `hidden_states[-1]` est la SORTIE DE LA DERNIÈRE COUCHE, AVANT LA NORME FINALE ✓ —
            # c'est la couche pré-linguistique ✗. `last_hidden_state` est APRÈS la norme ✗ (et
            # `logits` après la tête ✗) : prendre l'un pour l'autre est l'erreur que cette ligne
            # évite, et elle a coûté une mesure ce soir (normer l'état ne changeait rien ✓✗).
            h = sortie.hidden_states[-1][0]                     # (L, 896) pré-linguistique
            if a.norme:
                with torch.no_grad():
                    h = m.model.norm(h.unsqueeze(0))[0]          # l'état NORMALISÉ (celui de l'alignement ✓)
            e = emb(bloc)[0]                                    # (L, 896) post-linguistique
            H.append(h[:-1].numpy())                            # position p
            E.append(e[1:].numpy())                             # jeton p+1
            debut += a.longueur
    H = np.concatenate(H)[:a.positions].astype(np.float64)
    E = np.concatenate(E)[:a.positions].astype(np.float64)
    print(f"couples récoltés : {H.shape[0]} · état {H.shape[1]} · embedding {E.shape[1]}")

    # ================= LE BALAYAGE : QUELLE COUCHE SAIT QUOI, ET JUSQU'OÙ =================
    # L'HYPOTHÈSE (de Stéphane, 16/10) : « si un LLM peut répéter intégralement un énoncé, tu as ce
    # qu'il te faut dans les couches intermédiaires » ✓. Elle se teste sans supposer : on apprend, pour
    # CHAQUE couche L et CHAQUE horizon k, un mapping `h_p^(L) → embedding(jeton p+k)` ✓ et on regarde
    # deux choses — **quelle** couche lit le mieux la suite ✗, et **jusqu'où** elle la lit ✗✓.
    if a.couches:
        couches = [int(x) for x in a.couches.split(",") if x.strip()]
        horizons = [int(x) for x in a.horizons.split(",") if x.strip()]
        with torch.no_grad():
            debut, HS, ES = 0, {L: [] for L in couches}, []
            while sum(len(v) for v in HS[couches[0]]) < a.positions and debut + a.longueur + 1 <= len(ids):
                bloc = torch.tensor([ids[debut:debut + a.longueur]])
                sortie = m(bloc, output_hidden_states=True)
                for L in couches:
                    hsL = sortie.hidden_states[L][0]
                    if a.norme:
                        with torch.no_grad():
                            hsL = m.model.norm(hsL.unsqueeze(0))[0]
                    HS[L].append(hsL.numpy())
                ES.append(emb(bloc)[0].numpy())
                debut += a.longueur
            ES = np.concatenate(ES)
        print()
        print("  ce que l'état sait de la suite, par COUCHE et par HORIZON (écart relatif du")
        print("  mapping appris vers l'embedding du jeton p+k ; le jeton prédit par le modèle est")
        print("  le témoin du repli sur le mot ✗) :")
        entete = "   couche | " + " | ".join(f"k={k:<2}" for k in horizons) + " |  témoin jeton k=1"
        print(entete); print("   " + "-" * (len(entete) - 3))
        for L in couches:
            Hl = np.concatenate(HS[L])[:a.positions].astype(np.float64)
            ligne = []
            for k in horizons:
                Hb = Hl[:Hl.shape[0] - k]
                Eb = ES[k:k + Hb.shape[0]].astype(np.float64)
                mh, me = Hb.mean(0), Eb.mean(0)
                Hc2, Ec2 = Hb - mh, Eb - me
                lam2 = _lambda_cv(Hc2, Ec2) if Hc2.shape[0] > 100 else a.ridge
                W2 = np.linalg.solve(Hc2.T @ Hc2 + lam2 * np.eye(Hc2.shape[1]), Hc2.T @ Ec2)
                P2 = Hc2 @ W2 + me
                ligne.append(100 * float(np.linalg.norm(P2 - Eb) / np.linalg.norm(Eb)))
            # le témoin : le jeton que le MODÈLE aurait choisi, à l'horizon 1
            with torch.no_grad():
                d2, pr = 0, []
                while sum(len(p) for p in pr) < a.positions:
                    bloc = torch.tensor([ids[d2:d2 + a.longueur]])
                    pr.append(emb(m(bloc).logits[0][:-1].argmax(-1)).numpy())
                    d2 += a.longueur
            Ej = np.concatenate(pr)[:a.positions - 1].astype(np.float64)
            Eb1 = ES[1:a.positions].astype(np.float64)
            tem = 100 * float(np.linalg.norm(Ej - Eb1) / np.linalg.norm(Eb1))
            print(f"   {L:>6} | " + " | ".join(f"{v:5.1f}" for v in ligne) + f" |  {tem:5.1f}")
        print()
        print("   lecture : plus la case est BASSE, mieux cette couche dit ce qui vient ✓ ; si les")
        print("   couches du MILIEU lisent loin (k grand) alors que le jeton prédit lit mal, alors le")
        print("   contenu est bien DANS l'état, et le mot n'en est qu'un résumé pauvre ✓✓.")
        return 0

    # ---- 2. le mapping, appris (ridge : solution fermée, et le linéaire est la PREMIÈRE question ✓)
    moy_h, moy_e = H.mean(0), E.mean(0)
    Hc, Ec = H - moy_h, E - moy_e
    d = H.shape[1]
    lam0 = _lambda_cv(Hc, Ec) if Hc.shape[0] > 100 else a.ridge
    W = np.linalg.solve(Hc.T @ Hc + lam0 * np.eye(d), Hc.T @ Ec)      # (896, 896)
    pred = Hc @ W + moy_e

    def ecart(P, etiq):
        rel = float(np.linalg.norm(P - E) / np.linalg.norm(E))
        cos = float(np.mean(np.sum(P * E, axis=1) /
                            (np.linalg.norm(P, axis=1) * np.linalg.norm(E, axis=1) + 1e-12)))
        print(f"   {etiq:34s} : écart relatif {rel * 100:6.2f} % · cosinus moyen {cos:+.4f}")
        return rel

    print()
    print("  le mapping appris contre ses témoins :")
    rel_pont = ecart(pred, "MAPPING APPRIS (état → entrée)")
    ecart(np.tile(moy_e, (E.shape[0], 1)), "témoin bête (embedding moyen)")

    # ---- 3. le témoin du JETON : ce que le modèle PRÉDIRAIT, dans l'espace d'entrée
    with torch.no_grad():
        debut, predits = 0, []
        while sum(len(p) for p in predits) < H.shape[0]:
            bloc = torch.tensor([ids[debut:debut + a.longueur]])
            lg = m(bloc).logits[0]                              # (L, vocab)
            predits.append(emb(lg[:-1].argmax(-1)).numpy())
            debut += a.longueur
    E_jeton = np.concatenate(predits)[:H.shape[0]].astype(np.float64)
    rel_jeton = ecart(E_jeton, "témoin du JETON (argmax du modèle)")
    ecart(E, "témoin ORACLE (le vrai jeton suivant)")

    print()
    if rel_pont < rel_jeton:
        print(f"  ✅ LE LANGAGE ABSTRAIT EXISTE ET BAT LE JETON : {rel_pont * 100:.2f} % contre "
              f"{rel_jeton * 100:.2f} % — l'état pré-linguistique, une fois MAPPÉ, dit mieux ce qui")
        print("     vient que le mot que le modèle aurait choisi ✓✓ (c'est la réponse à la question posée).")
    else:
        print(f"  ✗ le mapping appris ne bat pas le jeton ({rel_pont * 100:.2f} % contre "
              f"{rel_jeton * 100:.2f} %) : dans cet espace, LE MOT EST LE MEILLEUR PONT ✓ — ce qui ne")
        print("     condamne pas le langage abstrait, mais dit qu'il lui faut autre chose qu'un linéaire ✗.")

    np.savez(a.sortie, W=W, b=moy_e - moy_h @ W, moy_h=moy_h, moy_e=moy_e,
             ridge=a.ridge, positions=H.shape[0], rel_pont=rel_pont, rel_jeton=rel_jeton)
    print(f"\n  mapping écrit dans {a.sortie} (W 896 × 896, biais, et les deux écarts ✓) —")
    print("  `tools/pensee_silencieuse.py --pont <fichier>` sait l'injecter dans la boucle silencieuse ✓")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

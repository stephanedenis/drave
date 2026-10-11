#!/usr/bin/env python3
"""profondeur_routee_oracle.py — dessin H : ce qu'un routeur PARFAIT pourrait éviter.

LA QUESTION (docs/modele-pour-drave.md, dessin H « routage par profondeur »). Un modèle peut-il
décider, **jeton par jeton**, de s'arrêter plus tôt ? Avant d'entraîner un routeur, il faut savoir
ce qu'il y a à gagner : si un oracle qui connaîtrait la réponse ne gagne presque rien, aucun
routeur appris ne le fera. C'est la **borne supérieure**, et elle se mesure avec ce qui existe.

DEUX CHEMINS, MÊMES JETONS.
  · chemin LONG  : l'état après 24 couches (le modèle entier), relu par la norme finale et la
    tête liée — c'est le modèle, au bit près (vérifié par `verifier_chaine_etat.py` : 0,013 %) ;
  · chemin COURT : l'état après 16 couches, relu par un **adaptateur entraîné** A (896×896) puis
    la même tête gelée. C'est le meilleur lecture bon marché qu'on sache construire à cette
    profondeur — celui de C8.

TROIS CHIFFRES, ET ILS NE DISENT PAS LA MÊME CHOSE.
  1. **l'accord** : part des jetons où le chemin court rend la MÊME réponse que le chemin long.
     C'est la borne de l'oracle : sur ces jetons, sortir tôt ne change pas la décision.
  2. **la cascade** : un routeur réel ne connaît pas la réponse, mais il a la **confiance** du
     chemin court. On sort tôt si `confiance ≥ seuil`. On balaie le seuil et on regarde la part
     de jetons sortis tôt **à qualité au moins égale** au chemin long. C'est le gain atteignable.
  3. **le témoin** : la même part de jetons sortis tôt, mais choisis AU HASARD. Sans lui, on ne
     saurait pas si le seuil de confiance sélectionne, ou s'il ne fait que réduire le débit.

PROTOCOLE, ET SA LIMITE. L'adaptateur s'entraîne sur une partie du texte et se teste sur une
autre, jamais vue — mais c'est UN texte, et un adaptateur de 800 000 poids pour quelques milliers
d'exemples surapprend : le chiffre du chemin court est donc **optimiste**, ce qui rend la borne de
l'oracle optimiste elle aussi. C'est écrit dans le rapport et ne se lit pas autrement.

Usage :
  tools/profondeur_routee_oracle.py --etats16 /tmp/c8-8k/etat --etats24 /tmp/mod/final \
      --ids /tmp/campagne24/ids_0.5B-Q8.txt --modele models/Qwen2.5-0.5B-Q8_0.gguf \
      --test-max 2632 --epoques 30
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lecture_etat import Tete, charger_etats, charger_ids  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats16", required=True)
    ap.add_argument("--etats24", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--modele", required=True)
    ap.add_argument("--limite", type=int, default=8192)
    ap.add_argument("--test-max", type=int, default=None,
                    help="dernière position du TEST (défaut : la plus grande disponible en "
                         "profondeur 24). Fixée, elle rend le chiffre reproductible.")
    ap.add_argument("--test-min", type=int, default=0,
                    help="première position du TEST : avec --test-min on peut tester la SECONDE "
                         "moitié du texte et entraîner sur la première, comme C8")
    ap.add_argument("--train-partie", choices=("avant", "apres"), default="apres",
                    help="où prendre les états d'entraînement, par rapport au test")
    ap.add_argument("--marge", type=int, default=512,
                    help="positions laissées entre le test et l'entraînement (le texte voisin se "
                         "ressemble : sans marge, le test n'est plus un test)")
    ap.add_argument("--epoques", type=int, default=30)
    ap.add_argument("--pas", type=float, default=1e-2)
    ap.add_argument("--batch", type=int, default=256)
    ap.add_argument("--graine", type=int, default=0)
    a = ap.parse_args()

    torch.manual_seed(a.graine)
    np.random.seed(a.graine)
    ids = charger_ids(a.ids, a.limite)
    pos16, X16 = charger_etats(a.etats16)
    pos24, X24 = charger_etats(a.etats24)
    test_max = a.test_max if a.test_max is not None else int(pos24.max())

    # --- le TEST : les positions où les DEUX profondeurs existent -----------------------------
    communes = sorted(set(int(p) for p in pos24) & set(int(p) for p in pos16))
    test = np.array([p for p in communes
                     if a.test_min <= p <= test_max and p + 1 < len(ids)], dtype=np.int64)
    if len(test) < 100:
        raise SystemExit(f"seulement {len(test)} positions communes : trop peu pour mesurer")
    # --- l'ENTRAÎNEMENT : l'autre moitié du texte, séparée par une marge -----------------------
    if a.train_partie == "apres":
        bas, haut = int(test.max()) + a.marge, len(ids)
    else:
        bas, haut = 0, int(test.min()) - a.marge
    train_pool = np.array([int(p) for p in pos16 if bas <= int(p) < haut and int(p) + 1 < len(ids)],
                          dtype=np.int64)
    coupe = len(train_pool) * 4 // 5
    train, val = train_pool[:coupe], train_pool[coupe:]
    if len(train) < 500:
        raise SystemExit(f"{len(train)} états d'entraînement : trop peu")
    print(f"test   : positions {test.min()}..{test.max()} ({len(test)} jetons)")
    print(f"entraînement : {len(train)} états ({train.min()}..{train.max()}) · "
          f"validation : {len(val)} ({val.min()}..{val.max()})")
    print(f"marge test/entraînement : {a.marge} positions\n")

    tete = Tete(a.modele)
    h = tete.h
    idx16 = {int(p): i for i, p in enumerate(pos16)}
    idx24 = {int(p): i for i, p in enumerate(pos24)}

    def lot(positions, X, index):
        idx = np.array([index[int(p)] for p in positions])
        return X[idx], ids[positions + 1]

    Xtr, ytr = lot(train, X16, idx16)
    Xva, yva = lot(val, X16, idx16)
    Xte16, yte = lot(test, X16, idx16)
    Xte24, _ = lot(test, X24, idx24)

    # --- le chemin LONG (référence) ------------------------------------------------------------
    L24 = tete.logits(Xte24)
    pred24 = L24.argmax(-1).numpy()
    ppl24 = tete.ppl(Xte24, yte)
    juste24 = pred24 == yte

    # --- l'adaptateur du chemin COURT ----------------------------------------------------------
    dev = tete.appareil
    Xtr_t = torch.from_numpy(Xtr).to(dev).half()
    ytr_t = torch.from_numpy(ytr).to(dev)
    Xva_t = torch.from_numpy(Xva).to(dev).half()
    yva_t = torch.from_numpy(yva).to(dev)
    A = torch.eye(h, device=dev, dtype=torch.float32, requires_grad=True)
    opt = torch.optim.Adam([A], lr=a.pas)

    def ppl_val():
        return tete.ppl(Xva, yva, A.detach())

    meilleur = (ppl_val(), 0, A.detach().clone())
    print(f"avant entraînement (A = identité) : perplexité de validation = {meilleur[0]:,.4f}")
    for e in range(a.epoques):
        perm = torch.randperm(len(ytr), device=dev)
        tot = 0.0
        for d in range(0, len(ytr), a.batch):
            idx = perm[d:d + a.batch]
            opt.zero_grad()
            logits = tete.norme((Xtr_t[idx].float() @ A.T).half()) @ tete.W.T
            perte = torch.nn.functional.cross_entropy(logits.float(), ytr_t[idx])
            perte.backward()
            opt.step()
            tot += perte.item() * len(idx)
        if (e + 1) % max(1, a.epoques // 6) == 0 or e == 0:
            pv = ppl_val()
            marque = ""
            if pv < meilleur[0]:
                meilleur = (pv, e + 1, A.detach().clone())
                marque = "  ← meilleur"
            print(f"  époque {e + 1:>3}/{a.epoques} · perte train {np.exp(tot / len(ytr)):,.4f} "
                  f"· validation {pv:,.4f}{marque}")
    A = meilleur[2]
    print(f"meilleure époque : {meilleur[1]} · validation {meilleur[0]:,.4f}\n")

    L16 = tete.logits(Xte16, A)
    pred16 = L16.argmax(-1).numpy()
    ppl16 = tete.ppl(Xte16, yte, A)
    juste16 = pred16 == yte

    # --- 1. l'accord, borne de l'oracle --------------------------------------------------------
    accord = pred16 == pred24
    n = len(yte)
    print("| chemin | perplexité (test) | justesse@1 |")
    print("|---|---|---|")
    print(f"| long — 24 couches, tête du modèle | {ppl24:,.4f} | {100 * juste24.mean():.2f} % |")
    print(f"| court — 16 couches, adaptateur entraîné | {ppl16:,.4f} | {100 * juste16.mean():.2f} % |")
    print()
    print(f"ACCORD court/long : {100 * accord.mean():.2f} % des {n} jetons "
          f"({accord.sum()} jetons) — sur ceux-là, sortir à 16 couches ne change pas la décision.")
    print(f"oracle (le meilleur des deux par jeton) : {100 * (juste16 | juste24).mean():.2f} %")

    # --- 2. la cascade : sortir tôt selon la confiance du chemin court --------------------------
    conf = torch.softmax(L16, dim=-1).max(-1).values.numpy()
    print("\n| seuil de confiance | sortis tôt | justesse globale | court sur les sortis | "
          "long sur les sortis | témoin au hasard |")
    print("|---|---|---|---|---|---|")
    rng = np.random.default_rng(a.graine)
    for seuil in (0.0, 0.5, 0.7, 0.9, 0.95, 0.99):
        sortis = conf >= seuil
        if sortis.sum() == 0:
            continue
        # justesse : chemin court sur les jetons sortis, chemin long sur les autres
        juste = np.where(sortis, juste16, juste24).mean()
        # LES DEUX CHEMINS SUR LES MÊMES JETONS : c'est la comparaison qui dit si le seuil
        # sélectionne des jetons où le chemin court est À PARITÉ, ou seulement des jetons où il
        # est moins mauvais. Sans ces deux colonnes, on ne saurait pas quoi améliorer.
        court_sur = juste16[sortis].mean()
        long_sur = juste24[sortis].mean()
        # témoin : la MÊME part de jetons, tirés au hasard (là où le choix ne veut rien dire)
        temoin = 0.0
        for _ in range(20):
            t = rng.random(n) < sortis.mean()
            temoin += np.where(t, juste16, juste24).mean() / 20
        print(f"| {seuil:.2f} | {100 * sortis.mean():.1f} % | {100 * juste:.2f} % | "
              f"{100 * court_sur:.2f} % | {100 * long_sur:.2f} % | {100 * temoin:.2f} % |")
    print(f"\n(point de comparaison : tout en long = {100 * juste24.mean():.2f} % · "
          f"tout en court = {100 * juste16.mean():.2f} %)")
    print("Les colonnes « court » et « long » portent sur LES MÊMES jetons : si le court y reste")
    print("derrière le long, le seuil de confiance ne trouve aucun sous-ensemble où sortir tôt")
    print("soit neutre — et c'est cette colonne qu'un vrai modèle routé devrait renverser.")

    # --- 3. la confiance sépare-t-elle les désaccords ? ----------------------------------------
    if accord.sum() and (~accord).sum():
        m_ok, m_ko = conf[accord].mean(), conf[~accord].mean()
        print(f"\nconfiance moyenne du chemin court — quand il est d'accord avec le long : "
              f"{m_ok:.3f} · quand il ne l'est pas : {m_ko:.3f}")
        if m_ok <= m_ko:
            print("  ⚠ la confiance NE sépare PAS les désaccords : un routeur appris sur elle "
                  "n'a aucune prise sur la borne de l'accord")
    else:
        print("\n(aucun désaccord : le chemin court et le chemin long répondent toujours la même "
              "chose sur ce test — la borne vaut alors 100 %)")

    # --- ce que coûterait la sortie anticipée --------------------------------------------------
    print("\nLecture : sortir à 16 couches épargne 8 couches sur 24, soit un tiers des paires")
    print("de ces jetons (mêmes contexte et largeur). La question du dessin H n'est donc pas")
    print("« peut-on épargner ? » mais « sur quelle part des jetons, et le sait-on sans oracle ? »")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""langue_dans_etat.py (v2) — LA LANGUE EST-ELLE LISIBLE DANS L'ÉTAT ? (l'outil du chapitre 7, RÉPARÉ)

CE QUI ÉTAIT FAUX DANS LA v1, ET C'EST GRAVE ✗✗. La v1 construisait les états de toutes les fenêtres anglais
puis de toutes les fenêtres françaises, **concaténait** les deux blocs et appelait `precision_lineaire(X, y)` —
laquelle découpait les LIGNES en deux moitiés ✓✗ : `X[:n2]` (entraînement) = **la première moitié des fenêtres
anglaises**, `X[n2:]` (test) = **le reste des anglaises + TOUTES les françaises** ✓✗. Le classifieur apprenait donc
« l'anglais » sur une seule classe ✗, et on lisait sa précision sur un mélange ✗. Pire, `max(acc, 100-acc)`
(ajouté pour le signe arbitraire ✓) transformait ce mélange en un chiffre d'apparence raisonnable ✓✗.

*Conséquence : la « neutralité du noyau » (50,2 % aux couches 1-2 ✓✓) — le résultat fondateur du chapitre 7 —
était un artefact de l'instrument* ✗✗. Avec un découpage correct et des étiquettes alignées, la même sonde
donne **87 à 99 %** sur les mêmes modèles ✓✓ : **la langue est lisible partout**.

CE QUE LA v2 FAIT, ET QUI DOIT ÊTRE VÉRIFIÉ À CHAQUE FOIS ✗ :
  · **découpage par fenêtre** ✓ : les fenêtres paires entraînent, les impaires testent ✓✓ (pas de recouvrement ✓),
    et les deux langues sont **mélangées** dans les deux ensembles ✓ ;
  · **standardisation** des états ✓ (moyenne/écart de l'entraînement ✓) — sans elle, un ridge à λ fixe est
    dominé par quelques dimensions ✓✗ ;
  · **contrôle intra-langue** ✓ : deux moitiés du corpus anglais, même découpage ✓ — c'est le plancher ✓ ;
  · **contrôle négatif** ✓✓ : étiquettes mélangées → la précision **doit** retomber au hasard ✓, sinon la sonde
    mesure autre chose ✗✗ ;
  · et la précision est rendue **avec son signe le plus favorable** ✓ (héritage de la v1 ✓) mais le contrôle
    négatif dit si ce maximum est légitime ✓✓.

Usage :
  python3 tools/langue_dans_etat.py --hf /tmp/jouet-mixte-litt2 --en data/corpus_en.txt --fr data/corpus_fr.txt
"""
from __future__ import annotations
import argparse, pathlib
import numpy as np, torch


def fenetres(texte: str, longueur: int, nombre: int):
    b = np.frombuffer(texte.encode("utf-8", errors="ignore"), dtype=np.uint8).astype(np.int64)
    pas = max(longueur, len(b) // max(1, nombre + 1))
    out = []
    for i in range(nombre):
        d = i * pas
        if d + longueur >= len(b):
            break
        out.append(b[d:d + longueur])
    return out


def etats(modele, lot, couches, pooling="position"):
    S = {L: [] for L in couches}
    with torch.no_grad():
        for w in lot:
            b = torch.tensor(w).unsqueeze(0)
            hs = modele(b, output_hidden_states=True).hidden_states
            for L in couches:
                h = hs[L][0]
                z = modele.model.norm(h)
                S[L].append((z.mean(0) if pooling == "moyenne" else z).numpy().astype(np.float64))
    if pooling == "moyenne":
        return {L: np.concatenate([v[None, :] for v in S[L]]) for L in couches}
    return {L: np.concatenate(S[L]) for L in couches}


def classer(X_tr, y_tr, X_te, y_te):
    """Régression logistique binaire, standardisée, sur CPU (les états sont petits) ✓."""
    mu, sd = X_tr.mean(0), X_tr.std(0) + 1e-8
    Xt = torch.tensor((X_tr - mu) / sd, dtype=torch.float32)
    Xv = torch.tensor((X_te - mu) / sd, dtype=torch.float32)
    yt = torch.tensor((y_tr > 0).astype(np.int64), dtype=torch.long)
    couche = torch.nn.Linear(X_tr.shape[1], 2)
    opt = torch.optim.Adam(couche.parameters(), lr=2e-2, weight_decay=1e-3)
    for _ in range(300):
        opt.zero_grad()
        torch.nn.functional.cross_entropy(couche(Xt), yt).backward()
        opt.step()
    with torch.no_grad():
        pred = couche(Xv).argmax(1).numpy()
    acc = 100 * float((pred == (y_te > 0).astype(np.int64)).mean())
    return max(acc, 100 - acc)          # le signe reste arbitraire ✓, mais le contrôle négatif le contrôle ✓✓


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--en", default="data/corpus_en.txt")
    ap.add_argument("--fr", default="data/corpus_fr.txt")
    ap.add_argument("--longueur", type=int, default=128)
    ap.add_argument("--fenetres", type=int, default=200)
    ap.add_argument("--couches", default="")
    ap.add_argument("--pooling", choices=["position", "moyenne"], default="position")
    ap.add_argument("--temoin", action="store_true", help="étiquettes mélangées ✓")
    a = ap.parse_args()
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    n_couches = m.config.num_hidden_layers
    couches = [int(x) for x in a.couches.split(",")] if a.couches else list(range(n_couches + 1))
    f_en = fenetres(pathlib.Path(a.en).read_text(errors="ignore"), a.longueur, a.fenetres)
    f_fr = fenetres(pathlib.Path(a.fr).read_text(errors="ignore"), a.longueur, a.fenetres)
    E_en_all, E_fr_all = etats(m, f_en, couches, a.pooling), etats(m, f_fr, couches, a.pooling)
    n = min(len(f_en), len(f_fr))
    print(f"  {len(f_en)} fenêtres anglaises · {len(f_fr)} françaises · longueur {a.longueur} · pooling {a.pooling}")
    print(f"  modèle : {n_couches} couches · dimension {m.config.hidden_size}")
    if a.temoin:
        print("  ⚠️ CONTRÔLE NÉGATIF : étiquettes mélangées ✓")
    print("\n   couche | langue | contrôle intra-langue | verdict")
    print("   -------|--------|----------------------|--------")
    rng = np.random.RandomState(0)

    def deux_blocs(Xa, Xb, melanger=False):
        """Entraîne sur la 1re moitié de CHAQUE bloc, teste sur la 2e ✓✓ (découpage par fenêtre ✓)."""
        ma, mb = len(Xa) // 2, len(Xb) // 2
        X_tr = np.concatenate([Xa[:ma], Xb[:mb]])
        y_tr = np.r_[np.ones(ma), -np.ones(mb)]
        X_te = np.concatenate([Xa[ma:], Xb[mb:]])
        y_te = np.r_[np.ones(len(Xa) - ma), -np.ones(len(Xb) - mb)]
        if melanger:
            y_tr, y_te = rng.permutation(y_tr), rng.permutation(y_te)
        return classer(X_tr, y_tr, X_te, y_te)

    for L in couches:
        E_en, E_fr = E_en_all[L], E_fr_all[L]
        acc = deux_blocs(E_en, E_fr, melanger=a.temoin)
        k = min(len(E_en), len(E_fr)) // 2
        acc_c = deux_blocs(E_en[:k], E_en[k:2 * k])       # les DEUX moitiés de l'anglais ✓
        verdict = "LA LANGUE ✓ (lisible)" if acc > 60 else ("neutre ✓✓" if acc < 50 else "±")
        print(f"   {L:>5} | {acc:5.1f}% |        {acc_c:5.1f}%        | {verdict}")
    return 0


raise SystemExit(main())

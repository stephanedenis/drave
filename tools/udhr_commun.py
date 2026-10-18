#!/usr/bin/env python3
"""udhr_commun.py — LE SOCLE DES MESURES UDHR : charger, encoder, moyenner.

POURQUOI UN MODULE À PART. Les expériences de cette série (sonde de langue, retrieval croisé, restitution) ont
toutes le **même** premier étage ✓✓ : charger un modèle, encoder un article, garder les états par couche et les
**moyenner** ✓. Si cet étage est écrit trois fois, il divergera trois fois ✗✓ — et c'est exactement le genre
d'écart qu'on ne voit pas ✓✓.

TROIS CHOIX QUI DOIVENT ÊTRE DITS ✗ :
  · **la moyenne des positions** ✓ : elle détruit l'ordre des mots ✓✗. Pour identifier une **langue** c'est sans
    gravité (la langue est dans le vocabulaire et l'orthographe ✓) ; pour la **traduction**, c'est une hypothèse
    forte ✓ — un état moyen n'est pas une phrase ✓.
  · **la normalisation du modèle** (`model.norm` ✓) : on lit l'état tel que le modèle l'utiliserait pour sortir ✓✓,
    pas l'état brut de la couche ✓ — c'est le choix du chapitre 7 ✓.
  · **la troncature** à `--longueur` octets/jetons ✓ : les articles longs (l'article 2 fait 1 500 caractères ✓)
    sont coupés ✗✓ ; la moyenne porte donc sur le **début** de l'article ✓.

CE QU'IL NE FAIT PAS ✗ : il ne vérifie pas que l'article N dit la même chose dans deux langues ✓ — c'est la
structure du corpus XML qui le garantit ✓✓ (et le nombre d'articles par langue le contrôle ✓).
"""
from __future__ import annotations
import json, pathlib
import numpy as np


def charger_articles(chemin: str = "data/udhr/articles_propres.jsonl") -> dict[str, dict[int, str]]:
    """{fichier: {numéro d'article: texte}} ✓."""
    out: dict[str, dict[int, str]] = {}
    for ligne in pathlib.Path(chemin).read_text().splitlines():
        x = json.loads(ligne)
        out.setdefault(x["fichier"], {})[int(x["art"])] = x["texte"]
    return out


def charger_meta(chemin: str = "data/udhr/meta.json") -> dict[str, dict]:
    return json.loads(pathlib.Path(chemin).read_text())


def charger_modele(chemin: str, tokeniseur: bool = False):
    """Charge un modèle HF ; renvoie (modèle, encodeur, device).

    L'encodeur transforme un texte en identifiants : **octets** pour les modèles-jouets ✓ (vocabulaire 256 ✓),
    **jetons** pour un vrai modèle de langue ✓✓ (Qwen ✗ ne comprend pas les octets bruts ✓).
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    m = AutoModelForCausalLM.from_pretrained(chemin, dtype=torch.float32).to(device).eval()
    tok = None
    if tokeniseur:
        tok = AutoTokenizer.from_pretrained(chemin)
    def encoder(txt: str, longueur: int):
        if tok is not None:
            ids = tok(txt, add_special_tokens=False).input_ids[:longueur]
            return torch.tensor(ids, dtype=torch.long, device=device)
        b = np.frombuffer(txt.encode("utf-8", errors="ignore"), dtype=np.uint8).astype(np.int64)[:longueur]
        return torch.tensor(b, dtype=torch.long, device=device)
    return m, encoder, device


def etats_par_couche(modele, ids, couches: list[int], pooling: str = "moyenne") -> dict[int, np.ndarray]:
    """L'état de chaque couche demandée, normalisé comme le modèle le ferait ✓.

    `pooling` vaut « moyenne » ✓ (un vecteur par article, ce qui détruit l'ordre des mots ✓✗) ou « position »
    ✓✓ (un vecteur par position, comme le chapitre 7 ✓). *Les deux ne mesurent pas la même chose : la moyenne dit
    si la langue est dans le NUAGE de l'article, la position dit si elle est dans CHAQUE mot* ✓✓.
    """
    import torch
    with torch.no_grad():
        sortie = modele(ids.unsqueeze(0), output_hidden_states=True)
        hs = sortie.hidden_states
        L = len(hs) - 1
        out = {}
        for c in couches:
            cc = L if c < 0 else c
            z = modele.model.norm(hs[cc][0])
            out[c] = (z.mean(0) if pooling == "moyenne" else z).float().cpu().numpy()
    return out


def accuracy(y_pred, y_vrai) -> float:
    return float((np.asarray(y_pred) == np.asarray(y_vrai)).mean())


def entrainer(X_train, y_train, X_test, n_classes, epochs=400, lr=2e-2):
    """Une régression logistique multiclasse, standardisée, sur GPU si possible ✓."""
    import torch
    torch.manual_seed(0)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    mu, sd = X_train.mean(0), X_train.std(0) + 1e-8
    Xt = torch.tensor((X_train - mu) / sd, dtype=torch.float32, device=dev)
    yt = torch.tensor(y_train, dtype=torch.long, device=dev)
    Xv = torch.tensor((X_test - mu) / sd, dtype=torch.float32, device=dev)
    couche = torch.nn.Linear(X_train.shape[1], n_classes).to(dev)
    opt = torch.optim.Adam(couche.parameters(), lr=lr, weight_decay=1e-3)
    for _ in range(epochs):
        opt.zero_grad()
        torch.nn.functional.cross_entropy(couche(Xt), yt).backward()
        opt.step()
    with torch.no_grad():
        logits = couche(Xv)
        pred = logits.argmax(1).cpu().numpy()
        top5 = logits.topk(min(5, n_classes), dim=1).indices.cpu().numpy()
    return pred, top5, couche

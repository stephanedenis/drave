#!/usr/bin/env python3
"""c8_entrainer_tete.py — C8 : une TÊTE ENTRAÎNÉE pour une profondeur donnée.

LA QUESTION, ET ELLE EST MAINTENANT PRÉCISE. La sonde linéaire a montré que l'état de la couche
16 **contient** le prochain jeton (40,8 % parmi les 256 plus fréquents, contre 4,0 % pour la
classe majoritaire — `reports/rapport-c8-sonde-profondeur.md`). Mais le chemin tronqué, lui,
avec la **tête du modèle**, rend **1 127 368** de perplexité contre **9,43** au modèle complet.
Alors : une tête **entraînée** pour cette profondeur peut-elle combler l'écart ?

CE QUI EST ENTRAÎNÉ, ET CE QUI NE L'EST PAS. On n'entraîne **pas** de tête de sortie complète
(151 936 × 896 = 136 M poids, pour 8 000 exemples : ce serait de l'apprentissage par cœur). On
entraîne un **adaptateur** `A` (896 × 896) qui place l'état intermédiaire dans l'espace que la
**tête liée du modèle** (`token_embd.weight`, gelée) sait déjà lire, la norme finale du modèle
étant appliquée entre les deux — exactement la chaîne du moteur :

    logits = W_tête · rmsnorm(A · x_16)

La perplexité obtenue est donc **plein vocabulaire**, directement comparable à 1 127 368 (chemin
tronqué avec la tête empruntée) et à 9,43 (modèle complet).

CE QUE ÇA MESURE, ET SA LIMITE. Ça mesure ce qu'un **seul texte** permet d'apprendre : un
adaptateur ajusté sur la première moitié du texte et évalué sur la seconde. Un vrai réflexe
s'entraînerait sur un corpus — le chiffre d'ici est donc une **borne supérieure optimiste** de ce
qu'une tête dédiée peut faire, pas la performance d'un modèle entraîné. C'est écrit dans le
rapport, et ça ne se lit pas autrement.

Usage :
  tools/c8_entrainer_tete.py --etats /tmp/c8-8k/etat --ids /tmp/campagne24/ids_0.5B-Q8.txt \
      --modele models/Qwen2.5-0.5B-Q8_0.gguf --limite 8192 [--epoques 40] [--pas 1e-2]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import struct
import sys

import numpy as np
import torch


# --------------------------------------------------------------------------------------------
# Lecture GGUF : juste ce qu'il faut (l'énorme majorité du format ne sert pas ici)
# --------------------------------------------------------------------------------------------
def _chaine(f) -> str:
    n = struct.unpack("<Q", f.read(8))[0]
    return f.read(n).decode("utf-8", "replace")


def _valeur(f, t: int):
    fmt = {0: "<B", 1: "<b", 2: "<H", 3: "<h", 4: "<I", 5: "<i", 6: "<f", 7: "<B", 10: "<Q", 11: "<q",
           12: "<d"}
    if t == 8:
        return _chaine(f)
    if t == 9:
        et = struct.unpack("<I", f.read(4))[0]
        n = struct.unpack("<Q", f.read(8))[0]
        return [_valeur(f, et) for _ in range(n)]
    return struct.unpack(fmt[t], f.read(struct.calcsize(fmt[t])))[0]


def lire_entete(chemin: str):
    """(tenseurs {nom: (dims, type, offset)}, début des données)."""
    f = open(chemin, "rb")
    if f.read(4) != b"GGUF":
        raise SystemExit(f"{chemin} : ce n'est pas un GGUF")
    struct.unpack("<I", f.read(4))[0]
    n_tensors, n_kv = struct.unpack("<QQ", f.read(16))
    alignement = 32
    for _ in range(n_kv):
        cle = _chaine(f)
        t = struct.unpack("<I", f.read(4))[0]
        v = _valeur(f, t)
        if cle == "general.alignment":
            alignement = int(v)
    tenseurs = {}
    for _ in range(n_tensors):
        nom = _chaine(f)
        nd = struct.unpack("<I", f.read(4))[0]
        dims = [struct.unpack("<Q", f.read(8))[0] for _ in range(nd)]
        ttype = struct.unpack("<I", f.read(4))[0]
        off = struct.unpack("<Q", f.read(8))[0]
        tenseurs[nom] = (dims, ttype, off)
    debut = (f.tell() + alignement - 1) // alignement * alignement
    return f, tenseurs, debut


def lire_q8_0(f, offset: int, n_elements: int) -> np.ndarray:
    """Déquantifie Q8_0 : blocs de 32 (une échelle f16 + 32 i8)."""
    n_blocs = n_elements // 32
    f.seek(offset)
    brut = np.frombuffer(f.read(n_blocs * 34), dtype=np.uint8).reshape(n_blocs, 34)
    echelles = np.ascontiguousarray(brut[:, :2]).view(np.float16).astype(np.float32).reshape(-1, 1)
    qs = np.ascontiguousarray(brut[:, 2:]).view(np.int8).astype(np.float32)
    return (echelles * qs).reshape(-1)


def lire_f32(f, offset: int, n_elements: int) -> np.ndarray:
    f.seek(offset)
    return np.frombuffer(f.read(4 * n_elements), dtype="<f4").astype(np.float32)


# --------------------------------------------------------------------------------------------
# L'état, les cibles, l'entraînement
# --------------------------------------------------------------------------------------------
def charger_ids(chemin: str, limite: int) -> np.ndarray:
    texte = pathlib.Path(chemin).read_text()
    vals = []
    for m in re.split(r"[,\s]+", texte):
        if not m:
            continue
        try:
            vals.append(int(m))
        except ValueError:
            continue
        if len(vals) >= limite:
            break
    if not vals:
        raise SystemExit(f"{chemin} : aucun identifiant lisible")
    return np.array(vals, dtype=np.int64)


def charger_etats(prefixe: str):
    fichiers = sorted(pathlib.Path(prefixe).parent.glob(pathlib.Path(prefixe).name + ".*"),
                      key=lambda f: int(f.name.rsplit(".", 1)[1]))
    pos, lignes = [], []
    for f in fichiers:
        octets = f.read_bytes()
        if len(octets) % 4:
            continue
        pos.append(int(f.name.rsplit(".", 1)[1]))
        lignes.append(np.frombuffer(octets, dtype="<f4"))
    if not lignes:
        raise SystemExit(f"{prefixe} : aucun état lisible")
    return np.array(pos, dtype=np.int64), np.vstack(lignes)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", default=None,
                    help="un préfixe : moitié entraînement, moitié test (même texte)")
    ap.add_argument("--train", default=None, help="préfixes séparés par des virgules")
    ap.add_argument("--test", default=None, help="préfixes séparés par des virgules (textes JAMAIS vus)")
    ap.add_argument("--val", default=None,
                    help="morceaux de VALIDATION (choisir l'époque dessus, jamais sur le test) : "
                         "sans eux, la « meilleure époque » est choisie sur le test, ce qui est "
                         "une fuite et gonfle le chiffre publié")
    ap.add_argument("--ids", default=None,
                    help="fichier d'identifiants ; utile seulement pour `--etats` (un texte) — "
                         "avec --train/--test, chaque morceau `etat-m<i>` prend SES `morceau-<i>.txt`")
    ap.add_argument("--modele", required=True)
    ap.add_argument("--limite", type=int, default=8192)
    ap.add_argument("--epoques", type=int, default=40)
    ap.add_argument("--pas", type=float, default=1e-2)
    ap.add_argument("--batch", type=int, default=256)
    ap.add_argument("--repertoire", type=float, default=1e-5)
    ap.add_argument("--graine", type=int, default=0,
                    help="graine du tirage des lots : sans elle, deux entraînements identiques "
                         "ne donnent pas le même chiffre (constaté : 2 632 puis 9 056 au même "
                         "protocole), et aucune comparaison n'est concluante")
    ap.add_argument("--cachee", type=int, default=0,
                    help="taille d'une couche cachée (0 = adaptateur purement linéaire)")
    ap.add_argument("--ppl_tronque", type=float, default=None,
                    help="perplexité du chemin tronqué avec la tête EMPRUNTÉE (pour la table)")
    ap.add_argument("--ppl_complet", type=float, default=None)
    a = ap.parse_args()

    # GRAINE FIXÉE PAR DÉFAUT : sans elle, deux entraînements au même protocole donnaient
    # 2 632 puis 9 056 sur le même test — l'ordre des lots change tout, et aucune comparaison
    # (linéaire contre non linéaire, 7 morceaux contre 39) n'aurait été concluante.
    torch.manual_seed(a.graine)
    np.random.seed(a.graine)

    if not (a.etats or (a.train and a.test)):
        raise SystemExit("donner --etats (un texte, partagé) ou --train ET --test (textes distincts)")

    def ids_du_morceau(pref: str) -> str:
        """Le fichier d'identifiants QUI VA AVEC ce préfixe d'états.

        Les cibles d'un morceau sont SES jetons : lire un seul fichier d'ids pour tous les
        morceaux donnait des cibles étrangères aux états — un apprentissage sur du bruit, qui
        aurait « mesuré » que la tête ne généralise pas. Convention : `etat-m3` ↔ `morceau-3.txt`
        dans le même dossier ; à défaut, on retombe sur `--ids`.
        """
        m = re.search(r"etat-m(\d+)$", pref)
        if m:
            voisin = pathlib.Path(pref).parent / f"morceau-{m.group(1)}.txt"
            if voisin.exists():
                return str(voisin)
        if not a.ids:
            raise SystemExit(f"aucun fichier d'identifiants pour {pref} (ni morceau-<i>.txt "
                             f"voisin, ni --ids)")
        return a.ids

    def jeu(prefixes: list[str]):
        """Concatène des préfixes d'états avec LEURS cibles (les ids de leur morceau)."""
        Xs, ys = [], []
        for pref in prefixes:
            ids_p = charger_ids(ids_du_morceau(pref), a.limite)
            pos_p, X_p = charger_etats(pref)
            garde = pos_p + 1 < len(ids_p)
            pos_p, X_p = pos_p[garde], X_p[garde]
            Xs.append(X_p)
            ys.append(ids_p[pos_p + 1])
        return np.vstack(Xs), np.concatenate(ys)

    if a.train and a.test:
        Xtr, ytr = jeu(a.train.split(","))
        Xte, yte = jeu(a.test.split(","))
        if a.val:
            Xva, yva = jeu(a.val.split(","))
            print(f"entraînement : {Xtr.shape[0]} états · validation : {Xva.shape[0]} · "
                  f"test (jamais vus) : {Xte.shape[0]}")
        else:
            Xva = yva = None
            print(f"entraînement : {Xtr.shape[0]} états · test (textes jamais vus) : {Xte.shape[0]} états")
            print("  ⚠ pas de --val : l'époque est choisie SUR LE TEST (fuite) — à n'utiliser que "
                  "pour comparer des protocoles entre eux")
    else:
        if not a.ids:
            raise SystemExit("--etats demande --ids (un texte, un fichier d'identifiants)")
        pos, X = charger_etats(a.etats)
        ids = charger_ids(a.ids, a.limite)
        garde = pos + 1 < len(ids)
        pos, X = pos[garde], X[garde]
        y = ids[pos + 1]
        coupe = len(y) // 2
        Xtr, ytr, Xte, yte = X[:coupe], y[:coupe], X[coupe:], y[coupe:]
        Xva = yva = None
        print(f"un seul texte : {len(y)} états (moitié entraînement, moitié test)")
    h_etats = Xtr.shape[1]

    f, tenseurs, debut = lire_entete(a.modele)
    nom_tete = "output.weight" if "output.weight" in tenseurs else "token_embd.weight"
    nom_norme = "output_norm.weight"
    dims, ttype, off = tenseurs[nom_tete]
    # ATTENTION À L'ORDRE : dans un GGUF, `dims[0]` est la dimension CONTIGUË (le pas), pas la
    # première dimension logique. `token_embd.weight` est donc (896, 151 936) en stockage, et
    # (151 936, 896) en logique. Lire `h = dims[1]` faisait 151 936 canaux cachés et demandait
    # une matrice identité de 86 Gio (attrapé par l'OOM, pas par le calcul).
    h, vocab = int(dims[0]), int(dims[1])
    print(f"tête liée : {nom_tete} dims={dims} (stockage) → logique ({vocab}, {h}) · "
          f"type {ttype} · norme : {nom_norme}")
    if ttype != 8:
        raise SystemExit(f"cette tête n'est pas Q8_0 (type {ttype}) : ce script ne sait pas la lire")
    W = lire_q8_0(f, debut + off, vocab * h).reshape(vocab, h)
    dims_n, type_n, off_n = tenseurs[nom_norme]
    g = lire_f32(f, debut + off_n, dims_n[0])
    print(f"tête déquantifiée : {W.shape} · norme : {g.shape}")

    # tenseurs torch — la tête et la norme sont GELÉES, seul l'adaptateur apprend
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    Wt = torch.from_numpy(W).to(dev).half()
    # fp16 partout SAUF l'adaptateur : mélanger float et Half lève une erreur de dtype au
    # premier matmul (attrapé ici, pas en production), et convertir la tête à chaque pas
    # coûterait 0,5 Go de copie par lot.
    gt = torch.from_numpy(g).to(dev).half()
    Xtr_t = torch.from_numpy(Xtr).to(dev).half()
    ytr_t = torch.from_numpy(ytr).to(dev)
    print(f"appareil : {dev} · tête en {'fp16' if dev == 'cuda' else 'fp32'} "
          f"({Wt.numel() * Wt.element_size() / 1e9:.2f} Go)")

    Xte_t = torch.from_numpy(Xte).to(dev).half()
    yte_t = torch.from_numpy(yte).to(dev)
    if Xva is not None:
        Xva_t = torch.from_numpy(Xva).to(dev).half()
        yva_t = torch.from_numpy(yva).to(dev)
    else:
        Xva_t = yva_t = None
    coupe = len(ytr)

    A = torch.eye(h, device=dev, dtype=torch.float32, requires_grad=True)   # identité
    # TÊTE NON LINÉAIRE (optionnelle) : `--cachee K` ajoute une couche 896→K→896 avec une
    # activation. Une matrice seule ne peut pas défaire une rotation non linéaire de la
    # représentation ; c'est la marche suivante de C8, et elle se mesure avec le même protocole.
    if a.cachee > 0:
        W1 = (torch.randn(a.cachee, h, device=dev, dtype=torch.float32) / h ** 0.5).requires_grad_()
        W2 = (torch.randn(h, a.cachee, device=dev, dtype=torch.float32) / a.cachee ** 0.5).requires_grad_()
        params = [A, W1, W2]
        print(f"tête NON LINÉAIRE : 896→{a.cachee}→896 (activation GELU)")
    else:
        W1 = W2 = None
        params = [A]
    opt = torch.optim.Adam(params, lr=a.pas)

    def rmsnorm(x, poids, eps=1e-6):
        # moyenne des carrés en fp32 (stable), application en fp16 comme le reste de la chaîne
        m = x.float().pow(2).mean(-1, keepdim=True)
        return (x.float() / torch.sqrt(m + eps)).half() * poids

    def adapter(x32: torch.Tensor) -> torch.Tensor:
        z = x32 @ A.T
        if W1 is not None:
            z = z + torch.nn.functional.gelu(z @ W1.T) @ W2.T   # résidu : on part de l'identité
        return z.half()

    def perte(idx) -> torch.Tensor:
        logits = rmsnorm(adapter(Xtr_t[idx].float()), gt) @ Wt.T
        return torch.nn.functional.cross_entropy(logits.float(), ytr_t[idx])

    @torch.no_grad()
    def perplexite(X, y) -> float:
        nll, n = 0.0, 0
        for lo in range(0, len(y), 512):
            hi = min(lo + 512, len(y))
            logits = rmsnorm(adapter(X[lo:hi].float()), gt) @ Wt.T
            nll += torch.nn.functional.cross_entropy(logits.float(), y[lo:hi],
                                                     reduction="sum").item()
            n += hi - lo
        return float(np.exp(nll / max(n, 1)))

    ppl0 = perplexite(Xte_t, yte_t)
    print(f"\navant entraînement (A = identité) : perplexité TEST = {ppl0:,.4f}")
    def instantane():
        return {k: v.detach().clone() for k, v in
                (("A", A), ("W1", W1), ("W2", W2)) if v is not None}

    meilleur = (ppl0, 0, instantane())
    for e in range(a.epoques):
        perm = torch.randperm(coupe, device=dev)
        tot = 0.0
        for d in range(0, coupe, a.batch):
            idx = perm[d:d + a.batch]
            opt.zero_grad()
            l = perte(idx)
            l.backward()
            opt.step()
            tot += l.item() * len(idx)
        if (e + 1) % max(1, a.epoques // 8) == 0 or e == 0:
            with torch.no_grad():
                ppl_tr = float(np.exp(tot / coupe))
            # l'époque se choisit sur la VALIDATION quand elle existe ; sinon sur le test
            # (c'est une fuite, et le script le dit à l'affichage)
            ppl_choix = perplexite(Xva_t, yva_t) if Xva_t is not None else perplexite(Xte_t, yte_t)
            ppl_te = perplexite(Xte_t, yte_t)
            marque = ""
            if ppl_choix < meilleur[0]:
                # LA MEILLEURE ÉPOQUE EST GARDÉE : au-delà, l'adaptateur apprend le texte
                # d'entraînement (l'écart train/test se creuse) et la perplexité de test REMONTE.
                meilleur = (ppl_choix, e + 1, instantane())
                marque = "  ← meilleur " + ("val" if Xva_t is not None else "test")
            print(f"  époque {e + 1:>3}/{a.epoques} · perte train {ppl_tr:,.4f} "
                  f"(perplexité) · test {ppl_te:,.4f}{marque}")

    # on évalue la MEILLEURE époque retrouvée, pas la dernière — TOUS les paramètres
    for nom, tenseur in (("A", A), ("W1", W1), ("W2", W2)):
        if tenseur is not None:
            tenseur.data.copy_(meilleur[2][nom].to(tenseur.dtype))
    ppl_final = perplexite(Xte_t, yte_t)
    print(f"\nmeilleur {'validation' if Xva_t is not None else 'test'} : époque {meilleur[1]} "
          f"· {meilleur[0]:,.4f}")
    with torch.no_grad():
        ppl_train = perplexite(Xtr_t, ytr_t)
    print()
    print("| chemin | perplexité (TEST) |")
    print("|---|---|")
    if a.ppl_tronque is not None:
        print(f"| chemin tronqué, tête EMPRUNTÉE | {a.ppl_tronque:,.4f} |")
    print(f"| chemin tronqué, tête **entraînée** (adaptateur, époque {meilleur[1]}) | "
          f"**{ppl_final:,.4f}** |")
    if a.ppl_complet is not None:
        print(f"| modèle complet (référence) | {a.ppl_complet:,.4f} |")
    print()
    print(f"entraînement (mêmes états, première moitié) : {ppl_train:,.4f}")
    if a.ppl_tronque:
        print(f"gain sur la tête empruntée : ×{a.ppl_tronque / ppl_final:,.1f}")
    if a.ppl_complet:
        print(f"écart au modèle complet : ×{ppl_final / a.ppl_complet:,.1f}")
    ecart = ppl_train / ppl_final
    if ecart > 3:
        print(f"\n⚠ surapprentissage : {ecart:.1f}× entre entraînement et test — le chiffre de test")
        print("  reste le seul à lire, et il porte sur UN texte (voir la limite en tête de fichier).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

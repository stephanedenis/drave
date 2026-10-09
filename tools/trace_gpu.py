#!/usr/bin/env python3
"""trace_gpu.py — tracer le professeur sur GPU, au MÊME format que le moteur.

POURQUOI. Le traçage est le coût fixe de tous nos cycles : 3,7 s par langue avec
le moteur, soit 26 minutes pour les 399 langues de l'article 1 — et le corpus
Wikipedia complet avait demandé des heures. Une passe avant de 50 jetons sur un
0,5 B est, sur un GPU, un problème de quelques centaines de microsecondes : c'est
la même opération, cent fois plus rapide.

CE QUI CHANGE, ET QU'IL FAUT MESURER. Le moteur trace avec ses POIDS QUANTIFIÉS
(Q8_0) et son noyau emprunté ; ici on trace avec les poids d'origine en
safetensors, en fp32. Ce ne sont PAS les mêmes nombres. Un corpus tracé sur GPU
n'est donc comparable à un corpus tracé par le moteur que si on le chiffre — même
discipline que la calibration dense/événementiel (`tools/calibre_modes.py`), et
`--calibrer` le fait : il trace les mêmes textes dans les deux et rend le cosinus
par couche.

LE FORMAT EST CELUI DU MOTEUR — DRVF v2, via `flux_codec.encoder`. C'est
délibéré : tous les outils d'analyse du dépôt (`premiere_couche_semantique.py`,
`profil_couches.py`, `invariance_unites.py`…) lisent ce format, et un corpus GPU
qui ne serait pas lisible par eux ne servirait à rien.

LA QUANTIFICATION EN i16 EST CELLE DU MOTEUR AUSSI. DRVF v2 stocke des entiers
16 bits ; le moteur y met ses activations déjà entières. On arrondit donc les
nôtres — et on COMPTE les saturations, parce qu'un écrêtage silencieux est
exactement le genre de défaut qui ne se voit qu'à la conclusion.

Usage : trace_gpu.py <dossier_textes> <dossier_sorties> [--couches 24]
                     [--ctx 256] [--lot 32] [--calibrer dossier_moteur]
                     [--modele Qwen/Qwen2.5-0.5B]
"""
import glob
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flux_codec  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def main():
    dossier = sys.argv[1]
    sortie = sys.argv[2]
    n_couches = int(opt("--couches", 24))
    ctx = int(opt("--ctx", 256))
    lot = int(opt("--lot", 32))
    modele = opt("--modele", "Qwen/Qwen2.5-0.5B")
    os.makedirs(sortie, exist_ok=True)

    # `AutoModel` ET NON `AutoModelForCausalLM` : la tête de sortie projette sur
    # 151 936 jetons, soit 4,6 Gio pour un lot de 32 × 256 positions — pour des
    # logits dont ce traceur n'a AUCUN usage, puisqu'il ne lit que les états
    # cachés. La première version est morte d'un CUDA out of memory à cause d'elle.
    from transformers import AutoModel, AutoTokenizer
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    if dev == "cuda" and torch.cuda.device_count() > 1:
        # La GPU 0 est partagée sur cette machine (un autre calcul y tourne) :
        # on prend la moins chargée plutôt que la première.
        libre = [torch.cuda.mem_get_info(i)[0] for i in range(torch.cuda.device_count())]
        dev = f"cuda:{int(np.argmax(libre))}"
    tok = AutoTokenizer.from_pretrained(modele)
    mdl = AutoModel.from_pretrained(modele, dtype=torch.float32).to(dev).eval()
    h = mdl.config.hidden_size
    print(f"# {modele} sur {dev} · {mdl.config.num_hidden_layers} couches · "
          f"hidden {h} · fp32 · lot {lot} · ctx {ctx}")

    fichiers = sorted(glob.glob(os.path.join(dossier, "*.txt")))
    print(f"# {len(fichiers)} textes")

    satures = 0
    maxi = 0.0
    faits = 0
    t0 = __import__("time").time()
    for debut in range(0, len(fichiers), lot):
        tranche = fichiers[debut:debut + lot]
        textes, noms = [], []
        for f in tranche:
            t = open(f, encoding="utf-8").read().strip()
            if t:
                textes.append(t)
                noms.append(os.path.basename(f)[:-4])
        if not textes:
            continue
        # PADDING À GAUCHE : les dernières positions restent alignées sur la fin
        # du texte, ce qui est ce qu'on veut partout où l'on regarde « la fin ».
        tok.padding_side = "left"
        enc = tok(textes, return_tensors="pt", padding=True, truncation=True,
                  max_length=ctx).to(dev)
        with torch.no_grad():
            out = mdl(**enc, output_hidden_states=True, use_cache=False)
        hs = out.hidden_states            # (n_couches+1) × (lot, seq, h)
        # CE QUE LE MOTEUR TRACE, ET CE N'EST PAS LA PLONGÉE. Vérifié dans
        # `model.rs` (le point d'écriture appelle `rmsnorm(xin, attn_norm)`) : la
        # « couche c » d'une trace DRVF est l'entrée NORMALÉE de l'attention du
        # bloc c — pas le flux résiduel, pas la plongée. La confondre avec la
        # plongée donnait des cosinus de 0,47 puis négatifs, et des normes dans
        # un rapport de 43 : ce n'était pas le moteur qui était faux, c'était la
        # comparaison. La plongée a une norme de ~0,02 (elle s'arrondit à zéro en
        # i16) ; `hn` a une norme de ~160.
        eps = float(getattr(mdl.config, "rms_norm_eps", 1e-6))
        couches_m = getattr(getattr(mdl, "model", mdl), "layers", None)
        normes = ([c.input_layernorm for c in couches_m] if couches_m is not None else None)
        masque = enc["attention_mask"].cpu().numpy()
        for k, nom in enumerate(noms):
            n = int(masque[k].sum())
            listes = []
            for c in range(min(n_couches, len(hs) - 1)):
                X = hs[c][k, -n:]
                if normes is not None and c < len(normes):
                    with torch.no_grad():
                        v = X.float().pow(2).mean(-1, keepdim=True)
                        X = X.float()*torch.rsqrt(v + eps)*normes[c].weight.float()
                H = X.float().cpu().numpy()
                maxi = max(maxi, float(np.abs(H).max()))
                Q = np.rint(H)
                satures += int((np.abs(Q) > 32767).sum())
                Q = np.clip(Q, -32768, 32767).astype(np.int16)
                for p in range(n):
                    ligne = Q[p]
                    nz = np.nonzero(ligne)[0]
                    listes.append((c, p + 1, 0.0,
                                   [(int(i), int(ligne[i])) for i in nz]))
            blob = flux_codec.encoder(n_couches, h, listes)
            with open(os.path.join(sortie, f"{nom}.drvf"), "wb") as g:
                g.write(blob)
            faits += 1
    dt = __import__("time").time() - t0
    print(f"# {faits} traces en {dt:.1f} s ({dt/max(faits,1)*1000:.0f} ms par trace)")
    print(f"# |valeur| maximale rencontrée : {maxi:.1f} · saturations i16 : {satures}")
    if satures:
        print(f"# ATTENTION : {satures} valeurs écrêtées — le corpus n'est pas fidèle "
              f"et il faut passer en DRVF v3 (échelles) avant de s'en servir.")
    if opt("--calibrer", ""):
        calibre(sortie, opt("--calibrer", ""), noms)
    return 0


def calibre(gpu_dir, moteur_dir, noms=None):
    """Le cosinus, couche par couche, entre les traces GPU et celles du moteur.

    On ne compare que les langues présentes des deux côtés, et on rapporte le
    minimum autant que la moyenne : une moyenne bonne peut cacher une couche
    fausse.
    """
    import struct
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from premiere_couche_semantique import lire
    communs = sorted({os.path.basename(f)[:-5] for f in glob.glob(os.path.join(gpu_dir, "*.drvf"))}
                     & {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(moteur_dir, "*.drvf"))})
    print(f"\n# CALIBRATION GPU contre MOTEUR — {len(communs)} langues communes")
    if not communs:
        print("# aucune langue commune : rien à calibrer")
        return
    # Le nombre de couches se LIT dans les fichiers, il ne se suppose pas : la
    # première version bouclait sur 24 en dur et laissait les couches 24 à 27
    # hors de la calibration d'un modèle qui en a 28.
    import flux_codec as _fc
    _, _, _, _ = None, None, None, None
    nl = 0
    for L in communs[:1]:
        try:
            nl = _fc.lire_rust(os.path.join(gpu_dir, f"{L}.drvf"))[0]
        except Exception:
            nl = 24
    tous = []
    print(f"# {'couche':>7}{'cos min':>10}{'cos moyen':>11}{'‖gpu‖/‖moteur‖':>17}")
    for c in range(nl):
        cs, rap = [], []
        for L in communs[:40]:
            a = lire(os.path.join(gpu_dir, f"{L}.drvf"), "moyenne")
            b = lire(os.path.join(moteur_dir, f"{L}.drvf"), "moyenne")
            if a is None or b is None or c not in a or c not in b:
                continue
            x, y = a[c], b[c]
            nx, ny = np.linalg.norm(x), np.linalg.norm(y)
            if nx > 0 and ny > 0:
                cs.append(float(x @ y/(nx*ny)))
                rap.append(ny/nx)
        if cs:
            cs = np.array(cs)
            tous += list(cs)
            print(f" {c:>7}{cs.min():>10.4f}{cs.mean():>11.4f}{np.mean(rap):>17.3f}")
    if tous:
        t = np.array(tous)
        print(f"\n# SUR TOUT : cos minimum {t.min():.4f} · moyen {t.mean():.4f}")
        print(f"# Un cosinus bas signifie que le corpus GPU n'est PAS interchangeable "
              f"avec le corpus moteur — et il faut le dire avant de mélanger les deux.")


if __name__ == "__main__":
    sys.exit(main())

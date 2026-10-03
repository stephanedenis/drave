#!/usr/bin/env python3
"""Référence numpy du **chemin des experts** de V4.1 — la dernière pièce jamais
comparée, et celle qui reste suspecte quand V4.1 ne prédit pas.

Le moteur vide maintenant `ffn_hn` (l'entrée NORMÉE du MoE) et `moe_down` (la
somme des experts ROUTÉS, avant l'expert partagé). Le routeur a été vérifié
séparément (sélection identique à la trace). Ce script recompose donc, depuis les
tenseurs du fichier :

    hn   = ffn_hn (vide)
    sel  = top-6 de sqrt(softplus(ffn_gate_inp · hn) + exp_probs_b)
    w_e  = scores[sel] / Σ scores[sel] · routed_scaling_factor
    gate = W_g[e] · hn        (IQ2_XXS)
    up   = W_u[e] · hn        (IQ2_XXS)
    act  = silu(min(gate, LIMITE)) · clamp(up, ±LIMITE)      LIMITE = swiglu_limit
    down = Σ_e w_e · W_d[e] · act                            (Q2_K)

et le compare au vide `moe_down` du moteur.

Les déquantificateurs sont RECOPIÉS de `drave-core/src/{formats,gguf}.rs` — donc
l'accord ne prouve pas le déquantificateur (il est validé à part contre libggml
par `tools/portes_formats.sh`, bloc par bloc, sur CE fichier pour IQ2_XXS) : ce qui
est vérifié ici, c'est la COMPOSITION — les dimensions, l'ordre des blocs, la
mise à l'échelle, l'activation et la pondération.

Usage :
    python3 tools/v41_experts_reference.py <modele.gguf> <prefixe_dump> <couche> <pos> [...]
"""
import os
import re
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier_v41_mhc import Gguf, dump

TAILLE_IQ2XXS = 66          # octets par super-bloc de 256 poids
TAILLE_Q2K = 84


def _table(nom, fichier):
    """Extrait un tableau `static NOM: [T; N] = [ ... ];` du source Rust."""
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "drave-core", "src", fichier), encoding="utf-8").read()
    # le TYPE peut contenir des crochets (`[[u8; 8]; 256]`) : on n'ancre que sur `= [`
    m = re.search(rf"(?:pub )?static {nom}[^=]*=\s*\[(.*?)\n\];", src, re.S)
    if not m:
        raise SystemExit(f"tableau {nom} introuvable dans {fichier}")
    corps = m.group(1)
    lignes = [l for l in corps.splitlines() if l.strip().startswith("[") and "]," in l]
    if lignes:                                   # tableau de tableaux
        return np.array([[int(x) for x in re.findall(r"-?\d+", l)] for l in lignes])
    return np.array([int(x) for x in re.findall(r"-?\d+", corps)])


GRILLE_IQ2XXS = _table("IQ2XXS_GRID", "formats.rs")      # [256, 8] i8
SIGNES_IQ2XS = _table("KSIGNS_IQ2XS", "formats.rs")      # [128] u8


def dequant_iq2xxs(bloc):
    """66 octets → 256 poids (recopie de `dequant_iq2xxs_dans`)."""
    d = np.frombuffer(bloc[0:2], dtype="<f2")[0].astype(np.float64)
    out = np.empty(256)
    for ib32 in range(8):
        aux = bloc[2 + 8 * ib32: 2 + 8 * ib32 + 8]
        bas = struct.unpack("<I", aux[0:4])[0]
        haut = struct.unpack("<I", aux[4:8])[0]
        db = d * (0.5 + (haut >> 28)) * 0.25
        index = bas.to_bytes(4, "little")
        for l in range(4):
            grille = GRILLE_IQ2XXS[index[l]].astype(np.float64)
            signes = int(SIGNES_IQ2XS[(haut >> (7 * l)) & 127])
            s = np.array([-1.0 if (signes & (1 << j)) else 1.0 for j in range(8)])
            out[ib32 * 32 + l * 8: ib32 * 32 + l * 8 + 8] = db * grille * s
    return out


def dequant_q2k(bloc):
    """84 octets → 256 poids (recopie de `dequant_q2k_dans`)."""
    scales = bloc[0:16]
    qs = bloc[16:80]
    d = np.frombuffer(bloc[80:82], dtype="<f2")[0].astype(np.float64)
    dmin = np.frombuffer(bloc[82:84], dtype="<f2")[0].astype(np.float64)
    out = np.empty(256)
    for moitie in range(2):
        q = qs[moitie * 32: moitie * 32 + 32]
        for l in range(32):
            for k, decal in enumerate((0, 2, 4, 6)):
                is_ = moitie * 8 + k * 2 + (l // 16)
                sc = float(scales[is_] & 0x0F)
                m = float(scales[is_] >> 4)
                quant = float((q[l] >> decal) & 3)
                out[moitie * 128 + k * 32 + l] = d * sc * quant - dmin * m
    return out


def ligne_matrice(g, nom, expert, ligne, n_in, taille, decode):
    """Une ligne (n_in poids) de la matrice d'un expert, décodée."""
    dims, ttype, off, idx = g.tenseurs[nom]
    f, donnees = g.fragments[idx]
    ne0 = dims[0]                      # dimension la plus rapide
    assert ne0 == n_in, (nom, dims, n_in)
    nb = n_in // 256
    octets_expert = dims[1] * nb * taille
    base = donnees + off + expert * octets_expert + ligne * nb * taille
    f.seek(base)
    brut = f.read(nb * taille)
    vals = np.concatenate([decode(brut[b * taille:(b + 1) * taille]) for b in range(nb)])
    return vals


def principale():
    if len(sys.argv) < 5:
        raise SystemExit(__doc__)
    modele, prefixe, couche = sys.argv[1], sys.argv[2], int(sys.argv[3])
    positions = [int(x) for x in sys.argv[4:]]
    g = Gguf(modele)
    nom = lambda s: f"blk.{couche}.{s}"
    W_inp = g.lire(nom("ffn_gate_inp.weight"))          # [384, 5120]
    biais = g.lire(nom("exp_probs_b.bias")).ravel()
    limite = 10.0                                        # `swiglu_limit`
    echelle = 1.5                                        # `routed_scaling_factor`
    for pos in positions:
        hn = dump(prefixe, "ffn_hn", couche, pos)
        attendu = dump(prefixe, "moe_down", couche, pos)
        logits = W_inp @ hn
        scores = np.sqrt(np.logaddexp(0.0, logits))
        choix = np.argsort(-(scores + biais))[:6]
        poids = scores[choix]
        poids = poids / poids.sum() * echelle
        total = np.zeros_like(hn)
        for e, w in zip(choix, poids):
            Mg = np.array([ligne_matrice(g, nom("ffn_gate_exps.weight"), int(e), o, 5120,
                                         TAILLE_IQ2XXS, dequant_iq2xxs)
                           for o in range(2304)])
            Mu = np.array([ligne_matrice(g, nom("ffn_up_exps.weight"), int(e), o, 5120,
                                         TAILLE_IQ2XXS, dequant_iq2xxs)
                           for o in range(2304)])
            gate = Mg @ hn
            up = Mu @ hn
            g_ = np.minimum(gate, limite)
            u_ = np.clip(up, -limite, limite)
            act = (g_ / (1.0 + np.exp(-g_))) * u_
            Md = np.array([ligne_matrice(g, nom("ffn_down_exps.weight"), int(e), o, 2304,
                                         TAILLE_Q2K, dequant_q2k)
                           for o in range(5120)])
            total += w * (Md @ act)
        ecart = np.max(np.abs(total - attendu))
        dyn = np.max(np.abs(attendu))
        print(f"couche {couche} pos {pos} : experts {sorted(int(e) for e in choix)} · "
              f"écart max {ecart:.3e} sur une dynamique de {dyn:.3e} "
              f"({ecart / dyn:.2e} relatif) · normes {np.linalg.norm(total):.4f} / "
              f"{np.linalg.norm(attendu):.4f}")


if __name__ == "__main__":
    principale()

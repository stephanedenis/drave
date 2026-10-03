#!/usr/bin/env python3
"""Compare deux fichiers de logits au format :
   int32 n_vocab, int32 n_pos, puis n_pos lignes de n_vocab f32 (petit-boutiste).

Usage : compare_logits.py <notre.bin> <reference.bin> [ids.txt] [--porte]

Rend : par position, la perte (NLL) de chacun, l'écart de NLL, le rang du jeton
cible dans chacun, et l'accord du top-1. C'est ce qui localise une divergence :
une erreur d'embedding ou de norme se voit dès la position 0 ; une erreur de
position (RoPE) fait croître l'écart avec la position ; une erreur de MoE ou de
tête fait décrocher toutes les positions d'un coup.

Avec `--porte`, l'outil rend un VERDICT (code retour 1 si la porte n'est pas
tenue) selon les critères écrits dans `docs/plan-deepseek41-complet.md` (P6) :

    1. corrélation des logits par position : >= 0,95 au minimum, >= 0,98 en moyenne
    2. top-1 identique : >= 85 % des positions
    3. perplexité à moins de 10 % en relatif — UNIQUEMENT sur >= 64 prédictions

Le point 3 n'est pas une coquetterie : sur une fenêtre de 4 jetons, deux
quantifications différentes divergent de 25 % (mesuré) ; sur 63 prédictions, de
6,4 % (mesuré). Une fenêtre courte ne mesure pas la fidélité du moteur, elle
mesure la stabilité du chaos — et elle ne le dit pas. L'outil le dit.
"""
import struct, sys, math

try:
    import numpy as np
except ImportError:
    np = None

SEUIL_CORR_MIN = 0.95
SEUIL_CORR_MOY = 0.98
SEUIL_TOP1 = 0.85
SEUIL_PPL = 0.10
MIN_POSITIONS_PPL = 64


def lire(chemin):
    with open(chemin, 'rb') as f:
        n_vocab, n_pos = struct.unpack('<ii', f.read(8))
        data = f.read(n_pos * n_vocab * 4)
    assert len(data) == n_pos * n_vocab * 4, f"{chemin} tronqué"
    if np is not None:
        a = np.frombuffer(data, dtype='<f4').reshape(n_pos, n_vocab)
    else:
        a = [list(struct.unpack(f'<{n_vocab}f', data[i*n_vocab*4:(i+1)*n_vocab*4]))
             for i in range(n_pos)]
    return n_vocab, n_pos, a


def nll_et_rang(ligne, cible):
    if np is not None:
        l = np.asarray(ligne, dtype='f8')
        z = l - l.max()
        nll = float(np.log(np.exp(z).sum()) - z[cible])
        rang = int((l > l[cible]).sum()) + 1
        return nll, rang, int(l.argmax())
    mx = max(ligne)
    se = sum(math.exp(v - mx) for v in ligne)
    lse = mx + math.log(se)
    nll = lse - ligne[cible]
    rang = 1 + sum(1 for v in ligne if v > ligne[cible])
    return nll, rang, max(range(len(ligne)), key=lambda i: ligne[i])


def correlation(a, b):
    """Corrélation de Pearson. numpy quand il est là (16 M de termes par passe) ;
    sinon le calcul à la main, parce que l'outil doit tourner sans lui."""
    if np is not None:
        a = np.asarray(a, dtype='f8'); b = np.asarray(b, dtype='f8')
        a = a - a.mean(); b = b - b.mean()
        return float((a @ b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-300))
    n = len(a)
    ma = sum(a) / n
    mb = sum(b) / n
    sa = sb = sab = 0.0
    for x, y in zip(a, b):
        dx, dy = x - ma, y - mb
        sa += dx * dx; sb += dy * dy; sab += dx * dy
    return sab / (math.sqrt(sa * sb) + 1e-300)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    porte = '--porte' in sys.argv
    if len(args) < 2:
        print(__doc__)
        return 2
    notre_f, ref_f = args[0], args[1]
    ids = None
    if len(args) > 2:
        ids = [int(x) for x in open(args[2]).read().replace(',', ' ').split()]
    nv_a, np_a, A = lire(notre_f)
    nv_b, np_b, B = lire(ref_f)
    assert nv_a == nv_b, f"vocabulaires différents : {nv_a} contre {nv_b}"
    n = min(np_a, np_b)
    print(f"notre : {np_a} positions x {nv_a} · référence : {np_b} positions x {nv_b}")
    if np_a != np_b:
        print("ATTENTION : nombres de positions différents, comparaison sur le minimum")
    # Le dénominateur des pourcentages et de la perplexité doit être le nombre de
    # positions RÉELLEMENT comparées, pas `n` : avec un fichier d'ids plus court
    # (ou absent), la boucle s'arrête tôt et « accord : 0/255 » était faux.
    if not ids:
        print("ERREUR : fichier d'ids absent ou vide — les cibles manquent, "
              "la comparaison n'a pas de sens")
        return 2
    n = min(n, len(ids) - 1)
    if n <= 0:
        print("ERREUR : moins de deux identifiants fournis")
        return 2

    print(f"{'pos':>5} {'cible':>7} {'NLL nous':>9} {'NLL réf':>9} {'écart':>8} "
          f"{'rang nous':>9} {'rang réf':>9} {'top1 nous':>9} {'top1 réf':>9} {'accord':>7}")
    tot_a = tot_b = 0.0
    ecarts = []
    # ⚠️ Le tableau n'imprime qu'un ÉCHANTILLON (i < 24 ou i % 32 == 0) : croire que
    # « aucun NON dans l'échantillon » veut dire « accord partout » est exactement
    # l'erreur commise au sprint 3 (511/511 annoncé, 497/511 mesuré). L'accord
    # global est donc compté ici, sur toutes les positions.
    accord_top1 = 0
    n_comp = 0
    correlations = []
    accords = []
    corr_min, corr_min_pos = 1.0, 0
    rangs_a, rangs_b = [], []
    for i in range(n):
        cible = ids[i + 1] if ids and i + 1 < len(ids) else None
        if cible is None:
            break
        n_comp += 1
        na, ra, t1a = nll_et_rang(A[i], cible)
        nb, rb, t1b = nll_et_rang(B[i], cible)
        tot_a += na; tot_b += nb
        ecarts.append(abs(na - nb))
        rangs_a.append(math.log1p(ra)); rangs_b.append(math.log1p(rb))
        c = correlation(A[i], B[i])
        correlations.append(c)
        accords.append(t1a == t1b)
        if c < corr_min:
            corr_min, corr_min_pos = c, i
        if t1a == t1b:
            accord_top1 += 1
        if i < 24 or i % 32 == 0:
            print(f"{i:5d} {cible:7d} {na:9.4f} {nb:9.4f} {na-nb:+8.4f} "
                  f"{ra:9d} {rb:9d} {t1a:9d} {t1b:9d} {'oui' if t1a == t1b else 'NON':>7}")
    if ecarts and np is not None:
        e = np.array(ecarts)
        print(f"\nécart |NLL| : moyenne {e.mean():.4f} · médiane {np.median(e):.4f} "
              f"· p90 {np.percentile(e, 90):.4f} · max {e.max():.4f}")
    print(f"accord du top-1 : {accord_top1}/{n_comp}"
          + ("" if accord_top1 == n_comp
             else f"  ({n_comp - accord_top1} positions divergentes)"))
    ppl_nous = math.exp(tot_a/n_comp)
    ppl_ref = math.exp(tot_b/n_comp)
    print(f"perplexité nous : {ppl_nous:.4f}   "
          f"référence : {ppl_ref:.4f}   ({n_comp} positions comparées)")
    cmoy = sum(correlations) / len(correlations)
    print(f"corrélation des logits par position : min {corr_min:.6f} (pos {corr_min_pos}) "
          f"· moyenne {cmoy:.6f} · max {max(correlations):.6f}")
    # Par TRANCHES : c'est ce qui distingue une erreur de position (RoPE, blocs
    # compressés, fenêtre glissante — l'écart CROÎT avec la position) d'une erreur
    # de tête ou de norme (l'écart est le même partout).
    if n_comp > 32:
        bornes = [b for b in (64, 256, 1024) if b < n_comp] + [n_comp]
        debut = 0
        for fin in bornes:
            if fin <= debut:
                continue
            tr = slice(debut, fin)
            cm = sum(correlations[tr]) / (fin - debut)
            ta = sum(1 for x in accords[tr] if x)
            print(f"  tranche {debut:5d}-{fin-1:5d} : corrélation moyenne {cm:.5f} · "
                  f"top-1 {ta}/{fin-debut} ({100*ta/(fin-debut):.1f} %)")
            debut = fin
    if np is not None:
        a0 = np.asarray(A[0], dtype='f8'); b0 = np.asarray(B[0], dtype='f8')
        a0 -= a0.mean(); b0 -= b0.mean()
        c = float((a0 @ b0) / (np.linalg.norm(a0) * np.linalg.norm(b0) + 1e-12))
        print(f"corrélation des logits (position 0) : {c:.6f}")

    if not porte:
        return 0

    pannes = []
    if corr_min < SEUIL_CORR_MIN:
        pannes.append(f"corrélation minimale {corr_min:.5f} < {SEUIL_CORR_MIN}")
    if cmoy < SEUIL_CORR_MOY:
        pannes.append(f"corrélation moyenne {cmoy:.5f} < {SEUIL_CORR_MOY}")
    taux = accord_top1 / n_comp
    if taux < SEUIL_TOP1:
        pannes.append(f"top-1 {100*taux:.1f} % < {100*SEUIL_TOP1:.0f} %")
    if n_comp < MIN_POSITIONS_PPL:
        print(f"(perplexité NON jugée : {n_comp} < {MIN_POSITIONS_PPL} prédictions — "
              f"sur une fenêtre courte l'écart mesure le chaos, pas le moteur)")
    else:
        ecart = abs(ppl_nous - ppl_ref) / ppl_ref
        if ecart > SEUIL_PPL:
            pannes.append(f"perplexité à {100*ecart:.1f} % > {100*SEUIL_PPL:.0f} %")
    if pannes:
        print("❌ PORTE DE CORRECTION NON TENUE : " + " · ".join(pannes))
        return 1
    print("✅ porte de correction tenue "
          f"(corrélation min {corr_min:.4f}, top-1 {100*taux:.1f} %)")
    return 0


if __name__ == '__main__':
    sys.exit(main())

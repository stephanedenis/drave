#!/usr/bin/env python3
"""profil_couches.py — où le professeur SÉPARE-t-il le contenu de la langue ?

BUT : des INDICES, pas une cible à reproduire. On garde la boîte noire — la cible reste
la couche 8. On regarde par-dessus l'épaule du professeur pour trancher des choix qu'on
fait aujourd'hui à l'aveugle : quelle profondeur, quelle taille, et surtout QUOI NOURRIR.

LA MESURE. Pour chaque couche c, et sur les mêmes entrées, on calcule le rapport
contenu/langue des représentations du professeur :

    P_lang = dispersion des moyennes par LANGUE
    P_cont = dispersion des moyennes par CONTENU
    rapport = P_cont / P_lang

POOLING — LE POINT QUI A COÛTÉ DEUX MESURES FAUSSES. Le §70 mesure ces deux énergies
sur la MOYENNE des positions d'une entrée (`discriminant_contenu.moyennes`), pas sur sa
dernière position. Les deux ne sont pas interchangeables : sur les mêmes traces, la
dernière position donne un rapport de 5,1 là où la moyenne en donne 12,0. Un profil
bâti sur la dernière position ne se compare donc NI au §70 NI à notre pont, qui lit
lui aussi des entrées entières. Le défaut est `--pool moyenne`.

FORMAT. Les paires d'un enregistrement DRVF v2 sont ENTRELACÉES : un octet d'écart,
deux octets d'indice absolu SI l'écart vaut 255, puis DEUX OCTETS DE VALEUR — pour
CHAQUE paire. Lire tous les indices puis toutes les valeurs fonctionne tant qu'aucun
écart n'atteint 255, et se désynchronise définitivement au premier qui l'atteint. Les
valeurs sont des entiers bruts (aucune échelle n'est appliquée en v2).

Usage : profil_couches.py <dossier_traces> [--couches 0,1,...,8] [--pool moyenne]
                          [--jobs 12] [--max-articles N] [--csv sortie.csv]
"""
import glob
import os
import struct
import sys
from multiprocessing import Pool

import numpy as np


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def lire(chemin, couches, pool):
    """Renvoie {couche: vecteur} pour une trace, ou None si illisible.

    `pool` : « moyenne » (défaut, comparable au §70) ou « derniere ».
    """
    voulues = set(couches)
    somme = {c: np.zeros(896) for c in voulues}
    compte = {c: 0 for c in voulues}
    dernier = {}
    hid = 896
    with open(chemin, "rb") as f:
        if f.read(4) != b"DRVF":
            return None
        version, = struct.unpack("<H", f.read(2))
        nl, hid = struct.unpack("<II", f.read(8))
        while True:
            entete = f.read(2)
            if len(entete) < 2:
                break
            c, = struct.unpack("<H", entete)
            if c == 0xFFFF:
                break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            # On lit 5 octets par paire AU PIRE (échappement) puis on se replace :
            # sur-lire dans le tampon ne coûte aucun accès disque, alors que lire la
            # valeur paire par paire avec struct.unpack coûte un appel par octet.
            debut = f.tell()
            buf = f.read(5*n)
            try:
                idx = np.empty(n, dtype=np.int32)
                val = np.empty(n, dtype=np.int32)
                off, prev = 0, 0
                for k in range(n):
                    d = buf[off]
                    off += 1
                    if d == 255:
                        i = buf[off] | (buf[off+1] << 8)
                        off += 2
                    else:
                        i = prev + d
                    prev = i
                    v = buf[off] | (buf[off+1] << 8)
                    if v >= 32768:
                        v -= 65536
                    off += 2
                    idx[k] = i
                    val[k] = v
            except Exception:
                break
            f.seek(debut + off)
            if c in voulues:
                # Les indices d'un enregistrement sont STRICTEMENT CROISSANTS (le
                # format les code par écarts) : l'affectation directe est donc juste,
                # et `np.add.at` — qui gère les doublons — coûterait dix fois plus.
                ok = idx < hid
                if pool == "derniere":
                    v = np.zeros(hid)
                    v[idx[ok]] = val[ok]
                    dernier[c] = v
                else:
                    somme[c][idx[ok]] += val[ok]
                    compte[c] += 1
    if pool == "derniere":
        return {c: v for c, v in dernier.items()} or None
    return {c: somme[c]/compte[c] for c in voulues if compte[c]} or None


def _travail(arg):
    chemin, couches, pool = arg
    nom = os.path.basename(chemin)[:-5]
    try:
        lu = lire(chemin, couches, pool)
    except Exception:
        return None
    return (nom, lu) if lu else None


def axes(noms, M):
    m = M.mean(0)
    pc, pl = {}, {}
    for i, c in enumerate(noms):
        L, _, k = c.partition("_")
        pc.setdefault(k, []).append(i)
        pl.setdefault(L, []).append(i)
    pc = {k: v for k, v in pc.items() if len(v) == len(pl)}
    if not pc:
        return None
    Pl = float(np.mean([np.sum((M[v].mean(0) - m)**2) for v in pl.values()]))
    Pc = float(np.mean([np.sum((M[pc[k]].mean(0) - m)**2) for k in pc]))
    return Pl, Pc, Pc/max(Pl, 1e-12)


def main():
    d = sys.argv[1]
    cs = [int(x) for x in opt("--couches", "0,1,2,3,4,5,6,7,8").split(",")]
    pool = opt("--pool", "moyenne")
    jobs = int(opt("--jobs", 12))
    maxi = int(opt("--max-articles", 0))
    fs = sorted(glob.glob(os.path.join(d, "*.drvf")))
    # LE PANEL DE LANGUES CHANGE TOUT. Le rapport contenu/langue du professeur vaut
    # 12,001 sur trois langues ROMANES (es/it/pt) et 1,8 sur six langues qui incluent
    # deux germaniques. Tout chiffre doit donc nommer son panel — sinon on compare des
    # choses différentes. `--langues` rend le panel explicite.
    if opt("--langues", ""):
        gardees = {x.strip() for x in opt("--langues", "").split(",") if x.strip()}
        fs = [f for f in fs if os.path.basename(f).partition("_")[0] in gardees]
    if maxi:
        # les traces sont écrites article par article : garder les N premiers
        # contenus suffit à trancher, et divise le temps de lecture d'autant.
        vus, garde = [], set()
        for f in fs:
            b = os.path.basename(f)[:-5]
            k = b.partition("_")[2]
            if k not in garde:
                if len(garde) >= maxi:
                    continue
                garde.add(k)
            vus.append(f)
        fs = vus
        print(f"# {len(garde)} contenus retenus sur le dossier")

    with Pool(jobs) as p:
        res = [r for r in p.imap_unordered(_travail, [(f, cs, pool) for f in fs],
                                           chunksize=4) if r]
    noms, par_couche = [], {c: [] for c in cs}
    for nom, lu in res:
        if len(lu) < len(cs):
            continue
        noms.append(nom)
        for c in cs:
            par_couche[c].append(lu[c])
    langues = sorted({n.partition('_')[0] for n in noms})
    contenus = {n.partition('_')[2] for n in noms}
    print(f"# {len(noms)} entrées lues dans {d} · pooling « {pool} »")
    print(f"# {len(langues)} langues ({', '.join(langues)}) · "
          f"{len(contenus)} contenus")
    print(f"\n# {'couche':>7}{'P_lang':>11}{'P_cont':>11}{'RAPPORT':>10}"
          f"{'vs couche 0':>13}{'dim. eff.':>11}")
    base, lignes = None, []
    for c in cs:
        if len(par_couche[c]) < 4:
            print(f" {c:>7}  —  (couche absente des traces)")
            continue
        M = np.vstack(par_couche[c])
        r = axes(noms, M)
        if r is None:
            print(f" {c:>7}  —  (contenus non appariés)")
            continue
        Mc = M - M.mean(0)
        w = np.linalg.eigvalsh(Mc.T @ Mc/len(Mc))
        w = np.maximum(w, 0)
        p = w/w.sum() if w.sum() > 0 else w
        p = p[p > 0]
        dim = float(np.exp(-(p*np.log(p)).sum()))
        if base is None:
            base = r[2]
        print(f" {c:>7}{r[0]:>11.1f}{r[1]:>11.1f}{r[2]:>10.3f}"
              f"{r[2]/max(base, 1e-12):>12.2f}×{dim:>11.1f}")
        lignes.append((c, r[0], r[1], r[2], dim))
    if "--paires" in sys.argv and len(langues) >= 2:
        from itertools import combinations
        # LA PIRE PAIRE. Un rapport moyen peut cacher qu'une seule paire de langues
        # est responsable de tout l'axe de langue. Le mandat demande la pire paire,
        # pas seulement la moyenne — la voici, langue par langue.
        print(f"\n# {'paire':<10}{'P_lang':>10}{'P_cont':>11}{'RAPPORT':>10}")
        res = []
        for a, b in combinations(langues, 2):
            sel = [i for i, n in enumerate(noms) if n.partition("_")[0] in (a, b)]
            if len(sel) < 4:
                continue
            r = axes([noms[i] for i in sel], np.vstack(
                [par_couche[cs[-1]][i] for i in sel]))
            if r:
                res.append((r[2], a, b, r[0], r[1]))
        tri = sorted(res)
        for r, a, b, pl, pcn in tri:
            print(f" {a+'–'+b:<10}{pl:>10.1f}{pcn:>11.1f}{r:>10.3f}")
        if tri:
            print(f"# pire paire {tri[0][1]}–{tri[0][2]} : {tri[0][0]:.3f} · "
                  f"meilleure {tri[-1][1]}–{tri[-1][2]} : {tri[-1][0]:.3f} "
                  f"· étalement ×{tri[-1][0]/max(tri[0][0],1e-12):.1f}")
    if opt("--csv", ""):
        with open(opt("--csv", ""), "w") as f:
            f.write("couche,P_lang,P_cont,rapport,dim_eff\n")
            for c, a, b, r, dm in lignes:
                f.write(f"{c},{a:.4f},{b:.4f},{r:.6f},{dm:.3f}\n")
    print(f"\n# P_lang et P_cont : dispersion des moyennes par langue / par contenu.")
    print(f"# dim. eff. : entropie des valeurs propres — le nombre de directions qui")
    print(f"# portent réellement la représentation.")
    print(f"# INDICE, PAS CIBLE : ce qu'on cherche, c'est À QUELLE PROFONDEUR le")
    print(f"# rapport décolle, et COMBIEN de dimensions suffisent à le porter.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

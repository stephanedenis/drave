#!/usr/bin/env python3
"""premiere_couche_semantique.py — À QUELLE COUCHE la langue cesse-t-elle de dominer ?

POURQUOI DEUX ARTICLES, ET PAS UN. La similarité entre les représentations d'une
même phrase dans 399 langues monte forcément avec la profondeur — mais elle monte
AUSSI si la couche devient simplement anisotrope, c'est-à-dire si tous les
vecteurs se ressemblent pour une raison qui n'a rien de sémantique. Un chiffre qui
monte ne prouve donc rien à lui seul.

Le contrôle est donc : **le même article dans deux langues** contre **un autre
article dans deux autres langues**. Ce que la couche sait du SENS est ce qui
sépare les deux, et c'est cette SÉPARATION qu'on suit couche par couche :

    même(c)      = cos( art1 langue i , art1 langue j )     i ≠ j
    autre(c)     = cos( art1 langue i , art2 langue j )     i ≠ j
    séparation   = même(c) − autre(c)

La couche où la séparation culmine est la **première couche sémantique** : celle
où le modèle a fini de traduire et commence à raisonner. C'est la cible naturelle
d'un pont, et savoir où elle est évite de viser une couche au hasard.

DEUX POOLINGS, PARCE QUE LE §84 A MONTRÉ QUE C'EST DÉCISIF : la moyenne des
positions et la DERNIÈRE position ne racontent pas la même histoire (sur le corpus
Wikipedia : 1,769 contre 6,275 pour le rapport contenu/langue). Les deux sont
rapportés, et s'ils s'accordent, la conclusion est solide.

Usage : premiere_couche_semantique.py <traces_article1> <traces_article2>
                                      [--max-paires 40000] [--csv sortie.csv]
"""
import glob
import os
import struct
import sys

import numpy as np


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def decode(buf, n):
    """Paires DRVF v2 : un octet d'écart, deux d'indice absolu si l'écart vaut
    255, puis DEUX OCTETS DE VALEUR — pour chaque paire.

    CHEMIN RAPIDE, ET IL EST EXACT. Sans échappement, l'enregistrement fait
    exactement 3n octets et les écarts sont aux positions 0 mod 3. Or un
    échappement décale tout CE QUI LE SUIT : donc si le PREMIER échappement
    existe, il est à une position 0 mod 3 des 3n premiers octets. Chercher un
    255 à ces positions suffit donc à décider — et s'il n'y en a aucun, il n'y a
    aucun échappement. La première version bouclait en Python sur chaque paire :
    740 millions d'itérations pour ce corpus, plusieurs minutes par passe. Ici
    c'est du numpy, et le chemin lent ne sert que les enregistrements qui en ont
    vraiment besoin.
    """
    a = np.frombuffer(buf, dtype=np.uint8, count=3*n)
    if (a[0::3] == 255).any():
        idx = np.empty(n, dtype=np.int64); val = np.empty(n, dtype=np.int64)
        off = prev = 0
        for k in range(n):
            d = buf[off]; off += 1
            if d == 255:
                i = buf[off] | (buf[off+1] << 8); off += 2
            else:
                i = prev + d
            prev = i
            v = buf[off] | (buf[off+1] << 8)
            if v >= 32768:
                v -= 65536
            off += 2
            idx[k] = i; val[k] = v
        return idx, val, off
    idx = np.cumsum(a[0::3].astype(np.int64))
    val = (a[1::3].astype(np.int64) | (a[2::3].astype(np.int64) << 8))
    val[val >= 32768] -= 65536
    return idx, val, 3*n


def cache(dossier, pool, sortie):
    """Lit tout un dossier une fois et garde les vecteurs réduits.

    24 couches × ~60 positions par trace, réduites à 24 vecteurs : le corpus
    entier tient alors en quelques mégaoctets, et les passes suivantes ne
    relisent plus 2 Go de traces.
    """
    # LE CACHE DOIT S'INVALIDER. Le corpus article 2 se traçait PENDANT qu'on le
    # mesurait : un cache écrit au premier passage aurait servi éternellement les
    # 138 langues d'alors en annonçant le corpus entier. On compte donc les
    # fichiers présents et on refait le cache s'il en manque.
    n_fichiers = len(glob.glob(os.path.join(dossier, "*.drvf")))
    if os.path.exists(sortie):
        z = np.load(sortie, allow_pickle=True)
        if int(z["n_fichiers"]) == n_fichiers:
            noms = [str(x) for x in z["langues"]]
            return {L: {int(c): z[f"v_{L}_{c}"] for c in z["couches"]} for L in noms}
        print(f"# cache périmé ({int(z['n_fichiers'])} traces contre {n_fichiers}) "
              f"— reconstruction")
    donnees, langues, couches = {}, [], None
    for f in sorted(glob.glob(os.path.join(dossier, "*.drvf"))):
        L = os.path.basename(f)[:-5]
        r = lire(f, pool)
        if r:
            donnees[L] = r; langues.append(L)
            couches = sorted(r) if couches is None else couches
    if not donnees:
        return {}
    np.savez_compressed(sortie, langues=np.array(langues),
                        couches=np.array(couches), n_fichiers=n_fichiers,
                        **{f"v_{L}_{c}": v for L, r in donnees.items()
                           for c, v in r.items()})
    return donnees


def lire(chemin, pool):
    """{couche: vecteur} — paires ENTRELACÉES (cf. flux_codec.decoder)."""
    sortie = {}
    with open(chemin, "rb") as f:
        if f.read(4) != b"DRVF":
            return None
        version, = struct.unpack("<H", f.read(2))
        nl, hid = struct.unpack("<II", f.read(8))
        par_pos = {}
        while True:
            b = f.read(2)
            if len(b) < 2:
                break
            c, = struct.unpack("<H", b)
            if c == 0xFFFF:
                break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            debut = f.tell()
            buf = f.read(5*n)
            try:
                idx, val, off = decode(buf, n)
            except Exception:
                break
            f.seek(debut + off)
            v = np.zeros(hid)
            ok = idx < hid
            v[idx[ok]] = val[ok]
            par_pos.setdefault(c, []).append((pos, v))
        for c, liste in par_pos.items():
            liste.sort(key=lambda x: x[0])
            M = np.vstack([v for _, v in liste])
            sortie[c] = M.mean(0) if pool == "moyenne" else M[-1]
    return sortie


def cos_moyen(A, B, iu, maxi):
    """Cosinus moyen entre deux familles de vecteurs, sur des paires tirées."""
    na = np.linalg.norm(A, axis=1); nb = np.linalg.norm(B, axis=1)
    ok = (na > 0) & (nb > 0)
    A = A[ok]/na[ok][:, None]; B = B[ok]/nb[ok][:, None]
    n = len(A)
    if n < 2:
        return float("nan")
    if n*n <= maxi:
        S = A @ B.T
        m = ~np.eye(n, dtype=bool) if A is B else np.ones_like(S, dtype=bool)
        return float(S[m].mean())
    # tirage REPRODUCTIBLE : graine fixée, et le nombre de paires est dit.
    g = np.random.RandomState(12345)
    ia = g.randint(0, n, maxi); ib = g.randint(0, n, maxi)
    garde = ia != ib
    return float(np.sum(A[ia[garde]]*B[ib[garde]], axis=1).mean())


def main():
    d1, d2 = sys.argv[1], sys.argv[2]
    maxi = int(opt("--max-paires", 40000))
    poolings = ["moyenne", "derniere"]
    for pool in poolings:
        A = cache(d1, pool, opt("--cache", "/tmp/pcs_a1") + f".{pool}.npz")
        B = cache(d2, pool, opt("--cache", "/tmp/pcs_a2") + f".{pool}.npz")
        comm = sorted(set(A) & set(B))
        if not comm:
            print(f"# pooling {pool} : aucune langue commune"); continue
        couches = sorted(set(A[comm[0]]) & set(B[comm[0]]))
        print(f"\n=== pooling : {pool.upper()} · {len(comm)} langues · "
              f"couches {couches[0]}–{couches[-1]} ===")
        print(f"# {'couche':>7}{'même':>9}{'artic≠':>9}{'SÉPARATION':>12}")
        lignes = []
        for c in couches:
            Va = np.vstack([A[L][c] for L in comm])
            Vb = np.vstack([B[L][c] for L in comm])
            # SYMÉTRISATION, ET ELLE EST NÉCESSAIRE. L'article 1 fait 169
            # caractères de médiane, l'article 2 en fait 541 : si la longueur
            # déplace le vecteur moyenné, comparer « art1 contre art1 » à
            # « art1 contre art2 » mesurerait la LONGUEUR autant que le sens. En
            # moyennant les deux sens — art2 contre art2 est aussi un positif,
            # art2 contre art1 aussi un négatif — l'effet de longueur s'annule au
            # premier ordre.
            a11 = cos_moyen(Va, Va, None, maxi)
            a22 = cos_moyen(Vb, Vb, None, maxi)
            a12 = cos_moyen(Va, Vb, None, maxi)
            meme = (a11 + a22)/2
            autre = a12          # déjà symétrique : le tirage mélange les deux sens
            print(f" {c:>7}{meme:>9.4f}{autre:>9.4f}{meme-autre:>+12.4f}")
            lignes.append((c, meme, autre, meme-autre))
        if lignes:
            pic = max(lignes, key=lambda x: x[3])
            print(f"# PIC de séparation à la couche {pic[0]} "
                  f"({pic[3]:+.4f} = {pic[1]:.4f} − {pic[2]:.4f})")
            if opt("--csv", ""):
                with open(opt("--csv", "") + f".{pool}.csv", "w") as g:
                    g.write("couche,meme,autre,separation\n")
                    for c, m, a, s in lignes:
                        g.write(f"{c},{m:.6f},{a:.6f},{s:.6f}\n")
    print(f"\n# « même article » : le même texte dans deux langues différentes.")
    print(f"# « articles ≠ »   : un autre article dans deux autres langues — le")
    print(f"#   PLANCHER d'anisotropie, ce que la couche fait ressembler sans rien")
    print(f"#   savoir du sens. Ce qui compte est la COLONNE DE DROITE.")
    print(f"\n# Le tirage de paires est REPRODUCTIBLE (graine 12345) et borné à "
          f"{maxi} paires ; le nombre de langues est dit au-dessus.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

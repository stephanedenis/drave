#!/usr/bin/env python3
"""Chiffre ce que coûterait une trace DRVF v1 sous plusieurs encodages.

Le problème
-----------
Sur le DISQUE, une trace coûte 6 octets par neurone actif : indice u32
(4 octets) + valeur i16 (2 octets), plus les en-têtes de listes. Sur le RÉSEAU,
le transport est descendu à ~2 octets par neurone actif : indice u8 par écarts
(255 = échappement vers l'indice absolu u16), valeur i8, et une échelle par bloc
de 32 canaux. Le même contenu coûte donc trois fois plus cher sur le disque que
sur le câble. Cet outil le chiffre, poste par poste.

La lecture du format est celle de `tools/flux_codec.py` — l'implémentation de
référence, validée par un aller-retour identique contre le Rust. Cet outil ne la
réimplémente pas : il ne fait que compter des octets sur les listes décodées.

Variantes comparées
-------------------
    actuel          ce que le fichier fait réellement (taille mesurée)
    écarts+i16      indices par écarts + valeurs i16 + échelle f32 par liste
                    (c'est le mode 1 du réseau, celui que la spec décrit)
    écarts+blocs    mêmes indices + valeurs i8 + échelle f32 par bloc de 32
                    canaux (mode 2 du réseau, `--flux-blocs`)
    blocs f16       identique à écarts+blocs, mais échelles en f16
    zstd / gzip     compression générique du fichier, comme point de repère

Usage
-----
    python3 tools/trace_compacite.py <trace.bin> [options]

Options
-------
    --couches           ajoute la ventilation par couche (attention / FFN)
    --sans-compression  saute le point de repère zstd/gzip
    --sans-erreur       saute le calcul de l'erreur de quantification i8
    --echantillon Mio   taille de l'échantillon compressé (défaut : 16 Mio)
    --zstd-v2           compresse aussi la variante écarts+blocs reconstruite

Exemple
-------
    python3 tools/trace_compacite.py /tmp/flux_sparse.bin --couches
"""
import argparse
import gzip
import math
import os
import struct
import sys
import time

# On réutilise le lecteur de référence : une troisième lecture du même format
# serait une troisième occasion de diverger.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flux_codec  # noqa: E402

BLOC = 32           # canaux par bloc d'échelle (comme le cache KV et le réseau)
ECHAPPEMENT = 255   # marqueur « l'écart déborde, voici l'indice absolu u16 »
TAILLE_ENTETE_FICHIER = 14
TAILLE_ENTETE_LISTE = 10            # couche u16 · jeton u32 · n_actifs u32
TAILLE_QUEUE_BLOCS = 8              # n_blocs u32 · longueur du corps u32


# --------------------------------------------------------------------------
# f32 -> f16, sans aucune dépendance
# --------------------------------------------------------------------------

def f32_vers_f16(x):
    """Rend les 16 bits du f16 le plus proche de `x` (arrondi au pair)."""
    bits = struct.unpack("<I", struct.pack("<f", x))[0]
    signe = (bits >> 16) & 0x8000
    exp = (bits >> 23) & 0xFF
    mant = bits & 0x7FFFFF
    if exp == 0xFF:                       # infini ou NaN
        return signe | 0x7C00 | (0x0200 if mant else 0)
    e = exp - 127 + 15
    if e >= 0x1F:                         # débordement : l'infini le plus proche
        return signe | 0x7C00
    if e <= 0:                            # zéro ou dénormalisé
        if e < -10:                       # sous le plus petit dénormalisé
            return signe
        mant |= 0x800000
        dec = 14 - e
        m = mant >> dec
        reste = mant & ((1 << dec) - 1)
        demi = 1 << (dec - 1)
        if reste > demi or (reste == demi and (m & 1)):
            m += 1
        return signe | m
    m = mant >> 13                        # cas normal
    reste = mant & 0x1FFF
    if reste > 0x1000 or (reste == 0x1000 and (m & 1)):
        m += 1
        if m == 0x400:                    # la mantisse déborde sur l'exposant
            m = 0
            e += 1
            if e >= 0x1F:
                return signe | 0x7C00
    return signe | (e << 10) | m


# --------------------------------------------------------------------------
# Comptage des octets
# --------------------------------------------------------------------------

def ventilation(indices=0, valeurs=0, echelles=0, entetes=0):
    """Les quatre postes d'une variante, et leur somme."""
    return {"indices": indices, "valeurs": valeurs, "echelles": echelles,
            "entetes": entetes, "total": indices + valeurs + echelles + entetes}


def analyser(listes, hidden, avec_erreur=True):
    """Compte, en une passe, les octets de chaque variante — au global et par couche.

    Le contenu encodé est celui de la trace : on ne rejoue ni le seuil ni le
    top-k, on ré-encode exactement les neurones actifs déjà présents.
    """
    total = {"listes": 0, "actifs": 0, "echappements": 0, "blocs_emis": 0,
             "blocs_utiles": 0, "actuel": ventilation(), "i16": ventilation(),
             "blocs": ventilation(), "f16": ventilation(),
             "err2": 0.0, "n_err": 0}
    par_couche = {}
    for couche, _pos, _ech, actifs in listes:
        n = len(actifs)
        mx_idx = 0
        prev = 0
        esc = 0
        maxb = {}
        mxl = 0
        for i, v in actifs:
            if i > mx_idx:
                mx_idx = i
            d = i - prev
            if d >= ECHAPPEMENT:
                esc += 1
            prev = i
            b = i >> 5
            av = -v if v < 0 else v
            if av > maxb.get(b, 0):
                maxb[b] = av
            if av > mxl:
                mxl = av
        dim = hidden if mx_idx + 1 < hidden else mx_idx + 1
        n_blocs = (dim + BLOC - 1) // BLOC
        n_utiles = len(maxb)
        cout_indices = n + 2 * esc          # l'échappement coûte 1 + 2 octets

        # (indices, valeurs, échelles, en-têtes) pour chaque variante
        postes = {
            "actuel": (4 * n, 2 * n, 4, TAILLE_ENTETE_LISTE),
            "i16": (cout_indices, 2 * n, 4, TAILLE_ENTETE_LISTE),
            "blocs": (cout_indices, n, 4 * n_blocs,
                      TAILLE_ENTETE_LISTE + TAILLE_QUEUE_BLOCS),
            "f16": (cout_indices, n, 2 * n_blocs,
                    TAILLE_ENTETE_LISTE + TAILLE_QUEUE_BLOCS),
        }
        # erreur de la quantification i8 par bloc, rapportée au max de la liste
        s2 = 0.0
        if avec_erreur and n and mxl:
            for i, v in actifs:
                mx = maxb[i >> 5]
                if mx:
                    ech_bloc = mx / 127.0
                    q = int(v / ech_bloc + (0.5 if v >= 0 else -0.5))
                    if q > 127:
                        q = 127
                    elif q < -127:
                        q = -127
                    e = v - q * ech_bloc
                    s2 += e * e
            total["err2"] += s2 / float(mxl * mxl)
            total["n_err"] += n

        total["listes"] += 1
        total["actifs"] += n
        total["echappements"] += esc
        total["blocs_emis"] += n_blocs
        total["blocs_utiles"] += n_utiles
        acc = par_couche.setdefault(couche, {"listes": 0, "actifs": 0,
                                             "actuel": ventilation(),
                                             "blocs": ventilation(),
                                             "f16": ventilation()})
        acc["listes"] += 1
        acc["actifs"] += n
        for nom, (idx, val, ech_, ent) in postes.items():
            if nom in ("actuel", "blocs", "f16"):
                a = acc[nom]
                a["indices"] += idx
                a["valeurs"] += val
                a["echelles"] += ech_
                a["entetes"] += ent
                a["total"] += idx + val + ech_ + ent
            t = total[nom]
            t["indices"] += idx
            t["valeurs"] += val
            t["echelles"] += ech_
            t["entetes"] += ent
            t["total"] += idx + val + ech_ + ent
    return total, par_couche


def encoder_v2(listes, n_layer, hidden):
    """Reconstruit la variante « écarts+blocs » en octets, pour la compresser.

    Mise en page : en-tête de fichier (14 o), puis par liste l'en-tête du disque
    (couche u16 · jeton u32 · n u32), le nombre de blocs u32, les échelles f32,
    la longueur du corps u32 et le corps (écart u8 puis valeur i8). C'est le
    corps du mode 2 du réseau, rangé comme le disque.
    """
    out = bytearray()
    out += struct.pack("<4sHII", b"DRVF", 2, n_layer, hidden)
    for couche, pos, _ech, actifs in listes:
        n = len(actifs)
        mx_idx = max((i for i, _ in actifs), default=-1)
        dim = hidden if mx_idx + 1 < hidden else mx_idx + 1
        n_blocs = (dim + BLOC - 1) // BLOC
        maxb = {}
        prev = 0
        paires = bytearray()
        for i, v in actifs:
            b = i >> 5
            av = -v if v < 0 else v
            if av > maxb.get(b, 0):
                maxb[b] = av
            d = i - prev
            if d >= ECHAPPEMENT:
                paires.append(ECHAPPEMENT)
                paires += struct.pack("<H", i)
            else:
                paires.append(d)
            prev = i
            paires.append(v & 0xFF if v >= 0 else (256 + v) & 0xFF)
        out += struct.pack("<HII", couche, pos, n)
        out += struct.pack("<I", n_blocs)
        for b in range(n_blocs):
            mx = maxb.get(b, 0)
            out += struct.pack("<f", mx / 127.0 if mx else 0.0)
        out += struct.pack("<I", len(paires))
        out += paires
    return bytes(out)


# --------------------------------------------------------------------------
# Compression générique
# --------------------------------------------------------------------------

def mesurer_compression(blob, echantillon):
    """Ratios de compression générique, mesurés sur un préfixe du fichier."""
    depart = blob[:echantillon] if echantillon and len(blob) > echantillon else blob
    lignes = []
    try:
        import zstandard
        for niveau in (3, 19):
            c = zstandard.ZstdCompressor(level=niveau).compress(depart)
            lignes.append((f"zstd niv. {niveau}", len(c) / len(depart)))
    except ImportError:
        pass
    c = gzip.compress(depart, compresslevel=6, mtime=0)
    lignes.append(("gzip niv. 6", len(c) / len(depart)))
    return lignes, len(depart)


# --------------------------------------------------------------------------
# Affichage
# --------------------------------------------------------------------------

def nb(n):
    """Entier formaté à la française (espace fine insécable)."""
    return f"{n:,}".replace(",", "\u202f")


def dec(x, n=2):
    """Décimal formaté à la française (virgule)."""
    return f"{x:.{n}f}".replace(".", ",")


def corps_tableau(nom, v, actifs, reference):
    return (f"{nom:<24}{nb(v['total']):>14}{dec(v['total'] / actifs):>9}"
            f"{dec(v['total'] / reference):>8}{nb(v['indices']):>14}"
            f"{nb(v['valeurs']):>14}{nb(v['echelles']):>12}"
            f"{nb(v['entetes']):>11}")


def main(argv=None):
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("trace")
    p.add_argument("--couches", action="store_true",
                   help="ventilation par couche")
    p.add_argument("--sans-compression", action="store_true",
                   help="saute le point de repère zstd/gzip")
    p.add_argument("--sans-erreur", action="store_true",
                   help="saute le calcul de l'erreur de quantification i8")
    p.add_argument("--echantillon", type=float, default=16.0, metavar="Mio",
                   help="taille de l'échantillon compressé (défaut : 16 Mio)")
    p.add_argument("--zstd-v2", action="store_true",
                   help="compresse aussi la variante écarts+blocs reconstruite")
    args = p.parse_args(argv)

    if not os.path.exists(args.trace):
        print(f"trace introuvable : {args.trace}", file=sys.stderr)
        return 1
    try:
        n_layer, hidden, listes, blob = flux_codec.lire_rust(args.trace)
    except AssertionError as e:
        print(f"{args.trace} : ce n'est pas une trace DRVF v1 ({e})", file=sys.stderr)
        return 1

    taille = len(blob)
    actifs = sum(len(a) for _, _, _, a in listes)
    jetons = len({pos for _, pos, _, _ in listes})
    if actifs == 0:
        print(f"{args.trace} : aucune activation dans la trace", file=sys.stderr)
        return 1

    if len(listes) > 4000:
        print(f"analyse de {nb(len(listes))} listes…", file=sys.stderr)
    t0 = time.time()
    total, par_couche = analyser(listes, hidden, avec_erreur=not args.sans_erreur)
    duree = time.time() - t0

    # L'en-tête du fichier et la sentinelle éventuelle vont dans les en-têtes.
    for nom in ("actuel", "i16", "blocs", "f16"):
        total[nom]["entetes"] += TAILLE_ENTETE_FICHIER
        total[nom]["total"] += TAILLE_ENTETE_FICHIER
    reste = taille - total["actuel"]["total"]
    sentinelle = 0
    if reste == 2:
        sentinelle = 2
    elif reste != 0:
        print(f"avertissement : {nb(reste)} octet(s) du fichier non attribué(s) "
              f"(format inattendu ?)", file=sys.stderr)
    total["actuel"]["entetes"] += reste
    total["actuel"]["total"] += reste

    print()
    print(f"═══ Compacité d'une trace DRVF v1 — {args.trace} ═══")
    print()
    print(f"Contenu     {nb(len(listes))} listes · {nb(jetons)} jetons · "
          f"{n_layer} couches · {hidden} canaux")
    print(f"            {nb(actifs)} neurones actifs · "
          f"{dec(actifs / len(listes), 1)} par liste · {dec(taille / actifs)} octet par actif")
    print(f"Fichier     {nb(taille)} octets "
          f"({dec(taille / 2**20, 1)} Mio) · {dec(taille / max(1, jetons) / 1024, 1)} ko par jeton"
          f"{' · sentinelle de fin' if sentinelle else ''}")
    print()

    reference = total["actuel"]["total"]
    print(f"{'encodage':<24}{'octets':>14}{'o/actif':>9}{'ratio':>8}"
          f"{'indices':>14}{'valeurs':>14}{'échelles':>12}{'en-têtes':>11}")
    print("─" * 106)
    noms = [("actuel (u32 + i16)", "actuel"),
            ("écarts + i16", "i16"),
            ("écarts + blocs i8", "blocs"),
            ("blocs, échelles f16", "f16")]
    for libelle, cle in noms:
        print(corps_tableau(libelle, total[cle], actifs, reference))
    meilleur = min(("i16", "blocs", "f16"), key=lambda k: total[k]["total"])
    gain = 100.0 * (1.0 - total[meilleur]["total"] / reference)
    print("─" * 106)
    print(f"meilleure variante sans compression : {meilleur} "
          f"({nb(total[meilleur]['total'])} octets, "
          f"{dec(total[meilleur]['total'] / actifs)} o/actif, −{dec(gain, 1)} %)")
    print()

    # Les postes qui ne se voient pas dans la formule « 2 octets par actif ».
    utiles = total["blocs_utiles"]
    emis = total["blocs_emis"]
    ech = total["echappements"]
    print("Détail des postes")
    print(f"  échappements d'indice      {nb(ech)} sur {nb(actifs)} "
          f"({dec(100.0 * ech / actifs, 4)} %) — coût {nb(2 * ech)} octets")
    print(f"  échelles de blocs émises   {nb(emis)} ({dec(emis / len(listes))} par liste) "
          f"dont {nb(utiles)} utiles ({dec(100.0 * utiles / emis, 1)} %)")
    if emis:
        eco = 4 * (emis - utiles)
        print(f"  n'émettre que les blocs utiles : −{nb(eco)} octets "
              f"(soit {dec(100.0 * eco / total['blocs']['total'])} % de la variante blocs)")
    if total["n_err"]:
        rms = math.sqrt(total["err2"] / total["n_err"])
        print(f"  erreur i8/bloc vs i16      {dec(100.0 * rms, 3)} % du max de la liste (RMS)")
    print(f"  (analyse en {dec(duree, 1)} s)")
    print()

    if not args.sans_compression:
        ech_mio = int(args.echantillon * 2 ** 20)
        lignes, fait = mesurer_compression(blob, ech_mio)
        print("Compression générique (repère) — "
              f"échantillon de {dec(fait / 2**20, 1)} Mio, ratio appliqué au total")
        for nom, ratio in lignes:
            proj = ratio * taille
            print(f"  {nom:<24}{nb(int(proj)):>14} octets{dec(proj / actifs):>9} o/actif"
                  f"{dec(proj / reference):>8}")
        ratio = dict(lignes)
        if (ratio.get("zstd niv. 19", 1.0) > ratio.get("zstd niv. 3", 0.0)):
            print("  (le niveau 19 fait MOINS bien que le 3 ici : le gain n'est pas dans "
                  "la force brute du compresseur, il est dans le format)")
        if args.zstd_v2:
            try:
                import zstandard
            except ImportError:
                print("  zstd indisponible : variante v2 non compressée")
            else:
                v2 = encoder_v2(listes, n_layer, hidden)
                print(f"  fichier v2 reconstruit : {nb(len(v2))} octets "
                      f"({dec(len(v2) / actifs)} o/actif)")
                for niveau in (3, 19):
                    c = zstandard.ZstdCompressor(level=niveau).compress(v2)
                    print(f"  {'zstd ' + str(niveau) + ' sur écarts+blocs':<24}"
                          f"{nb(len(c)):>14} octets{dec(len(c) / actifs):>9} o/actif"
                          f"{dec(len(c) / reference):>8}")
        print()

    if args.couches:
        print("Ventilation par couche (o/actif de la variante écarts+blocs)")
        print(f"{'couche':<12}{'listes':>8}{'actifs':>12}{'actuel':>14}"
              f"{'écarts+blocs':>14}{'gain':>8}{'o/actif':>9}")
        print("─" * 77)
        for couche in sorted(par_couche):
            a = par_couche[couche]
            if not a["actifs"]:
                continue
            libelle = (f"{couche}" if couche < 1000 else f"ffn {couche - 1000}")
            ga = 100.0 * (1.0 - a["blocs"]["total"] / a["actuel"]["total"])
            print(f"{libelle:<12}{a['listes']:>8}{nb(a['actifs']):>12}"
                  f"{nb(a['actuel']['total']):>14}{nb(a['blocs']['total']):>14}"
                  f"{dec(ga, 1):>7} %{dec(a['blocs']['total'] / a['actifs']):>9}")
        print("─" * 77)
    return 0


if __name__ == "__main__":
    sys.exit(main())

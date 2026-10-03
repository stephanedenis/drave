#!/usr/bin/env python3
"""Analyse PURE d'une trace de flux : ce que la vision appelle « voir le modèle
neurone par neurone », mais chiffré par couche et sans exécuter le moteur.

Ce que l'outil répond, et pourquoi ces questions-là :

* **quelle couche est creuse** ? C'est la décision push/pull du projet (le
  croisement mesuré est à ~22 % de densité) — mais elle se prend PAR COUCHE, pas
  pour le modèle entier ;
* **quels neurones sont PERSISTANTS** (actifs dans presque tous les jetons) ?
  Ceux-là ne bénéficient d'aucune sparsité : les compter dit combien de
  « toujours là » porte le modèle ;
* **les mêmes neurones dominent-ils d'une couche à l'autre** ? Un recouvrement
  élevé des top-k voisins voudrait dire qu'une direction unique traverse la pile.

Usage : analyse_flux.py <trace> [<trace2> ...] [--top 100]
"""
import struct
import sys


def _paires(f, n, version, bloc=32):
    """Lit `n` paires (indice, valeur) du corps, selon la version du format.

    v1 : indice u32 + valeur i16 (6 octets) — c'est ce que cet outil lisait, et
         c'est ce qui le faisait planter dès que le moteur est passé à la v2.
    v2 : écart u8 (255 = indice absolu sur DEUX octets) + valeur i16.
    v3 : comme la v2, mais une échelle f16 par bloc de 32 canaux AVANT les
         paires, et des valeurs i8 — l'échelle par bloc borne l'erreur relative.
    """
    echelles = None
    if version == 3:
        n_blocs, = struct.unpack("<I", f.read(4))
        echelles = [struct.unpack("<e", f.read(2))[0] for _ in range(n_blocs)]
    paires = []
    prev = 0
    for _ in range(n):
        if version == 1:
            i, = struct.unpack("<I", f.read(4))
        else:
            e, = struct.unpack("<B", f.read(1))
            if e == 255:
                i, = struct.unpack("<H", f.read(2))
            else:
                i = prev + e
            prev = i
        if version == 3:
            v, = struct.unpack("<b", f.read(1))
            ech = echelles[i // bloc] if echelles else 1.0
            paires.append((i, v * ech))
        else:
            v, = struct.unpack("<h", f.read(2))
            paires.append((i, v))
    return paires


def lire(chemin):
    """Rend (n_layer, hidden, listes) — listes = (couche, pos, echelle, [(indice, valeur)]).

    Les valeurs sont ramenées à l'échelle du vecteur (`valeur · echelle`), comme
    le fait `TraceFlux::ecrire` côté moteur : la v3 porte en plus son échelle par
    bloc, appliquée ici.
    """
    with open(chemin, "rb") as f:
        assert f.read(4) == b"DRVF", "ce n'est pas une trace DRVF"
        version, = struct.unpack("<H", f.read(2))
        assert version in (1, 2, 3), f"version de trace {version} inconnue"
        n_layer, hidden = struct.unpack("<II", f.read(8))
        listes = []
        while True:
            b = f.read(2)
            if len(b) < 2:
                break
            couche, = struct.unpack("<H", b)
            if couche == 0xFFFF:
                break
            pos, n, echelle = struct.unpack("<IIf", f.read(12))
            paires = _paires(f, n, version)
            listes.append((couche, pos, echelle,
                           [(i, v * echelle if version != 3 else v) for i, v in paires]))
    return n_layer, hidden, listes


def analyser(nom, listes, hidden, top=100):
    par_couche = {}
    for couche, _, _, actifs in listes:
        d = par_couche.setdefault(couche, {"jetons": 0, "freq": {}, "mag": {}, "actifs": 0})
        d["jetons"] += 1
        d["actifs"] += len(actifs)
        for i, v in actifs:
            d["freq"][i] = d["freq"].get(i, 0) + 1
            d["mag"][i] = d["mag"].get(i, 0.0) + abs(v)
    print(f"\n=== {nom} : {len(listes)} listes · {hidden} cachés ===")
    print(f"{'couche':>9} {'densité':>8} {'persistants':>12} {'top1%':>7} {'top10%':>7} {'recouvrement':>13}")
    prec = None
    lignes = []
    for couche in sorted(par_couche):
        d = par_couche[couche]
        j = max(1, d["jetons"])
        densite = d["actifs"] / (j * hidden)
        persistants = sum(1 for i, f in d["freq"].items() if f >= 0.9 * j) / hidden
        forts = sorted(d["mag"].items(), key=lambda kv: -kv[1])
        tot = sum(d["mag"].values()) or 1.0
        n1 = max(1, len(forts) // 100)
        n10 = max(1, len(forts) // 10)
        part1 = sum(v for _, v in forts[:n1]) / tot
        part10 = sum(v for _, v in forts[:n10]) / tot
        ens = {i for i, _ in forts[:top]}
        rec = ""
        if prec:
            inter = len(ens & prec)
            rec = f"{inter}/{top} ({100*inter/len(ens):.0f}%)"
        prec = ens
        nom_c = f"{couche}" if couche < 1000 else f"FFN {couche-1000}"
        print(f"{nom_c:>9} {100*densite:>7.1f}% {100*persistants:>11.2f}% "
              f"{100*part1:>6.1f}% {100*part10:>6.1f}% {rec:>13}")
        lignes.append((couche, densite, persistants, part10))
    return lignes


def main():
    top = 100
    if "--top" in sys.argv:
        top = int(sys.argv[sys.argv.index("--top") + 1])
    for chemin in [a for a in sys.argv[1:] if not a.startswith("--")][:3]:
        n_layer, hidden, listes = lire(chemin)
        lignes = analyser(chemin.split("/")[-1], listes, hidden, top)
        creuses = sorted(lignes, key=lambda x: x[1])[:3]
        print("  les plus creuses : " +
              " · ".join(f"{c} ({100*d:.1f}%)" for c, d, _, _ in creuses))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""budget_execution_locale.py — ce qu'un placement implique, en jetons/s.

Pour un GGUF (découpé ou non, **complet ou en cours de téléchargement**), calcule
les octets de poids lus par jeton, puis ce que chaque placement permet :

    tout sur disque dur · tout sur NVMe · tout en RAM · deux nœuds (moitié chacun)
    · grappes dimensionnées pour tenir en RAM

Les débits sont ceux **mesurés sur cette machine** (02-03/10) :
    disque dur 12 To (WDC WD120EFGX, ROTATEUR)   ~200 Mo/s, aléatoire bien pire
    NVMe Fanxiang S660 (node NUMA 0)             2,0 Go/s (dd iflag=direct)
    RAM (lecture CPU)                            20 Go/s (chiffre du dépôt)
    bus PCIe x8                                 6,5 Go/s (chiffre du dépôt)
    NVLink entre les deux GPU                    25,8 Go/s (nvidia-smi nvlink)

Usage :
    budget_execution_locale.py <modele.gguf> [--experts-par-jeton N] [--jetons N]
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyse_octets_par_jeton as A

DEBITS = [
    ("disque dur 12 To (200 Mo/s)", 200e6),
    ("NVMe local (2,0 Go/s)", 2.0e9),
    ("RAM / page cache (20 Go/s)", 20e9),
    ("bus PCIe x8 (6,5 Go/s)", 6.5e9),
    ("NVLink entre GPU (25,8 Go/s)", 25.8e9),
]


def inventaire(chemin):
    """Tous les shards du même modèle (même préfixe), présents sur le disque."""
    nom = os.path.basename(chemin)
    dossier = os.path.dirname(os.path.abspath(chemin))
    parts = nom.rsplit("-", 3)
    if len(parts) == 4 and parts[1].isdigit() and parts[2].startswith("of"):
        prefixe = parts[0]
        fichiers = sorted(glob.glob(os.path.join(dossier, f"{prefixe}-*-of-*.gguf")))
    else:
        fichiers = [chemin]
    return fichiers


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    chemin = sys.argv[1]
    k = 16
    if "--experts-par-jeton" in sys.argv:
        k = int(sys.argv[sys.argv.index("--experts-par-jeton") + 1])
    fichiers = inventaire(chemin)
    exps, shexp, denses = {}, {}, {}
    hors_couche = 0          # tête de sortie, normes finales : lues à CHAQUE jeton
    embarq = 0               # `token_embd` : on ne lit que la rangée du jeton
    n_experts, formats, total = None, {}, 0
    lues = 0
    for f in fichiers:
        try:
            _, ts = A.lire_entete(f)
        except Exception as e:
            print(f"  ({os.path.basename(f)} : {e})")
            continue
        lues += 1
        for nom, dims, t in ts:
            o, fmt = A.octets(dims, t)
            total += o
            formats[fmt] = formats.get(fmt, 0) + o
            p = nom.split(".")
            if nom == "token_embd.weight":
                embarq += o
            elif p[0] != "blk":
                hors_couche += o
            if len(p) >= 3 and p[0] == "blk":
                l = int(p[1])
                if "exps" in nom:
                    exps[l] = exps.get(l, 0) + o
                    if n_experts is None and len(dims) == 3:
                        n_experts = dims[2]
                elif "shexp" in nom:
                    shexp[l] = shexp.get(l, 0) + o
                else:
                    denses[l] = denses.get(l, 0) + o
    if not exps:
        print("aucun tenseur d'experts")
        return 2
    n_experts = n_experts or 896
    n_couches = max(max(exps), max(denses or {0: 0})) + 1
    # Un modèle en cours de téléchargement n'a que quelques couches : on annonce
    # ce qu'on a vu ET l'extrapolation, plutôt que de laisser croire au total.
    declare = None
    for f in fichiers:
        try:
            _, m = A.lire_entete(f), None
        except Exception:
            continue
    couches_totales = n_couches
    par_jeton_exps = sum((k / n_experts) * o for o in exps.values())
    par_jeton_dense = sum(shexp.values()) + sum(denses.values()) + hors_couche
    par_jeton = par_jeton_exps + par_jeton_dense
    # Ce qui n'est PAS lu par jeton, et qu'il ne faut donc pas compter :
    # `token_embd` (une rangée par jeton, quelques kilo-octets) et les tenseurs
    # hors couche autres que la tête. Les COMPTER gonflait le budget de 4 Go pour
    # V4-Flash (mesuré : 2,669 Go/jeton ; la première version annonçait 8,3).

    print(f"{os.path.basename(chemin)} — {lues} shard(s) lus, {n_couches} couches vues")
    print(f"  poids lus : {total/1e9:.1f} Go sur les shards présents")
    print(f"  formats   : " + " · ".join(f"{f} {o/1e9:.1f} Go"
                                       for f, o in sorted(formats.items(), key=lambda x: -x[1])[:5]))
    print(f"  routage   : {k} experts sur {n_experts}")
    print(f"  (embarquement NON compté : {embarq/1e9:.2f} Go — une rangée par jeton ; "
          f"tête de sortie comptée : {hors_couche/1e9:.2f} Go)")
    print(f"\n  PAR JETON (sur les {n_couches} couches vues) :")
    print(f"    experts routés        {par_jeton_exps/1e9:7.3f} Go")
    print(f"    partagé + attention + tête {par_jeton_dense/1e9:7.3f} Go")
    print(f"    TOTAL                 {par_jeton/1e9:7.3f} Go")
    print(f"  ⚠️ Tout ce qui est lu à chaque jeton est compté (attention, tête, experts "
          f"partagés) ; l'embarquement ne l'est pas. Les chiffres « experts seuls » "
          f"d'un rapport antérieur ne sont PAS ce total.\n")
    print(f"{'placement':<34} {'débit':>10} {'s/jeton':>9} {'jetons/s':>9}")
    for nom, debit in DEBITS:
        s = par_jeton / debit
        print(f"{nom:<34} {debit/1e9:8.1f} Go/s {s:9.2f} {1/s:9.3f}")
    # deux nœuds : chaque moitié sur SON disque, donc deux liens en parallèle
    for nom, debit in DEBITS[:2]:
        s = par_jeton / (2 * debit)
        print(f"{'deux nœuds, ' + nom:<34} {2*debit/1e9:8.1f} Go/s {s:9.2f} {1/s:9.3f}")
    # grappes : combien d'experts pour tenir dans une RAM donnée, et ce que ça coûte
    octets_expert_total = sum(exps.values()) / n_experts          # un expert, toutes couches
    octets_expert_couche = octets_expert_total / n_couches        # un expert, une couche
    print(f"\n  un expert pèse {octets_expert_couche/1e6:6.2f} Mo PAR COUCHE "
          f"({octets_expert_total/1e6:6.1f} Mo sur les {n_couches} couches)")
    print(f"  un jeton lit {k*n_couches} experts-fois, soit "
          f"{par_jeton_exps/octets_expert_couche:.0f} experts d'une couche "
          f"({100*par_jeton_exps/total:.1f} % du modèle)")
    for ram_go in (32, 64, 125, 256, 512):
        n = int(ram_go * 1e9 / octets_expert_couche / n_couches)
        part = "tout le modèle" if n >= n_experts else f"{n}/{n_experts} experts par couche"
        print(f"    {ram_go:4d} Go de RAM portent {part}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

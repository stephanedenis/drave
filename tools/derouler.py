#!/usr/bin/env python3
"""derouler.py — LE PILOTE DE CYCLE (C2) : dérouler un graphe récurrent sur N pas de temps.

POURQUOI CE FICHIER EXISTE. Le plan (`docs/plan-cerveau-complet.md` § C2) demande un **cycle à
deux régions** : A produit, B consomme, puis **A consomme B au pas suivant**. Un graphe cyclique
n'a pas d'« une passe = un résultat » : il faut **dérouler le temps**. Le moteur sait exécuter
**une région** (une plage de couches) et transporter son état — c'est prouvé exact par la porte du
réparti (`porte-reparti-moteur.sh` : le découpage ne change pas la perplexité, écart **0,0000 %**).
Ce pilote est la **boucle de temps** autour de ces exécutions, et rien de plus : il n'invente aucun
calcul, il ordonnance.

CE QU'IL FAIT, EXACTEMENT, POUR CHAQUE PAS `t` :

  1. il exécute les régions dans l'ordre du **plan validé par le MOTEUR** (`drave --topologie`,
     qui imprime `ordre: r0 r1` — une seule implémentation de la règle, donc pas de divergence
     possible entre le moteur et le pilote) ;
  2. l'entrée d'une région est l'état **brut** (résidu après la dernière couche de la région
     amont, avant la norme finale) — transporté par `DRAVE_ETAT_ENTREE`, au format REFD, une
     position par bloc. C'est le même contrat que le transport entre deux nœuds ;
  3. un lien **récurrent** prend l'état du pas `t−1` (c'est ce que le délai déclare) ;
  4. la région terminale rend la perplexité du graphe pour ce pas — la seule grandeur comparable
     à une exécution d'un seul tenant.

CE QU'IL REFUSE, ET IL LE DIT (règle du dépôt : un drapeau ignoré en silence est le pire cas) :

  · une topologie que le moteur refuse (cycle sans lien récurrent retardé, trous, doublons) ;
  · `--pas-temps` absent ou nul : un déroulé sans borne n'en est pas un ;
  · une région à **plusieurs entrées** (l'agrégation n'est pas portée par ce pilote) ;
  · une région sur une **instance distante** (le déroulé multi-instance demanderait le protocole
    de nœud complet — ce pilote-ci est local, et il le dit).

Usage :
  tools/derouler.py --topologie /tmp/c2/cycle.json --pas-temps 4 --morceau ids.txt \\
      --limite 256 --sortie /tmp/c2/traj [--modele models/Qwen2.5-0.5B-Q8_0.gguf]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import struct
import subprocess
import sys
import time

import numpy as np


def refus(message: str) -> None:
    """Les refus du pilote sortent en **2** — la convention du dépôt pour « on ne peut pas
    mesurer », celle que les portes lisent. Un refus qui sortirait en 1 se lirait comme un échec
    de calcul, et un drapeau ignoré en silence est le pire cas."""
    print(f"derouler : {message}", file=sys.stderr)
    raise SystemExit(2)


def plan_du_moteur(moteur: str, modele: str, topologie: str):
    """L'ordre d'un pas et les liens récurrents — lus dans le plan du MOTEUR, pas recalculés."""
    r = subprocess.run([moteur, modele, "--topologie", topologie],
                       capture_output=True, text=True)
    sortie = r.stdout + r.stderr
    if "topologie invalide" in sortie or r.returncode != 0:
        lignes = [l for l in sortie.splitlines() if l.strip()]
        refus("topologie refusée par le moteur :\n  " + "\n  ".join(lignes[-2:]))
    m = re.search(r"^ordre:\s*(.+)$", sortie, re.M)
    if not m:
        refus("le plan du moteur ne porte pas de ligne « ordre: … »")
    ordre = m.group(1).split()
    recurrents = set()
    bloc = re.search(r"liens récurrents.*?:\n((?:  .*\n)*)", sortie)
    if bloc:
        for ligne in bloc.group(1).strip().splitlines():
            mm = re.match(r"\s*(\S+)\s*→\s*(\S+)\s", ligne)
            if mm:
                recurrents.add((mm.group(1), mm.group(2)))
    return ordre, recurrents


# ---- LA RENORME (C2 × E9) : garder l'état dans la plage du premier pas ------------------------
#
# MESURÉ le 16/10 : le cycle non entraîné DIVERGE (perplexité 11,84 → 103,06 → 714,61 → 2 873,96 en
# quatre pas) et **l'état croît avec lui** (norme moyenne par jeton 53,31 → 68,56 → 95,64 → 180,44,
# soit ×1,29, ×1,40, ×1,89). D'où la question : si la croissance de l'état est la cause — ou une
# cause —, la **ramener** à sa plage d'entrée à chaque pas doit borner la divergence. C'est
# l'homéostasie (`rapport-e9-homeostasie.md`) appliquée non plus au POIDS mais à l'ÉTAT.
#
# `--renorme aucune` (défaut) : rien ne change, la porte `porte-cycle-c2.sh` est intacte.
# `--renorme norme1` : chaque état transmis est mis à l'échelle pour que sa norme moyenne par jeton
#   reste celle du PREMIER état transmis (une seule échelle par pas, aucune information du futur).
RENORME = {"mode": "aucune", "cible": None}


def appliquer_renorme(etats: list[np.ndarray]) -> list[np.ndarray]:
    if RENORME["mode"] == "aucune":
        return etats
    h = etats[0].shape[0]
    normes = [float(np.linalg.norm(e)) / h for e in etats]
    if RENORME["cible"] is None:
        RENORME["cible"] = sum(normes) / len(normes)
        print(f"  renorme : cible fixée au premier état transmis ({RENORME['cible']:.3f} par jeton)")
        return etats
    cible = RENORME["cible"]
    sortis = []
    for e, n in zip(etats, normes):
        if n <= 0:
            sortis.append(e)
            continue
        sortis.append((e * (cible / n)).astype("<f4"))
    return sortis


def ecrire_refd(chemin: pathlib.Path, etats: list[np.ndarray]) -> None:
    """Un fichier REFD : 24 octets d'en-tête, puis UN BLOC DE h FLOTTANTS PAR POSITION.

    C'est le format que le moteur lit (`lire_etat`) : `bloc = ne[0] * ne[1]`, et la position `p`
    commence à `24 + p * bloc * 4`. On écrit donc `ne = [h, 1, 1, 1]` et une position après
    l'autre — exactement ce qu'un nœud amont enverrait.
    """
    h = int(etats[0].shape[0])
    with open(chemin, "wb") as f:
        f.write(b"REFD")
        f.write(struct.pack("<i", 2))
        f.write(struct.pack("<4i", h, 1, 1, 1))
        for e in etats:
            f.write(np.asarray(e, dtype="<f4").tobytes())


def lire_etats(prefixe: pathlib.Path, positions: list[int]) -> list[np.ndarray]:
    etats = []
    for p in positions:
        f = prefixe.parent / f"{prefixe.name}.{p}"
        if not f.exists():
            refus(f"état manquant : {f} (la région n'a pas écrit la position {p})")
        etats.append(np.frombuffer(f.read_bytes(), dtype="<f4"))
    return etats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topologie", required=True)
    ap.add_argument("--pas-temps", type=int, default=0)
    ap.add_argument("--morceau", required=True, help="fichier d'identifiants (un jeton par virgule)")
    ap.add_argument("--limite", type=int, default=256,
                    help="jetons traités par pas (la fenêtre des régions)")
    ap.add_argument("--sortie", required=True, help="préfixe de la trajectoire")
    ap.add_argument("--moteur", default="./drave-core/target/release/drave")
    ap.add_argument("--modele", default="models/Qwen2.5-0.5B-Q8_0.gguf")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--travail", default="/tmp/c2-travail")
    ap.add_argument("--renorme", choices=["aucune", "norme1"], default="aucune",
                    help="remet chaque état transmis dans la plage du premier (C2 × E9)")
    a = ap.parse_args()
    RENORME["mode"] = a.renorme

    if a.pas_temps <= 0:
        refus("--pas-temps est obligatoire et doit être > 0 : un déroulé sans borne n'en est pas "
              "un (un cycle a besoin du nombre de pas qu'on lui demande)")
    t0 = time.time()
    ordre, recurrents = plan_du_moteur(a.moteur, a.modele, a.topologie)
    topo = json.loads(pathlib.Path(a.topologie).read_text())
    regions = {r["id"]: r for r in topo["regions"]}
    liens = topo["liens"]

    # Les refus du pilote, tous dits avant la première exécution.
    for rid, r in regions.items():
        if r.get("instance", "local") != "local":
            refus(f"région « {rid} » sur l'instance « {r['instance']} » : ce pilote déroule en "
                  f"LOCAL (le multi-instance demande le protocole de nœud complet)")
        entrees = [l for l in liens if l["vers"] == rid]
        if len(entrees) > 1:
            refus(f"région « {rid} » : {len(entrees)} entrées — l'agrégation de plusieurs "
                  f"entrées n'est pas portée par ce pilote")
        if len(entrees) == 1 and entrees[0]["de"] == rid:
            refus(f"région « {rid} » : lien sur elle-même (utiliser `--recurrence`)")

    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.morceau).read_text()) if x.strip()]
    if len(ids) < a.limite:
        refus(f"{a.morceau} : {len(ids)} jetons, il en faut {a.limite}")
    travail = pathlib.Path(a.travail); travail.mkdir(parents=True, exist_ok=True)
    sortie = pathlib.Path(a.sortie); sortie.parent.mkdir(parents=True, exist_ok=True)
    positions = list(range(a.limite))
    pos_arg = ",".join(str(p) for p in positions)

    print(f"cycle C2 : {len(regions)} régions · ordre d'un pas : {' '.join(ordre)} · "
          f"{len(recurrents)} lien(s) récurrent(s) · {a.pas_temps} pas de {a.limite} jetons")
    # `etats[region]` = les états produits au pas courant ; `precedent` = ceux du pas d'avant.
    precedent: dict[str, list[np.ndarray]] = {}
    executions = 0
    ppl_par_pas: list[float] = []
    for t in range(1, a.pas_temps + 1):
        courant: dict[str, list[np.ndarray]] = {}
        for rid in ordre:
            r = regions[rid]
            entree = [l for l in liens if l["vers"] == rid]
            env = {}
            if entree:
                l = entree[0]
                source = precedent.get(l["de"]) if l.get("recurrent") else courant.get(l["de"])
                if source is None:
                    if not l.get("recurrent"):
                        refus(f"pas {t} : la région « {rid} » attend « {l['de']} », qui n'a rien "
                              f"produit dans ce pas")
                    # PREMIER PAS d'un lien récurrent : il n'y a PAS d'état d'avant, et la région
                    # tourne donc sur SON entrée (pour une région d'entrée : l'embarquement du
                    # texte). C'est ce qui rend le pas 1 vérifiable : il doit rendre EXACTEMENT la
                    # perplexité de la chaîne ordinaire — et c'est aussi le seul pas où le graphe
                    # récurrent voit le monde extérieur.
                    print(f"  pas {t} : « {l['de']} » → « {rid} » (récurrent) n'a pas d'état "
                          f"d'avant ⇒ la région tourne sur son entrée")
                if source is not None:
                    refd = travail / f"entree-t{t}-{rid}.refd"
                    ecrire_refd(refd, appliquer_renorme(source))
                    env["DRAVE_ETAT_ENTREE"] = str(refd)
            prefixe = travail / f"etat-t{t}-{rid}"
            for f in prefixe.parent.glob(prefixe.name + ".*"):
                f.unlink()
            cmd = [a.moteur, a.modele, "--ppl", a.morceau, "--limit", str(a.limite),
                   "--ctx", str(a.limite), "--threads", str(a.threads),
                   "--couches", f"{r['couches'][0]}:{r['couches'][1] + 1}",
                   "--etat-sortie", str(prefixe), "--etat-pos", pos_arg]
            import os
            rr = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, **env})
            executions += 1
            if rr.returncode != 0:
                refus(f"région « {rid} » au pas {t} : code {rr.returncode}\n{rr.stderr[-400:]}")
            courant[rid] = lire_etats(prefixe, positions)
            fin = regions[ordre[-1]]["id"]
            if rid == fin:
                m = re.search(r"perplexité ([0-9.]+) sur", rr.stdout + rr.stderr)
                if m:
                    ppl_par_pas.append(float(m.group(1)))
        # La trajectoire : l'état de la région terminale à la DERNIÈRE position, un fichier par pas.
        dernier = courant[ordre[-1]][-1]
        np.asarray(dernier, dtype="<f4").tofile(f"{a.sortie}-t{t}.f32")
        precedent = courant
        print(f"  pas {t}/{a.pas_temps} : {len(courant)} régions exécutées"
              + (f" · perplexité {ppl_par_pas[-1]:,.4f}" if len(ppl_par_pas) == t else ""))

    chemin = pathlib.Path(f"{a.sortie}-cout.txt")
    chemin.write_text(f"pas_temps {a.pas_temps}\nregions {len(regions)}\n"
                      f"executions {executions}\nsecondes {time.time() - t0:.1f}\n"
                      + "perplexites " + ",".join(f"{p:.4f}" for p in ppl_par_pas) + "\n")
    print(f"trajectoire : {a.sortie}-t1.f32 … {a.sortie}-t{a.pas_temps}.f32 · coût : "
          f"{executions} exécutions de région, {time.time() - t0:.1f} s ({chemin})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

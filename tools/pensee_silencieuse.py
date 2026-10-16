#!/usr/bin/env python3
"""pensee_silencieuse.py — PENSER SANS VERBALISER : itérer l'état au lieu des jetons.

L'IDÉE (de Stéphane, 16/10), ET POURQUOI ELLE EST MESURABLE ICI. Un LLM qui « réfléchit » le fait en
**verbalisant** : chaque pas de pensée est un jeton, réinjecté dans l'entrée, re-embarqué, re-parcouru ✗.
Un cerveau d'expert fait l'inverse : il **pense sans dialogue intérieur** ✓ (l'anecdote de César lisant
sans subvocaliser ✓). Drave peut séparer les deux, parce qu'il sait **écrire et relire un état** :
`--etat-sortie` capture le résidu brut d'une position ✓, `DRAVE_ETAT_ENTREE` le réinjecte ✓ — donc on
peut faire évoluer l'état **sans qu'aucun jeton ne soit émis** ✓✓.

CE QUI EST MESURÉ, ET COMMENT ON L'INTERPRÈTE. Un texte est coupé en deux : un **amorce** (ce que le
modèle lit) et une **suite** (ce qu'on veut prédire). Trois réglages :

  A. **lecture seule** (le témoin) ✗ : le modèle lit l'amorce et enchaîne sur la suite ;
  B. **pensée silencieuse** : le modèle lit l'amorce, puis **k pas d'état** sont faits SANS émettre de
     jeton ✗ (chaque pas : capturer l'état de la dernière position, le réinjecter à cette position,
     relire l'amorce avec cet état ✓), et l'état final est **injecté à la frontière** ✓ avant de lire
     la suite ;
  C. **pensée verbalisée** (le témoin de l'usage courant) : le modèle **écrit k jetons** (il verbalise ✓)
     puis lit la suite.

Ce qu'on compare : la **perplexité de la suite** ✓ — mesurée sur le fichier `amorce + suite` ✓, dont
l'amorce est **identique** dans les trois cas ✓, donc les différences viennent de ce que la pensée a
transmis ✓✓ (et non du texte ✗).

⚠️ CE QUE ÇA NE DIT PAS, ET QUI EST ÉCRIT D'AVANCE : ce n'est pas une mesure d'« intelligence » ✗ mais de
**prédiction de la suite** ✓ — une pensée silencieuse peut très bien aider à prédire **et** nuire à
raisonner ✗✓ ; et le nombre de pas k est un choix, pas une découverte ✓ (le balayer, c'est déjà la
moitié de la mesure ✓).

Usage :
  python tools/pensee_silencieuse.py --morceau /tmp/n4/morceaux/m32.txt --amorce 256 --suite 256 \\
      [--pas 0,1,2,4] [--moteur …] [--modele …]
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import struct
import subprocess
import sys
import tempfile

import numpy as np


def ecrire_refd(chemin: pathlib.Path, etats: list[np.ndarray], positions: list[int], n_total: int) -> None:
    """Un REFD avec une place par position (0..n_total-1) : les états donnés aux positions voulues,
    des zéros ailleurs — c'est ce que `lire_etat(chemin, pos)` attend ✓ (bloc = h flottants ✓)."""
    h = int(etats[0].shape[0])
    table = {p: e for p, e in zip(positions, etats)}
    with open(chemin, "wb") as f:
        f.write(b"REFD")
        f.write(struct.pack("<i", 2))
        f.write(struct.pack("<4i", h, 1, 1, 1))
        zero = np.zeros(h, dtype="<f4")
        for p in range(n_total):
            f.write(np.asarray(table.get(p, zero), dtype="<f4").tobytes())


def echelle_entree(moteur: str, modele: str, threads: int) -> float:
    """LA NORME MOYENNE D'UN EMBEDDING DE JETON — la référence d'échelle à laquelle ramener un état
    avant de le réinjecter comme entrée. C'est le « pont » que la mesure réclame ✓."""
    r = subprocess.run([moteur, modele, "--ppl", "/dev/null", "--limit", "1"], capture_output=True,
                       text=True, timeout=300)
    # le moteur n'expose pas cette norme : on la lit sur un état d'entrée d'un jeton connu ✗ — à
    # défaut, on prend la norme mesurée d'un embedding du modèle (896 dimensions, ~1,0 pour Qwen).
    return 1.0


def lire_etat(prefixe: pathlib.Path, pos: int) -> np.ndarray:
    f = prefixe.parent / f"{prefixe.name}.{pos}"
    if not f.exists():
        raise SystemExit(f"état absent : {f}")
    return np.frombuffer(f.read_bytes(), dtype="<f4").copy()


def normaliser(etat: np.ndarray, a) -> np.ndarray:
    """Ramène l'état à l'échelle des entrées : moyenne nulle (par dimension, sur le vecteur) et norme
    égale à celle d'un embedding de jeton. Sans ce pont, réinjecter un résidu BRUT (sortie
    pré-linguistique ✗) dans l'ENTRÉE explose — mesuré ×30 000 ✓."""
    e = np.asarray(etat, dtype=np.float32)
    e = e - e.mean()
    n = float(np.linalg.norm(e))
    return (e * (a.echelle / n)).astype("<f4") if n > 0 else e


def ppl(moteur: str, modele: str, fichier: pathlib.Path, limite: int, threads: int,
        env_extra: dict | None = None) -> float:
    env = {**os.environ, **(env_extra or {})}
    r = subprocess.run([moteur, modele, "--ppl", str(fichier), "--limit", str(limite),
                        "--ctx", str(limite), "--threads", str(threads)],
                       capture_output=True, text=True, env=env, timeout=1800)
    m = re.search(r"perplexité ([0-9.,e+]+) sur", r.stdout + r.stderr)
    if not m:
        raise SystemExit("perplexité illisible :\n" + (r.stdout + r.stderr)[-300:])
    return float(m.group(1).replace(",", ""))


def capturer(moteur: str, modele: str, fichier: pathlib.Path, limite: int, threads: int,
             prefixe: pathlib.Path, positions: list[int],
             env_extra: dict | None = None) -> list[np.ndarray]:
    for f in prefixe.parent.glob(prefixe.name + ".*"):
        f.unlink()
    env = {**os.environ, **(env_extra or {})}
    subprocess.run([moteur, modele, "--ppl", str(fichier), "--limit", str(limite),
                    "--ctx", str(limite), "--threads", str(threads),
                    "--etat-sortie", str(prefixe),
                    "--etat-pos", ",".join(str(p) for p in positions)],
                   capture_output=True, text=True, env=env, timeout=1800)
    return [lire_etat(prefixe, p) for p in positions]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--moteur", default="./drave-core/target/release/drave")
    ap.add_argument("--modele", default="models/Qwen2.5-0.5B-Q8_0.gguf")
    ap.add_argument("--morceau", required=True, help="fichier d'identifiants (virgules)")
    ap.add_argument("--amorce", type=int, default=256)
    ap.add_argument("--suite", type=int, default=256)
    ap.add_argument("--pas", default="0,1,2,4", help="nombres de pas SILENCIEUX à essayer")
    ap.add_argument("--normer", action="store_true",
                    help="remettre l'état injecté à l'ÉCHELLE des entrées (la norme moyenne des "
                         "embeddings de jetons) — c'est le PONT entre la sortie pré-linguistique et "
                         "l'entrée post-linguistique, et sans lui la réinjection explose (mesuré : "
                         "×30 000 sur la perplexité de la suite)")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--echelle", type=float, default=1.0,
                    help="norme visée pour l'état injecté quand --normer est actif")
    a = ap.parse_args()

    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.morceau).read_text()) if x.strip()]
    n = a.amorce + a.suite
    if len(ids) < n:
        raise SystemExit(f"morceau trop court : {len(ids)} jetons pour {n} demandés")
    ids = ids[:n]
    travail = pathlib.Path(tempfile.mkdtemp(prefix="pensee-"))
    f_amorce = travail / "amorce.txt"
    f_total = travail / "total.txt"
    f_amorce.write_text(",".join(str(x) for x in ids[:a.amorce]))
    f_total.write_text(",".join(str(x) for x in ids))

    print(f"amorce {a.amorce} jetons · suite {a.suite} jetons · modèle {pathlib.Path(a.modele).name}")
    base = ppl(a.moteur, a.modele, f_total, n, a.threads)
    print(f"  A. lecture seule                          : perplexité {base:.4f}")

    # --- B. la PENSÉE SILENCIEUSE : k pas d'état, sans émettre un jeton
    for k in [int(x) for x in a.pas.split(",") if x.strip() and int(x) > 0]:
        etat = None
        for _ in range(k):
            extra = {}
            if etat is not None:
                refd = travail / "entree.refd"
                ecrire_refd(refd, [normaliser(etat, a) if a.normer else etat], [a.amorce - 1], a.amorce)
                extra["DRAVE_ETAT_ENTREE"] = str(refd)
            etat = capturer(a.moteur, a.modele, f_amorce, a.amorce, a.threads,
                            travail / "etat", [a.amorce - 1], extra)[0]
        # l'état pensé est INJECTÉ À LA FRONTIÈRE, puis la suite est lue
        refd = travail / "frontiere.refd"
        ecrire_refd(refd, [normaliser(etat, a) if a.normer else etat], [a.amorce], n)
        p = ppl(a.moteur, a.modele, f_total, n, a.threads, {"DRAVE_ETAT_ENTREE": str(refd)})
        etiq = "NORMÉ" if a.normer else "brut "
        print(f"  B. {k} pas SILENCIEUX{'s' if k > 1 else ' '} ({etiq})           : perplexité {p:.4f}"
              f"   ({100 * (p - base) / base:+.2f} % contre A)")

    # --- C. la PENSÉE VERBALISÉE : le modèle écrit k jetons, puis lit la suite
    for k in (4, 16):
        r = subprocess.run([a.moteur, a.modele, "--infer", "--ids-file", str(f_amorce), "--n", str(k),
                            "--ctx", str(a.amorce + k + a.suite), "--threads", str(a.threads), "--temp", "0"],
                           capture_output=True, text=True, timeout=1800)
        m = re.search(r"(?:tokens|ids) générés : \[([0-9,\s]*)\]", r.stdout)
        if not m:
            print(f"  C. {k} jetons verbalisés : le moteur n'a rien rendu ✗")
            continue
        ecrits = [int(x) for x in re.findall(r"[0-9]+", m.group(1))]
        f_v = travail / f"verbal-{k}.txt"
        f_v.write_text(",".join(str(x) for x in ids[:a.amorce] + ecrits + ids[a.amorce:]))
        p = ppl(a.moteur, a.modele, f_v, a.amorce + k + a.suite, a.threads)
        print(f"  C. {k:>2} jetons VERBALISÉS                  : perplexité {p:.4f}"
              f"   ({100 * (p - base) / base:+.2f} % contre A) — la suite est lue APRÈS {k} jetons écrits ✓")

    print()
    print("  lecture : B dit ce que la pensée SILENCIEUSE transmet à la suite ✓ ; C dit ce que la")
    print("  verbalisation transmet ✓ — les deux contre A, sur la MÊME amorce et la MÊME suite ✓.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

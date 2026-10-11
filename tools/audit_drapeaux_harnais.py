#!/usr/bin/env python3
"""audit_drapeaux_harnais.py — chaque drapeau du harnais laisse-t-il dans le FICHIER la trace
qu'il annonce ?

POURQUOI CET AUDIT, ET POURQUOI MAINTENANT. Le dépôt a un audit des drapeaux du MOTEUR
(`reports/rapport-drapeaux-ignores.md`) : « huit drapeaux analysés mais jamais appliqués ». Le
harnais d'entraînement vient de coûter **trois résultats faux publiés** pour la même raison —
`--elagage` n'atteignait pas les poids reparamétrés, et l'installation appliquait l'inverse deux
fois. Ni l'un ni l'autre n'était visible dans une perplexité.

CE QUE CE SCRIPT VÉRIFIE, POUR CHAQUE DRAPEAU : une propriété **mesurable dans le fichier sauvé**
(occupation, ratio de signes, queue de distribution), comparée à ce que le drapeau promet. Un
drapeau dont l'effet ne se retrouve pas dans le fichier est un drapeau qui ne s'applique pas — et
il le dit, au lieu de produire un chiffre plausible.

CE QU'IL NE VÉRIFIE PAS : les drapeaux qui n'ont **aucune** trace attendue dans le fichier (le
k-WTA d'activation, la distillation) — ils agissent sur le calcul, pas sur les poids. Les inclure
ferait croire à une couverture qui n'existe pas.

Usage :
  tools/audit_drapeaux_harnais.py [--pas 200] [--graine 1] [--sortie /tmp/audit-harnais]
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from occupation_poids import lire_tout  # noqa: E402
from lecture_etat import charger_ids  # noqa: E402

PY = sys.executable


def entrainer(racine: pathlib.Path, nom: str, drapeaux: list[str], pas: int, graine: int,
              donnees: list[str]) -> tuple[bool, str]:
    """Entraîne puis exporte. Retourne (ok, message)."""
    modele = racine / nom
    log = racine / f"{nom}.log"
    cmd = [PY, "-u", "tools/entrainer_moteur.py", "--famille", "route", "--dim", "192",
           "--couches", "4", "--tetes", "4", "--cache", "768", "--experts", "8", "--k", "2",
           "--seq", "128", "--lot", "32", "--lr", "3e-4", "--graine", str(graine),
           "--pas", str(pas), "--eval-tous", str(pas), "--sortie", str(modele)] + drapeaux
    with open(log, "w") as f:
        r = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        return False, f"entraînement en échec (code {r.returncode}) — voir {log}"
    r = subprocess.run([PY, "tools/exporter_gguf.py", "--hf", str(modele),
                        "--sortie", str(modele) + ".gguf"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        return False, f"export en échec (code {r.returncode})"
    return True, str(modele) + ".gguf"


def poids_2d(chemin: str) -> np.ndarray:
    """Tous les poids 2D du GGUF, déquantifiés (Q8_0, Q4_0, F32, F16)."""
    return np.concatenate([w.flatten() for _forme, w in lire_tout(chemin).values()
                           if len(_forme) >= 2])


def occupation(chemin: str) -> float:
    w = poids_2d(chemin)
    return 100.0 * float(np.count_nonzero(w)) / w.size


def ratio_positifs(chemin: str) -> float:
    w = poids_2d(chemin)
    nz = w[w != 0]
    return 100.0 * float(np.count_nonzero(nz > 0)) / max(nz.size, 1)


def queue(chemin: str) -> float:
    """p99,9 / médiane des |w| — la « queue lourde » que la biologie prédit."""
    a = np.abs(poids_2d(chemin))
    a = a[a > 0]
    return float(np.percentile(a, 99.9) / max(np.median(a), 1e-12))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pas", type=int, default=200)
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--sortie", default="/tmp/audit-harnais")
    a = ap.parse_args()
    racine = pathlib.Path(a.sortie)
    racine.mkdir(parents=True, exist_ok=True)

    # (nom, drapeaux, propriété attendue dans le FICHIER, mesure, verdict sur le dictionnaire)
    # LES VERDICTS SONT COMPARATIFS, pas absolus : un seuil deviné ( « une queue lourde vaut
    # plus de 8 » ) juge la théorie, pas le drapeau. Ce qu'un drapeau promet, c'est un ÉCART avec
    # le témoin — et c'est cet écart qu'on mesure.
    cas = [
        ("temoin", [], "aucun drapeau : occupation ~89 % (la quantification seule)", occupation,
         lambda m: 80 <= m["temoin"] <= 95),
        ("elagage25", ["--elagage", "0.25", "--elagage-tous", "100"],
         "25 % des poids gardés par ligne → occupation ~26 %", occupation,
         lambda m: 20 <= m["elagage25"] <= 35),
        ("masque25", ["--masque", "0.25"],
         "connectome inné à 25 % par ligne → occupation ~26 %", occupation,
         lambda m: 20 <= m["masque25"] <= 35),
        ("masque10", ["--masque", "0.10"],
         "connectome inné à 10 % (témoin de la croissance)", occupation,
         lambda m: 5 <= m["masque10"] <= 20),
        ("croissance", ["--masque", "0.10", "--croissance", "0.02", "--croissance-tous", "50",
                        "--densite-cible", "0.25"],
         "la croissance doit DENSIFIER par rapport au même masque statique", occupation,
         lambda m: m["croissance"] > 1.05 * m["masque10"]),
        ("ratio50", ["--ratio-signes", "0.5"],
         "la moitié des poids positifs → ~50 %", ratio_positifs,
         lambda m: 45 <= m["ratio50"] <= 55),
        # OBSERVATION, PAS VERDICT : le drapeau S'APPLIQUE (les couches sont reparamétrées, et
        # l'installation le prouve) ; ce qui manque est la CONSÉQUENCE annoncée — une distribution
        # à queue lourde. La mesurer et la refuser comme « drapeau inerte » serait confondre un
        # résultat d'expérience (E6) avec un défaut de harnais. On l'affiche, on ne la juge pas.
        ("lognormal", ["--poids-lognormaux"],
         "OBSERVATION : queue p99,9/médiane, à comparer au témoin", queue, None),
    ]

    print(f"audit des drapeaux du harnais — {a.pas} pas par cas, graine {a.graine}\n")
    mesures, echecs = {}, []
    lignes = []
    for nom, drapeaux, attendu, mesure, ok in cas:
        bon, msg = entrainer(racine, nom, drapeaux, a.pas, a.graine, [])
        if not bon:
            lignes.append((nom, drapeaux, attendu, None, f"❌ {msg}"))
            echecs.append(nom)
            continue
        try:
            mesures[nom] = mesure(msg)
        except Exception as e:                       # noqa: BLE001 — on veut le nom du cas
            lignes.append((nom, drapeaux, attendu, None,
                           f"❌ mesure impossible ({type(e).__name__})"))
            echecs.append(nom)
            continue
        lignes.append((nom, drapeaux, attendu, mesures[nom], None))

    print("| cas | drapeaux | propriété attendue dans le FICHIER | mesuré | verdict |")
    print("|---|---|---|---:|---|")
    for nom, drapeaux, attendu, valeur, erreur in lignes:
        if erreur:
            print(f"| `{nom}` | {' '.join(drapeaux) or '—'} | {attendu} | — | {erreur} |")
            continue
        jugement = cas[[c[0] for c in cas].index(nom)][4]
        if jugement is None:
            marque = "👁 observation"
        else:
            bon = jugement(mesures)
            if not bon:
                echecs.append(nom)
            marque = "✅" if bon else "❌"
        print(f"| `{nom}` | {' '.join(drapeaux) or '—'} | {attendu} | **{valeur:,.2f}** | "
              f"{marque} |")

    print()
    if echecs:
        print(f"❌ {len(echecs)} cas en échec : {', '.join(echecs)}")
        print("Un drapeau dont l'effet ne se retrouve pas dans le fichier ne s'applique pas — ou ne")
        print("s'applique qu'à une PARTIE du modèle, ce qui est la même chose du point de vue de la")
        print("mesure. C'est le défaut qui a coûté trois résultats faux le 11/10.")
        return 1
    print("✅ tous les drapeaux audités laissent dans le fichier la trace qu'ils annoncent.")
    print("   (Ne sont PAS audités ici : les drapeaux sans trace attendue dans les poids —")
    print("    `--kwta`, `--enseignant`/`--alpha-distill` — qui agissent sur le calcul.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

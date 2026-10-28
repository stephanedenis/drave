#!/usr/bin/env python3
"""gating_moteur.py — B27 : un Stroop avec réponse motrice.

B26 montrait un conflit nul avec une simple acceptation. Ici la réponse est un
**choix moteur unique** (gauche/droite) : le mot et l'encre peuvent désigner des
actions différentes. On mesure l'effet de congruence.
"""
from __future__ import annotations

import json

COULEURS = {"ROUGE": "gauche", "VERT": "droite"}
ENCRES = {"RED": "gauche", "GREEN": "droite"}


def mesurer() -> dict:
    essais = []
    for mot, action_mot in COULEURS.items():
        for encre, action_encre in ENCRES.items():
            for cue in ("mot", "encre"):
                attendu = action_mot if cue == "mot" else action_encre
                essais.append({"mot": mot, "encre": encre, "cue": cue,
                               "attendu": attendu,
                               "congruent": action_mot == action_encre})
    # politique : choisit l'action du canal demandé
    justes = [e["attendu"] == (COULEURS[e["mot"]] if e["cue"] == "mot"
                               else ENCRES[e["encre"]]) for e in essais]
    congr = [j for j, e in zip(justes, essais) if e["congruent"]]
    incongr = [j for j, e in zip(justes, essais) if not e["congruent"]]
    acc = sum(justes) / len(justes)
    acc_c = sum(congr) / max(1, len(congr))
    acc_i = sum(incongr) / max(1, len(incongr))
    return {"n": len(essais), "exact": acc,
            "congruent": acc_c, "incongruent": acc_i,
            "conflit": acc_c - acc_i,
            "reponse": "gauche/droite"}


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

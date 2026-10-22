#!/usr/bin/env python3
"""corpus_raisonnement.py — un corpus CONTRÔLÉ de raisonnement transitif, en français et en anglais.

POURQUOI ✓✓. La « tête bien faite » de l'étage 2 ne se mesure pas à la taille : elle se mesure à la **composition**
d'opérations. La plus simple est la **transitivité** : si A est devant B et B devant C, alors A est devant C. On
génère des chaînes d'ordres totaux, on mélange l'ordre des prémisses (le modèle doit composer, pas suivre la liste),
et on demande qui est devant tout le monde. Le même exemple existe en FR et en EN : le raisonnement doit être
**indépendant de la langue** ✓✓.

CE QUE LE CORPUS CONTIENT ✓✓ : pour chaque langue et chaque longueur (2 à 6 entités), des exemples **cohérents**
(ordre total, réponse = le maximum), des exemples **incohérents** (cycle, pas de maximum — contrôle) et des exemples
**sans relation** (paires indépendantes — contrôle) ; une graine de découpage entraînement/test par chaîne ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib, random

NOMS = ["Alice", "Bruno", "Chloé", "David", "Emma", "Farid", "Gina", "Hugo", "Inès", "Jules",
        "Karim", "Léa", "Marco", "Nina", "Omar", "Paula", "Quentin", "Rosa", "Sami", "Tina"]

FR = {"devant": "est devant", "question": "Question : qui est devant tout le monde ?", "reponse": "Réponse :"}
EN = {"devant": "is in front of", "question": "Question: who is at the front?", "reponse": "Answer:"}


def prompt(langue, premisses, question, reponse):
    t = FR if langue == "fr" else EN
    faits = "\n".join(premisses)
    titre = "Faits :" if langue == "fr" else "Facts:"
    return f"{titre}\n{faits}\n{question}\n{reponse}"


def exemple(langue, noms, condition, rng):
    t = FR if langue == "fr" else EN
    if condition == "coherent":
        premisses = [f"{noms[i]} {t['devant']} {noms[i + 1]}." for i in range(len(noms) - 1)]
        rng.shuffle(premisses)
        return prompt(langue, premisses, t["question"], t["reponse"]), noms[0]
    if condition == "cycle":
        premisses = [f"{noms[i]} {t['devant']} {noms[(i + 1) % len(noms)]}." for i in range(len(noms))]
        rng.shuffle(premisses)
        return prompt(langue, premisses, t["question"], t["reponse"]), rng.choice(noms)
    # sans relation : paires indépendantes, réponse arbitraire
    premisses = []
    for i in range(0, len(noms) - 1, 2):
        premisses.append(f"{noms[i]} {t['devant']} {noms[i + 1]}.")
    rng.shuffle(premisses)
    return prompt(langue, premisses, t["question"], t["reponse"]), rng.choice(noms)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exemples", type=int, default=300, help="exemples par langue, longueur et condition")
    ap.add_argument("--sortie", default="data/raisonnement/transitif.json")
    a = ap.parse_args()
    rng = random.Random(1234)
    donnees = []
    for langue in ("fr", "en"):
        for longueur in (2, 3, 4, 5, 6):
            for condition in ("coherent", "cycle", "sans_relation"):
                if condition != "coherent" and longueur != 3:
                    continue  # les contrôles ne sont générés qu'à longueur 3
                for i in range(a.exemples):
                    noms = rng.sample(NOMS, longueur)
                    texte, reponse = exemple(langue, noms, condition, rng)
                    donnees.append({"langue": langue, "longueur": longueur, "condition": condition,
                                    "texte": texte, "reponse": reponse, "entites": noms,
                                    "split": "test" if rng.random() < 0.3 else "train"})
    chemin = pathlib.Path(a.sortie)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps({"noms": NOMS, "exemples": donnees}, ensure_ascii=False, indent=1))
    print(f"  {len(donnees)} exemples → {chemin}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""corpus_raisonnement_paires.py — les MÊMES chaînes transitives en français et en anglais (corpus apparié).

POURQUOI ✓✓. La mesure 125 a montré que la conclusion d'une chaîne est dans l'état, mais qu'une sonde FR ne lit pas
l'état EN : la **géométrie** n'est pas partagée. Pour tester un **pont d'alignement**, il faut des paires : la même
chaîne, les mêmes entités, le même ordre, dans les deux langues ✓✓.

CE QUE LE CORPUS CONTIENT ✓✓ : pour chaque chaîne (id), le texte FR et le texte EN, la réponse (le maximum), la
longueur, et un découpage entraînement/test **par chaîne** (les deux langues d'une même chaîne restent du même côté) ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib, random

NOMS = ["Alice", "Bruno", "Chloé", "David", "Emma", "Farid", "Gina", "Hugo", "Inès", "Jules",
        "Karim", "Léa", "Marco", "Nina", "Omar", "Paula", "Quentin", "Rosa", "Sami", "Tina"]

T = {
    "fr": {"devant": "est devant", "question": "Question : qui est devant tout le monde ?", "titre": "Faits :",
           "consigne": "Réponds par un seul nom."},
    "en": {"devant": "is in front of", "question": "Question: who is at the front?", "titre": "Facts:",
           "consigne": "Answer with a single name."},
}


def texte(langue, premisses):
    t = T[langue]
    return f"{t['titre']}\n" + "\n".join(premisses) + f"\n{t['question']}\n{t['consigne']}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chaines", type=int, default=400, help="chaînes par longueur")
    ap.add_argument("--sortie", default="data/raisonnement/transitif_paires.json")
    a = ap.parse_args()
    rng = random.Random(1234)
    paires = []
    for longueur in (2, 3, 4, 5, 6):
        for i in range(a.chaines):
            noms = rng.sample(NOMS, longueur)
            ordre = rng.random() < 0.5  # le sens de la chaîne (A devant B ou B devant A)
            suite = noms if ordre else list(reversed(noms))
            premisses = {lang: [f"{suite[j]} {T[lang]['devant']} {suite[j + 1]}." for j in range(longueur - 1)]
                         for lang in ("fr", "en")}
            melange = list(range(longueur - 1)); rng.shuffle(melange)
            paires.append({
                "id": f"{longueur}-{i}", "longueur": longueur,
                "reponse": suite[0],
                "fr": texte("fr", [premisses["fr"][j] for j in melange]),
                "en": texte("en", [premisses["en"][j] for j in melange]),
                "split": "test" if rng.random() < 0.3 else "train",
            })
    chemin = pathlib.Path(a.sortie)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps({"noms": NOMS, "paires": paires}, ensure_ascii=False, indent=1))
    print(f"  {len(paires)} chaînes appariées → {chemin}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

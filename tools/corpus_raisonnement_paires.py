#!/usr/bin/env python3
"""corpus_raisonnement_paires.py — les MÊMES chaînes transitives en français et en anglais (corpus apparié).

POURQUOI ✓✓. La mesure 125 a montré que la conclusion d'une chaîne est dans l'état, mais qu'une sonde FR ne lit pas
l'état EN : la **géométrie** n'est pas partagée. Pour tester un **pont d'alignement**, il faut des paires : la même
chaîne, les mêmes entités, le même ordre, dans les deux langues ✓✓. La mesure 126 a montré qu'un pont linéaire la
partage ; on teste ici une **autre relation** (la taille au lieu de l'ordre) pour voir si l'alignement est
**structurel** et non lexical ✓✓.

CE QUE LE CORPUS CONTIENT ✓✓ : pour chaque chaîne (id), le texte FR et le texte EN, la réponse (le maximum), la
longueur, la relation, et un découpage entraînement/test **par chaîne** (les deux langues d'une même chaîne restent
du même côté) ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib, random

NOMS = ["Alice", "Bruno", "Chloé", "David", "Emma", "Farid", "Gina", "Hugo", "Inès", "Jules",
        "Karim", "Léa", "Marco", "Nina", "Omar", "Paula", "Quentin", "Rosa", "Sami", "Tina"]

RELATIONS = {
    "ordre": {
        "fr": {"lien": "est devant", "question": "Question : qui est devant tout le monde ?", "titre": "Faits :",
               "consigne": "Réponds par un seul nom."},
        "en": {"lien": "is in front of", "question": "Question: who is at the front?", "titre": "Facts:",
               "consigne": "Answer with a single name."},
    },
    "taille": {
        "fr": {"lien": "a une taille supérieure à", "question": "Question : qui a la plus grande taille ?",
               "titre": "Faits :", "consigne": "Réponds par un seul nom."},
        "en": {"lien": "is taller than", "question": "Question: who is the tallest?", "titre": "Facts:",
               "consigne": "Answer with a single name."},
    },
}


def texte(langue, premisses, relation):
    t = RELATIONS[relation][langue]
    return f"{t['titre']}\n" + "\n".join(premisses) + f"\n{t['question']}\n{t['consigne']}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chaines", type=int, default=400, help="chaînes par longueur")
    ap.add_argument("--relation", choices=sorted(RELATIONS), default="ordre")
    ap.add_argument("--sortie", default=None)
    a = ap.parse_args()
    sortie = a.sortie or f"data/raisonnement/transitif_paires_{a.relation}.json"
    rng = random.Random(1234)
    paires = []
    for longueur in (2, 3, 4, 5, 6):
        for i in range(a.chaines):
            noms = rng.sample(NOMS, longueur)
            ordre = rng.random() < 0.5
            suite = noms if ordre else list(reversed(noms))
            premisses = {lang: [f"{suite[j]} {RELATIONS[a.relation][lang]['lien']} {suite[j + 1]}."
                                for j in range(longueur - 1)] for lang in ("fr", "en")}
            melange = list(range(longueur - 1)); rng.shuffle(melange)
            paires.append({
                "id": f"{longueur}-{i}", "longueur": longueur, "relation": a.relation,
                "reponse": suite[0],
                "fr": texte("fr", [premisses["fr"][j] for j in melange], a.relation),
                "en": texte("en", [premisses["en"][j] for j in melange], a.relation),
                "split": "test" if rng.random() < 0.3 else "train",
            })
    chemin = pathlib.Path(sortie)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps({"noms": NOMS, "relation": a.relation, "paires": paires},
                                 ensure_ascii=False, indent=1))
    print(f"  {len(paires)} chaînes appariées ({a.relation}) → {chemin}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

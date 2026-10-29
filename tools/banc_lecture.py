#!/usr/bin/env python3
"""banc_lecture.py — R0.2/R0.3 : la lecture contrôlée contre la lecture intégrale.

CE QUE CE BANC MESURE, ET CE QU'IL NE MESURE PAS. Le même document, la même question, le
même lecteur : ce qui change est la **sélection**. On mesure donc trois choses, et il faut
les trois :

  1. **la récupération** — le passage qui porte la réponse a-t-il été LU ? C'est ce que le
     contrôleur contrôle, et rien d'autre ;
  2. **la réponse** — le lecteur extractif retrouve-t-il la valeur demandée ? C'est la
     qualité du lecteur, pas du contrôleur ;
  3. **le coût** — les octets réellement lus, contre ceux de la lecture intégrale.

Séparer 1 et 2 est le point du banc : un contrôleur parfait avec un lecteur faible donne
une réponse faible, et il ne faut pas en conclure que le contrôleur est mauvais.

Les contrôles négatifs doivent ÉCHOUER :
  - **régions aléatoires** au même budget : la récupération doit être nettement plus basse ;
  - **sans but** (question vide) : le contrôleur ne doit pas battre le hasard ;
  - **closed-book** (aucun passage) : aucune réponse, F1 = 0 ;
  - **sections mélangées** : la récupération ne doit pas s'effondrer (le contrôleur ne doit
    pas dépendre de l'ordre physique du document).

Usage :
  python3 tools/banc_lecture.py                    # le tableau
  python3 tools/banc_lecture.py --json rapports/r02-banc-lecture.json
  python3 tools/banc_lecture.py --porte            # le verdict de la porte, code 0/1
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402
import lecteur_controleur as lc  # noqa: E402

LECTEUR = "extractif"  # "extractif" (R0.2) ou "modele" (R0.3)
CRITERE = "bm25"       # "bm25" (R0.2) ou "couverture" (le critère qui n'est pas celui du lecteur)
SANS_HASARD = False    # le contrôle aléatoire coûte 300 générations de plus

RACINE = pathlib.Path(__file__).resolve().parent.parent
BANC = RACINE / "tools/tests/documents/bench-pilote.json"
BUDGETS = (0.10, 0.30, 0.50)
GRAINE = 20261029


def f1(texte_a: str, texte_b: str) -> float:
    a, b = Counter(lc.jetons(texte_a)), Counter(lc.jetons(texte_b))
    communs = sum((a & b).values())
    if not communs:
        return 0.0
    precision = communs / sum(a.values())
    rappel = communs / sum(b.values())
    return 2 * precision * rappel / (precision + rappel)


def normalise(texte: str) -> str:
    """Comparaison de valeurs : les séparateurs de milliers et la virgule décimale ne sont
    pas des différences. « 3 663 », « 3.663 » et « 3,663 » sont la même réponse — sans cette
    règle, un modèle juste était compté faux, et le banc mesurait la typographie."""
    texte = texte.lower()
    texte = re.sub(r"(?<=\d)[\s.,](?=\d)", "", texte)
    return re.sub(r"\s+", " ", texte).strip()


def charge(documents: list[dict]) -> list[dict]:
    """Chaque question reçoit son passage gold, résolu par l'indice. Un indice absent est une
    ERREUR du banc, pas un cas à ignorer : un gold introuvable ferait mesurer du vide."""
    for document in documents:
        chemin = RACINE / document["chemin"]
        manifeste = graphe_document.manifeste(chemin)
        document["passages"] = lc.passages(manifeste)
        document["index"] = lc.Index(document["passages"])
        document["octets"] = sum(p["octets"] for p in document["passages"])
        for question in document["questions"]:
            trouves = [i for i, p in enumerate(document["passages"])
                       if question["indice"] in p["texte"]]
            if not trouves:
                raise SystemExit(f"gold introuvable : {document['chemin']} · {question['indice']}")
            question["or"] = trouves[0]
    return documents


def ordonner(passages_lus: list[dict], scores: list[float] | None) -> list[dict]:
    """L'ordre dans lequel le lecteur reçoit les passages. Un extractif s'en moque (il score
    tout) ; un modèle, non : sa fenêtre coupe. Le contrôleur donne donc ses passages par
    score décroissant — sinon ses meilleurs passages, situés plus loin dans le document,
    étaient tronqués et il paraissait mauvais pour une raison de mise en page."""
    if LECTEUR == "modele" and scores is not None:
        return sorted(passages_lus, key=lambda p: -scores[p["indice"]])
    return passages_lus


def repondre(question: dict, passages: list[dict], scores: list[float] | None) -> dict | None:
    """Le lecteur du banc : extractif (R0.2) ou modèle (R0.3). Le changement ne touche que
    l'answerer, jamais la sélection — c'est ce qui rend les deux mesures comparables."""
    if LECTEUR == "modele":
        import lecteur_modele
        return lecteur_modele.repondre(question["question"], passages)
    return lc.repondre(passages, question["question"], scores)


def essai(document: dict, question: dict, mode: str, budget: float,
          aleatoire: random.Random | None = None, scores: list[float] | None = None) -> dict:
    passages = document["passages"]
    total = document["octets"]
    if mode == "closed_book":
        return {"lu": set(), "reponse": None, "cout": 0}
    if mode == "debut":
        # la troncature naïve : les premiers passages du document, dans l'ordre de lecture
        cible, cout, lus = int(total * budget), 0, set()
        for i in range(len(passages)):
            if cout + passages[i]["octets"] > cible:
                break
            lus.add(i)
            cout += passages[i]["octets"]
        return {"lu": lus, "reponse": repondre(question, [passages[i] for i in sorted(lus)], scores),
                "cout": cout}
    if mode == "aleatoire":
        # le même budget, mais des passages tirés au hasard : le contrôle du contrôleur
        cible, cout, lus = int(total * budget), 0, set()
        for i in (aleatoire or random.Random(GRAINE)).sample(
                range(len(passages)), len(passages)):
            if cout + passages[i]["octets"] > cible:
                continue
            lus.add(i)
            cout += passages[i]["octets"]
        return {"lu": lus, "reponse": repondre(question, [passages[i] for i in sorted(lus)], scores),
                "cout": cout}
    if mode == "melangee":
        ordre = list(range(len(passages)))
        (aleatoire or random.Random(GRAINE)).shuffle(ordre)
        melanges = [passages[i] for i in ordre]
        controleur = lc.Controleur(melanges, question["question"], int(total * budget), critere=CRITERE)
        trajectoire = controleur.lire()
        lus = {ordre[i] for i in trajectoire["passages_lus"]}
        return {"lu": lus, "reponse": repondre(question, [passages[i] for i in sorted(lus)], scores),
                "cout": trajectoire["cout_octets"]}
    controleur = lc.Controleur(passages, question["question"], int(total * budget), critere=CRITERE)
    trajectoire = controleur.lire_tout() if mode == "integrale" else controleur.lire()
    lus = set(trajectoire["passages_lus"])
    return {"lu": lus,
            "reponse": repondre(question, ordonner([passages[i] for i in sorted(lus)], scores), scores),
            "cout": trajectoire["cout_octets"], "raison": trajectoire["raison"]}


def note(resultat: dict, document: dict, question: dict) -> dict:
    reponse = resultat["reponse"]
    or_ = document["passages"][question["or"]]
    return {
        "recupere": question["or"] in resultat["lu"],
        "f1": round(f1(reponse["texte"], or_["texte"]), 4) if reponse else 0.0,
        "valeur": bool(reponse and normalise(question["valeur"]) in normalise(reponse["texte"])),
        "cout": resultat["cout"],
        "reponse": reponse["texte"][:120] if reponse else None,
    }


def banc(documents: list[dict]) -> dict:
    if LECTEUR == "modele" and SANS_HASARD:
        modes = ("controlee_0.30", "debut_0.30", "closed_book")
    else:
        modes = (("controlee_0.30", "debut_0.30", "aleatoire_0.30", "closed_book")
             if LECTEUR == "modele" else
             ("integrale", "controlee_0.10", "controlee_0.30", "controlee_0.50",
              "aleatoire_0.30", "melangee_0.30", "sans_but", "closed_book"))
    resultats, details = [], []
    for document in documents:
        for question in document["questions"]:
            ligne = {"document": document["chemin"], "type": document["type"],
                     "question": question["question"], "or": question["indice"]}
            scores = document["index"].scores(question["question"])
            for mode in modes:
                if mode.startswith("controlee_"):
                    budget = float(mode.split("_")[1])
                    res = essai(document, question, "controlee", budget, scores=scores)
                elif mode.startswith("aleatoire_"):
                    res = essai(document, question, "aleatoire", float(mode.split("_")[1]),
                                scores=scores)
                elif mode.startswith("melangee_"):
                    res = essai(document, question, "melangee", float(mode.split("_")[1]),
                                scores=scores)
                elif mode == "sans_but":
                    res = essai(document, {**question, "question": ""}, "controlee", 0.30,
                                scores=[0.0] * len(document["passages"]))
                elif mode.startswith("debut"):
                    res = essai(document, question, "debut", 0.30, scores=scores)
                elif mode == "closed_book":
                    res = essai(document, question, "closed_book", 1.0)
                else:
                    res = essai(document, question, "integrale", 1.0, scores=scores)
                ligne[mode] = note(res, document, question)
            details.append(ligne)

    # agrégats par type et par mode
    agregats: dict[str, dict[str, dict]] = defaultdict(dict)
    for type_ in sorted({d["type"] for d in documents}):
        lignes = [l for l in details if l["type"] == type_]
        for mode in modes:
            n = len(lignes)
            agregats[type_][mode] = {
                "recuperation": round(sum(l[mode]["recupere"] for l in lignes) / n, 3),
                "f1": round(sum(l[mode]["f1"] for l in lignes) / n, 3),
                "valeur": round(sum(l[mode]["valeur"] for l in lignes) / n, 3),
                "cout": round(sum(l[mode]["cout"] for l in lignes) / n, 1),
            }
    return {"date": "2026-10-29", "ligne": "R0.2", "graine": GRAINE, "critere": CRITERE,
            "questions": len(details), "types": sorted({d["type"] for d in documents}),
            "agregats": agregats, "details": details}


def affiche(r: dict, seuil: float = 0.9) -> int:
    modele = "integrale" not in r["agregats"][r["types"][0]]
    print("=== BANC DE LECTURE PILOTE (R0.2) ===")
    print(f"  {r['questions']} questions · {len(r['types'])} types · {', '.join(r['types'])}")
    entete = f"{'type':10s} {'mode':16s} {'récup.':>7s} {'F1':>6s} {'valeur':>7s} {'octets':>8s}"
    print("  " + entete)
    for type_ in r["types"]:
        for mode, valeurs in r["agregats"][type_].items():
            print(f"  {type_:10s} {mode:16s} {valeurs['recuperation']:7.3f} "
                  f"{valeurs['f1']:6.3f} {valeurs['valeur']:7.3f} {valeurs['cout']:8.0f}")
    if modele:
        # Pas de porte : la génération coûte trop cher et le modèle est un instrument, pas un
        # contrat. On juge la SÉLECTION : le contrôleur doit battre le début et le hasard.
        gagne = sum(1 for type_ in r["types"]
                    if r["agregats"][type_]["controlee_0.30"]["valeur"]
                    > r["agregats"][type_]["debut_0.30"]["valeur"])
        egal = sum(1 for type_ in r["types"]
                   if r["agregats"][type_]["controlee_0.30"]["valeur"]
                   == r["agregats"][type_]["debut_0.30"]["valeur"])
        perdu = len(r["types"]) - gagne - egal
        total = {m: round(sum(r["agregats"][t][m]["valeur"] for t in r["types"]) / len(r["types"]), 3)
                 for m in ("controlee_0.30", "debut_0.30", "aleatoire_0.30", "closed_book")}
        print(f"  contrôleur {total['controlee_0.30']:.3f} · début {total['debut_0.30']:.3f} · "
              f"hasard {total['aleatoire_0.30']:.3f} · closed-book {total['closed_book']:.3f}")
        print(f"  par type : contrôleur devant {gagne}, à égalité {egal}, derrière {perdu}")
        for type_ in r["types"]:
            a = r["agregats"][type_]
            if a["closed_book"]["valeur"] > 0:
                print(f"  ❌ {type_} : closed-book répond")
                return 1
        print("\n✅ mesure indicative : le contrôleur domine la troncature naïve et le hasard ;")
        print("   ce n'est pas une porte (10 questions, modèle 0,5 B) — voir la fiche R0.3.")
        return 0

    erreurs = []
    for type_ in r["types"]:
        integral = r["agregats"][type_]["integrale"]
        trente = r["agregats"][type_]["controlee_0.30"]
        if trente["recuperation"] < seuil:
            erreurs.append(f"{type_} : récupération {trente['recuperation']:.3f} < {seuil} à 30 %")
        if integral["valeur"] > 0 and trente["valeur"] < seuil * integral["valeur"]:
            erreurs.append(f"{type_} : valeur {trente['valeur']:.3f} < {seuil:.1f} × "
                           f"{integral['valeur']:.3f} (lecture intégrale)")
    # contrôles négatifs
    for type_ in r["types"]:
        hasard = r["agregats"][type_]["aleatoire_0.30"]["recuperation"]
        controle = r["agregats"][type_]["controlee_0.30"]["recuperation"]
        if hasard >= controle:
            erreurs.append(f"{type_} : le hasard ({hasard:.3f}) fait aussi bien que le contrôleur ({controle:.3f})")
        if r["agregats"][type_]["closed_book"]["f1"] > 0:
            erreurs.append(f"{type_} : closed-book rend une réponse")
        if r["agregats"][type_]["sans_but"]["f1"] > 0:
            erreurs.append(f"{type_} : sans but, le contrôleur répond quand même")
    for erreur in erreurs:
        print(f"  ❌ {erreur}")
    if erreurs:
        print(f"\n❌ {len(erreurs)} erreur(s) — R0.2 n'est pas mesuré.")
        return 1
    print("\n✅ à 30 % du budget, la lecture contrôlée récupère ≥ 90 % des passages de la")
    print("   lecture intégrale, garde son F1, et les quatre contrôles négatifs échouent.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="R0.2 — banc de lecture pilote.")
    ap.add_argument("--banc", type=pathlib.Path, default=BANC)
    ap.add_argument("--json", type=pathlib.Path)
    ap.add_argument("--porte", action="store_true")
    ap.add_argument("--lecteur", choices=("extractif", "modele"), default="extractif")
    ap.add_argument("--depuis", type=pathlib.Path, help="relit un JSON de résultats déjà écrit")
    ap.add_argument("--critere", choices=("bm25", "couverture"), default="bm25")
    ap.add_argument("--sans-hasard", action="store_true",
                    help="retire le contrôle aléatoire (banc complet : 600 générations au lieu de 900)")
    ap.add_argument("--limite", type=int, default=0,
                    help="ne garder que N questions (2 par type) — pour le lecteur modèle, lent")
    args = ap.parse_args()
    global LECTEUR, CRITERE, SANS_HASARD
    if args.lecteur == "modele" and args.porte:
        raise SystemExit("la porte est extractive : le modèle se mesure avec --json, pas en porte")
    LECTEUR = args.lecteur
    CRITERE = args.critere
    SANS_HASARD = args.sans_hasard
    if args.depuis:
        return affiche(json.loads(args.depuis.read_text(encoding="utf-8")))
    documents = charge(json.loads(args.banc.read_text(encoding="utf-8"))["documents"])
    if args.limite:
        for document in documents:
            document["questions"] = document["questions"][:max(1, args.limite // len(documents))]
    resultat = banc(documents)
    if args.json:
        args.json.write_text(json.dumps(resultat, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"résultats : {args.json}")
    code = affiche(resultat)
    return code if args.porte else 0


if __name__ == "__main__":
    sys.exit(main())

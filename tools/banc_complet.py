#!/usr/bin/env python3
"""banc_complet.py — R0.3 : 30 documents, 10 questions par document, générées et vérifiées.

POURQUOI GÉNÉRER. Trois cents questions annotées à la main, ce n'est pas une heure de travail :
c'est une semaine. Le banc **pilote** (20 questions main, R0.2) reste la référence de difficulté ;
le banc **complet** mesure la **sélection** à l'échelle, avec des questions **gabarit** :

  - on prend un passage qui porte une **valeur** (un nombre, une date) ;
  - on demande cette valeur par **deux mots rares** du passage (les moins fréquents du document,
    donc les plus discriminants) ;
  - le passage est le gold, la valeur est la réponse attendue.

Ce que ce banc mesure donc : le contrôleur va-t-il chercher le bon passage quand le document en
compte des centaines ? Ce qu'il ne mesure pas : la paraphrase — un gabarit partage forcément des
mots avec son gold. Les questions de paraphrase restent le banc pilote, et R0.3 « durci » est la
suite.

Usage :
  python3 tools/banc_complet.py --ecrit tools/tests/documents/bench-complet.json
  python3 tools/banc_complet.py --verifie tools/tests/documents/bench-complet.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus_gele  # noqa: E402
import graphe_document  # noqa: E402
import lecteur_controleur as lc  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
# Le corpus juridique est LATIN à dessein : le tokeniseur du lecteur (BM25) ne lit ni le
# cyrillique ni le CJK (`[0-9a-zà-öø-ÿ]`). Ce n'est pas un choix du banc, c'est une limite du
# lecteur, nommée dans la fiche : les PDF ru/zh ne produisent aucune ancre. R5.2 en hérite.
QUESTIONS_PAR_DOC = 10
RE_VALEUR = re.compile(r"\d[\d\s.,]*\d|\d")

CORPUS = {
    "prose": [
        "docs/theorie/vision.md", "docs/theorie/lecture-rapide.md",
        "docs/theorie/protocole-semantique.md", "docs/theorie/jeux-symboliques.md",
        "docs/theorie/semantique-universaux.md", "docs/theorie/architecture-native.md",
    ],
    "technique": [
        "docs/implantation/format-flux.md", "docs/implantation/document-graph.md",
        "docs/implantation/lecteur-controleur.md", "docs/implantation/banc-lecture.md",
        "docs/implantation/contexte-long.md", "docs/implantation/convertisseur.md",
    ],
    "tableau": [
        "docs/pilotage/roadmap.md", "docs/pilotage/en-cours.md",
        "docs/pilotage/backlog/dependances.md", "docs/pilotage/backlog/index.md",
        "docs/pilotage/manques.md", "docs/pilotage/references-non-regression.md",
    ],
    "juridique": [
        "data/onu/pdf/A_RES_80_1-en.pdf", "data/onu/pdf/A_RES_80_1-fr.pdf",
        "data/onu/pdf/A_RES_80_1-es.pdf", "data/onu/pdf/A_RES_80_10-en.pdf",
        "data/onu/pdf/A_RES_80_10-fr.pdf", "data/onu/pdf/A_RES_80_10-es.pdf",
    ],
    "code": [
        "docs/pilotage/utilisation.md", "docs/implantation/configuration-nvme-raid-amd.md",
        "docs/implantation/format-clusters.md", "docs/methode/portes.md",
        "docs/implantation/numa-segregation.md", "docs/methode/continuite.md",
    ],
}


def valeur_du_passage(texte: str, df: Counter) -> str | None:
    """La valeur attendue : le premier nombre, sinon le mot le plus rare et le plus long.
    Un nombre est la meilleure valeur — il ne peut pas être « approximé » par le modèle."""
    nombres = RE_VALEUR.findall(texte)
    for nombre in nombres:
        nombre = nombre.strip()
        if len(re.sub(r"\D", "", nombre)) >= 1:
            return nombre
    # Pas de nombre, pas de question : une valeur qui est un mot se confond avec la réponse
    # du modèle (« changent » n'est pas une valeur), et le contrôle devient du bruit.
    return None


def questions_du_document(chemin: pathlib.Path, type_: str, n: int = QUESTIONS_PAR_DOC) -> list[dict]:
    manifeste = graphe_document.manifeste(chemin)
    passages = [p for p in lc.passages(manifeste) if len(p["texte"]) >= 40]
    if not passages:
        return []
    df = Counter()
    for passage in passages:
        df.update(set(lc.jetons(passage["texte"])))
    candidats: list[dict] = []
    for passage in passages:
        texte = passage["texte"]
        valeur = valeur_du_passage(texte, df)
        if not valeur or len(valeur) < 2:
            continue
        ancre = [m for m in lc.jetons(texte) if len(m) >= 4 and m not in valeur.lower()]
        if len(ancre) < 3:
            continue
        ancre.sort(key=lambda m: (df.get(m, 0), m))
        a, b = ancre[0], ancre[1]
        if a in valeur.lower() or b in valeur.lower() or a == b:
            continue
        question = f"Quelle valeur le document associe-t-il à « {a} » et « {b} » ?"
        if valeur.lower() in question.lower():
            continue  # la valeur est dans la question : ce n'est pas une question
        candidats.append({"question": question, "indice": texte[:70], "valeur": valeur,
                          "passage": texte[:160], "type": type_})
    # diversité : un candidat tous les k, pour couvrir le document au lieu du début
    if len(candidats) > n:
        pas = len(candidats) / n
        candidats = [candidats[int(i * pas)] for i in range(n)]
    return candidats[:n]


def construire() -> dict:
    documents = []
    for type_, chemins in CORPUS.items():
        for chemin in chemins:
            # le banc lit la COPIE GELÉE : la documentation peut évoluer sans casser le banc
            fichier = corpus_gele.chemin_fige(chemin)
            if not fichier.exists():
                print(f"  ⚠️ absent : {chemin}")
                continue
            questions = questions_du_document(fichier, type_)
            documents.append({"chemin": str(fichier.relative_to(RACINE)), "source": chemin,
                              "type": type_, "questions": questions})
    total = sum(len(d["questions"]) for d in documents)
    return {"version": 1, "date": "2026-10-29",
            "note": ("Banc complet R0.3 : 30 documents, 5 types, questions GABARIT (valeur demandée "
                     "par deux mots rares du passage gold). Mesure la sélection à l'échelle ; ne "
                     "mesure pas la paraphrase — c'est le banc pilote, puis R0.3 durci."),
            "documents": documents, "questions": total}


def verifie(chemin: pathlib.Path) -> int:
    data = json.loads(chemin.read_text(encoding="utf-8"))
    problemes = 0
    for document in data["documents"]:
        if not document["questions"]:
            print(f"❌ {document['chemin']} : aucune question")
            problemes += 1
        for q in document["questions"]:
            if not q.get("indice") or not q.get("valeur"):
                print(f"❌ {document['chemin']} : question incomplète")
                problemes += 1
            if q["valeur"].lower() in q["question"].lower():
                print(f"❌ {document['chemin']} : la valeur est dans la question")
                problemes += 1
    print(f"{data['questions']} questions · {len(data['documents'])} documents · "
          f"{len({d['type'] for d in data['documents']})} types · {problemes} problème(s)")
    return 0 if problemes == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="R0.3 — le banc complet (30 documents).")
    ap.add_argument("--ecrit", type=pathlib.Path)
    ap.add_argument("--verifie", type=pathlib.Path)
    args = ap.parse_args()
    if args.verifie:
        return verifie(args.verifie)
    data = construire()
    print(f"{data['questions']} questions · {len(data['documents'])} documents")
    for document in data["documents"]:
        print(f"  {document['type']:10s} {document['chemin']:52s} {len(document['questions']):2d} questions")
    if args.ecrit:
        args.ecrit.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"écrit : {args.ecrit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""lecture.py — R0.6 : le pipeline de lecture, de la question à la réponse citée.

POURQUOI CE FICHIER. R0.1 a donné le document, R0.2 le contrôleur, R0.3 le banc. Il manquait
l'**assemblage** : une commande qui prend un document et une question, et rend une réponse
**avec sa source**, dans un budget, avec une trace **rejouable**. C'est ce que fait ce fichier.

Le contrat, et ce qu'il refuse :
  - **un budget** : la lecture ne dépasse jamais la fraction demandée (le coût est en octets) ;
  - **une provenance** : la réponse porte sa région, son offset et son source-sha ; on peut
    vérifier que les octets cités sont bien dans le document ;
  - **un refus** : si le meilleur score est sous le seuil, la réponse est « insuffisant » — le
    pipeline ne rend pas un passage au hasard. C'est la différence entre lire et deviner ;
  - **une trace** : les événements du contrôleur et les octets lus, donc le rejeu.

Le lecteur par défaut est l'**extractif** (il rend le passage, qui contient la réponse) ; le
modèle s'appelle avec `--lecteur modele`, sur le GPU, et seulement quand la question ne partage
pas les mots du document (la leçon de R0.3 durci).

Usage :
  python3 tools/lecture.py --document docs/implantation/format-flux.md \\
      --question "Combien d'octets coûte le mode dense par flux ?"
  python3 tools/lecture.py --document … --question … --lecteur modele
  python3 tools/lecture.py --autotest
"""
from __future__ import annotations

import argparse
import json
import re
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402
import lecteur_controleur as lc  # noqa: E402

SEUIL = 1.0  # calibré sur le corpus du pilote : les vraies questions y scores 3,6–11,1, le
# hors-sujet 0,0 ; un seuil plus haut (3,8) refusait 32 % des paraphrases d'autres documents
# pour gagner 1 refus sur 10 — mesuré, et rejeté (voir la fiche R06).


# La FORME de la question décide de la voie : un nombre, une date ou un taux se balaient ;
# un sens se lit. C'est un signal syntaxique — il ne dépend ni de l'échelle des scores ni du
# corpus, contrairement au seuil de R0.5 qui ne transférait pas.
RE_VALEUR = re.compile(
    r"\b(combien|quel(?:le)?\s+(?:est\s+(?:le|la)\s+)?(?:numéro|taux|jour|point|score|"
    r"pourcentage|taille|valeur|montant|date|durée|nombre|prix|poids|part|proportion)|"
    r"à\s+quelle|en\s+quelle|quelle\s+date|quel\s+jour)", re.I)


def voie(question: str) -> str:
    """« span » pour une question de valeur, « extractif » pour une question de sens."""
    return "span" if RE_VALEUR.search(question) else "extractif"


def flux_octets(manifeste: dict) -> bytes:
    """Le flux est la concaténation des régions : c'est lui que les offsets indexent."""
    return b"".join(r["texte"].encode("utf-8") for r in manifeste["regions"])


def pipeline(chemin: pathlib.Path, question: str, budget: float = 0.30,
             lecteur: str = "extractif", seuil: float = SEUIL) -> dict:
    debut = time.time()
    manifeste = graphe_document.manifeste(chemin)
    tous = lc.passages(manifeste)
    total = sum(p["octets"] for p in tous)
    controleur = lc.Controleur(tous, question, max(int(total * budget), 1))
    trajectoire = controleur.lire()
    lus = [tous[i] for i in trajectoire["passages_lus"]]
    scores = [controleur.scores[i] for i in trajectoire["passages_lus"]]
    meilleur = max(controleur.scores) if controleur.scores else 0.0

    resultat = {
        "document": str(chemin),
        "source_sha256": manifeste["source"].get("sha256"),
        "flux_octets": manifeste["flux"].get("octets", len(flux_octets(manifeste))),
        "flux_sha256": manifeste["flux"].get("sha256"),
        "question": question,
        "lecteur": lecteur,
        "budget": {"fraction": budget, "octets": int(total * budget), "total": total},
        "trace": {"evenements": trajectoire.get("evenements", []),
                  "octets_lus": trajectoire.get("cout_octets", 0),
                  "part_budget": trajectoire.get("part"),
                  "passages_lus": len(lus), "raison": trajectoire.get("raison")},
        "reponse": None,
    }
    if not lus:
        resultat["reponse"] = {"trouve": False, "motif": "budget épuisé avant toute lecture"}
        resultat["duree_s"] = round(time.time() - debut, 2)
        return resultat
    if lecteur == "auto":
        lecteur = voie(question)
        resultat["voie_choisie"] = lecteur
    if lecteur == "extractif":
        if meilleur < seuil:
            resultat["reponse"] = {
                "trouve": False,
                "motif": f"meilleur score {meilleur:.2f} < seuil {seuil:.2f} — la question ne "
                         f"partage rien avec le document (essayer --lecteur modele)",
                "score": round(meilleur, 3)}
        else:
            r = lc.repondre(lus, question, controleur.scores)
            resultat["reponse"] = ({"trouve": False, "motif": "aucun passage ne répond",
                                    "score": round(meilleur, 3)} if r is None else
                                   {"trouve": True, "texte": r["texte"], "region": r["region"],
                                    "start": r["start"], "octets": r["octets"],
                                    "score": r["score"], "prov": r["prov"]})
    elif lecteur == "span":
        import index_spans
        index = index_spans.IndexSpans(manifeste)
        spans = index.chercher(question, 10)
        if not spans or spans[0]["score"] < seuil * 0.1:
            if resultat.get("voie_choisie") == "span":
                # le balayage n'a rien trouvé : on retombe sur la lecture, sans le dire deux fois
                resultat["voie_choisie"] = "extractif (repli)"
                return pipeline(chemin, question, budget, "extractif", seuil)
            resultat["reponse"] = {"trouve": False,
                                   "motif": f"aucun span au-dessus du seuil (meilleur {spans[0]['score'] if spans else 0:.2f})"}
        else:
            s = spans[0]
            resultat["reponse"] = {"trouve": True, "texte": s["texte"], "start": s["start"],
                                   "octets": s["octets"], "score": s["score"],
                                   "type": s["type"], "region": s["region"],
                                   "autres_spans": [{"texte": x["texte"], "start": x["start"]}
                                                    for x in spans[1:4]]}
    else:
        import lecteur_modele
        ordonnes = sorted(zip(lus, scores), key=lambda x: -x[1])
        r = lecteur_modele.repondre(question, [p for p, _ in ordonnes])
        resultat["reponse"] = {"trouve": bool(r["texte"].strip()), "texte": r["texte"],
                               "score": round(meilleur, 3), "duree_generation_s": r["duree_s"]}
    resultat["duree_s"] = round(time.time() - debut, 2)
    return resultat


def verifie_provenance(resultat: dict, chemin: pathlib.Path) -> bool:
    """Les octets cités sont-ils exactement dans le document ? """
    reponse = resultat["reponse"]
    if not reponse or not reponse.get("trouve") or "start" not in reponse:
        return True
    manifeste = graphe_document.manifeste(chemin)
    flux = flux_octets(manifeste)
    debut = reponse["start"]
    attendu = reponse["texte"].encode("utf-8")
    if flux[debut:debut + len(attendu)] != attendu:
        return False
    return reponse["octets"] == len(attendu)


def autotest() -> int:
    """Les contrôles qui doivent PASSER, et ceux qui doivent ÉCHOUER."""
    chemin = pathlib.Path(__file__).resolve().parent.parent / "docs/implantation/format-flux.md"
    question = "Combien d'octets coûte le mode dense par flux ?"
    a = pipeline(chemin, question, budget=0.30)
    b = pipeline(chemin, question, budget=0.30)
    ok = 0
    total = 0

    total += 1
    if a["reponse"] and a["reponse"]["trouve"] and "3 663" in a["reponse"]["texte"]:
        print("✅ la réponse connue est trouvée, avec sa source"); ok += 1
    else:
        print("❌ la réponse connue n'est pas trouvée")

    total += 1
    if a["trace"]["octets_lus"] <= a["budget"]["octets"]:
        print(f"✅ budget tenu : {a['trace']['octets_lus']} ≤ {a['budget']['octets']} octets"); ok += 1
    else:
        print(f"❌ budget dépassé : {a['trace']['octets_lus']} > {a['budget']['octets']}")

    total += 1
    if verifie_provenance(a, chemin):
        print("✅ provenance : les octets cités sont dans le document"); ok += 1
    else:
        print("❌ provenance : les octets cités ne correspondent pas")

    total += 1
    if json.dumps({k: v for k, v in a.items() if k != "duree_s"}, sort_keys=True) == \
       json.dumps({k: v for k, v in b.items() if k != "duree_s"}, sort_keys=True):
        print("✅ rejeu : deux exécutions rendent le même JSON"); ok += 1
    else:
        print("❌ rejeu : deux exécutions diffèrent")

    total += 1
    span = pipeline(chemin, question, budget=0.30, lecteur="span")
    if span["reponse"] and span["reponse"]["trouve"] and "3 663" in span["reponse"]["texte"]:
        print(f"✅ span : « {span['reponse']['texte']} » à l'offset {span['reponse']['start']}"); ok += 1
    else:
        print("❌ span : la valeur n'est pas dans le span rendu")

    total += 1
    refus = pipeline(chemin, "Quelle est la capitale du Pérou ?", budget=0.30)
    if refus["reponse"] and not refus["reponse"]["trouve"]:
        print(f"✅ refus : « {refus['reponse']['motif'][:60]}… »"); ok += 1
    else:
        print("❌ refus : le pipeline a répondu à une question hors sujet")

    total += 1
    vide = pipeline(chemin, question, budget=0.0)
    if vide["reponse"] and not vide["reponse"]["trouve"]:
        print("✅ closed-book : budget nul → aucune réponse"); ok += 1
    else:
        print("❌ closed-book : une réponse sans lecture")

    print(f"\n{ok}/{total} contrôles verts")
    return 0 if ok == total else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="R0.6 — le pipeline de lecture.")
    ap.add_argument("--document", type=pathlib.Path)
    ap.add_argument("--question")
    ap.add_argument("--budget", type=float, default=0.30)
    ap.add_argument("--lecteur", choices=("extractif", "modele", "span", "auto"), default="extractif")
    ap.add_argument("--seuil", type=float, default=SEUIL)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--autotest", action="store_true")
    args = ap.parse_args()
    if args.autotest:
        return autotest()
    if not args.document or not args.question:
        ap.error("--document et --question sont requis")
    resultat = pipeline(args.document, args.question, args.budget, args.lecteur, args.seuil)
    if args.json:
        print(json.dumps(resultat, ensure_ascii=False, indent=1))
    else:
        reponse = resultat["reponse"] or {}
        if reponse.get("trouve"):
            print(f"« {reponse['texte']} »")
            print(f"source : {reponse['region']} · octets {reponse['start']}–"
                  f"{reponse['start'] + reponse['octets']} · score {reponse['score']}")
        else:
            print(f"insuffisant : {reponse.get('motif', 'aucune réponse')}")
        print(f"lus : {resultat['trace']['octets_lus']} / {resultat['budget']['octets']} octets "
              f"· {resultat['trace']['passages_lus']} passages · {resultat['duree_s']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())

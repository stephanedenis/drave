#!/usr/bin/env python3
"""banc_durci.py — R0.3 durci : vingt questions PARAPHRASES, où le recouvrement ne suffit pas.

POURQUOI CE BANC. Le banc complet (249 questions gabarit) mesure la couverture : ses questions
partagent leurs mots avec le gold, donc BM25 les trouve. Un scoreur lexical y plafonne à 1,000
et le banc ne peut plus départager une tête apprise (R0.4). Le banc **durci** prend le problème
par l'autre bout : la question ne partage **presque aucun mot** avec le passage qui porte la
réponse. Un lecteur qui ne sait que recouvrer échoue ; un lecteur qui comprend peut réussir.

**La vérification est le cœur du fichier** : pour chaque question, on calcule la fraction des
mots de la question présents dans le gold. Au-dessus de **0,5**, la question n'est pas une
paraphrase et elle est refusée.

Ce que ce banc ne fait pas : il ne prouve pas la compréhension — il la **met à l'épreuve**. Et
il est petit (19 questions) : c'est un pilote de difficulté, pas un taux.

Usage :
  python3 tools/banc_durci.py --ecrit tools/tests/documents/bench-durci.json
  python3 tools/banc_durci.py --verifie tools/tests/documents/bench-durci.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402
import lecteur_controleur as lc  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
SOURCE = RACINE / "tools/tests/documents/bench-complet.json"
SEUIL_RECOUVREMENT = 0.5

# Les paraphrases sont écrites à la main, une par gold du banc complet. Chaque entrée désigne
# le document et l'indice de la question source : la valeur et le gold sont repris tels quels,
# seule la FORMULATION change — c'est tout l'objet du banc.
ENTREES = [
    # prose — vision.md
    ("docs/theorie/vision.md", 0,
     "Quel numéro identifie le neurone cité en exemple quand le texte définit ce qu'est un fait ?"),
    ("docs/theorie/vision.md", 1,
     "À partir de quelle taille la sonde cesse-t-elle de progresser ?"),
    ("docs/theorie/vision.md", 3,
     "À quel taux de remplissage les listes deviennent-elles moins intéressantes que le reste ?"),
    ("docs/theorie/vision.md", 5,
     "Quelle année figure dans la note de renommage ?"),
    # technique — format-flux.md
    ("docs/implantation/format-flux.md", 0,
     "Sur combien de bits le numéro de version est-il codé ?"),
    ("docs/implantation/format-flux.md", 1,
     "Quelle largeur a l'indice d'un neurone actif dans la liste ?"),
    ("docs/implantation/format-flux.md", 2,
     "Combien d'octets fixes compte une entrée de liste en première version ?"),
    ("docs/implantation/format-flux.md", 7,
     "Quelle quantité de jetons a été traitée en quatre lots de 64 ?"),
    # tableau — roadmap.md
    ("docs/pilotage/roadmap.md", 1,
     "Quel numéro porte la fiche de la mémoire de travail ?"),
    ("docs/pilotage/roadmap.md", 3,
     "Quel pourcentage de temps l'abandon anticipé fait-il gagner ?"),
    ("docs/pilotage/roadmap.md", 4,
     "Quel est le numéro de la phase qui ajoute les trois têtes de lecture ?"),
    ("docs/pilotage/roadmap.md", 9,
     "Quel numéro désigne le raisonnement mené sur l'espace latent ?"),
    # juridique — A_RES_80_1-fr.pdf
    ("data/onu/pdf/A_RES_80_1-fr.pdf", 0,
     "Quel numéro de session figure dans la référence du document préparatoire ?"),
    ("data/onu/pdf/A_RES_80_1-fr.pdf", 1,
     "Quel article de l'accord sur le siège est invoqué pour les représentants ?"),
    ("data/onu/pdf/A_RES_80_1-fr.pdf", 2,
     "Quel jour du mois la réunion citée a-t-elle eu lieu ?"),
    # code — portes.md
    ("docs/methode/portes.md", 0,
     "Quelle durée maximale est accordée à chaque porte ?"),
    ("docs/methode/portes.md", 1,
     "Combien d'épreuves le dernier passage intégral a-t-il exécutées ?"),
    ("docs/methode/portes.md", 2,
     "Quel numéro de jour figure dans le nom du dossier des journaux ?"),
    ("docs/methode/portes.md", 3,
     "Quel code de sortie signale un dépassement de délai ?"),
    # ---- deuxième vague : 30 documents, deux à quatre paraphrases par document ----
    # prose
    ("docs/theorie/lecture-rapide.md", 0,
     "De quelle année date l'étude qui a lancé la mode de la lecture ultra-rapide ?"),
    ("docs/theorie/lecture-rapide.md", 5,
     "De quel pourcentage l'abandon anticipé accélère-t-il ?"),
    ("docs/theorie/lecture-rapide.md", 8,
     "Combien de pièces le protocole d'évaluation doit-il rassembler ?"),
    ("docs/theorie/protocole-semantique.md", 1,
     "Combien de nombres porte le vecteur de sens ?"),
    ("docs/theorie/protocole-semantique.md", 6,
     "Quel est le nombre de propriétés typées du schéma fixe ?"),
    ("docs/theorie/jeux-symboliques.md", 1,
     "Combien de cases compte le plateau du jeu de dames décrit ?"),
    ("docs/theorie/jeux-symboliques.md", 2,
     "Combien d'idées le vocabulaire commun aux langues couvre-t-il ?"),
    ("docs/theorie/jeux-symboliques.md", 3,
     "Quel est le nombre de règles de jeu que les maîtres enseignent ?"),
    ("docs/theorie/semantique-universaux.md", 4,
     "Quel score le premier protocole a-t-il obtenu sur la restitution ?"),
    ("docs/theorie/semantique-universaux.md", 5,
     "Quelle proportion des positions l'outil déterministe décode-t-il ?"),
    ("docs/theorie/architecture-native.md", 0,
     "Combien de millions de paramètres compte le petit modèle natif ?"),
    ("docs/theorie/architecture-native.md", 1,
     "Quelle taille fait le vocabulaire d'entrée du modèle ?"),
    # technique
    ("docs/implantation/format-flux.md", 5,
     "Quelle erreur relative le codage par valeur introduit-il, en pourcentage du maximum ?"),
    ("docs/implantation/format-flux.md", 6,
     "Quel chiffre de perplexité traduit une clé réécrite au mauvais endroit ?"),
    ("docs/implantation/format-flux.md", 8,
     "Quelle phase exige une réponse plutôt qu'un refus ?"),
    ("docs/implantation/document-graph.md", 4,
     "Combien de bits fait le condensat du fichier complet ?"),
    ("docs/implantation/document-graph.md", 7,
     "À partir de quel seuil de recouvrement la découpe est-elle acceptée ?"),
    ("docs/implantation/lecteur-controleur.md", 2,
     "Quelle proportion du document le plus petit budget représente-t-il ?"),
    ("docs/implantation/lecteur-controleur.md", 3,
     "Quelle part du budget la lecture peut-elle consommer au plus ?"),
    ("docs/implantation/lecteur-controleur.md", 4,
     "Quel cinquième de l'enveloppe est gardé pour vérifier ?"),
    ("docs/implantation/contexte-long.md", 1,
     "Combien d'entrées les blocs à portée courte regardent-ils ?"),
    ("docs/implantation/contexte-long.md", 3,
     "Sur combien de bits les clés sont-elles stockées dans la variante compressée ?"),
    ("docs/implantation/convertisseur.md", 1,
     "Combien de milliards de paramètres compte le modèle dont le fichier pèse 60 Go ?"),
    ("docs/implantation/convertisseur.md", 4,
     "Combien de milliards de paramètres le modèle qui tient en 17,7 Go compte-t-il ?"),
    # tableau
    ("docs/pilotage/roadmap.md", 6,
     "Quel identifiant porte le chantier qui bloque sur les cartes tenues ?"),
    ("docs/pilotage/en-cours.md", 6,
     "Quel plafond de contexte est refusé par les essais du modèle ?"),
    ("docs/pilotage/en-cours.md", 9,
     "Combien d'items le réseau de dépendances réunit-il ?"),
    ("docs/pilotage/backlog/index.md", 0,
     "Combien de fiches le backlog contient-il au total ?"),
    ("docs/pilotage/manques.md", 7,
     "Combien d'épreuves le dernier passage complet a-t-il lancées ?"),
    ("docs/pilotage/manques.md", 2,
     "Quel débit le disque atteint-il au hasard sur l'array ?"),
    ("docs/pilotage/manques.md", 8,
     "Combien d'épreuves de rappel le réseau a-t-il passées à longue portée ?"),
    ("docs/pilotage/references-non-regression.md", 0,
     "Combien d'épreuves le dernier passage intégral a-t-il lancées ?"),
    ("docs/pilotage/references-non-regression.md", 3,
     "Combien de renvois internes le script a-t-il validés ?"),
    # juridique
    ("data/onu/pdf/A_RES_80_1-en.pdf", 0,
     "Quel numéro de session figure dans la référence du projet de résolution ?"),
    ("data/onu/pdf/A_RES_80_1-en.pdf", 1,
     "Quel article de l'accord de siège est cité pour les représentants ?"),
    ("data/onu/pdf/A_RES_80_1-en.pdf", 2,
     "Quel jour du mois l'assemblée mentionnée a-t-elle eu lieu ?"),
    ("data/onu/pdf/A_RES_80_1-es.pdf", 0,
     "Quel numéro de session apparaît dans la référence du document préparatoire ?"),
    ("data/onu/pdf/A_RES_80_1-es.pdf", 1,
     "Quelle section de l'accord sur le siège concerne les représentants ?"),
    ("data/onu/pdf/A_RES_80_1-es.pdf", 2,
     "Quel jour du mois la réunion citée s'est-elle tenue ?"),
    ("data/onu/pdf/A_RES_80_10-en.pdf", 0,
     "Quel point de l'ordre du jour est examiné à cette session ?"),
    ("data/onu/pdf/A_RES_80_10-fr.pdf", 0,
     "Quel thème de l'ordre du jour ouvre le document ?"),
    ("data/onu/pdf/A_RES_80_10-es.pdf", 0,
     "Quel point de l'ordre du jour ouvre le document ?"),
    ("data/onu/pdf/A_RES_80_10-en.pdf", 5,
     "Quel numéro porte la recommandation sur les droits des femmes autochtones ?"),
    # code
    ("docs/pilotage/utilisation.md", 2,
     "À partir de quelle version de Python l'intégration continue du projet tourne-t-elle ?"),
    ("docs/pilotage/utilisation.md", 7,
     "Quel score l'adaptation de faible rang obtient-elle sur l'exercice de copie ?"),
    ("docs/pilotage/utilisation.md", 8,
     "Quel taux le réseau à couches cachées obtient-il avec de mauvais paramètres ?"),
    ("docs/implantation/configuration-nvme-raid-amd.md", 3,
     "Combien de gigaoctets de fichiers faut-il écrire pour épuiser la mémoire tampon ?"),
    ("docs/implantation/configuration-nvme-raid-amd.md", 6,
     "Quelle taille fait la zone d'échange de la machine ?"),
    ("docs/implantation/format-clusters.md", 3,
     "Quelle longueur d'empreinte est comparée pour vérifier chaque tenseur ?"),
    ("docs/implantation/format-clusters.md", 6,
     "Combien de tableaux de nombres le manifeste recense-t-il ?"),
    ("docs/methode/portes.md", 5,
     "Quelle quantité de mémoire graphique un modèle occupé prend-il pendant une passe ?"),
    ("docs/methode/portes.md", 7,
     "Combien de lignes du journal faut-il lire pour connaître la cause d'un échec ?"),
    ("docs/implantation/numa-segregation.md", 1,
     "Quelle vitesse le pont NVLink atteint-il dans chaque direction ?"),
    ("docs/implantation/numa-segregation.md", 4,
     "Quelle taille de RAM faut-il garder des deux côtés ?"),
    ("docs/methode/continuite.md", 2,
     "Quel plafond de mots l'état courant ne doit-il pas dépasser ?"),
    ("docs/theorie/lecture-rapide.md", 2,
     "Quel volume les tampons d'avance ont-ils traité ?"),
    ("docs/theorie/protocole-semantique.md", 4,
     "Combien de langues la première exécution du protocole a-t-elle couvertes ?"),
    ("docs/implantation/contexte-long.md", 5,
     "Quel facteur les blocs du réseau appliquent-ils aux lancements graphiques ?"),
    ("docs/implantation/convertisseur.md", 6,
     "Quelle vitesse avait été annoncée avant la mesure ?"),
    ("docs/pilotage/roadmap.md", 8,
     "Quel identifiant désigne le manque de corpus d'articles ?"),
    ("docs/pilotage/backlog/dependances.md", 4,
     "Quel numéro porte la restitution après le gist ?"),
    ("data/onu/pdf/A_RES_80_10-en.pdf", 3,
     "Quelle année borne l'agenda du développement durable ?"),
    ("docs/pilotage/utilisation.md", 3,
     "À quelle date le vieux démon a-t-il cessé d'être utilisé ?"),
    ("docs/implantation/configuration-nvme-raid-amd.md", 1,
     "Quel paragraphe traite du read_ahead_kb resté ouvert ?"),
    ("docs/implantation/format-clusters.md", 4,
     "Combien de nœuds la nouvelle disposition épargne-t-elle ?"),
]


def construit() -> dict:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    par_chemin = {d["chemin"]: d for d in source["documents"]}
    documents: dict[str, dict] = {}
    for chemin, indice_source, question in ENTREES:
        origine = par_chemin[chemin]
        q = origine["questions"][indice_source]
        document = documents.setdefault(
            chemin, {"chemin": chemin, "type": origine["type"], "questions": []})
        document["questions"].append({
            "question": question, "indice": q["indice"], "valeur": q["valeur"],
            "source": q["question"],
        })
    return {"version": 1, "date": "2026-10-29",
            "note": ("Banc durci R0.3 : questions PARAPHRASES, écrites à la main sur des golds "
                     "du banc complet. Le recouvrement lexical question↔gold est vérifié < 0,5. "
                     "Mesure la compréhension, pas la couverture."),
            "documents": list(documents.values())}


def passages_du(chemin: str) -> list[str]:
    manifeste = graphe_document.manifeste(RACINE / chemin)
    return [p["texte"] for p in lc.passages(manifeste)]


def recouvrement(question: str, gold: str) -> float:
    mots = set(lc.jetons(question))
    if not mots:
        return 1.0
    return len(mots & set(lc.jetons(gold))) / len(mots)


def verifie(chemin: pathlib.Path) -> int:
    data = json.loads(chemin.read_text(encoding="utf-8"))
    problemes, recouvrements = 0, []
    for document in data["documents"]:
        textes = passages_du(document["chemin"])
        for q in document["questions"]:
            golds = [t for t in textes if q["indice"] in t]
            if not golds:
                print(f"❌ {document['chemin']} : gold introuvable ({q['question'][:50]})")
                problemes += 1
                continue
            part = recouvrement(q["question"], golds[0])
            recouvrements.append(part)
            if part >= SEUIL_RECOUVREMENT:
                print(f"❌ recouvrement {part:.2f} ≥ {SEUIL_RECOUVREMENT} : {q['question'][:60]}")
                problemes += 1
            if q["valeur"].lower() in q["question"].lower():
                print(f"❌ la valeur est dans la question : {q['question'][:60]}")
                problemes += 1
    moyenne = sum(recouvrements) / len(recouvrements) if recouvrements else 0
    print(f"{len(recouvrements)} questions · recouvrement moyen {moyenne:.2f} "
          f"(max {max(recouvrements):.2f}) · {problemes} problème(s)")
    return 0 if problemes == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="R0.3 durci — les paraphrases.")
    ap.add_argument("--ecrit", type=pathlib.Path)
    ap.add_argument("--verifie", type=pathlib.Path)
    args = ap.parse_args()
    if args.verifie:
        return verifie(args.verifie)
    data = construit()
    total = sum(len(d["questions"]) for d in data["documents"])
    print(f"{total} questions paraphrases · {len(data['documents'])} documents")
    if args.ecrit:
        args.ecrit.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"écrit : {args.ecrit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""prompts_publics.py — les prompts du banc externe, sans donnée privée.

Deux sources, toutes deux publiques :
1. la **Déclaration universelle des droits de l'homme** (`data/udhr/articles.jsonl`,
   domaine public) : cinq articles en anglais, traduits vers dix langues, avec la
   **traduction humaine officielle** comme référence pour le chrF ;
2. des **questions de jeux** (dames, échecs, go, cartes, morpion), écrites pour ce
   banc, sans texte sous licence.

Le fichier produit (`prompts_publics.jsonl`) ne contient **que les prompts** et les
références ; aucune sortie de modèle. Il est versionné, donc la mesure est
reproductible. Le script est séparé : les données UDHR sont dans `data/` (gitignoré).
"""
from __future__ import annotations

import json
import pathlib

RACINE = pathlib.Path(__file__).resolve().parents[2]
ARTICLES = RACINE / "data" / "udhr" / "articles.jsonl"
SORTIE = pathlib.Path(__file__).resolve().parent / "prompts_publics.jsonl"

CIBLES = [("fra", "français"), ("spa", "espagnol"), ("deu", "allemand"),
          ("ita", "italien"), ("por", "portugais"), ("rus", "russe"),
          ("arb", "arabe"), ("cmn", "chinois mandarin"), ("hin", "hindi"),
          ("swh", "swahili")]

JEUX = [
    ("jeu-go-coins", "Explique en cinq phrases pourquoi, au go, les coins passent avant les côtés et les côtés avant le centre. Donne un contre-exemple où ce principe échoue."),
    ("jeu-go-ko", "Explique le ko au go en trois phrases, puis décris un ko simple et un ko positionnel."),
    ("jeu-echecs-centre", "Explique le principe du contrôle du centre aux échecs selon Lasker et Capablanca. Donne une position de départ et le premier coup recommandé."),
    ("jeu-echecs-developpement", "Pourquoi développer les pièces avant d'attaquer ? Donne trois conséquences concrètes d'un développement retardé."),
    ("jeu-echecs-colonnes", "Qu'est-ce qu'une colonne ouverte, et pourquoi une tour y vaut-elle mieux ? Donne un exemple."),
    ("jeu-dames-ligne", "Aux dames anglaises, pourquoi garder la ligne de fond le plus longtemps possible ? Relie cela à la promotion."),
    ("jeu-dames-prises", "Explique la règle de prise obligatoire aux dames anglaises et la différence entre une prise simple et une prise multiple."),
    ("jeu-cartes-longue", "Au whist, pourquoi entamer de la couleur la plus longue ? Explique la règle de la seconde main basse et celle de la troisième main haute."),
    ("jeu-cartes-honneur", "Au whist, que veut dire « couvrir un honneur » ? Donne un exemple avec un valet, une dame et un roi."),
    ("jeu-morpion", "Le morpion est résolu. Explique pourquoi la partie parfaite est nulle et pourquoi le centre est le premier coup naturel."),
]


def _lire_articles() -> dict[tuple[str, int], str]:
    out = {}
    for ligne in ARTICLES.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        d = json.loads(ligne)
        cle = (d["iso3"], int(d["art"]))
        if cle not in out:
            out[cle] = d["texte"]
    return out


def construire() -> list[dict]:
    articles = _lire_articles()
    prompts = []
    for art in range(1, 6):
        source = articles.get(("eng", art))
        if not source:
            continue
        for iso3, nom in CIBLES:
            reference = articles.get((iso3, art))
            if not reference:
                continue
            prompts.append({
                "id": f"udhr-{art:02d}-{iso3}",
                "system": "Tu es un traducteur professionnel. Réponds uniquement par la traduction, sans commentaire.",
                "prompt": (f"Traduis en {nom} l'article {art} de la Déclaration universelle "
                           f"des droits de l'homme. Réponds uniquement par la traduction.\n\n{source}"),
                "meta": {"source": "UDHR", "art": art, "langue_source": "eng",
                         "cible_iso3": iso3, "cible_nom": nom, "reference": reference,
                         "categorie": "traduction"},
            })
    for ident, prompt in JEUX:
        prompts.append({
            "id": ident,
            "system": "Tu es un professeur de jeux de réflexion. Réponds en français, avec des exemples concrets.",
            "prompt": prompt,
            "meta": {"source": "banc de jeux", "categorie": "jeu"},
        })
    return prompts


def main() -> int:
    prompts = construire()
    SORTIE.write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in prompts),
                      encoding="utf-8")
    print(f"écrit {SORTIE} : {len(prompts)} prompts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

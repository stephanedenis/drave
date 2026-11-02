"""Le juge des réponses : la mesure qui manque — la correction, pas la présence.

Le bloc ne répond pas au contenu (0/19) ; mais mesure-t-on seulement la *présence* d'une
réponse ? Ce module pose le juge : une réponse candidate est comparée à une **référence**
(le gold). Il mesure aussi la **couverture** : combien de questions du gold portent une
référence. Sans référence, aucun juge ne peut mesurer la correction.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from tools.tests.linguistique.evaluer_gold import charger


def juge(reponse_candidate, reference) -> float:
    """1.0 si la réponse candidate égale la référence (normalisée), 0.0 sinon."""
    if reference is None or reponse_candidate is None:
        return 0.0
    norm = lambda s: " ".join(str(s).lower().split())
    return 1.0 if norm(reponse_candidate) == norm(reference) else 0.0


def couverture(phrases: list[dict]) -> dict:
    """La part des questions du gold qui portent une réponse de référence."""
    q = [p for p in phrases if "?" in p["texte"]]
    avec = sum(1 for p in q if (p.get("pragma") or {}).get("reponse"))
    return {"questions": len(q), "avec_reference": avec,
            "taux": round(avec / max(1, len(q)), 4)}


def main() -> int:
    ph = charger()
    c = couverture(ph)
    print("couverture du juge :", c)
    ex = [p for p in ph if "?" in p["texte"]][:3]
    for p in ex:
        ref = (p.get("pragma") or {}).get("reponse")
        print(p["id"], "| référence", ref, "| juge(None, ref)", juge(None, ref))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

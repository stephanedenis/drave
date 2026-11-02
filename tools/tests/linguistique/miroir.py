"""Le miroir entrée/sortie du bloc linguistique : restitution et fidélité.

Règle 6 : toute mesure d'entrée se double d'une mesure de sortie. `rendre` reconstruit
le texte depuis les étiquettes de **surface** (`graphème`, `mot`) ; `fidelite` le compare
à la source. La **fluidité** (longueur, ponctuation) n'est pas la **fidélité** : une
restitution peut être fluide et infidèle, ou fidèle et hachée.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import tools.bloc_linguistique as bl
from tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc


def rendre(a: bl.Annotation) -> str:
    """Reconstruit le texte depuis les étiquettes de surface, sans lire `a.texte`."""
    g = [e for e in a.etiquettes if e.niveau == "graphème"]
    if not g:
        return ""
    return "".join(e.valeur for e in sorted(g, key=lambda e: (e.debut, e.fin)))


def fidelite(a: bl.Annotation, source: str) -> float:
    """1.0 si la restitution égale la source, 0.0 sinon (la mesure est binaire ici)."""
    return 1.0 if rendre(a) == source else 0.0


def rendre_mots(a: bl.Annotation) -> str:
    """Restitution depuis le niveau `mot` : la surface, token par token, espacée."""
    mots = [e for e in a.etiquettes if e.niveau == "mot"]
    return " ".join(e.valeur for e in sorted(mots, key=lambda e: (e.debut, e.fin)))


def fidelite_mots(a: bl.Annotation, source: str) -> float:
    """La fidélité des mots : la suite des tokens est-elle celle de la source ?"""
    return 1.0 if rendre_mots(a) == " ".join(source.split()) else 0.0


def fluidite(a: bl.Annotation) -> float:
    """La part de la longueur restituée qui est du texte (pas des trous)."""
    r = rendre(a)
    return round(len(r) / max(1, len(a.texte)), 4)


def mesurer(phrases: list[dict], bloc=None) -> dict:
    bloc = bloc or bl.Heuristique()
    fid = 0.0
    flu = []
    details = []
    for p in phrases:
        a = bloc.analyser(p["texte"], p["langue"])
        f = min(fidelite(a, p["texte"]), fidelite_mots(a, p["texte"]))
        fid += f
        flu.append(fluidite(a))
        if f < 1.0:
            details.append({"id": p["id"], "source": p["texte"], "rendu": rendre(a)[:80]})
    n = max(1, len(phrases))
    return {"phrases": len(phrases), "fidelite": round(fid / n, 4),
            "fluidite": round(sum(flu) / n, 4), "echecs": details[:5]}


def main() -> int:
    ph = charger()
    for nom, bloc in (("heuristique", bl.Heuristique()),
                      ("cascade", bl.Cascade(bl.Heuristique(), bl.MockNeuronal()))):
        r = mesurer(ph, bloc)
        print(nom, r["phrases"], "fidélité", r["fidelite"], "fluidité", r["fluidite"],
              "échecs", len(r["echecs"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

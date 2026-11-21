#!/usr/bin/env python3
"""rsn.py — la représentation sémantique neutre : les candidats, l'état, l'empreinte.

LA FONDATION. Le produit lit un texte et rend une `Annotation` (le POS, les syntagmes, les
attachements). Ce module en tire la **RSN** : un **état** fait de **candidats**, chacun avec un
**corps canonique**, une **annotation** (confiance, provenance), un **statut**, un **coût** et un
**score**. C'est le matériau que le moteur de pensée manipule (`moteur-de-pensee.md`) : sans RSN, il
n'a rien à faire tourner.

LE CONTRAT (repris de `docs/implantation/moteur-de-pensee.md`) :
  - `corps` : un dict canonique — clés triées, pas de flottants, UTF-8. `H(corps)` est stable.
  - `empreinte` : le Merkle des empreintes des candidats, **triées** — deux états identiques ont la
    même empreinte quel que soit l'ordre d'insertion.
  - `statut` : `hypothese` · `retenu` · `refute` · `ouvert`.
  - `confiance` : la confiance **déclarée** du candidat (celle de l'étiquette source), pas une
    précision mesurée.

LA SURFACE → LA RSN. Un candidat est une **lecture possible** d'un fait de surface :
  - une étiquette (POS, syntagme, attachement) devient un candidat « fait » ;
  - un syntagme avec un rôle et une cible devient une **prédication candidate** (sujet, verbe,
    objet, circonstant) — c'est la brique du sens ;
  - l'ambiguïté est **conservée** : deux étiquettes concurrentes du même span donnent deux candidats.

Usage :
  python3 tools/rsn.py --texte "Le chat de la voisine dort." --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

STATUTS = ("hypothese", "retenu", "refute", "ouvert")


def canonicaliser(corps: dict) -> bytes:
    """Le corps canonique : clés triées, pas d'espaces, UTF-8, aucun flottant."""
    def _propre(v):
        if isinstance(v, float):
            raise TypeError("aucun flottant dans un corps : mets-le dans l'annotation")
        if isinstance(v, dict):
            return {str(k): _propre(x) for k, x in sorted(v.items())}
        if isinstance(v, (list, tuple)):
            return [_propre(x) for x in v]
        return v
    return json.dumps(_propre(corps), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def h(corps: dict) -> str:
    """L'empreinte d'un corps : sha256 du canonique."""
    return hashlib.sha256(canonicaliser(corps)).hexdigest()


def empreinte(candidats: list["Candidate"]) -> str:
    """L'empreinte d'un état : le Merkle des empreintes des candidats, triées."""
    return hashlib.sha256("".join(sorted(c.empreinte for c in candidats)).encode()).hexdigest()


class Candidate:
    """Un candidat de la RSN : un corps canonique et son annotation."""

    __slots__ = ("corps", "annotation", "statut", "provenance", "cout", "score")

    def __init__(self, corps: dict, annotation: dict | None = None,
                 statut: str = "hypothese", provenance: dict | None = None,
                 cout: dict | None = None, score: float | None = None):
        if statut not in STATUTS:
            raise ValueError(f"statut inconnu : {statut}")
        self.corps = corps
        self.annotation = dict(annotation or {})
        self.statut = statut
        self.provenance = dict(provenance or {})
        self.cout = dict(cout or {"noeuds": 1})
        self.score = score if score is not None else float(self.annotation.get("confiance", 0.5))

    @property
    def empreinte(self) -> str:
        return h(self.corps)

    def json(self) -> dict:
        return {"corps": self.corps, "empreinte": self.empreinte,
                "annotation": self.annotation, "statut": self.statut,
                "provenance": self.provenance, "cout": self.cout,
                "score": round(float(self.score), 4)}


class State:
    """Un état de la RSN : des candidats, un parent, une empreinte de Merkle."""

    __slots__ = ("id", "parent", "profondeur", "candidats", "budget", "statut")

    def __init__(self, id: str, candidats: list[Candidate], parent: str | None = None,
                 profondeur: int = 0, budget: dict | None = None, statut: str = "ouvert"):
        self.id = id
        self.parent = parent
        self.profondeur = profondeur
        self.candidats = list(candidats)
        self.budget = dict(budget or {"noeuds": len(self.candidats), "max": 50})
        self.statut = statut

    @property
    def empreinte(self) -> str:
        return empreinte(self.candidats)

    def retenus(self) -> list[Candidate]:
        return [c for c in self.candidats if c.statut == "retenu"]

    def json(self) -> dict:
        return {"id": self.id, "parent": self.parent, "profondeur": self.profondeur,
                "budget": self.budget, "statut": self.statut,
                "candidats": [c.empreinte for c in self.candidats],
                "empreinte": self.empreinte,
                "detail": [c.json() for c in self.candidats]}


def _predication(et: "bl.Etiquette") -> dict | None:
    """Un syntagme avec rôle et cible → une prédication candidate (le corps canonique)."""
    meta = et.meta or {}
    att = meta.get("attachement") or {}
    if not att:
        return None
    return {
        "type": "predication",
        "role": str(meta.get("role") or et.type),
        "forme": str(et.valeur),
        "debut": int(et.debut),
        "fin": int(et.fin),
        "cible": {"forme": str(att.get("cible", ""))},
        "niveau": int(meta.get("niveau", 0) or 0),
        "langue": str(et.langue),
    }


def depuis_annotation(annotation, source: str = "heuristique") -> State:
    """La surface → la RSN : une Annotation devient un état de candidats."""
    import tools.bloc_linguistique as bl  # noqa: F401 — le type est duck-typé

    cands: list[Candidate] = []
    for et in getattr(annotation, "etiquettes", []):
        corps = {"type": "fait", "niveau": str(et.niveau), "classe": str(et.type),
                 "forme": str(et.valeur), "debut": int(et.debut), "fin": int(et.fin),
                 "langue": str(et.langue)}
        cands.append(Candidate(
            corps,
            annotation={"confiance": float(et.confiance), "source": str(et.source),
                        "candidats": list(getattr(et, "candidats", []))},
            statut="hypothese",
            provenance={"operateur": f"{source}.etiquette", "pas": 0},
        ))
        pred = _predication(et)
        if pred is not None:
            cands.append(Candidate(
                pred,
                annotation={"confiance": float(et.confiance), "source": str(et.source)},
                statut="hypothese",
                provenance={"operateur": f"{source}.predication", "pas": 0},
            ))

    # les prédications sont les candidats les plus structurants : on les met « retenu » quand
    # leur confiance dépasse celle des faits — c'est le premier tri, pas une vérité.
    seuil = 0.7
    for c in cands:
        if c.corps["type"] == "predication" and c.score >= seuil:
            c.statut = "retenu"

    return State("s0", cands, parent=None, profondeur=0,
                 budget={"noeuds": len(cands), "max": 50}, statut="ouvert")


def analyser_et_rsn(texte: str, langue: str | None = None, contexte: str | None = None,
                    tagger: bool = False) -> State:
    """Le chemin complet : le texte → l'annotation → la RSN."""
    import tools.bloc_linguistique as bl

    annotation = bl.Heuristique().analyser(texte, langue, contexte)
    return depuis_annotation(annotation, source=getattr(annotation, "source", "heuristique"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--texte", required=True)
    ap.add_argument("--langue", default=None)
    ap.add_argument("--tagger", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    etat = analyser_et_rsn(a.texte, a.langue, tagger=a.tagger)
    if a.json:
        print(json.dumps({"schema": "drave.rsn", "version": 1, "etat": etat.json()},
                         ensure_ascii=False, indent=2))
    else:
        print(f"état {etat.id} · {len(etat.candidats)} candidats · {len(etat.retenus())} retenus · "
              f"empreinte {etat.empreinte[:16]}")
        for c in etat.candidats[:8]:
            print(f"  [{c.statut:9s}] {c.corps['type']:11s} {c.corps.get('forme', '')[:40]!r} "
                  f"(score {c.score:.2f})")


if __name__ == "__main__":
    main()

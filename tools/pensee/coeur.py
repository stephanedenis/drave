"""coeur.py — les types du moteur de pensée, et leur forme canonique.

Le contrat est dans [`docs/implantation/moteur-de-pensee.md`](../../docs/implantation/moteur-de-pensee.md).
Un **état** porte des **candidats** ; son empreinte est le **Merkle** des empreintes de ses
candidats, **triées**. Deux états qui portent les mêmes candidats ont la même empreinte quel que
soit l'ordre d'insertion — c'est la transposition, et c'est ce qui rend l'arbre un DAG.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


def canonique(objet: Any) -> bytes:
    """JSON canonique : clés triées, aucun espace, UTF-8, aucun flottant.

    Un flottant dans un `corps` rendrait l'empreinte dépendante de la représentation binaire ;
    on le refuse. Les scores et les coûts vivent dans l'état, pas dans le corps.
    """
    def controle(x):
        if isinstance(x, float):
            raise TypeError("flottant interdit dans un corps canonique")
        if isinstance(x, dict):
            return {k: controle(v) for k, v in sorted(x.items())}
        if isinstance(x, (list, tuple)):
            return [controle(v) for v in x]
        return x
    return json.dumps(controle(objet), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def h(objet: Any) -> str:
    return hashlib.sha256(canonique(objet)).hexdigest()


@dataclass(frozen=True)
class Candidat:
    id: str
    corps: dict
    annotation: dict = field(default_factory=dict)
    statut: str = "hypothese"

    def empreinte(self) -> str:
        return h(self.corps)

    def vers_dict(self) -> dict:
        return {"id": self.id, "corps": self.corps, "annotation": self.annotation,
                "statut": self.statut}


@dataclass
class Etat:
    id: str
    parent: str | None
    profondeur: int
    candidats: tuple[Candidat, ...]
    statut: str = "ouvert"

    def empreinte(self) -> str:
        """Merkle des empreintes des candidats **triées**."""
        feuilles = sorted(c.empreinte() for c in self.candidats)
        return hashlib.sha256(("merkle:" + "|".join(feuilles)).encode("utf-8")).hexdigest()

    def corps_merkle(self) -> dict:
        return {"type": "etat", "candidats": sorted(c.empreinte() for c in self.candidats)}

    def vers_dict(self) -> dict:
        return {"id": self.id, "parent": self.parent, "profondeur": self.profondeur,
                "statut": self.statut, "candidats": [c.vers_dict() for c in self.candidats]}


@dataclass
class Noeud:
    empreinte: str
    score: float = 0.0
    cout: int = 0
    visites: int = 0


@dataclass(frozen=True)
class Arete:
    parent: str
    enfant: str
    operateur: str
    params: dict
    score: float


@dataclass
class Decision:
    etat: Etat
    justification: list[str]
    budget_consomme: int
    strategie: str

    def vers_dict(self) -> dict:
        return {"etat": self.etat.id, "empreinte": self.etat.empreinte(),
                "justification": self.justification,
                "budget_consomme": self.budget_consomme, "strategie": self.strategie}

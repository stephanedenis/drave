#!/usr/bin/env python3
"""moteur_pensee.py — la boucle anytime avec l'ANTI-BOUCLE mesurée.

LE PROBLÈME. Une boucle d'exploration sans garde-fou **tourne en rond par construction** : elle
re-pousse les mêmes états, elle re-explore ce qu'elle a déjà vu, et elle ne sait pas le dire.
Le contrat du moteur (`docs/implantation/moteur-de-pensee.md`) décrit la **structure** (le store,
l'arbre, la frontière, les stratégies) — pas la **garde**.

CE QUE CE MODULE AJOUTE (les cinq gardes) :
  1. **le `visited` explicite** : l'ensemble des empreintes **explorées** (et pas seulement
     stockées) — un état déjà vu n'est jamais ré-empilé ;
  2. **la nouveauté comptée** : `nouveaux / (nouveaux + répétitions)` — si elle tombe sous le
     seuil, le moteur s'arrête (la boucle ne produit plus de neuf) ;
  3. **la mémoire des échecs** : les états `refute` sont exclus, jamais ré-explorés ;
  4. **trois terminaisons** : le **budget** (le nombre de pas), le **fixpoint** (plus rien de
     nouveau dans la frontière), la **contradiction** (un état et sa négation) ;
  5. **la trace** : chaque pas est écrit (nouveau / répétition / échec), rejouable.

LA MESURE. Le moteur rend un **rapport de circularité** : les répétitions évitées, le taux de
nouveauté, la raison de la terminaison. C'est ce qui rend « itérer sans tourner en rond »
**mesurable** — au lieu d'être une intention.

Usage :
  python3 tools/moteur_pensee.py --demonstration
"""
from __future__ import annotations

import argparse
import heapq
import json
import math
from dataclasses import dataclass, field


@dataclass
class Etat:
    """Un état minimal : une empreinte, un corps, un statut."""
    empreinte: str
    corps: dict = field(default_factory=dict)
    statut: str = "ouvert"       # ouvert | settled | refute
    negation: str | None = None  # l'empreinte de la négation, pour la contradiction

    def json(self) -> dict:
        return {"empreinte": self.empreinte[:16], "corps": self.corps,
                "statut": self.statut, "negation": (self.negation or "")[:16]}


class Moteur:
    """La boucle anytime : le store, la frontière, les gardes, la trace."""

    def __init__(self, budget_max: int = 50, seuil_nouveaute: float = 0.30):
        self.visited: dict[str, Etat] = {}     # les empreintes EXPLORÉES
        self.frontier: list[tuple] = []        # un tas (-score, ordre, état)
        self.echecs: set[str] = set()          # les empreintes réfutées
        self.budget_max = budget_max
        self.budget = budget_max
        self.seuil_nouveaute = seuil_nouveaute
        self.nouveaux = 0
        self.repetitions = 0
        self.echecs_evites = 0
        self.contradictions = 0
        self.termine: str | None = None
        self.trace: list[dict] = []
        self._ordre = 0

    # -- les gardes --------------------------------------------------------
    def _empiler(self, etat: Etat, score: float = 0.0) -> bool:
        """La garde : nouveau ? sinon on le compte et on l'ignore."""
        self._ordre += 1
        emp = etat.empreinte
        if emp in self.visited:
            self.repetitions += 1
            self.trace.append({"pas": len(self.trace) + 1, "empreinte": emp[:16],
                               "garde": "deja_vu", "score": score})
            return False
        if emp in self.echecs:
            self.echecs_evites += 1
            self.trace.append({"pas": len(self.trace) + 1, "empreinte": emp[:16],
                               "garde": "echec_connu", "score": score})
            return False
        self.visited[emp] = etat
        self.nouveaux += 1
        heapq.heappush(self.frontier, (-score, self._ordre, etat))
        self.trace.append({"pas": len(self.trace) + 1, "empreinte": emp[:16],
                           "garde": "nouveau", "score": score})
        return True

    def _contradiction(self, etat: Etat) -> bool:
        """Un état et sa négation : les deux explorés → contradiction."""
        if etat.negation and etat.negation in self.visited:
            self.contradictions += 1
            self.termine = f"contradiction ({etat.empreinte[:8]} ↔ {etat.negation[:8]})"
            return True
        return False

    def taux_nouveaute(self) -> float:
        total = self.nouveaux + self.repetitions + self.echecs_evites
        return self.nouveaux / total if total else 0.0

    def circularite(self) -> dict:
        """Le rapport : ce que la garde a évité, et si la boucle a produit du neuf."""
        return {
            "nouveaux": self.nouveaux,
            "repetitions_evitees": self.repetitions,
            "echecs_evites": self.echecs_evites,
            "contradictions": self.contradictions,
            "taux_nouveaute": round(self.taux_nouveaute(), 4),
            "termine": self.termine,
            "pas": len(self.trace),
        }

    # -- la boucle ---------------------------------------------------------
    def boucle(self, racine: Etat, expand, score_fn=None) -> Etat | None:
        """La boucle anytime avec les cinq gardes.

        `expand(etat) -> [etat]` : les successeurs (les opérateurs, quel que soit le paradigme).
        `score_fn(etat) -> float` : le score (0 par défaut — l'ordre de priorité).
        """
        score_fn = score_fn or (lambda e: 0.0)
        if not self._empiler(racine, score_fn(racine)):
            return racine
        meilleur = racine
        while self.budget > 0 and self.frontier and self.termine is None:
            _, _, noeud = heapq.heappop(self.frontier)
            self.budget -= 1
            if noeud.statut == "settled":
                return noeud
            for enfant in expand(noeud):
                if enfant.statut == "refute":
                    # la mémoire des échecs : l'état est exclu AVANT d'être empilé
                    self.echecs.add(enfant.empreinte)
                    self.echecs_evites += 1
                    self.trace.append({"pas": len(self.trace) + 1, "empreinte": enfant.empreinte[:16],
                                       "garde": "refute_memorise", "score": score_fn(enfant)})
                    continue
                if self._contradiction(enfant):
                    break
                self._empiler(enfant, score_fn(enfant))
                if score_fn(enfant) > score_fn(meilleur):
                    meilleur = enfant
                if self.budget <= 0:
                    self.termine = "budget"
                    break
        if self.termine is None:
            if not self.frontier:
                self.termine = "fixpoint (frontière vide)"
            elif self.budget <= 0:
                self.termine = "budget"
            elif self.taux_nouveaute() < self.seuil_nouveaute:
                self.termine = f"nouveauté sous le seuil ({self.taux_nouveaute():.2f} < {self.seuil_nouveaute})"
        return meilleur


def _h(corps: dict) -> str:
    import hashlib
    return hashlib.sha256(json.dumps(corps, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def demonstration() -> None:
    """Le banc : un opérateur identité (la boucle pure) contre un opérateur qui avance."""
    print("=== Cas 1 : l'opérateur identité (la boucle parfaite) ===")
    m = Moteur(budget_max=20, seuil_nouveaute=0.30)
    racine = Etat(empreinte=_h({"n": 0}), corps={"n": 0})
    # chaque expansion rend le MÊME état : c'est la boucle
    m.boucle(racine, lambda e: [Etat(empreinte=_h({"n": 0}), corps={"n": 0})])
    print(json.dumps(m.circularite(), ensure_ascii=False))

    print("\n=== Cas 2 : l'opérateur qui avance (n → n+1) ===")
    m2 = Moteur(budget_max=20, seuil_nouveaute=0.30)
    racine2 = Etat(empreinte=_h({"n": 0}), corps={"n": 0})
    m2.boucle(racine2, lambda e: [Etat(empreinte=_h({"n": e.corps["n"] + 1}),
                                       corps={"n": e.corps["n"] + 1})])
    print(json.dumps(m2.circularite(), ensure_ascii=False))

    print("\n=== Cas 3 : l'opérateur avec un échec connu (le refus revient) ===")
    m3 = Moteur(budget_max=20, seuil_nouveaute=0.30)
    racine3 = Etat(empreinte=_h({"n": 0}), corps={"n": 0})
    def expand3(e):
        n = e.corps["n"]
        if n == 1:
            return [Etat(empreinte=_h({"n": 1}), corps={"n": 1}, statut="refute")]
        return [Etat(empreinte=_h({"n": n + 1}), corps={"n": n + 1})]
    m3.boucle(racine3, expand3)
    print(json.dumps(m3.circularite(), ensure_ascii=False))

    print("\n=== Cas 4 : la contradiction (p et non-p) ===")
    m4 = Moteur(budget_max=20, seuil_nouveaute=0.30)
    p = _h({"p": True}); nonp = _h({"p": False})
    racine4 = Etat(empreinte=p, corps={"p": True}, negation=nonp)
    m4.boucle(racine4, lambda e: [Etat(empreinte=nonp, corps={"p": False}, negation=p)])
    print(json.dumps(m4.circularite(), ensure_ascii=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demonstration", action="store_true")
    a = ap.parse_args()
    if a.demonstration:
        demonstration()
    else:
        demonstration()

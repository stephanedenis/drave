#!/usr/bin/env python3
"""bus.py — le bus d'événements des modules cerveau-langage.

Un événement est un **fait** typé, horodaté, avec sa source. Le bus le journalise,
le pousse aux abonnés et sait le **rejouer**. C'est le contrat minimal qui permet
de composer M1–M9 sans les fondre dans un seul bloc.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterator


@dataclass(frozen=True)
class Evenement:
    type: str
    valeur: Any
    source: str
    t: int = 0
    meta: tuple[tuple[str, Any], ...] = ()

    def vers_dict(self) -> dict:
        return {"type": self.type, "source": self.source, "t": self.t,
                "valeur": self.valeur, "meta": dict(self.meta)}


class Bus:
    def __init__(self) -> None:
        self.journal: list[Evenement] = []
        self.abonnes: dict[str, list[Callable[[Evenement], None]]] = {}
        self._t = 0

    def abonner(self, type_: str, f: Callable[[Evenement], None]) -> None:
        self.abonnes.setdefault(type_, []).append(f)

    def publier(self, type_: str, valeur: Any, source: str,
                meta: dict | None = None) -> Evenement:
        self._t += 1
        e = Evenement(type_, valeur, source, self._t, tuple(sorted((meta or {}).items())))
        self.journal.append(e)
        for f in self.abonnes.get(type_, ()):
            f(e)
        return e

    def rejouer(self, type_: str | None = None) -> Iterator[Evenement]:
        for e in self.journal:
            if type_ is None or e.type == type_:
                yield e

    def compter(self, type_: str) -> int:
        return sum(1 for e in self.rejouer(type_))

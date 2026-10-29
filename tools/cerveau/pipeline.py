#!/usr/bin/env python3
"""pipeline.py — la chaîne minimale M1 → M4 → M8, sur un seul bus.

Le pipeline ne prétend pas être un cerveau : il vérifie que les modules se
**chaînent** sans se contredire. La surface est perçue par M1, stockée par M4,
résumée par M8 ; la lecture d'un code partiel passe par M4 et, si M8 a consolidé,
par ses prototypes.
"""
from __future__ import annotations

from .bus import Bus
from .episodique import Episodique
from .hub import Hub
from .sommeil import Sommeil


class Pipeline:
    nom = "pipeline-M1-M4-M8"

    def __init__(self) -> None:
        self.bus = Bus()
        self.hub = Hub(self.bus)
        self.memoire = Episodique()
        self.sommeil = Sommeil()
        self.prototypes = {}

    def percevoir(self, texte: str, jeu: str, contexte=None, langue: str = "?"):
        code = self.hub.percevoir(texte, jeu, contexte)
        if code is not None:
            self.memoire.stocker(texte, code, langue)
        return code

    def percevoir_item(self, it):
        """Perçoit un `ItemType` en portant son **contexte RSN** (pas son résumé).

        `ItemType.contexte` est une chaîne (`resume_contexte`) ; le codec attend
        un `RSN` avec `.corps`. Passer la chaîne faisait échouer la lecture en
        silence, et le pipeline ne stockait rien.
        """
        ctx = getattr(it, "contexte_rsn", None)
        if ctx is None and not isinstance(getattr(it, "contexte", None), str):
            ctx = getattr(it, "contexte", None)
        return self.percevoir(it.texte, it.jeu, ctx)

    def consolider(self):
        self.prototypes = self.sommeil.consolider(self.memoire.episodes)
        self.bus.publier("prototypes", len(self.prototypes), self.nom)
        return self.prototypes

    def repondre(self, cue: dict):
        r = self.memoire.completion(cue)
        if r.get("exact"):
            return "memoire", r
        proto = self.prototypes.get((cue.get("jeu"), cue.get("action")))
        if proto:
            # Hybride : garder le candidat qui explique le mieux les champs **observés**
            # (le champ masqué ne sert jamais à choisir, seulement à évaluer).
            code_m4 = r.get("code")
            observes = [k for k, v in cue.items() if v is not None]
            m4_ok = sum(1 for k in observes if code_m4 and code_m4.get(k) == cue.get(k))
            p_ok = sum(1 for k in observes if proto.get(k) == cue.get(k))
            if code_m4 is not None and m4_ok > p_ok:
                return "memoire-partiel", r
            champs = sum(1 for k, v in cue.items() if proto.get(k) == v and v is not None)
            return "prototype", {"champs": champs, "code": proto}
        return "vide", r

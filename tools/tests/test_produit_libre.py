#!/usr/bin/env python3
"""test_produit_libre.py — non-régression sur les **50 textes libres** de l'audit A26.

Ce que le test fige :
- la vue **`filtrer`** ne produit **aucun** chevauchement de syntagmes (0/50) ;
- la vue **`alternative`** (défaut) documente les chevauchements dans `meta.alternative` ;
- les **5 textes non linguistiques** (emoji, vide, espaces, ponctuation, nombre nu) n'ont
  **aucun** syntagme ;
- l'analyse est **déterministe** (deux passes identiques).
"""
from __future__ import annotations

import json
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
NON_LINGUISTIQUES = {"f14", "f15", "f16", "f17", "f18"}


def _textes() -> list[tuple[str, str]]:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    return [(item["id"], item["texte"]) for item in donnees["banc_50"]["resultats"]]


def _segments(annotation) -> list:
    return [e for e in annotation.etiquettes if e.niveau == "syntagme"]


def _chevauchements(segments: list) -> int:
    return sum(1 for i, a in enumerate(segments) for b in segments[i + 1:]
               if max(a.debut, b.debut) < min(a.fin, b.fin))


class TestProduitLibre(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tools.bloc_linguistique as bl
        cls.bl = bl
        cls.textes = _textes()

    def test_filtrer_sans_chevauchement(self):
        h = self.bl.Heuristique(partition="filtrer")
        total = sum(_chevauchements(_segments(h.analyser(t, "fr"))) for _, t in self.textes)
        self.assertEqual(total, 0)

    def test_alternative_etiquettes(self):
        h = self.bl.Heuristique(partition="alternative")
        etiquetes = sum(
            1 for _, t in self.textes
            for e in _segments(h.analyser(t, "fr"))
            if "alternative" in (e.meta or {})
        )
        self.assertGreater(etiquetes, 0)

    def test_non_linguistiques_sans_syntagme(self):
        h = self.bl.Heuristique(partition="filtrer")
        for ident, texte in self.textes:
            if ident in NON_LINGUISTIQUES:
                self.assertEqual(_segments(h.analyser(texte, "fr")), [], ident)

    def test_deterministe(self):
        h = self.bl.Heuristique(partition="filtrer")
        texte = "Le chat de la voisine qui dort sur le toit se réveille."
        a = h.analyser(texte, "fr").json()
        b = h.analyser(texte, "fr").json()
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)

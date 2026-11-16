"""test_verifier_performance_fix.py — le comparateur du contrôle négatif de U1.

Le comparateur ne mesure rien : il vérifie que deux répertoires d'annotations canoniques
sont identiques ou non. Ces tests couvrent le vert (même contenu) et le rouge (un octet
différent), sans rejouer les 10 000 mots.

    python3 tools/tests/test_verifier_performance_fix.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]


def _charger():
    spec = importlib.util.spec_from_file_location(
        "verifier_performance_fix_test", RACINE / "tools" / "verifier_performance_fix.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


verificateur = _charger()


class TestComparateur(unittest.TestCase):
    def _ecrire(self, racine: pathlib.Path, suffixe: str = "") -> None:
        for nom in verificateur.FICHIERS:
            (racine / nom).write_text("annotation" + suffixe + nom, encoding="utf-8")

    def test_identique(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            self._ecrire(pathlib.Path(a))
            self._ecrire(pathlib.Path(b))
            self.assertEqual(verificateur.comparer(pathlib.Path(a), pathlib.Path(b)), 0)

    def test_un_octet_different(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            self._ecrire(pathlib.Path(a))
            self._ecrire(pathlib.Path(b))
            nom = verificateur.FICHIERS[-1]
            (pathlib.Path(b) / nom).write_text("autre", encoding="utf-8")
            self.assertEqual(verificateur.comparer(pathlib.Path(a), pathlib.Path(b)), 1)

    def test_fichier_manquant(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            self._ecrire(pathlib.Path(a))
            self.assertEqual(verificateur.comparer(pathlib.Path(a), pathlib.Path(b)), 2)


if __name__ == "__main__":
    unittest.main()

"""Tests de la mesure DeepSeek : chrF, coût, plancher."""
from __future__ import annotations

import json
import pathlib
import tempfile
import unittest

from llm.mesure import chrf, mesure


class TestMesure(unittest.TestCase):
    def test_chrf(self):
        self.assertEqual(chrf("abc", "abc"), 100.0)
        self.assertLess(chrf("abc", "xyz"), 100.0)
        self.assertEqual(chrf("", "abc"), 0.0)

    def test_mesure_et_plancher(self):
        d = tempfile.mkdtemp()
        chemin = pathlib.Path(d) / "prof.jsonl"
        lignes = [
            {"id": "t1", "dry_run": False, "reponse": "Le roi est la pièce la plus importante.",
             "prompt": "Traduis.\n\nThe king is the most important piece.",
             "usage": {"prompt_tokens": 10, "completion_tokens": 8},
             "latence_s": 0.5, "cache": False, "modele": "deepseek-chat",
             "meta": {"categorie": "traduction", "cible_iso3": "fra",
                      "reference": "Le roi est la pièce la plus importante."}},
            {"id": "j1", "dry_run": False, "reponse": "Une réponse de jeu.",
             "prompt": "Explique le ko.", "usage": {"prompt_tokens": 3,
                                                    "completion_tokens": 2},
             "latence_s": 0.2, "cache": True, "modele": "deepseek-chat",
             "meta": {"categorie": "jeu"}},
            {"id": "dry", "dry_run": True, "reponse": "faux", "prompt": "x",
             "meta": {"categorie": "traduction"}},
        ]
        chemin.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in lignes),
                          encoding="utf-8")
        r = mesure(chemin)
        self.assertEqual(r["exemples"], 2)
        self.assertEqual(r["traductions"], 1)
        self.assertEqual(r["jeux"], 1)
        self.assertEqual(r["chrF_moyen"], 100.0)
        self.assertLess(r["chrF_plancher"], 100.0)
        self.assertEqual(r["tokens_entree"], 13)
        self.assertEqual(r["tokens_sortie"], 10)
        self.assertEqual(r["caches"], 1)


if __name__ == "__main__":
    unittest.main()

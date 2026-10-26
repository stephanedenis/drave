"""Tests du corpus professeur et de la distillation, sans réseau."""
from __future__ import annotations

import json
import pathlib
import tempfile
import unittest

from llm.deepseek import DeepSeek
from llm.distillation import construire, lire_enseignant
from llm.enseignant import charger_prompts, generer


def _client(tmp: str):
    def transport(url, entetes, corps, timeout):
        return {"model": "deepseek-chat",
                "choices": [{"message": {"content": "réponse du professeur"}}],
                "usage": {"prompt_tokens": 12, "completion_tokens": 4,
                          "total_tokens": 16}}
    return DeepSeek(cle="test-key", transport=transport, cache_dir=tmp)


class TestEnseignant(unittest.TestCase):
    def test_prompts_publics(self):
        fic = pathlib.Path(__file__).parents[1] / "prompts_publics.jsonl"
        prompts = charger_prompts(fic)
        self.assertEqual(len(prompts), 60)
        self.assertEqual(sum(1 for p in prompts if p["meta"]["categorie"] == "traduction"), 50)
        self.assertEqual(sum(1 for p in prompts if p["meta"]["categorie"] == "jeu"), 10)
        for p in prompts:
            self.assertIn("id", p)
            self.assertIn("prompt", p)
            self.assertIn("system", p)

    def test_generation_et_reprise(self):
        d = tempfile.mkdtemp()
        sortie = pathlib.Path(d) / "enseignant.jsonl"
        prompts = charger_prompts(pathlib.Path(__file__).parents[1] / "prompts_publics.jsonl")[:3]
        stats = generer(prompts, sortie, _client(tempfile.mkdtemp()))
        self.assertEqual(stats["reussies"], 3)
        self.assertEqual(len(sortie.read_text(encoding="utf-8").splitlines()), 3)
        # une seconde passe ne redemande rien
        stats2 = generer(prompts, sortie, _client(tempfile.mkdtemp()))
        self.assertEqual(stats2["demandes"], 0)
        self.assertEqual(len(sortie.read_text(encoding="utf-8").splitlines()), 3)

    def test_dry_run_ecrit_mais_est_ignore(self):
        d = tempfile.mkdtemp()
        sortie = pathlib.Path(d) / "dry.jsonl"
        prompts = charger_prompts(pathlib.Path(__file__).parents[1] / "prompts_publics.jsonl")[:2]
        generer(prompts, sortie, DeepSeek(cle=""), dry_run=True)
        self.assertEqual(len(lire_enseignant(sortie)), 0)


class TestDistillation(unittest.TestCase):
    def _ecrire(self, chemin, n=10):
        lignes = []
        for i in range(n):
            lignes.append({"id": f"ex-{i}", "system": "sys", "prompt": f"question {i}",
                           "reponse": f"réponse {i}", "dry_run": False,
                           "modele": "deepseek-chat"})
        lignes.append({"id": "dry", "system": "sys", "prompt": "q", "reponse": "faux",
                       "dry_run": True, "modele": "deepseek-chat"})
        pathlib.Path(chemin).write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in lignes),
            encoding="utf-8")

    def test_decoupage(self):
        d = tempfile.mkdtemp()
        entree = pathlib.Path(d) / "prof.jsonl"
        self._ecrire(entree)
        meta = construire(entree, pathlib.Path(d) / "dist")
        self.assertEqual(meta["exemples"], 10)
        self.assertGreaterEqual(meta["val"], 1)
        self.assertEqual(meta["train"] + meta["val"], 10)
        train = (pathlib.Path(d) / "dist" / "train.txt").read_text(encoding="utf-8")
        val = (pathlib.Path(d) / "dist" / "val.txt").read_text(encoding="utf-8")
        self.assertIn("réponse 0", train + val)
        self.assertNotIn("faux", train + val)
        self.assertIn("source_sha256", meta)

    def test_reponse_seule(self):
        d = tempfile.mkdtemp()
        entree = pathlib.Path(d) / "prof.jsonl"
        self._ecrire(entree)
        construire(entree, pathlib.Path(d) / "dist", reponse_seule=True)
        train = (pathlib.Path(d) / "dist" / "train.txt").read_text(encoding="utf-8")
        self.assertIn("### professeur", train)
        self.assertNotIn("### user", train)


if __name__ == "__main__":
    unittest.main()

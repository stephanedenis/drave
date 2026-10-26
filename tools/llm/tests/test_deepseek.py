"""Tests du banc DeepSeek, sans réseau et sans clé réelle."""
from __future__ import annotations

import json
import os
import pathlib
import tempfile
import unittest
from unittest.mock import patch

from llm.deepseek import DeepSeek, ErreurDeepSeek, _cle_env


def _reponse(contenu="bonjour", modele="deepseek-chat",
             raisonnement=None, usage=None):
    return {
        "model": modele,
        "choices": [{"message": {"content": contenu,
                                 "reasoning_content": raisonnement}}],
        "usage": usage or {"prompt_tokens": 10, "completion_tokens": 3,
                           "total_tokens": 13},
    }


class TestDeepSeek(unittest.TestCase):
    def test_dry_run_sans_cle(self):
        c = DeepSeek(cle="")
        r = c.demande("test", dry_run=True)
        self.assertIn("[dry-run]", r.contenu)
        self.assertFalse(r.cache)

    def test_cle_absente(self):
        c = DeepSeek(cle="")
        with self.assertRaises(ErreurDeepSeek) as ctx:
            c.demande("test")
        self.assertIn("clé absente", str(ctx.exception))

    def test_requete_et_parse(self):
        vues = {}

        def transport(url, entetes, corps, timeout):
            vues["url"] = url
            vues["entetes"] = entetes
            vues["corps"] = json.loads(corps)
            return _reponse("la réponse", usage={"prompt_tokens": 7,
                                                 "completion_tokens": 2,
                                                 "total_tokens": 9})

        c = DeepSeek(cle="test-key", transport=transport, cache_dir=tempfile.mkdtemp())
        r = c.demande("salut", system="tu es un maître", temperature=0.2,
                      max_tokens=64)
        self.assertEqual(r.contenu, "la réponse")
        self.assertEqual(r.usage["total_tokens"], 9)
        self.assertFalse(r.cache)
        self.assertTrue(vues["url"].endswith("/chat/completions"))
        self.assertEqual(vues["entetes"]["Authorization"], "Bearer test-key")
        self.assertEqual(vues["corps"]["model"], "deepseek-chat")
        self.assertEqual(vues["corps"]["messages"][0]["role"], "system")
        self.assertEqual(vues["corps"]["messages"][1]["content"], "salut")
        self.assertEqual(vues["corps"]["temperature"], 0.2)
        self.assertEqual(vues["corps"]["max_tokens"], 64)

    def test_cache_evite_le_second_appel(self):
        appels = []

        def transport(url, entetes, corps, timeout):
            appels.append(1)
            return _reponse("en cache")

        dossier = tempfile.mkdtemp()
        c = DeepSeek(cle="test-key", transport=transport, cache_dir=dossier)
        a = c.demande("même prompt")
        b = c.demande("même prompt")
        self.assertEqual(a.contenu, b.contenu)
        self.assertEqual(len(appels), 1)
        self.assertTrue(b.cache)
        fichiers = list(pathlib.Path(dossier).glob("*.json"))
        self.assertEqual(len(fichiers), 1)
        self.assertNotIn("test-key", fichiers[0].read_text(encoding="utf-8"))

    def test_prompts_differents_deux_appels(self):
        appels = []

        def transport(url, entetes, corps, timeout):
            appels.append(1)
            return _reponse("ok")

        c = DeepSeek(cle="test-key", transport=transport, cache_dir=tempfile.mkdtemp())
        c.demande("a")
        c.demande("b")
        self.assertEqual(len(appels), 2)

    def test_retry_sur_429(self):
        appels = []
        dormis = []

        def transport(url, entetes, corps, timeout):
            appels.append(1)
            if len(appels) == 1:
                raise ErreurDeepSeek("HTTP 429", code=429, reessayable=True)
            return _reponse("après retry")

        c = DeepSeek(cle="test-key", transport=transport, cache_dir=tempfile.mkdtemp(),
                     sleep=lambda s: dormis.append(s))
        r = c.demande("retry")
        self.assertEqual(r.contenu, "après retry")
        self.assertEqual(len(appels), 2)
        self.assertEqual(dormis, [1])

    def test_pas_de_retry_sur_401(self):
        appels = []

        def transport(url, entetes, corps, timeout):
            appels.append(1)
            raise ErreurDeepSeek("HTTP 401", code=401, reessayable=False)

        c = DeepSeek(cle="test-key", transport=transport, cache_dir=tempfile.mkdtemp())
        with self.assertRaises(ErreurDeepSeek):
            c.demande("non")
        self.assertEqual(len(appels), 1)

    def test_cle_dans_un_fichier(self):
        d = tempfile.mkdtemp()
        f = pathlib.Path(d) / "deepseek.key"
        f.write_text("cle-fichier\n", encoding="utf-8")
        with patch.dict(os.environ, {"DEEPSEEK_KEY_FILE": str(f),
                                     "DEEPSEEK_API_KEY": "",
                                     "DSH_API_KEY": ""}, clear=False):
            self.assertEqual(_cle_env(), "cle-fichier")

    def test_raisonnement_et_usage(self):
        def transport(url, entetes, corps, timeout):
            return _reponse("fini", raisonnement="j'ai réfléchi",
                            usage={"prompt_tokens": 1, "completion_tokens": 2,
                                   "total_tokens": 3})
        c = DeepSeek(cle="test-key", transport=transport, cache_dir=tempfile.mkdtemp())
        r = c.demande("p")
        self.assertEqual(r.raisonnement, "j'ai réfléchi")
        self.assertEqual(r.usage["total_tokens"], 3)


if __name__ == "__main__":
    unittest.main()

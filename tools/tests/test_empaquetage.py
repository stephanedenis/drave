#!/usr/bin/env python3
"""test_empaquetage.py — le paquet `drave` et ses deux entrées.

Ce que le test fige :

- `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,
  **aucune dépendance**, script console `drave = tools.drave:main` ;
- le **chemin historique** `python3 tools/drave.py` rend la même version et analyse ;
- l'entrée `tools.drave:main` est **importable depuis un autre répertoire** (c'est ce que
  l'installation éditable met sur `sys.path`) ;
- **sans installation**, `drave` échoue **proprement** : code 127, « command not found »,
  pas de trace Python.

Le test ne crée pas de venv et ne télécharge rien : la vérification complète
`python3 -m pip install -e .` dans `/tmp/venv-drave` est consignée dans
`reports/rapport-empaquetage.md` et `reports/empaquetage.json`.
"""
from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
PYPROJECT = RACINE / "pyproject.toml"
VERSION = "drave 0.1.0"

try:  # Python 3.11+ ; le paquet doit seulement tourner en 3.10, le test peut se sauter.
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - dépend de l'interpréteur
    tomllib = None  # type: ignore[assignment]


def _lire_pyproject() -> dict:
    if tomllib is None:
        raise unittest.SkipTest("tomllib absent (Python < 3.11) : métadonnées non lues")
    with PYPROJECT.open("rb") as flux:
        return tomllib.load(flux)


def _executer(cmd: list[str], cwd: pathlib.Path, env: dict | None = None,
              timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True,
                          timeout=timeout)


class TestMetadonnees(unittest.TestCase):
    def test_pyproject_existe(self):
        self.assertTrue(PYPROJECT.is_file(), PYPROJECT)

    def test_identite_et_python(self):
        project = _lire_pyproject()["project"]
        self.assertEqual(project["name"], "drave")
        self.assertEqual(project["version"], "0.1.0")
        self.assertEqual(project["requires-python"], ">=3.10")

    def test_aucune_dependance(self):
        project = _lire_pyproject()["project"]
        self.assertEqual(project.get("dependencies", []), [])
        self.assertNotIn("optional-dependencies", project)
        build = _lire_pyproject()["build-system"]
        # Le backend est une dépendance de *construction*, pas d'exécution.
        self.assertEqual(build["build-backend"], "setuptools.build_meta")

    def test_script_console(self):
        project = _lire_pyproject()["project"]
        self.assertEqual(project["scripts"]["drave"], "tools.drave:main")


class TestEntreeHistorique(unittest.TestCase):
    def test_version(self):
        r = _executer([sys.executable, "tools/drave.py", "--version"], RACINE)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), VERSION)

    def test_analyser(self):
        r = _executer([sys.executable, "tools/drave.py", "analyser", "Le chat dort."],
                      RACINE)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("GN", r.stdout)
        self.assertIn("Le chat", r.stdout)


class TestEntreeInstallable(unittest.TestCase):
    def test_import_depuis_un_autre_repertoire(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ)
            env["PYTHONPATH"] = str(RACINE)
            env.pop("VIRTUAL_ENV", None)
            r = _executer(
                [sys.executable, "-c",
                 "from tools.drave import main; main(['--version'])"],
                pathlib.Path(tmp), env=env,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout.strip(), VERSION)


class TestControleNegatif(unittest.TestCase):
    def test_sans_installation_echec_propre(self):
        """PATH vide : le nom `drave` n'est pas résolu, et l'échec est lisible."""
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ)
            env["PATH"] = tmp  # aucun binaire, donc aucun `drave`
            for cle in ("PYTHONPATH", "VIRTUAL_ENV", "PYTHONHOME", "BASH_ENV", "ENV"):
                env.pop(cle, None)
            bash = shutil.which("bash") or "/bin/bash"
            r = _executer([bash, "-c", "drave --version"], pathlib.Path(tmp), env=env)
            self.assertEqual(r.returncode, 127, (r.stdout, r.stderr))
            self.assertIn("command not found", r.stderr.lower())
            self.assertNotIn("traceback", r.stderr.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)

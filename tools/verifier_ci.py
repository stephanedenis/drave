#!/usr/bin/env python3
"""verifier_ci.py — vérifier le workflow CI **sans `act`** : YAML, commandes, contrôle négatif.

POURQUOI CET OUTIL EXISTE. Le workflow `.github/workflows/ci.yml` n'est exécuté que par
GitHub Actions. Quand `act` n'est pas installé, il reste trois preuves possibles en local :

1. **le YAML est valide** : un parseur (PyYAML) le charge, et le contrat attendu est là
   (matrice 3.10/3.13, `pip install -e .`, les cinq commandes, `runs-on`) ;
2. **les commandes qu'il lance passent** : chaque `run` est exécuté dans l'ordre, avec
   l'interpréteur courant (ou `--python`), et son code de sortie est relevé ;
3. **le contrôle négatif** : un test volontairement cassé, copié depuis
   `tools/tests/test_produit.py`, doit sortir en **1** et **arrêter la séquence** — c'est
   exactement ce que fait un job GitHub Actions quand une étape échoue.

Il vérifie aussi que la **copie de secours de S** (`.github/ci/structures/`) est identique au
sous-module quand celui-ci est présent : un run GitHub sans sous-module utiliserait sinon une
version différente du générateur.

L'outil ne remplace pas `act` : il ne simule ni l'image du runner, ni `actions/checkout`,
ni `actions/setup-python`. Il prouve le YAML et les commandes, pas l'exécution GitHub.

Usage :
    python3 tools/verifier_ci.py                  # YAML + commandes + négatif
    python3 tools/verifier_ci.py --json           # le même résultat en JSON
    python3 tools/verifier_ci.py --sans-porte     # saute la porte (plus rapide)
    python3 tools/verifier_ci.py --python /tmp/ci310/bin/python3

Codes de sortie : 0 tout est vert · 1 un contrôle a échoué · 2 YAML illisible ou PyYAML absent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

RACINE = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = RACINE / ".github" / "workflows" / "ci.yml"
COMMANDES_ATTENDUES = (
    "pip install -e .",
    "python3 tools/tests/test_produit.py",
    "python3 tools/tests/test_tagger_api.py",
    "bash tools/porte-produit.sh",
    "python3 tools/tests/test_schema_produit.py",
)
MATRICE_ATTENDUE = ["3.10", "3.13"]


def _sortir_erreur(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(2)


def charger_yaml(chemin: pathlib.Path) -> tuple[dict, str]:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover — l'environnement de mesure l'a
        _sortir_erreur(f"PyYAML absent : {exc}. Installer pyyaml pour vérifier le workflow.")
    try:
        donnees = yaml.safe_load(chemin.read_text(encoding="utf-8"))
    except Exception as exc:
        _sortir_erreur(f"YAML invalide : {chemin} : {exc}")
    if not isinstance(donnees, dict):
        _sortir_erreur(f"YAML invalide : la racine n'est pas un mapping : {type(donnees).__name__}")
    return donnees, getattr(yaml, "__version__", "?")


def _declencheurs(donnees: dict) -> bool:
    # PyYAML 1.1 lit `on:` comme le booléen True. Le workflow le cite (`"on":`), on
    # accepte les deux formes pour ne pas dépendre d'un détail du parseur.
    return "on" in donnees or True in donnees


def controler(donnees: dict) -> dict:
    """Le contrat du workflow : matrice, étapes, commandes exactes."""
    job = (donnees.get("jobs") or {}).get("produit")
    if not isinstance(job, dict):
        _sortir_erreur("YAML invalide : `jobs.produit` est absent")
    strategie = job.get("strategy") or {}
    matrice = (strategie.get("matrix") or {}).get("python")
    if matrice != MATRICE_ATTENDUE:
        _sortir_erreur(f"matrice inattendue : {matrice!r} (attendu {MATRICE_ATTENDUE!r})")
    etapes = job.get("steps") or []
    runs = [str(etape.get("run", "")).strip() for etape in etapes]
    manquantes = [commande for commande in COMMANDES_ATTENDUES if commande not in runs]
    if manquantes:
        _sortir_erreur(f"commandes absentes du workflow : {manquantes}")
    if job.get("runs-on") != "ubuntu-latest":
        _sortir_erreur(f"runs-on inattendu : {job.get('runs-on')!r}")
    if not _declencheurs(donnees):
        _sortir_erreur("YAML invalide : aucun déclencheur `on`")
    return {
        "matrice": matrice,
        "runs_on": job["runs-on"],
        "etapes": [nom for nom in runs if nom],
        "commandes_attendues": list(COMMANDES_ATTENDUES),
    }


def _python_et_pip(python: str | None) -> tuple[str, list[str]]:
    python = python or shutil.which("python3") or sys.executable
    pip = shutil.which("pip")
    return python, [pip] if pip else [python, "-m", "pip"]


def _argv(commande: str, python: str, pip: list[str]) -> list[str]:
    mots = shlex.split(commande)
    if mots and mots[0] == "python3":
        mots[0] = python
    elif mots and mots[0] == "pip":
        mots = [*pip, *mots[1:]]
    return mots


def _resume(texte: str, limite: int = 800) -> str:
    texte = texte.strip()
    return texte if len(texte) <= limite else "…" + texte[-limite:]


def _executer(etapes: list[tuple[str, str]], python: str, pip: list[str],
              timeout: int) -> list[dict]:
    """Exécute les étapes en **fail-fast** : la première non nulle arrête le job."""
    resultats: list[dict] = []
    env = dict(os.environ)
    env["PATH"] = str(pathlib.Path(python).parent) + os.pathsep + env.get("PATH", "")
    for nom, commande in etapes:
        argv = _argv(commande, python, pip)
        debut = time.monotonic()
        try:
            r = subprocess.run(
                argv, cwd=str(RACINE), capture_output=True, text=True,
                encoding="utf-8", timeout=timeout, env=env,
            )
            code, sortie, erreur = r.returncode, r.stdout or "", r.stderr or ""
            expire = False
        except subprocess.TimeoutExpired as exc:
            code = 124
            sortie = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
            erreur = f"timeout après {timeout} s"
            expire = True
        resultats.append({
            "etape": nom,
            "commande": commande,
            "argv": argv,
            "code": code,
            "duree_s": round(time.monotonic() - debut, 3),
            "timeout": expire,
            "stdout": _resume(sortie),
            "stderr": _resume(erreur),
        })
        if code != 0:
            break
    return resultats


def restaurer_secours() -> dict:
    """Reproduit l'étape CI : restaurer S depuis `.github/ci/structures` s'il manque."""
    cible = RACINE / "tools" / "structures" / "generateur.py"
    if cible.is_file():
        return {"fait": False, "raison": "sous-module tools/structures présent"}
    paires = (
        (".github/ci/structures/generateur.py", "tools/structures/generateur.py"),
        (".github/ci/structures/donnees/gold-analyseur.json",
         "tools/structures/donnees/gold-analyseur.json"),
    )
    for source, destination in paires:
        (RACINE / destination).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(RACINE / source, RACINE / destination)
    return {"fait": True, "fichiers": [destination for _, destination in paires]}


def verifier_secours() -> dict:
    """La copie CI de S est-elle identique au sous-module présent ?"""
    paires = (
        ("tools/structures/generateur.py", ".github/ci/structures/generateur.py"),
        ("tools/structures/donnees/gold-analyseur.json",
         ".github/ci/structures/donnees/gold-analyseur.json"),
    )
    if not all((RACINE / source).is_file() for source, _ in paires):
        return {"code": 2, "identique": None,
                "raison": "sous-module absent : la copie de secours est la seule source"}
    details = []
    for source, secours in paires:
        a = hashlib.sha256((RACINE / source).read_bytes()).hexdigest()
        b = hashlib.sha256((RACINE / secours).read_bytes()).hexdigest()
        details.append({"source": source, "secours": secours,
                        "sha256_source": a, "sha256_secours": b, "identique": a == b})
    identique = all(d["identique"] for d in details)
    return {"code": 0 if identique else 1, "identique": identique, "fichiers": details}


def controle_negatif(python: str, pip: list[str], timeout: int) -> dict:
    """Un test cassé doit faire échouer la commande **et** arrêter les suivantes."""
    source = (RACINE / "tools" / "tests" / "test_produit.py").read_text(encoding="utf-8")
    avant_main = source.split('\nif __name__ == "__main__":', 1)[0]
    casse = avant_main + '''
class TestControleNegatifCI(unittest.TestCase):
    """Le test volontairement cassé : il doit sortir en 1, jamais en 0."""

    def test_echec_volontaire(self) -> None:
        self.fail("contrôle négatif CI volontaire")


if __name__ == "__main__":
    unittest.main()
'''
    fd, chemin = tempfile.mkstemp(prefix="_controle_negatif_ci_", suffix=".py",
                                  dir=str(RACINE / "tools" / "tests"))
    chemin = pathlib.Path(chemin)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as flux:
            flux.write(casse)
        relatif = chemin.relative_to(RACINE).as_posix()
        etapes = [
            ("test_casse", f"python3 {relatif}"),
            ("temoin_apres", "python3 tools/tests/test_schema_produit.py"),
        ]
        resultats = _executer(etapes, python, pip, timeout)
    finally:
        chemin.unlink(missing_ok=True)
    premier = resultats[0]
    echec = premier["code"] != 0
    arret = len(resultats) == 1
    return {
        "fichier_temporaire": relatif,
        "code": premier["code"],
        "casse": echec,
        "job_echoue": echec and arret,
        "etape_suivante_executee": len(resultats) > 1,
        "sortie": premier["stdout"] + premier["stderr"],
        "resultats": resultats,
    }


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(description="Vérifie le workflow CI sans act.")
    parseur.add_argument("--workflow", type=pathlib.Path, default=WORKFLOW)
    parseur.add_argument("--python", help="interpréteur à utiliser à la place de python3")
    parseur.add_argument("--sans-porte", action="store_true", help="saute `porte-produit.sh`")
    parseur.add_argument("--timeout", type=int, default=900, help="timeout par étape (s)")
    parseur.add_argument("--json", action="store_true", help="sortie JSON")
    parseur.add_argument("--sortie", type=pathlib.Path, help="écrit le JSON dans ce fichier")
    args = parseur.parse_args(argv)

    workflow = args.workflow if args.workflow.is_absolute() else RACINE / args.workflow
    donnees, version_yaml = charger_yaml(workflow)
    contrat = controler(donnees)
    python, pip = _python_et_pip(args.python)

    restauration = restaurer_secours()
    negatif = controle_negatif(python, pip, min(args.timeout, 300))
    secours = verifier_secours()
    etapes = [("installer", "pip install -e ."),
              ("test_produit", "python3 tools/tests/test_produit.py"),
              ("test_tagger_api", "python3 tools/tests/test_tagger_api.py"),
              ("porte_produit", "bash tools/porte-produit.sh"),
              ("test_schema_produit", "python3 tools/tests/test_schema_produit.py")]
    if args.sans_porte:
        etapes = [etape for etape in etapes if etape[0] != "porte_produit"]
    execution = _executer(etapes, python, pip, args.timeout)

    ok = (negatif["job_echoue"]
          and secours["code"] != 1
          and len(execution) == len(etapes)
          and all(etape["code"] == 0 for etape in execution))
    resultat = {
        "ok": ok,
        "workflow": str(workflow.relative_to(RACINE)) if workflow.is_relative_to(RACINE) else str(workflow),
        "act": shutil.which("act"),
        "python": python,
        "python_version": subprocess.run(
            [python, "--version"], capture_output=True, text=True).stdout.strip(),
        "pip": pip,
        "yaml": {"valide": True, "parseur": f"PyYAML {version_yaml}"},
        "contrat": contrat,
        "restauration": restauration,
        "secours_s": secours,
        "execution": execution,
        "negatif": negatif,
    }
    if args.sortie:
        args.sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    if args.json:
        sys.stdout.write(json.dumps(resultat, ensure_ascii=False, indent=2) + "\n")
    else:
        print(f"YAML valide · {resultat['yaml']['parseur']} · matrice {contrat['matrice']}")
        print(f"{resultat['python_version']} · act={resultat['act'] or 'absent'}")
        if restauration["fait"]:
            print("  ✅ sous-module S restauré depuis .github/ci/structures")
        for etape in execution:
            marque = "✅" if etape["code"] == 0 else "❌"
            print(f"  {marque} {etape['etape']:<20} code={etape['code']} · {etape['duree_s']} s")
        marque = "✅" if negatif["job_echoue"] else "❌"
        print(f"  {marque} contrôle négatif  code={negatif['code']} · "
              f"job_echoue={negatif['job_echoue']} · "
              f"étape suivante exécutée={negatif['etape_suivante_executee']}")
        marque = "✅" if secours["code"] != 1 else "❌"
        etat = ("identique" if secours["code"] == 0 else
                "sous-module absent" if secours["code"] == 2 else "dérive")
        print(f"  {marque} copie de secours S  {etat}")
        print("✅ CI locale verte" if ok else "❌ CI locale rouge")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

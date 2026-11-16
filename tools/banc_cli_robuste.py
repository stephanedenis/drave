#!/usr/bin/env python3
"""banc_cli_robuste.py — rejoue les cas de robustesse du CLI `drave` (T5).

Ce que le banc mesure, sans réseau et sans clé :

1. `--duree` : la durée est **absente** du JSON par défaut, **présente** dans `cout.duree_s`
   avec le drapeau, et c'est le **seul** ajout (texte et étiquettes identiques) ; idem pour
   chaque ligne de `--jsonl` ;
2. le **tableau des codes** est écrit dans `--aide` (0, 3, 4, 5) et la notice ;
3. `--aide` et `--help` sortent **0** sur les **quatre** sous-commandes ;
4. `--fichier` sur un chemin **inexistant** (4) et sur un **répertoire** (5) : message clair,
   `stdout` vide, **aucune trace** Python.

Le **contrôle négatif** est explicite : sans `--duree`, `duree_s` doit être absent ; une option
fantôme (`--sortie`) doit sortir 5 et non 0.

Usage :
    python3 tools/banc_cli_robuste.py            # résumé lisible, code 0/1
    python3 tools/banc_cli_robuste.py --json     # le JSON de reports/cli-robuste.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile

RACINE = pathlib.Path(__file__).resolve().parents[1]
CLI = RACINE / "tools" / "drave.py"
DATE = "2026-11-15"
COMMANDES = ("analyser", "evaluer", "rejouer", "restituer")


def _commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=RACINE, text=True,
                              capture_output=True, timeout=10).stdout.strip() or "inconnu"
    except (OSError, subprocess.SubprocessError):
        return "inconnu"


def _run(*arguments: str, env: dict | None = None) -> dict:
    resultat = subprocess.run(
        [sys.executable, str(CLI), *arguments], cwd=str(RACINE), text=True,
        encoding="utf-8", errors="replace", capture_output=True, timeout=120, env=env,
    )
    return {
        "commande": "drave " + " ".join(arguments),
        "code": resultat.returncode,
        "stdout": resultat.stdout,
        "stderr": resultat.stderr,
        "trace": "Traceback" in resultat.stdout or "Traceback" in resultat.stderr,
    }


def _sans_cle() -> dict:
    """Un environnement sans aucune clé DeepSeek, pour mesurer le code 4 sans réseau."""
    import os
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("DEEPSEEK", "DSH_"))}
    env["HOME"] = tempfile.mkdtemp(prefix="drave-t5-home-")
    return env


def _cas_duree() -> dict:
    sans = _run("analyser", "Le chat dort.", "--json")
    avec = _run("analyser", "Le chat dort.", "--json", "--duree")
    d_sans = json.loads(sans["stdout"]) if sans["code"] == 0 else {}
    d_avec = json.loads(avec["stdout"]) if avec["code"] == 0 else {}
    duree = d_avec.get("cout", {}).get("duree_s")
    ok = (
        sans["code"] == 0 and avec["code"] == 0
        and "duree_s" not in d_sans.get("cout", {})
        and isinstance(duree, (int, float)) and duree >= 0
        and d_sans.get("texte") == d_avec.get("texte")
        and d_sans.get("etiquettes") == d_avec.get("etiquettes")
    )
    return {
        "cas": "duree_json",
        "ok": ok,
        "code_sans": sans["code"],
        "code_avec": avec["code"],
        "duree_s_sans": d_sans.get("cout", {}).get("duree_s"),
        "duree_s_avec": duree,
        "seul_ajout": (d_sans.get("texte") == d_avec.get("texte")
                       and d_sans.get("etiquettes") == d_avec.get("etiquettes")),
        "controle_negatif": {
            "nom": "sans --duree, la duree est absente",
            "verifie": "duree_s" not in d_sans.get("cout", {}),
        },
    }


def _cas_duree_jsonl() -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as f:
        f.write("Le chat dort.\n\nLa voisine parle.\n")
        chemin = f.name
    try:
        sortie = _run("analyser", "--fichier", chemin, "--jsonl", "--duree")
        lignes = [json.loads(l) for l in sortie["stdout"].splitlines() if l.strip()]
        ok = (sortie["code"] == 0 and len(lignes) == 2
              and all(isinstance(l["cout"].get("duree_s"), (int, float)) for l in lignes))
        return {"cas": "duree_jsonl", "ok": ok, "code": sortie["code"],
                "lignes": len(lignes),
                "durees_s": [l["cout"].get("duree_s") for l in lignes]}
    finally:
        pathlib.Path(chemin).unlink(missing_ok=True)


def _cas_aide() -> list[dict]:
    cas = []
    globale = _run("--aide")
    attendus = ("Codes de sortie", "0 succès", "3 refus", "4 clé/dépendance", "5 usage")
    cas.append({
        "cas": "aide_globale",
        "ok": globale["code"] == 0 and all(a in globale["stdout"] for a in attendus),
        "code": globale["code"],
        "tableau_des_codes": all(a in globale["stdout"] for a in attendus),
    })
    for commande in COMMANDES:
        for drapeau in ("--aide", "--help"):
            sortie = _run(commande, drapeau)
            cas.append({
                "cas": f"{commande}_{drapeau.lstrip('-')}",
                "ok": (sortie["code"] == 0 and "usage:" in sortie["stdout"]
                       and commande in sortie["stdout"]),
                "code": sortie["code"],
            })
    return cas


def _cas_entrees() -> list[dict]:
    cas = []
    with tempfile.TemporaryDirectory(prefix="drave-t5-") as dossier:
        absent = pathlib.Path(dossier) / "absent.txt"
        sortie = _run("analyser", "--fichier", str(absent))
        cas.append({
            "cas": "fichier_inexistant",
            "ok": (sortie["code"] == 4 and sortie["stdout"] == ""
                   and "fichier introuvable" in sortie["stderr"] and not sortie["trace"]),
            "code": sortie["code"],
            "stdout_vide": sortie["stdout"] == "",
            "message": sortie["stderr"].strip(),
            "trace": sortie["trace"],
        })
        sortie = _run("analyser", "--fichier", dossier)
        cas.append({
            "cas": "fichier_repertoire",
            "ok": (sortie["code"] == 5 and sortie["stdout"] == ""
                   and "répertoire" in sortie["stderr"] and not sortie["trace"]),
            "code": sortie["code"],
            "stdout_vide": sortie["stdout"] == "",
            "message": sortie["stderr"].strip(),
            "trace": sortie["trace"],
        })
    return cas


def _cas_codes() -> list[dict]:
    cas = []
    for nom, arguments, attendu in (
        ("usage_sans_commande", (), 5),
        ("usage_langue_inconnue", ("analyser", "Le chat dort.", "--langue", "de"), 5),
        ("usage_option_fantome", ("analyser", "Le chat dort.", "--sortie"), 5),
        ("refus_texte_vide", ("analyser", "", "--json"), 3),
        ("refus_rejouer", ("rejouer", ""), 3),
    ):
        sortie = _run(*arguments)
        entree = {"cas": nom, "attendu": attendu, "code": sortie["code"],
                  "ok": sortie["code"] == attendu and not sortie["trace"], "trace": sortie["trace"]}
        if nom == "refus_texte_vide":
            try:
                d = json.loads(sortie["stdout"])
                entree["json_de_refus"] = bool(d.get("refus") and d.get("schema"))
            except ValueError:
                entree["json_de_refus"] = False
                entree["ok"] = False
        cas.append(entree)
    sans_cle = _run("analyser", "Le chat dort.", "--tagger", env=_sans_cle())
    cas.append({
        "cas": "dependance_cle_absente",
        "attendu": 4, "code": sans_cle["code"],
        "ok": (sans_cle["code"] == 4 and sans_cle["stdout"] == ""
               and "dépendance absente" in sans_cle["stderr"] and not sans_cle["trace"]),
        "stdout_vide": sans_cle["stdout"] == "", "trace": sans_cle["trace"],
    })
    return cas


def principal() -> dict:
    cas = [_cas_duree(), _cas_duree_jsonl(), *_cas_aide(), *_cas_entrees(), *_cas_codes()]
    notice = (RACINE / "docs" / "produit" / "README.md").read_text(encoding="utf-8")
    codes_notice = {}
    for code in ("0", "3", "4", "5"):
        ligne = re.search(rf"^\| \*\*{code}\*\* \|.*$", notice, re.MULTILINE)
        codes_notice[code] = bool(ligne)
    cas.append({"cas": "tableau_codes_notice", "ok": all(codes_notice.values()),
                "codes": codes_notice})
    return {
        "schema": "drave.cli_robuste.verification",
        "version": 1,
        "date": DATE,
        "tache": "T5 (exploitable, 5/5)",
        "commit": _commit(),
        "python": sys.version.split()[0],
        "cas": cas,
        "ok": all(c["ok"] for c in cas),
    }


def _resume(rapport: dict) -> str:
    lignes = [f"CLI robuste — {sum(c['ok'] for c in rapport['cas'])}/{len(rapport['cas'])} "
              f"cas tenus · commit {rapport['commit'][:8]}"]
    for cas in rapport["cas"]:
        if not cas["ok"]:
            lignes.append(f"  ❌ {cas['cas']} : {json.dumps(cas, ensure_ascii=False)[:300]}")
    lignes.append("✅ CLI robuste" if rapport["ok"] else "❌ CLI non robuste")
    return "\n".join(lignes)


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--json", action="store_true",
                         help="le JSON de reports/cli-robuste.json")
    args = parseur.parse_args(argv)
    rapport = principal()
    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=1))
    else:
        print(_resume(rapport))
    return 0 if rapport["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

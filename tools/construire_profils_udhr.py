#!/usr/bin/env python3
"""construire_profils_udhr.py — construit l'artefact de profils de langue UDHR.

Les profils sont des **données** : 398 langues, un profil de trigrammes de caractères par
langue, construit sur les articles **0–14** de `data/udhr/articles.jsonl` (article 15 tenu à
l'écart). Le fichier produit est embarqué dans la roue (`package-data`) et lu par
`tools/profils_udhr.py`, donc par `drave profils` et `drave analyser --profils`.

    python3 tools/construire_profils_udhr.py
    python3 tools/construire_profils_udhr.py --udhr data/udhr/articles.jsonl \
        --sortie tools/tests/linguistique/profils_udhr.json --top 200

Le fichier est **déterministe** (langues triées, JSON compact, pas d'horodatage) : deux
constructions sur le même corpus rendent le même octet. `source_sha256` permet de vérifier
que l'artefact vient bien du corpus courant ; `--verifier` compare l'artefact existant à une
construction fraîche et sort en 1 s'il a dérivé.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE))

import bloc_linguistique as bl  # noqa: E402
import profils_udhr as pu  # noqa: E402


def construire(udhr: pathlib.Path, top: int = pu.TOP_DEFAUT,
               train: tuple[int, int] = (0, 14)) -> dict:
    """Construit l'artefact complet (métadonnées + 398 profils)."""
    profils, _tests = bl.charger_profils_udhr(
        udhr, train=train, test=(15, 30), min_train=5, min_test=0, top=top)
    noms: dict[str, str] = {}
    scripts: dict[str, set[str]] = collections.defaultdict(set)
    for ligne in udhr.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        d = json.loads(ligne)
        code = d.get("iso3", "und")
        if code == "und":
            continue
        noms.setdefault(code, d.get("nom", ""))
        if d.get("script"):
            scripts[code].add(d["script"])
    langues = {}
    for code, p in sorted(profils.items()):
        langues[code] = {
            "nom": noms.get(code, ""),
            "script": p["script"],
            "scripts": sorted(scripts.get(code, [])),
            "n_train": int(p["n_train"]),
            "trigrammes": p["trigrammes"],
        }
    return {
        "schema": pu.SCHEMA_PROFILS,
        "version": pu.VERSION_PROFILS,
        "source": str(udhr.resolve().relative_to(RACINE)) if udhr.resolve().is_relative_to(RACINE) else str(udhr),
        "source_sha256": pu.empreinte_fichier(udhr),
        "train": [int(train[0]), int(train[1])],
        "top": int(top),
        "langues": langues,
    }


def ecrire(donnees: dict, sortie: pathlib.Path) -> str:
    """Écrit le JSON compact et rend son sha256 (même octet à chaque construction)."""
    sortie.parent.mkdir(parents=True, exist_ok=True)
    texte = json.dumps(donnees, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n"
    sortie.write_text(texte, encoding="utf-8")
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--udhr", default=str(RACINE / "data/udhr/articles.jsonl"))
    ap.add_argument("--sortie", default=str(pu.PROFILS_DEFAUT))
    ap.add_argument("--top", type=int, default=pu.TOP_DEFAUT)
    ap.add_argument("--verifier", action="store_true",
                    help="comparer l'artefact existant à une construction fraîche (code 1 si dérive)")
    a = ap.parse_args()
    udhr = pathlib.Path(a.udhr)
    sortie = pathlib.Path(a.sortie)
    if not udhr.is_file():
        print(f"drave: profils : corpus introuvable : {udhr}", file=sys.stderr)
        return 4
    donnees = construire(udhr, top=a.top)
    sha = ecrire(donnees, sortie) if not a.verifier else ""
    texte = json.dumps(donnees, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n"
    sha_frais = hashlib.sha256(texte.encode("utf-8")).hexdigest()
    if a.verifier:
        if not sortie.is_file():
            print(f"drave: profils : artefact absent : {sortie}", file=sys.stderr)
            return 4
        sha_existant = pu.empreinte_fichier(sortie)
        if sha_existant != sha_frais:
            print(f"drave: profils : artefact dérivé ({sha_existant[:16]}… != "
                  f"{sha_frais[:16]}…) — relancer sans --verifier", file=sys.stderr)
            return 1
    else:
        print(f"profils UDHR : {len(donnees['langues'])} langues · "
              f"{len(texte.encode('utf-8'))} octets · sha256 {sha[:16]}…")
        print(f"  source : {donnees['source']} ({donnees['source_sha256'][:16]}…)")
        print(f"  sortie : {sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

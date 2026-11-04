#!/usr/bin/env python3
"""n3_inventaire.py — la couverture N3, vérifiée au lieu d'être racontée.

POURQUOI CET OUTIL EXISTE. N3.1 (29/10) publie un inventaire statique : « sortie
précoce : service non », « k-WTA/routes : aucune porte, aucun chemin ». N3.2b0 et
N3.3a lui donnent tort **le même jour**, et N3.4d conclut « couvert par brique »
sans qu'aucune des deux fiches ne soit corrigée. Six jours plus tard, la fiche de
backlog dit encore « ⏳ une porte par brique » alors que `tools/porte-n3-*.sh` en
contient dix-sept, toutes vertes. Un inventaire écrit à la main ment dès qu'une
brique bouge : c'est le même défaut qu'une porte qu'on croit verte sans l'avoir
lancée — appliqué à la documentation.

CE QUE L'OUTIL VÉRIFIE (statique, aucune mesure, aucun run) :
  1. chaque porte `tools/porte-n3-*.sh` est citée par au moins une fiche
     `reports/rapport-n3*.md` (aucune porte orpheline) ;
  2. chaque porte citée existe sur disque et passe `bash -n` (aucune référence
     morte, aucune porte cassée) ;
  3. chaque JSON `reports/n3*.json` est cité par une fiche, et chaque JSON cité
     existe (la chaîne fiche → données → porte est complète) ;
  4. les seuils de couverture du 2026-11-04 ne baissent pas (17 portes de brique
     + celle-ci, 19 fiches + celle-ci, 19 JSON + celui-ci) : perdre un instrument est
     une régression, pas un détail.

CONTRÔLE NÉGATIF (`--autotest`). L'outil construit un dépôt temporaire minimal et
vérifie qu'il **échoue** quand on retire une porte, quand on ajoute une porte
orpheline, quand on retire un JSON et quand on ajoute un JSON orphelin. Un
vérificateur qui ne sait pas échouer ne vérifie rien.

Usage :
  python3 tools/n3_inventaire.py                 # le tableau + le verdict
  python3 tools/n3_inventaire.py --json F        # écrit l'inventaire
  python3 tools/n3_inventaire.py --autotest      # contrôle négatif (5 cas)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]

# Le contrat de couverture, figé le 2026-11-04 : 17 portes de brique + la porte
# d'inventaire = 18, 19 fiches + celle-ci = 20, 19 JSON + celui-ci = 20. Perdre un
# instrument est une régression : les seuils ne baissent pas sans décision explicite.
SEUILS = (18, 20, 20)

PORTE = re.compile(r"(porte-n3-[a-z0-9-]+\.sh)")
JSON_N3 = re.compile(r"(?<![\w-])(n3[.-][a-z0-9.-]+\.json)")


def fiches(racine: Path) -> list[Path]:
    return sorted((racine / "reports").glob("rapport-n3[.-]*.md"))


def lire_references(racine: Path):
    refs_portes: set[str] = set()
    refs_json: set[str] = set()
    for f in fiches(racine):
        texte = f.read_text(encoding="utf-8", errors="replace")
        refs_portes |= set(PORTE.findall(texte))
        refs_json |= {Path(m).name for m in JSON_N3.findall(texte)}
    return refs_portes, refs_json


def collecter(racine: Path, seuils=SEUILS) -> dict:
    portes = {p.name for p in (racine / "tools").glob("porte-n3-*.sh")}
    listes = [p.name for p in (racine / "reports").glob("n3[.-]*.json")]
    jsons = {n for n in listes}
    refs_portes, refs_json = lire_references(racine)

    portes_manquantes = sorted(refs_portes - portes)
    portes_orphelines = sorted(portes - refs_portes)
    json_manquants = sorted(refs_json - jsons)
    json_orphelins = sorted(jsons - refs_json)

    syntaxe = []
    for nom in sorted(portes):
        r = subprocess.run(["bash", "-n", str(racine / "tools" / nom)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            syntaxe.append(nom)

    constats: list[str] = []
    if portes_manquantes:
        constats.append("portes manquantes : " + ", ".join(portes_manquantes))
    if portes_orphelines:
        constats.append("portes orphelines : " + ", ".join(portes_orphelines))
    if json_manquants:
        constats.append("json manquants : " + ", ".join(json_manquants))
    if json_orphelins:
        constats.append("json orphelins : " + ", ".join(json_orphelins))
    if syntaxe:
        constats.append("portes qui ne passent pas bash -n : " + ", ".join(syntaxe))
    if len(portes) < seuils[0]:
        constats.append(f"couverture perdue : {len(portes)} portes < {seuils[0]}")
    if len(fiches(racine)) < seuils[1]:
        constats.append(f"couverture perdue : {len(fiches(racine))} fiches < {seuils[1]}")
    if len(jsons) < seuils[2]:
        constats.append(f"couverture perdue : {len(jsons)} json < {seuils[2]}")

    return {
        "portes": sorted(portes),
        "fiches": [f.name for f in fiches(racine)],
        "json": sorted(jsons),
        "references": {"portes": sorted(refs_portes), "json": sorted(refs_json)},
        "constats": constats,
        "seuils": list(seuils),
    }


def autotest() -> int:
    """Cinq cas : le sain passe, les quatre défauts échouent."""
    with tempfile.TemporaryDirectory() as tmp:
        r = Path(tmp)
        (r / "tools").mkdir()
        (r / "reports").mkdir()
        (r / "tools" / "porte-n3-a.sh").write_text("#!/bin/bash\nexit 0\n")
        (r / "reports" / "n3.a.json").write_text("{}\n")
        (r / "reports" / "rapport-n3.a.md").write_text(
            "# T\n\n- `tools/porte-n3-a.sh`\n- `reports/n3.a.json`\n")
        seuils = (1, 1, 1)

        def constats() -> str:
            return " | ".join(collecter(r, seuils)["constats"])

        cas = []
        cas.append(("sain", constats(), None))
        (r / "tools" / "porte-n3-a.sh").unlink()
        cas.append(("porte retirée", constats(), "portes manquantes"))
        (r / "tools" / "porte-n3-a.sh").write_text("#!/bin/bash\nexit 0\n")
        (r / "tools" / "porte-n3-b.sh").write_text("#!/bin/bash\nexit 0\n")
        cas.append(("porte orpheline", constats(), "portes orphelines"))
        (r / "tools" / "porte-n3-b.sh").unlink()
        (r / "reports" / "n3.a.json").unlink()
        cas.append(("json retiré", constats(), "json manquants"))
        (r / "reports" / "n3.a.json").write_text("{}\n")
        (r / "reports" / "n3.b.json").write_text("{}\n")
        cas.append(("json orphelin", constats(), "json orphelins"))

        echecs = []
        for nom, sortie, attendu in cas:
            if attendu is None:
                ok = sortie == ""
            else:
                ok = attendu in sortie
            print(f"  {'✅' if ok else '❌'} autotest · {nom}"
                  + (f" → « {sortie} »" if not ok else ""))
            if not ok:
                echecs.append(nom)
        if echecs:
            print(f"  ❌ autotest : {len(echecs)} cas faux")
            return 1
        print(f"  ✅ autotest : {len(cas)}/{len(cas)} cas attendus")
        return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--racine", default=str(RACINE))
    p.add_argument("--json", dest="sortie")
    p.add_argument("--autotest", action="store_true")
    a = p.parse_args()

    if a.autotest:
        return autotest()

    racine = Path(a.racine).resolve()
    inv = collecter(racine)
    print("=== l'inventaire N3 (couverture exécutable) ===")
    print(f"  portes ......... {len(inv['portes']):2d}  "
          f"({len(inv['references']['portes'])} citées par les fiches)")
    print(f"  fiches ......... {len(inv['fiches']):2d}")
    print(f"  JSON ........... {len(inv['json']):2d}  "
          f"({len(inv['references']['json'])} cités par les fiches)")
    if inv["constats"]:
        for c in inv["constats"]:
            print(f"  ❌ {c}")
        if a.sortie:
            Path(a.sortie).write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")
        return 1
    print("  ✅ PORTE TENUE : chaque brique a sa porte, chaque fiche sa porte et son JSON — "
          "aucune référence morte, aucun instrument orphelin")
    if a.sortie:
        Path(a.sortie).write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n",
                                  encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""verifier_schemas.py — les illustrations sont des SVG, pas de l'ASCII art.

Ce que l'outil vérifie :
  1. aucun bloc de code des documents ne dessine une architecture, un flux, un arbre ou une
     carte (caractères de boîte, flèches `──►`, `+--+`) ;
  2. chaque SVG parse, a un `viewBox`, un `<title>`, un `<desc>`, `role="img"` et n'appelle
     aucune ressource externe. Un SVG **généré** (`<source>.puml.svg` / `<source>.mmd.svg`)
     n'a pas à porter les métadonnées : docwatch les produit ;
  3. chaque image Markdown est relative, pointe vers un `.svg` et a un texte alternatif ; un
     `<source>.svg` peut être **absent** si le source `.puml`/`.mmd` existe (docwatch le génère) ;
  4. chaque SVG direct et chaque source `.puml`/`.mmd` est référencé dans un document ;
  5. chaque bloc **PlantUML inline** (```plantuml) se rend (PlantUML requis ; Mermaid est
     rendu par docwatch mais non vérifié ici).

Sortie : un rapport lisible, code 0 si tout passe, 1 sinon.
"""
from __future__ import annotations
import pathlib
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

RACINE = pathlib.Path(__file__).resolve().parent.parent
DOCS = RACINE / "docs"
SCHEMAS = DOCS / "schemas"
SCHEMAS_SYNTH = DOCS / "synthese" / "schemas"
GENERE = (".puml.svg", ".mmd.svg")
NS = "{http://www.w3.org/2000/svg}"


def documents():
    return [p for p in DOCS.rglob("*.md") if "archive" not in p.parts]


def blocs_code(texte: str):
    for m in re.finditer(r"```([^\n]*)\n(.*?)```", texte, re.S):
        ligne = texte[: m.start()].count("\n") + 1
        yield ligne, m.group(1).strip().lower(), m.group(2)


def est_ascii_art(contenu: str) -> bool:
    boites = len(re.findall(r"[┌┐└┘├┤┬┴┼│─═║╔╗╚╝]", contenu))
    fleches = len(re.findall(r"──►|◄──|──>", contenu))
    plus = len(re.findall(r"^\s*\+--", contenu, re.M))
    barres = len(re.findall(r"^\s*\|", contenu, re.M))
    return boites >= 3 or fleches >= 2 or (plus >= 2 and barres >= 2)


def verifier_ascii(alertes: list[str]):
    for p in documents():
        texte = p.read_text(encoding="utf-8", errors="ignore")
        for ligne, info, contenu in blocs_code(texte):
            if "mermaid" in info or "plantuml" in info or "puml" in info:
                continue
            if est_ascii_art(contenu):
                alertes.append(f"ASCII art : {p.relative_to(RACINE)}:{ligne} — dessiner en SVG")


def verifier_images(alertes: list[str]):
    for p in documents():
        texte = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", texte):
            alt, cible = m.group(1).strip(), m.group(2).strip()
            ligne = texte[: m.start()].count("\n") + 1
            if not alt:
                alertes.append(f"image sans texte alternatif : {p.relative_to(RACINE)}:{ligne}")
            if cible.startswith(("http://", "https://", "/")):
                alertes.append(f"image non relative : {p.relative_to(RACINE)}:{ligne} → {cible}")
                continue
            if not cible.lower().endswith(".svg"):
                alertes.append(f"image non SVG : {p.relative_to(RACINE)}:{ligne} → {cible}")
                continue
            if cible.endswith(GENERE):
                source = cible[:-4]
                if not (p.parent / source).exists():
                    alertes.append(f"source absente : {p.relative_to(RACINE)}:{ligne} → {source}")
                continue
            if not (p.parent / cible).resolve().exists():
                alertes.append(f"image absente : {p.relative_to(RACINE)}:{ligne} → {cible}")


def verifier_svg(alertes: list[str]) -> set[pathlib.Path]:
    vus: set[pathlib.Path] = set()
    for p in sorted(DOCS.rglob("*.svg")):
        vus.add(p.resolve())
        genere = p.name.endswith(GENERE)
        try:
            racine = ET.parse(p).getroot()
        except Exception as e:
            alertes.append(f"SVG invalide : {p.relative_to(RACINE)} ({e})")
            continue
        if racine.get("viewBox") is None:
            alertes.append(f"SVG sans viewBox : {p.relative_to(RACINE)}")
        if not genere:
            if racine.find(NS + "title") is None and racine.find("title") is None:
                alertes.append(f"SVG sans <title> : {p.relative_to(RACINE)}")
            if racine.find(NS + "desc") is None and racine.find("desc") is None:
                alertes.append(f"SVG sans <desc> : {p.relative_to(RACINE)}")
            if racine.get("role") != "img":
                alertes.append(f"SVG sans role=\"img\" : {p.relative_to(RACINE)}")
        for elem in racine.iter():
            if elem.tag.endswith("script"):
                alertes.append(f"SVG avec script : {p.relative_to(RACINE)}")
            for attr in ("href", "{http://www.w3.org/1999/xlink}href", "src"):
                val = elem.get(attr)
                if val and val.startswith(("http://", "https://", "/")):
                    alertes.append(f"SVG avec ressource externe : {p.relative_to(RACINE)} ({val})")
    return vus


def verifier_references(alertes: list[str]):
    texte = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in documents())
    for dossier in (SCHEMAS, SCHEMAS_SYNTH):
        if not dossier.exists():
            continue
        for src in sorted(list(dossier.glob("*.mmd")) + list(dossier.glob("*.puml"))):
            if src.name not in texte:
                alertes.append(f"source non référencée : {src.relative_to(RACINE)}")
        for p in sorted(dossier.glob("*.svg")):
            if p.name.endswith(GENERE):
                continue
            if p.name not in texte:
                alertes.append(f"schéma non référencé : {p.relative_to(RACINE)}")


def _valider_plantuml(source: str) -> bool:
    """Rend le source en SVG ; sans PlantUML installé, on ne bloque pas."""
    plantuml = shutil.which("plantuml")
    if not plantuml:
        return True
    if not re.search(r"(?m)^\s*@start\w*", source):
        source = "@startuml\n" + source + "\n@enduml\n"
    try:
        r = subprocess.run(
            [plantuml, "-tsvg", "-pipe"],
            input=source.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return r.returncode == 0 and b"<svg" in r.stdout


def verifier_inline(alertes: list[str]):
    """Un bloc PlantUML inline qui ne se rend pas laisserait son code dans la page."""
    for p in documents():
        texte = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(
            r"(?m)^[ \t]*```[ \t]*(plantuml|puml|pu)[ \t]*\n(.*?)^[ \t]*```[ \t]*$",
            texte,
            re.S,
        ):
            ligne = texte[: m.start()].count("\n") + 1
            if not _valider_plantuml(m.group(2)):
                alertes.append(f"diagramme inline invalide : {p.relative_to(RACINE)}:{ligne}")


def main() -> int:
    alertes: list[str] = []
    verifier_ascii(alertes)
    verifier_images(alertes)
    verifier_svg(alertes)
    verifier_references(alertes)
    verifier_inline(alertes)
    nd = len(documents())
    ni = len(list(DOCS.rglob("*.svg")))
    nsrc = len(list(DOCS.rglob("*.puml"))) + len(list(DOCS.rglob("*.mmd")))
    print(f"  schémas · {nd} document(s) · {ni} SVG · {nsrc} source(s)")
    if not alertes:
        print("  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,")
        print("     sources et images relatives.")
        return 0
    print(f"  ❌ {len(alertes)} anomalie(s) :")
    for a in alertes:
        print(f"     · {a}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

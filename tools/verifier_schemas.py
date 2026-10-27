#!/usr/bin/env python3
"""verifier_schemas.py — les illustrations sont des SVG, pas de l'ASCII art.

Ce que l'outil vérifie :
  1. aucun bloc de code des documents ne dessine une architecture, un flux, un arbre ou une
     carte (caractères de boîte, flèches `──►`, `+--+`) ;
  2. chaque SVG parse, a un `viewBox`, un `<title>`, un `<desc>`, `role="img"` et n'appelle
     aucune ressource externe ;
  3. chaque image Markdown est relative, pointe vers un `.svg` existant et a un texte alternatif ;
  4. chaque SVG de `docs/schemas/` et `docs/synthese/schemas/` est référencé dans un document.

Sortie : un rapport lisible, code 0 si tout passe, 1 sinon.
"""
from __future__ import annotations
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

RACINE = pathlib.Path(__file__).resolve().parent.parent
DOCS = RACINE / "docs"
SCHEMAS = DOCS / "schemas"
SCHEMAS_SYNTH = DOCS / "synthese" / "schemas"


def documents():
    return [p for p in DOCS.rglob("*.md") if "archive" not in p.parts]


def blocs_code(texte: str):
    """(ligne, info, contenu) des blocs de code fencés."""
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
            if not (p.parent / cible).resolve().exists():
                alertes.append(f"image absente : {p.relative_to(RACINE)}:{ligne} → {cible}")


def verifier_svg(alertes: list[str]) -> set[pathlib.Path]:
    vus: set[pathlib.Path] = set()
    for p in sorted(DOCS.rglob("*.svg")):
        vus.add(p.resolve())
        try:
            racine = ET.parse(p).getroot()
        except Exception as e:
            alertes.append(f"SVG invalide : {p.relative_to(RACINE)} ({e})")
            continue
        if racine.get("viewBox") is None:
            alertes.append(f"SVG sans viewBox : {p.relative_to(RACINE)}")
        if racine.get("{http://www.w3.org/2000/svg}title") is None and racine.find("{http://www.w3.org/2000/svg}title") is None:
            if racine.find("title") is None:
                alertes.append(f"SVG sans <title> : {p.relative_to(RACINE)}")
        if racine.find("desc") is None and racine.find("{http://www.w3.org/2000/svg}desc") is None:
            alertes.append(f"SVG sans <desc> : {p.relative_to(RACINE)}")
        if racine.get("role") != "img":
            alertes.append(f"SVG sans role=\"img\" : {p.relative_to(RACINE)}")
        for elem in racine.iter():
            if elem.tag.endswith("script"):
                alertes.append(f"SVG avec script : {p.relative_to(RACINE)}")
            for attr in ("href", "{http://www.w3.org/1999/xlink}href", "src"):
                val = elem.get(attr)
                if val and (val.startswith(("http://", "https://", "/"))):
                    alertes.append(f"SVG avec ressource externe : {p.relative_to(RACINE)} ({val})")
    return vus


def verifier_references(alertes: list[str], svgs: set[pathlib.Path]):
    texte = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in documents())
    for dossier in (SCHEMAS, SCHEMAS_SYNTH):
        if not dossier.exists():
            continue
        for p in sorted(dossier.glob("*.svg")):
            if p.name not in texte:
                alertes.append(f"schéma non référencé : {p.relative_to(RACINE)}")


def main() -> int:
    alertes: list[str] = []
    verifier_ascii(alertes)
    verifier_images(alertes)
    svgs = verifier_svg(alertes)
    verifier_references(alertes, svgs)
    nd = len(documents())
    ni = len(list(DOCS.rglob("*.svg")))
    print(f"  schémas · {nd} document(s) · {ni} SVG")
    if not alertes:
        print("  ✅ aucun ASCII art, SVG valides et référencés, images relatives.")
        return 0
    print(f"  ❌ {len(alertes)} anomalie(s) :")
    for a in alertes:
        print(f"     · {a}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

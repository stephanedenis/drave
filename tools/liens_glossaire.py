#!/usr/bin/env python3
"""liens_glossaire.py — lier la première occurrence des termes du glossaire.

POURQUOI CE SCRIPT. Le glossaire (335 entrées) n'est utile que si le lecteur le
trouve. Docwatch annote les termes **au rendu**, sans toucher au Markdown ; mais
GitHub ne lit que le Markdown, et n'affiche ni pointillé ni fiche. Ce script
ajoute donc, dans les pages de `docs/`, un lien vers la fiche du terme — pour la
**première occurrence de chaque terme dans chaque page**, jamais « partout » :
lier toutes les occurrences noierait la lecture et gonflerait le contenu.

CE QU'IL NE FAIT PAS. Il n'entre pas dans les blocs de code, le code en ligne,
les liens existants, les titres d'image ni les tableaux de caractères ; il
n'invente pas de terme (il lit `docs/theorie/glossaire/index.json`) ; il
n'écrit rien sans `--ecrire`.

Usage :
  python3 tools/liens_glossaire.py --verifier     # liste ce qui serait lié
  python3 tools/liens_glossaire.py --ecrire       # écrit les liens
  python3 tools/liens_glossaire.py --page docs/theorie/vision.md --verifier
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
GLOSSAIRE = RACINE / "docs/theorie/glossaire"
INDEX = GLOSSAIRE / "index.json"
DOCS = RACINE / "docs"

#: Dossiers de docs/ exclus : le glossaire lui-même (il se cite) et l'archive
#: (les documents datés ne se réécrivent pas).
EXCLUS = ("theorie/glossaire", "archive")


def charger_termes() -> dict:
    """Charge l'index et rend {variante minuscule: slug}, variantes comprises."""
    donnees = json.loads(INDEX.read_text(encoding="utf-8"))
    termes = {}
    for entree in donnees.get("entrees", []):
        slug = str(entree.get("slug", "")).strip()
        terme = str(entree.get("terme", "")).strip()
        if not slug or not terme:
            continue
        variantes = {terme.lower(), re.split(r"[·;,(]", terme)[0].strip().lower()}
        for variante in variantes:
            if 2 <= len(variante) <= 60 and variante not in termes:
                termes[variante] = slug
    return termes


def compiler(termes: dict) -> re.Pattern:
    """L'alternance des termes, les plus longs d'abord (sinon « porte » mange
    « porte de correction »)."""
    morceaux = sorted(termes, key=len, reverse=True)
    return re.compile(
        r"(?<![\w-])(" + "|".join(re.escape(m) for m in morceaux) + r")(?![\w-])",
        re.IGNORECASE,
    )


def _masque_code(texte: str):
    """Rend le texte et un masque des zones interdites (code, liens, balises).

    Le masque est une liste de booléens, un par caractère : ``True`` = zone
    muette. Une occurrence qui commence dans une zone muette est ignorée.
    """
    muet = [False] * len(texte)
    motifs = [
        r"```.*?```",          # blocs de code
        r"`[^`\n]*`",           # code en ligne
        r"!\[[^\]]*\]\([^)]*\)",  # images
        r"\[[^\]]*\]\([^)]*\)",   # liens existants
        r"<[^>\n]*>",           # balises HTML
    ]
    for motif in motifs:
        for m in re.finditer(motif, texte, flags=re.S):
            for i in range(m.start(), m.end()):
                muet[i] = True
    return muet


def lier(texte: str, chemin: pathlib.Path, motif: re.Pattern, termes: dict):
    """Rend (nouveau texte, liste des (terme, slug)) en liant la première
    occurrence de chaque terme, hors zones muettes."""
    muet = _masque_code(texte)
    vus = set()
    liens = []
    sortie = []
    dernier = 0
    for m in motif.finditer(texte):
        debut = m.start()
        if muet[debut]:
            continue
        cle = m.group(0).lower()
        if cle in vus:
            continue
        slug = termes.get(cle) or termes.get(re.sub(r"[·;,(].*$", "", cle).strip())
        if not slug:
            continue
        fiche = GLOSSAIRE / "entrees" / (slug + ".md")
        if not fiche.is_file():
            continue
        relatif = pathlib.Path(
            *[".."] * (len(chemin.relative_to(DOCS).parts) - 1)
        ) / "theorie/glossaire/entrees" / (slug + ".md")
        vus.add(cle)
        liens.append((m.group(0), slug))
        sortie.append(texte[dernier:debut])
        sortie.append("[%s](%s)" % (m.group(0), relatif.as_posix()))
        dernier = m.end()
    sortie.append(texte[dernier:])
    return "".join(sortie), liens


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ecrire", action="store_true", help="écrit les liens")
    ap.add_argument("--verifier", action="store_true", help="ne fait que lister")
    ap.add_argument("--page", type=pathlib.Path, help="une seule page")
    args = ap.parse_args()
    if not (args.ecrire or args.verifier):
        args.verifier = True
    termes = charger_termes()
    motif = compiler(termes)
    pages = [args.page.resolve()] if args.page else sorted(DOCS.rglob("*.md"))
    total_pages = 0
    total_liens = 0
    for page in pages:
        if not page.is_file():
            continue
        rel = page.relative_to(DOCS).as_posix()
        if any(rel.startswith(exclu) for exclu in EXCLUS):
            continue
        texte = page.read_text(encoding="utf-8")
        nouveau, liens = lier(texte, page, motif, termes)
        if not liens:
            continue
        total_pages += 1
        total_liens += len(liens)
        if args.verifier:
            print("%s : %d lien(s) %s" % (rel, len(liens), [s for _, s in liens][:8]))
        if args.ecrire and nouveau != texte:
            page.write_text(nouveau, encoding="utf-8")
    print("→ %d page(s), %d lien(s)%s" % (
        total_pages, total_liens, "" if args.ecrire else " (rien écrit : --ecrire pour appliquer)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

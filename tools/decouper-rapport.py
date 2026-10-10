#!/usr/bin/env python3
"""decouper-rapport.py — éclater un rapport monolithique en UNE EXPÉRIENCE PAR FICHIER.

POURQUOI. `reports/` doit contenir un rapport par expérience (voir
`docs/organisation-du-depot.md`). Un fichier de 179 Ko couvrant 47 expériences n'est ni
citable, ni reliable, ni datable : on ne peut pas dire « le §32 a été mesuré le … ». Ce
script découpe un rapport par ses titres `## `, écrit un fichier par section, et **date
chaque fichier avec git** — la seule source de vérité des dates de ce dépôt, puisque des
estampilles écrites à la main s'étaient retrouvées **dans le futur**.

CE QU'IL GARANTIT :
  1. le **contenu est recopié à l'identique** (aucun paragraphe réécrit, aucune perte) :
     chaque fichier = un en-tête de 5 lignes + la section d'origine, verbatim ;
  2. la **date réelle** de chaque section vient du commit qui l'a introduite
     (`git log -S`), avec le hash cité ; si elle est introuvable, le fichier dit
     « date inconnue » — jamais une date plausible ;
  3. l'**index** liste chaque fichier avec son titre, sa date et son hash ;
  4. le monolithe est **déplacé** vers `reports/archive/` (git mv), pas supprimé.

Usage :
  tools/decouper-rapport.py reports/rapport-campagne-benefices.md --dossier campagne-benefices
  tools/decouper-rapport.py <source> --dossier <nom> [--index <chemin>] [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent


def sans_accents(txt: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", txt) if not unicodedata.combining(c))


def slug(titre: str, maxi: int = 48) -> str:
    t = sans_accents(titre).lower()
    t = re.sub(r"`|\*|_|«|»|\"|'", "", t)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:maxi].rstrip("-")


def date_git(chemin: Path, extrait: str) -> tuple[str, str]:
    """(date, hash) du commit qui a introduit `extrait` dans `chemin`."""
    for motif in (extrait, extrait[:40], extrait[:24]):
        if len(motif) < 8:
            break
        r = subprocess.run(
            ["git", "log", "-S", motif, "-1", "--format=%ad|%h", "--date=format:%Y-%m-%d %H:%M",
             "--", str(chemin.relative_to(RACINE))],
            cwd=RACINE, capture_output=True, text=True)
        sortie = r.stdout.strip()
        if sortie and "|" in sortie:
            d, h = sortie.split("|", 1)
            return d + " HAE", h
    return "date inconnue", "?"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--dossier", required=True, help="sous-dossier de reports/ à créer")
    ap.add_argument("--index", default=None, help="chemin de l'index (défaut : reports/<dossier>.md)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    src = (RACINE / a.source).resolve()
    texte = src.read_text(encoding="utf-8")
    lignes = texte.splitlines(keepends=True)

    # découpe sur les titres de niveau 2
    titres = [(i, l.rstrip("\n")) for i, l in enumerate(lignes) if l.startswith("## ")]
    if not titres:
        print("aucun titre `## ` : rien à découper", file=sys.stderr)
        return 1

    sortie = RACINE / "reports" / a.dossier
    archive = RACINE / "reports" / "archive"
    if not a.dry_run:
        sortie.mkdir(parents=True, exist_ok=True)
        archive.mkdir(parents=True, exist_ok=True)
    index = RACINE / (a.index or f"reports/{a.dossier}.md")

    # préambule = tout ce qui précède le premier titre de niveau 2
    preambule = "".join(lignes[: titres[0][0]]).strip()

    entrees = []
    for n, (i, titre) in enumerate(titres):
        fin = titres[n + 1][0] if n + 1 < len(titres) else len(lignes)
        corps = "".join(lignes[i:fin]).rstrip() + "\n"
        nom_titre = titre[3:].strip()
        # numéro d'expérience : « ## 32. … », « ## 0 bis. … », sinon l'ordre
        m = re.match(r"(\d+)\s*(bis|ter|quater)?\.?\s*(.*)", nom_titre)
        if m and m.group(1):
            # le numéro d'origine est CONSERVÉ dans le nom, mais le préfixe d'ordre reste
            # unique : deux sections pouvaient porter « 0 » (le résumé non numéroté et le §0).
            num = f"{int(m.group(1)):02d}" + (f"-{m.group(2)}" if m.group(2) else "")
            libelle = m.group(3)
        else:
            num, libelle = "R", nom_titre
        fichier = sortie / f"{n + 1:02d}-{num}-{slug(libelle, 40)}.md"
        date, hash_ = date_git(src, nom_titre)
        entete = (
            f"> Campagne : **{a.dossier}** · expérience **{num}**\n"
            f"> Titre : {nom_titre}\n"
            f"> Date réelle : **{date}** (source : commit `{hash_}`)\n"
            f"> Source : extrait **verbatim** du rapport monolithique, archivé en "
            f"`reports/archive/{src.name}`\n\n"
        )
        if not a.dry_run:
            fichier.write_text(entete + corps, encoding="utf-8")
        entrees.append((f"{n + 1:02d} · {num}", nom_titre, fichier.name, date, hash_))

    # index
    lignes_index = [preambule, "", "## Index des expériences", "",
                    "| # | expérience | date réelle (git) | fichier |",
                    "|---|---|---|---|"]
    for num, nom_titre, nom_fichier, date, hash_ in entrees:
        lignes_index.append(f"| {num} | {nom_titre} | {date} (`{hash_}`) | "
                            f"[{nom_fichier}]({a.dossier}/{nom_fichier}) |")
    lignes_index += [
        "",
        "**Les estampilles écrites dans le corps des textes ne sont pas fiables** : elles ont été",
        "saisies à la main en avançant une horloge supposée, et certaines tombaient **dans le",
        "futur** (jusqu'au 12 octobre 2026). La date fiable est celle de l'en-tête de chaque",
        "fichier, tirée de git. Voir `docs/organisation-du-depot.md` § 4.",
        "",
    ]
    if not a.dry_run:
        index.write_text("\n".join(lignes_index), encoding="utf-8")

    print(f"{len(entrees)} expériences → {sortie}")
    for num, nom_titre, nom_fichier, date, hash_ in entrees:
        print(f"  {num:>5}  {date:<22} {hash_:<9} {nom_fichier}")
    if not a.dry_run:
        # le monolithe part en archive (git mv quand il est suivi, sinon copie)
        dest = archive / src.name
        suivi = subprocess.run(["git", "ls-files", "--error-unmatch", str(src.relative_to(RACINE))],
                               cwd=RACINE, capture_output=True).returncode == 0
        if suivi:
            subprocess.run(["git", "mv", str(src.relative_to(RACINE)),
                            str(dest.relative_to(RACINE))], cwd=RACINE, check=True)
        else:
            src.rename(dest)
        print(f"monolithe archivé : {dest.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

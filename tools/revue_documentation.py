#!/usr/bin/env python3
"""revue_documentation.py — LA REVUE DE FIN DE SOUS-CHANTIER (AGENTS.md §4).

Ce qu'elle vérifie, et qu'il faut corriger AVANT le commit de clôture :
  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
     ment pas sur la cible ; les sources externes sont citées ;
  4. fraîcheur  : en-cours.md date du dernier commit (comparaison réelle, pas de format) ;
  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
  6. vocabulaire : « jeton » ne désigne **jamais** la représentation sémantique neutre (RSN) ;
  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
     ne pointe vers un fichier absent (hors gabarits `AAAA`, `<...>`, `*`).

Sortie : un rapport lisible, code 0 si tout passe, 1 sinon (utilisable comme porte).
"""
from __future__ import annotations
import pathlib, re, subprocess, sys
import xml.etree.ElementTree as ET
from datetime import date

RACINE = pathlib.Path(__file__).resolve().parent.parent
GABARIT = ("<", "*", "AAAA", "...")
CHEMIN = re.compile(
    r"`((?:docs|reports|tools|journal|data|drave-core|sprints)/"
    r"[^`\s]+?\.(?:md|json|sh|py|rs|txt|svg|csv|jsonl))`"
)


def liens(texte: str):
    return re.findall(r"\]\(([^)#]+?)\)", texte)


def date_dernier_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--format=%ad", "--date=short"], cwd=RACINE, text=True
        ).strip()
    except Exception:
        return ""


def date_dernier_changement(chemin: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", chemin],
            cwd=RACINE, text=True,
        ).strip()
    except Exception:
        return ""


def docs_vivants():
    return [p for p in (RACINE / "docs").rglob("*.md")
            if "archive" not in p.parts and p.name != "README.md"]


def docs_tous():
    return list((RACINE / "docs").rglob("*.md"))


def rapports():
    return list((RACINE / "reports").glob("*.md"))


def sources_nav():
    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins)."""
    return (docs_vivants() + rapports()
            + [RACINE / "docs/README.md", RACINE / "README.md",
               RACINE / "REPRISE.md", RACINE / "AGENTS.md"])


def sources_propres():
    """Les documents vivants dont on vérifie les libellés et les chemins en code inline."""
    return (docs_vivants()
            + [RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])


def sources_liens():
    """Les fichiers dont les liens doivent résoudre (docs, fiches courantes, racine)."""
    return (docs_tous()
            + [RACINE / "reports/07-mesures-couche-commune.md",
               RACINE / "reports/fiche-nuit-17-10.md",
               RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])


def compte_portes() -> int:
    return len(list((RACINE / "tools").glob("porte-*.sh")))


def compte_chapitres() -> int:
    return len(list((RACINE / "docs/synthese").glob("0*.md")))


def compte_fiches() -> int:
    return len(rapports())


def compte_json() -> int:
    return len(list((RACINE / "reports").glob("*.json")))


def compte_docs() -> int:
    return len(docs_vivants())


def extrait_entier(texte: str, motif: str):
    m = re.search(motif, texte)
    return int(m.group(1)) if m else None


def main() -> int:
    alertes: list[str] = []
    en = RACINE / "docs/en-cours.md"
    if not en.exists():
        print("✗ docs/en-cours.md absent")
        return 1
    t = en.read_text()

    # 2. les sept chantiers
    ids = sorted(set(re.findall(r"\*\*(C[1-7])\*\*", t)))
    if len(ids) < 7:
        alertes.append(f"structure : {len(ids)} chantiers sur 7 dans en-cours.md ({ids})")

    # 4. fraîcheur : la date de la page doit être celle du dernier commit
    m = re.search(r"Mis à jour : (\d{4}-\d\d-\d\d)", t)
    if not m:
        alertes.append("fraîcheur : en-cours.md n'a pas de date « Mis à jour : AAAA-MM-JJ »")
    else:
        page, dernier = m.group(1), date_dernier_commit()
        if dernier and page != dernier:
            alertes.append(
                f"fraîcheur : en-cours.md dit {page}, le dernier commit date du {dernier}"
            )

    # 1. classement : aucune donnée de résultat dans docs/
    for f in (RACINE / "docs").rglob("*"):
        if f.suffix in (".json", ".csv", ".npz", ".jsonl") and f.is_file():
            alertes.append(f"classement : donnée de résultat dans docs/ → {f.relative_to(RACINE)}")
    for nom in ("07-mesures-couche-commune.md", "fiche-nuit-17-10.md"):
        if not (RACINE / "reports" / nom).exists():
            alertes.append(f"classement : la fiche courante reports/{nom} manque")
    if not (RACINE / "reports/README.md").exists():
        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")

    # 5. compteurs : la page d'état est la source unique, et elle dit le disque
    portes = extrait_entier(t, r"\|\s*portes\s*\|\s*\*\*(\d+)\*\*")
    chapitres = extrait_entier(t, r"\|\s*chapitres de la synthèse\s*\|\s*\*\*(\d+)\*\*")
    documents = extrait_entier(t, r"\|\s*documents de[^|]*\|\s*\*\*(\d+)\*\*")
    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
    for nom, valeur, disque in (
        ("portes", portes, compte_portes()),
        ("chapitres", chapitres, compte_chapitres()),
        ("documents", documents, compte_docs()),
    ):
        if valeur is None:
            alertes.append(f"compteurs : la ligne « {nom} » manque dans en-cours.md")
        elif valeur != disque:
            alertes.append(f"compteurs : en-cours.md dit {valeur} {nom}, le disque en a {disque}")
    if not fiches:
        alertes.append("compteurs : la ligne « fichiers / JSON » manque dans en-cours.md")
    else:
        for valeur, disque, quoi in (
            (int(fiches.group(1)), compte_fiches(), "fichiers"),
            (int(fiches.group(2)), compte_json(), "JSON"),
        ):
            if valeur != disque:
                alertes.append(
                    f"compteurs : en-cours.md dit {valeur} {quoi}, le disque en a {disque}"
                )

    # 3. annotation : les liens résolvent, et leur libellé ne ment pas sur la cible
    for f in sources_liens():
        try:
            texte = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for cible in liens(texte):
            if cible.startswith(("http://", "https://", "mailto:")):
                continue
            p = (f.parent / cible).resolve()
            if not p.exists():
                alertes.append(f"annotation : {f.relative_to(RACINE)} → {cible} (cassé)")
    for f in sources_propres():
        try:
            texte = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for label, cible in re.findall(r"\[([^\]]+)\]\(([^)#]+?)\)", texte):
            if cible.startswith(("http://", "https://", "mailto:")):
                continue
            lab = label.strip("`")
            if not (re.match(r"^(docs|reports|tools|journal)/", lab)
                    and lab.endswith((".md", ".json", ".sh"))):
                continue
            p = (f.parent / cible).resolve()
            lp = (RACINE / lab).resolve()
            if p.exists() and lp != p:
                alertes.append(
                    f"libellé : {f.relative_to(RACINE)} annonce « {lab} » mais pointe {cible}"
                )

    # 7a. chemins morts en code inline (hors gabarits)
    for f in sources_propres():
        try:
            brut = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        texte = re.sub(r"\[[^\]]+\]\([^)]+\)", "", brut)
        for m in CHEMIN.finditer(texte):
            p = m.group(1).rstrip(".,;:)")
            if any(g in p for g in GABARIT):
                continue
            if not (RACINE / p).exists():
                ligne = texte[: m.start()].count("\n") + 1
                alertes.append(f"chemin mort : {f.relative_to(RACINE)}:{ligne} → {p}")

    # 7b. orphelins : tout document vivant doit avoir au moins un lien entrant
    entrants: set[pathlib.Path] = set()
    for f in sources_nav():
        try:
            texte = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for cible in liens(texte):
            if cible.startswith(("http://", "https://", "mailto:")):
                continue
            p = (f.parent / cible).resolve()
            if p.suffix == ".md":
                entrants.add(p)
    for p in docs_vivants():
        if p.resolve() not in entrants:
            alertes.append(f"navigation : {p.relative_to(RACINE)} n'a aucun lien entrant")

    # 7c. documents datés : une date de vérification, et pas trop vieille
    for f in docs_vivants():
        try:
            tete = f.read_text(encoding="utf-8", errors="ignore")[:900]
        except OSError:
            continue
        if "> **Document daté." not in tete:
            continue
        m = re.search(r"Dernière vérification : (\d{4}-\d\d-\d\d)", tete)
        if not m:
            alertes.append(
                f"dates : {f.relative_to(RACINE)} est daté sans « Dernière vérification : AAAA-MM-JJ »"
            )
            continue
        try:
            age = (date.today() - date.fromisoformat(m.group(1))).days
        except ValueError:
            alertes.append(f"dates : {f.relative_to(RACINE)} a une date invalide ({m.group(1)})")
            continue
        if age > 90:
            alertes.append(
                f"dates : {f.relative_to(RACINE)} vérifié il y a {age} jours (> 90) — archiver ou revoir"
            )

    # 6. vocabulaire : « jeton » ne désigne jamais la RSN
    for f in (RACINE / "docs").rglob("*.md"):
        if f.name == "glossaire.md" or f.parent.name == "glossaire":
            continue
        for m in re.finditer(r"jeton[s]?\s+(sémantique|de sens|neutre)", f.read_text(), re.I):
            alertes.append(
                f"vocabulaire : {f.relative_to(RACINE)} → « {m.group(0)} » "
                "(la RSN est en unités de sens ; le jeton est technique)"
            )

    # 5bis. cohérence de la synthèse : huit chapitres, chapitres 7-8, B10–B12
    idx = RACINE / "docs/synthese/index.md"
    if idx.exists():
        it = idx.read_text()
        if "Huit chapitres" not in it:
            alertes.append("cohérence : l'index ne dit pas « Huit chapitres »")
        for cible in (
            "07-modeles-alternatifs-entree-sortie.md",
            "08-les-operations.md",
            "B10", "B11", "B12",
        ):
            if cible not in it:
                alertes.append(f"cohérence : l'index ne mentionne pas {cible}")

        # 5ter. la synthèse est une introduction tenue à jour
        syn = RACINE / "docs/synthese"
        chapitres = sorted(syn.glob("0*.md"))
        for p in chapitres:
            if p.name not in it:
                alertes.append(f"synthèse : {p.name} n'est pas listé dans l'index")
            tete = p.read_text(encoding="utf-8", errors="ignore")[:2500]
            if "**Fiche concept" not in tete:
                alertes.append(f"synthèse : {p.name} n'a pas de fiche concept en tête")
            if "../glossaire/" not in tete:
                alertes.append(f"synthèse : {p.name} n'a pas de lien glossaire dans sa fiche")
            if "![" not in tete:
                alertes.append(f"synthèse : {p.name} n'a pas d'illustration dans sa fiche")
        m = re.search(r"Dernière mise à jour : (\d{4}-\d\d-\d\d)", it)
        if not m:
            alertes.append("synthèse : l'index n'a pas de « Dernière mise à jour »")
        else:
            dernier = date_dernier_changement("docs/synthese")
            if dernier and m.group(1) < dernier:
                alertes.append(f"synthèse : index daté {m.group(1)}, dernier changement {dernier}")
        n = len(list((syn / "schemas").glob("*.svg")))
        mots = {
            1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq", 6: "six",
            7: "sept", 8: "huit", 9: "neuf", 10: "dix", 11: "onze", 12: "douze",
            13: "treize", 14: "quatorze", 15: "quinze",
        }
        forme = mots.get(n, str(n))
        if f"{forme} schémas" not in it:
            alertes.append(f"synthèse : l'index ne dit pas « {forme} schémas » ({n} fichiers)")
        utilisees: set[pathlib.Path] = set()
        for p in [idx] + chapitres:
            txt = p.read_text(encoding="utf-8", errors="ignore")
            for im in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', txt):
                c = im.group(1)
                if c.startswith(("/", "http://", "https://")):
                    alertes.append(f"synthèse : image non relative dans {p.name} → {c}")
                    continue
                cible = (p.parent / c).resolve()
                if not cible.exists():
                    alertes.append(f"synthèse : image absente dans {p.name} → {c}")
                else:
                    utilisees.add(cible)
        for s in (syn / "schemas").glob("*.svg"):
            if s.resolve() not in utilisees:
                alertes.append(f"synthèse : schéma non référencé → {s.name}")
            try:
                ET.parse(s)
            except Exception as e:
                alertes.append(f"synthèse : SVG invalide {s.name} ({e})")

    print(f"  revue de documentation · {compte_fiches()} fiche(s) · {compte_json()} JSON · "
          f"{compte_docs()} doc(s) · {compte_portes()} porte(s) · {compte_chapitres()} chapitre(s)")
    if not alertes:
        print("  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, "
              "cohérence, vocabulaire, navigation")
        return 0
    print(f"  ❌ {len(alertes)} anomalie(s) :")
    for a in alertes:
        print(f"     · {a}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""verifier_liens_faq.py — les liens de la FAQ produit et de son sommaire.

Tâche **E1** : la FAQ (D3) vit dans `docs/produit/README.md` § 8. Ce vérificateur
contrôle trois choses :

  1. le **sommaire** du document : chaque entrée pointe vers un titre qui existe
     (ancre GitHub), et la ligne **8. FAQ** y est ;
  2. les **liens de la section § 8** : chaque fichier cité existe ;
  3. la **ligne FAQ de `docs/README.md`** : elle existe et son ancre est valide.

Il vérifie aussi que le **contenu des réponses n'a pas bougé** : l'empreinte sha256
de la section § 8 doit rester celle de D3. Le contrôle négatif injecte un lien de
fichier mort et une ancre morte : le vérificateur doit les détecter, sinon il ne
prouverait rien.

Usage :
    python3 tools/verifier_liens_faq.py            # résumé lisible
    python3 tools/verifier_liens_faq.py --json     # le JSON de reports/faq-sommaire.json
    python3 tools/verifier_liens_faq.py --autotest # vérifie que le négatif est détecté
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent
DOC = RACINE / "docs/produit/README.md"
README_DOCS = RACINE / "docs/README.md"
DATE = "2026-11-15"

#: L'empreinte de la section § 8 au moment de D3 (2026-11-15), avant E1.
SHA256_FAQ_D3 = "8855b475faef9079ecadcf9f5426cca62965160403f5542ecc1bc209e6912364"

#: Le budget de `docs/README.md` (T1, `tools/taille_documents.py`).
BUDGET_DOCS_README = 1000

LIEN = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
TITRE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.M)


def slug(titre: str) -> str:
    """L'ancre GitHub d'un titre (minuscules, ponctuation retirée, espaces → tirets)."""
    s = titre.strip().lower()
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE)
    return s.replace(" ", "-")


def ancres(texte: str) -> set[str]:
    """Les ancres des titres d'un document, doublons suffixés -1, -2 comme GitHub."""
    vues: dict[str, int] = {}
    sortie: set[str] = set()
    for m in TITRE.finditer(texte):
        base = slug(m.group(2))
        n = vues.get(base, 0)
        vues[base] = n + 1
        sortie.add(base if n == 0 else f"{base}-{n}")
    return sortie


def section(texte: str, debut: str, fin: str) -> str:
    i = texte.index(debut)
    j = texte.index(fin, i + len(debut))
    return texte[i:j]


def inspecter(texte: str, base: pathlib.Path, doc_texte: str | None = None) -> list[dict]:
    """Inspecte chaque lien du bloc ; rend un dict par lien (ok = fichier + ancre).

    `doc_texte` est le document complet, pour résoudre les ancres seules (`#...`) :
    l'ancre d'un lien du sommaire vise le document, pas le bloc de sommaire.
    """
    resultats = []
    for libelle, cible in LIEN.findall(texte):
        if cible.startswith(("http://", "https://", "mailto:")):
            continue
        chemin, _, ancre = cible.partition("#")
        p = (base / chemin).resolve() if chemin else None
        fichier_ok = p.exists() if p is not None else True
        ancre_ok = True
        if ancre:
            support = (p.read_text(encoding="utf-8", errors="ignore") if p is not None
                       else (doc_texte if doc_texte is not None else texte))
            ancre_ok = ancre in ancres(support)
        resultats.append({
            "libelle": libelle.strip("`"),
            "cible": cible,
            "fichier": str(p.relative_to(RACINE)) if p is not None and p.exists() else
                       (str(p) if p is not None else ""),
            "fichier_ok": fichier_ok,
            "ancre": ancre,
            "ancre_ok": ancre_ok,
            "ok": fichier_ok and ancre_ok,
        })
    return resultats


def controle_negatif() -> dict:
    """Deux liens faux doivent être rejetés : un fichier absent, une ancre absente."""
    faux = (
        "## 8. FAQ — contrôle négatif\n\n"
        "[fiche morte](../../reports/rapport-e1-inexistant.md)\n"
        "[ancre morte](#section-qui-nexiste-pas)\n"
        "[lien valide](README.md#8-faq--dix-questions)\n"
    )
    liens = inspecter(faux, DOC.parent, faux)
    morts = [l for l in liens if not l["ok"]]
    detecte = len(liens) == 3 and len(morts) == 2 and any(l["ok"] for l in liens)
    return {
        "liens_injectes": [
            {"cible": "../../reports/rapport-e1-inexistant.md", "attendu": "fichier absent"},
            {"cible": "#section-qui-nexiste-pas", "attendu": "ancre absente"},
            {"cible": "README.md#8-faq--dix-questions", "attendu": "lien valide conservé"},
        ],
        "detectes": [l["cible"] for l in morts],
        "detecte": detecte,
    }


def principal() -> dict:
    texte = DOC.read_text(encoding="utf-8")
    sommaire = section(texte, "## Sommaire", "## 1.")
    faq = section(texte, "## 8. FAQ", "## 9.")

    liens_sommaire = inspecter(sommaire, DOC.parent, texte)
    ancres_sommaire = [l for l in liens_sommaire if l["ancre"]]
    faq_dans_sommaire = any(l["ancre"] == "8-faq--dix-questions" for l in ancres_sommaire)

    liens_faq = inspecter(faq, DOC.parent, texte)

    readme = README_DOCS.read_text(encoding="utf-8")
    cible_readme = "produit/README.md#8-faq--dix-questions"
    ligne_readme = cible_readme in readme
    # La ligne est vérifiée comme un lien ordinaire, avec la même règle d'ancre.
    liens_readme = inspecter(f"[FAQ]({cible_readme})", README_DOCS.parent, readme)
    ligne_readme_ok = ligne_readme and liens_readme[0]["ok"]

    sha = hashlib.sha256(faq.encode("utf-8")).hexdigest()
    inchangee = sha == SHA256_FAQ_D3

    mots = len(re.findall(r"\S+", readme))
    budget_ok = mots <= BUDGET_DOCS_README

    sommaire_ok = bool(ancres_sommaire) and all(l["ok"] for l in ancres_sommaire)
    faq_ok = bool(liens_faq) and all(l["ok"] for l in liens_faq)
    negatif = controle_negatif()

    rapport = {
        "schema": "drave.faq.sommaire.liens",
        "version": 1,
        "date": DATE,
        "tache": "E1",
        "document": "docs/produit/README.md",
        "sommaire": {
            "trouve": "## Sommaire" in texte,
            "entrees": len(liens_sommaire),
            "ancres": len(ancres_sommaire),
            "mortes": sum(1 for l in ancres_sommaire if not l["ok"]),
            "faq_dans_sommaire": faq_dans_sommaire,
            "ligne_faq": "#8-faq--dix-questions",
            "details": liens_sommaire,
        },
        "section_8": {
            "liens": len(liens_faq),
            "morts": sum(1 for l in liens_faq if not l["ok"]),
            "details": liens_faq,
            "sha256": sha,
            "sha256_d3": SHA256_FAQ_D3,
            "inchangee": inchangee,
        },
        "docs_readme": {
            "ligne_faq": ligne_readme,
            "cible": cible_readme,
            "ancre_valide": bool(liens_readme[0]["ok"]),
            "mots": mots,
            "budget": BUDGET_DOCS_README,
            "budget_ok": budget_ok,
        },
        "controle_negatif": negatif,
        "ok": (sommaire_ok and faq_dans_sommaire and faq_ok and inchangee
               and ligne_readme_ok and budget_ok and negatif["detecte"]),
    }
    return rapport


def _resume(r: dict) -> str:
    s = r["sommaire"]
    f = r["section_8"]
    d = r["docs_readme"]
    return "\n".join([
        f"Sommaire — {s['ancres']} ancre(s), {s['mortes']} morte(s) · "
        f"FAQ listée : {'oui' if s['faq_dans_sommaire'] else 'non'}",
        f"Section § 8 — {f['liens']} lien(s), {f['morts']} mort(s) · "
        f"contenu inchangé : {'oui' if f['inchangee'] else 'NON'}",
        f"docs/README — ligne FAQ : {'oui' if d['ligne_faq'] else 'non'} · "
        f"{d['mots']}/{d['budget']} mots",
        f"Contrôle négatif : {'détecté' if r['controle_negatif']['detecte'] else 'NON DÉTECTÉ'}",
        "✅ liens et sommaire vérifiés" if r["ok"] else "❌ liens ou sommaire non vérifiés",
    ])


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--json", action="store_true",
                         help="le JSON de reports/faq-sommaire.json")
    parseur.add_argument("--autotest", action="store_true",
                         help="vérifie que le contrôle négatif échoue bien")
    args = parseur.parse_args(argv)
    if args.autotest:
        negatif = controle_negatif()
        ok = negatif["detecte"] is True
        print("✅ autotest : les deux liens faux sont rejetés" if ok
              else "❌ autotest : le contrôle négatif ne détecte rien")
        return 0 if ok else 1
    rapport = principal()
    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=1))
    else:
        print(_resume(rapport))
    return 0 if rapport["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

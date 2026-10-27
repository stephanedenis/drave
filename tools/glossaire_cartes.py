#!/usr/bin/env python3
"""glossaire_cartes.py — une fiche par entrée de glossaire, un index, un manifeste.

Le glossaire est découpé en **11 familles** (les définitions longues). Ce script en extrait
les **entrées** et génère :

  - `docs/glossaire/entrees/<slug>.md` : une **fiche courte** (titre, résumé, famille,
    lien vers la définition complète) — c'est l'unité que docwatch peut afficher en contexte ;
  - `docs/glossaire/README.md` : l'**index** groupé par famille, avec un lien direct par entrée ;
  - `docs/glossaire/index.json` : le **manifeste** (slug, terme, famille, fichier, fiche, résumé)
    pour la résolution côté docwatch.

Les familles restent la source des définitions : une fiche est une **carte**, pas une copie.
Après une modification d'une famille, relancer :

    python3 tools/glossaire_cartes.py

Options :
  --pilote   ne générer que les entrées du pilote (les autres fiches restent absentes) ;
  --force    réécrire une fiche même si elle ne porte pas le marqueur de génération ;
  --seche    afficher le compte sans écrire.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import unicodedata
from datetime import date

RACINE = pathlib.Path(__file__).resolve().parent.parent
GLOSS = RACINE / "docs" / "glossaire"
ENTREES = GLOSS / "entrees"
FAMILLES = [
    "01-le-projet-ses-noms-sa-methode.md",
    "02-modeles-et-architectures.md",
    "03-formats-quantification-encodage.md",
    "04-le-moteur-drave-execution-structures-out.md",
    "05-flux-protocole-et-transport.md",
    "06-repartition-materiel-et-energie.md",
    "07-mesure-qualite-et-methode-experimentale.md",
    "10-le-pont-linguistico-semantique-le-vocabu.md",
]
ANNEXES = [
    ("8. Points relevés", "08-points-releves-non-corriges.md"),
    ("9. Sources externes", "09-sources-externes-citees.md"),
    ("11. Sources du § 10", "11-sources-externes-ajoutees-par-le-10.md"),
]
PILOTE = [
    "état", "région", "bus", "porte", "mode", "faculté", "contrôle négatif",
    "RSN", "unité de sens", "jeton", "pont", "plan", "opérateur", "grappe",
    "perplexité", "couche", "étage", "tokeniseur", "résidu", "tête",
]


def slugify(terme: str) -> str:
    base = terme.split("(")[0]
    base = unicodedata.normalize("NFKD", base)
    base = "".join(c for c in base if not unicodedata.combining(c))
    base = base.lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    return base or "entree"


def nettoyer(terme: str) -> str:
    return re.sub(r"[*`_]", "", terme).strip()


def titre_famille(texte: str) -> str:
    for ligne in texte.splitlines():
        if ligne.startswith("# "):
            return ligne[2:].strip()
    return "Glossaire"


def premier_paragraphe(body: list[str]) -> str:
    morceaux = []
    for ligne in body:
        if not ligne.strip():
            break
        if ligne.startswith("**Où**") or ligne.startswith("**Réf.**"):
            break
        morceaux.append(ligne.strip())
    return " ".join(morceaux)


def resume(body: list[str]) -> str:
    par = premier_paragraphe(body)
    par = re.sub(r"\s+", " ", par).strip()
    # deux premières phrases, puis 60 mots au plus
    phrases = re.split(r"(?<=[.!?])\s+", par)
    court = " ".join(phrases[:2]).strip()
    mots = court.split()
    if len(mots) > 60:
        court = " ".join(mots[:60]) + "…"
    return court or par[:240] or "Voir la définition dans la famille."


def parser_famille(chemin: pathlib.Path):
    texte = chemin.read_text(encoding="utf-8", errors="ignore")
    famille = titre_famille(texte)
    lignes = texte.splitlines()
    est_10 = chemin.name.startswith("10-")
    entrees = []
    courante = None
    for ligne in lignes:
        if est_10:
            m = re.match(r"^> \*\*([^*]+)\*\*.*[—–-]", ligne)
            if m:
                if courante:
                    entrees.append(courante)
                reste = re.split(r"[—–]", ligne[2:], maxsplit=1)
                corps = [reste[1].strip()] if len(reste) > 1 else [ligne[2:].strip()]
                courante = {"terme": nettoyer(m.group(1)), "body": corps}
                continue
            if courante:
                if ligne.startswith("> "):
                    courante["body"].append(ligne[2:].strip())
                elif ligne == ">":
                    courante["body"].append("")
                elif ligne.strip() == "":
                    entrees.append(courante)
                    courante = None
                elif ligne.startswith("#"):
                    entrees.append(courante)
                    courante = None
                else:
                    entrees.append(courante)
                    courante = None
            continue
        m = re.match(r"^\*\*([^*]+)\*\*\s*(?:\*\([^)]*\)\*\s*)?[—–-]\s*(.*)$", ligne)
        if m:
            if courante:
                entrees.append(courante)
            courante = {"terme": nettoyer(m.group(1)), "body": [m.group(2).strip()]}
            continue
        if courante:
            if ligne.startswith(("## ", "### ", "---")):
                entrees.append(courante)
                courante = None
            else:
                courante["body"].append(ligne)
    if courante:
        entrees.append(courante)
    for e in entrees:
        e["famille"] = famille
        e["fichier"] = chemin.name
    return [e for e in entrees if e["terme"] and e["body"]]


def construire():
    toutes = []
    vus = {}
    for nom in FAMILLES:
        p = GLOSS / nom
        if not p.exists():
            continue
        for e in parser_famille(p):
            if not re.search(r"[A-Za-zÀ-ÿ]", e["terme"]):
                continue
            base = slugify(e["terme"])
            slug = base
            n = 2
            while slug in vus:
                slug = f"{base}-{n}"
                n += 1
            vus[slug] = True
            e["slug"] = slug
            e["resume"] = resume(e["body"])
            e["resume"] = e["resume"][:1].upper() + e["resume"][1:]
            toutes.append(e)
    return toutes


def carte(e: dict) -> str:
    return f"""<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# {e['terme']}

> **Fiche glossaire — {e['terme']}.** {e['resume']}
>
> **Famille :** [{e['famille']}](../{e['fichier']}) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../{e['fichier']})
"""


def lien(e: dict) -> str:
    cible = ENTREES / f"{e['slug']}.md"
    if cible.exists():
        return f"[{e['terme']}](entrees/{e['slug']}.md)"
    return e['terme']


def index(toutes: list[dict]) -> str:
    lignes = [
        "# L'index des entrées du glossaire",
        "",
        "> **Ce que ce fichier est.** L'index **généré** des entrées du glossaire : une ligne par",
        "> entrée, groupée par famille, avec un lien direct vers sa **fiche** courte. Les définitions",
        "> complètes restent dans les 11 familles ; le manifeste [`index.json`](index.json) sert à",
        "> docwatch pour afficher une fiche en contexte.",
        "> **Chargement :** T1 — ouvrir la fiche du terme, pas les 11 familles.",
        "> **Pour docwatch.** Charger `index.json`, résoudre un terme par `slug`, puis rendre la fiche",
        "> **Vérifier.** `python3 tools/glossaire_cartes.py --verifier` compare les fiches,",
        "> l'index et le manifeste ; après une modification d'une famille, relancer le générateur.",
        "> `entrees/<slug>.md` en carte ; `resume` permet le survol sans lire le fichier.",
        "",
        f"**{len(toutes)} entrées.** Index général : [le glossaire](../glossaire.md).",
        "",
    ]
    familles = {}
    for e in toutes:
        familles.setdefault((e["famille"], e["fichier"]), []).append(e)
    for (famille, fichier), entrees in familles.items():
        lignes.append(f"### {famille} · [la famille]({fichier})")
        liens = [lien(e) for e in sorted(entrees, key=lambda x: x["terme"].casefold())]
        lignes.append(" · ".join(liens))
        lignes.append("")
    lignes.append("## Les annexes")
    for titre, fichier in ANNEXES:
        lignes.append(f"- [{titre}]({fichier}) — pas d'entrée de terme, une annexe.")
    lignes.append("")
    return "\n".join(lignes)


def manifeste(toutes: list[dict]) -> str:
    data = {
        "genere": date.today().isoformat(),
        "entrees": [
            {
                "slug": e["slug"],
                "terme": e["terme"],
                "famille": e["famille"],
                "fichier": e["fichier"],
                "fiche": (f"entrees/{e['slug']}.md" if (ENTREES / f"{e['slug']}.md").exists() else None),
                "resume": e["resume"],
            }
            for e in toutes
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilote", action="store_true", help="ne générer que les fiches du pilote")
    ap.add_argument("--force", action="store_true", help="réécrire même sans marqueur de génération")
    ap.add_argument("--seche", action="store_true", help="afficher le compte sans écrire")
    ap.add_argument("--verifier", action="store_true", help="vérifier sans écrire")
    args = ap.parse_args()

    toutes = construire()
    if args.verifier:
        ecarts = []
        for chemin, attendu in (
            (GLOSS / "README.md", index(toutes)),
            (GLOSS / "index.json", manifeste(toutes)),
        ):
            if not chemin.exists() or chemin.read_text(encoding="utf-8") != attendu:
                ecarts.append(chemin.name)
        for e in toutes:
            cible = ENTREES / f"{e['slug']}.md"
            if cible.exists() and cible.read_text(encoding="utf-8") != carte(e):
                ecarts.append(cible.name)
        if ecarts:
            print(f"  ❌ {len(ecarts)} fichier(s) périmé(s) : {', '.join(ecarts[:12])}")
            return 1
        print(f"  ✅ {len(toutes)} entrées · fiches, index et manifeste à jour")
        return 0

    if args.seche:
        print(f"{len(toutes)} entrées, {len({e['slug'] for e in toutes})} slugs")
        for e in toutes[:12]:
            print(f"  {e['slug']:30s} {e['famille'][:30]:30s} {e['terme']}")
        return 0

    ENTREES.mkdir(parents=True, exist_ok=True)
    ecrites = 0
    for e in toutes:
        if args.pilote and not any(e["terme"].lower().startswith(p.lower()) for p in PILOTE):
            continue
        cible = ENTREES / f"{e['slug']}.md"
        if cible.exists() and "généré par tools/glossaire_cartes.py" not in cible.read_text(encoding="utf-8") and not args.force:
            print(f"  conservé (non généré) : {cible.name}")
            continue
        cible.write_text(carte(e), encoding="utf-8")
        ecrites += 1
    (GLOSS / "README.md").write_text(index(toutes), encoding="utf-8")
    (GLOSS / "index.json").write_text(manifeste(toutes), encoding="utf-8")
    print(f"  {len(toutes)} entrées · {ecrites} fiche(s) écrite(s) · index et manifeste à jour")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

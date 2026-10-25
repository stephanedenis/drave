#!/usr/bin/env python3
"""decoupage_familles.py — C3.2a : les articles UDHR, groupés par FAMILLE de langues.

POURQUOI. C3 (la restitution) est mesuré : 85,1 % de fragments exacts à une langue, puis
30 % → 4,4 % → 0,4 % → 0,6 % à 1/10/50/448 langues — la restitution exacte meurt entre
1 et 10 langues. La suite (C3.2) est de donner à chaque FAMILLE son module. Cet outil
prépare le matériau : un fichier d'articles par famille, et un index.

CE QU'IL LIT. `data/udhr/genealogie.json` (chaque langue → sa `famille`, 441 langues,
55 familles) et `data/udhr/articles_propres.jsonl` (un article par ligne, avec `iso3`).

CE QU'IL ÉCRIT. `data/udhr/familles/<slug>.jsonl` (les articles de la famille) et
`data/udhr/familles/index.json` (la famille, son slug, ses langues, ses comptes).

CE QU'IL NE FAIT PAS. Il ne vérifie pas que l'article N dit la même chose dans deux
langues — c'est la structure du corpus XML qui le garantit. Et il ne mesure rien : la
mesure (C3.2b/c) est `lora_recopie.py --ids <famille>` et la comparaison à la courbe.

Usage : python3 tools/decoupage_familles.py [--min-langues 2]
"""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import unicodedata
from collections import defaultdict

RACINE = pathlib.Path(__file__).resolve().parent.parent
UDHR = RACINE / "data" / "udhr"
SORTIE = UDHR / "familles"


def slug(texte: str) -> str:
    """Un nom de fichier sûr pour une famille (« Indo-European » → « indo-european »)."""
    t = unicodedata.normalize("NFD", texte.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "inconnue"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-langues", type=int, default=2,
                    help="ne garder que les familles d'au moins N langues (défaut 2)")
    a = ap.parse_args()

    genealogie = json.loads((UDHR / "genealogie.json").read_text(encoding="utf-8"))
    famille_de = {meta.get("iso3"): (meta.get("famille") or "inconnue")
                  for meta in genealogie.values()}
    noms = {meta.get("iso3"): meta.get("nom", meta.get("iso3"))
            for meta in genealogie.values()}

    familles: dict[str, dict] = defaultdict(lambda: {"langues": set(), "articles": []})
    total = 0
    for ligne in (UDHR / "articles_propres.jsonl").read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        art = json.loads(ligne)
        iso = art.get("iso3")
        fam = famille_de.get(iso) or "inconnue"
        familles[fam]["langues"].add(iso)
        familles[fam]["articles"].append(art)
        total += 1

    SORTIE.mkdir(parents=True, exist_ok=True)
    index = []
    for fam, d in sorted(familles.items(), key=lambda kv: -len(kv[1]["langues"])):
        if len(d["langues"]) < a.min_langues:
            continue
        nom = slug(fam)
        (SORTIE / f"{nom}.jsonl").write_text(
            "\n".join(json.dumps(art, ensure_ascii=False) for art in d["articles"]) + "\n",
            encoding="utf-8")
        index.append({
            "famille": fam, "slug": nom,
            "n_langues": len(d["langues"]), "n_articles": len(d["articles"]),
            "langues": sorted((iso, noms.get(iso, iso)) for iso in d["langues"]),
        })
    (SORTIE / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"  {len(index)} familles · {sum(i['n_langues'] for i in index)} langues · "
          f"{sum(i['n_articles'] for i in index)} / {total} articles")
    for i in index[:12]:
        print(f"    {i['n_langues']:4d} langues · {i['n_articles']:5d} articles · {i['famille']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

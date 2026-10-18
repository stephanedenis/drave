#!/usr/bin/env python3
"""genealogie_udhr.py — LA GÉNÉALOGIE DES 448 LANGUES (famille, branche), depuis Glottolog.

POURQUOI. Une couche entrée-sortie n'est pas « riche en langues » parce qu'elle en compte beaucoup : elle l'est si
elle couvre la **structure** — familles, branches, dialectes (cf. `docs/genealogie-des-langues.md`). Et les tests
doivent être **organisés par niveau** : une paire de langues sœurs n'est pas une paire de familles différentes.

LA SOURCE. Glottolog (CLDF, `glottolog/glottolog-cldf` sur GitHub) ✓ : `languages.csv` (27 000 languoïdes, avec
`Family_ID`, `Level`, `ISO639P3code`) et `values.csv` (dont la **classification** complète, « Indo-European > Italic
> Romance > … »). On télécharge une fois, on cache dans `data/glottolog/`.

SORTIE : `data/udhr/genealogie.json` — pour chaque fichier UDHR : `{iso3, famille, branche, glottocode, niveau}`.
⚠️ Ce que ce n'est pas ✗ : Glottolog donne la classification **savante**, pas la distance mesurée ; et certaines
langues UDHR ont un code qui n'est pas dans Glottolog ✗✓ (on le compte et on le dit ✓).
"""
from __future__ import annotations
import argparse, csv, json, pathlib, urllib.request

BASE = "https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/"


def telecharger(nom: str, cache: pathlib.Path) -> pathlib.Path:
    cache.mkdir(parents=True, exist_ok=True)
    f = cache / nom
    if not f.exists():
        urllib.request.urlretrieve(BASE + nom, f)
    return f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="data/glottolog")
    ap.add_argument("--sortie", default="data/udhr/genealogie.json")
    a = ap.parse_args()
    cache = pathlib.Path(a.cache)
    lang = telecharger("languages.csv", cache)
    val = telecharger("values.csv", cache)

    familles, niveaux, glotto = {}, {}, {}
    with lang.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("ISO639P3code"):
                familles[r["ISO639P3code"]] = r.get("Family_ID") or ""
                glotto[r["ISO639P3code"]] = r.get("Glottocode") or ""
                niveaux[r["ISO639P3code"]] = r.get("Level") or ""
    # la classification complète (chaîne « A > B > C ») ✓
    classif = {}
    with val.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("Parameter_ID") == "classification":
                classif[r["Language_ID"]] = r.get("Value") or ""
    # Family_ID → le nom de la famille (languoïde de niveau famille) ✓
    noms = {}
    with lang.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            noms[r["ID"]] = r.get("Name") or r["ID"]

    meta = json.loads(pathlib.Path("data/udhr/meta.json").read_text())
    out, manquants = {}, []
    for fichier, m in meta.items():
        iso = m["iso3"]
        fam_id = familles.get(iso, "")
        famille = noms.get(fam_id, fam_id) if fam_id else "(inconnue)"
        branche = classif.get(glotto.get(iso, ""), "")
        if not fam_id and not branche:
            manquants.append(iso)
        out[fichier] = {"iso3": iso, "nom": m["nom"], "script": m["script"],
                        "famille": famille, "branche": branche, "niveau": niveaux.get(iso, "")}
    pathlib.Path(a.sortie).write_text(json.dumps(out, ensure_ascii=False, indent=0))

    from collections import Counter
    fam = Counter(v["famille"] for v in out.values())
    print(f"  {len(out)} fichiers UDHR · {len(fam)} familles · {len(manquants)} sans classification ✗")
    print("  les plus grandes familles :")
    for nom, n in fam.most_common(10):
        print(f"    {nom:34s} {n:4d}")
    ex = next(iter(out.values()))
    print(f"\n  exemple : {ex['nom']} → {ex['branche'][:110]}")
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

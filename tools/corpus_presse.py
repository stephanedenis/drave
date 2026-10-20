#!/usr/bin/env python3
"""corpus_presse.py — LE CORPUS « QUOTIDIEN » : des communiqués de presse UE de 2026, alignés par paragraphe.

POURQUOI ✓✓. Le juridique (règlements UE) et le littéraire (Verne) sont mesurés ; le registre **quotidien** — la
presse, l'actualité, la langue de tous les jours — ne l'est pas ✗. Les communiqués de la Commission européenne sont
**traduits par des humains** dans les 24 langues ✓✓, publiés **après la coupure** des modèles (2026) ✓✓, et leur
structure est **la même** dans toutes les langues : le même nombre de paragraphes ✓✓ — l'alignement est donc
**garanti par la structure**, comme pour les règlements, mais dans un autre registre ✓✓.

LA SOURCE. L'API de la presse de la Commission (le site est une application ; le HTML ne contient pas le texte) ✓ :
  https://ec.europa.eu/commission/presscorner/api/documents?reference=IP/26/1900&language=EN
qui rend un JSON avec `docuLanguageResource.htmlContent` (le corps en HTML) et `docuLanguageResource.language` ✓.
⚠️ Une version **fraîche du jour** peut ne pas être encore traduite : l'API rend alors l'anglais même si l'on demande
`FR` ou `DE` ✗✓ — on vérifie donc `language` et l'égalité du nombre de paragraphes **avant** d'accepter ✓✓.

CE QUE L'OUTIL VÉRIFIE ✓✓ : les 15 communiqués ont EN, FR et DE **avec le même nombre de paragraphes** (7 à 23) ;
on n'apparie que les paragraphes présents partout, et on rapporte les longueurs relatives (fra/eng, deu/eng) ✓.
"""
from __future__ import annotations
import argparse, json, pathlib, urllib.request

REFERENCES = [
    "IP/26/1633", "IP/26/1654", "IP/26/1661", "IP/26/1710", "IP/26/1738",
    "IP/26/1829", "IP/26/1871", "IP/26/1920", "IP/26/1934", "IP/26/1941",
    "IP/26/1983", "IP/26/1990", "IP/26/2018", "IP/26/2039", "IP/26/2137",
]
LANGUES = ["EN", "FR", "DE"]


def telecharge(ref: str, langue: str, cache: pathlib.Path) -> dict | None:
    f = cache / f"{ref.replace('/', '_')}-{langue}.json"
    if f.exists():
        return json.loads(f.read_text())
    url = f"https://ec.europa.eu/commission/presscorner/api/documents?reference={ref}&language={langue}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (corpus Drave)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode("utf-8", "ignore"))
    except Exception:
        return None
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(d, ensure_ascii=False))
    return d


def paragraphes(d: dict) -> tuple[str, list[str]]:
    from lxml import html as LH
    r = d["docuLanguageResource"]
    ps = [" ".join(p.text_content().split()) for p in LH.fromstring(r["htmlContent"]).iter("p")]
    return r.get("title", "").strip(), [p for p in ps if p.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="data/presse/presse_2026.json")
    ap.add_argument("--cache", default="data/presse/api")
    a = ap.parse_args()
    cache = pathlib.Path(a.cache)
    docs, unites = [], []
    for ref in REFERENCES:
        textes = {}
        for lg in LANGUES:
            d = telecharge(ref, lg, cache)
            if not d or d.get("docuLanguageResource", {}).get("language") != lg:
                textes = {}
                break
            titre, ps = paragraphes(d)
            textes[lg] = {"titre": titre, "ps": ps, "date": d.get("eventDate")}
        if not textes:
            print(f"  ✗ {ref} : langue manquante"); continue
        n = {lg: len(textes[lg]["ps"]) for lg in LANGUES}
        if len(set(n.values())) != 1:
            print(f"  ✗ {ref} : {n} paragraphes — appariement impossible"); continue
        docs.append({"ref": ref, "date": textes["EN"]["date"], "n": n["EN"],
                     "titre_en": textes["EN"]["titre"]})
        for i in range(n["EN"]):
            unites.append({"id": f"{ref.replace('/', '_')}_p{i + 1}", "ref": ref,
                           "date": textes["EN"]["date"], "type": "paragraphe",
                           "textes": {lg: textes[lg]["ps"][i] for lg in LANGUES}})
        # le titre est une unité à part (traduit aussi) ✓
        unites.append({"id": f"{ref.replace('/', '_')}_titre", "ref": ref,
                       "date": textes["EN"]["date"], "type": "titre",
                       "textes": {lg: textes[lg]["titre"] for lg in LANGUES}})
        print(f"  ✓ {ref} {textes['EN']['date']} · {n['EN']} paragraphes · {textes['EN']['titre'][:60]}")
    # contrôle de longueur : des rapports aberrants signaleraient un mauvais appariement ✓✗
    for lg in ("FR", "DE"):
        ratios = sorted(len(u["textes"][lg]) / max(1, len(u["textes"]["EN"])) for u in unites)
        print(f"  longueur {lg}/EN : médiane {ratios[len(ratios) // 2]:.2f} · min {ratios[0]:.2f} · "
              f"max {ratios[-1]:.2f}")
    sortie = pathlib.Path(a.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps({"source": "Commission européenne, presse, 2026",
                                  "references": REFERENCES, "documents": docs, "langues": ["eng", "fra", "deu"],
                                  "unites": [{"id": u["id"], "ref": u["ref"], "date": u["date"],
                                              "type": u["type"], "textes": {"eng": u["textes"]["EN"],
                                                                            "fra": u["textes"]["FR"],
                                                                            "deu": u["textes"]["DE"]}}
                                             for u in unites]}, ensure_ascii=False, indent=1))
    print(f"  → {sortie} : {len(docs)} documents, {len(unites)} unités")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

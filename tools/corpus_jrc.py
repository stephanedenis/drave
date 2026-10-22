#!/usr/bin/env python3
"""corpus_jrc.py — extraire un sous-corpus **technique à référence humaine** de JRC-Acquis.

POURQUOI ✓✓. Le registre technique n'était mesuré que sur **WikiMatrix** (paires **minées**, bruitées). JRC-Acquis
est un corpus **parallèle humain** (la législation européenne traduite par des traducteurs) : on y filtre les
segments **techniques** (chimie, énergie, environnement, santé, sécurité) par mots-clés ✓✓.

CE QU'ON GARDE ✓✓ : 30-300 caractères, marqueurs FR/EN, similarité < 0,4, et **au moins deux mots-clés techniques**
dans le segment anglais ✓✓.
"""
from __future__ import annotations
import argparse, gzip, json, pathlib, random, re
import xml.etree.ElementTree as ET

XML = "{http://www.w3.org/XML/1998/namespace}lang"
FR = (" le ", " la ", " les ", " de ", " des ", " est ", " une ", " un ", " pour ", " dans ", " que ", " qui ",
      " avec ", " sur ", " au ", " du ")
EN = (" the ", " of ", " and ", " to ", " is ", " in ", " that ", " for ", " with ", " on ", " by ", " as ",
      " was ", " are ")
TECH = ("chemical", "substance", "emission", "energy", "environment", "radiation", "waste", "fuel", "gas",
        "water", "air", "soil", "plant", "animal", "health", "safety", "product", "material", "equipment",
        "technology", "research", "scientific", "measurement", "quality", "standard", "limit", "concentration",
        "toxic", "hazardous", "pollution", "climate")


def _marqueurs(t, mots):
    t = " " + t.lower() + " "
    return sum(m in t for m in mots) >= 2


def _jaccard6(a, b):
    A = {a[i:i + 6] for i in range(max(0, len(a) - 5))}
    B = {b[i:i + 6] for i in range(max(0, len(b) - 5))}
    return len(A & B) / max(1, len(A | B))


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tmx", default="data/jrc/en-fr.tmx.gz")
    ap.add_argument("--n", type=int, default=800)
    ap.add_argument("--candidats", type=int, default=20000)
    ap.add_argument("--sortie", default="data/jrc/jrc_tech_fr_en.json")
    a = ap.parse_args()
    paires, vus = [], set()
    with gzip.open(a.tmx, "rb") as f:
        for _, elem in ET.iterparse(f, events=("end",)):
            if elem.tag != "tu":
                continue
            segs = {}
            for tuv in elem:
                if tuv.tag == "tuv":
                    seg = tuv.find("seg")
                    if seg is not None and seg.text:
                        segs[tuv.get(XML) or tuv.get("lang")] = re.sub(r"\s+", " ", seg.text).strip()
            if "en" in segs and "fr" in segs:
                en, fr = segs["en"], segs["fr"]
                if (30 <= len(en) <= 300 and 30 <= len(fr) <= 300 and 0.5 <= len(fr) / len(en) <= 2.0
                        and _marqueurs(fr, FR) and _marqueurs(en, EN) and _jaccard6(en, fr) < 0.4
                        and sum(k in en.lower() for k in TECH) >= 2):
                    if (en, fr) not in vus:
                        vus.add((en, fr)); paires.append({"en": en, "fr": fr})
            elem.clear()
            if len(paires) >= a.candidats:
                break
    rng = random.Random(1234); rng.shuffle(paires)
    paires = paires[:a.n]
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(paires, ensure_ascii=False, indent=0))
    print(f"  {len(paires)} paires JRC techniques → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())

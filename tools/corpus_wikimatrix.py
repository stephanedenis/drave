#!/usr/bin/env python3
"""corpus_wikimatrix.py — extraire un échantillon de **WikiMatrix** (paires Wikipedia minées) pour le registre technique.

POURQUOI ✓✓. Le registre **technique** manquait ; WikiMatrix est un corpus parallèle **miné** de Wikipédia (paires
de phrases EN/FR alignées par un modèle, pas par un traducteur) : il couvre les articles scientifiques et techniques
✓✓. Ce n'est pas une traduction humaine — c'est un **miné**, avec du bruit —, mais c'est le seul corpus technique
parallèle disponible sans construire un aligneur ✓✗.

CE QU'ON GARDE ✓✓ : les paires de 30 à 300 caractères, ratio de longueur 0,5-2, dédupliquées, échantillonnées avec
une graine fixe ✓✓.
"""
from __future__ import annotations
import argparse, gzip, json, pathlib, random, re
import xml.etree.ElementTree as ET

XML = "{http://www.w3.org/XML/1998/namespace}lang"


def _marqueurs(t, mots):
    t = " " + t.lower() + " "
    return sum(m in t for m in mots) >= 2


def _jaccard6(a, b):
    A = {a[i:i + 6] for i in range(max(0, len(a) - 5))}
    B = {b[i:i + 6] for i in range(max(0, len(b) - 5))}
    return len(A & B) / max(1, len(A | B))


FR = (" le ", " la ", " les ", " de ", " des ", " est ", " une ", " un ", " pour ", " dans ", " que ", " qui ",
      " avec ", " sur ", " au ", " du ")
EN = (" the ", " of ", " and ", " to ", " is ", " in ", " that ", " for ", " with ", " on ", " by ", " as ",
      " was ", " are ")


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tmx", default="data/wikimatrix/en-fr.tmx.gz")
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--candidats", type=int, default=20000)
    ap.add_argument("--sortie", default="data/wikimatrix/wikimatrix_fr_en.json")
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
                        and en.strip().lower() != fr.strip().lower()):
                    if (en, fr) not in vus:
                        vus.add((en, fr)); paires.append({"en": en, "fr": fr})
            elem.clear()
            if len(paires) >= a.candidats:
                break
    rng = random.Random(1234); rng.shuffle(paires)
    paires = paires[:a.n]
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(paires, ensure_ascii=False, indent=0))
    print(f"  {len(paires)} paires WikiMatrix → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())

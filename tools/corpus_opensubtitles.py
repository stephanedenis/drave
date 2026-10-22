#!/usr/bin/env python3
"""corpus_opensubtitles.py — extraire un échantillon de **OpenSubtitles** (sous-titres, dialogue parlé) EN/FR.

POURQUOI ✓✓. Le registre **dialogue spontané** manquait ; les sous-titres de films sont du **parlé conversationnel**
(interjections, phrases courtes, tours de parole), traduits par des humains ✓✓. C'est le dernier registre de la
carte (juridique, presse, littéraire, parlé préparé, technique miné, **dialogue**) ✓✓.

CE QU'ON GARDE ✓✓ : les répliques de 20 à 200 caractères, ratio 0,5-2, marqueurs de langue parlée, similarité
< 0,4, sans annotations techniques (`[MUSIC]`, `♪`, `--`) ✓✓.
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


FR = (" je ", " tu ", " vous ", " il ", " elle ", " on ", " est ", " pas ", " que ", " qui ", " pour ", " dans ",
      " avec ", " ça ", " moi ", " toi ", " mon ", " mais ")
EN = (" i ", " you ", " the ", " to ", " and ", " is ", " it ", " that ", " we ", " he ", " she ", " not ", " for ",
      " with ", " me ", " my ", " but ", " what ")
BRUIT = re.compile(r"\[[A-Z ]+\]|♪|^\s*--|^\s*\.\.\.|^\s*-\s*$")


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tmx", default="data/opensubtitles/en-fr.tmx.gz")
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--candidats", type=int, default=20000)
    ap.add_argument("--sortie", default="data/opensubtitles/opensubtitles_fr_en.json")
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
                if (20 <= len(en) <= 200 and 20 <= len(fr) <= 200 and 0.5 <= len(fr) / len(en) <= 2.0
                        and _marqueurs(fr, FR) and _marqueurs(en, EN) and _jaccard6(en, fr) < 0.4
                        and not BRUIT.search(en) and not BRUIT.search(fr)
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
    print(f"  {len(paires)} paires OpenSubtitles → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())

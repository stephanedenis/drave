#!/usr/bin/env python3
"""corpus_pidgin_bible.py — LA BIBLE PIDGIN : des milliers de paires narratives, verset par verset.

POURQUOI ✓✓. Les paires translatewiki sont **courtes et techniques** (mesure 95) ✗✗ ; il faut des paires
**narratives**. La **Bible en pidgin nigérian** (PCMWBT, 2019, Wycliffe) existe sur eBible en **USFM**, avec les
mêmes numéros de versets que la Bible anglaise (KJV) ✓✓ — l'alignement est **structurel** (livre, chapitre, verset)
✓✓. On construit les paires et on les ajoute à l'entraînement ✓✓.

⚠️ CE QUE CELA NE DIT PAS ✗ : la Bible est **ancienne** (contamination possible de l'anglais) et son registre est
**religieux** ✓✗ ; l'évaluation reste sur les **contes** tenus à part ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib, re, urllib.request, zipfile

UA = {"User-Agent": "Mozilla/5.0 (corpus Drave)"}


def telecharge(url: str, dest: pathlib.Path) -> pathlib.Path:
    if dest.exists() and dest.stat().st_size > 100_000:
        return dest
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())
    return dest


def parse_usfm(texte: str) -> dict[tuple[str, int, int], str]:
    out = {}
    livre = None; chapitre = None
    for ligne in texte.splitlines():
        m = re.match(r"\\id\s+([A-Z0-9]{3})", ligne)
        if m:
            livre = m.group(1); continue
        m = re.match(r"\\c\s+(\d+)", ligne)
        if m:
            chapitre = int(m.group(1)); continue
        m = re.match(r"\\v\s+(\d+)\s+(.*)", ligne)
        if m and livre and chapitre:
            verset = int(m.group(1))
            t = re.sub(r"\\[a-z]+\*?", " ", m.group(2))
            t = re.sub(r"\{[^}]*\}", " ", t)
            t = " ".join(t.split())
            if t:
                out[(livre, chapitre, verset)] = t
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="data/pidgin/bible.json")
    a = ap.parse_args()
    cache = pathlib.Path("data/pidgin")
    cache.mkdir(parents=True, exist_ok=True)
    pcm_zip = telecharge("https://ebible.org/Scriptures/pcm_usfm.zip", cache / "pcm_usfm.zip")
    en_zip = telecharge("https://ebible.org/Scriptures/eng-kjv_usfm.zip", cache / "eng_kjv_usfm.zip")
    def charge(z: pathlib.Path) -> dict:
        out = {}
        with zipfile.ZipFile(z) as zf:
            for nom in zf.namelist():
                if nom.lower().endswith(".usfm"):
                    out.update(parse_usfm(zf.read(nom).decode("utf-8", "ignore")))
        return out
    pcm = charge(pcm_zip); en = charge(en_zip)
    print(f"  pidgin {len(pcm)} versets · anglais {len(en)} versets")
    communs = sorted(set(pcm) & set(en))
    paires = [{"cle": f"{b}.{c}.{v}", "en": en[(b, c, v)], "pcm": pcm[(b, c, v)]}
              for (b, c, v) in communs if len(pcm[(b, c, v)]) > 10 and len(en[(b, c, v)]) > 10]
    pathlib.Path(a.sortie).write_text(json.dumps(paires, ensure_ascii=False, indent=0))
    print(f"  {len(paires)} paires alignées → {a.sortie}")
    print(f"  exemple : {paires[0] if paires else '—'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

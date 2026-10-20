#!/usr/bin/env python3
"""corpus_onu.py — LE CORPUS ONU 2026 : cinq langues, alignées par les paragraphes NUMÉROTÉS.

POURQUOI ✓✓. Le banc 24 langues (mesure 71) couvre les langues de l'Union ; il manque les **grandes langues
hors UE** — le chinois (2ᵉ langue du monde par le total de locuteurs, Ethnologue 2026) et le russe (11ᵉ) ✓✓. Les
résolutions de l'Assemblée générale de la **80ᵉ session** (septembre 2025 - 2026) sont **postérieures à la coupure**
des modèles ✓✓, **traduites par des humains** dans les six langues officielles ✓✓, et leurs **paragraphes du
dispositif sont numérotés** (1., 2., …) — l'alignement est donc **garanti par la structure**, comme pour les
règlements ✓✓.

LA SOURCE ✓✓. L'API des documents de l'ONU sert le PDF par symbole et par langue :
  https://documents.un.org/api/symbol/access?s=A/RES/80/1&l=en&t=pdf
puis `pdftotext -layout` → les paragraphes numérotés ✓✓.

⚠️ L'ARABE EST ÉCARTÉ ✗✗ : `pdftotext` rend le texte arabe **déchiqueté** (écriture de droite à gauche, ligatures),
et les numéros de paragraphe y apparaissent en fin de ligne (« 5 - ») ✓✗. L'arabe demandera une autre source ou un
autre extracteur ; on ne l'inclut pas pour ne pas fabriquer un alignement faux ✓✓.

CE QUE L'OUTIL VÉRIFIE ✓✓ : pour chaque résolution, les numéros forment une séquence **1..N contiguë** dans
**chaque** langue ; les textes sont non vides ; on rapporte les longueurs relatives (zh/en, ru/en, fr/en, es/en) ✓.
"""
from __future__ import annotations
import argparse, json, pathlib, re, subprocess, urllib.request

REFERENCES = ["A/RES/80/1", "A/RES/80/2", "A/RES/80/4", "A/RES/80/5", "A/RES/80/10"]
LANGUES = ["en", "fr", "es", "ru", "zh"]


def telecharge_pdf(ref: str, langue: str, cache: pathlib.Path) -> pathlib.Path | None:
    f = cache / f"{ref.replace('/', '_')}-{langue}.pdf"
    if f.exists() and f.stat().st_size > 10_000:
        return f
    url = f"https://documents.un.org/api/symbol/access?s={ref}&l={langue}&t=pdf"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (corpus Drave)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        if not data.startswith(b"%PDF"):
            return None
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(data)
        return f
    except Exception:
        return None


def texte_pdf(pdf: pathlib.Path) -> str:
    txt = pdf.with_suffix(".txt")
    if not txt.exists():
        subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return txt.read_text(encoding="utf-8", errors="ignore") if txt.exists() else ""


def paragraphes(texte: str) -> dict[int, str]:
    """Les paragraphes du dispositif : « N. » en début de ligne, jusqu'au suivant ✓."""
    marques = list(re.finditer(r"(?m)^\s*(\d{1,3})\.\s+", texte))
    out = {}
    for i, m in enumerate(marques):
        n = int(m.group(1))
        fin = marques[i + 1].start() if i + 1 < len(marques) else len(texte)
        corps = " ".join(texte[m.end():fin].split())
        if corps and n not in out:
            out[n] = corps
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="data/onu/onu_2026.json")
    ap.add_argument("--cache", default="data/onu/pdf")
    a = ap.parse_args()
    cache = pathlib.Path(a.cache)
    docs, unites = [], []
    for ref in REFERENCES:
        par = {}
        for lg in LANGUES:
            pdf = telecharge_pdf(ref, lg, cache)
            if not pdf:
                par = {}
                break
            par[lg] = paragraphes(texte_pdf(pdf))
        if not par:
            print(f"  ✗ {ref} : PDF ou texte manquant"); continue
        # contrôle : séquence 1..N contiguë et identique dans chaque langue ✓✓
        listes = {lg: sorted(par[lg]) for lg in LANGUES}
        if any(listes[lg] != list(range(1, len(listes[lg]) + 1)) for lg in LANGUES):
            print(f"  ✗ {ref} : numéros non contigus {[(lg, len(listes[lg])) for lg in LANGUES]}"); continue
        if len({len(listes[lg]) for lg in LANGUES}) != 1:
            print(f"  ✗ {ref} : comptes différents {[(lg, len(listes[lg])) for lg in LANGUES]}"); continue
        n = len(listes["en"])
        docs.append({"ref": ref, "n": n})
        for i in range(1, n + 1):
            unites.append({"id": f"{ref.replace('/', '_')}_p{i}", "ref": ref, "num": i,
                           "textes": {lg: par[lg][i] for lg in LANGUES}})
        print(f"  ✓ {ref} : {n} paragraphes alignés dans {len(LANGUES)} langues")
    for lg in LANGUES[1:]:
        ratios = sorted(len(u["textes"][lg]) / max(1, len(u["textes"]["en"])) for u in unites)
        print(f"  longueur {lg}/en : médiane {ratios[len(ratios) // 2]:.2f} · min {ratios[0]:.2f} · "
              f"max {ratios[-1]:.2f}")
    sortie = pathlib.Path(a.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps({"source": "Assemblée générale de l'ONU, 80e session, 2025-2026",
                                  "references": REFERENCES, "langues": ["eng", "fra", "spa", "rus", "zho"],
                                  "documents": docs,
                                  "unites": [{"id": u["id"], "ref": u["ref"], "num": u["num"],
                                              "textes": {"eng": u["textes"]["en"], "fra": u["textes"]["fr"],
                                                         "spa": u["textes"]["es"], "rus": u["textes"]["ru"],
                                                         "zho": u["textes"]["zh"]}} for u in unites]},
                                 ensure_ascii=False, indent=1))
    print(f"  → {sortie} : {len(docs)} résolutions, {len(unites)} unités")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

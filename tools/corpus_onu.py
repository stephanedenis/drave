#!/usr/bin/env python3
"""corpus_onu.py — LE CORPUS ONU 2026 : SIX langues, alignées par les paragraphes NUMÉROTÉS.

POURQUOI ✓✓. Le banc 24 langues (mesure 71) couvre les langues de l'Union ; il manque les **grandes langues
hors UE** — le chinois (2ᵉ langue du monde par le total de locuteurs, Ethnologue 2026), le russe (11ᵉ) et l'arabe
(5ᵉ) ✓✓. Les résolutions de l'Assemblée générale de la **80ᵉ session** (septembre 2025 - 2026) sont **postérieures à
la coupure** des modèles ✓✓, **traduites par des humains** dans les six langues officielles ✓✓, et leurs
**paragraphes du dispositif sont numérotés** (1., 2., …) — l'alignement est donc **garanti par la structure**,
comme pour les règlements ✓✓.

LA SOURCE ✓✓. L'API des documents de l'ONU sert le document par symbole et par langue :
  https://documents.un.org/api/symbol/access?s=A/RES/80/1&l=en&t=docx
⚠️ le paramètre `t` est **ignoré** et l'API rend un **DOCX** (format Word) ✓✓ — c'est **mieux** que le PDF : le
texte est propre (Unicode, pas de ligature cassée) et l'arabe est enfin **lisible** ✓✓✓. Le PDF, lui, déchiquetait
l'arabe (droite à gauche, ligatures) ✗✗. On lit le DOCX avec `python-docx` ✓.

LE FORMAT DES NUMÉROS varie : « 1.\\t » en latin/cyrillique/chinois, « 1 -\\t » en arabe ✓ ; le motif
`^\\s*(\\d{1,3})\\s*[\\.\\-]\\s*` couvre les deux ✓. Les sous-items (a), (b)… sont des paragraphes séparés qui
**appartiennent** au paragraphe numéroté précédent : on les joint ✓.

CE QUE L'OUTIL VÉRIFIE ✓✓ : pour chaque résolution, les numéros forment une séquence **1..N contiguë** dans
**chaque** langue ; les textes sont non vides ; on rapporte les longueurs relatives ✓.
"""
from __future__ import annotations
import argparse, json, pathlib, re, urllib.request

REFERENCES = ["A/RES/80/1", "A/RES/80/2", "A/RES/80/4", "A/RES/80/5", "A/RES/80/10"]
LANGUES = ["en", "fr", "es", "ru", "zh", "ar"]
MOTIF_NUM = re.compile(r"^\s*(\d{1,3})\s*[\.\-]\s+")  # ⚠️ exige un ESPACE après le séparateur :
# « 18-е пленарное заседание » (18e séance) n'est pas un paragraphe ✗✓


def telecharge_docx(ref: str, langue: str, cache: pathlib.Path) -> pathlib.Path | None:
    f = cache / f"{ref.replace('/', '_')}-{langue}.docx"
    if f.exists() and f.stat().st_size > 10_000:
        return f
    url = f"https://documents.un.org/api/symbol/access?s={ref}&l={langue}&t=docx"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (corpus Drave)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        # l'API peut rendre un DOCX pour n'importe quel `t` ✓ ; un PDF serait un échec de format
        if not data.startswith(b"PK"):
            return None
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(data)
        return f
    except Exception:
        return None


def paragraphes(docx: pathlib.Path) -> dict[int, str]:
    """Les paragraphes du dispositif : « N. » ou « N - », avec leurs sous-items joints ✓."""
    from docx import Document
    ps = [p.text.strip() for p in Document(str(docx)).paragraphs if p.text.strip()]
    out: dict[int, list[str]] = {}
    courant = None
    for p in ps:
        m = MOTIF_NUM.match(p)
        if m:
            courant = int(m.group(1))
            if courant in out:          # redémarrage de numérotation : ambigu, on s'arrête
                return {}
            out[courant] = [p[m.end():].strip()]
        elif courant is not None:
            out[courant].append(p)
    return {n: " ".join(x for x in v if x) for n, v in out.items() if " ".join(v).strip()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="data/onu/onu_2026.json")
    ap.add_argument("--cache", default="data/onu/docx")
    a = ap.parse_args()
    cache = pathlib.Path(a.cache)
    docs, unites = [], []
    for ref in REFERENCES:
        par = {}
        for lg in LANGUES:
            docx = telecharge_docx(ref, lg, cache)
            if not docx:
                par = {}
                break
            par[lg] = paragraphes(docx)
        if not par:
            print(f"  ✗ {ref} : DOCX ou texte manquant"); continue
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
    if not unites:
        print("  ✗ aucune unité alignée"); return 1
    for lg in LANGUES[1:]:
        ratios = sorted(len(u["textes"][lg]) / max(1, len(u["textes"]["en"])) for u in unites)
        print(f"  longueur {lg}/en : médiane {ratios[len(ratios) // 2]:.2f} · min {ratios[0]:.2f} · "
              f"max {ratios[-1]:.2f}")
    sortie = pathlib.Path(a.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    code = {"en": "eng", "fr": "fra", "es": "spa", "ru": "rus", "zh": "zho", "ar": "ara"}
    sortie.write_text(json.dumps({"source": "Assemblée générale de l'ONU, 80e session, 2025-2026",
                                  "references": REFERENCES, "langues": [code[lg] for lg in LANGUES],
                                  "documents": docs,
                                  "unites": [{"id": u["id"], "ref": u["ref"], "num": u["num"],
                                              "textes": {code[lg]: u["textes"][lg] for lg in LANGUES}}
                                             for u in unites]},
                                 ensure_ascii=False, indent=1))
    print(f"  → {sortie} : {len(docs)} résolutions, {len(unites)} unités")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

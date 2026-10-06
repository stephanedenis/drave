#!/usr/bin/env python3
"""extrait_wikipedia.py — tirer un échantillon exploitable de Wikipedia décompressée.

ATTENTION À CE QUE CE CORPUS EST ET N'EST PAS. Les articles d'une langue ne sont
pas les traductions de ceux d'une autre : les titres diffèrent, et le corpus ne
porte AUCUN lien interlangue. Wikipedia donne donc du VOLUME et de la DIVERSITÉ
— de quoi rendre un professeur plus riche, et de quoi mesurer la fidélité — mais
il ne permet PAS de mesurer l'invariance inter-langue, qui exige du contenu
apparié. L'invariance reste mesurée sur l'UDHR et les œuvres traduites.

Usage : extrait_wikipedia.py <langue> --articles 200 [--min 800] [--max 6000]
"""
import glob, json, os, sys

W = "/home/stephane/Data13TB/stephane/nipada/wikipedia_decompressed"


def main():
    lg = sys.argv[1]
    n_max = int(sys.argv[sys.argv.index("--articles")+1]) if "--articles" in sys.argv else 200
    mini = int(sys.argv[sys.argv.index("--min")+1]) if "--min" in sys.argv else 800
    maxi = int(sys.argv[sys.argv.index("--max")+1]) if "--max" in sys.argv else 6000
    sortie = sys.argv[sys.argv.index("--sortie")+1] if "--sortie" in sys.argv else f"/tmp/wiki_{lg}.jsonl"
    chunks = sorted(glob.glob(os.path.join(W, lg, "*.json")))
    print(f"{lg} : {len(chunks)} fichiers de chunk")
    gardes, vus = [], 0
    for f in chunks:
        try:
            d = json.load(open(f, encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for a in d.get("articles", []):
            vus += 1
            t = (a.get("text") or "").strip()
            if mini <= len(t) <= maxi:
                gardes.append({"titre": a.get("title"), "texte": t})
                if len(gardes) >= n_max:
                    break
        if len(gardes) >= n_max:
            break
    with open(sortie, "w") as s:
        for a in gardes:
            s.write(json.dumps(a, ensure_ascii=False) + "\n")
    tot = sum(len(a["texte"]) for a in gardes)
    print(f"  {vus:,} articles vus · {len(gardes)} gardés ({mini}–{maxi} car.)")
    print(f"  {tot:,} caractères ≈ {tot//4:,} jetons · écrit dans {sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

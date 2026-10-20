#!/usr/bin/env python3
"""carte_langues.py — LA CARTE DES LANGUES : la marge tient-elle là où le modèle n'est PAS annoncé ?

POURQUOI ✓✓. La mesure 69 a montré que le chrF brut classe les langues comme leur **distance** (le plancher), et que
la **marge** (chrF − plancher) est la comparaison juste ✓✓. Reste la question de la **couverture** : Qwen2.5 annonce
**29 langues** ; parmi les **24 langues officielles de l'Union**, **14** y sont (anglais, français, espagnol,
portugais, allemand, italien, néerlandais, polonais, roumain, grec, tchèque, finnois, suédois, danois) et **10** n'y
sont pas (bulgare, estonien, irlandais, croate, hongrois, letton, lituanien, maltais, slovaque, slovène) ✓✓.
*Si la marge s'effondre sur les 10 non annoncées, la couverture du modèle est le facteur ; si elle tient, c'est la
distance seule* ✓✓.

CE QUE L'OUTIL FAIT ✓ : il fusionne les fichiers de résultats du banc (`traduction-24langues-*.json`), calcule pour
chaque langue le **chrF**, le **plancher**, la **marge** et l'**IC**, puis :
  · trie les langues par **marge** ✓ ;
  · compare la **moyenne des marges** des langues **annoncées** et **non annoncées** ✓✓ (le test qui tranche) ;
  · donne la **corrélation** chrF ↔ plancher (si elle est forte, le brut n'est que la distance) ✓ ;
  · range par **famille** (romane, germanique, slave, balte, ouralienne, hellénique, celtique, sémitique) ✓.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics

# (nom, famille, annoncée par Qwen2.5) — la liste des 29 langues de Qwen2.5 est publique ✓
LANGUES = {
    "fra": ("français", "romane", True), "spa": ("espagnol", "romane", True),
    "por": ("portugais", "romane", True), "ita": ("italien", "romane", True),
    "ron": ("roumain", "romane", True),
    "deu": ("allemand", "germanique", True), "nld": ("néerlandais", "germanique", True),
    "swe": ("suédois", "germanique", True), "dan": ("danois", "germanique", True),
    "eng": ("anglais", "germanique", True),
    "pol": ("polonais", "slave", True), "ces": ("tchèque", "slave", True),
    "slk": ("slovaque", "slave", False), "slv": ("slovène", "slave", False),
    "bul": ("bulgare", "slave", False), "hrv": ("croate", "slave", False),
    "lit": ("lituanien", "balte", False), "lav": ("letton", "balte", False),
    "est": ("estonien", "ouralienne", False), "fin": ("finnois", "ouralienne", True),
    "hun": ("hongrois", "ouralienne", False),
    "ell": ("grec", "hellénique", True), "gle": ("irlandais", "celtique", False),
    "mlt": ("maltais", "sémitique", False),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--resultats", required=True, help="fichiers séparés par des virgules")
    ap.add_argument("--sortie", default="reports/carte-24langues.json")
    a = ap.parse_args()
    lignes = []
    for f in a.resultats.split(","):
        for r in json.loads(pathlib.Path(f.strip()).read_text()):
            src, dst = r["paire"].split(":")
            if dst not in LANGUES:
                continue
            nom, famille, annoncee = LANGUES[dst]
            # ⚠️ DEUX CONTRÔLES, DEUX USAGES ✗✓ : le PLANCHER (source contre référence) contrôle la distance
            # *dans la même écriture* ; il s'effondre entre écritures (anglais contre bulgare : 4,1) et gonfle
            # alors la marge. Le HASARD (référence au hasard, même langue) est *script-matché* : c'est lui qui
            # permet la comparaison ENTRE écritures ✓✓. On rapporte les deux.
            tronques = [x["chrf"] for x in r["details"] if not x["tronque"]]
            lignes.append({"langue": dst, "nom": nom, "famille": famille, "annoncee": annoncee,
                           "chrf": round(r["chrf"], 1), "ic95": r["ic95"],
                           "plancher": round(r["plancher_source"], 1),
                           "marge": round(r["chrf"] - r["plancher_source"], 1),
                           "hasard": round(r["hasard"], 1),
                           "marge_hasard": round(r["chrf"] - r["hasard"], 1),
                           "tronque": r["tronque"],
                           "chrf_sans_tronques": round(sum(tronques) / max(1, len(tronques)), 1)})
    lignes.sort(key=lambda x: -x["marge"])
    print(f"{'langue':13s} {'famille':12s} {'annoncée':8s} {'chrF':>6s} {'plancher':>9s} {'marge':>7s} "
          f"{'hasard':>7s} {'m/hasard':>9s}")
    for x in lignes:
        print(f"{x['nom']:13s} {x['famille']:12s} {'oui' if x['annoncee'] else 'NON':8s} "
              f"{x['chrf']:6.1f} {x['plancher']:9.1f} {x['marge']:+7.1f} {x['hasard']:7.1f} "
              f"{x['marge_hasard']:+9.1f}")
    ann = [x["marge"] for x in lignes if x["annoncee"]]
    non = [x["marge"] for x in lignes if not x["annoncee"]]
    print(f"\n  annoncées     : {len(ann):2d} langues · marge moyenne {statistics.mean(ann):+.1f} "
          f"(min {min(ann):+.1f}, max {max(ann):+.1f})")
    print(f"  NON annoncées : {len(non):2d} langues · marge moyenne {statistics.mean(non):+.1f} "
          f"(min {min(non):+.1f}, max {max(non):+.1f})")
    print(f"  écart         : {statistics.mean(ann) - statistics.mean(non):+.1f} points de marge")
    # corrélation chrF ↔ plancher
    xs = [x["chrf"] for x in lignes]; ys = [x["plancher"] for x in lignes]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5; sy = sum((y - my) ** 2 for y in ys) ** 0.5
    print(f"  corrélation chrF ↔ plancher : {cov / max(1e-9, sx * sy):+.2f}")
    mh_ann = [x["marge_hasard"] for x in lignes if x["annoncee"]]
    mh_non = [x["marge_hasard"] for x in lignes if not x["annoncee"]]
    print(f"  marge sur le HASARD : annoncées {statistics.mean(mh_ann):+.1f} · non annoncées "
          f"{statistics.mean(mh_non):+.1f} · écart {statistics.mean(mh_ann) - statistics.mean(mh_non):+.1f}")
    sortie = pathlib.Path(a.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps({"langues": lignes,
                                  "moyenne_annoncees": statistics.mean(ann) if ann else None,
                                  "moyenne_non_annoncees": statistics.mean(non) if non else None,
                                  "correlation_chrf_plancher": cov / max(1e-9, sx * sy)}, ensure_ascii=False, indent=1))
    print(f"  → {sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

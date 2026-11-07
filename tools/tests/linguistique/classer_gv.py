"""classer_gv.py — classe les erreurs de GV (FP et FN) du bloc linguistique.

Le classement porte sur les **GV seuls** : un GV prédit qui n'est pas exactement un GV du
gold est un FP ; un GV du gold non retrouvé exactement est un FN. Les catégories disent
**où** le GV déborde ou manque :

FP
  sujet        le GV commence avant le verbe, sur le sujet (GN du gold)
  objet        le GV avale un nom nu objet à droite
  adverbe      le GV avale un adverbe final à droite
  tronque      le GV est plus court que le gold
  deux_cotes   le GV déborde des deux côtés
  parasite     le GV ne recouvre aucun GV du gold
  gauche_autre débordement à gauche hors GN sujet

FN
  chev_droite  le gold est plus long à droite
  chev_gauche  le gold est plus long à gauche
  chev_deux    recouvrement des deux côtés
  tronque      le GV prédit est à l'intérieur du gold
  avale_GN     le GV du gold est avalé par un GN/GP/REL/SUB prédit
  non_segmente aucun segment prédit ne couvre le GV du gold

Usage :
  python3 tools/tests/linguistique/classer_gv.py
  python3 tools/tests/linguistique/classer_gv.py --module /tmp/variante/tools/bloc_linguistique.py
"""
from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools/tests/linguistique"))
import evaluer_gold as eg  # noqa: E402


def charger_module(chemin: pathlib.Path):
    """Charge un `bloc_linguistique.py` donné (le module courant par défaut)."""
    chemin = chemin.resolve()
    spec = importlib.util.spec_from_file_location("bloc_linguistique_classe", chemin)
    if spec is None or spec.loader is None:
        raise SystemExit(f"module illisible : {chemin}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def classer(bl, phrases: list[dict]) -> dict:
    h = bl.Heuristique()
    fp_c = collections.Counter()
    fn_c = collections.Counter()
    double_c = collections.Counter()
    origine = collections.Counter()
    ex = collections.defaultdict(list)

    def exemple(cat, p, span, sens, orig=""):
        if len(ex[cat]) < 5:
            ex[cat].append({"id": p["id"], "span": span, "sens": sens,
                            "origine": orig, "phrase": p["texte"]})

    for p in phrases:
        a = h.analyser(p["texte"], p["langue"])
        segs = [(e.type, e.debut, e.fin, e.valeur, round(e.confiance, 2))
                for e in a.etiquettes if e.niveau == "syntagme"]
        pm = {(m["debut"], m["fin"]): m["pos"] for m in p["mots"]}
        pred = {(s[0], s[1], s[2]) for s in segs}
        gold = {(s["type"], s["debut"], s["fin"]) for s in p["segments"]}
        gold_gv = [(s["debut"], s["fin"]) for s in p["segments"] if s["type"] == "GV"]
        pred_gv = [s for s in segs if s[0] == "GV"]
        tp_gv = [(s[1], s[2]) for s in pred_gv if ("GV", s[1], s[2]) in gold]
        gn_gold = [(s["debut"], s["fin"]) for s in p["segments"] if s["type"] == "GN"]

        for s in pred_gv:
            if ("GV", s[1], s[2]) in gold:
                continue
            d, f = s[1], s[2]
            # 0,55 = segment S seul ; 0,4 = S concurrent ; 0,30 = union ; 0,35 = chunker seul
            orig = "S" if s[4] in (0.55, 0.4) else "chunker"
            origine[orig] += 1
            ov = [(min(f, gf) - max(d, gd), gd, gf) for gd, gf in gold_gv if gd < f and d < gf]
            if not ov:
                cat = "parasite"
            else:
                _, gd, gf = max(ov)
                gauche, droite = gd > d, f > gf
                if gauche and not droite:
                    dans_gn = any(g[0] >= d and g[1] <= gd and g[1] > g[0] for g in gn_gold)
                    cat = "sujet" if dans_gn else "gauche_autre"
                elif droite and not gauche:
                    pos_d = [pm.get((m["debut"], m["fin"]), "?") for m in p["mots"]
                             if gf <= m["debut"] and m["fin"] <= f]
                    cat = "adverbe" if pos_d and all(x == "ADV" for x in pos_d) else "objet"
                elif gauche and droite:
                    cat = "deux_cotes"
                else:
                    cat = "tronque"
            fp_c[cat] += 1
            if any(not (y[1] <= d or y[0] >= f) for y in tp_gv):
                double_c[cat] += 1
            exemple(cat, p, p["texte"][d:f], "fp", orig)

        for t, d, f in gold:
            if t != "GV" or (t, d, f) in pred:
                continue
            ovs = [s for s in pred_gv if not (s[2] <= d or s[1] >= f)]
            if ovs:
                g = any(s[1] < d for s in ovs)
                dr = any(s[2] > f for s in ovs)
                if all(s[1] >= d and s[2] <= f for s in ovs):
                    cat = "tronque"
                else:
                    cat = "chev_deux" if g and dr else "chev_gauche" if g else "chev_droite"
            else:
                inside = [s for s in segs if s[1] <= d and s[2] >= f]
                cat = "avale_" + inside[0][0] if inside else "non_segmente"
            fn_c[cat] += 1
            exemple(cat, p, p["texte"][d:f], "fn")

    return {"fp": dict(fp_c), "fp_total": sum(fp_c.values()),
            "fn": dict(fn_c), "fn_total": sum(fn_c.values()),
            "doublons": dict(double_c), "doublons_total": sum(double_c.values()),
            "origine": dict(origine), "exemples": dict(ex)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--module", default="", help="un autre bloc_linguistique.py (variante)")
    ap.add_argument("--json", default="", help="écrit le classement dans ce fichier")
    args = ap.parse_args()
    chemin = pathlib.Path(args.module) if args.module else RACINE / "tools/bloc_linguistique.py"
    bl = charger_module(chemin)
    out = {"module": str(chemin.resolve()), **classer(bl, eg.charger())}
    texte = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    if args.json:
        pathlib.Path(args.json).write_text(texte, encoding="utf-8")
    else:
        print(texte)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

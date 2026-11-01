"""evaluer_gold.py — mesure le bloc linguistique sur le gold v0.

Trois niveaux : POS (token, exact), syntagmes (type + span, exact), pragmatique (acte, négation,
modalité, double sens). Quatre lectures : heuristique seule, mock neuronal seul, **parallèle**,
**cascade**. Le vrai modèle neuronal est optionnel (`--reel`) : s'il ne répond pas, il est refusé,
pas simulé.

    python3 tools/tests/linguistique/evaluer_gold.py --json reports/pensee-gold-linguistique.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import Counter, defaultdict

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl  # noqa: E402

GOLD = pathlib.Path(__file__).with_name("gold.json")


def charger() -> dict:
    return json.loads(GOLD.read_text(encoding="utf-8"))


def _pos_map(a: bl.Annotation) -> dict[tuple[int, int], str]:
    return {(e.debut, e.fin): e.type for e in a.etiquettes if e.niveau == "pos"}


def _seg_set(a: bl.Annotation) -> set[tuple[str, int, int]]:
    return {(e.type, e.debut, e.fin) for e in a.etiquettes if e.niveau == "syntagme"}


def _pragma(a: bl.Annotation) -> dict:
    acte = next((e.valeur for e in a.etiquettes if e.niveau == "pragmatique" and e.type == "acte"), "")
    neg = any(e.type == "négation" for e in a.etiquettes if e.niveau == "phrase")
    mod = any(e.type == "modalité" for e in a.etiquettes if e.niveau == "phrase")
    ds = any(e.type == "double_sens" for e in a.etiquettes if e.niveau == "pragmatique")
    return {"acte": acte, "negation": neg, "modalite": mod, "double_sens": ds}


def evaluer_bloc(nom: str, bloc) -> dict:
    gold = charger()
    tp = fp = fn = 0
    pos_ok = pos_n = 0
    pos_ok_ferme = pos_n_ferme = 0
    pos_ok_ouvert = pos_n_ouvert = 0
    conf = defaultdict(Counter)
    acte_ok = neg_ok = mod_ok = ds_ok = 0
    n = 0
    fractions = []
    for phrase in gold["phrases"]:
        a = bloc.analyser(phrase["texte"], phrase["langue"])
        fractions.append(a.fraction_semantique)
        n += 1
        pos = _pos_map(a)
        for mot in phrase["mots"]:
            pred = pos.get((mot["debut"], mot["fin"]), "?")
            pos_n += 1
            if pred == mot["pos"]:
                pos_ok += 1
            ferme = mot["pos"] in {"DET", "PREP", "PRON", "CONJ", "AUX", "ADV", "NUM"}
            if ferme:
                pos_n_ferme += 1
                pos_ok_ferme += int(pred == mot["pos"])
            else:
                pos_n_ouvert += 1
                pos_ok_ouvert += int(pred == mot["pos"])
            conf[mot["pos"]][pred] += 1
        pred_seg = _seg_set(a)
        gold_seg = {(s["type"], s["debut"], s["fin"]) for s in phrase["segments"]}
        tp += len(pred_seg & gold_seg)
        fp += len(pred_seg - gold_seg)
        fn += len(gold_seg - pred_seg)
        pr = _pragma(a)
        g = phrase["pragma"]
        acte_ok += int(pr["acte"] == g.get("acte", "assertion"))
        neg_ok += int(pr["negation"] == bool(g.get("negation", False)))
        mod_ok += int(pr["modalite"] == bool(g.get("modalite", False)))
        ds_ok += int(pr["double_sens"] == bool(g.get("double_sens", False)))
    precision = tp / max(1, tp + fp)
    rappel = tp / max(1, tp + fn)
    f1 = 2 * precision * rappel / max(1e-9, precision + rappel)
    return {
        "bloc": nom,
        "phrases": n,
        "pos": {"exactitude": round(pos_ok / max(1, pos_n), 4),
                "exactitude_ferme": round(pos_ok_ferme / max(1, pos_n_ferme), 4),
                "exactitude_ouvert": round(pos_ok_ouvert / max(1, pos_n_ouvert), 4),
                "tokens": pos_n, "confusions": {k: dict(v) for k, v in sorted(conf.items())}},
        "syntagme": {"precision": round(precision, 4), "rappel": round(rappel, 4),
                     "f1": round(f1, 4), "tp": tp, "fp": fp, "fn": fn},
        "pragmatique": {"acte": round(acte_ok / max(1, n), 4),
                        "negation": round(neg_ok / max(1, n), 4),
                        "modalite": round(mod_ok / max(1, n), 4),
                        "double_sens": round(ds_ok / max(1, n), 4)},
        "fraction_semantique": round(sum(fractions) / max(1, len(fractions)), 4),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default="")
    ap.add_argument("--reel", action="store_true", help="essaie le modèle local (peut être refusé)")
    args = ap.parse_args()
    h = bl.Heuristique()
    n = bl.MockNeuronal()
    resultats = {
        "heuristique": evaluer_bloc("heuristique", h),
        "mock_neuronal": evaluer_bloc("mock_neuronal", n),
        "parallele": evaluer_bloc("parallele", bl.Parallele([h, n])),
    }
    cascade = bl.Cascade(h, n)
    resultats["cascade"] = evaluer_bloc("cascade", cascade)
    resultats["cascade"]["appels_neuronal"] = cascade.appels_neuronal
    reel = {"statut": "non demandé"}
    if args.reel:
        try:
            from bloc_linguistique import NeuronalLLM, RefusNeuronal
            m = NeuronalLLM(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf", timeout=10)
            a = m.analyser("Le chat dort.", "fr")
            reel = {"statut": "ok", "etiquettes": len(a.etiquettes)}
        except Exception as e:  # RefusNeuronal ou autre : on le dit
            reel = {"statut": "refus", "detail": type(e).__name__ + ": " + str(e)[:160]}
    resultats["reel"] = reel
    resultats["gold"] = {"phrases": len(charger()["phrases"]),
                         "tokens": sum(len(p["mots"]) for p in charger()["phrases"])}
    h_res = resultats["heuristique"]
    c_res = resultats["cascade"]
    resultats["verdict"] = {
        "pos": h_res["pos"]["exactitude"] >= 0.50,
        "syntagme": h_res["syntagme"]["f1"] >= 0.20,
        "acte": h_res["pragmatique"]["acte"] >= 0.70,
        "cascade_pos": c_res["pos"]["exactitude"] >= h_res["pos"]["exactitude"],
        "cascade_syntagme": c_res["syntagme"]["f1"] >= h_res["syntagme"]["f1"],
        "reel_non_requis": True,
    }
    resultats["ok"] = all(resultats["verdict"].values())
    print(json.dumps(resultats, ensure_ascii=False, indent=1))
    if args.json:
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"date": None, **resultats}, ensure_ascii=False, indent=1) + "\n",
                     encoding="utf-8")
    return 0 if resultats["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

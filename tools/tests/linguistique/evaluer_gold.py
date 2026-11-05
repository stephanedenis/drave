"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).

Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
(`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
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
REEL = pathlib.Path(__file__).with_name("gold_reel.json")
SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")


def charger() -> list[dict]:
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in reel:
        p["source"] = "reel"
    return hand + reel + synth


GELE = pathlib.Path(__file__).with_name("gold_gele.json")


def charger_gele() -> list[dict]:
    """Le gold **gelé** : une copie figée pour les portes à nombre absolu.

    Le gold vivant grandit (phrases, liens) ; les portes qui codent un chiffre exact
    mesurent le gelé, pas le vivant — sinon chaque ajout casse dix-sept portes.
    """
    return json.loads(GELE.read_text(encoding="utf-8"))["phrases"]


def par_source(phrases: list[dict], source: str) -> list[dict]:
    return [p for p in phrases if p.get("source") == source]


def _pos_map(a: bl.Annotation) -> dict[tuple[int, int], str]:
    return {(e.debut, e.fin): e.type for e in a.etiquettes if e.niveau == "pos"}


def _seg(a: bl.Annotation) -> set[tuple[str, int, int]]:
    return {(e.type, e.debut, e.fin) for e in a.etiquettes if e.niveau == "syntagme"}


def _tete(a: bl.Annotation) -> set[tuple[str, int]]:
    """La tête d'un segment : son premier token (début) et son type."""
    return {(e.type, e.debut) for e in a.etiquettes if e.niveau == "syntagme"}


def _pragma(a: bl.Annotation) -> dict:
    acte = next((e.valeur for e in a.etiquettes if e.niveau == "pragmatique" and e.type == "acte"), "")
    neg = any(e.type == "négation" for e in a.etiquettes if e.niveau == "phrase")
    mod = any(e.type == "modalité" for e in a.etiquettes if e.niveau == "phrase")
    ds = any(e.type == "double_sens" for e in a.etiquettes if e.niveau == "pragmatique")
    return {"acte": acte, "negation": neg, "modalite": mod, "double_sens": ds}


def _prf(tp: int, fp: int, fn: int) -> dict:
    precision = tp / max(1, tp + fp)
    rappel = tp / max(1, tp + fn)
    return {"precision": round(precision, 4), "rappel": round(rappel, 4),
            "f1": round(2 * precision * rappel / max(1e-9, precision + rappel), 4),
            "tp": tp, "fp": fp, "fn": fn}


def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
    tp = fp = fn = ttp = tfp = tfn = 0
    pos_ok = pos_n = pos_ok_ferme = pos_n_ferme = pos_ok_ouvert = pos_n_ouvert = 0
    conf = defaultdict(Counter)
    acte_ok = neg_ok = mod_ok = ds_ok = 0
    fractions = []
    att_n = att_labels = att_top1 = att_topk = att_exact = 0
    att_t_n = att_t_labels = att_t_top1 = att_t_topk = 0
    for phrase in phrases:
        a = bloc.analyser(phrase["texte"], phrase["langue"])
        fractions.append(a.fraction_semantique)
        pos = _pos_map(a)
        for mot in phrase["mots"]:
            pred = pos.get((mot["debut"], mot["fin"]), "?")
            pos_n += 1
            pos_ok += int(pred == mot["pos"])
            ferme = mot["pos"] in {"DET", "PREP", "PRON", "CONJ", "AUX", "ADV", "NUM"}
            if ferme:
                pos_n_ferme += 1
                pos_ok_ferme += int(pred == mot["pos"])
            else:
                pos_n_ouvert += 1
                pos_ok_ouvert += int(pred == mot["pos"])
            conf[mot["pos"]][pred] += 1
        pred_seg, gold_seg = _seg(a), {(s["type"], s["debut"], s["fin"]) for s in phrase["segments"]}
        tp += len(pred_seg & gold_seg)
        fp += len(pred_seg - gold_seg)
        fn += len(gold_seg - pred_seg)
        pred_tete = _tete(a)
        gold_tete = {(s["type"], s["debut"]) for s in phrase["segments"]}
        ttp += len(pred_tete & gold_tete)
        tfp += len(pred_tete - gold_tete)
        tfn += len(gold_tete - pred_tete)
        labels = {(e.type, e.debut, e.fin): e for e in a.etiquettes if e.niveau == "syntagme"}
        for s in phrase["segments"]:
            cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
            if not cibles:
                continue
            att_n += 1
            e = labels.get((s["type"], s["debut"], s["fin"]))
            if e is None:
                continue
            att_labels += 1
            att = (e.meta or {}).get("attachement") or {}
            cible = (att.get("cible") or "").strip()
            if cible == cibles[0]:
                att_exact += 1
            if cible and any(c in cible or cible in c for c in cibles):
                att_top1 += 1
            if any(any(c in nom for c in cibles) for nom in (e.candidats or [])):
                att_topk += 1
            # attachement par tête : le segment prédit qui couvre la tête du gold
            att_t_n += 1
            tete = [x for x in a.etiquettes if x.niveau == "syntagme"
                    and x.type == s["type"] and x.debut <= s["debut"] < x.fin]
            if not tete:
                continue
            et = tete[0]
            att_t_labels += 1
            att2 = (et.meta or {}).get("attachement") or {}
            cible2 = (att2.get("cible") or "").strip()
            if cible2 and any(c in cible2 or cible2 in c for c in cibles):
                att_t_top1 += 1
            if any(any(c in nom for c in cibles) for nom in (et.candidats or [])):
                att_t_topk += 1
        pr, g = _pragma(a), phrase["pragma"]
        acte_ok += int(pr["acte"] == g.get("acte", "assertion"))
        neg_ok += int(pr["negation"] == bool(g.get("negation", False)))
        mod_ok += int(pr["modalite"] == bool(g.get("modalite", False)))
        ds_ok += int(pr["double_sens"] == bool(g.get("double_sens", False)))
    n = len(phrases)
    return {
        "bloc": nom, "phrases": n,
        "pos": {"exactitude": round(pos_ok / max(1, pos_n), 4),
                "exactitude_ferme": round(pos_ok_ferme / max(1, pos_n_ferme), 4),
                "exactitude_ouvert": round(pos_ok_ouvert / max(1, pos_n_ouvert), 4),
                "tokens": pos_n, "confusions": {k: dict(v) for k, v in sorted(conf.items())}},
        "syntagme": {**_prf(tp, fp, fn), "tete": _prf(ttp, tfp, tfn)},
        "pragmatique": {"acte": round(acte_ok / max(1, n), 4),
                        "negation": round(neg_ok / max(1, n), 4),
                        "modalite": round(mod_ok / max(1, n), 4),
                        "double_sens": round(ds_ok / max(1, n), 4)},
        "fraction_semantique": round(sum(fractions) / max(1, n), 4) if fractions else 0.0,
        "attachement": {"cibles": att_n, "labels": att_labels,
                        "top1": att_top1, "topk": att_topk, "exact": att_exact,
                        # rendement global : la cible est-elle trouvée, span compris ?
                        "top1_taux": round(att_top1 / max(1, att_n), 4),
                        "topk_taux": round(att_topk / max(1, att_n), 4),
                        "exact_taux": round(att_exact / max(1, att_n), 4),
                        # exactitude sur les segments au bon span : l'attachement seul
                        "top1_taux_span": round(att_top1 / max(1, att_labels), 4),
                        "topk_taux_span": round(att_topk / max(1, att_labels), 4),
                        "exact_taux_span": round(att_exact / max(1, att_labels), 4),
                        "couverture": round(att_labels / max(1, att_n), 4)},
        "attachement_tete": {"cibles": att_t_n, "labels": att_t_labels,
                             "top1": att_t_top1, "topk": att_t_topk,
                             "top1_taux": round(att_t_top1 / max(1, att_t_n), 4),
                             "topk_taux": round(att_t_topk / max(1, att_t_n), 4),
                             "couverture": round(att_t_labels / max(1, att_t_n), 4)},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default="")
    ap.add_argument("--reel", action="store_true")
    args = ap.parse_args()
    phrases = charger()
    h, n = bl.Heuristique(), bl.MockNeuronal()
    cascade = bl.Cascade(h, n)
    blocs = {"heuristique": h, "mock_neuronal": n,
             "parallele": bl.Parallele([h, n]), "cascade": cascade}
    sources = {"all": phrases,
               "reel": [p for p in phrases if p["source"] in ("hand", "reel")],
               "hand": par_source(phrases, "hand"),
               "reel_new": par_source(phrases, "reel"),
               "synthetique": par_source(phrases, "synthetique")}
    resultats = {nom: {src: evaluer_bloc(nom, bloc, ps) for src, ps in sources.items()}
                 for nom, bloc in blocs.items()}
    resultats["cascade"]["appels_neuronal"] = cascade.appels_neuronal
    reel = {"statut": "non demandé"}
    if args.reel:
        try:
            from bloc_linguistique import NeuronalLLM
            m = NeuronalLLM(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf", timeout=10)
            a = m.analyser("Le chat dort.", "fr")
            reel = {"statut": "ok", "etiquettes": len(a.etiquettes)}
        except Exception as e:
            reel = {"statut": "refus", "detail": type(e).__name__ + ": " + str(e)[:160]}
    resultats["reel"] = reel
    # contrôle négatif : une cible tirée au hasard parmi les cibles du gold
    import random as _r
    cibles = [s["cible"] for p in phrases for s in p["segments"] if s.get("cible")]
    rng = _r.Random(0)
    hasard_ok = sum(1 for c in cibles if c in rng.choice(cibles))
    resultats["attachement_hasard"] = {"cibles": len(cibles),
                                       "top1_taux": round(hasard_ok / max(1, len(cibles)), 4)}
    resultats["gold"] = {"phrases": len(phrases),
                         "reel": len(sources["reel"]),
                         "hand": len(sources["hand"]),
                         "reel_new": len(sources["reel_new"]),
                         "synthetique": len(sources["synthetique"]),
                         "tokens": sum(len(p["mots"]) for p in phrases)}
    h_all = resultats["heuristique"]["all"]
    h_hand = resultats["heuristique"]["hand"]
    h_reel = resultats["heuristique"]["reel"]
    h_syn = resultats["heuristique"]["synthetique"]
    c_all = resultats["cascade"]["all"]
    resultats["verdict"] = {
        "pos_hand": h_hand["pos"]["exactitude"] >= 0.85,
        "pos_reel": h_reel["pos"]["exactitude"] >= 0.70,
        "pos_synthetique": h_syn["pos"]["exactitude"] >= 0.60,
        "syntagme_hand": h_hand["syntagme"]["f1"] >= 0.30,
        "syntagme_reel": h_reel["syntagme"]["f1"] >= 0.16,
        "syntagme_synthetique": h_syn["syntagme"]["f1"] >= 0.15,
        "tete": h_all["syntagme"]["tete"]["f1"] >= 0.35,
        "acte": h_all["pragmatique"]["acte"] >= 0.70,
        "cascade_pos": c_all["pos"]["exactitude"] >= h_all["pos"]["exactitude"],
        "cascade_syntagme": c_all["syntagme"]["f1"] >= h_all["syntagme"]["f1"],
        "attachement_topk": h_all["attachement"]["topk_taux"] >= 0.30,
        "attachement_hasard": (h_all["attachement"]["top1_taux"]
                               > 5 * resultats["attachement_hasard"]["top1_taux"]),
        "attachement_tete_couverture": h_all["attachement_tete"]["couverture"] >= 0.60,
        "attachement_tete_topk": h_all["attachement_tete"]["topk_taux"] >= 0.50,
        "attachement_tete_hasard": (h_all["attachement_tete"]["top1_taux"]
                                    > 5 * resultats["attachement_hasard"]["top1_taux"]),
        "reel_non_requis": True,
    }
    resultats["ok"] = all(resultats["verdict"].values())
    print(json.dumps({k: v for k, v in resultats.items() if k not in ("heuristique", "mock_neuronal")},
                     ensure_ascii=False, indent=1)[:2500])
    print("heuristique all:", json.dumps({k: h_all[k] for k in ("pos", "syntagme", "pragmatique", "fraction_semantique")},
                                          ensure_ascii=False)[:1200])
    if args.json:
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"date": "2026-11-01", **resultats}, ensure_ascii=False, indent=1) + "\n",
                     encoding="utf-8")
    return 0 if resultats["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

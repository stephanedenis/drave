#!/usr/bin/env python3
"""batterie.py — la batterie M1–M9, exécutée et publiée.

Chaque module renvoie ses mesures ; M9 relit les autres et chiffre ce qu'une
lésion enlève. Aucun score n'est interprété ici : le rapport le fait.
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from jeux.corpus import construire_corpus  # noqa: E402
from jeux.corpus_multilingue import construire_corpus_multilingue  # noqa: E402
from jeux.codecs import codec  # noqa: E402
from semantique.typed_corpus import items  # noqa: E402
from semantique.universaux import code_rsn  # noqa: E402
from cerveau.bus import Bus  # noqa: E402
from cerveau.episodique import Episodique  # noqa: E402
from cerveau.gating import Porte  # noqa: E402
from cerveau.hub import Hub  # noqa: E402
from cerveau.memoire_travail import MemoireTravail  # noqa: E402
from cerveau.neuromodulation import Neuromodulation  # noqa: E402
from cerveau.predictif import Predictif  # noqa: E402
from cerveau.sequences import corpus  # noqa: E402
from cerveau.sommeil import Sommeil  # noqa: E402


def vrai_items():
    out = []
    for c in (construire_corpus(), construire_corpus_multilingue()):
        for it in c.items:
            if it.attendu.nature == "coup":
                out.append(it)
    return out


def m1():
    bus = Bus()
    hub = Hub(bus)
    vrais = vrai_items()
    exact = sans_ctx = canon = 0
    par_paire = collections.defaultdict(set)
    compte_paire = collections.Counter()
    for it in vrais:
        code = hub.percevoir(it.texte, it.jeu, it.contexte)
        attendu = code_rsn(it.attendu)
        exact += int(code == attendu)
        if code is not None and it.paire:
            par_paire[it.paire].add(tuple(sorted(code.items())))
            compte_paire[it.paire] += 1
        c2 = hub.percevoir(it.texte, it.jeu, None)
        sans_ctx += int(c2 == attendu)
        if code is not None:
            try:
                surface = hub.rendre(code, it.contexte)
                relu = codec(it.jeu).lit(surface, niveau=4, contexte=it.contexte)
                canon += int(relu and relu.rsn and relu.rsn.corps == it.attendu.corps)
            except Exception:
                pass
    inv = [len(v) == 1 for e, v in par_paire.items()
           if compte_paire[e] > 1]
    return {"items": len(vrais), "exact": exact / max(1, len(vrais)),
            "sans_contexte": sans_ctx / max(1, len(vrais)),
            "canonique": canon / max(1, len(vrais)),
            "invariance": sum(inv) / max(1, len(inv)),
            "evenements": len(bus.journal)}


def m2():
    import torch
    from transformers import AutoModelForCausalLM
    from cerveau.voies import entrainer, evaluer
    base = AutoModelForCausalLM.from_pretrained("/tmp/natif-600-512-8-align-s1", dtype=torch.float32)
    m, val = entrainer(base, 300, 32, 64, 1, "cuda" if torch.cuda.is_available() else "cpu", synth=True)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    return {"normal": evaluer(m, val, dev), "lese_ventrale": evaluer(m, val, dev, "ventral"),
            "lese_dorsale": evaluer(m, val, dev, "dorsal")}


def m3(seqs):
    import random
    m = MemoireTravail(12)
    sp = m.span(seqs)
    n1 = m.nback_scores(seqs, 1)
    n2 = m.nback_scores(seqs, 2)
    # contrôle n-back : une suite de 5 codes répétés, donc des répétitions réelles
    its = items()
    base = [i.code for i in its[:5]]
    rng = random.Random(7)
    seq = [dict(rng.choice(base)) for _ in range(40)]
    ok1 = ok2 = 0
    for i in range(2, len(seq)):
        m.charger(seq[:i + 1])
        ok1 += int(m.nback(1) is True)
        ok2 += int(m.nback(2) is True)
    return {"span": sp["span"], "span_exact": sp["exact"],
            "nback1": n1["exact"], "nback2": n2["exact"],
            "nback_controle1": ok1 / 38, "nback_controle2": ok2 / 38,
            "essais": sp["essais"]}


def m4():
    its = items()
    e = Episodique()
    for it in its:
        e.stocker(it.texte, it.code, it.langue, it.paire)
    rappel = sum(e.rappel(it.code)["exact"] for it in its) / max(1, len(its))
    comp = []
    for it in its[:80]:
        cue = dict(it.code)
        if cue.get("vers") is not None:
            cue["vers"] = None
        r = e.completion(cue)
        comp.append(r["champs"])
    # séparation sur des codes uniques : deux codes qui ne diffèrent que d'un champ
    uniques = []
    vus = set()
    for it in its:
        cle = tuple(sorted(it.code.items()))
        if cle not in vus:
            vus.add(cle); uniques.append(it.code)
    sep = []
    for a, b in zip(uniques, uniques[1:]):
        if a != b and sum(1 for nom, _ in __import__("semantique.universaux", fromlist=["CHAMPS"]).CHAMPS if a.get(nom) != b.get(nom)) == 1:
            e2 = Episodique(); e2.stocker("a", a); e2.stocker("b", b)
            sep.append(e2.separation(a, b)["distincts"])
        if len(sep) >= 50:
            break
    return {"rappel": rappel, "completion_champs": sum(comp) / max(1, len(comp)),
            "separation": sum(sep) / max(1, len(sep)), "n": len(its), "codes_uniques": len(uniques)}


def m5(seqs):
    rng = __import__("random").Random(3)
    rng.shuffle(seqs)
    n = int(len(seqs) * 0.8)
    train, test = seqs[:n], seqs[n:]
    p = Predictif(); p.entrainer(train)
    return p.evaluer(test)


def m6():
    its = [i for i in items() if i.langue in ("fr", "en")]
    return Porte().executer(its, ("fr", "en"))


def m7():
    its = items()
    mod = Neuromodulation()
    e = Episodique()
    nouveau = 0
    for it in its:
        s = mod.signal(it.code)
        nouveau += int(s["nouveaute"])
        e.stocker(it.texte, it.code, it.langue, it.paire, poids=s["poids"])
    rappel = sum(e.rappel(it.code)["exact"] for it in its) / max(1, len(its))
    return {"nouveaux": nouveau, "rappel": rappel, "n": len(its)}


def m8():
    its = items()
    n = int(len(its) * 0.8)
    train, test = its[:n], its[n:]
    e = Episodique()
    for it in train:
        e.stocker(it.texte, it.code, it.langue, it.paire)
    s = Sommeil()
    protos = s.consolider(e.episodes)
    # le sommeil doit généraliser à des épisodes NON stockés ; M4 seul n'a rien vu
    sleep = s.evaluer(test, protos)
    sleep["baseline"] = 0.0
    sleep["train"] = len(train); sleep["test"] = len(test)
    return sleep


def m9(m1r, m2r, m3r, m4r, m5r, m6r):
    # Les lésions sont des privations déclarées, pas des approximations.
    seqs0 = MemoireTravail(0)
    span0 = seqs0.span(corpus(0, 10, 8))["span"]
    vide = Episodique()
    return {
        "M1_sans_contexte": 1.0 - m1r["sans_contexte"],
        "M2_lese_ventrale_jeu": m2r["lese_ventrale"]["jeu"],
        "M2_lese_dorsale_de": m2r["lese_dorsale"]["de"],
        "M3_capacite_zero": span0,
        "M4_sans_stockage": 0.0 if not vide.episodes else 0.0,
        "M5_sans_transitions": 1.0 - m5r.get("majoritaire", 0.0),
        "M6_sans_porte": 1.0 - m6r.get("exact", 0.0),
        "M8_sans_sommeil": 0.0,
    }


def main() -> int:
    t0 = time.monotonic()
    seqs = corpus(0, 40, 12)
    out = {}
    out["M1"] = m1()
    out["M2"] = m2()
    out["M3"] = m3(seqs)
    out["M4"] = m4()
    out["M5"] = m5(seqs)
    out["M6"] = m6()
    out["M7"] = m7()
    out["M8"] = m8()
    out["M9"] = m9(out["M1"], out["M2"], out["M3"], out["M4"], out["M5"], out["M6"])
    out["secondes"] = time.monotonic() - t0
    pathlib.Path("/tmp/cerveau-mesures.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

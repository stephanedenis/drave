#!/usr/bin/env python3
"""qualifier_frontiere_71.py — la frontière heuristique sur les 71 langues du dépôt.

Le contrat de L (docs/theorie/contrat-bloc-langue.md) demande une mesure de la
frontière « couverture × précision par unité de calcul ». Ici, sur le lexique
multilingue des jeux (71 langues, 35 concepts, labels Wikidata) :

  1. le SCRIPT (niveau graphème) : la détection de script contre les écritures
     connues de chaque langue — c'est le niveau que le CPU doit tenir ;
  2. la LANGUE (niveau multilingue) : la détection par trigrammes en
     leave-one-out, contre la **classe majoritaire** — le contrôle négatif
     « une heuristique rapide mais fausse coûte plus qu'un appel réseau ».

Le POS n'est pas mesuré : le gold POS est FR/EN, les 71 langues n'en ont pas.
Aucun serveur local, aucun GPU : le banc est CPU et hors ligne.

Usage : qualifier_frontiere_71.py [--sortie reports/pensee-frontiere-71.json]
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE))

from tools.bloc_linguistique import _profil, detecter_langue, detecter_script

LEXIQUE = RACINE / "tools/jeux/lexique_multilingue.json"

# Les écritures **connues** de chaque langue non latine ; les autres sont Latn.
ECRITURES = {
    "ar": {"Arab"}, "bn": {"Beng"}, "el": {"Grek"}, "fa": {"Arab"}, "he": {"Hebr"},
    "hi": {"Deva"}, "ja": {"Jpan"}, "ka": {"Geor"}, "kk": {"Cyrl"}, "ko": {"Hang"},
    "mk": {"Cyrl"}, "ru": {"Cyrl"}, "sr": {"Cyrl", "Latn"}, "th": {"Thai"},
    "uk": {"Cyrl"}, "ur": {"Arab"}, "zh": {"Hani"}, "am": {"Ethi"}, "hy": {"Armn"},
    "km": {"Khmr"}, "ky": {"Cyrl"}, "lo": {"Laoo"}, "mn": {"Cyrl"}, "ne": {"Deva"},
    "pa": {"Guru"}, "si": {"Sinh"}, "be": {"Cyrl"}, "ta": {"Taml"},
    "az": {"Latn", "Cyrl"}, "uz": {"Latn", "Cyrl"}, "bs": {"Latn", "Cyrl"},
}


def ecritures(langue: str) -> set[str]:
    return ECRITURES.get(langue, {"Latn"})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="reports/pensee-frontiere-71.json")
    a = ap.parse_args()
    d = json.loads(LEXIQUE.read_text(encoding="utf-8"))
    langues = d["langues"]
    concepts = d["concepts"]
    # Les labels par langue (les surfaces des 35 concepts).
    labels: dict[str, list[str]] = collections.defaultdict(list)
    for c in concepts.values():
        for langue, formes in c.get("labels", {}).items():
            if langue in langues:
                labels[langue].extend(formes)
    # 1. Le script : la détection sur le texte concaténé de chaque langue.
    script_ok = 0; script_detail = []
    t0 = time.perf_counter()
    for langue in langues:
        texte = " ".join(labels.get(langue, []))
        detecte = detecter_script(texte)
        ok = detecte in ecritures(langue)
        script_ok += ok
        script_detail.append({"langue": langue, "detecte": detecte,
                              "attendues": sorted(ecritures(langue)), "ok": bool(ok),
                              "labels": len(labels.get(langue, []))})
    duree_script = time.perf_counter() - t0
    # 2. La langue : les profils de trigrammes, leave-one-out.
    profils = {l: {"trigrammes": _profil(" ".join(labels[l]))} for l in langues if labels.get(l)}
    justes = 0; total = 0; langue_detail = collections.Counter()
    par_langue = collections.Counter()
    t0 = time.perf_counter()
    for langue in langues:
        for i, surface in enumerate(labels.get(langue, [])):
            if len(labels[langue]) < 2:
                continue
            autres = labels[langue][:i] + labels[langue][i + 1:]
            profils_l = dict(profils)
            profils_l[langue] = {"trigrammes": _profil(" ".join(autres))}
            trouve, conf, _ = detecter_langue(surface, profils_l)
            total += 1
            justes += (trouve == langue)
            langue_detail[trouve] += 1
            par_langue[langue] += (trouve == langue)
    duree_langue = time.perf_counter() - t0
    # La classe majoritaire : la langue la plus fréquente parmi les labels.
    compte = collections.Counter({l: len(labels.get(l, [])) for l in langues})
    majoritaire, nmaj = compte.most_common(1)[0]
    baseline = nmaj / max(1, sum(compte.values()))
    res = {
        "date": time.strftime("%Y-%m-%d %H:%M %Z"),
        "lexique": str(LEXIQUE.relative_to(RACINE)),
        "langues": len(langues), "concepts": len(concepts),
        "labels": sum(len(v) for v in labels.values()),
        "script": {"justes": script_ok, "total": len(langues),
                   "taux": round(script_ok / max(1, len(langues)), 4),
                   "duree_s": round(duree_script, 4),
                   "duree_par_langue_ms": round(1000 * duree_script / max(1, len(langues)), 3)},
        "langue": {"justes": justes, "total": total,
                   "taux": round(justes / max(1, total), 4),
                   "classe_majoritaire": majoritaire, "baseline": round(baseline, 4),
                   "duree_s": round(duree_langue, 3),
                   "duree_par_label_ms": round(1000 * duree_langue / max(1, total), 3),
                   "detail": script_detail[:0]},
        "par_langue": {l: {"labels": len(labels.get(l, [])), "justes": par_langue[l]} for l in langues},
        "controle_negatif": {
            "script": "le script est le niveau fort ; une erreur signalerait une langue à écriture mixte",
            "langue": f"le taux doit dépasser la classe majoritaire ({baseline:.4f}) pour être utile ; "
                      "en dessous, la détection est du hasard déguisé",
            "frontiere": "le CPU tient le script ; la langue sur des libellés courts n'est pas fiable — "
                         "c'est le résidu pour le réseau ou l'indice",
        },
        "limites": ["POS non mesuré : le gold POS est FR/EN, les 71 langues n'en ont pas",
                    "libellés courts (quelques mots) : la détection de langue y est défavorisée",
                    "les écritures de chaque langue sont une table (à relire)"],
    }
    p = pathlib.Path(a.sortie)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("langues", "concepts", "labels")}, ensure_ascii=False))
    print("script", res["script"])
    print("langue", {k: res["langue"][k] for k in ("justes", "total", "taux", "baseline")})


if __name__ == "__main__":
    main()

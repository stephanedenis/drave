#!/usr/bin/env python3
"""preparer_udhr.py — LE CORPUS UDHR PRÊT POUR LES MESURES : langues propres, articles propres, méta.

CE QUE LE PREMIER ESSAI A FAIT DE MAL ✗✓, ET POURQUOI C'EST INSTRUCTIF. J'avais exigé **3 000 caractères**
par langue pour la garder ✓ — un seuil pensé pour les écritures **alphabétiques** ✓. Il a rejeté **le chinois,
le gan, le hak, le canto** ✗✗ : un article chinois fait **47 caractères** et la Déclaration entière **2 792** ✓✓ —
*elle est COMPLÈTE, elle est simplement compacte* ✗✓. **C'est le quinzième piège de la nuit : un seuil
script-aveugle.** Le seuil doit dépendre de l'**écriture** ✓ (un caractère chinois porte 2 à 3 caractères latins
d'information ✓).

CE QU'IL FAIT :
  · garde les langues qui ont **30 articles** ✓ et dont le total dépasse un seuil **par écriture** ✓
    (1 200 caractères pour les écritures CJK ✓, 3 000 sinon ✓) ;
  · **retire les articles dégénérés** (< 8 caractères en CJK ✓, < 20 sinon ✓) au lieu de jeter la langue ✓✓ ;
  · garde les langues qui conservent **≥ 28 articles** ✓ ;
  · écrit : `udhr_train.txt` (les textes, pour l'entraînement ✓), `articles_propres.jsonl` (pour les mesures ✓),
    `meta.json` (écriture, nom, variante ✓) et la liste des **variantes** d'une même langue ✓.

Usage : python3 tools/preparer_udhr.py
"""
from __future__ import annotations
import json, pathlib, collections

CJK = {"Hans", "Hant", "Hani", "Jpan", "Hang"}


def seuil(script: str) -> int:
    return 8 if script in CJK else 20


def main() -> int:
    langues = [json.loads(l) for l in pathlib.Path("data/udhr/langues.jsonl").read_text().splitlines()]
    arts = [json.loads(l) for l in pathlib.Path("data/udhr/articles.jsonl").read_text().splitlines()]
    par_fichier = collections.defaultdict(list)
    pour_fichier = {L["fichier"]: L for L in langues}
    for a in arts:
        if isinstance(a["art"], int) and a["art"] >= 1:
            par_fichier[a["fichier"]].append(a)

    propres, rejets = [], []
    for L in sorted(langues, key=lambda x: x["fichier"]):
        a = sorted(par_fichier.get(L["fichier"], []), key=lambda x: x["art"])
        if len(a) < 30:
            rejets.append((L["fichier"], f"{len(a)} articles")); continue
        total = sum(len(x["texte"]) for x in a)
        mini = 1200 if L["script"] in CJK else 3000
        if total < mini:
            rejets.append((L["fichier"], f"{total} car. (< {mini} pour {L['script']})")); continue
        s = seuil(L["script"])
        gardes = [x for x in a if len(x["texte"]) >= s]
        if len(gardes) < 28:
            rejets.append((L["fichier"], f"{len(gardes)} articles non dégénérés")); continue
        for x in gardes:
            x["variante"] = L["fichier"].replace("udhr_", "").replace(".xml", "")
            x["script"] = L["script"]
        propres.append((L, gardes))

    lignes = []
    for L, gardes in propres:
        for x in gardes:
            lignes.append(x["texte"])
    corpus = "\n".join(lignes)
    pathlib.Path("data/udhr/udhr_train.txt").write_text(corpus, encoding="utf-8")
    with pathlib.Path("data/udhr/articles_propres.jsonl").open("w") as f:
        for L, gardes in propres:
            for x in gardes:
                f.write(json.dumps({k: x[k] for k in ("fichier", "iso3", "nom", "script", "art", "texte", "variante")},
                                   ensure_ascii=False) + "\n")
    meta = {L["fichier"]: {"iso3": L["iso3"], "nom": L["nom"], "script": L["script"], "sens": L["sens"],
                            "variante": L["fichier"].replace("udhr_", "").replace(".xml", ""),
                            "nb_articles": len(g)} for L, g in propres}
    pathlib.Path("data/udhr/meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=0))

    multi = {k: v for k, v in collections.Counter(L["iso3"] for L, _ in propres).items() if v > 1}
    print(f"  langues gardées : {len(propres)} · rejetées : {len(rejets)}")
    for f, r in rejets: print(f"    ✗ {f:26s} {r}")
    print(f"  corpus : {len(corpus)/1048576:.2f} Mo · {len(lignes)} articles")
    print(f"  écritures : {dict(collections.Counter(L['script'] for L, _ in propres).most_common(8))}")
    print(f"  langues à plusieurs variantes : {len(multi)} → {dict(sorted(multi.items(), key=lambda kv: -kv[1])[:10])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

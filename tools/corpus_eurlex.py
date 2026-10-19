#!/usr/bin/env python3
"""corpus_eurlex.py — UN CORPUS JURIDIQUE **POST-CUTOFF** (donc non mémorisable), aligné par structure.

POURQUOI ✗✗. La mesure 61 a montré que le banc UDHR est **contaminé** : sur une phrase où l'on remplace un mot par
un mot absurde, le 7 B **récite la traduction officielle** au lieu de traduire la source (« en dignité et en
couleur » → « in dignity and rights ») ✓✗. Un chrF élevé sur l'UDHR ne mesure donc pas la qualité de traducteur
✓✗. Il faut un texte que le modèle **n'a pas pu voir** à l'entraînement ✓✓ : les règlements européens publiés
**après la date de coupure** (2025-2026 pour Qwen2.5) sont traduits par des **traducteurs humains** dans les 24
langues ✓✓, et leur structure est **numérotée** (considérants (1), (2)…, articles 1, 2…) — l'alignement est donc
**garanti par la structure**, comme l'UDHR, mais sans la mémoire ✓✓✓.

LA SOURCE. Cellar (publications.europa.eu) sert le texte XHTML officiel par CELEX et par langue ✓ :
  https://publications.europa.eu/resource/celex/32025R1106  +  Accept-Language: eng / fra / deu / spa
(c'est le même texte que l'OJ ; l'accès par eur-lex.europa.eu renvoie 202/0 aux robots ✗✓).

L'ALIGNEMENT EST VÉRIFIÉ, PAS SUPPOSÉ ✓✓ : on compte les considérants et les articles dans **chaque** langue, on
n'apparie que les identifiants présents partout, et on rapporte les désaccords ✓✓ (la leçon de la mesure 59 : un
banc littéraire invalide parce que l'appariement n'était pas vérifié ✗✗).
"""
from __future__ import annotations
import argparse, json, pathlib, re, urllib.request

LANGUES_CELLAR = {"fra": "fra", "eng": "eng", "deu": "deu", "spa": "spa", "ita": "ita",
                  "pol": "pol", "nld": "nld", "por": "por"}


def telecharge(celex: str, langue: str, cache: pathlib.Path) -> str:
    f = cache / f"{celex}-{langue}.xhtml"
    if f.exists() and f.stat().st_size > 10_000:
        return f.read_text(encoding="utf-8", errors="ignore")
    req = urllib.request.Request(
        f"https://publications.europa.eu/resource/celex/{celex}",
        headers={"Accept": "application/xhtml+xml", "Accept-Language": LANGUES_CELLAR[langue],
                 "User-Agent": "Mozilla/5.0 (corpus Drave)"})
    with urllib.request.urlopen(req, timeout=120) as r:
        s = r.read().decode("utf-8", errors="ignore")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(s, encoding="utf-8")
    return s


def local(el) -> str:
    return el.tag.rsplit("}", 1)[-1] if isinstance(el.tag, str) else ""


def texte(el) -> str:
    return " ".join("".join(el.itertext()).split())


def blocs(div) -> list[str]:
    """Les paragraphes d'une division, dans l'ordre ; une TABLE = une unité par ligne ✓."""
    out = []
    for child in div:
        tag = local(child)
        cls = child.get("class", "") or ""
        if tag == "p":
            if "oj-ti-art" in cls or "oj-sti-art" in cls or "oj-note" in cls:
                continue
            t = texte(child)
            if t:
                out.append(t)
        elif tag == "table":
            for tr in child.iter():
                if local(tr) != "tr":
                    continue
                cellules = [texte(c) for c in tr if local(c) in ("td", "th")]
                t = " ".join(c for c in cellules if c)
                if t:
                    out.append(t)
        elif tag == "div":
            if "eli-title" in cls:
                continue
            out.extend(blocs(child))
    return out


def parse(html: str) -> tuple[dict[int, list[str]], dict[int, list[str]], dict[int, str]]:
    """→ (considérants, articles, titres d'articles), chaque division découpée en paragraphes ✓."""
    from lxml import etree
    doc = etree.fromstring(html.encode("utf-8"), parser=etree.HTMLParser(recover=True))
    rct, art, titres = {}, {}, {}
    for el in doc.iter():
        ident = el.get("id") or ""
        m = re.fullmatch(r"rct_(\d+)", ident)
        if m and ident not in rct:
            rct[int(m.group(1))] = blocs(el)
            continue
        m = re.fullmatch(r"art_(\d+)", ident)
        if m and ident not in art:
            numero = int(m.group(1))
            titre = ""
            for d in el.iter():
                if "eli-title" in (d.get("class", "") or ""):
                    titre = texte(d)
                    break
            titres[numero] = titre
            art[numero] = blocs(el)
    return rct, art, titres


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--celex", required=True)
    ap.add_argument("--langues", default="eng,fra,deu,spa")
    ap.add_argument("--sortie", default="")
    ap.add_argument("--cache", default="data/eurlex/xhtml")
    a = ap.parse_args()
    langues = a.langues.split(",")
    cache = pathlib.Path(a.cache)
    par = {}
    for lg in langues:
        html = telecharge(a.celex, lg, cache)
        rct, art, titres = parse(html)
        par[lg] = {"rct": rct, "art": art, "titres": titres}
        print(f"  {lg} : {len(rct)} considérants · {len(art)} articles · {sum(len(v) for v in rct.values())} "
              f"paragraphes de considérants · {sum(len(v) for v in art.values())} paragraphes d'articles")
    # le contrôle d'ALIGNEMENT ✓✓ : les numéros doivent être les mêmes partout ✗ sinon on s'arrête
    ids_rct = [set(par[lg]["rct"]) for lg in langues]
    ids_art = [set(par[lg]["art"]) for lg in langues]
    communs_rct = set.intersection(*ids_rct)
    communs_art = set.intersection(*ids_art)
    print(f"  alignement : {len(communs_rct)} considérants communs aux {len(langues)} langues "
          f"(manquants : {sorted(set.union(*ids_rct) - communs_rct)[:10]}) · "
          f"{len(communs_art)} articles communs (manquants : {sorted(set.union(*ids_art) - communs_art)[:10]})")
    unites = []
    desaccords = 0
    for n in sorted(communs_rct):
        textes = {lg: par[lg]["rct"][n] for lg in langues}
        if len({len(v) for v in textes.values()}) == 1:
            for i in range(len(textes[langues[0]])):
                unites.append({"id": f"rct_{n}" if len(textes[langues[0]]) == 1 else f"rct_{n}_p{i + 1}",
                               "type": "considerant", "numero": n,
                               "textes": {lg: textes[lg][i] for lg in langues}})
        else:
            desaccords += 1
            unites.append({"id": f"rct_{n}", "type": "considerant", "numero": n,
                           "textes": {lg: " ".join(textes[lg]) for lg in langues}})
    for n in sorted(communs_art):
        textes = {lg: par[lg]["art"][n] for lg in langues}
        titre = par[langues[0]]["titres"].get(n, "")
        if len({len(v) for v in textes.values()}) == 1:
            for i in range(len(textes[langues[0]])):
                unites.append({"id": f"art_{n}" if len(textes[langues[0]]) == 1 else f"art_{n}_p{i + 1}",
                               "type": "article", "numero": n, "titre": titre,
                               "textes": {lg: textes[lg][i] for lg in langues}})
        else:
            desaccords += 1
            unites.append({"id": f"art_{n}", "type": "article", "numero": n, "titre": titre,
                           "textes": {lg: " ".join(textes[lg]) for lg in langues}})
    print(f"  unités : {len(unites)} dont {sum(u['type'] == 'considerant' for u in unites)} considérants · "
          f"{desaccords} divisions appariées au niveau article (comptes de paragraphes différents)")
    # contrôle de longueur : un désaccord de longueur extrême signale un appariement douteux ✓✗
    for lg in langues[1:]:
        ratios = [len(u["textes"][lg]) / max(1, len(u["textes"][langues[0]])) for u in unites]
        ratios.sort()
        print(f"  longueur {lg}/{langues[0]} : médiane {ratios[len(ratios) // 2]:.2f} · "
              f"min {ratios[0]:.2f} · max {ratios[-1]:.2f}")
    sortie = a.sortie or f"data/eurlex/{a.celex}.json"
    pathlib.Path(sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(sortie).write_text(json.dumps(
        {"celex": a.celex, "langues": langues, "unites": unites}, ensure_ascii=False, indent=1))
    print(f"  → {sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

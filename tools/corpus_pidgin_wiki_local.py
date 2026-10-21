#!/usr/bin/env python3
"""corpus_pidgin_wiki_local.py — les paires Wikipédia pidgin-anglais depuis le CONTENU LOCAL (sans API).

POURQUOI ✓✓. La Wikipédia pidgin est moderne, non religieuse (le registre que la leçon 96-102 demande) ✓✓ ; le
dump local `data/pidgin/pcmwiki-latest-pages-articles.xml.bz2` et ses `langlinks` donnent les articles et leurs
équivalents anglais ✓✓ ; l'index local `data/pidgin/en_index.tsv` (construit sur les 28 126 morceaux Nipada)
retrouve les textes anglais **sans API** ✓✓.
"""
from __future__ import annotations
import bz2, gzip, json, os, re, sqlite3, sys
import xml.etree.ElementTree as ET

RACINE_EN = "/home/stephane/Data13TB/stephane/nipada/wikipedia_decompressed/en"
DUMP = "data/pidgin/pcmwiki-latest-pages-articles.xml"
LANGS = "data/pidgin/pcmwiki-latest-langlinks.sql.gz"
INDEX = "data/pidgin/en_titles.tsv"
DB_EN = "/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_wikipedia_en.db"


def nettoie(t: str) -> str:
    t = re.sub(r"<ref[^>]*>.*?</ref>", " ", t, flags=re.S)
    t = re.sub(r"<ref[^>]*/>", " ", t)
    for _ in range(5):  # templates imbriqués (infobox)
        t = re.sub(r"\{\{[^{}]*\}\}", " ", t)
    t = re.sub(r"\{\|.*?\|\}", " ", t, flags=re.S)  # tableaux
    t = re.sub(r"^\s*\|.*$", " ", t, flags=re.M)     # lignes de paramètres
    t = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[https?://[^\s\]]+\s*([^\]]*)\]", r"\1", t)
    t = re.sub(r"''+", "", t)
    t = re.sub(r"^=+.*?=+$", " ", t, flags=re.M)
    t = re.sub(r"<[^>]+>", " ", t)
    return " ".join(t.split())


def pages_pcm() -> tuple[dict[str, str], dict[str, str]]:
    """(id → titre, titre → texte brut) pour les articles (namespace 0, sans redirect)."""
    ids, textes = {}, {}
    with open(DUMP, "rb") as f:
        for ev, el in ET.iterparse(f, events=("end",)):
            if el.tag != "{http://www.mediawiki.org/xml/export-0.11/}page":
                continue
            titre = el.findtext("{http://www.mediawiki.org/xml/export-0.11/}title") or ""
            pid = el.findtext("{http://www.mediawiki.org/xml/export-0.11/}id") or ""
            redirect = el.find("{http://www.mediawiki.org/xml/export-0.11/}redirect") is not None
            ns = el.findtext("{http://www.mediawiki.org/xml/export-0.11/}ns")
            texte = el.findtext(".//{http://www.mediawiki.org/xml/export-0.11/}text") or ""
            if ns == "0" and not redirect and titre:
                ids[pid] = titre
                textes[titre] = texte
            el.clear()
    return ids, textes


def langlinks_en(ids: dict[str, str]) -> dict[str, str]:
    """titre pcm → titre anglais."""
    out = {}
    with gzip.open(LANGS, "rt", encoding="utf-8", errors="ignore") as f:
        for ligne in f:
            for m in re.finditer(r"\((\d+),'en','((?:[^'\\]|\\.)*)'", ligne):
                pid, en = m.group(1), m.group(2).replace("\\'", "'")
                if pid in ids:
                    out[ids[pid]] = en
    return out


def lead(t: str, n: int = 2) -> str:
    """Les n premières phrases (le texte anglais local est souvent mono-ligne)."""
    t = " ".join(t.split())
    phrases = re.split(r"(?<=[.!?])\s+", t)
    return " ".join(phrases[:n])


def charge_en(titre: str, index: dict[str, str], cache: dict) -> str | None:
    f = index.get(titre)
    if not f:
        return None
    if f not in cache:
        try:
            cache[f] = json.load(open(os.path.join(RACINE_EN, f), encoding="utf-8"))
        except Exception:
            cache[f] = {}
    for a in cache[f].get("articles", []):
        if a.get("title") == titre:
            return a.get("text")
    return None


def main() -> int:
    ids, textes = pages_pcm()
    print(f"  {len(ids)} articles pidgin (namespace 0, sans redirect)")
    liens = langlinks_en(ids)
    print(f"  {len(liens)} avec un lien anglais")
    en_db = {}
    if os.path.exists(DB_EN):
        c = sqlite3.connect(f"file:{DB_EN}?mode=ro", uri=True)
        en_db = {t: txt for t, txt in c.execute("select title, raw_text from backlog") if t and txt}
        print(f"  {len(en_db)} textes anglais (Panini backlog_wikipedia_en.db)")
    index = {}
    if os.path.exists(INDEX):
        with open(INDEX, encoding="utf-8") as f:
            for l in f:
                parts = l.rstrip("\n").split("\t")
                if len(parts) >= 2:
                    index.setdefault(parts[0], parts[-1])
        print(f"  {len(index)} titres anglais indexés (Nipada)")
    cache, paires = {}, []
    for tp, te in liens.items():
        # le lien anglais peut commencer par 'en:' ; on retire
        te = te.split(":", 1)[1] if te.startswith("en:") and len(te.split(":", 1)[1]) > 0 else te
        te = te.replace("_", " ")  # les langlinks stockent les titres avec des soulignés
        en = en_db.get(te) or en_db.get(te.replace(" ", "_")) or charge_en(te, index, cache)
        if not en:
            continue
        a_, b_ = lead(nettoie(textes.get(tp, ""))), lead(nettoie(en))
        if len(a_) > 40 and len(b_) > 40 and 0.3 < len(b_) / max(1, len(a_)) < 3.5:
            paires.append({"en": b_, "pcm": a_, "article": tp})
    json.dump(paires, open("data/pidgin/wiki_local.json", "w"), ensure_ascii=False, indent=0)
    print(f"  {len(paires)} paires → data/pidgin/wiki_local.json")
    for x in paires[:2]:
        print("   EN :", x["en"][:110]); print("   PCM:", x["pcm"][:110])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

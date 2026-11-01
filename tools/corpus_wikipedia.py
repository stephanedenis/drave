#!/usr/bin/env python3
"""corpus_wikipedia.py — des corpus de prose par langue depuis les bases Wikipédia v14.

POURQUOI CE FICHIER. L'inventaire du disque a montré que le seul stock local d'un autre ordre de
grandeur que le dépôt est Wikipédia : 10 bases `xxwiki_v14.db`, ~2,75 M d'articles pour le seul
français, 7,0 Go de résumés en texte déjà débalisé. Ce script en fait des corpus **propres,
dédupliqués et découpés** — un par langue — avec leur provenance et leurs limites écrites.

CE QUE LE CORPUS EST. Le champ `summary` de la base est le **début** de l'article (tronqué à
8 000 caractères), déjà débalisé (les dates des modèles ont disparu, quelques artefacts de
templates restent). C'est de la **prose de lead**, pas l'article entier : c'est dit dans chaque
manifeste. Le texte intégral demanderait le dump `xml.bz2` et un débaliseur complet.

CE QUE LE SCRIPT FAIT, PAR LANGUE :
1. lit `articles(page_id, title, summary, n_chars)` en lecture seule ;
2. filtre (n_chars >= --min-chars), nettoie les espaces et les balises résiduelles ;
3. déduplique les **articles** (empreinte exacte du texte normalisé) ;
4. découpe en **tronçons** aux frontières de mots, déduplique les **tronçons** exacts (train) ;
5. sépare train / val / test par **article** (hash salé de page_id) ;
6. écrit `train.txt`, `val.txt`, `test.txt` et un manifeste JSON (chiffres, empreintes, limites).

Usage :
  python3 tools/corpus_wikipedia.py --db .../frwiki_v14.db            # une langue
  python3 tools/corpus_wikipedia.py --toutes-les-langues              # les 10 bases
  python3 tools/corpus_wikipedia.py --max-articles 5000 --sortie /tmp/essai
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import pathlib
import re
import sqlite3
import sys

BASE_DB = pathlib.Path("/home/stephane/Data13TB/stephane/data/wikipedia/db")
RACINE = pathlib.Path(__file__).resolve().parent.parent
TAGS = re.compile(r"<[^>]+>")
ESPACES = re.compile(r"\s+")
CONTROLES = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
JOINTURE = re.compile(r"(?<=[a-zà-ÿœæ])(?=[A-ZÀ-ÝŒÆ])")
APOSTROPHE_L = re.compile(r"(?<![A-Za-zÀ-ÿ'’])l(?=[A-ZÀ-Ý])")
APOSTROPHE_D = re.compile(r"(?<![A-Za-zÀ-ÿ'’])d(?=[A-ZÀ-Ý])")


def nettoie(texte: str) -> str:
    t = html.unescape(texte)
    t = TAGS.sub(" ", t)
    t = CONTROLES.sub(" ", t)
    t = t.replace("\u00a0", " ").replace("\u202f", " ")
    # le débalisage de la base colle parfois les phrases et perd l'apostrophe : « bourbonnaiseSa
    # famille », « lOfficial ». On remet l'espace et l'apostrophe — mesuré sur le FR : ~92 700
    # jointures minuscule→majuscule dans 200 Mo, soit ~3,2 M sur le corpus.
    t = JOINTURE.sub(" ", t)
    t = APOSTROPHE_L.sub("l'", t)
    t = APOSTROPHE_D.sub("d'", t)
    return ESPACES.sub(" ", t).strip()


def empreinte(texte: str, taille: int = 16) -> str:
    return hashlib.blake2b(texte.encode("utf-8"), digest_size=taille).hexdigest()


def troncons(texte: str, taille: int):
    debut = 0
    while debut < len(texte):
        fin = min(debut + taille, len(texte))
        if fin < len(texte):
            coupe = texte.rfind(" ", debut + taille // 2, fin)
            if coupe > debut:
                fin = coupe
        morceau = texte[debut:fin].strip()
        if morceau:
            yield morceau
        debut = fin


def construire(db: pathlib.Path, sortie: pathlib.Path, manifeste: pathlib.Path,
               langue: str, min_chars: int, chunk: int, val: float, test: float,
               graine: int, max_articles: int) -> dict:
    sortie.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(f"file:{db.resolve()}?mode=ro", uri=True)
    con.text_factory = str
    total = con.execute("select count(*) from articles").fetchone()[0]
    seuil_val, seuil_test = int(val * 1000), int((val + test) * 1000)
    fichiers = {nom: (sortie / f"{nom}.txt").open("w", encoding="utf-8")
                for nom in ("train", "val", "test")}
    vus_articles: set[str] = set()
    vus_troncons: set[str] = set()
    stats = {"langue": langue, "articles_db": total, "articles_lus": 0, "articles_gardes": 0,
             "articles_courts": 0, "articles_vides": 0, "articles_doublons": 0,
             "caracteres_gardes": 0, "troncons": 0, "troncons_doublons": 0,
             "octets": {"train": 0, "val": 0, "test": 0},
             "articles": {"train": 0, "val": 0, "test": 0},
             "troncons_par_split": {"train": 0, "val": 0, "test": 0}}
    for page_id, titre, resume, n_chars in con.execute(
            "select page_id, title, summary, n_chars from articles "
            "where n_chars >= ? and summary is not null order by page_id", (min_chars,)):
        stats["articles_lus"] += 1
        if max_articles and stats["articles_lus"] > max_articles:
            break
        texte = nettoie(resume or "")
        if len(texte) < min_chars // 2:
            stats["articles_vides"] += 1
            continue
        marque = empreinte(texte)
        if marque in vus_articles:
            stats["articles_doublons"] += 1
            continue
        vus_articles.add(marque)
        h = int(empreinte(f"{graine}:{page_id}", 8), 16) % 1000
        split = "val" if h < seuil_val else ("test" if h < seuil_test else "train")
        morceaux = []
        for morceau in troncons(texte, chunk):
            if split == "train":
                m = empreinte(morceau)
                if m in vus_troncons:
                    stats["troncons_doublons"] += 1
                    continue
                vus_troncons.add(m)
            morceaux.append(morceau)
        if not morceaux:
            continue
        fichiers[split].write("\n\n".join(morceaux) + "\n\n")
        stats["articles_gardes"] += 1
        stats["articles"][split] += 1
        stats["troncons"] += len(morceaux)
        stats["troncons_par_split"][split] += len(morceaux)
        stats["caracteres_gardes"] += len(texte)
        if stats["articles_lus"] % 200000 == 0:
            print(f"  [{langue}] {stats['articles_lus']}/{total} lus · "
                  f"{stats['articles_gardes']} gardés · {stats['troncons']} tronçons", flush=True)
    for f in fichiers.values():
        f.close()
    con.close()
    stats["mots_estimes"] = int(stats["caracteres_gardes"] / 6.2)
    stats["note_mots"] = ("caractères / 6,2 : estimation pour les langues à espaces ; pour le "
                          "japonais et le chinois, le caractère est l'unité de volume")
    for nom in ("train", "val", "test"):
        chemin = sortie / f"{nom}.txt"
        stats["octets"][nom] = chemin.stat().st_size
        h = hashlib.sha256()
        with chemin.open("rb") as f:
            for bloc in iter(lambda: f.read(1 << 20), b""):
                h.update(bloc)
        stats[f"sha256_{nom}"] = h.hexdigest()
    manifeste.parent.mkdir(parents=True, exist_ok=True)
    manifeste.write_text(json.dumps({
        "date": "2026-11-01", "ligne": "Données", "langue": langue,
        "nature": f"corpus Wikipédia {langue} (résumés)",
        "source": {"db": db.as_posix(), "table": "articles", "champ": "summary",
                   "octets_db": db.stat().st_size,
                   "note": "résumé d'article tronqué à 8 000 caractères, déjà débalisé"},
        "methode": {
            "filtre": f"n_chars >= {min_chars}",
            "nettoyage": "entités HTML, balises résiduelles, espaces, caractères de contrôle ; espace aux jointures minuscule→majuscule et apostrophe restaurée devant majuscule",
            "deduplication_articles": "empreinte BLAKE2b du texte normalisé, première occurrence gardée",
            "deduplication_troncons": f"tronçons de {chunk} caractères coupés aux mots, BLAKE2b, première occurrence gardée (train seulement)",
            "split": f"hash salé (graine {graine}) de page_id : {val:.0%} val, {test:.0%} test, le reste train ; un article n'est que dans un split",
            "mots": "caractères / 6,2 (estimation)"},
        **stats,
        "licence": "Wikipédia : CC-BY-SA 4.0 (et GFDL) — attribution et partage à l'identique ; corpus local, non diffusé",
        "limites": [
            "résumés tronqués à 8 000 caractères (le lead et le début des sections), pas l'article entier",
            "artefacts de débalisage : dates de modèles vides (« né le à »), parenthèses de prononciation, titres de sections restés dans le texte",
            "déduplication exacte seulement : les quasi-doublons (stubs similaires) restent",
            "le texte intégral demanderait le dump xml.bz2 et un débaliseur complet"]},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: stats[k] for k in ("langue", "articles_lus", "articles_gardes",
                                             "articles_doublons", "caracteres_gardes",
                                             "mots_estimes", "octets")},
                     ensure_ascii=False, indent=1), flush=True)
    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", type=pathlib.Path, default=BASE_DB / "frwiki_v14.db")
    ap.add_argument("--sortie", type=pathlib.Path)
    ap.add_argument("--manifeste", type=pathlib.Path)
    ap.add_argument("--langue", default=None, help="déduite du nom de la base si absente")
    ap.add_argument("--toutes-les-langues", action="store_true")
    ap.add_argument("--force", action="store_true", help="refaire un corpus déjà présent")
    ap.add_argument("--min-chars", type=int, default=300)
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--val", type=float, default=0.05)
    ap.add_argument("--test", type=float, default=0.05)
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--max-articles", type=int, default=0)
    args = ap.parse_args()
    if args.toutes_les_langues:
        langues = []
        for db in sorted(BASE_DB.glob("*wiki_v14.db")):
            langue = db.stem.split("wiki")[0]
            sortie = RACINE / "data" / f"corpus_wiki_{langue}"
            manifeste = RACINE / "reports" / f"corpus-wiki-{langue}.json"
            if manifeste.exists() and not args.force:
                print(f"  [{langue}] déjà fait ({manifeste.name}), ignoré", flush=True)
                continue
            print(f"===== {langue} ({db.stat().st_size / 1e9:.1f} Go) =====", flush=True)
            construire(db, sortie, manifeste, langue, args.min_chars, args.chunk,
                       args.val, args.test, args.graine, args.max_articles)
        return 0
    langue = args.langue or args.db.stem.split("wiki")[0]
    sortie = args.sortie or (RACINE / "data" / f"corpus_wiki_{langue}")
    manifeste = args.manifeste or (RACINE / "reports" / f"corpus-wiki-{langue}.json")
    construire(args.db, sortie, manifeste, langue, args.min_chars, args.chunk,
               args.val, args.test, args.graine, args.max_articles)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""corpus_wikipedia.py — un corpus de prose française depuis la base Wikipédia v14.

POURQUOI CE FICHIER. L'inventaire du disque a montré que le seul stock local d'un autre ordre de
grandeur que le dépôt est Wikipédia : 2,75 M d'articles, 7,0 Go de résumés en texte déjà débalisé
dans `data/wikipedia/db/frwiki_v14.db`. Ce script en fait un corpus **propre, dédupliqué et
découpé** pour l'entraînement, avec sa provenance et ses limites écrites.

CE QUE LE CORPUS EST. Le champ `summary` de la base est le **début** de l'article (tronqué à
8 000 caractères), déjà débalisé (les dates des modèles ont disparu, quelques artefacts de
templates restent). C'est de la **prose de lead**, pas l'article entier : c'est dit dans le
manifeste. Le texte intégral demanderait le dump `xml.bz2` et un débaliseur complet.

CE QUE LE SCRIPT FAIT :
1. lit `articles(page_id, title, summary, n_chars)` en lecture seule ;
2. filtre (n_chars >= --min-chars), nettoie les espaces et les balises résiduelles ;
3. déduplique les **articles** (empreinte exacte du texte normalisé) ;
4. découpe en **tronçons de 8 Ko** aux frontières de mots, déduplique les **tronçons** exacts
   (le même paragraphe répété dans mille articles ne compte qu'une fois) ;
5. sépare train / val / test par **article** (hash salé de page_id) : un article n'est jamais
   dans deux splits ;
6. écrit `train.txt`, `val.txt`, `test.txt` et un manifeste JSON avec les chiffres, les
   empreintes et les limites.

Usage :
  python3 tools/corpus_wikipedia.py --db data/wikipedia/db/frwiki_v14.db --max-articles 5000
  python3 tools/corpus_wikipedia.py --db ... --sortie data/corpus_wiki_fr
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sqlite3
import sys
import time

RACINE = None  # rempli dans main()
TAGS = re.compile(r"<[^>]+>")
ESPACES = re.compile(r"\s+")
CONTROLES = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def nettoie(texte: str) -> str:
    t = html.unescape(texte)
    t = TAGS.sub(" ", t)
    t = CONTROLES.sub(" ", t)
    t = t.replace("\u00a0", " ").replace("\u202f", " ")
    # le débalisage de la base colle parfois les phrases et perd l'apostrophe : « bourbonnaiseSa
    # famille », « lOfficial ». On remet l'espace et l'apostrophe — mesuré : ~92 700 jointures
    # minuscule→majuscule dans 200 Mo, soit ~3,2 M sur le corpus.
    t = re.sub(r"(?<=[a-zà-ÿœæ])(?=[A-ZÀ-ÝŒÆ])", " ", t)
    t = re.sub(r"(?<![A-Za-zÀ-ÿ'’])l(?=[A-ZÀ-Ý])", "l'", t)
    t = re.sub(r"(?<![A-Za-zÀ-ÿ'’])d(?=[A-ZÀ-Ý])", "d'", t)
    t = ESPACES.sub(" ", t).strip()
    return t


def empreinte(texte: str, taille: int = 16) -> str:
    return hashlib.blake2b(texte.encode("utf-8"), digest_size=taille).hexdigest()


def troncons(texte: str, taille: int):
    """Des tronçons de ~taille octets, coupés aux frontières de mots, sans perdre de texte."""
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


def main() -> int:
    global RACINE
    import pathlib
    RACINE = pathlib.Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__)
    # la base Wikipédia vit sur le volume de données, pas dans le dépôt
    defaut_db = RACINE.parents[1] / "data/wikipedia/db/frwiki_v14.db"
    ap.add_argument("--db", type=pathlib.Path, default=defaut_db)
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "data/corpus_wiki_fr")
    ap.add_argument("--min-chars", type=int, default=300)
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--val", type=float, default=0.05)
    ap.add_argument("--test", type=float, default=0.05)
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--max-articles", type=int, default=0, help="0 = tous (test sinon)")
    ap.add_argument("--manifeste", type=pathlib.Path,
                    default=RACINE / "reports/corpus-wiki-fr.json")
    args = ap.parse_args()

    args.sortie.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(f"file:{args.db.resolve()}?mode=ro", uri=True)
    con.text_factory = str
    total = con.execute("select count(*) from articles").fetchone()[0]
    seuil_val, seuil_test = int(args.val * 1000), int((args.val + args.test) * 1000)
    fichiers = {nom: (args.sortie / f"{nom}.txt").open("w", encoding="utf-8")
                for nom in ("train", "val", "test")}
    vus_articles: set[str] = set()
    vus_troncons: set[str] = set()
    stats = {"articles_db": total, "articles_lus": 0, "articles_gardes": 0,
             "articles_courts": 0, "articles_vides": 0, "articles_doublons": 0,
             "caracteres_gardes": 0, "troncons": 0, "troncons_doublons": 0,
             "octets": {"train": 0, "val": 0, "test": 0},
             "articles": {"train": 0, "val": 0, "test": 0},
             "troncons_par_split": {"train": 0, "val": 0, "test": 0}}
    # un article = un bloc ; on garde les tronçons dédupliqués, séparés par deux sauts de ligne
    for page_id, titre, resume, n_chars in con.execute(
            "select page_id, title, summary, n_chars from articles "
            "where n_chars >= ? and summary is not null order by page_id", (args.min_chars,)):
        stats["articles_lus"] += 1
        if args.max_articles and stats["articles_lus"] > args.max_articles:
            break
        texte = nettoie(resume or "")
        if len(texte) < args.min_chars // 2:
            stats["articles_vides"] += 1
            continue
        marque = empreinte(texte)
        if marque in vus_articles:
            stats["articles_doublons"] += 1
            continue
        vus_articles.add(marque)
        h = int(empreinte(f"{args.graine}:{page_id}", 8), 16) % 1000
        split = "val" if h < seuil_val else ("test" if h < seuil_test else "train")
        morceaux = []
        for morceau in troncons(texte, args.chunk):
            if split == "train":
                m = empreinte(morceau)
                if m in vus_troncons:
                    stats["troncons_doublons"] += 1
                    continue
                vus_troncons.add(m)
            morceaux.append(morceau)
        if not morceaux:
            continue
        bloc = "\n\n".join(morceaux)
        f = fichiers[split]
        f.write(bloc + "\n\n")
        stats["articles_gardes"] += 1
        stats["articles"][split] += 1
        stats["troncons"] += len(morceaux)
        stats["troncons_par_split"][split] += len(morceaux)
        stats["caracteres_gardes"] += len(texte)
        if stats["articles_lus"] % 200000 == 0:
            print(f"  {stats['articles_lus']}/{total} lus · {stats['articles_gardes']} gardés "
                  f"· {stats['troncons']} tronçons", flush=True)
    for f in fichiers.values():
        f.close()
    con.close()
    # mots ~ caractères / 6,2 en français (mesure sur le corpus du dépôt)
    stats["mots_estimes"] = int(stats["caracteres_gardes"] / 6.2)
    stats["duree_s"] = None
    # les empreintes des fichiers pour le manifeste
    for nom in ("train", "val", "test"):
        chemin = args.sortie / f"{nom}.txt"
        stats["octets"][nom] = chemin.stat().st_size
        h = hashlib.sha256()
        with chemin.open("rb") as f:
            for bloc in iter(lambda: f.read(1 << 20), b""):
                h.update(bloc)
        stats[f"sha256_{nom}"] = h.hexdigest()
    manifeste = {
        "date": "2026-11-01", "ligne": "Données", "nature": "corpus Wikipédia FR (résumés)",
        "source": {"db": args.db.as_posix(), "table": "articles", "champ": "summary",
                   "octets_db": args.db.stat().st_size,
                   "note": "résumé d'article tronqué à 8 000 caractères, déjà débalisé"},
        "methode": {
            "filtre": f"n_chars >= {args.min_chars}",
            "nettoyage": "entités HTML, balises résiduelles, espaces, caractères de contrôle ; espace aux jointures minuscule→majuscule et apostrophe restaurée devant majuscule",
            "deduplication_articles": "empreinte BLAKE2b du texte normalisé, première occurrence gardée",
            "deduplication_troncons": f"tronçons de {args.chunk} caractères coupés aux mots, BLAKE2b, première occurrence gardée (train seulement)",
            "split": f"hash salé (graine {args.graine}) de page_id : {args.val:.0%} val, {args.test:.0%} test, le reste train ; un article n'est que dans un split",
            "mots": "caractères / 6,2 (estimation)"},
        **stats,
        "licence": "Wikipédia : CC-BY-SA 4.0 (et GFDL) — attribution et partage à l'identique ; corpus local, non diffusé",
        "limites": [
            "résumés tronqués à 8 000 caractères (le lead et le début des sections), pas l'article entier",
            "artefacts de débalisage : dates de modèles vides (« né le à »), parenthèses de prononciation",
            "déduplication exacte seulement : les quasi-doublons (stubs similaires) restent",
            "le texte intégral demanderait le dump xml.bz2 et un débaliseur complet"]}
    args.manifeste.parent.mkdir(parents=True, exist_ok=True)
    args.manifeste.write_text(json.dumps(manifeste, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8")
    print(json.dumps({k: stats[k] for k in ("articles_lus", "articles_gardes", "articles_doublons",
                                             "troncons", "troncons_doublons", "caracteres_gardes",
                                             "mots_estimes", "octets")}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

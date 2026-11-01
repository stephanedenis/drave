#!/usr/bin/env python3
"""corpus_wikipedia_texte.py — le texte INTÉGRAL des articles Wikipédia, par langue.

POURQUOI CE FICHIER. Les corpus `corpus_wiki_<langue>` sont des **résumés** tronqués à 8 000
caractères (le champ `summary` de la base v14). N2 a besoin de la **prose entière** : ce script
lit le dump `xxwiki-latest-pages-articles-multistream.xml.bz2`, débalise le wikitexte et écrit
`train.txt`, `val.txt`, `test.txt` — même nettoyage, même déduplication exacte, même split par
article que `corpus_wikipedia.py`.

CE QUE LE DÉBALISEUR FAIT, ET CE QU'IL PERD. Il retire commentaires, références, tableaux,
modèles (par itérations), fichiers et catégories, garde le **libellé** des liens, les titres de
sections, le texte des listes ; il remplace les liens externes par leur libellé. Il ne comprend
pas la sémantique des modèles : les **infobox** et les **dates de modèles** disparaissent, les
formules `<math>` sont retirées, les tableaux sont perdus. C'est un débaliseur **mesuré** : la
fiche donne le taux de résidus (`{{`, `[[`, `<`) et un échantillon.

Usage :
  python3 tools/corpus_wikipedia_texte.py --max-articles 100000       # pilote
  python3 tools/corpus_wikipedia_texte.py                            # l'article entier, 2,5 M
"""
from __future__ import annotations

import argparse
import bz2
import hashlib
import html
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

RACINE = pathlib.Path(__file__).resolve().parent.parent
BASE = pathlib.Path("/home/stephane/Data13TB/stephane/data/wikipedia/dumps")
TAGS_MEDIA = re.compile(r"<(gallery|math|timeline|score|imagemap|references|chem|ce|graph)\b.*?</\1>",
                        re.S | re.I)
TAGS = re.compile(r"<[^>]+>")
COMMENT = re.compile(r"<!--.*?-->", re.S)
REF = re.compile(r"<ref\b[^>]*/>|<ref\b[^>]*>.*?</ref>", re.S | re.I)
TABLE = re.compile(r"\{\|.*?\|\}", re.S)
MODELE = re.compile(r"\{\{[^{}]*\}\}")
FICHIER = re.compile(r"\[\[(?:Fichier|File|Image|Catégorie|Category|Modèle|Template)\s*:.*?\]\]",
                     re.S | re.I)
LIEN = re.compile(r"\[\[([^\]|]*)\|([^\]]*)\]\]")
LIEN_SIMPLE = re.compile(r"\[\[([^\]]*)\]\]")
EXTERNE = re.compile(r"\[https?://[^\s\]]+(?:\s+([^\]]*))?\]")
TITRE = re.compile(r"^=+\s*(.*?)\s*=+\s*$", re.M)
PUCE = re.compile(r"^[*#:;]+\s*", re.M)
ESPACES = re.compile(r"[ \t]+")
LIGNES = re.compile(r"\n\s*\n+")
MAGIE = re.compile(r"__[A-Z]+__")


def nettoie_wikitext(texte: str) -> str:
    t = COMMENT.sub("", texte)
    t = REF.sub("", t)
    t = TAGS_MEDIA.sub("", t)
    t = TABLE.sub("", t)
    for _ in range(30):  # modèles imbriqués, de l'intérieur vers l'extérieur
        t2 = MODELE.sub("", t)
        if t2 == t:
            break
        t = t2
    t = re.sub(r"\{\{[^{}]*$", "", t)
    t = FICHIER.sub("", t)
    for _ in range(5):  # les liens de légende peuvent être imbriqués
        t2 = LIEN.sub(r"\2", t)
        if t2 == t:
            break
        t = t2
    t = LIEN_SIMPLE.sub(r"\1", t)
    t = EXTERNE.sub(lambda m: m.group(1) or "", t)
    t = TAGS.sub("", t)
    t = t.replace("'''", "").replace("''", "")
    t = TITRE.sub(r"\1", t)
    t = PUCE.sub("", t)
    t = MAGIE.sub("", t)
    t = html.unescape(t)
    t = t.replace("\u00a0", " ").replace("\u202f", " ")
    t = ESPACES.sub(" ", t)
    t = LIGNES.sub("\n\n", t)
    return t.strip()


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


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--langue", default="fr")
    ap.add_argument("--dump", type=pathlib.Path, help="par défaut dumps/<langue>/<langue>wiki-…xml.bz2")
    ap.add_argument("--sortie", type=pathlib.Path)
    ap.add_argument("--manifeste", type=pathlib.Path)
    ap.add_argument("--min-chars", type=int, default=300)
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--val", type=float, default=0.05)
    ap.add_argument("--test", type=float, default=0.05)
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--max-articles", type=int, default=0)
    args = ap.parse_args()
    if args.dump is None:
        candidats = sorted((BASE / args.langue).glob("*pages-articles-multistream.xml.bz2"))
        if not candidats:
            sys.exit(f"aucun dump pour {args.langue} dans {BASE / args.langue}")
        args.dump = candidats[0]
    args.sortie = args.sortie or RACINE / "data" / f"corpus_wiki_{args.langue}_texte"
    args.manifeste = args.manifeste or RACINE / "reports" / f"corpus-wiki-{args.langue}-texte.json"
    args.sortie.mkdir(parents=True, exist_ok=True)
    seuil_val, seuil_test = int(args.val * 1000), int((args.val + args.test) * 1000)
    fichiers = {n: (args.sortie / f"{n}.txt").open("w", encoding="utf-8") for n in ("train", "val", "test")}
    vus: set[str] = set()
    vus_troncons: set[str] = set()
    stats = {"langue": args.langue, "dump": args.dump.as_posix(),
             "dump_octets": args.dump.stat().st_size,
             "articles_lus": 0, "articles_gardes": 0, "articles_rediriges": 0,
             "articles_hors_ns": 0, "articles_courts": 0, "articles_doublons": 0,
             "caracteres_gardes": 0, "troncons": 0, "troncons_doublons": 0,
             "octets": {"train": 0, "val": 0, "test": 0},
             "articles": {"train": 0, "val": 0, "test": 0},
             "residus": {"modele": 0, "lien": 0, "balise": 0},
             "echantillon": ""}
    with bz2.open(args.dump, "rb") as flux:
        for event, elem in ET.iterparse(flux, events=("end",)):
            if local(elem.tag) != "page":
                continue
            stats["articles_lus"] += 1
            if args.max_articles and stats["articles_gardes"] >= args.max_articles:
                break
            ns = elem.findtext("{*}ns") or "0"
            redsh = elem.find("{*}redirect")
            titre = elem.findtext("{*}title") or ""
            texte = elem.findtext("{*}revision/{*}text") or elem.findtext(".//{*}text") or ""
            pid = elem.findtext("{*}id") or str(stats["articles_lus"])
            elem.clear()
            if ns != "0":
                stats["articles_hors_ns"] += 1
                continue
            if redsh is not None or texte.upper().startswith("#REDIRECTION"):
                stats["articles_rediriges"] += 1
                continue
            propre = nettoie_wikitext(texte)
            if len(propre) < args.min_chars:
                stats["articles_courts"] += 1
                continue
            marque = empreinte(propre)
            if marque in vus:
                stats["articles_doublons"] += 1
                continue
            vus.add(marque)
            h = int(empreinte(f"{args.graine}:{pid}", 8), 16) % 1000
            split = "val" if h < seuil_val else ("test" if h < seuil_test else "train")
            morceaux = []
            for m in troncons(f"{titre}\n{propre}", args.chunk):
                if split == "train":
                    mq = empreinte(m)
                    if mq in vus_troncons:
                        stats["troncons_doublons"] += 1
                        continue
                    vus_troncons.add(mq)
                morceaux.append(m)
            if not morceaux:
                continue
            fichiers[split].write("\n\n".join(morceaux) + "\n\n")
            stats["articles_gardes"] += 1
            stats["articles"][split] += 1
            stats["troncons"] += len(morceaux)
            stats["caracteres_gardes"] += len(propre)
            if stats["articles_lus"] % 200000 == 0:
                print(f"  [{args.langue}] {stats['articles_lus']} lus · {stats['articles_gardes']} gardés "
                      f"· {stats['caracteres_gardes'] / 1e9:.2f} G caractères", flush=True)
            if stats["articles_lus"] <= 3:
                stats["echantillon"] = (stats["echantillon"] + "\n---\n" + f"{titre}\n" + propre[:600]).strip()
    for f in fichiers.values():
        f.close()
    stats["mots_estimes"] = int(stats["caracteres_gardes"] / 6.2)
    stats["note_mots"] = "caractères / 6,2 (estimation ; le japonais et le chinois se comptent en caractères)"
    for nom in ("train", "val", "test"):
        chemin = args.sortie / f"{nom}.txt"
        stats["octets"][nom] = chemin.stat().st_size
        h = hashlib.sha256()
        with chemin.open("rb") as f:
            for bloc in iter(lambda: f.read(1 << 20), b""):
                h.update(bloc)
        stats[f"sha256_{nom}"] = h.hexdigest()
    # résidus : une mesure du débaliseur, sur un échantillon du train
    import random
    random.seed(1)
    lignes = (args.sortie / "train.txt").read_text(encoding="utf-8").splitlines()[:20000]
    stats["residus"]["modele"] = sum("{{" in l for l in lignes)
    stats["residus"]["lien"] = sum("[[" in l for l in lignes)
    stats["residus"]["balise"] = sum(("<" in l and ">" in l) for l in lignes)
    stats["residus"]["lignes_echantillon"] = len(lignes)
    args.manifeste.parent.mkdir(parents=True, exist_ok=True)
    args.manifeste.write_text(json.dumps({
        "date": "2026-11-01", "ligne": "Données", "langue": args.langue,
        "nature": f"corpus Wikipédia {args.langue} (texte intégral)",
        "source": {"dump": args.dump.as_posix(), "octets": stats["dump_octets"]},
        "methode": {"debaliseur": "regex : commentaires, refs, tableaux, modèles (30 itérations), "
                                 "fichiers/catégories, liens → libellé, titres de sections, listes",
                    "filtre": f"ns 0, sans redirection, texte >= {args.min_chars} caractères",
                    "deduplication": "articles (BLAKE2b) + tronçons (train), première occurrence gardée",
                    "split": f"hash salé (graine {args.graine}) de page_id : {args.val:.0%} val, {args.test:.0%} test"},
        **stats,
        "licence": "Wikipédia : CC-BY-SA 4.0 (et GFDL) — attribution et partage à l'identique ; corpus local",
        "limites": ["débaliseur regex : infobox/dates de modèles perdues, formules <math> retirées, "
                    "tableaux perdus", "les redirections et les espaces de noms autres que 0 sont exclus",
                    "déduplication exacte seulement (quasi-doublons non détectés)"]},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: stats[k] for k in ("articles_lus", "articles_gardes", "articles_rediriges",
                                             "caracteres_gardes", "mots_estimes", "octets", "residus")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""construire_lexique_multilingue.py — le lexique des jeux, en 53 langues.

CE QUE CE SCRIPT FAIT, ET POURQUOI IL EST SÉPARÉ. Le lexique multilingue est une
**donnée** (des libellés) et non une règle : on le construit une fois depuis
Wikidata, on le versionne, et la porte n'a plus besoin du réseau. Le script est
donc un **outil de construction**, pas un outil de mesure : il écrit
`tools/jeux/lexique_multilingue.json`, que `lexique_multilingue.py` charge.

LA SOURCE. Les libellés viennent de **Wikidata** (`wbgetentities`,
`props=labels`), donc de la licence **CC0** ; les identifiants sont ceux des
articles Wikipédia anglais, lus par `pageprops`. Les concepts sont volontairement
**peu nombreux et stables** (pièces, rangs, couleurs, enseignes, noms de jeux,
notions de maîtres) : un libellé faux serait pire qu'un libellé absent, et la
couverture est mesurée, pas supposée.

CE QUI EST MANUEL. Les verbes (« joue », « prend », « passe ») ne sont pas des
entités Wikidata : le lexique multilingue ne les invente pas. Les surfaces
multilingues sont donc des **mots-clés** (pièce + cases, rang + enseigne), et la
grammaire reste FR/EN. C'est un choix du contrat, écrit dans la fiche.

Usage :
    python3 tools/jeux/construire_lexique_multilingue.py
"""
from __future__ import annotations

import json
import pathlib
import re
import time
import unicodedata
import urllib.parse
import urllib.request

UA = "DraveGames/1.0 (https://github.com/stephanedenis/drave; recherche)"
SORTIE = pathlib.Path(__file__).resolve().parent / "lexique_multilingue.json"

LANGUES = ["ar", "bn", "ca", "cs", "da", "de", "el", "en", "eo", "es", "et", "eu",
           "fa", "fi", "fr", "gl", "he", "hi", "hr", "hu", "id", "is", "it", "ja",
           "ka", "kk", "ko", "lt", "lv", "mk", "ms", "mt", "nb", "nl", "nn", "pl",
           "pt", "ro", "ru", "sk", "sl", "sq", "sr", "sv", "sw", "ta", "th", "tr",
           "uk", "ur", "vi", "zh",
           # deuxième vague : 19 langues, pour « le plus de langues possibles »
           "af", "am", "az", "be", "bs", "cy", "ga", "hy", "km", "ky", "lo", "mn",
           "ne", "pa", "si", "so", "uz", "yo", "zu"]

# Les variantes d'écriture sont fusionnées dans la langue de base : le chinois
# simplifié, le portugais du Brésil et le serbe latin doivent être lus comme la
# même langue, pas comme trois langues de plus.
VARIANTES = {
    "zh": ["zh-hans", "zh-cn", "zh-sg", "zh-hant"],
    "pt": ["pt-br"],
    "sr": ["sr-ec", "sr-el"],
}

QIDS = {
    "jeu.morpion": "Q210339",
    "jeu.echecs": "Q718",
    "jeu.dames": "Q2180601",
    "jeu.go": "Q11413",
    "jeu.cartes": "Q47883",
    "jeu.whist": "Q767979",
    "echecs.piece.K": "Q138",
    "echecs.piece.Q": "Q139",
    "echecs.piece.R": "Q137",
    "echecs.piece.B": "Q134",
    "echecs.piece.N": "Q136",
    "echecs.piece.P": "Q135",
    "echecs.roque": "Q102877",
    "echecs.mat": "Q20819848",
    "echecs.promotion": "Q215599",
    "echecs.nulle": "Q1137224",
    "cartes.rang.14": "Q378907",
    "cartes.rang.13": "Q516114",
    "cartes.rang.12": "Q505744",
    "cartes.rang.11": "Q510474",
    "cartes.couleur.H": "Q3419242",
    "cartes.couleur.D": "Q513847",
    "cartes.couleur.C": "Q1788166",
    "cartes.couleur.S": "Q2094951",
    "cartes.atout": "Q727407",
    "cartes.pli": "Q1191150",
    "go.ko": "Q1121484",
    "go.proverbe": "Q859707",
    "maitre.colonne": "Q1320746",
    "maitre.poste": "Q3817711",
    "maitre.tempo": "Q1682303",
    "maitre.pions": "Q544685",
    "commun.blanc": "Q23444",
    "commun.noir": "Q23445",
}

# Certains concepts ont plusieurs entités : « English draughts » (Q2180601) est
# la variante, « checkers » (Q1293) le jeu générique. On fusionne les deux
# libellés pour couvrir les langues qui nomment le jeu générique.
FUSIONS = {"jeu.dames": ["Q1293"]}

# Les verbes ne sont pas des entités : on n'ajoute que les mots-clés de passe
# du go, dans les langues où le mot est court et non ambigu. La source est
# « manuel » et la fiche le dit ; les autres langues utilisent le mot GTP `pass`.
MANUEL = {
    "go.passe": {
        "fr": ["passe", "passer", "je passe"],
        "en": ["pass", "i pass"],
        "de": ["passen", "ich passe"],
        "es": ["pasar", "paso"],
        "it": ["passare", "passo"],
        "pt": ["passar", "passo"],
        "nl": ["passen", "ik pas"],
        "pl": ["pas", "pasuję"],
        "ru": ["пас", "пропуск"],
        "ar": ["تمرير", "أمر"],
        "ja": ["パス"],
        "ko": ["패스"],
        "zh": ["停一手", "虚着"],
        "tr": ["pas", "geç"],
    },
}


def _garde_marque(base: str) -> bool:
    cp = ord(base)
    # On retire les diacritiques OPTIONNELS du latin, du grec, de l'arabe et de
    # l'hébreu. On GARDE ceux du cyrillique (й, ё, ї sont des lettres), des
    # écritures indiennes et du thaï (les voyelles en sont).
    return not (0x0041 <= cp <= 0x024F or 0x0370 <= cp <= 0x03FF
                or 0x1E00 <= cp <= 0x1EFF
                or 0x0590 <= cp <= 0x05FF or 0x0600 <= cp <= 0x06FF
                or 0x0750 <= cp <= 0x077F or 0x08A0 <= cp <= 0x08FF)


def _sans_diacritiques(t: str) -> str:
    out = []
    base = None
    for c in t:
        if unicodedata.category(c).startswith("M"):
            if base is not None and not _garde_marque(base):
                continue
            out.append(c)
        else:
            out.append(c)
            base = c
    return "".join(out)


def _plie(s: str) -> str:
    t = unicodedata.normalize("NFKC", s or "").casefold()
    t = t.replace("\u0153", "oe").replace("\u0152", "OE").replace("\u00e6", "ae").replace("\u00c6", "AE")
    t = unicodedata.normalize("NFD", t)
    t = _sans_diacritiques(t)
    t = re.sub(r"\s*\([^)]*\)\s*$", "", t)
    t = t.replace("\u2019", "'").replace("`", "'")
    t = re.sub(r"\s+", " ", t).strip(" .;:!?«»\"'")
    return unicodedata.normalize("NFC", t)


def _appel(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def _libelles(ids: list[str], langues: list[str]) -> dict[str, dict]:
    """Les libellés Wikidata, par QID et par langue (fusion de plusieurs lots)."""
    out: dict[str, dict] = {q: {} for q in ids}
    for i in range(0, len(langues), 40):
        lot = langues[i:i + 40]
        url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({
            "action": "wbgetentities", "ids": "|".join(ids), "props": "labels",
            "languages": "|".join(lot), "format": "json"})
        d = _appel(url)
        for q, e in d.get("entities", {}).items():
            for langue, v in e.get("labels", {}).items():
                if langue in lot:
                    out[q][langue] = v.get("value", "")
        time.sleep(0.4)
    return out


def main() -> int:
    ids = list(QIDS.values()) + [q for qs in FUSIONS.values() for q in qs]
    toutes = LANGUES + [v for vs in VARIANTES.values() for v in vs]
    labels = _libelles(ids, toutes)
    concepts = {}
    for concept, q in QIDS.items():
        formes = {}
        for langue in LANGUES:
            variantes = [langue] + VARIANTES.get(langue, [])
            vues = []
            for v in variantes:
                valeur = labels.get(q, {}).get(v, "")
                if not valeur:
                    continue
                f = _plie(valeur)
                if f and f not in vues:
                    vues.append(f)
            if vues:
                formes[langue] = vues
        if concept in FUSIONS:
            for extra in FUSIONS[concept]:
                for langue, v in labels.get(extra, {}).items():
                    f = _plie(v)
                    if f and f not in formes.get(langue, []):
                        formes.setdefault(langue, []).append(f)
        concepts[concept] = {"qid": q, "qids": [q] + FUSIONS.get(concept, []),
                             "labels": formes}
    for concept, langues in MANUEL.items():
        concepts[concept] = {"qid": None,
                             "labels": {langue: [_plie(x) for x in formes if _plie(x)]
                                        for langue, formes in langues.items()}}
        concepts[concept]["manuel"] = True
    data = {
        "version": 1,
        "source": "Wikidata (CC0), wbgetentities props=labels ; pageprops Wikipédia pour les QID ; "
                  "libellés normalisés (NFKC, casse pliée, accents retirés, parenthèses retirées)",
        "date": "2026-10-26",
        "langues": LANGUES,
        "variantes": VARIANTES,
        "concepts": concepts,
        "manuel": list(MANUEL),
    }
    SORTIE.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    total = sum(len(c["labels"]) for c in concepts.values())
    print(f"écrit {SORTIE} : {len(concepts)} concepts, {total} couples concept-langue")
    for concept, c in sorted(concepts.items()):
        manquantes = [l for l in LANGUES if l not in c["labels"]]
        print(f"  {concept:22s} {len(c['labels']):2d}/{len(LANGUES)}  manquantes: {', '.join(manquantes[:8])}"
              + (" …" if len(manquantes) > 8 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

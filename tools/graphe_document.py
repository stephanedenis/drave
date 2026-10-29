#!/usr/bin/env python3
"""graphe_document.py — R0.1 : le document devient un graphe de régions vérifiable.

POURQUOI CE FICHIER. Le modèle ne voit qu'un flux d'octets : il ne peut pas dire « lis le
titre, saute la section 3, compare les colonnes ». Il faut une représentation du document
qui survive au rejeu et qui serve de champ de lecture au contrôleur (R0.2). Trois choses
sont donc mesurables ici, et une seule ne suffit pas :

  1. **la partition** — chaque octet du flux appartient à exactement une région. C'est
     mécanique, donc incontestable : la somme des longueurs fait le flux, les spans sont
     contigus, et le SHA-256 de chaque région se recalcule depuis le flux ;
  2. **la fidélité** — le flux n'ajoute ni ne perd de mot par rapport à une extraction
     INDÉPENDANTE (pypdf pour le PDF, pandoc pour le DOCX/EPUB, lxml pour le HTML, la
     source pour le Markdown). C'est le contrôle qui attrape l'extracteur qui invente ;
  3. **la structure** — les types de région ne sont pas triviaux : un texte plat ne doit
     pas passer la porte, sinon le graphe ne sert à rien.

Le manifeste ne porte **aucun horodatage** : deux exécutions sur le même fichier doivent
donner le même SHA-256. C'est ce qui rend le rejeu vérifiable.

Usage :
  python3 tools/graphe_document.py --json docs/theorie/vision.md
  python3 tools/graphe_document.py --verifie docs/theorie/vision.md
  python3 tools/graphe_document.py --rejeu docs/theorie/vision.md
  python3 tools/graphe_document.py --porte          # les 50 pages + les contrôles négatifs
  python3 tools/graphe_document.py --plat X.md      # contrôle négatif : un seul paragraphe
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_mod
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
from collections import Counter

VERSION = 1
RACINE = pathlib.Path(__file__).resolve().parent.parent

# Le vocabulaire est FERMÉ : un type inventé casse le contrôleur qui lira le graphe.
TYPES = {
    "titre", "section", "paragraphe", "liste", "tableau", "code", "maths",
    "figure", "legende", "note", "blanc",
}
TYPES_STRUCTURELS = TYPES - {"paragraphe", "blanc"}


def sha256(octets: bytes) -> str:
    return hashlib.sha256(octets).hexdigest()


def mots(texte: str) -> Counter:
    """Le multiensemble des mots : la seule comparaison honnête entre deux extracteurs,
    qui ne peuvent pas produire les mêmes blancs ni le même ordre."""
    return Counter(re.findall(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]+", texte.lower()))


# ------------------------------------------------------------------ le Markdown

RE_TITRE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
RE_CLOTURE = re.compile(r"^\s*(```+|~~~+)\s*([\w+-]*)")
RE_ITEM = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
RE_TABLEAU = re.compile(r"^\s*\|")
RE_SEPARATEUR = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*$")
RE_NOTE = re.compile(r"^\s*\[\^[^\]]+\]:\s*(.*)$")
RE_IMAGE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")
RE_LEGENDE = re.compile(r"^\*{0,2}(figure|table|tableau|encadr[ée]|graphique)\b", re.I)
RE_REGLE = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")


def inline(texte: str) -> str:
    """Le texte VISIBLE d'un fragment Markdown : on retire le balisage, pas les mots.
    Une cible de lien disparaît (elle n'est pas lue), le texte du lien reste.

    Le contenu d'un fragment `code` est **verbatim** : `<hôte:port>` y est du texte, pas
    une balise. On le met de côté avant de retirer le balisage, sinon il disparaît — et
    c'est exactement ce que la fidélité a attrapé sur 35 documents au premier passage."""
    texte = html_mod.unescape(texte)
    morceaux: list[str] = []

    def garde(m: re.Match) -> str:
        morceaux.append(m.group(1))
        return f"\x00{len(morceaux) - 1}\x00"

    texte = re.sub(r"`([^`]*)`", garde, texte)
    texte = re.sub(r"<(https?://[^>\s]+)>", r"\1", texte)
    texte = re.sub(r"<([^@>\s]+@[^>\s]+)>", r"\1", texte)
    texte = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", texte)
    texte = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", texte)
    texte = re.sub(r"\[([^\]]*)\]\[[^\]]*\]", r"\1", texte)
    texte = re.sub(r"\*\*([^*]+)\*\*", r"\1", texte)
    texte = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", texte)
    texte = re.sub(r"(?<![\w_])_([^_]+)_(?![\w_])", r"\1", texte)
    texte = re.sub(r"~~([^~]+)~~", r"\1", texte)
    texte = re.sub(r"<br\s*/?>", " ", texte, flags=re.I)
    # On ne retire que les balises HTML **connues**. `<ID>` (un gabarit) et
    # `< 1 et contenu >` (une inégalité dans un tableau) sont du TEXTE : les manger
    # faisait perdre des mots réels, et la fidélité l'a montré sur deux documents.
    texte = re.sub(
        r"</?(?:a|b|i|em|strong|code|span|sup|sub|u|s|del|ins|mark|small|kbd|img|p|div"
        r"|li|ul|ol|table|tr|td|th|thead|tbody|caption|figure|figcaption|blockquote"
        r"|h[1-6]|details|summary)(?:\s[^<>]*)?/?>",
        "", texte, flags=re.I)
    texte = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|>])", r"\1", texte)
    texte = re.sub(r"\x00(\d+)\x00", lambda m: morceaux[int(m.group(1))], texte)
    return re.sub(r"[ \t]+", " ", texte).strip()


def _offsets(texte: str) -> list[int]:
    """L'offset OCTET de chaque ligne. Les offsets sont en octets, jamais en caractères :
    un accent coûte deux octets, et c'est précisément l'erreur qu'un test doit attraper."""
    offsets, position = [], 0
    for ligne in texte.splitlines(keepends=True):
        offsets.append(position)
        position += len(ligne.encode("utf-8"))
    return offsets


def analyse_markdown_texte(texte: str, offsets: list[int] | None = None) -> list[dict]:
    """Les blocs d'un texte Markdown, dans l'ordre de lecture. `offsets` donne l'offset
    source de chaque ligne ; sans lui (sortie de pandoc), la provenance est un indice."""
    lignes = texte.splitlines()
    blocs: list[dict] = []

    def ajoute(type_: str, contenu: str, i: int, **prov) -> None:
        contenu = contenu.strip()
        if not contenu:
            return
        if offsets is not None and i < len(offsets):
            prov.setdefault("offset", offsets[i])
        else:
            prov.setdefault("bloc", len(blocs))
        blocs.append({"type": type_, "texte": contenu, "prov": prov})

    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        if not ligne.strip() or RE_REGLE.match(ligne):
            i += 1
            continue

        m = RE_CLOTURE.match(ligne)
        if m:
            cloture, langage = m.group(1), m.group(2)
            debut = i
            i += 1
            contenu = []
            while i < len(lignes) and not lignes[i].strip().startswith(cloture[:3]):
                contenu.append(lignes[i])
                i += 1
            i += 1
            ajoute("code", "\n".join(contenu).strip("\n"), debut,
                   **({"langage": langage} if langage else {}))
            continue

        m = RE_TITRE.match(ligne)
        if m:
            niveau = len(m.group(1))
            ajoute("titre" if niveau == 1 else "section", inline(m.group(2)), i, niveau=niveau)
            i += 1
            continue

        if RE_TABLEAU.match(ligne):
            debut = i
            lignes_tableau = []
            while i < len(lignes) and RE_TABLEAU.match(lignes[i]):
                if not RE_SEPARATEUR.match(lignes[i]):
                    lignes_tableau.append(lignes[i])
                i += 1
            rangees = []
            for brute in lignes_tableau:
                cellules = [inline(c) for c in brute.strip().strip("|").split("|")]
                rangees.append("\t".join(cellules).strip())
            ajoute("tableau", "\n".join(r for r in rangees if r), debut,
                   lignes=len(lignes_tableau))
            continue

        m = RE_NOTE.match(ligne)
        if m:
            debut = i
            contenu = [inline(m.group(1))]
            i += 1
            while i < len(lignes) and lignes[i].startswith((" ", "\t")) and lignes[i].strip():
                contenu.append(inline(lignes[i]))
                i += 1
            ajoute("note", " ".join(contenu), debut)
            continue

        m = RE_IMAGE.match(ligne)
        if m:
            ajoute("figure", inline(m.group(1)) or pathlib.Path(m.group(2)).stem, i)
            i += 1
            continue

        if RE_LEGENDE.match(inline(ligne)) and len(inline(ligne)) < 200:
            ajoute("legende", inline(ligne), i)
            i += 1
            continue

        if ligne.lstrip().startswith(">"):
            debut = i
            contenu = []
            while i < len(lignes) and lignes[i].lstrip().startswith(">"):
                contenu.append(inline(re.sub(r"^\s*>\s?", "", lignes[i])))
                i += 1
            ajoute("paragraphe", " ".join(c for c in contenu if c), debut)
            continue

        if RE_ITEM.match(ligne):
            item = RE_ITEM.match(ligne)
            debut = i
            contenu = [item.group(3)]
            i += 1
            while i < len(lignes) and lignes[i].strip() and not RE_ITEM.match(lignes[i]) \
                    and not RE_TITRE.match(lignes[i]) and not RE_CLOTURE.match(lignes[i]):
                if lignes[i].lstrip().startswith((">", "|")):
                    break
                contenu.append(lignes[i].strip())
                i += 1
            ajoute("liste", inline(" ".join(contenu)), debut, niveau=len(item.group(1)))
            continue

        debut = i
        contenu = []
        while i < len(lignes) and lignes[i].strip() and not (
            RE_TITRE.match(lignes[i]) or RE_CLOTURE.match(lignes[i])
            or RE_TABLEAU.match(lignes[i]) or RE_ITEM.match(lignes[i])
            or RE_NOTE.match(lignes[i]) or RE_IMAGE.match(lignes[i])
            or lignes[i].lstrip().startswith(">") or RE_REGLE.match(lignes[i])
        ):
            contenu.append(lignes[i].strip())
            i += 1
        if not contenu:  # ligne qui n'a matché aucun cas : on avance, jamais de boucle infinie
            contenu = [lignes[i].strip()]
            i += 1
        ajoute("paragraphe", inline(" ".join(contenu)), debut)

    return blocs


def analyse_markdown(chemin: pathlib.Path) -> list[dict]:
    texte = chemin.read_text(encoding="utf-8", errors="replace")
    return analyse_markdown_texte(texte, _offsets(texte))


# ------------------------------------------------------------ les autres formats

def _module(nom: str):
    chemin = pathlib.Path(__file__).with_name(nom + ".py")
    if not chemin.exists():
        raise SystemExit(f"parseur absent : {chemin.name}")
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def analyse_pandoc(chemin: pathlib.Path) -> list[dict]:
    """DOCX, EPUB, ODT : pandoc fait l'extraction, puis le parseur Markdown lit le résultat.
    Un seul lecteur de blocs pour trois formats, et un extracteur qu'on ne code pas."""
    sortie = subprocess.run(
        ["pandoc", "-f", chemin.suffix.lstrip("."), "-t", "gfm", "--wrap=none", str(chemin)],
        capture_output=True, text=True, check=True,
    )
    return analyse_markdown_texte(sortie.stdout)


def analyse(chemin: pathlib.Path) -> list[dict]:
    suffixe = chemin.suffix.lower()
    if suffixe in (".md", ".markdown", ".txt"):
        return analyse_markdown(chemin)
    if suffixe in (".html", ".htm"):
        return _module("graphe_document_html").analyse(chemin)
    if suffixe == ".pdf":
        return _module("graphe_document_pdf").analyse(chemin)
    if suffixe in (".docx", ".epub", ".odt"):
        return analyse_pandoc(chemin)
    raise SystemExit(f"format non pris en charge : {suffixe}")


# ------------------------------------------------------------------- le manifeste

def manifeste(chemin: pathlib.Path, langue: str = "und", plat: bool = False) -> dict:
    """Le manifeste : un flux, des régions qui le partitionnent, et de quoi tout vérifier."""
    octets_source = chemin.read_bytes()
    blocs = analyse(chemin)
    if plat:  # contrôle négatif : le même flux, mais une seule région — la structure meurt
        blocs = [{"type": "paragraphe", "texte": " ".join(b["texte"] for b in blocs),
                  "prov": {"plat": True}}]
    if not blocs:
        raise SystemExit(f"aucun bloc : {chemin}")

    regions, position, morceaux = [], 0, []
    for indice, bloc in enumerate(blocs):
        if indice:
            regions.append({
                "id": f"b{indice:05d}", "type": "blanc", "texte": "\n",
                "start": position, "end": position + 1, "sha256": sha256(b"\n"),
                "ordre": len(regions) + 1, "prov": {"separateur": True},
            })
            morceaux.append("\n")
            position += 1
        texte = bloc["texte"]
        octets = texte.encode("utf-8")
        regions.append({
            "id": f"r{indice:05d}", "type": bloc["type"], "texte": texte,
            "start": position, "end": position + len(octets), "sha256": sha256(octets),
            "ordre": len(regions) + 1, "prov": bloc.get("prov", {}),
        })
        morceaux.append(texte)
        position += len(octets)

    flux = "".join(morceaux)
    types = Counter(r["type"] for r in regions)
    return {
        "version": VERSION,
        "source": {
            "chemin": chemin.as_posix(), "sha256": sha256(octets_source),
            "octets": len(octets_source), "format": chemin.suffix.lstrip(".").lower(),
            "langue": langue,
        },
        "extraction": {"outil": "graphe_document.py", "version": VERSION,
                       "plat": bool(plat)},
        "flux": {"octets": len(flux.encode("utf-8")), "sha256": sha256(flux.encode("utf-8"))},
        "regions": regions,
        "stats": {"regions": len(regions), "types": dict(sorted(types.items()))},
    }


def verifie(m: dict, chemin: pathlib.Path | None = None) -> list[str]:
    """Les invariants du manifeste. Un manifeste qui échoue ici n'est pas un graphe."""
    erreurs: list[str] = []
    regions = m["regions"]
    if m.get("version") != VERSION:
        erreurs.append(f"version {m.get('version')} inconnue")
    if chemin is not None and sha256(chemin.read_bytes()) != m["source"]["sha256"]:
        erreurs.append("la source a changé depuis la découpe")
    concatenation = "".join(r["texte"] for r in regions).encode("utf-8")
    if sha256(concatenation) != m["flux"]["sha256"]:
        erreurs.append("le flux ne se recompose pas depuis les régions")
    if len(concatenation) != m["flux"]["octets"]:
        erreurs.append("la longueur du flux ne correspond pas")
    position = 0
    for region in regions:
        if region["start"] != position:
            erreurs.append(f"{region['id']} : trou ou chevauchement à l'offset {position}")
            break
        octets = region["texte"].encode("utf-8")
        if region["end"] - region["start"] != len(octets):
            erreurs.append(f"{region['id']} : span incohérent avec le texte")
        if concatenation[region["start"]:region["end"]] != octets:
            erreurs.append(f"{region['id']} : le span ne pointe pas le bon octet")
        if sha256(octets) != region["sha256"]:
            erreurs.append(f"{region['id']} : hash faux")
        if region["type"] not in TYPES:
            erreurs.append(f"{region['id']} : type inconnu « {region['type']} »")
        if not region["texte"] and region["type"] != "blanc":
            erreurs.append(f"{region['id']} : région vide")
        if not region["prov"]:
            erreurs.append(f"{region['id']} : provenance absente")
        position = region["end"]
    if position != len(concatenation):
        erreurs.append("la partition ne couvre pas tout le flux")
    if [r["ordre"] for r in regions] != list(range(1, len(regions) + 1)):
        erreurs.append("l'ordre de lecture n'est pas une permutation 1..N")
    return erreurs


def verifie_provenance(m: dict, chemin: pathlib.Path) -> list[str]:
    """La provenance doit pointer le BON endroit. Un offset qui désigne la ligne d'après
    n'est pas une provenance, c'est une approximation — et l'inverse d'un graphe. C'est ce
    contrôle qui a trouvé que six types de blocs pointaient la ligne suivante."""
    erreurs: list[str] = []
    contenu = [r for r in m["regions"] if r["type"] != "blanc"]
    suffixe = chemin.suffix.lower()
    if suffixe in (".md", ".markdown"):
        brut = chemin.read_bytes()
        for region in contenu:
            offset = region["prov"].get("offset")
            if not isinstance(offset, int):
                erreurs.append(f"{region['id']} : offset source absent")
                continue
            fenetre = brut[offset:offset + 400].decode("utf-8", "ignore")
            # Les trois premiers mots, dans l'ordre, à 80 caractères d'écart au plus : une
            # cible de lien peut s'intercaler entre eux dans la source, et ce n'est pas une
            # faute de provenance — c'est le balisage qui n'est pas lu.
            premiers = re.findall(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]+", region["texte"])[:3]
            if premiers:
                motif = r".{0,80}".join(re.escape(mot) for mot in premiers)
                if not re.search(motif, fenetre, re.I | re.S):
                    erreurs.append(f"{region['id']} : rien du bloc à l'offset {offset}")
    elif suffixe == ".pdf":
        page = 0
        for region in contenu:
            numero = region["prov"].get("page")
            if not isinstance(numero, int) or numero < 1:
                erreurs.append(f"{region['id']} : page absente")
                continue
            if numero < page:
                erreurs.append(f"{region['id']} : l'ordre des pages recule ({numero} après {page})")
            page = max(page, numero)
    return erreurs


def canonique(m: dict) -> str:
    return json.dumps(m, ensure_ascii=False, sort_keys=True)


def empreinte(m: dict) -> str:
    return sha256(canonique(m).encode("utf-8"))


# ---------------------------------------------------------------- la fidélité

def _fidelite_caracteres(reference: str, flux: str) -> tuple[float, list[str]]:
    """Le CONTENU, indépendamment de l'ordre et de la script : combien de caractères de la
    référence se retrouvent dans le flux, et réciproquement. Deux sens, parce qu'un
    extracteur peut perdre (`perte`) ou inventer (`invention`) — et le CJK, qui n'a pas
    d'espaces, interdit la comparaison par mots comme par bigrammes de position."""
    def propre(texte: str) -> str:
        return re.sub(r"[\W_]+", "", texte.lower())

    a, b = Counter(propre(reference)), Counter(propre(flux))
    communs = sum((a & b).values())
    perte = communs / max(sum(a.values()), 1)
    invention = communs / max(sum(b.values()), 1)
    ecarts = []
    if perte < 1.0:
        manquants = sorted((a - b).elements())[:8]
        ecarts.append("caractères absents : " + " ".join(manquants))
    if invention < 1.0:
        ajoutes = sorted((b - a).elements())[:8]
        ecarts.append("caractères ajoutés : " + " ".join(ajoutes))
    return min(perte, invention), ecarts


def fidelite(chemin: pathlib.Path, m: dict) -> tuple[float, list[str]]:
    """Le flux contre une extraction INDÉPENDANTE. Rend le ratio de mots communs et les
    écarts : c'est ici qu'on voit un extracteur qui invente ou qui perd."""
    flux = "".join(r["texte"] for r in m["regions"])
    suffixe = chemin.suffix.lower()
    if suffixe in (".md", ".markdown"):
        source = chemin.read_text(encoding="utf-8", errors="replace")
        source = re.sub(r"<!--.*?-->", "", source, flags=re.S)
        source = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", source)
        source = re.sub(r"\]\([^)]*\)", "]", source)
        # les marqueurs de liste (`1.`, `-`) ne sont pas lus : le rendu les fabrique.
        # Les compter ferait échouer le contrôle sur du texte parfaitement fidèle.
        source = re.sub(r"^(\s*)(\d+[.)]|[-*+])\s+", r"\1", source, flags=re.M)
        # le langage d'une clôture (```bash) est une métadonnée : le rendu ne le lit pas.
        source = re.sub(r"^\s*(```+|~~~+)\s*[\w+-]*\s*$", "", source, flags=re.M)
        reference = source
    elif suffixe in (".txt",):
        reference = chemin.read_text(encoding="utf-8", errors="replace")
    elif suffixe in (".html", ".htm"):
        from lxml import html as lxml_html
        racine = lxml_html.fromstring(chemin.read_bytes())

        def texte(noeud) -> str:
            # On joint les noeuds par une espace : `marque<sup>1</sup>` se lit « marque 1 »,
            # pas « marque1 ». Les éléments ignorés par le parseur (script, style, nav) le
            # sont aussi ici — sinon on comparerait le flux à du chrome de page.
            if not isinstance(noeud.tag, str) or noeud.tag in ("script", "style", "noscript", "nav"):
                return ""
            morceaux = [noeud.text or ""]
            for enfant in noeud:
                morceaux.append(texte(enfant))
                morceaux.append(enfant.tail or "")
            return " ".join(morceaux)

        reference = texte(racine)
    elif suffixe == ".pdf":
        import pypdf
        reference = "\n".join((p.extract_text() or "") for p in pypdf.PdfReader(str(chemin)).pages)
        # Le PDF se compare en bigrammes de caractères : la césure, l'ordre des colonnes et
        # les marqueurs de note sont des artefacts de mise en page, pas du contenu.
        return _fidelite_caracteres(reference, flux)
    elif suffixe in (".docx", ".epub", ".odt"):
        reference = subprocess.run(
            ["pandoc", "-f", chemin.suffix.lstrip("."), "-t", "plain", "--wrap=none", str(chemin)],
            capture_output=True, text=True, check=True).stdout
        # le texte brut rend les puces et les numéros de liste ; ils ne sont pas lus.
        reference = re.sub(r"^(\s*)(\d+[.)]|[-*+•])\s+", r"\1", reference, flags=re.M)
    else:
        return 1.0, []
    a, b = mots(reference), mots(flux)
    communs = sum((a & b).values())
    total = max(sum(a.values()), 1)
    manquants = sorted((a - b).elements())[:8]
    en_trop = sorted((b - a).elements())[:8]
    ecarts = []
    if manquants:
        ecarts.append("absents du flux : " + ", ".join(manquants))
    if en_trop:
        ecarts.append("ajoutés par le flux : " + ", ".join(en_trop))
    return communs / total, ecarts


# ------------------------------------------------------------- le corpus et la porte

# 50 pages : 16 documents ONU (37 pages réelles, 5 langues), 8 documents Markdown
# (une page = un document, tous < 8 ko), 3 pages HTML, 3 pages DOCX/EPUB fabriquées par
# pandoc. Le mélange est délibéré : le PDF donne les colonnes et les notes, le Markdown
# les tableaux et le code, les autres la conversion.
CORPUS_MD = [
    "docs/theorie/vision.md",
    "docs/pilotage/roadmap.md",
    "docs/pilotage/en-cours.md",
    "docs/theorie/lecture-rapide.md",
    "docs/methode/resultats.md",
    "docs/implantation/format-flux.md",
    "docs/theorie/glossaire/README.md",
    "docs/theorie/synthese/01-le-cerveau-drave.md",
]


def corpus() -> list[pathlib.Path]:
    """37 pages PDF + 8 documents Markdown + les fixtures HTML + 3 conversions DOCX/EPUB
    fabriquées à la volée. Le mélange est délibéré : chaque format a son extracteur et son
    contrôle, et la conversion est testée à chaque passage de la porte."""
    pdf = sorted((RACINE / "data/onu/pdf").glob("*.pdf"))[:16]
    html = sorted((RACINE / "tools/tests/documents/html").glob("*.html"))
    md = [RACINE / p for p in CORPUS_MD if (RACINE / p).exists()]
    fabrique = pathlib.Path("/tmp/r01-porte")
    fabrique.mkdir(parents=True, exist_ok=True)
    conversions = []
    for source, suffixe in (
        ("docs/theorie/vision.md", ".docx"),
        ("docs/methode/resultats.md", ".epub"),
        ("docs/implantation/format-flux.md", ".docx"),
    ):
        origine = RACINE / source
        if not origine.exists():
            continue
        cible = fabrique / (origine.stem + suffixe)
        subprocess.run(
            ["pandoc", "-f", "markdown", "-t", suffixe.lstrip("."), "-o", str(cible), str(origine)],
            check=True, capture_output=True)
        conversions.append(cible)
    return pdf + md + html + conversions


def pages(chemins: list[pathlib.Path]) -> int:
    total = 0
    for chemin in chemins:
        if chemin.suffix.lower() == ".pdf":
            try:
                sortie = subprocess.run(["pdfinfo", str(chemin)], capture_output=True, text=True).stdout
                total += int(re.search(r"Pages:\s+(\d+)", sortie).group(1))
            except Exception:
                total += 1
        else:
            total += 1
    return total


def porte(rapport: pathlib.Path | None = None) -> int:
    """La porte R0.1 : 50 pages découpées, partitions exactes, fidélité, rejeu, et trois
    contrôles négatifs qui doivent ÉCHOUER."""
    chemins = corpus()
    if not chemins:
        print("❌ corpus introuvable")
        return 1
    lignes, erreurs, types_vus, notes, details = [], [], Counter(), [], []
    for chemin in chemins:
        rel = chemin.relative_to(RACINE) if chemin.is_relative_to(RACINE) else chemin
        try:
            m = manifeste(chemin)
        except SystemExit as e:
            erreurs.append(f"{rel} : {e}")
            continue
        problemes = verifie(m, chemin) + verifie_provenance(m, chemin)
        if problemes:
            erreurs += [f"{rel} : {p}" for p in problemes]
        ratio, ecarts = fidelite(chemin, m)
        if ratio < 0.99:
            erreurs.append(f"{rel} : fidélité {ratio:.4f} < 0,99 ({ecarts})")
        m2 = manifeste(chemin)
        if empreinte(m) != empreinte(m2):
            erreurs.append(f"{rel} : le rejeu ne redonne pas le même manifeste")
        types_vus.update(m["stats"]["types"])
        notes += [(rel, m, r) for r in m["regions"] if r["type"] == "note"]
        lignes.append((str(rel), m["stats"]["regions"], m["stats"]["types"], ratio))
        details.append({"document": str(rel), "regions": m["stats"]["regions"],
                        "types": m["stats"]["types"], "fidelite": round(ratio, 4),
                        "partition": not problemes, "rejeu": empreinte(m) == empreinte(m2)})

    # 1. la couverture et la structure
    n_pages = pages(chemins)
    if n_pages < 50:
        erreurs.append(f"seulement {n_pages} pages découpées : la porte en exige 50")
    if len(types_vus) < 6:
        erreurs.append(f"{len(types_vus)} types de région seulement : la structure est trop pauvre")
    for attendu in ("tableau", "code", "note"):
        if types_vus.get(attendu, 0) < 1:
            erreurs.append(f"aucune région « {attendu} » dans tout le corpus")

    # 2. le contrôle négatif du texte plat : il DOIT échouer
    temoin = next((c for c in chemins if c.suffix in (".md", ".markdown")), None)
    echec_attendu = False
    if temoin:
        plat = manifeste(temoin, plat=True)
        echec_attendu = len(plat["stats"]["types"]) == 1
        if not echec_attendu:
            erreurs.append("le contrôle « texte plat » n'échoue pas : la porte ne voit rien")

    # 3. le contrôle négatif des deux colonnes : la gauche avant la droite, sans alternance
    deux = RACINE / "tools/tests/documents/pdf/deux-colonnes.pdf"
    colonnes = "absente"
    if deux.exists():
        mp = manifeste(deux)
        corps = [r["texte"] for r in mp["regions"] if r["type"] != "blanc"]
        gauche = [t for t in corps if "GAUCHE" in t]
        droite = [t for t in corps if "DROITE" in t]
        ordre = [("G" if "GAUCHE" in t else "D") for t in corps if "GAUCHE" in t or "DROITE" in t]
        retours = sum(1 for i in range(len(ordre) - 2) if ordre[i] == "D" and ordre[i + 1] == "G")
        colonnes = f"{len(gauche)} G puis {len(droite)} D, {retours} retour(s)"
        if not gauche or not droite:
            erreurs.append("deux-colonnes.pdf : une des deux colonnes est vide")
        elif ordre != ["G"] * len(gauche) + ["D"] * len(droite):
            erreurs.append(f"deux-colonnes.pdf : l'ordre entrelace les colonnes ({ordre})")

    # 4. la requête sans modèle : « où est le tableau X ? » — le type mène à la source
    tableaux = []
    for chemin in chemins:
        if chemin.suffix.lower() not in (".md", ".markdown"):
            continue
        m = manifeste(chemin)
        tableaux += [(chemin, r) for r in m["regions"] if r["type"] == "tableau"]
    if not tableaux:
        erreurs.append("aucun tableau trouvé : la requête par type ne peut pas être testée")
    else:
        chemin, region = tableaux[0]
        offset = region["prov"].get("offset", -1)
        ligne = chemin.read_bytes()[offset:offset + 4].decode("utf-8", "ignore")
        if not ligne.lstrip().startswith("|"):
            erreurs.append(f"{chemin.name} : le tableau {region['id']} ne pointe pas une ligne de tableau")

    # 5. les notes ne sont pas recopiées dans le corps du même document
    fuites = []
    for rel, mm, note in notes:
        # Un appel de note (« 1 », « 25-15106 ») est trop court pour être cherché : il
        # apparaîtrait dans n'importe quel paragraphe. On teste les notes qui ont un texte.
        if len(note["texte"]) < 12:
            continue
        for region in mm["regions"]:
            # L'égalité stricte, pas la contenance : en chinois, un en-tête courant est une
            # sous-chaîne banale d'une phrase (« … 世界土著妇女和女童国际日；»). Une note
            # recopiée dans le corps, elle, EST le corps.
            if region["type"] in ("note", "blanc") or region["texte"].strip() != note["texte"].strip():
                continue
            # Un en-tête courant répète un titre d'une AUTRE page : c'est le document, pas
            # une fuite. Une note recopiée dans le corps est sur la MÊME page.
            meme_page = note["prov"].get("page") == region["prov"].get("page")
            if meme_page or "page" not in note["prov"]:
                fuites.append(f"{rel}:{note['id']}")
                break
    if notes and fuites:
        erreurs.append(f"notes recopiées dans le corps : {fuites[:3]}")

    print("=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ===")
    print(f"  {len(chemins)} documents · {n_pages} pages · {sum(v for k, v in types_vus.items() if k != 'blanc')} régions")
    print(f"  types : {dict(sorted(types_vus.items()))}")
    print(f"  deux colonnes : {colonnes}")
    print(f"  contrôle texte plat : {'échoue comme attendu' if echec_attendu else 'PAS échoué'}")
    print(f"  notes hors corps : {len(notes)} région(s), {len(fuites)} fuite(s)")
    for rel, n, types, ratio in lignes[:6]:
        print(f"    {rel:52s} {n:4d} régions  fidélité {ratio:.3f}")
    if len(lignes) > 6:
        print(f"    … et {len(lignes) - 6} autres")
    if rapport is not None:
        rapport.write_text(json.dumps({
            "date": "2026-10-29", "ligne": "R0.1",
            "documents": len(chemins), "pages": n_pages,
            "regions": sum(v for k, v in types_vus.items() if k != "blanc"),
            "types": dict(sorted(types_vus.items())),
            "controles": {"texte_plat_echoue": echec_attendu, "deux_colonnes": colonnes,
                          "notes": len(notes), "fuites_de_notes": len(fuites),
                          "requete_tableau": bool(tableaux)},
            "documents_detail": details, "erreurs": erreurs,
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  rapport : {rapport}")
    for erreur in erreurs:
        print(f"  ❌ {erreur}")
    if erreurs:
        print(f"\n❌ {len(erreurs)} erreur(s) — R0.1 n'est pas mesuré.")
        return 1
    print("\n✅ les 50 pages sont découpées, les partitions exactes, le rejeu identique,")
    print("   la fidélité ≥ 0,99 et les trois contrôles négatifs se comportent comme prévu.")
    return 0


# ------------------------------------------------------------------------ CLI

def main() -> int:
    ap = argparse.ArgumentParser(description="R0.1 — le graphe de document.")
    ap.add_argument("chemin", nargs="?", type=pathlib.Path)
    ap.add_argument("--json", action="store_true", help="imprime le manifeste")
    ap.add_argument("--verifie", action="store_true", help="vérifie les invariants")
    ap.add_argument("--rejeu", action="store_true", help="deux découpes, même empreinte")
    ap.add_argument("--fidelite", action="store_true", help="compare à une extraction indépendante")
    ap.add_argument("--plat", action="store_true", help="contrôle négatif : une seule région")
    ap.add_argument("--cherche", metavar="MOTIF",
                    help="où est … ? : régions dont le type ou le texte contient le motif")
    ap.add_argument("--langue", default="und")
    ap.add_argument("--porte", action="store_true", help="la porte des 50 pages")
    ap.add_argument("--rapport", type=pathlib.Path, help="écrit le JSON de résultats")
    args = ap.parse_args()

    if args.porte:
        return porte(rapport=args.rapport)
    if not args.chemin:
        ap.error("un chemin est requis (ou --porte)")
    m = manifeste(args.chemin, langue=args.langue, plat=args.plat)
    problemes = verifie(m, args.chemin)
    if args.cherche:
        motif = args.cherche.lower()
        trouvees = [r for r in m["regions"] if r["type"] != "blanc"
                    and (motif in r["type"] or motif in r["texte"].lower())]
        print(f"{len(trouvees)} région(s) pour « {args.cherche} » :")
        for r in trouvees[:20]:
            print(f"  {r['id']} {r['type']:10s} [{r['start']:5d},{r['end']:5d}) "
                  f"{r['prov']} :: {r['texte'][:64]}")
        return 0
    if args.verifie:
        problemes += verifie_provenance(m, args.chemin)
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=1))
        return 0
    if args.rejeu:
        m2 = manifeste(args.chemin, langue=args.langue, plat=args.plat)
        meme = empreinte(m) == empreinte(m2)
        print(f"rejeu : {empreinte(m)[:16]} · {empreinte(m2)[:16]} → {'identique' if meme else 'DIFFÉRENT'}")
        return 0 if meme else 1
    if args.fidelite:
        ratio, ecarts = fidelite(args.chemin, m)
        print(f"fidélité : {ratio:.4f}")
        for ecart in ecarts:
            print(f"  {ecart}")
        return 0 if ratio >= 0.99 else 1
    if args.verifie:
        print(f"manifeste {empreinte(m)[:16]} · {m['stats']['regions']} régions · "
              f"{m['flux']['octets']} octets · {m['stats']['types']}")
        for probleme in problemes:
            print(f"❌ {probleme}")
        print("✅ partition exacte, hashes justes, ordre complet" if not problemes else "❌ faux")
        return 0 if not problemes else 1
    print(f"{m['stats']['regions']} régions · {m['stats']['types']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

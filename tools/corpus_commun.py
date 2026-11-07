#!/usr/bin/env python3
"""Corpus commun Panini/NIPADA ↔ Drave — UDHR article 1 (tâche J2.2).

Le corpus est écrit dans ``work/corpus-commun/`` (non versionné) ; la fiche
``reports/rapport-corpus-commun.md`` et le JSON ``reports/corpus-commun.json``
sont les artefacts versionnés.

Le script est **lecteur seul** côté Panini : il ouvre
``../Panini/research/data/udhr_corpus.json`` et vérifie son empreinte avant/après.
Aucune écriture n'est faite dans Panini.

Usage :
    python3 tools/corpus_commun.py --tout
    python3 tools/corpus_commun.py --construire
    python3 tools/corpus_commun.py --verifier
    python3 tools/corpus_commun.py --controle-negatif
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

RACINE = Path(__file__).resolve().parents[1]
PANINI_RESEARCH = RACINE.parent / "Panini" / "research"
PANINI_UDHR = PANINI_RESEARCH / "data" / "udhr_corpus.json"
DRAVE_UDHR = RACINE / "data" / "udhr"
DRAVE_LANGUES = DRAVE_UDHR / "langues.jsonl"
DRAVE_ARTICLES = DRAVE_UDHR / "articles_propres.jsonl"
DRAVE_GENEALOGIE = DRAVE_UDHR / "genealogie.json"
OUTIL = RACINE / "tools" / "corpus_commun.py"
SORTIE = RACINE / "work" / "corpus-commun"
RAPPORT_JSON = RACINE / "reports" / "corpus-commun.json"

DATE = "2026-11-07"
VERSION = "1.0"
GENRE = "declaration"
EPOQUE = 1948
EPOQUE_LABEL = "1948 — adoption de la DUDH"
EPOQUE_NOTE = "date de l'œuvre ; date de la traduction non documentée"

# Sélection raisonnée : 5 familles glottolog × 4 langues, puis le français
# (pivot de Drave) hors strate. Toutes les paires sont vérifiées « exactes »
# avant écriture ; aucune n'est corrigée à la main.
SELECTION: list[tuple[str, str]] = [
    # Indo-European
    ("eng", "strate"),           # latin
    ("hin", "strate"),           # devanagari
    ("bel", "strate"),           # cyrillique
    ("ell_monotonic", "strate"), # grec
    # Atlantic-Congo
    ("kin", "strate"),           # latin
    ("ewe", "strate"),           # latin
    ("ibo", "strate"),           # latin
    ("fuf_adlm", "strate"),      # adlam
    # Austronesian
    ("ind", "strate"),           # latin
    ("tgl", "strate"),           # latin
    ("mly_arab", "strate"),      # arabe (jawï)
    ("jav", "strate"),           # latin
    # Sino-Tibetan
    ("mya", "strate"),           # birman
    ("cmn_hant", "strate"),      # han traditionnel
    ("cnh", "strate"),           # latin (chin, haka)
    ("ctd", "strate"),           # latin (chin, tedim)
    # Afro-Asiatic
    ("arb", "strate"),           # arabe
    ("amh", "strate"),           # éthiopien
    ("heb", "strate"),           # hébreu
    ("hau_NE", "strate"),        # latin
    # Pivot Drave, hors strate
    ("fra", "pivot_fr"),
]

FAMILLES_ATTENDUES = {
    "Indo-European",
    "Atlantic-Congo",
    "Austronesian",
    "Sino-Tibetan",
    "Afro-Asiatic",
}

TERMINATEURS_FORTS = ".!?…।။؟۔።፧"
RE_TERMINATEUR_ESPACE = re.compile(
    r"(?<=[" + re.escape(TERMINATEURS_FORTS) + r"])\s+"
)
RE_TERMINATEUR_CJK = re.compile(r"(?<=[。！？])")
RE_ESPACES = re.compile(r"\s+")


# ---------------------------------------------------------------------------
# Petites fonctions de lecture / empreinte
# ---------------------------------------------------------------------------

def sha256_bytes(donnees: bytes) -> str:
    return hashlib.sha256(donnees).hexdigest()


def sha256_texte(texte: str) -> str:
    return sha256_bytes(texte.encode("utf-8"))


def sha256_fichier(chemin: Path) -> str:
    h = hashlib.sha256()
    with chemin.open("rb") as f:
        for bloc in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloc)
    return h.hexdigest()


def lire_jsonl(chemin: Path) -> list[dict[str, Any]]:
    lignes: list[dict[str, Any]] = []
    with chemin.open("r", encoding="utf-8") as f:
        for no, ligne in enumerate(f, 1):
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                lignes.append(json.loads(ligne))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{chemin}:{no}: JSON invalide ({exc})") from exc
    return lignes


def git_run(depot: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    """Commande git en lecture seule ; ne lève jamais."""
    try:
        return subprocess.run(
            ["git", "--no-optional-locks", "-C", str(depot), *args],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def git_info(depot: Path) -> dict[str, Any]:
    """HEAD et date, en lecture seule. Ne lève jamais."""
    head = git_run(depot, "log", "-1", "--format=%H")
    date = git_run(depot, "log", "-1", "--format=%ad", "--date=short")
    return {
        "depot": str(depot.relative_to(RACINE.parent))
        if depot.is_relative_to(RACINE.parent)
        else str(depot),
        "head": head.stdout.strip() if head and head.returncode == 0 else None,
        "date": date.stdout.strip() if date and date.returncode == 0 else None,
    }


def fichier_suivi_par_git(depot: Path, relatif: str) -> bool | None:
    """True si le fichier est suivi par git, False s'il est non suivi, None si git échoue."""
    resultat = git_run(depot, "ls-files", "--error-unmatch", "--", relatif)
    if resultat is None:
        return None
    if resultat.returncode == 0:
        return True
    if resultat.returncode == 1:
        return False
    return None


def fichier_suivi_modifie(depot: Path, relatif: str) -> bool | None:
    """True si le fichier suivi a une différence (index ou travail).

    None si git échoue ou si le fichier n'est pas suivi : dans ce cas, seule
    l'empreinte SHA-256 avant/après fait foi.
    """
    if fichier_suivi_par_git(depot, relatif) is not True:
        return None
    travail = git_run(depot, "diff", "--quiet", "--", relatif)
    index = git_run(depot, "diff", "--cached", "--quiet", "--", relatif)
    if travail is None or index is None:
        return None
    if travail.returncode not in (0, 1) or index.returncode not in (0, 1):
        return None
    return travail.returncode == 1 or index.returncode == 1


# ---------------------------------------------------------------------------
# Normalisation et segmentation
# ---------------------------------------------------------------------------

def normaliser_texte(texte: str) -> str:
    """NFC, LF, espaces collapsés, frontière éthiopienne U+1362 U+1361.

    On ne change ni la casse, ni les diacritiques, ni la ponctuation — sauf
    l'espace-mot éthiopien qui suit immédiatement le point final, ramené à une
    espace ordinaire pour que la phrase ne commence pas par un U+1361.
    """
    t = unicodedata.normalize("NFC", texte)
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    t = t.replace("\u1362\u1361", "\u1362 ")
    t = " ".join(t.split())
    return t


def decouper_phrases(texte: str) -> list[str]:
    """Segmentation par ponctuation forte, sans modèle statistique.

    Règles : après ``.!?…।။؟۔።፧`` suivi d'une espace ; après ``。！？`` même
    sans espace. Pas de gestion des abréviations : le corpus (article 1 de la
    DUDH) n'en contient pas.
    """
    t = normaliser_texte(texte)
    if not t:
        return []
    morceaux = RE_TERMINATEUR_ESPACE.split(t)
    phrases: list[str] = []
    for morceau in morceaux:
        for p in RE_TERMINATEUR_CJK.split(morceau):
            p = p.strip()
            if p:
                phrases.append(p)
    return phrases


def texte_fichier(phrases: list[str]) -> str:
    return "\n".join(phrases) + "\n"


def sans_espaces(texte: str) -> str:
    return RE_ESPACES.sub("", texte)


def valider_phrases(
    phrases: list[str],
    source_normalisee: str,
    nb_attendu: int | None = None,
) -> list[str]:
    """Contrôles d'un texte phrase par phrase. Retourne la liste des erreurs."""
    erreurs: list[str] = []
    if not phrases:
        return ["aucune phrase"]
    if nb_attendu is not None and len(phrases) != nb_attendu:
        erreurs.append(f"nb_phrases {len(phrases)} != {nb_attendu}")
    if any(not p.strip() for p in phrases):
        erreurs.append("ligne vide")
    if any("\n" in p or "\r" in p for p in phrases):
        erreurs.append("saut de ligne interne")
    if any(p != p.strip() for p in phrases):
        erreurs.append("espace de bord")
    if sans_espaces("".join(phrases)) != sans_espaces(source_normalisee):
        erreurs.append("caractères perdus ou ajoutés (hors espaces)")
    return erreurs


def egalite_normee(a: str, b: str) -> bool:
    return normaliser_texte(a) == normaliser_texte(b)


# ---------------------------------------------------------------------------
# Lecture des sources
# ---------------------------------------------------------------------------

def lire_sources() -> dict[str, Any]:
    if not PANINI_UDHR.is_file():
        raise SystemExit(f"source Panini absente : {PANINI_UDHR}")
    for chemin in (DRAVE_LANGUES, DRAVE_ARTICLES, DRAVE_GENEALOGIE):
        if not chemin.is_file():
            raise SystemExit(f"source Drave absente : {chemin}")

    panini = json.loads(PANINI_UDHR.read_text(encoding="utf-8"))
    langues = {d["fichier"]: d for d in lire_jsonl(DRAVE_LANGUES)}
    articles = [d for d in lire_jsonl(DRAVE_ARTICLES) if d.get("art") == 1]
    articles_par_fichier: dict[str, dict[str, Any]] = {}
    for d in articles:
        if d["fichier"] in articles_par_fichier:
            raise SystemExit(f"article 1 dupliqué : {d['fichier']}")
        articles_par_fichier[d["fichier"]] = d
    genealogie = json.loads(DRAVE_GENEALOGIE.read_text(encoding="utf-8"))
    return {
        "panini": panini,
        "langues": langues,
        "articles1": articles_par_fichier,
        "genealogie": genealogie,
    }


def statistiques_intersection(sources: dict[str, Any]) -> dict[str, Any]:
    panini: dict[str, Any] = sources["panini"]["languages"]
    langues: dict[str, Any] = sources["langues"]
    articles1: dict[str, Any] = sources["articles1"]
    genealogie: dict[str, Any] = sources["genealogie"]

    cles_panini = set(panini)
    fichiers_panini = {f"udhr_{k}.xml" for k in cles_panini}
    fichiers_drave = set(langues)
    intersection = fichiers_panini & fichiers_drave

    sans_fichier = sorted(fichiers_panini - fichiers_drave)
    sans_article = sorted(f for f in intersection if f not in articles1)
    appariables = sorted(f for f in intersection if f in articles1)

    exacts: list[str] = []
    ecarts: list[str] = []
    for fichier in appariables:
        cle = fichier[len("udhr_"):-len(".xml")]
        if egalite_normee(panini[cle]["text"], articles1[fichier]["texte"]):
            exacts.append(fichier)
        else:
            ecarts.append(fichier)

    hors_panini = sorted(f for f in articles1 if f not in fichiers_panini)
    familles_exactes = Counter(
        genealogie.get(f, {}).get("famille", "(inconnue)") for f in exacts
    )

    return {
        "panini_langues": len(panini),
        "drave_langues": len(langues),
        "intersection_fichiers": len(intersection),
        "article1_drave": len(articles1),
        "appariables_article1": len(appariables),
        "exacts": len(exacts),
        "ecarts_surface": len(ecarts),
        "sans_article1": len(sans_article),
        "sans_fichier_drave": len(sans_fichier),
        "drave_article1_hors_panini": len(hors_panini),
        "familles_exactes": dict(familles_exactes.most_common()),
        "listes": {
            "exacts": exacts,
            "ecarts_surface": ecarts,
            "sans_article1": sans_article,
            "sans_fichier_drave": sans_fichier,
            "drave_article1_hors_panini": hors_panini,
        },
    }


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def construire_records(sources: dict[str, Any]) -> list[dict[str, Any]]:
    panini: dict[str, Any] = sources["panini"]["languages"]
    langues: dict[str, Any] = sources["langues"]
    articles1: dict[str, Any] = sources["articles1"]
    genealogie: dict[str, Any] = sources["genealogie"]

    records: list[dict[str, Any]] = []
    ids: set[str] = set()
    for cle, role in SELECTION:
        if cle not in panini:
            raise SystemExit(f"sélection : clé Panini absente : {cle}")
        fichier = f"udhr_{cle}.xml"
        if fichier not in langues:
            raise SystemExit(f"sélection : fichier Drave absent : {fichier}")
        if fichier not in articles1:
            raise SystemExit(f"sélection : article 1 absent côté Drave : {fichier}")

        source_panini = normaliser_texte(panini[cle]["text"])
        source_drave = normaliser_texte(articles1[fichier]["texte"])
        if source_panini != source_drave:
            raise SystemExit(
                f"sélection : texte non identique pour {cle} ({fichier}) — "
                "le corpus ne corrige pas les écarts de source"
            )

        phrases = decouper_phrases(source_panini)
        erreurs = valider_phrases(phrases, source_panini)
        if erreurs:
            raise SystemExit(f"sélection : {cle} — {', '.join(erreurs)}")

        identifiant = f"udhr_{cle}"
        if identifiant in ids:
            raise SystemExit(f"identifiant dupliqué : {identifiant}")
        ids.add(identifiant)

        meta_drave = langues[fichier]
        gene = genealogie.get(fichier, {})
        if not gene:
            raise SystemExit(f"généalogie absente pour {fichier}")

        contenu_fichier = texte_fichier(phrases)
        record = {
            "id": identifiant,
            "role": role,
            "panini_cle": cle,
            "drave_fichier": fichier,
            "iso3": meta_drave["iso3"],
            "langue": panini[cle]["name"],
            "script": panini[cle]["script"],
            "sens": meta_drave.get("sens"),
            "famille": gene.get("famille"),
            "branche": gene.get("branche"),
            "branche_feuille": (gene.get("branche") or "").split("/")[-1],
            "niveau_glottolog": gene.get("niveau"),
            "famille_panini": panini[cle].get("family"),
            "branche_panini": panini[cle].get("branch"),
            "tradition_panini": panini[cle].get("tradition"),
            "genre": GENRE,
            "epoque": EPOQUE,
            "epoque_label": EPOQUE_LABEL,
            "epoque_note": EPOQUE_NOTE,
            "nb_phrases": len(phrases),
            "nb_mots_ws": sum(len(p.split()) for p in phrases),
            "nb_caracteres": len(source_panini),
            "phrases": phrases,
            "sha256_source_panini": sha256_texte(source_panini),
            "sha256_source_drave": sha256_texte(source_drave),
            "sha256_fichier": sha256_texte(contenu_fichier),
        }
        records.append(record)

    if len(records) != len(SELECTION):
        raise SystemExit("sélection incomplète")
    return records


def statistiques_echantillon(records: list[dict[str, Any]]) -> dict[str, Any]:
    familles = Counter(r["famille"] for r in records)
    scripts = Counter(r["script"] for r in records)
    par_famille: dict[str, list[str]] = defaultdict(list)
    for r in records:
        par_famille[r["famille"]].append(r["id"])
    return {
        "n_textes": len(records),
        "n_strates": sum(1 for r in records if r["role"] == "strate"),
        "n_pivots": sum(1 for r in records if r["role"] != "strate"),
        "n_familles": len(familles),
        "familles": dict(familles.most_common()),
        "n_scripts": len(scripts),
        "scripts": dict(scripts.most_common()),
        "n_phrases": sum(r["nb_phrases"] for r in records),
        "n_mots_ws": sum(r["nb_mots_ws"] for r in records),
        "n_caracteres": sum(r["nb_caracteres"] for r in records),
        "langues_par_famille": {k: sorted(v) for k, v in par_famille.items()},
    }


def construire_corpus_jsonl(records: list[dict[str, Any]], sources: dict[str, Any]) -> str:
    panini: dict[str, Any] = sources["panini"]["languages"]
    lignes: list[str] = []
    for r in records:
        phrases = decouper_phrases(panini[r["panini_cle"]]["text"])
        for i, phrase in enumerate(phrases):
            objet = {
                "id": r["id"],
                "iso3": r["iso3"],
                "langue": r["langue"],
                "script": r["script"],
                "famille": r["famille"],
                "branche_feuille": r["branche_feuille"],
                "genre": r["genre"],
                "epoque": r["epoque"],
                "role": r["role"],
                "phrase_index": i,
                "phrase": phrase,
                "sha256_phrase": sha256_texte(phrase),
            }
            lignes.append(json.dumps(objet, ensure_ascii=False, sort_keys=True))
    return "\n".join(lignes) + "\n"


def construire_metadata_tsv(records: list[dict[str, Any]]) -> str:
    colonnes = [
        "id",
        "iso3",
        "langue",
        "script",
        "famille",
        "branche_feuille",
        "genre",
        "epoque",
        "role",
        "nb_phrases",
        "nb_mots_ws",
        "nb_caracteres",
        "sha256_fichier",
    ]
    def propre(valeur: Any) -> str:
        return str(valeur).replace("\t", " ").replace("\n", " ").replace("\r", " ")

    lignes = ["\t".join(colonnes)]
    for r in records:
        lignes.append("\t".join(propre(r[c]) for c in colonnes))
    return "\n".join(lignes) + "\n"


def sources_sha256(records: list[dict[str, Any]], panini_avant: str) -> str:
    fichiers = [
        (PANINI_UDHR, "../Panini/research/data/udhr_corpus.json"),
        (DRAVE_LANGUES, "data/udhr/langues.jsonl"),
        (DRAVE_ARTICLES, "data/udhr/articles_propres.jsonl"),
        (DRAVE_GENEALOGIE, "data/udhr/genealogie.json"),
        (OUTIL, "tools/corpus_commun.py"),
    ]
    lignes = [f"{sha256_fichier(chemin)}  {relatif}" for chemin, relatif in fichiers]
    lignes.append(f"{panini_avant}  ../Panini/research/data/udhr_corpus.json#avant")
    return "\n".join(lignes) + "\n"


def controle_negatif(sources: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    panini: dict[str, Any] = sources["panini"]["languages"]
    articles1: dict[str, Any] = sources["articles1"]
    par_id = {r["id"]: r for r in records}
    r_eng = par_id["udhr_eng"]
    r_fra = par_id["udhr_fra"]

    tp_eng = normaliser_texte(panini["eng"]["text"])
    td_eng = normaliser_texte(articles1["udhr_eng.xml"]["texte"])
    tp_fra = normaliser_texte(panini["fra"]["text"])
    td_fra = normaliser_texte(articles1["udhr_fra.xml"]["texte"])
    phrases_eng = decouper_phrases(tp_eng)

    tests: list[dict[str, Any]] = []

    def ajouter(
        nom: str,
        attendu: str,
        obtenu: str,
        detail: str,
    ) -> None:
        tests.append(
            {
                "nom": nom,
                "attendu": attendu,
                "obtenu": obtenu,
                "ok": attendu == obtenu,
                "detail": detail,
            }
        )

    # Témoin : la paire correcte passe.
    ajouter(
        "temoin_paire_correcte",
        "acceptation",
        "acceptation" if egalite_normee(tp_eng, td_eng) else "rejet",
        "udhr_eng : Panini == Drave après normalisation",
    )

    # Négatif 1 : altérer un caractère côté Panini.
    tp_altere = tp_eng.replace("All", "Xll", 1)
    ajouter(
        "panini_altere",
        "rejet",
        "acceptation" if egalite_normee(tp_altere, td_eng) else "rejet",
        "un caractère changé dans le texte Panini doit casser l'égalité",
    )

    # Négatif 2 : altérer un caractère côté Drave.
    td_altere = td_eng.replace("All", "Xll", 1)
    ajouter(
        "drave_altere",
        "rejet",
        "acceptation" if egalite_normee(tp_eng, td_altere) else "rejet",
        "un caractère changé dans le texte Drave doit casser l'égalité",
    )

    # Négatif 3 : appariement croisé (anglais contre français).
    ajouter(
        "appariement_croise",
        "rejet",
        "acceptation" if egalite_normee(tp_eng, td_fra) else "rejet",
        "deux langues différentes ne doivent pas être appariables",
    )

    # Négatif 4 : supprimer une phrase.
    phrases_supprimees = phrases_eng[:-1]
    erreurs = valider_phrases(
        phrases_supprimees, tp_eng, nb_attendu=len(phrases_eng)
    )
    ajouter(
        "phrase_supprimee",
        "rejet",
        "rejet" if erreurs else "acceptation",
        "; ".join(erreurs) or "aucune erreur",
    )

    # Négatif 5 : ligne vide.
    phrases_vides = phrases_eng[:1] + [""] + phrases_eng[1:]
    erreurs = valider_phrases(phrases_vides, tp_eng, nb_attendu=len(phrases_eng))
    ajouter(
        "ligne_vide",
        "rejet",
        "rejet" if erreurs else "acceptation",
        "; ".join(erreurs) or "aucune erreur",
    )

    # Négatif 6 : empreinte de fichier fausse.
    fausse_empreinte = sha256_texte("texte qui n'est pas le corpus")
    ajouter(
        "empreinte_fausse",
        "rejet",
        "rejet" if fausse_empreinte != r_eng["sha256_fichier"] else "acceptation",
        "une empreinte différente doit être refusée",
    )

    # Négatif 7 : rôle/famille incohérent (le pivot français est bien IE).
    ajouter(
        "pivot_francais_coherent",
        "acceptation",
        "acceptation"
        if r_fra["famille"] == "Indo-European" and r_fra["role"] == "pivot_fr"
        else "rejet",
        "le pivot français doit rester Indo-European et role=pivot_fr",
    )

    return {
        "date": DATE,
        "n_tests": len(tests),
        "n_ok": sum(1 for t in tests if t["ok"]),
        "n_rejets_attendus": sum(1 for t in tests if t["attendu"] == "rejet"),
        "n_temoins_attendus": sum(1 for t in tests if t["attendu"] == "acceptation"),
        "verdict": "PASS" if all(t["ok"] for t in tests) else "FAIL",
        "tests": tests,
    }


def construire_readme(index: dict[str, Any]) -> str:
    stats = index["statistiques"]
    return f"""# Corpus commun Panini/NIPADA ↔ Drave — UDHR article 1

> **Corpus local, non versionné.** `work/` est ignoré par git. La fiche versionnée est
> `reports/rapport-corpus-commun.md` ; le JSON versionné est `reports/corpus-commun.json`.
> Date : {DATE} · outil : `tools/corpus_commun.py` · version : {VERSION}.

## Ce que c'est

L'intersection **exacte** de l'article 1 de la Déclaration universelle des droits de l'homme
(DUDH, 1948) entre :

- Panini/NIPADA : `../Panini/research/data/udhr_corpus.json` (532 langues) ;
- Drave : `data/udhr/articles_propres.jsonl` (456 langues, article 1).

{stats['n_textes']} textes ({stats['n_strates']} stratifiés + {stats['n_pivots']} pivot),
{stats['n_familles']} familles, {stats['n_scripts']} écritures, {stats['n_phrases']} phrases.

## Contenu

| fichier | contenu |
|---|---|
| `textes/<id>.txt` | le texte normalisé, **une phrase par ligne**, UTF-8, LF, sans ligne vide |
| `corpus.jsonl` | une phrase par ligne + métadonnées (id, langue, famille, époque, rôle) |
| `metadata.tsv` | une ligne par texte, colonnes fixes |
| `index.json` | manifeste complet (sources, sélection, contrôles, textes) |
| `sources.sha256` | empreintes des sources et de l'outil |
| `controle-negatif.json` | tests de contrôle (altération, phrase supprimée, ligne vide, etc.) |

## Reproduction

```bash
python3 tools/corpus_commun.py --tout
```

`--verifier` reconstruit le corpus dans un dossier temporaire et compare octet par octet ;
`--controle-negatif` rejoue les tests de contrôle. Le script ne modifie jamais Panini : il vérifie
l'empreinte de `udhr_corpus.json` avant et après.

## Limites, nommées

- **Un seul genre** (`declaration`) et **une seule époque** (1948) : ce corpus ne permet pas de
  contrôler l'époque ni le genre. Il ne suffit pas, à lui seul, au protocole atome ↔ niveau de J2.1.
- **Article 1 seulement** : Panini ne publie que l'article 1 ; les 30 articles de Drave ne sont pas
  dans l'intersection.
- **Sélection non aléatoire** : 20 langues stratifiées (5 familles × 4) + le français, choisis pour
  la diversité des écritures et parce que le texte est identique des deux côtés. Les 20 langues
  écartées pour un écart de surface (apostrophes, cédilles, ponctuation) ne sont pas représentées.
- **Comptage des mots** : `nb_mots_ws` est un comptage sur les espaces ; chaque phrase vaut 1 pour
  le chinois et l'amharique, qui ne séparent pas les mots par des espaces. Ce n'est pas une
  tokenisation.
- **Segmentation** : règles de ponctuation forte, sans modèle statistique ; pas de traitement des
  abréviations. Le tibétain a été écarté de l'échantillon pour cette raison.
"""


def fabriquer_rapport(
    index: dict[str, Any],
    records: list[dict[str, Any]],
    intersection: dict[str, Any],
    controle: dict[str, Any],
) -> dict[str, Any]:
    return {
        "fiche": "reports/rapport-corpus-commun.md",
        "version": VERSION,
        "date": DATE,
        "titre": "Corpus commun Panini/NIPADA ↔ Drave — UDHR article 1",
        "statut": "corpus_construit_verifie",
        "ligne_roadmap": "R0.7 — semaine Panini, J2.2",
        "sources": index["sources"],
        "intersection": intersection,
        "selection": index["selection"],
        "normalisation": index["normalisation"],
        "controles": index["controles"],
        "statistiques": index["statistiques"],
        "limites": index["limites"],
        "prochaine_etape": index["prochaine_etape"],
        "fichiers": {
            "corpus_local": "work/corpus-commun/",
            "index_local": "work/corpus-commun/index.json",
            "rapport_json": "reports/corpus-commun.json",
            "outil": "tools/corpus_commun.py",
            "note": "work/ n'est pas versionné ; le corpus se régénère avec tools/corpus_commun.py.",
        },
        "controle_negatif": controle,
        "textes": records,
    }


def construire(sortie: Path, ecrire_rapport: bool = True) -> dict[str, Any]:
    panini_avant = sha256_fichier(PANINI_UDHR)
    drave_hashes = {
        "langues": sha256_fichier(DRAVE_LANGUES),
        "articles1": sha256_fichier(DRAVE_ARTICLES),
        "genealogie": sha256_fichier(DRAVE_GENEALOGIE),
    }
    sources = lire_sources()
    intersection = statistiques_intersection(sources)
    records = construire_records(sources)
    stats = statistiques_echantillon(records)
    controle = controle_negatif(sources, records)

    familles_attendues = set(stats["familles"]) == FAMILLES_ATTENDUES
    if not familles_attendues:
        raise SystemExit(
            "familles inattendues : "
            + ", ".join(sorted(set(stats["familles"]) ^ FAMILLES_ATTENDUES))
        )

    index: dict[str, Any] = {
        "version": VERSION,
        "date": DATE,
        "titre": "Corpus commun Panini/NIPADA ↔ Drave — UDHR article 1",
        "sources": {
            "panini": {
                **git_info(PANINI_RESEARCH),
                "fichier": "../Panini/research/data/udhr_corpus.json",
                "sha256": panini_avant,
                "format": sources["panini"].get("format"),
                "source_declaree": sources["panini"].get("source"),
                "article": sources["panini"].get("article"),
                "total_languages": sources["panini"].get("total_languages"),
                "fichier_suivi_par_git": fichier_suivi_par_git(
                    PANINI_RESEARCH, "data/udhr_corpus.json"
                ),
                "fichier_modifie_avant": fichier_suivi_modifie(
                    PANINI_RESEARCH, "data/udhr_corpus.json"
                ),
                "lecture_seule": True,
            },
            "drave": {
                **git_info(RACINE),
                "n_langues": len(sources["langues"]),
                "n_article1": len(sources["articles1"]),
                "n_genealogie": len(sources["genealogie"]),
                "fichiers": {
                    "data/udhr/langues.jsonl": drave_hashes["langues"],
                    "data/udhr/articles_propres.jsonl": drave_hashes["articles1"],
                    "data/udhr/genealogie.json": drave_hashes["genealogie"],
                },
            },
            "commune": {
                "source": "eric-muller/udhr (Unicode UDHR XML Project)",
                "url": "https://github.com/eric-muller/udhr",
                "note": "même source XML des deux côtés ; Drave normalise les codes en iso3.",
            },
            "outil": {
                "fichier": "tools/corpus_commun.py",
                "sha256": sha256_fichier(OUTIL),
            },
        },
        "selection": {
            "principe": (
                "20 langues stratifiées (5 familles glottolog × 4) + le français, "
                "pivot de Drave ; toutes les paires sont exactes après normalisation."
            ),
            "criteres": [
                "présent des deux côtés (même fichier udhr_<clé>.xml)",
                "article 1 identique après NFC et espaces collapsés",
                "5 familles parmi les six plus représentées, choisies pour la diversité des écritures (Turkic, 17 paires, écarté : ses écritures sont déjà couvertes)",
                "4 langues par famille, écritures distinctes quand c'est possible",
                "français ajouté hors strate comme pivot de Drave",
            ],
            "familles_attendues": sorted(FAMILLES_ATTENDUES),
            "pivot": "fra",
            "n_strates": stats["n_strates"],
            "n_pivots": stats["n_pivots"],
        },
        "normalisation": {
            "encodage": "UTF-8 sans BOM",
            "unicode": "NFC",
            "fins_de_ligne": "LF",
            "espaces": "toute suite d'espaces collapsée en une espace ; lignes vides supprimées",
            "ethiopien": "U+1362 U+1361 -> U+1362 espace (frontière de phrase)",
            "segmentation": (
                "après . ! ? … । ။ ؟ ۔ ። ፧ suivis d'une espace ; "
                "après 。！？ même sans espace"
            ),
            "limite": "pas d'abréviations ; pas de modèle statistique",
        },
        "statistiques": stats,
        "textes": records,
        "controles": {
            "egalite_exacte": {
                "n": len(records),
                "attendu": len(records),
                "verdict": "PASS"
                if all(
                    r["sha256_source_panini"] == r["sha256_source_drave"]
                    for r in records
                )
                else "FAIL",
            },
            "familles": {
                "n": stats["n_familles"],
                "attendu": len(FAMILLES_ATTENDUES),
                "verdict": "PASS" if familles_attendues else "FAIL",
            },
            "controle_negatif": {
                "n": controle["n_tests"],
                "n_ok": controle["n_ok"],
                "verdict": controle["verdict"],
            },
        },
        "limites": [
            "un seul genre (declaration) et une seule époque (1948) : l'époque et le genre ne sont pas contrôlables",
            "article 1 seulement : Panini ne publie que l'article 1, les 30 articles de Drave ne sont pas dans l'intersection",
            "sélection non aléatoire : 20 langues stratifiées + le français, choisies pour l'égalité exacte et la diversité des écritures",
            "20 langues écartées pour un écart de surface (apostrophes, cédilles, ponctuation) : biais d'orthographe",
            "nb_mots_ws = comptage sur les espaces, non une tokenisation (1 pour le chinois et l'amharique)",
            "segmentation par ponctuation forte, sans modèle ; le tibétain a été écarté",
            "le corpus local n'est pas versionné (work/) ; la fiche et le JSON sont les artefacts durables",
        ],
        "prochaine_etape": (
            "J3.1 : mesure de retrieval à époque contrôlée sur ce corpus (surface : écriture, famille) "
            "et, pour l'époque, un second corpus multi-époques (§334 de Panini ou Gutenberg daté) ; "
            "J3.2 : généalogie à deux faces sur les 21 langues."
        ),
    }

    # Écriture du corpus local.
    sortie.mkdir(parents=True, exist_ok=True)
    textes_dir = sortie / "textes"
    textes_dir.mkdir(parents=True, exist_ok=True)
    ids = {r["id"] for r in records}
    for vieux in textes_dir.glob("*.txt"):
        if vieux.stem not in ids:
            vieux.unlink()

    for r in records:
        phrases = decouper_phrases(sources["panini"]["languages"][r["panini_cle"]]["text"])
        contenu = texte_fichier(phrases)
        (textes_dir / f"{r['id']}.txt").write_text(contenu, encoding="utf-8", newline="\n")

    (sortie / "corpus.jsonl").write_text(
        construire_corpus_jsonl(records, sources), encoding="utf-8", newline="\n"
    )
    (sortie / "metadata.tsv").write_text(
        construire_metadata_tsv(records), encoding="utf-8", newline="\n"
    )
    (sortie / "sources.sha256").write_text(
        sources_sha256(records, panini_avant), encoding="utf-8", newline="\n"
    )
    (sortie / "controle-negatif.json").write_text(
        json.dumps(controle, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    index["intersection"] = {
        k: v for k, v in intersection.items() if k != "listes"
    }
    index["fichiers"] = {
        "index": "work/corpus-commun/index.json",
        "corpus_jsonl": "work/corpus-commun/corpus.jsonl",
        "metadata_tsv": "work/corpus-commun/metadata.tsv",
        "textes": f"work/corpus-commun/textes/ ({len(records)} fichiers)",
        "sources_sha256": "work/corpus-commun/sources.sha256",
        "controle_negatif": "work/corpus-commun/controle-negatif.json",
    }
    (sortie / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (sortie / "README.md").write_text(
        construire_readme(index), encoding="utf-8", newline="\n"
    )

    # Contrôle de lecture seule : Panini n'a pas bougé.
    panini_apres = sha256_fichier(PANINI_UDHR)
    if panini_apres != panini_avant:
        raise SystemExit(
            "Panini a été modifié pendant la construction : "
            f"{panini_avant} -> {panini_apres}"
        )

    if ecrire_rapport:
        rapport = fabriquer_rapport(index, records, intersection, controle)
        RAPPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
        RAPPORT_JSON.write_text(
            json.dumps(rapport, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    return index


# ---------------------------------------------------------------------------
# Vérification
# ---------------------------------------------------------------------------

def comparer_arbres(a: Path, b: Path, ignores: set[str] | None = None) -> list[str]:
    ignores = ignores or set()
    erreurs: list[str] = []
    chemins_a = {
        p.relative_to(a).as_posix()
        for p in a.rglob("*")
        if p.is_file() and p.relative_to(a).as_posix() not in ignores
    }
    chemins_b = {
        p.relative_to(b).as_posix()
        for p in b.rglob("*")
        if p.is_file() and p.relative_to(b).as_posix() not in ignores
    }
    for rel in sorted(chemins_a - chemins_b):
        erreurs.append(f"fichier manquant : {rel}")
    for rel in sorted(chemins_b - chemins_a):
        erreurs.append(f"fichier en trop : {rel}")
    for rel in sorted(chemins_a & chemins_b):
        if sha256_fichier(a / rel) != sha256_fichier(b / rel):
            erreurs.append(f"contenu différent : {rel}")
    return erreurs


def sources_stables(sources: dict[str, Any]) -> dict[str, Any]:
    """Les sources sans la provenance git (HEAD, dates, statut du fichier)."""
    panini = {
        k: v
        for k, v in sources.get("panini", {}).items()
        if k not in {"head", "date", "fichier_modifie_avant", "fichier_suivi_par_git"}
    }
    drave = {
        k: v
        for k, v in sources.get("drave", {}).items()
        if k not in {"head", "date"}
    }
    return {
        "panini": panini,
        "drave": drave,
        "commune": sources.get("commune"),
        "outil": sources.get("outil"),
    }


def verifier(sortie: Path) -> list[str]:
    erreurs: list[str] = []
    index_path = sortie / "index.json"
    if not index_path.is_file():
        return [f"index absent : {index_path}"]
    index = json.loads(index_path.read_text(encoding="utf-8"))
    records = index.get("textes", [])
    if not records:
        return ["index sans textes"]

    # 1. Reconstruire dans un dossier temporaire et comparer octet par octet.
    #    `index.json` est comparé sémantiquement : le HEAD git peut avoir bougé
    #    depuis la construction (le corpus, lui, n'a pas changé).
    with tempfile.TemporaryDirectory(dir=sortie.parent, prefix=".verif-corpus-") as tmp:
        tmp_path = Path(tmp)
        tmp_index = construire(tmp_path, ecrire_rapport=False)
        erreurs.extend(comparer_arbres(sortie, tmp_path, ignores={"index.json"}))
        index_sans_sources = {k: v for k, v in index.items() if k != "sources"}
        tmp_sans_sources = {k: v for k, v in tmp_index.items() if k != "sources"}
        if index_sans_sources != tmp_sans_sources:
            erreurs.append("index.json diffère de la reconstruction (hors sources)")
        if sources_stables(index.get("sources", {})) != sources_stables(
            tmp_index.get("sources", {})
        ):
            erreurs.append("sources: empreintes ou compteurs différents de la reconstruction")

    # 2. Contrôles sémantiques sur les fichiers écrits.
    corpus_jsonl = sortie / "corpus.jsonl"
    if not corpus_jsonl.is_file():
        return erreurs + ["corpus.jsonl absent"]
    lignes = lire_jsonl(corpus_jsonl)
    par_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ligne in lignes:
        par_id[ligne["id"]].append(ligne)

    ids_attendus = {r["id"] for r in records}
    if set(par_id) != ids_attendus:
        erreurs.append(
            "corpus.jsonl: ids "
            f"{sorted(set(par_id) ^ ids_attendus)} ne correspondent pas à l'index"
        )
    for identifiant, lignes_id in par_id.items():
        indices = sorted(ligne["phrase_index"] for ligne in lignes_id)
        if indices != list(range(len(lignes_id))):
            erreurs.append(f"{identifiant}: phrase_index non contigus {indices}")
        for ligne in lignes_id:
            if ligne.get("sha256_phrase") != sha256_texte(ligne["phrase"]):
                erreurs.append(f"{identifiant}: sha256_phrase différent")

    for r in records:
        identifiant = r["id"]
        chemin = sortie / "textes" / f"{identifiant}.txt"
        if not chemin.is_file():
            erreurs.append(f"{identifiant}: fichier texte absent")
            continue
        try:
            brut = chemin.read_bytes()
            texte = brut.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            erreurs.append(f"{identifiant}: UTF-8 invalide ({exc})")
            continue
        if b"\r" in brut:
            erreurs.append(f"{identifiant}: CR présent")
        phrases = texte.splitlines()
        erreurs_texte = valider_phrases(
            phrases,
            normaliser_texte(
                " ".join(ligne["phrase"] for ligne in par_id.get(identifiant, []))
            ),
            nb_attendu=r["nb_phrases"],
        )
        # La validation ci-dessus vérifie les caractères ; on vérifie aussi la
        # concaténation exacte avec les phrases de corpus.jsonl.
        if phrases != [ligne["phrase"] for ligne in par_id.get(identifiant, [])]:
            erreurs.append(f"{identifiant}: textes/*.txt != corpus.jsonl")
        for e in erreurs_texte:
            erreurs.append(f"{identifiant}: {e}")
        if sha256_texte(texte) != r["sha256_fichier"]:
            erreurs.append(f"{identifiant}: sha256_fichier différent")
        if len(phrases) != r["nb_phrases"]:
            erreurs.append(f"{identifiant}: nb_phrases différent")

    # 3. metadata.tsv : une ligne par texte, colonnes attendues.
    tsv = sortie / "metadata.tsv"
    if not tsv.is_file():
        erreurs.append("metadata.tsv absent")
    else:
        lignes_tsv = tsv.read_text(encoding="utf-8").splitlines()
        if len(lignes_tsv) != len(records) + 1:
            erreurs.append(
                f"metadata.tsv: {len(lignes_tsv)} lignes pour {len(records)} textes"
            )
        entetes = lignes_tsv[0].split("\t") if lignes_tsv else []
        for obligatoire in ("id", "iso3", "langue", "script", "famille", "genre", "epoque"):
            if obligatoire not in entetes:
                erreurs.append(f"metadata.tsv: colonne {obligatoire} absente")
        if lignes_tsv:
            ids_tsv = {ligne.split("\t", 1)[0] for ligne in lignes_tsv[1:]}
            if ids_tsv != ids_attendus:
                erreurs.append(
                    "metadata.tsv: ids "
                    f"{sorted(ids_tsv ^ ids_attendus)} ne correspondent pas à l'index"
                )

    # 4. Empreintes des sources.
    for ligne in (sortie / "sources.sha256").read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        empreinte, _, relatif = ligne.partition("  ")
        if relatif.endswith("#avant"):
            if sha256_fichier(PANINI_UDHR) != empreinte:
                erreurs.append(
                    "sources.sha256: la source Panini a changé depuis la construction"
                )
            continue
        chemin = (RACINE / relatif).resolve()
        if not chemin.is_file():
            erreurs.append(f"sources.sha256: fichier absent {relatif}")
            continue
        if sha256_fichier(chemin) != empreinte:
            erreurs.append(f"sources.sha256: empreinte différente {relatif}")

    # 5. Contrôle négatif rejoué.
    controle_attendu = json.loads(
        (sortie / "controle-negatif.json").read_text(encoding="utf-8")
    )
    if controle_attendu.get("verdict") != "PASS":
        erreurs.append("controle-negatif.json: verdict != PASS")
    if any(not t.get("ok") for t in controle_attendu.get("tests", [])):
        erreurs.append("controle-negatif.json: un test a échoué")

    # 6. Le JSON versionné doit être à jour avec le manifeste local.
    if not RAPPORT_JSON.is_file():
        erreurs.append(f"rapport JSON absent : {RAPPORT_JSON}")
    else:
        rapport = json.loads(RAPPORT_JSON.read_text(encoding="utf-8"))
        for cle in ("sources", "textes", "controles", "statistiques"):
            if rapport.get(cle) != index.get(cle):
                erreurs.append(f"reports/corpus-commun.json: {cle} désynchronisé")

    return erreurs


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(description=__doc__)
    groupe = parseur.add_mutually_exclusive_group()
    groupe.add_argument("--tout", action="store_true", help="construire puis vérifier")
    groupe.add_argument("--construire", action="store_true", help="construire le corpus")
    groupe.add_argument("--verifier", action="store_true", help="vérifier le corpus")
    groupe.add_argument(
        "--controle-negatif", action="store_true", help="rejouer les tests de contrôle"
    )
    args = parseur.parse_args(argv)

    if args.verifier:
        erreurs = verifier(SORTIE)
        if erreurs:
            print("VERIFIER: FAIL")
            for e in erreurs:
                print(" -", e)
            return 1
        print("VERIFIER: PASS")
        return 0

    if args.controle_negatif:
        sources = lire_sources()
        records = construire_records(sources)
        controle = controle_negatif(sources, records)
        print(json.dumps(controle, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if controle["verdict"] == "PASS" else 1

    # --tout ou --construire (défaut)
    index = construire(SORTIE, ecrire_rapport=True)
    print(
        "CONSTRUIRE: "
        f"{index['statistiques']['n_textes']} textes, "
        f"{index['statistiques']['n_phrases']} phrases, "
        f"{index['statistiques']['n_familles']} familles, "
        f"{index['statistiques']['n_scripts']} écritures"
    )
    if args.tout:
        erreurs = verifier(SORTIE)
        if erreurs:
            print("VERIFIER: FAIL")
            for e in erreurs:
                print(" -", e)
            return 1
        print("VERIFIER: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

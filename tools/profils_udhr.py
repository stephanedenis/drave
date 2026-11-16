#!/usr/bin/env python3
"""profils_udhr.py — les profils de langue UDHR, chargés et exposés par le CLI.

Le bloc linguistique sait déjà détecter la langue par **recouvrement de trigrammes** sur les
profils construits depuis l'UDHR (`bloc_linguistique.charger_profils_udhr`). Ce module rend
cette détection **utilisable** : il charge l'artefact de profils (un JSON versionné, embarqué
dans la roue), expose la langue probable, le script et la confiance, et garde le seuil du
produit (`0,12`) explicite.

    python3 tools/drave.py profils --texte "Le chat dort."
    python3 tools/drave.py profils --texte "Le chat the cat dort sleeps." --json

Le profil est une **donnée**, pas un prompt : il se versionne, se rejoue et se vérifie par son
empreinte. Il est construit par `tools/construire_profils_udhr.py` à partir des articles 0–14
de `data/udhr/articles.jsonl` ; l'article 15 reste tenu à l'écart pour la mesure.

Ce que la confiance est : la marge du premier profil sur le second, mélangée au recouvrement
(`(meilleur - second) / meilleur + 0,2 × meilleur`). Ce n'est **pas** une probabilité calibrée.
Sous le seuil `0,12`, la **décision** du produit est `und` ; la langue probable reste exposée.
"""
from __future__ import annotations

import functools
import hashlib
import json
import os
import pathlib
from typing import Any

RACINE = pathlib.Path(__file__).resolve().parent.parent
PROFILS_DEFAUT = (pathlib.Path(__file__).resolve().parent
                  / "tests" / "linguistique" / "profils_udhr.json")
SCHEMA_PROFILS = "drave.profils-udhr"
VERSION_PROFILS = 1
SCHEMA_DETECTION = "drave.profils"
VERSION_DETECTION = 1
SEUIL_DEFAUT = 0.12
TOP_DEFAUT = 200
CANDIDATS_DEFAUT = 5
# En dessous de cette longueur (en caractères), les profils UDHR sont trop courts pour
# trancher : le prior des mots-outils des 7 langues du bloc prend le relais. C'est un
# arbitrage mesuré (voir `reports/rapport-profils.md`), pas une règle de langue.
LONGUEUR_PRIOR = 80
SEUIL_PRIOR = 0.25

# Les codes ISO 639-1 que le CLI accepte aujourd'hui (`--langue fr|en`) et les quelques
# voisins utiles. Les profils UDHR sont en ISO 639-3 : la table ne sert qu'à l'affichage.
ISO2_VERS_ISO3 = {
    "fr": "fra", "en": "eng", "de": "deu", "es": "spa", "it": "ita", "pt": "por",
    "nl": "nld", "ru": "rus", "uk": "ukr", "pl": "pol", "cs": "ces", "tr": "tur",
    "ar": "ara", "he": "heb", "hi": "hin", "bn": "ben", "ta": "tam", "th": "tha",
    "ja": "jpn", "zh": "cmn", "ko": "kor", "el": "ell", "sv": "swe", "fi": "fin",
    "da": "dan", "ro": "ron", "hu": "hun", "id": "ind", "vi": "vie", "sw": "swh",
}


class ProfilsAbsents(RuntimeError):
    """L'artefact de profils manque dans cette installation : la détection ne peut pas mentir.

    Le CLI sort en **4** (dépendance absente), `stdout` reste vide et le message nomme le
    fichier attendu. C'est le contrôle négatif de la roue : sans les profils, `profils` ne
    rend pas un `und` déguisé en succès.
    """


def code_iso3(code: str | None) -> str | None:
    """Le code ISO 639-3 d'un code ISO 639-1 connu ; sinon le code tel quel."""
    if not code:
        return None
    return ISO2_VERS_ISO3.get(code.lower(), code.lower())


def chemin_profils(chemin: str | pathlib.Path | None = None) -> pathlib.Path:
    """Le chemin de l'artefact : argument, `DRAVE_PROFILS`, puis l'artefact embarqué."""
    if chemin:
        return pathlib.Path(chemin).expanduser()
    variable = os.environ.get("DRAVE_PROFILS")
    if variable:
        return pathlib.Path(variable).expanduser()
    return PROFILS_DEFAUT


@functools.lru_cache(maxsize=4)
def _charger(chemin: str) -> dict[str, Any]:
    p = pathlib.Path(chemin)
    if not p.is_file():
        raise ProfilsAbsents(
            f"profils de langue absents : {p} — réinstaller la roue complète, ou lancer "
            "`python3 tools/construire_profils_udhr.py` depuis le dépôt "
            "(DRAVE_PROFILS peut pointer vers un autre artefact)."
        )
    try:
        donnees = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ProfilsAbsents(
            f"profils de langue illisibles : {p} ({type(exc).__name__}: {exc})"
        ) from exc
    langues = donnees.get("langues")
    if not isinstance(langues, dict) or not langues:
        raise ProfilsAbsents(
            f"profils de langue invalides : {p} (le champ `langues` est absent ou vide)"
        )
    if donnees.get("schema") not in (None, SCHEMA_PROFILS):
        raise ProfilsAbsents(
            f"profils de langue invalides : {p} (schéma {donnees.get('schema')!r}, "
            f"attendu {SCHEMA_PROFILS!r})"
        )
    return donnees


def charger_profils(chemin: str | pathlib.Path | None = None) -> dict[str, Any]:
    """Charge l'artefact, avec cache par chemin résolu (le JSON fait ~800 Ko)."""
    p = chemin_profils(chemin).resolve()
    return _charger(str(p))


def langues_de(profils: dict[str, Any] | None = None) -> dict[str, dict]:
    """Le dict interne `code -> profil` (accepte l'artefact complet ou le dict interne)."""
    if profils is None:
        profils = charger_profils()
    if "langues" in profils and isinstance(profils["langues"], dict):
        return profils["langues"]
    return profils


def info_profils(profils: dict[str, Any] | None = None) -> dict[str, Any]:
    """Les métadonnées utiles au CLI, sans le contenu des trigrammes."""
    if profils is None:
        profils = charger_profils()
    langues = langues_de(profils)
    return {
        "langues": len(langues),
        "schema": profils.get("schema", SCHEMA_PROFILS),
        "version": profils.get("version", VERSION_PROFILS),
        "source": profils.get("source", ""),
        "source_sha256": profils.get("source_sha256", ""),
        "train": profils.get("train", []),
        "top": profils.get("top", TOP_DEFAUT),
    }


def _candidats(scores: dict[str, float], langues: dict[str, dict],
               n: int = CANDIDATS_DEFAUT) -> list[dict[str, Any]]:
    classement = sorted(((code, score) for code, score in scores.items() if score > 0.0),
                        key=lambda kv: (-kv[1], kv[0]))
    return [{"langue": code,
             "nom": langues.get(code, {}).get("nom", ""),
             "score": round(score, 6)}
            for code, score in classement[:max(0, n)]]


def _tokens(texte: str) -> int:
    import re
    return len(re.findall(r"\w+", texte or ""))


def detecter(texte: str, profils: dict[str, Any] | None = None,
             seuil: float = SEUIL_DEFAUT,
             candidats: int = CANDIDATS_DEFAUT,
             prior_lexique: bool = True,
             longueur_prior: int = LONGUEUR_PRIOR) -> dict[str, Any]:
    """Détecte la langue probable, le script et la confiance, avec le seuil du produit.

    La **décision** (`langue`) est `und` sous le seuil ; la **langue probable**
    (`langue_probable`) reste le premier profil, avec sa confiance. Le texte vide ou sans
    lettre/chiffre est un refus (`refus = "vide"`), pas une langue inventée.

    Deux chemins, et le champ `source` dit lequel a servi :

    - `lexique` : sur un texte **court** (≤ 80 caractères), le prior des mots-outils des
      sept langues du bloc peut trancher avant les profils UDHR — c'est le cas des phrases
      d'exemple (« Le chat dort. »), où 398 profils de trigrammes se recouvrent ;
    - `profils` : au-delà, les 398 profils UDHR. Un texte de moins de cinq mots qui passe par les profils est
      **pénalisé** (confiance × mots/5) : un mot isolé n'est pas une langue.
    """
    # Import local : `drave.py` importe déjà le bloc, et le module reste utilisable seul.
    import bloc_linguistique as bl

    if profils is None:
        profils = charger_profils()
    langues = langues_de(profils)
    script = bl.detecter_script(texte)
    a_des_signes = any(ch.isalnum() for ch in texte or "")
    if not (texte or "").strip() or not a_des_signes:
        return {
            "schema": SCHEMA_DETECTION, "version": VERSION_DETECTION,
            "texte": texte, "langue": "und", "langue_probable": "und", "nom": "",
            "script": script, "confiance": 0.0, "marge": 0.0, "source": "aucune",
            "seuil": round(float(seuil), 4), "sous_seuil": True,
            "refus": "vide", "prior": None, "candidats": [],
            "profils": info_profils(profils),
        }

    # 1. Le prior des mots-outils, sur un texte court : il corrige le recouvrement des
    #    trigrammes, qui ne distingue pas « Le chat dort. » de plusieurs langues proches.
    if prior_lexique and len(texte) <= longueur_prior and _tokens(texte) >= 2:
        fb_langue, _fb_conf, fb_scores = bl.detecter_langue(texte, None)
        score_fb = float(fb_scores.get(fb_langue, 0.0)) if fb_langue else 0.0
        if fb_langue in ISO2_VERS_ISO3 and score_fb >= SEUIL_PRIOR:
            code = ISO2_VERS_ISO3[fb_langue]
            # la confiance du prior est sa part de mots-outils, sans le ×2 du repli
            sous_seuil = score_fb < float(seuil)
            scores_profils = _scores_profils(texte, langues)
            cands = _candidats(scores_profils, langues, candidats)
            return {
                "schema": SCHEMA_DETECTION, "version": VERSION_DETECTION,
                "texte": texte, "langue": "und" if sous_seuil else code,
                "langue_probable": code,
                "nom": langues.get(code, {}).get("nom", ""),
                "script": script, "confiance": round(score_fb, 4),
                "marge": round(score_fb - max((s for c, s in fb_scores.items()
                                                if c != fb_langue), default=0.0), 6),
                "source": "lexique", "seuil": round(float(seuil), 4),
                "sous_seuil": bool(sous_seuil), "refus": "",
                "prior": {"langue": code, "nom": langues.get(code, {}).get("nom", ""),
                          "score": round(score_fb, 6)},
                "candidats": cands, "profils": info_profils(profils),
            }

    # 2. Les profils UDHR ; la confiance d'un texte de moins de cinq mots est réduite.
    scores = _scores_profils(texte, langues)
    classement = sorted(((code, score) for code, score in scores.items() if score > 0.0),
                        key=lambda kv: (-kv[1], kv[0]))
    if not classement:
        return {
            "schema": SCHEMA_DETECTION, "version": VERSION_DETECTION,
            "texte": texte, "langue": "und", "langue_probable": "und", "nom": "",
            "script": script, "confiance": 0.0, "marge": 0.0, "source": "profils",
            "seuil": round(float(seuil), 4), "sous_seuil": True,
            "refus": "", "prior": None, "candidats": [],
            "profils": info_profils(profils),
        }
    langue, meilleur = classement[0]
    second = classement[1][1] if len(classement) > 1 else 0.0
    confiance = min(1.0, (meilleur - second) / meilleur + 0.2 * meilleur) if meilleur else 0.0
    n = _tokens(texte)
    # La pénalité ne vise que les textes **très courts** : un article chinois de 37
    # caractères n'a qu'un « mot » séparé par des espaces, et n'est pas un mot isolé.
    if n < 5 and len(texte) < 20:
        confiance *= n / 5.0
    sous_seuil = float(confiance) < float(seuil)
    return {
        "schema": SCHEMA_DETECTION, "version": VERSION_DETECTION,
        "texte": texte,
        "langue": "und" if sous_seuil else langue,
        "langue_probable": langue,
        "nom": langues.get(langue, {}).get("nom", ""),
        "script": script,
        "confiance": round(float(confiance), 4),
        "marge": round(float(meilleur - second), 6),
        "source": "profils",
        "seuil": round(float(seuil), 4),
        "sous_seuil": bool(sous_seuil),
        "refus": "",
        "prior": None,
        "candidats": _candidats(scores, langues, candidats),
        "profils": info_profils(profils),
    }


def _scores_profils(texte: str, langues: dict[str, dict]) -> dict[str, float]:
    """Les scores de recouvrement des trigrammes, sans le détour par `detecter_langue`."""
    import collections

    import bloc_linguistique as bl
    tri = collections.Counter(bl._trigrammes(texte))
    return {code: bl._score_profil(tri, p["trigrammes"]) for code, p in langues.items()}


def formater(detection: dict[str, Any], titre: str | None = None) -> str:
    """La sortie lisible : langue (ou und + probable), script, confiance, candidats."""
    lignes = [titre or "profils de langue (UDHR, hors ligne)"]
    if detection.get("refus"):
        lignes.append(f"langue=und script={detection['script']} confiance=0.0000 "
                      f"source={detection.get('source', 'aucune')} refus={detection['refus']}")
        lignes.append(f"refus       : {detection['refus']} "
                      "(le texte doit contenir au moins une lettre ou un chiffre)")
        lignes.append(f"script      : {detection['script']}")
        return "\n".join(lignes)
    langue = detection["langue"]
    lignes.append(f"langue={langue} script={detection['script']} "
                  f"confiance={detection['confiance']:.4f} "
                  f"source={detection.get('source', 'profils')}")
    probable = detection["langue_probable"]
    nom = detection.get("nom") or ""
    if langue == "und":
        lignes.append(f"langue      : und (sous le seuil {detection['seuil']:.2f})")
        lignes.append(f"probable    : {probable}" + (f" ({nom})" if nom else ""))
    else:
        lignes.append(f"langue      : {langue}" + (f" ({nom})" if nom else ""))
        if probable != langue:
            lignes.append(f"probable    : {probable}")
    lignes.append(f"script      : {detection['script']}")
    lignes.append(f"confiance   : {detection['confiance']:.4f} "
                  f"(marge {detection['marge']:.4f}, seuil {detection['seuil']:.2f})")
    lignes.append(f"source      : {detection.get('source', 'profils')}")
    if detection.get("prior"):
        prior = detection["prior"]
        lignes.append(f"prior       : {prior['langue']} (mots-outils {prior['score']:.4f})")
    if detection.get("candidats"):
        lignes.append("candidats   : " + " · ".join(
            f"{c['langue']} {c['score']:.4f}" for c in detection["candidats"]))
    p = detection["profils"]
    lignes.append(f"profils     : {p['langues']} langues UDHR "
                  f"(articles 0–14, top {p['top']})")
    return "\n".join(lignes)


def empreinte_fichier(chemin: str | pathlib.Path) -> str:
    return hashlib.sha256(pathlib.Path(chemin).read_bytes()).hexdigest()

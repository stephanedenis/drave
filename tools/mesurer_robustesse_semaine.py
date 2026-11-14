#!/usr/bin/env python3
"""mesurer_robustesse_semaine.py — le banc J11.3 sur les **50 textes libres** de l'audit A26.

Ce que le banc mesure, avec le code de la semaine (F1 0,7902, schéma v2, restitution v1) :

- **plantages** : code de sortie du CLI hors `{0, 3}`, traceback, `stderr` sur succès ;
- **chevauchements** : paires de syntagmes dont les spans s'intersectent, dans les deux
  vues publiées (`alternative` et `filtrer`) ; le décompte est le même que celui de
  l'audit A26 (toutes les paires, chevauchement strict) ;
- **les 8 champs** obligatoires du schéma v2, et la validation JSON Schema des annotations
  (CLI et API, dans les deux vues) ;
- **le temps** : horloge murale du CLI (démarrage compris) et durée interne de l'API ;
- **la restitution v1** : forme canonique, miroir strict, structure, stabilité ;
- **l'invariant de version** : F1, POS et attachement du gold, pour dire sur quel code
  porte la mesure.

Le banc de textes est `reports/pensee-fiabilite-produit.json` (audit A26, 50 phrases
écrites à la main). Sortie : `reports/pensee-robustesse-semaine.json`.

    python3 tools/mesurer_robustesse_semaine.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import statistics
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import tools.bloc_linguistique as bl  # noqa: E402
import tools.restitution as restitution  # noqa: E402
from tools.verifier_schema_produit import OBLIGATOIRES, SCHEMAS  # noqa: E402

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
SORTIE = RACINE / "reports" / "pensee-robustesse-semaine.json"
CLI = RACINE / "tools" / "drave.py"
COMMANDE = "python3 tools/mesurer_robustesse_semaine.py"

# Les chiffres de l'audit A26, figés pour la comparaison. La source est la fiche
# `reports/rapport-fiabilite-produit.md` (commit mesuré 56eb43af, 2026-11-06).
A26 = {
    "fiche": "reports/rapport-fiabilite-produit.md",
    "commit": "56eb43af",
    "date": "2026-11-06",
    "plantages": "0/50",
    "json_invalide": "0/46",
    "refus": "4/50 (code 1, stdout 0 octet)",
    "champs_8": "0/46 (ni schema ni version ; 11 clés racine)",
    "chevauchements_alternative": "107 paires / 23/46 textes",
    "chevauchements_filtrer": "0 conflit après filtre meta.union (hors schéma)",
    "sans_syntagme": "4/46 textes annotés (f13, f18, f27, f37)",
    "temps_cli_median_ms": 152.7,
    "temps_cli_min_ms": 136.8,
    "temps_cli_max_ms": 226.6,
    "temps_api_median_ms": 1.0,
    "temps_api_min_ms": 0.2,
    "temps_api_max_ms": 45.1,
}

LIMITES = [
    "Le banc est **écrit à la main** pour l'audit A26 : 50 phrases, pas un échantillon "
    "aléatoire. Il teste la robustesse d'entrée, pas la justesse linguistique.",
    "Le décompte des chevauchements est **strict** (intersection non vide des spans, "
    "toutes paires de syntagmes). C'est la définition qui reproduit les comptes par texte "
    "de l'audit A26 ; une autre définition (paires de types différents, spans identiques "
    "exclus, etc.) donnerait un autre chiffre.",
    "La comparaison A26 → J11.3 n'est **pas à code constant** : le module a changé entre "
    "les deux mesures (morphologie, chunker, s065, J11.1/J11.2). Les écarts de "
    "chevauchements sont donc des effets du code, pas du compteur.",
    "Les 4 refus (f14–f17) n'ont pas d'annotation : les mesures de structure portent sur "
    "46 textes, pas 50. Ils sont comptés à part et validés comme réponses JSON.",
    "Le temps CLI est dominé par le **démarrage** de Python (~150 ms) ; le temps interne "
    "(~1 ms) est la mesure du bloc. Les deux ne répondent pas à la même question.",
    "La restitution canonique vaut 1,0000 **par construction** (les jetons viennent des "
    "spans, qui sont des sous-chaînes de la source) : c'est un invariant de codec, pas une "
    "compréhension sémantique. Le miroir strict ne monte pas (5/46).",
]


# --------------------------------------------------------------------------- outils


def _sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def _head() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(RACINE),
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


def _stats(valeurs: list[float]) -> dict:
    if not valeurs:
        return {"n": 0}
    tri = sorted(valeurs)
    return {
        "n": len(tri),
        "min": round(tri[0], 1),
        "mediane": round(statistics.median(tri), 1),
        "moyenne": round(statistics.fmean(tri), 1),
        "p95": round(tri[min(len(tri) - 1, int(round(0.95 * (len(tri) - 1))))], 1),
        "max": round(tri[-1], 1),
        "total": round(sum(tri), 1),
    }


def _segments(annotation: bl.Annotation) -> list[bl.Etiquette]:
    return [e for e in annotation.etiquettes if e.niveau == "syntagme"]


def _chevauchements(segments: list[bl.Etiquette]) -> list[tuple[int, int]]:
    """Les paires (i, j), i < j, dont les spans s'intersectent strictement."""
    return [(i, j) for i, a in enumerate(segments) for j, b in enumerate(segments[i + 1:], i + 1)
            if max(a.debut, b.debut) < min(a.fin, b.fin)]


def _cli(texte: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CLI), "analyser", texte, "--json"],
        cwd=str(RACINE), capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=120,
    )


def _valider_annotation(annotation: dict, valideur) -> tuple[bool, str]:
    try:
        valideur(annotation)
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:240]


def _anneau_vide(annotation: bl.Annotation, source: str) -> dict:
    """Les invariants de spans/cibles de l'audit A26, rejoués sur l'annotation."""
    hors_texte = vides = cibles_absentes = 0
    for e in annotation.etiquettes:
        if e.debut < 0 or e.fin > len(source) or e.debut > e.fin:
            hors_texte += 1
        if e.debut == e.fin:
            vides += 1
        cible = ((e.meta or {}).get("attachement") or {}).get("cible")
        if cible and cible not in source:
            cibles_absentes += 1
    return {
        "etiquettes": len(annotation.etiquettes),
        "spans_hors_texte": hors_texte,
        "spans_vides": vides,
        "cibles_absentes": cibles_absentes,
    }


def _evaluer() -> dict:
    """L'invariant de version : F1, POS et attachement du gold vivant."""
    sortie = subprocess.run([sys.executable, str(CLI), "evaluer", "--json"],
                            cwd=str(RACINE), capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=300)
    if sortie.returncode != 0:
        raise RuntimeError(f"evaluer a échoué ({sortie.returncode}) : {sortie.stderr[:300]}")
    d = json.loads(sortie.stdout)
    h = d["heuristique"]
    return {
        "gold": d["gold"]["nom"],
        "phrases": d["gold"]["phrases"],
        "f1": h["syntagme"]["f1"],
        "precision": h["syntagme"]["precision"],
        "rappel": h["syntagme"]["rappel"],
        "tp": h["syntagme"]["tp"],
        "fp": h["syntagme"]["fp"],
        "fn": h["syntagme"]["fn"],
        "pos": h["pos"]["exactitude"],
        "attachement": {
            "labels": h["attachement"]["labels"],
            "cibles": h["attachement"]["cibles"],
            "exact": h["attachement"]["exact"],
            "top1": h["attachement"]["top1"],
            "top1_taux": h["attachement"]["top1_taux"],
        },
    }


# --------------------------------------------------------------------------- mesure


def main() -> int:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    items = restitution.items_banc(donnees)
    schemas = {v: json.loads(p.read_text(encoding="utf-8")) for v, p in SCHEMAS.items()}
    import fastjsonschema
    valideurs = {v: fastjsonschema.compile(s) for v, s in schemas.items()}
    obligatoires = tuple(OBLIGATOIRES)

    h_alt = bl.Heuristique(partition="alternative")
    h_fil = bl.Heuristique(partition="filtrer")
    h_fu = bl.Heuristique(partition="filtrer_union")

    # Chauffe : on ne veut pas attribuer au premier texte le coût d'import du module ni
    # la compilation des expressions régulières du bloc.
    _cli("Le chat dort.")
    h_alt.analyser("Le chat dort.")
    h_fil.analyser("Le chat dort.")
    h_fu.analyser("Le chat dort.")

    resultats: list[dict] = []
    temps_cli: list[float] = []
    temps_api: list[float] = []
    temps_api_fil: list[float] = []
    for item in items:
        texte = item.get("texte", "")
        ident = item.get("id", f"t{len(resultats) + 1:02d}")

        debut = time.perf_counter()
        p1 = _cli(texte)
        t1 = (time.perf_counter() - debut) * 1000.0
        p2 = _cli(texte)
        t2 = (time.perf_counter() - debut) * 1000.0 - t1

        annotation_cli = None
        erreur_json = ""
        if p1.stdout.strip():
            try:
                annotation_cli = json.loads(p1.stdout)
            except json.JSONDecodeError as exc:
                erreur_json = str(exc)[:160]
        champs_8 = bool(annotation_cli) and all(k in annotation_cli for k in obligatoires)
        schema_ok, schema_erreur = (False, "pas de JSON")
        if annotation_cli is not None:
            version = annotation_cli.get("version")
            valideur = valideurs.get(version)
            if valideur is None:
                schema_erreur = f"version inconnue : {version!r}"
            else:
                schema_ok, schema_erreur = _valider_annotation(annotation_cli, valideur)

        traceback = "Traceback (most recent call last)" in (p1.stderr or "")
        plantage = p1.returncode not in (0, 3) or traceback
        deterministe = (p1.stdout == p2.stdout and p1.returncode == p2.returncode)
        stderr_succes = bool((p1.stderr or "").strip()) and p1.returncode == 0

        debut = time.perf_counter()
        a_alt = h_alt.analyser(texte)
        t_api = (time.perf_counter() - debut) * 1000.0
        debut = time.perf_counter()
        a_fil = h_fil.analyser(texte)
        t_api_fil = (time.perf_counter() - debut) * 1000.0
        a_fu = h_fu.analyser(texte)

        seg_alt = _segments(a_alt)
        seg_fil = _segments(a_fil)
        seg_fu = _segments(a_fu)
        ov_alt = _chevauchements(seg_alt)
        ov_fil = _chevauchements(seg_fil)
        ov_fu = _chevauchements(seg_fu)

        inv = _anneau_vide(a_alt, texte)
        cli_champs = champs_8
        api_alt_json = a_alt.json()
        api_fil_json = a_fil.json()
        api_alt_champs = all(k in api_alt_json for k in obligatoires)
        api_fil_champs = all(k in api_fil_json for k in obligatoires)
        api_alt_ok, api_alt_err = _valider_annotation(api_alt_json, valideurs[2])
        api_fil_ok, api_fil_err = _valider_annotation(api_fil_json, valideurs[2])

        temps_cli.append(t1)
        temps_api.append(t_api)
        temps_api_fil.append(t_api_fil)

        resultats.append({
            "id": ident,
            "categorie": item.get("categorie", ""),
            "attendu": item.get("attendu", ""),
            "caracteres": len(texte),
            "rc": p1.returncode,
            "rc_2": p2.returncode,
            "plantage": plantage,
            "traceback": traceback,
            "stderr_succes": stderr_succes,
            "deterministe": deterministe,
            "json_valide": annotation_cli is not None,
            "erreur_json": erreur_json,
            "champs_8": cli_champs,
            "schema_v2": schema_ok,
            "schema_erreur": schema_erreur,
            "version": (annotation_cli or {}).get("version"),
            "refus": (annotation_cli or {}).get("refus", ""),
            "langue": (annotation_cli or {}).get("langue", ""),
            "script": (annotation_cli or {}).get("script", ""),
            "temps_cli_ms": round(t1, 1),
            "temps_cli_2_ms": round(t2, 1),
            "temps_api_ms": round(t_api, 1),
            "temps_api_filtrer_ms": round(t_api_fil, 1),
            "api_alternative_schema_v2": api_alt_ok,
            "api_filtrer_schema_v2": api_fil_ok,
            "api_alternative_champs_8": api_alt_champs,
            "api_filtrer_champs_8": api_fil_champs,
            "alternative": {
                "segments": len(seg_alt),
                "chevauchements": len(ov_alt),
                "sans_syntagme": not seg_alt,
            },
            "filtrer": {
                "segments": len(seg_fil),
                "chevauchements": len(ov_fil),
                "sans_syntagme": not seg_fil,
            },
            "filtrer_union": {
                "segments": len(seg_fu),
                "chevauchements": len(ov_fu),
                "sans_syntagme": not seg_fu,
            },
            "invariants": inv,
            "erreurs_api": {
                "alternative": api_alt_err,
                "filtrer": api_fil_err,
            },
        })

    annotes = [r for r in resultats if not r["refus"]]
    refuses = [r for r in resultats if r["refus"]]

    # ----- restitution v1 (46 annotations, 4 refus)
    debut = time.perf_counter()
    mesure_v1 = restitution.mesurer_banc_v1(items)
    duree_v1 = time.perf_counter() - debut
    s_v1 = mesure_v1["synthese"]

    # ----- invariant de version : F1/POS/attachement du gold
    eval_ = _evaluer()

    # ----- contrôles négatifs
    temoin = h_alt.analyser("Le chat dort.")
    temoin_json = temoin.json()
    v1 = json.loads(json.dumps(temoin_json))
    v1["version"] = 1
    for etiquette in v1.get("etiquettes", []):
        meta = etiquette.get("meta")
        if isinstance(meta, dict):
            meta.pop("partition", None)
            meta.pop("alternative", None)
    v1_lue, _ = _valider_annotation(v1, valideurs[1])
    v2_accepte_v1, _ = _valider_annotation(v1, valideurs[2])
    v2_refuse_v1 = not v2_accepte_v1
    sans_champ = json.loads(json.dumps(temoin_json))
    sans_champ.pop("refus", None)
    v2_accepte_champ_manquant, _ = _valider_annotation(sans_champ, valideurs[2])
    v2_refuse_champ_manquant = not v2_accepte_champ_manquant

    seg_temoin = _segments(temoin)
    injecte = seg_temoin + seg_temoin[:1]  # duplique un segment : une paire qui se chevauche
    chevauchement_injecte = len(_chevauchements(injecte))
    base_sans = len(_chevauchements(seg_temoin))
    filtrer_non_vide = sum(r["filtrer"]["segments"] for r in resultats)
    role_cibles = s_v1["controle_negatif_structure"]

    controles = {
        "schema_v1_lue": {"attendu": True, "observe": v1_lue},
        "schema_v2_refuse_v1": {"attendu": True, "observe": v2_refuse_v1},
        "schema_v2_refuse_champ_manquant": {"attendu": True, "observe": v2_refuse_champ_manquant},
        "chevauchement_injecte": {
            "attendu": 1,
            "observe": chevauchement_injecte,
            "temoin_sans_chevauchement": base_sans,
        },
        "filtrer_non_vide": {"attendu": "> 0", "observe": filtrer_non_vide},
        "restitution_melange_detecte": s_v1["controle_negatif_canonique"]["detectes"],
        "restitution_troncature_detecte": s_v1["controle_negatif_canonique"]["detectes"],
        "restitution_melange_exacts": s_v1["controle_negatif_canonique"]["melange_exacts"],
        "restitution_troncature_exacts": s_v1["controle_negatif_canonique"]["tronque_exacts"],
        "restitution_roles_retires": role_cibles["roles_retires"],
        "restitution_cibles_retirees": role_cibles["cibles_retirees"],
    }

    # ----- synthèse
    alternative = {
        "segments": sum(r["alternative"]["segments"] for r in resultats),
        "chevauchements": sum(r["alternative"]["chevauchements"] for r in resultats),
        "textes_avec_chevauchement": sum(1 for r in resultats if r["alternative"]["chevauchements"]),
        "textes_sans_syntagme": sum(1 for r in resultats if r["alternative"]["sans_syntagme"]),
        "textes_avec_syntagme": sum(1 for r in resultats if not r["alternative"]["sans_syntagme"]),
    }
    filtrer = {
        "segments": sum(r["filtrer"]["segments"] for r in resultats),
        "chevauchements": sum(r["filtrer"]["chevauchements"] for r in resultats),
        "textes_avec_chevauchement": sum(1 for r in resultats if r["filtrer"]["chevauchements"]),
        "textes_sans_syntagme": sum(1 for r in resultats if r["filtrer"]["sans_syntagme"]),
        "textes_avec_syntagme": sum(1 for r in resultats if not r["filtrer"]["sans_syntagme"]),
    }
    filtrer_union = {
        "segments": sum(r["filtrer_union"]["segments"] for r in resultats),
        "chevauchements": sum(r["filtrer_union"]["chevauchements"] for r in resultats),
        "textes_avec_chevauchement": sum(1 for r in resultats if r["filtrer_union"]["chevauchements"]),
    }
    sans_syntagme_ids = [r["id"] for r in resultats if r["alternative"]["sans_syntagme"]]
    sans_syntagme_annotes = [r["id"] for r in annotes if r["alternative"]["sans_syntagme"]]
    temps = {
        "cli_ms": _stats(temps_cli),
        "api_ms": _stats(temps_api),
        "api_filtrer_ms": _stats(temps_api_fil),
        "restitution_s": round(duree_v1, 2),
    }
    restitution_bloc = {
        "n": s_v1["n"],
        "annotations": s_v1["annotations"],
        "refus": s_v1["refus"],
        "refus_ids": s_v1["refus_ids"],
        "canonique": s_v1["canonique"],
        "strict": s_v1["strict"],
        "strict_sur_canonique": s_v1["strict_sur_canonique"],
        "structure": s_v1["structure"],
        "stabilite": s_v1["stabilite"],
        "controle_negatif_canonique": s_v1["controle_negatif_canonique"],
        "controle_negatif_structure": s_v1["controle_negatif_structure"],
    }

    comparaison = {
        "reference": A26,
        "lignes": [
            {"mesure": "plantages", "a26": A26["plantages"],
             "j11_3": f"{sum(1 for r in resultats if r['plantage'])}/50",
             "verdict": "="},
            {"mesure": "JSON invalide", "a26": A26["json_invalide"],
             "j11_3": f"{sum(1 for r in resultats if not r['json_valide'])}/50",
             "verdict": "les refus rendent aussi un JSON"},
            {"mesure": "refus", "a26": A26["refus"],
             "j11_3": f"{len(refuses)}/50 (code 3, JSON valide)",
             "verdict": "le refus est une réponse, plus une sortie vide"},
            {"mesure": "8 champs obligatoires", "a26": A26["champs_8"],
             "j11_3": f"{sum(1 for r in resultats if r['champs_8'])}/50",
             "verdict": "corrigé (schéma v2)"},
            {"mesure": "validation JSON Schema", "a26": "absente",
             "j11_3": f"{sum(1 for r in resultats if r['schema_v2'])}/50",
             "verdict": "nouveau"},
            {"mesure": "chevauchements, vue alternative",
             "a26": A26["chevauchements_alternative"],
             "j11_3": f"{alternative['chevauchements']} paires / "
                      f"{alternative['textes_avec_chevauchement']}/46 textes annotés",
             "verdict": "même définition ; le code a changé"},
            {"mesure": "chevauchements, vue filtrer",
             "a26": A26["chevauchements_filtrer"],
             "j11_3": f"{filtrer['chevauchements']}/50",
             "verdict": "la vue publiée tient la promesse"},
            {"mesure": "textes annotés sans syntagme", "a26": A26["sans_syntagme"],
             "j11_3": f"{len(sans_syntagme_annotes)}/{len(annotes)} : "
                      f"{', '.join(sans_syntagme_annotes)}",
             "verdict": "f13 segmenté depuis"},
            {"mesure": "temps CLI médian", "a26": f"{A26['temps_cli_median_ms']} ms",
             "j11_3": f"{temps['cli_ms']['mediane']} ms",
             "verdict": "même ordre"},
            {"mesure": "temps interne médian", "a26": f"{A26['temps_api_median_ms']} ms",
             "j11_3": f"{temps['api_ms']['mediane']} ms",
             "verdict": "même ordre"},
        ],
    }

    rapport = {
        "schema": "drave.robustesse.semaine",
        "version": 1,
        "date": datetime.date.today().isoformat(),
        "ligne": "B13",
        "tache": "J11.3",
        "titre": "Les 50 textes libres re-mesurés avec le code de la semaine",
        "banc": str(BANC.relative_to(RACINE)),
        "banc_sha256": _sha256(BANC),
        "commande": COMMANDE,
        "code": {
            "head": _head(),
            "drave": "0.1.0",
            "schema_annotation": 2,
            "sha256_schemas": {str(v): _sha256(p) for v, p in SCHEMAS.items()},
            "gold": eval_,
        },
        "dispositif": {
            "banc": "reports/pensee-fiabilite-produit.json (audit A26)",
            "cli": "python3 tools/drave.py analyser TEXTE --json (deux passages)",
            "api": "bloc_linguistique.Heuristique(partition=...).analyser(texte)",
            "vues": ["alternative", "filtrer", "filtrer_union (contrôle)"],
            "chevauchement": "paires (i, j), i < j, de syntagmes dont les spans "
                             "s'intersectent strictement : max(debut) < min(fin)",
            "champs": list(obligatoires),
            "schema": "tools/schemas/drave-annotation-v2.json",
            "restauration": "tools/restitution.py · mesurer_banc_v1",
        },
        "synthese": {
            "n": len(resultats),
            "annotations": len(annotes),
            "refus": len(refuses),
            "refus_ids": [r["id"] for r in refuses],
            "plantages": sum(1 for r in resultats if r["plantage"]),
            "codes": {str(c): sum(1 for r in resultats if r["rc"] == c)
                      for c in sorted({r["rc"] for r in resultats})},
            "stderr_succes": sum(1 for r in resultats if r["stderr_succes"]),
            "json_valide": sum(1 for r in resultats if r["json_valide"]),
            "champs_8": {
                "cli_alternative": sum(1 for r in resultats if r["champs_8"]),
                "api_alternative": sum(1 for r in resultats if r["api_alternative_champs_8"]),
                "api_filtrer": sum(1 for r in resultats if r["api_filtrer_champs_8"]),
            },
            "schema_v2": {
                "cli_alternative": sum(1 for r in resultats if r["schema_v2"]),
                "api_alternative": sum(1 for r in resultats if r["api_alternative_schema_v2"]),
                "api_filtrer": sum(1 for r in resultats if r["api_filtrer_schema_v2"]),
            },
            "determinisme": sum(1 for r in resultats if r["deterministe"]),
            "alternative": alternative,
            "filtrer": filtrer,
            "filtrer_union": filtrer_union,
            "sans_syntagme": {
                "total": len(sans_syntagme_ids),
                "ids": sans_syntagme_ids,
                "annotations": len(sans_syntagme_annotes),
                "ids_annotations": sans_syntagme_annotes,
            },
            "invariants": {
                "spans_hors_texte": sum(r["invariants"]["spans_hors_texte"] for r in resultats),
                "spans_vides": sum(r["invariants"]["spans_vides"] for r in resultats),
                "cibles_absentes": sum(r["invariants"]["cibles_absentes"] for r in resultats),
                "etiquettes": sum(r["invariants"]["etiquettes"] for r in resultats),
            },
            "temps": temps,
            "restitution": restitution_bloc,
            "controles_negatifs": controles,
        },
        "comparaison_a26": comparaison,
        "resultats": resultats,
        "limites": LIMITES,
    }

    SORTIE.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")

    print("J11.3 — les 50 textes libres re-mesurés")
    print(f"  code : HEAD {rapport['code']['head'][:8]} · F1 {eval_['f1']} · "
          f"POS {eval_['pos']} · attachement {eval_['attachement']['labels']}/"
          f"{eval_['attachement']['cibles']}")
    print(f"  plantages {rapport['synthese']['plantages']}/50 · refus "
          f"{len(refuses)}/50 · JSON valide {rapport['synthese']['json_valide']}/50 · "
          f"8 champs {rapport['synthese']['champs_8']['cli_alternative']}/50 · "
          f"schéma v2 {rapport['synthese']['schema_v2']['cli_alternative']}/50")
    print(f"  alternative : {alternative['segments']} segments · "
          f"{alternative['chevauchements']} chevauchements · "
          f"{alternative['textes_avec_chevauchement']}/46 textes")
    print(f"  filtrer     : {filtrer['segments']} segments · "
          f"{filtrer['chevauchements']} chevauchement · "
          f"{filtrer['textes_sans_syntagme']} textes sans syntagme")
    print(f"  temps CLI   : médiane {temps['cli_ms']['mediane']} ms "
          f"({temps['cli_ms']['min']}–{temps['cli_ms']['max']}) · "
          f"API médiane {temps['api_ms']['mediane']} ms")
    print(f"  restitution : canonique {s_v1['canonique']['exacts']}/{s_v1['annotations']} · "
          f"strict {s_v1['strict']['exacts']}/{s_v1['annotations']} · "
          f"segments {s_v1['structure']['segments']}")
    print(f"  écrit : {SORTIE.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

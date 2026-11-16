#!/usr/bin/env python3
"""mesurer_profils.py — la mesure de `drave profils` sur l'échantillon UDHR de 20 langues.

Le dispositif, en une commande :

  1. charge l'artefact de profils (`tools/tests/linguistique/profils_udhr.json`) ;
  2. vérifie qu'il est **identique** aux profils reconstruits depuis les articles 0–14 du
     corpus (mêmes trigrammes, même script, même empreinte de source) ;
  3. mesure la langue et le script sur les **20 langues stratifiées** de l'échantillon
     UDHR ([`rapport-corpus-commun.md`](../reports/rapport-corpus-commun.md) § 3), sur
     l'article **15** tenu à l'écart — puis sur les articles **15–30** ;
  4. mesure l'autotest complet **398 langues** (article 15, 447 textes) et le contrôle
     **profils permutés** ;
  5. joue les contrôles négatifs : texte bilingue équilibré, mot isolé, texte vide ;
  6. rejoue un cas par le **CLI** (`drave profils --json`) pour vérifier le chemin produit.

    python3 tools/mesurer_profils.py
    python3 tools/mesurer_profils.py --sortie reports/profils.json
    python3 tools/mesurer_profils.py --sans-complet   # article 15 seulement

Aucun réseau, aucune clé, aucun GPU. Le JSON produit est la mesure reproductible de
`reports/rapport-profils.md`.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(RACINE / "tools"))

import bloc_linguistique as bl  # noqa: E402
import profils_udhr as pu  # noqa: E402

UDHR = RACINE / "data/udhr/articles.jsonl"

# Les 20 langues stratifiées de `reports/rapport-corpus-commun.md` § 3 : 5 familles × 4,
# 10 écritures, article 1 identique des deux côtés. On garde le **fichier** exact, pas
# seulement l'ISO3 : `cmn_hant` et `mly_arab` ont des variantes d'écriture sous le même code.
ECHANTILLON_20 = [
    ("udhr_eng.xml", "eng", "Indo-European", "Latn"),
    ("udhr_hin.xml", "hin", "Indo-European", "Deva"),
    ("udhr_bel.xml", "bel", "Indo-European", "Cyrl"),
    ("udhr_ell_monotonic.xml", "ell", "Indo-European", "Grek"),
    ("udhr_kin.xml", "kin", "Atlantic-Congo", "Latn"),
    ("udhr_ewe.xml", "ewe", "Atlantic-Congo", "Latn"),
    ("udhr_ibo.xml", "ibo", "Atlantic-Congo", "Latn"),
    ("udhr_fuf_adlm.xml", "fuf", "Atlantic-Congo", "Adlm"),
    ("udhr_ind.xml", "ind", "Austronesian", "Latn"),
    ("udhr_tgl.xml", "tgl", "Austronesian", "Latn"),
    ("udhr_mly_arab.xml", "zlm", "Austronesian", "Arab"),
    ("udhr_jav.xml", "jav", "Austronesian", "Latn"),
    ("udhr_mya.xml", "mya", "Sino-Tibetan", "Mymr"),
    ("udhr_cmn_hant.xml", "cmn", "Sino-Tibetan", "Hant"),
    ("udhr_cnh.xml", "cnh", "Sino-Tibetan", "Latn"),
    ("udhr_ctd.xml", "ctd", "Sino-Tibetan", "Latn"),
    ("udhr_arb.xml", "arb", "Afro-Asiatic", "Arab"),
    ("udhr_amh.xml", "amh", "Afro-Asiatic", "Ethi"),
    ("udhr_heb.xml", "heb", "Afro-Asiatic", "Hebr"),
    ("udhr_hau_NE.xml", "hau", "Afro-Asiatic", "Latn"),
]

TEXTE_AMBIGU = (
    "All human beings are born free and equal in dignity and rights. "
    "Tous les êtres humains naissent libres et égaux en dignité et en droits."
)
MOT_ISOLE = "chat"


def _rows(udhr: pathlib.Path) -> dict[str, dict[int, dict]]:
    rows: dict[str, dict[int, dict]] = collections.defaultdict(dict)
    for ligne in udhr.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        d = json.loads(ligne)
        rows[d.get("fichier", "")][int(d.get("art", 0))] = d
    return rows


def _script_ok(detecte: str, attendu: str) -> bool:
    return detecte == attendu or (detecte == "Hani" and attendu in {"Hans", "Hant"})


def _mesurer(rows, profils, arts: tuple[int, ...]) -> dict:
    par_langue = []
    justes = decisions = scripts = total = 0
    confiances = []
    for fichier, iso3, famille, script in ECHANTILLON_20:
        n = k = d = s = 0
        details = []
        for art in arts:
            row = rows.get(fichier, {}).get(art)
            if not row:
                continue
            det = pu.detecter(row["texte"], profils)
            ok = det["langue_probable"] == iso3
            ok_decision = det["langue"] == iso3
            ok_script = _script_ok(det["script"], row.get("script", script))
            n += 1
            k += int(ok)
            d += int(ok_decision)
            s += int(ok_script)
            total += 1
            justes += int(ok)
            decisions += int(ok_decision)
            scripts += int(ok_script)
            confiances.append(float(det["confiance"]))
            details.append({"art": art, "langue": det["langue_probable"],
                            "decision": det["langue"], "script": det["script"],
                            "confiance": det["confiance"], "source": det["source"],
                            "ok": bool(ok), "script_ok": bool(ok_script)})
        par_langue.append({
            "fichier": fichier, "iso3": iso3, "famille": famille, "script": script,
            "tests": n, "justes": k, "decisions": d, "scripts": s,
            "confiance_min": round(min((x["confiance"] for x in details), default=0.0), 4),
            "exemple": details[0] if details else None,
        })
    return {
        "langues": len(ECHANTILLON_20),
        "tests": total,
        "langue": {"justes": justes, "total": total,
                   "taux": round(justes / max(1, total), 4)},
        "decision": {"justes": decisions, "total": total,
                     "taux": round(decisions / max(1, total), 4)},
        "script": {"justes": scripts, "total": total,
                   "taux": round(scripts / max(1, total), 4)},
        "confiance": {"moyenne": round(sum(confiances) / max(1, len(confiances)), 4),
                      "min": round(min(confiances, default=0.0), 4),
                      "max": round(max(confiances, default=0.0), 4)},
        "par_langue": par_langue,
    }


def _permutes(langues: dict[str, dict]) -> dict[str, dict]:
    noms = sorted(langues)
    return {noms[i]: langues[noms[(i + 1) % len(noms)]].copy() for i in range(len(noms))}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--udhr", default=str(UDHR))
    ap.add_argument("--profils", default=str(pu.PROFILS_DEFAUT))
    ap.add_argument("--sortie", default=str(RACINE / "reports/profils.json"))
    ap.add_argument("--sans-complet", action="store_true",
                    help="ne pas mesurer les articles 15–30 de l'échantillon")
    a = ap.parse_args()
    udhr = pathlib.Path(a.udhr)
    t0 = time.perf_counter()
    profils = pu.charger_profils(a.profils)
    duree_chargement = time.perf_counter() - t0
    langues = pu.langues_de(profils)
    rows = _rows(udhr)

    # 0. identité artefact ↔ corpus
    profils_corpus, tests = bl.charger_profils_udhr(
        udhr, train=(0, 14), test=(15, 15), min_train=5, min_test=1, top=200)
    differences = [code for code in sorted(set(profils_corpus) | set(langues))
                   if profils_corpus.get(code, {}).get("trigrammes") != langues.get(code, {}).get("trigrammes")
                   or profils_corpus.get(code, {}).get("script") != langues.get(code, {}).get("script")]
    sha_corpus = hashlib.sha256(udhr.read_bytes()).hexdigest()
    identite = {
        "langues_corpus": len(profils_corpus), "langues_artefact": len(langues),
        "differences": differences[:10], "n_differences": len(differences),
        "sha256_source_corpus": sha_corpus,
        "sha256_source_artefact": profils.get("source_sha256", ""),
        "source_identique": sha_corpus == profils.get("source_sha256", ""),
        "ok": not differences and sha_corpus == profils.get("source_sha256", ""),
    }

    # 1. l'échantillon 20, article 15
    mesure_20 = _mesurer(rows, profils, (15,))
    # 2. l'échantillon 20, articles 15–30
    mesure_20_complet = None if a.sans_complet else _mesurer(rows, profils, tuple(range(15, 31)))

    # 3. l'autotest complet 398 (article 15) — brut et chemin CLI (hybride)
    brut = hybride = script_ok = 0
    sources = collections.Counter()
    for langue, texte, script in tests:
        brut += int(bl.detecter_langue(texte, langues)[0] == langue)
        det = pu.detecter(texte, profils)
        hybride += int(det["langue_probable"] == langue)
        script_ok += int(_script_ok(det["script"], script))
        sources[det["source"]] += 1
    autotest = {
        "langues": len(profils_corpus), "tests": len(tests),
        "brut": {"justes": brut, "total": len(tests),
                 "taux": round(brut / max(1, len(tests)), 4)},
        "cli": {"justes": hybride, "total": len(tests),
                "taux": round(hybride / max(1, len(tests)), 4),
                "sources": dict(sources)},
        "script": {"justes": script_ok, "total": len(tests),
                   "taux": round(script_ok / max(1, len(tests)), 4)},
    }

    # 4. contrôle permuté (profils bruts, comme l'autotest)
    permutes = _permutes(langues)
    perm_20 = 0
    for fichier, iso3, _famille, _script in ECHANTILLON_20:
        row = rows.get(fichier, {}).get(15)
        if row:
            perm_20 += int(bl.detecter_langue(row["texte"], permutes)[0] == iso3)
    perm_full = sum(int(bl.detecter_langue(t, permutes)[0] == lg) for lg, t, _s in tests)
    controle_permute = {
        "echantillon_20": {"justes": perm_20, "total": 20,
                           "taux": round(perm_20 / 20, 4)},
        "autotest_398": {"justes": perm_full, "total": len(tests),
                         "taux": round(perm_full / max(1, len(tests)), 4)},
        "attendu": "proche du hasard",
    }

    # 5. contrôles négatifs
    ambigu = pu.detecter(TEXTE_AMBIGU, profils)
    mot = pu.detecter(MOT_ISOLE, profils)
    vide = pu.detecter("", profils)
    controle_negatif = {
        "texte_ambigu": {
            "texte": TEXTE_AMBIGU, "langue": ambigu["langue"],
            "langue_probable": ambigu["langue_probable"],
            "confiance": ambigu["confiance"], "seuil": ambigu["seuil"],
            "sous_seuil": ambigu["sous_seuil"], "source": ambigu["source"],
            "attendu": "und (sous le seuil) — deux langues mélangées à parts égales",
            "ok": ambigu["langue"] == "und" and ambigu["sous_seuil"],
        },
        "mot_isole": {
            "texte": MOT_ISOLE, "langue": mot["langue"],
            "langue_probable": mot["langue_probable"], "confiance": mot["confiance"],
            "attendu": "und — un mot ne fait pas une langue (pénalité des textes très courts)",
            "ok": mot["langue"] == "und",
        },
        "vide": {"langue": vide["langue"], "refus": vide["refus"],
                 "attendu": "und + refus=vide", "ok": vide["langue"] == "und" and vide["refus"] == "vide"},
    }

    # 6. le chemin CLI (un cas), pour prouver que le produit sert le même détecteur
    row_eng = rows.get("udhr_eng.xml", {}).get(15)
    cli = {"commande": "python3 tools/drave.py profils --texte <article 15 eng> --json",
           "code": None, "langue": "", "ok": False}
    if row_eng:
        r = subprocess.run([sys.executable, str(RACINE / "tools/drave.py"),
                            "profils", "--texte", row_eng["texte"], "--json"],
                           cwd=str(RACINE), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
        cli["code"] = r.returncode
        if r.returncode == 0:
            d = json.loads(r.stdout)
            cli["langue"] = d.get("langue_probable", "")
            cli["ok"] = d.get("langue_probable") == "eng"
        else:
            cli["erreur"] = r.stderr[:300]

    duree_totale = time.perf_counter() - t0
    rapport = {
        "schema": "drave.profils.mesure",
        "version": 1,
        "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "tache": "U3 (suite de T5)",
        "ligne_roadmap": "B13",
        "produit": "0.1.0",
        "profils": {
            "fichier": (str(pathlib.Path(a.profils).resolve().relative_to(RACINE))
                        if pathlib.Path(a.profils).resolve().is_relative_to(RACINE)
                        else str(pathlib.Path(a.profils))),
            "sha256": pu.empreinte_fichier(a.profils),
            "octets": pathlib.Path(a.profils).stat().st_size,
            "langues": len(langues), "top": profils.get("top", pu.TOP_DEFAUT),
            "train": profils.get("train", [0, 14]),
            "source": profils.get("source", ""),
            "source_sha256": profils.get("source_sha256", ""),
            "duree_chargement_s": round(duree_chargement, 3),
        },
        "echantillon_20": {
            "nom": "20 langues stratifiées UDHR (5 familles × 4, 10 écritures)",
            "source": "reports/rapport-corpus-commun.md § 3",
            "article": 15,
            **mesure_20,
        },
        "echantillon_20_complet": None if mesure_20_complet is None else {
            "articles": "15–30", **mesure_20_complet,
        },
        "autotest_398": autotest,
        "controle_permute": controle_permute,
        "controle_negatif": controle_negatif,
        "identite": identite,
        "cli": cli,
        "duree_totale_s": round(duree_totale, 3),
        "verdict": {
            "echantillon_20": mesure_20["langue"]["justes"] == 20,
            "script_20": mesure_20["script"]["justes"] == 20,
            "permute_faible": controle_permute["echantillon_20"]["taux"] <= 0.10,
            "ambigu_refuse": controle_negatif["texte_ambigu"]["ok"],
            "vide_refuse": controle_negatif["vide"]["ok"],
            "identite": identite["ok"],
            "cli": cli["ok"],
        },
        "limites": [
            "l'échantillon de 20 langues est stratifié (5 familles, 10 écritures), pas aléatoire : "
            "20/20 ne se transporte pas aux 398 ; l'autotest complet donne 433/447 brut et "
            "431/447 sur le chemin CLI (hybride court/long)",
            "l'UDHR est parallèle et propre : pas de bruit, pas de codes mêlés, pas de langues "
            "proches non séparées (le chinois mandarin et le jinyu, l'anglais et le scots)",
            "la confiance n'est pas calibrée : c'est une marge entre profils, pas une probabilité",
            "le prior des textes courts ne couvre que les sept langues à mots-outils du bloc ; "
            "hors de ces sept langues, un texte très court peut rester und",
            "les profils sont construits sur les articles 0–14 et testés sur l'article 15 : "
            "c'est un test tenu à l'écart, pas une validation croisée",
        ],
    }
    # Un résumé plat, pour un client qui ne veut pas descendre dans les sous-objets.
    rapport["resume"] = {
        "langues_profil": len(langues),
        "echantillon_langues": len(ECHANTILLON_20),
        "article": 15,
        "precision_langue_20": mesure_20["langue"]["taux"],
        "precision_script_20": mesure_20["script"]["taux"],
        "precision_langue_20_complet": (None if mesure_20_complet is None
                                         else mesure_20_complet["langue"]["taux"]),
        "precision_script_20_complet": (None if mesure_20_complet is None
                                         else mesure_20_complet["script"]["taux"]),
        "precision_398_brut": autotest["brut"]["taux"],
        "precision_398_cli": autotest["cli"]["taux"],
        "permute_20": controle_permute["echantillon_20"]["taux"],
        "ambigu_langue": ambigu["langue"],
        "ambigu_confiance": ambigu["confiance"],
        "mot_isole_langue": mot["langue"],
    }
    sortie = pathlib.Path(a.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")

    print("=== PROFILS DE LANGUE — UDHR ===")
    print(f"profils : {len(langues)} langues · {rapport['profils']['octets']} octets · "
          f"{rapport['profils']['sha256'][:16]}…")
    print(f"identité artefact ↔ corpus : {'oui' if identite['ok'] else 'NON'} "
          f"({identite['n_differences']} différence(s))")
    print(f"échantillon 20 (article 15) : langue {mesure_20['langue']['justes']}/"
          f"{mesure_20['langue']['total']} ({mesure_20['langue']['taux']:.4f}) · "
          f"script {mesure_20['script']['justes']}/{mesure_20['script']['total']}")
    if mesure_20_complet:
        m = mesure_20_complet
        print(f"échantillon 20 (articles 15–30) : langue {m['langue']['justes']}/"
              f"{m['langue']['total']} ({m['langue']['taux']:.4f}) · "
              f"script {m['script']['justes']}/{m['script']['total']}")
    print(f"autotest 398 (article 15) : brut {autotest['brut']['taux']:.4f} · "
          f"CLI {autotest['cli']['taux']:.4f} · script {autotest['script']['taux']:.4f}")
    print(f"permuté : 20 {controle_permute['echantillon_20']['taux']:.4f} · "
          f"398 {controle_permute['autotest_398']['taux']:.4f}")
    print(f"ambigu : {ambigu['langue']} ({ambigu['confiance']:.4f}) · "
          f"mot isolé : {mot['langue']} · vide : {vide['refus']}")
    print(f"verdict : {'OK' if all(rapport['verdict'].values()) else 'ÉCHEC'} "
          f"· {sortie}")
    return 0 if all(rapport["verdict"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

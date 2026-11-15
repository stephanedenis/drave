#!/usr/bin/env python3
"""panini_signatures_26.py — W4 : le signeur V14 à lancer côté Panini/NIPADA.

Ce script est **côté Panini** : il lit les sources du §334, re-extrait les 44
signatures de référence pour la calibration, puis signe les 26 textes du
manifeste W4 avec le **même** extracteur (`sign_analytic`). Il n'écrit jamais
dans l'arborescence Panini : `--sortie` doit être hors de `--panini`.

Usage (depuis un checkout de Panini, avec son venv) :
  cd /chemin/vers/Panini/research
  .venv/bin/python /chemin/vers/Qtrinet/tools/panini_signatures_26.py \
    --manifeste /chemin/vers/Qtrinet/reports/panini-manifeste.json \
    --sortie /tmp/panini-v14-26.json

Sortie : un JSON `{instrument, commit, calibration, signatures, sources}`.
Code de sortie : 0 = calibration et 26 signatures OK ; 2 = calibration
incomplète (le test ne doit pas être lancé) ; 3 = source absente ou signature
invalide. Le fichier est écrit dans tous les cas, pour que Panini voie le
diagnostic.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import math
import pathlib
import subprocess
import sys

sys.dont_write_bytecode = True

V14 = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS", "MODALITÉ",
    "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION", "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]
W = 10000
SEUIL_COS = 0.99
SEUIL_L2 = 0.01
SEUIL_MOTS = 300


def lire(chemin: pathlib.Path):
    return json.loads(chemin.read_text(encoding="utf-8"))


def sha256(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def signer_module(panini: pathlib.Path):
    src = panini / "src"
    if not (src / "nipada" / "signing" / "analytical_projection.py").exists():
        raise SystemExit(f"Panini introuvable : {src / 'nipada/signing/analytical_projection.py'}")
    sys.path.insert(0, str(src))
    try:
        from nipada.signing.analytical_projection import sign_analytic
    except Exception as e:
        raise SystemExit(
            "extracteur V14 indisponible : lancer avec le venv de Panini "
            f"(.venv/bin/python) et PYTHONPATH=src ; erreur : {e}"
        )
    return sign_analytic


def valider(sig: dict) -> tuple[bool, str]:
    if set(sig) != set(V14):
        return False, "les 14 clés V14 ne sont pas exactement celles de l'instrument"
    vals = [float(sig[a]) for a in V14]
    if any(x < -1e-9 for x in vals):
        return False, "valeur négative"
    s = sum(vals)
    if abs(s - 1.0) > 1e-6:
        return False, f"somme={s:.12f} (attendu 1 ± 1e-6)"
    return True, ""


def cos_l2(a: dict, b: dict) -> tuple[float, float]:
    va = [float(a[x]) for x in V14]
    vb = [float(b[x]) for x in V14]
    na = math.sqrt(sum(x * x for x in va))
    nb = math.sqrt(sum(x * x for x in vb))
    cos = sum(x * y for x, y in zip(va, vb)) / (na * nb) if na and nb else 0.0
    l2 = math.sqrt(sum((x - y) ** 2 for x, y in zip(va, vb)))
    return cos, l2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="W4 — signer les 26 textes V14 du manifeste Panini")
    ap.add_argument("--manifeste", required=True, help="reports/panini-manifeste.json (Drave)")
    ap.add_argument("--sortie", required=True, help="JSON de signatures à écrire (hors Panini)")
    ap.add_argument("--panini", default=".", help="racine research/ du checkout Panini")
    ap.add_argument("--force", action="store_true", help="écrase la sortie")
    args = ap.parse_args(argv)

    manifeste = lire(pathlib.Path(args.manifeste))
    panini = pathlib.Path(args.panini).resolve()
    sortie = pathlib.Path(args.sortie).resolve()
    if str(sortie).startswith(str(panini)):
        raise SystemExit("refus d'écrire dans Panini : choisir une sortie hors de l'arborescence")
    if sortie.exists() and not args.force:
        raise SystemExit(f"sortie existante : {sortie} (utiliser --force)")

    sources = panini / "nipada" / "corpus" / "_cache" / "sources"
    sign_analytic = signer_module(panini)

    def signer(ident: str) -> dict:
        p = sources / f"{ident}.txt"
        if not p.exists():
            raise FileNotFoundError(f"source absente : {p}")
        mots = p.read_text(encoding="utf-8", errors="replace").split()
        sig = sign_analytic(" ".join(mots[:W]))
        ok, msg = valider(sig)
        if not ok:
            raise ValueError(f"{ident} : {msg}")
        return {"signature": {a: float(sig[a]) for a in V14}, "mots": len(mots),
                "fichier": str(p.relative_to(panini)), "sha256": sha256(p)}

    # 1. calibration sur les 44 signatures de référence
    ref = manifeste.get("calibration", {}).get("reference", {})
    if not ref:
        raise SystemExit("le manifeste ne porte pas calibration.reference (44 signatures)")
    calibration = {"n": 0, "ok": 0, "fails": [], "seuil": {"cos": SEUIL_COS, "l2": SEUIL_L2},
                   "par_oeuvre": {}}
    for ident in sorted(ref):
        try:
            r = signer(ident)
            cos, l2 = cos_l2(ref[ident], r["signature"])
            bon = bool(cos >= SEUIL_COS or l2 <= SEUIL_L2)
            calibration["par_oeuvre"][ident] = {
                "cos": cos, "l2": l2, "mots": r["mots"], "sha256": r["sha256"], "ok": bon,
            }
            calibration["n"] += 1
            calibration["ok"] += int(bon)
            if not bon:
                calibration["fails"].append(ident)
        except Exception as e:
            calibration["fails"].append(ident)
            calibration["par_oeuvre"][ident] = {"erreur": str(e), "ok": False}
    calibration["ok"] = sum(1 for v in calibration["par_oeuvre"].values() if v.get("ok"))
    calibration["n"] = len(calibration["par_oeuvre"])

    # 2. les 26 signatures demandées
    a_signer = manifeste.get("a_signer") or manifeste.get("manifeste", {}).get("a_signer")
    if not a_signer:
        raise SystemExit("le manifeste ne porte pas a_signer (26 textes)")
    signatures, sources_out, erreurs = {}, {}, []
    for t in a_signer:
        ident = t["id"]
        try:
            r = signer(ident)
            signatures[ident] = r["signature"]
            sources_out[ident] = {"fichier": r["fichier"], "sha256": r["sha256"],
                                  "mots": r["mots"], "seuil_300": r["mots"] >= SEUIL_MOTS}
            if r["mots"] < SEUIL_MOTS:
                erreurs.append(f"{ident} : {r['mots']} mots < {SEUIL_MOTS} (hors support de calibration)")
        except Exception as e:
            erreurs.append(f"{ident} : {e}")

    try:
        commit = subprocess.check_output(["git", "-C", str(panini), "rev-parse", "HEAD"],
                                         stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        commit = None

    # Le rejeu de `protocole_date.py` lit UN seul fichier. On y met les 59
    # signatures (44 de référence + 26 nouvelles) **seulement si la calibration
    # est 44/44**. Sinon `signatures` reste à 44 : le rejeu voit 27/60 paires et
    # s'arrête en `incomplet`, au lieu de tester sur un instrument non calibré.
    calibration_ok = calibration["n"] > 0 and calibration["ok"] == calibration["n"]
    reference = {k: {a: float(v[a]) for a in V14} for k, v in ref.items()}
    signatures_completes = dict(reference)
    signatures_completes.update(signatures)

    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps({
        "instrument": "V14 — sign_analytic (nipada.signing.analytical_projection), 10 000 premiers mots",
        "commit": commit,
        "date": _dt.datetime.now().isoformat(timespec="seconds"),
        "manifeste": str(pathlib.Path(args.manifeste).resolve()),
        "calibration": calibration,
        "calibration_ok": calibration_ok,
        "signatures": signatures_completes if calibration_ok else reference,
        "n_reference": len(reference),
        "n_nouvelles": len(signatures),
        "n_total_livrees": len(signatures_completes) if calibration_ok else len(reference),
        "nouvelles": signatures,
        "sources": sources_out,
        "avertissements": erreurs,
        "regle": "les 26 nouvelles signatures ne sont livrées à `signatures` que si la calibration est 44/44 ; "
                 "sinon elles restent dans `nouvelles` pour diagnostic et le rejeu reste incomplet.",
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"calibration : {calibration['ok']}/{calibration['n']} ; échecs : {calibration['fails']}")
    print(f"signatures   : {len(signatures)}/{len(a_signer)} ; sortie : {sortie}")
    for e in erreurs:
        print(" -", e)
    if calibration["ok"] != calibration["n"]:
        return 2
    if len(signatures) != len(a_signer):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

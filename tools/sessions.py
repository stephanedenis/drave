#!/usr/bin/env python3
"""sessions.py — plans de session : qui fait quoi, avant d'écrire `en-cours`.

Chaque session active expose son mandat dans `journal/sessions/<id>/plan.md` :
périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
sessions consultent `--status` avant de claim, et `--check` refuse les mandats
incomplets, les identifiants dupliqués, les périmètres qui se recouvrent et
les heartbeats périmés. `en-cours` reste la seule source de l'état : ce plan
est le **contrat de travail** qui le précède.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SESSIONS = "journal/sessions"
ETAT = "docs/pilotage/en-cours.md"
CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
          "prochaine action", "état")
ACTIFS = {"actif", "active", "en cours", "bloqué", "bloquee", "bloqué(e)"}
PEREMPTION_MIN = 45


def _cle(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def _valeur(s: str) -> str:
    return s.strip().strip("`").strip()


def lire_plan(chemin: Path) -> dict:
    champs: dict[str, str] = {}
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*[-*]\s*\*\*(.+?)\*\*\s*:\s*(.*?)\s*$", ligne)
        if m:
            champs[_cle(m.group(1))] = _valeur(m.group(2))
    # tolérances : Role / Perimetre sans accent
    for alias, cible in (("role", "rôle"), ("perimetre", "périmètre"),
                         ("fichiers reserves", "fichiers réservés"),
                         ("prochaine", "prochaine action"), ("etat", "état")):
        if cible not in champs and alias in champs:
            champs[cible] = champs[alias]
    sid = champs.get("session") or chemin.parent.name
    per = [x.strip().strip("`") for x in re.split(r"[,;]", champs.get("périmètre", "")) if x.strip()]
    fic = [x.strip().strip("`") for x in re.split(r"[,;]", champs.get("fichiers réservés", "")) if x.strip()]
    hb = champs.get("heartbeat", "")
    heartbeat = None
    age = None
    try:
        brut = re.sub(r"\s*(HAE|EDT|EST|UTC[−-]?[0-9]+)\s*$", "", hb).strip()
        if "T" in brut:
            heartbeat = datetime.fromisoformat(brut)
        else:
            heartbeat = datetime.strptime(brut, "%Y-%m-%d %H:%M")
        age = (datetime.now() - heartbeat).total_seconds() / 60.0
    except Exception:
        pass
    return {"id": sid, "chemin": chemin, "champs": champs, "perimetre": per,
            "fichiers": fic, "heartbeat": heartbeat, "age": age,
            "etat": _cle(champs.get("état", ""))}


def decouvrir(racine: Path) -> list[dict]:
    base = racine / SESSIONS
    plans = []
    if base.is_dir():
        for chemin in sorted(base.glob("*/plan.md")):
            if chemin.parent.name.startswith("_"):
                continue
            plans.append(lire_plan(chemin))
    return plans


def ids_en_cours(racine: Path) -> list[str]:
    p = racine / ETAT
    if not p.exists():
        return []
    texte = p.read_text(encoding="utf-8")
    return re.findall(r"^###\s+Session\s+`?([A-Za-z0-9_.-]+)`?", texte, re.M)


def verifier(racine: Path, strict: bool = False) -> tuple[list[str], list[str]]:
    erreurs: list[str] = []
    avertissements: list[str] = []
    plans = decouvrir(racine)
    actifs = [p for p in plans if p["etat"] in ACTIFS]
    vus: dict[str, str] = {}
    for p in plans:
        manquants = [c for c in CHAMPS if c not in p["champs"]]
        if manquants:
            erreurs.append(f"{p['chemin']} : champ(s) manquant(s) — {', '.join(manquants)}")
        if p["etat"] not in ACTIFS and p["etat"] not in {"terminé", "termine", "libre", "libre."}:
            erreurs.append(f"{p['chemin']} : état inconnu {p['etat']!r}")
        if p["age"] is None:
            erreurs.append(f"{p['chemin']} : heartbeat illisible")
        if p["id"] in vus:
            erreurs.append(f"id dupliqué : {p['id']} ({vus[p['id']]} et {p['chemin']})")
        vus[p["id"]] = str(p["chemin"])
    for i, a in enumerate(actifs):
        if a["age"] is not None and a["age"] > PEREMPTION_MIN:
            msg = f"mandat périmé ({a['age']:.0f} min) : {a['id']} — heartbeat à rafraîchir"
            (erreurs if strict else avertissements).append(msg)
        for b in actifs[i + 1:]:
            commun = sorted(set(a["perimetre"]) & set(b["perimetre"]))
            if commun:
                erreurs.append(f"périmètre recouvrant : {a['id']} et {b['id']} — {', '.join(commun)}")
            for fa in a["fichiers"]:
                for fb in b["fichiers"]:
                    if fa == fb:
                        erreurs.append(f"fichier réservé deux fois : {fa} ({a['id']}, {b['id']})")
                    elif fa.startswith(fb.rstrip("*")) or fb.startswith(fa.rstrip("*")):
                        avertissements.append(f"fichiers proches : {fa} ({a['id']}) / {fb} ({b['id']})")
    en_cours = set(ids_en_cours(racine))
    for sid in sorted(en_cours):
        if sid not in vus:
            msg = f"session en-cours sans plan : {sid}"
            (erreurs if strict else avertissements).append(msg)
    for p in actifs:
        if en_cours and p["id"] not in en_cours:
            msg = f"plan actif non listé dans en-cours : {p['id']}"
            (avertissements if not strict else erreurs).append(msg)
    return erreurs, avertissements


def afficher(racine: Path) -> int:
    plans = decouvrir(racine)
    erreurs, avertissements = verifier(racine)
    print("sessions · plans de mandat")
    if not plans:
        print("  (aucun plan — chaque session active doit créer journal/sessions/<id>/plan.md)")
    for p in plans:
        age = "—" if p["age"] is None else f"{p['age']:.0f} min"
        marque = "⏰" if p["age"] is not None and p["age"] > PEREMPTION_MIN and p["etat"] in ACTIFS else " "
        per = ", ".join(p["perimetre"]) or "—"
        print(f"  {marque} {p['id'][:18]:18} · {p['etat'] or '?':8} · {age:>7} · {per}")
        if p["champs"].get("prochaine action"):
            print(f"      → {p['champs']['prochaine action']}")
    for a in avertissements:
        print(f"  ⚠ {a}")
    for e in erreurs:
        print(f"  ❌ {e}")
    return 1 if erreurs else 0


def autotest() -> int:
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "docs/pilotage").mkdir(parents=True)
        (r / ETAT).write_text("### Session `a` — test\n", encoding="utf-8")
        d = r / SESSIONS / "a"
        d.mkdir(parents=True)
        (d / "plan.md").write_text(
            "# Plan\n\n- **Session** : `a`\n- **Rôle** : test\n- **Périmètre** : A8.0\n"
            "- **Fichiers réservés** : `tools/a.py`\n- **Heartbeat** : 2026-10-30 11:00 HAE\n"
            "- **Prochaine action** : finir\n- **État** : actif\n", encoding="utf-8")
        e, _ = verifier(r)
        assert not e, e
        b = r / SESSIONS / "b"
        b.mkdir(parents=True)
        (b / "plan.md").write_text(
            "# Plan\n\n- **Session** : `b`\n- **Rôle** : test\n- **Périmètre** : A8.0\n"
            "- **Fichiers réservés** : `tools/b.py`\n- **Heartbeat** : 2026-10-30 11:00 HAE\n"
            "- **Prochaine action** : finir\n- **État** : actif\n", encoding="utf-8")
        e, _ = verifier(r)
        assert any("recouvrant" in x for x in e), e
        (b / "plan.md").unlink()
        (d / "plan.md").write_text(
            "# Plan\n\n- **Session** : `a`\n- **Rôle** : test\n- **Heartbeat** : 2026-10-30 11:00 HAE\n"
            "- **État** : actif\n", encoding="utf-8")
        e, _ = verifier(r)
        assert any("manquant" in x for x in e), e
    print("autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé")
    return 0


MODELE = """# Plan de session — <id>

> **Mandat vivant.** Écris ce fichier **avant** `en-cours`, mets-le à jour à chaque cycle,
> et passe `État : terminé` quand la session se retire.

- **Session** : `<id>`
- **Rôle** : <chantier / programme>
- **Périmètre** : <A8.0, R13, ...>
- **Fichiers réservés** : `tools/...`, `reports/...`
- **Heartbeat** : <AAAA-MM-JJ HH:MM HAE>
- **Prochaine action** : <une action nommée>
- **État** : actif
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--racine", default=str(RACINE))
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--modele", action="store_true")
    ap.add_argument("--autotest", action="store_true")
    a = ap.parse_args()
    if a.modele:
        print(MODELE)
        return 0
    if a.autotest:
        return autotest()
    r = Path(a.racine).resolve()
    if a.check:
        e, w = verifier(r, strict=a.strict)
        for x in w:
            print(f"  ⚠ {x}")
        for x in e:
            print(f"  ❌ {x}")
        if not e and not w:
            print("  ✅ plans cohérents")
        return 1 if e or (a.strict and w) else 0
    return afficher(r)


if __name__ == "__main__":
    sys.exit(main())

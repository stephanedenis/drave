#!/usr/bin/env python3
"""sessions.py — plans de session : qui fait quoi, avant d'écrire `en-cours`.

Chaque session active expose son mandat dans `journal/sessions/<id>/plan.md` :
périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
sessions consultent `--status` avant de claim, et `--check --strict` refuse les
mandats incomplets, les identifiants dupliqués, les périmètres qui se recouvrent
et les heartbeats périmés (le `--check` seul les signale). Les **fichiers
proches** (une réservation imbriquée dans une autre, `data/` ⊃ `data/structures/`)
restent des **avertissements**, même en strict : l'imbrication est le régime
normal d'un territoire partagé, et une porte qui échoue sur toute imbrication
est rouge dès qu'une session réserve un sous-dossier — mesuré le 02/11, le
strict sortait en 1 avec **0 erreur et 4 avertissements**. `en-cours` reste la
seule source de l'état : ce plan est le **contrat de travail** qui le précède.
Une session arrêtée (reboot, panne) passe à `État : en pause` : elle reste dans
l'état, son heartbeat n'est plus exigé, et la reprise la remet `actif`.
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
PAUSE = {"en pause", "pause", "suspendu", "suspendue"}
A_CONFIRMER = {"à confirmer", "a confirmer"}
ETATS_CONNUS = ACTIFS | PAUSE | {"terminé", "termine", "libre", "libre."} | A_CONFIRMER
PEREMPTION_MIN = 45


def _cle(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def _valeur(s: str) -> str:
    return s.strip().strip("`").strip()


def lire_plan(chemin: Path) -> dict:
    champs: dict[str, str] = {}
    # un champ peut tenir sur plusieurs lignes (réservations, périmètre) : on prend la ligne du
    # champ ET ses continuations jusqu'au prochain « - **champ** ». Sans cela, la moitié des
    # fichiers réservés n'était pas vérifiée (mesuré sur le plan de la session Pensée : 2 items
    # lus au lieu de 9).
    texte = chemin.read_text(encoding="utf-8")
    for m in re.finditer(r"^\s*[-*]\s*\*\*(.+?)\*\*\s*:\s*"
                         r"(.*(?:\n(?![ \t]*(?:[-*]\s*\*\*|#)).*)*)", texte, re.M):
        valeur = " ".join(x.strip() for x in m.group(2).splitlines()).strip()
        champs[_cle(m.group(1))] = _valeur(valeur)
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


def sections_en_cours(racine: Path) -> list[dict]:
    p = racine / ETAT
    if not p.exists():
        return []
    texte = p.read_text(encoding="utf-8")
    m = re.search(r"Mis à jour\s*:\s*(\d{4}-\d{2}-\d{2}),\s*(\d{1,2})\s*h\s*(\d{2})", texte)
    heartbeat = f"{m.group(1)} {int(m.group(2)):02d}:{m.group(3)} HAE" if m else ""
    morceaux = re.split(r"^###\s+Session\s+`?([A-Za-z0-9_.-]+)`?\s*—\s*(.*)$", texte, flags=re.M)
    out = []
    for i in range(1, len(morceaux), 3):
        sid, role, bloc = morceaux[i], morceaux[i + 1].strip(), morceaux[i + 2]
        champs = {}
        for mm in re.finditer(r"^-\s+\*\*(.+?)\*\*\s*:\s*(.*(?:\n(?![ \t]*(?:-\s+\*\*|#)).*)*)", bloc, re.M):
            champs[_cle(mm.group(1))] = " ".join(x.strip() for x in mm.group(2).splitlines()).strip()
        out.append({"id": sid, "role": role, "champs": champs,
                    "fichiers": champs.get("fichiers réservés", ""),
                    "prochaine": champs.get("prochaine action", ""),
                    "heartbeat": heartbeat})
    return out


def depuis_en_cours(racine: Path) -> int:
    """Crée un plan *à confirmer* à partir de la section `en-cours`, sans l'inventer."""
    n = 0
    for s in sections_en_cours(racine):
        chemin = racine / SESSIONS / s["id"] / "plan.md"
        if chemin.exists():
            continue
        chemin.parent.mkdir(parents=True, exist_ok=True)
        heartbeat = s["heartbeat"] or datetime.now().strftime("%Y-%m-%d %H:%M HAE")
        role = s["role"] or "à confirmer"
        fichiers = s["fichiers"] or "à confirmer"
        prochaine = s["prochaine"] or "à confirmer"
        chemin.write_text(f"""# Plan de session — {s['id']}

> **Repris de `en-cours` le {datetime.now().strftime('%Y-%m-%d %H:%M')}** — plan *à confirmer* par la
> session : le heartbeat est celui de l'état, pas une preuve de vie.

- **Session** : `{s['id']}`
- **Rôle** : {role}
- **Périmètre** : à confirmer
- **Fichiers réservés** : {fichiers}
- **Heartbeat** : {heartbeat}
- **Prochaine action** : {prochaine}
- **État** : à confirmer
""", encoding="utf-8")
        n += 1
        print(f"  + {chemin.relative_to(racine)}")
    print(f"  {n} plan(s) créé(s) à confirmer ; les sessions les complètent, elles ne sont pas actives.")
    return 0


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
        if p["etat"] not in ETATS_CONNUS:
            erreurs.append(f"{p['chemin']} : état inconnu {p['etat']!r}")
        if p["etat"] in A_CONFIRMER:
            (erreurs if strict else avertissements).append(
                f"plan à confirmer : {p['id']} — la session doit le compléter")
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
        # une session arrêtée passe en pause : plus de heartbeat exigé, même en strict
        (d / "plan.md").write_text(
            "# Plan\n\n- **Session** : `a`\n- **Rôle** : test\n- **Périmètre** : A8.0\n"
            "- **Fichiers réservés** : `tools/a.py`\n- **Heartbeat** : 2026-10-30 11:00 HAE\n"
            "- **Prochaine action** : reprendre\n- **État** : en pause\n", encoding="utf-8")
        e, _ = verifier(r)
        assert not e, e
        e, _ = verifier(r, strict=True)
        assert not e, e
        # une réservation IMBRIQUÉE (data/ ⊃ data/structures/) est un avertissement,
        # pas un refus strict : le territoire partagé est le régime normal
        frais = datetime.now().strftime("%Y-%m-%d %H:%M")
        (r / ETAT).write_text("### Session `a` — test\n### Session `b` — test\n",
                              encoding="utf-8")
        (d / "plan.md").write_text(
            "# Plan\n\n- **Session** : `a`\n- **Rôle** : test\n- **Périmètre** : A8.0\n"
            "- **Fichiers réservés** : `data/`\n"
            f"- **Heartbeat** : {frais} HAE\n"
            "- **Prochaine action** : finir\n- **État** : actif\n", encoding="utf-8")
        b.mkdir(parents=True, exist_ok=True)
        (b / "plan.md").write_text(
            "# Plan\n\n- **Session** : `b`\n- **Rôle** : test\n- **Périmètre** : A8.1\n"
            "- **Fichiers réservés** : `data/structures/`\n"
            f"- **Heartbeat** : {frais} HAE\n"
            "- **Prochaine action** : finir\n- **État** : actif\n", encoding="utf-8")
        e, w = verifier(r, strict=True)
        assert not e, e
        assert any("proches" in x for x in w), w
    print("autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, "
          "pause sans heartbeat exigé, réservation imbriquée avertie sans refus")
    return 0


MODELE = """# Plan de session — <id>

> **Mandat vivant.** Écris ce fichier **avant** `en-cours`, mets-le à jour à chaque cycle,
> et passe `État : en pause` (arrêt) ou `État : terminé` (retrait) quand elle s'arrête.

- **Session** : `<id>`
- **Rôle** : <chantier / programme>
- **Périmètre** : <A8.0, R13, ...>
- **Fichiers réservés** : `tools/...`, `reports/...`
- **Heartbeat** : <AAAA-MM-JJ HH:MM HAE>
- **Prochaine action** : <une action nommée>
- **État** : actif (ou `en pause` / `terminé`)
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--racine", default=str(RACINE))
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--modele", action="store_true")
    ap.add_argument("--autotest", action="store_true")
    ap.add_argument("--depuis-en-cours", action="store_true",
                    help="crée des plans à confirmer depuis les sections de en-cours")
    a = ap.parse_args()
    if a.modele:
        print(MODELE)
        return 0
    if a.autotest:
        return autotest()
    r = Path(a.racine).resolve()
    if a.depuis_en_cours:
        return depuis_en_cours(r)
    if a.check:
        e, w = verifier(r, strict=a.strict)
        for x in w:
            print(f"  ⚠ {x}")
        for x in e:
            print(f"  ❌ {x}")
        if not e and not w:
            print("  ✅ plans cohérents")
        # le contrat strict porte sur les ERREURS (champs, identifiants, périmètres,
        # heartbeats) ; « fichiers proches » reste un avertissement — sinon quatre
        # sessions qui imbriquent leur territoire (`data/` ⊃ `data/structures/`) rendent
        # la porte rouge sans qu'aucune réservation ne se recouvre réellement.
        return 1 if e else 0
    return afficher(r)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""ressources.py — le registre des ressources de Hauru et le protocole de claim.

Pourquoi. Le pilotage réservait des **fichiers** (`sessions.py`) et surveillait les
**fichiers en mouvement** (`surveille_sessions.py`), mais pas la **machine** : deux
sessions pouvaient lancer deux entraînements sur le même GPU, ou saturer le même
NVMe, sans le voir. Ce registre rend les ressources explicites, les réserve et met
en file ce qui ne tient pas — pour éviter les attentes inutiles et les simultanéités
intenses.

Capacités (Hauru, 2026-11-02) :
  gpu0 / gpu1 : 1 job exclusif, 16 Gio de VRAM, NUMA 0 (0-9,20-29)
  cpu0        : 20 fils (0-9,20-29), réserve 4 → 16 fils utilisables
  cpu1        : 20 fils (10-19,30-39), réserve 4 → 16 fils utilisables
  ram         : 125 Gio, réserve 16 → 109 Gio utilisables
  nvme_system : 1 IO lourde, / (Fanxiang 1 To : /, /home, /FastNVMe)
  nvme_raid   : 1 IO lourde, /home/stephane/IA (RAID0 4× NVMe, ~33 Gio libres)
  hdd_data13tb: 1 IO lourde, /home/stephane/Data13TB (HDD 10,9 To)
  machine     : 1 job exclusif global (passe complète des portes, mesure globale)

Le registre vit dans `work/ressources.json` (ignoré par git) ; la politique est
dans `docs/pilotage/plan-travail.md` § 10. Le registre est **consultatif** : il
n'empêche pas un job de tourner, il dit si le claim tient et ce qui est libre.
L'application dure (cgroups) se ferait avec `systemd-run`/`AllowedCPUs`.

Usage :
  python3 tools/ressources.py --status
  python3 tools/ressources.py --claim --session <id> --job <nom> \\
      --res "gpu0=exclusive,cpu0=12,ram=60,nvme_raid=heavy:20" --prio 1 --eta 240
  python3 tools/ressources.py --release --session <id> [--job <nom>]
  python3 tools/ressources.py --check [--strict]
  python3 tools/ressources.py --suggest
  python3 tools/ressources.py --actual
  python3 tools/ressources.py --autotest
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime

RACINE = pathlib.Path(__file__).resolve().parents[1]
LEDGER = RACINE / "work/ressources.json"

RESSOURCES = {
    "gpu0": {"kind": "gpu", "cap": 1, "numa": 0, "vram": 16,
             "label": "Quadro RTX 5000 (slot 2)"},
    "gpu1": {"kind": "gpu", "cap": 1, "numa": 0, "vram": 16,
             "label": "Quadro RTX 5000 (slot 4)"},
    "cpu0": {"kind": "cpu", "cap": 20, "reserve": 4, "numa": 0,
             "label": "Xeon socket 0 (0-9,20-29)"},
    "cpu1": {"kind": "cpu", "cap": 20, "reserve": 4, "numa": 1,
             "label": "Xeon socket 1 (10-19,30-39)"},
    "ram": {"kind": "ram", "cap": 125, "reserve": 16, "label": "RAM 125 Gio"},
    "nvme_system": {"kind": "io", "cap": 1, "mount": "/",
                     "label": "NVMe 1 To système (/ /home /FastNVMe)"},
    "nvme_raid": {"kind": "io", "cap": 1, "mount": "/home/stephane/IA",
                  "label": "RAID0 4× NVMe (/home/stephane/IA)"},
    "hdd_data13tb": {"kind": "io", "cap": 1, "mount": "/home/stephane/Data13TB",
                     "label": "HDD 10,9 To (Data13TB)"},
    "machine": {"kind": "global", "cap": 1,
                "label": "passe complète des portes / mesure globale"},
}


# --------------------------------------------------------------------------- #
# Le registre
# --------------------------------------------------------------------------- #
def lire(chemin: pathlib.Path) -> dict:
    if not chemin.exists():
        return {"claims": [], "queue": []}
    try:
        data = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"claims": [], "queue": []}
    data.setdefault("claims", [])
    data.setdefault("queue", [])
    return data


def ecrire(chemin: pathlib.Path, data: dict) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    tmp = chemin.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(chemin)


def libre_go(ressource: str) -> int:
    r = RESSOURCES[ressource]
    mount = r.get("mount")
    if not mount:
        return 0
    try:
        return shutil.disk_usage(mount).free // (1024 ** 3)
    except OSError:
        return 0


def utile(ressource: str) -> int:
    r = RESSOURCES[ressource]
    if r["kind"] == "cpu":
        return r["cap"] - r.get("reserve", 0)
    if r["kind"] == "ram":
        return r["cap"] - r.get("reserve", 0)
    return r["cap"]


def parse_res(brut: str) -> dict:
    """Parse ``gpu0=exclusive,cpu0=12,ram=60,nvme_raid=heavy:20``."""
    res: dict = {}
    for morceau in [x.strip() for x in brut.split(",") if x.strip()]:
        if "=" not in morceau:
            raise ValueError(f"réservation invalide : {morceau!r} (attendu ressource=valeur)")
        nom, valeur = (x.strip() for x in morceau.split("=", 1))
        if nom not in RESSOURCES:
            raise ValueError(f"ressource inconnue : {nom!r} (connues : {', '.join(RESSOURCES)})")
        kind = RESSOURCES[nom]["kind"]
        if kind in ("gpu", "global"):
            if valeur not in ("exclusive", "shared"):
                raise ValueError(f"{nom} : valeur {valeur!r} (attendu exclusive|shared)")
            if kind == "global" and valeur != "exclusive":
                raise ValueError(f"{nom} : la passe globale est forcément exclusive")
            res[nom] = valeur
        elif kind in ("cpu", "ram"):
            try:
                n = int(valeur)
            except ValueError as exc:
                raise ValueError(f"{nom} : {valeur!r} n'est pas un entier") from exc
            if n < 1:
                raise ValueError(f"{nom} : {n} doit être > 0")
            res[nom] = n
        else:  # io
            mode, _, gb = valeur.partition(":")
            if mode not in ("heavy", "light"):
                raise ValueError(f"{nom} : {valeur!r} (attendu heavy[:Gio]|light)")
            if gb:
                try:
                    int(gb)
                except ValueError as exc:
                    raise ValueError(f"{nom} : {gb!r} n'est pas un nombre de Gio") from exc
            res[nom] = valeur
    if not res:
        raise ValueError("aucune ressource réservée")
    return res


def charges(ledger: dict) -> dict:
    c = {r: 0 for r in RESSOURCES}
    for claim in ledger["claims"]:
        for r, v in claim["res"].items():
            if RESSOURCES[r]["kind"] in ("gpu", "global"):
                c[r] += 1
            elif RESSOURCES[r]["kind"] in ("cpu", "ram"):
                c[r] += int(v)
            elif RESSOURCES[r]["kind"] == "io" and str(v).startswith("heavy"):
                c[r] += 1
    return c


def reserves_go(ledger: dict, ressource: str) -> int:
    n = 0
    for claim in ledger["claims"]:
        v = claim["res"].get(ressource)
        if v and ":" in str(v):
            n += int(str(v).split(":", 1)[1])
    return n


# --------------------------------------------------------------------------- #
# Les conflits
# --------------------------------------------------------------------------- #
def conflits(ledger: dict, claim: dict) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    res = claim["res"]
    actifs = ledger["claims"]

    if "machine" in res:
        if actifs:
            errs.append("machine exclusive : des réservations sont déjà actives")
    elif any("machine" in c["res"] for c in actifs):
        errs.append("machine exclusive en cours : aucune autre réservation")

    for r, v in res.items():
        kind = RESSOURCES[r]["kind"]
        if kind == "gpu":
            n = sum(1 for c in actifs if r in c["res"])
            if n >= 1:
                errs.append(f"{r} : déjà réservé (1 job exclusif à la fois)")
        elif kind == "cpu":
            total = sum(int(c["res"].get(r, 0)) for c in actifs) + int(v)
            if total > utile(r):
                errs.append(f"{r} : {total} fils > {utile(r)} utilisables (réserve {RESSOURCES[r]['reserve']})")
        elif kind == "ram":
            total = sum(int(c["res"].get(r, 0)) for c in actifs) + int(v)
            if total > utile(r):
                errs.append(f"{r} : {total} Gio > {utile(r)} utilisables (réserve {RESSOURCES[r]['reserve']})")
        elif kind == "io":
            mode = str(v).split(":", 1)[0]
            if mode == "heavy":
                n = sum(1 for c in actifs if str(c["res"].get(r, "")).startswith("heavy"))
                if n >= 1:
                    errs.append(f"{r} : IO lourde déjà réservée")
                if ":" in str(v):
                    gb = int(str(v).split(":", 1)[1])
                    dispo = libre_go(r)
                    deja = reserves_go(ledger, r)
                    if gb + deja > dispo:
                        errs.append(f"{r} : {gb} Gio demandés + {deja} déjà réservés > {dispo} Gio libres")
                if r == "nvme_system":
                    warns.append("IO lourde sur le NVMe système : préférer nvme_raid ou hdd_data13tb")
    if ("gpu0" in res or "gpu1" in res) and "cpu1" in res:
        warns.append("GPU sur NUMA 0 : les fils du GPU devraient être réservés sur cpu0")
    for r in ("nvme_raid", "nvme_system", "hdd_data13tb"):
        if r in res and libre_go(r) < 40:
            warns.append(f"{r} : {libre_go(r)} Gio libres seulement")
    return errs, warns


def valider(ledger: dict) -> tuple[list[str], list[str]]:
    """Valide un registre complet (pour --check)."""
    errs: list[str] = []
    warns: list[str] = []
    actifs = ledger["claims"]
    c = charges(ledger)

    for r in ("gpu0", "gpu1", "machine"):
        if c[r] > 1:
            errs.append(f"{r} : {c[r]} réservations actives (1 maximum)")
    if c["machine"] and len(actifs) > c["machine"]:
        errs.append("machine exclusive avec d'autres réservations")
    for r in ("cpu0", "cpu1"):
        if c[r] > utile(r):
            errs.append(f"{r} : {c[r]} fils > {utile(r)} utilisables")
    if c["ram"] > utile("ram"):
        errs.append(f"ram : {c['ram']} Gio > {utile('ram')} utilisables")
    for r in ("nvme_system", "nvme_raid", "hdd_data13tb"):
        if c[r] > 1:
            errs.append(f"{r} : {c[r]} IO lourdes actives (1 maximum)")
        engages = reserves_go(ledger, r)
        if engages > libre_go(r):
            errs.append(f"{r} : {engages} Gio réservés > {libre_go(r)} Gio libres")
        if libre_go(r) < 40:
            warns.append(f"{r} : {libre_go(r)} Gio libres seulement")
    for claim in actifs:
        res = claim["res"]
        if ("gpu0" in res or "gpu1" in res) and "cpu1" in res:
            warns.append(f"{claim['session']} : GPU sur NUMA 0 avec des fils sur cpu1")
    return errs, warns


# --------------------------------------------------------------------------- #
# Les commandes
# --------------------------------------------------------------------------- #
def cmd_status(chemin: pathlib.Path, ledger: dict) -> int:
    c = charges(ledger)
    print("ressources · Hauru — registre", chemin)
    print(f"  {'ressource':14} {'type':7} {'capacité':>10} {'utilisé':>8} {'libre':>8}  détail")
    for r, meta in RESSOURCES.items():
        kind = meta["kind"]
        if kind == "cpu":
            cap, used = utile(r), c[r]
            detail = f"réserve {meta['reserve']} fils"
        elif kind == "ram":
            cap, used = utile(r), c[r]
            detail = f"réserve {meta['reserve']} Gio"
        elif kind == "io":
            cap, used = 1, c[r]
            detail = f"{libre_go(r)} Gio libres · {reserves_go(ledger, r)} Gio réservés"
        elif kind == "global":
            cap, used = 1, c[r]
            detail = "passe complète"
        else:
            cap, used = 1, c[r]
            detail = f"{meta.get('vram', 0)} Gio VRAM · NUMA {meta.get('numa', '—')}"
        libre = cap - used
        marque = " ⚠" if libre < 0 else ""
        print(f"  {r:14} {kind:7} {cap:>10} {used:>8} {libre:>8}  {detail}{marque}")
    print()
    if ledger["claims"]:
        print("  Réservations actives :")
        for claim in ledger["claims"]:
            res = ", ".join(f"{k}={v}" for k, v in claim["res"].items())
            print(f"    · {claim['session']} / {claim['job']} : {res} "
                  f"(prio {claim.get('prio', 3)}, {claim.get('eta_min', '?')} min)")
    else:
        print("  Aucune réservation active.")
    if ledger["queue"]:
        print("  File d'attente :")
        for claim in ledger["queue"]:
            res = ", ".join(f"{k}={v}" for k, v in claim["res"].items())
            print(f"    ⏸ {claim['session']} / {claim['job']} : {res} "
                  f"(prio {claim.get('prio', 3)}, {claim.get('eta_min', '?')} min)")
    return 0


def cmd_claim(chemin: pathlib.Path, ledger: dict, args) -> int:
    if not args.session or not args.job or not args.res:
        print("  ❌ --claim exige --session, --job et --res", file=sys.stderr)
        return 2
    try:
        res = parse_res(args.res)
    except ValueError as exc:
        print(f"  ❌ {exc}", file=sys.stderr)
        return 2
    if any(c["session"] == args.session and c["job"] == args.job for c in ledger["claims"]):
        print(f"  ❌ {args.session} / {args.job} a déjà une réservation active", file=sys.stderr)
        return 1
    claim = {
        "id": f"{args.session}:{args.job}:{int(time.time())}",
        "session": args.session,
        "job": args.job,
        "res": res,
        "prio": args.prio,
        "eta_min": args.eta,
        "created": datetime.now().isoformat(timespec="seconds"),
    }
    if args.note:
        claim["note"] = args.note
    errs, warns = conflits(ledger, claim)
    if errs:
        claim["state"] = "pending"
        ledger["queue"].append(claim)
        ecrire(chemin, ledger)
        print(f"  ⏸ différé : {args.session} / {args.job}")
        for e in errs:
            print(f"     · {e}")
        print(f"     → placé en file (position {len(ledger['queue'])}) ; "
              "prends une autre tâche ou attends la libération.")
        for w in warns:
            print(f"     ⚠ {w}")
        return 0
    ledger["claims"].append(claim)
    ecrire(chemin, ledger)
    print(f"  ✅ accordé : {args.session} / {args.job}")
    for w in warns:
        print(f"     ⚠ {w}")
    return 0


def admettre(ledger: dict) -> int:
    if not ledger["queue"]:
        return 0
    restants = []
    admis = 0
    for claim in sorted(ledger["queue"], key=lambda x: (x.get("prio", 3), x.get("created", ""))):
        errs, _ = conflits(ledger, claim)
        if errs:
            restants.append(claim)
            continue
        propre = dict(claim)
        propre.pop("state", None)
        ledger["claims"].append(propre)
        admis += 1
        print(f"  ▶ admis : {claim['session']} / {claim['job']}")
    ledger["queue"] = restants
    return admis


def cmd_release(chemin: pathlib.Path, ledger: dict, args) -> int:
    if not args.session:
        print("  ❌ --release exige --session", file=sys.stderr)
        return 2
    avant = len(ledger["claims"])
    ledger["claims"] = [
        c for c in ledger["claims"]
        if not (c["session"] == args.session and (not args.job or c["job"] == args.job))
    ]
    liberes = avant - len(ledger["claims"])
    if liberes == 0:
        print(f"  ℹ aucune réservation active pour {args.session}"
              + (f" / {args.job}" if args.job else ""))
    else:
        print(f"  ✅ libéré : {liberes} réservation(s) de {args.session}"
              + (f" / {args.job}" if args.job else ""))
    admettre(ledger)
    ecrire(chemin, ledger)
    return 0


def cmd_check(chemin: pathlib.Path, ledger: dict, strict: bool) -> int:
    errs, warns = valider(ledger)
    if not errs:
        print("  ✅ registre cohérent : aucune ressource sur-réservée.")
    else:
        print(f"  ❌ {len(errs)} conflit(s) :")
        for e in errs:
            print(f"     · {e}")
    for w in warns:
        print(f"  ⚠ {w}")
    if errs:
        return 1
    if strict and warns:
        print("  ❌ --strict : les avertissements comptent comme des conflits.")
        return 1
    return 0


def cmd_suggest(chemin: pathlib.Path, ledger: dict) -> int:
    c = charges(ledger)
    libres = []
    for r in ("gpu0", "gpu1"):
        if c[r] == 0:
            libres.append(f"{r} libre")
    for r in ("cpu0", "cpu1"):
        n = utile(r) - c[r]
        libres.append(f"{r} : {n} fils libres")
    n = utile("ram") - c["ram"]
    libres.append(f"ram : {n} Gio libres")
    for r in ("nvme_raid", "nvme_system", "hdd_data13tb"):
        if c[r] == 0:
            libres.append(f"{r} : libre, {libre_go(r)} Gio")
    print("  Libre maintenant : " + " · ".join(libres))
    if ledger["queue"]:
        print(f"  File : {len(ledger['queue'])} claim(s) en attente — "
              "libère une ressource pour les admettre.")
    else:
        print("  File vide.")
    print("  Règle : si la ressource voulue est prise, prends une tâche compatible "
          "plutôt que d'attendre.")
    return 0


def cmd_actual(chemin: pathlib.Path, ledger: dict) -> int:
    print("  Réel · GPU")
    try:
        idx = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,uuid", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10,
        ).stdout
        uuid_index = {}
        for ligne in idx.splitlines():
            if "," in ligne:
                i, u = [x.strip() for x in ligne.split(",", 1)]
                uuid_index[u] = i
        proc = subprocess.run(
            ["nvidia-smi", "--query-compute-apps=gpu_uuid,pid,process_name,used_memory",
             "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10,
        ).stdout
        par_gpu: dict[str, list[str]] = {}
        for ligne in proc.splitlines():
            morceaux = [x.strip() for x in ligne.split(",")]
            if len(morceaux) < 4:
                continue
            u, pid, nom, mem = morceaux[:4]
            g = uuid_index.get(u, u)
            par_gpu.setdefault(g, []).append(f"PID {pid} {nom} ({mem})")
        for i in ("0", "1"):
            lignes = par_gpu.get(i, [])
            reserve = any(f"gpu{i}" in c["res"] for c in ledger["claims"])
            etat = "réservé" if reserve else "non réservé"
            print(f"    GPU{i} ({etat}) : " + (" ; ".join(lignes) if lignes else "aucun processus"))
            if lignes and not reserve:
                print(f"      ⚠ GPU{i} utilisé sans réservation")
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"    (nvidia-smi indisponible : {exc})")

    print("  Réel · CPU (top 8)")
    try:
        ps = subprocess.run(
            ["ps", "-eo", "pid,comm,pcpu,pmem", "--sort=-pcpu"],
            capture_output=True, text=True, timeout=10,
        ).stdout.splitlines()
        for ligne in ps[:9]:
            print("    " + ligne)
    except (OSError, subprocess.SubprocessError):
        pass

    print("  Réel · stockage")
    for r in ("nvme_system", "nvme_raid", "hdd_data13tb"):
        print(f"    {r:14} {libre_go(r)} Gio libres ({RESSOURCES[r]['mount']})")
    return 0


def autotest() -> int:
    with tempfile.TemporaryDirectory() as d:
        ledger = str(pathlib.Path(d) / "ressources.json")

        def run(*args):
            return subprocess.run(
                [sys.executable, str(pathlib.Path(__file__).resolve()), "--ledger", ledger, *args],
                capture_output=True, text=True, timeout=30,
            )

        cas = []
        r = run("--status")
        cas.append(("status vide", r.returncode == 0, r.returncode))
        r = run("--claim", "--session", "s1", "--job", "j1",
                "--res", "gpu0=exclusive,cpu0=12,ram=60,nvme_raid=heavy:5")
        cas.append(("claim gpu0 accordé", "accordé" in r.stdout, r.stdout + r.stderr))
        r = run("--claim", "--session", "s2", "--job", "j2", "--res", "gpu0=exclusive")
        cas.append(("second gpu0 différé", "différé" in r.stdout, r.stdout + r.stderr))
        r = run("--claim", "--session", "s3", "--job", "j3", "--res", "machine=exclusive")
        cas.append(("machine différée", "différé" in r.stdout, r.stdout + r.stderr))
        r = run("--claim", "--session", "s4", "--job", "j4", "--res", "cpu1=12")
        cas.append(("cpu1 12 accordé", "accordé" in r.stdout, r.stdout + r.stderr))
        r = run("--claim", "--session", "s5", "--job", "j5", "--res", "cpu1=8")
        cas.append(("cpu1 surcharge différée", "différé" in r.stdout, r.stdout + r.stderr))
        r = run("--release", "--session", "s1")
        cas.append(("release admet s2", "admis" in r.stdout, r.stdout + r.stderr))
        r = run("--check")
        cas.append(("registre cohérent", r.returncode == 0, r.stdout + r.stderr))
        r = run("--claim", "--session", "s6", "--job", "j6", "--res", "gpu9=exclusive")
        cas.append(("ressource inconnue refusée", r.returncode != 0, r.stdout + r.stderr))

        mauvais = [nom for nom, ok, detail in cas if not ok]
        if mauvais:
            print("  ❌ autotest : " + " · ".join(mauvais))
            for nom, ok, detail in cas:
                if not ok:
                    print(f"     --- {nom} ---\n{detail}")
            return 1
        print(f"  ✅ autotest : {len(cas)} cas (claim, conflit, file, admission, check)")
        return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", default=str(LEDGER))
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--claim", action="store_true")
    ap.add_argument("--release", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--suggest", action="store_true")
    ap.add_argument("--actual", action="store_true")
    ap.add_argument("--autotest", action="store_true")
    ap.add_argument("--session")
    ap.add_argument("--job")
    ap.add_argument("--res")
    ap.add_argument("--prio", type=int, default=3, help="1 = prioritaire, 5 = fond de file")
    ap.add_argument("--eta", type=int, default=60, help="durée estimée en minutes")
    ap.add_argument("--note")
    args = ap.parse_args(argv)

    if args.autotest:
        return autotest()
    chemin = pathlib.Path(args.ledger)
    ledger = lire(chemin)
    if args.claim:
        return cmd_claim(chemin, ledger, args)
    if args.release:
        return cmd_release(chemin, ledger, args)
    if args.check:
        return cmd_check(chemin, ledger, args.strict)
    if args.suggest:
        return cmd_suggest(chemin, ledger)
    if args.actual:
        return cmd_actual(chemin, ledger)
    return cmd_status(chemin, ledger)


if __name__ == "__main__":
    raise SystemExit(main())

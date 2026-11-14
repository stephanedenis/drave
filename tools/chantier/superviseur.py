#!/usr/bin/env python3
"""superviseur.py — le méta-harnais du chantier autonome : file de tâches, exécution, vérification.

**Le problème.** DSH donne l'**agent** : des rounds, une session reprenable (`--session-id`), la
compaction du contexte, des sous-agents. Il **ne donne pas** la couche de contrôle d'un chantier de
plusieurs jours : file de tâches persistante, vérification d'acceptation **indépendante** de
l'agent, budget, reprise après crash, escalade, journal d'audit. Ce superviseur est cette couche.

**Les trois garanties.**
1. **Une tâche n'est finie que si son acceptation passe** — une commande, un attendu, exécutés par
   le superviseur, pas par l'agent.
2. **Rien n'est perdu** : l'état (`work/chantier/etat.json`) et le journal (`work/chantier/journal.log`)
   sont écrits après **chaque** étape ; une relance reprend la première tâche non finie.
3. **On s'arrête proprement** : le fichier `work/chantier/STOP` (ou le budget, ou le nombre de
   tâches) arrête la boucle ; l'agent n'est jamais tué au milieu d'un commit.

**Usage.**
    python3 tools/chantier/superviseur.py etat          # où en est-on ?
    python3 tools/chantier/superviseur.py prochaine     # la prochaine tâche et son mandat
    python3 tools/chantier/superviseur.py executer      # exécute UNE tâche (agent + acceptation)
    python3 tools/chantier/superviseur.py boucle        # boucle jusqu'au STOP/budget
    python3 tools/chantier/superviseur.py stop          # crée le STOP (arrêt propre)
    python3 tools/chantier/superviseur.py reprendre ID  # remet une tâche en file
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import json
import pathlib
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[2]
CHANTIER = RACINE / "tools" / "chantier"
PLAN = CHANTIER / "plan.json"
WORK = RACINE / "work" / "chantier"
ETAT = WORK / "etat.json"
JOURNAL = WORK / "journal.log"
STOP = WORK / "STOP"
SESSION = WORK / "session_id.txt"
CLE = pathlib.Path.home() / ".config" / "drave" / "deepseek.key"
GATES = RACINE / "tools" / "porte-produit.sh"


def _maintenant() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _journal(ligne: str) -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(f"{_maintenant()} · {ligne}\n")


def _charger(o: pathlib.Path, defaut):
    if not o.exists():
        return defaut
    return json.loads(o.read_text(encoding="utf-8"))


def _ecrire(o: pathlib.Path, valeur) -> None:
    o.parent.mkdir(parents=True, exist_ok=True)
    o.write_text(json.dumps(valeur, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def charger_plan() -> dict:
    plan = _charger(PLAN, None)
    if plan is None:
        raise SystemExit(f"plan absent : {PLAN}")
    return plan


def charger_etat() -> dict:
    return _charger(ETAT, {"taches": {}, "depuis": _maintenant(), "budget_s": 0, "lancements": 0})


def save_etat(etat: dict) -> None:
    _ecrire(ETAT, etat)


def taches_en_file(plan: dict, etat: dict) -> list[dict]:
    return [t for t in plan["taches"] if etat["taches"].get(t["id"], {}).get("statut", "a_faire") == "a_faire"]


def session_id() -> str | None:
    return SESSION.read_text(encoding="utf-8").strip() if SESSION.exists() else None


# ------------------------------------------------------------------ acceptation

def verifier_acceptation(tache: dict) -> tuple[bool, list[str]]:
    """Exécute les commandes d'acceptation de la tâche ; rend (ok, détails)."""
    ok, details = True, []
    for test in tache.get("acceptation", []):
        commande = test["commande"]
        attendu = test.get("attendu", "")
        try:
            r = subprocess.run(commande, shell=True, cwd=RACINE, capture_output=True,
                               text=True, timeout=test.get("timeout_s", 300))
        except subprocess.TimeoutExpired:
            ok = False
            details.append(f"⌛ {commande} (timeout)")
            continue
        sortie = (r.stdout or "") + (r.stderr or "")
        if "code" in test and r.returncode != test["code"]:
            ok = False
            details.append(f"❌ {commande} → code {r.returncode} (attendu {test['code']})")
        elif attendu and attendu not in sortie:
            ok = False
            details.append(f"❌ {commande} → « {attendu} » absent")
        else:
            details.append(f"✅ {commande}")
    return ok, details


def git_avant() -> dict:
    """L'état git **avant** la tâche : HEAD et fichiers modifiés (note, jamais blocage).

    Un dépôt multi-sessions n'est jamais propre : d'autres sessions écrivent `reports/` et
    `journal/` en continu. Le superviseur n'exige pas un worktree propre ; il note le HEAD pour
    vérifier, après la tâche, qu'un commit a bien été produit.
    """
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=RACINE,
                          capture_output=True, text=True).stdout.strip()
    r = subprocess.run(["git", "status", "--porcelain"], cwd=RACINE, capture_output=True, text=True)
    modifies = [l for l in r.stdout.splitlines() if l.strip()]
    return {"head": head, "modifies": modifies[:10]}


# ------------------------------------------------------------------ exécution

def executer_tache(tache: dict, etat: dict, timeout_s: int) -> dict:
    """Lance l'agent sur le mandat, puis vérifie l'acceptation. Rend le résultat."""
    sid = session_id()
    mandat = tache["mandat"]
    commande = ["dsh", "--profile", "headless"]
    if sid:
        commande += ["--session-id", sid]
    commande.append(mandat)
    # la clé : `DEEPSEEK_API_KEY` sinon le fichier `~/.config/drave/deepseek.key`
    env = dict(os.environ)
    if not env.get("DEEPSEEK_API_KEY") and CLE.is_file():
        env["DEEPSEEK_API_KEY"] = CLE.read_text(encoding="utf-8").strip()
    if not env.get("DEEPSEEK_API_KEY"):
        _journal("⛔ clé absente : ni DEEPSEEK_API_KEY ni ~/.config/drave/deepseek.key")
        return {"statut": "echec", "debut": _maintenant(), "duree_s": 0, "code_agent": None,
                "acceptation": ["clé DeepSeek absente"], "sortie_agent": "", "cle": False}
    debut = time.time()
    _journal(f"▶ {tache['id']} — {tache['titre']} (timeout {timeout_s} s)")
    try:
        r = subprocess.run(commande, cwd=RACINE, capture_output=True, text=True,
                           timeout=timeout_s, env=env)
        code, sortie = r.returncode, (r.stdout or "")[-4000:]
    except subprocess.TimeoutExpired:
        code, sortie = 124, "(timeout : l'agent n'a pas rendu dans le budget)"
    duree = round(time.time() - debut, 1)
    ok, details = verifier_acceptation(tache)
    # l'acceptation **prime** : un agent qui a fini son travail (fiche + portes) puis dépasse le
    # timeout a réussi ; le code 124 est noté, pas pénalisé.
    resultat = {"statut": "fait" if ok else "echec",
                "timeout": code == 124,
                "debut": _maintenant(), "duree_s": duree, "code_agent": code,
                "acceptation": details, "sortie_agent": sortie[-1500:]}
    _journal(f"{'✔' if resultat['statut'] == 'fait' else '✘'} {tache['id']} en {duree} s "
             f"(code {code}) — {'; '.join(details)}")
    return resultat


# ------------------------------------------------------------------ commandes

def cmd_etat(_: argparse.Namespace) -> int:
    plan, etat = charger_plan(), charger_etat()
    print(f"chantier : {plan.get('nom', '?')} · depuis {etat.get('depuis')}")
    print(f"session : {session_id() or '(aucune — dsh créera une session neuve)'}")
    print(f"budget consommé : {etat.get('budget_s', 0)} s · lancements : {etat.get('lancements', 0)}")
    print(f"STOP : {'présent — la boucle s’arrêtera' if STOP.exists() else 'absent'}\n")
    for t in plan["taches"]:
        s = etat["taches"].get(t["id"], {}).get("statut", "a_faire")
        print(f"  [{s:8s}] {t['id']:6s} j{t.get('jour', '?')} — {t['titre']}")
    return 0


def cmd_prochaine(_: argparse.Namespace) -> int:
    plan, etat = charger_plan(), charger_etat()
    file = taches_en_file(plan, etat)
    if not file:
        print("file vide : toutes les tâches sont faites ou bloquées.")
        return 0
    t = file[0]
    print(f"{t['id']} — {t['titre']}\n\n{t['mandat']}\n")
    for a in t.get("acceptation", []):
        print(f"  acceptation : {a['commande']}" + (f" → « {a['attendu']} »" if a.get("attendu") else ""))
    return 0


def cmd_executer(args: argparse.Namespace) -> int:
    plan, etat = charger_plan(), charger_etat()
    if STOP.exists():
        print("STOP présent : on ne lance rien.")
        return 3
    avant = git_avant()
    if avant["modifies"]:
        print(f"note : {len(avant['modifies'])} fichier(s) déjà modifié(s) (autres sessions) — on continue.")
    file = taches_en_file(plan, etat)
    if not file:
        print("file vide.")
        return 0
    if args.id:
        choisie = [x for x in file if x["id"] == args.id]
        if not choisie:
            print(f"{args.id} n'est pas en file (fait, bloquée ou absente) — « reprendre {args.id} » pour la remettre.")
            return 5
        t = choisie[0]
    else:
        t = file[0]
    resultat = executer_tache(t, etat, args.timeout)
    apres = subprocess.run(["git", "rev-parse", "HEAD"], cwd=RACINE,
                           capture_output=True, text=True).stdout.strip()
    resultat["head_avant"] = avant["head"][:10]
    resultat["head_apres"] = apres[:10]
    resultat["commit_produit"] = apres != avant["head"]
    etat["taches"][t["id"]] = {"titre": t["titre"], **resultat}
    etat["budget_s"] = etat.get("budget_s", 0) + resultat["duree_s"]
    etat["lancements"] = etat.get("lancements", 0) + 1
    if resultat["statut"] == "echec":
        etat["taches"][t["id"]]["tentatives"] = etat["taches"][t["id"]].get("tentatives", 0) + 1
        if etat["taches"][t["id"]]["tentatives"] >= args.max_tentatives:
            etat["taches"][t["id"]]["statut"] = "bloque"
            _journal(f"⛔ {t['id']} bloquée après {args.max_tentatives} tentatives")
    save_etat(etat)
    print(json.dumps(resultat, ensure_ascii=False, indent=1))
    return 0 if resultat["statut"] == "fait" else 1


def cmd_boucle(args: argparse.Namespace) -> int:
    etat = charger_etat()
    debut = time.time()
    while True:
        # le plan est **relu** à chaque tour : des tâches peuvent être ajoutées pendant la boucle
        plan = charger_plan()
        if STOP.exists():
            print("STOP présent : arrêt propre."); return 0
        if etat.get("budget_s", 0) >= args.budget:
            print(f"budget atteint ({etat['budget_s']} s) : arrêt."); return 0
        file = taches_en_file(plan, etat)
        if not file:
            print("file vide : chantier terminé."); return 0
        t = file[0]
        code = cmd_executer(argparse.Namespace(id=t["id"], timeout=args.timeout,
                                               max_tentatives=args.max_tentatives))
        etat = charger_etat()
        if code != 0 and etat["taches"].get(t["id"], {}).get("statut") != "bloque":
            print(f"échec non bloquant sur {t['id']} : on continue.")
        if args.max_taches and etat.get("lancements", 0) >= args.max_taches:
            print(f"{args.max_taches} lancements atteints : arrêt."); return 0


def cmd_stop(_: argparse.Namespace) -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    STOP.write_text(f"arrêt demandé le {_maintenant()}\n", encoding="utf-8")
    _journal("⏹ STOP demandé")
    print(f"STOP écrit dans {STOP} — la boucle en cours s’arrêtera après la tâche courante.")
    return 0


def cmd_reprendre(args: argparse.Namespace) -> int:
    etat = charger_etat()
    plan = charger_plan()
    identifiants = {t["id"] for t in plan["taches"]} | set(etat["taches"])
    if args.id not in identifiants:
        print(f"tâche inconnue : {args.id}"); return 1
    titre = etat["taches"].get(args.id, {}).get("titre") or next(
        (x["titre"] for x in plan["taches"] if x["id"] == args.id), "")
    etat["taches"][args.id] = {"titre": titre, "statut": "a_faire"}
    save_etat(etat)
    _journal(f"↺ {args.id} remise en file")
    print(f"{args.id} remise en file.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sous = ap.add_subparsers(dest="commande", required=True)
    sous.add_parser("etat").set_defaults(fonction=cmd_etat)
    sous.add_parser("prochaine").set_defaults(fonction=cmd_prochaine)
    for nom, fn in (("executer", cmd_executer),):
        p = sous.add_parser(nom)
        p.add_argument("--id", default=None)
        p.add_argument("--timeout", type=int, default=5400)
        p.add_argument("--max-tentatives", type=int, default=2)
        p.set_defaults(fonction=fn)
    p = sous.add_parser("boucle")
    p.add_argument("--budget", type=int, default=6 * 3600, help="secondes d'agent par lancement de boucle")
    p.add_argument("--timeout", type=int, default=5400)
    p.add_argument("--max-tentatives", type=int, default=2)
    p.add_argument("--max-taches", type=int, default=0)
    p.set_defaults(fonction=cmd_boucle)
    sous.add_parser("stop").set_defaults(fonction=cmd_stop)
    p = sous.add_parser("reprendre")
    p.add_argument("id")
    p.set_defaults(fonction=cmd_reprendre)
    args = ap.parse_args()
    return args.fonction(args)


if __name__ == "__main__":
    sys.exit(main())

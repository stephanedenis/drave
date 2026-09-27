#!/usr/bin/env python3
"""Produit, pour chaque session DSH, un rapport qui reconstitue son essence et
démontre le travail accompli, étape par étape.

Sortie, à côté du digest brut :

  journal/sessions/<id>/rapport.md   la synthèse structurée de la session
  journal/README.md                  l'index des sessions

Ce que le rapport contient, et pourquoi :

  1. fiche      — identité, durée, volumes : de quoi situer la session
  2. demandes   — ce qui a été demandé, tour par tour, verbatim
  3. déroulé    — pour chaque tour : les actions (fichiers, commandes, délégations)
                  puis la synthèse produite. C'est la démonstration du travail.
  4. travail    — tables des fichiers créés/modifiés, des commandes, des sous-agents
  5. mesures    — les lignes de résultat qui portent un chiffre mesuré
  6. erreurs    — ce qui a échoué, et où
  7. commits    — ce qui a été inscrit dans l'histoire du dépôt

Usage :
  python3 tools/session_report.py [--repo DIR] [--session ID] [--quiet]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter, OrderedDict
from pathlib import Path

# Un résultat d'outil est tronqué avant d'entrer dans le rapport.
TRONC_SORTIE = 700
TRONC_DEMANDE = 700
TRONC_SYNTHESE = 2500

# Motifs de mesure : ce sont les lignes qui prouvent quelque chose.
# Une mesure, c'est un NOMBRE suivi d'une unité — pas une phrase qui contient
# le mot « gain ». Et on ne les cherche que dans les sorties de commandes.
MOTIFS_MESURE = re.compile(
    r"\d+(?:[.,]\d+)?\s*(?:tok/s|G\s*év|G\s*evt|G\s*ev|MHz|ALMs|M20K|DSP\b|"
    r"Go/s|Mo\b|Ko\b|%|ms\b)|"
    r"(?:perplexité|surcoût|résidu|rang|R²|×)\s*[:=]?\s*[-+]?\d+(?:[.,]\d+)?",
    re.I)
MOTIFS_ERREUR = re.compile(
    r"exit code: [1-9]|panicked at|^Error\b|^error\[|\bECHEC\b|\bÉCHEC\b|"
    r"DIVERGENT au rang|Error \([0-9]+\)|fatal error", re.M)


def decompresse(chemin: Path) -> str:
    if chemin.name.endswith(".zstd"):
        out = subprocess.run(["zstd", "-dc", str(chemin)], capture_output=True, check=False)
        if out.returncode != 0:
            raise RuntimeError(f"zstd: {out.stderr[:200]!r}")
        return out.stdout.decode("utf-8", "replace")
    return chemin.read_text(encoding="utf-8", errors="replace")


def txt(contenu) -> str:
    if isinstance(contenu, str):
        return contenu
    return "\n".join(b.get("text", "") for b in (contenu or [])
                     if isinstance(b, dict) and b.get("type") == "text")


def sans_titres(s: str) -> str:
    """Neutralise les titres markdown d'un texte inséré : sans cela les messages
    de l'assistant cassent la table des matières du rapport."""
    return "\n".join(("\\" + l) if l.lstrip().startswith("#") else l
                     for l in (s or "").splitlines())


def tronque(s: str, n: int) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[:n] + f"\n… [{len(s)-n} caractères tronqués]"


def charge(chemin: Path):
    """Rend la liste des enregistrements d'une session."""
    recs = []
    for ligne in decompresse(chemin).splitlines():
        if ligne.strip():
            try:
                recs.append(json.loads(ligne))
            except json.JSONDecodeError:
                pass
    return recs


def analyse(recs) -> dict:
    """Extrait tout ce qui servira au rapport."""
    d: dict = {
        "id": None, "cwd": None, "debut": None, "fin": None, "titre": None,
        "tours": [],                       # [(num, demande, actions, synthese)]
        "fichiers": OrderedDict(),         # chemin -> [n_ecritures, n_editions, dernière taille connue]
        "commandes": [], "sous_agents": [], "commits": [],
        "mesures": [], "erreurs": [], "compactages": 0, "objectifs": [],
        "outils_par_appel": {},
        "n_outils": 0, "n_messages": 0,
    }
    tour_courant = 0
    for r in recs:
        t = r.get("type")
        data = r.get("data") or {}
        ts = r.get("time")

        if t == "session":
            d["id"] = r.get("id"); d["cwd"] = r.get("cwd")
            d["debut"] = r.get("createdAt")
        if ts:
            d["fin"] = ts
        if t == "session/title":
            d["titre"] = data.get("title")
        elif t == "turn/start":
            tour_courant = data.get("turn", tour_courant + 1)
            d["tours"].append({"num": tour_courant, "demande": "", "synthese": "",
                               "actions": [], "outils": 0})
        elif t == "user/message":
            d["n_messages"] += 1
            corps = txt(data.get("content"))
            if d["tours"] and not d["tours"][-1]["demande"]:
                d["tours"][-1]["demande"] = corps
        elif t == "assistant/message":
            d["n_messages"] += 1
            corps = txt(data.get("message", {}).get("content"))
            if corps.strip() and d["tours"]:
                d["tours"][-1]["synthese"] = corps
        elif t == "tool/call":
            d["n_outils"] += 1
            nom = data.get("name", "?")
            if data.get("callId"):
                d["outils_par_appel"][data["callId"]] = nom
            try:
                args = json.loads(data.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            if d["tours"]:
                d["tours"][-1]["outils"] += 1
            if nom in ("write", "edit", "str_replace_editor"):
                f = args.get("file_path") or args.get("path") or "?"
                e = d["fichiers"].setdefault(f, {"ecritures": 0, "editions": 0})
                e["ecritures" if nom == "write" else "editions"] += 1
                if d["tours"]:
                    d["tours"][-1]["actions"].append(f"{nom} `{f}`")
            elif nom == "bash":
                cmd = (args.get("command") or "").strip().replace("\n", " ")
                d["commandes"].append((tour_courant, args.get("description", ""), cmd))
                if "git commit" in cmd:
                    d["commits"].append(cmd)
                if d["tours"]:
                    d["tours"][-1]["actions"].append(f"bash — {args.get('description','')}")
            elif nom in ("subagent", "subagent_fork"):
                desc = args.get("description", "?")
                d["sous_agents"].append((tour_courant, desc))
                if d["tours"]:
                    d["tours"][-1]["actions"].append(f"sous-agent — {desc}")
            elif d["tours"]:
                d["tours"][-1]["actions"].append(f"{nom}")
        elif t == "tool/result":
            msg = data.get("message", {})
            blocs, err = [], False
            for c in msg.get("content", []):
                if c.get("isError"):
                    err = True
                for cc in (c.get("content") or []):
                    if isinstance(cc, dict):
                        blocs.append(cc.get("text", ""))
            corps = "\n".join(blocs)
            origine = d["outils_par_appel"].get(msg.get("source", {}).get("callId"), "?")
            # seules les erreurs de COMMANDES comptent : une redirection web qui
            # échoue n'est pas un échec du travail
            if origine == "bash" and (err or MOTIFS_ERREUR.search(corps)):
                d["erreurs"].append((tour_courant, tronque(corps, 300)))
            # les mesures ne viennent que des commandes exécutées
            if origine == "bash":
                for ligne in corps.splitlines():
                    if MOTIFS_MESURE.search(ligne) and len(ligne.strip()) > 8:
                        d["mesures"].append((tour_courant, ligne.strip()[:200]))
        elif t == "goal/change":
            g = data.get("goal") or {}
            d["objectifs"].append((data.get("operation"), g.get("objective", "")))
        elif t == "compaction/summary":
            d["compactages"] += 1
    return d


def rapport(a: dict) -> str:
    L = []
    debut = a["debut"] / 1000 if a["debut"] else 0
    fin = a["fin"] / 1000 if a["fin"] else 0
    L += [f"# Session {str(a['id'])[:8]} — {a['titre'] or '(sans titre)'}", ""]
    L += ["| | |", "|---|---|",
          f"| Identifiant | `{a['id']}` |",
          f"| Dossier | `{a['cwd']}` |",
          f"| Début | {time.strftime('%Y-%m-%d %H:%M', time.localtime(debut))} |",
          f"| Durée | {(fin-debut)/3600:.1f} h |",
          f"| Tours | {len(a['tours'])} |",
          f"| Messages | {a['n_messages']} |",
          f"| Appels d'outils | {a['n_outils']} |",
          f"| Fichiers touchés | {len(a['fichiers'])} |",
          f"| Commandes | {len(a['commandes'])} |",
          f"| Sous-agents | {len(a['sous_agents'])} |",
          f"| Commits | {len(a['commits'])} |",
          f"| Compactages de contexte | {a['compactages']} |", ""]
    if a["objectifs"]:
        L += ["## Objectifs déclarés", ""]
        for op, obj in a["objectifs"]:
            L += [f"- **{op}** — {tronque(obj, 300)}"]
        L += [""]

    L += ["## 1. Ce qui a été demandé", ""]
    for t in a["tours"]:
        if t["demande"]:
            prem = tronque(t["demande"], 400).replace("\n", " ").lstrip("# ")
            L += [f"**Tour {t['num']}** — {prem}", ""]

    L += ["## 2. Déroulé, étape par étape", ""]
    for t in a["tours"]:
        if not (t["demande"] or t["actions"] or t["synthese"]):
            continue
        entete = tronque(t["demande"], 120).replace(chr(10), " ").lstrip("# ")
        L += [f"### Tour {t['num']} — {entete or '(suite)'}", ""]
        if t["actions"]:
            L += [f"*{t['outils']} appels d'outils.* Actions notables :", ""]
            vues, vus = [], set()
            for x in t["actions"]:
                cle = x.split("`")[0]
                if cle in vus and "`" not in x:
                    continue
                vus.add(cle); vues.append(x)
            for x in vues[:14]:
                L += [f"- {x}"]
            if len(vues) > 14:
                L += [f"- … et {len(vues)-14} autres"]
            L += [""]
        if t["synthese"]:
            L += ["**Synthèse produite :**", "",
                  sans_titres(tronque(t["synthese"], TRONC_SYNTHESE)), ""]

    L += ["## 3. Travail accompli", "", "### Fichiers créés ou modifiés", "",
          "| Fichier | Écritures | Éditions |", "|---|---|---|"]
    for f, e in a["fichiers"].items():
        L += [f"| `{f}` | {e['ecritures']} | {e['editions']} |"]
    L += [""]
    if a["sous_agents"]:
        L += ["### Sous-agents lancés", ""]
        for tour, desc in a["sous_agents"]:
            L += [f"- tour {tour} — {desc}"]
        L += [""]
    L += ["### Commandes exécutées (échantillon)", ""]
    for tour, desc, cmd in a["commandes"][:40]:
        L += [f"- **T{tour}** {desc or cmd[:80]}"]
    if len(a["commandes"]) > 40:
        L += [f"- … et {len(a['commandes'])-40} autres"]
    L += [""]

    if a["mesures"]:
        L += ["## 4. Mesures et résultats marquants", ""]
        vus = set()
        for tour, m in a["mesures"]:
            if m in vus:
                continue
            vus.add(m)
            L += [f"- **T{tour}** `{m}`"]
            if len(vus) >= 120:
                L += ["- … (tronqué)"]
                break
        L += [""]

    if a["erreurs"]:
        L += ["## 5. Erreurs rencontrées", "",
              f"{len(a['erreurs'])} sorties en erreur ou divergentes. Les premières :", ""]
        for tour, e in a["erreurs"][:15]:
            L += [f"- **T{tour}** : {e.replace(chr(10),' ')[:200]}"]
        L += [""]

    if a["commits"]:
        L += ["## 6. Commits", ""]
        for c in a["commits"]:
            m = re.search(r"-m\s+[\"'](.{0,160})", c)
            L += [f"- {m.group(1) if m else c[:160]}"]
        L += [""]
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--session", default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo)
    dsh = Path(os.environ.get("DSH_HOME", Path.home() / ".dsh"))
    slug = "--" + str(repo).strip("/").replace("/", "-") + "--"
    src = dsh / "sessions" / slug
    if not src.is_dir():
        print(f"aucune session pour {repo}", file=sys.stderr)
        return 1

    dest = repo / "journal" / "sessions"
    dest.mkdir(parents=True, exist_ok=True)
    index = ["# Journal des sessions", "",
             "Un rapport par session, régénéré automatiquement à chaque commit et",
             "chaque heure (`tools/session_report.py`). Le rapport reconstitue l'essence",
             "de la session ; le `digest.md` voisin en donne le verbatim complet.", "",
             "| Session | Titre | Début | Durée | Tours | Outils | Fichiers | Commits | Rapport |",
             "|---|---|---|---|---|---|---|---|---|"]
    for sess in sorted(src.iterdir()):
        if not sess.is_dir() or (args.session and not sess.name.startswith(args.session)):
            continue
        traces = sorted(sess.glob("session.jsonl*"))
        if not traces:
            continue
        a = analyse(charge(traces[0]))
        md = rapport(a)
        (dest / sess.name).mkdir(exist_ok=True)
        (dest / sess.name / "rapport.md").write_text(md, encoding="utf-8")
        debut = (a["debut"] or 0) / 1000
        duree = ((a["fin"] or 0) - (a["debut"] or 0)) / 3.6e6
        titre = tronque(a["titre"] or "—", 60).replace("|", "/")
        index.append(f"| `{sess.name[:8]}` | {titre} | "
                     f"{time.strftime('%Y-%m-%d %H:%M', time.localtime(debut))} | "
                     f"{duree:.1f} h | {len(a['tours'])} | {a['n_outils']} | "
                     f"{len(a['fichiers'])} | {len(a['commits'])} | "
                     f"[rapport](sessions/{sess.name}/rapport.md) |")
        if not args.quiet:
            print(f"  {sess.name[:8]} : rapport {len(md)/1024:.0f} Ko, "
                  f"{len(a['tours'])} tours, {len(a['fichiers'])} fichiers, "
                  f"{len(a['mesures'])} mesures, {len(a['erreurs'])} erreurs")
    (repo / "journal" / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Archive les sessions DSH de ce projet.

Trois sorties, dans `journal/sessions/` :

  <id>/digest.md          relecture lisible et *versionnable* de la session :
                          tours, messages, appels d'outils, résultats tronqués,
                          compactages et changements d'objectif. Régénéré à
                          chaque passage — donc idempotent, et le diff git ne
                          montre que ce qui est nouveau.
  <id>/session.jsonl.zstd copie brute de la trace DSH (ignorée par git : elle
                          est volumineuse et binaire, mais c'est la preuve exacte).
  MANIFEST.md             table des sessions : identifiant, date, volume,
                          empreinte, nombre d'événements.

Pourquoi journaliser : les traces d'une session contiennent le raisonnement, les
mesures et les erreurs — c'est-à-dire ce qui ne se reconstitue pas depuis le code.

Usage :
  python3 tools/archive_sessions.py [--repo DIR] [--quiet]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

TRONC_RESULTAT = 1200      # caractères conservés par résultat d'outil
TRONC_ARGUMENT = 300       # caractères conservés par appel d'outil


def decompresse(chemin: Path) -> str:
    """Rend le JSONL décompressé (zstd -dc, ou lecture directe)."""
    if chemin.suffix == ".zstd" or chemin.name.endswith(".zstd"):
        out = subprocess.run(["zstd", "-dc", str(chemin)],
                             capture_output=True, check=False)
        if out.returncode != 0:
            raise RuntimeError(f"zstd a échoué sur {chemin}: {out.stderr[:200]!r}")
        return out.stdout.decode("utf-8", "replace")
    return chemin.read_text(encoding="utf-8", errors="replace")


def texte_de(contenu) -> str:
    """Concatène les blocs `text` d'un contenu de message."""
    if isinstance(contenu, str):
        return contenu
    parts = []
    for bloc in contenu or []:
        if isinstance(bloc, dict) and bloc.get("type") == "text":
            parts.append(bloc.get("text", ""))
    return "\n".join(parts)


def tronque(s: str, n: int) -> str:
    s = s.strip()
    if len(s) <= n:
        return s
    return s[:n] + f"\n… [{len(s) - n} caractères tronqués]"


def digest(chemin: Path) -> tuple[str, dict]:
    """Construit le digest markdown d'une session, et ses statistiques."""
    lignes = ["# Session DSH — relecture", ""]
    stat = {"tours": 0, "messages": 0, "outils": 0, "erreurs": 0, "compactages": 0}
    tour = 0
    for brute in decompresse(chemin).splitlines():
        if not brute.strip():
            continue
        try:
            r = json.loads(brute)
        except json.JSONDecodeError:
            continue
        t = r.get("type")
        d = r.get("data") or {}

        if t == "session":
            # les champs de session sont à la racine de l'enregistrement
            lignes += [f"- identifiant : `{r.get('id')}`",
                       f"- dossier : `{r.get('cwd')}`",
                       f"- créée : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r.get('createdAt', 0) / 1000))}",
                       f"- agent : {r.get('agentPreset')}", ""]
        elif t == "turn/start":
            tour = d.get("turn", tour + 1)
            stat["tours"] += 1
            lignes += ["", f"## Tour {tour}", ""]
        elif t == "user/message":
            stat["messages"] += 1
            lignes += ["### 👤 Utilisateur", "", texte_de(d.get("content")), ""]
        elif t == "assistant/message":
            stat["messages"] += 1
            msg = d.get("message", {})
            txt = texte_de(msg.get("content"))
            if txt.strip():
                lignes += ["### 🤖 Assistant", "", txt, ""]
        elif t == "tool/call":
            stat["outils"] += 1
            args = tronque(str(d.get("arguments", "")), TRONC_ARGUMENT).replace("\n", " ")
            lignes += [f"- **{d.get('name')}** `{args}`"]
        elif t == "tool/result":
            msg = d.get("message", {})
            blocs = []
            for c in msg.get("content", []):
                for cc in (c.get("content") or []):
                    if isinstance(cc, dict):
                        blocs.append(cc.get("text", ""))
            corps = "\n".join(blocs)
            if msg.get("isError") or (msg.get("content") or [{}])[0].get("isError"):
                stat["erreurs"] += 1
            if corps.strip():
                lignes += ["", "  ```", tronque(corps, TRONC_RESULTAT), "  ```", ""]
        elif t == "goal/change":
            g = d.get("goal") or {}
            lignes += ["", f"> **Objectif** ({d.get('operation')}) : {g.get('objective', '')}", ""]
        elif t in ("compaction/summary", "compaction/start"):
            stat["compactages"] += 1
            if t == "compaction/summary":
                lignes += ["", "> **Compactage de contexte** — résumé conservé :", "",
                           "```", tronque(texte_de(d.get("summary")), 4000), "```", ""]
    return "\n".join(lignes) + "\n", stat


def empreinte(chemin: Path) -> str:
    h = hashlib.sha256()
    with chemin.open("rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()[:16]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo)
    dsh = Path(os.environ.get("DSH_HOME", Path.home() / ".dsh"))
    # le projet est identifié par le nom du dossier de sessions, dérivé du cwd
    slug = "--" + str(repo).strip("/").replace("/", "-") + "--"
    src = dsh / "sessions" / slug
    if not src.is_dir():
        print(f"aucune session DSH pour {repo} (cherché : {src})", file=sys.stderr)
        return 1

    dest = repo / "journal" / "sessions"
    dest.mkdir(parents=True, exist_ok=True)

    lignes_manifeste = [
        "# Sessions DSH archivées", "",
        "Régénéré par `tools/archive_sessions.py`. Le digest est versionnable ; la",
        "trace brute (`session.jsonl.zstd`) reste sur disque et n'est pas suivie par git.",
        "",
        "| Session | Début | Trace | Digest | Tours | Messages | Outils | Erreurs | Compactages |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    total = 0
    for sess in sorted(src.iterdir()):
        if not sess.is_dir():
            continue
        traces = sorted(sess.glob("session.jsonl*"))
        if not traces:
            continue
        trace = traces[0]
        cible = dest / sess.name
        cible.mkdir(exist_ok=True)
        # copie brute (rafraîchie à chaque passage)
        if trace.exists():
            shutil.copy2(trace, cible / trace.name)
        md, stat = digest(trace)
        (cible / "digest.md").write_text(md, encoding="utf-8")
        taille = trace.stat().st_size
        total += taille
        debut = time.strftime("%Y-%m-%d %H:%M", time.localtime(trace.stat().st_mtime))
        lignes_manifeste.append(
            f"| `{sess.name[:8]}` | {debut} | {taille/1e6:.1f} Mo | "
            f"{len(md)/1024:.0f} Ko | {stat['tours']} | {stat['messages']} | "
            f"{stat['outils']} | {stat['erreurs']} | {stat['compactages']} |")
        if not args.quiet:
            print(f"  {sess.name[:8]} : {taille/1e6:.1f} Mo de trace, "
                  f"digest {len(md)/1024:.0f} Ko, {stat['messages']} messages, "
                  f"{stat['outils']} outils")

    lignes_manifeste += ["", f"Total : {total/1e6:.1f} Mo de traces brutes.", ""]
    (dest / "MANIFEST.md").write_text("\n".join(lignes_manifeste), encoding="utf-8")
    if not args.quiet:
        print(f"manifeste écrit : {dest/'MANIFEST.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

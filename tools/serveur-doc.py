#!/usr/bin/env python3
"""serveur-doc.py — le serveur de documentation du dépôt : « où en est le travail ? », en HTML.

POURQUOI IL EXISTE. Le dépôt écrit beaucoup (`docs/`, `reports/`, `journal/`) et **lire vingt
fiches markdown dans un terminal n'est pas lire**. Ce serveur rend les documents en HTML — tableaux
compris — et fabrique une **page d'accueil qui répond à la question posée** : où en est le cerveau,
qu'est-ce qui a été mesuré, qu'est-ce qui est ouvert, et qu'est-ce qui tourne en ce moment.

CE QU'IL SERT :
  · `/`            la page d'état (carte des facultés, dernière passe, fiches récentes, questions
                   ouvertes, et le **journal du jour**) ;
  · `/<chemin>`    n'importe quel `.md` du dépôt, rendu (les liens relatifs fonctionnent) ;
  · le reste       servi tel quel (images, `.sh`, `.py`).

Usage :  python3 tools/serveur-doc.py [--port 8787] [--hote 0.0.0.0]
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import http.server
import pathlib
import re
import socketserver
import urllib.parse

import mistune

RACINE = pathlib.Path(__file__).resolve().parent.parent
MD = mistune.create_markdown(plugins=["table", "strikethrough", "task_lists", "url"])

STYLE = """
:root { --fond:#12141a; --carte:#1b1e26; --trait:#2c313d; --texte:#e6e8ee; --doux:#9aa3b2;
        --accent:#7cc4ff; --ok:#54d18c; --non:#ff7b72; --attention:#e3b341; }
* { box-sizing:border-box; }
body { margin:0; background:var(--fond); color:var(--texte);
       font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
a { color:var(--accent); text-decoration:none; } a:hover { text-decoration:underline; }
header { position:sticky; top:0; background:rgba(18,20,26,.94); backdrop-filter:blur(6px);
         border-bottom:1px solid var(--trait); padding:.6rem 1.2rem; display:flex; gap:1rem;
         align-items:baseline; flex-wrap:wrap; z-index:5; }
header b { font-size:1rem; } header span { color:var(--doux); font-size:.85rem; }
main { max-width:1180px; margin:0 auto; padding:1.2rem; }
h1 { font-size:1.5rem; margin:.4rem 0 .8rem; } h2 { font-size:1.2rem; margin:1.6rem 0 .6rem;
     border-bottom:1px solid var(--trait); padding-bottom:.3rem; }
h3 { font-size:1.02rem; margin:1.1rem 0 .4rem; }
table { border-collapse:collapse; width:100%; margin:.6rem 0 1rem; font-size:.92rem; }
th,td { border:1px solid var(--trait); padding:.35rem .55rem; text-align:left; vertical-align:top; }
th { background:#20242e; } tr:nth-child(even) td { background:#181b22; }
code { background:#22262f; padding:.1rem .3rem; border-radius:4px; font-size:.9em; }
pre { background:#15181f; border:1px solid var(--trait); border-radius:8px; padding:.8rem;
      overflow:auto; } pre code { background:none; padding:0; }
blockquote { border-left:3px solid var(--accent); margin:.6rem 0; padding:.2rem .9rem;
             color:var(--doux); background:#171a21; }
.grille { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:.8rem; }
.carte { background:var(--carte); border:1px solid var(--trait); border-radius:10px; padding:.8rem 1rem; }
.carte h3 { margin:0 0 .3rem; font-size:.98rem; } .carte p { margin:.2rem 0; color:var(--doux);
            font-size:.88rem; }
.etat { display:inline-block; padding:.05rem .45rem; border-radius:999px; font-size:.78rem;
        border:1px solid var(--trait); }
.ok { color:var(--ok); } .non { color:var(--non); } .att { color:var(--attention); }
footer { color:var(--doux); font-size:.82rem; padding:2rem 1.2rem; text-align:center; }
"""


def lier(chemin: pathlib.Path) -> str:
    """Chemin relatif à la racine, en URL."""
    return "/" + chemin.relative_to(RACINE).as_posix()


def rendre_page(titre: str, corps: str) -> bytes:
    maintenant = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    doc = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titre)} · Drave</title><style>{STYLE}</style></head><body>
<header><b><a href="/">Drave</a></b>
<a href="/docs/en-cours.md">en ce moment</a>
<a href="/docs/cerveau-facultes.md">carte des facultés</a>
<a href="/docs/etat-cerveau.md">état du cerveau</a>
<a href="/docs/references-non-regression.md">portes</a>
<a href="/reports/">fiches</a>
<a href="/journal/">journal</a>
<span style="margin-left:auto">généré à {maintenant}</span></header>
<main>{corps}</main>
<footer>serveur de documentation · <code>tools/serveur-doc.py</code> · dépôt Qtrinet</footer>
</body></html>"""
    return doc.encode("utf-8")


def fichier_du_jour() -> pathlib.Path | None:
    jour = dt.datetime.now().strftime("%Y-%m-%d")
    f = RACINE / "journal" / f"{jour}.md"
    return f if f.exists() else None


def page_accueil() -> bytes:
    """LA PAGE QUI RÉPOND À « OÙ EN EST LE TRAVAIL ? » — construite à partir du dépôt lui-même."""
    morceaux = ["<h1>Où en est le cerveau de Drave</h1>"]

    # 0. « EN CE MOMENT » — le fichier écrit à la main à chaque round, affiché EN PREMIER : c'est la
    #    question posée au serveur (« où en est le travail ? »), et elle mérite la première réponse.
    en_cours = RACINE / "docs" / "en-cours.md"
    if en_cours.exists():
        morceaux.append("<div class='carte' style='border-color:var(--accent)'>"
                        "<h3>⏵ En ce moment</h3></div>")
        morceaux.append(MD(en_cours.read_text()))

    # 1. les documents de tête
    tete = [("docs/cerveau-facultes.md", "La carte des facultés",
             "chaque faculté → le mécanisme le plus efficient → son coût → le verdict"),
            ("docs/etat-cerveau.md", "L'état du cerveau",
             "les douze capacités C1-C12, ce qui est fait, ce qui reste ouvert"),
            ("docs/references-non-regression.md", "Les portes",
             "ce qui est vérifié à chaque passe, et ce qui ne l'est pas")]
    morceaux.append("<h2>Les documents de tête</h2><div class='grille'>")
    for chemin, titre, quoi in tete:
        morceaux.append(f"<div class='carte'><h3><a href='/{chemin}'>{titre}</a></h3>"
                        f"<p>{quoi}</p></div>")
    morceaux.append("</div>")

    # 2. la dernière passe (extraite du fichier de référence : le premier bloc « Passe du »)
    ref = RACINE / "docs/references-non-regression.md"
    if ref.exists():
        texte = ref.read_text()
        m = re.search(r"> \*\*Passe du ([^`]*?)\*\*", texte)
        if m:
            lignes = []
            for l in texte.splitlines():
                if l.startswith("> ") and "Passe du" not in l and lignes:
                    lignes.append(l)
                elif l.startswith("> ") and "Passe du" in l:
                    lignes.append(l)
                elif lignes and not l.startswith(">"):
                    break
            bloc = "\n".join(x[2:] for x in lignes[:8])
            morceaux.append("<h2>La dernière passe de portes</h2>")
            morceaux.append(MD(bloc))

    # 3. les fiches les plus récentes (par date de modification)
    fiches = sorted((RACINE / "reports").glob("*.md"), key=lambda p: -p.stat().st_mtime)[:12]
    morceaux.append("<h2>Les fiches les plus récentes</h2><div class='grille'>")
    for f in fiches:
        quand = dt.datetime.fromtimestamp(f.stat().st_mtime).strftime("%d/%m %H:%M")
        titre = f.stem.replace("rapport-", "").replace("-", " ")
        morceaux.append(f"<div class='carte'><h3><a href='{lier(f)}'>{html.escape(titre)}</a></h3>"
                        f"<p>{quand} · {f.stat().st_size // 1024} ko</p></div>")
    morceaux.append("</div>")

    # 4. les outils de ce matin / de la nuit (derniers modifiés)
    outils = sorted([p for p in (RACINE / "tools").glob("*") if p.suffix in (".py", ".sh")],
                    key=lambda p: -p.stat().st_mtime)[:10]
    morceaux.append("<h2>Les outils les plus récents</h2><div class='grille'>")
    for f in outils:
        quand = dt.datetime.fromtimestamp(f.stat().st_mtime).strftime("%d/%m %H:%M")
        morceaux.append(f"<div class='carte'><h3><a href='{lier(f)}'>{f.name}</a></h3>"
                        f"<p>{quand}</p></div>")
    morceaux.append("</div>")

    # 5. le journal du jour
    j = fichier_du_jour()
    if j:
        morceaux.append(f"<h2>Le journal du jour — <a href='{lier(j)}'>{j.name}</a></h2>")
        txt = j.read_text()
        m = re.search(r"<!-- notes -->(.*?)<!-- /notes -->", txt, re.S)
        corps = (m.group(1) if m else txt)[:20000]
        morceaux.append(MD(corps))
    return rendre_page("où en est", "".join(morceaux))


class Serveur(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(RACINE), **k)

    def do_GET(self):                                    # noqa: N802
        chemin = urllib.parse.urlparse(self.path).path
        cible = (RACINE / chemin.lstrip("/")).resolve()
        if not str(cible).startswith(str(RACINE)):
            self.send_error(403)
            return
        if chemin in ("/", "/index.html"):
            corps = page_accueil()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            self.wfile.write(corps)
            return
        if cible.is_dir():
            fichiers = sorted(cible.glob("*.md"), key=lambda p: -p.stat().st_mtime)
            if fichiers and cible.name != "docs":
                liens = "".join(
                    f"<div class='carte'><h3><a href='{lier(f)}'>{html.escape(f.stem)}</a></h3>"
                    f"<p>{dt.datetime.fromtimestamp(f.stat().st_mtime):%d/%m %H:%M}</p></div>"
                    for f in fichiers)
                corps = rendre_page(cible.name, f"<h1>{cible.name}/</h1><div class='grille'>{liens}</div>")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(corps)))
                self.end_headers()
                self.wfile.write(corps)
                return
        if cible.suffix == ".md" and cible.exists():
            corps = rendre_page(cible.stem, MD(cible.read_text()))
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            self.wfile.write(corps)
            return
        return super().do_GET()

    def log_message(self, fmt, *args):                    # silencieux hors erreurs
        if args and str(args[1]).startswith(("4", "5")):
            super().log_message(fmt, *args)


class Reutilisable(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--hote", default="0.0.0.0")
    a = ap.parse_args()
    with Reutilisable((a.hote, a.port), Serveur) as httpd:
        print(f"serveur de documentation : http://localhost:{a.port}/  (racine {RACINE})")
        httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

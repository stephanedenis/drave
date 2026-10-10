#!/usr/bin/env python3
"""journal_auto.py — le journal quotidien, ÉCRIT PAR JOUR ET PAR THÈME, à partir de git et des sessions.

POURQUOI. Le journal doit consigner les **événements datés** (voir
`docs/organisation-du-depot.md`), et une journée de ce dépôt est trop riche pour un seul
fichier : un jour touche le moteur, les protocoles, les mesures, les portes et la
documentation. D'où le découpage **`<AAAA-MM-JJ>_<thème>.md`** : on lit la journée d'un thème,
et on suit un thème **d'un jour à l'autre** (le nom commence par la date, le thème suit —
`ls journal/2026-10-1*_attention.md`).

SOURCES, et rien d'autre :
  1. **git** — les commits du jour (heure d'auteur, en heure locale de la machine) et les
     fichiers touchés ; c'est la chronologie **fiable** (les horodatages écrits à la main
     s'étaient retrouvés dans le futur) ;
  2. **journal/sessions/** — les rapports de session dont la fenêtre de temps couvre le jour
     (début et durée lus dans l'index `journal/README.md`, régénéré par
     `tools/session_report.py`) : on en extrait les **titres de tour** classés par thème, avec
     le lien vers le rapport complet.

CE QUI EST PRÉSERVÉ. Tout ce que l'humain (ou l'agent) écrit à la main **entre les marqueurs**
`<!-- notes -->` et `<!-- /notes -->` est conservé tel quel d'une génération à l'autre. Le
reste du fichier est régénéré : ne pas écrire en dehors des marqueurs.

Usage :
  tools/journal_auto.py                     # aujourd'hui
  tools/journal_auto.py --jour 2026-10-09   # un jour
  tools/journal_auto.py --depuis 2026-10-08 # chaque jour depuis cette date
  tools/journal_auto.py --lister            # les thèmes connus et leurs mots-clés
  tools/journal_auto.py --dry-run           # montre sans écrire
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "journal"
NOTES_DEB, NOTES_FIN = "<!-- notes -->", "<!-- /notes -->"

# --- les thèmes ---------------------------------------------------------------------------
# L'ordre COMPTE : le premier motif qui matche gagne (le plus spécifique d'abord). Chaque thème
# a ses mots-clés (sujet du commit) et ses chemins (fichiers touchés).
THEMES: list[tuple[str, str, list[str], list[str]]] = [
    ("attention", "Attention, fenêtre, puits", 
     ["attention", "fenêtre", "fenetre", "puits", "sinks", "attn-", "softmax", "swa", "kv"],
     ["model.rs"]),
    ("memoire", "Mémoire épisodique, consolidation, greffe",
     ["mémoire", "memoire", "épisodique", "episodique", "greffe", "consolid", "rappel", "indice",
      "magasin", "c6", "c7", "clé", "cle"],
     ["episodique.rs"]),
    ("distribue", "Régions, flux, protocoles, budgets, pannes",
     ["topologie", "région", "region", "nœud", "noeud", "flux", "bus", "latence", "budget",
      "panne", "registre", "trace", "protocole", "v7", "v8", "paires", "message", "gigue",
      "réparti", "reparti", "relais", "découpage", "decoupage", "lien"],
     ["topologie.rs", "trace_globale.rs", "bus.rs", "flux.rs"]),
    ("modele", "Modèles, entraînement, parcimonie, biologie",
     ["modèle", "modele", "entraîn", "entrain", "distill", "parcimonie", "poids", "échelle",
      "echelle", "biolog", "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "log-normal"],
     ["entrainer_moteur.py", "biologie"]),
    ("moteur", "Moteur : chargement, calcul, listes, quantification",
     ["moteur", "gguf", "listes", "quantif", "noyau", "gpu", "threads", "mmap", "lots",
      "profil", "débit", "debit"],
     ["gguf.rs", "model.rs", "main.rs"]),
    ("mesures", "Campagnes et mesures",
     ["campagne", "mesure", "perplexité", "perplexite", "carte", "banc", "benchmark", "aiguille"],
     ["reports/"]),
    ("portes", "Portes et vérifications",
     ["porte", "portes", "vérification", "verification", "tests", "gate"],
     ["tools/porte-", "toutes-les-portes"]),
    ("docs", "Documentation, état, conventions",
     ["document", "doc", "readme", "glossaire", "rangement", "convention", "état", "etat",
      "journal", "organisation", "manques"],
     ["docs/", "README.md"]),
    ("outils", "Outils et harnais",
     ["outil", "script", "harnais", "hook", "générateur", "generateur"],
     ["tools/"]),
]
THEME_DEFAUT = ("divers", "Ce qui ne rentre dans aucun thème")


def theme_de(sujet: str, fichiers: list[str]) -> str:
    s = sujet.lower()
    for slug, _, mots, chemins in THEMES:
        if any(m in s for m in mots):
            return slug
    for slug, _, _, chemins in THEMES:
        if any(c in f for f in fichiers for c in chemins):
            return slug
    return THEME_DEFAUT[0]


def titre_theme(slug: str) -> str:
    for s, titre, _, _ in THEMES:
        if s == slug:
            return titre
    return THEME_DEFAUT[1]


def git_commits(jour: str) -> list[dict]:
    """Les commits du jour : heure locale, hash, sujet, fichiers.

    Lecture LIGNE À LIGNE, et pas par découpage sur le séparateur : `--format=…@@@` place le
    séparateur APRÈS l'en-tête du commit, donc le premier bloc d'un découpage ne contient
    qu'un en-tête et tous les suivants commencent par des noms de fichiers — le premier essai
    de ce script n'a ainsi trouvé **1** commit sur 56. C'est la même famille d'erreur que le
    harnais qui comptait les jetons annoncés au lieu de les compter.
    """
    out = subprocess.run(
        ["git", "log", f"--since={jour} 00:00:00", f"--until={jour} 23:59:59",
         "--format=%h|%ad|%s", "--date=format:%H:%M", "--name-only"],
        cwd=RACINE, capture_output=True, text=True).stdout
    commits: list[dict] = []
    for ligne in out.splitlines():
        if not ligne.strip():
            continue
        tete = ligne.split("|", 2)
        if len(tete) == 3 and re.fullmatch(r"[0-9a-f]{7,40}", tete[0]) and re.match(r"^\d{2}:\d{2}$", tete[1]):
            commits.append({"hash": tete[0], "heure": tete[1], "sujet": tete[2], "fichiers": []})
        elif commits:
            commits[-1]["fichiers"].append(ligne.strip())
    return commits


def sessions_du_jour(jour: str) -> list[dict]:
    """Les sessions dont la fenêtre [début, début+durée] couvre le jour (index journal/README.md)."""
    idx = JOURNAL / "README.md"
    if not idx.exists():
        return []
    trouvees = []
    for l in idx.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*`([0-9a-f]{8})`\s*\|\s*(.*?)\s*\|\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*\|"
                     r"\s*([\d.]+) h\s*\|", l)
        if not m:
            continue
        sid, titre, debut, duree = m.group(1), m.group(2), m.group(3), float(m.group(4))
        t0 = time.mktime(time.strptime(debut, "%Y-%m-%d %H:%M"))
        t1 = t0 + duree * 3600
        # INTERSECTION de la fenêtre de session avec la JOURNÉE, et non « midi dedans » : une
        # session de 49 h qui finit à 10 h 23 couvre bien le 10 octobre, mais pas midi — le
        # premier essai comptait donc 0 session pour la journée en cours.
        j0 = time.mktime(time.strptime(jour + " 00:00", "%Y-%m-%d %H:%M"))
        j1 = j0 + 86400
        if t0 < j1 and t1 > j0:
            trouvees.append({"id": sid, "titre": titre, "debut": debut, "duree": duree})
    return trouvees


def etapes_du_jour(sid: str) -> list[tuple[str, str]]:
    """Les ÉTAPES du jour, telles que les a consignées le journal de session.

    Chaque tour du rapport contient la « synthèse produite » — les lignes que l'agent écrit
    pour dire CE QU'IL FAIT (`⏵ …`). C'est la matière la plus utile du journal : le titre du
    tour dit la demande, ces lignes disent le travail. On les renvoie (texte, titre du tour),
    dédoublonnées, dans l'ordre.
    """
    for d in (JOURNAL / "sessions").glob(f"{sid}-*"):
        r = d / "rapport.md"
        if not r.exists():
            continue
        etapes, tour, vues = [], "", set()
        for l in r.read_text(encoding="utf-8", errors="replace").splitlines():
            if l.startswith("### Tour "):
                tour = l[4:].strip()
                tour = tour if len(tour) <= 90 else tour[:87].rstrip() + "…"
            elif l.startswith("⏵ "):
                t = l[2:].strip()
                cle = t.lower()
                if t and cle not in vues:
                    vues.add(cle)
                    etapes.append((t, tour))
        return etapes
    return []


def tours_de_session(sid: str) -> list[str]:
    """Les titres de tour du rapport de session (le détail reste dans le rapport)."""
    for d in (JOURNAL / "sessions").glob(f"{sid}-*"):
        r = d / "rapport.md"
        if not r.exists():
            continue
        titres = []
        for l in r.read_text(encoding="utf-8", errors="replace").splitlines():
            if l.startswith("### Tour "):
                t = l[4:].strip().replace("|", "/")
                # les tours portent la première ligne du message : on la borne, sinon le
                # journal recopie la conversation au lieu de la résumer
                titres.append(t if len(t) <= 120 else t[:117].rstrip() + "…")
        return titres
    return []


# Ce qu'on reconnaît comme un CHIFFRE qui compte : un pourcentage, un facteur, une durée, un
# volume, un compte de jetons ou de paires, une perplexité. Extrait des textes DÉJÀ fiables
# (sujets de commit, étapes du journal de session) — PAS de la section « mesures » des rapports
# de session, qui mélange des extraits de diff et des digests (essayé, illisible).
MOTIFS_CHIFFRES = [
    r"[-−+]?\d+(?:[.,]\d+)?\s*%",
    r"[÷×]\s*\d+(?:[.,]\d+)?",
    r"\d+(?:[.,]\d+)?\s*(?:ms|µs|ns|s)\b",
    r"\d+(?:[.,]\d+)?\s*(?:Go|Mo|Ko|Gio|Mio|Kio|Go/s|Mo/s)\b",
    r"\d+(?:[.,]\d+)?\s*(?:jetons?|paires?|messages?|fibres?|couches?|états?|tours?)\b",
    r"\d+(?:[.,]\d+)?\s*tok/s",
    r"\d{2,}(?:[.,]\d+)?\s*(?:M|G)?\s*par (?:jeton|pas|token)",
    # les perplexités, écrites « 29.0206 », « 1297,5437 », « perplexité 15,4339 »
    r"(?:perplexité|ppl)\s*[:=]?\s*\d+(?:[.,]\d+)?",
    r"\b\d{1,4}[.,]\d{3,4}\b",
]


def chiffres_du_jour(textes: list[str], plafond: int = 12) -> list[str]:
    """Les chiffres qui reviennent dans les textes du jour, dans l'ordre d'apparition."""
    vus, sortis = set(), []
    for t in textes:
        # « 2 048 jetons » : l'espace est un séparateur de milliers FRANÇAIS ; sans ce collage,
        # l'extraction sortait « 048 jetons » (un chiffre tronqué, donc faux).
        t = re.sub(r"(\d)\s(\d{3})\b", r"\1\2", t)
        for motif in MOTIFS_CHIFFRES:
            for m in re.finditer(motif, t):
                c = m.group(0).strip()
                if c not in vus:
                    vus.add(c)
                    sortis.append(c)
                    if len(sortis) >= plafond:
                        return sortis
    return sortis


def lire_notes(chemin: Path, defaut: str = "") -> str:
    if not chemin.exists():
        return defaut
    t = chemin.read_text(encoding="utf-8")
    if NOTES_DEB in t and NOTES_FIN in t:
        return t.split(NOTES_DEB, 1)[1].split(NOTES_FIN, 1)[0].strip("\n")
    # fichier écrit AVANT cette convention : son contenu devient les notes (rien n'est perdu)
    lignes = [l for l in t.splitlines() if not l.startswith("# ")]
    return "\n".join(lignes).strip("\n")


def ecrire(chemin: Path, contenu: str, dry: bool, journal: list[str]) -> None:
    journal.append(f"  {'(sec) ' if dry else ''}{chemin.relative_to(RACINE)}")
    if not dry:
        chemin.write_text(contenu, encoding="utf-8")


def generer_jour(jour: str, dry: bool, trace: list[str], themes_ecrits: list | None = None) -> int:
    commits = git_commits(jour)
    sessions = sessions_du_jour(jour)
    par_theme: dict[str, list[dict]] = {}
    for c in commits:
        par_theme.setdefault(theme_de(c["sujet"], c["fichiers"]), []).append(c)
    # les tours de session, classés par thème (par mots-clés du titre)
    tours: dict[str, list[tuple[str, str]]] = {}
    etapes: dict[str, list[str]] = {}
    for s in sessions:
        for t in tours_de_session(s["id"]):
            tours.setdefault(theme_de(t, []), []).append((s["id"], t))
        for texte, tour in etapes_du_jour(s["id"]):
            # les étapes sont classées comme les commits : par mots-clés de leur propre texte
            etapes.setdefault(theme_de(texte + " " + tour, []), []).append(texte)

    themes = sorted(set(par_theme) | set(tours))
    fichiers_theme = []
    for th in themes:
        cs = par_theme.get(th, [])
        lignes = [
            f"# {jour} — {titre_theme(th)}", "",
            "> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).",
            "> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.",
            "> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : "
            f"[{jour}.md]({jour}.md). Convention : `docs/organisation-du-depot.md`.", "",
            f"## Commits du jour ({len(cs)})", "",
        ]
        if cs:
            lignes += ["| heure | commit | fait | fichiers |", "|---|---|---|---|"]
            for c in sorted(cs, key=lambda c: c["heure"]):
                n = len(c["fichiers"])
                apercu = ", ".join(f"`{f.split('/')[-1]}`" for f in c["fichiers"][:3])
                if n > 3:
                    apercu += f" (+{n - 3})"
                lignes.append(f"| {c['heure']} | `{c['hash']}` | {c['sujet']} | {apercu} |")
        else:
            lignes.append("*(aucun commit classé dans ce thème)*")
        lignes.append("")
        chiffres = chiffres_du_jour([c["sujet"] for c in cs] + etapes.get(th, []))
        if chiffres:
            lignes += ["## Chiffres du jour", "", " · ".join(f"`{c}`" for c in chiffres), "",
                       "*Extraits des sujets de commit et des étapes — le détail et les "
                       "conditions sont dans la fiche correspondante de `reports/`.*", ""]
        if etapes.get(th):
            plafond = 25
            lignes += [f"## Étapes du jour ({len(etapes[th])})", "",
                       "*Ce que l'agent a consigné en le faisant (lignes `⏵` du journal de "
                       "session) :*", ""]
            for e in etapes[th][:plafond]:
                lignes.append(f"- {e}")
            reste = len(etapes[th]) - plafond
            if reste > 0:
                lignes.append(f"- *(+{reste} autres étapes — voir les rapports de session)*")
            lignes.append("")
        if tours.get(th):
            plafond = 20
            lignes += ["## Sessions (titres de tour)", ""]
            for sid, t in tours[th][:plafond]:
                lignes.append(f"- `{sid}` — {t} → "
                              f"[rapport complet](sessions/{sid}/rapport.md)")
            reste = len(tours[th]) - plafond
            if reste > 0:
                lignes.append(f"- *(+{reste} autres tours — le détail est dans le rapport de "
                              f"session)*")
            lignes.append("")
        if sessions:
            lignes += ["## Sessions actives ce jour", ""]
            for s in sessions:
                lignes.append(f"- `{s['id']}` — {s['titre']} (début {s['debut']}, "
                              f"{s['duree']:.1f} h) → "
                              f"[rapport](sessions/{s['id']}/rapport.md) · "
                              f"[digest](sessions/{s['id']}/digest.md)")
            lignes.append("")
        # les fiches de reports touchées ce jour-là : le lien vers la MESURE
        fiches = sorted({f for c in cs for f in c["fichiers"]
                         if f.startswith("reports/") and f.endswith(".md")})
        if fiches:
            lignes += ["## Mesures et rapports touchés", ""]
            lignes += [f"- [{f}](../{f})" for f in fiches] + [""]
        nom = JOURNAL / f"{jour}_{th}.md"
        notes = lire_notes(nom)
        lignes += [NOTES_DEB, notes, NOTES_FIN, ""]
        ecrire(nom, "\n".join(lignes), dry, trace)
        fichiers_theme.append((th, len(cs), f"{jour}_{th}.md"))

    # l'index du jour
    lignes = [
        f"# {jour}", "",
        "> **Généré** par `tools/journal_auto.py` — index de la journée, découpée par **thème**",
        "> (une journée de ce dépôt ne tient pas dans un fichier). Le récit écrit à la main est",
        "> conservé plus bas, dans le bloc « notes » (marqueurs HTML).", "",
        f"**{len(commits)} commits** · **{len(sessions)} session(s)** · "
        f"**{len(themes)} thème(s)**", "",
        "## Thèmes du jour", "", "| thème | commits | fichier |", "|---|---|---|",
    ]
    for th, n, nom in fichiers_theme:
        lignes.append(f"| {th} | {n} | [{nom}]({nom}) |")
    lignes.append("")
    if sessions:
        lignes += ["## Sessions du jour", "",
                   "| session | titre | début | durée | liens |", "|---|---|---|---|---|"]
        for s_ in sessions:
            lignes.append(f"| `{s_['id']}` | {s_['titre']} | {s_['debut']} | "
                          f"{s_['duree']:.1f} h | [rapport](sessions/{s_['id']}/rapport.md) · "
                          f"[digest](sessions/{s_['id']}/digest.md) |")
        lignes.append("")
    if commits:
        lignes += ["## Tous les commits (heure réelle)", "", "| heure | commit | fait |",
                   "|---|---|---|"]
        for c in sorted(commits, key=lambda c: c["heure"]):
            lignes.append(f"| {c['heure']} | `{c['hash']}` | {c['sujet']} |")
        lignes.append("")
    # la TABLE DES THÈMES, écrite à côté : c'est la règle de classement, elle doit être lisible
    # (et modifiable) sans lire le script
    table = ["# Thèmes du journal", "",
             "> Généré par `tools/journal_auto.py` — c'est la **règle de classement** des fichiers",
             "> `journal/AAAA-MM-JJ_<thème>.md`. Un commit (ou une étape de session) est classé par",
             "> le **premier** thème dont un mot-clé apparaît dans son texte ; à défaut, par les",
             "> **chemins** touchés ; à défaut, en `divers`. Pour changer le classement, éditer la",
             "> table `THEMES` du script et relancer : rien d'autre n'est à toucher.", "",
             "| thème | ce qu'il couvre | mots-clés | chemins |", "|---|---|---|---|"]
    for slug, titre, mots, chemins in THEMES:
        table.append(f"| `{slug}` | {titre} | {', '.join(mots)} | {', '.join(chemins)} |")
    table += [f"| `{THEME_DEFAUT[0]}` | {THEME_DEFAUT[1]} | — | — |", ""]
    if themes_ecrits is not None and "themes" not in themes_ecrits:
        themes_ecrits.append("themes")
        ecrire(JOURNAL / "THEMES.md", "\n".join(table), dry, trace)
    notes = lire_notes(JOURNAL / f"{jour}.md")
    lignes += ["## Le récit de la journée (écrit à la main)", "", NOTES_DEB, notes, NOTES_FIN, ""]
    ecrire(JOURNAL / f"{jour}.md", "\n".join(lignes), dry, trace)
    return len(commits)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jour", help="AAAA-MM-JJ (défaut : aujourd'hui)")
    ap.add_argument("--depuis", help="générer chaque jour depuis cette date")
    ap.add_argument("--lister", action="store_true", help="montrer les thèmes et leurs mots-clés")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    if a.lister:
        for slug, titre, mots, chemins in THEMES:
            print(f"{slug:<10} {titre}\n           mots-clés : {', '.join(mots[:8])}…"
                  f"\n           chemins   : {', '.join(chemins)}")
        print(f"{THEME_DEFAUT[0]:<10} {THEME_DEFAUT[1]}")
        return 0

    if a.depuis:
        j0 = time.mktime(time.strptime(a.depuis, "%Y-%m-%d"))
        jours = [time.strftime("%Y-%m-%d", time.localtime(j0 + 86400 * i))
                 for i in range(int((time.time() - j0) // 86400) + 1)]
    else:
        jours = [a.jour or time.strftime("%Y-%m-%d")]

    trace: list[str] = []
    total = 0
    themes_ecrits: list = []
    for j in jours:
        n = generer_jour(j, a.dry_run, trace, themes_ecrits)
        total += n
        if not a.quiet:
            print(f"{j} : {n} commits")
    if not a.quiet:
        print("\n".join(trace))
        print(f"{len(trace)} fichiers {'(simulation)' if a.dry_run else 'écrits'} · "
              f"{total} commits classés")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

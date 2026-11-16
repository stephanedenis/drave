#!/usr/bin/env python3
"""verifie_exemples.py — le contrôle négatif des exemples de la doc produit.

Ce script rejoue les sorties publiées dans `docs/produit/exemples.md` et
`docs/produit/demarrage.md` avec le code courant, puis compare :

  - le JSON **parsé** (pas le texte) pour les blocs `--json` ;
  - le texte exact pour les sorties lisibles ;
  - le couple `stdout`/`stderr` et le code de sortie pour le refus ;
  - les **syntagmes** des blocs `--tagger` à l'heuristique (le tagger ne change que le POS) ;
  - les trois commandes du démarrage dans une copie **sans** `tools/structures`, condition du
    clone public.

La durée (`cout.duree_s`) est la seule valeur non reproductible : le script vérifie sa présence
et son type, jamais son nombre. Le mode `--mutation` casse volontairement une valeur attendue et
exige que le script la détecte : c'est le contrôle négatif du contrôle.

    python3 tools/verifie_exemples.py
    python3 tools/verifie_exemples.py --json
    python3 tools/verifie_exemples.py --mutation
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
DOCS = RACINE / "docs" / "produit"
EXEMPLES = DOCS / "exemples.md"
DEMARRAGE = DOCS / "demarrage.md"

try:  # paquet : `python3 -m tools.verifie_exemples`
    from .roles_vocabulaire import ROLES
except ImportError:  # script : `python3 tools/verifie_exemples.py`
    from roles_vocabulaire import ROLES


# --------------------------------------------------------------------------- lecture markdown


class Bloc:
    def __init__(self, lang: str, debut: int, fin: int, corps: str) -> None:
        self.lang = lang
        self.debut = debut          # position du début de la clôture ```lang
        self.fin = fin              # position de la fin de la clôture ```
        self.corps = corps


class Section:
    def __init__(self, titre: str, debut: int, fin: int, blocs: list[Bloc]) -> None:
        self.titre = titre
        self.debut = debut
        self.fin = fin
        self.blocs = blocs


def lire_sections(texte: str) -> list[Section]:
    """Découpe le markdown par titres `##` et associe les blocs de code à leur section."""
    tetes = [(m.start(), m.group(0)) for m in re.finditer(r"^#{2,3} .+$", texte, re.M)]
    sections: list[Section] = []
    for i, (debut, titre) in enumerate(tetes):
        fin = tetes[i + 1][0] if i + 1 < len(tetes) else len(texte)
        blocs = [
            Bloc(m.group(1) or "text", m.start(), m.end(), m.group(2))
            for m in re.finditer(r"^```(\w*)\n(.*?)\n```$", texte[debut:fin], re.M | re.S)
        ]
        # les positions des blocs sont relatives à la section : on les rend absolues
        for b in blocs:
            b.debut += debut
            b.fin += debut
        sections.append(Section(titre, debut, fin, blocs))
    return sections


def section(sections: list[Section], prefixe: str) -> Section:
    for s in sections:
        if s.titre.startswith(prefixe):
            return s
    raise LookupError(f"section introuvable : {prefixe!r}")


def bloc_bash(s: Section, contient: str, exclut: str | None = None) -> Bloc:
    for b in s.blocs:
        if b.lang == "bash" and contient in b.corps and (exclut is None or exclut not in b.corps):
            return b
    raise LookupError(f"commande {contient!r} introuvable dans {s.titre!r}")


def bloc_apres(s: Section, ancre: Bloc, lang: str) -> Bloc:
    for b in s.blocs:
        if b.lang == lang and b.debut > ancre.debut:
            return b
    raise LookupError(f"bloc {lang!r} après la commande introuvable dans {s.titre!r}")


def bloc_lang(s: Section, lang: str, rang: int = 0) -> Bloc:
    trouves = [b for b in s.blocs if b.lang == lang]
    if rang >= len(trouves):
        raise LookupError(f"bloc {lang!r} #{rang} introuvable dans {s.titre!r}")
    return trouves[rang]


# --------------------------------------------------------------------------- exécution


def executer(commande: str, cwd: pathlib.Path) -> subprocess.CompletedProcess:
    return subprocess.run(commande, shell=True, cwd=str(cwd), text=True,
                          capture_output=True, executable="/bin/bash")


def normaliser_texte(texte: str) -> str:
    return "\n".join(ligne.rstrip() for ligne in texte.replace("\r\n", "\n").split("\n")).strip()


def comparer_json(attendu, obtenu, chemin: str = "") -> list[str]:
    """Les écarts entre deux structures JSON ; `duree_s` est le seul champ toléré."""
    ecarts: list[str] = []
    if chemin.endswith("duree_s"):
        if not isinstance(obtenu, (int, float)) or obtenu < 0:
            ecarts.append(f"{chemin}: nombre >= 0 attendu, reçu {obtenu!r}")
        return ecarts
    if type(attendu) is not type(obtenu) and not (
            isinstance(attendu, (int, float)) and isinstance(obtenu, (int, float))):
        return [f"{chemin or '<racine>'}: type {type(attendu).__name__} attendu, "
                f"{type(obtenu).__name__} reçu"]
    if isinstance(attendu, dict):
        for cle in sorted(set(attendu) | set(obtenu)):
            if cle not in attendu:
                ecarts.append(f"{chemin}.{cle}: champ inattendu")
            elif cle not in obtenu:
                ecarts.append(f"{chemin}.{cle}: champ manquant")
            else:
                ecarts.extend(comparer_json(attendu[cle], obtenu[cle], f"{chemin}.{cle}"))
        return ecarts
    if isinstance(attendu, list):
        if len(attendu) != len(obtenu):
            ecarts.append(f"{chemin}: {len(attendu)} éléments attendus, {len(obtenu)} reçus")
        for i, (a, o) in enumerate(zip(attendu, obtenu)):
            ecarts.extend(comparer_json(a, o, f"{chemin}[{i}]"))
        return ecarts
    if attendu != obtenu:
        ecarts.append(f"{chemin}: {attendu!r} attendu, {obtenu!r} reçu")
    return ecarts


# --------------------------------------------------------------------------- cas


class Cas:
    def __init__(self, ident: str, doc: str, commande: str, attendu: str, genre: str,
                 cwd: pathlib.Path = RACINE, detail: str = "") -> None:
        self.ident = ident
        self.doc = doc
        self.commande = commande
        self.attendu = attendu
        self.genre = genre
        self.cwd = cwd
        self.detail = detail


def cas_exemples(texte: str) -> list[Cas]:
    sections = lire_sections(texte)
    cas: list[Cas] = []

    # § 1 — la sortie lisible
    s = section(sections, "## 1. Une déclarative simple")
    cmd = bloc_bash(s, "analyser \"Le chat dort.\"", exclut="--json")
    cas.append(Cas("exemples §1 lisible", "exemples.md", cmd.corps,
                   bloc_lang(s, "text").corps, "texte"))

    # § 1 — le JSON (candidats objets)
    cmd = bloc_bash(s, "--json", exclut="--duree")
    cas.append(Cas("exemples §1 JSON", "exemples.md", cmd.corps,
                   bloc_apres(s, cmd, "json").corps, "json"))

    # § 1 — la durée : valeur variable, présence et type contrôlés
    cmd = bloc_bash(s, "--duree")
    cas.append(Cas("exemples §1 durée", "exemples.md", cmd.corps,
                   bloc_apres(s, cmd, "json").corps, "json_duree",
                   detail="duree_s variable : présence et type seulement"))

    # § 2 — l'union
    s = section(sections, "## 2. Un attachement de REL")
    cmd = bloc_bash(s, "--json")
    cas.append(Cas("exemples §2 JSON", "exemples.md", cmd.corps,
                   bloc_apres(s, cmd, "json").corps, "json"))

    # § 3 — l'anglais
    s = section(sections, "## 3. L'anglais et le marqueur ambigu")
    cmd = bloc_bash(s, "--json")
    cas.append(Cas("exemples §3 JSON", "exemples.md", cmd.corps,
                   bloc_apres(s, cmd, "json").corps, "json"))

    # § 4 — le refus (CLI) : stderr + code 3
    s = section(sections, "## 4. Le refus")
    cmd = bloc_bash(s, "analyser \"\"")
    cas.append(Cas("exemples §4 refus CLI", "exemples.md", cmd.corps,
                   bloc_lang(s, "text").corps, "refus"))

    # § 4 — le refus (API)
    cmd = bloc_bash(s, "bloc_linguistique.py")
    cas.append(Cas("exemples §4 refus API", "exemples.md", cmd.corps,
                   bloc_apres(s, cmd, "json").corps, "json"))

    # § 5 — r035
    s = section(sections, "## 5. L'échec autrefois connu")
    cmd = bloc_bash(s, "--json")
    cas.append(Cas("exemples §5 JSON", "exemples.md", cmd.corps,
                   bloc_apres(s, cmd, "json").corps, "json"))

    # § 6 — les syntagmes du tagger sont ceux de l'heuristique (le tagger ne change que le POS)
    for prefixe, ident, texte_entree in (
        ("### 6.1", "exemples §6.1 syntagmes", "Le chat dort."),
        ("### 6.2", "exemples §6.2 syntagmes", "Le livre que j'ai lu est intéressant."),
        ("### 6.3", "exemples §6.3 syntagmes", "The day when we left was beautiful."),
    ):
        sec = section(sections, prefixe)
        attendu = bloc_lang(sec, "text").corps
        commande = (f"python3 tools/drave.py analyser {json.dumps(texte_entree, ensure_ascii=False)}"
                    + (" --langue en" if prefixe == "### 6.3" else ""))
        cas.append(Cas(ident, "exemples.md", commande, attendu, "syntagmes",
                       detail="le tagger ne change que le POS"))

    # § 7.1 — la sortie lisible de --reel
    s = section(sections, "### 7.1")
    cmd = bloc_bash(s, "evaluer --reel", exclut="--json")
    cas.append(Cas("exemples §7.1 --reel", "exemples.md", cmd.corps,
                   bloc_lang(s, "text").corps, "texte"))

    # § 7.2 — le JSON de --reel
    s = section(sections, "### 7.2")
    cmd = bloc_bash(s, "evaluer --reel --json")
    cas.append(Cas("exemples §7.2 --reel JSON", "exemples.md", cmd.corps,
                   bloc_apres(s, cmd, "json").corps, "json"))

    return cas


def extraire_syntagmes(texte: str) -> str:
    lignes = normaliser_texte(texte).split("\n")
    try:
        debut = lignes.index("SYNTAGMES") + 1
    except ValueError:
        return "\n".join(lignes)
    fin = len(lignes)
    for i in range(debut, len(lignes)):
        if lignes[i].startswith(("PRAGMATIQUE", "COUVERTURE", "TAGGER API")):
            fin = i
            break
    return "\n".join(lignes[debut:fin]).strip()


# --------------------------------------------------------------------------- démarrage sans structures


def copie_sans_structures(destination: pathlib.Path) -> None:
    """La copie du code **sans** `tools/structures` : la condition du clone public."""
    ignorer = shutil.ignore_patterns("structures", "docwatch", "__pycache__", "*.pyc")
    shutil.copytree(RACINE / "tools", destination / "tools", ignore=ignorer)
    for nom in ("pyproject.toml", "README.md"):
        source = RACINE / nom
        if source.is_file():
            shutil.copy2(source, destination / nom)


def cas_demarrage(texte: str, cwd: pathlib.Path) -> tuple[list[Cas], dict]:
    sections = lire_sections(texte)
    cas: list[Cas] = []

    # Les trois commandes du § 3, telles que le débutant les lance.
    for prefixe, ident in (
        ("### 3.1", "demarrage §3.1 --version"),
        ("### 3.2", "demarrage §3.2 analyser"),
        ("### 3.3", "demarrage §3.3 evaluer"),
    ):
        s = section(sections, prefixe)
        cmd = bloc_bash(s, "drave ")
        attendu = bloc_lang(s, "text").corps
        commande = cmd.corps.replace("drave ", "python3 tools/drave.py ", 1)
        cas.append(Cas(ident, "demarrage.md", commande, attendu, "texte", cwd=cwd))

    # § 3.4 — le JSON et son consommateur
    s = section(sections, "### 3.4")
    cmd = bloc_bash(s, "--json")
    commande = (cmd.corps.replace("drave ", "python3 tools/drave.py ", 1)
                .replace("> annotation.json", "> annotation.json"))
    attendu = bloc_lang(s, "json").corps
    cas.append(Cas("demarrage §3.4 JSON", "demarrage.md", commande, attendu, "json_lignes",
                   cwd=cwd))
    cas.append(Cas("demarrage §3.4 octets", "demarrage.md", commande, "5899", "octets",
                   cwd=cwd, detail="le JSON complet annoncé à 5 899 octets"))

    cmd = bloc_bash(s, "python3 -c")
    attendu = bloc_lang(s, "text").corps
    cas.append(Cas("demarrage §3.4 consommateur", "demarrage.md", cmd.corps, attendu,
                   "texte", cwd=cwd))

    # § 3.5 — les profils
    s = section(sections, "### 3.5")
    cmd = bloc_bash(s, "profils --texte")
    attendu = bloc_lang(s, "text").corps
    # Le bloc du § 3.5 enchaîne quatre commandes pour la même sortie : on rejoue la première.
    commande = cmd.corps.splitlines()[0].replace("drave ", "python3 tools/drave.py ", 1)
    cas.append(Cas("demarrage §3.5 profils", "demarrage.md", commande, attendu, "texte",
                   cwd=cwd))

    # Les chiffres de la note : le dépôt de développement, avec structures, rend agent/chat
    # et 79,02 / 99,58. On les vérifie sur une seule exécution chacun.
    note = {
        "analyser": "rôle=agent", "cible": "→ chat", "f1": "F1 79.02 %",
        "attachement": "ATTACHEMENT exact 99.58 %",
    }
    return cas, note


# --------------------------------------------------------------------------- exécution des cas


def executer_cas(c: Cas) -> tuple[bool, list[str], str]:
    """Rend (ok, écarts, détail)."""
    if c.genre == "syntagmes":
        attendu = extraire_syntagmes(c.attendu)
        proc = executer(c.commande, c.cwd)
        if proc.returncode != 0:
            return False, [f"code {proc.returncode}: {proc.stderr.strip()[:300]}"], ""
        obtenu = extraire_syntagmes(proc.stdout)
        if normaliser_texte(attendu) == normaliser_texte(obtenu):
            return True, [], f"{len(attendu.splitlines())} ligne(s) de syntagmes"
        return False, [f"SYNTAGMES:\nattendu:\n{attendu}\nobtenu:\n{obtenu}"], ""

    proc = executer(c.commande, c.cwd)

    if c.genre == "refus":
        lignes = normaliser_texte(c.attendu).split("\n")
        message = lignes[0] if lignes else ""
        code_attendu = None
        for ligne in lignes:
            m = re.fullmatch(r"exit=(\d+)", ligne.strip())
            if m:
                code_attendu = int(m.group(1))
        ecarts = []
        if normaliser_texte(proc.stderr) != message:
            ecarts.append(f"stderr: {message!r} attendu, {proc.stderr.strip()!r} reçu")
        if code_attendu is None:
            ecarts.append("le bloc attendu ne porte pas de ligne exit=N")
        elif f"exit={code_attendu}" not in normaliser_texte(proc.stdout):
            ecarts.append(f"stdout: exit={code_attendu} attendu, {proc.stdout.strip()!r} reçu")
        if proc.returncode != 0:
            ecarts.append(f"code du shell {proc.returncode} (la commande doit rendre 0)")
        return not ecarts, ecarts, f"code {code_attendu}, stderr exact"

    if proc.returncode != 0:
        return False, [f"code {proc.returncode}: {proc.stderr.strip()[:300]}"], ""

    if c.genre in ("json", "json_duree"):
        try:
            attendu = json.loads(c.attendu)
        except json.JSONDecodeError as exc:
            return False, [f"JSON attendu illisible: {exc}"], ""
        try:
            obtenu = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            return False, [f"JSON obtenu illisible: {exc}\n{proc.stdout[:300]}"], ""
        ecarts = comparer_json(attendu, obtenu)
        detail = "JSON exact"
        if c.genre == "json_duree":
            detail = f"duree_s={obtenu.get('duree_s')} (variable), octets exacts"
            if "duree_s" not in obtenu:
                ecarts.append("cout.duree_s absent alors que --duree est demandé")
        return not ecarts, ecarts, detail

    if c.genre == "octets":
        if proc.returncode != 0:
            return False, [f"code {proc.returncode}: {proc.stderr.strip()[:300]}"], ""
        fichier = c.cwd / "annotation.json"
        if not fichier.is_file():
            return False, [f"{fichier} absent"], ""
        taille = fichier.stat().st_size
        attendu = int(c.attendu)
        if taille == attendu:
            return True, [], f"{taille} octets"
        return False, [f"{taille} octets, {attendu} attendus"], ""

    if c.genre == "json_lignes":
        # Le bloc du démarrage est un extrait de 22 lignes, pas un JSON complet.
        attendu = normaliser_texte(c.attendu)
        obtenu = normaliser_texte(proc.stdout)
        if attendu == obtenu:
            return True, [], f"{len(attendu.splitlines())} lignes"
        return False, [f"extrait:\nattendu:\n{attendu}\nobtenu:\n{obtenu}"], ""

    if c.genre == "texte":
        attendu = normaliser_texte(c.attendu)
        obtenu = normaliser_texte(proc.stdout)
        if attendu == obtenu:
            return True, [], f"{len(attendu.splitlines())} ligne(s)"
        # premier écart utile
        la, lo = attendu.split("\n"), obtenu.split("\n")
        for i in range(min(len(la), len(lo))):
            if la[i] != lo[i]:
                return False, [f"ligne {i + 1}: {la[i]!r} attendu, {lo[i]!r} reçu"], ""
        return False, [f"{len(la)} lignes attendues, {len(lo)} reçues"], ""

    return False, [f"genre inconnu: {c.genre}"], ""


def verifier_note_demarrage(note: dict) -> list[dict]:
    """Les chiffres de la note du § 3, dans le dépôt de développement (avec structures)."""
    resultats = []
    proc = executer("python3 tools/drave.py analyser \"Le chat dort.\"", RACINE)
    for cle in ("analyser", "cible"):
        ok = proc.returncode == 0 and note[cle] in proc.stdout
        resultats.append({"id": f"note dev {cle}", "ok": ok, "ecarts": [],
                          "detail": note[cle] if ok else f"absent de: {proc.stdout[:200]}"})
    proc = executer("python3 tools/drave.py evaluer", RACINE)
    for cle in ("f1", "attachement"):
        ok = proc.returncode == 0 and note[cle] in proc.stdout
        resultats.append({"id": f"note dev {cle}", "ok": ok, "ecarts": [],
                          "detail": note[cle] if ok else f"absent de: {proc.stdout[:200]}"})
    return resultats


def verifier_invariants() -> list[dict]:
    """Les invariants v2 : candidats objets, spans exacts, rôles dans le vocabulaire, durée.

    Ce n'est pas une comparaison à la doc : c'est le contrat que la doc affirme. Il est
    vérifié sur les quatre textes des blocs JSON (g001, g011, r241, r035).
    """
    textes = [
        "Le chat dort.",
        "Le livre que j'ai lu est intéressant.",
        "The day when we left was beautiful.",
        "The film she talks about is out.",
    ]
    total = 0
    faux: list[str] = []
    roles: set[str] = set()
    for texte in textes:
        proc = executer(f"python3 tools/drave.py analyser {json.dumps(texte, ensure_ascii=False)} --json",
                        RACINE)
        if proc.returncode != 0:
            faux.append(f"{texte!r}: code {proc.returncode}")
            continue
        annotation = json.loads(proc.stdout)
        for etiquette in annotation["etiquettes"]:
            if etiquette["niveau"] != "syntagme":
                continue
            role = etiquette.get("meta", {}).get("role", "")
            if role:
                roles.add(role)
            for candidat in etiquette.get("meta", {}).get("attachement", {}).get("candidats", []):
                if not isinstance(candidat, dict):
                    faux.append(f"{texte!r}: candidat non objet {candidat!r}")
                    continue
                total += 1
                span = candidat.get("span", {})
                debut, fin = span.get("debut"), span.get("fin")
                if not (isinstance(debut, int) and isinstance(fin, int)
                        and 0 <= debut < fin <= len(texte)):
                    faux.append(f"{texte!r}: span invalide {span!r}")
                elif texte[debut:fin] != candidat.get("cible"):
                    faux.append(f"{texte!r}: {texte[debut:fin]!r} != {candidat.get('cible')!r}")
    hors = sorted(roles - set(ROLES))

    # La durée : absente par défaut, numérique avec --duree.
    sans = executer("python3 tools/drave.py analyser \"Le chat dort.\" --json", RACINE)
    avec = executer("python3 tools/drave.py analyser \"Le chat dort.\" --json --duree", RACINE)
    duree_ok = (sans.returncode == 0 and avec.returncode == 0
                and "duree_s" not in json.loads(sans.stdout).get("cout", {})
                and isinstance(json.loads(avec.stdout).get("cout", {}).get("duree_s"), (int, float))
                and json.loads(avec.stdout)["cout"]["duree_s"] >= 0)

    resultats = []
    resultats.append({
        "id": "invariants candidats objets", "ok": not faux, "ecarts": faux,
        "detail": f"{total} candidats objets, 0 span faux" if not faux else f"{len(faux)} écart(s)",
    })
    resultats.append({
        "id": "invariants rôles normalisés", "ok": not hors, "ecarts": hors,
        "detail": f"{len(roles)} rôle(s), tous dans les {len(ROLES)} du vocabulaire"
                  if not hors else f"hors vocabulaire : {hors}",
    })
    resultats.append({
        "id": "invariants durée", "ok": duree_ok, "ecarts": [] if duree_ok else ["durée"],
        "detail": "absente sans --duree, numérique avec",
    })
    return resultats


# --------------------------------------------------------------------------- principal


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--json", action="store_true", help="rapport machine sur stdout")
    parseur.add_argument("--mutation", action="store_true",
                         help="contrôle négatif : casse une valeur et exige la détection")
    parseur.add_argument("--sans-demarrage", action="store_true",
                         help="ne pas copier le code sans structures (plus rapide)")
    args = parseur.parse_args(argv)

    if shutil.which("jq") is None:
        print("verifie_exemples: jq est requis", file=sys.stderr)
        return 2

    texte_exemples = EXEMPLES.read_text(encoding="utf-8")
    texte_demarrage = DEMARRAGE.read_text(encoding="utf-8")

    mutation = False
    if args.mutation:
        # Une seule valeur : `qualite` -> `qualité` dans le premier bloc JSON.
        avant = texte_exemples
        texte_exemples = texte_exemples.replace('"role": "qualite"', '"role": "qualité"', 1)
        mutation = texte_exemples != avant
        if not mutation:
            print("verifie_exemples: mutation impossible (motif absent)", file=sys.stderr)
            return 2

    cas = cas_exemples(texte_exemples)
    note = {}
    temporaire = None
    try:
        if not args.sans_demarrage:
            temporaire = tempfile.TemporaryDirectory(prefix="drave-exemples-")
            cwd = pathlib.Path(temporaire.name)
            copie_sans_structures(cwd)
            cas_dem, note = cas_demarrage(texte_demarrage, cwd)
            cas.extend(cas_dem)
        resultats = []
        for c in cas:
            ok, ecarts, detail = executer_cas(c)
            resultats.append({"id": c.ident, "doc": c.doc, "ok": ok, "detail": detail,
                              "ecarts": ecarts, "genre": c.genre})
        if note and not args.sans_demarrage:
            resultats.extend(verifier_note_demarrage(note))
        resultats.extend(verifier_invariants())
    finally:
        if temporaire is not None:
            temporaire.cleanup()

    echecs = [r for r in resultats if not r["ok"]]
    ok = not echecs

    if args.json:
        rapport = {
            "outil": "tools/verifie_exemples.py",
            "date": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "head": subprocess.run(["git", "rev-parse", "--short=8", "HEAD"], cwd=RACINE,
                                   text=True, capture_output=True).stdout.strip(),
            "mutation": mutation,
            "ok": ok,
            "comptes": {"cas": len(resultats), "ok": len(resultats) - len(echecs),
                        "echecs": len(echecs)},
            "resultats": resultats,
        }
        if mutation:
            rapport["mutation_detectee"] = bool(echecs)
        sys.stdout.write(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n")
    else:
        for r in resultats:
            marque = "✅" if r["ok"] else "❌"
            print(f"  {marque} {r['id']} — {r['detail'] or 'conforme'}")
            for e in r["ecarts"][:3]:
                print(f"      {e}")
        if mutation:
            print(f"\n{'✅' if echecs else '❌'} mutation détectée : "
                  f"{len(echecs)} cas en écart (attendu > 0)")
        print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} cas conformes"
              + (" — ✅ aucun écart" if ok else f" — ❌ {len(echecs)} écart(s)"))

    if mutation:
        return 0 if echecs else 1
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

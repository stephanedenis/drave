#!/usr/bin/env python3
"""verifie_etat_a_jour.py — aucun fait commité sans sa ligne d'état.

POURQUOI CET OUTIL EXISTE. `en-cours` est la seule source de l'état, et le contrat
disait « seul le principal écrit ». Ce n'est pas une garantie : l'identité se déduit
d'une variable d'environnement absente — un « pair » est autodéclaré — et si la
principale s'arrête, l'état se fige. Surtout, rien ne comparait les commits : la
revue ne regardait que la DATE, donc deux commits du même jour passaient. Le 29/10,
A8.0 (15 h 51) a été commité après le dernier état (15 h 34) sans aucune alerte.

La garantie est au commit, pas dans la discipline d'un écrivain :
  --index  (hook pre-commit) : un commit qui prépare un fait (reports/, roadmap,
           backlog) sans toucher `en-cours` est REFUSÉ ;
  --head   : si un fait a été commité après le dernier commit d'`en-cours`, l'état
           est en retard — la session qui le voit le corrige, sans attendre.

Le journal est du récit dérivé (le hook l'archive) : il n'exige pas de ligne d'état.

Usage :
  python3 tools/verifie_etat_a_jour.py             # --head
  python3 tools/verifie_etat_a_jour.py --index     # pour le hook
  python3 tools/verifie_etat_a_jour.py --autotest  # contrôle négatif, dépôt temporaire
"""
from __future__ import annotations
import argparse
import pathlib
import subprocess
import sys
import tempfile

ETAT = "docs/pilotage/en-cours.md"
FAITS = ("reports/", "docs/pilotage/roadmap.md", "docs/pilotage/backlog/")


def est_fait(chemin: str) -> bool:
    """Un fait est ce qui change l'état du projet : fiche, JSON, plan, backlog."""
    return chemin.startswith(FAITS[0]) or chemin == FAITS[1] or chemin.startswith(FAITS[2])


def git(racine: pathlib.Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=str(racine), text=True, capture_output=True
    )


def dernier_commit(racine: pathlib.Path, chemins):
    """Rend (hash, court, sujet) du dernier commit qui touche `chemins`, ou None."""
    r = git(racine, "log", "-1", "--format=%H%x1f%h%x1f%s", "--", *chemins)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return tuple(r.stdout.strip().split("\x1f", 2))


def est_ancetre(racine: pathlib.Path, a: str, b: str) -> bool:
    return git(racine, "merge-base", "--is-ancestor", a, b).returncode == 0


def retards(racine: pathlib.Path):
    """Rend (état, fait, lignes) si un fait est postérieur au dernier état, sinon None."""
    etat = dernier_commit(racine, [ETAT])
    if etat is None:
        return ("absent", None, [])
    fait = dernier_commit(racine, list(FAITS))
    if fait is None or fait[0] == etat[0]:
        return None
    if not est_ancetre(racine, etat[0], fait[0]):
        return None
    r = git(racine, "log", "--format=%h %s", f"{etat[0]}..{fait[0]}", "--", *FAITS)
    lignes = [l for l in r.stdout.splitlines() if l.strip()]
    return (etat, fait, lignes)


def faits_index(racine: pathlib.Path):
    """Rend les faits stagés si `en-cours` n'est pas stagé avec eux."""
    r = git(racine, "diff", "--cached", "--name-only")
    stages = [l for l in r.stdout.splitlines() if l.strip()]
    faits = [p for p in stages if est_fait(p)]
    if faits and ETAT not in stages:
        return faits
    return []


def etat_modifie(racine: pathlib.Path) -> bool:
    """Vrai si `en-cours` a une modification (index ou copie de travail) non commitée.

    Sert à la revue de clôture : elle tourne AVANT le commit, donc l'état corrigé
    n'est pas encore dans HEAD. On ne crie pas au retard quand la correction est
    déjà dans l'arbre ; le hook, lui, vérifie qu'elle est bien dans l'index.
    """
    r = git(racine, "status", "--porcelain", "--", ETAT)
    return bool(r.stdout.strip())


def resume(racine: pathlib.Path) -> str:
    etat = dernier_commit(racine, [ETAT])
    fait = dernier_commit(racine, list(FAITS))
    if etat is None:
        return "  état · aucun commit d'en-cours"
    fin = f"dernier état {etat[1]}"
    if fait is not None:
        fin = f"dernier fait {fait[1]} · {fin}"
    return f"  état · {fin}"


def signaler_retard(ret) -> None:
    etat, fait, lignes = ret
    if etat == "absent":
        print("  ❌ en-cours n'a jamais été commité : l'état n'existe pas")
        return
    print(f"  ❌ état en retard : {len(lignes)} fait(s) commité(s) après "
          f"{etat[1]} « {etat[2][:64]} »")
    for ligne in lignes[:5]:
        print(f"     · {ligne}")
    if len(lignes) > 5:
        print(f"     · … et {len(lignes) - 5} autre(s)")
    print("     → ajouter la ligne dans docs/pilotage/en-cours.md, puis committer")


def _ecrire(chemin: pathlib.Path, texte: str) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(texte, encoding="utf-8")


def _commit(racine: pathlib.Path, message: str) -> int:
    git(racine, "add", "-A")
    return git(racine, "commit", "-q", "-m", message).returncode


def autotest() -> int:
    """Contrôle négatif : les deux modes doivent REFUSER puis PASSER."""
    with tempfile.TemporaryDirectory() as d:
        r = pathlib.Path(d)
        git(r, "init", "-q")
        git(r, "config", "user.email", "etat@test")
        git(r, "config", "user.name", "etat")
        _ecrire(r / "reports/a.md", "un fait")
        if _commit(r, "fait seul") != 0:
            print("  ❌ autotest : le dépôt temporaire n'a pas pu committer")
            return 1
        cas = [
            ("head · fait sans état", retards(r) is not None, True),
        ]
        _ecrire(r / ETAT, "# En ce moment\n\n**Mis à jour : 2026-10-29**\n")
        if _commit(r, "état") != 0:
            print("  ❌ autotest : commit d'état impossible")
            return 1
        cas.append(("head · état après le fait", retards(r) is None, True))

        _ecrire(r / "reports/b.md", "un second fait")
        if _commit(r, "fait après état") != 0:
            print("  ❌ autotest : commit du second fait impossible")
            return 1
        cas.append(("head · fait après état", retards(r) is not None, True))

        _ecrire(r / ETAT, "# En ce moment\n\n**Mis à jour : 2026-10-30**\n")
        if _commit(r, "état rattrapé") != 0:
            print("  ❌ autotest : commit de rattrapage impossible")
            return 1
        cas.append(("head · état rattrapé", retards(r) is None, True))

        _ecrire(r / "reports/c.md", "fait stagé")
        git(r, "add", "reports/c.md")
        cas.append(("index · fait stagé sans état", faits_index(r) != [], True))

        _ecrire(r / ETAT, "# En ce moment\n\n**Mis à jour : 2026-10-31**\n")
        git(r, "add", ETAT)
        cas.append(("index · état stagé avec le fait", faits_index(r) == [], True))

        mauvais = [nom for nom, obtenu, attendu in cas if obtenu != attendu]
        if mauvais:
            print(f"  ❌ autotest : {len(mauvais)} cas faux — " + " · ".join(mauvais))
            return 1
        print(f"  ✅ autotest : {len(cas)} cas, dont 3 refus attendus et 3 passes")
        return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--index", action="store_true", help="vérifie l'index (hook pre-commit)")
    p.add_argument("--head", action="store_true", help="vérifie HEAD (défaut)")
    p.add_argument("--autotest", action="store_true", help="contrôle négatif en dépôt temporaire")
    p.add_argument("--racine", default=str(pathlib.Path(__file__).resolve().parent.parent))
    p.add_argument("--quiet", action="store_true")
    a = p.parse_args(argv)
    r = pathlib.Path(a.racine)

    if a.autotest:
        return autotest()

    if a.index:
        faits = faits_index(r)
        if faits:
            if not a.quiet:
                print(f"  ❌ commit refusé : {len(faits)} fait(s) stagé(s) sans {ETAT}")
                for f in faits[:5]:
                    print(f"     · {f}")
                print("     → mettre l'état à jour, puis `git add docs/pilotage/en-cours.md`")
            return 1
        if not a.quiet:
            print("  ✅ index : aucun fait stagé sans état")
        return 0

    ret = retards(r)
    if ret is None:
        if not a.quiet:
            print(resume(r))
            print("  ✅ aucun fait commité après le dernier état")
        return 0
    if not a.quiet:
        signaler_retard(ret)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

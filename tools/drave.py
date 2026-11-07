#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, quatre gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
**restitution v0** (annotation → surface, avec la fidélité du miroir). La restitution est un
**codec de surface** : elle reconstruit depuis le niveau `graphème`, pas un décodeur neuronal.
Ce qu'elle n'expose pas encore : le neuronal (`llama-cli` ou endpoint local), la traduction et la
génération : ils demandent des poids, un service ou un GPU, alors que ce prototype est hors ligne,
CPU et sans réseau.

Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 1 erreur.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import random
import sys
import textwrap

# Le dépôt d'abord — `sys.path.insert(0, '.')` quand on lance depuis sa racine, et les chemins
# déduits du fichier pour que la commande marche aussi depuis un autre répertoire. Aucun paquet
# externe n'est importé : le point d'entrée est autonome.
sys.path.insert(0, ".")
RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "tools"))
sys.path.insert(0, str(RACINE))

import bloc_linguistique as bl  # noqa: E402  (import après l'installation des chemins)
import restitution  # noqa: E402  (la restitution v0 : annotation → surface)

NOM = "drave"
VERSION = "0.1.0"
LARGEUR = 100


# --------------------------------------------------------------------------- sorties JSON


def _sur(s: str) -> str:
    """Une chaîne toujours **écrivable** : un surrogate isolé devient U+FFFD (jamais d'exception)."""
    return s.encode("utf-8", "replace").decode("utf-8", "replace")


def _dumps(objet) -> str:
    """JSON stable (pas d'horodatage, pas de durée) et lisible."""
    return _sur(json.dumps(objet, ensure_ascii=False, indent=1)) + "\n"


def _canonique(a: bl.Annotation) -> str:
    """La forme comparée par `rejouer` : clés triées, durée exclue, sans espaces inutiles."""
    return _sur(json.dumps(a.json(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))


# --------------------------------------------------------------------------- rendu lisible


def _valeur_affichee(valeur: str, largeur: int) -> str:
    """Une valeur de syntagme sur une ligne (les blancs sont normalisés pour l'affichage)."""
    v = " ".join(str(valeur).split())
    if len(v) <= largeur:
        return v
    return v[: max(1, largeur - 1)].rstrip() + "…"


def _envelopper(prefixe: str, contenu: str, largeur: int = LARGEUR) -> list[str]:
    """Coupe une ligne trop longue en gardant l'alignement sous le préfixe."""
    lignes = textwrap.wrap(contenu, width=max(20, largeur - len(prefixe)),
                           break_long_words=False, break_on_hyphens=False) or [""]
    return [prefixe + lignes[0]] + [" " * len(prefixe) + ligne for ligne in lignes[1:]]


class _Formateur(argparse.RawDescriptionHelpFormatter):
    """Une aide de largeur fixe : la sortie ne dépend pas de la taille du terminal."""

    def __init__(self, prog: str, **kwargs):
        kwargs.setdefault("width", LARGEUR)
        super().__init__(prog, **kwargs)


def formater_annotation(a: bl.Annotation) -> str:
    """La sortie lisible : POS compact, syntagmes (rôle + cible), pragmatique, couverture."""
    lignes = [f"{NOM} {VERSION} — analyse heuristique (CPU, hors ligne)"]
    lignes.append(
        f"langue={a.langue} script={a.script} source={a.source} · {len(a.etiquettes)} étiquettes "
        f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"
    )

    pos = [e for e in a.etiquettes if e.niveau == "pos"]
    if pos:
        lignes.extend(_envelopper("POS  ", " ".join(f"{e.valeur}/{e.type}" for e in pos)))
    else:
        lignes.append("POS  —")

    syntagmes = [e for e in a.etiquettes if e.niveau == "syntagme"]
    if syntagmes:
        valeurs = [_valeur_affichee(e.valeur, 46) for e in syntagmes]
        roles = [str(e.meta.get("role") or "—") for e in syntagmes]
        cibles = [str((e.meta.get("attachement") or {}).get("cible") or "—") for e in syntagmes]
        spans = [f"[{e.debut}:{e.fin}]" for e in syntagmes]
        lt = max(3, max(len(e.type) for e in syntagmes))
        lsp = max(len(s) for s in spans)
        lv = max(len(v) for v in valeurs)
        lr = max(len(r) for r in roles)
        lignes.append("SYNTAGMES")
        for e, valeur, role, cible, span in zip(syntagmes, valeurs, roles, cibles, spans):
            lignes.append(
                f"  {e.type:<{lt}}  {span:<{lsp}}  {valeur:<{lv}}  "
                f"rôle={role:<{lr}}  → {cible}"
            )
    else:
        lignes.append("SYNTAGMES —")

    phrases = [e for e in a.etiquettes if e.niveau == "phrase" and e.type == "type"]
    if phrases:
        lignes.append("PRAGMATIQUE")
        par_span: dict[tuple[int, int], list[bl.Etiquette]] = {}
        for e in a.etiquettes:
            if e.niveau == "pragmatique":
                par_span.setdefault((e.debut, e.fin), []).append(e)
        for p in phrases:
            ici = par_span.get((p.debut, p.fin), [])
            acte = next((e.valeur for e in ici if e.type == "acte"), "—")
            negation = "oui" if any(e.type == "négation" for e in ici) else "non"
            modalite = "oui" if any(e.type == "modalité" for e in ici) else "non"
            double_sens = "oui" if any(e.type == "double_sens" for e in ici) else "non"
            lignes.append(
                f"  phrase [{p.debut}:{p.fin}] {p.valeur} · acte={acte} "
                f"· négation={negation} · modalité={modalite} · double sens={double_sens}"
            )
    else:
        lignes.append("PRAGMATIQUE —")

    couverture = a.couverture()
    if couverture:
        ordre = [n for n in bl.NIVEAUX if n in couverture]
        ordre += sorted(n for n in couverture if n not in bl.NIVEAUX)
        lignes.extend(_envelopper(
            "COUVERTURE  ",
            "(confiance max par niveau)  "
            + " · ".join(f"{n}={couverture[n]:.2f}" for n in ordre),
        ))
    return "\n".join(lignes)


# --------------------------------------------------------------------------- commandes


def _lire_entree(args: argparse.Namespace) -> str:
    """Le texte : l'argument, ou le **fichier** (`--fichier`)."""
    if getattr(args, "fichier", None):
        return pathlib.Path(args.fichier).read_text(encoding="utf-8", errors="replace")
    return args.texte or ""


def _analyser_jsonl(texte: str, args: argparse.Namespace) -> int:
    """Une **ligne JSON par phrase** (traitement de corpus : `--jsonl`)."""
    h = bl.Heuristique(partition=args.partition)
    n = 0
    for debut, fin, _typ, _ in h._phrases(texte):
        phrase = texte[debut:fin]
        if not phrase.strip():
            continue
        a = h.analyser(phrase, args.langue, args.contexte)
        sys.stdout.write(_sur(json.dumps(a.json(), ensure_ascii=False)) + "\n")
        n += 1
    if n == 0:
        print(f"{NOM}: refus d'analyse : vide", file=sys.stderr)
        return 3
    return 0


def cmd_analyser(args: argparse.Namespace) -> int:
    texte = _lire_entree(args)
    if args.jsonl:
        return _analyser_jsonl(texte, args)
    annotation = bl.Heuristique(partition=args.partition).analyser(texte, args.langue,
                                                                   args.contexte)
    if annotation.refus:
        # un refus est une **réponse** : le JSON la porte, le code 3 la distingue d'une erreur
        if args.json:
            sys.stdout.write(_dumps(annotation.json()))
        else:
            print(f"{NOM}: refus d'analyse : {annotation.refus} "
                  "(le texte doit contenir au moins une lettre ou un chiffre)", file=sys.stderr)
        return 3
    if args.json:
        sys.stdout.write(_dumps(annotation.json()))
    else:
        print(_sur(formater_annotation(annotation)))
    return 0


def _module_evaluation():
    """Charge `evaluer_gold.py` (le gold et sa mesure) sans dépendre du répertoire courant."""
    chemin = RACINE / "tools" / "tests" / "linguistique" / "evaluer_gold.py"
    if not chemin.is_file():
        raise FileNotFoundError(f"mesure du gold introuvable : {chemin}")
    spec = importlib.util.spec_from_file_location("_drave_evaluer_gold", chemin)
    if spec is None or spec.loader is None:
        raise ImportError(f"impossible de charger {chemin}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _cibles_gold(phrases: list[dict]) -> list[str]:
    return [s["cible"] for p in phrases for s in p.get("segments", []) if s.get("cible")]


def _controle_hasard(phrases: list[dict]) -> float:
    """Contrôle négatif : une cible **exacte** tirée au hasard parmi les cibles du gold.

    Graine fixe, donc reproductible : c'est un plancher, pas une mesure de qualité.
    """
    cibles = _cibles_gold(phrases)
    if not cibles:
        return 0.0
    univers = sorted(set(cibles))
    rng = random.Random(0)
    justes = sum(1 for c in cibles if rng.choice(univers) == c)
    return round(justes / len(cibles), 4)


def _pct(valeur: float) -> str:
    return f"{100.0 * float(valeur):.2f} %"


def _formater_evaluation(rapport: dict) -> str:
    gold = rapport["gold"]
    mesure = rapport["heuristique"]
    pos = mesure["pos"]
    syn = mesure["syntagme"]
    tete = syn["tete"]
    att = mesure["attachement"]
    att_tete = mesure["attachement_tete"]
    prag = mesure["pragmatique"]
    controle = rapport["controle_negatif"]
    return "\n".join([
        f"{NOM} {VERSION} — évaluation de l'heuristique sur le gold",
        f"gold {gold['nom']} · {gold['phrases']} phrases · {gold['tokens']} tokens · "
        f"{gold['cibles_attachement']} cibles d'attachement",
        "",
        f"POS         exactitude {_pct(pos['exactitude'])}  "
        f"(fermé {_pct(pos['exactitude_ferme'])}, ouvert {_pct(pos['exactitude_ouvert'])})",
        f"SYNTAGMES   F1 {_pct(syn['f1'])}  "
        f"(P {_pct(syn['precision'])} / R {_pct(syn['rappel'])})",
        f"  tête      F1 {_pct(tete['f1'])}  "
        f"(P {_pct(tete['precision'])} / R {_pct(tete['rappel'])})",
        f"  vue linéaire (partition filtrer) F1 {_pct(rapport['syntagmes_lineaire']['f1'])}  "
        f"· attachement {_pct(rapport['attachement_lineaire']['couverture'])} de couverture",
        f"ATTACHEMENT exact {_pct(att['exact_taux'])} · couverture {_pct(att['couverture'])} "
        f"· exact sur span {_pct(att['exact_taux_span'])} · top-k {_pct(att['topk_taux'])}",
        f"  tête      couverture {_pct(att_tete['couverture'])} "
        f"· top-k {_pct(att_tete['topk_taux'])}",
        f"PRAGMATIQUE acte {_pct(prag['acte'])} · négation {_pct(prag['negation'])} "
        f"· modalité {_pct(prag['modalite'])} · double sens {_pct(prag['double_sens'])}",
        f"FRACTION SÉMANTIQUE {_pct(mesure['fraction_semantique'])}",
        f"CONTRÔLE NÉGATIF cible exacte tirée au hasard {_pct(controle['exact_taux'])} "
        f"(graine {controle['graine']}, {controle['cibles']} cibles)",
    ])


def cmd_evaluer(args: argparse.Namespace) -> int:
    evaluateur = _module_evaluation()
    phrases = evaluateur.charger_gele() if args.gold else evaluateur.charger()
    mesure = evaluateur.evaluer_bloc("heuristique", bl.Heuristique(), phrases)
    # transparence : la vue **fidèle** (défaut) et la vue **linéaire** (partition filtrer)
    _lineaire = evaluateur.evaluer_bloc("lineaire", bl.Heuristique(partition="filtrer"), phrases)
    hasard = _controle_hasard(phrases)
    rapport = {
        "version": VERSION,
        "gold": {
            "nom": "gelé (référence figée)" if args.gold else "vivant (hand + reel + synthétique)",
            "gele": bool(args.gold),
            "phrases": len(phrases),
            "tokens": mesure["pos"]["tokens"],
            "cibles_attachement": mesure["attachement"]["cibles"],
        },
        "heuristique": mesure,
        "syntagmes_lineaire": _lineaire["syntagme"],
        "attachement_lineaire": {"exact": _lineaire["attachement"]["exact"],
                                 "labels": _lineaire["attachement"]["labels"],
                                 "couverture": _lineaire["attachement"]["couverture"]},
        "controle_negatif": {
            "nom": "cible exacte tirée au hasard dans le gold",
            "graine": 0,
            "cibles": len(_cibles_gold(phrases)),
            "exact_taux": hasard,
        },
    }
    if args.json:
        sys.stdout.write(_dumps(rapport))
    else:
        print(_formater_evaluation(rapport))
    return 0


def cmd_rejouer(args: argparse.Namespace) -> int:
    premiere = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
    seconde = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
    if premiere.refus or seconde.refus:
        refus = premiere.refus or seconde.refus
        print(f"{NOM}: refus d'analyse : {refus} "
              "(le texte doit contenir au moins une lettre ou un chiffre)", file=sys.stderr)
        return 1
    canonique_1 = _canonique(premiere)
    canonique_2 = _canonique(seconde)
    identique = canonique_1 == canonique_2
    empreinte = hashlib.sha256(canonique_1.encode("utf-8")).hexdigest()[:16]
    print(f"rejeu identique : {'oui' if identique else 'non'}")
    print(f"  texte      : {args.texte!r}")
    print(f"  langue     : {premiere.langue}")
    print(f"  étiquettes : {len(premiere.etiquettes)}")
    print(f"  JSON       : {len(canonique_1.encode('utf-8'))} octets "
          f"· sha256 {empreinte}…")
    if not identique:
        print("  divergence : les deux analyses ne rendent pas le même JSON canonique",
              file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------- restitution


def cmd_restituer(args: argparse.Namespace) -> int:
    """Reconstruit la surface depuis l'annotation et rend la fidélité du miroir.

    Deux modes : un **texte** (ou un fichier), ou un **banc** JSON de textes
    (`--banc`, le format de `reports/pensee-fiabilite-produit.json`). Le mode banc
    laisse le bloc détecter la langue, comme le CLI sans `--langue`.
    """
    if args.banc:
        if args.texte is not None or args.fichier:
            print(f"{NOM}: erreur d'usage : --banc est exclusif de TEXTE et --fichier",
                  file=sys.stderr)
            return 2
        try:
            donnees = json.loads(pathlib.Path(args.banc).read_text(encoding="utf-8"))
            items = restitution.items_banc(donnees)
        except (OSError, ValueError) as exc:
            print(f"{NOM}: erreur : banc illisible : {exc}", file=sys.stderr)
            return 1
        rapport = restitution.mesurer_banc(items, args.langue)
        rapport["banc"] = args.banc
        if args.json:
            sys.stdout.write(_dumps(rapport))
        else:
            print(_sur(restitution.formater_banc(rapport, args.banc)))
        return 0

    texte = _lire_entree(args)
    if args.texte is None and not args.fichier:
        print(f"{NOM}: erreur d'usage : TEXTE ou --fichier requis", file=sys.stderr)
        return 2
    annotation = bl.Heuristique().analyser(texte, args.langue, args.contexte)
    if annotation.refus:
        print(f"{NOM}: refus d'analyse : {annotation.refus} "
              "(le texte doit contenir au moins une lettre ou un chiffre)", file=sys.stderr)
        return 3
    mesure = restitution.mesurer_annotation(annotation, texte)
    if args.json:
        sys.stdout.write(_dumps({
            "schema": restitution.SCHEMA,
            "version": restitution.VERSION,
            **mesure,
        }))
    else:
        print(_sur(restitution.formater_mesure(mesure, texte)))
    return 0


# --------------------------------------------------------------------------- CLI


class _Parseur(argparse.ArgumentParser):
    """Un parseur francophone : `-h`, `--help` et `--aide` partout, sans doublon."""

    def __init__(self, *args, **kwargs):
        kwargs["add_help"] = False
        super().__init__(*args, **kwargs)
        self._positionals.title = "arguments"
        self._optionals.title = "options"
        self.add_argument("-h", "--help", "--aide", action="help",
                          help="afficher cette aide et quitter")

    def error(self, message: str) -> None:  # type: ignore[override]
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: erreur d'usage : {message}\n")


def construire_parseur() -> argparse.ArgumentParser:
    epilogue = (
        "Commandes : analyser, evaluer, rejouer, restituer.\n"
        "Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) · 1 erreur.\n"
        "Options : --json, --langue fr|en, --partition brut|alternative|filtrer_union|filtrer,\n"
        "--contexte, --banc.\n"
        "Limites : heuristique CPU, hors ligne, déterministe ; la restitution est un codec de\n"
        "surface (graphème), pas un décodeur neuronal ; ni traduction ni génération.\n"
        "Exemples :\n"
        "  python3 tools/drave.py analyser \"Le chat dort.\"\n"
        "  python3 tools/drave.py evaluer --gold --json\n"
        "  python3 tools/drave.py restituer \"Le chat dort.\"\n"
        "  python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json\n"
    )
    parseur = _Parseur(
        prog=NOM,
        description="Point d'entrée produit du bloc linguistique (analyse et restitution).",
        epilog=epilogue,
        formatter_class=_Formateur,
    )
    parseur.add_argument("-V", "--version", action="version", version=f"{NOM} {VERSION}",
                         help="afficher la version et quitter")
    sous = parseur.add_subparsers(dest="commande",
                                  metavar="{analyser,evaluer,rejouer,restituer}",
                                  required=True)

    analyser = sous.add_parser(
        "analyser",
        help="étiqueter un texte (POS, syntagmes, pragmatique)",
        description="Analyse un texte avec l'heuristique et rend la lecture compacte ou le JSON.",
        epilog="Exemple : python3 tools/drave.py analyser \"Le chat dort.\" --json",
        formatter_class=_Formateur,
    )
    analyser.add_argument("texte", metavar="TEXTE", nargs="?", default=None,
                          help="texte à analyser (entre guillemets) ou --fichier")
    analyser.add_argument("--partition", choices=("brut", "alternative", "filtrer_union", "filtrer"),
                          default="alternative",
                          help="la vue des syntagmes qui se chevauchent (défaut : alternative)")
    analyser.add_argument("--fichier", default=None, metavar="CHEMIN",
                          help="lire le texte dans un fichier UTF-8 (au lieu de l'argument)")
    analyser.add_argument("--jsonl", action="store_true",
                          help="une ligne JSON par phrase (traitement de corpus)")
    analyser.add_argument("--contexte", default=None,
                          help="le texte qui précède (mémoire de discours : coréférence, connecteurs)")
    analyser.add_argument("--langue", choices=("fr", "en"), default=None,
                          help="indice de langue (fr/en) ; sans lui, le bloc détecte")
    analyser.add_argument("--json", action="store_true",
                          help="sortie JSON complète (annotation, sans durée)")
    analyser.set_defaults(fonction=cmd_analyser)

    evaluer = sous.add_parser(
        "evaluer",
        help="mesurer l'heuristique sur le gold",
        description="Mesure POS, syntagmes (F1/tête) et attachement (exact/couverture) "
                    "sur le gold, avec un contrôle négatif reproductible.",
        epilog="Exemple : python3 tools/drave.py evaluer --gold --json",
        formatter_class=_Formateur,
    )
    evaluer.add_argument("--gold", action="store_true",
                         help="mesurer le gold gelé (référence figée) au lieu du gold vivant")
    evaluer.add_argument("--json", action="store_true",
                         help="sortie JSON des mesures complètes")
    evaluer.set_defaults(fonction=cmd_evaluer)

    rejouer = sous.add_parser(
        "rejouer",
        help="analyser deux fois et vérifier le déterminisme",
        description="Analyse le texte deux fois, compare le JSON canonique et rend une empreinte "
                    "sha256. Sortie 1 si les deux analyses divergent.",
        epilog="Exemple : python3 tools/drave.py rejouer \"Le chat dort.\"",
        formatter_class=_Formateur,
    )
    rejouer.add_argument("texte", metavar="TEXTE", help="texte à rejouer (entre guillemets)")
    rejouer.add_argument("--partition", choices=("brut", "alternative", "filtrer_union", "filtrer"),
                         default="alternative")
    rejouer.add_argument("--langue", choices=("fr", "en"), default=None,
                         help="indice de langue (fr/en) ; sans lui, le bloc détecte")
    rejouer.set_defaults(fonction=cmd_rejouer)

    restituer = sous.add_parser(
        "restituer",
        help="reconstruire la surface depuis l'annotation et mesurer le miroir",
        description="Analyse un texte, reconstruit la surface depuis le niveau `graphème` "
                    "(sans lire le champ `texte` de l'annotation) et compare à la source. "
                    "Affiche la fidélité binaire du miroir, la fidélité de caractères et un "
                    "contrôle négatif. Avec --banc, mesure un JSON de textes (50 textes libres).",
        epilog="Exemples : python3 tools/drave.py restituer \"Le chat dort.\" ; "
               "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json",
        formatter_class=_Formateur,
    )
    restituer.add_argument("texte", metavar="TEXTE", nargs="?", default=None,
                           help="texte à restituer (entre guillemets) ou --fichier")
    restituer.add_argument("--banc", default=None, metavar="CHEMIN",
                           help="mesurer un banc JSON de textes (ex. les 50 textes libres)")
    restituer.add_argument("--fichier", default=None, metavar="CHEMIN",
                           help="lire le texte dans un fichier UTF-8 (au lieu de l'argument)")
    restituer.add_argument("--langue", choices=("fr", "en"), default=None,
                           help="indice de langue (fr/en) ; sans lui, le bloc détecte")
    restituer.add_argument("--contexte", default=None,
                           help="le texte qui précède (mémoire de discours)")
    restituer.add_argument("--json", action="store_true",
                           help="sortie JSON (restitution, miroir, contrôle négatif)")
    restituer.set_defaults(fonction=cmd_restituer)
    return parseur


def main(argv: list[str] | None = None) -> int:
    # un stdout non-UTF-8 ne doit pas faire planter l'en-tête (« — ») : on tolère les remplacements
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    args = construire_parseur().parse_args(argv)
    try:
        return args.fonction(args)
    except BrokenPipeError:
        # `drave analyser ... | head` : le lecteur a fermé la sortie, ce n'est pas une erreur.
        return 0
    except KeyboardInterrupt:
        print(f"{NOM}: interrompu", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 — le point d'entrée rend un code, pas une trace
        print(f"{NOM}: erreur : {type(exc).__name__} : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

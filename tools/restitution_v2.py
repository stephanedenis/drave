"""restitution_v2.py — la restitution v2 : les rôles (agent, prédicat, lieu).

La v0 restitue la **surface** (graphème → texte) ; la v1 restitue la **forme canonique**
(segments + rôles + cibles). La v2 ajoute une lecture **lisible des rôles** : un cadre
principal `agent / prédicat / lieu`, les cadres de chaque prédicat, et les segments de rôle.

La fidélité des rôles ne se mesure pas contre l'annotation qui les produit (ce serait une
tautologie) : elle se mesure contre un **or de rôles écrit à la main** sur les 46 textes
annotables du banc v0 (`tools/tests/linguistique/gold_restitution_v2.json`). L'or ne porte
que le **cadre principal** et quelques variantes d'ambiguïté ; il ne prétend pas annoter
toutes les propositions.

Deux mesures sont séparées :

- la **restitution** du rôle (le rôle est-il lisible et relu à l'identique ?) — un codec ;
- la **fidélité** du rôle (le rôle est-il celui de l'or ?) — une exactitude sémantique.

Le contrôle négatif retire ou permute les rôles du rendu : le lecteur doit le voir. Le
contrôle « cadre vide » et le contrôle « rôle constant par type » donnent les planchers.

    python3 tools/mesurer_restitution_v2.py
    python3 tools/drave.py restituer "Le chat dort." --roles
"""
from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import tools.bloc_linguistique as bl  # noqa: E402
from tools import restitution as _r  # noqa: E402

SCHEMA = "drave.restitution.v2"
VERSION = 1
SCHEMA_BANC = SCHEMA + ".banc"
ROLES = ("agent", "predicat", "lieu")
LIBELLES = {"agent": "agent", "predicat": "prédicat", "lieu": "lieu"}
VIDE = "—"
GOLD_DEFAUT = RACINE / "tools" / "tests" / "linguistique" / "gold_restitution_v2.json"

# Un rôle normalisé : les deux orthographes du prédicat, rien d'autre n'est touché.
_ROLE_LIGNE = re.compile(r"^\s*(agent|prédicat|predicat|lieu)\s*:\s?(.*)$",
                         re.IGNORECASE)


def normaliser_role(role: str) -> str:
    """`prédicat` → `predicat` ; les autres rôles sont rendus en minuscules."""
    r = (role or "").strip()
    if not r:
        return ""
    return {"agent": "agent", "prédicat": "predicat", "predicat": "predicat",
            "lieu": "lieu"}.get(r.casefold(), r.casefold())


def _valeur_lisible(valeur: str) -> str:
    """Une valeur sur **une** ligne : les blancs (sauts de ligne inclus) sont réduits."""
    return " ".join(str(valeur).split())


def _valeur_ou_vide(valeur: str) -> str:
    v = _valeur_lisible(valeur)
    return v if v else VIDE


def _segments_syntagmes(a: bl.Annotation) -> list[dict]:
    """Les syntagmes triés, avec leur rôle normalisé et leur cible."""
    lineaires = {id(e) for e in _r.segments_lineaires(a)}
    sortie = []
    for e in sorted((x for x in a.etiquettes if x.niveau == "syntagme"),
                    key=lambda x: (x.debut, x.fin, x.type)):
        meta = e.meta or {}
        attachement = meta.get("attachement") or {}
        sortie.append({
            "type": e.type,
            "role": str(meta.get("role", "") or ""),
            "role_normalise": normaliser_role(meta.get("role", "")),
            "niveau": meta.get("niveau", 0),
            "debut": e.debut,
            "fin": e.fin,
            "valeur": e.valeur,
            "cible": str(attachement.get("cible", "") or ""),
            "lineaire": id(e) in lineaires,
            "union": bool(meta.get("union")),
            "confiance": e.confiance,
            "source": e.source,
        })
    return sortie


def _cadre_vide() -> dict:
    return {
        "agent": "", "predicat": "", "lieu": "",
        "agent_role": "", "agent_origine": "",
        "lieu_role": "", "lieu_origine": "",
        "agent_span": None, "predicat_span": None, "lieu_span": None,
    }


def _span(segment: dict | None) -> list[int] | None:
    return [segment["debut"], segment["fin"]] if segment else None


def _plus_proche(segments: list[dict], avant: bool, position: int,
                 fin: bool = False) -> dict | None:
    """Le segment le plus proche avant (ou après) `position`."""
    if avant:
        candidats = [e for e in segments
                     if (e["fin"] <= position if fin else e["debut"] < position)]
        if not candidats:
            return None
        return max(candidats, key=lambda e: (e["fin"], e["debut"]))
    candidats = [e for e in segments if e["debut"] >= position]
    if not candidats:
        return None
    return min(candidats, key=lambda e: (e["debut"], -e["fin"]))


def _cadre_de(predicat: dict, agents: list[dict], lieux: list[dict],
              groupes: list[dict]) -> dict:
    """Le cadre d'un prédicat : agent le plus proche à gauche, lieu le plus proche à droite.

    Si aucun `agent` n'est annoté, un `groupe nominal` **à gauche** du prédicat sert de
    repli (le sujet probable). C'est une heuristique nommée, pas une annotation : elle
    permet de lire `The cat sleeps` alors que le GN anglais n'a pas reçu le rôle `agent`.
    """
    agent = _plus_proche(agents, True, predicat["debut"])
    origine = "agent_avant" if agent else ""
    if not agent:
        agent = _plus_proche(agents, False, predicat["fin"])
        origine = "agent_apres" if agent else ""
    if not agent:
        agent = _plus_proche(groupes, True, predicat["debut"])
        origine = "groupe_nominal_avant" if agent else ""

    lieu = _plus_proche(lieux, False, predicat["fin"])
    origine_lieu = "lieu_apres" if lieu else ""
    if not lieu:
        lieu = _plus_proche(lieux, True, predicat["debut"])
        origine_lieu = "lieu_avant" if lieu else ""

    return {
        "agent": agent["valeur"] if agent else "",
        "predicat": predicat["valeur"],
        "lieu": lieu["valeur"] if lieu else "",
        "agent_role": agent["role"] if agent else "",
        "agent_origine": origine,
        "lieu_role": lieu["role"] if lieu else "",
        "lieu_origine": origine_lieu,
        "agent_span": _span(agent),
        "predicat_span": _span(predicat),
        "lieu_span": _span(lieu),
    }


def cadres(a: bl.Annotation) -> list[dict]:
    """Les cadres (agent, prédicat, lieu), un par prédicat, dans l'ordre de la surface.

    Les prédicats qui commencent au même point sont fusionnés au **plus large** : dans
    `Il n'y a`, `n'y` et `n'y a` sont deux étiquettes du même prédicat ; garder la plus
    large évite de lire un prédicat tronqué. Les autres chevauchements restent des cadres
    distincts (la v1 les documente déjà).
    """
    segments = _segments_syntagmes(a)
    predicats: list[dict] = []
    for e in segments:
        if e["role_normalise"] != "predicat":
            continue
        # même début : garder le plus large (le prédicat complet).
        if predicats and predicats[-1]["debut"] == e["debut"]:
            if e["fin"] > predicats[-1]["fin"]:
                predicats[-1] = e
            continue
        predicats.append(e)
    if not predicats:
        return []
    agents = [e for e in segments if e["role_normalise"] == "agent"]
    lieux = [e for e in segments if e["role_normalise"] == "lieu"]
    groupes = [e for e in segments if e["type"] == "GN"
               and e["role_normalise"] in ("", "groupe nominal")]
    return [_cadre_de(p, agents, lieux, groupes) for p in predicats]


def cadre_principal(a: bl.Annotation, tous: list[dict] | None = None) -> dict:
    """Le cadre principal : le premier qui porte un agent ou un lieu, sinon le premier."""
    tous = cadres(a) if tous is None else tous
    if not tous:
        return _cadre_vide()
    for cadre in tous:
        if cadre["agent"] or cadre["lieu"]:
            return cadre
    return tous[0]


def rendre_roles(a: bl.Annotation) -> dict:
    """La forme **lisible** des rôles : cadre principal, cadres, segments de rôle.

    Le rendu ne lit jamais `Annotation.texte` : il ne lit que les étiquettes `syntagme` et
    leur `meta` (rôle, cible). Les valeurs sont ramenées sur une ligne pour l'affichage.
    """
    segments = _segments_syntagmes(a)
    tous = cadres(a)
    principal = cadre_principal(a, tous)
    roles_segments = [e for e in segments if e["role_normalise"] in ROLES]
    autres = [e for e in segments if e["role_normalise"] not in ROLES]
    lignes = [
        "rôles (agent, prédicat, lieu)",
        f"  agent     : {_valeur_ou_vide(principal['agent'])}",
        f"  prédicat  : {_valeur_ou_vide(principal['predicat'])}",
        f"  lieu      : {_valeur_ou_vide(principal['lieu'])}",
    ]
    if autres:
        lignes.append("  autres    : " + " · ".join(
            f"{e['role'] or e['type']}: {_valeur_lisible(e['valeur'])}" for e in autres))
    lignes.append(f"segments de rôle : {len(roles_segments)}")
    for i, e in enumerate(roles_segments, 1):
        lignes.append(
            f"  {i:2}. {e['type']}/{e['role'] or '—'} [{e['debut']}:{e['fin']}] "
            f"« {_valeur_lisible(e['valeur'])} » → {_valeur_ou_vide(e['cible'])}")
    return {
        "definition": ("cadre principal (agent, prédicat, lieu) lu depuis les syntagmes "
                       "et leur meta.role ; cadres par prédicat ; segments de rôle"),
        "principal": principal,
        "cadres": tous,
        "segments": roles_segments,
        "autres": autres,
        "compteurs": {
            "segments": len(segments),
            "segments_role": len(roles_segments),
            "agents": sum(1 for e in segments if e["role_normalise"] == "agent"),
            "predicats": sum(1 for e in segments if e["role_normalise"] == "predicat"),
            "lieux": sum(1 for e in segments if e["role_normalise"] == "lieu"),
            "cadres": len(tous),
        },
        "lisible": "\n".join(lignes),
        "lignes": lignes,
    }


def relire_roles(texte_lisible: str) -> dict:
    """Relit un rendu de rôles : les trois lignes du cadre principal.

    C'est le **décodeur** de la forme lisible. Il ne connaît que le format publié :
    `agent : valeur`, `prédicat : valeur`, `lieu : valeur`. La valeur `—` vaut vide.
    """
    cadre = {"agent": "", "predicat": "", "lieu": ""}
    for ligne in texte_lisible.splitlines():
        m = _ROLE_LIGNE.match(ligne)
        if not m:
            continue
        role = normaliser_role(m.group(1))
        valeur = m.group(2).strip()
        cadre[role] = "" if valeur in ("", VIDE) else valeur
    return cadre


def _canonique(valeur: str) -> str:
    return _r.canoniser(valeur or "")


def comparer_cadre(predit: dict, variantes: list[dict]) -> dict:
    """Compare un cadre prédit à une liste de cadres attendus (variantes d'ambiguïté).

    Une valeur est **exacte** si sa forme canonique (casse, ponctuation, espaces) égale
    celle de l'or. Le meilleur variant est retenu : les variantes ne sont pas un droit à
    mélanger les rôles, seulement une autre lecture complète du même cadre.
    """
    if not variantes:
        variantes = [{"agent": "", "predicat": "", "lieu": ""}]
    meilleur = None
    for rang, variante in enumerate(variantes):
        par_role = {}
        for role in ROLES:
            p = predit.get(role, "") or ""
            v = variante.get(role, "") or ""
            egal = _canonique(p) == _canonique(v)
            par_role[role] = {
                "predit": p, "attendu": v, "egal": egal,
                "juste": bool(egal and p and v),
                "faux_positif": bool((not egal) and p),
                "faux_negatif": bool((not egal) and v),
                "vrai_negatif": bool(egal and not p and not v),
            }
        exacts = sum(1 for x in par_role.values() if x["egal"])
        justes = sum(1 for x in par_role.values() if x["juste"])
        fp = sum(1 for x in par_role.values() if x["faux_positif"])
        fn = sum(1 for x in par_role.values() if x["faux_negatif"])
        score = (exacts, justes, -fp, -fn, -rang)
        fiche = {
            "variante": rang,
            "exacts": exacts,
            "justes": justes,
            "attendus": sum(1 for v in variante.values() if v),
            "predits": sum(1 for role in ROLES if predit.get(role)),
            "faux_positifs": fp,
            "faux_negatifs": fn,
            "vrais_negatifs": sum(1 for x in par_role.values() if x["vrai_negatif"]),
            "par_role": par_role,
        }
        if meilleur is None or score > meilleur[0]:
            meilleur = (score, fiche)
    return meilleur[1]


def _cadre_constant_par_type(a: bl.Annotation) -> dict:
    """Le plancher : premier GN = agent, premier GV = prédicat, premier GP = lieu."""
    segments = _segments_syntagmes(a)

    def premier(type_: str) -> str:
        for e in segments:
            if e["type"] == type_:
                return e["valeur"]
        return ""

    return {"agent": premier("GN"), "predicat": premier("GV"), "lieu": premier("GP")}


def melanger_roles(cadre: dict) -> dict:
    """Le contrôle : agent ← prédicat, prédicat ← lieu, lieu ← agent."""
    return {"agent": cadre.get("predicat", ""),
            "predicat": cadre.get("lieu", ""),
            "lieu": cadre.get("agent", "")}


def _lignes_rendu(rendu: dict) -> list[str]:
    return list(rendu.get("lignes") or [])


def controler_negatif_rendu(rendu: dict) -> dict:
    """Deux altérations du rendu : retirer le prédicat, permuter agent et prédicat.

    Le lecteur doit voir les deux : la forme lisible n'est pas un decorum, elle porte les
    rôles. Un rendu vide (`f18`, `f27`, `f37`) n'a rien à altérer ; il est marqué inéligible.
    """
    principal = rendu["principal"]
    lignes = _lignes_rendu(rendu)

    def altere(sans: bool) -> tuple[str, dict]:
        sortie = []
        for ligne in lignes:
            m = _ROLE_LIGNE.match(ligne)
            if not m:
                sortie.append(ligne)
                continue
            role = normaliser_role(m.group(1))
            if sans and role == "predicat":
                continue
            if not sans and role == "agent":
                sortie.append(f"  agent     : {_valeur_ou_vide(principal['predicat'])}")
                continue
            if not sans and role == "predicat":
                sortie.append(f"  prédicat  : {_valeur_ou_vide(principal['agent'])}")
                continue
            sortie.append(ligne)
        return "\n".join(sortie), relire_roles("\n".join(sortie))

    texte_sans, relu_sans = altere(True)
    texte_permute, relu_permute = altere(False)
    meme = lambda x: all(_canonique(x.get(r, "")) == _canonique(principal.get(r, ""))
                         for r in ROLES)
    eligible = bool(principal["predicat"])
    return {
        "definition": ("retrait de la ligne `prédicat` et permutation des valeurs "
                       "`agent` / `prédicat` du rendu, puis relecture"),
        "eligible": eligible,
        "sans_predicat": {"lisible": texte_sans, "relu": relu_sans,
                          "change": eligible and not meme(relu_sans)},
        "permute": {"lisible": texte_permute, "relu": relu_permute,
                    "change": eligible and not meme(relu_permute)},
        "detecte": bool(eligible and not meme(relu_sans) and not meme(relu_permute)),
    }


def _dans_source(a: bl.Annotation, source: str) -> dict:
    """Les spans de rôle sont-ils des sous-chaînes exactes de la source ?"""
    total = justes = 0
    for e in _segments_syntagmes(a):
        if e["role_normalise"] not in ROLES:
            continue
        total += 1
        if (0 <= e["debut"] <= e["fin"] <= len(source)
                and source[e["debut"]:e["fin"]] == e["valeur"]):
            justes += 1
    return {"justes": justes, "total": total,
            "taux": round(justes / total, 4) if total else 0.0}


def mesurer_annotation_v2(a: bl.Annotation, source: str,
                          gold: dict | None = None) -> dict:
    """La restitution v2 d'une annotation : rôles lisibles, fidélité et contrôles."""
    if a.refus:
        return {
            "langue": a.langue,
            "refus": a.refus,
            "source_caracteres": len(source),
            "roles": None,
            "comparaison": None,
            "comparaison_stricte": None,
            "constant_par_type": None,
            "vide": None,
            "melange": None,
            "rendu": None,
            "controle_negatif_rendu": None,
            "spans_dans_source": None,
        }
    rendu = rendre_roles(a)
    principal = rendu["principal"]
    variantes = (gold or {}).get("variantes") or []
    comparaison = comparer_cadre(principal, variantes) if variantes else None
    stricte = comparer_cadre(principal, variantes[:1]) if variantes else None
    relu = relire_roles(rendu["lisible"])
    rendu_juste = all(_canonique(relu.get(r, "")) == _canonique(principal.get(r, ""))
                      for r in ROLES)
    return {
        "langue": a.langue,
        "refus": "",
        "source_caracteres": len(source),
        "roles": rendu,
        "comparaison": comparaison,
        "comparaison_stricte": stricte,
        "constant_par_type": (comparer_cadre(_cadre_constant_par_type(a), variantes)
                              if variantes else None),
        "vide": (comparer_cadre({"agent": "", "predicat": "", "lieu": ""}, variantes)
                 if variantes else None),
        "melange": (comparer_cadre(melanger_roles(principal), variantes)
                    if variantes else None),
        "rendu": {"exact": rendu_juste, "relu": relu,
                  "principal": principal, "definition": "relire_roles(rendre_roles(a))"},
        "controle_negatif_rendu": controler_negatif_rendu(rendu),
        "spans_dans_source": _dans_source(a, source),
    }


def _moyenne(valeurs: list[float]) -> float:
    return round(sum(valeurs) / max(1, len(valeurs)), 4)


def _taux(a: int, b: int) -> float:
    return round(a / b, 4) if b else 0.0


def _agreger_comparaisons(comparaisons: list[dict]) -> dict:
    par_role = {
        role: {"exacts": 0, "attendus": 0, "predits": 0,
               "justes": 0, "faux_positifs": 0, "faux_negatifs": 0,
               "vrais_negatifs": 0}
        for role in ROLES
    }
    for c in comparaisons:
        for role in ROLES:
            x = c["par_role"][role]
            p = par_role[role]
            p["exacts"] += int(x["egal"])
            p["attendus"] += int(bool(x["attendu"]))
            p["predits"] += int(bool(x["predit"]))
            p["justes"] += int(x["juste"])
            p["faux_positifs"] += int(x["faux_positif"])
            p["faux_negatifs"] += int(x["faux_negatif"])
            p["vrais_negatifs"] += int(x["vrai_negatif"])
    for role, p in par_role.items():
        p["taux_exact"] = _taux(p["exacts"], len(comparaisons))
        p["precision"] = _taux(p["justes"], p["predits"])
        p["rappel"] = _taux(p["justes"], p["attendus"])
        p["f1"] = (round(2 * p["precision"] * p["rappel"]
                         / (p["precision"] + p["rappel"]), 4)
                   if p["precision"] + p["rappel"] else 0.0)
    exacts = sum(c["exacts"] for c in comparaisons)
    justes = sum(c["justes"] for c in comparaisons)
    attendus = sum(c["attendus"] for c in comparaisons)
    predits = sum(c["predits"] for c in comparaisons)
    precision = _taux(justes, predits)
    rappel = _taux(justes, attendus)
    f1 = (round(2 * precision * rappel / (precision + rappel), 4)
          if precision + rappel else 0.0)
    return {
        "exacts": exacts,
        "total": 3 * len(comparaisons),
        "taux": _taux(exacts, 3 * len(comparaisons)),
        "cadres_exacts": sum(1 for c in comparaisons if c["exacts"] == 3),
        "cadres_exacts_taux": _taux(
            sum(1 for c in comparaisons if c["exacts"] == 3), len(comparaisons)),
        "cadres_partiels": sum(1 for c in comparaisons if c["exacts"] > 0),
        "justes": justes,
        "attendus": attendus,
        "predits": predits,
        "precision": precision,
        "rappel": rappel,
        "f1": f1,
        "faux_positifs": sum(c["faux_positifs"] for c in comparaisons),
        "faux_negatifs": sum(c["faux_negatifs"] for c in comparaisons),
        "vrais_negatifs": sum(c["vrais_negatifs"] for c in comparaisons),
        "par_role": par_role,
    }


def _variante_de(resultat: dict) -> dict:
    """La variante d'or retenue pour un résultat (celle qui a servi à la comparaison)."""
    variantes = resultat.get("or_variantes") or []
    rang = (resultat.get("comparaison") or {}).get("variante", 0)
    return variantes[rang] if 0 <= rang < len(variantes) else {}


def _agreger_resultats(resultats: list[dict]) -> dict:
    annotes = [r for r in resultats if not r.get("refus")]
    refuses = [r for r in resultats if r.get("refus")]
    n = len(annotes)
    comparaisons = [r["comparaison"] for r in annotes if r.get("comparaison")]
    strictes = [r["comparaison_stricte"] for r in annotes if r.get("comparaison_stricte")]
    constant = [r["constant_par_type"] for r in annotes if r.get("constant_par_type")]
    vides = [r["vide"] for r in annotes if r.get("vide")]
    melanges = [r["melange"] for r in annotes if r.get("melange")]
    n_or = len(comparaisons)
    roles = _agreger_comparaisons(comparaisons)
    compteurs = collections.Counter()
    for r in annotes:
        compteurs.update(r["roles"]["compteurs"])
    return {
        "n": len(resultats),
        "annotations": n,
        "refus": len(refuses),
        "refus_ids": [r.get("id") for r in refuses],
        "or": {
            "textes": n_or,
            "variantes": sum(len(r.get("or_variantes") or []) for r in annotes),
            "roles_attendus": roles["attendus"],
        },
        "cadre": {
            "exacts": sum(1 for c in comparaisons if c["exacts"] == 3),
            "taux": _taux(sum(1 for c in comparaisons if c["exacts"] == 3), n_or),
            "exacts_non_vides": sum(
                1 for r in annotes
                if r.get("comparaison") and r["comparaison"]["exacts"] == 3
                and any(_variante_de(r).get(role) for role in ROLES)),
            "exacts_vides": sum(
                1 for r in annotes
                if r.get("comparaison") and r["comparaison"]["exacts"] == 3
                and not any(_variante_de(r).get(role) for role in ROLES)),
            "partiels": sum(1 for c in comparaisons if c["exacts"] > 0),
            "partiels_taux": _taux(sum(1 for c in comparaisons if c["exacts"] > 0), n_or),
            "exacts_stricts": sum(1 for c in strictes if c["exacts"] == 3),
            "taux_strict": _taux(sum(1 for c in strictes if c["exacts"] == 3), n_or),
            "roles_exacts_moyens": _moyenne([c["exacts"] for c in comparaisons]),
        },
        "or_textes": n_or,
        "roles": roles,
        "couverture": {
            "textes_avec_role": sum(1 for r in annotes if r["roles"]["compteurs"]["segments_role"]),
            "taux_textes_avec_role": _taux(
                sum(1 for r in annotes if r["roles"]["compteurs"]["segments_role"]), n),
            "segments_role": compteurs["segments_role"],
            "agents": compteurs["agents"],
            "predicats": compteurs["predicats"],
            "lieux": compteurs["lieux"],
            "cadres": compteurs["cadres"],
        },
        "controles": {
            "vide": _agreger_comparaisons(vides),
            "constant_par_type": _agreger_comparaisons(constant),
            "roles_melanges": _agreger_comparaisons(melanges),
            "rendu": {
                "exacts": sum(1 for r in annotes if r["rendu"]["exact"]),
                "taux": _taux(sum(1 for r in annotes if r["rendu"]["exact"]), n),
            },
            "negatif_rendu": {
                "eligibles": sum(1 for r in annotes
                                 if r["controle_negatif_rendu"]["eligible"]),
                "sans_predicat": sum(1 for r in annotes
                                     if r["controle_negatif_rendu"]["sans_predicat"]["change"]),
                "permute": sum(1 for r in annotes
                               if r["controle_negatif_rendu"]["permute"]["change"]),
                "detectes": sum(1 for r in annotes
                                if r["controle_negatif_rendu"]["detecte"]),
            },
            "spans_dans_source": {
                "justes": sum(r["spans_dans_source"]["justes"] for r in annotes),
                "total": sum(r["spans_dans_source"]["total"] for r in annotes),
                "taux": _taux(sum(r["spans_dans_source"]["justes"] for r in annotes),
                              sum(r["spans_dans_source"]["total"] for r in annotes)),
            },
        },
    }


def mesurer_banc_v2(items: list[dict], gold: dict,
                    langue: str | None = None) -> dict:
    """Mesure la v2 sur les textes d'un banc et l'or de rôles (`gold["textes"]`).

    `langue=None` laisse le bloc détecter, comme la v0 (`restitution.mesurer_banc`) : sans
    cela, les 46 textes ne seraient pas mesurés dans les mêmes conditions que la fiche v0.
    """
    par_id = {g["id"]: g for g in gold.get("textes", [])}
    h = bl.Heuristique()
    resultats = []
    for item in items:
        texte = item.get("texte", "")
        ident = item.get("id", f"t{len(resultats) + 1:02d}")
        a = h.analyser(texte, langue)
        if a.refus:
            resultats.append({
                "id": ident, "refus": a.refus, "caracteres": len(texte),
                "langue": a.langue,
            })
            continue
        attendu = par_id.get(ident)
        m = mesurer_annotation_v2(a, texte, attendu)
        resultats.append({
            "id": ident,
            "refus": "",
            "langue": a.langue,
            "caracteres": len(texte),
            "or_variantes": (attendu or {}).get("variantes"),
            "roles": m["roles"],
            "comparaison": m["comparaison"],
            "comparaison_stricte": m["comparaison_stricte"],
            "constant_par_type": m["constant_par_type"],
            "vide": m["vide"],
            "melange": m["melange"],
            "rendu": m["rendu"],
            "controle_negatif_rendu": m["controle_negatif_rendu"],
            "spans_dans_source": m["spans_dans_source"],
        })
    return {
        "schema": SCHEMA_BANC,
        "version": VERSION,
        "definition": ("rôles (agent, prédicat, lieu) lus depuis les syntagmes ; cadre "
                       "principal ; fidélité comparée à l'or écrit à la main"),
        "parametres": {"langue": langue or "auto", "roles": list(ROLES)},
        "synthese": _agreger_resultats(resultats),
        "resultats": resultats,
    }


# --------------------------------------------------------------------------- affichage


def formater_mesure_v2(m: dict, source: str) -> str:
    """La sortie lisible de `drave restituer TEXTE --roles`."""
    if m.get("refus"):
        return f"refus d'analyse : {m['refus']} (aucun rôle à restituer)"
    rendu = m["roles"]
    p = rendu["principal"]
    lignes = [
        "restitution v2 (rôles)",
        f"source          : {source!r}",
        "cadre principal :",
        f"  agent         : {_valeur_ou_vide(p['agent'])}",
        f"  prédicat      : {_valeur_ou_vide(p['predicat'])}",
        f"  lieu          : {_valeur_ou_vide(p['lieu'])}",
        f"segments de rôle: {rendu['compteurs']['segments_role']} "
        f"({rendu['compteurs']['agents']} agents, {rendu['compteurs']['predicats']} "
        f"prédicats, {rendu['compteurs']['lieux']} lieux)",
        "",
        rendu["lisible"],
        "",
        "restitution du rendu : " + ("exacte" if m["rendu"]["exact"] else "non exacte")
        + " (relire_roles(rendre_roles(a)))",
    ]
    if m.get("comparaison"):
        c = m["comparaison"]
        lignes.append(
            f"fidélité à l'or       : {c['exacts']}/3 rôles exacts, "
            f"{c['justes']}/{c['attendus']} justes, {c['faux_positifs']} faux positifs, "
            f"{c['faux_negatifs']} faux négatifs (variante {c['variante']})")
    neg = m["controle_negatif_rendu"]
    lignes.append(
        f"contrôle négatif      : retrait {'détecté' if neg['sans_predicat']['change'] else 'non détecté'} "
        f"· permutation {'détectée' if neg['permute']['change'] else 'non détectée'} "
        f"· détecté {neg['detecte']}")
    return "\n".join(lignes)


def formater_banc_v2(rapport: dict, chemin: str = "") -> str:
    """La sortie lisible du banc v2 (`restituer --banc ... --roles`)."""
    s = rapport["synthese"]
    n = s["annotations"]
    n_or = s.get("or_textes", n)
    cadre = s["cadre"]
    roles = s["roles"]
    couv = s["couverture"]
    c = s["controles"]
    lignes = [
        f"restitution v2 — les rôles — banc {chemin or '(fourni)'}",
        f"textes {s['n']} · annotés {n} · refus {s['refus']} "
        f"({', '.join(str(x) for x in s['refus_ids'])})",
        "",
        "cadre principal (agent, prédicat, lieu)",
        f"  cadres exacts            {cadre['exacts']:>6}/{n_or:<6} {cadre['taux']:>8.4f}",
        f"  dont non vides           {cadre['exacts_non_vides']:>6}/{n_or:<6} "
        f"({_taux(cadre['exacts_non_vides'], n_or):.4f}) · vides {cadre['exacts_vides']}",
        f"  cadres partiels          {cadre['partiels']:>6}/{n_or:<6} "
        f"{cadre['partiels_taux']:>8.4f}",
        f"  exacts stricts (1re var.){cadre['exacts_stricts']:>6}/{n_or:<6} "
        f"{cadre['taux_strict']:>8.4f}",
        f"  rôles exacts            {roles['exacts']:>6}/{roles['total']:<6} "
        f"{roles['taux']:>8.4f}",
        f"  justes / attendus       {roles['justes']:>6}/{roles['attendus']:<6}",
    ]
    precision = roles["precision"]
    rappel = roles["rappel"]
    f1 = roles["f1"]
    lignes.extend([
        f"  précision / rappel / F1 {precision:.4f} / {rappel:.4f} / {f1:.4f}",
        f"  faux positifs / négatifs {roles['faux_positifs']} / {roles['faux_negatifs']}",
        "",
        "par rôle                  exacts    attendus   prédits   justes   préc.   rappel",
    ])
    for role in ROLES:
        p = roles["par_role"][role]
        lignes.append(
            f"  {LIBELLES[role]:<22} {p['exacts']:>5}/{n_or:<5} {p['attendus']:>7} "
            f"{p['predits']:>9} {p['justes']:>8} {p['precision']:>7.4f} {p['rappel']:>8.4f}")
    lignes.extend([
        "",
        f"segments de rôle {couv['segments_role']} · agents {couv['agents']} · "
        f"prédicats {couv['predicats']} · lieux {couv['lieux']} · cadres {couv['cadres']}",
        f"textes avec au moins un rôle : {couv['textes_avec_role']}/{n} "
        f"({couv['taux_textes_avec_role']:.4f})",
        f"spans de rôle dans la source : {c['spans_dans_source']['justes']}/"
        f"{c['spans_dans_source']['total']} ({c['spans_dans_source']['taux']:.4f})",
        "",
        f"contrôle vide            : {c['vide']['exacts']}/{3 * n_or} rôles exacts · "
        f"cadres exacts {c['vide']['cadres_exacts']}/{n_or}",
        f"contrôle constant (type) : {c['constant_par_type']['exacts']}/{3 * n_or} rôles exacts "
        f"· cadres exacts {c['constant_par_type']['cadres_exacts']}/{n_or}",
        f"contrôle rôles mélangés  : {c['roles_melanges']['exacts']}/{3 * n_or} rôles exacts "
        f"· cadres exacts {c['roles_melanges']['cadres_exacts']}/{n_or}",
        f"restitution du rendu     : {c['rendu']['exacts']}/{n} ({c['rendu']['taux']:.4f})",
        f"contrôle négatif rendu   : {c['negatif_rendu']['detectes']}/"
        f"{c['negatif_rendu']['eligibles']} éligibles détectés",
    ])
    return "\n".join(lignes)


# --------------------------------------------------------------------------- gold externe


ROLE_CONSTANT = {"GN": "agent", "GV": "predicat", "GP": "lieu",
                 "SUB": "contenu", "REL": "qualite"}
GOLD_ANALYSEUR = RACINE / "tools" / "structures" / "donnees" / "gold-analyseur.json"


def _spans_gold(phrase: dict) -> list[dict]:
    curseur, spans = 0, []
    for texte, type_, role in phrase.get("attendus", []):
        debut = phrase["texte"].find(texte, curseur)
        if debut < 0:
            raise ValueError(f"{phrase.get('id')} : segment introuvable {texte!r}")
        spans.append({"debut": debut, "fin": debut + len(texte), "texte": texte,
                      "type": type_, "role": role})
        curseur = debut + len(texte)
    return spans


def mesurer_gold_analyseur(chemin: pathlib.Path | None = None) -> dict:
    """Le **contrôle externe** : le lecteur de rôles v2 sur le gold S de 61 phrases.

    Ce n'est pas le banc v0 : c'est un gold de rôles **écrit avant** la v2 (le gold de
    l'analyseur S, 144 rôles). Il sert à montrer que la lecture des rôles n'est pas cassée
    quand l'or est propre ; l'écart avec les 46 textes v0 mesure la difficulté du banc,
    pas la qualité du code.
    """
    chemin = chemin or GOLD_ANALYSEUR
    donnees = json.loads(chemin.read_text(encoding="utf-8"))
    h = bl.Heuristique()
    justes = total = base_justes = 0
    par_type = collections.Counter()
    for phrase in donnees.get("phrases", []):
        a = h.analyser(phrase["texte"])
        if a.refus:
            continue
        segments = _segments_syntagmes(a)
        pris: set[int] = set()
        for attendu in _spans_gold(phrase):
            total += 1
            par_type[attendu["type"]] += 1
            meilleur = None
            for i, seg in enumerate(segments):
                if i in pris or seg["type"] != attendu["type"]:
                    continue
                inter = min(attendu["fin"], seg["fin"]) - max(attendu["debut"], seg["debut"])
                if inter > 0 and (meilleur is None or inter > meilleur[0]):
                    meilleur = (inter, i, seg)
            if meilleur is not None:
                pris.add(meilleur[1])
                if normaliser_role(meilleur[2]["role"]) == normaliser_role(attendu["role"]):
                    justes += 1
            if normaliser_role(ROLE_CONSTANT.get(attendu["type"], "")) == normaliser_role(
                    attendu["role"]):
                base_justes += 1
    return {
        "or": str(chemin.relative_to(RACINE)),
        "phrases": len(donnees.get("phrases", [])),
        "roles_justes": justes,
        "roles_total": total,
        "taux": _taux(justes, total),
        "baseline_role_constant": {"justes": base_justes, "total": total,
                                   "taux": _taux(base_justes, total)},
        "par_type": dict(sorted(par_type.items())),
        "definition": ("appariement par recouvrement maximal à type égal, puis comparaison "
                       "du rôle normalisé (prédicat/predicat)"),
    }

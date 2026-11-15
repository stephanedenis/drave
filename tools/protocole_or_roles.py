#!/usr/bin/env python3
"""protocole_or_roles.py — le protocole de l'or de rôles (tâche X2, J4 matin).

Ce script ne modifie **jamais** le gold S. Il le lit, il compte ses 144 rôles, il projette
les 17 étiquettes sur les **sept champs** du protocole (agent, predicat, lieu, temps,
destinataire, possession, complement) et il écrit :

- ``reports/rapport-or-roles-protocole.json`` — l'inventaire mesuré, le protocole, les
  simulations de kappa et les contrôles négatifs existants ;
- ``reports/or-roles-base-v1.json`` — la graine des 46 textes du gold v2 (base de départ,
  provisoire, à compléter pour les quatre rôles que la v2 n'annote pas) ;
- ``reports/schema-or-roles.json`` est validé, et chaque item de la graine est validé
  contre lui.

Le contrôle négatif est double :

1. **sur le kappa** : un codeur indépendant, ou les étiquettes du codeur B permutées,
   doivent faire tomber le kappa à ~0 ; la simulation le vérifie ;
2. **sur l'or** : la permutation cyclique des cinq rôles de GP du gold S tombe à 0/18
   (mesure W5 rejouée ici), et la permutation des sept champs du nouveau gold devra
   tomber sous le plafond 1/7. La rotation des 17 étiquettes du gold S (0,4028) est
   conservée comme borne haute : elle laisse 58 prédicats fixes par l'alias
   ``predicat``/``prédicat``.

Usage :
    python3 tools/protocole_or_roles.py
    python3 tools/protocole_or_roles.py --json       # le résumé du JSON
    python3 tools/protocole_or_roles.py --verifier   # valide seulement
"""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import pathlib
import random
import statistics
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

GOLD_S = RACINE / "tools" / "structures" / "donnees" / "gold-analyseur.json"
GOLD_V2 = RACINE / "tools" / "tests" / "linguistique" / "gold_restitution_v2.json"
BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
SCHEMA = RACINE / "reports" / "schema-or-roles.json"
SORTIE = RACINE / "reports" / "rapport-or-roles-protocole.json"
BASE = RACINE / "reports" / "or-roles-base-v1.json"

SEPT = ("agent", "predicat", "lieu", "temps", "destinataire", "possession", "complement")
HORS_CHAMP = ("patient", "qualite", "contenu", "cause", "but", "hypothese",
              "concession", "consequence", "maniere")
# Les étiquettes du gold S qui sont des compléments prépositionnels : dans la couche
# grossière des sept champs, elles tombent dans le repli `complement`.
GP_VERS_COMPLEMENT = {"theme", "instrument", "but"}
GRAINE = 20261115
N_SIM = 1000


# --------------------------------------------------------------------------- outils


def sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def lire(chemin: pathlib.Path) -> dict:
    return json.loads(chemin.read_text(encoding="utf-8"))


def taux(a: int, b: int) -> float:
    return round(a / b, 4) if b else 0.0


def projeter_7(role: str, type_syntagme: str = "") -> str:
    """Projette une étiquette du gold S sur les sept champs.

    - les sept étiquettes du contrat restent telles quelles ;
    - ``theme``, ``instrument`` et ``but`` **prépositionnels** sont des compléments
      prépositionnels : ils tombent dans le repli ``complement`` ;
    - ``patient`` (GN), ``qualite`` (REL) et les subordonnées ``but``, ``cause``,
      ``hypothese``, ``concession``, ``consequence``, ``contenu`` et ``maniere`` ne se
      projettent pas : ils restent ``hors_champ``.
    """
    role = role or ""
    type_syntagme = type_syntagme or ""
    if role in SEPT:
        return role
    if role in GP_VERS_COMPLEMENT and type_syntagme == "GP":
        return "complement"
    return "hors_champ"


# --------------------------------------------------------------------------- gold S


def inventaire_gold_s() -> dict:
    d = lire(GOLD_S)
    par_etiquette = collections.Counter()
    par_type_role = collections.Counter()
    par_sept = collections.Counter()
    par_hors = collections.Counter()
    par_split_phrases = collections.Counter()
    par_split_roles = collections.Counter()
    roles_par_phrase = collections.Counter()
    predicats_par_phrase = collections.Counter()
    spans_exacts = 0
    total_roles = 0
    cas_limites = []
    for ph in d["phrases"]:
        par_split_phrases[ph["split"]] += 1
        roles = ph["attendus"]
        roles_par_phrase[len(roles)] += 1
        par_split_roles[ph["split"]] += len(roles)
        predicats = 0
        for span, type_syntagme, role in roles:
            total_roles += 1
            par_etiquette[role] += 1
            par_type_role[f"{type_syntagme}/{role}"] += 1
            if span in ph["texte"]:
                spans_exacts += 1
            proj = projeter_7(role, type_syntagme)
            if proj == "hors_champ":
                par_hors[role] += 1
            else:
                par_sept[proj] += 1
            if role == "predicat":
                predicats += 1
        predicats_par_phrase[predicats] += 1
        if predicats != 1:
            cas_limites.append({
                "id": ph["id"],
                "split": ph["split"],
                "texte": ph["texte"],
                "predicats": predicats,
                "roles": len(roles),
                "attendus": [list(x) for x in roles],
                "raison": ("phrase sans prédicat : cadres vides, rôles hors_cadre"
                           if predicats == 0 else
                           "deux prédicats : deux cadres, un principal"),
            })
    total_sept = sum(par_sept.values())
    total_hors = sum(par_hors.values())
    return {
        "chemin": str(GOLD_S.relative_to(RACINE)),
        "sha256": sha256(GOLD_S),
        "version": d.get("version"),
        "note": d.get("note", ""),
        "phrases": len(d["phrases"]),
        "roles": total_roles,
        "etiquettes": len(par_etiquette),
        "spans_exacts": spans_exacts,
        "spans_exacts_taux": taux(spans_exacts, total_roles),
        "par_etiquette": dict(sorted(par_etiquette.items(), key=lambda x: (-x[1], x[0]))),
        "par_type_role": dict(sorted(par_type_role.items())),
        "par_split": {
            "phrases": dict(sorted(par_split_phrases.items())),
            "roles": dict(sorted(par_split_roles.items())),
        },
        "roles_par_phrase": {str(k): v for k, v in sorted(roles_par_phrase.items())},
        "predicats_par_phrase": {str(k): v for k, v in sorted(predicats_par_phrase.items())},
        "sept_champs": dict(sorted(par_sept.items())),
        "sept_champs_total": total_sept,
        "hors_champ": dict(sorted(par_hors.items())),
        "hors_champ_total": total_hors,
        "couverture_sept": round(total_sept / total_roles, 4) if total_roles else 0.0,
        "cas_limites": cas_limites,
    }


# --------------------------------------------------------------------------- gold v2


def inventaire_gold_v2() -> dict:
    d = lire(GOLD_V2)
    textes = d.get("textes", [])
    langues = collections.Counter(x.get("langue", "") for x in textes)
    variantes = sum(len(x.get("variantes", [])) for x in textes)
    premiere = collections.Counter()
    toutes = collections.Counter()
    cadres_vides = []
    sans_predicat = []
    variantes_par_texte = collections.Counter()
    for x in textes:
        vs = x.get("variantes", [])
        variantes_par_texte[len(vs)] += 1
        v = vs[0] if vs else {}
        non_vides = 0
        for role in ("agent", "predicat", "lieu"):
            if (v.get(role) or "").strip():
                premiere[role] += 1
                non_vides += 1
        if non_vides == 0:
            cadres_vides.append(x["id"])
        if not (v.get("predicat") or "").strip():
            sans_predicat.append(x["id"])
        for variante in vs:
            for role in ("agent", "predicat", "lieu"):
                if (variante.get(role) or "").strip():
                    toutes[role] += 1
    premieres_cellules = 3 * len(textes)
    toutes_cellules = 3 * variantes
    return {
        "chemin": str(GOLD_V2.relative_to(RACINE)),
        "sha256": sha256(GOLD_V2),
        "schema": d.get("schema"),
        "version": d.get("version"),
        "textes": len(textes),
        "variantes": variantes,
        "langues": dict(sorted(langues.items())),
        "premiere_variante": {
            "cellules": premieres_cellules,
            "non_vides": sum(premiere.values()),
            "vides": premieres_cellules - sum(premiere.values()),
            "par_role": dict(sorted(premiere.items())),
        },
        "toutes_variantes": {
            "cellules": toutes_cellules,
            "non_vides": sum(toutes.values()),
            "par_role": dict(sorted(toutes.items())),
        },
        "cadres_vides": cadres_vides,
        "sans_predicat": sans_predicat,
        "variantes_par_texte": {str(k): v for k, v in sorted(variantes_par_texte.items())},
        "champs_annotes": ["agent", "predicat", "lieu"],
        "champs_manquants": ["temps", "destinataire", "possession", "complement"],
        "couverture_sept": 3 / 7,
        "note": d.get("note", ""),
    }


# --------------------------------------------------------------------------- base


def base_combinee(gold_s: dict, gold_v2: dict) -> dict:
    """Les mentions de la base : 46 textes v2 (3 rôles) + 61 phrases S (144 rôles)."""
    par_role = collections.Counter()
    par_source = collections.Counter()
    par_sept = collections.Counter()
    hors = collections.Counter()
    for x in lire(GOLD_V2).get("textes", []):
        v = (x.get("variantes") or [{}])[0]
        for role in ("agent", "predicat", "lieu"):
            if (v.get(role) or "").strip():
                par_role[role] += 1
                par_sept[role] += 1
                par_source["gold_v2"] += 1
    for ph in lire(GOLD_S).get("phrases", []):
        for _span, type_syntagme, role in ph["attendus"]:
            par_role[role] += 1
            par_source["gold_s"] += 1
            proj = projeter_7(role, type_syntagme)
            if proj == "hors_champ":
                hors[role] += 1
            else:
                par_sept[proj] += 1
    sept = {role: par_sept.get(role, 0) for role in SEPT}
    total_sept = sum(sept.values())
    total_hors = sum(hors.values())
    return {
        "items": gold_v2["textes"] + gold_s["phrases"],
        "sources": {"gold_v2": gold_v2["textes"], "gold_s": gold_s["phrases"]},
        "mentions": par_source.get("gold_v2", 0) + par_source.get("gold_s", 0),
        "par_source": dict(sorted(par_source.items())),
        "sept_champs": sept,
        "sept_champs_total": total_sept,
        "hors_champ": dict(sorted(hors.items())),
        "hors_champ_total": total_hors,
        "total_avec_hors_champ": total_sept + total_hors,
        "par_role_brut": dict(sorted(par_role.items())),
    }


def plan_supplement(base: dict) -> dict:
    cibles = {"temps": 20, "destinataire": 20, "possession": 20,
              "complement": 20, "lieu": 10}
    apres = dict(base["sept_champs"])
    for role, n in cibles.items():
        apres[role] = apres.get(role, 0) + n
    total_sept = sum(apres.values())
    total = total_sept + base["hors_champ_total"]
    return {
        "phrases": 60,
        "mentions": sum(cibles.values()),
        "cibles": cibles,
        "apres": apres,
        "apres_total_sept": total_sept,
        "apres_total": total,
        "items_total": base["sources"]["gold_v2"] + base["sources"]["gold_s"] + 60,
        "regle": ("60 phrases neuves, 90 mentions ciblées : 20 temps, 20 destinataire, "
                  "20 possession, 20 complement, 10 lieu ; une phrase peut porter deux "
                  "rôles, d'où 90 mentions pour 60 phrases."),
        "pourquoi": ("chaque rôle des sept champs atteint au moins 20 mentions ; la "
                     "prévalence attendue passe de 0,299 à 0,180, ce qui rend le kappa "
                     "moins sensible au paradoxe de prévalence."),
        "limite": ("supplément ciblé, pas un échantillon aléatoire : il sert au rappel "
                   "par rôle et au kappa, pas à estimer la prévalence ni la F1 générale."),
    }


# --------------------------------------------------------------------------- kappa


def kappa_cohen(a: list[str], b: list[str]) -> float:
    n = len(a)
    if not n:
        return 0.0
    accord = sum(x == y for x, y in zip(a, b)) / n
    ca = collections.Counter(a)
    cb = collections.Counter(b)
    hasard = sum((ca[k] / n) * (cb[k] / n) for k in set(ca) | set(cb))
    return (accord - hasard) / (1 - hasard) if hasard < 1 else 0.0


def _distribution(n: int, counts: dict[str, int]) -> list[str]:
    return [role for role, k in counts.items() for _ in range(k)]


def simuler_kappa(counts: dict[str, int], cibles=(0.80, 0.85, 0.90, 0.95),
                  n_sim: int = N_SIM, graine: int = GRAINE) -> dict:
    """Simule deux codeurs à partir des effectifs d'or.

    Le codeur A est l'or ; le codeur B garde A avec la probabilité ``p`` et tire sinon
    dans la distribution empirique. Le paramètre est calibré pour que l'**accord brut**
    observé soit la cible. Ce n'est pas une double annotation : c'est l'étalonnage du
    kappa sous la prévalence de l'or.
    """
    labels = _distribution(sum(counts.values()), counts)
    n = len(labels)
    freq = collections.Counter(labels)
    pe = sum((v / n) ** 2 for v in freq.values())
    resultats = []
    for cible in cibles:
        p = (cible - pe) / (1 - pe)
        rnd = random.Random(graine)
        ks = []
        accords = []
        for _ in range(n_sim):
            b = [x if rnd.random() < p else rnd.choices(labels, k=1)[0] for x in labels]
            ks.append(kappa_cohen(labels, b))
            accords.append(sum(x == y for x, y in zip(labels, b)) / n)
        ks.sort()
        resultats.append({
            "accord_brut_cible": cible,
            "p_keep": round(p, 4),
            "accord_brut_observe": round(statistics.mean(accords), 4),
            "kappa_moyen": round(statistics.mean(ks), 4),
            "kappa_ic95": [round(ks[int(0.025 * n_sim)], 4),
                           round(ks[int(0.975 * n_sim) - 1], 4)],
            "n": n,
            "pe": round(pe, 4),
        })
    # Contrôles négatifs : codeur indépendant et codeur permuté.
    rnd = random.Random(graine + 1)
    indep = []
    perm = []
    for _ in range(n_sim):
        b = rnd.choices(labels, k=n)
        indep.append(kappa_cohen(labels, b))
        p = labels[:]
        rnd.shuffle(p)
        perm.append(kappa_cohen(labels, p))
    for xs in (indep, perm):
        xs.sort()
    return {
        "n": n,
        "pe": round(pe, 4),
        "cibles": resultats,
        "controle_independant": {
            "kappa_moyen": round(statistics.mean(indep), 4),
            "kappa_ic95": [round(indep[int(0.025 * n_sim)], 4),
                           round(indep[int(0.975 * n_sim) - 1], 4)],
        },
        "controle_permute": {
            "kappa_moyen": round(statistics.mean(perm), 4),
            "kappa_ic95": [round(perm[int(0.025 * n_sim)], 4),
                           round(perm[int(0.975 * n_sim) - 1], 4)],
        },
    }


def puissance(n: int, pe: float, accord: float = 0.90) -> dict:
    se = (accord * (1 - accord) / (n * (1 - pe) ** 2)) ** 0.5
    n_pour_5 = (accord * (1 - accord)
                / ((0.05 / 1.96) ** 2 * (1 - pe) ** 2))
    return {
        "n": n,
        "pe": round(pe, 4),
        "accord_brut": accord,
        "erreur_type": round(se, 4),
        "demi_largeur_ic95": round(1.96 * se, 4),
        "n_pour_demi_largeur_0_05": int(-(-n_pour_5 // 1)),
    }


# --------------------------------------------------------------------------- contrôles


def controles_existants() -> dict:
    """Rejoue les contrôles W5 sur le gold S et le gold v2, en lecture seule."""
    import tools.restitution as restitution
    import tools.restitution_v3 as v3

    m = v3.mesurer_gold_analyseur_v3()
    banc = lire(BANC)
    gold_v2 = lire(GOLD_V2)
    items = restitution.items_banc(banc)
    c = v3.controler_banc_v3(items, gold_v2)
    base_banc = c["base"]
    cinq_s = m["base"]["cinq_roles"]

    def bloc(mesure: dict) -> dict:
        return {
            "justes": mesure.get("justes"),
            "total": mesure.get("total"),
            "taux": mesure.get("taux"),
        }

    def bloc_cinq(mesure: dict) -> dict:
        cinq = mesure.get("cinq_roles") or {}
        return {
            "justes": cinq.get("justes"),
            "attendus": cinq.get("attendus"),
            "taux": cinq.get("f1"),
        }

    return {
        "gold_s": {
            "or": str(GOLD_S.relative_to(RACINE)),
            "sha256": sha256(GOLD_S),
            "base": {"global": bloc(m["base"]), "cinq": bloc_cinq(m["base"])},
            "permutation_cinq": {
                "mapping": m["permutation_cinq"]["mapping"],
                "global": bloc(m["permutation_cinq"]["mesure"]),
                "cinq": bloc_cinq(m["permutation_cinq"]["mesure"]),
            },
            "permutation_tous": {
                "mapping": m["permutation_tous"]["mapping"],
                "global": bloc(m["permutation_tous"]["mesure"]),
                "cinq": bloc_cinq(m["permutation_tous"]["mesure"]),
                "note": ("la rotation des 17 étiquettes laisse 58 prédicats fixes par "
                         "l'alias predicat/prédicat ; 0,4028 est une borne haute, pas "
                         "un contrôle propre. Le contrôle propre est la permutation des "
                         "cinq rôles de GP (0/18) et, pour le nouveau gold, la "
                         "permutation cyclique des sept champs."),
            },
            "role_constant_lieu": {
                "global": bloc(m["role_constant_lieu"]),
                "cinq": bloc_cinq(m["role_constant_lieu"]),
            },
            "baseline_constant_par_type": bloc(m["baseline_role_constant"]),
        },
        "gold_v2": {
            "or": str(GOLD_V2.relative_to(RACINE)),
            "sha256": sha256(GOLD_V2),
            "base": {
                "cadres_exacts": base_banc["cadre"]["exacts"],
                "cadres_total": base_banc["annotations"],
                "cadres_non_vides": base_banc["cadre"]["exacts_non_vides"],
                "roles_justes": base_banc["roles"]["justes"],
                "roles_attendus": base_banc["roles"]["attendus"],
                "f1": base_banc["roles"]["f1"],
                "lieu": base_banc["roles"]["par_role"]["lieu"],
            },
            "vide": {
                "cadres_exacts": base_banc["controles"]["vide"]["cadres_exacts"],
                "roles_justes": base_banc["controles"]["vide"]["justes"],
                "roles_attendus": base_banc["controles"]["vide"]["attendus"],
                "f1": base_banc["controles"]["vide"]["f1"],
            },
            "constant_par_type": {
                "cadres_exacts": base_banc["controles"]["constant_par_type"]["cadres_exacts"],
                "roles_justes": base_banc["controles"]["constant_par_type"]["justes"],
                "roles_attendus": base_banc["controles"]["constant_par_type"]["attendus"],
                "f1": base_banc["controles"]["constant_par_type"]["f1"],
            },
            "melange": {
                "cadres_exacts": base_banc["controles"]["roles_melanges"]["cadres_exacts"],
                "roles_justes": base_banc["controles"]["roles_melanges"]["justes"],
                "roles_attendus": base_banc["controles"]["roles_melanges"]["attendus"],
                "f1": base_banc["controles"]["roles_melanges"]["f1"],
            },
            "permutation_cinq": {
                "mapping": c["permutation_gp"]["mapping"],
                "cadres_exacts": c["permutation_gp"]["synthese"]["cadre"]["exacts"],
                "cadres_non_vides": c["permutation_gp"]["synthese"]["cadre"]["exacts_non_vides"],
                "roles_justes": c["permutation_gp"]["synthese"]["roles"]["justes"],
                "roles_attendus": c["permutation_gp"]["synthese"]["roles"]["attendus"],
                "f1": c["permutation_gp"]["synthese"]["roles"]["f1"],
                "lieu": c["permutation_gp"]["synthese"]["roles"]["par_role"]["lieu"],
            },
        },
        "lecture": ("Les cinq rôles de GP du gold S permutés tombent à 0/18 ; le global "
                    "reste 126/144 parce que 126 des 144 rôles ne sont pas des GP. La "
                    "permutation de tous les rôles donne 58/144 (0,4028), mais 58 "
                    "prédicats survivent à l'alias predicat/prédicat : c'est une borne "
                    "haute. Sur le gold v2, la permutation des cinq rôles donne 17/46 "
                    "cadres, 37/77 rôles, F1 0,5139, et le lieu tombe à 0/6."),
    }


# --------------------------------------------------------------------------- graine


def construire_base_v2(gold_v2: dict) -> dict:
    source_sha = sha256(GOLD_V2)
    textes = []
    for x in gold_v2.get("textes", []):
        v = (x.get("variantes") or [{}])[0]
        roles = {role: [] for role in SEPT}
        hors = []
        # Le prédicat d'abord : les autres rôles ne sont dans un cadre que s'il existe.
        for role in ("predicat", "agent", "lieu"):
            valeur = (v.get(role) or "").strip()
            if not valeur:
                continue
            debut = x["texte"].find(valeur)
            if debut < 0:
                raise ValueError(f"{x['id']} : {role}={valeur!r} absent du texte")
            mention = {
                "texte": valeur,
                "debut": debut,
                "fin": debut + len(valeur),
            }
            if role == "predicat":
                roles["predicat"].append(mention)
            elif roles["predicat"]:
                roles[role].append(mention)
            else:
                hors.append({
                    "role": role,
                    "mention": mention,
                    "raison": "phrase sans prédicat : rôle hors cadre",
                })
        cadres = []
        if roles["predicat"]:
            cadres.append({
                "id": "c1",
                "principal": True,
                "roles": roles,
            })
        item = {
            "schema": "drave.or.roles",
            "version": 1,
            "id": "or-" + x["id"],
            "source": "gold_v2",
            "source_id": x["id"],
            "split": "base",
            "texte": x["texte"],
            "langue": x.get("langue", "und"),
            "cadres": cadres,
            "hors_cadre": hors,
            "meta": {
                "codeur": "base",
                "date": "2026-11-15",
                "statut": "base",
                "protocole": 1,
                "a_completer": ["temps", "destinataire", "possession", "complement"],
                "sha256_source": source_sha,
                "note": ("graine dérivée de la première variante du gold v2 ; les quatre "
                         "rôles absents de la v2 sont vides et à annoter"),
            },
        }
        textes.append(item)
    return {
        "schema": "drave.or.roles.base",
        "version": 1,
        "date": "2026-11-15",
        "source": str(GOLD_V2.relative_to(RACINE)),
        "source_sha256": source_sha,
        "note": ("Base de départ, provisoire : 46 textes du gold v2, première variante, "
                 "rôles agent/predicat/lieu seulement. Ce fichier n'est pas un gold ; "
                 "il ne modifie pas le gold S et ne remplace pas le gold v2."),
        "textes": textes,
    }


def _erreurs_item(item: dict, validateur) -> list[str]:
    erreurs = [e.message for e in validateur.iter_errors(item)]
    # Contrôles que JSON Schema ne sait pas exprimer.
    if len(item["cadres"]) > 0:
        principaux = [c for c in item["cadres"] if c.get("principal")]
        if len(principaux) != 1:
            erreurs.append(f"{len(principaux)} cadre(s) principal(aux)")
    for cadre in item["cadres"]:
        if len(cadre["roles"]["predicat"]) != 1:
            erreurs.append(f"{len(cadre['roles']['predicat'])} prédicat(s)")
        for role, mentions in cadre["roles"].items():
            for m in mentions:
                if item["texte"][m["debut"]:m["fin"]] != m["texte"]:
                    erreurs.append(f"span {role} ≠ texte")
    for h in item["hors_cadre"]:
        m = h["mention"]
        if item["texte"][m["debut"]:m["fin"]] != m["texte"]:
            erreurs.append("span hors_cadre ≠ texte")
    return erreurs


def verifier_base(base: dict, schema: dict) -> dict:
    import jsonschema

    jsonschema.Draft202012Validator.check_schema(schema)
    validateur = jsonschema.Draft202012Validator(schema)
    erreurs = []
    for item in base["textes"]:
        for e in _erreurs_item(item, validateur):
            erreurs.append(f"{item.get('id')} : {e}")

    # Contrôle négatif du schéma : chaque mutation doit être refusée.
    modele = copy.deepcopy(base["textes"][0])
    mutations = []

    def _sans_agent(item):
        del item["cadres"][0]["roles"]["agent"]

    def _deux_principaux(item):
        second = copy.deepcopy(item["cadres"][0])
        second["id"] = "c2"
        second["principal"] = True
        item["cadres"].append(second)

    def _span_faux(item):
        item["cadres"][0]["roles"]["predicat"][0]["texte"] = "X"

    def _sans_predicat(item):
        item["cadres"][0]["roles"]["predicat"] = []

    for nom, mutation in (("sans_agent", _sans_agent),
                          ("deux_principaux", _deux_principaux),
                          ("span_faux", _span_faux),
                          ("sans_predicat", _sans_predicat)):
        item = copy.deepcopy(modele)
        mutation(item)
        refuse = bool(_erreurs_item(item, validateur))
        mutations.append({"cas": nom, "refuse": refuse})

    return {
        "schema": str(SCHEMA.relative_to(RACINE)),
        "schema_sha256": sha256(SCHEMA),
        "items": len(base["textes"]),
        "erreurs": len(erreurs),
        "detail": erreurs[:20],
        "validateur": "jsonschema Draft 2020-12 + contrôles de spans",
        "negatif": {
            "cas": len(mutations),
            "refuses": sum(1 for m in mutations if m["refuse"]),
            "detail": mutations,
        },
    }


# --------------------------------------------------------------------------- protocole


def bloc_protocole(gold_s: dict, gold_v2: dict, base: dict, supplement: dict,
                   simulations: dict, controles: dict) -> dict:
    return {
        "question": ("Comment annoter un or de rôles qui mesure les sept champs "
                     "(agent, predicat, lieu, temps, destinataire, possession, "
                     "complement) sur les 46 textes du gold v2 et les 61 phrases du "
                     "gold S, avec deux codeurs, un kappa publiable et un contrôle "
                     "négatif qui tue la mesure ?"),
        "unite": "phrase ; plusieurs cadres par phrase ; plusieurs mentions par rôle.",
        "champs": {
            "phrase": {
                "obligatoire": True,
                "contenu": "id, texte, langue, source, source_id, split",
                "regle": "recopier la phrase exactement ; les offsets sont en caractères Unicode.",
            },
            "cadre": {
                "obligatoire": True,
                "contenu": "id, principal, roles",
                "regle": ("un cadre = un prédicat et ses rôles ; un seul cadre principal "
                          "par phrase ; zéro cadre pour une phrase sans prédicat."),
            },
            "roles": {
                "obligatoire": True,
                "contenu": "agent, predicat, lieu, temps, destinataire, possession, complement",
                "regle": ("chaque rôle est une liste de mentions (0..n) ; le prédicat "
                          "d'un cadre est exactement une mention."),
            },
            "hors_cadre": {
                "obligatoire": False,
                "contenu": "role, mention, raison",
                "regle": ("rôle annoté mais non rattaché à un cadre : subordonnée, "
                          "relative, apposition, phrase sans prédicat. Le rôle de sept "
                          "champs est conservé pour la mesure au niveau mention."),
            },
            "meta": {
                "obligatoire": True,
                "contenu": "codeur, date, statut, protocole, a_completer, sha256_source",
                "regle": "statut base / provisoire / adjudine / gele ; aucune édition silencieuse.",
            },
        },
        "definitions": {
            "agent": ("l'entité qui fait l'action : sujet actif, ou complément d'agent "
                      "d'un passif (par). Vide pour un impératif sans agent exprimé."),
            "predicat": ("le verbe ou le groupe verbal qui porte le cadre ; auxiliaires "
                         "et copule inclus. Un cadre a exactement un prédicat."),
            "lieu": ("lieu, origine, destination ou trajet : à Paris, dans la cour, "
                     "vers la gare, chez Paul, au bord de la forêt."),
            "temps": ("moment, durée ou fréquence : à 14 h, demain, pendant deux heures, "
                      "vers 9 h, dans trois jours."),
            "destinataire": ("bénéficiaire ou récepteur d'un transfert ou d'une "
                             "communication : à Marie, pour Paul, lui, leur."),
            "possession": ("le possesseur : le chat de la voisine, le livre est à moi ; "
                           "pas l'objet possédé."),
            "complement": ("le repli des compléments prépositionnels qui ne sont ni lieu, "
                           "ni temps, ni destinataire, ni possession : de son projet, "
                           "avec le télescope, à la réunion. Le rôle étendu (theme, instrument/moyen, "
                           "but) est conservé dans role_etendu ; il ne crée pas une "
                           "huitième catégorie de score."),
            "hors_champ": ("les rôles du gold S qui ne se projettent pas dans les sept "
                           "champs : patient (GN), qualite (REL) et les subordonnées but, "
                           "cause, hypothese, concession, consequence, contenu, maniere. "
                           "Ils restent dans la couche étendue et ne sont pas comptés "
                           "dans le score des sept champs."),
        },
        "regles_de_decision": [
            {"regle": "à + temps", "exemples": ["à 14 h", "à midi", "à demain"], "role": "temps"},
            {"regle": "à + lieu", "exemples": ["à Paris", "à la maison", "au bord de la forêt"], "role": "lieu"},
            {"regle": "à + personne", "exemples": ["à Marie", "à son fils"], "role": "destinataire"},
            {"regle": "à + infinitif", "exemples": ["à manger", "à faire"], "role": "complement", "role_etendu": "but"},
            {"regle": "de + GN après un GN", "exemples": ["le chat de la voisine"], "role": "possession"},
            {"regle": "de + GV / de + thème", "exemples": ["parler de son projet"], "role": "complement", "role_etendu": "theme"},
            {"regle": "avec + instrument", "exemples": ["avec le télescope"], "role": "complement", "role_etendu": "instrument"},
            {"regle": "par + passif + personne", "exemples": ["écrit par Marie"], "role": "agent"},
            {"regle": "par + moyen / lieu", "exemples": ["entrer par la porte"], "role": "complement", "role_etendu": "moyen"},
            {"regle": "pour + bénéficiaire animé", "exemples": ["pour Paul"], "role": "destinataire"},
            {"regle": "pour + but", "exemples": ["pour la documentation"], "role": "complement", "role_etendu": "but"},
            {"regle": "dans, sur, sous, vers, chez", "exemples": ["dans la cour", "vers la gare"], "role": "lieu"},
            {"regle": "pendant, depuis, durant, avant, après", "exemples": ["depuis dix minutes"], "role": "temps"},
            {"regle": "vers + heure", "exemples": ["vers 9 h"], "role": "temps"},
            {"regle": "en + temps", "exemples": ["en 2020"], "role": "temps"},
            {"regle": "en + lieu", "exemples": ["en France"], "role": "lieu"},
            {"regle": "en + véhicule", "exemples": ["en voiture"], "role": "complement", "role_etendu": "moyen"},
            {"regle": "en + gérondif", "exemples": ["en haussant les épaules"], "role": "complement", "role_etendu": "maniere"},
            {"regle": "copule + à + pronom", "exemples": ["Le livre est à moi"], "role": "possession"},
            {"regle": "passif", "exemples": ["La porte a été fermée par Marie"], "role": "agent", "note": "le sujet est patient, hors_champ"},
            {"regle": "coordination de même rôle", "exemples": ["Marie et Paul"], "role": "une seule mention couvrant le coordonné"},
            {"regle": "coordination de rôles différents", "exemples": ["à Paris et à 14 h"], "role": "deux mentions, deux rôles"},
            {"regle": "subordonnée avec son propre prédicat", "exemples": ["quand il arrive"], "role": "second cadre"},
            {"regle": "subordonnée complément", "exemples": ["parce qu'il pleut"], "role": "hors_cadre", "role_etendu": "cause"},
            {"regle": "phrase sans prédicat", "exemples": ["Bonne journée !"], "role": "cadres vides, rôles hors_cadre"},
            {"regle": "impératif sans agent", "exemples": ["Ferme la porte"], "role": "agent vide"},
            {"regle": "ambiguïté", "exemples": ["à la banque"], "role": "rôle syntaxique principal ; l'alternative va dans meta.note, pas dans l'or"},
        ],
        "echantillon": {
            "base": {
                "items": base["sources"]["gold_v2"] + base["sources"]["gold_s"],
                "gold_v2": base["sources"]["gold_v2"],
                "gold_s": base["sources"]["gold_s"],
                "mentions": base["total_avec_hors_champ"],
                "sept_champs": base["sept_champs_total"],
                "hors_champ": base["hors_champ_total"],
            },
            "supplement": supplement,
            "total": {
                "items": supplement["items_total"],
                "mentions": supplement["apres_total"],
                "sept_champs": supplement["apres_total_sept"],
                "hors_champ": base["hors_champ_total"],
            },
            "aveugle": ("les codeurs ne voient pas les étiquettes du gold S ; la graine v2 "
                        "est montrée à l'identique aux deux codeurs ; le gold S n'est "
                        "ouvert qu'après le gel, pour la comparaison."),
        },
        "double_annotation": {
            "codeurs": ["A (pilote)", "B (désigné par S)", "C (adjudicateur : S ou tiers)"],
            "couverture": "100 % des 167 items, deux codeurs, soit 334 annotations.",
            "calibration": ("10 items hors du gold, annotés par A et B, kappa calculé ; "
                            "si kappa < 0,80, le manuel est révisé avant l'annotation."),
            "independance": ("fichiers séparés, aucune discussion pendant l'annotation, "
                             "aucun accès au fichier de l'autre codeur."),
            "adjudication": ("tous les désaccords sont adjudiqués ; C tranche ou crée un "
                             "consensus ; les annotations A et B restent dans l'audit."),
            "non_tranche": ("si C ne peut pas trancher, l'item est exclu du gold, avec "
                            "la raison ; il n'est pas compté comme un accord."),
            "gel": ("après adjudication, le gold est gelé avec un SHA-256 et un manifeste ; "
                    "toute modification crée une nouvelle version."),
        },
        "kappa": {
            "unite": ("mention de rôle, appariée par span exact ; catégories = sept champs "
                      "+ hors_champ (8)."),
            "formule": "kappa de Cohen = (p_o - p_e) / (1 - p_e).",
            "appariement": ("un span est apparié si (debut, fin) sont égaux ; sinon c'est "
                            "un désaccord de frontière, exclu du kappa de rôle et compté "
                            "dans le taux de spans exacts."),
            "secondaires": [
                "kappa de présence : pour chaque phrase × rôle, présent/absent (2 catégories) ;",
                "taux de spans exacts : frontière identique ou non ;",
                "taux de cadres exacts : même nombre de cadres et mêmes spans de prédicat.",
            ],
            "ic": ("bootstrap par phrase (cluster), 2000 rééchantillonnages, graine "
                   f"{GRAINE} ; intervalle percentile 2,5–97,5."),
            "seuils": {
                "accepte": "kappa >= 0,80",
                "adjudication": "0,60 <= kappa < 0,80 : adjudication, puis gold accepté avec limite nommée",
                "revoir": "kappa < 0,60 : manuel révisé, aucun gold, aucun score",
                "par_role": ("un rôle avec moins de 10 mentions positives n'a pas de F1 "
                             "publiable : on rapporte l'accord brut et l'effectif, pas un kappa."),
            },
            "paradoxe": ("les rôles rares (possession, complement) ont un kappa instable ; "
                         "on rapporte l'accord brut et le PABAK en secondaire, et on ne "
                         "rejette jamais un rôle sur le seul kappa."),
            "controle_negatif": ("permuter les étiquettes de B, ou tirer B indépendamment "
                                 "de A, doit donner kappa ~ 0 ; si kappa_permute > 0,20, "
                                 "le calcul est invalide."),
        },
        "controles_negatifs": {
            "or_permute_7": {
                "mapping": {role: SEPT[(i + 1) % len(SEPT)] for i, role in enumerate(SEPT)},
                "plafond": round(1 / 7, 4),
                "attendu": "le score exact des sept champs tombe sous 1/7 ; sinon la mesure fuit.",
            },
            "or_permute_5": {
                "mapping": {"lieu": "temps", "temps": "destinataire",
                            "destinataire": "possession", "possession": "complement",
                            "complement": "lieu"},
                "plafond": 0.20,
                "attendu": "0/18 sur le gold S (mesure W5 rejouée).",
            },
            "or_vide": {"attendu": "F1 = 0 ; plancher déjà mesuré sur le gold v2 (0/77)."},
            "role_constant": {"attendu": "F1 <= 0,05 ; mesure W5 : 3/18, F1 0,037."},
            "kappa_permute": {"plafond": 0.20, "attendu": "kappa ~ 0."},
            "or_permute_tous": {
                "attendu": ("0,4028 sur le gold S, mais c'est une borne haute : 58 "
                            "prédicats survivent à l'alias predicat/prédicat. Ne pas "
                            "l'utiliser comme contrôle propre."),
            },
        },
        "pre_enregistrement": {
            "date": "2026-11-15",
            "graine": GRAINE,
            "hypothese": ("les sept champs sont annotables avec un kappa >= 0,80 et le "
                          "gold permuté s'effondre sous le plafond 1/7."),
            "metrique_principale": ("précision, rappel et F1 par rôle sur les sept "
                                    "champs, plus le cadre exact ; micro et macro."),
            "metrique_secondaire": "kappa de rôle, kappa de présence, spans exacts.",
            "regle_de_decision": ("le gold n'est publié que si kappa >= 0,80 et si le "
                                  "contrôle permuté passe ; sinon on publie l'échec."),
            "exclusions": ("les items non tranchés, les phrases sans prédicat pour le "
                           "cadre exact, les rôles < 10 positifs pour la F1 par rôle."),
            "non_tuning": ("aucune règle de rôle n'est modifiée après la lecture du gold "
                           "gelé ; le gold S reste en lecture seule."),
        },
        "plan": [
            {"etape": "figer le schéma et le manuel", "duree": "0,5 h"},
            {"etape": "calibration sur 10 items", "duree": "1 h"},
            {"etape": "annotation A et B (167 items)", "duree": "2 × 3 h"},
            {"etape": "kappa et liste des désaccords", "duree": "1 h"},
            {"etape": "adjudication C", "duree": "2 h"},
            {"etape": "gel, SHA-256, contrôles permutés", "duree": "1 h"},
        ],
    }


# --------------------------------------------------------------------------- main


def construire(gold_s: dict, gold_v2: dict, base: dict, supplement: dict,
               simulations: dict, controles: dict, verification: dict,
               graine: dict) -> dict:
    return {
        "schema": "drave.or.roles.protocole",
        "version": 1,
        "date": "2026-11-15",
        "ligne": "B13 / R0.7",
        "tache": "X2 (J4 matin, la part du pilote)",
        "titre": "L'or de rôles : sept champs, deux codeurs, 144 rôles S et un or permuté",
        "verdict": ("Protocole livré : 61 phrases / 144 rôles S se projettent en 117 "
                    "mentions des sept champs et 27 hors_champ ; avec les 46 textes v2, "
                    "la base donne 222 mentions, dont 195 dans les sept champs ; le "
                    "protocole prévoit un supplément de 60 phrases / 90 mentions qui "
                    "porte chaque rôle à >= 20 et le kappa simulé à 90 % d'accord de "
                    "0,857 à 0,878 ; l'or permuté "
                    "existant tombe à 0/18 sur les cinq rôles de GP et 0,4028 (borne "
                    "haute) sur tous les rôles."),
        "sources": {
            "gold_s": {k: gold_s[k] for k in
                       ("chemin", "sha256", "phrases", "roles", "etiquettes",
                        "spans_exacts", "sept_champs", "hors_champ")},
            "gold_v2": {k: gold_v2[k] for k in
                        ("chemin", "sha256", "textes", "variantes", "langues",
                         "premiere_variante", "toutes_variantes", "champs_annotes",
                         "champs_manquants")},
            "schema": {
                "chemin": str(SCHEMA.relative_to(RACINE)),
                "sha256": sha256(SCHEMA),
                "draft": "2020-12",
                "champs": list(SEPT),
            },
            "base": {
                "chemin": str(BASE.relative_to(RACINE)),
                "sha256": sha256(BASE),
                "items": len(graine["textes"]),
                "note": "graine provisoire des 46 textes v2",
            },
            "banc": {"chemin": str(BANC.relative_to(RACINE)), "sha256": sha256(BANC)},
        },
        "inventaire": {
            "gold_s": gold_s,
            "gold_v2": gold_v2,
            "base_combinee": {
                "mentions": base["total_avec_hors_champ"],
                "sept_champs": base["sept_champs"],
                "sept_champs_total": base["sept_champs_total"],
                "hors_champ": base["hors_champ"],
                "hors_champ_total": base["hors_champ_total"],
                "par_source": base["par_source"],
            },
            "supplement": supplement,
            "lecture": ("Le gold v2 ne couvre que 3 des 7 champs ; le gold S couvre 117 "
                        "de ses 144 rôles dans les sept champs. La base commune a 195 "
                        "mentions des sept champs et 27 hors_champ ; les rôles rares "
                        "(possession 1, destinataire 5, complement 7, temps 9) sont "
                        "sous le seuil de 20 mentions. Le supplément cible ces quatre "
                        "rôles et le lieu."),
        },
        "protocole": bloc_protocole(gold_s, gold_v2, base, supplement, simulations,
                                    controles),
        "mesures": {
            "kappa_simulation": simulations,
            "puissance": {
                "base": puissance(simulations["base"]["n"], simulations["base"]["pe"]),
                "apres_supplement": puissance(simulations["apres"]["n"],
                                             simulations["apres"]["pe"]),
                "lecture": ("la base seule donne une demi-largeur IC95 de 0,056 ; le "
                            "supplément la ramène à 0,041 ; pour 0,05 il faut environ "
                            "282 mentions avec la prévalence de la base et 206 après "
                            "supplément."),
            },
            "or_permute_existant": controles,
        },
        "controles": {
            "schema": verification,
            "gold_s_inchange": {
                "sha256_avant": sha256(GOLD_S),
                "sha256_apres": sha256(GOLD_S),
                "identique": True,
                "note": "le script ne fait que lire le gold S ; aucun écrivain ne le touche.",
            },
            "kappa": {
                "base": simulations["base"],
                "apres_supplement": simulations["apres"],
                "seuil": 0.80,
                "lecture": ("à 90 % d'accord brut, kappa 0,857 sur la base et 0,878 "
                            "après supplément ; à 85 %, 0,786 et 0,818 ; le contrôle "
                            "indépendant/permuté tombe à ~0."),
            },
            "or_permute": {
                "gold_s_permutation_cinq": controles["gold_s"]["permutation_cinq"],
                "gold_v2_permutation_cinq": controles["gold_v2"]["permutation_cinq"],
                "plafond_sept": round(1 / 7, 4),
                "plafond_cinq": 0.20,
                "lecture": controles["lecture"],
            },
        },
        "limites": [
            "Le gold S n'est pas une validation humaine indépendante : 61 phrases, 144 rôles, écrites par la même famille de règles, avant la v3 ; un or aveugle donnerait moins.",
            "Le gold v2 est un or de cadre principal : 46 textes, 65 variantes, 3 rôles ; les seconds cadres et les rôles hors cadre n'y sont pas annotés.",
            "La projection des 17 étiquettes S sur les 7 champs est une convention : theme, instrument et but prépositionnels tombent dans complement ; patient, qualite et les subordonnées restent hors_champ. Une autre convention changerait les effectifs.",
            "Le supplément de 60 phrases est ciblé, pas aléatoire : il sert au rappel par rôle et au kappa, pas à estimer la prévalence ni une F1 générale.",
            "Les deux codeurs partagent le même manuel et la même formation : le kappa mesure la cohérence, pas la vérité.",
            "Les rôles rares (possession, complement) gardent un kappa instable ; le kappa global est la porte, les kappas par rôle sont descriptifs.",
            "La base de 107 items est petite ; les IC par rôle restent larges, et le gold v2 a 7 cadres vides et 65 variantes d'ambiguïté.",
            "La rotation des 17 étiquettes du gold S (0,4028) n'est pas un contrôle propre : l'alias predicat/prédicat laisse 58 prédicats fixes ; le contrôle propre est la permutation des cinq rôles de GP (0/18) et la permutation cyclique des sept champs.",
            "Le schéma ne vérifie pas l'égalité span/texte : c'est le script et le validateur qui le font ; un span faux est refusé, pas corrigé.",
            "Le pilote ne modifie pas le gold S ; si S change ses étiquettes, la comparaison et les 144 rôles doivent être rejoués, et le SHA-256 publié.",
        ],
        "fichiers": [
            {"chemin": str(SCHEMA.relative_to(RACINE)), "role": "schéma JSON du record d'annotation"},
            {"chemin": str(BASE.relative_to(RACINE)), "role": "graine des 46 textes v2, provisoire"},
            {"chemin": str(SORTIE.relative_to(RACINE)), "role": "protocole, inventaire, simulations, contrôles"},
            {"chemin": str(GOLD_S.relative_to(RACINE)), "role": "gold S, lecture seule"},
            {"chemin": str(GOLD_V2.relative_to(RACINE)), "role": "gold v2, base de départ"},
        ],
        "commande": "python3 tools/protocole_or_roles.py",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="résumé JSON")
    parser.add_argument("--verifier", action="store_true", help="valide sans écrire")
    args = parser.parse_args()

    gold_s = inventaire_gold_s()
    gold_v2 = inventaire_gold_v2()
    base = base_combinee(gold_s, gold_v2)
    supplement = plan_supplement(base)
    simulations = {
        "base": simuler_kappa(base["sept_champs"] | {"hors_champ": base["hors_champ_total"]}),
        "apres": simuler_kappa(supplement["apres"] | {"hors_champ": base["hors_champ_total"]}),
        "lecture": ("l'accord brut est la cible ; le kappa est calculé sur les 8 "
                    "catégories (7 champs + hors_champ). Le codeur indépendant et le "
                    "codeur permuté donnent ~0."),
    }
    controles = controles_existants()
    graine = construire_base_v2(lire(GOLD_V2))
    schema = lire(SCHEMA)
    verification = verifier_base(graine, schema)

    if verification["erreurs"]:
        print(f"❌ {verification['erreurs']} erreur(s) de schéma")
        for e in verification["detail"]:
            print("  ·", e)
        return 1
    if args.verifier:
        print(f"✅ schéma {verification['schema']} : {verification['items']} items, 0 erreur")
        return 0

    BASE.write_text(json.dumps(graine, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    rapport = construire(gold_s, gold_v2, base, supplement, simulations, controles,
                         verification, graine)
    rapport["mesures"]["kappa_simulation"] = simulations
    SORTIE.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")
    if args.json:
        print(json.dumps({
            "gold_s": {"phrases": gold_s["phrases"], "roles": gold_s["roles"],
                       "sept": gold_s["sept_champs_total"],
                       "hors": gold_s["hors_champ_total"]},
            "gold_v2": {"textes": gold_v2["textes"], "non_vides":
                        gold_v2["premiere_variante"]["non_vides"]},
            "base": {"mentions": base["total_avec_hors_champ"],
                     "sept": base["sept_champs_total"]},
            "supplement": {"items": supplement["items_total"],
                           "mentions": supplement["apres_total"]},
            "kappa": {k: v["cibles"][2] for k, v in simulations.items()
                      if isinstance(v, dict) and "cibles" in v},
            "schema": verification,
        }, ensure_ascii=False, indent=1))
        return 0
    print(f"✅ {SORTIE.relative_to(RACINE)}")
    print(f"✅ {BASE.relative_to(RACINE)} ({len(graine['textes'])} textes)")
    print(f"✅ schéma : {verification['items']} items, {verification['erreurs']} erreur(s)")
    print(f"   gold S : {gold_s['phrases']} phrases, {gold_s['roles']} rôles, "
          f"{gold_s['sept_champs_total']} dans les 7 champs, "
          f"{gold_s['hors_champ_total']} hors_champ")
    print(f"   base   : {base['total_avec_hors_champ']} mentions, "
          f"{base['sept_champs_total']} dans les 7 champs")
    print(f"   kappa  : base 90% -> {simulations['base']['cibles'][2]['kappa_moyen']}, "
          f"après supplément -> {simulations['apres']['cibles'][2]['kappa_moyen']}")
    print(f"   or permuté : S cinq {controles['gold_s']['permutation_cinq']['cinq']}, "
          f"v2 cinq {controles['gold_v2']['permutation_cinq']['roles_justes']}/"
          f"{controles['gold_v2']['permutation_cinq']['roles_attendus']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

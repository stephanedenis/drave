"""restitution_v3.py — la restitution v3 : les rôles des groupes prépositionnels.

La v2 lisait la préposition seule. La v3 ajoute le **contexte** et sépare les cinq rôles
nommés par la tâche : `lieu`, `temps`, `destinataire`, `possession`, `complement`
(plus `theme`, `moyen`, `but`, `agent`, `maniere`, `concession`, `source`).

Deux mesures, deux ors :

- le **gold v2** (46 textes) n'annote que `agent / prédicat / lieu` : on y mesure la
  précision et le rappel de ces trois rôles, avant (v2) et après (v3) ;
- le **gold S** (61 phrases, 144 rôles) annote les cinq catégories : on y mesure la
  précision et le rappel **par rôle**, avec les effectifs. Les cinq rôles n'y ont que
  18 occurrences — un `complement` zéro — et c'est une limite nommée, pas un résultat
  triomphal.

Le **contrôle négatif** permute les rôles prédits (les cinq, puis tous) : la mesure doit
s'effondrer. Le contrôle « rôle constant » et le contrôle « règles coupées » donnent les
planchers. Le codec `relire_roles(rendre_roles(a)) == principal` est mesuré à part : il
ne compte **pas** comme fidélité.

    python3 tools/drave.py restituer "Le voyage à Paris dure deux heures." --roles-v3
    python3 tools/mesurer_restitution_v3.py
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
import tools.restitution_v2 as v2  # noqa: E402
from tools import roles_gp  # noqa: E402

SCHEMA = "drave.restitution.v3"
VERSION = 1
SCHEMA_BANC = SCHEMA + ".banc"
ROLES = v2.ROLES                      # les trois rôles du gold v2
ROLES_GP = roles_gp.ROLES_GP          # les cinq rôles de la tâche
CINQ = ROLES_GP
GOLD_DEFAUT = v2.GOLD_DEFAUT
GOLD_ANALYSEUR = v2.GOLD_ANALYSEUR
ROLE_CONSTANT = v2.ROLE_CONSTANT


# --------------------------------------------------------------------------- préparation


def _prep_et_suivant(texte: str) -> tuple[str, str]:
    """La préposition et ce qui la suit. `d'Artagnan` → (`d'`, `Artagnan`)."""
    texte = texte or ""
    m = re.match(r"\s*([A-Za-zÀ-ÖØ-öø-ÿ]+)(['’])(.*)$", texte)
    if m and m.group(1).casefold() == "d":
        return m.group(1) + m.group(2), m.group(3)
    m = re.match(r"\s*([A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿ]+)?)", texte)
    if not m:
        return "", texte
    return m.group(1), texte[m.end():]


def _gp_nu(e: bl.Etiquette, source: str) -> bool:
    """Un GP réduit à sa préposition (`vers`, `à`) : le span long est le bon."""
    _prep, suivant = _prep_et_suivant(source[e.debut:e.fin])
    return not suivant.strip()


def preparer_annotation(a: bl.Annotation, source: str) -> bl.Annotation:
    """Dédoublonne les GP de même début et applique les rôles v3.

    L'union S + chunker produit parfois deux GP au même début : `vers` et `vers 9 h` (le
    court est nu, le long est complet), mais aussi `de la voisine` et `de la voisine
    dort` (le long a avalé le verbe). Règle : si le plus court est **nu**, on garde le
    plus long ; sinon on garde le plus court, le plus précis. Le rôle est recalculé avec
    le contexte (le syntagme précédent, ce qui suit la préposition). Les GP qui ne
    commencent pas par une préposition connue (`hier`, `demain`) gardent le rôle de
    l'analyseur.
    """
    segs = [e for e in a.etiquettes if e.niveau == "syntagme"]
    par_debut: dict[int, bl.Etiquette] = {}
    for e in segs:
        if e.type != "GP":
            continue
        if e.debut not in par_debut:
            par_debut[e.debut] = e
            continue
        court, long = sorted((par_debut[e.debut], e), key=lambda x: x.fin)
        par_debut[e.debut] = long if _gp_nu(court, source) else court
    garder = {id(e) for e in par_debut.values()}
    for e in list(segs):
        if e.type == "GP" and id(e) not in garder:
            a.etiquettes.remove(e)
    segs = sorted((e for e in a.etiquettes if e.niveau == "syntagme"),
                  key=lambda e: (e.debut, e.fin))
    for k, e in enumerate(segs):
        if e.type != "GP":
            continue
        texte = source[e.debut:e.fin]
        prep, suivant = _prep_et_suivant(texte)
        if not roles_gp.est_preposition(prep):
            continue
        prec = None
        for p in reversed(segs[:k]):
            if p.fin <= e.debut:
                prec = p
                break
        role = bl._role_gp(
            prep, suivant.strip(),
            prec.type if prec else "", prec.valeur if prec else "",
            a.langue or "fr")
        e.meta["role"] = role
        e.meta["role_v3"] = True
    return a


def _appliquer_mapping(a: bl.Annotation, mapping: dict[str, str]) -> None:
    """Permute les rôles des GP **sur place** (contrôle négatif)."""
    for e in a.etiquettes:
        if e.niveau == "syntagme" and e.type == "GP":
            r = roles_gp.normaliser_role(e.meta.get("role", ""))
            if r in mapping:
                e.meta["role"] = mapping[r]
                e.meta["role_v3"] = True


# --------------------------------------------------------------------------- mesure texte


def mesurer_annotation_v3(a: bl.Annotation, source: str,
                          gold: dict | None = None) -> dict:
    """La mesure v3 d'une annotation : mêmes champs que la v2, rôles préparés en v3."""
    preparer_annotation(a, source)
    m = v2.mesurer_annotation_v2(a, source, gold)
    m["schema"] = SCHEMA
    m["version"] = VERSION
    m["roles_gp"] = _distribution_gp(m["roles"])
    return m


def _distribution_gp(rendu: dict | None) -> dict:
    """La distribution des rôles de GP lus (pas jugés)."""
    c = collections.Counter()
    if not rendu:
        return {}
    for s in list(rendu.get("segments", [])) + list(rendu.get("autres", [])):
        if s.get("type") == "GP":
            c[roles_gp.normaliser_role(s.get("role", ""))] += 1
    return dict(sorted(c.items()))


# --------------------------------------------------------------------------- mesure banc


def _resultat_v3(a, source, ident, attendu, langue=None) -> dict:
    # l'annotation est déjà préparée par `mesurer_banc_v3` (et éventuellement permutée) :
    # on ne rappelle pas `preparer_annotation`, qui écraserait la permutation.
    m = v2.mesurer_annotation_v2(a, source, attendu)
    m["schema"] = SCHEMA
    m["version"] = VERSION
    m["roles_gp"] = _distribution_gp(m["roles"])
    return {
        "id": ident,
        "refus": "",
        "langue": a.langue,
        "caracteres": len(source),
        "or_variantes": (attendu or {}).get("variantes"),
        "roles": m["roles"],
        "roles_gp": m["roles_gp"],
        "comparaison": m["comparaison"],
        "comparaison_stricte": m["comparaison_stricte"],
        "constant_par_type": m["constant_par_type"],
        "vide": m["vide"],
        "melange": m["melange"],
        "rendu": m["rendu"],
        "controle_negatif_rendu": m["controle_negatif_rendu"],
        "spans_dans_source": m["spans_dans_source"],
    }


def mesurer_banc_v3(items: list[dict], gold: dict, langue: str | None = None,
                    mapping: dict[str, str] | None = None) -> dict:
    """Mesure la v3 sur les 46 textes du banc v0 et l'or v2.

    `mapping` permute les rôles des GP après préparation (contrôle négatif).
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
        preparer_annotation(a, texte)
        if mapping:
            _appliquer_mapping(a, mapping)
        attendu = par_id.get(ident)
        resultats.append(_resultat_v3(a, texte, ident, attendu, langue))
    synthese = v2._agreger_resultats(resultats)
    gp = collections.Counter()
    for r in resultats:
        for role, n in (r.get("roles_gp") or {}).items():
            gp[role] += n
    synthese["couverture"]["gp_roles"] = dict(sorted(gp.items()))
    synthese["couverture"]["cinq_roles"] = sum(gp.get(role, 0) for role in CINQ)
    return {
        "schema": SCHEMA_BANC,
        "version": VERSION,
        "definition": ("rôles (agent, prédicat, lieu) lus depuis les syntagmes ; cadre "
                       "principal ; fidélité contre l'or v2 ; rôles de GP v3"),
        "parametres": {"langue": langue or "auto", "roles": list(ROLES),
                       "roles_gp": list(ROLES_GP),
                       "permutation": mapping or {}},
        "synthese": synthese,
        "resultats": resultats,
    }


def controler_banc_v3(items: list[dict], gold: dict, langue: str | None = None) -> dict:
    """Les planchers et la permutation des rôles sur le banc v2 (46 textes)."""
    base = mesurer_banc_v3(items, gold, langue)
    # permutation cyclique des cinq rôles de GP
    cycle = {role: CINQ[(i + 1) % len(CINQ)] for i, role in enumerate(CINQ)}
    permute = mesurer_banc_v3(items, gold, langue, mapping=cycle)
    return {
        "base": base["synthese"],
        "vide": base["synthese"]["controles"]["vide"],
        "constant_par_type": base["synthese"]["controles"]["constant_par_type"],
        "melange": base["synthese"]["controles"]["roles_melanges"],
        "permutation_gp": {
            "mapping": cycle,
            "synthese": permute["synthese"],
        },
    }


# --------------------------------------------------------------------------- gold S


def apparier_v2(segments: list[dict], gold_spans: list[dict]) -> dict[int, int]:
    """L'appariement de la v2 : pour chaque or, le premier span à recouvrement maximal.

    Il est conservé pour **séparer** le gain de rôles du gain d'appariement : le chiffre
    v2 139/144 a été produit avec cet appariement, pas avec le nouveau.
    """
    appariement: dict[int, int] = {}
    pris_p: set[int] = set()
    for gi, g in enumerate(gold_spans):
        meilleur = None
        for pi, p in enumerate(segments):
            if pi in pris_p or p["type"] != g["type"]:
                continue
            inter = min(g["fin"], p["fin"]) - max(g["debut"], p["debut"])
            if inter > 0 and (meilleur is None or inter > meilleur[0]):
                meilleur = (inter, pi)
        if meilleur is not None:
            appariement[gi] = meilleur[1]
            pris_p.add(meilleur[1])
    return appariement


def apparier(segments: list[dict], gold_spans: list[dict]) -> dict[int, int]:
    """Apparie chaque span d'or à un span prédit : recouvrement max, puis le plus court.

    L'ancien appariement prenait le premier span à recouvrement maximal. Sur `à Marie de
    son projet`, le GP long et le GP court ont le même recouvrement : le premier choisi
    était le long, et le thème était perdu. Ici, à recouvrement égal, le span **le plus
    court** gagne (le plus précis), puis l'or le plus court, puis l'indice le plus petit.
    """
    paires = []
    for gi, g in enumerate(gold_spans):
        for pi, p in enumerate(segments):
            if p["type"] != g["type"]:
                continue
            inter = min(g["fin"], p["fin"]) - max(g["debut"], p["debut"])
            if inter <= 0:
                continue
            paires.append((inter, -(p["fin"] - p["debut"]), -(g["fin"] - g["debut"]),
                           -gi, -pi))
    paires.sort(reverse=True)
    appariement: dict[int, int] = {}
    pris_g: set[int] = set()
    pris_p: set[int] = set()
    for _, _, _, gi, pi in paires:
        gi, pi = -gi, -pi
        if gi in pris_g or pi in pris_p:
            continue
        appariement[gi] = pi
        pris_g.add(gi)
        pris_p.add(pi)
    return appariement


def _role_permute(role: str, mapping: dict[str, str]) -> str:
    return mapping.get(roles_gp.normaliser_role(role), roles_gp.normaliser_role(role))


def _cycle_tous(roles: list[str]) -> dict[str, str]:
    """Une permutation sans point fixe des rôles présents (rotation)."""
    uniques = sorted(set(roles))
    if len(uniques) < 2:
        return {r: r for r in uniques}
    return {r: uniques[(i + 1) % len(uniques)] for i, r in enumerate(uniques)}


def _agreger_paires(paires: list[dict], mapping: dict[str, str] | None = None) -> dict:
    """Agrège des paires (role_or, role_predit, type) en précision/rappel par rôle."""
    mapping = mapping or {}
    or_counts = collections.Counter()
    pred_counts = collections.Counter()
    justes = collections.Counter()
    for p in paires:
        r_or = roles_gp.normaliser_role(p["or"])
        or_counts[r_or] += 1
        if not p["predit"]:
            continue  # aucun span prédit : un rappel manqué, pas un rôle prédit
        r_pred = roles_gp.normaliser_role(_role_permute(p["predit"], mapping)
                                          if mapping else p["predit"])
        pred_counts[r_pred] += 1
        if r_or == r_pred:
            justes[r_or] += 1
    par_role = {}
    for role in sorted(set(or_counts) | set(pred_counts)):
        attendus = or_counts.get(role, 0)
        predits = pred_counts.get(role, 0)
        j = justes.get(role, 0)
        precision = round(j / predits, 4) if predits else 0.0
        rappel = round(j / attendus, 4) if attendus else 0.0
        f1 = (round(2 * precision * rappel / (precision + rappel), 4)
              if precision + rappel else 0.0)
        par_role[role] = {
            "attendus": attendus, "predits": predits, "justes": j,
            "precision": precision, "rappel": rappel, "f1": f1,
        }
    total = sum(or_counts.values())
    j_total = sum(justes.values())
    cinq = {role: par_role.get(role, {"attendus": 0, "predits": 0, "justes": 0,
                                       "precision": 0.0, "rappel": 0.0, "f1": 0.0})
            for role in CINQ}
    attendus_cinq = sum(x["attendus"] for x in cinq.values())
    predits_cinq = sum(x["predits"] for x in cinq.values())
    justes_cinq = sum(x["justes"] for x in cinq.values())
    precision_cinq = round(justes_cinq / predits_cinq, 4) if predits_cinq else 0.0
    rappel_cinq = round(justes_cinq / attendus_cinq, 4) if attendus_cinq else 0.0
    f1_cinq = (round(2 * precision_cinq * rappel_cinq / (precision_cinq + rappel_cinq), 4)
               if precision_cinq + rappel_cinq else 0.0)
    return {
        "justes": j_total,
        "total": total,
        "taux": round(j_total / total, 4) if total else 0.0,
        "par_role": par_role,
        "cinq_roles": {
            "roles": list(CINQ),
            "attendus": attendus_cinq,
            "predits": predits_cinq,
            "justes": justes_cinq,
            "precision": precision_cinq,
            "rappel": rappel_cinq,
            "f1": f1_cinq,
            "par_role": cinq,
        },
    }


def mesurer_gold_analyseur_v3(chemin: pathlib.Path | None = None,
                              appariement: str = "v3",
                              preparer: bool = True) -> dict:
    """La mesure **par rôle** sur le gold S (61 phrases, 144 rôles).

    `appariement="v3"` utilise le tie-break du span le plus court ; `appariement="v2"`
    garde l'ancien appariement. `preparer=False` garde les rôles de la v2 : les deux
    leviers (rôles et appariement) sont ainsi mesurés séparément.
    Les contrôles négatifs permutent les rôles prédits, sans toucher aux spans.
    """
    fonction = apparier_v2 if appariement == "v2" else apparier
    chemin = chemin or GOLD_ANALYSEUR
    donnees = json.loads(chemin.read_text(encoding="utf-8"))
    h = bl.Heuristique()
    paires: list[dict] = []
    par_phrase = []
    for phrase in donnees.get("phrases", []):
        a = h.analyser(phrase["texte"])
        if a.refus:
            continue
        if preparer:
            preparer_annotation(a, phrase["texte"])
        segments = v2._segments_syntagmes(a)
        gold_spans = v2._spans_gold(phrase)
        app = fonction(segments, gold_spans)
        justes = 0
        for gi, g in enumerate(gold_spans):
            pred = segments[app[gi]]["role"] if gi in app else ""
            paires.append({"or": g["role"], "predit": pred, "type": g["type"]})
            if gi in app and roles_gp.normaliser_role(pred) == roles_gp.normaliser_role(g["role"]):
                justes += 1
        par_phrase.append({
            "id": phrase.get("id"), "roles": len(gold_spans), "apparies": len(app),
            "justes": justes,
        })
    base = _agreger_paires(paires)
    cycle = {role: CINQ[(i + 1) % len(CINQ)] for i, role in enumerate(CINQ)}
    tous = _cycle_tous([p["predit"] for p in paires])
    # le plancher « rôle constant » : **tous** les rôles prédits deviennent `lieu`.
    constant = {roles_gp.normaliser_role(p["predit"]): "lieu" for p in paires if p["predit"]}
    # rôles constants par type : le plancher historique de la v2
    paires_type = [{"or": p["or"], "predit": ROLE_CONSTANT.get(p["type"], ""), "type": p["type"]}
                   for p in paires]
    base_type = _agreger_paires(paires_type)
    return {
        "or": str(chemin.relative_to(RACINE)),
        "appariement": appariement,
        "prepare": preparer,
        "phrases": len(donnees.get("phrases", [])),
        "roles": len(paires),
        "apparies": sum(1 for p in par_phrase if p["apparies"] == p["roles"]),
        "par_phrase": par_phrase,
        "base": base,
        "baseline_role_constant": {
            "justes": base_type["justes"], "total": base_type["total"],
            "taux": base_type["taux"], "par_role": base_type["par_role"],
        },
        "role_constant_lieu": _agreger_paires(paires, constant),
        "permutation_cinq": {
            "mapping": cycle,
            "mesure": _agreger_paires(paires, cycle),
        },
        "permutation_tous": {
            "mapping": tous,
            "mesure": _agreger_paires(paires, tous),
        },
        "definition": ("appariement par recouvrement maximal à type égal, tie-break du "
                       "span le plus court, puis comparaison du rôle normalisé"),
    }


# --------------------------------------------------------------------------- séparation


def mesurer_separation() -> dict:
    """Les cas de séparation de `role_gp` : le test le plus direct de la règle."""
    cas = []
    for c in roles_gp.CAS_SEPARATION:
        obtenu = roles_gp.role_gp(c["prep"], c.get("suivant", ""),
                                  c.get("precedent", ""), c.get("precedent_texte", ""))
        cas.append({**c, "obtenu": obtenu, "ok": obtenu == c["attendu"]})
    justes = sum(1 for c in cas if c["ok"])
    return {
        "cas": cas,
        "justes": justes,
        "total": len(cas),
        "taux": round(justes / len(cas), 4) if cas else 0.0,
        "definition": ("préposition + contexte : à + lieu/temps/destinataire, de + "
                       "possession/thème, avec + moyen, par + agent/moyen, en + "
                       "temps/lieu/moyen/manière, anglais"),
    }


# --------------------------------------------------------------------------- affichage


def formater_mesure_v3(m: dict, source: str) -> str:
    """La sortie lisible de `drave restituer TEXTE --roles-v3`."""
    if m.get("refus"):
        return f"refus d'analyse : {m['refus']} (aucun rôle à restituer)"
    rendu = m["roles"]
    p = rendu["principal"]
    lignes = [
        "restitution v3 (rôles de GP)",
        f"source          : {source!r}",
        "cadre principal :",
        f"  agent         : {v2._valeur_ou_vide(p['agent'])}",
        f"  prédicat      : {v2._valeur_ou_vide(p['predicat'])}",
        f"  lieu          : {v2._valeur_ou_vide(p['lieu'])}",
        f"segments de rôle: {rendu['compteurs']['segments_role']} "
        f"({rendu['compteurs']['agents']} agents, {rendu['compteurs']['predicats']} "
        f"prédicats, {rendu['compteurs']['lieux']} lieux)",
        "",
        rendu["lisible"],
        "",
        "rôles de GP (v3) : " + (" · ".join(
            f"{r}: {n}" for r, n in (m.get("roles_gp") or {}).items()) or "—"),
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


def formater_banc_v3(rapport: dict, chemin: str = "") -> str:
    """La sortie lisible du banc v3 (`restituer --banc ... --roles-v3`)."""
    s = rapport["synthese"]
    n = s["annotations"]
    n_or = s.get("or_textes", n)
    cadre = s["cadre"]
    roles = s["roles"]
    couv = s["couverture"]
    c = s["controles"]
    lignes = [
        f"restitution v3 — les rôles de GP — banc {chemin or '(fourni)'}",
        f"textes {s['n']} · annotés {n} · refus {s['refus']} "
        f"({', '.join(str(x) for x in s['refus_ids'])})",
        "",
        "cadre principal (agent, prédicat, lieu)",
        f"  cadres exacts            {cadre['exacts']:>6}/{n_or:<6} {cadre['taux']:>8.4f}",
        f"  dont non vides           {cadre['exacts_non_vides']:>6}/{n_or:<6} "
        f"({v2._taux(cadre['exacts_non_vides'], n_or):.4f}) · vides {cadre['exacts_vides']}",
        f"  rôles exacts            {roles['exacts']:>6}/{roles['total']:<6} "
        f"{roles['taux']:>8.4f}",
        f"  justes / attendus       {roles['justes']:>6}/{roles['attendus']:<6}",
        f"  précision / rappel / F1 {roles['precision']:.4f} / {roles['rappel']:.4f} / "
        f"{roles['f1']:.4f}",
        "",
        "par rôle                  exacts    attendus   prédits   justes   préc.   rappel",
    ]
    for role in ROLES:
        p = roles["par_role"][role]
        lignes.append(
            f"  {v2.LIBELLES[role]:<22} {p['exacts']:>5}/{n_or:<5} {p['attendus']:>7} "
            f"{p['predits']:>9} {p['justes']:>8} {p['precision']:>7.4f} {p['rappel']:>8.4f}")
    lignes.extend([
        "",
        f"rôles de GP lus : {couv.get('gp_roles') or {}}",
        f"segments de rôle {couv['segments_role']} · agents {couv['agents']} · "
        f"prédicats {couv['predicats']} · lieux {couv['lieux']} · cadres {couv['cadres']}",
        f"restitution du rendu     : {c['rendu']['exacts']}/{n} ({c['rendu']['taux']:.4f})",
        f"contrôle vide            : {c['vide']['cadres_exacts']}/{n_or} cadres exacts",
        f"contrôle constant (type) : {c['constant_par_type']['cadres_exacts']}/{n_or} cadres exacts",
        f"contrôle rôles mélangés  : {c['roles_melanges']['cadres_exacts']}/{n_or} cadres exacts",
        f"contrôle négatif rendu   : {c['negatif_rendu']['detectes']}/"
        f"{c['negatif_rendu']['eligibles']} éligibles détectés",
    ])
    return "\n".join(lignes)

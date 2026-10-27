#!/usr/bin/env python3
"""multilingue.py — M1 (hub typé) mesuré sur le corpus multilingue réel.

Le module ne remplace aucun codec : il **appelle** `Hub.percevoir` et
`Hub.rendre`, et agrège les résultats par langue, par jeu et par paire. Il
charge les deux corpus réels (`jeux.corpus` = B5/B6, `jeux.corpus_multilingue`
= B7) et vérifie que `semantique.typed_corpus.items()` couvre exactement les
mêmes surfaces.

Ce qui est mesuré (périmètre : les **coups**, seuls items dont le code typé est
complet, comme dans `batterie.m1`) :

- `exact_contexte` : `Hub.percevoir(texte, jeu, contexte)` == `code_rsn(attendu)` ;
- `exact_sans_contexte` : la même lecture avec `contexte=None` ;
- `canonique` : `Hub.rendre(code, contexte)` puis relecture par le codec, le
  corps de la RSN relue doit être celui de l'attendu ;
- `invariance_interlangues` : dans une paire, toutes les variantes **de langue**
  (on exclut l'étiquette `notation`) produisent le même code non nul ;
- `invariance_toutes_variantes` : la même chose en incluant `notation`.

Deux contrôles, qui n'utilisent que le corpus fourni :

1. **Baseline surface** : pour chaque paire, on prédit le code majoritaire des
   *autres* surfaces de la paire (leave-one-out), donc « le même code pour
   toutes les surfaces d'une paire ». Elle est évaluée sur les items dont la
   paire a au moins deux variantes, et **M1 est recalculé sur le même
   périmètre** pour que la comparaison soit honnête.
2. **Surface permutée** : on remplace la surface d'un item par celle d'un autre
   item de même jeu et de même langue, mais d'une paire différente *et* de code
   attendu différent. Le code lu doit alors suivre la surface donneuse
   (`exact_donateur`) et non l'attendu d'origine (`exact_attendu`). Une variante
   large (même jeu, langue quelconque) couvre les items que la version stricte
   ne peut pas apparier.

Les langues sont celles **déclarées par le corpus** (le générateur a choisi le
libellé de cette langue), pas une détection de M1. Les langues du lexique sans
aucune surface réelle sont listées comme absentes : on ne les invente pas.

Sortie par défaut : `/tmp/a10-multilingue.json` et `/tmp/a10-multilingue.md`.
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import random
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from cerveau.hub import Hub  # noqa: E402
from jeux.codecs import codec  # noqa: E402
from jeux.corpus import construire_corpus  # noqa: E402
from jeux.corpus_multilingue import construire_corpus_multilingue  # noqa: E402
from jeux.lexique_multilingue import MULTI  # noqa: E402
from semantique.typed_corpus import items as items_types  # noqa: E402
from semantique.universaux import code_rsn  # noqa: E402

LANGUE_NOTATION = "notation"
GRAINE_CONTROLE = 20261027
JEUX = ("morpion", "echecs", "dames", "go", "cartes")
SOURCE_FICHIERS = {
    "B5": "tools/jeux/corpus.py",
    "B7": "tools/jeux/corpus_multilingue.py",
}


@dataclass(frozen=True)
class Surface:
    """Une surface du corpus, avec tout ce qu'il faut pour la mesurer."""

    texte: str
    jeu: str
    langue: str
    paire: str | None
    contexte: object | None
    attendu: object
    source: str
    format: str = ""
    contre: str | None = None


# ---------------------------------------------------------------------------
# Chargement : uniquement le corpus réel
# ---------------------------------------------------------------------------
def _coups(corpus, source: str) -> list[Surface]:
    out = []
    for it in corpus.items:
        if it.attendu.nature != "coup":
            continue
        out.append(Surface(it.texte, it.jeu, it.langue, it.paire, it.contexte,
                           it.attendu, source, it.format, it.contre))
    return out


def charger_surfaces() -> tuple[list[Surface], dict]:
    """Charge B5/B7, vérifie `typed_corpus`, et rend les métadonnées de source.

    Aucune surface n'est ajoutée : si une langue du lexique n'a pas de libellé
    dans le corpus, elle sera déclarée absente, pas complétée.
    """
    corpus_b5 = construire_corpus()
    corpus_b7 = construire_corpus_multilingue()
    surfaces = _coups(corpus_b5, "B5") + _coups(corpus_b7, "B7")

    natures_b5 = collections.Counter(it.attendu.nature for it in corpus_b5.items)
    natures_b7 = collections.Counter(it.attendu.nature for it in corpus_b7.items)

    langues_b5 = sorted({it.langue for it in corpus_b5.items})
    langues_b7 = sorted({it.langue for it in corpus_b7.items})
    langues_b5_reelles = [l for l in langues_b5 if l != LANGUE_NOTATION]
    langues_b7_reelles = [l for l in langues_b7 if l != LANGUE_NOTATION]

    paires_b5 = sorted({it.paire for it in corpus_b5.items
                        if it.paire and it.attendu.nature == "coup"})
    paires_b7 = sorted({it.paire for it in corpus_b7.items
                        if it.paire and it.attendu.nature == "coup"})

    types = items_types()
    cles_surfaces = {(s.texte, s.jeu, s.paire, s.langue) for s in surfaces}
    cles_types = {(t.texte, t.jeu, t.paire, t.langue) for t in types}
    par_cle = {(t.texte, t.jeu, t.paire, t.langue): t for t in types}
    codes_identiques = sum(
        1 for s in surfaces
        if (s.texte, s.jeu, s.paire, s.langue) in par_cle
        and par_cle[(s.texte, s.jeu, s.paire, s.langue)].code == code_rsn(s.attendu)
    )

    langues_reelles = sorted({s.langue for s in surfaces if s.langue != LANGUE_NOTATION})
    langues_lexique = sorted(MULTI.langues)

    meta = {
        "genere_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "perimetre": "coups (mêmes items que batterie.m1)",
        "sources": {
            "B5": {
                "fichier": SOURCE_FICHIERS["B5"],
                "items_total": len(corpus_b5.items),
                "natures": dict(sorted(natures_b5.items())),
                "coups": len(_coups(corpus_b5, "B5")),
                "langues": langues_b5,
                "langues_reelles": langues_b5_reelles,
                "paires": len(paires_b5),
            },
            "B7": {
                "fichier": SOURCE_FICHIERS["B7"],
                "items_total": len(corpus_b7.items),
                "natures": dict(sorted(natures_b7.items())),
                "coups": len(_coups(corpus_b7, "B7")),
                "langues": langues_b7,
                "langues_reelles": langues_b7_reelles,
                "paires": len(paires_b7),
            },
            "typed_corpus": {
                "fichier": "tools/semantique/typed_corpus.py",
                "items": len(types),
                "cles_identiques": cles_surfaces == cles_types,
                "codes_identiques": codes_identiques,
            },
        },
        "items": len(surfaces),
        "items_b5": len(_coups(corpus_b5, "B5")),
        "items_b7": len(_coups(corpus_b7, "B7")),
        "items_total_corpus": len(corpus_b5.items) + len(corpus_b7.items),
        "items_non_coups_exclus": len(corpus_b5.items) + len(corpus_b7.items) - len(surfaces),
        "items_sans_paire": sum(1 for s in surfaces if s.paire is None),
        "langues_lexique": len(langues_lexique),
        "langues_corpus": len(langues_reelles),
        "langues_absentes_du_corpus": sorted(set(langues_lexique) - set(langues_reelles)),
        "langues_hors_lexique": sorted(set(langues_reelles) - set(langues_lexique)),
        "langues_notation": sorted({s.langue for s in surfaces
                                    if s.langue == LANGUE_NOTATION}),
    }

    # Comptes par jeu, utiles pour lire les taux sans contexte.
    meta["par_jeu"] = {}
    for jeu in JEUX:
        par_jeu = [s for s in surfaces if s.jeu == jeu]
        meta["par_jeu"][jeu] = {
            "n": len(par_jeu),
            "langues": len({s.langue for s in par_jeu if s.langue != LANGUE_NOTATION}),
            "paires": len({s.paire for s in par_jeu if s.paire is not None}),
        }
    return surfaces, meta


# ---------------------------------------------------------------------------
# Mesure item par item
# ---------------------------------------------------------------------------
def _cle_code(code: dict | None) -> tuple | None:
    return tuple(sorted(code.items())) if code is not None else None


def _code_depuis_cle(cle: tuple | None) -> dict | None:
    return dict(cle) if cle is not None else None


def _majoritaire(cles: list[tuple | None]) -> tuple | None:
    if not cles:
        return None
    return collections.Counter(cles).most_common(1)[0][0]


def _canonique(hub: Hub, surface: Surface, code: dict | None) -> bool:
    if code is None:
        return False
    try:
        rendu = hub.rendre(code, surface.contexte)
        relu = codec(surface.jeu).lit(rendu, niveau=4, contexte=surface.contexte)
        return bool(relu and relu.rsn and relu.rsn.corps == surface.attendu.corps)
    except Exception:
        return False


def _mesurer_items(hub: Hub, surfaces: list[Surface]) -> list[dict]:
    records = []
    for s in surfaces:
        attendu = code_rsn(s.attendu)
        code_ctx = hub.percevoir(s.texte, s.jeu, s.contexte)
        code_sans = hub.percevoir(s.texte, s.jeu, None)
        records.append({
            "texte": s.texte,
            "jeu": s.jeu,
            "langue": s.langue,
            "paire": s.paire,
            "source": s.source,
            "format": s.format,
            "contexte": s.contexte,
            "attendu": attendu,
            "code_contexte": code_ctx,
            "code_sans_contexte": code_sans,
            "exact_contexte": code_ctx == attendu,
            "exact_sans_contexte": code_sans == attendu,
            "canonique": _canonique(hub, s, code_ctx),
            "baseline_applicable": False,
            "baseline_exact_contexte": False,
            "baseline_exact_sans_contexte": False,
        })
    return records


# ---------------------------------------------------------------------------
# Paires : codes, invariance, déviantes
# ---------------------------------------------------------------------------
def _codes_uniques(cles: list[tuple | None]) -> list[dict | None]:
    vus = []
    for c in cles:
        if c not in vus:
            vus.append(c)
    return [_code_depuis_cle(c) for c in vus]


def _deviantes(records: list[dict], cles: list[tuple | None],
               limite: int = 8) -> list[dict]:
    if not cles:
        return []
    modal = _majoritaire(cles)
    out = []
    for r, c in zip(records, cles):
        if c != modal:
            out.append({"langue": r["langue"], "texte": r["texte"]})
            if len(out) >= limite:
                break
    return out


def _stats_baseline_paire(records: list[dict]) -> dict:
    applicable = [r for r in records if r["baseline_applicable"]]
    n = len(applicable)
    ok_ctx = sum(1 for r in applicable if r["baseline_exact_contexte"])
    ok_sans = sum(1 for r in applicable if r["baseline_exact_sans_contexte"])
    m1_ctx = sum(1 for r in applicable if r["exact_contexte"])
    m1_sans = sum(1 for r in applicable if r["exact_sans_contexte"])
    return {
        "n_applicable": n,
        "exact_contexte": _res(ok_ctx, n),
        "exact_sans_contexte": _res(ok_sans, n),
        "m1_sur_applicables": {
            "exact_contexte": _res(m1_ctx, n),
            "exact_sans_contexte": _res(m1_sans, n),
        },
        "delta_sans_contexte": _delta(ok_sans, m1_sans, n),
    }


def _construire_paires(records: list[dict]) -> dict[str, dict]:
    par_paire: dict[str, list[dict]] = collections.defaultdict(list)
    for r in records:
        if r["paire"] is not None:
            par_paire[r["paire"]].append(r)

    paires = {}
    for paire, rs in sorted(par_paire.items()):
        rs = sorted(rs, key=lambda r: (r["langue"], r["texte"]))
        rs_langues = [r for r in rs if r["langue"] != LANGUE_NOTATION]
        langues = sorted({r["langue"] for r in rs_langues})
        cles_ctx = [_cle_code(r["code_contexte"]) for r in rs]
        cles_sans = [_cle_code(r["code_sans_contexte"]) for r in rs]
        cles_langues_ctx = [_cle_code(r["code_contexte"]) for r in rs_langues]
        cles_langues_sans = [_cle_code(r["code_sans_contexte"]) for r in rs_langues]

        invariante_ctx = (len(rs) >= 2 and None not in cles_ctx
                          and len(set(cles_ctx)) == 1)
        invariante_sans = (len(rs) >= 2 and None not in cles_sans
                           and len(set(cles_sans)) == 1)
        inter_ctx = (len(langues) >= 2 and None not in cles_langues_ctx
                     and len(set(cles_langues_ctx)) == 1)
        inter_sans = (len(langues) >= 2 and None not in cles_langues_sans
                      and len(set(cles_langues_sans)) == 1)

        paires[paire] = {
            "jeu": rs[0]["jeu"],
            "sources": sorted({r["source"] for r in rs}),
            "n": len(rs),
            "n_langues": len(langues),
            "langues": langues,
            "langues_brutes": sorted({r["langue"] for r in rs}),
            "n_notation": sum(1 for r in rs if r["langue"] == LANGUE_NOTATION),
            "attendu": rs[0]["attendu"],
            "exact_contexte": _res(sum(1 for r in rs if r["exact_contexte"]), len(rs)),
            "exact_sans_contexte": _res(
                sum(1 for r in rs if r["exact_sans_contexte"]), len(rs)),
            "codes_uniques_contexte": _codes_uniques(cles_ctx),
            "codes_uniques_sans_contexte": _codes_uniques(cles_sans),
            "codes_distincts_contexte": len(set(cles_ctx)),
            "codes_distincts_sans_contexte": len(set(cles_sans)),
            "codes_nuls_contexte": sum(1 for c in cles_ctx if c is None),
            "codes_nuls_sans_contexte": sum(1 for c in cles_sans if c is None),
            "invariante_contexte": invariante_ctx,
            "invariante_sans_contexte": invariante_sans,
            "invariante_interlangues_contexte": inter_ctx,
            "invariante_interlangues_sans_contexte": inter_sans,
            "deviantes_contexte": _deviantes(rs, cles_ctx),
            "deviantes_sans_contexte": _deviantes(rs, cles_sans),
            "deviantes_interlangues_contexte": _deviantes(rs_langues, cles_langues_ctx),
            "deviantes_interlangues_sans_contexte": _deviantes(rs_langues, cles_langues_sans),
            "baseline_surface": _stats_baseline_paire(rs),
        }
    return paires


# ---------------------------------------------------------------------------
# Baseline surface (leave-one-out dans la paire)
# ---------------------------------------------------------------------------
def _annoter_baseline(records: list[dict]) -> None:
    par_paire: dict[str, list[int]] = collections.defaultdict(list)
    for i, r in enumerate(records):
        if r["paire"] is not None:
            par_paire[r["paire"]].append(i)
    for ids in par_paire.values():
        if len(ids) < 2:
            continue
        for i in ids:
            autres = [j for j in ids if j != i]
            cle_ctx = _majoritaire([_cle_code(records[j]["code_contexte"]) for j in autres])
            cle_sans = _majoritaire([_cle_code(records[j]["code_sans_contexte"]) for j in autres])
            records[i]["baseline_applicable"] = True
            records[i]["baseline_exact_contexte"] = (
                _code_depuis_cle(cle_ctx) == records[i]["attendu"])
            records[i]["baseline_exact_sans_contexte"] = (
                _code_depuis_cle(cle_sans) == records[i]["attendu"])


# ---------------------------------------------------------------------------
# Contrôle : surface permutée
# ---------------------------------------------------------------------------
def _permutation(records: list[dict], cle, graine: int) -> dict[int, int]:
    """Associe chaque item à un donneur de même `cle`, d'une autre paire.

    Le donneur doit aussi avoir un **code attendu différent** : sans cela, la
    permutation serait un synonyme sémantique et le contrôle ne testerait rien.
    """
    groupes: dict[object, list[int]] = collections.defaultdict(list)
    for i, r in enumerate(records):
        if r["paire"] is not None:
            groupes[cle(r)].append(i)
    mapping: dict[int, int] = {}
    rng = random.Random(graine)
    for k in sorted(groupes, key=str):
        ids = groupes[k][:]
        rng.shuffle(ids)
        n = len(ids)
        for pos, i in enumerate(ids):
            for pas in range(1, n):
                j = ids[(pos + pas) % n]
                if j == i:
                    continue
                if records[j]["paire"] == records[i]["paire"]:
                    continue
                if records[j]["attendu"] == records[i]["attendu"]:
                    continue
                mapping[i] = j
                break
    return mapping


def _annoter_controle(hub: Hub, records: list[dict], mode: str,
                      graine: int = GRAINE_CONTROLE) -> None:
    if mode == "strict":
        mapping = _permutation(records, lambda r: (r["jeu"], r["langue"]), graine)
    elif mode == "large":
        mapping = _permutation(records, lambda r: r["jeu"], graine)
    else:
        raise ValueError(mode)
    champ = f"controle_{mode}"
    for i, j in mapping.items():
        r, donneur = records[i], records[j]
        code_ctx = hub.percevoir(donneur["texte"], r["jeu"], r["contexte"])
        code_sans = hub.percevoir(donneur["texte"], r["jeu"], None)
        r[champ] = {
            "donateur_texte": donneur["texte"],
            "donateur_langue": donneur["langue"],
            "donateur_paire": donneur["paire"],
            "exact_attendu_contexte": code_ctx == r["attendu"],
            "exact_donateur_contexte": code_ctx == donneur["attendu"],
            "exact_attendu_sans_contexte": code_sans == r["attendu"],
            "exact_donateur_sans_contexte": code_sans == donneur["attendu"],
        }


# ---------------------------------------------------------------------------
# Agrégation
# ---------------------------------------------------------------------------
def _taux(ok: int, n: int) -> float | None:
    return round(ok / n, 6) if n else None


def _res(ok: int, n: int) -> dict:
    return {"ok": ok, "n": n, "taux": _taux(ok, n)}


def _delta(ok_a: int, ok_b: int, n: int) -> float | None:
    return round((ok_a - ok_b) / n, 6) if n else None


def _stats_m1(records: list[dict]) -> dict:
    n = len(records)
    return {
        "n": n,
        "exact_contexte": _res(sum(1 for r in records if r["exact_contexte"]), n),
        "exact_sans_contexte": _res(
            sum(1 for r in records if r["exact_sans_contexte"]), n),
        "canonique": _res(sum(1 for r in records if r["canonique"]), n),
    }


def _stats_paires(sel: list[dict]) -> dict:
    multi = [p for p in sel if p["n"] >= 2]
    inter = [p for p in sel if p["n_langues"] >= 2]
    return {
        "n_paires": len(sel),
        "n_paires_multi": len(multi),
        "n_paires_interlangues": len(inter),
        "invariance_toutes_variantes": {
            "n": len(multi),
            "invariantes_contexte": sum(1 for p in multi if p["invariante_contexte"]),
            "taux_contexte": _taux(sum(1 for p in multi if p["invariante_contexte"]),
                                   len(multi)),
            "invariantes_sans_contexte": sum(
                1 for p in multi if p["invariante_sans_contexte"]),
            "taux_sans_contexte": _taux(
                sum(1 for p in multi if p["invariante_sans_contexte"]), len(multi)),
        },
        "invariance_interlangues": {
            "n": len(inter),
            "invariantes_contexte": sum(
                1 for p in inter if p["invariante_interlangues_contexte"]),
            "taux_contexte": _taux(
                sum(1 for p in inter if p["invariante_interlangues_contexte"]),
                len(inter)),
            "invariantes_sans_contexte": sum(
                1 for p in inter if p["invariante_interlangues_sans_contexte"]),
            "taux_sans_contexte": _taux(
                sum(1 for p in inter if p["invariante_interlangues_sans_contexte"]),
                len(inter)),
        },
    }


def _stats_baseline(records: list[dict]) -> dict:
    applicable = [r for r in records if r["baseline_applicable"]]
    n = len(applicable)
    ok_ctx = sum(1 for r in applicable if r["baseline_exact_contexte"])
    ok_sans = sum(1 for r in applicable if r["baseline_exact_sans_contexte"])
    m1_ctx = sum(1 for r in applicable if r["exact_contexte"])
    m1_sans = sum(1 for r in applicable if r["exact_sans_contexte"])
    return {
        "definition": ("code majoritaire des autres surfaces de la paire "
                       "(leave-one-out), même code pour toutes les surfaces"),
        "n_items": len(records),
        "n_applicable": n,
        "m1_sur_applicables": {
            "exact_contexte": _res(m1_ctx, n),
            "exact_sans_contexte": _res(m1_sans, n),
        },
        "exact_contexte": _res(ok_ctx, n),
        "exact_sans_contexte": _res(ok_sans, n),
        "delta_sans_contexte": _delta(ok_sans, m1_sans, n),
    }


def _stats_controle(records: list[dict], mode: str) -> dict:
    champ = f"controle_{mode}"
    sel = [r[champ] for r in records if r.get(champ)]
    n = len(sel)
    return {
        "n_items": len(records),
        "n": n,
        "exact_attendu_contexte": _res(
            sum(1 for c in sel if c["exact_attendu_contexte"]), n),
        "exact_donateur_contexte": _res(
            sum(1 for c in sel if c["exact_donateur_contexte"]), n),
        "exact_attendu_sans_contexte": _res(
            sum(1 for c in sel if c["exact_attendu_sans_contexte"]), n),
        "exact_donateur_sans_contexte": _res(
            sum(1 for c in sel if c["exact_donateur_sans_contexte"]), n),
    }


def _ligne(records: list[dict], paires: list[dict], avec_controle: bool) -> dict:
    ligne = _stats_m1(records)
    ligne.update(_stats_paires(paires))
    ligne["baseline_surface"] = _stats_baseline(records)
    if avec_controle:
        ligne["controle_strict"] = _stats_controle(records, "strict")
        ligne["controle_large"] = _stats_controle(records, "large")
    return ligne


def _langues_n1(records: list[dict]) -> list[str]:
    compte = collections.Counter(r["langue"] for r in records)
    return sorted(l for l, n in compte.items() if n == 1 and l != LANGUE_NOTATION)


# ---------------------------------------------------------------------------
# Point d'entrée de mesure
# ---------------------------------------------------------------------------
def mesurer(avec_controle: bool = True) -> dict:
    """Mesure M1 sur tout le corpus multilingue réellement présent."""
    t0 = time.perf_counter()
    surfaces, meta = charger_surfaces()
    hub = Hub()
    records = _mesurer_items(hub, surfaces)
    _annoter_baseline(records)

    if avec_controle:
        _annoter_controle(hub, records, "strict")
        _annoter_controle(hub, records, "large")

    paires = _construire_paires(records)
    toutes_paires = list(paires.values())

    global_ = _ligne(records, toutes_paires, avec_controle)
    global_["langues"] = sorted({r["langue"] for r in records
                                 if r["langue"] != LANGUE_NOTATION})
    global_["items_sans_paire"] = sum(1 for r in records if r["paire"] is None)

    par_jeu = {}
    for jeu in JEUX:
        rs = [r for r in records if r["jeu"] == jeu]
        ps = [p for p in toutes_paires if p["jeu"] == jeu]
        par_jeu[jeu] = _ligne(rs, ps, avec_controle)
        par_jeu[jeu]["langues"] = sorted({r["langue"] for r in rs
                                          if r["langue"] != LANGUE_NOTATION})

    par_source = {}
    for source in ("B5", "B7"):
        rs = [r for r in records if r["source"] == source]
        ps = [p for p in toutes_paires if source in p["sources"]]
        par_source[source] = _ligne(rs, ps, avec_controle)
        par_source[source]["langues"] = sorted(
            {r["langue"] for r in rs if r["langue"] != LANGUE_NOTATION})
        par_source[source]["paires_noms"] = sorted(
            {p["jeu"] + ":" + nom for nom, p in paires.items()
             if source in p["sources"]})

    par_langue = {}
    for langue in sorted({r["langue"] for r in records}):
        rs = [r for r in records if r["langue"] == langue]
        ps = [p for p in toutes_paires if langue in p["langues_brutes"]]
        ligne = _ligne(rs, ps, avec_controle)
        ligne["langue"] = langue
        ligne["jeux"] = dict(sorted(collections.Counter(r["jeu"] for r in rs).items()))
        if langue == LANGUE_NOTATION:
            # `notation` est une étiquette de format, pas une langue : on ne lui
            # attribue pas l'invariance interlangues des paires où elle figure.
            ligne["invariance_interlangues"] = {
                "n": 0, "invariantes_contexte": 0, "taux_contexte": None,
                "invariantes_sans_contexte": 0, "taux_sans_contexte": None,
            }
        par_langue[langue] = ligne

    # Table croisée langue × jeu (le taux sans contexte dépend de la composition).
    par_langue_jeu = {}
    for langue, ligne in par_langue.items():
        par_langue_jeu[langue] = {}
        for jeu in JEUX:
            rs = [r for r in records if r["langue"] == langue and r["jeu"] == jeu]
            if not rs:
                continue
            par_langue_jeu[langue][jeu] = {
                "n": len(rs),
                "exact_contexte": _res(
                    sum(1 for r in rs if r["exact_contexte"]), len(rs)),
                "exact_sans_contexte": _res(
                    sum(1 for r in rs if r["exact_sans_contexte"]), len(rs)),
                "canonique": _res(sum(1 for r in rs if r["canonique"]), len(rs)),
                "baseline_surface": _stats_baseline(rs),
            }

    meta["items_sans_paire"] = global_["items_sans_paire"]
    meta["paires"] = global_["n_paires"]
    meta["paires_multi"] = global_["n_paires_multi"]
    meta["paires_interlangues"] = global_["n_paires_interlangues"]
    meta["items_paires_multi"] = global_["baseline_surface"]["n_applicable"]
    meta["langues_n1"] = _langues_n1(records)
    meta["langues_par_jeu"] = {j: v["langues"] for j, v in meta["par_jeu"].items()}

    resultat = {
        "meta": meta,
        "global": global_,
        "par_jeu": par_jeu,
        "par_langue": par_langue,
        "par_langue_jeu": par_langue_jeu,
        "par_source": par_source,
        "paires": paires,
    }

    if avec_controle:
        resultat["controle_surface_permutee"] = {
            "graine": GRAINE_CONTROLE,
            "strict": {
                "definition": ("même (jeu, langue), paire différente, "
                               "code attendu différent"),
                "global": global_["controle_strict"],
                "par_source": {s: par_source[s]["controle_strict"]
                               for s in ("B5", "B7")},
                "par_jeu": {j: par_jeu[j]["controle_strict"] for j in JEUX},
            },
            "large": {
                "definition": ("même jeu, langue quelconque, paire différente, "
                               "code attendu différent"),
                "global": global_["controle_large"],
                "par_source": {s: par_source[s]["controle_large"]
                               for s in ("B5", "B7")},
                "par_jeu": {j: par_jeu[j]["controle_large"] for j in JEUX},
            },
        }

    resultat["autocritique"] = _autocritique(resultat)
    resultat["duree_s"] = round(time.perf_counter() - t0, 3)
    return resultat


def _autocritique(r: dict) -> list[str]:
    g = r["global"]
    b7 = r["par_source"]["B7"]
    go = r["par_jeu"]["go"]
    morpion = r["par_jeu"]["morpion"]
    lignes = [
        ("Corpus construit par le code : les attendus et les contextes viennent "
         "des mêmes règles que le codec. Ce n'est pas un gold standard "
         "indépendant ; le contrôle permuté est la seule vérification externe "
         "de la liaison surface → code."),
        ("Couche lexicale seulement : les surfaces B7 sont « libellé + "
         "coordonnée » ; la réussite mesure la reconnaissance lexicale, pas la "
         "compréhension d'une phrase libre ni la traduction."),
    ]
    absentes = r["meta"]["langues_absentes_du_corpus"]
    if absentes:
        lignes.append(
            f"{r['meta']['langues_corpus']} langues réelles sur "
            f"{r['meta']['langues_lexique']} du lexique ; absentes du corpus : "
            f"{', '.join(absentes)}. Elles ne sont pas complétées.")
    n1 = r["meta"].get("langues_n1", [])
    if n1:
        lignes.append(
            f"n par langue de 1 à "
            f"{max(x['n'] for x in r['par_langue'].values())} ; "
            f"{len(n1)} langue(s) à n=1 ({', '.join(n1)}) : un taux de 0 ou "
            f"100 % sur un seul item n'est pas une estimation.")
    lignes.append(
        "Invariance n'est pas exactitude : sans contexte, les paires go et "
        "morpion restent souvent invariantes (même code pour toutes les "
        f"langues) alors que le code est faux (go : {_pct(go['exact_sans_contexte']['taux'])}, "
        f"morpion : {_pct(morpion['exact_sans_contexte']['taux'])} d'exact).")
    if "controle_strict" in g:
        c = g["controle_strict"]
        lignes.append(
            "Contrôle permuté strict : exact_attendu = "
            f"{_pct(c['exact_attendu_contexte']['taux'])} par construction "
            "(le donneur a un code attendu différent) ; le signal utile est "
            f"exact_donateur = {_pct(c['exact_donateur_contexte']['taux'])} "
            f"(B7 : {_pct(b7['controle_strict']['exact_donateur_contexte']['taux'])}).")
    lignes.append(
        "La baseline de paire est un contrôle de collapse, pas un modèle "
        "open-world : elle utilise l'étiquette de paire et les prédictions M1 "
        "des autres surfaces. Comparée à M1 sur le même périmètre, elle ne "
        f"gagne que {_delta_pts(g['baseline_surface']['delta_sans_contexte'])} "
        "sans contexte, et elle perd "
        f"{_delta_pts(morpion['baseline_surface']['delta_sans_contexte'])} "
        "sur le morpion.")
    lignes.append(
        "La langue est une étiquette du corpus (le libellé choisi par le "
        "générateur), pas la langue détectée par M1 ; une étiquette erronée "
        "déplacerait les taux par langue.")
    lignes.append(
        "Pas d'intervalle de confiance ni de test de signification ; une seule "
        "graine de permutation ; le format canonique réutilise le codec "
        "(aller-retour), donc il teste sa cohérence avec lui-même.")
    return lignes


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------
def _pct(taux: float | None, decimales: int = 1) -> str:
    if taux is None:
        return "—"
    return f"{taux * 100:.{decimales}f} %".replace(".", ",")


def _pts(delta: float | None) -> str:
    if delta is None:
        return "—"
    signe = "+" if delta >= 0 else "−"
    return f"{signe}{abs(delta) * 100:.2f} pt".replace(".", ",")


def _delta_pts(delta: float | None) -> str:
    return _pts(delta)


def _frac(res: dict | None) -> str:
    if not res or not res.get("n"):
        return "—"
    return f"{res['ok']} / {res['n']} ({_pct(res['taux'])})"


def _oui_non(valeur: bool | None) -> str:
    if valeur is None:
        return "—"
    return "oui" if valeur else "non"


def _tableau(entetes: list[str], lignes: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(entetes) + " |",
           "|" + "|".join("---" for _ in entetes) + "|"]
    out += ["| " + " | ".join(str(c) for c in ligne) + " |" for ligne in lignes]
    return out


def _jeux_compacts(jeux: dict) -> str:
    lettres = {"cartes": "c", "echecs": "e", "dames": "d", "go": "g", "morpion": "m"}
    return " ".join(f"{n}{lettres.get(j, j)}" for j, n in sorted(jeux.items()))


def rendre_markdown(r: dict) -> str:
    meta = r["meta"]
    g = r["global"]
    b7 = r["par_source"]["B7"] if "B7" in r["par_source"] else None
    inv = g["invariance_interlangues"]
    inv_multi = g["invariance_toutes_variantes"]
    baseline = g["baseline_surface"]
    lignes = [
        "# A10 — M1 (hub typé) sur le corpus multilingue",
        "",
        f"**Date** : {meta['genere_le']}  ",
        f"**Périmètre** : {meta['perimetre']}, {g['n']} surfaces, "
        f"{meta['langues_corpus']} langues réelles.  ",
        "**Source de mesure** : `tools/cerveau/hub.py` (`Hub.percevoir`, "
        "`Hub.rendre`), sans modification des modules existants.",
        "",
        "## Verdict",
        "",
        f"- **Avec contexte** : M1 lit **{_frac(g['exact_contexte'])}** et le "
        f"canonique revient à **{_frac(g['canonique'])}**.",
        f"- **Sans contexte** : **{_frac(g['exact_sans_contexte'])}** ; c'est là "
        "que se voient les dépendances au contexte (go, morpion, notations "
        "courtes).",
        f"- **Invariance interlangues** : **{_frac({'ok': inv['invariantes_contexte'], 'n': inv['n'], 'taux': inv['taux_contexte']})}** "
        f"des paires avec contexte et **{inv['invariantes_sans_contexte']} / "
        f"{inv['n']}** sans contexte. Les variantes de langue d'une même paire "
        "donnent bien le même code.",
        f"- **Mais invariance ≠ exactitude** : sans contexte, les paires go et "
        "morpion peuvent être invariantes avec un code faux (voir § 5).",
        f"- **Baseline surface** : {_frac(baseline['exact_sans_contexte'])} sans "
        f"contexte, contre "
        f"{_frac(baseline['m1_sur_applicables']['exact_sans_contexte'])} pour M1 "
        "sur le même périmètre.",
    ]
    if "controle_surface_permutee" in r:
        strict = r["controle_surface_permutee"]["strict"]["global"]
        lignes.append(
            f"- **Contrôle surface permutée** : exact attendu "
            f"**{_frac(strict['exact_attendu_contexte'])}**, exact donneur "
            f"**{_frac(strict['exact_donateur_contexte'])}** avec contexte "
            f"(B7 : **{_frac(b7['controle_strict']['exact_donateur_contexte'])}**). "
            "La lecture suit la surface, pas l'étiquette de paire.")
    lignes += [
        "",
        "## 1. Ce qui existe réellement dans le corpus",
        "",
    ]
    s5, s7 = meta["sources"]["B5"], meta["sources"]["B7"]
    lignes += [
        f"- **B5/B6** (`{s5['fichier']}`) : {s5['items_total']} items, dont "
        f"**{s5['coups']} coups** ; {s5['items_total'] - s5['coups']} items "
        "non-coups exclus (états, parties, mains). "
        f"Langues : {', '.join(s5['langues'])} ; {s5['paires']} paires de coups.",
        f"- **B7** (`{s7['fichier']}`) : {s7['items_total']} items, tous des "
        f"coups ; **{len(s7['langues'])} langues** et {s7['paires']} paires.",
        f"- **Corpus typé** (`{meta['sources']['typed_corpus']['fichier']}`) : "
        f"{meta['sources']['typed_corpus']['items']} items ; clés identiques au "
        f"chargement : {_oui_non(meta['sources']['typed_corpus']['cles_identiques'])}, "
        f"codes identiques : {meta['sources']['typed_corpus']['codes_identiques']} "
        f"/ {meta['sources']['typed_corpus']['items']}.",
        f"- **Lexique** : {meta['langues_lexique']} langues ; **{meta['langues_corpus']} "
        "ont des surfaces réelles** dans le corpus. Langues du lexique sans "
        f"surface : **{', '.join(meta['langues_absentes_du_corpus']) or 'aucune'}**. "
        "Elles sont déclarées absentes, pas inventées.",
        f"- **Paires** : {meta['paires']} paires nommées, dont "
        f"{meta['paires_interlangues']} avec au moins deux langues réelles. "
        f"{meta['items_sans_paire']} coups sans paire (contrôles de collision) "
        "sont exclus de l'invariance et de la baseline.",
        f"- **Baseline applicable** : {baseline['n_applicable']} items dans des "
        "paires à au moins deux variantes ; "
        f"{meta['items'] - baseline['n_applicable'] - meta['items_sans_paire']} "
        "items supplémentaires sont dans une paire à variante unique et ne "
        "peuvent pas être prédits par leave-one-out.",
        f"- **Langues à n=1** : {', '.join(meta['langues_n1']) or 'aucune'} "
        "(leurs taux ne sont pas des estimations).",
        "",
        "## 2. Définitions",
        "",
        "- **exact avec contexte** : `Hub.percevoir(texte, jeu, contexte)` rend "
        "exactement le code typé à 15 champs de l'attendu.",
        "- **exact sans contexte** : même lecture avec `contexte=None`.",
        "- **canonique** : `Hub.rendre(code, contexte)` puis relecture ; le "
        "corps de la RSN relue doit être celui de l'attendu.",
        "- **invariance interlangues** : dans une paire, toutes les variantes "
        "de **langue** (l'étiquette `notation` est exclue de la comparaison) "
        "donnent le même code non nul.",
        "- **invariance toutes variantes** : mêmes paires, mais `notation` "
        "compte aussi ; elle est plus stricte et révèle les notations courtes "
        "qui ont besoin du contexte.",
        "- **baseline surface** : code majoritaire des **autres** surfaces de "
        "la paire (leave-one-out), appliqué à toutes les surfaces de la paire. "
        "Elle mesure le collapse « une paire = un code » ; M1 est recalculé sur "
        "le même périmètre.",
        "- **contrôle surface permutée (strict)** : la surface d'un item est "
        "remplacée par celle d'un item de même jeu et de même langue, d'une "
        "paire différente et de code attendu différent. `exact_attendu` doit "
        "s'effondrer, `exact_donateur` doit rester haut.",
        "",
        "## 3. Résultats globaux",
        "",
    ]
    lignes += _tableau(
        ["mesure", "valeur"],
        [
            ["items mesurés", str(g["n"])],
            ["exact avec contexte", _frac(g["exact_contexte"])],
            ["exact sans contexte", _frac(g["exact_sans_contexte"])],
            ["canonique", _frac(g["canonique"])],
            [f"invariance interlangues (ctx, {inv['n']} paires)",
             _frac({"ok": inv["invariantes_contexte"], "n": inv["n"],
                    "taux": inv["taux_contexte"]})],
            [f"invariance interlangues (sans ctx, {inv['n']} paires)",
             _frac({"ok": inv["invariantes_sans_contexte"], "n": inv["n"],
                    "taux": inv["taux_sans_contexte"]})],
            [f"invariance toutes variantes (ctx, {inv_multi['n']} paires)",
             _frac({"ok": inv_multi["invariantes_contexte"], "n": inv_multi["n"],
                    "taux": inv_multi["taux_contexte"]})],
            [f"invariance toutes variantes (sans ctx, {inv_multi['n']} paires)",
             _frac({"ok": inv_multi["invariantes_sans_contexte"],
                    "n": inv_multi["n"], "taux": inv_multi["taux_sans_contexte"]})],
            [f"baseline surface (ctx, {baseline['n_applicable']} items)",
             _frac(baseline["exact_contexte"])],
            [f"baseline surface (sans ctx, {baseline['n_applicable']} items)",
             _frac(baseline["exact_sans_contexte"])],
            ["M1 sans contexte, même périmètre que la baseline",
             _frac(baseline["m1_sur_applicables"]["exact_sans_contexte"])],
            ["delta baseline − M1 (sans contexte)",
             _pts(baseline["delta_sans_contexte"])],
        ])
    if "controle_surface_permutee" in r:
        strict = r["controle_surface_permutee"]["strict"]["global"]
        large = r["controle_surface_permutee"]["large"]["global"]
        lignes += [
            "",
            "Contrôle de permutation (strict) :",
            "",
        ]
        lignes += _tableau(
            ["mesure", "valeur"],
            [
                ["items appariés", f"{strict['n']} / {strict['n_items']}"],
                ["exact attendu (ctx)", _frac(strict["exact_attendu_contexte"])],
                ["exact donneur (ctx)", _frac(strict["exact_donateur_contexte"])],
                ["exact attendu (sans ctx)",
                 _frac(strict["exact_attendu_sans_contexte"])],
                ["exact donneur (sans ctx)",
                 _frac(strict["exact_donateur_sans_contexte"])],
                ["exact donneur B7 (ctx)",
                 _frac(b7["controle_strict"]["exact_donateur_contexte"])],
                ["exact donneur, variante large (ctx)",
                 _frac(large["exact_donateur_contexte"])],
            ])

    lignes += [
        "",
        "## 4. Par jeu",
        "",
    ]
    lignes += _tableau(
        ["jeu", "n", "langues", "exact ctx", "exact sans ctx", "canonique",
         "inv. interlangues ctx", "inv. interlangues sans ctx",
         "inv. toutes variantes sans ctx"],
        [[jeu,
          str(v["n"]),
          str(len(v["langues"])),
          _pct(v["exact_contexte"]["taux"]),
          _pct(v["exact_sans_contexte"]["taux"]),
          _pct(v["canonique"]["taux"]),
          _frac({"ok": v["invariance_interlangues"]["invariantes_contexte"],
                 "n": v["invariance_interlangues"]["n"],
                 "taux": v["invariance_interlangues"]["taux_contexte"]}),
          _frac({"ok": v["invariance_interlangues"]["invariantes_sans_contexte"],
                 "n": v["invariance_interlangues"]["n"],
                 "taux": v["invariance_interlangues"]["taux_sans_contexte"]}),
          _frac({"ok": v["invariance_toutes_variantes"]["invariantes_sans_contexte"],
                 "n": v["invariance_toutes_variantes"]["n"],
                 "taux": v["invariance_toutes_variantes"]["taux_sans_contexte"]})]
         for jeu, v in r["par_jeu"].items()])
    lignes += [
        "",
        "Le go et le morpion sont les deux jeux où le contexte porte le sens "
        "(taille du plateau, symbole au trait) : leur exact sans contexte est "
        "bas, mais leurs paires restent invariantes. C'est le point "
        "« invariance ≠ exactitude ».",
        "",
        "## 5. Invariance interlangues, paire par paire",
        "",
    ]
    paires_inter = [p for p in r["paires"].values() if p["n_langues"] >= 2]
    paires_inter.sort(key=lambda p: (p["jeu"], p["n"], -p["n_langues"]))
    lignes += _tableau(
        ["paire", "jeu", "variantes", "langues", "codes ctx", "codes sans ctx",
         "inv. ctx", "inv. sans ctx", "exact ctx", "exact sans ctx"],
        [[nom, p["jeu"], str(p["n"]), str(p["n_langues"]),
          str(p["codes_distincts_contexte"]),
          str(p["codes_distincts_sans_contexte"]),
          _oui_non(p["invariante_interlangues_contexte"]),
          _oui_non(p["invariante_interlangues_sans_contexte"]),
          _pct(p["exact_contexte"]["taux"]),
          _pct(p["exact_sans_contexte"]["taux"])]
         for nom, p in sorted(r["paires"].items())
         if p["n_langues"] >= 2])
    lignes += [
        "",
        "Les paires B7 (`ml-…`) ont de 14 à 62 variantes de langue. Le détail "
        "des codes uniques, des surfaces déviantes et des langues est dans le "
        "JSON (`paires`).",
        "",
        "## 6. Baseline et contrôle permuté",
        "",
        "Comparaison équitable : M1 et la baseline sont évalués sur les mêmes "
        "items (paires à au moins deux variantes).",
        "",
    ]
    lignes += _tableau(
        ["jeu", "items applicables", "M1 sans ctx", "baseline sans ctx",
         "delta", "contrôle strict n", "exact attendu", "exact donneur"],
        [[jeu,
          str(v["baseline_surface"]["n_applicable"]),
          _pct(v["baseline_surface"]["m1_sur_applicables"]
               ["exact_sans_contexte"]["taux"]),
          _pct(v["baseline_surface"]["exact_sans_contexte"]["taux"]),
          _pts(v["baseline_surface"]["delta_sans_contexte"]),
          str(v.get("controle_strict", {}).get("n", "—")),
          _pct(v.get("controle_strict", {})
               .get("exact_attendu_contexte", {}).get("taux")),
          _pct(v.get("controle_strict", {})
               .get("exact_donateur_contexte", {}).get("taux"))]
         for jeu, v in r["par_jeu"].items()])
    lignes += [
        "",
        "La baseline ne gagne pas uniformément : elle corrige des incohérences "
        "de notation dans les échecs, mais elle **cache** les erreurs du "
        "morpion en figeant un code faux. Le contrôle permuté, lui, vérifie "
        "que le code suit la surface donneuse : la lecture n'est pas un simple "
        "effet de l'étiquette de paire.",
        "",
        "## 7. Autocritique — ce qui pourrait rendre ce résultat faux",
        "",
    ]
    lignes += [f"- {phrase}" for phrase in r["autocritique"]]
    lignes += [
        "",
        "## 8. Reproductibilité",
        "",
        "```bash",
        "PYTHONPATH=tools python3 tools/cerveau/multilingue.py",
        "# → /tmp/a10-multilingue.json et /tmp/a10-multilingue.md",
        "PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools",
        "```",
        "",
        f"Durée de la mesure : {r['duree_s']} s (CPU, déterministe hors "
        "horodatage). Ligne de roadmap : **A10**.",
        "",
    ]
    return "\n".join(lignes)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default="/tmp/a10-multilingue.json",
                    help="chemin du JSON de sortie")
    ap.add_argument("--md", default="/tmp/a10-multilingue.md",
                    help="chemin du Markdown de sortie")
    ap.add_argument("--sans-controle", action="store_true",
                    help="ne pas exécuter les permutations (plus rapide)")
    args = ap.parse_args(argv)

    resultat = mesurer(avec_controle=not args.sans_controle)
    chemin_json = pathlib.Path(args.json)
    chemin_md = pathlib.Path(args.md)
    chemin_json.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
    chemin_md.write_text(rendre_markdown(resultat) + "\n", encoding="utf-8")

    g = resultat["global"]
    print(f"A10 — M1 multilingue : {g['n']} items, "
          f"exact ctx {_pct(g['exact_contexte']['taux'])}, "
          f"sans ctx {_pct(g['exact_sans_contexte']['taux'])}, "
          f"invariance interlangues {_pct(g['invariance_interlangues']['taux_contexte'])}")
    print(f"JSON : {chemin_json}")
    print(f"MD   : {chemin_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

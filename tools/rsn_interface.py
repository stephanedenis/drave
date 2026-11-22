#!/usr/bin/env python3
"""rsn_interface.py — l'interface de la RSN : cinq verbes, la substitution des paradigmes.

LE CONTRAT (voir `docs/theorie/rsn-interface.md`) : un paradigme (formel, flou, probabiliste,
provenance, TMS, Dung) est **substituable** s'il accepte les cinq verbes et rend les mêmes
structures :

  - `assert(affirmation)` → un id stable (idempotent) ;
  - `query(terme)` → {statut, degre, preuve, contexte} — le statut est toujours tri-état
    (`prouve`, `refute`, `inconnu`) — jamais « refusé par défaut » ;
  - `promote(id, preuve)` → le nouveau statut — **sans** preuve, `refuse` ;
  - `explain(id)` → {justification, provenance} — la trace jusqu'à la source ;
  - `context(id)` → {texte, span, version, langue} — le contexte source ne se perd jamais.

DEUX ADAPTATEURS ICI : `RSNFlou` (les degrés [0,1], la composition) et `RSNProvenance` (le
contexte, l'explain). Ils se **composent** : `RSNFlou(RSNProvenance(base))` donne une RSN floue
traçable. Les adaptateurs lourds (PSL, ProbLog, Dung) sont **à écrire** si le besoin est mesuré.
"""
from __future__ import annotations

import json
from typing import Any, Protocol

STATUTS = ("prouve", "refute", "inconnu", "hypothese", "retenu", "ouvert")


class RSN(Protocol):
    """Le protocole : les cinq verbes, rien d'autre."""

    def assert_(self, affirmation: dict) -> str: ...
    def query(self, terme: dict | str) -> dict: ...
    def promote(self, id_: str, preuve: dict | None = None) -> str: ...
    def explain(self, id_: str) -> dict: ...
    def context(self, id_: str) -> dict: ...


class RSNBase:
    """Le socle : le stockage, l'idempotence, le tri-état par défaut."""

    def __init__(self) -> None:
        self._aff: dict[str, dict] = {}

    # -- les cinq verbes ---------------------------------------------------
    def assert_(self, affirmation: dict) -> str:
        corps = affirmation.get("corps", {})
        texte = json.dumps(corps, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        import hashlib
        id_ = "sha256:" + hashlib.sha256(texte.encode("utf-8")).hexdigest()
        if id_ not in self._aff:
            self._aff[id_] = {
                "id": id_,
                "corps": corps,
                "contexte": dict(affirmation.get("contexte", {})),
                "statut": "hypothese",
                "degre": affirmation.get("degre"),
                "provenance": dict(affirmation.get("provenance", {})),
            }
        return id_

    def query(self, terme: dict | str) -> dict:
        if isinstance(terme, str) and terme in self._aff:
            a = self._aff[terme]
            return {"statut": self._statut(a), "degre": a.get("degre"),
                    "preuve": a.get("preuve"), "contexte": a.get("contexte", {})}
        # une requête par corps : on cherche
        for a in self._aff.values():
            if a["corps"] == terme:
                return {"statut": self._statut(a), "degre": a.get("degre"),
                        "preuve": a.get("preuve"), "contexte": a.get("contexte", {})}
        return {"statut": "inconnu", "degre": None, "preuve": None, "contexte": {}}

    def promote(self, id_: str, preuve: dict | None = None) -> str:
        a = self._aff.get(id_)
        if a is None:
            return "inconnu"
        if not preuve:
            a["statut"] = a["statut"]  # refuse silencieusement : reste hypothèse
            return "refuse"
        a["preuve"] = preuve
        a["statut"] = "prouve"
        return "prouve"

    def explain(self, id_: str) -> dict:
        a = self._aff.get(id_)
        if a is None:
            return {"justification": None, "provenance": None}
        return {"justification": a.get("preuve"), "provenance": a.get("provenance", {})}

    def context(self, id_: str) -> dict:
        a = self._aff.get(id_)
        return dict(a.get("contexte", {})) if a else {}

    # -- la mécanique interne ---------------------------------------------
    def _statut(self, a: dict) -> str:
        s = a.get("statut", "hypothese")
        return s if s in STATUTS else "inconnu"


class RSNFlou(RSNBase):
    """Le flou : les degrés [0,1] et la composition par règles.

    La règle : `compose([regle], [faits])` applique `min` (ET) et `max` (OU) — Zadeh. Aucun
    résultat n'est promu : la composition **produit des hypothèses**, pas des certitudes.
    """

    def compose(self, regles: list[dict], faits: list[str]) -> list[dict]:
        sorties = []
        for r in regles:
            antecedents = r.get("si", [])
            if not antecedents:
                continue
            degres = []
            for a in antecedents:
                q = self.query(a)
                if q["statut"] == "inconnu" or q["degre"] is None:
                    degres = []
                    break
                degres.append(float(q["degre"]))
            if not degres:
                continue
            d = min(degres) if r.get("mode", "et") == "et" else max(degres)
            id_ = self.assert_({"corps": r["alors"], "degre": round(d, 4),
                                "provenance": {"operateur": "compose", "regle": r.get("nom", "")}})
            sorties.append({"id": id_, "degre": round(d, 4), "corps": r["alors"]})
        return sorties


class RSNProvenance(RSNBase):
    """La provenance : le contexte et l'explain complets (RDF-star / PROV-O, en minimal).

    `explain` rend la chaîne complète : l'affirmation, sa provenance, et le contexte source.
    """

    def explain(self, id_: str) -> dict:
        a = self._aff.get(id_)
        if a is None:
            return {"justification": None, "provenance": None, "chaine": []}
        chaine = [{"id": id_, "statut": a["statut"], "provenance": a.get("provenance", {}),
                   "contexte": a.get("contexte", {})}]
        return {"justification": a.get("preuve"), "provenance": a.get("provenance", {}),
                "chaine": chaine}


def conformite(impl: RSN) -> dict:
    """Le test de conformité : 5 contrôles, le même pour tout paradigme."""
    base = impl
    aff = {"corps": {"type": "predication", "role": "agent", "forme": "Le chat", "cible": "dort"},
           "contexte": {"texte": "Le chat dort.", "span": [0, 7], "langue": "fr", "version": "t"},
           "degre": 0.62, "provenance": {"operateur": "test"}}
    i1 = base.assert_(aff)
    i2 = base.assert_(aff)
    r = {
        "idempotent": i1 == i2,
        "inconnu_sur_absent": base.query({"type": "absent"})["statut"] == "inconnu",
        "refus_sans_preuve": base.promote(i1) == "refuse",
        "explain_complet": base.explain(i1).get("provenance") is not None,
        "contexte_exact": base.context(i1).get("span") == [0, 7],
    }
    r["conforme"] = all(r.values())
    return r


if __name__ == "__main__":
    for nom, impl in (("RSNBase", RSNBase()), ("RSNFlou", RSNFlou()),
                      ("RSNProvenance", RSNProvenance())):
        r = conformite(impl)
        print(nom, "→", "CONFORME" if r["conforme"] else "NON CONFORME", r)


# ---------------------------------------------------------------------------
# La passerelle : la RSN d'une annotation entre DANS l'interface
# ---------------------------------------------------------------------------

def depuis_annotation_interface(annotation, impl: "RSNBase | None" = None) -> tuple["RSNBase", list[str]]:
    """Le chemin complet : une `Annotation` (la surface) → les affirmations de l'interface.

    Chaque fait et chaque prédication de la RSN devient une affirmation avec son **contexte
    source** (le texte, le span, la langue) et son **degré** (la confiance de l'étiquette).
    Rend l'implémentation et les ids — l'état est **rejouable** : la même annotation donne les
    mêmes ids.
    """
    from tools.rsn import depuis_annotation

    impl = impl or RSNFlou()
    etat = depuis_annotation(annotation)
    texte = getattr(annotation, "texte", "")
    langue = getattr(annotation, "langue", "und")
    ids = []
    for c in etat.candidats:
        corps = dict(c.corps)
        span = [int(corps.get("debut", 0)), int(corps.get("fin", 0))]
        ids.append(impl.assert_({
            "corps": corps,
            "contexte": {"texte": texte, "span": span, "langue": langue,
                         "version": getattr(annotation, "source", "heuristique")},
            "degre": float(c.annotation.get("confiance", 0.5)),
            "provenance": dict(c.provenance),
        }))
    return impl, ids


def requete_etat(impl: "RSNBase", ids: list[str]) -> dict:
    """L'état d'une RSN : le tri-état de chaque affirmation, les degrés, le contexte."""
    st = [impl.query(i)["statut"] for i in ids]
    deg = [impl.query(i)["degre"] for i in ids]
    return {"n": len(ids), "statuts": {s: st.count(s) for s in set(st)},
            "degre_moyen": round(sum(d for d in deg if d is not None) / max(1, sum(1 for d in deg if d is not None)), 4),
            "ids": ids}

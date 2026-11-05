"""replis_cible.py — prototype **autonome** des trois retouches de repli (A10).

**Statut (2026-11-05)** : prototype **non intégré**. Sur le bloc v3, les trois retouches
valent +4 net (145/145 exact sur les 145 segments au bon span) mais sont **dessinées sur
les cas** : la fiche `reports/rapport-replis-cible.md` recommande un gold tenu à l'écart
avant intégration. Les règles générales de la v3 (R2 hors-span, R3 cible vide génitive,
R4 enclitiques) sont, elles, intégrées.
"""

"""replis_cible.py — prototype **autonome** des trois retouches d'attachement de A3.

Le problème. La fiche `reports/rapport-classement-appris.md` (B13) recommande trois
retouches déterministes après avoir constaté que le classement appris réparait 7 des 8
erreurs de la règle live, mais en introduisait 2 :

1. **repli quand la cible est vide** (`g002`, `s041`) ;
2. **préférence d'un verbe sur un nom proche** (`g012`, `r018`, `s108`, `s122`) ;
3. **complétive en tête de phrase** (`r309`).

Ce fichier mesure ces trois retouches **sans modifier `bloc_linguistique.py`**. Il
sous-classe `Heuristique` et post-traite les cibles déjà calculées : pour chaque étiquette
`syntagme` non-`GV`, il relit `meta.attachement.cible`, construit le **vivier ordonné** de
la phrase (mêmes tokens pleins que `classement_cible.py` : POS ouverte ou `_est_verbe`,
auxiliaires exclus ; ordre gauche → droite → dedans, puis distance), et applique la
retouche demandée. Un run sans retouche reproduit exactement la règle live (contrôle de
fidélité) ; les métriques sont celles de `evaluer_gold.evaluer_bloc`.

Les trois retouches, telles que simulées :

- **R1 — repli cible vide** : cible absente/vide et segment non-`GV` → `rang 0` du vivier
  (token plein le plus proche, gauche d'abord). Variante « tous types » et témoins
  « dernier candidat », « premier verbe du lexique ».
- **R2 — préférence de tête** (forme qui reproduit le +4 de A3) : pour un `GP`, si la
  cible n'est pas déjà un **verbe plein reconnu hors du segment**, prendre le `rang 0` du
  vivier. La variante **littérale** demandée par A3 (« préférer un verbe à un nom ») est
  mesurée séparément : elle ne répare rien avec le lexique de base, +2 seulement si on y
  ajoute `rêve`/`saute` (les deux cibles du gold), et 6 régressions si on utilise le POS
  au lieu du lexique. Elle ne peut pas réparer `g012`/`r018`, dont le gold est un adjectif
  (`prêt`/`prête`), pas un verbe.
- **R3 — complétive en tête** : pour un `SUB`, si la cible n'est pas un token candidat,
  qu'aucun candidat n'est à gauche et qu'il y a un candidat dedans, prendre le **dernier
  candidat intérieur** (le verbe de la complétive). Variante large (tout `SUB` → intérieur)
  mesurée comme contrôle négatif.

Ce que le banc ne fait pas. Il ne touche ni au span, ni au vivier de `candidats` (le top-k
reste donc inchangé), ni au lexique. Il simule la **décision de cible** par un
post-traitement, pas un diff littéral : une intégration réelle devrait placer les mêmes
conditions au bon endroit dans `analyser`, puis repasser les portes. Les cas réparés par
R1/R2/R3 ont servi à **définir** les règles : les gains sont des bornes hautes, pas une
estimation de généralisation (pas de gold tenu à l'écart). La règle live bouge : le JSON
fige l'empreinte lue et dit si le fichier a changé pendant le run.

Le script n'écrit que `reports/pensee-replis-cible.json` (chemin surchargeable par
`--json`) ; il ne modifie aucun fichier existant et n'importe pas `bloc_linguistique.py`
en écriture. Aucune dépendance nouvelle (bibliothèque standard seulement).
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # n'écrit pas de __pycache__ dans le dépôt

import argparse
import datetime
import hashlib
import json
import math
import pathlib
from collections import Counter

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
sys.path.insert(0, str(RACINE / "tools" / "tests" / "linguistique"))

import bloc_linguistique as bl  # noqa: E402
from evaluer_gold import charger, evaluer_bloc  # noqa: E402

SORTIE_DEFAUT = RACINE / "reports" / "pensee-replis-cible.json"
TYPES = ("GP", "REL", "SUB")
POS_OUVERTES = {"NOUN", "PROPN", "VERB", "ADJ"}
# deux verbes du gold absents de VERBES_CONNUS ; utilisés uniquement par la variante
# « lexique étendu » de R2, jamais par la variante principale.
LEXIQUE_ETENDU = frozenset({"rêve", "rêves", "rêvent", "rêvait", "saute", "sautes",
                            "sautent", "sautait"})


# --------------------------------------------------------------------------- corpus
def _cibles(segment: dict) -> list[str]:
    return segment.get("cibles") or ([segment["cible"]] if segment.get("cible") else [])


def _labels(annotation) -> dict:
    """Les étiquettes `syntagme` par (type, debut, fin) ; la dernière gagne, comme
    `evaluer_gold._tete`/`evaluer_bloc` qui construisent le même dictionnaire."""
    return {(e.type, e.debut, e.fin): e
            for e in annotation.etiquettes if e.niveau == "syntagme"}


def _pos(annotation) -> dict:
    return {(e.debut, e.fin): e.type for e in annotation.etiquettes if e.niveau == "pos"}


def _cible_de(etiquette) -> str:
    att = (etiquette.meta or {}).get("attachement") or {}
    return (att.get("cible") or "").strip()


def _top1(cible: str, gold: list[str]) -> bool:
    """Le top1 de `evaluer_gold.evaluer_bloc` : non vide et sous-chaîne d'une cible."""
    return bool(cible and any(c in cible or cible in c for c in gold))


def _pos_gold(phrase: dict, token: str) -> str | None:
    for m in phrase.get("mots", []):
        if phrase["texte"][m["debut"]:m["fin"]] == token:
            return m["pos"]
    return None


def _nature_gold(phrase: dict, token: str) -> str:
    """verbe / nom / autre, en suivant le POS du gold (comme `evaluer_gold`)."""
    if not token:
        return "vide"
    p = _pos_gold(phrase, token)
    if p == "VERB":
        return "verbe"
    if p in ("NOUN", "PROPN", "ADJ"):
        return "nom"
    if p:
        return "autre"
    return "verbe" if bl._est_verbe(token) else "nom"


# --------------------------------------------------------------------------- vivier
def _candidats(texte: str, annotation, segment: dict) -> list[dict]:
    """Le vivier ordonné d'un segment, sans le gold.

    Tokens pleins = POS ouverte ou `_est_verbe`, auxiliaires exclus. Ordre : gauche →
    droite → dedans, puis distance au segment, puis position dans la phrase. C'est
    exactement l'ordre du prototype `classement_cible.py`, réutilisé ici pour que les
    trois retouches parlent le même langage que A3.
    """
    pos = _pos(annotation)
    mots = bl.Heuristique._mots(texte)
    indices = [i for i, (d, f, _t, _ty) in enumerate(mots)
               if d >= segment["debut"] and f <= segment["fin"]]
    if not indices:
        return []
    i_min, i_max = min(indices), max(indices)
    sortie = []
    for i, (d, f, t, typ) in enumerate(mots):
        if typ != "mot" or bl._normaliser(t) in bl.AUXILIAIRES:
            continue
        p = pos.get((d, f), "")
        if p in POS_OUVERTES or bl._est_verbe(t):
            if i_min <= i <= i_max:
                cote, distance = "dedans", 0
            elif i < i_min:
                cote, distance = "gauche", i_min - i
            else:
                cote, distance = "droite", i - i_max
            sortie.append({"i": i, "texte": t, "debut": d, "fin": f, "pos": p,
                           "verbe_lexique": bl._est_verbe(t),
                           "cote": cote, "distance": distance})
    ordre = {"gauche": 0, "droite": 1, "dedans": 2}
    sortie.sort(key=lambda c: (ordre[c["cote"]], c["distance"], c["i"]))
    for rang, c in enumerate(sortie):
        c["rang"] = rang
    return sortie


# --------------------------------------------------------------------------- retouches
class HeuristiqueReplis(bl.Heuristique):
    """`Heuristique` + post-traitement des cibles (aucune modification du bloc).

    Chaque retouche est une fonction pure sur (vivier, cible courante) ; le
    post-traitement ne change que `meta.attachement.cible`, jamais les candidats ni le
    span. C'est la simulation de la **décision** de cible, pas un patch du code.
    """

    def __init__(self, t1: str | None = None, t1_scope: str = "GP",
                 t2: str | None = None, t2_scope: str = "GP",
                 t3: str | None = None, extra_lex=frozenset()):
        super().__init__()
        self.t1 = t1
        self.t1_scope = t1_scope
        self.t2 = t2
        self.t2_scope = t2_scope
        self.t3 = t3
        self.extra_lex = frozenset(extra_lex)

    def _est_verbe(self, token: str) -> bool:
        return bl._est_verbe(token) or bl._normaliser(token) in self.extra_lex

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None):
        annotation = super().analyser(texte, langue, contexte)
        if self.t1 or self.t2 or self.t3:
            self._appliquer(annotation, texte)
        return annotation

    def _appliquer(self, annotation, texte: str) -> None:
        syntagmes = [x for x in annotation.etiquettes if x.niveau == "syntagme"]
        for etiquette in annotation.etiquettes:
            if etiquette.niveau != "syntagme" or etiquette.type == "GV":
                continue
            segment = {"type": etiquette.type, "debut": etiquette.debut,
                       "fin": etiquette.fin, "texte": etiquette.valeur}
            candidats = _candidats(texte, annotation, segment)
            if not candidats:
                continue
            meta = etiquette.meta or {}
            att = meta.get("attachement") or {}
            ancienne = (att.get("cible") or "").strip()
            cible = ancienne

            # R1 — repli cible vide : rang 0 du vivier.
            if self.t1 and not cible and (self.t1_scope == "tous"
                                          or etiquette.type == self.t1_scope):
                if self.t1 == "rang0":
                    cible = candidats[0]["texte"]
                elif self.t1 == "dernier":
                    cible = candidats[-1]["texte"]
                elif self.t1 == "verbe":
                    cible = next((c["texte"] for c in candidats
                                  if self._est_verbe(c["texte"])), "")

            actuel = next((c for c in candidats if c["texte"] == cible), None)

            # R2 — préférence de tête (garde le verbe gouverneur déjà choisi).
            if self.t2 and cible and (self.t2_scope == "tous"
                                      or etiquette.type == self.t2_scope):
                if self.t2 == "rang0_brut":
                    cible = candidats[0]["texte"]
                elif self.t2 == "rang0":
                    if actuel is None or not (self._est_verbe(cible)
                                              and actuel["cote"] != "dedans"):
                        cible = candidats[0]["texte"]
                elif self.t2 == "etroite":
                    # la cible n'est pas un verbe reconnu et un candidat est strictement
                    # plus proche, hors du segment : c'est la forme minimale qui répare
                    # s108/s122 sans toucher aux GV intérieurs ni aux verbes gouverneurs.
                    if (actuel is not None and not self._est_verbe(cible)
                            and candidats[0]["distance"] < actuel["distance"]
                            and candidats[0]["cote"] != "dedans"):
                        cible = candidats[0]["texte"]
                elif self.t2 in ("litteral", "litteral_pos"):
                    if actuel is not None:
                        if self.t2 == "litteral":
                            deja_verbe = self._est_verbe(cible)
                        else:
                            deja_verbe = actuel["pos"] == "VERB"
                        if not deja_verbe:
                            distance = actuel["distance"]
                            if self.t2 == "litteral":
                                verbes = [c for c in candidats
                                          if self._est_verbe(c["texte"])
                                          and c["distance"] <= distance]
                            else:
                                verbes = [c for c in candidats
                                          if c["pos"] == "VERB"
                                          and c["distance"] <= distance]
                            if verbes:
                                cible = verbes[0]["texte"]

            # R3 — complétive en tête.
            if self.t3 and cible and etiquette.type == "SUB":
                dedans = [c for c in candidats if c["cote"] == "dedans"]
                gauche = [c for c in candidats if c["cote"] == "gauche"]
                if self.t3 == "large":
                    if dedans:
                        cible = dedans[-1]["texte"]
                elif self.t3 == "etroite":
                    # complétive en tête : la cible actuelle est le texte du segment
                    # qui précède (un GV mal étiqueté), pas un token candidat.
                    avant = [x for x in syntagmes
                             if x is not etiquette and x.fin <= etiquette.debut]
                    precedent = max(avant, key=lambda x: x.fin) if avant else None
                    if (precedent is not None and cible == precedent.valeur
                            and cible not in {c["texte"] for c in candidats}
                            and not gauche and dedans):
                        cible = dedans[-1]["texte"]

            if cible and cible != ancienne:
                meta = dict(meta)
                meta["attachement"] = {"segment": att.get("segment", etiquette.valeur),
                                       "cible": cible}
                etiquette.meta = meta


# --------------------------------------------------------------------------- mesures
def _resume_attachement(att: dict) -> dict:
    return {k: att[k] for k in ("cibles", "labels", "top1", "topk", "exact",
                                "top1_taux", "top1_taux_span", "topk_taux",
                                "topk_taux_span", "exact_taux", "exact_taux_span",
                                "topk_exact", "topk_exact_taux",
                                "topk_exact_taux_span", "couverture")}


def _collecter(bloc, phrases: list[dict]) -> tuple[dict, dict, dict]:
    """(mesures par segment, cibles par phrase, types par span) pour un bloc.

    `mesures` ne contient que les 145 segments gold dont le span est prédit ; c'est la
    population de `evaluer_gold`. `cibles` sert à la surface de changement et au Q1.
    """
    mesures = {}
    par_phrase = {}
    types_span = {}
    for phrase in phrases:
        annotation = bloc.analyser(phrase["texte"], phrase["langue"])
        labels = _labels(annotation)
        par_phrase[phrase["id"]] = {span: _cible_de(e) for span, e in labels.items()}
        for span, e in labels.items():
            types_span[(phrase["id"],) + span] = e.type
        for segment in phrase["segments"]:
            cibles = _cibles(segment)
            if not cibles:
                continue
            etiquette = labels.get((segment["type"], segment["debut"], segment["fin"]))
            if etiquette is None:
                continue
            cible = _cible_de(etiquette)
            mesures[(phrase["id"], segment["type"], segment["debut"], segment["fin"])] = {
                "id": phrase["id"], "source": phrase["source"],
                "type": segment["type"], "debut": segment["debut"],
                "fin": segment["fin"], "segment": segment.get("texte", ""),
                "gold": cibles[0], "gold_all": cibles,
                "gold_nature": _nature_gold(phrase, cibles[0]),
                "cible": cible, "nature": _nature_gold(phrase, cible) if cible else "vide",
                "cible_dans_gold": bool(cible and _pos_gold(phrase, cible)),
                "exact": cible == cibles[0], "top1": _top1(cible, cibles),
            }
    return mesures, par_phrase, types_span


def _gold_spans(phrases: list[dict]) -> set:
    return {(p["id"], s["type"], s["debut"], s["fin"])
            for p in phrases for s in p["segments"] if _cibles(s)}


def _diff(baseline: dict, variante: dict) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """(gains exact, régressions exact, gains top1, régressions top1)."""
    gains, regs, gains_t1, regs_t1 = [], [], [], []
    for cle, b in baseline.items():
        v = variante.get(cle)
        if v is None:
            continue
        resume = {"id": b["id"], "type": b["type"], "segment": b["segment"],
                  "gold": b["gold"], "gold_all": b["gold_all"],
                  "avant": b["cible"], "apres": v["cible"]}
        if v["exact"] and not b["exact"]:
            gains.append(resume)
        if b["exact"] and not v["exact"]:
            regs.append(resume)
        if v["top1"] and not b["top1"]:
            gains_t1.append(resume)
        if b["top1"] and not v["top1"]:
            regs_t1.append(resume)
    return gains, regs, gains_t1, regs_t1


def _surface(baseline_par_phrase: dict, variante_par_phrase: dict,
             gold_spans: set, phrases: list[dict], exemples_max: int = 12) -> dict:
    """Combien d'étiquettes changent, et combien sont hors des 239 cibles gold."""
    textes = {p["id"]: p["texte"] for p in phrases}
    changed = Counter()
    changed_gold = Counter()
    changed_autres = Counter()
    exemples = []
    spans_total = 0
    for pid, base in baseline_par_phrase.items():
        var = variante_par_phrase.get(pid, {})
        spans_total += len(var)
        for span, cible in var.items():
            avant = base.get(span, "")
            if cible == avant:
                continue
            typ = span[0]
            changed[typ] += 1
            if (pid,) + span in gold_spans:
                changed_gold[typ] += 1
            else:
                changed_autres[typ] += 1
                if len(exemples) < exemples_max:
                    exemples.append({"id": pid, "type": typ,
                                     "debut": span[1], "fin": span[2],
                                     "avant": avant, "apres": cible,
                                     "phrase": textes.get(pid, "")})
    return {"spans_uniques": spans_total,
            "changes": sum(changed.values()),
            "changes_par_type": dict(changed),
            "dont_gold": sum(changed_gold.values()),
            "dont_gold_par_type": dict(changed_gold),
            "dont_hors_gold": sum(changed_autres.values()),
            "dont_hors_gold_par_type": dict(changed_autres),
            "exemples_hors_gold": exemples}


def _mcnemar_exact(b: int, c: int) -> float:
    """p bilatéral exact de McNemar (binomiale sur les paires discordantes)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = 2.0 * sum(math.comb(n, i) for i in range(k + 1)) / (2.0 ** n)
    return round(min(1.0, p), 6)


def _taux(ok: int, n: int) -> float:
    return round(ok / n, 4) if n else 0.0


def _config_json(config: dict) -> dict:
    """Copie sérialisable d'une configuration (les frozensets deviennent des listes)."""
    sortie = dict(config)
    if "extra_lex" in sortie:
        sortie["extra_lex"] = sorted(sortie["extra_lex"])
    return sortie


def _empreinte_bloc() -> dict:
    """Fige la version du bloc lue : le banc est sensible à son lexique et à sa POS."""
    p = RACINE / "tools" / "bloc_linguistique.py"
    data = p.read_bytes()
    return {"fichier": "tools/bloc_linguistique.py",
            "sha256_16": hashlib.sha256(data).hexdigest()[:16],
            "octets": len(data),
            "mtime": datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(
                timespec="seconds")}


# --------------------------------------------------------------------------- variantes
def _configurations() -> list[dict]:
    """Les variantes mesurées, dans l'ordre du rapport.

    `principal` distingue les retouches recommandées sur l'empreinte courante des
    témoins et des comparaisons. R2 est mesurée sous trois formes : littérale (celle de
    A3), large (rang 0 gardé, qui valait +4 sur le baseline A3 137) et étroite (plus
    proche strict, la forme marginale recommandée).
    """
    return [
        {"nom": "temoin_noop", "famille": "controle", "principal": False,
         "config": {}, "definition": "témoin de fidélité : aucune retouche"},
        {"nom": "R1_repli_vide_GP", "famille": "R1", "principal": True,
         "config": {"t1": "rang0", "t1_scope": "GP"},
         "definition": "cible vide sur un GP → rang 0 du vivier (gauche d'abord)"},
        {"nom": "R1_repli_vide_tous_non_GV", "famille": "R1", "principal": False,
         "config": {"t1": "rang0", "t1_scope": "tous"},
         "definition": "même repli sur tous les types non-GV (surface large)"},
        {"nom": "R1_dernier_temoin", "famille": "R1", "principal": False,
         "config": {"t1": "dernier", "t1_scope": "GP"},
         "definition": "témoin : dernier candidat au lieu du rang 0"},
        {"nom": "R1_verbe_lexique_temoin", "famille": "R1", "principal": False,
         "config": {"t1": "verbe", "t1_scope": "GP"},
         "definition": "témoin : premier verbe reconnu du lexique au lieu du rang 0"},
        {"nom": "R2_litterale", "famille": "R2", "principal": False,
         "config": {"t2": "litteral", "t2_scope": "GP"},
         "definition": "littérale : cible non verbale → verbe du lexique ≤ distance"},
        {"nom": "R2_litterale_POS", "famille": "R2", "principal": False,
         "config": {"t2": "litteral_pos", "t2_scope": "GP"},
         "definition": "témoin : même règle avec le POS VERB au lieu du lexique"},
        {"nom": "R2_litterale_lexique_etendu", "famille": "R2", "principal": False,
         "config": {"t2": "litteral", "t2_scope": "GP", "extra_lex": LEXIQUE_ETENDU},
         "definition": "littérale + rêve/saute ajoutés au lexique (optimiste)"},
        {"nom": "R2_large", "famille": "R2", "principal": False,
         "config": {"t2": "rang0", "t2_scope": "GP"},
         "definition": "large : GP → rang 0, sauf verbe gouverneur reconnu hors segment "
                        "(forme qui valait +4 sur le baseline A3)"},
        {"nom": "R2_etroite", "famille": "R2", "principal": True,
         "config": {"t2": "etroite", "t2_scope": "GP"},
         "definition": "étroite : GP dont la cible n'est pas un verbe reconnu et qu'un "
                        "candidat hors segment est strictement plus proche → ce candidat"},
        {"nom": "R3_completive_etroite", "famille": "R3", "principal": True,
         "config": {"t3": "etroite"},
         "definition": "SUB : cible non candidate, rien à gauche, candidat intérieur → "
                        "dernier intérieur"},
        {"nom": "R3_completive_large", "famille": "R3", "principal": False,
         "config": {"t3": "large"},
         "definition": "témoin : tout SUB → dernier candidat intérieur"},
        {"nom": "combinaison", "famille": "combinaison", "principal": True,
         "config": {"t1": "rang0", "t1_scope": "GP", "t2": "etroite",
                    "t2_scope": "GP", "t3": "etroite"},
         "definition": "R1 (GP) + R2 étroite (GP) + R3 (étroite)"},
        {"nom": "combinaison_R2_large", "famille": "combinaison", "principal": False,
         "config": {"t1": "rang0", "t1_scope": "GP", "t2": "rang0",
                    "t2_scope": "GP", "t3": "etroite"},
         "definition": "comparaison : R1 + R2 large (rang 0 gardé) + R3"},
        {"nom": "combinaison_R2_litterale", "famille": "combinaison", "principal": False,
         "config": {"t1": "rang0", "t1_scope": "GP", "t2": "litteral",
                    "t2_scope": "GP", "t3": "etroite"},
         "definition": "témoin : R1 + R2 littérale + R3 (interaction)"},
        {"nom": "rang0_partout_A3", "famille": "controle", "principal": False,
         "config": {"t1": "rang0", "t1_scope": "tous", "t2": "rang0_brut",
                    "t2_scope": "tous"},
         "definition": "contrôle A3 §7.1 : rang 0 pour tous les segments, sans garde"},
    ]

# --------------------------------------------------------------------------- lecture
def _bilan(variante: dict) -> dict:
    d = variante["detail"]
    return {"exact_145": d["exact_145"], "top1_145": d["top1_145"],
            "exact_239": d["exact_239"], "top1_239": d["top1_239"],
            "surface": {k: variante["surface"][k] for k in
                        ("changes", "dont_gold", "dont_hors_gold",
                         "exemples_hors_gold")}}


def _limites(variantes: dict, base_att: dict) -> list[str]:
    r2e = variantes["R2_etroite"]["surface"]
    r2l = variantes["R2_large"]["surface"]
    combo = variantes["combinaison"]["detail"]["exact_145"]
    return [
        f"145 segments seulement (dont 26 REL) : le net {combo['net']:+d} du combiné "
        f"est une borne haute, pas une estimation de généralisation.",
        "Les cas réparés (R1, R2, R3) ont servi à définir les règles (HARKing) ; aucun "
        "gold tenu à l'écart n'est disponible ici.",
        "La simulation post-traite les cibles ; une intégration réelle doit placer les "
        "mêmes conditions dans `analyser` et rejouer les portes.",
        "Le top1 de `evaluer_gold` accepte les sous-chaînes et les cibles alternatives : "
        "s108/s122 sont déjà top1 vrais avant (papier est dans cibles) ; un repli "
        "« dernier candidat » gagne même +1 top1 sans gagner d'exact (s041, avocat).",
        "94 cibles n'ont pas de span prédit : aucune retouche de cible ne peut les "
        "atteindre ; le plafond global reste 145/239.",
        "Le lexique verbal est incomplet (rêve, saute, marche) ; la variante littérale "
        "de R2 ne mord qu'en ajoutant les deux cibles du gold.",
        f"R2 étroite change {r2e['changes']} étiquettes ({r2e['dont_gold']} gold / "
        f"{r2e['dont_hors_gold']} hors gold) ; R2 large en change {r2l['changes']} "
        f"({r2l['dont_gold']} / {r2l['dont_hors_gold']}).",
        "Le gold mêle deux conventions (verbe gouverneur / nom antécédent) ; la nature "
        "est lue sur le POS du gold, avec _est_verbe en repli.",
        "Le code live a bougé pendant la session (empreintes 6e843018 → bb020516 → "
        "empreinte courante) : les chiffres sont une photo de l'empreinte mesurée.",
    ]


def _recommandation(variantes: dict, base_att: dict, base_mesures: dict) -> dict:
    def b(nom):
        return _bilan(variantes[nom])

    r1, r2e, r2l = b("R1_repli_vide_GP"), b("R2_etroite"), b("R2_large")
    r3 = b("R3_completive_etroite")
    combo = b("combinaison")
    lit = b("R2_litterale")
    lit_ext = b("R2_litterale_lexique_etendu")
    lit_pos = b("R2_litterale_POS")
    r3l = b("R3_completive_large")
    gains = variantes["combinaison"]["gains"]
    gagnes = {m["id"] for m in gains}
    reste = [m["id"] for m in base_mesures.values()
             if not m["exact"] and m["id"] not in gagnes]
    reste += [m["id"] for m in variantes["combinaison"]["regressions"]]
    reste_exact = (f"aucune erreur exacte restante sur les 145 ; top1 "
                   f"{combo['top1_145']['justes']}/{combo['top1_145']['n']}")
    if reste:
        reste_exact = "cas non réparés ou régressions : " + ", ".join(sorted(set(reste)))
    return {
        "R1": {"integrer": True, "forme": "GP seulement, rang 0 du vivier",
               "bilan": r1,
               "pourquoi": (f"+{r1['exact_145']['net']} exact, "
                            f"{r1['exact_145']['regressions']} régression, "
                            f"{r1['surface']['changes']} étiquettes changées "
                            f"({r1['surface']['dont_hors_gold']} hors gold) ; le repli "
                            f"ne peut pas dégrader un exact déjà faux.")},
        "R2": {"integrer": True, "forme": "étroite (plus proche strict, GP seulement)",
               "bilan": r2e,
               "pourquoi": (f"+{r2e['exact_145']['net']} exact, "
                            f"{r2e['exact_145']['regressions']} régression, "
                            f"{r2e['surface']['changes']} étiquettes changées "
                            f"({r2e['surface']['dont_hors_gold']} hors gold) ; "
                            f"la forme large de A3 donne +{r2l['exact_145']['gain']} "
                            f"mais change {r2l['surface']['changes']} étiquettes "
                            f"({r2l['surface']['dont_hors_gold']} hors gold)."),
               "ne_pas_integrer": (f"la préférence verbe littérale : net "
                                    f"{lit['exact_145']['net']:+d} avec le lexique de "
                                    f"base, net {lit_ext['exact_145']['net']:+d} en "
                                    f"ajoutant rêve/saute, "
                                    f"{lit_pos['exact_145']['regressions']} "
                                    f"régressions avec le POS ; elle défait g002, "
                                    f"g012 et r018, déjà réparés par le live, et ne "
                                    f"répare pas g012/r018 par construction (gold "
                                    f"adjectival).")},
        "R3": {"integrer": True, "forme": "étroite : cible non candidate, rien à "
                                            "gauche, candidat intérieur",
               "bilan": r3,
               "pourquoi": (f"+{r3['exact_145']['net']} exact, "
                            f"{r3['exact_145']['regressions']} régression, "
                            f"{r3['surface']['changes']} étiquette changée ; la "
                            f"variante large coûte "
                            f"{r3l['exact_145']['regressions']} régressions.")},
        "combinaison": {"bilan": combo,
                        "exact_145": f"{combo['exact_145']['justes']}/"
                                       f"{combo['exact_145']['n']} "
                                       f"({combo['exact_145']['taux']:.4f})",
                        "top1_145": f"{combo['top1_145']['justes']}/"
                                      f"{combo['top1_145']['n']} "
                                      f"({combo['top1_145']['taux']:.4f})",
                        "exact_239": f"{combo['exact_239']['justes']}/"
                                       f"{combo['exact_239']['n']} "
                                       f"({combo['exact_239']['taux']:.4f})",
                        "top1_239": f"{combo['top1_239']['justes']}/"
                                      f"{combo['top1_239']['n']} "
                                      f"({combo['top1_239']['taux']:.4f})",
                        "reste": reste_exact,
                        "gains": [m["id"] for m in gains]},
        "avant_integration": "gold tenu à l'écart, revue des changements hors gold, "
                              "portes, puis commit unique.",
    }


# --------------------------------------------------------------------------- exécution
def executer(phrases: list[dict]) -> dict:
    empreinte_debut = _empreinte_bloc()
    base_bloc = bl.Heuristique()
    base_eval = evaluer_bloc("heuristique", base_bloc, phrases)
    base_att = _resume_attachement(base_eval["attachement"])
    base_mesures, base_par_phrase, _ = _collecter(base_bloc, phrases)
    gold_spans = _gold_spans(phrases)

    if len(base_mesures) != base_att["labels"]:
        raise SystemExit("population mesurée incohérente avec evaluer_bloc")
    if sum(m["exact"] for m in base_mesures.values()) != base_att["exact"]:
        raise SystemExit("exact par segment incohérent avec evaluer_bloc")
    if sum(m["top1"] for m in base_mesures.values()) != base_att["top1"]:
        raise SystemExit("top1 par segment incohérent avec evaluer_bloc")

    variantes = {}
    for cfg in _configurations():
        bloc = HeuristiqueReplis(**cfg["config"])
        evaluation = evaluer_bloc(cfg["nom"], bloc, phrases)
        att = _resume_attachement(evaluation["attachement"])
        mesures, par_phrase, _ = _collecter(bloc, phrases)
        if len(mesures) != att["labels"]:
            raise SystemExit(f"{cfg['nom']}: population incohérente")
        if sum(m["exact"] for m in mesures.values()) != att["exact"]:
            raise SystemExit(f"{cfg['nom']}: exact incohérent avec evaluer_bloc")
        if sum(m["top1"] for m in mesures.values()) != att["top1"]:
            raise SystemExit(f"{cfg['nom']}: top1 incohérent avec evaluer_bloc")
        gains, regs, gains_t1, regs_t1 = _diff(base_mesures, mesures)
        variantes[cfg["nom"]] = {
            "famille": cfg["famille"], "principal": cfg["principal"],
            "definition": cfg["definition"], "config": _config_json(cfg["config"]),
            "attachement": att,
            "exact_145": att["exact"], "top1_145": att["top1"],
            "exact_239": att["exact"], "top1_239": att["top1"],
            "detail": {
                "exact_145": {"justes": att["exact"], "n": att["labels"],
                              "taux": att["exact_taux_span"],
                              "gain": len(gains), "regressions": len(regs),
                              "net": len(gains) - len(regs)},
                "top1_145": {"justes": att["top1"], "n": att["labels"],
                             "taux": att["top1_taux_span"],
                             "gain": len(gains_t1), "regressions": len(regs_t1),
                             "net": len(gains_t1) - len(regs_t1)},
                "exact_239": {"justes": att["exact"], "n": att["cibles"],
                              "taux": att["exact_taux"]},
                "top1_239": {"justes": att["top1"], "n": att["cibles"],
                             "taux": att["top1_taux"]},
            },
            "gains": gains, "regressions": regs,
            "gains_top1": gains_t1, "regressions_top1": regs_t1,
            "mcnemar_exact": _mcnemar_exact(len(gains), len(regs)),
            "surface": _surface(base_par_phrase, par_phrase, gold_spans, phrases),
        }
        del evaluation

    # Q1 — état des lieux de la cible au span exact et sur les 239.
    absents = Counter()
    absents_ids = {t: [] for t in TYPES}
    vides = []
    remplis = Counter()
    croisement = Counter()
    nom_gold_verbe = []
    verbe_gold_non_verbe = []
    for phrase in phrases:
        labels = _labels(base_bloc.analyser(phrase["texte"], phrase["langue"]))
        for segment in phrase["segments"]:
            cibles = _cibles(segment)
            if not cibles:
                continue
            etiquette = labels.get((segment["type"], segment["debut"], segment["fin"]))
            if etiquette is None:
                absents[segment["type"]] += 1
                absents_ids[segment["type"]].append(phrase["id"])
                continue
            cible = _cible_de(etiquette)
            if not cible:
                vides.append({"id": phrase["id"], "type": segment["type"],
                              "segment": segment.get("texte", ""),
                              "gold": cibles[0], "gold_all": cibles})
                croisement["vide", _nature_gold(phrase, cibles[0])] += 1
                continue
            remplis[segment["type"]] += 1
            nature_pred = _nature_gold(phrase, cible)
            nature_gold = _nature_gold(phrase, cibles[0])
            croisement[nature_pred, nature_gold] += 1
            fiche = {"id": phrase["id"], "type": segment["type"],
                     "segment": segment.get("texte", ""),
                     "avant": cible, "gold": cibles[0], "gold_all": cibles,
                     "nature_avant": nature_pred, "nature_gold": nature_gold,
                     "token_gold": bool(_pos_gold(phrase, cible))}
            if nature_pred == "nom" and nature_gold == "verbe":
                nom_gold_verbe.append(fiche)
            if nature_pred == "verbe" and nature_gold != "verbe":
                verbe_gold_non_verbe.append(fiche)

    corpus = {
        "phrases": len(phrases),
        "tokens": sum(len(p["mots"]) for p in phrases),
        "phrases_hand": sum(1 for p in phrases if p["source"] == "hand"),
        "phrases_reel": sum(1 for p in phrases if p["source"] == "reel"),
        "phrases_synthetique": sum(1 for p in phrases if p["source"] == "synthetique"),
        "cibles_gold": sum(1 for p in phrases for s in p["segments"] if _cibles(s)),
        "spans_predits": base_att["labels"],
        "spans_non_predits": sum(absents.values()),
        "predits_sans_cible": len(vides),
        "remplis": sum(remplis.values()),
    }
    etat = {
        "cibles_gold": corpus["cibles_gold"],
        "spans_predits": base_att["labels"],
        "spans_non_predits": {"total": sum(absents.values()),
                              "par_type": {t: absents[t] for t in TYPES},
                              "ids_par_type": {t: absents_ids[t] for t in TYPES}},
        "predits_sans_cible": {"total": len(vides), "liste": vides},
        "cibles_sans_cible_utilisable": sum(absents.values()) + len(vides),
        "remplis": sum(remplis.values()),
        "remplis_par_type": {t: remplis[t] for t in TYPES},
        "par_type_239": {
            t: {"cibles": sum(1 for p in phrases for s in p["segments"]
                              if s["type"] == t and _cibles(s)),
                "spans_predits": sum(1 for m in base_mesures.values() if m["type"] == t),
                "vides": sum(1 for v in vides if v["type"] == t),
                "absents": absents[t]}
            for t in TYPES},
        "croisement_nature": {
            f"{pred}→{gold}": n for (pred, gold), n in sorted(croisement.items())},
        "cible_nom_gold_verbe": nom_gold_verbe,
        "cible_verbe_gold_non_verbe": verbe_gold_non_verbe,
        "top1_sans_exact": [
            {"id": m["id"], "type": m["type"], "segment": m["segment"],
             "cible": m["cible"], "gold_all": m["gold_all"]}
            for m in base_mesures.values() if m["top1"] and not m["exact"]],
    }

    # Audit des 145 : une ligne par segment, avec les variantes principales.
    cles = ("R1_repli_vide_GP", "R2_etroite", "R3_completive_etroite",
            "combinaison")
    audit = []
    for cle, m in base_mesures.items():
        ligne = {
            "id": m["id"], "source": m["source"], "type": m["type"],
            "debut": m["debut"], "fin": m["fin"], "segment": m["segment"],
            "gold": m["gold"], "gold_all": m["gold_all"],
            "gold_nature": m["gold_nature"],
            "base": {"cible": m["cible"], "nature": m["nature"],
                     "exact": m["exact"], "top1": m["top1"]},
            "variantes": {},
        }
        for nom in cles:
            # relire la cible de la variante depuis ses mesures n'est pas possible
            # ici sans relancer ; on stocke les diffs dans `gains`/`regressions`.
            ligne["variantes"][nom] = None
        audit.append(ligne)
    # remplir les cibles des variantes principales à partir d'une passe dédiée
    for nom in cles:
        cfg = next(c for c in _configurations() if c["nom"] == nom)
        bloc = HeuristiqueReplis(**cfg["config"])
        mesures, _, _ = _collecter(bloc, phrases)
        for m in audit:
            cle = (m["id"], m["type"], m["debut"], m["fin"])
            v = mesures.get(cle)
            if v:
                m["variantes"][nom] = {"cible": v["cible"], "exact": v["exact"],
                                       "top1": v["top1"]}

    variantes_principales = {n: v for n, v in variantes.items() if v["principal"]}
    combo = variantes["combinaison"]
    empreinte_fin = _empreinte_bloc()
    return {
        "titre": "Trois retouches déterministes de l'attachement (replis de cible)",
        "date": "2026-11-05",
        "ligne_roadmap": "B13",
        "empreinte_bloc_linguistique": empreinte_debut,
        "empreinte_fin_de_run": empreinte_fin,
        "bloc_stable_pendant_le_run": (empreinte_debut["sha256_16"]
                                       == empreinte_fin["sha256_16"]),
        "note": ("Prototype autonome : `bloc_linguistique.py` n'est pas modifié ; les "
                 "retouches sont simulées par post-traitement des cibles. Le top-k et "
                 "les spans sont inchangés par construction. La règle live bouge : "
                 "l'empreinte lue est figée ci-dessus, et `bloc_stable_pendant_le_run` "
                 "dit si le fichier a changé pendant la mesure."),
        "protocole": {
            "population": "612 phrases ; 239 segments gold porteurs d'une cible ; "
                          "145 dont le span (type, debut, fin) est prédit",
            "mesure": "égalité exacte avec cibles[0] et top1 de evaluer_gold "
                      "(sous-chaîne d'une des cibles), sur 145 (span) et 239 (global)",
            "vivier": "tokens pleins (POS ouverte ou _est_verbe), auxiliaires exclus ; "
                      "gauche → droite → dedans, puis distance",
            "simulation": "sous-classe de Heuristique + post-traitement de "
                          "meta.attachement.cible ; aucun autre champ modifié",
            "controle_fidelite": f"le témoin no-op redonne exactement "
                                  f"{base_att['exact']}/{base_att['labels']} exact et "
                                  f"{base_att['top1']}/{base_att['labels']} top1 ; "
                                  f"pour chaque variante, les agrégats par segment sont "
                                  f"vérifiés contre evaluer_bloc",
            "regression": "segment exact avant → faux après ; le gain net = gains - "
                          "régressions",
            "mcnemar": "exact bilatéral sur les paires discordantes (descriptif : les "
                       "cas ont servi à définir les règles)",
        },
        "corpus": corpus,
        "base": base_att,
        "etat_des_lieux": etat,
        "derive_du_bloc": {
            "empreinte_mesuree": empreinte_debut,
            "stable_pendant_le_run": (empreinte_debut["sha256_16"]
                                       == empreinte_fin["sha256_16"]),
            "historique": [
                {"empreinte": "6e843018", "octets": 101568,
                 "mtime": "2026-11-05T13:51:26", "baseline_exact": 137,
                 "note": "état de la fiche A3 / début de session, non rejoué ici"},
                {"empreinte": "bb020516", "octets": 103191,
                 "mtime": "2026-11-05T15:03:12", "baseline_exact": 137,
                 "retouches": {"R1": "+2", "R2_large": "+4", "R3": "+1",
                               "combinaison": "+7 (144/145 exact, 145/145 top1)"},
                 "note": "snapshot intermédiaire mesuré par ce prototype ; le live a "
                         "ensuite absorbé g002, g012/r018 et r230"},
                {"empreinte": "64b7c520", "octets": 105381,
                 "mtime": "2026-11-05T15:04:59", "baseline_exact": 141,
                 "retouches": {"R1": "+1", "R2_etroite": "+2", "R3": "+1",
                               "combinaison": "+4 (145/145 exact, 145/145 top1)"},
                 "note": "run live avant le refactor de cache (sortie identique)"},
            ],
            "lecture": ("Le code live a absorbé une partie des retouches : "
                        "`_repli_cible_gp` (g002), `_cible_hors_span` (g012/r018) et "
                        "`_sans_enclitique` (r230). Les gains marginaux ci-dessus sont "
                        "donc plus petits que les +2/+4/+1 du baseline A3 ; ils portent "
                        "sur les 4 erreurs restantes."),
        },
        "snapshot_a3_137": {
            "empreinte": "bb020516", "octets": 103191,
            "mtime": "2026-11-05T15:03:12",
            "note": ("mesure intermédiaire de ce prototype, avant l'intégration live ; "
                     "baseline 137 = les 8 erreurs de la fiche A3. R2 y est la forme "
                     "large (rang 0 gardé), R3 la forme étroite."),
            "baseline": {"exact_145": 137, "top1_145": 140, "topk_exact": 141,
                         "cibles": 239},
            "erreurs_baseline": ["g002", "g012", "r018", "r230", "r309", "s041",
                                  "s108", "s122"],
            "R1": {"gain": 2, "regressions": 0, "net": 2,
                   "gains": ["g002", "s041"],
                   "surface": {"changes": 3, "dont_gold": 2, "dont_hors_gold": 1}},
            "R2_large": {"gain": 4, "regressions": 0, "net": 4,
                         "gains": ["g012", "r018", "s108", "s122"],
                         "surface": {"changes": 14, "dont_gold": 4,
                                     "dont_hors_gold": 10}},
            "R3": {"gain": 1, "regressions": 0, "net": 1, "gains": ["r309"],
                   "surface": {"changes": 1, "dont_gold": 1, "dont_hors_gold": 0}},
            "combinaison": {"gain": 7, "regressions": 0, "net": 7,
                            "exact_145": "144/145 (0,9931)",
                            "top1_145": "145/145 (1,0000)",
                            "gains": ["g002", "g012", "r018", "r309", "s041",
                                      "s108", "s122"]},
        },
        "retouches": {
            "R1": {n: v for n, v in variantes.items()
                   if v["famille"] == "R1"},
            "R2": {n: v for n, v in variantes.items()
                   if v["famille"] == "R2"},
            "R3": {n: v for n, v in variantes.items()
                   if v["famille"] == "R3"},
            "combinaison": {n: v for n, v in variantes.items()
                            if v["famille"] == "combinaison"},
            "controles": {n: v for n, v in variantes.items()
                          if v["famille"] == "controle"},
        },
        "variantes": variantes,
        "principales": variantes_principales,
        "combinaison": combo,
        "segments_145": audit,
        "limites": _limites(variantes, base_att),
        "recommandation": _recommandation(variantes, base_att, base_mesures),
    }


# --------------------------------------------------------------------------- CLI    }


# --------------------------------------------------------------------------- CLI
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", default=str(SORTIE_DEFAUT),
                    help="chemin du JSON de résultat (défaut : "
                         "reports/pensee-replis-cible.json)")
    args = ap.parse_args()

    phrases = charger()
    resultat = executer(phrases)
    sortie = pathlib.Path(args.json)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")

    b = resultat["base"]
    print("== base ==")
    print("bloc:", resultat["empreinte_bloc_linguistique"])
    print(f"exact {b['exact']}/{b['labels']} ({b['exact_taux_span']:.4f}) | "
          f"top1 {b['top1']}/{b['labels']} ({b['top1_taux_span']:.4f}) | "
          f"topk strict {b['topk_exact']}/{b['cibles']} | "
          f"exact global {b['exact']}/{b['cibles']} ({b['exact_taux']:.4f})")
    print("== retouches ==")
    for nom, v in resultat["variantes"].items():
        d = v["detail"]
        print(f"{nom:32s} exact {d['exact_145']['justes']:3d}/{d['exact_145']['n']} "
              f"({d['exact_145']['taux']:.4f}) Δ{d['exact_145']['net']:+d} "
              f"top1 {d['top1_145']['justes']:3d}/{d['top1_145']['n']} "
              f"({d['top1_145']['taux']:.4f}) Δ{d['top1_145']['net']:+d} "
              f"reg {d['exact_145']['regressions']:2d} | "
              f"surface {v['surface']['changes']:3d} "
              f"({v['surface']['dont_gold']} gold / {v['surface']['dont_hors_gold']} hors)")
    print("== état des lieux ==")
    e = resultat["etat_des_lieux"]
    print(f"239 cibles : {e['spans_predits']} spans prédits, "
          f"{e['spans_non_predits']['total']} absents, "
          f"{e['predits_sans_cible']['total']} vides au span prédit, "
          f"{e['remplis']} remplis")
    print("croisement nature:", e["croisement_nature"])
    print("nom→verbe:", [(x["id"], x["avant"], x["gold"]) for x in e["cible_nom_gold_verbe"]])
    print("verbe→non-verbe:", [(x["id"], x["avant"], x["gold"])
                              for x in e["cible_verbe_gold_non_verbe"]])
    c = resultat["combinaison"]["detail"]
    print("== combinaison ==")
    print(f"exact {c['exact_145']['justes']}/{c['exact_145']['n']} "
          f"({c['exact_145']['taux']:.4f}) | top1 {c['top1_145']['justes']}/"
          f"{c['top1_145']['n']} ({c['top1_145']['taux']:.4f}) | "
          f"global exact {c['exact_239']['justes']}/{c['exact_239']['n']} "
          f"({c['exact_239']['taux']:.4f}) | top1 {c['top1_239']['justes']}/"
          f"{c['top1_239']['n']} ({c['top1_239']['taux']:.4f})")
    print("JSON ->", sortie)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

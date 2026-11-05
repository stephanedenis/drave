"""classement_cible.py — prototype **autonome** d'un classement appris des candidats d'attachement.

Le problème. `bloc_linguistique.Heuristique` choisit la cible d'un segment par **type +
proximité** (REL/SUB → antécédent nominal à gauche, GP → verbe du GV le plus proche). Sur les
segments gold dont le span est prédit, cette règle donnait **123/145** en égalité exacte au
début de la session (référence de la consigne) ; un autre agent l'a modifiée pendant la
session (129 puis 137/145) — le run fige l'empreinte du fichier lu, et la fiche rapporte les
deux comparaisons. Ce fichier teste une autre sélection : un **score linéaire appris** sur des
features lisibles, candidat par candidat, sans toucher à `bloc_linguistique.py` (l'intégration
éventuelle est une autre décision).

**Statut (2026-11-05)** : prototype **non intégré**. Face à la règle vivante à 137/145, le
modèle fait 142/145 — gain +5, McNemar 7/2, p = 0,18, IC95 [−0,7 ; +7,6] : non significatif,
avec 2 régressions. Décision consignée dans `reports/rapport-pensee-attachement-v2.md` § 3.

Protocole (fixé ici). Limite assumée : le vivier, la liste des features et l'ordre de la liste
ont été dessinés après une passe exploratoire sur le corpus ; le découpage ne valide donc que
les **poids appris**, pas le dessin des features (voir la fiche).

1. On garde les segments gold qui portent une cible (`cibles`) **et** dont le span
   `(type, debut, fin)` est prédit par l'heuristique — exactement les 145 segments de la
   mesure courante (123/145). Le gold et la mesure sont ceux de `evaluer_gold.py`.
2. Pour chaque segment, le **vivier** est l'ensemble des tokens pleins de la phrase : POS
   ouverte (`NOUN`, `PROPN`, `VERB`, `ADJ`) ou `_est_verbe(token)`, auxiliaires exclus. Le
   vivier est construit **sans le gold** ; il contient la cible dans 144/145 cas (le cas
   manquant est `appelle` vs le token `appelle-moi`, découpage différent du gold).
3. Chaque candidat reçoit les features demandées : distance en tokens au segment, côté
   (gauche / droite / dedans), type du segment (GP/REL/SUB), préposition éventuelle, longueur
   du candidat, nature verbe/nom (`_est_verbe`) et POS heuristique, rang dans la liste
   (liste ordonnée gauche → droite → dedans, puis distance). S'y ajoutent quelques
   interactions lisibles (type × nature, génitif × nature), sans quoi un modèle linéaire ne
   peut pas exprimer « un GP en *de* s'accroche au nom, un GP en *dans* au verbe ».
4. Le score est une **régression logistique binaire** (« ce candidat est-il la cible ? »)
   implémentée à la main : descente de gradient pleine bataille, L2, pondération de classes.
   La cible prédite est l'**argmax** du score sur le vivier.
5. Découpage : phrases d'**id pair** → entraînement, ids **impairs** → test, puis l'inverse.
   La mesure est l'égalité exacte avec `cibles[0]`, comme `evaluer_gold.py`. On rapporte les
   deux sens, leur moyenne et le **regroupé hors-pli** (chaque segment est prédit par le
   modèle qui ne l'a pas vu).
6. Contrôles négatifs sur les mêmes segments : **règle actuelle**, **hasard uniforme dans le
   vivier**, **hasard parmi les cibles distinctes**. Test de McNemar exact, intervalle de
   confiance bootstrap de la différence, et 10 découpages aléatoires pour la stabilité.

Aucune dépendance nouvelle (bibliothèque standard seulement). Le script n'écrit que le JSON
de résultat (`reports/pensee-classement-appris.json` par défaut) ; il ne modifie rien d'autre.
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
import random
import re
from collections import Counter

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
sys.path.insert(0, str(RACINE / "tools" / "tests" / "linguistique"))

import bloc_linguistique as bl  # noqa: E402
from evaluer_gold import charger  # noqa: E402

SORTIE_DEFAUT = RACINE / "reports" / "pensee-classement-appris.json"
TYPES = ("GP", "REL", "SUB")
POS_OUVERTES = {"NOUN", "PROPN", "VERB", "ADJ"}

# --------------------------------------------------------------------------- features
#
# Codage par référence : type SUB, côté droit, préposition absente, nature nominale (lexique).
# Les interactions couvrent les six combinaisons type × nature sans variable redondante.
FEATURES = (
    "biais",
    "distance",          # écart en tokens au segment, normalisé (0 = dedans)
    "rang",              # rang dans la liste gauche → droite → dedans
    "longueur",          # longueur du candidat en caractères, normalisée
    "cote_gauche",       # référence : droite
    "cote_dedans",
    "type_GP",           # référence : SUB
    "type_REL",
    "prep_gen",          # de/du/des/of/from  (référence : aucune préposition)
    "prep_dat",          # à/au/aux/to
    "prep_loc",          # dans/sur/sous/.../in/on/at/over
    "prep_but",          # pour/afin/for
    "prep_moy",          # avec/sans/with/without
    "prep_autre",
    "nat_verbe",         # `_est_verbe` (référence : nom)
    "pos_verbe",         # POS heuristique VERB
    "pos_nom",           # POS heuristique NOUN/PROPN
    "GP_x_verbe",
    "REL_x_verbe",
    "SUB_x_verbe",
    "GP_x_posV",
    "REL_x_posV",
    "SUB_x_posV",
    "GEN_x_verbe",       # un génitif préfère-t-il un nom (poids négatif) ?
    "GEN_x_posV",
)

PREP_GEN = {"de", "du", "des", "d'", "d’", "of", "from"}
PREP_DAT = {"à", "a", "au", "aux", "to"}
PREP_LOC = {"dans", "sur", "sous", "chez", "vers", "entre", "devant", "derrière", "in", "on",
            "at", "over", "under", "between", "into", "near"}
PREP_BUT = {"pour", "afin", "for"}
PREP_MOY = {"avec", "sans", "with", "without"}


def _categorie_prep(mot: str) -> str:
    p = bl._normaliser(mot)
    if p in PREP_GEN:
        return "gen"
    if p in PREP_DAT:
        return "dat"
    if p in PREP_LOC:
        return "loc"
    if p in PREP_BUT:
        return "but"
    if p in PREP_MOY:
        return "moy"
    return "autre"


def _parite(identifiant: str) -> int:
    """La moitié d'une phrase : la parité du nombre final de son id (`g001`, `r202`…)."""
    m = re.search(r"(\d+)$", identifiant or "")
    return int(m.group(1)) % 2 if m else 0


def _empreinte_bloc() -> dict:
    """Fige la version du bloc lue : le banc est sensible à son lexique et à sa POS."""
    p = RACINE / "tools" / "bloc_linguistique.py"
    data = p.read_bytes()
    return {"fichier": "tools/bloc_linguistique.py",
            "sha256_16": hashlib.sha256(data).hexdigest()[:16],
            "octets": len(data),
            "mtime": datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds")}


def _sigmoide(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


# --------------------------------------------------------------------------- corpus
def _etiquettes_syntagmes(annotation) -> dict:
    return {(e.type, e.debut, e.fin): e
            for e in annotation.etiquettes if e.niveau == "syntagme"}


def _pos(annotation) -> dict:
    return {(e.debut, e.fin): e.type for e in annotation.etiquettes if e.niveau == "pos"}


def _cibles(segment: dict) -> list[str]:
    return segment.get("cibles") or ([segment["cible"]] if segment.get("cible") else [])


def _candidats(phrase: dict, annotation) -> list[dict]:
    """Le vivier : tokens pleins de la phrase, sans utiliser le gold.

    Un token est candidat si sa POS heuristique est ouverte ou si `_est_verbe` le reconnaît.
    Les auxiliaires sont exclus : le gold n'en donne jamais comme cible (vérifié : 0/282).
    """
    pos = _pos(annotation)
    sortie = []
    for i, (d, f, t, typ) in enumerate(bl.Heuristique._mots(phrase["texte"])):
        if typ != "mot" or bl._normaliser(t) in bl.AUXILIAIRES:
            continue
        p = pos.get((d, f), "")
        verbe = bl._est_verbe(t)
        if p in POS_OUVERTES or verbe:
            sortie.append({"i": i, "debut": d, "fin": f, "texte": t, "pos": p,
                           "verbe_lex": verbe})
    return sortie


def construire(phrases: list[dict], bloc) -> tuple[list[dict], dict]:
    """Les segments mesurables : gold avec cible **et** span prédit, plus leur vivier."""
    stats = Counter()
    segments: list[dict] = []
    for phrase in phrases:
        annotation = bloc.analyser(phrase["texte"], phrase["langue"])
        labels = _etiquettes_syntagmes(annotation)
        vivier = _candidats(phrase, annotation)
        mots = bl.Heuristique._mots(phrase["texte"])
        for s in phrase["segments"]:
            cibles = _cibles(s)
            if not cibles:
                continue
            stats["segments_gold_avec_cible"] += 1
            etiquette = labels.get((s["type"], s["debut"], s["fin"]))
            if etiquette is None:
                stats["span_non_predit"] += 1
                continue
            if s["type"] not in TYPES:
                stats["type_hors_perimetre"] += 1
                continue
            indices = [i for i, (d, f, _t, _ty) in enumerate(mots)
                       if d >= s["debut"] and f <= s["fin"]]
            if not indices:
                stats["segment_sans_token"] += 1
                continue
            if not vivier:
                stats["vivier_vide"] += 1
                continue
            i_min, i_max = min(indices), max(indices)
            prep = _categorie_prep(mots[i_min][2]) if s["type"] == "GP" else ""
            candidats = []
            for c in vivier:
                j = c["i"]
                if j < i_min:
                    distance, cote = i_min - j, "gauche"
                elif j > i_max:
                    distance, cote = j - i_max, "droite"
                else:
                    distance, cote = 0, "dedans"
                candidats.append({**c, "distance": distance, "cote": cote})
            # liste gauche → droite → dedans, puis distance : l'ordre d'un prior de proximité
            ordre = {"gauche": 0, "droite": 1, "dedans": 2}
            candidats.sort(key=lambda c: (ordre[c["cote"]], c["distance"], c["i"]))
            for rang, c in enumerate(candidats):
                c["rang"] = rang
                c["x"] = _vecteur(s["type"], prep, c, len(candidats))
                c["positif"] = int(c["texte"] == cibles[0])
            positif = sum(c["positif"] for c in candidats)
            if positif == 0:
                stats["cible_hors_vivier"] += 1
            att = (etiquette.meta or {}).get("attachement") or {}
            segments.append({
                "id": phrase["id"], "source": phrase["source"], "parite": _parite(phrase["id"]),
                "texte": phrase["texte"], "type": s["type"], "segment": s.get("texte", ""),
                "cible": cibles[0], "prep": prep, "pred_actuelle": (att.get("cible") or "").strip(),
                "ok_actuelle": (att.get("cible") or "").strip() == cibles[0],
                "candidats": candidats,
            })
    return segments, dict(stats)


def _vecteur(type_segment: str, prep: str, c: dict, n: int) -> list[float]:
    verbe = 1.0 if c["verbe_lex"] else 0.0
    posv = 1.0 if c["pos"] == "VERB" else 0.0
    posn = 1.0 if c["pos"] in ("NOUN", "PROPN") else 0.0
    gp = 1.0 if type_segment == "GP" else 0.0
    rel = 1.0 if type_segment == "REL" else 0.0
    sub = 1.0 - gp - rel
    gen = 1.0 if prep == "gen" else 0.0
    return [
        1.0,
        min(c["distance"], 6) / 6.0,
        c["rang"] / max(1, n - 1),
        min(len(c["texte"]), 12) / 12.0,
        1.0 if c["cote"] == "gauche" else 0.0,
        1.0 if c["cote"] == "dedans" else 0.0,
        gp,
        rel,
        1.0 if prep == "gen" else 0.0,
        1.0 if prep == "dat" else 0.0,
        1.0 if prep == "loc" else 0.0,
        1.0 if prep == "but" else 0.0,
        1.0 if prep == "moy" else 0.0,
        1.0 if prep == "autre" else 0.0,
        verbe,
        posv,
        posn,
        gp * verbe,
        rel * verbe,
        sub * verbe,
        gp * posv,
        rel * posv,
        sub * posv,
        gen * verbe,
        gen * posv,
    ]


# --------------------------------------------------------------------------- modèle
def entrainer(segments: list[dict], epochs: int = 6000, lr: float = 0.6,
              l2: float = 0.01) -> tuple[list[float], dict]:
    """Régression logistique binaire par descente de gradient pleine bataille, L2.

    Les lignes sont les couples (candidat, est-il la cible ?). Les classes sont pondérées
    (une cible pour ~4 candidats) pour que la positivité pèse. Le biais n'est pas régularisé.
    """
    lignes = []
    for seg in segments:
        for c in seg["candidats"]:
            lignes.append(([(j, v) for j, v in enumerate(c["x"]) if v], c["positif"]))
    n = len(lignes)
    n_pos = sum(y for _, y in lignes)
    n_neg = n - n_pos
    if n_pos == 0 or n_neg == 0:
        raise ValueError("découpage dégénéré : une classe est vide")
    wp = n / (2.0 * n_pos)
    wn = n / (2.0 * n_neg)
    poids = [wp if y else wn for _, y in lignes]
    d = len(FEATURES)
    w = [0.0] * d
    perte = float("inf")
    perte_prec = None
    arret = 0
    iteration = 0
    for iteration in range(1, epochs + 1):
        grad = [0.0] * d
        perte = 0.0
        for (x, y), poids_i in zip(lignes, poids):
            z = sum(w[j] * v for j, v in x)
            p = _sigmoide(z)
            p = min(1.0 - 1e-12, max(1e-12, p))
            perte += poids_i * (-(y * math.log(p) + (1 - y) * math.log(1.0 - p)))
            g = (p - y) * poids_i
            for j, v in x:
                grad[j] += g * v
        for j in range(d):
            grad[j] = grad[j] / n + (0.0 if j == 0 else l2 * w[j])
            w[j] -= lr * grad[j]
        if perte_prec is not None and abs(perte_prec - perte) < 1e-7 * max(1.0, abs(perte_prec)):
            arret += 1
            if arret >= 20:
                break
        else:
            arret = 0
        perte_prec = perte
    return w, {"lignes": n, "positifs": n_pos, "negatifs": n_neg,
               "epochs_effectues": iteration, "perte_finale": round(perte, 6),
               "perte_moyenne": round(perte / n, 6),
               "poids_positif": round(wp, 4), "poids_negatif": round(wn, 4)}


def _score(w: list[float], x: list[float]) -> float:
    return sum(a * b for a, b in zip(w, x))


def _predire(modele: list[float], seg: dict) -> tuple[str, list[dict]]:
    """Argmax du score ; égalité tranchée par le rang (le plus prioritaire d'abord)."""
    meilleur, meilleur_score = None, -float("inf")
    scores = []
    for c in seg["candidats"]:
        s = _score(modele, c["x"])
        scores.append({**{k: c[k] for k in ("texte", "distance", "cote", "rang",
                                            "verbe_lex", "pos", "positif")},
                       "score": round(s, 6)})
        if s > meilleur_score:
            meilleur, meilleur_score = c, s
    return (meilleur["texte"] if meilleur else ""), scores


def _taux(ok: int, n: int) -> float:
    return round(ok / n, 4) if n else 0.0


def evaluer(modele: list[float], segments: list[dict]) -> dict:
    ok = 0
    par_type = Counter()
    n_par_type = Counter()
    for seg in segments:
        pred, _ = _predire(modele, seg)
        juste = pred == seg["cible"]
        ok += int(juste)
        n_par_type[seg["type"]] += 1
        par_type[seg["type"]] += int(juste)
    return {"n": len(segments), "justes": ok, "taux": _taux(ok, len(segments)),
            "par_type": {t: {"n": n_par_type[t], "justes": par_type[t],
                             "taux": _taux(par_type[t], n_par_type[t])}
                         for t in TYPES}}


def evaluer_regle(segments: list[dict]) -> dict:
    ok = sum(1 for s in segments if s["ok_actuelle"])
    par_type = {t: {"n": sum(1 for s in segments if s["type"] == t),
                    "justes": sum(1 for s in segments if s["type"] == t and s["ok_actuelle"])}
                for t in TYPES}
    for t in TYPES:
        par_type[t]["taux"] = _taux(par_type[t]["justes"], par_type[t]["n"])
    return {"n": len(segments), "justes": ok, "taux": _taux(ok, len(segments)),
            "par_type": par_type}


def _argmax_aleatoire(seg: dict, rng: random.Random) -> str:
    return rng.choice(seg["candidats"])["texte"] if seg["candidats"] else ""


def evaluer_hasard(segments: list[dict], rng: random.Random) -> dict:
    """Hasard uniforme dans le vivier ; on joint le taux attendu (espérance, pas un tirage)."""
    ok = sum(1 for s in segments if _argmax_aleatoire(s, rng) == s["cible"])
    attendu = sum((sum(c["positif"] for c in s["candidats"]) / len(s["candidats"]))
                  for s in segments if s["candidats"]) / max(1, len(segments))
    return {"n": len(segments), "justes": ok, "taux": _taux(ok, len(segments)),
            "taux_attendu": round(attendu, 4)}


def _mcnemar_exact(b: int, c: int) -> float:
    """p bilatéral exact du test de McNemar (binomiale sur les paires discordantes)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = 2.0 * sum(math.comb(n, i) for i in range(k + 1)) / (2.0 ** n)
    return round(min(1.0, p), 6)


# --------------------------------------------------------------------------- évaluation
def _masquer(segments: list[dict], masque: set[str]) -> list[dict]:
    """Copie des segments où les features du masque sont mises à zéro (ablation)."""
    indices = {FEATURES.index(f) for f in masque if f in FEATURES}
    sortie = []
    for s in segments:
        candidats = []
        for c in s["candidats"]:
            x = [0.0 if j in indices else v for j, v in enumerate(c["x"])]
            candidats.append({**c, "x": x})
        sortie.append({**s, "candidats": candidats})
    return sortie


def _evaluer_hors_pli(segments: list[dict], epochs: int, lr: float, l2: float) -> dict:
    """Deux plis appris puis regroupés : chaque segment est prédit par l'autre moitié."""
    modeles = {}
    for parite in (0, 1):
        modeles[parite], _ = entrainer([s for s in segments if s["parite"] == parite],
                                       epochs=epochs, lr=lr, l2=l2)
    ok = 0
    par_type = Counter()
    par_type_n = Counter()
    for s in segments:
        pred, _ = _predire(modeles[1 - s["parite"]], s)
        juste = pred == s["cible"]
        ok += int(juste)
        par_type_n[s["type"]] += 1
        par_type[s["type"]] += int(juste)
    return {"justes": ok, "n": len(segments), "taux": _taux(ok, len(segments)),
            "par_type": {t: {"n": par_type_n[t], "justes": par_type[t],
                             "taux": _taux(par_type[t], par_type_n[t])}
                         for t in TYPES}}


def executer(phrases: list[dict], graine: int = 0, stabilite: int = 10,
             epochs: int = 6000, lr: float = 0.6, l2: float = 0.01) -> dict:
    h = bl.Heuristique()
    segments, stats = construire(phrases, h)
    if not segments:
        raise SystemExit("aucun segment mesurable")
    segments_tries = sorted(segments, key=lambda s: (s["parite"], s["id"]))
    compte_parite = Counter(s["parite"] for s in segments_tries)

    def entrainer_sur(parite: int):
        return entrainer([s for s in segments_tries if s["parite"] == parite],
                         epochs=epochs, lr=lr, l2=l2)

    modeles, infos = {}, {}
    for parite in (0, 1):
        w, info = entrainer_sur(parite)
        modeles[parite] = w
        infos[parite] = info

    sens = {}
    for parite_train in (0, 1):
        test = [s for s in segments_tries if s["parite"] != parite_train]
        train = [s for s in segments_tries if s["parite"] == parite_train]
        modele = modeles[parite_train]
        res_modele = evaluer(modele, test)
        res_regle = evaluer_regle(test)
        res_hasard = evaluer_hasard(test, random.Random(graine))
        sens[f"{'pairs' if parite_train == 0 else 'impairs'}->{'impairs' if parite_train == 0 else 'pairs'}"] = {
            "entrainement": {"segments": len(train), "lignes": infos[parite_train]["lignes"],
                             **infos[parite_train]},
            "test": {"segments": len(test), **{k: res_modele[k] for k in ("justes", "n", "taux")}},
            "modele": res_modele,
            "regle_actuelle": res_regle,
            "hasard": res_hasard,
        }

    # regroupé hors-pli : chaque segment est prédit par le modèle de l'autre moitié
    ok_modele = ok_regle = 0
    par_type_modele = Counter()
    par_type_regle = Counter()
    par_type_n = Counter()
    segments_audit = []
    for s in segments_tries:
        modele = modeles[1 - s["parite"]]
        pred, scores = _predire(modele, s)
        juste = pred == s["cible"]
        ok_modele += int(juste)
        ok_regle += int(s["ok_actuelle"])
        par_type_n[s["type"]] += 1
        par_type_modele[s["type"]] += int(juste)
        par_type_regle[s["type"]] += int(s["ok_actuelle"])
        segments_audit.append({
            "i_seg": len(segments_audit), "id": s["id"], "source": s["source"],
            "plis": s["parite"],
            "texte": s["texte"], "type": s["type"], "segment": s["segment"], "prep": s["prep"],
            "cible": s["cible"], "pred_actuelle": s["pred_actuelle"],
            "pred_modele": pred, "ok_actuelle": bool(s["ok_actuelle"]),
            "ok_modele": bool(juste), "candidats": scores,
        })
    n = len(segments_tries)
    regroupe = {
        "n": n,
        "modele": {"justes": ok_modele, "taux": _taux(ok_modele, n),
                   "par_type": {t: {"n": par_type_n[t], "justes": par_type_modele[t],
                                    "taux": _taux(par_type_modele[t], par_type_n[t])}
                                for t in TYPES}},
        "regle_actuelle": {"justes": ok_regle, "taux": _taux(ok_regle, n),
                           "par_type": {t: {"n": par_type_n[t], "justes": par_type_regle[t],
                                            "taux": _taux(par_type_regle[t], par_type_n[t])}
                                        for t in TYPES}},
    }
    b = sum(1 for s in segments_audit if s["ok_modele"] and not s["ok_actuelle"])
    c = sum(1 for s in segments_audit if s["ok_actuelle"] and not s["ok_modele"])
    mcnemar = {"modele_juste_regle_fausse": b, "regle_juste_modele_fausse": c,
               "p_exact": _mcnemar_exact(b, c)}

    # bootstrap de la différence, sur les prédictions hors-pli
    rng = random.Random(graine)
    predictions = {s["i_seg"]: int(s["ok_modele"]) for s in segments_audit}
    regle_ok = {s["i_seg"]: int(s["ok_actuelle"]) for s in segments_audit}
    ids = [s["i_seg"] for s in segments_audit]
    diffs = []
    for _ in range(2000):
        e = [rng.choice(ids) for _ in range(n)]
        d = sum(predictions[i] - regle_ok[i] for i in e) / n
        diffs.append(d)
    diffs.sort()
    bootstrap = {"tirages": 2000, "difference": round((ok_modele - ok_regle) / n, 4),
                 "ic95": [round(diffs[int(0.025 * len(diffs))], 4),
                          round(diffs[int(0.975 * len(diffs)) - 1], 4)]}

    # stabilité : découpages aléatoires de phrases (même protocole, autre graine)
    stabilite_res = []
    phrases_par_id = {p["id"]: p for p in phrases}
    ids_phrases = sorted(phrases_par_id)
    for k in range(stabilite):
        melange = list(ids_phrases)
        random.Random(1000 + k).shuffle(melange)
        moitie = set(melange[:len(melange) // 2])
        app = [s for s in segments_tries if s["id"] in moitie]
        test = [s for s in segments_tries if s["id"] not in moitie]
        if not app or not test:
            continue
        w, _ = entrainer(app, epochs=epochs, lr=lr, l2=l2)
        rm = evaluer(w, test)
        rr = evaluer_regle(test)
        stabilite_res.append({"modele": rm["taux"], "regle": rr["taux"],
                              "n_test": len(test)})
    if stabilite_res:
        def _moy(vals):
            return round(sum(vals) / len(vals), 4)
        def _ecart(vals):
            m = sum(vals) / len(vals)
            return round((sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5, 4)
        stabilite_resume = {
            "decoupages": len(stabilite_res),
            "modele_moyen": _moy([r["modele"] for r in stabilite_res]),
            "modele_ecart_type": _ecart([r["modele"] for r in stabilite_res]),
            "regle_moyenne": _moy([r["regle"] for r in stabilite_res]),
            "regle_ecart_type": _ecart([r["regle"] for r in stabilite_res]),
            "gain_moyen": round(_moy([r["modele"] for r in stabilite_res])
                                - _moy([r["regle"] for r in stabilite_res]), 4),
        }
    else:
        stabilite_resume = {}

    # repères : accuracy d'entraînement (sur-apprentissage) et rang 0 (prior de proximité)
    app_ok = 0
    app_n = 0
    rang0_ok = 0
    rang0_type = Counter()
    n_type = Counter()
    for s in segments_tries:
        pred_train, _ = _predire(modeles[s["parite"]], s)
        app_ok += int(pred_train == s["cible"])
        app_n += 1
        juste_rang0 = int(s["candidats"][0]["texte"] == s["cible"])
        rang0_ok += juste_rang0
        rang0_type[s["type"]] += juste_rang0
        n_type[s["type"]] += 1
    repere = {"exactitude_entrainement": _taux(app_ok, app_n),
              "rang0_justes": rang0_ok, "rang0_taux": _taux(rang0_ok, app_n),
              "rang0_par_type": {t: {"n": n_type[t], "justes": rang0_type[t],
                                     "taux": _taux(rang0_type[t], n_type[t])}
                                 for t in TYPES}}

    # ablations : que porte le résultat ? On retire des groupes de features, à modèle égal.
    ablations = {}
    for nom, masque in (
        ("sans_rang", {"rang"}),
        ("sans_prior_de_position", {"rang", "distance", "cote_gauche", "cote_dedans"}),
        ("sans_interactions", {f for f in FEATURES if "_x_" in f}),
        ("sans_nature", {"nat_verbe", "pos_verbe", "pos_nom", "GP_x_verbe", "REL_x_verbe",
                         "SUB_x_verbe", "GP_x_posV", "REL_x_posV", "SUB_x_posV",
                         "GEN_x_verbe", "GEN_x_posV"}),
    ):
        ablations[nom] = _evaluer_hors_pli(_masquer(segments_tries, masque),
                                           epochs=epochs, lr=lr, l2=l2)

    # sensibilité : mêmes plis, valeurs d'hyperparamètres différentes (aucune sélection)
    sensibilite = {}
    for l2_v, ep_v in ((0.001, 6000), (0.1, 500), (0.1, 6000)):
        r = _evaluer_hors_pli(segments_tries, ep_v, lr, l2_v)
        sensibilite[f"l2={l2_v},epochs={ep_v}"] = {"justes": r["justes"],
                                                   "n": r["n"], "taux": r["taux"]}

    # hors segments à vivier unique : la mesure ne dépend pas du classement
    uniques = [s for s in segments_tries if len(s["candidats"]) == 1]
    hors_uniques = {
        "n": n - len(uniques),
        "modele": _taux(ok_modele - sum(1 for s in uniques if s["candidats"][0]["texte"] == s["cible"]),
                        n - len(uniques)),
        "regle_actuelle": _taux(ok_regle - sum(1 for s in uniques if s["ok_actuelle"]),
                                n - len(uniques)),
        "segments_vivier_unique": len(uniques),
    }

    # moyenne des deux sens (moyenne de taux, pas regroupée)
    taux = [sens[k]["modele"]["taux"] for k in sens]
    taux_regle = [sens[k]["regle_actuelle"]["taux"] for k in sens]
    moyenne = {
        "modele": round(sum(taux) / len(taux), 4),
        "regle_actuelle": round(sum(taux_regle) / len(taux_regle), 4),
        "gain": round(sum(taux) / len(taux) - sum(taux_regle) / len(taux_regle), 4),
    }

    poids = {
        "pairs->impairs": dict(zip(FEATURES, [round(v, 4) for v in modeles[0]])),
        "impairs->pairs": dict(zip(FEATURES, [round(v, 4) for v in modeles[1]])),
        "moyenne": {f: round((modeles[0][i] + modeles[1][i]) / 2.0, 4)
                    for i, f in enumerate(FEATURES)},
    }
    return {
        "titre": "Classement appris des candidats d'attachement (prototype autonome)",
        "date": "2026-11-05",
        "graine": graine,
        "empreinte_bloc_linguistique": _empreinte_bloc(),
        "note_regle_actuelle": (
            "La règle live mesurée ici est celle de l'empreinte ci-dessus. La consigne citait "
            "123/145 (mesuré en début de session) ; le fichier a ensuite été modifié par un "
            "autre agent (129/145 puis 137/145) pendant la session. Le modèle ne lit pas la "
            "cible choisie par la règle : ses 142/145 ne dépendent pas de cette dérive, seuls "
            "le vivier, la POS et `_est_verbe` (lexique) comptent."),
        "hyperparametres": {"epochs": epochs, "learning_rate": lr, "l2": l2,
                            "ponderation_classes": "équilibrée"},
        "corpus": {"phrases": len(phrases),
                   "tokens": sum(len(p["mots"]) for p in phrases),
                   **stats},
        "protocole": {
            "segments_mesures": len(segments_tries),
            "par_plis": {"pairs": compte_parite[0], "impairs": compte_parite[1]},
            "vivier": "tokens pleins (POS ouverte ou _est_verbe), auxiliaires exclus",
            "liste": "gauche → droite → dedans, puis distance (rang 0 = plus proche à gauche)",
            "modele": "régression logistique binaire, descente de gradient, L2, classes pondérées",
            "selection": "argmax du score sur le vivier",
            "mesure": "égalité exacte avec cibles[0] (celle de evaluer_gold.py)",
            "decoupage": "parité du numéro d'id de phrase ; apprentissage pair → test impair, "
                         "puis inverse ; regroupé hors-pli",
        },
        "features": list(FEATURES),
        "poids": poids,
        "resultats": {"sens": sens, "moyenne_des_sens": moyenne,
                      "regroupe_hors_pli": regroupe,
                      "ablations_hors_pli": ablations,
                      "sensibilite_hyperparametres": sensibilite,
                      "hors_vivier_unique": hors_uniques},
        "controle_negatif": {
            "regle_actuelle_regroupee": regroupe["regle_actuelle"],
            # espérance du hasard uniforme dans le vivier, segment par segment
            "hasard_vivier_attendu": round(sum(
                sum(c["positif"] for c in s["candidats"]) / len(s["candidats"])
                for s in segments_tries) / n, 4),
            "hasard_cibles_distinctes": round(
                1.0 / len({s["cible"] for s in segments_tries}), 4),
            "mcnemar": mcnemar,
            "bootstrap_difference": bootstrap,
            "repere": repere,
        },
        "stabilite_decoupages_aleatoires": stabilite_resume,
        "limites": [
            "145 segments seulement (dont 26 REL) : les écarts de quelques unités ne sont pas "
            "interprétables sans le test apparié et le bootstrap joints.",
            "Le vivier, la POS et la segmentation viennent de l'heuristique : une erreur de "
            "tokenisation ou d'étiquetage est invisible au classement (cas `appelle`/`appelle-moi`).",
            "Les paraphrases du gold (mêmes phrases à quelques mots près) se répartissent des "
            "deux côtés du découpage : les taux absolus sont optimistes, pas forcément le gain.",
            "La convention du gold (verbe gouverneur ou nom antécédent) n'est pas documentée ; "
            "le modèle apprend la convention observée, pas une vérité.",
            "Aucune recherche d'hyperparamètres par pli (valeurs fixées a priori) ; le test "
            "n'est pas réutilisé pour régler le modèle.",
        ],
        "segments": segments_audit,
    }


# --------------------------------------------------------------------------- CLI
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", default=str(SORTIE_DEFAUT),
                    help="chemin du JSON de résultat (défaut : reports/pensee-classement-appris.json)")
    ap.add_argument("--graine", type=int, default=0)
    ap.add_argument("--stabilite", type=int, default=10,
                    help="nombre de découpages aléatoires (0 pour désactiver)")
    ap.add_argument("--epochs", type=int, default=6000)
    ap.add_argument("--lr", type=float, default=0.6)
    ap.add_argument("--l2", type=float, default=0.01)
    ap.add_argument("--verbeux", action="store_true")
    args = ap.parse_args()

    phrases = charger()
    resultat = executer(phrases, graine=args.graine, stabilite=args.stabilite,
                        epochs=args.epochs, lr=args.lr, l2=args.l2)

    sortie = pathlib.Path(args.json)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")

    r = resultat["resultats"]
    print("== corpus ==")
    print("bloc:", resultat["empreinte_bloc_linguistique"])
    print(json.dumps({k: resultat["corpus"][k] for k in
                      ("phrases", "segments_gold_avec_cible", "span_non_predit")},
                     ensure_ascii=False))
    print(json.dumps(resultat["protocole"]["par_plis"], ensure_ascii=False))
    print("== par sens ==")
    for nom, b in r["sens"].items():
        print(f"{nom}: modèle {b['modele']['justes']}/{b['modele']['n']} "
              f"({b['modele']['taux']:.4f}) | règle {b['regle_actuelle']['justes']}/"
              f"{b['regle_actuelle']['n']} ({b['regle_actuelle']['taux']:.4f}) | "
              f"hasard {b['hasard']['taux']:.4f}")
    print("== regroupé hors-pli ==")
    print(f"modèle {r['regroupe_hors_pli']['modele']['justes']}/{r['regroupe_hors_pli']['n']} "
          f"({r['regroupe_hors_pli']['modele']['taux']:.4f}) | règle "
          f"{r['regroupe_hors_pli']['regle_actuelle']['justes']}/"
          f"{r['regroupe_hors_pli']['n']} ({r['regroupe_hors_pli']['regle_actuelle']['taux']:.4f})")
    print("moyenne des sens:", r["moyenne_des_sens"])
    print("McNemar:", resultat["controle_negatif"]["mcnemar"])
    print("bootstrap:", resultat["controle_negatif"]["bootstrap_difference"])
    print("hasard vivier attendu:", resultat["controle_negatif"]["hasard_vivier_attendu"])
    print("repères:", resultat["controle_negatif"]["repere"])
    print("ablations:", {k: v["taux"] for k, v in r["ablations_hors_pli"].items()})
    print("sensibilité:", {k: v["taux"] for k, v in r["sensibilite_hyperparametres"].items()})
    print("hors vivier unique:", r["hors_vivier_unique"])
    print("stabilité:", resultat["stabilite_decoupages_aleatoires"])
    if args.verbeux:
        print("== poids (moyenne des plis) ==")
        for f, v in resultat["poids"]["moyenne"].items():
            print(f"  {f:16s} {v:+.4f}")
    print("JSON ->", sortie)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

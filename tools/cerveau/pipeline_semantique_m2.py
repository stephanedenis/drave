#!/usr/bin/env python3
"""pipeline_semantique_m2.py — B13 + M2 : la chaîne M1 → M2 → M5 → M6.

Ce module est un **test d'intégration**, pas un nouveau module de perception.
Il branche les briques existantes sur un seul flux et mesure chaque étage sur
son propre banc :

- **M1** (`hub.py`) lit la surface et rend le code typé ; la mesure est le code
  exact sur les 528 surfaces réelles, avec et sans contexte ;
- **M2** (`voies.py`) relit la surface et rend les champs dorsaux `de`/`vers`
  (encodeur natif gelé, têtes linéaires) ; la mesure est l'exactitude de champ
  sur les 146 items réels qui portent `de`/`vers`, découpée en surfaces **vues**
  (forme normalisée présente dans l'entraînement synthétique) et **inédites**,
  avec les lésions ventrale/dorsale ;
- **M5** (`predictif.py`) prédit la source/la cible du pas suivant avec le
  plateau ; la mesure est l'exactitude et la surprisal sur un split 80/20 par
  partie, avec le plateau et sans lui ;
- **M6** (`gating.py`) sélectionne la tâche ; la mesure est la porte de
  confluence et la tâche de commutation ;
- **M9** (`lesion.py` pour les principes) applique les privations : M1 sans
  contexte, M2 sans voie ventrale/dorsale, M5 sans plateau ou sans transitions.

Le point méthodologique est le suivant : sur le corpus réel, **M1 est exact**
(528/528). M2, qui lit la même surface avec un encodeur gelé, ne peut donc pas
*ajouter* d'information au code ; il peut seulement le remplacer, et il le
remplace moins bien. Le module mesure ce remplacement au lieu de le supposer :
la chaîne est évaluée avec le champ M1, avec le champ M2, et avec M1 privé de
contexte (le seul cas où M2 pourrait servir de secours). Aucune fusion n'est
inventée : sans porte de confiance, il n'y a pas de mécanisme qui choisisse
M2 plutôt que M1, et le module le dit.

Usage :

    PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python \\
        -m cerveau.pipeline_semantique_m2 --pas 300 --graines 1,2,3 \\
        --sortie /tmp/a9-pipeline-m2.json

Le JSON contient les chiffres, les prédictions par item et les commandes. Le
rapport `/tmp/a9-pipeline-m2.md` est rédigé à partir de ce JSON.
"""
from __future__ import annotations

import argparse
import collections
import dataclasses
import hashlib
import json
import random
import re
import statistics
import time
from pathlib import Path

import torch

from jeux.corpus import construire_corpus
from jeux.corpus_multilingue import construire_corpus_multilingue
from jeux.rsn import RSN
from semantique.entrainer import pad
from semantique.normalisation import normaliser
from semantique.synth_corpus import items_synth
from semantique.typed_corpus import ItemType, items as corpus_items, octets
from semantique.universaux import CHAMPS, code_rsn, resume_contexte

from .bus import Bus
from .episodique import Episodique
from .gating import Porte
from .hub import Hub
from .predictif import Predictif, permuter_contextes
from .sequences import Sequence, corpus
from .voies import VALEURS, Voies, entrainer, evaluer_champs

CHAMPS_DORSAUX = ("de", "vers")
NOM_CHAMPS = tuple(nom for nom, _ in CHAMPS)


# ---------------------------------------------------------------------------
# Contexte : le corpus de séquences ne garde que le résumé textuel du RSN.
# ---------------------------------------------------------------------------
def champs_resume(resume: str) -> dict[str, str]:
    """Décode `resume_contexte` en couples clé/valeur (les listes sont gardées)."""
    return {m.group(1): m.group(2)
            for m in re.finditer(r"(\w+)=(\[[^\]]*\]|\S+)", resume or "")}


def contexte_depuis_resume(resume: str, jeu: str):
    """Reconstruit le RSN de contexte à partir du résumé de `sequences.py`.

    `resume_contexte` jette les champs non listés (ko, komi, variante…), mais
    garde tout ce dont les codecs ont besoin pour désambiguïser un coup :
    plateau, trait, roques, prise en passant, cases, taille. La reconstruction
    est donc suffisante pour la lecture, pas une identité parfaite du RSN.
    """
    c = champs_resume(resume)
    if not c:
        return None
    if jeu == "echecs":
        ep = c.get("ep")
        return RSN("echecs", "etat", {
            "plateau": c["plateau"],
            "trait": c["trait"],
            "roques": c.get("roques") or "-",
            "ep": None if ep in (None, "None", "-") else ep,
            "demi": int(c.get("demi", 0)),
            "plein": int(c.get("plein", 1)),
        })
    if jeu == "dames":
        return RSN("dames", "etat", {
            "cases": c["cases"].split(","),
            "trait": c["trait"],
            "demi": int(c.get("demi", 0)),
        })
    if jeu == "go":
        plateau = [int(x) for x in c["plateau"].strip("[]").split(",") if x.strip()]
        return RSN("go", "etat", {
            "taille": int(c["taille"]),
            "plateau": plateau,
            "trait": int(c["trait"]),
            "passe": int(c.get("passe", 0)),
        })
    if jeu == "morpion":
        cases = [None if x == "." else x for x in c["cases"].split(",")]
        return RSN("morpion", "etat", {
            "taille": int(c["taille"]),
            "cases": cases,
            "trait": c["trait"],
        })
    return None


def code_vide(jeu: str) -> dict:
    """Un code typé dont tous les champs sont absents (perception ratée)."""
    code = {nom: None for nom in NOM_CHAMPS}
    code["jeu"] = jeu
    return code


# ---------------------------------------------------------------------------
# Entrées M2 pour un seul item (le reste passe par `evaluer_champs`)
# ---------------------------------------------------------------------------
def _entrees_voies(m, textes, contextes, seq: int = 64, seq_ctx: int = 192):
    x, masque = pad([octets(normaliser(t), seq) for t in textes])
    if not m.contexte:
        return x, masque, None, None
    c, cm = pad([octets(t or "", seq_ctx) for t in contextes])
    return x, masque, c, cm


def _device_de(m) -> str:
    return str(next(m.parameters()).device)


class PipelineSemantiqueM2:
    """La chaîne B13 avec M2 intercalé entre M1 et M5.

    `voies` est un modèle `Voies` déjà entraîné (ou None : la chaîne reste
    utilisable pour M1/M5/M6, M2 est alors déclaré absent). `device` sert aux
    appels M2 ; M1/M5/M6 sont des modules Python déterministes.
    """

    nom = "B13-M2-pipeline-semantique"

    def __init__(self, voies: Voies | None = None, device: str = "cuda") -> None:
        self.bus = Bus()
        self.hub = Hub(self.bus)
        self.voies = voies
        self.device = device
        self.predictif = Predictif(cible="source", ordre=1, contexte=True,
                                   melange=0.5)
        self.porte = Porte()
        self.memoire = Episodique()

    # ---- M1 ---------------------------------------------------------
    def percevoir(self, texte: str, jeu: str, contexte=None):
        """M1 : surface → code typé. `contexte` est un RSN (pas un résumé)."""
        code = self.hub.percevoir(texte, jeu, contexte)
        if code is not None:
            self.memoire.stocker(texte, code, "?")
        return code

    # ---- M2 ---------------------------------------------------------
    def coder_voies(self, texte: str, jeu: str, contexte=None,
                    seq: int = 64, seq_ctx: int = 192) -> dict | None:
        """M2 : surface (+ contexte) → champs ventraux/dorsaux.

        Rend `None` si aucun modèle M2 n'est branché. Les clés sont celles de
        `VALEURS` : `action` et chaque champ dorsal du modèle. `contexte` peut
        être un RSN (il est résumé) ou directement le résumé textuel.
        """
        if self.voies is None:
            return None
        if isinstance(contexte, RSN):
            contexte = resume_contexte(contexte)
        elif contexte is None:
            contexte = ""
        device = _device_de(self.voies)
        x, masque, c, cm = _entrees_voies(self.voies, [texte], [contexte],
                                          seq=seq, seq_ctx=seq_ctx)
        self.voies.eval()
        with torch.no_grad():
            va, vd = self.voies.logits(
                x.to(device), masque.to(device),
                c.to(device) if c is not None else None,
                cm.to(device) if cm is not None else None,
            )
        out = {"action": VALEURS["action"][int(va[0].argmax())]}
        for nom, tete in vd.items():
            out[nom] = VALEURS[nom][int(tete[0].argmax())]
        return out

    # ---- M5 ---------------------------------------------------------
    def predire(self, sequences):
        """M5 : entraîne puis évalue sur les mêmes séquences (convention B13)."""
        self.predictif.entrainer(sequences)
        return self.predictif.evaluer(sequences)

    # ---- M6 ---------------------------------------------------------
    def selectionner(self, items=None):
        return self.porte.executer(items)

    # ---- flux -------------------------------------------------------
    def etape(self, texte: str, jeu: str, contexte=None) -> dict:
        """Un pas de la chaîne : M1 lit, M2 relit, les deux rendent leur code.

        Le flux n'invente pas de fusion : les deux lectures sont rendues
        côte à côte. C'est à l'appelant (ou à une porte de confiance, qui
        n'existe pas encore) de choisir.
        """
        return {"M1": self.percevoir(texte, jeu, contexte),
                "M2": self.coder_voies(texte, jeu, contexte)}

    # ---- M9 ---------------------------------------------------------
    def lesionner_m1(self, items) -> dict:
        """M1 sans contexte : privation de la position, pas une lésion réelle."""
        n = ok = n_de = ok_de = n_vers = ok_vers = 0
        for it in items:
            code = _code_item(it)
            lu = self.hub.percevoir(it.texte, it.jeu, None)
            n += 1
            ok += int(lu == code)
            if code.get("de") is not None:
                n_de += 1
                ok_de += int(lu is not None and lu.get("de") == code["de"])
            if code.get("vers") is not None:
                n_vers += 1
                ok_vers += int(lu is not None and lu.get("vers") == code["vers"])
        return {
            "n": n,
            "code_exact": ok / max(1, n),
            "de": {"n": n_de, "exact": ok_de / max(1, n_de)},
            "vers": {"n": n_vers, "exact": ok_vers / max(1, n_vers)},
        }

    def lesionner_m2(self, items, champs=CHAMPS_DORSAUX, lesions: bool = True) -> dict:
        """M2 : bruit gaussien sur les logits ventraux ou dorsaux."""
        if self.voies is None:
            raise ValueError("aucun modèle M2 branché")
        return evaluer_champs(self.voies, items, champs=tuple(champs),
                              device=_device_de(self.voies), lesions=lesions,
                              retour_pred=True)

    def lesionner_m5(self, train, test, cible: str = "source") -> dict:
        """M5 : sans plateau, puis sans transitions (ordre 0)."""
        out = {}
        for nom, contexte, ordre in (
            ("avec_plateau", True, 1),
            ("sans_plateau", False, 1),
            ("sans_transitions", True, 0),
            ("sans_plateau_ni_transitions", False, 0),
        ):
            m = Predictif(cible=cible, ordre=ordre, contexte=contexte,
                          melange=0.5)
            m.entrainer(train)
            out[nom] = m.evaluer(test)
        return out


# ---------------------------------------------------------------------------
# Utilitaires de mesure
# ---------------------------------------------------------------------------
def _code_item(it) -> dict:
    """Le code de référence d'un item (ItemType ou Item du corpus)."""
    if hasattr(it, "code") and isinstance(it.code, dict):
        return it.code
    return code_rsn(it.attendu)


def _items_reels():
    out = []
    for c in (construire_corpus(), construire_corpus_multilingue()):
        out += [it for it in c.items if it.attendu.nature == "coup"]
    return out


def _macro_rappel(pred, cible) -> float:
    par = collections.defaultdict(lambda: [0, 0])
    for p, c in zip(pred, cible):
        par[c][0] += int(p == c)
        par[c][1] += 1
    return sum(a / b for a, b in par.values()) / max(1, len(par))


def _exact(pred, cible) -> float:
    return sum(int(a == b) for a, b in zip(pred, cible)) / max(1, len(cible))


def _stats_champ(pred, cible, vu, couvert) -> dict:
    """Exactitude globale et par sous-ensemble (vu / inédit / nouvelle classe)."""
    def sous(masque):
        p = [x for x, m in zip(pred, masque) if m]
        c = [x for x, m in zip(cible, masque) if m]
        return {"n": len(c), "exact": _exact(p, c) if c else 0.0}

    inedit = [not v for v in vu]
    inedit_couvert = [i and c for i, c in zip(inedit, couvert)]
    nouvelle = [i and not c for i, c in zip(inedit, couvert)]
    global_ = sous([True] * len(cible))
    global_["macro_rappel"] = _macro_rappel(pred, cible)
    global_["majorite"] = (max(collections.Counter(cible).values())
                           / max(1, len(cible)))
    return {
        "global": global_,
        "vu": sous(vu),
        "inedit": sous(inedit),
        "inedit_couvert": sous(inedit_couvert),
        "nouvelle_classe": sous(nouvelle),
    }


def _masques_m2(items_, synth, champ):
    """Vu = forme normalisée présente dans l'entraînement ; couvert = classe."""
    train = [i for i in synth if i.code.get(champ) is not None]
    formes = {normaliser(i.texte) for i in train}
    classes = {i.code[champ] for i in train}
    vu = [normaliser(i.texte) in formes for i in items_]
    couvert = [i.code[champ] in classes for i in items_]
    return vu, couvert


def _plat(res: dict, prefixe: str = "") -> dict:
    """Aplatit les métriques utiles d'un `evaluer_champs` pour un champ."""
    nom = prefixe
    return {
        f"{nom}global_exact": res["global"]["exact"],
        f"{nom}global_macro": res["global"]["macro_rappel"],
        f"{nom}vu_exact": res["vu"]["exact"],
        f"{nom}vu_n": res["vu"]["n"],
        f"{nom}inedit_exact": res["inedit"]["exact"],
        f"{nom}inedit_n": res["inedit"]["n"],
        f"{nom}inedit_couvert_exact": res["inedit_couvert"]["exact"],
        f"{nom}inedit_couvert_n": res["inedit_couvert"]["n"],
        f"{nom}nouvelle_classe_exact": res["nouvelle_classe"]["exact"],
        f"{nom}nouvelle_classe_n": res["nouvelle_classe"]["n"],
    }


def _agg(valeurs: list) -> dict:
    """Moyenne ± écart-type (échantillon) sur les graines."""
    vals = [float(v) for v in valeurs]
    return {
        "moyenne": statistics.mean(vals),
        "ecart_type": statistics.stdev(vals) if len(vals) > 1 else 0.0,
        "valeurs": vals,
    }


def _agg_dict(par_graine: dict[str, dict]) -> dict:
    """Agrège des dictionnaires plats de même schéma, clé par clé."""
    cles = sorted(set.intersection(*(set(v) for v in par_graine.values())))
    return {cle: _agg([v[cle] for v in par_graine.values()]) for cle in cles}


def _sequence_avec_codes(seq: Sequence, codes: list[dict]) -> Sequence:
    pas = tuple(dataclasses.replace(p, code=codes[i])
                for i, p in enumerate(seq.pas))
    return Sequence(seq.jeu, pas)


def _percevoir_sequences(sequences, hub: Hub, avec_contexte: bool = True):
    """Fait passer les surfaces d'une séquence par M1 et rend les codes."""
    codes = []
    n = ok = n_none = 0
    for seq in sequences:
        cs = []
        for p in seq.pas:
            ctx = (contexte_depuis_resume(p.contexte, p.jeu)
                   if avec_contexte else None)
            c = hub.percevoir(p.surface, p.jeu, ctx)
            if c is None:
                c = code_vide(p.jeu)
                n_none += 1
            cs.append(c)
            n += 1
            ok += int(c == p.code)
        codes.append(cs)
    return codes, {"n": n, "code_exact": ok / max(1, n), "n_none": n_none}


def _sequences_codes(sequences, codes) -> list[Sequence]:
    return [_sequence_avec_codes(s, c) for s, c in zip(sequences, codes)]


def _eval_m5(train, test, cible: str = "source", contexte: bool = True,
             ordre: int = 1, melange: float = 0.5) -> dict:
    m = Predictif(cible=cible, ordre=ordre, contexte=contexte,
                  melange=melange)
    m.entrainer(train)
    return m.evaluer(test)


def _m5_compact(res: dict) -> dict:
    return {cle: res[cle] for cle in
            ("n", "exact", "majoritaire", "surprise", "surprise_majoritaire",
             "gain", "gain_surprise", "hors_vocabulaire", "cible", "ordre")}


def _m5_par_jeu(train, test, cible: str, contexte: bool, ordre: int) -> dict:
    """Décomposition par jeu, au même réglage que le résultat global."""
    m = Predictif(cible=cible, ordre=ordre, contexte=contexte, melange=0.5)
    m.entrainer(train)
    return _par_jeu_modele(m, test)


def _par_jeu_modele(modele: Predictif, test) -> dict:
    """Évalue un modèle déjà entraîné, jeu par jeu.

    Sert au contrôle M1 lésé : il montre quels jeux **survivent** à la
    privation de contexte et lesquels sont perdus. Un exact plus haut sur un
    sous-ensemble plus petit n'est pas un gain, c'est une sélection.
    """
    out = {}
    for jeu in sorted({s.jeu for s in test}):
        sous = [s for s in test if s.jeu == jeu]
        if not sous:
            continue
        r = modele.evaluer(sous)
        if r["n"]:
            out[jeu] = {cle: r[cle] for cle in
                        ("n", "exact", "majoritaire", "surprise",
                         "surprise_majoritaire", "gain_surprise")}
    return out


# ---------------------------------------------------------------------------
# M2 : entraînement (avec cache de têtes) et évaluation
# ---------------------------------------------------------------------------
def _cle_cache(config: dict) -> str:
    brut = json.dumps(config, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(brut.encode("utf-8")).hexdigest()[:12]


def _train_m2(base, pas: int, graine: int, contexte: bool, lot: int = 32,
              seq: int = 64, device: str = "cuda", cache_dir=None,
              reuse: bool = False):
    """Entraîne M2 sur les surfaces synthétiques, ou recharge les têtes du cache."""
    config = {"checkpoint": str(base.config._name_or_path), "pas": int(pas),
              "graine": int(graine), "contexte": bool(contexte),
              "champs": list(CHAMPS_DORSAUX), "pool": "mean+last",
              "lot": int(lot), "seq": int(seq)}
    cache = None
    if cache_dir:
        cache = Path(cache_dir) / f"m2-{_cle_cache(config)}.pt"
        if reuse and cache.exists():
            m = Voies(base, champs_dorsaux=CHAMPS_DORSAUX, pool="mean+last",
                      contexte=contexte).to(device)
            for p in m.base.parameters():
                p.requires_grad = False
            charge = torch.load(cache, map_location=device, weights_only=False)
            m.load_state_dict(charge["tetes"], strict=False)
            m.eval()
            return m, {"graine": graine, "contexte": contexte,
                       "duree_s": 0.0, "cache": str(cache)}

    torch.manual_seed(int(graine))
    t0 = time.time()
    m, _ = entrainer(base, pas=pas, lot=lot, seq=seq, graine=graine,
                     device=device, synth=True, champs=CHAMPS_DORSAUX,
                     pool="mean+last", contexte=contexte)
    duree = time.time() - t0
    if cache is not None:
        cache.parent.mkdir(parents=True, exist_ok=True)
        tetes = {k: v.detach().cpu()
                 for k, v in m.state_dict().items()
                 if not k.startswith("base.")}
        torch.save({"tetes": tetes, "config": config}, cache)
    return m, {"graine": graine, "contexte": contexte, "duree_s": duree,
               "cache": str(cache) if cache else None}


def _mesurer_m2(m, items_, synth, contexte_mode: str = "reel",
                lesions: bool = True) -> dict:
    """Évalue `de`/`vers` sur les 146 items, avec masques vu/inédit et lésions."""
    r = evaluer_champs(m, items_, champs=CHAMPS_DORSAUX, device=_device_de(m),
                       lesions=lesions, contexte_mode=contexte_mode,
                       retour_pred=True)
    out = {"conditions": {}, "predictions": {}}
    for champ in CHAMPS_DORSAUX:
        res = r[champ]
        vu, couvert = _masques_m2(items_, synth, champ)
        stats = _stats_champ(res["pred"], res["cible"], vu, couvert)
        plat = _plat(stats)
        plat["action"] = res["action"]
        if lesions and "lesions" in res:
            plat["lesion_ventrale_action"] = res["lesions"]["ventrale"]["action"]
            plat["lesion_ventrale_champ"] = res["lesions"]["ventrale"][champ]
            plat["lesion_dorsale_action"] = res["lesions"]["dorsale"]["action"]
            plat["lesion_dorsale_champ"] = res["lesions"]["dorsale"][champ]
        out["conditions"][champ] = plat
        out["predictions"][champ] = {
            "pred": res["pred"], "cible": res["cible"], "ok": res["ok"],
            "vu": vu, "couvert": couvert,
        }
    return out


# ---------------------------------------------------------------------------
# La mesure complète
# ---------------------------------------------------------------------------
def mesurer(pas: int = 300, graines=(1, 2, 3), device: str = "cuda",
            checkpoint: str = "/tmp/natif-600-512-8-align-s1",
            cache_dir: str | None = "/tmp/a9-m2-cache",
            reuse: bool = False, sortie: str | None = None,
            m5_graine: int = 3, m5_fraction: float = 0.8,
            sequences_n: int = 200, sequences_pas: int = 12) -> dict:
    """Exécute la chaîne complète et rend le dictionnaire de mesures.

    Aucune modification des modules existants : tout passe par leurs API
    publiques (`Hub`, `Voies`/`entrainer`/`evaluer_champs`, `Predictif`,
    `Porte`). Les seules fonctions locales sont le rebranchissement (M2 →
    code) et la reconstruction du contexte des séquences.
    """
    from transformers import AutoModelForCausalLM

    t0 = time.time()
    torch.manual_seed(0)
    base = AutoModelForCausalLM.from_pretrained(checkpoint,
                                                dtype=torch.float32)
    base.eval()
    for p in base.parameters():
        p.requires_grad = False

    its = corpus_items()
    synth = items_synth()
    reels = _items_reels()
    items_146 = [i for i in its if i.code.get("de") is not None]
    # invariant du corpus : les 146 items de `de` sont les 146 de `vers`.
    assert {id(i) for i in items_146} == {
        id(i) for i in its if i.code.get("vers") is not None}

    p = PipelineSemantiqueM2(voies=None, device=device)
    hub = Hub()

    # ---- M1 ---------------------------------------------------------
    m1_avec = {"n": len(reels), "n_ok": 0, "de": {"n": 0, "n_ok": 0},
               "vers": {"n": 0, "n_ok": 0}}
    m1_sans = {"n": len(reels), "n_ok": 0, "de": {"n": 0, "n_ok": 0},
               "vers": {"n": 0, "n_ok": 0}}
    for it in reels:
        code = code_rsn(it.attendu)
        a = hub.percevoir(it.texte, it.jeu, it.contexte)
        s = hub.percevoir(it.texte, it.jeu, None)
        m1_avec["n_ok"] += int(a == code)
        m1_sans["n_ok"] += int(s == code)
        for nom in CHAMPS_DORSAUX:
            if code.get(nom) is not None:
                m1_avec[nom]["n"] += 1
                m1_avec[nom]["n_ok"] += int(a is not None
                                           and a.get(nom) == code[nom])
                m1_sans[nom]["n"] += 1
                m1_sans[nom]["n_ok"] += int(s is not None
                                            and s.get(nom) == code[nom])
    for d in (m1_avec, m1_sans):
        d["code_exact"] = d["n_ok"] / max(1, d["n"])
        for nom in CHAMPS_DORSAUX:
            d[nom]["exact"] = d[nom]["n_ok"] / max(1, d[nom]["n"])

    # ---- M2 : entraînement des deux conditions ----------------------
    modeles = {}
    infos_train = []
    for graine in graines:
        for contexte in (True, False):
            m, info = _train_m2(base, pas, graine, contexte, device=device,
                                cache_dir=cache_dir, reuse=reuse)
            modeles[(graine, contexte)] = m
            infos_train.append(info)

    # ---- M2 : évaluation par condition ------------------------------
    par_graine = {"contexte_reel": {}, "contexte_vide": {}, "sans_contexte": {}}
    predictions = {"contexte_reel": {}, "contexte_vide": {}}
    for graine in graines:
        m_ctx = modeles[(graine, True)]
        m_nc = modeles[(graine, False)]
        reel = _mesurer_m2(m_ctx, items_146, synth, "reel", lesions=True)
        vide = _mesurer_m2(m_ctx, items_146, synth, "vide", lesions=False)
        sans = _mesurer_m2(m_nc, items_146, synth, "reel", lesions=True)
        for nom, r in (("contexte_reel", reel), ("contexte_vide", vide),
                       ("sans_contexte", sans)):
            plat = {}
            for champ in CHAMPS_DORSAUX:
                plat.update({f"{champ}_{k}": v
                             for k, v in r["conditions"][champ].items()})
            par_graine[nom][graine] = plat
            if nom in predictions:
                predictions[nom][graine] = {
                    champ: r["predictions"][champ] for champ in CHAMPS_DORSAUX}
    m2 = {nom: _agg_dict(v) for nom, v in par_graine.items()}
    m2["predictions"] = predictions
    m2["entrainements"] = infos_train

    # ---- Chaîne : M1 seul, M1 remplacé par M2, M1 sans contexte -----
    # Le seul point où M2 peut agir est le champ dorsal : on compare les trois
    # lectures sur les mêmes 146 items.
    chaine = {"sans_m2": {"de": m1_avec["de"]["exact"],
                          "vers": m1_avec["vers"]["exact"]},
              "m1_sans_contexte": {"de": m1_sans["de"]["exact"],
                                   "vers": m1_sans["vers"]["exact"]},
              "avec_m2": {}, "par_graine": {}}
    # La lecture M1 sans contexte, par item et par champ : la même pour toutes
    # les graines, on la calcule une fois.
    m1_sans_ok = {}
    for champ in CHAMPS_DORSAUX:
        ok = []
        for it in items_146:
            lu = hub.percevoir(it.texte, it.jeu, None)
            ok.append(int(lu is not None and lu.get(champ) == it.code[champ]))
        m1_sans_ok[champ] = ok
    for graine in graines:
        pred = predictions["contexte_reel"][graine]
        d = {}
        for champ in CHAMPS_DORSAUX:
            ok = pred[champ]["ok"]
            d[champ] = sum(ok) / max(1, len(ok))
            # secours oracle : M2 corrige-t-il les erreurs de M1 sans contexte ?
            erreurs = [i for i, v in enumerate(m1_sans_ok[champ]) if not v]
            secours = sum(int(ok[i]) for i in erreurs)
            d[f"{champ}_oracle_secours"] = secours
            d[f"{champ}_erreurs_m1_sans_contexte"] = len(erreurs)
            d[f"{champ}_oracle_exact"] = (
                sum(int(a or b) for a, b in zip(m1_sans_ok[champ], ok))
                / max(1, len(ok)))
        chaine["par_graine"][graine] = d
    for champ in CHAMPS_DORSAUX:
        chaine["avec_m2"][champ] = _agg(
            [chaine["par_graine"][g][champ] for g in graines])
        chaine[f"{champ}_oracle_secours"] = _agg(
            [chaine["par_graine"][g][f"{champ}_oracle_secours"]
             for g in graines])
        chaine[f"{champ}_erreurs_m1_sans_contexte"] = _agg(
            [chaine["par_graine"][g][f"{champ}_erreurs_m1_sans_contexte"]
             for g in graines])
        chaine[f"{champ}_oracle_exact"] = _agg(
            [chaine["par_graine"][g][f"{champ}_oracle_exact"]
             for g in graines])

    # ---- M5 ---------------------------------------------------------
    sequences = corpus(0, sequences_n, sequences_pas)
    idx = list(range(len(sequences)))
    random.Random(m5_graine).shuffle(idx)
    n_train = int(len(idx) * m5_fraction)
    train = [sequences[i] for i in idx[:n_train]]
    test = [sequences[i] for i in idx[n_train:]]
    codes_train, info_m1_train = _percevoir_sequences(train, hub, True)
    codes_test, info_m1_test = _percevoir_sequences(test, hub, True)
    codes_train_nc, info_m1_train_nc = _percevoir_sequences(train, hub, False)
    codes_test_nc, info_m1_test_nc = _percevoir_sequences(test, hub, False)
    train_m1 = _sequences_codes(train, codes_train)
    test_m1 = _sequences_codes(test, codes_test)
    train_nc = _sequences_codes(train, codes_train_nc)
    test_nc = _sequences_codes(test, codes_test_nc)

    m5 = {"sequences": {"n": len(sequences), "n_train": len(train),
                        "n_test": len(test), "graine_split": m5_graine,
                        "fraction": m5_fraction},
          "m1_sur_sequences": {"avec_contexte": info_m1_test,
                               "sans_contexte": info_m1_test_nc,
                               "avec_contexte_train": info_m1_train,
                               "sans_contexte_train": info_m1_train_nc},
          "source": {}, "cible": {}}
    for cible in ("source", "cible"):
        ref = _eval_m5(train, test, cible, True, 1)
        m1 = _eval_m5(train_m1, test_m1, cible, True, 1)
        sans = _eval_m5(train_m1, test_m1, cible, False, 1)
        trans = _eval_m5(train_m1, test_m1, cible, True, 0)
        lese_modele = Predictif(cible=cible, ordre=1, contexte=True,
                                melange=0.5)
        lese_modele.entrainer(train_nc)
        lese = lese_modele.evaluer(test_nc)
        perm = _eval_m5(train_m1, permuter_contextes(test_m1, graine=0),
                        cible, True, 1)
        n_ref = max(1, ref["n"])
        m5[cible] = {
            "reference_codes_vrais": _m5_compact(ref),
            "chaine_m1": _m5_compact(m1),
            "sans_plateau": _m5_compact(sans),
            "sans_transitions": _m5_compact(trans),
            "m1_sans_contexte": _m5_compact(lese),
            "plateau_permute": _m5_compact(perm),
            "couverture_m1_sans_contexte": lese["n"] / n_ref,
            "note_m1_sans_contexte": (
                "exact sur les pas qui survivent à la privation de contexte ; "
                "la couverture n/ref et le détail par jeu montrent que le gain "
                "apparent est une sélection, pas une amélioration"),
            "par_jeu_reference": _m5_par_jeu(train, test, cible, True, 1),
            "par_jeu_sans_plateau": _m5_par_jeu(train_m1, test_m1, cible,
                                                False, 1),
            "par_jeu_m1_sans_contexte": _par_jeu_modele(lese_modele, test_nc),
        }

    # ---- M6 ---------------------------------------------------------
    porte = Porte()
    m6 = {"confluence": porte.executer(), "commutation": porte.executer_switch()}

    # ---- M9 : les déficits, calculés depuis les mesures ci-dessus ----
    m9 = {
        "M1_sans_contexte": {
            "code_exact": m1_sans["code_exact"],
            "de_exact": m1_sans["de"]["exact"],
            "vers_exact": m1_sans["vers"]["exact"],
            "deficit_code": m1_avec["code_exact"] - m1_sans["code_exact"],
        },
        "M2": {},
        "M5": {},
    }
    for champ in CHAMPS_DORSAUX:
        normal = m2["contexte_reel"][f"{champ}_global_exact"]["moyenne"]
        lv = m2["contexte_reel"][f"{champ}_lesion_ventrale_champ"]["moyenne"]
        ld = m2["contexte_reel"][f"{champ}_lesion_dorsale_champ"]["moyenne"]
        m9["M2"][champ] = {
            "normal": normal,
            "lesion_ventrale": lv,
            "lesion_dorsale": ld,
            "deficit_ventral": normal - lv,
            "deficit_dorsal": normal - ld,
        }
    for cible in ("source", "cible"):
        ref = m5[cible]["chaine_m1"]
        for nom, res in (("sans_plateau", m5[cible]["sans_plateau"]),
                         ("sans_transitions", m5[cible]["sans_transitions"]),
                         ("m1_sans_contexte", m5[cible]["m1_sans_contexte"])):
            m9["M5"][f"{cible}_{nom}"] = {
                "reference_exact": ref["exact"],
                "lessee_exact": res["exact"],
                "deficit_exact": ref["exact"] - res["exact"],
                "reference_surprise": ref["surprise"],
                "lessee_surprise": res["surprise"],
                "gain_surprise": ref["surprise"] - res["surprise"],
                "n_reference": ref["n"],
                "n_lessee": res["n"],
                "couverture": res["n"] / max(1, ref["n"]),
            }

    # ---- Flux : la chaîne se parle-t-elle ? -------------------------
    exemple = items_146[0]
    ctx = None
    # retrouver un contexte RSN réel pour l'exemple
    for it in reels:
        if (it.texte, it.jeu) == (exemple.texte, exemple.jeu):
            ctx = it.contexte
            break
    code_m1 = hub.percevoir(exemple.texte, exemple.jeu, ctx)
    # `p` n'a pas encore de modèle : on prend la graine 1, condition contexte.
    p.voies = modeles[(graines[0], True)]
    code_m2 = p.coder_voies(exemple.texte, exemple.jeu, ctx)
    p.predictif = Predictif(cible="source", ordre=1, contexte=True,
                            melange=0.5)
    p.predictif.entrainer(train_m1)
    pred_m5, prob_m5 = p.predictif.predire(
        code_m1, contexte=getattr(exemple, "contexte", None))
    flux = {
        "exemple": {"texte": exemple.texte, "jeu": exemple.jeu,
                    "code_attendu": exemple.code},
        "m1": code_m1,
        "m2": code_m2,
        "m5": {"cible": p.predictif.cible, "valeur": pred_m5,
               "probabilite": prob_m5},
        "m6": {"exact": m6["confluence"]["exact"], "n": m6["confluence"]["n"]},
        "m2_consomme_par_m5": False,
        "note": ("M5 consomme le code M1 ; aucun étage ne consomme M2. "
                 "La chaîne se parle, mais M2 est un rameau latéral."),
    }

    duree = time.time() - t0
    resultat = {
        "meta": {
            "nom": "A9 — B13 + M2 (M1 → M2 → M5 → M6)",
            "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "duree_s": duree,
            "pas_m2": pas,
            "graines": list(graines),
            "device": device,
            "checkpoint": checkpoint,
            "torch": torch.__version__,
            "cuda": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "commande": ("PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 "
                         "/home/stephane/gpu-env/bin/python -m "
                         "cerveau.pipeline_semantique_m2 --pas %d --graines %s "
                         "--sortie /tmp/a9-pipeline-m2.json"
                         % (pas, ",".join(str(g) for g in graines))),
        },
        "corpus": {
            "n_items_types": len(its),
            "n_items_reels": len(reels),
            "n_de": len(items_146),
            "n_vers": len(items_146),
            "n_synth": len(synth),
            "vu": {"de": sum(_masques_m2(items_146, synth, "de")[0]),
                   "vers": sum(_masques_m2(items_146, synth, "vers")[0])},
        },
        "M1": {"avec_contexte": m1_avec, "sans_contexte": m1_sans},
        "M2": m2,
        "chaine": chaine,
        "M5": m5,
        "M6": m6,
        "M9": m9,
        "flux": flux,
        "verdict": _verdict(m1_avec, m2, chaine, m5, m6),
    }
    if sortie:
        Path(sortie).parent.mkdir(parents=True, exist_ok=True)
        Path(sortie).write_text(json.dumps(resultat, ensure_ascii=False,
                                           indent=1, default=str))
    return resultat


def _verdict(m1, m2, chaine, m5, m6) -> dict:
    """Les phrases que les chiffres autorisent, et celles qu'ils interdisent."""
    de = m2["contexte_reel"]["de_global_exact"]["moyenne"]
    vers = m2["contexte_reel"]["vers_global_exact"]["moyenne"]
    ameliore = (de > m1["de"]["exact"] or vers > m1["vers"]["exact"])
    return {
        "M1_code_exact": m1["code_exact"],
        "M1_de_exact": m1["de"]["exact"],
        "M1_vers_exact": m1["vers"]["exact"],
        "M2_de_exact": de,
        "M2_vers_exact": vers,
        "M2_ecart_de": de - m1["de"]["exact"],
        "M2_ecart_vers": vers - m1["vers"]["exact"],
        "M2_sans_contexte_de": m2["sans_contexte"]["de_global_exact"]["moyenne"],
        "M2_sans_contexte_vers": m2["sans_contexte"]["vers_global_exact"]["moyenne"],
        "M2_egal_M1": de == m1["de"]["exact"] and vers == m1["vers"]["exact"],
        "M2_avec_m2_de": chaine["avec_m2"]["de"]["moyenne"],
        "M2_avec_m2_vers": chaine["avec_m2"]["vers"]["moyenne"],
        "M5_source_avec_plateau": m5["source"]["chaine_m1"]["exact"],
        "M5_source_sans_plateau": m5["source"]["sans_plateau"]["exact"],
        "M5_source_surprise_avec": m5["source"]["chaine_m1"]["surprise"],
        "M5_source_surprise_sans": m5["source"]["sans_plateau"]["surprise"],
        "M5_source_gain_surprise": (m5["source"]["chaine_m1"]["surprise"]
                                    - m5["source"]["sans_plateau"]["surprise"]),
        "M5_source_m1_sans_contexte": m5["source"]["m1_sans_contexte"]["exact"],
        "M6_confluence": m6["confluence"]["exact"],
        "M6_commutation": m6["commutation"]["exact"],
        "ajoute": bool(ameliore),
        "phrase": (
            "M2 n'ajoute rien à la chaîne : M1 lit 100 % des 146 items réels, "
            "M2 93–94 %, et aucun étage ne consomme M2. Remplacer M1 par M2 "
            "ne peut que dégrader le champ dorsal."
            if not ameliore else
            "M2 dépasse M1 sur au moins un champ : à vérifier, M1 est exact "
            "sur le corpus réel."),
        "nuance": ("M2 est un rameau neural parallèle, pas un étage de la "
                   "chaîne ; il ne pourrait servir que de secours sur des "
                   "surfaces que le codec ne lit pas, cas absent de ce corpus "
                   "et non mesuré ici."),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pas", type=int, default=300)
    ap.add_argument("--graines", default="1,2,3")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--checkpoint", default="/tmp/natif-600-512-8-align-s1")
    ap.add_argument("--cache", default="/tmp/a9-m2-cache")
    ap.add_argument("--reuse", action="store_true")
    ap.add_argument("--sortie", default="/tmp/a9-pipeline-m2.json")
    ap.add_argument("--m5-graine", type=int, default=3)
    ap.add_argument("--m5-fraction", type=float, default=0.8)
    ap.add_argument("--sequences-n", type=int, default=200)
    ap.add_argument("--sequences-pas", type=int, default=12)
    args = ap.parse_args()
    graines = tuple(int(x) for x in args.graines.split(",") if x.strip())
    r = mesurer(pas=args.pas, graines=graines, device=args.device,
                checkpoint=args.checkpoint, cache_dir=args.cache,
                reuse=args.reuse, sortie=args.sortie,
                m5_graine=args.m5_graine, m5_fraction=args.m5_fraction,
                sequences_n=args.sequences_n,
                sequences_pas=args.sequences_pas)
    print(json.dumps({
        "duree_s": round(r["meta"]["duree_s"], 1),
        "M1": r["verdict"]["M1_code_exact"],
        "M2_de": r["verdict"]["M2_de_exact"],
        "M2_vers": r["verdict"]["M2_vers_exact"],
        "M2_sans_contexte_de": r["verdict"]["M2_sans_contexte_de"],
        "M5_source": r["verdict"]["M5_source_avec_plateau"],
        "M5_source_sans_plateau": r["verdict"]["M5_source_sans_plateau"],
        "M6_confluence": r["verdict"]["M6_confluence"],
        "sortie": args.sortie,
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

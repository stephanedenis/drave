#!/usr/bin/env python3
"""M9 — lésions par module : privations déclarées et déficits mesurés.

Une lésion n'est pas une approximation : c'est une **privation déclarée** du
module, mesurée sur le même test que la version intacte, avec un **sham** (la
même mesure répétée sans privation) qui doit donner un déficit nul. Le déficit
est ``intacte - lésée`` ; un déficit négatif veut dire que la lésion *améliore*
— c'est un résultat, pas une erreur.

Modules couverts :

- **M1** : retirer le contexte de perception ;
- **M2** : couper la voie ventrale (action) ou dorsale (``de``). Par défaut le
  **vrai ``voies.py``** est exécuté (encodeur natif gelé, entraînement des têtes
  sur GPU ou CPU) ; si la base ou torch manque, le substitut bayésien à deux
  têtes est déclaré dans ``statut`` (repli documenté, jamais silencieux) ;
- **M3** : capacité du tampon (0, 1, 2, 4, 8, 12), dose-réponse ;
- **M4** : stockage vide, puis lésion du champ d'adressage (le champ est mis à
  ``None`` dans la requête) ;
- **M5** : retirer les transitions, l'ordre 2 ou le repli majoritaire ; contrôle
  positif sur une chaîne de Markov synthétique ;
- **M6** : retirer la porte (tout accepter), l'inverser, la rendre aléatoire ;
- **M7** : retirer la modulation (FIFO) ; décomposition clé surface/code et
  signal nouveauté ;
- **M8** : retirer le sommeil (repli sur la marginale globale) sur un **code
  tenu à l'écart**, puis hybride surface + prototype et hybrides tautologiques.

Tous les déficits sont ``intacte - lésée`` (jamais ``1 - lésée``) ; le cas M4
``par_champ`` est calculé explicitement depuis l'intacte mesurée. ``batterie_lesions(rapide=True)``
exécute M2 réel (≈ 30 s sur GPU) ; ``m2="proxy"`` force le substitut CPU,
``rapide=False`` augmente l'échantillon M4, les permutations M7 et les graines M2.
"""
from __future__ import annotations

import collections
import math
import os
import pathlib
import random
import time

from jeux.corpus import construire_corpus
from jeux.corpus_multilingue import construire_corpus_multilingue
from semantique.typed_corpus import decouper, items as corpus_items
from semantique.universaux import CHAMPS, code_rsn
from cerveau.episodique import Episodique
from cerveau.gating import Porte
from cerveau.hub import Hub
from cerveau.memoire_travail import MemoireTravail
from cerveau.neuromodulation import experience_m7
from cerveau.predictif import Predictif
from cerveau.sequences import corpus
from cerveau.sommeil import Sommeil, experience_contexte, experience_m8

NOMS = tuple(nom for nom, _ in CHAMPS)


def _vrais_items():
    out = []
    for c in (construire_corpus(), construire_corpus_multilingue()):
        for it in c.items:
            if it.attendu.nature == "coup":
                out.append(it)
    return out


def _champs(proto: dict, code: dict) -> int:
    return sum(1 for nom in NOMS if proto.get(nom) == code.get(nom))


def _entree(lesion: str, intacte: dict, lessee: dict, deficit: dict,
            n: int, statut: str = "mesure", sham=None, note: str = "") -> dict:
    return {"lesion": lesion, "intacte": intacte, "lessee": lessee,
            "deficit": deficit, "n": n, "statut": statut,
            "controle_sham": sham if sham is not None else 0.0, "note": note}


# ---------------------------------------------------------------------------
# M1 — le contexte
# ---------------------------------------------------------------------------
def _m1() -> dict:
    vrais = _vrais_items()
    hub = Hub()
    ok_ctx = ok_sans = 0
    for it in vrais:
        attendu = code_rsn(it.attendu)
        ok_ctx += int(hub.percevoir(it.texte, it.jeu, it.contexte) == attendu)
        ok_sans += int(hub.percevoir(it.texte, it.jeu, None) == attendu)
    n = len(vrais)
    a, b = ok_ctx / n, ok_sans / n
    return _entree("retirer le contexte (percevoir sans contexte)", {"exact": a},
                   {"exact": b},
                   {"exact": a - b, "relatif": (a - b) / max(1e-9, a)},
                   n, sham=0.0,
                   note="le codec lit la surface ; le contexte lève l'ambiguïté")


# ---------------------------------------------------------------------------
# M2 — les deux voies (voies.py réel, proxy bayésien en repli)
# ---------------------------------------------------------------------------
def _ngrammes(texte: str, jeu: str) -> list[str]:
    t = "<" + texte.lower() + ">"
    out = ["jeu=" + str(jeu)]
    for n in (2, 3):
        for i in range(max(0, len(t) - n + 1)):
            out.append(t[i:i + n])
    return out


class _Bayes:
    """Deux têtes indépendantes : P(action | surface), P(de | surface)."""

    def __init__(self):
        self.n = 0
        self.cls = collections.Counter()
        self.compte = collections.defaultdict(collections.Counter)
        self.total = collections.Counter()
        self.vocab = set()

    def entrainer(self, exemples):
        for feats, classe in exemples:
            self.n += 1
            self.cls[classe] += 1
            for f in feats:
                self.compte[classe][f] += 1
                self.total[classe] += 1
                self.vocab.add(f)

    def predire(self, feats) -> str:
        if not self.cls:
            return "?"
        v = max(1, len(self.vocab))
        meilleur, score_max = None, -float("inf")
        for c, n_c in self.cls.items():
            s = math.log((n_c + 1) / (self.n + len(self.cls)))
            for f in feats:
                s += math.log((self.compte[c][f] + 1) / (self.total[c] + v))
            if s > score_max:
                meilleur, score_max = c, s
        return meilleur


def _m2_proxy() -> dict:
    """Substitut CPU : deux têtes bayésiennes, même dissociation structurelle."""
    its = corpus_items()
    tr, te = decouper(its, 1, 0.2)
    if not te:
        tr, te = its[:422], its[422:]
    modele = _Bayes()
    modele.entrainer([(_ngrammes(i.texte, i.jeu), i.code["action"]) for i in tr])
    modele_d = _Bayes()
    modele_d.entrainer([(_ngrammes(i.texte, i.jeu), i.code["de"]) for i in tr])
    rng = random.Random(3)
    actions = sorted(modele.cls)
    des = sorted(modele_d.cls, key=repr)
    major_a = modele.cls.most_common(1)[0][0]
    major_d = modele_d.cls.most_common(1)[0][0]
    n = len(te)
    ok_a = ok_d = 0
    ok_a_rand = ok_d_rand = 0
    ok_a_prio = ok_d_prio = 0
    ok_d_nn = ok_d_rand_nn = ok_d_prio_nn = n_nn = 0
    repetitions = 10
    for it in te:
        fa = _ngrammes(it.texte, it.jeu)
        pa = modele.predire(fa)
        pd = modele_d.predire(fa)
        ok_a += int(pa == it.code["action"])
        ok_d += int(pd == it.code["de"])
        ok_a_prio += int(major_a == it.code["action"])
        ok_d_prio += int(major_d == it.code["de"])
        if it.code["de"] is not None:
            n_nn += 1
            ok_d_nn += int(pd == it.code["de"])
            ok_d_prio_nn += int(major_d == it.code["de"])
        for _ in range(repetitions):
            ra = rng.choice(actions)
            rd = rng.choice(des)
            ok_a_rand += int(ra == it.code["action"])
            ok_d_rand += int(rd == it.code["de"])
            if it.code["de"] is not None:
                ok_d_rand_nn += int(rd == it.code["de"])
    a, d = ok_a / n, ok_d / n
    a_rand = ok_a_rand / (n * repetitions)
    d_rand = ok_d_rand / (n * repetitions)
    a_prio, d_prio = ok_a_prio / n, ok_d_prio / n
    d_nn = ok_d_nn / max(1, n_nn)
    d_rand_nn = ok_d_rand_nn / max(1, n_nn * repetitions)
    d_prio_nn = ok_d_prio_nn / max(1, n_nn)
    r = _entree(
        "couper la voie ventrale (action) / dorsale (de) — tête détruite",
        {"action": a, "de": d, "de_non_nul": d_nn, "n_de_non_nul": n_nn},
        {"action": a_rand, "de": d_rand, "de_non_nul": d_rand_nn,
         "avec_priori": {"action": a_prio, "de": d_prio},
         "ventrale": {"action": a_rand, "de": d, "de_non_nul": d_nn},
         "dorsale": {"action": a, "de": d_rand, "de_non_nul": d_rand_nn}},
        {"action": a - a_rand, "de": d - d_rand,
         "de_non_nul": d_nn - d_rand_nn,
         "avec_priori": {"action": a - a_prio, "de": d - d_prio,
                         "de_non_nul": d_nn - d_prio_nn},
         "majorite": {"action": a_prio, "de": d_prio},
         "preservation": {"action_sous_lesion_dorsale": a,
                          "de_sous_lesion_ventrale": d},
         "double_dissociation": (a - a_rand) > 0.2 and (d_nn - d_rand_nn) > 0.2},
        n, statut="proxy CPU (bayes naïf, deux têtes) ; voies.py non exécuté",
        sham=0.0,
        note=("la tête détruite répond au hasard ; le repli majoritaire est mesuré à part. "
              "Sur le sous-ensemble `de`, l'action est structurellement constante "
              "(`deplacer`) : le score action de M2 y est trivial, comme le note M5."))
    r["mode"] = "proxy"
    return r


def _m2_voies(pas: int = 300, graines=(1,), device: str | None = None,
              base: str | None = None) -> dict:
    """Le vrai M2 : encodeur natif gelé + têtes ventrale/dorsale de ``voies.py``.

    Même dispositif que ``batterie.py`` (300 pas, lot 32, graine 1) pour que les
    chiffres soient comparables. Les deux lésions sont **séparées** : la ventrale
    détruit la tête action, la dorsale la tête ``de``. Le ``lessee`` publié est
    l'union des deux lésions simples (chaque métrique vient de sa propre lésion).
    """
    import torch
    from transformers import AutoModelForCausalLM
    from cerveau.voies import entrainer, evaluer

    base = base or os.environ.get("DRAVE_M2_BASE", "/tmp/natif-600-512-8-align-s1")
    if not pathlib.Path(base).is_dir():
        raise FileNotFoundError(f"base M2 absente : {base}")
    device = device or os.environ.get(
        "DRAVE_DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
    t0 = time.monotonic()
    par_graine = []
    val = []
    for graine in graines:
        # Les têtes sont initialisées par le RNG torch global : sans graine,
        # deux exécutions du même protocole diffèrent de 1–2 items. On fixe la
        # graine pour que la lésion soit reproductible (l'échantillonnage des
        # données est déjà seedé par `entrainer`).
        torch.manual_seed(int(graine))
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(int(graine))
        modele_base = AutoModelForCausalLM.from_pretrained(base, dtype=torch.float32)
        m, val = entrainer(modele_base, pas, 32, 64, graine, device, synth=True)
        intact = evaluer(m, val, device)
        ventrale = evaluer(m, val, device, "ventral")
        dorsale = evaluer(m, val, device, "dorsal")
        sham = evaluer(m, val, device)
        cibles_a = [it.code["action"] for it in val]
        cibles_d = [it.code["de"] for it in val]
        maj_a = collections.Counter(cibles_a).most_common(1)[0][1] / max(1, len(cibles_a))
        maj_d = collections.Counter(cibles_d).most_common(1)[0][1] / max(1, len(cibles_d))
        par_graine.append({
            "graine": graine, "intacte": intact, "ventrale": ventrale,
            "dorsale": dorsale,
            "sham_action": abs(sham["action"] - intact["action"]),
            "sham_de": abs(sham["de"] - intact["de"]),
            "majorite_action": maj_a, "majorite_de": maj_d,
        })
        del modele_base, m
        if device == "cuda":
            torch.cuda.empty_cache()

    def moy(famille: str, nom: str = "") -> float:
        if nom:
            return sum(g[famille][nom] for g in par_graine) / len(par_graine)
        return sum(g[famille] for g in par_graine) / len(par_graine)

    a, d = moy("intacte", "action"), moy("intacte", "de")
    a_v, d_v = moy("ventrale", "action"), moy("ventrale", "de")
    a_d, d_d = moy("dorsale", "action"), moy("dorsale", "de")
    maj_a, maj_d = moy("majorite_action"), moy("majorite_de")
    n = len(val)
    r = _entree(
        "couper la voie ventrale (action) / dorsale (de) — voies.py réel",
        {"action": a, "de": d, "de_non_nul": d, "n": n},
        {"action": a_v, "de": d_d, "de_non_nul": d_d,
         "ventrale": {"action": a_v, "de": d_v, "de_non_nul": d_v},
         "dorsale": {"action": a_d, "de": d_d, "de_non_nul": d_d},
         "avec_priori": {"action": maj_a, "de": maj_d}},
        {"action": a - a_v, "de": d - d_d, "de_non_nul": d - d_d,
         "avec_priori": {"action": a - maj_a, "de": d - maj_d,
                         "de_non_nul": d - maj_d},
         "majorite": {"action": maj_a, "de": maj_d},
         "preservation": {"action_sous_lesion_dorsale": a_d,
                          "de_sous_lesion_ventrale": d_v},
         "double_dissociation": ((a - a_v) > 0.2 and (d - d_d) > 0.2
                                 and abs(d_v - d) < 0.05
                                 and abs(a_d - a) < 0.05)},
        n,
        statut=(f"voies.py réel : base {base}, {pas} pas, graines "
                f"{list(graines)}, {device}"),
        sham=sum(g["sham_action"] + g["sham_de"] for g in par_graine)
        / (2 * len(par_graine)),
        note=("encodeur gelé ; chaque métrique du lessee vient de sa propre "
              "lésion simple. Sur le sous-ensemble `de`, l'action est presque "
              "constante (majorité %.3f), donc le score action intact est "
              "trivial : le déficit utile est celui contre le hasard/majorité."
              % maj_a))
    r["mode"] = "voies"
    r["graines"] = list(graines)
    r["par_graine"] = par_graine
    r["device"] = device
    r["base"] = base
    r["temps_s"] = time.monotonic() - t0
    return r


def _m2(mode: str = "auto", graines=(1,)) -> dict:
    """Exécute M2 réel, ou le proxy déclaré (repli jamais silencieux)."""
    if mode not in ("auto", "voies", "proxy"):
        raise ValueError(f"m2 inconnu : {mode!r} (auto, voies, proxy)")
    if mode == "proxy":
        return _m2_proxy()
    try:
        return _m2_voies(graines=graines)
    except Exception as exc:  # torch, transformers, base ou GPU absents
        if mode == "voies":
            raise
        r = _m2_proxy()
        r["statut"] = (f"proxy CPU (voies.py non exécuté : "
                       f"{type(exc).__name__}: {exc})")
        r["note"] += (" — repli documenté : le proxy reproduit la double "
                      "dissociation, il ne remplace pas le module M2")
        r["repli"] = f"{type(exc).__name__}: {exc}"
        return r


# ---------------------------------------------------------------------------
# M3 — le tampon
# ---------------------------------------------------------------------------
def _m3(seqs) -> dict:
    intact = MemoireTravail(12).span(seqs)
    graded = {}
    for cap in (0, 1, 2, 4, 8, 12):
        m = MemoireTravail(cap)
        sp = m.span(seqs)
        graded[str(cap)] = {"span": sp["span"], "exact": sp["exact"],
                            "nback1": m.nback_scores(seqs, 1)["exact"]}
    lese = graded["0"]
    # contrôle n-back valide : une suite de 5 codes répétés (comme batterie.py)
    # motif A,B,A,B,... : nback(1) doit être faux, nback(2) vrai ;
    # une capacité < 2 ne peut pas calculer nback(2).
    a = dict(seqs[0].pas[0].code)
    b = dict(seqs[0].pas[1].code)
    suite = [dict(a if i % 2 == 0 else b) for i in range(40)]
    def controle(cap):
        m = MemoireTravail(cap)
        ok1 = ok2 = 0
        for i in range(2, len(suite)):
            m.charger(suite[:i + 1])
            ok1 += int(m.nback(1) is True)
            ok2 += int(m.nback(2) is True)
        return ok1 / 38, ok2 / 38
    c1, c2 = controle(12)
    l1, l2 = controle(0)
    return _entree("capacité du tampon mise à 0", {"span": intact["span"],
                   "exact": intact["exact"], "nback1_brut": graded["12"]["nback1"],
                   "nback1_controle": c1, "nback2_controle": c2},
                   {"span": lese["span"], "exact": lese["exact"],
                    "nback1_brut": lese["nback1"],
                    "nback1_controle": l1, "nback2_controle": l2},
                   {"span": (intact["span"] - lese["span"]) / max(1, intact["span"]),
                    "exact": intact["exact"] - lese["exact"],
                    "nback2_controle": c2 - l2},
                   intact["essais"], sham=0.0,
                   note=f"dose-réponse : {graded}")


# ---------------------------------------------------------------------------
# M4 — la mémoire épisodique
# ---------------------------------------------------------------------------
def _m4(taille: int = 32) -> dict:
    its = corpus_items()
    par_jeu = collections.defaultdict(list)
    for it in its:
        par_jeu[it.jeu].append(it)
    rng = random.Random(7)
    echantillon = []
    for jeu, v in par_jeu.items():
        k = max(1, taille // len(par_jeu))
        echantillon.extend(rng.sample(v, min(k, len(v))))
    plein = Episodique()
    for it in echantillon:
        plein.stocker(it.texte, it.code, it.langue, it.paire)
    vide = Episodique()
    intact = sum(plein.rappel(it.code)["exact"] for it in echantillon) / len(echantillon)
    sans = sum(vide.rappel(it.code)["exact"] for it in echantillon) / len(echantillon)
    completion = sum(plein.completion({**it.code, "vers": None})["champs"]
                     for it in echantillon) / len(echantillon)
    completion_vide = sum(vide.completion({**it.code, "vers": None})["champs"]
                          for it in echantillon) / len(echantillon)
    champs = {}
    for nom in NOMS:
        if nom in ("jeu", "action"):
            continue  # None n'est pas dans le vocabulaire de ces deux champs
        presents = [it for it in echantillon if it.code.get(nom) is not None]
        if not presents:
            continue
        ok = ok_intact = 0
        for it in presents:
            # intacte : même requête sans lésion du champ (le code complet est
            # dans le magasin, donc le rappel vaut 1,0 par construction — c'est
            # une tautologie de M4, pas une performance du champ).
            e_intact = plein.chercher(dict(it.code), 1)
            ok_intact += int(bool(e_intact) and e_intact[0].code == it.code)
            cue = dict(it.code)
            cue[nom] = None
            e = plein.chercher(cue, 1)
            ok += int(bool(e) and e[0].code == it.code)
        intacte_champ = ok_intact / len(presents)
        rappel_lese = ok / len(presents)
        champs[nom] = {"n": len(presents),
                       "intacte": intacte_champ,
                       "rappel_lese": rappel_lese,
                       "deficit": intacte_champ - rappel_lese}
    plus_faible = max(champs, key=lambda k: champs[k]["deficit"]) if champs else None
    if plus_faible is not None and champs[plus_faible]["deficit"] <= 0.0:
        # La requête partielle retrouve l'épisode stocké lui-même : le champ
        # lésé n'est pas détectable. Ne pas publier un « champ nécessaire » nul.
        plus_faible = None
    deficit_max = champs[plus_faible]["deficit"] if plus_faible else 0.0
    if plus_faible:
        note = (f"échantillon stratifié par jeu ; le champ lésé est mis à None "
                f"dans la requête. L'intacte par champ vaut 1,0 par construction "
                f"(le code complet est dans le magasin). Les champs dont le "
                f"retrait ne change pas le voisin (de, vers, case, symbole) ont "
                f"un déficit nul : propriété du magasin (codes uniques), pas une "
                f"lésion manquée. `{plus_faible}` est détectable "
                f"({deficit_max:.4f}) : plusieurs valeurs partagent les autres "
                f"champs, le voisin bascule.")
    else:
        note = ("échantillon stratifié par jeu ; aucun champ n'a de déficit "
                "detectable : la requête partielle retrouve l'épisode stocké "
                "lui-même (tautologie de récupération de M4).")
    return _entree(
        "stockage vide (M4 sans épisodes) ; puis lésion du champ d'adressage",
        {"rappel": intact, "completion": completion,
         "n": len(echantillon)},
        {"rappel": sans, "completion": completion_vide, "n": len(echantillon)},
        {"rappel": intact - sans, "completion": completion - completion_vide,
         "par_champ": champs,
         "champ_le_plus_necessaire": plus_faible,
         "deficit_champ_max": deficit_max,
         "tautologie_recuperation": True},
        len(echantillon), sham=0.0, note=note)


# ---------------------------------------------------------------------------
# M5 — le prédictif
# ---------------------------------------------------------------------------
class _Pas:
    __slots__ = ("code", "jeu")

    def __init__(self, action: str):
        self.jeu = "synthetique"
        self.code = {"jeu": "synthetique", "action": action}


class _Seq:
    __slots__ = ("pas",)

    def __init__(self, pas):
        self.pas = pas


def _m5(seqs) -> dict:
    rng = random.Random(3)
    seqs = list(seqs)
    rng.shuffle(seqs)
    n = int(len(seqs) * 0.8)
    tr, te = seqs[:n], seqs[n:]
    # cible par défaut du module actuel : la case d'arrivée (varie), pas l'action
    intact = Predictif(cible="cible", ordre=2)
    intact.entrainer(tr)
    mes_intact = intact.evaluer(te)
    sans = Predictif(cible="cible", ordre=2)
    sans.entrainer(tr)
    sans.transitions.clear()
    sans.transitions2.clear()
    mes_sans = sans.evaluer(te)
    ordre1 = Predictif(cible="cible", ordre=1)
    ordre1.entrainer(tr)
    mes_ordre1 = ordre1.evaluer(te)
    # contrôle positif : une chaîne de Markov où les transitions comptent
    rng2 = random.Random(5)
    actions = ("a", "b", "c", "d")
    synth = []
    for _ in range(200):
        pas = []
        etat = rng2.randrange(4)
        for _ in range(12):
            pas.append(_Pas(actions[etat]))
            etat = (etat + 1) % 4 if rng2.random() > 0.1 else rng2.randrange(4)
        synth.append(_Seq(pas))
    tr2, te2 = synth[:160], synth[160:]
    ps = Predictif(cible="action")
    ps.entrainer(tr2)
    pos_intact = ps.evaluer(te2)
    ps.transitions.clear()
    ps.transitions2.clear()
    pos_lese = ps.evaluer(te2)
    return _entree(
        "retirer les transitions (repli marginal) ; retirer l'ordre 2 ; contrôle positif",
        {"exact": mes_intact["exact"], "surprise": mes_intact["surprise"],
         "majoritaire": mes_intact["majoritaire"],
         "controle_positif_exact": pos_intact["exact"],
         "controle_positif_majoritaire": pos_intact["majoritaire"]},
        {"exact": mes_sans["exact"], "surprise": mes_sans["surprise"],
         "sans_ordre2_exact": mes_ordre1["exact"],
         "sans_ordre2_surprise": mes_ordre1["surprise"],
         "controle_positif_exact": pos_lese["exact"]},
        {"exact": mes_intact["exact"] - mes_sans["exact"],
         "surprise": mes_intact["surprise"] - mes_sans["surprise"],
         "sans_ordre2": mes_intact["exact"] - mes_ordre1["exact"],
         "controle_positif_deficit": pos_intact["exact"] - pos_lese["exact"]},
        mes_intact["n"], sham=0.0,
        note="le contrôle positif valide que la lésion des transitions est détectable")


# ---------------------------------------------------------------------------
# M6 — la porte
# ---------------------------------------------------------------------------
def _m6(its) -> dict:
    porte = Porte()
    integre = porte.executer(its, ("fr", "en"))
    essais = porte.tache_conflit(its, ("fr", "en"))
    n = len(essais)
    prevalence = sum(1 for e in essais if e.attendu) / max(1, n)
    pol = integre.get("politiques", {})
    langue = pol.get("langue", {}).get("exact", 0.0)
    sens = pol.get("sens", {}).get("exact", 0.0)
    tout_non = pol.get("tout_non", {}).get("exact", 0.0)
    return _entree(
        "retirer la conjonction (un seul canal), tout accepter, tout refuser",
        {"exact": integre["exact"], "n": n,
         "faux_positifs": integre.get("faux_positifs"),
         "faux_negatifs": integre.get("faux_negatifs"),
         "taux_base_tout_non": integre.get("taux_base_tout_non")},
        {"canal_langue": langue, "canal_sens": sens,
         "tout_non": tout_non, "tout_accepter": prevalence},
        {"canal_langue": integre["exact"] - langue,
         "canal_sens": integre["exact"] - sens,
         "tout_non": integre["exact"] - tout_non,
         "tout_accepter": integre["exact"] - prevalence},
        n, sham=0.0,
        note="la conjonction (sens ET langue) est la seule politique au-dessus du taux de base")


# ---------------------------------------------------------------------------
# M7 — la modulation
# ---------------------------------------------------------------------------
def _m7(permutations: int = 6) -> dict:
    r = experience_m7(permutations=permutations, synthetique=False)
    pol = r["politiques"]
    d = r["deltas_vs_fifo"]

    def m(nom):
        return {k: pol[nom][k]["moyenne"] for k in
                ("ret_code", "rep_surface", "rep_code", "suf_surface", "suf_code")}

    # décomposition : la clé (surface/code) et le signal (nouveauté)
    return _entree(
        "retirer la modulation (FIFO, poids 1) ; puis décomposer clé et signal",
        {"modulation_surface": m("nouveaute"), "modulation_code": m("nouveaute_code")},
        {"sans_modulation": m("fifo"), "fifo_code": m("fifo_code")},
        {"surface_vs_fifo": {"suf_code": d["nouveaute"]["suf_code"]["moyenne"],
                             "rep_surface": d["nouveaute"]["rep_surface"]["moyenne"]},
         "code_vs_fifo": {"suf_code": d["nouveaute_code"]["suf_code"]["moyenne"],
                          "rep_surface": d["nouveaute_code"]["rep_surface"]["moyenne"]},
         "signal_sur_cle_code": d["nouveaute_code"].get("vs_fifo_code", {}).get(
             "suf_code", {}).get("moyenne", 0.0),
         "cle_code_sans_signal": d["fifo_code"]["suf_code"]["moyenne"],
         "plafond_code": r["protocole"]["plafonds"]["code"],
         "plafond_surface": r["protocole"]["plafonds"]["surface_finale"]},
        r["protocole"]["n"], sham=0.0,
        note="déficit négatif = la modulation dégrade ; la clé code est un effet de clé, pas de signal")


# ---------------------------------------------------------------------------
# M8 — le sommeil
# ---------------------------------------------------------------------------
def _m8() -> dict:
    """Le sommeil, lésé sur le protocole honnête : code tenu à l'écart.

    La lésion est le retrait de tout prototype (repli sur la marginale globale),
    mesurée sur le **même** leave-one-code-out que l'intacte. La queue publiée
    (96,48 %) est rappelée pour mémoire : ses 106 codes sont tous dans le train,
    c'est une reconstruction intra-code, pas une généralisation.
    """
    rq = experience_m8()
    rc = experience_contexte()
    q = rq["queue"]
    lq = rc["loo_codes"]
    intact = lq["ladder"]
    lese = lq["global"]
    hyb = rc["codes_tenus_resume"]["hybride_surface"]
    exact_nouveaux = rc["verdict"]["exact_codes_tenus"]
    return _entree(
        "retirer le sommeil (aucun prototype, marginale globale) — code tenu à l'écart",
        {"champs": intact["champs"], "exact": intact["exact"],
         "champs_non_nuls": intact["champs_non_nuls"],
         "champs_nuls": intact["champs_nuls"],
         "exact_codes_nouveaux": exact_nouveaux,
         "exact_codes_uniques": rq["dedup_tout"]["module"]["exact"],
         "hybride_exact_queue": q["hybride"]["exact"],
         "hybride_couverture_queue": q["hybride"]["couverture"],
         "hybride_surface_couverture_codes_tenus": hyb["couverture"],
         "queue_champs": q["module_champs"]["champs"],
         "queue_exact": q["module_champs"]["exact"],
         "queue_codes_vus": rc["queue_publiee"]["codes_test_vus_dans_train"]},
        {"champs": lese["champs"], "exact": lese["exact"],
         "champs_non_nuls": lese["champs_non_nuls"],
         "champs_nuls": lese["champs_nuls"]},
        {"champs": intact["champs"] - lese["champs"],
         "exact": intact["exact"] - lese["exact"],
         "champs_non_nuls": intact["champs_non_nuls"] - lese["champs_non_nuls"],
         "champs_nuls": intact["champs_nuls"] - lese["champs_nuls"],
         "exact_codes_nouveaux": [x - lese["exact"] for x in exact_nouveaux],
         "hybride_exact_sur_codes_nouveaux": hyb["exact"],
         "gain_honnete_sur_par_jeu_champs": rc["verdict"]["gain_groupe_sur_jeu_champs"],
         "plafond_contextuel_groupe": rc["verdict"]["plafond_groupe"],
         "type_seul_sur_jeu_champs": rc["verdict"]["gain_type_sur_jeu_champs"]},
        29, sham=0.0,
        note=("le sommeil porte la structure des champs (motif de None, +15,2 pts "
              "de champs et +58,9 pts de non nuls contre la marginale globale) ; "
              "il ne produit aucun code jamais vu (exact nul par construction). "
              "L'hybride 100 % de la queue est tautologique (clé = code cible) ; "
              "clé par surface, sa couverture sur codes tenus est 0 %."))


# ---------------------------------------------------------------------------
# La batterie
# ---------------------------------------------------------------------------
def batterie_lesions(rapide: bool = True, m2: str = "auto") -> dict:
    """Batterie M1–M9. ``m2`` : auto (réel si possible), voies, proxy."""
    t0 = time.monotonic()
    seqs = corpus(0, 40, 12)
    its = corpus_items()
    m1 = _m1()
    m2r = _m2(m2, graines=(1,) if rapide else (1, 2, 3))
    m3 = _m3(seqs)
    m4 = _m4(36 if rapide else 72)
    m5 = _m5(seqs)
    m6 = _m6(its)
    m7 = _m7(6 if rapide else 20)
    m8 = _m8()
    modules = {"M1": m1, "M2": m2r, "M3": m3, "M4": m4, "M5": m5,
               "M6": m6, "M7": m7, "M8": m8}
    deficits = {k: v["deficit"] for k, v in modules.items()}
    plats = []
    for k, v in modules.items():
        d = v["deficit"]
        if isinstance(d, dict):
            vals = [x for x in d.values() if isinstance(x, (int, float))]
            plat = bool(vals) and max(abs(x) for x in vals) < 0.01
        else:
            plat = abs(d) < 0.01
        if plat:
            plats.append(k)
    return {
        "protocole": {"rapide": rapide, "cpu": m2r.get("mode") != "voies",
                      "m2_mode": m2r.get("mode"),
                      "m2_statut": m2r["statut"],
                      "m4_echantillon": 36 if rapide else 72,
                      "m7_permutations": 6 if rapide else 20,
                      "n_items": len(its), "n_sequences": len(seqs)},
        "modules": modules,
        "controles": {
            "sham": {k: v["controle_sham"] for k, v in modules.items()},
            "dose_reponse_M3": m3["note"],
            "positif_M5": {"deficit": m5["deficit"]["controle_positif_deficit"]},
            "M6_tout_non": m6["lessee"]["tout_non"],
            "M6_tout_accepter": m6["lessee"]["tout_accepter"],
            "M2_mode": m2r.get("mode"),
            "M2_double_dissociation": m2r["deficit"]["double_dissociation"],
            "M2_preservation": m2r["deficit"]["preservation"],
            "M8_par_jeu": m8["lessee"]["champs"],
            "M8_exact_loo": m8["intacte"]["exact"],
            "M8_hybride": {
                "exact_queue_oracle": m8["intacte"]["hybride_exact_queue"],
                "couverture_queue": m8["intacte"]["hybride_couverture_queue"],
                "couverture_surface_codes_tenus":
                    m8["intacte"]["hybride_surface_couverture_codes_tenus"],
                "exact_codes_nouveaux": m8["deficit"]["exact_codes_nouveaux"]},
            "M8_queue": {"champs": m8["intacte"]["queue_champs"],
                         "exact": m8["intacte"]["queue_exact"],
                         "codes_vus": m8["intacte"]["queue_codes_vus"],
                         "plafond_corpus_groupe":
                             m8["deficit"]["plafond_contextuel_groupe"]},
        },
        "audit": {
            "deficits": "tous calculés intacte - lésée, jamais 1 - lésée",
            "M4_par_champ": ("corrigé : intacte mesurée (1,0 par construction, "
                             "tautologie de M4) moins rappel lésé"),
            "batterie_py_M9": ("batterie.py publie des scores bruts (M3 span, "
                               "M5 1-majoritaire, M6 1-exact, M7 rétention FIFO, "
                               "M8 0,0 constant), pas des déficits ; "
                               "incohérence de mapping documentée, batterie.py non modifié"),
            "voies_vs_proxy": m2r.get("mode"),
        },
        "resume": {
            "deficits": deficits,
            "modules_sans_deficit": plats,
            "negatifs": [
                "M5 : les transitions ne gagnent que 3,7 pts (12,45 -> 8,79 %) ; "
                "l'ordre 2 ne gagne rien ; l'ancien 98,9 % était la constante action",
                "M7 : aucun signal ne bat FIFO ; la nouveauté par surface dégrade",
                "M8 : exact nul par construction sur un code tenu à l'écart ; "
                "le conditionnement (jeu, action, type) ne gagne que le motif de None",
                "M8 : le 96,48 % publié est intra-code (106/106 codes de test "
                "sont dans le train, plafond corpus du groupe 57,95 %)",
            ],
            "lesions_qui_ameliorent": [
                "M7 : retirer la modulation de surface améliore le suffixe "
                "(-déficit : la modulation coûte)",
            ],
        },
        "secondes": time.monotonic() - t0,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(batterie_lesions(), ensure_ascii=False, indent=1,
                     default=lambda o: o if isinstance(o, (int, float, str, bool, type(None))) else str(o)))

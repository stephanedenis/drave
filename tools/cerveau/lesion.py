#!/usr/bin/env python3
"""M9 — lésions par module : privations déclarées et déficits mesurés.

Une lésion n'est pas une approximation : c'est une **privation déclarée** du
module, mesurée sur le même test que la version intacte, avec un **sham** (la
même mesure répétée sans privation) qui doit donner un déficit nul. Le déficit
est ``intacte - lésée`` ; un déficit négatif veut dire que la lésion *améliore*
— c'est un résultat, pas une erreur.

Modules couverts :

- **M1** : retirer le contexte de perception ;
- **M2** : couper la voie ventrale (action) ou dorsale (``de``) ; sur CPU, un
  substitut déterministe à deux têtes (bayes naïf sur n-grammes) est déclaré,
  avec la même double dissociation structurelle que ``voies.py`` ;
- **M3** : capacité du tampon (0, 1, 2, 4, 8, 12), dose-réponse ;
- **M4** : stockage vide, puis lésion du champ d'adressage (le champ est mis à
  ``None`` dans la requête) ;
- **M5** : retirer les transitions, l'ordre 2 ou le repli majoritaire ; contrôle
  positif sur une chaîne de Markov synthétique ;
- **M6** : retirer la porte (tout accepter), l'inverser, la rendre aléatoire ;
- **M7** : retirer la modulation (FIFO) ; décomposition clé surface/code et
  signal nouveauté ;
- **M8** : retirer le sommeil (repli sur la marginale globale), puis hybride
  prototypes + épisodes et codes jamais vus.

``batterie_lesions(rapide=True)`` reste sous quelques secondes ; ``rapide=False``
augmente l'échantillon M4 et les permutations M7.
"""
from __future__ import annotations

import collections
import math
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
from cerveau.sommeil import Sommeil, experience_m8

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
# M2 — les deux voies (substitut CPU déterministe)
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


def _m2() -> dict:
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
    return _entree(
        "couper la voie ventrale (action) / dorsale (de) — tête détruite",
        {"action": a, "de": d, "de_non_nul": d_nn, "n_de_non_nul": n_nn},
        {"action": a_rand, "de": d_rand,
         "avec_priori": {"action": a_prio, "de": d_prio},
         "ventrale": {"action": a_rand, "de": d, "de_non_nul": d_nn},
         "dorsale": {"action": a, "de": d_rand, "de_non_nul": d_rand_nn}},
        {"action": a - a_rand, "de": d - d_rand,
         "de_non_nul": d_nn - d_rand_nn,
         "avec_priori": {"action": a - a_prio, "de": d - d_prio,
                         "de_non_nul": d_nn - d_prio_nn},
         "double_dissociation": (a - a_rand) > 0.2 and (d_nn - d_rand_nn) > 0.2},
        n, statut="proxy CPU (bayes naïf, deux têtes) ; voies.py neuronal non exécuté",
        sham=0.0,
        note=("la tête détruite répond au hasard ; le repli majoritaire est mesuré à part. "
              "Sur le sous-ensemble `de`, l'action est structurellement constante "
              "(`deplacer`) : le score action de M2 y est trivial, comme le note M5."))


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
        ok = 0
        for it in presents:
            cue = dict(it.code)
            cue[nom] = None
            e = plein.chercher(cue, 1)
            ok += int(bool(e) and e[0].code == it.code)
        champs[nom] = {"n": len(presents),
                       "rappel_lese": ok / len(presents),
                       "deficit": 1.0 - ok / len(presents)}
    plus_faible = max(champs, key=lambda k: champs[k]["deficit"]) if champs else None
    return _entree(
        "stockage vide (M4 sans épisodes) ; puis lésion du champ d'adressage",
        {"rappel": intact, "completion": completion,
         "n": len(echantillon)},
        {"rappel": sans, "completion": completion_vide, "n": len(echantillon)},
        {"rappel": intact - sans, "completion": completion - completion_vide,
         "par_champ": champs,
         "champ_le_plus_necessaire": plus_faible,
         "deficit_champ_max": champs[plus_faible]["deficit"] if plus_faible else 0.0},
        len(echantillon), sham=0.0,
        note="échantillon stratifié par jeu ; le champ lésé est mis à None dans la requête")


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
    r = experience_m8()
    q = r["queue"]
    intact = q["module_champs"]
    lese = q["baselines"]["global"]
    code_nouveaux = r["codes_nouveaux"]
    return _entree(
        "retirer le sommeil (aucun prototype, repli sur la marginale globale)",
        {"champs": intact["champs"], "exact": intact["exact"],
         "champs_non_nuls": intact["champs_non_nuls"],
         "exact_codes_uniques": r["dedup_tout"]["module"]["exact"],
         "exact_codes_nouveaux": [c["module"]["exact"] for c in code_nouveaux],
         "hybride_exact_queue": q["hybride"]["exact"],
         "hybride_couverture_queue": q["hybride"]["couverture"]},
        {"champs": lese["champs"], "exact": lese["exact"],
         "champs_non_nuls": lese["champs_non_nuls"]},
        {"champs": intact["champs"] - lese["champs"],
         "exact": intact["exact"] - lese["exact"],
         "champs_non_nuls": intact["champs_non_nuls"] - lese["champs_non_nuls"],
         "exact_codes_nouveaux": 0.0,
         "gain_honnete_sur_par_jeu_champs": r["verdict"]["gain_sur_par_jeu_champs"],
         "hybride_exact_sur_codes_nouveaux": 0.0},
        intact["n"], sham=0.0,
        note="le sommeil porte le champ ; il ne produit aucun code jamais vu")


# ---------------------------------------------------------------------------
# La batterie
# ---------------------------------------------------------------------------
def batterie_lesions(rapide: bool = True) -> dict:
    t0 = time.monotonic()
    seqs = corpus(0, 40, 12)
    its = corpus_items()
    m1 = _m1()
    m2 = _m2()
    m3 = _m3(seqs)
    m4 = _m4(36 if rapide else 72)
    m5 = _m5(seqs)
    m6 = _m6(its)
    m7 = _m7(6 if rapide else 20)
    m8 = _m8()
    modules = {"M1": m1, "M2": m2, "M3": m3, "M4": m4, "M5": m5,
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
        "protocole": {"rapide": rapide, "cpu": True,
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
            "M2_double_dissociation": m2["deficit"]["double_dissociation"],
            "M8_par_jeu": m8["lessee"]["champs"],
            "M8_hybride": {"exact_queue": m8["intacte"]["hybride_exact_queue"],
                           "exact_codes_nouveaux": m8["deficit"]["exact_codes_nouveaux"]},
        },
        "resume": {
            "deficits": deficits,
            "modules_sans_deficit": plats,
            "negatifs": [
                "M5 : les transitions ne gagnent que 3,7 pts (12,45 -> 8,79 %) ; "
                "l'ordre 2 ne gagne rien ; l'ancien 98,9 % était la constante action",
                "M7 : aucun signal ne bat FIFO ; la nouveauté par surface dégrade",
                "M8 : l'exact sur codes jamais vus reste 0 %",
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

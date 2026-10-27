#!/usr/bin/env python3
"""M7 — neuromodulation : nouveauté, incertitude, récompense, rétention bornée.

Le module ne change pas le code : il change le **poids d'écriture** dans une
mémoire épisodique bornée. La question mesurable n'est pas « le poids bouge-t-il ? »
(oui, par construction) mais « la politique de rétention qui en résulte retient-elle
mieux ce qui sera redemandé ? ».

Trois corrections de banc, mesurées ici :

1. **Plafond de la métrique historique.** La batterie comptait la rétention des
   surfaces nouvelles : 16 places / 439 surfaces = **3,64 %**. C'est le plafond
   de *toute* mémoire à 16 places qui garde des surfaces distinctes. La métrique
   ne peut donc pas distinguer deux politiques : 3,64 % n'est pas un résultat,
   c'est la capacité divisée par le vocabulaire.
2. **Le comparateur n'était pas FIFO.** `MemoireLimitee.stocker` triait par poids
   et tronquait ; à poids égaux le tri est stable, donc la mémoire gardait les
   16 **premiers** arrivés (« gel »), pas les 16 derniers. `politique="gel"`
   reproduit l'ancien banc ; `politique="fifo"` est le vrai FIFO.
3. **La nouveauté binaire sature.** Les 16 premiers items nouveaux ont tous le
   même poids maximal ; aucun item suivant ne peut les évincer par ce signal.
   Une politique « nouveauté » est donc une politique de gel, pas une politique
   adaptative.

L'expérience `experience_m7` compare, sur le même flux et à capacité égale
(contrôle apparié, permutations), le FIFO, le LRU, le LFU, la nouveauté par
surface et par code, l'incertitude (1 − confiance du codec), une récompense
déclarée (gain matériel : `prendre`/`promouvoir`), une combinaison, un hasard
et des oracles. Elle mesure la rétention des nouveaux (surface et code), des
répétés, et le rappel hors échantillon (suffixe). Le contrôle positif est un
flux de Zipf où le LFU et une récompense informative doivent battre le FIFO :
si l'appareil ne les voit pas, il ne peut pas conclure au négatif.
"""
from __future__ import annotations

import collections
import dataclasses
import datetime
import math
import random
import statistics

from semantique.universaux import CHAMPS

POLITIQUES = ("fifo", "lru", "lfu", "gel", "nouveaute", "incertitude",
              "recompense", "combine", "hasard")
CLEFS = ("surface", "code")
SIGNAUX = ("nouveaute", "incertitude", "recompense")


class Neuromodulation:
    nom = "M7-neuromodulation"

    def __init__(self, alpha: float = 0.5, beta: float = 0.5,
                 gamma: float = 0.2) -> None:
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.vus = set()
        self.vus_surface = set()

    def signal(self, code: dict, marge: float = 1.0,
               recompense: float = 0.0) -> dict:
        cle = tuple(code.get(n) for n, _ in CHAMPS)
        nouveau = cle not in self.vus
        self.vus.add(cle)
        nouveaute = 1.0 if nouveau else 0.0
        incertitude = max(0.0, min(1.0, 1.0 - marge))
        poids = 1.0 + self.alpha * nouveaute + self.beta * incertitude \
            + self.gamma * recompense
        return {"nouveaute": nouveaute, "incertitude": incertitude,
                "recompense": float(recompense), "poids": poids}

    def signal_surface(self, surface: str) -> dict:
        nouveau = surface not in self.vus_surface
        self.vus_surface.add(surface)
        return {"nouveaute": 1.0 if nouveau else 0.0,
                "poids": 1.0 + self.alpha * (1.0 if nouveau else 0.0)}

    def signaux(self, surface: str, code: dict, marge: float = 1.0,
                recompense: float = 0.0) -> dict:
        """Les trois signaux et le poids, sans double comptage des ensembles vus."""
        cle = tuple(code.get(n) for n, _ in CHAMPS)
        nouveau_code = cle not in self.vus
        nouveau_surface = surface not in self.vus_surface
        self.vus.add(cle)
        self.vus_surface.add(surface)
        nouveaute = 1.0 if (nouveau_code or nouveau_surface) else 0.0
        incertitude = max(0.0, min(1.0, 1.0 - marge))
        poids = 1.0 + self.alpha * nouveaute + self.beta * incertitude \
            + self.gamma * recompense
        return {"nouveaute": nouveaute, "incertitude": incertitude,
                "recompense": float(recompense), "poids": poids}


class MemoireLimitee:
    """Une mémoire épisodique bornée, avec une politique de rétention explicite.

    Chaque entrée est un épisode (surface, code). La clé peut être la surface ou
    le code typé ; dans les deux cas une entrée par clé (pas de doublon).

    Politiques :

    - ``fifo`` : évince le plus ancien **arrivé** (pas de rafraîchissement sur
      lecture) ;
    - ``lru`` : évince le moins récemment **écrit** ;
    - ``lfu`` : évince le moins **fréquent** ;
    - ``gel`` : garde les ``capacite`` premiers arrivés, ignore les suivants —
      c'est le comportement historique de ``stocker`` (tri stable par poids) ;
    - ``nouveaute`` : score 1 si la clé n'a jamais été vue, 0 sinon ; évince le
      score le plus bas (à égalité, le plus ancien). Comme le score d'un item
      déjà vu ne remonte pas, la politique se fige après les premières places ;
    - ``incertitude`` / ``recompense`` : score = poids fourni (1 − confiance, ou
      récompense déclarée), max au fil des écritures ;
    - ``combine`` : ``1 + 0.5*nouveaute + 0.5*incertitude + 0.2*recompense
      + log1p(frequence)`` ; ``sans`` retire des signaux (ablation) ;
    - ``hasard`` : priorité aléatoire fixée à la première écriture.

    Le poids d'une entrée est son score de rétention, pas une probabilité.
    """

    nom = "M7-memoire-limitee"

    def __init__(self, capacite: int = 64, politique: str = "fifo",
                 cle: str = "surface", graine: int = 0,
                 sans: tuple[str, ...] = ()) -> None:
        if politique not in POLITIQUES:
            raise ValueError(f"politique inconnue : {politique}")
        if cle not in CLEFS:
            raise ValueError(f"clé inconnue : {cle}")
        self.capacite = max(0, int(capacite))
        self.politique = politique
        self.cle = cle
        self.sans = tuple(sans)
        self._slots: dict[tuple, dict] = {}
        self._vus: set = set()
        self._t = 0
        self._rng = random.Random(graine)

    # ---- compatibilité avec l'ancien banc --------------------------------
    @property
    def episodes(self) -> list[tuple[str, dict, float]]:
        entrees = sorted(self._slots.values(), key=lambda e: e["t"])
        return [(e["surface"], dict(e["code"]), float(e["poids"])) for e in entrees]

    def contient(self, surface: str) -> bool:
        return any(e["surface"] == surface for e in self._slots.values())

    def contient_code(self, code: dict) -> bool:
        return any(e["code"] == code for e in self._slots.values())

    def rappel(self, code: dict) -> bool:
        return self.contient_code(code)

    def codes(self) -> list[dict]:
        return [dict(e["code"]) for e in self._slots.values()]

    def etat(self) -> list[dict]:
        return [{"surface": e["surface"], "code": dict(e["code"]),
                 "poids": float(e["poids"]), "t": e["t"], "frequence": e["n"]}
                for e in sorted(self._slots.values(), key=lambda e: e["t"])]

    # ---- écriture --------------------------------------------------------
    def _cle(self, surface: str, code: dict) -> tuple:
        if self.cle == "code":
            return tuple(sorted(code.items()))
        return ("surface", surface)

    def _score(self, nouveau: bool, frequence: int, poids: float,
               signaux: dict | None) -> float:
        if self.politique == "nouveaute":
            return 1.0 if nouveau else 0.0
        if self.politique in ("incertitude", "recompense"):
            return float(poids)
        if self.politique == "hasard":
            return self._rng.random()
        if self.politique == "combine":
            sig = signaux or {}
            nou = 0.0 if "nouveaute" in self.sans else (1.0 if nouveau else 0.0)
            inc = 0.0 if "incertitude" in self.sans else float(sig.get("incertitude", 0.0))
            rec = 0.0 if "recompense" in self.sans else float(sig.get("recompense", 0.0))
            return 1.0 + 0.5 * nou + 0.5 * inc + 0.2 * rec + math.log1p(frequence)
        if self.politique == "lfu":
            return float(frequence)
        return 0.0

    def stocker(self, surface: str, code: dict, poids: float = 1.0,
                signaux: dict | None = None) -> None:
        if self.capacite <= 0:
            return
        cle = self._cle(surface, code)
        nouveau = cle not in self._vus
        self._vus.add(cle)
        self._t += 1
        existant = self._slots.get(cle)
        frequence = (existant["n"] + 1) if existant else 1
        score = self._score(nouveau, frequence, poids, signaux)
        if existant is not None:
            existant.update(surface=surface, code=dict(code), poids=float(poids),
                            n=frequence)
            if self.politique in ("incertitude", "recompense", "combine"):
                # un renforcement tardif ne peut pas effacer une trace forte
                existant["score"] = max(float(existant["score"]), float(score))
            elif self.politique in ("fifo", "gel", "nouveaute"):
                pass  # pas de rafraîchissement : la date d'arrivée compte
            elif self.politique == "hasard":
                pass  # priorité tirée une fois
            else:
                existant["score"] = float(score)
                existant["t"] = self._t
            return
        if self.politique == "gel" and len(self._slots) >= self.capacite:
            return
        if len(self._slots) >= self.capacite:
            self._evincer()
        self._slots[cle] = {"surface": surface, "code": dict(code),
                            "poids": float(poids), "n": frequence,
                            "score": float(score), "t": self._t}

    def _evincer(self) -> None:
        if not self._slots:
            return
        if self.politique in ("fifo", "gel"):
            cle = min(self._slots, key=lambda k: self._slots[k]["t"])
        else:
            cle = min(self._slots,
                      key=lambda k: (self._slots[k]["score"],
                                     self._slots[k]["t"], k))
        del self._slots[cle]


# ---------------------------------------------------------------------------
# L'expérience appariée
# ---------------------------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class EpisodeM7:
    surface: str
    code: dict
    jeu: str
    incertitude: float
    recompense: float

    @property
    def cle_code(self) -> tuple:
        return tuple(sorted(self.code.items()))


def preparer_flux(items_=None) -> list[EpisodeM7]:
    """Les épisodes du corpus, avec les signaux disponibles *au moment de l'écriture*.

    - incertitude : ``1 - confiance`` de la lecture du codec (pas d'étiquette) ;
    - récompense : proxy déclaré de gain matériel (``prendre``/``promouvoir``),
      le corpus n'ayant pas de récompense externe.
    """
    from jeux.codecs import codec
    from semantique.typed_corpus import items as corpus_items

    its = list(items_) if items_ is not None else corpus_items()
    out = []
    for it in its:
        try:
            lec = codec(it.jeu).lit(it.texte, niveau=4)
            confiance = float(lec.confiance) if lec is not None else 0.0
        except Exception:
            confiance = 0.0
        out.append(EpisodeM7(it.texte, dict(it.code), it.jeu,
                             max(0.0, min(1.0, 1.0 - confiance)),
                             1.0 if it.code.get("action") in ("prendre", "promouvoir") else 0.0))
    return out


def _poids_politique(ep: EpisodeM7, politique: str) -> float:
    if politique == "incertitude":
        return ep.incertitude
    if politique == "recompense":
        return ep.recompense
    return 1.0


def _tourner(episodes: list[EpisodeM7], ordre: list[int], prefixe: int,
             politique: str, capacite: int, cle: str, graine: int,
             sans: tuple[str, ...] = ()) -> dict:
    memoire = MemoireLimitee(capacite, politique=politique, cle=cle,
                             graine=graine, sans=sans)
    surfaces_vues: set[str] = set()
    codes_vus: set[tuple] = set()
    rep_s = rep_s_n = rep_c = rep_c_n = 0
    for i in ordre[:prefixe]:
        ep = episodes[i]
        nouveau_s = ep.surface not in surfaces_vues
        nouveau_c = ep.cle_code not in codes_vus
        surfaces_vues.add(ep.surface)
        codes_vus.add(ep.cle_code)
        if not nouveau_s:
            rep_s_n += 1
            rep_s += int(memoire.contient(ep.surface))
        if not nouveau_c:
            rep_c_n += 1
            rep_c += int(memoire.contient_code(ep.code))
        memoire.stocker(ep.surface, ep.code, poids=_poids_politique(ep, politique),
                        signaux={"incertitude": ep.incertitude,
                                 "recompense": ep.recompense})
    surfaces_memoire = {e["surface"] for e in memoire.etat()}
    codes_memoire = {tuple(sorted(e["code"].items())) for e in memoire.etat()}
    suffixe = ordre[prefixe:]
    suf_s = sum(1 for i in suffixe if episodes[i].surface in surfaces_memoire)
    suf_c = sum(1 for i in suffixe if episodes[i].cle_code in codes_memoire)
    return {
        "slots": len(memoire.etat()),
        "ret_surface_prefixe": len(surfaces_memoire) / max(1, len(surfaces_vues)),
        "ret_surface_finale": len(surfaces_memoire) / max(1, len({e.surface for e in episodes})),
        "ret_code": len(codes_memoire) / max(1, len(codes_vus)),
        "rep_surface": rep_s / max(1, rep_s_n),
        "rep_code": rep_c / max(1, rep_c_n),
        "rep_n": rep_s_n,
        "suf_surface": suf_s / max(1, len(suffixe)),
        "suf_code": suf_c / max(1, len(suffixe)),
        "codes_memoire": len(codes_memoire),
    }


def _oracle(episodes: list[EpisodeM7], ordre: list[int], prefixe: int,
            capacite: int) -> dict:
    suffixe = ordre[prefixe:]
    cs = collections.Counter(episodes[i].surface for i in suffixe)
    cc = collections.Counter(episodes[i].cle_code for i in suffixe)
    n = max(1, len(suffixe))
    return {"suf_surface": sum(v for _, v in cs.most_common(capacite)) / n,
            "suf_code": sum(v for _, v in cc.most_common(capacite)) / n}


def _stats(valeurs: list[float]) -> dict:
    if not valeurs:
        return {"moyenne": 0.0, "ecart_type": 0.0, "n": 0}
    return {"moyenne": statistics.fmean(valeurs),
            "ecart_type": statistics.stdev(valeurs) if len(valeurs) > 1 else 0.0,
            "min": min(valeurs), "max": max(valeurs), "n": len(valeurs)}


def _delta(apparie: list[float], temoin: list[float]) -> dict:
    d = [a - b for a, b in zip(apparie, temoin)]
    if not d:
        return {"moyenne": 0.0, "ecart_type": 0.0, "n": 0, "gains": 0,
                "ic95": [0.0, 0.0]}
    mu = statistics.fmean(d)
    sd = statistics.stdev(d) if len(d) > 1 else 0.0
    demi = 1.96 * sd / math.sqrt(len(d))
    return {"moyenne": mu, "ecart_type": sd, "n": len(d),
            "gains": sum(1 for x in d if x > 0),
            "ic95": [mu - demi, mu + demi]}


def _configurations() -> list[dict]:
    return [
        {"nom": "fifo", "politique": "fifo", "cle": "surface", "sans": ()},
        {"nom": "lru", "politique": "lru", "cle": "surface", "sans": ()},
        {"nom": "lfu", "politique": "lfu", "cle": "surface", "sans": ()},
        {"nom": "gel", "politique": "gel", "cle": "surface", "sans": ()},
        {"nom": "nouveaute", "politique": "nouveaute", "cle": "surface", "sans": ()},
        {"nom": "incertitude", "politique": "incertitude", "cle": "surface", "sans": ()},
        {"nom": "recompense", "politique": "recompense", "cle": "surface", "sans": ()},
        {"nom": "combine", "politique": "combine", "cle": "surface", "sans": ()},
        {"nom": "combine_sans_nouveaute", "politique": "combine", "cle": "surface",
         "sans": ("nouveaute",)},
        {"nom": "combine_sans_incertitude", "politique": "combine", "cle": "surface",
         "sans": ("incertitude",)},
        {"nom": "combine_sans_recompense", "politique": "combine", "cle": "surface",
         "sans": ("recompense",)},
        {"nom": "combine_sans_tout", "politique": "combine", "cle": "surface",
         "sans": ("nouveaute", "incertitude", "recompense")},
        {"nom": "fifo_code", "politique": "fifo", "cle": "code", "sans": ()},
        {"nom": "nouveaute_code", "politique": "nouveaute", "cle": "code", "sans": ()},
        {"nom": "lfu_code", "politique": "lfu", "cle": "code", "sans": ()},
        {"nom": "hasard", "politique": "hasard", "cle": "surface", "sans": ()},
    ]


_METRIQUES = ("ret_surface_prefixe", "ret_surface_finale", "ret_code",
              "rep_surface", "rep_code", "suf_surface", "suf_code",
              "codes_memoire")


def experience_m7(episodes: list[EpisodeM7] | None = None,
                  permutations: int = 30, capacite: int = 16,
                  graine: int = 0, synthetique: bool = True) -> dict:
    """Compare les politiques de rétention sur le même flux, appariées.

    Le suffixe est le dernier 20 % du flux ; la mémoire est gelée à la fin du
    préfixe. Les deltas sont ``politique - fifo`` par permutation (même ordre,
    même capacité), avec le taux de gains et un IC 95 % normal.
    """
    ep = episodes if episodes is not None else preparer_flux()
    n = len(ep)
    prefixe = int(n * 0.8)
    configs = _configurations()
    resultats: dict[str, dict[str, list[float]]] = {
        c["nom"]: collections.defaultdict(list) for c in configs}
    oracle = collections.defaultdict(list)
    for k in range(permutations):
        ordre = list(range(n))
        random.Random(graine + k).shuffle(ordre)
        for c in configs:
            m = _tourner(ep, ordre, prefixe, c["politique"], capacite,
                         c["cle"], graine + k, c["sans"])
            for nom in _METRIQUES:
                resultats[c["nom"]][nom].append(m[nom])
        o = _oracle(ep, ordre, prefixe, capacite)
        oracle["suf_surface"].append(o["suf_surface"])
        oracle["suf_code"].append(o["suf_code"])
    moyennes = {nom: {m: _stats(v) for m, v in vals.items()}
                for nom, vals in resultats.items()}
    deltas = {}
    for c in configs:
        nom = c["nom"]
        if nom == "fifo":
            continue
        d = {}
        for m in _METRIQUES:
            d[m] = _delta(resultats[nom][m], resultats["fifo"][m])
        if nom.endswith("_code"):
            d["vs_fifo_code"] = {m: _delta(resultats[nom][m], resultats["fifo_code"][m])
                                 for m in _METRIQUES}
        deltas[nom] = d
    # contrôle nul : le FIFO contre lui-même, et le FIFO sur deux flux disjoints
    moitie = max(1, permutations // 2)
    bruit = {m: _delta(resultats["fifo"][m][:moitie],
                       resultats["fifo"][m][moitie:moitie * 2])
             for m in _METRIQUES}
    resultat = {
        "protocole": {
            "n": n, "prefixe": prefixe, "suffixe": n - prefixe,
            "capacite": capacite, "permutations": permutations, "graine": graine,
            "metriques": {
                "ret_surface_prefixe": "surfaces retenues / surfaces distinctes vues au préfixe",
                "ret_surface_finale": "surfaces retenues / surfaces distinctes du flux (dénominateur historique, plafonné)",
                "ret_code": "codes retenus / codes distincts vus au préfixe",
                "rep_surface": "écritures répétées dont la surface était déjà en mémoire",
                "rep_code": "écritures répétées dont le code était déjà en mémoire",
                "suf_surface": "queries du suffixe dont la surface est en mémoire (mémoire gelée)",
                "suf_code": "queries du suffixe dont le code est en mémoire (mémoire gelée)",
            },
            "plafonds": {
                "surface_finale": capacite / max(1, len({e.surface for e in ep})),
                "code": capacite / max(1, len({e.cle_code for e in ep})),
                "surface_prefixe": capacite / max(1, int(n * 0.8)),
            },
        },
        "politiques": moyennes,
        "deltas_vs_fifo": deltas,
        "oracle_suffixe": {m: _stats(v) for m, v in oracle.items()},
        "controles": {
            "fifo_contre_lui_meme": {m: {"moyenne": 0.0, "n": permutations}
                                     for m in _METRIQUES},
            "fifo_flux_disjoints": bruit,
            "hasard_vs_fifo": deltas["hasard"],
        },
    }
    if synthetique:
        resultat["controle_synthetique"] = controle_synthetique(
            ep, permutations=max(8, permutations // 2), graine=graine + 1000)
    # verdicts calculés, pas déclarés
    signaux = ("nouveaute", "incertitude", "recompense", "combine")
    bat_suffixe = [nom for nom in signaux
                   if deltas[nom]["suf_code"]["moyenne"] > 0
                   and deltas[nom]["suf_code"]["gains"] >= 0.8 * permutations]
    bat_repetes = [nom for nom in signaux
                   if deltas[nom]["rep_surface"]["moyenne"] > 0
                   and deltas[nom]["rep_surface"]["gains"] >= 0.8 * permutations]
    meilleur_suf = max(moyennes, key=lambda k: moyennes[k]["suf_code"]["moyenne"])
    meilleur_rep = max(moyennes, key=lambda k: moyennes[k]["rep_surface"]["moyenne"])
    resultat["verdict"] = {
        "meilleur_suffixe_code": meilleur_suf,
        "meilleur_repetes": meilleur_rep,
        "signaux_qui_battent_fifo_suffixe": bat_suffixe,
        "signaux_qui_battent_fifo_repetes": bat_repetes,
        "plafond_surface_atteint_par_toutes": all(
            abs(moyennes[c["nom"]]["ret_surface_finale"]["moyenne"]
                - resultat["protocole"]["plafonds"]["surface_finale"]) < 1e-9
            for c in configs),
        "gel_egal_fifo_sur_la_metrique_historique": (
            abs(moyennes["gel"]["ret_surface_finale"]["moyenne"]
                - moyennes["fifo"]["ret_surface_finale"]["moyenne"]) < 1e-9),
        "nouveaute_code_egale_fifo_code": (
            abs(moyennes["nouveaute_code"]["suf_code"]["moyenne"]
                - moyennes["fifo_code"]["suf_code"]["moyenne"]) < 1e-9
            and abs(moyennes["nouveaute_code"]["ret_code"]["moyenne"]
                    - moyennes["fifo_code"]["ret_code"]["moyenne"]) < 1e-9),
    }
    return resultat


def _flux_zipf(episodes: list[EpisodeM7], n: int, capacite: int,
               graine: int) -> tuple[list[EpisodeM7], set[tuple]]:
    """Un flux synthétique à queue lourde : le contrôle positif de l'appareil.

    Les codes sont tirés selon une loi de Zipf ; les 8 premiers rangs forment
    l'ensemble « chaud ». La récompense synthétique vaut 1 pour un code chaud :
    elle est donc *informative*, contrairement au proxy du corpus réel.
    """
    par_code: dict[tuple, list[EpisodeM7]] = collections.defaultdict(list)
    for e in episodes:
        par_code[e.cle_code].append(e)
    codes = sorted(par_code, key=repr)
    rng = random.Random(graine)
    rng.shuffle(codes)
    poids = [1.0 / (i + 1) ** 1.1 for i in range(len(codes))]
    chauds = set(codes[:8])
    out = []
    for _ in range(n):
        code = rng.choices(codes, weights=poids, k=1)[0]
        base = rng.choice(par_code[code])
        out.append(dataclasses.replace(
            base, recompense=1.0 if code in chauds else 0.0))
    return out, chauds


def controle_synthetique(episodes: list[EpisodeM7], permutations: int = 15,
                         graine: int = 1000, capacite: int = 8) -> dict:
    """Vérifie que l'appareil voit un effet quand il y en a un.

    Sur un flux de Zipf, le LFU (fréquence) et la récompense *informative*
    doivent battre le FIFO sur le suffixe ; le hasard doit rester au niveau
    d'un échantillon aléatoire. Si ce contrôle échoue, le négatif du corpus
    réel ne vaut rien.
    """
    configs = [
        {"nom": "fifo", "politique": "fifo", "cle": "surface", "sans": ()},
        {"nom": "fifo_code", "politique": "fifo", "cle": "code", "sans": ()},
        {"nom": "lfu_code", "politique": "lfu", "cle": "code", "sans": ()},
        {"nom": "nouveaute_code", "politique": "nouveaute", "cle": "code", "sans": ()},
        {"nom": "recompense_code", "politique": "recompense", "cle": "code", "sans": ()},
        {"nom": "hasard", "politique": "hasard", "cle": "surface", "sans": ()},
    ]
    res = {c["nom"]: collections.defaultdict(list) for c in configs}
    for k in range(permutations):
        flux, chauds = _flux_zipf(episodes, 528, capacite, graine + k)
        ordre = list(range(len(flux)))
        random.Random(graine + k).shuffle(ordre)
        prefixe = int(len(flux) * 0.8)
        for c in configs:
            m = _tourner(flux, ordre, prefixe, c["politique"], capacite,
                         c["cle"], graine + k, c["sans"])
            for nom in _METRIQUES:
                res[c["nom"]][nom].append(m[nom])
    moyennes = {nom: {m: _stats(v) for m, v in vals.items()}
                for nom, vals in res.items()}
    deltas = {nom: {m: _delta(res[nom][m], res["fifo"][m]) for m in _METRIQUES}
              for nom in res if nom != "fifo"}
    deltas["lfu_code"]["vs_fifo_code"] = {
        m: _delta(res["lfu_code"][m], res["fifo_code"][m]) for m in _METRIQUES}
    deltas["recompense_code"]["vs_fifo_code"] = {
        m: _delta(res["recompense_code"][m], res["fifo_code"][m]) for m in _METRIQUES}
    return {
        "protocole": {"capacite": capacite, "permutations": permutations,
                      "n": 528, "zipf": 1.1, "chauds": 8},
        "politiques": moyennes,
        "deltas_vs_fifo": deltas,
        "verdict": {
            "lfu_bat_fifo": deltas["lfu_code"]["suf_code"]["moyenne"] > 0,
            "recompense_informative_bat_fifo": deltas["recompense_code"]["suf_code"]["moyenne"] > 0,
            "hasard_non_significatif": abs(deltas["hasard"]["suf_code"]["moyenne"]) < 0.10,
        },
    }


# ---------------------------------------------------------------------------
# M7-bis — MemoireFrequence : la fréquence comme politique, pas comme signal
# ---------------------------------------------------------------------------
POLITIQUES_FREQUENCE = ("fifo", "lru", "lfu", "lfu_recence",
                        "contexte", "lfu_contexte", "hasard")


class MemoireFrequence:
    """M7-bis — une mémoire bornée dont la politique de base est la fréquence.

    A2 a montré qu'aucun signal neuromodulateur ne bat le FIFO sur ce corpus,
    mais que le LFU améliore nettement la rétention des répétés. M7-bis reprend
    donc la fréquence comme *politique* et pose deux questions contrôlées :

    - le **départage par récence** apporte-t-il quelque chose au LFU ? À
      fréquence égale, on évince soit la plus ancienne arrivée (``lfu``), soit
      la moins récemment écrite (``lfu_recence``) ;
    - un **contexte** (jeu, longueur de surface, type d'action) apporte-t-il
      quelque chose que la fréquence de l'item ne contient pas déjà ?

    Politiques :

    - ``fifo`` : évince la plus ancienne arrivée ;
    - ``lru`` : évince la moins récemment écrite ;
    - ``lfu`` : évince la moins fréquente ; à égalité, la plus ancienne
      arrivée. Les items de fréquence 1 ont ``t_dernier == t_arrivee`` : le
      départage ne diffère donc du LFU nu que sur des fréquences ≥ 2 ;
    - ``lfu_recence`` : évince la moins fréquente ; à égalité, la moins
      récemment écrite ;
    - ``contexte`` : évince l'item dont le contexte est le moins fréquent
      (score = nombre d'écritures du contexte) ; à égalité, le moins récent ;
    - ``lfu_contexte`` : score = ``log1p(frequence) + beta * part_du_contexte``
      où ``part_du_contexte`` est la part des écritures du contexte dans le
      flux vu. ``beta=0`` redonne exactement ``lfu_recence`` (contrôle de
      cohérence) ;
    - ``hasard`` : priorité aléatoire fixée à la première écriture (contrôle
      négatif).

    Le contexte n'est utilisé que pour les politiques contextuelles ; il doit
    alors être fourni à chaque écriture. Aucune information du suffixe n'entre
    dans le score : le contexte est compté en ligne, au fil des écritures.
    """

    nom = "M7bis-memoire-frequence"

    def __init__(self, capacite: int = 64, politique: str = "lfu",
                 cle: str = "surface", graine: int = 0,
                 beta: float = 1.0) -> None:
        if politique not in POLITIQUES_FREQUENCE:
            raise ValueError(f"politique inconnue : {politique}")
        if cle not in CLEFS:
            raise ValueError(f"clé inconnue : {cle}")
        self.capacite = max(0, int(capacite))
        self.politique = politique
        self.cle = cle
        self.beta = float(beta)
        self._slots: dict[tuple, dict] = {}
        self._ctx: collections.Counter = collections.Counter()
        self._t = 0
        self._n = 0
        self.evictions = 0
        self.evictions_sans_freq1 = 0
        self._rng = random.Random(graine)

    @property
    def contextuel(self) -> bool:
        return self.politique in ("contexte", "lfu_contexte")

    # ---- lecture ---------------------------------------------------------
    def contient(self, surface: str) -> bool:
        return any(e["surface"] == surface for e in self._slots.values())

    def contient_code(self, code: dict) -> bool:
        return any(e["code"] == code for e in self._slots.values())

    def codes(self) -> list[dict]:
        return [dict(e["code"]) for e in self._slots.values()]

    def etat(self) -> list[dict]:
        return [{"surface": e["surface"], "code": dict(e["code"]),
                 "frequence": int(e["freq"]), "contexte": e["ctx"],
                 "t_arrivee": e["t_arrivee"], "t_dernier": e["t_dernier"]}
                for e in sorted(self._slots.values(),
                                key=lambda e: e["t_arrivee"])]

    # ---- score et éviction ----------------------------------------------
    def _cle(self, surface: str, code: dict) -> tuple:
        if self.cle == "code":
            return tuple(sorted(code.items()))
        return ("surface", surface)

    def _score(self, e: dict) -> float:
        if self.politique in ("lfu", "lfu_recence"):
            return float(e["freq"])
        if self.politique == "contexte":
            return float(self._ctx.get(e["ctx"], 0))
        if self.politique == "lfu_contexte":
            part = self._ctx.get(e["ctx"], 0) / max(1, self._n)
            return math.log1p(e["freq"]) + self.beta * part
        if self.politique == "hasard":
            return float(e["hasard"])
        return 0.0

    def _departage(self, e: dict) -> int:
        if self.politique in ("fifo", "lfu"):
            return int(e["t_arrivee"])
        return int(e["t_dernier"])

    def _evincer(self) -> None:
        if not self._slots:
            return
        self.evictions += 1
        if min(e["freq"] for e in self._slots.values()) >= 2:
            self.evictions_sans_freq1 += 1
        if self.politique == "fifo":
            cle = min(self._slots,
                      key=lambda k: self._slots[k]["t_arrivee"])
        elif self.politique == "lru":
            cle = min(self._slots,
                      key=lambda k: self._slots[k]["t_dernier"])
        else:
            cle = min(self._slots, key=lambda k: (
                self._score(self._slots[k]),
                self._departage(self._slots[k]), repr(k)))
        del self._slots[cle]

    def stocker(self, surface: str, code: dict,
                contexte=None) -> None:
        if self.capacite <= 0:
            return
        if self.contextuel and contexte is None:
            raise ValueError(
                f"contexte requis pour la politique {self.politique}")
        cle = self._cle(surface, code)
        self._t += 1
        self._n += 1
        if self.contextuel:
            self._ctx[contexte] += 1
        existant = self._slots.get(cle)
        if existant is not None:
            existant.update(surface=surface, code=dict(code),
                            freq=existant["freq"] + 1,
                            t_dernier=self._t, ctx=contexte)
            return
        if len(self._slots) >= self.capacite:
            self._evincer()
        self._slots[cle] = {"surface": surface, "code": dict(code),
                            "freq": 1, "t_arrivee": self._t,
                            "t_dernier": self._t, "ctx": contexte,
                            "hasard": self._rng.random()}


# ---------------------------------------------------------------------------
# Le banc M7-bis : LFU, LFU + récence, contextes, clé permutée
# ---------------------------------------------------------------------------
_METRIQUES_BIS = ("ret_surface_prefixe", "ret_surface_finale",
                  "ret_nouveaux_utiles", "ret_nouveaux_suffixe",
                  "ret_code", "rep_surface", "rep_code", "suf_surface",
                  "suf_code", "codes_memoire")


def _classe_longueur(surface: str) -> str:
    n = len(surface)
    if n <= 6:
        return "court"
    if n <= 11:
        return "moyen"
    return "long"


def _contextes_episodes(episodes: list[EpisodeM7]) -> dict[str, list]:
    """Les trois contextes disponibles *à l'écriture*, sans étiquette future."""
    return {
        "jeu": [f"jeu={e.jeu}" for e in episodes],
        "longueur": [f"longueur={_classe_longueur(e.surface)}"
                     for e in episodes],
        "type": [f"type={e.code.get('action')}" for e in episodes],
    }


def _contextes_permutes(contextes: dict[str, list], ordre: list[int],
                        prefixe: int, graine: int) -> dict[str, list]:
    """Permute les étiquettes *du préfixe* en gardant exactement leur multiset.

    C'est le contrôle « clé permutée » : les comptes marginaux de contexte sont
    identiques, mais l'association item-contexte est détruite. Si la politique
    contextuelle réelle ne fait pas mieux que sa version permutée, le contexte
    n'apporte rien au-delà de sa distribution marginale.
    """
    out = {}
    for j, (signal, labels) in enumerate(contextes.items()):
        rng = random.Random(graine + 100003 + j * 7919)
        sous = [labels[i] for i in ordre[:prefixe]]
        rng.shuffle(sous)
        lab = list(labels)
        for pos, i in enumerate(ordre[:prefixe]):
            lab[i] = sous[pos]
        out[signal] = lab
    return out


def _tourner_frequence(episodes: list[EpisodeM7], ordre: list[int],
                       prefixe: int, config: dict, capacite: int,
                       contextes: list | None, graine: int = 0) -> dict:
    memoire = MemoireFrequence(
        capacite, politique=config["politique"], cle=config["cle"],
        graine=graine, beta=config.get("beta", 1.0))
    surfaces_vues: set[str] = set()
    codes_vus: set[tuple] = set()
    rep_s = rep_s_n = rep_c = rep_c_n = 0
    for i in ordre[:prefixe]:
        ep = episodes[i]
        if ep.surface in surfaces_vues:
            rep_s_n += 1
            rep_s += int(memoire.contient(ep.surface))
        if ep.cle_code in codes_vus:
            rep_c_n += 1
            rep_c += int(memoire.contient_code(ep.code))
        surfaces_vues.add(ep.surface)
        codes_vus.add(ep.cle_code)
        ctx = None if contextes is None else contextes[i]
        memoire.stocker(ep.surface, ep.code, contexte=ctx)
    entrees = memoire.etat()
    surfaces_memoire = {e["surface"] for e in entrees}
    codes_memoire = {tuple(sorted(e["code"].items())) for e in entrees}
    total_surfaces = collections.Counter(e.surface for e in episodes)
    utiles = {s for s in surfaces_vues if total_surfaces[s] >= 2}
    suffixe = ordre[prefixe:]
    prefix_counts = collections.Counter(
        episodes[i].surface for i in ordre[:prefixe])
    suffix_surfaces = {episodes[i].surface for i in suffixe}
    nouveaux_suffixe = {s for s, c in prefix_counts.items()
                        if c == 1 and s in suffix_surfaces}
    suf_s = sum(1 for i in suffixe
                if episodes[i].surface in surfaces_memoire)
    suf_c = sum(1 for i in suffixe
                if episodes[i].cle_code in codes_memoire)
    return {
        "slots": len(entrees),
        "ret_surface_prefixe": len(surfaces_memoire & surfaces_vues)
        / max(1, len(surfaces_vues)),
        "ret_surface_finale": len(surfaces_memoire)
        / max(1, len({e.surface for e in episodes})),
        "ret_nouveaux_utiles": len(surfaces_memoire & utiles)
        / max(1, len(utiles)),
        "ret_nouveaux_suffixe": len(surfaces_memoire & nouveaux_suffixe)
        / max(1, len(nouveaux_suffixe)),
        "ret_code": len(codes_memoire & codes_vus) / max(1, len(codes_vus)),
        "rep_surface": rep_s / max(1, rep_s_n),
        "rep_code": rep_c / max(1, rep_c_n),
        "rep_n": rep_s_n,
        "suf_surface": suf_s / max(1, len(suffixe)),
        "suf_code": suf_c / max(1, len(suffixe)),
        "codes_memoire": len(codes_memoire),
        "evictions": memoire.evictions,
        "evictions_sans_freq1": memoire.evictions_sans_freq1,
    }


def _oracle_frequence(episodes: list[EpisodeM7], ordre: list[int],
                      prefixe: int, capacite: int) -> dict:
    suffixe = ordre[prefixe:]
    cs = collections.Counter(episodes[i].surface for i in suffixe)
    cc = collections.Counter(episodes[i].cle_code for i in suffixe)
    n = max(1, len(suffixe))
    return {"suf_surface": sum(v for _, v in cs.most_common(capacite)) / n,
            "suf_code": sum(v for _, v in cc.most_common(capacite)) / n}


def _p_sign(deltas: list[float]) -> float:
    """p bilatéral exact du signe, sans hypothèse de normalité."""
    non_nuls = [d for d in deltas if d != 0]
    if not non_nuls:
        return 1.0
    gains = sum(1 for d in non_nuls if d > 0)
    n = len(non_nuls)
    k = max(gains, n - gains)
    p = sum(math.comb(n, i) for i in range(k, n + 1)) / (2 ** n)
    return min(1.0, 2.0 * p)


def _delta_bis(apparie: list[float], temoin: list[float]) -> dict:
    d = [a - b for a, b in zip(apparie, temoin)]
    out = _delta(apparie, temoin)
    out["p_sign"] = _p_sign(d)
    return out


def _configs_frequence() -> list[dict]:
    configs = []
    for cle in ("surface", "code"):
        suffixe = "" if cle == "surface" else "_code"
        for politique in ("fifo", "lru", "lfu", "lfu_recence"):
            configs.append({"nom": politique + suffixe,
                            "politique": politique, "cle": cle, "beta": 0.0,
                            "signal": None, "permute": False})
    configs.append({"nom": "hasard", "politique": "hasard", "cle": "surface",
                    "beta": 0.0, "signal": None, "permute": False})
    for signal in ("jeu", "longueur", "type"):
        configs.append({"nom": f"contexte_{signal}", "politique": "contexte",
                        "cle": "surface", "beta": 0.0, "signal": signal,
                        "permute": False})
        configs.append({"nom": f"lfu_contexte_{signal}",
                        "politique": "lfu_contexte", "cle": "surface",
                        "beta": 1.0, "signal": signal, "permute": False})
        for beta in (0.0, 0.5, 2.0, 4.0):
            configs.append({"nom": f"lfu_contexte_{signal}_b{beta:g}",
                            "politique": "lfu_contexte", "cle": "surface",
                            "beta": beta, "signal": signal,
                            "permute": False})
    return configs


def _configs_permutees(configs: list[dict]) -> list[dict]:
    signaux = ("jeu", "longueur", "type")
    noms = {f"contexte_{s}" for s in signaux}
    noms |= {f"lfu_contexte_{s}" for s in signaux}
    return [dict(c, nom=c["nom"] + "_permute", permute=True)
            for c in configs if c["nom"] in noms]


def _resume_delta(d: dict) -> dict:
    return {"moyenne": d["moyenne"], "ic95": d["ic95"],
            "gains": d["gains"], "p_sign": d["p_sign"], "n": d["n"],
            "bat_zero": d["moyenne"] > 0 and d["ic95"][0] > 0}


def experience_m7_bis(episodes: list[EpisodeM7] | None = None,
                      permutations: int = 30, capacite: int = 16,
                      graine: int = 0, synthetique: bool = True) -> dict:
    """Le banc M7-bis, apparié sur les mêmes 30 permutations.

    Toutes les politiques voient le même flux, la même capacité et le même
    préfixe. La mémoire est gelée à la fin du préfixe ; le suffixe (20 %) est
    interrogé sans réécriture. Les deltas sont ``politique - LFU`` (même clé)
    et ``politique - FIFO`` (même clé), permutation par permutation.

    Le contrôle « clé permutée » réassigne les étiquettes de contexte du
    préfixe au hasard, à multiset constant. Un gain contexte réel qui
    disparaît après permutation est un gain de contexte ; un gain qui survit
    est un artefact de la marge.
    """
    ep = episodes if episodes is not None else preparer_flux()
    n = len(ep)
    prefixe = int(n * 0.8)
    base = _configs_frequence()
    configs = base + _configs_permutees(base)
    contextes = _contextes_episodes(ep)
    resultats: dict[str, dict[str, list[float]]] = {
        c["nom"]: collections.defaultdict(list) for c in configs}
    oracle = collections.defaultdict(list)
    diagnostics = collections.defaultdict(collections.Counter)
    for k in range(permutations):
        ordre = list(range(n))
        random.Random(graine + k).shuffle(ordre)
        permutes = _contextes_permutes(contextes, ordre, prefixe,
                                       graine + k)
        for c in configs:
            ctx = None
            if c["signal"]:
                source = permutes if c["permute"] else contextes
                ctx = source[c["signal"]]
            m = _tourner_frequence(ep, ordre, prefixe, c, capacite, ctx,
                                   graine + k)
            for met in _METRIQUES_BIS:
                resultats[c["nom"]][met].append(m[met])
            if c["nom"] in ("lfu", "lfu_recence", "lfu_code",
                            "lfu_recence_code"):
                diagnostics[c["nom"]]["evictions"] += m["evictions"]
                diagnostics[c["nom"]]["sans_freq1"] += m[
                    "evictions_sans_freq1"]
        o = _oracle_frequence(ep, ordre, prefixe, capacite)
        oracle["suf_surface"].append(o["suf_surface"])
        oracle["suf_code"].append(o["suf_code"])
    moyennes = {nom: {m: _stats(v) for m, v in vals.items()}
                for nom, vals in resultats.items()}
    ref_lfu = {"surface": "lfu", "code": "lfu_code"}
    ref_fifo = {"surface": "fifo", "code": "fifo_code"}
    deltas_lfu = {}
    deltas_fifo = {}
    for c in configs:
        nom = c["nom"]
        if nom != ref_lfu[c["cle"]]:
            deltas_lfu[nom] = {m: _delta_bis(resultats[nom][m],
                                             resultats[ref_lfu[c["cle"]]][m])
                               for m in _METRIQUES_BIS}
        if nom != ref_fifo[c["cle"]]:
            deltas_fifo[nom] = {m: _delta_bis(resultats[nom][m],
                                              resultats[ref_fifo[c["cle"]]][m])
                                for m in _METRIQUES_BIS}
    # contrôle de cohérence : beta=0 doit être identique à lfu_recence
    ecart_beta_zero = {}
    for signal in ("jeu", "longueur", "type"):
        nom_b0 = f"lfu_contexte_{signal}_b0"
        ecart_beta_zero[signal] = {
            m: max((abs(a - b) for a, b in zip(resultats[nom_b0][m],
                                               resultats["lfu_recence"][m])),
                   default=0.0) for m in _METRIQUES_BIS}
    # contrôles de contexte : réel vs permuté, réel vs LFU
    contexte_controle = {}
    for signal in ("jeu", "longueur", "type"):
        for variante in ("contexte", "lfu_contexte"):
            nom = f"{variante}_{signal}"
            perm = nom + "_permute"
            contexte_controle[nom] = {
                "delta_reel_vs_permute": {
                    m: _resume_delta(_delta_bis(resultats[nom][m],
                                                resultats[perm][m]))
                    for m in ("suf_surface", "suf_code", "rep_surface",
                              "rep_code", "ret_nouveaux_utiles")},
                "delta_reel_vs_lfu": {
                    m: _resume_delta(deltas_lfu[nom][m])
                    for m in ("suf_surface", "suf_code", "rep_surface",
                              "rep_code", "ret_nouveaux_utiles")},
                "delta_permute_vs_lfu": {
                    m: _resume_delta(deltas_lfu[perm][m])
                    for m in ("suf_surface", "suf_code", "rep_surface",
                              "rep_code", "ret_nouveaux_utiles")},
            }
    plafond = capacite / max(1, len({e.surface for e in ep}))
    toutes_au_plafond = all(
        abs(moyennes[c["nom"]]["ret_surface_finale"]["moyenne"] - plafond)
        < 1e-12 for c in configs)
    # verdicts calculés, jamais déclarés
    def _bat(d: dict) -> bool:
        return d["moyenne"] > 0 and d["ic95"][0] > 0

    rec = "lfu_recence"
    rec_code = "lfu_recence_code"
    verdict = {
        "lfu_recence_bat_lfu": {
            "surface": {m: _resume_delta(deltas_lfu[rec][m])
                        for m in ("suf_surface", "rep_surface",
                                  "ret_nouveaux_utiles",
                                  "ret_nouveaux_suffixe")},
            "code": {m: _resume_delta(deltas_lfu[rec_code][m])
                     for m in ("suf_code", "rep_code", "ret_code")},
        },
        "lfu_bat_fifo": {
            "surface": {m: _resume_delta(deltas_fifo["lfu"][m])
                        for m in ("suf_surface", "rep_surface",
                                  "ret_nouveaux_utiles",
                                  "ret_nouveaux_suffixe")},
            "code": {m: _resume_delta(deltas_fifo["lfu_code"][m])
                     for m in ("suf_code", "rep_code", "ret_code")},
        },
        "contexte_bat_lfu": {
            nom: {m: _resume_delta(deltas_lfu[nom][m])
                  for m in ("suf_surface", "suf_code", "rep_surface",
                            "rep_code", "ret_nouveaux_utiles")}
            for nom in contexte_controle},
        "cle_permutee_egale_reelle": {
            nom: {m: _resume_delta(v["delta_reel_vs_permute"][m])
                  for m in ("suf_surface", "suf_code", "rep_surface",
                            "rep_code", "ret_nouveaux_utiles")}
            for nom, v in contexte_controle.items()},
        "plafond_surface_finale": plafond,
        "toutes_politiques_au_plafond_historique": toutes_au_plafond,
        "beta_zero_egal_lfu_recence": {
            signal: all(max(abs(a - b) for a, b in zip(
                resultats[f"lfu_contexte_{signal}_b0"][m],
                resultats["lfu_recence"][m])) < 1e-12
                for m in _METRIQUES_BIS)
            for signal in ("jeu", "longueur", "type")},
    }
    resultat = {
        "meta": {"module": "M7-bis", "classe": "MemoireFrequence",
                 "date": datetime.datetime.now(
                     datetime.timezone.utc).isoformat(timespec="seconds")},
        "protocole": {
            "n": n, "prefixe": prefixe, "suffixe": n - prefixe,
            "capacite": capacite, "permutations": permutations,
            "graine": graine,
            "metriques": {
                "ret_surface_prefixe": "surfaces retenues / surfaces distinctes vues au préfixe (plafonnée par la capacité)",
                "ret_surface_finale": "surfaces retenues / surfaces distinctes du flux (plafond = capacité/vocabulaire)",
                "ret_nouveaux_utiles": "surfaces vues au préfixe qui reviennent dans le flux et sont retenues / ces surfaces",
                "ret_nouveaux_suffixe": "surfaces vues une seule fois au préfixe et présentes dans le suffixe, retenues / ces surfaces (oracle d'évaluation)",
                "ret_code": "codes retenus / codes distincts vus au préfixe",
                "rep_surface": "écritures répétées dont la surface était déjà en mémoire",
                "rep_code": "écritures répétées dont le code était déjà en mémoire",
                "suf_surface": "requêtes du suffixe dont la surface est en mémoire (mémoire gelée)",
                "suf_code": "requêtes du suffixe dont le code est en mémoire (mémoire gelée)",
            },
            "plafond_surface_finale": plafond,
        },
        "configurations": configs,
        "resultats": moyennes,
        "deltas_vs_lfu": deltas_lfu,
        "deltas_vs_fifo": deltas_fifo,
        "oracle_suffixe": {m: _stats(v) for m, v in oracle.items()},
        "controles": {
            "contexte_reel_vs_permute": contexte_controle,
            "beta_zero_ecart_max": ecart_beta_zero,
            "evictions": {
                nom: {"evictions": int(v["evictions"]),
                      "sans_freq1": int(v["sans_freq1"]),
                      "part_sans_freq1": v["sans_freq1"]
                      / max(1, v["evictions"])}
                for nom, v in diagnostics.items()},
        },
        "verdict": verdict,
        "limites": [
            "Les permutations aléatoires rendent le suffixe échangeable avec le préfixe : la fréquence d'item y est le prédicteur optimal, un contexte ne peut pas la battre par construction.",
            "Le contrôle de contexte mesure donc surtout l'absence d'information contextuelle *au-delà* de la fréquence ; il ne teste pas une dérive temporelle réelle (jeux successifs), que les permutations détruisent.",
            "rep_surface est en partie tautologique : le LFU est défini pour garder les items répétés.",
            "Le plafond de rétention des nouveaux (capacité/vocabulaire) n'est pas un résultat ; ret_nouveaux_utiles et ret_nouveaux_suffixe sont les métriques discriminantes ajoutées.",
        ],
    }
    if synthetique:
        resultat["controle_synthetique_frequence"] = controle_zipf_frequence(
            ep, permutations=max(8, permutations // 2), graine=graine + 1000)
    return resultat


def controle_zipf_frequence(episodes: list[EpisodeM7],
                            permutations: int = 15, graine: int = 1000,
                            capacite: int = 8) -> dict:
    """Contrôle positif : sur un flux de Zipf, le LFU doit battre le FIFO."""
    configs = [
        {"nom": "fifo_code", "politique": "fifo", "cle": "code",
         "beta": 0.0, "signal": None},
        {"nom": "lfu_code", "politique": "lfu", "cle": "code",
         "beta": 0.0, "signal": None},
        {"nom": "lfu_recence_code", "politique": "lfu_recence", "cle": "code",
         "beta": 0.0, "signal": None},
        {"nom": "hasard", "politique": "hasard", "cle": "surface",
         "beta": 0.0, "signal": None},
    ]
    res = {c["nom"]: collections.defaultdict(list) for c in configs}
    for k in range(permutations):
        flux, chauds = _flux_zipf(episodes, 528, capacite, graine + k)
        ordre = list(range(len(flux)))
        random.Random(graine + k).shuffle(ordre)
        prefixe = int(len(flux) * 0.8)
        for c in configs:
            m = _tourner_frequence(flux, ordre, prefixe, c, capacite, None,
                                   graine + k)
            for met in _METRIQUES_BIS:
                res[c["nom"]][met].append(m[met])
    moyennes = {nom: {m: _stats(v) for m, v in vals.items()}
                for nom, vals in res.items()}
    deltas = {}
    for nom in res:
        if nom != "fifo_code":
            deltas[nom] = {m: _delta_bis(res[nom][m], res["fifo_code"][m])
                           for m in _METRIQUES_BIS}
    deltas["lfu_code_vs_lfu_recence"] = {
        m: _delta_bis(res["lfu_recence_code"][m], res["lfu_code"][m])
        for m in _METRIQUES_BIS}
    return {
        "protocole": {"capacite": capacite, "permutations": permutations,
                      "n": 528, "zipf": 1.1, "chauds": 8},
        "politiques": moyennes,
        "deltas": deltas,
        "verdict": {
            "lfu_bat_fifo_suffixe_code": (
                deltas["lfu_code"]["suf_code"]["moyenne"] > 0
                and deltas["lfu_code"]["suf_code"]["ic95"][0] > 0),
            "lfu_recence_bat_lfu_suffixe_code": (
                deltas["lfu_code_vs_lfu_recence"]["suf_code"]["moyenne"] > 0
                and deltas["lfu_code_vs_lfu_recence"]["suf_code"]["ic95"][0]
                > 0),
            "hasard_non_significatif": (
                abs(deltas["hasard"]["suf_code"]["moyenne"]) < 0.10),
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(experience_m7(permutations=10), ensure_ascii=False,
                     indent=1))

#!/usr/bin/env python3
"""M6 — porte exécutive : une vraie tâche de conflit langue/tâche sur B7.

L'ancienne porte ne mesurait qu'une chose : `MULTI.detecte_langue(surface)`
comparée à la langue cible. Son « exactitude » de 72,9 % était donc le taux du
classifieur lexical, pas une mesure d'inhibition ; son « coût de commutation »
négatif venait de la composition des blocs (les cibles alternaient sur des
items très majoritairement français), pas d'un coût cognitif.

La tâche construite ici est un **go/no-go de confluence** sur les surfaces B7
fr/en (11 codes, deux langues) :

- `go`          : la sonde est le coup cible **dans la langue cible** → accepter ;
- `traduction`  : même coup, **autre langue** → inhiber le sens, refuser ;
- `langue`      : autre coup, **langue cible** → inhiber la langue, refuser ;
- `ni`          : autre coup, autre langue → refuser.

Les quatre conditions sont équilibrées (22 essais chacune, 88 au total) : un
politique « toujours non » obtient 75 %, et chaque canal seul (langue ou sens)
obtient 75 % aussi, avec 25 % de faux positifs. La seule politique qui dépasse
le taux de base est la **conjonction** (sens ET langue) : exactitude 94,3 %,
exactitude équilibrée 88,6 %, 0 faux positif, 5 faux négatifs. Les 5 FN sont
tous des échecs du canal langue sur des surfaces **non identifiables** (deux
codes ont la même surface en fr et en en : « go D4 », « tic-tac-toe A1 ») ou
d'ambiguïté lexicale (« english draughts »). Aucun effet d'inhibition ni de
commutation n'apparaît : la porte est une règle déterministe sans mémoire ; le
coût de commutation apparié est 0,000, alors qu'un contrôle positif de
persévération donne 0,381. Conclusion : **la détection de langue n'est pas du
contrôle exécutif**, c'est un classifieur lexical bruité ; le contrôle est la
règle de conjonction, et le corpus B7 ne permet pas de mesurer l'inhibition.

Voir `/tmp/a1-m5-m6.md` pour les chiffres et la décomposition.
"""
from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass

from jeux.codecs import codec
from jeux.corpus_multilingue import construire_corpus_multilingue
from jeux.lexique import langue_probable
from jeux.lexique_multilingue import MULTI
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G
from jeux.regles import morpion as M
from semantique.universaux import code_rsn, empreinte_code

CONDITIONS = ("go", "traduction", "langue", "ni")
# Tâches de la porte de tâche : juger le sens ou la langue de la sonde.
TACHES = ("sens", "langue")
# Domaines du lexique qui portent la langue d'une surface de jeu.
DOMAINES = ("jeu.nom", "echecs.piece", "cartes.rang", "cartes.couleur",
            "go.passe", "commun.couleur")


@dataclass(frozen=True)
class Essai:
    """Un essai de la tâche : la sonde, la cible et la bonne réponse."""

    texte: str
    jeu: str
    langue_vraie: str
    code_vrai: dict
    cible_code: dict
    cible_langue: str
    condition: str
    contexte: object

    @property
    def attendu(self) -> bool:
        return self.condition == "go"


@dataclass(frozen=True)
class EssaiTache:
    """Un essai de la tâche de commutation : sonde, cible, indice de tâche.

    `tache` est la **consigne** (ce que la porte doit juger) ; `condition` dit
    si les deux canaux sont d'accord (`congruent`) ou non (`incongruent`).
    `transition` vaut `initiale`, `repetition` ou `commutation` selon le bloc
    précédent. La bonne réponse dépend de la consigne, jamais de l'accord.
    """

    texte: str
    jeu: str
    langue_vraie: str
    code_vrai: dict
    cible_code: dict
    cible_langue: str
    tache: str
    condition: str
    transition: str
    tache_precedente: str | None
    reponse_sens: bool
    reponse_langue: bool
    contexte: object

    @property
    def attendu(self) -> bool:
        return self.reponse_sens if self.tache == "sens" else self.reponse_langue


def _contexte_depart(jeu: str):
    """Le contexte des surfaces B7 : elles sont générées depuis l'état initial.

    Les `ItemType` de `typed_corpus` ne conservent le contexte que sous forme de
    chaîne ; pour décoder une surface B7 il faut la position de départ, qui est
    connue et fixe par jeu. On la reconstruit ici (et seulement pour B7).
    """
    if jeu == "echecs":
        return E.rsn_depuis_position(E.Position.depart())
    if jeu == "dames":
        return D.rsn_depuis_position(D.Position.depart())
    if jeu == "go":
        return G.Position.depart(9, 65).vers_rsn()
    if jeu == "morpion":
        return M.etat_initial()
    return None


def _normalise(it) -> dict:
    """Ramène un item B7 (corpus natif ou `typed_corpus.ItemType`) à un dict."""
    if hasattr(it, "attendu"):  # jeux.corpus.Item : contexte RSN disponible
        return {"texte": it.texte, "jeu": it.jeu, "langue": it.langue,
                "code": code_rsn(it.attendu), "contexte": getattr(it, "contexte", None),
                "format": getattr(it, "format", "multilingue")}
    return {"texte": it.texte, "jeu": it.jeu, "langue": it.langue,
            "code": dict(it.code), "contexte": _contexte_depart(it.jeu),
            "format": getattr(it, "format", "multilingue")}


def _wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Intervalle de Wilson à 95 % pour une proportion."""
    if n <= 0:
        return 0.0, 1.0
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    demi = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - demi), min(1.0, centre + demi)


def _mcc(tp: int, fp: int, fn: int, tn: int) -> float:
    denom = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return (tp * tn - fp * fn) / denom if denom else 0.0


class Porte:
    """La porte : deux canaux (langue, sens) et une règle de conjonction."""

    nom = "M6-gating"
    LANGUES = ("fr", "en")

    def __init__(self) -> None:
        self._cache_lecture: dict[tuple[str, str], dict | None] = {}
        self._cache_langue: dict[str, str | None] = {}

    # ------------------------------------------------------------------
    # Les deux canaux perceptifs.
    # ------------------------------------------------------------------
    def langue(self, texte: str) -> str | None:
        """Canal langue, **déterministe**.

        On combine deux readouts : le lexique fr/en (`langue_probable`, qui
        tranche les formes fléchies) puis un vote sur le lexique multilingue des
        domaines de jeu, départagé par ordre alphabétique. Le canal MULTI global
        (`MULTI.detecte_langue`) n'est **pas** déterministe sur les surfaces
        ambiguës — il itère des ensembles dont l'ordre dépend de
        `PYTHONHASHSEED` ; il reste exposé par `langue_multi` pour comparaison,
        mais la porte ne l'utilise pas.
        """
        if texte in self._cache_langue:
            return self._cache_langue[texte]
        lp, _ = langue_probable(texte)
        if lp in self.LANGUES:
            resultat = lp
        else:
            resultat = self._vote_lexical(texte)
        self._cache_langue[texte] = resultat
        return resultat

    def langue_multi(self, texte: str) -> str | None:
        """L'ancien canal (MULTI), gardé pour mesurer son instabilité."""
        return MULTI.detecte_langue(texte)

    @staticmethod
    def _vote_lexical(texte: str) -> str | None:
        votes: Counter[str] = Counter()
        for domaine in DOMAINES:
            for m in MULTI.cherche(domaine, texte):
                votes[m.langue] += 1
        if not votes:
            return None
        # départage déterministe : plus de formes, puis ordre alphabétique
        return min(votes, key=lambda langue: (-votes[langue], langue))

    def lire(self, texte: str, jeu: str, contexte=None) -> dict | None:
        """Canal sens : surface → code typé, au niveau sémantique (4)."""
        cle = (texte, jeu)
        if cle in self._cache_lecture:
            return self._cache_lecture[cle]
        try:
            lec = codec(jeu).lit(texte, niveau=4, contexte=contexte)
        except Exception:
            lec = None
        code = code_rsn(lec.rsn) if (lec is not None and lec.rsn is not None) else None
        self._cache_lecture[cle] = code
        return code

    # ------------------------------------------------------------------
    # Construction de la tâche.
    # ------------------------------------------------------------------
    def tache_conflit(self, items=None, cibles=("fr", "en")) -> list[Essai]:
        """Construit les 4 conditions × codes × langues cibles.

        `items=None` prend le corpus B7 natif (contextes RSN exacts). Sinon on
        accepte une liste d'items B7 (y compris `typed_corpus.items()`), en se
        limitant au format `multilingue` pour ne pas mélanger les surfaces B5
        (dont certaines étiquettes de langue sont des variantes anglaises
        rangées côté fr).
        """
        if len(cibles) != 2:
            raise ValueError("la tâche de conflit exige exactement deux langues")
        if items is None:
            brut = [it for it in construire_corpus_multilingue().items]
        else:
            brut = list(items)
        infos = [_normalise(it) for it in brut]
        b7 = [i for i in infos if i["format"] == "multilingue"]
        if sum(1 for i in b7 if i["langue"] in cibles) >= 2 * len(cibles):
            infos = b7
        infos = [i for i in infos if i["langue"] in cibles]

        groupes: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
        for info in infos:
            groupes[empreinte_code(info["code"])][info["langue"]].append(info)
        codes = sorted(cle for cle, par_langue in groupes.items()
                       if all(langue in par_langue for langue in cibles))
        if not codes:
            return []

        def sonde(cle: str, langue: str) -> dict:
            # plusieurs surfaces pour un même code : ordre stable, on prend la 1re
            return sorted(groupes[cle][langue], key=lambda i: i["texte"])[0]

        essais: list[Essai] = []
        for i_code, cle in enumerate(codes):
            for i_langue, langue in enumerate(cibles):
                autre = cibles[1] if langue == cibles[0] else cibles[0]
                autres = [c for c in codes if c != cle]
                cle_autre = autres[(i_code + i_langue) % len(autres)]
                description = {
                    "go": (cle, langue),
                    "traduction": (cle, autre),
                    "langue": (cle_autre, langue),
                    "ni": (cle_autre, autre),
                }
                # rotation déterministe : la condition en tête de bloc change
                decalage = (i_code + i_langue) % len(CONDITIONS)
                ordre = CONDITIONS[decalage:] + CONDITIONS[:decalage]
                for condition in ordre:
                    cle_sonde, langue_sonde = description[condition]
                    info = sonde(cle_sonde, langue_sonde)
                    essais.append(Essai(
                        texte=info["texte"], jeu=info["jeu"],
                        langue_vraie=info["langue"], code_vrai=dict(info["code"]),
                        cible_code=dict(groupes[cle][cibles[0]][0]["code"]),
                        cible_langue=langue, condition=condition,
                        contexte=info["contexte"]))
        return essais

    # ------------------------------------------------------------------
    # Tâche de commutation : deux consignes, conflit, switch.
    # ------------------------------------------------------------------
    def tache_switch(self, items=None, cibles=("fr", "en")) -> list[EssaiTache]:
        """Tâche à deux consignes (`sens` / `langue`) sur les mêmes sondes B7.

        Chaque groupe (code cible × langue cible) donne **9 blocs de 4 essais**
        (go, traduction, langue, ni), tous de même consigne dans un bloc. La
        suite des consignes est `sens, langue, langue, sens, sens, langue,
        langue, sens, sens` : 4 commutations et 4 répétitions par groupe, à
        sondes appariées (mêmes 4 essais, ordre tourné). La consigne est
        l'**indice** ; elle est parfaitement fiable.

        `condition` vaut `congruent` quand les deux canaux donnent la même
        réponse (go : oui/oui ; ni : non/non) et `incongruent` quand ils
        divergent (traduction : sens oui, langue non ; langue : sens non,
        langue oui). C'est le conflit de la tâche : sous la consigne `sens`, le
        canal langue est le distracteur, et réciproquement.
        """
        if len(cibles) != 2:
            raise ValueError("la tâche de commutation exige exactement deux langues")
        if items is None:
            brut = [it for it in construire_corpus_multilingue().items]
        else:
            brut = list(items)
        infos = [_normalise(it) for it in brut]
        b7 = [i for i in infos if i["format"] == "multilingue"]
        if sum(1 for i in b7 if i["langue"] in cibles) >= 2 * len(cibles):
            infos = b7
        infos = [i for i in infos if i["langue"] in cibles]

        groupes: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
        for info in infos:
            groupes[empreinte_code(info["code"])][info["langue"]].append(info)
        codes = sorted(cle for cle, par_langue in groupes.items()
                       if all(langue in par_langue for langue in cibles))
        if not codes:
            return []

        def sonde(cle: str, langue: str) -> dict:
            return sorted(groupes[cle][langue], key=lambda i: i["texte"])[0]

        # Blocs appariés : 4 commutations et 4 répétitions, tâches équilibrées.
        cycle = ("sens", "langue", "langue", "sens",
                 "sens", "langue", "langue", "sens", "sens")
        essais: list[EssaiTache] = []
        for i_code, cle in enumerate(codes):
            for i_langue, langue in enumerate(cibles):
                autre = cibles[1] if langue == cibles[0] else cibles[0]
                autres = [c for c in codes if c != cle]
                cle_autre = autres[(i_code + i_langue) % len(autres)]
                description = {
                    "go": (cle, langue),
                    "traduction": (cle, autre),
                    "langue": (cle_autre, langue),
                    "ni": (cle_autre, autre),
                }
                cible_code = dict(groupes[cle][cibles[0]][0]["code"])
                probes = []
                for condition, (cle_s, langue_s) in description.items():
                    info = sonde(cle_s, langue_s)
                    rep_sens = dict(info["code"]) == cible_code
                    rep_langue = info["langue"] == langue
                    probes.append({
                        "info": info, "condition": condition,
                        "reponse_sens": rep_sens, "reponse_langue": rep_langue,
                        "congruent": rep_sens == rep_langue,
                    })
                for b, tache in enumerate(cycle):
                    prec = cycle[b - 1] if b else None
                    transition = ("initiale" if prec is None else
                                  "commutation" if tache != prec else "repetition")
                    decalage = (i_code + i_langue + b) % len(probes)
                    for p in probes[decalage:] + probes[:decalage]:
                        info = p["info"]
                        essais.append(EssaiTache(
                            texte=info["texte"], jeu=info["jeu"],
                            langue_vraie=info["langue"], code_vrai=dict(info["code"]),
                            cible_code=dict(cible_code), cible_langue=langue,
                            tache=tache,
                            condition="congruent" if p["congruent"] else "incongruent",
                            transition=transition, tache_precedente=prec,
                            reponse_sens=p["reponse_sens"],
                            reponse_langue=p["reponse_langue"],
                            contexte=info["contexte"]))
        return essais

    def _decisions_switch(self, essais, politique: str = "tache") -> list[dict]:
        """Les décisions de la porte sur la tâche de commutation.

        `tache` est la porte dure : elle applique le canal désigné par la
        consigne et ignore l'autre. Les autres politiques sont les témoins
        (canal seul, consigne inversée, indice aléatoire, tout-non) et le
        **contrôle positif** de persévération : sur un bloc de commutation, la
        porte reste sur la consigne précédente.
        """
        rng = random.Random(0)
        decisions = []
        for essai in essais:
            code = self.lire(essai.texte, essai.jeu, essai.contexte)
            langue = self.langue(essai.texte)
            sens = code == essai.cible_code
            langue_ok = langue == essai.cible_langue
            if politique == "tache":
                accepte = sens if essai.tache == "sens" else langue_ok
            elif politique == "sens":
                accepte = sens
            elif politique == "langue":
                accepte = langue_ok
            elif politique == "tache_inversee":
                accepte = langue_ok if essai.tache == "sens" else sens
            elif politique == "tout_non":
                accepte = False
            elif politique == "indice_aleatoire":
                accepte = sens if rng.choice(TACHES) == "sens" else langue_ok
            elif politique == "perseveration_tache":
                if essai.transition == "commutation" and essai.tache_precedente:
                    accepte = (sens if essai.tache_precedente == "sens" else langue_ok)
                else:
                    accepte = sens if essai.tache == "sens" else langue_ok
            else:
                raise ValueError(f"politique de tâche inconnue : {politique!r}")
            decisions.append({"accepte": bool(accepte), "code": code,
                              "langue": langue, "sens": bool(sens),
                              "langue_ok": bool(langue_ok), "essai": essai})
        return decisions

    @staticmethod
    def _metriques_switch(decisions) -> dict:
        """Exactitude et coûts de conflit/commutation, par tâche et croisés.

        Les coûts sont des **effets d'exactitude** : `effet_conflit` =
        exact(incongruent) − exact(congruent), `effet_commutation` =
        exact(commutation) − exact(répétition). Un effet négatif est un coût.
        """
        par_tache = {t: {"n": 0, "corrects": 0, "acceptes": 0} for t in TACHES}
        par_condition = {c: {"n": 0, "corrects": 0}
                         for c in ("congruent", "incongruent")}
        par_transition = {t: {"n": 0, "corrects": 0}
                          for t in ("initiale", "repetition", "commutation")}
        par_croise = {(c, t): {"n": 0, "corrects": 0}
                      for c in par_condition for t in par_transition}
        # Macro-moyenne par sonde (texte, jeu, code cible, langue cible) : les
        # sondes ne sont pas également représentées dans le flux, la moyenne
        # par essai favoriserait les sondes répétées.
        par_sonde = {t: defaultdict(lambda: {"n": 0, "corrects": 0}) for t in TACHES}
        n = ok = acceptes = positifs = 0
        for d in decisions:
            e = d["essai"]
            correct = d["accepte"] == e.attendu
            n += 1
            ok += int(correct)
            acceptes += int(d["accepte"])
            positifs += int(e.attendu)
            for table, cle in ((par_tache, e.tache),
                               (par_condition, e.condition),
                               (par_transition, e.transition),
                               (par_croise, (e.condition, e.transition))):
                table[cle]["n"] += 1
                table[cle]["corrects"] += int(correct)
            par_tache[e.tache]["acceptes"] += int(d["accepte"])
            sonde = (e.texte, e.jeu, empreinte_code(e.cible_code), e.cible_langue)
            par_sonde[e.tache][sonde]["n"] += 1
            par_sonde[e.tache][sonde]["corrects"] += int(correct)

        def exact(x):
            return x["corrects"] / x["n"] if x["n"] else 0.0

        for table in (par_tache, par_condition, par_transition, par_croise):
            for x in table.values():
                x["exact"] = exact(x)
        effet_conflit = exact(par_condition["incongruent"]) - exact(par_condition["congruent"])
        effet_commutation = (exact(par_transition["commutation"])
                             - exact(par_transition["repetition"]))
        macro_sonde = {}
        for tache in TACHES:
            vals = [exact(x) for x in par_sonde[tache].values()]
            macro_sonde[tache] = {"n_sondes": len(vals),
                                  "exact": sum(vals) / len(vals) if vals else 0.0}
        # interaction : la commutation coûte-t-elle plus sous conflit ?
        effet_commutation_congruent = (exact(par_croise[("congruent", "commutation")])
                                       - exact(par_croise[("congruent", "repetition")]))
        effet_commutation_incongruent = (
            exact(par_croise[("incongruent", "commutation")])
            - exact(par_croise[("incongruent", "repetition")]))
        return {
            "exact": ok / n if n else 0.0, "n": n, "acceptes": acceptes,
            "positifs": positifs,
            "taux_base_tout_non": (n - positifs) / n if n else 0.0,
            "par_tache": par_tache, "par_condition": par_condition,
            "par_transition": par_transition,
            "par_croise": {f"{c}_{t}": x for (c, t), x in par_croise.items()},
            "par_sonde": macro_sonde,
            "effet_conflit": effet_conflit,
            "effet_commutation": effet_commutation,
            "effet_commutation_congruent": effet_commutation_congruent,
            "effet_commutation_incongruent": effet_commutation_incongruent,
            "interaction_conflit_commutation": (effet_commutation_incongruent
                                                - effet_commutation_congruent),
            "effet_tache_langue": (exact(par_tache["langue"])
                                   - exact(par_tache["sens"])),
            "effet_tache_langue_macro": (macro_sonde["langue"]["exact"]
                                         - macro_sonde["sens"]["exact"]),
        }

    def executer_switch(self, items=None, cibles=("fr", "en")) -> dict:
        """Exécute la tâche de commutation et rend les coûts mesurés.

        La porte dure `tache` est comparée à ses témoins et au contrôle positif
        `perseveration_tache`. Aucune clé n'est partagée avec `executer` : la
        batterie M6 continue de mesurer la tâche de confluence.
        """
        essais = self.tache_switch(items, cibles)
        if not essais:
            return {"exact": 0.0, "n": 0, "effet_conflit": 0.0,
                    "effet_commutation": 0.0, "politique": "tache"}
        resultat = self._metriques_switch(self._decisions_switch(essais, "tache"))
        resultat.update({
            "politique": "tache", "cibles": list(cibles),
            "n_commutations": resultat["par_transition"]["commutation"]["n"],
            "n_repetitions": resultat["par_transition"]["repetition"]["n"],
            "politiques": {},
            "controles": {},
        })
        for politique in ("sens", "langue", "tache_inversee",
                          "indice_aleatoire", "tout_non"):
            r = self._metriques_switch(self._decisions_switch(essais, politique))
            resultat["politiques"][politique] = {
                "exact": r["exact"], "effet_conflit": r["effet_conflit"],
                "effet_commutation": r["effet_commutation"],
            }
        persev = self._metriques_switch(
            self._decisions_switch(essais, "perseveration_tache"))
        resultat["controles"]["perseveration_tache"] = {
            "exact": persev["exact"],
            "effet_conflit": persev["effet_conflit"],
            "effet_commutation": persev["effet_commutation"],
            "effet_commutation_congruent": persev["effet_commutation_congruent"],
            "effet_commutation_incongruent": persev["effet_commutation_incongruent"],
            "interaction_conflit_commutation": persev["interaction_conflit_commutation"],
        }
        resultat["controle_perseveration"] = persev["effet_commutation"]
        return resultat

    # ------------------------------------------------------------------
    # Politiques et mesures.
    # ------------------------------------------------------------------
    def _decisions(self, essais, politique: str = "conjonction",
                   langues_forcees: list[str | None] | None = None) -> list[dict]:
        decisions = []
        for i, essai in enumerate(essais):
            code = self.lire(essai.texte, essai.jeu, essai.contexte)
            langue = self.langue(essai.texte)
            forcee = langues_forcees[i] if langues_forcees is not None else None
            if politique == "conjonction":
                accepte = code == essai.cible_code and langue == essai.cible_langue
            elif politique == "langue":
                accepte = langue == essai.cible_langue
            elif politique == "sens":
                accepte = code == essai.cible_code
            elif politique == "perseveration":
                reference = forcee if forcee is not None else essai.cible_langue
                accepte = code == essai.cible_code and langue == reference
            elif politique == "tout_non":
                accepte = False
            else:
                raise ValueError(f"politique inconnue : {politique!r}")
            decisions.append({"accepte": bool(accepte), "code": code,
                              "langue": langue, "essai": essai})
        return decisions

    @staticmethod
    def _metriques(decisions) -> dict:
        tp = fp = fn = tn = 0
        par_condition: dict[str, dict] = {}
        par_langue: dict[str, dict] = {}
        for d in decisions:
            essai = d["essai"]
            attendu, accepte = essai.attendu, d["accepte"]
            if attendu and accepte:
                tp += 1
            elif attendu:
                fn += 1
            elif accepte:
                fp += 1
            else:
                tn += 1
            c = par_condition.setdefault(essai.condition, {"n": 0, "corrects": 0, "acceptes": 0})
            c["n"] += 1
            c["corrects"] += int(accepte == attendu)
            c["acceptes"] += int(accepte)
            l = par_langue.setdefault(essai.cible_langue, {"n": 0, "corrects": 0,
                                                           "tp": 0, "fn": 0})
            l["n"] += 1
            l["corrects"] += int(accepte == attendu)
            if attendu:
                l["tp"] += int(accepte)
                l["fn"] += int(not accepte)
        n = tp + fp + fn + tn
        sensibilite = tp / (tp + fn) if (tp + fn) else 0.0
        specificite = tn / (tn + fp) if (tn + fp) else 0.0
        for c in par_condition.values():
            c["exact"] = c["corrects"] / c["n"] if c["n"] else 0.0
        for l in par_langue.values():
            l["exact"] = l["corrects"] / l["n"] if l["n"] else 0.0
            l["sensibilite"] = l["tp"] / (l["tp"] + l["fn"]) if (l["tp"] + l["fn"]) else 0.0
        return {
            "exact": (tp + tn) / n if n else 0.0,
            "n": n, "vrais_positifs": tp, "faux_positifs": fp,
            "faux_negatifs": fn, "vrais_negatifs": tn,
            "sensibilite": sensibilite, "specificite": specificite,
            "exactitude_equilibree": (sensibilite + specificite) / 2,
            "mcc": _mcc(tp, fp, fn, tn),
            "sensibilite_ic95": _wilson(tp, tp + fn),
            "specificite_ic95": _wilson(tn, tn + fp),
            "taux_base_tout_non": (tn + fp) / n if n else 0.0,
            "par_condition": par_condition, "par_langue": par_langue,
        }

    def _canal_diagnostic(self, essais) -> dict:
        """Fiabilité des deux canaux sur les surfaces **uniques**.

        On mesure sur les couples (surface, langue) : une surface identique en
        fr et en en compte deux, et aucun canal ne peut réussir les deux. C'est
        le plafond d'identifiabilité du corpus, pas une faute de la porte.
        """
        paires = {}
        lectures = {}
        for essai in essais:
            paires[(essai.texte, essai.langue_vraie)] = essai.langue_vraie
            lectures[(essai.texte, essai.jeu)] = essai.code_vrai
        langue_ok = sum(1 for (texte, vraie) in paires
                        if self.langue(texte) == vraie)
        lecture_ok = sum(1 for (texte, jeu), code in lectures.items()
                         if self.lire(texte, jeu, next(
                             (e.contexte for e in essais
                              if e.texte == texte and e.jeu == jeu), None)) == code)
        # codes dont les surfaces sont identiques dans toutes les langues cibles
        # (les essais « go » portent le code cible dans la langue cible)
        go = [e for e in essais if e.condition == "go"]
        textes_par_code: dict[str, set[str]] = defaultdict(set)
        for e in go:
            textes_par_code[empreinte_code(e.cible_code)].add(e.texte)
        ambigus = sorted({texte for textes in textes_par_code.values()
                          if len(textes) == 1 for texte in textes})
        return {"langue_n": len(paires), "langue_exact": langue_ok / len(paires) if paires else 0.0,
                "lecture_n": len(lectures), "lecture_exact": lecture_ok / len(lectures) if lectures else 0.0,
                "surfaces_ambigues": ambigus}

    def _cout_commutation(self, essais, politique: str = "conjonction") -> dict:
        """Coût de commutation **apparié** (mêmes stimuli après switch/repeat).

        Chaque bloc (code cible × langue cible) est rejoué deux fois de suite :
        le premier passage suit la langue du bloc précédent, le second répète sa
        propre langue. La comparaison se fait donc à composition identique. Un
        contrôle positif `perseveration` réutilise la langue précédente : si
        l'instrument est sensible à une mémoire, il doit le voir.
        """
        if not essais or len(essais) % len(CONDITIONS) != 0:
            return {"cout": 0.0, "n_commutations": 0, "n_repetitions": 0,
                    "erreur_commutation": 0.0, "erreur_repetition": 0.0}
        blocs = [essais[i:i + len(CONDITIONS)] for i in range(0, len(essais), len(CONDITIONS))]
        rejoues = []
        for bloc in blocs:
            rejoues.append(bloc)
            rejoues.append(bloc)  # répétition appariée du même bloc
        erreurs = []
        precedente = None
        classes = []
        for k, bloc in enumerate(rejoues):
            langue_bloc = bloc[0].cible_langue
            # Les deux premiers passages forment la paire initiale : le premier
            # n'a pas de contexte de commutation, le second est sa répétition
            # appariée. On les exclut tous deux pour que switch et repeat
            # portent exactement les mêmes stimuli.
            if k < 2 or precedente is None:
                classes.append("sans_precedent")
            elif precedente != langue_bloc:
                classes.append("commutation")
            else:
                classes.append("repetition")
            forcees = [precedente] * len(bloc) if politique == "perseveration" else None
            decisions = self._decisions(bloc, politique, forcees)
            erreurs.append(sum(int(d["accepte"] != d["essai"].attendu) for d in decisions)
                           / len(bloc))
            precedente = langue_bloc
        def moyenne(classe):
            vals = [e for e, c in zip(erreurs, classes) if c == classe]
            return sum(vals) / len(vals) if vals else 0.0
        return {"cout": moyenne("commutation") - moyenne("repetition"),
                "n_commutations": classes.count("commutation"),
                "n_repetitions": classes.count("repetition"),
                "erreur_commutation": moyenne("commutation"),
                "erreur_repetition": moyenne("repetition")}

    # ------------------------------------------------------------------
    # Le point d'entrée (compatible avec `batterie.m6`).
    # ------------------------------------------------------------------
    def executer(self, items=None, cibles=("fr", "en")) -> dict:
        """Exécute la tâche de conflit et rend toutes les mesures.

        Les clés historiques (`exact`, `faux_positifs`, `faux_negatifs`, `n`,
        `cout_commutation`) sont conservées telles quelles pour la batterie.
        """
        essais = self.tache_conflit(items, cibles)
        if not essais:
            return {"exact": 0.0, "faux_positifs": 0, "faux_negatifs": 0,
                    "n": 0, "cout_commutation": 0.0, "politique": "conjonction"}
        decisions = self._decisions(essais, "conjonction")
        mesures = self._metriques(decisions)
        # les trois contrôles de politique : un seul canal ne suffit pas
        politiques = {}
        for politique in ("langue", "sens", "tout_non"):
            politiques[politique] = self._metriques(
                self._decisions(essais, politique))
        cout = self._cout_commutation(essais, "conjonction")
        cout_persev = self._cout_commutation(essais, "perseveration")
        mesures.update({
            "politique": "conjonction",
            "cibles": list(cibles),
            "cout_commutation": cout["cout"],
            "cout_commutation_details": cout,
            "controle_perseveration": cout_persev["cout"],
            "politiques": {nom: {"exact": p["exact"],
                                 "faux_positifs": p["faux_positifs"],
                                 "faux_negatifs": p["faux_negatifs"],
                                 "sensibilite": p["sensibilite"],
                                 "specificite": p["specificite"],
                                 "exactitude_equilibree": p["exactitude_equilibree"]}
                           for nom, p in politiques.items()},
            "canaux": self._canal_diagnostic(essais),
        })
        return mesures

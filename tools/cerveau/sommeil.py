#!/usr/bin/env python3
"""M8 — sommeil : consolider des épisodes en prototypes, et mesurer ce que cela vaut.

Le module d'origine groupait par ``(jeu, action)`` et prenait le mode **champ par
champ**. Le score publié, 96,48 % sur 106 épisodes de test, est réel mais il est
mal lu :

- les champs sont **dominés par ``None``** : 12 des 15 champs ont plus de 98 %
  d'exactitude agrégée parce que la bonne réponse y est presque toujours
  ``None``. Sur les valeurs non nulles, la précision tombe à ~84 % sur tout le
  corpus (~86 % sur la queue), et les trois champs porteurs (``de``, ``vers``,
  ``carte``) sont à ~50 %, ~50 % et ~22–28 % conditionnellement.
- le score **exact** n'est pas 0 % : il vaut 65,1 % sur la queue, 24,1 % sur les
  29 codes uniques. La « baseline 0,0 » du rapport était l'absence de mémoire,
  pas un prédicteur.
- groupé par ``(jeu)`` seul, le prototype fait déjà 96,10 % : le groupe
  ``(jeu, action)`` n'ajoute que +0,38 point. Le score vient du jeu, pas de
  l'action.
- sur des **codes jamais vus**, le prototype ne peut pas produire le bon code :
  l'exact est 0 % par construction. Un prototype est une marginale, pas une
  généralisation.

Le module ajoute donc : prototypes joints, prototypes par type de code,
baselines explicites (global, par jeu, groupes mélangés, hasard), évaluation
dédupliquée par code et par paire, split par codes tenus à l'écart, et un
**hybride prototypes + épisodes** (récupération exacte si le code a été vu,
repli sur le prototype sinon). L'hybride porte l'exact à 100 % sur la queue,
mais uniquement parce que les 106 codes y ont été vus : c'est M4 qui travaille,
pas la consolidation.

**Passe A7 (M8 conditionné par le contexte).** ``experience_contexte`` mesure la
question laissée ouverte : jeu, action et type de coup suffisent-ils, et
« prototype + épisode » aide-t-il sur un code tenu à l'écart ? Résultats
reproductibles sur le corpus (29 codes, 528 items) :

- en *leave-one-code-out*, l'exact d'un prototype est **nul par construction** —
  il ne peut sortir qu'un code déjà vu, et le code exclu n'est pas dans le
  train. Ce n'est pas une mesure, c'est une preuve ;
- la seule partie gagnée sur un code neuf est le **motif de ``None``** : la clé
  ``jeu`` porte les champs à 89,20 %, le backoff ``type→groupe→jeu→global`` à
  90,11 %, mais les champs non nuls ne passent que de 61,26 % à 63,51 %, dont
  l'essentiel vient de ``jeu``/``action``/``taille`` (déjà connus par la clé) ;
  les coordonnées du coup (``de``, ``vers``, ``point``, ``carte``, ``case``,
  ``chemin``) sont à 0 % hors coïncidences de marginale ;
- conditionner plus finement que ``(jeu, action)`` **n'aide pas** : le type
  seul perd 0,23 pt de champs et 2,2 pts de non nuls ; le backoff ne récupère
  que la structure ;
- l'hybride historique est **tautologique** (index clé par le code cible
  entier) ; un hybride honnête se clé par la **surface** et ne couvre alors que
  les surfaces déjà vues, soit 0 % sur un code tenu à l'écart.

Le négatif est donc net : la consolidation est une marginale du contexte, elle
ne remplace pas la lecture de la surface (M2/M5). ``experience`` reste
l'expérience publiée ; ``experience_contexte`` est le contrôle conditionné.
"""
from __future__ import annotations

import collections
import random

from semantique.universaux import CHAMPS

NOMS = tuple(nom for nom, _ in CHAMPS)
CLES = ("global", "jeu", "groupe", "type", "jeu_type", "action_type", "type_seul")
LADDER = ("type", "groupe", "jeu", "global")


def _code(e) -> dict:
    c = getattr(e, "code", None)
    return dict(c) if c is not None else dict(e)


def _signature(code: dict) -> tuple:
    return tuple(sorted(nom for nom in NOMS if code.get(nom) is not None))


def _cle(code: dict, cle) -> tuple:
    if callable(cle):
        return cle(code)
    if cle == "type":
        return (code.get("jeu"), code.get("action"), _signature(code))
    if cle == "jeu_type":
        return (code.get("jeu"), _signature(code))
    if cle == "action_type":
        return (code.get("action"), _signature(code))
    if cle == "type_seul":
        return (_signature(code),)
    if cle == "jeu":
        return (code.get("jeu"),)
    if cle == "global":
        return ("global",)
    return (code.get("jeu"), code.get("action"))


def _mode_champs(codes) -> dict:
    proto = {}
    for nom in NOMS:
        vals = [c.get(nom) for c in codes]
        proto[nom] = collections.Counter(vals).most_common(1)[0][0]
    return proto


def _mode_joint(codes) -> dict:
    t = collections.Counter(tuple(sorted(c.items())) for c in codes).most_common(1)[0][0]
    return dict(t)


class Sommeil:
    nom = "M8-sommeil"

    # ---- consolidation ---------------------------------------------------
    def consolider(self, episodes, mode: str = "champs", cle="groupe") -> dict:
        """Compacte les épisodes en prototypes.

        ``mode`` : ``champs`` (mode par champ), ``joint`` (code complet le plus
        fréquent), ``type`` (même chose, mais la clé inclut la signature des
        champs non nuls).
        """
        groupes = collections.defaultdict(list)
        for e in episodes:
            code = _code(e)
            groupes[_cle(code, cle)].append(code)
        protos = {}
        for k, codes in groupes.items():
            if not codes:
                continue
            protos[k] = _mode_joint(codes) if mode == "joint" else _mode_champs(codes)
        return protos

    # ---- évaluation ------------------------------------------------------
    def evaluer(self, episodes, prototypes, cle="groupe", fallback=None) -> dict:
        ok = ex = n = n_inconnus = 0
        ok_nn = n_nn = 0
        for e in episodes:
            code = _code(e)
            proto = prototypes.get(_cle(code, cle))
            if proto is None and fallback:
                for k in (_cle(code, "groupe"), _cle(code, "jeu"), ("global",)):
                    proto = fallback.get(k)
                    if proto is not None:
                        break
            if proto is None:
                n_inconnus += 1
                n += 1
                continue
            n += 1
            ok += sum(1 for nom in NOMS if proto.get(nom) == code.get(nom))
            ex += int(proto == code)
            for nom in NOMS:
                if code.get(nom) is not None:
                    n_nn += 1
                    ok_nn += int(proto.get(nom) == code.get(nom))
        return {"champs": ok / max(1, n * len(NOMS)), "exact": ex / max(1, n),
                "champs_non_nuls": ok_nn / max(1, n_nn),
                "n": n, "n_inconnus": n_inconnus, "n_champs_non_nuls": n_nn,
                "prototypes": len(prototypes)}

    # ---- détail par champ ------------------------------------------------
    def par_champ(self, episodes, prototypes, cle="groupe", fallback=None) -> dict:
        out = {}
        for nom in NOMS:
            n = total = 0
            for e in episodes:
                code = _code(e)
                if code.get(nom) is None:
                    continue
                proto = prototypes.get(_cle(code, cle))
                if proto is None and fallback:
                    for k in (_cle(code, "groupe"), _cle(code, "jeu"), ("global",)):
                        proto = fallback.get(k)
                        if proto is not None:
                            break
                if proto is None:
                    continue
                total += 1
                n += int(proto.get(nom) == code.get(nom))
            out[nom] = {"n_non_nul": total,
                        "exact_non_nul": n / max(1, total)}
        return out

    # ---- baselines -------------------------------------------------------
    def baselines(self, train, test) -> dict:
        codes = [_code(e) for e in train]
        glob = {("global",): _mode_champs(codes)}
        jeux = collections.defaultdict(list)
        groupes = collections.defaultdict(list)
        types = collections.defaultdict(list)
        for c in codes:
            jeux[(c.get("jeu"),)].append(c)
            groupes[(c.get("jeu"), c.get("action"))].append(c)
            types[(c.get("jeu"), c.get("action"), _signature(c))].append(c)
        baselines = {}
        baselines["global"] = self.evaluer(
            test, glob, cle="global")
        baselines["par_jeu"] = self.evaluer(
            test, {k: _mode_champs(v) for k, v in jeux.items()},
            cle="jeu", fallback=glob)
        baselines["par_groupe"] = self.evaluer(
            test, {k: _mode_champs(v) for k, v in groupes.items()},
            cle="groupe", fallback={**glob, **{k: _mode_champs(v) for k, v in jeux.items()}})
        baselines["par_type"] = self.evaluer(
            test, {k: _mode_champs(v) for k, v in types.items()},
            cle="type", fallback={**glob, **{k: _mode_champs(v) for k, v in groupes.items()}})
        baselines["joint"] = self.evaluer(
            test, {k: _mode_joint(v) for k, v in groupes.items()},
            cle="groupe", fallback={**glob, **{k: _mode_champs(v) for k, v in jeux.items()}})
        # groupes mélangés : la clé ne porte plus l'information
        rng = random.Random(7)
        labels = [k for k, v in groupes.items() for _ in v]
        rng.shuffle(labels)
        melanges = collections.defaultdict(list)
        for code, lab in zip(codes, labels):
            melanges[lab].append(code)
        baselines["groupes_melanges"] = self.evaluer(
            test, {k: _mode_champs(v) for k, v in melanges.items()},
            cle="groupe", fallback=glob)
        # hasard : un code du train tiré pour chaque groupe
        rng = random.Random(11)
        hasard = {k: dict(rng.choice(v)) for k, v in groupes.items()}
        baselines["hasard"] = self.evaluer(
            test, hasard, cle="groupe", fallback=glob)
        # plafond triché : prototype par paire (l'étiquette paire n'est pas
        # disponible au test, c'est une borne supérieure, pas une baseline)
        paires = collections.defaultdict(list)
        for e in train:
            paires[getattr(e, "paire", "")].append(_code(e))
        protos_paires = {k: _mode_joint(v) for k, v in paires.items()}
        ok = ex = n = 0
        for e in test:
            code = _code(e)
            proto = protos_paires.get(getattr(e, "paire", ""))
            if proto is None:
                continue
            n += 1
            ok += sum(1 for nom in NOMS if proto.get(nom) == code.get(nom))
            ex += int(proto == code)
        baselines["plafond_par_paire"] = {
            "champs": ok / max(1, n * len(NOMS)), "exact": ex / max(1, n),
            "n": n, "prototypes": len(protos_paires)}
        return baselines

    # ---- hybride prototypes + épisodes -----------------------------------
    def index_episodes(self, episodes) -> dict:
        index = {}
        for e in episodes:
            code = _code(e)
            index.setdefault(tuple(sorted(code.items())), code)
        return index

    def evaluer_hybride(self, episodes, prototypes, index, cle="groupe",
                        fallback=None) -> dict:
        ok = ex = n = couverts = ex_c = champs_c = 0
        ex_nc = champs_nc = n_nc = 0
        for e in episodes:
            code = _code(e)
            k = tuple(sorted(code.items()))
            n += 1
            if k in index:
                proto = index[k]
                couverts += 1
                ex += 1
                ex_c += 1
                ok += len(NOMS)
                champs_c += len(NOMS)
                continue
            proto = prototypes.get(_cle(code, cle))
            if proto is None and fallback:
                for kk in (_cle(code, "groupe"), _cle(code, "jeu"), ("global",)):
                    proto = fallback.get(kk)
                    if proto is not None:
                        break
            if proto is None:
                n_nc += 1
                continue
            n_nc += 1
            g = sum(1 for nom in NOMS if proto.get(nom) == code.get(nom))
            ok += g
            champs_nc += g
            ex_nc += int(proto == code)
        return {"champs": ok / max(1, n * len(NOMS)), "exact": ex / max(1, n),
                "couverture": couverts / max(1, n), "n": n, "couverts": couverts,
                "exact_sur_couverts": ex_c / max(1, couverts),
                "champs_sur_couverts": champs_c / max(1, couverts * len(NOMS)),
                "exact_sur_non_couverts": ex_nc / max(1, n_nc),
                "champs_sur_non_couverts": champs_nc / max(1, n_nc * len(NOMS)),
                "n_non_couverts": n_nc}

    # ---- déduplication ---------------------------------------------------
    @staticmethod
    def dedupliquer(episodes, par: str = "code") -> list:
        vus = set()
        out = []
        for e in episodes:
            if par == "paire":
                k = getattr(e, "paire", "")
            elif par == "surface":
                k = getattr(e, "texte", getattr(e, "surface", ""))
            else:
                k = tuple(sorted(_code(e).items()))
            if k in vus:
                continue
            vus.add(k)
            out.append(e)
        return out

    # ---- expérience complète ---------------------------------------------
    def experience(self, items_=None, graines=(1, 2, 3)) -> dict:
        from semantique.typed_corpus import decouper, items as corpus_items
        its = list(items_) if items_ is not None else corpus_items()
        n = int(len(its) * 0.8)
        train, test = its[:n], its[n:]
        protos = self.consolider(train)
        base = self.baselines(train, test)
        codes_tr = [_code(e) for e in train]
        glob = {("global",): _mode_champs(codes_tr)}
        jeux = collections.defaultdict(list)
        for c in codes_tr:
            jeux[(c.get("jeu"),)].append(c)
        fallback = {**glob, **{k: _mode_champs(v) for k, v in jeux.items()}}
        queue = {
            "module_champs": self.evaluer(test, protos),
            "module_joint": self.evaluer(
                test, self.consolider(train, mode="joint")),
            "module_type": self.evaluer(
                test, self.consolider(train, mode="champs", cle="type"),
                cle="type", fallback=fallback),
            "baselines": base,
            "dedup_code": self.evaluer(self.dedupliquer(test), protos),
            "dedup_paire": self.evaluer(self.dedupliquer(test, "paire"), protos),
            "hybride": self.evaluer_hybride(test, protos, self.index_episodes(train)),
        }
        # les 29 codes uniques, évalués une fois chacun
        dedup_tout = self.dedupliquer(its)
        global_tout = {"global": self.evaluer(
            dedup_tout, {("global",): _mode_champs([_code(e) for e in its])},
            cle="global")}
        dedup_tout_res = self.evaluer(dedup_tout, protos)
        # codes tenus à l'écart : le test ne contient que des codes jamais vus
        codes = sorted({tuple(sorted(_code(e).items())) for e in its}, key=repr)
        resultats_codes = []
        for g in graines:
            rng = random.Random(g)
            mel = list(codes)
            rng.shuffle(mel)
            nv = max(1, int(len(mel) * 0.2))
            exclus = set(mel[:nv])
            tr = [e for e in its if tuple(sorted(_code(e).items())) not in exclus]
            te = [e for e in its if tuple(sorted(_code(e).items())) in exclus]
            p = self.consolider(tr)
            resultats_codes.append({
                "graine": g, "n_train": len(tr), "n_test": len(te),
                "codes_exclus": len(exclus),
                "module": self.evaluer(te, p),
                "baselines": self.baselines(tr, te),
                "hybride": self.evaluer_hybride(te, p, self.index_episodes(tr)),
            })
        # paires tenues à l'écart (le split de typed_corpus)
        resultats_paires = []
        for g in graines:
            tr, te = decouper(its, g, 0.2)
            p = self.consolider(tr)
            codes_tr = {tuple(sorted(_code(e).items())) for e in tr}
            novel = sum(1 for e in te if tuple(sorted(_code(e).items())) not in codes_tr)
            resultats_paires.append({
                "graine": g, "n_train": len(tr), "n_test": len(te),
                "codes_nouveaux": novel,
                "module": self.evaluer(te, p),
                "baselines": self.baselines(tr, te),
                "hybride": self.evaluer_hybride(te, p, self.index_episodes(tr)),
            })
        # contrôle : les champs dominés par None
        codes_its = [_code(e) for e in its]
        valeurs = {nom: len({c.get(nom) for c in codes_its}) for nom in NOMS}
        taux_none = {nom: sum(1 for c in codes_its if c.get(nom) is None) / len(its)
                     for nom in NOMS}
        constants = [nom for nom, k in valeurs.items() if k == 1]
        quasi_none = [nom for nom, k in taux_none.items() if k >= 0.9]
        queue["par_champ"] = self.par_champ(test, protos)
        res = {
            "protocole": {
                "n": len(its), "train": len(train), "test": len(test),
                "prototypes": len(protos), "codes_uniques": len(codes),
                "champs_constants": constants,
                "champs_quasi_none": quasi_none,
                "champs_variables": [nom for nom in NOMS if nom not in constants],
                "valeurs_par_champ": valeurs,
                "taux_none_par_champ": taux_none,
            },
            "queue": queue,
            "dedup_tout": {"module": dedup_tout_res, **global_tout},
            "codes_nouveaux": resultats_codes,
            "paires": resultats_paires,
        }
        q = queue
        m = q["module_champs"]
        res["verdict"] = {
            "champs_96_48_reproduit": abs(m["champs"] - 0.9647798742138365) < 1e-12,
            "exact_queue": m["exact"],
            "exact_annonce_0_est_faux": m["exact"] > 0.0,
            "gain_sur_par_jeu_champs": m["champs"] - q["baselines"]["par_jeu"]["champs"],
            "gain_sur_par_jeu_exact": m["exact"] - q["baselines"]["par_jeu"]["exact"],
            "champs_non_nuls": m["champs_non_nuls"],
            "exact_codes_uniques": dedup_tout_res["exact"],
            "exact_codes_nouveaux": [r["module"]["exact"] for r in resultats_codes],
            "hybride_exact_queue": q["hybride"]["exact"],
            "hybride_couverture_queue": q["hybride"]["couverture"],
            "hybride_exact_codes_nouveaux": [r["hybride"]["exact"] for r in resultats_codes],
            "baseline_globale_champs": q["baselines"]["global"]["champs"],
            "baseline_globale_exact": q["baselines"]["global"]["exact"],
            "groupes_melanges_champs": q["baselines"]["groupes_melanges"]["champs"],
        }
        return res

    # ---- A7 : prototypes conditionnés, tenue à l'écart, hybrides honnêtes ---
    @staticmethod
    def _groupes(episodes, cle):
        groupes = collections.defaultdict(list)
        for e in episodes:
            groupes[_cle(_code(e), cle)].append(_code(e))
        return groupes

    @classmethod
    def _prototypes(cls, episodes, cle, mode: str = "champs"):
        """Prototypes d'une clé, avec le support (nombre d'épisodes du groupe)."""
        protos, supports = {}, {}
        for k, codes in cls._groupes(episodes, cle).items():
            if not codes:
                continue
            protos[k] = _mode_joint(codes) if mode == "joint" else _mode_champs(codes)
            supports[k] = len(codes)
        return protos, supports

    def prototypes_multi(self, episodes, cles=CLES, mode: str = "champs") -> dict:
        """Un couple (prototypes, supports) par clé, construit sur le même train."""
        return {cle: self._prototypes(episodes, cle, mode) for cle in cles}

    @staticmethod
    def _predire(code, protos_par_cle, ladder=LADDER, min_support: int = 1):
        """Prédit champ par champ en descendant l'échelle du plus fin au plus gros.

        Un champ prend la valeur du premier prototype dont le groupe existe et
        compte au moins ``min_support`` épisodes. Le niveau retenu est renvoyé :
        il mesure la part du fin qui sert réellement.
        """
        protos_g, supports_g = protos_par_cle.get("global", ({}, {}))
        global_proto = protos_g.get(("global",), {})
        pred = {}
        niveaux = collections.Counter()
        for nom in NOMS:
            valeur, niveau = None, "absent"
            for cle in ladder:
                protos, supports = protos_par_cle.get(cle, ({}, {}))
                k = _cle(code, cle)
                if k in protos and supports.get(k, 0) >= min_support:
                    valeur, niveau = protos[k].get(nom), cle
                    break
            if niveau == "absent":
                valeur, niveau = global_proto.get(nom), "global_absent"
            pred[nom] = valeur
            niveaux[niveau] += 1
        return pred, niveaux

    def evaluer_profond(self, episodes, protos_par_cle, ladder=LADDER,
                        min_support: int = 1) -> dict:
        """Évalue avec backoff et décompose champs nuls / non nuls.

        L'exact ne compare que les champs présents dans le code cible, pour que
        les codes partiels des tests unitaires restent évaluables.
        """
        ok = ex = n = 0
        ok_nn = n_nn = ok_nul = n_nul = 0
        par_champ = collections.defaultdict(
            lambda: {"n_non_nul": 0, "ok_non_nul": 0, "n_nul": 0, "ok_nul": 0})
        niveaux = collections.Counter()
        for e in episodes:
            code = _code(e)
            pred, niv = self._predire(code, protos_par_cle, ladder, min_support)
            niveaux.update(niv)
            n += 1
            ex += int(all(pred.get(nom) == code.get(nom) for nom in code))
            for nom in NOMS:
                bon = int(pred.get(nom) == code.get(nom))
                ok += bon
                d = par_champ[nom]
                if code.get(nom) is None:
                    n_nul += 1
                    ok_nul += bon
                    d["n_nul"] += 1
                    d["ok_nul"] += bon
                else:
                    n_nn += 1
                    ok_nn += bon
                    d["n_non_nul"] += 1
                    d["ok_non_nul"] += bon
        return {
            "champs": ok / max(1, n * len(NOMS)),
            "exact": ex / max(1, n),
            "champs_non_nuls": ok_nn / max(1, n_nn),
            "champs_nuls": ok_nul / max(1, n_nul),
            "n": n, "n_non_nuls": n_nn, "n_nuls": n_nul,
            "niveaux_utilises": dict(niveaux),
            "bruts": {"ok_champs": ok, "n_champs": n * len(NOMS),
                      "ok_non_nuls": ok_nn, "n_non_nuls": n_nn,
                      "ok_nuls": ok_nul, "n_nuls": n_nul, "exact": ex, "n": n},
            "par_champ": {nom: {
                "n_non_nul": d["n_non_nul"],
                "exact_non_nul": d["ok_non_nul"] / max(1, d["n_non_nul"]),
                "ok_non_nul": d["ok_non_nul"],
                "n_nul": d["n_nul"],
                "exact_nul": d["ok_nul"] / max(1, d["n_nul"]),
                "ok_nul": d["ok_nul"],
            } for nom, d in par_champ.items()},
        }

    @staticmethod
    def _metriques(episodes, predire) -> dict:
        ok = ex = n = ok_nn = n_nn = 0
        for e in episodes:
            code = _code(e)
            pred = predire(e, code)
            n += 1
            ex += int(all(pred.get(nom) == code.get(nom) for nom in code))
            ok += sum(1 for nom in NOMS if pred.get(nom) == code.get(nom))
            for nom in NOMS:
                if code.get(nom) is not None:
                    n_nn += 1
                    ok_nn += int(pred.get(nom) == code.get(nom))
        return {"champs": ok / max(1, n * len(NOMS)), "exact": ex / max(1, n),
                "champs_non_nuls": ok_nn / max(1, n_nn),
                "n": n, "n_non_nuls": n_nn}

    @staticmethod
    def _prototypes_paires(episodes, mode: str = "champs") -> dict:
        groupes = collections.defaultdict(list)
        for e in episodes:
            groupes[getattr(e, "paire", "")].append(_code(e))
        return {k: (_mode_joint(v) if mode == "joint" else _mode_champs(v))
                for k, v in groupes.items()}

    def evaluer_paires(self, episodes, protos, global_proto=None) -> dict:
        """Baseline **oracle** par paire : l'étiquette paire n'est pas une entrée.

        Elle sert de détecteur de fuite : si une paire apparaît des deux côtés,
        le prototype par paire rend le code cible sans rien lire.
        """
        def predire(e, code):
            p = protos.get(getattr(e, "paire", ""))
            return p if p is not None else (global_proto or {})
        return self._metriques(episodes, predire)

    @staticmethod
    def index_surfaces(episodes) -> dict:
        """Index des épisodes par (surface, jeu), la seule clé lisible au test."""
        index = {}
        for e in episodes:
            texte = getattr(e, "texte", getattr(e, "surface", ""))
            code = _code(e)
            index.setdefault((texte, code.get("jeu")), code)
        return index

    def evaluer_hybride_surface(self, episodes, protos_par_cle, index,
                                ladder=LADDER, min_support: int = 1) -> dict:
        """Hybride honnête : mémoire de surface, repli sur le prototype.

        La branche épisodique ne se déclenche que si la **surface** a été vue ;
        c'est la seule information réellement disponible avant de lire le code.
        """
        n = couverts = ex = ex_c = ex_nc = ok = ok_c = ok_nc = 0
        for e in episodes:
            code = _code(e)
            texte = getattr(e, "texte", getattr(e, "surface", ""))
            k = (texte, code.get("jeu"))
            n += 1
            if k in index:
                pred = index[k]
                couverts += 1
                bon = sum(1 for nom in NOMS if pred.get(nom) == code.get(nom))
                ok += bon
                ok_c += bon
                ex_c += int(all(pred.get(nom) == code.get(nom) for nom in code))
                ex += int(all(pred.get(nom) == code.get(nom) for nom in code))
                continue
            pred, _ = self._predire(code, protos_par_cle, ladder, min_support)
            bon = sum(1 for nom in NOMS if pred.get(nom) == code.get(nom))
            ok += bon
            ok_nc += bon
            ex_nc += int(all(pred.get(nom) == code.get(nom) for nom in code))
            ex += int(all(pred.get(nom) == code.get(nom) for nom in code))
        n_nc = n - couverts
        return {"champs": ok / max(1, n * len(NOMS)), "exact": ex / max(1, n),
                "couverture": couverts / max(1, n), "n": n,
                "n_couverts": couverts, "n_non_couverts": n_nc,
                "exact_sur_couverts": ex_c / max(1, couverts),
                "exact_sur_non_couverts": ex_nc / max(1, n_nc),
                "champs_sur_non_couverts": ok_nc / max(1, n_nc * len(NOMS))}

    @staticmethod
    def plafond_contextuel(episodes, cles=CLES) -> dict:
        """Masse du code modal par clé : plafond d'exact d'un prédicteur contextuel.

        Sur le corpus entier, aucun modèle qui ne voit que la clé ne peut faire
        mieux que de rendre le code modal de son groupe. La masse modale est donc
        la borne supérieure de l'exact ; ``1 - masse`` est l'irréductible.
        """
        n = len(episodes)
        out = {}
        for cle in cles:
            groupes = Sommeil._groupes(episodes, cle)
            masse = 0
            for codes in groupes.values():
                if codes:
                    masse += collections.Counter(
                        tuple(sorted(c.items())) for c in codes).most_common(1)[0][1]
            out[cle] = {"masse_modale": masse / max(1, n), "groupes": len(groupes)}
        par_paire = collections.defaultdict(list)
        for e in episodes:
            par_paire[getattr(e, "paire", "")].append(_code(e))
        masse = 0
        for codes in par_paire.values():
            if codes:
                masse += collections.Counter(
                    tuple(sorted(c.items())) for c in codes).most_common(1)[0][1]
        out["paire"] = {"masse_modale": masse / max(1, n), "groupes": len(par_paire),
                        "oracle": "l'étiquette paire n'est pas une entrée"}
        return out

    @staticmethod
    def _etiquette_code(code: dict) -> str:
        champs = [nom for nom in NOMS if code.get(nom) is not None]
        return f"{code.get('jeu')}:{code.get('action')}:{'+'.join(champs)}"

    @staticmethod
    def _resume_par_cle(cles: dict, cles_liste=CLES) -> dict:
        out = {}
        for cle in cles_liste:
            acc = {"ok_champs": 0, "n_champs": 0, "ok_non_nuls": 0,
                   "n_non_nuls": 0, "ok_nuls": 0, "n_nuls": 0, "exact": 0, "n": 0}
            for r in cles.values():
                for k in acc:
                    acc[k] += r[cle]["bruts"][k]
            out[cle] = {
                "champs": acc["ok_champs"] / max(1, acc["n_champs"]),
                "exact": acc["exact"] / max(1, acc["n"]),
                "champs_non_nuls": acc["ok_non_nuls"] / max(1, acc["n_non_nuls"]),
                "champs_nuls": acc["ok_nuls"] / max(1, acc["n_nuls"]),
                "n": acc["n"], "n_non_nuls": acc["n_non_nuls"],
            }
        return out

    @staticmethod
    def _controle_cle_permutee(protos, supports, cle, rng) -> tuple:
        """Même nombre de groupes, associations clé→prototype détruites.

        Les prototypes d'un même jeu sont permutés en cycle : toutes les clés
        existent encore, mais aucune ne porte plus l'information de sa clé.
        """
        cles_ = list(protos)
        groupes = collections.defaultdict(list)
        for k in cles_:
            groupes[k[0] if cle in ("jeu", "groupe", "type") else "tous"].append(k)
        perm = {}
        fixes = 0
        for membres in groupes.values():
            if len(membres) < 2:
                for k in membres:
                    perm[k] = protos[k]
                fixes += len(membres)
                continue
            valeurs = [protos[k] for k in membres]
            decale = valeurs[1:] + valeurs[:1]
            for k, v in zip(membres, decale):
                perm[k] = v
        return (perm, supports), fixes

    def experience_contexte(self, items_=None, graines=(1, 2, 3)) -> dict:
        """M8 conditionné : jeu, action, type de coup, et code tenu à l'écart.

        Trois protocoles, tous les prototypes construits **sans** le code testé :

        1. ``leave-one-code-out`` : 29 plis, un code exclu par pli, évalué une
           fois (moyenne par code, non pondérée par la fréquence des surfaces) ;
        2. ``codes_tenus`` : 3 graines, 20 % des codes exclus par jeu, évaluation
           pondérée par les items et par code ;
        3. ``paires_tenues`` : le split historique ``decouper`` par paire, avec
           le contrôle de fuite ``codes_test_vus_dans_train``.

        L'exact y est nul **par construction** (un prototype ne sort qu'un code
        vu, le code exclu n'est pas dans le train) : la mesure utile est la
        décomposition champs / non nuls / nuls et le backoff par champ.
        """
        from semantique.typed_corpus import decouper, items as corpus_items
        its = list(items_) if items_ is not None else corpus_items()
        n = len(its)
        codes = sorted({tuple(sorted(_code(e).items())) for e in its}, key=repr)
        par_jeu = collections.defaultdict(list)
        for t in codes:
            par_jeu[dict(t).get("jeu")].append(t)
        plafond = self.plafond_contextuel(its, CLES)

        # ---- 1. leave-one-code-out --------------------------------------
        loo = {cle: {"champs": [], "exact": [], "champs_non_nuls": [],
                     "champs_nuls": [], "n": 0} for cle in CLES}
        loo["ladder"] = {"champs": [], "exact": [], "champs_non_nuls": [],
                         "champs_nuls": [], "n": 0}
        par_champ_loo = collections.defaultdict(
            lambda: {"n_non_nul": 0, "ok_non_nul": 0, "n_nul": 0, "ok_nul": 0})
        par_champ_jeu = collections.defaultdict(
            lambda: {"n_non_nul": 0, "ok_non_nul": 0})
        niveaux_loo = collections.Counter()
        for t in codes:
            tr = [e for e in its if tuple(sorted(_code(e).items())) != t]
            te = [e for e in its if tuple(sorted(_code(e).items())) == t][:1]
            pp = self.prototypes_multi(tr)
            for cle in CLES:
                r = self.evaluer_profond(
                    te, {cle: pp[cle], "global": pp["global"]},
                    ladder=(cle, "global"))
                for k in ("champs", "exact", "champs_non_nuls", "champs_nuls"):
                    loo[cle][k].append(r[k])
                loo[cle]["n"] += r["n"]
                if cle == "jeu":
                    for nom, d in r["par_champ"].items():
                        par_champ_jeu[nom]["n_non_nul"] += d["n_non_nul"]
                        par_champ_jeu[nom]["ok_non_nul"] += d["ok_non_nul"]
            r = self.evaluer_profond(te, pp)
            for k in ("champs", "exact", "champs_non_nuls", "champs_nuls"):
                loo["ladder"][k].append(r[k])
            loo["ladder"]["n"] += r["n"]
            niveaux_loo.update(r["niveaux_utilises"])
            for nom, d in r["par_champ"].items():
                par_champ_loo[nom]["n_non_nul"] += d["n_non_nul"]
                par_champ_loo[nom]["ok_non_nul"] += d["ok_non_nul"]
                par_champ_loo[nom]["n_nul"] += d["n_nul"]
                par_champ_loo[nom]["ok_nul"] += d["ok_nul"]
        loo_resume = {}
        for cle in CLES + ("ladder",):
            r = loo[cle]
            m = lambda k: sum(r[k]) / max(1, len(r[k]))
            loo_resume[cle] = {"champs": m("champs"), "exact": m("exact"),
                               "champs_non_nuls": m("champs_non_nuls"),
                               "champs_nuls": m("champs_nuls"), "n": r["n"]}
        loo_resume["ladder"]["niveaux_utilises"] = dict(niveaux_loo)
        loo_resume["ladder"]["par_champ"] = {
            nom: {"n": d["n_non_nul"],
                  "exact_non_nul": d["ok_non_nul"] / max(1, d["n_non_nul"]),
                  "n_nul": d["n_nul"],
                  "exact_nul": d["ok_nul"] / max(1, d["n_nul"])}
            for nom, d in par_champ_loo.items() if d["n_non_nul"]}

        # ---- 2. codes tenus à l'écart, 3 graines -------------------------
        codes_tenus = []
        for g in graines:
            rng = random.Random(g)
            exclus = set()
            for jeu in sorted(par_jeu, key=str):
                mel = list(par_jeu[jeu])
                rng.shuffle(mel)
                k = max(1, round(0.2 * len(mel)))
                exclus.update(mel[:k])
            tr = [e for e in its if tuple(sorted(_code(e).items())) not in exclus]
            te = [e for e in its if tuple(sorted(_code(e).items())) in exclus]
            pp = self.prototypes_multi(tr)
            vus = {tuple(sorted(_code(e).items())) for e in tr}
            row = {
                "graine": g, "n_train": len(tr), "n_test": len(te),
                "n_codes_exclus": len(exclus),
                "codes_exclus": [self._etiquette_code(dict(t))
                                 for t in sorted(exclus, key=repr)],
                "codes_test_vus_dans_train": sum(
                    1 for e in te if tuple(sorted(_code(e).items())) in vus),
                "cles": {cle: self.evaluer_profond(
                    te, {cle: pp[cle], "global": pp["global"]},
                    ladder=(cle, "global")) for cle in CLES},
                "dedup_code": self.evaluer_profond(
                    self.dedupliquer(te, "code"), pp),
                "ladder": self.evaluer_profond(te, pp),
                "hybride_surface": self.evaluer_hybride_surface(
                    te, pp, self.index_surfaces(tr)),
                "hybride_oracle_code": self.evaluer_hybride(
                    te, pp["groupe"][0], self.index_episodes(tr)),
                "paire_oracle": self.evaluer_paires(
                    te, self._prototypes_paires(tr),
                    pp["global"][0].get(("global",))),
            }
            codes_tenus.append(row)
        codes_tenus_resume = {
            "par_cle": self._resume_par_cle(
                {r["graine"]: r["cles"] for r in codes_tenus}),
            "ladder_champs": sum(r["ladder"]["champs"] for r in codes_tenus)
            / max(1, len(codes_tenus)),
            "ladder_non_nuls": sum(r["ladder"]["champs_non_nuls"]
                                   for r in codes_tenus) / max(1, len(codes_tenus)),
            "ladder_exact": sum(r["ladder"]["exact"] for r in codes_tenus)
            / max(1, len(codes_tenus)),
            "hybride_surface": {
                "couverture": sum(r["hybride_surface"]["couverture"]
                                  for r in codes_tenus) / max(1, len(codes_tenus)),
                "exact": sum(r["hybride_surface"]["exact"]
                             for r in codes_tenus) / max(1, len(codes_tenus)),
                "exact_sur_couverts": sum(
                    r["hybride_surface"]["exact_sur_couverts"]
                    for r in codes_tenus) / max(1, len(codes_tenus))},
            "hybride_oracle_code": {
                "couverture": sum(r["hybride_oracle_code"]["couverture"]
                                  for r in codes_tenus) / max(1, len(codes_tenus)),
                "exact": sum(r["hybride_oracle_code"]["exact"]
                             for r in codes_tenus) / max(1, len(codes_tenus))},
            "paire_oracle_champs": sum(r["paire_oracle"]["champs"]
                                       for r in codes_tenus) / max(1, len(codes_tenus)),
        }

        # ---- 3. paires tenues à l'écart (split historique) ---------------
        paires = []
        for g in graines:
            tr, te = decouper(its, g, 0.2)
            pp = self.prototypes_multi(tr)
            vus = {tuple(sorted(_code(e).items())) for e in tr}
            paires.append({
                "graine": g, "n_train": len(tr), "n_test": len(te),
                "n_codes_test": len({tuple(sorted(_code(e).items())) for e in te}),
                "items_code_vu": sum(
                    1 for e in te if tuple(sorted(_code(e).items())) in vus),
                "cles": {cle: self.evaluer_profond(
                    te, {cle: pp[cle], "global": pp["global"]},
                    ladder=(cle, "global")) for cle in CLES},
                "dedup_code": self.evaluer_profond(
                    self.dedupliquer(te, "code"), pp),
                "ladder": self.evaluer_profond(te, pp),
                "hybride_surface": self.evaluer_hybride_surface(
                    te, pp, self.index_surfaces(tr)),
                "paire_oracle": self.evaluer_paires(
                    te, self._prototypes_paires(tr),
                    pp["global"][0].get(("global",))),
            })

        # ---- 4. contrôles : la clé porte-t-elle l'information ? ---------
        controles = {}
        for cle in ("groupe", "type"):
            rows, fixes = [], 0
            for g in graines:
                rng = random.Random(g)
                exclus = set()
                for jeu in sorted(par_jeu, key=str):
                    mel = list(par_jeu[jeu])
                    rng.shuffle(mel)
                    exclus.update(mel[:max(1, round(0.2 * len(mel)))])
                tr = [e for e in its if tuple(sorted(_code(e).items())) not in exclus]
                te = [e for e in its if tuple(sorted(_code(e).items())) in exclus]
                pp = self.prototypes_multi(tr, (cle, "global"))
                (perm, supports), f = self._controle_cle_permutee(
                    pp[cle][0], pp[cle][1], cle, rng)
                rows.append(self.evaluer_profond(
                    te, {cle: (perm, supports), "global": pp["global"]},
                    ladder=(cle, "global")))
                fixes += f
            controles[cle] = {
                "champs": sum(r["champs"] for r in rows) / max(1, len(rows)),
                "exact": sum(r["exact"] for r in rows) / max(1, len(rows)),
                "champs_non_nuls": sum(r["champs_non_nuls"] for r in rows)
                / max(1, len(rows)),
                "prototypes_fixes": fixes / max(1, len(graines)),
                "note": "clé→prototype permutée en cycle dans chaque jeu",
            }

        # ---- 4 bis. la queue publiée : ses codes sont-ils dans le train ?
        nq = int(len(its) * 0.8)
        trq, teq = its[:nq], its[nq:]
        ppq = self.prototypes_multi(trq)
        vusq = {tuple(sorted(_code(e).items())) for e in trq}
        queue = {
            "n_train": len(trq), "n_test": len(teq),
            "codes_test_vus_dans_train": sum(
                1 for e in teq if tuple(sorted(_code(e).items())) in vusq),
            "prototype": self.evaluer_profond(
                teq, ppq, ladder=("groupe", "global")),
            "paire_oracle": self.evaluer_paires(
                teq, self._prototypes_paires(trq),
                ppq["global"][0].get(("global",))),
        }

        # ---- 5. verdict ------------------------------------------------
        g = loo_resume
        gain_jeu = g["jeu"]["champs"] - g["global"]["champs"]
        gain_groupe = g["groupe"]["champs"] - g["jeu"]["champs"]
        gain_type = g["type"]["champs"] - g["jeu"]["champs"]
        gain_ladder = g["ladder"]["champs"] - g["jeu"]["champs"]
        gain_ladder_nn = (g["ladder"]["champs_non_nuls"]
                          - g["jeu"]["champs_non_nuls"])
        coords = {nom: g["ladder"]["par_champ"].get(nom, {}).get("exact_non_nul", 0.0)
                  for nom in ("de", "vers", "point", "carte", "case",
                              "chemin_0", "chemin_1", "roque", "promotion", "passe")}

        def _acc_coordonnees(par) -> float:
            noms = ("de", "vers", "point", "carte", "case", "chemin_0",
                    "chemin_1", "chemin_2", "roque", "promotion", "passe")
            n = sum(par[f]["n_non_nul"] for f in noms if f in par)
            ok = sum(par[f]["ok_non_nul"] for f in noms if f in par)
            return ok / max(1, n)

        gain_coordonnees = _acc_coordonnees(par_champ_loo) - _acc_coordonnees(par_champ_jeu)
        verdict = {
            "exact_loo": g["ladder"]["exact"],
            "exact_loo_preuve": ("nul par construction : le prototype ne peut "
                                 "rendre qu'un code vu, le code exclu n'est pas "
                                 "dans le train"),
            "exact_codes_tenus": [r["ladder"]["exact"] for r in codes_tenus],
            "champs_loo": {cle: g[cle]["champs"] for cle in CLES + ("ladder",)},
            "non_nuls_loo": {cle: g[cle]["champs_non_nuls"]
                             for cle in CLES + ("ladder",)},
            "gain_jeu_sur_global_champs": gain_jeu,
            "gain_groupe_sur_jeu_champs": gain_groupe,
            "gain_type_sur_jeu_champs": gain_type,
            "gain_backoff_sur_jeu_champs": gain_ladder,
            "gain_backoff_sur_jeu_non_nuls": gain_ladder_nn,
            "gain_backoff_sur_jeu_coordonnees": gain_coordonnees,
            "plafond_groupe": plafond["groupe"]["masse_modale"],
            "irreductible_groupe": 1.0 - plafond["groupe"]["masse_modale"],
            "coordonnees_non_nulles_ladder": coords,
            "hybride_surface_couverture": codes_tenus_resume[
                "hybride_surface"]["couverture"],
            "hybride_oracle_couverture": codes_tenus_resume[
                "hybride_oracle_code"]["couverture"],
            "hybride_oracle_tautologique": True,
            "controle_cle_permutee": controles,
            "queue_publiee": {
                "champs": queue["prototype"]["champs"],
                "exact": queue["prototype"]["exact"],
                "n_test": queue["n_test"],
                "codes_test_vus_dans_train": queue["codes_test_vus_dans_train"],
                "paire_oracle_exact": queue["paire_oracle"]["exact"],
                "plafond_corpus_groupe": plafond["groupe"]["masse_modale"],
            },
            "conditionner_aide_exact": False,
            "conditionner_aide_structure": True,
            "conditionner_aide_valeurs": gain_coordonnees > 0.05,
            "conclusion": ("le conditionnement ne gagne que le motif de None ; "
                           "les coordonnées justes sont des coïncidences de "
                           "marginale (case de départ, sous-type roque) ; exact nul"),
        }
        return {
            "protocole": {
                "n": n, "codes": len(codes), "paires": len(
                    {getattr(e, "paire", "") for e in its}),
                "cles": CLES, "ladder": LADDER,
                "graines": list(graines),
                "split_codes": "20 % des codes par jeu, tenus à l'écart",
                "split_paires": "decouper(graine, 0.2), comme typed_corpus",
                "note": ("les prototypes ne voient jamais le code testé ; "
                         "l'exact est nul par construction, pas par échec"),
            },
            "plafond_contextuel": plafond,
            "loo_codes": loo_resume,
            "codes_tenus": codes_tenus,
            "codes_tenus_resume": codes_tenus_resume,
            "paires_tenues": paires,
            "controles": controles,
            "queue_publiee": queue,
            "verdict": verdict,
        }


def experience_m8(items_=None) -> dict:
    return Sommeil().experience(items_)


def experience_contexte(items_=None, graines=(1, 2, 3)) -> dict:
    return Sommeil().experience_contexte(items_, graines)


if __name__ == "__main__":
    import json
    print(json.dumps(experience_m8()["verdict"], ensure_ascii=False, indent=1))

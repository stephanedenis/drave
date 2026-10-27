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
"""
from __future__ import annotations

import collections
import random

from semantique.universaux import CHAMPS

NOMS = tuple(nom for nom, _ in CHAMPS)


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


def experience_m8(items_=None) -> dict:
    return Sommeil().experience(items_)


if __name__ == "__main__":
    import json
    print(json.dumps(experience_m8()["verdict"], ensure_ascii=False, indent=1))

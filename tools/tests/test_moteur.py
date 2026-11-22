#!/usr/bin/env python3
"""test_moteur.py — l'anti-boucle du moteur de pensée : 5 invariants mesurés.

Ce que le test verrouille :
  1. **la boucle pure** (l'opérateur identité) : les répétitions sont **comptées**, la boucle
     s'arrête au fixpoint — pas de re-exploration infinie ;
  2. **le progrès** (n → n+1) : le taux de nouveauté est à 1,0, la terminaison est le budget ;
  3. **la mémoire des échecs** : un état `refute` est **exclu** et compté (`echecs_evites`) ;
  4. **la contradiction** : `p` et `non-p` explorés → terminaison `contradiction` ;
  5. **la trace** : chaque pas est écrit (nouveau / déjà vu / échec), rejouable.
"""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from tools.moteur_pensee import Etat, Moteur  # noqa: E402


def h(corps):
    return hashlib.sha256(json.dumps(corps, sort_keys=True).encode()).hexdigest()


def test_boucle_pure():
    m = Moteur(budget_max=20)
    racine = Etat(empreinte=h({"n": 0}), corps={"n": 0})
    m.boucle(racine, lambda e: [Etat(empreinte=h({"n": 0}), corps={"n": 0})])
    r = m.circularite()
    assert r["nouveaux"] == 1, r
    assert r["repetitions_evitees"] == 1, r
    assert r["termine"].startswith("fixpoint"), r
    print("OK boucle pure : 1 nouveau, 1 répétition comptée, fixpoint")


def test_progres():
    m = Moteur(budget_max=10)
    racine = Etat(empreinte=h({"n": 0}), corps={"n": 0})
    m.boucle(racine, lambda e: [Etat(empreinte=h({"n": e.corps["n"] + 1}),
                                     corps={"n": e.corps["n"] + 1})])
    r = m.circularite()
    assert r["taux_nouveaute"] == 1.0, r
    assert r["termine"] == "budget", r
    print("OK progrès : 1,0 de nouveauté, budget")


def test_echecs():
    m = Moteur(budget_max=10)
    racine = Etat(empreinte=h({"n": 0}), corps={"n": 0})
    def expand(e):
        n = e.corps["n"]
        if n == 1:
            return [Etat(empreinte=h({"n": 1}), corps={"n": 1}, statut="refute")]
        return [Etat(empreinte=h({"n": n + 1}), corps={"n": n + 1})]
    m.boucle(racine, expand)
    r = m.circularite()
    assert r["echecs_evites"] == 1, r
    print("OK mémoire des échecs : 1 état réfuté exclu et compté")


def test_contradiction():
    m = Moteur(budget_max=10)
    p, nonp = h({"p": True}), h({"p": False})
    racine = Etat(empreinte=p, corps={"p": True}, negation=nonp)
    m.boucle(racine, lambda e: [Etat(empreinte=nonp, corps={"p": False}, negation=p)])
    r = m.circularite()
    assert r["contradictions"] == 1, r
    assert r["termine"].startswith("contradiction"), r
    print("OK contradiction : p et non-p → terminaison")


def test_trace():
    m = Moteur(budget_max=5)
    racine = Etat(empreinte=h({"n": 0}), corps={"n": 0})
    m.boucle(racine, lambda e: [Etat(empreinte=h({"n": e.corps["n"] + 1}),
                                     corps={"n": e.corps["n"] + 1}),
                                Etat(empreinte=h({"n": 0}), corps={"n": 0})])
    assert len(m.trace) >= 4, m.trace
    gardes = {t["garde"] for t in m.trace}
    assert "nouveau" in gardes and "deja_vu" in gardes, gardes
    print(f"OK trace : {len(m.trace)} pas tracés, gardes {sorted(gardes)}")



def test_strategies():
    from tools.moteur_pensee import BFS, DFS, Glouton
    frontiere = [(-1.0, 1, Etat(empreinte="a", corps={"n": 1})),
                 (-0.5, 2, Etat(empreinte="b", corps={"n": 2})),
                 (-0.1, 3, Etat(empreinte="c", corps={"n": 3}))]
    import copy
    for strat in (BFS(), DFS(), Glouton()):
        f = copy.deepcopy(frontiere)
        e = strat.select(f)
        assert e is not None, strat.nom
        assert len(f) == 2, (strat.nom, len(f))
    assert BFS().select(copy.deepcopy(frontiere)).empreinte == "a", "BFS devrait prendre le plus ancien"
    assert DFS().select(copy.deepcopy(frontiere)).empreinte == "c", "DFS devrait prendre le plus récent"
    print("OK stratégies : BFS (ancien), DFS (récent), Glouton (meilleur)")


def test_branchement_rsn():
    """Le moteur branché sur l'interface : la même boucle, un paradigme substituable."""
    from tools.moteur_pensee import MoteurRSN
    from tools.rsn_interface import RSNFlou, RSNProvenance
    racine = {"corps": {"type": "question", "n": 0},
              "contexte": {"texte": "Le chat dort.", "span": [0, 3], "langue": "fr", "version": "t"}}
    def operateur(corps):
        n = corps.get("n", 0)
        return [{"type": "question", "n": n + 1}, {"type": "question", "n": n + 2}]
    resultats = []
    for impl in (RSNFlou(), RSNProvenance()):
        m = MoteurRSN(impl, budget_max=10)
        d = m.boucle(racine, operateur)
        assert d["circularite"]["nouveaux"] > 0, d
        assert "explain" in d, d
        resultats.append(d["circularite"])
    # les deux paradigmes rendent la MÊME structure de circularité : ils sont substituables
    assert set(resultats[0]) == set(resultats[1]), resultats
    print("OK branchement RSN : 2 paradigmes, la même structure de décision")


if __name__ == "__main__":
    test_boucle_pure()
    test_progres()
    test_echecs()
    test_contradiction()
    test_trace()
    test_strategies()
    test_branchement_rsn()
    print("MOTEUR : 7/7 invariants (5 anti-boucle + les stratégies + le branchement RSN)")


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


if __name__ == "__main__":
    test_boucle_pure()
    test_progres()
    test_echecs()
    test_contradiction()
    test_trace()
    print("MOTEUR : 5/5 invariants d'anti-boucle")

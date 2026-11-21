#!/usr/bin/env python3
"""test_rsn.py — les invariants de la RSN (la fondation de la pensée).

Ce que le test verrouille :
  1. la **canonicalisation** : clés triées, aucun flottant dans le corps ;
  2. l'**empreinte Merkle** : l'ordre des candidats ne change pas l'empreinte ;
  3. le **déterminisme** : deux analyses du même texte → la même empreinte ;
  4. la **surface → RSN** : un syntagme à rôle et cible devient une prédication ;
  5. le **contrôle négatif** : un texte vide ne produit aucun candidat (refus).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import tools.bloc_linguistique as bl  # noqa: E402
from tools.rsn import (Candidate, State, canonicaliser, depuis_annotation,  # noqa: E402
                       empreinte, h)


def test_canonicalisation():
    a = canonicaliser({"b": 1, "a": [3, 2]})
    b = canonicaliser({"a": [3, 2], "b": 1})
    assert a == b, "l'ordre des clés change le canonique"
    try:
        canonicaliser({"x": 1.5})
    except TypeError:
        pass
    else:
        raise AssertionError("un flottant dans le corps devrait lever")
    print("OK canonicalisation")


def test_empreinte_ordre():
    c1 = Candidate({"type": "fait", "forme": "a"})
    c2 = Candidate({"type": "fait", "forme": "b"})
    e1 = empreinte([c1, c2])
    e2 = empreinte([c2, c1])
    assert e1 == e2, "l'ordre change l'empreinte"
    print("OK empreinte Merkle (ordre indifférent)")


def test_determinisme():
    e1 = depuis_annotation(bl.Heuristique().analyser("Le chat dort."))
    e2 = depuis_annotation(bl.Heuristique().analyser("Le chat dort."))
    assert e1.empreinte == e2.empreinte, "deux analyses du même texte diffèrent"
    print("OK déterminisme", e1.empreinte[:16])


def test_predication():
    a = bl.Heuristique().analyser("Le chat de la voisine dort sur le toit.")
    etat = depuis_annotation(a)
    preds = [c for c in etat.candidats if c.corps["type"] == "predication"]
    assert preds, "aucune prédication extraite"
    assert all("role" in c.corps and "cible" in c.corps for c in preds)
    print(f"OK prédication : {len(preds)} candidates")


def test_negatif():
    a = bl.Heuristique().analyser("")
    etat = depuis_annotation(a)
    assert etat.candidats == [], "un texte vide produit des candidats"
    assert a.refus, "un texte vide devrait être refusé"
    print("OK contrôle négatif (texte vide, refus =", repr(a.refus) + ")")


if __name__ == "__main__":
    test_canonicalisation()
    test_empreinte_ordre()
    test_determinisme()
    test_predication()
    test_negatif()
    print("RSN : 5/5 invariants")

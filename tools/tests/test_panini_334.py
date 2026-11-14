"""Tests de J12.1 — l'outil `panini_334.py` et ses invariants.

Les artefacts Panini sont hors du dépôt Drave (`../Panini/research`) : les
tests sont sautés s'ils ne sont pas présents. On vérifie les **faits de
structure** (pas les p-values, qui dépendent de la graine et du nombre de
permutations) : le nombre de paires, la dé-duplication, la H0 officielle, le
retrieval des 44 signatures et les doublons exacts.
"""
import importlib.util
import pathlib

import pytest

RACINE = pathlib.Path(__file__).resolve().parents[2]
OUTIL = RACINE / "tools" / "panini_334.py"

pytestmark = pytest.mark.skipif(
    not OUTIL.exists() or not (RACINE.parent / "Panini" / "research" / "nipada" / "falsification" / "pairs334_axes_v1.json").exists(),
    reason="artefacts Panini absents",
)


def _module():
    spec = importlib.util.spec_from_file_location("panini_334", OUTIL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def donnees():
    mod = _module()
    paires, graphe, signatures, revalidation, textes, ids_paires, ids_signes, audit = mod.charger()
    return mod, paires, textes, ids_paires, ids_signes, audit


def test_audit_du_corpus(donnees):
    _, _, _, ids_paires, ids_signes, audit = donnees
    assert audit["corpus_actif_officiel"] == 114
    assert audit["paires"] == 655
    assert len(ids_paires) == 48
    assert len(ids_signes) == 44
    assert audit["sources_ok"] == 102
    assert audit["sources_manifeste"] == 107
    assert audit["sources_ok_parmi_44"] == 44
    assert audit["textes_absents_des_paires"] == 66


def test_deduplication_et_h0(donnees):
    mod, paires, textes, ids_paires, _, _ = donnees
    res = mod.analyser_paires(paires, textes, ids_paires, n_perm=10, n_boot=10, graine=0)
    assert res["n_paires_officielles"] == 655
    assert res["n_paires_uniques"] == 495
    assert res["n_auto_paires"] == 7
    assert res["n_doublons_lignes"] == 160
    assert res["n_paires"] == 488
    h0 = res["modeles"]["H0"]
    assert h0["n"] == 488
    assert h0["r2_655_lignes"] == pytest.approx(0.909139, abs=1e-6)
    assert h0["r2"] == pytest.approx(0.906307, abs=1e-6)


def test_retrieval_des_44(donnees):
    mod, _, textes, _, ids_signes, _ = donnees
    res = mod.analyser_oeuvres(textes, ids_signes, n_perm=10, n_boot=10, graine=0)
    assert res["n"] == 44
    # 27/44 même tradition, 16/44 même auteur, 25/44 à <= 50 ans.
    assert round(res["retrieval"]["top1_meme_tradition"] * 44) == 27
    assert round(res["retrieval"]["top1_meme_auteur"] * 44) == 16
    assert round(res["retrieval"]["top1_proche_50ans"] * 44) == 25
    assert res["retrieval"]["chance_meme_tradition"] < res["retrieval"]["top1_meme_tradition"]


def test_doublons_exacts(donnees):
    mod, _, textes, _, ids_signes, _ = donnees
    # `analyser_oeuvres` n'expose pas les doublons : on les recalcule.
    C = mod.construire_matrice(textes, ids_signes)[1]
    trouves = {
        (ids_signes[i], ids_signes[j])
        for i in range(len(ids_signes))
        for j in range(i + 1, len(ids_signes))
        if C[i, j] >= mod.SEUIL_DOUBLON
    }
    assert ("plato_gorgias", "plato_gorgias_jowett") in trouves
    assert ("plato_meno", "plato_meno_jowett") in trouves
    assert len(trouves) == 2

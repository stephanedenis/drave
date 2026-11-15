"""Tests de l'outil B2 — CLR, fenêtres, qualité, CV ridge groupée, permutations."""
import pathlib
import sys
import unittest

import numpy as np

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import atomes_prediction as ap


class TestAtomesPrediction(unittest.TestCase):
    def test_clr_somme_nulle(self):
        X = np.array([[0.2, 0.3, 0.5], [0.1, 0.1, 0.8]])
        Z = ap.clr(X)
        np.testing.assert_allclose(Z.sum(1), 0.0, atol=1e-12)

    def test_design_date(self):
        a = np.array([-400, 0, 1000, 2000], float)
        D = ap._design_date(a, 2)
        self.assertEqual(D.shape, (4, 3))
        self.assertTrue(np.all(D[:-1, 1] < D[1:, 1]))
        self.assertEqual(ap._design_date(a, 1).shape, (4, 2))

    def test_r2_et_rho(self):
        y = np.array([1.0, 2.0, 3.0, 4.0])
        self.assertAlmostEqual(ap._r2(y, y), 1.0)
        self.assertAlmostEqual(ap._r2(y, np.full(4, y.mean())), 0.0)
        self.assertAlmostEqual(ap._rho(y, y), 1.0)

    def test_groupes_doublons(self):
        oeuvres = [{"id": "plato_gorgias"}, {"id": "plato_gorgias_jowett"},
                   {"id": "plato_meno"}, {"id": "plato_meno_jowett"}, {"id": "x"}]
        groupes = ap._groupes(oeuvres)
        tailles = sorted(len(g) for g in groupes)
        self.assertEqual(tailles, [1, 2, 2])

    def test_cv_ridge_retrouve_une_relation(self):
        rng = np.random.default_rng(0)
        n, p = 30, 5
        X = rng.normal(size=(n, p))
        y = (X[:, 0] - 2 * X[:, 1] + rng.normal(scale=0.1, size=n))[:, None]
        preds, r2, _ = ap.cv_ridge_multi(X, y, np.logspace(-2, 3, 20))
        self.assertGreater(r2[0], 0.8)
        self.assertGreater(ap._rho(y[:, 0], preds[:, 0]), 0.8)

    def test_permutation_colonnes_detruit(self):
        rng = np.random.default_rng(1)
        n, p = 40, 6
        X = rng.normal(size=(n, p))
        y = (X[:, 0] + rng.normal(scale=0.5, size=n))[:, None]
        _, r2, _ = ap.cv_ridge_multi(X, y, np.logspace(-2, 3, 20))
        _, r2p, _ = ap.cv_ridge_multi(X, y, np.logspace(-2, 3, 20),
                                      permutation="colonnes", rng=rng)
        self.assertGreater(r2[0], 0.3)
        self.assertLess(r2p[0], 0.3)

    def test_fenetres_non_chevauchantes(self):
        texte = "mot " * 20_000
        f = ap.fenetres(texte, n=6, taille=10_000)
        self.assertEqual(len(f), 6)
        for x in f:
            self.assertLessEqual(len(x), 10_000)

    def test_filtrer_prose_retire_le_js(self):
        texte = ("// Apply the local archive-bar preference before shared HTML can paint. "
                 "try { document.documentElement.dataset.x = '1'; } catch (e) {} "
                 "Mencius went to see king Hûi of Liang. The king said, Venerable sir, "
                 "since you have not counted it far to come here, a distance of a thousand li.")
        sortie = ap.filtrer_prose(texte)
        self.assertIn("Mencius", sortie)

    def test_p_perm(self):
        null = np.array([0.0, 0.1, 0.2])
        self.assertAlmostEqual(ap._p_perm(null, 0.3), 0.25)
        self.assertAlmostEqual(ap._p_perm(null, -0.1), 1.0)

    def test_holm_et_bh(self):
        np.testing.assert_allclose(ap._holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])
        np.testing.assert_allclose(ap._bh([0.01, 0.04, 0.03]), [0.03, 0.04, 0.04])


if __name__ == "__main__":
    unittest.main()

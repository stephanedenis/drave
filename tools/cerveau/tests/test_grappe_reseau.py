from __future__ import annotations
import sys, pathlib, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from tools.grappe_reseau import encoder, decoder


class TestGrappeReseau(unittest.TestCase):
    def test_aller_retour(self):
        flux = [[0.0, 1.0, 0.0, 2.0], [0.0, 0.0, 3.0, 0.0]]
        b = encoder(flux)
        relu, meta = decoder(b)
        self.assertEqual(relu, flux)
        self.assertEqual(meta["nval"], 3)

    def test_sparse(self):
        flux = [[0.0, 1.0, 0.0, 2.0]]
        dense = encoder(flux, dense=True)
        sparse = encoder(flux)
        self.assertLess(len(sparse), len(dense))
        relu, _ = decoder(sparse)
        self.assertEqual(relu[0][3], 2.0)
        self.assertEqual(relu[0][1], 1.0)


if __name__ == "__main__":
    unittest.main()

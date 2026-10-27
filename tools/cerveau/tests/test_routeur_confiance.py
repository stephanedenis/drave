from __future__ import annotations
import unittest
try:
    from cerveau.routeur_confiance import mesurer
    _TORCH = True
except ImportError:
    _TORCH = False


@unittest.skipUnless(_TORCH, "torch absent")
class TestRouteurConfiance(unittest.TestCase):
    def test_mesure(self):
        r = mesurer(pas=1, graine=1, device="cpu")
        self.assertEqual(r["n"], 146)
        self.assertIn("oracle", r["modes"]["original"])


if __name__ == "__main__":
    unittest.main()

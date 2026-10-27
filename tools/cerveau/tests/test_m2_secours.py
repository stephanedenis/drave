from __future__ import annotations
import random
import unittest
try:
    from cerveau.m2_secours import _perturber, _reels
    _TORCH = True
except ImportError:
    _perturber = _reels = None
    _TORCH = False


@unittest.skipUnless(_TORCH, "torch absent du python courant")
class TestM2Secours(unittest.TestCase):
    def test_perturbations(self):
        rng = random.Random(0)
        self.assertEqual(_perturber("e2e4", "casse", rng), "E2E4")
        self.assertTrue(_perturber("e2e4", "phrase", rng).startswith("le coup"))
        self.assertEqual(len(_reels()), 528)


if __name__ == "__main__":
    unittest.main()

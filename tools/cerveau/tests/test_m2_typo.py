from __future__ import annotations
import random
import unittest
try:
    from cerveau.m2_typo import _typo, _reels
    _TORCH = True
except ImportError:
    _typo = _reels = None
    _TORCH = False


@unittest.skipUnless(_TORCH, "torch absent")
class TestM2Typo(unittest.TestCase):
    def test_modes(self):
        rng = random.Random(0)
        for mode in ("suppression", "substitution", "insertion", "transposition"):
            self.assertNotEqual(_typo("e2e4", mode, rng), "e2e4")
        self.assertEqual(len(_reels()), 528)


if __name__ == "__main__":
    unittest.main()

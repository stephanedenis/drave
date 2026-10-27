from __future__ import annotations
import unittest
try:
    from cerveau.routeur_m1_m2 import router, _lexique, _reels
    _TORCH = True
except ImportError:
    _TORCH = False


@unittest.skipUnless(_TORCH, "torch absent")
class TestRouteur(unittest.TestCase):
    def test_router(self):
        lex = _lexique(_reels())
        self.assertEqual(router("e2e4", lex), "M1")
        self.assertEqual(router("  e2e4  ", lex), "M2")
        self.assertEqual(router("le coup e2e4 est joue", lex), "M1")


if __name__ == "__main__":
    unittest.main()

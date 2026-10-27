from __future__ import annotations
import unittest
from cerveau.restitution import Restitution
from semantique.typed_corpus import items


class TestRestitution(unittest.TestCase):
    def test_roundtrip(self):
        r = Restitution().mesurer()
        self.assertEqual(r["n"], 528)
        self.assertGreaterEqual(r["roundtrip"], 0.99)
        self.assertFalse(r["echecs"])


if __name__ == "__main__":
    unittest.main()

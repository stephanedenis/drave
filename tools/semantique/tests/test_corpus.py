from __future__ import annotations
import random
import unittest
from semantique.corpus import charger, decouper, exemple, lot, LANGUES

ART = {1: {l: f"article un en {l}" for l in LANGUES},
       2: {l: f"article deux en {l}" for l in LANGUES},
       3: {l: f"article trois en {l}" for l in LANGUES}}


class TestCorpus(unittest.TestCase):
    def test_exemple_octets(self):
        x = exemple(ART, 1, "fra", 128)
        self.assertEqual(x[:4], list("arti".encode()))
        self.assertGreaterEqual(len(x), 8)

    def test_decouper_par_article(self):
        train, val = decouper(ART, (2, 2))
        self.assertEqual(list(train), [1, 3])
        self.assertEqual(list(val), [2])

    def test_lot_parallel(self):
        xs, ls, xt, lt, arts = lot(ART, LANGUES, 5, 128, random.Random(0))
        self.assertEqual(len(xs), 5)
        self.assertTrue(all(a != b for a, b in zip(ls, lt)))
        self.assertTrue(all(i < len(LANGUES) for i in ls + lt))


if __name__ == "__main__":
    unittest.main()

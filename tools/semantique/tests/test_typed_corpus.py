from __future__ import annotations
import unittest
from semantique.typed_corpus import items, decouper, lot
import random


class TestTypedCorpus(unittest.TestCase):
    def test_items(self):
        its = items()
        self.assertGreater(len(its), 400)
        self.assertTrue(all(i.code["jeu"] in ("morpion","echecs","dames","go","cartes") for i in its))
        self.assertTrue(all(isinstance(i.code["action"], str) for i in its))

    def test_split_sans_fuite(self):
        its = items()
        tr, va = decouper(its, 1, 0.2)
        self.assertTrue(tr and va)
        self.assertFalse({i.paire for i in tr} & {i.paire for i in va})

    def test_lot(self):
        its = items()
        xs, choix = lot(its, 4, 64, random.Random(0))
        self.assertEqual(len(xs), 4)
        self.assertTrue(all(0 < len(x) <= 64 for x in xs))


if __name__ == "__main__":
    unittest.main()

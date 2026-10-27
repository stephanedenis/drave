from __future__ import annotations
import unittest
from cerveau.pipeline_memoire import PipelineMemoire
from semantique.typed_corpus import items


class TestPipelineMemoire(unittest.TestCase):
    def test_flux(self):
        p = PipelineMemoire()
        r = p.mesurer(items(), permutations=3)
        self.assertIn("fifo", r["politiques"])
        self.assertIn("lfu", r["politiques"])
        self.assertEqual(r["M8"]["prototypes"], 6)
        self.assertLessEqual(r["M8"]["couverture"], 1.0)

    def test_lfu_suffixe(self):
        p = PipelineMemoire()
        r = p.mesurer(items(), permutations=3)
        self.assertGreaterEqual(r["politiques"]["lfu"]["suf_surface"],
                                r["politiques"]["fifo"]["suf_surface"])


if __name__ == "__main__":
    unittest.main()
